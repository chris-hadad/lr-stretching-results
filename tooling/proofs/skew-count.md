# Scalar skew-tableau counter

`skew_tableau_count(outer, inner, content, t=1, *, max_states=None,
max_transitions=None)` counts all semistandard tableaux of the scaled skew
shape with the scaled ordered content. It uses exact Python integers and the
canonical constructor's integer and partition validators. It rejects coercion,
malformed partitions, failed containment, an empty alphabet, inconsistent
content size, negative dilation, and invalid work ceilings before any shortcut.

This API counts full skew SSYT/Kostka fibers. A separately proved application
of `skew_content_to_lr` identifies the count with its constructed ordinary LR
value. The API does not evaluate arbitrary LR triples or assert dimension,
degree, a full coefficient vector, or negativity.

For valid input, `t=0` counts the empty scaled tableau as one, including when
every positive dilation has no tableaux. This scalar convention does not
assign an Ehrhart or ordinary LR polynomial through the zero-dilation value
to an infeasible positive-stretch family.

## Recurrence and aggregation proof

A semistandard tableau corresponds bijectively to a chain of partitions from
`inner` to `outer`: after label `j`, retain the inner diagram and all boxes
with labels at most `j`. The boxes added at one label form a horizontal strip
of size `content[j]`. Conversely, assigning that label to its strip produces
weakly increasing rows and strictly increasing columns.

For old shape `nu`, the new row length `new[i]` can independently range from
`nu[i]` to `min(outer[i], nu[i-1])`, with top-row upper bound `outer[0]`.
These inequalities are exactly the horizontal-strip condition. They also
ensure that the new shape is a partition, because
`new[i] >= nu[i] >= new[i+1]`. Only the total added area couples the choices.

The implementation sweeps rows bottom-up. Its tuple contains old upper rows
and new lower rows, so the predecessor needed by the next interlacing bound
has not been overwritten. At a label boundary, every old shape has the same
area `A`. Therefore, the spent strip budget is `sum(mixed_tuple)-A`.
Two partial sweeps with the same tuple necessarily have the same spent budget
and the same remaining row choices. Their numbers of labeled chains can be
added immediately, including when they started from different old shapes.
No original-label multiplicity is discarded, and no separate spent coordinate
or per-shape list of complete strips is needed.

Before selecting row `i`, let `room` be its remaining strip budget. The old
upper rows can absorb at most

```text
U = sum_{j < i}(min(outer[j], old[j-1]) - old[j]),
```

where the top-row cap is `outer[0]`. The current row must add at least
`room-U` and at most `room`. Intersecting those bounds with its horizontal-strip
interval prunes exactly the choices that exceed the budget or leave more boxes
than the unprocessed rows can hold. At the top row, `U=0` forces the exact
strip size. Additional necessary constraints may still rule out a surviving
partial sweep later; this capacity bound is not a sufficiency claim.

If `h` positive-content labels remain after the current label, any completable
new shape must satisfy `new[i] >= outer[i+h]`, taking rows outside the outer
shape as zero. Repeated interlacing gives this directly: one future strip
implies `next[i+1] <= current[i]`, and iterating through `h` strips implies
`outer[i+h] <= new[i]`. This is only a necessary condition, so it is safe to
enforce while each new row is chosen. It also yields an elementary initial
zero test and forces the final label's new shape to be `outer`.

Content remains in its original order. A zero-content label is an identity
strip and is skipped internally without changing the chain count or the
relative order of all other labels. Zero labels do not contribute to the
future-height bound.

## Work ceilings and elementary fibers

`max_states` bounds cumulative admitted state work: the initial tuple, then
every newly created dictionary entry in every row sweep. A key created again
in a later sweep is new work and is charged again. `max_transitions` bounds
admitted row choices, including choices whose updated tuple already exists
and receives another chain contribution. Merely merging a contribution does
not create another state entry.

Both ceilings are checked before either counter or the destination dictionary
advances. State exhaustion has priority when both checks would fail. The
typed `SkewCountLimitError` carries `resource`, `limit`, and a copied
`statistics` dictionary containing admitted `states` and `transitions`.
It carries no partial numerical count. A failed call cannot install a cache
entry or influence a later call because all state belongs to that call.

Empty shapes, zero dilation, a single nonempty skew row, a single positive
label on a horizontal skew strip, and the initial impossible-height test have
elementary zero/one answers after full validation. These shortcuts use no DP
work and accept zero work ceilings. In particular, enormous dilation of a
trivial fiber does not allocate an array indexed by that dilation. General
instances remain combinatorial; the ceilings do not bound integer bit cost,
peak memory in bytes, or wall time.

## Provenance and checks

The lab's native forward prototype enumerates complete strips from every old
shape; its independent row-sweep prototype aggregates partial shapes with a
spent coordinate. The maintained implementation uses tuple-only aggregation,
exact remaining-capacity pruning and the future-height bound above. Frozen
selected native functions remain benchmark oracles; native files are not changed.

The included thirteen tests cover literal small cell fillings, input and
zero-dilation conventions, scaling, exact work-limit behavior and an actual
rank-thirteen control. The larger scalar comparisons and their method-specific
timings are documented in BENCHMARKS.md. Complete degree-29 coefficient vectors
remain outside these scalar checks.
