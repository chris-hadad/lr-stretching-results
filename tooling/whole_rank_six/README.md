# Verify the rank-six theorem

Start with the [mathematical proof](../../results/rank-six-positivity/PROOF.md)
and [verification map](../../results/rank-six-positivity/VERIFYING.md). Choose
the depth of computation you want. All commands run locally and install nothing.

| Route | What it checks | Prerequisites and observed cost |
| --- | --- | --- |
| [Closure calculus and witnesses](closure/README.md) | Exact closure for every physical row set; constructive legal boundaries and edges | Python 3.11+, standard library; about 5 seconds |
| Original cone and boundary examples | All 45 rhombi, 166 rays and six isometries; edge, padded interval, empty and point examples | Python 3.11+, standard library; about 3.5 seconds |
| Small coefficient components | Complete c6–c9 finite premises, with independent scalar algorithms | Python, C++17, GMP; about 96 seconds |
| Complete supplied-scalar fields | Geometry, original primitive action and exact inequalities for c1–c5 | Versioned numerical data plus Python/C++17/GMP; tens of minutes |
| [Complete scalar regeneration](scalars/README.md) and [lower chain](lower/README.md) | Every analytic scalar premise and its complete lower dependencies | Same data and tools; substantial computation, with measured costs below |

Times are measurements on an Apple Silicon host with 24 GiB RAM, sometimes
under concurrent load. They are not promises for another machine. The small
commands each certify their stated component; the whole theorem joins all
components to the analytic argument.

## Begin without downloading numerical archives

Run from the repository root, choosing fresh output directories with existing
parents, outside the source tree:

```sh
python3 -B tooling/whole_rank_six/geometry.py --out /path/to/new-geometry-run
python3 -B tooling/whole_rank_six/verify.py small --out /path/to/new-small-run
```

The first needs only Python. The second also requires an installed C++17
compiler (`c++`) and GMP development headers/libraries. Use
`--gmp-prefix /path/to/prefix` and `--cxx /path/to/compiler` if needed.
An existing standard Homebrew GMP installation is detected on Apple Silicon.
The process wrappers target macOS or Linux and use POSIX process groups; the
observed publication executions used macOS on Apple Silicon. Use unoptimized
Python: do not set `PYTHONOPTIMIZE` or pass `-O`.

The small coefficient command enumerates every one-, two- and three-normal
support using two exact scalar algorithms, then all 102,297 independent
four-normal supports. It checks 381 saturated kernels and 14,067 primitive
incidences in the sixth-coefficient field. Exact minima are `1/2`, `1/9`,
`1/144`, and `164999999111/491400000000000`. Dependent complements are included.
`PASS_COMPLETE_SMALL_COMPONENTS` covers c6–c9; c10 is the volume term.

## Restore the complete numerical data

