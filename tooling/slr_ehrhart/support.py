"""Conditional monomial support from exact Minkowski-summand directions.

The caller must supply complete direction-spanning sets for the summands P_i,
not sampled directions. On a valid closed common-type cone where
H(sum(s_i r_i)) = sum(s_i P_i) and the lattice count is a polynomial E(s),
every exponent alpha in E obeys

    sum(alpha[i] for i in S) <= dim(sum(P_i for i in S)).

This module computes that necessary support condition only. It neither checks
those hypotheses nor evaluates LR coefficients, proves coefficient positivity,
or asserts that an allowed monomial actually occurs.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from math import comb
import re


_RATIONAL_STRING = re.compile(r"[+-]?[0-9]+(?:/[0-9]+)?\Z")


@dataclass(frozen=True)
class SupportPlan:
    """An exact rank table and the exponents permitted by its subset caps.

    ``active_indices`` maps the nonpoint variables to their original input
    indices. ``rank_table[mask]`` is the span rank of the active direction sets
    whose positions in ``active_indices`` have bits set in ``mask``; index zero
    is the empty subset. Point summands do not enlarge the rank table.
    ``allowed_support`` contains exponent tuples ordered by total degree, then
    lexicographically, in the original summand order with zero slots for points.
    ``degree=None`` denotes the full polynomial support across all degrees.
    """

    degree: int | None
    summand_count: int
    ambient_dimension: int
    active_indices: tuple[int, ...]
    rank_table: tuple[int, ...]
    allowed_support: tuple[tuple[int, ...], ...]


def _integer(value, name, minimum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer (not bool or float)")
    if value < minimum:
        qualifier = "positive" if minimum == 1 else "nonnegative"
        raise ValueError(f"{name} must be {qualifier}")
    return value


def _sequence(value, name):
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    return value


def _rational(value):
    if isinstance(value, bool):
        raise TypeError("direction entries must be exact rationals, not bool")
    if isinstance(value, (int, Fraction)):
        return Fraction(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not _RATIONAL_STRING.fullmatch(stripped):
            raise ValueError("rational strings must be integers or numerator/denominator")
        try:
            return Fraction(stripped)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("invalid rational string") from exc
    raise TypeError("direction entries must be int, Fraction, or rational strings")


def _span_rank(vectors, dimension):
    """Compute row rank by exact Fraction elimination without external tools."""
    basis = {}
    for vector in vectors:
        row = list(vector)
        for pivot in range(dimension):
            coefficient = row[pivot]
            if not coefficient:
                continue
            if pivot in basis:
                pivot_row = basis[pivot]
                for column in range(pivot, dimension):
                    row[column] -= coefficient * pivot_row[column]
            else:
                basis[pivot] = [entry / coefficient for entry in row]
                break
        if len(basis) == dimension:
            break
    return len(basis)


def _compositions(total, length):
    if length == 0:
        if total == 0:
            yield ()
    elif length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in _compositions(total - first, length - 1):
                yield (first,) + rest


def plan_support(summand_directions, degree=None, *, max_subsets=4096, max_candidates=100000):
    """Return the monomial support permitted by all subset ranks.

    ``summand_directions[i]`` is a finite sequence of vectors spanning the
    complete direction space of P_i. All vectors share an ambient dimension;
    empty direction sets and zero vectors represent point summands. If there
    are no vectors, the inferred ambient dimension is zero. The caller is
    responsible for completeness of the spans and the module's mathematical
    hypotheses; this API cannot infer either from the vectors.

    Entries accept int (excluding bool), Fraction, and strings containing a
    signed integer or signed numerator/positive denominator, with optional
    surrounding whitespace. Decimal/exponent strings, floats, and ragged
    vectors are rejected. ``degree`` is a nonnegative integer for homogeneous
    support, or None (the default) for the full support over degrees zero
    through the full span rank. The latter is a finite coordinatewise lower
    set; it can support a later polynomial interpolation step, but this helper
    performs no evaluations or interpolation.

    Both work caps must be positive integers, excluding bool and float.
    ``max_subsets`` limits the rank table of nonpoint variables, including the
    empty subset. All vectors are validated and singleton ranks computed
    before this cap is checked. ``max_candidates`` limits the weak compositions
    of nonpoint variables *before* subset filtering, combined across all
    degrees in full-support mode. Point variables are omitted during subset
    ranking and enumeration, and restored as zero slots in allowed_support.
    A requested degree above the full span rank returns empty support without
    enumeration. Exceeding a cap raises ValueError instead of returning partial
    results. These caps do not bound input vector storage or rational integer
    bit lengths; this helper is meant for small numbers of active summands with
    modest exact direction sets.
    """
    if degree is not None:
        degree = _integer(degree, "degree", 0)
    max_subsets = _integer(max_subsets, "max_subsets", 1)
    max_candidates = _integer(max_candidates, "max_candidates", 1)
    summands = _sequence(summand_directions, "summand_directions")
    count = len(summands)
    directions = []
    dimension = None
    for summand in summands:
        converted = []
        for vector in _sequence(summand, "summand directions"):
            vector = _sequence(vector, "direction vector")
            if dimension is None:
                dimension = len(vector)
            elif len(vector) != dimension:
                raise ValueError("direction vectors must share an ambient dimension")
            converted.append(tuple(_rational(entry) for entry in vector))
        directions.append(tuple(converted))
    if dimension is None:
        dimension = 0

    singleton_ranks = tuple(_span_rank(summand, dimension) for summand in directions)
    active = tuple(index for index, rank in enumerate(singleton_ranks) if rank)
    # Compare logarithms first so an over-cap input does not build a huge int.
    if len(active) >= max_subsets.bit_length():
        raise ValueError("subset rank table exceeds max_subsets")
    subset_count = 1 << len(active)
    ranks = [0]
    for mask in range(1, subset_count):
        if mask & (mask - 1) == 0:
            ranks.append(singleton_ranks[active[mask.bit_length() - 1]])
            continue
        vectors = (
            vector
            for position, index in enumerate(active)
            if mask & (1 << position)
            for vector in directions[index]
        )
        ranks.append(_span_rank(vectors, dimension))
    rank_table = tuple(ranks)

    def result(support):
        return SupportPlan(degree, count, dimension, active, rank_table, tuple(support))

    full_rank = rank_table[-1]
    if degree is not None and degree > full_rank:
        return result(())
    if degree is None:
        degrees = range(full_rank + 1)
        candidate_count = comb(full_rank + len(active), len(active))
    else:
        degrees = (degree,)
        candidate_count = comb(degree + len(active) - 1, len(active) - 1) if active else 1
    if candidate_count > max_candidates:
        raise ValueError("degree compositions exceed max_candidates")

    support = []
    for current_degree in degrees:
        for values in _compositions(current_degree, len(active)):
            if all(
                sum(value for position, value in enumerate(values) if mask & (1 << position))
                <= rank_table[mask]
                for mask in range(1, subset_count)
            ):
                exponents = [0] * count
                for index, value in zip(active, values):
                    exponents[index] = value
                support.append(tuple(exponents))
    return result(support)
