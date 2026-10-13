# Pro049 U12 — whole pre-stable compensation before residue separation

This is a curated copy of the completed originating Pro049 U12 research proof,
SHA-256 `8bf014ee64307fad5c527f71e42458c9cb1afe2e1975aa96adf093540735bc96`.
The A70 independent reconstruction accepts the main rank-five operation at the
scope of [the adoption proof](A70-PRO049-U12-ADOPTION.md). Broader finite provider
censuses, separate shadow/arrival counts and other unit claims remain SOURCE.
Only private lifecycle/operator text was removed; all mathematical sections,
formulas, complete rays/facets/cells, shifts and coefficient tables are retained.

**Originating status:** the theorem is proved by a complete integer original-cone decomposition and exact polynomial identities. The finite certificates are fully specified below and in DATA, with independent implementations. This is not campaign adoption, human review, proof-assistant certification or a priority assertion. This is a protected rank-five original family; its positive endpoints are not new campaign rank coverage. The new conclusion is uniform **coefficientwise positivity of the entire segment operation in every pre-stable and stable chamber**, including the U11 period-two projection and unbounded-birth examples.

## 1. Complete objects and theorem

For integers s,u>=0 use the literal original


```text
lambda=(2s+4u,2s+3u,2s+2u,2s,s),
mu=(2s+2u,2s+u,2s,s,0),
nu=(s+3u,s+2u,u).
```

Denote its stretching polynomial by P_(s,u)(t), and its grade-one count by N(s,u). Equivalently this is b_s+u sigma, with b_s=((2s,2s,2s,2s,s);(2s,2s,2s,s,0);(s,s,0)) and sigma=((4,3,2,0,0);(2,1,0,0,0);(3,2,1)). All five physical rows remain, including the first three empty rows at u=0 and the last two empty rows at s=0. Partition order, containment and trace hold for every stated parameter; the common area is 2s+6u.

### Theorem U12-COMPENSATION

The complete all-grade count is given by the four parameter polynomials in Sections 4–5. For every s>0 and 0<=u<v,

    P_(s,v)(t)-P_(s,u)(t)

has zero constant coefficient and strictly positive ordinary coefficients in every degree 1,...,5. No independent ordinary-polynomial assumption is made for either the present-tail or arriving-tail summand. Every complete original P_(s,u), s,u>0, is strict through actual degree five. Boundary formulas are P_(s,0)=1 and P_(0,u)=1+ut; at s=u=0 it is a point. These are complete homogeneous-original and complete operation statements, not signs of a selected residue or affine subtotal.

Integer parameters specify the originals. The exact polynomial sign certificates also apply to nonnegative real chamber parameters; rational parameters represent homogeneous originals after common denominator clearing. No integer lattice is evaluated at an unacknowledged fractional grade.

## 2. Entire physical cone and actual lattice

Write S=st,U=ut. Let the two tail rows be (a,b,S-a-b) and (d,e,S-d-e). With z the first entry in row two minus U, the complete original array is

    (2U,0,0),
    (z+U,U-z,0),
    (S-a-d-z,S-b-e+z+U,U-2S+a+b+d+e),
    (a,b,S-a-b),
    (d,e,S-d-e).

Every row and content equation is solved, and the inverse is integer coordinate projection. The leading zeroes follow from the LR ballot rule. Nonnegativity, all physical adjacent columns and all reading-prefix ballot comparisons are imposed by


```text
x_(i,j)>=0,
mu_(i-1)-mu_i+sum_(k<j)x_(i-1,k)-sum_(k<=j)x_(i,k)>=0,
sum_(k<i)x_(k,j)-sum_(k<=i)x_(k,j+1)>=0.
```

Together with S,U>=0 these are exactly 39 labeled occurrences, 28 distinct nonzero primitive linear forms in (S,U,z,a,b,d,e). DATA/CONE-INPUT.json gives every coefficient and label, including forced zero occurrences and repeated physical rows. These criteria are necessary and sufficient for a sorted LR tableau: the worst ballot prefix is after the larger-letter block, and adjacent column comparisons imply strictness along an entire skew column. Thus the cone describes the **whole original**, not the shadow used in U11.

