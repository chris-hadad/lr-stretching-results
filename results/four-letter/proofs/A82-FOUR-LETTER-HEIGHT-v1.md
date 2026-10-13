# A82: a complete four-letter original and paid height operation

Curated mathematical proof from **A82**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Provenance is Pro057 Phase 0,
U03 and U04. The root argument below retains the entire original. No returned
program is executed. Earlier accepted results and all other provider claims keep
their exact status. This is not whole rank seven or unrestricted KTT.

## 1. Literal theorem and a terminating cover

Let m >= 3, s > 0 and u >= 3s be integers. Retain every displayed physical row:


```text
lambda = (ms+6u, ms+5u, ms+4u, ms+3u, ms, (m-1)s, ..., s),
mu = (ms+3u, ms+2u, ms+u, ms, (m-1)s, (m-2)s, ..., 0),
nu = ((m-3)s+6u, s+3u, s+2u, s+u).
```

Lambda is outer. These are partitions without sorting, with containment and
skew/content size ms+12u. They have m+4 physical outer rows and four positive
content parts. The entire polynomial C_(m;s,u)(t) is strictly positive in every
ordinary degree 0 through its prior actual degree d = 3m+3. At s = 0 the original
is exactly 1+ut: degree one if u > 0, and the point otherwise.

There is a full polynomial W_m(S), strict in degrees 0 through 3m+2, such that


```text
C_m(S,U+V)-C_m(S,U) = V W_m(S),  U >= 3S, V >= 0.       (1)
```

On physical stretching rays S=st, U=ut and V=vt, the gain is vt W_m(st),
strict in every nonconstant degree through d if s,v > 0. Both full endpoints
and the baseline F_m(S)=C_m(S,3S) are paid. Reducing u to 3s decreases the
nonnegative integer u-3s and terminates at that actual legal baseline. This is
an original-generating cover of exactly this family; no unproved index-gain or
arbitrary-shape cover is inferred.

## 2. Complete original tableau chart and saturated lattice

Write a_(i,k) for the number of letter k in physical row i. Nonnegative row
entries, the literal row/content sums, and ALL inequalities


```text
mu_(i-1)-mu_i + sum_(j<k) a_(i-1,j)-sum_(j<=k) a_(i,j) >= 0,
sum_(r<i) a_(r,k)-sum_(r<=i) a_(r,k+1) >= 0, k=1,2,3,
```

are respectively the adjacent column conditions and worst reading-word ballot
prefixes of the unique weakly increasing fillings. Each worst prefix occurs
while the k+1 letters precede the k letters in that row. Thus these conditions
are equivalent to every tableau constraint, including the fourth-letter ballot.

The first row is (3U,0,0,0); ballot conditions force entries above the top
letter diagonal to zero. Put x=U-a_(2,1), y=U-a_(3,1), z=U-a_(4,1), and let
B,C,D be total tail counts of letters 2,3,4. The first-letter column and content
conditions give


```text
x,y,z >= 0,  x+y+z+B+C+D = 3S.                         (2)
```

Every labeled tail remains (S-b_i-c_i-d_i,b_i,c_i,d_i), with all four entries
nonnegative. In particular b_i+c_i+d_i <= S is a coupled physical capacity.
With p=a_(3,2), ALL top rows are reconstructed as

    (3U,0,0,0),
    (U-x,2U+x,0,0),
    (U-y,p,2U+y-p,0),
    (U-z,U+S-x-B-p,S-y-C+p,U+S-D).                         (3)

The inverse reads x,y,z,p and the labeled tails from the original. One may use
x,y, all 3m tail entries and p as free coordinates and eliminate z using (2).
Both maps have integer coefficients and coefficient-one elimination; hence the
original difference lattice is saturated Z^(3m+3), with no altered residue.
This is a tableau lattice statement, not a character-exponent substitution.

Before imposing U >= 3S, the complete nonautomatic top bounds are


```text
x,y,z <= U, p >= 0, p <= 2U+y, p <= U+S-x-B,
p >= y+C-S, D <= U+S,
p <= U-x+y, p >= S-x-B+y-z, p >= y-S+D,
p <= 2U-2x, p >= y-x, 2U >= S+x+y-B,
p >= S-C-x, p <= U+y-S+D.                              (4)
```

