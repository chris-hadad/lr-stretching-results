"""Exact arithmetic for the rank-18 positive LR cone and primitive threshold.

Univariate coefficients are ascending. Bivariate keys are monomial exponents.
All reconstruction, count, Routh, and Rouche computations use exact integers
or fractions from the Python standard library.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations
from math import comb, gcd, isqrt, lcm

DEGREE = 31


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def binomial(n, k):
    """Falling-factorial polynomial at an integer n, k>=0."""
    require(k >= 0, "negative binomial degree")
    if n >= 0:
        return comb(n, k) if n >= k else 0
    return (-1) ** k * comb(k - n - 1, k)


def coefficient_b(p, n):
    if n < 0:
        return 0
    if p > 0:
        return comb(n + p - 1, p - 1)
    return (-1) ** n * comb(-p, n) if n <= -p else 0


def literal_flow(A, B, p, h, r):
    if min(A, B) < 0:
        return 0
    return sum(coefficient_b(p, A - k) * coefficient_b(h, k) * coefficient_b(r, B - k) for k in range(min(A, B) + 1))


def short_positive(A, B, p, h, r):
    if A < B:
        A, B, p, r = B, A, r, p
    return sum((-1) ** j * binomial(A + p - 1 - j, p - 1 - j) * comb(h + j - 1, j) * binomial(B + h + r - 1, h + r + j - 1) for j in range(p))


@lru_cache(None)
def profile_polynomial_value(u, v):
    """Evaluate the degree-bounded polynomial, using generalized binomials."""
    x, y = u + v, u + 2 * v
    total = 0
    for i in range(8, 19):
        for k in range(min(4, 18 - i) + 1):
            A, B = (i - 6) * x - y + i - 18, (6 - k) * x - y - 2 * k
            p, h, r = 17 - k, i + k - 1, 17 - i
            if r <= 0:
                D = A - B
                value = binomial(D + p - 1, p - 1) * binomial(B + h - 1, h - 1)
                if r == -1:
                    value -= binomial(D + p, p - 1) * binomial(B + h - 2, h - 1)
                else:
                    require(r == 0, "unexpected exceptional exponent")
            else:
                # This ordering is eventual on the entire closed chamber;
                # do not branch on small numerical A,B in a polynomial.
                if i + k < 13:
                    A, B, p, r = B, A, r, p
                value = sum((-1) ** j * binomial(A + p - 1 - j, p - 1 - j) * comb(h + j - 1, j) * binomial(B + h + r - 1, h + r + j - 1) for j in range(p))
            total += (-1) ** (18 - i - k) * comb(18, i) * comb(18 - i, k) * value
    return total


def binomial_polynomials(n):
    rows = [[Q(1)]]
    for k in range(1, n + 1):
        row = [Q(0)] * (k + 1)
        for j, value in enumerate(rows[-1]):
            row[j] -= value * Q(k - 1, k)
            row[j + 1] += value / k
        rows.append(row)
    return rows


def construct_H():
    # Unisolvent simplex evaluations of a mathematically prior-bounded
    # polynomial. These are not asserted to be native count evaluations.
    values = {(a, b): profile_polynomial_value(a, b) for a in range(DEGREE + 1) for b in range(DEGREE + 1 - a)}
    differences = {}
    for i in range(DEGREE + 1):
        for j in range(DEGREE + 1 - i):
            differences[i, j] = sum((-1) ** (i + j - a - b) * comb(i, a) * comb(j, b) * values[a, b] for a in range(i + 1) for b in range(j + 1))
    basis = binomial_polynomials(DEGREE)
    H = {(a, b): Q(0) for a in range(DEGREE + 1) for b in range(DEGREE + 1 - a)}
    for (i, j), weight in differences.items():
        if not weight:
            continue
        for a, ca in enumerate(basis[i]):
            for b, cb in enumerate(basis[j]):
                H[a, b] += weight * ca * cb
    return H, values, differences


def linear_substitution(H, a, b, c, d):
    """H(a*x+b*y,c*x+d*y)."""
    result = {(i, j): Q(0) for i in range(DEGREE + 1) for j in range(DEGREE + 1 - i)}
    for (i, j), weight in H.items():
        for yi in range(i + 1):
            for yj in range(j + 1):
                result[i + j - yi - yj, yi + yj] += weight * comb(i, yi) * a ** (i - yi) * b ** yi * comb(j, yj) * c ** (j - yj) * d ** yj
    return result


def encode_poly(poly, names):
    return [{names[0]: i, names[1]: j, "coefficient": str(c)} for (i, j), c in sorted(poly.items())]


def decode_poly(rows, names):
    result = {(row[names[0]], row[names[1]]): Q(row["coefficient"]) for row in rows}
    require(len(result) == len(rows), "duplicate coefficient key")
    return result


def evaluate(H, u, v):
    return sum(c * u ** i * v ** j for (i, j), c in H.items())


def ray_coefficients(H, u, v):
    result = [Q(0)] * (DEGREE + 1)
    for (i, j), c in H.items():
        result[i + j] += c * u ** i * v ** j
    return result


def value_at(coefficients, t):
    value = Q(0)
    for c in reversed(coefficients):
        value = value * t + c
    return value


def literal_count(x, y):
    require(x >= 1 and x <= y <= 2 * x, "outside fixed chamber")
    total = 0
    for i in range(19):
        for k in range(19 - i):
            A, B = (i - 6) * x - y + i - 18, (6 - k) * x - y - 2 * k
            total += (-1) ** (18 - i - k) * comb(18, i) * comb(18 - i, k) * literal_flow(A, B, 17 - k, i + k - 1, 17 - i)
    return total


def direct_character_count(x, y):
    """Multiply h_x^18 as a positive coefficient grid; extract six alternant terms.

    This uses neither partial fractions nor the A2 flow expression.
    """
    shape, delta = (6 * x + y, 6 * x, 6 * x - y), (2, 1, 0)
    targets = []
    for perm in permutations(delta):
        sign = (-1) ** sum(perm[i] < perm[j] for i in range(3) for j in range(i + 1, 3))
        exp = tuple(shape[i] + delta[i] - perm[i] for i in range(3))
        targets.append((sign, exp[1], exp[2]))
    cap_b = max(b for _, b, _ in targets)
    cap_c = max(c for _, _, c in targets)
    increments = [(b, c) for b in range(x + 1) for c in range(x + 1 - b)]
    grid = {(0, 0): 1}
    for _ in range(18):
        following = {}
        for (b, c), value in grid.items():
            for db, dc in increments:
                if b + db <= cap_b and c + dc <= cap_c:
                    key = (b + db, c + dc)
                    following[key] = following.get(key, 0) + value
        grid = following
    return sum(sign * grid.get((b, c), 0) for sign, b, c in targets)


def primitive_row(row):
    g = 0
    for value in row:
        g = gcd(g, value)
    require(g != 0, "zero Routh row")
    return [value // g for value in row]


def routh(coefficients):
    require(coefficients and coefficients[0] != 0 and coefficients[-1] != 0, "degenerate polynomial")
    denominator = 1
    for value in coefficients:
        denominator = lcm(denominator, value.denominator)
    descending = [int(c * denominator) for c in reversed(coefficients)]
    n, width = len(descending) - 1, (len(descending) + 1) // 2
    a = primitive_row(descending[::2] + [0] * (width - len(descending[::2])))
    b = primitive_row(descending[1::2] + [0] * (width - len(descending[1::2])))
    require(a[0] != 0 and b[0] != 0, "initial zero Routh pivot")
    columns = [a[0], b[0]]
    for step in range(n - 1):
        sign = 1 if b[0] > 0 else -1
        row = [sign * (b[0] * a[j + 1] - a[0] * b[j + 1]) for j in range(width - 1)] + [0]
        row = primitive_row(row)
        require(row[0] != 0, f"zero Routh pivot at row {step + 2}")
        columns.append(row[0])
        a, b = b, row
    signs = [1 if x > 0 else -1 for x in columns]
    return {"status": "regular", "rhp_count": sum(a != b for a, b in zip(signs, signs[1:])), "signs": signs, "primitive_first_column": [str(x) for x in columns]}


def gaussian_mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def normalized_G(H):
    result = [[Q(0)] * (d + 1) for d in range(DEGREE + 1)]
    for (i, j), c in H.items():
        for k in range(i + 1):
            result[i + j][j + k] += c * comb(i, k) * (-1) ** k
    return result


def rouche(H, disk):
    e0, eta = Q(disk["epsilon_center"]), Q(disk["epsilon_radius"])
    lo, hi = map(Q, disk["epsilon_interval"])
    center, radius = tuple(map(Q, disk["z_center"])), Q(disk["z_radius"])
    require(lo == e0 - eta and hi == e0 + eta and eta > 0, "inconsistent parameter interval")
    require(radius > 0 and center[0] > radius and center[1] > radius, "disk outside separated upper RHP")
    G = normalized_G(H)
    epowers = [e0 ** k for k in range(DEGREE + 1)]
    cpower = [(Q(1), Q(0))]
    for _ in range(DEGREE):
        cpower.append(gaussian_mul(cpower[-1], center))
    shifted_e = [[sum(G[d][l] * comb(l, k) * epowers[l - k] for l in range(k, d + 1)) for k in range(d + 1)] for d in range(DEGREE + 1)]
    taylor = {}
    for j in range(DEGREE + 1):
        for k in range(DEGREE + 1):
            real = imag = Q(0)
            for d in range(max(j, k), DEGREE + 1):
                factor = shifted_e[d][k] * comb(d, j)
                real += factor * cpower[d - j][0]
                imag += factor * cpower[d - j][1]
            taylor[j, k] = real, imag
    scale = 10 ** 30
    U, by_z_degree = Q(0), []
    for j in range(DEGREE + 1):
        group = Q(0)
        for k in range(DEGREE + 1):
            if (j, k) == (1, 0):
                continue
            real, imag = taylor[j, k]
            square = real * real + imag * imag
            upper = Q(0) if square == 0 else Q(isqrt(square.numerator * scale * scale // square.denominator) + 1, scale)
            require(upper * upper >= square, "invalid rational modulus upper bound")
            group += upper * radius ** j * eta ** k
        by_z_degree.append(str(group))
        U += group
    re, im = taylor[1, 0]
    linear_square = (re * re + im * im) * radius * radius
    gap = linear_square - U * U
    require(gap > 0, "Rouche strict inequality failed")
    ratio_square = U * U / linear_square
    rounded = Q((ratio_square.numerator * 10 ** 12 + ratio_square.denominator - 1) // ratio_square.denominator, 10 ** 12)
    return {"interval": [str(lo), str(hi)], "center": [str(c) for c in center], "radius": str(radius), "left_margin": str(center[0] - radius), "conjugate_separation_margin": str(center[1] - radius), "modulus_bound_scale": str(scale), "remainder_majorants_by_z_degree": by_z_degree, "remainder_upper": str(U), "linear_modulus_squared_times_radius_squared": str(linear_square), "strict_squared_gap": str(gap), "squared_ratio_upper_rounded": str(rounded), "roots_in_upper_disk_for_every_parameter": 1, "rhp_roots_uniform_lower_bound": 2}

def selftest(H, disks):
    # Known factor/root locations exercise positive row scaling and
    # signs independently of the scientific coefficient fixtures.
    known = [([1, 1], 0), ([-1, 1], 1), ([2, 3, 1], 0), ([2, -3, 1], 2), ([-2, -1, 1], 1), ([6, 11, 6, 1], 0)]
    for coefficients, count in known:
        require(routh(list(map(Q, coefficients)))["rhp_count"] == count, "known-root Routh control failed")
    rejected = []
    for name, coefficients in [("imaginary_axis_zero_row", [1, 1, 1, 1]), ("zero_pivot", [1, 1, 1, 1, 1])]:
        try:
            routh(list(map(Q, coefficients)))
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("degenerate Routh fixture was accepted")
    disk = dict(disks[0])
    disk["z_radius"] = "1"
    try:
        rouche(H, disk)
    except AssertionError:
        rejected.append("disk_crossing_imaginary_axis")
    else:
        raise AssertionError("geometrically invalid disk was accepted")
    disk = dict(disks[0])
    disk["epsilon_center"] = "0"
    try:
        rouche(H, disk)
    except AssertionError:
        rejected.append("inconsistent_parameter_interval")
    else:
        raise AssertionError("inconsistent interval was accepted")
    disk = dict(disks[0])
    disk["z_center"] = ["1", "1"]
    try:
        rouche(H, disk)
    except AssertionError as error:
        require(str(error) == "Rouche strict inequality failed", "wrong failure for false root witness")
        rejected.append("false_root_witness")
    else:
        raise AssertionError("false root disk was accepted")
    return {"known_root_routh_controls": len(known), "negative_fixtures_rejected": rejected}


def count_controls(H):
    cases = [(x, y) for x in range(1, 7) for y in range(x, 2 * x + 1)] + [(23, 24), (33, 34), (37, 55), (47, 56)]
    counts = []
    for x, y in cases:
        actual, predicted = literal_count(x, y), evaluate(H, 2 * x - y, y - x)
        require(actual == predicted, f"literal count mismatch at {(x,y)}")
        counts.append({"x": x, "y": y, "exact_count": str(actual)})
    characters = []
    for x in range(1, 4):
        for y in range(x, 2 * x + 1):
            actual = direct_character_count(x, y)
            require(actual == evaluate(H, 2 * x - y, y - x), "independent character-grid mismatch")
            characters.append({"x": x, "y": y, "exact_count": str(actual)})
    checked = 0
    for p in range(1, 5):
        for h in range(1, 5):
            for r in range(1, 5):
                for A in range(13):
                    for B in range(13):
                        require(short_positive(A, B, p, h, r) == literal_flow(A, B, p, h, r), "short-flow identity control failed")
                        checked += 1
    return {"literal_counts": counts, "independent_positive_character_grid_counts": characters, "short_flow_identity_cases": checked}


def exact_count(value):
    """Accept only exact nonnegative integer count data, never a truncation."""
    if type(value) is int:
        require(value >= 0, "negative count")
        return value
    require(isinstance(value, str) and value.isascii() and value.isdecimal(),
            "count must be an exact nonnegative integer")
    return int(value)


def q_threshold(H, q_records):
    require(len(q_records) == 23, "the q certificate roster must contain exactly 23 polynomials")
    rows = []
    for q, supplied in enumerate(q_records, 1):
        require(type(supplied["q"]) is int and type(supplied["s"]) is int,
                "q parameters must be exact integers")
        require(q == supplied["q"] and supplied["s"] == q + 1, "q record order or parameter mismatch")
        require(supplied["lambda"] == [q * i for i in range(18, 0, -1)] and supplied["mu"] == [q * i for i in range(17, 0, -1)] and supplied["nu"] == [7 * q + 1, 6 * q, 5 * q - 1], "LR boundary mismatch")
        coefficients = ray_coefficients(H, q - 1, 1)
        require(coefficients == list(map(Q, supplied["coefficients"])), "q coefficient mismatch")
        determining = supplied["determining_values_t0_through31"]
        holdouts = supplied["unused_holdouts"]
        require(isinstance(determining, list) and len(determining) == 32,
                "exactly 32 determining counts required")
        require(isinstance(holdouts, list) and len(holdouts) == 3
                and all(type(row["t"]) is int for row in holdouts)
                and [row["t"] for row in holdouts] == [32, 33, 36],
                "complete unused holdout roster 32,33,36 required")
        for t, v in enumerate(determining):
            require(value_at(coefficients, t) == exact_count(v), "q determining value mismatch")
        for row in holdouts:
            require(value_at(coefficients, row["t"]) == exact_count(row["value"]), "q supplied holdout mismatch")
        table = routh(coefficients)
        require(table["rhp_count"] == (0 if q <= 22 else 2), "q threshold Routh mismatch")
        rows.append({"q": q, "coefficients": [str(c) for c in coefficients], **table})
    return {"q_range": [1, 23], "regular_tables": 23, "strictly_hurwitz_q": list(range(1, 23)), "q23_rhp_count": 2, "coefficient_and_supplied_value_agreements": True, "rows": rows}


def count_data_selftest(H, q_records):
    """Regression controls for absent rosters and lossy count coercion."""
    from copy import deepcopy
    rejected = []
    for name in ("missing_determining", "short_determining", "missing_holdouts",
                 "wrong_holdout_site", "fractional_count", "boolean_count",
                 "fractional_string", "float_holdout_site"):
        records = deepcopy(q_records)
        row = records[0]
        if name == "missing_determining": row["determining_values_t0_through31"] = []
        elif name == "short_determining": row["determining_values_t0_through31"].pop()
        elif name == "missing_holdouts": row["unused_holdouts"] = []
        elif name == "wrong_holdout_site": row["unused_holdouts"][0]["t"] = 31
        elif name == "fractional_count": row["determining_values_t0_through31"][0] = 1.5
        elif name == "boolean_count": row["determining_values_t0_through31"][0] = True
        elif name == "fractional_string": row["determining_values_t0_through31"][0] = "1.5"
        else: row["unused_holdouts"][0]["t"] = 32.0
        try:
            q_threshold(H, records)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("invalid count-data fixture accepted: " + name)
    return rejected
