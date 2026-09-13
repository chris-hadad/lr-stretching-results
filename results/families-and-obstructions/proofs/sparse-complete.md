# Completion of the exact positive-R two-support grammar

This certificate completes the earlier sparse-constructor evidence without
changing the enumeration or its domain. The complete-count and active-degree
arguments are in [the constructor proof](sparse-constructor.md) and
[the nonnegative-multiplicity lemma](sparse-nonnegative-parameters.md).
The earlier completion includes a 23-row tail.

## Exact population and all-stretch premises

The finite grammar has n=5 or 6 cuts, two nonempty support masks covering every
cut, strictly positive integral R, the explicit dominance conditions making
theta a partition, and direct outer size at most 30. Canonicalization uses only
inner exchange and common positive dilation. It produces 5,861 keys from the
previously authenticated 19,013 parameter tuples. This is not all rank 6/7 LR
triples or the entire original box.

The complete enumeration and certificates partition the keys into
1,848 infeasible positive-stretch zero cases,2,439 nonempty intrinsic-degree
at-most-two cases,960 Horn products of rank-at-most-five children with proved positivity,
and 614 initially unresolved nonempty polynomials. The selected 64 of those 614 were completed in two earlier calculations.
The continuation input removes precisely those 64 keys, retaining the complete
ordered 550 remainder and original residual indices. The six original source
hashes, exact subtraction, representatives and all degrees are independently
checked; no row is substituted.

For every one of the 550, verify_inputs.py reconstructs the full interval edge
roster from the two supports, the direct bare LR triple and canonical identity,
dominance, balance and size. It checks the nonnegative integral flow witness.
Every edge is accounted for either by a positive/residual-cycle witness or by
a closed balanced cut proving it is identically zero. Rational elimination
independently checks the rank of the complete active interval matrix.
All 550 are feasible, primitive, degree 3 through 8, with 171 rank-six and 379
rank-seven keys. This is their prior intrinsic-degree certificate, independent
of the Normaliz dimension or of fitting LR values.

The complete-count identity is

    c^(t theta)_(t eta1,t eta2) = #{x>=0 integral : A_m x=tR}.

The consecutive-ones interval matrix is totally unimodular. Its nonempty
fibers are bounded integral polytopes in their saturated relative lattices.
The positive-active-edge averaging argument excludes additional hidden affine
equalities. Hence each full count has exact ordinary degree d and P(0)=1.
These statements precede the new native interpolation; they do not follow
from an observed coefficient-array length.

## Complete two-model verification

Every bare triple received a new full Normaliz hive polynomial, required to
have period 1, dimension equal to its independently certified d, all d+1
exact rational coefficients, constant 1 and positive leading coefficient.
Its independent LR/tableau count batch supplied t=1,...,d+2. The producer
uses P(0)=1 with only t=1,...,d for Newton determination. The two remaining
sites d+1,d+2 are unused holdouts. All coefficients and every holdout agree.

The archival verifier independently uses the full Lagrange basis, rather than
the producer's Newton conversion. It checks every row and source index, exact
request, response hash, complete vector, determining value, unused check, and
successful execution record. This verifies recorded calculations without
rerunning the counts. All 550 rows pass, with no partial, invalid, uncomputed
or ordinary-negative row.

The new vectors contain 3,649 strictly positive ordinary coefficients, minimum
1/40320. They use 4,199 measured positive-stretch LR values plus 550 theorem
values at zero, with 1,100 unused holdouts among the measured values.
The calculation used 1,101 commands: version queries,550 polynomial calls
and 550 LR batches. The 2+550+4,199=4,751 recorded units were below the 4,800
limit; aggregate time was 334.2176997670322 seconds, below 900. Each computation
had a 60-second limit; the first eight count commands had zero failures and
no row was retried. All 1,101 execution records show cleanup, the overall exit
was 0, and all 1,102 recorded processes had ended.

## Precise closure statement

Together with the previously verified selected 64, all 614 original nonempty residual
polynomials are independently verified. The 5,861-key grammar therefore has a
complete coefficient-nonnegative disposition: 1,848 infeasible positive-stretch
zero cases,3,399 cases covered by proofs and 614 full verified nonempty polynomials.
For infeasible triples the positive-stretch zero-polynomial convention remains
distinct from the formal t=0 count 1; no false interpolation through that
discontinuity is used. Common dilation preserves every ordinary sign and
accounts for the original nonprimitive parameter representatives.

The 614 verified vectors have 4,276 strictly positive coefficients and 4,890
measured LR values in total across the original distinct attempts. Their
combined minimum remains the selected panel's1/79833600. Earlier failed or
partial attempts remain immutable historical records; this new completion
does not rewrite their outcomes.

There is no ordinary-negative example and no additive original-box coverage
increment. Zero-coordinate R, more than two supports, other ranks/sizes, other
constructions and generic rank-six/seven positivity remain outside the theorem.
