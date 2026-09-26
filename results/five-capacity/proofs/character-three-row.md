# Complete three-row character and chamber identity

## Object and exact scalar identity

Let w_1,...,w_n be nonnegative integer weights with sum W, and let
alpha = (alpha_1,alpha_2,alpha_3) be a partition of W. The entire family is
K_(t alpha,t w). It is an entire ordinary LR family under the suffix lift
lambda_i = sum_(j>=i) w_j, mu_i = lambda_(i+1), nu = alpha. Zero weights
can be deleted. No affine hive equivalence or general short-inner-three skew
factorization is asserted.

Set rho = (2,1,0), Delta(x) = product_(i<j)(x_i-x_j). The complete character
and highest-weight identities are

    K_(t alpha,t w) = [x^(t alpha+rho)] Delta(x) product_l h_(t w_l)(x),
    h_m(x_1,x_2,x_3) = sum_i x_i^(m+2) / product_(j!=i)(x_i-x_j).       (1)

The second identity is polynomial partial fractions, valid also for m = 0.
The first follows by Schur expansion: alpha+rho is strictly decreasing, so
only the identity monomial of its own Weyl alternant reaches that exponent.

For an assignment sigma of all n labels to the three nodes, let n_i be the
occupation and v_i the sum of weights assigned there. Define

    m_ij = n_i+n_j-1,
    delta_i = (i-1)n_i - sum_(j>i)n_j,
    b_sigma(t) = t(v-alpha)+delta,
    epsilon_sigma = (-1)^(n_2+2n_3).                                  (2)

Multiplying by Delta removes exactly one factor for every pair. Converting
x_i-x_j to x_i(1-x_j/x_i), the exponent at node i is

    t v_i + 2n_i - sum_(j>i)(n_i+n_j-1) - (t alpha_i+rho_i)
      = t(v_i-alpha_i)+delta_i.

This derives every offset and the sign in (2). Expand in the ordered formal
region x_1 >> x_2 >> x_3, so every positive root points along an acyclic graph.
If m_ij = -1, retain the numerator (1-x_j/x_i). For every subset U of these
negative-multiplicity edges put alpha_U = sum_(ij in U)(e_i-e_j), and set
m+_ij = max(m_ij,0). Then the exact scalar formula at every t >= 0 is

    sum_sigma epsilon_sigma sum_U (-1)^|U|
       F_(m+)(b_sigma(t)-alpha_U).                                   (3)

Here F is the complete integer vector-partition count. A zero multiplicity
demands zero flow on that edge. It is not replaced by a denominator of
multiplicity one. Formula (3) includes the empty assignment and all numerator
subsets. The elementary implementation verifies those cases separately.

At t = 0 the literal collapsed tableau count is one even if the positive-stretch
family is empty. For an empty family the campaign's stretching polynomial is
instead defined to be zero. This distinction is retained in the coefficient
formula and in the tests; the scalar t = 0 convention is not used to interpolate
an empty family's constant.

## Complete A2 count and chamber polynomials

Write (a,b,c) for nonnegative multiplicities on edges (12,13,23), and put
A = netflow_1, B = -netflow_3. For positive multiplicity m, let
B_m(z) = binom(z+m-1,m-1) at nonnegative integer z; B_0(z) is 1 at z = 0
and zero otherwise. Directly, z = flow_13 determines every group total:

    F(A,B) = sum_(z=0)^min(A,B) B_a(A-z) B_b(z) B_c(B-z).             (4)

It vanishes when A < 0 or B < 0. This counts every labeled-edge allocation in
the original integer lattice. A spanning tree identifies the saturated
sum-zero incidence lattice with Z^2; no index or dilation change is inserted.

When a,b,c > 0, the full support has precisely the two regions A <= B and
B <= A. On the first, its whole polynomial is

    F_L(A,B) = sum_(j=0)^(c-1) (-1)^j binom(b+j-1,j)
               binom(B+c-1-j,c-1-j)
               binom(A+a+b-1,a+b+j-1).                              (5)

To derive it, expand

    binom(B-z+c-1,c-1)
      = sum_j (-1)^j binom(z,j) binom(B+c-1-j,c-1-j),

multiply B_b(z) binom(z,j) = binom(b+j-1,j)
binom(z+b-1,b+j-1), and apply the finite Vandermonde convolution with
B_a(A-z). Thus (5) is an all-parameter polynomial identity on its full closed
counting chamber, with degree at most a+b+c-2. The other polynomial is
F_R(A,B;a,b,c) = F_L(B,A;c,b,a). They agree on the entire shared wall.

All missing-edge cases have complete elementary descriptions:

- b = 0: B_a(A) B_c(B) on its full supported axes or quadrant.
- a = 0 and b,c > 0: B_b(A) B_c(B-A), supported on 0 <= A <= B.
- c = 0 and a,b > 0: B_a(A-B) B_b(B), supported on 0 <= B <= A.
- Only b > 0: B_b(A) on A = B >= 0. A lone a or c uses its corresponding
  axis. With no edges, only zero netflow is counted.

The B_0 convention implements each rank drop explicitly. A polynomial formula
from a supported chamber is never substituted for a true out-of-support count.

## Exact first coefficient, including every wall

For each term of (3), write its affine A and B as t A_1+A_0 and t B_1+B_0.
Choose its eventual supported region by the lexicographic pairs
(A_1,A_0), (B_1,B_0), and (A_1-B_1,A_0-B_0). For a missing-edge axis or
diagonal, both the slope equality and offset equality must hold. These rules
exhaust all affine directions, including slopes on a support or internal wall.
They select the true count for every sufficiently large positive integer t.

Evaluate (5), its reflected polynomial or the appropriate product at the
original offset. Its ordinary linear coefficient is

    A_1 partial_A F(A_0,B_0) + B_1 partial_B F(A_0,B_0).                (6)

Sum (6) with every original assignment and numerator sign from (3). This is
the complete c1 of the whole Kostka/LR stretching polynomial. Polynomiality
of stretching is an established source premise: Rassart, *A polynomiality
property for Littlewood-Richardson coefficients*, `arXiv:math/0308101v2`,
Theorem 4.1 and Corollary 4.2, with the usual outer-partition convention
translated to ours. Eventual equality of two polynomials implies equality of
their coefficients. It does not assert that an individual shifted summand is
its supported polynomial at an inadmissible early grade.

For n >= 3 a prior whole degree bound is 2n-5. With at least two occupied
nodes, the nonnegative multiplicities sum to 2n-3 and the connected incidence
rank is two, yielding that bound directly from (4)-(5) and the missing-edge
products. In the one-occupied case only the first node can contribute at large
positive grades for a nonzero dominant alpha. Its entire contribution is

    binom(alpha_2 t+n-2,n-2) binom(alpha_3 t+n-2,n-2)
      - binom(alpha_2 t+n-1,n-2) binom(alpha_3 t+n-3,n-2).             (7)

The top degree 2n-4 cancels. When alpha_3 = 0, the second factor of the
subtracted term is zero and the remaining degree n-2 is at most 2n-5.
Empty or one-/two-label families are handled directly as the zero polynomial
or the constant one. These arguments precede the independent reconstruction
of the complete numerical controls.
