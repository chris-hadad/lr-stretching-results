# A83: complete three-factor boundary payment and two top gain coefficients

**Accepted at the actual internal scientific/public review gate.** The original frozen source retains its historical proposed wording and exact byte identity.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

A bounded Astra research lane derived the full four-family organizer and the
top-layer comparison. Root reconstructed it, supplied the finite canonical
reduction n<=2d and independent complete coefficient certificate, and transfers
the two top layers to an actual unequal-row original gain below. The preceding
Pro056 fusion and reflection retain their source credit. This is not an
all-coefficient theorem for unequal-row two-positive-overlap originals.

## 1. Whole auxiliary object, exact fusion and canonical reduction

Let n>=0, 0<=k,l,m<=n and


```text
E_(n;k,l,m)(A,z)=[u^n v^(n+1)](v-u)
                 (1-u)^(-A-2)(1-v)^(-z) r_k r_l r_m,
r_i=h_i(u,v)-uv h_(i-1)(u,v), r_0=1.
```

Its derivative F is taken at FIXED A, then A=x+z with x,z>=0. Whole E,
including all z-independent terms, is retained. A physical original contributes
its original rising prefactor at both prefix endpoints, and an additional t
when differentiating a stretched ray.

Complete two-row multiplication gives the exact, unshifted fusion


```text
r_k r_l=sum_(i=0)^min(k,l)(uv)^i r_(k+l-2i)
      -sum_(i=0)^(min(k,l)-1)(uv)^(i+1)r_(k+l-2i-1).    (1)
```

Substitute r_i=h_i-uv h_(i-1) and use the full two-row Pieri product to
verify all four resulting h families; the equal-index h_-1 endpoint is zero.
Also (v-u)r_i=v^(i+1)(1-u)-u^(i+1)(1-v), so an index i>n makes the
ENTIRE requested extraction zero, before any differentiation.

Suppose k+l>n, put p=k+l-n, n'=2n-k-l, k'=n-l, l'=n-k. Apply (1)
and retain both full fusion sums. Their terms with i<p are zero by the exact
index bound, and i=p+j reindexes the rest, INCLUDING the terminal. Therefore


```text
E_(n;k,l,m)=E_(n';k',l',m).                              (2)
```

If m>n' the complete object is zero; at n'=0 only E_(0;0,0,0)=1 remains.
Every nonzero step decreases n. By product symmetry, reflecting any offending
pair terminates at a zero/constant branch or at


```text
k+l<=n, k+m<=n, l+m<=n.                                (3)
```

This is auxiliary algebra, not a change of physical LR rows or degree. The
original prefactor and both complete E endpoints stay attached. The invariant


```text
d=2n-k-l-m
```

is unchanged by (2). In the canonical cone, adding the three inequalities
in (3) yields 2(k+l+m)<=3n and hence


```text
n<=2d.                                                (4)
```

This finite-reduction bound is useful for a complete deficit band. It does
not bound the original rank or claim the unrestricted coefficient problem finite.
If one index is n, (3) forces the other two zero, E=A_n(A) and F=0.

## 2. Complete four-family organizer

Order k<=l<=m and put K=k+l+m, alpha=k+l. For an integer interval [a,b],
write its cardinality as max(0,b-a+1). Define


```text
B_s=#[max(0,s-m), min(k,s,alpha-s)],
U_s=#[max(0,s-m+1), min(k,s,alpha-s-1)],
V_s=#[max(0,s-m), min(k-1,s,alpha-s-1)],
W_s=#[max(0,s-m+1), min(k-1,s,alpha-s-2)],
C_s=U_s+V_s, N_s=n-s, M_s=n-K+s.
```

These counts vanish outside finite ranges. With the full primitive


```text
q_(N,M-1)=A_N(A)d_M(z)
            -A_(M-1)(A+1)[d_(N+1)(z)-d_N(z)], 1<=M<=N,
q_(N,-1)=A_N(A),
```

