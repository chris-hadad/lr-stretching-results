# The eleventh ordinary coefficient at every rank-seven LR boundary

For every balanced triple b=(lambda,mu,nu) of nonnegative integral partitions, with lambda outer and maximum trimmed length at most seven, the entire stretching polynomial P_b(t)=c^(t lambda)_(t mu, t nu) satisfies c11(b)>=0. It is strictly positive when the whole hive is nonempty and its actual affine dimension is at least eleven; below degree eleven or in an empty family it is zero. No area, boundary gap, coordinate-reduction, codegree or reflection restriction is imposed.

In the ORIGINAL fifteen-coordinate hive with its single standard scalar product, the stronger inequality is

    c11(b) >= (1/3000) sum_(actual eleven-faces F) vol_Z(F).    (1)

The measure is normalized by the actual saturated face lattice, with a fundamental parallelepiped of volume one, not by multiplying that measure by 11!. This is a whole-coefficient theorem, not ordinary positivity of every rank-seven polynomial, not full KTT, and not an additional result in the original bounded domain. The original box's c11 was already known to be nonnegative; the new conclusion is all-size and all-boundary.

## Entire unreduced model and exact coefficient index

Pad all partitions to seven parts. For 0<=i,j, i+j<=7 put

    h(i,0)=sum_(a<=i) mu_a,
    h(0,j)=sum_(a<=j) lambda_a,
    h(7-j,j)=|mu|+sum_(a<=j) nu_a.

Use all 63 original elementary rhombi, obtuse-corner sum minus acute-corner sum >=0. The interior variables h(i,j), i,j>0, i+j<7, are in lexicographic order and form the saturated ambient lattice Z^15. Hidden affine strata use its intersection with the true affine hull. The ordinary hive/LR identity, period collapse, and actual-degree=affine-dimension premise are the prior source facts.

There are 60 distinct primitive inward directions N. The cone calculation deduplicates only DIRECTIONS. It deletes no original inequality or boundary constant. DATA/ATLAS-R7.json retains all 63 original coordinate rows and every direction. Its inherited outward atlas comparison has one simultaneous sign reversal of the full list, not a sign reversal of individual cone generators. The independent verifier regenerates every original rhombus from the canonical triangular grid.

Eleven-faces have codimension four in ambient15. A correction facet of their normal cones has rank three, so its primitive conormal quotient has rank 12. The previously successful rank-six quotient has rank 7 and is not substituted for it.

## Complete rational finite certificate

Every four-subset of N is enumerated: 487635 total,462468 independent and 25167 dependent. The full literal list, normal-generator indices, original complete constants and every type-binding word survive in DATA/R7-FULL-RAW.json.gz. All 132 negative original local occurrences are saved before correction in R7-NEGATIVE-LOCAL.jsonl. These are complete abstract simplicial cones; no whole LR coefficient or actual-face realization follows just from their signs.

For every independent quadruple I, alpha_I is the complete zero-vertex transverse Berline--Vergne constant in the SATURATED normal plane, equivalently the projected primal quotient with the induced dual metric. The full half-open fundamental numerator, every proper-face quotient, all required Laurent jets and cancellation of every negative pole are retained. Normal generators are not treated as tangent generators.

For each selected independent triple J, let M_J be an integral 15-by 12 column basis of its complete saturated kernel. If I=J union{n}, set

    u_(I/J)=primitive(M_J^T n) in Z^12.

Primitive normalization divides the gcd of ALL twelve coordinates. Choose a rational linear form h_J on this quotient and define

    alpha'_I=alpha_I+sum_(J facet I) h_J(u_(I/J)).             (2)

There are 381 support triples and 4572 scalar variables. All 20925 primitive incidences are retained. EVERY independent quadruple is constrained, including every originally positive cone affected by a nonzero h. Missing supports carry the zero functional. The complete rounded rational certificate has minimum

    164999998979/491400000000000 > 1/3000.                    (3)

The real optimization was only a proposal. Rounding to denominator10^12 was followed by exact rational verification of every inequality; no floating tolerance establishes (3). The full supports, saturated bases, incidences, functionals and original/corrected values are in R7-FULL-INCIDENCE.json.gz and R7-FULL-CORRECTION.json.gz.

The target consists of 6238 exact lattice/metric cone types. Twelve extra types are calibration-only. Equal permuted Gram matrices are used only when the row-generated normal lattice is saturated. At higher index, an explicit signed AMBIENT coordinate permutation and generator permutation identify the entire integer embedding; equal Gram and equal index alone remain invalid. The complete type index preserves every numerator and every isometry word.

