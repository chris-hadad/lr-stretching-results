# A83: complete low-overlap originals and their paid fixed bases

**Accepted at the actual internal scientific/public review gate.** The original frozen source retains its historical proposed wording and exact byte identity.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

The
arguments below reconstruct selected Pro054 U04/U06/U07 and Pro056 U04/U05
premises. Provider records themselves remain SOURCE. This document and
OVERLAP-GENERATORS-v1.md form one complete proof; a positive auxiliary or
fixed slice alone is not the theorem.

## 1. Literal family and conventions

Let L >= 1, b >= c >= 1, h,g >= 0, h+g <= c, 0 <= j <= b, and s >= j
be integers. Take three labeled widths u,v,k >= b and L labeled widths
w_i >= b+c-h-g-j. Keep the physical lists, including every permitted zero:


```text
d=(u,v,k,s,w_1,...,w_L), e=(h,g,j,0,...,0), N=L+4,
lambda_N=d_N, lambda_i=lambda_(i+1)+d_i-e_i,
mu_i=lambda_i-d_i, nu=(sum_i d_i-b-c,b,c,0,...,0).
```

Lambda is outer. No sorting or conjugation is used. Since
lambda_i-lambda_(i+1)=d_i-e_i and mu_i-mu_(i+1)=d_(i+1)-e_i,
the overlap bounds prove both partition orders, nonnegativity and containment.
Three long widths give nu_1 >= b and the size identity is immediate.
Physical zero rows stay in the construction even where the conventional
partition notation trims trailing zeros.

Write P_s(t) for this complete LR polynomial. P_j always means its ACTUAL
fixed fourth-width-j original: reconstruct lambda,mu,nu with s=j, retaining
all other widths. It is not an unchanged-content shape operation. Let


```text
H=min(h,g), G=max(h,g), A=c-H-G, delta=b-c,
U=b-j, V=max(b-s,0), n=L+1.
```

