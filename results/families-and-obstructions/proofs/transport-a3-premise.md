# Independent verification of type-A3 chamber certificates

The whole-count identities, support inverse and named finite chamber
certificates withstand the mathematical and exact computational checks below.
The degree-53 cubic proposal remains uncomputed. No ordinary-negative LR
coefficient was found or inferred. Source identities are recorded in the input
manifest. The independent checker uses standard-library integer and rational
arithmetic and does not use the original AI-derived implementation.

## 1. Whole ordinary LR realization

The construction in the source character proof gives an actual equality
of full counts. For factors eta_i, put each component in its own rows and in
the column interval `(o_i,o_i+w_i]`, where `o_i=sum_{j>i} w_j`. These intervals
are disjoint; the resulting outer and inner row lists decrease. Semistandard
tableau conditions therefore separate across components, proving
`s_(lambda/mu)=product_i s_(eta_i)`. The offsets scale with the factors, so
the ordinary LR identity holds at every stretch.

For a factor with active Dynkin support S, a permutation outside the
equal-part-block Weyl subgroup changes the first j selected indices at some
active cut j. Among all j-element subsets different from the first j indices,
the smallest prefix-sum deficit is the adjacent gap. Applied to
`t eta_i+rho`, that gap is at least `t M_i+1`. All prefix deficits are
nonnegative, so a deficit exceeding `t R_j` cannot be cancelled by any
remaining normalized numerator or denominator series. The surviving
parabolic alternant is precisely the denominator for roots disjoint from S.
Highest-weight extraction contributes one final Weyl denominator, leaving
the root multiplicities

`m_J = number of factor supports intersecting J - 1`.

The stated buffer `M_i>2 max(R)` is sufficient. Each simple index lies in at
least two supports; the summed Dynkin gap dominates the largest possible
loss `2 max(R)` in the extracted target. The target is a partition with the
correct size. The more general condition used in uniform records, every
active gap greater than `max(R)` together with dominant target, also makes
the same argument work. At t=0 both sides are one.

Independently reconstructing factor partitions, support multiplicities,
offsets, outer/inner partitions, target, rank, outer size and stability
conditions passed for all 520 explicit polynomial records and the proposal
(521 explicit embeddings). This does not assert a separately constructed
unimodular map to conventional hives; the full character/count equality is
the required bridge.

## 2. Exact support inverse

For positive `(p,q,r,u,v,w)`, set `x=c_2`. The six equations force

```
c_1=w-v,                 c_2=x,                 c_3=w-u,
c_12=v-r-x,              c_13=u+v-w-q,           c_23=u-p-x,
c_123=1+p+q+r-u-v+x.
```

Their sum is w+1. The three inequalities in the source support-inverse proof
are exactly the conditions that this integer interval for x is nonempty
and every displayed count is nonnegative. Conversely substitution gives
all six coverage equations. There is no claim about other possible LR
realizations of inadmissible multiplicity systems.

An independently written composition enumeration reproduced all 3,424
support-count vectors with total 2 through 7. Its realizable positive
sextuples agree exactly with the inverse test on all 46,656 sextuples in
`{1,...,6}^6`, including all 1,585 saved positive-roster entries and their
canonical/enumerated support solutions.

## 3. Dimension, lattice and independent counts

For positive R, sufficiently small positive assignments to every nonsimple
root coordinate leave positive residuals for the simple groups. Thus the
full nonnegative fiber has a point with all coordinates positive, rank three
and dimension `sum(m)-3`. If a coordinate of R vanishes, exactly the columns
meeting it are forced to zero. Delete them first; the surviving simple
columns have rank equal to the number of positive coordinates. The exact
degree is the surviving multiplicity sum minus this rank.

All 83 minors of the six distinct root columns were checked independently;
each is 0 or +/-1. Repeating columns preserves total unimodularity. The
fiber is bounded and integral in its affine integer lattice, so its
Ehrhart polynomial has the stated degree before any values are fitted.

Let `B_k(z)=binom(z+k-1,k-1)` for k>0, and let `B_0(z)` be one at z=0 and
zero otherwise. Grouping the repeated root coordinates by their total
flows gives the positive sum

