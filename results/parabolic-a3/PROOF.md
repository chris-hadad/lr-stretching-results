# A3 realization and exact finite certificates

All vectors and multiplicities below are integral unless indicated
otherwise. The six positive roots, in order, are

`e1, e2, e3, e1+e2, e2+e3, e1+e2+e3`.

Their positive multiplicities are `m=(p,q,r,u,v,w)`. Write K_m(R) for the
coefficient of the six-factor generating function in the README. Let
`q_j(R)=[t^j]K_m(tR)`.

## Whole ordinary Littlewood–Richardson realization

Give the seven nonempty subsets S of {1,2,3} nonnegative counts c_S. Suppose
every interval root J has

`m_J=sum_(S intersects J) c_S - 1 > 0`.

Choose one GL4 partition eta_i per support occurrence, with Dynkin labels
M_i on S and zero off S, where `M_i>2 max(R)`. Pad with a fourth zero row.
Writing T for the componentwise sum of these factors, the extracted target is

`theta=(T1-R1, T2+R1-R2, T3+R2-R3, R3)`.

Each simple index occurs in at least two supports, so the summed positive
Dynkin gaps dominate the possible loss `2 max(R)`. Thus theta is a partition
of the correct size.

Normalize the Weyl character of eta_i by its highest monomial. Its numerator
is a sum of monomials with nonnegative simple-root exponents. The zero-label
parabolic subgroup permutes equal-part blocks. A permutation outside that
subgroup changes the selected prefix at some active cut j. For the strictly
decreasing vector `t eta_i+rho`, its prefix deficit there is at least the
active adjacent gap `t M_i+1`. It cannot contribute to the rectangle up to
tR, because that deficit exceeds tR_j and subsequent factors have
nonnegative exponents. The surviving numerator is exactly the Weyl
denominator for the roots disjoint from S.

Highest-weight extraction contributes one final Weyl denominator. After
parabolic cancellation, the surviving denominator exponent for root J is
the number of supports meeting J minus one, namely m_J. Hence the full
tensor multiplicity is K_m(tR) for every positive t; both constant terms
are one at t=0.

To turn the tensor coefficient into one ordinary LR coefficient, let h_i
and w_i be the positive height and width of eta_i and set
`o_i=sum_(j>i) w_j`. Form lambda from all rows `o_i+eta_(i,r)` and mu from
h_i copies of o_i, dropping trailing zeros. Both row lists decrease. Each
skew component occupies its own rows and a column interval disjoint from
every other component. Therefore its skew Schur function is the product
of the factor Schur functions. Offsets scale under dilation, giving

`c^(t lambda)_(t mu,t theta)=K_m(tR)`.

This is equality of full counts. No separate lattice isomorphism to a
conventional hive polytope is required or asserted.

## Exact admissibility of the support construction

In support order `1,2,3,12,13,23,123`, the coverage equations have the solution

```
c_1=w-v,                 c_2=x,                 c_3=w-u,
c_12=v-r-x,              c_13=u+v-w-q,           c_23=u-p-x,
c_123=1+p+q+r-u-v+x.
```

All entries are nonnegative precisely when

```
w >= max(u,v),
u+v >= w+q,
max(0,u+v-p-q-r-1) <= x <= min(u-p,v-r).
```

The endpoints are integral, and substitution proves sufficiency. Their sum
is w+1. These are necessary and sufficient conditions for this support
construction. Every system in the data passes the inverse and all six
coverage equations. Failure does not rule out a different LR realization.

## Fiber dimension, integrality and reciprocal interpolation

Let A_m repeat each root column its prescribed number of times. The counted
fiber is the whole polytope `{x>=0:A_m x=R}` in its affine integer lattice.
For positive R, sufficiently small positive values on all nonsimple root
coordinates leave a positive residual for each simple group. Thus all
coordinates can be positive, the rank is three, and the dimension is
`sum(m)-3`. Every column is nonzero and nonnegative, so the fiber is bounded.

If a coordinate of R is zero, delete all columns meeting that coordinate:
those flow coordinates are forced to zero. The surviving simple columns
have rank s, the number of positive coordinates of R. The same strict-point
argument shows that the exact dimension is N-s, where N is the surviving
multiplicity sum. At R=0 the fiber is one point.

The six interval columns are totally unimodular; the program checks all
83 minors directly. Repeated columns preserve this property. The surviving
simple columns supply an integral affine origin. Consequently the fiber is
an integral polytope, and its Ehrhart degree is exactly N-s before fitting.