The last upper bound is exactly the top row-four 3/4 ballot; it is indispensable.
All remaining top tests are forced equalities or automatic nonnegative forms.

## 3. Stable interval, all tails and actual degree

Let Omega_m(S) be exactly the configurations in (2) with all labeled coupled
capacities. For U >= 3S, (4) is equivalent to


```text
L <= p <= U+h,
L=max(0,y-x,S-C-x,y+C-S,S-x-B+y-z,y-S+D),
h=min(y-x,S-x-B,y-S+D).                                (5)
```

Indeed x+y+z+B+C+D=3S bounds each nonnegative term by U and makes
2U >= S+x+y-B automatic. Also U-x+y <= 2U-2x and <= 2U+y, so these upper
bounds are redundant at exactly this domain. Nothing is continued below it.

Tail columns are disjoint: each lower row ends at its preceding inner boundary.
For each tail i, with previous tail subtotals denoted by a subscript prev,
the three worst ballot slacks are bounded below respectively by


```text
3U-(x+y+z)-S >= 3U-4S,
U-(B-B_prev)+(C-C_prev-c_i) >= U-B,
U-(C-C_prev)+(D-D_prev-d_i) >= U-C.
```

They are nonnegative at this domain, for every physical prefix. The labels and
capacities that make these bounds valid have not been replaced by totals alone.

L >= h. On the simplex (2), maxima of the eighteen lower-minus-upper-offset
forms, divided by S, in the orders of (5), are

    (3,2,1), (0,2,1), (1,3,2),
    (2,1,3), (1,3,2), (2,1,0).

For a linear form cS+sum a_i v_i on v_i >= 0, sum v_i=3S, the maximum is
(c+3 max a_i)S. This derives every entry without counting. Thus L-h <= 3S,
and every configuration has the full uncut interval U+1+h-L.

For S>0 choose all 3m tail non-one entries and x,y,z equal to S/(m+1),
and p=U/2. The relation (2) holds; tail ones are (m-2)S/(m+1)>0. In (5)
L=h=0. Every nonforced original inequality has positive slack, including the
bounds discarded above and every tail prefix. A rational open box in the
saturated chart therefore gives growth of exact degree 3m+3. Sections 5-6
supply explicit all-grade polynomials of degree at most 3m+3 before any fitting,
so the actual polynomial degree is established directly. No external
polynomiality theorem, integral-vertex assumption or finite interpolation is
needed for this selected stable-domain proof. At S=0, Omega has one point and
(5) is 0 <= p <= U, proving the interval/point convention separately.

## 4. Entire height operation and symmetry, with all compensation

Holding x,y,z, every tail, and p fixed while increasing U by V adds to the four
top rows respectively

    (3V,0,0,0), (V,2V,0,0), (V,0,2V,0), (V,V,0,V).

The full interval (5) proves legality. Subtraction is its inverse on the image;
increments compose. The image is full-dimensional, not asserted to be a face.
Its entire complement has V choices per Omega configuration. Therefore (1)
holds with


```text
W_m(S) = [q^(3S)] (1-q)^(-3) f_S(q)^m,
f_S(q) = sum_(r=0)^S binom(r+2,2) q^r.                 (6)
```

For J_m(S)=sum_Omega (x+B-S)_+, the complete count is


```text
C_m(S,U) = (U+1)W_m(S)-4J_m(S).                        (7)
```

Here is the full compensation proof. Put A=y-x, E=y+C-S,
M=max(0,S-C-x,y+D-S). The total equation gives the pointwise identities
L=E_+ + M and h=A+min(0,S-B-y,x+D-S). Omega is preserved by permutations of
the three deficits and, separately, a global common permutation of the three
non-one entries in every labeled tail; every capacity remains. These act on the
complete configuration sum, not as a claimed symmetry of individual tableaux.
The sums of A and x+B-S are zero. The negative of the last minimum has the same
sum as M. Put a=x+C-S,b=y+D-S,c=z+B-S, so a+b+c=0 and the distributions agree.
Exchanging a,b makes max(0,-a,b) equidistributed with -min(0,-a,b).
The range of (0,-a,b) is (|a|+|b|+|c|)/2. Hence 2 sum M=3 sum a_+,
while sum E_+=sum a_+=J. Thus sum(L-h)=4J, proving (7). Also
J=sum_Omega(S-x-B)_+. All ties, zero terms and both sides of the moment remain.
In general L-h is NOT pointwise 4(x+B-S)_+.