```
K_m(X,Y,Z) = sum_(c,a,b >= 0)
 B_w(c) B_u(a) B_v(b)
 B_p(X-c-a) B_q(Y-c-a-b) B_r(Z-c-b),
```

where negative arguments contribute zero. Every term counts independent
weak compositions in the six root groups. The checker caches the inner
positive convolution in `(Z-c,Y-c-a)`; this changes reuse of arithmetic,
not the count. No Weyl cancellation or original prefix-grid implementation
is used in this numerical route.

For signed interpolation, let A' contain only surviving columns and put
`B=A' 1`. The strict-point argument already established that the relative
interior consists exactly of positive surviving coordinates. Subtracting
one from each such coordinate bijects interior integer flows at sR with
nonnegative integer flows at `sR-B`. Ehrhart reciprocity therefore gives

`P(-s)=(-1)^D K_reduced(sR-B)`.

If any coordinate of this target is negative, its count is zero. The checker
independently counted D+1 consecutive signed sites from `-floor(D/2)` and
expanded Newton differences over the rationals. It directly counted unused
positive sites D+1 and D+2, then compared the entire reconstructed vector
and every saved count with the original AI-derived records.

All 456 distinct polynomials passed: 10,677 determining sites and 912 unused
positive holdouts. All 10,677 coefficients through their actual degrees are
strictly positive. There are 688 record appearances because ray certificates
repeat standalone records and the finite panels intentionally overlap.
The 64 uniform, 128 nonuniform and 208 pair records in the finite comparison panel, plus all 120
boundary-ray records, are completely covered. This is independent complete
polynomial reconstruction through a grouped-flow counter and proof-backed
signed interpolation; it is not a claim to have re-enumerated every saved
positive determining site or rerun a native LR/GT engine.

## 4. Seven cones and the infinite-direction claims

Use the seven source rays r0,...,r6. Explicit cone coordinates are:

| Cone generators | Coordinates for R=(x,y,z) |
|---|---|
| r0,r2,r5 | x-y, z-y, y |
| r2,r4,r5 | z-y, y-x, x |
| r0,r3,r5 | x-y, y-z, z |
| r3,r1,r6 | x-z, y-x-z, z |
| r4,r1,r6 | z-x, y-x-z, x |
| r3,r5,r6 | x-z, x+z-y, y-x |
| r4,r5,r6 | z-x, x+z-y, y-z |

These coordinates prove the stated region descriptions. Ordering y against
x,z, and then comparing y with x+z when it is largest, covers the whole
nonnegative orthant. Each cone is unimodular. All 16 nonsingular root bases
and all 112 cone/basis comparisons were independently rebuilt over Q. A
cone is either inside the basis cone or has a nonpositive inverse-coordinate
row with at least one strict negative entry, putting its whole strict
interior outside that basis cone. Hence no basis-cone boundary cuts a listed
cone's strict interior.

The explicit classical premise is closed-chamber polynomiality for a
unimodular vector partition function, as identified in the source references.
Positive column repetition preserves the chamber complex. The fan check
therefore puts one polynomial on each closed listed cone. Its degree-j
homogeneous component is exactly `q_j(R)=[t^j]K_m(tR)`.

For q1, nonnegative values at all seven rays are necessary and sufficient:
every point of a cone is a nonnegative combination of its generators.
All 168 independent ray values agree with the 24 submitted systems; every
submitted root-coordinate linear form was also rebuilt and matched.

For q2, the coefficient of XY in a cone with generators a,b,c is exactly
`q2(a+b)-q2(a)-q2(b)`, and similarly for the other two mixed monomials.
The complete independent ray/pair polynomials give all 112 cone forms and
their 672 monomial coefficients for the 16 named nonuniform systems. Every
coefficient matches and is nonnegative. This is a sufficient sign
certificate throughout each closed cone, including shared boundaries.

The exclusions concern q1 for these 24 systems and q2 for these 16 systems.
They do not establish arbitrary-multiplicity positivity, higher-coefficient
positivity at uncomputed directions, or new original-box coverage.

