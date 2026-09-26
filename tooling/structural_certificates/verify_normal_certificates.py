#!/usr/bin/env python3
"""Independent, standard-library checker for the frozen FRONTIER-027 certificates.

Commands (all outputs must be outside the returned packet):
  freeze --root PACKET --output normal_manifest.json
  file --root PACKET --manifest normal_manifest.json --file DATA/...json.gz
       --start 0 --limit 50000 --output normal_file_000.json
  types --root PACKET --manifest normal_manifest.json --start 0 --limit 50
        --output normal_types_000.json
  exceptions --root PACKET --manifest normal_manifest.json --output normal_rank5.json
  aggregate --root PACKET --manifest normal_manifest.json
            --reports normal_file_*.json normal_types_*.json normal_rank5.json
            --output normal_aggregate.json

File checks independently establish geometry, complete tuple identities, exact
integer indices and quotient divisors, template kernels, type correspondence,
and raw-plus-correction arithmetic. Their raw numbers remain source-bound until
the separate type checks rebuild every referenced Laurent trace. Aggregate
requires all 34 exact file identities, disjoint complete ordinal coverage,
every referenced type, and the original-rhombus exception check. A deadline or
bounded slice is PARTIAL, never a complete finite certificate. No returned
program is imported or executed. No external mathematical theorem is proved by
this checker: hive/LR correspondence, BV's local formula and valuation theorem,
global cancellation, and geometric rank compression remain proof premises.

freeze binds current bytes, not a Git/capture attestation; the owner must bind
its manifest to the independently captured packet. Source mutation is checked
on every read and again during aggregation. Stdout always contains one report.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations, permutations, product
import json
from math import factorial, gcd, lcm, prod
from pathlib import Path
import sys
import time


SCHEMA = "frontier-027-independent-normal-certificate-v1"
SEALED = "VERIFICATION/SEALED-ROSTERS.json"
PATCH_SYSTEM = "HISTORY/P11-A01/DATA/BOUNDARY-PATCH-SYSTEM.json.gz"
PATCH_VECTORS = "HISTORY/P11-A01/DATA/BOUNDARY-PATCH-FUNCTIONALS.json"
EXCEPTIONS = "DATA/RANK5-EXCEPTION-CERTIFICATE.json"
B5 = "DATA/A02/B-R5-Q4.json.gz"
PREMISES = [
    "Hive/LR correspondence, stretching period collapse, and degree statement.",
    "BV local formula, analyticity, lattice equivariance and orthogonal multiplicativity.",
    "Complete refined normal cycle and cancellation against actual face-volume weights.",
    "Geometric compression horizons and transfer to all boundaries or untested ranks.",
    "Capture/Git provenance is supplied by the owner, not inferred from this manifest.",
]


def sealed_spec():
    result = {}
    for q in range(1, 4):
        for n in range(3, 2 * q + 4):
            legacy = 0 if (n, q) == (3, 3) else q
            result[f"DATA/A02/A-R{n}-Q{legacy}.json.gz"] = ("A", n, q)
    for n in range(5, 13):
        result[f"DATA/{'A04' if n == 12 else 'A02'}/B-R{n}-Q4.json.gz"] = ("B", n, 4)
    for n in range(5, 16):
        result[f"DATA/C-R{n}-Q{0 if n == 5 else 4}.json.gz"] = ("C", n, 4)
    return dict(sorted(result.items()))


EXPECTED = sealed_spec()


class CheckError(Exception):
    pass


class DeadlineReached(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckError(message)


class Deadline:
    def __init__(self, seconds=None):
        self.end = None if seconds is None else time.monotonic() + seconds

    def check(self):
        if self.end is not None and time.monotonic() >= self.end:
            raise DeadlineReached("Declared wall-clock budget reached")


def integer(value):
    require(type(value) is int, f"Expected integer, got {value!r}")
    return value


def rational(value):
    require(type(value) in (int, str), f"Expected exact rational, got {value!r}")
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CheckError(f"Malformed rational: {value!r}") from error


def pairs_unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_number(value):
    raise CheckError(f"Non-exact JSON number: {value}")


def decode(data):
    return json.loads(data, object_pairs_hook=pairs_unique,
                      parse_constant=reject_number)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity_digest(items):
    h = hashlib.sha256()
    for item in items:
        h.update(json.dumps(item, separators=(",", ":"), sort_keys=True).encode())
        h.update(b"\n")
    return h.hexdigest()


def safe_path(root, relative):
    require(isinstance(relative, str), "Input path must be a string")
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts, f"Escaping path: {relative}")
    target = (root / path).resolve()
    require(target.is_relative_to(root.resolve()), f"Escaping symlink: {relative}")
    require(target.is_file(), f"Missing input: {relative}")
    return target


class Inputs:
    def __init__(self, root, entries=None):
        self.root = Path(root).resolve()
        self.entries = entries
        self.reads = {}

    def read(self, relative):
        data = safe_path(self.root, relative).read_bytes()
        evidence = {"sha256": digest(data), "bytes": len(data)}
        if self.entries is not None:
            require(relative in self.entries, f"Unbound source: {relative}")
            require(evidence == self.entries[relative], f"Changed source: {relative}")
        self.reads[relative] = evidence
        return decode(gzip.decompress(data) if relative.endswith(".gz") else data)


def imatrix(rows, nrows=None, ncols=None):
    require(isinstance(rows, list) and bool(rows), "Expected nonempty integer matrix")
    result = tuple(tuple(integer(x) for x in row) for row in rows)
    width = len(result[0])
    require(width > 0 and all(len(row) == width for row in result), "Ragged/empty matrix")
    require(nrows is None or len(result) == nrows, "Matrix row count mismatch")
    require(ncols is None or width == ncols, "Matrix column count mismatch")
    return result


def qmatrix(rows, nrows=None, ncols=None):
    require(isinstance(rows, list) and bool(rows), "Expected nonempty rational matrix")
    result = tuple(tuple(rational(x) for x in row) for row in rows)
    width = len(result[0])
    require(width > 0 and all(len(row) == width for row in result), "Ragged/empty matrix")
    require(nrows is None or len(result) == nrows, "Matrix row count mismatch")
    require(ncols is None or width == ncols, "Matrix column count mismatch")
    return result


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    require(len(a[0]) == len(b), "Matrix multiplication dimension mismatch")
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in transpose(b)) for row in a)


def eye(n):
    return tuple(tuple(Q(i == j) for j in range(n)) for i in range(n))


def inverse(a):
    n = len(a)
    require(all(len(row) == n for row in a), "Inverse of nonsquare matrix")
    rows = [list(map(Q, row)) + list(eye(n)[i]) for i, row in enumerate(a)]
    for k in range(n):
        pivot = next((i for i in range(k, n) if rows[i][k]), None)
        require(pivot is not None, "Singular matrix")
        rows[k], rows[pivot] = rows[pivot], rows[k]
        scale = rows[k][k]
        rows[k] = [x / scale for x in rows[k]]
        for i in range(n):
            if i != k and rows[i][k]:
                scale = rows[i][k]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[k])]
    return tuple(tuple(row[n:]) for row in rows)


def determinant(a):
    n = len(a)
    require(all(len(row) == n for row in a), "Determinant of nonsquare matrix")
    rows = [list(map(Q, row)) for row in a]
    value = Q(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if rows[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            rows[pivot], rows[k] = rows[k], rows[pivot]
            value = -value
        p = rows[k][k]
        value *= p
        for i in range(k + 1, n):
            scale = rows[i][k] / p
            for j in range(k + 1, n):
                rows[i][j] -= scale * rows[k][j]
    return value


def bezout(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    sign = -1 if old_r < 0 else 1
    return sign * old_r, sign * old_s, sign * old_t


def column_reduce(rows, track=False):
    """Unimodular column elimination; kernel columns retain saturation exactly."""
    q, width = len(rows), len(rows[0])
    a = [list(row) for row in rows]
    transform = [list(map(int, row)) for row in eye(width)] if track else None
    if width < q:
        return 0, transform
    answer = 1
    for k in range(q):
        for j in range(k + 1, width):
            if not a[k][j]:
                continue
            first, second = a[k][k], a[k][j]
            g, x, y = bezout(first, second)
            for matrix in (a, transform) if track else (a,):
                for row in matrix:
                    u, v = row[k], row[j]
                    row[k], row[j] = x * u + y * v, -(second // g) * u + (first // g) * v
        if not a[k][k]:
            return 0, transform
        answer *= abs(a[k][k])
    return answer, transform


def normalized_columns(rows):
    cols = []
    for col in zip(*rows):
        lead = next((x for x in col if x), 0)
        if lead:
            cols.append(tuple(x if lead > 0 else -x for x in col))
    return tuple(sorted(cols))


@lru_cache(maxsize=100000)
def index_from_columns(columns, q):
    if not columns:
        return 0
    return column_reduce(transpose(columns))[0] if len(columns) >= q else 0


def lattice_index(rows):
    return index_from_columns(normalized_columns(rows), len(rows)) if rows else 1


def primitive(row):
    row = tuple(map(Q, row))
    den = lcm(*(x.denominator for x in row))
    ints = [int(x * den) for x in row]
    g = gcd(*ints)
    require(g > 0, "Zero primitive vector")
    return tuple(x // g for x in ints)


@lru_cache(maxsize=100000)
def primitive_divisor(columns, facet):
    rows = transpose(columns)
    extra = next(i for i in range(len(rows)) if i not in facet)
    jrows = tuple(rows[i] for i in facet)
    ji, transform = column_reduce(jrows, track=True)
    require(ji > 0, "Dependent patch triple")
    kernel = tuple(tuple(row[j] for j in range(len(facet), len(columns))) for row in transform)
    restricted = [sum(rows[extra][k] * kernel[k][c] for k in range(len(columns)))
                  for c in range(len(columns) - len(facet))]
    divisor = gcd(*restricted)
    require(divisor > 0, "Extra normal vanishes on saturated kernel")
    ii = lattice_index(rows)
    require(ii == ji * divisor, "Index ratio differs from independently restricted gcd")
    return divisor


def gram(rows):
    return matmul(rows, transpose(rows))


def permuted_gram_match(rows, wanted):
    actual = gram(rows)
    return any(tuple(tuple(actual[i][j] for j in p) for i in p) == wanted
               for p in permutations(range(len(rows))))


def signed_match(rows, wanted):
    target = normalized_columns(wanted)
    return any(normalized_columns(tuple(rows[i] for i in p)) == target
               for p in permutations(range(len(rows))))


def atlas(n):
    """Construct 60-degree parallelograms directly, not triangle adjacency."""
    all_points = {(i, j) for i in range(n + 1) for j in range(n + 1 - i)}
    points = tuple(sorted(p for p in all_points if min(p) > 0 and sum(p) < n))
    positions = {p: i for i, p in enumerate(points)}
    directions = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
    rhombi = set()
    for p in sorted(all_points):
        for a, b in combinations(directions, 2):
            dot_twice = 2*a[0]*b[0] + a[0]*b[1] + a[1]*b[0] + 2*a[1]*b[1]
            if dot_twice != 1:
                continue
            x, y = (p[0]+a[0], p[1]+a[1]), (p[0]+b[0], p[1]+b[1])
            z = (p[0]+a[0]+b[0], p[1]+a[1]+b[1])
            if {x, y, z} <= all_points:
                rhombi.add(tuple(sorted((*v, sign) for v, sign in ((p,-1),(x,1),(y,1),(z,-1)))))
    require(len(rhombi) == 3*n*(n-1)//2, "Geometric rhombus count mismatch")
    full = defaultdict(list)
    for rhombus in sorted(rhombi):
        row = [0] * len(points)
        for i, j, value in rhombus:
            if (i, j) in positions:
                row[positions[i, j]] = value
        if any(row):
            require(tuple(row) == primitive(row), "Nonprimitive inward geometric normal")
            full[tuple(row)].append(rhombus)
    normals = tuple(sorted(full))
    return points, normals, full


def connected_tuples(normals, q, deadline):
    """Unique connected induced sets using a rooted frontier exclusion search."""
    incidence = defaultdict(set)
    for i, row in enumerate(normals):
        for c, value in enumerate(row):
            if value:
                incidence[c].add(i)
    neighbors = [set() for _ in normals]
    for bucket in incidence.values():
        for i in bucket:
            neighbors[i].update(bucket - {i})

    def visit(chosen, frontier, excluded, root):
        if len(chosen) == q:
            yield tuple(sorted(chosen))
            return
        remaining, forbidden = set(frontier), set(excluded)
        while remaining:
            vertex = min(remaining)
            remaining.remove(vertex)
            extended = chosen | {vertex}
            new = remaining | {j for j in neighbors[vertex]
                               if j > root and j not in extended and j not in forbidden}
            yield from visit(extended, new, forbidden, root)
            forbidden.add(vertex)

    out = set()
    for root in range(len(normals)):
        deadline.check()
        for item in visit({root}, {j for j in neighbors[root] if j > root}, set(), root):
            require(item not in out, f"Connected enumerator duplicated {item}")
            out.add(item)
        deadline.check()
    return out


def tuple_ids(value, q, count):
    require(isinstance(value, list), "Tuple IDs must be a list")
    result = tuple(integer(x) for x in value)
    require(len(result) == q and tuple(sorted(set(result))) == result,
            f"Unsorted, duplicated or wrong-size tuple: {result}")
    require(all(0 <= x < count for x in result), f"Out-of-range tuple: {result}")
    return result


def templates(inputs):
    system, functionals = inputs.read(PATCH_SYSTEM), inputs.read(PATCH_VECTORS)
    source, vectors = system["templates"], functionals["template_vectors"]
    require(len(source) == len(vectors), "Template/vector roster mismatch")
    coefficients = tuple(rational(x) for x in functionals["coefficients"])
    used, ids, out = set(), set(), []
    for record, vector in zip(source, vectors):
        flags, xy0, rows0 = decode(record["key"])
        xy = imatrix(xy0, ncols=2)
        rows = imatrix(rows0, nrows=3, ncols=len(xy))
        tid = integer(record["id"])
        require(tid not in ids, "Duplicate template ID")
        ids.add(tid)
        require(record["positions"] == xy0 and record["normals"] == rows0,
                "Template key disagrees with literal geometry")
        require(len(flags) == 3 and all(type(f) is int and f in (0, 1) for f in flags), "Bad boundary flags")
        require(xy == tuple(sorted(set(xy))) and min(x for x, _ in xy) == min(y for _, y in xy) == 0,
                "Template support lacks its unique translation anchor")
        require(all(any(row[c] for row in rows) for c in range(len(xy))), "Template has a zero support column")
        require(lattice_index(rows) > 0, "Dependent template triple")
        v = tuple(rational(x) for x in vector)
        require(len(v) == len(xy), "Template vector dimension mismatch")
        require(all(sum(x*y for x, y in zip(row, v)) == 0 for row in rows), "Template Jv is nonzero")
        basis = record["basis"]
        start = integer(record["start"])
        require(start >= 0 and start + len(basis) <= len(coefficients), "Coefficient interval out of bounds")
        positions = set(range(start, start + len(basis)))
        require(not used & positions, "Duplicate coefficient ownership")
        used.update(positions)
        rebuilt = [Q(0)] * len(xy)
        for j, row0 in enumerate(basis):
            row = tuple(integer(x) for x in row0)
            require(len(row) == len(xy), "Template basis dimension mismatch")
            require(all(sum(a*b for a, b in zip(normal, row)) == 0 for normal in rows), "Template basis not in kernel")
            rebuilt = [a + coefficients[start+j]*b for a, b in zip(rebuilt, row)]
        require(tuple(rebuilt) == v, "Functional does not equal its declared basis combination")
        out.append((tuple(flags), xy, rows, v, tid))
    require(used == set(range(len(coefficients))), "Omitted patch coefficient")
    return out


def matched_supports(points, normals, n, source, deadline):
    coords = {p: i for i, p in enumerate(points)}
    normal_ids = {row: i for i, row in enumerate(normals)}
    out = {}
    for flags, shape, rows, vector, tid in source:
        deadline.check()
        for a, b in points:
            embedded = [(a+x, b+y) for x, y in shape]
            if any(p not in coords for p in embedded):
                continue
            actual_flags = (int(a == 1), int(b == 1), int(max(x+y for x, y in embedded) == n-1))
            if flags != actual_flags:
                continue
            cols = [coords[p] for p in embedded]
            ids = []
            for row in rows:
                ambient = [0] * len(points)
                for c, value in zip(cols, row):
                    ambient[c] = value
                if tuple(ambient) not in normal_ids:
                    break
                ids.append(normal_ids[tuple(ambient)])
            if len(ids) != 3:
                continue
            ids = tuple(sorted(ids))
            require(len(set(ids)) == 3, "Collapsed template triple")
            v = tuple(sorted((c, value) for c, value in zip(cols, vector) if value))
            value = (v, lattice_index(rows), tid)
            require(ids not in out or out[ids] == value, "Ambiguous template match")
            out[ids] = value
    return out


def check_supports(records, expected, normals):
    actual = {}
    for record in records:
        ids = tuple_ids(record["ids"], 3, len(normals))
        require(ids not in actual, f"Duplicate support: {ids}")
        vector = tuple(rational(x) for x in record["vector"])
        require(len(vector) == len(normals[0]), "Ambient patch vector dimension mismatch")
        require(all(sum(x*y for x, y in zip(normals[i], vector)) == 0 for i in ids), "Ambient Jv is nonzero")
        actual[ids] = (tuple((i, x) for i, x in enumerate(vector) if x),
                       integer(record["index"]), integer(record["template"]))
    require(actual == expected, "Actual support identities/vectors/indices differ from all template translations")


def multiply_series(a, b, degree):
    out = [Q(0)] * (degree + 1)
    for i, x in enumerate(a):
        for j in range(min(len(b), degree + 1 - i)):
            out[i+j] += x * b[j]
    return out


def exponential_denominator(a, degree):
    """t/(1-exp(a*t)), by formal reciprocal, without a Bernoulli table."""
    require(a != 0, "Nongeneric Laurent covector")
    original = [-a**(j+1) / factorial(j+1) for j in range(degree+1)]
    result = [1 / original[0]]
    for j in range(1, degree+1):
        result.append(-sum(original[k]*result[j-k] for k in range(1, j+1)) / original[0])
    return result


def series_map(value):
    require(isinstance(value, dict), "Expected Laurent coefficient object")
    out = {}
    for exponent, coefficient in value.items():
        power = int(exponent)
        require(str(power) == exponent and power not in out, "Malformed/aliased Laurent exponent")
        out[power] = rational(coefficient)
    return out


def check_fundamental_points(projected, raw_points):
    q = len(projected)
    points = [tuple(integer(x) for x in p) for p in raw_points]
    require(all(len(p) == q for p in points), "Fundamental point dimension mismatch")
    require(len(points) == len(set(points)) == abs(determinant(projected)),
            "Incomplete/duplicate fundamental point roster")
    parallelepiped_inverse = inverse(transpose(projected))
    for point in points:
        coefficients = matmul(parallelepiped_inverse, tuple((Q(x),) for x in point))
        require(all(0 <= x[0] < 1 for x in coefficients),
                "Point outside half-open fundamental parallelepiped")
    return points


def verify_trace(trace, deadline):
    rays = imatrix(trace["tangent_rays"])
    d = len(rays)
    require(1 <= d <= 4 and len(rays[0]) == d and determinant(rays) != 0, "Invalid trace cone dimension/rank")
    require(all(primitive(row) == row for row in rays), "Nonprimitive tangent ray")
    metric = qmatrix(trace["metric"], d, d)
    require(metric == transpose(metric), "Nonsymmetric metric")
    require(all(determinant(tuple(row[:k] for row in metric[:k])) > 0 for k in range(1, d+1)), "Metric not positive definite")
    dual = inverse(metric)
    xi = tuple((rational(x),) for x in trace["generic_covector"])
    require(len(xi) == d, "Trace covector dimension mismatch")
    expected = {tuple(c) for k in range(d) for c in combinations(range(d), k)}
    faces = {}
    for record in trace["faces"]:
        face = tuple_ids(record["face"], len(record["face"]), d)
        require(face in expected and face not in faces, "Duplicate/unexpected Laurent face")
        faces[face] = record
    require(set(faces) == expected, "Missing Laurent face")
    mu_values, point_count = {}, 0
    for face in sorted(expected, key=lambda x: (-len(x), x)):
        deadline.check()
        record, q = faces[face], d-len(face)
        basis = imatrix(record["quotient_basis"], d, q)
        require(lattice_index(transpose(basis)) == 1, "Unsaturated quotient lattice basis")
        require(all(all(x == 0 for x in row) for row in matmul(tuple(rays[i] for i in face), basis)) if face else True,
                "Quotient basis does not annihilate face")
        quotient_metric = inverse(matmul(matmul(transpose(basis), dual), basis))
        require(quotient_metric == qmatrix(record["quotient_metric"], q, q), "Wrong quotient metric")
        rest = [i for i in range(d) if i not in face]
        projected = tuple(primitive(row) for row in matmul(tuple(rays[i] for i in rest), basis))
        require(projected == imatrix(record["projected_rays"], q, q), "Wrong projected primitive rays")
        covector = matmul(matmul(matmul(quotient_metric, transpose(basis)), dual), xi)
        require(tuple(row[0] for row in covector) == tuple(rational(x) for x in record["covector"]), "Wrong projected covector")
        values = [sum(x*y[0] for x, y in zip(row, covector)) for row in projected]
        require(all(values), "Nongeneric projected covector")
        points = check_fundamental_points(projected, record["fundamental_points"])
        # Index-many distinct integral points inside the half-open domain are
        # the complete roster; there is no dependence on an enumeration engine.
        point_count += len(points)
        numerator = [sum(sum(x*y[0] for x, y in zip(p, covector))**k for p in points) / factorial(k)
                     for k in range(d+1)]
        series = numerator
        for value in values:
            series = multiply_series(series, exponential_denominator(value, d), d)
        raw = {k-q: value for k, value in enumerate(series)}
        require(series_map(record["S_series"]) == raw, "Laurent exponential-sum coefficients disagree")
        mu, subtractions = dict(raw), []
        for size in range(1, q+1):
            for local in combinations(range(q), size):
                global_face = tuple(sorted(face + tuple(rest[j] for j in local)))
                index = lattice_index(tuple(projected[j] for j in local))
                prefactor = Q((-1)**size * index) / prod(values[j] for j in local)
                child = {0: Q(1)} if len(global_face) == d else mu_values[global_face]
                for power in mu:
                    mu[power] -= prefactor * child.get(power+size, 0)
                subtractions.append((local, global_face, index, prefactor))
        actual = [(tuple_ids(x["local_face"], len(x["local_face"]), q),
                   tuple_ids(x["global_face"], len(x["global_face"]), d),
                   integer(x["index"]), rational(x["integral_prefactor"]))
                  for x in record["face_subtractions"]]
        require(actual == subtractions, "Missing/duplicate/incorrect Laurent face subtraction")
        require(series_map(record["mu_series"]) == mu, "Laurent local valuation recurrence disagrees")
        require(all(value == 0 for power, value in mu.items() if power < 0), "Uncancelled Laurent pole")
        mu_values[face] = mu
    alpha = mu_values[()][0]
    require(alpha == rational(trace["alpha"]), "Trace alpha differs from reconstructed constant")
    return {"alpha": str(alpha), "proper_faces": len(faces), "fundamental_points": point_count}


def type_description(record):
    if "kind" in record:
        kind = record["kind"]
        require(kind in ("saturated_gram", "signed_ambient"), "Unknown inherited type kind")
        representative = imatrix(record["representative_normals"])
        index = integer(record.get("normal_index", 1))
        target = imatrix(record["normal_gram"] if kind == "saturated_gram" else record["canonical_normals"])
        full = record["full_laurent"]
        trace = full if kind == "saturated_gram" else full["laurent"]
    else:
        key = record["key"]
        require(isinstance(key, list) and len(key) == 3 and key[1] in ("g", "s"), "Malformed type key")
        kind = "saturated_gram" if key[1] == "g" else "signed_ambient"
        representative, target = imatrix(record["representative"]), imatrix(key[2])
        index, trace = integer(record["index"]), record["trace"]
        require(integer(key[0]) == len(representative), "Type key dimension mismatch")
    require(1 <= len(representative) <= 4, "Type outside q <= 4")
    require(lattice_index(representative) == index > 0, "Type representative index mismatch")
    if kind == "saturated_gram":
        require(index == 1 and permuted_gram_match(representative, target), "Representative does not realize saturated Gram")
    else:
        require(signed_match(representative, target), "Representative does not realize signed integer embedding")
    return kind, representative, target, index, rational(record["alpha"]), trace


def verify_type(record, deadline):
    kind, representative, target, index, alpha, trace = type_description(record)
    q = len(representative)
    rays, metric = imatrix(trace["tangent_rays"], q, q), qmatrix(trace["metric"], q, q)
    if kind == "saturated_gram":
        require(rays == eye(q) and metric == inverse(target), "Saturated trace lacks its exact lattice/metric binding")
    else:
        conormals = tuple(primitive(row) for row in transpose(inverse(rays)))
        embedding = matmul(inverse(conormals), target)
        require(all(x.denominator == 1 for row in embedding for x in row), "Nonintegral normal embedding")
        embedding = tuple(tuple(int(x) for x in row) for row in embedding)
        require(lattice_index(embedding) == 1, "Trace integer embedding is not saturated")
        require(gram(embedding) == inverse(metric), "Trace metric differs from actual integer embedding")
        if "kind" in record:
            full = record["full_laurent"]
            basis = imatrix(full["normal_basis_columns"], len(target[0]), q)
            coordinates = imatrix(full["normal_coordinates"], q, q)
            require(lattice_index(transpose(basis)) == 1, "Inherited normal basis not saturated")
            require(matmul(coordinates, transpose(basis)) == target, "Inherited normal coordinates do not embed exactly")
            require(tuple(primitive(row) for row in transpose(inverse(coordinates))) == rays, "Inherited tangent rays disagree")
            require(inverse(gram(transpose(basis))) == metric == qmatrix(full["tangent_metric"], q, q), "Inherited tangent metric disagrees")
    result = verify_trace(trace, deadline)
    require(rational(result["alpha"]) == alpha, "Type alpha differs from independently reconstructed trace")
    return {"q": q, "index": index, "kind": kind, **result}


class TypeBindings:
    def __init__(self, inputs):
        self.inputs, self.types, self.matches = inputs, {}, {}

    def bind(self, rows, path):
        if path not in self.types:
            self.types[path] = type_description(self.inputs.read(path))
        kind, _, target, claimed_index, alpha, _ = self.types[path]
        columns = normalized_columns(rows)
        key = (columns, path)
        if key not in self.matches:
            index = index_from_columns(columns, len(rows))
            require(index == claimed_index > 0, "Occurrence/type integer index mismatch")
            if kind == "saturated_gram":
                require(permuted_gram_match(rows, target), "Occurrence/type Gram mismatch")
            else:
                require(signed_match(rows, target), "Occurrence/type signed embedding mismatch")
            self.matches[key] = index
        return alpha, self.matches[key], columns


def freeze(root, deadline, specification=None):
    specification = EXPECTED if specification is None else specification
    inputs = Inputs(root)
    sealed = inputs.read(SEALED)
    listed = [row["path"] for row in sealed["checks"]]
    require(len(listed) == len(set(listed)) and set(listed) == set(specification),
            "Sealed roster has omitted, duplicated or unexpected file identities")
    types, files = set(), []
    by_path = {row["path"]: row for row in sealed["checks"]}
    for path, (gate, rank, q) in specification.items():
        deadline.check()
        record = inputs.read(path)
        require(record["rank"] == rank and record["gate"] == gate, "Frozen file metadata differs from roster identity")
        require(by_path[path]["gate"] == gate and by_path[path]["rank"] == rank and by_path[path]["q"] == q,
                "Sealed metadata differs from exact declared roster")
        types.update(x["type_source"] for x in record["records"])
        files.append({"path": path, "gate": gate, "rank": rank, "q": q,
                      "records": len(record["records"]), "dependent": len(record["dependent"])})
    for path in [PATCH_SYSTEM, PATCH_VECTORS, EXCEPTIONS, *sorted(types)]:
        deadline.check()
        inputs.read(path)
    return {"schema": SCHEMA, "kind": "manifest", "status": "FROZEN_INPUTS_ONLY",
            "root_at_freeze": str(Path(root).resolve()), "files": files,
            "type_paths": sorted(types), "inputs": dict(sorted(inputs.reads.items())),
            "provenance": "Current byte hashes; capture/Git binding must be supplied independently."}


def check_file(inputs, spec, start, limit, deadline, result):
    path, n, q, gate = spec["path"], spec["rank"], spec["q"], spec["gate"]
    data = inputs.read(path)
    require(data["rank"] == n and data["gate"] == gate, "File identity metadata changed")
    points, normals, _ = atlas(n)
    require(imatrix(data["points"], ncols=2) == points and imatrix(data["normals"]) == normals,
            "Stored normal atlas differs from original geometric rhombi")
    supports = {} if gate == "A" else matched_supports(points, normals, n, templates(inputs), deadline)
    check_supports(data["supports"], supports, normals)
    if gate == "C":
        expected = set()
        for triple, (v, _, _) in supports.items():
            deadline.check()
            for extra, normal in enumerate(normals):
                if extra not in triple and sum(value*normal[c] for c, value in v):
                    expected.add(tuple(sorted((*triple, extra))))
    else:
        expected = connected_tuples(normals, q, deadline)
    records, dependent = data["records"], data["dependent"]
    all_ids = [tuple_ids(record["ids"], q, len(normals)) for record in records]
    all_ids += [tuple_ids(ids, q, len(normals)) for ids in dependent]
    require(len(all_ids) == len(set(all_ids)), "Duplicate tuple identity, including across independent/dependent lists")
    found = set(all_ids)
    require(found == expected,
            f"Tuple coverage mismatch: missing={sorted(expected-found)[:5]}, unexpected={sorted(found-expected)[:5]}")
    require(len(records) == spec["records"] and len(dependent) == spec["dependent"], "Manifest record lengths changed")
    total = len(all_ids)
    require(0 <= start <= total, "Slice start is outside the exact roster")
    stop = total if limit is None else min(total, start+limit)
    result.update(topology_complete=True, expected_tuple_sha256=identity_digest(sorted(expected)),
                  total=total, records_total=len(records), dependent_total=len(dependent),
                  supports=len(supports), start=start, stop=start, checked_ids_sha256=identity_digest([]),
                  independent=0, dependent=0, primitive_incidences=0, nonpositive=0,
                  positive_minimum=None, used_types=[])
    bindings, checked, used_types = TypeBindings(inputs), [], set()
    sparse = [{j: value for j, value in enumerate(row) if value} for row in normals]
    minimum = None
    try:
        for ordinal in range(start, stop):
            deadline.check()
            ids = all_ids[ordinal]
            cols = sorted(set().union(*(sparse[i] for i in ids)))
            rows = tuple(tuple(sparse[i].get(c, 0) for c in cols) for i in ids)
            if ordinal >= len(records):
                require(lattice_index(rows) == 0, f"Listed dependent tuple is independent: {ids}")
                result["dependent"] += 1
            else:
                rec = records[ordinal]
                alpha, index, columns = bindings.bind(rows, rec["type_source"])
                require(index == integer(rec["index"]) and alpha == rational(rec["raw"]), f"Raw/index mismatch at {ids}")
                value, events = alpha, []
                for facet in combinations(range(q), 3) if q == 4 and gate != "A" else ():
                    triple = tuple(ids[j] for j in facet)
                    if triple not in supports:
                        continue
                    vector, ji, tid = supports[triple]
                    extra = next(i for i in ids if i not in triple)
                    divisor = primitive_divisor(columns, facet)
                    require(index == ji*divisor, f"Primitive quotient divisor mismatch at {ids}/{triple}")
                    change = sum((z*normals[extra][c] for c, z in vector), Q(0)) / divisor
                    value += change
                    events.append([list(triple), extra, str(divisor), str(change), tid])
                require(rec["events"] == events, f"Correction event roster/arithmetic mismatch at {ids}")
                require(value == rational(rec["corrected"]), f"Corrected sign arithmetic mismatch at {ids}")
                if value <= 0:
                    require(gate == "B" and n == 5, f"Unexpected nonpositive local value at {path}:{ids} -> {value}")
                    result["nonpositive"] += 1
                else:
                    minimum = value if minimum is None else min(value, minimum)
                    if gate in ("B", "C") and n >= 6:
                        require(value > Q(1, 3000), f"Positive value below claimed strict bound at {ids}")
                result["primitive_incidences"] += len(events)
                result["independent"] += 1
                used_types.add(rec["type_source"])
            checked.append(ids)
            result["stop"] = ordinal+1
    finally:
        result["checked_ids_sha256"] = identity_digest(checked)
        result["positive_minimum"] = None if minimum is None else str(minimum)
        result["used_types"] = sorted(used_types)
    result["status"] = "FILE_ARITHMETIC_PASS" if start == 0 and stop == total else "PARTIAL"
    result["raw_value_scope"] = "Source-bound type values; full Laurent validation is a separate required aggregate gate."


def check_types(inputs, paths, start, limit, deadline, result):
    require(0 <= start <= len(paths), "Type slice start out of range")
    stop = len(paths) if limit is None else min(len(paths), start+limit)
    result.update(start=start, stop=start, total=len(paths), checked=[])
    for ordinal in range(start, stop):
        deadline.check()
        path = paths[ordinal]
        check = verify_type(inputs.read(path), deadline)
        result["checked"].append({"ordinal": ordinal, "path": path, **check})
        result["stop"] = ordinal+1
    result["status"] = "ALL_TYPE_TRACES_PASS" if start == 0 and stop == len(paths) else "PARTIAL"


def check_exceptions(inputs, deadline, result):
    data, claims = inputs.read(B5), inputs.read(EXCEPTIONS)
    points, normals, original = atlas(5)
    require(imatrix(data["points"], ncols=2) == points and imatrix(data["normals"]) == normals, "Exception normal atlas mismatch")
    negative = {}
    for rec in data["records"]:
        if rational(rec["corrected"]) <= 0:
            ids = tuple_ids(rec["ids"], 4, len(normals))
            require(ids not in negative, "Duplicate nonpositive tuple")
            negative[ids] = rational(rec["raw"])
    expected = {}
    for ids, raw in negative.items():
        deadline.check()
        for choice in product(*(original[normals[i]] for i in ids)):
            positions = {(i, j) for row in choice for i, j, _ in row}
            gaps = (min(i for i, _ in positions), min(j for _, j in positions), 5-max(i+j for i, j in positions))
            require(all(0 <= gap < 2 for gap in gaps), f"Rank-five preimage has a liftable gap: {ids} {gaps}")
            identity = (ids, tuple(sorted(choice)))
            require(identity not in expected, "Duplicate generated original-rhombus choice")
            expected[identity] = (gaps, raw)
    found = {}
    for rec in claims["checks"]:
        ids = tuple_ids(rec["ids"], 4, len(normals))
        rows = tuple(sorted(tuple(sorted(tuple(integer(z) for z in p) for p in row)) for row in rec["full_rhombi"]))
        identity = (ids, rows)
        require(identity not in found, "Duplicate exceptional original-rhombus identity")
        found[identity] = (tuple(integer(x) for x in rec["boundary_gaps"]), rational(rec["raw"]))
        require(rec["no_gap_can_have_been_compressed"] is True, "False exceptional gap claim")
    require(found == expected, "Omitted, changed or unexpected original-rhombus preimage")
    maximum = max((max(gaps) for gaps, _ in expected.values()), default=None)
    require(claims["negative_tuples"] == len(negative) and claims["original_rhombus_choices"] == len(expected), "Exceptional aggregate counts disagree")
    require(claims["maximum_gap"] == maximum and claims["all_unliftable_by_cap_two"] is True, "Exceptional aggregate gap claim disagrees")
    result.update(status="EXCEPTION_PREIMAGES_PASS", negative_tuples=len(negative), original_choices=len(expected),
                  maximum_gap=maximum, identities_sha256=identity_digest(sorted(expected)),
                  scope="All original preimages of the source-recorded nonpositive rank-five tuples; sign arithmetic requires the B5 file gate.")


def validate_manifest(manifest):
    require(manifest["schema"] == SCHEMA and manifest["kind"] == "manifest", "Wrong manifest format")
    files = manifest["files"]
    paths = [x["path"] for x in files]
    require(len(paths) == len(set(paths)) and set(paths) == set(EXPECTED), "Manifest omitted/duplicated/changed exact 34-file roster")
    for spec in files:
        require((spec["gate"], spec["rank"], spec["q"]) == EXPECTED[spec["path"]], "Manifest file identity changed")
        require(integer(spec["records"]) >= 0 and integer(spec["dependent"]) >= 0, "Invalid manifest lengths")
    require(manifest["type_paths"] == sorted(set(manifest["type_paths"])), "Manifest type identities not unique/sorted")
    required = set(paths) | set(manifest["type_paths"]) | {SEALED, PATCH_SYSTEM, PATCH_VECTORS, EXCEPTIONS}
    require(set(manifest["inputs"]) == required, "Manifest source closure mismatch")


def aggregate(inputs, manifest, reports, manifest_sha, code_sha, deadline, result):
    grouped, type_seen, exception_reports = defaultdict(list), {}, []
    report_bytes = set()
    for path in reports:
        deadline.check()
        body = Path(path).read_bytes()
        require(digest(body) not in report_bytes, "Duplicate/retried report supplied to aggregate")
        report_bytes.add(digest(body))
        report = decode(body)
        require(report.get("schema") == SCHEMA and report.get("manifest_sha256") == manifest_sha
                and report.get("checker_sha256") == code_sha, "Report belongs to another manifest/checker")
        require(report["status"] not in ("FAIL", "NOT_STARTED"), "Failed/unstarted report cannot contribute coverage")
        require(report["kind"] in ("file", "types", "exceptions"), "Unexpected aggregate report kind")
        for source, binding in report["read_inputs"].items():
            require(source in manifest["inputs"] and binding == manifest["inputs"][source], "Report input binding changed")
        if report["kind"] == "file":
            require(report["file"] in EXPECTED, "Unexpected file report identity")
            if report.get("topology_complete"):
                grouped[report["file"]].append(report)
        elif report["kind"] == "types":
            checked = report.get("checked", [])
            require([x["ordinal"] for x in checked] == list(range(report["start"], report["stop"])), "Type report interval mismatch")
            for check in checked:
                require(check["path"] not in type_seen, "Duplicated type verification identity")
                require(manifest["type_paths"][check["ordinal"]] == check["path"], "Type identity/ordinal mismatch")
                require(check["path"] in report["read_inputs"], "Type report omitted its source binding")
                source = inputs.read(check["path"])
                kind, representative, _, index, alpha, trace = type_description(source)
                require((check["kind"], check["q"], check["index"], rational(check["alpha"])) ==
                        (kind, len(representative), index, alpha), "Type report metadata/value differs from bound source")
                require(check["proper_faces"] == (1 << len(representative))-1 and
                        check["fundamental_points"] == sum(len(face["fundamental_points"]) for face in trace["faces"]),
                        "Type report face/point population mismatch")
                type_seen[check["path"]] = check
        else:
            if report["status"] == "EXCEPTION_PREIMAGES_PASS":
                exception_reports.append(report)
            else:
                require(report["status"] == "PARTIAL", "Invalid exceptional-preimage report")
    require(len(exception_reports) <= 1, "Duplicate exceptional-preimage gate")
    result.update(files=[], type_paths_verified=sorted(type_seen), missing_type_paths=sorted(set(manifest["type_paths"])-set(type_seen)),
                  exceptional_preimages_complete=bool(exception_reports), unproved_mathematical_premises=PREMISES)
    all_complete = True
    for spec in manifest["files"]:
        deadline.check()
        path, total = spec["path"], spec["records"]+spec["dependent"]
        data = inputs.read(path)
        ids = [x["ids"] for x in data["records"]] + data["dependent"]
        require(len(ids) == total and len({tuple(x) for x in ids}) == total, "Bound source roster length/uniqueness mismatch")
        pieces = sorted(grouped[path], key=lambda x: (x["start"], x["stop"]))
        require(total != 0 or len(pieces) <= 1, "Duplicate empty-roster verification")
        require(len({x["expected_tuple_sha256"] for x in pieces}) <= 1, "Reports disagree on expected tuple identities")
        expected_ids_digest = identity_digest(sorted(ids))
        cursor, missing, sums, minimum = 0, [], Counter(), None
        for piece in pieces:
            start, stop = integer(piece["start"]), integer(piece["stop"])
            require(0 <= start <= stop <= total and start >= cursor, "Overlapping/invalid file slices")
            if start > cursor:
                missing.append([cursor, start])
            require(piece["total"] == total and piece["checked_ids_sha256"] == identity_digest(ids[start:stop]), "Slice identity digest/length mismatch")
            require(piece["expected_tuple_sha256"] == expected_ids_digest, "Expected tuple digest does not bind the complete source identities")
            independent_count = max(0, min(stop, spec["records"])-min(start, spec["records"]))
            require(piece["independent"] == independent_count and piece["dependent"] == stop-start-independent_count,
                    "Slice independent/dependent population mismatch")
            slice_records = data["records"][start:min(stop, spec["records"])]
            used_types = sorted({rec["type_source"] for rec in slice_records})
            require(piece["used_types"] == used_types, "Slice type-source identity coverage mismatch")
            required_reads = {path, *used_types}
            if spec["gate"] != "A":
                required_reads.update((PATCH_SYSTEM, PATCH_VECTORS))
            require(required_reads <= set(piece["read_inputs"]), "File report omitted required source bindings")
            corrected = [rational(rec["corrected"]) for rec in slice_records]
            positive = [value for value in corrected if value > 0]
            require(piece["nonpositive"] == sum(value <= 0 for value in corrected) and
                    piece["primitive_incidences"] == sum(len(rec["events"]) for rec in slice_records),
                    "Slice sign/event population mismatch")
            slice_minimum = None if not positive else str(min(positive))
            require(piece["positive_minimum"] == slice_minimum, "Slice positive minimum mismatch")
            for key in ("independent", "dependent", "primitive_incidences", "nonpositive"):
                sums[key] += integer(piece[key])
            if piece["positive_minimum"] is not None:
                value = rational(piece["positive_minimum"])
                minimum = value if minimum is None else min(minimum, value)
            cursor = stop
        if cursor < total:
            missing.append([cursor, total])
        complete = bool(pieces) and not missing
        all_complete &= complete
        result["files"].append({"path": path, "complete": complete, "missing_intervals": missing,
                                "positive_minimum": None if minimum is None else str(minimum), **sums})
    result["derived_totals_for_verified_slices"] = {
        key: sum(record.get(key, 0) for record in result["files"])
        for key in ("independent", "dependent", "primitive_incidences", "nonpositive")
    }
    # Verify every frozen source again, including templates, exception claims,
    # all used types and the literal selected-roster manifest.
    for source in manifest["inputs"]:
        deadline.check()
        inputs.read(source)
    complete = all_complete and not result["missing_type_paths"] and bool(exception_reports)
    result["status"] = "COMPLETE_FINITE_CERTIFICATE_PASS" if complete else "PARTIAL"
    result["finite_scope"] = "Exact selected A/B/C files only; B ranks 13 and 14 are not checked."


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("freeze", "file", "types", "exceptions", "aggregate"))
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--file")
    parser.add_argument("--reports", nargs="*", default=[])
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--budget-seconds", type=int, default=100)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    started = time.monotonic()
    result = {"schema": SCHEMA, "kind": args.command, "status": "NOT_STARTED"}
    inputs = None
    try:
        require(0 < args.budget_seconds <= 110, "Internal budget must be 1..110 seconds; owner retains a 120-second child cap")
        require(args.start >= 0 and (args.limit is None or args.limit > 0), "Invalid slice")
        root, output = Path(args.root).resolve(), Path(args.output).resolve()
        require(not output.is_relative_to(root), "Output must be outside the immutable packet")
        require(not output.exists(), "Refusing to overwrite an existing report")
        require(output.parent.is_dir(), "Output directory must already exist")
        deadline = Deadline(args.budget_seconds)
        code_sha = digest(Path(__file__).read_bytes())
        if args.command == "freeze":
            result = freeze(root, deadline)
            result["checker_sha256_at_freeze"] = code_sha
        else:
            require(args.manifest is not None, "--manifest is required")
            manifest_bytes = Path(args.manifest).read_bytes()
            manifest = decode(manifest_bytes)
            validate_manifest(manifest)
            manifest_sha = digest(manifest_bytes)
            result.update(manifest_sha256=manifest_sha, checker_sha256=code_sha)
            inputs = Inputs(root, manifest["inputs"])
            if args.command == "file":
                require(args.file in EXPECTED, "--file must name an exact sealed roster path")
                result["file"] = args.file
                spec = next(x for x in manifest["files"] if x["path"] == args.file)
                check_file(inputs, spec, args.start, args.limit, deadline, result)
            elif args.command == "types":
                check_types(inputs, manifest["type_paths"], args.start, args.limit, deadline, result)
            elif args.command == "exceptions":
                check_exceptions(inputs, deadline, result)
            else:
                aggregate(inputs, manifest, args.reports, manifest_sha, code_sha, deadline, result)
    except DeadlineReached as error:
        result.update(status="PARTIAL", interruption=str(error))
    except (CheckError, KeyError, TypeError, ValueError, IndexError, OSError, EOFError, ZeroDivisionError, json.JSONDecodeError) as error:
        result.update(status="FAIL", error=f"{type(error).__name__}: {error}")
    result["elapsed_seconds"] = round(time.monotonic()-started, 6)
    requested_slice_complete = False
    if (args.command in ("file", "types") and result["status"] == "PARTIAL"
            and "interruption" not in result and "total" in result):
        requested_stop = result["total"] if args.limit is None else min(result["total"], args.start + args.limit)
        requested_slice_complete = result.get("stop") == requested_stop
    result["requested_slice_complete"] = requested_slice_complete
    if inputs is not None:
        result["read_inputs"] = dict(sorted(inputs.reads.items()))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    # Never write into the packet or replace an existing artifact, even on a
    # failing invocation. No parent directories are implicitly created.
    output = Path(args.output).resolve()
    if not output.is_relative_to(Path(args.root).resolve()) and not output.exists() and output.parent.is_dir():
        with output.open("x", encoding="utf-8") as stream:
            stream.write(text)
    print(text, end="")
    # A completed requested slice is a successful command, while its PARTIAL
    # status still forbids a whole-file/type-population claim before aggregate.
    return 1 if result["status"] == "FAIL" else 2 if result["status"] == "PARTIAL" and not requested_slice_complete else 0


if __name__ == "__main__":
    sys.exit(main())
