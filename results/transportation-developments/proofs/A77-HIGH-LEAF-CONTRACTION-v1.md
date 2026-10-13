# A77 draft: full high-band leaf contraction and boundary derivative jump

Curated mathematical proof from **A77**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation from the complete A73/A74 formulas, with no new active-provider premise.. This signs the complete auxiliary leaf correction's derivatives on H>=A; it is not by itself a full-star positivity theorem.

## Complete count and rising expansion

Set x=At,h=Ht=x+z, z>=0, n>=2. The full count of a specified leaf violation while the central width A remains imposed is


```text
W_n(x,h)=V_n(x,h)-J_(n-1,2)(A,H;t)
   =sum_(a,b>=0,a+b<=x) V_(n-1)(x-a,h-b).           (1)
```

For integral x,h in this band h-b>=0, so the complete V formula applies with both residual row bounds. Its terminal a_(n-1) is retained. This is an exact all-grade count identity: the center has entries a,b, the leaf retains its strict +1, and all n-1 remaining slots and original multiplicities survive.

Rising addition gives W_n(x,x+z)=sum_(j=0)^(n-1)d_j(z) C_(n,j)(x). Every C has a positive product formula. Put s=n-1-j and L=n+s+1=2n-j. For s=0,


```text
C_(n,n-1)=a_n(x)[1+n x/(n+1)].                     (2)
```

For 1<=s<=n-1,


```text
C_(n,j)=a_n(x)d_(s+1)(x)
  +sum_(k=1)^(s-1)d_(L-k-1)(x)d_(k+1)(x)
  +d_(L-2)(x)/[L(L-1)]
     [n x^2+(L^2-3L+3s+3)x+L^2-2s-2].             (3)
```

Every factor and bracket coefficient is nonnegative (indeed the numeric brackets are positive) for n>=2 and these indices. Empty sums and d_0 are literal.

## Derivation of every triangle term

Change I=x-a,J=x-b, so 0<=I,J<=x and I+J>=x. For r,k>=1 the full triangle sum of d_r(I)d_k(J) is d_(r+1)(x)d_(k+1)(x)-d_(r+k+2)(x-2), by the generating series sum_I d_r(I)t^I=t/(1-t)^(r+1). For k=0 it is 2d_(r+1)(x)+(r+1)d_(r+2)(x-1). The terminal a_(n-1)(I)d_s(J), s>=1, contributes a_n(x)d_(s+1)(x)-d_(n+s+1)(x-1). For s=0 its full triangle sum is sum_(I=0)^x(I+1)a_(n-1)(I), giving (2).

In the nonterminal sum r=n-1+s-k, so every adverse shifted polynomial has the same L. Collecting ALL of them gives

    2d_(L-1)+(L-2)d_L(x-1)-(s-1)d_L(x-2).

Substitute d_L(x-1)=(x-1)d_(L-1)(x)/L and d_L(x-2)=(x-2)(x-1)d_(L-2)(x)/[L(L-1)], with d_(L-1)=(x+L-2)d_(L-2)/(L-1). The resulting bracket is exactly (3). The shifted polynomials are algebraic terms in the complete finite identity, not counts on negative margins. Integer-grade equality proves the polynomial identity; no fit is a premise.

## High-band monotonicity, convexity and the full jump

The full correction g_n= W_n-V_n(x,0) has the same first and second fixed-x derivatives as W_n. Equations (2)-(3) and positive-coefficient d_j(z) prove all ordinary coefficients of both derivatives nonnegative on z>=0, for arbitrary n. Fixed-row numerical H differentiation adds only positive powers of t and preserves signs.

The complete high-minus-low J tail T vanishes at h=x. Its first derivative there has the exact negative polynomial


```text
-partial_h T(x,x)
  =sum_(j=0)^(n-2)(j+1) a_(n-2-j)(x) B(n-1+j,4)>=0, (4)
```

where B(p,4)=(p-1)! 3!/(p+3)!. This is the derivative jump of g. To derive it retain every original high-tail summand: its delta-linear coefficient is (-1)^(l+3)B(n-1,l+4). The remaining signed sum inside the beta integral is


```text
sum_l (-1)^l(l+1)binom(n+x,n-2-l)(1-u)^l
  =sum_(j=0)^(n-2)(j+1)u^j a_(n-2-j)(x).
```

Coefficient extraction from (1+v)^(n+x)/(1+(1-u)v)^2 proves the transformation. Integrate u^(n-2)(1-u)^3; all terms are finite and integrable. Thus full boundary continuity and a nonnegative derivative jump are established for every n, not extrapolated from A76's finite arrays.

Low-band curvature and full high-band equal-star reserve remain independent obligations. Both row bounds, the terminal, all tail summands and the original strict shifts remain. No new original/candidate/coverage or general KTT claim follows from this auxiliary result.
