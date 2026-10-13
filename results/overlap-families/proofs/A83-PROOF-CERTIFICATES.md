# Independent overlap algebra handoff

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

No LR/table/Sage oracle, returned program, source coefficient array or new named
original was used. All computations are exact formal polynomial identities with
rational coefficients. The finite fields corroborate implementations; they do
not supply any unbounded quantifier below.

## Definitions and complete-original interface

Use `A_r(v)=product_(i=1)^r(v+i)/i` and
`d_r(v)=product_(i=0)^(r-1)(v+i)/r!`, with `A_0=d_0=1` and negative
indices zero. Indices of finite sums are literal, including empty and exterior
ranges. All physical parameters on a stretching ray acquire the same grade;
scalar convolution offsets occur once.

The supplied complete original has `L>=1`, `n=L+1`, `b>=c>=1`,
`H,G>=0`, `H+G<=c`, three labeled long widths at least `b`, third overlap
`0<=j<=b`, fourth width `s>=j`, and `L` labeled detached widths at least
`b+c-H-G-j`. Its physical width and overlap lists are
`(u,v,k,s,w_1,...,w_L)` and `(H,G,j,0,...,0)`. Its literal backward
lambda-outer constructor retains all rows and zeros; none is sorted. The
complete determinant includes both partners of its potentially live lower entry.
Their paired cancellation gives the full character

```
P_s(t)=[z^(bt)w^(ct)](1-w/z) r_(Ht)(z,w) r_(Gt)(z,w)
                     (H_(st)(1,z,w)-H_(jt-1)(1,z,w))/D^(L+2),
D=(1-z)(1-w), r_q=h_q-zw h_(q-1).
```

The all-grade positive chart keeps `y<=ct`, both strip-size inequalities,
ordinary integer interlacing coordinates and its actual affine equalities. Its
separate signed residual-cap extension needs both Weyl partners. These original,
saturated-lattice and prior-degree premises are read-only SOURCE inputs in this
lane; root must retain their exact physical guards and independently assess them.
No integral-vertex, transportation-dimension or fitted-degree inference is made.

Set `A=c-H-G`, `delta=b-c`, `U=b-j`, `V=max(b-s,0)`.
The complete transfer is `P_s=P_j+Q(U)-Q(V)`. `P_j` is the actual fixed
fourth-width original, with its changed content and separately constructed
literal triple. It is used once. Neither endpoint loses constants because their
physical derivatives vanish.

## Two-r chain: the all-index payment

For `a>=1`, `0<=m<=a-1`, put

```
q_(a,m)=A_a(A)d_(m+1)(z)-A_m(A+1)(d_(a+1)(z)-d_a(z)),
q_(a,-1)=A_a(A),
C_(n;k,l)=q_(n,n-k-l-1)
  +sum_(i=0)^(min(k,l)-1)(q_(n-1-i,n+i-k-l)-q_(n-1-i,n+i-k-l-1)).
```

Differentiate at fixed physical `A`, then substitute `A=x+z`. The direction in
legal coordinates is `partial_z-partial_x`. Ordinary `partial_z` at fixed slack
is a different operation. The independent auxiliary construction extracts
`[u^n v^(n+1)](v-u)(1-u)^(-A-2)(1-v)^(-z) r_k(u,v)r_l(u,v)` by its
complete rectangular series. It never calls the q-chain routine.

Order `k<=l`, let `p=n-k`, `q=n-l`, `e=n-k-l`. If `q=0`, the complete
derivative is zero. The constant `C_(n;n,n)=1` stays in the primitive. For
`q>=1,e<=0`, changing `i=-e+r` leaves precisely

```
sum_(r=0)^(q-1)(D_(p+q-1-r,r)-D_(p+q-1-r,r-1)).
```

This is the complete canonical derivative at
`(n',k',l')=(p+q-1,q-1,p-1)`, whose `e'=1`. Its first negative term is
the derivative of an actual constant. The smallest boundary `p=q=1` gives
`n'=1` and `D_(1,0)=x+3/2`; it needs no n>=2 extrapolation.

For canonical `e>=1`, define

```
R_(a,M)(v)=(M-1)!/a! (v+1) product_(r=M+1)^a(v+r),
K_(a,M)=A_a(A)-A_(M-1)(A+1)R_(a,M)(z),
S_(a,M)=K_(a,M)d'_M(z),
B_(a,M)=R_(a,M)(z)d'_M(z)-d'_(a+1)(z)+d'_a(z).
```

