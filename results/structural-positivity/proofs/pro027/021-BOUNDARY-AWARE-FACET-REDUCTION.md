# Complete boundary-aware facet reduction

This all-boundary certificate consists of complete rational identities and lattice-cone evaluations. Worldwide priority and external independent verification are not claimed. Floating optimization proposed some identities; every feasibility conclusion used in the proof is verified exactly.

## Whole objects, mask convention and actual lattice

Take balanced nonnegative integral partitions b=(lambda,mu,nu), with lambda outer, padded to n=6 or 7. Ordinary rank means the maximum trimmed partition length, not n when trailing zeros occur and not the number of coordinates. Use the complete conventional hive

    h(i,0)=sum_(k<=i) mu_k,
    h(0,j)=sum_(k<=j) lambda_k,
    h(n-j,j)=|mu|+sum_(k<=j) nu_k.

Every triangular-grid rhombus is present: 45 rows at n=6 and 63 at n=7. Their exact three families are in the source derivation of the complete rhombus inequalities. The standard whole hive/LR correspondence, LR stretching polynomiality, degree equal to actual affine dimension, and positive-dilation sign transfer are inherited source premises. No selected tableau support replaces that model.

The source boundary-mask reduction starts from all zero adjacent boundary gaps and closes under exact equal sums of one or two distinct nonnegative rhombus rows. Each zero-gap forcing and propagation is a sound whole-parent implication. Its integral unit-pivot elimination expresses every old interior coordinate as

    h_i = O_i b + x_sigma(i), or h_i=O_i b,                 (1)

with integral O_i and selected surviving original coordinates x. At stretch t, replace b by tb. The inverse literally selects x. Every original rhombus remains in the chart, including boundary-only rows that can certify emptiness. The ambient counting lattice of an m-coordinate chart is the full Z^m. If hidden equalities occur, the actual affine lattice is its intersection with the true affine hull; actual dimension need not equal m.

Mask bits, from low to high, encode the n-1 zero lambda gaps, then the zero mu gaps, then the zero nu gaps. We treat the closed boundary domain obtained by imposing the specified zero gaps and leaving all other partition gaps nonnegative. Thus our implications stay valid on additional equality walls. The source exhaustive certificates cover all 2^(3(n-1)) masks without an area or feasibility restriction.

There are exactly 1,911 n=6 masks and 20,606 n=7 masks whose source reduction has exactly four selected coordinates. The earlier all-size metric certificate, after the twelve full invariant-tensor symmetries, covers 1,887 and 20,384 respectively. The remaining 24+222=246 masks were not covered by that all-size theorem. Their finite size-at-most-thirty occurrences were already positive by separate complete counts; these cases do not add to the previously counted bounded domain.

## The missing information in a normal list

Write all reduced forms as

    r_i(b,x)=B_i b+A_i x >=0.                            (2)

Let g_j(b)>=0 be all remaining partition gaps and last parts, and let e_l(b)=0 be the specified zero gaps and trace equality. A row can be removed if there is a certificate

    r_i = sum_(j in K\{i}) y_j r_j + sum_a z_a g_a
                            + sum_l v_l e_l,            (3)

with y_j,z_a nonnegative rational and v_l rational. The equality is an identity in ALL 3n+4 variables, not merely on a seed boundary or edge. The certificate retains its full coefficients. On the legal boundary domain, (3) proves that the remaining inequalities imply r_i>=0. The reverse implication is automatic. Removing the row therefore changes neither the full real polytope nor its full lattice-point set, at ANY stretch or boundary in this closed domain.

The removals are sequential. Every certificate names only the rows present at that step. Later removals imply the earlier supporting rows recursively; no circular implication or jointly deleted pair is assumed. All boundary-only constraints also remain or receive an exact implication. No Horn inequality, random slack sample or early scalar equality is used to justify a removal.

This is stronger information than A_i belonging to the nonnegative span of other normal directions: the boundary forms B_i and the allowed partition inequalities are indispensable. [Co-realized negative cells, complete compensation, and an offset falsifier](024-CO-REALIZED-CONES-AND-BOUNDARY-CHALLENGE.md) below gives an explicit offset-decoupling falsifier.

## Complete residual coverage and finite certificate

The exact invariant-weight action is the source count symmetry of (mu,nu,-reverse(lambda)), including simultaneous dualization and determinant normalization. On gap masks it gives at most twelve words. The whole count, hence polynomial and degree, is preserved at every stretch. No affine isomorphism between the two conventional hives is assumed.

