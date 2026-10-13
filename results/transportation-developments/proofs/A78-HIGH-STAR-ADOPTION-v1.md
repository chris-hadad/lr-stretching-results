# A78: complete high equal-star payment and the arbitrary-count triangle-free theorem

Curated mathematical proof from **A78**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root reconstruction of completed Pro053 U10, originating proof SHA-256
`9eea71ce6034778058220ebfaff34e3127623c3f9495a3226ff83f3b5028cffe`.
The provider facts remain SOURCE. This separate root argument, its complete
checks and the resulting theorem are.
No provider program is imported or run.

## 1. Entire originals, domain and inherited premises

Fix integral balanced rows (A,B,R), specified 0<A<=B, and a physical labeled
list of nonnegative columns e with N positive entries. Assume every positive
e>=A and that the threshold graph e_i+e_j<A+B is triangle-free. Retain the
physical zeros and original order. For N>=3, the nonempty graph argument below
forces R>0; an empty graph retains the accepted A73/A74 theorem and all of its
actual-degree cases. Put n=N-1. The claimed whole-polynomial inequality is


```text
P_e(t)>=K_n(At)>=a_(2n-1)(At)[1+(n-1)At/(2n)],
K_n(x)=a_n(x)^2-(n+1)d_(2n)(x),
a_j(x)=product_(i=1)^j(1+x/i),
d_j(x)=x a_(j-1)(x)/j, a_0=d_0=1.                 (1)
```

Thus every ordinary coefficient is strict through actual degree 2n. There is
no bound on n, the margins, overlap count, individual height or total height.
This is a family of complete LR originals, not a cover of arbitrary LR shapes.

With M=A+B+R and physical suffix sums C_j, the literal lambda-outer original is


```text
lambda=(M+B+R,M+R,C_1,...,C_L),
mu=(M,M,C_2,...,C_L,0), nu=(M,B+R,R).
```

Keep the exact A65/A73 buffer-row/tableau-to-table bijection and inverse:
the first skew row forces B+R ones, the next forces R twos; the remaining
disjoint row intervals encode the three entries of each labeled table column.
Their buffer reserves protect every ballot prefix, including physical zero
intervals. This is an all-grade count correspondence, not a metric statement
about full hives. Positive active margins have the strict rational table
r_i e_j/M. The upper-left 2 by (N-1) integer entries give a saturated index-one
chart; the directed bipartite incidence matrix is totally unimodular. The
dimension and actual degree are therefore 2(N-1), before reconstruction.
Each comparison endpoint retains its own full margins and degree. Rational
comparison slopes are justified by common-denominator clearing and polynomial
rescaling, never by fractional counts or a changed original lattice.

The complete A77 uniform G, full low E, A76 common profile/widening and A75
one-pair theorem are accepted premises at their exact boundaries. Their full
arguments are included in this adoption's dependency set. The new obligation
here is the entire equal star at H>A for every n, with all pairs and tails.

## 2. The complete high star

Its rows are (A,A+2H,(n-1)A+(n-2)H), with columns A and n copies of A+H.
Set x=At, h=Ht=x+z, z>=0. Define


```text
U(w)=a_n(x)a_n(x+w),
V(w)=sum_(l=0)^(n-1)d_l(w)d_(2n-l)(x)+d_n(w)a_n(x),
F(w)=U(w)-V(w), W(x,h)=V(h)-J_n(x,h).
```

The terminal a_n is essential. The full pair is


```text
J_low=(x+1)binom(h+2n-3,2n-1)
                -(n-1)binom(h+2n-3,2n),
J_high=J_low+sum_(l=0)^(n-2)(l+1)
                binom(x+n,n-2-l)binom(h-x+n-2,n+2+l). (2)
```

Every binomial is its full falling-product polynomial, backed by the complete
finite count with I<=x and I+J<=h-2. The two strict shifts, first-row cutoff and
all high-tail summands remain. At h=x the tail vanishes identically. Imposing
the center triangle first leaves W as the full violation of a specified leaf.
Two leaves cannot violate jointly because their widths sum to A+B and the two
strict shifts remain. The exact entire original is consequently


