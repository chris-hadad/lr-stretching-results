# Full quotient supports, exact local isometries, and a legal release failure

All negative coefficient-like observations below concern complete local BV constants or trial-corrected local weights. The boundary outside the stable region supplies an entire LR scalar but no negative ordinary coefficient. No ordinary-negative entire LR counterexample was found.

## Twelve quotient components cannot be replaced by the first seven

For each of the 381 supporting normal triples in the rank-seven certificate, retain its ACTUAL15-by 12 saturated kernel basis M_J and the complete primitive restriction primitive(M_J^T n). Hold the successful functionals h_J fixed, then set their last five coordinate entries to zero. This is an explicitly defined different rational functional in that fixed basis. It is not the rank-six certificate transported through an asserted geometric isomorphism, and it is not an impossibility test for every possible seven-dimensional correction space.

Evaluate this trial on ALL462468 independent quadruples, including every originally positive affected cone. DATA/J08-SEVEN-COMPONENT-TRIAL-RAW.json.gz contains the entire trial array. The successful functionals are necessarily an input to this trial. Every trial value and every negative occurrence is written in J08-SEVEN-COMPONENT-NEGATIVES.jsonl and the complete raw array before attaching the favorable full-minimum comparison. The code does not claim to have avoided reading the functionals it uses.

There are 2484 negative trial weights. The minimum is

    -16259903422350773/39501000000000000.

The full twelve-component certificate has minimum 164999998979/491400000000000>1/3000. Both complete arrays are preserved. This is a failure of that coordinate-truncated proposal, not an ordinary-negative LR coefficient, not a negative realized complete face, and not proof that every successful functional needs twelve nonzero coordinates in every basis. Primitive normalization itself is retained in this challenge; the distinct nonprimitive-normal counterexample remains a separate observation.

## The equal negative counts now have explicit, but only local, isometries

Both the rank-six and rank-seven full codimension-four atlases contain132 negative quadruple occurrences. Counting alone would not identify them. The local-isometry calculation checks an explicit exact equivalence: permute generator rows, sign-normalize and permute AMBIENT coordinate columns, and remove only identically zero columns. For every match the resulting entire integer normal matrices are identical. Signs are never changed independently on individual normal generators.

A signed ambient permutation is an integral Euclidean isometry. Removing a coordinate zero in every normal row removes an orthogonal free direction before passage to the transverse quotient; it leaves the saturated normal plane, its metric and its dual projected counting lattice unchanged. Thus the complete transverse BV constants agree under these recorded maps, at all lattice indices. The primary BV equivariance and ambient/subspace compatibility are precisely Proposition13 and Proposition14(b), not an equal-Gram/index heuristic.

The complete 132/132 occurrences occupy22 shared signed-support types. DATA/J08-NEGATIVE-SUPPORT-ISOMETRIES.json.gz retains the canonical matrices and the row/column/sign/zero-column words. Their values agree. This establishes LOCAL transverse-cone isometry, not a map of the two entire normal atlases, not matching complete affected incidence stars, not transfer of h_J, not co-realization in a hive, and not an all-rank classification. The failure in the first section illustrates the missing quotient/incidence information.

The surviving next question is whether a support-localized functional can be defined intrinsically on these geometric coordinate patches and verified against every affected positive extension. A complete finite-patch classification or generation argument at arbitrary rank remains unproved. Equal cardinalities or the 22 local types alone cannot supply it.

## A legal whole-LR boundary leaves the stable flow domain

The all-stretch direct geometric map in [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md) assumes M>=s. At n=7,M=1,s=2 the balanced bare triple is

    lambda=(10,10,8,6,4,2,2),
    mu=nu=(6,5,4,3,2,1,0).

It has ordinary rank seven and outer size 42. Complete literal LR enumeration gives P(1)=76. The uncut source--sink model at total flow2 instead gives 450. The difference is374, not zero. The whole coefficient vector and actual degree were not reconstructed in this test; no under-degree fit or negative inference is made.

The failure is already visible in every original inequality. Put flow2 on path 1->6->7 and zero elsewhere. The stable affine expression would give interior hive coordinates

    (15,24,31,36,41,19,27,33,39,22,29,36,24,32,27).

At the displayed boundary this point violates eleven of the 63 full original rhombi, each by one; the minimum slack is-1. All edge coordinates, all fifteen candidate hive coordinates, the bare triple and all 63 slacks were saved in J09-RELEASE-BOUNDARY-RAW.json before the favorable stable comparison. The complete actual scalar and the 450 uncut count are retained separately in J09-RELEASE-BOUNDARY-CHALLENGE.json.

The material repair required outside M>=s is to retain the complete column and ballot caps, or to use a separately proved complete released-Horn identity. A separate source gives such an all-rank count identity at its stated scope, but its unavailable larger certificates do not supply a new rank-seven full polynomial here. The stable geometric theorem in [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md) and the unrestricted c11 theorem in [The eleventh ordinary coefficient at every rank-seven LR boundary](034-ALL-RANK7-ELEVENTH-COEFFICIENT.md) remain valid; no general all-coefficient released-family positivity is asserted.

## Exact reduction of the verification cost

The first full atlas verifier stopped before producing a complete mathematical verdict because it spent substantial time checking full-column exact minors that were identically zero. The following algebraic reduction preserves the saturation calculation:

For a rational q-by-m matrix U, det(U U^T)=0 if and only if its rows are dependent, because U U^T is its Euclidean Gram matrix. This determinant is evaluated exactly by independent integer Bareiss elimination. For an independent U, any maximal minor using a column that is identically zero vanishes. Removing those columns before enumerating the minors therefore leaves their gcd, and hence the saturation index, unchanged. Every remaining maximal minor is still checked exactly.

The implementation in CODE/verify_ambient_v2.py uses these reductions and completes all 462468 independent bindings,25167 dependencies,381 full kernel saturations,20925 primitive incidences and every exact corrected sign. The earlier incomplete computation is not counted as a successful verification.

## Evidence scope

The full finite c11 certificate has independent exhaustive Laurent checks and a complete incidence check. The scalar outside the stable region is counted by the independent literal LR rule. The local comparisons and truncated-functional trial are bounded structural checks; they are not additional independent entire polynomials or external independent verification. Complete input identities, source versions, and raw negative values are retained.
