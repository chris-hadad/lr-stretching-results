# Global cubic positivity and two-sided balancing for four-by-five transportation polynomials

## Theorem, whole-object scope and consequences

Let r=(r1,r2,r3,r4) and c=(c1,c2,c3,c4,c5) be nonnegative integral margins with common total M. Let T(r,c) be the ENTIRE set of nonnegative real 4-by-5 matrices having those row and column sums. Use its full affine integer table lattice and ORIGINAL stretch:

    P_(r,c)(t) = #(T(tr,tc) intersect Z^20) = sum_k a_k(r,c)t^k.

Then a3(r,c)>=0 at every margin size, including every zero-margin, forcing, equality and origin boundary. If d is the actual dimension, a3>0 exactly when d>=3. Points and lower-degree fibers have a3=0. The degree bound is established before counting; it is not inferred from a fitted vector.

At fixed rows, every legal unit balancing of ANY two columns is nondecreasing for this cubic coefficient:

    a3(r,c-e_j+e_l) >= a3(r,c) whenever c_j>=c_l+2.

The same assertion holds for any pair of rows at fixed columns. The donor need not be largest. More generally, the homogeneous piecewise-cubic coefficient function is nondecreasing on continuous balancing segments up to equality. This real coefficient extension does not assert period-one Ehrhart counting for arbitrary rational margins without the appropriate original grading.

For strictly positive integral four-row/five-column margins of total M>=5, the sharp minimum is attained by

    r=(M-3,1,1,1), c=(M-4,1,1,1,1),

and equals

    M=5:   5005039/362880,
    M=6:   221771/13440,
    M>=7:  1271281/75600.

These three values increase strictly. Thus the sharp positive-integral minimum over all totals is 5005039/362880. Simultaneously balanced integral rows and columns maximize a3 at any fixed total. The extremal assertions are cubic-coefficient statements, not whole-polynomial majorization.

There is a whole-polynomial consequence: every entire 3-by-4 or 4-by-3 transportation polynomial is strictly positive through its actual degree, with the constant-one convention for point fibers. More generally, this closes every 4-by-5 member of actual dimension at most six. Section 7 derives this using the NEW cubic result together with the precisely credited prior linear, quadratic and intrinsic third-highest-coefficient theorems. It is not a theorem for every ordinary-rank-six LR triple and uses no unreturned Pro028 work.

The main arbitrary-margin whole-coefficient endpoint remains open. After the results here and the stated existing protections, the remaining indices are 4,5 for active 3-by-5 tables, 4,5,6 for active 4-by-4 tables, and 4 through 9 for active 4-by-5 tables. These are the potentially unprotected indices, not claims that a negative occurs. Their transposed table polynomials are identical. No fourth-degree production was started in this unit.

## 1. Complete LR realization, saturated lattice, and degree

For the labeled margins, put R_i=sum_(a>=i)r_a and C_j=sum_(b>=j)c_b. With lambda outer, a whole ordinary LR constructor is

    lambda=(M+R2,M+R3,M+R4,C1,C2,C3,C4,C5),
    mu=(M,M,M,C2,C3,C4,C5),
    nu=(M,R2,R3,R4).

These are weakly decreasing nonnegative integral partitions and their areas balance. Trim trailing zeros only AFTER constructing them. Positive five-column margins give displayed ordinary rank eight; zero margins can change the trimmed rank. This does not identify every rank-eight LR fiber with a table fiber.

The first three skew rows have common inner offset M and are forced superstandard with diagonal label counts R2,R3,R4. The five remaining skew rows are mutually detached column intervals of lengths c1,...,c5. Their label counts are precisely the table entries. The initial surplus between adjacent labels is the entire remaining content of the higher label, so every subsequent ballot inequality is automatically satisfied by every table. Deleting the three forced rows is the inverse. Thus neither a selected face nor extra unrestricted tableaux are substituted for the whole object.

