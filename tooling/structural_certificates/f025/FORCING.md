# Complete recheck of the accepted boundary-mask forcing tables

This checker regenerates every rank-six and rank-seven boundary-mask record
used by the structural mask certificates: 32,768 and 262,144 records,
respectively. It compares the boundary mask, the entire closed-rhombus bitmask
and the sound dimension upper bound. It also verifies the exact full row and
coordinate ordering against `original_rows(n)` in the accepted
`verify_pro027_masks.py`.

The result is a **sound dimension upper bound**, conditional on the prescribed
boundary equalities. It does not establish feasibility, actual dimension,
lattice-point counts, or completeness of all possible boundary-forcing
implications. This is a fresh recheck of a previously accepted finite premise,
not a new positivity theorem.

## Reader commands and dependencies

Use Python 3.10 or later and its standard library on a POSIX system. No Sage,
compiler, Python package or provider program is required. Optimized Python
(`-O` or `PYTHONOPTIMIZE`) is refused. First restore the existing structural
certificate data bundle with the parent directory's `restore.py` instructions; no new
archive is needed. Let `DATA` be that restored root and `SCRATCH` an existing
writable external scratch directory. From the repository root:

```sh
DATA=/path/to/restored/structural-certificates-data
SCRATCH=/path/to/external/scratch
python3 -B tooling/structural_certificates/f025/verify_forcing.py --data-root "$DATA" --output "$SCRATCH/forcing-calibration" --calibrate 1024 --deadline 120
python3 -B tooling/structural_certificates/f025/verify_forcing.py --data-root "$DATA" --output "$SCRATCH/forcing-full" --deadline 180
python3 -B tooling/structural_certificates/f025/forcing_controls.py --data-root "$DATA" --output "$SCRATCH/forcing-controls"
```

Each output directory must be new, its parent must exist, and it cannot
overlap the code or data tree. The checker runs one child at a time with an
explicit wall deadline, kills its owned process group on interruption or
timeout, and waits for the child to exit. Interrupted attempts remain
incomplete. The whole-run deadline may be increased up to 3600 seconds.
Calibration samples 1,024 masks spread across each complete bit domain and is
explicitly not a complete-domain pass. The full command must finish with
`COMPLETE_F025_FORCING_RECHECK` and `masks_compared=294912`.

The only data members used are already in `DATA-ASSET.json`:

| Member | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `f025/F025-MASK-R6-001.json` | 32,768 | 3,355,507 | `6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0` |
| `f025/F025-MASK-R7-001.json` | 262,144 | 28,416,986 | `bb595b3914ce05105743e9386f2cc64a4d2ae2d59df0d340c3221b8b74d7cd9c` |

Both files are authenticated before use and rehashed at completion. Their
small historical runtime headers are retained in the accepted bytes but are
not used as evidence that the new computation succeeded. The old provider
atlas is not required. The new computation reconstructs the model directly
from the complete original rhombus stencils.

The parent directory's `verify_pro027_masks.py` and `DATA-ASSET.json` are read without
execution. For a separated checkout they can be supplied explicitly through
`--row-checker` and `--data-manifest`. The row checker must have its exact
accepted hash; the two data-member size/hash bindings must match the constants
above. All other computational dependencies are the small supplied modules
`forcing_model.py`, `forcing_hive.py` and `forcing_rows.py`.

## Definitions and the soundness argument

Let `n` be 6 or 7. A hive uses integer-indexed vertices `(i,j)` with
`i,j >= 0` and `i+j <= n`. Its interior coordinates, in lexicographic order,
are `(i,j)` with `i,j >= 1` and `i+j < n`. Their ambient number is
`(n-1)(n-2)/2`, namely 10 or 15. The full system has `3n(n-1)/2` original
rhombus inequalities, namely 45 or 63. Each row is the sum at its two obtuse
vertices minus the sum at its two acute vertices, with nonnegative slack.

For the original ordinary LR boundary `c^lambda_(mu,nu)`, lambda is outer and
the balanced boundary convention is

```text
h(i,0)   = mu_1 + ... + mu_i,
h(0,j)   = lambda_1 + ... + lambda_j,
h(n-j,j) = |mu| + nu_1 + ... + nu_j,
|lambda| = |mu| + |nu|.
```

Partitions are padded to `n` parts. A boundary mask has `3(n-1)` bits. Bit
`s(n-1)+k`, for zero-based `k=0,...,n-2`, asserts equality of consecutive
parts `k` and `k+1` on side `s`: lambda, then mu, then nu. The integer mask
domain is exactly `0,...,2^(3(n-1))-1`; no symmetry reduction removes masks.
Some masks or particular boundaries may be infeasible. The resulting bound
remains a conditional upper bound and does not assert that a hive exists.

