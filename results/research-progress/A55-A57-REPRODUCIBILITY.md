# A55–A57 complete dependency closures and reproduction

This package supplies the complete A55 initial-split proof, A56 five-width ray certificate, Pro045 U11 construction used by A57, its precise two-sided inherited-metric transfer, and the new rank-seven p=3 original parent and common-shift certificates. The original all-rank/component claim limits remain in the proofs. A positive extracted component leaves an unsigned residual; no complete c9/c10, whole-rank-seven or unrestricted KTT sign is claimed.

The initial-split checker performs literal interval-convolution DP recounts of the existing layered K3 parents through the accepted complete LR bridge, rebuilding every recorded parent vector and comparing every historically unused positive holdout, checks all 372 kernel cases and the entire negative fourth-range moment, then checks every one of the 125 width-fan rays. The exact C++ enumerator visits all 3,183,545 four-normal intersections. Its arithmetic uses only small integer determinants, not floating point. Python replays all 250 parent vectors / 4,886 historical determining values / 500 historical holdouts, independently extracts all 125 first coefficients and checks all 500 bounded-composition slice controls and six full compatible ray sums. These determining and holdout records retain their original roles; the replay creates no new unused evidence. Higher ray coefficients are finite controls and do not extend by first-coefficient linearity. Historical original-LR checks and their actual timeout limits remain data, and are not rerun by this package.

The A57 checkers retain every physical label and all original rows, the saturated interior-height lattices, each inherited Gram matrix, every collar induction record, all complete cofacets and all shared-shift margins. They replay every one of the 448 U11 faces at ranks 7–10; the all-rank quantifier comes from the complete symbolic induction in the proof. The p=3 scripts separately verify the entire strict rank-seven parent, all 48 nine-dimensional faces, complete balance/kernel and one generic compatible shift. All 41 old-boundary witnesses and six exact Farkas certificates are checked, with one source cell still unresolved on that old boundary. No optimizer is required and no new parent is constructed. The full p=3 BV pairing is the explicit simplex/valuation argument, not a new alpha-six scalar census.

Requirements: Python 3 standard library and a C++17 compiler. From the repository root, use a fresh output directory; scripts refuse overwriting result JSON. For example:

```sh
mkdir -p a55-a57-replay
c++ -std=c++17 -O2 results/research-progress/code/a55_a56/enumerate_width_rays.cpp -o a55-a57-replay/enumerate_width_rays
a55-a57-replay/enumerate_width_rays 5 a55-a57-replay/RAYS5-FRESH.json
python3 -B results/research-progress/code/a55_a56/check_initial_split.py --a55 --output a55-a57-replay/A55.json
python3 -B results/research-progress/code/a55_a56/check_initial_split.py --a56 --rays-replay a55-a57-replay/RAYS5-FRESH.json --output a55-a57-replay/A56.json
python3 -B results/research-progress/code/a55_a56/check_initial_split.py --global --output a55-a57-replay/A57-GLOBAL.json
python3 -B results/research-progress/code/a57/check_u11.py a55-a57-replay/u11
python3 -B results/research-progress/code/a57/check_p3_parent.py a55-a57-replay/p3-parent
python3 -B results/research-progress/code/a57/check_p3_component.py a55-a57-replay/p3-component
python3 -B results/research-progress/code/a57/check_fixed_boundary.py a55-a57-replay/fixed-boundary.json
```

The checkers operate solely on the exported proof/data/code package. They use no private filesystem, optimizer, LR backend, network, provider program or environment-specific service. The compiler and Python run one task at a time in the observed export replay. Every original/staged hash and mathematical transformation is in the closure provenance manifest. Compiler/interpreter identity, measured costs and fresh outputs belong to the separate verification handoff; this document does not substitute a prior green receipt for mathematical premises.

A57's existing public premise proofs are `results/structural-positivity/proofs/pro027/025-COMPLETE-REFINED-NORMAL-CYCLE.md`, `022-HIDDEN-STRATA-BY-DUAL-VALUATION.md` in that directory, and `results/rank-six-positivity/PROOF.md`. The exported U04 transfer retains its precise quotient-lattice and inherited-metric argument.
