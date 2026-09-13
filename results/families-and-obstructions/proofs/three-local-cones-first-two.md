# Exact lattice geometry of two fixed rank-six cones

Date: 2026-09-04. This is a mathematical certificate from the frozen raw hive system and two fixed sets of recorded rays. It proves the two proposed full count identities on those two closed cones. It uses neither fitted coefficient forms nor any LR count as a premise. The independent reproduction and review record is summarized at the end.

## 1. Domain and source identities

For each `rng` in `{32,33}`, let `C_rng` be the nonnegative real span of the seventeen rays in the corresponding frozen JSON record. All seventeen vectors are reproduced in [the two-cone certificate](../data/local-cones/first-two.json), together with the seed boundary and source hash.

- Source commit: `4d8ab55b8e885e2bc676fa7172cd91f897f7aa26`.
- Record directory: `sessions/2026-09-03-S1959-phase1-c/computations/`.
- `r6-mp200-rng32-seed-0.json`: SHA-256 `5924494e568c3eac72e183eda048ebee6cd971041d8ce841131cadd16bdab644`; chamber identifier `3103fe3d0905e0a2aff0f4548e1eae8272d87ff901888888837353ddf29eed39`.
- `r6-mp200-rng33-seed-0.json`: SHA-256 `7ed6eec15e2d2aa3d442d50be985cfd76b783d3ec48df805788dc9fb385495cc`; chamber identifier `e696628ff86a1ce2048f731e90fd6ab8120385a81fe395d56f3c56fa70c900a7`.
- Target commit: `719311618110024e72c2a3f0000b06e7367381f5`.
- Target constructor: `code/ehrhart/src/slr_ehrhart/hive.py`, SHA-256 `8797f8e2662fd9ba9b4f7e0b9e29d7831e96f4a0d15e86841b348278e588392a`.

The original checker obtains the constructor bytes through `git show` at the
specified commit, checks their hash, and loads them into an in-memory module. The source was inspected before use. Only its pure `hive_linear_system`, `hive_system`, and interior-coordinate construction execute; Sage functions, random generators, evaluator code, and lab code do not execute. The two pure hive constructions agree row by row on each exact fixed seed.

All row and ray indices below are **zero-based**. Boundary components `lambda_i, mu_i, nu_i` use the usual **one-based** partition indices and length-six padding. Let

\[
 b=(\lambda_1,\ldots,\lambda_6,\mu_1,\ldots,\mu_6,\nu_1,\ldots,\nu_6),
 \qquad \ell_i(h,b)=A_i h+B_i b.
\]

The raw hive is defined by all 45 inequalities `ell_i >= 0`. Its free-coordinate order is

\[
(h_{11},h_{12},h_{13},h_{14},h_{21},h_{22},h_{23},h_{31},h_{32},h_{41}).
\]

The JSON contains the complete selected normal matrix `M`, its integer inverse, the selected boundary matrix `D`, and every transformed row `T_i,C_i`, with

\[
 q=Mh+Db,\qquad h=M^{-1}(q-Db),\qquad
 \ell_i=T_iq+C_i b,
 \quad T_i=A_iM^{-1},\quad C_i=B_i-T_iD.
\]

These matrices specify the maps completely and allow reconstruction of all raw rows. Their determinants are respectively `+1` and `-1`, so these are affine bijections of the standard integer lattice for **every integral boundary**.

## 2. The stored cone inequalities have exactly the asserted domain

This point does not rely on the stored `simplicial`, `seed_in_cone`, or `cone_dim` flags. In both records, exact rational algebra verifies:

1. The seventeen rays have rank seventeen; each ray is a balanced triple of nonnegative weakly decreasing partitions.
2. The homogeneous cone equation matrix has rank one and annihilates every ray. Thus the ray span equals its seventeen-dimensional kernel.
3. Every stored cone inequality, pulled back to the seventeen ray coordinates, has nonnegative coefficients.
4. For each ray coordinate `s_j`, at least one pulled-back inequality is a positive multiple of `s_j >= 0`. The JSON gives its row index and multiplier.

Every vector satisfying the equation therefore has unique ray coordinates. Items 3 and 4 show that it satisfies the stored cone inequalities **if and only if** all those coordinates are nonnegative. Thus `C_rng` also equals the cone described by the stored homogeneous H-representation. This proves equality for these two represented cones; it does not prove they are maximal chambers or that they cover any other part of the hive fan.

