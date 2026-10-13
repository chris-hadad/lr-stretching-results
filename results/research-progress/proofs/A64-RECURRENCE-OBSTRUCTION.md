# A64: the natural dimension recurrence fails at its first coefficient

Curated accepted mathematical source; the module guide states its exact domain.

Let F_a be that complete scaled polynomial with caps (X,R,...,R,R+Z), larger deficit R, smaller deficit S, and D_a=partial_X F_a at fixed R,S,other caps. Compare adjacent cap counts by appending one cap R. The natural recurrence would require


```text
D_(a+1) >=_c b(R) D_a,   b(R)=(R+1)(R+2)/2.       (1)
```

The free part has constant derivative 11/4. Let m be the number of active distinguished-cap singleton terms: m=2 on X<S<R and m=1 on S<X<R. Put n=2a. Each active singleton has binomial top h-X+n-3. At all scaled variables zero the three falling-binomial derivatives are


```text
2/[n(n-1)(n-2)],
-6/[(n+1)n(n-1)(n-2)],
24/[(n+2)(n+1)n(n-1)(n-2)].
```

Removing the unique zero factor proves these identities for every a>=3. The cap-growth derivative takes their combination 4,4,1, giving


```text
q_a=1/[a(a^2-1)],
[1]D_a=11/4+m q_a.
```

Here [1] denotes the constant in the scaled parameter polynomial, not the constant coefficient of the original stretching polynomial. Multiplication by the external t in dC/dx converts it to the original ordinary linear coefficient. Thus


```text
[1](D_(a+1)-b(R)D_a)
  = -3m/[(a-1)a(a+1)(a+2)] < 0.                 (2)
```

The obstruction holds in every positive parameter point in either open chamber and at every a>=3. It is not merely one adverse mixed coefficient of a chosen parametrization. Both D_a and D_(a+1) may still be strictly positive; subtracting the entire b(R)D_a asks too much.

For a representative large-cap excess Z, the free part's pure-Z coefficient is 62/9. The singleton contribution is the 2,1 combination of the first two derivatives above:


```text
z_a=(4a-1)/[2a(a-1)(4a^2-1)],
[Z]D_a=62/9+m z_a,
z_(a+1)-z_a=
  -3(4a^2+2a-1)/[a(a-1)(a+1)(2a-1)(2a+1)(2a+3)] < 0. (3)
```

A64's exact complete symbolic checks at a=3,4,8 find only these two negative residual monomials in each chamber. They compare entire polynomials, not sampled originals. Their output does not prove that no additional negative appears at another cap count.

A serious corrected candidate is


```text
E_a=D_a-m(q_a+z_a Z),
E_(a+1) >=_c b(R) E_a.                            (4)
```

Subtracting the exact low terms cancels the two observed losses and adds nonnegative R and RZ multiples. Hence (4) passes those six complete finite identities. A uniform proof still needs to control every other coefficient for arbitrary a, and an induction would need an appropriate positive base and the full excess-vector interpretation. It remains CONJECTURED, not retired by the failure of (1), and not adopted from finite positives. The A64 alternative is the complete two-active-cap paid operation.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation, 27 September 2026.. Accepted premise: the complete one-active-cap expression in A63 CROSSING-PROOF Section 3. This is a whole recurrence obstruction, not a negative whole original.

## A bounded consequence that the checked recurrence does prove

The complete a=8-to-9 corrected identity is already among the six independently checked maps. It has a useful finite consequence without claiming a uniform recurrence. In each chamber the accepted A63 D_8 certificate is coefficientwise nonnegative. Subtracting m(q_8+z_8 Z) changes only its constant and pure-Z coefficients, leaving exactly 11/4 and 62/9; hence E_8 is still coefficientwise nonnegative. Its pure-u supports in the both-active chamber and pure-u/pure-v supports in the one-active chamber remain positive in every parameter degree 0,...,17. Their constant becomes 11/4, still positive.

The checked E_9>=_c b(R)E_8 therefore makes E_9 nonnegative in every zero/one-excess coefficient. Since R=u+v+w, the product b(R)E_8 supplies the same strict pure supports in every degree 0,...,19. Adding back m(q_9+z_9 Z) preserves those signs. A63 Section 4's analytic high-excess payment holds for every a>=3 and supplies all omitted excess degrees at a=9. The x=0 base has eight large caps and is paid by A62. The complete coefficient functions join continuously at the singleton walls.

Consequently the entire one-arbitrary-small-cap fixed-deficit growth theorem extends to a=9: positive x gives actual degree 20, x=0 degree 18, and the gain is strict in degrees 1,...,20. The physical original has rank 13 before extra zero-row insertion. This is the finite dividend of the already checked 8-to-9 identity, not an arbitrary-a theorem or a two-small-cap theorem at a=9. The full two-cap result in TWO-CAP-PROOF.md remains a=4,...,8. No new original-count panel is used for this corollary; it depends on the complete identities and the accepted complete original/count bridge.
