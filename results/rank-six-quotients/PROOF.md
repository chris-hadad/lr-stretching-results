# Saturated quotient transfer and an explicit segment-tail bound

## Definitions and coefficient premises

For a legal balanced LR boundary b=(lambda_b,mu_b,nu_b), lambda is outer and
P_b(t)=#(t H_b intersect Lambda)=sum c_k(H_b)t^k. All boundaries are padded to
length six in the original ten-height lattice Lambda=Z^10. Feasibility means
the entire hive is nonempty. The LR saturation and polynomiality premises give
an integral hive point and a polynomial count in the original stretch, with
constant one and degree the actual dimension. An infeasible positive-stretch
family instead has the zero polynomial; the all-empty triple has polynomial one.

The [whole-rank-six coefficient theorem](../rank-six-positivity/README.md)
provides, for every feasible whole parent and 1<=k<=actual dimension,

    c_k(H) >= epsilon_k sum_(actual k-faces F of H) vol_Lambda(F),

where ordinary volume is normalized in the full saturated direction lattice,
without a factorial multiplier. For the corollary here only k>=2 is needed:

    epsilon_2=epsilon_3=1/200000000,
    epsilon_k=1/2000000 for 4<=k<=10.

Padded lower ranks, boundary strata and nonsimple cones are included. An index
above actual degree is zero. The finite normal-cycle certificates proving
these parent inequalities are separate prerequisites, not inferred from the
quotient construction.

Take feasible integral whole boundaries b,a and put r=dim H_a>=1. Write
A=|lambda_b| and choose

    S=22528 A+1, P=H_(b+S a).

Choose any integral z in H_a, let Z=H_a-z and W=lin Z. Let pi be the coordinate
quotient by W, and set

    K=pi(P), barLambda=Lambda/(Lambda intersect W).

W is rational, so Lambda intersect W is saturated and barLambda is free.
K is the entire stabilized quotient. Its dimension is dim P-r. Translation
of H_a by z changes no counts, volumes or quotient. Nothing in this definition
identifies K with an LR hive of another ordinary rank.

## Complete stabilization, including boundaries

In the [original hive coordinates](../five-height-hives/PROOF.md), every row
has at most four coefficients of absolute value one. Write its inward form as
N_i x+beta_i(b)>=0. Boundary heights lie in [0,A], hence |beta_i(b)|<=2A.
Consider every invertible ten-row submatrix B. Its prospective vertex for
boundary b+s a, and every original-row slack at that vertex, are affine in s.
Use the same denominator det B for a slack's intercept and slope. Its
intercept numerator is the determinant of an eleven-by-eleven augmented
matrix. Expansion in the boundary column has eleven terms. Each boundary
entry has absolute value at most 2A; each ten-by-ten cofactor is at most
2^10 by Hadamard, since every normal row has Euclidean norm at most two.
Thus the intercept numerator has absolute value at most

    11 * 2A * 2^10 = 22528 A.

A nonzero slope numerator is an integer with absolute value at least one.
Every nonnegative root of a nonconstant slack is therefore at most 22528 A.
The chosen integer S lies strictly beyond every such root, simultaneously for
all prospective bases and rows. Zero slopes and identically zero slacks are
retained. This argument requires no full-dimensionality of the hive: a vertex
of any nonempty bounded polytope has ten independent active rows in the
ambient chart, including rows enforcing a smaller affine hull.

For s>=S the feasible basis set is fixed. The slope of each eventual vertex
satisfies every direction inequality, because its slack stays nonnegative as
s tends to infinity. The slope therefore lies in the entire H_a. Consequently
every vertex at S+u is a vertex at S plus u times a point of H_a. The reverse
inclusion follows by adding every original inequality. For every real u>=0,

    H_(b+(S+u)a) = P+u H_a.                         (1)

Its dimension is fixed for u>=0 because the feasible active-basis incidence
is fixed. Since the right side contains a translate of u H_a, W lies in the
parent direction space. This proves the quotient dimension above.

## Closed-axis polynomiality and the whole quotient identity

The hives may be rational polytopes. Choose a common positive integer L such
that L P and L Z are lattice polytopes. The multivariate Ehrhart theorem gives
a polynomial F(x,y) counting x L P+y L Z for all nonnegative integers x,y,
including the axes, with y-degree at most r. For each integer u>=0, (1) gives

    P_(b+(S+u)a)(L t)=F(t,u t).

Both sides are polynomials in t: on the left use whole LR polynomiality.
Equality on all nonnegative integers proves their polynomial equality, hence

    P_(b+(S+u)a)(t)=F(t/L,u t/L).                    (2)

This argument retains the original stretch t; denominator clearing is an
intermediate proof step, not a new counting lattice or a period assignment
to arbitrary intermediate pieces. The right side is a polynomial in (t,u).
Its u-degree is at most r, and its coefficient of u^r is divisible by t^r.

Let V>0 be the ordinary r-volume of H_a in Lambda intersect W. Fix a positive
integer t. Each lattice point of t K has an integral lift in Lambda, by the
definition of the quotient lattice. Its fiber in t P is a nonempty bounded
real convex set in a translate of W, possibly with no initial lattice point.
After adding ut Z, the leading lattice-count growth in that fiber is
u^r t^r V. A translate of ut Z inside the fiber sum gives the lower bound;
a fixed bounded thickening of ut Z gives the upper bound. Their leading
normalized volumes coincide. Rational facets give lower-order boundary errors.
This includes initially lattice-empty real fibers; none is discarded.

