# A83: two complete low-overlap generating families

**Accepted at the actual internal scientific/public review gate.** The original frozen source retains its historical proposed wording and exact byte identity.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Original geometry, lattice, the nine ordered actual-degree branches and both
kinds of actual fixed base are proved in ORIGINALS-AND-BASES-v1.md. This
companion proves the ENTIRE moving operation. Its provenance is Pro056 U04's
whole two-factor chain and U05's balanced transfer, with the full Pro054
original/base dependencies reconstructed in the companion. No provider program
is executed and no source statement is adopted by a name or finite panel.

## 1. The theorem and complete expression to be paid

Use the literal parameters and originals of the companion. For every L>=1,
b>=c>=1 and its physical width/overlap/capacity conditions, P_s is strictly
ordinary-coefficient-positive from zero through its actual degree whenever


```text
hg=0, or b=c.                                         (T)
```

There is no upper bound on L, any permitted parameter, or the fourth width s.
For either family the full operation from its own fixed original satisfies


```text
P_s-P_j >=_coef 0.                                    (G)
```

If U>V, the gain is strict in every positive degree through the moving
original's prior actual degree, with constant zero. If U=V, it is identically
zero and the actual fixed base retains its own degree. In particular balanced
two-positive-overlap moving originals have degree 2L+2 even on A=0; their
merged comparisons can have smaller degree and are not used beyond it.

Let Q(Z;t) be the entire strict prefix x+y<Zt of the complete signed kernel
in (2) of the companion, for 0<=Z<=b. The signed cap involution applies to
both full prefixes, so the exact original identity is


```text
P_s=P_j+Q(U)-Q(V).                                    (1)
```

P_j is included once. Every endpoint, constant term and supported mask stays
until this entire difference is formed. The full general eight-mask formula is


```text
Q(Z)=sum_(etaH,etaG,etaD in {0,1}) (-1)^k
        F_(n-m,n-1+m)((A+R)t+k,(Z-R)t-k-1),
m=etaH+etaG, k=m+etaD,
R=etaH H+etaG G+etaD delta,
F_(a,beta)(X,Y)=sum_(v=0)^Y(v+1)A_a(X+v)A_beta(Y-v).    (2)
```

Actual support Z>R is imposed before continuation. Each labeled occurrence
remains at coincident thresholds. The once-only scalar offsets k,-k-1 are
not stretched. Equation (2) follows by retaining both Weyl terms and the
complete finite endpoint summation in the original extraction. Alternatively,
expand the two r factors and the fourth-width difference directly in (1) of
the companion and sum the whole residual cap, including its reflected partners.

When one factor has width zero, pair its TWO labeled occurrences using


```text
F_(a,beta)(X,Y)-F_(a,beta)(X+1,Y-1)=G_(a,beta)(X,Y).     (3)
```

Reindex the second sum by v+1: its weight becomes v, while the first weight
is v+1. The v=0 endpoint remains once. At Y=0 the second sum is empty.
Thus specialization pairs full shifted sectors rather than deleting a mask.

For hg=0 the complete four-sector prefix is


```text
Q=G_(n,n)(At,Zt-1)
 -G_(n-1,n+1)((A+G)t+1,(Z-G)t-2)
 -G_(n,n)((A+delta)t+1,(Z-delta)t-2)
 +G_(n-1,n+1)((A+G+delta)t+2,(Z-G-delta)t-3).            (4)
```

For b=c and H,G>0 it is


```text
Q=G_(n,n-1)(At,Zt-1)
 -G_(n-1,n)((A+H)t+1,(Z-H)t-2)
 -G_(n-1,n)((A+G)t+1,(Z-G)t-2)
 +G_(n-2,n+1)((A+H+G)t+2,(Z-H-G)t-3).                 (5)
```

The fixed originals for (4) and (5) were separately paid in the companion.
We now sign the complete physical derivative in every chamber, then integrate
it over [V,U]. This is not positivity inferred from a changing number of fibers.

## 2. One proof for both pre-return payments

