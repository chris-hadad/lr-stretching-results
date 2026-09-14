# Complete rank-six c4 and c5 certificates

This module independently checks finite certificates proving nonnegativity of
the fourth and fifth ordinary coefficients of every stretched
Littlewood-Richardson polynomial of ordinary rank at most six. It includes all
areas and boundaries. For a nonempty hive, the coefficient is strictly positive
when its actual dimension reaches the coefficient index, and zero below it.

The complete theorem, lattice conventions and analytic dependencies are in
[PROOF.md](PROOF.md). Whole rank-six positivity remains open at the first three
ordinary coefficients outside the previously protected domains. This module
verifies supplied certificates; it does not search for their rational fields.

## Reproduce the complete finite proof

Requirements are Python 3.11 or later, a C++17 compiler, a POSIX system and the
GMP C++ development headers and libraries. The topology checker uses only the
C++ standard library and checked integer arithmetic; the local-value checker
uses GMP exact rationals. No original research checkout, network access or
provider program is required.

Choose an output directory that does not already exist, outside this source
directory. Its parent must exist. From this directory, run:

```sh
python3 -B verify.py --full --out /path/to/new-rank6-verification
```

When GMP is outside the compiler's default search paths, supply its paths.
The wrapper records each library directory in the executable runtime search path:

```sh
python3 -B verify.py --full --out /path/to/new-rank6-verification \
  --include-dir /path/to/gmp/include --library-dir /path/to/gmp/lib
```

The final result must be `PASS_COMPLETE_C4_C5_FINITE_CERTIFICATES` in
`RESULT.json`. The output retains every local primary value, input identity,
compiler log, process result and corruption-control result. A failed or
interrupted run retains its files and has no complete verdict. Use a fresh
directory for a later attempt.

A short diagnostic route is available:

```sh
python3 -B verify.py --quick --out /path/to/new-rank6-diagnostic
```

Its status is `PASS_QUICK_DIAGNOSTICS_NOT_THEOREM`: it checks the full rational
inequalities but only bounded geometry and local-value samples. Only `--full`
reconstructs every finite mathematical predicate. Each child has at most
120 seconds; the default cumulative child allowance is 1,300 seconds. Slower
hosts can use a larger `--child-seconds` allowance and a smaller `--batch-size`
(from 1 to 2,000). Topology stages also have an internal 110-second refusal.
Timeouts and handled termination signals stop and reap the active child.
Uncatchable termination or host loss cannot run cleanup; the output records
the child PID as soon as it is spawned.

## What is checked

| Predicate | c5 certificate | c4 certificate |
| --- | ---: | ---: |
| Original normal subsets, including dependent subsets | 850,668 | 5,245,786 |
| Independent original normal cones | 725,697 | 4,050,197 |
| Safe local lattice and metric types | 39,974 | 293,795 |
| Complete rational inequalities | 121,241 | 675,721 |
| Available functional coordinates | 102,990 | 606,205 |
| Nonzero integer matrix entries | 1,307,258 | 8,139,966 |
| Negative raw local types retained | 580 | 9,850 |

Both certificates have corrected margin at least `1/2000000`. Every local
constant is reconstructed from its literal original normals, with full image
lattices, primitive quotient factors, finite numerators and all face terms.
The topology checker independently rebuilds the 45 rhombi, 42 oriented normal
directions and six integral orthogonal actions, then every required assignment,
kernel and matrix row, including omitted zeros. High-index reuse keeps the
complete lattice embedding; Gram matrix and index alone are insufficient.

The compressed dataset is about 44.8 MB and expands to 229,617,456 bytes in
24 schema-defined mathematical files. [DATA.json](DATA.json) gives exact
sizes, hashes and binary layouts. These arrays contain no executable code.

## Measurements and provenance

Before standalone packaging, a fresh serial reconstruction of all 333,769 local
constants took 613.318 seconds of native child wall time on the campaign's
24 GiB Mac. Complete topology and matrix checks took 13.566 seconds of native
core time, with maximum observed native RSS about 283 MB. These are verification
measurements for this fixed dataset. Certificate discovery, mathematical proof
development and performance on another host are separate questions. The final
standalone run records its own compiler, outputs and wall times.

The rational fields and source arguments originated in the Pro028 research
return. The distributed computational cores and wrapper were independently
authored for verification. GMP arithmetic is shared with some original
calculations; the code, full reconstruction and exact source checks are
distinct, without a claim of independent human peer review.

Alper Ferudun's rank-five positivity theorem and correction methods are credited
foundations. The analytic local formula is due to Nicole Berline and Michele
Vergne. [PROOF.md](PROOF.md) supplies source links and the complete finite-to-
whole-hive implication. Software follows the repository's MIT license;
original research exposition and certificate data follow its CC BY 4.0 license.
GMP is an external dependency and is not redistributed here.

## Parser and process regressions

After a quick or full run, the bounded regression command checks truncated
headers, four real termination signals and both cleanup-entry signal races,
including observed child exit:

```sh
python3 -B test_controls.py --compiled-dir /path/to/completed-verification \
  --out /path/to/new-rank6-regressions
```
