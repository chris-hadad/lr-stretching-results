"""Knutson--Tao hive polytope: H-representation, Sage polyhedron, and the exact linear system.

Campaign convention: ``c^{lambda}_{mu,nu}`` with ``lambda`` the OUTER partition and
``|lambda| = |mu| + |nu|``.  ``P(t) = c^{t lambda}_{t mu, t nu} = #(t*H cap Z^m)`` where ``H`` is
the hive polytope in the ``m = (n-1)(n-2)/2`` interior coordinates, ``n`` the maximum length.

Hive coordinates are the entries ``h(i, j)`` for ``0 <= i, j`` and ``i + j <= n`` (a triangle with
corners ``(0,0)``, ``(n,0)``, ``(0,n)``).  The boundary is fixed by partial sums, walked so that
rhombus concavity forces weakly decreasing differences on every side::

    side 1  (0,0)->(n,0):  h(i,0)   = mu_1 + ... + mu_i
    side 2  (n,0)->(0,n):  h(n-k,k) = |mu| + nu_1 + ... + nu_k
    side 3  (0,0)->(0,n):  h(0,j)   = lambda_1 + ... + lambda_j

so the corner ``(0,n)`` is consistent exactly when ``|lambda| = |mu| + |nu|``.  The interior
entries are the free coordinates.  Rhombus inequalities: for every unit rhombus the sum at the two
obtuse vertices is at least the sum at the two acute vertices; there are three orientations and
``3*n*(n-1)/2`` rhombi in total.

``H(lambda, mu, nu)`` and ``H(lambda, nu, mu)`` are *different* polytopes with equal lattice-point
counts -- mu and nu occupy different sides of the triangle.  Canonicalising the unordered pair
{mu, nu} is an enumeration-layer concern (see :mod:`slr_ehrhart.census`), never a property of this
construction.

This module imports only the standard library at module load.  Sage is imported lazily inside
:func:`hive_polyhedron` and :func:`hive_dimension`, so the pure-combinatorial surface
(:func:`hive_system`, :func:`hive_linear_system`, the partition helpers) runs under any Python 3.11+
interpreter.
"""

from __future__ import annotations

import random
from typing import Any, Iterable, Sequence

__all__ = [
    "MAX_LEN",
    "MAX_PART",
    "parse_partition",
    "pad",
    "scale",
    "interior_points",
    "rhombus_terms",
    "hive_boundary",
    "hive_system",
    "hive_polyhedron",
    "hive_dimension",
    "hive_linear_system",
    "cross_validate_linear_system",
    "random_partition",
]

#: Largest part :func:`parse_partition` accepts.  The hive polytope's rhombus constants are partial
#: sums of the parts, so an unbounded part flows straight into polyhedral construction and lattice
#: point enumeration; the campaign's own ranges are three orders of magnitude below this ceiling.
MAX_PART = 10_000

#: Largest number of parts :func:`parse_partition` accepts.  The interior coordinate count grows as
#: ``(n-1)(n-2)/2`` in the rank ``n``, so length is the more expensive of the two bounds; the
#: campaign works at ranks 4-7.
MAX_LEN = 64


def parse_partition(text: str) -> list[int]:
    """Parse a comma-separated partition string into a weakly decreasing list of positive parts.

    Magnitude and length are bounded: a part may not exceed :data:`MAX_PART` (``10_000``) and a
    partition may not have more than :data:`MAX_LEN` (``64``) parts once trailing zeros are
    stripped.  Both ceilings are far above anything the campaign enumerates and exist so that a
    hostile or mistyped argument is refused at the parser rather than inside polyhedral
    construction.

    Args:
        text: Comma-separated non-negative integers, e.g. ``"5,4,3,2,1"``.  Spaces are ignored and
            an empty string denotes the empty partition.

    Returns:
        The parts with trailing zeros stripped.

    Raises:
        ValueError: If a field is not an integer, a part is negative, a part exceeds
            :data:`MAX_PART`, the sequence has more than :data:`MAX_LEN` parts, or the sequence is
            not weakly decreasing.
    """
    fields = [x for x in text.replace(" ", "").split(",") if x != ""]
    if len(fields) > MAX_LEN:
        raise ValueError(f"partition length {len(fields)} exceeds MAX_LEN = {MAX_LEN} in {text!r}")
    try:
        parts = [int(x) for x in fields]
    except ValueError as exc:
        raise ValueError(f"non-integer part in {text!r}: {exc}") from exc
    if any(p < 0 for p in parts):
        raise ValueError(f"negative part in {text!r}")
    oversized = [p for p in parts if p > MAX_PART]
    if oversized:
        raise ValueError(f"part {oversized[0]} exceeds MAX_PART = {MAX_PART} in {text!r}")
    while parts and parts[-1] == 0:
        parts.pop()
    if any(parts[i] < parts[i + 1] for i in range(len(parts) - 1)):
        raise ValueError(f"not weakly decreasing: {text!r}")
    return parts