Ordering H,G is a symmetry of the complete character below; each physical
overlap order has its own original. All statements preserve the original
stretch t and its full integer lattice. Ordinary polynomiality of stretched
LR coefficients is the established premise of Rassart, Corollary 4.2
(https://arxiv.org/abs/math/0308101). We use it only to identify complete
all-grade counts with their eventual polynomial expressions, never to infer
coefficient signs or an integral-vertex theorem.

The two families to be signed are:

* every original above with hg=0, at arbitrary b >= c;
* every original above with b=c, including h,g > 0 and the hg=0 boundary.

The unequal b>c, h,g>0 region is not included by an unstated limit.

## 2. Entire character, all affine shifts and integer chart

Use H_q= h_q(1,z,w), h_q=h_q(z,w), D=(1-z)(1-w), and
r_q=h_q-zw h_(q-1), with negative symmetric-function indices zero.
The complete three-letter Schur extraction is

    [z^(bt)w^(ct)] D(1-w/z) det(H_((lambda_i-mu_j)t-i+j)).

The exact identity D H_q=1-r_(q+1) shows why a long factor may be
replaced by 1/D. In a complete determinant term its first discrepancy is
annihilated by the target extraction: for m>bt,


```text
(1-w/z)r_m=z^m(1-w)-z^(-1)w^(m+1)(1-z).
```

Neither part can hit the requested exponents after multiplication by the
other nonnegative-power series. The long-width floors justify every such
replacement. The retained first-four-row matrix is


```text
[Z Z Z Z; B Z Z Z; 0 C Z Z; 0 E J T],
Z=1/D, B=H_(ht-1), C=H_(gt-1),
E=H_((g+j-k)t-2), J=H_(jt-1), T=H_(st).
```

Subtract its first row from its second and subtract its third row from its
fourth, or expand the complete determinant. The result is
Z(Z-B)(Z-C)(T-J): both E-dependent partners cancel. E is not assumed absent.
A detached factor's first omitted degree w_i t+1 exceeds the entire
remaining degree (b+c-h-g-j)t. Therefore


```text
P_s(t)=[z^(bt)w^(ct)] (1-w/z)r_(Ht)r_(Gt)
                          (H_(st)-H_(jt-1))/D^(L+2).       (1)
```

All scalar determinant offsets occur once. The expression clips s to b
inside the count only; the physical original still uses s.

Since r_q/D=sum_(a>=q) h_a, complete two-row Pieri extraction of (1) gives


```text
P_s(t)=sum K_L(ct+x,y;Ht,Gt),
0<=x<=delta t, 0<=y<=ct, Vt<=x+y<=Ut.                     (2)
```

The kernel counts m=L+2 two-row chains (a_i,b_i), starting at (0,0),
with b_1=0 and final (B,C), under


```text
a_i>=a_(i-1)>=b_i>=b_(i-1),
a_1>=Ht, a_2+b_2-a_1>=Gt.
```

The first and second constraints are on FULL horizontal-strip sizes. Every
integer chain occurs once by h_a h_b=sum_(r=0)^min(a,b)(zw)^r h_(a+b-2r).
Together with the full Schur extraction, this retains all original ballot
constraints. We do not claim a hive isometry from this count identity.

Nonemptiness is explicit. For B>=C and B>=Ht+Gt choose
p=max(Ht,C-Gt), q=Gt, v=p+q, and z0=B+C-v. Then h_p h_q contains h_v
and h_v h_z0 contains shape (B,C). The other free strips are zero.
In (2), choose x=max(0,(V-c)t), y=min(V,c)t. At t=0 there is one point.

The physical cap y<=ct is always part of (2). Only a full SIGNED strict
prefix may extend beyond it: (x,y) maps to (y-ct-1,ct+x+1), preserves
x+y, preserves the complete allowed x interval when x+y<Zt<=bt, and
reverses the two Weyl weights. Fixed points have zero weight. Thus the
extension cancels in complete pairs, not by discarding a dominant partner.

## 3. Prior degree and lattice, including all collapsed faces

The generic kernel has 2L+1 coordinates. For 0<C<B and Gt<B, take
Ht<a_1<min(B,B+C-Gt), choose b_2 just below min(a_1,C) and a_2 just
below B, and interpolate strictly between these and the final rows. The
strict inequalities have a rational relative interior of that dimension.
At B=C>0 only the additional final equality a_(m-1)=B is forced, giving
2L. At C=0 the lower chain vanishes and the increments give an (L+1)-simplex
if B>Ht+Gt, otherwise a point. At Gt=B, necessarily H=0, the entire
first-strip constraint forces a_2=B, b_2=a_1 and all later upper entries B;
the residual weak chain has L coordinates and count A_L(C), or one at C=0.
The reversed physical overlap order has the same complete character and count.

Every affine equality eliminates a coordinate with coefficient one. In the
residual chart, a fixed band eliminates y=Ut-x; the upper corner fixes both
x and y at integral slopes; the rectangle fixes a_(m-1)=ct. Forced-strip
and simplex branches use ordinary integer increments. Thus the difference
lattice is saturated in each branch; no residue or parity coset is selected.
Boundedness and a rational relative-interior box give exact growth t^d.
Polynomiality then establishes these PRIOR actual degrees, before arithmetic:

| Ordered guard | d |
| --- | --- |
| U=0 | L+1 if A>0, otherwise 0 |
| delta>0, U>V | 2L+3 |
| delta>0, 0<U=V<b | 2L+2 |
| delta>0, U=V=b | 2L+1 |
| delta=0, A+H>0, U>V | 2L+2 |
| delta=0, A+H>0, 0<U=V<c | 2L+1 |
| delta=0, A+H>0, U=V=c | 2L |
| delta=0, A=H=0, U>V | L+1 |
| delta=0, A=H=0, U=V>0 | L |

For delta>0, an open moving rectangle band adds two dimensions; a fixed
noncorner band adds one; the upper corner adds none. For delta=0, x=0
and the preceding kernel cases give the other rows. These observations also
prove no branch has larger dimension. The table is ordered: U=0 is handled first.

## 4. Complete fixed bases with one zero overlap

In this section H=0, so A=c-G. Put
A_r(x)=prod_(i=1)^r(1+x/i), d_r(x)=prod_(i=0)^(r-1)(x+i)/r!,
A_0=d_0=1, negative indices zero. Define the supported convolution


```text
G_(a,beta)(X,Y)=sum_(v=max(0,-X))^Y A_a(X+v)A_beta(Y-v).
```

It is zero if Y<0 or X+Y<0. Its exact branches are


```text
G_(a,beta)(X,Y)=sum_(i=0)^a d_i(X)A_(a+beta+1-i)(Y), X>=0;
G_(a,beta)(X,Y)=A_(a+beta+1)(X+Y), X<0<=X+Y.              (3)
```

The first formula is rising addition plus complete Vandermonde; for the second
shift v by -X first. Every endpoint is retained. Complete supported sectors
on a fixed ray have eventual polynomial forms; their WHOLE sum is P_j.

The complete fixed base, with both reflected and returned sectors, is


```text
P_j=G_(n,n-1)((U-G)t,ct)
   -G_(n-1,n)(Ut+1,At-1)
   -G_(n,n-1)((A+delta)t+1,(U-delta)t-1)
   +G_(n-1,n)(bt+2,(U-G-delta)t-2).                       (4)
```

### 4a. Near side j>=A

Let v0=(U-delta)_+, w0=(U-G)_+, rho=U-v0-w0>=0. The last sector of
(4) is absent on this side. With T=n-k-l and M=2n-k-l set


```text
Phi_(n;k,l)(a,b)=A_T(a)A_(n-1)(b)
            +sum_(r=T)^(n-1)A_r(b)d_(M-r)(a), T>=0;
            =A_M(a+b), T<0.
```

Then the ENTIRE base equals


```text
P_j=sum_(k=0)^(2n) d_k(rho t)
         sum_(l=0)^min(n,2n-k) d_l(w0 t) Phi_(n;k,l)(At,v0 t). (5)
```

To verify (5), reduce (4), on its actual supports, to
sum_(l=0)^n d_l(w0 t)A_(2n-l)((A+v0+rho)t)
minus sum_(a=0)^(n-1)A_a(Ut)d_(2n-a)(At)
minus sum_(a=0)^n A_a((A+w0+rho)t)d_(2n-a)(v0 t).
Expand rho and w0. Each coefficient is the full finite rectangle identity


```text
A_M(a+b)-sum_(i=0)^T A_i(a)d_(M-i)(b)
   -sum_(j=0)^(M-T-1) A_j(b)d_(M-j)(a)
     =A_T(a)A_(M-T-1)(b), 0<=T<M.                       (6)
```

Writing d=A-A_previous and telescoping proves (6), with the shared corner
once. Restore the missing positive tail j=T,...,n-1 to obtain Phi.
All factors in (5) are nonnegative in the ordinary basis.

Every nonzero summand has an uninterrupted positive degree interval beginning
by degree three. Some summand reaches the prior actual degree, so it pays
all degrees three and above. Three DISJOINT index groups supply the low reserve


```text
P_j >=_coef A_n(At)A_(n-1)(v0 t)+A_n(w0 t)+A_(2n)(rho t)-2. (7)
```

The constant is one. The linear and quadratic are strict except the point
A=U=0 and the actual degree-one case n=2,A=w0=rho=0,v0>0. There (5)
is exactly A_1(v0 t), so no quadratic is claimed.

### 4b. Far side j<A

Put a=j, d=delta, z=A-j>0 and S=G. Thus c=a+S+z, b=a+S+d+z.
Equation (4), including its return, becomes

    G_(n,n-1)((d+z)t,(a+S+z)t)
    -G_(n-1,n)((S+d+z)t+1,(a+z)t-1)
    -G_(n,n-1)((a+d+z)t+1,(S+z)t-1)
    +G_(n-1,n)((a+S+d+z)t+2,zt-2).                           (8)

Suppress t and set Y=S+z. Its complete coefficient in d_k(a)d_l(d),
0<=k,l<=n, with M=2n-k-l, is


```text
Q=sum_(r=0)^(n-l)d_r(z)A_(M-r)(Y)
  -sum_(r=0)^(n-1-l)A_r(Y)d_(M-r)(z)
  -sum_(r=0)^(n-k-l)A_r(z)d_(M-r)(Y)
  +sum_(r=0)^(n-1-k-l)d_r(Y+2)A_(M-r)(z-2).              (9)
```

For k>n or l>n, complete Vandermonde cancels the remaining ranges, giving zero.
The returning convolution telescopes by


```text
sum_(r=0)^e d_r(Y+2)A_(M-r)(z-2)
   =sum_(i=0)^e A_i(Y)d_(M-i)(z)-A_e(Y+1)d_(M-e-1)(z).  (10)
```

Here M-e>=2 whenever used. It follows from d_r(Y+2)=sum_(i=0)^r A_i(Y)
and A_m(z-2)=d_m(z)-d_(m-1)(z). In particular the final endpoint survives.
The coefficient Q is symmetric in p=n-k and q=n-l; assume p>=q.
Expand it in d_h(S), put tau=p+q-n and M0=p+q-h, and let
f_i=A_i(z)d_(M0-i)(z), zero outside 0<=i<=M0. The exact remaining coefficient is


```text
R=A_q(z)A_(p-h-1)(z)-A_(tau-h-1)(z+1)d_n(z)
  +sum_(i=tau+1)^q f_i-sum_(i=tau-h)^(q-h-1) f_i.        (11)
```

Equations (9)-(10) and one finite difference of d_r prove (11). At h>=n all
terms cancel or vanish; every exterior-zero index is part of the convention.

Two elementary product identities pay the WHOLE expression. For i<j,


```text
A_(i+1)A_(j-1)-A_i A_j
   =z(1/(i+1)-1/j)A_i A_(j-1)>=_coef0.                  (12)
```

Thus fixed-total products increase toward balance. In the determinant of
(11), write r=p-h-1 and v=tau-h-1=r+q-n. If r<0 both terms vanish;
if v<0 only a positive product remains. Otherwise balancing gives
A_q A_r>=A_v A_n, and


```text
A_v A_n-A_v(z+1)d_n=A_(n-1), v=0;
  =A_(v-1)(z+1)A_(n-1)(z)[1+(1-v/n)z]/v, 1<=v<=n-1.  (13)
```

The two intervals in (11) have equal length. Cancel their intersection; pair
remaining negative indices increasingly with positive indices decreasingly.
Each pair has i<j and i+j=q+tau-h<=M0-1, unless i is an exterior zero.
For supported pairs,


```text
f_j-f_i=z/(M0-j)[A_j A_(M0-j-1)-A_i A_(M0-i-1)]
  +z[1/(M0-j)-1/(M0-i)]A_i A_(M0-i-1)>=_coef0.         (14)
```

The first bracket is balanced by (12). The exceptional f_(M0) is never divided
by zero. This pays every original occurrence exactly once, at all n.

Four distinct (k,l)=(0,0),(1,0),(0,1),(1,1) in (9) have the same coefficient


```text
T_n(S,z)=A_(n-1)(z) prod_(i=2)^(n-1)(1+(S+z)/i)(1+S+z/n).
```

One can verify this by (10) and A_m(Y)+A_(m-1)(Y+1)=A_m(Y+1), keeping
l=n's zero index. They give the disjoint reserve


```text
P_j >=_coef (1+at)(1+dt)T_n(St,zt).                     (15)
```

Its degree is 2n if a,d>0, 2n-1 if precisely one is positive, and 2n-2 if
both vanish. These are exactly the prior far-side fixed degrees. Since z>0,
every factor has positive slope: all degrees through the actual degree are
strict. At z=0 use the near side and its own degree. Both actual fixed bases
are now paid, with no signed return omitted.

## 5. Actual balanced fixed bases with two positive overlaps

Assume b=c and H,G>0. P0 denotes the separately constructed merged fixed
original with overlaps (0,H+G,j,0,...), SAME widths and content. Section 4
pays it on both sides of j=A, with its own degree. This is not yet P_j.
Let p=L, S=H+G, A=c-S. The whole character difference
r_H r_G-r_(H+G)=zwD h_(H-1)h_(G-1) yields


```text
Delta=P_j-P0=Q_p(At,Ut)-Q_p((A+H)t,(U-H)t)
                -Q_p((A+G)t,(U-G)t)+Q_p((A+S)t,(U-S)t),
Q_p(X,Y)=sum_(l=0)^p A_l(X)d_(2p+1-l)(Y), Y>=0;
        =0, Y<=0.                                     (16)
```

The displayed polynomial is zero at Y=0. For each R=0,H,G,S, the exact
supported finite sector before summation is
G_(p,p)((A+R)t+1,(U-R)t-1). It follows by expanding the full character's
1/(z-w); the strict endpoint is present once. Thus (16) retains every
returning sector and is an all-grade original identity.

Order H<=G using complete character symmetry. For U<=H, only Q_p(A,U)
remains. For H<=U<=G, v=U-H and full cancellation gives


```text
Delta=sum_(i=1)^(2p+1)d_i(H)
   sum_(l=max(0,p-i+1))^min(p,2p+1-i) A_l(A)d_(2p+1-i-l)(v). (17)
```

For G<=U<=S put e=S-U, x=U-G, y=U-H. Expanding in d_i(e)d_k(A),
put M=2p+1-i-k, T=p-i-k, q=p-i. The full residual is


```text
Phi=A_M(x+y)-A_q(x+y)
   -sum_(r=0)^T A_r(x)d_(M-r)(y)-sum_(r=0)^T A_r(y)d_(M-r)(x). (18)
```

If T<0, A-index monotonicity pays it, since M-q=p+1-k>0. Otherwise (6)
rewrites the first term minus both prefixes as


```text
sum_(v=0)^T d_v(x)A_p(y)+sum_(v=T+1)^p d_v(x)A_(M-v)(y).
```

Each term of A_q(x+y)=sum_(v=0)^q d_v(x)A_(q-v)(y) is paid at the SAME
v by the larger A index. The difference is a full positive d-tail. Unmatched
terms stay positive.

For U>=S put z=U-S>=0, a=A-z=j>=0. Expand in d_k(a)d_i(H)d_j(G),
0<=k<=p and i,j>=1; let P=p-k, M=2p+1-k, N0=M-i-j, J=i+j-2.
Terms with N0<0 vanish. Set `C(r)=[v^r](1+...+v^(i-1))(1+...+v^(j-1))`,
zero outside 0..J. Complete range collection yields


```text
R=sum_t [C(P-t)-C(P-1-t)]A_t(z)d_(N0-t)(z).              (19)
```

For u>=v>=0 define the whole determinant


```text
S_(u,v)=A_u A_v-A_(u+1)A_(v-1)=(u-v+1)A_u d_v/(u+1).
S_(u+1,v)-S_(u,v)
   =A_u d_v[(u-v+2)z+v]/[(u+1)(u+2)]>=_coef0.           (20)
```

Telescoping A_t A_(D-t)=sum_(r=0)^min(t,D-t)S_(D-r,r) in both parts
of d_(N0-t)=A_(N0-t)-A_(N0-t-1) gives two complete levels, with weights


```text
beta_r=C(P-r)-C(p-r), gamma_r=C(p-1-r)-C(P-r).
```

The full rectangle sequence is symmetric unimodal, including exterior zeros.
On the actual first-level range beta_r>=0; on the paired range
beta_r+gamma_r>=0. Indeed P+p-2r=N0+J+1-2r>=J+1 and
2p-1-2r>=p-P+J+1>=J+1. Pair complete levels as


```text
beta_r[S_(N0-r,r)-S_(N0-1-r,r)]
   +(beta_r+gamma_r)S_(N0-1-r,r)>=_coef0.                (21)
```

The even-N0 unmatched terminal remains. N0=0 keeps it; negative N0 is zero.
Individual gamma weights need not be positive. This proves the full fixed
overlap gain nonnegative across all four bands and every wall.

Strictness needs a separate degree check. At U=0 the whole original is
A_(L+1)(At), or one at A=0. For A>0 the merged and unmerged fixed degrees
agree, and P0 supplies strictness. At A=0,HG>0,U>0, P0=A_p(Ut) has degree p.
If U=S, the ENTIRE rectangle original is A_p(Ht)A_p(Gt), degree 2p.
For 0<U<S, the unmerged degree is 2p+1. Every nonzero paid summand in the
first three cones has a consecutive degree interval beginning by degree three;
a top-degree summand thus pays degrees 3..2p+1. The base covers 0,1,2 for
p>=2. For p=1, the first two cones need at most two d factors; in the middle,


```text
[t^2]Delta=e^2+(3/2)e(x+y)+xy>0, since e=S-U>0.
```

The base pays degrees zero and one and the top summand pays degree three.
This closes every degree-loss and point boundary of the ACTUAL fixed original.

## 6. Dependencies and verification boundary

The complete source compilation is the authenticated A82 Pro056 object
0b2365881c48fc41444697bd3bfe7e0616aacad6482c9b0222ad831d6e02ef17.md,
sections U04-03, U04-02 v2, U06-01 v2, U07-01 v2 and U07-02 v2. The root read
all these sections, rechecked the full determinant, integer chart, degree
branches, finite telescopes and disjoint payments above. Pro056 U04/U05 supplies
the operation joined in the companion proof; its provider claims stay SOURCE.
The trusted independent arithmetic handoff and actual Astra gate determine
acceptance. Finite coefficient panels corroborate identities, never supply
unbounded indices. No new original or LR backend call is asserted here.