and all invalid indices zero, the ENTIRE identity is


```text
E=sum_(s>=0)[B_s q_(N_s,M_s-1)
            -C_s q_(N_s-1,M_s-1)+W_s q_(N_s-2,M_s-1)]. (5)
```

A zero multiplicity is removed before evaluating nominal indices. In particular
M_s=0 contributes an actual constant-in-z primitive, not a discarded endpoint.

Here is a direct derivation. Fuse r_k r_l, then each remaining r with r_m.
The four full families, before collecting s=i+j, are


```text
+sum_(i=0)^k sum_(j=0)^min(alpha-2i,m)
                      (uv)^(i+j) r_(K-2i-2j),
-sum_(i=0)^k sum_(j=0)^(min(alpha-2i,m)-1)
                      (uv)^(i+j+1) r_(K-2i-2j-1),
-sum_(i=0)^(k-1) sum_(j=0)^min(alpha-2i-1,m)
                      (uv)^(i+j+1) r_(K-2i-2j-1),
+sum_(i=0)^(k-1) sum_(j=0)^(min(alpha-2i-1,m)-1)
                      (uv)^(i+j+2) r_(K-2i-2j-2).
```

For each family, solve its full interval inequalities for i at fixed s.
They give respectively B_s,U_s,V_s,W_s. A single r_R extraction is
q_(n,n-R-1), directly from (v-u)r_R's two endpoints. This proves (5),
including the compulsory double-negative W contribution and all constants.

## 3. Two full leading homogeneous layers at every index

Let D_(N,M-1)=partial_z q_(N,M-1) at fixed A. For N>=M>=1 its leading
homogeneous layer, in total degree N+M-1, is


```text
L_(N,M)=[A^N z^(M-1)-A^(M-1)z^N]/[N!(M-1)!].          (6)
```

After A=x+z its numerator is
A^(M-1)z^(M-1)(A^(N-M+1)-z^(N-M+1)), hence nonnegative and nonzero.
Its next complete homogeneous layer is


```text
P_(N,M)=1/[2N!(M-1)!] *
  [N(N+1)A^(N-1)z^(M-1)+(M-1)^2 A^N z^(M-2)
   -(M-1)(M+2)A^(M-2)z^N-N(N-2)A^(M-1)z^(N-1)].      (7)
```

For M=1 the zero-multiplier terms are absent; no negative power is evaluated.
Equations (6)-(7) follow by retaining the top two coefficients of EVERY rising
factor of the full q, including the lower d'_N term. Since N_s+M_s=d,
(5) gives the complete layers


```text
[F]_(d-1)=sum_(M_s>=1) B_s L_(N_s,M_s),
[F]_(d-2)=sum_(M_s>=1)
              [B_s P_(N_s,M_s)-C_s L_(N_s-1,M_s)].     (8)
```

The W terms first enter degree d-3; they remain in the full object (5).
A terminal L_(N-1,M) with N=M is exactly zero and no invalid primitive is
introduced by that algebraic zero.

The defining intervals give 0<=C_s<=2B_s. Except for (N,M)=(2,1),


```text
P_(N,M)-2L_(N-1,M) >=_coef 0 after A=x+z.               (9)
```

For M>=2 set R=N-M. Apart from the positive factor
A^(M-2)z^(M-2)/(2N!(M-1)!), the difference is


```text
T=(M-1)^2 A^(R+2)+N(N-3)A^(R+1)z
                   +N(6-N)A z^(R+1)-(M-1)(M+2)z^(R+2).
```

After A=x+z, its x^0 coefficient is 3(R+1), and the coefficient at
x z^(R+1) is
(M-1)^2(R+2)+N(N-3)R+3N.
For j>=2, the coefficient at x^j z^(R+2-j) is


```text
(M-1)^2 binom(R+2,j)+N(N-3)binom(R+1,j)>=0, N>=3.
```