The first three sectors of (4) and (5) admit a useful common description.
Take (a,b0,eta)=(G,delta,1) for (4), and (H,G,0) for (5). Expand Q in
d_K(A), K=0,...,n. Set r=n-K, D0=n+r+eta and


```text
tau_1=r-1, tau_2=r-1+eta.
```

Before the double return, the COMPLETE coefficient is


```text
q_r(Z)=d_(D0)(Z)
  -sum_(i=0)^tau_1 A_i(a)[d_(D0-i)(Z-a)-d_(D0-i-1)(Z-a)] [Z>a]
  -sum_(i=0)^tau_2 A_i(b0)[d_(D0-i)(Z-b0)-d_(D0-i-1)(Z-b0)] [Z>b0]. (6)
```

The second lower-order term in every bracket is compulsory. This follows by
full G summation, d_i(a+1)=A_i(a), and A_m(w-2)=d_m(w)-d_(m-1)(w).
An empty cutoff is literal; r=0 does not acquire a negative-index term.

Before the first birth q_r=d_(D0)(Z). If only the a sector is active and
x=Z-a, the complete telescoping expansion is


```text
q_r=sum_(i=r)^(D0)d_i(a)d_(D0-i)(x)+A_(r-1)(a)d_(n+eta)(x). (7)
```

If only the b0 sector is active, y=Z-b0 gives


```text
q_r=sum_(i=r+eta)^(D0)d_i(b0)d_(D0-i)(y)
                           +A_(r-1+eta)(b0)d_n(y).     (8)
```

Both follow by A_i=sum_(j=0)^i d_j and cancellation of the whole shared
initial range. Their physical derivatives act on x or y alone and are
nonnegative in every ordinary degree. Every terminal stays in (7)-(8).

In the both-single-active chamber put


```text
e=a+b0-Z, x=Z-a, y=Z-b0,
a=e+y, b0=e+x, Z=e+x+y.
```

The physical direction at fixed a,b0 is
L=-partial_e+partial_x+partial_y. For phi=d_l(e)d_i(x)d_j(y),
sigma=l+i+j, let


```text
I1=1_(l+j<=r-1), I2=1_(l+i<=r-1+eta), beta=1-I1-I2.
```

Complete rising addition rewrites (6) as its top beta field plus the TWO
lower products A_(r-1)(a)d_(n+eta)(x) and A_(r-1+eta)(b0)d_n(y).
The indicator identity
beta(l,i+q,j)+beta(l,i,j+q)-beta(l+q,i,j)=beta(l,i,j), q>=1,
and d'_a(v)=sum_(b=0)^(a-1)d_b(v)/(a-b) give the exact full derivative
coefficient, for sigma<=D0-1,


```text
beta/(D0-sigma)
   +I1/(n+eta-i) [0<=i<=n+eta-1]
   +I2/(n-j) [0<=j<=n-1].                             (9)
```

No outside total degree or zero denominator is suppressed. The lower products
have total derivative degree at most D0-2. If beta=-1, both partners are
present, and


```text
(D0-sigma)-(n+eta-i)=r-l-j>=1,
(D0-sigma)-(n-j)=r+eta-l-i>=1.                         (10)
```

Both denominators are positive. Each partner alone is larger than the adverse
magnitude; both remain in the whole payment. If beta>=0, every term is already
nonnegative. Equations (7)-(10) prove the full pre-return sign at all n,r.
Multiplication by d_K(At) and the physical grade factor t preserves it.

## 3. Complete last-chamber dual extraction

Let X=(1-u)^(-1), Y=(1-v)^(-1), where u,v here are auxiliary variables.
For nonnegative integer q define R_q(X,Y)=h_q(X,Y)-h_(q-1)(X,Y).
In the GENERAL last chamber Z=H+G+delta+z, capacity Z<=b gives
A=x+z with x=b-Z>=0. The complete dual identity is


```text
Q=[u^n v^(n+1)](v-u)X^(A+2)Y^z R_H R_G h_delta.        (11)
```

For clarity, it retains the finite upper endpoint of every F sector. Its
full generating function, with x0=1-u,y0=1-v, is


