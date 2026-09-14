# Whole transportation and capped-family positivity

Computer-assisted finite certificates in the original integer lattices. The accompanying verifier reconstructs every original normal subset and every rational inequality. This note states the complete mathematical implication; independent reproduction and review are reported in README.md.

## Statements

**T1. Whole transportation.** Every balanced nonnegative integral transportation polytope with at most three rows and at most five columns, or its transpose, has nonnegative ordinary Ehrhart coefficients. Every coefficient through its actual degree is strictly positive. Zero rows and columns are allowed; a point has polynomial one. This also proves positivity of the ENTIRE ordinary LR polynomial given by the exact constructor below, at every area. It is not every ordinary rank-seven LR polynomial.

For the full three-by-five presentation in the eight free integer coordinates, the quantitative statement is

    c_k >= (1/1000000) sum_(actual k-faces F) vol_Z(F), 1<=k<=8.     (1)

A third complete q7 field supplies the linear coefficient locally. The earlier the earlier all-size linear-coefficient argument equality with the complete positive double-cut functional and its stronger linear bounds retain their separate credit and active-margin deletion convention. On a three-by-four presentation the stronger raw certificate gives the analogous bound with 1/720 for every 1<=k<=6.

**T2. Whole capped family.** Let 1<=m<=4 and w_1,...,w_m,c,d be nonnegative integers with sum w>=c+d. Count all nonnegative integer vectors y,z with

    sum z_i=c t,  sum y_i<=d t,  y_i+z_i<=w_i t.                   (2)

Its whole polynomial has nonnegative ordinary coefficients, strictly positive through actual degree. In the seven-coordinate m=4 presentation the quantitative bound is

    c_k >= (1/300) sum_(actual k-faces F) vol_Z(F), 1<=k<=7.       (3)

For four positive capacities with c,d>0 the actual degree is seven. Empty capacities and zero c/d retain their actual dimension drops. This removes the free-capacity floor from the preceding capped-family derivation's whole-polynomial result at m<=4. The earlier all-m linear bound c1>=d remains a separate stronger statement about c1; no higher-coefficient assertion for arbitrary m follows here.

For any h,u,v with 0<=c<=h and u,v>=h+d, put s=sum w and U=u+v. The entire ordinary LR triple for (2) is

    lambda=(s+U-h,s+v,suffix_1(w),...,suffix_m(w)),
    mu=(s+v-h,s,suffix_2(w),...,suffix_m(w),0),
    nu=(U+s-h-d-c,h+d,c).                                      (4)

All input partitions are balanced and dominant at these conditions. The original integer stretch and every lattice point are preserved. Rank is at most m+2, hence at most six; for positive four-capacity interiors it is a rank-six, degree-seven family. The general short-inner-three LR problem remains open.

## 1. Complete original polytopes and lattices

For a p-by-N transportation polytope, take the upper-left (p-1)-by-(N-1) entries as free integer coordinates x_ij. The remaining entries are

    x_iN=r_i-sum_(j<N)x_ij,
    x_pj=c_j-sum_(i<p)x_ij,
    x_pN=r_p-sum_(j<N)c_j+sum_(i<p,j<N)x_ij.

Nonnegativity of ALL p*N entries gives the complete inequality system. The normal rows are minus each free coordinate, plus each free-row sum, plus each free-column sum, and minus the total free sum. There are 12 rows in Z^6 for 3-by-4, and 15 rows in Z^8 for 3-by-5. No sampled redundant facet is removed. This map is a bijection of the entire real fibers and their affine integer lattices. With positive margins, x_ij=r_i*c_j/M gives a strictly positive point, so the actual dimension is (p-1)(N-1). Incidence matrices of bipartite graphs are totally unimodular after changing signs on one vertex class: every square minor has determinant zero or plus/minus one, by removing a column with at most one nonzero entry or observing a row dependence when every column has both entries. The transportation vertices are therefore integral. Boundedness follows from 0<=x_ij<=min(r_i,c_j).

For m=4 in (2), eliminate z_4=c-sum_(i<4)z_i. The ORIGINAL free lattice is Z^7, in order (y_1,y_2,y_3,y_4,z_1,z_2,z_3). Its 13 inequalities are

    -y_i<=0 (four),  -z_i<=0 (three),  sum_(i<4)z_i<=c,
    y_i+z_i<=w_i (i<4),  y_4-sum_(i<4)z_i<=w_4-c,
    sum_i y_i<=d.

