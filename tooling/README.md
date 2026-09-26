# Exact tools for LR and related lattice counts

This standalone Python library evaluates proved LR families, transportation
tables, skew tableaux, invariant multiplicities and several related lattice
models. The current additions are the complete principal rank-six split sector,
the clipped rank-eight family, abstract two-width bundles and general rectangular
matrix invariant counts. Every API keeps its mathematical domain explicit.

For the 25 September 2026 all-size result, start with the separate
[whole-rank-six verification module](whole_rank_six/README.md) and
[theorem page](../results/rank-six-positivity/README.md). Its finite original
normal fields, saturated-lattice checks and retained-support proof have a
different scope from the standalone c4/c5 module below. The generic Python
API commands here are not a replay of the new theorem.

The Python API and the following commands use Python 3.11+ and its standard
library, with no network or original research checkout. The separate native
modules below state their compiler/library requirements. From the repository root:

```sh
python3 -B tooling/examples/current_apis.py
python3 -B tooling/check_current.py
python3 -B tooling/check.py
```

The first command prints small examples. The second runs only the new small
interface and synthetic-model controls. The third is the preserved earlier
75-check suite. For the additional maintained research controls and exact
recorded rank-eight certificate consistency, use:

```sh
python3 -B tooling/check_current.py --research-controls
python3 -B tooling/check_rank8_data.py
```

These commands print results without writing files. Recorded-data consistency
does not constitute a fresh independent LR count. The complete counter and
verification distribution for the finite box are separate from these APIs.

For a notebook or script, add `tooling/` to `PYTHONPATH`:

```python
from slr_ehrhart import rank6_split_count, rank8_clipped_polynomial
from slr_ehrhart import rectangular_matrix_invariant_count

lam = (9, 8, 6, 4, 2, 1)
mu = nu = (5, 4, 3, 2, 1)
assert rank6_split_count(lam, mu, nu) == 16
coefficients = rank8_clipped_polynomial(1, 2)  # 22 exact Fractions.
assert rectangular_matrix_invariant_count(2, 3, 3, 1) == 20
```

## Choose a mathematical object

All ordinary triples use lambda outer; padding and inner symmetry have their
documented meanings. Ferrers conjugation is never an implicit normalization.
Polynomial vectors contain exact `Fraction` values in ordinary degree order,
low to high. Counts are integers. A refused domain or exhausted work limit is
not count zero.

