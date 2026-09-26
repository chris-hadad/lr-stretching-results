# The linear coefficient on the entire capacity cone

## Full object and theorem

For n>=1 and nonnegative integers w_1,...,w_n,c,d with s=sum w_i>=c+d, let P(t) count ALL nonnegative integer vectors y,z satisfying

    sum z_i=ct, sum y_i<=dt, y_i+z_i<=w_i t.                (1)

There is always an integer point: allocate c units greedily within the w capacities and take y=0, then scale. The original grade and full coordinate lattice are retained. The affine dimension is at most 2n-1 when c>0; this is a safe whole-polynomial degree bound also on degeneracies. For n=0 the only admitted data are c=d=0 and the count is one.

[the whole lift](one-overlap.md) gives this count as the ENTIRE LR polynomial whenever

    0<=c<=h, u,v>=h+d,
    alpha=(u+v+s-h-d-c,h+d,c),

using its displayed lambda/mu. In particular the linear choice h=c,u=v=c+d gives alpha=(s+d,c+d,c) and one common linear LR embedding on the entire cone s>=c+d. Zero rows are allowed and trailing zeros may be removed. Hence ordinary polynomiality follows from the classical stretched LR theorem. We prove that its c1 has a continuous, homogeneous degree-one, jointly concave extension on that whole cone, and

    c1(P) >= d.                                          (2)

For one active capacity the polynomial is dt+1, so the bound is sharp. The earlier product formula proves every coefficient only in its capacity-floor subchamber. Equation (2) does not assert all higher signs outside that subchamber, all single-overlap families, general three-row-inner LR or a whole ordinary rank.

## Exact capped extraction and the finite-difference bridge

Write x=x_2/x_1 and z=x_3/x_1. Then (1) is exactly the coefficient of x^(dt) z^(ct) in

    product_i h_(w_i t)(1,x,z)/(1-x).

The extra geometric series introduces the UNIQUE slack dt-sum y_i. It does not add multiplicity. In homogeneous root coordinates the target is ((s-c-d)t, dt, ct). The full three-term partial fractions of each h give assignments with occupations (p,q,r), assigned totals (v1,v2,v3), sign (-1)^q, slopes

    A=d+c-v2-v3, B=c-v3,

and original offsets (A0,B0)=(-q-r,-2r). The complete root multiplicities are

    (a,b,e)=(p+q+1,p+r,q+r).                              (3)

Every multiplicity-zero edge is retained with its Kronecker support convention. There is no missing-edge numerator because (3) is nonnegative. On the strict cone w_i,c,d>0,s>c+d, assignments with p=0 are eventually outside support; their A slope is c+d-s<0. The one occupied surviving assignment p=n gives

    binom(dt+n,n) binom(ct+n-1,n-1),

whose linear coefficient is d H_n+c H_(n-1).

Let F_(a,b,e) be the complete A2 flow chamber polynomial. Pascal's exact coefficient identity gives, on either common eventual strict chamber,

    F_(a,b,e)(A,B)-F_(a,b,e)(A-1,B)
       = F_(a-1,b,e)(A,B).                               (4)

The identity first holds for literal integer counts at all sufficiently deep points of that chamber; polynomial identity then justifies both derivatives at the stated offsets. It does not replace a negative-support count by a polynomial at an early grade.

The shifted term in (4), evaluated at (A0-1,B0), is EXACTLY the Astra008 Kostka kernel for occupations (p+1,q+1,r). Its sign is opposite to our (-1)^q. The right-hand term is the C011 transportation kernel for occupations (p,q,r), with its ORIGINAL offsets and slopes. This gives a direct connection to complete accepted kernels, without any new hypergeometric specialization.

Full load-bearing sources: [the complete transportation kernel proof](transport-kernels.md) proves both transportation chambers and every two-class boundary by elementary beta substitution and finite differences. [the occupation kernel proof](occupation-kernel.md) and [the complete three-row linear proof](three-row-linear.md) give the complete Kostka kernels, including r=0 and positive beta integral. Those files were read completely. Their classical summation sources remain credited. The later all-rank transportation proof is consistent but not needed beyond this independently proved three-node case.

## Complete signed linear functional

Use the positive Astra008 kernel

    K(a,b,r)=(2a-3)!!(2b-3)!!(2r-1)!!
              /[2(a+b-2)(2(a+b+r)-5)!!],

for a,b>=1,a+b>=3,r>=0, and (-1)!!=1. Let B(a,b)=(a-1)!(b-1)!/(a+b-1)!, and put, for p,q,r>=1 where used,

    C(p,q)=B(p+1,q),
    L(p,q)=C(p,q)/2+K(p+1,q+1,0),
    D(p,q)=C(p,q)/2-K(p+1,q+1,0),
    E(p,r)=B(p,r)/2+K(p+1,1,r).

