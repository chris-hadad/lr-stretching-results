# A60: complete balanced deficit-three originals

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation, 27 September 2026. The accepted A58 whole-character bridge
and A59 deficit-two theorem are premises at their exact scopes. This proof
extends the reserve to deficit three; it uses no active provider proof.
 No novelty claim is made.

## 1. Legal entire original, lattice and statement

Let a>=3, k_1,...,k_a>=1, K=sum k_i>=6, B=K-3 and s>=1 be integers.
Take widths (u_1,v_1,s k_1,...,s k_a,u_2,v_2) with all four paired
widths >=H=2sB. The first and last adjacent pairs have overlap sB;
all other overlaps are zero. Construct the literal partitions upwards by
lambda_n=w_n, mu_n=0, mu_i=lambda_(i+1)-e_i, lambda_i=mu_i+w_i.
The output is nu=(sum w_i-2H,H,H), with lambda OUTER.

All adjacent partition inequalities follow from 0<=e_i<=min(w_i,w_(i+1));
containment and size balance hold, and sum w_i>=4H implies nu dominance.
The last outer row is positive, so the maximum trimmed original rank is
exactly a+4. Arbitrary cap order, unequal paired widths above their floors,
and physical isolated zero-width row insertion are allowed. In the last
case a still counts only positive caps; physical rank counts every listed
row. Common scaling is s(K-3), never sK-3.

The COMPLETE original polynomial is P(s t), where


```text
P(t)=sum (Bt-U+1)(Bt-V+1),
u_i,v_i>=0, u_i+v_i<=k_i t, U=sum u_i<=Bt, V=sum v_i<=Bt.       (1)
```

The accepted A58 A58-FIRST-WALL-PROOF.md Section 2 derives this equality from the
full skew character, retaining the two paired determinants, full Weyl
annihilator and every once-only shift. It applies to arbitrary caps and
budgets under the stated paired-width floors. Each of the two weights in
(1) counts two nonnegative slack coordinates with fixed sum. Eliminating
one slack per budget gives the saturated lattice Z^(2a+2). All caps and
budgets are positive; sufficiently small positive u,v and strict slack
choices give a full-dimensional rational interior. The result below also
proves degree exactly 2a+2 without asserting a generic hive isometry.

**Theorem.** Every ordinary coefficient of P, from constant one through
actual degree 2a+2, is strictly positive. For a>=6, with r=K-6>=0,


```text
P >=_c N [1+(139/140+5r/4)t
             +(47/780+2387r/2340+5r^2/12)t^2],                (2)
N=product_i binom(k_i t+2,2).
```

Here >=_c compares ordinary monomial coefficients. This is a theorem about
this entire original family at every rank >=7, not whole-rank positivity
or arbitrary-budget KTT. The four paired widths may change within their
floors because the original-character identity, not a row deletion, gives
(1). Zero isolated rows contribute h_0=1 and preserve the physical original.

## 2. Complete correction, including simultaneous cap violations

Put m_1=#{k_i=1}, m_2=#{k_i=2}, c=B-3/2 and


```text
L=5K/4-6, Q=(4(2K-9)^2-sum k_i^2)/36, A(t)=2+ct,
T=A(t) binom(3t+2a-1,2a+1)+binom(3t+2a-1,2a+2),
C_k=(kt+2)A(t) binom((3-k)t+2a-3,2a)
   +((kt+2)+A(t)) binom((3-k)t+2a-3,2a+1)
   +binom((3-k)t+2a-3,2a+2),                         k=1,2,
D=(t+2)^2 A(t) binom(t+2a-5,2a-1)
   +((t+2)^2+2(t+2)A(t)) binom(t+2a-5,2a)
   +(2(t+2)+A(t)) binom(t+2a-5,2a+1)
   +binom(t+2a-5,2a+2).
```

All binomials here are rational falling-product polynomials. Then


```text
P=N(1+Lt+Qt^2)+2T-2m_1 C_1-2m_2 C_2+2 binom(m_1,2)D.         (3)
```

