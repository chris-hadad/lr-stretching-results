# Two complete all-size five-coordinate LR domains

Let lambda, mu, nu be balanced nonnegative integral partitions, with lambda outer, padded to six parts. Every ordinary coefficient of the entire stretched LR polynomial is nonnegative if either of the following complete boundary conditions holds:

    A: lambda1=lambda2=lambda3, lambda4=lambda5, mu1=mu2;
    B: lambda1=lambda2, lambda3=lambda4=lambda5, mu1=mu2.

All unlisted partition gaps and last parts may be arbitrary nonnegative integers. Additional equality walls, all hidden dimensions and empty fibers are included. Nonempty members have actual degree at most five, and every coefficient through their ACTUAL degree is strictly positive. The claim also transfers under the source's full invariant-tensor symmetries, giving 24 exact zero-gap patterns plus their closed equality walls.

This is not all rank six, not all actual quintics, not all five-coordinate masks, not a whole original-box certificate, and not external independent verification or worldwide novelty. The complete rank-six five-coordinate selector contains 125 residual orbits / 1,275 exact masks; this theorem certifies two orbits / 24 exact patterns. The other 123 orbits / 1,251 exact masks remain untreated here, not proved negative or infeasible.

## Complete hive map, retained inequalities and lattice

Use the inherited complete conventional hive with

    h(i,0)=mu1+...+mu_i,
    h(0,j)=lambda1+...+lambda_j,
    h(6-j,j)=|mu|+nu1+...+nu_j.

All 45 rhombus inequalities are present. The source zero-gap closure and integral coordinate-identification map express each old interior coordinate as O_i b+x_sigma(i), or O_i b, where b=(lambda,mu,nu). The inverse selects the five surviving original coordinates. At stretch t substitute tb. This is a full real/integer bijection to the entire hive, in the saturated ambient lattice Z^5; no face or selected-support model replaces it. All boundary-only consistency rows remain. The actual affine lattice in a hidden stratum is its intersection with the actual affine hull, not a guessed full five-dimensional lattice.

The four required zero gaps are masks 43 and 45 in the convention: low five bits are lambda gaps, next five mu gaps, last five nu gaps. The complete fixed-mask closure leaves five selected coordinates in both cases. Every boundary-linear row and the full integral map are frozen in DATA/J02-BOUNDARY-PILOT.json, and independently rebuilt from the original triangular-grid rhombi by the independent verifier.

The two complete closed domains each permit exact sequential implication reduction to a 22-normal presentation. There are respectively 20 and 21 removals. Every removed FULL row is a nonnegative rational sum of still-retained rhombi and legal partition inequalities, plus a rational sum of the four required zero gaps and trace equality. The identities hold in all 23 boundary/chart coordinates. They preserve the whole polytope and lattice at every legal boundary, including further equality walls. A normal-only dependence without its boundary term is insufficient. The finite source mask and integer-elimination theorem remains an prior premise; no original global census is newly regenerated.

## Complete normal-cycle certificates

Use ONE standard scalar product on each representative Z^5 chart. The full normal sets and the exact correction arrays are in DATA/J04-NORMAL-CYCLE-CERTIFICATE.json. For c2, enumerate every independent three-subset: 1,374 at mask43 and 1,363 at mask45. All their complete BV constants are positive, minimum 1/144, so no correction is needed.

For c1, enumerate EVERY independent four-subset: 5,348 at mask43 and 5,180 at mask45. Their original lists contain 103 and 71 negative complete abstract local cones respectively. All original values are saved before attempting a correction. Each is a complete simplicial cone; most are not asserted to be realized at a hive face. One is independently co-realized as a negative complete edge cone in the size 60 mask45 parent below.

Choose as correction supports the independent triple facets of the nonpositive four-cones. On each support retain the full saturated rank-two kernel basis. For every independent four-cone, including all positive affected cones, restrict its extra normal to that kernel and divide its gcd to obtain the primitive quotient conormal. The full rational solution to (1) of [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md) gives

    mask43: 269 nonzero supports,
            every corrected alpha >=672453/350000000;
    mask45: 197 nonzero supports,
            every corrected alpha >=15624979/9000000000.

