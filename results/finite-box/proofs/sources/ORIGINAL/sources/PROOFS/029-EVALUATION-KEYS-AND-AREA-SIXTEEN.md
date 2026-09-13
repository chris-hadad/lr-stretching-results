# Whole-count invariant symmetries and exact evaluation-key reduction

This note gives complete representation/count identities and a proposed finite mapping computation. The identities are standard tensor-duality operations, distinct from ordinary Ferrers conjugation.

## 1. Identity at every stretch

For length-n padding, the complete LR multiplicity is

    dim (V_mu tensor V_nu tensor V_lambda^*)^GL(n).

An integral dominant GL(n) weight w may have negative parts; its contragredient highest weight is w^*=(-w_n,...,-w_1). Permuting the three tensor factors preserves the invariant dimension. Simultaneously taking all three contragredients also preserves it, since the dual of the invariant space has the same dimension. These operations commute with stretching.

Thus start with three dominant weights (mu,nu,lambda^*), optionally dualize all of them, choose any as the factor to dualize into the new outer, and use the other two as inner weights. For intermediate (L,M,N) put a=M_n,b=N_n and define

    L'=L-(a+b)1_n, M'=M-a1_n, N'=N-b1_n.

This is the exact determinant identity. The two new inners are partitions. If L'_n<0, the tensor product of these polynomial representations cannot contain that highest weight, and the original whole count is zero. Otherwise these are nonnegative partitions of balanced size with the same whole count at every nonnegative integer stretch. A genuine nonempty original fiber cannot encounter the negative-last-part branch.

Their boundary zero-gap masks are obtained by permuting the three invariant-weight masks and reversing bits for each contragredient. This proves every mask symmetry used in proof 028. There are at most twelve oriented mask images; after identifying the two inner orders, six concrete determinant-normalized triples suffice.

Divide every part of a legal transformed triple by their common positive gcd g, recording

    P_original(t)=P_evaluation(g t).

Every ordinary coefficient is multiplied by the positive number g^k. Zero/empty cases are treated separately. This is sign equivalence, not equality of coefficient vectors when g>1. The entire count identity suffices; no false affine isomorphism of conventional hive charts is asserted.

The normalizations use only additions, reversal and integral determinant shifts. For an original area-at-most-thirty triple every component before gcd remains at most thirty: it is either an original component difference bounded by lambda_1, or at most mu_1+nu_1<=|lambda|. This justifies the five-bit per part keys even when a transformed outer AREA exceeds thirty. Only representatives with outer area<=30 are retained; the normalized identity image guarantees at least one. All final positive-part ranks are recomputed. A reduced rank<=5 or another previously proved terminal may be used at its exact scope.

## 2. Finite evaluation map

For each exported original residual input triple, the current implementation tests these six concrete variants, normalizes determinants and gcd, and selects a deterministic minimum ordered by outer area, actual rank, and packed bare triple. The two inners are ordered by their packed integer key. This is a documented deterministic reduction, not a proof of global minimal size/rank or maximal symmetry-orbit compression. In particular a rank drop may permit further lower-rank duality reductions not iterated in this version.

All original input triples survive this additional terminal check. Deduplication nevertheless gives:

    1615508 original rank-six roots -> 1364223 retained evaluation keys;
    3728012 original rank-seven roots -> 3406483 retained evaluation keys.

The two key files overlap at exactly 22732 identical bare triples. A streaming exact merge compares full packed identities, not only hashes or totals, and produces 4747974 distinct evaluation keys. There are 1380818 of actual rank six and 3367156 of actual rank seven. Every key has outer area<=30.

The source files CANON6/7-MAP.tsv contain one row per original residual input triple, in original TSV row order. Each records the selected local evaluation ID, positive stretch scale, and variant. The two GLOBAL-MAP6/7.txt files map each local evaluation ID to the merged global ID. GLOBAL-KEYS.tsv contains every complete merged triple and the number of original rank-six and rank-seven preimages. The sums are exactly 1615508 and 3728012. Global IDs are consecutive and key order is checked strictly; duplicates between files are merged only after exact identity comparison.

This is a genuine finite endpoint bridge: coefficientwise positivity of every retained evaluation key suffices for positivity of every original input triple. If a retained evaluation key has a verified negative coefficient, it is itself within the original size/rank box and gives a candidate; the scaling map also transfers the sign to each recorded original preimage. The data do not assert that any such coefficient is negative.

## 3. Closing the area-sixteen subbox

Only 56 ORIGINAL residual input triples in proof 028 have outer area at most sixteen: two at area fourteen, eight at fifteen, and forty-six at sixteen. Their priors are the complete degree-at-most-m spaces from their certified mask charts, with whole-count symmetry as above. These bounds are fixed before any numerical counts.

For each nonempty input triple, exact whole LR values at t=0,...,m determine the full polynomial. Stretches m+1 and m+2 are two positive sites unused in that fit. The first implementation enumerates all LR row-count arrays with every nonnegativity, column, ballot and content condition. The second independently fills each skew cell in reading order, enforcing row weak increase, column strict increase and the lattice-word condition. Neither counts a selected support. Both implementations agree on every determining and holdout value for every one of the 56 triples. Newton and independent Lagrange interpolation agree on every rational ordinary coefficient. All are nonnegative.

The prior degree bound prevents underfitting. Any P(1)=0 input triple would have used the separate zero-polynomial convention, not been interpolated through a false nonempty constant. All observed vectors here are nonempty. Actual degree is the largest nonzero reconstructed coefficient, consistent with LR polynomiality and the prior upper bound; no higher-degree count is approximated.

Consequently every ordinary LR polynomial with all lengths<=7 and outer area<=16 is coefficientwise nonnegative, including all dimensions, walls, empty cases and inner orders. Empty inners are the separate zero-or-one case. The only classical/source sign premises needed for this smaller-box conclusion are rank<=5, valid Horn factorization, intrinsic top coefficients, and proof 027; the newer strict-boundary area-thirty numerical arrays are not needed.

The simplest two residuals, at area fourteen, have mu=nu=(3,2,1,1) and lambda=(4,3,3,2,1,1) or (5,3,2,2,1,1). Both entire polynomials are binom(t+4,4), with values 1,5,15,35,70,126,210. This is an illustrative complete count, not a novelty claim for those small polynomials.

Exactly 56 global evaluation keys have area<=16. They collectively cover 526 original rank-six and 556 original rank-seven residual input triples, including larger-area preimages. Deleting this proved smaller-box class leaves precisely

    4747918 retained evaluation keys, all of area 17..30,
    representing 5342438 original root obligations under this cover.

Their exact definition is the rows of GLOBAL-KEYS.tsv with sum(lambda)>16. No mathematically unproved closure is inferred from this numeric reduction.

## 4. Verification scope

The original-input maps and key merge are fully serialized, with exact data/command hashes and successful native process receipts. Their algebraic transformations are proved above. A complete separately implemented replay of all 5343520 transformation words and of the entire native filtering pass has not been executed. Independent component checks and the full small-box two-model reconstructions do not supply that missing complete replay. The finite mapping remains a reproducible proof/certificate proposal at this scope.
