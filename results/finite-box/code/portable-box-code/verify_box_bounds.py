#!/usr/bin/env python3
"""Freeze and check Pro026's used finite interior-bound premises, without search.

index: select one shard from the complete final unit roster, bind its original
geometry/count lines and all primary/repair proof records, and freeze jobs.
verify: check an exact half-open slice of those jobs under a 100-second cap.
aggregate: require unique complete coverage of the frozen expected identities.
Aggregation additionally requires --accepted-verifier-source and its explicit
--accepted-verifier-sha256. The indexer must be that same accepted source version.
This can name a preserved predecessor: its corpus verification is recorded
separately from the current aggregation source, without rerunning its proofs.

Geometry validity, count-oracle correctness, and protected top-three coefficient
signs remain explicitly separate premises. The index binds their exact source
identities. No returned module is imported, no tree is searched or completed,
and no whole count is inferred from a lower subset or an unfinished branch.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from fractions import Fraction
from functools import lru_cache
import gzip
import hashlib
from itertools import zip_longest
import json
import math
from pathlib import Path, PurePosixPath
import re
import signal
import sys
import time


CERTIFICATES = {
    "U05": "DATA/U05/third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz",
    "U06": "DATA/U06/final-science/UNIFORM-SEPTIC-CERTIFICATES.jsonl.gz",
    "U07": "DATA/U07/final-science/UNIFORM-OCTIC-CERTIFICATES.jsonl.gz",
    "U08": "DATA/U08/final-science-v2/UNIFORM-NONIC-CERTIFICATES.jsonl.gz",
    "U09": "DATA/U09/final-science/COMPACT-CERTIFICATES.jsonl.gz",
    "U10": "DATA/U10/final-science/COMPACT-CERTIFICATES.jsonl.gz",
}
POPULATIONS = {"U05": 154408, "U06": 143401, "U07": 99212, "U08": 51477, "U09": 18424, "U10": 2806}
PROOF_FIELDS = {"lower_slice_proof": "lower", "lower_pair_proof": "pair",
                "additional_upper_cover": "cover", "joint_fiber_proof": "pair"}
PREMISES = ["Complete saturated geometry and actual degree, joined by raw geometry SHA-256",
            "Correctness of the paired numerical counters and their separately checked raw requests",
            "Strict positivity of the top three coefficients under the accepted geometric theorem",
            "Original exhaustive population and count-preserving transport"]
MAX_LINE = 64 * 1024**2
MAX_FILE = 2_000_000_000
MAX_EXPANDED_FILE = 4_000_000_000
SHA = re.compile(r"[0-9a-f]{64}\Z")


class CannotCheck(ValueError):
    """A missing premise or declared resource boundary, never a passing proof."""


def need(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, label="integer"):
    need(type(value) is int, f"Expected exact integer {label}; bool/float prohibited")
    need(value.bit_length() <= 4096, f"Integer magnitude limit: {label}")
    return value


def boolean(value, label):
    need(type(value) is bool, f"Expected boolean {label}")
    return value


def nonnegative(value, label):
    need(integer(value, label) >= 0, f"Negative {label}")
    return value


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def row_digest(rows):
    return digest(json.dumps(rows, separators=(",", ":"), allow_nan=False).encode())


def json_object(data):
    need(len(data) <= MAX_LINE, "JSON record exceeds the fixed size limit")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    def constant(value):
        raise ValueError(f"Nonfinite JSON number: {value}")
    value = json.loads(data, object_pairs_hook=unique, parse_constant=constant)
    need(isinstance(value, dict), "Expected JSON object")
    return value


@contextmanager
def time_cap(seconds=100):
    need(0 < seconds <= 100, "Wall-time cap must be at most 100 seconds")
    def expired(_signum, _frame):
        raise CannotCheck("Internal wall-time cap reached; incomplete work is not verified")
    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def integer_rows(rows, dimension):
    need(isinstance(rows, list) and 0 < len(rows) <= 10000, "Missing/oversized complete row system")
    need(0 < integer(dimension, "dimension") <= 32, "Invalid dimension")
    for row in rows:
        need(isinstance(row, list) and len(row) == dimension + 1, "Incomplete row width")
        for value in row:
            integer(value, "row coefficient")


def proof_binding(rows, proof):
    need(isinstance(proof, dict), "Missing formal proof body")
    n = integer(proof.get("dimension"), "proof dimension")
    integer_rows(rows, n)
    need(proof.get("rows_sha256") == row_digest(rows), "Stale or different complete strict-row geometry")
    return n


def bounds_list(values, dimension, *, finite=False):
    need(isinstance(values, list) and len(values) == dimension, "Endpoint vector dimension mismatch")
    for value in values:
        need(value is not None or not finite, "Finite endpoint not derived")
        if value is not None:
            integer(value, "interval endpoint")
    return values


def index(value, limit, label):
    need(0 <= integer(value, label) < limit, f"Invalid {label}")
    return value


def row_extreme(row, low, high, *, maximum):
    result = row[0]
    for k, coefficient in enumerate(row[1:]):
        if not coefficient:
            continue
        endpoint = high[k] if ((coefficient > 0) == maximum) else low[k]
        need(endpoint is not None, "Row extremum requires an underived endpoint")
        result += coefficient * endpoint
    return result


def check_tree(rows, proof, *, upper_only=False):
    """Replay every node iteratively, with integral exhaustive two-child splits."""
    n = proof_binding(rows, proof)
    nodes = proof.get("nodes")
    need(isinstance(nodes, list) and 0 < len(nodes) <= 1_000_000, "Missing/oversized complete tree")
    seen, totals = set(), {}
    leaves = splits = deductions = 0
    stack = [(0, [None] * n, [None] * n, False)]
    while stack:
        number, low, high, returning = stack.pop()
        index(number, len(nodes), "node identity")
        node = nodes[number]
        need(isinstance(node, dict), "Malformed tree node")
        if returning:
            left, right = node["split"]["children"]
            lower = totals[left][0] + totals[right][0]
            upper = totals[left][1] + totals[right][1]
            own_lower = 0 if upper_only else node["box_lower"]
            need(own_lower <= lower <= upper <= node["box_upper"], "Child aggregate is inconsistent with its parent box")
            totals[number] = (lower, upper)
            continue
        need(number not in seen, "Duplicate, cyclic, or overlapping tree child")
        seen.add(number)
        bounds_list(low, n)
        bounds_list(high, n)
        logs = node.get("deductions")
        need(isinstance(logs, list), "Missing deduction sequence")
        for step in logs:
            need(isinstance(step, list) and len(step) == 4, "Malformed bound deduction")
            row_number, axis, direction, value = step
            row = rows[index(row_number, len(rows), "deduction row")]
            axis = index(axis, n, "deduction coordinate")
            integer(value, "deduced endpoint")
            coefficient, rest = row[axis + 1], row[0]
            for k, other in enumerate(row[1:]):
                if k == axis or not other:
                    continue
                endpoint = high[k] if other > 0 else low[k]
                need(endpoint is not None, "Deduction used an underived coordinate bound")
                rest += other * endpoint
            if direction == "lower":
                need(coefficient > 0 and coefficient * (value - 1) + rest < 0 <= coefficient * value + rest,
                     "Invalid integer lower rounding inequality")
                need(low[axis] is None or value > low[axis], "Lower deduction does not tighten")
                low[axis] = value
            else:
                need(direction == "upper" and coefficient < 0
                     and coefficient * (value + 1) + rest < 0 <= coefficient * value + rest,
                     "Invalid integer upper rounding inequality")
                need(high[axis] is None or value < high[axis], "Upper deduction does not tighten")
                high[axis] = value
            deductions += 1
        bounds_list(node.get("lo"), n)
        bounds_list(node.get("hi"), n)
        need(node["lo"] == low and node["hi"] == high, "Saved endpoints differ from replayed necessary bounds")
        upper = nonnegative(node.get("box_upper"), "node upper cardinality")
        if not upper_only:
            lower = nonnegative(node.get("box_lower"), "node lower cardinality")
            whole = boolean(node.get("wholly_feasible"), "whole-box feasibility")
        need("contradiction" in node, "Missing explicit contradiction disposition")
        contradiction = node["contradiction"]
        if contradiction is not None and contradiction is not False:
            need(isinstance(contradiction, dict) and contradiction, "Malformed contradiction")
            if contradiction.get("type") == "interval":
                axis = index(contradiction.get("coordinate"), n, "contradiction coordinate")
                need(low[axis] is not None and high[axis] is not None and low[axis] > high[axis], "Unproved interval contradiction")
            else:
                need(contradiction.get("type") == "row", "Unknown contradiction rule")
                row = rows[index(contradiction.get("row"), len(rows), "contradiction row")]
                need(row_extreme(row, low, high, maximum=True) < 0, "Unproved row contradiction")
            need(upper == 0 and "split" not in node, "Contradiction has nonzero cardinality or children")
            need(upper_only or (lower == 0 and whole is False), "Contradiction has a feasible lower contribution")
            totals[number] = (0, 0)
            leaves += 1
            continue
        bounds_list(low, n, finite=True)
        bounds_list(high, n, finite=True)
        need(all(a <= b for a, b in zip(low, high)), "Inconsistent box without a contradiction proof")
        need(upper == math.prod(b - a + 1 for a, b in zip(low, high)), "Incorrect whole-box cardinality")
        if upper_only:
            lower = 0
        else:
            feasible = all(row_extreme(row, low, high, maximum=False) >= 0 for row in rows)
            need(whole == feasible and lower == (upper if feasible else 0), "Incorrect wholly feasible lower box")
        if "split" not in node:
            totals[number] = (lower, upper)
            leaves += 1
            continue
        split = node["split"]
        need(isinstance(split, dict), "Malformed split")
        axis = index(split.get("coordinate"), n, "split coordinate")
        middle = integer(split.get("mid"), "split midpoint")
        need(low[axis] <= middle < high[axis], "Split does not partition its integer interval")
        children = split.get("children")
        need(isinstance(children, list) and len(children) == 2, "Missing or extra split child")
        left, right = [index(c, len(nodes), "split child") for c in children]
        need(left != right, "Overlapping duplicate split children")
        left_high, right_low = high.copy(), low.copy()
        left_high[axis], right_low[axis] = middle, middle + 1
        stack.extend([(number, low, high, True), (right, right_low, high.copy(), False),
                      (left, low.copy(), left_high, False)])
        splits += 1
    need(seen == set(range(len(nodes))), "Extra or unreachable tree nodes")
    lower, upper = totals[0]
    need(nonnegative(proof.get("certified_upper"), "certified upper") == upper, "Incorrect complete upper aggregate")
    if upper_only:
        target = integer(proof.get("target_upper"), "target upper")
        expected_met = upper <= target
    else:
        need(nonnegative(proof.get("certified_lower"), "certified lower") == lower, "Incorrect complete lower aggregate")
        target_lower = integer(proof.get("target_lower"), "target lower")
        target_upper = proof.get("target_upper")
        if target_upper is not None:
            integer(target_upper, "target upper")
        expected_met = lower >= target_lower and (target_upper is None or upper <= target_upper)
        need(boolean(proof.get("exact_only_if_bounds_equal"), "equal-endpoint flag") == (lower == upper), "Incorrect equal-endpoint flag")
    need(boolean(proof.get("target_met"), "target result") == expected_met, "Incorrect bound target result")
    return {"interval": [lower, upper], "nodes": len(nodes), "leaves": leaves,
            "splits": splits, "deductions": deductions,
            "all_split_midpoints_and_endpoints_exact_integers": True,
            "all_nodes_and_both_children_checked": True, "whole_count_inferred": False}


def check_lower(rows, proof, *, pair=False):
    n = proof_binding(rows, proof)
    pieces = proof.get("slices")
    need(isinstance(pieces, list) and len(pieces) <= 1_000_000, "Missing/oversized lower subset")
    seen, total, first_axis, first_coordinate_values = set(), 0, None, 0
    if pair:
        axes = proof.get("axes")
        need(isinstance(axes, list) and len(axes) == 2, "Expected two fiber coordinates")
        a, b = [index(k, n, "fiber coordinate") for k in axes]
        need(a != b, "Duplicate fiber coordinate")
    for piece in pieces:
        need(isinstance(piece, dict), "Malformed lower piece")
        low = bounds_list(piece.get("lo"), n, finite=True)
        high = bounds_list(piece.get("hi"), n, finite=True)
        need(all(x <= y for x, y in zip(low, high)), "Empty lower-piece box")
        if not pair:
            a = index(piece.get("axis"), n, "slice coordinate")
            first_axis = a if first_axis is None else first_axis
            need(a == first_axis, "Changing slice coordinate breaks prefix disjointness")
            axes = [a]
        need(all(low[k] == high[k] for k in range(n) if k not in axes), "Separator coordinates were not fixed")
        key = tuple(low[k] for k in range(n) if k not in axes)
        need(key not in seen, "Overlapping or duplicate separator state")
        seen.add(key)
        if not pair:
            need(all(row_extreme(row, low, high, maximum=False) >= 0 for row in rows), "Lower interval violates a complete-system row")
            count = high[a] - low[a] + 1
        else:
            first_coordinate_values += high[a] - low[a] + 1
            if first_coordinate_values > 10_000_000:
                raise CannotCheck("Two-coordinate certificate exceeds the fixed verification enumeration cap")
            count = 0
            # Enumerate only the explicitly certified restricted fibers, never
            # unseen separator states, and retain all mixed inequalities.
            constants = [row[0] + sum(row[k + 1] * low[k] for k in range(n) if k not in axes) for row in rows]
            for x in range(low[a], high[a] + 1):
                lower, upper, feasible = low[b], high[b], True
                for row, constant in zip(rows, constants):
                    rest, coefficient = constant + row[a + 1] * x, row[b + 1]
                    if coefficient > 0:
                        endpoint = -(rest // coefficient)
                        need(coefficient * (endpoint - 1) + rest < 0 <= coefficient * endpoint + rest,
                             "Fiber lower rounding failure")
                        lower = max(lower, endpoint)
                    elif coefficient < 0:
                        endpoint = (-rest) // coefficient
                        need(coefficient * (endpoint + 1) + rest < 0 <= coefficient * endpoint + rest,
                             "Fiber upper rounding failure")
                        upper = min(upper, endpoint)
                    elif rest < 0:
                        feasible = False
                if feasible:
                    count += max(0, upper - lower + 1)
            need(nonnegative(piece.get("cardinality"), "fiber cardinality") == count and count > 0,
                 "Incorrect complete restricted fiber cardinality")
        total += count
    need(nonnegative(proof.get("certified_lower"), "subset lower bound") == total, "Incorrect disjoint lower aggregate")
    target = integer(proof.get("target_lower"), "subset target")
    need(boolean(proof.get("target_met"), "subset target result") == (total >= target), "Incorrect lower target result")
    if pair:
        need(proof.get("exact_whole_count_claimed") is False, "Restricted fibers claimed an exact whole count")
    return {"interval": [total, None], "pieces": len(pieces), "explicit_first_coordinate_values": first_coordinate_values,
            "every_original_mixed_constraint_checked": True, "whole_count_inferred": False}


@lru_cache(None)
def protected_rows(degree):
    """Independent rational elimination for the protected numerator inequalities."""
    p, m = degree // 2, degree - degree // 2
    nodes = [0, *range(1, p + 1), *range(-1, -m - 1, -1)]
    n = len(nodes)
    matrix = [[Fraction(t)**k for k in range(n)] + [Fraction(i == k) for k in range(n)] for i, t in enumerate(nodes)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if matrix[i][k])
        matrix[pivot], matrix[k] = matrix[k], matrix[pivot]
        factor = matrix[k][k]
        matrix[k] = [x / factor for x in matrix[k]]
        for i in range(n):
            if i != k:
                factor = matrix[i][k]
                matrix[i] = [x - factor * y for x, y in zip(matrix[i], matrix[k])]
    result = []
    for k in range(degree - 2, degree + 1):
        weights = [x * ((-1)**degree if t < 0 else 1) for x, t in zip(matrix[k][n:], nodes)]
        denominator = math.lcm(*(x.denominator for x in weights))
        result.append([int(x * denominator) for x in weights])
    return result


def protected_interval(degree, values):
    need(len(values) == degree - 1 and all(type(x) is int and x >= 0 for x in values) and values[0] > 0,
         "Invalid complete paired count vector")
    low, high = 0, None
    for row in protected_rows(degree):
        constant = row[0] + sum(a * b for a, b in zip(row[1:-1], values))
        coefficient = row[-1]
        if coefficient > 0:
            endpoint = -((constant - 1) // coefficient)
            need(coefficient * (endpoint - 1) + constant < 1 <= coefficient * endpoint + constant,
                 "Protected lower rounding failure")
            low = max(low, endpoint)
        elif coefficient < 0:
            endpoint = (1 - constant) // coefficient
            need(coefficient * (endpoint + 1) + constant < 1 <= coefficient * endpoint + constant,
                 "Protected upper rounding failure")
            high = endpoint if high is None else min(high, endpoint)
        else:
            need(constant >= 1, "Protected fixed coefficient/count conflict")
    need(high is not None and 0 <= low <= high, "Protected count-bound interval conflict")
    return [low, high]


def claimed_interval(record, unit):
    grade = (int(unit[1:]) + 2) // 2
    if unit == "U05":
        interval = record["proved_I3_interval"]
    elif "interior_interval" in record:
        interval = record["interior_interval"]
    elif f"I{grade}_interval" in record:
        interval = record[f"I{grade}_interval"]
    elif "interior_lower" in record:
        interval = [record["interior_lower"], record["interior_upper"]]
    else:
        interval = [record[f"I{grade}_lower"], record[f"I{grade}_upper"]]
    need(isinstance(interval, list) and len(interval) == 2, "Malformed claimed interval")
    low, high = [nonnegative(x, "claimed interval endpoint") for x in interval]
    need(low <= high, "Inconsistent claimed interval")
    return [low, high]


def counts(record, unit):
    if unit == "U05" and "A" in record:
        return [record[k] for k in ("A", "B", "C", "I1", "I2")]
    fields = [k for k in record if k.startswith("counts_")]
    need(len(fields) == 1, "Missing/ambiguous count vector")
    return record[fields[0]]


def exact_count(value):
    if type(value) is str:
        need(re.fullmatch(r"0|[1-9][0-9]*", value), "Noncanonical nonnegative integer count")
        value = int(value)
    return nonnegative(value, "count response")


def compact_id(record):
    value = record.get("group_id", record.get("id"))
    return nonnegative(value, "certificate identity")


def relative_source(value, unit):
    need(isinstance(value, str), "Missing source path")
    if value.startswith("/mnt/data/"):
        match = re.fullmatch(r"/mnt/data/FR026_" + unit + r"[A-Z]?/return/(DATA/.*)", value)
        need(match is not None, "Unknown historical execution root")
        value = match[1]
    path = PurePosixPath(value)
    need(str(path) == value and not path.is_absolute() and ".." not in path.parts
         and "\\" not in value and value.startswith(f"DATA/{unit}/"), "Unsafe or cross-unit source path")
    return value


def evidence_directory(record, unit):
    if unit == "U05":
        return str(PurePosixPath(relative_source(record["geometry"]["path"], unit)).parent)
    return relative_source(record["evidence_directory"], unit)


def file_pin(path):
    need(path.is_file() and not path.is_symlink(), f"Missing/nonregular source file: {path}")
    st = path.stat()
    before = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    need(st.st_size <= MAX_FILE, f"File size cap exceeded: {path}")
    sha = hashlib.sha256()
    with path.open("rb") as f:
        for data in iter(lambda: f.read(1024**2), b""):
            sha.update(data)
    after = path.stat()
    need((after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns) == before,
         f"Source changed while hashing: {path}")
    return {"bytes": st.st_size, "sha256": sha.hexdigest()}


def source_lines(path):
    opener = gzip.open if path.suffix == ".gz" else open
    total = 0
    with opener(path, "rb") as f:
        number = 0
        while True:
            offset = f.tell()
            data = f.readline(MAX_LINE + 1)
            if not data:
                break
            total += len(data)
            need(len(data) <= MAX_LINE and total <= MAX_EXPANDED_FILE and data.endswith(b"\n"), "Oversized or unterminated source record")
            number += 1
            yield number, offset, data


class Sources:
    def __init__(self, root, unit):
        self.root, self.unit, self.files, self.lookup = root, unit, {}, {}
        self.stamps = {}

    def path(self, relative):
        relative = relative_source(relative, self.unit)
        path = self.root / relative
        need(not any(p.is_symlink() for p in (path, *path.parents)), "Symlink source is prohibited")
        if relative not in self.files:
            if not path.exists():
                raise CannotCheck(f"Required source premise is unavailable: {path}")
            before = path.stat()
            signature = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
            self.files[relative] = file_pin(path)
            need(signature(path.stat()) == signature(before), "Source changed before indexing")
            self.stamps[relative] = signature(before)
        return path

    def check_unchanged(self):
        for relative, expected in self.stamps.items():
            st = (self.root / relative).stat()
            need((st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns) == expected,
                 f"Source changed during the freeze: {relative}")

    def ref(self, relative, number, data, field=None):
        self.path(relative)
        result = {"path": relative, "line": number, "bytes": len(data), "sha256": digest(data)}
        if field:
            result["field"] = field
        return result

    def indexed(self, relative, *, key=None, line=None):
        path = self.path(relative)
        if relative not in self.lookup:
            ids, lines = {}, {}
            for number, offset, data in source_lines(path):
                record = json_object(data)
                identity = nonnegative(record.get("id"), "proof source identity")
                need(identity not in ids, "Duplicate proof source identity")
                row = {"offset": offset, "bytes": len(data), "sha256": digest(data), "line": number}
                ids[identity] = row
                lines[number] = row
            self.lookup[relative] = (ids, lines)
        ids, lines = self.lookup[relative]
        need(key in ids if key is not None else line in lines, "Required proof source record is missing")
        row = ids[key] if key is not None else lines[line]
        if line is not None:
            need(row["line"] == line, "Proof source line/identity mismatch")
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rb") as f:
            f.seek(row["offset"])
            data = f.read(row["bytes"])
        need(digest(data) == row["sha256"], "Proof source changed after indexing")
        return json_object(data), self.ref(relative, row["line"], data)


def add_proof(job, kind, record, field, reference, label):
    proof = record[field]
    need(isinstance(proof, dict), "Referenced proof is absent or refused")
    ref = {**reference, "field": field}
    identity = digest(encoded({"source": ref, "kind": kind, "label": label}))
    job["proofs"].append({"identity": identity, "kind": kind, "label": label, "reference": ref,
                          "body_sha256": digest(encoded(proof)), "body": proof})


def bind_parent(compact, geometry, raw, geometry_ref, count_ref, unit):
    identity, degree = compact_id(compact), int(unit[1:]) + 1
    sha = compact["geometry"]["sha256"] if unit == "U05" else compact["geometry_sha256"]
    need(SHA.fullmatch(sha or "") and geometry_ref["sha256"] == raw["geometry_sha256"] == sha,
         "Stale geometry/source SHA-256 binding")
    need(geometry.get("id") == raw.get("id") == identity and type(geometry.get("id")) is int and type(raw.get("id")) is int,
         "Geometry/count/compact identity mismatch")
    need(geometry["original"] == compact["bare_triple"] == raw["bare_triple"], "Different parent bare triple")
    need(all(type(x) is int and x == degree for x in (geometry["actual_dimension"], geometry["degree_bound"],
                                                    raw["actual_dimension"], compact["actual_dimension"])), "Different parent actual degree")
    expected_line = compact["geometry"]["line"] if unit == "U05" else compact["record_line"]
    need(integer(expected_line, "parent line") == geometry_ref["line"] == count_ref["line"], "Parent source line mismatch")
    values = counts(compact, unit)
    need(isinstance(values, list) and len(values) == degree - 1 and all(type(v) is int and v >= 0 for v in values),
         "Malformed compact count vector")
    sites = [(f"P{t}", t, False) for t in range(1, degree // 2 + 1)]
    sites += [(f"I{t}", t, True) for t in range(1, degree - degree // 2)]
    for model in ("hive", "rows"):
        rows = raw["model_sites"][model]
        need(isinstance(rows, list) and len(rows) == len(sites), "Incomplete numerical site roster")
        for row, expected in zip(rows, sites):
            need((row["kind"], integer(row["physical_grade"], "physical count grade"), boolean(row["strict"], "count strictness")) == expected,
                 "Count grade/strictness order changed")
            need(row["response"]["status"] == "complete", "Incomplete numerical response used as a premise")
        need([exact_count(row["response"]["value"]) for row in rows] == values, "Parent numerical count vector differs from compact certificate")
    integer_rows(geometry["count_rows"], degree)
    if unit in ("U09", "U10"):
        need(compact.get("grid") == raw.get("grid") == "balanced", "Unsupported production grid")
        need(integer(raw["unknown_interior_grade"], "unknown interior grade") == degree - degree // 2
             == integer(compact["unknown_interior_grade"], "compact interior grade"), "Wrong fixed interior grade")
    return degree, values, sha


def bind_repair(record, reference, job, raw, count_ref, unit, evidence):
    need(record.get("id") == job["id"] and type(record.get("id")) is int, "Repair identity mismatch")
    need(record["geometry_sha256"] == job["geometry_sha256"] and record["bare_triple"] == job["bare_triple"], "Repair parent geometry changed")
    need(integer(record["source_record_line"], "repair source line") == count_ref["line"]
         and record["source_record_sha256"] == count_ref["sha256"], "Repair source count line changed")
    need(relative_source(record["source_directory"], unit) == evidence and counts(record, unit) == job["paired_counts"], "Repair source/count vector changed")
    need(record["initial_failed_enclosure"] == raw["final_enclosure"], "Repair omitted or changed the initial interval")
    for key in record:
        if key.endswith("_proof") and key not in PROOF_FIELDS:
            raise CannotCheck(f"Unknown repair proof field: {key}")
    if unit in ("U09", "U10"):
        need(record["grid"] == "balanced" and integer(record["unknown_interior_grade"], "repair grade") == job["interior_grade"], "Repair grade/grid changed")


def freeze_index(root, unit, shard, output, *, expected_total=None, expected_selected=None):
    need(unit in CERTIFICATES and re.fullmatch(r"shard-?[0-9]+", shard), "Invalid unit/shard")
    root = root.resolve(strict=True)
    sources = Sources(root, unit)
    final_path = CERTIFICATES[unit]
    wanted, unit_ids, shard_ids = {}, set(), {}
    for number, _offset, data in source_lines(sources.path(final_path)):
        record = json_object(data)
        identity = compact_id(record)
        need(identity not in unit_ids, "Duplicate final production identity")
        unit_ids.add(identity)
        directory = evidence_directory(record, unit)
        parts = PurePosixPath(directory).parts
        need(len(parts) == 5 and parts[:3] == ("DATA", unit, "production") and parts[4] == "counts", "Unexpected final production source")
        owner = parts[3]
        need(re.fullmatch(r"shard-?[0-9]+", owner), "Final certificate refers to a pilot/nonproduction source")
        shard_ids.setdefault(owner, []).append(identity)
        if owner == shard:
            wanted[identity] = (record, sources.ref(final_path, number, data))
    total = POPULATIONS[unit] if expected_total is None else expected_total
    need(len(unit_ids) == total, "Incomplete final unit population")
    need(wanted and (expected_selected is None or len(wanted) == expected_selected), "Missing or unexpected selected shard population")
    directory = f"DATA/{unit}/production/{shard}/counts"
    geometry_path, count_path = directory + "/geometry.jsonl.gz", directory + "/certificates.jsonl"
    cover_path = directory + "/covers.jsonl.gz"
    cover_rows = iter(source_lines(sources.path(cover_path))) if unit != "U05" else None
    jobs_path = output.with_suffix(".jobs.jsonl")
    need(not output.exists() and not jobs_path.exists(), "Fresh index outputs are required")
    seen, entries, proof_types = set(), [], Counter()
    with jobs_path.open("xb") as jobs:
        pairs = zip_longest(source_lines(sources.path(geometry_path)), source_lines(sources.path(count_path)))
        for geometry_item, count_item in pairs:
            need(geometry_item is not None and count_item is not None, "Geometry/count source roster length mismatch")
            number, _offset, geometry_bytes = geometry_item
            cn, _co, count_bytes = count_item
            geometry, raw = json_object(geometry_bytes), json_object(count_bytes)
            need(number == cn and geometry.get("id") == raw.get("id"), "Raw geometry/count order mismatch")
            primary, primary_ref = None, None
            if raw.get("cover_sha256") is not None:
                need(cover_rows is not None, "Unexpected cover source")
                item = next(cover_rows, None)
                need(item is not None, "Missing referenced complete cover")
                pn, _po, pb = item
                need(digest(pb) == raw["cover_sha256"], "Primary cover line SHA-256 mismatch")
                if raw["id"] in wanted:
                    primary = json_object(pb)
                    need(type(primary.get("id")) is int and primary["id"] == raw["id"], "Primary cover parent identity mismatch")
                    primary_ref = sources.ref(cover_path, pn, pb)
            identity = raw["id"]
            if identity not in wanted:
                continue
            need(identity not in seen, "Duplicate selected raw parent")
            seen.add(identity)
            compact, compact_ref = wanted[identity]
            geometry_ref = sources.ref(geometry_path, number, geometry_bytes)
            count_ref = sources.ref(count_path, number, count_bytes)
            degree, values, sha = bind_parent(compact, geometry, raw, geometry_ref, count_ref, unit)
            job = {"unit": unit, "shard": shard, "id": identity, "degree": degree,
                   "interior_grade": degree - degree // 2, "bare_triple": compact["bare_triple"],
                   "geometry_sha256": sha, "count_rows": geometry["count_rows"],
                   "count_rows_sha256": row_digest(geometry["count_rows"]), "paired_counts": values,
                   "compact_interval": claimed_interval(compact, unit),
                   "compact_reference": compact_ref, "geometry_reference": geometry_ref,
                   "count_reference": count_ref, "proofs": [], "checkpoints": []}
            if unit == "U05":
                reference = compact.get("formal_cover")
                if reference is not None:
                    relative = relative_source(reference["path"], unit)
                    repair, ref = sources.indexed(relative, key=identity, line=integer(reference["line"], "cover reference line"))
                    need(repair["geometry_sha256"] == sha, "U05 upper proof parent geometry changed")
                    need(relative_source(repair["five_count_source"], unit) == directory, "U05 count source changed")
                    need(nonnegative(reference["certified_I3_upper"], "compact formal upper") == repair["proof"]["certified_upper"], "U05 referenced upper value mismatch")
                    add_proof(job, "upper", repair, "proof", ref, "primary_upper")
                    need(compact["upper_bound_kind"] == "FORMAL_COMPLETE_INTERIOR_UPPER_COVER", "Unrecorded U05 formal dependency")
                else:
                    need(compact["upper_bound_kind"] == "GEOMETRIC_HIGHER_COEFFICIENT_UPPER_BOUND", "U05 formal proof reference omitted")
            else:
                for model in ("hive", "rows"):
                    job["checkpoints"].append({"after": 0, "interval": claimed_interval(raw["initial_enclosures"][model], unit),
                                               "source": {**count_ref, "field": "initial_enclosures/" + model}})
                if primary is not None:
                    add_proof(job, "cover", primary, "proof", primary_ref, "primary_cover")
                if "cover_sha256" in compact:
                    need(compact["cover_sha256"] == raw.get("cover_sha256"), "Compact/primary cover binding differs")
                job["checkpoints"].append({"after": len(job["proofs"]), "interval": claimed_interval(raw["final_enclosure"], unit),
                                           "source": {**count_ref, "field": "final_enclosure"}})
                repair_path = None
                repair_line, repair_sha = None, None
                if compact.get("repair_evidence"):
                    repair_path = relative_source(compact["repair_evidence"], unit) + "/REPAIRS.jsonl"
                    repair_line = integer(compact["repair_line"], "repair line")
                elif compact.get("secondary_repair"):
                    pointer = compact["secondary_repair"]
                    repair_path, repair_line, repair_sha = relative_source(pointer["path"], unit), integer(pointer["line"], "repair line"), pointer["sha256_of_record"]
                elif unit == "U10" and compact.get("status") == "TEN_COUNT_REPAIRED_POSITIVE":
                    repair_path = f"DATA/{unit}/production/{shard}/repairs/REPAIRS.jsonl"
                    if not (root / repair_path).exists() and (root / (repair_path + ".gz")).exists():
                        repair_path += ".gz"
                if repair_path:
                    repair, repair_ref = sources.indexed(repair_path, key=identity, line=repair_line)
                    need(repair_sha is None or repair_sha == repair_ref["sha256"], "Final secondary repair SHA-256 mismatch")
                    bind_repair(repair, repair_ref, job, raw, count_ref, unit, directory)
                    need(repair["status"] == compact["status"], "Final repair status differs from compact certificate")
                    previous = None
                    if "previous_repair_sha256" in repair:
                        previous_path = relative_source(repair["previous_repair_directory"], unit) + "/REPAIRS.jsonl"
                        previous, previous_ref = sources.indexed(previous_path, key=identity)
                        need(previous_ref["sha256"] == repair["previous_repair_sha256"], "Inherited repair SHA-256 mismatch")
                        bind_repair(previous, previous_ref, job, raw, count_ref, unit, directory)
                        need(previous["final_enclosure"] == repair["previous_failed_enclosure"], "Inherited repair enclosure changed")
                        for field in PROOF_FIELDS:
                            if field != "joint_fiber_proof":
                                need(previous.get(field) == repair.get(field), "Inherited formal proof was omitted or changed")
                    for field, kind in PROOF_FIELDS.items():
                        if field in repair:
                            if field == "joint_fiber_proof" and previous is not None:
                                job["checkpoints"].append({"after": len(job["proofs"]), "interval": claimed_interval(previous["final_enclosure"], unit),
                                                           "source": {**previous_ref, "field": "final_enclosure"}})
                            add_proof(job, kind, repair, field, repair_ref, "repair_" + field)
                    job["checkpoints"].append({"after": len(job["proofs"]), "interval": claimed_interval(repair["final_enclosure"], unit),
                                               "source": {**repair_ref, "field": "final_enclosure"}})
                else:
                    need("REPAIRED" not in compact.get("status", "") and "JOINT" not in compact.get("status", ""), "Final repair dependency was omitted")
            job["checkpoints"].append({"after": len(job["proofs"]), "interval": job["compact_interval"], "source": compact_ref})
            offset = jobs.tell()
            data = encoded(job) + b"\n"
            need(len(data) <= MAX_LINE, "Frozen job size limit exceeded")
            jobs.write(data)
            entries.append({"ordinal": len(entries), "id": identity, "geometry_sha256": sha,
                            "compact_sha256": compact_ref["sha256"], "offset": offset, "bytes": len(data), "sha256": digest(data),
                            "proof_identities": [p["identity"] for p in job["proofs"]]})
            proof_types.update(p["kind"] for p in job["proofs"])
            if len(entries) % 1000 == 0:
                print(json.dumps({"phase": "index", "unit": unit, "shard": shard, "records": len(entries)}), flush=True)
        need(cover_rows is None or next(cover_rows, None) is None, "Unconsumed primary proof records")
    need(seen == set(wanted), "Incomplete selected parent identity roster")
    sources.check_unchanged()
    manifest = {"schema": "pro026-bounds-index-v1", "status": "FROZEN_INPUTS_NOT_VERIFIED", "root": str(root), "unit": unit, "shard": shard,
                "unit_population": total, "selected": len(entries), "jobs": {"path": str(jobs_path.resolve()), **file_pin(jobs_path)},
                "expected": entries, "proof_types": dict(proof_types), "sources": sources.files,
                "complete_unit_shards": {k: {"count": len(v), "sorted_ids_sha256": digest(encoded(sorted(v)))} for k, v in shard_ids.items()},
                "geometry_and_count_premises_checked_separately": PREMISES, "returned_code_executed": False,
                "indexer_sha256": file_pin(Path(__file__))["sha256"]}
    with output.open("x", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    return manifest


def check_job(job, expected):
    unit, degree = job["unit"], integer(job["degree"], "degree")
    need(unit in POPULATIONS and degree == int(unit[1:]) + 1, "Unsupported parent degree")
    need(job["id"] == expected["id"] and type(job["id"]) is int
         and job["geometry_sha256"] == expected["geometry_sha256"] == job["geometry_reference"]["sha256"]
         and job["compact_reference"]["sha256"] == expected["compact_sha256"], "Frozen parent identity changed")
    rows = job["count_rows"]
    integer_rows(rows, degree)
    need(row_digest(rows) == job["count_rows_sha256"], "Frozen parent count rows changed")
    grade = integer(job["interior_grade"], "fixed interior grade")
    need(grade == degree - degree // 2, "Wrong fixed interior grade")
    strict_rows = [[grade * row[0] - int(any(row[1:])), *row[1:]] for row in rows]
    interval = protected_interval(degree, job["paired_counts"])
    need([p["identity"] for p in job["proofs"]] == expected["proof_identities"], "Omitted, extra, or reordered formal proof obligation")
    checkpoints = job["checkpoints"]
    need(isinstance(checkpoints, list) and checkpoints, "Missing final interval comparison")
    for point in checkpoints:
        need(0 <= integer(point["after"], "checkpoint position") <= len(job["proofs"]), "Invalid bound checkpoint")
        need(len(point["interval"]) == 2 and all(type(v) is int for v in point["interval"]), "Noninteger saved count-bound interval")
    def compare(position):
        for point in checkpoints:
            if point["after"] == position:
                need(interval == point["interval"], f"Proved/count-derived interval differs from source checkpoint at proof {position}")
    compare(0)
    checked = []
    for number, item in enumerate(job["proofs"], 1):
        need(digest(encoded(item["body"])) == item["body_sha256"], "Frozen proof body changed")
        kind = item["kind"]
        if kind in ("upper", "cover"):
            result = check_tree(strict_rows, item["body"], upper_only=kind == "upper")
        else:
            need(kind in ("lower", "pair"), "Unknown proof kind")
            result = check_lower(strict_rows, item["body"], pair=kind == "pair")
        low, high = result["interval"]
        interval = [max(interval[0], low), interval[1] if high is None else min(interval[1], high)]
        need(interval[0] <= interval[1], "Formal/numerical count-bound premise conflict")
        checked.append({"identity": item["identity"], "kind": kind, "source": item["reference"], **result})
        compare(number)
    need(interval == job["compact_interval"], "Final compact interval not proved")
    return {"unit": unit, "shard": job["shard"], "id": job["id"], "bare_triple": job["bare_triple"],
            "geometry_sha256": job["geometry_sha256"], "actual_degree": degree, "interior_grade": grade,
            "strict_rows_sha256": row_digest(strict_rows), "proved_interval": interval,
            "compact_source": job["compact_reference"], "geometry_source": job["geometry_reference"],
            "count_source": job["count_reference"], "proofs": checked,
            "whole_count_inferred": False, "all_integer_tree_fields_checked": True}


def read_index(path, sha):
    need(SHA.fullmatch(sha or ""), "Expected index SHA-256 is required")
    data = path.read_bytes()
    need(digest(data) == sha, "Frozen index SHA-256 mismatch")
    manifest = json_object(data)
    need(manifest.get("schema") == "pro026-bounds-index-v1" and manifest.get("status") == "FROZEN_INPUTS_NOT_VERIFIED", "Index is not a complete input freeze")
    expected = manifest["expected"]
    need(len(expected) == manifest["selected"] > 0 and len({r["id"] for r in expected}) == len(expected), "Incomplete or duplicate frozen expected identities")
    offset = 0
    for number, row in enumerate(expected):
        need(row["ordinal"] == number and integer(row["offset"], "job offset") == offset
             and 0 < integer(row["bytes"], "job bytes") <= MAX_LINE, "Incomplete/noncontiguous frozen job membership")
        offset += row["bytes"]
    need(offset == manifest["jobs"]["bytes"], "Frozen jobs size mismatch")
    return manifest


def verify_slice(index_path, sha, start, stop, output):
    manifest = read_index(index_path, sha)
    need(0 <= integer(start, "slice start") < integer(stop, "slice stop") <= manifest["selected"], "Invalid or empty exact slice")
    jobs = Path(manifest["jobs"]["path"])
    need(jobs.is_file() and not jobs.is_symlink() and jobs.stat().st_size == manifest["jobs"]["bytes"], "Frozen job file missing or size changed")
    identities = output.with_suffix(".identities.jsonl")
    count = 0
    types = Counter()
    with jobs.open("rb") as f, identities.open("xb") as out:
        for expected in manifest["expected"][start:stop]:
            f.seek(expected["offset"])
            data = f.read(expected["bytes"])
            need(digest(data) == expected["sha256"], "Frozen job row SHA-256 mismatch")
            job = json_object(data)
            need(job["unit"] == manifest["unit"] and job["shard"] == manifest["shard"], "Cross-index job binding")
            row = check_job(job, expected)
            row.update(ordinal=expected["ordinal"], job_sha256=expected["sha256"])
            out.write(encoded(row) + b"\n")
            count += 1
            types.update(p["kind"] for p in row["proofs"])
            if count % 100 == 0:
                print(json.dumps({"phase": "verify", "checked": count, "slice": [start, stop]}), flush=True)
    result = {"status": "PASS", "predicate": "Every supplied formal bound and exact derived final interval checked for the frozen slice",
              "index_sha256": sha, "unit": manifest["unit"], "shard": manifest["shard"], "slice": [start, stop],
              "checked": count, "identities": {"path": str(identities.resolve()), **file_pin(identities)},
              "proof_types": dict(types), "all_split_midpoints_and_endpoints_exact_integers": True,
              "unproved_branches_treated_as_zero": False, "whole_counts_inferred": False,
              "separate_premises": PREMISES, "returned_code_executed": False,
              "verifier_sha256": file_pin(Path(__file__))["sha256"]}
    with output.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    return result


def aggregate(index_path, sha, results, output, *, accepted_verifier_source, accepted_verifier_sha256):
    need(SHA.fullmatch(accepted_verifier_sha256 or ""), "An explicit accepted verifier SHA-256 is required")
    accepted_verifier_source = Path(accepted_verifier_source)
    accepted_pin = file_pin(accepted_verifier_source)
    need(accepted_pin["sha256"] == accepted_verifier_sha256, "Accepted verifier source bytes changed or do not match the declared SHA-256")
    aggregator_source = Path(__file__).resolve()
    aggregator_pin = file_pin(aggregator_source)
    manifest = read_index(index_path, sha)
    need(manifest.get("indexer_sha256") == accepted_verifier_sha256,
         "Frozen indexer is incompatible with the explicitly accepted verifier source version")
    seen, proof_counts = set(), Counter()
    receipts = []
    for path in results:
        result = json_object(path.read_bytes())
        need(result.get("status") == "PASS" and result["index_sha256"] == sha
             and result["unit"] == manifest["unit"] and result["shard"] == manifest["shard"], "Failed/stale/cross-index slice result")
        need(result.get("verifier_sha256") == accepted_verifier_sha256,
             "Slice verifier identity is missing, changed, or not the explicitly accepted source version")
        identity_path = Path(result["identities"]["path"])
        need(file_pin(identity_path) == {k: result["identities"][k] for k in ("bytes", "sha256")}, "Slice identity ledger changed")
        start, stop = result["slice"]
        need(0 <= integer(start, "result start") < integer(stop, "result stop") <= manifest["selected"], "Invalid result slice")
        local = set()
        for _n, _offset, data in source_lines(identity_path):
            row = json_object(data)
            ordinal = integer(row["ordinal"], "result ordinal")
            need(start <= ordinal < stop and ordinal not in seen and ordinal not in local, "Overlapping/duplicate slice identity")
            expected = manifest["expected"][ordinal]
            need(row["id"] == expected["id"] and row["geometry_sha256"] == expected["geometry_sha256"]
                 and row["job_sha256"] == expected["sha256"] and row["compact_source"]["sha256"] == expected["compact_sha256"], "Result identity/source mismatch")
            need([p["identity"] for p in row["proofs"]] == expected["proof_identities"], "Result omitted a required formal proof")
            local.add(ordinal)
            proof_counts.update(p["kind"] for p in row["proofs"])
        need(local == set(range(start, stop)) and result["checked"] == len(local), "Incomplete slice result identities")
        seen.update(local)
        receipts.append({"path": str(path), **file_pin(path)})
    need(seen == set(range(manifest["selected"])), "Incomplete full frozen identity coverage")
    need(dict(proof_counts) == manifest["proof_types"], "Formal obligation kind/count mismatch")
    need(file_pin(accepted_verifier_source) == accepted_pin, "Accepted verifier source changed during aggregation")
    need(file_pin(aggregator_source) == aggregator_pin, "Aggregator source changed during aggregation")
    result = {"status": "PASS", "index_sha256": sha, "unit": manifest["unit"], "shard": manifest["shard"],
              "checked": len(seen), "proof_types": dict(proof_counts), "slice_receipts": receipts,
              "complete_expected_identities_once": True, "separate_premises": PREMISES,
              "whole_counts_inferred": False, "returned_code_executed": False,
              "accepted_verifier_source": {"path": str(accepted_verifier_source.resolve()), **accepted_pin},
              "verifier_sha256": accepted_verifier_sha256,
              "indexer_sha256": manifest["indexer_sha256"],
              "indexer_compatibility": "Exact same source version as the explicitly accepted corpus verifier",
              "aggregator_source": {"path": str(aggregator_source), **aggregator_pin},
              "aggregator_sha256": aggregator_pin["sha256"],
              "aggregation_only": True, "corpus_proofs_reverified": False}
    with output.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("index")
    build.add_argument("--root", type=Path, required=True, help="One restored namespace, e.g. namespaces/u05")
    build.add_argument("--unit", choices=CERTIFICATES, required=True)
    build.add_argument("--shard", required=True)
    build.add_argument("--expected-selected", type=int)
    run = commands.add_parser("verify")
    join = commands.add_parser("aggregate")
    for sub in (run, join):
        sub.add_argument("--index", type=Path, required=True)
        sub.add_argument("--index-sha256", required=True)
    run.add_argument("--start", type=int, required=True)
    run.add_argument("--stop", type=int, required=True)
    join.add_argument("--results", nargs="+", type=Path, required=True)
    join.add_argument("--accepted-verifier-source", type=Path, required=True)
    join.add_argument("--accepted-verifier-sha256", required=True)
    for sub in (build, run, join):
        sub.add_argument("--output", type=Path, required=True)
        sub.add_argument("--max-seconds", type=float, default=100)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        need(not args.output.exists() and args.output.parent.is_dir(), "Output must be fresh with an existing parent")
        with time_cap(args.max_seconds):
            if args.command == "index":
                result = freeze_index(args.root, args.unit, args.shard, args.output, expected_selected=args.expected_selected)
            elif args.command == "verify":
                result = verify_slice(args.index, args.index_sha256, args.start, args.stop, args.output)
            else:
                result = aggregate(args.index, args.index_sha256, args.results, args.output,
                                   accepted_verifier_source=args.accepted_verifier_source,
                                   accepted_verifier_sha256=args.accepted_verifier_sha256)
        print(json.dumps({"status": result["status"], "output": str(args.output), "elapsed_seconds": time.monotonic() - started}), flush=True)
    except (Exception, KeyboardInterrupt) as exc:
        result = {"status": "CANNOT_CHECK" if isinstance(exc, (CannotCheck, FileNotFoundError, KeyboardInterrupt)) else "FAIL",
                  "error": f"{type(exc).__name__}: {exc}", "command": args.command,
                  "elapsed_seconds": time.monotonic() - started, "returned_code_executed": False}
        if not args.output.exists():
            with args.output.open("x", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
                f.write("\n")
        print(json.dumps(result), file=sys.stderr, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
