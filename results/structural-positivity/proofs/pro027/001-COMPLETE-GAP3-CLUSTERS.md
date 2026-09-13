# Complete gap-three branching with all overlap clusters

This all-stretch branching identity retains every overlap cluster. It does not establish positivity for the entire gap-three stratum. The counting models, implementations, and arithmetic checks have the distinct scopes described below.

## Entire object, conventions and source premises

Let alpha=(A1,A2,A3,a,b) be strictly decreasing and positive and beta=(B1,B2,B3,v1,v2,v3) weakly decreasing and positive. Assume equal total size and strictly positive proper dominance gaps. Write Delta_k=sum_(i<=k)(alpha_i-beta_i), with alpha padded by zero, and require Delta_3=3. The object is the complete Kostka polynomial K_(t alpha,t beta), t an integer >=0.

For kappa_i=sum_(j=i)^6 beta_j, the bare ordinary LR triple is lambda=kappa (outer), mu=(kappa_2,...,kappa_6), nu=alpha. The skew rows of lambda/mu are column-disjoint and have lengths beta_i. Thus s_(t lambda/t mu)=product_i h_(t beta_i), and taking the s_(t alpha) coefficient proves the all-stretch LR/Kostka identity. The ordinary rank is exactly six because kappa has six positive parts. This is a whole count identity, not a newly asserted affine map to conventional hive coordinates or a minimum-rank assertion.

The [Defect two and weighted straight-GT interiors](../../replay/proofs/WEIGHTED-GT-INTERIORS.md) gives actual dimension (5-1)*6-5*6/2+1=10. The fifteen variable GT entries below the fixed top have five coefficient-one row-sum equations; integral elimination of one variable per nonterminal row yields a saturated Z^10 lattice. Strict dominance and strict positive shape give the relative full-dimensionality premise. LR polynomiality and the whole count identity therefore give a degree-ten ordinary LR polynomial. These are prior geometric/source premises, not a degree guessed from values.

Its true codegree is the maximum of ceil(5/min beta), the four ceil(2/(alpha_i-alpha_(i+1))), ceil(2/b), and ceil(k(6-k)/Delta_k), k=1,...,4. This is the source's full interior staircase identity, not an assumed reflection. In the present strict gap-three domain q is one of 3,4,5,8: q=8 if Delta_2=1 or Delta_4=1; otherwise q=5 if min beta=1 or Delta_1=1; otherwise q=4 if Delta_2=2 or Delta_4=2; otherwise q=3. The classification is a direct application of the previously established formula. No numerical first-interior count is inferred.

The ingredients are the three-letter Kostka interval, Schur alphabet branching, skew Jacobi–Trudi, and the strict weighted-Gelfand–Tsetlin interior theorem. The gap-two branching theorem is used only within its stated domain.

## Complete first-block state set

For t>=0, let u=(u1,u2,u3)>=0, u1+u2+u3=3t, and eta=(tA1-u1,tA2-u2,tA3-u3). Put g1=A1-A2, g2=A2-A3, g3=A3-a and

m=min(g1*t-u1+u2, g2*t-u2+u3, (A1-B1)*t-u1, (B3-A3)*t+u3).

The state is admitted precisely when m>=0. Since A3>=3 and every ui<=3t, eta has nonnegative entries. The first two inequalities are its partition conditions, and the last two are exactly dominance over t(B1,B2,B3). The complete three-letter multiplicity is m+1. States with m<0 are absent, not assigned a negative count. Schur branching gives

P(t)=sum_(u>=0, |u|=3t, m>=0) (m+1) [z1^(t v1) z2^(t v2) z3^(t v3)] s_(t alpha/eta)(z1,z2,z3).

This includes every first-block partition and all its multiplicity. It is not an image face or a restricted-support count.

## Eight-term identity

In the following all h's use the three tail variables; h_0=1 and h_n=0 for n<0. Write S(C,D)=s_(C,D) in those variables. Set

x1=u1-g1*t-1, x2=u2-g2*t-1, x3=u3-g3*t-1,
y=u3-(A3-b)*t-2,
p12=g1*t+u2+1, p23=g2*t+u3+1, p13=(g1+g2)*t+u3+2.

For every admitted state, the entire skew Schur function D=s_(t alpha/eta) is

    h_u1 h_u2 h_u3 S(at,bt)
  - h_x1 h_p12 h_u3 S(at,bt)
  - h_u1 h_x2 h_p23 S(at,bt)
  - h_u1 h_u2 h_x3 S(A3*t+1,bt)
  + h_x1 h_x2 h_p13 S(at,bt)
  + h_x1 h_p12 h_x3 S(A3*t+1,bt)
  + h_u1 h_x2 h_x3 S(A2*t+2,bt)
  + h_u1 h_u2 h_y S(A3*t+1,at+1).

