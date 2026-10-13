# A81: complete fixed-wall index augmentation

Curated mathematical proof from **A81**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Proposed independent reconstruction, version 2, of Pro055 U11, with the complete character
and normal-form dependencies of U03–U10.  This document
states the selected original and complement results. Quotients, the stronger
rho-normalized gain, other u values and unrestricted KTT are outside its claim.

## 1. Complete originals and proposed theorem

For every integer m >= 3 and s >= 0, preserve all physical rows in


```text
lambda_m = ((m+8)s,(m+6)s,(m+4)s,ms,(m-1)s,...,s),
mu_m = ((m+4)s,(m+2)s,ms,(m-1)s,(m-2)s,...,0),
nu_m = ((m+4)s,5s,3s).
```

Lambda is outer. These are the root-square family at u = 2s. Let C_m(S) be
the entire stretching polynomial after S = st, with all ordinary coefficients
in ascending powers. Define


```text
a_n(z) = product_(r=1)^n (1+z/r),  a_0(z) = 1,
B_m(S) = product_(r=1)^(m-3) (S+r)(S+r+1)/(r(r+1)),
j_m(S) = 1 + (2+3/[m(m-1)])S + (4m-3)S^2/[m(m-1)],
J_m(S) = B_m(S) j_m(S),   E_m(S) = C_m(S)-J_m(S),
D_m(S) = a_(2m+1)(4S),
T_m(S) = D_m(S)(1+S/(m+2)).
```

B_3 is the empty product 1. J is the complete explicitly embedded component
proved in section 3; E is its full complement. D_m here is the slope-four
product, not the old unrestricted-tail product a_2(S)^m.

The selected theorem is


```text
C_(m+1)-C_m >=_coef S T_m/(4m),             m >= 3,
E_(m+1)-E_m >=_coef S T_m/(4m),             m >= 4.       (1)
```

For m >= 96 the denominator 4m may be replaced by 2m. The full J gain is
ordinary nonnegative, and therefore for m >= 4 the first comparison strengthens
to J_(m+1)-J_m + S T_m/(4m). The C/E gains in (1) have zero constant and, for
s > 0, strictly positive coefficients in every degree 1 through 2m+3.

The complete C_m is strict in every degree 0 through 2m+1 for s > 0. The
complete E_m has constant zero and is strict in every degree 1 through 2m+1.
Their actual degrees and saturated original lattice are established before
fitting in ORIGINALS-AND-GEOMETRY-v1.md. At s = 0 the wall has u = 0;
C_m = J_m = 1, E_m = 0 and both gains are zero.

The complement induction cannot start at m = 3:


```text
[S](E_4-E_3) = -499/2520,
[S](J_4-J_3) = 5/4,
[S](C_4-C_3) = 2651/2520.                              (2)
```

The adverse complete gain is compensated in the same ordinary coefficient.
It is not a negative LR original. All complete endpoint and gain vectors,
including this exception, belong to the verification evidence.

## 2. Full character, recentring and every physical capacity

At general integer S,U >= 0 the top skew shape is
(4U,3U,2U)/(2U,U,0). The m remaining labeled strips of length S are disjoint
from each other and the top. In three variables its entire top character is


```text
h_(2U)^3 - 2 h_(2U) h_(3U+1) h_(U-1)
              + h_(4U+2) h_(U-1)^2 = s_(2U,U,0)^2.     (3)
```

A direct proof sets the variables to (1,x,y) and substitutes


```text
h_d = 1/[(1-x)(1-y)]
      - x^(d+1)/[(1-x)(1-y/x)]
      + y^(d+2)/[x(1-y)(1-y/x)].
```

The numerator is also zero at d = -1. With independent symbols X = x^U and
Y = y^U, combine all three determinant terms. The result is

    X^2 [(1-xX)/(1-x)]^2 [(1-yY)/(1-y)]^2
                          [(1-yY/(xX))/(1-y/x)]^2,

the square of the complete Weyl character. The A81 symbolic certificate checks
the identity in four independent symbols, rather than finitely many U.