## 3. First map: `rng32` is an integral GT factor times a simplex

Take the slack-coordinate basis

\[
q=(u_6,u_8,u_9,u_{11},u_{12},u_{25},u_{35},p,q_0,r)
 =(\ell_6,\ell_8,\ell_9,\ell_{11},\ell_{12},\ell_{25},\ell_{35},\ell_{19},\ell_{21},\ell_{30}).
\]

Its normal matrix has determinant `+1`. The simplex normals span rank seven, the remaining six facet normals span rank three, their combined rank is ten, and their rational subspaces intersect trivially. The determinant certifies a lattice direct product as well as rational separation.

Define the following integer boundary-linear forms:

\[
\begin{aligned}
x&=\nu_3-\nu_4,\\
y&=\nu_4-\nu_5,\\
z&=-\lambda_1-\lambda_4-\lambda_5-\lambda_6
 +\mu_1+\mu_3+\mu_4+\mu_5
 +\nu_1+\nu_3+\nu_4+\nu_5.
\end{aligned}
\]

Their values on the seventeen rays are exactly `x(r_j)=delta_(j,14)`, `y(r_j)=delta_(j,15)`, `z(r_j)=delta_(j,16)`. At the stored seed they are `(3,3,1)`.

The eight simplex facet slacks are the seven coordinates `u_i` and

\[
\ell_{44}=z-\sum_{i\in\{6,8,9,11,12,25,35\}}u_i.
\]

The other six facet slacks are exactly

\[
\ell_{19}=p,\quad \ell_{21}=q_0,\quad \ell_{30}=r,\quad
\ell_{31}=p+q_0+r-y,\quad \ell_{32}=y-q_0,\quad
\ell_{39}=x+y-p-q_0-r.
\]

These are exact matrix identities in the boundary vector, not solely identities at sampled points. Make the further integral change

\[
a=p+q_0+r-y,\quad b_0=q_0-y,\quad c=p+q_0-y;
\qquad
p=c-b_0,\quad q_0=b_0+y,\quad r=a-c.
\]

It has determinant of absolute value one. The fourteen selected inequalities become

\[
u_i\ge0,\quad \sum_i u_i\le z,
\qquad 0\le a\le x,\quad -y\le b_0\le0,\quad b_0\le c\le a.
\]

This is precisely a seven-dimensional standard dilated simplex and a three-dimensional GT polytope, with the product lattice. Sections 5 and 6 prove that the other 31 raw hive inequalities add no restrictions anywhere on `C_32`.

Consequently, for **every integral boundary in `C_32`**,

\[
\begin{aligned}
\#H(b)&=\binom{z+7}{7}
 \sum_{a=0}^{x}\sum_{b_0=-y}^{0}(a-b_0+1)\\
&=\boxed{\frac{(x+1)(y+1)(x+y+2)}2\binom{z+7}{7}}.
\end{aligned}
\]

Zero parameter values are included. This is a full count formula, not an inference from agreement through degree six.

## 4. Second map: `rng33` is a rectangle bundle over a simplex

Take the slack-coordinate basis

\[
q=(u_6,u_8,u_{11},u_{16},u_{19},u_{24},u_{39},u_{43},a,b_0)
=(\ell_6,\ell_8,\ell_{11},\ell_{16},\ell_{19},\ell_{24},\ell_{39},\ell_{43},\ell_4,\ell_{37}).
\]

Its normal matrix has determinant `-1`. The nine simplex normals span rank eight; the four rectangle-facet normals span rank four; their intersection has rank two and the combined rank is ten. Thus a rational direct product of these normal subspaces would be the wrong assertion. The displayed unimodular map instead gives the affine rectangle widths below.

The parameter forms are

\[
\begin{aligned}
x&=\lambda_5-\mu_5-\nu_3,\\
y&=-\lambda_3+\mu_3+\nu_4,\\
z&=-\lambda_1-\lambda_4-\lambda_5
 +\mu_1+\mu_4+\mu_5+\nu_1+\nu_2+\nu_3.
\end{aligned}
\]

Again their ray values are exactly the coordinate functions `s14,s15,s16`; at the seed they are `(10,5,1)`. They are integers on every integral boundary in the real cone.

