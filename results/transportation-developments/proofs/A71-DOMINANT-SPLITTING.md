# A71: complete unequal dominant-parent splitting

Curated mathematical proof from **A71**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation. This argument was developed from the accepted A70 full cap and dominant-parent identities before semantic reading of the completed Pro050 proofs. No provider working result is a premise. Its unbounded claim is established by the analytic argument below; finite complete-original checks are separate controls.

## The full original and statement

Let d=(d_1,...,d_m) be nonnegative integral old-column widths and D=sum d_j. Let r_1,r_2,r_3>=D, set c=r_1+r_2+r_3-D, and split the merged column c into s,c-s with 0<=s<=c. Parent columns are (c,d), child columns (s,c-s,d). Both are the ENTIRE transportation counts and hence the entire lambda-outer LR polynomials under the accepted A65 constructor. All labeled row/column positions, including zeros, are retained in the original record. Zero old columns may be removed for the formula.

For D>0, the complete ordinary quadratic gain G(s) is strictly positive whenever 0<s<c and is zero at s=0,c. The theorem holds for arbitrary unequal rows and arbitrary old-column count. In particular the child's entire ordinary c2 is positive. This extends the balanced A70 theorem; it is not an all-coefficient theorem, arbitrary nonfree-parent splitting, all transportation c2, whole rank seven or unrestricted KTT.

For D=0 the parent is a point. At a genuine positive split the child's actual degree is p-1, where p is the number of positive rows. Its c2 is positive for p=3 and zero for p<=2. The all-zero table and zero split endpoints are points. Thus the gain is nonnegative in every allowed degeneration.

Rational margins/split parameters mean scaling ALL margins together to integral values, then dividing the quadratic coefficient by the square of that scale. No lattice or residue is relaxed. The analytic inequalities extend continuously to real parameters, but counting statements retain the scaled integral original.

## Premises, original count and degree

Every old-column allocation is legal in the parent since each old row total is at most Dt<=r_i t. Its remaining entry is forced. Hence P_parent(t)=product_j binom(d_j t+2,2) at every integer t>=0. For D>0 all rows are positive; with m positive old widths the actual parent degree is 2m and a genuine child's degree is 2m+2. The strictly positive table r_i c_j/sum r supplies the interior; the free active table chart is saturated and the incidence matrix is totally unimodular. These degrees precede extraction. Zero split parts retain the parent's degree.

Write C(h) for the complete A70 weighted-cap quadratic, with the exact truncated count and once-only offsets of CONVEX-CAP.md. Let Q=sum_j d_j^2 and

```text
K=Q/36-11D^2/72,
F(h)=h^2/2+Dh/12+K.
```

A70 proves:

```text
C(h)=0 for h<=0;
C is convex and nondecreasing on the entire real line;
C(h)=F(h) for h>=D;
C(D)=31D^2/72+Q/36<=11D^2/24;
C(h)<=11Dh/24 for 0<=h<=D.
```

All labeled subset sums and nonnegative slope jumps are included. Individual harmonic weights need not be positive.

Set a_i=r_i-D>=0 and A=a_1+a_2+a_3, so c=A+2D. The exact full singleton/pair identity is

```text
G(s)=s^2/2+9Ds/4
     -sum_i C(s-a_i)
     +sum_i [F(c-s-a_i)-C(c-s-a_i)].             (1)
```

This is the A70 whole count identity before coefficient extraction, including every paired term and the strict original binomial shifts. The triple cap vanishes over 0<=s<=c with its actual shift. Formula (1) is symmetric under s -> c-s and has zero endpoints. It remains exact at every subset-sum tie. We prove its sign on 0<s<=c/2.

## Why at most one paired cap can remain

Put x_i=s-a_i and y_i=c-s-a_i. A paired quadratic correction is zero whenever y_i>=D. If y_i<D, equivalently

```text
s>a_j+a_k+D.
```

Two such inequalities, for distinct i, would imply 2s>c+a_k>=c, contrary to s<=c/2. Thus at most one y_i is strictly below D. Also x_i<=y_i. If y_i<D, then

```text
x_j=s-a_j>a_k+D>=D,
x_k=s-a_k>a_j+D>=D.                            (2)
```

