# Exact completion of 23 previously unevaluated two-support triples

This is a new verification of precisely the initial two-support sample's selected indices 41 through 63.
The earlier attempts are unchanged. The mathematical premises are the complete
ordinary LR/interval-flow identity and complete active-edge dimension proof in
FRC/sparse/PROOF.md, together with its frozen source/NONNEGATIVE-M-LEMMA.md.
No additional theorem, parameter grammar or row selection is introduced here.

`input-provenance.json` authenticates the exact original selected file, full
parameter file, specified counting implementation and source dependencies. The new selected
file is precisely the 23 original entries with their original
indices attached. `attempt-001/parameters.json` extracts each original complete
representative certificate without changing any record. This directory contains
the exact input records; the parameter enumeration was not repeated.

`verify_inputs.py` checks each direct triple from its two support masks and
positive integral R, including dominance, partition conditions, balance, outer
size at most 30, primitive identity and equality to the frozen bare triple. It
reconstructs every interval edge and verifies the full nonnegative integral
flow. Every declared active edge has positive flow or a simple residual return
path; every remaining edge has the recorded closed balanced forced-zero cut.
These two sets partition all edges. Independent rational elimination on the
active interval matrix gives rank 5 in every row, with 13 active edges, hence
intrinsic dimension 8. All 23 original certificates pass; three require 11
forced-zero edge certificates in total.

The cited complete-count identity applies for every integer stretch t >= 0.
The interval matrix is totally unimodular and the nonempty fibers are bounded,
so their stretching counts are ordinary degree-eight Ehrhart polynomials.
The integral witness proves nonemptiness. Therefore P(0)=1 is a theorem value,
not an engine measurement, and the sites 0 through 8 determine the polynomial.

For each bare triple, a fresh full Normaliz hive polynomial has period 1,
dimension 8, nine exact coefficients, constant 1 and a positive leading term.
Independent LR/tableau values were freshly computed at t=1 through 10. The
Newton determining reconstruction uses only P(0)=1 and t=1 through 8; sites
9 and 10 remain unused holdouts. The archival verifier independently uses
Lagrange interpolation and compares all nine coefficients and both holdouts.
Every polynomial agrees exactly between the two models.

All 207 ordinary monomial coefficients are strictly positive. Their minimum
is 1/40320, attained as the degree-eight coefficient at original indices
41, 46, 47, 51, 52, 53, 54, 57 and 58. There are five distinct coefficient
vectors across these 23 different triples. No ordinary-negative result
appeared. The new results comprise 20 rank-six and 3 rank-seven triples.

The independent record check binds every original index to its local input
record. All 47 version/poly/LR-batch records match the exact ordered requests,
serialized arguments, response digests, retained primary values, complete
row vectors, source roster and source bytes. All calculations completed
successfully.

This completes the original selected 64-row panel together with the initial two-support certificate's verified
41 rows: 32 triples of each ordinary rank, 627 strictly positive ordinary
coefficients, 691 measured positive-stretch LR values, 64 proved P(0)=1
values and 128 unused holdouts. The combined minimum remains the initial sample's
1/79833600. The earlier resource-limited partial result remains recorded separately.

Only 64 of the 614 original canonical pre-count residuals now have complete
polynomial verification; the other 550 were not selected and remain open.
This changes the 23 selected rows from unrun partials to complete polynomial
verification. It proves no all-size, all-rank, whole-box or other grammar closure.
