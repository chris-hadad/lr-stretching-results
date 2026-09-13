"""Exact evaluation for the stated rank-eight family, 0 <= M <= S <= 2*M.

The data encode G(u, v), with u = 2*M - S and v = S - M. Dilation
evaluates G(u*t, v*t). The scientific certificate is identified in the data
module; this evaluator does not itself establish that certificate's LR scope.
"""

from fractions import Fraction

from ._rank8_clipped_data import DEGREE, DENOMINATOR, NUMERATOR_TERMS


def _nonnegative_integer(value: int, name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative Python integer")


def _parameters(M: int, S: int) -> tuple[int, int]:
    _nonnegative_integer(M, "M")
    _nonnegative_integer(S, "S")
    if not M <= S <= 2 * M:
        raise ValueError("rank8 clipped parameters must satisfy 0 <= M <= S <= 2*M")
    return 2 * M - S, S - M


def _powers(value: int) -> list[int]:
    result = [1]
    for _ in range(DEGREE):
        result.append(result[-1] * value)
    return result


def rank8_clipped_boundary(M: int, S: int) -> tuple[tuple[int, ...], ...]:
    """Return (lambda, mu, nu) as partition tuples for the admitted family.

    M and S must be exact Python integers satisfying 0 <= M <= S <= 2*M.
    The origin returns three empty partitions. Invalid inputs raise ValueError.
    """
    _parameters(M, S)
    if M == 0:
        return (), (), ()
    return (
        (50 * M - S, 46 * M, 36 * M, 32 * M, 23 * M + S, 19 * M, 9 * M, 5 * M),
        (27 * M, 23 * M, 19 * M, 15 * M, 13 * M, 9 * M, 5 * M, M),
        (25 * M, 22 * M, 19 * M, 14 * M, 12 * M, 9 * M, 6 * M, M),
    )


def rank8_clipped_count(M: int, S: int, t: int = 1) -> int:
    """Return the exact count at nonnegative integer dilation t.

    Validate M and S even when t is zero. Work uses 253 terms, independent
    of parameter magnitude; integer arithmetic cost grows with input size.
    Out-of-domain inputs raise ValueError and carry no count or sign judgment.
    """
    u, v = _parameters(M, S)
    _nonnegative_integer(t, "t")
    if t == 0 or M == 0:
        return 1
    up, vp = _powers(u * t), _powers(v * t)
    numerator = sum(coefficient * up[i] * vp[j] for i, j, coefficient in NUMERATOR_TERMS)
    result, remainder = divmod(numerator, DENOMINATOR)
    if remainder:
        raise ArithmeticError("rank8 clipped data evaluated to a nonintegral count")
    return result


def rank8_clipped_polynomial(M: int, S: int) -> tuple[Fraction, ...]:
    """Return exact ordinary coefficients in t, from constant term upward.

    Trim only trailing zeros. The origin returns (Fraction(1),); every other
    admitted parameter pair has positive coefficients through degree 21.
    Invalid inputs raise ValueError.
    """
    u, v = _parameters(M, S)
    up, vp = _powers(u), _powers(v)
    numerators = [0] * (DEGREE + 1)
    for i, j, coefficient in NUMERATOR_TERMS:
        numerators[i + j] += coefficient * up[i] * vp[j]
    while len(numerators) > 1 and numerators[-1] == 0:
        numerators.pop()
    return tuple(Fraction(value, DENOMINATOR) for value in numerators)
