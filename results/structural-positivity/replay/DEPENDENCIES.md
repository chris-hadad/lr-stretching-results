# What proves each statement, and what the replay checks

Every polynomial uses ordinary ascending monomial coefficients and lambda as
the outer partition. The table separates a proved all-parameter identity from
its finite numerical premises. Historical count values are portable inputs;
checks of those values against a reconstructed polynomial do not independently
regenerate the underlying counts.

| Result or premise | Complete local argument and input | Replay coverage | Remaining dependency or limit |
|---|---|---|---|
| Suffix-sum LR lift, arbitrary positive weights | [Pro027 019](../proofs/pro027/019-UNEQUAL-WEIGHT-NONCENTRAL-POSITIVITY.md), sections 1 and 3; [root slope three](../proofs/root/SLOPE-THREE-PROOF.md), complete count derivation | Separate integer product recurrence versus polynomial cap formulas on a bounded profile roster | Classical skew-Schur product and two-variable extraction are analytic premises; this is a full count identity, not a new general hive-coordinate equivalence |
| Slope-two all-rank positivity, `n>=5` | Pro027 019, section 4, coefficientwise remainder and bound | Exact formulas and bounded complete character checks | The all-rank inequality is the proof; no finite rank panel replaces it. Prior degree is `n-2` |
| Slope-three all-rank positivity, `n>=6` | Root slope-three proof: profile minimum, coefficient ratio bounds, analytic `d>=21` range and required `d=4,...,20` cases | All 17 finite vectors, 221 ambient coefficient entries; explicit degree-three exception | Count formula credited to Pro027; root owns this stronger sign argument. Higher slopes and all two-row LR shapes remain open here |
| Weighted-GT degree, lattice and true-interior premises for gap three | [Weighted-GT interiors](proofs/WEIGHTED-GT-INTERIORS.md), sections 2–3, with [General height](proofs/GENERAL-HEIGHT.md), complete staircase proof | Strict positive degree-ten bases are reconstructed in the exact prior space | Dimension is proved using a strict point, not equation counting alone. Rassart polynomiality and rational Ehrhart reciprocity are external classical inputs |
| Complete gap-three eight-term count | [Pro027 001](../proofs/pro027/001-COMPLETE-GAP3-CLUSTERS.md), complete expansion and cap intersections; elementary interval and path-cancellation details in [Delta-two branching](proofs/DELTA-TWO-BRANCHING.md), sections 2–4 | No new enumeration of the full signed tableau count | The earlier gap-two positivity conclusion is not imported; only its fully stated elementary identities enter. The general gap-three count identity is broader than this positive family |
| Initial gap-three axis and quotient | [002](../proofs/pro027/002-QUOTIENT-LATTICE-AND-ZERO-GRADE.md), [003](../proofs/pro027/003-SHARP-AFFINE-THRESHOLD.md), [004](../proofs/pro027/004-UNBOUNDED-RANK6-POSITIVITY.md) | Reconstruct `P00,P10,P20`; derive `Q0` by exact division; preserve `W0` and its four negative coefficients | Full quotient polytope and cancellation arguments supply all-grade applicability. The `x=0` wall cannot be removed |
| Whole integer quadrant, axes and corner | [005](../proofs/pro027/005-COMPLETE-QUADRANT-AND-DUALITY.md), [006](../proofs/pro027/006-QUOTIENT-MOMENTS-AND-POSITIVE-CERTIFICATE.md), [008](../proofs/pro027/008-INITIAL-WALLS-AND-POSITIVE-DIFFERENCES.md) | All four parent vectors from 32 determining positive values, eight unused values; exact positive factors, hinge formulas, 169 finite moment controls, first and mixed differences | Full branching, determinant duality and the wall identities remain analytic. Both independent interpolation algorithms share the historical count inputs |
| Homogeneous gap-three cone and every zero-parameter boundary | [007](../proofs/pro027/007-HOMOGENEOUS-CONE-AND-BOUNDARIES.md), all five sections; factor formulas in 006 | All 40 joint coefficients, independent-width normalization, rectangle/segment/point boundary polynomial and complete staircase comparisons | The proof gives independent widths and saturated boundary inverse; a rational substitution into a quadrant theorem would not suffice |
| Four gap-three numerical bases | [data/gap-three.json](data/gap-three.json); accepted root aggregate `F2627-GAP3-AGGREGATE-001` and its preserved raw vectors, source hashes in SOURCE-MAP | Exactly 40 historical positive sites: 32 determining plus eight unused; all complete vectors and algebra checked afresh when run | Full root Jacobi–Trudi counter, signed query rosters and child receipts are not included or rerun. The data retain their historical numerical provenance |
| Full endpoint LR/table identity, actual dimension and codegree | [011](../proofs/pro027/011-COMPLETE-RANK10-CAP-RELEASE-FAMILY.md), complete tail construction, saturated chart and cap formula; [012](../proofs/pro027/012-INDEPENDENT-WHOLE-MODELS-AND-CHALLENGES.md), full models | Literal endpoint triples and seven strict grade-seven witnesses checked; polynomial degree 18 and every coefficient checked | Classical Hall adjunction/Pieri, network total unimodularity and Ehrhart reciprocity are analytic premises. Both implementations in the historical source are distinct from this algebra replay |
| Seven endpoint vectors, complete positive shells and sharp stabilization | [data/transport.json](data/transport.json); accepted root aggregate `F2627-TRANSPORT-AGGREGATE-001` and preserved raw vectors; proof 011 | Seven vectors, 133 positive coefficients, 108 positive nonconstant differences, 14 unused positive values and final shell identity | Seven grade-zero constants and roots `-1,...,-6` are proved premises. Full 189-group signed assignments at 98 positive nodes are not recounted |
| Homogeneous transport linear bound `e1>=5279u/360` | [Root transport proof](../proofs/root/TRANSPORT-CONE-LINEAR-COEFFICIENT.md), sections 1–5; seven exact endpoint coefficients above | Exact endpoint premise only | Complete cut-wall analysis, support-function/Minkowski equality and classical first-coefficient additivity are analytic. Higher mixed coefficients do not follow from endpoint interpolation |
| Transport `e16>0` corollary | Root transport proof, section 6, citing the complete two-normal quotient-lattice formula in Frontier025 proof 023 | Not regenerated by the endpoint replay | Existing accepted theorem retained in the parent catalog. Its separate BV source dependency is mapped below; it is not needed for endpoint positivity or the `e1` bound |