Proof of the COMPLETE identity: the unrestricted signed slack sum in (1)
is N(1+Lt+Qt^2), by E(u_i)=E(v_i)=k_i t/3 and
Cov(u_i,v_i)=-(k_i^2 t^2+3k_i t)/36. The two negative budget tails
are disjoint: 2Bt+2>Kt for K>=6. A zero slack contributes nothing.
In the first negative tail replace u_i by k_i t-v_i-x_i. Its residual
total S=sum(x_i+v_i)<=3t-2. The correction weight is
(3t-1-S)(Bt+1-V), retaining x_i+v_i<=k_i t.

For any fixed list of pair sums, symmetry x_i<->v_i makes the average
V exactly S/2. Thus we may sum the multiplicity times
(3t-1-S)(Bt+1-S/2); this is an exact first moment, not independence.
For a set J of violated caps put q=|J|, M=sum_(i in J)k_i and write
x_i+v_i=k_i t+1+w_i. The available residual for all free increments is
R=(3-M)t-q-2. Its multiplicity generating function is


```text
(1-z)^(-2(a-q)) product_(i in J)
           [(k_i t+2)/(1-z)+z/(1-z)^2].
```

Writing g=R-n for the unused residual, the remaining weight is
(g+1)(A(t)+g/2). Its generating function is
A(t)/(1-z)^2+z/(1-z)^3. Taking the coefficient of z^R gives T for
J empty, C_k for one cap of size k, and D for two unit caps.
No other J survives: a cap >=3, a unit plus a two-cap, or three units
already exceeds S<=3t-2. This proves every intersection in (3).
The empty early ranges agree with the displayed polynomial binomials:
for a>=3 their tops are nonnegative and smaller than the bottom indices.
In particular D first contributes at t=4, and C_2 first contributes at
t=3. Omitting these terms changes the whole count at those grades.

## 3. Large dimension: one reserve pays every correction

Write E_j(z)=product_(h=1)^j(1+z/h), n=2a,
D_3=n(n-1)(n-2), D_4=(n-1)(n-2)(n-3)(n-4), and
N_0=((1+t)(1+t/2))^a. For a>=6 the following bounds hold:


```text
E_(2a-1)(3t) <=_c (3/2)N_0,
E_(2a-3)(2t)(1+2t)(1+t)^2 <=_c (3/2)N_0,        (4)
E_(2a-3)(t)(1+t)^2(1+t/2) <=_c N_0,
E_(2a-5)(t)(1+t)^4 <=_c N_0.
```

The first two have exact finite bases a=6 in ../certificates/a60-a61/k3-certificate-v1.json.
Every coefficient of their residuals is nonnegative; their maximum ratios
are respectively 83711/83160 and 4867/4410, both <3/2. To pass a->a+1,
the first gains factors (1+3t/(2a))(1+3t/(2a+1)); the second gains
(1+2t/(2a-2))(1+2t/(2a-1)). Each pair is coefficientwise at most
(1+t)(1+t/2) for a>=6. The last two inequalities follow by factor
matching: after their extra slope-one factors, assign the earliest E
factors to the remaining slope-one slots, and the others to slope-one-half
slots. For the last inequality one slope-one-half slot remains unused.
Finally N>=_c N_0 by the cap floors. These are coefficient inequalities,
not merely inequalities at positive t.

The tail factors exactly as


```text
2T = 3t(3t-1)E_(2a-1)(3t)(F+Gt)/(a(2a+1)),
F=(2a+1)/(a+1), G=B-3a/(2(a+1))>0.
```

Only its linear and possibly quadratic terms outside E can be negative.
The linear term is -3/[a(a+1)] and the quadratic negative magnitude
is at most 3B/[a(2a+1)]. Dropping the positive terms, then using (4),


```text
2T >=_c -N[9t/(2a(a+1))+9Bt^2/(2a(2a+1))].                 (5)
```

For k=1,2 put s_k=3-k, H=(n+1)(n+2), and


```text
f_0=4-12/(n+1)+12/H,
f_1=2(k+c)+(4s_k-3(k+c))/(n+1)-7s_k/H,
f_2=kc+s_k(k+c)/(n+1)+s_k^2/H.
```

Then


```text
C_k=E_(n-3)(s_k t)(s_k t)(s_k t-1)(s_k t-2)
                 (f_0+f_1 t+f_2 t^2)/D_3.                 (6)
```

