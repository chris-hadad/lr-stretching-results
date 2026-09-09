"""Exact skew semistandard tableau counts by aggregated horizontal-strip chains.

Standard library only. Native algorithm provenance and the aggregation proof
are recorded in the owning SHARED-TOOLS extension's SKEW-COUNT.md.
"""

from __future__ import annotations

from collections.abc import Sequence

from .constructions import _integers, _partition

__all__ = ["SkewCountLimitError", "skew_tableau_count"]


class SkewCountLimitError(RuntimeError):
    """An admitted-work ceiling stopped the count; no partial count is supplied.

    ``statistics`` is a copied snapshot with ``states`` and ``transitions``.
    States count the initial entry and each newly created entry in each row
    sweep. Transitions count admitted row choices before their multiplicities
    are aggregated. These are work ceilings, not peak-memory or wall-time caps.
    """

    def __init__(self, resource: str, limit: int, statistics: dict[str, int]) -> None:
        self.resource = resource
        self.limit = limit
        self.statistics = dict(statistics)
        super().__init__(f"skew tableau count incomplete: {resource} limit {limit} exhausted")


def skew_tableau_count(
    outer: Sequence[int], inner: Sequence[int], content: Sequence[int], t: int = 1, *,
    max_states: int | None = None, max_transitions: int | None = None,
) -> int:
    """Count SSYT of shape t*outer / t*inner with ordered content t*content.

    Partitions, content, t, and optional ceilings require exact nonnegative
    Python integers; bools and numeric coercions are rejected with ValueError.
    The inner partition must be contained in the outer, and the nonempty
    content sequence must sum to their size difference. Zero content entries
    retain their label positions; their identity steps need no row sweeps.
    All inputs are validated before t=0 or other elementary shortcuts.

    This is a full skew SSYT/Kostka count. Its interpretation as an ordinary LR
    value requires the separately proved skew_content_to_lr construction; it
    does not evaluate arbitrary LR triples or impose the LR lattice-word rule.
    At t=0 the empty scaled tableau counts as one even if positive dilations
    have no tableaux. This scalar API assigns no dimension, degree, or Ehrhart
    or LR polynomial through that exceptional zero-dilation value.

    A state admission is the initial tuple or a newly created dictionary entry
    in any bottom-up row sweep. A transition admission is a row choice from a
    current mixed tuple, including choices that merge into an existing entry.
    Both ceilings are checked before either counter or dictionary advances.
    Exhaustion raises SkewCountLimitError without a partial numerical result.
    Elementary zero/one results use no DP work and respect zero work ceilings.
    No global cache or array indexed by dilation is used; general instances
    remain combinatorial and require an external runtime bound when needed.
    """
    lam = _partition(_integers(outer, "outer"), "outer")
    mu = _partition(_integers(inner, "inner"), "inner")
    weights = _integers(content, "content")
    if any(part > (lam[i] if i < len(lam) else 0) for i, part in enumerate(mu)):
        raise ValueError("inner must be contained in outer")
    if not weights:
        raise ValueError("content must specify a nonempty ordered alphabet")
    if sum(weights) != sum(lam) - sum(mu):
        raise ValueError("content sum must equal |outer| - |inner|")
    for name, value in (("t", t), ("max_states", max_states),
                        ("max_transitions", max_transitions)):
        if value is None and name != "t":
            continue
        if type(value) is not int or value < 0:
            raise ValueError(f"{name} must be an exact nonnegative integer")
    if t == 0 or not any(weights):
        return 1

    n = len(lam)
    mu += [0] * (n - len(mu))
    remaining_labels = sum(weight > 0 for weight in weights)
    # After h horizontal strips, outer[i+h] <= inner[i] is necessary.
    if any(mu[i] < lam[i + remaining_labels] for i in range(n - remaining_labels)):
        return 0
    if remaining_labels == 1 or sum(left != right for left, right in zip(lam, mu)) == 1:
        return 1

    cap = tuple(t * value for value in lam)
    initial = tuple(t * value for value in mu)
    statistics = {"states": 0, "transitions": 0}

    def admit(new_state: bool, transition: bool) -> None:
        if new_state and max_states is not None and statistics["states"] >= max_states:
            raise SkewCountLimitError("states", max_states, statistics)
        if (transition and max_transitions is not None
                and statistics["transitions"] >= max_transitions):
            raise SkewCountLimitError("transitions", max_transitions, statistics)
        if new_state:
            statistics["states"] += 1
        if transition:
            statistics["transitions"] += 1

    admit(True, False)
    states = {initial: 1}
    previous_area = sum(initial)
    for weight in weights:
        if weight == 0:
            continue
        size = t * weight
        remaining_labels -= 1
        future_minimum = tuple(cap[i + remaining_labels] if i + remaining_labels < n else 0
                               for i in range(n))
        for i in range(n - 1, -1, -1):
            following: dict[tuple[int, ...], int] = {}
            for shape, ways in states.items():
                # Lower rows are new, upper rows are old. Every old shape at
                # this label boundary has previous_area, so no spent key is needed.
                room = size + previous_area - sum(shape)
                upper_capacity = sum(
                    (cap[j] if j == 0 else min(cap[j], shape[j - 1])) - shape[j]
                    for j in range(i)
                )
                low = max(shape[i], shape[i] + room - upper_capacity, future_minimum[i])
                high = min(cap[i], shape[i - 1] if i else cap[i], shape[i] + room)
                for value in range(low, high + 1):
                    updated = shape[:i] + (value,) + shape[i + 1:]
                    admit(updated not in following, True)
                    following[updated] = following.get(updated, 0) + ways
            states = following
            if not states:
                return 0
        previous_area += size
    return states.get(cap, 0)
