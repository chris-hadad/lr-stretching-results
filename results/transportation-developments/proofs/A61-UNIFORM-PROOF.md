# A61 root derivation: a uniform linear reserve and all-deficit three-cap originals

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

27 September 2026. Sections 1–4 originated as root work from the accepted A58 character bridge
and A60 formula (10), before semantic reading of the new provider proofs.
Section 5 later develops the same root cap-balancing idea using only the
complete root chamber certificate. No active provider theorem is a premise.
 All provider working material remains separately SOURCE-qualified.

## 1. Complete original and parameter domain

For a positive integer caps k_i with a>=3, put K=sum k_i. Let B be an integer
with K/2<=B<=K and r=K-B. In the two separated pair original, take row widths
(u1,v1,k1,...,ka,u2,v2), all four paired widths at least H=2B, first and last
adjacent overlaps B and all other overlaps zero. Construct lambda,mu upwards
as in A58 A58-FIRST-WALL-PROOF.md §1, and nu=(sum widths-4B,2B,2B), lambda OUTER.
The accepted complete character proof in its §2 gives the ENTIRE count


```text
P(t)=sum (Bt-U+1)(Bt-V+1),
u_i,v_i>=0, u_i+v_i<=k_i t, U=sum u_i<=Bt, V=sum v_i<=Bt.
```

No row, paired determinant or once-shifted Weyl partner is discarded. The
full slack-coordinate lattice is saturated Z^(2a+2); positive parameters give
strict interior and actual dimension 2a+2. The original maximum trimmed rank
is a+4. Permuting caps, changing paired widths within their floors, scaling
all parameters by s>=1, and physically inserting isolated zero-width rows
preserve the accepted exact count rules. Zero rows do not lower physical rank.

## 2. All-deficit first coefficient

For a subset J, set q=|J| and M_J=sum_(i in J) k_i, and let x_+=max(x,0).
The COMPLETE ordinary linear coefficient is


```text
c1(P)=11K/4-2r-F_a(k;r),
F_a(k;r)=sum_(J proper subset) w_(a,q) (r-M_J)_+,
w_(a,q)=(a-q-1)!(q+1)!/(a+1)!.                         (1)
```

Every subset correction is present, including intersections first visible
only at later integer grades. This is not the linear coefficient of a tail.

Derivation. In A60 (10), put c=2a-2q-1, d=2a-q+h+1 and s=r-M_J>0.
The derivative at zero of binom(st+c,d) is


```text
s (-1)^(q+h+1) c!(q+h+1)!/d!
  =s (-1)^(q+h+1) integral_0^1 x^c(1-x)^(q+h+1) dx.
```

The elementary factor's constant is 2^(q-h) binom(q,h), and A_r(0)=2;
its derivatives multiply a binomial with zero constant and do not enter c1.
Combining the next binomial degree replaces 2 by 2-(1-x)=1+x inside the
integral. Summing in h yields (2-(1-x))^q=(1+x)^q. Consequently


```text
(-1)^q [t]T_J
   =-s integral_0^1 x^(2a-2q-1)(1-x^2)^(q+1) dx
   =-s (a-q-1)!(q+1)!/[2(a+1)!].
```

The factor two in (10), together with [t]N=3K/2 and L_r=5K/4-2r,
proves (1). Because M_J<r<=K/2, J is proper and c>=1. At M_J=r the
term is identically zero, so the hinge convention includes every wall.

## 3. Sharp reserve by convexity, and a paid linear cap operation

For fixed K,r with 0<=r<=K, F_a is symmetric and convex in the nonnegative
cap vector: it is a positive sum of hinges of affine functions. On sum k_i=K,
write k as the convex combination sum (k_i/K) K e_i. All concentrated vertices
have the same value. Only subsets avoiding the nonzero cap contribute, so


```text
F_a(K e_i;r)
  =r sum_(q=0)^(a-1) binom(a-1,q) w_(a,q)
  =r sum_(q=0)^(a-1) (q+1)/[a(a+1)]=r/2.
```

