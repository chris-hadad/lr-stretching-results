# Defect two and weighted straight-GT interiors

This derivation extends [The interior staircase shift at arbitrary height](GENERAL-HEIGHT.md)
to nonuniform positive contents and uses the resulting dominance costs to locate
a whole-LR family. Independent verification of this source derivation and
worldwide priority are not claimed here.

## 1. Two genuine interior counts, with no numerator-positivity assumption

Let P be the period-one Ehrhart polynomial of a nonempty rational polytope in
its saturated relative lattice, with degree d=q+1, q>=2, P(0)=1 and actual
codegree q. Write U=I(q)>0, V=I(q+1), where I(n) counts its actual relative
interior, not a selected set of strict inequalities on a wrong affine hull.
Reciprocity and the roots -1,...,-(q-1) give

    P(t)=binom(t+q-1,q-1) (a t^2+b t+1),
    a=(V-(q+1)U+1)/(q(q+1)) > 0,
    b=(q V-(q+1)^2 U+2q+1)/(q(q+1)).                 (1)

Indeed U=q^2 a-q b+1 and V=q((q+1)^2 a-(q+1)b+1).
Solving these two equations proves (1). If f_i are the ordinary coefficients
of binom(t+q-1,q-1), extended by zero, complete coefficient nonnegativity is
exactly the finite set

    a f_(k-2)+b f_(k-1)+f_k >= 0,  1<=k<=q.         (2)

This is the earlier kernel with a normalized constant. A sufficient stronger
condition is b>=0. Neither this stronger inequality nor (2) is universal for
rational or integral Ehrhart polytopes. Reeve T13 has q=2, U=12, V=48,
a=13/6, b=-7/6 and c1=-1/6. Its role is a non-LR falsifier only.

The exact period-one numerator here is 1+h1*z+U*z^2, with
h1=V-(q+2)U=P(1)-(q+2). It may have a negative entry. No h-star sign is used.

## 2. Full weighted straight-GT model and hypotheses

Let m>=h>=2, alpha_1>...>alpha_h>0 be integral, and let
beta_1>=...>=beta_m>=1 be integral of the same total M. Assume

    Delta_k=sum_(i<=k) alpha_i-sum_(i<=k) beta_i > 0,
                   1<=k<h.                        (3)

For k>=h and k<m strict dominance follows from positive remaining contents.
Define P(t)=K_(t alpha,t beta). Its full tableaux are chains x^(r), r=0..m,
with at most min(r,h) coordinates, fixed x^(0)=0, x^(m)=t alpha,
row sums t(beta_1+...+beta_r), and weak interlacing

    x^(r+1)_i >= x^(r)_i >= x^(r+1)_(i+1),

with missing entries zero. These are all tableau conditions. Eliminating one
coordinate in each nonterminal row, with coefficient one, gives the full
saturated affine lattice Z^D, where

    D=(h-1)m-h(h+1)/2+1.                            (4)

The lattice claim precedes the dimension claim: full dimension follows from
a strict point constructed below. Coordinates are bounded by the terminal
shape, so the polytope is rational and bounded.

For the entire ordinary LR realization, set kappa_j=sum_(i=j)^m beta_i.
Then lambda=kappa, mu=(kappa_2,...,kappa_m), nu=alpha. At every stretch,
lambda/mu consists of column-disjoint rows of lengths beta_1,...,beta_m;
its skew Schur function is the product of the corresponding h's. The Schur
coefficient of s_(t alpha) is K_(t alpha,t beta). This proves a complete
count identity, not just an inclusion or face. The outer rank is exactly m,
outer size sum_i i*beta_i, and |lambda|=|mu|+|nu|. Polynomiality is the
inherited stretched-LR theorem; this theorem supplies no ordinary signs.

## 3. Exact nonuniform staircase formula

Put delta^(r)_i=r+h+1-2i, for 1<=i<=min(r,h). Its row sum is rh. Subtracting
this staircase takes integral strict interlacing to weak interlacing, changes
every content by -h, and changes the top shape by -delta^(m). The full proof
of nonnegative remaining coordinates in the inherited uniform argument uses
only strict interlacing, not equality of contents: the minimal last coordinate
at row h is one, the row-h gaps give 2(h-i)+1, and propagation gives the
entire staircase lower bound. Thus that proof applies unchanged. Conversely,
adding the staircase makes every nonforced inequality strict.

