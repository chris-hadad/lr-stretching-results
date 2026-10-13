"""Exact rank-seven six-support balance and one common generic row shift."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import sys

from check_u11 import DATA, U, unit_pivot, split
from check_p3_parent import geometry, roster, rank

SOURCE=DATA/"p3-common-v1.json"
OUT=(Path(sys.argv[1]) if len(sys.argv)>1 else Path("a57-p3-component-replay"))/"p3-component-v1.json"


def insist(cond,message):
    if not cond:
        raise AssertionError(message)


def sparse_rank(equations):
    pivots={}
    for equation in equations:
        row={j:Q(x) for j,x in equation.items() if x}
        while row:
            p=min(row)
            if p not in pivots:
                scale=row[p]
                pivots[p]={j:x/scale for j,x in row.items()}
                break
            scale=row[p]
            for j,x in pivots[p].items():
                z=row.get(j,Q(0))-scale*x
                if z:
                    row[j]=z
                else:
                    row.pop(j,None)
    return len(pivots)


def balance(cells,norm,m):
    around=defaultdict(list)
    for ci,seed in enumerate(cells):
        for missing in seed:
            face=tuple(r for r in seed if r!=missing)
            around[face].append((ci,missing))
    eq=[]
    nonzero=0
    max_unit_residual=0
    primitive_images=0
    unit_cofacets=0
    for face,incidence in around.items():
        mat=[norm[r] for r in face]
        pivot=unit_pivot(mat)
        free,Y,K,G=split(mat,pivot)
        unit_cofacets+=1
        vectors=[]
        for ci,missing in incidence:
            v=tuple(sum(norm[missing][q]*K[q][j] for q in range(m)) for j in range(m-5))
            insist(gcd(*v)==1,("nonprimitive image",face,missing))
            vectors.append((ci,v))
            primitive_images+=1
        for j in range(m-5):
            equation={ci:v[j] for ci,v in vectors if v[j]}
            if equation:
                eq.append(equation)
                nonzero+=1
                max_unit_residual=max(max_unit_residual,abs(sum(equation.values())))
    r=sparse_rank(eq)
    insist(max_unit_residual==0 and r==len(cells)-1,("balance failure",max_unit_residual,r))
    return {"five_cofacets":len(around),"unit_cofacets":unit_cofacets,
            "primitive_incidence_images":primitive_images,
            "nonzero_quotient_equations":nonzero,
            "unit_weight_residual_max":max_unit_residual,"signed_balance_rank":r,
            "signed_kernel_dimension":len(cells)-r}


def shared_shift(cert,cells,pts,ints,labs,rows,norm):
    m=len(ints)
    B=1<<m
    M=8*B+1
    eta_den=48*m*B*B
    denominator=M**len(labs)
    a={r:2 if r==U else 1 for r in labs}
    delta={r:a[r]*denominator+M**(len(labs)-i-1) for i,r in enumerate(labs)}
    insist(all(sum(z*z for z in norm[r])<=4 for r in labs),"Hadamard row norm")
    insist(Q(B,M-1)==Q(1,8),"lexicographic tail bound")
    basis_slack_change_bound=Q(3+12*m*B,eta_den)
    insist(basis_slack_change_bound<Q(1,3*B),"integral-basis compatibility bound")
    source_cells={tuple(map(tuple,f["seed"])):f["height"] for f in cert["faces"]}
    insist(len(source_cells)==len(cells),"source cell coverage")
    count=0
    extra_count=0
    base_extra_min=None
    min_positive=None
    min_extra_numerator=None
    min_all_positive_numerator=None
    max_right_inverse_entry=0
    for seed in cells:
        height=source_cells[seed]
        N=[norm[r] for r in seed]
        pivot=unit_pivot(N)
        free,Y,K,G=split(N,pivot)
        max_right_inverse_entry=max(max_right_inverse_entry,max(abs(x) for row in Y for x in row))
        selected=[delta[r] for r in seed]
        for r in labs:
            slack=sum(height[i]*z for i,z in rows[r])
            coeff=[sum(norm[r][i]*Y[i][j] for i in range(m)) for j in range(6)]
            numerator=slack*eta_den*denominator+delta[r]-sum(c*selected[j] for j,c in enumerate(coeff))
            count+=1
            if r in seed:
                insist(slack==0 and numerator==0,("selected shifted row",seed,r))
                continue
            insist(numerator>0,("offseed shifted row",seed,r,slack))
            min_all_positive_numerator=numerator if min_all_positive_numerator is None else min(min_all_positive_numerator,numerator)
            if slack==0:
                extra_count+=1
                base_margin=a[r]-sum(c*a[seed[j]] for j,c in enumerate(coeff))
                insist(base_margin>0,("base delta extra margin",seed,r,base_margin))
                base_extra_min=base_margin if base_extra_min is None else min(base_extra_min,base_margin)
                min_extra_numerator=numerator if min_extra_numerator is None else min(min_extra_numerator,numerator)
            else:
                min_positive=slack if min_positive is None else min(min_positive,slack)
    parent=cert["parent_height"]
    parent_shifted=sum(1 for r in labs if
        sum(parent[i]*z for i,z in rows[r])*eta_den*denominator+delta[r]>0)
    insist(parent_shifted==len(labs),"shifted strict parent")
    insist(extra_count==16 and base_extra_min==1,"extra zero census")
    return {"row_order":[list(r) for r in labs],
            "base_a":[a[r] for r in labs],"M":M,"eta":str(Q(1,eta_den)),
            "lex_tail_bound":str(Q(B,M-1)),
            "uniform_nonzero_basis_slack_change_bound":str(basis_slack_change_bound),
            "minimum_nonzero_integral_basis_slack":str(Q(1,B)),
            "genericity_argument":"Every primitive circuit has at most m+1 rows and integer coefficients of magnitude at most B by the row-norm-2 Hadamard bound. If c dot a is nonzero, its integer part dominates the total lex tail (<1/8). Otherwise the earliest nonzero lex term dominates all later terms by the same bound.",
            "compatibility_argument":"Every nonzero original integral-boundary basis slack has magnitude at least 1/B. The displayed common eta changes it by less than 1/(3B), so its sign cannot reverse.",
            "shifted_face_rows_checked":count,
            "shifted_parent_rows_checked":parent_shifted,
            "offseed_zero_rows":extra_count,
            "minimum_base_extra_margin":base_extra_min,
            "minimum_original_positive_offseed_slack":min_positive,
            "minimum_extra_shift_margin":str(Q(min_extra_numerator,eta_den*denominator)),
            "minimum_positive_shifted_margin":str(Q(min_all_positive_numerator,eta_den*denominator)),
            "maximum_unit_right_inverse_entry":max_right_inverse_entry}


def main():
    cert=json.loads(SOURCE.read_text())
    insist(cert["status"]=="EXACT_SHARED_PARENT","no exact parent source")
    pts,ints,labs,rows,norm=geometry()
    possible=roster()
    cells=sorted(tuple(map(tuple,f["seed"])) for f in cert["faces"])
    insist(set(cells)==possible and len(cells)==48,"roster mismatch")
    for seed in cells:
        insist(len(seed)==6 and len(set(seed))==6,"six-set")
        unit_pivot([norm[r] for r in seed])
    result={"schema":"A57-P3-RANK7-COMPONENT-GEOMETRY-SHIFT-V1",
            "source_sha256":sha256(SOURCE.read_bytes()).hexdigest(),
            "n":7,"original_dimension":len(ints),"cells":len(cells),
            "normal_span_rank":rank([norm[r] for seed in cells for r in seed]),
            "balance":balance(cells,norm,len(ints)),
            "shared_shift":shared_shift(cert,cells,pts,ints,labs,rows,norm),
            "status":"PASS"}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.open("x").write(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"normal_span_rank":result["normal_span_rank"],
                      "balance":result["balance"],"shifted_face_rows_checked":result["shared_shift"]["shifted_face_rows_checked"],
                      "offseed_zero_rows":result["shared_shift"]["offseed_zero_rows"],
                      "result":str(OUT)}))


if __name__=="__main__":
    main()
