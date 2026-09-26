# Fresh counts for the gap-three and rank-ten endpoint families

The commands below regenerate all 40 positive gap-three counts and all 98
positive transportation counts. They supplement the historical-data algebra
commands in [README.md](README.md); those existing commands keep their original
scope. The accepted inputs in `data/gap-three.json` and `data/transport.json`
are unchanged. Each fresh run preserves its reconstructed full vectors before
comparing unused grades or accepted numerical values.

Requirements are Python 3.9 or later, its standard library, a POSIX environment,
and a C++17 compiler supporting checked signed `__int128`. The compiler is
`c++` by default; select one executable with `--cxx /path/to/clang++` or `CXX`.
GMP is not required. There are
no Python packages, private packets, external data downloads or provider
programs to install. From the repository root, set `SCRATCH` to an existing
writable scratch directory, preferably on an external volume, and use fresh
output directories:

```sh
SCRATCH=/path/to/external/scratch
python3 -B results/structural-positivity/replay/fresh_counts.py gap --output "$SCRATCH/lr-gap-fresh" --deadline 300
python3 -B results/structural-positivity/replay/fresh_counts.py transport --output "$SCRATCH/lr-transport-fresh" --deadline 300
python3 -B results/structural-positivity/replay/controls.py --gap-run "$SCRATCH/lr-gap-fresh" --transport-run "$SCRATCH/lr-transport-fresh" --output "$SCRATCH/lr-fresh-controls"
```

The `--calibrate` option evaluates only P00 at grade 1 and P11 at grade 10 for
gap-three, or `(h,t)=(0,1),(0,14),(6,14)` for transportation. Calibration output
is explicitly incomplete for the theorem's finite bases. The full runs are
serial, refuse existing output directories, impose individual child and whole
run deadlines, wait for every child, and preserve incomplete attempts. Increase
the whole-run `--deadline` up to 7200 seconds if needed; each original count
still has its own 100-second internal and 110-second child boundary. A refused
node supplies no usable partial scalar.

`result.json` must report `COMPLETE_FRESH_GAP_THREE_RECOUNT` or
`COMPLETE_FRESH_INTEGER_H_TRANSPORT_RECOUNT`. The controls report
`COMPLETE_CONTROLS`. `source-binding.json` records the exact code and accepted
data used. `raw-vectors.json`, `algebra.json` and `fresh-counts.json` contain the
mathematical outputs. All 189 transportation assignment records, including
zeros, are retained for every positive node. Generated launch and timing
records are local verification evidence, not new mathematical premises.

The publication replay completed the gap-three command in under one second
including compilation, the transportation command in 6.306 seconds, and the
controls in 0.231 seconds on its recorded machine. These are observed costs,
not performance guarantees for other hardware or arbitrary LR instances.

## Exact objects and finite determination

For integers `x,y >= 0`, the gap-three family has outer partition

```text
lambda = (3x+15+9y, 2x+12+7y, x+9+5y, 6+3y, 4+2y, 2+y),
mu     = (lambda_2, ..., lambda_6),
nu     = (2x+5+2y, x+4+2y, 3+2y, 2+2y, 1+y).
```

Write `Pxy(t)=c_(t mu,t nu)^(t lambda)`. The four bases are
`P00, P10, P20, P11`. Their ordinary rank is 6, their actual degree is 10, and
their true codegree is 3. The strict weighted-GT theorem supplies the saturated
integer lattice, the actual dimension, `P(0)=1`, and the roots `-2,-1`. These
are analytic premises; the program does not guess them from samples. Grades
1 through 8 determine each polynomial, and independently recounted grades 9
and 10 are unused checks: 32 determining and 8 unused positive nodes.

The fresh engine uses the whole branching identity from
[Proof 001](../proofs/pro027/001-COMPLETE-GAP3-CLUSTERS.md). For every
`u1+u2+u3=3t`, it retains the exact three-letter multiplicity, and it expands
the complete five-by-five skew Jacobi–Trudi determinant over all 120
permutations. Negative complete-homogeneous indices give zero. All surviving
terms are complete three-column integer table counts; their signs and integer
multiplicities remain in the final sum. The signed 128-bit arithmetic checks
every addition, subtraction and multiplication for overflow. Overflow, scope,
time, work and table-size refusals cannot be interpreted as zero.

