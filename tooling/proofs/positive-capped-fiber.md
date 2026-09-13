# A positive capped interval over a split simplex

This note proves the complete single-capped-interval polynomial and the capped
first-moment identity used in the [two-sided strip proof](positive-strip.md).
It is the underlying mathematical derivation from 9 September 2026; the source
version is recorded in the tooling source map.

## Whole object and direct count

Fix p,q>=1 and N=p+q. A simplex has N nonnegative composition coordinates,
with total Z+W. Let U be the sum of its first p coordinates. Above each point
place an integer interval

    0<=h<=Y+min(W,U),

where Y,Z,W are nonnegative integers. These are the complete inequalities:
h>=0, h<=Y+W, h<=Y+U, the composition nonnegativities, and their one total
equality. The lattice is the full integer composition lattice together with
h; deleting one composition coordinate gives the saturated standard chart.

The full count is

    F_pq(Y,Z,W)=sum_(U=0)^(Z+W)
       binom(U+p-1,p-1) binom(Z+W-U+q-1,q-1)
       (Y+1+min(W,U)).                                 (1)

Put B_a(v)=binom(v+a-1,a-1). Writing min(W,U)=W-(W-U)_+ gives

    F=(Y+W+1) B_N(Z+W)
      -sum_(u+v=W, u,v>=0) v B_p(u) B_q(Z+v).           (2)

This subtraction retains the entire clipped region and its boundary. There
is no inference from pointwise inclusion to ordinary coefficient domination.

## A positive expansion that resolves the cancellation

Use the rising binomial polynomials

    R_0(Z)=1,  R_k(Z)=binom(Z+k-1,k), k>=1.

Every R_k has nonnegative ordinary coefficients. Formal multiplication of
(1-s)^(-Z) and (1-s)^(-W-1), or Vandermonde's identity, gives

    B_N(Z+W)=sum_(k=0)^(N-1) R_k(Z) B_(N-k)(W).

Likewise B_q(Z+v)=sum_(k=0)^(q-1) R_k(Z) B_(q-k)(v).
For Q>=1, the complete first moment is

    sum_(u+v=W) v B_p(u) B_Q(v)
       =Q binom(W+p+Q-1,p+Q)
       =Q W/(p+Q) B_(p+Q)(W).

The first equality follows by differentiating the ordinary generating function
(1-s)^(-Q), multiplying by (1-s)^(-p), and taking its Wth coefficient.
It holds also at W=0. Substitution in (2) therefore proves the exact identity

    F_pq(Y,Z,W)=sum_(k=0)^(N-1)
       R_k(Z) B_(N-k)(W) (Y+1+alpha_k W),               (3)

where

    alpha_k=p/(N-k)  for 0<=k<q,
    alpha_k=1        for q<=k<=N-1.

Every factor in every summand has nonnegative ordinary coefficients in
Y,Z,W. Consequently all mixed ordinary coefficients of F_pq are nonnegative,
and every nonzero stretching specialization F_pq(tY,tZ,tW) has strictly
positive coefficients through its actual degree. For W>0, the k=0 summand
alone is positive through degree N. If W=0 and Z>0, (1) is
(Y+1)B_N(Z), with degree N-1 or N according as Y=0 or Y>0. If Z=W=0, it is
Y+1, including the constant case Y=0. Thus the dimension drops are explicit.
Independent interval factors such as X+1 preserve the conclusion.

## The capped first moment

With the notation above, the capped moment is the part of the full count
remaining after its constant interval contribution is removed:

    M_pq(Z,W) = F_pq(Y,Z,W) - (Y+1) B_(p+q)(Z+W).

Using the displayed Vandermonde identity to subtract that contribution
from (3) gives exactly

    M_pq(Z,W) = sum_(k=0)^(p+q-1)
       R_k(Z) B_(p+q-k)(W) alpha_k W.

Every factor has nonnegative ordinary coefficients. This supplies both the
moment identity and the function F used for the single-active-cut case of
the two-sided strip proof, including all zero-parameter boundaries.

## Limitation for multiple coupled intervals

The proof uses ONE interval, whose width appears to the first power. Replacing
it by r independent intervals of the same width replaces the last factor in
(1) by (Y+1+min(W,U))^r and invalidates the first-moment cancellation above.
At p=q=1,Y=Z=0 it becomes sum_(u=0)^W(u+1)^r, the known cube-pyramid count.
For r=20 its ordinary linear coefficient is negative. Thus a blanket
coefficient-preserving rule for arbitrarily many coupled fibers is false even
though the single-fiber operation is positive at every p,q.

The multiple-interval obstruction is an abstract polytope, with no asserted
whole-LR realization here. Its negative coefficient does not transfer to an
LR coefficient without a complete lattice and counting equivalence.
