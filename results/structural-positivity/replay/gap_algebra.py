"""Finite algebra adapted from the accepted root gap-three checker.

No counts are regenerated here. All-parameter count identities remain the
analytic proof dependencies listed in DEPENDENCIES.md.
"""
import hashlib
import json
from math import comb
from exact import Q, need, trim, plus, scale, minus, times, shift, evaluate, lagrange, newton, binomial_polynomial

PARENTS = {"P00": (0, 0), "P10": (1, 0), "P20": (2, 0), "P11": (1, 1)}
PROOFS = ("001-COMPLETE-GAP3-CLUSTERS.md", "004-UNBOUNDED-RANK6-POSITIVITY.md", "005-COMPLETE-QUADRANT-AND-DUALITY.md", "006-QUOTIENT-MOMENTS-AND-POSITIVE-CERTIFICATE.md", "007-HOMOGENEOUS-CONE-AND-BOUNDARIES.md")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def moment_polynomial(slope,offset):
    return plus(plus(times(binomial_polynomial(1,1,2),binomial_polynomial(slope-1,offset+6,7)),
                     scale(shift(binomial_polynomial(slope-1,offset+7,8)),2)),
                scale(binomial_polynomial(slope-1,offset+8,9),3))

def closed_quotients():
    r=minus(binomial_polynomial(3,8,8),binomial_polynomial(2,7,8))
    q=minus(times([1,2],r),scale(minus(moment_polynomial(3,0),moment_polynomial(2,-1)),3))
    return q,r

def finite_binomial(n,k):return comb(n,k) if n>=k>=0 else 0

def moment_sum(S,t):
    return sum((r-t)*finite_binomial(r+2,2)*finite_binomial(S-r+5,5) for r in range(t+1,S+1))

def moment_closed(S,t):
    return (finite_binomial(t+1,2)*finite_binomial(S-t+6,7)
            +2*t*finite_binomial(S-t+7,8)+3*finite_binomial(S-t+8,9))

def mv(p,x=0,y=0):return {(i,x,y):Q(c) for i,c in enumerate(p) if c}

def mv_add(*polys):
    out={}
    for p in polys:
        for e,c in p.items():out[e]=out.get(e,Q(0))+c
    return {e:c for e,c in out.items() if c}

def mv_scale(p,c):return {e:v*c for e,v in p.items() if v*c}

def mv_mul(a,b):
    out={}
    for e,x in a.items():
        for f,y in b.items():
            g=tuple(i+j for i,j in zip(e,f));out[g]=out.get(g,Q(0))+x*y
    return {e:c for e,c in out.items() if c}

def mv_translate(p,axis,offset):
    out={}
    for e,c in p.items():
        for k in range(e[axis]+1):
            f=list(e);f[axis]=k;f=tuple(f)
            out[f]=out.get(f,Q(0))+c*comb(e[axis],k)*offset**(e[axis]-k)
    return {e:c for e,c in out.items() if c}

def mv_at(p,axis,value):
    out={}
    for e,c in p.items():
        f=list(e);f[axis]=0;f=tuple(f)
        out[f]=out.get(f,Q(0))+c*value**e[axis]
    return {e:c for e,c in out.items() if c}

def mv_delta(p,axis):return mv_add(mv_translate(p,axis,1),mv_scale(p,-1))

def serialize_mv(p):
    return [{"exponents":list(e),"coefficient":str(c)} for e,c in sorted(p.items())]

def reconstruct(counts):
    xs=[-2,-1,0,*range(1,9)];polys={}
    for parent in PARENTS:
        ys=[0,0,1,*[counts[f"{parent}:t{t}"] for t in range(1,9)]]
        p=lagrange(xs,ys)
        need(p==newton(xs,ys),"Independent interpolation arithmetic disagrees")
        need(len(p)<=11 and p[0]==1 and evaluate(p,-1)==evaluate(p,-2)==0,"Interpolation did not preserve its supplied parent-space constraints")
        polys[parent]=p
    difference=minus(polys["P20"],polys["P10"])
    need(difference[0]==0,"P20-P10 is not divisible by t")
    polys["Q0"]=trim(difference[1:])  # computed constant; never supplied as data
    need(len(polys["Q0"])<=10,"Derived quotient exceeds its degree upper bound")
    polys["W0"]=plus(minus(polys["P00"],polys["P10"]),shift(polys["Q0"]))
    polys["Q1_closed"],polys["R_closed"]=closed_quotients()
    return polys

