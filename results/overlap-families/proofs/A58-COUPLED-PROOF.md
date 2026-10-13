# A58 independent adoption: complete coupled cancellation and one residual cap

Curated mathematical proof from **A58**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

27 September 2026. Root proof checking and rederivation of selected Pro046
U10/U11 results. The originating proofs retain their original source qualification; only the exact stated claims are in scope. Returned programs were not imported or executed.

## 1. Literal original and the complete two-partner map

Let a>=2, b>=c>=1, 0<=h<=b, u,v>=b, and k_i>=0 be integers, with k_a>0.
Set K=sum k_i, sigma_i=sum_(j>=i)k_j, d=K-c, p=b-h and delta=b-c. Require
0<=d<=k_a. The entire original is


```text
lambda=(K+u+v-h,K+v,sigma_1,...,sigma_a),
mu=(K+v-h,K,sigma_2,...,sigma_a,0),
nu=(u+v+K-b-c,b,c).
```

The two top row widths are u,v and their overlap is h; every other row is
isolated with its original capacity k_i. Partition inequalities, containment
and balance follow directly; nu_1>=b+d>=b. Maximum trimmed original rank is
exactly a+2 because the last outer part is k_a>0. These statements also hold
when an interior cap is zero; such a row does not delete an outer part.

The complete highest-weight annihilator checked in FIRST-WALL-PROOF.md gives


```text
P_h(t)=[x^(pt)y^(ct)]Phi/(1-x)
         -[x^(bt+1)y^((c-h)t-1)]Phi/(1-y),
Phi=product_i h_(k_i t)(1,x,y).
```

Both shifts occur once. Complementing the exact y total of the first domain
gives nonnegative pairs (U_i,Z_i), with total d t, sum U_i<=p t, and every
pair bounded by k_i t. For the second domain, complement its exact x total:
the corresponding total is (K-b)t-1 and its aggregate bound is (c-h)t-1.
Add delta*t+1 to the LAST U coordinate. This is an integer injection into
the first domain; all other pair caps are unchanged, and the last cap is
paid by k_a>=d. Its image is precisely U_a>=delta*t+1. Subtracting the same
integer is its inverse. If either second-domain bound is negative, the image
is empty for the same reason. Therefore the ENTIRE original is the count


```text
U_i,Z_i>=0, sum_i(U_i+Z_i)=d t,
sum_i U_i<=p t, U_a<=delta t,
U_i+Z_i<=k_i t for i<a.                              (1)
```

This adopts Pro046 P046-U10-T01 as a complete count and degree theorem.
It does not sign every middle coefficient of (1). No generic original
hive-face isometry or transfer of normal-cycle weights is asserted.

For d=0, (1) is one point. For d>0 let E be the number of positive k_i.
Zero pair caps force their two coordinates to zero. Eliminate Z_a from the
primitive total equation; when p=0 eliminate every U, and when p>0,delta=0
eliminate U_a. The remaining lattice is saturated, of exact dimension


```text
p=0: E-1;    p>0,delta=0: 2E-2;    p>0,delta>0: 2E-1.
```

Strict small positive choices for all remaining coordinates show that no
other equality is forced. The network with cap nodes feeding U/Z aggregators,
the aggregate U bound and the special absorber-to-U bound has an integer
incidence matrix with unit bounds. Thus the polytope is integral in that
lattice. Its Ehrhart degree is the displayed dimension. The original count
equality transports this degree, without asserting generic hive integrality.

## 2. One two-increment span, all flags, and the finite positive factor class

Independently consider 0<=x_1<=...<=x_N<=d t, arbitrary integer upper
flags x_i<=f_i t, and ONE span x_(j+2)-x_j<=k t, where N>=3,
1<=j<=N-2 and all parameters are nonnegative integers. At k>0 write each
positive coordinate uniquely as (beta_i-1)t+v_i, 1<=v_i<=t; zero
coordinates have beta_i=0 and are fixed. The beta sequence is weakly
increasing and bounded by d and the flags. Its population is independent
of t. A positive equal-band block gives a chain of weakly ordered v's.

If beta_j=0 the span is equivalent to beta_(j+2)<=k. Otherwise its band
difference must be <=k, and equality imposes v_(j+2)<=v_j. For k>0 the
two endpoints then lie in distinct blocks. The only intervening coordinate
is x_(j+1), so the resulting connected factor is two chains
A_1<...<A_u, B_1<...<B_v with a relation B_s<=A_r satisfying
(u-r)+(s-1)<=1. Other factors are independent chains. At k=0 identify
the primitive equality x_j=x_(j+1)=x_(j+2), use the minimum flag on that
triple, and work with the shorter chain. No cyclic weak order is miscounted.

Write W_m(z)=binom(z+m-1,m), E_n(z)=binom(z+n-2,n),
F_n(z)=binom(z+n-3,n), with n=u+v. Directly classifying the forbidden
relative positions of the two chains gives these complete order polynomials:


```text
B_1<=A_u:        W_u W_v-E_n;
B_1<=A_(u-1):    W_u W_v-2E_n-(v-1)F_n;
B_2<=A_u:        W_u W_v-2E_n-(u-1)F_n.
```

For the first formula the forbidden assignments form one concatenated chain
with one strict junction. For the second, insert A_u among the B values:
the two endpoint positions have one strict junction and the v-1 interior
positions have two. Duality gives the third formula. Their linear
coefficients are respectively 1/[n(n-1)],
2(u-1)/[n(n-1)(n-2)] and 2(v-1)/[n(n-1)(n-2)], all positive.
The latter formulas apply only where n>=3.