```text
P_equal=F(2h)-nW(x,h).                              (3)
```

This counts each leaf once inside the same constrained center and omits no
supported intersection. It is not a sign assertion for a separate pair term.

## 3. A uniform upper bound for the complete constrained leaf

The accepted A77 finite contraction gives


```text
W(x,x+z)=sum_(j=0)^(n-1)d_j(z) C_(n,j)(x).
```

Let T_n=a_n(x)[1+nx/(n+1)]. The terminal is C_(n,n-1)=T_n.
For k=n-j, 2<=k<=n, and L=n+k, the complete coefficient is


```text
C_(n,n-k)=a_n d_k+sum_(p=2)^(k-1)d_(n+k-p)d_p
   +d_(n+k-2)/[L(L-1)]
            [L^2-2k+(L^2-3L+3k)x+n x^2].          (4)
```

This retains the terminal and both boundaries of the center triangle. In
particular it comes from summing V_(n-1)(x-a,x+z-b) over a,b>=0,a+b<=x,
collecting every adverse shifted d polynomial before simplifying. A77's full
derivation, rather than count-value positivity, supplies the identity.

We prove the ordinary coefficientwise upper bound


```text
C_(n,n-k)<=2T_n d_(k-1), n>=k>=2.                  (5)
```

First derive the exact polynomial quotient c(n,k)=C_(n,n-k)/a_n. For k>=3,
write b_r(n,x)=x/(n+r) product_(i=n+1)^(n+r-1)(1+x/i). Then


```text
c(n,k)=d_k+sum_(p=2)^(k-1)b_(k-p)(n,x)d_p
   +x product_(i=n+1)^(n+k-3)(1+x/i)(f0+f1 x+f2 x^2),
(f0,f1,f2)=(L^2-2k,L^2-3L+3k,L-k)/[L(L-1)(L-2)].
```

Every displayed factor is nonnegative. The b_r decrease coefficientwise as n
increases. The three forward differences f_i(L)-f_i(L+1), multiplied by the
positive L(L-1)(L-2)(L+1), are respectively


```text
L^2+3L+2-6k, L^2-3L+9k-4, 2L-3k+2.
```

For L=2k+s,k=r+3 with r,s>=0 these have nonnegative coefficients and positive
constants. Therefore c(n,k)<=c(k,k). This compares an explicitly derived
polynomial quotient; it does not cancel a positive factor from an inequality.

At k=2 use the separate exact cancellation


```text
c(n,2)=d_2+x(nx+n+4)/[(n+1)(n+2)].                 (6)
```

The extra x and x^2 coefficients decrease in n: the difference numerators are
n+7 and n-1 over their common positive denominator. At n=2 this is exactly
(1+2x/3)d_1. Multiplication by a_n and 2/3<=n/(n+1) proves even the factor-one
version of (5) for k=2. An unrelated earlier provider k=2 implementation failure
is not mathematical evidence against this exact identity.

It remains to bound c(k,k), k>=3. The full Vandermonde sum, with terminal, is


```text
V_k(x,x)=[d_(2k)(2x)-d_k(x)^2]/2+d_k(x)a_k(x).
```

Write Q=a_(2k-3), c=(2k-1)/k, e=(k+1)/(2k), Delta=2(k-1)(2k-1).
The full wall pair is J=x(x-1)Q(c+ex)/Delta. Retaining its adverse part gives


```text
-J<=xQ(c+ex)/Delta<=[1/(2k)]T_k d_(k-1).          (7)
```

Indeed a_k a_(k-2)>=(1+x)Q by sorted denominator factors and c+ex<=c(1+x).
The remaining factor of T is nonnegative. Independently,


```text
d_k a_k<=[(k-1)/k]T_k d_(k-1),                   (8)
```

