# Constructive rank-six hive closure API

`constructive_hive_closure.py` takes **zero-based physical rhombus IDs 0..44** in the literal certificate/atlas row order. It never chooses a representative of the atlas's 42 interior-normal labels. It computes exact forward closure from all 103 positive identities, then exact ranks in the original ten interior coordinates. A branch is reported as dependent, excluded by a closure rank increase, or retained and independent.

First run the included independent `verify_closure.py` on
`CLOSURE-CERTIFICATE.json` and the parent directory's `atlas.json`. It checks
the complete 103-identity proof in about five seconds with Python 3.11+ and
its standard library. It produces `RESULT.json` and the separate minimum-test
input `EXHAUSTION.txt` in a fresh output directory. The API requires that
passing receipt, pins the certificate SHA-256, and checks the atlas's complete
physical row ordering. Loading JSON alone does not replay the RUP proof.
The certificate is inert data; the verifier and API are independent campaign
implementations. [The geometric explanation](../../../results/rank-six-positivity/GEOMETRY.md)
states the exact theorem and proof.

From this directory, with fresh writable paths outside the source tree:

```sh
python3 -B verify_closure.py --certificate CLOSURE-CERTIFICATE.json \
  --atlas ../atlas.json --out /path/to/fresh-verification-directory
python3 -B constructive_hive_closure.py --certificate CLOSURE-CERTIFICATE.json \
  --atlas ../atlas.json \
  --verification-receipt /path/to/fresh-verification-directory/RESULT.json \
  --physical-rows 14,12,16,17,15,36,44,7,2 --out /path/to/branch.json
```

The corresponding Python API is `load_verified_certificate(certificate, atlas, receipt)` followed by `analyze_branch(data, physical_rows, expand_fractions=False)`. `forward_closure(data, physical_rows)` and `normal_rank(rows)` are also available. Passing `--expand-fractions` or `expand_fractions=True` adds exact pairs `[numerator, denominator]` for all 45 relaxation increments and perturbed slacks, the perturbed interior point, and its displacement. The default JSON retains the exact rational recipe: a right inverse `Y`, integral `y0` and `a`, common denominator `D`, `M_generic`, `tau`, and `epsilon`. It checks all increments and all 45 perturbed slacks exactly before returning.

For a retained branch, the result includes the sum of **all** supplied feasible height vectors tight on the selected rows, its exact tight-set check, an integral legalized full-height hive, and the public boundary convention

```text
mu_i     = h(i,0) - h(i-1,0)
lambda_j = h(0,j) - h(0,j-1)       (lambda is outer)
nu_j     = h(6-j,j) - h(7-j,j-1)
```

It applies `u=max(0,-mu_6)`, `v=max(0,-lambda_6,u-nu_6)`, and `h'=h+u*i+v*j-h(0,0)`, then checks all three partitions, the full trace `|lambda|=|mu|+|nu|`, and every original rhombus slack. The fixed-boundary interior lattice remains `Z^10`. The face has dimension `10-rank(N_closure)` and saturated affine lattice `xstar+ker_Z(N_closure)`. For rank nine, the API gives a primitive integer direction, both exact endpoints, the entire rational parameter interval, and its saturated length. For rank ten it reports a point **face** and makes no claim that its parent hive is a point. Other ranks retain the exact lattice equations without an unproved basis.

The complete minimum-six obstruction check additionally needs an installed
C++17 compiler, with no GMP dependency:

```sh
c++ -std=c++17 -O3 minimum_six.cpp -o /path/to/minimum-six
/path/to/minimum-six /path/to/fresh-verification-directory/EXHAUSTION.txt
```

This exhausts every seed of sizes zero through five (1,385,980 seeds). Use only
the input emitted by the successful closure verifier. The separate six-row
countermodel is checked by that verifier. The exhaustive native step took
about 0.61 seconds locally, in addition to compilation and closure checking.

The independently executed constructive integration check is:

```sh
python3 -B test_constructive_hive_closure.py \
  --certificate CLOSURE-CERTIFICATE.json \
  --atlas ../atlas.json \
  --verification-receipt /path/to/fresh-verification-directory/RESULT.json
```

It covers the source kit's retained nine-row branch, the six-row old-rule obstruction `{4,17,18,23,31,41}` with rank `6 -> 8`, dependent parallel physical rows `7,9` from the atlas, and a full-rank endpoint branch in the same positive-length parent edge. It independently reconstructs the exact right inverse, perturbation, and selected/off-selected slacks from the returned rational data.

This is an implementation of source-qualified Pro043 U04 geometry. U02 supplied the short positive identities; U03 supplied the closure/fiber and physical-branch controls; U04 supplied the legal-realization converse and the final six-versus-six identity with a finite closure certificate. The A54 quantitative field and whole rank-six positivity are separate incoming campaign results. This API neither proves whole rank-six positivity nor computes a whole LR count. Its existential construction concerns some legal integral boundary and some compatible positive generic refinement, including lower-dimensional parents; it does not certify every boundary or refinement.
