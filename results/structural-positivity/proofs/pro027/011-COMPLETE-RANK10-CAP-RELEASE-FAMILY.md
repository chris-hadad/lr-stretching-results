# Complete ordinary positivity of a rank-ten cap-release family

Originating Unit3 theorem with two complete counting models and exact prior-space determination. This family has unbounded boundary size but exactly seven distinct entire polynomials; its finite stabilization is explicit, not presented as an infinite polynomial spectrum. No global novelty, external campaign acceptance, whole-rank or full KTT claim is made.

For every integer h>=0, let
lambda_h=(27+h,22+h,18+h,17+h,13,10,8,6,4,2),
mu_h=(17+h,17+h,17+h,13,10,8,6,4,2),
nu_h=(17+h,10,5,1),
P_h(t)=c^(t lambda_h)_(t mu_h,t nu_h), lambda outer.

Every ordinary coefficient of P_h through its actual degree18 is strictly positive. For h=0,...,5 every nonconstant ordinary coefficient strictly increases from P_h to P_(h+1), while P_h=P_6 for all h>=6. The complete linear coefficients at h=0,...,6 are

5279/360, 1085/72, 5521/360, 1117/72, 1127/72, 1133/72, 379/24.

## Entire object, lattice and prior polynomial space

These are positive balanced partitions of sizes127+4h=(94+3h)+(33+h), with maximum trimmed length10. The displayed rank is not asserted minimal. The complete S05 tail construction identifies P_h at every nonnegative integer stretch with ALL4-by7 tables with row margins t(7+h,5,4,1), column margins t(4+h,3,2,2,2,2,2).

For completeness, if R_i and C_j are the row and column tails and M=17+h, let alpha=(R2,R3,R4). The skew shape lambda/mu is alpha translated beyond column M plus column-disjoint horizontal rows of the column lengths. Its Schur function is s_alpha*product_j h_(tc_j). The skew shape nu/alpha has disjoint rows of the row lengths. Hall adjunction yields the scalar product of the two complete h-products, which is the number of all nonnegative tables. This is a full count identity, not an affine equivalence asserted for conventional hive coordinates.

The first3-by6 table entries form a free affine integer chart, with the last row and column recovered by integer margin subtraction. Its lattice is saturated Z18. The positive product table r_i*c_j/M proves full relative dimension18, and bipartite incidence total unimodularity gives integral vertices. Thus degree18 is a prior geometric fact, not a fit from positive samples.

True relative interiors require all28 entries positive. Subtracting one from every entry gives margins tr_i-7 and tc_j-4. The unit row forces t>=7, and at t=7 all residual margins are nonnegative with equal total, so a complete bipartite table exists. Therefore the true codegree is7 for every h. Reciprocity gives P_h(-1)=...=P_h(-6)=0 and nonemptiness gives P_h(0)=1. Positive stretches1,...,12 determine the remaining12 degrees of freedom;13 and14 are reserved unused checks.

## Exact count with every initial cap

Leave the large column last. For the six small columns, put
F_t(x,y,z)=h_(3t)(x,y,z,1) h_(2t)(x,y,z,1)^5.
Its coefficient at x^i y^j z^k counts every distribution to the three minor rows, with the major entry in each small column recovered from its own total. The COMPLETE count is

P_h(t)=sum_(0<=i<=t,0<=j<=4t,0<=k<=5t,
i+j+k>=max(0,(6-h)t)) [x^i y^j z^k]F_t.                (1)

The last column is uniquely(t-i,4t-j,5t-k,(h-6)t+i+j+k), in minor/major row order. Conversely every complete table gives exactly one coefficient contribution. Equation(1) is therefore an integer bijection, not leakage restricted to a support.

For h>=6 the last inequality is redundant, proving exact all-stretch stabilization P_h=P_6. All six initial cap bands h=0,...,5 remain. Their complete differences are the corresponding total-degree shells, not an arbitrarily removed positive part.

The final shell has the especially simple complete identity

P_6(t)-P_5(t)=binom(t+17,18).                            (2)

Indeed its total small-column minor mass is at most t-1, so all three row caps and all six column caps are automatically satisfied. There are18 independent nonnegative minor entries, with sum at most t-1. This proves(2) for positive stretches and also at t=0; its polynomial is t(t+1)...(t+17)/18!, with all18 nonconstant coefficients positive. At t=1 it equals1, proving that stabilization threshold6 is sharp among integer h>=0.

## Full exact positivity certificates

The seven complete ascending rational coefficient arrays, determining values, bare triples and model premises are in DATA/TF-0-vector-raw.json through TF-6-vector-raw.json. All133 coefficients are strictly positive. The six complete difference arrays are in DATA/SLAB-0-vector-raw.json through SLAB-5-vector-raw.json. Their constants are zero and all108 nonconstant coefficients are strictly positive. The assertions follow by the prior degree/codegree space, exact determining counts, and the independent whole model in proof012; they are not inferred from positivity of integer samples.

Every entire raw vector was saved before unused checks or favorable reconciliation. Each difference was likewise saved before comparison, with an immediate auxiliary-negative gate; none of these six differences has a negative ordinary coefficient. The differences are auxiliary, not assigned their own ordinary LR ranks.

Seven bases plus all-stretch stabilization now prove the theorem for every integer h>=0. Every nonconstant coefficient increases strictly through the six legal cap releases and is constant afterward. The c1 values listed above are distinct, so the family has exactly seven distinct polynomials.

## Complete cut compensation at this scope

The independently evaluated double-cut functional equals each of the seven complete c1 values. Thus the FULL higher-class first-jet remainder is zero at these seven margin pairs, not merely at a selected sector. It remains zero for every h>=6 as well: choose the side of each row cut not containing the major row, of total s<=10, and the side of each column cut not containing the large column, of total q<=13. At h>=6 the opposite row side is at least s and the opposite column side is at least10, so the cut length is min(s,q), independent of h. Therefore D_cut and P_h are both stable.

This establishes c1=D_cut for the entire displayed integer family. It is not a proof for arbitrary4-by7 margins or an unproved homogeneous parameter cone. The last two smallest row margins1,4 violate1+4<=2+2, so the source two-gate theorem does not cover any of these points. The near-corner condition would require every column to be at least9 and also fails. No original-area-thirty increment follows, since every displayed outer size is at least127.

## The pinned source parent is included by full permutation

At h=0 these tables are exactly the row/column permutation of the source margins(5,4,7,1) by(3,4,2,2,2,2,2). The pinned source triple
(29,25,18,17,14,10,8,6,4,2);
(17,17,17,14,10,8,6,4,2);
(17,12,8,1)
has outer size133 and rank10, and hence the same complete polynomial P_0. Its prior three scalars do not determine it; the fresh full reconstruction does. The smaller size127 tail lift is not a minimum-size theorem. This overlap is not counted as an eighth independent polynomial.
