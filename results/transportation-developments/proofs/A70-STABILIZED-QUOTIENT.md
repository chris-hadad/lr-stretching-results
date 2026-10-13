# A70: independently reconstructed positive three-letter stabilization

Curated mathematical proof from **A70**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Selected completed Pro049 U09 adoption. The root independently rederives the complete original fibers, tail-chain map, positive simplex description and whole-vector bound below. The one classical positivity premise is checked directly against Postnikov's primary paper. U11's correct trimming interpretation is retained. Returned programs remain inert. This adopts the coarse theorem stated here; it does not silently adopt U10's sharp support algorithm, quotient lift, primitive cover, or any starting-original sign.

## The complete theorem and its limit

Let b=(lambda;mu,nu) be a legal integral partition triple, lambda outer, with one inner factor of length at most three. Put that factor in the content position by inner commutativity and pad every physical row to n>=4, retaining zeros. Use


```text
sigma=((4,3,2,0,...);(2,1,0,...);(3,2,1)).
```

This is a complete LR segment with P_sigma(t)=1+t. The construction below gives a complete integral tail polytope T_b, actual dimension d and ordinary count E_b(t). If T_b is empty, every b+u sigma is empty for every u>=0, with the campaign's zero-polynomial convention. Otherwise EVERY coefficient of E_b is positive through d, with e_k>=1/d!. Write W=|nu|, K=3W+1, D=d+1 and Q_b=P_(b+K sigma). Then for integers s>=1 and u>=sK,


```text
P_(s b+u sigma)(t)=Q_b(st)+(u-sK)t E_b(st).       (1)
```

Its actual degree is D. The entire increment for increasing u is strictly positive in all positive degrees. An explicit count-free integer U_safe given below makes every coefficient of the whole original strictly positive for u>=s U_safe. In particular every nonempty starting original with a short inner factor admits such an augmentation. Augmentation changes the polynomial. Neither (1) nor the positive quotient signs b, Q_b or an arbitrary pre-stable member. Unrestricted KTT remains open.

## Every physical original inequality

Set w_i=lambda_i-mu_i, d_i=mu_(i-1)-mu_i and alpha=nu_1-w_1. Tail rows i>=4 are (a_i,b_i,c_i), and their sums are A,B,C. For an integer augmentation U, all row/content equations force the array


```text
row 1: (w_1+2U,0,0),
row 2: (z+U,w_2-z+U,0),
row 3: (alpha-A-z,nu_2-w_2-B+z+U,nu_3-C+U),
row i>=4: (a_i,b_i,c_i).
```

The first row and the second-row zero follow from the ballot rule. Its inverse takes the literal tail entries and z=row2_ones-U, so no lattice index is introduced. All original row widths and content sums are preserved.

Define T_b by the ENTIRE tail conditions


```text
a_i,b_i,c_i>=0,  a_i+b_i+c_i=w_i,
a_i<=d_i                                      (i>=4),
c_i<=lambda_i-lambda_(i+1)                     (4<=i<n),
a_i+b_i<=d_i+a_(i-1)                          (i>=5).
```

There is no extra last-row c_n cap. The remaining functions are


```text
L=max(0,w_2+B-nu_2,alpha-A-d_3,
      alpha+nu_2-w_2-A-B-d_3,w_2-w_1,nu_2-B-w_1),

H=min(d_2,alpha-A,w_2-nu_3+C,
      d_4+alpha-A-a_4-b_4),

R=max(0,w_2-w_1-d_2,w_3-w_2-d_3,C-nu_3,
      w_4-d_4-w_3+nu_3-C,
      nu_2-nu_1+sum_(j>=i)a_j-sum_(j>i)b_j,
      nu_3-nu_2+sum_(j>=i)b_j-sum_(j>i)c_j : i>=4).
```

The complete original is exactly


```text
y in T_b, R(y)<=U, L(y)-U<=z<=H(y).             (2)
```

Here is the independent physical derivation. For each adjacent row, strict columns are equivalent to


```text
d_i(U)+sum_(k<j)x_(i-1,k)-sum_(k<=j)x_(i,k)>=0.
```

For each reading-prefix letter comparison, ballot is equivalent to


```text
sum_(k<i)x_(k,j)-sum_(k<=i)x_(k,j+1)>=0.
```

