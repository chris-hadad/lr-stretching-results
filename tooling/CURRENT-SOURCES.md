# Current tooling source notes

This update copies the maintained `two_widths`, `rank6_split`,
`rank8_clipped`, fixed clipped coefficient data and `matrix_invariants`
modules from the research package. The matrix module includes general
rectangular scalar counts. The public initializer adds nine entry points and
retains every previous export.

Only the split module's import changes: two exact `partition` and `triple`
helper bodies are placed in private `_partitions.py`. The complete Horn
module, census/process orchestration, engine installation, native interfaces
and broad research CLI are not dependencies of these APIs and are omitted.
Historical absolute strings in source comments, result metadata and proof
notes remain provenance, with no runtime lookup of the research checkout.

The previous initializer, matrix module, README and proof overview are kept
under `history/previous-tooling/`. All earlier examples, checks, benchmark
artifacts and source notices are preserved byte for byte. Selected maintained
tests retain their mathematical bodies; the square and rectangular test
projections remove only research CLI test classes and the CLI import.

New proof notes point to the complete selected source arguments and exact
adoption excerpts. The clipped-family JSON projections retain every
mathematical field and list order, including full coefficient, count, chart,
cut and witness data. They remove the declared operational path, process,
timing and counter fields. The wrapper pins each original source hash.
`SOURCE-UPDATE.json` records the exact source and included hashes,
transformations and complete selected-file roster. It is a source record,
not a scientific execution receipt.

The unchanged C++ H-system kernel comes from the separately reviewed fresh
count work. The small Python control driver only exposes its protocol and
refusal semantics. Python APIs need the standard library; the optional kernel
needs a compatible C++17 compiler and no Boost/GMP.

[The original notice](SOURCE-LICENSES.md) remains in force. This update makes
no new licensing, worldwide novelty or human-peer-review assertion. Returned
research programs are not imported into the runtime package. The current
examples and check commands are reproducible routes; their actual execution
evidence belongs in the review records, with fresh results distinguished from
the preserved research observations.

