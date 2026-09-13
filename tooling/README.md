# Exact tools for LR and related lattice counts

This standalone Python library evaluates proved LR families, transportation
tables, skew tableaux, invariant multiplicities and several related lattice
models. The current additions are the complete principal rank-six split sector,
the clipped rank-eight family, abstract two-width bundles and general rectangular
matrix invariant counts. Every API keeps its mathematical domain explicit.

Use Python 3.11+ and its standard library. No installation, network or original
research checkout is needed. From the repository root:

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

## Optional complete H-system counter

[cpp/README.md](cpp/README.md) supplies the unchanged reviewed C++ integer
counter, a small control route and its input protocol. It needs a C++17
GCC/Clang-compatible compiler with checked `__int128` arithmetic, and needs no
Boost or GMP. It counts every supplied inequality inside a caller-proved finite
box; it does not prove the chart, lattice, dimension, interior interpretation or
coordinate bounds. Partial and refused results remain explicit.

## Sources and prior measurements

[PROOFS.md](PROOFS.md) collects the contracts.
[CURRENT-SOURCES.md](CURRENT-SOURCES.md) explains the current additions and
source projections; [SOURCE-LICENSES.md](SOURCE-LICENSES.md) preserves the prior
source, model-assistance and owner licensing notice. No license decision is
made by this tooling refresh.

The old examples, 75-check driver, tests, benchmarks and source notices remain.
[The prior README](history/previous-tooling/README.md) records their earlier
scope. [BENCHMARKS.md](BENCHMARKS.md) and frozen measurement JSON remain dated
evidence, not performance claims about every new API. Benchmark execution is
optional; the default panel remains the original seventeen inputs.

```sh
python3 -B tooling/examples/quickstart.py
python3 -B tooling/benchmarks/compare.py --case transport-repeated8x8
```
