# Codimension-four compensation through ordinary rank twelve

This computer-assisted theorem has complete finite rational certificates and independently checked arithmetic and enumeration. It does not claim external independent verification, worldwide priority, whole-rank ordinary positivity, or full KTT.

## Whole-LR statement

For each integer n with 6<=n<=12, put D_n=(n-1)(n-2)/2 and k=D_n-4. Let lambda, mu, nu be balanced nonnegative integral partitions of maximum trimmed length at most n, with lambda OUTER. For the entire stretched LR polynomial

    P_b(t)=c^(t lambda)_(t mu,t nu)=sum_j c_j(b)t^j,

we have

    c_k(b) >= (1/3000) sum_(ALL actual k-faces F) vol_Z(F).       (1)

The chart is the ORIGINAL D_n-coordinate hive, in one standard coordinate metric. Volume gives a fundamental parallelepiped of the actual saturated face lattice volume one, not k!. If the family is empty, both sides are zero. If its actual degree is below k, both sides are zero. Otherwise c_k is strictly positive. No area, zero-gap, coordinate-reduction, codegree or reflection hypothesis is imposed.

The indices k at n=6,...,12 are 6,11,17,24,32,41,51. The first two are inherited whole-coefficient conclusions, now included in the same finite-patch certificate; the last five are the additional coefficient indices established here. Combining with the previously established ambient top-four source premise protects the five ambient highest coefficients c_(D_n-4),...,c_(D_n), at these ranks. It does not protect every lower coefficient, nor every actual-degree top-five index when actual degree is much smaller than the ambient dimension.

## Entire model, lattice and source premises

Interior coordinates are h(i,j), i,j>0 and i+j<n, in lexicographic order. Fix h(i,0)=sum_(a<=i)mu_a, h(0,j)=sum_(a<=j)lambda_a, and h(n-j,j)=|mu|+sum_(a<=j)nu_a. Retain ALL 3n(n-1)/2 original rhombus inequalities and their boundary constants. Deduplicating primitive directions for a cone list does not remove any original inequality.

The whole hive/LR correspondence, period-one stretching and degree equal to actual affine dimension are prior source premises. The ambient integer lattice is Z^(D_n); a hidden affine stratum uses its intersection with the actual affine hull. The complete refined-normal-cycle theorem ([Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md)) treats compatible subdivisions and hidden affine strata in this exact setting. It uses the ORIGINAL face-volume weights, never a coefficient limit of perturbed polytopes. Positive denominator clearing transfers (1) because LR period collapse gives P(Qt) and both sides scale by Q^k. The periodic-constituent counterexamples remain exceptions outside that premise.

The 399 geometric boundary-tagged templates and their exact rational functionals are inherited from [Intrinsic boundary-patch compensation in complete hive atlases](038-INTRINSIC-BOUNDARY-PATCH-COMPENSATION.md). Their literal source is HISTORY/P11-A01/DATA/BOUNDARY-PATCH-SYSTEM.json.gz and BOUNDARY-PATCH-FUNCTIONALS.json. For a supporting triple J, v_J is supported on its nonzero coordinate union and lies in ker J. The correction on an independent extra normal a is

    delta_J(a)=(v_J dot a)/g_J(a),
    g_J(a)=index(J union {a})/index(J).

[Intrinsic boundary-patch compensation in complete hive atlases](038-INTRINSIC-BOUNDARY-PATCH-COMPENSATION.md) establishes that this positive integer is exactly the gcd of the full restricted normal in any saturated quotient basis. The correction therefore represents a genuine linear functional evaluated on the PRIMITIVE quotient conormal. Missing templates have the zero functional. Every facet contribution, including every affected originally positive cone, stays in the sum.

## Criterion A: every smaller connected component

Connect normals when their NONZERO COORDINATE supports intersect. All connected independent q-tuples were checked at every possible rank through 2q+3 for q=1,2,3. The exact verified raw minima are respectively

    q=1: 1/2;     q=2: 1/9;     q=3: 1/144.                 (2)

