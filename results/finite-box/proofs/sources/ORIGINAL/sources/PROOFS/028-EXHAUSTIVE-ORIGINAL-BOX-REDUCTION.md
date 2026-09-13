# An exhaustive finite cover of the original box

FRONTIER-025 P08. Originating computer-assisted reduction, pending independent campaign review. The final residual is a sufficient certificate list, NOT a list known to be negative, feasible, or mathematically unsettled after every campaign theorem.

## 1. Original domain and what a cover proves

The counted domain B contains nonempty partitions lambda,mu,nu with lambda outer, |lambda|=|mu|+|nu|<=30, maximum trimmed length<=7, and one representative for exchanging the two inners. The C++ enumeration uses size-first orientation while generating; its TSV output uses lexicographic inner orientation. These describe the same unordered original identities. Empty-inner input cases excluded from this count have P=0 or 1 by the identity representation and are independently harmless for the literal FrontierMath prompt.

Original rank <=5 is an adopted all-size source terminal. Its counted population is 140613221. The remaining exact-rank populations are 252489578 and 398740124. No asymptotic perturbation or common dilation of the BOX is used to assert coverage.

## 2. Every boundary profile and its exact root count

For a zero-gap mask m on one length-n partition, put

    a(m)=sum(i: gap i is NOT zero), 1<=i<=n-1.
    F_m(z)=z^a(m) / [(1-z^n) product_(i:not zero)(1-z^i)],
    F_m^0(z)=z^a(m) / product_(i:not zero)(1-z^i).

The exponent a(m) is the sum of the INDEX WEIGHTS i, not their cardinality. These are exactly the area generating functions of the partition with that exact gap mask, allowing arbitrary nonnegative last part or fixing last part zero respectively. Every positive gap is at least one. Coefficients through thirty are computed by exact integer dynamic programming and checked against a separate decreasing-part enumeration of every individual partition.

For each triple of masks, convolve the two inner series at positive areas, multiply by the outer coefficient at their sum, then subtract the identical construction with all three last parts zero. This isolates exact rank n. The terminal score is minimized over the invariant-weight symmetries of proof 029. It is symmetric in the two inners. The number of unordered roots is therefore (number of ordered roots + diagonal roots)/2; the diagonal uses one partition count, not its square.

This exact calculation gives:

| Original rank | All roots | Mask-terminal roots | Residual before other tests |
|---|---:|---:|---:|
| 6 | 252489578 | 222258876 | 30230702 |
| 7 | 398740124 | 342004926 | 56735198 |

Many mask-terminal roots are empty or were already protected by earlier theorems. These are actual counts under the present sufficient cover, not new additive campaign credit and not a measure of research difficulty.

## 3. Sound additional predicates

The complete original-root enumeration applies the following deterministic first-success order after the mask terminal:

(a) Containment lambda_i>=mu_i,nu_i and prefix highest-weight inequalities sum lambda<=sum(mu+nu). A failure proves the whole polynomial zero.

(b) The explicitly supplied A06 source-positive roster: strict padded rank-six inners rho=(5,4,3,2,1,0) and strict positive six-row outer of area thirty; and its two exact degree-thirteen rank-seven roots. The source reports complete numerical authentication, but the newly linked A004 numerical/review arrays were not supplied. This predicate retains that SOURCE scope.

(c) Valid multiplicity-one Horn inequalities, generated using tau(I)=(i_s-s,...,i_1-1). Every used index satisfies c^tau(K)_(tau(I),tau(J))=1. A negative slack proves zero. A zero slack gives the adopted whole-polynomial factorization into selected and complementary triples WHEN THE PARENT IS FEASIBLE.

At rank six, both proper children have rank<=5. At rank seven, sizes 2+5 and 3+4 are immediately positive. For 1+6, the full rank-six child is checked by rank<=5, the mask terminal, basic zero predicates, the stated A06 class, and all rank-six multiplicity-one Horn tests. A failed child test remains unresolved, and the parent continues examining later Horn indices.

IMPORTANT: an early successful equality need not be preceded by every other Horn inequality. The sign proof is the following exhaustive dichotomy. If the parent is infeasible, its polynomial is zero. If it is feasible, the valid tight Horn factorization applies and the certified children are coefficientwise nonnegative. Thus early termination certifies NONNEGATIVITY, not a positive count, feasibility, or a specific nonzero product for an infeasible parent. The same dichotomy is used for a rank-six child. This avoids falsely asserting feasibility from a selected equality.

The tiny LR index calculation is capped at two: it distinguishes zero, one, and at least two without pretending to give the latter full multiplicities. There are 521 used indices at rank six and 2042 at rank seven. All 2563 used multiplicity-one indices are independently recounted by literal cell-by-cell LR tableaux, rather than the primary row-allocation recursion. A true multiplicity-two fixture is rejected as a split certificate. The sound cover does not require that no additional valid Horn indices exist; omitting a valid test can only enlarge the residual.

## 4. Exact complete enumeration and resulting residual

The fresh C++ enumerator generates every partition of every area at most thirty with at most n parts. For each balanced total it enumerates unordered nonempty inner pairs, then all outer partitions of that total, rejecting only original rank below n before applying the sign predicates. Equal-sized inner pairs use the diagonal once. Thus every original identity is visited exactly once. Its integer sizes, mask fields, subset sums, and counters fit their declared machine types; no floating arithmetic is used. Subset sums are at most thirty and original counters are below 2^64.

The exact disjoint counts of its successive branches are:

| Branch | Rank 6 | Rank 7 |
|---|---:|---:|
| Mask terminal | 222258876 | 342004926 |
| Basic zero | 20002803 | 38386838 |
| Supplied A06 source class | 13 | 2 |
| Negative Horn slack | 918254 | 1605610 |
| Tight Horn sign terminal | 7694124 | 13014736 |
| Retained original identities | 1615508 | 3728012 |

The column sums reproduce the independent generating-function domain counts, including the mask-terminal counts. All 5343520 retained original identities are exported, not merely their counts, in BOX6-RESIDUAL.tsv and BOX7-RESIDUAL.tsv. Every line contains the complete bare triple and a certified chart DIMENSION UPPER BOUND. The Horn branch label is a sign terminal at its stated feasible/infeasible dichotomy, not an assertion that every such original parent has a nonempty Horn face.

Consequently every original root outside these two files is coefficientwise nonnegative, subject to the explicit adopted source premises. The 140613221 original lower-rank roots are separate and disjoint. The historical additive counter remains 4554; it is not replaced by or added to these cover counts.

## 5. Verification boundary

This is a complete originating finite enumeration with a sound mathematical predicate for each omitted root. The boundary-mask logic is independently audited at all 294912 masks, each used Horn index is independently recounted, and the entire domain and mask-class counts have independent generating-function verification. The full native 651229702-root filtering pass has NOT been repeated end to end by a second independently authored full enumerator. Its exact source, frozen scores/indices, runtime receipts, all area subtotals, and the entire retained identity lists are exported for campaign review. Do not inflate component verification into an independently accepted whole-census certificate.

The residual is conservative: other adopted full families, further geometric reduction, true-interior terminals, multiplicity-one/two count terminals, and old finite-vector membership have not all been applied. Therefore its size is not the exact number of previously mathematically unknown hives.
