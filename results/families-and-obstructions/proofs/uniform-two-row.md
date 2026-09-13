# Uniform rank-two tensor channels: complete ordinary positivity

Derivation dated 10 September 2026. Exact checks and independent verification
are separate requirements. This is an all-rank family result, with no claim of worldwide novelty
or coverage of a whole ordinary rank.

## Entire LR family and exact count

Let `n >= 3`, `g >= 1` be integers with `ng` even. Define the ordinary triple

    lambda = (ng, (n - 1)g, ..., g),
    mu = ((n - 1)g, ..., g),
    nu = (ng/2, ng/2).

The outer partition has rank `n` and area `g n(n + 1)/2`. The inner sizes
sum to that area. At every stretch, `t lambda / t mu` consists of `n`
column-disjoint horizontal rows of length `gt`. Its complete skew character
is therefore `h_(gt)^n`, and the ordinary LR coefficient is the full Kostka
number `K_((ngt/2,ngt/2),(gt)^n)`.

Equivalently it is the multiplicity of the trivial `SL(2)` representation in
`Sym^(gt)(C^2)` tensored `n` times. The central weight multiplicity minus the
next weight multiplicity extracts that entire irreducible multiplicity.
Inclusion-exclusion for bounded compositions gives, for every integer `t >= 0`,

    P_(n,g)(t) = sum_(0 <= j < n/2) (-1)^j binom(n,j)
       binom((n/2 - j)gt + n - 2 - j, n - 2).                 (1)

For each retained summand its upper argument at zero is a nonnegative integer;
the polynomial binomial automatically vanishes on every early empty band.
Terms with `j >= n/2` have no admissible composition and are omitted before
polynomial continuation. Thus (1) is an all-grade identity, including zero,
not an eventual fit. It retains both weight multiplicities and every endpoint.

Put `x = gt + 1` and

    F_n(u) = binom(u + (n - 4)/2, n - 2).

Then (1) equals

    sum_(0 <= j < n/2) (-1)^j binom(n,j) F_n((n/2 - j)x).

## Even number of factors

For `n = 2m`, `m >= 2`,

    F_(2m)(u) = u(u - m + 1)
                  product_(l=1)^(m-2)(u^2 - l^2) / (2m - 2)!.

The constant term of `F_(2m)` is already zero. Every positive even power
disappears from the sum: its half-sum is half the complete order-`2m` finite
difference of a polynomial of degree below `2m` (the omitted central term
vanishes for those positive powers).
For `0 <= k <= m - 2`, define

    T_k = sum_(j=0)^(m-1) (-1)^j binom(2m,j)(m - j)^(2k + 1).

Its sign is exactly `(-1)^(m - k - 1)`. To prove this, use the elementary
integral identity

    |y|^(2k+1) = (-1)^(k+1) 2(2k+1)!/pi
       * integral_0^infinity
         [cos(yu) - sum_(l=0)^k (-1)^l(yu)^(2l)/(2l)!]
                                                    / u^(2k+2) du.

Repeated integration by parts reduces this to the Dirichlet integral; every
boundary term vanishes. The polynomial subtraction makes it convergent at
zero and infinity. Apply the full finite difference; all subtraction terms
vanish, and the cosine sum becomes `(-1)^m 2^(2m) sin(u/2)^(2m)`.
Consequently

    T_k = (-1)^(m+k+1) 2^(2m)(2k+1)!/pi
               * integral_0^infinity sin(u/2)^(2m)/u^(2k+2) du.

The integral is finite and strictly positive. This has the stated sign.
The coefficient of `u^(2k+1)` in `F_(2m)` has that same sign, since it is
`(-1)^(m-1-k)(m-1)` times a positive elementary symmetric sum of
`1^2,...,(m-2)^2`, divided by `(2m-2)!`.

It follows that the complete polynomial in `x` has strictly positive
coefficients at all odd powers `1,3,...,2m-3`, and zero at every even power.

## Odd number of factors

For `n = 2m + 1`, `m >= 1`, the integer condition forces `g` even. Now

    F_(2m+1)(u) = (u - m + 1/2)
       product_(l=1)^(m-1)(u^2 - (l - 1/2)^2) / (2m - 1)!.

All odd powers disappear by the complete order-`2m+1` finite difference.
For `0 <= k <= m-1`, set

    U_k = sum_(j=0)^m (-1)^j binom(2m+1,j)(2m+1-2j)^(2k).

Its sign is `(-1)^(m-k)`. The counterpart integral is

    sign(y)|y|^(2k) = (-1)^k 2(2k)!/pi
       * integral_0^infinity
         [sin(yu) - sum_(l=0)^(k-1) (-1)^l(yu)^(2l+1)/(2l+1)!]
                                                    / u^(2k+1) du.

The sum is empty for `k = 0`, when the integral is the ordinary Dirichlet
integral. For `k > 0` the subtracted expression is integrable. Applying the
finite difference gives

    U_k = (-1)^(m+k) 2^(2m+1)(2k)!/pi
                  * integral_0^infinity sin(u)^(2m+1)/u^(2k+1) du.

This integral is strictly positive. Pair consecutive lobes `[2j pi,(2j+1)pi]`
and `[(2j+1)pi,(2j+2)pi]`: their sine powers are opposite and the denominator
is strictly larger on the second lobe. Each paired integral is positive.
The behavior at zero is integrable; convergence at infinity is absolute for
`k >= 1` and follows from decreasing alternating lobes for `k = 0`.

The coefficient of `u^(2k)` in `F_(2m+1)` has sign `(-1)^(m-k)` as well.
The harmless factor `2^(-2k)` converts `U_k` to the required half-integer
moment. Thus the complete polynomial in `x` has strictly positive coefficients
at all even powers `0,2,...,2m-2` and zero at every odd power.

## Consequence, degree and exact limits

In both parities, replacing `x` by `gt + 1` gives **strictly positive ordinary
coefficients in every degree `0,...,n-3`**. The highest allowed coefficient
is nonzero by its positive integral, so the actual whole-LR degree is `n-3`.
The ordinary hive model and its saturated relative lattice remain the standard
LR premises; no auxiliary polytope is promoted to a parent.

At `n = 3` the result is the constant one. The separate `n = 2` family is also
a point and is outside the degree formula. Common positive `g` preserves the
exact count identity. The construction does not establish positivity for
unequal tensor weights: their subset-dependent shifts destroy the common
centered-binomial factor. It also does not justify suppressing one of the
central-weight terms or replacing a whole LR count by a synchronized face.

The `n = 6, g = 1` member is in the original box and was already covered
by low-dimensional positivity results. Larger even `n` and odd `n >= 7`
in this displayed construction lie outside the box. Any overlap count must
use exact original identities. The conclusion is an unbounded family theorem; it adds no finite-box count
or ordinary-negative example.

## Verification dependencies

The proof depends on (1), the finite-difference signs, convergence and the lobe
argument, together with the full LR character bridge and parity/domain
exceptions. Exact centered-coefficient checks cover both parities, degree
cancellation, `P(0)` and complete positive vectors; a separate unsigned
tensor-weight recurrence supplies scalar controls. The controls corroborate
the derivation without replacing its all-rank argument. Their documented
scope is given in the collection README.
