# Proof of rank-six coefficient positivity

This is the complete geometric implication and coefficient assembly. The
[manuscript](../../papers/rank-six/rank-six.tex) also derives the scalar
recurrences and their odd-dimensional acceleration. The [verification guide](VERIFYING.md)
states the working distribution's current status; incomplete execution must
not be represented as a completed finite premise.

## 1. Original object and conventions

Let λ, μ and ν be integral partitions with λ outer and
`|λ| = |μ| + |ν|`. Pad them to six parts. On the triangular grid
`T = {(i,j): i,j >= 0, i+j <= 6}`, fix

$$h(i,0)=\sum_{a\leq i}\mu_a,\qquad
h(0,j)=\sum_{a\leq j}\lambda_a,\qquad
h(6-j,j)=|\mu|+\sum_{a\leq j}\nu_a.$$

The interior coordinates, in order, are

`(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)`.

Their lattice is `L = Z^10` with the standard metric. All 45 elementary
rhombi are imposed, with the obtuse-corner sum minus the acute-corner sum
nonnegative. Write their physical rows as

$$\rho_r(b,x)=\ell_r(b)+\langle n_r,x\rangle\geq0.$$

The 45 rows restrict to 42 distinct primitive oriented interior normals.
Three directions have two physical preimages. Equal directions retain their
separate boundary offsets.

The hive correspondence identifies `P_b(t) = c^(tλ)_(tμ,tν)` with the lattice
count of `t H_b`. Stretching polynomiality makes that count a polynomial.
Its actual degree is `d = dim H_b`, which need not be ten. All face volumes
below use the full saturated lattice `Z^10 intersect lin(F-F)`, with a
fundamental parallelepiped of volume one, without factorial normalization.

If `s` clears the vertices of a rational hive, `s H_b` is integral and

$$c_k(sH_b)=s^k c_k(H_b),\qquad
\operatorname{vol}_{\mathbb Z}(sF)=s^k\operatorname{vol}_{\mathbb Z}(F).$$

The coefficient identity uses polynomiality. It does not follow by taking
limits of arbitrary Ehrhart quasipolynomials. Constant one transfers from
the integral dilate. A nonempty point therefore has polynomial one. Empty
positive-stretch families have polynomial zero; the all-empty triple has
polynomial one. Padding is handled in the same original hive lattice.

## 2. A complete normal-cycle identity

Work first in a fixed lattice `Z^m`, with a fixed rational positive-definite
metric and a bounded nonempty integral polytope `P` given by the original
inequalities. Fix `1 <= k < m` and `q = m-k`.

**Compatible refinement.** Loosen every original nonzero row by
`δ a_r`, where all `a_r > 0` are generic and `δ > 0` is sufficiently small.
The relaxed polytope is full-dimensional, has the same zero recession cone,
and is simple. Every relaxed vertex uses an independent `m`-row basis.
There are finitely many bases; each one feasible for arbitrarily small δ
has a finite limit in `P`, with that basis still tight. Its limit is an
actual vertex, and the relaxed vertex normal cone is contained in the original
vertex cone. A common small δ therefore gives a pointed simplicial refinement
`Γ` of the full ambient normal fan, with rays from the original normals.
This includes normal fans with lineality from hidden affine equalities.
The relaxed polytope's lattice count is never used.

Give a `q`-cone σ of Γ weight `w_σ = vol_Z(F)` when its relative interior lies
in the normal cone of an actual `k`-face F, whose normal cone has dimension q.
Otherwise give it weight zero. Every top-dimensional subdivision cell of one
actual normal cone receives the same full actual face volume.

**Primitive quotient balance.** For every `(q-1)`-cone τ of Γ,

$$\sum_{\sigma\supset\tau,\ \dim\sigma=q}
w_\sigma u_{\sigma/\tau}=0
\quad\text{in }L^*/(L^*\cap\operatorname{span}\tau),$$

where `u` is the primitive quotient generator. There are three cases. If τ
lies in a coarse `(q-1)`-cone, that cone belongs to an actual `(k+1)`-face G.
The adjacent contributing cells correspond to facets F of G. Put
`M_G = L intersect lin(G-G)`. Saturation makes restriction `L* -> M_G*`
surjective, with the displayed quotient kernel. For a primitive facet
conormal u,

$$\operatorname{covol}(M_F)=\operatorname{covol}(M_G)\|u\|.$$

To see this, extend a basis of `ker u` by a lattice vector v with `u(v)=1`;
its perpendicular height is `1/||u||`. Dividing Euclidean facet balance by
the common covolume gives exactly the primitive lattice balance above.
Changing all outward normals to inward normals preserves its zero sum.
If τ is internal to a coarse q-cone, the two adjacent subdivision cells
have equal weights and opposite primitive directions. If it is internal
to a coarse cone of larger dimension, all relevant weights vanish.
These cases exhaust the refinement, including its nonpointed coarse cones.

