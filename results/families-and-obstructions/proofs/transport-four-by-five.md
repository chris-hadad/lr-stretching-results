# The full 4-by-5 transportation linear coefficient and its sharp minimum

This AI-assisted derivation uses a complete finite exact A3 certificate. The all-N higher-class
vanishing conjecture remains open. This is the complete N=5 extension.

## 1. The theorem

For all positive integral r in Z^4 and c in Z^5 of the same total,

 [t]F_{r,c}(t)=D_{4,5}(r,c)>=325/72>0,                     (1)

with D defined in [the double-cut proof](transport-double-cuts.md). Equality is attained at rows(2,1,1,1), columns
(1,1,1,1,1). Every member is a whole ordinary rank 8 LR polynomial of degree 12
under the explicit construction below. This proves only c1 for the whole class,
not positivity of every coefficient or all rank 8 LR polynomials.

The double-cut proof settles every one/two-class contribution for arbitrary multiplicities.
The remaining task is exactly the higher-class vanishing, not a fit to margins.
For N=5, class counts n=(n1,n2,n3,n4) satisfy sum n=5. When n1=0 the first
netflow target is eventually negative for positive r1, so it contributes nothing.
There are exactly 22 n with n1>=1 and at least three positive entries: 18 with
three occupied classes,4 with four. These are the ENTIRE relevant roster.

## 2. Complete polynomial certificate, before the first-jet evaluation

Use roots 100,010,001,110,011,111 and multiplicities

 m=(n1+n2,n2+n3,n3+n4,n1+n3,n2+n4,n1+n4).

Their total is 15 and rank is 3, so the chamber degree is at most 12 before counting.
Every m is positive for this roster. The assignment offset is

 delta=(-n2-n3-n4,-2(n3+n4),-3n4).

The seven cone bases are, as columns,

 (100,001,111), (001,011,111), (100,110,111),
 (110,010,121), (011,010,121), (110,111,121), (011,111,121).

The inherited complete A3 proof establishes that these unimodular cones cover
the orthant and refine all 16 root-basis cones. Repetition preserves the fan.
[The complete A3 proof](transport-a3-premise.md) gives the cone argument;
its classical premise is unimodular vector-partition chamber polynomiality.

For a degree<=D polynomial f in three variables, values on e>=0,|e|<=D give

 f(x)=sum_{|e|<=D} f(e) prod_{i=1}^3 binom(x_i,e_i)
                            binom(D-sum x,D-|e|).         (2)

Indeed the four barycentric binomial coordinates sum to D. At a lattice node
of the same simplex the product is 1 only for its own node and 0 for every other.
These cardinal polynomials have degree<=D, and there are binom(D+3,3) of them,
the dimension of the polynomial space. This proves unisolvence and (2).

All determining sites are the STRICT-interior cone coordinates x=1+e,|e|<=12:
455 sites for each of 154 chamber polynomials. The fresh grouped-root integer
DP computes their full counts. Starting at value 1 at 0, each root copy alpha
updates f(v) by f(v)+f(v-alpha) in increasing coordinates. Induction on copies
proves the count; no signed cancellation appears in this DP. Coordinate
truncation is exact because every root coordinate is nonnegative.

Differentiate (2) at G^{-1}delta-(1,1,1), then transform the gradient back to
ambient coordinates. For target tR+delta, the assignment's c1 is exactly
sign*grad(P_G)(G^{-1}delta) dot G^{-1}R.

[The complete chamber certificate](../data/transport/four-by-five-source.json) contains every determining integer, all 154 exact gradient
vectors, and two UNUSED strict-interior holdouts per chamber: e=(13,0,0) and
(0,14,1). All 308 holdouts agree. Every one of the 154 gradients is exactly zero.
There are 70,070 determining occurrences; all represent the fixed 22 systems,
not that many distinct LR triples. An independent postcheck re-forms the expected
roster and verifies no system/cone is missing or duplicated.

Since each higher-class multiplicity system here is positive, the same
closed-chamber polynomiality applies on walls. If the slope lies on a wall,
the affine offset chooses an adjacent chamber; if tied identically use its
closed-wall restriction. Every relevant adjacent gradient is zero, so this
cannot hide a boundary contribution. A negative root-cone target contributes
zero eventually. Finite exact eventual equality identifies the complete
polynomial's linear term; F itself is the full integral Ehrhart polynomial.
Thus every higher-class contribution vanishes and (1)'s equality follows.
This argument does NOT extrapolate the 22-system certificate to arbitrary N.

