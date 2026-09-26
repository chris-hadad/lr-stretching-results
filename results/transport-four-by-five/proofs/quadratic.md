# Global quadratic positivity and two-sided balancing for entire four-by-five transportation/LR polynomials

## Theorem and exact scope

Let r=(r1,r2,r3,r4) and c=(c1,c2,c3,c4,c5) be nonnegative integer vectors with common total M. Let

    T(r,c)={X in R^(4×5): X>=0, row_sums(X)=r, column_sums(X)=c},
    P_(r,c)(t)=#(t T(r,c) intersect Z^20)=sum_k a_k(r,c)t^k.

The original lattice is the full affine integer table lattice and t is the ORIGINAL stretch. Then a2>=0 for every pair at every size and on every zero-margin, forcing and equality boundary. If d is the actual dimension, then a2>0 exactly when d>=2. A point or a segment has a2=0. This is a theorem about the quadratic coefficient of the ENTIRE polynomial, not a positive bound for an auxiliary sum or a bounded panel.

At fixed row margins, every legal balancing move between any two columns is quadratic-coefficient nondecreasing:

    a2(r,c-e_j+e_l)>=a2(r,c),  c_j>=c_l+2.

The donor need not be largest. At fixed column margins, the analogous move between any two rows is likewise nondecreasing. Both statements include zero entries. More generally they hold for the continuous homogeneous piecewise-quadratic extension along balancing segments up to equality. This continuous extension is a coefficient function, not an assertion that arbitrary rational tables have period-one Ehrhart polynomials in an unchanged grade.

For strictly positive integer margins, M>=5, put

    b_5=328081/33264,
    b_6=3741137/332640,
    b_M=239053/20790 for M>=7.

The sharp minimum at fixed M is b_M, attained by rows (M-3,1,1,1) and columns (M-4,1,1,1,1). In particular the global positive-integral minimum is328081/33264, attained at rows(2,1,1,1), columns(1,1,1,1,1). At any fixed total, simultaneously balanced integer rows and columns maximize a2. The extremal statements concern a2, not all ordinary coefficients.

No conclusion here settles the main whole-coefficient endpoint. General coefficients of indices3 through d-2 remain unresolved on the unprotected active rectangles; the leading and second-leading coefficients already have their standard positive integral-polytope interpretation. Arbitrary ordinary-rank-eight LR triples are not all transportation triples. General LR/KTT positivity and a legal ordinary-negative entire LR polynomial remain separate unresolved goals.

## 1. Entire ordinary LR realization, lattice and prior degree

For any labeled r,c, let R_i=sum_(a>=i)r_a, C_j=sum_(b>=j)c_b. The whole LR lift, with lambda outer, is

    lambda=(M+R2,M+R3,M+R4,C1,C2,C3,C4,C5),
    mu=(M,M,M,C2,C3,C4,C5),
    nu=(M,R2,R3,R4).

All entries are nonnegative decreasing integers and |lambda|=|mu|+|nu|. Trim trailing zeros only after this construction. At five positive columns the displayed ordinary rank is eight. Zero margins can change trimmed rank without altering the fixed padded chart used in the proof.

The first three skew rows are forced superstandard, with diagonal row-label counts R2,R3,R4. Their common inner offset is M. The five lower skew rows are disjoint intervals of lengths c1,...,c5, whose label counts are the table columns. Between adjacent labels, the initial buffer surplus is exactly the entire remaining content of the higher label. Hence every lower ballot inequality is automatic for every table. Conversely, deleting the forced rows from an LR row array gives the entire nonnegative table with precisely the required margins. This is an invertible real and integer map, not just a scalar identity or a selected face.

At padding n=8, the conventional hive map is

    H(i,j)=sum_(v<=j)mu_v + sum_(u<=i)sum_(v=u..j)a(u,v),
    h(x,y)=H(y,x+y).

Its inverse is a(i,i)=h(0,i)-h(1,i-1) and, for i<j,

    a(i,j)=h(j-i,i)+h(j-i,i-1)-h(j-i+1,i-1)-h(j-i-1,i).

The three rhombus types are exactly column slack, ballot slack and nonnegative off-diagonal row count. Diagonal nonnegativity follows from the remaining ballot inequalities and the final content; the other boundary tests are partition inequalities. Thus both implications hold over the reals and the integer second differences recover the entire original affine lattice, including degenerations. The complete source proof [S1] is retained and was reread in this unit.