## 5. Full capacity and moment polynomials

Write a_n(v)=product_(r=1)^n(1+v/r), a_0=1, and put


```text
M_m=a_(3m+2)(3S), A_m=a_(3m-1)(2S), B_m=a_(3m-4)(S),
P_m=a_(m+1)(S)a_(2m+1)(2S).
```

At total 3S, three distinct row violations would require 3(S+1)>3S.
All zero-, one- and two-capacity subsets are retained. For one violated row
its residual r has multiplicity binom(S+3+r,2). Its full generating function
is [c0+c1 q/(1-q)+q^2/(1-q)^2]/(1-q), c0=(S+3)(S+2)/2,c1=S+3.
With `d_h=[q^h](c0+c1 q+q^2)^2`, the complete inclusion-exclusion yields


```text
W_m=M_m-S p_m A_m+S(S-1)q_m B_m,
p_m=(2/3)[c0+(S+3)(2S-1)/(3m+1)
                +(2S-1)(2S-2)/((3m+1)(3m+2))],
q_m=m/[6(3m-2)] sum_(h=0)^4
             d_h(S)(S-2)_fall,h/(3m-1)_rise,h.           (8)
```

Every labeled subset has multiplicity m or binom(m,2), and each strict S+1
shift is present. An independent numerator construction uses


```text
f_S(q)=[1-binom(S+3,2)q^(S+1)
            +(S+1)(S+3)q^(S+2)-binom(S+2,2)q^(S+3)]/(1-q)^3.
```

For j specified violating rows let J_j be the lower moment (S-x-B)_+, leaving
the other capacities unrestricted. The ENTIRE moment is


```text
J=J_0-mJ_1+binom(m,2)J_2,
J_j=sum_(h=0)^j sum_(v=0)^(j-h)
   (-1)^h binom(j,h)binom(j-h,v)(S+1)^v
   sum_(i=0)^(2m+1-h-v)
    binom((2-j)S+2m+2-j-v,2m+1-h-v-i)
    binom(j+h+1+i,i) binom(S+m+1,m+h+2+i).               (9)
```

To derive this, restrict R=x+sum b_i <= S-1. A violated row has
c_i+d_i >= S+1-b_i>0, with series
q^(S+1-b_i)[(S+2-b_i)-(S+1-b_i)q]/(1-q)^2. Summing the j selected b_i and
the lower moment gives, for the subtotal r of x and unselected b_i,


```text
sum_h (-1)^h binom(j,h)[1+(S+1)(1-q)]^(j-h)(1-q)^h
                                  binom(S-r+j,j+h+1).
```

The unselected subtotal has binom(r+m-j,m-j) compositions. Expand the bracket
by v and extract the remaining q power; its coefficient is
binom((3-j)S+2m+1-j-h-v-r,2m+1-h-v). Substituting S-1-r=h+z, expanding
in binom(z,i), and using Vandermonde gives exactly (9). Both endpoint slacks
and the full i range remain. Each term has degree at most 3m+3. At S=0,1 the
single/double violations have exact polynomial zeros: their counting arguments
are nonnegative and below their lower indices. No negative-top continuation is
counted as a population. Equations (7)-(9) are complete all-grade formulas.

## 6. Positive one-cap moment and complete double-cap combination

The uncapped moment is J_0=(2S/3)P_m. For k=m+1, l=2k and T=3S, set
w_r=binom(r+k-1,k-1)binom(T-r+l-1,l-1) and b_r=r(T-r+l)w_r.
Then b_(r+1)-b_r=3k(S-r)w_r. Summing r=0,...,S-1 retains both endpoints
and proves that entire identity.

Define V_m=sum_(k=0)^(2m) binom(S+3m-k-1,3m-k)binom(S+k-1,k), and
D1=9(m+1)(2m+1)(3m+1)(3m+2). Put


