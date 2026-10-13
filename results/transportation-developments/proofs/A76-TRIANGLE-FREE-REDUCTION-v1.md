# A76: complete triangle-free star reduction and a finite exact all-margin certificate

Curated mathematical proof from **A76**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root mathematics derived after the complete height-budget theorem and its explicit over-budget obstruction. The accepted A73 product/half-profile results and A75 complete one-pair theorem retain their Pro051-derived provenance. No active Pro052 or Pro053 scientific result is a premise. The new arbitrary-n widening lemma below is a proof; the other two lemmas currently have a finite n=3..14 COMPLETE coefficient certificate. Their bounds must not be merged into an unbounded claim.

The certificate requires the actual independent complete-array equality/sign checks and every negative control, not a positive sample panel.

## 1. The entire original and the missing reserve

Use STAR-COMPOSITION-v2.md's full original: balanced integral rows (A,B,R), 0<A<=B, N=n+1 positive labeled columns, every positive column at least A, and overlapping pairs defined by ei+ej<A+B. Keep physical zeros and the literal lambda-outer LR preimage. Suppose there is no triangle of three mutually overlapping columns. Every edge must then meet a minimum column e0: if ei+ej<A+B for two nonminimum columns, the minimum forms the two other edges and gives a triangle. Thus the graph is either empty or a star. An empty graph is already paid by A73/A74.

For a nonempty star, set e0=A+alpha, C=B-A, L=C-2alpha>0 and let Hi be its m leaf heights. Minimum-column order gives 0<Hi<=L; nonoverlap of two leaves gives Hi+Hj<=L. All n-m nonleaves have shortfall at most alpha. N>=3 and R>0 follow exactly as in the complete composition proof; the saturated original lattice and actual degree 2n are proved before any coefficient extraction.

Write x=At, y=alpha t and h=Ht. The same full U,V,F,K notation applies. Define the COMPLETE leaf correction


```text
g_n(x,h)=V_n(x,h)-V_n(x,0)-J_(n-1,2)(A,H;t).        (1)
```

The pair J retains both original row bounds, both strict shifts, the entire high-band tail and its zero value at H=0. All derivatives below concern numerical height H at fixed A, coefficient by coefficient in t. Equivalently take formal partial_h first and then substitute x=At,h=Ht; the positive powers of t introduced by numerical differentiation merely shift the coefficient index.

Two sufficient lemmas are:


```text
G: every ordinary coefficient of g_n is nondecreasing and convex in H>=0;
E: E_n(x,h)=F_n(x,2h)-F_n(x,0)-n g_n(x,h)>=_coef 0. (2)
```

G must include every H=A derivative jump, not only smooth pieces. E is the ENTIRE equal-height n-leaf star minus K_n, not an isolated signed intersection. The original for E+K has rows (A,A+2H,(n-1)A+(n-2)H), columns A and n copies of A+H. Its full pair incidence has n pairs and no triple. All dimensions and margins are explicit.

## 2. A new uniform coefficient ratio and whole-star widening

This section holds for EVERY n>=2. Let uk(x)=[z^k]U(z), vk(x)=[z^k]V(z). The accepted A73 rising addition and complete product bound give, for 0<=l<n,


```text
B_l=a_n(x)a_(n-l)(x), D_l=d_(2n-l)(x),
B_l >= a_n(x)+(n+1)D_l.
```

For k>=1 let s_lk=[z^k]d_l(z). All s_lk are nonnegative. The terminal l=n contributes a_n(x) to BOTH U and V and is retained:


```text
uk=sum_(l=k)^(n-1) s_lk B_l+s_nk a_n(x),
vk=sum_(l=k)^(n-1) s_lk D_l+s_nk a_n(x).
```