The first four terms are the diagonal and three single overlaps. The other four are the upper three-cycle, two disjoint overlaps, the middle three-cycle with its complete lower determinant, and the bottom second-subdiagonal term. The displayed signs are part of the identity, not claims about ordinary stretching coefficients of the separate terms.

To prove completeness, use the five-by-five matrix M_ij=h_(t alpha_i-eta_j-i+j), padding eta by zeros. Entry M31 vanishes: a nonnegative index requires u1>=(g1+g2)t+2; partition order then requires u2>=g2*t+2 and u3>=2. The total is at least (g1+2g2)t+6>3t. Entries M41 and M51 vanish as well. Entry M42 also vanishes: its index requires u2>=(g2+g3)t+2 and partition order requires u3>=g3*t+2, giving total at least (g2+2g3)t+4>3t. The still-lower M52 vanishes. M53=h_y is the only surviving entry beyond the first subdiagonal.

For clarity, expansion in the first two columns is

D=(h_u1*h_u2-h_x1*h_p12) T3 - h_u1*h_x2 T2 + h_x1*h_x2 T1,

where

T3=h_u3 S(at,bt)-h_x3 S(A3*t+1,bt)+h_y S(A3*t+1,at+1),
T2=h_p23 S(at,bt)-h_x3 S(A2*t+2,bt)+h_y S(A2*t+2,at+1),
T1=h_p13 S(at,bt)-h_x3 S(A1*t+3,bt)+h_y S(A1*t+3,at+1).

This expansion has twelve terms. The product h_x1*h_x2*h_x3 vanishes because it would require total deficit at least (g1+g2+g3)t+3>=3t+3. Each h_y*h_xi, i=1,2, vanishes because A3-b>=2 and gi>=1, again requiring at least 3t+3. These exact zero products delete four terms and leave precisely the eight displayed. There is no omitted determinant permutation or unexamined endpoint. At t=0 the formula gives 1.

## Complete cap intersections

Each term is h_r1 h_r2 h_r3 S(C,D). For nonnegative r, enumerate the entire three-by-three nonnegative integer matrix X with row sums r. Let gamma be its three column sums and w=t v-gamma. Reject any negative component of w; when |w|=C+D and C>=D>=0, use

K_((C,D),w)=sum_(J subset {1,2,3}) (-1)^|J| (D-w(J)-|J|+1)_+.

Here (x)_+=max(x,0). The formula follows from h_C h_D-h_(C+1)h_(D-1) and complete bounded-composition inclusion-exclusion. All eight subsets are retained. Wrong total size or a negative residual content means zero. Thus every cap, simultaneous violation and joint intersection is handled. No gap-two assertion that at most one unit cap can fail is imported.

The implementation also evaluates the equivalent two signed five-row, three-column matrix counts obtained by expanding S(C,D). Its exact integer kernel uses

(1-X)(1-Y) h_r(X,Y,1)=1-H_(r+1)(X,Y)+XY H_r(X,Y),

where H is the two-variable complete homogeneous polynomial. Diagonal sums evaluate the two H convolutions, and two-dimensional prefix inversion divides by (1-X)(1-Y). The third-column cap is imposed AFTER inversion. All totals use C++ `boost::multiprecision::cpp_int`. Negative row degrees give zero, and each output is associated with its stated input parameters.

## Counterexamples to truncation and finite checks

The state u=(t+1,t+1,t-2) for the unit anchor has a positive upper three-cycle contribution (t-2)(t+1)^3. The literal correction count gives 64 at t=3. The four-term truncation is therefore materially insufficient, not just slower.

A distinct simultaneous-cap witness is alpha=(10,9,8,2,1), beta=(8,8,8,4,1,1), t=2, u=(2,2,2), gamma=(0,3,3). The tail caps are(8,2,2): the last two caps both fail. Exactly seven matrices have these margins, all saved in DATA/structural-challenges.jsonl. Single-cap subtraction gives the invalid indicator1-1-1=-1, while complete inclusion-exclusion gives 0. The top multiplicity is 3. This is an invalid residual-content mechanism, not an observed negative ordinary LR coefficient.

The full 120-permutation Jacobi–Trudi expansion agrees as a FORMAL h-monomial dictionary with the eight-term law at 5534 admitted states across54 specified profiles and t=0,...,4. All eight blocks occur in this test set, with nonzero occurrences (5534,378,773,2120,27,30,120,120). The matrix kernel passes1264 independent small brute-force comparisons. Full parent counts use independently implemented unsigned horizontal-strip enumeration; their complete-vector comparisons and unused positive checks are detailed in [An unbounded rank-six LR family with exact complete compensation](004-UNBOUNDED-RANK6-POSITIVITY.md) and DATA/RECONCILIATION.json.

These bounded checks challenge the all-state algebraic proof but do not themselves establish its generality. In particular no exhaustive gap-three profile census or general gap-three sign conclusion is asserted. Repeated/zero shapes, nonsorted content conventions, dominance walls and Delta3>=4 require their own complete applicability argument.