```text
sum_(a,b>=0)F_ab(X0,Y0)u^a v^b
  ={x0^(1-X0)y0^(-Y0-1)
   +[(Y0+1)(u-v)+(u-1)]x0^(-X0-Y0-1)}/(u-v)^2.       (12)
```

Multiply each of (2)'s masks by (u/v)^m and extract u^n v^(n-1).
All masks have X0+Y0=A+Z-1. Their ENTIRE second numerator sums to
(delta+1)(u-v)v^(-2)x0^(-A-Z); the requested v coefficient vanishes
because n-1=L>=1. The first numerators factor into the three complete
finite differences for H,G,delta; cancelling their common (u-v)^2 and
using reciprocal variables gives (11). No individual baseline is discarded.

For (4), H=0 and only R_G h_delta remains. For (5), delta=0 and only
R_H R_G remains. These are the two specializations proved here. The physical
derivative changes z at FIXED A before setting A=x+z: it inserts log(Y).
It is partial_z-partial_x in legal coordinates, with the further factor t
on a homogeneous LR ray. Holding x fixed gives the wrong operation.

Write r_k(u,v)=h_k(u,v)-uv h_(k-1)(u,v). The full finite rising expansions are


```text
R_G=sum_(k>=0)d_k(G)r_k,
h_delta=sum_(ell>=0)d_ell(delta)r_(max(ell-1,0)).        (13)
```

Indeed R_G=(1-u)(1-v)sum_(j>=0)A_j(G)h_j(u,v), and
sum_(j>=k)h_j=r_k/((1-u)(1-v)). The analogous A_(j+1)(delta)
identity proves the second formula. Physical ell=0 and ell=1 are DISTINCT
equal-coefficient occurrences. The identity
(v-u)r_k=v^(k+1)(1-u)-u^(k+1)(1-v) proves that every index k>n vanishes
in the requested rectangle, even after multiplication by the other series.
Thus both specializations reduce to complete coefficients


```text
C_(n;k,l)=[u^n v^(n+1)](v-u)X^(A+2)Y^z r_k r_l,
0<=k,l<=n.                                           (14)
```

All constant coefficients stay in Q at both endpoints.

## 4. Full two-r chain, all indices and every birth term

Put


```text
q_(a,m)=A_a(A)d_(m+1)(z)
          -A_m(A+1)[d_(a+1)(z)-d_a(z)], 0<=m<=a-1;
q_(a,-1)=A_a(A).
```

Invalid indices are zero; q_(0,-1)=1. Let D_(a,m) denote the derivative
at fixed A, so D_(a,-1)=0. The complete product identity
r_k r_l=r_(k+l)+uv(1-u)(1-v)h_(k-1)h_(l-1), followed by the full
finite two-row Pieri sum and both endpoints of (v-u)h_j, gives


```text
C_(n;k,l)=q_(n,n-k-l-1)
  +sum_(i=0)^(min(k,l)-1)
       [q_(n-1-i,n+i-k-l)-q_(n-1-i,n+i-k-l-1)].         (15)
```

It is the whole chain whose derivative must be paid. Individual adjacent
D differences can be negative and are not premises of the following proof.

By symmetry take k<=l, p=n-k, q=n-l and e=n-k-l. If q=0 the derivative
vanishes, including the constant C_(n;n,n)=1. If q>=1,e<=0, reindex ALL
nonzero terms of (15) to


```text
sum_(r=0)^(q-1)[D_(p+q-1-r,r)-D_(p+q-1-r,r-1)].        (16)
```

This is the canonical e'=1 chain at n'=p+q-1,k'=q-1,l'=p-1.
Its n'=1 endpoint is D_(1,0)=x+3/2. Hence it suffices to pay e>=1,
without omitting the constants that differentiated to zero.

For 1<=M<=a define


```text
R_(a,M)(v)=(M-1)!/a! (v+1)prod_(r=M+1)^a(v+r),
K_(a,M)=A_a(A)-A_(M-1)(A+1)R_(a,M)(z),
S_(a,M)=K_(a,M)d'_M(z),
B_(a,M)=R_(a,M)(z)d'_M(z)-d'_(a+1)(z)+d'_a(z).
```