The integer lattice of the seven-parameter cone is Z^7. At s,u>0 put epsilon=min(s,u)/4, tail rows (s-2epsilon,epsilon,epsilon) and (epsilon,s-2epsilon,epsilon), and z=epsilon-u/2. Every nonconstant physical constraint is strict. The independent auditor substitutes s=4epsilon+p,u=4epsilon+q with p,q>=0: each nonzero slack has nonnegative p,q coefficients and a strictly positive epsilon coefficient. Fixed positive s,u therefore have actual dimension five and saturated lattice Z^5. At u=0 the original has its unique tableau; at s=0 only the primitive z interval remains. No degree is borrowed across these boundaries.

## 3. Complete unimodular decomposition, including all boundaries

Intersect the seven-dimensional cone with S+U=1. This is bounded: 0<=S,U<=1, the four tail coordinates are in [0,S], and -U<=z<=0. Every nonzero ray has S+U>0. Exhausting all binom(28,6)=376740 six-row subsets gives 282835 rank-six subsets and 49464 feasible bases, resolving to exactly the 15 primitive rays in Appendix A. This is not a cardinality argument on an incomplete subset.

A separately authored standard-library double-description implementation starts from the signed nonnegative coordinate orthant (S,U,-z,a,b,d,e)>=0 and intersects all remaining inequalities. At every step it forms every positive/negative ray pair and retains exactly the rays whose active normals have rank six. Its complete 21-stage record independently returns the same 15 rays. All numerical arithmetic is exact; no floating feasibility or triangulation is used.

The complete cone has 13 facets. Their zero-ray sets are the sets of rank six arising from the full physical row list. A pulling triangulation of the S+U=1 section selects the least-indexed vertex of each face, cones to all facets not containing it, and recurses. The face facets are all rank-one-lower intersections with the complete 13 global facets. This produces exactly 16 maximal cones, listed in Appendix A. The recursive construction proves their coverage and face-to-face intersection, not merely a volume check. Every seven-by-seven primitive ray matrix has determinant +1 or -1.

Choose the exact vector omega recorded in DATA/CONE-SERIES.json, a strictly positive sum of all rays, such that every coordinate of M^(-1)omega is nonzero for every simplex matrix M. The certificate checks both facts. Assign a lattice point to the cone into whose relative interior it moves under a sufficiently small positive multiple of omega. This partitions the **closed** entire cone, including external boundaries. A simplex coordinate is open at zero exactly where the corresponding coordinate of M^(-1)omega is negative. Since M is unimodular, its half-open fundamental parallelepiped has exactly one lattice point: the sum of the rays at its open coordinates. Consequently the whole bivariate generating function is exactly the sum of these 16 monomial-over-ray-denominator terms. No residue point, boundary ownership or zero-grade contribution is omitted.

Let G(x,y)=sum_(S,U>=0)N(S,U)x^S y^U. Clearing complete denominators gives the following nine-term identity. The independent rational polynomial auditor verifies every coefficient after multiplying by the common denominator; it does not compare a finite initial series.


```text
G = (1+4x+x^2)/((1-x)^5(1-y)^2)
    -(9x+12x^2+2x^3)/((1-x)^6(1-y))
    +3x^2/((1-x)^4(1-xy)^3)
    +(3x^2-2x^3)/((1-x)^5(1-xy)^2)
    +(4x^2-8x^3-4x^4)/((1-x)^6(1-xy))
    -x^3/((1-x)^4(1-x^2y)^3)
    -x^3/((1-x)^5(1-x^2y)^2)
    -x^3/((1-x)^6(1-x^2y))
    +(x+15x^2+15x^3+x^4+y(6x^2+20x^3+6x^4))
         /((1-x)^6(1-xy^2)).                         (G)
```