The worst prefix is the end of the larger-letter block; adjacent comparisons cover each whole skew column. Substitution of the full array gives the following exhaustive groups. Row-two nonnegativity gives z>=-U and z<=w_2+U; row-three nonnegativity gives H's alpha-A, L's w_2+B-nu_2 and R's C-nu_3. The row-two column tests give H's d_2 and R's w_2-w_1-d_2. Row-three columns give the two L terms involving d_3 and R's w_3-w_2-d_3. Row-four columns give its a_4 cap, H's fourth term and R's exceptional w_4 term. Later columns give exactly the three displayed kinds of tail inequality, with the c cap stopping at n-1. The first row-two/row-three ballot tests give L's final two terms; the other row-three test gives H's w_2-nu_3+C. Every later ballot test is one of R's two suffix expressions. Earlier forced-zero tests vanish.

The apparent extra upper bound z<=w_2+U follows from the retained inequalities: H<=w_2-nu_3+C and U>=C-nu_3. Their two slacks sum to w_2+U-z. Row-one nonnegativity is legal w_1>=0 and U>=0. Thus no condition has been dropped on faith. These formulas hold over both real and integer coordinates, including ties and empty physical rows. Every integral tail contributes exactly


```text
1_(R<=U) max(0,U+H-L+1).
```

The +1 and every tail-only admission test survive in all pre-stable bands. Separate shadow/arrival pieces are not asserted to be polynomials.

## Whole quotient, actual lattice and strict stable degree

Legality and total width W give 0<=L<=W, -2W<=H<=W and R<=2W. For H's fourth term, w_1+A+a_4+b_4<=2W suffices; all d_i are nonnegative. The other bounds follow term by term from the complete nonnegative row/content totals. Therefore U>=K=3W+1 makes every tail admissible and every real fiber have length U+H-L>=1. K is a conservative bound, not the sharp support maximum and not itself a homogeneous function of b. The interval forms and T_b do scale homogeneously; the sufficient condition u>=sK is preserved under the stated s scaling.

For i=n,...,4 put


```text
x_i=mu_i+a_i,  y_i=lambda_i-c_i=mu_i+a_i+b_i.
```

This is an integral affine map with an integral inverse. The entire quotient is the ordered chain


```text
x_n<=y_n<=x_(n-1)<=y_(n-1)<=...<=x_4<=y_4,
mu_i<=x_i<=min(lambda_i,mu_(i-1)),
max(mu_i,lambda_(i+1))<=y_i<=lambda_i  (i<n),
mu_n<=y_n<=lambda_n.
```

Let v be this chain, of length ell=2(n-3). For its individual bounds l_i,u_i, replace them with L_i=max_(j<=i)l_j and U_i=min_(j>=i)u_j. These nondecreasing lists give the identical domain. A coordinatewise violation L_i>U_i means empty; otherwise v=L is an integer point. At any vertex, every tied-coordinate block is pinned to an integer individual bound, since an unpinned block can move both ways. Thus the chain is integral, with forced equalities retained.

Append the fixed endpoint N=U_ell and form gaps


```text
z_1=v_1, z_i=v_i-v_(i-1), z_(ell+1)=N-v_ell.
```

This is an integral affine inverse pair. For k=1,...,N, let a(k) be the first index with U_i>=k and b(k) the first with L_i>=k, using the appended fixed bound at ell+1. The full gap polytope equals


```text
sum_(k=1)^N Delta_[a(k),b(k)] = sum_I c_I Delta_I.   (3)
```

Indeed every allowed token placement obeys all prefix bounds. Conversely, for an integer gap point, sort its N token positions j_k. If j_k<a(k), a prefix exceeds U; if j_k>b(k), the prefix at b(k) falls below L. Hence each token lies in its prescribed interval. Integrality of the chain promotes equality of all lattice points to equality of the complete convex polytopes. This counts points, not multiple token assignments. Grouping intervals uses only bound breakpoints; it does not require iterating to a huge N.

The graph joining coordinates within every positive nonsingleton interval has components V. The tangent span has dimension d=sum_V(|V|-1); within each component its edge differences generate the full integer zero-sum lattice. Component sums are fixed integers and there are no other affine equations. Singleton summands are integer translations. Thus the actual tail lattice is saturated. A stable fiber is everywhere nondegenerate, so the original has dimension and degree d+1, with affine lattice equal to the actual tail lattice times the primitive z lattice. It is not asserted to be a Cartesian product of polytopes. The complete LR polynomiality premise applies to this full original only.

