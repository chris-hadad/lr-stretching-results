# Higher coefficients need not be concave in the weights

For k>=2 and C>=(k+1)x, the two-row Kostka family with fixed shape (C,C)
and weights beta(x)=(C-kx,C-x,x^(k+1)) has the exact stretch

    K_(t(C,C),t beta(x)) = binom(xt+k,k).

Its coefficient of t^j is e_j(1,1/2,...,1/k)x^j. Consequently every j>=2
admits a strict midpoint failure of concavity in the weights, including
examples whose weights are all positive. All ordinary coefficients of each
polynomial remain nonnegative. Rooted-coefficient concavity and monotonicity
under balancing are different statements and are not refuted.

Read [PROOF.md](PROOF.md) for the full argument, an explicit ordinary LR
embedding, and the general two-row skew coefficient formula with its correct
zero-weight and endpoint terms.

```sh
python3 -B two_row.py
```

This standard-library program compares two independent counting formulas,
the symbolic coefficient formula, harmonic quadratic formula, 90 exact
nonconcavity gaps and endpoint fixtures. It writes no files. The proof gives
the all-k conclusion; finite controls verify the implementation. Novelty
remains unestablished; see the repository's provenance and references.