## 3. Sharp positive minimum and explicit whole LR bridge

D is a positive sum of minima of homogeneous linear forms. It is nonnegative
on nonnegative balanced margins and superadditive. Since total M>=5, some row
has margin>=2. Subtract rows(2,1,1,1) with that row placed at the 2, and subtract
one from every column. The residual pair is nonnegative and balanced. Separate
permutation symmetry and superadditivity give

 D(r,c)>=D((2,1,1,1),(1,1,1,1,1))=325/72.

The residual D need not be the Ehrhart coefficient of the dimension-dropped
boundary for this argument; only its nonnegativity is used. The baseline
itself has positive margins and attains equality, so the bound is sharp.

For any positive margins use [the double-cut proof](transport-double-cuts.md)'s complete constructor with p=4,N=5:

 lambda=(M+R2,M+R3,M+R4,C1,C2,C3,C4,C5),
 mu=(M,M,M,C2,C3,C4,C5), nu=(M,R2,R3,R4).

All boundaries are balanced integral partitions; outer length 8 is positive,
so actual ordinary rank for THIS displayed constructor is 8. The saturated
transportation dimension is 12. The inherited full character/count bridge,
not a selected face, proves c^(t lambda)_(t mu, t nu)=F_{r,c}(t) for all t>=0.
At the baseline the bare triple is

 lambda=(8,7,6,5,4,3,2,1), mu=(5,5,5,4,3,2,1), nu=(5,3,2,1).

Outer size 36 equals 25+11. It lies outside the original size 30 box.
No minimal ordinary rank among ALL possible alternative realizations is claimed.

Combining the inherited min(p,N)<=3 theorem, the N=4 theorem, transposition,
and (1), every positive transportation fiber whose displayed constructor has
rank<=8 has positive c1 (p=1 or N=1 is a point with c1=0).
The next unprotected shapes under this constructor are 4-by-6,5-by-5,6-by-4,
all rank 9, with degrees 15,16,15. Generic rank 8 LR c1 positivity remains unresolved.

## 4. A different complete counting challenge

For the baseline, delete the major row and let

 g_t(x,y,z)=sum_{a,b,c>=0,a+b+c<=t}x^a y^b z^c.

Every minor-row table is counted exactly by [x^t y^t z^t]g_t^5; the missing
entry of each column is t-a-b-c, hence nonnegative, and its major row sums to 2t.
This is a bijection, not an A3 assignment formula. Degree 12 is known from the
positive-margin transportation geometry before any reconstruction.

The new exact counter packs coefficients with coordinate radix 2t+1 and bit
digit width exceeding log2(binom(t+3,3)^5). After EACH multiplication it deletes
monomials with any exponent>t, since they cannot reach the target later. Both
factors have exponents<=t, so their product has exponents<=2t and no coordinate
alias in this radix. All coefficients are bounded by the total number of choices
binom(t+3,3)^5, so no digit carries occur. Thus it uses exact integer arithmetic.

TRANSPORT-OUTPUT-V02.json retains counts at t=0..14, all 13 ordinary coefficients,
and the two untouched holdouts t=13,14. The full vector reconstructed from 0..12 is

 (1,325/72,328081/33264,5005039/362880,29441411/2177280,
  399515/41472,1257551/248832,44951/23040,1587499/2903040,
  31375/290304,24827/1741824,233/207360,547/13685760).

All 13 coefficients are positive, and c1 independently agrees with (1).
The holdouts are 6,652,891,350 and 14,228,589,110. No direct LR count was performed
for this comparison; the whole LR identification is via the complete inherited bridge.
This check has combinatorial-model independence from the A3 jet calculation,
but both use CPython integers/Fraction, not independent arithmetic engines.

The first packed implementation used a much larger single power without
intermediate coordinate truncation. It timed out at 25 seconds and preserved no
count result. Its measured time remains recorded. The materially
repaired representation completed in under one observed second;
its partial counts are saved at every node. No result from the timeout is used.

## 5. Limits and the unresolved vanishing statement

The all-p,N positive core is now proved, but complete all-N four-row vanishing
of E_{>=3} is not. A general theorem would require a symbolic divisibility or order-of-vanishing
argument for all n1>0 three-/four-class A3 systems at their exact delta.
If individual vanishing fails, the aggregate E_{>=3} remains the relevant
quantity. A positive core does not by itself prove
whole transportation c1. The Birkhoff source comparisons in [the double-cut proof](transport-double-cuts.md) are
regressions of a broader conjecture, not an all-rank theorem.
