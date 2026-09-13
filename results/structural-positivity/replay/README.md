# Exact checks for three structural families

This module makes three accepted structural results reproducible at their
stated levels. It uses Python's standard library and exact integers and
fractions. It installs nothing and reads no private campaign archive.
Run from the repository root:

```sh
python3 -B results/structural-positivity/replay/reproduce.py --module two-row
python3 -B results/structural-positivity/replay/reproduce.py --module gap-three
python3 -B results/structural-positivity/replay/reproduce.py --module transport
python3 -B results/structural-positivity/replay/failure_cases.py
```

Each successful command prints a JSON result and exits zero. The first three
commands can be combined with `--module all`. To keep a report, redirect stdout
to a new file outside the source tree. A missing input, changed file, duplicate
identity or failed mathematical check returns nonzero. There are no downloads,
implicit caches or hidden data directories. Paths are relative to this file,
so the commands also work from a different working directory.

The two-row command freshly expands every finite case needed by the slope-three
proof and checks bounded complete character counts. The other two commands
reconstruct their entire polynomials from **historical accepted root count
values**. They check all coefficients, unused values and displayed algebra
again; they do not rerun the historical tableau or transportation counters.
The names of their successful statuses explicitly retain this distinction.
A new run becomes evidence only when its actual command completes.

The [dependency table](DEPENDENCIES.md) identifies the complete analytic chain,
finite input populations, source credit and remaining reproduction gaps.
[SOURCE-MAP.json](SOURCE-MAP.json) pins every required local proof, data file and
checker. Original proofs retain their bytes, including their historical
pending/accepted wording; the current structural [accepted scopes](../ACCEPTED-SCOPES.json)
record their later campaign dispositions. Scientific arguments, source
verification, AI review and external human peer review remain distinct.

## 1. Unequal-weight two-row LR families

Choose positive integers `w_1,...,w_n` and write `W=sum_i w_i`. With lambda
outer, define the entire LR triple by

```text
lambda_i = sum_(j=i)^n w_j,  1 <= i <= n,
mu = (lambda_2,...,lambda_n),
nu = (W-r,r).
```

Its ordinary rank is `n`, and its outer size is `sum_i i w_i`. The rows of
`lambda/mu` occupy disjoint columns, so their whole skew character is
`product_i h_(t w_i)`. The two-variable Schur extraction gives the complete
stretched coefficient

```text
P_r(t) = [z^(rt)] (1-z) product_i (1+z+...+z^(t w_i)).
```

This includes all content caps and both terms of the character difference.
Let `d=n-2`, `u=#{i:w_i=1}` and `v=#{i:w_i=2}`. Then

```text
P_2(t) = binom(2t+d,d) - u binom(t+d-1,d),

P_3(t) = binom(3t+d,d) - u binom(2t+d-1,d)
         - v binom(t+d-1,d) + binom(u,2) binom(t+d-2,d).
```

Here each binomial denotes its polynomial in `t`, including at zero. The
subset-cap derivations in the proofs establish the identities for every
nonnegative integer stretch, without interpolation.

For **slope two**, `r=2` and `n>=5`, every ordinary coefficient through actual
degree `d` is strictly positive. Its exact lower bound is

```text
P_2 >=_coeff 1 + (n-4) binom(t+d-1,d).
```

For **slope three**, `r=3` and `n>=6`, every ordinary coefficient through the
actual degree is strictly positive. The degree is `d`, except for six unit
weights, when

```text
P_3(t) = 1 + 2t + (3/2)t^2 + (1/2)t^3.
```

The all-unit profile minimizes every nonconstant coefficient. The proof
establishes its positivity analytically for `d>=21` and leaves exactly
`d=4,...,20` for rational expansion. The replay checks all 17 complete vectors,
including the exceptional ambient zero coefficient: 221 ambient coefficient
entries. Those finite cases **complete the analytic proof**; they do not
establish an all-rank theorem by extrapolation.

Bounded extra checks compare the formulas with an independently written
integer product recurrence at stretches `0,1,2,3`, across every realizable
unit/two-weight profile in the declared small-rank roster and two additional
unequal-weight examples. These challenge the complete character identity;
they do not constitute an independent general LR or hive implementation.
The exact profile and site counts are reported by the command.

