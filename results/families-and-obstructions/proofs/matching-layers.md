# A second-shift identity for the fourth and fifth matching layers

Derivation dated 10 September 2026, with complete exact symbolic checks.
No historical novelty claim is made.

## Complete inherited object

Use the entire unit-flank matching LR family and saturated flow lattice in
[the shift-difference proof](matching-positive-shifts.md),
[the earlier layers](matching-three-layers.md), and
[their scope analysis](matching-scope.md), retaining the full character/count
bridge and numerator. Put `q = 4`, `r >= 4`, `B = 6`, `d = 8r + 27`,
`D = d - 4 = 8r + 23`, and `m = D - r = 7r + 23`.
The whole parent has ordinary rank `a + f + r + 11` for positive end runs
`a, f`; at unit ends its rank is `r + 13`, at least seventeen.
The parent degree is `d`, not the auxiliary degree `D`.

The exact rational identity is

    P(t) = A(t) G(t) + Bop(t) Omega(t),
    sum G(t) z^t = (1 + B z)^r / (1 - z)^(D + 1),
    Omega(t) = G(t - 1),
    W(t) = t G(t) - (t + m) Omega(t),
    C(t) = Bop(t) + A(t) - 1 + m (A(t) - 1) / t.

Here `A(0) = 1`, and the exact `A`, `Bop`, `C` coefficient arrays are the
[operator certificate](../data/astra-five/matching-operator-certificate.json), row `q = 4`.
All coefficients of `A - 1` and `C` except `C(0)` are positive. The negative
leading parameter term of `C(0)` is the old sufficient-certificate failure.

## A positive two-shift combination

For general integers `B, r >= 1` and
`m >= (B - 1)r + B + 3`, set

    R_s(t) = sum_j binom(s,j) B^j
                    t_under(j) (t + m + 1)_over(s - j).

The complete recurrence from the exponential generating identity is

    R_(k+1)(t) = ((B + 1)t + m + 1 - (B - 1)k) R_k(t)
                   + B k(k + m) R_(k-1)(t).

After replacing `t` by `t - 2`, its affine constants for `k <= r - 1` are
at least `m - (B - 1)r - B - 2 >= 1`. Hence `R_r(t - 2)` has strictly
positive coefficients through degree `r`, as do `R_r(t - 1)` and their
difference through degree `r - 1`. This is a coefficient argument: if
`R_r(t - 2) = sum p_k t^k`, then the difference is
`sum p_k ((t + 1)^k - t^k)`.

Define

    Phi(t) = G(t - 1) + (m - 1) G(t - 2).

Although `G(t - 2)` itself has a negative linear coefficient, their complete
combination has the factorization

    Phi(t) = t(t + 1)...(t + m - 2) / D!
       * [t R_r(t - 1) + (m - 1)t R_r(t - 2)
                      + (m - 1)(R_r(t - 1) - R_r(t - 2))].

Thus `Phi(0) = 0` and all its coefficients in degrees `1,...,D` are strictly
positive. Retaining the negative shift together with its compensation is
essential. The condition holds for the matching parameters because its
leftover constant is `2r + 15 > 0`.

## Exact re-expression of the whole parent

Differentiate the complete generating function. Its sequence obeys

    t G(t) = (K - (B - 1)t) G(t - 1)
                         + B(t + m - 1) G(t - 2),
    K = (B + 1)r + m + B.

This is a polynomial identity: derive it for all sufficiently large integer
`t`, then use polynomiality. No negative-grade sequence convention is needed.
Let `a1 = [t]A`, and put

    L2(t) = (A(t) - 1) / t - a1,
    C2(t) = C(t) + (B + 1)r a1 - B a1 m t / (m - 1).

Substitution gives the exact complete identity

    P(t) = G(t) + L2(t) W(t) + C2(t) Omega(t)
                       + B a1 (t + m - 1) Phi(t) / (m - 1).

There are no omitted numerator, projection or intercept terms. This follows
by eliminating `a1 t G` through the sequence recurrence and replacing
`G(t - 2)` by `(Phi - Omega)/(m - 1)`.