For positive margins, X_ij=r_i c_j/M is strictly positive and the eight independent row/column equations leave dimension12. The upper-left3×4 entries give a saturated integer chart; every omitted entry is an integer subtraction from the margins. The difference lattice has basis E_ij-E_i5-E_4j+E_45. A vertex has forest support because a support cycle would admit a two-sided alternating perturbation. Leaf deletion solves the forest margin equations integrally. Hence the polytope is integral in its original lattice, of degree12 before any interpolation. Delete forced-zero rows/columns for active sizes p,N; then d=(p-1)(N-1). If p<=1 or N<=1, including M=0, the fiber is a point. All13 ordinary slots were retained in the independent whole-polynomial controls.

## 2. Why cut cones carry the actual boundary coefficients

For two same-size margin pairs (r,c),(s,d), of totals R,S, put delta(r,c;I,J)=r(I)+c(J)-R. A table X in the sum-margin fiber decomposes as Y+Z exactly when a capacitated source-row-column-sink network admits Y with the first margins and0<=Y<=X. Its full min-cut inequalities are X(I,J)>=delta(r,c;I,J). The real-capacity statement follows by compactness of the maximum-flow set and the residual augmenting-path cut argument, not a termination claim for arbitrary real augmentations.

For a complete transportation fiber of total M, the minimum of a block X(I,J) is max(0,r(I)+c(J)-M). Attainment follows by aggregating to2×2 and distributing each block; zero groups carry zero mass. Combining a cut and its complementary cut proves

    T(r+s,c+d)=T(r,c)+T(s,d)
    iff delta(r,c;I,J) delta(s,d;I,J)>=0 for every I,J.

Replacing J by its complement gives the equivalent convention h_(I,J)=r(I)-c(J) used below. Thus a cone on which all cuts have fixed weak signs is a WHOLE real Minkowski cone. The homogeneous buffer/hive map also preserves the sum.

Choose integral tables on its integral generating rays and subtract their corresponding parameter combination. The summands then lie in one common saturated kernel lattice, with their smaller affine spans retained. Bernstein–McMullen multivariate Ehrhart polynomiality [S2, Theorem2.3] supplies the count polynomial for all nonnegative integer ray coefficients, including zero coefficients. Its homogeneous quadratic part is a2. For a rational ray combination, clear denominators and use P_(qr,qc)(t)=P_(r,c)(qt); a2 scales by q². Consequently the same quadratic field gives the ACTUAL whole coefficient on every closed cone boundary. Individual signed assignment contributions need not be continuous or equal isolated boundary counts.

This argument also proves that the whole piecewise-quadratic function joins continuously across all common cut walls. No floating limit or high-degree-zero clamp is involved. Nonunimodular parameter cones require denominator clearing; their indices are not physical table-lattice indices.

## 3. Complete original-offset assignment formula and finite coefficient space

The full table count is the coefficient of x^(tr) in product_j h_(t c_j)(x1,x2,x3,x4). The elementary partial-fraction identity

    h_m(x)=sum_i x_i^(m+3)/product_(k!=i)(x_i-x_k)

expands the five factors into all4^5=1024 labeled assignments f. Rewrite the denominators in the fixed ordered positive-root expansion. With labels0,...,3, occupation n_i=#f^(-1)(i), the sign is(-1)^sum_j f(j), the netflow slope is beta_i=sum_(j:f(j)=i)c_j-r_i, and the shift is

    delta_i=i n_i-sum_(j>i)n_j.

For pair i<j there are n_i+n_j labeled parallel root variables. Their total is15 and their incidence rank is3; a star through any occupied class supplies a saturated basis. In simple-root coordinates the original offset is

    d=(-n1-n2-n3,-2(n2+n3),-3n3),

and the slope is(beta0,beta0+beta1,-beta3). Every original offset and every assignment sign is retained. The exact all-grade generating identity is thus a signed sum of these complete15-edge vector-partition counts at d+t beta_simple.

The accepted A3 unimodular vector-partition chamber theorem [S3] gives a total-degree-at-most12 polynomial on each of the seven source cones. Deleting zero-multiplicity roots only coarsens the common basis-cone refinement; an unsupported open cone has the zero polynomial. The seven ordered ray bases are printed in DATA/ATLAS-RECOUNT-CONTRACT.json. Each basis has determinant±1. The accepted theorem and refinement proof remain credited premises; finite successful counts alone do not establish polynomiality.

At a generic margin pair, each affine assignment ray eventually lies in one fixed chamber or outside support. The count polynomial therefore agrees for all sufficiently large positive stretches with the complete assignment polynomial. Both sides are polynomials, so they agree at every stretch. Its homogeneous quadratic part is the entire a2, not a lower-class approximation. The closed-cone argument of section2 handles every tied or zero-margin boundary.

