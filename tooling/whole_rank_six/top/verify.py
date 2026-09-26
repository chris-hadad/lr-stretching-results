#!/usr/bin/env python3
"""Exact independent direct-projection verification of rank-six q<=3 BV values.

Only Python's standard library is used. The lattice is the full image of the
original normal matrix. This is a finite premise; PROOF.md supplies its meaning.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from functools import lru_cache
from math import factorial, gcd, prod
from pathlib import Path
import argparse
import hashlib
import json
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def hive_normals():
    points = [(i, j) for i in range(7) for j in range(7-i)]
    locations = {p: k for k, p in enumerate(points)}
    interior = [p for p in points if min(p) > 0 and sum(p) < 6]
    directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    rows = set()
    for p in points:
        for u, v in combinations(directions, 2):
            if 2*u[0]*v[0]+u[0]*v[1]+u[1]*v[0]+2*u[1]*v[1] != 1:
                continue
            corners = [p, (p[0]+u[0], p[1]+u[1]),
                       (p[0]+v[0], p[1]+v[1]),
                       (p[0]+u[0]+v[0], p[1]+u[1]+v[1])]
            if not all(c in locations for c in corners):
                continue
            row = [0]*28
            for c, sign in zip(corners, [-1, 1, 1, -1]):
                row[locations[c]] += sign
            rows.add(tuple(row))
    normals = sorted({tuple(r[locations[p]] for p in interior) for r in rows})
    require(len(rows) == 45 and len(normals) == 42 and len(interior) == 10,
            'wrong original hive geometry')
    return normals


def determinant(a):
    n = len(a)
    if n == 0:
        return 1
    if n == 1:
        return a[0][0]
    if n == 2:
        return a[0][0]*a[1][1]-a[0][1]*a[1][0]
    require(n == 3, 'small-codimension contract')
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def image_index(rows):
    if not rows:
        return 1
    value = 0
    for cols in combinations(range(len(rows[0])), len(rows)):
        value = gcd(value, abs(determinant([[r[j] for j in cols] for r in rows])))
        if value == 1:
            break
    return value


def inverse(a):
    n = len(a)
    augmented = [[Q(x) for x in r]+[Q(i == j) for j in range(n)]
                 for i, r in enumerate(a)]
    for i in range(n):
        pivot = next((j for j in range(i, n) if augmented[j][i]), None)
        require(pivot is not None, 'singular metric')
        augmented[i], augmented[pivot] = augmented[pivot], augmented[i]
        scale = augmented[i][i]
        augmented[i] = [x/scale for x in augmented[i]]
        for j in range(n):
            if j != i:
                scale = augmented[j][i]
                augmented[j] = [x-scale*y for x, y in zip(augmented[j], augmented[i])]
    return [r[n:] for r in augmented]


def bernoulli(a, x):
    return [Q(1), x-Q(1, 2), x*x-x+Q(1, 6),
            x*x*x-Q(3, 2)*x*x+Q(1, 2)*x][a]


def scalar(rows):
    q = len(rows)
    index = image_index(rows)
    require(index > 0, 'dependent support')
    axes = [index // image_index(rows[:i]+rows[i+1:]) for i in range(q)]
    require(all(d > 0 for d in axes), 'invalid primitive axis')
    fundamental = [p for p in product(*(range(d) for d in axes))
                   if image_index([list(r)+[p[i]] for i, r in enumerate(rows)]) == index]
    require(len(fundamental)*index == prod(axes), 'incomplete image numerator')
    metric = inverse([[sum(x*y for x, y in zip(a, b)) for b in rows] for a in rows])

    @lru_cache(None)
    def projected(poles, exponents):
        if not poles:
            require(not any(exponents), 'unbalanced homogeneous degree')
            return Q(1)
        j = next(i for i, e in enumerate(exponents) if e)
        block = inverse([[metric[i][k] for k in poles] for i in poles])
        coefficients = [sum(block[a][b]*metric[k][j] for b, k in enumerate(poles))
                        for a in range(len(poles))]
        lowered = list(exponents)
        lowered[j] -= 1
        return sum((coefficients[a]*projected(poles[:a]+poles[a+1:], tuple(lowered))
                    for a in range(len(poles))), Q(0))

    answer = Q(0)
    for powers in product(range(q+1), repeat=q):
        if sum(powers) != q:
            continue
        weight = sum((prod(Q(axes[i]**a, factorial(a))*bernoulli(a, Q(p[i], axes[i]))
                           for i, a in enumerate(powers)) for p in fundamental), Q(0))
        poles = tuple(i for i, a in enumerate(powers) if a == 0)
        extra = tuple(max(a-1, 0) for a in powers)
        answer += weight*projected(poles, extra)
    return Q((-1)**q, prod(axes))*answer, index


def reference(path):
    records = {}
    for line in path.read_text().splitlines():
        fields = line.split()
        require(len(fields) == 3, 'malformed forward reference')
        key = tuple(map(int, fields[0].split(',')))
        require(key not in records, 'duplicate forward reference')
        records[key] = (Q(fields[1]), int(fields[2]))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'output must be fresh')
    started = time.monotonic()
    require(scalar([(1, 0), (1, 2)])[0] == Q(1, 5), 'index-two control')
    require(scalar([(1, 0), (0, 1)])[0] == Q(1, 4), 'orthant control')
    normals = hive_normals()
    expected = reference(args.reference)
    results = {}
    seen = set()
    for q in (1, 2, 3):
        minimum, minimizers, independent, dependent = None, [], 0, 0
        indices = {}
        for support in combinations(range(42), q):
            rows = [normals[i] for i in support]
            if not image_index(rows):
                dependent += 1
                require(support not in expected, 'dependent reference row')
                continue
            value, index = scalar(rows)
            require(expected.get(support) == (value, index), 'reference mismatch: '+str(support))
            require(value > 0, 'nonpositive local constant: '+str(support))
            seen.add(support)
            independent += 1
            indices[index] = indices.get(index, 0)+1
            if minimum is None or value < minimum:
                minimum, minimizers = value, [support]
            elif value == minimum:
                minimizers.append(support)
        results[q] = dict(independent=independent, dependent=dependent,
                          minimum=str(minimum), minimizers=minimizers, image_indices=indices)
        print(q, independent, dependent, minimum, flush=True)
    require(seen == set(expected), 'missing or extra forward rows')
    report = dict(schema='rank-six-small-codimension-v1', status='PASS_COMPLETE',
                  scope='all independent original normal subsets of size one through three',
                  results=results, seconds=time.monotonic()-started,
                  reference_sha256=hashlib.sha256(args.reference.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with args.output.open('x') as out:
        json.dump(report, out, indent=2, sort_keys=True)
        out.write('\n')


if __name__ == '__main__':
    main()
