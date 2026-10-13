# Formal verification: present status and exact obligations

The whole rank-six theorem is **not currently formalized in Lean, Coq or HOL**.
The proof package consists of a mathematical argument, exact finite certificates
and independent checking implementations. This page identifies what a complete
formalization would need to prove.

| Obligation | What must be connected, without an assumed conclusion |
| --- | --- |
| Original combinatorial object | The concrete LR coefficient equals the original hive lattice count, with its boundary convention and dilation |
| Coefficient interpretation | Polynomiality, actual degree, constant term, rational denominator clearing, empty and point cases |
| Local formula | The BV coefficient identity with the original quotient lattice and metric |
| Refined normal fan | Existence of a compatible original-ray simplicial refinement, including hidden affine equalities and lineality |
| Primitive balance | Surjectivity of lattice restriction, saturated kernels, normalized facet measures and exact quotient conormals |
| Realizability restriction | Every positive-weight cell has an actual physical-row branch whose universal closure has the required interior rank |
| Finite geometry | Complete original normal domains, complete universal cone, all branches and symmetry transports |
| Exact scalars | The scalar recurrence agrees with the mathematical BV constant, including full lattice numerators and exceptional characters |
| Certificate arithmetic | Every required rational inequality and its complete coverage, with a verified parser and computation-to-proof bridge |

A theorem that assumes the entire LR-to-certificate connection and proves only
nonnegativity of a weighted sum is useful as a lemma, but is not a formal proof
of the rank-six theorem. Likewise, a checksum verifier proves file identity
rather than the mathematical meaning or completeness of those files.

The strongest immediate finite target is now the
[103-identity closure certificate](GEOMETRY.md). It replaces an extreme-ray
completeness premise with positive identities, feasible heights and nine RUP
refutations. Their 6,488 additions and 45 complete formula transports are
already checked by an independent Python program. A formal version must also
prove the closure sandwich and formula interpretation, not merely accept a
Boolean checker result.

## Closed native formal evidence through G3

A concrete finite pilot has now landed. The attempted core Lean LRAT kernel
reduction was blocked by opaque platform operations and partial parsing.
A separate structurally recursive 45-bit mask/trie checker was proved sound;
closed-session audits report nine representative refutations, 6,488 additions,
166 feasible heights / 7,470 slacks and 103 row identities. These certify their
actual data and Boolean/algebraic predicates; the full hive interpretation and
geometric bridge are separate obligations.

The evidence labels distinguish **KERNEL** proofs using the standard axioms,
**NATIVE** compiled evaluation with its additional trust boundary, and **STATED**
soundness obligations. The earlier pilot audit reports 56 KERNEL / 9 NATIVE
components; the G3 audited run copies report 126 KERNEL / 14 STATED claims.
The latter counts concern those run copies, not wholesale adoption into the
maintained library. No current build was run for this public assessment.

Later closed-session work reports actual LR/hive, polyhedral and local-weight
components and a complete **rank-at-most-four kernel theorem** on the real LR
statement: polynomial agreement and uniqueness, actual dimension at most three,
constant one and strict coefficients for nonempty hives, and the zero empty
case. This is formal assurance progress, not new mathematical rank-four coverage.
The recorded rank-four audit reaches 32,424 constants with no own-sorry leaves
and standard axioms only. These are attributed native audit results; this public
package does not contain or freshly compile the full native formal library.

Whole rank six remains incomplete. Its assembly still reaches
`correction_identity` and `hbeta_c1` through `hbeta_c9` placeholders. The G3
`hbeta_c6_pkg` record was STATED with four named soundness premises:
`checkSup_sound`, `thetaField_isKernelField`, `thetaOKQ_sound` and
`betaThetaQ_sound`. The later support-checker proof below is progress on one
part of that route; G4 did not repin or adopt the old c6 package or compose a
whole-rank-six proof. Residue or unimodularity lemmas alone do not supply the
remaining field, soundness and coverage bridges.

