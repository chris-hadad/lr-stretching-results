# Whole ordinary positivity for four-by-five transportation polytopes

## Theorem and exact endpoint

Let r=(r1,r2,r3,r4) and c=(c1,c2,c3,c4,c5) be nonnegative integer vectors with the same total M. Let

    T(r,c) = {X in R^(4×5): Xij>=0, row sums r, column sums c},
    P_(r,c)(t) = #(T(tr,tc) intersect Z^20) = sum_k a_k(r,c)t^k.

The lattice is the FULL affine integer table lattice and t is the ORIGINAL stretch. Every ordinary monomial coefficient a_k is nonnegative. After deleting zero margins, let p,N be the active numbers of rows and columns. If M=0, or p<=1 or N<=1, P=1. Otherwise its actual degree is d=(p-1)(N-1), and

    a_k(r,c)>0 for every 0<=k<=d;  a_k(r,c)=0 for k>d.

This includes every margin size, forcing region, cut equality, zero row, zero column and origin. It is the complete arbitrary-margin 4×5 endpoint, not a bounded positive panel. Genuine transposition gives the identical theorem for 5×4 tables. In particular all 3×5, 5×3 and 4×4 transportation polynomials, as well as their smaller active rectangles, are positive through actual degree.

There is also a uniform, nonsharp quantitative consequence. In the original active table lattice, write

    V_k(T) = sum_(F an actual k-dimensional face of T) vol_Z(F),

where vol_Z uses a fundamental lattice parallelepiped of volume one (not the convention multiplying by k!), and a point has volume one. An empty face roster contributes zero. Then, for every integer k>=4,

    a_k(T) >= (1/1000) V_k(T).                                      (1)

For k>d both sides are zero. For 4<=k<=d the face-volume sum is positive. This theorem does NOT assert coefficientwise balancing at indices k>=4, whole ordinary-rank-eight LR positivity, unrestricted KTT positivity, Hurwitz stability, or an ordinary-negative LR example.

The new ingredient is a small finite certificate in a single natural table metric. It contains 317 exact local constants, covering all 257,019 independent normal-subset occurrences needed to fill the previously unprotected coefficients. Every constant is strictly greater than 1/1000. The 15,288 dependent occurrences are separately certified as dependent. Independent exact local computations, an exhaustive combinatorial/lattice audit, and full whole-table controls verify this certificate. The already proved global low-coefficient theorems from Units 4 and 5 remain inherited, explicitly identified premises. Their complete proofs and original finite certificates are retained in the cumulative collection.

## 1. The entire table, original lattice, integrality and LR realization

For positive margins of an active p×N rectangle, the point Xij=ri cj/M is strictly positive in every coordinate. The p+N margin equations have exactly one dependency, so their affine solution space has dimension

    d=pN-p-N+1=(p-1)(N-1).

The table polytope is bounded: every entry lies between zero and its row margin. Strict positivity proves that no further affine equations have been silently imposed, even when some entries have positive forced minima. A zero margin forces its entire row or column to zero; delete such rows and columns before using this argument. With at most one active row or column the unique table gives P=1, including M=0.

Let z consist of the upper-left (p-1)×(N-1) entries. The omitted last-column and last-row entries are integer subtractions from the margins. The difference lattice is therefore the saturated lattice Z^d in this chart. Its full-table basis columns are

    B_ab=E_ab-E_aN-E_pb+E_pN,  a<p, b<N.                            (2)

Every zero-row-sum/zero-column-sum integer matrix has exactly one integer expansion in these columns, with coefficients its upper-left entries. This is an explicit integral inverse, not just a rank calculation.

A vertex cannot have a cycle in its positive bipartite support: an alternating signed perturbation around that cycle would remain feasible in both directions for sufficiently small magnitude. Its support is therefore a forest. On a forest, remove a leaf; the incident edge equals the corresponding remaining integer margin. Continue inductively. Thus every vertex is integral in the original affine lattice. Ordinary Ehrhart theory gives a genuine polynomial of degree d, with leading coefficient its positive lattice volume. No degree is inferred from a successful interpolation or from the ambient dimension of a larger hive.

Here is the complete ordinary LR lift for any active or padded p×N margins. Set R_i=sum_(a>=i)r_a and C_j=sum_(b>=j)c_b. With lambda the outer partition, take

    lambda=(M+R2,...,M+Rp,C1,...,CN),
    mu=(M repeated p-1 times,C2,...,CN),
    nu=(M,R2,...,Rp).                                             (3)

