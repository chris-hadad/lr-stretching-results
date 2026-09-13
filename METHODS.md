# How the result was found and checked

The finite-box result began as a search for a negative ordinary coefficient.
Repeated positive examples did not justify a theorem. The useful change was
to make the original bounded domain explicit and attach a sufficient proof
to every input. This account explains the mathematical development, the
computational responsibilities and the limitations of the resulting evidence.

## From search to a finite proof

1. **Fix the original question.** Use λ as the outer partition, remove trailing
   zero parts, and retain all legal balanced triples through length seven and
   outer area thirty. Separate trivial zero/one cases and Ferudun's all-size
   theorem through length five. The remaining original rank-six/seven census
   has 651,229,702 identities under its documented enumeration conventions.
2. **Reduce entire counting problems.** Delete empty skew rows, clip inactive
   gaps, apply tensor/determinant symmetries and positive dilation, and use
   proper Horn factorization with its hypotheses. Tableau bijections and
   representation identities justify these operations for every stretch;
   matching a few counts is insufficient. Keep each original preimage and scale.
3. **Prove the actual geometry.** Reconstruct all hive inequalities and the
   corresponding tableau system, retain the full integer lattice, and certify
   the actual affine hull before counting relative-interior points. A chart's
   number of coordinates can exceed its actual dimension.
4. **Use expensive counts where they matter.** Known high-coefficient signs
   and reciprocity let a small determining set constrain the remaining
   coefficients. Exact interpolation often leaves one unknown interior count.
   Rigorous lower and upper bounds suffice when every possible value in the
   interval makes all remaining coefficients nonnegative.
5. **Change methods for the difficult remainder.** The final 495 targets use
   complete polynomial vectors and unused positive checks. The proof does
   not force interval completion onto cases where full counting is clearer.
6. **Close the literal domain.** Join each required proof to its exact original
   triple, reductions, geometry and count records. Verify the complete expected
   identity sets and their complements, including earlier dependencies.
   An empty final list or equal cardinalities alone would not establish this.

The [research note](papers/finite-box.md) explains why these steps imply the
theorem. The [detailed proof](results/finite-box/PROOF.md) supplies the formulas,
exact population table and links into preserved source proofs.

## Failures that changed the verification

| Observation | Why it matters mathematically | Resolution and retained limit |
|---|---|---|
| A simple quintic linear-coefficient sufficient bound could be negative for a positive polynomial | A failed lower bound is not a negative coefficient | Retain the third interior term and verify the stronger exact identity |
| Strictifying an oversized affine chart can count the wrong interior | Reciprocity requires the true relative interior and actual dimension | Verify forced equalities, a saturated integer inverse and a strict witness in the final hull |
| Fractional split syntax could skip an integer point in a supplied upper-bound tree | An incomplete partition cannot certify a global upper bound | The independent checker requires integral splits and checks both children; retained trees pass |
| Some unused checks at large grades were unnecessarily expensive | A timeout supplies no value and cannot be counted as agreement | Keep every original determining node; use a frozen first-two-unused-positive-grades rule for 40 parents and recount all 80 replacements; original larger-grade observations remain supplemental |
| Aggregation and metadata assembly timed out despite completed numerical work | Completed counts are not a completed identity join | Preserve the failed attempts; authenticate the permitted caching adaptations and finish the exact union under separately stated metadata limits |
| An auxiliary gap-three polynomial has negative ordinary coefficients while its parent is positive | Auxiliary negativity need not survive the full LR count | Publish both objects at their precise scopes; no counterexample is inferred |

The unused-check change was selected from node locations, without choosing
grades by favorable values. The 1,854 retained original numerical sites and
80 replacements were independently counted. Expected polynomial values at
new grades are labeled predictions until recounted; old observations are not
rewritten. The [verification record](results/finite-box/REPLAY.json) and
[adaptation account](results/finite-box/code/ADAPTATIONS.md) bind the actual
implementations and earlier incomplete attempts.

## Who did what, and what “independent” means here

Chris Hadad chose the research objectives, supplied resources, continued
external research sessions and steered the work. GPT 6 Pro proposed much of
the mathematics, proof development, data and source programs. Codex developed
and ran separate checkers, rederived consequential arguments, organized the
evidence and integrated the results. Earlier Codex and Claude/Fable research
supplied specific geometric, counting and certificate prerequisites. The
[provenance account](PROVENANCE.md) retains those result-specific attributions.

For the finite box, verifiers saw the proposed proofs and numerical data;
this is not described as blind verification. Independently written programs,
different complete counting representations and fresh AI reasoning sessions
provide different checks. They share some mathematical premises and source
identities. They are not independent human peer review. The isolated earlier
Hurwitz example has a separately documented bare-triple blind reconstruction;
that independence claim does not transfer to every later module.

## What a reader can inspect

The public-content proposal includes mathematical source proofs, complete
selected certificates and numerical inputs, independently written code,
source maps, reproduction instructions, failure explanations and attribution.
It excludes private correspondence, operator conversations, credentials and
unrelated account or workflow state. Source filenames and old receipt labels
are retained where needed to make the audit trail unambiguous; a reader need
not learn the internal session vocabulary to follow the note or run the tools.

The portable finite-box route regenerates its required finite premises. It
still cites universal theorems, including Ferudun's result, rather than
claiming to reproduce all their earlier external generators. Some broader
structural certificates are currently available as source proofs and scoped
records rather than complete standalone execution packages. Their dependency
maps identify that remaining work. No missing premise becomes a theorem merely
because a program prints success.

External mathematical review, novelty assessment and FrontierMath's treatment
of the result remain open. The strongest immediate contribution is a specific,
checkable result with methods other researchers can scrutinize and extend.
