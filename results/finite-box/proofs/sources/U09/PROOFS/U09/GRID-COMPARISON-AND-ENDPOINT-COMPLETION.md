# A measured grid decision and exact complementary endpoint identity

The two grid designs apply to the same complete degree-ten polynomial and the same genuine lattice. The balanced grid is [-5,5], with observed P1,...,P5 and I1,...,I4, leaving I5 unknown. The interior-biased grid [-6,4] observes P1,...,P4 and I1,...,I5, leaving I6 unknown. Both have nine numerical premises and an independently proved complete degree-at-most-ten identity space. Both retain a negative c8 unknown kernel and therefore an initial finite upper bound under the precise normal theorem. Neither is automatically cheaper as a complete certificate.

## Same-input comparison

The frozen 256 targets were selected without count or sign information from the exact 18424-target roster. Every target's actual ten-dimensional geometry is checked separately. All 256 targets are ordinary rank seven, so no target-level ambient-rank-six c7 protection is used. This does not exclude a different recorded whole-count equivalence to a rank-six realization; no such additional shortcut is needed or claimed in this comparison.

The balanced direct computation uses 24.701376702 seconds: its hive/row numerical wrappers account for 7.891004229/11.711607644 seconds, with the remainder including fresh geometry, map and formal-cover work. Its initial protected interval closes 152 targets; primary covers close 103 more. One secondary formal repair takes 2.072501260 seconds and closes the last target. Independent primary and repair audits check all 256.

The biased direct computation takes 22.094090231 seconds. Numerical wrapper time is substantially smaller,3.330290689/2.754430805 seconds, but the primary formal-bound work rises from 2.215977637 to 13.061504949 seconds. The initial interval closes 146 and primary covers 76, leaving 34. A further 29.837487213-second bounded repair closes 33 of those 34; one direct-certificate exception remains. Its independent audit passes at precisely that scope. These are finite measurements with distinct components, not host-independent predictions. The balanced method was selected before the full computation because it finished the entire pilot with less complete certificate work, not because its scalar counting stage was fastest.

The separately verified full-vector baseline determines all 256 entire polynomials, preserves each vector before comparison and uses unchanged positive check sites 6 and 7. There are 213 distinct vectors and 2816 strictly positive ordinary coefficient occurrences. Forty-one originally missing/refused row check sites are repaired by exact inner commutativity; the other two need a newly controlled finite state/work cap at the same grade 7. All 43 original failed/uncomputed-site dispositions and every failed numerical attempt remain. This independent baseline proves the biased method's remaining parent positive, but does not retrospectively turn an insufficient biased direct bound into a complete direct certificate.

## A concrete remaining biased-grid exception

For original-area-thirty target 372590,

    lambda=(8,7,5,4,3,2,1),
    mu=(5,4,2,2),  nu=(6,5,3,2,1),

The independent complete polynomial has I5=16392, I6=155617 and P5=1636888. The balanced certificate succeeds while the bounded biased certificate remains insufficient. Complete old and repaired intervals, required sign thresholds, full coefficients and the exact data source are in DATA/U09/grid-diagnosis-v2/DIAGNOSIS.json. These numbers are derived from the already independently checked full vector, not fresh unrecorded scalar calls. No negative ordinary coefficient is present.

The diagnosis's first reader attempted to retain every large proof body in memory and refused its 256 MiB reservation. Its fresh streaming revision discards only in-memory proof copies irrelevant to the diagnosis; all original proof files remain untouched. The revision completes within the same reservation. The failed attempt and its timing remain part of the comparison.

## Exact endpoint completion in even degree

Let d=2q and let P have degree at most d. The d+2 consecutive values on [-q-1,q] satisfy the zero (d+1)-st finite difference. Thus

    P(q)-P(-q-1)
      = -sum(k=1..d) (-1)^(d+1-k) binom(d+1,k) P(-q-1+k).

For an actual even-dimensional entire period-one hive polynomial, reciprocity gives P(-q-1)=I(q+1), while every value in the displayed sum is a known biased-grid premise (including P0=1). Define the exact integer right-hand side as Delta. Then

    P(q)-I(q+1)=Delta.

Consequently a complete closed-count enclosure L<=P(q)<=H transports to

    L-Delta <= I(q+1) <= H-Delta,

and conversely. No estimate is silently made exact. A complete proof for either object must retain its whole lattice and all constraints; the identity alone provides no numerical enclosure.

For target 372590, Delta=1481271. This identity and all 45 monomial actions in even degrees 4,6,8,10,12 are checked in the diagnosis. It suggests a concrete additional cost-adaptive repair: after the cheaper biased counts, compare a complete closed-endpoint enclosure with an interior-endpoint enclosure, translate either by Delta, and retain the less expensive valid proof. No such whole-population enclosure comparison is executed here, and no new coverage is assigned to this proposal. Generic finite differences are inherited; the scoped application is the two-object certificate option, not a priority claim.
