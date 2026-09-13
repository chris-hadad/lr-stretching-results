"""Exact rational polynomial arithmetic selected from the accepted root checker.

Arithmetic functions retain the source formulas. SOURCE-MAP.json identifies
that checker; this module has no campaign filesystem or execution dependency.
"""
from fractions import Fraction as Q
from math import factorial


class CheckError(ValueError):
    pass


def need(predicate, message):
    if not predicate:
        raise CheckError(message)


def integer(value):
    if type(value) is int:
        return value
    if type(value) is str and value and (value.isdecimal() or (value[0] == "-" and value[1:].isdecimal())):
        return int(value)
    raise CheckError("Expected an exact integer, with no float or boolean")


def rational(value):
    need(type(value) in (int, str), "Expected an exact rational string or integer")
    return Q(value)


def trim(p):
    p=list(map(Q,p))
    while len(p)>1 and p[-1]==0:p.pop()
    return p or [Q(0)]

def plus(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def scale(p,c):return trim([Q(c)*x for x in p])

def minus(a,b):return plus(a,scale(b,-1))

def times(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)

def shift(p,n=1):return trim([Q(0)]*n+list(p))

def evaluate(p,x):
    out=Q(0)
    for c in reversed(p):out=out*x+c
    return out

def lagrange(xs,ys):
    need(len(xs)==len(ys) and len(set(xs))==len(xs),"Duplicate/missing interpolation node")
    out=[Q(0)]
    for i,x in enumerate(xs):
        basis=[Q(1)];den=Q(1)
        for j,y in enumerate(xs):
            if i!=j:basis=times(basis,[-y,1]);den*=x-y
        out=plus(out,scale(basis,Q(ys[i])/den))
    return out

def newton(xs,ys):
    a=list(map(Q,ys));out=[Q(0)];basis=[Q(1)]
    for order in range(len(xs)):
        if order:
            for i in range(len(xs)-1,order-1,-1):
                a[i]=(a[i]-a[i-1])/Q(xs[i]-xs[i-order])
            basis=times(basis,[-xs[order-1],1])
        out=plus(out,scale(basis,a[order]))
    return out

def binomial_polynomial(slope,offset,k):
    p=[Q(1)]
    for j in range(k):p=times(p,[offset-j,slope])
    return scale(p,Q(1,factorial(k)))
