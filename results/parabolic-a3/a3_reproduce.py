#!/usr/bin/env python3
"""Reconstruct fixed A3 ray/pair polynomials and their sign certificates.

Python standard library only. No file writes, external executables, or data
outside the explicitly selected mathematical JSON file are used.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys

ROOTS = ((1, 0, 0), (0, 1, 0), (0, 0, 1),
         (1, 1, 0), (0, 1, 1), (1, 1, 1))
RAYS = ROOTS + ((1, 2, 1),)
CONES = ((0, 2, 5), (2, 4, 5), (0, 3, 5), (3, 1, 6),
         (4, 1, 6), (3, 5, 6), (4, 5, 6))
SUPPORTS = ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j * a[0][j] * determinant(
        [row[:j] + row[j+1:] for row in a[1:]]) for j in range(len(a)))


def columns(vectors):
    return [list(row) for row in zip(*vectors)]


def inverse(a):
    n = len(a)
    b = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        k = next(k for k in range(j, n) if b[k][j])
        b[j], b[k] = b[k], b[j]
        scale = b[j][j]
        b[j] = [x / scale for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x - scale*y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def verify_geometry():
    minors = 0
    for k in (1, 2, 3):
        for rows in combinations(range(3), k):
            for cols in combinations(range(6), k):
                minor = [[ROOTS[j][i] for j in cols] for i in rows]
                require(determinant(minor) in (-1, 0, 1), "Nonunimodular root minor")
                minors += 1
    bases = []
    for indices in combinations(range(6), 3):
        matrix = columns([ROOTS[i] for i in indices])
        if determinant(matrix):
            bases.append(inverse(matrix))
    require(len(bases) == 16, "Wrong nonsingular root-basis count")
    comparisons = 0
    for cone in CONES:
        generators = columns([RAYS[i] for i in cone])
        require(abs(determinant(generators)) == 1, "Nonunimodular fan cone")
        for basis_inverse in bases:
            coordinates = multiply(basis_inverse, generators)
            contained = all(x >= 0 for row in coordinates for x in row)
            excluded = any(all(x <= 0 for x in row) and any(x < 0 for x in row)
                           for row in coordinates)
            require(contained or excluded, "A root-basis boundary cuts a cone interior")
            comparisons += 1
    return minors, len(bases), comparisons


def inverse_support(m):
    """Canonical support solution, or None if this construction is inadmissible."""
    p, q, r, u, v, w = m
    x = max(0, u + v - p - q - r - 1)
    if w < max(u, v) or u + v < w + q or x > min(u - p, v - r):
        return None
    return (w-v, x, w-u, v-r-x, u+v-w-q, u-p-x, 1+p+q+r-u-v+x)


def reduced_fiber(m, direction):
    live = tuple(n if all(not root[i] or direction[i] > 0 for i in range(3)) else 0
                 for n, root in zip(m, ROOTS))
    degree = sum(live) - sum(x > 0 for x in direction)
    shift = tuple(sum(n*root[i] for n, root in zip(live, ROOTS)) for i in range(3))
    return degree, live, shift


class GroupedFlow:
    """Positive aggregate-flow sum with a cached three-group convolution."""
    def __init__(self, multiplicities):
        self.m = multiplicities
        self.weights = [[1] for _ in range(6)]
        self.inner = lru_cache(maxsize=None)(self._inner)
        self.count = lru_cache(maxsize=None)(self._count)

    def prepare(self, bound):
        for k, sequence in zip(self.m, self.weights):
            for z in range(len(sequence), bound + 1):
                sequence.append(0 if k == 0 else sequence[-1]*(z+k-1)//z)

    def _inner(self, z, y):
        q, r, v = self.weights[1], self.weights[2], self.weights[4]
        end = min(z, y) if self.m[4] else 0
        return sum(v[b]*r[z-b]*q[y-b] for b in range(end + 1))

    def _count(self, X, Y, Z):
        if min(X, Y, Z) < 0:
            return 0
        self.prepare(max(X, Y, Z))
        p, _, _, u, _, w = self.weights
        end_c = min(X, Y, Z) if self.m[5] else 0
        total = 0
        for c in range(end_c + 1):
            x, y, z = X-c, Y-c, Z-c
            end_a = min(x, y) if self.m[3] else 0
            total += w[c]*sum(u[a]*p[x-a]*self.inner(z, y-a) for a in range(end_a+1))
        return total


def ordinary_coefficients(values, first):
    """Expand Newton forward differences at consecutive integer sites over Q."""
    degree = len(values) - 1
    differences = list(values)
    coefficients = [Fraction(0)]*(degree+1)
    basis = [Fraction(1)]
    for k in range(degree+1):
        for j, b in enumerate(basis):
            coefficients[j] += differences[0]*b
        differences = [b-a for a, b in zip(differences, differences[1:])]
        if k < degree:
            next_basis = [Fraction(0)]*(len(basis)+1)
            for j, b in enumerate(basis):
                next_basis[j] -= Fraction(first+k, k+1)*b
                next_basis[j+1] += b/Fraction(k+1)
            basis = next_basis
    return coefficients


def evaluate(coefficients, t):
    value = Fraction(0)
    for coefficient in reversed(coefficients):
        value = value*t + coefficient
    return value


def component(coefficients, j):
    return coefficients[j] if j < len(coefficients) else Fraction(0)


def reproduce(data):
    require(tuple(map(tuple, data['roots'])) == ROOTS, "Root roster differs")
    require(tuple(map(tuple, data['rays'])) == RAYS, "Ray roster differs")
    require(tuple(map(tuple, data['cones'])) == CONES, "Cone roster differs")
    linear = data['linear_certificates']
    quadratic = data['quadratic_certificates']
    lm = [tuple(row['m']) for row in linear]
    qm = [tuple(row['m']) for row in quadratic]
    require(len(lm) == len(set(lm)) == 24, "Expected 24 distinct linear systems")
    require(len(qm) == len(set(qm)) == 16 and set(qm) <= set(lm),
            "Expected 16 distinct quadratic systems within the linear roster")
    for m in lm:
        require(len(m) == 6 and all(type(x) is int and x > 0 for x in m),
                "Multiplicities must be positive integers")
        counts = inverse_support(m)
        require(counts is not None and min(counts) >= 0, "Missing support realization")
        reconstructed = tuple(sum(n for n, s in zip(counts, SUPPORTS)
                                  if any(root[i] for i in s))-1 for root in ROOTS)
        require(reconstructed == m, "Support inverse does not reconstruct multiplicities")
    pairs = sorted({tuple(sorted(pair)) for cone in CONES for pair in combinations(cone, 2)})
    pair_directions = {tuple(a+b for a, b in zip(RAYS[i], RAYS[j])) for i, j in pairs}
    require(len(pairs) == len(pair_directions) == 13, "Expected 13 pair directions")
    expected = {(m, R) for m in lm for R in RAYS}
    expected |= {(m, R) for m in qm for R in pair_directions}
    records = {(tuple(row['m']), tuple(row['R'])): row for row in data['polynomials']}
    require(len(records) == len(data['polynomials']) == 376 and set(records) == expected,
            "Polynomial roster is incomplete or has duplicate/extra cases")
    minors, bases, comparisons = verify_geometry()
    computed = {}
    determining_count = holdout_count = 0
    for m in lm:
        counters = {}
        for key in sorted(key for key in records if key[0] == m):
            _, R = key
            record = records[key]
            degree, live, shift = reduced_fiber(m, R)
            require(record['degree'] == degree, "Saved degree disagrees with fiber dimension")
            if live not in counters:
                counters[live] = GroupedFlow(live)
            counter = counters[live]
            first = -(degree//2)
            values = []
            for t in range(first, first+degree+1):
                target = tuple(t*x for x in R) if t >= 0 else tuple(-t*x-b for x, b in zip(R, shift))
                value = counter.count(*target)
                values.append(-value if t < 0 and degree % 2 else value)
            coefficients = ordinary_coefficients(values, first)
            determining_count += len(values)
            require(coefficients == [Fraction(x) for x in record['coefficients']],
                    f"Coefficient mismatch: m={m}, R={R}")
            require(len(coefficients) == degree+1 and coefficients[-1] > 0 and coefficients[0] == 1,
                    "Recovered polynomial has wrong degree or constant")
            require(all(x > 0 for x in coefficients), "Nonpositive ordinary coefficient")
            require([point[0] for point in record['holdouts']] == [degree+1, degree+2],
                    "Wrong unused positive holdout sites")
            for t, saved in record['holdouts']:
                value = counter.count(*(t*x for x in R))
                require(value == saved == evaluate(coefficients, t),
                        f"Unused holdout mismatch: m={m}, R={R}, t={t}")
                holdout_count += 1
            computed[key] = coefficients
    for certificate in linear:
        m = tuple(certificate['m'])
        values = [component(computed[m, R], 1) for R in RAYS]
        require(values == [Fraction(x) for x in certificate['ray_values']], "Linear ray certificate mismatch")
        require(all(x >= 0 for x in values), "Negative linear ray value")
    quadratic_forms = 0
    for certificate in quadratic:
        m = tuple(certificate['m'])
        require(len(certificate['forms']) == 7, "Incomplete quadratic cone roster")
        for cone, form in zip(CONES, certificate['forms']):
            require(tuple(form['cone']) == cone, "Quadratic cone differs")
            diagonal = [component(computed[m, RAYS[i]], 2) for i in cone]
            mixed = []
            for i, j in combinations(range(3), 2):
                R = tuple(a+b for a, b in zip(RAYS[cone[i]], RAYS[cone[j]]))
                mixed.append(component(computed[m, R], 2) - diagonal[i] - diagonal[j])
            require(diagonal == [Fraction(x) for x in form['diagonal']] and
                    mixed == [Fraction(x) for x in form['mixed']], "Quadratic form mismatch")
            require(all(x >= 0 for x in diagonal+mixed), "Negative cone-coordinate quadratic coefficient")
            quadratic_forms += 1
    return {'root_minors_verified': minors, 'nonsingular_root_bases': bases,
            'cone_basis_comparisons': comparisons, 'complete_polynomials': len(computed),
            'independent_signed_determining_values': determining_count,
            'independent_unused_positive_holdouts': holdout_count,
            'linear_systems': len(linear), 'linear_ray_values': 7*len(linear),
            'quadratic_systems': len(quadratic), 'quadratic_forms': quadratic_forms,
            'quadratic_monomial_coefficients': 6*quadratic_forms,
            'ordinary_coefficients_positive_through_actual_degree': True}


if __name__ == '__main__':
    require(len(sys.argv) <= 2, "Usage: python3 a3_reproduce.py [a3-data.json]")
    filename = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).with_name('a3-data.json')
    print(json.dumps(reproduce(json.loads(filename.read_text())), indent=2, sort_keys=True))
