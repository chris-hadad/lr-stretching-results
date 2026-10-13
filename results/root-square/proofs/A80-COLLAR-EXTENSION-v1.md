# A80: complete pre-collar reflection, payment and augmentation

Curated mathematical proof from **A80**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Proposed root theorem, 7 October 2026.  The original family and
upper-collar moments come from completed Pro053 U02; root reconstructs their
load-bearing arguments below. New Pro055 U02/U03 independently supplies the
full prefix chart and warns that a universally positive correction is false.
No active-provider theorem is adopted merely by reading it. Related literature
suggest complete cancellation and ballot accounting; the identities here are
proved directly, not deduced from their different positive quantities.

## 1. Complete original and claimed result

For integers m>=3 and s,u>=0 retain all m+3 physical rows, including zeros:


```text
lambda=(ms+4u,ms+3u,ms+2u,ms,(m-1)s,...,s),
mu=(ms+2u,ms+u,ms,(m-1)s,(m-2)s,...,0),
nu=((m-2)s+3u,s+2u,s+u).
```

Lambda is outer, both shapes are partitions, lambda contains mu, and both skew
area and content size are ms+6u. Set S=st, U=ut and h_m=max(3,m-2).
The proposed conclusion is strict ordinary-coefficient positivity of the
ENTIRE stretching polynomial C_m(st,ut) through its actual degree whenever
u>=h_m*s. For s>0 the degree is 2m+1. For s=0 the entire original is 1+ut,
including the point at u=0. The result imposes no bound on m or s or u.

The complete augmentation operation, for v>=u>=h_m*s, also satisfies


```text
C_m(st,vt)-C_m(st,ut)
  >=_coef (v-u)t a_(2m-1)(st)[1+(1-3/(2m))st],      (A)
a_j(z)=binom(z+j,j).
```

Thus its gain is strict in every nonconstant degree through 2m+1 when s>0
and v>u. The gain is exactly (v-u)t on s=0. This extends the paid collar
u>=ms down by one width for m=4 and two widths for every m>=5; m=3 retains
its original bound. The lower pre-collar region and unrestricted KTT remain
open. This is neither an all-parameter collar theorem nor an arbitrary-shape
or arbitrary-rank theorem.

## 2. Literal tableau chart and every constraint

At integer grade the top skew shape, after horizontal translation by mS, is
(4U,3U,2U)/(2U,U,0). The m tail rows are disjoint intervals of width S.
Put tail row i equal to (d_i,b_i,c_i), with d_i+b_i+c_i=S and all entries
nonnegative. Let B=sum b_i, C=sum c_i, x=B-S, y=C-S.
The forced top first row has 2U ones; row two has a ones and 2U-a twos;
row three has U+x+y-a ones, a-x twos and U-y threes. All top column and
ballot inequalities are exactly


```text
max(0,x,y,x+y,-x)<=a<=U+min(0,x+y,y).
```

The untruncated interval length is U+1-phi, where


```text
phi=max(B+C-2S,B-C,C-S,3S-2B-C).
```

Every tail 1/2 and 2/3 prefix respectively requires


```text
h12_i=(4-i)S-b_i-c_i-2B_after_i-C_after_i<=U,
h23_i=B_from_i-C_after_i<=U.                       (P)
```

These follow by reading the threes, then twos, then ones within each weak row.
The top ending gaps are U+2B+C-3S and U-B+C. Neither condition depends on a.
Consequently the complete count is the sum of (U+1-phi) over ALL ordered
tails for which U>=phi and every inequality (P) holds. Rejection uses the
union of failed prefixes, not the sum of their individual populations.

All coordinates (b_i,c_i,a) and their inverse are integral, proving the
original affine lattice is saturated Z^(2m+1) on a full-dimensional domain.
In the claimed positive-s domain choose b_i=c_i=d_i=S/3 and choose a strictly
between 2(m/3-1)S and U. This interval has positive length because
U>=h_m*S>2(m/3-1)S. Every nonforced top and tail inequality is strict; in
particular the 2/3 tail gap is U>S/3 and the 1/2 gap is U+(m-3)S>S/3.
Hence the chart has dimension 2m+1 BEFORE reconstruction. No integral-vertex
or total-unimodularity assertion is made about this nontransportation chart.
The all-grade polynomial identities below and positive leading coefficient
give its actual polynomial degree independently of any interpolation.

## 3. Complete affine continuation and its exact moments

Let T_m(B,C) count all ordered tail triangles with totals B,C. It is symmetric
in B,C, has total D_m(S)=((1+S)(1+S/2))^m, and first sum of B+C equal to
2mS*D_m/3. The pointwise identity


```text
phi(x,y)+phi(y,x)
  =2(x+y)+3[(-x)_++(-y)_+]+2(-x-y)_+
```

gives the exact signed affine sum over ALL tails:


```text
M_m(S,U)=[U+1-(2m-6)S/3]D_m(S)-3L_m(S)-R_m(S),  (M)
L_m=sum T_m(B,C)(S-B)_+,
R_m=sum T_m(B,C)(2S-B-C)_+.
```

