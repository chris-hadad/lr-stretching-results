# Hidden affine strata from one complete dual valuation

The following identity establishes the hidden-cubic condition from the Berline–Vergne dual solid valuation and its ambient/subspace compatibility. It does not rely on a separate low-degree assertion whose full certificate was unavailable.

## Identity with the actual quotient lattice

Let L be a saturated rank-four coordinate lattice, with one rational positive-definite scalar product. Let u,v,w be independent rational covectors, taken primitive integral when their lattice directions are specified. Put H=ker(u). Let alpha_3(u,v,w) mean the complete BV constant of the tangent quotient dual to pos(u,v,w), in the projected lattice and induced metric. Let alpha_2(v|H,w|H) mean the complete constant of the restricted tangent quotient in the saturated lattice L intersect H. Primitive normalization of the restrictions is performed in that lattice, not guessed from their ambient coordinates.

Then

    alpha_2(v|H,w|H)
      = alpha_3(u,v,w)+alpha_3(-u,v,w).                 (1)

There is no extra lattice index multiplying either term.

To prove this, first quotient the common edge line ker(u,v,w). The dual space has rank three. The nonpointed normal cone

    sigma=R u+pos(v,w)

is the union of sigma_+=pos(u,v,w) and sigma_-=pos(-u,v,w). Their intersection pos(v,w) has smaller dimension. The BV dual SOLID valuation adds the two full-dimensional pieces and vanishes on that smaller-dimensional intersection. The polar of sigma lies in H and is exactly the two-dimensional tangent cone cut out there by v and w. Ambient/subspace compatibility of mu identifies its value with the restricted-cone value. This proves (1).

The lattice assertion is essential. A saturated kernel basis of u spans L intersect H. Since the common edge line lies inside H, first restricting to H and then quotienting that line gives the same projected lattice as the polar construction. Equivalently, restriction of integral covectors to a saturated subgroup has the expected integral image, not an arbitrary finite-index replacement. The Gram matrix on a kernel basis is retained and dualized when normal coordinates are used. Orthogonal projection of the lattice is not silently replaced by intersection with an orthogonal plane.

The primary references are Berline–Vergne, Local Euler–Maclaurin formula for polytopes, `arXiv:math/0507256v3` (28 July 2006), Proposition13, Definition22 and Corollary23. Only these cited sections are used here. The source's formula for indexed two-cones supplies a separate exact numerical challenge.

## Application to a genuinely hidden cubic

Consider a nonempty four-coordinate whole presentation with actual affine dimension three. At a point of its relative interior, all globally tight nonzero inequality normals annihilate the whole affine hull, hence lie in one line R u. Both orientations must occur among the retained inequalities. Otherwise moving a sufficiently small distance to the permitted side preserves every tight inequality and every other strict inequality, producing a four-dimensional feasible neighborhood, a contradiction.

Inside the actual affine hyperplane, an edge's complete two-dimensional normal cone has two extreme restricted normal rays. They are restrictions of retained original forms, say v,w; u,v,w are independent. If every independent triple from the retained normal list is positive in one metric, BOTH triples (u,v,w) and (-u,v,w) are included. Equation (1) therefore makes the full restricted edge weight positive. This treats the complete edge cone, not a single simplicial cell from an unrelated fan.

An affine hyperplane need not pass through a lattice point at unit stretch. Choose a positive dilation clearing all vertices of the rational polytope, translate its integral affine hull by an integral vertex, and apply the preceding zero-vertex identity in its saturated kernel lattice. The actual face formula then gives positive c1 for this integral cubic. Period-one dilation scales c1 by the same positive integer; transfer back. No codegree, reflection or empty-interior premise is required.

If actual dimension is at most two, intrinsic leading/next-leading positivity and the nonempty constant one suffice. Empty positive-stretch fibers have the zero polynomial. Thus the full-dimensional four-coordinate triple certificate extends to every hidden stratum. In the new 29 representatives the hidden cubic weights are strictly positive, although the earlier inherited all-strata theorem only required nonnegativity at that clause.

## Complete independent challenge

The check in CODE/hidden_strata_v1.py enumerated every u with both signs in every new retained list and every independent pair after restriction to its saturated kernel. It computes the pair directly with its gcd-of-minors index, primitive residue and induced Gram matrix. It separately adds the two independently reconstructed complete three-cone constants by the independent three-cone calculation.

All 6,105 restricted-pair occurrences agree exactly with (1); their minimum is 1/18. DATA/J07-HIDDEN-PAIR-CERTIFICATE.json preserves every annihilator, integer kernel basis, restricted primitive pair, index, residue and three rational values. This finite test challenges the universal valuation argument; it is not its substitute.

The claim is conditional on one fixed metric and the full normal list, including both orientations. A single positive triple, an arbitrary nonintegral slice, or metrics chosen separately at different faces does not meet the premise. The source's own separate hidden-pair checks were valid and are not withdrawn; (1) supplies a more direct sufficient mechanism at the current stronger premise.