The historical root gap-three checker was separately written from the complete
mathematics and accepted numerical inputs. `exact.py` and `gap_algebra.py`
select its exact polynomial functions, with the campaign runtime wrapper and
filesystem dependencies removed. `reproduce.py` supplies a new reader adapter,
explicit identity checks, two-row product controls and transport replay. This
is reuse of an accepted verification implementation, not a new blind or
independent mathematical derivation. The two interpolation algorithms are
arithmetically separate and use the same data.

Pro027 originated the selected family arguments and count formulas. The root
supplied independent finite verification, the slope-three sign extension and
the homogeneous transport linear-bound proof. The arbitrary-height staircase
source is an earlier campaign-derived extension; its weighted variant is
credited to Pro024. Per Alexandersson's GT/reciprocity work, Alper Ferudun's
positivity/correction methods and classical Schur/Ehrhart theory remain
antecedents. See the repository [references](../../../REFERENCES.md) and
[provenance](../../../PROVENANCE.md). These family proofs do not use Ferudun's
rank-at-most-five theorem to assert positivity at their higher ranks. No
worldwide novelty or external human endorsement is claimed.

## External theory and exact source locators

The local arguments supply the special-family hypotheses. The following
established theory is cited, not independently reproved by a Python run:

- Rassart, *A polynomiality property for Littlewood–Richardson coefficients*,
  arXiv `math/0308101`: stretched-LR polynomiality.
- Rational Ehrhart–Macdonald reciprocity, for example Beck–Ehrenborg,
  arXiv `math/0504230`, as identified in the retained staircase proof.
- Classical Schur, Pieri, Hall-adjunction and Jacobi–Trudi identities. The
  selected Delta-two proof includes the elementary branching, three-letter
  interval and determinant cancellation used by the gap-three proof.
- Bernstein–McMullen multivariate Ehrhart polynomiality, as cited in Haase,
  Juhnke-Kubitzke, Sanyal and Theobald, *Mixed Ehrhart polynomials*, Theorem 2.1;
  the linear-coefficient additivity is also explicit in Böröczky–Ludwig,
  *Minkowski valuations on lattice polytopes*, Theorem 22 and Corollary 23.

The parent repository owns the live primary-reference audit. Source documents
and their quoted historical reference labels are preserved without silently
upgrading bibliographic or novelty claims.

The optional transport BV corollary's earlier mathematical source is research
`methods/frontier-025-2026-09-10/sources/PROOFS/023-SHORT-NORMAL-COEFFICIENT-POSITIVITY.md`.
Its hash is in SOURCE-MAP's `mapped_nonreplayed_dependencies`. That source is
not required to reproduce the endpoint vectors, nor included as if it had
been freshly checked in this module.

## Remaining structural packaging work

The full normal atlas and the other structural families remain in the parent
[structural catalog](../README.md), with their existing accepted scopes.
The normal atlas is **not** part of this small replay. Its exact next packaging
destination is a separate normal-certificate module under the parent structural
collection, starting from accepted root `F2627-NORMAL-AGGREGATE-002` and proofs
025–042. Reentry requires a complete manifest for all 34 rosters, 1,508,387
independent occurrences, 34,761 dependent occurrences, 127,467 incidences and
5,480 complete types; a standalone adapter must verify literal identities,
quotient lattices, Laurent values and every affected incidence from a clean
export. Those populations are not numbers of LR triples.

A normal-module cost must be priced prospectively from its actual full inputs
and work budget. Reusing the current aggregate's historical success would not
supply fresh reproduction. Untouched rank-thirteen/fourteen connected
quadruples are later science, not a packaging gap that this session may close.
The theorem's protected indices remain ambient `D_n-4,...,D_n`, not
necessarily the top five coefficients of every degenerate hive.

A complete historical-count replay for gap three or transportation is another
possible module extension. Its reentry condition is a compact approved export
of the full exact counters, every query/assignment identity and their
mathematical input dependencies, followed by prospectively budgeted clean
recounts and adverse-input checks. The current adapter is intentionally
specific about the historical input it trusts.