The moments include every tail cap and strict shift. Expanding
((S+1)/(1-z)-z/(1-z)^2)^m and summing the closed slack gives


```text
L_m=sum_(j=0)^m (-1)^j binom(m,j)(S+1)^(m-j)
                                  binom(S+m,m+j+1).
```

For R, each w_i=b_i+c_i has multiplicity w_i+1 and lies in [0,S]. Below
the strict total 2S, at most one w_i>=S+1 can occur. Retaining its full
weight S+2+r and every labeled choice gives


```text
R_m=binom(2S+2m,2m+1)
   -m[(S+2)binom(S+2m-2,2m)+binom(S+2m-2,2m+1)].
```

These are finite identities at EVERY nonnegative integer S, including S=0,1;
their falling-product polynomials have the required empty initial zeros.
M need not equal the original outside the domains proved next. Its omitted
clipping and ballot populations must not be discarded or signed separately.

## 4. Full two-letter reflection and exact second-band correction

Suppose U>=3S. Every h12_i<=3S, so all 1/2 tail prefixes are automatic.
For fixed totals B,C and a valid initial top interval, the initial 2/3 gap is
g=U-B+C>=0 and the final gap is U. The complete number of tails satisfying
all 2/3 prefixes is


```text
T_m(B,C)-T_m(B+g+1,C-g-1)
  =T_m(B,C)-T_m(U+C+1,B-U-1).                     (R)
```

Here negative arguments mean zero. This is a complete weak-row reflection,
not reflection of independently labeled unit steps: fix the ones d_i in each
tail row. Its remaining weak row contributes the two-variable character
h_(S-d_i)(X,Y). Tensor it with h_g(X,Y). Multiplication by 1-Y/X cancels the
finite h_g string to 1-(Y/X)^(g+1), giving exactly the two coefficients in
(R). The two-variable Pieri rule itself follows by multiplying the finite
strings: h_g h_k=sum_(r=0)^min(g,k) (XY)^r h_(g+k-2r).
Its summation index r is the number of threes in the appended weak row, and
the conditions r<=g,k are exactly that row's 2/3 prefix bound. Induction on
the physical rows proves (R), preserving every multiplicity and prefix.
Finally sum over ALL d_i; this recovers T with each tail counted once.

Write L(B,C)=(U+1-phi(B,C))_+. Reindexing the ENTIRE second term of (R)
shows that C-M is the sum against T(B,C) of


```text
(phi(B,C)-U-1)_+
   - 1[B>=U+1] L(U+C+1,B-U-1).                  (E)
```

Also suppose m>=5 and U>=(m-2)S. Then B+C<=mS<=U+2S and U>=3S. Therefore
the first term of (E) is exactly

    (B-C-U-1)_+ + (C-U-S-1)_+.

These two possible clipping regions are disjoint; the other two phi branches
are at most U. Put z=B-C-U-1 and A0=U+1+2S-B-C>=1. The reflected length
in (E) equals min(A0,z)_+. Indeed its two relevant phi branches are
B+C-2S and 2U+C-B+2; its remaining branches are dominated, and z>0 already
implies B>=U+1. Thus z_+-min(A0,z)_+=(z-A0)_+=2(B-U-S-1)_+.
Symmetry of T in B,C gives the COMPLETE correction


```text
C-M=3 sum_(B,C) T_m(B,C)(B-U-S-1)_+.              (C)
```

Set q=(m-1)S-U. If q<=0 the correction is empty. If 0<=q<=S, write
D=sum d_i, so B=mS-D-C. The positive summand is q-1-D-C, requiring
D+C<=q-2. Every individual row cap is then redundant because q<=S.
There are binom(l+2m-1,2m-1) choices of all d_i,c_i with total l. Summing
the whole slack yields


```text
C_m(S,U)=M_m(S,U)+3 binom(q+2m-1,2m+1),
m>=5, (m-2)S<=U<=(m-1)S.                       (F)
```

For U>=(m-1)S the whole count equals M. For m=4, U>=3S also makes the
correction empty by the same calculation; for m=3, U>=3S gives the original
collar directly from phi<=mS and (P). All grade-zero, q=0, q=1 and equality
walls are retained. Equation (F) is an all-grade finite identity. Its
correction has ordinary linear coefficient -3q/[2m(2m+1)] after q is
specialized homogeneously. Positive correction VALUES are not a coefficient
sign theorem; section 6 pays that adverse coefficient and every other term.

## 5. Complete coefficientwise augmentation, including the wall

Let b(q)=binom(q+2m-1,2m+1)=q(q-1)a_(2m-1)(q)/[2m(2m+1)]. At fixed S,
the derivative with respect to U in (F) is D_m(S)-3b'(q). Since a has
nonnegative coefficients and q*a'<=_coef(2m-1)a,