For the conventional hive at padding eight, write a(i,j) for the number of labels i in row j and set

    H(i,j)=sum_(v<=j)mu_v + sum_(u<=i)sum_(v=u..j)a(u,v),
    h(x,y)=H(y,x+y).

The inverse is a(i,i)=h(0,i)-h(1,i-1) and, for i<j,

    a(i,j)=h(j-i,i)+h(j-i,i-1)-h(j-i+1,i-1)-h(j-i-1,i).

The three rhombus types are the column, ballot and off-diagonal nonnegativity inequalities. Diagonal nonnegativity follows from the remaining ballot inequalities and content; the other boundary inequalities are partition inequalities. The complete source proof [S1] supplies both real implications and the integer inverse, including zeros. Hence the original entire real polytopes and affine integer lattices correspond homogeneously at every stretch.

With positive margins, X_ij=r_i c_j/M is strictly positive. Eight independent margin equations leave dimension twelve. The upper-left 3-by-4 entries are a saturated integer chart: every omitted last-row/last-column entry is an integral subtraction from the margins. Its difference lattice has basis E_ij-E_i5-E_4j+E_45. Every vertex has forest support in the bipartite incidence graph, since a cycle permits a small two-sided alternating perturbation. Leaf elimination on a forest solves the margin equations integrally. Therefore the table is a lattice polytope in its ORIGINAL affine lattice, and ordinary Ehrhart degree equals twelve. Delete forced-zero rows and columns for active sizes p,N; the same proof gives d=(p-1)(N-1). If either active size is at most one, including M=0, the fiber is a point with polynomial one. All 13 slots are retained in the numerical whole controls.

## 2. The inherited complete domain and why its boundary fields are actual coefficients

For two margin pairs, the whole Minkowski criterion is compatibility of all weak cut signs h_(I,J)=r(I)-c(J). To extract a component table Y from a given table X in the sum fiber, impose 0<=Y<=X in the complete source-row-column-sink network. The min-cut inequalities are block lower bounds. The exact minimum of block X(I,J) in a complete fiber of total M is max(0,r(I)+c(J)-M); aggregation to a 2-by-2 table and distribution of each block proves attainment, including zero groups. Applying a cut and its complement proves that compatible signs are equivalent to the whole real Minkowski equality. The reverse inclusion is immediate [S1].

Consequently, on a closed cone generated by integral margin rays v_i with compatible signs,

    T(sum_i z_i v_i)=sum_i z_i T(v_i), z_i>=0.

Subtract integral tables on the generating rays to place all summands in the same saturated kernel lattice, keeping each smaller affine span. Bernstein-McMullen multivariate Ehrhart polynomiality [S2, Theorem 2.3] then provides one count polynomial for ALL nonnegative integral z, including faces and zero summands. Its total degree is at most twelve. No coefficient positivity is supplied by that theorem. Rational nonnegative ray coordinates are treated by denominator clearing and P_(qr,qc)(t)=P_(r,c)(qt); a3 scales by q^3. Parameter-cone index is not table-lattice index. This proves the actual whole coefficient on each closed boundary without assuming continuity of an individual signed assignment term.

Unit 4 already supplies an exact complete cover of the normalized SORTED domain K. In affine coordinates x=(r1,r2,r3,c1,c2,c3,c4), put r4=1-r1-r2-r3 and c5=1-c1-c2-c3-c4. K is the product of the two ordered simplices, defined by the four row-order/nonnegative-last-row inequalities and five column-order/nonnegative-last-column inequalities. Its exact volume is 1/414720. All 512 labeled cuts are controlled by 210 unoriented proper hyperplanes and the nonnegative margin inequalities.

