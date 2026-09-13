# FRD / WI-268 and WI-270: two coupled-simplex hive models

These are worker-produced proofs and certificates, pending independent review
and root adoption. They establish two full lattice-count identities on the
exact represented closed cones. They make no maximal-chamber, whole-fan,
whole-box or additive coverage claim.

## 1. Exact sources and complete geometry

`source-manifest.json` authenticates precisely the two records named in
FRC/FRD-inputs.json at lab commit
`5763f356748ea5f2813b288e680d288c81537ae4`:

| ID | Raw source | SHA256 |
|---|---|---|
| `04b974e74c9d1358` | `sessions/2026-09-03-S1960-phase1-d/computations/r6-mp200-rng36-seed-0.json` | `3fefe94b4b1b16e6e967294740e857f06b9d3fad11735b6de952c30c8f19bbf7` |
| `b54e0912e4e93806` | `sessions/2026-09-03-S1960-phase1-d/computations/r6-mp200-rng36-seed-9.json` | `313d5e50f5a339cec27143654cfb87fa7cc5a8573a74774925a4028ea22ba247` |

Write the balanced boundary vector as
`beta=(lambda1,...,lambda6,mu1,...,mu6,nu1,...,nu6)`, with lambda outer.
The independently frozen campaign constructor gives all45 inequalities
`A h+B beta>=0` in10 interior hive coordinates. Its separately written
specialized and symbolic constructions agree exactly at each seed.
PPL independently enumerates the complete bounded10-dimensional seed hives:
48 and32 vertices. All vertices are simple, and their complete tight signatures
agree with the authenticated source records. No native recognition code is
imported or executed.

Let R have the17 stored rays as its rows. They are independent, integral,
primitive, legal balanced partition triples. The stored H-cone is homogeneous,
with equation rank1 and span equal to `ker(equation)`. Every H-inequality
pulls back along `beta=R^T s` to a nonnegative linear form in s, and every
coordinate halfspace `s_i>=0` occurs up to a positive factor. Thus the H-cone
equals `R^T R_{≥0}^{17}`. Both seeds have all17 ray coordinates strictly
positive. For each complete seed tight set I, the checker forms
`V_I=-A_I^{-1}B_I`. All45 rows of `(A V_I+B)R^T` are nonnegative for every
one of the48/32 maps. These61,200 comparisons establish all these vertex maps
throughout the represented cone.

## 2. Integer coordinates and the coupled models

The respective ten-row bases are

```
I48 = [0,9,13,17,27,30,34,37,39,41]
I32 = [0,1,6,9,16,19,21,26,29,35].
```

Set `M=A_I`, `D=B_I`, `q=M h+D beta`. The determinants are respectively-1
and+1, and both inverse matrices are integral. Consequently this is a
saturated integer-lattice bijection for every integral beta, with inverse
`h=M^{-1}(q-D beta)`. All45 raw slacks become `Tq+C beta`, where
`T=A M^{-1}` and `C=B-TD`. Every transformed row is included in the
geometry certificates. In particular, the ten basis rows give `q_i>=0`.

For model48 use `a=s14`, `b=s15`, `w=s16`; for model32 use `a=s15`, `w=s16`.
The active parameters are integral boundary forms on the balanced span:

| Model | Parameter | Integral boundary form |
|---|---|---|
|48|a|`nu5-nu6`|
|48|b|`mu2+nu2-lambda1`|
|48|w|`mu1+mu3+nu1+nu3-lambda2-lambda3`|
|32|a|`lambda3+lambda5-mu1-mu6-nu2-nu6`|
|32|w|`lambda1+lambda2-mu2-mu3-nu4-nu5`|

The checker verifies these forms on all17 independent rays, and also provides
integer forms obtained directly from the transformed raw rows. Thus integral
beta implies integral active parameters, even if other real ray coordinates
are nonintegral. All active parameters are nonnegative on the closed cone.

The model inequalities, in addition to every `q_i>=0`, are exactly:

| Model | Block | Raw row and total |
|---|---|---|
|48|base7-simplex|row44: `q0+q2+q3+q5+q6+q8+q9<=w`|
|48|independent interval|row22: `q1<=a`|
|48|coupled2-simplex|row43: `q4+q7<=b+q0+q2`|
|32|base7-simplex|row31: `q0+q1+q4+q5+q6+q7+q8<=w`|
|32|coupled3-simplex|row44: `q2+q3+q9<=a+q0+q1+q5+q8`|

There is an implicit eighth nonnegative base coordinate making the base total
equal w. The two nontrivial simplex blocks in each model are disjoint; model48
also retains an interval of the previous grammar. Each later total is affine,
nonnegative, and depends only on represented earlier coordinates and parameters.

## 3. Complete corner generation and all raw slacks

Here is the extension of the affine interval-generation argument. Suppose
`P=conv(v_i)` and L is affine and nonnegative on P. For
`Q={(x,y):x in P, y_j>=0, sum_j y_j<=L(x)}`, write
`x=sum_i alpha_i v_i`. If `L(x)>0`, set `theta_j=y_j/L(x)` and
`theta_0=1-sum_j theta_j`. Then

`(x,y)=sum_i sum_j alpha_i theta_j (v_i,L(v_i)e_j)`,

where `e_0=0`. These coefficients are nonnegative and sum to1. If `L(x)=0`,
then y=0 and every positively weighted L(v_i) is zero, so the same statement
holds using only j=0. Thus the successive simplex corners generate all of Q,
also on zero-total faces. Iterate this lemma through the displayed blocks.

