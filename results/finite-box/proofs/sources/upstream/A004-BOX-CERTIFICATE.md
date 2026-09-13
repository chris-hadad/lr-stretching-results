# Closing the highest-dimensional original-box strata

The independent review of this certificate is complete; see review/DISPOSITIONS.md. This is a complete certificate for the named
strata and a whole-box coefficient consequence, not a certificate of the whole
box. The counted original domain still contains 651,229,702 rank-six/seven
roots before its other theorem predicates are resolved.

## What is proved

1. Every full-dimensional rank-six hive in the original area-30 box is
   coefficientwise positive. Its complete strict-padded candidate roster has
   twenty-six original identities: thirteen exact zeros, six proper Horn
   factorizations and seven positive degree-ten polynomials.
2. A rank-seven boxed hive has degree at most thirteen. If its degree is
   thirteen, it is one of exactly two stated original hives; both complete
   polynomials are now independently authenticated and positive.
3. Consequently the eleventh ordinary coefficient is nonnegative throughout
   the entire original box. The possible negative indices are now
   `1..min(d-2,6)` at boxed rank six and `1..min(d-2,10)` at boxed rank seven.
   The corresponding all-size rank-seven frontier still includes index eleven.

The rank-six cap at index six also uses the previously adopted all-size
source-transfer premise, explicitly recorded in
`methods/ferudun-ktt5-2026-09-05/README.md` lines 50–55 and its source audit.
It is not deduced merely by removing the degree-ten stratum here.

All original identities, empty cases, degenerations and source dependencies
are retained. Overlaps with previously certified classes are retained in the finite accounting.

## Boundary gaps force dimension loss

For each adjacent gap on each padded boundary, two nonnegative hive rhombus
slacks sum to that gap, modulo the trace equality. Their interior normals
are opposite and nonzero. The boundary-gap certificate lists all fifteen identities
at rank six and all eighteen at rank seven, directly in the canonical
`hive_linear_system` convention. Therefore a zero gap forces a genuine
affine equality. If the normals forced by zero gaps span rank `r`, then
the actual hive dimension is at most `D_n-r`.

For the two inner boundaries these primitive normal vectors are coordinate
units or differences of two coordinate units. Their rank is exactly the
rank of the corresponding graph incidence edges, computed by a spanning
forest; no floating rank threshold is used. At ranks six and seven the
largest total index weight of one parallel class is respectively six and
seven. The only two-inner corner overlap is accounted for explicitly.

For a padded inner partition with gaps `g_i`, its area is

```text
n*mu_n + sum(i=1..n-1) i*g_i.
```

All nonzero integral gaps are at least one. Thus if a nonempty hive has
dimension at least `D_n-1`, its two inner partitions have total area at least
`n*(n-1)-n=n*(n-2)` for these ranks. In particular rank-seven degree
fourteen would require area at least thirty-five, outside the box. This
rederives the degree-thirteen ceiling without relying on the older large
equality-mask census.

## The complete rank-six strict roster

A degree-ten rank-six hive has no zero boundary gap. Its two strict-padded
inners each have area at least fifteen. Total area at most thirty therefore
forces both to be `rho=(5,4,3,2,1)`, with a padded sixth zero. The outer
partition has six distinct positive parts totaling thirty. Two independent
enumerators agree: a decreasing-part recursion and the six-element subsets
of `1..15` whose sum is thirty. There are exactly twenty-six.

The exact triples match both recorded geometry implementations and both Horn
classification implementations. Fresh checks prove the thirteen zero terminals from valid
negative Horn slacks and the six product terminals from multiplicity-one
Horn equalities. Every proper rank-six Horn split has rank-at-most-five
children, so the adopted all-size KTT5 theorem settles their coefficients.
The seven remaining whole hives have exact rational strict points in the
standard saturated ten-dimensional hive lattice.

The first strict-point replay caught a real convention error: historical FE
uses `h_old(i,j)` where the current builder uses `h_new(j,i)`. The failed
attempt is retained. The repaired permutation is explicit, and all forty-five
slacks of each transformed witness are strictly positive. Neither a historical
degree label nor the current polynomial's length supplies the degree premise.

All seven complete Normaliz vectors are newly computed. The original planned
positive-node LR reconstruction stopped at FE/018, stretch ten, after its
sixty-second cap. That failed calculation is retained. Thirty-two later requests
were not executed; their specified inputs remain recorded.

## The interior repair that makes reconstruction practical

For these strict rank-six hives,

```text
Q(i,j)=6*(i+j)-i^2-j^2-i*j
```

has every rhombus slack one. Subtract it from a strict integer hive, then
apply the exact determinant translation. With `rho=(5,4,3,2,1)`, this gives

```text
P(-j)=I(j)
     = c^(j*lambda-(15,13,11,9,7,5))_((j-2)*rho,(j-2)*rho), j>=3.
```

The degree is even, so reciprocity has positive sign. Invalid shifted
boundaries give zero by an explicit necessary boundary or Horn inequality.
The first two interiors are zero: at one the shifted inner gaps are negative;
at two determinant removal leaves zero inner weights and a nonzero trace-zero
outer weight. Every one of the forty-five unit-slack identities is checked.

