# A strict rank-six gap-one family with a complete positive factorization

Derivation dated 9 September 2026, with independent computational checks. This is an unbounded family at ordinary rank six,
not a proof of all rank six or a whole-box certificate.

## Family, lattice, degree and codegree

Let `alpha=(alpha1,...,alpha5)` be strictly decreasing positive integers,
and let `beta=(beta1,...,beta6)` be weakly decreasing positive integers of
the same total. Assume every proper nonautomatic dominance gap is positive:

```text
Delta_k = alpha1+...+alpha_k - beta1-...-beta_k > 0,  k=1,...,4,
Delta_3 = 1.
```

The entire straight-GT count is `P(t)=K_(t*alpha,t*beta)`. For the ordinary
LR realization put `kappa_i=sum(j=i..6) beta_j`; the complete skew-content
identity gives `(lambda,mu,nu)=(kappa,(kappa2,...,kappa6),alpha)`, with
lambda outer. It has ordinary rank six. All statements below concern this
entire count, not a selected face or coefficient of an unrelated series.

The complete weighted-GT staircase argument is supplied in
[the nonuniform GT interior proof](gap-staircase.md).
Its saturated row-sum lattice has dimension
`D=(5-1)*6-5*6/2+1=10`. Strict shape and dominance give a genuine strict
point. Its exact codegree formula has maximum nine, attained at
`3*(6-3)/Delta_3=9`; the other terms are at most eight. Hence `q=9`.

The actual interior count is

```text
I(j) = K_(j*alpha-(10,8,6,4,2), j*beta-5*(1,1,1,1,1,1)).
```

Reciprocity and polynomiality therefore give roots `-1,...,-8` and

```text
P(t) = binom(t+8,8) * (1+B*t+A*t^2).
```

Writing `U=I(9), V=I(10)`, the complete two-interior identity gives

```text
A = (V-10*U+1)/90,
B = (9*V-100*U+19)/90.                             (1)
```

These are determining identities in a proved three-dimensional polynomial
space, with constant term fixed. The counts below are derived symbolically.

## Three-label multiplicities

For a three-part dominant shape `l` and sorted weight `b` of equal total,
the complete GT model has one free coordinate with interval

```text
max(l2,b1+b2-l2,b1) <= x <= min(l1,b1+b2-l3).
```

Thus its multiplicity is one plus
`min(l1-l2,l2-l3,l1-b1,b3-l3)` when dominance holds.
This follows directly by taking the middle GT row `(x,b1+b2-x)` and the
bottom row `(b1)`. It includes a zero third shape part.

At `j=9`, the third dominance gap in the shifted interior data is zero.
The first three labels must fill the first three rows completely: their
number equals the total size of those rows. The bottom two rows use the
last three labels. This proves the complete factorization `U=u*v`, where

```text
u = 1+min(9*(alpha1-alpha2)-2,
          9*(alpha2-alpha3)-2,
          9*(alpha1-beta1)-5,
          9*(beta3-alpha3)+1),
v = 1+min(9*(alpha4-alpha5)-2,
          9*alpha5-2,
          9*(alpha4-beta4)+1,
          9*beta6-5).
```

Here `beta3-alpha3=Delta_2-1>=0` and
`alpha4-beta4=Delta_4-1>=0`. Hence `u,v>=2`.

## The next interior count factors again

At `j=10` the shifted third dominance gap is one. The shape formed by
labels one through three is therefore the top-three shifted shape with
exactly one box deleted from one of its three rows. Its consecutive row
gaps are at least eight, so all three deletions give valid partitions.

The remaining single top box is column-disjoint from the bottom two shifted
rows: even the smallest relevant top-bottom gap is at least eight. For
each deletion its remaining skew character is the same product of `h1`
with the bottom two-row character. Pieri's rule gives exactly the three
valid shapes obtained by adding one box to that bottom shape, including a
new third row. Therefore

```text
V = (sum over three top deletions of the top multiplicity)
    * (sum over three bottom additions of the bottom multiplicity).
```

There are no omitted components, additional column interactions, or alternative
label supports: the first-three-label subshape and its complement give the
inverse decomposition of every tableau.

