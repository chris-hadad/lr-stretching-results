# A67: exact column coarsening and the complete quadratic obligation

Curated mathematical proof from **A67**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Proposed root reduction. It is an identity for ENTIRE transportation polynomials, not a positivity theorem for a weighted moving sum.

## 1. Complete split-column fiber, all endpoints retained

Let a,b be positive integers and c=a+b. Merge two labeled columns a,b of an arbitrary three-row table into a column c. Each integer parent table X has a nonnegative integer vector v=(v1,v2,v3) in its merged column, of sum ct. Its split lifts are exactly


```text
w1+w2+w3=at,  0<=wi<=vi,  wi integral;
```

the two child columns are w and v-w. This is a full integer bijection, with no deleted row, relaxed exterior condition, or residue index. In free coordinates w1,w2 it is a saturated two-dimensional lattice polygon when its actual dimension is two; zero entries and endpoint collapses give the lower-dimensional original fiber. Adding the split column increases the whole actual dimension by two when every original row and column margin is positive.

For any integers A>=0 and v_i>=0 with C=sum v_i and 0<=A<=C, set B=C-A. Define


```text
L(A,v)=(1/2) sum_(i=1)^3 min(A,B,vi,C-vi),
V(A,v)=(1/2)[A^2-sum_i(A-vi)_+^2+sum_i(vi-B)_+^2].
```

The EXACT number of split lifts is


```text
W(A,v)=1+L(A,v)+V(A,v).                         (1)
```

Here L>=0 is the interval-cut functional and V>=0 is the polygon's area in the free saturated lattice. Both are homogeneous in A,v, of degrees one and two. On a point both vanish; on a segment V=0 and L is its saturated length. The formula keeps weak upper caps, integer endpoints and every equality wall.

To prove (1), bounded-composition inclusion-exclusion gives


```text
W=sum_(I subset[3]) (-1)^|I|
     binom(A-v(I)-|I|+2,2),                    (2)
```

where a binomial is zero unless its upper argument is at least two. For empty I it is (A^2+3A+2)/2. For a singleton the contribution is -[(A-vi)_+^2+(A-vi)_+]/2. For a pair, complement its missing index to get [(vi-B)_+^2-(vi-B)_+]/2. The triple term is zero because A<=C. This is valid at integer positive-part values one and zero: the pair polynomial has its exact zero at one, not an omitted strict shift. The linear term becomes L because


```text
min(A,vi)-(vi-B)_+=min(A,B,vi,C-vi).
```

The quadratic term is V by the ordinary area formula for a capped two-simplex, or by taking the leading coefficient of the complete homogeneous two-dimensional count (2). Lower-dimensional strata follow from the same exact formula; no generic degree is assigned to a collapsed fiber.

The complete parent-to-child identity is consequently


```text
P_split(t)=P_merged(t)
   +sum_(X in T_merged(t) integral) L(at,X_column)
   +sum_(X in T_merged(t) integral) V(at,X_column).   (3)
```

Every parent table appears once, and every split table appears once in its fiber. This is also the original all-stretch LR count identity after the accepted full table constructor. No general hive/table metric equivalence is asserted.

## 2. Exact global consequence IF the weighted quadratic gain is paid

For each legal parent and split define G_2 as the ordinary t^2 coefficient of the COMPLETE two weighted sums in (3). Then


```text
c2(P_split)-c2(P_merged)=G_2.                    (4)
```

The sufficient universal claim G_2>=0 would prove c2>=0 for EVERY three-row transportation polytope: start from its one-column point and split successively into the prescribed positive columns. The number of columns is a strict terminating measure. Delete forced-zero rows/columns first and keep the two-row/point cases at their actual degrees. This gives a complete coverage implication, not an assertion that G_2 has already been signed.

The weights in (3) being pointwise nonnegative does NOT sign their ordinary coefficients. Parent lattice points and the break lines of L,V move with t. Even sums of nonnegative homogeneous polynomial weights can have lower ordinary terms (for example sum_(j=0)^t j^2 contains t/6). A theorem about a fixed homothetic positive fiber does not commute with this moving parent sum. The exact gap is the complete weighted coefficient G_2, with both L and V and every cap wall present.

The earlier two-row/prism-slice positivity theorem, credited to Ferroni--McGinnis and already used in accepted A56, covers fixed fibers but supplies no such moving-parent coefficient rule by itself. Its primary source is https://arxiv.org/abs/2202.11808; no new attribution or external novelty claim is made here.

## 3. Why the previous sector shortcut fails

The accepted A65 T5 original, after row reordering to (1,1,8) with columns (5,1,1,1,1,1), has


```text
S12=-260131/12600, S3=1015/36, c2=95119/12600.
```

The full polynomial is row-invariant, but the assignment-sector payment is not. Choosing a large first row avoids that particular failure, so it is not enough to retire a canonical-order strategy.

A67 H4 has rows (20,20,20) and sixty columns equal to one. Every row ordering is identical. The exact all-t assignment formula gives


```text
S12=-3991547606142494009561036875954587901689182268859930249257556171503956683
    /227040097471642086412801496448967011495289682146436302073696508104961600 <0.
```

Its ENTIRE three-class subtotal is positive and restores a positive full c2; exact values and all grouped assignments are in canonical-payment-H4-v1.json, with the later independent algebra check. H4 therefore kills one-plus-two positivity even in canonical row order. It does not kill full three-row c2 positivity, the split-column gain (4), or unrestricted KTT. Its degree is 118 from the original positive table lattice. This is exact coefficient differentiation of an accepted all-t formula, not an interpolated full degree-118 vector; the low-grade original joins are not misreported as independent c2 reconstruction.

## 4. Comparison and next sharp discriminator

Direct row elimination is also exact:


```text
P(t)=sum_(0<=z<=tc, sum z=tr3)
          #T((tr1,tr2),tc-z).
```

It retains N-1 moving fiber parameters. Column coarsening (3) has a two-dimensional local fiber regardless of N and offers a terminating whole-object induction, so it is the stronger immediate contraction to pursue. Its complete weighted sums, not the unweighted parent polynomial, are the required state.

Challenge (4) on H2 versus H5, where H5 merges two of H2's unit columns into a column two; and on accepted unequal T4 versus H6, where H6 merges its columns three and two into a column five. Verify both entire endpoint vectors, all determining and unused grades, and the literal split fibers. A negative G_2 would refute this sufficient induction but would not be a negative original. Positive controls leave the all-margin G_2 theorem open; they do not justify a larger positive panel as the next task. The next theoretical discriminator is a complete closed formula or cancellation-preserving recurrence for the weighted sums in (3), compared with the new positive-occupation kernel and its zero-column recurrence.