Read the [slope-two proof](../proofs/pro027/019-UNEQUAL-WEIGHT-NONCENTRAL-POSITIVITY.md)
and [slope-three proof](../proofs/root/SLOPE-THREE-PROOF.md). Pro027 supplied
the count formulas and slope-two sign proof. The root supplied the stronger
slope-three profile comparison and sign argument. Classical Schur identities
and earlier two-row work remain credited. The result covers these suffix-sum
families, with arbitrary positive weights; it does not settle every two-row
LR coefficient, higher slopes or all-rank KTT.

## 2. Gap-three quadrant and homogeneous cone

For integers `x,y>=0`, set

```text
lambda = (3x+15+9y, 2x+12+7y, x+9+5y, 6+3y, 4+2y, 2+y),
mu = (lambda_2,...,lambda_6),
nu = (2x+5+2y, x+4+2y, 3+2y, 2+2y, 1+y).
```

These are balanced rank-six triples, of outer size `6x+48+27y`, with entire
polynomial `P_xy` of actual degree ten and true codegree three. The weighted-GT
model uses its saturated `Z^10` lattice. LR polynomiality and reciprocity give
`P_xy(0)=1` and roots `-1,-2` before reconstruction.

The complete quadrant identity is

```text
P_xy = P11 + (x+y-2)t Q1 + (x-1)(y-1)t^2 R,  x,y >= 1;
P_x0 = P10 + (x-1)t Q0,                       x >= 1;
P_0y = P10 + (y-1)t Q0,                       y >= 1;
P_00 = P00.
```

The four parent bases are `P00,P10,P20,P11`; derive `Q0=(P20-P10)/t`.
No quotient constant is inserted into that division. `Q1` and `R` have the
complete closed hinge-moment formulas in proof 006. Every coefficient of
`P00,P10,P11,Q0,Q1,R` is strictly positive. Thus all eleven coefficients of
every whole quadrant member are strictly positive, including both axes and
the initial corner.

For the genuinely homogeneous cone, let integers `s,a,b>=0` and put

```text
lambda = (27s+3a+9b, 21s+2a+7b, 15s+a+5b, 9s+3b, 6s+2b, 3s+b),
mu = (lambda_2,...,lambda_6),
nu = (9s+2a+2b, 7s+a+2b, 5s+2b, 4s+2b, 2s+b).
```

After trimming zeros, its entire stretched polynomial is

```text
P_(s,a,b)(t) = P11(st) + (a+b)t Q1(st) + ab t^2 R(st).
```

Proof 007 establishes independent widths; this formula is not inferred by
substituting noninteger `x,y` into the quadrant theorem. The grade-one count
has exactly 40 nonzero joint coefficients: 11 from `P11(s)`, ten each from
`aQ1(s)` and `bQ1(s)`, and nine from `abR(s)`. All are positive.
For `s>0`, the actual degree is ten, ordinary rank six and true codegree
`ceil(3/s)`. For `s=0`, the whole count is `(at+1)(bt+1)`, of actual degree
two, one or zero according to the positive parameters. Its codegree is
`max(ceil(2/a),ceil(2/b))` when both are positive, the corresponding one-sided
ceiling on a segment, and one at the origin. The explicit saturated rectangle
chart in proof 007 handles these boundaries. Ordinary rank is six when
`s+b>0`, three when `s=b=0<a`, and zero at the origin; rank and actual degree
are different quantities.

The separate homogeneous edge has

```text
lambda = (24s+9b, 19s+7b, 14s+5b, 9s+3b, 6s+2b, 3s+b),
mu = (lambda_2,...,lambda_6),
nu = (7s+2b, 6s+2b, 5s+2b, 4s+2b, 2s+b),
P(t) = P10(st) + bt Q0(st),                    s,b >= 0.
```

It has degree ten and codegree `ceil(3/s)` for `s>0`; at `s=0` its complete
count is `bt+1`.

The input contains exactly **40 historical positive counts**: four parents
at grades `1,...,10`. Of these, 32 are determining values and eight at grades
9 and 10 are unused checks. The replay independently runs Lagrange and Newton
arithmetic, checks all full vectors and positive factors, derives the quotient
constant, checks the complete quadrant identities and 40 joint coefficients,
and retains the auxiliary

