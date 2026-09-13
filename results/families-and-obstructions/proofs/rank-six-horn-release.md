# The first release from the highest-weight Horn vertex

Root derivation, 10 September 2026. Exact reconstruction and independent
counts are complete; mathematical review governs adoption.

## Whole family and complete Weyl cancellation

For `n >= 3`, let `rho = (n-1,n-2,...,0)`, and let
`theta = (1,0,...,0,-1)`. Take integers `M >= 0`, `0 <= s <= 2M`, and set

    mu = nu = M rho,
    lambda = 2M rho - s theta.

These are balanced ordinary partitions. The origin is the point polynomial;
for `M,s > 0` the final ordinary rank is `n` and the outer area is
`M n(n-1)`. At `s=0` the highest-weight product has coefficient one.
The complete departure from this Horn vertex is being studied, not a selected
face or a polynomial assigned to an auxiliary graph.

Let `K_(n-1)(R)` count all nonnegative integral flows on the complete acyclic
graph with vertices `0,...,n-1`, where the prefix netflow at cut `i` is `R_i`.
It is zero if any prefix is negative. Expanding both Weyl alternants and
extracting the dominant monomial gives

    P_(M,s)(t) = sum_(w,w' in S_n) sign(w) sign(w')
       K_(n-1)(st * 1 - (Mt+1)(d(w)+d(w'))),

where `d_i(w)` is the loss in the first `i` partial sum of `rho` under `w`.
Each `d_i` is a nonnegative integer. Since `st <= 2Mt < 2(Mt+1)`, a surviving
term has `d_i(w)+d_i(w') <= 1` at every cut.

The permutations with all `d_i` in `{0,1}` are exactly products of disjoint
adjacent transpositions. Indeed a size-`i` prefix with loss zero is
`{1,...,i}`; loss one forces `{1,...,i-1,i+1}`. Two consecutive losses equal
to one are incompatible with nested prefixes. Conversely disjoint adjacent
swaps give exactly those losses. The two swap sets must be disjoint, and
their union is a subset `S` of the path of `n-1` cuts. Each connected run of
`S` has exactly two alternating colorings between `w` and `w'`.

Therefore the **entire all-stretch identity** is

    P_(M,s)(t) = sum_(S subset [n-1]) (-1)^|S| 2^components(S)
           K_(n-1)(st * 1 - (Mt+1) 1_S),                 (1)

with the empty-set weight one. Every Weyl contribution is accounted for.
For `s <= M`, only `S` empty survives, giving the stable complete-flow count.
For `M <= s <= 2M`, put `u = 2M-s >= 0`, `v = s-M >= 0`. The two prefix
levels for positive `t` are

    H = (u+2v)t,       L = vt-1.

For `v >= 1`, both are nonnegative and `H >= 2L`. At `v=0`, every nonempty
`S` vanishes and the stable complete-flow branch is retained separately.

## Complete polynomial space on the two-level cone

For fixed `S`, the complete graph flow polytope with prefixes in `{H,L}`
has one Minkowski chamber on `H >= 2L >= 0`.

Every spanning-tree basic edge flow is a signed subset sum of netflows,
hence `aH+bL` for integers `a,b`. Setting `H=L` makes the netflow
`(L,0,...,0,-L)`, so `a+b` is one of `-1,0,1`. With `U=H-2L`, the edge flow
is `aU+(a+delta)L`, where `delta=a+b`. The two coefficients cannot have
opposite strict signs. Thus every tree basis has an unchanged feasibility
status in the interior of this parameter cone. Optimal reduced costs depend
on the objective and basis, not on the boundary. Its support function is
linear on the cone, giving the exact whole Minkowski sum from the two rays,
including the boundary by continuity of these bounded fibers.

Incidence tree bases are unimodular; both ray polytopes are integral. The
complete lattice-point count is consequently a bivariate Ehrhart polynomial
of total degree at most `D=(n-1)(n-2)/2`, valid on the closed cone. This uses
the full lattice, all edges and exact support functions; a pair of sample
counts would not establish the chamber.

At `n=6`, `D=10`. Write `w=v-1 >= 0`. Formula (1) at stretch one is a single
polynomial `F(u,w)` of total degree at most ten, since each term is evaluated
at `U=u+2`, `L=w`. The 66 sites `u,w >= 0`, `u+w <= 10` therefore determine
the entire polynomial. Define `G(u,v)=F(u,v-1)`. For `v>0`,

    P_(u+v,u+2v)(t) = G(tu,tv)

at all positive integer stretches, hence as polynomials including zero.
The `v=0` branch was checked separately against the stable flow count at
`u=0,...,12`, in the full prior degree-ten space. The two independent
polynomials therefore agree identically on this boundary.

All 66 determining sites and two unused positive parameter sites were counted
independently from their bare LR triples using the pinned installed lrcalc.
A separate rational Vandermonde elimination reconstructs all 66 coefficients
directly from those native values and matches the root interval-root model.
The unused sites `(u,w)=(11,0),(0,11)` agree in both models, with counts
5,607,328 and 5,004,792. `A005-HORN-VERIFY-001.json` binds this complete
reconciliation. No selected scalar agreement substitutes for reconstruction.

The resulting `G(u,v)` has 63 nonzero monomials, all with positive rational
coefficients; its constant is one and its linear part is

    (2843/840) u + (129/35) v.

Hence every ordinary coefficient of the entire family is nonnegative for
all `M >= 0, 0 <= s <= 2M`. For `M < s < 2M` its actual degree is ten;
at `s=2M>0` it is eight. For `0 < s <= M`, the stable branch is
`C_6(st)` of degree ten; `s=0` is the point polynomial. The first nontrivial
released endpoint, `M=1,s=2`, has lambda `(8,8,6,4,2,2)`, inner partitions
`(5,4,3,2,1)`, outer size 30, and value 23 at stretch one. This family
contains boundary and lower-dimensional cases; no whole-rank theorem follows.

The exact ordered triples at `(u,v)=(0,1),(1,1)` are refused by both existing
`Cdagger` and `Csplit` membership APIs: respectively domain row 341 and the
split row `nonnegative_5_5` with slack `-1`. Thus the released theorem includes
members outside both current sufficient charts. The stable `(1,0)` example
is admitted by `Csplit`, so the stable overlap is preserved explicitly.
These observations are retained in `A005-AUXILIARY-VERIFY-001.json`; they
make no worldwide novelty assertion or census increment.

The root dense interval-root counter supplies one counting model. All its
prefix coordinates are nonnegative and its complete grid is downward closed,
so the ordinary unbounded-knapsack recurrence over every positive interval
root gives exact whole counts. Its grid coordinate count is `n-1`; this is
not the flow/hive dimension `D`.

## Interior threshold of the stable complete-flow branch

For `s=1 <= M`, write `C_n(t)=K_(n-1)(t,...,t)`. All edges are active, the
incidence matrix has rank `n-1`, and the saturated affine lattice is obtained
by taking nonadjacent edges freely and solving adjacent edges integrally.
Hence the entire polynomial has actual degree `D=(n-1)(n-2)/2`.

Its relative interior consists exactly of positive edge flows. Each cut has
`i(n-i)` edges and total flow `t`, so an integral interior point needs
`t >= max_i i(n-i) = floor(n^2/4)`. This is attained: assign one to every
nonadjacent edge and assign

    x_(i-1,i) = t - i(n-i) + 1

to each adjacent edge. Every edge is positive at that threshold, and all cut
equations hold. Thus the true codegree is exactly

    q = floor(n^2/4).

Reciprocity gives roots `-1,...,-(q-1)`. The remaining factor has degree
`D-q+1`; its complete numerical reconstruction needs only that many positive
determining nodes, constant one and two unused positive holds. This greatly
reduces the required full counts. It does not by itself prove any remaining
ordinary sign or a reflection law.

The new complete-flow component sums all outgoing distributions through exact
suffix sums on simplex grids. It counts the whole graph and keeps every
source-to-sink edge. Its separate direct-recurrence fixtures, state/work/memory
limits and independent LR reconstruction govern use. Counts beyond a typed
limit remain unknown; no partial vector is promoted.

At ranks 8, 9 and 10, primary vectors of degrees 21, 28 and 36 were recovered
in their complete codegree-reduced spaces, then matched at two unused positive
nodes. A separate complete interval-root model reconstructs the entire rank-8
vector and both holds. Rank 8 is independently supported; ranks 9 and 10
remain provisional one-model vectors. The rank-10 native check at stretch 14
hit its 60-second deadline and is retained as incomplete, with verified exit.
This timeout is neither a failed identity nor a negative coefficient.

The rank-8 second model uses 4,782,969 grid cells and 76,527,504 array bytes.
The faster simplex-grid component retains all complete graph edges and reduces
the determining-count cost substantially. Its 40 direct/failure fixtures and
the interval-root component's 340 independent small counts, two rank-8 base
controls and eight typed failure controls are separate from the scientific
rank and polynomial claims. No original-box or additive coverage promotion
is assigned to these flow diagnostics.