For an independent normal support I, let α_I be the **complete** BV local
constant in its saturated normal plane and induced quotient metric. For each
independent `(q-1)`-support J, choose a rational quotient functional h_J.
If `I = J union {n}`, choose a saturated integer kernel basis M_J and set

$$u_{I/J}=\frac{M_J^T n}{\gcd(\text{all coordinates of }M_J^T n)},
\qquad
\beta_I=\alpha_I+\sum_{J\text{ facet of }I}h_J(u_{I/J}).$$

Independence makes the gcd positive. A normal-plane index, or the unchanged
ambient normal, cannot replace this primitive quotient operation.

**Correction identity.** BV's dual solid valuation adds the local constants
over the top-dimensional simplicial cells of each actual normal cone.
Lower-dimensional intersections contribute zero in that fixed span. For a
nonpointed cone, ambient/subspace compatibility identifies the value in the
actual transverse space. The local coefficient formula consequently gives

$$c_k(P)=\sum_\sigma w_\sigma\alpha_\sigma
       =\sum_\sigma w_\sigma\beta_\sigma.$$

For the second equality, insert the correction, interchange the finite sums,
and apply primitive balance at every J. This works for **every rational field**,
independently of the signs of its corrected values. The complete identity
retains every incidence. Transfer to period-one rational polytopes by dilation.

It follows immediately that a positive lower bound ε on all contributing
β_I gives `c_k >= ε sum_F vol_Z(F)`: all weights are nonnegative, and every
actual k-face has at least one top-dimensional normal subdivision cell.

