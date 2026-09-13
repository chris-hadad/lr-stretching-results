# Ordinary positivity for an admissible two-sided strip

## Object and admissibility

Split N=h+q1+q2 composition coordinates into groups of sizes h,q1,q2, where
h>=0 and q1,q2>=1. Their respective totals are U,V,R, with U+V+R=T. For h=0
the first group is absent and U=0. All coordinates are nonnegative integers.
Add one integer coordinate s with the complete bounds

    max(0,V-B) <= s <= D+min(C,U+V).

Assume T,B,C,D>=0 and T<=B+C+D. The interval is nonempty at every base point:
V-B<=D+C follows from V<=T, and V-B<=D+U+V follows from B,D,U>=0. Both upper
bounds are nonnegative. The whole lattice is the composition lattice times
Z; deleting one composition coordinate gives a saturated integer chart.

We prove that the complete count under simultaneous stretching of T,B,C,D
has nonnegative ordinary coefficients on this entire admissible domain.
Independent interval factors preserve the conclusion.

Write B_n(v)=binom(v+n-1,n-1), for n>=1, and R_k(v)=binom(v+k-1,k) for
k>=1, with R_0=1. For positive p,q define the clipped first-moment tail

    E_pq(W,Z)=sum_(u+v=W, u,v>=0) v B_p(u) B_q(Z+v).

Also let M_pq(Z,W) be the complete capped moment, with p distinguished base
coordinates and q others, at total Z+W:

    M_pq(Z,W)=sum_(v=0)^(Z+W) min(W,v) B_p(v) B_q(Z+W-v).