The preserved campaign model performs these finite steps:

1. Generate all original rhombus rows in the full vertex coordinates.
2. Enumerate every positive sum of one row or two **distinct** rows. Group
   literally equal full-coordinate sums. If a sum's rows all have zero
   slack, every row in every equal positive expression must also have zero
   slack, since all summand slacks are nonnegative. These are sound forcing
   rules. The regenerated sets have 60 rules at rank 6 and 90 at rank 7.
3. For each consecutive boundary gap, find its unique expression as the sum
   of two distinct rhombus rows. A zero partition gap forces both slacks to
   vanish. Initialize the zero-row set using every bit of the boundary mask,
   then iterate the finite rule set to its least fixed point.
4. In the homogeneous direction equations of the forced rows, eliminate only
   a coefficient-one coordinate or a difference of two coordinates with
   coefficients `+1,-1`. A union structure records coordinate identifications
   and a distinguished zero component. Repeat until no elimination remains;
   explicitly check that every forced direction equation reduces to zero.
   The number of nonground components is the recorded dimension upper bound.

Step 2 is sound by nonnegativity and literal equality in the full vertex
space. Step 3 composes those sound implications. In step 4, every direction
of a feasible hive lies in every forced row's kernel, so the recorded
coordinate eliminations cannot discard an actual direction. Remaining
inequalities, further boundary constraints or infeasibility may lower the
actual dimension. No converse is inferred from this upper-bound calculation.
The closure is complete for the stated generated rule set; the code does not
claim that all universal zero-slack implications arise from one- or two-row
equal sums.

This is the argument implemented by the previously accepted campaign model.
The present wrapper changes neither the forcing rules nor the elimination
procedure. It replaces the historical provider-atlas comparison with direct
comparison against the already accepted complete tables.

## Full-coordinate and row-order correspondence

The model writes each original inequality as `A_r x+B_r b >= 0`, with
`b=(lambda,mu,nu)`. The new checker compares every coefficient of every
concatenated row `(B_r,A_r)` with the accepted structural checker's
`original_rows(n)`. Equality is literal, in the same order, including all
boundary coefficients; it is not merely equality after deleting boundary
coordinates, a row-space comparison, or a reordered row set. Thus bit `r` in
the accepted closed-row mask denotes precisely the original rhombus row used
by the structural certificate checker.

The checker also verifies every gap's side/bit convention against its exact
partition difference. At the shared lambda/nu corner, the two boundary
descriptions differ only by the original balance equation; the code checks
the full integer multiple of that equation explicitly. All other original
boundary and interior coefficients remain present. The complete model and
the selected `original_rows` function come from separately written accepted
campaign checkers, with their source hashes and unchanged function spans in
[FORCING-SOURCE-MAP.json](FORCING-SOURCE-MAP.json).

## Coverage, controls and provenance

Every accepted record is compared, including mask zero and the full mask.
The regenerated normalized records and accepted normalized records have
matching full-stream SHA-256 digests. Complete runs also compare the
dimension-upper-bound histograms and the numbers of distinct closures:
24,709 at rank 6 and 215,867 at rank 7. These figures count the finite table's
closures, not affine dimensions or LR-polynomial counts.

The controls check both complete coordinate constructions and eight original
mask cases. They deliberately reject changed closure/dimension records,
omissions, duplicate records, invalid or boolean masks, changed original row
ordering, changed gap bits, corrupt accepted data, duplicate JSON keys,
existing/overlapping outputs, absent output parents and optimized Python.
Real timeout and signal tests verify child and process-group cleanup. The
publication run passed 10 positive cases and 21 negative controls. The
calibration forecast was about 16.3 seconds for the two complete domains;
observed timings and exact tested-source bindings are in
[FORCING-VERIFICATION.json](FORCING-VERIFICATION.json).

`forcing_model.py` preserves the accepted `mask_model_v1.py` bytes except for
its import module name. `forcing_hive.py` selects the exact `interior_points`,
`rhombus_terms` and `hive_linear_system` functions from the existing public
`slr_ehrhart/hive.py`. This avoids loading unrelated APIs. `forcing_rows.py`
preserves the exact `original_rows` body and decorator from the accepted
structural checker. The new wrapper supplies source authentication, direct
table comparison and bounded portable execution; `forcing_controls.py`
supplies the bounded failure fixtures. No returned provider code is imported
or executed, and reuse of these accepted implementations is not represented
as a new blind mathematical derivation.

For the larger structural mask theorem, this command closes only the finite
F025 forcing-table premise. The normal-cycle theorem, boundary feasibility,
actual affine-hull certificates, normal/correction arithmetic and other
analytic or inherited premises retain the distinct scopes stated by their
own verifiers and proofs.
