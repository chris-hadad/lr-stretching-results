"""Exact graded matrix-invariant counts and their entire-family LR construction.

Adapted from the root-authored weighted-transport Weyl counter and A08/A09
proofs. Standard library only; all memoization is local to one count call.
"""

from __future__ import annotations

from collections import Counter
from functools import cache, lru_cache
from itertools import permutations
from math import comb, prod
from typing import Any

__all__ = ["MatrixCountLimitError", "matrix_invariant_count", "matrix_invariants_to_lr"]


class MatrixCountLimitError(RuntimeError):
    """An explicit work ceiling stopped the count; no partial value is valid.

    ``statistics`` is a copied snapshot of admitted work. Transitions include
    Weyl permutations, newly generated equal-cap allocation orbits and consumed
    residual terms, including schedule-cache hits; states count canonical DP
    cache misses. Represented labeled allocations sum generated orbit
    multiplicities and are recorded separately from consumed residual terms. This exception
    has no numerical count attribute.
    """

    def __init__(self, resource: str, limit: int, statistics: dict[str, int]) -> None:
        self.resource = resource
        self.limit = limit
        self.statistics = dict(statistics)
        super().__init__(f"matrix invariant count incomplete: {resource} limit {limit} exhausted")


def _integer(value: int, name: str, minimum: int) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an exact integer >= {minimum}")
    return value


