# A layered triangle family at unbounded ordinary rank

Let r>=3, b>=1 and A>=(r-3)b be integers. The whole original LR construction
with positive layers obtained from (A,b,...,b), with r copies of b, has
nonnegative ordinary stretching coefficients. If A,b>0, every coefficient
through its actual degree 3r+1 is strictly positive, and its ordinary rank is
2r+4. At r=3,A=0, delete the zero layer first: the ordinary rank is eight and
the degree is seven; higher nominal coefficients vanish.

[The proof](PROOF.md) defines the original outer/inner/content partitions and
both directions of the tableau/flow map. The three colors are a content
alphabet, not the ordinary rank. The family is feasible throughout.

The infinite theorem uses four adjoining parameter regions:

| Region | Uniform proof | Complete finite remainder |
| --- | --- | --- |
| A>=rb | Every r>=1 | None |
| (r-1)b<=A<=rb | r>=6 | r=3,4,5 |
| (r-2)b<=A<=(r-1)b | r>=15 | r=3,...,14 |
| (r-3)b<=A<=(r-2)b | r>=44 | r=3,...,43 |

The included second-strip controls also retain r=2 and its degree-four rank
drop. The complete three-strip fields contain 136,332 coefficient slots and
342 unused whole-count holdouts. The last strip alone does not prove the
whole half-line. Complete mixed monomial fields, not positive sampled counts,
close the finite ranges after the total degree has been proved.

[Verification instructions](VERIFICATION.md) give the portable checker and
its exact limits. [Analytic dependencies](proofs/README.md) retain the critical
parent expansion and both earlier strip arguments. The result is credited to
the Pro042 mathematical work and A53's independent original-count verification
and audit; discrete Rodrigues/orthogonality and Ehrhart methods are classical.
These are inherited accepted proofs, with source bytes recorded in the source
map. The publication curation itself is not a new independent mathematical
verification or an external peer review.

This theorem concerns the displayed complete LR construction. It proves no
claim for arbitrary layered widths, deeper balanced regions, larger alphabets,
coefficientwise width monotonicity on the second/third strips, arbitrary LR
parents, or unrestricted KTT.

[All results](../../RESULTS.md) · [Main page](../../README.md) · [Tools](../../tooling/README.md)