```text
Q=2/D1[(4m^3+10m^2+15m+7)S^2
         +(26m^3+83m^2+71m+18)S+(51m^3+96m^2+58m+11)],
R=2/[9(3m+1)(3m+2)] [(2m^2+10m+12)S^3
         +(21m^2+51m+18)S^2+(46m^2+41m+6)S+12m^2+6m].
```

The exact positive decomposition is


```text
J_1=S^2 a_(m-1)(S)a_(2m)(S)Q+R V_m.                     (10)
```

For a direct finite telescoping certificate, the full sum before (9) at j=1
is sum_(r=0)^(S-1) w_r f(r), with
w_r=binom(r+m-1,m-1)binom(2S-1-r+2m,2m) and
f(r)=(S-r)(S-r+1)[(2m+4)S+7m+2+(m-1)r]/[3(2m+1)].
For T=2S-1 the exact identity is


```text
f(r)=(r+m)(T-r)b(r+1)-r(T-r+2m+1)b(r)+R,
b(r)=b0+b1 r+b2 r^2,
b0=[(23m^3+82m^2+85m+26)S^2
    +(97m^3+262m^2+205m+48)S+102m^3+192m^2+116m+22]/D1,
b1=-[(2m^2+20m+14)S+15m^2+27m+12]/[9(m+1)(2m+1)(3m+2)],
b2=-(m-1)/[9(m+1)(2m+1)].
```

Expansion in r proves it as a free-variable rational identity; b(S)=Q.
The boundary S(T-S+2m+1)w_S is S^2 a_(m-1)(S)a_(2m)(S).
The remaining sum of w_r is V_m: encode 3m nonnegative coordinates by their
weak cumulative sums ending at most 2S-1, with the mth sum at most S-1.
Exactly k=0,...,2m cumulative sums lie at least S. The two disjoint blocks
have the multiset counts in V_m, preserving the boundary S. All its factors
are rising products with nonnegative coefficients. Therefore J_1 is positive
through degree 3m+3 outside its zero constant; it may be discarded only after
this complete coefficient proof.

The double-cap combination is


```text
binom(m,2)J_2=S(S-1)B_m r_m,
H_m=(3S+1)q_m-4r_m,
r_m=binom(m,2) sum_(h=0)^2 sum_(v=0)^(2-h)
  (-1)^h binom(2,h)binom(2-h,v)(S+1)^v
  sum_(i=0)^(3+h) binom(4,3+h-i)binom(2m+1-h-v+i,i)
   (S-2)_fall,i (S+3m-3)_rise,(2-h-v)
                     /(3m-3)_rise,(4-h-v+i).            (11)
```

It follows by setting n=S-2-r in the j=2 subtotal, expanding
binom(n+4,3+h) in binom(n,i), and performing the full convolution. Its
finite lengths h<=2,v<=2-h,i<=5 are independent of m. The factor S(S-1)
retains both empty grades and is never declared coefficientwise positive.

## 7. Exact all-index majorants and paid infinite tails

Let


```text
pbar=2+2S+S^2/2,
qbar=1411/1320+4457S/2520+40049S^2/36960
                      +1009S^3/3465+51S^4/1760,
Hbar=409/1458+1579S/1215+45475S^2/22176
                      +34549S^3/22176+3947S^4/7392+2509S^5/36960.
```

For every m>=3, the complete finite rational functions satisfy


```text
p_m <=_coef pbar, 0 <=_coef q_m <=_coef qbar,
0 <=_coef H_m <=_coef Hbar.                             (12)
```

These bounds concern every coefficient, not values at positive S. For q and H,
substitute m=x+3 into the explicit finite expressions (8),(11), clear their
positive denominators and compare every numerator coefficient. The exact
positive numerator and nonnegative residual lists are independently reconstructed
in the A82 free-variable certificates. A finite index grid cannot replace this
step. Equivalently the q upper bound follows from m/[6(3m-2)]<=1/14 and
|(S-2)_fall,h|_coef <= (S+2)_rise,h with denominators at least (8)_rise,h;
this expands to the entire qbar. The three explicit coefficients of p give
its bound. For Hbar each scalar is the maximum ratio of matching nonnegative
shifted numerator/denominator coefficients; the full residual has nonnegative
coefficients in x. All denominators are strictly positive for x>=0.

