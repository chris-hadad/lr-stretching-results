# A65: a complete original-offset kernel for three-row transportation

Curated mathematical proof from **A65**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

This is a complete finite formula for every coefficient of every three-row table polynomial, with an explicit degree-two specialization. It is not an assertion of arbitrary-column coefficient positivity or a worldwide novelty claim. The full LR/table bridge and the all-rank first-jet theorem are accepted A006 premises. The two A2 chamber polynomials below are independently derived here and checked against complete table and bare LR counts.

## Entire object, lattice and degree

Let r=(r1,r2,r3) and c=(c1,...,cN) be balanced nonnegative integral margins. Delete forced-zero columns for the formula while retaining their positions in the original record. Zero rows remain allowed. If the total M is zero, the table is a point. Otherwise let p and q be the numbers of positive rows and columns. The strict rational table r_i c_j/M in the active rectangle proves dimension d=(p-1)(q-1); a spanning tree/free upper-left chart proves the saturated table lattice, and the incidence matrix is totally unimodular. Its entire count is a polynomial of actual degree d. P(0)=1.

The accepted original LR constructor uses suffix sums R_i,C_j:


```text
lambda=(M+R2,M+R3,C1,...,CN),
mu=(M,M,C2,...,CN), nu=(R1,R2,R3), lambda OUTER.
```

It is a whole all-grade count identity, including zero margins. No original hive metric, face-volume or local BV identification is inferred.

## Every labeled assignment and the original offset

Expand the COMPLETE product of column complete-symmetric functions by its three-term Lagrange identity. Keep every f:{1,...,N}->{1,2,3}. Let n_i be the occupation and C_i the sum of columns assigned to i. The accepted original-offset assignment identity has sign (-1)^(n2+2n3), edge multiplicities


```text
a=n1+n2, b=n1+n3, c=n2+n3,
```

and netflow b_i(t)=t(C_i-r_i)+(i-1)n_i-sum_(j>i)n_j. Put


```text
U(t)=x t-c, V(t)=y t-2n3,
x=C1-r1, y=r3-C3.
```

A root-flow table has edge allocations z12+z13=U and z13+z23=V. The complete chamber count for nonnegative integral U,V is


```text
sum_(z=0)^min(U,V)
  binom(U-z+a-1,a-1) binom(z+b-1,b-1)
  binom(V-z+c-1,c-1).                         (1)
```

Repeated edges are all present. There is no omitted determinant partner or additional stretch shift.

For a,b,c>0 the U<=V chamber polynomial is


```text
F_U(U,V)=sum_(k=0)^(c-1) (-1)^k binom(b+k-1,k)
   binom(V+c-1-k,c-1-k)
   binom(U+a+b-1,a+b+k-1).                    (2)
```

Every binomial in (2) means its rational falling-product POLYNOMIAL. To prove (2), Newton-expand the last factor of (1) in z:


```text
binom(V-z+c-1,c-1)
  =sum_k (-1)^k binom(z,k)binom(V+c-1-k,c-1-k).
```

Multiply binom(z,k) by the middle factor and use the full finite Vandermonde convolution. This gives binom(b+k-1,k) times the last binomial in (2), including all endpoints. The V<=U formula F_V swaps (a,c) and (U,V). Their restrictions agree on U=V by (1). Both are full polynomials of degree at most a+b+c-2=2N-2.

The one-occupied cases retain missing edges, rather than using a binomial with lower index -1. If a=0 use B_b(U)B_c(V-U); if b=0 use B_a(U)B_c(V); if c=0 use B_a(U-V)B_b(V), where B_j(z)=binom(z+j-1,j-1). Each factor's argument must be eventually nonnegative. For N=1 this gives the point where supported.

## Exact chamber selection, including initial bands and empty classes

For an affine integer expression at+b, eventual nonnegativity means a>0 or a=0,b>=0. If U or V fails it, the assignment is exterior and contributes zero; a missing-edge case imposes its additional displayed inequality. Otherwise choose the smaller affine expression by lexicographic comparison of (slope,offset). Equal slopes MUST retain the offsets; identically tied expressions permit either chamber.

Substitute the original U(t),V(t) into the selected polynomial and retain its polynomial continuation, even when some early scalar counts on that assignment ray are outside support. No initial grade is replaced by an actual negative-flow count. The original Lagrange identity holds at all sufficiently large integer t; the finite sum of these eventual assignment polynomials therefore equals the entire transportation Ehrhart polynomial identically, at every t including zero. This proves all initial bands without silently discarding them. All one-, two- and three-occupied assignments are included. There is no four-occupied class for three rows.

For c2 it suffices to multiply each falling product modulo t^3. This is an exact finite quadratic kernel for every N, with no chamber census or symbolic multivariate vector-partition solver. Labeled assignments may be grouped only by identical (n,C), retaining their exact multiplicities. A negative sector remains part of the whole sum; no sign assertion is supplied by the representation itself.

## Full original verification and scope

The frozen six-table roster contains five complete 3-by-6 originals and one forced-zero boundary. The 3-by-6 objects are not active subrectangles of the accepted 4-by-5 theorem. They cover tied margins, unequal slopes, a forced-entry region and actual-degree drop. Every full polynomial from (2), all 72 determining/unused values of an independent direct-table dynamic program, and all 72 bare original LR values agree. Twelve unused grades are separate from determining values. The six whole c2 values are


```text
26377/2100, 183109/25200, 785557/50400,
1150889/50400, 95119/12600, 61/12.
```

For T1, r=(2,2,2), c=(1,1,1,1,1,1), the complete c2 sector totals are


```text
one occupied:   32269/900,
two occupied:  -76301/3150,
three occupied: 13/14.
```

Their sum is 26377/2100. Dropping the third sector fails the complete coefficient check. The exact negative two-class term rules out a termwise-nonnegative-assignment proof; it is not a negative original. The example n=(1,1,0), U<=V has signed quadratic -x^2/2, explaining the local failure without changing the whole count.

All six entire polynomials are positive through their actual degrees (ten for T1–T5, four for T6). That is bounded evidence. A separately proved prior degree, the full original/count correspondence, all original zeros and strict shifts, unused grades and negative/failure controls are retained in the cited code and receipts. No broader census, rank-seven closure or general KTT theorem follows. The all-three-positive occupation probe through N=16 is a bounded kernel test; its 1,120 positive chamber rows alone do not prove an all-N sign.