For each occupation/chamber, the455 strict-interior sites V(1+u), u>=0 andsum u<=12, determine the full degree12 space. The four sites u=(13,0,0),(0,13,0),(0,0,13),(5,4,4) were reserved before the fresh recount and excluded from determination. A new C++ repeated-labeled-edge dynamic program counted all179928 occurrences using6934760 checked unsigned128 additions. No source count or coefficient entered that program. A nonnegative root-coordinate path cannot leave the truncated box and return, so the complete coin-change recurrence is exact.

All392 full Newton polynomials were reconstructed independently from the178360 determining values and persisted before comparison. Every one of their178360 positions matches the source full atlas. All1568 unused strict-interior checks pass:1408 counts are positive and160 are genuinely zero for unsupported chambers. No missing count is represented by zero. This is a fresh complete AUXILIARY atlas recount; it is not a full whole-table polynomial reconstruction on every global margin chamber.

## 4. Independent finite cover of the complete seven-dimensional margin domain

Normalize M=1 and sort both margin vectors. Use x=(r1,r2,r3,c1,c2,c3,c4), with r4=1-r1-r2-r3 andc5=1-c1-c2-c3-c4. The complete domain K is the product of the ordered row and ordered column simplices. Its nine inequalities are

    r1-r2>=0, r2-r3>=0, r3-r4>=0, r4>=0,
    c1-c2>=0, c2-c3>=0, c3-c4>=0, c4-c5>=0, c5>=0.

Its Lebesgue volume is1/(3!4!4!5!)=1/414720. There are420 labeled proper row/column cut pairs, or210 unoriented primitive hyperplanes after complementary identification. Nonproper cuts have fixed weak signs from nonnegative margins. All512 labeled cuts are therefore controlled by these210 cuts and the original domain.

The primary construction split first at r1+c1=1, to price and retain both the unforced and forced regions. Exact base enumeration gave34 and31 vertices. The unforced side has143 interior-crossing cuts; the forced side has105. Complete incremental splitting produced respectively591214 and41482 full-dimensional cells. Every stage, trace and failure is retained. This primary algorithm's reported completeness is NOT the sole cover certificate.

The independent cover verifier instead starts from the final vertex sets, reconstructs the nine domain inequalities and210 proper cuts directly, and checks every cell's full dimension and fixed weak cut signs. Each cell center lies on no proper cut. All632696 strict cut-sign vectors are different, so distinct cell interiors are disjoint.

Within a cell, recursively cone one listed point over each supporting facet that does not contain it. A facet is an intersection with a valid supporting hyperplane and has the required exact affine rank. Repeated facets are deduplicated. The resulting simplices are contained in the cell and have disjoint relative interiors: radial projection from the chosen point meets at most one relative interior of an opposite supporting facet. This argument remains valid if a listed point is not extreme. Missing facets or vertices can only omit volume; no assumption that the primary vertex list is complete is needed for this lower-cover construction.

For homogeneous integer vertices v1,...,v8 with last coordinates M_i>0, seven-factorial times simplex volume is

    |det(v1,...,v8)| / product_i M_i.

Exact Bareiss determinants, denominator divisibility and all supporting-face ranks are checked with overflow refusal. The common denominator is L^8, L=5342931457063200, the exact lcm of every final vertex denominator. The maximum observed homogeneous simplex determinant is8, so global parameter unimodularity is explicitly NOT assumed.

The independent construction yields4209661 contained full-dimensional simplices. The exact sum of their seven-factorial volumes is7/576, which equals7! times vol(K). A finite closed subset of K with disjoint simplex interiors and that full volume must cover K: an omitted interior point would have an omitted open neighborhood of positive volume; boundary points follow from closedness and density of the interior. Thus every margin pair, including all boundaries and forcing strata, lies in the finite cover. A cell's containment in its strict cut-sign chamber, sign uniqueness and this coverage also establish that it is the complete closed chamber.

DATA/COMPLETE-COVER-VERIFIED.json records every batch and exact volume numerator/denominator. The full cell vertices, individual simplex vertex rosters, per-cell volumes and strict sign vectors are retained. This is an exact cover proof, not just a chamber count, an approximate volume test or a selected panel.

## 5. Full quadratic fields, polarization and all balancing directions

Use homogeneous physical coordinates y=(r1,r2,r3,c1,c2,c3,c4,M). On each of the632696 chambers, the complete low coefficient field has45 slots: one constant, eight linear coefficients and36 coefficients q_ij, i<=j, of a homogeneous quadratic

    12! a2(y)=q(y)=sum_(i<=j)q_ij y_i y_j.

