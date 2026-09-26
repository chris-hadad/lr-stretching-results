#!/usr/bin/env python3
"""Exact constructive rank-six hive closure for explicit physical row IDs.

The certificate is JSON data, never Python code. A receipt from the independent
closure-certificate verifier is required before any geometric construction.
This implements the source-qualified U04 recipe; it does not count LR objects.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path
from typing import Sequence


CERTIFICATE_SCHEMA = "fr043-u04-portable-positive-closure-certificate/v1"
CERTIFICATE_SHA256 = "b7bf252262130fab5b98047df8ef37b2a59da42b19708650b9048f403acd460c"
RECEIPT_STATUS = "PASS_COMPLETE_POSITIVE_CLOSURE_CERTIFICATE"
N = 6
M = 10
R = 45
BDET = 1 << M
POINTS = tuple((i, j) for i in range(N + 1) for j in range(N + 1 - i))


def _need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _dot(a: Sequence[int | Fraction], b: Sequence[int | Fraction]) -> int | Fraction:
    return sum((x * y for x, y in zip(a, b)), 0)


def _pair(value: int | Fraction) -> list[int]:
    value = Fraction(value)
    return [value.numerator, value.denominator]


def _pairs(values: Sequence[int | Fraction]) -> list[list[int]]:
    return [_pair(value) for value in values]


def _mask(indices: Sequence[int]) -> int:
    result = 0
    for index in indices:
        result |= 1 << index
    return result


def _ids(mask: int) -> list[int]:
    return [index for index in range(R) if mask & (1 << index)]


def _rref(rows: Sequence[Sequence[int | Fraction]], columns: int = M) -> tuple[list[list[Fraction]], list[int]]:
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    _need(all(len(row) == columns for row in matrix), "inconsistent matrix width")
    pivots: list[int] = []
    row_index = 0
    for column in range(columns):
        pivot = next((i for i in range(row_index, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row_index], matrix[pivot] = matrix[pivot], matrix[row_index]
        scale = matrix[row_index][column]
        matrix[row_index] = [value / scale for value in matrix[row_index]]
        for i in range(len(matrix)):
            if i != row_index and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [x - scale * y for x, y in zip(matrix[i], matrix[row_index])]
        pivots.append(column)
        row_index += 1
        if row_index == len(matrix):
            break
    return matrix, pivots


def normal_rank(rows: Sequence[Sequence[int | Fraction]]) -> int:
    """Rank of interior normal rows in the original ten-coordinate lattice."""
    return len(_rref(rows)[1])


def _inverse(square: Sequence[Sequence[int | Fraction]]) -> list[list[Fraction]]:
    size = len(square)
    augmented = [
        [Fraction(value) for value in row]
        + [Fraction(int(i == j)) for j in range(size)]
        for i, row in enumerate(square)
    ]
    _need(all(len(row) == 2 * size for row in augmented), "non-square pivot matrix")
    for column in range(size):
        pivot = next((i for i in range(column, size) if augmented[i][column]), None)
        _need(pivot is not None, "singular pivot matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for i in range(size):
            if i != column and augmented[i][column]:
                scale = augmented[i][column]
                augmented[i] = [x - scale * y for x, y in zip(augmented[i], augmented[column])]
    return [row[size:] for row in augmented]


def _right_inverse(rows: Sequence[Sequence[int]]) -> tuple[list[list[Fraction]], list[int]]:
    q = len(rows)
    _, pivots = _rref(rows)
    _need(len(pivots) == q, "selected normal rows are dependent")
    inverse = _inverse([[row[pivot] for pivot in pivots] for row in rows])
    result = [[Fraction(0) for _ in range(q)] for _ in range(M)]
    for i, pivot in enumerate(pivots):
        result[pivot] = inverse[i]
    for i, row in enumerate(rows):
        for j in range(q):
            _need(sum(row[k] * result[k][j] for k in range(M)) == int(i == j), "right inverse check failed")
    return result, pivots


def _primitive_kernel_direction(rows: Sequence[Sequence[int]]) -> list[int]:
    reduced, pivots = _rref(rows)
    free = [i for i in range(M) if i not in pivots]
    _need(len(free) == 1, "edge requires a one-dimensional kernel")
    rational = [Fraction(0) for _ in range(M)]
    rational[free[0]] = Fraction(1)
    for row_index, pivot in enumerate(pivots):
        rational[pivot] = -reduced[row_index][free[0]]
    denominator = lcm(*(value.denominator for value in rational))
    integral = [int(denominator * value) for value in rational]
    divisor = gcd(*integral)
    _need(divisor > 0, "zero kernel direction")
    integral = [value // divisor for value in integral]
    if next(value for value in integral if value) < 0:
        integral = [-value for value in integral]
    _need(all(_dot(row, integral) == 0 for row in rows), "kernel direction check failed")
    _need(gcd(*integral) == 1, "nonprimitive edge direction")
    return integral


@dataclass(frozen=True)
class VerifiedCertificate:
    certificate_sha256: str
    points: tuple[tuple[int, int], ...]
    rows: tuple[tuple[int, ...], ...]
    interior_positions: tuple[int, ...]
    normals: tuple[tuple[int, ...], ...]
    feasible_heights: tuple[tuple[int, ...], ...]
    zero_masks: tuple[int, ...]
    rules: tuple[tuple[int, int], ...]


def load_verified_certificate(
    certificate_path: str | Path, atlas_path: str | Path, receipt_path: str | Path
) -> VerifiedCertificate:
    """Load authenticated data only after an independent verifier receipt.

    The receipt must come from the root-authored ``verify_closure.py``. The
    caller must run that verifier first; this loader checks its result and the
    exact bytes and row ordering used by this constructive implementation.
    """
    certificate_bytes = Path(certificate_path).read_bytes()
    digest = sha256(certificate_bytes).hexdigest()
    _need(digest == CERTIFICATE_SHA256, "unexpected closure certificate SHA-256")
    receipt = json.loads(Path(receipt_path).read_text())
    _need(receipt.get("status") == RECEIPT_STATUS, "closure certificate has no passing independent verification receipt")
    _need(receipt.get("schema") == "pub-independent-pro043-closure-v1", "unexpected verifier receipt schema")
    _need(receipt.get("certificate_sha256") == digest, "verification receipt is for a different certificate")
    _need(receipt.get("identities") == 103 and receipt.get("feasible_vectors") == 166, "incomplete verifier receipt")
    _need(receipt.get("short_identity_populations_independently_exhausted") == [30, 72]
          and receipt.get("slack_checks") == 166 * R and receipt.get("Horn_clauses") == 564,
          "incomplete identity or feasibility receipt")
    _need(receipt.get("RUP_refutations") == 9 and receipt.get("RUP_additions") == 6488
          and receipt.get("full_CNF_transports") == 45 and receipt.get("initial_sets_covered") == "2^45",
          "incomplete closure proof receipt")
    _need(receipt.get("provider_code_executed") is False, "verification did not preserve provider-code separation")
    _need(receipt.get("certificate_row_to_original_row") == list(range(R)), "certificate rows do not use atlas physical order")

    data = json.loads(certificate_bytes)
    atlas = json.loads(Path(atlas_path).read_text())
    _need(data.get("schema") == CERTIFICATE_SCHEMA and data.get("rank") == N, "wrong certificate schema or rank")
    points = tuple(tuple(point) for point in data["points"])
    rows = tuple(tuple(row) for row in data["rows"])
    _need(points == POINTS and len(rows) == R, "unexpected point or physical row population")
    _need(rows == tuple(tuple(row) for row in atlas["rhombi"]), "certificate and atlas physical row orders differ")
    _need(all(len(row) == len(points) and all(type(value) is int for value in row) for row in rows), "nonintegral physical row")
    interior_positions = tuple(i for i, (x, y) in enumerate(points) if x > 0 and y > 0 and x + y < N)
    _need(len(interior_positions) == M, "unexpected interior coordinate count")
    _need(tuple(points[i] for i in interior_positions) == tuple(tuple(p) for p in atlas["interior"]), "atlas interior order differs")
    normals = tuple(tuple(row[i] for i in interior_positions) for row in rows)
    _need(all(sum(value * value for value in row) <= 4 for row in normals), "determinant bound assumption fails")

    heights = tuple(tuple(height) for height in data["feasible_heights"])
    _need(len(heights) == 166, "unexpected feasible vector population")
    zero_masks = []
    for height in heights:
        _need(len(height) == len(points) and all(type(value) is int for value in height), "nonintegral feasible height")
        slacks = [_dot(row, height) for row in rows]
        _need(min(slacks) >= 0, "infeasible certificate height")
        zero_masks.append(_mask([i for i, slack in enumerate(slacks) if slack == 0]))

    identities = data["identities"]
    _need(len(identities) == 103, "unexpected identity population")
    rules = []
    for identity in identities:
        sides = []
        for name in ("left", "right"):
            side = identity[name]
            _need(isinstance(side, dict) and side, "empty identity side")
            terms = []
            for key, coefficient in side.items():
                index = int(key)
                _need(str(index) == key and 0 <= index < R and type(coefficient) is int and coefficient > 0, "invalid positive identity term")
                terms.append((index, coefficient))
            sides.append(terms)
        left, right = sides
        _need(all(sum(coefficient * rows[i][j] for i, coefficient in left)
                  == sum(coefficient * rows[i][j] for i, coefficient in right)
                  for j in range(len(points))), "identity fails in full heights")
        a, b = _mask([i for i, _ in left]), _mask([i for i, _ in right])
        rules.extend(((a, b), (b, a)))
    return VerifiedCertificate(digest, points, rows, interior_positions, normals,
                               heights, tuple(zero_masks), tuple(rules))


def forward_closure(data: VerifiedCertificate, physical_rows: Sequence[int]) -> list[int]:
    """Return exact physical-row closure under the 103 positive identities."""
    selected = _physical_ids(physical_rows)
    mask = _mask(selected)
    while True:
        before = mask
        for premise, conclusion in data.rules:
            if mask & premise == premise:
                mask |= conclusion
        if mask == before:
            return _ids(mask)


def _physical_ids(physical_rows: Sequence[int]) -> list[int]:
    selected = list(physical_rows)
    _need(all(type(row) is int and 0 <= row < R for row in selected), "physical row IDs must be integers 0..44")
    _need(len(selected) == len(set(selected)), "duplicate physical row ID")
    return sorted(selected)


def _boundary(data: VerifiedCertificate, height: Sequence[int]) -> dict:
    index = {point: i for i, point in enumerate(data.points)}

    def words(values: Sequence[int]) -> tuple[list[int], list[int], list[int]]:
        mu = [values[index[i, 0]] - values[index[i - 1, 0]] for i in range(1, N + 1)]
        lam = [values[index[0, j]] - values[index[0, j - 1]] for j in range(1, N + 1)]
        nu = [values[index[N - j, j]] - values[index[N + 1 - j, j - 1]] for j in range(1, N + 1)]
        return lam, mu, nu

    lam0, mu0, nu0 = words(height)
    u = max(0, -mu0[-1])
    v = max(0, -lam0[-1], u - nu0[-1])
    legalized = [height[k] + u * i + v * j - height[index[0, 0]]
                 for k, (i, j) in enumerate(data.points)]
    lam, mu, nu = words(legalized)
    for name, word in (("lambda", lam), ("mu", mu), ("nu", nu)):
        _need(all(type(part) is int and part >= 0 for part in word), name + " is not a nonnegative integral word")
        _need(all(word[k] >= word[k + 1] for k in range(N - 1)), name + " is not a partition")
    _need(sum(lam) == sum(mu) + sum(nu), "original boundary trace fails")
    _need(all(_dot(row, height) == _dot(row, legalized) for row in data.rows), "affine legalization changed a rhombus")
    return {
        "lambda_outer": lam, "mu": mu, "nu": nu,
        "trace": {"lambda_size": sum(lam), "mu_size": sum(mu), "nu_size": sum(nu)},
        "affine_shift_u_i_plus_v_j": [u, v],
        "legal_height": legalized,
    }


def _edge(data: VerifiedCertificate, height: Sequence[int], closure: Sequence[int]) -> dict:
    direction = _primitive_kernel_direction([data.normals[row] for row in closure])
    lower: Fraction | None = None
    upper: Fraction | None = None
    for row, normal in zip(data.rows, data.normals):
        slack = _dot(row, height)
        slope = _dot(normal, direction)
        if slope > 0:
            bound = Fraction(-slack, slope)
            lower = bound if lower is None else max(lower, bound)
        elif slope < 0:
            bound = Fraction(-slack, slope)
            upper = bound if upper is None else min(upper, bound)
        else:
            _need(slack >= 0, "negative slack on edge")
    _need(lower is not None and upper is not None and lower < 0 < upper,
          "witness is not in the relative interior of a bounded edge")
    xstar = [height[i] for i in data.interior_positions]
    endpoint_x = [[Fraction(x) + t * d for x, d in zip(xstar, direction)]
                  for t in (lower, upper)]
    endpoints = []
    for coordinates in endpoint_x:
        full = [Fraction(value) for value in height]
        for position, value in zip(data.interior_positions, coordinates):
            full[position] = value
        _need(all(_dot(row, full) >= 0 for row in data.rows), "edge endpoint is infeasible")
        endpoints.append({"interior": _pairs(coordinates), "full_height": _pairs(full)})
    return {
        "primitive_direction": direction,
        "parameter_interval": [_pair(lower), _pair(upper)],
        "endpoints": endpoints,
        "saturated_length": _pair(upper - lower),
    }


def _perturbation(data: VerifiedCertificate, selected: Sequence[int], height: Sequence[int],
                  expand_fractions: bool) -> dict:
    selected_normals = [data.normals[row] for row in selected]
    y, pivots = _right_inverse(selected_normals)
    y0 = [-sum(row, Fraction(0)) for row in y]
    selected_set = set(selected)
    a0 = [Fraction(1) if r in selected_set else
          max(Fraction(1), Fraction(1) - _dot(data.normals[r], y0))
          for r in range(R)]
    denominator = lcm(*(value.denominator for value in y0 + a0))
    y0_scaled = [int(denominator * value) for value in y0]
    a = [int(denominator * value) for value in a0]
    for r in range(R):
        margin = _dot(data.normals[r], y0_scaled) + a[r]
        _need(margin == 0 if r in selected_set else margin >= denominator,
              "scaled selected or off-selected margin fails")
    cmax = max(sum(abs(sum(data.normals[r][k] * y[k][s] for k in range(M)))
                   for s in range(len(selected))) for r in range(R))
    generic_bound = 2 * (Fraction(cmax) + 1)
    large = max(4 * BDET + 5, generic_bound.numerator // generic_bound.denominator + 1)
    _need(large > 4 * BDET + 4 and large > 2 * (cmax + 1), "generic base bound fails")
    tau = Fraction(1, large)
    powers = [tau ** (r + 1) for r in range(R)]
    delta = [a[r] + powers[r] for r in range(R)]
    ydelta = [Fraction(y0_scaled[k]) - sum(y[k][s] * powers[row]
                    for s, row in enumerate(selected)) for k in range(M)]
    hbound = max(a) + 1
    epsilon = Fraction(1, 16 * M * BDET * BDET * hbound)
    _need(all(0 < value < hbound for value in delta), "positive relaxation bound fails")
    _need(epsilon < Fraction(1, 8 * M * BDET * BDET * hbound), "epsilon bound fails")

    perturbed_slacks = []
    for r in range(R):
        slack = Fraction(_dot(data.rows[r], height))
        perturbed = slack + epsilon * (_dot(data.normals[r], ydelta) + delta[r])
        _need(perturbed == 0 if r in selected_set else perturbed > 0,
              "selected/off-selected perturbed slack fails at row " + str(r))
        perturbed_slacks.append(perturbed)
    result = {
        "right_inverse_Y_rows": [_pairs(row) for row in y],
        "right_inverse_pivot_columns": pivots,
        "common_denominator_D": denominator,
        "integral_y0": y0_scaled,
        "integral_a_by_physical_row": a,
        "Bdet": BDET,
        "Cmax": _pair(cmax),
        "M_generic": large,
        "tau": _pair(tau),
        "H": hbound,
        "epsilon": _pair(epsilon),
        "recipe": "delta_r=a_r+tau^(r+1); ydelta=y0-Y*(tau^(s+1))_(s in selected physical row order); x(epsilon)=xstar+epsilon*ydelta",
        "exact_checks": {"all_delta_positive": True, "selected_slacks_zero": True,
                         "all_off_selected_slacks_positive": True},
    }
    if expand_fractions:
        xstar = [height[i] for i in data.interior_positions]
        result["expanded"] = {
            "delta_by_physical_row": _pairs(delta),
            "ydelta": _pairs(ydelta),
            "perturbed_interior": _pairs([Fraction(x) + epsilon * d for x, d in zip(xstar, ydelta)]),
            "perturbed_slacks_by_physical_row": _pairs(perturbed_slacks),
        }
    return result


def analyze_branch(data: VerifiedCertificate, physical_rows: Sequence[int],
                   *, expand_fractions: bool = False) -> dict:
    """Classify and, when retained, construct an exact legal hive witness.

    Inputs are physical row IDs 0..44, never the atlas's 42 normal labels.
    For excluded or dependent branches only closure and ranks are returned.
    """
    selected = _physical_ids(physical_rows)
    closed = forward_closure(data, selected)
    rank_selected = normal_rank([data.normals[row] for row in selected])
    rank_closed = normal_rank([data.normals[row] for row in closed])
    result = {
        "source_certificate_sha256": data.certificate_sha256,
        "physical_rows": selected,
        "closure_physical_rows": closed,
        "rank_selected": rank_selected,
        "rank_closure": rank_closed,
    }
    if rank_selected != len(selected):
        result["classification"] = "dependent"
        return result
    if rank_closed > rank_selected:
        result["classification"] = "excluded_rank_increase"
        return result
    _need(rank_closed == rank_selected, "closure rank decreased")
    result["classification"] = "retained_independent"

    seed_mask = _mask(selected)
    survivors = [height for height, zeros in zip(data.feasible_heights, data.zero_masks)
                 if zeros & seed_mask == seed_mask]
    raw = [sum(height[i] for height in survivors) for i in range(len(data.points))]
    raw_slacks = [_dot(row, raw) for row in data.rows]
    _need(all(slack >= 0 for slack in raw_slacks), "feasible-vector sum is infeasible")
    _need([r for r, slack in enumerate(raw_slacks) if slack == 0] == closed,
          "feasible-vector tight set differs from certified closure")
    boundary = _boundary(data, raw)
    legal_height = boundary["legal_height"]
    _need([r for r, row in enumerate(data.rows) if _dot(row, legal_height) == 0] == closed,
          "legalized tight set changed")
    xstar = [legal_height[i] for i in data.interior_positions]
    face = {
        "dimension": M - rank_closed,
        "selected_equations": selected,
        "closure_equations": closed,
        "interior_point_xstar": xstar,
        "saturated_lattice": {
            "equation": "xstar + ker_Z(N_closure)",
            "N_closure": [list(data.normals[row]) for row in closed],
            "ambient_interior_lattice": "Z^10",
        },
    }
    if rank_closed == 9:
        face["edge"] = _edge(data, legal_height, closed)
    if rank_closed == 10:
        face["parent_dimension"] = "not inferred from this zero-dimensional face"
    result["witness"] = {
        "summed_feasible_vector_count": len(survivors),
        "raw_height": raw,
        "boundary": boundary,
        "physical_slacks_at_legal_height": [_dot(row, legal_height) for row in data.rows],
        "face": face,
        "positive_generic_relaxation": _perturbation(data, selected, legal_height,
                                                       expand_fractions),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, required=True, help="authenticated CLOSURE-CERTIFICATE.json")
    parser.add_argument("--atlas", type=Path, required=True, help="original whole-rank-six atlas.json")
    parser.add_argument("--verification-receipt", type=Path, required=True,
                        help="RESULT.json from the independent closure verifier")
    parser.add_argument("--physical-rows", required=True,
                        help="comma-separated zero-based physical IDs 0..44; empty string selects no rows")
    parser.add_argument("--expand-fractions", action="store_true")
    parser.add_argument("--out", type=Path, help="write JSON here instead of standard output")
    args = parser.parse_args()
    if args.out:
        _need(not args.out.exists() and not args.out.is_symlink()
              and args.out.parent.is_dir(), "fresh output file and existing parent required")
        _need(args.out.resolve() not in {
            args.certificate.resolve(), args.atlas.resolve(),
            args.verification_receipt.resolve()}, "output must differ from every input")
    selected = [] if args.physical_rows == "" else [int(value) for value in args.physical_rows.split(",")]
    data = load_verified_certificate(args.certificate, args.atlas, args.verification_receipt)
    result = analyze_branch(data, selected, expand_fractions=args.expand_fractions)
    encoded = json.dumps(result, indent=2) + "\n"
    if args.out:
        with args.out.open("x") as stream:
            stream.write(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