All are weakly decreasing nonnegative integral partitions and |lambda|=|mu|+|nu|. Construct the full partitions before trimming trailing zeros. For positive margins, the displayed ordinary rank is p+N-1: eight for 4×5 and seven for 3×5 or 4×4. The first p-1 skew rows share inner offset M and are forced superstandard with diagonal label counts R2,...,Rp. The remaining N skew rows are detached intervals of lengths c1,...,cN. Their label counts are exactly the columns of X. The initial buffer surplus between labels i and i+1 equals the entire remaining content of label i+1, so every lower ballot inequality holds for every table. Deleting the forced buffer rows is the inverse. Both maps are integral and homogeneous in the original stretch.

For completeness, the preserved source [S1] supplies the conventional-hive map, with a(i,j) denoting the number of labels i in row j:

    H(i,j)=sum_(v<=j)mu_v + sum_(u<=i)sum_(v=u..j)a(u,v),
    h(x,y)=H(y,x+y).

Its integer inverse is

    a(i,i)=h(0,i)-h(1,i-1),
    a(i,j)=h(j-i,i)+h(j-i,i-1)-h(j-i+1,i-1)-h(j-i-1,i), i<j.

All three rhombus orientations are, respectively, column slack, ballot slack and off-diagonal nonnegativity; the remaining diagonal nonnegativity follows from ballot and content. The source proves both real implications, including zero margins. Thus (3) is an entire real/integer correspondence, not an embedding into a proper face or merely a coincidence of finitely many counts. This theorem concerns precisely those whole LR polynomials; not every LR triple of the same displayed rank has this table form.

## 2. One rational metric on the entire table lattice

Let B be the pN-by-d matrix of (2). Give the table difference space the ordinary Euclidean inner product on all pN entries. Its matrix in the integral free chart is

    Q=B^T B,
    Q_(a,b),(u,v)=(delta_au+1)(delta_bv+1).                        (4)

This is a positive-definite rational metric, chosen once for each active rectangle and used for every face and cone in that rectangle. It is not changed to make an individual local constant favorable.

The full inward normal list consists of the pN rows n_ij of B. In the free chart these are coordinate unit vectors, negative row sums, negative column sums, and the positive sum of all coordinates. These are all original nonnegativity inequalities. An actual facet normal is among this list; removing a redundant inequality never introduces a new normal. Margins change the offsets, not this list or Q.

The orthogonal projection from all matrices to the zero-margin subspace subtracts each row mean and column mean and adds the grand mean. Applying it to coordinate matrices gives the dual Gram formula

    <n_ij,n_uv>_(Q^-1)
       = delta_iu delta_jv - delta_iu/N - delta_jv/p + 1/(pN).     (5)

Consequently the integer-scaled Gram pN H of any selected normals has diagonal d, off-diagonal 1-p for cells in the same row, 1-N for cells in the same column, and 1 for cells in different rows and columns. Formula (5) is also checked by a second construction that literally forms B, computes Q=B^T B, solves Qx=n^T, and contracts nQ^-1n^T. It does not obtain its Gram by copying the primary four-case formula.

Actual row and column permutations preserve the full matrix inner product and the integer zero-margin lattice. They are therefore lattice-preserving isometries of (4). Adjacent row and column transpositions generate these groups. All 19 such generators for the three needed active rectangles were checked by explicit integer free-chart matrices U: BU is the corresponding permuted B, U^2=I, and U^TQU=Q. No equal-Gram comparison with an unproved lattice identification is used in the final certificate. The square case is not further quotiented by transposition; extra safe types are simply retained.

## 3. Connectivity is exactly independence, and supplies the full quotient lattice

Choose a set S of cells and let G_S be the bipartite graph K_(p,N) with those edges REMOVED. Write N_S for the matrix of their selected normal rows. Then

    the rows N_S are independent  iff  G_S is connected.           (6)

Moreover, in the independent case,

    N_S : Z^d -> Z^|S| is surjective.                             (7)

To prove the forward-useful direction, suppose G_S is connected. Fix a selected edge e from a row i to a column j. Prescribe value one on e and zero on every other selected edge. In G_S choose a path from column j back to row i. Give its edges alternating signed integer values so that the resulting full matrix has every row and column sum zero. Its free coordinates are integral by (2), and N_S sends them to the coordinate unit vector associated to e. Repeating for all e gives an explicit integer right inverse. Therefore (7) holds and the rows are independent. The independent verifier retains each actual compensating path and free-chart right-inverse column and checks the full matrix reconstruction and every selected coordinate.

Conversely, suppose G_S is disconnected. Let A be one proper connected component. Summing zero row balances for row vertices in A and subtracting zero column balances for column vertices in A gives

    sum_(e in S) (1_(row(e) in A)-1_(column(e) in A)) n_e=0.        (8)

