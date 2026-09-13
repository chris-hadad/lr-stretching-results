# Complete source-sink LR interiors are generated at their first grade

The codegree and stable LR count are rederived below. The principal result is exact closed-polytope Minkowski equality and integral first-interior generation. Worldwide novelty, ordinary-coefficient positivity at every rank, and an affine identification with conventional hive coordinates are not claimed.

## 1. Entire LR count and the actual lattice

Let n>=3 and let rho=(n-1,n-2,...,0), theta=(1,0,...,0,-1). For integers M>=s>=1 set

    lambda=2M rho-s theta, mu=nu=M rho, lambda outer.

These are nonnegative partitions: the first and last adjacent gaps of lambda are 2M-s>=M, and its other gaps are 2M. Lambda has n positive parts, the inners have n-1 after trimming. Their sizes are M n(n-1), M n(n-1)/2, M n(n-1)/2. Thus ordinary rank is n, and balance holds. The displayed rank/size need not be minimal. The s=0 case is the multiplicity-one highest component and is excluded from the positive-dimensional statements.

Write K_n(R) for all nonnegative flows on edges i<j of the complete acyclic graph on n vertices, with prefix netflow R=(R1,...,R_(n-1)). The subscript denotes the vertex count. The entire all-stretch identity is

    c^(t lambda)_(t mu,t nu)=K_n(st,...,st).             (1)

The following direct derivation establishes the count identity. Multiplying the Schur product by the Weyl alternant A_rho, the coefficient of the strictly dominant monomial x^(t lambda+rho) is exactly the desired LR coefficient. Expanding both numerator alternants and the denominator product over positive roots gives the complete double-Weyl sum

    sum_(w,v in S_n) sign(w) sign(v)
      K[st theta-(Mt+1)(2rho-wrho-vrho)].

Every proper prefix sum of rho-wrho is a nonnegative integer, and at least one is positive for w!=id: the first k entries of rho have the largest possible k-entry sum, and equality at every k forces the identity. Thus any nonidentity pair makes some target prefix at most st-(Mt+1)<0. A nonnegative acyclic flow cannot have a negative prefix. Only the identity pair survives. At t=0 the same argument gives one. No numerator term is dropped without this support proof. This also establishes the equality case M=s of the stable region, without assuming a separate Horn-release identity.

Let F_n(t)={x_ij>=0: div x=t(e1-en)}. It is bounded because every coordinate is at most the value across any prefix it crosses, namely t. Its affine lattice is saturated: freely choose the nonadjacent-edge coordinates, then recover

    x_(k,k+1)=t-sum_(i<=k<j, j>i+1) x_ij.

This integer inverse has coefficient one on every eliminated adjacent edge. There are

    d=binom(n,2)-(n-1)=(n-1)(n-2)/2

free coordinates. Every edge lies on a source-sink path. Averaging all unit path flows gives a strictly positive real point, so the actual dimension is d. The unit polytope is the convex hull of unit path flows: repeatedly remove a positive source-sink path from any nonnegative flow; acyclicity rules out a nonzero circulation left over. It is therefore integral. Its entire Ehrhart polynomial has degree d. Equation (1) transfers this degree and all counting values to the entire LR polynomial, without asserting a lattice equivalence to the conventional hive.

In this full affine space, all coordinates can be positive, and every zero coordinate is on a supporting hyperplane. Thus true relative-interior lattice points are precisely flows with every coordinate at least one. Reciprocity gives the same true interior COUNT for the entire LR model of equal dimension. The translation geometry below is explicitly in this complete flow counting model, not a claimed ring isomorphism of all LR degenerations.

## 2. Codegree and first-interior polytope

Let b=div(1), so b_i=n+1-2i. The number of edges crossing prefix k is k(n-k). A positive integer flow of value N has N>=k(n-k) at every prefix. Hence its least possible value is at least

    q=floor(n^2/4).

It is attained. Set all nonadjacent residual edges to zero and set residual adjacent edge k,k+1 to q-k(n-k)>=0. Adding one to every edge gives a positive integer flow of value q. This proves codegree q, with no sampled-interior premise.

For a real N define the CLOSED positive-slack polytope

    C_N={x_ij>=1: div x=N(e1-en)}.