This class, together with disjoint unions, is closed under lower ideals and
upper filters. Retaining prefixes/suffixes can shorten either chain or turn
the link into an endpoint link; it cannot create a second overhang. Retain
transitive comparisons when deleting intermediate elements. For every poset,
the elementary ideal split of maps into [x+y] gives


```text
Omega_P(x+y)=sum_(I ideal) Omega_I(x)Omega_(P\I)(y).
```

Putting x=y=z gives, for q>=2,


```text
(2^q-2)[z^q]Omega_P
  =sum_(empty!=I!=P) sum_(l=1)^(q-1)
       [z^l]Omega_I [z^(q-l)]Omega_(P\I).
```

Induction on the number of elements, using the explicit positive linear
terms, proves every coefficient nonnegative. Connected factors are strict:
for an endpoint link the full B-chain ideal supplies two strict chain
factors; for a single overhang, deleting the end element leaves an endpoint
link and a singleton. These terms pay every higher degree in the recurrence.
This rederives the finite factor argument of Pro046 U11-01. The classical
ideal identity and reduction are also checked in Ferroni--Morales--Panova,
*Skew shapes, Ehrhart positivity and beyond*, arXiv:2503.16403v3, Section 3.
Arbitrary width-two positivity is a conjecture in that paper, not an input.

Summing these paid factors over ALL admitted band sequences proves the
whole flagged-chain theorem. Increasing upper flags selects additional
complete band states, so gains are coefficientwise nonnegative. It does
not prove monotonicity in the span parameter k. After the k=0 collapse,
delete the prefix forced zero. The remaining coordinates form a saturated
integer lattice; all can be strictly increasing and sufficiently small.
Placing them in the first positive band contributes a full chain order
polynomial, strict in every positive degree up to the actual dimension.
The unique zero assignment pays the constant one.

## 3. Complete one-cap original theorem and paid generator

Specialize (1) to a>=3, k_1=kappa>=0, and every k_i>=d for i>=2.
The only nonautomatic pair cap is U_1+Z_1<=kappa t. Order the residual
increments as

    U_a,U_2,...,U_(a-1),U_1,Z_1,Z_2,...,Z_a.

Take their cumulative sums except the final total. The map and inverse use
integer triangular matrices with determinant one. The exact domain is


```text
0<=x_1<=...<=x_(2a-1)<=d t,
x_1<=delta t, x_a<=p t,
x_(a+1)-x_(a-1)<=kappa t.                            (2)
```

It retains both original character terms, the aggregate flag and the small
pair cap, including p<d and kappa<d/2. Section 2 signs every coefficient.
At kappa=0 identify the central triple; a>=3 leaves the required other U
coordinate available. The degree is exactly Section 1's formula with
E=a for kappa>0 and E=a-1 for kappa=0. The d=0 case remains a point.

For fixed widths, b,c,u,v, lower h from b to any target h>=0. Every
intermediate is a legal original with the same total, output and rank.
The median flag P=min(b-h,d) increases; its full gains are sums of new
band states, with constant zero. Every nonzero gain is strict through degree
2E-1 if delta>0, or 2E-2 if delta=0. To see this, put all free coordinates
in the unit band (P0 t,(P0+1)t] when delta>P0. Otherwise put x_1 in
[0,delta t] and the remaining coordinates in that band. The cap endpoints
both have index at least two, so the span holds. These subcollections pay
all asserted degrees, and their complements are still paid band states.
For kappa=0 apply the same argument in the primitive quotient.

The initial h=b parent is explicitly paid:


```text
binom(d t+a-1,a-1)
  -1_(kappa<d) binom((d-kappa)t+a-2,a-1).
```

If kappa=0 Pascal reduces it to binom(d t+a-2,a-2). If 0<kappa<d,
match the a-1 factors of the two products: each difference is kappa*t+1.
Product telescoping pays every coefficient. Other endpoints are a binomial
or point. The integer distance to the target h decreases at each step.
Saturation occurs precisely at P=d because U_2=d t is a feasible residual
witness. This adopts the U11 original theorem and generator at this exact
scope. An overlap gain is not asserted to be a single affine LR family.

## 4. Exact checks, failed variants, and remaining domain

The independently authored coupled_v2.py checks 96 endpoint/overhang factor
classes at u,v=1..6 against a separate ideal-prefix count, including all
determining grades and two unused positive grades. It directly counts seven
complete residual families and compares every supplied positive grade with
the separate bare-original LR engine. These include the paid initial,
crossing and saturated U11 parents, zero-cap and balanced degree drops, and
the distinct two-small-cap U12 discriminator. It checks the two actual
shifted partner counts and three entire nonzero overlap-gain vectors.

Six exact mutations fail as required: dropping the small cap, aggregate
flag or absorber-U flag; omitting or stretching the once-only shifts; and
making the pair endpoint strict. For the main rank-seven original the
correct grade-two value is 3472, whereas these wrong grade-two values include
4074,3580,3133,3565 and 2644. At grade one cap deletion gives 180 instead
of 157. The first checker attempt encountered a record-schema KeyError;
its exact code/failed receipt are preserved and no result was accepted.
The fresh v2 handles both producer schemas and passes all scientific checks.

The U12 two-small-cap original has caps (1,1,3,3,3), b=9,c=8,h=7,
rank seven and degree nine. Its full vector is independently recovered and
positive; it remains ONE computed original, not a uniform two-cap theorem.
General interacting residual caps, no-absorber parents, adjacent/triple
overlaps and unrestricted three-row-inner generation are still open.
Neither this theorem nor the separate A58 first-wall theorem closes whole
rank seven or general KTT. The source return's other claims remain unadopted source
unless independently accepted at an explicitly listed earlier scope.
