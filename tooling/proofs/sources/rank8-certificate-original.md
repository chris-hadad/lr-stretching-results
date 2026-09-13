# Ordinary positivity of the entire clipped rank-eight family

The complete computational certificate and independent count comparison
were verified on 9 September 2026. [The verification summary](rank8-adoption.md)
records the resulting theorem scope.

## The statement

For integers `0<=M<=S<=2M`, use the complete ordinary LR boundary

```text
lambda=(50M-S,46M,36M,32M,23M+S,19M,9M,5M),
mu=(27M,23M,19M,15M,13M,9M,5M,M),
nu=(25M,22M,19M,14M,12M,9M,6M,M).
```

For every `M>0`, every ordinary coefficient of the entire stretched LR
polynomial is strictly positive, through degree 21. The origin gives the
constant polynomial one. This closes the formerly unknown `M=1,S=2` member
and the entire stated clipped parameter cone. Together with the
separate `M>=S>=0` proof, signs are settled on `0<=S<=2M`.

This is a family theorem at ordinary rank eight, with outer area `220M`.
It is not a theorem for all rank eight, the original box or full KTT.
The two abstract nonlinear/affine-width negatives retain their missing LR
realizations. The negative abstract models are not counterexamples to LR positivity.

## Complete count and polynomiality

The complete integer tableau map retains all 92 original
nonnegativity, column and ballot inequalities and all row/content identities.
For `M<=S<=2M`, exactly the three displayed additional cuts remain, including
the empty bottom-simplex branch. Deleting one cross coordinate gives the
saturated 21-dimensional integer chart. The strict conventional-hive point
at `M=1,S=2` independently proves degree 21 before any interpolation.

RANK8-AGGREGATION.md contracts that entire count by conditional column
symmetry. It replaces literal sixteen-entry composition enumeration by
quadratically many row-total groups and short exact convolutions. The two
top exclusions and their intersection collapse to two one-column quadratic
tails. RANK8-POLYNOMIALITY.md then expresses every term as a polynomial sum
over explicitly split integer triangles and rectangles, including all walls
and empty ranges. It proves a single polynomial of total degree at most 21
in the nonnegative parameters

```text
u=2M-S, v=S-M, so M=u+v and S=u+2v.
```

There are no unproved extra parameter chambers or parity-dependent endpoints.
Every exact binomial summand has a fixed nonnegative lower index, and each
finite power-sum elimination raises total degree by at most one.

## A finite positive certificate for every parameter

Let `G(u,v)` be the complete count at stretch one. The 253 values on
`i,j>=0`, `i+j<=21` determine it in the triangular Newton basis
`binom(u,i)*binom(v,j)`. Exact conversion gives **253 strictly positive
ordinary coefficients**, with no missing or zero monomial in that triangle.
The source array is `science/results/FRI-R8-BIVARIATE-001.json`.

The maintained data module records all integer numerators over the common
denominator `121645100408832000`. Therefore, for any fixed nonnegative
integers `U,V`, every ordinary coefficient of
`G(U*t,V*t)` is a sum of nonnegative terms. At every positive total degree
through 21, a strictly positive pure-axis term survives whenever `(U,V)` is
not the origin. This proves the stated strict positivity and degree.

In particular the full linear coefficient is

```text
c1 = (867149951/116396280)*(2M-S)
     +(19208731/1956240)*(S-M).
```

At `M=1,S=2`, all 22 coefficients are positive and the linear coefficient is
`19208731/1956240`. Its negative integer roots are `-1` through `-11`.
The full vector is preserved in `FRI-R8-POLYNOMIAL-001.json`; positivity is
not inferred from its first four values or a necessary sign functional.

## Independent representation and controls

The independent program retains the original three cuts directly. For a
fixed column margin `c`, put

```text
H_c(x,y)=sum_(a,b>=0,a+b<=c) (c-a-b+1)*x^a*y^b.
```

The product of four such polynomials counts every cross matrix by its first
two row totals; `c-a-b+1` counts the assignments in the last two rows. Weight
each coefficient by the exact bottom child count. This value is symmetric
in the four column margins, so sum it over sorted margins and multiply by
the sum of the exact top child count over distinct margin permutations.
No conditional-moment simplification is used by this program.

Its sparse numerator identity is

```text
(1-x)(1-y)*H_c=(c+1)-sum_(i=1)^(c+1)(x^i+y^i)
                         +sum_(i=1)^(c+1)x^i*y^(c+2-i).
```

Triangular two-dimensional prefix sums recover the full product coefficients;
truncation occurs only above the known true product degree. Checked signed
128-bit arithmetic is backed by a conservative absolute intermediate bound
below `2^114` on its explicit verification domain `m<=24,s<=48`.

Every one of the 253 independent counts agrees with the first count model
and the reconstructed bivariate polynomial. A separate Lagrange reconstruction
of the independent `M=1,S=2` axis agrees in all 22 coefficients. The two
positive stretches 22 and 23 were excluded from both fits and give

```text
P(22)=29770172352100574100,
P(23)=65809335330948932400.
```

Two additional unused cone points, `(M,S)=(22,34)` and `(24,31)`, also agree.
The twelve complete literal controls, all 1,678 reconstructed parent tableaux
at the first outside seed, and two fresh bare-LR counts pass. The combined
record is `science/results/FRI-R8-CERTIFICATE-001.json`.

## What the mechanism teaches

These first three actual LR cuts do not overcome the complete cubic-fiber
compensation. The positive parameter certificate explains their combined
effect at every scale; a negative contribution from one cut is insufficient.
This theorem excludes a negative ordinary coefficient throughout its
stated domain. Other couplings require separate arguments. The algebraically legal range beyond `S=2M` has additional
constraints and is not covered by this result. The rectangular invariant-ring construction is a separate family and is
not covered by this theorem.
