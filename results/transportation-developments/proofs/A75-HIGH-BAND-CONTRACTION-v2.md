# A75: complete high-band payment by unequal free-slot contractions

Curated mathematical proof from **A75**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation. This completes the uniform high-band bridge left in the initial ONE-PAIR-REDUCTION.md draft; the final combined statement is ONE-PAIR-REDUCTION-v2.md. Both notes, the complete accepted A73/A74 premises and exact verification are. No active Pro052 source is used. Every quantity is a whole polynomial or a complete explicitly defined auxiliary count; returned code remains inert.

## 1. The complete unequal-slot object

For integers n>=m>=2 and an integer x>=0, take two labeled columns with first-two-row entries (a_i,b_i), a_i,b_i>=0 and a_i+b_i<=x. Require a_1+a_2<=x. Keep n-1 independent uncapped slots for the remaining first row and m-1 independent uncapped slots for the second row, with original totals x and 2x. The entire weighted count is


```text
W_(n,m)(x)=sum a_(n-2)(x-a_1-a_2)
                    a_(m-2)(2x-b_1-b_2),           (1)
```

over exactly those four entries. The second-row residual is automatically nonnegative because b_1+b_2<=2x. Neither labeled small column, either row bound nor any allocation multiplicity is omitted. This auxiliary count is not asserted to be a new LR original.

Without the two column caps the entire count is a_n(x)a_m(2x). One violation keeps its first-row bound I<=x and its strict +1. Complete rising addition and Vandermonde convolution give


```text
V_(n,m)(x)=sum_(l=0)^(m-1) d_l(x)d_(n+m-l)(x)
                     +d_m(x)a_n(x).                (2)
```

Indeed the literal single-violation sum is
sum_(I=0)^x binom(I+n-1,n-1)binom(2x-I+m-1,m).
Expand the second factor as sum_l d_l(x)d_(m-l)(x-I). The full convolution is d_(n+m-l)(x) when l<m; the last constant factor instead gives a_n(x). The terminal a_n is essential.

Both columns violate exactly when their two remaining row totals I,J satisfy I+J<=x-2. Summing their two positive overshoots and all distributions leaves the exact double intersection


```text
J_(n,m)(x)=(x+1)binom(x+L-3,L-1)
                       -(n-1)binom(x+L-3,L),
L=n+m.
```

The -2 is the original pair of strict shifts. All upper entries are nonnegative at integer x>=0. Thus falling-product binomials give zero on every empty initial grade and the identity is all-grade. Equivalently


```text
J_(n,m)=x(x-1)a_(L-3)(x)/D [(m+1)x+3n+m-2],
D=L(L-1)(L-2).                                     (3)
```

For example, Newton expansion of x-I+1 in the full I,J/overshoot convolution yields the first expression directly. The ENTIRE auxiliary polynomial is


```text
W_(n,m)=a_n(x)a_m(2x)-2V_(n,m)(x)+J_(n,m)(x).        (4)
```

This is inclusion-exclusion with both singletons and their complete intersection. It is not an exact-violation sector and does not discard negative ordinary coefficients of J.

## 2. Uniform coefficientwise payment

Rising addition in a_m(2x) transforms (4) into


```text
W_(n,m)=sum_(l=0)^(m-1) d_l(x)
             [a_n(x)a_(m-l)(x)-2d_(L-l)(x)]
               -d_m(x)a_n(x)+J_(n,m)(x).           (5)
```

Every bracket with m-l>=1 is coefficientwise nonnegative by the complete sorted-denominator bound


```text
a_p a_q-2d_(p+q)>=a_(p+q-1)[1+(1-2/(p+q))x].
```

Combine the last l=m-1 term with the negative terminal term. Their exact sum is


```text
R=d_(m-1)(x)a_n(x)[1/m+lambda x],
lambda=1-2/(n+1)-1/m>=0.                           (6)
```

For m>=3 this lambda is at least 1/6; for m=2 and n>=3 it is (n-3)/(2(n+1)). These are the entire domain, including the lambda=0 boundary.

The product a_(m-2)(x)a_n(x) dominates a_(L-2)(x) by sorting its denominator list, including m=2 where a_0=1. Therefore


```text
R>=x a_(L-3)(x)/(m-1)
                      (1+x/(L-2))(1/m+lambda x).   (7)
```

From the complete (3), discarding only explicitly nonnegative terms gives


```text
J_(n,m)>=-x a_(L-3)(x)[(m+1)x+3n+m-2]/D.            (8)
```

Subtract (8)'s adverse bracket from (7). Its constant is positive because