Put e_k=[z^k]a_(n-1)(z). The exact hockey-stick identity sum_(l=0)^(n-1)d_l(z)=a_(n-1)(z) gives sum_(l=k)^(n-1)s_lk=e_k. Also s_nk=e_(k-1)/n. For 1<=k<n, expanding elementary symmetric polynomials in the n-1 slopes 1,1/2,...,1/(n-1) proves


```text
k e_k >= (n-k)e_(k-1)/(n-1)
        >= (n-k)e_(k-1)/n.
```

The first inequality counts every k-subset k times and bounds each unused slope below by 1/(n-1). It remains valid when the relevant elementary polynomial is zero. Consequently


```text
k uk-n vk
  >= [k e_k-(n-k)e_(k-1)/n]a_n
        +[k(n+1)-n]sum_(l=k)^(n-1)s_lk D_l >=0.    (3)
```

At k=n, both sides are exactly zero after the identical terminal terms; no lower-index product lemma is used. Thus k uk>=n vk for every 1<=k<=n, as an ordinary coefficient inequality in x. This is an arbitrary-n proof, not extrapolation of the finite ratio probe.

Now consider the ENTIRE symmetric-star original


```text
Z_n(x,h,y)=U(2h+2y)-V(2h+y)-nV(h+y)+nJ(h).          (4)
```

Its margins are rows (A,A+2H+2alpha,(n-1)(A+alpha)+(n-2)H), columns A+alpha and n copies of A+H+alpha. It has exactly the original n central-leaf pairs of height H and no triple. Both bands remain in J.

The pure-y portion of Z(x,h,y)-Z(x,h,0) is exactly the accepted A73 Q_half-K_n and is nonnegative. A mixed h^r y^s term, r,s>=1 and k=r+s<=n, has positive binomial factor times


```text
2^k uk-(2^r+n)vk.
```

By (3), n>=k, r<=k-1 and 2^(k-1)>=k for k>=2, this is at least


```text
[n(2^k/k-1)-2^r]vk
  >= [2^(k-1)-k]vk >=0.                            (5)
```

Terms of larger k vanish; terms with y exponent zero cancel. Hence


```text
Z_n(x,h,y)>=_coef Z_n(x,h,0)                         (6)
```

for EVERY n>=2, with all complete original terms retained. This is a paid widening operation between the displayed entire original family, not arbitrary column splitting. Its exact difference has zero constant and is nonnegative; no unsupported strictness is claimed for every difference degree.

## 3. From G and E to every complete star profile

For fixed nonnegative alpha define


```text
g_alpha(H)=V_n(At,(H+alpha)t)-V_n(At,alpha t)-J(A,H;t).
```

It equals g_n plus V(h+y)-V(h) minus an H-independent constant. The latter difference has nonnegative coefficients in x,h,y, so G implies that every coefficient of g_alpha is nondecreasing and convex in H, with the same nonnegative boundary jump. g_alpha(0)=0.

Let q=max Hi. If q<=L/2, monotonicity gives sum_i g_alpha(Hi)<=m g_alpha(L/2). Otherwise every other height is at most L-q; the convex chord of g_alpha(q)+(m-1)g_alpha(L-q) on [L/2,L] gives the common-weight comparison


```text
sum_i g_alpha(Hi)
   <=theta g_alpha(L)+(1-theta)m g_alpha(L/2),
theta=max(0,2q/L-1).                                (7)
```

These are the SAME numerical weights for every ordinary coefficient. Since g_alpha(L/2)>=0 and m<=n, replace m by n in the upper bound.

The entire original, with all singleton height improvements retained as nonnegative slack, therefore dominates the same convex combination of:

- the one-pair original with two columns A+alpha and n-1 columns A+C-alpha;
- the n-leaf symmetric-star original (4), with H=L/2 and y=alpha t.

The first is paid by the full A75 theorem and dominates K_n(At). The second dominates its alpha=0 original by the UNIFORM widening lemma (6), and that original is K_n+E_n>=K_n by E. Rational H=L/2 is solely a comparison slope; all polynomial inequalities extend by common-denominator clearing, without changing the physical original or its lattice.

