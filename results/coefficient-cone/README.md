# Positive linear and quadratic coefficients on a rank-18 LR cone

This note proves two coefficient bounds for an explicit infinite family of
ordinary Littlewood–Richardson stretching polynomials. A short exact program
reconstructs the finite certificate from the nine Schur factors.

## Theorem

Let x,y be nonnegative integers, h=x+y>0, and let the multiset of partitions be

\[
\mathcal T(x,y)=\{(8x+y,h)^{\times3},\ (5h,3h),\
(3h,2h)^{\times2},\ (x+8y,h)^{\times3}\}.
\]

Define

\[
P_{x,y}(t)=[s_{(17ht,17ht,17ht)}]\prod_{\tau\in\mathcal T(x,y)}s_{t\tau},
\qquad c_j(x,y)=[t^j]P_{x,y}(t).
\]

These are coefficients in the **ordinary monomial basis in t**. For every
such x,y,

\[
c_0(x,y)=1,\qquad
c_1(x,y)\geq\frac{275511}{20020}h>0,\qquad
c_2(x,y)\geq\frac{704687791}{7207200}h^2>0.
\]

Both bounds are attained on both boundary rays x=0 and y=0. The functions
c1 and sqrt(c2), extended homogeneously to the nonnegative real parameter
cone and continuously by zero at the origin, are concave and superadditive.
The assertion of concavity for c2 itself is restricted to the normalized
one-dimensional slice below.

The full stretch degree is at most 19. Coefficients c3 through c19 are not
computed here; positivity of the full polynomial is not asserted.

## An explicit ordinary LR boundary

The tensor multiplicity above is one ordinary LR coefficient

\[
P_{x,y}(t)=c^{\,t\lambda(x,y)}_{\,t\mu(x,y),\,t\nu(x,y)},
\]

with lambda the outer partition, lambda=x lambda_x+y lambda_y,
mu=x mu_x+y mu_y, and nu=(17h,17h,17h). The generators are

```text
lambda_x = (38,31,30,23,22,15,14,12,9,8,6,5,3,3,2,2,1,1)
mu_x     = (30,30,22,22,14,14,9,9,6,6,3,3,2,2,1,1)
lambda_y = (38,38,37,37,36,36,35,33,30,29,27,26,24,17,16,9,8,1)
mu_y     = (37,37,36,36,35,35,30,30,27,27,24,24,16,16,8,8)
```

They have 18 nonzero outer rows, with
|lambda|=225x+477y, |mu|=174x+426y, and |nu|=51h.

To prove the identity, order the nine factors as displayed and set
o_i=sum_(j>i) tau_(j,1). Form lambda by concatenating o_i+tau_(i,k), and
mu by concatenating o_i for each positive row of tau_i, omitting trailing
zeros. This produces partitions: the first row of the next block equals
o_i, below every positive row of the preceding shifted block. Block i
uses columns o_i+1 through o_i+tau_(i,1); all later blocks use columns at
most o_i. Thus distinct blocks share neither rows nor columns, and their
semistandard tableaux vary independently:

\[
s_{\lambda/\mu}=\prod_i s_{\tau_i}.
\]

Extracting s_nu proves the asserted identity, and dilation preserves the
construction. The program reconstructs both boundary generators.

For the degree bound, in a central GL3 tensor product of n>=3 factors the
final determinant pairing fixes its partner highest weight. The remaining
chain has n-3 variable intermediate partitions, with at most two coordinates
each, and n-2 rank-three LR interval variables. Its bounded rational polytope
has dimension at most 2(n-3)+(n-2)=3n-8. Stretched LR polynomiality therefore
gives degree at most 19 when n=9.

## Exact coefficient calculation

Normalize h=1 and put s=(4x-3y)/h in [-3,4]. The factors become
(4+s,1)^3,(5,3),(3,2)^2,(5-s,1)^3, with target (17,17,17).
Rational parameters are interpreted by clearing denominators; homogeneity
then recovers the coefficients for every integral x,y.

Let delta=(2,1,0), u=z2/z1 and v=z3/z2. The GL3 Weyl denominator is
z^delta(1-u)(1-uv)(1-v). Multiplying the nine characters by this denominator
leaves the product of their nine alternants over its eighth power. Highest
weight extraction consequently asks for the product numerator, multiplied
by ((1-u)(1-uv)(1-v))^(-8), at exponent (17t,17t,17t)+9delta.

Suppose a signed numerator state has first exponent (a+da*s)t+c and third
exponent (b+db*s)t+d. Its contribution is its multiplicity times F(A,B), where

\[
A=(a-17+da\,s)t+c-18,\qquad B=(17-b-db\,s)t-d,
\]

\[
F(A,B)=\sum_{k=0}^{\min(A,B)}
\binom{A-k+7}{7}\binom{k+7}{7}\binom{B-k+7}{7}.
\]

The term is zero if either coordinate is negative. Expanding the nine
six-term alternants and aggregating identical states gives 67,458 nonzero
states. All possible branch changes occur at zeros of