The source cover has 591,214 unforced-side cells and 41,482 forced-side cells, hence 632,696 closed chambers. Its independent verification uses cell containment, distinct strict interior cut-sign vectors, and 4,209,661 disjoint contained simplices. Their exact total volume equals vol(K). A finite closed contained union of that volume covers every interior point, since an omitted interior point would have an omitted open neighborhood; density and closedness then cover all boundary points. The determinant bound observed there is eight, so no universal parameter unimodularity is assumed. The exact source argument, vertices, simplices and independent volume receipts are preserved in the U04 base.

THIS UNIT authenticates the complete U04 core and supplement and uses that previously verified cover as a load-bearing inherited certificate. It does not claim a fresh regeneration of every geometry step or volume determinant. The two exact state files and their hashes are in CUBIC-FULL-WORKLOAD.json; all current field intervals cover each state without a gap or overlap. Every one of their 15,573 distinct primitive margin rays has its cubic restrictions reconciled across all occurrences.

## 3. Entire original-offset assignment formula and cubic extraction

The complete table count is the coefficient of x^(tr) in product_j h_(tc_j)(x1,x2,x3,x4). The elementary partial-fraction identity

    h_m(x)=sum_i x_i^(m+3)/product_(k!=i)(x_i-x_k)

gives all 4^5=1,024 labeled assignments f of the five columns to four labels 0,...,3. If n_i=#f^(-1)(i), keep sign (-1)^sum_j f(j), slope beta_i=sum_(j:f(j)=i)c_j-r_i, and EXACT ORIGINAL offset

    delta_i=i n_i-sum_(j>i)n_j.

The ordered A3 expansion has 15 labeled root variables, with multiplicity n_i+n_j on root i<j and saturated incidence rank three. In simple-root coordinates its offset is

    d=(-n1-n2-n3,-2(n2+n3),-3n3),

and slope is (beta0,beta0+beta1,-beta3). No occupation class, cap term or offset is dropped. The seven unimodular source cones provide a common refinement for all 56 occupations. Unsupported open cones have the zero polynomial. The whole count agrees eventually on a generic ray with the signed sum of the full chamber polynomials; polynomial identity in the original stretch extends equality to all grades [S3]. Section 2 gives the whole closed-boundary extension.

The accepted full data have 392 arrays, each containing 455 Newton coefficients for total degree at most twelve. Unit 4 independently recounted every array from 178,360 determining lattice counts and 1,568 reserved checks. We inherit that complete count evidence, rather than relabel it a new U05 recount. In this unit the primary cubic jets come from the entire original-offset rebases of those polynomials. The secondary jets are freshly derived from ALL 455 Newton entries, substituting the exact offset BEFORE truncating to degree three.

For a chamber matrix V whose columns are its three rays, write its complete polynomial as

    K(V(1+u))=sum_(i+j+k<=12) N_ijk binom(u1,i)binom(u2,j)binom(u3,k).

To extract the cubic along direction w, insert u=V^(-1)(d+t w)-1 into every term and keep [t^3] after multiplying the three complete falling-factorial expressions. This includes contributions from Newton terms of degrees greater than three; truncating the original array to its first cubic entries would be wrong. The denominator 12!=479001600 clears every i!j!k! because i+j+k<=12. All calculations use exact integer arithmetic.

Ten evaluations determine a homogeneous cubic in three variables: e1,e2,e3; e1+e2,e1-e2,e1+e3,e1-e3,e2+e3,e2-e3; and (1,1,1). For i<j, the coefficients of x_i^2 x_j and x_i x_j^2 are respectively

    (q(ei+ej)-q(ei-ej)-2q(ej))/2,
    (q(ei+ej)+q(ei-ej)-2q(ei))/2.

The coefficient of x1 x2 x3 is the value at (1,1,1) minus the other nine coefficients. Directions with a negative component here are evaluations of a chamber POLYNOMIAL continuation, not assertions about a negative-netflow count. The seven inverses are derived exactly from their ray matrices and checked in both multiplication directions. All 3,920 cubic-jet positions agree with the primary after both complete arrays are saved.