Each of the four quantities defining `u-1` is `9*m+c`, with integral `m`
and `c` in `{-5,-2,1}`. The two gap quantities share the constant `-2`.
Distinct constants cannot tie. If the two gap quantities tied as minima,
the three-label dominance inequalities would force both distance quantities
to equal them too. To see this, write the gaps as `g1,g2` and distances
as `c,d`; sorted weight implies `g1>=2*c-d` and `g2>=2*d-c`.
If `g1=g2=g<=c,d`, these force `c=d=g`. That equality is impossible
modulo nine here. The minimum is consequently unique.

Replacing nine by ten preserves its winning index, since the largest
difference between the constants is six. At ten the gap to another index
is at least three. A one-box deletion changes each quantity by at most one,
so it cannot change the winner. If a gap wins, the three changes sum to zero;
if the top distance `l1-b1` wins they sum to minus one; if `b3-l3` wins
they sum to plus one. In every case the sum of the three multiplicities is

```text
(10*u+1)/3.
```

The same argument applies to the bottom block, with the two distance
constants exchanged and the corresponding addition signs exchanged. Its
sum is `(10*v+1)/3`. The numerators are divisible by three: every possible
`u` or `v` is congruent to two modulo three. We obtain the exact identity

```text
U = u*v, V = (10*u+1)*(10*v+1)/9.                  (2)
```

## Complete factorization and positivity

Substitution of (2) into (1) yields

```text
A = (u+1)*(v+1)/81, B = (u+v+2)/9,
P(t) = binom(t+8,8)*(1+(u+1)*t/9)*(1+(v+1)*t/9).  (3)
```

Every one of the eleven ordinary coefficients is strictly positive, since
`u,v>=2`. This is the full polynomial at every nonnegative integer stretch.
No nonnegative-numerator or generic coefficient-concavity premise is used.
The slopes can equivalently be computed before multiplying by nine:

```text
p = min(alpha1-alpha2, alpha2-alpha3,
        alpha1-beta1-1/3, beta3-alpha3+1/3),
q = min(alpha4-alpha5, alpha5,
        alpha4-beta4+1/3, beta6-1/3),
P(t) = binom(t+8,8)*(1+p*t)*(1+q*t).
```

The smallest displayed shape control is
`alpha=(5,4,3,2,1), beta=(4,4,3,2,1,1)`. It has `u=v=2`, so
`P=binom(t+8,8)*(t+3)^2/9`. Its ordinary LR triple is
`lambda=(15,11,7,4,2,1), mu=(11,7,4,2,1), nu=(5,4,3,2,1)`.
Its outer area is forty, outside the original finite box.

## A second proof: the complete count at every stretch

This proof makes the compensating geometry explicit and does not reconstruct
from interior values. In the tableau of `t*alpha`, the first three labels
form a shape `eta_i=t*alpha_i-r_i`, `i=1,2,3`, where `r_i>=0` and
`r1+r2+r3=t`. All these shapes are partitions and dominate the first three
contents: each original shape gap and each of `Delta_1,Delta_2` is at least
one. The remaining top row segments are column-disjoint from one another
and from the bottom two rows. This follows from `r_i<=t` and the strict
original shape gaps. Thus their nine label counts form an arbitrary
nonnegative three-by-three matrix `z` with total `t`. Its row sums are `r`
and its column sums `c` are the amounts of the last three labels placed
in those detached rows. All residual bottom contents are nonnegative since
`beta_j>=1` and `c_j<=t`.

For the top block abbreviate

```text
A1=alpha1-alpha2, B1=alpha2-alpha3,
C1=alpha1-beta1, D1=beta3-alpha3.
```

The complete three-label interval has width

```text
min(A1*t-r1+r2, B1*t-r2+r3, C1*t-r1, D1*t+r3).
```

Sorted content and the gap-one total give
`A1>=2*C1-D1-1` and `B1>=2*D1-C1+1`. They ensure the following exhaustive
table, selected by the minimum defining `p` in (3):

