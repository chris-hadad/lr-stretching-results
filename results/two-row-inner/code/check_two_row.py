#!/usr/bin/env python3
"""Fresh stdlib controls for the U07 adoption proof; no returned code imports.

All coefficient vectors below are exact Fraction values in the ordinary basis.
No finite roster is claimed to prove the uniform theorem.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations_with_replacement, permutations, product
import json
from math import factorial
from pathlib import Path
import os
import resource
import time


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p or [0])


def add(a, b, scale=1):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += scale*x
    return trim(c)


def mul(a, b):
    c = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return trim(c)


def coeff(p, i):
    return p[i] if 0 <= i < len(p) else 0


def evaluate(p, t):
    out = 0
    for x in reversed(p): out = out*t+x
    return out


def binomial_poly(q, a, d):
    out = (F(1, factorial(d)),)
    for j in range(d): out = mul(out, (a-j, q))
    return out


def subsets(w):
    for mask in range(1 << len(w)):
        yield sum(w[i] for i in range(len(w)) if mask >> i & 1), mask.bit_count()


def transfer_poly(w, b, c, k):
    d = len(w)
    out = (0,)
    for s, j in subsets(w):
        for cap, sign in [(0, 1), (b, -1), (c, -1), (b+c, 1)]:
            q = k-s-cap
            if q > 0:
                out = add(out, binomial_poly(q, d-1-j, d), sign*(-1)**j)
    return out


@lru_cache(None)
def kostka_poly(w, k):
    w = tuple(x for x in w if x)
    total = sum(w)
    if not 0 <= 2*k <= total or max(w, default=0) > total-k: return (0,)
    if len(w) <= 2: return (1,)
    d = len(w)-2
    out = (0,)
    for s, j in subsets(w):
        if j == 0 or s < k:
            assert j <= d
            out = add(out, binomial_poly(k-s, d-j, d), (-1)**j)
    return out


def interval_count(w, k, t):
    p = (1,)
    for v in w: p = mul(p, (1,)*(v*t+1))
    return coeff(p, k*t)-coeff(p, k*t-1)


def literal_cycles(p):
    seen = set()
    cycles = []
    for i in range(len(p)):
        if i in seen: continue
        c = []
        j = i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = p[j]
        cycles.append(tuple(c))
    return cycles


@lru_cache(None)
def eulerian(h):
    out = [0]*max(1, h)
    for p in permutations(range(h)):
        out[sum(a > b for a, b in zip(p, p[1:]))] += 1
    return tuple(out)


@lru_cache(None)
def cycles_wv(w, h):
    W, V = (0,), (0,)
    for p in permutations(range(len(w))):
        cycles = literal_cycles(p)
        caps = [sum(w[i] for i in cy) for cy in cycles]
        if len(cycles) == h:
            term = (1,)
            for cap in caps: term = mul(term, (1,)*cap)
            W = add(W, term)
        if len(cycles) == h+1:
            for i, cy in enumerate(cycles):
                term = (0,)*caps[i]+(len(cy),)
                for j, cap in enumerate(caps):
                    if j != i: term = mul(term, (1,)*cap)
                V = add(V, term)
    return W, V


def cycle_coefficient(w, b, c, k, h, omit_v=False):
    W, V = cycles_wv(tuple(w), h)
    p = mul((1,)*b, mul(eulerian(h), W if omit_v else add(W, V)))
    return F(coeff(p, k-1)-coeff(p, k-c-1), factorial(len(w)))


def majorization_path(y, k):
    y = tuple(sorted(y, reverse=True))
    total = sum(y)
    x = tuple(sorted((total-k, k)+(0,)*(max(2, len(y))-2), reverse=True))
    y = y+(0,)*(len(x)-len(y))
    path = [x]
    while x != y:
        i = next(i for i in range(len(x)) if x[i] != y[i])
        j = next(j for j in range(i+1, len(x)) if x[j] < y[j])
        assert x[i] >= x[j]+2
        z = list(x)
        z[i] -= 1
        z[j] += 1
        z = tuple(sorted(z, reverse=True))
        assert sum(abs(a-b) for a,b in zip(z,y)) <= sum(abs(a-b) for a,b in zip(x,y))-2
        assert all(sum(z[:j]) >= sum(y[:j]) for j in range(1,len(z)+1))
        assert max(z,default=0) <= total-k
        gain = add(kostka_poly(z,k), kostka_poly(x,k), -1)
        assert gain[0] == 0 and all(c >= 0 for c in gain)
        x = z
        path.append(x)
    return path


def invariant_count(u, t):
    states = {0: 1}
    for v in u:
        new = Counter()
        for old, count in states.items():
            for edge in range(abs(old-v*t), old+v*t+1, 2): new[edge] += count
        states = new
    return states.get(0, 0)


def reduction(lam, mu, A, B):
    n = max(len(lam),len(mu))
    lam = tuple(lam)+(0,)*(n-len(lam))
    mu = tuple(mu)+(0,)*(n-len(mu))
    if A < B or B < 0 or sum(lam)-sum(mu) != A+B or any(a < b for a,b in zip(lam,mu)):
        return None
    if any(lam[i+2] > mu[i] for i in range(n-2)): return None
    overlap = [0]+[max(lam[i+1]-mu[i],0) for i in range(n-1)]+[0]
    w = tuple(lam[i]-mu[i]-overlap[i]-overlap[i+1] for i in range(n))
    assert min(w,default=0) >= 0
    k = B-sum(overlap)
    W = sum(w)
    if k < 0 or 2*k > W or max(w,default=0) > W-k: return None
    return tuple(v for v in w if v), k


def lr_tableaux(lam, mu, A, B, t):
    """Direct full LR tableaux, original scaled cells, no character reduction."""
    n = max(len(lam),len(mu))
    lam = tuple(t*x for x in lam)+(0,)*(n-len(lam))
    mu = tuple(t*x for x in mu)+(0,)*(n-len(mu))
    if A < B or B < 0 or sum(lam)-sum(mu) != t*(A+B) or any(a < b for a,b in zip(lam,mu)):
        return 0
    cells = [(r,c) for r in range(n) for c in range(lam[r],mu[r],-1)]
    assigned = {}
    def walk(i, ones, twos):
        if i == len(cells): return int(ones == t*A and twos == t*B)
        r,c = cells[i]
        out = 0
        for val in (1,2):
            if (r,c+1) in assigned and val > assigned[r,c+1]: continue
            if (r-1,c) in assigned and val <= assigned[r-1,c]: continue
            a,b = ones+(val == 1), twos+(val == 2)
            if a > t*A or b > t*B or b > a: continue
            assigned[r,c] = val
            out += walk(i+1,a,b)
            del assigned[r,c]
        return out
    return walk(0,0,0)


def partition_box(width, height):
    return [tuple(reversed(x)) for x in combinations_with_replacement(range(width+1),height)]


def source_hashes(root):
    manifest=json.loads((root/'SOURCE-MAP.json').read_text())
    rows={}
    for item in manifest['files']:
        data=(root/item['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256'] and len(data)==item['bytes']
        rows[item['path']]={'sha256':item['sha256'],'bytes':item['bytes']}
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    begin = time.monotonic()
    checks = Counter()
    records = []
    # Full local transfer domain: all b,c and admitted k, not only central cases.
    weights = [w for d in range(1,5) for w in combinations_with_replacement(range(1,4),d)]
    weights += [(1,1,1,1,1),(1,2,3,4,5),(2,2,3,3,4)]
    for w in weights:
        C = sum(w)
        for b,c in product(range(1,4),repeat=2):
            for k in range(1,min(C,(C+b+c)//2)+1):
                p = transfer_poly(w,b,c,k)
                for h in range(len(w)+1):
                    assert coeff(p,h) == cycle_coefficient(w,b,c,k,h), (w,b,c,k,h,p)
                    checks['cycle_coefficient_slots'] += 1
                assert p[0] == 0 and all(x >= 0 for x in p)
                for t in (1,2,3):
                    expected = interval_count(w+(b,c),k,t)-interval_count(w+(b+c,0),k,t)
                    assert evaluate(p,t) == expected, (w,b,c,k,t)
                    checks['transfer_direct_grade_equalities'] += 1
                checks['transfer_vectors'] += 1
                if 2*k == C+b+c:
                    assert coeff(p,len(w)) == 0
                    assert all(cycle_coefficient(w,b,c,k,h,True) == 0 for h in range(1,len(w)+1))
                    checks['balanced_whole_W_cancellations'] += 1
    # Feasible, point, odd/zero and actual-degree cases, including all majorization steps.
    for n in range(0,8):
        for w in combinations_with_replacement(range(1,4),n):
            W = sum(w)
            for k in range(W//2+1):
                if max(w,default=0) > W-k: continue
                p = kostka_poly(w,k)
                u = tuple(x for x in w+(W-2*k,) if x)
                point = len(u) <= 3 or max(u,default=0) == W-k
                degree = 0 if point else len(u)-3
                assert len(p)-1 == degree and p[0] == 1 and all(x > 0 for x in p)
                path = majorization_path(w,k)
                checks['majorization_steps'] += len(path)-1
                for t in (1,2,3):
                    assert evaluate(p,t) == interval_count(w,k,t) == invariant_count(u,t)
                    checks['count_parity_equalities'] += 1
                checks['kostka_vectors'] += 1
                checks['point_vectors' if point else 'nonpoint_vectors'] += 1
    # A complete small original-shape domain, with invalid/empty cases retained.
    shapes = partition_box(3,4)
    for lam in shapes:
        for mu in shapes:
            if any(a < b for a,b in zip(lam,mu)): continue
            area = sum(lam)-sum(mu)
            if area > 7: continue
            for B in range(area//2+1):
                A = area-B
                reduced = reduction(lam,mu,A,B)
                for t in (1,2):
                    literal = lr_tableaux(lam,mu,A,B,t)
                    expected = 0 if reduced is None else interval_count(*reduced,t)
                    assert literal == expected, (lam,mu,A,B,t,reduced,literal,expected)
                    checks['original_LR_tableau_equalities'] += 1
                checks['original_triples'] += 1
                checks['empty_original_triples' if reduced is None else 'feasible_original_triples'] += 1
    # Larger-rank originals, central cancellation, parity changes and nonunit overlaps.
    for w,k in [((1,)*4,2),((1,)*6,3),((1,)*8,4),((1,2,3,3,4),5)]:
        lam = tuple(sum(w[i:]) for i in range(len(w)))
        mu = lam[1:]+(0,)
        A,B = sum(w)-k,k
        for t in (1,2,3):
            assert lr_tableaux(lam,mu,A,B,t) == evaluate(kostka_poly(w,k),t)
            checks['higher_rank_literal_original_counts'] += 1
        records.append({'weights':w,'k':k,'coefficients':[str(x) for x in kostka_poly(w,k)]})
    # Invalid containment/shape, three-high columns, determinant boundary, empty row.
    controls = [((1,1,1),(0,0,0),2,1), ((3,3),(0,0),3,3),
                ((3,3),(0,0),4,2), ((3,3,1),(2,1,0),3,1),
                ((0,0),(0,0),0,0), ((2,),(3,),0,0), ((2,),(0,),1,0)]
    for lam,mu,A,B in controls:
        reduced = reduction(lam,mu,A,B)
        for t in (1,2,3):
            expected = 0 if reduced is None else interval_count(*reduced,t)
            assert lr_tableaux(lam,mu,A,B,t) == expected
            checks['boundary_original_equalities'] += 1
    # Mutations are independently rejected, and adverse sectors remain adverse.
    central = transfer_poly((1,1),1,1,2)
    without_v = tuple(cycle_coefficient((1,1),1,1,2,h,True) for h in range(3))
    assert central == (0,1) and trim(without_v) == (0,)
    negative_sector = tuple(15*x for x in binomial_poly(1,2,4))
    assert coeff(negative_sector,1) == F(-5,4)
    six = kostka_poly((1,)*6,3)
    assert six == (1,2,F(3,2),F(1,2))
    # Replacing the once-only -1 by -t corrupts a physical grade.
    def wrong_shift(t):
        p = mul((1,)*(t+1),(1,)*(t+1))
        numerator = mul((1,)+(0,)*(t-1)+(-1,), (1,)+(0,)*(t-1)+(-1,))
        p = mul(p,numerator)
        return sum(coeff(p,j) for j in range(2*t-t+1))
    assert wrong_shift(2) != evaluate(central,2)
    checks['adverse_mutations_rejected'] = 2
    checks['negative_auxiliary_sector_retained'] = 1
    report = {'status':'PASS','scope':'Independent finite disconfirmation controls; uniform proof is PROOF.md',
              'checks':dict(checks),'sample_vectors':records,'source_hashes':source_hashes(args.source_root),
              'mutations':{'drop_distinguished_V':{'correct':['0','1'],'mutated':['0']},
                           'replace_minus_one_by_minus_t':{'t':2,'correct':str(evaluate(central,2)),'mutated':str(wrong_shift(2))},
                           'six_unit_last_sector_c1':'-5/4'},
              'resources':{'pid':os.getpid(),'workers':1,'sage_workers':0,'wall_seconds':time.monotonic()-begin,
                           'user_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime,
                           'system_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_stime,
                           'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
              'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'checks':report['checks'],'resources':report['resources']},sort_keys=True))


if __name__ == '__main__': main()
