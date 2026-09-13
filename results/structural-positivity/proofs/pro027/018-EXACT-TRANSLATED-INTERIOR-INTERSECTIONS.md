# A complete overlap operator for first-interior translates

Building on [Complete source-sink LR interiors are generated at their first grade](017-COMPLETE-FLOW-INTERIOR-GENERATION.md), this proof establishes exact whole-count intersections and a finite geometric Euler operator. It does not give an ordinary-positive basis or a complexity bound.

## 1. Every intersection retains its true affine netflow

Use the complete flow family, q and U=C_q cap Z^E of [Complete source-sink LR interiors are generated at their first grade](017-COMPLETE-FLOW-INTERIOR-GENERATION.md). For a nonempty finite J subset U put

    ell_J(e)=max_(u in J)u(e),
    Delta_J(k)=sum_(i<=k<j)ell_J(i,j)-q, 1<=k<n.

A coordinatewise maximum is NOT declared to be a flow. Its divergence is retained exactly. An integer x belongs to every u+F_n(t), u in J, precisely when div x=(q+t)(e1-en) and x>=ell_J. Subtracting ell_J is an integral bijection with the complete nonnegative-flow count

    K_n(t*1-Delta_J).                                (1)

The convention is K_n(R)=0 when any prefix coordinate is negative. For the complete graph this is also the exact feasibility criterion: nonnegative prefixes can always be realized by adjacent-edge flows. Thus the first nonempty grade of this intersection is max_k Delta_J(k), and all higher grades are feasible. Each Delta_J(k)>=0 since the maximum dominates any u in J.

For a pair u,v, their prefix crossing totals both equal q; therefore

    Delta_(u,v)(k)=1/2 sum_(i<=k<j)|u_ij-v_ij|.

In particular the half-sum is integral. Full inclusion-exclusion gives, at EVERY integer t>=0,

    I_n(q+t)=sum_(empty!=J subset U) (-1)^(|J|+1)
                K_n(t*1-Delta_J).                   (2)

All translates cover by [Complete source-sink LR interiors are generated at their first grade](017-COMPLETE-FLOW-INTERIOR-GENERATION.md). No selected intersection, moving endpoint or netflow correction is missing. An individual shifted count in (1) is not asserted to be a single all-grade polynomial; any coefficient extraction from it needs its own chamber and endpoint argument.

## 2. A smaller exact Euler operator

Subdivide the closed polytope C_q by all integer coordinate hyperplanes that meet it. Every resulting cell is an incidence-flow polytope with integral lower and upper coordinate bounds. Incidence total unimodularity, unchanged by adjoining coordinate-bound rows, gives integral vertices. Hence all vertices belong to U, and every point of U is a grid vertex. Triangulate this finite polytopal complex compatibly using a global pulling order; no extra vertices are needed. Call the resulting simplicial complex T.

For any integer flow x of value q+t, the set

    A_x={u in C_q : u_e<=x_e for every edge e}

is empty or convex. Since the bounds x_e are integral coordinate cuts in the chosen subdivision, A_x is exactly a subcomplex of T; it is not only a collection of selected lattice points. Its Euler characteristic is zero when empty and one when nonempty. A simplex F belongs to this subcomplex exactly when all of its vertices are <=x coordinatewise. Summing Euler characteristics over x yields the complete finite identity

    I_n(q+t)=sum_(nonempty simplices F of T) (-1)^dim(F)
                 K_n(t*1-Delta_(vertices F)).         (3)

This replaces arbitrary subsets by faces of one fixed compatible complex. It does not prove a small complex at high rank, unimodularity of every simplex, positivity of the signed terms, or count-polynomiality of every intersection. The integral grid-vertex premise and convex clipped subcomplex are the points that repair a naive nerve/pointwise-max argument.

## 3. Two fully explicit rectangular cases

For n6 and n7 the left half in [Complete source-sink LR interiors are generated at their first grade](017-COMPLETE-FLOW-INTERIOR-GENERATION.md) has dimension one. Set h=n-5, so h=1 or 2. Its sink demand at its third vertex is h. If a is the direct first-to-third residual flow, then 0<=a<=h, with the other two residual edges equal to fixed constants minus a. The right half has independent parameter b in the same interval. Thus U is the full grid {0,...,h}^2.

For fixed x, membership u_(a,b)<=x cuts each of a,b to an integer interval, so the admitted grid is a rectangle or empty. Its vertex-edge-square Euler sum is one precisely when nonempty. Adjacent horizontal intersections all have the same prefix deficit (1,1,0,...,0); adjacent vertical intersections are their reversals. Every elementary square has deficit one in the first two and last two prefix positions, zero otherwise. Define

    F_n(t)=K_n(t-1,t-1,t,...,t),
    G_n(t)=K_n(t-1,t-1,t,...,t,t-1,t-1),

with overlapping notation interpreted by the first/last-two position rule. The whole count is

    I_n(q+t)=(h+1)^2 P_n(t)-2h(h+1)F_n(t)+h^2G_n(t). (4)

This is proved for all stretches, not fitted. The n6 checks at t1,2,3 give (P,I,F,G)=(16,49,4,1),(125,320,50,20),(660,1485,330,165). At n7, t1,2 give (32,200,8,2),(450,2178,180,72).

## 4. Necessary overlap terms and limitations

Dropping all intersections would count 64 rather than 49 at n6,t1. Dropping the final positive square correction after subtracting edges would count 48 instead of 49. At n7,t1 the corresponding square correction is 8. Thus both the negative and positive overlap layers are mathematically necessary.

The complete flow coverage proof does not transfer solely from a matching Ehrhart polynomial, a coordinate face, or a first-interior count. The two-row positivity and quantitative-surplus proofs give complete LR counting models with unique first interiors but genuinely uncovered points in every later positive grade. The rank 7 example in those proofs is one instance. Such uncovered strata must be retained in a general LR interior approach.
