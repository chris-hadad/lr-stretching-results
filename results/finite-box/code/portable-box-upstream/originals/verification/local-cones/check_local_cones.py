#!/usr/bin/env python3
"""Independent finite-lattice/Laurent checks for the frozen Pro025 P09 cones.

Standard library only. Returned programs are never imported or executed.
Scientific execution is reserved for the root's frozen, contained jobs.
See README.md for premises, supported domain, and the staged CLI.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import combinations, permutations
import json
from math import factorial, gcd, lcm, prod
import os
from pathlib import Path
import re
import sys
import time


SCHEMA = 1
TYPE_COUNT = 1217
ATLAS_COUNTS = {6: 743, 7: 3809}
METRIC_COUNTS = {6: 643, 7: 3294}
METRIC_COUNT = 3937
TRIPLE_COUNT = 3827947
EXPECTED_MINIMUM = Q(111599, 1643405760)
SCOPE = (
    "Exact finite cone/metric/kernel certificates conditional on the BV recursion, "
    "its quotient-lattice convention and the separately reviewed whole-hive chart. "
    "No independent box census, LR positivity adoption, or actual-edge incidence claim."
)


class Invalid(ValueError):
    pass


class Nongeneric(Invalid):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def integer(x):
    need(type(x) is int, "Expected integer, excluding bool")
    return x


def rational(x):
    need(type(x) is int or isinstance(x, str) and re.fullmatch(r"[+-]?\d+(?:/[1-9]\d*)?", x),
         "Expected exact rational string or integer")
    return Q(x)


def ivec(v, n=None):
    need(isinstance(v, (list, tuple)) and (n is None or len(v) == n), "Integer vector shape mismatch")
    return tuple(integer(x) for x in v)


def imat(a, m, n):
    need(isinstance(a, (list, tuple)) and len(a) == m, "Integer matrix height mismatch")
    return tuple(ivec(row, n) for row in a)


def dot(a, b):
    need(len(a) == len(b), "Dot product shape mismatch")
    return sum(x * y for x, y in zip(a, b))


def transpose(a):
    return tuple(zip(*a))


def multiply(a, b):
    return tuple(tuple(dot(row, col) for col in transpose(b)) for row in a)


def eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def det(a):
    n = len(a)
    need(all(len(row) == n for row in a), "Determinant requires a square matrix")
    if n == 0:
        return 1
    if n == 1:
        return a[0][0]
    if n == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return sum((-1) ** j * a[0][j] * det([row[:j] + row[j + 1:] for row in a[1:]]) for j in range(n))


def inverse(a):
    n = len(a)
    need(n and all(len(row) == n for row in a), "Inverse requires a nonempty square matrix")
    work = [[Q(x) for x in row] + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        need(pivot is not None, "Singular matrix")
        work[j], work[pivot] = work[pivot], work[j]
        divisor = work[j][j]
        work[j] = [x / divisor for x in work[j]]
        for i in range(n):
            if i != j and work[i][j]:
                multiplier = work[i][j]
                work[i] = [x - multiplier * y for x, y in zip(work[i], work[j])]
    return tuple(tuple(row[n:]) for row in work)


def exact_integers(a):
    need(all(Q(x).denominator == 1 for row in a for x in row), "Expected integral coordinates")
    return tuple(tuple(int(x) for x in row) for row in a)


def index(rows):
    k, n = len(rows), len(rows[0])
    return gcd(*(det(tuple(tuple(row[j] for j in cols) for row in rows)) for cols in combinations(range(n), k)))


def primitive(v):
    divisor = gcd(*v)
    need(divisor > 0, "Zero vector has no primitive direction")
    return tuple(x // divisor for x in v)


def normal_list(value, dimension=4):
    need(isinstance(value, list) and value, "Empty normal list")
    normals = tuple(ivec(v, dimension) for v in value)
    need(normals == tuple(sorted(set(normals))), "Normals must be distinct and lexicographically ordered")
    need(all(gcd(*v) == 1 for v in normals), "A normal is zero or nonprimitive")
    return normals


def primitive_row_reduction(v):
    """Euclidean column subtraction/exchange: v * P = (1,0,...,0)."""
    need(gcd(*v) == 1, "Primitive row required")
    n = len(v)
    values, p = list(v), [list(row) for row in eye(n)]
    for j in range(1, n):
        while values[j]:
            quotient = values[0] // values[j]
            for row in p:
                row[0] -= quotient * row[j]
                row[0], row[j] = row[j], row[0]
            values[0], values[j] = values[j], values[0] - quotient * values[j]
    if values[0] < 0:
        values[0] = -values[0]
        for row in p:
            row[0] = -row[0]
    p = tuple(map(tuple, p))
    need(tuple(dot(v, col) for col in transpose(p)) == (1,) + (0,) * (n - 1), "Integer reduction identity failed")
    need(abs(det(p)) == 1, "Integer reduction is not unimodular")
    return p


def kernel_basis(v):
    basis = transpose(primitive_row_reduction(v))[1:]
    need(index(basis) == 1 and all(dot(v, row) == 0 for row in basis), "Kernel basis is not saturated")
    return basis


def coordinates(rows, basis):
    dimension = len(basis)
    cols = next((cols for cols in combinations(range(len(basis[0])), dimension)
                 if det(tuple(tuple(row[j] for j in cols) for row in basis))), None)
    need(cols is not None, "Dependent lattice basis")
    square = tuple(tuple(row[j] for j in cols) for row in basis)
    restricted = tuple(tuple(row[j] for j in cols) for row in rows)
    result = exact_integers(multiply(restricted, inverse(square)))
    need(multiply(result, basis) == rows, "Integer basis does not represent the original rows")
    return result


def primitive_dual_rays(a):
    rays = []
    for column in transpose(inverse(a)):
        denominator = lcm(*(x.denominator for x in column))
        rays.append(primitive(tuple(int(x * denominator) for x in column)))
    rays = tuple(rays)
    scales = tuple(dot(a[i], rays[i]) for i in range(len(a)))
    need(all(k > 0 for k in scales), "Wrong primitive tangent-ray orientation")
    need(all(dot(a[i], rays[j]) == (scales[i] if i == j else 0)
             for i in range(len(a)) for j in range(len(a))), "Tangent rays are not dual to the normals")
    return rays, scales


def parallelepiped(rays):
    """Enumerate the entire finite quotient using unit-coordinate generators.

    The residues are R^-1 Z^d modulo Z^d. Closure under all standard lattice
    generators, together with the determinant index, certifies completeness.
    This uses no geometric bounding-box scan and no returned point roster.
    """
    dimension = len(rays)
    r = transpose(rays)
    volume = abs(det(r))
    need(type(volume) is int and 0 < volume <= 100000, "Parallelepiped index outside supported finite domain")
    generators = transpose(inverse(r))
    zero = (Q(0),) * dimension
    seen, queue = {zero}, deque([zero])
    while queue:
        residue = queue.popleft()
        for generator in generators:
            candidate = tuple((x + y) % 1 for x, y in zip(residue, generator))
            if candidate not in seen:
                seen.add(candidate)
                queue.append(candidate)
                need(len(seen) <= volume, "Finite quotient exceeds its determinant index")
    need(len(seen) == volume, "Incomplete parallelepiped residue group")
    points = exact_integers(tuple(tuple(dot(row, residue) for row in r) for residue in seen))
    need(len(set(points)) == volume, "Duplicated parallelepiped lattice point")
    return tuple(sorted(points))


def laurent_coefficient(rays, points, covector, power):
    """Expand the full numerator times z^d / product(1-exp(z*a_i))."""
    degree = len(rays) + power
    need(0 <= degree <= 3, "Laurent request exceeds the independently implemented degree-three expansion")
    denominator = [Q(1)] + [Q(0)] * degree
    for ray in rays:
        a = dot(covector, ray)
        if not a:
            raise Nongeneric("Covector vanishes on a generating ray")
        factor = [-Q(1) / a, Q(1, 2), -Q(a) / 12, Q(0)]
        denominator = [sum((denominator[j] * factor[k - j] for j in range(k + 1)), Q(0))
                       for k in range(degree + 1)]
    numerator = [sum((Q(dot(covector, point)) ** k for point in points), Q(0)) / factorial(k)
                 for k in range(degree + 1)]
    return sum((numerator[k] * denominator[degree - k] for k in range(degree + 1)), Q(0))


def metric_gram(rows, weights):
    need(len(weights) == 5 and all(x > 0 for x in weights[:4]) and weights[4] >= 0,
         "Metric must have four positive diagonal weights and nonnegative common weight")
    return tuple(tuple(sum(weights[k] * u[k] * v[k] for k in range(4)) +
                       weights[4] * sum(u) * sum(v) for v in rows) for u in rows)


def metric_dot(a, metric, b):
    return dot(a, tuple(dot(row, b) for row in metric))


def edge_quotient(ray, others):
    # If ray * P=e_0, then V=P^-T has primitive ray as its first column.
    p = primitive_row_reduction(ray)
    v = exact_integers(transpose(inverse(p)))
    need(transpose(v)[0] == ray, "Primitive-ray completion failed")
    inverse_v = transpose(p)
    projected = tuple(primitive(tuple(dot(row, other) for row in inverse_v[1:])) for other in others)
    return v, projected, parallelepiped(projected)


def cone_geometry(normals):
    need(len(normals) == 3 and all(len(row) == 4 and gcd(*row) == 1 for row in normals),
         "Expected three primitive normals in Z^4")
    normal_index = index(normals)
    need(normal_index > 0, "Dependent normal triple")
    annihilator = primitive(tuple((-1) ** j * det(tuple(tuple(row[k] for k in range(4) if k != j)
                                                        for row in normals)) for j in range(4)))
    basis = kernel_basis(annihilator)
    a = coordinates(normals, basis)
    rays, scales = primitive_dual_rays(a)
    need(abs(det(a)) == normal_index, "Normal-lattice index mismatch")
    for i in range(3):
        pair_index = index(tuple(normals[j] for j in range(3) if j != i))
        need(normal_index % pair_index == 0 and scales[i] == normal_index // pair_index,
             "Primitive tangent-ray scale/index identity failed")
    facets = {pair: index(tuple(rays[i] for i in pair)) for pair in combinations(range(3), 2)}
    need(all(normal_index * qij == scales[i] * scales[j] for (i, j), qij in facets.items()),
         "Primitive tangent facet index identity failed")
    return {"normal_index": normal_index, "basis": basis, "normal_coordinates": a,
            "rays": rays, "scales": scales, "points": parallelepiped(rays), "facet_indices": facets,
            "edges": [edge_quotient(rays[i], tuple(rays[j] for j in range(3) if j != i)) for i in range(3)]}


def cone_constant(geometry, metric, covector):
    rays, points = geometry["rays"], geometry["points"]
    s0 = laurent_coefficient(rays, points, covector, 0)
    edge_sum = Q(0)
    for i, (v, projected, quotient_points) in enumerate(geometry["edges"]):
        a = dot(covector, rays[i])
        if not a:
            raise Nongeneric("Covector vanishes on an edge")
        rotated = multiply(multiply(transpose(v), metric), v)
        xi_basis = tuple(dot(covector, col) for col in transpose(v))
        quotient_xi = tuple(xi_basis[j] - xi_basis[0] * rotated[0][j] / rotated[0][0] for j in (1, 2))
        # The first BV jet of this full 2-cone equals its first discrete jet:
        # the transverse ray's quadratic Bernoulli coefficient is zero.
        first_jet = laurent_coefficient(projected, quotient_points, quotient_xi, 1)
        expected_jet = -sum((dot(quotient_xi, ray) for ray in projected), Q(0)) / 24
        need(first_jet == expected_jet, "Indexed two-cone first-jet identity failed")
        edge_sum += -first_jet / a
    # Facet contributions need the zero quadratic ray coefficient; the full
    # cone integral is homogeneous of degree -3 and contributes no constant.
    value = s0 - edge_sum
    a = tuple(dot(covector, ray) for ray in rays)
    metricless_edges = sum((Q(a[j]) / (24 * geometry["facet_indices"][tuple(sorted((i, j)))] * a[i])
                            for i in range(3) for j in range(3) if i != j), Q(0))
    return value, s0 - metricless_edges


def generic_cone_values(geometry, metric):
    values = []
    for k in range(2, 201):
        xi = (1, k, k * k)
        try:
            value, constant = cone_constant(geometry, metric, xi)
        except Nongeneric:
            continue
        values.append((xi, value, constant))
        if len(values) == 2:
            break
    need(len(values) == 2, "No two generic covectors within the supported search window")
    need(values[0][1:] == values[1][1:], "Cone constant depends on the generic covector")
    return values


def bezout(v):
    result = transpose(primitive_row_reduction(v))[0]
    need(dot(v, result) == 1, "Bezout identity failed")
    return result


def dedekind(p, q):
    need(q > 0 and (q == 1 and p == 0 or 0 < p < q and gcd(p, q) == 1), "Invalid primitive residue/index")
    return sum(((Q(k, q) - Q(1, 2)) * (Q((p * k) % q, q) - Q(1, 2)) for k in range(1, q)), Q(0))


@lru_cache(maxsize=None)
def pair_tangent(u, v):
    """Indexed inward-normal pair weight by an independent full 2D Laurent calculation."""
    need(len(u) == len(v) and gcd(*u) == gcd(*v) == 1, "Pair normals must be primitive")
    q = index((u, v))
    if q == 0:
        return None
    p = dot(v, bezout(u)) % q
    a = ((1, 0), (p, q))
    rays, scales = primitive_dual_rays(a)
    need(scales == (q, q), "Two-dimensional primitive tangent-ray index mismatch")
    normal_gram = ((dot(u, u), dot(u, v)), (dot(v, u), dot(v, v)))
    ai = inverse(a)
    metric = inverse(multiply(multiply(ai, normal_gram), transpose(ai)))
    points = parallelepiped(rays)
    values = []
    for k in range(1, 30):
        xi = (1, k)
        args = tuple(dot(xi, ray) for ray in rays)
        if not all(args):
            continue
        s0 = laurent_coefficient(rays, points, xi, 0)
        edge_sum = sum((Q(args[j]) - metric_dot(rays[i], metric, rays[j]) * args[i] /
                        metric_dot(rays[i], metric, rays[i])) / (12 * q * args[i])
                       for i, j in ((0, 1), (1, 0)))
        values.append(s0 - edge_sum)
        if len(values) == 2:
            break
    need(len(values) == 2 and values[0] == values[1], "Indexed two-cone Laurent constants disagree")
    formula = Q(1, 4) + dedekind(p, q) - Q(dot(u, v), 12 * q) * (Q(1, dot(u, u)) + Q(1, dot(v, v)))
    need(values[0] == formula, "Indexed tangent two-cone formula fails independent Laurent expansion")
    return values[0]


@lru_cache(maxsize=None)
def signature(normals):
    # Row permutations leave the cone unchanged. Coordinate permutations and
    # coordinate sign changes are integral isometries; never flip single normals.
    forms = []
    for order in permutations(range(3)):
        columns = []
        for j in range(4):
            column = tuple(normals[i][j] for i in order)
            first = next((x for x in column if x), 0)
            columns.append(tuple(-x for x in column) if first > 0 else column)
        forms.append(tuple(sorted(columns)))
    return min(forms)


def metric_value(normals, weights, q, scales, constant):
    g = metric_gram(normals, weights)
    a, b, c = (g[i][i] for i in range(3))
    d, e, f = g[0][1], g[0][2], g[1][2]
    need(a > 0 and a * b - d * d > 0 and det(g) > 0, "Metric Gram matrix is not positive definite")
    return weighted_gram_value(a, b, c, d, e, f, q, tuple(scales), constant)


@lru_cache(maxsize=None)
def weighted_gram_value(a, b, c, d, e, f, q, scales, constant):
    diagonal = (b * c - f * f, a * c - e * e, a * b - d * d)
    off = (e * f - d * c, d * f - b * e, d * e - a * f)
    sums = (off[0] + off[1], off[0] + off[2], off[1] + off[2])
    need(min(diagonal) > 0, "Nonpositive inverse-Gram diagonal")
    value = constant + Q(q, 24) * sum((Q(sums[i], scales[i] ** 2 * diagonal[i]) for i in range(3)), Q(0))
    # Authenticate the producer's documented unreduced digest spelling as an
    # additional transport check; it is not the primary arithmetic route above.
    common = lcm(*(k * k for k in scales))
    numerator = 24 * constant.numerator * common * prod(diagonal)
    numerator += q * constant.denominator * sum(common // scales[i] ** 2 * sums[i] *
                                                prod(diagonal[j] for j in range(3) if j != i) for i in range(3))
    denominator = 24 * constant.denominator * common * prod(diagonal)
    need(Q(numerator, denominator) == value, "Historical digest normalization disagrees with independent rational weight")
    return value, numerator, denominator


def verify_type(primary, repaired, expected):
    normals = imat(expected["normals"], 3, 4)
    need(imat(primary["normals"], 3, 4) == normals == imat(repaired["normals"], 3, 4), "Misattached literal cone identity")
    need(integer(repaired["type_id"]) == expected["source_index"], "Repaired cone type index is not unique/attached")
    geometry = cone_geometry(normals)
    basis = imat(primary["quotient_dual_basis"], 3, 4)
    need(index(basis) == 1, "Returned normal-plane basis is not saturated")
    transform = coordinates(basis, geometry["basis"])
    need(abs(det(transform)) == 1, "Returned normal-plane chart is not integrally equivalent")
    a = coordinates(normals, basis)
    need(a == imat(primary["integer_normal_coordinates"], 3, 3), "Returned integer normal coordinates are wrong")
    stored_rays = tuple(tuple(dot(row, ray) for row in transform) for ray in geometry["rays"])
    need(stored_rays == imat(primary["primal_rays"], 3, 3), "Returned tangent rays are not the primitive dual rays")
    points = tuple(sorted(tuple(dot(row, point) for row in transform) for point in geometry["points"]))
    need(points == tuple(sorted(ivec(point, 3) for point in repaired["parallelepiped_points"])), "Returned complete parallelepiped point roster differs")
    need(len(points) == integer(repaired["parallelepiped_index"]), "Returned parallelepiped index mismatch")
    need(geometry["normal_index"] == integer(primary["normal_plane_index"]) == integer(repaired["q"]), "Returned normal index mismatch")
    need(geometry["scales"] == ivec(repaired["primitive_ray_scales"], 3), "Returned primitive ray scales differ")
    saved_metric = imat(primary["scaled_quotient_metric"], 3, 3)
    normal_basis_gram = multiply(basis, transpose(basis))
    true_metric = inverse(normal_basis_gram)
    scaled_metric = exact_integers(tuple(tuple(x * det(normal_basis_gram) for x in row) for row in true_metric))
    need(saved_metric == scaled_metric, "Returned scaled quotient metric is incorrect")
    facets = primary["facets"]
    need(len(facets) == 3 and [tuple(f["pair"]) for f in facets] == list(combinations(range(3), 2)), "Incomplete or repeated facet roster")
    for facet in facets:
        i, j = facet["pair"]
        r, s = stored_rays[i], stored_rays[j]
        q = index((r, s))
        p = dot(s, bezout(r)) % q
        need(integer(facet["q"]) == q and integer(facet["p"]) == p, "Returned primal facet residue/index mismatch")
        need(rational(facet["dedekind"]) == dedekind(p, q), "Returned finite facet sum mismatch")
        for field, left, right in (("a", r, r), ("b", s, s), ("c", r, s)):
            need(integer(facet[field]) == metric_dot(left, saved_metric, right), "Returned facet Gram entry mismatch")
    saved_covectors = repaired["two_covectors"]
    need(len(saved_covectors) == 2 and len({ivec(x, 3) for x in saved_covectors}) == 2 and
         all(dot(x, ray) != 0 for x in saved_covectors for ray in stored_rays), "Invalid returned generic covectors")
    expansions = []
    k0 = None
    for weights in ((1, 1, 1, 1, 0), (1, 2, 4, 8, 16)):
        metric = inverse(metric_gram(geometry["basis"], weights))
        values = generic_cone_values(geometry, metric)
        value, constant = values[0][1:]
        need(k0 is None or k0 == constant, "Metric-independent cone constant changes with the metric")
        k0 = constant
        predicted, _, _ = metric_value(normals, weights, geometry["normal_index"], geometry["scales"], constant)
        need(predicted == value, "Three-cone indexed metric formula disagrees with full BV recursion")
        if weights[-1] == 0:
            need(value == rational(primary["weight"]) == rational(repaired["standard_weight"]), "Returned standard cone weight mismatch")
        expansions.extend({"weights": weights, "covector": xi, "value": str(val)} for xi, val, _ in values)
    need(k0 == rational(repaired["metric_independent_K"]), "Returned metric-independent K mismatch")
    need(k0 == Q(1, 8) - sum((rational(f["dedekind"]) / 2 for f in facets), Q(0)), "Three-cone finite-sum constant fails independent Laurent reconstruction")
    return {"id": expected["id"], "source_index": expected["source_index"], "normals": normals,
            "q": geometry["normal_index"], "primitive_ray_scales": geometry["scales"],
            "metric_independent_K": str(k0), "standard_weight": str(expansions[0]["value"]),
            "saturated_normal_basis": geometry["basis"], "primitive_tangent_rays": geometry["rays"],
            "complete_parallelepiped_points": geometry["points"], "expansions": expansions}


def hidden_cubic(normals, certificate):
    needed = {v for v in normals if tuple(-x for x in v) in normals and v < tuple(-x for x in v)}
    need(certificate["passed"] is True, "Returned hidden-cubic gate is not passed")
    clauses = certificate["clauses"]
    directions = [ivec(clause["flat_normal"], 4) for clause in clauses]
    need(len(directions) == len(set(directions)) and set(directions) == needed, "Missing, duplicate, or extra hidden-cubic direction")
    checked = []
    for direction, clause in zip(directions, clauses):
        basis = imat(clause["kernel_basis"], 3, 4)
        need(all(dot(direction, row) == 0 for row in basis), "Hidden-cubic basis leaves the stated kernel")
        need(index(basis) == 1, "Hidden-cubic kernel basis is rank deficient or nonsaturated")
        restricted = set()
        for normal in normals:
            projected = tuple(dot(normal, row) for row in basis)
            if any(projected):
                restricted.add(primitive(projected))
        restricted = tuple(sorted(restricted))
        need(restricted, "Empty restricted normal list")
        proof = {"flat_normal": direction, "saturated_kernel_basis": basis,
                 "complete_restricted_normals": restricted, "criterion": clause["criterion"]}
        if clause["criterion"] == "P07 norm-six theorem":
            maximum = max(dot(v, v) for v in restricted)
            need(maximum == integer(clause["max_squared_norm"]) <= 6, "Hidden-cubic norm-six bound is false")
            proof["max_squared_norm"] = maximum
        else:
            need(clause["criterion"] == "all rank-two pair weights", "Unknown hidden-cubic criterion")
            pairs = []
            for i, j in combinations(range(len(restricted)), 2):
                value = pair_tangent(restricted[i], restricted[j])
                if value is not None:
                    need(value >= 0, "A complete restricted pair has a negative tangent weight")
                    pairs.append([i, j, str(value)])
            need(pairs and len(pairs) == integer(clause["pair_count"]), "Restricted independent-pair roster count mismatch")
            minimum = min(Q(row[2]) for row in pairs)
            need(minimum == rational(clause["minimum"]), "Restricted complete pair minimum mismatch")
            proof.update(independent_pairs=pairs, minimum=str(minimum))
        checked.append(proof)
    return checked


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, f"Duplicate JSON object key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise Invalid(f"Invalid JSON number: {value}")


def decode(data):
    return json.loads(data, object_pairs_hook=no_duplicate_keys, parse_constant=reject_constant)


def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_bound(entry):
    need(isinstance(entry["path"], str) and Path(entry["path"]).is_absolute(), "Bound input path is not absolute")
    data = Path(entry["path"]).read_bytes()
    need(hashlib.sha256(data).hexdigest() == entry["sha256"], "Bound input SHA256 mismatch: " + entry["path"])
    need(len(data) == integer(entry["bytes"]), "Bound input byte count mismatch")
    return decode(data)


def atlas_id(rank, number):
    return f"R{rank}-A{number:04d}"


def load_inputs(roster):
    need(roster["schema_version"] == SCHEMA and roster["status"] == "proposed_for_root_verification", "Unsupported verification roster")
    inputs = roster["inputs"]
    required = {"atlas6", "atlas7", "primary_types", "repaired_types", "metric0", "metric1500", "metric3000", "reconciliation"}
    need(set(inputs) == required, "Input roster is not the exact declared dependency set")
    paths = [str(Path(entry["path"]).resolve()) for entry in inputs.values()]
    need(len(paths) == len(set(paths)), "Duplicate or aliased input dependency")
    documents = {name: read_bound(entry) for name, entry in inputs.items()}
    atlases = {}
    for rank in (6, 7):
        doc = documents[f"atlas{rank}"]
        need(integer(doc["n"]) == rank, "Misattached rank atlas")
        rows = doc["normal_atlases"]
        need(len(rows) == ATLAS_COUNTS[rank] and [integer(row["id"]) for row in rows] == list(range(len(rows))), "Incomplete or reordered complete normal-atlas identities")
        lists = set()
        for row in rows:
            normals = normal_list(row["normals"])
            need(normals not in lists, "Duplicate normal-list identity within rank")
            lists.add(normals)
            atlases[atlas_id(rank, row["id"])] = row
    records = []
    for name, begin, end in (("metric0", 0, 1500), ("metric1500", 1500, 3000), ("metric3000", 3000, METRIC_COUNT)):
        doc = documents[name]
        need((doc["begin"], doc["end"], doc["total_proposals"]) == (begin, end, METRIC_COUNT), "Metric shard boundary mismatch")
        need(len(doc["records"]) == end - begin, "Incomplete metric input shard")
        records.extend(doc["records"])
    expected = roster["expected_metric_atlases"]
    need(len(expected) == len(records) == METRIC_COUNT, "Incomplete expected metric identities")
    ids = [entry["id"] for entry in expected]
    need(len(set(ids)) == len(ids), "Duplicate expected metric identity")
    observed = []
    for position, (record, wanted) in enumerate(zip(records, expected)):
        key = atlas_id(integer(record["rank"]), integer(record["atlas_id"]))
        need(key == wanted["id"] and wanted["source_index"] == position, "Misattached metric identity or source index")
        need(key in atlases, "Metric certificate names an unknown normal list")
        normal_list(record["normals"])
        need(record["normals"] == wanted["normals"] == atlases[key]["normals"], "Metric/list literal normals mismatch")
        need(record["masks"] == wanted["masks"] == atlases[key]["masks"], "Metric/list masks mismatch")
        need(record["dual_extended_diagonal"] == wanted["weights"], "Metric weights differ from the frozen identity roster")
        observed.append(key)
    need(dict(Counter(record["rank"] for record in records)) == METRIC_COUNTS, "Metric atlas rank population mismatch")
    need(observed == ids, "Metric expected identities are not exactly attached")
    types = roster["expected_types"]
    need(len(types) == TYPE_COUNT and len({row["id"] for row in types}) == TYPE_COUNT, "Incomplete or duplicated expected type identity roster")
    need(len(documents["primary_types"]["types"]) == len(documents["repaired_types"]["types"]) == TYPE_COUNT, "Incomplete returned type rosters")
    for i, wanted in enumerate(types):
        need(wanted["id"] == f"T{i:04d}" and wanted["source_index"] == i, "Invalid expected type index")
        need(wanted["normals"] == documents["primary_types"]["types"][i]["normals"] == documents["repaired_types"]["types"][i]["normals"], "Type literal identity mismatch across inputs")
    return documents, atlases, records


def verify_types(roster, documents, atlases, result, persist):
    raw, raw_pairs = set(), set()
    for atlas in atlases.values():
        normals = tuple(map(tuple, atlas["normals"]))
        need(max(dot(v, v) for v in normals) <= 6, "An input normal list violates the short-normal premise")
        raw.update(combinations(normals, 3))
        raw_pairs.update(combinations(normals, 2))
    actual_signatures = {signature(triple) for triple in raw if index(triple)}
    expected_signatures = [signature(imat(row["normals"], 3, 4)) for row in roster["expected_types"]]
    need(len(set(expected_signatures)) == TYPE_COUNT and set(expected_signatures) == actual_signatures,
         "Canonical independent type identities do not exactly equal all complete-list triples")
    result["complete_normal_atlas_ids"] = list(atlases)
    result["raw_distinct_triples"] = len(raw)
    result["expected_ids"] = [row["id"] for row in roster["expected_types"]]
    # Reconstruct the indexed two-dimensional formula over the entire distinct
    # pair roster of the complete supplied lists, in addition to hidden kernels.
    independent_pairs = [pair for pair in sorted(raw_pairs) if index(pair)]
    result["expected_pair_ids"] = [f"P{i:05d}" for i in range(len(independent_pairs))]
    result["completed_pair_ids"] = []
    result["pairs"] = []
    for pair_id, (u, v) in zip(result["expected_pair_ids"], independent_pairs):
        result["active_id"] = pair_id
        value = pair_tangent(u, v)
        q = index((u, v))
        need(1 <= q <= 5 and value >= Q(1, 100), "Named short-normal pair violates the claimed index or weight bound")
        result["pairs"].append({"id": pair_id, "normals": (u, v), "q": q,
                                "p": dot(v, bezout(u)) % q, "tangent_weight": str(value)})
        result["completed_pair_ids"].append(pair_id)
        if len(result["pairs"]) % 100 == 0:
            persist()
    need(result["expected_pair_ids"] == result["completed_pair_ids"], "Incomplete explicit indexed pair roster")
    result["pair_expansion_values"] = 2 * len(result["pairs"])
    result["types"] = []
    for wanted, primary, repaired in zip(roster["expected_types"], documents["primary_types"]["types"], documents["repaired_types"]["types"]):
        result["active_id"] = wanted["id"]
        checked = verify_type(primary, repaired, wanted)
        result["types"].append(checked)
        result["completed_ids"].append(wanted["id"])
        if len(result["types"]) % 50 == 0:
            persist()
    result["normal_index_histogram"] = dict(Counter(str(row["q"]) for row in result["types"]))
    result["parallelepiped_points"] = sum(len(row["complete_parallelepiped_points"]) for row in result["types"])
    result["direct_expansion_values"] = sum(len(row["expansions"]) for row in result["types"])
    need(result["normal_index_histogram"] == documents["repaired_types"]["normal_index_histogram"], "Normal-index histogram mismatch")
    need(result["parallelepiped_points"] == documents["repaired_types"]["points_enumerated"] == 1895, "Complete parallelepiped point population mismatch")
    need(result["direct_expansion_values"] == 4868, "Missing Laurent expansion values")
    need(sum(Q(row["standard_weight"]) < 0 for row in result["types"]) == documents["primary_types"]["negative_count"] == 37, "Standard negative local-type inventory mismatch")
    embedded = documents["reconciliation"]["standard_negative_type"]
    matching = [row for row in result["types"] if row["normals"] == imat(embedded["normals"], 3, 4)]
    need(len(matching) == 1 and Q(matching[0]["standard_weight"]) == rational(embedded["standard_weight"]), "Embedded negative example has no matching literal verified identity")
    result["metadata_discrepancies"] = []
    if embedded["type_id"] != matching[0]["source_index"]:
        result["metadata_discrepancies"].append({"field": "J24.standard_negative_type.type_id", "reported": embedded["type_id"],
                                                 "corrected_index": matching[0]["source_index"], "normals": matching[0]["normals"],
                                                 "scope": "Display index only; literal normals and weight independently checked"})


def load_type_certificate(path, sha, roster_sha, checker_sha, roster):
    need(path and sha and re.fullmatch(r"[0-9a-f]{64}", sha), "Metrics require the exact root-approved type-certificate SHA256")
    need(digest_file(path) == sha, "Type-certificate SHA256 mismatch")
    document = decode(Path(path).read_bytes())
    need(document["status"] == "complete" and document["mode"] == "types" and document["native_calls"] == 0,
         "Type certificate is incomplete or incompatible")
    need(document["roster_sha256"] == roster_sha and document["checker_sha256"] == checker_sha, "Type certificate belongs to another frozen checker/roster")
    wanted = [row["id"] for row in roster["expected_types"]]
    need(document["expected_ids"] == wanted == document["completed_ids"], "Type-certificate exact identity coverage mismatch")
    need(document["expected_pair_ids"] == document["completed_pair_ids"] == [row["id"] for row in document["pairs"]] and
         len(document["pairs"]) == len(set(document["completed_pair_ids"])), "Type-certificate pair identity completion mismatch")
    rows = document["types"]
    need(len(rows) == TYPE_COUNT, "Type certificate has the wrong actual type population")
    lookup = {}
    for row, expected in zip(rows, roster["expected_types"]):
        need(row["id"] == expected["id"] and row["normals"] == expected["normals"], "Type certificate literal identity mismatch")
        key = signature(tuple(map(tuple, row["normals"])))
        need(key not in lookup, "Duplicate canonical type certificate")
        lookup[key] = (row["id"], rational(row["metric_independent_K"]))
    return lookup


def verify_metric_record(record, expected, types, geometry_cache):
    normals = normal_list(record["normals"])
    weights = ivec(record["dual_extended_diagonal"], 5)
    need(all(x > 0 for x in weights[:4]) and weights[4] >= 0, "Invalid global metric")
    need(max(dot(v, v) for v in normals) <= 6, "Complete normal list violates the norm-six prerequisite")
    triples = []
    digest = hashlib.sha256()
    minimum = None
    for i, j, k in combinations(range(len(normals)), 3):
        triple = (normals[i], normals[j], normals[k])
        if triple not in geometry_cache:
            q = index(triple)
            if q:
                pair_indices = tuple(index(tuple(triple[b] for b in range(3) if b != a)) for a in range(3))
                need(all(q % pair_index == 0 for pair_index in pair_indices), "Nonintegral primitive ray scale")
                scales = tuple(q // pair_index for pair_index in pair_indices)
                sig = signature(triple)
                need(sig in types, "An independent metric triple is absent from the complete verified type roster")
                geometry_cache[triple] = (q, scales, *types[sig])
            else:
                geometry_cache[triple] = None
        geometry = geometry_cache[triple]
        if geometry is None:
            continue
        q, scales, type_id, constant = geometry
        value, numerator, denominator = metric_value(triple, weights, q, scales, constant)
        need(value > 0, f"Nonpositive complete metric weight at {expected['id']} triple {(i, j, k)}")
        digest.update((str(triple) + ":" + str(numerator) + "/" + str(denominator) + "\n").encode())
        triples.append([i, j, k, type_id, value.numerator, value.denominator])
        minimum = value if minimum is None else min(minimum, value)
    need(triples and len(triples) == integer(record["independent_triples_checked"]), "Independent triple roster/count mismatch")
    need(minimum == rational(record["minimum_weight"]), "Complete metric minimum mismatch")
    need(digest.hexdigest() == record["ordered_exact_weight_digest"], "Complete ordered producer-weight digest mismatch")
    need(record["negative_triple"] is None and record["all_dimension_terminal"] is True, "Returned atlas terminal is not successful")
    clauses = hidden_cubic(normals, record["hidden_cubic"])
    summary = {"id": expected["id"], "source_index": expected["source_index"], "rank": record["rank"],
               "atlas_id": record["atlas_id"], "weights": weights, "triple_count": len(triples),
               "minimum_weight": str(minimum), "producer_weight_digest": digest.hexdigest(),
               "hidden_cubic": clauses, "masks": record["masks"]}
    detail = {"id": expected["id"], "normal_roster": normals, "weights": weights,
              "triple_schema": ["normal_index_i", "normal_index_j", "normal_index_k", "verified_type_id", "weight_numerator", "weight_denominator"],
              "independent_triples": triples}
    return summary, detail


def verify_explicit_triples(entries, normals, types, geometry):
    expected = []
    for tri in combinations(range(len(normals)), 3):
        vectors = tuple(normals[i] for i in tri)
        if vectors not in geometry:
            independent = index(vectors) != 0
            type_id = types.get(signature(vectors), (None, None))[0] if independent else None
            need(not independent or type_id is not None, "Aggregate discovered an uncovered independent type")
            geometry[vectors] = type_id
        if geometry[vectors] is not None:
            expected.append((*tri, geometry[vectors]))
    need(isinstance(entries, list), "Explicit triple roster must be a list")
    values = []
    for row in entries:
        need(isinstance(row, list) and len(row) == 6, "Malformed explicit triple record")
        ivec(row[:3], 3)
        numerator, denominator = integer(row[4]), integer(row[5])
        need(denominator > 0 and gcd(numerator, denominator) == 1, "Malformed exact triple weight")
        values.append(Q(numerator, denominator))
    need([tuple(row[:4]) for row in entries] == expected,
         "Explicit independent-triple roster is incomplete, duplicated, or misattached")
    need(values and min(values) > 0, "Explicit triple roster contains a nonpositive weight")
    return values


def verify_metrics(args, roster, records, result, persist, triple_stream):
    need(0 <= args.begin < args.end <= METRIC_COUNT, "Invalid bounded metric interval")
    types = load_type_certificate(args.type_certificate, args.type_sha256, result["roster_sha256"], result["checker_sha256"], roster)
    wanted = roster["expected_metric_atlases"][args.begin:args.end]
    result.update(begin=args.begin, end=args.end, type_certificate_sha256=args.type_sha256,
                  expected_ids=[row["id"] for row in wanted], metrics=[])
    cache = {}
    for record, expected in zip(records[args.begin:args.end], wanted):
        result["active_id"] = expected["id"]
        summary, detail = verify_metric_record(record, expected, types, cache)
        triple_stream.write(json.dumps(detail, separators=(",", ":")) + "\n")
        triple_stream.flush()
        result["metrics"].append(summary)
        result["completed_ids"].append(expected["id"])
        if len(result["metrics"]) % 25 == 0:
            persist()
    os.fsync(triple_stream.fileno())
    result["triple_occurrences"] = sum(row["triple_count"] for row in result["metrics"])
    result["minimum_weight"] = str(min(Q(row["minimum_weight"]) for row in result["metrics"]))
    result["triple_roster"] = {"path": str(Path(args.triples_output).resolve()), "sha256": digest_file(args.triples_output),
                              "bytes": Path(args.triples_output).stat().st_size,
                              "expected_atlas_ids": result["expected_ids"], "completed_atlas_ids": result["completed_ids"]}


def verify_aggregate(args, roster, documents, result, persist):
    need(args.results_roster, "Aggregate mode requires a frozen results roster")
    receipts = decode(Path(args.results_roster).read_bytes())
    need(set(receipts) == {"type_certificate", "metric_batches"}, "Aggregate roster requires exact type and metric dependencies")
    type_entry = receipts["type_certificate"]
    types = load_type_certificate(type_entry["path"], type_entry["sha256"], result["roster_sha256"], result["checker_sha256"], roster)
    expected = {row["id"]: row for row in roster["expected_metric_atlases"]}
    result["expected_ids"] = list(expected)
    result["metric_atlases"] = []
    seen, criteria, occurrences, minimum, intervals = set(), Counter(), 0, None, []
    batch_names = set()
    geometry = {}
    for receipt in receipts["metric_batches"]:
        need(receipt["job"] not in batch_names, "Duplicate aggregate batch identity")
        batch_names.add(receipt["job"])
        doc = read_bound(receipt)
        need(doc["status"] == "complete" and doc["mode"] == "metrics" and doc["native_calls"] == 0, "Incomplete metric batch")
        need(doc["roster_sha256"] == result["roster_sha256"] and doc["checker_sha256"] == result["checker_sha256"] and
             doc["type_certificate_sha256"] == type_entry["sha256"], "Batch belongs to another checker, roster, or type certificate")
        begin, end = integer(doc["begin"]), integer(doc["end"])
        need(0 <= begin < end <= METRIC_COUNT, "Invalid batch interval")
        ids = [row["id"] for row in roster["expected_metric_atlases"][begin:end]]
        need(doc["expected_ids"] == doc["completed_ids"] == ids, "Batch exact identity coverage mismatch")
        need([row["id"] for row in doc["metrics"]] == ids, "Batch actual metric identities differ")
        intervals.append((begin, end))
        triple_entry = doc["triple_roster"]
        need(digest_file(triple_entry["path"]) == triple_entry["sha256"] and Path(triple_entry["path"]).stat().st_size == triple_entry["bytes"], "Explicit triple roster bytes changed")
        need(triple_entry["expected_atlas_ids"] == triple_entry["completed_atlas_ids"] == ids, "Triple stream identity coverage mismatch")
        line_ids = []
        with Path(triple_entry["path"]).open() as stream:
            for line, summary in zip(stream, doc["metrics"], strict=True):
                detail = decode(line)
                key = detail["id"]
                need(key == summary["id"] and key not in seen, "Duplicate, missing, or misattached atlas completion")
                normals = normal_list(detail["normal_roster"])
                need(detail["normal_roster"] == expected[key]["normals"] and detail["weights"] == expected[key]["weights"], "Explicit triple stream has a different normal list or metric")
                actual = detail["independent_triples"]
                weights = verify_explicit_triples(actual, normals, types, geometry)
                need(len(actual) == summary["triple_count"], "Aggregate triple count mismatch")
                need(weights and min(weights) > 0 and min(weights) == rational(summary["minimum_weight"]), "Aggregate exact minimum mismatch")
                minimum = min(weights) if minimum is None else min(minimum, min(weights))
                occurrences += len(actual)
                criteria.update(clause["criterion"] for clause in summary["hidden_cubic"])
                seen.add(key)
                line_ids.append(key)
                result["completed_ids"].append(key)
                result["metric_atlases"].append({"id": key, "triple_count": len(actual), "minimum_weight": summary["minimum_weight"]})
        need(line_ids == ids, "Explicit triple stream atlas identity order mismatch")
        persist()
    need(sorted(intervals) and sorted(intervals)[0][0] == 0 and sorted(intervals)[-1][1] == METRIC_COUNT and
         all(a[1] == b[0] for a, b in zip(sorted(intervals), sorted(intervals)[1:])), "Metric intervals overlap or leave a gap")
    need(seen == set(expected), "Missing exact atlas identities at final aggregation")
    need(occurrences == TRIPLE_COUNT == documents["reconciliation"]["metric_triple_occurrences"], "Global independent-triple population mismatch")
    need(minimum == EXPECTED_MINIMUM == rational(documents["reconciliation"]["minimum_metric_weight"]), "Global metric minimum mismatch")
    need(dict(criteria) == {"P07 norm-six theorem": 26095, "all rank-two pair weights": 18} == documents["reconciliation"]["hidden_flat_criteria_occurrences"], "Hidden-cubic criterion inventory mismatch")
    result.update(triple_occurrences=occurrences, minimum_weight=str(minimum), hidden_cubic_criteria=dict(criteria),
                  all_3937_metric_identities_and_explicit_triple_rosters_complete=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", required=True)
    parser.add_argument("--mode", required=True, choices=("types", "metrics", "aggregate"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--triples-output")
    parser.add_argument("--type-certificate")
    parser.add_argument("--type-sha256")
    parser.add_argument("--begin", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--results-roster")
    args = parser.parse_args(argv)
    need(args.mode != "metrics" or args.triples_output and args.begin is not None and args.end is not None,
         "Metrics mode needs explicit begin/end and a fresh triple output")
    output = Path(args.output)
    need(args.triples_output is None or output.resolve() != Path(args.triples_output).resolve(), "Summary and triple outputs alias")
    state = {"schema_version": SCHEMA, "status": "running", "mode": args.mode,
             "pid": os.getpid(), "pgid": os.getpgrp(), "native_calls": 0, "scope": SCOPE,
             "checker_sha256": digest_file(__file__), "roster_sha256": digest_file(args.roster),
             "expected_ids": [], "completed_ids": [], "seconds": None}
    start = time.monotonic()
    with output.open("x") as stream:
        def persist():
            state["seconds"] = time.monotonic() - start
            stream.seek(0)
            json.dump(state, stream, indent=2, allow_nan=False)
            stream.write("\n")
            stream.truncate()
            stream.flush()
            os.fsync(stream.fileno())

        persist()
        try:
            roster = decode(Path(args.roster).read_bytes())
            documents, atlases, records = load_inputs(roster)
            if args.mode == "types":
                verify_types(roster, documents, atlases, state, persist)
            elif args.mode == "metrics":
                with Path(args.triples_output).open("x") as triple_stream:
                    verify_metrics(args, roster, records, state, persist, triple_stream)
            else:
                verify_aggregate(args, roster, documents, state, persist)
            need(len(state["completed_ids"]) == len(set(state["completed_ids"])) and
                 set(state["completed_ids"]) == set(state["expected_ids"]), "Final exact identity completion mismatch")
            state.pop("active_id", None)
            state["status"] = "complete"
        except Exception as exc:
            state["status"] = "failed"
            state["error"] = f"{type(exc).__name__}: {exc}"
            persist()
            print(state["error"], file=sys.stderr, flush=True)
            return 2
        persist()
    print(json.dumps({"status": state["status"], "mode": args.mode, "completed": len(state["completed_ids"]),
                      "seconds": state["seconds"], "native_calls": 0}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