Put `u44=z-sum(u6,u8,u11,u16,u19,u24,u39,u43)`. The thirteen selected inequalities become

\[
 u_i\ge0\ (i\in J),\quad \sum_{i\in J}u_i=z,
 \qquad
0\le a\le y+A(u),\quad 0\le b_0\le x+B(u),
\]

where

\[
J=\{6,8,11,16,19,24,39,43,44\},\qquad
A=u_{16}+u_{19}+u_{24},\qquad B=u_8+u_{19}+u_{39}.
\]

Each support has size three and their intersection is `{19}`. In particular,

\[
\ell_{32}=y+A-a,\qquad \ell_{41}=x+B-b_0.
\]

Sections 5 and 6 prove that the remaining 32 raw hive inequalities are redundant on `C_33`.

For nonnegative integer `z`, let `N=binom(z+8,8)` be the number of weak compositions among these nine coordinates. Symmetry or the elementary generating functions give

\[
\frac{1}{N}\sum u_i=\frac z9,\qquad
\frac{1}{N}\sum u_i u_j=\frac{z(z-1)}{90}\ (i\ne j),\qquad
\frac{1}{N}\sum u_i^2=\frac{z(z+4)}{45}.
\]

For example the generating functions for the two quadratic sums are `t^2/(1-t)^11` and `t(1+t)/(1-t)^11`; coefficient extraction proves these formulas, including `z=0`. There are eight distinct-index products and one equal-index product in `AB`, hence

\[
\frac1N\sum A=\frac1N\sum B=\frac z3,
\qquad
\frac1N\sum AB
=8\frac{z(z-1)}{90}+\frac{z(z+4)}{45}=\frac{z^2}{9}.
\]

Summing the integral rectangle fiber counts therefore gives, for **every integral boundary in `C_33`**,

\[
\#H(b)=\sum_{u}(y+A(u)+1)(x+B(u)+1)
=\boxed{\left(x+1+\frac z3\right)\left(y+1+\frac z3\right)\binom{z+8}{8}}.
\]

Although its factor notation uses thirds, this expression counts integral points; it is not a claim that either fractional factor separately counts a lattice interval.

## 5. Completeness of the canonical vertex lists, including degenerations

For `rng32`, the GT factor's vertices are among

\[
a\in\{0,x\},\quad b_0\in\{-y,0\},\quad c\in\{b_0,a\}.
\]

For positive `x,y`, these are seven distinct points because the two choices at `a=b_0=0` coincide. A vertex must have `c` at an endpoint unless that interval has collapsed, and on each endpoint sheet the `(a,b_0)` domain is a rectangle. Thus this list generates the GT factor; degeneration of either rectangle side preserves the same convex-hull statement. Taking the product with the eight simplex vertices gives 56 symbolic vertex maps, with possible collisions on parameter boundaries.

For `rng33`, use the nine simplex corners `u=z e_i`, and at each choose each of the two interval endpoints independently. These 36 symbolic points generate the whole rectangle bundle. Indeed write any base point as a convex combination `u=sum lambda_i z e_i`. Both widths are nonnegative affine functions of `u`. If `a=alpha*(y+A(u))` and `b_0=beta*(x+B(u))`, with `alpha,beta` in `[0,1]` (choose zero when a width is zero), the corresponding fiber point is the same convex combination of points with fractions `alpha,beta` in the corner fibers. Each corner-fiber point is a convex combination of its four corners. For `z=0` the base is a single point and the statement is immediate. This proves the convex-hull description also when any parameter vanishes.

Every listed slack-coordinate vertex is homogeneous linear in `(x,y,z)`. Its inverse-image hive vertex is therefore homogeneous linear in the full boundary `b`.

## 6. Omitted inequalities are certified universally, not sampled

Let `Q(b)` be the polytope cut out by the fourteen or thirteen selected rows. Because those rows are among the raw hive rows, `H(b)` is contained in `Q(b)`. The exact transformed rows identify `Q(b)` with the corresponding bounded canonical model.

For every canonical symbolic vertex map `v(b)`, every raw inequality row `i`, and every one of the seventeen stored rays `r_j`, the script verifies

\[
\ell_i(v(r_j),r_j)\ge0.
\]

