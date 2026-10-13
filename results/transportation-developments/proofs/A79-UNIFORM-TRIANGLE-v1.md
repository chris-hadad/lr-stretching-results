# A79: complete positivity for one supported triangle at arbitrary column count

Curated mathematical proof from **A79**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root reconstruction and extension of completed Pro053 U03, U05, U11 and U12.
 This draft
is not an adoption receipt. Pro054/Pro055 records are separate source evidence and are not premises of this derivation.

## 1. Complete original and claim

Fix positive integer rows (A,B,R), with 0 < A <= B, and a labeled physical
column vector e of total A+B+R. Retain every physical zero in its position.
There are N=n+1 >= 4 positive columns, every one at least A. Form the graph of
ALL pairs with e_i+e_j < A+B. Suppose this graph consists of exactly one
triangle and isolated vertices. Then the entire ordinary stretching polynomial
satisfies


```text
P_e(t) >= K_n(At)
       >= a_(2n-1)(At)[1+(n-1)At/(2n)],
a_j(z)=binom(z+j,j), d_j(z)=binom(z+j-1,j), a_0=d_0=1,
K_n(x)=a_n(x)^2-(n+1)d_(2n)(x).
```

All comparisons are coefficientwise in ordinary powers. Every coefficient is
strict through the actual degree 2n. There is no bound on n, triangle widths,
their gaps, central excess, pair/triple height, or isolated-column excess.
The complete surplus over K_n is strict in every nonconstant degree for a
genuine triangle. This does not cover extra overlap edges, larger cliques,
below-A columns, arbitrary transportation, general LR shapes or unrestricted KTT.

The literal lambda-outer realization, with L physical columns, M=A+B+R and
C_j=sum_(i=j)^L e_i, is


```text
lambda=(M+B+R,M+R,C_1,...,C_L),
mu=(M,M,C_2,...,C_L,0), nu=(M,B+R,R).
```

These are partitions, lambda contains mu, and their size difference is |nu|.
Ballot order forces B+R ones in the first skew row. Its R-position overlap
with the second row and column strictness force R twos there. The disjoint
tail intervals (C_(j+1),C_j] have weak fillings determined exactly by each
table column's counts of 1,2,3. The buffers protect every subsequent ballot
prefix. This is an all-grade bijection in both directions, including the unique
empty grade zero and empty physical intervals. Each changed endpoint has its
own literal triple and explicitly changed third row.

The strictly positive real table r_i e_j/M on positive support proves relative
dimension 3N-(N+2)=2N-2. Its upper-left 2 by (N-1) integer chart is saturated,
index one; all other entries follow by integer additions/subtractions, with
physical forced zeros reinserted. Signed bipartite incidence is totally
unimodular, so integral margins give integral vertices and actual polynomial
degree 2N-2 before interpolation. No full hive/table affine equivalence or
residue replacement is asserted. N<=3 is not obtained by a degree-changing
limit; the inherited two positive N=3 originals with an adverse whole gain
remain outside this theorem.

## 2. Full polynomial, source dependencies and reduction

At fixed x=At define


```text
U(w)=a_n(x)a_n(x+w),
V(w)=sum_(j=0)^(n-1)d_j(w)d_(2n-j)(x)+d_n(w)a_n(x),
D(w)=U(w)-V(w).
```

The singleton terminal is a_n, never d_n. The full pair J_n(x,h) is


```text
sum_(0<=I<=x,J>=0,I+J<=h-2)
  (x-I+1)a_(n-2)(I)a_(n-2)(J)(h-I-J-1).
```

Its low formula is (x+1)binom(h+2n-3,2n-1)
minus (n-1)binom(h+2n-3,2n). At h>x retain the entire upper correction
sum_(j=0)^(n-2)(j+1)binom(x+n,n-2-j)binom(h-x+n-2,n+2+j).
All strict shifts and the original first-row bound survive.

The complete triple T_n(x,g), zero for g<=0, has finite form


