"""Certificate-only original-row verifier for the new rank-seven p=3 parent.

No LP, returned program, or producer method is imported.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys

DATA=Path(__file__).resolve().parents[2]/"data/a57"
SOURCE=DATA/"p3-common-v1.json"
OUT=(Path(sys.argv[1]) if len(sys.argv)>1 else Path("a57-p3-parent-replay"))/"p3-common-verify-v1.json"
N=7


def insist(test,message):
    if not test:
        raise AssertionError(message)


def geometry():
    pts=[(i,j) for i in range(N+1) for j in range(N+1-i)]
    interior=[p for p in pts if p[0]>=1 and p[1]>=1 and sum(p)<=N-1]
    ids={p:i for i,p in enumerate(pts)}
    intids={p:i for i,p in enumerate(interior)}
    forms={}
    for i in range(N+1):
        for j in range(N+1-i):
            if i+j<=N-2:
                forms[("A",i,j)]={(i,j):-1,(i+1,j):1,(i,j+1):1,(i+1,j+1):-1}
            if i>=1 and i+j<=N-1:
                forms[("B",i,j)]={(i,j):-1,(i,j+1):1,(i-1,j+1):1,(i-1,j+2):-1}
            if i>=2:
                forms[("C",i,j)]={(i,j):-1,(i-1,j+1):1,(i-1,j):1,(i-2,j+1):-1}
    insist(len(forms)==63 and len(pts)==36 and len(interior)==15,"rank-seven geometry")
    rows={}
    normals={}
    for lab,f in forms.items():
        insist(all(p in ids for p in f),"invalid physical row")
        rows[lab]=[(ids[p],a) for p,a in f.items()]
        v=[0]*len(interior)
        for p,a in f.items():
            if p in intids:
                v[intids[p]]+=a
        normals[lab]=v
    return pts,interior,sorted(forms),rows,normals


def rank(rows):
    a=[[Fraction(z) for z in r] for r in rows]
    if not a:
        return 0
    pos=0
    for col in range(len(a[0])):
        pivot=next((k for k in range(pos,len(a)) if a[k][col]),None)
        if pivot is None:
            continue
        a[pos],a[pivot]=a[pivot],a[pos]
        q=a[pos][col]
        a[pos]=[x/q for x in a[pos]]
        for k in range(pos+1,len(a)):
            if a[k][col]:
                q=a[k][col]
                a[k]=[x-q*y for x,y in zip(a[k],a[pos])]
        pos+=1
        if pos==len(a):
            break
    return pos


def roster():
    pset=(("A",0,0),("C",2,0))
    sset=(("A",0,3),("B",1,3))
    minus=("A",0,1);plus=("B",1,1);u=("A",0,2)
    v=("A",1,1);w=("B",2,1)
    rays=(v,w,("C",2,4),("C",3,4))
    cells=set()
    for p in pset:
        for s in sset:
            for sign in (minus,plus):
                for triple in combinations(rays,3):
                    if sign==minus and v in triple and w in triple:
                        t=next(x for x in triple if x not in (v,w))
                        for chosen in ((minus,u,v,t),(minus,u,w,t),(u,v,w,t)):
                            cells.add(tuple(sorted((p,s)+chosen)))
                    else:
                        cells.add(tuple(sorted((p,s,sign)+triple)))
    insist(len(cells)==48,"candidate roster count")
    return cells


def boundary(height,pts):
    h={p:height[i] for i,p in enumerate(pts)}
    lam=[h[0,j]-h[0,j-1] for j in range(1,N+1)]
    mu=[h[i,0]-h[i-1,0] for i in range(1,N+1)]
    nu=[h[N-i,i]-h[N-i+1,i-1] for i in range(1,N+1)]
    insist(all(min(a)>0 and all(a[i]>a[i+1] for i in range(N-1)) for a in (lam,mu,nu)),"illegal partition")
    insist(sum(lam)==sum(mu)+sum(nu),"trace")
    return {"lambda":lam,"mu":mu,"nu":nu,"trace":sum(lam)}


def check():
    d=json.loads(SOURCE.read_text())
    insist(d["status"]=="EXACT_SHARED_PARENT","source status")
    insist(d["variables"]==755 and d["original_inequalities"]==2799 and d["seed_equalities"]==288,"domain counts")
    pts,inside,labs,rows,normals=geometry()
    possible=roster()
    parent=d["parent_height"]
    insist(len(parent)==len(pts) and all(type(x) is int for x in parent) and parent[0]==0,"parent height")
    common=boundary(parent,pts)
    insist(common==d["boundary"],"boundary data")
    parent_slacks={r:sum(parent[i]*c for i,c in rows[r]) for r in labs}
    insist(min(parent_slacks.values())==d["parent_minimum_original_slack"]>=1,"strict parent")
    seen=set()
    zero_hist=Counter()
    min_strict=None
    inspan_offseed_zero=0
    for cell in d["faces"]:
        seed=tuple(map(tuple,cell["seed"]))
        insist(seed in possible and seed not in seen,"missing or duplicate support")
        seen.add(seed)
        height=cell["height"]
        insist(len(height)==len(pts) and all(type(x) is int for x in height) and height[0]==0,"face height")
        insist(boundary(height,pts)==common,"shared original boundary")
        matrix=[normals[r] for r in seed]
        insist(rank(matrix)==6,"six-normal rank")
        slacks={r:sum(height[i]*c for i,c in rows[r]) for r in labs}
        insist(all(z>=0 for z in slacks.values()),("original inequality",seed))
        insist(all(slacks[r]==0 for r in seed),("selected zero",seed))
        strict=[r for r in labs if rank(matrix+[normals[r]])==7]
        insist(len(strict)>0,"strict row set")
        ownmin=min(slacks[r] for r in strict)
        insist(ownmin==cell["minimum_strict_original_slack"]>=1,("offspan strict",seed))
        min_strict=ownmin if min_strict is None else min(min_strict,ownmin)
        extra=[r for r in labs if r not in seed and r not in strict and slacks[r]==0]
        inspan_offseed_zero+=len(extra)
        zero_hist[sum(z==0 for z in slacks.values())]+=1
    insist(seen==possible,"roster coverage")
    result={"schema":"A57-P3-RANK7-CERTIFICATE-ONLY-VERIFICATION-V1",
            "source_sha256":sha256(SOURCE.read_bytes()).hexdigest(),
            "status":"PASS","shared_boundary":common,
            "checked_original_rows":63*49,"seed_equalities":48*6,
            "faces":48,"parent_minimum_slack":min(parent_slacks.values()),
            "minimum_offspan_face_slack":min_strict,
            "inspan_offseed_zeros":inspan_offseed_zero,
            "zero_counts":dict(zero_hist)}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.open("x").write(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result))


if __name__=="__main__":
    check()
