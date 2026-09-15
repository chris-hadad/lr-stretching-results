# Whole three-letter LR positivity through rank six

**Every ordinary coefficient is nonnegative when the three LR partitions have
at most six parts and one inner partition has at most three parts.** For a
feasible family, every coefficient through its actual degree is strictly
positive. There is no area bound, genericity condition or excluded parameter
wall. Infeasible families have the zero polynomial.

With lambda outer, this concerns the entire polynomial

    P(t)=c^(t lambda)_(t mu,t nu), len(lambda)<=6, len(nu)<=3,

and its image under inner symmetry. It closes the complete three-letter
slice at the first unresolved ordinary rank. Whole ordinary rank six outside
this slice, and unrestricted King-Tollu-Toumazet positivity, remain open.

The [complete proof](../../tooling/three_letter_certificates/PROOF.md) starts
from a [full row-letter model](../../tooling/three_letter_certificates/MODEL.md)
with seven original integer coordinates. Four exact correction fields give
the bound

    [t^k] P(t) >= 1/100000000 * sum_(actual k-faces F) vol_Z(F),
                                                     1<=k<=7,

in that model's saturated lattice. Actual degree can be smaller than seven.
Normalized volumes do not include a factorial. This is a uniform whole-family
certificate, not a fit to sampled boundary data.

## How the proof is checked

The [portable verifier](../../tooling/three_letter_certificates/README.md)
reconstructs the full original normal populations, their image lattices and
metrics, every exact local constant, and every rational field inequality.
It needs no private research checkout, linear-program solver or raw provider
return. The fields themselves use only a few megabytes when compressed.

| Exact population | Count |
| --- | --- |
| Original normal subsets | 1,149,016 |
| Independent / dependent subsets | 665,057 / 483,959 |
| Complete image-lattice and metric types | 395,657 |
| Original rows checked by the four fields | 664,539 |

Two independently organized exact implementations agree on every local
constant. All original higher-index lattices are retained, up to index eight.
The earlier universal rank-six c4/c5 theorem remains separately available;
this new chart has its own small c4 field, making this certificate
self-contained. See [verification evidence](VERIFICATION.json) and the [relocated replay, runtime controls and measured costs](TOOLING-VERIFICATION.json).

## Interior and complete count formulas

The [interior translation](../../tooling/three_letter_certificates/INTERIOR.md)
is valid for every full-dimensional n-row, three-letter model with n>=4.
It gives exact shifted LR counts for the entire interior, including empty
interiors. Its distinguished family has a proved odd-center symmetry that
reduces the determining space while preserving unused positive holdouts.

The [successive-overlap identity](../../tooling/three_letter_certificates/HESSENBERG.md)
collects the complete Jacobi-Trudi determinant into block multisets, retaining
every affine offset. Removing those offsets creates false negative ordinary
coefficients in explicit examples. Those incorrect expressions are controls,
not LR counterexamples.

For example, the entire triple

    lambda=(13,11,9,7,5,3), mu=(10,8,6,4,2,0), nu=(8,6,4)

has degree seven and polynomial

    1 + (236/35)t + (4061/180)t^2 + (17447/360)t^3
      + (5033/72)t^4 + (24299/360)t^5
      + (14233/360)t^6 + (14233/1260)t^7.

The whole-hive Ehrhart series, independent tableau/lrcalc counts and full
symbolic formula agree. [Complete examples](EXAMPLES.json) include lower
ranks, another successive-overlap family, diagonal and empty boundaries.

Every whole stabilized saturated quotient along a positive-dimensional
direction inside the admitted rank-six family is also positive through
actual quotient degree. Its initial and intermediate parents are covered
by the family theorem. The proof retains complete fibers and the quotient
lattice; it assigns no ordinary LR rank to the quotient.

## Sources and limits

The LR rule, LR triangles, polynomiality, saturation and BV valuation are
classical inputs. Alper Ferudun's rank-five theorem and correction approach,
and the earlier complete normal-cycle work, are credited foundations.
[The source comparison](NOVELTY.md) records the bounded novelty assessment.
This result does not assert worldwide priority or external expert acceptance.
See the repository's [AI-assistance statement](../../AI-ASSISTANCE.md) for the
research process and its limitations.