def pad(partition: Sequence[int], n: int) -> list[int]:
    """Zero-pad a partition to length ``n`` (never truncates a longer partition).

    Args:
        partition: The parts to pad.
        n: Target length; a ``partition`` already at least this long is returned unchanged.

    Returns:
        A new list of length ``max(len(partition), n)``.
    """
    return list(partition) + [0] * (n - len(partition))


def scale(partition: Sequence[int], t: int) -> list[int]:
    """Return the componentwise ``t``-fold stretch of a partition.

    Args:
        partition: The parts to stretch.
        t: Stretch factor.

    Returns:
        A new list ``[t * x for x in partition]``.
    """
    return [t * x for x in partition]


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


def hive_boundary(lam: Sequence[int], mu: Sequence[int], nu: Sequence[int]) -> tuple[int, dict[tuple[int, int], int]]:
    """Return ``(n, boundary)`` mapping every boundary hive coordinate to its fixed value.

    Args:
        lam: Outer partition.
        mu: First inner partition.
        nu: Second inner partition.

    Returns:
        ``n`` (the rank) and a dict from boundary point to its integer value.

    Raises:
        ValueError: If ``|lambda| != |mu| + |nu|``, or if any input is not weakly decreasing or has
            a negative part.
        RuntimeError: If the corner ``(0, n)`` is set inconsistently by sides 2 and 3.  Given the
            size identity this cannot happen; the check is retained as a structural tripwire.
    """
    for name, p in (("lambda", lam), ("mu", mu), ("nu", nu)):
        if any(x < 0 for x in p):
            raise ValueError(f"{name} has a negative part: {list(p)}")
        if any(p[i] < p[i + 1] for i in range(len(p) - 1)):
            raise ValueError(f"{name} is not weakly decreasing: {list(p)}")
    n = max(len(lam), len(mu), len(nu), 1)
    lam_p, mu_p, nu_p = pad(lam, n), pad(mu, n), pad(nu, n)
    if sum(lam_p) != sum(mu_p) + sum(nu_p):
        raise ValueError(f"|lambda| must equal |mu| + |nu| (got {sum(lam_p)} vs {sum(mu_p)} + {sum(nu_p)})")
    bnd: dict[tuple[int, int], int] = {(0, 0): 0}
    s = 0
    for i in range(1, n + 1):
        s += mu_p[i - 1]
        bnd[(i, 0)] = s
    s = sum(mu_p)
    for k in range(1, n + 1):
        s += nu_p[k - 1]
        bnd[(n - k, k)] = s
    s = 0
    for j in range(1, n + 1):
        s += lam_p[j - 1]
        # (0,n) was already set by side 2; the two agree exactly when |lambda| = |mu| + |nu|.
        if (0, j) in bnd and bnd[(0, j)] != s:
            raise RuntimeError(f"hive corner inconsistency at (0,{j}): {bnd[(0, j)]} != {s}")
        bnd[(0, j)] = s
    return n, bnd


def hive_system(
    lam: Sequence[int], mu: Sequence[int], nu: Sequence[int]
) -> tuple[int, list[tuple[int, int]], list[list[int]]]:
    """Build the hive polytope's H-representation in Sage inequality form.

    Args:
        lam: Outer partition.
        mu: First inner partition.
        nu: Second inner partition.

    Returns:
        ``(n, interior, ieqs)`` where ``interior`` lists the free coordinates in index order and
        each row of ``ieqs`` is ``[b, a_1, ..., a_m]`` meaning ``b + a . x >= 0``.

    Raises:
        ValueError: Propagated from :func:`hive_boundary` on a malformed triple.
    """
    n, bnd = hive_boundary(lam, mu, nu)
    interior = interior_points(n)
    idx = {p: k for k, p in enumerate(interior)}
    m = len(interior)

    def row(terms: Iterable[tuple[tuple[int, int], int]]) -> list[int]:
        r = [0] * (m + 1)
        for p, sgn in terms:
            if p in idx:
                r[1 + idx[p]] += sgn
            else:
                # Every point a rhombus references lies in the closed triangle, so it is either
                # interior or on one of the three sides; bnd covers all three sides.
                r[0] += sgn * bnd[p]
        return r

    ieqs = [row(terms) for terms in rhombus_terms(n)]
    return n, interior, ieqs