The individual signed partial fractions need not count LR originals or have positive ordinary coefficients. Only their full sum is used.

## 4. Exact extraction and the cancellation of the apparent parity

Define ordinary polynomials


```text
E(S)=(S+1)^2(S+2)^2/4,
A(S)=S(S+1)(S+2)(23S^2+81S+76)/120,
C(k,U)=k(k-1)(k+1)(30U^2+5Uk+140U-8k^2+45k+142)/120,
D(k,U)=k(k-1)(k-2)(10U^2+5Uk+35U+k^2+8k+27)/120.
```

Let an indicated term be zero when its accompanying condition is false. Then for **every** pair of nonnegative integers S,U,


```text
N(S,U)=(U+1)E(S)-A(S)
       + 1_(U<=2S) binom(2S-U+3,5)
       + 1_(U<=S) C(S-U,U)
       - 1_(2U<=S) D(S-2U,U).                       (N)
```

All binomial arguments in an active term are nonnegative integers; binom(n,k)=0 for 0<=n<k. This is a direct coefficient extraction from (G), not interpolation on parameter nodes or an assumed conic chamber theorem. The C term is the complete sum of the three (1-xy) denominators, and D is the complete sum of the three (1-x^2y) denominators. Their factors k(k-1)(k+1) and k(k-1)(k-2) retain their exact early zero bands.

For clarity, the last term in (G) appears to separate U by parity. If U=2v, put n=S-v; its coefficient is


```text
binom(n+4,5)+15binom(n+3,5)+15binom(n+2,5)+binom(n+1,5)
    =binom(2n+3,5).
```

If U=2v+1, put n=S-v; its coefficient is


```text
6binom(n+3,5)+20binom(n+2,5)+6binom(n+1,5)
    =binom(2n+2,5).
```

Both full identities are verified as polynomials. They yield the SAME expression binom(2S-U+3,5), with its actual support and zero initial band. When the x coefficient is outside its support it is zero, as in (N). Thus the parity is eliminated **before** an ordinary coefficient sign is asserted. No period-one property is assigned to U11's shadow or arriving pieces.

The four closed chambers in (N) are 0<=2U<=S; S<=2U with U<=S; S<=U<=2S; and 2S<=U. The formulas agree on every shared wall, including all zero parameter cases. In the first chamber the complete expression simplifies to


```text
N(S,U)=(U+1)(U+2)(U+3)(7U^2+13U+10)/60.              (LOW)
```

In the last it is (U+1)E(S)-A(S). Both intermediate chamber polynomials, and every coefficient in all four, are given in Appendix B. There is no omitted transition band near an affine shift.

## 5. Complete coefficientwise compensation and operation signs

Substitute S=st,U=ut in (N) within the appropriate fixed parameter chamber. This gives the ENTIRE homogeneous polynomial P_(s,u)(t)=sum_(k=0)^5 c_k(s,u)t^k. The constant is always one for this family. Appendix B records all 24 c_k, including zeros at special parameters, and Appendix C records every sign and derivative polynomial.

To prove all signs uniformly, use these exact nonnegative cone coordinates (a,b):


```text
chamber 0: s=2a+b, u=a;
chamber 1: s=2a+b, u=a+b;
chamber 2: s=a+b, u=2a+b;
chamber 3: s=a, u=2a+b.
```

For each chamber and k=0,...,5, expand c_k and its derivative with respect to u **at fixed s**, then substitute these coordinates. The complete certificate has 48 polynomial slots and 99 nonzero rational coefficients. Every nonzero coefficient is positive; every omitted monomial is zero by the displayed full degree limit (k, or k-1 for the derivative). All constant derivative slots are explicitly zero. An independent standard-library polynomial ring reconstructs (N), all four c_k, all 48 substitutions, and every rational entry. It also checks all three wall identities and both degree-drop boundaries. This is an unbounded exact polynomial certificate, not a positive grid.