Two exact reconstruction algorithms, Lagrange and Newton, must agree. The
program derives `Q0=(P20-P10)/t`, including its constant coefficient, and retains
`W0=P00-P10+t Q0` as an auxiliary polynomial. Its four negative coefficients
are preserved; they are not negative ordinary LR coefficients. The unchanged
whole-count algebra verifies all factor arrays, both closed hinge quotients,
169 finite hinge identities, initial absent-correction branches, complete
quadrant and difference identities, and all 40 positive joint coefficients of
the homogeneous cone. Its entire quadrant law is

```text
Pxy = P11 + (x+y-2)t Q1 + (x-1)(y-1)t^2 R       (x,y >= 1),
Px0 = P10 + (x-1)t Q0                          (x >= 1),
P0y = P10 + (y-1)t Q0                          (y >= 1),
P00 = P00.
```

The unbounded count identities rely on
[Proof 004](../proofs/pro027/004-UNBOUNDED-RANK6-POSITIVITY.md),
[Proof 005](../proofs/pro027/005-COMPLETE-QUADRANT-AND-DUALITY.md),
[Proof 006](../proofs/pro027/006-QUOTIENT-MOMENTS-AND-POSITIVE-CERTIFICATE.md), and
[Proof 007](../proofs/pro027/007-HOMOGENEOUS-CONE-AND-BOUNDARIES.md),
including the independent-width argument. The full quotient lattice,
sharp initial threshold and wall corrections are respectively
[Proof 002](../proofs/pro027/002-QUOTIENT-LATTICE-AND-ZERO-GRADE.md),
[Proof 003](../proofs/pro027/003-SHARP-AFFINE-THRESHOLD.md), and
[Proof 008](../proofs/pro027/008-INITIAL-WALLS-AND-POSITIVE-DIFFERENCES.md).
They are not inferred from a
rational substitution or a finite grid. For the homogeneous family in Proof
007, the full count is `P11(st)+(a+b)t Q1(st)+ab t^2 R(st)` for integers
`s,a,b >= 0`. At `s>0`, the actual degree is 10 and codegree `ceil(3/s)`.
At `s=0`, the count is `(at+1)(bt+1)` with actual degree 2, 1 or 0 and its
own saturated rectangle, segment or point lattice. Ordinary rank is 6 when
`s+b>0`, 3 when `s=b=0<a`, and 0 at the origin. The separately proved edge
`P10(st)+bt Q0(st)` has the boundary `1+bt`. The full strict-GT hypotheses
are in [the interior proof](proofs/WEIGHTED-GT-INTERIORS.md). None of these
checks establishes positivity for all gap-three profiles. Its antecedents
are the full staircase proof in [General height](proofs/GENERAL-HEIGHT.md)
and the elementary branching/interval/path-cancellation identities in
[Delta-two branching](proofs/DELTA-TWO-BRANCHING.md); no gap-two positivity
conclusion is imported outside its own domain.

For each integer `h >= 0`, the transportation endpoint family is the original
ordinary rank-ten LR triple

```text
lambda_h = (27+h,22+h,18+h,17+h,13,10,8,6,4,2),
mu_h     = (17+h,17+h,17+h,13,10,8,6,4,2),
nu_h     = (17+h,10,5,1).
```

The outer size is `127+4h`. Its complete count equals the number of nonnegative
integer four-row, seven-column tables with margins

```text
rows    = t(7+h,5,4,1),
columns = t(4+h,3,2,2,2,2,2).
```

[Proof 011](../proofs/pro027/011-COMPLETE-RANK10-CAP-RELEASE-FAMILY.md)
establishes the whole LR/table identity and stabilization. The actual dimension
is 18. The literal first-three-row/first-six-column coordinate chart and its
integer inverse give the saturated `Z^18` lattice; network total unimodularity
gives integral vertices. The unit row needs seven positive entries, and an
explicit strict grade-seven table proves true codegree 7. Reciprocity supplies
roots `-1,...,-6`. The program reconstructs from these roots, constant 1 and
fresh grades 1 through 12, then checks unused grades 13 and 14. This is exactly
98 positive nodes: 84 determining and 14 unused.