Let F = s_(2U,U,0) h_S^m and rho = (2,1,0). Schur-coefficient extraction
uses every term of sum_(w in S3) sign(w) [x^(nu+rho-w((2U,U,0)+rho))] F.
Writing A = (m-2)S+U and Z = S+U, the targets are

    + (A,Z,Z),
    - (A+U+1,S-1,Z),
    - (A,S+2U+1,S-1),
    - ((m-2)S+3U+2,Z,S-U-2),
    + (A+U+1,S+2U+1,S-U-2),
    + ((m-2)S+3U+2,S-1,S-1).

For U >= 2S, the fourth and fifth have a negative coordinate. In the sixth,
a nonnegative last pair forces the first top coordinate after removing all
tail content to be at least 3U+2-2S > 2U, outside the top character's weight
support; S = 0 is already excluded by the last coordinates. These are complete
support exclusions, not deletions of unfavorable coefficients. Ballot prefixes
are represented by the full Schur extraction; they are not assumed automatic.

For top weight beta of sum 3U its multiplicity is


```text
[1+min(beta_1,beta_2,beta_3,2U-beta_1,2U-beta_2,2U-beta_3)]_+.
```

Indeed the entire two-level interlacing interval has lower endpoint
max(U,Z'-U,beta_1,beta_2), upper endpoint min(2U,Z'), where Z' = beta_1+beta_2.
Its closed length gives the formula, including empty support.

For all raw labeled tails (alpha_i,b_i,c_i), alpha_i+b_i+c_i = S, put
b = sum b_i and c = sum c_i. Their multiplicity is symmetric under exchange
of raw letter totals; this does not permute letters in individual LR tableaux.
The surviving positive radius is


```text
r = b+c-2S + (S-b)_+ + (S-c)_+ + (2S-b-c)_+.
```

The stable negative multiplicities sum, after full b,c exchange, to one full
(S-c)_+ moment. The complete negative multiplicities are


```text
f1 = [S-b-(c-S)_+]_+,
f2 = [min(S-c,b-S,U+2S-b-c+1)]_+.
```

For f2, its other closed bounds are U-2S+b+c+1, 2U+S-b+2,
and 2U-S+c+2. On the only possible support b>S,c<S they are no
smaller than the retained minimum, since U>=2S. Outside that support the
whole weight is zero. The same support check reduces f1 to the displayed
expression. After exchanging b,c in the FULL f1 sum, f1+f2_infinity
sums to (S-c)_+; for c<S this is the exact identity
[S-c-(b-S)_+]_+ + [min(S-c,b-S)]_+ = S-c.
The second negative multiplicity loses exactly


```text
ell(b,c) = min((S-c)_+,(b-U-S-1)_+).
```

Splitting into the four sign cases of b-S,c-S gives the full radius-clipping
correction: (b+c-2S-U-1)_+ + ell(b,c) + ell(c,b). Including the lost
subtracted multiplicity gives three copies of the saturated ell, not three
uncapped simplices. Every row capacity remains in the raw tail multiplicity.

Let D be the whole tail count, L=sum tails (S-c)_+, and
R=sum tails (2S-b-c)_+. The complete affine continuation is
M=[U+1-(2m-6)S/3]D-3L-R. The radius split and the lost negative term
therefore give C=M+sum tails (b+c-2S-U-1)_+ +3 sum tails ell.
Use z_+=z+(-z)_+ on the total slack. Its affine part cancels the
D coefficient in M. Subtracting the saturated loss from L leaves the
complete minimum below. Recenter the total slack, retaining both strict shifts. For N >= 0 put


```text
A_m(N) = [z^N] h_S(z,z)^m/(1-z)^2,
T_m^edge(S,N) = sum_(q=0)^(S-1)
               [x^q y^(N-q)] h_S(x,y)^m/[(1-x)(1-y)].
```

Here h_S(x,y) = sum_(b,c >= 0, b+c <= S) x^b y^c. Since
min((S-c)_+,(N+1-b-c)_+) counts every q with c <= q <= S-1 and b <= N-q,
the entire original, for U >= 2S, is


