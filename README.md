# Littlewood–Richardson stretching: results and exact verification

This private working collection organizes mathematical results that may
support a future paper. Each result has a precise statement, proof and
standalone exact reproduction. Historical novelty and publication priority
remain unresolved; no public release or human peer review is implied.

The leading result is an infinite family of stretched Kostka/Littlewood–
Richardson polynomials with positive ordinary coefficients and an exact
integer threshold for Hurwitz stability. Let rho_m=(m,m-1,...,1). For
u,v>=0, u+v>0, and lambda the outer partition, set

    lambda=(u+v)rho_18, mu=(u+v)rho_17,
    nu=(7u+8v,6u+6v,5u+4v).

The stretching polynomial has degree 31 and 32 strictly positive ordinary
coefficients. Every u>=22v has at least two roots in the open right half-plane.
On the primitive slice (u,v)=(q-1,1), it is strictly Hurwitz stable exactly
for q=1,...,22 and unstable for every q>=23. The complete two-variable
polynomial has 528 strictly positive coefficients. See the
[cone theorem and proof](results/hurwitz-cone/README.md).

The simpler [R18 example](results/hurwitz-counterexample/README.md) is
K_((7t,6t,5t),(t^18)), with exactly two open-right-half-plane roots.
Thus universal Hurwitz stability cannot prove ordinary coefficient positivity.
These results do **not** refute KTT positivity.

Run every module with Python 3.11+ and its standard library:

```sh
python3 -B reproduce.py
```

No package installation, network access or original research checkout is
needed. The default command writes no files. The individual commands and
scope of each result are listed in [RESULTS.md](RESULTS.md).

The collection also contains [parabolic A3 certificates](results/parabolic-a3/README.md),
a [two-parameter linear/quadratic coefficient theorem](results/coefficient-cone/README.md),
and an [all-index obstruction to raw weight concavity](results/two-row-nonconcavity/README.md).
Each addresses a different part of the positivity problem; none establishes
all-rank positivity or a completed finite-box search.

[REFERENCES.md](REFERENCES.md) separates established antecedents from the
results here. [PROVENANCE.md](PROVENANCE.md) records discovery, verification,
AI assistance and source identities. Future results should add a focused
module with its exact statement and reproduction; proposals belong in the
catalog until their mathematical obligations are discharged. Public licensing,
authorship and release remain decisions for the repository owner.