The 246 residual masks split into 29 exact representative classes: four n=6 representatives and twenty-five n=7 representatives. DATA/J05-ROSTER.json preserves EVERY member. DATA/J06-INDEPENDENT-VERIFICATION.json supplies an independently written word from each member to its representative and checks, exactly, that old and new mask sets are disjoint and their union is the full four-coordinate set.

The complete representative certificate DATA/J05-COMPLETE-MASK-CERTIFICATE.json contains, for every representative:

* the original-coordinate selector, full integral offset matrix O, and zero-or-one identification matrix C;
* every one of its 45 or 63 reduced full boundary-linear rhombus rows;
* each sequential implication (3), with every nonzero rational multiplier and the exact remaining-row list;
* the final retained rows and their complete primitive nonzero normal list.

There are 1,180 removal steps. The final retained rows are NOT asserted to be irredundant facets for every boundary. They are a sufficient full presentation with a tractable complete normal list.

For each representative we use ONE standard positive-definite rational metric in its selected-coordinate lattice. Every independent three-subset of its final normal list has strictly positive complete transverse BV constant. There are 10,125 triple occurrences and 2,535 distinct literal triples. The minimum is 1/144; the representative n=7, mask27033 has the larger minimum 1/132. No different metric is chosen at individual faces of a parent.

Each retained primitive normal has positive coordinate mass at most two and negative coordinate mass at most two, since (1) only identifies original coordinates. Its squared norm is at most six: the only larger preprimitive possibility is (2,-2), which reduces to (1,-1). Thus the source complete codimension-two positivity theorem also applies whenever the chart is truly four-dimensional.

## Independent exact verification

The primary scalar evaluator uses the complete indexed three-cone formula of the source indexed three-cone derivation, in the projected quotient lattice. It does not treat normal rays as tangent rays. If the primitive tangent rays form an s-gon cone section, its complete value is

    1/2-s/8 + sum_(facets ij) [ -s(p_ij,q_ij)/2
          + <v_i,v_j>(1/||v_i||^2+1/||v_j||^2)/(24q_ij) ],

where every facet index and Dedekind sum is retained. The tangent metric is dual to the Gram matrix of a saturated normal-lattice basis. The formula handles the complete nonsimplicial three-cone as well as simplicial triples.

The independent verifier CODE/verify_certificate_v1.py neither imports the optimizer nor calls this evaluator. It regenerates every original rhombus from six triangular-lattice neighbor directions, substitutes the stored integral chart, and compares the entire 3n+4 coefficient rows. It verifies the coordinate-selection inverse and every sequential implication with exact SymPy rationals.

For each independent triple, it independently constructs a unimodular completion of the primitive edge direction, a saturated normal-plane basis and the primitive tangent rays. It enumerates ALL cosets of the half-open tangent-ray parallelepiped. In total 2,774 fundamental-lattice-point occurrences are retained. It expands the complete exponential numerator and three geometric denominators through the constant Laurent term, subtracts the complete edge-transverse linear terms, and compares the resulting constant with the primary indexed formula. All 2,535 distinct literal constants and all 10,125 occurrences agree. Every lattice point, generic covector, index and subtraction is saved in DATA/J06-LAURENT-CERTIFICATE.json.

The independent verifier also rederives every mask action, checks every new word and the exact old/new/full set equality. Its output is a complete finite certificate, not an inference from a collection of positive scalar values. The source's larger old certificate remains an prior result, and was not recomputed here.

## Why the full boundary identities are necessary

The first eight complete seed hives had no negative realized edge weights even though their unreduced normal lists contained negative independent triples. Those seeds were already positive finite controls, not new sign discoveries. Requiring an isolated negative triple cone at a legal edge gave exact infeasibility certificates. Relaxing that requirement admitted 46 occurrences with negative SELECTED subcone constants, but additional forced normals enlarged every actual cone; the 46 complete cone values are positive.

The full affine identities suggested the repair (3), replacing an unqualified normal-atlas test by an exact boundary-aware presentation. The first eight repaired lists and then all 29 residual representatives passed. The argument uses the incidence relations among the complete boundary-linear inequalities. It does not prove an unrestricted Farkas cone-generation theorem for realizable hive face volumes, nor positivity for arbitrary systems with the same short normals.

The following proofs treat hidden strata, the all-size LR consequence, explicit full polynomials, and the independent-offset challenge. The verification uses the complete hive and boundary-mask interfaces together with separately written exact certificate checks.
