"""Exact transportation counts, LR tail lift, and primitive-segment quotient.

Pure Python integer arithmetic; no engine, global cache or process ownership.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator, Sequence
from math import comb, prod
from typing import Any

from .constructions import skew_content_to_lr

__all__ = [
    "transport_to_lr", "transport_count", "minkowski_obstruction",
    "segment_quotient_count", "segment_quotient_geometry", "segment_quotient_evaluate",
]


def _integers(values: Sequence[int], name: str) -> tuple[int, ...]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes, bytearray)):
        raise ValueError(f"{name} must be a sequence of exact integers")
    result = tuple(values)
    if any(type(value) is not int for value in result):
        raise ValueError(f"{name} entries must be exact integers (not bool, fractions or strings)")
    if any(value < 0 for value in result):
        raise ValueError(f"{name} entries must be nonnegative")
    return result


def _margins(
    row_margins: Sequence[int], column_margins: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    rows = _integers(row_margins, "row_margins")
    columns = _integers(column_margins, "column_margins")
    if sum(rows) != sum(columns):
        raise ValueError("row and column margins must have equal totals")
    return rows, columns


def transport_to_lr(
    row_margins: Sequence[int], column_margins: Sequence[int],
) -> dict[str, Any]:
    """Lift the entire labeled transportation polytope to one ordinary LR triple.

    Vectors must be nonempty and balanced, with nonnegative exact Python ints.
    The column suffixes C and the ordered row content r give the existing lift
    ``skew_content_to_lr(C, C[1:], r)``. Original order and zero margins remain
    in metadata. Output partitions follow the existing trailing-zero trimming
    convention; use ``ambient_rank`` to restore the common hive chart before
    adding boundaries. Dimension and degree are not inferred, including when
    the total is zero. Raises ValueError for invalid inputs.
    """
    rows, columns = _margins(row_margins, column_margins)
    if not rows or not columns:
        raise ValueError("the transportation LR lift requires nonempty margin vectors")
    suffixes = [0] * len(columns)
    total = 0
    for j in range(len(columns) - 1, -1, -1):
        total += columns[j]
        suffixes[j] = total
    result = skew_content_to_lr(suffixes, suffixes[1:], rows)
    result["metadata"]["transportation"] = {
        "row_margins": list(rows),
        "column_margins": list(columns),
        "ambient_rank": len(rows) + len(columns) - 1,
        "domain": "entire nonnegative transportation polytope with these labeled margins",
        "lattice_preservation": "disconnected-row tableau identification, then integral skew-content lift",
    }
    return result


def _row_residuals(
    residual: tuple[int, ...], cap: int, *, exact: bool,
) -> Iterator[tuple[tuple[int, ...], int]]:
    """Yield each labeled next residual once, and the row allocation's total.

    Equal residual coordinates still occupy distinct positions in this walk.
    Callers may sort the yielded vector only if they add every multiplicity.
    """
    n = len(residual)
    tail = [0] * (n + 1)
    for j in range(n - 1, -1, -1):
        tail[j] = tail[j + 1] + residual[j]
    next_residual = [0] * n

    def visit(j: int, remaining: int) -> Iterator[tuple[tuple[int, ...], int]]:
        if j == n:
            if not exact or remaining == 0:
                yield tuple(next_residual), cap - remaining
            return
        low = max(0, remaining - tail[j + 1]) if exact else 0
        high = min(residual[j], remaining)
        for used in range(low, high + 1):
            next_residual[j] = residual[j] - used
            yield from visit(j + 1, remaining - used)

    yield from visit(0, cap)


def transport_count(row_margins: Sequence[int], column_margins: Sequence[int]) -> int:
    """Count nonnegative integer tables with balanced labeled margins exactly.

    Nonnegative exact Python ints only; invalid inputs raise ValueError. Empty
    balanced vectors and all-zero margins describe one (possibly empty) table.
    Internally permuted rows/columns reduce states, but tables are never counted
    up to permutation: every labeled row allocation contributes separately.
    Runtime is combinatorial in the margins; no variable-rank efficiency claim.
    """
    rows, columns = _margins(row_margins, column_margins)
    rows = tuple(value for value in rows if value)
    columns = tuple(value for value in columns if value)
    if not rows:
        return 1
    # Residual states live on the side with the smaller elementary box bound.
    if prod(value + 1 for value in rows) < prod(value + 1 for value in columns):
        rows, columns = columns, rows
    rows = tuple(sorted(rows))
    states: dict[tuple[int, ...], int] = {tuple(sorted(columns)): 1}
    for row in rows[:-1]:
        following: dict[tuple[int, ...], int] = defaultdict(int)
        for residual, count in states.items():
            for next_residual, _ in _row_residuals(residual, row, exact=True):
                following[tuple(sorted(next_residual))] += count
        states = following
    # Conservation forces the final labeled row, for every surviving state.
    return sum(states.values())


def _subset_pairs(
    first: tuple[int, ...], second: tuple[int, ...],
) -> Iterator[tuple[tuple[int, ...], int, int]]:
    """Enumerate paired subset sums in increasing original-label bitmask order."""
    for mask in range(1 << len(first)):
        indices = tuple(i for i in range(len(first)) if mask & (1 << i))
        yield indices, sum(first[i] for i in indices), sum(second[i] for i in indices)


def minkowski_obstruction(
    r: Sequence[int], c: Sequence[int], s: Sequence[int], d: Sequence[int],
) -> dict[str, Any] | None:
    """Return a strict opposite-sign cut, or None when every cut passes.

    The two balanced margin pairs must have the same labeled row and column
    lengths. For I,J set delta1=r(I)+c(J)-sum(r), and similarly delta2 for s,d.
    Return zero-based original-label ``row_indices`` and ``column_indices``,
    together with exact ``delta1`` and ``delta2``, when their product is <0.
    None certifies the all-subsets real transportation Minkowski criterion;
    this is not a criterion for arbitrary LR boundaries. Empty dimensions and
    zero margins are valid. Invalid inputs raise ValueError. The search visits
    up to 2**(p+q) cuts and is intended for bounded rank.
    """
    rows1, columns1 = _margins(r, c)
    rows2, columns2 = _margins(s, d)
    if len(rows1) != len(rows2) or len(columns1) != len(columns2):
        raise ValueError("both margin pairs must use the same labeled row and column lengths")
    total1, total2 = sum(rows1), sum(rows2)
    for indices_i, row1, row2 in _subset_pairs(rows1, rows2):
        for indices_j, col1, col2 in _subset_pairs(columns1, columns2):
            delta1, delta2 = row1 + col1 - total1, row2 + col2 - total2
            if delta1 * delta2 < 0:
                return {
                    "row_indices": list(indices_i), "column_indices": list(indices_j),
                    "delta1": delta1, "delta2": delta2,
                }
    return None


def _star_quotient_count(central: int, leaves: tuple[int, ...]) -> int | None:
    """Use the root's A03 exact formulas on their two redundant-cap cones.

    Arguments are positive active caps after dilation. None means that both
    kinds of cap can be active and the caller must use the general DP.
    Arithmetic is integral; the elementary-symmetric expansion uses O(b**2)
    arithmetic operations, with integer/combination cost depending on bit size.
    """
    total = sum(leaves)
    if central >= total:
        numerator = (3 + 3 * central - total) * prod(comb(cap + 2, 2) for cap in leaves)
        value, remainder = divmod(numerator, 3)
        if remainder:
            raise ArithmeticError("the redundant-row star formula must be integral")
        return value
    if any(cap < central for cap in leaves):
        return None
    b = len(leaves)
    elementary = [1] + [0] * b
    for i, cap in enumerate(leaves):
        excess = cap - central
        for j in range(i + 1, 0, -1):
            elementary[j] += excess * elementary[j - 1]
    result = 0
    for j, coefficient in enumerate(elementary):
        if coefficient:
            k = b - j
            contraction = sum(
                (-1) ** ell * comb(k, ell) * (central + 1) ** (k - ell)
                * comb(central + b + 1, b + ell + 1)
                for ell in range(min(k, central) + 1)
            )
            result += coefficient * contraction
    return result


def segment_quotient_count(
    exterior_rows: Sequence[int], exterior_columns: Sequence[int], t: int = 1,
) -> int:
    """Evaluate the primitive-segment exterior weighted count with exact ints.

    Sum over nonnegative integer matrices Z with row caps t*a and column caps
    t*b, with weight product_i(t*a_i-row_i(Z)+1) times
    product_j(t*b_j-column_j(Z)+1). Caps and t must be nonnegative exact Python
    ints. Empty exterior dimensions use empty products: q([],b,t)=prod(t*b+1),
    and q([],[],t)=1. Zero caps are valid and do not imply full dimension or
    degree. Invalid inputs raise ValueError.

    Interpretation as a whole-hive segment quotient requires the separate
    Minkowski gate on the base margins. This function has no base margins and
    does not certify that premise. Its recurrence weights each labeled row
    allocation before aggregating sorted residual column states. It supports
    unequal caps and uses per-call state only. A one-active-side star uses exact
    scalar formulas when either all leaf caps or the central cap are redundant;
    other cases retain the DP and can still be expensive.
    """
    rows = _integers(exterior_rows, "exterior_rows")
    columns = _integers(exterior_columns, "exterior_columns")
    if type(t) is not int or t < 0:
        raise ValueError("t must be a nonnegative exact integer")
    rows = tuple(t * value for value in rows if t * value)
    columns = tuple(t * value for value in columns if t * value)
    if not rows or not columns:
        return prod(value + 1 for value in rows + columns)
    star = (_star_quotient_count(rows[0], columns) if len(rows) == 1 else
            _star_quotient_count(columns[0], rows) if len(columns) == 1 else None)
    if star is not None:
        return star
    if prod(value + 1 for value in rows) < prod(value + 1 for value in columns):
        rows, columns = columns, rows
    states: dict[tuple[int, ...], int] = {tuple(sorted(columns)): 1}
    for row in sorted(rows):
        following: dict[tuple[int, ...], int] = defaultdict(int)
        for residual, count in states.items():
            for next_residual, used in _row_residuals(residual, row, exact=False):
                following[tuple(sorted(next_residual))] += count * (row - used + 1)
        states = following
    return sum(count * prod(value + 1 for value in residual)
               for residual, count in states.items())


def segment_quotient_geometry(
    exterior_rows: Sequence[int], exterior_columns: Sequence[int],
) -> dict[str, Any]:
    """Give exact intrinsic degree/codegree after deleting forced zero margins.

    The quotient has active variables z_ij,u_i,v_j with row sums z+u<=a
    and column sums z+v<=b. Its incidence matrix is totally unimodular.
    A small positive point gives degree p*q+p+q. Interior integer points
    require all variables >=1 and strict caps, so the first dilation is
    max(ceil((q+2)/a),ceil((p+2)/b)). Empty sides are interval products;
    both empty give degree zero and codegree one. No LR parent gate is inferred.
    """
    rows = _integers(exterior_rows, "exterior_rows")
    columns = _integers(exterior_columns, "exterior_columns")
    row_indices = [i for i, value in enumerate(rows) if value]
    column_indices = [j for j, value in enumerate(columns) if value]
    p, q = len(row_indices), len(column_indices)
    thresholds = [(q + 1 + rows[i]) // rows[i] for i in row_indices]
    thresholds += [(p + 1 + columns[j]) // columns[j] for j in column_indices]
    return {
        "dimension": p * q + p + q,
        "degree": p * q + p + q,
        "codegree": max([1] + thresholds),
        "active_row_indices": row_indices,
        "active_column_indices": column_indices,
        "lattice": "full integer lattice in active z,u,v coordinates",
    }


def segment_quotient_evaluate(
    exterior_rows: Sequence[int], exterior_columns: Sequence[int], t: int,
) -> int:
    """Evaluate the full quotient Ehrhart polynomial at any exact integer t.

    Nonnegative t uses segment_quotient_count. At t=-s<0, delete zero
    margins, subtract one from every active z,u,v coordinate, and use row
    caps s*a-(q+2), column caps s*b-(p+2), with sign (-1)^(p*q+p+q).
    A negative shifted cap gives zero. This is the complete nonuniform
    interior schedule; no reflection or parent-LR premise is assumed.
    """
    rows = _integers(exterior_rows, "exterior_rows")
    columns = _integers(exterior_columns, "exterior_columns")
    if type(t) is not int:
        raise ValueError("t must be an exact integer")
    if t >= 0:
        return segment_quotient_count(rows, columns, t)
    rows = tuple(value for value in rows if value)
    columns = tuple(value for value in columns if value)
    p, q = len(rows), len(columns)
    shifted_rows = tuple(-t * value - q - 2 for value in rows)
    shifted_columns = tuple(-t * value - p - 2 for value in columns)
    if any(value < 0 for value in shifted_rows + shifted_columns):
        return 0
    count = segment_quotient_count(shifted_rows, shifted_columns)
    return (-1) ** (p * q + p + q) * count
