# Reproducing and checking the results

Choose a check by the mathematical question it answers. A file inventory,
an exact scalar count and a proof of every coefficient sign provide different
kinds of evidence.

## A first local run

Obtain a source snapshot at a specific Git commit. From its root, use Python
3.11 or later with assertions enabled:

```sh
python3 -B examples/sign_completion.py
python3 -B reproduce.py
```

The educational example verifies two universal quintic identities by expanding
each monomial and gives a worked example. Its simplex is an illustration, not
an additional LR result. The root command runs the five small established
modules described in their READMEs. Their exact checks and independence limits
are listed in [PROVENANCE.md](PROVENANCE.md). These programs install nothing.

For selected modern counters and geometric constructors:

```sh
python3 -B tooling/examples/current_apis.py
python3 -B tooling/check_current.py --research-controls
python3 -B tooling/check_rank8_data.py
```

See [the tool contracts](tooling/README.md) before using a specialized family
interface on a new triple. Agreement at selected scalar values does not supply
a degree bound or prove a whole polynomial. The rank-eight data check tests
the supplied complete certificate against recorded observations; it does not
freshly enumerate their independent LR counts.

The [structural module guide](results/structural-positivity/README.md) gives
the commands for its individual families. Each distinguishes newly performed
algebra from retained historical count observations.

## Complete three-letter rank-six certificate

The [three-letter module](tooling/three_letter_certificates/README.md) includes
all mathematical inputs and a full original-lattice reconstruction. It needs
Python 3.11+, C++17, GMP and the POSIX facilities named in its guide:

```sh
python3 -B tooling/three_letter_certificates/verify.py full --output /path/to/new-three-letter-run
python3 -B tooling/three_letter_certificates/controls.py --verified-output /path/to/new-three-letter-run --output /path/to/new-three-letter-controls
```

Use the module's `--gmp-prefix` option if headers and libraries are outside
the compiler's standard search path. A fresh relocated export has executed
the complete 1,149,016-subset / 395,657-value / 664,539-field-row check. The
[verification record](results/three-letter-rank-six/VERIFICATION.json) separates
that reproduction from the underlying theorem and independent count controls.
The controls exercise missing/corrupted input, the full image lattice,
Bernoulli and field omissions, and interruption of the actual outer CLI.
Neither command runs the finite box or an old rank-six coefficient census.

## Complete transportation and capped-family certificates

The [small whole-family module](tooling/transport_certificates/README.md) requires only Python 3.11+ for its complete proof replay:

```sh
python3 -B tooling/transport_certificates/verify.py --out /path/to/new-transport-check
PYTHONPATH=tooling python3 -B -m unittest three_row_coefficients.test_coefficients
python3 -B results/transport-capped/reproduce_examples.py
```

The first command rebuilds every original normal subset and local constant, and checks every complete rational inequality. The other commands independently test the full coefficient interfaces and reproduce the exact example vectors. The result page's [verification record](results/transport-capped/VERIFICATION.json) distinguishes source and fresh-export executions. Optional C++ comparison and corruption/interruption checks have their exact commands in the module guide. These checks do not rerun the finite box or imply a whole-rank theorem.

## Complete rank-six c4/c5 certificates

The [rank-six module](tooling/rank6_certificates/README.md) includes the full
44.8 MB compressed mathematical dataset and a complete fresh-reconstruction
command. It needs Python 3.11+, a C++17 compiler and GMP development libraries:

```sh
python3 -B tooling/rank6_certificates/verify.py --full --out /path/to/new-rank6-run
```

The full command was executed from an exact clean source export and returned
`PASS_COMPLETE_C4_C5_FINITE_CERTIFICATES`, including all original subsets,
lattice/type/kernel/matrix predicates, all local values and all rational
inequalities. [The record](results/rank-six-coefficients/VERIFICATION.json)
gives its exact counts and measured cost. `--quick` is a diagnostic prefix,
with an explicitly incomplete theorem verdict. This command does not rerun
the finite-box computation or prove the remaining rank-six coefficients.

