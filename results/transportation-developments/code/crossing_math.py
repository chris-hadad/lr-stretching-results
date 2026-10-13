"""Exact trusted root mathematical functions; orchestration excluded."""
from __future__ import annotations

import argparse

import hashlib

import importlib.util

import itertools

import json

import math

import time

from fractions import Fraction as Q

from pathlib import Path

T = Path(__file__).resolve().parents[1]

M = T

CERT = M / 'data/crossing/CHAMBER-CERTIFICATE-v1.json'

ZERO_CERT = M / 'data/crossing/ZERO-BASE-CERTIFICATE-v1.json'

E0 = (0, 0, 0, 0)

ONE = {E0: Q(1)}

VARS = tuple({tuple(int(i == j) for i in range(4)): Q(1)} for j in range(4))

def scalar(value):
    q = Q(value)
    return {E0: q} if q else {}

def add(*terms):
    out = {}
    for term in terms:
        for e, c in term.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}

def neg(term):
    return {e: -c for e, c in term.items()}

def scale(term, value):
    q = Q(value)
    return {e: q*c for e, c in term.items()} if q else {}

def mul(left, right):
    if not left or not right:
        return {}
    out = {}
    for e, c in left.items():
        for f, d in right.items():
            if e[3] + f[3] > 1:
                continue
            g = tuple(e[i] + f[i] for i in range(4))
            out[g] = out.get(g, 0) + c*d
    return {e: c for e, c in out.items() if c}

def prod(*terms):
    out = ONE
    for term in terms:
        out = mul(out, term)
    return out

def power(term, n):
    out = ONE
    for _ in range(n):
        out = mul(out, term)
    return out

def diff(term, axis):
    out = {}
    for e, c in term.items():
        if e[axis]:
            f = list(e)
            f[axis] -= 1
            out[tuple(f)] = c * e[axis]
    return out

def binomial_poly(top, lower):
    out = ONE
    for j in range(lower):
        out = scale(mul(out, add(top, scalar(-j))), Q(1, j+1))
    return out

def b(value):
    return scale(prod(add(value, scalar(1)), add(value, scalar(2))), Q(1, 2))

def tail(h, other, a):
    top = add(h, scalar(2*a-1))
    return add(prod(add(scalar(2), other, scale(h, -Q(1, 2))),
                    binomial_poly(top, 2*a+1)),
               binomial_poly(top, 2*a+2))

def singleton(h, other, x, a):
    top = add(h, neg(x), scalar(2*a-3))
    common = add(scalar(2), other, scale(h, -Q(1, 2)))
    return add(prod(add(scalar(2), x), common,
                    binomial_poly(top, 2*a)),
               prod(add(scalar(4), x, other, scale(h, -Q(1, 2))),
                    binomial_poly(top, 2*a+1)),
               binomial_poly(top, 2*a+2))

def chamber(a, which):
    u, v, w, z = VARS
    if which == 'both':
        x = u
        s = add(u, v)
        r = add(u, v, w)
        axes = (0, 1)
    elif which == 'one':
        s = u
        x = add(u, v)
        r = add(u, v, w)
        axes = (1, 2)
    else:
        raise ValueError(which)
    k = add(x, scale(r, a-1), z)
    nr = prod(b(x), power(b(r), a-2), b(add(r, z)))
    linear = add(scalar(1), scale(k, Q(5, 4)), neg(r), neg(s))
    quadratic = add(prod(add(scale(k, Q(2, 3)), neg(r)),
                         add(scale(k, Q(2, 3)), neg(s))),
                    scale(add(prod(x, x), scale(prod(r, r), a-2),
                              prod(add(r, z), add(r, z))), -Q(1, 36)))
    f = add(prod(nr, add(linear, quadratic)),
            tail(r, add(k, neg(s)), a),
            tail(s, add(k, neg(r)), a),
            neg(singleton(r, add(k, neg(s)), x, a)))
    if which == 'both':
        f = add(f, neg(singleton(s, add(k, neg(r)), x, a)))
    # At fixed r,s,other caps: both uses d/du-d/dv; one uses d/dv-d/dw.
    return add(diff(f, axes[0]), neg(diff(f, axes[1])))

def exponents(degree):
    for z in (0, 1):
        for u in range(degree-z+1):
            for v in range(degree-z-u+1):
                for w in range(degree-z-u-v+1):
                    yield (u, v, w, z)

