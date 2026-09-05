# A positive LR cone and its primitive root threshold

This note proves a degree-31 Littlewood–Richardson cone theorem using explicit
rational coefficients and seven uniform root certificates. The complete tables
and proposed disks are in [theorem-data.json](data/theorem-data.json);
[reproduce.py](reproduce.py) reconstructs and checks their arithmetic.

## Theorem and scope

Put \(\rho_m=(m,m-1,\ldots,1)\). For integers \(u,v\ge0\), \(q=u+v>0\), set

\[
\lambda=q\rho_{18},\quad \mu=q\rho_{17},\quad
\nu=(7u+8v,6u+6v,5u+4v).
\]

With lambda the outer partition, the full ordinary stretching polynomial
\(T_{u,v}(t)=c^{t\lambda}_{t\mu,t\nu}\) has degree 31 and every one of its
32 coefficients is strictly positive. Every member with \(u\ge22v\) has at
least two zeros in the open right half-plane. For the primitive slice
\((u,v)=(q-1,1)\), strict Hurwitz stability holds exactly for
\(1\le q\le22\), while every \(q\ge23\) is unstable.

The full cone's uniform assertion is **at least two** zeros. Exactly two is
certified here at q=23, not throughout the infinite cone.

## 1. Full LR realization and prior degree

At stretch t, row i of the skew diagram occupies
\([qt(18-i)+1,qt(19-i)]\), for i=1,...,18. These intervals are pairwise
disjoint. No column comparison connects different rows, so its skew Schur
function is \(h_{qt}^{18}\). The Schur coefficient of this product is the
Kostka number with uniform content. Writing \(s=u+2v\), we obtain at every
nonnegative integral stretch

\[
T_{u,v}(t)=K_{((6q+s)t,6qt,(6q-s)t),((qt)^{18})}.
\tag{1}
\]

This is the whole fiber. No additional hive equalities, selected face, or
subpolytope has been substituted. At t=0 the empty object contributes one.

In the GT chain, nonterminal level k has at most min(k,3) nonzero entries.
There are \(1+2+15\cdot3=48\) such coordinates and 17 independent fixed
level-sum equations, each involving its own level. All entries are O(t), so
the count is O(t^31). The standard stretched-LR polynomiality theorem
(Rassart, arXiv:math/0308101, Corollary 4.2) therefore
gives a degree bound of 31 before any reconstruction. The exact-degree
conclusion below follows from our positive leading coefficients, so it does
not additionally depend on the cited McAllister degree formula.

The shape strictly dominates the content: its first part exceeds q, its first
two parts exceed 2q, and after its first three parts the sum is 18q, exceeding
kq for every k<18. Its three positive parts are distinct throughout the cone.

## 2. Character extraction and the short flow identity

For any integer p, define \(b_p(n)=[z^n](1-z)^{-p}\), zero for n<0. For p>0,
\(b_p(n)=\binom{n+p-1}{p-1}\); for p<=0 it is
\((-1)^n\binom{-p}{n}\) on the finite support 0<=n<=-p. Define

\[
\Phi(A,B;p,h,r)=\sum_{k=0}^{\min(A,B)}b_p(A-k)b_h(k)b_r(B-k),
\tag{2}
\]

zero if A<0 or B<0. When A>=B>=0 and p,h,r>0, Newton expansion gives

\[
\binom{A-k+p-1}{p-1}
=\sum_{j=0}^{p-1}(-1)^j\binom{A+p-1-j}{p-1-j}\binom{k}{j}.
\]

Multiplying by \(b_h(k)b_r(B-k)\), using
\(\binom{k}{j}b_h(k)=\binom{h+j-1}{j}\binom{k+h-1}{h+j-1}\), and applying
Vandermonde yields

\[
\Phi(A,B;p,h,r)=\sum_{j=0}^{p-1}(-1)^j
\binom{A+p-1-j}{p-1-j}\binom{h+j-1}{j}
\binom{B+h+r-1}{h+r+j-1}.
\tag{3}
\]

For A<B, swap (A,p) with (B,r). Nonpositive exponents retain their finite
support from (2); they are not replaced by the positive-exponent formula.

Here is a direct check of the profile parameters and signs, directly from
the character identity. Set \(D_{ab}=X_a-X_b\). In the partial-fraction
expansion
\(h_b=\sum_j X_j^{b+2}/\prod_{l\ne j}(X_j-X_l)\), choose i copies of the
first term, l=m-i-k of the second, and k of the third. Multiplication by the
Vandermonde leaves denominator
\(D_{12}^{p}D_{13}^{h}D_{23}^{r}\), where

