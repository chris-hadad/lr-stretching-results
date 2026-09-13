# A complete stable source--sink hive map

This geometric refinement of the stable source–sink count identity gives a direct affine lattice map. The stable family, its complete counts, dimension, and codegree are previously established results. Numerical checks and face certificates concern n=7; the elementary map proof is dimension-independent.

Let n>=3, rho=(n-1,...,0), theta=(1,0,...,0,-1), and integers M>=s>=0. With lambda outer set lambda=2M rho-s theta and mu=nu=M rho. For s>0 the displayed ordinary rank is n and outer area is M n(n-1). At s=0 the highest component is a point, including the zero origin. The displayed size/rank is not a minimality assertion.

Let f_ij>=0, i<j, be ALL edges of the complete acyclic n-vertex graph, with div(f)=s(e1-en). Every coordinate and every vertex's total inflow/outflow is at most s: acyclic path decomposition writes f as nonnegative source--sink paths of total mass s. No support edge is deleted.

Define the complete LR row-count triangle X by

    X_(r,j)=f_(j,r) for j<r,
    X_(i,i)=nu_i - sum_(r>i) f_(i,r),
    X_(r,j)=0 for j>r.

Content sums are nu. Conservation gives row sums lambda_i-mu_i, including the changed first/last rows. Diagonal entries are nonnegative: for i<n, nu_i>=M>=s, and at i=n both the diagonal and outflow are zero. Every off-diagonal is nonnegative by definition.

Here are ALL remaining inequalities of the full LR triangle, not a restricted support test. The column inequality at successive rows r-1,r and label j<r is

    mu_(r-1) + sum_(ell<j) X_(r-1,ell)
              -mu_r -sum_(ell<=j) X_(r,ell) >=0.

The lower sum contains only off-diagonal entries and is at most s; the upper sum is nonnegative, and mu_(r-1)-mu_r=M. Thus its slack is at least M-s. At j=r it is exactly lambda_(r-1)-lambda_r>=0. Higher labels give the same redundant row-end inequality. The ballot inequality is

    sum_(r<i) X_(r,j) - sum_(r<=i) X_(r,j+1)>=0.

If i<=j both sums vanish. If i>j, both relevant diagonals are included, and subtracting from the full content sums expresses the slack as

    nu_j-nu_(j+1) - sum_(r>=i) f_(j,r)
                            + sum_(r>i) f_(j+1,r).

The negative flow total is at most s and the positive total is nonnegative. The slack is therefore at least M-s. This covers all ballot indices, including the initial and final labels. Equality M=s is included. These inequalities, positivity, row sums and content sums are the complete LR row-count model inherited from the original hive convention.

The equality with the ORIGINAL rhombi can be checked without an unproved geometric LR equivalence. Put r=i+j. The first elementary rhombus is the column slack between rows r+1 and r+2 at label j+1. The second rhombus (j>=1) is the ballot slack sum_(a<=r) X_(a,j)-sum_(a<=r+1) X_(a,j+1). The third rhombus (i>=1) is exactly X_(i+j+1,j+1), an off-diagonal flow. Substituting the double-prefix formula gives these three identities term by term, with all boundary values retained. These identities exhaust all 3n(n-1)/2 rhombi. Thus the forward map lands in the whole hive; conversely, the third rhombi of any hive give nonnegative off-diagonal flows, and the fixed boundaries telescope to the required divergence.

Conversely, every point of the complete LR triangle has off-diagonal entries f>=0. Subtracting its content equation from its row equation gives exactly div(f)=s theta. The diagonal is recovered by the displayed formula. Thus the correspondence is a real affine bijection and an integer bijection in every grade. It does not follow merely from the stable Weyl identity, and it is not a map from a proper coordinate face.

The whole hive map is the standard integer double-prefix map

    h(i,j)=sum_(a<=i+j) mu_a
                   +sum_(r<=i+j)sum_(ell<=j) X_(r,ell).

For H(r,j)=h(r-j,j), its integer inverse on off-diagonal entries is

    X_(r,j)=H(r,j)-H(r-1,j)-H(r,j-1)+H(r-1,j-1), j<r.

The boundary terms are included when an index reaches the boundary. Consequently no finite-index sublattice or metric is silently substituted. The normal-cycle certificate itself stays in the original hive metric; flow coordinates are used to compute the actual face volumes through the full integral map.

Free coordinates on the entire flow lattice are the nonadjacent edges, with inverse

    f_(i,i+1)=s-sum_(a<=i<b,b>a+1) f_(a,b).

There are D=(n-1)(n-2)/2 coordinates, the lattice is saturated, and the unit vertices are all 2^(n-2) source--sink paths. Their positive average is relatively strict, so s>0 has actual degree D. Interior integer points have every edge at least one. The cut k costs k(n-k); hence the unit codegree is floor(n^2/4). It is attained by putting one on each nonadjacent edge and choosing the adjacent residuals floor(n^2/4)-k(n-k)>=0 after the all-one translation. At integral s>0 the true codegree is ceil(floor(n^2/4)/s).

All these statements apply after replacing (M,s) by (Mt, st), including t=0. The direct whole-lattice equivalence transfers actual faces, normalized volumes and interior-translation geometry to the conventional hive. This strengthens only the geometric bridge of the previously known stable family; it is not a new all-coefficient positivity theorem for every n.

The n=7 certificate constructs the full 15-by-15 integer map and inverse, verifies determinant +/-1, retains all 63 original rhombi and all 21 flow inequalities, checks every 32 path vertices at M=s=1 and the extra M-direction, and checks an actually strict hive point. The detailed source/count and face verification is reported separately with its computational scope.