```text
W0 = P00-P10+tQ0.
```

Its ordinary coefficients in degrees one through four are respectively
`-1/7,-101/210,-2741/5040,-151/2520`. It is an auxiliary correction;
its complete `P00` parent is positive. The replay preserves this failure of
naive affine extension instead of treating it as an LR counterexample.

Read proofs [001](../proofs/pro027/001-COMPLETE-GAP3-CLUSTERS.md) through
[008](../proofs/pro027/008-INITIAL-WALLS-AND-POSITIVE-DIFFERENCES.md) through
the dependency table. General strict gap three, remaining fractional or
negative wings and non-strict strata are outside these positivity theorems.
The general eight-term count identity has a larger domain than the proved
positive quadrant; it does not supply positivity on that larger domain.

## 3. Seven transportation endpoints and exact stabilization

For integers `h>=0`, the entire LR family is

```text
lambda_h = (27+h,22+h,18+h,17+h,13,10,8,6,4,2),
mu_h = (17+h,17+h,17+h,13,10,8,6,4,2),
nu_h = (17+h,10,5,1).
```

The outer size is `127+4h`, and the ordinary rank is ten. Proof 011 identifies
its complete all-stretch count with all nonnegative `4 x 7` integer matrices
with row margins `t(7+h,5,4,1)` and column margins
`t(4+h,3,2,2,2,2,2)`. The first three rows and six columns give the saturated
`Z^18` chart. A strictly positive real table and network total unimodularity
establish dimension 18 and integral vertices. Subtracting one from every
entry shows codegree seven, so the prior roots are `-1,...,-6`.

Every ordinary coefficient of every `P_h` through degree 18 is strictly
positive. There are exactly seven distinct polynomials: all nonconstant
coefficients strictly increase from `h=0` through `h=6`, and `P_h=P_6` for
all `h>=6`. The full last-column cap becomes redundant precisely at that
threshold. Its final shell is

```text
P_6(t)-P_5(t) = binom(t+17,18),
```

whose value at one is one, so the integer stabilization threshold is sharp.
The linear endpoints for `h=0,...,6` are

```text
5279/360, 1085/72, 5521/360, 1117/72, 1127/72, 1133/72, 379/24.
```

The data contain all 105 historical values at `h=0,...,6`, `t=0,...,14`:
seven supplied grade-zero constants, 84 positive determining values at
grades `1,...,12`, and 14 unused positive values at grades 13 and 14. The
replay reconstructs all seven full vectors using separate Lagrange/Newton
arithmetic, checks all 133 positive coefficients, all 108 positive
nonconstant shell coefficients and the final shell identity. It also checks
all seven explicit positive grade-seven table witnesses against their margins.
It does not repeat the historical 189-group signed-assignment count.

The [root cone proof](../proofs/root/TRANSPORT-CONE-LINEAR-COEFFICIENT.md)
uses these linear endpoints with a separate complete sector and Minkowski
argument. For integers `u>=1,v>=0`, rows `(7u+v,5u,4u,u)` and columns
`(4u+v,3u,2u,2u,2u,2u)`, it gives

```text
e1(u,v) = ((j+1)u-v) a_j + (v-ju) a_(j+1), ju <= v <= (j+1)u;
e1(u,v) = u a_6,                             v >= 6u,
a_j = e1(1,j),
e1(u,v) >= 5279u/360 > 0.
```

Here `j=0,...,5`; equality in the bound holds at `v=0`. The entire LR
realization is obtained from the displayed endpoint triple by replacing each
constant with that constant times `u`, and each `h` with `v`. The independent
sector argument and classical multivariate Ehrhart theorem, not endpoint
sampling, establish the cone conclusion. This replay supplies its exact
endpoint premise. Its separate high-coefficient BV corollary is mapped in
the dependency table and is not regenerated by this command.

The coefficients `e2,...,e15` at noninteger `v/u` remain open in the accepted
cone analysis. The negative-`v` extension is separate and unproved here. The
source size-133 parent has the same `h=0` polynomial by full row/column
permutation; it is a distinct bare triple and is not an eighth endpoint.
These results neither settle every rank-ten LR family nor produce an
ordinary-negative entire LR polynomial.
