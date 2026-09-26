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

There is a concrete Lean route using the standard library alone. In
[Lean v4.34.1's pinned LRAT checker](https://github.com/leanprover/lean4/blob/5045d0056413266e57c625dcd7c365b10e377c52/src/Std/Tactic/BVDecide/LRAT/Checker.lean),
`Std.Tactic.BVDecide.LRAT.check_sound` proves that a successful check establishes
the input CNF's unsatisfiability. An exporter would attach ordered unit/conflict
reason IDs to each of the existing RUP additions, embed exact CNF and proof
data, and discharge the check by kernel reduction. Variables and clause IDs
must follow that release's exact conventions. A useful pilot starts with one
complete representative, then the largest 4,531-addition representative.
No mathlib cache or external SAT solver is required for this finite step.

**This pilot has not been compiled or kernel-checked.** The release and API
were inspected, but no Lean toolchain was installed. Kernel reduction time and
memory remain unmeasured. A proof using compiled native evaluation has a
different trust boundary from kernel-only evaluation and must be labeled
accordingly. Even a successful CNF pilot would leave the geometric
interpretation and the LR/BV bridge to formalize.

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

The current project contains no existing whole-theorem formalization. A bounded
search of the current mathlib source inventory did not identify the required
Ehrhart/BV/LR modules; that is not proof that no relevant formal development
exists elsewhere. A full estimate therefore requires actual library and
dependency work. The present release should make the complete exact proof
inspectable without promising a short formalization timeline.

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