These45 entries are NOT a full thirteen-entry ordinary polynomial. All complete source auxiliary rebases, every primary low field and every secondary field were saved before their sign or comparison tests. No known a1 formula was assigned into an output slot.

The primary construction sums all1024 signed original-offset assignment forms. An independently written algebraic construction expands each whole Newton product along six directions e1,e2,e3,e1+e2,e1+e3,e2+e3 and recovers its full constant, gradient and Hessian. It imports no primary evaluator. The exact secondary3920 low-jet entries and322560 physical assignment-template entries agree. A second whole-field census uses inverse-cone membership, direct linear substitutions and polarization, rather than the primary conditional selector and direct bilinear contraction. It reconstructs and matches all28471320 field positions. The freshly recounted atlas arrays in section3 equal the arrays used in both constructions.

For each chamber, let v_i denote all its integral generating rays. The complete polarization checks establish

    q(v_i)>=0,
    q(v_i+v_j)-q(v_i)-q(v_j)>=0 for every i,j.

There are46616414 unordered ray-pair checks, all nonnegative. Expanding q(sum a_i v_i) for arbitrary a_i>=0 proves a2>=0 on the entire cone, not only at the rays. Positive pure terms alone would not suffice; the complete mixed terms are included.

For column donor j<l in the sorted order, the homogeneous physical direction decreases c_j and increases c_l, keeping M androws fixed. The c5 coordinate is implicit. For each of all10 column pairs and every cone ray, the directional derivative is the polarization

    D_b q(v)=q(v+b)-q(v)-q(b).

All70084460 column-direction evaluations are nonnegative. Independently, all42050676 evaluations for the six row-balancing directions are nonnegative. Since these derivatives are linear in y, their nonnegativity on every cone generator proves their nonnegativity throughout each cone. A balancing segment is divided into finitely many cut/order pieces. Exact whole coefficient joins from section2 allow integration across all pieces, even when a segment lies on a wall. Genuine row and column permutations supply the needed sorted order on each piece. This proves every integer unit-transfer statement and the continuous balancing extension. No donor-largest assumption is used.

The entire result is a coefficient theorem obtained through a complete finite certificate. It does not claim a separate human reviewer; the different algorithms and count representations were used in this same research session.

## 6. Strictness on every actual-degree stratum

Across both domain parts there are15573 distinct primitive rays. Exactly15564 have strictly positive q, each of actual table dimension at least2. The other nine have q=0. Eight of those are point fibers. The only nonpoint zero ray is

    y=(1,1,0,1,1,0,0,2),

which is the2×2 segment with rows(1,1,0,0), columns(1,1,0,0,0). DATA/GLOBAL-RAY-QUADRATICS.json retains every full ray, original dimension and exact value; all repeated-ray restrictions agree.

Take a nonnegative ray representation of any margin pair in a covering cone. If some positively used ray has q>0, its positive diagonal term and all nonnegative mixed terms make q of the whole pair strictly positive. Otherwise every used summand is a point or a nonnegative multiple of that one fixed segment. Whole Minkowski equality then gives a point or a segment, of dimension at most1. Contrapositively, actual dimension at least2 forces a2>0. For dimension0 or1 the coefficient vanishes by the prior degree theorem. This argument covers arbitrary support subsets without enumerating exponentially many supports or imposing degree zeros in the evaluator.

## Mathematical references and dependency scope

[S1] [The complete table/LR map](whole-table-lr.md) and
[whole closed-boundary argument](closed-boundaries.md).

[S2] Haase, Juhnke-Kubitzke, Sanyal and Theobald, *Mixed Ehrhart polynomials*,
[arXiv:1509.02254v2](https://arxiv.org/abs/1509.02254v2), Theorem 2.3
(Bernstein–McMullen polynomiality). It includes zero coefficients and
lower-dimensional summands; it is not a mixed-sign theorem.

[S3] The [complete original-offset functional](original-offset-functional.md)
and the [seven-cone A3 argument](../../families-and-obstructions/proofs/transport-a3-premise.md).
The portable replay recomputes every one of the 392 complete degree-twelve
arrays from labeled-edge counts before contraction; no high Newton terms are
dropped before their original offsets are substituted.

[S4] Closed cut-cell coefficients on zero-column boundaries are actual whole
coefficients by the [closed-boundary proof](closed-boundaries.md). The sorted
full-dimensional cover is checked completely, including its boundary.
