# Five retained heights for the entire rank-six hive

For every integral LR boundary of ordinary rank at most six, all 45 original
rhombus inequalities can be evaluated with two private polygons, one private
interval and five retained heights. Each polygon count takes at most six
arithmetic sums. The complete real projection has 229 labelled affine
inequality occurrences, and every integral projected point has an original
integral lift. The original-coordinate primal graph has treewidth exactly five.

These are exact representation theorems. They preserve empty fibers, ties,
strict once-only shifts and count residues. Positivity of the private factors
does not prove positivity of a moving weighted sum. The separate
[whole-rank-six theorem](../rank-six-positivity/README.md) establishes the
ordinary coefficient signs by its own certificate.

Read [the complete proof and coordinate conventions](PROOF.md). The small
stdlib checker exercises the six-branch formula, projection and constructive
lift, every original first-failure field, and the width certificate:

```sh
python3 -B results/five-height-hives/reproduce.py
```

Its finite controls supplement the symbolic proof. They do not enumerate all
boundaries or independently certify the global coefficient theorem.

The five-height factorization and kernel closure were developed in the A53
mathematical work, building on the prior three-corner elimination. The complete
229-comparison projection and lifting statement were completed in A54. The
source map records exact inherited source bytes and the editorial changes.

The companion [no-additive-selector result](NO-ADDITIVE-SECTION.md) proves that
a global additive or affine original-hive selector does not exist on the
displayed rank-three control cone, although two piecewise integral charts
suffice there. It explains why an integral lift need not be globally linear.

[All results](../../RESULTS.md) · [Rank-six proof](../rank-six-positivity/README.md)
