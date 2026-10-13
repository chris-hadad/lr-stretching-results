# A76: a complete overlap-star composition theorem

Curated mathematical proof from **A76**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation recorded before reading either new active provider's scientific return. The premises are accepted A73 complete V/product identities and A75's full one-pair theorem, with Pro051-derived provenance retained. No Pro052 or Pro053 working result is used.  All comparisons concern ordinary coefficients in the SAME t.

## 1. Entire original, graph and height budget

Let integral balanced rows be (A,B,R), with 0<A<=B, and retain every labeled physical nonnegative column. Delete forced zeros only in formulas. There are N=n+1 positive columns, n>=2, each at least A. Choose a minimum column e0=A+alpha. Suppose the overlapping pairs (ei+ej<A+B) form a star with exactly m>=1 leaves; every other pair is nonoverlapping. Put C=B-A and Hi=A+B-e0-ei>0 on its m leaves. Set S=sum Hi. The additional height-budget hypothesis is


```text
S+2 alpha <= C.                                             (1)
```

For exactly two overlaps it is AUTOMATIC: the two leaves are nonoverlapping, so H1+H2+2 alpha<=C. For one overlap it follows from e0<=e1. Thus the theorem covers every original in A76's scheduled exactly-two-pair domain and more generally any number of star overlaps meeting (1). If m=0 use the accepted no-overlap theorem.

The largest leaf height is at most S; every nonleaf has e>=B-alpha and shortfall delta=(B-e)_+<=alpha. The central and leaf shortfalls are C-alpha and Hi+alpha. All are nonnegative. N>=3 is essential for an overlap in a legal original: N=2 would imply R<0. R>0 follows from any nonoverlapping pair plus a third positive column. With m=1 and N>=3, a third column forms a nonoverlapping pair with a leaf; with m>=2, any two leaves do. Hence actual degree is exactly 2n, established before reconstruction.

The literal A65 buffered lambda-outer constructor, inverse integral table map, saturated upper-left chart, total unimodularity and positive rational interior r_i e_j/M remain unchanged. Zero physical columns and labels remain in the original record; rational quantities below are comparison slopes, never fractional table grades. A=0, N<=2 and zero-total objects keep the accepted lower-dimensional conventions and are not assigned this theorem's generic degree.

Every triple contains a nonoverlapping pair, whose two strict +1 violations are impossible even at equality. Therefore no higher intersection is supported. Each of the m pair intersections is the ENTIRE A74 J_(n-1,2)(A,Hi;t), with its own H<=A or H>A band and full first-row tail. No relation among the height bands is assumed.

## 2. Common convex profile for the complete original

Write x=At, U(z)=a_n(x)a_n(x+z), V(z)=V_n(x,z), F(z)=U(z)-V(z), and V0=V(0)=d_(2n)(x). The full polynomial is


```text
P=U(Ct)-V((C-alpha)t)-sum_i V((Hi+alpha)t)
       -sum_nonleaf V(delta_j t)+sum_i J(Hi)
       +sum_nonleaf [d_(2n)(x)-d_(2n)(h_j t)],        (2)
```

where h_j=min(A,(A+B-e_j)_+). Central and leaf heights in their singleton corrections are A, so no improvement was omitted for them. The n-m nonleaf improvements are nonnegative.

For each ordinary coefficient V is nondecreasing and convex in its nonnegative numerical slope. Bound every nonleaf delta by alpha, and apply the convex chord to


```text
V((C-alpha)t)+sum_i V((Hi+alpha)t)+(n-m)V(alpha t)
```

on 0<=alpha<=(C-S)/2. This produces a COMMON coefficientwise convex combination of two complete lower profiles:


```text
Q0=F(Ct)-sum_i V(Hi t)-(n-m)V0+sum_i J(Hi),
Qh=U(s+2y)-V(s+y)-sum_i V(hi+y)-(n-m)V(y)+sum_i J(Hi),
```

where hi=Hi t, s=sum hi, y=(C-S)t/2. The weights for C>S are 1-2alpha/(C-S) and 2alpha/(C-S). At C=S, (1) forces alpha=0 and no division occurs.

Define the complete canonical polynomial


```text
T_n(x;h1,...,hm)=F(s)-sum_i V(hi)-(n-m)V0+sum_i J(Hi). (3)
```

It is a literal entire transportation/LR original for integer A,Hi: rows (A,A+S,(n-1)A+(n-2)S), columns A; A+S-Hi for each leaf; and n-m copies of A+S. All leaf pairs are nonoverlapping because Hi+Hj<=S. Every central-leaf overlap has height Hi. Its row sum, all N positive columns, actual degree and independent J bands are retained.

Accepted A73 gives nonnegative coefficients in x,z for F(z)-F(0):


```text
F(z)-F(0)=sum_(l=1)^(n-1) d_l(z)
                      [a_n(x)a_(n-l)(x)-d_(2n-l)(x)]. (4)
```