Its lattice points, not its real points, are exactly the true relative interiors at integral N. In particular C_N is not the open real relative interior of F_n(N). This distinction is essential in the next equality.

## 3. A complete cut bound proves generation

For every real N>=q and real t>=0,

    C_(N+t)=C_N+F_n(t).                               (2)

For integers N>=q and t>=0, equality also holds on integer points:

    C_(N+t) cap Z^E = (C_N cap Z^E)+(F_n(t) cap Z^E). (3)

The forward inclusion is immediate. For the reverse, take x in C_(N+t) and capacities y=x-1>=0. For any source-sink cut S (1 in S, n not in S),

    y(delta+ S)-y(delta- S)=N+t-b(S).

Since b(S)<=sum_i max(b_i,0)=floor(n^2/4)=q, its outgoing capacity is at least N+t-q>=t. Thus y contains a source-sink flow v of value t. Then u=x-v>=1 and div u=N(e1-en), giving (2). With integral capacities an integral v exists, giving (3).

For completeness, the integral max-flow argument used here needs no unprovided optimization oracle. Begin with zero flow and augment along a residual source-sink path, including reverse arcs, by an integral positive bottleneck, stopping at value t. If the process stops earlier, let S be the vertices reachable from the source in its residual network. All forward cut edges are saturated and all incoming cut flows are zero, so their original outgoing capacity equals the attained value, contradicting the lower bound t. The integral value increases at each step, so termination before or at t is finite. For real capacities, maximize the flow value on the compact feasible capacity polytope; the same residual-reachability argument at a maximizer proves the required cut equality. Thus real equality does not rely on termination of an irrational-capacity augmentation algorithm.

Taking N=q, every later true interior lattice point belongs to at least one translate u+F_n(t) with u a first-interior lattice point. This is the exact generating-at-first-grade property often called levelness for this integral Ehrhart model. It does NOT say the translates are disjoint or that the surplus is coefficient-positive.

All integer dilations are covered too. For F_n(s), s>=1, the true codegree is ceil(q/s). Use N=s ceil(q/s)>=q and t replaced by st in (2)-(3). This dilation changes the lattice-point scale, with the codegree adjusted as stated.

## 4. First-interior type is a square

Put m=floor(n/2). In C_q subtract the all-one flow. Every residual edge crossing a maximum middle cut is zero. At even n=2m this separates the left and right m-vertex graphs. At odd n=2m+1 both middle cuts are maximum, so the central vertex is isolated in the residual. The right half is the reversal of the left half.

The left half is the complete nonnegative K_m flow with netflow

    ((m-1)^2, -(2m-3), -(2m-5), ..., -1), n=2m;
    (m(m-1), -(2m-2), -(2m-4), ..., -2), n=2m+1.

For m=1 the half consists of one point. Let A_n be its integer count. The construction and its inverse retain every edge: insert both half-flows, reverse the right half, put zero on all remaining residual edges, then add one everywhere. Consequently

    I_n(q)=A_n^2.                                    (4)

Both half polytopes have their saturated incidence lattices, with dimension (m-1)(m-2)/2 for m>=2. The full closed first-interior polytope has twice this dimension. This is a structural first-interior factorization, not a factorization of the entire parent Ehrhart polynomial.

Fresh complete enumerations for n3..8 give A_n=1,1,1,2,3,13 and first-interior counts 1,1,1,4,9,169. These are finite checks of (4), not a substitute for its all-n proof.

## 5. Quantitative scope and the actual remaining subtraction

Let N0=I_n(q). Equations (2)-(3) give the complete, all-integer-grade inequalities

    P_n(t)<=I_n(q+t)<=N0 P_n(t).

Thus 0<=S_n(t)<= (N0-1)P_n(t) pointwise. There is no inference that either inequality holds coefficientwise. Overlaps are indispensable: at n6,t1 the 4 translates contain64 incidences but only 49 distinct points; at n8,t1 the 169 translates contain10816 incidences but only 4900 distinct points. [A complete overlap operator for first-interior translates](018-EXACT-TRANSLATED-INTERIOR-INTERSECTIONS.md) supplies their exact complete intersection operator. A general bound on each subtracted ordinary coefficient for all n remains open here.