```text
sum_(0<=I<=x,I<=g-3)a_(n-3)(I)a_2(x-I)a_n(g-I-3).
```

For 0<=g<=x this is


```text
T_low=a_2(x)binom(g+2n-5,2n-2)
   -(n-2)(x+1)binom(g+2n-5,2n-1)
   +(n-2)(n-1)binom(g+2n-5,2n)/2.
```

For g=x+v>=x it is


```text
T_high=sum_(j=0)^n binom(j+2,2)
               binom(x+n,n+j)binom(v+n-3,n-j).
```

The first identity follows from the three factorial moments of I, with I<=x
redundant only in that band. The second follows by putting r=x-I, expanding
a_n(v+r-3) in binom(r,j), and using
a_2(r)binom(r,j)=binom(j+2,2)binom(r+2,j+2) before convolution.
In the high finite count, negative residuals -1,-2,-3 have exactly zero
binomial polynomial at n>=3. No nonzero negative-margin count is continued.
The whole T is continuous at zero and x; derivative equality is not assumed.

The canonical equal-a original has rows

    (A, A+2u+H, (n-1)(A+u)+(n-3)H),

and columns three copies of A+u and n-2 copies of A+u+H, with n>=3,
A>0, H>0 and u>=0. Put s=ut and h=Ht. Its ENTIRE polynomial is


```text
Q_n(x,s,h)=U(2s+h)-3V(s+h)-(n-2)V(s)
                     +3J_n(x,h)-T_n(x,h-x-s).        (Q)
```

All three pairs remain even though their s derivatives vanish. The triple
changes with s and cannot be cancelled. The third row is positive, including
n=3. No fourth selected intersection survives because the remaining columns
are isolated in the full overlap graph.

The completed U11 argument removes isolated-column excess and then both
unequal triangle gaps through complete nonnegative gains. For triangle widths
a,a+v,a+v+w, a=A+u, H=A+B-(a+v)-(a+v+w)>0, the minimum isolated width is
a+2v+w+H. The minimum must belong to the triangle, since a smaller isolated
column would meet an existing edge. Lower isolated widths in place, changing R.
Their exact gains are V(ut)-V(delta*t)+d_(2n)(At)-d_(2n)(eta*t), with
delta<=u and eta<=A. Put


```text
D_s(w)=U(2s+w)-V(s+w),
S_s(w)=U(2s+w)-2V(s+w)-(n-1)V(s)+J_n(x,w).
```

D_s has nonnegative coefficients and S_s is coefficientwise monotone in
numerical height. The full two gap gains are

    S_s(h+p+z)-S_s(h+p)
      +D_s(h+2p+z)-D_s(h+p+z)-D_s(h+2p)+D_s(h+p),
    2[S_s(h+p)-S_s(h)]+D_s(h+2p)-2D_s(h+p)+D_s(h),

where p=vt,z=wt. Their triple height H-A-u is unchanged, so its full value
cancels only in these differences and remains in Q_n(x,s,h).

The U11 one-pair monotonicity has a full low-band proof keeping its last two
singleton partners, terminal and pair derivative; its six cleared numerator
identities and n=3 base are required verification inputs. The high-band proof
uses the complete A75 W contraction, including both boundary children and the
n=2 plateau. The shifted S_s identity has a height-independent Hhalf and
nonnegative mixed differences of D and U, so differentiating in height is
valid. This dependency is reconstructed at its displayed scope, not adopted
merely because its source bytes match.

At u=0 the full U03/U05 equal-three-narrow original is paid by K_n. U03 groups
the last two singleton partners, the entire negative terminal with multiplier
two, and ALL three full pairs. Its twelve exact index polynomials pay H<=A.
U05 pays the complete middle triple from that wall and then all eight bounded
endpoints in the high band, with all three D3 children, negative U_(n,1), and
the exceptional n=3,n=4,k=3,k=4 terms retained. All 65 sign-appendix identities
are dependencies to be independently reconstructed. This is a complete paid
starting original, not a sign assertion about isolated intersections.

