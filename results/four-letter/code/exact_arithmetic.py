"""Independent complete four-letter arithmetic, authored from mathematical definitions.

No returned program is executed or imported. No SOURCE numeric file is read here.
All polynomials are dense, low-to-high exact Fraction vectors. Native/LR oracles
are not called. Output is confined to the explicitly assigned four-letter roots.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, product
from math import comb, factorial, gcd
from pathlib import Path
import json
import time

S = (Q(0), Q(1))
ONE = (Q(1),)
ZERO = (Q(0),)

def trim(a):
    a = list(map(Q, a))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)

def add(*aa):
    out = [Q(0)] * max(map(len, aa), default=1)
    for a in aa:
        for i, c in enumerate(a):
            out[i] += c
    return trim(out)

def scale(a, c):
    return trim([Q(c)*x for x in a])

def sub(a, b):
    return add(a, scale(b, -1))

def mul(*aa):
    out = ONE
    for a in aa:
        v = [Q(0)]*(len(out)+len(a)-1)
        for i, x in enumerate(out):
            for j, y in enumerate(a):
                v[i+j] += x*y
        out = trim(v)
    return out

def powp(a, k):
    return mul(*([a]*k))

def falling(a, k):
    return mul(*(add(a, (-i,)) for i in range(k)))

def rising(a, k):
    return mul(*(add(a, (i,)) for i in range(k)))

def irise(a, k):
    v = 1
    for i in range(k):
        v *= a+i
    return v

@lru_cache(None)
def choose_linear(a, b, k):
    if k < 0:
        return ZERO
    return scale(falling((Q(b), Q(a)), k), Q(1, factorial(k)))

@lru_cache(None)
def a(n, c):
    return mul(*((Q(1), Q(c, i)) for i in range(1, n+1)))

def evalp(p, s):
    v = Q(0)
    for c in reversed(p):
        v = v*s+c
    return v

def divide_exact(p, q):
    rem=list(p);out=[Q(0)]*max(1,len(p)-len(q)+1)
    while len(rem)>=len(q) and any(rem):
        k=len(rem)-len(q);c=rem[-1]/q[-1];out[k]=c
        for i,v in enumerate(q):
            rem[k+i]-=c*v
        rem=list(trim(rem))
    assert not any(rem), 'nonzero exact division remainder'
    return trim(out)

def integer_form(p):
    den=1
    for c in p:
        den=den*c.denominator//gcd(den,c.denominator)
    return dict(common_denominator=str(den),integer_coefficients=[str(c.numerator*(den//c.denominator)) for c in p])

def poly_record(p, through=None):
    p = trim(p)
    if through is None:
        through = len(p)-1
    assert through >= len(p)-1
    dense = list(p)+[Q(0)]*(through+1-len(p))
    return dict(actual_degree=None if p == ZERO else len(p)-1,
                dense_through=through, coefficients=[str(c) for c in dense],
                zero_slots=[i for i,c in enumerate(dense) if c==0],
                negative_slots=[i for i,c in enumerate(dense) if c<0],
                strictly_positive_all_dense_slots=all(c>0 for c in dense))

PBAR = (Q(2),Q(2),Q(1,2))
QBAR = (Q(1411,1320),Q(4457,2520),Q(40049,36960),Q(1009,3465),Q(51,1760))
HBAR = (Q(409,1458),Q(1579,1215),Q(45475,22176),Q(34549,22176),Q(3947,7392),Q(2509,36960))

# Representation A: full one-tail truncated numerator, masks zero through two.
def w_numerator(m):
    alpha = choose_linear(1,3,2)
    beta = mul((1,1),(3,1))
    gamma = choose_linear(1,2,2)
    tail = [scale(alpha,-1),beta,scale(gamma,-1)]
    powers = [[ONE]]
    for j in range(1,3):
        old = powers[-1]
        nxt = [ZERO]*(len(old)+2)
        for k,c in enumerate(old):
            for h,d in enumerate(tail):
                nxt[k+h] = add(nxt[k+h],mul(c,d))
        powers.append(nxt)
    masks=[]
    for j in range(3):
        masks.append(scale(add(*(mul(c,choose_linear(3-j,3*m+2-j-k,3*m+2))
                                 for k,c in enumerate(powers[j]))),comb(m,j)))
    return add(*masks), masks

# Representation B: original complete violation p/q factorization.
def p_polynomial(m):
    r=3*m+1
    return scale(add(choose_linear(1,3,2),
                     scale(mul((3,1),(-1,2)),Q(1,r)),
                     scale(mul((-1,2),(-2,2)),Q(1,r*(r+1)))),Q(2,3))

def d_coefficients():
    base=[choose_linear(1,3,2),(3,1),ONE]
    out=[ZERO]*5
    for i,c in enumerate(base):
        for j,d in enumerate(base):
            out[i+j]=add(out[i+j],mul(c,d))
    return out

def q_polynomial(m):
    return scale(add(*(scale(mul(c,falling((-2,1),h)),Q(1,irise(3*m-1,h)))
                       for h,c in enumerate(d_coefficients()))),Q(m,6*(3*m-2)))

def w_violation(m):
    M,A,B=a(3*m+2,3),a(3*m-1,2),a(3*m-4,1)
    single=mul(S,p_polynomial(m),A)
    double=mul(S,(-1,1),q_polynomial(m),B)
    return add(M,scale(single,-1),double),(M,single,double)

# Representation A moment: all three complete double-Vandermonde cap sums.
def j_vandermonde(m,j):
    out=ZERO
    for h in range(j+1):
        for v in range(j-h+1):
            inner=ZERO
            n=2*m+1-h-v
            for i in range(n+1):
                inner=add(inner,scale(mul(choose_linear(2-j,2*m+2-j-v,n-i),
                                         choose_linear(1,m+1,m+h+2+i)),
                                    comb(j+h+1+i,i)))
            out=add(out,scale(mul(powp((1,1),v),inner),
                              (-1)**h*comb(j,h)*comb(j-h,v)))
    return out

# Representation B moments: uncapped telescoper, positive one-cap, fixed finite r.
def j0_telescoper(m):
    return scale(mul(S,a(m+1,1),a(2*m+1,2)),Q(2,3))

def one_cap_QR(m):
    D1=9*(m+1)*(2*m+1)*(3*m+1)*(3*m+2)
    qp=scale((51*m**3+96*m**2+58*m+11,
              26*m**3+83*m**2+71*m+18,
              4*m**3+10*m**2+15*m+7),Q(2,D1))
    rp=scale((12*m**2+6*m,
              46*m**2+41*m+6,
              21*m**2+51*m+18,
              2*m**2+10*m+12),Q(2,9*(3*m+1)*(3*m+2)))
    return qp,rp

def positive_V(m):
    return add(*(mul(choose_linear(1,3*m-k-1,3*m-k),choose_linear(1,k-1,k))
                 for k in range(2*m+1)))

def j1_positive(m):
    qp,rp=one_cap_QR(m)
    return add(mul(S,S,a(m-1,1),a(2*m,1),qp),mul(rp,positive_V(m)))

def r_polynomial(m):
    out=ZERO
    for h in range(3):
        for v in range(3-h):
            inner=ZERO
            for i in range(4+h):
                ci=comb(4,3+h-i) if 0<=3+h-i<=4 else 0
                if not ci:
                    continue
                den=irise(3*m-3,4-h-v+i)
                inner=add(inner,scale(mul(falling((-2,1),i),rising((3*m-3,1),2-h-v)),
                                      Q(ci*comb(2*m+1-h-v+i,i),den)))
            out=add(out,scale(mul(powp((1,1),v),inner),
                              (-1)**h*comb(2,h)*comb(2-h,v)))
    return scale(out,comb(m,2))

def j2_finite(m):
    return scale(mul(S,(-1,1),a(3*m-4,1),r_polynomial(m)),Q(1,comb(m,2)))

def complete(m):
    wa,masks=w_numerator(m)
    wb,caps=w_violation(m)
    ja=[j_vandermonde(m,j) for j in range(3)]
    jb=[j0_telescoper(m),j1_positive(m),j2_finite(m)]
    assert wa==wb, ('full W mismatch',m)
    for j in range(3):
        assert ja[j]==jb[j], ('full J cap mismatch',m,j)
    moment=add(ja[0],scale(ja[1],-m),scale(ja[2],comb(m,2)))
    fa=sub(mul((1,3),wa),scale(moment,4))
    M,A,B=a(3*m+2,3),a(3*m-1,2),a(3*m-4,1)
    P=mul(a(m+1,1),a(2*m+1,2))
    pm,qm,rm=p_polynomial(m),q_polynomial(m),r_polynomial(m)
    hm=sub(mul((1,3),qm),scale(rm,4))
    fb=add(mul((1,3),M),scale(mul(S,P),Q(-8,3)),
           scale(mul(S,(1,3),pm,A),-1),scale(jb[1],4*m),mul(S,(-1,1),B,hm))
    assert fa==fb, ('full F mismatch',m)
    G=add(mul((1,Q(1,3)),M),scale(mul(S,(1,3),PBAR,A),-1),scale(mul(S,HBAR,B),-1))
    terms=[scale(mul(S,sub(M,P)),Q(8,3)),mul(S,(1,3),sub(PBAR,pm),A),
           scale(jb[1],4*m),mul(S,S,B,hm),mul(S,B,sub(HBAR,hm))]
    assert sub(fa,G)==add(*terms),('same-coefficient compensation mismatch',m)
    assert all(all(c>=0 for c in p) for p in terms),('compensation sign failure',m)
    assert len(wa)-1==3*m+2 and all(c>0 for c in wa)
    assert len(fa)-1==3*m+3 and all(c>0 for c in fa),('complete original negative',m)
    return dict(m=m,W=poly_record(wa,3*m+3),W_masks=[poly_record(p,3*m+3) for p in masks],
                W_unsigned_violations=[poly_record(p,3*m+3) for p in caps],
                J_caps=[poly_record(p,3*m+3) for p in ja],J=poly_record(moment,3*m+3),
                F=poly_record(fa,3*m+3),G=poly_record(G,3*m+3),
                F_minus_G=poly_record(sub(fa,G),3*m+3),
                compensation_terms=[poly_record(p,3*m+3) for p in terms],
                p=poly_record(pm),q=poly_record(qm),r=poly_record(rm),H=poly_record(hm)),(wa,fa,ja,pm,qm,rm,hm)

def direct_omega(m,s):
    tail=[(b,c,d) for b in range(s+1) for c in range(s+1-b) for d in range(s+1-b-c)]
    configs=[]
    for tails in product(tail,repeat=m):
        B=sum(b for b,c,d in tails);C=sum(c for b,c,d in tails);D=sum(d for b,c,d in tails)
        n=3*s-B-C-D
        if n<0:
            continue
        for x in range(n+1):
            for y in range(n+1-x):
                z=n-x-y
                L=max(0,y-x,s-C-x,y+C-s,s-x-B+y-z,y-s+D)
                h=min(y-x,s-x-B,y-s+D)
                configs.append((x,y,z,tails,L,h,max(x+B-s,0)))
    return configs

def controls(m,ps):
    w,f,js,pm,qm,rm,hm=ps
    M,A,B=a(3*m+2,3),a(3*m-1,2),a(3*m-4,1)
    double=mul(S,(-1,1),B,hm)
    missing_double=sub(f,double)
    missing_one_moment=sub(f,scale(js[1],4*m))
    wrong_sign=add(f,scale(mul(S,B,hm),2))
    wrong_w=add(w,scale(mul(S,B,qm),2))
    out=dict(m=m,omit_double_caps=poly_record(missing_double,3*m+3),
             complete_minus_omit_double=poly_record(double,3*m+3),
             omit_one_cap_moment=poly_record(missing_one_moment,3*m+3),
             complete_minus_omit_one_moment=poly_record(scale(js[1],4*m),3*m+3),
             wrong_S_minus_1_sign=poly_record(wrong_sign,3*m+3),
             wrong_sign_extra=poly_record(sub(wrong_sign,f),3*m+3),
             wrong_slope_S_minus_1_sign=poly_record(wrong_w,3*m+3),
             formal_below_collar=[dict(U_multiple=k,classification='FORMAL_EXTRAPOLATION_NOT_LR_CANDIDATE',
                                      polynomial=poly_record(add(f,scale(mul(S,w),k-3)),3*m+3)) for k in range(3)])
    assert missing_double!=f and missing_one_moment!=f and wrong_sign!=f
    assert evalp(wrong_w,1)!=evalp(w,1)
    return out

def orbit_control():
    m,s=3,1
    whole=direct_omega(m,s)
    assert len(whole)==evalp(w_numerator(m)[0],s)
    sum_cost=sum(L-h for x,y,z,t,L,h,j in whole)
    sum_j=sum(j for x,y,z,t,L,h,j in whole)
    assert sum_cost==4*sum_j
    seed=(0,0,3,((0,0,0),)*m)
    orbit=set()
    for pi in permutations(range(3)):
        xyz=tuple(seed[k] for k in pi)
        for rho in permutations(range(3)):
            ts=tuple(tuple(t[k] for k in rho) for t in seed[3])
            orbit.add(xyz+(ts,))
    rows=[]
    for x,y,z,ts in sorted(orbit):
        B=sum(t[0] for t in ts);C=sum(t[1] for t in ts);D=sum(t[2] for t in ts)
        L=max(0,y-x,s-C-x,y+C-s,s-x-B+y-z,y-s+D)
        h=min(y-x,s-x-B,y-s+D)
        j=max(x+B-s,0)
        rows.append(dict(x=x,y=y,z=z,tails=ts,L=L,h=h,cost=L-h,four_J=4*j,imbalance=L-h-4*j))
    assert any(row['imbalance'] for row in rows)
    assert sum(row['imbalance'] for row in rows)==0
    grades=[]
    for mm,ss in [(3,0),(3,1),(3,2),(4,0),(4,1)]:
        configs=direct_omega(mm,ss)
        w0=len(configs);j0=sum(c[-1] for c in configs)
        wpoly=w_numerator(mm)[0]
        jpoly=add(j_vandermonde(mm,0),scale(j_vandermonde(mm,1),-mm),
                  scale(j_vandermonde(mm,2),comb(mm,2)))
        assert w0==evalp(wpoly,ss) and j0==evalp(jpoly,ss)
        counts=[]
        for k in range(4):
            formal=(k*ss+1)*w0-4*j0
            clipped=sum(max(0,k*ss+1+c[5]-c[4]) for c in configs)
            counts.append(dict(U_multiple=k,formal_interval_sum=formal,clipped_interval_sum=clipped,
                               classification='STABLE_IDENTITY' if k==3 else 'FORMAL_EXTRAPOLATION_NOT_LR_CANDIDATE'))
        assert counts[3]['formal_interval_sum']==counts[3]['clipped_interval_sum']
        grades.append(dict(m=mm,S=ss,W=w0,J=j0,collar_counts=counts,
                           double_caps_empty=ss in (0,1)))
    return dict(whole_Omega=dict(m=m,S=s,count=len(whole),sum_L_minus_h=sum_cost,four_sum_J=4*sum_j),
                pointwise_counterexample_and_complete_orbit=rows,direct_grade_checks=grades)

def slope_base():
    m=3
    M,A,B=a(3*m+2,3),a(3*m-1,2),a(3*m-4,1)
    G=add(M,scale(mul(S,PBAR,A),-1),scale(mul(S,QBAR,B),-1))
    w=w_numerator(m)[0]
    terms=[mul(S,sub(PBAR,p_polynomial(m)),A),mul(S,sub(QBAR,q_polynomial(m)),B),mul(S,S,q_polynomial(m),B)]
    assert add(*terms)==sub(w,G)
    assert len(G)-1==11 and all(c>0 for c in G)
    assert all(all(c>=0 for c in p) for p in terms)
    return dict(m=m,G=poly_record(G,11),integer_form=integer_form(G),W_minus_G=poly_record(sub(w,G),11),
                compensation_terms=[poly_record(p,11) for p in terms])

def run(phase,out):
    out=Path(out)
    assert not out.exists(), "Choose a fresh output directory"
    out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic()
    mlist=[3] if phase=='pilot' else list(range(3,13))
    rows=[];negative=[];ctrl=[]
    for m in mlist:
        ms=time.monotonic()
        row,ps=complete(m);rows.append(row)
        for i in row['G']['negative_slots']:
            negative.append(dict(m=m,degree=i,G=row['G']['coefficients'][i],F=row['F']['coefficients'][i],
                                 compensation=row['F_minus_G']['coefficients'][i],
                                 five_terms=[p['coefficients'][i] for p in row['compensation_terms']]))
        ctrl.append(controls(m,ps))
        print(json.dumps(dict(m=m,seconds=time.monotonic()-ms,F_degree=row['F']['actual_degree'],
                              W_degree=row['W']['actual_degree'],negative_G_slots=row['G']['negative_slots'])),flush=True)
    slope=slope_base()
    boundary=[]
    for m in mlist:
        w,_=w_numerator(m)
        jj=[j_vandermonde(m,j) for j in range(3)]
        assert evalp(w,0)==1 and all(evalp(j,0)==0 for j in jj)
        assert evalp(jj[2],1)==0
        assert all(evalp(cap,ss)==0 for cap in w_violation(m)[1][1:] for ss in ([0] if cap==w_violation(m)[1][1] else [0,1]))
        boundary.append(dict(m=m,S0_W=1,S0_J_caps=['0','0','0'],S1_double_moment=0,
                             s0_original='1+ut; degree one for u>0 and point for u=0'))
    g12_factor=None
    if phase=='full':
        gp=tuple(Q(c) for c in rows[-1]['G']['coefficients'])
        assert all(c>0 for c in gp) and len(gp)==40
        factor=a(12,1);quotient=divide_exact(gp,factor)
        assert len(quotient)==28 and all(c>0 for c in quotient)
        assert mul(factor,quotient)==gp
        g12_factor=dict(positive_factor=poly_record(factor),quotient=poly_record(quotient,27),
                         quotient_integer_form=integer_form(quotient),G12_integer_form=integer_form(gp),
                         multiplication_exact=True,independently_derived_before_appendix_read=True)
    result=dict(schema='a82-independent-four-letter-finite/v1',phase=phase,complete_rows=rows,
                finite_bridge_m=list(range(3,12)) if phase=='full' else [],
                G12=rows[-1]['G'] if phase=='full' else None,G12_factorization=g12_factor,
                slope_G3=slope,failed_sufficient_bound_same_coefficient_records=negative,
                omission_and_formal_controls=ctrl,boundary=boundary,
                orbit_and_direct=orbit_control(),seconds=time.monotonic()-start,
                provider_numeric_data_read=False,returned_programs_executed=False,
                new_named_originals=0,new_LR_or_table_oracle_calls=0)
    (out/'FINITE-CERTIFICATES.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',phase=phase,seconds=result['seconds'],m=mlist,
                          complete_F_slots=sum(len(r['F']['coefficients']) for r in rows),
                          negative_sufficient_bound_slots=len(negative))),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=['pilot','full'],required=True);p.add_argument('--output',required=True)
    z=p.parse_args();run(z.phase,z.output)
