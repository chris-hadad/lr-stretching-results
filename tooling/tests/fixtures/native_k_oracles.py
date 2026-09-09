"""Exact selected native Session K oracle functions; original function bodies retained."""
from __future__ import annotations
from functools import lru_cache
from itertools import product

def table_count(rows: tuple[int, ...], cols: tuple[int, ...]) -> int:
    """#{non-negative integer p × q tables with row sums ``rows`` and column sums ``cols``}.

    Args:
        rows: The row margins.
        cols: The column margins.

    Returns:
        The exact count, which is 0 when the two margins do not sum to the same total — no table
        exists there, and the recursion is not entered.
    """
    if sum(rows) != sum(cols):
        return 0

    @lru_cache(maxsize=None)
    def rec(i: int, residual: tuple[int, ...]) -> int:
        if i == len(rows):
            return 1 if all(v == 0 for v in residual) else 0
        target = rows[i]
        total = 0

        def fill(j: int, left: int, res: list[int]) -> int:
            if j == len(residual) - 1:
                if left <= res[j]:
                    res[j] -= left
                    v = rec(i + 1, tuple(res))
                    res[j] += left
                    return v
                return 0
            acc = 0
            for take in range(min(left, res[j]) + 1):
                res[j] -= take
                acc += fill(j + 1, left - take, res)
                res[j] += take
            return acc

        total = fill(0, target, list(residual))
        return total

    return rec(0, tuple(cols))

def quotient_count_enumerated(t: int) -> int:
    """#lattice points of the projection of T(t·r, t·c), r = c = (2, 2, 1, 1), along the block direction.

    A class is determined by the twelve exterior entries (rows 3–4 × every column; rows 1–2 ×
    columns 3–4): the distinguished 2 × 2 block then has fixed margins and completes non-negatively
    iff every remaining margin is ≥ 0, which the exterior bounds (rows 3–4 sum to t; columns 3–4 sum
    to t) force.  So the count is: over compositions of t into four parts for row 3 and for row 4,
    the number of ways to split each of columns 3 and 4's remaining sum (t − Z-column) into rows 1–2.

    Args:
        t: The dilation factor.

    Returns:
        The exact number of lattice points of the projection at that ``t``.
    """
    total = 0
    for x3 in compositions(t, 4):
        for x4 in compositions(t, 4):
            rem3 = t - x3[2] - x4[2]
            rem4 = t - x3[3] - x4[3]
            if rem3 < 0 or rem4 < 0:
                continue
            total += (rem3 + 1) * (rem4 + 1)
    return total

def quotient_count_closed_form(t: int) -> int:
    """VERIFICATION.md §5: Σ_Z Π_i (t·a_i − row_i(Z) + 1) Π_j (t·b_j − col_j(Z) + 1), a = b = (1, 1).

    Args:
        t: The dilation factor.

    Returns:
        The campaign's stated closed form at that ``t``, computed here so it is checked against
        :func:`quotient_count_enumerated` rather than assumed.
    """
    a = (1, 1)
    b = (1, 1)
    total = 0
    for z in product(range(t + 1), repeat=4):
        Z = ((z[0], z[1]), (z[2], z[3]))
        rows = [sum(Z[i]) for i in range(2)]
        cols = [Z[0][j] + Z[1][j] for j in range(2)]
        if any(rows[i] > t * a[i] for i in range(2)) or any(cols[j] > t * b[j] for j in range(2)):
            continue
        term = 1
        for i in range(2):
            term *= t * a[i] - rows[i] + 1
        for j in range(2):
            term *= t * b[j] - cols[j] + 1
        total += term
    return total

def compositions(n: int, k: int) -> list[tuple[int, ...]]:
    """Every weak composition of ``n`` into ``k`` non-negative parts.

    Args:
        n: The total to distribute.
        k: The number of parts; must be at least 1, and ``k = 1`` is the single ``(n,)``.

    Returns:
        The compositions, each as a tuple of ``k`` parts.
    """
    if k == 1:
        return [(n,)]
    out = []
    for first in range(n + 1):
        for rest in compositions(n - first, k - 1):
            out.append((first, *rest))
    return out