So the SAME coupled row constraints that admit a pair force the other two singleton caps into their exact terminal formulas. This is why the paired correction can be handled without a sign assumption on F-C.

## Region 1: every small split

For 0<s<=D, every y_i=a_j+a_k+2D-s>=D, so all paired corrections vanish. Each x_i<=s and C is nondecreasing. From the complete chord bound,

```text
G(s)>=s^2/2+9Ds/4-3C(s)
     >=s^2/2+7Ds/8>0.                         (3)
```

Negative x_i cause no exception since C(x_i)=0.

## Region 2: s>D and no active paired cap

Assume all y_i>=D. The row variables satisfy

```text
0<=a_i<=L=A+D-s,   sum_i a_i=A.
```

Since s<=D+A/2 and s>D, one has A/2<=L<A. The vertices of this capped simplex are exactly the permutations of (0,L,A-L), with the obvious coincident vertices at L=A/2. Indeed a vertex has two independent box equalities; two zero coordinates would require A<=L, and two upper coordinates require 2L<=A, possible here only at equality.

The function sum_i C(s-a_i) is convex. Expressing any feasible point as a convex combination of these vertices gives

```text
sum_i C(s-a_i)<=C(s)+C(D)+C(q),
q=2s-A-D<=D.                                  (4)
```

This is a full convex extremum, not a selected-row or subset bound. Since s>D, C(s)=F(s), and C(q)<=C(D) even when q<=0. Substituting the exact terminal coefficients,

```text
G(s)>=13Ds/6-5D^2/18-Q/18-C(q)
     >=13Ds/6-17D^2/24-Q/12
     >=11D^2/8+(13D/6)(s-D)>0.                (5)
```

The last step uses Q<=D^2. Equality walls y_i=D belong to this region and retain their original zero paired corrections.

## Region 3: the unique active paired cap

Let y_i<D be the unique one and let j,k be the other two rows. By (2), both C(x_j) and C(x_k) are their exact F values. All other paired corrections are zero. Straight expansion of the COMPLETE expression (1) gives

```text
G(s)=a_j a_k+(13D/6)(a_j+a_k)
         +167D^2/72-Q/36-C(x_i)-C(y_i).       (6)
```

This identity is valid when either argument is negative too: F was the untruncated polynomial throughout, while C retains its actual support.

Because x_i<=y_i<D, monotonicity gives C(x_i)+C(y_i)<=2C(D). Therefore

```text
G(s)>=a_j a_k+(13D/6)(a_j+a_k)
         +35D^2/24-Q/12
     >=a_j a_k+(13D/6)(a_j+a_k)+11D^2/8>0.    (7)
```

No sign of the paired remainder is asserted or needed. In particular the accepted full auxiliary c2=-7/24 control remains valid.

The three regions exhaust the half-interval and include every old subset-sum knot. Reflection gives the other half. At s=0,c the original itself is unchanged, so G=0 at its actual degree. For D>0, P_parent has positive c2 because at least one positive width occurs in its product, proving the child's positive c2 as well.

## D=0, original zeros and scope

When D=0, old columns are forced zero and the parent has one column and exactly one table. For c>0 and 0<s<c, the active p-by-2 table has actual dimension p-1 and a strictly positive rational interior in its saturated integer chart. If p=3, c2 is its positive leading Ehrhart coefficient. If p<=2, degree is at most one and c2=0. At c=0 all rows vanish; every table is a point. These cases never divide by D or assign a generic degree to a boundary.

The result pays every split ratio for every free-old-allocation parent r_i>=D. A final child therefore has positive c2 whenever some two columns leave residual total D<=min r_i (with the stated D=0 lower-dimensional conventions). It does not yield a terminating construction of arbitrary three-row tables: once the unsplit columns' residual exceeds a row, old allocations become constrained and equation (1) no longer applies without additional corrections. Positive stable operations in other architectures still leave their original bases unsigned.

The stronger derivative proposal C'(h)<=13h/12 is not used, proved or refuted here. The present proof uses the accepted complete convexity, exact terminal quadratic and coupled row constraints. A negative whole gain remains a mechanism obstruction only; a negative ordinary coefficient of an entire legal original alone activates the candidate protocol.