```text
(3n+m-2)/D<=3/[L(L-1)]<1/[m(m-1)],
```

using m>=2 and L>=2m. Its linear coefficient is nonnegative: if m>=3, lambda/(m-1)>=1/[6(m-1)] exceeds (m+1)/D, since D>=2m(2m-1)(2m-2) and 4m(2m-1)>6(m+1). If m=2, the extra product term 1/[2(L-2)]=1/(2n) already exceeds 3/D for n>=3. Its quadratic coefficient lambda/[(m-1)(L-2)] is nonnegative. All multiplied factors are nonnegative ordinary polynomials. Hence R+J>=0, with strict positive constant in the residual bracket.

The remaining l=0 term is still present (m>=2). Consequently


```text
W_(n,m)>=a_n(x)a_m(x)-2d_L(x)
         >=a_(L-1)(x)[1+(1-2/L)x],                 (9)
```

strictly positive in every degree 0..L for x>0. This is a proof for arbitrary n>=m>=2,n>=3. Finite checks corroborate the derivation but supply no unbounded quantifier. The excluded (2,2) is never used below; its whole auxiliary count is separately a_2(x)^2-d_4(x).

## 3. Restore the ENTIRE canonical high-band original

Use ONE-PAIR-REDUCTION's original S_n with small columns A,A, other n-1 columns B=A+H, and rows A,B,A+(n-2)B. For H>=A put z=(H-A)t>=0 and x=At, so B t=2x+z. Impose both small-column caps first, leaving the n-1 wide columns temporarily uncapped. In every such small-column allocation, the remaining second-row margin is z+2x-b_1-b_2 with 2x-b_1-b_2>=0. Complete rising addition gives


```text
a_(n-2)(z+w)=sum_(l=0)^(n-2) d_l(z)a_(n-2-l)(w),
w=2x-b_1-b_2.
```

Thus the ENTIRE small-column-constrained core is
sum_(l=0)^(n-2) d_l(z) W_(n,n-l)(x).
Each still-uncapped wide-column violation has complete height A and polynomial d_(2n)(x). It is disjoint from either small-column violation and from every other wide-column violation: small+wide widths sum to A+B exactly, while wide+wide widths are at least A+B. Their original strict +1 shifts make equality disjoint. Therefore every wide violation remains wholly within the core. Subtract ALL n-1 of them exactly once.

At z=0 the resulting original is S_n(x,x). Hence the exact all-grade ORIGINAL identity is


```text
S_n(x,x+z)=S_n(x,x)
              +sum_(l=1)^(n-2) d_l(z) W_(n,n-l)(x). (10)
```

For n=2 the sum is empty and the complete high-band original is constant in z; its rows include the actual repeated small row A. For n>=3 each displayed W has n>=m=n-l>=2 and n>=3, exactly the domain of (9). Every additional term is paid. At z=0 all d_l(0)=0 and the two complete bands join without a boundary correction.

The low-band proof already gives S_n(x,x)>=K_n(x). Thus (10) proves


```text
S_n(At,Ht)>=K_n(At)
   >=a_(2n-1)(At)[1+(n-1)At/(2n)]                  (11)
```

for EVERY H>=A and n>=2. The right side is strict through degree 2n. Together with the uniform low-band proof and the complete profile reduction, this signs every original in the one-overlapping-pair family at arbitrary positive-column count, in both height bands. All legal original/lattice/degree/label/zero-column and strict-shift conventions from the first note remain operative.

## 4. Exact ceiling and next mechanism

This proves a sufficient original-family theorem: 0<A<=B, every positive column>=A, and at most one pair with sum<A+B. The zero-overlap case is the accepted A73/A74 theorem; the exactly-one case is the new result. It does not establish arbitrary split-gain positivity, multiple overlapping pairs, an overlapping selected column below A, arbitrary three-letter LR shapes, whole rank seven or unrestricted KTT.

The next minimal unresolved incidence has two overlaps sharing the smallest column, with the other pair nonoverlapping; its complete polynomial has both pair corrections and no triple. A common extremal-profile payment or a paid original-generating operation must keep both corrections jointly. Three mutually overlapping caps also require the full triple when supported. These are proposed successor questions, not A75 execution scope.

The frozen n<=12 cone coefficient arrays remain useful stronger formal positivity evidence for those specific parameter expansions, but the ordinary all-n theorem is supplied by the finite identities and product bounds above, not extrapolation. All derivative/auxiliary/count scopes, earlier failures and historical debts survive. No public or formal-certification claim is made.
