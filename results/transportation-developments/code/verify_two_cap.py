"""Independent exact A64 two-active-cap derivative-certificate verifier.

The producer's JSON is read only as comparison data.  Each chamber map is
substituted into the complete subset formula before differentiation.  Sparse
arithmetic is over Q[u,v,w,z,E]/(E^2); the derivative fixes Y,R,S,E and is
computed with the exact inverse of the chamber's four-by-four matrix.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


Q = Fraction
Exponent = tuple[int, int, int, int, int]
Poly = dict[Exponent, Fraction]
ORIGIN: Exponent = (0, 0, 0, 0, 0)
ONE: Poly = {ORIGIN: Q(1)}
VARIABLES = tuple(
    {tuple(int(i == j) for i in range(5)): Q(1)} for j in range(5)
)
BASE_NAMES = ("u", "v", "w", "z")
CHAMBER_NAMES = ("A1", "A2", "A3", "A4", "B1a", "B1b", "B2", "B3")

# Rows are X,Y,R,S; columns are u,v,w,z.  E is an independent fifth variable.
CHAMBERS = {
    "A1": (((1, 1, 0, 0), (1, 1, 1, 0), (2, 2, 1, 1), (1, 0, 0, 0)),
           ("X", "Y", "XY"), ()),
    "A2": (((1, 0, 0, 0), (1, 1, 1, 0), (2, 1, 1, 1), (1, 1, 0, 0)),
           ("X", "Y", "XY"), ("X",)),
    "A3": (((1, 1, 0, 0), (1, 1, 1, 0), (2, 2, 1, 1), (2, 1, 1, 0)),
           ("X", "Y", "XY"), ("X", "Y")),
    "A4": (((1, 0, 0, 0), (1, 1, 0, 0), (2, 1, 1, 1), (2, 1, 1, 0)),
           ("X", "Y", "XY"), ("X", "Y", "XY")),
    "B1a": (((1, 1, 1, 0), (1, 1, 1, 1), (2, 2, 1, 1), (1, 0, 0, 0)),
            ("X", "Y"), ()),
    "B1b": (((1, 1, 1, 0), (1, 1, 1, 1), (2, 1, 1, 1), (1, 1, 0, 0)),
            ("X", "Y"), ()),
    "B2": (((1, 1, 0, 0), (1, 1, 1, 1), (1, 2, 1, 1), (1, 1, 1, 0)),
           ("X", "Y"), ("X",)),
    "B3": (((1, 1, 1, 0), (1, 1, 1, 1), (1, 2, 2, 1), (1, 2, 1, 1)),
           ("X", "Y"), ("X", "Y")),
}
SUBSETS = {"X": (0,), "Y": (1,), "XY": (0, 1)}
RATIONAL = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")


def constant(value: int | Fraction) -> Poly:
    value = Q(value)
    return {ORIGIN: value} if value else {}


def add(*parts: Poly) -> Poly:
    result: Poly = {}
    for part in parts:
        for exponent, coefficient in part.items():
            result[exponent] = result.get(exponent, Q(0)) + coefficient
    return {e: c for e, c in result.items() if c}


def scale(part: Poly, factor: int | Fraction) -> Poly:
    factor = Q(factor)
    return {e: c * factor for e, c in part.items()} if factor else {}


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, scale(right, -1))


def mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for e, c in left.items():
        for f, d in right.items():
            if e[4] + f[4] > 1:
                continue
            exponent = tuple(e[i] + f[i] for i in range(5))
            result[exponent] = result.get(exponent, Q(0)) + c * d
    return {e: c for e, c in result.items() if c}


def product(*parts: Poly) -> Poly:
    result = ONE
    for part in parts:
        result = mul(result, part)
    return result


def square(part: Poly) -> Poly:
    return mul(part, part)


def affine(row: tuple[int, int, int, int]) -> Poly:
    return add(*(scale(VARIABLES[i], row[i]) for i in range(4)))


def cap_factor(cap: Poly) -> Poly:
    return scale(product(add(cap, constant(1)), add(cap, constant(2))), Q(1, 2))


def falling_binomial_range(top: Poly, lowest: int, highest: int) -> dict[int, Poly]:
    """Build each needed falling binomial once in one exact recurrence."""
    result = ONE
    needed = {}
    for bottom in range(1, highest + 1):
        result = scale(mul(result, sub(top, constant(bottom - 1))), Q(1, bottom))
        if bottom >= lowest:
            needed[bottom] = result
    return needed


def elementary_shifted(caps: tuple[Poly, ...]) -> list[Poly]:
    values: list[Poly] = [ONE] + [{} for _ in caps]
    for cap in caps:
        shifted = add(cap, constant(2))
        for degree in range(len(caps), 0, -1):
            values[degree] = add(values[degree], mul(values[degree - 1], shifted))
    return values


def subset_tail(h: Poly, other_budget: Poly, selected: tuple[Poly, ...], a: int) -> Poly:
    q = len(selected)
    weight = add(*selected)
    top = add(sub(h, weight), constant(2 * a - 2 * q - 1))
    elementary = elementary_shifted(selected)
    multiplier = add(constant(2), other_budget, scale(h, Q(-1, 2)))
    binomials = falling_binomial_range(top, 2 * a - q + 1, 2 * a + 2)
    terms = []
    for j in range(q + 1):
        lower = 2 * a - q + j + 1
        bracket = add(mul(multiplier, binomials[lower]), binomials[lower + 1])
        terms.append(mul(elementary[q - j], bracket))
    return add(*terms)


def whole_after_substitution(a: int, chamber: str) -> Poly:
    """Construct the entire five-variable F in the selected active-mask cone."""
    matrix, active_r, active_s = CHAMBERS[chamber]
    x, y, r, s = (affine(row) for row in matrix)
    excess = VARIABLES[4]
    last_cap = add(r, excess)
    caps = (x, y) + (r,) * (a - 3) + (last_cap,)
    k = add(x, y, scale(r, a - 2), excess)
    n = product(*(cap_factor(cap) for cap in caps))
    linear = sub(sub(scale(k, Q(5, 4)), r), s)
    cap_squares = add(square(x), square(y), scale(square(r), a - 3),
                      square(last_cap))
    quadratic = sub(product(sub(scale(k, Q(2, 3)), r),
                            sub(scale(k, Q(2, 3)), s)),
                    scale(cap_squares, Q(1, 36)))
    full = mul(n, add(ONE, linear, quadratic))
    for h, other_budget, active in ((r, sub(k, s), active_r),
                                    (s, sub(k, r), active_s)):
        full = add(full, subset_tail(h, other_budget, (), a))
        for name in active:
            selected = tuple(caps[i] for i in SUBSETS[name])
            sign = -1 if len(selected) % 2 else 1
            full = add(full, scale(subset_tail(h, other_budget, selected, a), sign))
    return full


def inverse_and_determinant(matrix: tuple[tuple[int, ...], ...]):
    """Exact Gauss-Jordan inverse and determinant of a four-by-four matrix."""
    size = 4
    rows = [[Q(matrix[i][j]) for j in range(size)] +
            [Q(int(i == j)) for j in range(size)] for i in range(size)]
    determinant = Q(1)
    for column in range(size):
        pivot = next((i for i in range(column, size) if rows[i][column]), None)
        if pivot is None:
            raise ValueError("singular chamber matrix")
        if pivot != column:
            rows[pivot], rows[column] = rows[column], rows[pivot]
            determinant = -determinant
        value = rows[column][column]
        determinant *= value
        rows[column] = [entry / value for entry in rows[column]]
        for i in range(size):
            if i == column:
                continue
            multiple = rows[i][column]
            if multiple:
                rows[i] = [rows[i][j] - multiple * rows[column][j]
                           for j in range(2 * size)]
    inverse = tuple(tuple(rows[i][j + size] for j in range(size))
                    for i in range(size))
    for i in range(size):
        for j in range(size):
            entry = sum(Q(matrix[i][k]) * inverse[k][j] for k in range(size))
            if entry != int(i == j):
                raise ArithmeticError("inverse failed the exact identity check")
    return determinant, inverse


def partial(poly: Poly, axis: int) -> Poly:
    result: Poly = {}
    for exponent, coefficient in poly.items():
        if exponent[axis]:
            reduced = list(exponent)
            reduced[axis] -= 1
            result[tuple(reduced)] = coefficient * exponent[axis]
    return result


def fixed_deficit_derivative(poly: Poly, inverse) -> Poly:
    # The first inverse column varies X while Y,R,S stay fixed.  E stays fixed.
    return add(*(scale(partial(poly, axis), inverse[axis][0])
                 for axis in range(4)))


def domain(degree: int):
    """Every exponent with total degree <= degree and E degree <= one."""
    for excess in (0, 1):
        if excess > degree:
            continue
        remaining = degree - excess
        for u in range(remaining + 1):
            for v in range(remaining - u + 1):
                for w in range(remaining - u - v + 1):
                    for z in range(remaining - u - v - w + 1):
                        yield (u, v, w, z, excess)


def rational_string(value: object) -> Fraction:
    if not isinstance(value, str) or not RATIONAL.fullmatch(value):
        raise ValueError(f"coefficient is not an integer/fraction string: {value!r}")
    return Q(value)


def check_zero_declaration(declaration: object, degree: int) -> None:
    if not isinstance(declaration, dict):
        raise ValueError("exact_zero_domain must be a dict")
    required = {
        "total_degree_max": degree,
        "E_degree_max": 1,
        "omitted_coefficients": "exactly_zero",
        "monomial_count": math.comb(degree + 4, 4) + math.comb(degree + 3, 4),
    }
    for key, expected in required.items():
        actual = declaration.get(key)
        if type(actual) is not type(expected) or actual != expected:
            raise ValueError(f"exact_zero_domain {key} must be {expected!r}, got {actual!r}")


def parse_coefficients(row: dict, degree: int) -> dict[Exponent, Fraction]:
    entries = row.get("coefficients")
    if not isinstance(entries, list):
        raise ValueError("chamber coefficients must be a list")
    coefficients: dict[Exponent, Fraction] = {}
    for item in entries:
        if not isinstance(item, dict) or "exponents" not in item or "coefficient" not in item:
            raise ValueError("malformed coefficient item")
        raw = item["exponents"]
        if not isinstance(raw, list) or len(raw) != 5 or any(type(x) is not int or x < 0 for x in raw):
            raise ValueError(f"invalid exponent: {raw!r}")
        exponent = tuple(raw)
        if exponent[4] > 1 or sum(exponent) > degree:
            raise ValueError(f"exponent outside the declared domain: {exponent!r}")
        if exponent in coefficients:
            raise ValueError(f"duplicate exponent: {exponent!r}")
        coefficients[exponent] = rational_string(item["coefficient"])
    return coefficients


def check_chamber(a: int, name: str, row: dict, declaration: object) -> dict:
    start = time.monotonic()
    degree = 2 * a + 1
    check_zero_declaration(row.get("exact_zero_domain", declaration), degree)
    expected = parse_coefficients(row, degree)
    matrix, active_r, active_s = CHAMBERS[name]
    determinant, inverse = inverse_and_determinant(matrix)
    if abs(determinant) != 1 or any(value.denominator != 1
                                    for inverse_row in inverse for value in inverse_row):
        raise ArithmeticError("chamber matrix must have determinant +/-1 and integral inverse")
    whole = whole_after_substitution(a, name)
    actual = fixed_deficit_derivative(whole, inverse)
    outside = [e for e in actual if e[4] > 1 or sum(e) > degree]
    if outside:
        raise ArithmeticError(f"computed coefficients outside full domain: {outside[:8]!r}")

    checked = matched = negative = mismatch = actual_nonzero = 0
    mismatch_examples = []
    negative_examples = []
    digest = hashlib.sha256()
    for exponent in domain(degree):
        found = actual.get(exponent, Q(0))
        claimed = expected.get(exponent, Q(0))
        checked += 1
        actual_nonzero += bool(found)
        digest.update((",".join(map(str, exponent)) + ":" + str(found) + "\n").encode())
        if found == claimed:
            matched += 1
        else:
            mismatch += 1
            if len(mismatch_examples) < 12:
                mismatch_examples.append(dict(exponents=exponent, computed=str(found),
                                              producer=str(claimed)))
        if found < 0:
            negative += 1
            if len(negative_examples) < 12:
                negative_examples.append(dict(exponents=exponent, coefficient=str(found)))

    pure_support = {}
    pure_values = {}
    for axis, variable in enumerate(BASE_NAMES):
        pure_values[variable] = [
            actual.get(tuple(power if i == axis else 0 for i in range(5)), Q(0))
            for power in range(degree + 1)
        ]
        pure_support[variable] = [str(value) for value in pure_values[variable]]
    strict_axes = [BASE_NAMES[axis] for axis, coefficient in enumerate(matrix[0])
                   if coefficient > 0]
    strict_failures = [
        dict(variable=variable, degree=power, coefficient=str(value))
        for variable in strict_axes
        for power, value in enumerate(pure_values[variable])
        if value <= 0
    ]
    strict_checked = len(strict_axes) * (degree + 1)
    return dict(
        chamber=name, status="PASS" if mismatch == 0 and negative == 0
        and not strict_failures else "FAIL",
        matrix=[list(row) for row in matrix], determinant=str(determinant),
        inverse=[[str(value) for value in row] for row in inverse],
        determinant_abs_one=True, inverse_integral=True,
        direction_dX_at_fixed_Y_R_S_E=[str(inverse[i][0]) for i in range(4)],
        active_subsets_R=list(active_r), active_subsets_S=list(active_s),
        total_parameter_degree_at_most=degree, E_degree_at_most=1,
        domain_slots=checked, matched_slots=matched, mismatch_count=mismatch,
        mismatch_examples=mismatch_examples, producer_explicit_slots=len(expected),
        producer_explicit_nonzero=sum(bool(c) for c in expected.values()),
        computed_nonzero=actual_nonzero, computed_zero=checked - actual_nonzero,
        negative_count=negative, negative_examples=negative_examples,
        nonnegative=(negative == 0), pure_support=pure_support,
        selected_strict_axes=strict_axes, strict_support_checked=strict_checked,
        strict_support_positive_count=strict_checked - len(strict_failures),
        strict_support_failures=strict_failures,
        coefficient_sha256=digest.hexdigest(), elapsed_seconds=time.monotonic() - start,
    )


def pin(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_file(path: Path) -> dict:
    data = json.loads(path.read_bytes())
    if not isinstance(data, dict) or type(data.get("a")) is not int:
        raise ValueError("certificate must be an object with integer a")
    a = data["a"]
    if a not in range(4, 9):
        raise ValueError(f"a={a!r} is outside the bounded A64 domain 4..8")
    chambers = data.get("chambers")
    if not isinstance(chambers, list):
        raise ValueError("chambers must be a list")
    rows = {}
    for row in chambers:
        if not isinstance(row, dict) or row.get("chamber") not in CHAMBERS:
            raise ValueError("unknown or malformed chamber")
        name = row["chamber"]
        if name in rows:
            raise ValueError(f"duplicate chamber {name}")
        rows[name] = row
    if set(rows) != set(CHAMBER_NAMES):
        raise ValueError(f"chamber roster differs: have {sorted(rows)!r}")
    results = []
    for name in CHAMBER_NAMES:
        print(f"A64 verifier: a={a} chamber={name} start", flush=True)
        result = check_chamber(a, name, rows[name], data.get("exact_zero_domain"))
        results.append(result)
        print(f"A64 verifier: a={a} chamber={name} {result['status']} "
              f"slots={result['matched_slots']}/{result['domain_slots']} "
              f"seconds={result['elapsed_seconds']:.3f}", flush=True)
    return dict(cert=str(path), a=a, status="PASS" if all(
        row["status"] == "PASS" for row in results) else "FAIL", chambers=results)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cert", action="append", type=Path, required=True,
                        help="producer JSON comparison data; repeat for additional a")
    parser.add_argument("--out", type=Path, required=True,
                        help="new immutable JSON report path")
    args = parser.parse_args()
    started = time.monotonic()
    start_utc = datetime.now(timezone.utc).isoformat()
    paths = [Path(__file__).resolve()] + [path.resolve() for path in args.cert]
    before = {str(path): pin(path) for path in paths}
    reports = []
    errors = []
    seen_a = set()
    for path in paths[1:]:
        try:
            result = verify_file(path)
            if result["a"] in seen_a:
                raise ValueError(f"duplicate a={result['a']} across certificate files")
            seen_a.add(result["a"])
            reports.append(result)
        except Exception as error:
            errors.append(dict(cert=str(path), type=type(error).__name__,
                               message=str(error), traceback=traceback.format_exc(limit=8)))
            print(f"A64 verifier: {path} ERROR {type(error).__name__}: {error}", flush=True)
    after = {str(path): pin(path) for path in paths}
    source_pins = [dict(path=str(path), sha256_before=before[str(path)],
                        sha256_after=after[str(path)],
                        unchanged=(before[str(path)] == after[str(path)]))
                   for path in paths]
    status = "PASS" if (not errors and all(item["status"] == "PASS" for item in reports)
                        and all(item["unchanged"] for item in source_pins)) else "FAIL"
    report = dict(schema="a64-two-active-cap-verification/v1", status=status,
                  started_utc=start_utc, elapsed_seconds=time.monotonic() - started,
                  source_pins=source_pins, source_pins_unchanged=all(
                      item["unchanged"] for item in source_pins),
                  certificates=reports, errors=errors,
                  scope="exact derivative certificates only; no bare originals or actual-degree claim")
    with args.out.open("x", encoding="utf-8") as output:
        json.dump(report, output, indent=2, sort_keys=True)
        output.write("\n")
    print(f"A64 verifier: {status}; report={args.out}", flush=True)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
