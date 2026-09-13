# Positive weights with lower row of slope three

Codex derivation, 12 September 2026 UTC. This develops the lower-row-slope-three
formula from the preceding two-row work. The argument combines the inequalities
below with the exact finite expansion described in the
[public verification module](../../replay/README.md).

## Statement and whole-LR count

Let `n >= 6`, let `w_1,...,w_n` be positive integers, and put
`W = sum w_i`, `lambda_i = sum_{j=i}^n w_j`, `mu_i = lambda_{i+1}` (with
`lambda_{n+1}=0`), and `nu=(W-3,3)`. The entire stretched LR polynomial has
positive ordinary coefficients through its actual degree. Its degree is
`n-2`, except when `n=6` and all weights are one, when its degree is three.
This covers a particular disjoint-row family at every rank, not all two-row
LR coefficients and not KTT in general.

The skew diagram `lambda/mu` has horizontal rows with pairwise disjoint
column sets. Thus its skew Schur function is `product h_{w_i}`. Evaluating
in two variables and extracting the GL(2) highest weight gives, at stretch t,

`P(t) = [x^(3t)] (1-x) product_i (1+x+...+x^(w_i t))`.

Write `d=n-2`, `u=#{i:w_i=1}` and `v=#{i:w_i=2}`. Inclusion-exclusion gives
the exact polynomial identity

`P(t) = binom(3t+d,d) - u binom(2t+d-1,d)
        - v binom(t+d-1,d) + binom(u,2) binom(t+d-2,d)`.

For integer `t>=1`, the contributing subsets are empty, a single weight one,
a single weight two, or two weights one. Every other subset has total weight
at least three and positive cardinality, so its coefficient index is negative.
When the last displayed term has an out-of-range upper entry at a small t,
the polynomial binomial is zero there as well. At `t=0` the formula is one.
This derives the whole count, without fitting finitely many evaluations.

## The all-unit profile minimizes every nonconstant coefficient

Put `C(t)=binom(t+d-1,d)` and `D(t)=binom(t+d-2,d)`. For `1<=k<=d`,
`C_k=[t^k]C` is positive. Two polynomial identities give

`D_k/C_k >= -1/(d-1)` and `D_k/C_k <= (k-1)/(d-1)`.

For the first, `(d-1)D+C = (d/d!) t^2 product_{j=1}^{d-2}(t+j)`.
For the second, the following expression has nonnegative coefficients:

`t C' - C - (d-1)D
 = C/(t+d-1)
   + sum_{j=1}^{d-2} ((d-j)t+j) C/((t+j)(t+d-1))`.

Every quotient shown is a polynomial with nonnegative coefficients.
Moreover `D_1=-1/(d(d-1))<0` and
`D_2=(1-H_{d-2})/(d(d-1))<0` for `d>=4`.

For fixed u, each nonconstant coefficient of P decreases as v increases,
so its minimum over `0<=v<=n-u` occurs at `v=n-u`. Along those profiles,
increasing u to u+1 changes its kth coefficient by

`-(2^k-1) C_k + u D_k`.

This is strictly negative for k=1,2. For `3<=k<=d`, when `D_k>0`, use
`u<=n-1=d+1` and
`u D_k/C_k <= (d+1)(k-1)/(d-1) <= k+1 < 2^k-1`.
When `D_k<=0` strict negativity is immediate. Consequently the all-unit
profile `u=n,v=0` is the unique minimum of every nonconstant coefficient
among these profiles. Any non-unit weight strictly raises all coefficients
of indices 1 through d above that minimum.

## Positivity of the uniform minimum

It remains to prove coefficient nonnegativity of

`P*_d(t)=binom(3t+d,d)-(d+2)C(2t)+(d+2)(d+1)D(t)/2`.

Let `a=(1,1/2,...,1/(d-1))` and let `e_j` be its elementary symmetric
functions, with `e_0=1`. The coefficient ratio of the first term to C is

`A_k/C_k = 3^k (1+d e_k/e_{k-1})
          >= 3^k (d^2-k)/(k(d-1))`.

Indeed, summing over the `(k-1)`-subsets gives
`k e_k >= (d-k)e_{k-1}/(d-1)`; this also covers k=d.
Together with the lower bound for D, this gives

`P*_{d,k}/C_k >= L_{d,k}
 = 3^k(d^2-k)/(k(d-1)) - (d+2)2^k
   - (d+2)(d+1)/(2(d-1))`.

For `d>=21`, the k=1 and k=3 bounds simplify respectively to
`d(d-7)/(2(d-1))` and `(d^2-19d-24)/(2(d-1))`, both positive.
For `k>=4`, the first coefficient ratio is at least `3^k d/k`.
Since `(3/2)^k/k >= 81/64` and `17d/64-2>0`, the bound is at least

`16(17d/64-2) - (d/2+2+3/(d-1))
 = 15d/4-34-3/(d-1) > 0`.

For k=2, let `H=sum a`. Since `sum a_i^2<=H`,
`e_2>=H(H-1)/2`. The resulting lower bound is
`P*_{d,2}/C_2 >= (9/2)dH-9d-1-3/(d-1)`.
For `d>=5`, `H>=H_4=25/12`, so this is at least
`3d/8-1-3/(d-1)>0` (already `1/8` at d=5, and increasing).

For `4<=d<=20`, the accompanying independent exact-rational expansion checks
all coefficients, with no numerical fitting or floating point. The verified
finite result is positivity for `5<=d<=20` and
`P*_4(t)=1+2t+3t^2/2+t^3/2`. The [public verification module](../../replay/README.md)
provides these finite expansions, which are required premises of the proof.

These finite cases and the inequalities prove the statement. In the single
uniform d=4 exception the leading coefficient vanishes; every non-unit
profile strictly raises it. All constants are one. No lattice rescaling,
face count or negative summand is substituted for the whole polynomial.

## Credit and next question

The disjoint-row two-variable setup and the slope-three inclusion-exclusion
formula come from the preceding GPT-6 Pro derivation. The coefficientwise
profile comparison and uniform positivity proof are Codex contributions.
Alper Ferudun's rank-at-most-five positivity and high-coefficient methods
remain prior results and are not claimed here as new contributions.

The next open question is whether analogous profile comparisons and uniform
positivity can handle general fixed lower-row slope. It remains open here;
the extra alternating subset terms may obstruct the present monotonicity.
