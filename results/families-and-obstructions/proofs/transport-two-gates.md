# P01 / 004 — Removing the third margin gate from the whole transportation c1 theorem

Status: PROVED by originating derivation using the adopted complete pair/cut and LR bridge premises; subject to campaign verification. No full KTT or whole-rank conclusion.

## Theorem and complete margins

Let N>=3. Let r=(r1,r2,r3,r4) and c=(c1,...,cN) be strictly positive integral margins with equal total M. Allow a row ordering satisfying just

                    r4<=c_(1),
                    r3+r4<=c_(1)+c_(2),                 (1)

where columns are ordered increasingly for this test. There is NO restriction on r2+r3+r4 beyond positivity and balance. All ties in (1) are included. Then the ordinary linear coefficient of the ENTIRE transportation polynomial is

 c1=D_(4,N)(r,c)
   =sum_{I,J nonempty proper} w_4(I)w_N(J)
                  min(r(I),M-r(I),c(J),M-c(J))
   >=H_3 H_(N-1) min(min r,min c)>0,
 w_k(S)=(|S|-1)!(k-|S|-1)!/[2(k-1)!].                   (2)

The adopted double-cut theorem identifies the COMPLETE one-/two-class contribution and its lower bound. The new result is that every remaining higher-class first jet vanishes under (1).

## Every higher-class assignment

The full Lagrange expansion assigns every labeled column to one of four classes. Let n_i be their counts and C_i their margin totals. Its simple-root target is

 U=(C1-r1)t-n2-n3-n4,
 V=(C1+C2-r1-r2)t-2n3-2n4,
 W=(r4-C4)t-3n4.                                        (3)

A missing first class forces U<0. If n4>0, condition (1) gives C4>=r4, so W<0, even at equality. Thus every survivor has n4=0. If n3>=2, C3 is at least the two smallest columns, and V=(r3+r4-C3)t-2n3<0. A surviving higher-class assignment therefore has exactly

                        (n1,n2,n3,n4)=(a,b,1,0),
                        a,b>=1, a+b=N-1.                (4)

Proof 003 handles EVERY such occupation and all its eventual chambers, not just b=1 or b=2. No other survivor is omitted. The complete signed assignment sum agrees with the full count for every stretch; the sum of its finitely many eventual polynomials agrees with the entire Ehrhart polynomial at infinitely many integers and hence identically. Their first jets all vanish, proving (2).

The previous four-smallest-column gate was needed to limit b to at most two. It is no longer needed after the all-b proof. This is a strict enlargement of that nested region, not a claim about its convex hull or an unrestricted transportation theorem.

## Full ordinary LR map, lattice and degree

Define tails R_i=sum_(k=i)^4 r_k and C_j=sum_(k=j)^N c_k. With lambda outer put

 lambda=(M+R2,M+R3,M+R4,C1,...,CN),
 mu=(M,M,M,C2,...,CN),
 nu=(M,R2,R3,R4).                                       (5)

These are integral partitions. The difference of the first two sizes is M+R2+R3+R4=|nu|. Lambda has exactly N+3 positive parts, mu N+2 and nu four, so the final trimmed ordinary rank is N+3. This is the displayed constructor rank, not a minimum realization theorem.

Write alpha=(R2,R3,R4). The top component of lambda/mu is alpha translated beyond column M. The other skew rows occupy disjoint column intervals of lengths c_j. Thus s_(lambda/mu)=s_alpha product_j h_(c_j). The skew shape nu/alpha has disjoint rows of lengths r_i. Hall adjunction and the full Cauchy kernel give

 c^(t lambda)_(t mu,t nu)
  =<product_i h_(t r_i), product_j h_(t c_j)>
  =# ALL nonnegative integer tables with margins tr,tc.  (6)

Every shape and shift scales with t, so (6) holds for all integers t>=0, including value one at zero. This is a complete count proof, not an assertion that the conventional hive chart is affinely the matrix chart.

The upper-left 3-by-(N-1) entries freely generate the affine integer solution lattice, and margins recover the remaining entries integrally; it is saturated Z^(3(N-1)). The positive point r_i c_j/M proves full relative dimension. The oriented bipartite incidence matrix is totally unimodular, giving integral vertices. Thus the actual whole degree is 3(N-1), established before any numerical count. Zero margins are excluded; they must first be deleted and rank/degree reassigned. No empty positive-margin family occurs.

## A strict enlargement, not a reordering of an old example

Take r=(5,5,2,1), c=(1,2,2,2,3,3). The first two gates are equalities. The smallest possible sum outside a distinguished row is 13-5=8, larger than the four smallest columns' sum 7. Thus NO row permutation satisfies the former four-column gate. The earlier two-column exclusion also fails. The near-corner all-coefficient condition fails for every distinguished row: the smallest column is one, whereas the sum of the other two nonminimal minor rows is at least seven.

The complete LR triple is
 lambda=(21,16,14,13,12,10,8,6,3),
 mu=(13,13,13,12,10,8,6,3),
 nu=(13,8,3,1).

It has ordinary rank nine, outer size 103, and exact degree 15. DATA/P01/J04-WHOLE records its exact D and fresh complete counts from two representations. A handful of scalar counts is NOT claimed to reconstruct its full degree-15 polynomial. No new full coefficient vector is claimed.

## Endpoint gap

This proves c1 on a larger unbounded-column, unbounded-size entire LR family. It does not settle its higher coefficients, unrestricted four-row transportation, other LR boundaries of rank N+3, any entire rank above five, the original box, or full KTT. A legal negative completion outside the new cone and nonzero-but-sufficient compensation remain live alternatives. Frozen additive coverage remains 4,554; this theorem is not an identity-by-identity box enumeration. P02 retains the planned strict five-row/six-label all-coefficient arm.

## Recorded fresh scalar checks

The exact cut evaluates to 3871/360. Whole values t=0,1,2,3 are 1,5569,1131101,52437259, agreeing in both full count models. In the same member, assignment (2,1,1,1,0,0), zero-indexed, has occupations (2,3,1,0), target (1,8,5) and unsigned count 20090 at t=5. The newly handled occupation is not empty. Dropping the second gate instead permits (3,1,2,0): rows (4,4,4,1), assignment (2,2,1,0,0,0), t=3, target (9,2,3), count 39560. No sign claim for that entire parent follows. These are scalar checks, not determining values for a full polynomial.
