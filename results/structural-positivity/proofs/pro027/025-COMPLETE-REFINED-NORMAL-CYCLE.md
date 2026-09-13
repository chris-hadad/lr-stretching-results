# Complete refined normal-cycle compensation, including hidden affine strata

Claim FR027-P07-T001. This is an originating sufficient coefficient theorem. It does not identify the cone of realizable face volumes with every abstract balanced nonnegative weight, and it does not turn a failed sufficient correction into an LR counterexample.

## Lattices and the finite certificate

Let L=Z^m carry one fixed rational positive-definite scalar product. Let N be a finite set of primitive integral covectors. For an integer k>=1, put q=m-k. For each independent q-subset I of N, let sigma_I=pos(I), and let alpha_I be its COMPLETE transverse Berline–Vergne constant in the saturated normal lattice L* intersect span(sigma_I), equivalently the projected primal quotient lattice. In particular the normal generators are not substituted for tangent generators. Normal-plane indices, fundamental numerators and the induced dual metric are retained.

For each selected independent (q-1)-subset J, choose an arbitrary rational linear functional h_J on the quotient L*/(L* intersect span(J)). In coordinates, choose an integral basis matrix M_J for the saturated kernel of J in L; its columns have rank k+1. If I=J union {n}, the primitive quotient conormal is

    u_(I/J) = primitive(M_J^T n).

The primitive operation divides the gcd of ALL restricted integer coordinates. It is not the unchanged ambient normal. Set

    alpha'_I = alpha_I + sum_(J facet of I) h_J(u_(I/J)),       (1)

using zero h_J on every unselected facet. Suppose alpha'_I>=epsilon>0 for EVERY independent q-subset of N, including all positive cones affected by a nonzero correction.

Then every nonempty bounded rational polytope P presented by inequalities with normal directions in N, whose lattice count is a polynomial, has c_k(P)>0 whenever its actual dimension is at least k. More quantitatively,

    c_k(P) >= epsilon sum_(actual k-faces F) vol_L(F).          (2)

Actual lower-dimensional cases have c_k=0. No particular offsets, simple fan, codegree, reflection, nonnegative h-star numerator, or unimodular normal cone is assumed. The bound uses the actual saturated face lattices and their usual lattice-normalized measures, not factorial-normalized volumes.

## A compatible refinement exists using the same normals

First choose a positive dilation clearing all vertices; translating by an integral vertex, when needed, gives the appropriate saturated affine-hull lattice. This step preserves coefficient signs and scales c_k and every k-face volume by the same positive kth power. It suffices to prove the assertion for an integral P.

The normal fan of P can have nonpointed cones if P has hidden affine equalities. It nevertheless has a complete pointed simplicial refinement with rays drawn from N. Here is a direct construction that does NOT assume continuity of Ehrhart coefficients under perturbation. Loosen every nonzero row b_i+<n_i,x>>=0 by epsilon a_i, where all a_i>0 are generic. At any point of P all inequalities become strict, so the new polytope P_epsilon is full-dimensional. Its recession cone is unchanged and is {0}, hence it is bounded. Generic a avoids every finite affine circuit degeneracy, so for sufficiently small epsilon>0 it is simple.

Each vertex of P_epsilon is specified by an independent m-subset of the ORIGINAL rows. Its limit as epsilon tends to zero is feasible in P and makes the same m independent normals active; it is therefore a vertex of P. Its complete normal cone is contained in that vertex's normal cone of P. There are finitely many bases, so a sufficiently small common epsilon makes the entire fan a refinement. Use that fan, denoted Gamma. The polynomials of P_epsilon play NO role; no period-one or coefficient-limit assertion about the perturbed polytope is needed.

In the full-dimensional case a pulling triangulation with one GLOBAL order on the actual facet-normal rays gives another compatible refinement. Independently sorting coordinates after changing the quotient basis does not by itself supply such compatibility. The numerical geometric challenge uses the same ambient ray order at every face.

## The full face-volume weights are balanced

For a q-cone sigma in Gamma, give it weight w_sigma=vol_L(F) if its relative interior lies in the normal cone C_F of an actual k-face F, with dim C_F=q. Otherwise give it zero. This assigns the SAME actual face volume to every top-dimensional subdivision cell of C_F; it does not count selected faces only.

For every (q-1)-cone tau of Gamma,

    sum_(sigma contains tau, dim sigma=q) w_sigma u_(sigma/tau)=0
       in L*/(L* intersect span(tau)).                         (3)

There are three complete cases. If relint(tau) lies in a coarse normal cone of dimension q-1, it is the cone of an actual (k+1)-face G. Each adjacent nonzero-weight q-cone corresponds to exactly one facet F of G near relint(tau). Its primitive quotient conormal is the primitive integral facet conormal in the saturated lattice M_G=L intersect lin(G). For the dual metric on this space,

    covol(M_F)=covol(M_G)||u_(F/G)||.

The Euclidean boundary-balance identity for G therefore becomes precisely sum vol_L(F)u_(F/G)=0. No extra normal index remains after primitive normalization. Restriction L* -> M_G* is surjective because M_G is saturated, with kernel L* intersect span(tau).

If relint(tau) lies inside a coarse q-cone C_F, the two adjacent q-dimensional subdivision cells inside span(C_F) have the same weight vol_L(F) and opposite primitive quotient directions. Their contributions cancel; any other adjacent cells have zero weight. If relint(tau) lies in a coarse cone of dimension larger than q, all adjacent q-cell weights vanish. These cases exhaust all tau, including normal fans with lineality. Thus (3) holds for the COMPLETE refinement, not merely for a selected star.

## Invariance of the complete coefficient sum

The BV dual SOLID valuation adds the alpha_I over the top-dimensional simplicial cells of each C_F; lower-dimensional intersections have zero dual-solid value. For a nonpointed normal cone the polar lies in a smaller subspace, and BV ambient/subspace compatibility identifies its value with the actual transverse-cone value there. Thus the local Euler–Maclaurin formula reads

    c_k(P)=sum_(sigma in Gamma, dim sigma=q) w_sigma alpha_sigma.

Insert (1), interchange the finite sums, and apply (3). Every correction vanishes after the COMPLETE weighted aggregation. Consequently

    c_k(P)=sum_sigma w_sigma alpha'_sigma.

Every weight is nonnegative. Each actual k-face has at least one top-dimensional cell in its normal-cone subdivision, proving (2). This includes hidden affine strata: it is not obtained by fitting the upper coordinate bound as the true degree or by treating an arbitrary orthogonal slice as a saturated quotient.

## Source premises and scope

The complete lattice-normalized facet balance and its quotient-rank requirement are inherited from the fully read original FRB normal-pilot DERIVATION.md, copied in SOURCES/FRB-NORMAL-PILOT-DERIVATION.md. Its original correction required actual closed cones and all affected incidences. The originating contribution here is the compatible-refinement construction and complete balanced-weight argument allowing one sufficient certificate over every independent subset, including hidden-dimensional parents.

The analytic premises are Berline–Vergne, Local Euler–Maclaurin formula for polytopes, arXiv:math/0507256v3, Proposition12, Proposition13, Definition22, Corollary23 and Theorem26. The selected primary HTML sections and their projected-lattice conventions were read in this unit. This does not assert new analytic results or full reading of every section of the paper.

A solution of (1) is sufficient for every actually realized weight system. No necessity over realizable LR weights follows from the abstract Farkas alternative. A failed bounded/support-restricted numerical proposal remains a certificate failure, not an ordinary-negative polynomial.