## Complete global compensation, including hidden strata

Apply the dimension-independent complete refined-normal-cycle theorem in [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md), with m=15, k=11 and q=4. Choose a compatible pointed simplicial refinement of the ACTUAL normal fan using the same normal rays. It exists also when that normal fan has lineality. A generic outward perturbation may construct the fan, but its Ehrhart polynomial is not used and its coefficients are not assumed to converge.

Each refined four-cone sigma receives the ORIGINAL normalized volume of an actual eleven-face when it subdivides that face's normal cone, and otherwise receives zero. For every three-cone tau in the common refinement, the complete face-volume weights obey

    sum_(sigma contains tau) w_sigma u_(sigma/tau)=0          (4)

in its actual saturated rank 12 quotient. At a genuine twelve-face this is lattice-normalized facet balance. At an internal subdivision face equal weights multiply opposite primitive quotient directions. In higher-dimensional coarse-cone interiors the relevant weights vanish. These cases cover all hidden affine strata and all nonsimplicial cones.

The Berline--Vergne dual SOLID valuation and ambient/subspace compatibility give

    c11(P)=sum_sigma w_sigma alpha_sigma.

Insert (2), interchange finite sums, and apply (4). Every correction cancels in the entire weighted coefficient sum. Thus

    c11(P)=sum_sigma w_sigma alpha'_sigma
           >= (1/3000) sum_sigma w_sigma
           >= (1/3000) sum_(actual eleven-faces F) vol_Z(F).

Every weight is nonnegative; every actual eleven-face has a nonempty top-dimensional normal subdivision. When actual dimension is eleven, the whole polytope is itself its eleven-face; below eleven the sum and coefficient vanish.

For a rational hive, choose a positive integer dilation clearing all vertices. LR period collapse gives P(Qt), and both c11 and eleven-face lattice volumes scale by Q^11. This transfers the inequality back. It does not follow for arbitrary quasipolynomial constituents; the complete periodic counterexamples remain active exceptions to that broader statement. Empty LR families are identically zero and are never fitted through a special zero-grade value.

## Independent verification, controls and limits

The independent SymPy/Hermite-normal-form Laurent verifier replays both disjoint, exhaustive parity shards of DATA/TYPE-INDEX.json. It uses neither the primary Fraction elimination nor its finite-group coset construction. A separate all-atlas verifier independently regenerates the full grid, every independent/dependent subset, every lattice-isometry binding, kernel saturation, primitive incidence and exact corrected sign. Exact counts and completion records are in DATA/J04-TYPES-VERIFIED.json, J05-TYPES-VERIFIED.json and J06B-ATLAS-VERIFIED.json; the final report does not replace those finite certificate bodies.

[A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md) supplies an actual full stable source--sink hive model and its lattice inverse; [Complete eleven-face volumes and a genuine rank-seven LR count](036-COMPLETE-ELEVEN-FACE-CHALLENGE.md) evaluates every 3571 eleven-face and every 933 twelve-face balance at its rank-seven unit member. The complete face sum is22483/179625600. A separate literal LR reconstruction and reverse-pulling volume calculation challenge both the all-stretch polynomial and every normalized face volume. These are controls of the new complete coefficient theorem, not a new all-rank source--sink positivity theorem.

Combining (1) with the previously established ambient top-four protection gives c11,...,c15>=0 at every ordinary rank-at-most-seven boundary. The remaining possible negative indices at rank seven are

    1 <= j <= min(actual_degree-2,10),

subject to every other exact positivity criterion established in this collection. The rank-six c6 theorem remains separately valid. The lower ten rank-seven coefficients, whole-rank ordinary positivity, full KTT and the original finite-box endpoint are not settled by this coefficient theorem. No new identification with original bounded-domain cases is supplied; coverage4554 is unchanged.

Analytic source: Berline and Vergne, Local Euler--Maclaurin formula for polytopes, `arXiv:math/0507256v3`, Propositions13/14, Definition22, Corollary23 and Theorem26. The selected primary statements supply the analytic premises. No new analytic theorem, external independent verification, or worldwide novelty is claimed for these finite certificates.

The complete independent verification covers6250 types,94443 fundamental-lattice-point occurrences and 93672 proper-face quotient occurrences. An initial atlas check stopped while evaluating exact zero minors and produced no complete verdict. Exact Gram-rank and zero-column pruning then allowed a separate check to complete every atlas and incidence comparison. [Full quotient supports, exact local isometries, and a legal release failure](037-TWELVE-COMPONENT-AND-RELEASE-CHALLENGES.md) gives the argument supporting that pruning.