```text
C_m(S,U) = A_m(U+2S)-3 T_m^edge(S,U+2S)-A_m(2S-1).      (4)
```

The last term is zero when its counting index is negative. This derivation
keeps clipping and the rejected signed partners together. It reproduces the
complete cap organizer supplied in Pro055 U05; it is not a sign theorem for
arbitrary U or an unpaid isolated correction.

At U = 2S, inclusion-exclusion over all physical row capacities leaves exactly
j = 0,1,2,3: four violations require 4(S+1) > 4S. The explicit four-mask
formula in ORIGINALS-AND-GEOMETRY-v1.md follows. For the total masks use


```text
h_S(z,z) = [1-(S+2)z^(S+1)+(S+1)z^(S+2)]/(1-z)^2.
```

For a specified j-element edge violation set, retain its original labels and
substitute b_i = S+1+e_i-c_i. The edge cutoff c <= S-1 guarantees this
substitution is valid. Its complete one-subset count is


```text
sum_(q=0)^(S-1) binom(q+m-j,m-j) binom(S-1-q+j,j)
                              binom((4-j)S-j-q+m,m).
```

Set e = S-1-q, expand the last binomial by Vandermonde, and use
binom(e+j,j)binom(e,p) = binom(p+j,j)binom(e+j,p+j). The remaining full
convolution is binom(S+m,m+p+1), giving exactly the finite p-sum in the
four-mask expression. All early-grade zeros, all strict shifts and the complete
lower diagonal remain. The displayed degree bound and strict physical interior
establish the prior actual degree 2m+1.

## 3. Entire J image and actual complement

At U = 0 the physical top vanishes. Write a boundary tableau Q with totals
B = C = S. The original prefix conditions force b_1 = c_1 = c_2 = b_m = 0.
Its b and c occupations are the first and second rows of a semistandard
rectangle (S,S) on labels 2,...,m. Column strictness says
sum_(j<i) b_j >= sum_(j<=i) c_j, exactly the original 2/3 prefix condition.
It also bounds each label's total occupation by S. The 1/2 condition is then
automatic: its first row is forced, the next two follow from total B = S, and
for i >= 4 the bound is at least 3S. Filling the remaining ones reverses the
map, keeping every physical label.

The complete two-row determinant gives


```text
B_m = binom(S+m-2,m-2)^2
      -binom(S+m-3,m-2)binom(S+m-1,m-2),
```

which simplifies to the full product in section 1. Let q = b_2(Q). Take EVERY
Q and every integer 0 <= r <= q, r <= a <= U, at U = 2S. If a > U-r,
change r ones to twos in tail 1 and use top coordinates x = r,y = 0. If
a <= U-r, keep tail 1 unchanged, change r twos to ones in tail 2, and use
x = -r,y = 0. Both top intervals and every prefix hold. In the lower branch
U >= 2r and the initial gap offsets are (U-2r,U+r); after tail 2 they are
(U,U). In the upper branch the initial offsets are (U+2r,U-r); after tail 1
they are (U,U). Thus no later boundary prefix is lost.

The images are disjoint, distinguished by b_1 > 0 versus b_1 = 0. In the
upper image b_1 recovers r; in the lower image S-B recovers r. Reversing the
single row change recovers Q and a. At r = 0 use only the lower branch.
The full image count is therefore sum_Q sum_(r=0)^q (U-r+1).

For m >= 4, let l = m-3. The complete capacity distribution is


```text
number of Q with capacity q
   = (q+1) [a_l(S)/(S+1)] a_(l-1)(S-q),  0 <= q <= S.
```

Deleting the smallest rectangle label and rotating the residual two-row shape
gives this two-row determinant directly. Full convolution yields


```text
sum_Q q = 2S B_m/(m-1),
sum_Q q(q-1) = 6S(S-1) B_m/[m(m-1)].
```

For m = 3 the single Q has q = S and the same formulas hold. Substituting in
the whole double sum gives J_m = B_m j_m at U = 2S. The lattice maps are
integral and the image has degree 2m-4 for S > 0. E contains EVERY other valid
original tableau, including all five transverse freedoms and genuine nonunit
birth masses. The selected image's own first births are unit-sized. No ordinary
sign of E is inferred from its nonnegative integer cardinality.

