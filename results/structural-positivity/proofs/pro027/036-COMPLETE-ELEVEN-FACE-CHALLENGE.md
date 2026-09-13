# Complete eleven-face volumes and a genuine rank-seven LR count

This complete geometric calculation tests the eleventh-coefficient theorem. The stable source–sink family and count identity are previously established; [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md) gives the direct conventional-hive affine map. The computation checks the full eleventh coefficient using two complete representations.

## Bare entire parent and prior determining space

With lambda outer take

    lambda=(11,10,8,6,4,2,1),
    mu=nu=(6,5,4,3,2,1,0).

This is M=s=1 in [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md), balanced at outer size 42, ordinary rank seven, actual degree 15, and true codegree 12. Its entire polytope is integral in the saturated Z15 hive lattice. The full affine map is h=O+Uz, where z consists of every nonadjacent source--sink edge, and U and U inverse are integral with determinant +/-1. No original rhombus or path is omitted.

The complete unit flow vertices are ALL32 increasing source--sink paths on seven vertices. Their positive average is actually strict for every nonzero original hive rhombus. Every one of the 21 nonnegative edge inequalities occurs literally among the original63 rhombi after the map, and every original rhombus is nonnegative on all 32 vertices. The extra M-direction is nonnegative in every full boundary-dependent row. Thus the model and its complete face lattice apply on every M>=s>=0; M affects only an integral grade-compatible translation at fixed s. At s=0 the correct object is a point.

The source codegree proof uses every edge crossing each prefix. Positive integer flows need t>=k(7-k) for k=1,...,6; the maximum 12 is attained by the explicit all-one/nonadjacent-plus-adjacent-residual construction in [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md). Hence P(-1),...,P(-11) are zero by actual reciprocity. These eleven roots, P(0)=1 and the four positive nodes1,...,4 give the prior complete degree 15 determining space. Positive 5 and 6 are reserved and unused in both reconstructions.

## Every relevant face and its saturated lattice

For any set of edge equalities f_e=0, its entire face is the convex hull of all source--sink paths avoiding those edges. Let E_A and V_A denote the edges and vertices still lying on a surviving source--sink path. If nonempty, its dimension is |E_A|-|V_A|+1: its positive path average proves relative full dimension, and the connected incidence equations have rank |V_A|-1. This handles every extra zero edge forced by the requested equalities.

Of the 21 nonnegative edge inequalities,19 are actual facets. The source's first adjacent edge and final adjacent edge are redundant nonnegative sums, rather than additional independent facets. Enumerating every four-subset of the 19 facets, retaining its entire path set and actual dimension, produces exactly3571 eleven-faces. Every three-subset similarly produces exactly933 twelve-faces. Completeness follows because every codimension-r face has r independent active facet normals; their zero equations force every other active row at that face. Duplicates are removed by the complete vertex set, not merely by early counts or a loose dimension label.

For each face, a spanning tree of its connected active graph is chosen. Deleting one incidence row gives a tree incidence determinant +/-1. Projection to the complementary edges is therefore a full affine integer coordinate chart for that face, with an integer inverse and no index correction. The normalized volume is computed by a complete pulling triangulation in those coordinates, as

    vol_Z(F) = sum_(full simplices T) |det(T)| / 11!.

The division by 11! converts the simplex determinant to the requested fundamental-parallelepiped measure. It is not an extra multiplier in the face formula. All simplices, tree/free-edge lists and exact determinant values survive in the raw3571-face file.

The independent volume verifier uses the reverse spanning-tree order, the largest rather than smallest pulling vertex, and SymPy exact determinants rather than the primary Bareiss routine. It independently enumerates faces using ALL21 edge inequalities rather than the 19-facet reduction. Its complete reverse-pulling simplex and determinant bodies are retained. Thus the volume equality is not a re-reading of primary totals.

## Complete original-metric normal cycle

All actual eleven-face normal cones in this control are simplicial. Every extreme normal is identified with its literal direction in the ORIGINAL60-normal hive atlas. Extra redundant active rhombi lie inside the same cone; their full boundary constants were not detached. There are 3571 complete four-cones and 933 primitive rank 12 quotient balance equations. No different metric is chosen at different faces, and the flow coordinate map is not assumed isometric.

The exact original and corrected sums are

    sum_F vol_Z(F) alpha(F) = 22483/179625600,
    sum_F vol_Z(F) alpha'(F) = 22483/179625600.

Every complete twelve-face weighted primitive-conormal sum vanishes. The sum of all normalized eleven-face volumes is31153/19958400. Every original complete local weight in this control is positive, with minimum 15811/806400. No actual negative local face is claimed for this family. The raw132 negative abstract atlas cones are retained separately by the global certificate in [The eleventh ordinary coefficient at every rank-seven LR boundary](034-ALL-RANK7-ELEVENTH-COEFFICIENT.md) and are not bypassed by this positive control.

These calculations test the twelve-component normalization, complete high-dimensional face volumes and entire weighted aggregation. Earlier edge-only or six-face tests would not by themselves provide these current records.

## Entire polynomial and independent count

The unsigned complete flow counter distributes the entire incoming value at each vertex among ALL later vertices, with exact integer memoization; the sink is retained. It returns

    P(0..6) = 1,32,450,3976,25725,132608,574056.

The complete ascending coefficient vector is

    [1,
     1494803/360360,
     15027247/1965600,
     361525133/43243200,
     364801681/59875200,
     45175393/14370048,
     4314659/3628800,
     4392257/13063680,
     781271/10886400,
     75619/6531840,
     15257/10886400,
     22483/179625600,
     29/3628800,
     23/66718080,
     1/111196800,
     1/9340531200].

Every entry is positive, and both unused positive nodes agree. The eleventh entry agrees exactly with the complete geometric face sum before and after correction. The leading coefficient corresponds to factorial-normalized whole volume140, but the face formula uses the unfactored lattice measure throughout.

A separate complete literal ordinary-LR reading-word recursion recounts every node0,...,6, and separate Newton interpolation uses the same prior mixed-node space, not the primary Lagrange arithmetic. The complete vector was recorded and checked for negative coefficients before comparison with the primary calculation. Additional small-grade sites test M=2,s=1 and the common dilation M=s=2, with overlap explicitly retained rather than counted as additional polynomials. Completion records and evidence totals are in J09-VERIFIED.json.

The stable family and the positivity of historical source--sink controls are not newly discovered here. This is a complete independent-model and higher-face challenge of the unrestricted rank-seven c11 theorem. No claim is made that every source--sink polynomial at every n has all coefficients positive.

## Geometric consequence for first-interior generation

[Complete source-sink LR interiors are generated at their first grade](017-COMPLETE-FLOW-INTERIOR-GENERATION.md) proves the exact closed positive-slack Minkowski identity C_(N+t)=C_N+F_n(t) for every N>=floor(n^2/4), together with the corresponding equality on lattice points. The direct grade-compatible affine lattice map in [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md) now transfers that identity to the ACTUAL conventional hives of this stable family, not only to an equal-count model. At integral s>0 their first grade is ceil(floor(n^2/4)/s).

This does not assert disjointness of the translates or universal first-interior generation for other LR hives. The uncovered-stratum examples and its distinctions between equal polynomials and equal geometry remain unchanged. The new transfer has two explicit premises: that complete all-cut source--sink generation proof, and the full affine map in [A complete stable source--sink hive map](035-STABLE-FLOW-HIVE-MAP.md) at M>=s. It is not an additional independent positivity discovery.