The [single-capped-interval proof](positive-capped-fiber.md#the-capped-first-moment)
gives the explicit positive polynomial

    M_pq(Z,W)=sum_(k=0)^(p+q-1)
       R_k(Z) B_(p+q-k)(W) alpha_k W,

where alpha_k=p/(p+q-k) for k<q and alpha_k=1 otherwise. This is a
coefficientwise statement, not an inference from a pointwise inequality.

Changing variables from v to Z+v in the tail gives the useful exact identity

    E_pq(W+Z,0)-E_pq(W,Z)=M_qp(W,Z),                  (1)
    E_pq(T,0)=q T/(p+q) B_(p+q)(T).

In particular the left difference in (1) has nonnegative ordinary coefficients.

## Both cuts active: a complete positive expansion

First suppose T>=B and T>=C. There are nonnegative integer parameters
a,b,c,d,e with

    B=b+d, C=c+d, D=a+e, T=b+c+d+e.

For T<=B+C take d=B+C-T, e=0, b=T-C, c=T-B, a=D. For T>=B+C take
d=0, e=T-B-C, b=B, c=C, a=D-e; admissibility ensures a>=0. These formulas
are homogeneous, so they commute with stretching. Rational parameters obey
the same algebra. Their nonuniqueness is harmless.

Put T0=c+d+e. Summing the interval length directly yields the whole count

    (a+T0+1) B_N(b+T0)
      -E_(h+q1,q2)(c+d,b+e)
      -E_(h+q2,q1)(c+e,b+d).                         (2)

The first tail removes the excess of the tentative upper width C beyond
U+V. The second removes the lower-bound displacement beyond B. Admissibility
proved that these subtractions never leave an empty or reversed interval.

Expand each occurrence of b using the rising-binomial Vandermonde identity.
For 0<=k<=N-1 put n=N-k, tau1=max(q2-k,0), tau2=max(q1-k,0), and

    rho_k=1-(tau1+tau2)/n.

The coefficient of R_k(b) in (2), after applying (1), is exactly

    (a+1+rho_k T0) B_n(T0)
      + [k<q2] M_(q2-k,h+q1)(c+d,e)
      + [k<q1] M_(q1-k,h+q2)(c+e,d).                (3)

Here a bracket is 1 when its condition holds and 0 otherwise; absent terms
do not call M with a zero group size. To check (3), the corresponding full
tail moments are tau1*T0/n*B_n(T0) and tau2*T0/n*B_n(T0), with the two
positive capped-moment differences from (1).

Every rho_k is nonnegative. If k<min(q1,q2), then
n-tau1-tau2=h+k>=0. If just one tail remains, its tau is at most n; if no
tail remains the assertion is immediate. Thus (3), multiplied by R_k(b)
and summed over k, is a complete expansion into polynomials with nonnegative
ordinary coefficients in a,b,c,d,e. No numerical interpolation, numerator
positivity premise, or coefficient comparison from set inclusion is used.

## The other three closed cases

If B>=T and C<=T, the lower cut is inactive. The whole count is

    F_(h+q1,q2)(D,T-C,C),

the [positive single-capped-interval polynomial](positive-capped-fiber.md)
defined and proved by its complete composition sum. Its three
arguments are nonnegative and homogeneous in the physical parameters.

If C>=T and B<=T, the upper cutoff is inactive. The interval length is
D+1+U+min(V,B), so the whole count is

    (D+1+h*T/N) B_N(T) + M_(q1,h+q2)(T-B,B).

Both terms have nonnegative ordinary coefficients in D,T-B,B. If both
B>=T and C>=T, the count is simply

    (D+1+(h+q1)*T/N) B_N(T).

These four cases cover the entire admissible domain, including every equality
wall. Their formulas agree there because each was derived from the same
complete interval count. Substituting the nonnegative homogeneous parameters
of any fixed integer member proves its ordinary coefficient nonnegativity.
Dimension drops, T=0, and absent middle group h=0 are included; at T=0 the
base is a point and the count is D+1.

In fact every coefficient through the actual degree is strictly positive.
In all four cases the positive expansion proves coefficientwise domination
of B_N(T) by the full count. For T>0, B_N(tT) has strictly positive
coefficients through degree N-1. The whole polytope projects onto the entire
(N-1)-simplex and adds at most one interval dimension, so its actual degree
is N-1 or N. In the latter case its leading coefficient is positive by
relative volume. For T=0 the assertion follows from D+1. Independent
nonnegative-length interval factors preserve strict positivity through the
resulting actual degree. This argument does not require downward closure
of the multivariate monomial support.

Its linear coefficient also has the explicit concave formula

    c1 = D + (H_(N-1)-q1/N)*T
           + (h+q1)/N * min(C,T) + q1/N * min(B,T).

Indeed each tail has linear coefficient qW/N, as follows by setting Z=0
in its full first-moment identity; terms involving both W and Z have degree
at least two. Clamp B and C to T, which leaves the polytope unchanged, and
apply the two-tail formula. All displayed weights are positive. Thus c1
is concave on the convex admissible physical domain. This local structural
fact is consistent with the known failure of global c1 concavity for general LR.

## Application and exact limit

The rank-six cone has h=q1=q2=3, plus one independent interval
of length x. Its six formal active ray parameters are x,a,b,c,d,e, with
the exact relation a+b+c=d+e at the level of boundary generators. The count
depends only on the physical combinations in (2); the computed polynomial
annihilates the corresponding directional derivative. The displayed relation
is a relation among generators, not an equation restricting nonnegative
coefficient tuples.

The complete source geometry, unimodular slack map and all omitted-inequality
checks are described in the [sector proof](cdagger.md). Formula (3) supplies the sign proof; the independently
expanded 2,418 positive nonzero monomials are corroborating arithmetic. For
an integral boundary represented by rational nonnegative ray coefficients,
clear denominators, use the integer whole-model identity, then compare
coefficients in P_(q b)(t)=P_b(qt). This preserves signs without asserting
that every original ray coefficient was integral.

The general strip theorem is not a full-KTT theorem: arbitrary LR polytopes
have not been shown to reduce to these strips or to a closed class of such
operations. Several interval fibers coupled through the same base can restore the
cube-pyramid obstruction; constant-length independent interval factors preserve
the positive product theorem. The theorem explains a substantial actual positive
sector while retaining the need for a whole-object negative construction or
an exhaustive all-rank generation argument.
