"""Independent exact finite check of Pro045 U11's original-row component.

Returned programs are inert. This checker uses only the two specified JSON data
files and literal formulas from the proof; it never imports returned code.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import gcd
from pathlib import Path
import json
import sys

T = Path(__file__).resolve().parents[4]
DATA = Path(__file__).resolve().parents[2] / "data/a57"
HEIGHT = DATA / "U11-COLLAR-FAMILY.json"
GEOM = DATA / "U11-GEOMETRY-FAMILY.json"
PAIR = DATA / "U11-SIMPLEX-PAIR-VALUES.json"
OUT = Path(sys.argv[1]) if len(sys.argv)>1 else Path("a57-u11-replay")
P = (("A", 0, 0), ("C", 2, 0))
S_PAIR = (("A", 0, 3), ("B", 1, 3))
NEG_A, A, U, V, W = ("A", 0, 1), ("B", 1, 1), ("A", 0, 2), ("A", 1, 1), ("B", 2, 1)


def require(c, message):
    if not c:
        raise AssertionError(message)


def labels(n):
    result = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            if i + j <= n - 2:
                result.append(("A", i, j))
            if i >= 1 and i + j <= n - 1:
                result.append(("B", i, j))
            if i >= 2:
                result.append(("C", i, j))
    return sorted(result)


def points(n):
    return [(i, j) for i in range(n + 1) for j in range(n + 1 - i)]


def interior(n):
    return [(i, j) for i in range(1, n) for j in range(1, n - i)]


def form(label):
    kind, i, j = label
    if kind == "A":
        return {(i,j):-1, (i+1,j):1, (i,j+1):1, (i+1,j+1):-1}
    if kind == "B":
        return {(i,j):-1, (i,j+1):1, (i-1,j+1):1, (i-1,j+2):-1}
    return {(i,j):-1, (i-1,j+1):1, (i-1,j):1, (i-2,j+1):-1}


def rows(n):
    pts, ints, labs = points(n), interior(n), labels(n)
    ip = {p:i for i,p in enumerate(ints)}
    full = {p:i for i,p in enumerate(pts)}
    normals = {}
    fullrows = {}
    for lab in labs:
        f = form(lab)
        require(all(p in full for p in f), ("invalid physical row",n,lab))
        fullrows[lab] = tuple((full[p],c) for p,c in f.items())
        v = [0]*len(ints)
        for p,c in f.items():
            if p in ip:
                v[ip[p]] += c
        normals[lab] = tuple(v)
    return pts, ints, labs, fullrows, normals


def support(n):
    circuit = [V,W] + [("C",i,4) for i in range(2,n-3)]
    result = set()
    for p in P:
        for s in S_PAIR:
            for sign in (NEG_A,A):
                for r,t in combinations(circuit,2):
                    old = (p,s,sign,r,t)
                    if sign == NEG_A and (r,t) == (V,W):
                        for triple in ((NEG_A,U,V),(NEG_A,U,W),(U,V,W)):
                            result.add(tuple(sorted((p,s)+triple)))
                    else:
                        result.add(tuple(sorted(old)))
    return result, circuit


def det(a):
    b = [list(row) for row in a]
    size = len(b)
    if size == 0:
        return 1
    sign, last = 1, 1
    for k in range(size-1):
        if b[k][k] == 0:
            swap = next((r for r in range(k+1,size) if b[r][k]), None)
            if swap is None:
                return 0
            b[k],b[swap] = b[swap],b[k]
            sign = -sign
        pivot = b[k][k]
        for i in range(k+1,size):
            for j in range(k+1,size):
                num = b[i][j]*pivot-b[i][k]*b[k][j]
                require(num % last == 0, "Bareiss exact division")
                b[i][j] = num//last
            b[i][k] = 0
        last = pivot
    return sign*b[-1][-1]


def unit_pivot(mat):
    candidates = [j for j in range(len(mat[0])) if any(row[j] for row in mat)]
    for cols in combinations(candidates,len(mat)):
        if abs(det([[row[j] for j in cols] for row in mat])) == 1:
            return tuple(cols)
    raise AssertionError(("no unit column minor",len(mat),len(candidates)))


def inverse(mat):
    d = len(mat)
    a = [[Q(v) for v in row]+[Q(int(i==j)) for j in range(d)] for i,row in enumerate(mat)]
    for j in range(d):
        q = next((i for i in range(j,d) if a[i][j]),None)
        require(q is not None,"singular pivot")
        a[j],a[q] = a[q],a[j]
        p=a[j][j]
        a[j]=[x/p for x in a[j]]
        for i in range(d):
            if i != j:
                p=a[i][j]
                if p:
                    a[i]=[x-p*y for x,y in zip(a[i],a[j])]
    result = [r[d:] for r in a]
    require(all(x.denominator==1 for r in result for x in r),"nonintegral inverse")
    return [[int(x) for x in r] for r in result]


def split(mat,cols):
    d,m=len(mat),len(mat[0])
    cols=tuple(cols)
    require(abs(det([[r[j] for j in cols] for r in mat]))==1,"source pivot not unit")
    inv=inverse([[r[j] for j in cols] for r in mat])
    free=[j for j in range(m) if j not in cols]
    Y=[[0]*d for _ in range(m)]
    K=[[0]*len(free) for _ in range(m)]
    for i,j in enumerate(cols):
        Y[j]=list(inv[i])
        for f,col in enumerate(free):
            K[j][f]=-sum(inv[i][z]*mat[z][col] for z in range(d))
    for f,j in enumerate(free):
        K[j][f]=1
    require(all(sum(mat[i][q]*Y[q][j] for q in range(m))==int(i==j) for i in range(d) for j in range(d)),"right inverse")
    require(all(sum(mat[i][q]*K[q][j] for q in range(m))==0 for i in range(d) for j in range(len(free))),"kernel")
    gram=[[sum(K[q][i]*K[q][j] for q in range(m)) for j in range(len(free))] for i in range(len(free))]
    return free,Y,K,gram


def boundary(h,n,pt):
    val=lambda p:h[pt[p]]
    lam=[val((0,j))-val((0,j-1)) for j in range(1,n+1)]
    mu=[val((i,0))-val((i-1,0)) for i in range(1,n+1)]
    nu=[val((n-i,i))-val((n-i+1,i-1)) for i in range(1,n+1)]
    require(all(v[-1]>=1 and all(v[j]>v[j+1] for j in range(n-1)) for v in (lam,mu,nu)),"non-strict legal boundary")
    require(sum(lam)==sum(mu)+sum(nu),"trace mismatch")
    return dict(**{"lambda":lam,"mu":mu,"nu":nu,"trace":sum(lam)})


def slack(h,f):
    return sum(h[j]*c for j,c in f)


def extra(seed):
    x=set(seed)
    if {U,V,W} <= x:
        return {A}
    if {A,V,W} <= x:
        return {U}
    return set()


def balance(cells,normals,m,need_rank=True):
    around=defaultdict(list)
    ordered=sorted(cells)
    for index,cell in enumerate(ordered):
        for missing in cell:
            face=tuple(x for x in cell if x != missing)
            around[face].append((index,missing))
    eq=[]
    nonzero=0
    for face,inc in around.items():
        mat=[normals[x] for x in face]
        piv=unit_pivot(mat)
        free,Y,K,G=split(mat,piv)
        images=[]
        for index,missing in inc:
            vector=tuple(sum(normals[missing][z]*K[z][j] for z in range(m)) for j in range(m-4))
            require(gcd(*vector)==1,("nonprimitive cofacet",face,missing))
            images.append((index,vector))
        for j in range(m-4):
            row={index:vector[j] for index,vector in images if vector[j]}
            if row:
                eq.append(row)
                nonzero += 1
    residual=max((abs(sum(row.values())) for row in eq),default=0)
    result=dict(cofacets=len(around),equations=nonzero,unit_residual_max=residual)
    if need_rank:
        echelon={}
        for row in eq:
            r={j:Q(v) for j,v in row.items()}
            while r:
                p=min(r)
                if p not in echelon:
                    f=r[p]
                    echelon[p]={j:v/f for j,v in r.items()}
                    break
                f=r[p]
                for j,v in echelon[p].items():
                    x=r.get(j,Q(0))-f*v
                    if x:
                        r[j]=x
                    else:
                        r.pop(j,None)
        result["rank"]=len(echelon)
    return result


def reconstructed_rays(n):
    k=n-5
    d=k+1
    v=[0]*d;v[1]=1
    w=[0]*d;w[0]=w[1]=-1
    ray=[tuple(v),tuple(w)]
    for i in range(k):
        t=[0]*d
        t[0 if i==0 else i+1]=1
        if i+1<k:
            t[i+2]=-1
        ray.append(tuple(t))
    require(all(sum(r[j] for r in ray)==0 for j in range(d)),"circuit sum")
    return ray


def check_pairs(c):
    n=c["n"];rays=reconstructed_rays(n)
    d=len(rays[0]);diag=[Q(1,2)]+[Q(2)]*(d-1)
    require([list(r) for r in rays]==c["rays"],("rays",n))
    require(c["dimension"]==d and c["k"]==n-5,("pair dimension",n))
    require([Q(x) for x in c["primal_quotient_metric_diagonal"]]==[Q(2)]+[Q(1,2)]*(d-1),"primal metric")
    require([Q(x) for x in c["dual_metric_diagonal"]]==diag,"dual metric")
    expected={}
    for i,j in combinations(range(len(rays)),2):
        r,s=rays[i],rays[j]
        image_gcd=gcd(*(r[a]*s[b]-r[b]*s[a] for a,b in combinations(range(d),2)))
        require(image_gcd==1,("pair nonunit",n,i,j))
        g11=sum(diag[z]*r[z]**2 for z in range(d))
        g12=sum(diag[z]*r[z]*s[z] for z in range(d))
        g22=sum(diag[z]*s[z]**2 for z in range(d))
        alpha=Q(1,4)-Q(1,12)*(g12/g11+g12/g22)
        expected[(i,j)]=(g11,g12,g22,alpha)
    require(len(expected)==len(c["pairs"]),"pair count")
    for pair in c["pairs"]:
        key=tuple(pair["rays"])
        require(key in expected,("extraneous pair",n,key))
        g11,g12,g22,alpha=expected.pop(key)
        require(pair["N"]==[list(rays[key[0]]),list(rays[key[1]])],"pair rows")
        require([[Q(x) for x in row] for row in pair["Gram"]]==[[g11,g12],[g12,g22]],"pair Gram")
        require(Q(pair["alpha"])==alpha,"pair alpha")
        require(all(obj["index"]==1 and obj["points"]==[[0]*len(obj["axes"])] for obj in pair["images"].values()),"subset image index")
    require(not expected,"missing pairs")
    total=sum(Q(pair["alpha"]) for pair in c["pairs"])
    require(total==Q(c["sum"])==Q((n-3)*(3*n-10),24),("pair sum",n))
    wrong=sum(Q(1,4)-Q(1,12)*(
        Q(sum(rays[i][z]*rays[j][z] for z in range(d)),sum(x*x for x in rays[i]))+
        Q(sum(rays[i][z]*rays[j][z] for z in range(d)),sum(x*x for x in rays[j])))
        for i,j in combinations(range(len(rays)),2))
    require(wrong==total,"complete sum should be metric invariant by circuit identity")
    # A single pair exposes an incorrect metric even though the complete sum does not.
    i,j=0,1
    identity_pair=Q(1,4)-Q(1,12)*(Q(-1,1)+Q(-1,2))
    require(identity_pair!=Q(c["pairs"][0]["alpha"]),"wrong-metric control")
    return dict(n=n,pairs=len(c["pairs"]),pairing=str(total),wrong_metric_pair_rejected=True)


def check_extension(old,new,step):
    n=old["n"]
    require(step["n_from"]==n and new["n"]==n+1 and step["scale"]==6,"extension step")
    oldpts=points(n);newpts=points(n+1)
    oldindex={p:i for i,p in enumerate(oldpts)}
    newindex={p:i for i,p in enumerate(newpts)}
    oldrecords={tuple(map(tuple,r["seed"])):r for r in old["records"]}
    current={tuple(map(tuple,r["seed"])):r for r in new["records"]}
    require(len(step["provenance"])==len(current),"provenance count")
    coeff=step["common_affine_legalization"]
    z=step["new_diagonal_before_legalization"]
    shift=step["common_shift"]
    require(len(coeff)==2 and len(z)==n+2,"new diagonal data")
    seen=set()
    def assembled(oldheights,mods):
        arr=[None]*len(newpts)
        for p in oldpts:
            i,j=p
            arr[newindex[p]]=oldheights[oldindex[p]]+mods.get(p,0)+i*coeff[0]+j*coeff[1]
        for i in range(n+2):
            p=(i,n+1-i)
            arr[newindex[p]]=z[i]-shift+i*coeff[0]+(n+1-i)*coeff[1]
        return arr
    for prov in step["provenance"]:
        key=tuple(map(tuple,prov["seed"]))
        require(key in current and key not in seen,"duplicate or foreign provenance")
        seen.add(key)
        sources=[oldrecords[tuple(map(tuple,s))]["height"] for s in prov["old_seeds"]]
        require(len(sources) in (1,2),"provenance arity")
        if len(sources)==1:
            core=[6*x for x in sources[0]]
        else:
            require(prov["kind"]=="new_last_pair","two-source kind")
            core=[3*(a+b) for a,b in zip(*sources)]
        mods={(i,j):v for i,j,v in prov.get("modifications",[])}
        require(assembled(core,mods)==current[key]["height"],("collar reconstruction",n+1,key))
    require(seen==set(current),"provenance coverage")
    require(assembled([6*x for x in old["parent"]],{})==new["parent"],"parent induction")
    return dict(from_rank=n,to_rank=n+1,checked_records=len(seen))


def check_case(h,g):
    n=h["n"];pts,ints,labs,full,norm=rows(n);m=len(ints)
    pidx={p:i for i,p in enumerate(pts)}
    roster,circuit=support(n)
    require(len(labs)==3*n*(n-1)//2,"all physical rows count")
    require(h["points"]==[list(p) for p in pts] and h["interior"]==[list(p) for p in ints],"point system")
    require(n==g["n"] and g["m"]==m and h["whole_dimension"]==m and h["face_dimension"]==m-5,"dimension")
    require(len(roster)==h["cells"]==len(h["records"])==g["cells"].__len__()==4*(n*n-7*n+14),"domain size")
    records={tuple(map(tuple,r["seed"])):r for r in h["records"]}
    geom={tuple(map(tuple,r["seed"])):r for r in g["cells"]}
    require(len(records)==len(geom)==len(roster) and set(records)==set(geom)==roster,"complete seed coverage")
    B=2**m;M=8*B+1;eta=Q(1,48*m*B*B)
    require(g["a"]==[2 if r==U else 1 for r in labs] and g["M"]==M and g["circuit_bound"]==B and Q(g["eta"])==eta,"common perturbation")
    # A common exact denominator is used ONCE per rank for every physical row and cell.
    D=pow(M,len(labs));Qden=48*m*B*B
    deltas={lab:(2 if lab==U else 1)*D+pow(M,len(labs)-index-1) for index,lab in enumerate(labs)}
    parent=h["parent"]
    require(len(parent)==len(pts),"parent length")
    parent_slacks={lab:slack(parent,full[lab]) for lab in labs}
    require(min(parent_slacks.values())==h["parent_minimum_slack"]>0,"strict parent")
    bound=boundary(parent,n,pidx)
    require(bound==h["boundary"],("boundary",n))
    zeros=Counter();slacks=0;shifted=0;geometry=0;min_shift=None;max_cube=0
    for seed,rec in records.items():
        require(seed==tuple(sorted(seed)) and len(seed)==5,"seed canonical")
        height=rec["height"]
        require(len(height)==len(pts) and boundary(height,n,pidx)==bound,"shared legal boundary")
        sv={lab:slack(height,full[lab]) for lab in labs}
        require(min(sv.values())>=0,("negative original row",n,seed))
        truezero={lab for lab,x in sv.items() if x==0}
        require(truezero==set(seed)|extra(seed)==set(map(tuple,rec["zero_labels"])),("exact zero set",n,seed,truezero))
        pos=min(v for v in sv.values() if v>0)
        require(pos==rec["minimum_positive_slack"],"minimum slack")
        zeros[len(truezero)]+=1;slacks+=len(labs)
        mat=[norm[x] for x in seed]
        independent_pivot=unit_pivot(mat)
        require(abs(det([[row[j] for j in independent_pivot] for row in mat]))==1,"independent unit minor")
        srcpivot=tuple(rec["pivots"])
        require(srcpivot==tuple(geom[seed]["pivot"]),"pivot cross-source")
        free,Y,K,Gram=split(mat,srcpivot)
        src=geom[seed]
        require(free==src["free"] and Y==src["right_inverse"] and K==src["kernel"] and Gram==src["Gram"],("geometry mismatch",n,seed))
        require(src["lattice_cube_loss_bound"]==max(sum(abs(sum(norm[lab][q]*K[q][j] for q in range(m))) for j in range(m-5)) for lab in labs),"cube bound")
        max_cube=max(max_cube,src["lattice_cube_loss_bound"])
        geometry+=1
        seed_delta=[deltas[x] for x in seed]
        for lab in labs:
            coeff=[sum(norm[lab][q]*Y[q][j] for q in range(m)) for j in range(5)]
            numer=sv[lab]*Qden*D+deltas[lab]-sum(a*b for a,b in zip(coeff,seed_delta))
            if lab in seed:
                require(numer==0,("selected shifted slack",n,seed,lab))
            else:
                require(numer>0,("off-face shifted slack",n,seed,lab))
                if min_shift is None or numer<min_shift:
                    min_shift=numer
            if lab in extra(seed):
                match=[x for x in src["extra_shift_margins"] if tuple(x["row"])==lab]
                require(len(match)==1 and [int(x) for x in match[0]["coefficients"]]==coeff,"extra coefficients")
                require(Q(match[0]["margin"])==Q(numer,D),"extra exact margin")
            shifted+=1
        require(src["shifted_slack_count"]==len(labs),"shifted count")
    require(zeros==Counter({5:len(roster)-8,6:8})==Counter({int(k):v for k,v in h["zero_size_counts"].items()}),"zero census")
    require(g["max_cube_loss"]==max_cube,"max cube loss")
    bal=balance(roster,norm,m)
    require(bal["unit_residual_max"]==0 and bal["rank"]==len(roster)-1,("balance",n,bal))
    result=dict(n=n,physical_rows=len(labs),interior_dimension=m,cells=len(roster),full_slacks=slacks+len(labs),shifted_slacks=shifted,unit_minors=geometry,gram_matrices=geometry,zero_counts=dict(zeros),boundary=bound,parent_minimum_slack=min(parent_slacks.values()),balance=bal,maximum_cube_loss=max_cube)
    if n==8:
        old,_=support(7)
        obstruction=balance(old,norm,m)
        require(obstruction["rank"]==56 and obstruction["unit_residual_max"]>0,("old roster obstruction",obstruction))
        result["old_56_at_rank_8"]=obstruction
    return result


def controls(hcases,pcases):
    n=8;pts,ints,labs,full,norm=rows(n);roster,_=support(n)
    checks={}
    old,_=support(7)
    checks["wrong_endpoint"]=len(roster-old)>0 and balance(old,norm,len(ints),False)["unit_residual_max"]>0
    missing=set(roster);missing.remove(next(iter(missing)))
    checks["missing_cell"]=balance(missing,norm,len(ints),False)["unit_residual_max"]>0
    bad=norm.copy();bad[V]=tuple(-x for x in bad[V])
    checks["wrong_normal_sign"]=balance(roster,bad,len(ints),False)["unit_residual_max"]>0
    # A wrong metric is visible on an individual pair, although the circuit's total is invariant.
    rays=reconstructed_rays(7)
    g12=sum(rays[0][j]*rays[1][j] for j in range(3))
    wrong=Q(1,4)-Q(1,12)*(Q(g12,sum(x*x for x in rays[0]))+Q(g12,sum(x*x for x in rays[1])))
    checks["identity_metric_pair"]=wrong!=Q(pcases[0]["pairs"][0]["alpha"])
    h=hcases[1];sample=h["records"][0];alter=list(sample["height"])
    lab=next(x for x in labs if x not in set(map(tuple,sample["zero_labels"])))
    site,c=full[lab][0]
    alter[site]-=10**15*c
    checks["violated_full_row"]=slack(alter,full[lab])<0
    checks["altered_seed"]=tuple(sorted(tuple(map(tuple,sample["seed"]))[:-1]+(("A",1,2),))) not in roster
    shifted_parent=list(h["parent"]);shifted_parent[pts.index((0,1))]+=1
    checks["altered_boundary"]=boundary(h["parent"],n,{p:i for i,p in enumerate(pts)})!=boundary(shifted_parent,n,{p:i for i,p in enumerate(pts)})
    require(all(checks.values()),("corruption controls",checks))
    return checks


def main():
    sources={str(p.relative_to(T)):sha256(p.read_bytes()).hexdigest() for p in (HEIGHT,GEOM,PAIR)}
    hs=json.loads(HEIGHT.read_text())["cases"]
    gs=json.loads(GEOM.read_text())["cases"]
    ps=json.loads(PAIR.read_text())["cases"]
    require([x["n"] for x in hs]==[7,8,9,10]==[x["n"] for x in gs]==[x["n"] for x in ps],"rank cases")
    result={"schema":"A57-U11-INDEPENDENT-COMPONENT-CHECK-V1","source_sha256":sources,"cases":[],"extensions":[],"pair_checks":[]}
    for h,g,p in zip(hs,gs,ps):
        result["cases"].append(check_case(h,g))
        result["pair_checks"].append(check_pairs(p))
    for old,new,step in zip(hs,hs[1:],json.loads(HEIGHT.read_text())["extension_steps"]):
        result["extensions"].append(check_extension(old,new,step))
    result["corruption_controls"]=controls(hs,ps)
    result["status"]="PASS"
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/"exact-check-v1.json"
    with path.open("x") as f:
        json.dump(result,f,indent=2);f.write("\n")
    print(json.dumps({"status":result["status"],"cases":[{k:c[k] for k in ("n","cells","balance","full_slacks","shifted_slacks")} for c in result["cases"]],"pair_checks":result["pair_checks"],"extensions":result["extensions"],"corruption_controls":result["corruption_controls"],"result":str(path)},default=str))


if __name__=="__main__":
    main()