For the reduced matrix A', put `B=A' 1`. The strict point implies that the
relative-interior integer flows are exactly those whose surviving
coordinates are all at least one. Subtracting one from each coordinate
bijects them with the nonnegative flows at `sR-B`. Writing d for the
proved dimension and P(t)=K_m(tR), Ehrhart–Macdonald reciprocity gives

`P(-k)=(-1)^d K_reduced(kR-B)` for positive k.

Negative target coordinates give zero. This formula supplies D+1 consecutive
signed values, from `-floor(D/2)` through `D-floor(D/2)`, where D is the
proved degree. Newton forward differences, expanded over Q, recover the
complete polynomial. Direct counts at D+1 and D+2 are unused positive
holdouts, separate from all determining sites.

## Independent positive counting formula

For k>0 define `B_k(z)=binom(z+k-1,k-1)`, and let B_0 be the delta function
at zero. Negative arguments contribute zero. Grouping the repeated root
coordinates by total flows gives

```
K_m(X,Y,Z) = sum_(a,b,c >= 0)
 B_u(a) B_v(b) B_w(c)
 B_p(X-a-c) B_q(Y-a-b-c) B_r(Z-b-c).
```

Each factor counts a weak composition within one group of repeated roots;
the simple group totals are then forced. The implementation caches the
inner convolution over b as a function of the residual second and third
coordinates. This is arithmetic reuse inside the positive sum. All
polynomials and signs are reconstructed using Python integers and exact
rational arithmetic.

## Seven cones and the sign certificates

The rays are

```
r0=(1,0,0), r1=(0,1,0), r2=(0,0,1), r3=(1,1,0),
r4=(0,1,1), r5=(1,1,1), r6=(1,2,1).
```

Explicit nonnegative cone coordinates for R=(x,y,z) are:

| Generators | Coordinates |
|---|---|
| r0,r2,r5 | x-y, z-y, y |
| r2,r4,r5 | z-y, y-x, x |
| r0,r3,r5 | x-y, y-z, z |
| r3,r1,r6 | x-z, y-x-z, z |
| r4,r1,r6 | z-x, y-x-z, x |
| r3,r5,r6 | x-z, x+z-y, y-x |
| r4,r5,r6 | z-x, x+z-y, y-z |

Ordering y relative to x,z and, when y is largest, comparing y with x+z
proves coverage of the entire nonnegative orthant. Every cone is
unimodular. The program enumerates the 16 nonsingular root bases and checks
all 112 inverse-basis matrices on the cone generators. Each whole cone is
inside the basis cone, or some coordinate row is everywhere nonpositive
and negative on at least one generator. In the latter case the entire
strict interior is outside the basis cone. Thus no root-basis boundary
cuts a listed cone's strict interior.

The classical premise used here is polynomiality of a unimodular vector
partition function on closed chamber cones: see J. A. De Loera and
B. Sturmfels, *Algebraic Unimodular Counting*, arXiv:math/0104286, Theorem
1.1 and the chamber-complex characterization. Positive column repetitions
do not change the chamber complex. The verified fan is a common refinement,
so q_j is homogeneous of degree j on each closed listed cone.

It follows that q1 is nonnegative everywhere in the orthant if and only if
its seven ray values are nonnegative. The 24 listed systems satisfy this
criterion, with all deciding values independently reconstructed.

For a cone with generators a,b,c and coordinates X,Y,Z, q2 equals

```
q2(a) X^2 + q2(b) Y^2 + q2(c) Z^2
+ (q2(a+b)-q2(a)-q2(b)) XY
+ (q2(a+c)-q2(a)-q2(c)) XZ
+ (q2(b+c)-q2(b)-q2(c)) YZ.
```

The seven cones use 13 distinct pair sums. The complete ray and pair
polynomials determine all 112 quadratic forms for the 16 designated
systems. Each of their 672 cone monomial coefficients is nonnegative,
which suffices for q2>=0 on every cone, including shared boundaries.

These finite exact certificates concern only the stated multiplicity
systems and coefficient indices. They do not establish arbitrary-system
positivity or signs of higher components on uncomputed directions. Weyl
characters, disconnected skew Schur products, Ehrhart theory and chamber
polynomiality are classical ingredients; no priority claim is made for
the construction or certificates.
