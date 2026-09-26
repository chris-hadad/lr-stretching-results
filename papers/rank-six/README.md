# Rank-six coefficient positivity: paper and proof package

**[Read the 16-page preprint (PDF)](rank-six.pdf)** ·
**[Download the complete preprint source and small ancillary checks](rank-six-preprint-source.tar.gz)**

For every LR triple of partition length at most six, every ordinary stretching
coefficient is nonnegative. For a nonempty hive, every coefficient through its
actual degree is strictly positive. The paper includes all boundaries and
degree drops, the original saturated lattice, the complete normal-cycle proof,
the realizability criterion, every coefficient's finite premise, and the scalar
algorithms and contribution record.

It also proves a constructive legal-realization converse at every rank and
gives a 103-identity presentation of rank-six closure, with a small exact
certificate covering all physical-row subsets. [The geometric guide](../../results/rank-six-positivity/GEOMETRY.md)
explains these additional results and their executable witness interface.

## Source, build and verification

The editable sources are [rank-six.tex](rank-six.tex) and
[geometry-strengthening.tex](geometry-strengthening.tex). Both are required.
The bibliography is inline and all packages are standard LaTeX. Compile the
first file from their common directory using an installed LaTeX engine; the
publication build used isolated Tectonic 0.17.0 in cached, untrusted mode.

The source archive has the two TeX files at its root and small independent
checks under `anc/`. It contains no compiled PDF, logs, private outreach or
build intermediates. The ancillary README gives exact commands for the full
closure certificate, minimum-six exhaustion, constructive controls and complete
c6–c9 finite premises. The larger c1–c5 inputs remain in the separately
versioned numerical release.

[BUILD.json](BUILD.json) records the exact source members, archive/PDF hashes,
successful restored-source compilation, complete ancillary replay and all-page
visual QA. The final build has no TeX warnings and embeds its fonts. These
checks do not replace inspecting the PDF that arXiv itself processes at
submission.

## Status and review

This is a preprint prepared for independent mathematical verification. Complete
exact finite premises and three independent Astra mathematical review rounds
have passed. It is an exact computer-assisted proof, with shared classical
premises stated explicitly. External human peer review and whole-theorem
Lean/Coq/HOL formalization are not claimed.

Version: `rank-six-2026-09-25-v1`. The paper's repository links identify that
release. [Verification routes](../../results/rank-six-positivity/VERIFYING.md)
range from a few seconds for the geometry to complete scalar regeneration.
[Related work](../../results/rank-six-positivity/NOVELTY.md) credits Ferudun,
the classical hive and polynomiality theorems, and Berline–Vergne theory.

[Main result](../../results/rank-six-positivity/README.md) ·
[All results](../../RESULTS.md) · [Tools](../../tooling/README.md)
