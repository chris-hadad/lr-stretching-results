"""Exact entire three-row transportation polynomials in the original stretch."""

from fractions import Fraction as Q
from itertools import product
from .affine import flow_polynomial, one_overlap_polynomial, PolynomialResourceLimit


def _vector(values, name):
    try:
        values = tuple(values)
    except TypeError as error:
        raise ValueError(name + " must be an integer vector") from error
    if not values or any(type(x) is not int or x < 0 for x in values):
        raise ValueError(name + " requires a nonempty nonnegative exact-integer vector")
    return values


def transport_polynomial(rows, columns, *, max_assignments=20000, max_degree=24):
    rows = _vector(rows, "rows")
    columns = _vector(columns, "columns")
    if len(rows) > 3:
        raise ValueError("At most three supplied rows")
    if sum(rows) != sum(columns):
        raise ValueError("Balanced margins required")
    if type(max_assignments) is not int or max_assignments < 1:
        raise ValueError("Positive exact assignment cap required")
    if type(max_degree) is not int or max_degree < 0:
        raise ValueError("Nonnegative exact degree cap required")
    columns = tuple(x for x in columns if x)
    if not columns:
        return (Q(1),)
    rows = rows + (0,) * (3 - len(rows))
    n = len(columns)
    cost = 1
    for _ in columns:
        cost *= 3
        if cost > max_assignments:
            raise PolynomialResourceLimit(
                "complete transportation assignments", cost, max_assignments
            )
    bound = max(0, 2 * n - 2)
    if bound > max_degree:
        raise PolynomialResourceLimit(
            "transportation expansion degree", bound, max_degree
        )
    total = [Q(0)] * (bound + 1)
    for assignment in product(range(3), repeat=n):
        occupation = tuple(assignment.count(i) for i in range(3))
        assigned = tuple(
            sum(w for w, a in zip(columns, assignment) if a == i) for i in range(3)
        )
        slopes = tuple(assigned[i] - rows[i] for i in range(3))
        offsets = tuple(i * occupation[i] - sum(occupation[i + 1 :]) for i in range(3))
        multiplicities = tuple(
            occupation[i] + occupation[j] for i, j in [(0, 1), (0, 2), (1, 2)]
        )
        polynomial = flow_polynomial(multiplicities, slopes, offsets, max_degree=bound)
        sign = (-1) ** (occupation[1] + 2 * occupation[2])
        for k, value in enumerate(polynomial):
            total[k] += sign * value
    while len(total) > 1 and total[-1] == 0:
        total.pop()
    return tuple(total)


def capped_polynomial(
    weights,
    c,
    d,
    *,
    max_assignments=100000,
    max_total_assignments=200000,
    max_degree=32,
):
    weights = _vector(weights, "weights")
    if (
        type(c) is not int
        or type(d) is not int
        or c < 0
        or d < 0
        or sum(weights) < c + d
    ):
        raise ValueError("Nonnegative exact c,d and sum(weights)>=c+d required")
    u = c + d
    result = one_overlap_polynomial(
        u,
        u,
        c,
        weights,
        (sum(weights) + d, c + d, c),
        max_assignments=max_assignments,
        max_total_assignments=max_total_assignments,
        max_degree=max_degree,
    )
    return result["coefficients"]