## 3. All-index reduction to the initial slope

All derivatives hold x and the other displayed variables fixed BEFORE cone
substitution. Put


```text
M(x;s,h)=2U'(2s+h)-3V'(s+h)-(n-2)V'(s),
L_n(x,w)=2U'(w)-3V'(w)-(n-2)V'(0)+T_g(x,w-x).
```

Use the appropriate one-sided T branch. Then Q_s=M+T_g: the triple derivative
has a PLUS sign because Q subtracts a triple whose height decreases with s.

The full U12 ratio j U_j >= n V_j, 1<=j<=n, follows from rising addition,
the identical sigma_(n,j)a_n terminal, and the factor comparison
a_n a_k>=a_n+(n+1)d_(n+k), k>=1. If e_j=[w^j]a_(n-1)(w), then
sigma_(n,j)=e_(j-1)/n, sum_(l=j)^(n-1)sigma_(l,j)=e_j, and
j e_j >= (n-j)e_(j-1)/(n-1). At j=n the identical terminals cancel.
The complete half endpoint


```text
Hhalf(x,s)=U(2s)-(n+1)V(s)-K_n(x)
```

is nonnegative: its rising-addition decomposition retains the positive
R_(n,k)=a_n a_k-a_n-(n+1)d_(n+k), the mixed translation difference of a_n,
and B_n(s)-1, where B_n=a_n(2s)-(n+1)d_n(s)
>=a_(n-1)(s)[1+(n-1)s/n]>=1. Thus Hhalf_s(x,0)>=0.

The ratio proves M_s>=0. In a mixed monomial s^k h^q, q>=1, the relevant
bracket is 2^(k+2)U_(k+q+2)-3V_(k+q+2); for q=0 it is
2^j U_j-(n+1)V_j, j=k+2. It also proves


```text
M(x;s,s+w)-M(x;0,w)>=0.
```

The q>=1 bracket is 2*3^k U_(k+q+1)-3*2^k V_(k+q+1).
For q=0 it is 2*3^k U_(k+1)-(3*2^k+n-2)V_(k+1).
The last follows from 2*3^k-3*2^k-k+1>=0: it is zero at k=1 and its next
value minus twice its current value is 2*3^k+k-2>0. The n-2 isolated
singletons have not disappeared.

When h>=s the triple argument stays IDENTICAL in this comparison, giving
Q_s(x,s,h)>=L_n(x,h-s). If h<s, the triple is absent; M_s and the same
comparison reduce to Hhalf_s(x,0)>=0. It therefore suffices to sign L in all
three cones w<=x, x<=w<=2x, and w>=2x. No arbitrary-n conclusion follows
from extending the old finite array range.

## 4. Low cone, with the entire terminal

Write E(w)=2U(w)-3V(w), f(w)=d_(n-1)(w),
alpha=(n+1)/n, beta=(2n-1)/(n+1), c=f'(0)=1/(n-1),
q0=f''(0)=2H_(n-2)/(n-1). All earlier rising-addition partners have positive
coefficients. Their last group is EXACTLY a_n(x) f(w)(alpha+beta*x-w/n).
At x=b+w, the full second derivative of this group divided by the explicit
common factor a_n is


```text
alpha(f''-q0)+beta*b*f''+(beta-3/n)(f'-c)
  +(beta-1/n)(w f''-f'+c)+(alpha*q0-2c/n).
```

Every term is nonnegative for n>=3: f has positive coefficients,
w f''-f'+c>=0, beta-3/n>0, and H_(n-2)>=1. Multiply the factor back;
no coefficientwise inequality is cancelled through a positive polynomial.
Thus E''>=0 on w<=x. Since L(x,0)=Hhalf_s(x,0)>=0 and the triple is absent,
coefficientwise integration proves the complete low-cone claim.

## 5. New uniform payment of the middle cone, n>=7

