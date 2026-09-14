# Complete three-row coefficient calculations

This Python 3.11+ standard-library module computes full exact ordinary coefficient vectors for three-row transportation, the complete capped family, and three-row Schur coefficients of affine homogeneous products or complete Jacobi-Trudi determinants. It keeps every original shift, sign, support wall and zero term. No interpolation or numerical solver is used.

From the parent directory:

```sh
python3 -B -m unittest three_row_coefficients.test_coefficients
python3 -B -c 'from three_row_coefficients import transport_polynomial; print(transport_polynomial((3,4,5),(1,2,2,3,4)))'
```

Every vector is a tuple of exact Fraction values in increasing ordinary powers. A point returns `(Fraction(1),)`; the zero polynomial is `(Fraction(0),)`. These functions do not create files or subprocesses.

| Interface | Complete object and limits |
| --- | --- |
| `transport_polynomial(rows, columns, max_assignments=20000, max_degree=24)` | Balanced nonnegative margins, at most three supplied rows; preserves every column and original integer stretch. The full formula has 3^N assignments after zero columns are removed. |
| `capped_polynomial(weights, c, d, ...)` | Nonnegative capacities with sum weights>=c+d; complete y,z count with sum z=c*t, sum y<=d*t, y_i+z_i<=w_i*t. Its exact whole-LR lift is in the companion certificate proof. |
| `affine_kostka_polynomial(weights, offsets, alpha, ...)` | Complete eventual Schur coefficient of product h_(w_i*t+b_i), with alpha a partition of length at most three, balanced slopes and zero total offset. Individual affine products may differ from this polynomial at unsupported early grades. |
| `one_overlap_polynomial(u, v, h, remaining, alpha, ...)` | Entire single-overlap LR character; all original affine determinant offsets remain. Returns complete signed records and the whole vector. |
| `jacobi_trudi_polynomial(outer, inner, alpha, ...)` | Entire LR polynomial with at most three target rows; all permutations are retained. Defaults allow 720 permutations, 100000 assignments per product and 1000000 in total. This is a bounded exact interface, not a general fast LR algorithm. |

Inputs require exact Python integers, excluding booleans. Malformed inputs raise ValueError. PolynomialResourceLimit refuses before coefficient arithmetic when a declared assignment, permutation or intermediate-degree cap is exceeded. The intermediate degree can exceed the final degree after cancellation. A refusal returns no partial coefficient; computational caps do not bound integer bit lengths or replace an external wall-time limit for large calls.

The general polynomial interfaces themselves assert no universal sign theorem outside their exact proved regions. In particular affine summand coefficients, negative mixed coefficients and an incomplete count are not whole LR counterexamples. The complete assignment derivation and finite/count verification are in PROOF.md and the companion whole-family certificate module.