The sole remaining case N=M=2 gives T=x^2+8xz+3z^2. This proves every
coefficient, with the whole negative z endpoint accounted for.
For M=1 the difference is

    [(N-3)(x+z)^(N-1)+(6-N)z^(N-1)]/[2(N-1)!].

At N=1 this is 3/2. For N>=3 its pure-z coefficient is positive and
all positive-x coefficients are nonnegative. At N=2 the nominal factor 2
would fail. But the actual r index K-2s=N-M is then one. The intervals
force U_s=0, hence C_s=V_s<=B_s, and the exact needed comparison is


```text
P_(2,1)-L_(1,1)=x/2+3z/2>=0.                          (10)
```

Equations (8)-(10) pay the WHOLE two leading layers at every index. No
separate adjacent derivative is assumed positive.

For a canonical branch with all indices<n and d>=2, F has exact bivariate
degree d-1. Set s0=max(0,K-n+1). Then M_(s0)>=1 and
s0<=min(k+l,floor(K/2)); the interval defining B_(s0) is nonempty.
(The additional s0<=k+m follows from l<=m.) Thus its first line in (8)
contains a nonzero positive L. This claim concerns the complete auxiliary
field, not the degree of a physical LR original or a particular boundary ray.

## 4. Complete all-index deficit band d<=4

If d<=1, canonicalization leaves only zero derivatives or the explicit
small endpoints. For the entire band d<=4, (4) proves n<=8 after
canonicalization; the zero/constant/index-n branches are handled before
assigning a degree. Therefore a COMPLETE finite certificate at n=1,...,8
proves this reflected auxiliary subdomain at every original index n.
This is a proved reduction, not extrapolation from a positive panel.

Root's primary algorithm directly expands the entire r-product rectangle and
then differentiates the Y exponent. It froze 494 symmetric triple fields,
containing 6,329 nonzero ordinary derivative slots, before reading the new
Pro056 U06 fusion or the new research-lane argument. A separately authored
algorithm reconstructs all complete primitives from (5), differentiates at
fixed A, substitutes A=x+z and freezes its complete output BEFORE reading
the primary arrays. Every full field agrees. It additionally retains 6,686
nonzero whole-primitive slots and verifies every complete reflection in the
finite domain. Symmetry of the three r factors supplies the other orderings;
no physical LR triple is identified by this auxiliary symmetry.

There are exactly 29 canonical rows with n>=1 with d<=4 in this
complete finite domain: 2 at d=1, 5 at d=2, 8 at d=3 and 14 at d=4,
including the index-n zero-derivative rows. Every full derivative has
nonnegative coefficients. The n=0 constant and all reflected-zero branches
are exact algebraic cases. The CHECKS row list is the finite proof certificate;
all coefficients, including every zero branch, are reproducible using only
Python Fraction arithmetic. No LR/table backend, fit or new original is involved.

The result is


```text
F_(n;k,l,m)(x,z) >=_coef0 whenever 2n-k-l-m<=4,          (11)
```

with the full reflection and support conventions above. Complete low-deficit
examples include F=x+3/2 at d=2, and at d=3 either


```text
x^2/2+xz+3x/2+3z/2+7/6,
x^2+2xz+2x+3z+5/6,
```

on the nonzero canonical branches. These examples do not replace the full
certificate or its finite-reduction proof.

The independent join retains three distinguishing controls: removing W changes
the complete primitive; differentiating with x fixed changes the full field;
and the actual adjacent pair for n=3,k=l=m=1 has constant -1/3, while its
ACTUAL complete terminal has 7/6 and their full parent has constant 5/6.
All pair, terminal and parent polynomials remain in the receipt. Neither the
adverse pair nor the bound in (9) is substituted for the original full field.

## 5. Transfer to a whole unequal-row later-mask gain

Return to the complete literal original in ORIGINALS-AND-BASES-v1.md, with
H,G>0, delta=b-c>0 and A=c-H-G. Its entire last-chamber prefix is


