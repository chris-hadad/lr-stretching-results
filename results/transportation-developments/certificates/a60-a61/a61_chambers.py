"""Complete accepted A61 rational chamber/balancing certificate."""
from fractions import Fraction as F
from itertools import combinations
from math import factorial
from pathlib import Path
import argparse, hashlib, json, time
Z=(0,0,0,0)

def const(x):return {Z:F(x)} if x else {}
def add(*polys):
    out={}
    for p in polys:
        for k,v in p.items():out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
def scale(p,v):return {k:x*v for k,x in p.items() if x*v}
def mul(*polys):
    out=const(1)
    for p in polys:
        nxt={}
        for a,v in out.items():
            for b,w in p.items():
                k=tuple(x+y for x,y in zip(a,b));nxt[k]=nxt.get(k,F(0))+v*w
        out={k:v for k,v in nxt.items() if v}
    return out
def lin(co):return {tuple(int(i==j) for i in range(4)):F(c) for j,c in enumerate(co) if c}
def binp(s,c,d):return scale(mul(*[add(s,const(c-j)) for j in range(d)]),F(1,factorial(d)))
def sub(a,b):return add(a,scale(b,-1))
def elem(caps):
    es=[const(1)]
    for p in caps:
        nxt=[{} for _ in range(len(es)+1)]
        for j,e in enumerate(es):nxt[j]=add(nxt[j],e);nxt[j+1]=add(nxt[j+1],mul(e,add(const(2),p)))
        es=nxt
    return es

# Each row is (k1,k2,k3,r) in four independent nonnegative coordinates.
CHAMBERS={
 'zero-small':[(1,1,0,0),(1,1,1,0),(1,1,1,1),(1,0,0,0)],
 'one-small':[(1,0,0,0),(1,1,1,0),(1,1,1,1),(1,1,0,0)],
 'two-small-no-pair':[(1,1,0,0),(1,1,1,0),(1,2,1,1),(1,2,1,0)],
 'two-small-pair':[(1,0,0,0),(1,1,0,0),(2,1,2,1),(2,1,1,0)],
 'three-small':[(1,0,1,2),(1,1,1,2),(1,1,2,2),(1,1,2,3)]}

def formula(rows):
    caps=list(map(lin,rows[:3]));r=lin(rows[3]);a=3;K=add(*caps);B=sub(K,r)
    assert all(v>=0 for v in sub(K,scale(r,2)).values())
    N=mul(*(binp(k,2,2) for k in caps))
    L=sub(scale(K,F(5,4)),scale(r,2));Q=scale(sub(scale(mul(sub(scale(K,2),scale(r,3)),sub(scale(K,2),scale(r,3))),4),add(*(mul(k,k) for k in caps))),F(1,36))
    result=mul(N,add(const(1),L,Q));A=add(const(2),B,scale(r,F(-1,2)))
    terms=[]
    for q in range(a):
        for J in combinations(range(a),q):
            slope=sub(r,add(*(caps[j] for j in J)))
            if not slope or all(x<=0 for x in slope.values()):continue
            assert all(x>=0 for x in slope.values()),(rows,J,slope)
            es=elem([caps[j] for j in J]);part={}
            for h in range(q+1):
                d=2*a-q+h+1;c=2*a-2*q-1
                part=add(part,mul(es[q-h],add(mul(A,binp(slope,c,d)),binp(slope,c,d+1))))
            result=add(result,scale(part,2*(-1)**q));terms.append(J)
    assert result.get(Z)==1 and max(map(sum,result))==8
    return result,terms

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();start=time.monotonic();out=[]
    for name,rows in CHAMBERS.items():
        p,terms=formula(rows)
        neg=[{'powers':list(k),'coefficient':str(v)} for k,v in sorted(p.items()) if v<0]
        row=dict(chamber=name,parameter_rows=rows,active_subsets=terms,coefficients=[{'powers':list(k),'coefficient':str(v)} for k,v in sorted(p.items())],negative=neg,degree_counts={d:sum(sum(k)==d for k in p) for d in range(9)})
        out.append(row);print(json.dumps({k:row[k] for k in ['chamber','active_subsets','degree_counts','negative']}),flush=True)
    report=dict(schema='a61-three-cap-chambers/v1',status='PASS' if all(not x['negative'] for x in out) else 'OBSTRUCTION',seconds=time.monotonic()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),chambers=out)
    with a.out.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({k:report[k] for k in ['status','seconds']}))
if __name__=='__main__':main()