because 1/k<=(k-1)/(k+1) for k>=3. Split the factors of d_(2k)(2x) into
even and odd denominators. After factoring x a_(k-1), compare the odd list
(1/2,3/2,...,k-1/2) with (1,(k+1)/k,2,...,k-2,k). Every middle factor is
dominated directly; the first and last need factors 2 and k/(k-1/2).
The exact outside prefactors yield


```text
d_(2k)(2x)/2<=[1-1/(2k-1)]T_k d_(k-1).          (9)
```

Discarding only the explicitly negative square in this upper bound, (7)-(9)
give C_(k,0)<=[2-1/(2k-1)-1/(2k)]T_k d_(k-1). Multiply the exact quotient
comparison by a_n and the diagonal bound by the positive product a_n/a_k;
then k/(k+1)<=n/(n+1) proves (5) for every n>=k>=2.
The factor-one generalization is false, already at n=k=3. Its linear slack
is -1/12. The factor two is substantive, not a suppressed error.

## 4. One common reserve pays all leaves

Let F_(n,k)=a_n a_k-d_(n+k). Its exact difference is


```text
F_(n,k+1)-F_(n,k)
  =x F_(n,k)/(k+1)
   +d_(n+k)[nx/((k+1)(n+k+1))+1/(n+k+1)]>=0.      (10)
```

Sorted denominators prove F_(n,k)>=0 and F_(n,1)=T_n, so all F_(n,k)>=T_n.
Complete rising addition in F and the full hockey-stick identity imply


```text
F(2h)=sum_(j=0)^(n-1)d_j(2h)F_(n,n-j)
                                      >=T_n a_(n-1)(2h).
```

Using (5) on every nonterminal C and retaining the terminal with its exact
coefficient one, the full convolution gives


```text
W(x,x+z)<=T_n[2d_(n-1)(x+z)-d_(n-1)(z)].
```

Thus the ENTIRE original in (3) satisfies


```text
P_equal>=T_n[a_(n-1)(2h)-2n d_(n-1)(h)+n d_(n-1)(z)]. (11)
```

There is one expenditure of the full F reserve; no base is spent once per leaf.

For every integer m>=6 the uniform dilation inequality is


```text
a_m(2h)-2(m+1)d_m(h)>=a_m(h).                     (12)
```

To prove every coefficient, write a_(m-1)=sum b_k h^k, b_m=0. Double counting
subsets of slopes 1,1/2,...,1/(m-1) gives k b_k>=(m-k)b_(k-1)/(m-1).
For k>=1 the coefficient in the difference of (12) is


```text
(2^k-1)b_k+(2^k-2m-3)b_(k-1)/m.
```

For 3<=k<=m its lower-bound numerator over km(m-1) is
(2^k-1-2k)m^2-k(2^k-3). At k=3 this is m^2-15>0. At k>=4 use m>=k and
2^k-1>=2k+2, proved at k=4 and then inductively. The resulting minimum is
nonnegative. At k=1 the exact coefficient is H_(m-1)-2-1/m, equal to 7/60 at
m=6 and increasing. At k=2, b_2-(2/3)H is 5/72 at m=5; adding a slope a
increases it by a(H-2/3)>0. Hence 3b_2-(2-1/m)H>0 for m>=6. The constant
is zero and higher degrees vanish. The m=5 linear failure -7/60 is retained.

For n>=7 apply (12) with m=n-1 in (11), and keep h=x+z>=x:


```text
P_equal>=T_n a_(n-1)(h)>=T_n a_(n-1)(x)>=a_n(x)^2>=K_n(x). (13)
```

The middle product inequality is n/(n+1)>=1/n, valid for n>=2. All variables
are nonnegative multiples of the original t. This signs the whole high star
uniformly and includes H=A; it is not an infinite claim inferred from arrays.

## 5. Four fixed bases and independent complete evidence

For n=3,4,5,6 reconstruct ALL coefficients of P_equal(x,x+z)-K_n(x) through
total degree 2n, including every physical zero coefficient. The root uses (2)-(4).
The independent implementation uses the distinct first-row finite identity


