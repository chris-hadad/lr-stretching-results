"""Exact A82 original-geometry controls, no LR scalar engine or provider code."""
from fractions import Fraction as F
from itertools import permutations
import hashlib,json,os,sys,time
from pathlib import Path
R=Path(sys.argv[1])

def triple(m,S,U):
    lam=[m*S+6*U,m*S+5*U,m*S+4*U,m*S+3*U]+[i*S for i in range(m,0,-1)]
    mu=[m*S+3*U,m*S+2*U,m*S+U,m*S]+[i*S for i in range(m-1,-1,-1)]
    nu=[(m-3)*S+6*U,S+3*U,S+2*U,S+U]
    assert len(lam)==len(mu)==m+4
    assert all(a>=b for a,b in zip(lam,lam[1:])) and all(a>=b for a,b in zip(mu,mu[1:]))
    assert all(a>=b>=0 for a,b in zip(lam,mu)) and all(a>=b for a,b in zip(nu,nu[1:]))
    assert sum(lam)-sum(mu)==sum(nu)==m*S+12*U
    return lam,mu,nu

def rows_of(m,S,U,x,y,z,tails,p):
    B,C,D=map(sum,zip(*tails))
    assert x+y+z+B+C+D==3*S
    rows=[[3*U,0,0,0],[U-x,2*U+x,0,0],[U-y,p,2*U+y-p,0],
          [U-z,U+S-x-B-p,S-y-C+p,U+S-D]]
    return rows+[[S-b-c-d,b,c,d] for b,c,d in tails]

def slacks(m,S,U,rows):
    lam,mu,nu=triple(m,S,U)
    assert [sum(row) for row in rows]==[a-b for a,b in zip(lam,mu)]
    assert [sum(row[k] for row in rows) for k in range(4)]==nu
    out={}
    for i,row in enumerate(rows):
        for k in range(4):out[f'entry/{i+1}/{k+1}']=row[k]
        if i:
            for k in range(4):out[f'column/{i+1}/{k+1}']=mu[i-1]-mu[i]+sum(rows[i-1][:k])-sum(row[:k+1])
        for k in range(3):out[f'ballot/{i+1}/{k+1}']=sum(r[k] for r in rows[:i])-sum(r[k+1] for r in rows[:i+1])
    return out

def compositions(n,k):
    if k==1:
        yield (n,);return
    for a in range(n+1):
        for tail in compositions(n-a,k-1):yield (a,)+tail

def LH(S,v):
    x,y,z,B,C,D=v
    L=max(0,y-x,S-C-x,y+C-S,S-x-B+y-z,y-S+D)
    h=min(y-x,S-x-B,y-S+D)
    return L,h

def main():
    start=time.monotonic();R.mkdir(exist_ok=False,parents=True)
    # Every lower/upper form is encoded over the complete six-coordinate simplex.
    lower=[(0,[0]*6),(0,[-1,1,0,0,0,0]),(1,[-1,0,0,0,-1,0]),
           (-1,[0,1,0,0,1,0]),(1,[-1,1,-1,-1,0,0]),(-1,[0,1,0,0,0,1])]
    upper=[(0,[-1,1,0,0,0,0]),(1,[-1,0,0,-1,0,0]),(-1,[0,1,0,0,0,1])]
    bound=[[a-b+3*max(x-y for x,y in zip(u,v)) for b,v in upper] for a,u in lower]
    assert bound==[[3,2,1],[0,2,1],[1,3,2],[2,1,3],[1,3,2],[2,1,0]]
    assert max(map(max,bound))==3
    interior=[]
    for m in [3,4,7,12]:
        S=F(1);U=F(3);e=S/(m+1);tails=[(e,e,e)]*m
        a=rows_of(m,S,U,e,e,e,tails,U/2);ss=slacks(m,S,U,a)
        negative={k:str(v) for k,v in ss.items() if v<0};assert not negative
        # Only upper-triangular forced zeros and their forced ballot equalities vanish.
        zeros=[k for k,v in ss.items() if v==0]
        forced={f'entry/{i}/{k}' for i in range(1,4) for k in range(i+1,5)}
        forced|={f'ballot/{i}/{k}' for i in range(1,4) for k in range(i,4)}
        assert set(zeros)==forced,(m,zeros,forced)
        interior.append({'m':m,'prior_degree':3*m+3,'rows':[[str(x) for x in r] for r in a],
                         'minimum_nonforced_slack':str(min(v for v in ss.values() if v>0)),
                         'forced_zero_tests':sorted(forced)})
    ballot=[[90,0,0,0],[24,66,0,0],[24,24,42,0],[15,12,15,48],[9,6,11,4],[9,6,11,4],[9,6,11,4]]
    bad_ballot={k:str(v) for k,v in slacks(3,30,30,ballot).items() if v<0}
    assert bad_ballot=={'ballot/4/3':'-6'}
    cap=[[F(3),0,0,0],[F(1,2),F(5,2),0,0],[F(1,2),0,F(5,2),0],
         [1,F(1,2),0,F(3,2)],[1,1,F(1,2),F(-3,2)],[0,0,0,1],[0,0,0,1]]
    bad_cap={k:str(v) for k,v in slacks(3,F(1),F(1),cap).items() if v<0}
    assert bad_cap=={'entry/5/4':'-3/2'}
    permutations3=list(permutations(range(3)));orbit_cases=0;pointwise_failure=None
    for S in [0,1,2]:
        for v in compositions(3*S,6):
            L,h=LH(S,v);x,y,z,B,C,D=v
            assert L==max(y+C-S,0)+max(0,S-C-x,y+D-S)
            assert h==y-x+min(0,S-B-y,x+D-S)
            assert 0<=L-h<=3*S
            loss=moment=0
            for perm in permutations3:
                for perm2 in permutations3:
                    w=tuple(v[i] for i in perm)+tuple(v[3+i] for i in perm2)
                    a,b=LH(S,w);loss+=a-b;moment+=max(w[0]+w[3]-S,0)
            assert loss==4*moment
            orbit_cases+=1
            if v==(0,0,0,1,2,0) and S==1:
                pointwise_failure={'S':S,'totals':v,'L_minus_h':L-h,'four_positive_part':4*max(x+B-S,0)}
    assert pointwise_failure and pointwise_failure['L_minus_h']!=pointwise_failure['four_positive_part']
    axes=[]
    for m in [3,4,12]:
        for U in [0,1,3]:
            for p in range(U+1):
                a=rows_of(m,0,U,0,0,0,[(0,0,0)]*m,p)
                assert min(slacks(m,0,U,a).values())>=0
            axes.append({'m':m,'S':0,'U':U,'interval':[0,U]})
    out={'schema':'a82-root-geometry-checks/v1','status':'PASS','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'all_18_exact_simplex_bounds':bound,'interior_controls':interior,'ballot_deletion':bad_ballot,
         'coupled_capacity_deletion':bad_cap,'complete_symmetry_orbits':orbit_cases,'group_elements_per_orbit':36,
         'pointwise_countercontrol':pointwise_failure,'axis_controls':axes,'LR_scalar_requests':0,
         'new_originals_counted':0,'source_code_executed':False,'pid':os.getpid(),'seconds':time.monotonic()-start,
         'scope':'Exact constraint and finite identity controls; unbounded proof is in FOUR-LETTER-HEIGHT-v1.md, not extrapolated from controls.'}
    (R/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k in ['status','seconds','complete_symmetry_orbits','LR_scalar_requests']}))
if __name__=='__main__':main()