These are complete, including every capacity. Integrality can also be seen by an exact transportation-face representation: for each original column i use entries (z_i,y_i,w_i-z_i-y_i), append a column (0, d-sum y, sum y), and use row totals (c,d,s-c) and column totals (w_1,...,w_m,d). This is the entire face with its top appended entry zero. Its inverse forgets the forced coordinates, so both maps preserve the full lattice. All vertices are integral by the bipartite incidence argument. This representation is used for integrality only; a face theorem is not being substituted for a whole-LR theorem. The independent full count identity (4) supplies the LR interpretation.

The capped set is nonempty: distribute c among capacities and take y=0. It is bounded. If all four w_i,c,d are positive, choose z_i=c*w_i/s and y_i=eta*w_i with 0<eta<min(d/s,1-c/s); this makes every displayed inequality strict, even when s=c+d. Thus its actual dimension is seven. The remaining boundary cases need no guessed dimension; (3) concerns actual faces in the original saturated lattice.

## 2. The complete finite normal predicates

For each original normal matrix, every q-subset is classified as independent or dependent, with no sampling or orbit omission. Euclidean inner product is used in exactly the free coordinate lattice just specified. For an independent row matrix N, the image lattice N Z^D has index one. The Python verifier checks a complete nonzero minor and, when necessary, the gcd of maximal minors. The C++ program separately uses integer column reduction. At index one the whole normal-coordinate image lattice and each coordinate projection are saturated, so a generator-permuted Gram matrix identifies the full lattice and metric.

The finite raw results are:

| System | q | All subsets | Independent | Dependent | Minimum raw weight | Negative weights |
| --- | --- | --- | --- | --- | --- | --- |
| Capped m=4 | 1 | 13 | 13 | 0 | 1/2 | 0 |
| Capped m=4 | 2 | 78 | 78 | 0 | 7/48 | 0 |
| Capped m=4 | 3 | 286 | 282 | 4 | 1/24 | 0 |
| Capped m=4 | 4 | 715 | 674 | 41 | 1/64 | 0 |
| Capped m=4 | 5 | 1287 | 1092 | 195 | 1613/244800 | 0 |
| Capped m=4 | 6 | 1716 | 1152 | 564 | 2298481/605404800 | 0 |
| Transport 3-by-4 | 1 | 12 | 12 | 0 | 1/2 | 0 |
| Transport 3-by-4 | 2 | 66 | 66 | 0 | 11/72 | 0 |
| Transport 3-by-4 | 3 | 220 | 216 | 4 | 1/24 | 0 |
| Transport 3-by-4 | 4 | 495 | 456 | 39 | 127/14400 | 0 |
| Transport 3-by-4 | 5 | 792 | 612 | 180 | 1/720 | 0 |
| Transport 3-by-5 | 1 | 15 | 15 | 0 | 1/2 | 0 |
| Transport 3-by-5 | 2 | 105 | 105 | 0 | 5/32 | 0 |
| Transport 3-by-5 | 3 | 455 | 450 | 5 | 1/24 | 0 |
| Transport 3-by-5 | 4 | 1365 | 1305 | 60 | 83/13440 | 0 |
| Transport 3-by-5 | 5 | 3003 | 2670 | 333 | -7/2400 | 70 |
| Transport 3-by-5 | 6 | 5005 | 3870 | 1135 | -59/15680 | 56 |
| Transport 3-by-5 | 7 | 6435 | 3780 | 2655 | -1/448 | 28 |

There are 16,848 independent local constants across these three presentations. These are auxiliary normal cones, not counted LR triples. No number is added to the historical campaign coverage.

The raw recurrence is the fully stated image-lattice Euler-Maclaurin recurrence in the local recurrence in Section 6 below. The included independent Python and C++ implementations use normalized Taylor coefficients through order seven. Bernoulli B7 is zero, and B8 first affects cutoff eight, so all required terms are retained. Neither program claims validity above order seven. The executable normal generators are in arithmetic.py; every original subset and type assignment is rebuilt by verify.py. Pole cancellation, all proper-face terms, the degree-six Bernoulli term, lattice indices and original normals are retained. Positivity is NOT inferred merely from unimodularity.

## 3. Complete 3-by-5 corrections

Raw positivity fails at q=5, q=6 and q=7. The complete allowed field assigns one rational linear functional to every independent (q-1)-normal support J. Let M_J be a D-by-(D-q+1) integer basis for ker J with an integer left inverse. Choosing a maximal minor of determinant plus/minus one gives such a basis: set the free coordinates to the identity and solve the pivot coordinates integrally. Every claimed kernel and left inverse is checked.

For I=J union {n}, the primitive quotient conormal in this basis is

    u_(I/J)=M_J^T n / gcd(M_J^T n).

Its gcd is one here; this is checked for every incidence, not assumed from dimensions. Define

    beta_I=alpha_I+sum_(J facet of I) h_J(u_(I/J)).                (5)

The full matrices include every independent I and J and all zero entries. No symmetry average, restricted support or favorable-row selection is used. Their dimensions are:

