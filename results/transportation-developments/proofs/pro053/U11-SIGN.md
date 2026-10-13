# U11 exact monotonicity certificates

Curated mathematical proof from **Pro053/A79 accepted dependency**. The corresponding accepted scope
is stated in the module guide; [the source map](../../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Derived SOURCE; finite polynomial identities, not a sampled-margin proof.

## Entire n=3 low derivative

Differentiate the complete S at fixed x, then substitute x=b+h.

| Power of b | Power of h | Coefficient |
|---|---|---|
| 5 | 0 | 1/15 |
| 4 | 1 | 5/12 |
| 4 | 0 | 5/8 |
| 3 | 2 | 11/12 |
| 3 | 1 | 3 |
| 3 | 0 | 41/18 |
| 2 | 3 | 11/12 |
| 2 | 2 | 19/4 |
| 2 | 1 | 31/4 |
| 2 | 0 | 97/24 |
| 1 | 4 | 11/24 |
| 1 | 3 | 19/6 |
| 1 | 2 | 63/8 |
| 1 | 1 | 17/2 |
| 1 | 0 | 619/180 |
| 0 | 5 | 11/120 |
| 0 | 4 | 19/24 |
| 0 | 3 | 21/8 |
| 0 | 2 | 101/24 |
| 0 | 1 | 10/3 |
| 0 | 0 | 13/12 |

## Uniform n>=4 low-derivative payment

Denominator: 2*n*(n - 1)*(n + 1)*(n + 2). Set n=m+4.

| Power of b | Power of h | Numerator |
|---|---|---|
| 2 | 0 | m**4 + 18*m**3 + 115*m**2 + 314*m + 312 |
| 1 | 1 | 2*m**4 + 38*m**3 + 256*m**2 + 736*m + 768 |
| 1 | 0 | 4*m**4 + 62*m**3 + 350*m**2 + 856*m + 768 |
| 0 | 2 | m**4 + 20*m**3 + 139*m**2 + 400*m + 396 |
| 0 | 1 | 4*m**4 + 58*m**3 + 302*m**2 + 692*m + 648 |
| 0 | 0 | 2*m**3 + 26*m**2 + 104*m + 120 |
