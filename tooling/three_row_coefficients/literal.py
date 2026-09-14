"""Exact unsigned LR tableau counting for content of length at most three.

The algorithm enumerates sorted row patterns, enforces strict columns and the
lattice reading word, and aggregates equal dynamic-programming states. It has
no scientific imports, signed extraction, stretching normalization, or cache.
See LITERAL-METHOD.md for the proof, input contract, and precise work limit.
"""

from __future__ import annotations


class StateLimitExceeded(RuntimeError):
    """A complete count was refused; this exception contains no partial count."""

    def __init__(
        self, max_states: int, states_used: int, row_index: int, phase: str
    ) -> None:
        self.max_states = max_states
        self.states_used = states_used
        self.row_index = row_index
        self.phase = phase
        super().__init__(
            f"Literal LR work limit {max_states} exhausted after {states_used} "
            f"units, before {phase} in zero-based row {row_index}; "
            "no count was returned"
        )


def _partition(
    value: object, name: str, max_length: int | None = None
) -> tuple[int, ...]:
    """Validate before trimming only trailing zeros; never coerce entries."""
    if not isinstance(value, (tuple, list)):
        raise TypeError(f"{name} must be a tuple or list of built-in integers")
    if max_length is not None and len(value) > max_length:
        raise ValueError(f"{name} must have at most {max_length} entries")
    parts = tuple(value)
    if any(type(part) is not int for part in parts):
        raise TypeError(f"{name} entries must be built-in integers, excluding bool")
    if any(part < 0 for part in parts):
        raise ValueError(f"{name} entries must be nonnegative")
    if any(left < right for left, right in zip(parts, parts[1:])):
        raise ValueError(f"{name} must be a weakly decreasing partition")
    end = len(parts)
    while end and parts[end - 1] == 0:
        end -= 1
    return parts[:end]


def _strict_columns(
    upper_start: int,
    upper_counts: tuple[int, int, int],
    lower_start: int,
    lower_counts: tuple[int, int, int],
) -> bool:
    """Reject any overlap of upper value a and lower value b with a >= b."""
    upper_edges = [upper_start]
    lower_edges = [lower_start]
    for count in upper_counts:
        upper_edges.append(upper_edges[-1] + count)
    for count in lower_counts:
        lower_edges.append(lower_edges[-1] + count)
    for upper_symbol in range(3):
        for lower_symbol in range(upper_symbol + 1):
            left = max(upper_edges[upper_symbol], lower_edges[lower_symbol])
            right = min(upper_edges[upper_symbol + 1], lower_edges[lower_symbol + 1])
            if left < right:
                return False
    return True


def lr_count(
    outer: object, inner: object, content: object, max_states: int = 1_000_000
) -> int:
    """Return the exact LR count c_(inner,content)^outer or raise on refusal.

    Inputs are tuple/list partitions of built-in nonnegative integers. Outer
    and inner may have arbitrary length and trailing-zero padding. Content
    has at most three supplied entries. Inner must be contained in outer and
    the skew area must equal the content size. Invalid types raise TypeError;
    invalid values/shapes raise ValueError. Valid but infeasible data return 0.

    max_states is a positive built-in integer. One work unit is charged per
    frontier-state expansion and per candidate row pattern surviving the
    content and ballot bounds, including candidates rejected by columns.
    Exceeding the cap raises StateLimitExceeded without returning a count.
    Input validation, integer bit complexity, and wall time are not capped.
    """
    if type(max_states) is not int:
        raise TypeError("max_states must be a built-in integer, excluding bool")
    if max_states < 1:
        raise ValueError("max_states must be positive")
    outer_parts = _partition(outer, "outer")
    inner_parts = _partition(inner, "inner")
    content_parts = _partition(content, "content", max_length=3)
    if len(inner_parts) > len(outer_parts):
        raise ValueError("inner must be contained in outer")
    inner_parts += (0,) * (len(outer_parts) - len(inner_parts))
    if any(inside > outside for outside, inside in zip(outer_parts, inner_parts)):
        raise ValueError("inner must be contained in outer")
    target = content_parts + (0,) * (3 - len(content_parts))
    if sum(outer_parts) - sum(inner_parts) != sum(target):
        raise ValueError("skew area must equal content size")
    if not any(target):
        return 1

    states_used = 0

    def spend(row_index: int, phase: str) -> None:
        nonlocal states_used
        if states_used == max_states:
            raise StateLimitExceeded(max_states, states_used, row_index, phase)
        states_used += 1

    # State: (content used above this row, preceding row's sorted counts).
    # Value: number of distinct tableau prefixes reaching that state.
    zero = (0, 0, 0)
    frontier = {(zero, zero): 1}
    for row_index, (outside, inside) in enumerate(zip(outer_parts, inner_parts)):
        width = outside - inside
        following = {}
        for (used, preceding), ways in frontier.items():
            spend(row_index, "state expansion")
            remaining_one = target[0] - used[0]
            # Reading each row right to left gives 3s, then 2s, then 1s.
            # Each descending block need only satisfy its final ballot bound.
            max_twos = min(target[1] - used[1], used[0] - used[1])
            max_threes = min(target[2] - used[2], used[1] - used[2])
            first_threes = max(0, width - remaining_one - max_twos)
            last_threes = min(width, max_threes)
            for threes in range(first_threes, last_threes + 1):
                first_twos = max(0, width - threes - remaining_one)
                last_twos = min(width - threes, max_twos)
                # The outer bounds ensure this inner interval is nonempty;
                # no uncharged scan of empty candidate intervals is possible.
                for twos in range(first_twos, last_twos + 1):
                    spend(row_index, "candidate row pattern")
                    ones = width - twos - threes
                    row_counts = (ones, twos, threes)
                    if row_index and not _strict_columns(
                        inner_parts[row_index - 1], preceding, inside, row_counts
                    ):
                        continue
                    next_used = (used[0] + ones, used[1] + twos, used[2] + threes)
                    key = (next_used, row_counts)
                    following[key] = following.get(key, 0) + ways
        frontier = following
        if not frontier:
            return 0
    # Every surviving path filled every skew cell without exceeding any
    # target component. The validated area equality forces full content.
    return sum(frontier.values())
