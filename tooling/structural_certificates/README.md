# Structural normal and boundary certificate replay

This module requires Python 3.11 or later and a POSIX environment. It contains two byte-identical accepted mathematical checkers, their 54 existing tests, a byte-identical copy of the published `whole_rank_six/runtime.py`, a reader adapter, and a ZIP restorer. The data are distributed separately as `structural-certificates-data-v1.zip` (273,273,064 bytes; SHA-256 `cc5169a8509233cbb4e4b6241a176b418ebe25a061930f35b5d560b5335ec8b8`). `DATA-ASSET.json` binds every one of its 10,456 mathematical files and 269,680,674 uncompressed bytes by relative path, length and SHA-256. The ZIP contains no returned program, provider conversation or harness history.

Download the ZIP from the [versioned release](https://github.com/chris-hadad/lr-stretching-results/releases/tag/rank-six-2026-09-25-v1) into an archive directory. Then run from this module directory:

```sh
python3 -B restore.py inspect --archives /path/to/archive-directory
python3 -B restore.py restore --archives /path/to/archive-directory --out /path/to/fresh-data
python3 -B restore.py verify --out /path/to/fresh-data
python3 -B -m unittest -q normal_checker_tests pro027_mask_tests
python3 -B reader_replay.py calibrate --data /path/to/fresh-data --output-root /path/to/fresh-run
python3 -B reader_replay.py all --resume --data /path/to/fresh-data --output-root /path/to/fresh-run
```

The restore output must be fresh and disjoint from the module and archive directory. The reader output must also be fresh and disjoint from the module and restored data. `--resume` requires the same reader, runtime, data verifier, mathematical engines, data manifest and job roster by exact source hash. Optimized Python is refused. The public reader runs every child through its bounded cancellation-aware supervisor, uses `runtime.stop_group` and `runtime.group_exists` for exact group cleanup, and preserves each fresh report. The data verification subprocess uses the same supervisor. Outer INT, TERM, and HUP requests stop the owned child group before the reader exits. It does not sample child RSS. Use a new output directory for an independent replay.

`JOBS.json` declares 656 exact slice identities, intervals, expected statuses and accepted historical report hashes. `all` regenerates all slices and four complete joins. P08 adopts only the freshly replayed P07 aggregate. Historical reports are source locators, never substitutes for fresh results. The earlier source-identical campaign run completed all four aggregates in a 572.497-second report timestamp span. The final public reader was then run independently over all 656 slices, four freezes and four complete joins: all 664 children passed in 467.749 seconds, and every owned process group exited. Its prior 13-child calibration and zero-child exact resume are separate observations. [VERIFICATION.json](VERIFICATION.json) binds the completed public execution. On the packaging host, the complete ZIP restore took 1.883 seconds and an independent second rehash took 0.733 seconds; time and storage costs vary by machine.

The normal checker covers 34 sealed rosters, all 5,480 referenced Laurent types, 1,508,387 independent simplicial rows, 34,761 dependent rows, 127,467 incidences and the original-rhombus exception preimages. Its finite scope supports the ambient `c_(D_n-4)` argument through ranks 6–12, with the stated actual-degree qualification. P06 covers the rank-six and rank-seven selected at-most-four-coordinate boundary criterion, including exact forcing exceptions; rank seven is not subsumed by the whole-rank-six theorem. P07/P08 cover the rank-six selected at-most-five-coordinate criterion and its complete P07 adoption. These are finite certificate checks, conditional on the analytic proofs and accepted forcing tables listed in `DEPENDENCIES.md`. They do not prove unrestricted rank seven, every actual quartic or quintic, generic rank-six `c_1`, or KTT.

The F025 rank-six and rank-seven forcing tables are a separate **finite forcing premise**. Run the [complete F025 recheck](f025/README.md) on the same restored data. It regenerates every one of 32,768 and 262,144 records and checks full original row correspondence in 14.778 seconds on the recorded host; 10 positive and 21 refusal controls passed. The result supplies sound dimension upper bounds under boundary equalities, not actual dimension or complete universal closure. The normal/mask command authenticates these tables but does not rerun this separate proof premise.

`SOURCE-MAP.json` identifies accepted checker sources, repository-relative data provenance, unchanged source hashes and every wrapper or metadata transformation. The public manifest and job roster contain inert repository-relative provenance labels only; restoring the downloaded archive never requires the private captured packet. Fifteen refusal/cleanup fixtures in `public_controls.py` cover the ZIP, restored data, reader paths, optimization, resume identity and owned process groups.

[Structural results](../../results/structural-positivity/README.md) · [All tools](../README.md) · [Result catalog](../../RESULTS.md)
