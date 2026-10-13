# A74: the complete pair-sum primitive family and a second paid operation

Curated mathematical proof from **A74**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Independent reconstruction of completed Pro051 U11. Exact originating proof: SHA-256 1b9d98f438b8cd320ad025b06c7ea5e71b109c6411d0b3d871c16269ad4c41fd; U12 consolidation 2f41dbef57f4126ec0a51ba83253efaf008e377881bb6e9cc507a08c4d2076f7. Provider facts retain SOURCE; these independently checked root claims retain source provenance. No returned program is executed. This note and its source-derived checks are excluded from active Pro052.

## 1. Entire originals and theorem

Use specified rows (A,B,R), 0<=A<=B, and labeled nonnegative columns e with total M=A+B+R. Let N be the positive-column count. Keep physical zeros in the A65 suffix-sum buffered lambda-outer constructor and inverse. Its integral table correspondence, saturated upper-left chart, total unimodularity and strict table r_i e_j/M prove actual degree (p-1)(N-1) before reconstruction. M=0, one active row and N<=1 are points. Equal row or column parameters are not a quotient of the labeled lattice.

Assume ONLY that every pair of distinct positive columns satisfies


```text
e_i+e_j >= A+B.                                         (H)
```

Then the ENTIRE polynomial is strictly positive in every ordinary coefficient through its actual degree. For N>=3 and A>0 put n=N-1 and w0=min(A,min_positive e_j). The quantitative complete bound is


```text
P_e(t) >=_coef a_(2n-1)(w0 t)[1+(n-1)w0 t/(2n)],
a_n(x)=prod_(j=1)^n(1+x/j), d_n(x)=x a_(n-1)(x)/n,
a_0=d_0=1.                                             (1)
```

Summing (H) over all pairs forces M>=N(A+B)/2, so R>0 here and the degree is exactly 2n. Selecting the smallest two table rows for the test is an explicit permutation bijection with inverse; it never silently sorts an affine LR output. The equal first two inner parts obstruct positive subtraction in the accepted sigma direction, so these are actual primitive starting originals.

If every e_j>=A, A73 PRIMITIVE-ADOPTION sections 4-5 already prove (1), including C=B-A=0, rational comparison polynomials, the complete terminal a_n in V, the common coefficientwise mixture and all zero-degree boundaries. Retain that full accepted argument, not only its theorem label. A74 removes the remaining individual-width condition as follows.

## 2. The complete unique-small-column contraction

A positive w<A is unique under (H), and every other positive e_j>=A+B-w>B. Put x=wt, alpha=(A-w)t, beta=(B-w)t. Impose this column's FULL triangle first in the uncapped first-two-row composition model. Its count is


```text
W_n=sum_(a,b>=0,a+b<=x)
        a_(n-1)(x+alpha-a)a_(n-1)(x+beta-b).             (2)
```

Both remaining-row arguments are nonnegative. Rising addition in BOTH factors gives


```text
W_n=sum_(i,j=0)^(n-1) d_i(alpha)d_j(beta)
                            F_(n-i,n-j)(x),
F_(p,q)=a_p a_q-d_(p+q), p,q>=1.                        (3)
```

To derive each coefficient in this contraction, change I=x-a,J=x-b in the full rectangle 0<=I,J<=x. The excluded triangle is I+J<=x-1, whose complete Vandermonde sum is d_(p+q)(x). The strict -1, every boundary row of the double sum, and the unique (n-1,n-1) corner are retained. This proves (3) at every nonnegative integer x and hence the displayed polynomial identity. It is not positivity inferred from count values.

A73's sorted denominator comparison gives


```text
F_(p,q)(x)>=_coef a_(p+q-1)(x)[1+(p+q-1)x/(p+q)],
K_n(x):=a_n(x)^2-(n+1)d_(2n)(x)
       >=_coef a_(2n-1)(x)[1+(n-1)x/(2n)].              (4)
```

Hypothesis (H) forbids ALL simultaneous column violations, with the original strict +1 shifts, including those involving w. Thus imposing each remaining cap removes its entire disjoint violation d_(2n)(h_j t), where h_j=(A+B-e_j)_+<=w, already counted inside (2). The ENTIRE original is


```text
P_e=W_n-sum_(j != small)d_(2n)(h_j t).                 (5)
```

