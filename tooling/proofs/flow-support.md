# Exact interval-flow support certificates

## API and supported object

```python
from slr_ehrhart.flow_support import (
    flow_support_certificate,
    verify_flow_support_certificate,
)

certificate = flow_support_certificate([(0, 1), (0, 2), (1, 2)], [1, 1])
verify_flow_support_certificate([(0, 1), (0, 2), (1, 2)], [1, 1], certificate)
```

For `n = len(totals)`, the entire object is

```text
P = {x >= 0 : sum(x[e] for e=(u,v) if u <= i < v) = totals[i], 0 <= i < n}.
```

Inputs are lists or tuples. Each edge is a list or tuple `(u, v)` of exact
Python integers with `0 <= u < v <= n`; totals are exact Python integers.
Bools, integer subclasses, floats, fractions, strings, and numeric coercions
are refused with `ValueError`. Signed totals are allowed: a negative total
produces an infeasibility certificate. Empty edges, empty totals, and zero
totals are valid when the endpoint constraints hold.

The original input position labels an edge. Repeated endpoint pairs are
rejected, including repeated pairs written once as a list and once as a tuple.
This API does not merge duplicate columns or support parallel labeled edges.
Reordering the input reindexes all identity-bearing fields; copied endpoint
pairs bind each index to its original edge. Output does not alias inputs.

Both APIs use only the standard library and exact arithmetic. Generation uses
integer augmenting paths with sorted adjacency, then checks its own result.
Verification checks witnesses without rerunning max flow. There are no native
calls, persistent caches, samples, or internal execution deadlines; callers
own resource containment. No speed comparison is claimed.

## Certificate contract

Every result is a JSON-ready dictionary with copied `interval_edges`, copied
`totals`, the exact boolean `feasible`, and the successive-difference balances
`b`. Its remaining fields depend on feasibility.

For a feasible fiber:

- `flow` gives one nonnegative integer value for every original edge.
- `active` lists exactly the edge indices positive at some feasible point.
- `positive_cycles` maps the canonical decimal string of each active edge
  whose recorded flow is zero to a simple residual path from its head to tail.
  There are no extra cycle entries for edges already positive in `flow`.
- `forced_zero_cuts` maps every remaining edge index, and only those indices,
  to a residual-closed vertex cut separating its head from tail.
- `vertices_including_isolates` is `n + 1`. `components` counts the undirected
  components of the active graph, including all isolated vertices. `rank` is
  the rank of the active interval columns.
- `dimension` is the intrinsic dimension of this entire fiber. `degree` is
  the same integer, the degree of its Ehrhart polynomial.

For an infeasible fiber, `supply` is the total positive balance. The augmented
network uses source `n + 1`, sink `n + 2`, original-edge capacities equal to
`supply`, and source/sink capacities equal to the positive/negative balances.
`cut` lists a source-containing, sink-excluding vertex set; `cut_capacity`
records its exactly recomputed capacity, strictly less than `supply`. No
max-flow value, dimension, or polynomial degree is claimed by this result.

The verifier returns `True` for a valid certificate, including a valid
infeasibility certificate. Feasibility is the certificate's `feasible` value.
Malformed, incomplete, or false certificates raise `ValueError`. Certificate
containers must be plain dictionaries and lists, keys must be exact strings,
numeric fields must be exact Python integers, and the top-level field set
must match the selected result type. Missing, extra, repeated, out-of-range,
or mismatched identities are refused. Set lists need not be sorted when
verified, but must contain distinct vertices or indices. The generator emits
them sorted. Verification leaves both inputs and certificate untouched.

## Proof and claim boundary

Successive differences transform the interval equations into directed
incidence equations, with outgoing minus incoming balance
`b = (R[0], R[1] - R[0], ..., -R[-1])`. The empty system has one vertex and
`b = [0]`. Edges always point from a smaller vertex to a larger one, so the
graph is acyclic. A feasible nonnegative flow decomposes into paths from
positive to negative balance; every edge carries at most the total positive
balance. Capping original edges at this supply therefore preserves
feasibility. Integral maximum flow gives either a feasible integral witness
or the recorded strict cut obstruction, which also excludes real points.

At a feasible witness, retain every original forward edge as an unbounded
residual arc and add a reverse arc precisely for each positive flow entry.
A zero edge is active if a head-to-tail residual path exists. The recorded
simple path and that edge form a cycle: add one on its forward edges and
subtract one on its reverse edges. This preserves the equations and
nonnegativity and makes the target edge positive. Reverse steps are valid
because every positive integer flow is at least one.

If no such path exists, the vertices reachable from the head form a closed
cut excluding the tail. No original edge leaves this cut, and no positive
incoming edge exists at the recorded flow, since its reverse would leave.
The cut has total balance zero. For every other feasible flow, conservation
then forces every incoming edge across the cut, including the target edge,
to vanish. The verifier checks closure, separation, and zero balance.

The complete active/forced partition now identifies the affine hull. Average
the finitely many feasible witnesses that make each active edge positive to
obtain a point positive on every active coordinate. Nonnegativity imposes no
further affine equations there. Consequently,

```text
dimension = number of active edges - rank(active interval columns)
          = number of active edges - (n + 1) + components.
```

The rank comparison follows from the injective successive-difference map
and the incidence rank formula. Verification independently performs rational
elimination on the original interval columns and checks the graph component
count, including isolated vertices.

Every column is a nonempty interval, so every coordinate is bounded by a
total on that interval. The interval matrix has consecutive ones in each
column and is totally unimodular; equivalently these are acyclic incidence
flow equations. Integral totals therefore give a bounded integral polytope
when the fiber is feasible. Its lattice-counting Ehrhart polynomial has
degree exactly the certified intrinsic dimension, including degree zero for
a point. The all-zero fiber is the single zero flow. Infeasible fibers have
no nonempty-polytope Ehrhart degree assigned by this API.

This module supplies no arbitrary LR inverse and no theorem about ordinary
coefficient signs. Using its degree for an LR family requires an independent
argument identifying the entire polytope and its lattice, or another fully
proved count-transfer argument with the same consequence. A face embedding,
selected subset of tableaux, or agreement of finitely many counts is
insufficient. The original FRC support-construction premises remain separate.

## Focused verification

`tests/test_flow_support.py` exhausts all unique interval-edge subsets for
zero through three cuts and totals in `{0, 1, 2}`. It compares feasibility,
active identities, and dimension against independent integer enumeration
and rational rank of differences of all enumerated points. Additional cases
cover actual unit-cycle witnesses, disconnected supports, forced-zero edges,
isolated vertices, signed infeasibility, empty cases, large exact integers,
edge reordering, JSON round trips, input copies, and malformed/tampered
certificate refusals. These controls do not enlarge the mathematical scope.

Run the included checks with `python3 -B tooling/check.py` from the repository
root. They also compare twenty-six selected original support records with the
maintained certificate interface. This verifies the selected objects and
explicit general certificate arguments; it does not enlarge any LR domain.
