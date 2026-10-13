# A64: paying two simultaneously active residual caps

Curated mathematical proof from **A64**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

27 September 2026. Root derivation.  No active provider theorem is a premise. The accepted A58 complete C22 character/count bridge, A63 full unequal-budget subset identity and A63 one-small-cap theorem are used at their exact scopes. No worldwide novelty claim.

## 1. Complete original and statement

Let 4 <= a <= 8, let r >= s >= 0 with r > 0, and let


```text
0 <= x <= y <= r,   k_3,...,k_a >= r,
K=x+y+sum_(i=3)^a k_i,   P=K-r,   Q=K-s,   H=P+Q.
```

All final data are integral. Use physical row widths (u1,v1,x,y,k_3,...,k_a,u2,v2), with the four paired widths at least H. Only the first and last adjacent overlaps are nonzero, respectively P and Q. Construct upwards by lambda_n=w_n, mu_n=0, mu_i=lambda_(i+1)-e_i, lambda_i=mu_i+w_i, and set nu=(sum w_i-2H,H,H), lambda OUTER. The partition, containment and trace conditions follow from the overlap floors. The positive final paired row makes the physical rank a+4. Extra isolated zero rows may be inserted under the accepted complete count identity; they do not create extra positive caps.

The ENTIRE original has polynomial


```text
C(k;r,s;t)=sum (Pt-U+1)(Qt-V+1),
u_i,v_i >= 0,  u_i+v_i <= k_i t,
U=sum u_i <= Pt,  V=sum v_i <= Qt.                 (1)
```

Both paired determinants, all Weyl partners and once-only shifts belong to the accepted A58 proof of (1). The two weights count two slack compositions. Eliminating one slack per budget leaves the saturated count lattice Z^(2m+2), where m is the number of positive caps. Since K >= (a-2)r >= 2r, both budgets are positive and r+s <= K. Small positive free coordinates and strict slacks give a relative interior, so actual degree is 2m+2. Thus the degree is 2a+2 when x>0, 2a when x=0<y, and 2a-2 when x=y=0. Physical zero rows are retained; no hive metric or local-weight isometry is inferred.

**Proposed theorem.** Every ordinary coefficient of this entire original through its actual degree is strictly positive. At fixed y, other caps and deficits, increasing x from x0 to x1 with 0 <= x0 < x1 <= y has whole coefficientwise gain strictly positive in degrees 1,...,2a+2 and zero constant. BOTH budgets increase by x1-x0. Hold all four paired widths at any legal final H floor, so every intermediate original is legal. By symmetry of the complete count, any two small caps can be reordered to choose the smaller one for this operation.

Together with A63 for zero or one small cap, this signs the complete C22 family with a=4,...,8 positive caps and at most two caps below d=max(r,s)>0, arbitrary unequal deficits and parameter magnitudes, plus its stated zero-row boundaries. It is a family result at physical ranks 8 through 12 before extra zero-row insertion, not whole rank eight, arbitrary-a payment, low-budget joint tails or unrestricted KTT. The operation theorem is for growth of the smaller cap only; no unrestricted cap-growth or fixed-budget splitting law is claimed.

## 2. Full singleton and pair correction

Use scaled variables X=xt, Y=yt, R=rt, S=st and scaled cap values. Put b(z)=(z+1)(z+2)/2, N=product b(k_i t),


```text
L=5Kt/4-R-S,
A=(2Kt/3-R)(2Kt/3-S)-sum_i(k_i t)^2/36.
```

For h equal to R or S and the other scaled budget W equal to Kt-S or Kt-R, respectively, let J be a subset of the two distinguished caps with total M_J<h. Write q=|J|, z=h-M_J+2a-2q-1, and e_l for the elementary polynomial in (cap+2), cap in J. Then


```text
T_J(h,W)=sum_(j=0)^q e_(q-j)
  [(2+W-h/2) binom(z,2a-q+j+1)+binom(z,2a-q+j+2)],

C=N(1+L+A)+sum_(J:M_J<R)(-1)^|J|T_J(R,Kt-S)
             +sum_(J:M_J<S)(-1)^|J|T_J(S,Kt-R).     (2)
```

