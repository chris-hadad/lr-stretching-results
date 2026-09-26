# Count-preserving gap caps at every rank

For every legal balanced LR triple, determinant normalization and the explicit
prefix-dependent cap preserve the **entire stretching polynomial** and do not
increase ordinary rank. Negative deficit prefixes give the zero polynomial;
a zero proper prefix factors the whole count into smaller ordinary LR factors.
The [original cap proof](CAP-PROOF.md) retains every Weyl term, rho offset and
support wall. It asserts no affine isomorphism of hive polytopes.

If H is the maximum deficit prefix and H>0, the capped outer area satisfies

    |lambda_capped| <= 2 floor(n^2/2) H.

The bound is sharp for legal cap images. After division by H the full rational
parameter domain has a cover by at most (n-1)F_(n+1) closed rational polyhedra,
with F_1=F_2=1. [All-rank proof](AREA-BOUND.md). Rank six gives 36H and 65 pieces.
Empty and overlapping pieces are allowed; these are not coefficient chambers.

Rational denominators remain unbounded. This is not a reduction to integer
outer area at most36 or any finite global search. The result is a whole-count
normalization theorem, not unrestricted KTT positivity.

```sh
python3 -B results/gap-cap/reproduce.py
```

The small proposed replay reconstructs all 65 rank-six pieces and the full
binary-cube bound. Its finite checks supplement the written all-rank proofs.
The cap is credited to Pro031; the sharp all-rank area/cover proof to the
subsequent campaign derivation. No provider program is executed.

[All results](../../RESULTS.md) · [Main page](../../README.md) · [Tools](../../tooling/README.md)