The version is **rank-six-2026-09-25-v1**. Its nine files
`rank-six-data-01.tar.gz` through `rank-six-data-09.tar.gz` contain 1,842
mathematical inputs. [DATA-ASSETS.json](DATA-ASSETS.json) supplies every archive
and member size and SHA-256. Total download is **4,985,772,426 bytes**; the
restored tree is **14,054,651,154 bytes**. Allow at least 30 GB free for archives,
restored inputs and ordinary checking outputs; optional producer regeneration
needs additional space. These assets accompany the versioned repository release
on its [releases page](https://github.com/chris-hadad/lr-stretching-results/releases).
The old finite-box archives and the separate 4×5 companion are different datasets.

Download all nine archives into one directory, then:

```sh
python3 -B tooling/whole_rank_six/restore.py \
  --archives /path/to/downloaded-archives --out /path/to/rank-six-data
```

The destination must be fresh and outside the source/archive trees. The
restorer checks every archive before writing output, then checks every member.
Missing, duplicate, unsafe, changed or incomplete data cannot yield a complete
restoration. The publication round trip restored every member and independently
rehashed it. Restoration alone establishes byte identity, not the theorem.

## Check all coefficient fields

Set these two paths in your shell. The work directory must have an existing
parent and must not already exist:

```sh
SLR_DATA=/path/to/rank-six-data
SLR_WORK=/path/to/new-rank-six-check
mkdir "$SLR_WORK"
python3 -B tooling/whole_rank_six/c1.py --data "$SLR_DATA/c1" --out "$SLR_WORK/c1"
python3 -B tooling/whole_rank_six/lower/replay.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower" --phase c3-core
python3 -B tooling/whole_rank_six/lower/replay.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower" --phase c2-field
python3 -B tooling/rank6_certificates/verify.py --full --out "$SLR_WORK/c4-c5"
python3 -B tooling/whole_rank_six/verify.py small --out "$SLR_WORK/c6-c9"
```

The c1 command reconstructs the complete cone, every physical branch, the
original correction action and the full q7→q8→q9 domain/extension coverage.
Its finite sign domain has 13,325,662 retained orbit rows, within the complete
27,230,728-row roster. The new public c3 and c2 commands cover all 2,999,563
and 10,480,218 field rows respectively. The c4/c5 command includes complete
regeneration of its 333,769 local types. Each phase has a precise complete
receipt and retains its original-lattice interpretation.

## Regenerate the remaining scalar premises

Continue in the same `SLR_WORK/lower` directory, with phases in this order:

```sh
python3 -B tooling/whole_rank_six/lower/replay.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower" --phase c3-analytic
python3 -B tooling/whole_rank_six/lower/replay.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower" --phase h8-small
python3 -B tooling/whole_rank_six/lower/controls.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower"
python3 -B tooling/whole_rank_six/lower/replay.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower" --phase h8-full
python3 -B tooling/whole_rank_six/lower/q8_rhs_replay.py --asset-root "$SLR_DATA/lower" --output "$SLR_WORK/lower"
python3 -B tooling/whole_rank_six/scalars/replay.py --distribution "$SLR_DATA/c1" --lower-assets "$SLR_DATA/lower" --out "$SLR_WORK/scalars" --mode check-all --workers 1
```

The lower chain verifies all 1,988,979 q1–q7 types and their 4,706,329 jet slots,
then 19,271,753 additional level-ordered H8 slots, and all 6,958,562 q8
scalar types at two covectors. The last command authenticates all 8,947,541
lower cache entries and independently recomputes every q9 scalar in all 455
consecutive ranges. It includes each full image lattice and exceptional
finite-character correction. The [scalar guide](scalars/README.md) explains
parallelism, the optional more expensive producer mode and diagnostic-only runs.

Successful analytic child durations totaled about 24.5 minutes for c3 jets,
3.15 hours for H8, 2.20 hours for q8 and 20.66 hours for q9. These are sums of
elapsed child timers, not measured CPU time. The complete q9 stage took 3.49
wall hours with up to six children. Defaults are serial; account for other
applications before increasing concurrency. Full regeneration is deliberately
separate from the faster supplied-scalar field checks.

## Evidence and scope

[VERIFICATION.json](VERIFICATION.json) records complete scientific domains,
source bindings, fresh exports, data restoration and refusal controls. The
complete mathematical engines were replayed on isolated inputs. The final
portable lower wrapper additionally ran complete c3 core, complete c2 field,
small H8 levels, all six scientific controls and a diagnostic q8 shard from a
clean export. The final q9 parallel wrapper received actual interruption and
partial-result checks; its full 455-range computation is recorded under the
separate complete driver. Those implementation scopes are kept explicit.

The programs use bounded owned child groups and fresh output, and refuse
incomplete coverage. Preserve failed or interrupted work before diagnosing it.
The [formalization assessment](../../results/rank-six-positivity/FORMALIZATION.md)
states the remaining proof-assistant obligations. No human peer review or
kernel-checked whole theorem is asserted by these execution records.