def _canonical_table_state(
    rows: tuple[int, ...], columns: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Canonicalize transposition of already sorted, zero-free margin tuples.

    Keep the longer tuple on the row side, so elimination allocates over the
    shorter side. Equal lengths put the lexicographically smaller tuple first.
    """
    if len(rows) < len(columns) or (len(rows) == len(columns) and rows > columns):
        return columns, rows
    return rows, columns


def matrix_invariant_count(
    n: int, m: int, t: int, *,
    max_states: int | None = None, max_transitions: int | None = None,
) -> int:
    """Return dim R(n,m)_(n*t) for m n-by-n matrices under SL_n x SL_n.

    Exact Python ints n,m>=1 and t>=0 are required; bools and numeric coercions
    are rejected with ValueError. Optional ceilings are exact nonnegative ints.
    Zero forbids the corresponding counted work; elementary formulas use no
    DP states or transitions. No cross-call cache or wall-clock limit is used.

    The proved scalar identity P(n,m;t)=P(t,m;n), for n,t>=1, selects the
    smaller Weyl rank. It preserves this one count and entry degree n*t, not
    the entire graded ring or the constructor's original matrix size.

    A transition is an admitted Weyl permutation, a newly generated equal-cap
    allocation orbit, or a consumed residual term (also on schedule-cache hits).
    Labeled multiplicities of generated orbits are recorded separately. A state
    is a canonical DP cache miss, including forced terminal states. A per-call
    LRU holds at most 256 completed allocation schedules; it is not a byte cap.
    Exhaustion raises MatrixCountLimitError before admitting work beyond the
    ceiling, never returning zero or a partial signed sum. Limits do not bound
    integer bit complexity or wall time; use an external deadline for that.
    """
    n = _integer(n, "n", 1)
    m = _integer(m, "m", 1)
    t = _integer(t, "t", 0)
    for name, limit in (("max_states", max_states), ("max_transitions", max_transitions)):
        if limit is not None:
            _integer(limit, name, 0)
    if t == 0 or m == 1:
        return 1
    if m == 2:
        return comb(n + t, n)
    if t < n:
        n, t = t, n
    if n == 1:
        return comb(t + m - 1, m - 1)

    statistics = {"states": 0, "transitions": 0, "permutations": 0,
                  "allocation_orbits": 0, "represented_labeled_allocations": 0,
                  "residual_terms": 0, "schedule_cache_hits": 0,
                  "schedule_cache_misses": 0, "margin_profiles": 0}
    limits = {"states": max_states, "transitions": max_transitions}

    def charge(resource: str) -> None:
        limit = limits[resource]
        if limit is not None and statistics[resource] >= limit:
            raise MatrixCountLimitError(resource, limit, statistics)
        statistics[resource] += 1

    signs: Counter[tuple[int, ...]] = Counter()
    for sigma in permutations(range(n)):
        charge("transitions")
        statistics["permutations"] += 1
        margins = tuple(sorted(t + i - sigma[i] for i in range(n)))
        if margins[0] < 0:
            continue
        inversions = sum(sigma[i] > sigma[j] for i in range(n) for j in range(i + 1, n))
        signs[margins] += (-1) ** inversions
    profiles = [(margins, sign) for margins, sign in signs.items() if sign]
    statistics["margin_profiles"] = len(profiles)

    @cache
    def weight(entry: int) -> int:
        return comb(entry + m - 1, m - 1)

    def allocations(caps: tuple[int, ...], total: int):
        suffix = [0] * (len(caps) + 1)
        for j in range(len(caps) - 1, -1, -1):
            suffix[j] = suffix[j + 1] + caps[j]
        group_position = [0] * len(caps)
        group_remaining = [0] * len(caps)
        start = 0
        while start < len(caps):
            end = start + 1
            while end < len(caps) and caps[end] == caps[start]:
                end += 1
            for j in range(start, end):
                group_position[j] = j - start + 1
                group_remaining[j] = end - j
            start = end
        chosen = [0] * len(caps)

        def visit(j: int, left: int, row_weight: int, multiplicity: int, run_length: int):
            if j == len(caps):
                if left == 0:
                    charge("transitions")
                    statistics["allocation_orbits"] += 1
                    statistics["represented_labeled_allocations"] += multiplicity
                    residual = tuple(sorted(caps[i] - chosen[i] for i in range(len(caps))))
                    yield residual, row_weight * multiplicity
                return
            same_group = j > 0 and caps[j] == caps[j - 1]
            minimum = chosen[j - 1] if same_group else 0
            low = max(minimum, left - suffix[j + 1])
            # Remaining entries of this equal-cap group must be >= this one.
            high = min(caps[j], left // group_remaining[j])
            for used in range(low, high + 1):
                next_run = run_length + 1 if same_group and used == chosen[j - 1] else 1
                # Incremental multinomial update: at each completed group this
                # is group_size! / product(frequency!), times prior groups.
                next_multiplicity = multiplicity * group_position[j] // next_run
                chosen[j] = used
                yield from visit(j + 1, left - used, row_weight * weight(used),
                                 next_multiplicity, next_run)

        yield from visit(0, total, 1, 1, 0)

    @lru_cache(maxsize=256)
    def allocation_schedule(caps: tuple[int, ...], total: int):
        # m is fixed in this call. Each orbit is charged by allocations before
        # aggregation; exceptions never install a partial schedule in the LRU.
        statistics["schedule_cache_misses"] += 1
        combined: dict[tuple[int, ...], int] = {}
        for residual, row_weight in allocations(caps, total):
            positive = tuple(x for x in residual if x)
            combined[positive] = combined.get(positive, 0) + row_weight
        return tuple(combined.items())

    def tables(rows: tuple[int, ...], columns: tuple[int, ...]) -> int:
        # All entries are sorted and positive before the cache sees the state.
        return cached_tables(*_canonical_table_state(rows, columns))

    @cache
    def cached_tables(rows: tuple[int, ...], columns: tuple[int, ...]) -> int:
        charge("states")
        if sum(rows) != sum(columns):
            return 0
        if not rows:
            return int(not columns)
        if not columns:
            return 0
        if len(rows) == 1:
            return prod(weight(entry) for entry in columns)
        if len(columns) == 1:
            return prod(weight(entry) for entry in rows)
        misses = statistics["schedule_cache_misses"]
        schedule = allocation_schedule(columns, rows[0])
        if statistics["schedule_cache_misses"] == misses:
            statistics["schedule_cache_hits"] += 1
        answer = 0
        for residual, row_weight in schedule:
            # A cached schedule can still contain many terms: charge their
            # actual consumption, independently of schedule generation.
            charge("transitions")
            statistics["residual_terms"] += 1
            answer += row_weight * tables(rows[1:], residual)
        return answer

    answer = 0
    for left, (rows, coefficient) in enumerate(profiles):
        for right in range(left, len(profiles)):
            columns, column_coefficient = profiles[right]
            value = tables(tuple(x for x in rows if x), tuple(x for x in columns if x))
            answer += (1 if left == right else 2) * coefficient * column_coefficient * value
    if answer < 0:
        raise ArithmeticError("the complete matrix-invariant count cannot be negative")
    return answer


def matrix_invariants_to_lr(n: int, m: int) -> dict[str, Any]:
    """Construct the entire A08 LR family for original n>=1 and m>=2.

    With q=m-1, use the q*delta+e affine-E6 construction. Every integer
    stretch t>=0 has LR value dim R(n,m)_(n*t). The q=1 case uses the proved
    weight-zero square-edge contraction. No count-size/stretch swap is used.
    This constructor neither computes coefficients nor asserts negativity.
    Invalid inputs raise ValueError under the exact Python integer contract.
    """
    n = _integer(n, "n", 1)
    m = _integer(m, "m", 2)
    q = m - 1
    mu = [2 * q * q] * (q * n) + [q * q] * (q * n)
    lam = ([3 * q * q] * (q * n)
           + [2 * q * q + q] * ((q - 1) * n)
           + [q * q + 1] * (q * n)
           + [q * q] * n)
    return {
        "lambda": lam, "mu": mu, "nu": list(mu),
        "metadata": {
            "matrix_size": n,
            "matrix_count": m,
            "q": q,
            "ambient_rank": 3 * q * n,
            "entry_degree_per_stretch": n,
            "scope": "entire ordinary LR family: c^(t*lambda)_(t*mu,t*nu) = dim R(n,m)_(n*t)",
            "source_bounds": {"n_min": 1, "m_min": 2, "t_min": 0},
            "proof": "proofs/matrix-invariants.md",
            "dimension": None,
            "degree": None,
        },
    }