For s,u>0, every c_k, k=1,...,5, is strictly positive: in the first chamber u=a>0; in each middle chamber the endpoint pure powers of a and b have positive coefficients; in the final chamber s=a>0. The same statements give a strictly positive derivative for every k>=1 wherever s,u>0. The c_k are continuous across all three parameter walls. Integrating these nonnegative, piecewise polynomial derivatives at fixed s>0 therefore proves


```text
c_k(s,v)>c_k(s,u),  0<=u<v, 1<=k<=5.
```

Even when u=0, the interval (0,v) contains a positive-length set of strict derivatives. The constant difference is zero. This proves Theorem U12-COMPENSATION over the full parameter domain. At s=0 only the linear coefficient changes; at u=0 the original is a point. No separate clipped-sector coefficient has been required to be positive.

The stable signed intercept, for comparison, is


```text
J_s(t)=1+(26s/15)t-(37s^3/24)t^3-s^4 t^4-(23s^5/120)t^5.
```

Its quadratic coefficient is zero and it is not a count at u=0. The full count and the full operation remain positive because the entire quotient and pre-stable correction are kept. This observation is subordinate to the main complete-operation theorem; it is not a new negative-original candidate.

## 6. The U11 period obstruction is paid, not erased

For s=u=1, U11's full feasible-tail shadow is


```text
F(t)=3t^4/16+13t^3/12+19t^2/8+29t/12+31/32+(-1)^t/32.
```

Its nonpolynomiality and saturated Z^4 projection remain unchanged. The present all-parameter theorem now derives P_(1,1) and P_(1,2) without fitting. Their complete difference is


```text
21t/20+73t^2/24+77t^3/24+35t^4/24+29t^5/120.
```

The exact original arrival identity gives old contribution tF(t) and the ENTIRE arriving contribution


```text
13t^5/240+3t^4/8+5t^3/6+5t^2/8+13t/160-(-1)^t t/32.
```

The two parity terms cancel. This agrees with the independent full-tail joins at every grade 0,...,13. More importantly, (G)–(N) prove complete compensation for **all** s,u, including the three pre-stable regimes, not just this one displayed parity pair. The U11 tail with L=H=0,R=s still arrives with s+1 integer points. It is never replaced by a unit birth. All ninety additional layer records retain the actual starting multiplicities and both endpoint ties.

This is a proof that the identified two obstructions can be overcome in one complete original family. It is NOT a theorem for arbitrary primitive-boundary originals or for arbitrary three-row transportation margins.

## 7. Finite verification and exact limits

The frozen main count domain has 570 request records at 313 distinct literal original nodes. It includes the full rectangle S=0,...,10,U=0,...,24; twelve whole-polynomial seeds; every endpoint needed for ninety full arrival joins; and fourteen U11 shadow/arrival grades. Every literal partition and physical zero row is retained.

The independent C++ engine starts from the bare partitions, enumerates complete sorted row contents, enforces every original ballot prefix and physical column inequality, and forces the final content. It imports no cone or endpoint implementation. It visits 24,801,460 recursive nodes across the distinct inputs. Exact signed-64-bit counts are justified by the bound (U+1)(S+1)^4 on the injective five-coordinate tableau chart; the frozen maximum is 11,712,800. There are no floating counts, modular-only signs or overflow-dependent results. Seven independent cell-by-cell tableau counts additionally agree.

Twelve whole original vectors have actual degrees zero, one or five as proved above. All 87 determining/unused value occurrences are retained, including 24 genuinely unused positive grades. Independent Newton reconstruction matches every coefficient of the direct all-parameter formula. These protected-rank vectors are mechanism checks, not added campaign positivity coverage.

The complete layer audit retains 37,688 prospective tails and evaluates all 1,469,832 physical tail-constraint occurrences. Every ninety-layer old/new join agrees with the bare-original endpoints, and every U11 parity join through grade thirteen agrees. The complete tail tables include zero fibers and nonunit births; population overlaps are not added as new-original coverage.