## 4. Two full cores and exact finite normal form

Define W_q(r;N) = binom(r+q,q)binom(N-r+q,q),
A_q(N) = binom(N+2q+1,2q+1) and I_q(S;N) = sum_(r=0)^(S-1) W_q(r;N).
The complete telescoper is


```text
W_(q+1) - [(N+2q+2)(N+2q+3)/(2(q+1)(2q+3))] W_q
   = g_q(r+1;N)-g_q(r;N),
g_q(r;N) = r(N-r+q+1)(2r-N-1)W_q(r;N)
                                  /[2(q+1)^2(2q+3)].
```

Canceling factorial ratios proves this as a free-variable polynomial identity.
Sum with BOTH endpoints retained. For


```text
K_q = A_q(4S)-3I_q(S;4S),
L_q = (2q+1)[A_q(3S-1)-2I_q(S;3S-1)],
```

one obtains


```text
K_0 = 1+S,
K_(q+1) = rho_q K_q + Y_q,
rho_q = (1+4S/(2q+2))(1+4S/(2q+3)),
Y_q = 3S(1+2S)a_q(S)a_(q+1)(3S)/[2(q+1)(2q+3)],
L_0 = S,
L_(q+1) = sigma_q L_q + Z_q,
sigma_q = (1+3S/(2q+1))(1+3S/(2q+2)),
Z_q = 2S^3 a_q(S)a_q(2S)/(q+1)^2.                      (5)
```

Every factor and source is ordinary nonnegative. The empty diagonal at S = 0
has its polynomial zero; no negative counting degree is used as a population.

Here is a finite specification of the complete normal form, avoiding an
unbounded edge sum. For j = 1,2,3 let q = m-j and N_j = (4-j)S-j, and set


```text
P_j(r) = binom(S-1-r+j,j)
         product_(h=1)^j(N_j-r+q+h)/(q+1)_rise,j,
alpha_j = sum_(k=0)^(2j) [Delta^k P_j(0)/k!]
          (N_j)_fall,k (q+1)_rise,k/(2q+2)_rise,k.
```

The factorial-moment formula follows by shifting the full Vandermonde sum.
For j = 1,2 solve the polynomial identity


```text
P_j(r)-alpha_j = (r+q+1)(N_j-r)R_j(r+1)
                -r(N_j-r+q+1)R_j(r),
beta_j = S(N_j-S+q+1)R_j(S).
```

The finite rational coefficient solution is unique at degrees 1 and 3,
respectively; all coefficients and both endpoint identities are independently
reconstructed in the A81 linkage certificate. Thus
T_j = alpha_j I_(m-j)(S;N_j)+beta_j W_(m-j)(S;N_j).
For j = 2 the complete half-sum is (V_2+W_center)/2, retaining its center;
for j = 3 the entire support lies below the cutoff and T_3 = alpha_3 V_3.
Define


```text
V_j = binom((4-j)S+2m-3j+1,2m-2j+1),
D_j = (-1)^j binom(m,j)((4-j)S+2m-3j+2)_rise,j
      sum_(p=0)^j binom(j,p)(S+2)^(j-p)
        ((4-j)S-j)_fall,p/(2m-2j+2)_rise,j+p,
W_1 = binom(S+m-1,m-1)binom(2S+m-2,m-1),
W_center = binom(S+m-3,m-2)^2,
W_2 = binom(S+m-2,m-2)binom(S+m-4,m-2).
```

For every m >= 6 the ENTIRE four-mask expression is


```text
C_m = K_m + [D_1+3m alpha_1/2]V_1
      -(3m alpha_1/2) L_(m-1)/(2m-1) + 3m beta_1 W_1
      +[D_2-3binom(m,2)alpha_2/2]V_2
      -3binom(m,2)[alpha_2 W_center/2+beta_2 W_2]
      +[D_3+3binom(m,3)alpha_3]V_3 - R_low.             (6)
```