Sorted positive-factor slopes prove P_m <=_coef M_m: the count of slopes from
{1/i}_{1..m+1} and {2/i}_{1..2m+1} above a threshold is bounded by that for
{3/i}_{1..3m+2}, using floor(a)+floor(b)<=floor(a+b). This is coefficientwise
factor domination, not cancellation from an inequality.

Define two complete sufficient polynomials, distinguished by superscripts:


```text
G^W_m=M_m-S pbar A_m-S qbar B_m,
G^F_m=(1+S/3)M_m-S(3S+1)pbar A_m-S Hbar B_m.
```

Their exact full residual payments are


```text
W_m-G^W_m=S(pbar-p_m)A_m+S(qbar-q_m)B_m+S^2 q_m B_m,
F_m-G^F_m=(8S/3)(M_m-P_m)+S(3S+1)(pbar-p_m)A_m
               +4mJ_1+S^2 B_m H_m+S B_m(Hbar-H_m).     (13)
```

Every sign on the right was independently proved first. This accounts for the
entire actual baseline and both moments at the SAME ordinary coefficient.
Negative low-index G^F coefficients are failures of that sufficient bound;
their full positive F and compensation remain, not a purported LR candidate.

Let R_M=product_(i=0)^2(1+3S/(3m+3+i)),
R_A=product_(i=0)^2(1+2S/(3m+i)),
R_B=product_(i=0)^2(1+S/(3m-3+i)). These are the exact consecutive ratios.
For m>=3, cross-multiplication gives respectively 3m+i-6>=0 and
6m+2i-12>=0, so R_M dominates both R_A and R_B factor by factor.
For either superscript, the complete recurrence residual
G_(m+1)-R_M G_m is the sum of the two negative-base factors of G_m,
with their signs reversed, times R_M-R_A and R_M-R_B. It is nonnegative.

The independently reconstructed full G^W_3 has 12 strict ordinary slots.
The full G^F_12 has 40 strict slots. Exact multiplication, not provider PASS,
binds both starts to their defining expressions. Thus the recurrence proves
W_m strict through degree 3m+2 for every m>=3, and F_m strict through degree
3m+3 for every m>=12. The nine EXISTING complete F_m bases m=3,...,11 have
225 ordinary slots, all recomputed from both (9) and (10)-(11) and frozen before
unadopted source comparison. Those finite bases complete the remaining indices. They are
reuse of supplied all-grade originals, not new scalar requests or an all-index
claim extrapolated from a panel.

A quantitative root corollary retains the paid reserve explicitly:


```text
W_m >=_coef G^W_3 product_(r=12)^(3m+2)(1+3S/r), m>=3;
F_m >=_coef G^F_12 product_(r=39)^(3m+2)(1+3S/r), m>=12.
```

Empty products are one. Multiplying the first reserve by vt gives the full
height-gain lower bound. No analogous inequality for the RAW index gain is
claimed. The complete finite and free-variable certificates remain necessary
parts of this proof, with the actual A82 CHECKS and gate governing adoption.

## 8. Verification, failure controls and reach

Root checks all original geometry and the eighteen full interval comparisons;
meaningful hostile controls retain row-four 3/4 ballot deletion, coupled-capacity
deletion, the false pointwise moment replacement, missing double caps, and the
full low-index sufficient-bound negatives with their same-parent compensation.
The stable identity is not extrapolated below 3S: the supplied m=3,s=u=1
control has a different complete count from the formal affine extension.
Those historical observations remain unadopted source unless freshly reconstructed.

The operation frees height above a UNIFORM 3s threshold and proves a complete
family with four content letters at arbitrary rank m+4. Its prior degree
3m+3 exceeds the upper bound 2R-5 for a three-letter original at R<=m+4,
so it is not the same complete stretching polynomial as a three-letter
original at equal or lower rank. This does not exclude higher-rank transfers
or decompositions. All s<=u<3s four-letter originals, arbitrary shapes,
whole rank seven, and unrestricted KTT remain open. No public-release,
formal-certification, human-review or worldwide-novelty claim follows.