## The finite-box proof

The [module instructions](results/finite-box/README.md) are the complete command
contract. Work from `results/finite-box/` with separate source, archive, data
and writable work directories.

| Stage | What a successful result establishes | What it does not establish |
|---|---|---|
| `verify.py extract` | All ten archives have the declared hashes; exactly 11,607 required files are extracted and checked | No count or coefficient sign |
| `verify.py inventory` | Required data presence and sizes, plus the configured source and metadata hashes | No full data-content recount or theorem check |
| `verify.py sample` | Fresh complete counts for representative records from each numerical regime | No exhaustive coverage |
| `verify.py full` | Regenerated predecessor census, geometry, algebra, bounds, counts and literal terminal composition when the final complete report is reached | No proof of the cited universal theorems, unrestricted KTT, or human peer review |

The ten unchanged finite-box data archives are distributed at
[finite-box-2026-09-12-v1](https://github.com/chris-hadad/lr-stretching-results/releases/tag/finite-box-2026-09-12-v1).
They contain 1,761,805,311 compressed bytes and 12,349,067,632 expanded bytes.
Full verification additionally produces large identity indexes and count
journals: allow at least 150 GB free. It uses Python and a C++17 compiler with
checked 128-bit arithmetic; the exported route needs neither Sage nor Normaliz.
Scientific children are serial and bounded at 120 seconds. Final metadata
assembly has its separately documented 600/660-second internal/process limits.

Use the exact source/data versions named in a run's configuration. A work
directory is bound to its original source, interpreter, compiler and parameters.
For an explicit call-limit stop, continue with the same command and directory.
A refusal, interrupted preparation, missing file or unresolved count is not a
completed proof. Preserve its output before diagnosing it. Changing inputs
requires a fresh work directory, not editing the old successful receipts.

## What has actually been executed?

[The exhaustive verification record](results/finite-box/REPLAY.json) binds a
completed clean-export replay through the individual controllers and explicit
final metadata assembly. It records 624,314 terminal requirements,
3,561,385 physical count sites across the required numerical regimes, and
3,936,015 original residual keys representing 4,360,228 obligations.
These populations overlap in purpose and are not added together as coverage.
The original rank-six/seven census has 651,229,702 identities.

That replay used 9,078.727385 numerical child seconds, including recorded earlier
attempts, plus predecessor, geometry, algebra, composition and metadata work.
It ran on an Apple Silicon host with 24 GiB RAM, Python 3.14.3 and Apple Clang 21.
This numerical timing is not a total runtime prediction for another machine.

The inventory and representative modes of the final convenience interface
were executed, and its composition/acceptance transitions received targeted
checks. **A fresh end-to-end execution of the full convenience command is not
claimed.** Its component replay and interface testing remain distinct evidence.
The [publication preparation record](PUBLICATION-CHECKS.md) records this
edition's additional tests without replacing those earlier executions.

## Versions, missing evidence and review

[SOURCE-MAP.json](SOURCE-MAP.json) and the module manifests bind included
mathematical sources. Historical absolute paths are provenance labels, not
files a recipient must possess. Every input the portable program requires
comes from the source snapshot and listed assets; the universal mathematical
premises are listed separately. Earlier operational journals are retained in
the research archive and are not silently imported into a fresh replay.

To report an objection, give the commit, module, exact triple or certificate
identity, command, result and mathematical premise in question. A short
counterexample to a reduction or a missing terminal identity can be more useful
than another large sample. [The reviewer guide](results/finite-box/REVIEWER-GUIDE.md)
suggests specific audit points.

The [September 13 source and offline bundles](https://github.com/chris-hadad/lr-stretching-results/releases/tag/research-edition-2026-09-13-v2)
contain the reader-facing proof collection and identify their exact source
commit. The numerical archives retain their original version and hashes.

The September 13 archives remain dated editions. The later rank-six coefficient and three-letter family
modules are included in the current Git source and is not added retroactively to
those archives. Results are shared incrementally at their verified scopes;
subsequent corrections and extensions retain identifiable prior versions.
