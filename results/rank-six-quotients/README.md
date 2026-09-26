# Entire stabilized quotients of rank-at-most-six hives

Let b and a be feasible integral LR boundaries whose common padded ordinary
rank is at most six. Let the entire direction hive H_a have positive actual
dimension. After stabilization, project the entire parent hive along the
linear space parallel to H_a and use the full saturated quotient lattice.
Every ordinary coefficient of the quotient count is strictly positive through
its actual degree; a point quotient has polynomial one.

The [proof](PROOF.md) defines this object, proves polynomiality in the original
stretch, and transfers the parent face-volume bounds without losing lattice
indices, initially empty integer fibers, or lower-dimensional cases. These
quotients are not assigned an ordinary LR rank. A selected face or an early
unstabilized projection is not the object in this theorem.

The accepted quantitative bounds also give the following historical explicit
parent-tail consequence along any whole segment direction a. If A=|lambda_b|
and A_a=|lambda_a|, every integer

    m >= 22528 A+2+2047(10(A+(22528 A+1)A_a)+1)^10

is sufficient for strict positivity through the actual degree of the entire
parent H_(b+m a). This intentionally loose sufficient bound is retained as a
quantitative corollary. The later [whole-rank-six theorem](../rank-six-positivity/README.md)
separately protects every feasible initial parent, so no such large m is now
needed merely to establish positivity.

This module is an analytic corollary of the complete rank-six coefficient
bounds. Its finite-certificate reproduction is supplied by the parent theorem's
modules; it introduces no independent certificate or quotient enumeration.
The stabilization and saturated transfer build on Pro028 and Pro031, with the
segment-quotient linear coefficient completed by A17's global c2 bound. The
source map records the accepted source statements; curation is not external
peer review or a worldwide-priority claim.

[All results](../../RESULTS.md) · [Main page](../../README.md) · [Tools](../../tooling/README.md)