The complete derivative is `D_(a,M-1)=S_(a,M)+A_(M-1)(A+1)B_(a,M)`.
The identity `A_a(A)=A_(M-1)(A+1)R_(a,M)(A)` makes K a product difference
with nonnegative coefficients after `A=x+z`. The recurrence, after multiplication
by positive a, is the free-symbol identity

```
a (K_(a,M)-K_(a-1,M))
 = z K_(a-1,M)+(A-z)A_(a-1)(A).
```

The full slack chain reindexes to
`S_(p,q)+sum_(i=0)^(k-1)(S_(n-i,e+i)-S_(n-1-i,e+i))`.
All increments are within `1<=M<=a-1`; the terminal is retained positive.

For `r>=1`, define the entire deleted-factor polynomial

```
H_r=(z+2r+1)d'_r-r d_r
   =1/r! sum_(i=0)^(r-1)(2r+1-i) product_(0<=v<r,v!=i)(z+v).
```

The second identity follows by distributing `r d_r` over all r factors. Every
coefficient is nonnegative, including `H_1=3`. With `w_r=(r-1)!d'_r`, the
rising derivative recurrence gives
`(z+r+1)w_r-w_(r+1)=(r-1)!H_r/(r+1)` at arbitrary r. Telescoping every
index M through a-1 and keeping the last recurrence gives

```
B_(a,M)= (z+1)/a! sum_(r=M)^(a-1)
          (r-1)!/(r+1) product_(v=r+2)^a(z+v) H_r
          + H_a/[a(a+1)].
```

The terminal coefficient has no extra z+1. At `M=a=1` it is `3/2`.
This finite-sum identity, derived from the arbitrary recurrence, is the
all-index telescoper; testing a<=10 is its implementation control only.

Collect its entire H_r coefficient over the original chain. At `r<e` there is
no occurrence. At `r>=q`, each same-a correction retains both occurrences or
neither; `A_j(A+1)-A_(j-1)(A+1)=A_j(A)` pays the former, including the distinct
terminal. The sole possible debt is `e<=r<q`. Set
`b0=n+e-r-1>=p>=q>r`, `f_s=product_(v=r+2)^s(z+v)/s!`.
All occurrences of that atom are nonterminal. After factoring its common
positive H_r factor, its complete weight is

```
A_(e-1)(A+1) f_n
 +sum_(j=e)^(r-1) A_j(A) f_(n+e-j-1)
 -A_(r-1)(A+1) f_b0.
```

The entire telescoping A sum equals `A_(r-1)(A+1)`. Thus this is exactly

```
A_(e-1)(A+1)(f_n-f_b0)
 +sum_(j=e)^(r-1) A_j(A)(f_(n+e-j-1)-f_b0).
```

Every index is at least b0, and
`f_s=f_b0 product_(v=b0+1)^s(1+z/v)` signs each complete difference. This
pays every disappearing atom once. It uses no separate sign claim for adverse
adjacent-m or adjacent-n derivatives. Consequently the complete fixed-A chain
derivative is nonnegative at arbitrary n>=1 and all k,l in [0,n].

## Complete physical expansions and pre-return payment

In the last chamber, the balanced prefix is the same extraction multiplied by
`R_H R_G`, and its full expansion is
`sum_(k,l=0)^n d_k(H)d_l(G)C_(n;k,l)`.
The one-zero prefix uses `R_G h_delta` and expands as
`sum_(k=0)^n sum_(ell=0)^(n+1) d_k(G)d_ell(delta)C_(n;k,max(ell-1,0))`.
The physical ell=0 and ell=1 occurrences are distinct. The dual finite-baseline
cancellation is checked through the complete shifted G and all eight F fields;
no selected baseline was discarded by a program. Each physical derivative
retains the extra grade factor t.

Before return, the complete coefficient of `d_K(A)` has `r=n-K` and

```
q_r=d_D(Z)
 -sum_(i=0)^(r-1) A_i(T1)(d_(D-i)(Z-T1)-d_(D-i-1)(Z-T1)) [Z>T1]
 -sum_(i=0)^r2 A_i(T2)(d_(D-i)(Z-T2)-d_(D-i-1)(Z-T2)) [Z>T2].
```