| Field | Rows | Functional coordinates | Nonzero integer matrix entries | Nonzero chosen coordinates |
| --- | --- | --- | --- | --- |
| q5, protecting c3 | 2670 | 5220 | 22214 | 70 |
| q6, protecting c2 | 3870 | 8010 | 34520 | 78 |
| q7, protecting c1 | 3780 | 7740 | 33540 | 63 |

A floating linear program proposes coordinates only. All coordinates are rationalized, and every row is then evaluated exactly over Q. The respective exact minima are 1/100000, 1371386493343/137138649334400000, and 350693738411087/35069373841118400000, all strictly greater than 1/1000000. The complete chosen fields are in certificate.json. Its compact ambient representation is described below and reconstructs the same corrected values without requiring a stored sparse matrix. The q6/q7 exact minima are slightly below the floating proposal margin 1/100000; only the verified weaker bound is asserted. Solver termination is not the certificate. A later checker must reconstruct the complete matrices and values from the original normals, including omitted zeros.

## 4. From finite local weights to every whole object

This uses the Berline-Vergne dual-solid valuation and the complete refined-normal-cycle argument, restated here for the original normal systems and coordinate lattices. The argument applies to bounded integral polytopes in a fixed lattice, and to rational polytopes with proved period-one stretching after denominator clearing. Here the original polytopes are integral.

For clarity, the full implication is as follows. Loosen ALL original inequalities by a generic positive small amount. The resulting polytope is bounded, full-dimensional and simple, and its fan gives a compatible pointed simplicial refinement of the original normal fan using only the original normal rays. Every surviving vertex basis limits to an original vertex, so no unrelated face is inserted. Only this fan is used; no Ehrhart polynomial of a perturbed object is transferred by continuity. This includes original hidden affine strata and non-simple walls.

Fix k>=1 and q=D-k. Give each q-cone of the refinement the saturated normalized volume of the actual k-face whose coarse normal cone contains its relative interior, or zero if there is no such face. These weights are nonnegative. At each (q-1)-support, their complete primitive quotient-conormal sum is zero: at an actual (k+1)-face this is lattice facet balance; inside a subdivided coarse q-cone the adjacent primitive directions cancel with equal weights; inside a larger coarse cone all weights are zero. These are the same original quotient lattices used in (5).

The BV dual-solid valuation adds the local constants over subdivision cells, with the actual ambient/subspace lattice compatibility. The local formula and balance give

    c_k=sum_I w_I alpha_I=sum_I w_I beta_I.                       (6)

The correction equality collects each h_J against its entire zero balanced sum. With the zero field, beta=alpha. If every beta is at least epsilon, each actual k-face contributes at least one cell, so (6) implies the full face-volume bound. When there is an actual k-face, its normalized volume is positive. For k=D the zero normal cone has weight one, giving ordinary volume. If actual degree is below k, both sides are zero. Constant one is established by nonempty integral Ehrhart counting, without a q=D computation.

Apply this with D=7 and epsilon=1/300 to the capped system, and D=6 and epsilon=1/720 to 3-by-4 transport. Apply it with D=8 and epsilon=1/1000000 to all k>=1 for 3-by-5: q<=4 uses raw weights, and q5/q6/q7 use the three complete corrections. This yields the whole coefficient range directly; the prior all-size transportation c1 theorem is compatible but is not needed for this finite proof. With at most one active row or column the polytope is a point. Thus all coefficients through the actual degree are positive, including every zero-margin boundary. Padding a smaller system with zero margins or capacities preserves the whole polynomial, so the stated smaller and transposed cases follow.

## 5. Entire LR scope and the new parameter domain

For positive p-by-N transportation margins of total M set R_i=sum_(k>=i)r_k and C_j=sum_(l>=j)c_l. The complete constructor is

    lambda=(M+R_2,...,M+R_p,C_1,...,C_N),
    mu=(M repeated p-1 times,C_2,...,C_N),
    nu=(R_1,...,R_p).                                           (7)

The disjoint-row character and Hall adjunction identify its entire LR coefficient with ALL transportation matrices at every nonnegative integer stretch; the insert/delete superstandard buffer map preserves the full tableau lattice. This is the accepted constructor in the companion three-row counting module. The full character argument is given immediately below. It is not an assertion that an arbitrary transportation face is a whole LR object. Final trimmed constructor rank is p+N-1 when margins are positive. Hence 3-by-4 gives rank six and actual degree six; 3-by-5 gives rank seven and actual degree eight.