```text
Q(Z)=[u^n v^(n+1)](v-u)X^(A+2)Y^z R_H R_G h_delta,
Z=H+G+delta+z, x=b-Z, A=x+z.
```

The complete rising expansion, with both physical delta occurrences ell=0,1,
is


```text
Q=sum_(k,l=0)^n sum_(ell=0)^(n+1)
       d_k(H)d_l(G)d_ell(delta) E_(n;k,l,max(ell-1,0)).  (12)
```

It contains EVERY eight-mask term and its finite-baseline cancellation, as
proved in OVERLAP-GENERATORS-v1.md. Differentiating at fixed physical
A,H,G,delta inserts the factor t on a stretching ray.

For ell>=1 the original prefactor has degree K+1, where
K=k+l+max(ell-1,0). The two signed-and-paid layers in (8) therefore cover
the contributions in physical degrees 2n+1 and 2n. Lower prefactor coefficients
are nonnegative; lower F layers cannot reach those degrees. For ell=0 the
prefactor has degree K, so only the nonnegative leading F layer contributes
to degree 2n. Exact reflections preserve d and F while keeping the ORIGINAL
prefactor, so this degree accounting is unchanged by canonicalization.
The zero/constant/index-n cases add no derivative. Thus BOTH complete physical
derivative coefficients at degrees 2n+1 and 2n are nonnegative.

They are strict in a last-chamber interior x,z,delta>0: k=l=0,ell=1 is
an actual disjoint occurrence with multiplier delta t. Its D_(n,n-1)
leading layer is positive at x,z>0, and its next layer is positive by (9),
including n=2's explicit polynomial. The additional physical t remains.

Consequently, for every legal original with


```text
H,G,delta>0, 0<=j<s<=A=c-H-G,
```

both endpoints V=b-s and U=b-j lie in the full last chamber. Integrating
the complete derivative across [V,U] proves


```text
[t^(2L+3)](P_s-P_j)>0,
[t^(2L+2)](P_s-P_j)>0.                                (13)
```

The companion gives the full literal parent/target, all capacities, saturated
chart and prior actual degree 2L+3 of the moving original. The fixed parent's
own degree is 2L+2 or 2L+1 at j=0. Its full expression is used ONCE in
P_s=P_j+Q(U)-Q(V), and both full Q endpoints retain every mask and scalar shift.
No lower coefficient of this whole unequal-row gain is signed by (13).
At s=j the whole gain is zero; A=0 allows no nonempty last-chamber interval.
These are complete-operation high-coefficient statements, not a full generator.

## 6. Exact remaining problem and provenance

For a general d>=5, the organizer (5) leaves homogeneous degrees 0 through
d-3 unpaid by this root theorem. Pro056 separately supplies an all-index
constant theorem, still SOURCE here; it is not needed for (11) or (13).
The first remaining layer of (5) has its COMPULSORY W contribution:


```text
sum_s [B_s[D_(N_s,M_s-1)]_(d-3)
        -C_s P_(N_s-1,M_s)+W_s L_(N_s-2,M_s)].          (14)
```

A new joint inequality must pay this complete expression and every lower layer.
Full last-chamber positivity would still leave all earlier unequal-row masks,
both actual endpoints and the full fixed original. This result does not rule
out another representation or prove any ordinary-negative LR coefficient.

Pro056 U06 fusion/reflection source is the exact captured object
8e485de2d0ebe581809d6c2ff4affc57b39141584abdf9eb212915d94a1d8fc0.md.
The root/Astra derivation adds the four-family interval organizer and the full
leading-layer payment; root's n<=2d reduction plus two independent complete
arithmetic freezes supplies the entire d<=4 statement. The physical top-gain
transfer is reconstructed from the actual general eight-mask prefix. These
are distinct contributions, and no SOURCE constant/contact theorem is promoted.

The complete finite fields, reflection controls and two trusted representations are included in this module. The actual internal scientific/public review accepted these exact stated scopes; frozen source history remains unchanged.
