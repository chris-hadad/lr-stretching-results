"""Accepted exact polynomial primitives; counting/oracle/runtime code excluded."""
from fractions import Fraction as F
from math import factorial

def trim(p):
    p = [F(x) for x in p]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def add(*ps):
    q = [F(0)] * max(map(len, ps))
    for p in ps:
        for j, x in enumerate(p):
            q[j] += x
    return trim(q)

def scale(p, c):
    return trim([F(c) * x for x in p])

def mul(*ps):
    p = [F(1)]
    for q in ps:
        r = [F(0)] * (len(p) + len(q) - 1)
        for i, x in enumerate(p):
            for j, y in enumerate(q):
                r[i + j] += x * y
        p = trim(r)
    return p

def binpoly(slope, offset, n):
    return scale(mul(*[[offset - j, slope] for j in range(n)]), F(1, factorial(n)))

def at(p, t):
    v = F(0)
    for x in reversed(p):
        v = v * t + x
    return v

def dominates(large, small):
    return all(x >= 0 for x in add(large, scale(small, -1)))

def serial(o):
    if isinstance(o, F):
        return str(o)
    if isinstance(o, dict):
        return {k: serial(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [serial(x) for x in o]
    return o