For `q = 4` the constant correction is `C2(0) = C(0) + 7r a1`.
Its formerly negative highest power of `r` cancels exactly. Every remaining
coefficient of its numerator is positive. The only other changed coefficient
is `[t]C2 = [t]C - 6a1(7r + 23)/(7r + 22)`; after the legal normalization
`r = 4 + s`, its cleared numerator has all coefficients positive in `s`.
The first fixture incorrectly demanded positivity of these numerator
coefficients around the out-of-domain value `r = 0` and failed before any
parent count. That failure is preserved; the repaired fixture uses `s >= 0`.
The complete arrays and exact identities are retained in
`A005-MATCHING-SHIFT-002.json` and `A005-MATCHING-INDEPENDENT-001.json`.

The complete symbolic identities and sign checks imply that
`P >=_coeff G >=_coeff binom(t + m,m)`, and every ordinary coefficient of
every complete fourth-layer member is strictly positive. The fifth-layer
extension below further enlarges the symmetric domain.

## General retained-multiplier identity and the fifth layer

The same derivation allows a polynomial removal, not only the constant `a1`.
Write `Q(t)=(A(t)-1)/t`. Choose a polynomial `U` with both `U` and `Q-U`
coefficientwise nonnegative, and define

    C_U(t) = C(t) + (B+1)r U(t) - B m t U(t)/(m-1).

Then the exact entire identity is

    P = G + (Q-U)W + C_U Omega + B(t+m-1)U Phi/(m-1).

Thus nonnegativity of every coefficient of `C_U` is a sufficient complete
ordinary-positivity certificate. The positive auxiliary factors have the
complete degree supports established above. `G` covers degrees through `D`;
the positive leading term of the known degree-`D+q` parent supplies a top
multiplier whose product with `Omega` or `Phi` covers every remaining degree.
There is no omitted negative shifted factor.

The **full symbolic** matching identity was derived for `q=5` by
rational-function linear algebra in `r,z`, with no parameter interpolation.
Removing `U=a1+a2 t` passes every exact numerator/denominator coefficient
check after `r=5+y`. The zero-removal and other prefix removals are separately
recorded as failed sufficient certificates. The independent standard-library
`Fraction` checker regenerates the complete numerator identity, clears every
denominator, and verifies every coefficient in `r,z`, together with all changed
multiplier relations and sign arrays. `A005-MATCHING-INDEPENDENT-001.json`
records both successful all-parameter certificates.

For general `q`, the base hypotheses continue to hold because
`m-(B-1)r-B-2 = 2r+2q+7 > 0`. For larger layers, membership of the entire symbolic parent in this precise
nonnegative multiplier cone remains to be established.
A failure concerns that sufficient representation, not an ordinary
coefficient of the whole LR family.

## Scope and a sixth-layer obstruction

The complete unit-flank matching family is ordinary-coefficient positive
whenever `min(q,r) <= 5`, at all positive end-run lengths and common integral
dilations. Zero direction is separately the point polynomial. The proved
zero-run cases cover `q=0` or `r=0`; the tables here use `r >= q >= 4`.
The final ordinary rank is `a+f+q+r+7`; inactive end runs do not change the
polynomial. The actual parent degree is `qr+4q+4r+11`. Consequently a negative
member of this displayed constructor must have `q,r >= 6`, displayed rank
at least 21 and degree at least 95. This is not a minimum over other LR
realizations, and supplies no original-box coverage.

At `q=6`, removing any allowed polynomial `0 <=_coeff U <=_coeff Q` cannot
rescue this fixed second-shift cone uniformly in `r`. Its constant condition
is `C(0)+9r U(0) >= 0`, whose largest possible left side is
`C(0)+9r a1`. Exact rational arithmetic gives

    C(0)+9r a1 = -(2/2278125) r^2 + O(r).

It is therefore negative for all sufficiently large `r`. This rules out the
entire stated nonnegative-removal cone as an all-parameter certificate,
not the matching polynomial or another compensation mechanism.

A modified construction changed the auxiliary power from `r` to `r-1`, its degree
from `D` to `D-1`, and the complete operator order from `q` to `q+1`, with
`r >= 8`. The full changed numerator identity was independently verified,
but none of the tested prefix removals furnished a positive certificate.
Only that finite prefix search is closed for the changed baseline. A further
attempt needs a different positive basis or a non-prefix compensation;
larger flanks, nonconstant directions and different couplings remain open.

## Verification dependencies

The argument requires the sequence recurrence, both complete re-expressions,
the exact rational parameter arrays, and the parent rank, degree, lattice and
whole character bridge. The negative linear term of `G(t - 2)` is retained
inside its compensating combination. Finite numerator comparisons alone would
not establish the parameter identities. This all-size family theorem supplies
no additional finite-box coverage or ordinary-negative example.
