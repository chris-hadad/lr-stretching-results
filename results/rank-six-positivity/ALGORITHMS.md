# Algorithms behind the certificate

The infinite family of boundary triples is handled by the geometric proof.
The algorithms below work with a complete finite set of original normal
supports and exact lattice data. A bounded census of LR triples is not the
source of the all-size conclusion.

| Obstacle | Construction used here | Reusable implementation |
| --- | --- | --- |
| Boundary triples form an infinite family | Use the original fixed 45-row homogeneous hive family and its complete normal-cycle identity | [Proof](PROOF.md) |
| Many abstract supports cannot carry edges | Compute whole-cone tight-row closure for every physical-row branch; retain a support if at least one branch has interior closure rank nine | [Original-row classifier (C++)](../../tooling/whole_rank_six/src/astra054-2026-09-25/geometry/classify_v1.cpp) |
| A large polyhedral dependency complicates inspection | Reconstruct the gauged 25-dimensional cone by exact double description from 25 independent inequalities and 20 further cuts | [Exact cone reconstruction (Python)](../../tooling/whole_rank_six/src/portable/geometry_stdlib.py), with an optional independent Sage check |
| Closure needs a short, independently checkable explanation | Use 103 positive identities, feasible integral witnesses and complete RUP refutations to prove exact closure for all physical row sets | [Closure calculus and constructive interface](GEOMETRY.md) |
| A raw count of support rows does not prove completeness | Check the complete q7 domain and every q7-to-q8-to-q9 extension, kernel, original index, group transport and multiplicity | [Complete support coverage (C++)](../../tooling/whole_rank_six/src/portable/coverage.cpp) and the [lower coefficient package](../../tooling/whole_rank_six/lower/README.md) |
| A Gram matrix and lattice index do not determine a local scalar | Preserve the entire image lattice, primitive axes and finite numerator; check exact type transports against original columns | [Scalar derivation in the manuscript](../../papers/rank-six/rank-six.tex) and [complete scalar tools](../../tooling/whole_rank_six/scalars/README.md) |
| Full degree-nine Taylor data are expensive | Use odd-dimensional reciprocity to reduce to 511 proper-subset constants, with the complete exceptional finite-character correction | [Reciprocity core](../../tooling/whole_rank_six/scalars/src/production_core_v1.hpp), [finite characters](../../tooling/whole_rank_six/scalars/src/production_characters_v1.hpp) and [range checker](../../tooling/whole_rank_six/scalars/src/production_range_v2.cpp) |
| A floating proposal cannot establish a sign | Round to a declared rational field and evaluate every required inequality with integer/rational arithmetic, rebuilding the primitive original-normal action | [Field verification](../../tooling/whole_rank_six/README.md) |

## How the field was found

Write the complete sparse correction operator as B, the local constants as
alpha, and the floating field coordinates as x. For a retained row i, the
search seeks `alpha_i + B_i x >= tau`. One cyclic halfspace projection uses

```
violation = tau - alpha_i - dot(B_i, x)
if violation > 0:
    x += omega * violation / dot(B_i, B_i) * B_i
```

Rows are processed sequentially and a complete residual scan follows each
sweep. Here `0 < omega < 2`; the successful native searches used `omega=1`
and `tau=10^-6`. This projection method is classical. The decisive change
was the mathematically justified set of rows on which positivity was required.
Earlier unpruned searches had stalled; that was not an infeasibility proof of
the unpruned sufficient system.

The preserved discovery record describes two stages. A first search, started
from an earlier campaign checkpoint, imposed a more restrictive
full-dimensional search subset. A second search restored **every** retained
row, including the rows required for hidden-dimensional hives. It processed
13,325,662 orbit rows and 149,844,829 stored sparse entries, reaching a floating
minimum within about `2e-17` of the target after 576 sweeps. This is a report
of the discovery computation, not a fresh reproduction of its warm starts.
The published field uses the complete retained set, without relying on the
first search subset's classification. A later independent geometric
[converse](GEOMETRY.md) proves that each retained independent physical branch
does occur for some legal integral boundary and some compatible positive
generic refinement. This existential statement is separate from the discovery
run and does not assert occurrence at every boundary or refinement.

The floating field was converted to integer numerators using denominator
`6 × 10^10`. The factor six belongs to the averaged field convention and cannot
be omitted. Every retained corrected value was then checked exactly, giving
the explicit minimum in [the proof](PROOF.md#4-the-exact-finite-premises).
The theorem uses the convenient smaller bound `1/2,000,000`. Verification
needs the rational numerators and the complete original action; it does not
depend on the floating optimizer, its warm start or its stopping heuristic.

## What an independent checker reconstructs

The cone checker starts from inequalities, not a supplied ray list. Its
initial simplicial cone is the inverse image of the nonnegative orthant under
a square nonsingular original-row matrix. At a new halfspace, keep feasible
rays and intersect every positive-negative adjacent pair. Adjacency is tested
using the complete current tight-row masks: the smallest face containing a
pair must have exactly two extreme rays. Exact rank checks certify every
final ray and every original facet. The resulting 166 rays and tight masks
agree byte for byte with the separate Sage/PPL reconstruction.

An alternative five-second closure check uses the 254,843-byte positive-rule
certificate. It checks feasible witnesses, rather than requiring them to be a
complete extreme-ray list. The certificate's complete Boolean refutations close
the gap between rule closure and witness closure. Its 166 zero masks match the
original classifier exactly, and all six physical symmetry transports preserve
them. Both the direct cone reconstruction and the short closure proof are
included so readers can choose independent routes to the same predicate.

The field checker reconstructs each saturated kernel and primitive quotient
incidence, including stabilizers under all six triangle isometries. It checks
the action against the stored sparse matrix instead of accepting the matrix
as an unexplained oracle. The scalar checker separately reconstructs every
required local constant and its lower dependencies. Hashes identify the
particular inputs to these mathematical checks; hashes alone do not establish
their validity.

For the top coefficients, a short independent Python holomorphic-projection
implementation and a C++ forward Euler--Maclaurin implementation agree on
every original independent support of size one, two or three. This removes
a larger inherited catalog from the rank-six proof and supplies explicit
positive bounds without a correction field for these three indices.

## Further improvements

The certificate may admit a smaller field or a more local explanation.
One bounded follow-up fixes a single generic positive row relaxation and
filters supports by its additional slack signs, taking an existential choice
over every physical branch and every symmetry image. A distributed 1,000-row
diagnostic removed 237 of 520 supports retained by the current predicate.
That is not a complete support census or a global storage saving. A usable
replacement requires a complete pass, a complete used-coordinate analysis
and independent review of the stronger support argument. It is not a premise
of the certificate supplied here.

The [contribution record](CONTRIBUTIONS.md) separates the Opus pruning and field
construction, Fable orchestration, earlier Pro and Codex algorithms, subsequent
independent checks and the classical mathematical ingredients.