Hence Q0>=T. For Qh-T, all terms with no positive hi power form exactly the complete A73 half-profile Q_half-K_n, already nonnegative. A term with y^j, j>=1, and total height degree r>=1 has, after its positive multinomial factor, coefficient


```text
2^j u_(r+j)-2v_(r+j),  if only one height variable occurs;
2^j u_(r+j)-v_(r+j),   if two or more height variables occur,
```

where uk=[z^k]U and vk=[z^k]V. Equation (4) gives uk-vk>=0 for k>=1, while uk>=0. These displayed coefficients are nonnegative. Terms with y exponent zero cancel. Thus Qh>=T and the complete profile comparison is


```text
P >=_coef T_n.                                            (5)
```

This is a common-weight comparison retaining every singleton and every full pair. Positivity of endpoints alone is never used to sign a gain.

## 3. Joint payment by composition of whole one-pair originals

Let K_n=U(0)-(n+1)V0 and let the ENTIRE A75 one-pair canonical original be


```text
S_n(x,hi)=F(hi)-V(hi)-(n-1)V0+J(Hi).
```

It is paid in both height bands at every n>=2. Direct complete subtraction in (3) yields the exact identity


```text
T_n = sum_i S_n(x,hi)-(m-1)K_n + D_F(h1,...,hm),
D_F = F(sum_i hi)-sum_i F(hi)+(m-1)F(0).              (6)
```

By (4), expand F(z)-F(0)=sum_(k>=1) fk(x) z^k with fk>=0. Then


```text
D_F=sum_(k>=2) fk(x)[(sum_i hi)^k-sum_i hi^k]>=0.      (7)
```

The k=1 contribution is identically zero; every mixed monomial has nonnegative coefficient. Thus A75's whole S_n>=K_n gives


```text
P>=T_n>=K_n>=a_(2n-1)(At)[1+(n-1)At/(2n)].           (8)
```

For A>0 and n>=2 the final polynomial has strictly positive coefficients in every degree 0..2n, the actual degree of the original. This proves an unbounded all-coefficient theorem in column count, margins, overlap count and the independent height bands, subject to (1). The result is not a finite-panel extrapolation.

At m=1, D_F=0 and the argument recovers the full one-pair theorem. At m=2, (1) is automatic, so A76's entire two-overlap domain is closed. At any Hi=0 the zero-height leaf becomes a nonleaf: J(0)=0 and V(0)=V0, so (2)-(7) join exactly to m-1 leaves. C=S, alpha=0, equality of leaf widths, equality of nonoverlapping pair sums, and Hi=A all use the same identities with no invented tail. K_n's n=2 boundary is inherited from the full A75 theorem, including its row permutation. No unsupported triple or below-A extension is made.

## 4. A complete-original obstruction to removing the budget for free

The identity itself explains what the theorem has NOT paid. Take n>=3, A,H>0, rows (A,A+2H,(n-1)A+(2n-5)H), columns A; three copies of A+H; and n-3 copies of A+2H. They are balanced, strictly positive, and give exactly three star overlaps of height H. (Here the row formula follows from the displayed full column sum.) Every leaf-leaf pair sums to A+B exactly and no triple is supported. The budget fails: 3H>2H.

For this entire original P_star, all m=3 corrections still recombine exactly as


```text
P_star = 3 S_n(x,h)-2K_n + E_F,
E_F=F(2h)-3F(h)+2F(0).                              (9)
```

The coefficient of z*t in F at first order is the harmonic number H_(n-1), so


```text
[t]E_F = -H H_(n-1)<0.                              (10)
```

Consequently extending the nonnegative-gluing-remainder assertion beyond (1) is false for an infinite family of complete-original combinations. This does not assert a negative coefficient of P_star; the one-pair reserves may still pay E_F. All three complete pair corrections and both row bounds remain in (9). The next question is to retain and allocate those reserves jointly, or derive a different complete contraction. It is not justified to abandon star positivity or unrestricted KTT from (10).

## 5. Direction and exact ceiling

The theorem replaces separate one- and two-pair payments with a compositional mechanism for an arbitrary overlap count under one explicit budget. The next structural obstruction is the over-budget triangle-free star; three mutually overlapping columns additionally restore a possible triple. Below-A overlaps require the missing selected-column row constraints. These are materially different boundaries.

The full A65 character identity covers arbitrary three-row originals including those boundaries, but its signed occupation sectors already have complete negative controls. A successful general route must group entire sectors or preserve compensating reserves. The present composition provides such an exact whole-object grouping on its stated domain and a quantitative failed remainder outside it. It neither closes arbitrary transportation positivity nor establishes a bridge from transportation originals to every LR shape. Longer content, whole ordinary rank seven and unrestricted KTT remain open. No arbitrary split-gain sign follows.

All source provenance, earlier debts and candidate rules remain. Only a negative ordinary coefficient of an ENTIRE legal original triggers candidate handling. Internal independent model review is not external peer review, formal certification, novelty or publication.