def negative_observations(polys):
    return [{"object":name,"degree":i,"coefficient":str(c),
             "scope":"entire source-bound LR parent under the explicit GT/count-identity premises" if name in PARENTS else "auxiliary object, not an LR counterexample"}
            for name,p in polys.items() for i,c in enumerate(p) if c<0]

def algebra(polys,arrays):
    p0,p1,p2,p11,q0=(polys[key] for key in ("P00","P10","P20","P11","Q0"))
    first,second=arrays[PROOFS[1]],arrays[PROOFS[3]]
    factor=times([1,1],[2,1])
    expected0=scale(times(factor,first["A0"]),Q(1,40320))
    expected1=scale(times(factor,first["A1"]),Q(1,40320))
    expected_q0=scale(times(times(factor,[1,1]),first["B"]),Q(1,6720))
    expected11=scale(times(factor,second["A"]),Q(1,40320))
    need(p0==expected0 and p1==expected1 and p11==expected11,"Returned complete-parent factor array differs from fresh reconstruction")
    need(q0==expected_q0 and p2==plus(p1,shift(q0)),"Returned Q0 factor or complete P20 relation differs")
    q1,r=closed_quotients()
    need(q1==scale(times(factor,second["B"]),Q(1,40320)),"Closed hinge Q1 differs from its complete positive B array")
    need(r==scale(times(factor,second["C"]),Q(1,40320)),"Closed capped R differs from its complete positive C array")
    controls=[]
    for t in range(13):
        for S in range(13):
            direct=moment_sum(S,t);closed=moment_closed(S,t)
            need(direct==closed,"Complete hinge finite-sum control failed")
            controls.append([S,t,direct])
        for a,b in ((3,0),(2,-1)):
            need(evaluate(moment_polynomial(a,b),t)==moment_sum(a*t+b,t),"Generalized binomial formula mishandles initial absent correction")
    need(len(p11)==11 and len(q1)==10 and len(r)==9 and all(c>0 for p in (p0,p1,q0,p11,q1,r) for c in p),
         "A required entire/factor polynomial is not strictly coefficientwise positive")
    need(q1[0]==r[0]==1 and evaluate(q1,-1)==evaluate(q1,-2)==0,"Closed quotient initial/negative-root identity failed")
    # Polynomial identities in all t,x,y. Source all-parameter COUNT theorems
    # remain analytic premises; this is an exact, complete algebraic check.
    tQ1,tQ0,t2R=mv(shift(q1)),mv(shift(q0)),mv(shift(r,2))
    x={(0,1,0):Q(1)};y={(0,0,1):Q(1)};one={(0,0,0):Q(1)}
    xm=mv_add(x,mv_scale(one,-1));ym=mv_add(y,mv_scale(one,-1))
    interior=mv_add(mv(p11),mv_mul(mv_add(x,y,mv_scale(one,-2)),tQ1),mv_mul(mv_mul(xm,ym),t2R))
    axis_x=mv_add(mv(p1),mv_mul(xm,tQ0))
    axis_y=mv_add(mv(p1),mv_mul(ym,tQ0))
    need({(e[0],e[2],e[1]):c for e,c in interior.items()}==interior,"Entire interior polynomial is not duality symmetric")
    need({(e[0],e[2],e[1]):c for e,c in axis_x.items()}==axis_y,"Whole quadrant axes do not match under duality")
    need(mv_at(axis_x,1,1)==mv(p1) and mv_at(axis_x,1,2)==mv(p2)
         and mv_at(mv_at(interior,1,1),2,1)==mv(p11),"Base specializations of whole quadrant are wrong")
    need(mv_delta(mv_delta(interior,1),2)==t2R,"Interior complete mixed difference differs from t^2 R")
    first_boundary=mv_add(mv_at(interior,2,1),mv_scale(axis_x,-1))
    need(mv_delta(first_boundary,1)==mv(minus(shift(q1),shift(q0))),"Axis/interior mixed difference differs from t(Q1-Q0)")
    corner=plus(minus(p11,scale(p1,2)),p0)
    need(mv_add(mv_at(mv_at(interior,1,1),2,1),mv_scale(mv(p1),-2),mv(p0))==mv(corner),"Corner mixed difference incomplete")
    need(mv_delta(axis_x,1)==tQ0 and mv_delta(interior,1)==mv_add(tQ1,mv_mul(ym,t2R)),"Whole first differences omit an axis/mixed term")
    delta_q=minus(q1,q0)
    initial_difference=minus(p1,p0)
    need(all(c>=0 for p in (delta_q,corner,initial_difference,minus(p11,p1)) for c in p),"Claimed quadrant monotonicity/mixed sign failed")
    homogeneous={}
    for k,c in enumerate(p11):homogeneous[k,0,0]=c
    for k,c in enumerate(q1):homogeneous[k,1,0]=c;homogeneous[k,0,1]=c
    for k,c in enumerate(r):homogeneous[k,1,1]=c
    need(len(homogeneous)==40 and all(c>0 for c in homogeneous.values()),"Main homogeneous-cone forty coefficient supports are incomplete/nonpositive")
    normalized={}
    for (s,a,b),c in homogeneous.items():
        term=mv([Q(0)]*(s+a+b)+[c])
        if a:term=mv_mul(term,xm)
        if b:term=mv_mul(term,ym)
        normalized=mv_add(normalized,term)
    need(normalized==interior,"The full homogeneous-cone normalization differs from the whole quadrant law")
    # H(st,at,bt) has t exponent equal to the total parameter degree.
    graded=[{"parameters":[s,a,b],"stretch_degree":s+a+b,"coefficient":str(c)}
            for (s,a,b),c in sorted(homogeneous.items())]
    boundary={(a,b):c for (s,a,b),c in homogeneous.items() if s==0}
    need(boundary=={(0,0):Q(1),(1,0):Q(1),(0,1):Q(1),(1,1):Q(1)},"s=0 boundary is not the whole rectangle/segment/point product")
    # The separately stated homogeneous edge P10(st)+bt Q0(st) uses the
    # independently DERIVED Q0 constant; no strict degree-ten fit at s=0.
    need(p1[0]==q0[0]==1,"Homogeneous edge boundary is not bt+1")
    # Under the same reviewed strict-GT theorem, every staircase ratio is
    # <=3/s: check 3*denominator - numerator*s coefficientwise in s,a,b.
    costs=[((3,0,1),5),((2,1,0),2),((2,1,0),2),((1,0,0),2),
           ((2,0,1),2),((2,0,1),2),((3,1,0),5),((4,1,0),8),((3,0,0),9),((4,0,1),8)]
    inequalities=[(3*v[0]-c,3*v[1],3*v[2]) for v,c in costs]
    need(all(all(x>=0 for x in row) for row in inequalities) and inequalities[-2]==(0,0,0),
         "Homogeneous strict-GT codegree bound dropped a staircase constraint")
    # Keep the known negative auxiliary correction, never an LR candidate.
    w0=plus(minus(p0,p1),shift(q0))
    return {"closed_Q1":list(map(str,q1)),"closed_R":list(map(str,r)),"Q0_constant_derived":str(q0[0]),
        "factor_arrays":arrays,"hinge_controls":{"complete_pairs":len(controls),"digest":digest(encoded(controls)),
            "generalized_binomial_initial_branches_checked":True},
        "quadrant":{"interior":serialize_mv(interior),"x_axis":serialize_mv(axis_x),"y_axis":serialize_mv(axis_y),
            "corner":list(map(str,p0)),"interior_mixed_difference":list(map(str,shift(r,2))),
            "axis_mixed_difference":list(map(str,shift(delta_q))),"corner_mixed_difference":list(map(str,corner)),
            "complete_first_difference_identities":True,"coefficientwise_monotonicity_and_mixed_signs":True},
        "homogeneous_main_40":graded,"homogeneous_s0":"(1+at)(1+bt), with actual degree 2/1/0 as positive parameters drop",
        "homogeneous_edge_s0":"1+bt; derived Q0(0) checked",
        "homogeneous_s_positive_codegree":{"conditional_value":"ceil(3/s)","all_staircase_comparisons":inequalities,
            "dimension":10,"theorem_scope":"strict s>0 only; s=0 uses the explicit boundary product"},
        "negative_auxiliary_W0":{"coefficients":list(map(str,w0)),"negative_coefficients":negative_observations({"W0":w0}),
            "scope":"P00-P10+tQ0; auxiliary complete correction, never a whole LR counterexample"},
        "all_parameter_count_identity_acceptance":"separately reviewed analytic proofs; finite algebra alone does not prove their applicability"}