R_low is the complete R in the four-mask formula. All low-grade support zeros
follow from its nonnegative upper binomial arguments. No m < 6 is substituted
into a negative-index product.

Put V3 = a_(2m-2)(3S), V2 = a_(2m-5)(2S), V1 = a_(2m-8)(S),
W12 = a_(m-2)(2S)a_(m-1)(S), and W11 = a_(m-4)(S)^2. Factorial cancellation
in (6) uniquely defines six rational-in-m polynomial kernels l,p3,p12,p2,p11,p1:


```text
C_m = K_m + l L_(m-1) + p3 V3 + p12 W12
                  + p2 V2 + p11 W11 + p1 V1.           (7)
```

For exact implementation, V_j divided by its corresponding V3,V2,V1 has ratio
3S/(2m-1), 2S(2S-1)/[(2m-3)(2m-4)], and
S(S-1)(S-2)/(2m-7)_rise,3. W_1/W12 = 2S/(m-1),
W_center/W11 = S^2(S+m-3)^2/[(m-2)^2(m-3)^2], and
W_2/W11 = S(S-1)(S+m-3)(S+m-2)/[(m-2)^2(m-3)^2]. The first R_low
binomial belongs to p2; BOTH remaining R_low partners belong to p1. These
rules specify every coefficient of the six kernels; the linkage certificate
checks every free-variable identity against the explicit Pro055 definitions.

## 5. Derive the entire index gain

Write f^+(S,m) = f(S,m+1). The actual product ratios are


```text
r3 = (1+3S/(2m-1))(1+3S/(2m)),
r12 = (1+2S/(m-1))(1+S/m),
r2 = (1+2S/(2m-4))(1+2S/(2m-3)),
r11 = (1+S/(m-3))^2,
r1 = (1+S/(2m-7))(1+S/(2m-6)).
```

Define the full rescaled kernels


```text
h_l = m(l^+ r3-l),
h_i = (m/S)(p_i^+ r_i-p_i),                i = 3,2,11,1,
h_12 = (m/S)[p12^+ r12-p12
               + l^+(2S^3/m^2)(1+2S/(m-1))],
h_J = (m/S)[j_(m+1)(1+S/(m-2))(1+S/(m-1))-j_m].
```

Every division by S cancels exactly. h_l is deliberately NOT divided by S.
Set G_m = C_(m+1)-C_m, H_m = E_(m+1)-E_m and


```text
alpha_m = m[4/(2m+2)+4/(2m+3)],
beta_m = 16m/[(2m+2)(2m+3)].
```

Subtract every term of (7), including the full L source. The exact identities are


```text
(m/S)G_m = (alpha_m+beta_m S)K_m + (m/S)Y_m
          +h_l L_(m-1)/S+h_3 V3+h_12 W12
          +h_2 V2+h_11 W11+h_1 V1,
(m/S)H_m = (m/S)G_m-h_J B_m.                           (8)
```

The complete J kernel simplifies to


```text
h_J = [(4m+1)S^3+(10m^2-8m)S^2
        +(4m^3-5m^2+11m-13)S+2m^3-m^2-9m+12]
                     /[(m-2)(m-1)(m+1)].
```

After m = 3+x each numerator coefficient is a positive polynomial in x;
the denominator is positive. Thus the entire J gain is ordinary nonnegative
for all m >= 3. This is an exact polynomial argument, not a count injection
between different dimensions.

## 6. A uniform paid bound for all m >= 96

Complete finite expansion of recurrence (5) gives


```text
K_6 >=_coef (11/16)a_13(4S).
```

Multiplication by the positive subsequent factors and retention of every
positive source imply K_m >= (11/16)D_m. For the other core, sorted factor
lists give a_p(aS)a_q(bS) <= a_(p+q)((a+b)S). This follows by comparing
cumulative reciprocal-denominator counts floor(ax)+floor(bx) <= floor((a+b)x).
Apply it to every complete source in the L recurrence, inserting the two
missing positive factors. The bound sum_(r>=1) r^-2 < 5/3 gives


```text
0 <=_coef L_(m-1)/S <=_coef (1+10S^2/3)V3.
```

