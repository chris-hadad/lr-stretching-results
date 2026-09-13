# All-size rank-six positivity under the complete five-coordinate criterion

This computer-assisted theorem has a complete finite rational certificate and independent exact checks. External independent verification, worldwide priority, positivity of all actual quintics, all rank-six positivity, and full KTT are not claimed.

## Statement and exact domain

Let b=(lambda,mu,nu) be balanced nonnegative integral partitions, with lambda OUTER and maximum trimmed length at most six. Pad to six parts. Apply the complete zero-boundary-gap closure and integral coordinate-identification reduction, optionally after one of the twelve exact invariant-tensor count symmetries. If the resulting complete hive presentation has at most five selected integer coordinates, every ordinary coefficient of

    P_b(t)=c^(t lambda)_(t mu,t nu)

is nonnegative at every size. Empty fibers give the zero polynomial. A nonempty actual quintic has six strictly positive ordinary coefficients. Every nonempty fiber in any of the 125 certified five-coordinate representative closed domains is strictly positive through its actual degree, including its hidden-dimensional walls. The umbrella at-most-five statement is conservatively nonnegative on all previously inherited lower-coordinate positivity criteria.

The sufficient coordinate bound is not the actual affine dimension. A failure of this criterion does not imply actual degree greater than five, infeasibility or an ordinary-negative coefficient. No universal codegree or reflection premise is used.

## Complete original model and saturated lattice

Use the conventional six-part hive:

    h(i,0)=sum_(j<=i) mu_j,
    h(0,j)=sum_(i<=j) lambda_i,
    h(6-j,j)=|mu|+sum_(i<=j) nu_i.

All 45 triangular-grid rhombi and every boundary-only consistency row are present. The complete source mask certificate starts from prescribed zero adjacent partition gaps, propagates forced zero rhombus slacks, and eliminates with integral unit pivots. Each old interior coordinate is exactly

    h_i=t O_i(b)+x_sigma(i), or h_i=t O_i(b),

where O_i is integral and the inverse selects the surviving ORIGINAL hive coordinates. This is a bijection on the entire real polytope and on all lattice points at every nonnegative integer stretch, not a selected-support face. The ambient reduced lattice is Z^m. In a hidden stratum its actual affine lattice is the intersection with the true affine hull. LR stretching polynomiality and degree equal to actual dimension are previously established complete-object premises, not inferred from a fit.

The 15 mask bits, low to high, encode the five lambda, five mu and five nu zero gaps. A representative's domain is CLOSED: specified gaps vanish, other partition gaps and last parts remain nonnegative. Further equalities therefore remain inside the certified domain.

The complete source mask scores are pinned to the original file
methods/frontier-025-2026-09-10/science/results/F025-MASK-R6-001.json,
SHA -256 6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0.
Their original exhaustive closure proof remains an previously established source premise. The construction and independent verifier reconstruct every current representative and every original rhombus; they are not described as regenerating the historical 32768-mask closure computation.

## Exact finite coverage, without a feasibility census

There are 1275 source exact-five-coordinate masks, in 125 residual orbits under the complete invariant-tensor actions. The preceding two-domain theorem certified representatives 43 and 45, accounting for 24 exact patterns. The present theorem certifies every other 123 orbit, accounting for 1251 exact patterns. All representatives, member masks, integral maps, whole boundary-linear rows, sequential implication certificates and strict integer witnesses are in DATA/J01-COMPLETE-BOUNDARY-ROSTER.json. A witness proves that its displayed parent is a genuine quintic; it does not replace the all-boundary implications.

The independent action sweep examines all 32768 masks. It gives 30338 masks already meeting the at-most-four criterion and 1275 additional symmetry-minimum-five masks, for 31613 covered and 1155 outside this sufficient criterion. DATA/J09-SCOPE.json retains the entire remaining list, and DATA/J09-ALL-MASK-WORDS.json.gz retains every mask's exact action word. These numbers count GAP PATTERNS, not feasible hives, actual-degree populations, distinct polynomials, proportions of LR triples or cases in the original bounded domain.

