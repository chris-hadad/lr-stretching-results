# Exact complete coefficient extraction

The formulas here use ordinary rational coefficient arrays in the original integer stretching parameter. The implementation is independent of numerical fitting. Positivity outside the companion certificate's exact domains is not asserted by the calculation itself.

## A2 flow polynomial

Let a,b,c be nonnegative edge multiplicities on edges 01,02,12, and let the netflow be (A,B-A,-B). A positive multiplicity m on an edge with total k contributes binom(k+m-1,m-1) when k>=0. A missing edge contributes one exactly when its total is zero. These are counts in the full labeled integer-edge lattice.

When a,b,c are positive, the complete count is the finite sum over 0<=z<=min(A,B) of

    binom(A-z+a-1,a-1) binom(z+b-1,b-1) binom(B-z+c-1,c-1).

For A<=B, expand the last binomial by the finite Newton identity

    binom(X-z,C)=sum_(j=0)^C (-1)^j binom(X-j,C-j) binom(z,j).

Multiplication of the middle binomial by binom(z,j) gives binom(b+j-1,j) times binom(z+b-1,b+j-1). Vandermonde convolution with the first binomial then gives the complete left chamber formula

    sum_(j=0)^(c-1) (-1)^j binom(b+j-1,j)
      binom(B+c-1-j,c-1-j) binom(A+a+b-1,a+b+j-1).

The right chamber swaps (a,A) and (c,B). If an edge multiplicity is zero, the missing-edge equality directly gives the product-of-bundles cases in flow_polynomial; if only the middle edge remains, A=B is also required. Thus every missing edge and support face is retained.

Substitute A=A_s*t+A_0 and B=B_s*t+B_0. Their eventual signs and chamber order are determined lexicographically by slope and offset; an equal slope is not permission to discard its offset. Expanding the displayed binomials gives the exact polynomial that agrees with the whole affine flow at every sufficiently large positive grade. A negative eventual total gives zero. All coefficients use Fraction arithmetic. The prior expansion degree is the total edge multiplicity minus incidence rank; it can drop after support restrictions or cancellation.

## Schur and affine assignment extraction

In three variables, with rho=(2,1,0) and Delta=product_(i<j)(x_i-x_j), the complete Schur coefficient is

    [s_(t alpha)] H = [x^(t alpha+rho)] Delta H,
    h_m(x)=sum_i x_i^(m+2)/product_(j!=i)(x_i-x_j), m>=0.

Assign each factor h_(w_l*t+b_l) to one of the three nodes, indexed 0,1,2. Let n_i be the occupation, v_i its assigned slope sum, and q_i its assigned offset sum. After expanding every difference in one consistent root direction, the complete assignment has

    slope_i=v_i-alpha_i,
    offset_i=i*n_i-sum_(j>i)n_j+q_i,
    multiplicity_ij=n_i+n_j-1,
    sign=(-1)^(n_1+2*n_2).

Balance makes both netflow sums zero. A multiplicity of minus one is a numerator 1-x_j/x_i, so every subset of these numerator edges is expanded with its sign and exact offset change. Only afterwards may that multiplicity be replaced by zero in the flow denominator. The complete finite assignment sum uses the A2 polynomial above. Fixed positive factors and positive slopes with negative offsets remain. A zero slope with negative offset gives an identically zero product; h_0 factors may be removed.

Because there are finitely many assignments, their eventual identities hold beyond one common grade. No individual affine summand is assumed to equal its polynomial at an unsupported early grade. In particular its constant is not obtained by collapsing the character at t=0.

## Whole LR families

The one-overlap character is exactly

    (h_(u*t)h_(v*t)-h_((u+v-h)*t+1)h_(h*t-1)) product_l h_(w_l*t).

Both terms and their original offsets are retained. For arbitrary outer/inner partitions the complete Jacobi-Trudi determinant uses every permutation pi and the original degree

    t*(outer_i-inner_pi(i))+pi(i)-i.

A negative slope is eventually zero, and a zero slope with negative offset is identically zero. These terms remain explicit signed records. Specialization to three variables preserves the coefficients of all Schur functions with at most three rows. The ordinary stretched LR polynomiality theorem upgrades equality at all sufficiently large grades to equality of the entire stretching polynomial. An infeasible positive-stretch family has the zero polynomial; nonempty families have constant one. No conjugation or discarded affine shift is used.

The capped interface takes u=v=c+d, h=c and alpha=(sum w+d,c+d,c), so it is a complete instance of this one-overlap family. The companion certificate proof gives the entire bijection with y,z satisfying sum z=c*t, sum y<=d*t and y_i+z_i<=w_i*t. This identity holds for any supported number of capacities; its sign theorem has the separate m<=4 scope.

## Entire transportation count

For three row margins r and column margins w, the entire transportation count is

    [x^(t*r)] product_l h_(t*w_l)(x_0,x_1,x_2).

This has the same complete Lagrange assignment formula with q_i=0 and with multiplicity n_i+n_j instead of n_i+n_j-1, because there is no Vandermonde numerator. Hence it needs no missing-edge numerator expansion. Every original offset i*n_i-sum_(j>i)n_j remains. The whole polytope is integral in its original matrix lattice, so equality at sufficiently large grades identifies its entire Ehrhart polynomial. Zero columns are deleted before assignment pricing, and zero rows are retained or padded to three; they impose their exact component conditions. The all-zero object is a point.

This is a full-polynomial formula for any declared supported assignment count, not only the positive 3-by-5 theorem. Runtime is exponential in the number of active columns, and it is not a variable-size polynomial-time LR algorithm.

## Verification, limits and credit

The tests compare full vectors against independent unsigned LR row-pattern counts and direct integer matrix/capped counts at a complete prior degree space and two further positive grades. They also exercise both affine chambers, exact and offset-separated ties, fixed factors, zero objects, malformed inputs and refusals before arithmetic. The deliberate dropped-offset control gives the wrong vector (0,3/2,3/2) where the complete whole LR vector is (1,5/2,3/2).

The Schur, Jacobi-Trudi, Pieri, Lagrange and Vandermonde identities are classical. LR stretching polynomiality is due to Derksen-Weyman and Rassart; [Rassart's paper](https://arxiv.org/abs/math/0308101) gives the chamber-polynomial framework. Earlier three-row and affine-offset derivations are credited in the source constants. The new implementation expands the entire polynomial and retains all original offsets; it does not claim those classical identities as new discoveries. Independent programs and AI review do not constitute external human acceptance.
