# Whole degree-seven LR positivity from six counts and an enclosed fourth interior

## Complete-object hypotheses

Let P(t)=sum_{k=0}^7 c_k t^k be the stretching polynomial of the entire nonempty LR fiber, with lambda outer and the original physical stretch t. Require a complete saturated integer hive chart, actual dimension seven established independently of fitted counts, and primitive inward normals of squared Euclidean norm at most six in that chart. The source-adopted complete two-cone theorem gives c5>0; intrinsic leading and second-leading positivity give c7,c6>0. Nonemptiness gives c0=1. Polynomiality and actual dimension give P(-j)=-I(j), where I(j) is the true relative-interior count in the same lattice. A coordinate upper bound, a selected subspace, or strictifying forced-zero rows is not a substitute for these hypotheses.

The source certificate collection's short-normal and lattice-index certificates (FR025-SHORT-NORMAL / ROOT-F025-MASS-INDEX) and their complete proofs supply the geometric protection. The strict-witness criterion from the initial chart construction, the complete row–hive map, and the full-affine-space verifier from the degree-five analysis supply the concrete chart and independent true-interior counting representation. Those source premises remain dependencies, not new theorems of the degree-seven analysis. The degree-six source collection retains the complete proof and data bodies; the degree-seven certificate records the exact reused sources.

Where a recorded tensor variant is used, the strict point and enclosure belong to the stored count_boundary hive. Its entire polynomial equals the original bare target by the explicit all-stretch tensor word. Actual dimension agrees because it is the polynomial degree, and reciprocity then identifies the scalar interior sequences. No unrecorded affine isomorphism between arbitrary tensor-related hives is asserted.

## An exact one-unknown coefficient space

Write A=P(1), B=P(2), C=P(3), U=I(1), V=I(2), W=I(3), and Z=I(4). Only the first six quantities are initially counted. Define the integral forms

    N1 = 105 + 252A - 42B + 4C + 420U - 126V + 28W,
    N2 = -490 + 270(A-U) - 27(B-V) + 2(C-W),
    N3 = -245 - 48A + 71B - 8C - 440U + 267V - 64W,
    N4 = 56 - 39(A-U) + 12(B-V) - (C-W),
    N5 = 70 - 27A + 2B + C + 85U - 54V + 17W,
    N6 = -20 + 15(A-U) - 6(B-V) + (C-W),
    N7 = -35 + 21A - 7B + C - 35U + 21V - 7W.

On the entire prior degree-at-most-seven polynomial space,

    420 c1  = N1 - 3Z,
    360 c2  = N2,
    720 c3  = N3 + 7Z,
    144 c4  = N4,
    720 c5  = N5 - 2Z,
    720 c6  = N6,
    5040 c7 = N7 + Z.

One derivation is interpolation on the eight distinct nodes -4,-3,-2,-1,0,1,2,3, with negative values supplied by reciprocity. This is an identity on a previously established polynomial space, not fitting six observations to a guessed degree. The producer uses exact Lagrange products; the independent checker uses rational Gaussian elimination of the full Vandermonde matrix and tests all eight monomials. Constants 105,-490,... in this linear test multiply c0.

The coefficient of the uncomputed Z is

    t(t^2-1)(t^2-4)(t^2-9)/5040
      = (t^7-14t^5+49t^3-36t)/5040.

It has both positive and negative ordinary terms. Dropping it, forcing Z=0, or pretending the six counts determine a full vector would be invalid.

## Complete sufficient sign criterion

Since Z and all N_j are integers, c5>0 and c7>0 imply

    L0 = max(0,1-N7) <= Z <= H0 = floor((N5-1)/2).

The integer unit decrement follows from N5-2Z>0; no unsupported real-to-integer rounding is used. N6>0 is independently required by the fixed even coefficient. If a complete finite proof supplies L<=Z<=H, intersect it with [L0,H0]. An inconsistent interval indicates a conflict among the premises or counts and gives no positivity certificate.

For the resulting endpoints l,h, the four unprotected coefficients are strictly positive whenever

    N1 - 3h > 0,
    N2 > 0,
    N3 + 7l > 0,
    N4 > 0.

Together with c0=1 and the separately protected c5,c6,c7, this proves strict positivity of every ordinary coefficient. Replacing the four strict inequalities by weak ones gives nonnegativity. A negative lower bound merely fails the sufficient criterion. A negative exact even coefficient, or a strictly negative coefficient upper bound, establishes negativity of an entire LR coefficient at this scope. A formal polynomial or non-LR polytope control remains explicitly auxiliary.

The fixed coefficient lattices also give c5>=1/720, c6>=1/720 and c7>=1/5040 from their strict signs. Sharper lower bounds are taken only from actually verified integer forms; no volume estimate is invented.

## Finite lower and upper proofs for the fourth interior

In the checked actual seven-dimensional chart, the complete fourth-interior integer system has rows

    4*c_r + a_r*x >= 1  if a_r is nonzero,
    4*c_r >= 0          if a_r is zero.

All spatial coefficients and the original saturated lattice remain unchanged. Every nonconstant defining row is strict, including redundant rows; a valid nonconstant row cannot vanish at an ambient interior point. Forced zero rows remain equalities because the complete affine hull has already been identified and verified.

The producer derives finite coordinate intervals by necessary integer inequalities: maximize the other terms of a defining row over the current intervals, isolate one coordinate, and round inward. Every deduction names the original row, coordinate and integer endpoint. The separate checker verifies the endpoint using two multiplication/comparison inequalities rather than the producer's floor division. Contradictory intervals or negative maximal row value prove an empty node.

A remaining finite box has upper cardinality equal to the product of its integer side lengths. If the minimum of every original row over that WHOLE box is nonnegative, every point of the box is feasible and its full cardinality is also a lower bound. Otherwise its lower contribution is zero. A branch splits one finite coordinate interval into the two exhaustive, disjoint integer intervals [lo, mid] and [mid+1, hi], with proofs for BOTH children. Necessary propagation may remove only infeasible points, so summing child bounds remains valid. No uncovered branch or work-limit refusal is declared empty.

The sum of leaf lower cardinalities is a proved lower bound on the complete I(4); the sum of upper cardinalities is a proved upper bound. Equality, including a zero enclosure, gives an exact count; a nonzero interval is not assumed sharp. The search stops when the interval is sufficient for signs, a declared node/time cap is reached, or no uncertain box remains. The checker validates all nodes, exact split coverage, every deduction and every leaf, without invoking a count/search oracle.

This extends the degree-six analysis's upper-cover implementation to complete two-sided enclosures. The generic coefficient duality and interpolation principles are inherited. The concrete degree-seven identities, checked whole-object application and adaptive fourth-interior enclosure are the implementation and mathematical synthesis developed here.

## Verification and limits

Every consequential numerical value comes from two complete counting models: the homogeneous hive integer system and the independent semistandard/ballot-row recurrence with the exact row–hive thresholds. All geometry and every raw request/response are independently rebound to the same bare triple, physical grade and saturated lattice. The interval proof is a direct geometric cardinality certificate, not a mislabeled second numerical I(4) computation.

The six-count proof leaves an unknown Z unless a verified enclosure collapses. It generally does not reconstruct a full coefficient vector and needs no interpolation holdouts. A separate full-vector baseline genuinely counts I(4), retains the full degree-seven space, saves every vector before comparison/holds, and uses the two positive unused grades 4 and 5. Reserved grade 4 is a closed count, distinct from the negative determining node -4 represented by I(4).

The complete production disposition and original-key coverage are separate evidence. A passed pilot or a completed shard is not a complete original-box proof. Any case without a complete sign certificate remains unresolved.