The mixed nodes `-5,-4,...,5` determine the full degree-ten polynomial.
Fifteen of the twenty-one requested interiors at three, four and five have
exact zero certificates, leaving only six new bare-LR calls. Positive nodes
six and seven are unused in this new interpolation. FE/018's values at those
sites were already observed under the abandoned plan; they are unused-in-fit
checks, not newly blind observations. Its two extra positive values remain
additional checks. The other six parents' low positive nodes and holdouts
were completed under the new schedule.

The independent LR vectors match all seventy-seven Normaliz coefficients.
They represent seven original input triples and five distinct polynomials, with seventy
strictly positive nonconstant coefficient occurrences. Missing, duplicated,
misattached and altered certificate fixtures are refused. The complete record
is `science/results/A004-STRICT-CERTIFICATE-001.json`.

## Exactly two highest-degree rank-seven triples

For a degree-thirteen rank-seven boxed hive, the zero-gap normals of the two
inners can span rank at most two. The same is true after exchanging the
inners, since LR commutativity preserves the entire polynomial and degree.
Area at most thirty requires at least twelve units of missing gap index
weight from the strict-inner baseline forty-two.

The complete 4,096 two-inner zero-gap masks are checked by exact incidence
rank in both orientations. The only surviving mask has `mu6=mu7` and
`nu6=nu7`, with all earlier gaps positive. The area constraint then forces
both last parts to be zero, both inners to be exactly `rho`, and the outer
area to be thirty. Adding an
outer zero gap raises the forced rank above two except possibly at the last
gap, `lambda6=lambda7`.

That last exception also reduces dimension. Use row-first tableau coordinates
`x_ij`. The zero sixth and seventh contents force `x66=0`; the last two zero
inner parts force `x71=0` by the first column inequality. If the last two
outer rows have equal length, the column inequality for label five is

```text
lambda6-lambda7-x65 >= 0,
```

so `x65=0` too. The fourteen row/content equations on the twenty-eight
triangular coordinates have rank thirteen; adding these three coordinate
equalities raises the rank to sixteen. Thus the actual dimension is at most
twelve. This exact rank certificate is retained and does not assume that
raw repeat counts equal dimension loss.

The degree-thirteen outer must therefore have seven strictly decreasing
positive parts of area thirty. Subtracting `(7,6,5,4,3,2,1)` leaves a
partition of two, so the only possibilities are

```text
d13a: lambda=(9,6,5,4,3,2,1), mu=nu=rho;
d13b: lambda=(8,7,5,4,3,2,1), mu=nu=rho.
```

The intermediate twenty-one possible outer identities are also explicitly
classified: eight Horn zeros, four Horn dimension bounds, seven additional
outer-repeat dimension bounds, and these two actual degree-thirteen objects.
Their complete saturated lattices and exact codegrees six/four are the
previously adopted degree-thirteen proofs.

## Completing the two original degree-thirteen vectors

The accepted affine interior translation has shifts

```text
Delta_lambda=(16,14,12,10,8,6,4),
Delta_mu=Delta_nu=(11,9,7,5,3,0,0).
```

For `j>=6` in d13a and `j>=4` in d13b,

```text
P(-j)=-c^(j*lambda-Delta_lambda)_(j*mu-Delta_mu,j*nu-Delta_nu).
```

The minus sign is essential because the actual dimension is thirteen. The
full eroded/shifted polytopes are equal by the original exact certificates;
all 340 Farkas identities were rechecked before any new count. This is the
proved affine-boundary repair, not the refuted homothetic reflection.

The new determining sets use the previously authenticated positive nodes
`1,2,3,4,7,8` for d13a and `1,2,3,4,7` for d13b, constant one, the proved
negative zeros, and seven newly counted nonzero interior nodes. Each has
exactly fourteen distinct nodes. Positive stretches five and six are unused
in these fits and were freshly recounted as four holdouts. Their older values
remain known; no blind-context claim is made. The old failed positive sites
nine/eight were not retried.

Both fresh complete Normaliz vectors agree with the independent LR fits and
the preserved original arrays: all twenty-eight coefficients, including all
twenty-six nonconstant coefficients, are positive. The record is
`science/results/A004-FRF-CERTIFICATE-001.json`. The numerical reconstruction
is complete at this exact scope, with its independent-review qualification retained.

## Whole-box consequence and remaining work

At rank seven, degree thirteen is now positive, degree fourteen/fifteen is
impossible in the box, and at degree at most twelve the eleventh coefficient
is leading, next-to-leading or zero. Intrinsic top-two positivity therefore
certifies `c11>=0` for every boxed rank-seven hive. Smaller ranks have degree
at most ten, so the same coefficient vanishes there.

The remaining original-box problem lies at rank six, dimension at most nine,
and rank seven, dimension at most twelve. No count of that residual population
has been manufactured. The recorded 206 rank-seven degree-twelve and 1,636 rank-six degree-nine
populations are separate layers. Their source identities, exhaustiveness and
full verification are additional requirements for any further whole-box
coefficient or coverage conclusion. The broader
35,353/4,403 source margins are not silently subtracted from the original
651,229,702 identities.