Put w=x+g, x=b+g, b,g>=0. Let q(g)=a_(2n-5)(g) and
Delta=(2n-2)(2n-3)(2n-4). Set


```text
c3=(n-2)/(2n-1), d3=(n-2)(n-1)/(4n(2n-1)),
B=a_2(x)-c3(x+1)(g-3)+d3(g-3)(g-4),
C=c3(x+1)+7d3-2d3*g.
```

Then T_low=g(g-1)(g-2)q B/Delta and B_g=-C at FIXED x.
Both B and C have nonnegative coefficients after x=b+g. Indeed c3<1/2,
d3<1/8, c3-2d3>0; B has coefficients 1/2,1-c3,1/2-c3+d3 in
b^2,bg,g^2; 3/2+3c3,3/2+2c3-7d3 in b,g; and 1+3c3+12d3.
Moreover


```text
B <= 4+3x+5x^2/8 = Bbar,
C <= 11/8+x/2 = Cbar.
```

Expanding the ENTIRE fixed-x derivative and discarding only terms already
proved nonnegative gives


```text
T_g >= -[6g q B+3g^2 q' B+(g^3+2g)q C]/Delta
    >= -x q[(6n-9)Bbar+(x^2+2)Cbar]/Delta,         (M1)
```

because g q' <= (2n-5)q and 0<=g<=x. These are polynomial comparisons after
the stated cone substitution; the adverse full triple derivative is paid.

For E, retain the same complete last group as in section 4, but compare its
first derivative at w and zero. Earlier partner increments are nonnegative.
The elementary bounds f<=w f' and w<=2x give


```text
E'(w)-E'(0)
  >= a_n(x){[alpha+(beta-4/n)x](f'(w)-c)-2wc/n}.
```

For every m>=1, a_m'>=a_(m-1). One exact proof is


```text
a_m'-a_(m-1)
  =sum_(i=1)^(m-1)(m-i)/(mi)
                       product_(1<=j<=m-1,j!=i)(1+w/j)>=0.
```

Since a_m-1>=w a_(m-1)/m, it follows that
f'(w)-c >= w a_(n-3)(w)/(n-2). For n>=5 the resulting two coefficients


```text
C0=alpha/(n-2)-2/[n(n-1)] >= 1/n,
C1=(beta-4/n)/(n-2) >= 1/n
```

are positive. In the second inequality the cleared numerator is n^2-4n-2,
positive at n>=5. Also beta-4/n>=0. For x>=g and n>=5, sorting the COMPLETE
denominator lists 3,...,n and 1,...,n-3 proves


```text
a_n(x)a_(n-3)(g) >= a_2(x)q(g).
```

Consequently the FULL derivative increment satisfies


```text
E'(w)-E'(0) >= x a_2(x)q(g)(1+x)/n.              (M2)
```

As E'(0)-(n-2)V'(0)=Hhalf_s(x,0), combining (M1)-(M2) proves


```text
L_n(x,w) >= Hhalf_s(x,0)+x q(g) Z_n(x)/(n Delta),
```

where a valid smaller Z is the cubic with coefficients, in orders x^0..x^3,


```text
Delta-n(24n+11/4),
5Delta/2-n(18n+1),
2Delta-n(15n/4+11/8),
(Delta-n)/2.                                      (M3)
```

Substitute n=m+7. Every coefficient polynomial has positive coefficients;
the complete exact expansions are in uniform-certificates-v1.json. In
particular the first is 8m^3+108m^2+1541m/4+499/4. The other three are
checked as literal identities, not values at selected indices. This pays
every middle height for all n>=7, including both walls.

## 6. New complete high kernels

For w=2x+v, expand at v>=0. Define the full singleton moment


```text
S2_(n,k)=sum_(j=0)^(k-1)d_j(2x)d_(n+k-j)(x)
                                  +d_k(2x)a_n(x),
```

