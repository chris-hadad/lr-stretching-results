# Every zero-h cap wall and a positive whole-parent first jet

This proof retains the complete family m=k+1>=2, h=0, integer0<=g<=2k, p=2k-g. Positivity of all ordinary coefficients is not assumed. The g1 theorem is [Whole-bank ordinary positivity at unbounded rank](014-ALL-RANK-BANK-POSITIVITY.md); the endpoints have separate full formulas.

## Entire family and all-stretch contraction

The balanced partitions are
lambda=(8m-2,(6m-2i)_(i=1..m),4m,2m),
mu=(6m-2,(6m-2-2i)_(i=1..m-1),2m+g,2m),
nu=(6m-2-g,2m,2m).
Outer size5m^2+13m-2, ordinary rankm+3. For g>0 the entire source chart has saturated lattice Z^(2m-1), actual degree 2m-1 and true codegree max(2,ceil(m/g)). Necessity follows from strict internal y,z, u>Z and u<gt. At that claimed dilation, z2..z_(m-1)=1, y1..y_(m-1)=2, y_m=1,u=m-1 supplies a strict point. At m2, the strict bank bound u<y1<2t separately forces t>=2. At g0, z=u=0, dimensionm, lattice Z^m, codegree 1; no positive-gap degree is assigned there.

[Complete positive-gap two-bank contraction](013-COMPLETE-BANK-CONTRACTION.md)'s unsigned prefix N(A,B)=M(A,B)-M(A+1,B-1) remains complete. Its final weight is
(min(gt,A)-B+1)_+*(2mt-max(gt,A)+1).
The identical reindexing, square symmetry and conditional first moment now give
P_(m,g)(t)=sum_(B=0)^(gt) ((m+1-g)t+1+3B/2) S_B,
`S_B=[y^B](sum_(z=0)^(2t)(2t+1-z)y^z)^k.                  (1)`
This does NOT drop the individual z caps when g>2. The marked count before symmetrization is the complete
P_(m,g)(t;q)=sum_(A>=B>=0) q^B N(A,B) W_g(A,B).
Here B is the actual sum of internal label3 entries. Setting q=1 yields(1); arbitrary fixed q is not asserted to have polynomial dependence on t.

## Complete cap formula

Use
sum_(z=0)^(2t)(2t+1-z)y^z =[(2t+1)(1-y)-y+y^(2t+2)]/(1-y)^2.
For a high-power choices and j negative-y choices, let
r=k+a+j, U=(g-2a)t+k-a, X=2a(t+1)+j,
C_(a,j)=(-1)^j binom(k,a)binom(k-a,j)(2t+1)^(k-a-j).
Then the entire polynomial is
sum_(a,j) C_(a,j)*[((m+1-g)t+1+3X/2)binom(U,r)
                         +(3r/2)binom(U,r+1)].           (2)
Include every j0..k-a at a=0. For a>=1 include it iff g>2a; at g=2a every actual term is zero (the nonnegative constant upper index k-a is below the lower index). For g<2a omit it, rather than continuing a generalized binomial outside support. Every small positive t before a term's threshold also vanishes because its binomial upper index is nonnegative and smaller than the lower. This proves all endpoints and all stretches, not an eventual interpolation.

## Complete linear coefficient: positive tents

Put H_k=sum_(i=1)^k1/i and C_k=4^k/((2k+1)binom(2k,k)). The a0 terms have linear coefficient
3k+2+g*(1/2+H_k/2-3C_k/2).
For1<=a<=k-1 define the strictly positive rational
W_(k,a)=binom(k,a) sum_(j=0)^(k-a) binom(k-a,j)
  *(k-a)!(2a+j-1)!/(k+a+j)! *[1+3(2a+j)/(2(k+a+j+1))].
Direct differentiation of every binomial in(2), including the second term and its support condition, gives
c1(g)=3k+2+g*S_k -sum_(a=1)^(k-1) W_(k,a)(g-2a)_+,
S_k=1/2+H_k/2-3C_k/2.                                  (3)
For a0, the elementary identities sum_(j=1)^k [k!^2/((k-j)!(k+j)!)]/j=H_k/2 and sum_(j=1)^k k!^2/((k-j)!(k+j+1)!)=C_k-1/(k+1) provide the stated simplification. Alternatively (3) with the unsimplified finite factorial slope follows immediately from (2); the positive-tent proof below does not depend on either harmonic simplification.

At g0 the full polynomial is(2t+1)^k((k+2)t+1). At g=2k all prefix B are included, and the exact triangular-distribution mean B=2kt/3 gives
P_(m,2k)(t)=(t+1)^k(2t+1)^(k+1).
Both have c1=3k+2. Thus (3) at 2k proves 2k*S_k=sum_a W_(k,a)(2k-2a). Substitution yields the fully positive formula
c1(g)=3k+2+sum_(a=1)^(k-1) W_(k,a)
 *[g(1-a/k)-(g-2a)_+].                                  (4)
Each bracket is g(1-a/k) for0<=g<=2a and a(2-g/k) for2a<=g<=2k. It is nonnegative throughout the legal interval. Therefore the entire LR coefficient satisfies
c1(P_(m,g))>=3m-1,
with equality at both endpoints; for k>=2 it is strict at 0<g<2k. For k1 the sum is empty and c1=5 throughout. This is a uniform all-m theorem, not a finite table or a sign assertion for individual assignments.

In particular g1 has
c1(P_m)=3k+5/2+H_k/2-(3/2)C_k.
The beta-integral interpretation C_k=int_0^1(1-x^2)^k dx shows0<C_k<1 for k>=1 and supplies an immediate weaker positive bound. [Whole-bank ordinary positivity at unbounded rank](014-ALL-RANK-BANK-POSITIVITY.md) establishes all higher coefficients on g1 independently.

## Scope and failure of cap-free extrapolation

The cap-free g1 expression cannot be extrapolated to arbitrary g: as soon as g>=3, the y^(2t+2) term contributes at actual stretches. Omitting it produces a different polynomial, even when several early counts agree. The full binomial terms at a>=1 have strictly NEGATIVE ordinary linear contribution -W_(k,a)(g-2a); this is auxiliary cap-correction scope, not a negative entire LR observation. All such observations are retained in the exact coefficient data.

The positive tents control the whole first jet only. Higher ordinary coefficients for arbitrary g>=2 remain a distinct question except the explicit endpoint g2k, any finite fully checked members, or a later genuine theorem. The changed h>0 region and global synchronization of the separate factors in the synchronized product construction remain outside this proof.

### Elementary normalization details

For the first factorial sum use binom(k,j)B(j,k+1)=k!^2/[j(k-j)!(k+j)!]. Summing under the finite beta integral gives int_0^1[(1-x^2)^k-(1-x)^k]/x dx=H_k-H_k/2. For the second sum, multiply by(2k+1)!/(k!)^2 and sum binom(2k+1,k-j), j1..k. The lower half-binomial sum is4^k-binom(2k+1,k), yielding C_k-1/(k+1). Thus both identities hold for every k, not merely at tested numerical ranks.