The optimization engine proposed bounded real coefficients. They were converted to rationals with denominator 10^9, and every single corrected value was checked exactly; the positive margins above are rational results, not floating tolerances. All 7,334 nonzero-support incidence occurrences, including affected original positive cones, are retained. A missing support has coefficient zero. No separately chosen metric at individual faces or deletion of an inconvenient positive constraint is used.

Apply [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md)'s complete refined-normal-cycle theorem. For every actual edge in either representative,

    c1 >= epsilon_mask sum_F length_Z(F)>0,

and for every actual two-dimensional face,

    c2 >= (1/144) sum_F area_Z(F)>0,

whenever the actual dimension is at least the respective coefficient index. These are complete face sums with one compatible normal-fan refinement. Individual complete edge weights can remain negative before the global correction; positivity is not an assertion that boundary row deletion alone fixes them.

In actual dimension five, every primitive retained normal is an identification of an original rhombus normal, hence has positive and negative mass at most two and squared norm at most six. The previously established complete indexed short-normal theorem protects c3. The leading and next-leading coefficients c5,c4 are intrinsically positive. With c0=1, all six coefficients are positive.

In actual dimension four, the normal-cycle certificate still controls c1,c2, and c3,c4 are intrinsic. In dimension three it controls c1 while the other nonconstant coefficients are intrinsic (and c2 is also certified). Dimensions one and two follow intrinsically, and a nonempty point gives one. Empty LR families have the zero positive-stretch polynomial; the separate validated scalar t=0 convention is not used to fit them through one. [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md) supplies the actual affine-lattice and nonpointed-fan argument, rather than assuming that the coordinate bound equals degree.

## Exact transfer and domain coverage

Write the invariant tensor weights as (mu,nu,-reverse(lambda)). Permuting these three weights, simultaneously dualizing them, and then determinant-normalizing the two selected inner weights preserves the complete invariant multiplicity at EVERY stretch. The resulting count is again an ordinary LR polynomial after the admissible normalization. This is not Ferrers conjugation, and it does not assert an affine isomorphism between the conventional hives.

On gap masks the action reverses the outer gap word, permutes the three invariant words, optionally reverses all three, and reverses the selected new outer word back. DATA/J10-COMPLETE-MASK-WORDS.json independently binds each of the 24 exact patterns to 43 or 45 by an explicit word. Any further zero gaps satisfy the closed representative conditions as well. Metric/face-length interpretations stay with the representative chart; only the entire polynomial and its degree are transported by the count symmetry.

## Numerical certification and independent scope

The independent verifier uses neither the primary optimizer nor its lattice/evaluation functions. It independently regenerates every original rhombus, checks the full integral chart and all 41 sequential implications, reconstructs all subset bindings and verifies every primitive quotient incidence and corrected value.

For saturated normal-generator lattices, equality of the permuted Gram matrix gives a full lattice/metric cone isometry. This compression is used ONLY at index one. At higher index the literal normal embedding, saturated plane basis, primitive polar rays and complete fundamental numerator are retained. Equal index and Gram alone are not substituted for that information.

The independent exact evaluator uses SymPy rational matrices and Hermite-normal-form representatives of every half-open fundamental parallelepiped, in place of the primary Fraction elimination and finite-group BFS. It replays all 2,571 types, 36,157 proper-face quotient occurrences and 39,669 fundamental-point occurrences, including all jets needed by each transverse-face subtraction. It verifies every negative Laurent pole cancels and every stored complete constant agrees. All 13,265 cone occurrences and all 7,334 correction incidences pass.

Four whole degree-five parent records have 32 independently matched full-chart/literal-LR scalar sites, 24 matching ordinary coefficients and eight unused positive checks. Each determining space is fixed by an exact strict lattice witness before fitting. Three distinct polynomials occur among the four records; one two-member nonhomothetic boundary test has unchanged counts. The complete edge calculation separately verifies the full corrected normalized edge sum against the uncorrected sum and independent vector in both original parents, with 673 complete primitive balance checks. The hidden-fan calculation tests the hidden-fan argument on a full integral abstract quartic; it is a NON-LR control, not another LR member.

The analytic and short-normal premises are precisely those listed in [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md) and SOURCES/INDEX.json. These are independent implementations and complete counting models within this study; external independent review is not claimed. No new identification with original area-thirty cases has been made; the previously established coverage remains 4,554.