Thus the original uniform reserve is


```text
c1(P)>=11K/4-5r/2=(K+10B)/4>=3K/2>0.                 (2)
```

For positive caps, a>=2 and 0<r<K, the first inequality is strict: each
nonempty proper subset has 0<M_J<K, and
(r-M_J)_+<r(1-M_J/K). The bound is sharp on the nonnegative-cap closure;
at (K,0,...,0), B=K/2, the whole original count reduces to
binom(Bt+2,2)^2 and c1=3K/2. Zero cap rows are eliminated only for counting,
never silently for the physical original's rank.

For fixed positive integer a,K,r the exact minimum of c1 occurs at
(k_1,...,k_a)=(K-a+1,1,...,1), because the domain k_i>=1 is itself a simplex
and the same convex argument applies. Formula (1) evaluated there is the
sharp finite sum for this fixed-size integer problem. Cap balancing cannot
decrease c1: symmetric convex F is Schur-convex. Splitting a cap into two
nonnegative caps cannot decrease c1 either: append a zero cap (same count),
then replace (x+y,0) by (x,y), a convex combination of the two permutations.
The count formula and (1) extend to appended zero caps by the same generating
identity. This pays the LINEAR gain only. It asserts no whole-polynomial
positive gain or complete original-generation theorem.

## 4. A complete five-chamber reduction for three positive caps

Now a=3. Sort k1<=k2<=k3, without changing the full count. The following
rows give (k1,k2,k3,r) as nonnegative linear forms in four coordinates
(z0,z1,z2,z3). Each region is its complete closed cone; shared walls agree.

| Region | k1 | k2 | k3 | r |
| --- | --- | --- | --- | --- |
| r<=k1 | z0+z1 | z0+z1+z2 | z0+z1+z2+z3 | z0 |
| k1<=r<=k2 | z0 | z0+z1+z2 | z0+z1+z2+z3 | z0+z1 |
| k2<=r<=k3, k1+k2>=r | z0+z1 | z0+z1+z2 | z0+2z1+z2+z3 | z0+2z1+z2 |
| k1+k2<=r, 2r<=K | z0 | z0+z1 | 2z0+z1+2z2+z3 | 2z0+z1+z2 |
| k3<=r, 2r<=K | z0+z2+2z3 | z0+z1+z2+2z3 | z0+z1+2z2+2z3 | z0+z1+2z2+3z3 |

The inverse coordinates are, respectively:

1. (r,k1-r,k2-k1,k3-k2).
2. (k1,r-k1,k2-r,k3-k2).
3. (k1+k2-r,r-k2,k2-k1,k3-r).
4. (k1,k2-k1,r-k1-k2,K-2r).
5. (K-2r,k2-k1,k3-k2,r-k3).

All are nonnegative integers for the relevant integer parameters. These five
regions exhaust the ordered high-budget cone. In the last region each pair
sum is >=r because K>=2r and the remaining cap<=r. In region four only
the pair {1,2} can violate. Thus the complete surviving subsets are
(empty); (empty,{1}); (empty,{1},{2}); (empty,{1},{2},{1,2}); and
(empty,{1},{2},{3}), respectively. Equalities give zero corrections.

Expand A60 (10) in these four variables after replacing k_i t,r t by their
linear forms. Total parameter degree equals ordinary t degree. Every
coefficient in all five exact rational polynomials is nonnegative; the
complete sparse lists and deterministic expansion are ../certificates/a60-a61/chambers-v1.json and
../certificates/a60-a61/a61_chambers.py, with no numerical fitting. Their maximum degree is eight.
An independently authored complete cap/slack interpolation checks all
coefficients; exact populations and unused points are in the verification record.

