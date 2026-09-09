# Mathematical contracts behind the tools

Throughout, lambda is the outer partition and
`P(t)=c^(t*lambda)_(t*mu,t*nu)`. Ordinary coefficients are reported from degree
zero upward. A negative face, quotient or formal signed kernel alone is not a
negative ordinary coefficient of an entire LR polynomial.

## Admissible strips and the whole rank-six sector

Split an N-part composition into groups of sizes `h,q1,q2`, with totals
`U,V,R`, where `h>=0`, `q1,q2>=1` and `U+V+R=T`. The complete extra integer
coordinate satisfies

```text
max(0,V-B) <= s <= D+min(C,U+V).
```

Nonnegative `T,B,C,D` with `T<=B+C+D` guarantee a nonempty interval above
every base point. The lattice is the composition lattice times the integer
coordinate of s. Independent intervals of nonnegative lengths may be multiplied
in; arbitrary coupled fibers have no such positivity assertion.

The count equals the sum of `D+1-V+min(C,U+V)+min(B,V)`, after clamping the
two caps to T. Let `B_n(v)=binom(v+n-1,n-1)` and
`R_k(v)=binom(v+k-1,k)`, with `R_0=1`. The clipped moment for p distinguished
coordinates and q others is

```text
M_pq(Z,W) = sum(k=0..p+q-1) R_k(Z) B_(p+q-k)(W) alpha_k W,
alpha_k = p/(p+q-k) when k<q, and 1 otherwise.
```

This follows by the rising-binomial Vandermonde identity applied to the
clipped composition sum. Clearing its sole denominator with
`(W/r) B_r(W)=binom(W+r-1,r)` gives the maintained integer formula.
Every term has degree at most N under simultaneous dilation; the independent
interval factors give the additional stated degree bound. Exact finite
differences at that proved bound recover the whole polynomial.

The complete positive expansion for both active cuts is included in
[the strip proof](proofs/positive-strip.md). It supplies coefficient positivity;
the subtractive evaluation formula alone would not prove it.

The Cdagger API first checks a fixed, complete sufficient domain on padded
rank-six boundaries. It retains 521 essential Horn, 18 partition and 17 source
facet inequalities, yielding 553 distinct rows on the trace section. Its
unimodular slack chart identifies the entire hive with the strip at
`h=q1=q2=3` times an independent interval. The complete proof is included in
[the sector note](proofs/cdagger.md); the thirty-six exact implications are
replayed by `verify_cdagger_certificate()`. Neither the proof nor the tool
enumerates a complete rank-six fan or claims a whole-box cover.

## Transportation and segment quotients

`transport_count(r,c)` counts all nonnegative integer tables with the supplied
labeled balanced margins. Sorting residual margins does not identify tables:
each equal-cap allocation orbit carries its exact multinomial multiplicity,
and collisions of residual states add their full weights. With two rows left,
the completion is the coefficient of `z^A` in
`product_j(1+z+...+z^c[j])`. Sliding prefix sums and grouped inclusion-exclusion
are two exact ways to obtain it.

For two balanced margin pairs, the complete transportation Minkowski criterion
requires all subset cuts to have compatible signs. For row subset I and column
subset J, the cut quantity is `r(I)+c(J)-sum(r)`. An opposite-sign pair is an
obstruction; absence of one establishes this transportation criterion only.

The exterior segment-quotient count is

```text
q(a,b;t) = sum_Z product_i(t*a[i]-row_i(Z)+1)
                    * product_j(t*b[j]-col_j(Z)+1),
```

over nonnegative integer matrices satisfying the indicated row and column caps.
This is the lattice count of the full polytope with additional slack coordinates
`u_i,v_j>=0` and inequalities `row_i(Z)+u_i<=t*a_i`,
`col_j(Z)+v_j<=t*b_j`. Deleting forced zero caps leaves p by q active exterior
variables and intrinsic degree `p*q+p+q`. The network matrix is totally
unimodular. Strict interiors require positive coordinates and strict cap
inequalities, giving the exact codegree and nonuniform negative-dilation
schedule in the API. Reciprocity uses the original active dimension.

For a specified whole LR parent, the full-lattice construction and the
Minkowski premise are additional obligations. The count function receives no
parent margins and cannot certify them. The complete transportation-to-hive
argument is included in [the transport proof](proofs/transport.md).

## Whole-polytope constructions

For outer/inner skew partitions and ordered content w, set `H=outer[0]`,
`B_i=sum(w[j] for j>i)` and `kappa_i=sum(w[j] for j>=i)`. The ordinary triple
is

```text
Lambda = (H+B, outer),
Mu = (H repeated len(w)-1 times, inner),
Nu = kappa.
```

Insertion/deletion of the fixed superstandard buffer identifies the complete
real row-count polytopes and their integer lattices at every stretch. Content
order and zero entries keep their label positions; this is not Ferrers
conjugation. The full argument is in [the skew lift](proofs/skew-lift.md).

Positive matrix caps admit unique integral slack completion to transportation
margins `(sum(column_caps), *row_caps)` and `(sum(row_caps), *column_caps)`.
Disconnected skew rows followed by the buffer lift produce the whole LR family.
Strictly positive caps give dimension `k*n` and codegree equal to the maximum
of `ceil((n+1)/a_i)` and `ceil((k+1)/b_j)`, witnessed by the all-ones interior
matrix at the threshold. These are constructions, not arbitrary-LR inverses.

The square-matrix invariant constructor and counter retain their independently
verified specialized Weyl identity and scalar size/grade transposition. The
original matrix size is retained by the whole-family constructor. The supporting
[matrix notes](proofs/matrix-invariants.md) distinguish the scalar identity from
an assertion about the entire graded ring. Optional work limits raise a typed
exception; no partial signed sum is returned as a count.

## Exact support and dimension

For unique interval edges `(u,v)` on vertices `0..n`, the complete flow fiber is
`x>=0`, `sum(x[e] for u<=i<v)=totals[i]`. Successive differences turn these
equations into directed incidence balances on an acyclic graph. Integral max
flow supplies a feasible integer point or a strict cut obstruction.

At a feasible point, retain every forward edge and the reverse of every
positive-flow edge. A zero edge is active precisely when its head reaches its
tail in this residual graph. A recorded cycle makes it positive. Otherwise a
closed cut proves it forced zero. The complete active/forced partition gives
dimension `active_edges-(n+1)+components`, including isolated vertices.
Total unimodularity and boundedness make this the exact Ehrhart degree.
[The support note](proofs/flow-support.md) gives the complete certificate
contract and proof. No degree is assigned to an infeasible fiber.

`plan_support` is a different, conditional instrument. If complete summand
spans and a common-type Minkowski polynomial identity are supplied, every
monomial exponent must satisfy the subset span-rank caps. The tool computes
that necessary support. It does not establish the premises, claim each allowed
monomial occurs or evaluate any LR coefficient.