def check_certificate():
    data = json.loads(CERT.read_text())
    assert data['schema'] == 'a63-crossing-certificate/v1'
    rows = {(row['a'], row['chamber']): row for row in data['rows']}
    assert len(rows) == 12 and set(rows) == {(a, c) for a in range(3, 9) for c in ('both', 'one')}
    records = []
    for a in range(3, 9):
        for which in ('both', 'one'):
            row = rows[a, which]
            degree = 2*a+1
            assert row['variables'] == ['u','v','w','Z']
            assert row['full_domain'] == dict(total_degree_at_most=degree,
                                              Z_degree_at_most=1,
                                              omitted_coefficients='exact zero')
            expected = {}
            for item in row['coefficients']:
                e = tuple(item['exponents'])
                assert len(e) == 4 and all(type(i) is int and i >= 0 for i in e)
                assert e[3] <= 1 and sum(e) <= degree and e not in expected
                value = Q(item['value'])
                assert value
                expected[e] = value
            got = chamber(a, which)
            assert set(got).issubset(set(exponents(degree)))
            all_e = list(exponents(degree))
            mismatch = [(e, str(got.get(e, 0)), str(expected.get(e, 0)))
                        for e in all_e if got.get(e, 0) != expected.get(e, 0)]
            assert not mismatch, (a, which, mismatch[:8], len(mismatch))
            assert all(got.get(e, 0) >= 0 for e in all_e)
            supports = {(item['parameter_degree'],item['variable']): Q(item['value'])
                        for item in row['strict_support']}
            axes = (0,) if which == 'both' else (0,1)
            assert len(supports) == (degree+1)*len(axes)
            for j in range(degree+1):
                for axis in axes:
                    e = tuple(j if i == axis else 0 for i in range(4))
                    assert got.get(e, 0) == supports[j, axis] > 0, (a, which, e)
            records.append(dict(a=a,chamber=which,full_domain=len(all_e),
                                nonzero=len(expected),zero=len(all_e)-len(expected),
                                negative=0,strict_support=len(supports),
                                coefficient_sha256=hashlib.sha256(json.dumps(
                                    [(e,str(got.get(e,0))) for e in all_e],
                                    separators=(',',':')).encode()).hexdigest()))
    return dict(rows=records,identities=len(records),
                full_domain=sum(x['full_domain'] for x in records),
                nonzero=sum(x['nonzero'] for x in records),
                zero=sum(x['zero'] for x in records),
                strict_support=sum(x['strict_support'] for x in records))

def check_zero_base():
    """Rebuild the two-positive-cap base in its own four chamber coordinates."""
    data = json.loads(ZERO_CERT.read_text())
    assert data['schema'] == 'a63-zero-base/v1'
    assert data['variables'] == ['s', 'r-s', 'k1-r', 'k2-r']
    assert data['full_degree'] == 6 and data['omitted_coefficients'] == 'exact zero'
    return compare_zero_base_unrestricted(data)

def compare_zero_base_unrestricted(data):
    def umul(left,right):
        out={}
        for e,c in left.items():
            for f,d in right.items():
                g=tuple(e[i]+f[i] for i in range(4))
                out[g]=out.get(g,0)+c*d
        return {e:c for e,c in out.items() if c}
    def uprod(*terms):
        out=ONE
        for term in terms:out=umul(out,term)
        return out
    def ubin(top,lower):
        out=ONE
        for j in range(lower):out=scale(umul(out,add(top,scalar(-j))),Q(1,j+1))
        return out
    def ub(value):
        return scale(uprod(add(value,scalar(1)),add(value,scalar(2))),Q(1,2))
    def utail(h,other):
        top=add(h,scalar(3))
        return add(uprod(add(scalar(2),other,scale(h,-Q(1,2))),ubin(top,5)),
                   ubin(top,6))
    s,gap,e1,e2=VARS
    r=add(s,gap);k1=add(r,e1);k2=add(r,e2);k=add(k1,k2)
    n=uprod(ub(k1),ub(k2))
    linear=add(scalar(1),scale(k,Q(5,4)),neg(r),neg(s))
    quadratic=add(uprod(add(scale(k,Q(2,3)),neg(r)),
                         add(scale(k,Q(2,3)),neg(s))),
                  scale(add(uprod(k1,k1),uprod(k2,k2)),-Q(1,36)))
    got=add(uprod(n,add(linear,quadratic)),
            utail(r,add(k,neg(s))),utail(s,add(k,neg(r))))
    expected={}
    for item in data['coefficients']:
        e=tuple(item['exponents']);value=Q(item['value'])
        assert len(e)==4 and all(type(i) is int and i>=0 for i in e)
        assert sum(e)<=6 and e not in expected and value
        expected[e]=value
    domain=[(i,j,k,l) for i in range(7) for j in range(7-i)
            for k in range(7-i-j) for l in range(7-i-j-k)]
    assert set(got).issubset(set(domain))
    mismatch=[(e,str(got.get(e,0)),str(expected.get(e,0))) for e in domain
              if got.get(e,0)!=expected.get(e,0)]
    assert not mismatch, (mismatch[:8],len(mismatch))
    assert all(got.get(e,0)>=0 for e in domain)
    supports={(x['degree'],x['variable']):Q(x['value'])
              for x in data['strict_support']}
    assert len(supports)==14
    for degree in range(7):
        for axis in (0,1):
            e=tuple(degree if i==axis else 0 for i in range(4))
            assert got.get(e,0)==supports[degree,axis]>0
    return dict(full_domain=len(domain),nonzero=len(expected),
                zero=len(domain)-len(expected),strict_support=len(supports))

def degree(caps):
    return 2*sum(k > 0 for k in caps)+2