Strictness through degree eight follows from pure powers in the certificate.
In regions 1 and 2 the positive coordinate z0 suffices (for r=0 in region 1,
z1>0 suffices); in region 3 one of z0,z1 is positive; in region 4 z0>0;
in region 5 one of z0,z2,z3 is positive. Each relevant pure power z_i^j,
1<=j<=8, has a strictly positive coefficient. Constant one is exact.
Therefore every three-positive-cap complete original with K/2<=B<=K is
strictly positive through its actual degree eight, uniformly in the deficit.
For B>=K, both bounds are redundant for the cap domain. The unrestricted
formula N[1+(2B-3K/4)t+((4(3B-K)^2-sum k_i^2)/36)t^2] has strictly
positive coefficients, extending this three-cap theorem to all B>=K/2.
This is the full stated original FAMILY at rank seven, not whole rank seven.

## 5. A whole-polynomial balancing operation for three caps

Keep K,B (equivalently K,r) fixed. On each of the five closed chambers, take
all three directions partial_(k_i)-partial_(k_j), i<j. Since the caps are
ordered, these infinitesimally transfer width from a larger cap to a smaller
one. The inverse coordinate maps in Section 4 turn each direction into a
constant integral combination of partial_(z_l). Apply it to every monomial
of the COMPLETE chamber polynomial. The exact certificate
../certificates/a60-a61/balancing-probe-v1.json lists all fifteen resulting polynomials. Every
ordinary coefficient in the nonnegative z coordinates is nonnegative.
These derivatives are independently checked from the count-reconstructed
polynomials, not just from the original symbolic producer.

Each parameter-homogeneous degree j piece is precisely [t^j]P. Therefore
its directional derivative is nonnegative throughout the chamber. Complete
formulas agree on common faces (and count symmetry agrees at order walls).
A finite Robin Hood transfer is a finite succession of such chamber pieces,
possibly after permuting caps when an order wall is crossed. Integration
of the coefficient functions proves that balancing cannot decrease ANY
ordinary coefficient for these three-cap originals. This argument uses
piecewise polynomial extensions of coefficients to real boundary parameters;
only integer endpoints are asserted to be LR originals.

The nonnegative-cap closure is valid in all five polynomial identities.
Starting at (K,0,0) and balancing to any prescribed cap triple therefore gives


```text
P_(k1,k2,k3)(t) >=_c P_(K,0,0)(t)
   = binom(Bt+2,2)^2-binom((2B-K)t+3,4), K/2<=B<=K.  (3)
```

To verify the paid starting original directly, after the zero cap rows
contribute h_0=1, set A=Bt-u, C=Bt-v in its one remaining cap triangle.
The unconstrained weighted square has count binom(Bt+2,2)^2. Its removed
corner is A+C<=(2B-K)t-1, with weight (A+1)(C+1). Since 0<=2B-K<=B,
the square upper bounds are redundant there; the complete corner is
binom((2B-K)t+3,4). This proves (3) with all endpoints retained.
Writing L=2B-K, its four positive coefficients are


```text
3B-L/4,
13B^2/4-11L^2/24,
3B^3/2-L^3/4,
B^4/4-L^4/24.
```

They are strictly positive for B>0 and 0<=L<=B. The chamber certificates
add strict degrees five through eight when all three caps are positive.
For integer caps bounded below by one, the whole coefficientwise minimum
at fixed K,B is attained by (K-2,1,1), by the same balancing principle.
The operation changes the literal original partitions via their retained
row widths and keeps K,B fixed; it does not assert a polytope-face embedding.
Every endpoint is a complete legal original with its full paired widths.

This is a paid whole-polynomial original operation on THREE cap slots.
Section 3 proves its all-cap analogue only for c1. Eight complete cap-split
gains on named higher-dimensional controls are positive, but these finite
vectors do not prove the all-cap whole-gain conjecture. That is the next
structural bridge, distinct from rank-by-rank chamber enumeration.

## 6. Mathematical boundary

Whole coefficients for a>=4 and arbitrary deficits remain open. No linear
reserve alone pays them. The proposed complete cap-splitting gain and the
free-U grouped absorber are separate competitors. B<K/2 requires joint-budget
tail corrections and is outside these formulas. No unrestricted KTT conclusion follows.