Every binomial is its rational falling-product polynomial. Empty residual ranges are zero. A large cap cannot enter a residual subset because it is at least R; the complete roster is therefore empty, X, Y, XY, with exactly the indicated threshold tests. This is a specialization of the full accepted A63 identity, not a truncation of an arbitrary-cap identity. In particular, both pair intersections are retained when active. The budget tails are disjoint because r+s<=K. The identity also holds when x or y is zero by the same finite residual inclusion-exclusion, or by cancellation of its zero-cap factors; the physical original remains unchanged.

For q<=2 and a>=4, at a subset wall M_J=h the binomial top is the nonnegative integer 2a-2q-1, below every lower index. Thus that whole term vanishes. Adjacent polynomial pieces agree exactly at all walls, including simultaneous walls. Their derivatives need not agree. At S=0 the entire S correction is zero.

## 3. An exhaustive eight-cone parameter cover

It suffices to work on 0<=X<=Y<=R, 0<=S<=R. These are parameter cones, not hive cones. The following inverses give nonnegative coordinates u,v,w,z throughout each indicated region and reconstruct the original X,Y,R,S exactly. They prove coverage and preserve the parameter integer lattice without any relaxation.

| Cone | Region beyond 0<=X<=Y<=R and 0<=S<=R | Inverse (u,v,w,z) | Active R subsets | Active S subsets |
| --- | --- | --- | --- | --- |
| A1 | X+Y<=R, S<=X | (S, X-S, Y-X, R-X-Y) | X,Y,XY | none |
| A2 | X+Y<=R, X<=S<=Y | (X, S-X, Y-S, R-X-Y) | X,Y,XY | X |
| A3 | X+Y<=R, Y<=S<=X+Y | (S-Y, X+Y-S, Y-X, R-X-Y) | X,Y,XY | X,Y |
| A4 | X+Y<=S<=R | (X, Y-X, S-X-Y, R-S) | X,Y,XY | X,Y,XY |
| B1a | R<=X+Y, S<=R-Y | (S, R-Y-S, X+Y-R, Y-X) | X,Y | none |
| B1b | R<=X+Y, R-Y<=S<=X | (R-Y, S-R+Y, X-S, Y-X) | X,Y | none |
| B2 | R<=X+Y, X<=S<=Y | (X+Y-R, R-Y, S-X, Y-S) | X,Y | X |
| B3 | R<=X+Y, Y<=S<=R | (X+Y-R, S-Y, R-S, Y-X) | X,Y | X,Y |

The empty subset is always included; equality terms in the displayed active rosters vanish, so closed cones are legitimate. Each row is an integral inverse of its forward map. The independent verifier checks determinant plus or minus one and the exact inverse. For R>=X+Y the four positions of S give A1-A4. For R<=X+Y put q=R-Y in [0,X]; the two subdivisions of S<=X and the two remaining S intervals give B1a-B3. This exhausts the domain, including ties and zeros.

## 4. All higher large-cap excess degrees are paid analytically

Write the large caps as R+Z_i, i=3,...,a, Z_i>=0. Every correction term in (2) is at most affine in the entire excess vector, because its only excess dependence is through W. Differentiating at fixed Y,R,S,Z_i retains that property. Thus excess degree at least two comes entirely from the unrestricted derivative


```text
b(Y) product_(i>=3)b(R+Z_i)
   [ b'(X)(1+L+A)+b(X)(5/4+A_X) ],
A_X=[16Kt-12(R+S)-X]/18.                         (3)
```

Let G=R-S>=0 and W0=X+Y+sum Z_i. Then


```text
L=5X/4+5Y/4+(5a-18)R/4+G+5 sum Z_i/4,
A=[(2a-7)R/3+2W0/3]^2
    +[(2a-7)R/3+2W0/3]G
    -[X^2+Y^2+(a-2)R^2+2R sum Z_i+sum Z_i^2]/36.
```