There are finitely many points of t K. Sum those leading terms and compare
with the polynomial (2). This proves

    [u^r] P_(b+(S+u)a)(t) = V t^r E_K(t),
    Delta_u^r P_(b+(S+u)a)(t) = r! V t^r E_K(t),     (3)

where E_K(t)=#(t K intersect barLambda). Divisibility already established in
(2) makes E_K a polynomial on positive integers. Clear the vertex denominators
of K and compare with its integral Ehrhart polynomial: its constant is one
and its degree is the actual dim K. A point quotient is consequently one.

## Face volumes in the saturated lattices

Fix an actual j-face G of K, j>=1. Pull back an exposing quotient functional.
It annihilates W, so the corresponding face of P+u Z is
F_G(0)+u Z and projects onto all of G. For u>0 its dimension is r+j. Distinct
faces G give distinct exposed parent faces. The full direction lattices fit in

    0 -> Lambda intersect W
      -> Lambda intersect lin(F_G(u)-F_G(u))
      -> barLambda intersect lin(G-G) -> 0.         (4)

This sequence is exact and splits over the integers. To see surjectivity,
the parent face direction is precisely pi^(-1)(lin(G-G)) within the parent
span; an integral representative of a quotient lattice vector therefore lies
in this direction space. Freeness of the quotient gives an integral splitting.
Normalized volume disintegrates with these measures. In every real fiber over
G, division by u^r leaves the volume V of the full direction body Z, so

    lim_(u -> infinity) vol_Lambda(F_G(0)+u Z)/u^r
        = V vol_barLambda(G).                     (5)

No Euclidean covolume, factorial, primitive-index or residue factor is added.
Apply the complete parent bound at index r+j, retain the distinct faces above,
divide by u^r and take nonnegative integral u to infinity. The left side tends
to V [t^j]E_K by (3). Every omitted parent-face term was nonnegative. Thus

    [t^j]E_K >= epsilon_(r+j)
                 sum_(actual j-faces G of K) vol_barLambda(G) > 0. (6)

There are actual j-faces whenever 1<=j<=dim K. Since r+j<=dim P<=10,
every required epsilon is among the protected parent indices. In particular
r=1,j=1 uses the full c2 margin 1/200000000. This is the formerly missing
linear coefficient of a whole segment quotient. For r>=2 the inherited c3
and higher margins already suffice. Zero-dimensional directions were excluded
at the start and do not obtain this conclusion by the same argument.

## Segment directions and the exact eventual threshold

Suppose r=1, with P_a(t)=1+ell t and ell>0. Closed-axis polynomiality (2)
and the direction axis give

    c1(H_(b+(S+u)a)) = C1+ell u,
    C1=c1(P).                                      (7)

The coefficient of u in the linear t term is precisely the linear Ehrhart
coefficient of the whole direction, not a selected edge. Therefore every
integer u>=max(0,floor(-C1/ell)+1) makes (7) positive. The complete parent
bounds make every higher coefficient through actual degree strictly positive;
constant one and the actual-degree convention remain. A one-dimensional
parent has no higher coefficient to check.

For an explicit estimate, write A_a=|lambda_a| and
B=A+(22528 A+1)A_a. A complete LR tableau at stretch t is determined by ten
triangular row counts, each in [0,t B]. Explicitly, let x_(i,j) count color j
in tableau row i; the ballot condition gives j<=i. Choose the ten x_(i,j)
with 1<=j<i<=5. The first five row lengths determine their diagonal entries;
then the six content totals determine row six, with the last row-length
constraint following from total size. Thus every tableau is uniquely recovered
from these ten bounded integers, and

    0<=P(t)<=(t B+1)^10.

Interpolate the whole degree-at-most-ten polynomial at t=0,...,10 in the
Newton basis binom(t,k). Every k-th finite difference is at most
2^k(10B+1)^10 in absolute value. The sum of absolute ordinary coefficients of
binom(t,k) is one (also for k=0), from its falling product. Hence each
ordinary coefficient, including C1, has absolute value at most

    sum_(k=0)^10 2^k(10B+1)^10 = 2047(10B+1)^10.    (8)

The slope ell=P_a(1)-1 is a positive integer, hence at least one. Combining
(7)-(8), m=S+u satisfies a sufficient bound

    m >= 22528 A+2+2047(10(A+(22528 A+1)A_a)+1)^10.  (9)

For a whole segment direction of outer area 28 and length one, (9) specializes
to m>=22528 A+2+2047(6307850 A+281)^10. The general statement (9) requires
no choice or reconstruction of a preferred direction.

## Attribution and limits

Equations (1)-(3) use the whole stabilization and quotient construction of
Pro028. Pro031 supplied the strengthened saturated face-volume transfer and
the whole-tableau coefficient-height bound. A17's full c2 certificate and its
quotient consequence close the remaining r=j=1 case. The analytic argument
here expands those accepted dependencies for the reader; it does not infer
truth from an internal acceptance label. The underlying parent finite bounds
remain linked above and must be reproduced at their complete stated scopes.

The threshold is deliberately loose. It is not an optimal m, a finite
unbounded-area census, or a mechanism proving the sign of an initial parent.
The later complete rank-six theorem separately settles those initial signs.
No higher ordinary-rank result, arbitrary projection theorem or LR rank for K
is asserted. Normalizing a proper face or quotient as if it were a new ordinary
LR example would change the subject.