The EXACT split is


```text
D_(a,M-1)=S_(a,M)+A_(M-1)(A+1)B_(a,M).                 (17)
```

Since A_a(A)=A_(M-1)(A+1)R_(a,M)(A), K is a positive product difference
after A=x+z. More usefully, for M<=a-1,


```text
K_(a,M)-K_(a-1,M)
  =z K_(a-1,M)/a+x A_(a-1)(A)/a>=_coef0.              (18)
```

Define the complete deleted-factor polynomial


```text
H_r(z)=1/r! sum_(i=0)^(r-1)(2r+1-i)
                           prod_(0<=v<r,v!=i)(z+v).
```

All its coefficients are nonnegative. It equals (z+2r+1)d'_r-r d_r.
With w_r=(r-1)!d'_r the exact birth recurrence is
(z+r+1)w_r-w_(r+1)=(r-1)!H_r/(r+1). Telescoping every r=M,...,a-1
and retaining the last endpoint gives


```text
B_(a,M)=(z+1)/a! sum_(r=M)^(a-1)
           (r-1)!/(r+1) prod_(v=r+2)^a(z+v)H_r
           +H_a/[a(a+1)].                            (19)
```

The terminal coefficient differs from the nonterminal one. At a=M=1 it
is 3/2, which checks the canonical smallest endpoint.

The ENTIRE S part of the canonical chain (15) reindexes to


```text
S_(p,q)+sum_(i=0)^(k-1)
              [S_(n-i,e+i)-S_(n-1-i,e+i)].             (20)
```

Equation (18), multiplied by positive d'_M, pays every increment and the
terminal is positive. This pays all powers of the legal slack x, not only x=0.

For the remaining B part, collect each WHOLE H_r coefficient from (19).
No atom occurs for r<e. If r>=q, each correction either contains both
occurrences, whose multiplier is
A_(e+i)(A+1)-A_(e+i-1)(A+1)=A_(e+i)(A)>=0, or neither.
This also applies at its distinct terminal. The initial occurrence is positive.

For e<=r<q, the atom disappears from the positive correction at i=r-e.
Set b=n+e-r-1; then b>=p>=q>r, so every relevant occurrence is nonterminal.
Factor (z+1)(r-1)!H_r/(r+1) and put f_s=prod_(v=r+2)^s(z+v)/s!.
The ENTIRE remaining coefficient is


```text
A_(e-1)(A+1)f_n+sum_(j=e)^(r-1)A_j(A)f_(n+e-j-1)
                                -A_(r-1)(A+1)f_b.
```

The exact A telescope rewrites it as


```text
A_(e-1)(A+1)(f_n-f_b)
  +sum_(j=e)^(r-1)A_j(A)(f_(n+e-j-1)-f_b).              (21)
```

Every index s>=b, and f_s=f_b prod_(v=b+1)^s(1+z/v), so each difference
is nonnegative. Every disappearing adverse atom is paid ONCE by its initial
and earlier partners, with the complete terminal and all degrees retained.
Equations (16)-(21) prove


```text
partial_z C_(n;k,l)(x+z,z) >=_coef0                    (22)
```

for every n>=1 and 0<=k,l<=n, with derivative at fixed A. Equations (11)-(14)
therefore sign the entire last chamber of both families, including the physical
factor t and both ell=0,1 occurrences in the one-zero family.

## 5. Birth walls, complete endpoints and strictness

Every born G sector in (4)-(5) has zero complete continuation at its support
wall: after full G summation its remaining A order is at least n, n+1 or
n+2, while its scalar argument is respectively -1,-2,-3. Since n>=2 a zero
factor remains. The actual sector is absent at that equality. Distinct masks
stay distinct at coincident walls. Thus all coefficients of Q are continuous
across the full support decomposition; derivatives may jump.