All bases V3,V2,V1,W12,W11 are dominated by F3 = a_(2m+1)(3S), and B_m
by F2 = a_(2m+1)(2S). No arbitrary positive polynomial is canceled.

For m >= 96,


```text
alpha_m-39/10 = (2m^2-95m-117)/[10(m+1)(2m+3)] > 0,
beta_m-alpha_m/(m+2) = 6m/[(m+1)(m+2)(2m+3)] > 0.
```

The first numerator becomes 2x^2+289x+9195 at m = 96+x. Consequently
(alpha_m+beta_m S)K_m >= (429/160)T_m, retaining the extra leading degree.

For each complete h kernel substitute m = 96+x. Its positive denominator
D(x) depends only on x. For a numerator coefficient N_i(x), define


```text
b_i = max(0, max_h {- [x^h]N_i/[x^h]D})
```

for the six non-J kernels. For h_J use the positive version of this ratio to
obtain an upper majorant b_J. Clear denominators and check all padded residual
coefficients. The independent A81 symbolic reconstruction gives all 50 bounds
and 354 residual slots; no sampled m replaces these free-variable inequalities.
Put


```text
R(S) = b_l(S)(1+10S^2/3)+b_3+b_12+b_2+b_11+b_1,
Jbar(S) = b_J(S).
```

The complete arrays are in the frozen arithmetic evidence. R has degree 10
and Jbar degree 3. Their NONZERO constants are 48/12545 and 879702/433105.
Equation (8), including the entire J subtraction, now gives


```text
(m/S)H_m >=_coef (429/160)T_m - R F3 - Jbar F2.          (9)
```

Only the explicitly positive K source was omitted in this lower bound. The
error polynomial can have higher degree; the next comparison covers every
coefficient of the actual target, and never assigns those extra degrees to H.

## 7. Independent original-only finite bridge and every higher degree

For any positive linear-factor product with coefficients e_d, adding another
positive factor cannot increase e_(d-j)/e_d for 0 <= j <= d in the existing
degree range. The coefficients are log-concave: induction under multiplication
by (1+wS) expands the relevant difference into

    (a_i^2-a_(i-1)a_(i+1))
    +w(a_i a_(i-1)-a_(i-2)a_(i+1))
    +w^2(a_(i-1)^2-a_(i-2)a_i),

all nonnegative by the ordered adjacent ratios, including zero endpoints.
Cross-multiplication of the new ratio proves the assertion.

For ORIGINALS, no quotient deletion is needed. Every D_m at m >= 96 contains
the complete normalized product with integer numerator


```text
P0(S) = product_(r=1)^193 (r+4S) = sum_(d=0)^193 c_d S^d.
```

These are 193 CONSECUTIVE factors, unlike Pro055's 193-factor quotient
list obtained by removing the multiples of four from 1,...,257. The moving final factor of T_m need not be nested: it is an extra
positive factor. Also [S^r]Fb <= (b/4)^r [S^r]T_m for b = 2,3.
Therefore for EVERY d = 0,...,193,


```text
[S^d](R F3+Jbar F2)/[S^d]T_m <=
  sum_(j=0)^min(10,d) R_j(3/4)^(d-j)c_(d-j)/c_d
  +sum_(j=0)^min(3,d) Jbar_j(1/2)^(d-j)c_(d-j)/c_d.
```

The independent complete 194-degree rational certificate bounds each expression
strictly below 21/10. Its maximum is the constant
2211330126/1086660445. Every c_d, ratio and gap is retained.

For d >= 194, restrict a target to its first d factors. If d <= 2m+1, its
reciprocal-slope sum is d(d+1)/8. At the highest degree d = 2m+2, append the
reciprocal m+2, giving (d^2+3d+8)/8 <= P(d) = d(d+4)/8. Thus the EXTRA
leading-degree factor is accounted for. At exactly d factors, the complementary
elementary-symmetric identity and the full jth-power expansion give


```text
[S^(d-j)]T/[S^d]T <= P(d)^j/j!.
```

Adding the remaining factors decreases this ratio. The complete error ratio is
therefore bounded by


