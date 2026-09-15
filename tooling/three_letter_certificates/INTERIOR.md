# Entire three-letter interior translation

An exact full-dimensional interior identity. The argument uses the complete
row-letter model in MODEL.md. It does
not claim positivity from reciprocity or assume integral vertices.

## Statement

For n>=4, let a feasible ordinary LR triple (lambda,mu,nu) have at most n
rows and at most three content entries. Suppose its full row-letter polytope
has dimension D=2n-5. Pad lambda and mu to n rows and nu to three. Define

    delta_lambda_i=2(n-i)+3, delta_mu_i=2(n-i),
    delta_nu=(n+2,n,n-2).                                    (1)

For every positive integer t, the ENTIRE interior integer count is

    # (int(t H_b) intersect Z^D)
      = c^(t lambda-delta_lambda)_(t mu-delta_mu,t nu-delta_nu), (2)

where the right side is zero if a shifted boundary is not a nonnegative
partition, or if the shifted skew shape is invalid. The original integer
stretch and the full lattice are retained. Thus Ehrhart reciprocity gives

    P_b(-t)=(-1)^(2n-5) c^(t lambda-delta_lambda)
                                 _(t mu-delta_mu,t nu-delta_nu). (3)

The index is seven for n=6. Degenerate fibers require their relative-interior
system and are outside this full-dimensional identity as stated.

## Translation array

Use the fixed array g with

    g_11=3, (g_21,g_22)=(1,2),
    (g_i1,g_i2,g_i3)=(1,1,1) for 3<=i<=n.

Its row totals are three and its content is delta_nu. Together with
delta_mu it has outer partition delta_lambda. Translate every entry by g.
For every nonconstant column or word inequality, the slack of this fixed
array at the delta boundary is exactly one. Every nonconstant entry
nonnegativity slack is one except g_22=2. The only normal-zero tests are
the fixed first row, lambda_1>=lambda_2 (twice), lambda_2>=lambda_3, and
the tautological word tests at the opening rows.

For a full-dimensional fiber, an interior integer point makes every
nonconstant inequality strict, hence gives each at least one. Moreover

    a_22 >= a_33+1 >= 2

follows from the row-three word test and nonnegativity of a_33. Thus even
the exceptional subtraction g_22=2 leaves a nonnegative entry. Subtracting
g consequently gives every nonconstant weak inequality of the shifted
model. Adding g to any shifted feasible integer array gives every original
nonconstant inequality strictly, and the original boundary equations.
The maps are inverse translations in the full integer lattice.

## Original boundary and zero cases

It remains to prove that an original interior array forces the shifted
boundary to be legal, so that no formal nonpartition character is hidden
in (2). These are exact consequences of the strict inequalities:

- Each mu_(i-1)-mu_i is the sum of a_i1 and the column(i,1)
  slack, hence at least two.
- lambda_1-lambda_2 is the sum of column(2,1) and word(2,1)
  slacks, hence at least two.
- lambda_2-lambda_3 is the sum of column(3,2) and word(3,2)
  slacks, hence at least two.
- For i>=4, lambda_(i-1)-lambda_i is a_(i-1,3) plus
  column(i,3) slack, hence at least two.
- nu_1-nu_2 is a_n1 plus word(n,1) slack, and nu_2-nu_3
  is a_n2 plus word(n,2) slack; both are at least two.
- nu_3 is the sum of the n-2 positive third-letter entries, hence at
  least n-2. The last row total is at least three, so lambda_n>=3.
  mu_n>=0 is unchanged by (1).
- The first row total a_11 is at least a_22+1>=3; the second is
  a_21+a_22>=3; all later totals are sums of three positive entries.

Applying these inequalities to the stretched boundary proves that all
differences in (1) remain dominant and nonnegative and the shifted row
totals are nonnegative. Size balance is preserved since both delta boundary
sizes differ by 3n. If any shifted condition fails, no original interior
integer point exists. Conversely, any shifted valid tableau translates to
an original interior point. This establishes (2), including empty interiors.

## Dimension and polynomial meaning

