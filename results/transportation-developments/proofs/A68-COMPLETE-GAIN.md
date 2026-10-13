# A68: the complete split gain as an exact curvature operator

Curated mathematical proof from **A68**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root-derived mathematics.. Premises are the accepted A65 complete original-offset assignment identity and A67 full coarsening identity, transverse signs and zero-column recurrence. No active provider's working result is used here.

## The entire original and the exact difference

Let r=(r1,r2,r3) and columns (a+b,d1,...,dm) be balanced nonnegative integer margins, with a,b positive for a genuine split. Delete forced-zero columns and retain their original positions in any record. The parent and child are COMPLETE transportation originals, and through the accepted A65 constructor they are whole LR polynomials. With p positive rows and N positive columns their actual dimension is (p-1)(N-1), proved before coefficient extraction by a strictly positive table on the active rectangle, saturated free chart and total unimodularity. All-zero margins give a point. Zero split parts give the identical original. No hive metric equivalence is claimed.

For every labeled assignment of the m remaining columns, let n be its occupation and C its three totals. Let K_n(C;r) mean the ordinary t^2 coefficient of its full signed A65 eventual chamber polynomial, with sign (-1)^n2, U=(C1-r1)t-(n2+n3), V=(r3-C3)t-2n3. Apply its exact eventual support test, its missing-edge conditions and lexicographic (slope,offset) chamber choice. Unsupported assignments contribute zero. This definition retains initial polynomial continuation and every original shift once. K is a homogeneous, piecewise quadratic function of C-r; this follows directly by expanding each original falling product to order two. It is not a positive scalar in general.

For i<j put n'=n+e_i+e_j and


```text
F_(n,C,ij)(s)=K_(n')(C+(a+b-s)e_i+s e_j;r).
```

Then the ENTIRE quadratic gain is


```text
G2 = sum_(all labeled rest assignments) sum_(i<j)
      [F(a)+F(b)-F(0)-F(a+b)].                    (1)
```

Grouping by (n,C) is permitted only with its exact labeled multiplicity. Neither empty occupations nor negative blocks can be omitted.

For a direct proof put L_i=z_i^2/((z_i-z_j)(z_i-z_k)). The complete Lagrange identity has sum_i L_i=1 and h_A=sum_i z_i^A L_i. Therefore


```text
h_A h_B-h_(A+B)
  =sum_(i<j) L_i L_j
     (z_i^A z_j^B+z_i^B z_j^A-z_i^(A+B)-z_j^(A+B)).
```

Multiply by every remaining full h_(d t), extract the original row monomial in the same formal orientation, and then use the eventual chamber polynomial. The equality holds at every sufficiently large integer t, hence identically as a polynomial. Taking t^2 gives (1). This simultaneously extracts BOTH complete weighted sums L and V in A67 COARSENING.md; it is not a replacement of their parent domain or a sign inference from positive fiber values. The n' occupation and its offsets change together in every term. The one-column starting parent and every lower-dimensional endpoint are included.

## The admissible one-dimensional kernels are continuous

On a fixed pair direction the only possible breakpoints come from x(s)=0, y(s)=0 and x(s)=y(s), where x=C1-r1 and y=r3-C3 after the displayed shifts. All are affine forms; identically zero forms retain their original constant offsets. On each open interval F is a polynomial of degree at most two.

Crucially, F is continuous at these breakpoints, including its exact prescribed value. Here n'_i,n'_j are positive. If all three occupations are positive, the A67 formulas


```text
Q_U=A(p,q,r)xy+A(p,r,q)x(y-x),
Q_V=A(p,q,r)xy+A(q,p,r)y(x-y)
```

vanish on their supported axes and agree on x=y. Their exterior value is zero. For two occupied classes the admissible direction resolves the apparent difficulty:

- For (p,q,0), the pair is (1,2); y is fixed. The U polynomial has a factor x in its quadratic part, because its second falling product has a unique zero factor. At x=0 the support boundary is therefore continuous. If fixed y=0, the supported V quadratic is a constant multiple of x^2 and still vanishes at x=0. At x=y>0 both restrictions agree: the extra finite convolution terms have negative first residual of magnitude at most q, strictly less than a=p+q.
- For (0,q,r), the pair is (2,3); x is fixed. The analogous V quadratic has a factor y and vanishes at its varying support boundary. At x=y the extended convolution band has length |q-r|, strictly smaller than the relevant multiplicity q or q+r; the same exact binomial zeros give matching quadratic restrictions.
- For (p,0,r), the pair is (1,3); x-y is fixed. The chamber wall is never crossed. The U quadratic has a factor x, the V quadratic a factor y, so the varying support boundary has value zero. If x-y is identically zero, the original offsets choose one polynomial throughout and its value vanishes at x=y=0.

All letters shown as occupied are positive. Every n' has at least two occupied classes, so this exhausts the operator. General empty-class kernels can be discontinuous in OTHER directions; extending continuity beyond the admissible split directions is unwarranted.

## Exact hinge and curvature forms, including every wall

Let k range over all the above breakpoints, beta_0 be the quadratic coefficient on the leftmost interval, J_k the right derivative minus left derivative at k, and B_k the right quadratic coefficient minus left quadratic coefficient. Then


```text
F(s)=alpha_0+alpha_1 s+beta_0 s^2
       +sum_k [J_k(s-k)_+ + B_k(s-k)_+^2].       (2)
```

This is proved by matching the polynomial and its slope successively across every breakpoint; continuity eliminates value steps and isolated point corrections. The initial interval need not be supported. No smoothing or generic-wall omission is involved.

For c=a+b define


```text
W_(a,b)(s)=length([0,a] intersection [s-b,s]).
```

It is nonnegative, zero outside [0,c], has integral ab, and equals min(a,b,s,c-s) on [0,c]. Integrating (2), or just checking its constant, linear, square and hinge generators, gives