Every edge outside S lies within a component and cancels. At least one coefficient in (8) is nonzero, since the original complete bipartite graph is connected and A is proper. Thus the selected normals are dependent. The verifier supplies a literal nonzero relation (8) for EVERY excluded dependent subset, not just a reported rank or a floating singularity test.

For an independent S, (7) identifies the actual quotient lattice

    Z^d / (ker N_S intersect Z^d)  with  Z^|S|.

The dual-normal cone pos{n_e:e in S} has dual transverse cone equal, in the coordinates x=N_S z, to the standard nonnegative orthant. Its lattice is the FULL Z^|S|, not a sublattice. The half-open fundamental parallelepiped contains exactly its origin, every coordinate edge is primitive, and every coordinate-face fundamental volume is one. Every subset of S has a connected larger complementary graph and the same surjectivity property. All quotient stages of the local recursion therefore use the correct primitive axes and lattice numerators. This is why a simple numerator is justified here; it is not assumed for arbitrary hive normals or arbitrary equal-Gram cones.

## 4. Exact local Euler–Maclaurin constants, including every required jet

We use the Berline–Vergne local Euler–Maclaurin valuation with a rational metric [S2, Theorems 19–20, Definition 22, Corollary 23 and Theorem 26]. Its general analytic, translation, isometry and valuation properties are credited source theory. The present finite computation specializes that theory to the explicit orthants and original lattices just proved.

Let H be the positive-definite dual Gram of q independent selected normals. For a nonempty subset T, let H_T be its principal submatrix. Choose a vector w such that every coordinate of

    xi_T=H_T^(-1) w_T                                            (9)

is nonzero for every nonempty T. The programs search a finite explicitly tested list and refuse if no such choice is found. They do not perturb a zero denominator numerically.

Equation (9) is the compatible metric projection, not a separate arbitrary specialization on every face. On the full normal-coordinate dual space the scalar product is H and the initial covector is H^-1 w. Orthogonal projection to the subspace supported on T solves H_T xi_T=w_T. Further projections have the same formula. Equivalently the primal quotient metric is H_T^-1, as follows from the Schur complement. Hence every descendant in the recursion is evaluated at the projection of ONE covector under the SAME ambient metric.

For the orthant in coordinates T, its complete discrete and face-integral series along s xi_T are

    S_T(s)=product_(i in T) 1/(1-exp(s xi_(T,i))),
    I_U(s)=(-1)^|U| / (s^|U| product_(i in U)xi_(T,i)).              (10)

The lattice numerator is one and the face-volume factor is one by Section 3. Berline–Vergne's defining identity yields

    mu_empty=1,
    mu_T(s)=S_T(s)-sum_(empty!=U subset T) I_U(s) mu_(T\U)(s).       (11)

All nonempty removed faces U are included, including U=T. The required local constant is alpha(H)=[s^0]mu_full(s). Analyticity guarantees that the negative Laurent powers cancel; both implementations check every such cancellation exactly.

The primary implementation stores f_T=s^|T| mu_T with a COMMON upper degree q for every subset, not an upper degree equal to |T|. It multiplies the complete required expansion

    s/(1-exp(cs))=-1/c+s/2-c s^2/12+c^3 s^4/720
                  -c^5 s^6/30240+c^7 s^8/1209600+O(s^9).         (12)

Only terms up to the final required q<=8 are used. In normalized form each term I_U mu_(T\U), multiplied by s^|T|, is a constant times f_(T\U). Thus a common cutoff q is sufficient. In unnormalized form the child must be retained through positive order q-|T\U|: an integration pole can move its positive powers down to the parent's constant. Truncating a child at its own constant, or dropping the eighth-order term in (12), is wrong.

The secondary implementation does not import the primary recurrence or Bernoulli constants. It constructs the actual rational Gram by (4), uses exact LDL rather than Gauss–Jordan inversion for (9), and chooses a different signed specialization. For each c it forms

    (1-exp(cs))/s = -sum_(j>=0) c^(j+1)s^j/(j+1)!

and obtains the needed coefficients of its reciprocal by exact formal series division. It then uses direct Laurent exponents from -|T| through q-|T|, enumerating retained rather than removed subsets in (11). Every product, projection, division, pole cancellation and final coefficient uses arbitrary-precision rational arithmetic. There is no floating sign tolerance, modular reconstruction, fixed-width overflow assumption, omitted numerator, or imposed positivity.

