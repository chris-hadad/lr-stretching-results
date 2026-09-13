# Optional complete integer H-system counter

`complete_h_system.cpp` is an unchanged source copy of the reviewed
`v2_independent_hive_recount.cpp`. It counts all integer points inside
inclusive finite bounds satisfying every supplied affine inequality. Its
interval propagation, canonical memoization and component factorization use
exact arithmetic; mixed rows are retained unless an exact box implication
makes a row redundant.

It requires C++17 with GCC/Clang-compatible `__int128` and overflow builtins.
No Boost, GMP, network or installation is required. To compile in a fresh
temporary directory and run three tiny counts plus an explicit work refusal,
from the repository root:

```sh
build_dir=$(mktemp -d)
c++ -std=c++17 -O2 tooling/cpp/complete_h_system.cpp -o "$build_dir/complete-h-system"
python3 -B tooling/cpp/control.py --binary "$build_dir/complete-h-system"
```

The control leaves the chosen build directory for inspection. It starts the
binary directly and kills/waits on a ten-second timeout. It prints raw output
before comparing counts. A successful process exit alone is insufficient:
each response status and exact count must also be checked.

## Protocol

One whitespace-delimited request consists of:

```text
RECOUNT1 identity n m max_states milliseconds
lo_1 hi_1
...
lo_n hi_n
c_1 a_11 ... a_1n
...
c_m a_m1 ... a_mn
```

Every row means `c_i + sum_j a_ij*x_j >= 0`. Requests may be concatenated
until EOF. Identities contain 1 to 160 ASCII letters, digits or `_-.:`.
There are at most 64 variables and 10,000 rows. Bounds and row entries are
signed 64-bit integers; `max_states` is 1 through `2^63-1`, and the
per-request deadline is 1 through 110,000 milliseconds. The counter uses
checked signed 128-bit intermediate arithmetic and unsigned 128-bit totals.

Each valid request produces one JSON line. Complete responses contain
`status="complete"`, a decimal-string count, identity, visited-state and
row-work statistics. Refusals use `REFUSED_INPUT`, `REFUSED_OVERFLOW`,
`REFUSED_WORK`, `REFUSED_TIME`, `REFUSED_DEPTH`, `REFUSED_MEMORY` or
`REFUSED_INTERNAL`, with a null count. Input errors may omit the identity
and exit with code 2. Other refusals can occur with process exit 0.
Partial work and arithmetic exhaustion never mean count zero.

This is a bounded scalar counter. The caller must prove that the finite box
contains the complete intended lattice object, that the supplied chart is
saturated and that all original inequalities are present. It does not establish
an LR identity, an affine hull, true interiors, degree or reciprocity.
The control's tiny fixtures check the interface; they do not discharge those
proof obligations for any research input.