There are 33,839 independent occurrences and 1,140 dependent constructors in the complete criterion-A record. Empty cases carry no sign claim; the empty q=3,n=3 file has a legacy q0 filename, explicitly normalized by the verifier's intended q=3 list.

The full-rhombus compression in [A finite rank horizon for the proposed all-rank patch rule](040-FINITE-RANK-PATCH-REDUCTION.md) proves that every connected q-tuple at arbitrary rank is represented within these horizons, preserving the entire lattice and metric embedding. Thus (2) holds at all ranks. Coordinate-disconnected cones are orthogonal lattice direct sums; their complete BV weights multiply. This is not a factorization based merely on a disconnected Gram matrix.

In particular an untouched disconnected independent quadruple has weight at least the minimum of 1/288,1/81,1/36,1/16, according to component sizes. All these bounds exceed 1/3000. Orthogonal multiplicativity is the scoped Berline--Vergne Proposition14(c) premise.

## Criterion C: every actually affected extension at arbitrary rank

For every rank 5<=n<=15, enumerate EVERY matching template triple J and every normal a outside J for which v_J dot a is nonzero. Take the union of the sorted quadruples. This is exactly the relevant nonzero individual-change set, not a sample of stars. Configurations are retained even if several individual corrections cancel in their sum. Excluding a zero dot product excludes only an identically zero individual contribution.

The complete finite set has 58,062 independent quadruple occurrences, with 73,752 checked facet-incidence occurrences. Rank 5 has no nonzero affected configuration. Rank 6 has 5,790, and each of ranks 7 through 15 has 5,808. Their fully corrected values are all positive, with minimum

    epsilon_patch = 102306547/304687500000 > 1/3000.        (3)

The current code obtains matching supports by translating every literal directed template over every admissible anchor, retaining all three boundary-touch flags. Every possible match has exactly such an anchor. The independent replay rebuilds the atlas from adjacent elementary triangles and checks all translations, exact indices, template kernels and complete extension sets.

By [A finite rank horizon for the proposed all-rank patch rule](040-FINITE-RANK-PATCH-REDUCTION.md), any quadruple with a nonzero individual patch correction has full-rhombus triangular span at most nine. Capping the three full-rhombus boundary gaps at TWO preserves boundary membership, the first interior layer, every triple-facet template, all dot products and all primitive index ratios. It yields a rank at most fifteen. Therefore (3) controls EVERY affected quadruple at arbitrary rank, including disconnected ones. Untouched connected quadruples are deliberately not inferred from this set.

## Criterion B through rank twelve

The complete connected four-tuple lists at ranks 6,...,12 have respectively

    29,346; 64,080; 112,374; 174,168; 249,459; 338,247; 440,532

independent occurrences: 1,408,206 in total. Every fully corrected value is positive, with the same minimum (3). Every dependent constructor is also retained and independently checked. The rank 5 control is handled separately below rather than hidden in the positive total.

Connected enumeration begins with all singleton graph vertices and repeatedly adjoins every neighboring vertex, deduplicating sorted IDs. Any connected set has a spanning tree, so removing a leaf and inducting proves completeness. Sparse deletion of identically zero ambient columns preserves the full saturated normal lattice and metric; it is not a support restriction on the hive. The stream/sparse repair changed the implementation, not the intended list or the rational rule.

At any of the stated ranks, an independent quadruple is connected, affected, or untouched and disconnected. Criterion B, criterion C, or criterion A with product factorization covers it. Thus EVERY independent quadruple has corrected value >1/3000. The complete normal-cycle theorem makes the sum of all primitive-quotient corrections vanish against the actual lattice face-volume weights. The full local formula gives (1), including nonsimplicial normal cones and hidden dimensions.

## A genuine small-rank rule failure and its exact repair

The unchanged patch rule has 132 negative connected four-cones at rank 5. This is an actual failure of that local certificate; previously established whole rank-five positivity is not withdrawn. No entire LR coefficient is negative here.

