# Complete local-scalar verification

`check-all` authenticates every entry of the lower constant cache and
independently recomputes all **27,230,728** nine-normal local constants. It
checks all 455 consecutive ranges, with every original proper-subset lattice
and finite-character correction. Python 3.11+, a C++17 compiler and GMP are
required. The parallel driver supports macOS and Linux.

After restoring the [versioned mathematical data](../README.md), run from the
repository root, replacing the example paths with your own:

```sh
python3 -B tooling/whole_rank_six/scalars/replay.py \
  --distribution /path/to/rank-six-data/c1 \
  --lower-assets /path/to/rank-six-data/lower \
  --out /path/to/new-scalar-run \
  --mode check-all --workers 4
```

The output path must not exist and its parent must exist. Select 1–8 workers
to fit your available CPU and memory; one is the default. The parallel driver
requires 4 GiB of measured available host memory, bounds each child at 3 GiB
RSS and 600 seconds, and records partial work as incomplete after any failure.
It does not count workers in other applications. GMP can be supplied with
`--gmp-prefix /path/to/prefix`; `--cxx` selects the installed C++ compiler.
No installation or network access is performed.

This is the expensive part of the certificate. The complete publication run
recorded 20.66 aggregate child-hours and 3.49 elapsed hours with up to six
children. Aggregate elapsed timers are not measured CPU-hours, and another
host may differ substantially. Use
the [supplied-scalar field check](../README.md) first for a shorter geometric
and arithmetic inspection. Neither route substitutes for the mathematical
normal-cycle and realizability proof.

## Four deliberately different modes

| Mode | Complete scope |
| --- | --- |
| `cache` | Compare all 8,947,541 lower alpha values and all 8,947,541 derived W weights against their exact type, image-lattice and scalar sources |
| `check-all` | The complete cache check, then independent recomputation of every q9 scalar; the normal verification route |
| `full` | Optional serial regeneration of the cache, original q8 index and all q9 producer TSVs, followed by the independent checker; more expensive than required to check the finite premise |
| `diagnostic --range-index N` | One complete original range, with no whole-domain verification credit |

Every mode uses a fresh output directory. `INPUTS.json` lists exact relative
paths, sizes and SHA-256 values; source and input bytes are checked before and
after execution. The complete modes reject gaps, duplicates and missing tails.
Child commands, exit records and exact completed-range counts are retained.
The paired runtime stops only process groups created by this run and checks
their exit. A timeout, cancellation or resource refusal is never a pass.

## The mathematical join

The lower coefficient package must separately establish the analytic source
tables: all q1–q7 jets, the complete level-ordered H8 calculation, and all
6,958,562 q8 scalar types. This module reads those supplied tables but does
not prove their analytic validity merely by matching their hashes.

The cache check reconstructs each original Gram and image basis and verifies
its index, determinant and adjugate relation. It then checks alpha and
`W_k = alpha_k * index_k / (9-k)!` for every type. The q9 checker loads alpha,
solves the full adjugate and checks all 511 proper-subset terms and all
exceptional characters. The optional producer uses W and a different summation
organization. Both share the stated finite-group formula and exact arithmetic
primitives; their agreement is not a second proof of that formula.

Thus a successful result here remains conditional on the lower analytic
checks. The whole-theorem verification also needs complete support coverage,
the original corrected field action, and the other coefficient certificates.
The [main proof](../../../results/rank-six-positivity/PROOF.md) identifies those
joins explicitly.

The five C++ sources and their provenance are recorded in `SOURCE-MAP.json`.
The existing c1 and lower data trees contain every needed input; no private
research checkout, returned provider program or hidden numerical cache is
required. The `full` option needs about 4.2 GB of additional output for its
regenerated cache, index and TSVs. The checking modes keep only their binaries,
bounded logs and verification records.
