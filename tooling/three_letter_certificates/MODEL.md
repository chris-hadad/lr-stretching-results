# Complete six-row, three-letter LR model

Complete original-domain derivation, independently checked against direct
tableaux, bare LR counts and whole-hive counts. The row-count model is classical LR-triangle structure; the explicit
coordinate elimination and its use in this session do not assert novelty of
Littlewood-Richardson tableaux, polynomiality or their lattice models.

Let lambda and mu be weakly decreasing nonnegative integer sequences padded to
six rows, and nu a partition padded to three entries, with size balance. Put
d_i=lambda_i-mu_i. A negative d_i makes the positive-stretch coefficient zero.
Otherwise use nonnegative row-letter counts a_(i,j), 1<=i<=6, 1<=j<=3, and put
a_(i,j)=0 for j>i. The boundary equations are

    sum_j a_(i,j)=d_i,       sum_i a_(i,j)=nu_j.                 (1)

The ENTIRE additional conditions are

    mu_i + sum_(k<=j) a_(i,k)
       <= mu_(i-1) + sum_(k<j) a_(i-1,k), 2<=i<=6, 1<=j<=3;   (2)

    sum_(r<i) a_(r,j) >= sum_(r<=i) a_(r,j+1),
                                      1<=i<=6, 1<=j<=2.       (3)

All inequalities, including boundary-only and repeated-normal inequalities,
remain in the implementation. No parameter-specific facet deletion is used.

## Bijection and converse

Given an LR tableau, row weak increase uniquely orders its letters. Lattice
reading runs right to left, top to bottom. Inductively no letter greater than
the row index can occur: a letter j in row i must have a preceding j-1, and
that preceding letter cannot be to its right in the same weakly increasing
row. Iterating reaches an earlier row for each decrement. Thus j<=i.

For column strictness, the right endpoint of lower-row entries at most j is
R_i(j)=mu_i+sum_(k<=j)a_(i,k). Above it, the right endpoint of entries less
than j is R_(i-1)(j-1). If the lower endpoint lies in the upper inner shape,
it has no box above and the inequality is automatic. Otherwise dominance of
lambda ensures every relevant column has an upper box. Strictness of all
overlapping columns is exactly R_i(j)<=R_(i-1)(j-1). This proves necessity
of (2), and applying it to the actual letter in each lower box proves
sufficiency. For j>3 the condition is simply lambda_i<=lambda_(i-1).

Within a row, the largest excess of the number of j+1 over j occurs just
after all j+1 entries have been read and before any j entries in that row.
The lattice-word inequalities at precisely these points are (3). Every
other reading prefix has a no-larger excess, so (3) is also sufficient.
Labels above three do not occur and contribute only tautological tests.

Conversely, sort each nonnegative integer row vector into the actual skew
row. Equations (1) give the exact shape and content; (2) gives every strict
column, and (3) every lattice prefix. This construction is inverse to taking
row counts. It includes empty rows, zero content parts and all boundary
equalities. Hence the model counts the entire LR object at every positive
integer stretch, not a face or selected subset of tableaux.

## Seven coordinates and the saturated lattice

Choose x=(a_22,a_32,a_42,a_52,a_33,a_43,a_53). Set

    a_62=nu_2-a_22-a_32-a_42-a_52,
    a_63=nu_3-a_33-a_43-a_53,
    a_(i,1)=d_i-a_(i,2)-a_(i,3).                              (4)

All other entries with j>i are zero. Equations (4) impose both independent
content equations and all six row equations. Size balance then imposes the
remaining content equation. Every solution of (1) has exactly this form.
The inverse is the coordinate projection to the seven displayed entries.
Both maps have integer coefficients and the inverse contains an identity
minor. They identify the ENTIRE affine integer solution lattice with Z^7;
there is no hidden congruence, denominator rescaling or sublattice index.

For a lower-dimensional nonempty fiber, its direction lattice is the
intersection of this Z^7 with its rational direction space and is therefore
saturated. If its affine span contains no lattice point, it must retain its
affine lattice coset rather than silently translating by a rational point.
No assertion of vertex integrality is needed or made.

Under stretch t, all right-hand boundary terms multiply by t and the normal
matrix is fixed. Nonnegativity and row totals bound every coordinate. The
rational polytope therefore has dimension at most seven. LR polynomiality
turns its Ehrhart quasipolynomial into a period-one polynomial with degree
equal to the actual dimension for nonempty fibers. A proved upper bound of
seven supplies eight distinct determining grades; numerical acceptance also
requires unused positive grades and an independent complete model.

Positive-stretch infeasibility has the zero polynomial by campaign convention.
The collapsed t=0 triple itself has coefficient one even for a family with
no positive-stretch points; it must not be used as the zero polynomial's
constant. For a feasible family, saturation gives an integer point at t=1,
and the ordinary polynomial has constant one.

## Actual seven-dimensional witness

Take lambda=(130,80,50,32,20,5), mu=(80,50,30,20,12,0),
nu=(90,27,8), and x=(10,8,4,3,2,3,2). The restored rows are

    (50,0,0), (20,10,0), (10,8,2),
    (5,4,3), (3,3,2), (2,2,1).

Every nonconstant inequality in (2), (3) and nonnegativity is strict; the
only equalities are the identically zero word tests. Thus an open real
neighborhood of x in Z^7's ambient space is feasible and the dimension is
seven. This is an exact geometric witness, not interpolation evidence.

## Normal roster and next test

The literal system has 42 rows: 15 nonnegative entries, 15 column tests and
12 word tests. Seven are boundary-only. Three pairs have identical oriented
normal vectors but potentially different offsets. Keeping both offsets,
there are 32 distinct nonzero oriented normals in Z^7. The complete normal
populations at orders 1 through 6 are 32, 496, 4960, 35960, 201376 and
906192. These are auxiliary supports, not LR triples or coverage increments.
The q3/q4/q5/q6 systems protect c4/c3/c2/c1 through their complete local
weights, original lattices, full fields and the geometric implication. The companion PROOF.md supplies the complete finite certificate and sign
implication; this model derivation establishes the domain and lattice.

The lattice identity (4) does not imply all normal-coordinate images have
index one. Every index and its original image numerator must be checked
before any Gram-type compression or finite local evaluation.
