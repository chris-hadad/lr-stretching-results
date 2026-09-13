# Exact cone-lattice compression and complete independent verification

Claims FR027-P08-T002 and C 001. This is a finite verified extension of the complete normal-cycle method, not a new analytic BV theorem or external campaign review. The compression preserves full counting lattices; matching dimensions, determinants or Gram matrices alone is not assumed sufficient.

## The exact equivalences

Let U be an independent q-by-m integer matrix whose rows are primitive inward normal generators, with m=5 and q=3 or 4 for the current coefficient certificates. Let A be the saturated lattice Z^m intersect span(rows U), and let ind(U) be the index of the row-generated lattice in A, computed as the gcd of all q-by-q minors.

When ind(U)=1, the rows themselves form an integral basis of A. A permutation identifying two normal Gram matrices therefore identifies their full normal lattices and scalar products. The dual projected primal quotient lattices and the full cones are identified. This is the inherited index-one Gram rule.

At higher index, allow ONLY a permutation of generator rows and a SIGNED PERMUTATION OF AMBIENT COORDINATES. For every row permutation p, normalize each column's sign so its first nonzero entry is positive, sort the resulting column vectors, and select the lexicographically least column word. Store p, the column permutation c and signs s with every occurrence. The displayed identity is

    V_(i,j)=s_j U_(p_i,c_j),       s_j in {-1,1}.           (1)

The signed column matrix is integral unimodular and Euclidean orthogonal. It maps the entire ambient lattice, saturated normal sublattice, polar quotient and metric bijectively. Row permutation leaves the same positive cone. Equation(1) therefore supplies a complete lattice-preserving cone isometry, so its BV constant and every needed face jet agree. No individual generator is independently negated; that would change the positive cone.

For q<=4, the search has at most 24 row permutations and five signed columns. Every equality is independently checked rather than trusted from a hash. For index-one types the permuted full Gram is retained; for higher-index types the full canonical normal embedding is retained. The original full Laurent numerator and all proper-face quotients remain stored even when many occurrences share one type. BV equivariance under lattice-preserving isometries is Proposition 14(b) of Berline–Vergne, Local Euler–Maclaurin formula for polytopes, arXiv:math/0507256v3. Its analytic assumptions do not identify different nonsaturated overlattices.

## An explicit same-Gram/same-index falsifier

The new complete type population supplies 22 comparisons with the same permuted Gram and same generator index but DIFFERENT full constants. One pair has normal matrices

    U=[[0,0,1,1,1], [0,1,-1,-1,0],
       [1,-1,0,1,0], [-1,0,0,1,1]],
    V=[[0,0,1,1,1], [0,0,-1,-1,1],
       [0,1,-1,-1,0], [1,0,-1,0,-1]].

Both indices are two and the common permuted Gram is

    [[3,-2,-2,-1],[-2,3,1,0],[-2,1,3,2],[-1,0,2,3]].

Nevertheless their COMPLETE transverse constants are respectively

    alpha(U)=1601/21600,
    alpha(V)=8429/86400=alpha(U)+3/128.                    (2)

Both are positive. This is a lattice-compression falsifier, not ordinary negativity. All fundamental numerators were independently replayed. The two exact type keys and all 22 comparisons are in DATA/J09-GRAM-INDEX-CHALLENGE.json. The signed-ambient rule does not merge these distinct embeddings; equal-Gram/index reuse would have produced a wrong constant. Thus the repair is substantive, not merely a faster dictionary key.

## Every original value is frozen before correction

The expansion visits the entire 123-representative roster in three immutable shards J02,J03,J04. For every coefficient k=2 then 1 it enumerates every independent (5-k)-subset; no local sign screening discards positive constraints. The complete raw cones, alphas, type bindings and negative observations are saved before solving the correction. Original negative local records are appended and flushed immediately at COMPLETE_ABSTRACT_LOCAL_CONE_NOT_WHOLE_LR_COEFFICIENT scope.

The full numerator calculation takes the primitive tangent rays in the actual projected lattice. The exponential sum uses EVERY lattice point of the half-open fundamental parallelepiped. The recursion subtracts every positive-dimensional transverse-face contribution from the full exponential sum, retaining the jets required for the final constant. Negative Laurent poles must cancel exactly. Face-lattice saturation, Gram dualization, primitive rays, lattice indices and all face jets are part of the saved record, not implicit cached guesses.

