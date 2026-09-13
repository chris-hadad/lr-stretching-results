# A complete low-dimensional terminal from boundary masks

FRONTIER-025 P08. Originating proof with a finite exact mask certificate, awaiting campaign verification. This is an ordinary-coefficient theorem, not an inference from positive counting values.

## 1. Entire objects and conventions

Let b=(lambda,mu,nu) be a balanced triple of nonnegative integral partitions padded to n entries, n=6 or 7, with lambda outer. Its whole hive uses exactly the coordinates and ALL rhombi in proof 024, equations in Section 1. For the upper half-plane triangular grid the inequalities are those in that proof; their number is 45 and 63. The entire integer-count identity with the ordinary LR coefficient, polynomiality, saturation and reciprocity are adopted source premises. No facet or selected support is substituted for this entire count.

An empty positive-stretch fiber has the separate zero-polynomial convention. A nonempty fiber has P(0)=1, and its polynomial degree is its actual affine dimension. Our terminal allows arbitrary sizes, not just size thirty.

## 2. A certified subset of forced equalities is sufficient

For each of the 3(n-1) adjacent boundary gaps, the exact gap is the sum of two nonnegative rhombus slacks. For example a gap on a coordinate edge is 2h(k)-h(k-1)-h(k+1). Both corresponding rhombus slacks therefore vanish when the gap is zero. These identities are generated on the complete grid.

Let A_i denote the full linear rhombus form, including the boundary coordinates. If positive sums of such forms agree, say A_i+A_j=A_k+A_l, then vanishing of the two on either side forces vanishing of those on the other side. The certificate uses ALL equal positive sums of one or two DISTINCT rhombus rows. Closure is a sound inference of whole-parent equalities: no completeness claim about all forced equalities is required.

For each zero-gap mask the primary algorithm takes this finite closure. The independent algorithm rebuilds the identities on ALL vertices, including all three corners, and computes closure by synchronous repeated scans instead of the primary adjacency queue. This checks that anchoring the corners in the primary representation created no false row identity.

Now restrict the forced forms to the interior coordinates. Successively choose a row with just one coefficient +1 or -1, or a row whose two remaining coefficients are +1 and -1. Solve for one coordinate and substitute. Each step has an integral coefficient-one inverse and expresses an old coordinate as an integral boundary-dependent constant plus one selected free coordinate, or as a constant alone. The full boundary dependence is affine-linear with INTEGRAL coefficients: induction follows from the unit pivots. Every original rhombus remains in the final model. Any boundary-only inconsistency means the fiber is empty; it is not silently discarded for a nonempty fiber.

The finite certificates prove that every listed forced interior row vanishes after these eliminations, at EVERY mask in ranks six and seven. They store the entire unit-pivot word and the selected free-coordinate indices. In particular, for a nonempty boundary there is an exact all-stretch identification

    h_i = t b_i(lambda,mu,nu) + z_sigma(i), or h_i=t b_i(lambda,mu,nu),

where b_i is integral on integral boundaries. The inverse selects the surviving original coordinates. Thus the model has the full saturated integer coordinate lattice Z^m and ALL retained inequalities, not merely a count-preserving injection. If further equalities are present, the actual dimension can be less than m. We only use m as an UPPER bound.

## 3. The terminal

THEOREM. If the above integral coordinate-identification reduction leaves at most three free coordinates, the whole stretched LR polynomial is coefficientwise nonnegative.

Proof. Empty fibers give the zero polynomial. For a nonempty fiber, if its actual dimension is at most two, intrinsic leading and next-to-leading positivity and constant one prove the conclusion. The only other possibility is actual dimension three in a three-coordinate chart. Each original rhombus has at most two positive and two negative unit occurrences. After coordinate identification, each reduced normal has positive coordinate mass at most two and negative coordinate mass at most two. Primitive reduction therefore gives squared norm at most six: the only larger squared norm before primitive reduction is the pattern (2,-2), which reduces to (1,-1).

Since the whole three-dimensional polytope is full-dimensional in this saturated chart, its actual facet normals are primitive normals among these retained rows. Proof 023 gives positive c_(3-2)=c1, with every complete transverse two-cone weight at least 1/100. Intrinsic top-two positivity gives c2,c3>0. Therefore every coefficient is positive in the dimension-three case. Dimension drops were already treated, so the theorem is complete. QED.

This is why a complete affine-hull computation for every boundary is unnecessary for this terminal. It is NOT a theorem that every actually cubic hive has passed the sufficient reduction. A boundary can have a much looser mask bound than its true dimension.

## 4. Exhaustive finite mask certificate

Mask bits 0,...,n-2 represent zero lambda gaps, the next n-1 bits zero mu gaps, and the last n-1 bits zero nu gaps. There are exactly 32768 masks at n=6 and 262144 at n=7. Every mask is included; no area, feasibility or genericity filter is imposed.

The primary closure has 24709 distinct zero-row sets at n=6 and 215867 at n=7. All pass the coordinate-identification reduction. The counts with reduction dimension at most three, before taking symmetries, are 28427 and 171165 respectively. These are counts of boundary MASKS, not of hives, feasible parameter chambers, or original root identities.

Independent complete audits cover rank six in slices [0,8192),[8192,32768), and rank seven in the four consecutive slices of length 65536. Every row identity and every elimination is checked. Data are MASK6.json, MASK7.json and AUDIT6-0/1.json, AUDIT7-0/1/2/3.json. There are no unverified mask cases in these audits. The missing process wait of the first rank-seven producer remains a process qualification; its full mathematical output is subsequently checked by these four successfully waited audits.

## 5. Symmetries and exceptions

The criterion may be applied after any of the twelve invariant-weight permutations/dualities proved in proof 029. The reduced boundary need not have area at most thirty because this terminal is an ALL-SIZE theorem. Empty polynomial tensor cases created by determinant normalization are zero terminals. Partitions and rank are checked after normalization if a concrete transformed count is evaluated.

A failed terminal is UNKNOWN, not negative or necessarily dimension at least four. In particular FE/025, lambda=(9,8,7,3,2,1), mu=nu=(5,4,3,2,1), has all strict padded boundary gaps and hence mask bound ten, but its entire polynomial is (t+1)^2 by a proper Horn factorization. This exact source challenge demonstrates why the bound must not be called actual degree.
