# Independent bare-triple derivation, frozen before numerical execution

Input: outer lambda=(18,17,...,1), inner mu=(17,16,...,1), and
nu=(7,6,5). This degree and counting derivation was made from the ordinary triple
before the proposed polynomial or coefficient data were consulted.

## Reduction to a Kostka number

For row i=1,...,18 of t*lambda / t*mu, the occupied columns are
t*(18-i)+1,...,t*(19-i). These are 18 disjoint column intervals, each
containing t cells. Thus the semistandard filling choices in separate rows
are independent and the skew Schur function is h_t^18. Its Schur
coefficient at shape (7t,6t,5t) is the desired LR coefficient. Repeated
Pieri, equivalently the Schur expansion of a product of complete functions,
identifies this coefficient with K_((7t,6t,5t),(t^18)).

## A degree bound obtained before interpolation

Use the nested shapes q^(k) of the cells labelled at most k in such a
semistandard tableau, k=1,...,18. The fixed top shape is
q^(18)=(7t,6t,5t,0,...,0). Interlacing is
q^(k+1)_i >= q^(k)_i >= q^(k+1)_(i+1), and the fixed content gives
sum_i q^(k)_i=k*t.

Each q^(k) has at most min(k,3) potentially nonzero entries. There are
1+2+15*3=48 entries across k=1,...,17. On each level the sum equation
determines one entry from the others; the equations involve disjoint
levels, hence are 17 independent affine equations. The remaining 31
integer coordinates lie between 0 and 7t. Consequently the tableau count
is at most (7t+1)^31. This bound is elementary and does not presume that
the associated polytope has integral vertices or full dimension.

Rassart's polynomiality theorem for stretched LR coefficients implies
that this count agrees with a polynomial for positive integral t.
Therefore its degree is at most 31: a nonzero polynomial of larger degree
cannot satisfy the displayed growth bound. The rational-polytope Ehrhart
description supplies its value 1 at t=0 (the original feasible polytope
is nonempty; for example a standard tableau of shape (7,6,5) exists).
The coefficient extraction at t=0 below also gives 1. Thus 32 exact
values at t=0,...,31 determine the entire stretching polynomial.

Primary source read directly: Etienne Rassart, "A polynomiality property
for Littlewood-Richardson coefficients", arXiv: math/0308101v2,
https://arxiv.org/pdf/math/0308101. Only the general polynomiality and
Ehrhart statements are used; the degree bound above is specific to this
input and derived independently. No coefficient-sign assertion is taken
from that source.

## Exact coefficient extraction

Let H_t(x,y)=sum_(a,b>=0,a+b<=t) x^a y^b and let
A_t(a,b)=[x^a y^b] H_t(x,y)^18, with negative exponents assigned zero.
In three variables, multiplying h_t^18 by
(x-y)(x-z)(y-z) and extracting x^(7t+2)y^(6t+1)z^(5t)
selects exactly the Schur coefficient at (7t,6t,5t), by the alternant
formula. Homogeneity then gives

P(t) = A_t(7t,6t) - A_t(7t,6t+1) - A_t(7t+1,6t-1)
       + A_t(7t+1,6t+1) + A_t(7t+2,6t-1) - A_t(7t+2,6t).

The fast counter multiplies by H_t eighteen times. The identity

(1-x)(1-y)H_t = 1 - sum_(i=0)^(t+1) x^i y^(t+1-i)
                    + xy*sum_(i=0)^t x^i y^(t-i)

turns each triangular convolution into two prefix recurrences and two
antidiagonal segment sums. This is O(18*t^2) exact integer arithmetic.
Truncation to a<=7t+2,b<=6t+1 is safe because all exponents are
nonnegative. Every intermediate output coefficient is checked >=0.

A separate positive tableau recurrence adds one horizontal t-strip per
label. From old partition (a,b,c), it considers increments da,db,dc>=0
with da+db+dc=t and b+db<=a, c+dc<=b. These are exactly the horizontal
strip interlacing conditions. Its states stay inside (7t,6t,5t).
This control shares neither the alternant subtraction nor the fast
convolution identity. A direct unaccelerated convolution is also present
as a recurrence control. Controls are bounded to t<=8.

## Frozen numerical plan

- Interpolation nodes: 0 through 31 inclusive; exact rational arithmetic.
- Holdouts, not used in interpolation: 32, 33, 37.
- Small-case controls: direct convolution and positive tableau recurrence.

The [standalone reproduction](README.md) gives the public counting command
and complete verification data.

This file records a prior degree bound, not an observed interpolation degree.
