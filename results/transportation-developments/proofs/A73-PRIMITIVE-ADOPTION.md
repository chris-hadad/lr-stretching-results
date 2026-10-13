# A73: complete primitive bases and an all-coefficient splitting operation

Curated mathematical proof from **A73**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Independent root reconstruction of selected Pro051 U08 and U10 SOURCE. Provenance remains Pro051:
U08 proof SHA256 71f28e67e2d463cb51c1b9edc12fe7ffc0964f1c58f573b848005b90d2b13489;
U10 proof SHA256 516becb39444e127d8cfb4ed6d630c00bad55a7c4163569292f68510553c4728.
No provider program was imported or executed. This note, its claims and its
source-derived numerical fixtures are excluded from Pro052 supplements even
after adoption. The two results have different domains; base positivity never
signs a difference by itself.

## 1. Whole originals, exact lattice and prior degree

Fix specified rows (A,B,R), 0<=A<=B, and labeled nonnegative columns e_j with
sum e_j=A+B+R. Let N be the positive-column count. Keep all physical zeros in
the literal record. For total M>0, the active table r_i e_j/M is strictly
positive, its upper-left (p-1)(N-1) entries give an integral free chart, and
the bipartite incidence matrix is totally unimodular. Thus the actual
polynomial degree is (p-1)(N-1), proved before any reconstruction. Total zero,
one active row and one positive column give a point.

The whole A65 LR constructor is lambda=(M+B+R,M+R,C_1,...,C_l),
mu=(M,M,C_2,...,C_l), nu=(M,B+R,R), with physical suffix sums C_j and
lambda outer. A trailing zero in mu may be retained literally. The first two
skew rows force ones and twos, and the remaining row intervals are disjoint
table columns; their sorted multiplicities and the buffer ballot reserves
give the complete integral bijection and inverse. Empty physical lists use
the two zero buffer rows without inventing a column tail. This is a count and
integer-coordinate correspondence, not an identification of hive metrics.

The inner partition has mu_1=mu_2. Subtracting any positive multiple q of
the established sigma direction would leave M-2q<M-q, violating its order.
These are actual primitive starting originals. Table-row permutation is an
explicit bijection if a different specified pair is chosen; affine LR output
partitions are never silently sorted.

For polynomial comparisons write


```text
a_n(x)=product_(i=1)^n(1+x/i),
d_n(x)=x a_(n-1)(x)/n (n>=1),  d_0=a_0=1.
```

All comparisons are in ordinary monomial coefficients. Arguments such as
x=At, y=Ct/2 are numerical rational multiples of the SAME formal t. A rational
comparison polynomial is not a new lattice or a half-grade tableau count.

## 2. A complete bounded violation, including the terminal order

For N>=2 put n=N-1. Ignoring every column cap gives a_n(At)a_n(Bt).
Suppose e>=A is a specified column. If e>=B its full violation polynomial
is d_(2n)(ht), h=(A+B-e)_+<=A. If A<=e<B put delta=B-e and x=At,y=delta t.
The remaining two row totals I,J satisfy


```text
0<=I<=x, 0<=J<=Bt, I+J<=x+y-1.
```

The J bound is redundant because A+delta<=B; the I bound is essential.
Complete Vandermonde summation in J gives the entire violation


```text
V_n(x,y)=sum_(I=0)^x binom(I+n-1,n-1)
                              binom(x+y-I+n-1,n)
        =sum_(l=0)^(n-1) d_l(y)d_(2n-l)(x)+d_n(y)a_n(x). (1)
```

For an independent algebraic derivation, use the rising addition identity
binom(z+y+n-1,n)=sum_(l=0)^n d_l(y)d_(n-l)(z) with z=x-I.
For l<n the full convolution is d_(2n-l)(x). For l=n the remaining
d_0 is one and the complete sum is a_n(x). This explicitly explains the
last a_n rather than incorrectly continuing d_n. At y=0 (1) is d_(2n)(x).
The formula holds at every nonnegative integer x,y, including zero; it is
not interpolation of an incomplete region. Its coefficients in x,y are
nonnegative, so each fixed t coefficient of V_n(At,delta t) is a convex,
nondecreasing function of delta>=0.

## 3. A complete all-coefficient operation beyond one constrained row

First impose every positive column e_j>=B. Then any two violations would
use at least (e_i+e_j)t+2>(A+B)t entries, so no pair exists at any grade,
including equality. All residual row bounds in a single violation are
automatic. The ENTIRE polynomial is therefore


```text
P_e=a_n(At)a_n(Bt)-sum_j d_(2n)((A+B-e_j)_+ t).         (2)
```

