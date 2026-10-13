"""Exact complete original parent vectors on every declared arrangement ray."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import argparse,hashlib,json,time

def distribution(widths,t):
    a=[1]
    for w in widths:
        length=2*w*t+1;out=[];window=0
        for j in range(len(a)+length-1):
            if j<len(a):window+=a[j]
            if j>=length:window-=a[j-length]
            out.append(window)
        a=out
    return a

def count(w,t):return sum(v**3 for v in distribution(w,t))
def interpolate(v):
    out=[Q(0)]*len(v);basis=[Q(1)];v=list(map(Q,v))
    for k in range(len(v)):
        for i,b in enumerate(basis):out[i]+=v[0]*b
        v=[b-a for a,b in zip(v,v[1:])]
        q=[Q(0)]*(len(basis)+1)
        for i,b in enumerate(basis):q[i]-=k*b/(k+1);q[i+1]+=b/(k+1)
        basis=q
    return out

def ev(c,t):
    out=Q(0)
    for v in reversed(c):out=out*t+v
    return out

def triple(w):
    T=sum(w);h=(T,*w);suffix=sum(h);L=[];M=[]
    for a in h:
        suffix-=a;o=4*suffix;L.extend([o+4*a,o+2*a]);M.extend([o,o])
    return dict(lambda_=L,mu=M,nu=[6*T,4*T,2*T])

def main():
    p=argparse.ArgumentParser();p.add_argument('--rays',required=True);p.add_argument('--output',required=True);a=p.parse_args();start=time.monotonic()
    data=json.loads(Path(a.rays).read_text());rows=[]
    for i,raw in enumerate(data['sorted_primitive_rays']):
        old=tuple(x for x in raw if x);N=len(old);W=sum(old);D=3*N+4
        before=(*old,2*W);after=(*old,W,W)
        b=[count(before,t) for t in range(D+3)];c=[count(after,t) for t in range(D+3)]
        bp=interpolate(b[:D+1]);cp=interpolate(c[:D+1]);g=[x-y for x,y in zip(cp,bp)]
        assert all(ev(bp,t)==b[t] and ev(cp,t)==c[t] for t in [D+1,D+2])
        assert max(j for j,x in enumerate(bp) if x)==3*N+1 and cp[D]>0 and g[0]==0
        row=dict(ray=raw,old=old,W=W,degree_before=3*N+1,degree_after=D,before_values=b,after_values=c,before_coefficients=list(map(str,bp)),after_coefficients=list(map(str,cp)),gain=list(map(str,g)),c1_over_W=str(g[1]/W),before_triple=triple(before),after_triple=triple(after))
        rows.append(row)
        if min(bp)<0 or min(cp)<0:
            Path(a.output).write_text(json.dumps(dict(status='WHOLE_CANDIDATE_FREEZE',rows=rows),indent=2));raise SystemExit(3)
        if i%25==0:print(json.dumps(dict(done=i+1,total=len(data['sorted_primitive_rays']),seconds=time.monotonic()-start)),flush=True)
    result=dict(schema='a56-complete-split-ray-polynomials/v1',rays_sha256=hashlib.sha256(Path(a.rays).read_bytes()).hexdigest(),n=data['n'],rows=rows,ray_orbits=len(rows),min_c1_over_W=str(min(Q(r['c1_over_W']) for r in rows)),negative_gains=sum(any(Q(x)<0 for x in r['gain']) for r in rows),seconds=time.monotonic()-start,claim_ceiling='All ray vectors exact; only c1 extends to complete cones by the separately proved linearity. Higher coefficient signs are finite ray controls.')
    with Path(a.output).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
if __name__=='__main__':main()