Scaling H by pN scales the compatible covectors uniformly and does not change the degree-zero value. The primary uses pN H and positive-power specializations starting at base 17; the secondary uses H and different signed specializations starting at base 31. Their agreement thus also checks metric scaling and covector independence at every admitted type, while the analytic theorem justifies the independence in general.

For q=0 the constant is one. For q=1 it is one half. For a two-normal Gram with equal diagonal d and off-diagonal b, direct expansion of (11) gives

    alpha = 1/4-b/(6d).                                          (13)

For table normals b is one of 1-p,1-N,1, and b<=d. Thus every independent two-normal cone has alpha>=1/12. The connected-complement proof makes its quotient index one. All 821 q=1 or q=2 occurrences across every active subrectangle were checked against (13) or one half. This analytic top-three bound overlaps the inherited ternary-normal protection, but the present argument uses the single induced table metric directly.

## 5. The complete finite certificate

The only previously unprotected indices are 4,5 for active 3×5 tables, 4,5,6 for active 4×4, and 4,...,9 for active 4×5 [S3]. These correspond to the following codimensions q=d-k. EVERY subset of the full pN-cell normal list of each indicated size is retained and classified.

| Active rectangle | q | k=d-q | All subsets | Independent | Dependent | Safe row/column types |
|---|---:|---:|---:|---:|---:|---:|
|3×5|3|5|455|450|5|5|
|3×5|4|4|1,365|1,305|60|10|
|4×4|3|6|560|560|0|6|
|4×4|4|5|1,820|1,812|8|14|
|4×4|5|4|4,368|4,272|96|19|
|4×5|3|9|1,140|1,140|0|6|
|4×5|4|8|4,845|4,840|5|15|
|4×5|5|7|15,504|15,420|84|25|
|4×5|6|6|38,760|38,100|660|49|
|4×5|7|5|77,520|74,280|3,240|70|
|4×5|8|4|125,970|114,840|11,130|98|
|Total|||272,307|257,019|15,288|317|

The primary topology program enumerates all fixed-popcount bitmasks and uses complementary-graph union–find. To obtain a safe class representative it considers every row permutation and then sorts the resulting column bit-vectors. It saves the literal row permutation and column permutation for every independent subset. Equal canonical graphs therefore identify only actual integral metric isometries; no high-index Gram identification is substituted.

A separately written verifier instead enumerates all combinations of cells recursively and tests complementary connectivity by breadth-first search. It checks the full binomial population size, absence of duplicates or omissions, every row/column permutation witness, every class multiplicity, and the correspondence with the retained representative. It constructs (8) for each dependent subset and explicit integer right inverses for each representative. The same permutation carries those inverses to every occurrence. Section 2 proves that these permutations preserve the entire ambient lattice and metric. Thus each accepted local value has a complete population, original-lattice and isometry justification.

The complete arrays are printed in the companion certificate appendix and stored in DATA/LOCAL-CERTIFICATE.json. No zero or negative type is omitted: all 317 final values are positive and all primary values were persisted before any comparison. Their exact minima, in the row order above, are

    7/72,
    4043/86940,
    1/10,
    4819/118800,
    64619/2882880,
    11/104,
    739/16380,
    51171551/2354395680,
    49823847600697477/4315686954189811200,
    266446490874824818540889/42754826237980312750694400,
    160895356850988106001219145739/55646261445256136651283775488000.

The last is the overall minimum, at type 92 of the 4×5, q=8 roster. Exact rational comparison proves that every minimum is strictly greater than 1/1000. No sharpness of that convenient common lower bound is asserted.


## 6. From all listed simplicial cones to EVERY actual face

Fix integral margins of an active rectangle and an actual face F of dimension k. The integral-polytope argument supplies an integral vertex on F. Translate by that vertex. The transverse cone along F now has integral apex zero in the quotient of the original table lattice. Its inward normal cone sigma_F has dimension q=d-k and is generated by actual original facet normals from the full list of Section 2.

A pointed polyhedral cone has a triangulation into full-dimensional simplicial cones using its extreme rays: cut it by an affine hyperplane positive on all its rays and use a vertex triangulation of the resulting compact polytope, then cone back. Consequently sigma_F has such a triangulation whose full-dimensional pieces are generated by q independent ORIGINAL table normals. Section 3 identifies each piece's actual quotient lattice; Section 5 includes every required piece, whether or not that piece ever occurs alone as a complete face cone.