```text
U_d = sum_(j=0)^10 R_j(3/4)^(d-j)P(d)^j/j!
      +sum_(j=0)^3 Jbar_j(1/2)^(d-j)P(d)^j/j!.
```

Every summand decreases for d >= 194: its consecutive ratio is at most


```text
(3/4)[(d+1)(d+5)/(d(d+4))]^10 < 1.
```

The inner ratio decreases, since the derivative of (2d+5)/(d^2+4d) has
numerator -2d^2-10d-20. Exact arithmetic at d = 194 verifies both inequalities,
with U_194 approximately 0.0005120600464, well below 21/10. The rational value,
not this decimal, is the certificate. This proves the comparison in ALL higher
degrees through the actual target degree, not merely for fixed d as m grows.

Combining with (9) gives (m/S)H_m > (93/160)T_m >= (1/2)T_m in every
coefficient through degree 2m+2. Above that degree both the actual gain/S and
target are zero. Multiplication by S/m proves the large-index part of (1).
The positive full J gain then proves the C comparison.

## 8. Complete finite exceptions and ordinary-coefficient compensation

The necessary complete transitions are m = 3,...,95. They use the existing
supplied endpoint originals m = 3,...,96. The actual independent run produced
107 complete endpoints m = 3,...,109 before root improved the uniform proof.
The additional endpoints 97,...,109 remain complete overlapping controls.
The original roster's 110,...,128 are explicitly unexpanded; they are no
longer proof obligations because the exact uniform bound starts at 96.
All interrupted attempts and observed charges remain preserved. Each endpoint is reconstructed from
the full four-mask expression and the separately authored complete core/kernel
expression (with explicit small-index formulas where needed), retaining its
prior lattice, actual degree, all signed masks and every lower-diagonal term.
The B determinant and product give independent component arithmetic. No provider
program is executed and no finite index panel supplies the uniform quantifier.

Every full G vector is compared with S T_m/(4m). Every full H vector at m >= 4
receives the same comparison. H_3 is retained as the deliberate complete
countercontrol in (2). Complete positive bases C_3,E_3,E_4 plus these gains and
the uniform large-index proof establish the selected endpoint signs. The selected finite arithmetic contains 93 complete G/reserve transitions
(9,486 dense slots), 92 positive H/reserve transitions (9,476 dense slots),
and the entire H3/G3/J compensation. All eight targeted negative controls
pass. The source comparison joins every C/E field of the 107 actual endpoints
and every selected complete gain, target and reserve, with zero differences.
These are independently reconstructed all-grade identities, not new scalar
LR requests. The actual evidence pins and remaining bare-original join must
pass the single gate before adoption. The independent bare-triple B4/B6 checks freeze both
complete ordinary representations before four genuinely unused grade values.

For b > a >= 3, the paid operation iterates as


```text
C_b-C_a >=_coef sum_(r=a)^(b-1) S T_r/(4r).
```

For E the same statement holds for b > a >= 4. The endpoint lattices have their
own dimensions and physical rows; this is a coefficient comparison, not a
claimed tableau injection between them. The positive leading term has the
larger endpoint's degree because the smaller endpoint and J have lower degree.

## 9. Provenance, claim ceiling and remaining reach

The complete source chain is Pro055 U03–U11, with all original bytes and
failures retained by the final intake. Root rederived the original chart,
character and cap recentring, the full capacity-limited J injection, the
four-mask convolution, and the coefficient comparison. Fresh trusted code
independently reconstructs the free-variable identities and finite certificates.
The new original-only 193-factor bridge avoids quotient obligations; no quotient
result is promoted by this argument. Internal model review is not human review,
formal certification, public-release authority or a claim of worldwide novelty.

This proves a composable operation on an unbounded complete original family.
It leaves the full u interval, rho-normalized gain, arbitrary LR shapes, longer
content, whole rank seven and unrestricted KTT open. Pro054's complete fixed
low-overlap and connected moving-prefix theorems remain separately processed
unadopted source until their own complete original/base/transfer reconstruction. The old
A80 collar and prior transportation theorems retain their exact domains.