For n>=2 and A>0 let Q_n(x)=a_(2n-1)(x). The sorted denominator list of
a_n(x)^2/(1+x) is termwise at most 1,2,...,2n-1. Hence
a_n(x)^2>=(1+x)Q_n(x) coefficientwise. Every cap height is <=A, giving


```text
P_e >= Q_n(At)[1+(n-1)At/(2n)],                      (3)
```

strictly positive through its actual degree 2n. The zero and N<=2 cases
are treated below, not assigned this generic degree.

Now keep m>=1 positive old columns d_j>=B and split c=a+b with a,b>=B.
The same rows have R=D+a+b-A-B; both endpoints are complete originals in
(2). The parent merged cap is zero because c>=A+B. The exact WHOLE gain is


```text
G=U-sum_old [d_(2m+2)(h_jt)-d_(2m)(h_jt)]
                  -d_(2m+2)(h_at)-d_(2m+2)(h_bt),      (4)
```

where h_j=(A+B-d_j)_+, h_a=(A+B-a)_+, h_b=(A+B-b)_+, and


```text
U=a_m(At)a_m(Bt)[(A+B)t/(m+1)+ABt^2/(m+1)^2].
```

No positive endpoint inference has entered (4). Put x=At, Q=a_(2m-1)(x)
and L=(2m+2)(2m+1). Since B>=A,


```text
U >= 2x(1+x)Q(1+x/(2m+2))/(m+1).
```

The complete adverse old-cap difference is


```text
Delta_m(x)=d_(2m+2)(x)-d_(2m)(x)
  =xQ[x^2+(4m+1)x]/(2mL)-xQ/[2m(m+1)].              (5)
```

Call the first nonnegative polynomial R_m(x). For 0<=h<=A the slack
R_m(At)-Delta_m(ht)=R_m(At)-R_m(ht)+ht Q(ht)/[2m(m+1)]
is coefficientwise nonnegative. This justifies the upper bound while retaining
the adverse negative term in the exact identity. Bound all m old caps and
both new caps in (4) in this manner. Their COMPLETE total upper bound is


```text
xQ/[2(m+1)] [2+b_m x+a_m x^2],
b_m=(m+2)(4m+1)/[2m(2m+1)], a_m=(m+2)/[2m(2m+1)].
```

Subtracting from U yields


```text
G >= xQ/[2(m+1)]
         [2+(4+2/(m+1)-b_m)x+(2/(m+1)-a_m)x^2].     (6)
```

Here b_m<=5/2 for m>=1 and
2/(m+1)-a_m=(7m^2+m-2)/[2m(m+1)(2m+1)]>0. With A>0 the bound is
strict in EVERY degree 1..2m+2, the child's actual degree; its constant is
zero. If A=0<B, all caps vanish and G=Bt a_m(Bt)/(m+1), strict in
degrees 1..m+1. If A=B=0, both counts are one. A zero split is the identical
original, and m=0 is the point-parent/two-column formula below.

Merging any two positive columns preserves the wide-column class and strictly
decreases their count, so the reverse construction terminates at one column.
Every intermediate object has the same original row margins and saturated
lattice. This is a terminating complete-original recurrence with paid bases
and paid gains. When m>=2 and A,B>0, both small rows can lie below D; its
reach is therefore genuinely beyond the former one-constrained-row result.
Its width hypothesis remains essential; it is not arbitrary two-row-deficit
splitting.

## 4. A broader primitive-base theorem under pairwise shortfalls

Retain 0<=A<=B and let C=B-A, delta_j=(B-e_j)_+ over positive columns,
padding with zero if necessary. Assume

    the largest two delta_j sum to at most C.             (H)

For N>=2 this is equivalent to every positive e_j>=A and every pair of
positive columns satisfying e_i+e_j>=A+B. Thus there is again no double
COLUMN violation, even though multiple ROW-admission violations may exist.
The total sum of shortfalls can be arbitrarily large. Define
h_j=min(A,(A+B-e_j)_+). With (1), the entire original is exactly


```text
P_e=a_n(At)a_n(Bt)-sum_j V_n(At,delta_jt)
                 +sum_j[d_(2n)(At)-d_(2n)(h_jt)].     (7)
```

The final height-improvement sum is coefficientwise nonnegative.

If C>0 put q=max delta_j and theta=max(0,2q/C-1). For each coefficient
functional f of V, convexity and monotonicity give the SAME comparison


```text
sum_j f(delta_j)
   <=theta[f(C)+n f(0)]+(1-theta)(n+1)f(C/2).         (8)
```

