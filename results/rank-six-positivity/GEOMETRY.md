# Exact closure and legal realization of hive faces

Two geometric results make the rank-six proof easier to inspect and provide
tools for other hive questions. The first is valid at every rank. The second
replaces a polyhedral oracle for rank-six closure with 103 positive identities
and a small exact certificate. Neither requires the large positivity field.

## Which physical branches can occur?

Keep every original rhombus inequality `rho_r(b,x) >= 0`, including separate
physical rows with equal interior normals. Let `C` be the cone of all hive
heights, before fixing the boundary. For a physical-row set S define

$$\operatorname{cl}(S)=\{r:\rho_r(h)=0\text{ for every }h\in C
\text{ satisfying }\rho_s(h)=0\ (s\in S)\}.$$

Write `rank_x` for rank after restricting to the interior coordinates.
For rank n, their number is `m=(n-1)(n-2)/2`.

**Legal-realization theorem.** Suppose `n >= 3` and S has q independent
interior normals, with `1 <= q <= m`. Then

$$\operatorname{rank}_x\operatorname{cl}(S)=q$$

if and only if **some legal integral LR boundary and some compatible positive
generic relaxation of the original rows** realize S as a normal cell of
positive actual `(m-q)`-dimensional face weight. The parent hive may be
lower-dimensional or nonsimple. The face measure uses the original saturated
integer lattice. For q=m this is a point face; its parent need not be a point.

Necessity is the support lemma in the [main proof](PROOF.md): a positive-weight
face cannot obey more independent interior equalities than its codimension.
For sufficiency, choose an integral relative-interior height of the universal
face defined by S. Positive scaling clears rational denominators. Its tight
rows are exactly `T=cl(S)`. The fixed-boundary face has dimension `m-q` and
affine lattice `x_* + ker_Z(N_T)`.

The boundary can always be made legal. In the convention where lambda is the
vertical outer edge, the rhombus inequalities imply that all three boundary
words are decreasing. Adding the affine height `u*i+v*j-h(0,0)`, with

$$u=\max(0,-\mu_n),\qquad
v=\max(0,-\lambda_n,u-\nu_n),$$

makes them nonnegative integral partitions. It preserves every rhombus slack,
the trace, and the translated interior lattice. An explicit rational right
inverse of `N_S` then constructs a positive row relaxation with exactly S
tight. Small distinct powers of a rational parameter avoid every circuit
wall. Determinant bounds provide an explicit amplitude for which the entire
relaxed fan is compatible with the original hive. The
[manuscript](../../papers/rank-six/rank-six.tex) gives the complete construction,
including boundedness and the inequalities needed for hidden dimensions.

This is an existential theorem about a boundary and a refinement. It does not
assert occurrence at every boundary, in every refinement, or under an arbitrary
assignment of abstract weights. It also does not make each retained inequality
necessary for all possible positivity proofs.

## A complete 103-identity closure calculus

At rank six there are 45 physical rhombi on 28 height coordinates. All disjoint
unit-coefficient two-versus-two identities give 30 rules up to reversal; the
three-versus-three identities give 72. One further six-versus-six identity
completes their closure calculus:

$$\rho_4+\rho_{17}+\rho_{18}+\rho_{23}+\rho_{31}+\rho_{41}
=\rho_3+\rho_8+\rho_{24}+\rho_{26}+\rho_{35}+\rho_{39}.$$

The IDs are **zero-based physical rows 0–44** in the supplied
[atlas](../../tooling/whole_rank_six/atlas.json), not its 42 interior-normal
labels. The [certificate](../../tooling/whole_rank_six/closure/CLOSURE-CERTIFICATE.json)
contains the full 28-coordinate matrix and all 103 identities, so the statement
does not depend on a diagram or an implicit ordering convention.

In a feasible hive every slack is nonnegative. If all rows on one side of a
positive identity vanish, every row on the other side vanishes. Apply both
directions repeatedly. **The resulting set is exactly `cl(S)` for every one
of the `2^45` possible initial sets.** There are 206 set implications, or 564
distinct single-conclusion Horn clauses. Iteration adds at most 45 rows.

### Why the small certificate proves every set

Let R(S) be rule closure, C(S) actual cone closure, and V(S) the tight-row
closure on the 166 supplied feasible integral heights. Positive identities
and feasible heights give the sandwich

$$R(S)\subseteq C(S)\subseteq V(S).$$

For each target row r, encode a rule-closed set M that excludes r and meets
the positive support of every supplied height with positive r-slack. Such a
set would satisfy `r in V(M) \ M`. The certificate proves that each of these
45 Boolean formulas is unsatisfiable. It gives nine representative
reverse-unit-propagation (RUP) proofs with 6,488 additions, plus exact
variable bijections for every target's **entire** input clause set.

To check an added clause, assume all its literals false and unit-propagate
the existing clauses. A contradiction proves the addition; each representative
ends with a checked empty clause. Thus every rule-closed M has `V(M)=M`.
Apply the sandwich to `M=R(S)` to obtain `C(S)=R(S)`.

The independent checker regenerates the original rhombi, enumerates both
complete short-identity populations, checks all 2,884 identity coordinates
and 7,470 witness slacks, reconstructs the input formulas, and checks all
proof additions and target transports. It uses Python's standard library,
with **no SAT solver and no extreme-ray completeness premise**. The certificate
is 254,843 bytes and its complete independent check took about five seconds
on the publication host. These timings are measurements, not guarantees.

The witness zero masks also agree exactly with the independently reconstructed
166-ray cone and its six physical symmetry actions. Consequently the small
closure proof certifies the same predicate used by the large rank-six field
classifier. Both verification routes are retained.

### The smallest obstruction to the original short rules

The original 102 rules leave

$$S=\{4,17,18,23,31,41\}$$

unchanged, although its actual closure is

$$\{2,3,4,7,8,9,11,17,18,23,24,26,31,35,39,40,41,44\}.$$

The interior rank rises from six to eight. The new identity and the old rules
force exactly these rows, and a feasible integral height realizes exactly
that tight set. A separate complete check of all 1,385,980 seeds of sizes zero
through five proves **minimum cardinality six**. This does not assert uniqueness
of the obstruction or minimality of the 103-identity presentation.

## Construct witnesses and inspect exact edges

The [standalone tools](../../tooling/whole_rank_six/closure/README.md) verify
the closure certificate and expose an exact Python API. Given any physical
row set, it returns closure and interior ranks. For an independent retained
set it constructs a legal integral boundary, a hive in the relative interior
of its face, the saturated lattice equations, and a positive generic compatible
relaxation. For an edge it additionally returns a primitive direction, exact
endpoints and saturated length. Empty S gives the trivial full-dimensional
case; dependent or excluded sets receive their exact diagnostic.

Pro043 developed the converse and the completed closure calculus during
publication strengthening. The campaign independently checked the proof,
reimplemented the verifier and constructive interface, and replayed every
finite certificate predicate and the minimum-six exhaustion. See the
[contribution record](CONTRIBUTIONS.md) for discovery and verification roles.
The large rational positivity field and the analytic scalar regeneration
remain separate parts of the [whole-rank theorem](README.md).

[Main proof](PROOF.md) · [Algorithms](ALGORITHMS.md) · [All results](../../RESULTS.md)