The analytic premises are [Berline–Vergne](https://arxiv.org/html/math/0507256v3),
Propositions 12–13, Definition 22, Corollary 23 and Theorem 26. The refinement
and full lattice-normalized balance above supply the additional geometric
argument; the conclusion is not an extrapolation from sampled hives.

## 3. Which sign constraints are necessary?

For a homogeneous fixed-row family, let C be the cone of combined boundary
and interior coordinates satisfying every original physical row. It may be
a larger cone than the legal LR family, as long as it contains every original
hive. For physical row set S define

$$C_S=C\cap\{\rho_r=0:r\in S\},\qquad
\operatorname{cl}(S)=\{r:\rho_r\text{ vanishes on all of }C_S\}.$$

For an independent q-set I of normal directions, consider **all** physical
branches that choose one row above each direction. Retain I if at least one
branch S has `rank_x cl(S) = q`. The implication needed for positivity is the
necessary support condition below. For the cone of all original hive heights,
the later [legal-realization converse](GEOMETRY.md) proves sufficiency for
some legal integral boundary and some compatible positive generic refinement.
It does not claim occurrence at every boundary or refinement.

**Support lemma.** Every positive-weight q-cell σ has a retained branch.
Let F be the actual k-face carrying its weight. Choose σ's physical defining
rows S in the generic relaxation, and an incident relaxed vertex whose full
independent basis contains S. Its limit v is an actual vertex where those
rows are tight. A covector in `relint σ` is minimized precisely on F and is
also minimized at v, so v lies in F. Each normal in S belongs to `C_F` and
its row is constant on F. Being zero at v, it is zero on all of F.

Let `T(F)` be **all** original rows tight on F, including hidden equalities.
Then `S subset T(F)` and `rank_x T(F) = m-dim F = q`. At a relative-interior
point `(b,x)` of F, every row of `cl(S)` vanishes. Its restriction to F is
a nonnegative affine function; vanishing at a relative-interior point forces
it to vanish identically. Thus

$$S\subseteq\operatorname{cl}(S)\subseteq T(F),\qquad
q\leq\operatorname{rank}_x\operatorname{cl}(S)\leq q.$$

This proves retention for the actual branch. Taking an existential maximum
over all physical branches is safe. No ambient full-dimensionality was used.

**Pruned sign theorem.** If β_I is at least ε on every retained support,
then the same coefficient lower bound follows. The complete identity holds
for the whole field; the support lemma puts every positive weight in the
retained set. Negative values on excluded supports are multiplied by zero.
Only the sign test is restricted, not the field or balanced sum.

For rank six, C is the cone of all 28 heights satisfying the 45 rhombi.
Its three-dimensional affine lineality is removed by fixing heights at
`(0,0), (1,0), (0,1)`. This leaves a pointed 25-dimensional cone. Its full
166-ray description gives an exact closure test: retain the rays tight on
S, then find all rows tight on every such ray. With no surviving ray the
face is the origin and every row is in the closure. The ray description
must be proved complete; an incomplete list could exclude a genuine face.

For nine independent interior normals, an exact nonzero kernel vector w
tests the rank condition: every closure row must be orthogonal to w.
Every physical branch is tested. The six barycentric permutations preserve
the entire row system, lattice, metric and cone, making this predicate
invariant under the same group as the field.

## 4. The exact finite premises

The local scalar α_N is computed from `Λ = N Z^10`, the complete numerator
`Λ intersect product_i [0,d_i)`, and metric `Q = (N N^T)^(-1)`. The complete
generating function is

$$S(c)=\frac{\sum_{p\in\Lambda\cap\prod_i[0,d_i)}e^{\langle c,p\rangle}}
{\prod_i(1-e^{d_i c_i})}.$$

Its BV constant is the degree-zero multivariate holomorphic projection.
The [manuscript](../../papers/rank-six/rank-six.tex) derives a finite Bernoulli
formula and a terminating metric-projection recurrence, and gives an
independent forward Euler–Maclaurin calculation. It also proves the exact
odd-dimensional proper-subset formula with the finite-character defect when
the all-ones vector is absent from the full image lattice. At q=9 every
surviving defect character has at most six coordinate poles. Full image
lattices and phase data are indispensable; Gram/index equality alone is
insufficient for type reuse.

For the orbit-averaged c1–c5 fields the stored convention is

$$\beta_I=\alpha_I+\frac{B_I n}{6D}.$$

Every group element and stabilizer is included. The c6 field lists 381 literal
support functionals directly and has no additional factor of six. Saturation
is certified by an integer left inverse with the expected rank, or by full
rank and gcd one of all maximal minors. Every primitive correction is rebuilt
from original normals and compared with any stored sparse operator.

| Coefficient | Complete sign domain | Uniform bound |
| --- | ---: | ---: |
| c1 | 13,325,662 retained nine-normal orbit rows | 1/2,000,000 |
| c2 | 10,480,218 eight-normal orbit rows | 1/200,000,000 |
| c3 | 2,999,563 seven-normal orbit rows | 1/200,000,000 |
| c4 | 675,721 six-normal orbit rows | 1/2,000,000 |
| c5 | 121,241 five-normal orbit rows | 1/2,000,000 |
| c6 | 102,297 literal four-normal supports | 1/3,000 |
| c7 | 10,994 literal three-normal supports | 1/144 |
| c8 | 849 literal two-normal supports | 1/9 |
| c9 | 42 literal one-normal supports | 1/2 |

For c1, the all-support domain is 27,230,728 orbit rows. The closure test
visits 46,327,714 branches and retains the stated rows, representing
79,940,357 literal independent parents. The exact minimum is

$$\frac{40142888690844119591010700379369}
{40149066134252712057708583296000000000}>\frac1{2\,000\,000}.$$

The field has 20,960,436 integer coordinates, with `D = 10^10` and actual
denominator `6 × 10^10`. Its original-action check covers 119,963,492
primitive incidences. Negative excluded values are preserved as controls.

Completeness of the large domains is constructive. Every independent
eight-support extends an independent deleted seven-face; every independent
nine-support extends an independent deleted eight-face. Enumerate every
absent normal at the preceding complete level, test independence in its
saturated kernel, and canonicalize by the six actions. Verify every extension
is present, every listed parent is independent and canonical, all joins are
bijective, and the weighted incidence counts agree. Counts alone are not
substituted for those object-wise checks.

For c2–c6, every independent support is constrained, so no realizability
pruning is needed. For q1–q3 every raw scalar is already positive; two distinct
exact implementations agree on all 42, 849 and 10,994 independent supports,
including nonunimodular image numerators. The dependent complements have
sizes 0, 12 and 486. This replaces the inherited top-four computational
premise with a small rank-six-specific verification, while crediting the
earlier rank-uniform theorem as prior mathematics.

## 5. Assemble the whole polynomial

Apply the pruned sign theorem to c1 and the all-support correction identity
to c2–c6. Apply the latter with zero field to q1–q3, giving c9, c8 and c7.
All lower bounds use the same original saturated face lattices. Every
nonempty polytope of dimension at least k has an actual k-face with positive
normalized volume. The ten-dimensional leading coefficient is volume.

Consequently, once the complete listed finite predicates hold, **every
coefficient through the actual degree is strictly positive** for a nonempty
rank-at-most-six hive. Coefficients above actual degree vanish. Section 1
supplies constant one, point/empty conventions, padding and rational scaling.
No chamber-generic assumption, sampled boundary panel or hidden-dimensional
transfer by continuity is needed.

The complete exact finite checks and mathematical review are recorded in the
[verification guide](VERIFYING.md) and its linked execution records. The result's
scope is ordinary rank at most six.
It does not prove unrestricted KTT, positivity for arbitrary formal polytopes,
monotonicity, concavity, or an explicit positive tableau formula.

[Verification and costs](VERIFYING.md) · [Contribution map](CONTRIBUTIONS.md) ·
[Formalization obligations](FORMALIZATION.md)
