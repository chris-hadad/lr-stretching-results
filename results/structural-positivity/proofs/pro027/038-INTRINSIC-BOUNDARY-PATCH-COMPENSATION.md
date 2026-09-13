# Intrinsic boundary-patch compensation in complete hive atlases

The result gives a geometric representation of the complete normal-cycle correction supported on local coordinate patches. It does not establish a new coefficient index beyond the rank-six c6 and rank-seven c11 theorems. The exact certificate uses the A02 arrays; an earlier serialization contained floating-point contamination and is not used.

## Whole objects and inherited premises

Use lambda outer and balanced nonnegative integral partitions, padded to n=6 or 7. In the original hive chart the coordinates are h(i,j), i,j>0, i+j<n, in lexicographic order. The three fixed boundaries are prefix mu on (i,0), prefix lambda on (0,j), and |mu| plus prefix nu on (n-j,j). Every original rhombus and its boundary-dependent constant remains: 45 at n6 and 63 at n7. The ambient coordinate lattices are Z10 and Z15. Actual dimension can be smaller; its affine counting lattice is the intersection with the true affine hull. The entire hive/LR identity, stretching polynomiality, and degree=actual dimension remain the prior premises. Empty families have the zero polynomial. No universal codegree is assumed.

The complete refined-normal-cycle theorem, given in [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md), applies to any fixed normal list in any ambient dimension. Correcting all independent codimension-four cones by primitive quotient facet functionals leaves the entire face-volume coefficient sum invariant, including compatible subdivisions, hidden affine strata and integral-denominator clearing under period one. This is not a correction of a selected star alone.

## A basis-free local functional and its exact divisor

For an independent triple J of primitive normal rows, put

    S_J = union of the nonzero coordinate positions of its three rows.

Choose a rational ambient vector v_J supported on S_J and satisfying J v_J=0. It defines a linear functional on the saturated normal quotient, independent of the arbitrary coordinates of a kernel basis. For an extra normal n independent of J, put

    a_J = gcd of all maximal 3-minors of J,
    a_I = gcd of all maximal 4-minors of I=J union{n},
    g_J(n)=a_I/a_J.                                      (1)

If M_J is ANY integral basis matrix of the complete saturated kernel, then

    g_J(n)=gcd(M_J^T n).                                  (2)

Here the gcd is positive. To prove it, let A be the row-generated rank-three lattice, Abar its saturation, and B=A+Z n. Set C=Abar+Z n. Since n is independent of span A, [C:B]=[Abar:A]=a_J. The image of n in the free quotient Z^m/Abar has divisibility g; hence [Bbar:C]=g and a_I=a_J g. Restriction of integer covectors to the saturated kernel is surjective and has kernel Abar, so its coordinates M_J^T n have the same divisibility. This proves both identities without an assumed unimodular normal tuple.

The local correction is therefore

    delta_J(n) = (v_J dot n)/g_J(n).                     (3)

Since v_J lies in the rational span of M_J, it equals M_J h_J for a rational vector h_J and (3) is exactly h_J evaluated on the PRIMITIVE quotient conormal. A local basis need only span the rational solution space; it is not substituted for the integer counting lattice used in (1)–(2).

## Initial support-local certificates

On each complete original rank-six/rank-seven atlas, the 381 selected triple facets of the 132 negative quadruples have coordinate supports of sizes 3,4,5,6 and local kernel dimensions 0,1,2,3. Their local parameter spaces have 567 scalar dimensions each, rather than the unrestricted2667 and 4572 quotient parameters. Fresh proposals succeeded on every 102297 and 462468 independent quadruple, respectively, including every affected positive cone.

The full rational functionals are unchanged by the exact-arithmetic repair. The corrected minima in DATA/R6-PATCH0-EXACT-A02.json.gz and R7-PATCH0-EXACT-A02.json.gz are respectively

    99725274317/297000000000000,
    186037499191529/554053500000000000.

Those first two are exact re-evaluations; the stronger shared certificate below receives a separate independent complete replay.

## The shared boundary-aware rule

Normalize a support patch by subtracting its minimum i and minimum j coordinates. Retain the sorted three signed normal rows in those positions and THREE BOOLEAN FLAGS recording whether any support position satisfies respectively

    i=1, j=1, i+j=n-1.                                  (4)

These are the sides of the interior-coordinate triangle, not arbitrary entries of M_J. The triple's directed triangular geometry and its flags define its template. No independent sign changes or arbitrary coordinate isometries are used to identify these geometric templates.

The union of the two complete selected triple lists has 399 templates and 621 rational scalar parameters. The complete dictionary is DATA/BOUNDARY-PATCH-SYSTEM.json.gz; DATA/BOUNDARY-PATCH-FUNCTIONALS.json gives its vectors. At any rank, the proposed rule assigns the template vector to EVERY matching independent normal triple, and zero to other triples. The independent verifier enumerates every triple at ranks 6 and 7 and checks that exactly381 match at each rank; no additional unexamined matching support receives a hidden correction.

On EVERY independent quadruple of BOTH original atlases, the resulting complete corrected value is strictly positive. The common exact minimum is

    epsilon=102306547/304687500000 > 1/3000.               (5)

All 564765 quadruple occurrences and 34992 primitive incidence occurrences are retained and independently checked. The passing arrays are DATA/BOUNDARY-PATCH-R6-EXACT-A02.json.gz and its R7 analogue. Every originally negative and positive affected constraint is included. The original BV constants themselves are unchanged.

By the inherited complete normal-cycle theorem, this one boundary-aware rule proves

    c6 >= epsilon sum_(actual six-faces) vol_Z(F), n=6,
    c11>= epsilon sum_(actual eleven-faces) vol_Z(F),n=7.   (6)

The volume of a saturated lattice fundamental parallelepiped is one; no factorial is inserted. The inequalities hold also in hidden strata. The coefficient is zero below its index, strictly positive for a nonempty hive of sufficient actual dimension, and zero for an empty family. Period-one denominator clearing is essential. These strengthen the REPRESENTATION of the previous coefficient results; they are not new whole-rank positivity theorems.

## Complete aggregate check and independence

The independent verifier rederives template bindings, rational kernel constraints, every matching triple, all 564765 corrected signs, and every 34992 index-ratio/primitive-kernel agreement. It imports neither the optimizer nor the primary parameterization. The old complete BV Laurent values and their lattice verification remain explicit inherited premises, not a new replay of all historical type bodies.

On the stable n7,M=s1 whole parent, every 3571 original eleven-face contribution is recomputed with the NEW boundary-patch correction. Both sums remain

    c11=22483/179625600.

The original complete normalized face volumes and whole polynomial were already independently verified in [Complete eleven-face volumes and a genuine rank-seven LR count](036-COMPLETE-ELEVEN-FACE-CHALLENGE.md); their reuse is a full aggregate challenge, not a new vector or independent recount. DATA/J10-INDEPENDENT-PATCH-FACE-SUM.json.gz saves every new weighted change. No new bare-LR scalar or entire vector is claimed here.
