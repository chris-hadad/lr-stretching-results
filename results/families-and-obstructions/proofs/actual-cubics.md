# One strict fiber witness over an entire boundary face

Root derivation, 10 September 2026. Draft theorem and proposed application;
mask completeness and exact population acceptance remain separate gates.

Let `C` be a rational polyhedral cone in a real vector space, defined by
homogeneous nonnegative rows, and let `pi` be a linear boundary projection.
Write `B = pi(C)`. Let `F` be a face of `B`, and take `b` in `relint(F)`.
Suppose `x0` belongs to `C`, with `b0 = pi(x0)` in `F`.

There is a positive rational `epsilon` with `b - epsilon b0` in `F` when the
data are rational. In a complete inequality description of `B`, rows tight
on `F` vanish on both boundaries; every other row is positive on `b`.
Choose `epsilon` below the finitely many positive ratios
`ell(b)/ell(b0)` for rows with `ell(b0) > 0`. This explicitly preserves every
inequality. Choose `x1` in `C` above `b - epsilon b0`. Then

    x = x1 + epsilon x0

lies in the entire fiber above `b`. Every nonnegative row that is positive
on `x0` remains positive on `x`. Every row forced to zero on `pi^(-1)(F)`
remains zero. Thus a witness with the complete possible positive row set
certifies that same row set on every fiber above `relint(F)`.

The fiber's affine direction space is the kernel of its boundary projection
and those forced zero rows. A coordinate-identification chart with a witness
strict on every remaining nonconstant row therefore has its exact predicted
dimension throughout that relative boundary face. In this full chart, true
interiors are obtained by making precisely the nonconstant rows strict;
boundary-only zero rows must remain equalities.

For hives, use every full rhombus inequality and weakly decreasing **real**
boundary weights. Allow negative last parts in this auxiliary cone. The target
boundary still consists of ordinary nonnegative partitions, but the intermediate
`b - epsilon b0` need not: no counting assertion is made about that intermediate
fiber. This avoids an unjustified requirement that `b0` have the same zero
last parts. The complete boundary cone is supplied by the Horn theorem, with
trace balance and chamber inequalities. The primary
Knutson–Tao–Woodward paper, *The honeycomb model II*, Section 6 and its
corollary, supplies the sufficiency and multiplicity-one facet description.
Source: <https://arxiv.org/pdf/math/0107011>. This source theorem must be
matched to the complete actual index roster before computational application.

A sound boundary-mask closure supplies some forced rows. It does **not**
establish that all remaining rows can be simultaneously strict. The new exact
PPL probe asks for a witness with gap zero on mask bits, every other boundary
gap at least one, every closure rhombus zero and every other rhombus at least
one. Every returned rational coordinate and slack is checked directly.

A successful witness is useful over boundaries in the corresponding face
whose additional Horn inequalities are strict, provided the complete projection
description is certified. A failed primal LP alone is unresolved: it may
mean the mask is impossible, that all boundaries have a tight Horn inequality,
that the closure missed a forced row, or an instrument failure. Those are
different mathematical outcomes. The next repair is an explicit exact dual
certificate and a separate Horn-strict feasibility test, not a guess at degree.

## Complete rank-six/seven certificate and low-degree consequence

The new full orbit roster covers all `32,768 + 262,144` original gap masks.
The existing bound-at-most-three terminal handles `28,427 + 171,165` masks.
The remaining `4,341 + 90,979` masks have exactly `445 + 8,075` representatives
under the twelve accepted whole-count symmetries. Every one of those **8,520**
representatives now has a rational witness strict on every rhombus outside its
sound closure, with every coordinate, slack, gap and exact affine rank checked.
The independent complete roster/witness verifier and mathematical gate remain
acceptance requirements. The two deliberately impossible pilot controls are
outside this residual roster and retain their unresolved pilot status.

Assuming the complete certificate passes that gate, it proves:

**Every nonempty ordinary LR polynomial of final rank at most seven and actual
degree at most three is coefficientwise nonnegative, at every size.**

Here is the full argument. Ranks at most five use the adopted theorem. At
rank six, a feasible boundary on a proper multiplicity-one Horn facet factors
into two source-positive lower-rank polynomials. Otherwise every regular Horn
facet is strict. Its partition-gap mask determines its relative face in the
complete boundary cone. The witness-transfer argument gives exactly the sound
closure's predicted affine dimension on that face. If any equivalent mask has
bound at most three, the existing complete short-normal terminal applies.
Otherwise its certified representative has dimension at least four, contradicting
the actual degree at most three. The tensor permutations and duality preserve
regular Horn strictness, gap-face identities and the whole polynomial; determinant
normalization and any trimmed lower rank retain their explicit source maps.

At rank seven, a proper Horn factor has ranks at most five on both sides unless
it is a `1 + 6` split. In the latter case the nonempty rank-six child has degree
at most the parent's degree, since whole polynomial degrees add in the exact
factorization. The just-proved rank-six low-degree theorem applies. Away from
proper Horn facets the same complete mask/witness argument applies at rank seven.
Empty parents give the zero polynomial throughout. Degree zero, one and two
are already intrinsic positive terminals; the new substantive extension is the
entire actual cubic class.

This is an all-size low-degree theorem conditional only on the named accepted
source premises and the new complete certificate. It does not prove a whole
rank, the remaining degree-four-and-higher box, or cubic positivity at arbitrary
larger rank. It adds no original-box census credit without an exact overlap
join. A possible rank-six/seven ordinary-negative polynomial must therefore
have actual degree at least four after this theorem is accepted.
