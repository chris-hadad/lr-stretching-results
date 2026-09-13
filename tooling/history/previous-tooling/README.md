# Exact tools for LR and related lattice counts

These Python tools make several proved count models directly usable. They
include a fast bare-triple counter on one explicit rank-six sector, general
admissible strip counts, transportation and segment-quotient counters,
whole-polytope LR constructions, checkable support certificates, and a general exact skew-tableau counter.

Use Python 3.11+ and its standard library. No installation, network access or
original research checkout is needed for the commands below. From the repository
root:

```sh
python3 -B tooling/examples/quickstart.py
python3 -B tooling/check.py
python3 -B tooling/benchmarks/compare.py --case transport-repeated8x8
```

The example and checks print their results without writing output files.
The benchmark launches one bounded Python child at a time and prints JSON;
its default is the seventeen-input count panel with one cold repetition.

For a notebook or script, put `tooling/` on `PYTHONPATH` and import the APIs:

```python
from slr_ehrhart import cdagger_count, cdagger_polynomial, transport_count

lam = [43, 38, 33, 20, 12, 6]
mu = [22, 17, 16, 12, 6]
nu = [26, 21, 16, 12, 4]
assert cdagger_count(lam, mu, nu) == 4590
coefficients = cdagger_polynomial(lam, mu, nu)  # Eleven exact Fractions.
assert transport_count([1, 1, 1, 1], [1, 1, 1, 1]) == 24
```

## Choose a supported mathematical object

| API | Input and result | Required boundary |
| --- | --- | --- |
| `cdagger_count`, `cdagger_polynomial` | An ordinary triple, lambda outer; a scalar count or all ordinary coefficients | Complete Cdagger domain checked, maximum trimmed rank six; outside inputs raise `OutsideCdaggerError` |
| `cdagger_parameters`, `verify_cdagger_certificate` | Exact strip parameters, or replay of the fixed full-hive certificate | All 553 domain rows, the integer chart and all 36 implication identities |
| `skew_tableau_count` | A skew shape, ordered content and stretch; exact SSYT/Kostka count | Ordinary LR use needs the proved buffer lift; typed work limits, scalar t=0 convention and no degree/full-vector claim |
| `strip_count`, `strip_polynomial` | Group sizes and `T,B,C,D`; full admissible interval/simplex counts | `h>=0`, `q1,q2>=1`, nonnegative parameters and `T<=B+C+D` |
| `transport_count`, `transport_to_lr` | Balanced labeled margins; exact table count or an entire-family LR triple | Nonnegative margins; the constructor requires nonempty margin vectors |
| `minkowski_obstruction` | Two labeled margin pairs; an opposite-sign cut or `None` | The complete transportation criterion, not an arbitrary-hive criterion |
| `segment_quotient_count`, `segment_quotient_evaluate`, `segment_quotient_geometry` | Exterior row/column caps; weighted count, signed-dilation value, degree/codegree | Interpreting it as a specified LR parent's quotient additionally needs that parent's Minkowski premise |
| `skew_content_to_lr`, `capped_matrix_to_lr` | A skew shape/content or positive matrix caps; whole-family LR construction | The entire real polytope and integer lattice, with the stated input conventions |
| `flow_support_certificate`, `verify_flow_support_certificate` | Unique interval edges and integer cut totals; exact feasibility, active edges and degree witnesses | An acyclic interval-flow fiber; LR use requires a separate whole-object/count identity |
| `plan_support` | Complete summand direction spans; necessary multivariate monomial support | Caller supplies the common-type Minkowski and polynomial premises; allowed support is not actual coefficient support |
| `matrix_invariant_count`, `matrix_invariants_to_lr` | Matrix size, multiplicity and grade; exact invariant count or whole-family LR construction | Specialized square-matrix family; optional explicit state/transition limits |

All counts use exact integers; polynomial coefficients are exact `Fraction`
objects in ordinary degree order, low to high. APIs retain their documented
strict input checks. A failed domain gate is not count zero. A specialized
constructor does not invert arbitrary LR triples, and none of these tools
claims complete rank-six, original-box or all-rank positivity.

The optional `slr_ehrhart.hive` module constructs conventional hive inequalities
with the standard library. Its polyhedron/dimension functions require Sage,
which this snapshot does not install; the examples and checks need no Sage.

## Performance and provenance

The transport counter aggregates equal-cap allocation orbits with their exact
labeled multiplicities and closes the last rows by coefficient formulas.
The strip counter evaluates integer binomial moments instead of enumerating
compositions. [BENCHMARKS.md](../../BENCHMARKS.md) reports same-input measurements,
including startup costs and cases with little practical gain.

[PROOFS.md](PROOFS.md) states the mathematical contracts and their limits.
[SOURCE-LICENSES.md](../../SOURCE-LICENSES.md) explains source provenance, AI assistance
and the existing private licensing boundary. The repository's `SOURCE-MAP.json`
pins this versioned projection to its maintained sources. Historical benchmark
oracles remain frozen comparison code; the maintained algorithms have one source
home in the research package.

The skew counter makes the changed rank-thirteen family's previously expensive
small-dilation counts practical through partial-row aggregation. For example:

```python
from slr_ehrhart import skew_tableau_count
assert skew_tableau_count([30, 26, 3, 2, 1], [2, 1],
                          [14, 14, 14, 12, 1, 1, 1, 1, 1], 2) == 12562151868
```

Run `python3 -B tooling/benchmarks/compare.py --case skew-r11-t3` to compare
its three complete counting algorithms. Native-source Python methods in this
benchmark are not fresh LR-engine runs.
