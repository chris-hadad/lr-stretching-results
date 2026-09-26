# Complete lower-coefficient verification

This package contains the campaign-owned c2/c3 finite checkers and a portable
wrapper. Complete scientific engines were replayed on isolated data; the final
wrapper's additional clean-export tests are specified below. The eight files under `src/`
retain their mathematical code; `check_field.py` adds only an early refusal
when Python assertions are disabled. `SOURCE-MAP.json` binds their copied and
adapted hashes. `ASSETS.json` binds 271 inert external inputs by path, size and
SHA-256. No provider program, original job wrapper or input asset is included.

Use Python 3.11 or later, a C++17 compiler available as `c++` on `PATH`, and
GMP C++ headers and libraries. By default the wrapper links with
`-lgmpxx -lgmp`; on macOS it recognizes an installed Homebrew GMP prefix.
Use `--cxx /path/to/compiler`, `--gmp-prefix /path/to/gmp`, or
`--gmp-include /path/to/include --gmp-lib /path/to/lib` when needed. The
wrapper requires at least 4 GiB measured available memory before each child;
macOS measurement uses free, inactive and speculative pages, while Linux uses
`MemAvailable`. A failed memory or dependency check is a refusal, not evidence
about the mathematical result.

Assemble the exact manifest tree at `/path/to/data/lower`. Choose
`/path/to/new-run` outside both the source package and asset tree, with an
existing parent directory. The first command creates that output directory;
later commands use the same directory. From the package directory, run the
phases serially:

```sh
python3 -B replay.py --asset-root /path/to/data/lower --output /path/to/new-run --phase c3-core
python3 -B replay.py --asset-root /path/to/data/lower --output /path/to/new-run --phase c3-analytic
python3 -B replay.py --asset-root /path/to/data/lower --output /path/to/new-run --phase c2-field
python3 -B replay.py --asset-root /path/to/data/lower --output /path/to/new-run --phase h8-small
python3 -B controls.py --asset-root /path/to/data/lower --output /path/to/new-run
python3 -B replay.py --asset-root /path/to/data/lower --output /path/to/new-run --phase h8-full
python3 -B q8_rhs_replay.py --asset-root /path/to/data/lower --output /path/to/new-run
```

`h8-through4` and `h8-through5` are optional complete-level waypoints before
`h8-full`. `q8_rhs_replay.py --sample` checks one 16,384-type sample without
coverage credit in its own phase directory. The default is one child at a
time. The `--workers 2` option exists for H8 and q8 batches. First measure your
available memory and the cost of the sample; account for other running work.
The supplied default is serial, and the program enforces its memory floor.

The phases recheck different exact finite premises. `c3-core` checks q1–q7
topology, the geometric operator and the declared c3 field rows.
`c3-analytic` checks the complete 65-range analytic partition. `c2-field`
checks original q8 field rows and saturated operator action. H8 checks the
top-layer rows in level order; every level token depends on complete lower
coverage. The final q8 phase regenerates and compares accepted scalar rows.
The controls deliberately reject changed inputs, a zero field and malformed
H8 subjects. These numerical checks rely on the separate mathematical proof
for their whole-coefficient implications.

Each compiler or checker child runs in a new session with its normal signal
mask. TERM, HUP and INT set a cancellation flag; short communication polls
then stop and wait for the exact owned process group. A timeout or error uses
the same cleanup path.
A fresh successful H8 range records its row SHA-256 in the process receipt,
together with the checker binary and build binding, controller/runtime, source
map, asset manifest, source list and lower-token identities. On continuation,
the adapter requires that production-time binding and rechecks every row's
JSON fields, consecutive type ID, index and numerator-point count against the
manifest-verified inputs, as well as complete receipt counts. Completed-level
validation and lower tokens use the same range check. Earlier H8 outputs that
lack this binding are refused; preserve them as historical evidence and run a
fresh H8 sequence in a new output directory if continuation is needed. These
local hashes detect changed output and identity drift; they do not authenticate
coordinated changes to both output and metadata or replace a fresh mathematical
replay from trusted sources.
The JSONL audit rows have counts and timing rather than rational coefficients;
the rational `qk.layer8` rows remain hash-verified inputs read by the checker.

A completed q8 range may be reused only after its receipt and data pass the
adapter's validation. A partial range, occupied completed phase or changed
source/asset is refused;
remove or repair such output only after inspecting its exact identity. An
incomplete run grants no full replay credit.

`tests/test_adapter.py` stages bounded refusal checks for a missing compiler,
optimized Python, malformed or omitted analytic and operator ranges, H8 output
binding and per-type row tampering, macOS memory parsing and TERM cleanup of a
synthetic child. Run them with:

```sh
python3 -B -m unittest discover -s tests -p 'test_adapter.py'
```

Those tests exercise adapter behavior, not the scientific certificate. The
final public source export passed all seven adapter checks, complete c3 core,
complete c2 field, small H8 levels, all six scientific controls and a diagnostic
q8 shard. The complete c3 analytic/H8/q8 mathematical engines passed separate
full-domain replays on identical mathematical sources and input bytes. The
final convenience wrapper's full long H8/q8 orchestration was not repeated.
See the parent [verification record](../VERIFICATION.json) for these exact
scopes; a diagnostic or interrupted phase never counts as a complete replay.
