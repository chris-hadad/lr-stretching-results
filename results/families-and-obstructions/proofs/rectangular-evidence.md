# Rectangular nonvanishing: source values and a current check

The [complete original count result](../data/rectangular-nonvanishing.json)
records the three-matrix nonvanishing values 20 for a 2-by-3 matrix shape
and 266 for a 3-by-4 shape at their original primitive grade one. It also
contains all four 1-by-2 controls at grades zero through three: 1, 3, 6, 10.
This is a byte-preserved historical result, not a new execution receipt.

## Historical execution

The source attempt `A002-RECTANGULAR-NONVANISHING-002` has a successful
runtime exit and adapter return in the original research archive. The runtime
receipt's SHA-256 is
`07791831e722635214db149e6e618275b86cfede3415716466debef14db517c2`;
the result's SHA-256 is
`42f2acf869a670096cd21f76c6ec98e27c444d5f647bfb0195d320292b34b698`.
Those operational files are retained there and are not required inputs for
this repository's current counter. The relocated source proof now links here
instead of offering a nonexistent relative path to those files.

## Reproduce these scalar values

From the repository root, using the maintained exact counter:

```sh
PYTHONPATH=tooling python3 -B -c 'from slr_ehrhart import rectangular_matrix_invariant_count as c; values = [c(1, 2, 3, t) for t in range(4)] + [c(2, 3, 3, 1), c(3, 4, 3, 1)]; assert values == [1, 3, 6, 10, 20, 266]; print(values)'
```

The [whole LR bridge](rectangular-bridge.md) and
[canonical/codegree argument](rectangular-canonical.md) supply their own
geometric premises. A successful scalar check verifies these values; it
does not reprove either argument or compute a general rectangular polynomial.
The new edition's actual execution is listed in
[PUBLICATION-CHECKS.md](../../../PUBLICATION-CHECKS.md).