## Complete transportation assignment arithmetic

[Proof 012](../proofs/pro027/012-INDEPENDENT-WHOLE-MODELS-AND-CHALLENGES.md)
derives the signed complete assignment identity. Assign each of seven labeled
columns to classes 1, 2 or 3. Class 4 is exactly zero by its strictly positive
sink target, not discarded heuristically. Group the five equal columns while
retaining the classes of the two distinguished columns. There are
`9 * binomial(7,2) = 189` groups, of total labeled weight `3^7 = 2187`.
For occupation `(a,b,c)` and assigned column sums `(C1,C2,C3)`, the sign is
`(-1)^b` and the unscaled integer shifts are retained:

```text
X = t(C1-7-h)-b-c,    Y = t(5-C3)-2c,    Z = t.
```

Set `B_m(y)=binomial(y+m-1,m-1)` for `m>0,y>=0`, set `B_0(0)=1`, and set
it to zero for negative `y` or for `m=0,y!=0`. The complete unsigned group
count is

```text
sum_(y1+y2+y3=Z) B_a(y1) B_b(y2) B_c(y3) K(X-y1,Y-y1-y2),
K(U,V) = sum_(z=0)^min(U,V) B_(a+c)(z) B_(a+b)(U-z) B_(b+c)(V-z).
```

Negative targets give zero. All multiplicities, signs, zero-occupation cases
and all 189 groups remain in each node. The campaign-owned Python checker
uses direct arbitrary-integer weak-composition and A2 convolution, distinct
from the historical packed unsigned-table and repeated-edge grid programs.
Those historical returned programs are not executed or required here.
This is independent implementation and arithmetic evidence for the complete
signed-assignment formula, not a new formula-free generic LR engine.

All seven full vectors have 133 positive ordinary coefficients; their six
complete differences have zero constant and 108 positive nonconstant entries.
The final difference is exactly `binomial(t+17,18)`, equal to 1 at `t=1`.
Together with the analytic full-cap argument, this proves the sharp integer
stabilization threshold `h=6`, and positivity for the entire integer-h family.
No arbitrary noninteger `h=v/u` coefficient-positivity theorem follows from
these seven endpoints. The optional cut-functional comparison is not freshly
recomputed. The older size-133 parent is related to `h=0` by row and column
permutations, not identical bare partitions and not an eighth endpoint. The
new four-by-five transportation result has a different whole-object scope
and does not replace this four-by-seven replay.

## Controls, provenance and limits

`controls.py` compares the table recurrences with small literal table
enumerations, checks all 120 determinant permutation signs, and deliberately
rejects overflow, excess work, unsupported parent/grade, insufficient table
space, trailing input, missing/duplicate nodes and groups, changed signs and
offsets, partial assignments, malformed scalars, altered unused holds,
unproved class-four exclusion, a timed-out child and a signal interrupt. It
checks actual child and process-group exit after timeout and interruption.
The publication run passed 142 positive cases and 24
negative controls.

The numerical engines are selected from the campaign's accepted independent
September 12 checkers. `gap3_jt_counter.cpp` is byte-exact;
`gap_model.py` and `transport_math.py` preserve the selected mathematical
function/class bodies without changes. `exact.py`, `gap_algebra.py` and the
accepted JSON inputs reuse the existing public bytes. The new wrapper supplies
portable scope, process, preservation and comparison interfaces. The exact
source hashes, selected functions and public file bindings are recorded in
[FRESH-COUNTS-SOURCE-MAP.json](FRESH-COUNTS-SOURCE-MAP.json).

The analytic identities and geometric premises remain the proofs identified
above and in [DEPENDENCIES.md](DEPENDENCIES.md). Fresh finite counts do not
independently prove those all-parameter statements. Neither a copied proof nor
a positive quotient is presented as a new independent whole-rank theorem.
