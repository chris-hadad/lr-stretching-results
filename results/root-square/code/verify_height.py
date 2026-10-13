"""Root exact all-grade moment algebra; no LR count or source program imports."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json, time, sys

def add(a,b):
    c=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return c
def scale(a,c): return [x*c for x in a]
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c
def power(a,n):
    b=[F(1)]
    for _ in range(n): b=mul(b,a)
    return b
def binpoly(slope,offset,k):
    p=[F(1)]
    for j in range(k): p=mul(p,[F(offset-j),F(slope)])
    return scale(p,F(1,factorial(k)))
def moments(m):
    D=power([F(1),F(3,2),F(1,2)],m);L=[F(0)]
    for j in range(m+1):
        L=add(L,scale(mul(power([F(1),F(1)],m-j),binpoly(1,m,m+j+1)),(-1)**j*comb(m,j)))
    R=add(binpoly(2,2*m,2*m+1),scale(add(mul([F(2),F(1)],binpoly(1,2*m-2,2*m)),binpoly(1,2*m-2,2*m+1)),-m))
    return D,L,R
def at_sum(p):
    return {(i,d-i):c*comb(d,i) for d,c in enumerate(p) for i in range(d+1)}
def biadd(a,b):
    c=dict(a)
    for k,v in b.items(): c[k]=c.get(k,F(0))+v
    return c
def shift_w(a): return {(i,j+1):v for (i,j),v in a.items()}
def coefficient_records(a,d):
    return [{'q_degree':i,'w_degree':j,'value':str(a.get((i,j),F(0)))} for i in range(d+1) for j in range(d+1-i)]
def main():
    start=time.monotonic();records=[]
    for m in [4,5,6]:
        D,L,R=moments(m)
        if m==4:
            C=add(add(mul([F(1),F(m+3,3)],D),scale(L,-3)),scale(R,-1))
            p=biadd(at_sum(C),shift_w(at_sum(D)))
            # Here S=q+w and the independent augmentation is recorded separately.
            records.append({'m':m,'scope':'Complete first extended wall U=3S, plus V*D for arbitrary V>=0','wall_coefficients':[str(x) for x in C],'degree':2*m+1,'strict':all(x>0 for x in C),'D':[str(x) for x in D],'L':[str(x) for x in L],'R':[str(x) for x in R]})
        else:
            C=add(add(mul([F(1),F(m,3)],D),scale(L,-3)),scale(R,-1))
            p=biadd(at_sum(C),shift_w(at_sum(D)))
            correction=scale(binpoly(1,2*m-1,2*m+1),3)
            p=biadd(p,{(i,0):v for i,v in enumerate(correction)})
            records.append({'m':m,'scope':'Entire second band S=q+w,U=(m-2)q+(m-1)w, q,w>=0','coefficients':coefficient_records(p,2*m+1),'all_coefficients_nonnegative':all(x>=0 for x in p.values()),'axis_q_strict':all(p.get((i,0),F(0))>0 for i in range(2*m+2)),'axis_w_strict':all(p.get((0,i),F(0))>0 for i in range(2*m+2)),'D':[str(x) for x in D],'L':[str(x) for x in L],'R':[str(x) for x in R],'complete_correction':[str(x) for x in correction]})
    I=F(1)
    for j in range(1,8): I*=F(2*j,2*j+1)
    c7=I+F(2,9);r7=F(4,15)+F(14,13*15);beta=F(7,3)-3*c7-r7-F(3,14*15)
    result={'schema':'a80-collar-all-grade-algebra/v1','status':'PROPOSED_EXACT_ALGEBRA','records':records,'uniform_m7_beta':str(beta),'uniform_m7_c':str(c7),'uniform_m7_r':str(r7),'all_finite_bases_pass':all(r.get('strict',r.get('all_coefficients_nonnegative',False)) for r in records),'no_original_counts':True,'seconds':time.monotonic()-start}
    out=Path(sys.argv[1])
    with out.open('x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps({'bases_pass':result['all_finite_bases_pass'],'beta':str(beta),'seconds':result['seconds']}))
if __name__=='__main__':main()