\[
a-17+da\,s,\qquad17-b-db\,s,\qquad a+b-34+(da+db)s.
\]

Their zeros in [-3,4], together with the endpoints, give exactly

```text
-3, -8/3, -5/2, -7/3, -2, -5/3, -3/2, -4/3, -1,
-2/3, -1/2, -1/3, 0, 1/3, 1/2, 2/3, 1, 4/3, 3/2,
5/3, 2, 7/3, 5/2, 8/3, 3, 10/3, 7/2, 11/3, 4.
```

These 29 walls delimit 28 open intervals. The sign of an affine coordinate
at sufficiently large t is determined lexicographically by its slope and
offset. Every wall is evaluated with this rule, including the zero-slope
cases. An interval midpoint is used only to select a branch.

On A>=B>=0, expand the original summand as

\[
\frac{1}{(7!)^3}\prod_{i=1}^7(A-k+i)(k+i)(B-k+i).
\]

Each power of k is summed using the exact telescoping recurrence

\[
S_j(B)=\frac{(B+1)^{j+1}-\sum_{i=0}^{j-1}\binom{j+1}{i}S_i(B)}{j+1},
\qquad S_j(B)=\sum_{k=0}^{B}k^j.
\]

This yields Q(A,B)=22! F(A,B), a degree-22 polynomial with 156 nonzero
integer monomials. For the other branch, interchange A and B. If
A=alpha*t+c and B=beta*t+d, the first three coefficients of Q(A,B) are

\[
Q(c,d),\qquad Q_A(c,d)\alpha+Q_B(c,d)\beta,
\]

\[
\tfrac12Q_{AA}(c,d)\alpha^2+Q_{AB}(c,d)\alpha\beta+
\tfrac12Q_{BB}(c,d)\beta^2.
\]

After division by 22! and signed summation over the numerator, these give
the complete c0,c1,c2 formulas on each open interval and their actual wall
values. No stretch interpolation is involved. The character identity is
eventually valid on each ray; stretched LR polynomiality identifies its
polynomial continuation with the full stretching polynomial.

## Bounds and concavity

The generated certificate checks, using exact rational arithmetic:

- c0=1 on every piece;
- continuity at all 29 separately evaluated walls;
- affine c1 pieces with nonincreasing slopes;
- strictly negative second derivatives on all c2 pieces;
- strictly downward c2 first-derivative jumps at all 27 internal walls;
- equal endpoint minima 275511/20020 and 704687791/7207200.

Continuity and these derivative conditions prove that c1 and c2 are concave
on [-3,4]. Their minima are therefore the stated endpoint values. Since
c2>0, composition with the increasing concave square root also proves
concavity of sqrt(c2) on this slice.

Ordinary coefficient homogeneity gives
c1(x,y)=h c1(s) and sqrt(c2(x,y))=h sqrt(c2(s)). In a convex combination
of parameter points, the resulting s is the average of their s values
with weights proportional to their h values. The slice concavity inequality,
multiplied by the combined h, proves cone concavity. Degree-one homogeneity
then gives G(u+v)>=G(u)+G(v) for G=c1 and G=sqrt(c2). Their bounded slice
values give a continuous extension by zero at the origin.

## Reproduction and files

Run from this directory with Python 3 and its standard library:

```bash
python3 reproduce.py
```

The program takes no mathematical input files and writes none by default.
Use `--output-dir DIRECTORY` to save the reconstructed mathematical data:

- `certificate.json`: all 28 chamber formulas, 29 actual wall values,
  derivative inequalities, exact bounds, and the LR boundary generators;
- `numerator.json`: all 67,458 signed numerator states;
- `flow-polynomial.json`: all 156 integer monomials of 22! F(A,B).

The supplied files record the same independently reconstructed data. An error
in any required exact identity or inequality terminates the calculation.
The rational entries are serialized as strings. In
`chambers[i].coefficients_in_s[j]`, the list gives ascending powers of s
for the ordinary t coefficient cj. A negative s-squared term is parameter
curvature; the ordinary quadratic coefficient is the entire c2(s) function.

## Attribution and mathematical antecedents

The family and initial coefficient formulas were proposed in the GPT-6 Pro
research note *SLR-GPT6-PRO-WILDCARD-004* (2026). This package is an
independently written exact reconstruction. The Weyl character formula,
disconnected-skew-shape factorization, and finite power-sum identities are
classical ingredients.

The polynomiality premise is the standard theorem on stretched LR
coefficients; see E. Rassart, *A polynomiality property for Littlewood–Richardson
coefficients*, J. Combin. Theory Ser. A 107 (2004), 161–179
([arXiv:math/0308101](https://arxiv.org/abs/math/0308101)), and W. Thawinrak,
*A Short Proof for the Polynomiality of the Stretched Littlewood–Richardson
Coefficients*, Ars Combinatoria 162 (2025), 205–212
([arXiv:2211.06810](https://arxiv.org/abs/2211.06810)).
