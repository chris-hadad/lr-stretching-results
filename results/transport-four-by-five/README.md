# Whole four-by-five transportation positivity

For every pair of balanced nonnegative integral margins of a 4-by-5 table,
every ordinary stretching coefficient is strictly positive through actual
degree; higher coefficients vanish. Delete zero margins first: with p active
rows and N active columns the degree is (p-1)(N-1). Empty total, one active
row or one active column gives polynomial one. Transposition and all active
subrectangles are included. The whole LR constructor has ordinary rank at most
eight and preserves the original saturated lattice and stretch.

The proof joins the complete [quadratic](proofs/quadratic.md),
[cubic](proofs/cubic.md) and [higher-coefficient](proofs/higher.md) arguments.
The [linear theorem](proofs/linear-four-by-five.md) supplies c1, including all
zero-margin boundaries through its explicit closed-boundary argument. Its
complete N=5 finite gradient certificate is included and freshly rechecked. The
[whole table/LR map](proofs/whole-table-lr.md) defines the original object.
This is not every rank-eight LR triple and is not unrestricted KTT.

## Data and restoration

The [archive manifest](DATA-ASSETS.json) and [mathematical file manifest](DATA-MANIFEST.json) bind the complete companion. Download it from the repository's [versioned releases](https://github.com/chris-hadad/lr-stretching-results/releases).

The complete 4-by-5 companion data is supplied separately as
`transport-four-by-five-data-2026-09-25-v1.tar.gz` (308,421,533 bytes;
SHA-256 `ef9b326c0b9be511f08cfcfd4ca84c73c3f196d20358142e38cfd7dd8c858c11`). It contains exactly 47 mathematical input files,
with 1,483,813,110 uncompressed bytes, and is separate from the
main rank-six certificate bundle. Keep `restore_data.py`, `DATA-ASSETS.json`
and the unchanged `DATA-MANIFEST.json` together in this result module. Place
the archive in a download directory, then choose a fresh output directory
outside the module, archive and original-source roots:

```sh
python3 -B results/transport-four-by-five/restore_data.py --archives /path/to/downloaded-assets --out /path/to/transport-four-by-five-data
```

The restorer needs only Python 3.11 or later. It authenticates the compressed
archive before creating output, then checks every path, regular-file type,
size and SHA-256, refusing omissions, duplicates, unsafe links and existing or
overlapping output. `RESTORE.json` records completion; failed restores remain
explicitly partial. Publishers can also pass `--source-root /path/to/original-data`
to protect an original uncompressed source tree. Restoration verifies data
identity; the module's separate `reproduce.py --data /path/to/transport-four-by-five-data --scratch /your/scratch`
command performs the mathematical replay.

Full serial replay after obtaining that data:

```sh
python3 -B results/transport-four-by-five/reproduce.py --data /path/to/transport-four-by-five-data --scratch /your/scratch
```

Python uses the standard library. C++17 and GMP are required. If GMP is outside
the compiler's default paths, point to the existing installation explicitly:

```sh
GMP_PREFIX=/path/to/gmp
CPPFLAGS="-I$GMP_PREFIX/include" LDFLAGS="-L$GMP_PREFIX/lib" \
  python3 -B results/transport-four-by-five/reproduce.py --data /path/to/transport-four-by-five-data --scratch /your/scratch
```

For example, Apple Silicon Homebrew commonly uses `/opt/homebrew`; use your
actual installation prefix. No installation or provider program runs. The final public replay after the
execution-boundary repairs completed in 144.684 seconds on the recorded host.
The replay rebuilds the full 392-array atlas from labeled-edge integer counts,
retains all original offsets before low-degree contraction, regenerates the
quadratic carriers, and verifies all 52 disjoint cover/field batches. It joins
all 632,696 cells, 4,209,661 contained simplices, 15,573 rays, 46,616,414 pairs
and 248,939,603 triples. It also recomputes the 317 higher local constants,
all original lattice/topology classes, and the 17 full strictness baselines.

The 52 batches historically took 181.947 seconds in total. Ancillary arithmetic
was short: atlas counts about 2.18 seconds, templates 2.08, encodings 2.10,
topology 1.44, BV values 3.59, baselines 0.19 and final join 7.43. These are
historical measurements, not a portable runtime guarantee. Allow several
minutes and several GB of scratch space. This portable adapter passed a fresh private-candidate replay in 317.377
seconds on a concurrently occupied host; its 52 batches used 282.098 seconds.
Publication review remains separate. The complete output was retained.

Pro030 supplied the theorem/certificates; the campaign independently rebuilt
the numerical premises and accepted the complete result during Pro031's final
integration. Source authentication, finite replay, proof review and external
human scrutiny are distinct. No worldwide-priority assertion is made.

The linear coefficient also uses the existing published double-cut/A3 proof
and its [source data](../families-and-obstructions/data/transport/four-by-five-source.json).
These remain in the complete repository. The new replay independently rebuilds
the full atlas and checks the same 154 vanishing linear gradients.

`slr_ehrhart.transport.transport_count` and `transport_to_lr` already accept
these sizes. The older `transport_certificates` verifier remains limited to its
three-by-five/four-capacity fixed certificate; this new result uses the separate
complete checker here. Do not relabel the old finite certificate as a four-by-five
certificate or merge its byte-bound input schema with this companion dataset.

The existing `three_row_coefficients.transport_polynomial` still accepts at
most three rows. Its computational contract has not become four-row merely
because the theorem is stronger. The bundled `src/transport_math.py` supplies
complete four-by-five polynomial machinery, but its historical default
`whole_polynomial` wrapper requires positive columns; the lower-level explicit
generic-margin interface has a separate boundary contract. This result's
certificate replay covers all nonnegative margins through the closed-cell
proof and complete cover, independently of that wrapper's input restriction.

[All results](../../RESULTS.md) · [Main page](../../README.md) · [Tools](../../tooling/README.md)
