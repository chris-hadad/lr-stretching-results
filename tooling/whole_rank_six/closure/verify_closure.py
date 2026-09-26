#!/usr/bin/env python3
"""Independent complete check of the literal 103-identity hive closure proof.

Uses full-database bitmask unit propagation, not the returned occurrence-queue
checker or SAT solver. The certificate is read only as JSON data.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,time

ALL=(1<<45)-1


def need(ok,message):
    if not ok:raise ValueError(message)


def rank(rows):
    basis={}
    for row in rows:
        v=list(map(Fraction,row))
        for p,b in sorted(basis.items()):
            if v[p]:
                a=v[p];v=[x-a*y for x,y in zip(v,b)]
        p=next((i for i,x in enumerate(v) if x),None)
        if p is not None:
            a=v[p];basis[p]=[x/a for x in v]
    return len(basis)


def literal_rows(points):
    need(points==[(i,j) for i in range(7) for j in range(7-i)],'complete literal point order')
    pos={p:i for i,p in enumerate(points)};directions=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
    rows=set()
    for p in points:
        for u,v in combinations(directions,2):
            if 2*u[0]*v[0]+u[0]*v[1]+u[1]*v[0]+2*u[1]*v[1]!=1:continue
            quad=[p,(p[0]+u[0],p[1]+u[1]),(p[0]+v[0],p[1]+v[1]),(p[0]+u[0]+v[0],p[1]+u[1]+v[1])]
            if not all(x in pos for x in quad):continue
            r=[0]*28
            for x,c in zip(quad,(-1,1,1,-1)):r[pos[x]]+=c
            rows.add(tuple(r))
    return rows


def side(value):
    need(isinstance(value,dict) and value,'nonempty positive identity side')
    converted=[]
    for key,coefficient in value.items():
        i=int(key);need(str(i)==key and 0<=i<45 and type(coefficient) is int and coefficient>0,'positive integral literal coefficient')
        converted.append((i,coefficient))
    return tuple(sorted(converted))


def mask(indices):return sum(1<<i for i in set(indices))


def clauses(value):
    result=[]
    for pair in value:
        need(isinstance(pair,list) and len(pair)==2 and all(type(v) is int and 0<=v<=ALL for v in pair),'45-variable clause masks')
        p,n=pair;need(p&n==0,'non-tautological literal clause');result.append((p,n))
    return result


def rup(database,candidate):
    positive,negative=candidate
    # Falsifying every literal of the candidate is the RUP assumption.
    true=negative;false=positive
    while True:
        before=true|false
        for p,n in database:
            if p&true or n&false:continue
            remaining=(p|n)&~(true|false)
            if not remaining:return True
            if remaining&(remaining-1)==0:
                if remaining&p:true|=remaining
                else:false|=remaining
        if before==(true|false):return False


def closure(seed,rules):
    while True:
        before=seed
        for left,right in rules:
            if seed&left==left:seed|=right
        if before==seed:return seed


def verify(certificate,atlas,out):
    started=time.monotonic();data=json.loads(certificate.read_text())
    need(data['schema']=='fr043-u04-portable-positive-closure-certificate/v1' and data['rank']==6,'certificate type')
    points=list(map(tuple,data['points']));rows=list(map(tuple,data['rows']))
    need(len(rows)==45 and all(len(r)==28 and all(type(v) is int for v in r) for r in rows),'literal integer row matrix')
    need(set(rows)==literal_rows(points),'regenerated original rhombi')
    original=json.loads(atlas.read_text());original_rows=list(map(tuple,original['rhombi']))
    need(set(rows)==set(original_rows),'exact original full-coordinate row join')
    row_join=[original_rows.index(r) for r in rows]
    need(sorted(row_join)==list(range(45)),'bijective physical row join')
    identities=[];rules=[];horn=set();populations={2:set(),3:set()}
    need(len(data['identities'])==103,'103 identities')
    for index,entry in enumerate(data['identities']):
        left=side(entry['left']);right=side(entry['right'])
        need(not set(i for i,c in left)&set(i for i,c in right),'disjoint positive sides')
        need(all(sum(c*rows[i][j] for i,c in left)==sum(c*rows[i][j] for i,c in right) for j in range(28)),'full-height identity '+str(index))
        identities.append((left,right));a=mask(i for i,c in left);b=mask(i for i,c in right)
        rules.extend([(a,b),(b,a)])
        for premise,conclusion in [(a,b),(b,a)]:
            for i in range(45):
                if conclusion>>i&1:horn.add((1<<i,premise))
        if index<102:
            need(len(left)==len(right) and len(left) in (2,3) and all(c==1 for i,c in left+right),'short identity form')
            populations[len(left)].add(tuple(sorted((tuple(i for i,c in left),tuple(i for i,c in right)))))
    need(len(horn)==564 and len(rules)==206 and [len(populations[k]) for k in (2,3)]==[30,72],'rule and Horn populations')
    # Re-enumerate all disjoint literal row-sum identities of sizes two and three.
    for k in (2,3):
        grouped={}
        for indices in combinations(range(45),k):
            key=tuple(sum(rows[i][j] for i in indices) for j in range(28))
            grouped.setdefault(key,[]).append(indices)
        enumerated=set()
        for supports in grouped.values():
            for a,b in combinations(supports,2):
                if set(a).isdisjoint(b):enumerated.add(tuple(sorted((a,b))))
        need(enumerated==populations[k],'complete short identity population '+str(k))
    heights=data['feasible_heights'];need(len(heights)==166,'feasible witness population')
    zeros=[]
    for v in heights:
        need(len(v)==28 and all(type(x) is int for x in v),'integral full height witness')
        values=[sum(a*b for a,b in zip(r,v)) for r in rows]
        need(min(values)>=0,'infeasible supplied height')
        zeros.append(mask(i for i,x in enumerate(values) if x==0))
    def query(target):
        return horn|{(0,1<<target)}|{(ALL^z,0) for z in zeros if not z>>target&1}
    representatives={};steps=0
    need(len(data['representative_refutations'])==9,'representative population')
    for ref in data['representative_refutations']:
        target=ref['target'];need(type(target) is int and 0<=target<45 and target not in representatives,'distinct representative target')
        input_clauses=clauses(ref['input_clauses']);need(len(set(input_clauses))==len(input_clauses) and set(input_clauses)==query(target),'reconstructed complete CNF')
        additions=clauses(ref['RUP_additions']);need(additions and additions[-1]==(0,0),'final empty clause')
        database=list(input_clauses)
        for number,candidate in enumerate(additions):
            need(rup(database,candidate),'invalid RUP addition target '+str(target)+' step '+str(number))
            database.append(candidate);steps+=1
        representatives[target]=set(input_clauses)
        print('RUP target',target,'steps',len(additions),flush=True)
    need(steps==6488,'complete RUP addition population')
    seen=set();need(len(data['target_transports'])==45,'target coverage')
    for transport in data['target_transports']:
        target=transport['target'];representative=transport['representative'];permutation=transport['row_permutation']
        need(type(target) is int and 0<=target<45 and target not in seen and representative in representatives,'transport target')
        need(len(permutation)==45 and all(type(i) is int for i in permutation) and sorted(permutation)==list(range(45)),'literal variable bijection')
        need(permutation[representative]==target,'target variable transport')
        def moved(v):return mask(permutation[i] for i in range(45) if v>>i&1)
        need({(moved(p),moved(n)) for p,n in representatives[representative]}==query(target),'entire CNF transport')
        seen.add(target)
    need(seen==set(range(45)),'all target refutations')
    counter={4,17,18,23,31,41};seed=mask(counter);old=closure(seed,rules[:204]);closed=closure(seed,rules)
    expected={2,3,4,7,8,9,11,17,18,23,24,26,31,35,39,40,41,44}
    need(old==seed and closed==mask(expected),'old obstruction and complete repair')
    witnesses=[v for v,z in zip(heights,zeros) if z&seed==seed]
    witness=[sum(v[j] for v in witnesses) for j in range(28)]
    slacks=[sum(a*b for a,b in zip(r,witness)) for r in rows]
    need(min(slacks)>=0 and mask(i for i,s in enumerate(slacks) if s==0)==closed,'exact countermodel closure witness')
    columns=[i for i,p in enumerate(points) if min(p)>0 and sum(p)<6]
    need(rank([[rows[i][j] for j in columns] for i in sorted(counter)])==6 and rank([[rows[i][j] for j in columns] for i in sorted(expected)])==8,'countermodel rank increase')
    need(not out.exists() and out.parent.is_dir(),'fresh output');out.mkdir()
    with (out/'EXHAUSTION.txt').open('w') as f:
        f.write('45 204 166\n')
        for a,b in rules[:204]:f.write(f'{a} {b}\n')
        for z in zeros:f.write(str(z)+'\n')
    report={'status':'PASS_COMPLETE_POSITIVE_CLOSURE_CERTIFICATE','schema':'pub-independent-pro043-closure-v1',
            'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'identities':103,'identity_coordinates':103*28,
            'short_identity_populations_independently_exhausted':[30,72],'feasible_vectors':166,'slack_checks':166*45,
            'Horn_clauses':564,'RUP_refutations':9,'RUP_additions':steps,'full_CNF_transports':45,'initial_sets_covered':'2^45',
            'needs_extreme_ray_completeness':False,'provider_code_executed':False,'seconds':time.monotonic()-started,
            'certificate_row_to_original_row':row_join,'minimum_six_exhaustion':'separate check still required',
            'countermodel':{'seed':sorted(counter),'closure':sorted(expected),'ranks':[6,8],'integral_witness':witness}}
    (out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--certificate',type=Path,required=True)
    parser.add_argument('--atlas',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();verify(args.certificate,args.atlas,args.out)