These are respectively **42,840** (`56*45*17`) and **27,540** (`36*45*17`) exact rational comparisons. The script independently checks each residual by both transformed rows and original rows. For an arbitrary `b=sum s_j r_j` with real `s_j>=0`, linearity now gives

\[
\ell_i(v(b),b)=\sum_j s_j\ell_i(v(r_j),r_j)\ge0.
\]

Every canonical vertex of `Q(b)` is therefore in `H(b)`. Section 5 proves these maps generate **all** of `Q(b)`, even on the closed-cone boundary, so `Q(b)` is contained in `H(b)`. This proves equality uniformly over the full real cone. Checking the seventeen rays is decisive here because these are linear residual identities at a complete explicit parametric vertex list; ordinary finite wall counts have no such implication.

As a separate diagnostic, the resulting exact active sets at the two seeds equal all stored signatures, with 56 and 36 distinct vertices respectively. Seed full dimension ten and the complete incident row sets are also checked. The proof of completeness uses the explicit models, not the stored signatures.

## 7. Direction ranks, lattice indices, and consequences

All first fourteen ray hives have direction dimension zero. Exact ranks from the certified ray vertex lists give:

| Ray subset | `rng32` | `rng33` |
|---|---:|---:|
| `{14}` | 2 | 1 |
| `{15}` | 2 | 1 |
| `{16}` | 7 | 10 |
| `{14,15}` | 3 | 2 |
| `{14,16}` | 9 | 10 |
| `{15,16}` | 9 | 10 |
| `{14,15,16}` | 10 | 10 |

These are dimensions of the sums of the indicated direction spaces, equivalently dimensions of the corresponding Minkowski sums; they are not inferred from fitted degrees. Thus the previously conditional 64-node support bound for `rng32` has its missing pair-rank certificate. The full identities now supply a stronger direct conclusion than interpolation on the 64/40 nodes.

For `rng33`, the primitive hive directions of rays 14 and 15 are respectively

```text
(0,0,0,0,0,0,0,1,0,0)
(0,1,1,1,0,0,0,0,0,0).
```

Both segments have lattice length one. The gcd of all two-by-two minors of their direction matrix is one, proving their rank-two lattice span is saturated. The selected slack matrix determinant also proves the base-plus-fiber lattice index is one.

Under stretching `b -> t*b`, the integer-linear parameters become `(t*x,t*y,t*z)`. Each full formula is a product of affine factors in `t` with nonnegative slopes and positive constants. Hence every coefficient is nonnegative; every nonconstant stretched specialization has only negative real roots. Zero slopes remove factors and reduce degree on boundary faces, so no fixed-degree stability claim is being made there. The same formulas explicitly provide nonnegative mixed coefficients in the active ray parameters.

These conclusions cover exactly `C_32` and `C_33`. They prove no maximality, no classification of other cones, no full rank-six fan coverage, and no universal KTT or Conjecture M/R statement. Extending to another cone requires a new certificate. The connection between the standard integer hive model and LR coefficients is the established hive correspondence; no additional empirical evaluator result is used.

## 8. Verification record

The independent reproduction compared its complete output bytes with the
retained certificate.

The script rejects optimized Python immediately because assertions are part of its checker. The invocation has a 120-second SIGALRM hard limit and 15-second subprocess limits for each fixed `git show`. It produces `TWO_EXPLICIT_UNIMODULAR_MODELS_VERIFIED_ON_FIXED_CLOSED_CONES` at exit zero. There are zero LR calls, zero Sage calls, zero new triples enumerated, and no lattice-point enumeration. Only the two named source JSON records and fixed target constructor are read.

Final replay of the recorded checker: **6.20 seconds wall time**, 6.09 seconds user CPU, 0.07 seconds system CPU, exit zero. The explicit `python3 -O` negative control exited one with the assertion-required message and created no output. A separate read verified that the JSON's recorded script hash equals the recorded script bytes. All recorded commands completed.

The direct identities do not require the earlier 64/40 scalar-count grids;
selected counts can still test an independent evaluator. Unexamined cones and
full fan coverage remain open.


## Independent verification

An independent calculation reproduced the checker with a separate output: exit 0, identical certificate bytes, 70,380 nonnegative raw checks and
both unimodular maps reproduced. An independent mathematical review of this complete proof, checker, data and
underlying hive constructor reported no findings. It included the general
rectangle-bundle argument. This review does not establish wider cone coverage.