\[
p=m-k-1,\quad h=i+k-1,\quad r=m-i-1,
\]

and sign \((-1)^l\). Extracting the alternant exponent
\(t\alpha+(2,1,0)\) gives capacities

\[
A=(wi-\alpha_1)t+i-m,\qquad B=(\alpha_3-wk)t-2k.
\]

Thus the Kostka number is the sum of (2) over all i,k>=0, i+k<=m, weighted by
\((-1)^{m-i-k}\binom mi\binom{m-i}k\). This establishes the character
extraction as well as the sign convention.

## 3. The complete closed chamber polynomial

For m=18 put x=qt, y=st. Along rays x<=y<=2x the only eventually contributing
profiles are

\[
8\le i\le18,\quad 0\le k\le\min(4,18-i),
\]

which gives 45 profiles. Their capacities and exponents are

\[
A=(i-6)x-y+i-18,\quad B=(6-k)x-y-2k,
\quad(p,h,r)=(17-k,i+k-1,17-i).
\]

The difference is \(A-B=(i+k-12)x+i+2k-18\). Its eventual sign is positive
for i+k>=13 and negative otherwise; at i+k=12 the constant is k-6<0.
Use precisely that fixed order in (3), and interpret every binomial with
constant lower argument as its falling-factorial polynomial. Branching on
small numerical A,B instead would not construct the desired polynomial.

For r=0 use
\(\binom{A-B+p-1}{p-1}\binom{B+h-1}{h-1}\). For r=-1 subtract
\(\binom{A-B+p}{p-1}\binom{B+h-2}{h-1}\) from that expression. These follow
directly from the supports {0} and {0,1}. The positive-exponent terms have
degree p+h+r-2=31; the r=0 terms also have degree 31. The two degree-32
products for r=-1 have identical highest homogeneous parts, which cancel.
The resulting finite expression F(x,y) therefore has total degree at most 31.

Both boundaries are valid. At y=x, excluded i=7 and k=5 have A=-11 and B=-10,
respectively. At y=2x, included i=8 has A=-10; since its eventual order is
A<B, the second binomial in (3) becomes \(\binom{13}{23+j}=0\). Included
k=4 and i>=9 has B=-8 and its second binomial becomes
\(\binom{11}{19+j}=0\). Thus those included boundary profiles vanish
identically. No unverified continuity of integer counts is needed.

For each fixed integral (q,s) with q<=s<=2q, the exact flow count and F(qt,st)
agree for all sufficiently large integers t. They are both polynomials of
degree at most 31, by the preceding argument and (1). Hence they agree at
every stretch. In particular F(x,y) counts every integral point of the closed
chamber, including small stretches and both walls.

## 4. Independent reconstruction and positivity

Let H(u,v)=F(u+v,u+2v). Our checker evaluates the just-derived polynomial
expression on the fixed unisolvent simplex u=a,v=b, a,b>=0, a+b<=31, and uses

\[
H(u,v)=\sum_{i+j\le31}\Delta_u^i\Delta_v^jH(0,0)
\binom ui\binom vj.
\tag{4}
\]

This is an exact reconstruction of a polynomial with a prior degree bound.
Those simplex values are evaluations of the profile polynomial; we do not
misdescribe them as independently computed native tableau counts. Integer
generalized binomials at negative upper arguments are evaluated by
\(\binom nk=(-1)^k\binom{k-n-1}k\).

After converting (4) to monomials, every coefficient h_ij for i+j<=31 is
strictly positive: all 528 indices occur, and all 528 rational values agree
with the coefficient table. Independently substituting u=2x-y and v=y-x also reproduces
all 528 entries of the F table. The first terms are

\[
H=1+\frac{212282279}{19643150}u+
\frac{113824241067}{9831396575}v+\cdots.
\]

The full exact values are in [theorem-data.json](data/theorem-data.json).
An optional reproduction output contains both reconstructed tables. Since
\([t^d]T_{u,v}(t)=\sum_{i+j=d}h_{ij}u^iv^j\), every ordinary coefficient
is positive at every nonzero nonnegative (u,v), including the axes. The
degree-31 coefficient is positive, proving the exact degree independently
of a separate exact-dimension theorem.

