# Computational verification summary

This summary describes the independently checked computational evidence.
Source versions and exact result hashes are recorded in the tooling source
map. These are the recorded checks, not a claim of a new execution.

## Complete clipped rank-eight family

The entire three-cut LR family on `0<=M<=S<=2M` has a degree-at-most-21
bivariate polynomial in `u=2M-S`, `v=S-M`. All 253 ordinary bivariate
coefficients are strictly positive. Therefore every nonzero supported
parameter has a full positive stretching polynomial, including all boundary
rays. The origin has the constant polynomial one. This closes the actual
clipped family, including the previous M=1,S=2 degree-21 uncertainty.

The complete LR map and saturated-lattice/degree premises are given in the complete tableau-map proof. RANK8-AGGREGATION.md and RANK8-POLYNOMIALITY.md derive the entire
count and its single polynomial on the closed cone. An independent column
transfer agrees at all 253 poised sites and four unused positive sites.
The M=1,S=2 vector is independently reconstructed from those counts; all 22
coefficients are positive, with c1=19208731/1956240 and roots -1 through -11.
Twelve old sites, 1,678 full-parent tableaux and two fresh bare-LR calls agree.
The exact certificate is science/results/FRI-R8-CERTIFICATE-001.json.
No whole-rank or beyond-S=2M claim follows.