The actions permute (mu,nu,-reverse(lambda)), allow simultaneous duality, and determinant-normalize the two selected inner weights. They preserve the entire invariant multiplicity at all stretches. This is not Ferrers conjugation and does not assert affine lattice equivalence of conventional hives. Only the full polynomial and actual degree, not an unproved geometric metric, are transferred.

## Full affine reduction precedes the cone certificate

For each representative, write every row as r_i(b,x)>=0. Remove it only with an exact identity

    r_i = sum_(j still retained, j!=i) y_j r_j
          +sum_a z_a g_a(b)+sum_l v_l e_l(b),

where y_j,z_a are nonnegative rational, g_a are permitted partition inequalities, and e_l are required zero gaps and the trace equality. The identity holds in ALL 23 boundary/chart coordinates. Removals are sequential and never use a row already deleted; recursively, all old constraints remain implied. Neither a normal-only dependence nor a sampled slack equality suffices.

The 123 new representatives have 5535 complete original-rhombus occurrences and 2638 complete implication steps. The all-125 construction includes the 41 previously certified steps. The remaining presentations are not asserted to be irredundant at every boundary; they are exact sufficient presentations for the same entire polytope and lattice.

All retained primitive normals have positive and negative coordinate masses at most two. The explicit new list in fact has squared norms at most four; the inherited squared-norm-at-most-six theorem is sufficient below. The identity maps and mass/norm claims are checked independently by the independent verifier; eliminating arbitrary linear coordinates would not justify this bound.

## Complete coefficient compensation

In each representative's single standard metric on Z^5, compute the complete transverse BV constants alpha_I for EVERY independent normal quadruple I. The projected primal quotient lattice, or equivalently saturated normal-plane lattice, is used; normal generators are never treated as tangent rays. Let M_J be an integral saturated kernel basis of an independent normal triple J. Its rank is two. The primitive quotient conormal for I=J union {n} is

    u_(I/J)=primitive(M_J^T n),

with the gcd of all restricted coordinates divided out. Choose rational linear forms h_J and define

    alpha'_I=alpha_I+sum_(J facet of I) h_J(u_(I/J)).       (1)

Every independent quadruple is constrained, including originally positive cones changed by any correction. Across all new presentations there are 559253 complete quadruple occurrences, including 9254 negative original constants. All corrected values are strictly positive. The exact global minimum is

    118146761/6756750000000 > 1/60000,

attained in the mask1330 array. The 398551 primitive correction incidences are stored individually, with complete kernel bases and rational coefficients. The real optimizer only proposed values; rounding to denominator 10^9 was followed by exact rational verification of every value. No tolerance decides a sign. Missing supports have coefficient zero.

The complete refined-normal-cycle theorem applies to ANY actual fan defined by one of these final normal lists, including nonsimplicial cones and hidden affine equalities. Briefly, choose a compatible pointed simplicial refinement using the same normal rays. Assign each top-dimensional subdivision cell of an actual k-face's normal cone the ORIGINAL face's lattice volume; assign other cells zero. For every refinement facet tau these weights satisfy

    sum_(sigma contains tau) w_sigma u_(sigma/tau)=0.      (2)

This is full lattice-normalized facet balance, including internal subdivision cancellation. The BV dual solid valuation gives c_k=sum w_sigma alpha_sigma. Inserting (1) and using (2) gives c_k=sum w_sigma alpha'_sigma. Thus

    c1 >= (1/60000) sum_(actual edges F) length_Z(F)>0.    (3)

All 147779 independent normal TRIPLES are already positive, with minimum 1/144, so no c2 correction is needed:

    c2 >= (1/144) sum_(actual two-faces F) area_Z(F)>0.    (4)

These are complete sums in one representative chart and metric. They do not claim that each original complete local c1 weight is positive. [Complete actual hive compensation and a period-one boundary falsifier](030-COMPLETE-FAN-AND-PERIODIC-BOUNDARY-CHALLENGES.md) gives a legal actual edge whose complete original constant is -1/1800.

