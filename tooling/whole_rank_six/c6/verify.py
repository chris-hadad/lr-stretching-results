#!/usr/bin/env python3
"""Complete literal rank-six c6 field check using freshly evaluated local values."""
from fractions import Fraction as Q
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse,gzip,hashlib,importlib.util,json,time

def need(ok,msg):
    if not ok:raise ValueError(msg)

def det(a):
    a=[list(r) for r in a];n=len(a);sign=1;old=1
    if not n:return 1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        new=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                value=a[i][j]*new-a[i][k]*a[k][j]
                need(value%old==0,'Bareiss exact division')
                a[i][j]=value//old
            a[i][k]=0
        old=new
    return sign*a[-1][-1]

def index(rows):
    result=0
    for cols in combinations(range(len(rows[0])),len(rows)):
        result=gcd(result,abs(det([[r[j] for j in cols] for r in rows])))
        if result==1:break
    return result

def load(path):return json.loads(gzip.decompress(path.read_bytes()))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',type=Path,required=True)
    ap.add_argument('--reference',type=Path,required=True)
    ap.add_argument('--geometry-module',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--control',choices=['none','zero-field','omit-support'],default='none')
    args=ap.parse_args();need(not args.out.exists(),'fresh output')
    start=time.monotonic()
    spec=importlib.util.spec_from_file_location('hive_geometry',args.geometry_module)
    geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)
    normals=geo.hive_normals()
    raw=load(args.data/'raw.json.gz');inc=load(args.data/'incidence.json.gz');field=load(args.data/'field.json.gz')
    need(raw['normals']==[list(r) for r in normals],'all original normals')
    coeff=list(map(Q,field['coefficients']));need(len(coeff)==2667,'field dimension')
    if args.control=='zero-field':coeff=[Q(0)]*len(coeff)
    supports={}
    for ident,s in enumerate(inc['supports']):
        ids=tuple(s['ids']);M=s['kernel_columns']
        need(ids==tuple(sorted(set(ids))) and len(ids)==3 and max(ids)<42,'support identity')
        need(ids not in supports and len(M)==10 and all(len(r)==7 for r in M),'support shape/uniqueness')
        need(all(type(x) is int for r in M for x in r),'integer kernel')
        N=[normals[i] for i in ids];I=index(N);need(I>0,'independent support')
        need(all(sum(N[i][c]*M[c][j] for c in range(10))==0 for i in range(3) for j in range(7)),'NM zero')
        divisor=0
        for chosen in combinations(range(10),7):
            divisor=gcd(divisor,abs(det([M[i] for i in chosen])))
            if divisor==1:break
        need(divisor==1,'full saturated rank-seven kernel')
        supports[ids]=(ident,M,I)
    need(len(supports)==381,'all support blocks')
    if args.control=='omit-support':supports.pop(next(iter(supports)))
    independent=set();dependent=set();refs={}
    for line in args.reference.read_text().splitlines():
        a,b,c=line.split();ids=tuple(map(int,a.split(',')))
        if len(ids)!=4:continue
        need(ids not in refs,'duplicate reference support');refs[ids]=(Q(b),int(c))
    for ids in combinations(range(42),4):
        I=index([normals[i] for i in ids])
        if I:independent.add(ids);need(ids in refs and refs[ids][1]==I,'fresh original index/coverage')
        else:dependent.add(ids)
    need(independent==set(refs),'complete forward reference and no extras')
    need(len(independent)==102297 and len(dependent)==9633,'full rank partition')
    listed=[tuple(x) for x in raw['cones']]
    need(len(listed)==len(set(listed)) and set(listed)==independent,'raw complete roster')
    dep=[tuple(x) for x in raw['dependent_subsets']]
    need(len(dep)==len(set(dep)) and set(dep)==dependent,'dependent complete roster')
    need(len(raw['alphas'])==len(inc['incidence'])==len(field['corrected_values'])==len(listed),'complete aligned rows')
    minimum=None;negative=0;incidences=0
    for row,ids in enumerate(listed):
        alpha,I=refs[ids];need(alpha==Q(raw['alphas'][row]),'fresh BV scalar equality')
        negative+=alpha<0;beta=alpha;events=[]
        for J in combinations(ids,3):
            if J not in supports:continue
            ident,M,JI=supports[J];extra=next(i for i in ids if i not in J)
            u=[sum(M[c][j]*normals[extra][c] for c in range(10)) for j in range(7)]
            g=gcd(*u);need(g>0 and I==JI*g,'primitive full-image index ratio')
            u=[v//g for v in u];events.append({'support':ident,'extra':extra,'primitive_quotient':u})
            beta+=sum(coeff[7*ident+j]*u[j] for j in range(7));incidences+=1
        key=lambda e:(e['support'],e['extra'])
        need(sorted(events,key=key)==sorted(inc['incidence'][row],key=key),'all original incidences')
        need(beta>=Q(1,3000),'c6 bound')
        need(beta==Q(field['corrected_values'][row]),'corrected exact value')
        if minimum is None or beta<minimum:minimum=beta
    need(negative==132 and incidences==14067,'raw negative and incidence totals')
    need(minimum==Q('164999999111/491400000000000'),'exact minimum')
    result={'status':'PASS_COMPLETE_C6','rows':len(listed),'dependent':len(dependent),'raw_negatives':negative,'saturated_kernels':len(supports),'primitive_incidences':incidences,'minimum':str(minimum),'seconds':time.monotonic()-start}
    args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