For one-zero, `(T1,T2,D,r2)=(G,delta,n+r+1,r)`.
For balanced, `(T1,T2,D,r2)=(H,G,n+r,r-1)`.
Both lower partners remain. The balanced `r=0` branch has neither partner.
The first chamber is just d_D. In a single T1 chamber, the full positive
primitive is
`sum_(i=r)^D d_i(T1)d_(D-i)(Z-T1)+A_(r-1)(T1)d_(D-r)(Z-T1)`.
For the T2 chamber its cutoff is `r2+1` and its lower remaining order is
`D-r2-1`. Empty sums and all constant branches follow literally.

In the both-single-active cone put `e=T1+T2-Z`, `x=Z-T1`, `y=Z-T2`.
Then `T1=e+y,T2=e+x,Z=e+x+y`; the true direction is
`-partial_e+partial_x+partial_y`. Let `phi=d_l(e)d_i(x)d_j(y)`,
`sigma=l+i+j`, `I1=1_(l+j<=r-1)`, `I2=1_(l+i<=r2)` and
`beta=1-I1-I2`. The complete derivative coefficient for sigma<D is

```
one-zero: beta/(D-sigma)+I1/(n+1-i)[i<=n]+I2/(n-j)[j<=n-1],
balanced: beta/(D-sigma)+I1/(n-i)[i<=n-1]+I2/(n-j)[j<=n-1].
```

The derivative identity `d'_a=sum_(b=0)^(a-1)d_b/(a-b)` follows from the
complete generating series and log(1/(1-v)). The literal shifted indicator
identity `beta(l,i+q,j)+beta(l,i,j+q)-beta(l+q,i,j)=beta(l,i,j)` cancels
unchanged and shifted I1/I2 symbols at arbitrary q>=1. It yields the top
`beta/(D-sigma)` term. The two physically constant A factors provide the
other two displayed terms. Outside support coefficients are zero; a zero
denominator is never evaluated.

Only beta=-1 is adverse. It forces both partners to be active. Their denominator
differences are exactly `r-l-j>=1` and, respectively, `r+1-l-i>=1` or
`r-l-i>=1`. Each partner individually exceeds the adverse magnitude. Both stay
in the complete coefficient. The separate ALL-INDEX-INEQUALITIES.json records
these hypotheses and free-index comparisons; its finite rows are corroboration.

## The two actual merged fixed bases

On the no-return domain `j>=A`, put `v=(U-delta)_+`, `w=(U-S)_+`,
`rho=U-v-w>=0`, `S=H+G`. The complete four-G original, including its
negative-X reflected branch, becomes

```
sum_(l=0)^n d_l(w)A_(2n-l)(A+v+rho)
 -sum_(a=0)^(n-1) A_a(v+w+rho)d_(2n-a)(A)
 -sum_(a=0)^n A_a(A+w+rho)d_(2n-a)(v).
```

The fourth sector is genuinely absent at its own support. The four cones are
both-unborn, S-first, delta-first, and both-born. All gap coordinates remain in
the full ordinary field, including their zero slots.

For `T=n-k-l`, `N=2n-k-l`, its coefficient of `d_k(rho)d_l(w)` is

```
Phi = A_T(A)A_(n-1)(v)+sum_(b=T)^(n-1)A_b(v)d_(N-b)(A), T>=0;
Phi = A_N(A+v), T<0.
```

The all-index finite rectangle identity
`A_N(x+y)-sum_(a=0)^T A_a(x)d_(N-a)(y)-sum_(b=0)^(N-T-1) A_b(y)d_(N-b)(x)
=A_T(x)A_(N-T-1)(y)` is obtained using `d=A-A_previous` in the complete
Vandermonde sum. It retains the shared corner once. Restoring the omitted tail
of the actual second prefix gives the displayed Phi. All its products are
nonnegative. The disjoint index groups provide the once-only low reserve
`A_n(A)A_(n-1)(v)+A_n(w)+A_(2n)(rho)-2`. Its point and n=2 degree-one
exceptions keep their smaller actual degrees.

On the complementary far domain, write `a=j`, `d=delta`, `z=A-j>=0`.
The entire original is

```
G_(n,n-1)(d+z,a+S+z)-G_(n-1,n)(S+d+z+1,a+z-1)
-G_(n,n-1)(a+d+z+1,S+z-1)+G_(n-1,n)(a+S+d+z+2,z-2).
```