For every one of those tuples, the current audit retains EVERY choice of original full rhombi giving its four primitive directions. There are 192 choices after duplicate directions are respected. In each, all three enclosing-boundary gaps are at most ONE. An independent triangle-adjacency reconstruction verifies every full row, union, gap and choice.

If cap-two compression from a larger rank produced one of these negative configurations, any shortened boundary gap would become exactly TWO. None of the 192 choices has such a gap. Thus no boundary gap could have shortened, and the original rank would already have been5. These exceptional configurations cannot be compressed images of a rank>=6 failure.

This repairs the universal reduction's base case, not the rank-five functionals. The earlier sufficient test “B passes at every rank 5..14” is false. The stronger relevant formulation is: handle the verified rank-five nonliftable exceptions separately and test the remaining connected checks at ranks 6..14. The original sufficient implication remains a sufficient implication, but its unchanged antecedent cannot be advertised as completed.

## Exact remaining bridge

Criteria A and C are now complete at their universal horizons. Criterion B is verified through rank 12; its connected lists at ranks 13 and 14 are NOT complete sign verdicts. Since affected cones already pass universally, only the UNTOUCHED connected independent quadruples at these two ranks require remaining raw-sign checks. Equivalently one may verify their complete connected B lists with all corrections attached.

If those finite checks pass, the cap-two horizon plus the exceptional-preimage audit proves (1) at every n>=6. An actual nonpositive local result would instead identify a failure of this fixed patch rule, requiring different supports or further compensation; it would not itself be an entire LR counterexample. The theorem does not establish c62 at rank 13, c74 at rank 14, or an all-rank codimension-four theorem.

No complete quintuple/codimension-five computation was performed, and no additional lower unrestricted coefficient is established. This is the single most informative remaining test of this mechanism.

## Independent evidence and computational limits

VERIFICATION/SEALED-ROSTERS.json replays 1,508,387 independent occurrences across the three criteria and 127,467 primitive incidence occurrences. The criteria overlap; these are not counts of distinct polynomials or independent discoveries. All 132 nonpositive occurrences are the explicitly retained rank-five local exceptions. The accepted rank 12 file is DATA/A04/B-R12-Q4.json.gz. Its separate complete A03 record is overlapping same-model evidence, not another independent list.

VERIFICATION/NEW-TYPES.json independently checks 1,028 saved trace bodies representing 972 distinct new type keys, 12,273 fundamental-point occurrences and 12,054 proper-face quotient occurrences. It uses SymPy exact matrices and Hermite-normal-form cosets instead of the primary Fraction elimination and finite-group numerator construction. The higher-index trace is bound to its actual integer embedding by an integral saturated basis isometry, not by equal Gram/index alone. Previously verified rank-seven type values retain their explicit inherited scope.

No new LR scalars or full LR vectors are used here. The consequence rests on the complete all-boundary geometric theorem and finite certificates, challenged earlier by full whole-LR and face-volume comparisons preserved in history.

Several incomplete computations preceded the retained certificates: an orientation assertion stopped one after the affected-extension checks; a serialization memory limit stopped another after connected checks through rank 11. Streaming produced a complete rank 12 record. A separate sparse implementation reproduced rank 12, but reached its 45-second deadline before completing rank 13. No incomplete in-memory prefix supplies a sign verdict. The final verification checks only the retained complete records; ranks 13 and 14 remain unresolved.

Analytic reference: N. Berline and M. Vergne, Local Euler--Maclaurin formula for polytopes, `arXiv:math/0507256v3`, especially lattice equivariance, orthogonal multiplicativity, dual solid valuation and the complete local formula. The exact local/global normalization proof is retained in [Complete refined normal-cycle compensation, including hidden affine strata](025-COMPLETE-REFINED-NORMAL-CYCLE.md), and the finite geometric horizon in [A finite rank horizon for the proposed all-rank patch rule](040-FINITE-RANK-PATCH-REDUCTION.md).
