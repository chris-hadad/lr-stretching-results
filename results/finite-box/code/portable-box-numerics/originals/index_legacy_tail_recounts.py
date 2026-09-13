#!/usr/bin/env python3
"""Fresh forced-chart jobs for exactly legacy source IDs 272..296.

Owner harness command:
  index --output MANIFEST [--start 272 --stop 297] [--budget-seconds 90]
  accept --manifest MANIFEST --reports COUNT_REPORT... --output ACCEPTANCE

This generator does no lattice counting and does not import old generators,
geometry helpers, provider programs, or the frozen recount consumer. The latter
is a separately pinned consumer of the generic manifest and jobs schema.

RREF proves an integer coordinate chart and a degree upper bound, never actual
dimension. Mixed-node jobs require a FRESH complete positive strict anchor
before any reciprocity or interpolation claim. verified_interpolation_samples
is the explicit owner-facing gate; ordinary consumer MATCH/aggregate status
alone does not establish it. A larger chart bound uses closed nodes only.

The full 25-terminal roster remains literal in partial manifests. --start and
--stop select source IDs, whereas consumer run --start selects local manifest
ordinals. Earlier manifests/results, including attempted IDs 272..279, are not
reused. The owner separately joins the verified prefix 0..271 with this tail.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time


W = Path(__file__).resolve().parent
C = Path("/Volumes/SLR-Research/stretched-lr-research")
DEFAULT_SOURCES = W / "publication-staging/LEGACY-VECTOR-SOURCES.json"
SOURCE_SHA = "225c66d78739d69780d97f7849101cfeb7191e153261da0864156a6ccb2657fa"
MASK_PATHS = {n: C / f"methods/frontier-025-2026-09-10/science/results/F025-MASK-R{n}-001.json" for n in (6, 7)}
MASK_SHA = {6: "6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0",
            7: "bb595b3914ce05105743e9386f2cc64a4d2ae2d59df0d340c3221b8b74d7cd9c"}
SCHEMA = "pro026-independent-hive-recount-v1"
TAIL_IDS = tuple(range(272, 297))


class CheckError(ValueError):
    pass


class DeadlineReached(Exception):
    pass


def need(ok, message):
    if not ok:
        raise CheckError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    def unique(items):
        result = {}
        for key, value in items:
            need(key not in result, "Duplicate JSON field")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def integer(value):
    need(type(value) is int, "An exact integer field is required")
    return value


def rational(value):
    need(type(value) is int or type(value) is str and re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value),
         "Non-exact rational coefficient")
    return Q(value)


class Deadline:
    def __init__(self, seconds=90):
        need(0 < seconds <= 100, "Internal indexing deadline must be at most 100 seconds")
        self.end = time.monotonic() + seconds

    def check(self):
        if time.monotonic() >= self.end:
            raise DeadlineReached("Index incomplete at the declared deadline")


def pin(path, deadline=None):
    path = Path(path).resolve(strict=True)
    before = path.stat()
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while raw := stream.read(1024 * 1024):
            if deadline:
                deadline.check()
            h.update(raw)
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), "Source changed while hashing")
    return {"path": str(path), "bytes": before.st_size, "sha256": h.hexdigest()}


def save(path, value):
    with Path(path).open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def pointer(document, expression):
    if expression == "":
        return document
    need(isinstance(expression, str) and expression.startswith("/"), "Invalid exact JSON pointer")
    for token in expression[1:].split("/"):
        need(re.search(r"~(?![01])", token) is None, "Invalid pointer escape")
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(document, list):
            need(re.fullmatch(r"0|[1-9][0-9]*", token), "Invalid list pointer")
            document = document[int(token)]
        else:
            document = document[token]
    return document


def triple(value):
    if isinstance(value, dict):
        need(set(value) == {"lambda", "mu", "nu"}, "Incomplete or extra whole-triple field")
        value = [value[k] for k in ("lambda", "mu", "nu")]
    need(isinstance(value, (list, tuple)) and len(value) == 3, "Missing full triple")
    parts = []
    for part in value:
        need(isinstance(part, (list, tuple)) and all(type(x) is int and x >= 0 for x in part)
             and list(part) == sorted(part, reverse=True), "Invalid partition")
        part = list(part)
        while part and part[-1] == 0:
            part.pop()
        parts.append(part)
    need(sum(parts[0]) == sum(parts[1]) + sum(parts[2]), "Whole triple is unbalanced")
    return dict(zip(("lambda", "mu", "nu"), parts))


def bind_triples(source, terminal):
    source, terminal = triple(source), triple(terminal)
    need(source["lambda"] == terminal["lambda"], "Outer partition changed")
    if source == terminal:
        operation = "identity_after_trailing_zero_trim"
    else:
        need(source["mu"] == terminal["nu"] and source["nu"] == terminal["mu"], "Unsupported source-to-terminal transformation")
        operation = "inner_exchange_after_trailing_zero_trim"
    return {"operation": operation, "common_dilation_or_affine_reduction_used": False,
            "premise": "Classical LR inner commutativity and zero-padding invariance"}


def original_hive(bare):
    """Literal inward rhombi in the accepted F025 triangular row convention."""
    bare = triple(bare)
    n = max(map(len, bare.values()))
    need(n >= 2, "No positive-rank triangular chart")
    padded = [bare[k] + [0] * (n - len(bare[k])) for k in ("lambda", "mu", "nu")]
    points = [(i, j) for i in range(1, n) for j in range(1, n - i)]
    m = len(points)
    need(m == (n - 1) * (n - 2) // 2, "Missing ambient hive coordinate")
    vertex = {}
    def boundary(point, value):
        row = [value] + [0] * m
        need(point not in vertex or vertex[point] == row, "Inconsistent boundary corner")
        vertex[point] = row
    L, M, N = padded
    for k in range(n + 1):
        boundary((k, 0), sum(M[:k]))
        boundary((0, k), sum(L[:k]))
        boundary((n - k, k), sum(M) + sum(N[:k]))
    for k, p in enumerate(points):
        vertex[p] = [0] + [int(k == j) for j in range(m)]
    stencils, rows = [], []
    for i in range(n):
        for j in range(n - i):
            nearby = []
            if i + j + 1 < n:
                nearby.append(([(i + 1, j), (i, j + 1)], [(i, j), (i + 1, j + 1)]))
            if j > 0:
                nearby.append(([(i, j), (i + 1, j)], [(i, j + 1), (i + 1, j - 1)]))
            if i > 0:
                nearby.append(([(i, j), (i, j + 1)], [(i + 1, j), (i - 1, j + 1)]))
            for positive, negative in nearby:
                stencils.append({"row": len(rows), "positive": [list(p) for p in positive], "negative": [list(p) for p in negative]})
                rows.append([sum(vertex[p][k] for p in positive) - sum(vertex[p][k] for p in negative) for k in range(m + 1)])
    need(len(rows) == 3 * n * (n - 1) // 2, "Incomplete original rhombus system")
    mask = sum(1 << (s * (n - 1) + k) for s, part in enumerate(padded) for k in range(n - 1) if part[k] == part[k + 1])
    return {"rank": n, "ambient_dimension": m, "padded_boundary": dict(zip(("lambda", "mu", "nu"), padded)),
            "boundary_mask": mask, "points": [list(p) for p in points], "stencils": stencils, "rows": rows,
            "count_boundary_area": sum(L)}


def rref_equations(rows, width):
    """Exact RREF of [E|-b], with no inexact rank decisions."""
    need(all(len(row) == width + 1 for row in rows), "Ragged equation system")
    matrix = [[Q(x) for x in row] for row in rows]
    pivots, rank = [], 0
    for col in range(width):
        pivot = next((k for k in range(rank, len(matrix)) if matrix[k][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        divisor = matrix[rank][col]
        matrix[rank] = [x / divisor for x in matrix[rank]]
        for k in range(len(matrix)):
            if k != rank and matrix[k][col]:
                scale = matrix[k][col]
                matrix[k] = [x - scale * y for x, y in zip(matrix[k], matrix[rank])]
        pivots.append(col)
        rank += 1
    need(all(any(row[:width]) or row[-1] == 0 for row in matrix), "Forced closed equations are inconsistent")
    return matrix, pivots


def substitute(rows, offset, basis):
    d = len(basis[0]) if basis else 0
    return [[row[0] + sum(a * b for a, b in zip(row[1:], offset)),
             *[sum(a * basis[k][j] for k, a in enumerate(row[1:])) for j in range(d)]] for row in rows]


def verify_chart(rows, closed_mask, proof, expected_dimension=None):
    m = len(rows[0]) - 1
    need(type(closed_mask) is int and 0 <= closed_mask < (1 << len(rows)), "Invalid full-rhombus forced mask")
    forced = [i for i in range(len(rows)) if closed_mask >> i & 1]
    need(proof["closed_rows_mask"] == closed_mask and proof["forced_row_indices"] == forced
         and proof["forced_original_rows"] == [rows[i] for i in forced], "Missing, extra or changed forced row")
    matrix, pivots = rref_equations([rows[i][1:] + [-rows[i][0]] for i in forced], m)
    free = [j for j in range(m) if j not in pivots]
    d = len(free)
    need(proof["rank"] == len(pivots) == m - d and proof["free_original_coordinates"] == free
         and proof["pivot_columns"] == pivots and proof["dimension_bound"] == d, "Wrong chart rank or literal free selection")
    if expected_dimension is not None:
        need(d == expected_dimension, "Computed rank differs from accepted forced-mask bound")
    offset, basis = proof["offset"], proof["basis_rows"]
    need(len(offset) == len(basis) == m and all(len(row) == d for row in basis)
         and all(type(x) is int for x in offset + [x for row in basis for x in row]), "Nonintegral chart offset or inverse")
    need(proof["rref_augmented"] == [[str(x) for x in row] for row in matrix], "Changed exact rational row reduction")
    for j, k in enumerate(free):
        need(offset[k] == 0 and basis[k] == [int(i == j) for i in range(d)], "No literal integer free-coordinate selection inverse")
    transformed = substitute(rows, offset, basis)
    need(all(not any(transformed[i]) for i in forced), "Chart fails an original forced equation")
    need(transformed == proof["substituted_original_rows"], "An original inequality was omitted or changed by substitution")
    # Full rank of E and the literal coordinate inverse prove that this is
    # the entire affine solution lattice, not just an integer sublattice.
    return d


def derive_chart(rows, closed_mask, expected_dimension=None):
    need(rows and all(len(row) == len(rows[0]) and all(type(x) is int for x in row) for row in rows), "Original rows must be a full exact integer matrix")
    need(type(closed_mask) is int and 0 <= closed_mask < 1 << len(rows), "Invalid forced mask")
    m = len(rows[0]) - 1
    forced = [i for i in range(len(rows)) if closed_mask >> i & 1]
    reduced, pivots = rref_equations([rows[i][1:] + [-rows[i][0]] for i in forced], m)
    free = [j for j in range(m) if j not in pivots]
    offset = [Q(0)] * m
    basis = [[Q(int(k == j)) for j in free] for k in range(m)]
    for row, col in enumerate(pivots):
        offset[col] = reduced[row][-1]
        basis[col] = [-reduced[row][j] for j in free]
    need(all(x.denominator == 1 for x in offset + [x for row in basis for x in row]), "RREF does not give an integral offset/basis with literal free-coordinate inverse")
    offset = [int(x) for x in offset]
    basis = [[int(x) for x in row] for row in basis]
    proof = {"closed_rows_mask": closed_mask, "forced_row_indices": forced, "forced_original_rows": [rows[i] for i in forced],
             "rank": len(pivots), "dimension_bound": len(free), "pivot_columns": pivots,
             "rref_augmented": [[str(x) for x in row] for row in reduced], "offset": offset, "basis_rows": basis,
             "free_original_coordinates": free, "substituted_original_rows": substitute(rows, offset, basis),
             "actual_dimension": None, "lattice": "All integer solutions, with z_j equal to the selected original h coordinate"}
    verify_chart(rows, closed_mask, proof, expected_dimension)
    return proof


def canonical_mask(table, rank, mask):
    count = 1 << (3 * (rank - 1))
    need(table["rank"] == rank and table["start"] == 0 and table["stop"] == count
         and len(table["records"]) == count and 0 <= mask < count, "Accepted mask table identity or full roster changed")
    record = table["records"][mask]
    need(type(record["mask"]) is int and record["mask"] == mask and type(record["dimension_bound"]) is int
         and 0 <= record["dimension_bound"] <= (rank - 1) * (rank - 2) // 2, "Wrong selected canonical boundary mask")
    return record


def polynomial(coefficients, node):
    value = Q(0)
    for coefficient in reversed(coefficients):
        value = value * node + coefficient
    return value


def choose_nodes(raw, declared_degree, bound):
    coefficients = list(map(rational, raw))
    need(coefficients and len(coefficients) == integer(declared_degree) + 1 and coefficients[-1] != 0,
         "Incomplete source vector or false declared source degree")
    need(all(x >= 0 for x in coefficients), "Primary ordinary-negative source must pass the candidate gate first")
    need(coefficients[0] == 1 and 0 <= declared_degree <= bound, "Source degree exceeds the proved bound or constant is not one")
    def expected(node, parity=False):
        value = polynomial(coefficients, node) * ((-1) ** bound if parity else 1)
        need(value.denominator == 1 and value >= 0, "A requested physical count is fractional or negative")
        return value.numerator
    if bound > declared_degree:
        sites = list(range(1, bound + 1))
        holds = [bound + 1, bound + 2]
        plan = {"mode": "closed_only", "dimension_bound": bound, "actual_dimension": None,
                "dimension_anchor": None, "determining_nodes": [0] + sites, "unused_positive_grades": holds,
                "reciprocity_allowed_without_fresh_anchor": False, "cost_pool": []}
        values = {k: expected(k) for k in sites + holds}
    else:
        pool = []
        anchor = None
        for q in range(1, bound + 2):
            value = (-1) ** bound * polynomial(coefficients, -q)
            eligible = value.denominator == 1 and value >= 0
            pool.append({"signed_node": -q, "physical_count_heuristic": str(value), "eligible": eligible})
            if anchor is None and value > 0:
                need(eligible, "First tentative positive anchor has a noninteger source expectation")
                anchor = -q
        need(anchor is not None, "No tentative strict anchor in the root-authorized grade interval")
        for q in range(3, bound + 3):
            value = polynomial(coefficients, q)
            pool.append({"signed_node": q, "physical_count_heuristic": str(value),
                         "eligible": value.denominator == 1 and value >= 0})
        available = [p for p in pool if p["eligible"]]
        available.sort(key=lambda p: (rational(p["physical_count_heuristic"]), abs(p["signed_node"]), p["signed_node"] > 0, p["signed_node"]))
        need(len(available) >= bound, "Insufficient exact nonnegative heuristic sites")
        sites = [p["signed_node"] for p in available[:bound]]
        holds = [1, 2]
        plan = {"mode": "mixed_pending_positive_anchor", "dimension_bound": bound, "actual_dimension": None,
                "dimension_anchor": {"signed_node": anchor, "kind": f"I{-anchor}", "grade": -anchor,
                                     "requires_fresh_complete_count_strictly_positive": True,
                                     "source_expectation_is_not_dimension_evidence": True},
                "determining_nodes": [0] + sites, "unused_positive_grades": holds,
                "reciprocity_allowed_without_fresh_anchor": False, "cost_pool": pool,
                "choice_rule": "Increasing exact expected physical count, then grade, then signed node; source values are a cost heuristic only"}
        values = {k: expected(k, k < 0) for k in set(sites + holds + [anchor])}
    need(len(plan["determining_nodes"]) == bound + 1 and len(set(plan["determining_nodes"])) == bound + 1
         and not set(plan["determining_nodes"]) & set(holds), "Determining and held polynomial nodes overlap")
    order = ([plan["dimension_anchor"]["signed_node"]] if plan["dimension_anchor"] else []) + sites + holds
    nodes = []
    for signed in dict.fromkeys(order):
        roles = []
        if signed in sites:
            roles.append("determining")
        if signed in holds:
            roles.append("positive_holdout")
        if plan["dimension_anchor"] and signed == plan["dimension_anchor"]["signed_node"]:
            roles.append("dimension_anchor")
        nodes.append({"kind": ("I" if signed < 0 else "P") + str(abs(signed)), "grade": abs(signed), "strict": signed < 0,
                      "signed_polynomial_node": signed, "stored": {"source_polynomial": values[signed]},
                      "role": "+".join(roles), "roles": roles,
                      "expected_value_provenance": "One unaccepted source polynomial, used for cost selection and later comparison only",
                      "true_interior_interpretation": "PENDING_FRESH_POSITIVE_ANCHOR" if signed < 0 else "closed_count"})
    plan["known_zero_value"] = 1
    plan["zero_node_is_a_known_value_not_a_count_request"] = True
    return plan, nodes


def node_system(job, node):
    m, grade, strict = job["model"], integer(node["grade"]), node["strict"]
    need(type(strict) is bool and grade > 0, "Illegal physical count node")
    need(len(m["unit_selections"]) == m["dimension"] and all(len(row) == m["dimension"] + 1 for row in m["full_rows"]),
         "Incomplete variable bounds or full-row dimensions")
    bounds = []
    for j, selection in enumerate(m["unit_selections"]):
        need(selection["variable"] == j and selection["unit_row"] == [int(k == j) for k in range(m["dimension"])], "Changed literal bound inverse")
        bounds.append([-grade * selection["base"], grade * (m["count_boundary_area"] - selection["base"])])
    rows = [[grade * row[0] - int(strict and any(row[1:])), *row[1:]] for row in m["full_rows"]]
    return bounds, rows


def fresh_count(job, row):
    expected = {node["kind"]: node for node in job["nodes"]}
    kind = row["kind"]
    need(kind in expected, "Unexpected fresh physical node")
    node = expected[kind]
    bounds, system = node_system(job, node)
    response = row["counter"]
    integer(row["id"])
    integer(row["grade"])
    need(type(row["strict"]) is bool and row["id"] == job["id"]
         and row["node_id"] == response["id"] == f"LEGACY:{job['id']}:{kind}"
         and row["geometry_sha256"] == job["geometry_sha256"] and row["grade"] == node["grade"]
         and row["strict"] == node["strict"] and row["full_system_sha256"] == sha(encoded({"bounds": bounds, "rows": system}))
         and response["status"] == "complete", "Fresh result is not a complete count of this exact full system")
    value = rational(response["count"])
    need(value.denominator == 1 and value >= 0, "A refused, fractional or negative count cannot establish a dimension")
    return kind, value.numerator


def verified_dimension_anchor(job, count_row):
    """A single independently authenticated anchor can establish dimension.

    Source agreement is unnecessary for this geometric fact: an unexpected
    positive count still proves dimension while falsifying the old expectation.
    """
    plan = job["node_plan"]
    need(plan["mode"] == "mixed_pending_positive_anchor" and plan["dimension_bound"] == job["model"]["dimension"],
         "This plan cannot use a strict anchor to supply parity")
    anchor = plan["dimension_anchor"]
    need(anchor and count_row["kind"] == anchor["kind"] and count_row["strict"] is True,
         "Wrong dimension anchor identity")
    kind, count = fresh_count(job, count_row)
    need(count > 0, "Actual dimension and true-interior parity remain unproved: no fresh positive strict anchor")
    return {"actual_dimension": plan["dimension_bound"], "anchor_node_id": count_row["node_id"],
            "anchor_count": str(count), "source_expectation_used_as_proof": False}


def verified_interpolation_samples(job, count_rows):
    """Gate for the owner after independently authenticating count receipts.

    Returns exact samples and holds, not a publication or source-vector
    acceptance. The owner still compares the entire reconstructed vector.
    Hidden actual dimension can never silently supply the chart-bound parity.
    """
    plan = job["node_plan"]
    expected = {node["kind"]: node for node in job["nodes"]}
    fresh, raw_rows = {}, {}
    for row in count_rows:
        kind = row["kind"]
        need(kind in expected and kind not in fresh, "Missing/extra/duplicate fresh physical node")
        _, fresh[kind] = fresh_count(job, row)
        raw_rows[kind] = row
    need(set(fresh) == set(expected), "Fresh physical-node roster is incomplete")
    d = plan["dimension_bound"]
    actual = None
    if plan["mode"] == "mixed_pending_positive_anchor":
        anchor = plan["dimension_anchor"]
        actual = verified_dimension_anchor(job, raw_rows[anchor["kind"]])["actual_dimension"]
    else:
        need(plan["mode"] == "closed_only" and plan["dimension_anchor"] is None and not any(n["strict"] for n in expected.values()),
             "A hidden-dimension closed-only plan attempted strict-interior parity")
    samples = [[0, "1"]]
    for signed in plan["determining_nodes"][1:]:
        need(signed >= 0 or actual == d, "Unknown actual dimension cannot supply reciprocity parity")
        kind = ("I" if signed < 0 else "P") + str(abs(signed))
        value = fresh[kind] * ((-1) ** actual if signed < 0 else 1)
        samples.append([signed, str(value)])
    need(any(value > 0 for value in fresh.values()), "Nonemptiness required for the known constant has no fresh witness")
    return {"status": "INTERPOLATION_SAMPLES_GATED", "actual_dimension": actual, "degree_upper_bound": d,
            "samples": samples, "unused_holds": [[t, str(fresh[f"P{t}"])] for t in plan["unused_positive_grades"]],
            "source_vector_accepted": False, "required_remaining_gate": "Reconstruct the full degree-at-most-d vector; preserve primary negatives before comparison; compare every source coefficient and unused hold."}


class SourceDocuments:
    def __init__(self, catalog, deadline):
        self.catalog, self.deadline, self.used, self.documents = {}, deadline, {}, {}
        for value in catalog:
            need(value["path"] not in self.catalog or self.catalog[value["path"]] == value, "Conflicting frozen source pins")
            self.catalog[value["path"]] = value

    def get(self, reference):
        identity = {k: reference[k] for k in ("path", "bytes", "sha256")}
        path = Path(identity["path"]).resolve()
        need(str(path) == identity["path"] and (path.is_relative_to(C) or path.is_relative_to(W)), "Source pointer escaped its exact approved roots")
        need(self.catalog.get(identity["path"]) == identity, "Source pointer lacks its original metadata binding")
        if identity["path"] not in self.documents:
            self.deadline.check()
            need(pin(path, self.deadline) == identity, "Changed exact source bytes")
            self.used[identity["path"]] = identity
            self.documents[identity["path"]] = decode(path.read_bytes())
        return self.documents[identity["path"]]

    def verify_after(self):
        for value in self.used.values():
            need(pin(value["path"]) == value, "An accessed source changed during indexing")


def validate_selection(document, expected_total=297, tail_ids=TAIL_IDS):
    need(document["schema"] == "legacy-adopted-source-vectors-v1" and document["status"] == "SOURCE_VECTORS_EXTRACTED_UNACCEPTED"
         and document.get("source_vector_acceptance_asserted") is False, "Wrong or silently accepted source-vector metadata")
    records = document["records"]
    need(len(records) == expected_total and [integer(r["id"]) for r in records] == list(range(expected_total))
         and document["expected_record_ids"] == list(range(expected_total)), "Missing, extra, reordered or duplicate source ID")
    terminals = [r["terminal_id"] for r in records]
    need(all(isinstance(x, str) and x for x in terminals) and len(set(terminals)) == expected_total
         and terminals == document["expected_terminal_ids"], "Literal terminal roster differs")
    need(all(r.get("source_vector_accepted") is False and r["status"] == "SOURCE_VECTOR_UNACCEPTED_PENDING_FRESH_RECOUNT" for r in records),
         "A missing or accepted source vector was silently substituted")
    need(list(tail_ids) == sorted(set(tail_ids)) and set(tail_ids) <= set(range(expected_total)), "Invalid exact tail selection")
    return [records[i] for i in tail_ids]


def validate_source_record(record, sources, chosen):
    ref = record["vector_reference"]
    document = sources.get(ref)
    need(pointer(document, ref["json_pointer"]) == record["coefficients_low_to_high"], "Vector differs from its exact original source pointer")
    body = pointer(document, ref["record_pointer"])
    need(sha(encoded(body)) == ref["record_sha256"], "Original source record hash changed")
    tref = record["triple_reference"]
    need(triple(pointer(sources.get(tref), tref["json_pointer"])) == record["bare_triple"], "Original bare triple pointer differs")
    binding = bind_triples(record["bare_triple"], record["terminal_source_triple"])
    need(binding == record["source_to_terminal_binding"], "Source-to-terminal transport changed")
    need(chosen["terminal_id"] == record["terminal_id"] and chosen["source_id"] == record["source_id"]
         and chosen["family"] == record["family"] and chosen["seed_key"] == record["chosen_seed_key"]
         and triple(chosen["source_triple"]) == record["terminal_source_triple"], "Selected terminal/source identity differs")
    if record.get("adopted_disposition_reference"):
        reference = record["adopted_disposition_reference"]
        disposition = pointer(sources.get(reference), reference["json_pointer"])
        need(disposition["id"] == record["source_id"] and triple(disposition["canonical_identity"]) == record["terminal_source_triple"],
             "Old disposition binds a different full terminal")


def validate_alternate_vectors(record, sources):
    for alternate in record.get("additional_vector_sources", []):
        reference = record["vector_reference"] if alternate.get("same_source_file") else alternate
        source = sources.get(reference)
        need(pointer(source, alternate["json_pointer"]) == record["coefficients_low_to_high"], "Conflicting additional source vector")


def make_job(record, original, accepted_record, accepted_reference):
    bare = triple(record["bare_triple"])
    binding = bind_triples(bare, record["terminal_source_triple"])
    need(binding == record["source_to_terminal_binding"], "Source-to-terminal identity changed")
    need(accepted_record["mask"] == original["boundary_mask"], "Wrong boundary equality mask selected")
    proof = derive_chart(original["rows"], accepted_record["closed_rows_mask"], accepted_record["dimension_bound"])
    d, free = proof["dimension_bound"], proof["free_original_coordinates"]
    plan, nodes = choose_nodes(record["coefficients_low_to_high"], record["source_declared_degree"], d)
    model = {"rank": original["rank"], "dimension": d, "count_boundary_area": original["count_boundary_area"],
             "full_rows": proof["substituted_original_rows"],
             "unit_selections": [{"variable": j, "original_hive_coordinate": k, "base": proof["offset"][k],
                                  "unit_row": proof["basis_rows"][k]} for j, k in enumerate(free)],
             "dimension_is_chart_upper_bound": True, "actual_dimension_established": False,
             "geometry_premise": "Complete ordinary hive; accepted F025 forced equations; saturated chart with literal original-coordinate inverse; 0 <= h <= t*sum(lambda)."}
    geometry = {"original": original, "accepted_forcing": accepted_record, "accepted_reference": accepted_reference,
                "chart": proof, "stretch_chart": "h = t*offset + basis*z; z_j is the literal free original hive coordinate"}
    return {"unit": "LEGACY", "id": record["id"], "terminal_id": record["terminal_id"], "source_id": record["source_id"],
            "bare_triple": bare, "terminal_source_triple": record["terminal_source_triple"], "source_to_terminal_binding": binding,
            "geometry_sha256": sha(encoded({"bare_triple": bare, "geometry": geometry})),
            "geometry_reference": {"kind": "fresh_original_hive_and_accepted_forced_chart", "mask_reference": accepted_reference,
                                   "source_triple_reference": record["triple_reference"]},
            "chart_proof": geometry, "certificate_reference": record["vector_reference"],
            "source_coefficients_low_to_high": record["coefficients_low_to_high"], "source_declared_degree": record["source_declared_degree"],
            "original_execution_identity": record["original_execution_identity"], "original_source_record": record,
            "model": model, "nodes": nodes, "node_plan": plan, "actual_dimension": None, "degree_upper_bound": d,
            "geometry_acceptance": "SATURATED_FORCED_CHART_BOUND; TRUE_INTERIOR_AND_PARITY_PENDING_FRESH_POSITIVE_ANCHOR" if plan["dimension_anchor"]
                                   else "SATURATED_FORCED_CHART_BOUND; CLOSED_ONLY_INTERPOLATION; ACTUAL_DIMENSION_NOT_CLAIMED",
            "source_vector_accepted": False,
            "theorem_acceptance_gate": "verified_interpolation_samples requires all exact physical counts and a positive strict anchor before any negative-node parity; then reconstruct and compare the entire vector and unused holds."}


def source_negative_gate(record, candidate_path):
    coefficients = list(map(rational, record["coefficients_low_to_high"]))
    need(coefficients, "Missing complete source vector")
    negative = [i for i, value in enumerate(coefficients) if value < 0]
    if negative:
        save(candidate_path, {"schema": "legacy-primary-LR-negative-observation-v1", "status": "HOLD_PENDING_FRESH_INDEPENDENT_COUNTS",
                              "terminal_id": record["terminal_id"], "bare_triple": record["bare_triple"],
                              "coefficients_low_to_high": record["coefficients_low_to_high"], "negative_indices": negative,
                              "source": record["vector_reference"], "captured_before_chart_construction_or_count_comparisons": True})
        return False
    return True


def index_jobs(args):
    deadline = Deadline(args.budget_seconds)
    output, input_path, consumer = args.output.resolve(), args.input.resolve(), args.wrapper.resolve()
    need(output.parent.is_dir() and not output.exists() and output.is_relative_to(W)
         and not output.is_relative_to(input_path.parent), "Fresh outputs must be in the owner session outside the source metadata tree")
    need(consumer == W / "recount_records.py", "Use only the unchanged named recount consumer")
    need(272 <= args.start < args.stop <= 297, "Only root-selected tail IDs 272..296 are authorized")
    source_pin = pin(input_path, deadline)
    need(source_pin["sha256"] == SOURCE_SHA, "Legacy source map changed from the exact root-selected version")
    document = decode(input_path.read_bytes())
    tail = validate_selection(document)
    sources = SourceDocuments(document["inputs"], deadline)
    selection = sources.get(document["selection_reference"])
    choices = [r for r in selection["choices"] if r["family"] in ("FRE", "FRI-settled")]
    by_terminal = {r["terminal_id"]: r for r in choices}
    need(len(choices) == len(by_terminal) == 297 and set(by_terminal) == set(document["expected_terminal_ids"]), "Chosen whole-terminal roster differs")
    tables, mask_pins = {}, {}
    for rank, path in MASK_PATHS.items():
        value = pin(path, deadline)
        need(value["sha256"] == MASK_SHA[rank], "Canonical accepted F025 source changed")
        mask_pins[rank] = value
        tables[rank] = decode(path.read_bytes())
    creator, required_consumer = pin(__file__, deadline), pin(consumer, deadline)
    required_counter = pin(W / "v2_independent_hive_recount.cpp", deadline)
    required_harness = pin(W / "run_check.py", deadline)
    jobs_path = output.with_suffix(".jobs.jsonl")
    need(not jobs_path.exists(), "Refusing to replace old or partial tail jobs")
    result = {"schema": SCHEMA, "kind": "manifest", "status": "PARTIAL", "unit": "LEGACY",
              "stream": "legacy-source-272-296-saturated-forced-charts-v1", "input_root": str(input_path.parent),
              "expected_record_ids": list(TAIL_IDS), "expected_terminal_ids": [r["terminal_id"] for r in tail],
              "terminal_id_mapping": [{"id": r["id"], "terminal_id": r["terminal_id"], "source_id": r["source_id"]} for r in tail],
              "source_id_interval": [args.start, args.stop], "records": [], "selection_complete": True, "index_complete": False,
              "pending_index_ids": list(TAIL_IDS), "wrapper_sha256": required_consumer["sha256"], "required_consumer": required_consumer,
              "required_counter_source": required_counter, "required_harness": required_harness,
              "forcing_sources": {str(n): p for n, p in mask_pins.items()},
              "indexer": {**creator, "command": "index", "argv": list(sys.argv)}, "source_metadata": source_pin,
              "source_vectors_accepted": False, "actual_dimensions_asserted": False, "lattice_counts_performed": 0,
              "prefix_integration": {"excluded_source_ids": list(range(272)), "separate_owner_gate": "Join the independently verified prefix 0..271 and this exact tail by terminal identity; no old attempted tail count is reused."},
              "classical_premises": ["Complete ordinary hive/LR identity with lambda outer and nonnegative tableau-row coordinate bounds",
                                      "Already accepted F025 original-rhombus forced-mask implications",
                                      "Period-one LR stretching with degree at most the proved affine chart dimension",
                                      "Relative-interior reciprocity uses actual dimension, established only by a fresh positive strict anchor"]}
    seen = set()
    try:
        with jobs_path.open("xb") as stream:
            for record in tail:
                if not args.start <= record["id"] < args.stop:
                    continue
                deadline.check()
                validate_source_record(record, sources, by_terminal[record["terminal_id"]])
                candidate_path = output.with_suffix(".candidate.json")
                if not source_negative_gate(record, candidate_path):
                    result.update(status="HOLD_CANDIDATE", candidate=pin(candidate_path))
                    break
                validate_alternate_vectors(record, sources)
                original = original_hive(record["bare_triple"])
                rank, mask = original["rank"], original["boundary_mask"]
                need(rank in (6, 7), "Tail original rank is outside the two accepted F025 tables")
                accepted = canonical_mask(tables[rank], rank, mask)
                reference = {**mask_pins[rank], "json_pointer": f"/records/{mask}", "record_sha256": sha(encoded(accepted))}
                job = make_job(record, original, accepted, reference)
                need(job["id"] not in seen, "Duplicate tail job identity")
                raw = encoded(job) + b"\n"
                offset = stream.tell()
                stream.write(raw)
                stream.flush()
                seen.add(job["id"])
                result["records"].append({"ordinal": len(result["records"]), "id": job["id"], "geometry_sha256": job["geometry_sha256"],
                                          "offset": offset, "bytes": len(raw), "sha256": sha(raw),
                                          "node_ids": [f"LEGACY:{job['id']}:{node['kind']}" for node in job["nodes"]]})
            os.fsync(stream.fileno())
        if result["status"] != "HOLD_CANDIDATE":
            result["index_complete"] = seen == set(TAIL_IDS)
            result["status"] = "FROZEN_RECOUNT_JOBS" if result["index_complete"] else "PARTIAL"
    except DeadlineReached as error:
        result["interruption"] = str(error)
    except (CheckError, KeyError, ValueError, OSError, IndexError) as error:
        result.update(status="FAIL", error=f"{type(error).__name__}: {error}")
    finally:
        all_inputs = [source_pin, required_consumer, required_counter, required_harness, creator, *mask_pins.values(), *sources.used.values()]
        try:
            for value in all_inputs:
                need(pin(value["path"]) == value, "A frozen source changed during chart construction")
            result["source_bytes_verified_before_after"] = True
        except (CheckError, OSError) as error:
            result.update(status="FAIL", source_bytes_verified_before_after=False, source_error=str(error))
        result["pending_index_ids"] = sorted(set(TAIL_IDS) - seen)
        result["jobs"] = pin(jobs_path)
        result["inputs"] = list({value["path"]: value for value in all_inputs}.values())
        save(output, result)
    return result


def interpolate(samples):
    """Exact Lagrange expansion of the complete gated determining roster."""
    need(samples and len({x for x, _ in samples}) == len(samples), "Repeated or absent determining node")
    result = [Q(0)] * len(samples)
    for x, value in samples:
        term, denominator = [rational(value)], 1
        for other, _ in samples:
            if other == x:
                continue
            multiplied = [Q(0)] * (len(term) + 1)
            for k, coefficient in enumerate(term):
                multiplied[k] -= other * coefficient
                multiplied[k + 1] += coefficient
            term = multiplied
            denominator *= x - other
        for k, coefficient in enumerate(term):
            result[k] += coefficient / denominator
    return result


def check_count_receipt(path, report, manifest, manifest_pin):
    folder = Path(path).resolve().parent
    receipt = decode((folder / "receipt.json").read_bytes())
    config = decode((folder / "config.json").read_bytes())
    launch = decode((folder / "launch.json").read_bytes())
    need(receipt["cleanup_verified"] is True and receipt["source_input_bytes_unchanged"] is True
         and type(receipt["returncode"]) is int and type(receipt["pid"]) is int and receipt["pid"] > 0
         and receipt["pid"] == launch["pid"] == launch["pgid"] and receipt["id"] == config["id"] == folder.name,
         "Missing clean, stable actual child exit")
    code = {"SLICE_RECOUNTS_MATCH": 0, "PARTIAL": 2, "COUNT_MISMATCH": 1}[report["status"]]
    need(receipt["returncode"] == code and receipt["state"] == ("complete" if code == 0 else "invalid_input_or_output"),
         "A failed launch cannot supply a complete recount")
    need(config["sources"].get(manifest["required_consumer"]["path"]) == manifest["wrapper_sha256"]
         and config["sources"].get(manifest["required_harness"]["path"]) == manifest["required_harness"]["sha256"]
         and config["inputs"].get(manifest_pin["path"]) == manifest_pin["sha256"], "Count launch lacks exact consumer, harness or manifest provenance")
    need(config["argv"][1:4] == ["-B", manifest["required_consumer"]["path"], "run"]
         and config["argv"][-2:] == ["--output", str(Path(path).resolve())]
         and config["declared_output_root"] == str(folder) and config["arm"] == "algebra"
         and config["native_calls"] == 0 and 0 < config["deadline_seconds"] <= 120, "Wrong scientific count launch command or ownership")
    for value in (pin(path), report["results"]):
        need(Path(value["path"]).parent == folder and receipt["outputs"].get(Path(value["path"]).name) == value["sha256"], "Unreceipted raw count output")
    return {"receipt": pin(folder / "receipt.json"), "launch": pin(folder / "launch.json"), "config": pin(folder / "config.json")}


def load_count_rows(paths, jobs, entries, manifest, mp, deadline):
    expected = {f"LEGACY:{job['id']}:{node['kind']}": (job, node) for job in jobs.values() for node in job["nodes"]}
    complete, evidence, seen_paths = {}, [], set()
    build_identity = None
    for path in paths:
        deadline.check()
        report_pin = pin(path, deadline)
        need(report_pin["path"] not in seen_paths, "Duplicate count report")
        seen_paths.add(report_pin["path"])
        report = decode(Path(path).read_bytes())
        need(report["schema"] == SCHEMA and report["kind"] == "run" and report["manifest_sha256"] == mp["sha256"]
             and report["wrapper_sha256"] == manifest["wrapper_sha256"]
             and report["status"] in ("SLICE_RECOUNTS_MATCH", "PARTIAL", "COUNT_MISMATCH"), "Wrong, stale or failed recount report")
        custody = check_count_receipt(path, report, manifest, mp)
        build_pin = report["build_reference"]
        need(pin(build_pin["path"], deadline) == build_pin, "Build receipt changed")
        if build_identity is None:
            build_identity = build_pin
        need(build_identity == build_pin, "Tail reports mix different frozen builds")
        build = decode(Path(build_pin["path"]).read_bytes())
        need(build["schema"] == SCHEMA and build["kind"] == "build" and build["status"] == "BUILT_OWN_COUNTER"
             and build["wrapper_sha256"] == manifest["wrapper_sha256"] and build["source"] == report["counter_source"] == manifest["required_counter_source"]
             and build["binary"] == report["build"] and pin(build["binary"]["path"], deadline) == build["binary"], "Counter source/binary identity changed")
        need(pin(report["results"]["path"], deadline) == report["results"], "Raw count ledger changed")
        with Path(report["results"]["path"]).open("rb") as stream:
            for raw in stream:
                deadline.check()
                row = decode(raw)
                nid = row["node_id"]
                need(nid in expected, "Count report contains an extra or unindexed physical node")
                job, node = expected[nid]
                bounds, system = node_system(job, node)
                need(row["record_ordinal"] == entries[job["id"]]["ordinal"] and row["id"] == job["id"]
                     and row["kind"] == node["kind"] and row["grade"] == node["grade"] and row["strict"] == node["strict"]
                     and row["geometry_sha256"] == job["geometry_sha256"] and row["stored"] == node["stored"]
                     and row["counter"]["id"] == nid and row["full_system_sha256"] == sha(encoded({"bounds": bounds, "rows": system})),
                     "Count/source/full-system identity changed")
                if row["counter"]["status"] == "complete":
                    _, value = fresh_count(job, row)
                    agrees = all(value == wanted for wanted in node["stored"].values())
                    need(row["status"] == ("MATCH" if agrees else "MISMATCH") and nid not in complete,
                         "False status or duplicate successful count, including agreeing repetitions")
                    complete[nid] = row
                else:
                    need(row["status"] == "REFUSED" and row["counter"]["status"].startswith("REFUSED_")
                         and row["counter"].get("count") is None, "A refusal supplied a partial count")
        need(pin(report["results"]["path"]) == report["results"] and pin(path) == report_pin, "Count evidence changed while reading")
        evidence.append({"report": report_pin, "results": report["results"], "build": build_pin,
                         "binary": build["binary"], "counter_source": build["source"], **custody})
    return complete, sorted(set(expected) - set(complete)), evidence


def accept_jobs(args):
    deadline = Deadline(args.budget_seconds)
    output = args.output.resolve()
    need(output.parent.is_dir() and not output.exists() and output.is_relative_to(W), "Fresh acceptance output must be in the owner session")
    mp = pin(args.manifest, deadline)
    manifest = decode(Path(args.manifest).read_bytes())
    need(manifest["schema"] == SCHEMA and manifest["kind"] == "manifest" and manifest["status"] == "FROZEN_RECOUNT_JOBS"
         and manifest["selection_complete"] is True and manifest["index_complete"] is True and not manifest["pending_index_ids"]
         and manifest["expected_record_ids"] == list(TAIL_IDS) and manifest["source_bytes_verified_before_after"] is True,
         "Acceptance requires the complete exact 25-terminal index")
    need({k: manifest["indexer"][k] for k in ("path", "bytes", "sha256")} == pin(__file__, deadline)
         and manifest["required_consumer"] == pin(W / "recount_records.py", deadline)
         and manifest["required_counter_source"] == pin(W / "v2_independent_hive_recount.cpp", deadline)
         and manifest["required_harness"] == pin(W / "run_check.py", deadline), "Generator/consumer/counter/harness version changed")
    for value in manifest["inputs"]:
        need(pin(value["path"], deadline) == value, "A frozen index input changed")
    need(manifest["source_metadata"]["sha256"] == SOURCE_SHA
         and pin(manifest["source_metadata"]["path"], deadline) == manifest["source_metadata"], "Wrong legacy selection source version")
    source_document = decode(Path(manifest["source_metadata"]["path"]).read_bytes())
    tail = {r["id"]: r for r in validate_selection(source_document)}
    need(manifest["expected_terminal_ids"] == [tail[i]["terminal_id"] for i in TAIL_IDS], "Exact tail terminal roster differs")
    source_documents = SourceDocuments(source_document["inputs"], deadline)
    selection = source_documents.get(source_document["selection_reference"])
    choices = [r for r in selection["choices"] if r["family"] in ("FRE", "FRI-settled")]
    chosen = {r["terminal_id"]: r for r in choices}
    need(len(chosen) == len(choices) == 297 and set(chosen) == set(source_document["expected_terminal_ids"]), "Old full terminal selection changed")
    for n in MASK_PATHS:
        need(pin(MASK_PATHS[n], deadline) == manifest["forcing_sources"][str(n)]
             and manifest["forcing_sources"][str(n)]["sha256"] == MASK_SHA[n], "Canonical forcing bytes changed")
    tables = {n: decode(MASK_PATHS[n].read_bytes()) for n in MASK_PATHS}
    need(pin(manifest["jobs"]["path"], deadline) == manifest["jobs"], "Frozen chart/job bytes changed")
    jobs, entries, offset = {}, {}, 0
    with Path(manifest["jobs"]["path"]).open("rb") as stream:
        for ordinal, entry in enumerate(manifest["records"]):
            deadline.check()
            need(entry["ordinal"] == ordinal and entry["offset"] == offset and entry["id"] in tail and entry["id"] not in jobs,
                 "Duplicate, extra or missing job ordinal")
            raw = stream.read(entry["bytes"])
            offset += entry["bytes"]
            need(sha(raw) == entry["sha256"], "Frozen job content differs")
            job = decode(raw)
            validate_source_record(tail[entry["id"]], source_documents, chosen[tail[entry["id"]]["terminal_id"]])
            validate_alternate_vectors(tail[entry["id"]], source_documents)
            original = original_hive(tail[entry["id"]]["bare_triple"])
            n, mask = original["rank"], original["boundary_mask"]
            accepted = canonical_mask(tables[n], n, mask)
            reference = {**manifest["forcing_sources"][str(n)], "json_pointer": f"/records/{mask}", "record_sha256": sha(encoded(accepted))}
            need(reference["sha256"] == MASK_SHA[n] and reference["path"] == str(MASK_PATHS[n]), "Wrong accepted forcing premise")
            expected = make_job(tail[entry["id"]], original, accepted, reference)
            need(job == expected and job["id"] == entry["id"] and job["geometry_sha256"] == entry["geometry_sha256"]
                 and entry["node_ids"] == [f"LEGACY:{job['id']}:{node['kind']}" for node in job["nodes"]], "Original/chart/node-plan/source identity changed")
            jobs[job["id"]], entries[job["id"]] = job, entry
    need(set(jobs) == set(TAIL_IDS) and offset == manifest["jobs"]["bytes"], "Frozen index omits or adds tail identities")
    result = {"schema": "legacy-tail-polynomial-acceptance-v1", "status": "PARTIAL", "manifest": mp,
              "expected_terminal_ids": manifest["expected_terminal_ids"], "expected_record_ids": list(TAIL_IDS),
              "classical_premises": manifest["classical_premises"],
              "accepted": [], "pending_record_ids": list(TAIL_IDS), "dimension_observations": [], "source_vectors_accepted": False}
    raw_path = output.with_suffix(".reconstructed.jsonl")
    try:
        complete, missing, evidence = load_count_rows(args.reports, jobs, entries, manifest, mp, deadline)
        result.update(pending_node_ids=missing, count_evidence=evidence)
        with raw_path.open("xb") as raw_vectors:
            for idx in TAIL_IDS:
                deadline.check()
                job = jobs[idx]
                anchor = job["node_plan"]["dimension_anchor"]
                if anchor and f"LEGACY:{idx}:{anchor['kind']}" in complete:
                    observation = verified_dimension_anchor(job, complete[f"LEGACY:{idx}:{anchor['kind']}"])
                    result["dimension_observations"].append({"id": idx, "terminal_id": job["terminal_id"], **observation})
                needed = [f"LEGACY:{idx}:{node['kind']}" for node in job["nodes"]]
                if not all(nid in complete for nid in needed):
                    continue
                gate = verified_interpolation_samples(job, [complete[nid] for nid in needed])
                vector = interpolate(gate["samples"])
                record = {"id": idx, "terminal_id": job["terminal_id"], "bare_triple": job["bare_triple"],
                          "geometry_sha256": job["geometry_sha256"], "interpolation_gate": gate,
                          "coefficients_through_chart_bound": list(map(str, vector)),
                          "negative_indices": [i for i, value in enumerate(vector) if value < 0],
                          "captured_before_source_vector_and_unused_hold_comparisons": True}
                raw_vectors.write(encoded(record) + b"\n")
                raw_vectors.flush()
                os.fsync(raw_vectors.fileno())
                if record["negative_indices"]:
                    candidate = output.with_suffix(".candidate.json")
                    save(candidate, {"schema": "legacy-primary-LR-negative-observation-v1", "status": "HOLD_PRIMARY_NEGATIVE",
                                     "observation": record, "manifest": mp, "count_evidence": evidence})
                    result.update(status="HOLD_CANDIDATE", candidate=pin(candidate))
                    break
                source = list(map(rational, job["source_coefficients_low_to_high"]))
                need(vector == source + [Q(0)] * (len(vector) - len(source)), "Fresh full polynomial differs from the old unaccepted source vector")
                for grade, value in gate["unused_holds"]:
                    need(polynomial(vector, grade) == rational(value), "A fresh unused hold rejects the reconstructed vector")
                result["accepted"].append({"id": idx, "terminal_id": job["terminal_id"], "geometry_sha256": job["geometry_sha256"],
                                           "source_vector_reference": job["certificate_reference"], "coefficients_low_to_high": list(map(str, source)),
                                           "actual_dimension": gate["actual_dimension"], "chart_degree_upper_bound": job["degree_upper_bound"],
                                           "unused_holds": gate["unused_holds"], "node_ids": needed})
        if result["status"] != "HOLD_CANDIDATE" and len(result["accepted"]) == len(TAIL_IDS):
            result.update(status="COMPLETE_LEGACY_TAIL_POLYNOMIALS_VERIFIED", source_vectors_accepted=True,
                          theorem_scope="Exactly the 25 bound whole legacy terminals; prefix 0..271 requires its separate owner acceptance")
    except DeadlineReached as error:
        result["interruption"] = str(error)
    except (CheckError, KeyError, ValueError, OSError, IndexError) as error:
        result.update(status="FAIL", error=f"{type(error).__name__}: {error}")
    finally:
        result["pending_record_ids"] = sorted(set(TAIL_IDS) - {r["id"] for r in result["accepted"]})
        if raw_path.exists():
            result["raw_reconstructed_vectors"] = pin(raw_path)
        try:
            count_pins = [value for item in result.get("count_evidence", []) for value in item.values()
                          if isinstance(value, dict) and {"path", "bytes", "sha256"} <= set(value)]
            for value in [mp, manifest["jobs"], manifest["source_metadata"], *manifest["forcing_sources"].values(),
                          *source_documents.used.values(), *manifest["inputs"], *count_pins]:
                need(pin(value["path"]) == value, "Source changed during acceptance")
            result["source_bytes_verified_before_after"] = True
        except (CheckError, OSError) as error:
            result.update(status="FAIL", source_vectors_accepted=False, source_bytes_verified_before_after=False, source_error=str(error))
        save(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("index", "accept"))
    parser.add_argument("--input", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--wrapper", type=Path, default=W / "recount_records.py")
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--reports", type=Path, nargs="*")
    parser.add_argument("--start", type=int, default=272)
    parser.add_argument("--stop", type=int, default=297)
    parser.add_argument("--budget-seconds", type=float, default=90)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        if args.command == "accept":
            need(args.manifest and args.reports, "Acceptance requires the new complete manifest and literal count reports")
            result = accept_jobs(args)
        else:
            result = index_jobs(args)
    except (CheckError, DeadlineReached, KeyError, ValueError, OSError, IndexError) as error:
        # Preflight failures cannot create an apparently usable partial index.
        print(json.dumps({"status": "FAIL", "error": f"{type(error).__name__}: {error}"}), file=sys.stderr)
        return 1
    print(json.dumps({"status": result["status"], "records": len(result.get("records", result.get("accepted", []))),
                      "pending_ids": result.get("pending_index_ids", result.get("pending_record_ids")),
                      "lattice_counts_performed": 0, "elapsed_seconds": round(time.monotonic() - started, 6)}, sort_keys=True))
    return 0 if result["status"] in ("FROZEN_RECOUNT_JOBS", "COMPLETE_LEGACY_TAIL_POLYNOMIALS_VERIFIED") else 2 if result["status"] == "PARTIAL" else 1


if __name__ == "__main__":
    sys.exit(main())
