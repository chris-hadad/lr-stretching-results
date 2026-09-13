"""Exact counts for two affine interval widths over a composition simplex.

The full lattice object is specified by :func:`two_width_count`. This is an
abstract model; relating it to an LR polynomial requires a separate complete
polytope and lattice map. These formulas do not recognize arbitrary hives or
certify positivity for generic LR polynomials or multiple coupled intervals.
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from math import comb

__all__ = ['two_width_count', 'two_width_polynomial']


def _parameters(left: Sequence[int], right: Sequence[int], total: int,
                left_offset: int, right_offset: int):
    values = (total, left_offset, right_offset)
    if any(type(value) is not int or value < 0 for value in values):
        raise ValueError('total and offsets must be nonnegative exact Python integers')
    for vector in (left, right):
        if (not isinstance(vector, Sequence)
                or isinstance(vector, (str, bytes, bytearray))):
            raise ValueError('width vectors must be sequences of exact Python integers')
    left, right = tuple(left), tuple(right)
    if not left or len(left) != len(right):
        raise ValueError('width vectors must be nonempty and have equal length')
    if any(type(value) is not int or value < 0 for vector in (left, right)
           for value in vector):
        raise ValueError('width entries must be nonnegative exact Python integers')
    return left, right


def _quadratic(left: tuple[int, ...], right: tuple[int, ...], total: int,
               left_offset: int, right_offset: int) -> tuple[Fraction, ...]:
    """The exact normalized degree-two factor in the whole count identity."""
    n = len(left)
    a, b = sum(left), sum(right)
    c = sum(x * z for x, z in zip(left, right))
    alpha = Fraction(a * b + c, n * (n + 1))
    beta = Fraction(n * c - a * b, n * (n + 1))
    linear = (Fraction(left_offset + right_offset)
              + Fraction(total * (a + b), n) + total * beta)
    quadratic = (Fraction(left_offset * right_offset)
                 + Fraction(total * (left_offset * b + right_offset * a), n)
                 + total * total * alpha)
    return Fraction(1), linear, quadratic


def two_width_count(left: Sequence[int], right: Sequence[int], *, total: int = 1,
                    left_offset: int = 0, right_offset: int = 0,
                    dilation: int = 1) -> int:
    """Count every lattice point in the full model at ``dilation=t``.

    With n=len(left)=len(right)>=1, a=left and b=right, the coordinates satisfy
    u_i>=0, sum(u_i)=t*total, 0<=x<=t*left_offset+sum(a_i*u_i), and
    0<=z<=t*right_offset+sum(b_i*u_i). Thus total and both offsets stretch;
    width vectors stay fixed. All entries and scalar inputs must be exact,
    nonnegative Python integers; bools and numerical coercions are rejected.

    The closed identity uses one binomial and a rational quadratic factor.
    Integrality is checked before returning an int. Dilation zero returns one,
    including degenerate models. No enumeration or interpolation is used.
    """
    left, right = _parameters(left, right, total, left_offset, right_offset)
    if type(dilation) is not int or dilation < 0:
        raise ValueError('dilation must be a nonnegative exact Python integer')
    constant, linear, quadratic = _quadratic(left, right, total, left_offset, right_offset)
    n = len(left)
    answer = (comb(total * dilation + n - 1, n - 1)
              * (constant + dilation * linear + dilation * dilation * quadratic))
    if answer.denominator != 1:
        raise ArithmeticError('the exact two-width count is not integral')
    return answer.numerator


def two_width_polynomial(left: Sequence[int], right: Sequence[int], *, total: int = 1,
                         left_offset: int = 0,
                         right_offset: int = 0) -> tuple[Fraction, ...]:
    """Return all ordinary coefficients, low-to-high, as exact Fractions.

    Expand binom(total*t+n-1,n-1) as the product of 1+total*t/k for
    1<=k<n, then multiply by the exact quadratic factor. This is a symbolic
    closed formula, with no fitting or interpolation. Trailing zeros are
    removed, so len(result)-1 is the actual degree for this specified model.
    Its coefficients may be negative; no sufficient sign test is imposed.
    """
    left, right = _parameters(left, right, total, left_offset, right_offset)
    coefficients = list(_quadratic(left, right, total, left_offset, right_offset))
    if total:
        for k in range(1, len(left)):
            slope = Fraction(total, k)
            following = [Fraction(0)] * (len(coefficients) + 1)
            for power, value in enumerate(coefficients):
                following[power] += value
                following[power + 1] += slope * value
            coefficients = following
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)