On each open chamber (6)-(22) signs the physical derivative at all ordinary
degrees. Rational physical comparison parameters may be cleared together;
polynomial identities then extend to real chamber coordinates. Integrating
coefficient by coefficient across [V,U], split only at genuine walls, proves
(1)'s full gain nonnegative. Constant terms in either endpoint were never
removed merely because their derivative was zero.

Strictness also keeps the actual degree. For the balanced H,G>0 family the
K=0 branch has r=n,D0=2n. The first open chamber has d'_(2n)(Z), strict
through degree 2n-1. In a singly active chamber, the distinct terms
d_n(H)d'_n(x) and A_(n-1)(H)d'_n(x) cover degrees 1..2n-1 and degree zero.
In the both-active chamber the full coefficient (9) is positive at


```text
(l,i,j)=(0,0,0),(0,n-1,0),(0,n-1,n-1),(1,n-1,n-1).
```

These four complete terms cover every degree 0..2n-1 even at n=2. At the
third term the negative beta is paid by both lower partners; its coefficient
is 3/2. At the fourth, both indicators vanish and the coefficient is one.
In a last-chamber interior, the k=l=0 term has


```text
D_(n,n-1)=A_(n-1)(A+1)
             [(n+1)x d'_n(z)+H_n(z)]/[n(n+1)].         (23)
```

For x,z>0 its H_n part covers 0..2n-2 and the slack part reaches 2n-1.
If A=0 there is no last-chamber interior, and the earlier witnesses suffice.
The physical factor t gives strict gain at every degree 1..2n.

For the one-zero family with G,delta>0, the analogous first and singly active
terms in (7)-(8) cover 0..2n. In the both-active chamber the actual positive
occurrences (0,0,0),(0,n,0),(1,n,n-1) cover the same full interval. In the
last chamber BOTH ell=0 and ell=1 give the disjoint witness
(1+delta t)D_(n,n-1)(At,zt), covering 0..2n before the physical t.
When G=0,delta>0, the earlier full prefix is A_n(At)d_(n+1)(Zt), with
A=c>0; its derivative has the same strict range, and (23) pays the last part.
When delta=0,A>0, the earlier full prefix is A_n(At)d_n(Zt), and (23)
alone gives gain degrees 1..2n. When delta=A=0 the full prefix is d_n(Zt),
so the forced moving degree is n. These exhaust the companion's moving branches.
Every nonempty [V,U] has an open subinterval in one applicable chamber,
possibly below a clipping endpoint. Integrating its strict witnesses establishes
strictness; other chambers add nonnegative quantities. At U=V the gain is zero.

The companion pays the ACTUAL P_j at its actual degree, including both fixed
one-zero bases and the full balanced overlap gain/degree-loss payment. Joining
it ONCE to (1) proves (T) and (G) at the entire stated domain.

## 6. Composable operation, reach and falsifiers

Every reverse step s->s-1 with s>j preserves all physical floors and decreases
the nonnegative integer s-j. The full endpoint formula gives P_s=P_b when
s>b, while the literal shapes and contents remain distinct. Thus even the
clipped equal-count steps terminate; the rest compose through their actual
intermediate originals to the paid s=j base. This is a complete generating
cover of the UNION hg=0 OR b=c, under the original capacity hypotheses.
It is not a proof for the remaining unequal-row two-positive-overlap originals.

That remaining domain has all eight masks, the extra h_delta factor in (11),
a complete three-r extraction and further partially active chambers. A full
last-chamber theorem alone would still need those earlier masks and the actual
fixed base. Negative adjacent pieces or sufficient weights are not a negative
ordinary LR original. Deficient capacities, h+g>c, extra interacting blocks,
arbitrary shapes/content, whole rank seven and unrestricted KTT remain open.

Trusted verification reconstructs entire expressions by independent algebraic
paths, includes meaningful omission and wrong-direction controls, and retains
actual finite/infinite distinctions. Exact vectors and literal counts already
present in SOURCE are reuse if joined; no newly unused oracle evidence is
invented. Acceptance is governed only by the actual A83 scientific gate and
its full CHECKS. The companion and this proof retain every physical row,
label, lattice, prior degree, scalar shift, birth, endpoint and compensation.
