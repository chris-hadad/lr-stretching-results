# Literal originals, saturated chart and prior actual degrees — A81

Curated mathematical proof from **A81**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

This proof fixes the geometry before any A81 bare-original count. It does not
assume a favorable fitted degree, positive coefficient vector or source result.

For integers m >= 3 and s > 0, set u = 2s. Preserve the displayed physical rows:


```text
lambda = ((m+8)s, (m+6)s, (m+4)s, ms, (m-1)s, ..., s),
mu = ((m+4)s, (m+2)s, ms, (m-1)s, (m-2)s, ..., 0),
nu = ((m+4)s, 5s, 3s).
```

Lambda is outer. Both shapes are partitions in their displayed order, every
outer part dominates its corresponding inner part, and the skew area and
content size are (m+12)s. All m+3 physical rows and the final inner zero remain.
No conjugation, sorting of an affine output or unproved equivalence is used.

At grade t put S = st and U = 2S. Tail row i has multiplicities
(S-b_i-c_i, b_i, c_i), for i = 1,...,m. Put B = sum b_i, C = sum c_i,
x = B-S, y = C-S. The top three row multiplicities are

    (2U, 0, 0),
    (a, 2U-a, 0),
    (U+x+y-a, a-x, U-y).

Weak rows, columns and the top ballot conditions give precisely


```text
max(0,x,y,x+y,-x) <= a <= U + min(0,x+y,y).
```

In addition to b_i >= 0, c_i >= 0 and b_i+c_i <= S, every physical tail
retains BOTH ballot minima, after its threes and twos in reverse weak-row order:


```text
h12_i = (4-i)S-b_i-c_i-2 sum_(j>i)b_j-sum_(j>i)c_j <= U,
h23_i = sum_(j>=i)b_j-sum_(j>i)c_j <= U.
```

These follow by subtracting read twos from ones, and read threes from twos,
respectively. Neither family is declared automatic at U = 2S. Together with
the full top interval these are the entire literal tableau constraints.
The coordinates (b_1,c_1,...,b_m,c_m,a) and their inverse use integer additions
and subtractions. Thus the original affine difference lattice is the saturated
Z^(2m+1), with no parity division, root-lattice substitution or changed residue.

For S > 0 choose b_i = c_i = S/m and a = S. Then x = y = 0, all tail
entries are positive, and 0 < a < U. The tail thresholds are


```text
h23_i = S/m,
h12_i = (1-i)S + (3i-2)S/m.
```

The latter decrease with i (are constant at m = 3), with maximum S/m.
Consequently every nonforced constraint is strict, since S/m < 2S. A small
rational box around this point lies in the original chart. Together with
boundedness, this gives lattice counts of order t^(2m+1) before interpolation.
It does not assert that every vertex is integral or that degree-one tableaux
generate the complete semigroup.

For completeness an all-grade polynomial upper bound follows from the complete
three-variable skew character and all Weyl partners. Let n = 2m+1. The exact
four-mask expression is


```text
C_m = sum_(j=0)^3 A_j
      -3 sum_(j=0)^3 (-1)^j binom(m,j) T_j - R,
A_j = (-1)^j binom(m,j) sum_(p=0)^j binom(j,p)(S+2)^(j-p)
      binom((4-j)S+2m+1-2j, 2m+1-j+p),
T_j = sum_(p=0)^m binom(p+j,j)
      binom((3-j)S+m-j+1,m-p) binom(S+m,m+p+1),
R = binom(2S+2m,2m+1)
    -m[(S+2)binom(S+2m-2,2m)+binom(S+2m-2,2m+1)].
```

Every binomial is its full falling-product rational polynomial. For integer
S >= 0 and m >= 3 the upper arguments are nonnegative, and initially empty
supports have their exact polynomial zeros. No negative counting degree is
continued to a nonzero count. Four row-capacity violations require
4(S+1) > 4S, so j = 0,...,3 includes every supported labeled subset.
Each A term has degree at most (j-p)+(2m+1-j+p) = 2m+1, each T term
at most (m-p)+(m+p+1) = 2m+1, and R has the same bound. The complete
character derivation is reconstructed in the A81 index proof; this expression
is not a fitted ansatz. The interior lower bound and this upper bound prove
actual degree exactly 2m+1, with positive leading term, before any count.
At S = 0 this full expression is 1, the unique empty tableau.

The two fresh bare-engine controls are existing unadopted source originals:

- B4: lambda = (12,10,8,4,3,2,1), mu = (8,6,4,3,2,1,0),
  nu = (8,5,3); prior degree 9, determining grades 0,...,9 and unused 10,11.
- B6: lambda = (14,12,10,6,5,4,3,2,1), mu = (10,8,6,5,4,3,2,1,0),
  nu = (10,5,3); prior degree 13, determining grades 0,...,13 and unused 14,15.

Their complete formula vectors and independent bare-engine vectors must freeze
before any unused call. Pilots B4 at grade 1 and B6 at grade 13 are determining
sites and are reused. The complete workload is 28 main requests, including two
grade-zero requests with contained grade-one feasibility computations. These
contained calls are charged and identified, not counted as extra distinct sites.
Every native count has a hard child boundary and actual exit proof. No candidate
or ordinary-coefficient sign is assumed by this geometry record.
**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

lambda = ((m+8)s, (m+6)s, (m+4)s, ms, (m-1)s..., s),

```text
mu = ((m+4)s, (m+2)s, ms, (m-1)s, (m-2)s..., 0),
nu = ((m+4)s, 5s, 3s).
```