Thirteen actual isolated corrupted-certificate executions were rejected: a missing cone, nonprimitive ray, wrong open facet, missing physical inequality, false chamber polynomial, omitted chamber, false derivative, missing unused grade, false degree, lost physical zero row, erased shadow parity, unpaid arrival and false lattice index. Exact original/mutated identities and lossless patches remain. These hostile children recheck the full structural/algebra or recorded-vector certificate, not the complete C++ count domain on each run.

## 8. Scope, sources and final boundary

The main U12 result is a **complete coefficientwise-positive operation** across all four chambers of the fixed rank-five two-parameter family. Whole endpoint signs were already protected by the campaign's rank-at-most-six terminal; they are not new rank coverage. The operation signs do not follow from positive endpoints alone. The all-parameter proof is the exact cone and algebra certificate, not the finite count rectangle.

The classical LR tableau rule and elementary lattice-cone/triangulation arguments supply the count model. U11's full proof supplies the named original family and its previous period/birth obstruction; U09/U10 supply broader context only. Classical homogeneous LR polynomiality was checked from Thawinrak, arXiv:2211.06810v2, Theorem 1.1 and Section 3, but (N) directly proves the present all-grade formula and never transfers polynomiality to a projection. Postnikov's specified positive-simplex theorem remains the separately scoped prior premise for U09–U11, not a new U12 theorem or a justification for arbitrary signed sums.

There is no unrestricted KTT proof, no whole-rank extension and no suspected negative ordinary coefficient of a complete homogeneous original. The final synthesis retains the universal stabilized three-letter results and their exact unpaid primitive-wall/initial-band and longer-content obligations.

## Appendix A — full primitive rays and unimodular cones

Ray IDs below are zero-based, in (S,U,z,a,b,d,e) order.


```text
r0=(0, 1, -1, 0, 0, 0, 0)
r1=(0, 1, 0, 0, 0, 0, 0)
r2=(1, 0, 0, 1, 0, 0, 1)
r3=(1, 1, -1, 0, 1, 1, 0)
r4=(1, 1, 0, 0, 0, 0, 1)
r5=(1, 1, 0, 0, 0, 1, 0)
r6=(1, 1, 0, 0, 1, 0, 0)
r7=(1, 1, 0, 0, 1, 0, 1)
r8=(1, 1, 0, 0, 1, 1, 0)
r9=(1, 1, 0, 1, 0, 0, 0)
r10=(1, 2, -1, 1, 0, 1, 0)
r11=(1, 2, 0, 0, 0, 0, 0)
r12=(2, 1, 0, 0, 1, 1, 1)
r13=(2, 1, 0, 0, 2, 1, 0)
r14=(2, 1, 0, 0, 2, 1, 1)
```

All sixteen maximal cones follow. `open` uses coordinate positions within the listed ray matrix, not global ray IDs. The single numerator is the first two coordinates of the full listed lattice shift.