If q<=C/2 this is monotonicity. Otherwise all other shortfalls are <=C-q,
and f(q)+n f(C-q) is convex in q on [C/2,C]; its chord proves (8).
The numerical theta is common to every coefficient, preserving one complete
polynomial comparison. At C=0 every shortfall is zero and no division occurs.

It remains to pay the two entire endpoint polynomials. Set x=At, z=Ct and
K_n(x)=a_n(x)^2-(n+1)d_(2n)(x). Rising addition in (1) gives


```text
Q_one=a_n(x)a_n(x+z)-V_n(x,z)-n d_(2n)(x)
     =K_n(x)+sum_(l=1)^(n-1)d_l(z)
                     [a_n(x)a_(n-l)(x)-d_(2n-l)(x)]. (9)
```

For n,k>=1, the sorted denominator list of a_n a_k/(1+x) is bounded
termwise by 1,...,n+k-1. With J=n+k this proves


```text
a_n a_k-d_J >= a_(J-1)[1+(J-1)x/J] >=0.              (10)
```

Every term after K_n in (9) is paid. For the half endpoint put y=z/2 and


```text
R_(n,k)=a_n a_k-a_n-(n+1)d_(n+k),
B_n(y)=a_n(2y)-(n+1)d_n(y),
Phi_n(x,y)=a_n(x+2y)-a_n(x+y)-a_n(2y)+a_n(y).
```

The same full product bound gives


```text
R_(n,k)>=[a_(n+k-1)-a_n]
                     +(k-1)x a_(n+k-1)/(n+k)>=0
```

for k>=1; at k=1 the exact slack is zero. The sorted slopes
2,2/2,...,2/n give a_n(2y)>=(1+2y)a_(n-1)(y), hence


```text
B_n(y)>=a_(n-1)(y)[1+(n-1)y/n]>=1.
```

Phi has nonnegative coefficients because its pure terms cancel and every
mixed monomial x^i y^j is multiplied by 2^j-1 for i,j>=1. Complete
substitution of (1), retaining its terminal d_n(y)a_n(x), gives the identity


```text
Q_half=a_n(x)a_n(x+2y)-(n+1)V_n(x,y)
   =K_n(x)+a_n(x)[B_n(y)-1]+a_n(x)Phi_n(x,y)
                      +sum_(l=1)^(n-1)d_l(y)R_(n,n-l)(x). (11)
```

All terms after K_n are nonnegative. Equations (7)-(11) therefore prove


```text
P_e>=theta Q_one+(1-theta)Q_half>=K_n(At)
   >=a_(2n-1)(At)[1+(n-1)At/(2n)].                   (12)
```

For N>=3 and A>0, pairwise widths imply R>0, so the actual degree is
2n. The last bound is strictly positive in every degree 0..2n. This is
whole-original positivity across arbitrary column count, with a signed
primitive base and quantitative reserve. It supplies NO new gain theorem
for changing a narrow column. Equation (6) keeps its own stronger width
hypothesis.

## 5. All collapsed cases and exact adoption ceiling

For A=0<B and N>=3, (7) reduces to
P=a_n(Bt)-sum_j d_n(delta_jt). The same two-profile comparison dominates
a_(n-1)(Bt/2), paying every degree 0..n-1. The active integral polytope
has positive volume and actual degree n because R>0, so its leading
coefficient is positive as well. This uses a geometric top-degree fact,
not a zero three-row bound or a numerical fit. If A=B=0 the count is one.

For N=2, n=1, the exact polynomial from (7) has constant one and linear
coefficient


```text
A+B-(h_1+h_2)/2-(delta_1+delta_2)
   >= B-(delta_1+delta_2)>=A.
```

If A>0 the linear term is strict. Any degree-two term is the positive area
when all three rows are positive; otherwise the actual degree drops. For
A=0 it is exactly 1+[B-delta_1-delta_2]t, with the slope strict when the
actual degree is one and zero for a point. N<=1 and zero total are points.
For the wide-column specialization its explicit two-column polynomial is
1+[A+B-(h_1+h_2)/2]t+[AB-(h_1^2+h_2^2)/2]t^2, with these same actual
degree conventions. Thus (6)'s m=0 point-parent case and every equality,
zero width, zero row, equal shortfall and scalar endpoint are accounted for.

ADOPT only after the independent gate: (2)-(6) and their terminating
wide-column operation; (7)-(12) and full strict primitive-base positivity
under (H), including the exact actual-degree boundaries. The source identities
are corroborated by newly authored exact polynomial/convolution checks and
independent full-table/bare-LR replays of the selected literal originals.
The A65 T2 polynomial is reused through an explicit table-row permutation,
not credited as new coverage. Earlier failures and the adverse polynomial
pieces remain evidence against stronger isolated-piece arguments.