The last return is compulsory. Its expansion is
`sum_(k,l=0)^n d_k(a)d_l(d)sum_(h=0)^(n-1)d_h(S) R_(p,q,h)(z)`, where
`p=n-k,q=n-l` may be ordered by the complete coefficient symmetry. Put
`t0=p+q-n`, `M=p+q-h`, `f_i=A_i(z)d_(M-i)(z)` inside 0<=i<=M, else zero.
The full coefficient is

```
R=A_q(z)A_(p-h-1)(z)-A_(t0-h-1)(z+1)d_n(z)
   +sum_(i=t0+1)^q f_i-sum_(i=t0-h)^(q-h-1)f_i.
```

The +2/-2 telescope uses
`sum_(r=0)^e d_r(Y+2)A_(T-r)(z-2)
=sum_(i=0)^e A_i(Y)d_(T-i)(z)-A_e(Y+1)d_(T-e-1)(z)`;
its terminal cannot be omitted.

The elementary balancing step is
`A_(i+1)A_(j-1)-A_i A_j=z(1/(i+1)-1/j)A_i A_(j-1)`.
For `r=p-h-1>=0`, `v=t0-h-1>=0`, the determinant has
`r+q=v+n`, with the target pair more balanced than `(v,n)`.
Its remaining exact residual is `A_(n-1)` at v=0, or
`A_(v-1)(z+1)A_(n-1)(z)[1+(1-v/n)z]/v` at 1<=v<=n-1.
The absent branches are a positive product or zero.

The two equal-length f intervals cancel their intersection once. Pair remaining
negative indices increasingly and positive indices decreasingly. Every pair
has `j>i` and `i+j=q+t0-h<=M-1` unless both intervals are empty. For i>=0,

```
f_j-f_i= z/(M-j)(A_j A_(M-j-1)-A_i A_(M-i-1))
       +z(1/(M-j)-1/(M-i))A_i A_(M-i-1).
```

The product is more balanced and the scalar difference is nonnegative. For
i<0 its partner is just a nonnegative f_j, retaining f_M separately without
zero division. Exterior k,l coefficients vanish by complete Vandermonde;
h>=n has negative determinant indices and all remaining intervals outside
support. Every original index is paid once.

The distinct groups `(k,l)=(0,0),(1,0),(0,1),(1,1)` supply
`(1+a)(1+d)T_n(S,z)`, where
`T_n=A_(n-1)(z)product_(i=2)^(n-1)(1+(S+z)/i)(1+S+z/n)`.
At z>0 this reserve has the actual far-base degree 2n, 2n-1 or 2n-2,
according to how many of a,d are positive. At z=0 use the no-return base's
own degrees. This reserve is a complete base payment, not a replacement for
the two-positive-overlap gain.

## Balanced fixed overlap gain, both determinant levels and degree loss

For `p=L`, `b=c`, the complete character difference gives

```
Delta=Q_p(A,U)-Q_p(A+H,U-H)-Q_p(A+G,U-G)+Q_p(A+S,U-S),
Q_p(X,Y)=sum_(l=0)^p A_l(X)d_(2p+1-l)(Y), zero at Y<=0.
```

Its strict endpoint is `G_(p,p)(X+1,Y-1)`; the four terms retain the returning
contribution. The first support cone is a positive Q. The single cone has the
complete difference
`sum_(i=1)^(2p+1)d_i(H)sum_(l=max(0,p-i+1))^min(p,2p+1-i) A_l(A)d_(2p+1-i-l)(U-H)`.

In the middle cone put `e=S-U,x=U-G,y=U-H`. For each complete
`d_i(e)d_k(A)` coefficient set `N=2p+1-i-k,T=p-i-k,q=p-i`.
The entire coefficient includes the lower subtraction

```
A_N(x+y)-A_q(x+y)
 -sum_(r=0)^T A_r(x)d_(N-r)(y)-sum_(r=0)^T A_r(y)d_(N-r)(x).
```

For T<0, `N-q=p+1-k>=1` pays the index difference. For T>=0, the rectangle
identity gives `sum_(v=0)^T d_v(x)A_p(y)+sum_(v=T+1)^p d_v(x)A_(N-v)(y)`.
Pay each `d_v(x)A_(q-v)(y)` at that same v by the complete positive d tail;
keep unmatched v terms. The lower A_q term is never erased.