## 5. An uncomputed cubic and a reduced interpolation set

For the degree-53 proposal, all seven support counts are two, giving
`m=(7,7,7,11,11,13)`. The supplied factors have minimum positive Dynkin
label nine, exceeding `2 max(3,4,2)=8`. Independent reconstruction gives
rank 34, outer size 4571 and exact prior degree 53. The target is
`(234,159,83,2)`. The direction `(3,4,2)=r3+r5+r6` lies strictly inside
the corresponding cone. It is absent from the computed polynomial roster.
Its full polynomial and cubic value remain uncomputed in this verification.

The proposed ten-direction cubic interpolation in the source proof
is valid, but the already saved complete pair polynomials reduce new work.
Write the binary-edge cubic as

`A X^3+B Y^3+u X^2 Y+v X Y^2`.

The known pair sum gives `S=q3(a+b)-A-B=u+v`. One new ordered value gives
`U=q3(2a+b)-8A-B=4u+2v`. Thus

`u=(U-2S)/2`, and `v=(4S-U)/2`.

The cone's remaining XYZ coefficient is

`q3(a+b+c)-q3(a)-q3(b)-q3(c)-S_ab-S_ac-S_bc`.

There are 13 distinct unordered cone edges. Their known pair-sum cubic
values need only 13 new ordered values. Of the seven triple sums, the
direction `(2,1,2)` is already computed. Therefore 19 distinct additional
directions suffice generically for the existing 16 systems. The full list,
known rational values and exact reconstruction equations are in
`cubic-next-test.json`.

For the selected degree-53 system there is a further exact reduction.
Exchanging U and W in the generating function proves
`K(x,y,z)=K(z,y,x)` because p=r and u=v. Setting z=0 deletes every root
meeting coordinate three, leaving the symmetric A2 kernel with p=q=7;
hence `K(x,y,0)=K(y,x,0)`. The first symmetry exchanges the two mixed
coefficients on the edge (r0,r2), so each equals S/2 with no new count.
It identifies five pairs of the remaining ordered directions and the
three pairs of uncomputed triple sums. The boundary symmetry additionally
identifies `(3,1,0)` with `(1,3,0)`. This leaves the following
sufficient nine-direction roster:

| New direction | Prior full-polynomial degree | Role |
|---|---:|---|
| (3,1,0) | 23 | Representative of four boundary ordered directions |
| (3,1,1) | 53 | Ordered edge (r0,r5) and reflected edge |
| (1,4,1) | 53 | Ordered edge (r1,r6) |
| (3,3,1) | 53 | Ordered edge (r3,r5) and reflected edge |
| (3,4,1) | 53 | Ordered edge (r3,r6) and reflected edge |
| (3,4,3) | 53 | Ordered edge (r5,r6) |
| (3,2,1) | 53 | Triple sum for cone (r0,r3,r5), and reflected cone |
| (2,4,1) | 53 | Triple sum for cone (r3,r1,r6), and reflected cone |
| (3,4,2) | 53 | PROP-CUBIC-01 and reflected cone |

This roster is prepared, not executed. It recovers the full seven-cone
cubic, after which an exact sign analysis is still required. A negative
mixed monomial coefficient is only a lead. A negative evaluation at a legal
integer R, independently checked and realized using stable buffers, creates
an ordinary-negative LR example requiring full verification. Nonnegative cone monomial coefficients
would suffice for a cubic exclusion; more general nonnegative cubics may
need a different exact certificate.

## 6. Original computation and verification limits

The original calculation used a 120-second limit per process and a cumulative
900-second limit. Every recorded numerical process completed or was terminated.
The host rejected address-space and RSS soft limits, so those memory limits
were not enforced. Observed peak RSS was
51,888,128 bytes, below one GiB. An initial unsupported hard-limit setup and
one saved-roster field-name mismatch were repaired and retained as failed
attempts in the journal. All final computational stages passed.

Classical Weyl theory, Ehrhart reciprocity and unimodular chamber polynomiality
remain explicit mathematical premises. No historical priority claim or new
literature verification is made. The recorded checks cover the named finite
A3 certificates and do not compute the proposed additional cubic values.