with S2_(n,0)=a_n. Define D3_(n,k) as the complete polynomial convolution
sum_(r=0)^x a_(n-3)(x-r)a_2(r)a_k(r-3). For k>=3 it is exactly


```text
10binom(x+n+k-3,n+k)
 +5(k-3)binom(x+n+k-4,n+k)
 +(k-3)(k-4)binom(x+n+k-5,n+k)/2.
```

This follows from all three terms in the generating numerator
z^3[10+5(k-3)z+(k-3)(k-4)z^2/2]/(1-z)^(k+3).
The k=0,1,2 polynomial moments are retained separately; they need not be
interpreted as counts with negative residuals. Put


```text
B_(n,k)=2a_n(x)a_k(3x)-3S2_(n,k)+D3_(n,k).
```

Rising addition of the ENTIRE high T and V gives


```text
L_n(x,2x+v)=sum_(l=1)^n d_l'(v)B_(n,n-l)
                                      -(n-2)V'(0).     (H1)
```

Exactly B_(n,0)=B_(n,1)=0. We now prove B_(n,k)>=0 for
2<=k<=n-1, including every boundary child.

Let S1_(n,k)=sum_(j=0)^(k-1)d_j(x)d_(n+k-j)(x)+d_k(x)a_n,
and A_(n,k)=2a_n a_k(2x)-3S1_(n,k), with A_(n,0)=-a_n.
For k>=1, rising addition and the full terminal give


```text
A_(n,k)=sum_(j=0)^(k-2)d_j(x)[2a_n a_(k-j)-3d_(n+k-j)]
     +a_n d_(k-1)(x)[1+1/k+(beta-1/k)x]>=0.        (H2)
```

Here the factor comparison of section 2 signs all earlier partners. In
particular A_(n,1)=a_n b1, A_(n,2)=a_n b2, where


```text
b1=2+(n-2)x/(n+1),
b2=2+3(3n+4)x/[2(n+2)]
                  +(5n^2+9n-8)x^2/[2(n+1)(n+2)].
```

The exact second expansion is B_(n,k)=sum_(j=0)^k d_j(x)A_(n,k-j)+D3.
For k>=5, retain j<=k-3 as nonnegative and collect ALL three terminal terms:


```text
E=b2+(x+k-2)b1/(k-1)
                     -(x+k-2)(x+k-1)/[k(k-1)],
P=a_n(x)a_(k-3)(x), Q=a_(n+k-5)(x), f=a_2(x), L=n+k,
den5=L(L-1)(L-2)(L-3)(L-4),
BH=10(x+L-4)(x+L-3)+5(k-3)(x-3)(x+L-4)
                                  +(k-3)(k-4)(x-3)(x-4)/2.
```

The full terminal-plus-D3 group is

    x(P-fQ)E/(k-2)
      +xQ{fE/(k-2)+(x-1)(x-2)BH/den5}.               (H3)

For n>=k+1 and k>=5, P>=fQ by sorted denominator lists. Directly from b1,b2,
E>=2+4x+2x^2: its constant is at least 2, its linear coefficient at least 4,
and its quadratic coefficient at least 2 (n>=6 and (n-2)/(n+1)>=1/k).
BH has nonnegative coefficients. Its x^2 coefficient is (k+1)(k+2)/2,
its x coefficient is (k+1)(10n+3k-14)/2, and its constant is
10(L-4)(L-3)-15(k-3)(L-4)+6(k-3)(k-4), positive since
10(L-3)-15(k-3)=10n-5k+15>0. It obeys


```text
BH <= 16L^2(1+x)^2,
3x BH/den5 <= 768 x(1+x)^2/L^3
            <= 96 x(1+x)^2/k^3 < 4x(1+x)^2/k.
```

We used L>=2k+1>=11 and every L-i>=L/2 for 1<=i<=4.
Finally


```text
2a_2(x)(1+x)^2-4x(1+x)^2=2+3x+x^2+x^3+x^4>=0.
```