For n>=12 and B>=3 the f_i are positive, 3<f_0<=4, and


```text
f <=_c (1+t)(f_0+2Bt) for k=1,
f <=_c (1+t)(f_0+3Bt) for k=2.
```

For example f_1<=2B for k=1 follows from
2(k+c)+4s_k/(n+1)<=2B-1+8/13<2B; f_2<2B follows immediately.
For k=2 the same expressions give f_1<f_0+3B and f_2<3B.
Positive lower bounds follow by n>=12, c>=3/2. Replace the signed
cubic by (s_k t)(s_k t+1)(s_k t+2) only while multiplying its
nonnegative E and f, then apply these f bounds and (4). This yields


```text
C_1 <=_c (6/D_3)Nt(f_0+2Bt),
C_2 <=_c (2/D_3)Nt(f_0+3Bt).                               (7)
```

The pair-intersection term is essential even in the lower bound. Exactly,


```text
D=E_(n-5)(t)t(t-1)(t-2)(t-3)(g_0+g_1t+g_2t^2+g_3t^3)/D_4,
g_0=8-48/n+120/(n(n+1))-120/(n(n+1)(n+2)),
g_1=4c+8+(-16c-20)/n+(20c-14)/(n(n+1))+74/(n(n+1)(n+2)),
g_2=4c+2+(4-4c)/n+(-9c-12)/(n(n+1))-15/(n(n+1)(n+2)),
g_3=c+(2c+1)/n+(c+2)/(n(n+1))+1/(n(n+1)(n+2)).
```

For n>=12,c>=3/2 every g_i is positive, 4<=g_0<=8 and


```text
g <=_c (1+t)^2(g_0+4Bt).
```

Indeed g_1<=4c+8=4B+2, g_2<=4c+2=4B-4, and g_3<4B.
For their positivity it suffices to bound the negative fractions by their
n=12 magnitudes; for example g_1>=(4-16/12)c+8-20/12>0,
and g_2>=(4-4/12-9/156)c+2-12/156-15/2184>0.
The g_0 bounds follow directly by combining its last three fractions.
Since t(t-1)(t-2)(t-3)>=_c -6t(1+t^2), all multiplying factors
are nonnegative, and 1+t^2<=_c(1+t)^2, (4) gives


```text
D >=_c -(6/D_4)Nt(g_0+4Bt).                              (8)
```

Combining (3), (5), (7), (8), using m_1+m_2<=a and
binom(m_1,2)<=binom(a,2), gives a lower polynomial N(1+ell t+q t^2):


```text
ell >= L-9/(2a(a+1))-48a/D_3-96binom(a,2)/D_4,
q >= Q-B[9/(2a(2a+1))+24a/D_3+48binom(a,2)/D_4].          (9)
```

Each positive subtraction factor decreases for integer a>=6. Their sums
at a=6 are 71/140 and 67/260 respectively. Packing a positive cap sum
into one cap gives sum k_i^2<=(K-a+1)^2+a-1<=(K-5)^2+5.
With r=K-6 this gives Q>=5/6+23r/18+5r^2/12, and B=r+3.
Substitution in (9) proves (2), including positive reserves 139/140 and
47/780 at r=0. Because N is strict in degrees 0..2a, (2) pays every
degree through 2a+2. Formula (3) has no higher degree.

## 4. Three to five caps: a finite structural certificate

This is a reduction of all cap patterns, not a sampled positive grid.
For each a=3,4,5 partition the caps into m_1 ones, m_2 twos and m_3
caps >=3. Cap order is irrelevant to (1). Set every large cap initially
to 3; discard cases K<6 with no large cap. The only remaining base below
six is (1,1,3), which must start at (1,1,4). There are exactly forty
base patterns: seven at a=3, thirteen at a=4 and twenty at a=5.

Write each large cap as its base plus an independent z_j>=0. The correction
in (3) is affine in B, and m_1,m_2 stay fixed. N has nonnegative
coefficients jointly in t and all z_j. At each base, L>0,Q>0,
L'_j=5/4 and Q'_j=(16K-72-k_j)/18>0. Every quadratic coefficient of
Q in the z variables is positive (5/12 on squares and 8/9 on distinct
products); there are no higher ones. Consequently every monomial of
z-total-degree >=2 in the complete P is coefficientwise nonnegative.
Only the constant and first z coefficients require checking.

