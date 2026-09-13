# A finite rank horizon for the proposed all-rank patch rule

Claim FR027-P11-T004. This is a proved reduction to a finite certificate task, NOT a completed all-rank sign theorem. The necessary finite task below remains unfinished in this checkpoint.

Use the original triangular-grid hive directions N_n in the ordinary interior-coordinate lattice, with one standard coordinate metric. Assign the399 boundary-tagged template vectors from proof038 to every matching independent triple at every n, and zero to all other triples. The largest interior-coordinate triangular span of any template is THREE, independently checked in J10.

For a finite set A of lattice positions define

    r(A)=max_(i,j in A)(i+j)-min_(i,j in A)i-min_(i,j in A)j.

This is the side length of the smallest triangle of the fixed orientation enclosing A. A whole elementary rhombus has r=2. If two sets share a point, r(A union B)<=r(A)+r(B): translate the common point to zero, after which both coordinate minima are nonpositive and both sum maxima nonnegative, and bound the three extrema separately. Thus q rhombi connected by shared vertices have r<=2q.

## Raw connected cones: rank at most 2q+3

Connect normal generators when their NONZERO INTERIOR supports intersect. Choose an original full rhombus for each direction, retaining its boundary vertices. A connected q-tuple gives connected full rhombi, so their union A has r(A)<=2q. Write

    p=min i, q0=min j, r0=n-max(i+j).

All three are nonnegative. Translate the whole configuration and change the enclosing rank so that these gaps become min(p,1),min(q0,1),min(r0,1). Its new rank is

    n'=r(A)+min(p,1)+min(q0,1)+min(r0,1)<=2q+3.

Every full vertex is on the boundary before the operation exactly when its corresponding vertex is on the boundary afterward. Thus deletion of boundary coordinates leaves precisely the same signed normal matrix up to a permutation of active coordinates and insertion/removal of identically zero ambient columns. Independence, saturated normal lattices, projected counting lattices, metrics and complete zero-vertex BV values are preserved. Different generators remain different. Duplicate original rhombi cause no difficulty: choose any original representative and preserve all of its vertices in this construction.

In particular, RAW connected normal cones of dimensions1,2,3 can all be checked by ranks at most5,7,9 respectively. A coordinate-disconnected normal tuple is an orthogonal direct sum in disjoint coordinate sublattices, so its complete BV value is the product of the connected-component values. This uses a genuine integer lattice direct sum, not merely a disconnected Gram graph. The multiplicativity premise is Berline--Vergne Proposition14(c), at its full lattice scope.

## Corrected connected quadruples: rank at most fourteen

The previous compression need not preserve the flags i=1,j=1,i+j=n-1 used by the patch rule. Instead cap each of the THREE FULL-RHOMBUS boundary gaps at TWO. Boundary membership and membership in the first interior coordinate layer are both preserved for every vertex, hence for every triple facet's support. All normalized directed patch shapes, flags, template matches and ambient dot products remain identical. Formula038(1) preserves every primitive quotient divisor as well.

For connected quadruples r(A)<=8, so the corrected configuration has

    n'<=8+6=14.                                         (1)

The entire corrected constant, including every affected facet, is preserved. Capping at one is NOT adequate for this corrected statement. In J11,57 of120 concrete controls preserve the raw cone embedding but change at least one facet tag when cap one is used; cap two preserves them all.

## Possibly disconnected affected quadruples: rank at most fifteen

Suppose at least one correction delta_J(n) is nonzero. The vector v_J is supported on a template patch S with r(S)<=3. Nonzero dot product means the extra normal has a nonzero coordinate at a point of S. Each original rhombus for J contains a nonzero support point in S, and the extra rhombus also contains a point in S.

For any two vertices of one elementary rhombus, the changes in i,j, and i+j have absolute value at most two. Hence every vertex of the union A of the FOUR FULL rhombi has

    i>=min_S i-2, j>=min_S j-2,
    i+j<=max_S(i+j)+2.

Therefore r(A)<=r(S)+6<=9. The cap-two compression above preserves the entire corrected quadruple and gives

    n'<=9+6=15,                                         (2)

even if the interior-support graph is disconnected. If all corrections vanish, a disconnected quadruple is handled by the raw multiplicative component argument instead.

## Exact remaining finite certificate

The following finite tests suffice for strict all-rank codimension-four compensation:

A. Every connected independent tuple of q=1,2,3 hive directions has positive RAW value in every feasible atlas up to rank2q+3.

B. Every connected independent quadruple has positive FULL CORRECTED value in each atlas with5<=n<=14.

C. Every independent quadruple with at least one nonzero patch correction has positive FULL CORRECTED value in each atlas with5<=n<=15. A complete affected-star enumeration is an acceptable superset of C.

If A--C hold, every independent quadruple at every n>=5 has a positive corrected value: use (1) for connected tuples, (2) for affected disconnected tuples, and multiplicativity plus A for untouched disconnected tuples. The finite minima and finitely many products give a uniform positive epsilon. The complete normal-cycle theorem then gives

    c_(D_n-4) >= epsilon sum_(actual (D_n-4)-faces F)vol_Z(F),
    D_n=(n-1)(n-2)/2,

for every nonempty period-one whole hive of sufficient actual degree; smaller degrees give zero. This is the CONDITIONAL all-rank consequence, not a theorem already certified here.

Current verified coverage: both complete atlases at ranks6 and7 pass the patch rule; every affected rank8 star passes. This does not complete A--C. In particular the untouched rank8 connected quadruples and larger-rank configurations remain to be checked. A mere repeated count of132 negatives, the22 abstract isometry types, or a passing affected subset cannot replace this finite task.

J11 challenges the compression on120 exact full-rhombus configurations, expanded to ranks as large as27 by changing only noncritical boundary distances. All cap-two normal embeddings and all facet tags agree, while57 cap-one tag tests fail. These bounded controls challenge the general proof but do not supply its missing finite positivity certificates.

Primary analytic source: Berline and Vergne, Local Euler--Maclaurin formula for polytopes, arXiv:math/0507256v3, Proposition14(b),(c). The lattice-isometry and orthogonal-product hypotheses are retained. The finite geometry reduction above is an originating derivation.
