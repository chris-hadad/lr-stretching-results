"""Exact selected hive construction functions; see FORCING-SOURCE-MAP.json."""
from __future__ import annotations

def interior_points(n: int) -> list[tuple[int, int]]:
    """Return the interior hive coordinates for rank ``n``, in the canonical row order.

    Args:
        n: Rank (maximum partition length).

    Returns:
        The ``m = (n-1)(n-2)/2`` points ``(i, j)`` with ``i, j >= 1`` and ``i + j <= n - 1``.
    """
    return [(i, j) for i in range(1, n) for j in range(1, n) if i + j <= n - 1]


def rhombus_terms(n: int) -> list[list[tuple[tuple[int, int], int]]]:
    """Return the signed vertex terms of every rhombus inequality, in the canonical row order.

    Each element is a list of ``((i, j), sign)`` pairs; the inequality is
    ``sum(sign * h(i, j)) >= 0``, i.e. the two obtuse vertices (sign ``+1``) dominate the two acute
    vertices (sign ``-1``).  The order is fixed for a given ``n``, which is what lets
    :func:`hive_system` and :func:`hive_linear_system` be compared row by row.

    Args:
        n: Rank (maximum partition length).

    Returns:
        A list of ``3*n*(n-1)/2`` term lists.

    Raises:
        RuntimeError: If the generated row count differs from ``3*n*(n-1)/2``.
    """
    rows: list[list[tuple[tuple[int, int], int]]] = []
    for i in range(0, n):
        for j in range(0, n):
            if i + j > n - 1:
                continue
            # Up triangle U = (i,j), (i+1,j), (i,j+1); one rhombus per adjacent down triangle.
            if i + j + 2 <= n:  # down triangle (i+1,j), (i,j+1), (i+1,j+1)
                rows.append([((i + 1, j), 1), ((i, j + 1), 1), ((i, j), -1), ((i + 1, j + 1), -1)])
            if j >= 1:  # down triangle (i+1,j-1), (i,j), (i+1,j)
                rows.append([((i, j), 1), ((i + 1, j), 1), ((i, j + 1), -1), ((i + 1, j - 1), -1)])
            if i >= 1:  # down triangle (i,j), (i-1,j+1), (i,j+1)
                rows.append([((i, j), 1), ((i, j + 1), 1), ((i + 1, j), -1), ((i - 1, j + 1), -1)])
    expected = 3 * n * (n - 1) // 2
    if len(rows) != expected:
        raise RuntimeError(f"rhombus row count {len(rows)} != 3n(n-1)/2 = {expected} for n = {n}")
    return rows


def hive_linear_system(n: int) -> tuple[list[list[int]], list[list[int]], int]:
    """Return the rank-``n`` hive system as exact matrices ``(A, B)`` independent of the boundary.

    Every rhombus row reads ``A_r . x + B_r . b >= 0`` for the concatenated padded boundary vector
    ``b = (lambda, mu, nu)`` of length ``3n``.  This is a second, independently written derivation
    of the same system as :func:`hive_system`; :func:`cross_validate_linear_system` checks the two
    against each other row by row.

    Args:
        n: Rank (maximum partition length), ``n >= 1``.

    Returns:
        ``(A, B, m)`` with ``A`` a ``3n(n-1)/2`` by ``m`` integer matrix, ``B`` a
        ``3n(n-1)/2`` by ``3n`` integer matrix, and ``m = (n-1)(n-2)/2``.

    Raises:
        ValueError: If ``n < 1``.
        RuntimeError: If a rhombus references a point that is neither interior nor on a side.
    """
    if n < 1:
        raise ValueError(f"rank must be at least 1 (got {n})")
    interior = interior_points(n)
    idx = {p: k for k, p in enumerate(interior)}
    m = len(interior)

    def boundary_vec(point: tuple[int, int]) -> list[int]:
        i, j = point
        v = [0] * (3 * n)
        if j == 0:  # side 1: h(i,0) = mu_1 + ... + mu_i
            for k in range(i):
                v[n + k] += 1
        elif i == 0:  # side 3: h(0,j) = lambda_1 + ... + lambda_j
            for k in range(j):
                v[k] += 1
        elif i + j == n:  # side 2: h(n-k,k) = |mu| + nu_1 + ... + nu_k with k = j
            for k in range(n):
                v[n + k] += 1
            for k in range(j):
                v[2 * n + k] += 1
        else:
            raise RuntimeError(f"point {point} is neither interior nor on a hive side (n = {n})")
        return v

    a_rows: list[list[int]] = []
    b_rows: list[list[int]] = []
    for terms in rhombus_terms(n):
        a = [0] * m
        beta = [0] * (3 * n)
        for p, sgn in terms:
            if p in idx:
                a[idx[p]] += sgn
            else:
                bv = boundary_vec(p)
                for k in range(3 * n):
                    beta[k] += sgn * bv[k]
        a_rows.append(a)
        b_rows.append(beta)
    return a_rows, b_rows, m
