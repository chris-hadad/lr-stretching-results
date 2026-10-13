"""Root exact all-grade moment algebra; no LR count or source program imports."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import json, time

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
