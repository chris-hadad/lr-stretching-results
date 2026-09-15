"""Complete exact eventual affine A2/three-row coefficient polynomials.

Coefficient tuples use ascending powers of t and contain Fraction instances.
The zero polynomial is (Fraction(0),); trailing zero coefficients are removed.
Individual affine products are eventual polynomials. Complete ordinary LR
stretching families have their usual all-positive-integer polynomial meaning.
No numerical fitting, external imports, filesystem access or execution on import.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb, factorial

DEFAULT_MAX_DEGREE = 32
ZERO = (Q(0),)
ONE = (Q(1),)
EDGES = ((0, 1), (0, 2), (1, 2))


class PolynomialResourceLimit(RuntimeError):
    """Complete work exceeds a cap; required may be a certified lower bound."""

    def __init__(self, scope, required, limit):
        self.scope = scope
        self.required = required
        self.limit = limit
        super().__init__(f"{scope} requires {required}; limit is {limit}")


def _limit(value, name, *, allow_zero=False):
    minimum = 0 if allow_zero else 1
    if type(value) is not int or value < minimum:
        kind = "nonnegative" if allow_zero else "positive"
        raise ValueError(f"{name} must be a {kind} integer, excluding bool")
    return value


def _integers(values, name, *, nonnegative=False):
    try:
        values = tuple(values)
    except TypeError as exc:
        raise ValueError(f"{name} must be an iterable of integers") from exc
    if any(type(value) is not int for value in values):
        raise ValueError(f"{name} must contain exact integers, excluding bool")
    if nonnegative and any(value < 0 for value in values):
        raise ValueError(f"{name} must contain nonnegative integers")
    return values


def _partition(values, name, *, max_length=None):
    values = _integers(values, name, nonnegative=True)
    if max_length is not None and len(values) > max_length:
        raise ValueError(f"{name} must have at most {max_length} entries")
    if any(a < b for a, b in zip(values, values[1:])):
        raise ValueError(f"{name} must be a weakly decreasing partition")
    return values


def _trim(coefficients):
    coefficients = list(coefficients)
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


def _add(left, right, sign=1):
    coefficients = [Q(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        coefficients[i] += value
    for i, value in enumerate(right):
        coefficients[i] += sign * value
    return _trim(coefficients)


def _multiply(left, right):
    if left == ZERO or right == ZERO:
        return ZERO
    coefficients = [Q(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            coefficients[i + j] += x * y
    return _trim(coefficients)


def _binomial(slope, offset, degree):
    """Coefficients of binom(slope*t + offset, degree), already priced."""
    coefficients = [1]
    for i in range(degree):
        following = [0] * (len(coefficients) + 1)
        for j, value in enumerate(coefficients):
            following[j] += (offset - i) * value
            following[j + 1] += slope * value
        coefficients = following
    denominator = factorial(degree)
    return _trim(Q(value, denominator) for value in coefficients)


def _bundle(multiplicity, slope, offset):
    if multiplicity == 0:
        return ONE if slope == offset == 0 else ZERO
    if (slope, offset) < (0, 0):
        return ZERO
    return _binomial(slope, offset + multiplicity - 1, multiplicity - 1)


def _left(a, b, c, A, B, A0, B0):
    """Full left chamber polynomial; b and c are positive."""
    coefficients = ZERO
    for j in range(c):
        u = _binomial(B, B0 + c - 1 - j, c - 1 - j)
        v = _binomial(A, A0 + a + b - 1, a + b + j - 1)
        factor = (-1) ** j * comb(b + j - 1, j)
        coefficients = _add(coefficients, _multiply(u, v), factor)
    return coefficients


def _flow(multiplicities, slope, offset):
    """Pinned flow_jet support branches, with full polynomial arithmetic."""
    a, b, c = multiplicities
    A, B, A0, B0 = slope[0], -slope[2], offset[0], -offset[2]
    if b == 0:
        return _multiply(_bundle(a, A, A0), _bundle(c, B, B0))
    if a == c == 0:
        if (A - B, A0 - B0) != (0, 0):
            return ZERO
        return _bundle(b, A, A0)
    if a == 0:
        return _multiply(_bundle(b, A, A0), _bundle(c, B - A, B0 - A0))
    if c == 0:
        return _multiply(_bundle(a, A - B, A0 - B0), _bundle(b, B, B0))
    if (A, A0) < (0, 0) or (B, B0) < (0, 0):
        return ZERO
    if (A - B, A0 - B0) <= (0, 0):
        return _left(a, b, c, A, B, A0, B0)
    return _left(c, b, a, B, A, B0, A0)


def _check_degree(bound, limit, scope):
    if bound > limit:
        raise PolynomialResourceLimit(scope, bound, limit)


def flow_polynomial(multiplicities, slope, offset, *, max_degree=DEFAULT_MAX_DEGREE):
    """Full eventual A2 flow polynomial in the original integer lattice.

    All three vectors have length three and contain exact integers. Edge
    multiplicities are nonnegative, and each netflow vector sums to zero.
    The degree cap bounds the full chamber expansion, before support trimming.
    """
    degree_limit = _limit(max_degree, "max_degree", allow_zero=True)
    multiplicities = _integers(multiplicities, "multiplicities", nonnegative=True)
    slope = _integers(slope, "slope")
    offset = _integers(offset, "offset")
    if any(len(vector) != 3 for vector in (multiplicities, slope, offset)):
        raise ValueError("Three edge multiplicities and three-entry netflows required")
    if sum(slope) or sum(offset):
        raise ValueError("A2 netflow vectors must each sum to zero")
    positive_edges = sum(m > 0 for m in multiplicities)
    incidence_rank = min(positive_edges, 2)
    bound = sum(multiplicities) - incidence_rank
    _check_degree(bound, degree_limit, "A2 expansion degree")
    return _flow(multiplicities, slope, offset)


def _product_spec(weights, offsets, alpha):
    """Validate the balanced interface, retaining every nonzero fixed factor."""
    weights = _integers(weights, "weights", nonnegative=True)
    offsets = _integers(offsets, "offsets")
    alpha = _partition(alpha, "alpha", max_length=3)
    alpha += (0,) * (3 - len(alpha))
    if len(weights) != len(offsets):
        raise ValueError("weights and offsets must have the same length")
    if sum(weights) != sum(alpha) or sum(offsets) != 0:
        raise ValueError("Require sum(weights) = sum(alpha) and sum(offsets) = 0")
    pairs = tuple(zip(weights, offsets))
    zero_reason = (
        "negative fixed degree" if any(w == 0 and b < 0 for w, b in pairs) else None
    )
    active = tuple((w, b) for w, b in pairs if (w, b) != (0, 0))
    return weights, offsets, alpha, active, zero_reason


def _assignment_cost(active, zero_reason, limit):
    if zero_reason is not None:
        return 0
    cost = 1
    for _ in active:
        cost *= 3
        if cost > limit:
            raise PolynomialResourceLimit(
                "complete assignments for one product", cost, limit
            )
    return cost


def _price(active, zero_reason, assignment_limit, degree_limit):
    cost = _assignment_cost(active, zero_reason, assignment_limit)
    # One occupied node has two bundles of multiplicity r-1. Other
    # occupations have degree at most 2*r-5. No cancellation is priced in.
    bound = 0 if zero_reason is not None else max(0, 2 * len(active) - 4)
    _check_degree(bound, degree_limit, "affine product expansion degree")
    return cost, bound


def _affine_polynomial(active, alpha, zero_reason):
    if zero_reason is not None:
        return ZERO
    if not active:
        return ONE
    total = ZERO
    for assignment in product(range(3), repeat=len(active)):
        occupation = tuple(assignment.count(i) for i in range(3))
        slopes, shifts = [0, 0, 0], [0, 0, 0]
        for (weight, offset), node in zip(active, assignment):
            slopes[node] += weight
            shifts[node] += offset
        slope = tuple(slopes[i] - alpha[i] for i in range(3))
        delta = tuple(
            i * occupation[i] - sum(occupation[i + 1 :]) + shifts[i] for i in range(3)
        )
        signed_m = tuple(occupation[i] + occupation[j] - 1 for i, j in EDGES)
        positive = tuple(max(m, 0) for m in signed_m)
        missing = tuple(edge for edge, m in zip(EDGES, signed_m) if m == -1)
        sign = (-1) ** (occupation[1] + 2 * occupation[2])
        for size in range(len(missing) + 1):
            for chosen in combinations(missing, size):
                offset = list(delta)
                for i, j in chosen:
                    offset[i] -= 1
                    offset[j] += 1
                term = _flow(positive, slope, tuple(offset))
                total = _add(total, term, sign * (-1) ** size)
    return total


def affine_kostka_polynomial(
    weights,
    offsets,
    alpha,
    *,
    max_assignments=100000,
    max_degree=DEFAULT_MAX_DEGREE,
):
    """Complete eventual [s_(t alpha)] product_l h_(t weights_l + offsets_l).

    Return a trimmed ascending Fraction tuple. Slopes are nonnegative;
    alpha has at most three rows; sums of slopes/shape and offsets balance.
    max_degree bounds pre-cancellation expansion, not only the final degree.
    """
    assignment_limit = _limit(max_assignments, "max_assignments")
    degree_limit = _limit(max_degree, "max_degree", allow_zero=True)
    _, _, alpha, active, zero_reason = _product_spec(weights, offsets, alpha)
    _price(active, zero_reason, assignment_limit, degree_limit)
    return _affine_polynomial(active, alpha, zero_reason)


def _signed_term(label, sign, weights, offsets, coefficients, zero_reason, cost, bound):
    return {
        "label": label,
        "sign": sign,
        "weights": weights,
        "offsets": offsets,
        "coefficients": coefficients,
        "signed_coefficients": tuple(sign * value for value in coefficients),
        "zero_reason": zero_reason,
        "assignment_cost": cost,
        "degree_bound": bound,
    }


def _coefficient_fields(coefficients):
    return {
        "coefficients": coefficients,
        "constant": coefficients[0],
        "c1": coefficients[1] if len(coefficients) > 1 else Q(0),
        "c2": coefficients[2] if len(coefficients) > 2 else Q(0),
        "degree": -1 if coefficients == ZERO else len(coefficients) - 1,
    }


def one_overlap_polynomial(
    u,
    v,
    h,
    remaining,
    alpha,
    *,
    max_assignments=100000,
    max_total_assignments=200000,
    max_degree=DEFAULT_MAX_DEGREE,
):
    """Entire one-overlap character polynomial, with both signed products.

    Extract s_(t alpha) from
      (h_(ut) h_(vt) - h_((u+v-h)t+1) h_(ht-1)) product h_(t remaining_i).
    The input domain is u,v >= h >= 0. Both product/degree caps and the total
    assignment cap are checked before either product is expanded.
    """
    assignment_limit = _limit(max_assignments, "max_assignments")
    total_limit = _limit(max_total_assignments, "max_total_assignments")
    degree_limit = _limit(max_degree, "max_degree", allow_zero=True)
    if any(type(value) is not int for value in (u, v, h)):
        raise ValueError("u, v and h must be exact integers, excluding bool")
    if h < 0 or u < h or v < h:
        raise ValueError("Require u, v >= h >= 0")
    remaining = _integers(remaining, "remaining", nonnegative=True)
    alpha = _partition(alpha, "alpha", max_length=3)
    first = _product_spec((u, v) + remaining, (0,) * (2 + len(remaining)), alpha)
    second = _product_spec(
        (u + v - h, h) + remaining, (1, -1) + (0,) * len(remaining), alpha
    )
    prices = tuple(
        _price(spec[3], spec[4], assignment_limit, degree_limit)
        for spec in (first, second)
    )
    total_cost = sum(price[0] for price in prices)
    if total_cost > total_limit:
        raise PolynomialResourceLimit(
            "one-overlap total assignments", total_cost, total_limit
        )
    homogeneous = _affine_polynomial(first[3], first[2], first[4])
    affine = _affine_polynomial(second[3], second[2], second[4])
    terms = (
        _signed_term(
            "homogeneous", 1, first[0], first[1], homogeneous, first[4], *prices[0]
        ),
        _signed_term("affine", -1, second[0], second[1], affine, second[4], *prices[1]),
    )
    return {
        "alpha": first[2],
        "homogeneous": homogeneous,
        "affine": affine,
        "signed_terms": terms,
        "assignment_cost": total_cost,
        "degree_bound": max(price[1] for price in prices),
        **_coefficient_fields(_add(homogeneous, affine, -1)),
    }


def jacobi_trudi_polynomial(
    outer,
    inner,
    alpha,
    *,
    max_permutations=720,
    max_assignments=100000,
    max_total_assignments=1000000,
    max_degree=DEFAULT_MAX_DEGREE,
):
    """Whole c^(t outer)_(t inner,t alpha), preserving every permutation.

    Use original degrees t*(outer_i-inner_pi(i)) + pi(i)-i. Negative slopes
    are eventual-zero products; fixed negative degrees are identically zero.
    All zero records, offsets and trailing zero rows are retained. Price the
    complete determinant before polynomial arithmetic; no partial return.
    """
    permutation_limit = _limit(max_permutations, "max_permutations")
    assignment_limit = _limit(max_assignments, "max_assignments")
    total_limit = _limit(max_total_assignments, "max_total_assignments")
    degree_limit = _limit(max_degree, "max_degree", allow_zero=True)
    outer = _partition(outer, "outer")
    inner = _partition(inner, "inner")
    alpha = _partition(alpha, "alpha", max_length=3)
    n = max(len(outer), len(inner))
    outer += (0,) * (n - len(outer))
    inner += (0,) * (n - len(inner))
    if any(mu > lam for lam, mu in zip(outer, inner)):
        raise ValueError("inner must be contained in outer")
    if sum(outer) - sum(inner) != sum(alpha):
        raise ValueError("Require |outer| - |inner| = |alpha|")
    permutation_count = 1
    for size in range(2, n + 1):
        permutation_count *= size
        if permutation_count > permutation_limit:
            raise PolynomialResourceLimit(
                "Jacobi-Trudi permutations", permutation_count, permutation_limit
            )

    specs, total_cost = [], 0
    for permutation in permutations(range(n)):
        sign = (-1) ** sum(
            permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n)
        )
        weights = tuple(outer[i] - inner[permutation[i]] for i in range(n))
        offsets = tuple(permutation[i] - i for i in range(n))
        zero_reason = None
        if any(w < 0 for w in weights):
            zero_reason = "eventually negative degree"
        elif any(w == 0 and b < 0 for w, b in zip(weights, offsets)):
            zero_reason = "negative fixed degree"
        active = tuple((w, b) for w, b in zip(weights, offsets) if (w, b) != (0, 0))
        cost, bound = _price(active, zero_reason, assignment_limit, degree_limit)
        total_cost += cost
        if total_cost > total_limit:
            raise PolynomialResourceLimit(
                "Jacobi-Trudi total assignments", total_cost, total_limit
            )
        specs.append(
            (permutation, sign, weights, offsets, active, zero_reason, cost, bound)
        )

    padded_alpha = alpha + (0,) * (3 - len(alpha))
    terms, total = [], ZERO
    for permutation, sign, weights, offsets, active, zero_reason, cost, bound in specs:
        coefficients = _affine_polynomial(active, padded_alpha, zero_reason)
        term = _signed_term(
            "Jacobi-Trudi",
            sign,
            weights,
            offsets,
            coefficients,
            zero_reason,
            cost,
            bound,
        )
        term["permutation"] = permutation
        terms.append(term)
        total = _add(total, term["signed_coefficients"])
    return {
        "outer": outer,
        "inner": inner,
        "alpha": padded_alpha,
        "signed_terms": tuple(terms),
        "permutation_count": permutation_count,
        "assignment_cost": total_cost,
        "degree_bound": max(term["degree_bound"] for term in terms),
        **_coefficient_fields(total),
    }