```text
0: rays=[0, 1, 2, 4, 5, 6, 11]; open=[6]; shift=[1, 2, 0, 0, 0, 0, 0]
1: rays=[0, 1, 2, 4, 5, 6, 13]; open=[4, 5]; shift=[2, 2, 0, 0, 1, 1, 0]
2: rays=[0, 1, 2, 4, 5, 12, 13]; open=[3, 4]; shift=[2, 2, 0, 0, 0, 1, 1]
3: rays=[0, 1, 2, 5, 6, 9, 11]; open=[5, 6]; shift=[2, 3, 0, 1, 0, 0, 0]
4: rays=[0, 1, 2, 5, 6, 9, 13]; open=[5]; shift=[1, 1, 0, 1, 0, 0, 0]
5: rays=[0, 1, 2, 4, 6, 7, 14]; open=[5]; shift=[1, 1, 0, 0, 1, 0, 1]
6: rays=[0, 1, 2, 4, 6, 13, 14]; open=[4]; shift=[1, 1, 0, 0, 1, 0, 0]
7: rays=[0, 1, 2, 4, 12, 13, 14]; open=[3]; shift=[1, 1, 0, 0, 0, 0, 1]
8: rays=[0, 1, 2, 5, 8, 9, 13]; open=[4, 5]; shift=[2, 2, 0, 1, 1, 1, 0]
9: rays=[0, 1, 2, 5, 8, 13, 14]; open=[4]; shift=[1, 1, 0, 0, 1, 1, 0]
10: rays=[0, 1, 2, 5, 12, 13, 14]; open=[]; shift=[0, 0, 0, 0, 0, 0, 0]
11: rays=[0, 1, 2, 5, 8, 9, 10]; open=[1, 6]; shift=[1, 3, -1, 1, 0, 1, 0]
12: rays=[0, 2, 3, 5, 8, 9, 10]; open=[6]; shift=[1, 2, -1, 1, 0, 1, 0]
13: rays=[0, 2, 3, 5, 8, 9, 13]; open=[2, 5]; shift=[2, 2, -1, 1, 1, 1, 0]
14: rays=[0, 2, 3, 5, 8, 13, 14]; open=[2, 4]; shift=[2, 2, -1, 0, 2, 2, 0]
15: rays=[0, 2, 3, 5, 12, 13, 14]; open=[2]; shift=[1, 1, -1, 0, 1, 1, 0]
```

The exact generic direction is


```text
omega=[61436, 35835, -1033, 1540, 53704, 29992, 20628]
```