Then the ENTIRE c1 is the one-occupied term above plus every labeled assignment of the following types:

    r=0, p,q>=1:
      -C(p,q)(d-v2)_+ -L(p,q) max(0,min(c,d+c-v2));

    q=0, p,r>=1:
      -E(p,r)(c-v3)_+;

    p,q,r>=1:
      -K(p+1,q+1,r) max(0,min(d+c-v2-v3,c-v3)).             (5)

Here is the full check using (4). The transport contribution at three occupied nodes is zero in both chambers. At r=0 it is

    -B(p,q)(A-B)_+ -(B(p,q)/2) max(0,min(A,B));

at q=0, where A-B=d>0, it is -(B(p,r)/2) B_+. The opposite-signed Kostka contribution is -K for three occupied nodes, -K(p+1,1,r) B_+ when q=0, and

    +B(p,q+1)(A-B)_+
      +[B(p,q+1)/2-K(p+1,q+1,0)] max(0,min(A,B))

when r=0. The beta recurrence B(p,q)=B(p,q+1)+B(p+1,q) proves (5) exactly. All nontrivial constants are zero. For n=1 the sum is empty and c1=d. Tied slopes and boundary faces are handled below through the common whole polynomial, not through an unsupported individual continuation.

## A complete beta sum controls the only adverse wall

For m,q>=1,

    sum_(p=0)^m binom(m,p) K(p+1,q+1,m-p)
      = B(m+1,q)/2 = C(m,q)/2.                           (6)

Use the full positive integral from Astra008:

    K(p+1,q+1,r)=1/(2 pi) integral_(x1+x2+x3=1)
        x1^(p-1/2) x2^(q-1/2) x3^(r-1/2)/(x1+x2) dx1 dx2.

All terms are integrable, including p=0 or r=0. Summing replaces x1^p x3^(m-p) by (x1+x3)^m. At x2=z the x1 integral of

    [x1(1-z-x1)]^(-1/2)/(x1+z)

equals pi/sqrt(z). For example substitute x1=(1-z)sin^2(theta), then tan(theta). The remaining integral is (1/2) integral_0^1 z^(q-1)(1-z)^m dz, proving (6). It follows that D(m,q)>0, and the sum over proper nonempty splits p,r>=1 is

    D(m,q)-K(1,q+1,m) < D(m,q).                           (7)

No threshold-family hypothesis is needed for this complete majorant.

The whole coefficient is continuous and linear away from the finite support/chamber hyperplanes in (5). At A=0 each active kernel enters with a nonpositive slope jump, and the last-empty term does the same. At B=0 the middle-empty and all applicable three-occupied terms also have nonpositive jumps. The only potentially positive jump is at A=B, equivalently d=v2 for a fixed nonempty middle label set J of size q.

Let its complement have m labels. The r=0 term for this J has slope jump -D(m,q), in the increasing normal d-w(J). Every active split of the complement into nonempty first and third sets adds +K(p+1,q+1,r). Their total is at most the complete sum (7). Thus the net jump is at most

    -K(1,q+1,m)<0.

Inactive subsets only make it smaller. This accounts for every internal wall: one-occupied terms are linear, and q=0 has A-B=d>0 in the interior. Generic segments therefore have nonincreasing directional slopes across every wall, proving concavity in the strict cone. Simultaneous walls follow by limits.

## Boundary, lattice and sharp lower bound

The common linear LR embedding above and classical chamber polynomiality give a continuous piecewise-polynomial extension on closed rational parameter cones: restrictions to a shared rational face count the same integer stretches, so coefficient restrictions agree. Formula (5) is already a finite continuous piecewise-linear function. It agrees with the actual c1 on the strict cone, hence on all rational faces by the full chamber theorem and on the real cone by continuity. This includes c=0,d=0,s=c+d, zero weights and tied support slopes. Delete zero weights for direct lower-dimensional counting. The all-zero case is separately the point polynomial one. No Ehrhart polynomial of an irrational polytope is asserted.

The parameter cone w_i,c,d>=0,c+d<=sum w_i has the following generators, for each i:

    (w=e_i,c=0,d=0), (w=e_i,c=1,d=0), (w=e_i,c=0,d=1).

To see completeness, split the w capacities into three nonnegative allocations of totals s-c-d,c,d. Greedy interval allocation gives such a split, rational for rational data and integral for integer data. The first two rays have polynomial one; the third has polynomial t+1. Concavity and positive degree-one homogeneity imply superadditivity, so adding the generator contributions gives exactly c1>=d. This is a direct full-cone proof, not a conclusion drawn from positive finite comparisons.