```text
P_equal=a_n(x)a_n(3x+2z)
  -sum_(q=0)^n binom(x+n,n+q)binom(2x+2z+n-1,n-q)
  -n sum_(q=0)^n binom(x+n,n+q)binom(x+z+n-1,n-q)
  +n sum_(q=0)^n(q+1)binom(x+n,n+q)binom(z+n-2,n-q). (14)
```

Here the first-row compositions are complete. Their central, leaf and pair
strict violations leave second-row totals 2x+2z+a0-1, x+z+ai-1, and z+a0+ai-2.
Newton summation gives binom(x+n,n+q) and (q+1)binom(x+n,n+q), respectively.
At negative initial remainders only -1 or -2 can occur; their binomial products
vanish for n>=3. Every row bound, strict shift, endpoint and pair multiplicity
therefore survives this all-grade identity. It does not depend on fitting.

The four full exact nonnegative arrays, complete coefficient equality between
the two constructions, and the all-n argument (13) jointly establish high E.
The source's four certificates may be authenticated additionally, but provider
numerical outputs are not the independent evidence. These are fixed necessary
algebraic bases, not an expanding cutoff. Their exact outcomes are bound in
verification/CHECKS.json; the claim remains proposed until that receipt and the
single Astra review pass.

## 6. Restore arbitrary complete triangle-free originals

Any edge between two nonminimum widths forces a triangle with a minimum.
Thus a nonempty triangle-free graph is a star centered at e0=A+alpha. With
C=B-A and L=C-2alpha>0 its m leaf heights satisfy 0<Hi<=L and Hi+Hj<=L.
N>=3, and a nonoverlapping pair together with a third positive column forces
R>0, including the one-edge case. Every triple contains a nonoverlapping pair,
so its strict intersection is empty. No supported triple has been deleted.

Use the full A76 original formula with all singleton height improvements and
the complete g_alpha(H)=V(Ht+alpha t)-V(alpha t)-J(A,H;t). A77 proves every
ordinary coefficient nondecreasing and convex in H, on both bands and across
the full derivative jump. Let q=max Hi and theta=max(0,2q/L-1). Its common
chord gives one numerical convex weight for ALL coefficients and reduces the
entire original to a paid one-pair endpoint and the symmetric star endpoint.
The full A76 widening theorem pays its alpha increment; the latter reduces to
the equal star at H=L/2. That star is paid by A77 low E and sections 2-5 above.
The full A75 one-pair endpoint is already paid. Hence P_e>=K_n in (1).

For n=2, triangle-free means at most two edges and the accepted A76 complete
two-overlap theorem applies. Empty graphs retain the complete A73/A74 theorem,
including N<=2, zero rows, points and their true degrees; no generic degree is
assigned to them here. Hi=0 becomes a nonleaf exactly, pair equality stays
strictly disjoint, H=A uses both full formulas at their common wall, tied labels
remain distinct, and physical zeros never add free coordinates. No division
is performed when a profile interval collapses.

## 7. Scope, failed routes and reentry

ADOPT only the complete high-star argument, its full fixed bases, and the
resulting arbitrary-count selected-width triangle-free theorem after the gate.
The new root weakened block comparison also fails uniformly: for j=n-2,


```text
[x](2R_(n,j)-n C_(n,j)-2T_n)
            =(8-n)/2-(n-4)/[(n+1)(n+2)]<0, n>=8.
```

This is an obstruction to that sufficient separate-block payment. The full
star remains positive; combining the complete correction before payment is
what avoids that obstruction. Preserve the previous stronger failed bound and
all corresponding complete data. Neither is a KTT counterexample.

Below-A overlaps, triangles with supported triples, larger cliques, arbitrary
transportation/higher signs, general LR shapes/longer content and whole rank
seven remain open. Pro053 U11/U12 triangular results, its U02 independent
character theorem and U04 quadratic operation remain serious unadopted source until
their own full independent reconstruction. The high-E result has no arbitrary

review is not human peer review, formal certification, novelty or publication.