## Precisely applied classical positivity

Primary source checked directly: Alexander Postnikov, [Permutohedra, associahedra, and beyond](https://arxiv.org/html/math/0507163v1), Definition 9.2, Lemma 11.1, Definition 11.2 and Theorem 11.3 (PDF page 28), with the completed proof in Section 14 (pages 39–40). It counts lattice points of a trimmed positive sum of coordinate simplices using rising factorials over draconian vectors. For (3), add ONE full-coordinate simplex and trim that same simplex; Lemma 11.1 restores (3). The full-support factor is therefore (1)_a/a!=1. This covers disconnected actual supports and lower-dimensional cases without pretending a zero-weight summand creates dimension. The later alternative semiproof is not used. No arbitrary signed-simplex or generalized-permutohedron positivity claim follows.

Explicitly, after removing singleton translations, (3) has positive integer groups c_j Delta_(I_j), j=1,...,p, and


```text
E_b(t)=sum_a product_j binom(c_j t+a_j-1,a_j),     (4)
sum_(j in S)a_j<=|union_(j in S)I_j|-1
              for every nonempty S subset[p].
```

The dummy component is ell-sum a_j; constraints containing it are automatic. This is the complete formula with all feasible vectors, not a selected Hall panel. The p=0 case is E_b=1. Every factor has nonnegative ordinary coefficients. Because the nonempty integral tail has actual degree d, at least one feasible vector has total d and none can have total larger than d (positive leading terms cannot cancel). Every componentwise subvector remains feasible. For each k<=d, a subvector of total k contributes a positive t^k coefficient, proving strictness in EVERY degree, including e_0=1. Each denominator product divides d!, so d!e_k is a positive integer and e_k>=1/d!.

## Entire stable increment and explicit finite augmentation

At stable U, summing every full interval in (2) gives an identity with a complete signed intercept. Taking the difference at two stable augmentations eliminates that intercept. Scaling b by s and applying original LR polynomiality proves (1) identically, including t=0. Define


```text
A_b=(D(K+W)+1) product_(i>=4) binom(D w_i+2,2),
C_b=(2^(D+1)-1) A_b,
U_safe=K+d! C_b+1.
```

For each determining node i=0,...,D, the complete Q_b count is between one and A_b: each tail row has at most binom(iw_j+2,2) choices and its interval at most i(K+W)+1 points. The coefficient l1 norm of the ith Lagrange basis is bounded by

    (D+1)!/((i+1)i!(D-i)!).

The sum of these bounds is exactly 2^(D+1)-1. Thus every ordinary coefficient q_k of Q_b has absolute value at most C_b, without actually counting any large augmentation. For u>=sU_safe and k>=1, the kth coefficient of (1), divided by s^k, is


```text
q_k+(u/s-K)e_(k-1) >= -C_b+C_b+1/d! >0.
```

The constant is one. This proves complete eventual strict positivity and every positive-degree stable increment. The bound is intentionally conservative; it is not a sensible enumeration budget. Point tails have d=0 and stable degree one. Empty tails keep the zero-polynomial convention at positive grades and are not assigned a spurious point by literal zero scaling.

## Independent checks and exact adoption boundary

The campaign verifier independently reconstructs all physical affine forms on its declared finite n range, checks the conditional redundant bound, compares complete chain counts with the full simplex/draconian polynomial on every selected actual-degree determining and unused grade, and preserves point/empty/tied/disconnected controls. It also checks the complete Lagrange norm identity and wrong-dummy/offset/boundary controls. These symbolic and auxiliary-chain checks select no additional numerical LR original; A70's six-original ceiling is unchanged. The generic physical derivation, complete chain/token proof and correctly applied classical theorem supply the unbounded statement, not those finite checks.

The accepted scope is: the full fiber identity, complete integral quotient, strict E, coarse K, actual stable degree, (1), and U_safe. U10's sharp support algorithm, rho realization, primitive cover and collapse classification remain unadopted source pending their own independent treatment. The coefficient signs of b, the noncollapsed stable boundary and every arbitrary pre-stable band remain open. U12 independently supplies one complete operation across its own four chambers; it is not substituted for these general obligations. No candidate, coverage increment, public priority or formal/human endorsement is implied.