Every new type is immutable under DATA/TYPES/<key>.json.gz. Its deterministic gzip bytes, full expansion and input bindings are retained. DATA/FINAL-TYPE-INDEX.json lists 4790 types, including the small calibration types. The calibration checks orthants, an inherited negative three-cone and its orthogonal half-line product, and nontrivial-index controls under a different covector and signed ambient permutation. These controls have their own source scopes and are not new LR candidates.

## Complete rational correction and independent replay

For each independent triple J supporting a negative quadruple, retain its full saturated kernel M_J. All independent quadruple constraints are assembled, not just the negative ones. A bounded real optimization proposal h in [-1,1] is rounded to denominator 10^9. Then every complete corrected value

    alpha_I+sum_J h_J(primitive(M_J^T n_(I\J)))

is evaluated over exact rationals. Both originally negative and originally positive affected cones must be strictly positive; no tolerance is an acceptance criterion. The support choice is sufficient, not a claim that every conceivable face correction has been tested. No proposal failed in this extension.

J05 independently reconstructs all 4790 type traces using SymPy exact matrices and Hermite-normal-form fundamental representatives, rather than the primary Fraction elimination and finite-group BFS. It validates 68188 proper-face quotient occurrences and 72090 fundamental-point occurrences, every needed transverse jet, and every cancelled negative Laurent pole.

J06/J07 do not import the primary optimizer, evaluator or canonicalizer. They regenerate the complete original triangular rhombi, verify every retained unit chart and all 2638 new affine implications, enumerate all independent subsets using independent Bareiss minors, check every type word by(1) or the exact index-one Gram identity, and reconstruct all 398551 primitive correction incidences. Saturation of every kernel is checked by its complete minors. All 559253 quadruple and 147779 triple occurrences match. The new raw-negative quadruple population has 9254 entries; all corrected values are strictly positive. No triple is negative. The lowest quadruple margin is 118146761/6756750000000 and the lowest triple value is 1/144.

The source selector's complete action sweep is independent of the old helper and checks all 32768 gap masks, every action word, old/new disjointness and union. The old all-mask source closure and old two-orbit Unit 7 cone certificate remain explicitly inherited, not relabelled newly rederived from these current jobs.

## Why one old correction cannot just be copied

Literal transport of the old mask43 functionals to identical normal triples, extended by zero elsewhere, fails on 122 of the 123 new normal lists. The first failure, mask51, has an originally POSITIVE quadruple with normals

    (-1,0,1,1,-1), (0,-1,0,0,0),
    (0,0,1,-1,1),  (1,0,1,-1,0).

Its raw value is 127/2640. The old transferred functional on the displayed shared support subtracts 72080737/500000000, giving

    -1584914321/16500000000.                              (3)

This is a negative CORRECTED LOCAL trial weight, not a negative original parent coefficient. The new complete mask51 correction instead makes every quadruple positive, with minimum 914061857/351000000000. DATA/J09-FIXED-TEMPLATE-CHALLENGE.json retains all 122 failures and the successful fresh minima. The result is specific to this literal template extended by zero, not an impossibility theorem for transporting suitably enlarged corrections.

## Complete evidence and portability

All current successful source versions, exact launches, expected identities, raw outputs and waits are retained. Own earlier mission definitions were reviewed and copied under current identities; their old main functions were not run. Canonical original hive/mask/count interfaces are used only under the exact original EXECUTION-ALLOWLIST.json. Every other original historical program remains inert. A reused recurrence or helper is not counted as a new independent mathematical model.

The main finite certificates are self-contained data. They can be verified without the floating optimizer once the full base lattice/analytic premises are accepted. Current scientific drivers contain the owned runtime base path /mnt/data/FR027-BASE; the byte-restorer is portable, but rerunning science on a differently named host path requires an explicit reviewed path adaptation under a new attempt identity. No installation or unrestricted local/native access is implied.

Primary analytic reference: N. Berline and M. Vergne, Local Euler–Maclaurin formula for polytopes, arXiv:math/0507256v3 (28 July 2006), Proposition 13, Proposition 14(b), Definition 22, Corollary 23, Theorem 26 and Section 6. Selected primary HTML sections were read; no new analytic theorem or complete reading of all sections is claimed. URL: https://arxiv.org/html/math/0507256v3 . Whole-family application and precise exceptions are in proof 028; complete actual-fan and period-one challenges are in proof 030.