| API | Input and output | Exact scope and degree |
| --- | --- | --- |
| `rank6_split_parameters/count/polynomial` | Bare ordinary triple, optional stretch; checked parameters, scalar or full vector | Rank at most six; all 51 parent minima checked. Degree 10 when `S>0`; the `S=0` product has its actual lower degree. [Contract](proofs/rank6-split.md) |
| `rank8_clipped_boundary/count/polynomial` | Integers `0<=M<=S<=2M`; full ordinary boundary, scalar or full vector | Degree 21 and all coefficients positive for `M>0`; the origin is a point. Evaluates the full fixed certificate, with no interpolation at runtime. [Contract](proofs/rank8-clipped.md) |
| `two_width_count/polynomial` | Two equal-length nonnegative gain vectors, total and offsets | The complete abstract composition bundle with two independent intervals; degree at most `len(left)+1`, with trailing zero coefficients trimmed. LR use needs its own whole-object map. [Contract](proofs/two-widths.md) |
| `cdagger_parameters/count/polynomial`, `verify_cdagger_certificate` | Bare triple or replay of the fixed full-hive certificate | Complete sufficient Cdagger domain, maximum trimmed rank six; all 553 domain rows and 36 implications. Refuses outside inputs. [Contract](proofs/cdagger.md) |
| `strip_count/polynomial` | Group sizes and `T,B,C,D`; full interval/simplex count | `h>=0`, `q1,q2>=1`, nonnegative parameters and `T<=B+C+D`. [Contract](proofs/positive-strip.md) |
| `transport_count`, `transport_to_lr` | Balanced labeled nonnegative margins; table count or whole-family LR triple | Constructor needs nonempty margin vectors; the scalar counter does not return a degree. [Contract](proofs/transport.md) |
| `minkowski_obstruction` | Two labeled margin pairs; an opposite-sign cut or `None` | Complete transportation criterion; arbitrary hives need a separate argument. |
| `segment_quotient_count/evaluate/geometry` | Exterior caps; count, signed-dilation value or degree/codegree | The complete cap-and-slack polytope. Its relation to a particular LR parent's quotient needs that parent's Minkowski premise. |
| `skew_tableau_count` | Skew shape, ordered content and stretch; scalar SSYT count | Exact horizontal-strip chains, typed work limits, scalar `t=0` convention. No full-vector/degree claim. [Contract](proofs/skew-count.md) |
| `skew_content_to_lr`, `capped_matrix_to_lr` | Skew shape/content or positive matrix caps; whole-family ordinary LR construction | Complete real polytopes and integer lattices under the stated conventions. [Contract](proofs/skew-lift.md) |
| `matrix_invariant_count`, `matrix_invariants_to_lr` | Square matrix size, multiplicity and grade; scalar or whole-family construction | Scalar entry degree `n*t`; size/grade symmetry belongs to the scalar, while the constructor retains the original size. [Contract](proofs/matrix-invariants.md) |
| `rectangular_matrix_invariant_count` | Positive `p,q,m` and nonnegative `t`; scalar for `m` labeled `p×q` matrices | Entry degree `lcm(p,q)*t`. General rectangular Weyl count; no general rectangular LR constructor or polynomial/degree assertion. [Contract](proofs/rectangular-matrix-invariants.md) |
| `flow_support_certificate`, `verify_flow_support_certificate` | Unique interval edges and cut totals | Complete acyclic interval-flow feasibility, active edges and degree witnesses; LR use needs a separate count identity. [Contract](proofs/flow-support.md) |
| `plan_support` | Complete summand direction spans | Necessary monomial support given the caller's common-type Minkowski and polynomial premises; allowed support is not actual support. |

The new numerical parameters require exact Python integers: booleans and
numeric coercions are rejected. Specialized LR families are sufficient domains;
their APIs do not classify all triples of the same rank. Abstract two-width
bundles can have negative ordinary coefficients without being LR counterexamples.

Matrix and skew counts can grow expensive. Their explicit state/transition
limits raise typed exceptions with statistics and no partial count. Those limits
do not promise a wall-clock or memory bound. No general speedup is claimed.
The optional `slr_ehrhart.hive` module builds inequalities with the standard
library; its polyhedron/dimension hooks require separately installed Sage.

## Complete three-letter LR families

[three_letter_certificates/README.md](three_letter_certificates/README.md)
reconstructs every original normal subset, full image lattice, exact BV
constant and rational field for the entire rank<=6 family with one inner
partition of length<=3. The four q3–q6 fields give a common face-volume
margin of 1/100000000. Python, C++17 and GMP are required; all inputs are
included and no private checkout or LP solver is needed. The companion
model, interior and complete successive-overlap formulas retain their full
original-domain and zero-boundary contracts.

## Complete transportation and three-row coefficients

For the strongest current positivity scopes, use the separate
[4×5 transportation verifier](../results/transport-four-by-five/README.md)
and [five-capacity verifier](../results/five-capacity/README.md). They include
all nonnegative parameter boundaries and actual degree drops. The first has a
separate numerical companion; the second is a small standard-library replay.
`transport_count` and `transport_to_lr` already accept 4×5 margins, while
`capped_polynomial` already accepts five capacities. The `transport_polynomial`
API below still accepts at most three rows; its computational domain is separate
from the stronger theorem.

