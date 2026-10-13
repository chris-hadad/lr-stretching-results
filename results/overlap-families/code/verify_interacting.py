#!/usr/bin/env python3
"""Independent exact verifier for the Pro048 U05 interacting certificate.

This campaign-authored file reads inert, SHA-pinned JSON source. It imports no
returned program. --calibrate is bounded; --full is the scientific audit.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import comb, gcd, lcm
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path(__file__).resolve().parents[1]
PINS = ROOT/"SOURCE-MAP.json"
DEGREE = 9
DIM = 5
EXPECTED_BASE = (
    (0, 0, 0, 0, 1), (0, 1, 0, 0, -1), (1, -1, 0, 0, 0),
    (0, 0, 1, 0, -1), (0, 0, 0, 1, 0), (1, 0, 0, -1, 0),
)
EXPECTED_WALLS = (
    (0, 1, 0, -1, 0), (1, 0, 0, -1, -1), (0, 1, 0, -1, -1),
    (0, -1, 1, 0, 0), (-1, 0, 1, 0, 0), (-1, 0, 1, 1, 0),
    (0, -1, 1, 1, 0), (-1, -1, 1, 1, 0),
)
EXPECTED_PROOFS = {
    "U04/PROOFS/U04-01-COMPLETE-INTERACTING-CHARACTER.md",
    "U05/PROOFS/U05-01-ALL-RATIO-INTERACTING-POSITIVITY.md",
}
EXPECTED_MEMBERS = {
    "U05/DATA/WALL-FAN.json",
    "U05/DATA/DERIVATIVES.json",
    "U05/DATA/CORRECTED-DEGREE-SUPPORTS.json",
    "U05/DATA/SUPPORT-RESERVES.json",
    *(f"U05/DATA/CONE-{i:02d}.json" for i in range(30)),
}
ZERO = (0,) * DIM


class CheckFailure(Exception):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def eq(actual, expected, message: str) -> None:
    if actual != expected:
        raise CheckFailure(f"{message}: actual={actual!r}, expected={expected!r}")


def parse_q(value) -> Fraction:
    return Fraction(str(value))


def form(row, vector) -> int:
    return sum(a * b for a, b in zip(row, vector))


def primitive(values) -> tuple[int, ...]:
    scale = lcm(*(v.denominator for v in values))
    ints = [int(v * scale) for v in values]
    divisor = gcd(*ints)
    return tuple(v // divisor for v in ints)


def rank(rows) -> int:
    if not rows:
        return 0
    matrix = [[Fraction(x) for x in row] for row in rows]
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        factor = matrix[pivot_row][column]
        matrix[pivot_row] = [v / factor for v in matrix[pivot_row]]
        for r in range(pivot_row + 1, len(matrix)):
            factor = matrix[r][column]
            if factor:
                matrix[r] = [a - factor * b for a, b in
                             zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def null_line(rows, width: int) -> tuple[int, ...] | None:
    """Rational elimination, independent of signed-minor ray generation."""
    matrix = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    r = 0
    for column in range(width):
        pivot = next((i for i in range(r, len(matrix))
                      if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        factor = matrix[r][column]
        matrix[r] = [x / factor for x in matrix[r]]
        for i in range(len(matrix)):
            if i != r and matrix[i][column]:
                factor = matrix[i][column]
                matrix[i] = [a - factor * b for a, b in
                             zip(matrix[i], matrix[r])]
        pivots.append(column)
        r += 1
        if r == len(matrix):
            break
    if r != width - 1:
        return None
    free = next(i for i in range(width) if i not in pivots)
    vector = [Fraction(0) for _ in range(width)]
    vector[free] = Fraction(1)
    for pivot_row, pivot_col in enumerate(pivots):
        vector[pivot_col] = -matrix[pivot_row][free]
    return primitive(vector)


def inverse_and_det(columns) -> tuple[tuple[tuple[Fraction, ...], ...], int]:
    n = len(columns)
    matrix = [[Fraction(columns[j][i]) for j in range(n)] +
              [Fraction(i == j) for j in range(n)] for i in range(n)]
    determinant = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if matrix[i][c]), None)
        check(p is not None, "singular cone")
        if p != c:
            matrix[c], matrix[p] = matrix[p], matrix[c]
            determinant = -determinant
        pivot = matrix[c][c]
        determinant *= pivot
        matrix[c] = [v / pivot for v in matrix[c]]
        for r in range(n):
            if r != c and matrix[r][c]:
                factor = matrix[r][c]
                matrix[r] = [a - factor * b for a, b in
                             zip(matrix[r], matrix[c])]
    return tuple(tuple(row[n:]) for row in matrix), int(determinant)


def coordinates_in_basis(vector, basis) -> tuple[Fraction, ...]:
    """Solve a full-column-rank rectangular system exactly."""
    dimension = len(basis)
    augmented = [[Fraction(basis[j][i]) for j in range(dimension)] +
                 [Fraction(vector[i])] for i in range(DIM)]
    pivot_rows = []
    r = 0
    for c in range(dimension):
        p = next((i for i in range(r, DIM) if augmented[i][c]), None)
        check(p is not None, "dependent face basis")
        augmented[r], augmented[p] = augmented[p], augmented[r]
        factor = augmented[r][c]
        augmented[r] = [x / factor for x in augmented[r]]
        for i in range(DIM):
            if i != r and augmented[i][c]:
                factor = augmented[i][c]
                augmented[i] = [a - factor * b for a, b in
                                zip(augmented[i], augmented[r])]
        pivot_rows.append(r)
        r += 1
    check(all(not any(row[:dimension]) and row[dimension] == 0
              for row in augmented[dimension:]), "ray outside face span")
    return tuple(augmented[i][dimension] for i in pivot_rows)


def facets(ray_ids, rays):
    """All facets of a pointed cone by exact supporting hyperplanes."""
    ray_ids = tuple(sorted(ray_ids))
    d = rank([rays[i] for i in ray_ids])
    check(d >= 2, "facets requested for dimension below two")
    basis_ids = []
    for i in ray_ids:
        if rank([rays[j] for j in basis_ids] + [rays[i]]) > len(basis_ids):
            basis_ids.append(i)
    basis = [rays[i] for i in basis_ids]
    local = {i: coordinates_in_basis(rays[i], basis) for i in ray_ids}
    found = set()
    for selected in combinations(ray_ids, d - 1):
        normal = null_line([local[i] for i in selected], d)
        if normal is None:
            continue
        values = [form(normal, local[i]) for i in ray_ids]
        if not (all(v >= 0 for v in values) or all(v <= 0 for v in values)):
            continue
        face = tuple(i for i, v in zip(ray_ids, values) if v == 0)
        if rank([rays[i] for i in face]) == d - 1:
            found.add(face)
    return found


def pulling(ray_ids, rays):
    ray_ids = tuple(sorted(ray_ids))
    d = rank([rays[i] for i in ray_ids])
    if len(ray_ids) == d:
        return {ray_ids}
    anchor = ray_ids[0]
    output = set()
    for face in facets(ray_ids, rays):
        if anchor not in face:
            for simplex in pulling(face, rays):
                output.add(tuple(sorted((anchor, *simplex))))
    check(output, f"pulling failed for {ray_ids}")
    return output


def verify_fan(fan):
    base = tuple(tuple(row) for row in fan["base"])
    walls = tuple(tuple(row) for row in fan["walls"])
    eq(base, EXPECTED_BASE, "base forms from U05 Section 3")
    eq(walls, EXPECTED_WALLS, "eight walls from U05 Section 3")
    all_rows = base + walls
    eq(len(list(combinations(range(14), 4))), 1001, "four-row population")
    computed = set()
    for selected in combinations(all_rows, 4):
        candidate = null_line(selected, DIM)
        if candidate is None:
            continue
        values = [form(row, candidate) for row in base]
        if all(v >= 0 for v in values):
            computed.add(candidate)
        elif all(v <= 0 for v in values):
            computed.add(tuple(-x for x in candidate))
    rays = tuple(tuple(row) for row in fan["rays"])
    eq(len(computed), 16, "regenerated ray population")
    eq(set(rays), computed, "regenerated rays")
    eq(len(rays), 16, "certificate ray population")
    discovered = {}
    for signs in product((-1, 1), repeat=8):
        ray_ids = tuple(i for i, ray in enumerate(rays)
                        if all(sign * form(wall, ray) >= 0
                               for sign, wall in zip(signs, walls)))
        if rank([rays[i] for i in ray_ids]) == DIM:
            discovered[signs] = ray_ids
    eq(len(discovered), 27, "full-dimensional sign cells")
    eq(len(fan["cells"]), 27, "certificate cells")
    eq(len(fan["simplices"]), 30, "certificate simplices")
    certificate_cells = {}
    for index, cell in enumerate(fan["cells"]):
        signs = tuple(cell["signs"])
        check(signs not in certificate_cells, "duplicate cell sign")
        certificate_cells[signs] = index
        eq(set(cell["rays"]), set(discovered.get(signs, ())),
           f"cell {index} ray set")
        expected = pulling(discovered[signs], rays)
        reported = {tuple(sorted(s)) for s in cell["simplices"]}
        eq(reported, expected, f"cell {index} pulling triangulation")
    eq(set(certificate_cells), set(discovered), "all 256 signs exhausted")
    simplex_ids = []
    for index, simplex in enumerate(fan["simplices"]):
        cell = fan["cells"][simplex["cell"]]
        ids = tuple(simplex["ray_indices"])
        check(tuple(sorted(ids)) in
              {tuple(sorted(s)) for s in cell["simplices"]},
              f"simplex {index} missing from cell")
        cols = tuple(rays[i] for i in ids)
        eq(tuple(tuple(row) for row in simplex["rays"]), cols,
           f"simplex {index} rays")
        inverse, determinant = inverse_and_det(cols)
        eq(abs(determinant), 1, f"simplex {index} unimodularity")
        eq(int(simplex["determinant"]), determinant,
           f"simplex {index} determinant")
        reported_inverse = tuple(tuple(parse_q(v) for v in row)
                                 for row in simplex["inverse"])
        eq(reported_inverse, inverse, f"simplex {index} inverse")
        check(all(v.denominator == 1 for row in inverse for v in row),
              f"simplex {index} nonintegral inverse")
        simplex_ids.append(tuple(sorted(ids)))
    eq(set(simplex_ids),
       set().union(*(pulling(ids, rays) for ids in discovered.values())),
       "complete simplex roster")
    eq(len(set(simplex_ids)), 30, "duplicate simplices")
    return rays, tuple(tuple(s["ray_indices"]) for s in fan["simplices"])


def multiindices(n: int, degree: int):
    if n == 1:
        for k in range(degree + 1):
            yield (k,)
    else:
        for k in range(degree + 1):
            for tail in multiindices(n - 1, degree - k):
                yield (k, *tail)


NODES = tuple(multiindices(DIM, DEGREE))
DERIVATIVE_NODES = tuple(multiindices(DIM, DEGREE - 1))
eq(len(NODES), 2002, "degree-nine monomial count")
eq(len(DERIVATIVE_NODES), 1287, "degree-eight derivative count")


def band(X: int, Y: int, lo: int, hi: int, m: int = 5) -> int:
    """Literal full band, independent control for the A_j numerator route."""
    if X < 0 or Y < 0 or lo > hi:
        return 0
    total = 0
    for a in range(min(X, hi) + 1):
        for b in range(max(0, lo - a), min(Y, hi - a) + 1):
            total += comb(X - a + m - 1, m - 1) * \
                     comb(Y - b + m - 2, m - 2)
    return total


def numerator_A(j: int, X: int, Y: int, m: int = 5) -> int:
    """U05 Section 3 complete paired numerator, with once-only shifts."""
    if min(j, X, Y) < 0:
        return 0
    result = 0
    for i in range(max(0, j - Y), min(j - 1, X) + 1):
        result += comb(X - i + m - 1, m - 1) * \
                  comb(Y - j + i + m - 1, m - 1)
    if X >= j:
        result += comb(X - j + m, m) * comb(Y + m - 1, m - 1)
    return result


def both_counts(parameters, m: int = 5) -> tuple[int, int]:
    b, c, k, h, g = parameters
    first = numerator_A(g, b - h, c, m) - \
            numerator_A(k + 1, b - h, c, m)
    second = numerator_A(g, c - h - 1, b + 1, m) - \
             numerator_A(k + 1, c - h - 1, b + 1, m)
    return first, second


def whole(parameters) -> int:
    first, second = both_counts(parameters)
    return first - second


def whole_band(parameters, m: int = 5) -> int:
    b, c, k, h, g = parameters
    return band(b - h, c, g, k, m) - band(c - h - 1, b + 1, g, k, m)


def parameter_at(columns, coordinates):
    return tuple(sum(columns[j][i] * coordinates[j] for j in range(DIM))
                 for i in range(DIM))


def original(parameters):
    b, c, k, h, g = parameters
    widths = (b, b, k, b, b, b, b)
    overlaps = (h, g, 0, 0, 0, 0)
    outer = [0] * 7
    outer[-1] = widths[-1]
    for i in range(5, -1, -1):
        outer[i] = outer[i + 1] + widths[i] - overlaps[i]
    inner = [outer[i] - widths[i] for i in range(7)]
    content = (sum(widths) - b - c, b, c)
    return {"outer": outer, "inner": inner, "content": list(content)}


def legal(parameters):
    b, c, k, h, g = parameters
    return b >= c >= 0 and k >= 0 and 0 <= h <= b and \
           0 <= g <= min(c, k)


def verify_node(row, columns, held_out: bool, label: str):
    z = tuple(row["coordinates"])
    check(len(z) == DIM and all(isinstance(v, int) and v >= 0 for v in z),
          f"{label} coordinates")
    p = parameter_at(columns, z)
    eq(tuple(row["parameters"]), p, f"{label} parameters")
    check(legal(p), f"{label} illegal parameters")
    eq(row["original"], original(p), f"{label} literal original")
    first, second = both_counts(p)
    if not held_out:
        eq(row["first"], first, f"{label} first partner")
        eq(row["second"], second, f"{label} second partner")
    eq(row["count"], first - second, f"{label} whole count")
    return z, first - second


def newton_differences(values):
    """Tensor-product forward differences on the complete degree-nine simplex."""
    differences = dict(values)
    eq(set(differences), set(NODES), "complete determining simplex")
    for axis in range(DIM):
        lines = defaultdict(list)
        for alpha in NODES:
            lines[alpha[:axis] + alpha[axis + 1:]].append(alpha)
        for line in lines.values():
            line.sort(key=lambda alpha: alpha[axis])
            work = [differences[alpha] for alpha in line]
            transformed = []
            while work:
                transformed.append(work[0])
                work = [work[i + 1] - work[i] for i in range(len(work) - 1)]
            for alpha, value in zip(line, transformed):
                differences[alpha] = value
    return differences


@lru_cache(None)
def binomial_basis(k: int):
    """Exact ordinary coefficients of binom(z,k)."""
    poly = [Fraction(1)]
    for j in range(1, k + 1):
        next_poly = [Fraction(0)] * (len(poly) + 1)
        for degree, coefficient in enumerate(poly):
            next_poly[degree] -= coefficient * (j - 1) / j
            next_poly[degree + 1] += coefficient / j
        poly = next_poly
    return tuple((degree, value) for degree, value in enumerate(poly)
                 if value)


def ordinary_from_newton(differences):
    coefficients = defaultdict(Fraction)
    for alpha, multiplier in differences.items():
        if not multiplier:
            continue
        terms = [((), Fraction(multiplier))]
        for exponent in alpha:
            terms = [(powers + (power,), value * factor)
                     for powers, value in terms
                     for power, factor in binomial_basis(exponent)]
        for powers, value in terms:
            coefficients[powers] += value
    return {alpha: coefficients[alpha] for alpha in NODES}


def source_map(entries, key: str, value: str, population, label: str):
    result = {}
    for entry in entries:
        alpha = tuple(entry[key])
        check(alpha not in result, f"{label} duplicate {alpha}")
        result[alpha] = parse_q(entry[value])
    eq(set(result), set(population), f"{label} complete namespace")
    return result


def evaluate_newton(differences, coordinates):
    answer = 0
    choices = [tuple(comb(z, a) for a in range(min(z, DEGREE) + 1))
               for z in coordinates]
    for alpha, multiplier in differences.items():
        if multiplier and all(a < len(choices[i]) for i, a in enumerate(alpha)):
            term = multiplier
            for i, a in enumerate(alpha):
                term *= choices[i][a]
            answer += term
    return answer


def degree_case(p):
    b, c, k, h, g = p
    check(legal(p), f"degree case illegal parameter {p}")
    if b == 0:
        return 0
    if h == b:
        if g == c:
            return 0
        return 4 if k > g else 3
    if c == 0:
        return 5 if k > 0 else 4
    if b == c == g:
        return 4
    if k == 0:
        return 6 if b == c else 7
    if b == c:
        return 7 if k == g else 8
    return 8 if k == g else 9


def simplex_reserve_polynomial(degree):
    """Separate direct recurrence to avoid extrapolating from count values."""
    poly = [Fraction(1)]
    for j in range(1, degree + 1):
        next_poly = [Fraction(0)] * (len(poly) + 1)
        for i, coefficient in enumerate(poly):
            next_poly[i] += coefficient
            next_poly[i + 1] += coefficient / j
        poly = next_poly
    return tuple(poly)


def support_polynomial(coefficients, mask):
    result = [Fraction(0)] * (DEGREE + 1)
    for alpha, value in coefficients.items():
        if value and all(mask[i] or alpha[i] == 0 for i in range(DIM)):
            result[sum(alpha)] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def verify_supports(index, columns, coefficients, reserves, corrected):
    expected_masks = set(product((0, 1), repeat=DIM)) - {ZERO}
    data = {}
    for row in reserves:
        if row["cone"] == index:
            mask = tuple(row["support"])
            check(mask not in data, f"cone {index} duplicate reserve support")
            data[mask] = row
    eq(set(data), expected_masks, f"cone {index} reserve support coverage")
    corrected_data = {}
    for row in corrected:
        if row["cone"] == index:
            mask = tuple(row["support"])
            check(mask not in corrected_data,
                  f"cone {index} duplicate corrected support")
            corrected_data[mask] = row
    eq(set(corrected_data), expected_masks,
       f"cone {index} corrected support coverage")
    for mask in expected_masks:
        row = data[mask]
        correction = corrected_data[mask]
        p = parameter_at(columns, mask)
        eq(tuple(row["parameters"]), p,
           f"cone {index} support {mask} parameters")
        eq(tuple(correction["parameters"]), p,
           f"cone {index} corrected support {mask} parameters")
        ordinary = support_polynomial(coefficients, mask)
        degree = len(ordinary) - 1
        eq(degree, degree_case(p),
           f"cone {index} support {mask} actual-degree case")
        eq(row["degree"], degree, f"cone {index} support {mask} degree")
        eq(correction["actual_degree"], degree,
           f"cone {index} support {mask} corrected degree")
        eq(tuple(map(parse_q, row["coefficients"])), ordinary,
           f"cone {index} support {mask} complete polynomial")
        simplex = simplex_reserve_polynomial(degree)
        reserve = tuple(ordinary[j] - simplex[j]
                        for j in range(degree + 1))
        check(all(x >= 0 for x in reserve),
              f"cone {index} support {mask} negative reserve")
        check(ordinary[-1] > 0,
              f"cone {index} support {mask} vanishing top coefficient")
        eq(tuple(map(parse_q, row["simplex_reserve"])), reserve,
           f"cone {index} support {mask} reserve")
        eq(tuple(map(parse_q, correction["reserve"])), reserve,
           f"cone {index} support {mask} corrected reserve")


def derivative_coefficients(coefficients, inverse, physical_axis):
    result = defaultdict(Fraction)
    for alpha, value in coefficients.items():
        if not value:
            continue
        for i, exponent in enumerate(alpha):
            if exponent and inverse[i][physical_axis]:
                beta = list(alpha)
                beta[i] -= 1
                result[tuple(beta)] += value * exponent * \
                                       inverse[i][physical_axis]
    sign = -1 if physical_axis in (3, 4) else 1
    return {alpha: sign * result[alpha] for alpha in DERIVATIVE_NODES}


def verify_derivatives(index, columns, coefficients, source_row):
    eq(source_row["cone"], index, f"cone {index} derivative index")
    inverse, determinant = inverse_and_det(columns)
    eq(abs(determinant), 1, f"cone {index} derivative inverse")
    directions = source_row["directions"]
    eq([row["direction"] for row in directions],
       ["b", "c", "k", "-h", "-g"],
       f"cone {index} derivative directions")
    negative_c = 0
    for q, row in enumerate(directions):
        label = f"cone {index} derivative {row['direction']}"
        computed = derivative_coefficients(coefficients, inverse, q)
        reported = {}
        for powers, value in row["coefficients"]:
            alpha = tuple(powers)
            check(alpha in computed and alpha not in reported,
                  f"{label} sparse namespace")
            reported[alpha] = parse_q(value)
        check(all(value != 0 for value in reported.values()),
              f"{label} explicit zero in sparse map")
        eq(reported, {a: v for a, v in computed.items() if v},
           f"{label} all coefficient slots")
        signs = Counter("positive" if v > 0 else
                        "negative" if v < 0 else "zero"
                        for v in computed.values())
        for sign in ("positive", "negative", "zero"):
            eq(row[sign], signs[sign], f"{label} {sign} count")
        eq(parse_q(row["constant"]), computed[ZERO],
           f"{label} constant")
        if q == 1:
            negative_c += signs["negative"]
        elif q in (0, 2, 3, 4):
            eq(signs["negative"], 0, f"{label} sign theorem")
        if q == 0:
            check(computed[ZERO] >= Fraction(25, 12),
                  f"{label} b rate")
        if q == 3:
            check(computed[ZERO] >= Fraction(13, 12),
                  f"{label} -h rate")
        if q == 4:
            check(computed[ZERO] >= Fraction(77, 60),
                  f"{label} -g rate")
        if q == 2:
            p = parameter_at(columns, (1, 1, 1, 1, 1))
            b, c, k, h, _ = p
            star = min(b, b + c - h)
            if k >= star:
                check(all(v == 0 for v in computed.values()),
                      f"{label} saturated k derivative")
            else:
                check(computed[ZERO] >= Fraction(1, 9),
                      f"{label} unsaturated k rate")
    return negative_c


def verify_shared_faces(coefficient_maps, simplex_ids, rays):
    check(len(coefficient_maps) == 30, "all cone maps required for faces")
    checks = 0
    for i, j in combinations(range(30), 2):
        left, right = simplex_ids[i], simplex_ids[j]
        common = tuple(sorted(set(left) & set(right)))
        for alpha in multiindices(len(common), DEGREE) if common else [()]:
            left_key = [0] * DIM
            right_key = [0] * DIM
            for ray, exponent in zip(common, alpha):
                left_key[left.index(ray)] = exponent
                right_key[right.index(ray)] = exponent
            eq(coefficient_maps[i][tuple(left_key)],
               coefficient_maps[j][tuple(right_key)],
               f"shared face cones {i},{j} rays {common} power {alpha}")
        checks += 1
    eq(checks, 435, "pairwise common-face population")
    return checks


def read_regular_bytes(path: Path):
    check(path.is_relative_to(ROOT), f"path outside research root: {path}")
    check(stat.S_ISREG(path.lstat().st_mode),
          f"source is not a regular file: {path}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        parts = []
        remaining = before.st_size
        while remaining:
            part = os.read(descriptor, min(1 << 20, remaining))
            check(part, f"short source read: {path}")
            parts.append(part)
            remaining -= len(part)
        check(not os.read(descriptor, 1), f"source grew during read: {path}")
        content = b"".join(parts)
        after = os.fstat(descriptor)
        check(len(content) == before.st_size and
              (before.st_dev, before.st_ino, before.st_size) ==
              (after.st_dev, after.st_ino, after.st_size),
              f"source changed during read: {path}")
    finally:
        os.close(descriptor)
    return content


def read_regular_json(path: Path):
    content = read_regular_bytes(path)
    return json.loads(content), content


class PinnedData:
    def __init__(self):
        manifest,_=read_regular_json(PINS)
        self.rows={row['path']:row for row in manifest['files']}
        self.hashes_checked=0
        expected={'data/interacting/'+member.rsplit('/',1)[-1] for member in EXPECTED_MEMBERS}
        check(expected<=set(self.rows),'missing complete interacting certificate')
        for name in EXPECTED_PROOFS:
            self.read('proofs/pro048/'+name.rsplit('/',1)[-1])
    def read(self,name):
        row=self.rows[name];raw=read_regular_bytes(ROOT/name)
        eq(len(raw),row['bytes'],name+' bytes')
        eq(sha256(raw).hexdigest(),row['sha256'],name+' SHA-256')
        self.hashes_checked+=1
        return raw
    def load(self,member):
        check(member in EXPECTED_MEMBERS,'unselected certificate member')
        return json.loads(self.read('data/interacting/'+member.rsplit('/',1)[-1]))


def scalar_coefficients(parameters):
    """One-variable exact reconstruction under the source prior degree-nine bound."""
    values = [whole(tuple(t * v for v in parameters))
              for t in range(DEGREE + 1)]
    deltas = []
    while values:
        deltas.append(values[0])
        values = [values[i + 1] - values[i]
                  for i in range(len(values) - 1)]
    answer = [Fraction(0)] * (DEGREE + 1)
    for degree, delta in enumerate(deltas):
        for power, factor in binomial_basis(degree):
            answer[power] += delta * factor
    return tuple(answer)


def operation_controls():
    h_old = scalar_coefficients((3, 2, 1, 1, 0))
    h_new = scalar_coefficients((3, 2, 1, 0, 0))
    h_gain = tuple(a - b for a, b in zip(h_new, h_old))
    check(all(v >= 0 for v in h_gain), "whole -h gain control")
    eq(h_gain[1], Fraction(13, 12), "sharp -h linear rate")
    g_old = scalar_coefficients((3, 2, 1, 1, 1))
    g_new = scalar_coefficients((3, 2, 1, 1, 0))
    g_gain = tuple(a - b for a, b in zip(g_new, g_old))
    check(all(v >= 0 for v in g_gain), "whole -g gain control")
    eq(g_gain[1], Fraction(77, 60), "sharp -g linear rate")
    k_old = scalar_coefficients((2, 1, 1, 1, 1))
    k_new = scalar_coefficients((2, 1, 2, 1, 1))
    k_gain = tuple(a - b for a, b in zip(k_new, k_old))
    check(all(v >= 0 for v in k_gain), "whole k widening control")
    eq(k_gain[1], Fraction(1, 9), "sharp k linear rate")
    check(all(v > 0 for v in k_gain[2:]),
          "sharp k control higher gains")
    for t in range(4):
        eq(whole((3*t, 2*t, 3*t, t, 0)),
           whole((3*t, 2*t, 10*t, t, 0)),
           "whole k saturation control")
    c_gain = tuple(a - b for a, b in zip(
        scalar_coefficients((2, 2, 1, 0, 0)),
        scalar_coefficients((2, 1, 1, 0, 0))))
    eq(c_gain, tuple(map(Fraction, (
        0, "5/6", "137/36", "1043/144", "133/18", "2465/576",
        "191/144", "43/288", "-1/48", "-1/192"))),
       "complete signed c-gain failure control")


def local_controls():
    """Small, deliberately independent zero/tie/shift and fault controls."""
    cases = (
        (0, 0, 0, 0, 0), (0, 0, 3, 0, 0), (3, 2, 1, 1, 0),
        (3, 2, 1, 1, 1), (3, 2, 1, 3, 1),
        (4, 3, 2, 1, 1), (2, 2, 1, 0, 0),
        (2, 2, 2, 2, 2), (3, 0, 2, 1, 0),
    )
    for p in cases:
        check(legal(p), f"bad local control {p}")
        for t in (0, 1, 2, 3):
            scaled = tuple(t * v for v in p)
            eq(whole(scaled), whole_band(scaled),
               f"literal band versus full numerator at {p}, grade {t}")
    eq(whole((0, 0, 0, 0, 0)), 1, "zero/point count")
    eq(whole_band((6, 4, 2, 2, 0)), 5496,
       "no-absorber grade-two shift control")
    eq(whole_band((6, 4, 2, 6, 2)), 10,
       "triple-overlap grade-two control")
    b, c, k, h, g = 3, 2, 1, 1, 1
    erased_band = band(b - h, c, 0, k) - band(c - h - 1, b + 1, 0, k)
    eq(erased_band, 205, "erased overlap-band mutation")
    eq(whole_band((b, c, k, h, g)), 90,
       "retained overlap-band grade-one control")
    b, c, k, h, g, t = 3, 2, 1, 1, 0, 2
    correct = whole_band(tuple(t * v for v in (b, c, k, h, g)))
    stretched_offsets = band((b - h) * t, c * t, g * t, k * t) - \
        band((c - h - 1) * t, (b + 1) * t, g * t, k * t)
    check(stretched_offsets != correct,
          "stretched once-only endpoints failed to separate")


def expect_failure(operation, label):
    try:
        operation()
    except CheckFailure:
        return
    raise CheckFailure(f"fault injection went undetected: {label}")


def verify_cone(index, data, columns, include_holdouts=True):
    label = f"cone {index}"
    eq(data["schema"], "u05-full-cone-polynomial/v1", f"{label} schema")
    eq(data["cone"], index, f"{label} index")
    eq(data["prior_total_degree"], DEGREE, f"{label} prior degree")
    eq(tuple(tuple(r) for r in data["rays"]), columns, f"{label} ray order")
    eq(len(data["determining"]), 2002, f"{label} determining population")
    eq(len(data["holdouts"]), 2366, f"{label} holdout population")
    values = {}
    for row in data["determining"]:
        z, count = verify_node(row, columns, False, label + " determining")
        check(sum(z) <= DEGREE and z not in values,
              f"{label} determining namespace")
        values[z] = count
    eq(set(values), set(NODES), f"{label} determining simplex")
    differences = newton_differences(values)
    source_newton = source_map(data["newton"], "powers", "value",
                               NODES, label + " Newton")
    eq({a: parse_q(v) for a, v in differences.items()}, source_newton,
       f"{label} all Newton slots")
    coefficients = ordinary_from_newton(differences)
    source_coefficients = source_map(data["coefficients"], "powers", "value",
                                      NODES, label + " ordinary")
    eq(coefficients, source_coefficients,
       f"{label} all rational mixed slots")
    signs = Counter("positive" if v > 0 else "negative" if v < 0 else "zero"
                    for v in coefficients.values())
    for sign in ("positive", "negative", "zero"):
        eq(data["signs"][sign], signs[sign], f"{label} {sign} slots")
    eq(signs["negative"], 0, f"{label} coefficient positivity")
    if include_holdouts:
        shells = Counter()
        seen = set()
        for row in data["holdouts"]:
            z, count = verify_node(row, columns, True, label + " holdout")
            check(z not in seen, f"{label} duplicate holdout {z}")
            seen.add(z)
            shells[sum(z)] += 1
            eq(evaluate_newton(differences, z), count,
               f"{label} unused shell {z}")
        eq(shells, {10: 1001, 11: 1365},
           f"{label} both complete unused shells")
    return coefficients, signs


def calibrate(source):
    """Audit one high-density cone to price the full exact workflow."""
    started = time.perf_counter()
    local_controls()
    operation_controls()
    fan = source.load("U05/DATA/WALL-FAN.json")
    rays, simplex_ids = verify_fan(fan)
    index = 19
    data = source.load(f"U05/DATA/CONE-{index:02d}.json")
    columns = tuple(rays[i] for i in simplex_ids[index])
    first = time.perf_counter()
    coefficients, signs = verify_cone(index, data, columns)
    cone_seconds = time.perf_counter() - first
    reserves = source.load("U05/DATA/SUPPORT-RESERVES.json")
    corrected = source.load("U05/DATA/CORRECTED-DEGREE-SUPPORTS.json")
    derivatives = source.load("U05/DATA/DERIVATIVES.json")
    verify_supports(index, columns, coefficients,
                    reserves["supports"], corrected)
    verify_derivatives(index, columns, coefficients, derivatives[index])
    mutated = dict(data["determining"][0])
    mutated["count"] += 1
    expect_failure(
        lambda: verify_node(mutated, columns, False, "altered count"),
        "determining count")
    altered_unused = dict(data["holdouts"][0])
    altered_unused["count"] += 1
    expect_failure(
        lambda: verify_node(altered_unused, columns, True, "altered unused"),
        "unused-grade count")
    expect_failure(
        lambda: source_map(data["coefficients"][:-1], "powers", "value",
                           NODES, "omitted coefficient"),
        "coefficient namespace omission")
    altered_rows = list(data["coefficients"])
    altered_rows[0] = dict(altered_rows[0])
    altered_rows[0]["value"] = str(parse_q(altered_rows[0]["value"]) + 1)
    expect_failure(
        lambda: eq(
            source_map(altered_rows, "powers", "value", NODES,
                       "altered coefficient"),
            coefficients, "altered coefficient against reconstruction"),
        "rational mixed coefficient")
    check(len(simplex_ids) == 30, "calibration fan population")
    return {
        "mode": "calibrate",
        "status": "one-cone calibration only; no scientific acceptance",
        "cone": index,
        "source_hashes_checked": source.hashes_checked,
        "four_row_sets": 1001,
        "sign_vectors": 256,
        "rays": 16,
        "cells": 27,
        "simplices": 30,
        "mixed_slots_checked": 2002,
        "determining_occurrences_checked": 2002,
        "unused_occurrences_checked": 2366,
        "support_cases_checked": 31,
        "derivative_slots_checked": 6435,
        "one_cone_seconds": cone_seconds,
        "total_seconds": time.perf_counter() - started,
        "full_cones": 30,
        "other_full_phases": "29 other cones and 435 face restrictions unmeasured",
        "fault_injection": "altered determining and unused counts, omitted namespace, altered coefficient rejected",
    }

def full(source):
    started = time.perf_counter()
    local_controls()
    operation_controls()
    fan = source.load("U05/DATA/WALL-FAN.json")
    rays, simplex_ids = verify_fan(fan)
    corrected = source.load("U05/DATA/CORRECTED-DEGREE-SUPPORTS.json")
    reserves = source.load("U05/DATA/SUPPORT-RESERVES.json")
    derivatives = source.load("U05/DATA/DERIVATIVES.json")
    eq(len(corrected), 930, "corrected support population")
    eq(len(reserves["supports"]), 930, "reserve support population")
    eq(reserves["failed_reserves"], [], "source reported failed reserves")
    eq(len(derivatives), 30, "derivative cone population")
    source_derivatives = {row["cone"]: row for row in derivatives}
    eq(set(source_derivatives), set(range(30)),
       "derivative cone namespace")
    maps = []
    total_signs = Counter()
    negative_c = 0
    for index in range(30):
        cone_started = time.perf_counter()
        columns = tuple(rays[i] for i in simplex_ids[index])
        certificate = source.load(f"U05/DATA/CONE-{index:02d}.json")
        coefficients, signs = verify_cone(index, certificate, columns)
        maps.append(coefficients)
        total_signs.update(signs)
        verify_supports(index, columns, coefficients,
                        reserves["supports"], corrected)
        negative_c += verify_derivatives(
            index, columns, coefficients, source_derivatives[index])
        print(json.dumps({
            "phase": "cone-complete",
            "cone": index,
            "mixed_slots": 2002,
            "determining": 2002,
            "unused": 2366,
            "supports": 31,
            "derivative_slots": 6435,
            "seconds": time.perf_counter() - cone_started,
        }, sort_keys=True), flush=True)
    eq(total_signs["positive"], 24968, "global positive mixed slots")
    eq(total_signs["zero"], 35092, "global zero mixed slots")
    eq(total_signs["negative"], 0, "global negative mixed slots")
    eq(sum(total_signs.values()), 60060, "global mixed namespace")
    eq(negative_c, 2316, "global partial-c negative slots")
    face_checks = verify_shared_faces(maps, simplex_ids, rays)
    return {
        "mode": "full",
        "status": "exact certificate checks passed; mathematical adoption remains external",
        "source_hashes_checked": source.hashes_checked,
        "four_row_sets": 1001,
        "sign_vectors": 256,
        "rays": 16,
        "cells": 27,
        "simplices": 30,
        "mixed_slots": 60060,
        "mixed_positive": 24968,
        "mixed_zero": 35092,
        "mixed_negative": 0,
        "determining_occurrences": 60060,
        "unused_occurrences": 70980,
        "support_cases": 930,
        "derivative_slots": 193050,
        "negative_partial_c_slots": negative_c,
        "pairwise_face_restrictions": face_checks,
        "seconds": time.perf_counter() - started,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    phase = parser.add_mutually_exclusive_group(required=True)
    phase.add_argument("--calibrate", action="store_true")
    phase.add_argument("--full", action="store_true")
    arguments = parser.parse_args()
    try:
        source = PinnedData()
        result = calibrate(source) if arguments.calibrate else full(source)
    except (CheckFailure, KeyError, ValueError, OSError) as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}))
        raise SystemExit(1) from exc
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