def hive_polyhedron(
    lam: Sequence[int], mu: Sequence[int], nu: Sequence[int], backend: str = "ppl"
) -> tuple[Any | None, bool | None]:
    """Build the hive polytope as a Sage ``Polyhedron`` over ``QQ``.

    Args:
        lam: Outer partition.
        mu: First inner partition.
        nu: Second inner partition.
        backend: Sage polyhedron backend (``"ppl"``, ``"normaliz"``, ``"cdd"``, ...).

    Returns:
        ``(polyhedron, None)`` for ``n >= 3``.  For ``n <= 2`` the ambient space is
        zero-dimensional, so no polyhedron is built and ``(None, feasible)`` is returned with
        ``feasible`` the constant feasibility of the rhombus rows.

    Raises:
        ValueError: Propagated from :func:`hive_system` on a malformed triple.
    """
    n, interior, ieqs = hive_system(lam, mu, nu)
    if not interior:
        return None, all(r[0] >= 0 for r in ieqs)
    # Sage is a heavy import and this module must stay usable without it (see the module
    # docstring), so the import is deliberately inside the function.  Lint rule PLC0415
    # (import-outside-top-level) is expected to be configured off for this file rather than
    # suppressed inline.
    from sage.all import QQ, Polyhedron  # type: ignore

    return Polyhedron(ieqs=ieqs, base_ring=QQ, backend=backend), None


def hive_dimension(lam: Sequence[int], mu: Sequence[int], nu: Sequence[int], backend: str = "ppl") -> int:
    """Return the exact dimension of the hive polytope (``-1`` when it is empty).

    Args:
        lam: Outer partition.
        mu: First inner partition.
        nu: Second inner partition.
        backend: Sage polyhedron backend used for the computation.

    Returns:
        ``dim H``, with ``-1`` for an empty hive and ``0`` for the ``n <= 2`` feasible case.

    Raises:
        ValueError: Propagated from :func:`hive_system` on a malformed triple.
    """
    pol, feasible = hive_polyhedron(lam, mu, nu, backend=backend)
    if pol is None:
        return 0 if feasible else -1
    return int(pol.dim())


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


def cross_validate_linear_system(n: int, trials: int = 20, seed: int = 0, max_part: int = 9) -> int:
    """Check :func:`hive_linear_system` against :func:`hive_system` on random rank-``n`` triples.

    Args:
        n: Rank to check.
        trials: Number of random triples.
        seed: Seed for the deterministic random source.
        max_part: Maximum part size of the random inner partitions.

    Returns:
        The number of triples checked (equal to ``trials``).

    Raises:
        RuntimeError: On the first disagreement, naming the offending triple.
    """
    a_rows, b_rows, _m = hive_linear_system(n)
    rng = random.Random(seed)
    for _ in range(trials):
        mu = sorted((rng.randint(0, max_part) for _ in range(n)), reverse=True)
        nu = sorted((rng.randint(0, max_part) for _ in range(n)), reverse=True)
        lam = sorted((a + b for a, b in zip(mu, nu)), reverse=True)
        _n, _interior, rows = hive_system(lam, mu, nu)
        b_vec = lam + mu + nu
        for r, a_row, b_row in zip(rows, a_rows, b_rows):
            if r[1:] != a_row:
                raise RuntimeError(f"interior normals disagree at rank {n} for {(lam, mu, nu)}")
            constant = sum(x * y for x, y in zip(b_row, b_vec))
            if r[0] != constant:
                raise RuntimeError(f"row constants disagree at rank {n} for {(lam, mu, nu)}: {r[0]} != {constant}")
    return trials


def random_partition(rng: random.Random, max_len: int, max_size: int) -> list[int]:
    """Draw a random partition with at most ``max_len`` parts and size at most ``max_size``.

    The single canonical implementation for the package; the audit tree carried two importable
    functions of this name with different semantics (defect D16).

    Args:
        rng: Seeded random source.
        max_len: Maximum number of parts before trailing zeros are stripped.
        max_size: Maximum total size.

    Returns:
        A weakly decreasing list of positive parts (possibly empty).

    Raises:
        ValueError: If ``max_len`` is below 1 or ``max_size`` is negative.
    """
    if max_len < 1:
        raise ValueError(f"max_len must be at least 1 (got {max_len})")
    if max_size < 0:
        raise ValueError(f"max_size must be non-negative (got {max_size})")
    n = rng.randint(1, max_len)
    parts = sorted((rng.randint(0, max_size) for _ in range(n)), reverse=True)
    while sum(parts) > max_size:
        k = rng.randrange(n)
        if parts[k] > 0:
            parts[k] -= 1
            parts.sort(reverse=True)
    while parts and parts[-1] == 0:
        parts.pop()
    return parts