Thus fE/(k-2) pays the ENTIRE possible negative part -3x BH/den5 in
(H3). The other two pieces of (x-1)(x-2)BH are nonnegative. No factor
with a negative coefficient was cancelled or called positive in isolation.
This proves every k>=5 kernel uniformly.

For k=2,3,4, divide by the exact factor a_n and clear the positive
D_k=(n+1)...(n+k). All coefficients of the resulting degree-k polynomial
have positive numerator coefficients after n=m+k+1. The COMPLETE arrays
are in uniform-certificates-v1.json. At k=2 the explicit quotient is


```text
3 + 3(2n^2+4n-1)x/[(n+1)(n+2)]
  +3(n^2+n-1)x^2/[(n+1)(n+2)].
```

These are fixed small-k identities with an unbounded n, not a k or n cutoff.
The k=0,1 cancellations, all three D3 terms and every terminal are included
in their independent verification.

Equation (H1) now shows L_n(x,2x+v)>=L_n(x,2x+0), since
d_l'(v)-d_l'(0)>=0 and the constant isolated-singleton term is unchanged.

## 7. The FULL derivative jump and the four small indices

The high-minus-low triple value is minus the complete upper tail and vanishes
at g=x. Its derivative jump has the exact positive formula


```text
T_high,g(x,x)-T_low,g(x,x)
  =sum_(j=0)^(n-3)binom(j+2,2)a_(n-3-j)(x) B(n-2+j,6)>=0,   (J)
```

where B(p,6)=(p-1)!5!/(p+5)!. Retaining every upper-tail summand, its
delta-linear coefficient is (-1)^(l+5)B(n-2,l+6). The finite signed sum
inside the beta integral becomes positive by the exact coefficient identity


```text
sum_l (-1)^l binom(l+2,2)binom(x+n,n-3-l)(1-u)^l
  =sum_j binom(j+2,2)u^j a_(n-3-j)(x).
```

Extract the coefficient of z^(n-3) in
(1+z)^(x+n)/(1+(1-u)z)^3, and rewrite its denominator using
1+(1-u)z=(1+z)(1-u*z/(1+z)). Integration against
u^(n-3)(1-u)^5 proves (J). Thus high L starts no lower than the paid middle
L at w=2x. A false assumption of derivative continuity is unnecessary.

For n=3,4,5,6, the eight COMPLETE middle/high L polynomials, including every
zero through total degree 2n-1, are independently reconstructed from the
full Newton singleton and full triple formulas. Their exact nonnegative
coefficient arrays supply four fixed bases. Other n=7..15 arrays are
corroboration only. Combining these bases, sections 4-7 and the displayed
arbitrary-index inequalities signs L at every n>=3 and every w>=0.

## 8. Restore the entire original

Section 3 now proves Q_s>=0 in every chamber for every n>=3. The full Q is
continuous at both triple walls, so integrating each ordinary t coefficient
in the NUMERICAL u parameter gives Q(A,u,H;t)>=Q(A,0,H;t). Derivatives are
one-sided where required; no rational-grade count or period-one assertion on
arbitrary rational margins is used. The integral endpoints have their exact
original integer lattices and literal LR triples.

The full U03/U05 base pays Q(A,0,H;t)>=K_n(At). The complete U11 isolated
width and unequal-gap operations then restore every original in section 1.
The full triple remains in every base and both endpoints; every pair, high
tail, singleton terminal, strict shift and isolated column remains. Physical
zeros, labels and ties stay in place. Zero gap/excess increments are exactly
zero, not failures. The explicit K reserve proves strictness through actual
degree, and the genuine-triangle surplus inherits the complete paid base.

The proof's dependencies, full all-grade identities, unused-grade original
checks, omission controls and independent gate must pass before adoption.
Positive finite arrays, byte authentication, internal model review and this
draft individually imply no human peer review, formal certification, worldwide
novelty, whole-rank theorem or unrestricted KTT result.