For a>=4, the R^2 coefficient is [4(2a-7)^2-(a-2)]/36>0. Each X^2,Y^2,Z_i^2 coefficient is 5/12; distinct W0 mixed coefficients are 8/9; R X and R Y have coefficient 4(2a-7)/9; R Z_i has coefficient (16a-57)/18>0; R G and W0 G have coefficients (2a-7)/3 and 2/3. These list every term of A. All coefficients of L and A_X are nonnegative: A_X has R coefficient (16a-56)/18, X coefficient 5/6, Y and each Z_i coefficient 8/9, and G coefficient 2/3. Every factor of (3) is therefore coefficientwise nonnegative.

In each of the eight maps, X,Y,R and G=R-S are nonnegative linear forms in u,v,w,z. Consequently the analytic payment remains coefficientwise nonnegative after every chamber substitution. It covers ALL large-cap excess monomials of total degree at least two, at arbitrary a>=4. It is not a numerical check at equal caps.

## 5. The remaining complete finite identities and strictness

Only total excess degrees zero and one remain. The large caps are symmetric, so a single representative excess Z suffices: caps (X,Y,R,...,R,R+Z), with a-3 unmodified R slots. For every a=4,5,6,7,8 and all eight cones, the producer differentiates the complete expression (2) with respect to X while holding Y,R,S and the large caps fixed, then substitutes the cone map. It records every nonzero rational coefficient in (u,v,w,z,Z), (the JSON names the last variable E), with exact-zero domain total degree at most 2a+1 and Z degree at most one. There are 40 full polynomial identities and 204,336 declared coefficient slots, including zeros.

The independent checker constructs (2) AFTER cone substitution, computes the exact inverse map and applies the first inverse column as a differential operator. It imports no producer code. It must match every coefficient, including every implicit zero, and establish nonnegativity. The high-excess proof in Section 4 remains a separate analytic obligation.

Strictness uses the pure powers of every coordinate occurring in X. These are u,v for A1/A3/B2; u for A2/A4; and u,v,w for B1a/B1b/B3. The checker must certify each of these pure coefficients is strictly positive in every parameter degree 0,...,2a+1. This is 1,190 required supports over the full 40-identity domain. When x>0, at least one such coordinate is positive. Returning to unscaled parameters, dC/dx=t*(partial C/partial X), so every ordinary coefficient in degrees 1,...,2a+2 is strictly positive. The constant derivative is zero.

The complete coefficient functions are continuous across all subset walls by Section 2. Integrating the positive one-sided derivatives from x0 to x1, splitting at the finitely many walls if necessary, proves the stated full gain. The four paired widths can remain at their final legal floor throughout; no forbidden variation of a physical row is hidden in the argument.

At x=0, the factor h_0=1 removes one cap from the COUNT only. There remain a-1 slots, with one arbitrary cap y and all others >=r. A63's complete one-small-cap theorem applies because 3<=a-1<=7. Its own zero base covers y=0 as well. Hence the starting entire original is strict through its actual degree. The proved gain pays every higher new degree when x>0. Reverse decrease of the smaller positive cap terminates at this paid zero-cap base. For zero/one active cap in the positive-a formulation, use the already accepted A63 theorem directly. The r=0 no-tail case is already paid by A62 and is not obtained by dividing by r.

## 6. Verification and exact remaining boundary

The complete certificates, independent reconstructions and strict supports are necessary finite proof data. Named complete originals must additionally compare the full subset formula with an independently written rectangular convolution at every determining grade and two unused grades, retain actual degrees and zero physical rows, and test the complete gains. Selected bare-original counts check the accepted character/count bridge at the new literal witnesses; incomplete high-grade bare runs must remain explicit limits. Missing-pair, missing-singleton, wrong-shift, fixed-budget, zero/tie, empty/negative-domain and legal-width controls are required. Prospective full-domain costs and hard runtime exits remain separate evidence.