| Winning value of p | Required inequalities after using sorted content | Entire interval width |
| --- | --- | --- |
| A1 | B1>=A1+2, C1>=A1+1, D1>=A1+1 | (A1-1)*t+2*r2+r3 |
| B1 | A1>=B1+1, C1>=B1+1, D1>=B1 | (B1-1)*t+r1+2*r3 |
| C1-1/3 | A1>=C1, B1>=C1+1, D1>=C1 | (C1-1)*t+r2+r3 |
| D1+1/3 | A1,B1,C1>=D1+1 | D1*t+r3 |

For example, when `A1` wins, `C1>=A1+1`; sorted content then gives
`D1>=2*C1-A1-1>=A1+1` and
`B1>=2*D1-C1+1>=A1+2`. The minima of the other three widths minus the
chosen one over the simplex of `r` are respectively
`t*(B1-A1-2)`, `t*(C1-A1-1)` and `t*(D1-A1-1)`.
The other table rows follow by the same three vertex comparisons. An active
tie between `A1` and `B1` is excluded by those inequalities; fractional
and integral entries cannot tie. This proves the table for every integral
parameter member and every stretch, including endpoint compositions.

For the bottom block put

```text
A2=alpha4-alpha5, B2=alpha5,
C2=alpha4-beta4, D2=beta6.
```

For an arbitrary ordered three-label content, the exact interval width is
`min(l1-l2,l2-l3,l1-max(weight),min(weight)-l3)`. Apply this to
`l=(t*alpha4,t*alpha5,0)` and `weight=t*(beta4,beta5,beta6)-c`.
It includes all three choices in each maximum or minimum, so a possible
reordering after subtracting `c` is not ignored. The minimum defining `q`
gives the complete alternatives:

| Winning value of q | Entire interval width |
| --- | --- |
| min(A2,B2) | min(A2,B2)*t |
| C2+1/3 | C2*t+c1 |
| D2-1/3 | (D2-1)*t+c1+c2 |

In the constant case `C2>=q` and `D2>=q+1`, so every content or gap bound
is at least `q*t`. In the second case `A2,B2,D2>=C2+1`; the sorted-content
identity gives `beta4-beta5=A2-2*C2+D2-1>=1`. All other bounds therefore
exceed `C2*t+c1` on `c1+c2+c3=t`. In the last case `A2,B2,C2>=D2`, and
`beta5-beta6=B2+C2-2*D2+1>=1`, so the last content is the controlling
minimum. These arguments account for repeated original contents too.

Consequently the entire original tableau count is two affine interval counts
over the full nine-coordinate simplex. One width depends only on the matrix
row sums, the other only on column sums; their offsets are nonnegative and
their gains are at most two. If the row gains are `a_i` and column gains
`b_j`, the nine-coordinate vectors satisfy

```text
9*sum(i,j) a_i*b_j = (sum(i,j) a_i)*(sum(i,j) b_j).
```

The mixed linear moment for the coupled interval model is therefore zero. Their mean widths are
exactly `p*t` and `q*t`, proving (3) directly. The inverse reconstructs the
first-three-label subshape, the two three-label tableaux and the unique
fillings of the detached row segments. Thus this is a complete count
bijection at every stretch. It is not an asserted global affine isomorphism
of the two geometric polytopes when interval lower endpoints change.

The independent checks cover eight cases realizing all top and bottom
branches: forty full GT counts at `t=0,...,4`, every cross-matrix summand
at those sites, and sixteen actual shifted-interior counts. All agree.
Twenty-four direct LR controls, including eight additional sites at five and
six, are independently recorded. Seven of the eight controls are outside
both tested orientations of the previous interior-translation sufficient domain (`Cdagger` in the data); one
overlaps it. No disjoint census count is inferred from this panel.

## Exact scope

The theorem also transfers through justified common dilations and determinant
twists, with their complete reduction words. It does not assert the same
formula when `Delta_3>1`, when shape parts repeat, when contents vanish, or
on another dominance boundary. Those changes alter the proved interior
grades and decomposition. In particular the hypothesis is an integral gap-one
stratum, not an unrestricted homogeneous cone with arbitrary real gap.

The stated literal GT/skew panel, positive-stretch bare-LR controls and
membership challenges are complete. An extension to a changed domain would require corresponding verification. All determining assertions in this proof are
symbolic; numerical agreement corroborates the whole decomposition.
