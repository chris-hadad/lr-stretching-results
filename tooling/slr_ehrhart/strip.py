"""Exact counts for an admissible interval over a split composition simplex.

The complete lattice object is specified by :func:`strip_count`. Relating it
to an LR polynomial requires a separate whole-polytope and lattice map. The
formulas do not recognize arbitrary hives or certify a complete rank/box cover.
"""
from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from math import comb, prod

__all__ = ['strip_count', 'strip_polynomial']


def _parameters(h: int, q1: int, q2: int, total: int, lower_cap: int,
                upper_cap: int, height: int, interval_lengths: Sequence[int]):
    values = (h, q1, q2, total, lower_cap, upper_cap, height)
    if any(type(value) is not int for value in values):
        raise ValueError('strip parameters must be exact Python integers')
    if min(h, total, lower_cap, upper_cap, height) < 0 or min(q1, q2) < 1:
        raise ValueError('h,T,B,C,D must be nonnegative and q1,q2 positive')
    if total > lower_cap + upper_cap + height:
        raise ValueError('the complete interval requires T <= B+C+D')
    if (not isinstance(interval_lengths, Sequence)
            or isinstance(interval_lengths, (str, bytes, bytearray))):
        raise ValueError('interval_lengths must be a sequence of exact integers')
    intervals = tuple(interval_lengths)
    if any(type(value) is not int or value < 0 for value in intervals):
        raise ValueError('independent interval lengths must be nonnegative exact integers')
    return intervals


def _capped_moment(p: int, q: int, excess: int, cap: int) -> int:
    """Sum min(cap,V) over p+q-part compositions of excess+cap.

    The rising-binomial expansion uses p+q terms. Clearing its only
    denominator via W/r * binom(W+r-1,r-1) = binom(W+r-1,r) leaves integers.
    """
    if cap == 0:
        return 0
    n = p + q
    answer = 0
    for k in range(n):
        if k and excess == 0:
            break
        rising = 1 if k == 0 else comb(excess + k - 1, k)
        remaining = n - k
        moment = (p * comb(cap + remaining - 1, remaining) if k < q else
                  cap * comb(cap + remaining - 1, remaining - 1))
        answer += rising * moment
    return answer


def strip_count(h: int, q1: int, q2: int, total: int, lower_cap: int,
                upper_cap: int, height: int, t: int = 1, *,
                interval_lengths: Sequence[int] = ()) -> int:
    """Count the entire admissible split-simplex interval at stretch ``t``.

    There are h+q1+q2 nonnegative composition coordinates, in groups with
    totals U,V,R and U+V+R=t*T. When h=0, U=0. One integer s satisfies
    max(0,V-t*B) <= s <= t*D+min(t*C,U+V). Here T=total,
    B=lower_cap, C=upper_cap and D=height. Require T<=B+C+D, h>=0,
    q1,q2>=1 and nonnegative T,B,C,D,t. Every input is an exact Python int;
    bools and numerical coercions are rejected. Optional independent
    intervals contribute product(t*length+1); they are not coupled fibers.

    The sum is evaluated with at most 2*(h+q1+q2) binomial terms, independent
    of parameter magnitude in arithmetic-operation count. Big-integer cost
    and dimension remain relevant. t=0 returns 1, including dimension drops.
    No engine, filesystem operation, process or cross-call cache is used.
    """
    intervals = _parameters(h, q1, q2, total, lower_cap, upper_cap, height, interval_lengths)
    if type(t) is not int or t < 0:
        raise ValueError('t must be a nonnegative exact Python integer')
    n = h + q1 + q2
    total *= t
    lower_cap = min(lower_cap * t, total)
    upper_cap = min(upper_cap * t, total)
    height *= t
    simplex = comb(total + n - 1, n - 1)
    # Interval length = D+1 - V + min(C,U+V) + min(B,V).
    answer = ((height + 1) * simplex - q1 * comb(total + n - 1, n)
              + _capped_moment(h + q1, q2, total - upper_cap, upper_cap)
              + _capped_moment(q1, h + q2, total - lower_cap, lower_cap))
    return answer * prod(t * length + 1 for length in intervals)


def strip_polynomial(h: int, q1: int, q2: int, total: int, lower_cap: int,
                     upper_cap: int, height: int, *,
                     interval_lengths: Sequence[int] = ()) -> tuple[Fraction, ...]:
    """Return every ordinary coefficient, low-to-high, with exact rationals.

    The all-parameter binomial identity for the full count has degree at most
    N=h+q1+q2 (or one when T=0), plus one per positive independent interval.
    Newton differences at the resulting determining nodes therefore recover
    the entire polynomial; this is not an inferred degree or sampled sign test.
    Trailing zero coefficients are removed, including all dimension drops.
    The separate positivity proof covers this exact admissible domain only.
    """
    intervals = _parameters(h, q1, q2, total, lower_cap, upper_cap, height, interval_lengths)
    bound = (h + q1 + q2 if total else int(height > 0)) + sum(length > 0 for length in intervals)
    differences = [Fraction(strip_count(h, q1, q2, total, lower_cap, upper_cap, height, t,
                                       interval_lengths=intervals)) for t in range(bound + 1)]
    coefficients = [Fraction(0)] * (bound + 1)
    basis = [Fraction(1)]
    for k in range(bound + 1):
        for power, value in enumerate(basis):
            coefficients[power] += differences[0] * value
        differences = [right - left for left, right in zip(differences, differences[1:])]
        if k != bound:
            following = [Fraction(0)] * (len(basis) + 1)
            for power, value in enumerate(basis):
                following[power] -= value * k / (k + 1)
                following[power + 1] += value / (k + 1)
            basis = following
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)