## Closed G4: support soundness and conditional coverage

The native formalization program closed G4 on 12 October 2026. Its audited
library records `checkSup_sound_gen` as **KERNEL**, together with the original
`checkSup_sound` and `checkSup_sound_nine` statements. The generalized statement
has the fixed 42-by-10 representation and explicit normal, row independence,
index, source-list and lower-state hypotheses. The original bounded instance
retains Q<=9 and unimodularity. This is checker soundness under its stated
hypotheses, not arbitrary-input or all-rank positivity. The library census
reports fourteen own-sorry leaves remaining, including the ten assembly leaves.

The c5 arithmetic pilot was built and its measured arithmetic cost reproduced,
but `hbeta_c5_of_cov : CoverC5 -> Assembly.HBeta5` remains
**MODULO(CoverC5)**. Here MODULO(P) means a formal conditional result whose named
mathematical premise P remains unproved. The audit was explicitly partial:
complete roster coverage, roster/beta seams and whole-import memory checks
were not completed. This is neither unconditional c5 formalization nor full
independent certification of the entire pilot.

A separate coverage checker's original general soundness statements were
kernel-refuted and narrowed. The repairs require bounded key blocks, valid
45-bit masks and a matching image invariant; their soundness is still
**STATED (OPEN)**. Key/root invariant and composition bridges remain obligations.
Kernel evaluation of proxy chunks does not prove the checker meaning or full
roster coverage. Those refuted prototype statements are separate from the
published mathematical LR proof; no defect in that published proof follows.

Recorded chunk timings and partial-pilot measurements are distinct from a
whole-layer forecast; the key join and top walk remain unmeasured in Lean.
No completion time or whole-layer resource bound is established here.

This status uses frozen lab commit
`913e044b684b6926dc61188f78f92ffb3da76f98` and Lean commit
`c3c5ce923a366d682d704101a2d6577e3ef86021`. The source map records the exact native
statement/audit/source hashes. The whole rank-six assembly and rank-four assembly
are byte-unchanged from G3; the rank-four kernel result above is unchanged.
These are attributed native source reports. This public package neither
exports the complete native formal artifact nor freshly compiles or adopts it.
The [dated research record](../research-progress/README.md#qualified-native-research-and-formal-progress)
keeps native mathematical leads and their unproved hypotheses separate.

The original 45-row cone is another useful target: formalize exact
double description, the tight-face adjacency test and rational arithmetic,
then certify the 166-ray output. The included Python reconstruction takes
about three seconds and agrees exactly with independent Sage/PPL. The q1–q3
scalar calculation is also bounded once its projection recurrence is connected
to the analytic definition.

In parallel, formalize the support and balanced finite-sum lemmas with explicit
hypotheses and develop the saturated-lattice and geometric bridge. Every
remaining assumption must stay visible. A verified rational-inequality checker
would establish its finite predicate; it would still need the proof that its
parsed scalars are the required BV constants. Kernel checking must not be
described as covering unformalized analytic premises, unverified input parsing
or a trusted external computation.

The current project has no completed whole-rank-six formalization. The landed lower-rank and local components above reduce specific obligations, but a full estimate still requires the remaining bridge and soundness work. The present release makes the exact proof inspectable without promising a short completion timeline.

There is useful existing infrastructure: [mathlib's convex-cone library](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Geometry/Convex/Cone/Basic.html)
provides cone hulls, linear images and preimages, and the relevant cone
properties. Its terminology must be translated carefully: `Pointed` concerns
containing zero, while `Salient` captures the absence of opposite nonzero
directions. The manuscript's pointed cones use the latter geometric property.
This library evidence supports reuse of basic convex geometry; it does not
establish that the full Ehrhart, LR or BV bridge is already formalized.

The manuscript and verification guide state the present computer-assisted
assurance claim. No formal checker or proof-assistant dependency has been
silently treated as completed by this assessment.