## Hidden dimensions, rational vertices and higher coefficients

For rational P with polynomial lattice count, clear all vertex denominators by a positive integral dilation. Then c_k and every k-face lattice volume scale by the same positive kth power. The complete coefficient formula and inequalities transfer back. For hidden affine strata, the original actual lattice is retained; the nonpointed-fan argument supplies (2) without asserting continuity of perturbed Ehrhart coefficients. An outward perturbation is used only to obtain a compatible fan; all weights are ORIGINAL face volumes.

In actual dimension five, the previously established complete indexed short-normal theorem supplies c3>0, and leading/next-leading positivity gives c5,c4>0. In dimension four, (3),(4) supply c1,c2 and the top two are intrinsic. In dimension three, (3) supplies c1 and the top two are intrinsic. Dimensions one and two, nonempty points and empty fibers have their stated intrinsic conventions. Hence the whole polynomial is positive through actual degree on every one of the 125 certified five-coordinate closed domains. The old complete at-most-four theorem and rank-at-most-five theorem complete the umbrella criterion.

No nonnegative h-star, full reflection, unique-first-interior shortcut, or coordinate-bound-as-degree fit is used. Period-one is essential: [Complete actual hive compensation and a period-one boundary falsifier](030-COMPLETE-FAN-AND-PERIODIC-BOUNDARY-CHALLENGES.md) gives complete rational polytopes in these retained directions with negative quasipolynomial constituent coefficients.

## Independent finite and whole-object verification

[Exact cone-lattice compression and complete independent verification](029-EXACT-LATTICE-ISOMETRIES-AND-FINITE-CERTIFICATE.md) gives the exact lattice-isometric compression and independent complete Laurent checks. All 4790 stored types, 68188 proper-face quotient occurrences and 72090 fundamental-point occurrences pass; every new subset binding, affine implication, primitive incidence and rational corrected value passes. These are complete finite proofs, not estimates from a positive sample.

Four new entire LR parents have 32 matching whole-hive/literal-LR sites and 24 matching coefficients, with two unused positive checks each. Their actual degree five and codegree one were fixed by explicit complete strict integer witnesses before fitting. Independent Newton reconstruction agrees with primary Lagrange reconstruction. The four vectors are distinct. Two of these parents also have complete original/corrected edge sums matching their independent LR c1, with 447 complete primitive balance equations. Their purpose is to challenge the geometric theorem and full LR bridge, not to infer all-size signs from four vectors.

No new identification with original area-thirty cases is supplied; the previously established coverage remains4554. The 1155 patterns outside this criterion, rank-seven five-coordinate classes, actual quartics/quintics with larger coordinate bounds, and higher-rank signs remain open at their stated scopes.

## Source and certificate locations

The prior premises are the complete hive-coordinate reduction, invariant-tensor symmetries, and short-normal positivity theorem. The complete analytic argument is given in [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md), with its primary Berline–Vergne references. The earlier two-orbit certificate is retained in HISTORY/P07-A01/DATA/J04-NORMAL-CYCLE-CERTIFICATE.json. The new finite certificates are indexed by DATA/FINAL-CERTIFICATE-INDEX.json, cone types by DATA/FINAL-TYPE-INDEX.json, and independent checks by DATA/J05-VERIFICATION.json, DATA/J06-VERIFICATION.json and DATA/J07-VERIFICATION.json. EXPORT-MANIFEST.json records their exact hashes and sizes. [Exact cone-lattice compression and complete independent verification](029-EXACT-LATTICE-ISOMETRIES-AND-FINITE-CERTIFICATE.md) describes the scope of reproduction, and [Complete actual hive compensation and a period-one boundary falsifier](030-COMPLETE-FAN-AND-PERIODIC-BOUNDARY-CHALLENGES.md) gives the counterexamples to broader extensions.

