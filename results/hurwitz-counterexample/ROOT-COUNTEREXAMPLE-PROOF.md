# Campaign verification of a stretched LR polynomial with right-half-plane roots

The explicit example was proposed by GPT 6 Pro in the captured return. A fresh
Astra verification lane received only the bare triple and outer-partition
convention, independently derived its degree bound and counting algorithm,
and sealed the full polynomial before any comparison with returned data.
The root then independently recomputed both root certificates from that
campaign polynomial. Returned code was not executed or imported.

## The exact LR object and full polynomial

Let lambda=(18,17,...,1), mu=(17,16,...,1), and nu=(7,6,5). The outer
size is171=153+18, outside both original-box bounds. At stretch t the skew
diagram t lambda/t mu has eighteen rows of length t with disjoint column
intervals. Its skew Schur function is therefore h_t^18, and

`P(t)=c^(t lambda)_(t mu,t nu)=K_((7t,6t,5t),(t^18))`.

The independent lane's ROOT-DEGREE-AND-METHOD.md derives the Weyl coefficient
extraction and an exact two-dimensional triangular-convolution recurrence.
It also supplies separate direct-convolution, positive horizontal-strip
tableau and hook-length controls. These are campaign-owned implementations,
not wrappers around returned code.

Before any count, the degree bound was justified by the GT/tableau chain.
The nonterminal partitions at levels1 through17 have at most1,2,3,...,3
coordinates,48 in total. Each level has its independent fixed-size equation;
the17 equations occupy disjoint coordinate blocks. The bounded polytope
therefore has dimension at most31. Stretched LR polynomiality, together with
the all-stretch Schur identity above, makes its count a polynomial of degree
at most31. See Rassart, <https://arxiv.org/abs/math/0308101>; the dimension
bound is independently derived here rather than inferred from finite differences.

All32 values at t=0,...,31 were computed exactly. Newton and Lagrange
reconstruction agree, and held-out t=32,33,37 agree. The positive leading
coefficient establishes actual degree31. All32 ordinary coefficients are
strictly positive. The complete coefficient vector and independent source
seal are in ROOT-POLYNOMIAL.json and README.md.
The independent polynomial matches every returned coefficient exactly.
Checks of the37 provider-saved chain values, including t=100, are arithmetic
comparisons against this independently determined polynomial, not claims
that the campaign reran the provider's chain executable.

## Exact Rouché disk

Clear the polynomial's positive rational scale to obtain the integer
polynomial Q. Let

`c=1370566/10^9 + i*414381092/10^9`, `r=1/10^6`.

The root computed every Taylor coefficient
`a_k=sum_(j=k)^31 Q_j binomial(j,k)c^(j-k)` using pairs of exact rationals.
For `||z||_1=|Re z|+|Im z|`, put

`U=||a0||_1 + sum_(k=2)^31 ||ak||_1 r^k`,
`L=max(|Re a1|,|Im a1|) r`.

The exact inequality is `0<=U<L`, with `U/L<1/1000`. On |w|=r the constant
and nonlinear terms have magnitude at most U, while |a1 w| is at least L.
Rouché's theorem therefore gives exactly one zero of Q(c+w) in that disk.
The disk's left margin is `684783/500000000>0`; it lies wholly in the open
right half-plane. Its conjugate is disjoint and contains a second zero.
Floating approximations play no role in this verification.

## Exact total root count

The independently written Routh recurrence initializes its first two rows
from descending alternating coefficients. If the preceding rows are A and B,
the next entry is `(B0*A_(j+1)-A0*B_(j+1))/B0`. Each row is rescaled only by
a positive rational factor to retain small integer entries and preserve signs.
There is no zero pivot or zero row; otherwise this implementation refuses.
Stable and unstable quadratic controls give zero and two sign changes.

For Q, the first-column signs are positive through the t² row, negative in
the t row, and positive in the constant row. The standard nonzero-pivot Routh
criterion therefore gives exactly two open-right-half-plane roots. The full
integer column and exact disk bounds are in ROOT-CERTIFICATE.json.

## Scope and significance

This is a counterexample to the campaign's global Hurwitz Conjecture R, not
to ordinary coefficient positivity. It changes no original-box coverage,
does not refute the local real-rooted cone formulas, and establishes no
global minimality. It rules out universal Hurwitz stability as a sufficient
route to the main positivity conjecture. Its novelty and publication scope
require separate primary-source and expert assessment; a campaign conjecture
is not automatically a named conjecture in the literature.