Additional checks use newly written algorithms: 31 full literal flow counts,
nine positive coefficient-grid multiplications of h_x^18 followed by its six
alternant terms, and 10,816 comparisons of (3) with (2). The nine grid counts
use neither partial fractions nor the flow sum. These finite controls support
the implementation; the infinite identity rests on the polynomial argument.

## 5. Exact uniform root certificates

Put G(z,e)=H((1-e)z,ez)=F(z,(1+e)z). For q=u+v and e=v/q we have
T_(u,v)(t)=G(qt,e). In each proposed disk the checker independently constructs
all Taylor coefficients

\[
G(c+w,e_0+h)=\sum_{j,k=0}^{31}A_{jk}w^jh^k
\]

from its freshly reconstructed H. With Q=10^30, the rational upper bound
for a nonzero Gaussian rational a is

\[
U(a)=\frac{1+\lfloor\sqrt{\lfloor Q^2|a|^2\rfloor}\rfloor}{Q}>|a|;
\quad U(0)=0.
\]

The entire remainder is bounded by
\(U=\sum_{(j,k)\ne(1,0)}U(A_{jk})r^j\eta^k\). Every disk passes the exact
strict inequality

\[
U^2<|A_{10}|^2r^2.
\tag{5}
\]

The exact remainder, linear norm square, and positive squared gap are preserved
per disk. This uses no precomputed derivative lower bound or
precomputed majorant. The following rational numbers round **up**
the squared ratios in (5); all are below 1.

| e interval | Upper bound for U^2/(|A10|^2 r^2) |
|---|---:|
| [0,1/50] | 79519190499/200000000000 |
| [1/50,3/100] | 6211018373/20000000000 |
| [3/100,9/250] | 320895964751/1000000000000 |
| [9/250,1/25] | 114237352709/250000000000 |
| [1/25,21/500] | 421387995681/1000000000000 |
| [21/500,43/1000] | 365197853799/1000000000000 |
| [43/1000,1/23] | 253450731153/1000000000000 |

The closed intervals cover [0,1/23] without a gap. Every disk satisfies
Re(c)>r>0 and Im(c)>r. On its boundary, Rouché comparison with A10*w gives
exactly one zero, uniformly for all real |h|<=eta. Its conjugate lies in a
disjoint disk, also entirely in the open right half-plane. Therefore every
G(z,e), 0<=e<=1/23, has at least two RHP zeros. Positive scaling z=qt gives
the assertion u>=22v. No numerical root finder is part of this proof.

## 6. Primitive threshold, distinction, and crossing

For q=1,...,23 the checker specializes its reconstructed H at (q-1,1), verifies
the supplied full coefficient vectors and 35 recorded values per q, and builds
a fresh regular exact Routh table. Its rows use integer arithmetic, with only
positive rescaling: each numerator row is multiplied by the previous pivot's
sign and divided by a positive gcd. This preserves the Routh first-column
signs. Any zero row or pivot causes failure. All 23 tables are regular, with
zero sign changes for q<=22 and two for q=23. Regularity excludes imaginary-axis
zeros, so the first 22 polynomials are strictly Hurwitz stable. Together with
the uniform cover at e=1/q, this proves the sharp integer threshold.

The triple's gcd is one because its outer parts include q and its first nu
part is 7q+1. The ratio of nu's first adjacent gap to an outer adjacent gap
is (q+1)/q, which is injective in positive q and invariant under determinant
twists and common dilation. Exchanging the two inner partitions cannot defeat
the argument: the padded mu has 17 nonzero adjacent gaps, while padded nu has
three. That distinction is also twist/dilation invariant.

Finally G(z,1/23) has RHP zeros and G(z,1/22) is strictly stable. Its constant
is 1 and its leading coefficient is positive throughout [0,1]. Continuous
dependence of roots, together with the openness of both endpoint properties,
forces a nonzero imaginary-axis crossing at an interior point of
(1/23,1/22). A vanished leading coefficient cannot send roots to infinity,
and the nonzero constant excludes crossing through zero. No particular
location, uniqueness, or transversality is established.

## Dependencies and limits

The standard identities for skew Schur functions, Kostka expansion, stretched-LR
polynomiality, Routh counting, and Rouché's theorem are mathematical dependencies.
The degree proof uses a prior counting bound and positive reconstructed
leading coefficients, so no separate exact-dimension formula is needed.
The root conclusion is at least two zeros uniformly; exactly two is certified
only at the stated finite endpoint. Crossing uniqueness and transversality
are not asserted.