It gives exactly `8*2*3=48` symbolic corners for model48 and `8*4=32` for
model32. Every corner is homogeneous linear in the boundary ray coordinates.
At the strict seed, the full generated corner set equals the full PPL vertex
set; every corner's tight set is one of the complete seed tight sets, each
occurring exactly once. Its linear map agrees with the tight-set solution on
all17 independent domain generators. This supplies complete seed normal-fan
coverage and identifies all symbolic maps, without claiming completeness of a
fan in boundary-parameter space.

The model inequalities are raw hive rows, so the hive H lies in the model Q.
The certificates include every raw slack at every symbolic corner and domain
ray:36,720 comparisons for model48 and24,480 for model32, all nonnegative.
Hence every model corner lies in H throughout the closed cone. By the
generation lemma, Q lies in H, and H=Q. Together with the unimodular map this
proves the entire lattice model; seed agreement or fitted counts are not premises.

## 4. Full lattice sums

Put `C7(w)=binomial(w+7,7)`. A base lattice point is a weak composition U of
w into eight parts. If X is the sum of r specified parts, differentiating
`(1-yz)^(-r)(1-z)^(-(8-r))` j times in y at y=1 proves

```
sum_{|U|=w} binomial(X,j)
 = binomial(r+j-1,j) [z^(w-j)] (1-z)^(-8-j),
E[binomial(X,j)]
 = (r rising j)/(8 rising j) * (w falling j)/j!.
```

These coefficient identities hold for every integral w>=0, including w<j
when the falling product is zero. The Vandermonde polynomial identity

`binomial(a+X+f,f)=sum_{j=0}^f binomial(a+f,f-j) binomial(X,j)`

then performs the entire inner simplex sum. The checker verifies the polynomial
identity and the resulting exact moment expansion. This is finite summation,
with no degree interpolation or sample-fit identification.

For model48, `r=2`, `f=2`, and the interval contributes a+1. The full count is

```
E48(a,b,w) = (a+1) C7(w)
            * (12b^2+36b+24+6bw+11w+w^2)/24.
```

For model32, `r=4`, `f=3`. The full count is

```
E32(a,w) = C7(w)
          * (6a^3+36a^2+66a+36+9a^2w+40aw+41w+5aw^2+12w^2+w^3)/36.
```

Both are ordinary LR count identities for every integral boundary in their
proved closed cones, by the hive/LR correspondence and the lattice bijection.
They remain valid on every face, including zero parameters. For an integer
stretch t, substitute all active parameters by t times themselves.

Every coefficient of the displayed residual polynomials is positive, as are
all coefficients of `C7(w)=prod_{i=1}^7(w+i)/7!`. Therefore the complete
parameter polynomials have nonnegative coefficients:54 and38 nonzero
monomials, respectively, all strictly positive. The full degree is10.
`results/count-*.json` lists every ordinary stretching coefficient as a
homogeneous parameter form for degrees0 through10, explicitly inspects all
open rank-six mixed degrees1 through6, and checks that these are exactly the
coefficients of the directly substituted t-polynomial. Missing monomials are
zero. No mixed-negative term and no ordinary-negative evaluation occurs.
No stability or root-location claim is made.

The old native L/Q and fitted c3 through c6 arrays are compared only after
these complete proofs, as corroboration. Their earlier fit/runtime provenance
is not promoted. Eight independent fresh bare-LR controls agree, four per model:

| Model | Parameter tuples | Exact LR values |
|---|---|---|
|48|`(0,0,1),(1,1,1),(0,0,2),(1,1,0)`|`12,60,75,6`|
|32|`(0,1),(1,1),(0,2),(1,0)`|`20,56,174,4`|

The first four controls, alternating the two models' first two listed tuples,
were completed and checked before releasing the remaining four. These are
value controls only, with no extra coefficient-coverage increment.

## 5. Exact relevance to the size-30 box

Every domain ray has nonnegative outer size. The active rays give the bounds

`|lambda|>=18a+21b+33w` for model48,
`|lambda|>=28a+59w` for model32.

Since the active parameters are nonnegative integers, inside `|lambda|<=30`
model48 permits only `(a,b,w)=(0,0,0),(1,0,0),(0,1,0)`. Its stretching
polynomials are respectively1, t+1, and `binomial(t+2,2)`, of degree at most2.
Model32 permits only `(a,w)=(0,0),(1,0)`, giving1 and `binomial(t+3,3)`, of
degree at most3. The primitive-ray and exact active-tuple supplement is
`results/targeted-tests-and-box.json`. These are statements within the two
represented cones and imply no whole-box enumeration or additive coverage.

## 6. Verification and scope disposition

The full theorem premises are the frozen exact hive construction and standard
hive/LR correspondence, membership in the proved stored closed H-cone, and an
integral legal balanced boundary for lattice counting. All remaining geometric,
lattice, corner-generation and finite-summation steps are supplied here and in
the executable certificate verifier. The root's independent moment derivation
is `../root-count-check.md`.

The sole expected failed premise is a synthetic test: an intentionally altered
base total depending on an unrepresented coordinate is refused by the actual
geometry callback and retained as `fixture-unmet-premise.json`. It is not a
science partial. Synthetic negative mixed forms remain separate from ordinary
witness claims. The actual contained adapter refuses a mismatched source hash
before acquiring a child. The adapter and its containment dependency are exact
copies of the reviewed FRC/native/revision-003 sources; their finalization and
cancellation semantics are unchanged. All science attempts have distinct frozen
source/configuration identities and verified exits. No geometry route failed,
no model control or LAB009 attempt was used, and no promising route is retired.

`REVIEW-MANIFEST.json` freezes the review surface. `verify_archive.py` performs
read-only source/output/receipt joins and budget checks; it does not rerun a
scientific attempt. Frozen attempt configurations document the exact executed
commands. Replay must use fresh output and attempt identities, and a new
contained resource allocation; historical attempts are immutable.
