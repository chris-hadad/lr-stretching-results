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