The same row/content elimination as for n=6 gives (n-2)+(n-3)=2n-5 free
integer entries with an integral projection inverse. The parameter delta
itself has a strictly feasible g for all nonconstant inequalities, so the
bound is attained. LR polynomiality and Ehrhart reciprocity apply to the
entire rational polytope in this lattice. No vertex-integrality assertion
or change of dilation is used.

At b=delta, formula (2) becomes the exact interior-translation law

    E_delta(-t)=-E_delta(t-1).

The case t=1 has one interior point g because the shifted boundary is zero.
This is a full family symmetry, but it does not by itself prove ordinary
coefficient positivity. A complete polynomial or an independent structural
identity is still needed for a sign claim.

## Next discriminators

The n=6 base delta=(13,11,9,7,5,3; 10,8,6,4,2,0; 8,6,4)
was checked by its complete exact Jacobi-Trudi polynomial, unused independent
positive counts and a whole-hive polynomial. Complete interior point sets on
three base/perturbed families have counts 1, 2 and 16, matching shifted bare
LR counts. The full-dimensional boundary (12,11,9,7,5,3; 10,8,6,4,2,0;
7,6,4) has 148 lattice points but no interior point at grade one; at grade
two it has 37 interior points, exactly the shifted LR count. The explicit
rational strict witness certifies dimension seven in both grades. This supplies exact whole-object checks in addition to the finite normal
certificate. It does not extend the theorem to lower-dimensional fibers.

## Why the lower rank boundary is necessary

The statement does not extend to n=3: a_33 is then a
boundary constant, so full dimension one does not force it to be positive.
The exact triple (3,2,1; 2,1,0; 2,1,0) has P(t)=1+t; at t=2 its
interior count is one, while the proposed shifted content has a negative
third part. The general statement starts at n=4, where every
entry used in the strictness argument except a_11 is nonconstant. The
six-row theorem retains its full stated scope.

## Complete determining-space reduction

The interior-translation lemma supplies a stronger exact test of its
own distinguished family. It is not a degree guess or a fit chosen after
looking at values.

For n>=4, let delta be the complete boundary in this interior theorem and set
P_n(t)=c^(t delta_lambda)_(t delta_mu,t delta_nu). Its full dimension is
2n-5, and the proved interior identity gives

    P_n(-t)=-P_n(t-1).

Put s=t+1/2. The polynomial R_n(s)=P_n(s-1/2) is odd and has degree at most
2n-5, hence

    R_n(s)=s H_n(s^2), deg H_n<=n-3.                           (1)

Therefore exactly n-2 distinct values of P_n at t=0,...,n-3 determine the
entire polynomial in this PROVED space. Dividing by s gives n-2 values of
H_n at distinct rational nodes (t+1/2)^2; the Vandermonde determinant is
nonzero. P_n(0)=1 is the known nonempty-object constant. Independent positive
counts at t=n-2 and n-1 are not used in reconstruction and remain required
holdouts. This is an all-coefficient implication from a reviewed identity,
not a reduced fit to a selected set of ordinary powers.

For n=6 the determining space has four parameters, with positive counts at
1,2,3 plus the known constant. Positive counts at 4 and 5 are unused checks.
For n=5 they are 1,2 with holdouts 3,4; for n=4 they are 1 with holdouts 2,3.
The entire affine/Hessenberg calculation supplies a separate symbolic vector
for comparison. Its original offsets are never dropped in the accepted
calculation.

The independently checked finite roster consists of these three complete delta families,
one additional n=6,u=4,v=3 multiple-overlap family with alpha=(12,8,4), the
u=v=2 diagonal-character boundary with alpha=(6,4,2), and the empty object.
Each complete observed whole vector is preserved before any sign comparison.
Wrong-offset vectors retain auxiliary-control labels. Count evidence must
state its engine and scope; another wrapper around lrcalc is not independent.

This makes the interior mechanism operational without extrapolating beyond
its full-dimensional hypotheses. General non-delta boundaries have the
shifted LR right side in the theorem, not the symmetry (1), and therefore do
not acquire the smaller determining space automatically.
