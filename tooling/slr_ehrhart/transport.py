"""Exact transportation counts, LR tail lift, and primitive-segment quotient.

Pure Python integer arithmetic; no engine, global cache or process ownership.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator, Sequence
from itertools import groupby
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
    """Yield positive sorted residuals and their exact labeled transition weights.

    The input residual is sorted. Within each equal-cap group, enumerate only
    nondecreasing allocations and restore their multinomial multiplicities.
    Different groups can still produce the same sorted residual; add all such
    contributions. For capped rows the weight also includes row slack plus one.
    """
    n = len(residual)
    tail = [0] * (n + 1)
    for j in range(n - 1, -1, -1):
        tail[j] = tail[j + 1] + residual[j]
    group_position = [0] * n
    group_remaining = [0] * n
    start = 0
    while start < n:
        end = start + 1
        while end < n and residual[end] == residual[start]:
            end += 1
        for j in range(start, end):
            group_position[j] = j - start + 1
            group_remaining[j] = end - j
        start = end
    chosen = [0] * n
    combined: dict[tuple[int, ...], int] = defaultdict(int)

    def visit(j: int, remaining: int, multiplicity: int, run_length: int) -> None:
        if j == n:
            if not exact or remaining == 0:
                following = tuple(sorted(residual[i] - chosen[i] for i in range(n)
                                         if residual[i] != chosen[i]))
                combined[following] += multiplicity * (1 if exact else remaining + 1)
            return
        same_group = j > 0 and residual[j] == residual[j - 1]
        minimum = chosen[j - 1] if same_group else 0
        low = max(minimum, remaining - tail[j + 1]) if exact else minimum
        high = min(residual[j], remaining // group_remaining[j])
        for used in range(low, high + 1):
            next_run = run_length + 1 if same_group and used == chosen[j - 1] else 1
            # Every prefix has integral multinomial multiplicity. At the end
            # of a group it equals group_size! / product(value_frequency!).
            next_multiplicity = multiplicity * group_position[j] // next_run
            chosen[j] = used
            visit(j + 1, remaining - used, next_multiplicity, next_run)

    visit(0, cap, 1, 0)
    yield from combined.items()


def _bounded_composition_dp(caps: tuple[int, ...], target: int) -> int:
    """Extract a bounded-composition coefficient with sliding prefix sums."""
    coefficients = [1]
    for cap in caps:
        limit = min(target, len(coefficients) - 1 + cap)
        following = []
        window = 0
        for degree in range(limit + 1):
            if degree < len(coefficients):
                window += coefficients[degree]
            expired = degree - cap - 1
            if 0 <= expired < len(coefficients):
                window -= coefficients[expired]
            following.append(window)
        coefficients = following
    return coefficients[target]


def _bounded_composition_inclusion(
    target: int, size: int, groups: tuple[tuple[int, int], ...],
) -> int:
    """Grouped inclusion-exclusion for product_j(1+...+z**caps[j])."""
    choices = [tuple((k * (cap + 1), (-1) ** k * comb(multiplicity, k))
                     for k in range(min(multiplicity, target // (cap + 1)) + 1))
               for cap, multiplicity in groups]

    def visit(j: int, remaining: int, weight: int) -> int:
        if j == len(choices):
            return weight * comb(remaining + size - 1, size - 1)
        result = 0
        for shift, coefficient in choices[j]:
            if shift > remaining:
                break
            result += visit(j + 1, remaining - shift, weight * coefficient)
        return result

    return visit(0, target, 1)


def _bounded_composition_count(caps: tuple[int, ...], target: int) -> int:
    """Count one row in a two-row table, choosing exact coefficient algorithms.

    Complementation halves the target range. Prefix DP has at most two integer
    additions per coefficient update. Grouped inclusion-exclusion is chosen
    when its conservative branch/term work estimate is no larger. A binomial
    evaluation is one estimate unit, not a constant-bit-cost or timing claim.
    """
    total = sum(caps)
    if target < 0 or target > total:
        return 0
    target = min(target, total - target)
    if target == 0:
        return 1
    caps = tuple(sorted(cap for cap in caps if cap))
    if len(caps) == 1:
        return 1
    if caps[0] >= target:
        return comb(target + len(caps) - 1, len(caps) - 1)
    groups = tuple((cap, len(tuple(group))) for cap, group in groupby(caps)
                   if cap < target)
    prefix = 0
    dp_work = 0
    for cap in caps:
        prefix += cap
        dp_work += 2 * (min(target, prefix) + 1)
    # Each group contributes at most K+1 choices. Summed prefix products
    # bound the recursion tree even before pruning by accumulated shift.
    nodes = terms = 1
    choice_work = 0
    for cap, multiplicity in groups:
        width = min(multiplicity, target // (cap + 1)) + 1
        terms *= width
        nodes += terms
        choice_work += width
    inclusion_work = 3 * nodes + 5 * terms + 5 * choice_work
    if inclusion_work <= dp_work:
        return _bounded_composition_inclusion(target, len(caps), groups)
    return _bounded_composition_dp(caps, target)


def transport_count(row_margins: Sequence[int], column_margins: Sequence[int]) -> int:
    """Count nonnegative integer tables with balanced labeled margins exactly.

    Nonnegative exact Python ints only; invalid inputs raise ValueError. Empty
    balanced vectors and all-zero margins describe one (possibly empty) table.
    Equal-cap allocation orbits carry exact labeled multiplicities. The final
    two rows use a bounded-composition coefficient, with exact prefix DP or
    grouped inclusion-exclusion selected by explicit work bounds.
    Runtime is combinatorial in the margins; no variable-rank efficiency claim.
    """
    rows, columns = _margins(row_margins, column_margins)
    rows = tuple(value for value in rows if value)
    columns = tuple(value for value in columns if value)
    if not rows:
        return 1
    if len(rows) == 1 or len(columns) == 1:
        return 1
    if len(rows) == 2:
        return _bounded_composition_count(columns, rows[0])
    if len(columns) == 2:
        return _bounded_composition_count(rows, columns[0])
    # Residual states live on the side with the smaller elementary box bound.
    if prod(value + 1 for value in rows) < prod(value + 1 for value in columns):
        rows, columns = columns, rows
    rows = tuple(sorted(rows))
    states: dict[tuple[int, ...], int] = {tuple(sorted(columns)): 1}
    for row in rows[:-2]:
        following: dict[tuple[int, ...], int] = defaultdict(int)
        for residual, count in states.items():
            for next_residual, weight in _row_residuals(residual, row, exact=True):
                following[next_residual] += count * weight
        states = following
    return sum(count * _bounded_composition_count(residual, rows[-2])
               for residual, count in states.items())


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


def _star_quotient_dp(central: int, leaves: tuple[int, ...]) -> int:
    """Convolve truncated linear kernels using prefix sums and first moments."""
    coefficients = [1]
    for cap in leaves:
        limit = min(central, len(coefficients) - 1 + cap)
        following = []
        window_sum = window_moment = 0
        for degree in range(limit + 1):
            if degree < len(coefficients):
                window_sum += coefficients[degree]
                window_moment += degree * coefficients[degree]
            expired = degree - cap - 1
            if 0 <= expired < len(coefficients):
                window_sum -= coefficients[expired]
                window_moment -= expired * coefficients[expired]
            following.append((cap + 1 - degree) * window_sum + window_moment)
        coefficients = following
    return sum((central - degree + 1) * coefficient
               for degree, coefficient in enumerate(coefficients))


def _star_quotient_numerator(central: int, leaves: tuple[int, ...]) -> int:
    """Extract the star coefficient from a product of three-term numerators.

    The cap-b kernel is ((b+1)-(b+2)*z+z**(b+2))/(1-z)**2.
    Central slack supplies a further (1-z)**-2. The resulting expansion has
    at most 3**len(leaves) terms and allocates no array indexed by a cap.
    """
    denominator_degree = 2 * len(leaves) + 1

    def visit(j: int, remaining: int, weight: int) -> int:
        if j == len(leaves):
            return weight * comb(remaining + denominator_degree, denominator_degree)
        cap = leaves[j]
        result = visit(j + 1, remaining, weight * (cap + 1))
        if remaining >= 1:
            result -= visit(j + 1, remaining - 1, weight * (cap + 2))
        if remaining >= cap + 2:
            result += visit(j + 1, remaining - cap - 2, weight)
        return result

    return visit(0, central, 1)


def _star_quotient_count(central: int, leaves: tuple[int, ...]) -> int:
    """Close one weighted row exactly, preserving the A03 formula cones first.

    Active leaves are positive; empty leaves give central+1. Mixed caps use
    either a three-term numerator expansion or O(q*central) prefix/moment DP,
    selected by explicit arithmetic-work estimates. Integer/combination cost
    still depends on bit size, and no polynomial variable-rank bound is claimed.
    """
    total = sum(leaves)
    if central >= total:
        numerator = (3 + 3 * central - total) * prod(comb(cap + 2, 2) for cap in leaves)
        value, remainder = divmod(numerator, 3)
        if remainder:
            raise ArithmeticError("the redundant-row star formula must be integral")
        return value
    b = len(leaves)
    if all(cap >= central for cap in leaves):
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
    prefix = 0
    dp_work = 0
    nodes = terms = 1
    for cap in leaves:
        prefix += cap
        dp_work += 10 * (min(central, prefix) + 1)
        terms *= 3 if cap + 2 <= central else 2
        nodes += terms
    dp_work += 4 * (min(central, prefix) + 1)
    numerator_work = 5 * nodes + 3 * terms
    if numerator_work <= dp_work:
        return _star_quotient_numerator(central, leaves)
    return _star_quotient_dp(central, leaves)


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
    does not certify that premise. Equal-cap allocation orbits carry their
    exact labeled multiplicities and row-slack weights before aggregation by
    sorted residual. The final row closes as a scalar star count, including
    all remaining column-slack weights. The star retains both redundant-cap
    formula cones, then chooses a numerator expansion or prefix/moment DP by
    explicit work estimates. Unequal caps are supported, with per-call state
    only; general instances can still be expensive.
    """
    rows = _integers(exterior_rows, "exterior_rows")
    columns = _integers(exterior_columns, "exterior_columns")
    if type(t) is not int or t < 0:
        raise ValueError("t must be a nonnegative exact integer")
    rows = tuple(t * value for value in rows if t * value)
    columns = tuple(t * value for value in columns if t * value)
    if not rows or not columns:
        return prod(value + 1 for value in rows + columns)
    if len(rows) == 1:
        return _star_quotient_count(rows[0], columns)
    if len(columns) == 1:
        return _star_quotient_count(columns[0], rows)
    if prod(value + 1 for value in rows) < prod(value + 1 for value in columns):
        rows, columns = columns, rows
    rows = tuple(sorted(rows))
    states: dict[tuple[int, ...], int] = {tuple(sorted(columns)): 1}
    for row in rows[:-1]:
        following: dict[tuple[int, ...], int] = defaultdict(int)
        for residual, count in states.items():
            for next_residual, weight in _row_residuals(residual, row, exact=False):
                following[next_residual] += count * weight
        states = following
    return sum(count * _star_quotient_count(rows[-1], residual)
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