This subdivision occurs in the NORMAL cone. Berline–Vergne's dual-solid valuation, Definition 22 and Corollary 23 [S2], gives

    alpha(F)=mu_0^*(sigma_F)(0)
            =sum_(full-dimensional simplices sigma' in the subdivision)
                    mu_0^*(sigma')(0).                           (14)

There are no negative lower-dimensional correction terms in (14). In the fixed quotient by the annihilator of span(sigma_F), the dual of a lower-dimensional subdivision cell contains a line, and its mu-value is zero. This is the reason for dual-solid additivity. It is NOT an appeal to continuity of Ehrhart coefficients under perturbation, and it is NOT a claim that an arbitrary triangulation of the primal polytope preserves coefficients without boundary terms.

All terms in (14) use the same rational metric and quotient lattice system. Each term equals one of the verified local constants. At least one full-dimensional piece exists. For the tested q, therefore,

    alpha(F) >= min_(all listed q-types) alpha > 1/1000.           (15)

For q=0,1,2, the analytic constants and bound from Section 4 give the same weaker inequality with 1/1000. This covers every needed index k>=4 on every active subrectangle. In dimensions at most six such indices are already among q<=2; in dimensions eight, nine and twelve the remaining cases are precisely the eleven rows of Section 5.

Apply the local Euler–Maclaurin formula to the constant function one on tT. Derivatives of a constant vanish, leaving the value at zero of each transverse-cone symbol times the lattice volume of the corresponding face. Because T is integral, translation by a vertex of F makes its transverse cone constant under every integer dilation; integer-translation invariance removes any periodic apex term. Thus

    a_k(T)=sum_(dim F=k) alpha(F) vol_Z(F).                         (16)

Combining (15), the analytic q<=2 bounds and (16) proves (1). For k<=d an actual k-face exists, its relative lattice volume is positive, and so a_k>0. For k>d no such face exists and polynomial degree gives a_k=0. No enumeration of every possible margin or actual face is needed beyond the exhaustive finite normal-subset certificate and the all-margin structural argument.

## 7. Completing all ordinary coefficients

The constant coefficient is one for every nonempty lattice polytope. Balanced nonnegative complete-table margins are always feasible; one can allocate greedily, or use the positive product point on the active rectangle and integrality. Point cases remain P=1.

The [closed nonnegative-margin linear proof](linear-four-by-five.md#closed-nonnegative-margins-and-every-active-subrectangle) proves a1>0 whenever d>=1. It extends the complete N=5 first-jet equality through the supplied whole closed-Minkowski theorem and uses a positive separating double cut; no omitted N=4 certificate is needed. The [quadratic proof](quadratic.md) proves a2>0 exactly when d>=2, and the [cubic proof](cubic.md) proves a3>0 exactly when d>=3, on the ENTIRE arbitrary-margin 4×5 domain, with all zero and forcing boundaries. These are established coefficient theorems, not conjectures inferred from the present numerical controls. Their complete public arguments and finite premises are listed in [S3].

For clarity, those low-coefficient certificates use a different, already completed finite reduction: a complete 632,696-chamber cover of the sorted normalized margin domain with 4,209,661 contained simplices, full original-offset A3 assignment fields, and ALL generator-polarization and balancing checks at their stated degrees. The whole closed-Minkowski argument identifies those fields on boundaries. Unit 5's 57 full count controls are distinct from its entire cubic field census. This unit authenticates and inherits that completed proof, not relabels it as a newly rerun global chamber computation.

The present local theorem supplies every coefficient of index at least four. Combining the four cases k=0, k=1,2,3 and k>=4 proves all assertions of the main theorem. Strictness is exactly through actual degree. The maximal dimensions occurring after deletion are twelve (4×5), nine (4×4) and eight (3×5); all smaller rectangles have degree at most six. Thus no boundary coefficient or intermediate degree is unhandled.

This is a complete finite, computer-assisted proof of the unbounded endpoint. It does not require a quartic field on each margin chamber, a general majorization theorem, a claim of positive cap intersections, or unreturned work from another mission.

## Mathematical references and dependency scope

[S1] [Complete whole table/LR correspondence](whole-table-lr.md).

[S2] Berline and Vergne, *Local Euler–Maclaurin formula for polytopes*,
[arXiv:math/0507256v3](https://arxiv.org/abs/math/0507256v3): Theorems 19–20,
Definition 22, Corollary 23 and Theorem 26. The metric, saturated quotient
lattice and face-volume normalization are specified above.

[S3] Complete [quadratic](quadratic.md), [cubic](cubic.md), and
[linear](linear-four-by-five.md) arguments. The companion dataset and portable
replay supply the whole finite premises used here. The linear proof's original
154 vanishing chamber gradients are also freshly checked in the template
builder from all original-offset Newton terms.
