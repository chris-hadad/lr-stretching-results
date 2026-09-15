# Complete affine compensation for successive overlaps

The complete three-letter model and
interior translation suggest a direct character route on a family with many
successive overlaps. This is an exact all-parameter identity, not a sign
assertion about its individual terms.

For n>=3 and nonnegative integers v<=u<=2v, set

    lambda_i=(n-i)v+u, mu_i=(n-i)v, 1<=i<=n.

Let alpha have at most three parts and total n*u. The LR content is alpha. The entire skew diagram has
n equal rows of length u. Its successive overlaps have length u-v. Unless
u=v, this family generally has several overlaps and is outside a single
overlapping-pair constructor.

The Jacobi-Trudi entry in position (i,j) at stretch t is

    h_(u*t+(v*t+1)(j-i)).                                    (1)

Entries two or more rows below the diagonal vanish for every positive t,
since u<=2v. The determinant is upper Hessenberg with constant subdiagonal
h_((u-v)t-1). Expanding its first block gives the recurrence

    D_n=sum_(k=1)^n (-1)^(k-1)
       h_((u+(k-1)v)t+k-1) h_((u-v)t-1)^(k-1) D_(n-k),
    D_0=1.                                                  (2)

The permutation expansion proves the same recurrence directly: every
nonzero permutation is a sequence of contiguous cyclic blocks; a block of
length k has sign (-1)^(k-1), one long factor and k-1 subdiagonal factors.
This exhausts all permutations rather than selecting a favorable subset.

Because homogeneous functions commute, collect compositions of n with the
same block multiset. If m_k blocks have size k and m=sum m_k, their combined
contribution is exactly

    (-1)^(n-m) m! / product_k(m_k!)
      * h_((u-v)t-1)^(n-m)
      * product_k h_((u+(k-1)v)t+k-1)^(m_k).                  (3)

The slopes sum to n*u and the offsets sum to zero. Every original plus/minus
one and longer-block shift is retained. If u=v, the subdiagonal is h_-1=0,
so only all singleton blocks survive, giving D_n=h_(ut)^n. The u=v=0
boundary gives the empty skew character one. Dominance, nonnegativity and
size balance hold for the original triple at every allowed parameter.

Take the complete coefficient of s_(t alpha) in (3). A homogeneous factor
h_r forces the containing Schur diagram to have first row at least r by
Pieri. Thus a term with a long factor slope greater than alpha_1, or equal
slope and positive offset, vanishes identically at all positive grades.
Keeping an explicit zero record for these terms is exact. The remaining
terms use the full three-variable affine assignment formula with every
original offset. Its eventual polynomial agrees with the entire LR
polynomial by ordinary stretching polynomiality.

For n=6,u=3,v=2,alpha=(8,6,4), this is the interior-shift base. It has 11
block multisets before target containment, compared with 720 determinant
permutations and 32 Hessenberg compositions. The already computed entire
vector is

    (1,236/35,4061/180,17447/360,5033/72,
       24299/360,14233/360,14233/1260).

Its positive and negative character contributions cancel substantially at
every nonconstant ordinary index. For example, c1 is 293/35-57/35, and c2
is 6277/180-554/45. Individual negative signed terms therefore remain
auxiliary. The full vector agrees with independent tableau counts, lrcalc and the
whole-hive Ehrhart series, including the prior determining space and unused
positive grades.

The grouped formula supplies an exact stronger discriminator: test the whole
character with original offsets against the version that discards them,
then compare the complete vector and unused positive counts. The latter is
an intentionally incorrect control, never a second LR model. General
ordinary positivity of the signed formula does not follow from (3) alone.

Classical inputs are Jacobi-Trudi, Pieri and LR stretching polynomiality.
The grouping is an elementary complete Hessenberg determinant expansion;
the current work uses it to preserve and inspect full multiple-overlap
compensation, without claiming those classical identities as new.