Physical coordinates are y=(r1,r2,r3,c1,c2,c3,c4,M), with the last row and column implicit. Primary substitution expands each signed root cubic directly into its 120 physical monomials. A second implementation instead uses full cubic polarization on the three-vector images of the eight physical coordinates. Its 1,024 x 7 x 120 = 860,160 template entries agree exactly. The secondary template is frozen before opening the primary template for comparison. These are two different exact arithmetic constructions on the independently recounted source atlas, not two new complete lattice-counting representations for every margin chamber.

At each chamber's strict interior center, the primary conditional selector and a separate inverse-cone membership selector choose the supported auxiliary cone. Summing every selected assignment gives the complete cubic field

    q(y)=12! a3(y)=sum_(0<=i<=j<=k<8) q_ijk y_i y_j y_k.

The field is written and flushed before sign tests or comparison. Every field has all 120 signed PHYSICAL coefficients, not a favorable subset. Negative entries in that physical basis would not themselves be a negative original stretching coefficient. Across the complete cover, all 75,923,520 entries match the secondary reconstruction. The original-offset auxiliary jets themselves retain 1,140 negative positions; their existence is not a whole-LR counterexample.

## 4. Complete cubic and balancing certificates, including mixed terms

Let S=D^3 q be the constant symmetric trilinear form associated to q. Then

    q(y)=S(y,y,y)/6,   D_b q(y)=S(b,y,y)/2.

For the coefficient convention above, S_iii=6q_iii, S_iij=2q_iij for repeated indices, and S_ijk=q_ijk for distinct indices. All permutations are included. If y=sum_i z_i v_i in a covering cone, z_i>=0, then

    q(y)=(1/6) sum_(i,j,k) z_i z_j z_k S(v_i,v_j,v_k).

Thus the nonnegativity of EVERY unordered repeated-index triple of generators proves the sign on the whole cone. Checking only pure generators, or even only pairs, would not prove a cubic sign.

All 248,939,603 such trilinear values over the complete cover are nonnegative. For each of the ten sorted column-pair balancing directions b, every S(b,v_i,v_j), i<=j, is also nonnegative. There are 466,164,140 column-direction checks. Independently, the six row-pair directions give 279,698,484 checks, all nonnegative. These directions hold total and the other margin vector fixed, with the implicit last coordinate handled by subtraction. They do NOT change the stretch parameter.

The directional field is a quadratic in y. Expanding it in nonnegative generator coordinates using all pair checks proves its nonnegativity throughout the cone. Divide a balancing segment into finitely many cut/order pieces. The whole coefficient joins from section 2 agree at every common face, including a segment lying on a wall. Integrating the nonnegative directional derivative on each piece proves the continuous and integer balancing statements. Row and column reorderings are actual table coordinate permutations. No largest-donor hypothesis or strict positive linear increment is required.

The second sign implementation reads only each frozen physical cubic and the inherited geometric state. It forms its Hessian by differentiating each monomial twice over all ordered pairs of its three label positions. This treats multiplicities independently of the primary symmetric-tensor construction. It then contracts each Hessian with all the same complete generator pairs/triples and the sixteen balancing directions. Every interval, check count and verdict agrees. Per-cell minima and all adverse-output files are retained; the latter are empty for these complete cubic criteria.

Fixed-width arithmetic is bounded explicitly. Template entries have observed absolute maximum 4,331,250,000; production refuses a template maximum greater than 10^12 or a vertex coordinate greater than 10^6. A whole field is a sum of 1,024 such entries, with checked int64 narrowing. The tensor entries have the factor at most six. Every contraction has at most 512 summands and three vertex factors, so 512*6*1024*10^12*10^18 < 2^127. This bounds the signed-128 arithmetic without relying on an empirical absence of overflow. The actual maximal vertex coordinate is 42. Headers, ranges, every field ID and exact file lengths are checked. The independent Hessian checker enforces the corresponding field and coordinate bounds. Outside these declared engineering bounds no count or sign is manufactured.

