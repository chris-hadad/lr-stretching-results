# Every LR family with a two-row inner partition

Root extension of the two-row Kostka argument, Astra006. This is an exact
whole-character reduction, with no claimed affine hive isomorphism or
worldwide novelty. Inner commutativity permits putting the short inner
partition in the position nu below.

Let lambda contain mu, padded with zeros to a common length, and let
nu=(a,b), a>=b>=0, with |lambda|-|mu|=a+b. Consider the entire stretching
family c^(t lambda)_(t mu, t nu). One-row and empty nu are included.

## Complete two-variable skew character

If lambda/mu has a column containing at least three cells, its skew Schur
polynomial in two variables is zero. The same positive-width overlap scales
by t, so every positive stretch has LR coefficient zero. This is the
zero-polynomial convention, not a nonempty polynomial of constant one.
The criterion is exact: a three-row overlap occurs precisely when
lambda_(i+2)>mu_i for some i.

Otherwise every nonempty skew column has one or two cells. Define

    h_i = max(lambda_(i+1)-mu_i,0),
    h_0=h_n=0, h=sum_(i=1)^(n-1) h_i,
    ell_i=lambda_i-mu_i-h_(i-1)-h_i.

The h_i cells shared by adjacent rows i and i+1 form a prefix of the upper
row and a suffix of the lower row. They are forced to labels 1 and 2,
respectively. With no column of height three, the forced prefix and suffix
in any row are disjoint. The remaining ell_i>=0 cells are one interval of
single-cell columns. Their weak row word is unconstrained except to use
labels 1 and 2: its forced neighbors, when present, are a prefix of ones
and a suffix of twos. Free intervals in different rows share no column.

Thus every complete semistandard skew tableau, and only such a tableau,
is obtained by choosing those row words independently. Its exact character is

    s_(lambda/mu)(x,y)=(xy)^h product_i h_(ell_i)(x,y).

Every overlap and free length scales exactly with t, giving the all-stretch
identity with ht and t ell_i. No row, column constraint or initial stretch
has been omitted.

## Entire LR reduction

Schur expansion in two variables retains exactly the inner partitions with
at most two rows. Multiplication by (xy)^(ht) shifts both highest-weight
parts by ht. Put k=b-h and W=sum_i ell_i=a+b-2h. When k>=0 and the reduced
dominance conditions hold, the entire polynomial is

    c^(t lambda)_(t mu,t(a,b))
        = K_(t(a-h),t(b-h)),(t ell_1,...,t ell_n).

Equivalently it is the highest-weight coefficient of product_i h_(t ell_i)
at shape ((W-k)t, kt). If b<h, or an ell_i exceeds a-h, the positive-stretch
family is empty and its polynomial is zero. These conditions, containment,
the column-height test and balance give a complete elementary nonemptiness
test at this exact two-row-inner scope. If `W=k=0` the reduced family is a point.

The character proof fixes the original integer stretching parameter. It is
an equality of complete LR polynomials, not a selected face, quotient or
count inclusion. It does not require Ferrers conjugation.

## Linear-coefficient consequence

Apply TWO-ROW-LINEAR-PROOF.md to the complete reduced Kostka family. Every
ordinary LR stretching polynomial with at least one inner partition having
at most two rows has c1>=0. An empty family has the zero polynomial. A
nonempty constant family has polynomial one. Every nonconstant family in
this class satisfies the absolute bound c1>=1.

The exact point test uses augmented weights

    (W-2k, ell_1,...,ell_n).

After deleting zeros, the polynomial is one exactly when there are at most
three positive augmented weights or one equals half their total. All other
admissible cases have c1>=1. This is a theorem at arbitrary outer rank and
area, with the original whole LR object retained. It does not prove all
ordinary coefficients in this class or the unrestricted c1 conjecture.
