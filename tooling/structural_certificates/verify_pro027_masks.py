#!/usr/bin/env python3
"""Independent finite-certificate replay for Pro027 P06, P07 and P08.

No returned program is imported or executed. The sibling root-owned
verify_normal_certificates.py supplies exact lattice arithmetic and its complete
Laurent face recurrence. This file supplies the original boundary-linear hive,
chart/implication checks, complete (not merely connected) subset coverage,
primitive correction incidences, historical type adapters, compact P06 formula,
and source-mask joins. Every command is a bounded, resumable slice.

Typical root execution (all commands belong in the owner's science harness):
  freeze --root PACKET --stage p07 --f025-r6 ACCEPTED_R6 --output MANIFEST
  boundary --root PACKET --manifest MANIFEST --start 0 --limit 1 --output REPORT
  cones --root PACKET --manifest MANIFEST --presentation 6:43 --coefficient 1
        --start 0 --limit 1000 --output REPORT
  types --root PACKET --manifest MANIFEST --start 0 --limit 20 --output REPORT
  scope --root PACKET --manifest MANIFEST --rank 6 --start 0 --limit 1000
        --output REPORT
  aggregate --root PACKET --manifest MANIFEST --reports REPORT... --output FINAL

P08 freezes the 123 complementary presentations and all 125 chart identities;
its aggregate additionally requires --adopt-p07 P07_FINAL. P06 additionally
requires --f025-r7 ACCEPTED_R7. Manifest obligations declare exact slice totals.
Use each report's next_start after PARTIAL, including a deadline interruption.
--seconds defaults to 95 and cannot exceed 100. Fresh output files are required.

Acceptance means only the complete declared finite predicate, conditional on
the listed analytic and previously adopted premises. It is not a new proof of
the normal-cycle theorem, the accepted F025 forcing table, an LR lattice recount,
or positivity for every actual quartic/quintic or every rank-six/seven boundary.
Report origin/capture authenticity remains the owner's harness responsibility.

Schema sources read as inert text: P06 CODE/verify_certificate_v1.py; P07
CODE/{verify_cycle_v1,symbolic_v1}.py; P08 CODE/{verify_extension_v1,
scope_challenges_v1}.py; READING-COPY/PROOFS/{021,022,023,025,026,028,029}*.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations, permutations
import json
from math import comb, factorial, gcd
from pathlib import Path
import re
import sys
import time

sys.dont_write_bytecode = True
import verify_normal_certificates as N

SCHEMA = "pro027-independent-boundary-mask-certificates-v1"
P08 = "HISTORY/P11-A01/HISTORY/P10-A01/HISTORY/P09-A01/HISTORY/P08-A01"
P07 = P08 + "/HISTORY/P07-A01"
P06 = P07 + "/HISTORY/P06-A01"
SHORT_NORMAL_PROOF = P06 + "/SOURCES/023-SHORT-NORMAL-COEFFICIENT-POSITIVITY.md"
THREE_CONE_PROOF = P06 + "/SOURCES/031-THREE-CONE-PARITY-AND-METRIC.md"
P07_MASKS = (43, 45)
P08_MASKS = (
    43,45,51,54,57,58,75,77,83,86,89,90,101,105,106,113,114,116,
    139,141,147,166,172,181,201,202,209,210,309,341,565,1059,1062,
    1068,1077,1080,1091,1094,1100,1109,1112,1121,1122,1124,1155,
    1158,1164,1173,1189,1193,1194,1201,1202,1204,1217,1218,1283,
    1286,1301,1317,1321,1322,1329,1330,1349,1353,1354,1361,1557,
    1573,1577,1585,1605,1609,1669,2115,2118,2124,2133,2136,2146,
    2148,2179,2182,2188,2197,2213,2217,2218,2225,2226,2228,2242,
    2325,2341,2345,2346,2353,2354,2373,2377,2378,2385,2597,2601,
    2609,2629,2633,2693,3204,4230,4245,4261,4265,4266,4273,4274,
    4276,4393,4394,4401,4402,4426,4433,4657,
)
P06_MASKS = {
    6: (4235,4243,5426,9521),
    7: (14745,16951,17209,17210,17267,25011,27033,27747,37683,
        38167,38183,41623,41657,41751,41767,41779,43731,45772,
        46694,49963,70777,70778,74919,79465,104049),
}
SOURCE = {
    "p07_roster": P07 + "/DATA/J02-FIVE-MASK-ROSTER.json",
    "p07_boundary": P07 + "/DATA/J02-BOUNDARY-PILOT.json",
    "p07_cycles": P07 + "/DATA/J04-NORMAL-CYCLE-CERTIFICATE.json",
    "p07_types": P07 + "/DATA/J04-CONE-TYPES.json",
    "p07_words": P07 + "/DATA/J10-COMPLETE-MASK-WORDS.json",
    "p08_boundary": P08 + "/DATA/J01-COMPLETE-BOUNDARY-ROSTER.json",
    "p08_cert_index": P08 + "/DATA/FINAL-CERTIFICATE-INDEX.json",
    "p08_type_index": P08 + "/DATA/FINAL-TYPE-INDEX.json",
    "p08_words": P08 + "/DATA/J09-ALL-MASK-WORDS.json.gz",
    "p08_scope": P08 + "/DATA/J09-SCOPE.json",
    "p06_roster": P06 + "/DATA/J05-ROSTER.json",
    "p06_boundary": P06 + "/DATA/J05-COMPLETE-MASK-CERTIFICATE.json",
    "p06_types": P06 + "/DATA/J06-LAURENT-CERTIFICATE.json",
    "p06_metric": P06 + "/SOURCES/METRIC-MASK-BINDING.json",
}
# Exact bytes from the immutable captured packet / accepted F025 inputs. A
# different source version needs a reviewed checker change, not a lax freeze.
PINS = {
    "p07_roster": "93a90fbd33560a5ded4232df5121cb662ed5db114d244341249af9e212bd4f78",
    "p07_boundary": "8c3f8dfce7b79fe75f659e579ee0dbc6092fee86c9798e5696cb375d7320b422",
    "p07_cycles": "6e1aa02247a67feaf6a146e15b2f1e1c17bbeafd1c0f22e5c9445623dcdaecb7",
    "p07_types": "610cabf32167e236f99a92358a884673e44d0e7bed51724a1b2c726ba1234573",
    "p07_words": "40adbc803963d362ec08dfbec5f784f870b118c4857aa545c5253e715b221588",
    "p08_boundary": "3863cf26702a535cf3494b7b207bc44f532a571af8ef346e3a7e08b3ea933072",
    "p08_cert_index": "4ca23585389eae3373e11724ffe11afdbfe461b1b0eedcf0175b65639fb1bd08",
    "p08_type_index": "4cfcb1f64b2d3a0407dec2786fa0826683f164db392fffa41b540c12ebb2cd6d",
    "p08_scope": "e3e158def200b54e44c7e3edf58ea49da326c5d6dab7b0c85cf01045a8e7d214",
    "p06_roster": "52e18e2458e7c557d5350da1c8f0edb06db35c352308f7597b7b963ca19078b0",
    "p06_boundary": "871532c82a02e4eff8cc9107a76a29faab0da4d2d656f4ec6aaea476f8f16a87",
    "p06_types": "9ea6278a9832fb7b204c5b0042331f04dbfc39a3956c0be4691b5b6e5506df18",
    "p06_metric": "dfd5c3dc5692c041f87608df5172f95bcac50d260458ef8c72f8f6805538d50d",
    "f025:6": "6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0",
    "f025:7": "bb595b3914ce05105743e9386f2cc64a4d2ae2d59df0d340c3221b8b74d7cd9c",
}
PROOFS = {
    "p06": ("021-BOUNDARY-AWARE-FACET-REDUCTION.md",
            "022-HIDDEN-STRATA-BY-DUAL-VALUATION.md",
            "023-ALL-SIZE-FOUR-COORDINATE-LR-POSITIVITY.md"),
    "p07": ("025-COMPLETE-REFINED-NORMAL-CYCLE.md",
            "026-ALL-SIZE-FIVE-COORDINATE-DOMAINS.md"),
    "p08": ("025-COMPLETE-REFINED-NORMAL-CYCLE.md",
            "026-ALL-SIZE-FIVE-COORDINATE-DOMAINS.md",
            "028-ALL-RANK6-FIVE-COORDINATE-POSITIVITY.md",
            "029-EXACT-LATTICE-ISOMETRIES-AND-FINITE-CERTIFICATE.md"),
}
PREMISES = [
    "The explicitly hashed F025 full mask table and its original-rhombus ordering/forcing theorem are previously accepted inputs; they are not re-proved here.",
    "Hive/LR correspondence, stretching period collapse, actual-degree theorem and tensor/determinant count symmetries.",
    "BV local formula, lattice equivariance, analyticity and dual-solid valuation, with one representative-chart scalar product.",
    "P07/P08: complete compatible normal-cycle refinement, primitive balance cancellation against ORIGINAL actual face volumes, including hidden affine strata and lineality.",
    "P06: the compact three-cone constant formula and the hidden-stratum dual-valuation identity of proofs 021/022; the stored hidden-pair challenge is not a substitute for those proofs.",
    "Previously adopted short-normal bound for the remaining next-to-next-leading coefficient and intrinsic positivity of the leading two coefficients.",
    "Previously accepted rank-at-most-five theorem (Ferudun prior work), lower-coordinate cases, and old metric-mask branch; none is newly replayed by this finite module.",
    "Capture provenance and report execution provenance are supplied by the owner's scientific harness.",
]
MAX_SOURCE = 128 * 1024 * 1024
require = N.require
integer = N.integer
rational = N.rational


class CannotCheck(N.CheckError):
    pass


def jd(value):
    return N.digest(json.dumps(value, separators=(",", ":"), sort_keys=True).encode())


def bounded_bytes(path):
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_SOURCE+1)
    require(len(data) <= MAX_SOURCE, f"File exceeds explicit byte bound: {path}")
    return data


def exact_int(value, text_ok=False):
    if text_ok and isinstance(value, str) and re.fullmatch(r"0|-?[1-9][0-9]*", value):
        return int(value)
    return integer(value)


def ints(values, width=None, text_ok=False):
    require(isinstance(values, list), "Expected integer vector")
    out = tuple(exact_int(x, text_ok) for x in values)
    require(width is None or len(out) == width, "Integer vector width mismatch")
    return out


def matrix(values, height=None, width=None, text_ok=False):
    require(isinstance(values, list) and bool(values), "Expected nonempty integer matrix")
    out = tuple(ints(row, width, text_ok) for row in values)
    require(all(len(row) == len(out[0]) for row in out), "Ragged integer matrix")
    require(height is None or len(out) == height, "Integer matrix height mismatch")
    return out


def ordered_ids(values, count, length=None):
    out = ints(values, length)
    require(out == tuple(sorted(set(out))) and all(0 <= x < count for x in out),
            "Missing, duplicate, unsorted or out-of-range identity")
    return out


def perm(values, count):
    out = ints(values, count)
    require(sorted(out) == list(range(count)), "Not an exact permutation")
    return out


def unique_map(records, key, expected=None):
    require(isinstance(records, list), "Expected record list")
    result = {}
    for record in records:
        k = key(record)
        require(k not in result, f"Duplicate exact source identity: {k}")
        result[k] = record
    if expected is not None:
        require(set(result) == set(expected), "Missing, stale or unexpected source identity roster")
    return result


def checker_versions():
    here = Path(__file__).resolve()
    require(Path(N.__file__).resolve() == here.with_name("verify_normal_certificates.py"),
            "Root arithmetic helper did not resolve to the declared sibling source")
    return {p.name: N.digest(p.read_bytes()) for p in (here, Path(N.__file__).resolve())}


def premise_paths(stage):
    result = ["READING-COPY/PROOFS/"+proof for proof in PROOFS[stage]]+[SHORT_NORMAL_PROOF]
    if stage == "p06":
        result.append(THREE_CONE_PROOF)
    return result


def whole_polynomial_bridge(d):
    require(d in (4,5), "Unsupported whole-polynomial bridge")
    rows = []
    for actual in range(d+1):
        coefficients = {"0":"constant one for a nonempty period-one lattice family (adopted premise)"}
        for k in range(1,actual+1):
            if k >= actual-1:
                reason = "intrinsic leading/next-leading positivity in ACTUAL dimension, via integral dilation"
            elif d == 5 and k in (1,2):
                reason = "complete corrected normal-cycle certificate plus proof 025, including hidden affine strata"
            elif d == 4 and actual == 3 and k == 1:
                reason = "complete positive three-cone constants plus the hidden-stratum gluing/dual-valuation theorem in proof 022"
            elif d == 4 and actual == 4 and k == 1:
                reason = "complete positive three-cone constants plus the actual complete edge-fan BV sum"
            else:
                require(actual == d and k == d-2, "Unaccounted whole-polynomial coefficient")
                reason = "adopted complete indexed short-normal theorem in the fixed selected-coordinate Euclidean metric; norm hypotheses are independently checked here"
            coefficients[str(k)] = reason
        rows.append({"actual_degree":actual,"coefficients":coefficients,"coefficients_above_actual_degree":"zero by the adopted degree theorem"})
    return {"status":"conditional mathematical bridge, not a newly verified theorem",
            "coordinate_upper_bound":d,"actual_degree_not_inferred_from_bound":True,
            "by_actual_degree":rows,"short_normal_theorem_source":"packet:"+SHORT_NORMAL_PROOF,
            "short_normal_theorem_bound":"1/100 for complete codimension-two face weights, ONLY in the full-dimensional chosen lattice basis",
            "short_normal_proof_hypotheses":["nonempty bounded rational full-dimensional polytope in its specified saturated lattice",
                "period-one lattice count","standard Euclidean scalar product in one integral coordinate basis",
                "every primitive inward facet normal has squared norm at most six"],
            "empty_fibers":"zero positive-stretch polynomial; the special scalar t=0 convention is not used for interpolation",
            "metric_transport":"tensor words transport the entire polynomial and degree; no affine hive metric/face-volume transport is inferred",
            "unreplayed_examples":"historical numerical whole-polynomial examples and P06 hidden-pair numerical challenges are not used as analytic proof substitutes"}


class Sources:
    def __init__(self, root, external=None, entries=None):
        self.root = Path(root).resolve()
        self.external = external or {}
        self.entries = entries
        self.reads, self.cache = {}, {}

    def path(self, key):
        if key.startswith("f025:"):
            if key not in self.external:
                raise CannotCheck(f"Missing explicitly declared accepted source: {key}")
            p = Path(self.external[key]).resolve()
            if not p.is_file():
                raise CannotCheck(f"Missing declared accepted source: {p}")
            return p
        require(key.startswith("packet:"), "Unknown source namespace")
        try:
            return N.safe_path(self.root, key[7:])
        except N.CheckError as error:
            raise CannotCheck(str(error)) from error

    def bytes(self, key):
        p = self.path(key)
        require(p.stat().st_size <= MAX_SOURCE, f"Source exceeds declared bound: {key}")
        data = bounded_bytes(p)
        info = {"bytes": len(data), "sha256": N.digest(data)}
        if self.entries is not None:
            require(key in self.entries and info == self.entries[key], f"Stale/unbound source: {key}")
        if key in self.reads:
            require(info == self.reads[key], f"Source changed during command: {key}")
        self.reads[key] = info
        return data

    def read(self, key):
        if key not in self.cache:
            data = self.bytes(key)
            if key.endswith(".gz"):
                # All gzip inputs have a pinned compressed source; enforce a
                # separate decoded bound without an unbounded gzip.decompress.
                import io
                with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
                    data = stream.read(MAX_SOURCE + 1)
                require(len(data) <= MAX_SOURCE, "Decoded source exceeds bound")
            self.cache[key] = N.decode(data)
        return self.cache[key]

    def named(self, name):
        return self.read("packet:" + SOURCE[name])

    def unchanged(self):
        for key in list(self.reads):
            self.bytes(key)


def rref_basis(rows, width):
    basis = {}
    for source in rows:
        require(len(source) == width, "Linear relation width mismatch")
        row = list(map(Q, source))
        for pivot, prior in sorted(basis.items()):
            c = row[pivot]
            if c:
                row = [x - c*y for x, y in zip(row, prior)]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            den = row[pivot]
            basis[pivot] = tuple(x / den for x in row)
    return basis


def in_span(row, basis):
    row = list(map(Q, row))
    for pivot, prior in sorted(basis.items()):
        c = row[pivot]
        if c:
            row = [x - c*y for x, y in zip(row, prior)]
    return not any(row)


@lru_cache(None)
def original_rows(n):
    """Full boundary-linear rhombi in the accepted F025 up/down row order."""
    require(type(n) is int and 2 <= n <= 7, "Unsupported original hive rank")
    interior = [(i, j) for i in range(1, n) for j in range(1, n-i)]
    pos = {p: i for i, p in enumerate(interior)}
    width = 3*n + len(interior)
    values = {}
    for i in range(n+1):
        for j in range(n+1-i):
            row = [0]*width
            if (i, j) in pos:
                row[3*n+pos[i,j]] = 1
            elif j == 0:
                for k in range(i):
                    row[n+k] = 1
            elif i == 0:
                for k in range(j):
                    row[k] = 1
            else:
                for k in range(n):
                    row[n+k] = 1
                for k in range(j):
                    row[2*n+k] = 1
            values[i,j] = row
    stencils = []
    for i in range(n):
        for j in range(n-i):
            if i+j < n-1:
                stencils.append((((i+1,j),1),((i,j+1),1),((i,j),-1),((i+1,j+1),-1)))
            if j:
                stencils.append((((i,j),1),((i+1,j),1),((i,j+1),-1),((i+1,j-1),-1)))
            if i:
                stencils.append((((i,j),1),((i,j+1),1),((i+1,j),-1),((i-1,j+1),-1)))
    require(len(stencils) == 3*n*(n-1)//2, "Incomplete original rhombus roster")
    require(len({tuple(sorted(s)) for s in stencils}) == len(stencils), "Duplicate original rhombus")
    return tuple(tuple(sum(sign*values[p][c] for p, sign in stencil) for c in range(width))
                 for stencil in stencils)


def boundary_constraints(n, mask, d):
    require(type(mask) is int and 0 <= mask < 1 << (3*(n-1)), "Invalid exact mask")
    good, equalities, labels = [], [], []
    for side in range(3):
        for j in range(n-1):
            row = [0]*(3*n+d)
            row[side*n+j], row[side*n+j+1] = 1, -1
            if mask >> (side*(n-1)+j) & 1:
                equalities.append(tuple(row))
            else:
                good.append(tuple(row))
                labels.append(["partition_gap", side, j])
        row = [0]*(3*n+d)
        row[side*n+n-1] = 1
        good.append(tuple(row))
        labels.append(["last_part", side])
    equalities.append(tuple([1]*n+[-1]*(2*n)+[0]*d))
    return tuple(good), tuple(equalities), labels


def verify_implication(target, generators, equalities, positive, unrestricted):
    width = len(target)
    answer = [Q(0)]*width
    for terms, rows, nonnegative in ((positive, generators, True), (unrestricted, equalities, False)):
        require(isinstance(terms, list), "Missing implication coefficient roster")
        seen = set()
        for term in terms:
            require(isinstance(term, list) and len(term) == 2, "Malformed implication term")
            i, value = integer(term[0]), rational(term[1])
            require(0 <= i < len(rows) and i not in seen, "Repeated/out-of-range implication generator")
            require(not nonnegative or value > 0, "Nonpositive implication multiplier")
            require(len(rows[i]) == width, "Dropped boundary/chart coefficient in implication")
            seen.add(i)
            answer = [x+value*y for x, y in zip(answer, rows[i])]
    require(tuple(answer) == tuple(target), "Bad full boundary/chart affine implication")


def verify_chart_affine_hull(raw, off, basis, free, closed, boundary_equalities):
    """Prove the selection chart contains EVERY original forced solution.

    Pure boundary consistency equations need not vanish for every legal
    partition boundary: some such boundaries have an empty hive. Therefore
    prove each x_i - O_i*b - C_i*select(x) from the full forced affine equations,
    and preserve ALL substituted inequalities. Do not drop consistency rows or
    replace this implication by the stronger, unnecessary O-image assertion.
    """
    ambient, d, bw = len(basis), len(free), len(off[0])
    forced = [row for i,row in enumerate(raw) if closed >> i & 1]
    require(len(rref_basis([row[bw:] for row in forced],ambient)) == ambient-d,
            "Forced affine hull does not have the declared coordinate bound")
    require(all(sum(row[bw+i]*basis[i][j] for i in range(ambient)) == 0
                for row in forced for j in range(d)), "Unit chart leaves the forced linear kernel")
    equations = forced + [tuple(row[:bw])+tuple([0]*ambient) for row in boundary_equalities]
    span = rref_basis(equations,bw+ambient)
    for i in range(ambient):
        relation = [-x for x in off[i]]+[int(i == k) for k in range(ambient)]
        for j,k in enumerate(free):
            relation[bw+k] -= basis[i][j]
        require(in_span(relation,span), "Chart identity is not implied by all full forced affine rows and boundary equalities")


def verify_boundary(record, accepted, d, deadline):
    n = integer(record["rank"])
    mask = integer(record["representative_mask"] if d == 4 else record["mask"])
    sym, reduction = record["symbolic_chart"], record["reduction"]
    raw = original_rows(n)
    ambient = (n-1)*(n-2)//2
    closed = integer(sym["closed"])
    require(0 <= closed < 1 << len(raw), "Closed-row mask out of range")
    require(integer(accepted["mask"]) == mask and integer(accepted["closed_rows_mask"]) == closed
            and integer(accepted["dimension_bound"]) == d, "Stale accepted F025 mask/chart geometry")
    off = matrix(sym["offset_matrix"], ambient, 3*n)
    basis = matrix(sym["basis_rows"], ambient, d)
    free = ordered_ids(sym["free"], ambient, d)
    for j, i in enumerate(free):
        require(not any(off[i]) and basis[i] == tuple(int(j == k) for k in range(d)),
                "Chart lacks an integral coordinate-selection inverse")
    require(all(all(x in (0,1) for x in row) and sum(row) <= 1 for row in basis),
            "Chart is not an original unit coordinate identification")
    rows = matrix(sym["rows"], len(raw), 3*n+d)
    rebuilt = tuple(tuple(r[c]+sum(r[3*n+i]*off[i][c] for i in range(ambient)) for c in range(3*n))
                    + tuple(sum(r[3*n+i]*basis[i][c] for i in range(ambient)) for c in range(d))
                    for r in raw)
    require(Counter(rebuilt) == Counter(rows), "Missing/changed original boundary-linear rhombus after substitution")
    good, equalities, labels = boundary_constraints(n, mask, d)
    verify_chart_affine_hull(raw,off,basis,free,closed,equalities)
    # Every original hive satisfies these full affine identities by the adopted
    # forcing premise. Conversely every point of the full substituted system
    # is an original hive, by literal substitution; no feasibility is guessed.
    # Integer O/C and the original-coordinate inverse preserve the whole lattice.
    kept = list(range(len(rows)))
    if "boundary_labels" in reduction:
        expected_labels = [["gap",*label[1:]] if label[0] == "partition_gap" else label for label in labels]
        require(reduction["boundary_labels"] == expected_labels, "Boundary inequality label/order mismatch")
    steps = reduction["steps"]
    require(isinstance(steps, list), "Missing sequential implication roster")
    for step in steps:
        deadline.check()
        removed = integer(step["removed_row"] if d == 4 else step["removed"])
        require(removed in kept, "Removal uses absent/already removed full row")
        others = [i for i in kept if i != removed]
        declared = step["remaining_source_rows"] if d == 4 else step["others"]
        require(ints(declared) == tuple(others), "Implication uses a stale or incomplete retained-row roster")
        if "boundary_inequality_labels" in step:
            require(step["boundary_inequality_labels"] == labels, "Implication boundary label mismatch")
        certificate = step["certificate"]
        verify_implication(rows[removed], good + tuple(rows[i] for i in others), equalities,
                           certificate["nonnegative_multipliers"] if d == 4 else certificate["nonnegative"],
                           certificate["equality_multipliers"] if d == 4 else certificate["equalities"])
        kept.remove(removed)
    require(ints(reduction["kept_rows"] if d == 4 else reduction["kept"]) == tuple(kept),
            "Final retained full row roster differs from sequential removal")
    normals = tuple(sorted({N.primitive(rows[i][3*n:]) for i in kept if any(rows[i][3*n:])}))
    require(normals == matrix(reduction["normals"], width=d), "Wrong final retained primitive normal set")
    for normal in normals:
        require(sum(x*x for x in normal) <= 6 and sum(max(x,0) for x in normal) <= 2
                and sum(max(-x,0) for x in normal) <= 2, "Retained normal violates adopted short-normal premise")
    return {"rank": n, "mask": mask, "coordinate_bound": d, "closed_rows_mask": closed,
            "original_rhombi": len(raw), "integer_selection": list(free),
            "full_affine_implications": len(steps), "retained_full_rows": kept,
            "normal_count": len(normals), "normal_sha256": jd(normals),
            "short_normal_hypotheses":{"all_retained_directions_primitive":True,
                "maximum_squared_norm":max(sum(x*x for x in row) for row in normals),
                "maximum_positive_mass":max(sum(max(x,0) for x in row) for row in normals),
                "maximum_negative_mass":max(sum(max(-x,0) for x in row) for row in normals),
                "fixed_metric":[[int(i == j) for j in range(d)] for i in range(d)],
                "lattice":"the proved original integer-selection chart Z^"+str(d),
                "hypothesis_scope":"primitive facets of the full-dimensional retained presentation; no ambient-rank top-coefficient shortcut",
                "adopted_theorem_source":"packet:"+SHORT_NORMAL_PROOF},
            "actual_degree": "not inferred from coordinate bound"}


def type_metadata(record, stage):
    U = matrix(record["representative_normals"], width=5)
    q = len(U)
    # The P08 bank also retains three auxiliary types (one q1 and two q2).
    # Replay their complete traces; they are not extra c1/c2 occurrences.
    require(q in ((3,4) if stage == "p07" else (1,2,3,4)), "Type is outside the exact source dimension roster")
    index = integer(record["normal_index"])
    require(index > 0, "Nonpositive type index")
    if stage == "p07":
        kind = "saturated_gram" if index == 1 else "literal_ambient"
        target = matrix(record["normal_gram"], q, q) if index == 1 else U
    else:
        require(stage == "p08", "Unknown type source family")
        kind = record["kind"]
        require(kind in ("saturated_gram", "signed_ambient"), "Unknown complete type identity")
        require(integer(record["dimension"]) == q, "Type dimension metadata mismatch")
        target = matrix(record["normal_gram"], q, q) if kind == "saturated_gram" else matrix(record["canonical_normals"], q, 5)
        require(record["payload"] == [kind, [list(row) for row in target]], "Type payload does not bind its full metric/lattice embedding")
        require(N.digest(json.dumps(record["payload"], separators=(",", ":")).encode()) == record["key"],
                "Type key does not hash its exact payload")
    require((kind == "saturated_gram") == (index == 1), "Unsaturated type incorrectly uses Gram-only identity")
    return U, q, kind, target, index, rational(record["alpha"])


def verify_complete_type(record, stage, deadline):
    U, q, kind, target, index, alpha = type_metadata(record, stage)
    require(N.lattice_index(U) == index, "Type representative integer index mismatch")
    full = record["full_laurent"]
    if kind == "saturated_gram":
        p = perm(record["generator_permutation"] if stage == "p07" else record["representative_generator_permutation"], q)
        require(N.gram(tuple(U[i] for i in p)) == target, "Changed type representative Gram embedding")
        trace = full
        require(matrix(trace["tangent_rays"], q, q) == N.eye(q)
                and N.qmatrix(trace["metric"], q, q) == N.inverse(target), "Incorrect saturated type trace lattice/metric")
    else:
        require(N.lattice_index(target) == index and N.signed_match(U, target),
                "Changed unsaturated type full signed integer embedding")
        M = matrix(full["normal_basis_columns"], 5, q)
        C = matrix(full["normal_coordinates"], q, q)
        require(N.lattice_index(N.transpose(M)) == 1, "Unsaturated full normal-plane basis")
        require(Counter(N.primitive(row) for row in N.matmul(C, N.transpose(M)))
                == Counter(N.primitive(row) for row in target), "Normal coordinates do not give the literal full cone")
        require(N.determinant(C) != 0, "Dependent full normal coordinates")
        require(len(full["cells"]) == 1, "Only a single complete simplicial type cell is supported")
        cell = full["cells"][0]
        p = perm(cell["ids"], q)
        tri = full["triangulation"]
        require(ints(tri["extreme_ray_ids"]) == tuple(range(q)), "Missing extreme normal ray")
        facets = [ordered_ids(row, q, q-1) for row in tri["facet_ray_ids"]]
        require(len(facets) == q and set(facets) == set(combinations(range(q), q-1)), "Incomplete simplicial facet roster")
        simplices = [perm(row, q) for row in tri["simplices"]]
        require(simplices == [p], "Missing/duplicate complete simplicial cell")
        ordered = tuple(C[i] for i in p)
        rays = tuple(N.primitive(row) for row in N.transpose(N.inverse(ordered)))
        metric = N.inverse(N.gram(N.transpose(M)))
        trace = cell["laurent"]
        require(rays == matrix(trace["tangent_rays"], q, q), "Changed primitive polar rays or cell permutation")
        require(metric == N.qmatrix(full["tangent_metric"], q, q)
                == N.qmatrix(trace["metric"], q, q), "Changed actual induced lattice metric")
        require(rational(cell["alpha"]) == rational(full["alpha"]) == alpha, "Whole-cell constant mismatch")
    result = N.verify_trace(trace, deadline)
    require(rational(result["alpha"]) == alpha, "Type scalar differs from complete Laurent recurrence")
    # Negative raw complete local types are retained; a type is not a whole LR
    # coefficient and is not rejected merely for having a negative constant.
    return {"q": q, "normal_index": index, "kind": kind, "local_only": True, **result}


def bind_type(U, binding, record, stage):
    rep, q, kind, target, index, alpha = type_metadata(record, stage)
    require(len(U) == q and N.lattice_index(U) == integer(binding["normal_index"]) == index,
            "Occurrence/type full integer index mismatch")
    if kind == "saturated_gram":
        p = perm(binding["generator_permutation"], q)
        require(N.gram(tuple(U[i] for i in p)) == target, "Occurrence/type Gram mismatch")
    elif stage == "p07":
        require(U == rep, "P07 higher-index occurrence is not its literal normal embedding")
        if "generator_permutation" in binding:
            perm(binding["generator_permutation"], q)
    else:
        p, c = perm(binding["generator_permutation"], q), perm(binding["coordinate_permutation"], 5)
        signs = ints(binding["coordinate_signs"], 5)
        require(all(s in (-1,1) for s in signs), "Invalid signed integer coordinate isometry")
        require(tuple(tuple(signs[j]*U[i][c[j]] for j in range(5)) for i in p) == target,
                "Occurrence/type complete signed integer embedding mismatch")
    return alpha


def verify_compact_three(record, deadline):
    """Exact q3 formula: complete fundamental numerator minus all 3 edges.

    M spans the saturated normal plane, A=C M^T, and its induced metric is
    (M^T M)^-1. The supplied points are proved to be the ENTIRE half-open
    parallelepiped by index, uniqueness and containment. No BFS/search is used.
    The reciprocal exponential is computed as a formal series, independently
    of the returned evaluator's Bernoulli constants/table implementation.
    """
    U = matrix(record["normal_rows"], 3, 4)
    require(N.lattice_index(U) > 0 and all(N.primitive(row) == row for row in U), "Invalid compact normal triple")
    edge_direction = ints(record["primitive_edge_direction"], 4)
    require(N.primitive(edge_direction) == edge_direction and all(sum(a*b for a,b in zip(row, edge_direction)) == 0 for row in U),
            "Compact edge is not the complete primitive kernel line")
    M = matrix(record["saturated_normal_basis"], 4, 3, True)
    C = matrix(record["integer_normal_coordinates"], 3, 3, True)
    require(N.lattice_index(N.transpose(M)) == 1, "Compact normal-plane basis is unsaturated")
    require(all(sum(M[i][j]*edge_direction[i] for i in range(4)) == 0 for j in range(3)),
            "Compact normal-plane basis does not annihilate its edge")
    require(N.matmul(C, N.transpose(M)) == U and abs(N.determinant(C)) == N.lattice_index(U),
            "Compact exact normal lattice embedding mismatch")
    rays = tuple(N.primitive(row) for row in N.transpose(N.inverse(C)))
    require(rays == matrix(record["primitive_tangent_rays"], 3, 3), "Compact primitive polar rays mismatch")
    require(abs(N.determinant(rays)) == integer(record["tangent_lattice_index"]), "Compact tangent index mismatch")
    points = [list(ints(row, 3, True)) for row in record["fundamental_points"]]
    points = N.check_fundamental_points(rays, points)
    xi = tuple(rational(x) for x in record["generic_covector"])
    require(len(xi) == 3, "Compact covector dimension mismatch")
    ev = [sum(x*y for x,y in zip(ray, xi)) for ray in rays]
    require(all(ev), "Nongeneric compact Laurent covector")
    series = [sum(sum(x*y for x,y in zip(point, xi))**k for point in points)/Q(factorial(k)) for k in range(4)]
    for value in ev:
        deadline.check()
        series = N.multiply_series(series, N.exponential_denominator(value, 3), 3)
    constant = series[3]
    metric = N.inverse(N.gram(N.transpose(M)))
    def dot(a,b):
        return sum(a[i]*metric[i][j]*b[j] for i in range(3) for j in range(3))
    subtraction, indices = Q(0), []
    for i,j in combinations(range(3),2):
        deadline.check()
        index = N.lattice_index((rays[i],rays[j]))
        require(index > 0, "Dependent compact face")
        rr, ss, rs = dot(rays[i],rays[i]), dot(rays[j],rays[j]), dot(rays[i],rays[j])
        require(rr > 0 and ss > 0, "Invalid compact induced metric")
        subtraction += (ev[j]-rs*ev[i]/rr)/(24*index*ev[i]) + (ev[i]-rs*ev[j]/ss)/(24*index*ev[j])
        indices.append(index)
    require(ints(record["facet_indices"], 3) == tuple(indices), "Incomplete/wrong compact face-index roster")
    require(constant == rational(record["cone_laurent_constant"]), "Compact complete fundamental numerator constant mismatch")
    require(subtraction == rational(record["complete_edge_subtraction"]), "Compact complete edge subtraction mismatch")
    alpha = constant-subtraction
    require(alpha == rational(record["alpha"]), "Compact complete local alpha mismatch")
    return {"q": 3, "normal_index": N.lattice_index(U), "alpha": str(alpha),
            "fundamental_points": len(points), "edge_subtractions": 3, "local_only": True}


def correction_supports(certificate, normals, coefficient):
    d, q = len(normals[0]), len(normals[0])-coefficient
    co = certificate["correction"]
    require(co["status"] in ("ALREADY_STRICT", "EXACT_STRICT"), "Unfinished correction is not a certificate")
    support_rows = co["supports"]
    weights = tuple(rational(x) for x in co["coefficients"])
    require(len(weights) == len(support_rows)*(coefficient+1), "Incomplete correction coefficient vector")
    out = {}
    for number, row in enumerate(support_rows):
        ids = ordered_ids(row["normals"], len(normals), q-1)
        require(ids not in out and N.lattice_index(tuple(normals[i] for i in ids)) > 0,
                "Duplicate/dependent correction support")
        K = matrix(row["saturated_kernel_columns"], d, coefficient+1)
        require(N.lattice_index(N.transpose(K)) == 1, "Unsaturated correction support kernel")
        require(all(sum(normals[i][j]*K[j][k] for j in range(d)) == 0 for i in ids for k in range(coefficient+1)),
                "Correction support does not annihilate its exact normal subset")
        h = weights[number*(coefficient+1):(number+1)*(coefficient+1)]
        out[ids] = (number, K, h)
    nonzero = [i for i in range(len(support_rows)) if any(weights[i*(coefficient+1):(i+1)*(coefficient+1)])]
    require(integer(co["nonzero_support_count"]) == len(nonzero), "Incorrect nonzero-support count")
    if "used_support_ids" in co:
        require(ints(co["used_support_ids"]) == tuple(nonzero), "Missing/repeated nonzero support identity")
    if not support_rows:
        require(not co.get("incidence") and not co.get("corrected_values"), "Unexpected correction values without any support")
    return out


def apply_correction(normals, ids, raw, supports):
    value, events = raw, []
    for face in combinations(ids, len(ids)-1):
        if face not in supports:
            continue                         # the declared global functional is zero here
        number, K, h = supports[face]
        extra = next(i for i in ids if i not in face)
        restricted = [sum(normals[extra][j]*K[j][k] for j in range(len(normals[0]))) for k in range(len(h))]
        divisor = gcd(*restricted)
        require(divisor > 0, "Correction extra normal vanishes in the saturated quotient")
        require(N.lattice_index(tuple(normals[i] for i in ids)) == N.lattice_index(tuple(normals[i] for i in face))*divisor,
                "Restricted gcd disagrees with full lattice index ratio")
        primitive = [x//divisor for x in restricted]
        value += sum(x*y for x,y in zip(primitive,h))
        events.append({"support": number, "extra": extra, "primitive_quotient": primitive})
    return value, events


def preserve_local_result(raw, corrected, events):
    return {"raw": str(raw), "corrected": str(corrected), "primitive_incidences": len(events),
            "raw_negative": raw < 0, "raw_zero": raw == 0, "strictly_positive": corrected > 0,
            "scope": "complete local normal cone; not a whole LR coefficient"}


def reverse_bits(word, width):
    return sum(((word >> i) & 1) << (width-1-i) for i in range(width))


def apply_word(mask, n, word):
    w = n-1
    require(type(mask) is int and 0 <= mask < 1 << (3*w), "Mask outside exact source universe")
    if "dual" in word:
        dual, outer, inners = word["dual"], word["outer"], word["inners"]
    else:
        dual, outer, inners = word["simultaneous_dual"], word["new_outer_factor"], word["ordered_inner_factors"]
    dual, outer = integer(dual), integer(outer)
    inners = ints(inners, 2)
    require(dual in (0,1) and sorted((outer, *inners)) == [0,1,2], "Invalid tensor mask word")
    sides = [(mask >> (i*w)) & ((1 << w)-1) for i in range(3)]
    invariant = [sides[1], sides[2], reverse_bits(sides[0], w)]
    if dual:
        invariant = [reverse_bits(x,w) for x in invariant]
    return reverse_bits(invariant[outer],w) | (invariant[inners[0]] << w) | (invariant[inners[1]] << (2*w))


def word_key(word):
    if "dual" in word:
        return (integer(word["dual"]), integer(word["outer"]), *ints(word["inners"],2))
    return (integer(word["simultaneous_dual"]), integer(word["new_outer_factor"]), *ints(word["ordered_inner_factors"],2))


def words(mask, n):
    for dual in (0,1):
        for outer, first, second in permutations(range(3)):
            word = {"dual": dual, "outer": outer, "inners": [first,second]}
            yield apply_word(mask,n,word), word


def member_map(roster, d):
    result = {}
    for record in roster:
        n = integer(record["rank"])
        mask = integer(record["representative_mask"] if d == 4 else record["mask"])
        members = record["orbit_members"] if d == 4 else record["members"]
        ordered_ids(members, 1 << (3*(n-1)))
        require(mask in members, "Representative is absent from its own source orbit")
        for member in members:
            key = (n,member)
            require(key not in result, "Overlapping source orbit/member roster")
            result[key] = mask
    return result


def accepted_table(sources, n):
    cache_key = ("accepted_table", n)
    if cache_key not in sources.cache:
        obj = sources.read(f"f025:{n}")
        require(integer(obj["rank"]) == n, "Wrong rank in accepted F025 source")
        count = 1 << (3*(n-1))
        require(integer(obj["start"]) == 0 and integer(obj["stop"]) == count, "Incomplete accepted F025 mask interval")
        result = unique_map(obj["records"], lambda r: integer(r["mask"]), range(count))
        for rec in result.values():
            dim, closed = integer(rec["dimension_bound"]), integer(rec["closed_rows_mask"])
            require(0 <= dim <= (n-1)*(n-2)//2 and 0 <= closed < 1 << (3*n*(n-1)//2),
                    "Out-of-range accepted mask fields")
        sources.cache[cache_key] = result
    return sources.cache[cache_key]


def source_ref(key, index=None):
    return {"source": key, "index": index}


def read_ref(sources, ref):
    obj = sources.read(ref["source"])
    if ref["index"] is not None:
        i = integer(ref["index"])
        require(isinstance(obj, list) and 0 <= i < len(obj), "Source record selector is stale")
        return obj[i]
    return obj


def presentation_key(record, d):
    return (integer(record["rank"]), integer(record["representative_mask"] if d == 4 else record["mask"]))


def coefficient_map(record):
    return unique_map(record["certificates"], lambda c: integer(c["coefficient"]), (1,2))


def initial_sources(stage):
    names = [name for name in SOURCE if name.startswith(stage + "_")]
    if stage == "p08":
        names += [name for name in SOURCE if name.startswith("p07_")]
    return names


def freeze(args, deadline):
    stage = args.stage
    external = {f"f025:{n}": str(Path(getattr(args, f"f025_r{n}")).resolve())
                for n in (6,7) if getattr(args, f"f025_r{n}")}
    required_ranks = (6,7) if stage == "p06" else (6,)
    for n in required_ranks:
        if f"f025:{n}" not in external:
            raise CannotCheck(f"freeze {stage} requires --f025-r{n} with the accepted full table")
    sources = Sources(args.root, external)
    for name in initial_sources(stage):
        deadline.check()
        key = "packet:" + SOURCE[name]
        data = sources.bytes(key)
        if name in PINS:
            require(N.digest(data) == PINS[name], f"Frozen source is not the declared captured version: {name}")
    for n in required_ranks:
        data = sources.bytes(f"f025:{n}")
        require(N.digest(data) == PINS[f"f025:{n}"], "Accepted F025 input is a different source version")
    for proof in premise_paths(stage):
        sources.bytes("packet:" + proof)

    d = 4 if stage == "p06" else 5
    boundary = sources.named(stage + "_boundary")
    expected = {(n,m) for n, masks in P06_MASKS.items() for m in masks} if d == 4 else {(6,m) for m in (P07_MASKS if stage == "p07" else P08_MASKS)}
    by_boundary = unique_map(boundary, lambda r: presentation_key(r,d), expected)
    membership = member_map(boundary,d)
    require(len(membership) == {"p06":246,"p07":24,"p08":1275}[stage], "Wrong unique exact mask population")
    if stage == "p06":
        roster = sources.named("p06_roster")
        unique_map(roster,lambda r:presentation_key(r,4),expected)
        require(member_map(roster,4) == membership, "P06 frozen roster disagrees with certificate members")
    elif stage == "p07":
        roster = sources.named("p07_roster")
        full = unique_map(roster,lambda r:presentation_key(r,5),{(6,m) for m in P08_MASKS})
        require(sum(len(x["members"]) for x in full.values()) == 1275, "Wrong full P07 selector population")
        require(member_map([full[6,m] for m in P07_MASKS],5) == membership, "P07 two-presentation selector differs")
    else:
        old = unique_map(sources.named("p07_boundary"),lambda r:presentation_key(r,5),{(6,m) for m in P07_MASKS})
        for mask in P07_MASKS:
            for field in ("symbolic_chart","reduction","members"):
                require(old[6,mask][field] == by_boundary[6,mask][field], "P08 inherited P07 chart/presentation is stale")

    type_jobs, cycles = [], {}
    if stage == "p07":
        cycle_list = sources.named("p07_cycles")
        unique_map(cycle_list,lambda r:presentation_key(r,5),expected)
        for i, rec in enumerate(cycle_list):
            cycles[presentation_key(rec,5)] = source_ref("packet:"+SOURCE["p07_cycles"],i)
        types = sources.named("p07_types")
        require(len(types) == 2571, "Wrong complete P07 type population")
        for i, rec in enumerate(types):
            require(integer(rec["type_id"]) == i, "P07 positional type identity is stale/repeated")
            type_jobs.append({"id": f"p07:T{i}", "ref": source_ref("packet:"+SOURCE["p07_types"],i)})
    elif stage == "p08":
        cert_index = sources.named("p08_cert_index")
        type_index = sources.named("p08_type_index")
        require(len(cert_index) == 123 and len(type_index) == 4790, "Incomplete P08 finite source index")
        for index, is_type in ((cert_index,False),(type_index,True)):
            seen = set()
            for entry in index:
                deadline.check()
                path = entry["path"]
                require(isinstance(path,str) and path not in seen, "Repeated/malformed P08 index path")
                seen.add(path)
                pattern = r"DATA/TYPES/([0-9a-f]{64})\.json\.gz" if is_type else r"DATA/J0[234]/M([0-9]+)-CERTIFICATE\.json\.gz"
                match = re.fullmatch(pattern,path)
                require(match is not None, "Unexpected P08 index path or source family")
                key = "packet:"+P08+"/"+path
                sources.bytes(key)
                require(sources.reads[key] == {"bytes":integer(entry["bytes"]),"sha256":entry["sha256"]}, "P08 indexed byte hash/size mismatch")
                if is_type:
                    type_jobs.append({"id":"p08:"+match[1],"ref":source_ref(key)})
                else:
                    mask = int(match[1])
                    require(mask not in P07_MASKS and (6,mask) not in cycles, "Duplicate/inherited P08 certificate identity")
                    rec = sources.read(key)
                    require(presentation_key(rec,5) == (6,mask), "P08 source filename and literal mask differ")
                    cycles[6,mask] = source_ref(key)
        require(set(cycles) == expected-{(6,m) for m in P07_MASKS}, "Missing exact P08 complementary presentation")
        type_jobs.sort(key=lambda r:r["id"])
    else:
        types = sources.named("p06_types")
        require(len(types) == 2535, "Wrong exact P06 compact triple population")
        seen = set()
        for i, rec in enumerate(types):
            normals = matrix(rec["normal_rows"],3,4)
            require(normals not in seen, "Duplicate P06 literal compact triple")
            seen.add(normals)
            type_jobs.append({"id":"p06:Q3:"+jd(normals),"normals":[list(row) for row in normals],
                              "ref":source_ref("packet:"+SOURCE["p06_types"],i)})

    presentations, obligations = [], []
    for i, rec in enumerate(boundary):
        deadline.check()
        rank, mask = presentation_key(rec,d)
        pid = f"{rank}:{mask}"
        item = {"id":pid,"rank":rank,"mask":mask,"dimension":d,
                "boundary":source_ref("packet:"+SOURCE[stage+"_boundary"],i),
                "normal_count":len(rec["reduction"]["normals"]),
                "members":rec["orbit_members"] if d == 4 else rec["members"]}
        if stage == "p06":
            red = rec["reduction"]
            require(isinstance(red["negative_triples"],list) and isinstance(red["zero_triples"],list),
                    "Missing P06 negative/zero triple source lists")
            item["cycle"] = item["boundary"]
            coef_targets = {1:{"independent":integer(red["independent_triples"]),
                              "raw_negative":len(red["negative_triples"]),
                              "raw_zero":len(red["zero_triples"]),
                              "raw_minimum":str(rational(red["minimum_alpha"])),
                              "minimum":str(rational(red["minimum_alpha"]))}}
        elif (rank,mask) in cycles:
            item["cycle"] = cycles[rank,mask]
            cycle = read_ref(sources,item["cycle"])
            require(cycle["normals"] == rec["reduction"]["normals"], "Cycle source/retained boundary normal set mismatch")
            if stage == "p08":
                require(cycle["members"] == rec["members"], "P08 literal member roster differs between sources")
            coef_targets = {}
            for coefficient, c in coefficient_map(cycle).items():
                require(len(c["cones"]) == len(c["alphas"]) == len(c["type_bindings"]), "Incomplete frozen cone/scalar/type arrays")
                coef_targets[coefficient] = {"independent":len(c["cones"]),
                    "raw_negative":integer(c["negative_cones"]),"raw_zero":integer(c["zero_cones"]),
                    "raw_minimum":str(rational(c["uncorrected_minimum"])),"minimum":str(rational(c["correction"]["minimum"]))}
        else:
            item["adopted_from"] = "p07"
            coef_targets = {}
        for coefficient, targets in sorted(coef_targets.items()):
            q = d-coefficient
            obligations.append({"id":f"cones/{pid}/c{coefficient}","kind":"cones","presentation":pid,
                                "coefficient":coefficient,"q":q,"total":comb(item["normal_count"],q),"targets":targets})
        presentations.append(item)
    presentations.sort(key=lambda r:(r["rank"],r["mask"]))
    obligations.insert(0,{"id":"boundary","kind":"boundary","total":len(presentations)})
    obligations.append({"id":"types","kind":"types","total":len(type_jobs)})
    for n in required_ranks:
        total = 24 if stage == "p07" else 1 << (3*(n-1))
        obligations.append({"id":f"scope/{n}","kind":"scope","rank":n,"total":total})
    sources.unchanged()
    return {"schema":SCHEMA,"kind":"manifest","status":"FROZEN_INPUTS_ONLY","stage":stage,
            "checker_versions":checker_versions(),"root_at_freeze":str(sources.root),"external":external,
            "sources":dict(sorted(sources.reads.items())),"presentations":presentations,"types":type_jobs,
            "obligations":obligations,"requires_p07_adoption":stage == "p08","premises":PREMISES,
            "whole_polynomial_bridge":whole_polynomial_bridge(d),
            "source_claim_ids":{"p06":["FR027-P06-T003"],"p07":["FR027-P07-T001","FR027-P07-T002"],"p08":["FR027-P08-T001"]}[stage],
            "scope":"finite sufficient coordinate-mask criteria; inherited and analytic premises remain explicit"}


def checked_type_id(manifest, binding):
    if manifest["stage"] == "p07":
        return f"p07:T{integer(binding['type_id'])}"
    require(manifest["stage"] == "p08" and isinstance(binding["type_key"],str), "Wrong occurrence type family")
    return "p08:"+binding["type_key"]


class Work:
    def __init__(self, manifest, sources, deadline):
        self.manifest, self.sources, self.deadline = manifest, sources, deadline
        self.types = unique_map(manifest["types"],lambda r:r["id"])
        self.presentations = unique_map(manifest["presentations"],lambda r:r["id"])
        self.prepared = {}

    def type(self, identity):
        require(identity in self.types, f"Missing declared complete type: {identity}")
        rec = read_ref(self.sources,self.types[identity]["ref"])
        if self.manifest["stage"] == "p07":
            require(identity == f"p07:T{integer(rec['type_id'])}", "Stale positional P07 type identity")
        elif self.manifest["stage"] == "p08":
            require(identity == "p08:"+rec["key"], "Type filename/key/occurrence mismatch")
        return rec

    def boundary(self, ordinal):
        p = self.manifest["presentations"][ordinal]
        record = read_ref(self.sources,p["boundary"])
        require(presentation_key(record,p["dimension"]) == (p["rank"],p["mask"]), "Stale boundary record selector")
        answer = verify_boundary(record,accepted_table(self.sources,p["rank"])[p["mask"]],p["dimension"],self.deadline)
        require(answer["normal_count"] == p["normal_count"], "Boundary normal count changed after freeze")
        return {"id":p["id"],"source":p["boundary"],**answer}

    def type_job(self, ordinal):
        job = self.manifest["types"][ordinal]
        rec = self.type(job["id"])
        if self.manifest["stage"] == "p06":
            require(matrix(rec["normal_rows"],3,4) == matrix(job["normals"],3,4), "Compact type selector changed its literal normal triple")
            answer = verify_compact_three(rec,self.deadline)
        else:
            answer = verify_complete_type(rec,self.manifest["stage"],self.deadline)
        return {"id":job["id"],"source":job["ref"],**answer}

    def prepare_cones(self, obligation):
        key = obligation["id"]
        if key in self.prepared:
            return self.prepared[key]
        p = self.presentations[obligation["presentation"]]
        rec = read_ref(self.sources,p["cycle"])
        bd = read_ref(self.sources,p["boundary"])
        require(presentation_key(rec,p["dimension"]) == (p["rank"],p["mask"]), "Stale cone presentation identity")
        normals = matrix(bd["reduction"]["normals"],width=p["dimension"])
        require(normals == tuple(sorted(set(normals))) and all(N.primitive(row) == row for row in normals), "Repeated/unsorted/nonprimitive retained normal set")
        if self.manifest["stage"] != "p06":
            require(matrix(rec["normals"],width=5) == normals, "Cone source has stale retained normal embedding")
        require(len(normals) == p["normal_count"], "Stale retained normal count")
        q, c = obligation["q"], obligation["coefficient"]
        require(comb(len(normals),q) == obligation["total"], "Candidate combination interval is stale")
        candidates = list(combinations(range(len(normals)),q))
        if self.manifest["stage"] == "p06":
            compact = {matrix(job["normals"],3,4):job["id"] for job in self.manifest["types"]}
            data = {"p":p,"normals":normals,"candidates":candidates,"compact":compact}
        else:
            certificate = coefficient_map(rec)[c]
            ids = [ordered_ids(x,len(normals),q) for x in certificate["cones"]]
            require(ids == sorted(set(ids)), "Repeated/unsorted cone subset source roster")
            require(len(ids) == len(certificate["alphas"]) == len(certificate["type_bindings"])
                    == obligation["targets"]["independent"], "Incomplete cone arrays or frozen count")
            co = certificate["correction"]
            supports = correction_supports(certificate,normals,c)
            if supports:
                require(len(co["incidence"]) == len(co["corrected_values"]) == len(ids), "Incomplete correction incidence/value roster")
            if "constrained_full_independent_subsets" in co:
                require(integer(co["constrained_full_independent_subsets"]) == len(ids), "Correction drops raw-positive constraints")
            data = {"p":p,"normals":normals,"candidates":candidates,"certificate":certificate,
                    "positions":dict(zip(ids,range(len(ids)))),"supports":supports}
        self.prepared[key] = data
        return data

    def cone(self, obligation, ordinal):
        data = self.prepare_cones(obligation)
        ids, normals = data["candidates"][ordinal], data["normals"]
        U = tuple(normals[i] for i in ids)
        index = N.lattice_index(U)
        identity = obligation["presentation"]+f":c{obligation['coefficient']}:"+",".join(map(str,ids))
        base = {"id":identity,"normal_ids":list(ids),"independent":index > 0,"normal_index":index,
                "source":data["p"]["cycle"],"normal_sha256":jd(normals)}
        if not index:
            require(self.manifest["stage"] == "p06" or ids not in data["positions"], "Source includes a dependent tuple as an independent cone")
            return base
        if self.manifest["stage"] == "p06":
            require(U in data["compact"], "Missing complete compact certificate for an independent retained triple")
            tid = data["compact"][U]
            record = self.type(tid)
            require(matrix(record["normal_rows"],3,4) == U, "Compact literal type binding mismatch")
            raw = rational(record["alpha"])
            corrected, events = raw, []
        else:
            require(ids in data["positions"], "Omitted independent subset (including a raw-positive cone)")
            number = data["positions"][ids]
            certificate = data["certificate"]
            binding = certificate["type_bindings"][number]
            tid = checked_type_id(self.manifest,binding)
            raw = bind_type(U,binding,self.type(tid),self.manifest["stage"])
            require(raw == rational(certificate["alphas"][number]), "Occurrence raw scalar is not bound to its full type")
            corrected, events = apply_correction(normals,ids,raw,data["supports"])
            if data["supports"]:
                co = certificate["correction"]
                stored = co["incidence"][number]
                require(isinstance(stored,list), "Malformed incidence row")
                normalized = []
                for event in stored:
                    require(set(event) == {"support","extra","primitive_quotient"}, "Unexpected/dropped incidence field")
                    normalized.append({"support":integer(event["support"]),"extra":integer(event["extra"]),
                                       "primitive_quotient":list(ints(event["primitive_quotient"],obligation["coefficient"]+1))})
                require(normalized == events, "Incomplete/wrong primitive incidence, including positive affected cones")
                require(corrected == rational(co["corrected_values"][number]), "Wrong complete corrected local scalar")
        answer = {**base,"type_id":tid,**preserve_local_result(raw,corrected,events)}
        if self.manifest["stage"] == "p08" and obligation["coefficient"] == 1:
            answer["declared_margin_satisfied"] = corrected > Q(1,60000)
        return answer

    def prepare_scope(self, n):
        key = ("scope",n)
        if key in self.prepared:
            return self.prepared[key]
        stage = self.manifest["stage"]
        table = accepted_table(self.sources,n)
        boundary = self.sources.named(stage+"_boundary")
        members = member_map(boundary,4 if stage == "p06" else 5)
        data = {"table":table,"members":members}
        if stage == "p07":
            doc = self.sources.named("p07_words")
            require(integer(doc["rank_padding"]) == 6 and integer(doc["exact_patterns"]) == 24, "Stale P07 word summary")
            wm = unique_map(doc["words"],lambda r:integer(r["mask"]),[m for rank,m in members if rank == n])
            data["word_map"], data["order"] = wm, sorted(wm)
        elif stage == "p08":
            word_list = self.sources.named("p08_words")
            data["word_map"] = unique_map(word_list,lambda r:integer(r["mask"]))
            scope = self.sources.named("p08_scope")
            require(scope["source_score_sha256"] == self.sources.reads["f025:6"]["sha256"], "P08 scope uses a stale F025 source")
            remaining = ordered_ids(scope["remaining_masks"],1 << 15)
            require(len(data["word_map"]) == 31613 and len(remaining) == 1155
                    and set(data["word_map"]).isdisjoint(remaining)
                    and set(data["word_map"]) | set(remaining) == set(range(1 << 15)), "Incomplete/overlapping P08 source mask partition")
            data["remaining"] = set(remaining)
        else:
            metric = self.sources.named("p06_metric")
            strata = unique_map(metric["strata"],lambda r:integer(r["rank"]),(6,7))
            st = strata[n]
            full = unique_map(st["verified_bindings"],lambda r:integer(r["mask"]))
            old = unique_map(st["exact_source_mask_words"],lambda r:integer(r[0]))
            new = {m:rep for (rank,m),rep in members.items() if rank == n}
            expected_counts = {6:(1911,1887,24),7:(20606,20384,222)}[n]
            require((len(full),len(old),len(new)) == expected_counts and not set(old)&set(new)
                    and set(old)|set(new) == set(full), "Incomplete/overlapping P06 old/new exact-four mask partition")
            data.update(full=full,old=old,new=new)
        self.prepared[key] = data
        return data

    def scope(self, n, ordinal):
        data = self.prepare_scope(n)
        stage = self.manifest["stage"]
        mask = data["order"][ordinal] if stage == "p07" else ordinal
        source_bound = integer(data["table"][mask]["dimension_bound"])
        orbit = list(words(mask,n))
        images = {image for image,_ in orbit}
        if stage == "p07":
            record = data["word_map"][mask]
            dest = integer(record["representative"])
            require(dest == data["members"][n,mask] and dest in P07_MASKS
                    and apply_word(mask,n,record["word"]) == dest, "Wrong P07 exact mask-to-presentation word")
            matching = {word_key(word) for image,word in orbit if image == dest}
            claimed = [word_key(word) for word in record["all_matching_words"]]
            require(len(claimed) == len(set(claimed)) and set(claimed) == matching, "Missing/duplicate P07 matching tensor word")
            require(source_bound == 5 and integer(data["table"][dest]["dimension_bound"]) == 5,
                    "P07 exact-five domain has a stale source dimension")
            require({m for m,_ in words(dest,n)} == {m for (rank,m),rep in data["members"].items() if rank == n and rep == dest},
                    "P07 finite exact orbit roster is incomplete")
            return {"id":f"{n}:{mask}","role":"new_five","destination":dest,"source_bound":source_bound,
                    "word":record["word"],"additional_zero_gaps":"closed-domain analytic premise"}
        if stage == "p08":
            best = min(integer(data["table"][image]["dimension_bound"]) for image in images)
            is_member = (n,mask) in data["members"]
            require(is_member == (source_bound == 5 and best == 5), "Full 125-presentation selector omits/adds an exact residual-five mask")
            if best > 5:
                require(mask in data["remaining"] and mask not in data["word_map"], "Uncovered mask silently treated as certified")
                return {"id":f"{n}:{mask}","role":"outside_sufficient_criterion","source_bound":source_bound,"best_bound":best}
            require(mask in data["word_map"] and mask not in data["remaining"], "Missing covered mask/word")
            record = data["word_map"][mask]
            require(integer(record["source_bound"]) == source_bound and integer(record["best_symmetry_bound"]) == best,
                    "Stored source/symmetry coordinate bound is wrong")
            dest = integer(record["destination_mask"])
            require(apply_word(mask,n,record["word"]) == dest and dest in images, "Invalid exact P08 tensor mask transport")
            if best <= 4:
                require(record["terminal"] == "P06_OR_EARLIER_BOUND_AT_MOST_FOUR"
                        and integer(data["table"][dest]["dimension_bound"]) == best, "Wrong inherited lower-coordinate mask terminal")
                role = "prior_lower_coordinate"
            else:
                require(record["terminal"] == "P07_OR_P08_FIVE_COORDINATE_NORMAL_CYCLE" and dest in P08_MASKS,
                        "Missing exact five-coordinate normal-cycle terminal")
                require(integer(data["table"][dest]["dimension_bound"]) == 5, "Wrong destination coordinate bound")
                role = "new_five"
            return {"id":f"{n}:{mask}","role":role,"destination":dest,"source_bound":source_bound,
                    "best_bound":best,"word":record["word"],"source_member":is_member}
        is_four = source_bound == 4
        require((mask in data["full"]) == is_four, "Metric binding does not cover every exact-four F025 mask")
        if not is_four:
            return {"id":f"{n}:{mask}","role":"outside_exact_four","source_bound":source_bound}
        if mask in data["new"]:
            dest = data["new"][mask]
            require(dest in images and dest in P06_MASKS[n]
                    and integer(data["table"][dest]["dimension_bound"]) == 4, "New P06 mask lacks exact accepted transport to a checked presentation")
            word = next(word for image,word in orbit if image == dest)
            return {"id":f"{n}:{mask}","role":"new_four","destination":dest,"word":word}
        old = data["old"][mask]
        require(ints(old,6)[0] == mask and old[1] in images, "Inherited metric-mask source word is stale")
        return {"id":f"{n}:{mask}","role":"prior_metric_branch","exact_prior_source_row":old,
                "acceptance":"previously adopted premise, not newly verified here"}


def validate_manifest(manifest):
    require(manifest["schema"] == SCHEMA and manifest["kind"] == "manifest"
            and manifest["status"] == "FROZEN_INPUTS_ONLY", "Not a completed source freeze")
    stage = manifest["stage"]
    require(stage in ("p06","p07","p08"), "Unknown mask theorem stage")
    require(manifest["checker_versions"] == checker_versions(), "Stale/mixed checker version")
    d = 4 if stage == "p06" else 5
    expected = {(n,m) for n, masks in P06_MASKS.items() for m in masks} if d == 4 else {(6,m) for m in (P07_MASKS if stage == "p07" else P08_MASKS)}
    ps = unique_map(manifest["presentations"],lambda r:(integer(r["rank"]),integer(r["mask"])),expected)
    require([(p["rank"],p["mask"]) for p in manifest["presentations"]] == sorted(expected), "Stale presentation ordinal roster")
    boundary_indices = []
    for key,p in ps.items():
        require(p["id"] == f"{key[0]}:{key[1]}" and integer(p["dimension"]) == d, "Presentation identifier/dimension mismatch")
        require(type(p["normal_count"]) is int and d <= p["normal_count"] <= 64, "Invalid frozen normal count")
        require(p["boundary"]["source"] == "packet:"+SOURCE[stage+"_boundary"], "Wrong boundary source family")
        boundary_indices.append(integer(p["boundary"]["index"]))
        if stage == "p08" and p["mask"] in P07_MASKS:
            require(p.get("adopted_from") == "p07" and "cycle" not in p, "Inherited P07 presentation silently bypassed adoption")
        else:
            require("cycle" in p and "adopted_from" not in p, "Missing numerical presentation obligation")
    require(sorted(boundary_indices) == list(range(len(ps))), "Missing/duplicate boundary source selector")
    tjs = unique_map(manifest["types"],lambda r:r["id"])
    count = {"p06":2535,"p07":2571,"p08":4790}[stage]
    require(len(tjs) == count, "Stale/missing complete type roster")
    if stage == "p07":
        require(list(tjs) == [f"p07:T{i}" for i in range(count)], "P07 positional type roster changed")
    if stage in ("p06","p07"):
        for i, job in enumerate(manifest["types"]):
            require(job["ref"] == source_ref("packet:"+SOURCE[stage+"_types"],i), "Stale/repeated complete type source selector")
            if stage == "p06":
                require(job["id"] == "p06:Q3:"+jd(matrix(job["normals"],3,4)), "Compact literal identity changed")
    else:
        require(list(tjs) == sorted(tjs), "P08 type ordinal order changed")
        for job in manifest["types"]:
            key = job["id"].removeprefix("p08:")
            require(re.fullmatch("[0-9a-f]{64}",key) and job["ref"] == source_ref("packet:"+P08+"/DATA/TYPES/"+key+".json.gz"),
                    "P08 literal type key/source path mismatch")
    obligations = unique_map(manifest["obligations"],lambda r:r["id"])
    expected_obligations = {"boundary","types","scope/6"} | ({"scope/7"} if stage == "p06" else set())
    for p in ps.values():
        if "cycle" in p:
            for c in ((1,) if d == 4 else (1,2)):
                identity = f"cones/{p['id']}/c{c}"
                expected_obligations.add(identity)
                require(identity in obligations, "Missing complete coefficient gate")
                o = obligations[identity]
                require(o["kind"] == "cones" and o["presentation"] == p["id"] and integer(o["coefficient"]) == c
                        and integer(o["q"]) == d-c and integer(o["total"]) == comb(p["normal_count"],d-c),
                        "Stale independent-subset coverage interval")
    require(set(obligations) == expected_obligations, "Omitted/unexpected finite obligation")
    for name,total in (("boundary",len(ps)),("types",count),("scope/6",24 if stage == "p07" else 1 << 15)):
        require(integer(obligations[name]["total"]) == total, "Stale complete obligation total")
    if stage == "p06":
        require(integer(obligations["scope/7"]["total"]) == 1 << 18, "Stale rank-seven source mask universe")
    for name in initial_sources(stage):
        entry = manifest["sources"].get("packet:"+SOURCE[name])
        require(entry is not None and (name not in PINS or entry["sha256"] == PINS[name]), "Missing/stale captured source pin")
    for n in ((6,7) if stage == "p06" else (6,)):
        require(manifest["sources"][f"f025:{n}"]["sha256"] == PINS[f"f025:{n}"], "Stale accepted F025 source pin")
    for proof in premise_paths(stage):
        require("packet:"+proof in manifest["sources"], "Missing explicit analytic proof dependency")
    require(manifest["whole_polynomial_bridge"] == whole_polynomial_bridge(d), "Changed/missing conditional whole-polynomial coefficient bridge")
    for p in ps.values():
        for name in ("boundary","cycle"):
            if name in p:
                require(p[name]["source"] in manifest["sources"], "Unbound presentation source")
    for job in manifest["types"]:
        require(job["ref"]["source"] in manifest["sources"], "Unbound complete type source")
    require(manifest["requires_p07_adoption"] is (stage == "p08"), "Wrong inherited adoption gate")
    return obligations


def expected_identity(manifest, obligation, ordinal, cache):
    kind = obligation["kind"]
    if kind == "boundary":
        return manifest["presentations"][ordinal]["id"]
    if kind == "types":
        return manifest["types"][ordinal]["id"]
    if kind == "scope":
        n = obligation["rank"]
        if manifest["stage"] == "p07":
            if "scope_order" not in cache:
                cache["scope_order"] = sorted(m for p in manifest["presentations"] for m in p["members"])
            ordinal = cache["scope_order"][ordinal]
        return f"{n}:{ordinal}"
    key = obligation["id"]
    if key not in cache:
        p = next(p for p in manifest["presentations"] if p["id"] == obligation["presentation"])
        cache[key] = list(combinations(range(p["normal_count"]),obligation["q"]))
    return obligation["presentation"]+f":c{obligation['coefficient']}:"+",".join(map(str,cache[key][ordinal]))


def run_slice(work, obligation, start, limit, result):
    total = integer(obligation["total"])
    require(type(start) is int and 0 <= start <= total and type(limit) is int and limit > 0, "Invalid explicit slice")
    stop = min(total,start+limit)
    result.update(obligation=obligation["id"],start=start,next_start=start,total=total,
                  checked_ids=[],records=[],status="PARTIAL",termination="slice_limit")
    try:
        for ordinal in range(start,stop):
            work.deadline.check()
            kind = obligation["kind"]
            if kind == "boundary":
                row = work.boundary(ordinal)
            elif kind == "types":
                row = work.type_job(ordinal)
            elif kind == "scope":
                row = work.scope(obligation["rank"],ordinal)
            else:
                row = work.cone(obligation,ordinal)
            result["records"].append({"ordinal":ordinal,**row})
            result["checked_ids"].append(row["id"])
            result["next_start"] = ordinal+1
            if row.get("strictly_positive") is False or row.get("declared_margin_satisfied") is False:
                result.update(status="FAILED",termination="nonpositive_or_failed_margin",
                              error="Finite corrected local criterion failed; exact local value is preserved. No whole LR coefficient was derived.")
                return
    except N.DeadlineReached:
        result["termination"] = "deadline"
        return
    if result["next_start"] == total and start == 0:
        result["status"] = "OBLIGATION_VERIFIED"
        result["termination"] = "obligation_complete"
    elif result["next_start"] == total:
        result["termination"] = "end_of_obligation"


def complete_intervals(intervals, total):
    end = 0
    gaps = []
    for start,stop in sorted(intervals):
        require(type(start) is int and type(stop) is int and 0 <= start < stop <= total, "Invalid empty/out-of-range coverage segment")
        require(start >= end, "Duplicate/overlapping checked ordinal interval")
        if start != end:
            gaps.append([end,start])
        end = stop
    if end < total:
        gaps.append([end,total])
    return gaps


def aggregate_reports(manifest, manifest_sha, sources, report_paths, deadline, adopted_p07=None):
    """Stream bounded reports; require exact identities, coverage and type joins."""
    obligations = unique_map(manifest["obligations"],lambda r:r["id"])
    coverage = {key:[] for key in obligations}
    statistics = {key:{"independent":0,"raw_negative":0,"raw_zero":0,"primitive_incidences":0,
                       "minimum":None,"raw_minimum":None,"normal_sha256":None} for key,o in obligations.items() if o["kind"] == "cones"}
    boundaries, types, used_types, scope_roles, chunks, cache, seen_reports = {}, {}, {}, Counter(), [], {}, set()
    report_inputs, report_bindings = {}, {}
    for source_key in manifest["sources"]:
        deadline.check()
        sources.bytes(source_key)
    for path in report_paths:
        deadline.check()
        raw = bounded_bytes(path)
        sha = N.digest(raw)
        require(sha not in seen_reports, "Duplicate report bytes/retry")
        seen_reports.add(sha)
        report_bindings[str(Path(path).resolve())] = sha
        report = N.decode(raw)
        require(report["schema"] == SCHEMA and report["kind"] == "slice" and report["stage"] == manifest["stage"]
                and report["manifest_sha256"] == manifest_sha and report["checker_versions"] == manifest["checker_versions"],
                "Stale/mixed checker or source-manifest report")
        require(report["status"] in ("PARTIAL","OBLIGATION_VERIFIED") and report.get("inputs_unchanged") is True,
                "Failed, unbound or interrupted-without-rebinding report cannot be adopted")
        key = report["obligation"]
        require(key in obligations, "Unexpected report obligation")
        obligation = obligations[key]
        start,stop = integer(report["start"]),integer(report["next_start"])
        require(integer(report["total"]) == obligation["total"] and 0 <= start <= stop <= obligation["total"], "Stale slice endpoints/total")
        require(len(report["records"]) == len(report["checked_ids"]) == stop-start, "Report drops checked identities")
        require(stop > start, "Empty partial result is not evidence")
        for input_key, info in report["read_inputs"].items():
            require(input_key in manifest["sources"] and info == manifest["sources"][input_key], "Report source hash differs from complete freeze")
            report_inputs[input_key] = info
        coverage[key].append((start,stop))
        for i,row in enumerate(report["records"],start):
            deadline.check()
            expected = expected_identity(manifest,obligation,i,cache)
            require(integer(row["ordinal"]) == i and row["id"] == report["checked_ids"][i-start] == expected,
                    "Checked identity is missing, repeated, reordered or from a stale roster")
            if obligation["kind"] == "boundary":
                require(expected not in boundaries, "Repeated checked chart identity")
                p = manifest["presentations"][i]
                require(row["source"] == p["boundary"] and integer(row["normal_count"]) == p["normal_count"]
                        and integer(row["coordinate_bound"]) == p["dimension"], "Boundary result is detached from exact source geometry")
                h = row["short_normal_hypotheses"]
                require(h["all_retained_directions_primitive"] is True and 1 <= integer(h["maximum_squared_norm"]) <= 6
                        and 0 <= integer(h["maximum_positive_mass"]) <= 2 and 0 <= integer(h["maximum_negative_mass"]) <= 2
                        and matrix(h["fixed_metric"],p["dimension"],p["dimension"]) == N.eye(p["dimension"]),
                        "Missing/changed primitive-normal or single-metric hypothesis for the whole-polynomial bridge")
                boundaries[expected] = row
            elif obligation["kind"] == "types":
                require(expected not in types and row["source"] == manifest["types"][i]["ref"], "Repeated/stale type source identity")
                q = integer(row["q"])
                require(q in ((1,2,3,4) if manifest["stage"] == "p08" else (3,4))
                        and integer(row["fundamental_points"]) > 0, "Incomplete type dimension/point receipt")
                if manifest["stage"] == "p06":
                    require(q == 3 and integer(row["edge_subtractions"]) == 3, "Incomplete compact three-cone receipt")
                else:
                    require(integer(row["proper_faces"]) == (1 << q)-1, "Incomplete all-proper-face type receipt")
                types[expected] = row
            elif obligation["kind"] == "scope":
                scope_roles[obligation["rank"],row["role"]] += 1
            else:
                st = statistics[key]
                p = next(p for p in manifest["presentations"] if p["id"] == obligation["presentation"])
                require(row["source"] == p["cycle"], "Cone result detached from exact source record")
                normal_sha = row["normal_sha256"]
                require(st["normal_sha256"] in (None,normal_sha), "Mixed retained normal embeddings across slices")
                st["normal_sha256"] = normal_sha
                require(type(row["independent"]) is bool and (integer(row["normal_index"]) > 0) is row["independent"], "Invalid cone independence result")
                if row["independent"]:
                    a,b = rational(row["raw"]),rational(row["corrected"])
                    require(row["strictly_positive"] is True and b > 0, "Nonpositive corrected local value was discarded")
                    require(row["raw_negative"] is (a < 0) and row["raw_zero"] is (a == 0), "Raw negative/zero history was changed")
                    if manifest["stage"] == "p08" and obligation["coefficient"] == 1:
                        require(row["declared_margin_satisfied"] is True and b > Q(1,60000), "P08 declared corrected margin failed")
                    st["independent"] += 1
                    st["raw_negative"] += a < 0
                    st["raw_zero"] += a == 0
                    incidence = integer(row["primitive_incidences"])
                    require(incidence >= 0, "Negative primitive incidence count")
                    st["primitive_incidences"] += incidence
                    st["minimum"] = b if st["minimum"] is None else min(st["minimum"],b)
                    st["raw_minimum"] = a if st["raw_minimum"] is None else min(st["raw_minimum"],a)
                    tid = row["type_id"]
                    require(tid not in used_types or used_types[tid] == a, "Same type received inconsistent raw constants")
                    used_types[tid] = a
        chunks.append({"obligation":key,"start":start,"stop":stop,"checked_ids_sha256":jd(report["checked_ids"]),
                       "report":str(Path(path).resolve()),"report_sha256":sha})
    missing = {key:gap for key,o in obligations.items() if (gap := complete_intervals(coverage[key],o["total"]))}
    for path,sha in report_bindings.items():
        require(N.digest(bounded_bytes(path)) == sha, "Slice report changed during aggregation")
    answer = {"kind":"aggregate","status":"PARTIAL","missing_intervals":missing,
              "checked_id_chunks":sorted(chunks,key=lambda x:(x["obligation"],x["start"])),
              "presentations_checked":len(boundaries),"types_checked":len(types),
              "read_report_inputs":dict(sorted(report_inputs.items())),"premises":PREMISES}
    if missing:
        return answer
    for key,st in statistics.items():
        target = obligations[key]["targets"]
        for field in ("independent","raw_negative","raw_zero"):
            require(st[field] == integer(target[field]), f"Complete derived/source count mismatch: {key}/{field}")
        for field in ("minimum","raw_minimum"):
            require(st[field] == rational(target[field]), f"Complete derived/source minimum mismatch: {key}/{field}")
            st[field] = str(st[field])
        require(st["normal_sha256"] == boundaries[obligations[key]["presentation"]]["normal_sha256"],
                "Cone type/correction results do not join to the independently checked full chart")
    for tid,alpha in used_types.items():
        require(tid in types and rational(types[tid]["alpha"]) == alpha, "Missing complete Laurent replay for a used scalar/type")
    stage = manifest["stage"]
    desired_roles = ({(6,"new_five"):24} if stage == "p07" else
                     {(6,"new_five"):1275,(6,"prior_lower_coordinate"):30338,(6,"outside_sufficient_criterion"):1155} if stage == "p08" else
                     {(6,"new_four"):24,(7,"new_four"):222,(6,"prior_metric_branch"):1887,(7,"prior_metric_branch"):20384,
                      (6,"outside_exact_four"):(1 << 15)-1911,(7,"outside_exact_four"):(1 << 18)-20606})
    require(dict(scope_roles) == desired_roles, "Complete mask census/old-new partition mismatch")
    derived_cones = sum(st["independent"] for st in statistics.values())
    derived_incidences = sum(st["primitive_incidences"] for st in statistics.values())
    points = sum(integer(row["fundamental_points"]) for row in types.values())
    faces = sum(integer(row.get("proper_faces",0)) for row in types.values())
    implications = sum(integer(row["full_affine_implications"]) for row in boundaries.values())
    rhombi = sum(integer(row["original_rhombi"]) for row in boundaries.values())
    require(derived_cones == {"p06":10125,"p07":13265,"p08":707032}[stage], "Derived full cone population differs from fixed source claim")
    require(derived_incidences == {"p06":0,"p07":7334,"p08":398551}[stage], "Derived complete primitive incidence population differs from fixed source claim")
    require(points == {"p06":2774,"p07":39669,"p08":72090}[stage]
            and faces == {"p06":0,"p07":36157,"p08":68188}[stage], "Complete type point/proper-face census differs from fixed source claim")
    require(implications == {"p06":1180,"p07":41,"p08":2679}[stage]
            and rhombi == {"p06":1755,"p07":90,"p08":5625}[stage], "Full chart/rhombus/affine-implication census differs from fixed source claim")
    adoption = None
    if stage == "p08":
        if adopted_p07 is None:
            answer.update(status="CANNOT_CHECK",cannot_check="Full P08 theorem also needs the independent P07 aggregate for presentations 43 and 45")
            return answer
        data = bounded_bytes(adopted_p07)
        prior = N.decode(data)
        require(prior["schema"] == SCHEMA and prior["kind"] == "aggregate" and prior["stage"] == "p07"
                and prior["status"] == "FINITE_CERTIFICATES_VERIFIED" and prior.get("inputs_unchanged") is True
                and prior["checker_versions"] == manifest["checker_versions"], "P07 aggregate is incomplete or from a different checker")
        require(prior.get("missing_intervals") == {} and prior["presentations_checked"] == 2 and prior["types_checked"] == 2571
                and prior["independent_cones"] == 13265 and prior["primitive_incidences"] == 7334, "P07 exact completion identities/counts missing")
        for key,info in prior["read_inputs"].items():
            require(key in manifest["sources"] and info == manifest["sources"][key], "P07 adoption binds a different captured source or analytic premise text")
        for name in initial_sources("p07"):
            require("packet:"+SOURCE[name] in prior["read_inputs"], "P07 adoption omitted a required captured source")
        require(prior["read_inputs"]["f025:6"] == manifest["sources"]["f025:6"], "P07 adoption uses another forcing premise")
        for mask in P07_MASKS:
            require(prior["boundary_results"][f"6:{mask}"]["normal_sha256"] == boundaries[f"6:{mask}"]["normal_sha256"], "P07/P08 accepted presentation embedding changed")
        adoption = {"path":str(Path(adopted_p07).resolve()),"sha256":N.digest(data),"manifest_sha256":prior["manifest_sha256"]}
        require(N.digest(bounded_bytes(adopted_p07)) == adoption["sha256"], "P07 adoption report changed during aggregation")
    answer.update(status="FINITE_CERTIFICATES_VERIFIED",independent_cones=derived_cones,
                  primitive_incidences=derived_incidences,coefficient_results=statistics,boundary_results=boundaries,
                  all_type_fundamental_points=points,proper_face_quotients=faces,
                  compact_edge_subtractions=3*len(types) if stage == "p06" else 0,
                  full_affine_implications=implications,original_rhombus_occurrences=rhombi,
                  type_result_digest=jd(types),used_type_count=len(used_types),
                  scope_counts=[{"rank":n,"role":role,"count":count} for (n,role),count in sorted(scope_roles.items())],
                  adopted_p07=adoption,claim_ceiling="Complete declared finite predicate conditional on the explicitly listed analytic and prior-adoption premises; no fresh LR recount or theorem promotion")
    answer["whole_polynomial_bridge"] = whole_polynomial_bridge(4 if stage == "p06" else 5)
    return answer


def emit(output, value, root=None, protected=()):
    p = Path(output).resolve()
    require(root is None or not p.is_relative_to(Path(root).resolve()), "Output must be outside immutable returned sources")
    require(p not in {Path(x).resolve() for x in protected if x}, "Output would overwrite an input")
    require(p.parent.is_dir(), "Output parent must already exist")
    with p.open("x",encoding="utf-8") as stream:
        json.dump(value,stream,indent=2,sort_keys=True)
        stream.write("\n")


def cli_parser():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command",required=True)
    for name in ("freeze","boundary","cones","types","scope","aggregate"):
        p = sub.add_parser(name)
        p.add_argument("--root",required=True,type=Path,help="Immutable Pro027 P12 captured packet")
        p.add_argument("--output",required=True,type=Path,help="Fresh file outside the returned packet")
        p.add_argument("--seconds",type=float,default=95.0,help="Explicit internal wall limit, at most 100 seconds")
        p.add_argument("--f025-r6",type=Path,help="Explicit accepted R6 table; non-freeze override must preserve frozen bytes")
        p.add_argument("--f025-r7",type=Path,help="Explicit accepted R7 table, required for P06")
        if name == "freeze":
            p.add_argument("--stage",choices=("p06","p07","p08"),required=True)
        else:
            p.add_argument("--manifest",type=Path,required=True)
        if name in ("boundary","cones","types","scope"):
            p.add_argument("--start",type=int,required=True)
            p.add_argument("--limit",type=int,required=True)
        if name == "cones":
            p.add_argument("--presentation",required=True,help="Literal rank:mask, for example 6:43")
            p.add_argument("--coefficient",type=int,choices=(1,2),required=True)
        if name == "scope":
            p.add_argument("--rank",type=int,choices=(6,7),required=True)
        if name == "aggregate":
            p.add_argument("--reports",type=Path,nargs="+",required=True)
            p.add_argument("--adopt-p07",type=Path,help="Complete independent P07 aggregate required by full P08 adoption")
    return parser


def main(argv=None):
    args = cli_parser().parse_args(argv)
    started = time.monotonic()
    result = {"schema":SCHEMA,"kind":args.command,"status":"FAILED","checker_versions":checker_versions(),
              "argv":list(sys.argv[1:] if argv is None else argv),"read_inputs":{},"inputs_unchanged":False}
    sources = None
    manifest = None
    initial_versions = result["checker_versions"]
    manifest_sha = None
    exit_code = 1
    try:
        require(0 < args.seconds <= 100, "Internal wall-clock cap must be in (0,100] seconds")
        require(not args.output.exists(), "Output must be fresh; retries need a new file")
        deadline = N.Deadline(args.seconds)
        if args.command == "freeze":
            result.update(freeze(args,deadline))
            result["read_inputs"] = result["sources"]
            result["inputs_unchanged"] = True
        else:
            raw = bounded_bytes(args.manifest)
            manifest_sha = N.digest(raw)
            manifest = N.decode(raw)
            obligations = validate_manifest(manifest)
            external = dict(manifest["external"])
            for n in (6,7):
                if (p := getattr(args,f"f025_r{n}")) is not None:
                    external[f"f025:{n}"] = str(p.resolve())
            sources = Sources(args.root,external,manifest["sources"])
            result.update(stage=manifest["stage"],manifest_sha256=N.digest(raw))
            work = Work(manifest,sources,deadline)
            if args.command == "aggregate":
                result.update(aggregate_reports(manifest,N.digest(raw),sources,args.reports,deadline,args.adopt_p07))
            else:
                key = (f"cones/{args.presentation}/c{args.coefficient}" if args.command == "cones" else
                       f"scope/{args.rank}" if args.command == "scope" else args.command)
                require(key in obligations, "Requested gate is not in this exact stage's frozen obligation roster")
                result["kind"] = "slice"
                run_slice(work,obligations[key],args.start,args.limit,result)
            sources.unchanged()
            result["read_inputs"] = dict(sorted(sources.reads.items()))
            result["inputs_unchanged"] = True
        exit_code = 0 if result["status"] not in ("FAILED","CANNOT_CHECK") else 1
    except N.DeadlineReached as error:
        result.update(status="PARTIAL",termination="deadline",error=str(error))
        exit_code = 0
    except CannotCheck as error:
        result.update(status="CANNOT_CHECK",error=str(error))
    except (N.CheckError,KeyError,TypeError,ValueError,IndexError,OSError,ZeroDivisionError) as error:
        result.update(status="FAILED",error=f"{type(error).__name__}: {error}")
    finally:
        if sources is not None and not result["inputs_unchanged"]:
            try:
                sources.unchanged()
                result["inputs_unchanged"] = True
            except (N.CheckError,OSError) as error:
                result.update(status="FAILED",error=f"Source rebinding failed: {error}")
                exit_code = 1
            result["read_inputs"] = dict(sorted(sources.reads.items()))
        try:
            require(initial_versions == checker_versions(), "Checker source changed during execution")
            if manifest is not None:
                require(isinstance(manifest,dict) and manifest.get("checker_versions") == initial_versions,
                        "Manifest has no exact checker-version binding")
            if manifest_sha is not None:
                require(N.digest(bounded_bytes(args.manifest)) == manifest_sha, "Source manifest changed during execution")
        except (N.CheckError,OSError) as error:
            result.update(status="FAILED",error=str(error))
            exit_code = 1
        result["seconds"] = round(time.monotonic()-started,6)
    try:
        emit(args.output,result,args.root,(getattr(args,"manifest",None),args.f025_r6,args.f025_r7))
    except (N.CheckError,OSError) as error:
        print(json.dumps({"status":"FAILED","error":f"Report output was not written: {error}"}))
        return 1
    print(json.dumps({"status":result["status"],"output":str(args.output.resolve()),
                      "checked":len(result.get("checked_ids",[])),"next_start":result.get("next_start"),
                      "error":result.get("error"),"seconds":result["seconds"]}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