There are exactly n adverse terms. The (i,j)=(0,0) term in (3) minus their upper bounds is K_n(x). Every other term of (3), and every height-improvement d_(2n)(x)-d_(2n)(h_jt), is coefficientwise nonnegative. Equations (3)-(5) prove (1).

## 3. Full actual-degree boundaries

For A=0, (H) lies in the accepted A73 two-row case, with strict positivity through degree N-1 when both other rows are positive. A=B=0 is a point. For N=2 and w<A, let h=(w-R)_+. Formula (5) is exactly


```text
P=1+(3w-h)t/2+(w^2-h^2)t^2/2.
```

For R>0, h<w and the actual degree is two, with strict coefficients. For R=0, h=w and the segment is 1+wt. N=2 with both columns>=A keeps A73's complete polynomial and actual area/segment/point alternatives. N<=1 and zero total are points. Pair equality has no simultaneous violation because two strict shifts still require +2. Zero physical columns are forced zeros, not free composition variables.

## 4. Pay a whole operation, retaining every old cap

Keep w fixed, 0<w<A, and split a wide remainder c into a,b>=T=A+B-w, with every other positive column also >=T. Let m>=1 count the old columns INCLUDING w. Parent n=m, child n=m+1. The entire difference is paid, independently of endpoint positivity.

First F_(p+1,q+1)-F_(p,q) is coefficientwise positive in every nonconstant degree. Write L=p+q>=2, Q=a_(L-1), D0=(p+1)(q+1). The exact adverse difference is


```text
d_(L+2)-d_L=x Q[x^2+(2L+1)x-2(L+1)]/[L(L+1)(L+2)].
```

The complete positive product increment is


```text
a_p a_q * x[L+2+x]/D0 >= x(1+x)Q[L+2+x]/D0.
```

The remaining bracket has strictly positive constant, linear and quadratic coefficients: 1/D0>=L/[L(L+1)(L+2)], so its latter two lower numerators are L^2+L-1 and L-1, and its constant is positive. This proves the required simultaneous-index monotonicity without a sector-sign assumption.

Let E_n be (3) with only (0,0) removed. Every old term of E increases by this full F difference; new terms on both boundary rows are nonnegative and their shared corner is counted once. Hence E_(m+1)-E_m>=_coef0. Rewrite (5) as a_n(x)^2 minus its distinguished cap d_(2n)(x) and every ordinary wide cap, plus E_n. The merged cap vanishes since c>=2T>A+B. Every old and both new cap heights are <=w. Applying the exact A73 complete adverse-cap bound yields


```text
G >=_coef x a_(2m-1)(x)/[2(m+1)]
    [2+(4+2/(m+1)-b_m)x+(2/(m+1)-a_m)x^2],
a_m=(m+2)/[2m(2m+1)], b_m=(4m+1)a_m.                  (6)
```

This bounds all m old cap differences, including the distinguished small cap, and both new caps. Since b_m<=5/2 and the last coefficient is (7m^2+m-2)/[2m(m+1)(2m+1)]>0, the gain is strict in all degrees 1..2m+2, the child's actual degree, and has constant zero.

Merge wide columns repeatedly to the complete two-column base (w,M-w), whose second width T+R is >=T. The base above is paid; each reverse split obeys the same hypotheses, and the wide-column count decreases under merging. Restore all original labels and physical zeros by the explicit bijection. This is a terminating whole-original construction with paid bases and gains. It is SEPARATE from A73's all-wide operation and does not prove arbitrary pair-sum-preserving or small-column-changing gains.

## 5. Verification, provenance and remaining question

A74 independently evaluates every full W contraction on its frozen integer domain, verifies the complete F increments and all-grade new intersection formulas, and compares both full operation endpoints with the accepted complete character kernel and independent direct-table/bare-LR engines. Original degrees and all unused grades are retained. Formal finite tests do not establish the unbounded quantifiers supplied by (2)-(6).

Outside (H), several caps can violate simultaneously. COMPLETE-INTERSECTIONS.md supplies the full correction for all orders when selected widths>=A, including the H>A row-bound tail absent from U12. Their inclusion-signed c1 is uniformly adverse. This does not refute KTT, and it prevents treating the new intersections as automatic positive reserve. The complete first-pair polynomial, arbitrary below-A overlaps, general coefficientwise operation, all higher transportation signs, whole rank seven and unrestricted KTT remain open. No public, novelty, external human review or formal certification claim is made.
