# A complete positive rank-six cone from the principal Horn split

Root-originated Astra004 construction, 9 September 2026. Independent review complete; see
review/DISPOSITIONS.md. The source-defined H-domain below has dimension seventeen and includes
a full-dimensional original-box hive outside Cdagger. It does not cover every
rank-six boundary, every Horn facet, or all boxed degenerations.

## Full tableau coordinates

Pad `lambda,mu,nu` to six nonnegative parts, with lambda outer and total
balance. Let `a_i=lambda_i-mu_i`. An LR tableau is specified by nonnegative
integers `x_ij`, the number of labels `j` in row `i`, with `x_ij=0` for
`j>i`, fixed row sums `a_i` and content sums `nu_j`. The complete column
and lattice-word conditions are

```text
mu_(i-1)-mu_i + sum(k<j) x_(i-1,k) - sum(k<=j) x_(i,k) >= 0,
                                              2<=i<=6, 1<=j<i;
sum(r<i) x_(r,j) - sum(r<=i) x_(r,j+1) >= 0,    1<=j<i<=6.
```

Rows are weakly sorted and their counts determine their fillings uniquely.
The first inequalities express strict increase down columns; the second
test the beginning of each label block in the row reading word. Together
with all twenty-one nonnegativity rows these are the entire fifty-one-row
LR system, not a selected subset.

Set

```text
S = sum(i=1..3) (mu_i+nu_i-lambda_i),
A = lambda3-mu3-nu3, B = mu4+nu4-lambda4.
```

Take the nine cross counts `y_ij=x_(i+3,j)`, `1<=i,j<=3`; their row sums
are `r_i`, column sums `c_j`, and total is `S`. Put `s=x_32`, `v=x_54`.
The row and content equations give the full affine reconstruction:

```text
row 1: a1
row 2: a2-nu2+c2+s,  nu2-c2-s
row 3: A+c3-s,  s,  nu3-c3
row 4: y11,y12,y13,  a4-r1
row 5: y21,y22,y23,  v,  a5-r2-v
row 6: y31,y32,y33,  B+r1-v,  nu5-a5+r2+v,  nu6.
```

All twelve row/content identities hold modulo total balance and `sum y=S`.
Conversely every full LR array gives these exact coordinates. Nonnegativity
of `x_32,x_31,x_54,x_64` gives the necessary bounds

```text
y_ij>=0, sum y_ij=S,
0<=s<=A+c3, 0<=v<=B+r1.                           (1)
```

Deleting `y33` gives a saturated ten-coordinate integer chart. The forward
and inverse maps use only integer coefficients and selected coordinates.

## Exact complete boundary domain

Require `S,A,B>=0`. For each of the fifty-one full parent inequalities,
substitute the displayed reconstruction and write it as

```text
d(b) + sum(i,j) w_ij*y_ij + e*s + f*v >= 0.
```

Its exact minimum over (1) is the following linear boundary form:

```text
d(b) + min(e,0)*A + min(f,0)*B
     + S*min(i,j) [w_ij+min(e,0)*[j=3]+min(f,0)*[i=1]].  (2)
```

Minimize first over the two interval endpoints, then over the simplex; this
derives (2) without an optimizer or a sampled vertex set. Define `Csplit`
to be the trace section of the nonnegative partition cone where all fifty-one
forms (2) and `S,A,B` are nonnegative. The exact integer forms are serialized
in `science/results/A004-SPLIT-CONE-001.json`; the maintained
`slr_ehrhart.rank6_split` derives them directly in source. There are twenty-eight
distinct nonzero raw minimum forms before removing trace redundancies. No
irredundant facet list or complete extremal-ray roster is claimed.

For every boundary in `Csplit`, every model point satisfies every parent
inequality by its exact minimum. The preceding inverse proves that every
parent point is a model point. Thus (1) is the complete real LR row polytope,
and the maps identify its full integer lattice. All parameter walls and
dimension drops are included. No Horn inequalities are discarded on the
assumption of genericity: the complete tableau construction itself proves
LR feasibility on this domain.

The boundary

```text
lambda=(37,33,25,15,9,5),
mu=nu=(20,16,12,8,5,1)
```

has `S=A=B=1`, strict partition inequalities and strictly positive values
for every nonzero form (2) modulo trace. These exact checks are in the
certificate. Hence `Csplit` contains an open set in the seventeen-dimensional
trace hyperplane and has dimension seventeen.

## All ordinary coefficients and actual new membership

The two widths in (1) depend on one complete column and one complete row
of a three-by-three composition matrix. Their nine-coordinate gain vectors
have sums three each and overlap one. Their covariance term is exactly zero,
so A01 gives the full polynomial

```text
P_b(t) = binom(S*t+8,8)
         * (1+(A+S/3)*t) * (1+(B+S/3)*t).          (3)
```

Every coefficient through actual degree is strictly positive. For `S>0`,
the degree is ten: the open simplex and two positive interval fibers give
full dimension ten. For `S=0`, the polynomial is `(1+A*t)*(1+B*t)`, of
degree two, one or zero according to the positive interval lengths.
The linear coefficient is `A+B+(H_8+2/3)*S` on this complete domain.

The original-box boundary

```text
lambda=(9,8,6,4,2,1), mu=nu=(5,4,3,2,1)
```

has `S=1,A=B=0`; its entire degree-ten polynomial is
`binom(t+8,8)*(t+3)^2/9`. It is historical FE/024, with area thirty.
Both this point and the displayed domain-interior point are outside both
tested inner orientations of Cdagger. The latter is an interior point of
`Csplit`, so the new coverage includes an open set, not merely one new ray.
No assertion about disjointness from every historical native cone is made.

Moving one box from row four to row three gives FE/025,
`lambda=(9,8,7,3,2,1)`, with the same inners. It has `S=0,A=B=1` and
`P=(t+1)^2`, agreeing with its two rank-three Horn factors.

## Failed extension and next route

The neighboring boxed FE/018 boundary `lambda=(8,7,6,4,3,2)` with the same
inners has `S=3,A=B=0`, but violates the full-domain condition from
`x_21>=0`. Applying (3) anyway predicts `P(1)=660`; its complete Normaliz
count is seventy-six. This is an exact failure of the unrestricted chart,
not a negative coefficient. The omitted cuts cannot be ignored.

The next extension must account for those cuts or use a different complete
chart. Other principal/nonprincipal Horn splits, their actual coverage and
degenerate boxed populations remain live. The maintained recognizer refuses
unsupported boundaries instead of treating them as infeasible or positive.
