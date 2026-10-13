#!/usr/bin/env python3
"""A79 independent algebra audit. Root-launch only; provider bytes are inert.

Every arithmetic operation below is exact. No third-party dependency, subprocess,
network access, dynamic evaluation, provider module import, or LR count engine.
The Markdown table reader accepts a tiny mathematical AST as data, never code.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys
import time


VARS = ("x", "h", "b", "z", "v", "w", "s", "g", "n", "k", "m", "r", "u")
DIM = len(VARS)
ZERO = (0,) * DIM
POS = {name: i for i, name in enumerate(VARS)}
DEFAULT_SOURCE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PINS = {'U03': ('proofs/pro053/U03.md', 'cfa814760d6538760e00cf488480a56851b0c05bb6e464ef02148378fb765a86'), 'U05': ('proofs/pro053/U05.md', '27450456d5f5d2b175118654a5a68350f148da3651537ad7454d1d6e94a8c928'), 'U05_SIGN': ('proofs/pro053/U05_SIGN.md', '7d849f2a856c1b7263471fbd788f31d5bbb1a5f959a2c79cf39f833f4607c817'), 'U11': ('proofs/pro053/U11.md', '2035cca4dab3922cf207b18dabcb0112d4904d8ea5430adff480011b8921bb50'), 'U12': ('proofs/pro053/U12.md', '72182cab0c074b06a21ec385e43d02c1d499409afd0d7fcbaf42e59c8ae9239f'), 'ROOT_PROOF': ('proofs/A79-UNIFORM-TRIANGLE-v1.md', 'd10f3be03444c4e341fa33b0c2f50f757d368f5225d56357780df5fd55d4f305')}
ROOT_PROOF_VERSIONS = {'d10f3be03444c4e341fa33b0c2f50f757d368f5225d56357780df5fd55d4f305': "curated-accepted-proof"}


class P:
    """Sparse polynomial in explicitly named variables over Fraction."""

    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.t = terms.t
        elif isinstance(terms, dict):
            self.t = {e: F(c) for e, c in terms.items() if c}
        else:
            c = F(terms)
            self.t = {ZERO: c} if c else {}

    @staticmethod
    def var(name):
        e = list(ZERO)
        e[POS[name]] = 1
        return P({tuple(e): 1})

    def __add__(self, other):
        if isinstance(other, R):
            return NotImplemented
        other = P(other)
        out = dict(self.t)
        for e, c in other.t.items():
            out[e] = out.get(e, F(0)) + c
            if not out[e]:
                del out[e]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        if isinstance(other, R):
            return NotImplemented
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        if isinstance(other, R):
            return NotImplemented
        other = P(other)
        out = {}
        for e, c in self.t.items():
            for f, d in other.t.items():
                key = tuple(a + b for a, b in zip(e, f))
                out[key] = out.get(key, F(0)) + c * d
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (1 / F(other))

    def __pow__(self, power):
        if not isinstance(power, int) or not 0 <= power <= 100:
            raise ValueError("polynomial exponent out of bound")
        out, base = P(1), self
        while power:
            if power & 1:
                out = out * base
            power //= 2
            if power:
                base = base * base
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def diff(self, name):
        i = POS[name]
        out = {}
        for e, c in self.t.items():
            if e[i]:
                f = list(e)
                f[i] -= 1
                out[tuple(f)] = c * e[i]
        return P(out)

    def sub(self, **replacements):
        if not replacements or not self.t:
            return self
        idx = {POS[k]: P(v) for k, v in replacements.items()}
        powers = {(i, j): p**j for i, p in idx.items()
                  for j in range(1 + max(e[i] for e in self.t))}
        out = P(0)
        for e, c in self.t.items():
            f = list(e)
            term = P(c)
            for i in idx:
                term = term * powers[i, e[i]]
                f[i] = 0
            out = out + term * P({tuple(f): 1})
        return out

    def coeff(self, **exponents):
        idx = {POS[k]: v for k, v in exponents.items()}
        out = {}
        for e, c in self.t.items():
            if all(e[i] == j for i, j in idx.items()):
                f = tuple(0 if i in idx else a for i, a in enumerate(e))
                out[f] = out.get(f, F(0)) + c
        return P(out)

    def degree(self):
        return max((sum(e) for e in self.t), default=-1)

    def support(self):
        return {VARS[i] for e in self.t for i, a in enumerate(e) if a}

    def exact_div(self, divisor):
        """Sparse long division; return None if not a polynomial quotient."""
        divisor = P(divisor)
        if not divisor.t:
            raise ZeroDivisionError
        lead = max(divisor.t)
        lc = divisor.t[lead]
        remainder = dict(self.t)
        out = {}
        while remainder:
            e = max(remainder)
            if any(a < b for a, b in zip(e, lead)):
                return None
            q = tuple(a - b for a, b in zip(e, lead))
            c = remainder[e] / lc
            out[q] = out.get(q, F(0)) + c
            for f, d in divisor.t.items():
                k = tuple(a + b for a, b in zip(q, f))
                remainder[k] = remainder.get(k, F(0)) - c * d
                if not remainder[k]:
                    del remainder[k]
        return P(out)

    def key(self):
        return tuple(sorted((e, c) for e, c in self.t.items()))


class R:
    """Rational sparse polynomial with a factored index-only denominator."""

    def __init__(self, numerator=0, factors=None):
        if isinstance(numerator, R):
            self.p, self.d = numerator.p, numerator.d
            return
        self.p = P(numerator)
        self.d = dict(factors or {})
        if not self.p.t:
            self.d = {}

    @staticmethod
    def over(numerator, *factors):
        numerator = R(numerator)
        ds = dict(numerator.d)
        p = numerator.p
        for factor in factors:
            factor = P(factor)
            if factor.support() - {"n", "k", "m", "r"}:
                raise ValueError("rational denominator contains margin variable")
            if not factor.support():
                p = p / factor.t.get(ZERO, F(0))
            else:
                key = factor.key()
                ds[key] = ds.get(key, 0) + 1
        return R(p, ds).reduce()

    def reduce(self):
        p, ds = self.p, dict(self.d)
        for key, count in self.d.items():
            factor = P(dict(key))
            for _ in range(count):
                divided = p.exact_div(factor)
                if divided is None:
                    break
                p = divided
                ds[key] -= 1
            if not ds[key]:
                del ds[key]
        return R(p, ds)

    def denominator(self):
        out = P(1)
        for key, count in self.d.items():
            out = out * P(dict(key))**count
        return out

    def __add__(self, other):
        other = R(other)
        ds = {key: max(self.d.get(key, 0), other.d.get(key, 0))
              for key in set(self.d) | set(other.d)}
        left, right = self.p, other.p
        for key, count in ds.items():
            factor = P(dict(key))
            left = left * factor**(count - self.d.get(key, 0))
            right = right * factor**(count - other.d.get(key, 0))
        return R(left + right, ds).reduce()

    __radd__ = __add__

    def __neg__(self):
        return R(-self.p, self.d)

    def __sub__(self, other):
        return self + -R(other)

    def __rsub__(self, other):
        return R(other) + -self

    def __mul__(self, other):
        other = R(other)
        ds = dict(self.d)
        for key, count in other.d.items():
            ds[key] = ds.get(key, 0) + count
        return R(self.p * other.p, ds).reduce()

    __rmul__ = __mul__

    def __truediv__(self, other):
        return R.over(self, other)

    def sub(self, **replacements):
        out = R(self.p.sub(**replacements))
        for key, count in self.d.items():
            factor = P(dict(key)).sub(**replacements)
            out = R.over(out, *(factor for _ in range(count)))
        return out

    def coeff(self, **exponents):
        return R(self.p.coeff(**exponents), self.d)

    def equals_fraction(self, numerator, denominator=1):
        return self.p * P(denominator) == P(numerator) * self.denominator()

    def polynomial(self):
        out = self.p.exact_div(self.denominator())
        if out is None:
            raise ValueError("expression does not clear to a polynomial")
        return out


x, h, b, z, v, w, s, g, n, k, m, r, u = (P.var(name) for name in VARS)


def prod(items):
    out = P(1)
    for item in items:
        out = out * item
    return out


def abinom(top, bottom):
    """Generalized finite-product binomial polynomial; never a counting clamp."""
    if bottom < 0:
        return P(0)
    return prod(P(top) - j for j in range(bottom)) / math.factorial(bottom)


def aa(order, arg):
    return abinom(P(arg) + order, order)


def dd(order, arg):
    return P(1) if order == 0 else abinom(P(arg) + order - 1, order)


def ibinom(top, bottom):
    if bottom < 0:
        return 0
    num = math.prod(top - j for j in range(bottom))
    return num // math.factorial(bottom)


def count_a(order, arg):
    if order < 0 or arg < 0:
        return 0
    return math.comb(arg + order, order)


def newton_v(N, X=x, W=w):
    return sum((abinom(X + N, N + j) * abinom(W + N - 1, N - j)
                for j in range(N + 1)), P(0))


def rising_v(N, X=x, W=w, wrong_terminal=False):
    return sum((dd(j, W) * dd(2 * N - j, X)
                for j in range(N)), P(0)) + dd(N, W) * (
                    dd(N, X) if wrong_terminal else aa(N, X))


def uncapped_u(N, X=x, W=w):
    return aa(N, X) * aa(N, X + W)


def kn(N, X=x):
    return aa(N, X)**2 - (N + 1) * dd(2 * N, X)


def pair_low(N, X=x, H=h):
    return (X + 1) * abinom(H + 2 * N - 3, 2 * N - 1) - (
        N - 1) * abinom(H + 2 * N - 3, 2 * N)


def pair_high(N, X=x, Z=z):
    H = X + Z
    return pair_low(N, X, H) + sum((
        (j + 1) * abinom(X + N, N - 2 - j) *
        abinom(Z + N - 2, N + 2 + j) for j in range(N - 1)), P(0))


def triple_low_formula(N, X=x, G=g):
    return aa(2, X) * abinom(G + 2 * N - 5, 2 * N - 2) - (
        N - 2) * (X + 1) * abinom(G + 2 * N - 5, 2 * N - 1) + F(
            (N - 2) * (N - 1), 2) * abinom(G + 2 * N - 5, 2 * N)


def triple_high_newton(N, X=x, V=v):
    return sum((math.comb(j + 2, 2) * abinom(X + N, N + j) *
                abinom(V + N - 3, N - j) for j in range(N + 1)), P(0))


def finite_triple(N, X, G, shift=3, drop_cutoff=False):
    if X < 0 or G < 0:
        raise ValueError("finite triple requires nonnegative margins")
    end = G - shift if drop_cutoff else min(X, G - shift)
    return sum(count_a(N - 3, I) * count_a(2, X - I) *
               count_a(N, G - I - shift) for I in range(end + 1))


def finite_pair(N, X, H, shift=2):
    return sum((X - I + 1) * count_a(N - 2, I) * count_a(N - 2, J) *
               (H - I - J - shift + 1)
               for I in range(min(X, H - shift) + 1)
               for J in range(H - shift - I + 1))


def read_math(text):
    """Restricted data parser. No calls, attributes, comprehensions, or eval."""
    if len(text) > 12000:
        raise ValueError("math cell too long")
    tree = ast.parse(text, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > 5000:
        raise ValueError("math AST too large")

    def walk(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return P(node.value)
        if isinstance(node, ast.Name) and node.id in POS:
            return P.var(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -walk(node.operand)
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                return walk(node.left) + walk(node.right)
            if isinstance(node.op, ast.Sub):
                return walk(node.left) - walk(node.right)
            if isinstance(node.op, ast.Mult):
                return walk(node.left) * walk(node.right)
            if (isinstance(node.op, ast.Pow) and isinstance(node.right, ast.Constant)
                    and type(node.right.value) is int):
                return walk(node.left)**node.right.value
        raise ValueError("forbidden mathematical data syntax: " + type(node).__name__)

    return walk(tree.body)


def read_sign_rows(markdown):
    block, rows = None, []
    for line_no, line in enumerate(markdown.splitlines(), 1):
        if line.startswith("## "):
            block = line[3:].strip()
        if line.startswith("| `"):
            fields = [part.strip().strip("`") for part in line.split("|")[1:-1]]
            if len(fields) != 3:
                raise ValueError("malformed sign row")
            monomial = fields[0].replace("^", "**").replace(" ", "*")
            mp = read_math(monomial)
            if len(mp.t) != 1 or next(iter(mp.t.values())) != 1:
                raise ValueError("invalid sign-table monomial")
            rows.append((block, next(iter(mp.t)), read_math(fields[1]),
                         read_math(fields[2]), line_no))
    return rows


def serialized(poly, names=None, degree=None):
    if names is None:
        names = [name for name in VARS if name in poly.support()]
    allowed = set(names)
    if poly.support() - allowed:
        raise ValueError("output omits a variable")
    terms = [[*[e[POS[name]] for name in names], str(c)]
             for e, c in sorted(poly.t.items())]
    out = {"variables": names, "degree": poly.degree(), "nonzero": len(poly.t),
           "terms": terms}
    if degree is not None:
        if len(names) != 2 or poly.degree() > degree:
            raise ValueError("bad complete two-variable matrix degree")
        out["degree_bound"] = degree
        out["complete_triangular_slots"] = [
            [i, j, str(poly.t.get(tuple(i if q == POS[names[0]] else
                                     j if q == POS[names[1]] else 0
                                     for q in range(DIM)), F(0)))]
            for i in range(degree + 1) for j in range(degree + 1 - i)]
        out["zero_slots"] = len(out["complete_triangular_slots"]) - len(poly.t)
    return out


class Audit:
    def __init__(self, output):
        self.output = output
        self.checks, self.controls, self.details = Counter(), Counter(), []
        self.start = time.monotonic()

    def check(self, group, ok, detail=None):
        self.checks[group] += 1
        if not ok:
            raise AssertionError((group, detail))

    def equal(self, group, left, right, detail=None):
        self.check(group, P(left) == P(right), detail)

    def positive(self, group, poly, strict=False, detail=None):
        self.check(group, all(c > 0 if strict else c >= 0 for c in poly.t.values()), detail)

    def reject(self, label, ok):
        self.controls[label] += 1
        if not ok:
            raise AssertionError(("control not rejected", label))

    def save(self, name, payload):
        path = self.output / name
        if path.exists():
            raise FileExistsError("immutable attempt output already exists: " + str(path))
        data = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
        path.write_bytes(data)
        return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data)}


def positive_rational(audit, group, expr, substitution, detail=None):
    expr = R(expr).sub(**substitution)
    audit.positive(group, expr.p, detail=detail)
    den = expr.denominator()
    audit.positive(group + "_denominator", den, detail=detail)
    audit.check(group + "_positive_denominator_constant", den.t.get(ZERO, 0) > 0, detail)
    return expr


def u03_certificates(audit):
    G1 = R(1) + R.over((n - 2) * x, n + 1)
    G2 = R(1) + R.over(3 * n * x, 2, n + 2) + R.over((n - 1) * (n + 4) * x**2, 2, n + 1, n + 2)
    E = G2 + R.over((h + n - 2) * G1, n - 1) - R.over(2 * (h + n - 2) * (h + n - 1), n, n - 1)
    Z = R.over(E, n - 2) + R.over(3 * (h - 1) * (b + R.over(2*n - 1, n) + R.over((n + 1)*h, 2, n)), 2, n - 1, 2*n - 1)
    E = E.sub(x=b+h)
    Z = Z.sub(x=b+h)
    de = 2*n*(n-1)*(n+1)*(n+2)
    dz = 4*n*(n-2)*(n-1)*(n+1)*(n+2)*(2*n-1)
    expected = [
        (0,0,"6*m**3+64*m**2+210*m+200","12*m**4+166*m**3+832*m**2+1790*m+1400"),
        (1,0,"5*m**4+56*m**3+223*m**2+382*m+246","20*m**5+268*m**4+1374*m**3+3404*m**2+4162*m+2100"),
        (0,1,"5*m**4+50*m**3+163*m**2+208*m+126","20*m**5+259*m**4+1260*m**3+2903*m**2+3286*m+1620"),
        (2,0,"m**4+14*m**3+65*m**2+124*m+84","4*m**5+66*m**4+400*m**3+1146*m**2+1576*m+840"),
        (1,1,"2*m**4+30*m**3+148*m**2+294*m+198","8*m**5+146*m**4+970*m**3+3010*m**2+4374*m+2340"),
        (0,2,"m**4+16*m**3+79*m**2+134*m+34","4*m**5+77*m**4+518*m**3+1533*m**2+1884*m+580"),
    ]
    certs=[]
    for ib, ih, es, zs in expected:
        for name, expr, den, text in (("E", E, de, es), ("Z", Z, dz, zs)):
            got = (expr.coeff(b=ib,h=ih) * den).sub(n=m+3)
            want = read_math(text)
            audit.check("U03_12_coefficient_identities", got.equals_fraction(want), (name,ib,ih))
            audit.positive("U03_shifted_numerator_signs", want, strict=True)
            certs.append({"name":name,"b":ib,"h":ih,"numerator":serialized(want)})
    for name, expr, den in (("E",E,de),("Z",Z,dz)):
        audit.check("U03_complete_support", expr.p.support() <= {"n","b","h"} and
                    max((e[POS["b"]]+e[POS["h"]] for e in expr.p.t),default=0)<=2,name)
        positive_rational(audit,"U03_denominator_domains",R.over(1,den),{"n":m+3})
    return certs


@lru_cache(maxsize=None)
def normalized_d(offset):
    if offset < 1:
        raise ValueError("normalized d requires offset>=1")
    return R.over(x * prod(x+n+i for i in range(1,offset)),
                  *(n+i for i in range(1,offset+1)))


@lru_cache(maxsize=None)
def normalized_binomial(K, shift):
    if K < shift:
        raise ValueError("uncancelled a_n factor at exceptional boundary")
    return R.over(prod(x+i for i in range(1-shift,1)) *
                  prod(x+n+i for i in range(1,K-shift+1)),
                  *(n+i for i in range(1,K+1)))


@lru_cache(maxsize=None)
def normalized_s(K, scale=1):
    return R(1) if K == 0 else sum((dd(j,scale*x)*normalized_d(K-j)
                                  for j in range(K)),R(0))+dd(K,scale*x)


@lru_cache(maxsize=None)
def normalized_d3_newton(K):
    return sum((R.over(math.comb(j+2,2)*ibinom(K-3,K-j)*
                       prod(x-i for i in range(j)),
                       *(n+i for i in range(1,j+1)))
                for j in range(K+1)),R(0))


@lru_cache(maxsize=None)
def normalized_u05(K):
    if K == 0:
        return R(1)
    if K == 1:
        return -(R(2)+R.over((n-2)*x,n+1))
    d2=3*normalized_binomial(K,2)
    if K >= 3:
        d2=d2+(K-2)*normalized_binomial(K,3)
    return R(aa(K,2*x))-3*normalized_s(K)+3*d2


@lru_cache(maxsize=None)
def normalized_w05(K):
    return sum((dd(j,x)*normalized_u05(K-j) for j in range(K+1)),R(0))-normalized_d3_newton(K)


@lru_cache(maxsize=1)
def u05_expressions():
    G1=R(1)+R.over((n-2)*x,n+1)
    G2=R(1)+R.over(3*n*x,2,n+2)+R.over((n-1)*(n+4)*x**2,2,n+1,n+2)
    EU=G2+R.over((x+k-2)*G1,k-1)-R.over(2*(x+k-2)*(x+k-1),k,k-1)
    ZU=R.over(EU,k-2)+R.over(3*((k+1)*x**2+(3*n-3)*x-(3*n+k-2)),n+k,n+k-1,n+k-2)
    A1=R(2)+R.over((n-2)*x,n+1)
    A2=R(1)+R.over(3*(n+3)*(n-2)*x,2,n+1,n+2)+R.over((n-1)*(n-2)*x**2,2,n+1,n+2)
    EM=A2-R.over((z+n-2)*A1,n-1)+R.over((z+n-2)*(z+n-1),n,n-1)
    BF=R(aa(2,x))-R.over((n-2)*(x+1)*(z-3),2*n-1)+R.over((n-2)*(n-1)*(z-3)*(z-4),4,n,2*n-1)
    ZM=R.over(aa(2,x)*EM,n-2)-R.over((z-1)*(z-2)*BF,2*n-2,2*n-3,2*n-4)
    EM4=EM.sub(n=4)
    ZM4=(R.over((1+x)*(1+x/4)*EM,n-2)-R.over((z-1)*(z-2)*BF,2*n-2,2*n-3,2*n-4)).sub(n=4)
    EH=A2-R.over((x+k-2)*A1,k-1)+R.over((x+k-2)*(x+k-1),k,k-1)
    L=n+k
    BH=10*(x+L-4)*(x+L-3)+5*(k-3)*(x-3)*(x+L-4)+(k-3)*(k-4)*(x-3)*(x-4)/2
    ZH=R.over(aa(2,x)*EH,k-2)-R.over((x-1)*(x-2)*BH,L,L-1,L-2,L-3,L-4)
    return {"U-E":EU,"U-Z":ZU,"MID-E":EM.sub(x=b+z),"MID-Z":ZM.sub(x=b+z),
            "HIGH-E":EH,"HIGH-Z":ZH,"W-K3":normalized_w05(3),
            "W-K4":normalized_w05(4),"MID-N4-E":EM4.sub(x=b+z),"MID-N4-Z":ZM4.sub(x=b+z)}


def u05_certificates(audit, sign_markdown):
    expressions=u05_expressions()
    subs={"U-E":{"n":m+3,"k":r+3},"U-Z":{"n":m+3,"k":r+3},
          "MID-E":{"n":m+5},"MID-Z":{"n":m+5},
          "HIGH-E":{"n":m+r+6,"k":r+5},"HIGH-Z":{"n":m+r+6,"k":r+5},
          "W-K3":{"n":m+4},"W-K4":{"n":m+5},"MID-N4-E":{},"MID-N4-Z":{}}
    rows=read_sign_rows(sign_markdown)
    audit.check("U05_exact_table_population",len(rows)==65)
    counts=Counter()
    outputs=[]
    for name, exponent, expected, den, line_no in rows:
        counts[name]+=1
        formal=("b","z") if name.startswith("MID") else ("x",)
        coefficient=expressions[name].coeff(**{q:exponent[POS[q]] for q in formal}).sub(**subs[name])
        shifted_den=den.sub(**subs[name])
        audit.check("U05_65_coefficient_identities",coefficient.equals_fraction(expected,shifted_den),(name,line_no))
        audit.positive("U05_shifted_numerator_signs",expected,strict=True)
        audit.positive("U05_shifted_denominator_signs",shifted_den)
        audit.check("U05_positive_denominator_constants",shifted_den.t.get(ZERO,0)>0,(name,line_no))
        outputs.append({"block":name,"source_line":line_no,"monomial":[exponent[POS[q]] for q in formal],
                        "numerator":serialized(expected),"denominator":serialized(shifted_den)})
    audit.check("U05_all_ten_blocks",dict(counts)=={"U-E":3,"U-Z":3,"MID-E":6,"MID-Z":15,"HIGH-E":3,"HIGH-Z":5,"W-K3":4,"W-K4":5,"MID-N4-E":6,"MID-N4-Z":15})
    for name,expr in expressions.items():
        names=("b","z") if name.startswith("MID") else ("x",)
        bound=4 if name in {"MID-Z","MID-N4-Z","HIGH-Z","W-K4"} else 3 if name=="W-K3" else 2
        audit.check("U05_full_formal_support",max((sum(e[POS[q]] for q in names) for e in expr.p.t),default=0)<=bound,name)
    return outputs


def u11_certificates(audit):
    alpha=R.over(n-1,n+1)
    G1=R(1)+alpha*x
    G2=R((1+x)*(1+x/2))-R.over(2*x*(x+n+1),n+1,n+2)
    E=G2+R.over((h+n-2)*G1,n-1)-R.over((h+n-2)*(h+n-1),n,n-1)
    residue=(E-R.over((n-3)*h,n,n-1)-1-x/2).sub(x=b+h)
    denominator=2*n*(n-1)*(n+1)*(n+2)
    expected=[(2,0,"m**4+18*m**3+115*m**2+314*m+312"),
              (1,1,"2*m**4+38*m**3+256*m**2+736*m+768"),
              (1,0,"4*m**4+62*m**3+350*m**2+856*m+768"),
              (0,2,"m**4+20*m**3+139*m**2+400*m+396"),
              (0,1,"4*m**4+58*m**3+302*m**2+692*m+648"),
              (0,0,"2*m**3+26*m**2+104*m+120")]
    out=[]
    for ib,ih,text in expected:
        got=(residue.coeff(b=ib,h=ih)*denominator).sub(n=m+4)
        want=read_math(text)
        audit.check("U11_6_monotonicity_identities",got.equals_fraction(want),(ib,ih))
        audit.positive("U11_shifted_numerator_signs",want,strict=True)
        out.append({"b":ib,"h":ih,"numerator":serialized(want)})
    audit.equal("U11_high_boundary_constant",(n+k)*(n+k-1)*(n+k-2)-k*(k-1)*(3*n+k-2),n*(n-1)*(n+3*k-2))
    audit.equal("U11_low_payment_constant",(n**2-3*n+4).sub(n=m+4),m**2+5*m+8)
    audit.equal("U11_low_payment_linear",(4*n**2-14*n+18).sub(n=m+4),4*m**2+18*m+26)
    return out


def formal_dependencies(audit):
    for N in range(3,10):
        U=uncapped_u(N)
        V=newton_v(N)
        audit.equal("complete_singleton_Newton_rising",V,rising_v(N),N)
        C=uncapped_u(N,W=h)-3*newton_v(N,W=h)-(N-2)*dd(2*N,x)+3*pair_low(N)
        surplus=sum((dd(j,h)*(aa(N,x)*aa(N-j,x)-3*dd(2*N-j,x)) for j in range(1,N)),P(0))-2*dd(N,h)*aa(N,x)+3*pair_low(N)
        audit.equal("U03_complete_surplus_identity",C-kn(N),surplus,N)
        g1=1+F(N-2,N+1)*x
        g2=1+F(3*N,2*(N+2))*x+F((N-1)*(N+4),2*(N+1)*(N+2))*x**2
        e=g2+(h+N-2)*g1/(N-1)-2*(h+N-2)*(h+N-1)/(N*(N-1))
        last=sum((dd(j,h)*(aa(N,x)*aa(N-j,x)-3*dd(2*N-j,x)) for j in (N-2,N-1)),P(0))-2*dd(N,h)*aa(N,x)
        audit.equal("U03_complete_last_two_terminal",last,dd(N-2,h)*aa(N,x)*e,N)
        P0=aa(N-3,h)*aa(N,b+h)
        Q=aa(2*N-3,h)
        eb=e.sub(x=b+h)
        Z=eb/(N-2)+F(3,2*(N-1)*(2*N-1))*(h-1)*(b+F(2*N-1,N)+F(N+1,2*N)*h)
        audit.equal("U03_joint_three_pair_identity",(last+3*pair_low(N)).sub(x=b+h),h*(P0-Q)*eb/(N-2)+h*Q*Z,N)
        audit.positive("U03_P_minus_Q",P0-Q)
        S=uncapped_u(N,W=h)-2*newton_v(N,W=h)-(N-1)*dd(2*N,x)+pair_low(N)
        if N==3:
            derivative=S.diff("h").sub(x=b+h)
            audit.positive("U11_n3_entire_low_derivative",derivative,strict=True)
            audit.check("U11_n3_derivative_population",len(derivative.t)==21)
            audit.reject("derivative_after_cone_substitution",S.sub(x=b+h).diff("h")!=derivative)
            audit.save("u11-n3-complete-low-derivative.json",serialized(derivative,["b","h"],5))
        q=aa(N-3,h)
        f=prod(1+h/i for i in range(N-2,N+1))
        P1=q*q*f
        share=4*aa(N,h)*(h*q).diff("h")-(h*P1).diff("h")
        audit.equal("U11_derivative_sharing_identity",share,q*q*(3*f-h*f.diff("h"))+2*h*q*q.diff("h")*f,N)
        audit.positive("U11_derivative_sharing_sign",share)
        audit.equal("U11_pair_value_wall",pair_high(N,Z=0),pair_low(N,H=x),N)
        audit.positive("U11_one_pair_high_derivative",(uncapped_u(N,W=x+z)-2*newton_v(N,W=x+z)-(N-1)*dd(2*N,x)+pair_high(N)).diff("z"))
    N=2
    S=uncapped_u(N,W=h)-2*newton_v(N,W=h)-(N-1)*dd(2*N,x)+pair_low(N)
    audit.equal("U11_n2_complete_low_identity",S,kn(N)+dd(4,x)-dd(4,x-h))
    audit.equal("U11_n2_fixed_derivative",S.diff("h").sub(x=b+h),b**3/6+3*b**2/4+11*b/12+F(1,4))
    audit.equal("U11_n2_high_plateau",uncapped_u(N,W=x+z)-2*newton_v(N,W=x+z)-(N-1)*dd(2*N,x)+pair_high(N),kn(N)+dd(4,x))


def u05_formal_dependencies(audit):
    expressions=u05_expressions()
    for N in range(3,10):
        an=aa(N,x)
        kernels={}
        for K in range(N+1):
            sk=an if K==0 else sum((dd(j,x)*dd(N+K-j,x) for j in range(K)),P(0))+dd(K,x)*an
            if K==0:
                d2=an
            elif K==1:
                d2=2*dd(N+1,x)-an
            else:
                d2=3*abinom(x+N+K-2,N+K)+(K-2)*abinom(x+N+K-3,N+K)
            uk=an*aa(K,2*x)-3*sk+3*d2
            kernels[K]=uk
            audit.equal("U05_full_signed_small_U_and_normalization",uk,an*normalized_u05(K).sub(n=N).polynomial(),(N,K))
            if K>=3:
                eu=expressions["U-E"].sub(n=N,k=K).polynomial()
                zu=expressions["U-Z"].sub(n=N,k=K).polynomial()
                pp=an*aa(K-3,x)
                qq=aa(N+K-3,x)
                right=sum((dd(j,x)*(an*aa(K-j,x)-3*dd(N+K-j,x)) for j in range(K-2)),P(0))+x*(pp-qq)*eu/(K-2)+x*qq*zu
                audit.equal("U05_complete_U_grouping",uk,right,(N,K))
                audit.positive("U05_complete_U_sign",uk)
        Cwall=uncapped_u(N,W=x)-3*newton_v(N,W=x)-(N-2)*dd(2*N,x)+3*pair_low(N,H=x)
        Cmid=uncapped_u(N,W=x+z)-3*newton_v(N,W=x+z)-(N-2)*dd(2*N,x)+3*pair_high(N)-triple_low_formula(N,G=z)
        anchored=sum((dd(l,z)*kernels[N-l] for l in range(1,N+1)),P(0))-triple_low_formula(N,G=z)
        audit.equal("U05_complete_middle_anchored_gain",Cmid-Cwall,anchored,N)
        if N==3:
            audit.equal("U05_n3_middle_exception",Cmid-Cwall,dd(6,x)-dd(6,x-z))
        else:
            em=expressions["MID-E"].sub(n=N).polynomial()
            zm=expressions["MID-N4-Z" if N==4 else "MID-Z"].sub(n=N).polynomial()
            term=sum((dd(l,z)*kernels[N-l] for l in range(N-2,N+1)),P(0))-triple_low_formula(N,G=z)
            pp=aa(N-3,z)*aa(N,b+z)
            qq=aa(2*N-5,z)
            ff=(1+b+z)*(1+(b+z)/4) if N==4 else aa(2,b+z)
            right=z*(pp-ff*qq)*em/(N-2)+z*qq*zm
            audit.equal("U05_entire_terminal_minus_triple",term.sub(x=b+z),right,N)
            audit.positive("U05_middle_factor_domination",pp-ff*qq)
        fullWs={}
        for K in range(3,N):
            d3=10*abinom(x+N+K-3,N+K)+5*(K-3)*abinom(x+N+K-4,N+K)+F((K-3)*(K-4),2)*abinom(x+N+K-5,N+K)
            # Independent first-row Newton moment retains the zero children.
            audit.equal("U05_all_D3_boundary_children",d3,an*normalized_d3_newton(K).sub(n=N).polynomial(),(N,K))
            wk=sum((dd(j,x)*kernels[K-j] for j in range(K+1)),P(0))-d3
            fullWs[K]=wk
            audit.positive("U05_full_upper_W_sign",wk)
            if K>=5:
                eh=expressions["HIGH-E"].sub(n=N,k=K).polynomial()
                zh=expressions["HIGH-Z"].sub(n=N,k=K).polynomial()
                pp=aa(K-3,x)*an
                qq=aa(N+K-5,x)
                right=sum((dd(j,x)*kernels[K-j] for j in range(K-2)),P(0))+x*(pp-aa(2,x)*qq)*eh/(K-2)+x*qq*zh
                audit.equal("U05_complete_upper_terminal_minus_D3",wk,right,(N,K))
        Chigh=uncapped_u(N,W=2*x+v)-3*newton_v(N,W=2*x+v)-(N-2)*dd(2*N,x)+3*pair_high(N,Z=x+v)-triple_high_newton(N)
        uppergain=sum((dd(l,v)*fullWs[N-l] for l in range(1,N-2)),P(0))
        audit.equal("U05_complete_upper_anchored_gain",Chigh-Cmid.sub(z=x),uppergain,N)
        audit.equal("U05_two_complete_chamber_values",Chigh.sub(v=0),Cmid.sub(z=x),N)
        if N==3:
            audit.equal("U05_n3_complete_upper_plateau",uppergain,0)
    # The 75 complete bounded three-triangle moments are auxiliary counts,
    # with first-row ranges imposed before any continuation.
    for N in range(4,9):
        for K in range(3,N):
            wk=aa(N,x)*normalized_w05(K).sub(n=N).polynomial()
            for X in range(5):
                direct=0
                for a1 in range(X+1):
                    for a2 in range(X-a1+1):
                        for a3 in range(X-a1-a2+1):
                            multiplier=count_a(N-3,X-a1-a2-a3)
                            direct+=multiplier*sum(count_a(K-3,3*X-b1-b2-b3)
                                for b1 in range(X-a1+1) for b2 in range(X-a2+1)
                                for b3 in range(X-a3+1))
                audit.equal("U05_75_complete_bounded_W_moments",wk.sub(x=X),direct,(N,K,X))


def low_reduction(audit):
    # All coefficients are symbolic in margins; the n panel audits identities,
    # while explicit all-index numerators/recurrences supply the index argument.
    audit.equal("U12_beta_minus_3_over_n_numerator",(2*n**2-4*n-3).sub(n=m+3),2*m**2+8*m+3)
    recurrence=lambda K:2*3**K-3*2**K-K+1
    audit.check("U12_recurrence_base",recurrence(1)==0)
    for K in range(1,15):
        audit.check("U12_recurrence_identity",recurrence(K+1)-2*recurrence(K)==2*3**K+K-2,K)
        audit.check("U12_recurrence_increment_sign",2*3**K+K-2>0,K)
    for N in range(3,16):
        U=uncapped_u(N)
        V=newton_v(N)
        D=U-V
        for j in range(1,N+1):
            uj=U.coeff(w=j)
            vj=V.coeff(w=j)
            audit.positive("U12_full_ratio",j*uj-N*vj,detail=(N,j))
            sigma=dd(N,w).coeff(w=j)
            ejm1=aa(N-1,w).coeff(w=j-1)
            audit.equal("U12_identical_terminal",sigma,ejm1/N,(N,j))
            total=sum((dd(l,w).coeff(w=j) for l in range(j,N)),P(0))
            ej=aa(N-1,w).coeff(w=j)
            audit.equal("U12_hockey_stick",total,ej,(N,j))
            if j<N:
                audit.positive("U12_slope_subset_bound",j*ej-F(N-j,N-1)*ejm1)
        audit.equal("U12_D_full_rising_identity",D,sum((dd(j,w)*(aa(N,x)*aa(N-j,x)-dd(2*N-j,x)) for j in range(N)),P(0)),N)
        Hhalf=U.sub(w=2*s)-(N+1)*V.sub(w=s)-kn(N)
        Bn=aa(N,2*s)-(N+1)*dd(N,s)
        Phi=aa(N,x+2*s)-aa(N,x+s)-aa(N,2*s)+aa(N,s)
        Rn=lambda K:aa(N,x)*aa(K,x)-aa(N,x)-(N+1)*dd(N+K,x)
        half_decomp=aa(N,x)*(Bn-1)+aa(N,x)*Phi+sum((dd(j,s)*Rn(N-j) for j in range(1,N)),P(0))
        audit.equal("U12_entire_half_endpoint_decomposition",Hhalf,half_decomp,N)
        audit.positive("U12_half_endpoint_sign",Hhalf)
        audit.positive("U12_Bn_bound",Bn-aa(N-1,s)*(1+F(N-1,N)*s))
        f=dd(N-1,w)
        fp=f.diff("w"); fpp=fp.diff("w")
        c=F(1,N-1)
        q0=2*sum((F(1,i) for i in range(1,N-1)),F(0))/(N-1)
        alpha=F(N+1,N); beta=F(2*N-1,N+1); delta=beta-F(1,N)
        Rlast=(alpha+beta*b+delta*w)*fpp-2*fp/N
        paid=alpha*(fpp-q0)+beta*b*fpp+(beta-F(3,N))*(fp-c)+delta*(w*fpp-fp+c)+(alpha*q0-2*c/N)
        audit.equal("U12_low_payment_exact_decomposition",Rlast,paid,N)
        audit.positive("U12_low_payment_sign",paid)
        retained=aa(N,x)*f*(alpha+beta*x-w/N)
        E=2*U-3*V
        prior=sum((dd(j,w)*(2*aa(N,x)*aa(N-j,x)-3*dd(2*N-j,x)) for j in range(N-1)),P(0))
        audit.equal("U12_complete_low_terminal",E,prior+retained,N)
        audit.positive("U12_complete_low_second_derivative",E.diff("w").diff("w").sub(x=b+w))
        M=2*U.diff("w").sub(w=2*s+h)-3*V.diff("w").sub(w=s+h)-(N-2)*V.diff("w").sub(w=s)
        Qabsent=U.sub(w=2*s+h)-3*V.sub(w=s+h)-(N-2)*V.sub(w=s)+3*pair_low(N)
        audit.equal("U12_complete_Q_s_no_triple",Qabsent.diff("s"),M,N)
        audit.positive("U12_full_M_s",M.diff("s"))
        reduction=M.sub(h=s+w)-M.sub(s=0,h=w)
        audit.positive("U12_full_translated_reduction",reduction)
        audit.equal("U12_low_initial_half_derivative",M.sub(s=0,h=0),Hhalf.diff("s").sub(s=0),N)
        audit.check("U12_degree_vanish",M.degree()<=2*N-1 and M.diff("s").degree()<=2*N-2,N)
        # Verify Q_s in both full triple chambers before any substitution.
        # h=x+s+g in low triple chamber, h=2x+s+v in high chamber.
        for name,T,arg,coordinate in (("middle",triple_low_formula(N),x+s+g,"g"),
                                     ("high",triple_high_newton(N),2*x+s+v,"v")):
            H=arg
            J=pair_high(N,Z=H-x)
            Q=U.sub(w=2*s+H)-3*V.sub(w=s+H)-(N-2)*V.sub(w=s)+3*J-T
            # Fixed h: derivative on chamber coordinates is d_s-d_g/d_v.
            fixed_derivative=Q.diff("s")-Q.diff(coordinate)
            Tg=T.diff(coordinate)
            audit.equal("U12_complete_Q_s_plus_triple",fixed_derivative,M.sub(h=H)+Tg,(N,name))
            audit.reject("triple_derivative_wrong_sign_%s_%d"%(name,N),fixed_derivative!=M.sub(h=H)-Tg)
        for K in range(1,N+1):
            audit.positive("U12_full_product_premise",Rn(K))


def middle_uniform(audit):
    delta=(2*n-2)*(2*n-3)*(2*n-4)
    c3=R.over(n-2,2*n-1)
    d3=R.over((n-2)*(n-1),4,n,2*n-1)
    B=R(aa(2,x))-c3*(x+1)*(g-3)+d3*(g-3)*(g-4)
    C=c3*(x+1)+7*d3-2*d3*g
    Bbar=4+3*x+5*x**2/8
    Cbar=F(11,8)+x/2
    # Independent arbitrary-index cleared-polynomial tests of every coarse
    # bound, with n=m+5, before the n>=7 final payment.
    for name,expr in (("B",B),("C",C),("Bbar_minus_B",R(Bbar)-B),
                      ("Cbar_minus_C",R(Cbar)-C)):
        positive_rational(audit,"ROOT_middle_"+name,expr.sub(x=b+g),{"n":m+5})
    alpha=R.over(n+1,n)
    beta=R.over(2*n-1,n+1)
    C0=R.over(alpha,n-2)-R.over(2,n,n-1)
    C1=R.over(beta-R.over(4,n),n-2)
    for name,expr in (("C0_minus_1n",C0-R.over(1,n)),("C1_minus_1n",C1-R.over(1,n)),
                      ("beta_minus_4n",beta-R.over(4,n))):
        positive_rational(audit,"ROOT_middle_"+name,expr,{"n":m+5})
    expectedZ=[delta-n*(24*n+F(11,4)),F(5,2)*delta-n*(18*n+1),
               2*delta-n*(F(15,4)*n+F(11,8)),(delta-n)/2]
    independentZ=(R(aa(2,x)*(1+x))-R.over(n*((6*n-9)*Bbar+(x**2+2)*Cbar),delta))*delta
    # The cubic Z in the proof is a smaller polynomial, leaving additional
    # nonnegative low-degree terms in the independently cleared cubic.
    displayed=sum((p*x**j for j,p in enumerate(expectedZ)),P(0))
    positive_rational(audit,"ROOT_middle_smaller_Z",independentZ-displayed,{"n":m+7})
    audit.equal("ROOT_middle_first_shift_literal",expectedZ[0].sub(n=m+7),8*m**3+108*m**2+F(1541,4)*m+F(499,4))
    outputs=[]
    for j,coeff in enumerate(expectedZ):
        shifted=coeff.sub(n=m+7)
        audit.positive("ROOT_middle_four_shifted_index_certificates",shifted,strict=True)
        outputs.append({"x_power":j,"shifted_numerator":serialized(shifted,["m"])})
    audit.check("ROOT_middle_final_x_degree",max(e[POS["x"]] for e in displayed.t)==3)
    audit.check("ROOT_middle_shifted_index_degree",all(
        coefficient.sub(n=m+7).support() <= {"m"} and
        coefficient.sub(n=m+7).degree() <= 3 for coefficient in expectedZ))
    for N in range(5,16):
        q=aa(2*N-5,g)
        Bn=B.sub(n=N).polynomial()
        Cn=C.sub(n=N).polynomial()
        T=triple_low_formula(N)
        dn=(2*N-2)*(2*N-3)*(2*N-4)
        audit.equal("ROOT_middle_entire_triple_factorization",T,g*(g-1)*(g-2)*q*Bn/dn,N)
        audit.equal("ROOT_middle_fixed_x_B_derivative",Bn.diff("g"),-Cn,N)
        adverse=-(6*g*q*Bn+3*g**2*q.diff("g")*Bn+(g**3+2*g)*q*Cn)/dn
        audit.positive("ROOT_middle_discarded_positive_terms",(T.diff("g")-adverse).sub(x=b+g))
        coarse=-x*q*((6*N-9)*Bbar+(x**2+2)*Cbar)/dn
        audit.positive("ROOT_middle_complete_coarse_bound",(adverse-coarse).sub(x=b+g))
        fn=dd(N-1,w)
        cn=F(1,N-1)
        audit.positive("ROOT_middle_fprime_lower_bound",fn.diff("w")-cn-w*aa(N-3,w)/(N-2))
        an=aa(N,x)
        E=2*uncapped_u(N)-3*newton_v(N)
        al=F(N+1,N); be=F(2*N-1,N+1)
        increment=E.diff("w")-E.diff("w").sub(w=0)
        bound=an*((al+(be-F(4,N))*x)*(fn.diff("w")-cn)-2*w*cn/N)
        audit.positive("ROOT_middle_complete_E_increment_bound",(increment-bound).sub(x=b+g,w=b+2*g))
        product_difference=an*aa(N-3,g)-aa(2,x)*q
        audit.positive("ROOT_middle_complete_factor_domination",product_difference.sub(x=b+g))
        audit.positive("ROOT_middle_paid_E_increment",(increment-x*aa(2,x)*q*(1+x)/N).sub(x=b+g,w=b+2*g))
        for order in range(1,N+1):
            lhs=aa(order,w).diff("w")-aa(order-1,w)
            rhs=sum((F(order-i,order*i)*prod(1+w/j for j in range(1,order) if j!=i)
                     for i in range(1,order)),P(0))
            audit.equal("ROOT_a_derivative_identity",lhs,rhs,(N,order))
    return outputs


def high_uniform(audit):
    b1=R(2)+R.over((n-2)*x,n+1)
    b2=R(2)+R.over(3*(3*n+4)*x,2,n+2)+R.over((5*n**2+9*n-8)*x**2,2,n+1,n+2)
    E=b2+R.over((x+k-2)*b1,k-1)-R.over((x+k-2)*(x+k-1),k,k-1)
    positive_rational(audit,"ROOT_high_E_coarse_bound",E-(2+4*x+2*x**2),{"n":m+r+6,"k":r+5})
    L=n+k
    BH=10*(x+L-4)*(x+L-3)+5*(k-3)*(x-3)*(x+L-4)+(k-3)*(k-4)*(x-3)*(x-4)/2
    den5=L*(L-1)*(L-2)*(L-3)*(L-4)
    audit.equal("ROOT_high_BH_quadratic_coefficient",BH.coeff(x=2),(k+1)*(k+2)/2)
    audit.equal("ROOT_high_BH_linear_coefficient",BH.coeff(x=1),(k+1)*(10*n+3*k-14)/2)
    for label,expr in (("BH",BH),("BH_coarse",16*L**2*(1+x)**2-BH),
                       ("three_BH_to_768",768*(1+x)**2*den5-3*BH*L**3),
                       ("L_to_k",L**3-8*k**3),("96_to_4",4*k**2-96)):
        audit.positive("ROOT_high_"+label,expr.sub(n=m+r+6,k=r+5))
    audit.equal("ROOT_high_final_coarse_payment",2*aa(2,x)*(1+x)**2-4*x*(1+x)**2,2+3*x+x**2+x**3+x**4)
    small=[]
    for K in range(5):
        B=R(2*aa(K,3*x))-3*normalized_s(K,2)+normalized_d3_newton(K)
        if K in (0,1):
            audit.check("ROOT_high_k01_exact_cancellations",B.equals_fraction(0),K)
            small.append({"k":K,"zero":True})
        else:
            denom=prod(n+i for i in range(1,K+1))
            cleared=(B*denom).polynomial()
            coefficients=[]
            for j in range(K+1):
                shifted=cleared.coeff(x=j).sub(n=m+K+1)
                audit.positive("ROOT_high_small_k_shifted_coefficients",shifted,strict=True,detail=(K,j))
                coefficients.append({"x_power":j,"shifted_numerator":serialized(shifted,["m"])})
            audit.check("ROOT_high_small_k_complete_degree",cleared.degree()<=2*K and
                        max((e[POS["x"]] for e in cleared.t),default=0)==K,K)
            if K==2:
                expected=R(3)+R.over(3*(2*n**2+4*n-1)*x,n+1,n+2)+R.over(3*(n**2+n-1)*x**2,n+1,n+2)
                audit.check("ROOT_high_k2_explicit_identity",(B-expected).equals_fraction(0))
            small.append({"k":K,"coefficients":coefficients})
    for N in range(6,16):
        for K in range(5,N):
            Bnorm=(R(2*aa(K,3*x))-3*normalized_s(K,2)+normalized_d3_newton(K)).sub(n=N).polynomial()
            A=lambda q:(R(2*aa(q,2*x))-3*normalized_s(q)).sub(n=N).polynomial()
            expand=sum((dd(j,x)*A(K-j) for j in range(K+1)),P(0))+normalized_d3_newton(K).sub(n=N).polynomial()
            audit.equal("ROOT_high_complete_second_expansion",Bnorm,expand,(N,K))
            en=E.sub(n=N,k=K).polynomial()
            p=aa(N,x)*aa(K-3,x)
            q=aa(N+K-5,x)
            f=aa(2,x)
            bn=BH.sub(n=N,k=K)
            d=(N+K)*(N+K-1)*(N+K-2)*(N+K-3)*(N+K-4)
            lhs=aa(N,x)*Bnorm-sum((dd(j,x)*aa(N,x)*A(K-j) for j in range(K-2)),P(0))
            rhs=x*(p-f*q)*en/(K-2)+x*q*(f*en/(K-2)+(x-1)*(x-2)*bn/d)
            audit.equal("ROOT_high_complete_terminal_plus_D3",lhs,rhs,(N,K))
            audit.positive("ROOT_high_full_kernel_sign",Bnorm)
            audit.positive("ROOT_high_complete_P_minus_fQ",p-f*q)
    return small


@lru_cache(maxsize=None)
def binomial_basis(name, order):
    return abinom(P.var(name),order)


def interpolate_triangular(degree, evaluator, names):
    """Tensor Newton finite differences on all i+j<=degree; exact integers."""
    values={(i,j):evaluator(i,j) for i in range(degree+1) for j in range(degree+1-i)}
    result=P(0)
    for i in range(degree+1):
        for j in range(degree+1-i):
            diff=sum((-1)**(i-a+j-c)*math.comb(i,a)*math.comb(j,c)*values[a,c]
                     for a in range(i+1) for c in range(j+1))
            if diff:
                result=result+diff*binomial_basis(names[0],i)*binomial_basis(names[1],j)
    return result, len(values)


def complete_initial_slopes(audit):
    arrays=[]
    finite_evaluations=0
    freezes=[]
    for N in range(3,16):
        degree=2*N
        tmid,pop1=interpolate_triangular(degree,lambda B,G:finite_triple(N,B+G,G),("b","g"))
        thigh,pop2=interpolate_triangular(degree,lambda X,V:finite_triple(N,X,X+V),("x","v"))
        finite_evaluations+=pop1+pop2
        # Derivative taken at FIXED x, before cone substitution. The finite
        # middle reconstruction uses b=x-g, hence d_g|x=d_g|b-d_b|g.
        dmid=tmid.diff("g")-tmid.diff("b")
        dhigh=thigh.diff("v")
        U=uncapped_u(N)
        V=newton_v(N)
        M0=2*U.diff("w")-3*V.diff("w")-(N-2)*V.diff("w").sub(w=0)
        middle=M0.sub(x=b+g,w=b+2*g)+dmid
        high=M0.sub(w=2*x+v)+dhigh
        items=[{"n":N,"cone":"middle","L":serialized(middle,["b","g"],2*N-1)},
               {"n":N,"cone":"high","L":serialized(high,["x","v"],2*N-1)}]
        freeze=audit.save("initial-slope-n%d-frozen.json"%N,{"n":N,"arrays":items,
            "finite_triple_samples":pop1+pop2,"degree_prior":degree,
            "T_middle":serialized(tmid,["b","g"],degree),
            "T_high":serialized(thigh,["x","v"],degree),
            "freeze_precedes_unused":True})
        freezes.append(freeze)
        arrays.extend(items)
        for name,poly,evaluator in (("middle",tmid,lambda B,G:finite_triple(N,B+G,G)),
                                    ("high",thigh,lambda X,V:finite_triple(N,X,X+V))):
            for point in ((degree+1,1),(1,degree+2),(degree+3,degree+4)):
                q1,q2=("b","g") if name=="middle" else ("x","v")
                value=poly.sub(**{q1:point[0],q2:point[1]})
                audit.equal("finite_triple_genuinely_unused",value,evaluator(*point),(N,name,point))
        audit.equal("complete_triple_middle_formula",tmid,triple_low_formula(N).sub(x=b+g),N)
        audit.equal("complete_triple_high_Newton",thigh,triple_high_newton(N),N)
        audit.equal("triple_zero_wall",tmid.sub(g=0),0,N)
        audit.equal("triple_complete_value_wall",tmid.sub(b=0,g=x),thigh.sub(v=0),N)
        jump=dhigh.sub(v=0)-dmid.sub(b=0,g=x)
        activation_jump=dmid.sub(g=0,b=x)
        beta_jump=sum((F(math.factorial(N-3+j)*math.factorial(5),math.factorial(N+3+j))*
                       math.comb(j+2,2)*aa(N-3-j,x) for j in range(N-2)),P(0))
        audit.equal("ROOT_full_beta_derivative_jump",jump,beta_jump,N)
        audit.positive("ROOT_beta_jump_sign",jump,strict=True)
        signed=sum(((-1)**l*math.comb(l+2,2)*abinom(x+N,N-3-l)*(1-u)**l
                    for l in range(N-2)),P(0))
        positive=sum((math.comb(j+2,2)*u**j*aa(N-3-j,x) for j in range(N-2)),P(0))
        audit.equal("ROOT_signed_beta_sum_identity",signed,positive,N)
        audit.equal("ROOT_L_jump_wall",high.sub(v=0)-middle.sub(b=0,g=x),jump,N)
        audit.equal("ROOT_L_activation_jump",middle.sub(g=0,b=x)-M0.sub(w=x),activation_jump,N)
        audit.save("derivative-walls-n%d.json"%N,{"n":N,
            "activation_jump":serialized(activation_jump,["x"]),
            "upper_bound_jump":serialized(jump,["x"]),
            "continuity_of_derivatives_assumed":False})
        audit.positive("complete_L_middle_sign",middle,detail=N)
        audit.positive("complete_L_high_sign",high,detail=N)
        audit.check("complete_L_degree_bounds",middle.degree()<=2*N-1 and high.degree()<=2*N-1,N)
        if N<=6:
            audit.check("ROOT_eight_fixed_bases",len(items)==2,N)
        # The complete high expansion includes k0/1 and the isolated constant.
        Bnorm={K:(R(2*aa(K,3*x))-3*normalized_s(K,2)+normalized_d3_newton(K)).sub(n=N).polynomial()
               for K in range(N)}
        expansion=sum((dd(l,v).diff("v")*aa(N,x)*Bnorm[N-l] for l in range(1,N+1)),P(0))-(N-2)*V.diff("w").sub(w=0)
        audit.equal("ROOT_full_high_L_expansion",high,expansion,N)
        audit.positive("ROOT_high_L_increment",high-high.sub(v=0))
        audit.reject("derivative_continuity_%d"%N,jump!=0)
        audit.reject("triple_omission_%d"%N,middle!=M0.sub(x=b+g,w=b+2*g))
        audit.reject("singleton_terminal_mutation_%d"%N,V!=rising_v(N,wrong_terminal=True))
        audit.reject("isolated_singleton_derivative_omission_%d"%N,high!=high+(N-2)*V.diff("w").sub(w=0))
    audit.check("complete_L_total_slots",sum(len(a["L"]["complete_triangular_slots"]) for a in arrays)==5174)
    audit.check("finite_triple_exact_sample_population",finite_evaluations==5668)
    audit.save("COMPLETE-INITIAL-SLOPES-n3-n15.json",{"arrays":arrays,"total_zero_preserving_slots":5174,
        "finite_triple_determining_evaluations":finite_evaluations,"finite_triple_unused_evaluations":78,
        "freezes":freezes,"original_LR_requests":0,"scope":"auxiliary exact polynomial reconstruction; finite index audit only"})
    return arrays


def bounded_controls(audit):
    # Direct finite singleton, pair and triple evaluations audit ranges/shifts.
    for N in range(3,9):
        singleton=newton_v(N)
        plow=pair_low(N)
        phigh=pair_high(N)
        tlow=triple_low_formula(N)
        thigh=triple_high_newton(N)
        for X in range(5):
            for W in range(7):
                direct=sum(count_a(N-1,X-r0)*count_a(N,W+r0-1) for r0 in range(X+1))
                audit.equal("bounded_singleton_full_Newton",singleton.sub(x=X,w=W),direct,(N,X,W))
            for H in range(10):
                formula=plow.sub(x=X,h=H) if H<=X else phigh.sub(x=X,z=H-X)
                audit.equal("bounded_pair_full_both_bands",formula,finite_pair(N,X,H),(N,X,H))
            for G in range(11):
                formula=tlow.sub(x=X,g=G) if G<=X else thigh.sub(x=X,v=G-X)
                audit.equal("bounded_triple_full_both_bands",formula,finite_triple(N,X,G),(N,X,G))
    audit.reject("pair_strict_shift",finite_pair(4,2,4)!=finite_pair(4,2,4,shift=1))
    audit.reject("triple_strict_shift",finite_triple(4,2,6)!=finite_triple(4,2,6,shift=2))
    low_continuation=triple_low_formula(4).sub(x=2,g=9)
    complete_triple=finite_triple(4,2,9)
    audit.equal("active_upper_tail_fixture_low",low_continuation,2277)
    audit.equal("active_upper_tail_fixture_complete",P(complete_triple),2226)
    audit.equal("active_upper_tail_fixture_correction",low_continuation-complete_triple,51)
    audit.reject("upper_triple_tail_omission",low_continuation!=complete_triple)
    negative_continuation=triple_high_newton(3).sub(x=2,v=-8)
    audit.equal("negative_height_fixture_value",negative_continuation,-708)
    audit.reject("negative_height_polynomial_continuation",negative_continuation!=0)
    # U03 low continuation and the U05 exceptional domination are real domains.
    false_factor=aa(1,z)*aa(4,z)-aa(2,z)*aa(3,z)
    audit.equal("n4_false_factor_fixture_leading",false_factor.coeff(z=5),F(-1,24))
    audit.reject("n4_false_middle_factor",any(c<0 for c in false_factor.t.values()))
    isolated_triple=triple_low_formula(4).sub(x=b+g)
    audit.equal("isolated_triple_fixture_negative",isolated_triple.coeff(b=0,g=3),F(-11,288))
    audit.reject("separately_signing_counting_triple",any(c<0 for c in isolated_triple.t.values()))
    audit.reject("U05_signed_U1_omission",normalized_u05(1).sub(n=4).polynomial()!=0)
    for K in (5,6):
        child2=5*(K-3)*normalized_binomial(K,4).sub(n=K+1).polynomial()
        child3=F((K-3)*(K-4),2)*normalized_binomial(K,5).sub(n=K+1).polynomial()
        audit.reject("D3_second_child_%d"%K,child2!=0)
        audit.reject("D3_third_child_%d"%K,child3!=0)
    # Literal physical-zero/degree records: no LR engine or source rewriting.
    columns=[2,0,2,5,2,0,5]
    positive=sum(e>0 for e in columns)
    actual_degree=2*positive-2
    audit.reject("physical_zero_degree_inflation",actual_degree!=2*len(columns)-2)
    audit.reject("physical_zero_label_deletion",len(columns)!=len([e for e in columns if e]))
    unsupported_gain=[F(0),F(-3,4),F(-15,8),F(-9,4),F(-9,8)]
    audit.reject("remove_N_ge4_from_paid_reserve",any(q<0 for q in unsupported_gain))
    for payload in ("__import__('os')", "x.__class__", "[x for x in []]", "n/2", "2**101"):
        try:
            read_math(payload)
        except (ValueError,SyntaxError):
            audit.reject("forbidden_data_syntax_"+payload,True)
        else:
            audit.reject("forbidden_data_syntax_"+payload,False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-root",type=Path,default=DEFAULT_SOURCE_ROOT)
    parser.add_argument("--output-root","--output",dest="output_root",type=Path,required=True)

    args=parser.parse_args()
    source_root=args.source_root.resolve(strict=True)
    if not source_root.is_dir():
        raise ValueError("source-root is not a directory")
    output_root=args.output_root.resolve()
    if output_root.exists():
        raise FileExistsError("output-root must be a fresh explicit directory")
    output_root.mkdir(parents=True,exist_ok=False)
    audit=Audit(output_root)
    sources={}
    pins=[]
    try:
        for name,(relative,want) in SOURCE_PINS.items():
            path=source_root/relative
            data=path.read_bytes()
            got=hashlib.sha256(data).hexdigest()
            allowed = (want,) if isinstance(want,str) else want
            audit.check("dependency_hash_authentication",got in allowed,name)
            sources[name]=data.decode("utf-8")
            observed_version = ROOT_PROOF_VERSIONS[got] if name == "ROOT_PROOF" else "exact-source"
            pins.append({"name":name,"path":relative,"sha256":got,"bytes":len(data),"observed_version":observed_version})
        audit.save("DEPENDENCY-READBACK.json",{"pins":pins,"provider_code_executed":False})
        audit.save("COEFFICIENT-CERTIFICATES.json",{
            "U03":u03_certificates(audit),
            "U05":u05_certificates(audit,sources["U05_SIGN"]),
            "U11":u11_certificates(audit),
            "ROOT_middle":middle_uniform(audit),
            "ROOT_high_small_k":high_uniform(audit)})
        formal_dependencies(audit)
        u05_formal_dependencies(audit)
        low_reduction(audit)
        complete_initial_slopes(audit)
        bounded_controls(audit)
        script=Path(__file__).read_bytes()
        receipt={"status":"PASS","verifier_version":"v4","checks":dict(audit.checks),"check_count":sum(audit.checks.values()),
                 "controls":dict(audit.controls),"control_count":sum(audit.controls.values()),
                 "elapsed_seconds":time.monotonic()-audit.start,"script_sha256":hashlib.sha256(script).hexdigest(),
                 "pins":pins,"original_LR_count_requests":0,"provider_code_executed":False,
                 "source_root":str(source_root),"output_root":str(output_root),
                 "finite_n_arrays_are_not_unbounded_proof":True,
                 "complete_original_adoption_authority":"root plus independent Astra gate"}
        audit.save("RECEIPT.json",receipt)
        print(json.dumps({k:receipt[k] for k in ("status","check_count","control_count","elapsed_seconds","script_sha256")},sort_keys=True))
    except Exception as exc:
        audit.save("FAILURE.json",{"status":"FAIL","exception":type(exc).__name__,"detail":str(exc),
            "checks_before_failure":dict(audit.checks),"controls_before_failure":dict(audit.controls),
            "elapsed_seconds":time.monotonic()-audit.start,"pins":pins})
        raise


if __name__=="__main__":
    main()
