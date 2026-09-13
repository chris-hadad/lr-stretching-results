# Higher ordinary coefficients need not be concave in the weights

Let k>=2 and let C,x be nonnegative integers with C>=(k+1)x. For

    beta(x) = (C-kx, C-x, x,...,x),

with k+1 final copies of x, the straight two-row Kostka stretch is exactly

    K_(t(C,C), t beta(x)) = binom(xt+k,k).

Consequently every ordinary coefficient index j>=2 admits a failure of
concavity in the weights with the straight shape fixed. This is not a negative
ordinary coefficient: every polynomial in the displayed family has
nonnegative ordinary coefficients.

## Proof of the identity

Set q=xt, A=(C-kx)t, B=(C-x)t and F(z)=(1+z+...+z^q)^(k+1).
For G_a(z)=1+z+...+z^a, the two-row Jacobi–Trudi identity expresses the
Kostka number as `[z^(Ct)](1-z)G_A(z)G_B(z)F(z)`.

Since A<=B, the first factor has coefficients +1 in degrees 0 through A,
zero through B, and -1 in degrees B+1 through A+B+1. The inequality
Ct>=(k+1)q shows that the first contribution sums F's coefficients from
kq through (k+1)q, while the second subtracts those from 0 through q-1.
The degree-(k+1)q polynomial F is palindromic. Their difference is therefore
[z^q]F. No bound on a composition part binds at total q, giving binom(q+k,k).
This also holds at x=0 and t=0.

Expanding the product gives

    [t^j] K = e_j(1,1/2,...,1/k) x^j.

For 2<=j<=k the multiplier is strictly positive. At fixed C=2(k+1), the
weights beta(1) are the midpoint of beta(0) and beta(2), and the coefficient
gap is e_j(1,1/2,...,1/k)(1-2^(j-1))<0. Choosing k>=j proves the statement
for every j>=2.

The failure is also present when every weight is positive: fix C=3(k+1)
and use x=1,2,3. Strict convexity of x^j gives the same strict midpoint
failure. Thus zero-weight endpoints are not essential. This corollary follows
from the same identity; no new global search is involved.

For k=2,C=6 the three polynomials are

    1, 1+(3/2)t+(1/2)t^2, 1+3t+2t^2,

and the quadratic midpoint gap is -1/2. The middle polynomial is the
ordinary LR stretch with outer lambda=(12,8,3,2,1), inner mu=(8,3,2,1),
and nu=(6,6). Put rows of lengths beta_i in consecutive disjoint column
intervals: their skew Schur function is product_i h_(t beta_i), proving
the ordinary LR identity at every stretch. The outer size is 26 and rank 5.
This example is a concavity obstruction consistent with rank-five positivity.

Concavity of c_j, concavity of c_j^(1/j), and coefficientwise monotonicity
under balancing are different properties. This result refutes only the
first general assertion. It does not refute the other two.

## General two-row skew formula

For m>=2 nonnegative integer weights beta, write W=sum beta, d=m-1 and
assume 0<=w<=v, 2v<=W, max beta<=W-w. Put alpha=(W-w,v) and gamma=(v-w,0).
The entire skew Kostka stretch equals the difference of bounded-composition
coefficients

    P(t) = [z^(vt)] product_i G_(beta_i t)(z)
           - [z^(wt-1)] product_i G_(beta_i t)(z).

Equivalently P is the coefficient of s_(t alpha) in
h_(t(v-w)) product_i h_(t beta_i), so the same disjoint-row construction
realizes it as a full ordinary LR count. The displayed feasibility conditions
ensure the two-row shape dominates these weights; in particular P(0)=1.

For beta_S=sum_(i in S) beta_i, exact inclusion–exclusion gives

    P(t) = 1_(v=0)
      + sum_(beta_S<v) (-1)^|S| binom((v-beta_S)t+d-|S|,d)
      - sum_(beta_S<w) (-1)^|S| binom((w-beta_S)t+d-1-|S|,d).

The binomials here are falling-factorial polynomials. First establish this
identity for sufficiently large positive t: positive slopes contribute those
polynomials, negative slopes contribute zero, and zero slopes leave exactly
the constant term shown. Ordinary stretched-LR polynomiality extends the
identity to all t. This is also a prior degree bound d, independent of a fit.
Zero beta entries are permitted and cancel as dictated by inclusion–exclusion.

Writing H_n=sum_(i=1)^n 1/i and H_n^(2)=sum_(i=1)^n 1/i^2, expansion gives

    c2 = (v^2/2)(H_d^2-H_d^(2))
      - sum_(s=1)^d (H_(d-s)-H_(s-1))/(s binom(d,s))
                       sum_(|S|=s) (v-beta_S)_+^2
      - sum_(s=0)^(d-1) (H_(d-1-s)-H_s)/((d-s)binom(d,s))
                       sum_(|S|=s) (w-beta_S)_+^2.

For the first sum, the product defining binom(a t+d-s,d) has one zero
constant factor. The other constants have product
(-1)^(s-1)(d-s)!(s-1)! and reciprocal sum H_(d-s)-H_(s-1).
The inclusion–exclusion sign produces the stated minus sign. The second
sum follows with offset d-1-s and product (-1)^s(d-1-s)!s!.
Its potentially exceptional s=d positive-slope case is excluded by
max beta<=W-w. This proves the formula, including d=1 and zero endpoints.

## Independent verification and attribution

The identity, nonconcavity construction and quadratic formula were proposed
with GPT 6 Pro assistance. The present proof and standard-library code
were developed and checked separately with Codex; the initially proposed
implementation files were not used. Classical Schur, Jacobi–Trudi and
stretched-LR polynomiality are the mathematical inputs. Historical novelty
has not been established; the elementary construction is not presented as
an already peer-reviewed theorem or a priority claim.

`two_row.py` independently compares finite geometric-series DP with a positive
horizontal-strip Pieri chain, verifies the symbolic formula and 90 strict
midpoint gaps, and exercises zero-weight and capped endpoints. Its small
reproduction performs 594 family count comparisons and 241 endpoint count
comparisons. The argument above, not these finite controls, proves the
all-k statement.

Separately, independent verification recomputed all 6,000 saved full-polynomial objects
in the 3,000 balancing comparisons using all d+1 determining values and two
holdouts, for 65,670 exact count comparisons, with 192 positive Pieri checks.
The 5,000 quadratic-only comparisons also passed independent harmonic-formula
replay. No balancing decrease or negative ordinary coefficient occurred on
those exact finite rosters. These panels do not establish universal balancing
monotonicity and are not needed to reproduce the theorem module.