The 13 production intervals consist of twelve unforced batches and one forced batch. Their boundaries exactly partition 591,214 and 41,482 cells. Complete counts are:

    fields:                       632,696
    cubic physical positions:  75,923,520
    generator triples:        248,939,603
    generator pairs:           46,616,414
    column mixed derivatives: 466,164,140
    row mixed derivatives:    279,698,484.

These are nonadditive certificate occurrences, not distinct polynomials or original-box coverage. Pilots and repeated secondary runs overlap them and are not added as extra proof coverage.

## 5. Genuine whole-count controls and strictness on all active sizes

The complete unsigned table recurrence counts the coefficients of
`product_j h_(t c_j)(1,z1,z2,z3)`, with every nonnegative allocation of each
column retained. The omitted row is fixed by total balance. The replay here
reconstructs the 17 indispensable baselines below at grades 0 through 12 and
checks unused grades 13 and 14. It saves all 13 ordinary coefficients before
any sign or comparison test. These baselines suffice for the strictness proof;
additional historical illustrative control vectors are not required inputs.

For strictness, delete zero margins. At active p,N>=2, all positive integral margins of fixed total M are reachable from the pair of most unequal positive margins

    (M-p+1,1^(p-1)), (M-N+1,1^(N-1))

by legal balancing moves. To see this constructively for a target sorted vector, fill its recipients from the first entry. While a recipient remains deficient, its target is at most the first target; the donor includes the remaining total deficit, so the donor-recipient gap before a needed unit move is at least two. Repeat for the rows and then columns. The already proved cubic balancing therefore reduces strictness to these extreme baselines.

For M>=p+N-2 the (1,1) coordinate has forced minimum M-(p+N-2). Subtract it. This is a whole affine integral translation, reducing the extreme pair to total p+N-2, not a face or merely a scalar stabilization. It preserves the polynomial and actual degree. For p<=4,N<=5 and d=(p-1)(N-1)>=3, only the following 17 baseline cases remain. Every listed value comes from one of the NEW complete whole-vector reconstructions with both unused checks:

| p | N | M | a3 |
|---:|---:|---:|---:|
|2|4|4|1/6|
|2|5|5|5/12|
|3|3|3|3/4|
|3|3|4|1|
|3|4|4|11/4|
|3|4|5|49/16|
|3|5|5|169/32|
|3|5|6|4037/720|
|4|2|4|1/6|
|4|3|4|11/4|
|4|3|5|49/16|
|4|4|4|35117/5670|
|4|4|5|797089/90720|
|4|4|6|13777/1512|
|4|5|5|5005039/362880|
|4|5|6|221771/13440|
|4|5|7|1271281/75600|

All are strictly positive. This proves a3>0 for every integral member of actual dimension at least three. For d<3 it is zero by degree. Rational ray directions follow by common denominator clearing if needed. The 15 zero cubic generator rays have dimensions 0,1,2, but their dimensions ALONE would not establish the strictness theorem: sums can increase dimension. The complete extremal-baseline argument avoids that invalid shortcut.

## Mathematical references and dependency scope

[S1] [Complete table/LR map](whole-table-lr.md) and
[whole closed-boundary argument](closed-boundaries.md).

[S2] Haase, Juhnke-Kubitzke, Sanyal and Theobald, *Mixed Ehrhart polynomials*,
[arXiv:1509.02254v2](https://arxiv.org/abs/1509.02254v2), Theorem 2.3.

[S3] [Full original-offset functional](original-offset-functional.md),
[seven-cone A3 proof](../../families-and-obstructions/proofs/transport-a3-premise.md),
and the freshly reconstructed complete atlas in the portable replay.

The selected cubic argument ends after the complete 17-baseline strictness
proof. Additional source theorems about intrinsic ternary cones and sharp
extrema are not premises of this selected result. All quadratic cover and
boundary inputs are supplied by [the preceding proof](quadratic.md).