The complete facet zero-ray sets are

    [0, 1, 2, 3, 4, 5, 7, 8, 10, 12, 14]
    [0, 1, 2, 3, 6, 7, 8, 9, 10, 13, 14]
    [0, 1, 2, 4, 5, 9, 10, 11]
    [0, 1, 2, 4, 6, 7, 9, 11]
    [0, 1, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14]
    [0, 1, 3, 5, 6, 8, 9, 10, 11, 13]
    [0, 2, 3, 4, 5, 6, 9, 11, 12, 13]
    [0, 2, 3, 4, 6, 7, 12, 13, 14]
    [0, 2, 3, 5, 9, 10]
    [1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
    [1, 2, 5, 8, 9, 10]
    [2, 3, 5, 8, 9, 10, 13]
    [2, 3, 5, 8, 12, 13, 14]

## Appendix B — every ordinary coefficient


### Chamber 0: 0<=2u<=s


```text
c0(s,u)=1
c1(s,u)=47*u/15
c2(s,u)=49*u**2/12
c3(s,u)=11*u**3/4
c4(s,u)=11*u**4/12
c5(s,u)=7*u**5/60
```

### Chamber 1: s<=2u and u<=s


```text
c0(s,u)=1
c1(s,u)=(27*s + 134*u)/60
c2(s,u)=-(13*s**2 - 66*s*u - 18*u**2)/24
c3(s,u)=(s**3 - 25*s**2*u + 92*s*u**2 - 26*u**3)/24
c4(s,u)=(s**4 - 4*s**3*u - 6*s**2*u**2 + 40*s*u**3 - 18*u**4)/24
c5(s,u)=(s**5 - 5*s**4*u + 10*s**3*u**2 - 20*s**2*u**3 + 40*s*u**4 - 18*u**5)/120
```

### Chamber 2: s<=u<=2s


```text
c0(s,u)=1
c1(s,u)=7*(14*s + 9*u)/60
c2(s,u)=-(4*s**2 - 76*s*u + u**2)/24
c3(s,u)=-(29*s**3 - 66*s**2*u - 6*s*u**2 + u**3)/24
c4(s,u)=-(8*s**4 - 4*s**3*u - 24*s**2*u**2 + 8*s*u**3 - u**4)/24
c5(s,u)=(9*s**5 - 50*s**4*u + 80*s**3*u**2 - 40*s**2*u**3 + 10*s*u**4 - u**5)/120
```

### Chamber 3: 2s<=u


```text
c0(s,u)=1
c1(s,u)=(26*s + 15*u)/15
c2(s,u)=3*s*u
c3(s,u)=-s**2*(37*s - 78*u)/24
c4(s,u)=-s**3*(2*s - 3*u)/2
c5(s,u)=-s**4*(23*s - 30*u)/120
```

## Appendix C — complete sign and derivative certificate

Every listed row is the complete polynomial; all other monomials are zero. Derivatives are taken at fixed s before the cone substitution. This includes all zero slots.

### Chamber 0; {'s': '2*a + b', 'u': 'a'}


```text
k=0: coefficient 1; derivative 0
k=1: coefficient 47*a/15; derivative 47/15
k=2: coefficient 49*a**2/12; derivative 49*a/6
k=3: coefficient 11*a**3/4; derivative 33*a**2/4
k=4: coefficient 11*a**4/12; derivative 11*a**3/3
k=5: coefficient 7*a**5/60; derivative 7*a**4/12
```

### Chamber 1; {'s': '2*a + b', 'u': 'a + b'}


```text
k=0: coefficient 1; derivative 0
k=1: coefficient 47*a/15 + 161*b/60; derivative 67/30
k=2: coefficient 49*a**2/12 + 91*a*b/12 + 71*b**2/24; derivative 7*a + 17*b/4
k=3: coefficient 11*a**3/4 + 97*a**2*b/12 + 57*a*b**2/8 + 7*b**3/4; derivative 95*a**2/12 + 37*a*b/3 + 27*b**2/8
k=4: coefficient 11*a**4/12 + 11*a**3*b/3 + 21*a**2*b**2/4 + 3*a*b**3 + 13*b**4/24; derivative 11*a**3/3 + 10*a**2*b + 15*a*b**2/2 + 4*b**3/3
k=5: coefficient 7*a**5/60 + 7*a**4*b/12 + 7*a**3*b**2/6 + 13*a**2*b**3/12 + 11*a*b**4/24 + b**5/15; derivative 7*a**4/12 + 7*a**3*b/3 + 3*a**2*b**2 + 3*a*b**3/2 + 5*b**4/24
```

### Chamber 2; {'s': 'a + b', 'u': '2*a + b'}


```text
k=0: coefficient 1; derivative 0
k=1: coefficient 56*a/15 + 161*b/60; derivative 21/20
k=2: coefficient 6*a**2 + 9*a*b + 71*b**2/24; derivative 3*a + 37*b/12
k=3: coefficient 119*a**3/24 + 93*a**2*b/8 + 67*a*b**2/8 + 7*b**3/4; derivative 13*a**2/4 + 13*a*b/2 + 25*b**2/8
k=4: coefficient 2*a**4 + 13*a**3*b/2 + 15*a**2*b**2/2 + 7*a*b**3/2 + 13*b**4/24; derivative 3*a**3/2 + 9*a**2*b/2 + 9*a*b**2/2 + 4*b**3/3
k=5: coefficient 37*a**5/120 + 31*a**4*b/24 + 25*a**3*b**2/12 + 19*a**2*b**3/12 + 13*a*b**4/24 + b**5/15; derivative a**4/4 + a**3*b + 3*a**2*b**2/2 + a*b**3 + 5*b**4/24
```

### Chamber 3; {'s': 'a', 'u': '2*a + b'}


```text
k=0: coefficient 1; derivative 0
k=1: coefficient 56*a/15 + b; derivative 1
k=2: coefficient 6*a**2 + 3*a*b; derivative 3*a
k=3: coefficient 119*a**3/24 + 13*a**2*b/4; derivative 13*a**2/4
k=4: coefficient 2*a**4 + 3*a**3*b/2; derivative 3*a**3/2
k=5: coefficient 37*a**5/120 + a**4*b/4; derivative a**4/4
```