For the capped identity (4), the complete two-row character of the overlapping top pair is the sum of Schur functions s_(Ut-ht-j,ht+j) for 0<=j<=min(u,v)*t-ht. After adjunction against nu, containment restricts exactly to 0<=j<=dt because u,v>=h+d. The three residual rows have lengths s*t-c*t-d*t+j, d*t-j, c*t and are column-disjoint: the second row begins after the third since h>=c, and the first begins after the second by U>=2h+2d. Weight extraction therefore counts nonnegative x_i,y_i,z_i with x_i+y_i+z_i=w_i*t, sum z=c*t and sum y=d*t-j. Summing all channels j=0,...,dt is bijective with (2). Every original integer shift and lattice point is retained. The inequalities w_i>=c+d were only needed to drop the capacities in the old binomial product. The present normal proof retains them and therefore removes that floor for m<=4. General one-overlap parameters outside 0<=c<=h and u,v>=h+d remain outside this theorem.

Two new whole controls illustrate the scope: capped w=(2,3,5,7), c=4,d=5 gives (lambda;mu;nu)=((31,26,17,15,12,7);(22,17,15,12,7);(22,9,4)), outer area 108 and degree seven. Transport r=(3,4,5), c=(1,2,2,3,4) gives ((21,17,12,11,9,7,4);(12,12,11,9,7,4);(12,9,5)), outer area 81 and degree eight. Their full polynomials can be recomputed by the companion exact three-row counting module, and selected independent count vectors are included in the result page. These are controls of universal family proofs, not their quantifier.

## 6. Complete local recurrence and compact fields

For q independent original normal rows N and each row subset T, set L_T=N_T Z^D, I_T=[Z^T:L_T], and H_T=N_T N_T^T. The induced normal-coordinate metric is H_T^(-1). The primitive positive coordinate axis at i has length r_(T,i)=I_T/I_(T without i). The finite numerator consists of all points p in L_T with 0<=p_i<r_(T,i); its cardinality is product_i r_(T,i)/I_T. These indices and complete numerator sets retain the original lattice. They are all trivial numerators here because every independently admitted row system has index one.

Choose a generic vector w compatible across subsets and put c_T=H_T^(-1) w_T. Define

    S_T(s)=sum_p exp(s*c_T.p)/product_i(1-exp(s*r_(T,i)*c_(T,i))).

With mu_empty=1, the complete local Euler-Maclaurin recurrence is

    mu_T(s)=S_T(s)-sum_(nonempty U subset T)
      (-1)^|U| * I_(T without U)/I_T
      * mu_(T without U)(s)/(s^|U| product_(i in U)c_(T,i)).

The local weight is the constant term of mu_full. Multiplication by s^|T| permits a common normalized Taylor truncation through q; every smaller-face series is retained through exactly the degree required by its integral factor. The denominator expansion is

    1/(1-exp(z))=-1/z+1/2-z/12+z^3/720-z^5/30240+O(z^7).

After multiplying by z the next term is degree eight, so the displayed terms suffice for all q<=7. Pole cancellation is checked but does not by itself certify the constant: omission of the degree-six Bernoulli term can leave poles canceled and change a local value. Two independently organized exact implementations reproduce all 16,848 admitted constants, including every raw negative.

The BV local formula and dual-solid valuation are from Nicole Berline and Michele Vergne, [Local Euler-Maclaurin formula for polytopes](https://arxiv.org/abs/math/0507256). The lattice-coordinate recurrence is its exact specialization; numerical agreement does not substitute for the analytic theorem.

In certificate.json, each field at a support J is stored as an ambient rational vector g_J with J*g_J=0. It equals M_J times the discovered coordinate vector, and therefore its action on a primitive quotient is g_J.n because all relevant image indices equal one. Unlisted supports have g_J=0. The verifier reconstructs every original support and checks annihilation, primitive image indices and every complete inequality

    beta_I=alpha_I+sum_(n in I) g_(I without n).n >= epsilon.

This is the same complete field as (5), expressed without a basis-dependent sparse-matrix file. It has 62, 72 and 61 nonzero ambient supports for q5, q6 and q7. Every omitted contribution is explicitly zero under this definition. No linear-program solver is required for verification.

## 7. Scope and attribution

Whole ordinary rank-six/seven positivity and unrestricted KTT remain open. Arbitrary four-by-five transportation and capped families with five or more capacities are outside this new whole-family theorem. The whole LR constructors, coefficient indices and original lattices in this note are mandatory; local weights and arbitrary proper faces do not imply an entire LR counterexample.

The classical BV formula, Alper Ferudun's rank-five theorem and correction approach, earlier complete normal-cycle arguments and the full LR character constructions are credited foundations. The new finite fields and exact normal analyses yield these specific all-margin whole families. The independent implementations and reviews supply computer-assisted evidence for mathematical scrutiny, not human expert acceptance or a worldwide priority determination.