Thus wherever complete G and E are established,


```text
ENTIRE P >= K_n(At)
  >= a_(2n-1)(At)[1+(n-1)At/(2n)]>_coef 0           (8)
```

through actual degree 2n. No aggregate height budget is needed. Every original row, labeled cap, pair multiplicity, strict shift and independent pair height band survives.

## 4. The finite exact coefficient certificate

For EACH integer n=3,...,14, the root certificate and independent checker construct every bivariate coefficient in both closed cones:


```text
low:  x=u+v, h=v,       u,v>=0;
high: x=u,   h=u+v,     u,v>=0.
```

The exact full pair polynomial is


```text
J_low=(x+1)binom(h+2n-3,2n-1)
                -(n-1)binom(h+2n-3,2n),
J_high=J_low+sum_(l=0)^(n-2)(l+1)
                binom(n+x,n-2-l)binom(h-x+n-2,n+2+l). (9)
```

Every binomial is its falling-product polynomial. This is the accepted entire A74 formula specialized to k=2,q=n-1, not a changed early-grade count.

The certificate contains and checks ALL coefficients of:

1. E_n, through total degree 2n, in both cones;
2. partial_h g_n and partial_h^2 g_n, differentiated at fixed x BEFORE cone substitution;
3. the complete g_n in both cones, for exact producer/checker equality;
4. g_high-g_low at h=x, which is identically zero, and its first derivative jump, whose every x coefficient is nonnegative.

All coefficients in items 1 and 2 are nonnegative. Continuity and the full nonnegative first derivative jump prove G across H=A, including equality. g(0)=0 follows from the exact V0 and empty J. The independent dense integer/common-denominator construction must agree with every complete root array, including physical zeros, domains and exact boundary arrays; changed/omitted coefficients, missing high tails, duplicate domains and altered source hashes must refuse. This is a finite EXACT multivariate certificate and proves all margin values at EACH listed n. It does not prove G or E at n>=15.

At n=2, a triangle-free graph has at most two overlaps, so the unbounded height-budget theorem already pays it. Empty-overlap originals use the accepted no-overlap theorem for every n; point and smaller actual-degree cases retain their own accepted conventions.

THEOREM: For every complete three-row transportation/LR original with specified 0<A<=B, every positive column at least A, at most 15 positive columns, and no triple of mutually overlapping columns (pairs are overlapping exactly when their sum is below A+B), every ordinary coefficient is strictly positive through its actual degree. The at-most-two-overlaps and height-budget families have the separate arbitrary-column-count theorem.

The original six-record roster and first formula report predate this extension: their field theorem_expected denotes the HEIGHT-BUDGET theorem only. O5 is outside that theorem but inside the finite exact all-star certificate at n=5. O6 remains outside the selected-width condition. Preserve those frozen records with this explicit interpretation, not a silent changed outcome.

## 5. What this changes toward unrestricted KTT

The local bottleneck has moved from paying two interactions to TWO precise uniform inequalities, G and E. Proving those at arbitrary n would close the entire triangle-free selected-width class at once. Increasing the finite cutoff alone is not the proposed next session. The complete over-budget negative gluing remainder remains valid, but retaining the reserves now pays it on every certified n rather than discarding the adverse term.

The strongest alternative is a complete contraction or global character grouping that bypasses G/E and simultaneously handles supported triples or a positive column below A. The full character identity retains every one/two/three-occupation term; its known negative sectors preclude a termwise sign proof. No transportation-family result by itself covers every LR original. The strategic target remains unrestricted KTT positivity, with exact complete-negative-original verification as the alternative outcome.

No universal split gain, unrestricted transportation theorem, arbitrary three-letter LR theorem, whole new ordinary rank, formal certification, external peer review, novelty or public-release claim follows. Every source boundary and historical debt remains.