The constant is the full base P from (3). For one large cap j,


```text
partial_j P = N_j(1+Lt+Qt^2)
                +N[(5/4)t+((16K-72-k_j)/18)t^2]
                +partial_B(2T-2m_1C_1-2m_2C_2+2binom(m_1,2)D),
N_j=((3/2)t+k_j t^2) product_(i!=j)binom(k_i t+2,2).
```

At each base all large caps are equal (or there is the single 4), so one
such derivative suffices by permutation symmetry. The exact certificate
../certificates/a60-a61/k3-certificate-v1.json lists every base polynomial and derivative, as
rational coefficients computed with falling products. Each base is strict
through degree 2a+2; every derivative has constant zero and all other
listed coefficients positive. Independently implemented checks verify these
identities and signs. This proves positivity for all independent z_j>=0,
and hence every integer cap pattern with a=3,4,5 and K>=6.

As a useful exact consequence of the complete formula, its first coefficient is


```text
c1 = 11K/4-6-3/[a(a+1)]-(4m_1+2m_2)/[a(a^2-1)]
                   -6binom(m_1,2)/[a(a^2-1)(a-2)].          (11)
```

The pair term is nonzero in this linear coefficient even though its integer
count first appears at grade four. The all-unit a=K=6 value is 1429/140.
This is an entire-original coefficient, not the first coefficient of one tail.

## 5. Mathematical boundary

Both tails remain disjoint only under the stated K>=6 bound. The next
deficit four already needs more cap intersections, and arbitrary budgets
can have two simultaneous budget tails. Neither (2) nor a formal negative
correction signs those domains. General multiple-cap absorber signs, complete
rank seven and unrestricted KTT remain open; no ordinary-negative candidate
or additive census increment follows from this theorem.

## 6. Deficit-uniform complete identity and the next sign obligation

The same argument yields a useful all-deficit reduction without asserting
all-deficit positivity. Let r>=1, K>=2r, B=K-r, with the same complete
positive-cap original, four paired-width floors 2B and a>=3. Put


```text
L_r=5K/4-2r, Q_r=(4(2K-3r)^2-sum k_i^2)/36,
A_r(t)=2+(B-r/2)t.
```

For every subset J of caps with M_J=sum_(i in J)k_i<r, put q=|J|,
z_J=(r-M_J)t+2a-2q-1, and e_l(J;t) the elementary symmetric polynomial
of degree l in the q values (k_i t+2), with e_0=1. Define


```text
T_J=sum_(h=0)^q e_(q-h)(J;t)
       [A_r(t) binom(z_J,2a-q+h+1)+binom(z_J,2a-q+h+2)].
```

Then the ENTIRE original polynomial is exactly


```text
P=N(1+L_r t+Q_r t^2)+2 sum_(J:M_J<r)(-1)^|J| T_J.          (10)
```

The negative budget tails are disjoint because 2B>=K. Their residual total
is rt-2. For a violated subset J the free residual is
(r-M_J)t-q-2, and its multiplicity generating function is the one in
Section 2. Expanding by h selected numerator-z terms produces (10), with
the displayed common binomial top. Every nonempty simultaneous cap
intersection is present. Since M_J<r<=K/2, J cannot include every positive
cap, so q<=a-1; polynomial binomials also give the correct early empty
ranges. This proves the identity at all nonnegative integer grades and
hence as a polynomial. It specializes exactly to A59 at r=2 and (3) at r=3.

Only cap sizes <r appear in the correction. For fixed r it can therefore
be aggregated by the finite multiplicities of small cap types and subset
weight M_J; the remaining large caps occur only in N,K,sum k_i^2. This is
a structural route to a deficit-uniform reserve or finite reduction, with
its sign estimate explicitly unpaid. It is stronger next pressure than
merely collecting another positive fixed-deficit table. If B<K/2, the two
budget tails can meet and (10) is not the correct full formula without
additional joint-budget terms. No result for that missing domain is claimed.