In the far cone put `z=U-S`, `a=A-z=j>=0`. At the complete
`d_k(a)d_i(H)d_j(G)` coefficient, let
`P=p-k`, `N=2p+1-k-i-j`, `J=i+j-2`, i,j>=1. Define the whole rectangle
sequence C(r), including exterior zeros. The uncollected four ranges reindex to

```
R=sum_t (C(P-t)-C(P-1-t)) A_t(z)d_(N-t)(z).
```

For `u>=v>=0`, the two-row determinant and increment are exactly

```
S_(u,v)=A_u A_v-A_(u+1)A_(v-1)=(u-v+1)A_u d_v/(u+1),
S_(u+1,v)-S_(u,v)=A_u d_v((u-v+2)z+v)/((u+1)(u+2)).
```

The full telescope has both levels:
`sum_(r=0)^floor(N/2) beta_r S_(N-r,r)
+sum_(r=0)^floor((N-1)/2) gamma_r S_(N-1-r,r)`, where
`beta_r=C(P-r)-C(p-r)` and `gamma_r=C(p-1-r)-C(P-r)`.
Symmetry/unimodality of the exact rectangle sequence gives beta>=0 on its
range and beta+gamma>=0 on the paired range. It does not give gamma>=0.
Pair the levels as
`beta(S_(N-r,r)-S_(N-1-r,r))+(beta+gamma)S_(N-1-r,r)`.
The even-N unmatched terminal is retained. N=0 has exactly that term, and N<0
is the full zero coefficient. These arbitrary-index ratio and interval arguments
provide the quantifier; the p1..5 complete fields validate them at finite indices.

For A>0, the merged base and fixed original have matching prior degrees. At
A=0,H,G>0,0<U<S, the merged original is `A_p(Ut)` of degree p, while the
complete fixed original has prior degree 2p+1. Every paid cone summand has an
uninterrupted positive interval, beginning by degree three; some reaches the
prior top degree. For p>=2 the complete base pays 0,1,2. For p=1 the entire
middle quadratic gain is `e^2+(3/2)e(x+y)+xy`, positive at e>0. At U=S the
actual rectangle is `A_p(Ht)A_p(Gt)` of degree 2p. The complete formal boundary
fields check these degree losses; they never assign a generic degree to a
collapsed face.

## Walls, strictness and limits of this handoff

All complete support-wall continuations vanish by their actual shifted zero
factors. The balanced initial, single and return minimum orders are n, n+1,
n+2 at arguments -1,-2,-3; n>=2 supplies their factors. Coincident masks remain
separate before their complete zeros are taken. The one-zero walls have the
corresponding full n,n+1 orders. The prefix is coefficientwise continuous; a
derivative need not agree across the knot. Both actual endpoints are full
supported prefixes. Integration of the true dimensionless derivative carries
the extra grade t, so its gain constant is zero.

In a last interior, the whole k=l=0 derivative is
`A_(n-1)(A+1)[(n+1)(A-z)d'_n+H_n]/[n(n+1)]`.
It is strict in degrees 0..2n-1 when slack,z>0; one-zero delta>0 also retains
the distinct `(1+delta*t)` multiplier. The balanced pre-return K=0 first and
single reserves reach 2n-1. In its middle cone the distinct indices
`(0,0,0),(0,n-1,0),(0,n-1,n-1),(1,n-1,n-1)` cover every degree 0..2n-1;
the third has its fully paid coefficient 3/2, including beta=-1.
For one-zero positive G,delta, the corresponding indices
`(0,0,0),(0,n,0),(1,n,n-1)` cover 0..2n. Zero G or delta branches use the
complete simplex prefix and their own prior degrees; A=delta=0 has forced
moving degree n. A=0 balanced has no returning interior, so its strict witnesses
come from earlier cones. A nonempty interval has a nonempty open chamber
subinterval. A zero interval preserves the actual fixed original's degree.

Reverse legal width steps decrease the nonnegative integer s-j to the actual
paid fixed base, preserving the specified long/tail capacities and each literal
triple. Clipping inside the extraction does not clip the physical row or content.
Root must assess and adopt this complete-original transfer and termination with
its actual scientific gate. This lane does not select an unrestricted theorem,
new original count, LR candidate, coverage increment, provider action or public
claim. Unequal b>c with two positive first overlaps remains outside the payment.
