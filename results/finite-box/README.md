# The original FrontierMath box contains no counterexample

For partitions λ, μ and ν with λ outer, `|λ| = |μ| + |ν| <= 30`, and
maximum trimmed length at most seven, every ordinary coefficient of the
stretched Littlewood–Richardson polynomial is nonnegative. The campaign has
accepted the computer-assisted proof after independent mathematical and
computational checks. The unrestricted KTT conjecture and whole-rank positivity
for ranks six and seven remain open.

Start with the [research-note draft](../../papers/finite-box.md) for a connected
account. Read [the detailed proof](PROOF.md), [the audit map](REVIEWER-GUIDE.md), and
[the dependencies](DEPENDENCIES.md) first. The [verification record](REPLAY.json)
states exactly which exported computations were completed. A program success
message does not replace the named mathematical premises or external review.
Alper Ferudun's all-size rank-at-most-five theorem is a central dependency.
The [references](REFERENCES.bib) and [AI-assistance account](AI-ASSISTANCE.md)
identify prior contributions and how this campaign developed the result.

## Files and prerequisites

The repository contains the readable proof, original proof documents, independent
checkers, invocation adapters and exact source manifests. The ten data archives
listed in [DATA-ASSETS.json](DATA-ASSETS.json) contain all 11,607 required data
files: 1,761,805,311 compressed bytes and 12,349,067,632 expanded bytes. Obtain
all ten from the same [versioned release](https://github.com/chris-hadad/lr-stretching-results/releases/tag/finite-box-2026-09-12-v1).
The release also supplies a complete offline review kit. Private GitHub links
require repository access; an offline copy can be reviewed without GitHub.

Use Python 3.11 or later on a POSIX system, with assertions enabled, and an
installed C++17 compiler supporting checked 128-bit integer arithmetic and
the standard C++ library. The tested host and measured costs are recorded in
`REPLAY.json`. The commands install nothing and make no network requests.
Sage, Normaliz, Boost and GMP are not dependencies of this exported route.
Historical `.input` files are certificate source data, not commands to execute.

Use separate code, data and writable work directories. Full verification needs
substantial disk space for the exact identity index and fresh count journals;
allow at least 150 GB free before starting. A machine with 24 GB RAM was used.
Counting and individual terminal-check children run serially with 120-second
process deadlines. Final metadata assembly has a separate 600-second internal
allowance and a 660-second process deadline to authenticate the complete file
and identity union. It performs no new LR counts. An incomplete result,
overflow, deadline or work refusal supplies no count and cannot close a gate.

## Extract and check the inventory

From this directory, with the ten archives in an `assets` directory outside
the code tree:

```sh
python3 -I -S -B verify.py extract --assets /path/to/assets --data /path/to/new-data
python3 -I -S -B verify.py inventory --data /path/to/new-data --work /path/to/new-inventory
```

Extraction requires a new data directory. It verifies every archive, rejects
unsafe or unexpected members, and checks the exact global file union before
recording success. Inventory checks every declared data file's presence and
size, together with the configured metadata and source hashes. Full data-content
hashing is performed during extraction and the mathematical checks. Inventory
performs no mathematical count or theorem verification. Neither command needs
a compiler.

## Run representative numerical controls

```sh
python3 -I -S -B verify.py sample --data /path/to/new-data --work /path/to/new-sample --compiler /usr/bin/c++
```

This chooses declared representative records from every numerical regime and
recounts their complete systems. It verifies the interface and selected values,
not exhaustive positivity. Repeat the same command with the same work directory
to continue if the explicit call limit is reached. Use a different fresh work
directory to change the source version, compiler or frozen parameters.

## Reproduce the complete finite proof

```sh
python3 -I -S -B verify.py full --data /path/to/new-data --work /path/to/new-full --compiler /usr/bin/c++
```

The full profile permits at most 256 controller calls per invocation and
4,096 scientific jobs per controller call, with the original child deadlines,
finite source rosters and cumulative counting allocations. Larger batches
avoid repeatedly authenticating the same long history. If the explicit call
limit is reached, repeat the same command with the same work directory;
completion requires the final complete report. Configuration and completed
source-bound receipts are checked on every continuation. The full route regenerates the original
census and predecessor certificates, all terminal geometry/algebra/bounds,
literal residual coverage, fresh numerical values and the final acceptance
union. It retains the explicitly cited universal theorem premises.

The frozen [configuration](REPRODUCTION-CONFIG.json) supplies the measured
local numerical and upstream allocations and acceptance slice size. These
are finite per-workspace allocations, not permission to consume an arbitrary
research budget. The manual exhaustive export replay and the convenience
entrypoint tests are distinguished in `REPLAY.json`; no unperformed run is
implied by the existence of a command.

The recommended unused-check policy keeps all original determining nodes and
uses the first two positive integers outside each U02 determining set. It
replaces large held grades for 40 parents with 80 fresh checks. The original
larger-grade observations remain source evidence. A separate optional original-
hold replay is a stronger, potentially much more expensive audit.

## Inspect and report an issue

[SOURCE-MAP.json](SOURCE-MAP.json) binds the data, proof and code sources;
[FILE-MANIFEST.json](FILE-MANIFEST.json) lists the distributed module files. Preserved
historical paths and earlier incomplete headers are provenance labels. The
portable adapters resolve inputs only from the explicitly selected roots.
Original mathematical bodies remain available beside the adaptations.

For an objection, identify the source version, exact triple or terminal ID,
the claimed mathematical bridge, and the complete command/result when relevant.
The most useful review targets are domain coverage, whole-count reductions,
the original lattice and true interior, and the exact sign certificates.
Human mathematical review and FrontierMath's disposition remain separate from
the campaign's acceptance and reproducibility checks.