```text
b'(q)=[(2q-1)a+q(q-1)a']/[2m(2m+1)]
      <=_coef q*a_(2m-1)(q)/(2m).
```

For 0<=q<=S on a homogeneous ray, q*a(q)<=_coef S*a(S). Sorted positive
factor denominators give D_m(S)>=_coef(1+S)a_(2m-1)(S): after removing
one factor 1+S, the denominator list has m-1 ones and m twos, componentwise
at most 1,2,...,2m-1. Consequently


```text
D_m(S)-3b'(q)
  >=_coef a_(2m-1)(S)[1+(1-3/(2m))S].             (D)
```

Above q=0 the derivative is D_m(S) and obeys the same bound. At q=0 the
values agree exactly because b(0)=0. The derivatives need not agree: the
second-band derivative is D_m+3/[2m(2m+1)] there. Preserve this downward
jump on entering the upper band. Integrating each ordinary t coefficient
in the numerical parameter u across the continuous value wall proves (A).
No count at a nonintegral margin or change of lattice is needed: only the
polynomial coefficient expressions are extended between integral endpoints.

## 6. Entire paid bases and arbitrary-index reserve

For a polynomial f let |f|_c replace every coefficient by its absolute value.
In the L formula, replace each negative factor S-r by S+r. Its jth absolute
term is bounded by S*w_j times 2m positive factors, where


```text
w_j=binom(m,j)m!j!/(m+j+1)!.
```

For j>=2 the denominator list is dominated by that of D_m. For j=0,1 only
one extra slope-one factor remains; 1+S<=2(1+S/2) pays it. Also


```text
sum w_j=integral_0^1 [t(2-t)]^m dt
       =I_m=product_(r=1)^m 2r/(2r+1),
w_0+w_1=2/(m+2).
```

Hence |L_m|_c<=c_m*S*D_m with c_m=I_m+2/(m+2), decreasing in m.
The complete alternative R identity is


```text
R_m=2S*a_(2m)(2S)/(2m+1)
   -S(S-1)a_(2m-2)(S)[(m+1)S+2m]/[(2m-1)(2m+1)].
```

Remove only its explicitly nonpositive -S^2 product when taking an upper
bound. Sorted factors give a_(2m)(2S)<=2D_m and
a_(2m-2)(S)[1+(m+1)S/(2m)]<=D_m for m>=3. Thus


```text
R_m<=r_m*S*D_m,
r_m=4/(2m+1)+2m/[(2m-1)(2m+1)],
```

also decreasing. These comparisons retain both full moments and are not
sign assertions about isolated factors with negative coefficients.

In the second band put S=q+w and U=(m-2)S+w. The affine part M is at least
[1+w+(m/3-3c_m-r_m)S]D_m. The full correction is at least
-3q*a_(2m-1)(q)/[2m(2m+1)], hence at least
-3S*D_m/[2m(2m+1)]. For m=7, the exact remaining reserve is


```text
7/3-3c_7-r_7-3/(14*15)=719/2002>0,
c_7=3478/6435, r_7=22/65.
```

Monotonicity of c_m,r_m and the correction bound gives, for EVERY m>=7,


```text
C_m(S,U)>=_coef [1+w+(719/2002+(m-7)/3)S]D_m(S).
```

This is strict through degree 2m+1 for S>0. The uniform index quantifier
comes from these exact inequalities, not from a finite extension in m.

The four complete lower-wall polynomials are separately reconstructed for
m=3 at U=3S; m=4 at U=3S; m=5 at U=3S; and m=6 at U=4S. For m=3, the
full identity L_3=R_3=S(S+1)(S+2)(S+3)(2S+3)(13S^2+39S+32)/1260 gives
a strictly positive full reserve as in the completed U02 derivation. For
m=4,5,6, exact full coefficient arrays including degree zero through 2m+1
are proof bases. Their independent reconstruction, every zero slot, and
omission controls are mandatory. Root v1 algebra finds all coefficients
positive; m=5,6 also have full nonnegative two-variable cone arrays. No
adoption is made until those joins and the gate pass. Apply (A) from these
paid complete endpoints to finish every u>=h_m*s.

## 7. Verification, provenance and stopping

Independently check the full weak-row reflection identity, the reindexing of
every clipping partner, all moment formulas/bounds, the four finite bases,
the exact beta reserve, derivative sign and jump, and literal-original
determining/unused evidence. Deliberate deletion of reflection, factor three,
strict q-1 offset, either moment, any tail-prefix family, or the degree-loss
axis must be detected. The signed first correction is a required hostile
control. Full pre-collar C-M outside this domain remains potentially adverse;
source m4,s=u=1 is not contradicted.

Public balanced-signature or two-sided quotient claims remain unadopted source because
they lack the needed ordinary-coefficient identification. The new result is
a directly reconstructed complete LR identity and payment, with source
lineage preserved. It does not adopt the new Pro055 paw or capacity theorems,
Pro054's broader fixed/moving claims, or any public theorem wholesale.
Preserve these serious alternatives for exact independent reconstruction.