```text
F(a)+F(b)-F(0)-F(c)
   = - integral_0^c W_(a,b)(s) dF'(s)
   = -2ab beta_0
     +sum_k {J_k H_1(k)+B_k H_2(k)},             (3)

H_d(k)=(a-k)_+^d+(b-k)_+^d-(-k)_+^d-(c-k)_+^d.
```

In particular H_1(k)=-W_(a,b)(k). Here dF' includes the ordinary piecewise constant second derivative AND every derivative-jump atom. Summing (3) over every assignment and pair is a closed, exact, cancellation-preserving weighted coefficient operator for the full A67 gain. There is no remaining moving lattice-point sum. The unresolved sign law is for this entire signed curvature measure against W; signing only its chamber interiors or only one pair is insufficient.

The fixed positive A67 simplex measure organizes the individual A coefficients, but the signed differences in (1) and (3) are not nonnegative moment weights. Full row-fiber contraction is also exact but has m moving coordinates; it provides no current sign improvement over this one-dimensional operator. The unrestricted interacting-character program remains a distinct serious alternative.

## A uniform, realizable obstruction to local block payment

Even the sum of ALL THREE pair terms belonging to one rest assignment can be negative strictly inside a common supported chamber. Let n=(p,1,2), p>=1, and suppose every pair node lies in 0<x<y. The (1,2), (1,3), (2,3) quadratic coefficients in s are respectively

    -A(p+1,2,2),  A(p+1,1,3),  0.

Thus its full block in (1) is


```text
2ab[A(p+1,2,2)-A(p+1,1,3)]
  = -ab/[4(p+1)(p+2)(2p+3)(2p+5)] < 0.          (4)
```

This quantifier is analytic. With x=p+1, the accepted zero-column recurrence gives
A(x,2,2)=A(x,1,2)-A(x+1,1,2)-A(x,1,3). The accepted q=1 formula gives


```text
A(x,1,2)=3/[8x(2x+1)(2x+3)],
A(x,1,3)=5/[4x(2x+1)(2x+3)(2x+5)].
```

Substitution simplifies their difference to -1/[8x(x+1)(2x+1)(2x+3)], proving (4) without a fitted occupation table.

These are assignments of LEGAL COMPLETE ORIGINALS: for every p>=2 and positive integers a,b, use rows (p-1,1,a+b+4), rest columns (2,1^(p+2)) and merged column a+b. Assign p unit columns to color one, the width-two column to color two, and two unit columns to color three. Then C=(p,2,2), x_base=1 and y_base=a+b+2. Every point on every pair segment 0<=s<=a+b satisfies 0<x<y, so no omitted wall, boundary, empty class or relaxed margin explains the defect. Both full endpoint polynomials retain all other assignments. This is an infinite family of negative INTERNAL BLOCKS, not negative full gains or LR polynomials.

The p=2,a=b=1 realization J7/J8 has block -1/3024 (multiplicity six), while its full gain c2 is 324781/277200>0. J56 also has an ENTIRE pair-(2,3) sum -1/110 although its whole gain is positive. The balanced J1/J2 positive-rest-occupation subtotal is negative. These are exact architectural exclusions, not evidence against unrestricted KTT.

## Scope of the remaining result

The operator and obstruction are uniform theorems at the accepted scope. The general complete G2>=0 inequality remains OPEN. Exact selected whole endpoint/segment checks are computational evidence at their stated parent margins and scaling rays. No larger positive panel, universal concavity law, all-three-row c2 theorem, whole rank-seven result or unrestricted theorem is inferred. A negative whole gain would refute the sufficient splitting induction; only a negative coefficient of a complete original triggers the independent bare-triple candidate protocol.

## Complete split-ratio curves and the next sufficient theorem

Fix the complete integer parent (r;c,d1,...,dm), c>0, and let U(s) be the full sum of F_(n,C,ij)(s) over all rest assignments and pairs, with c replacing a+b. Then


```text
G(s)=U(s)+U(c-s)-U(0)-U(c),  0<=s<=c.
```

It is continuous, symmetric about c/2 and piecewise quadratic, with G(0)=G(c)=0. The complete breakpoint roster is obtained from x=0, y=0 and x=y for every assignment/pair and its reflection s -> c-s. For integer parent margins every nonconstant such form has slope +1 or -1, so every breakpoint is an integer; constant zero forms retain the original offsets. No numerical knot discovery is used. For rational s, choose any positive integer ell clearing its denominator and scale ALL parent margins by ell. The computed G(s) times ell^2 is the ordinary quadratic gain of that complete integer original. This is homogeneity of the exact coefficient operator; no rational-polytope quasipolynomial or residue is substituted.

A proof that G is concave for every legal parent would therefore prove the universal splitting gain. In exact terms it suffices that each complete interval's quadratic coefficient is nonpositive and every complete derivative jump is nonpositive. This is a new sufficient conjecture about the whole aggregated operator, not the signed individual blocks ruled out by (4). Concavity is stronger than nonnegativity: a future positive interval curvature or upward jump must be tested against the weaker full G itself before retiring splitting.

The complete selected calculations in verification/evidence/structural-checks-v3.json certify this concavity and G>=0 for five full parent-margin scaling families J1, J2, J34, J56 and J78. Their twelve quadratic intervals have three determining and two genuinely unused values each, exact derivatives at all seven interior knots and exact endpoint/stationary-point minima. The independently checked complete integer endpoint gains are 6865065131882772952621469/3175487602017397958491200, 47649840682511135512743681917213658539699073661385/21796094719709170671032715461689097922319213735296, 34817/33264, 238796/51975 and 324781/277200 respectively. These five full curves do not prove the universal sufficient conjecture.