[transport_certificates/README.md](transport_certificates/README.md) reconstructs the entire all-margin 3-by-5 transportation and four-capacity LR positivity proof with Python's standard library. Its three exact fields occupy about 58 KB. An optional C++/GMP command independently checks every local constant; complete rosters, original lattices and failure limits are explicit.

[three_row_coefficients/README.md](three_row_coefficients/README.md) computes full exact coefficient vectors for three-row transportation, coupled capacities and complete affine Schur/Jacobi-Trudi families. It retains original offsets and signed terms. The APIs have explicit assignment/permutation/degree refusals and independent unsigned count controls; their existence does not prove positivity outside the stated theorem domains.

## Complete rank-six coefficient certificates

[rank6_certificates/README.md](rank6_certificates/README.md) supplies a standalone
complete verifier for the universal rank-six c4/c5 fields. It reconstructs
every local value and the complete geometry, lattice, type and incidence
structure, then checks all rational inequalities. Its 44.8 MB dataset contains
all required finite inputs. The full fresh-export replay took about 10.4 minutes
on the recorded host. This optional module requires a C++17 compiler and GMP;
its exact scope and failure controls are explicit. The subsequent
whole-rank-six module supplies separate evidence for the then-open c1/c2/c3
complement.

## Structural normal and mask certificates

[structural_certificates/README.md](structural_certificates/README.md)
provides source-identical normal-atlas and P06/P07/P08 checkers, a manifest for
the separate data ZIP, a restorer and a resumable reader. The finite scopes
are the ambient `c_(D_n-4)` argument for ranks 6 through 12 and the selected
four- and five-coordinate boundary criteria. The accepted source-identical
campaign run completed four joins through 664 children in a 572.497-second
report span. The final public reader separately completed all 664 children and four
finite joins in 467.749 seconds; every child and owned process group exited.

The independent F025 forcing-table check has passed all 294,912 rank-six and
rank-seven records, but its [public sibling guide](structural_certificates/f025/README.md)
documents the completed original row-order check. The normal/mask reader consumes hash-pinned forcing
tables and does not replace that separate finite check. These forcing tables
supply sound dimension upper bounds; they are not a new universal closure theorem or a generic LR counter.
The [family count guide](../results/structural-positivity/replay/FRESH-COUNTS.md)
separately regenerates the gap-three and rank-ten transportation premises.

## Optional complete H-system counter

[cpp/README.md](cpp/README.md) supplies the unchanged reviewed C++ integer
counter, a small control route and its input protocol. It needs a C++17
GCC/Clang-compatible compiler with checked `__int128` arithmetic, and needs no
Boost or GMP. It counts every supplied inequality inside a caller-proved finite
box; it does not prove the chart, lattice, dimension, interior interpretation or
coordinate bounds. Partial and refused results remain explicit.

## Sources and prior measurements

Additional exact structural interfaces and proof checks are organized by
result: [five-height original hives](../results/five-height-hives/README.md),
[layered triangle families](../results/layered-triangle/README.md),
[gap caps](../results/gap-cap/README.md), and
[linear-coefficient geometry](../results/linear-coefficient-geometry/README.md).
The [closure and witness API](whole_rank_six/closure/README.md) is a small
entry point to the new rank-six geometry, with no large data download.

[PROOFS.md](PROOFS.md) collects the contracts.
[CURRENT-SOURCES.md](CURRENT-SOURCES.md) explains the current additions and
source projections; [SOURCE-LICENSES.md](SOURCE-LICENSES.md) explains
implementation provenance and AI-assistance account.

The old examples, 75-check driver, tests, benchmarks and source notices remain.
[The prior README](history/previous-tooling/README.md) records their earlier
scope. [BENCHMARKS.md](BENCHMARKS.md) and frozen measurement JSON remain dated
evidence, not performance claims about every new API. Benchmark execution is
optional; the default panel remains the original seventeen inputs.

```sh
python3 -B tooling/examples/quickstart.py
python3 -B tooling/benchmarks/compare.py --case transport-repeated8x8
```