Consequently the candidate integer-interior count is exactly

    I(n)=K_(n alpha-delta^(m), n beta-h*1_m).        (5)

Invalid shifted partitions or negative contents mean zero; all zero data mean
one. Contents remain sorted after subtracting the common constant.

For completeness, weak tableau existence is equivalent to dominance. One
constructive proof removes the smallest content beta_m as a horizontal strip
from the lowest available rows. With j maximal such that lambda_j>=beta_m,
the remaining shape is (lambda_1,...,lambda_(j-1),
lambda_j-beta_m+lambda_(j+1),lambda_(j+2),...). It is a partition. For k<j
its prefix is unchanged; for k>=j its prefix is the old (k+1)-prefix minus
beta_m, which dominates the new content k-prefix because beta_(k+1)>=beta_m.
Repeat. Necessity follows because labels 1,...,k occupy the first k rows.
This is the classical dominance construction, not a new theorem; the original
argument of Fayers and Wildon's account supply the primary exposition.

Applying this criterion to (5) gives exactly

    n beta_m >= h,
    n(alpha_i-alpha_(i+1)) >= 2,                   i<h,
    n alpha_h >= m-h+1,
    n Delta_k >= k(m-k),                          k<h.  (6)

The last line follows because the first k top staircase entries sum to
k(m+h-k), whereas the first k content entries lose kh. For k>=h, dominance
is automatic from nonnegative remaining contents. There are no omitted
subset constraints since the contents are sorted.

For sufficiently large n all (6) hold, so there is a weak shifted chain.
Adding delta and dividing by n supplies a point strict in every nonforced
inequality of the original fixed-weight affine space. Hence its dimension is
exactly D, its relative interior is the strict set just used, and (5) is an
actual relative-interior identity. This avoids circularly assuming dimension.
Rational reciprocity now gives I(n)=(-1)^D P(-n).

The exact codegree is therefore

    q0=max(ceil(h/beta_m), max_(i<h)ceil(2/(alpha_i-alpha_(i+1))),
           ceil((m-h+1)/alpha_h),
           max_(k<h)ceil(k(m-k)/Delta_k)).          (7)

All these inequalities are monotone in n, so there are no later missing
interior grades. Unlike the uniform-content formula, the final dominance
terms are essential for nonuniform contents.

## 4. A structural exclusion, not a global LR theorem

At h=3, m>=6, D=2m-5. All terms in (7), except the k=2 term, are at most
m-1. If Delta_2=1, that final term is 2m-4=D+1; if Delta_2>=2 it is at most
m-2. Thus

    q0<=m-1 OR q0=D+1.                             (8)

In particular q0=D-1 and q0=D cannot occur. In the D+1 case the inherited
high-codegree argument forces P(t)=binom(t+D,D). This is a whole, unbounded-
rank class of straight-Kostka/LR families, not every LR hive of that rank.
Repeated shape parts, zero contents and dominance equalities are outside
(3) and require their actual affine hull. Their exclusion is not a positivity
or impossibility statement about all such degenerations.

At h=4,m=6, D=9, the dominance costs are 5,8,9. Thus the exact conditions

    Delta_1>=1, Delta_2=1, Delta_3>=2               (9)

give q0=8. Every other term in (7) is at most five. This is a genuine rank-six
quadratic-residual stratum and is studied in the associated quadratic-residual family proof. It is not disposed
of by the rank-at-most-five theorem or the q0>=D positivity criterion.

## 5. Verification and boundaries

The proof is an extension of the read uniform staircase source, plus the
explicit dominance calculation. It does not assert hive vertex integrality,
affine hive/GT isomorphism, a Gorenstein shift on the original ray, or equality
of arbitrary polytope interiors under a mere scalar-count coincidence.
The LR conclusion uses the complete all-t count identity. Actual interiors
here are those of this full saturated GT model. Their count equals the
ordinary-LR relative-interior count by equality of full polynomials and the
common actual degree, not by an unproved affine identification.

The associated exact tests and their independence and failure records are
retained in DATA/PHASE5/. No finite test substitutes for (5)-(7).
