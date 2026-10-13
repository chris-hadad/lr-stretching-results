# Complete first-order transportation compensation at arbitrary size and rank

Curated mathematical proof from **Pro029/A006**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Provider theorem of Unit7, based on the all-rank chamber proof003 and the credited complete two-class identity. This is not a theorem about all LR triples or all ordinary coefficients.

## 1. Entire count and the remaining bridge

Let p,N>=2 and let r in positive integral p-tuples, c in positive integral N-tuples have common total M. The entire transportation polytope has strictly positive point x_ij=r_i c_j/M, free saturated integer coordinates in its upper-left(p-1)-by-(N-1) block, and dimension d=(p-1)(N-1). Forest supports prove integral vertices. Its count P(t) is therefore an ordinary Ehrhart polynomial of actual degree d, with P0=1, before any coefficient fit.

The complete identity

 P(t)=[x^(tr)]product_(j=1)^N h_(tc_j)(x_1,...,x_p)

and the full p-term Lagrange expansion give EVERY labeled assignment f:[N]->[p]. Its occupations n_i and assigned column totals C_i have sign(-1)^sum(i-1)n_i and exact graph multiplicities n_i+n_j and netflow

 b_i(t)=t(C_i-r_i)+(i-1)n_i-sum_(j>i)n_j.

Each term, on its eventual affine ray, is one complete unimodular chamber polynomial, including tied rays; an eventual ray outside support is zero. The finite sum of those eventual polynomials equals the entire P, because the original scalar identity holds for all positive integer t. There is no assertion that an individual assignment polynomial agrees with its initial out-of-support scalar counts.

For every assignment occupying at least three classes, proof003 gives zero full gradient at the original offset. Thus its ordinary linear coefficient is zero. This includes every possible empty position, every fully occupied class and every supported chamber; no scalar assignment term is discarded. Consequently

 E_(>=3)(r,c)=0.                                         (1)

The source's EXACT complete one-/two-class sum, Frontier024 proof017 and proof018, is D_(p,N), where

 w_k(I)=(|I|-1)!(k-|I|-1)!/[2(k-1)!],
 D_(p,N)=sum_(I,J proper nonempty) w_p(I)w_N(J)
            min(r(I),M-r(I),c(J),M-c(J)).

Combining its complete identity with(1) proves

 c1(P)=D_(p,N)>0.                                       (2)

The minimum is the length of a full2-by-2 transportation interval. All cuts, equality walls and class assignments are retained. A higher-class scalar or a higher ordinary coefficient can remain negative; only the full ordinary-linear contribution is zero.

## 2. Quantitative properties and sharp minimum

The credited weight sum is sum_(I proper nonempty)w_k(I)=H_(k-1). With epsilon the smallest individual positive margin, every cut minimum is at least epsilon. Hence

 c1(P)>=H_(p-1) H_(N-1) epsilon>0.                       (3)

The defined real extension D on the balanced nonnegative margin cone is symmetric separately in rows and columns, symmetric under transposition, homogeneous, concave and superadditive. On integral positive margins it now equals the whole ordinary linear coefficient; for arbitrary real margins D is the extension, not a claim of an Ehrhart polynomial on an irrational polytope. No corresponding concavity assertion is made for arbitrary LR polynomials.

Assume2<=p<=N, transposing otherwise. The previously proved SHARP minimum of D is now the unrestricted minimum of the entire c1:

 c1(P)>=L_(p,N)=D((N-p+1,1^(p-1)),1^N).                 (4)

Equality is attained at those literal positive margins; no uniqueness claim. For q_l=min(l,N-l), define

 T_l(N)=q_l[H_(N-q_l)-H_(q_l-1)]
             +N[H_(N-1)-H_(N-q_l)].

Then the credited finite harmonic evaluation is

 L_(p,N)=sum_(l=1)^(p-1) T_l(N)/l.                     (5)

For clarity its whole-domain proof is retained: choose integral1<=s_i<=r_i with sum s_i=N, subtract(s,1^N), use nonnegative superadditivity of D, and then row concavity/symmetry on the simplex with vertices the permutations of(N-p+1,1,...,1). AtN=p the simplex is a point; no division by N-p. Pair row subsets avoiding the large row with their complements and group column subsets by size; splitting the complete minimum sum at q_l,N-q_l yields(5). The minimization and harmonic algebra are credited to Frontier024 proof029; the new step is complete all-row equality c1=D.

For the n-by-n Birkhoff polytope the credited cut evaluation now identifies the ENTIRE coefficient for every n>=2:

 c1(B_n)=sum_(k=1)^floor(n/2) [H_(n-k)-H_(k-1)]^2.       (6)

The source had checked n<=9 against the published table without a general remainder proof. Here(1) supplies the all-n bridge, not an extrapolation of that table.

## 3. The literal entire ordinary LR constructor

Set R_i=sum_(k>=i)r_k and C_j=sum_(l>=j)c_l. Define

 lambda=(M+R_2,...,M+R_p,C_1,...,C_N),
 mu=(M repeated p-1 times,C_2,...,C_N),
 nu=(R_1,...,R_p).

These are balanced weakly decreasing nonnegative partitions, lambda outer. The skew character is the translated straight block(R_2,...,R_p) times disjoint rows c_j. Hall adjunction gives the inner product of product_i h_(tr_i) and product_j h_(tc_j), and Cauchy counts ALL tables. Every offset scales with t. Thus the identity is the entire LR stretching polynomial, not a proper face or selected subcount.

The final trimmed ordinary rank is p+N-1 and the outer area is

 (p-1)M+sum_(i=2)^p R_i+sum_j C_j.

The actual degree d is proved in the complete table lattice. General hive/table affine isomorphism is not assumed; exact all-stretch integer equality fixes the ordinary polynomial in the ORIGINAL stretching parameter. This yields a whole-LR c1 theorem at arbitrary constructor rank and size, not every LR object at any such rank.

## 4. Every zero-margin boundary

A zero row or column forces all its entries zero; delete them before classifying actual dimension and applying(2)-(5). With both active sides>=2 and positive active margins,(2) gives c1>0. With at most one active row or column, including the all-zero margins, the unique complete table is a point and P=1,c1=0.

D itself has the correct deletion identity: for a proper nonempty subset of the remaining k-1 indices, the two weights according as the deleted zero index is absent/present add to the lower-size weight. In beta notation,

 beta(a,k-a)+beta(a+1,k-a-1)=beta(a,k-1-a).

Excluded empty/full subsets have zero cut minimum. Repeated deletion therefore reconciles the cut expression with the active-dimensional statement, without a false full-dimensional boundary convention.

## 5. Exact remaining endpoint

This retires negative LINEAR-coefficient search throughout the entire transportation constructor. All ordinary coefficients c_k for k>=2 remain governed by their separate exact known regions and degree protections; auxiliary higher negatives do not become whole negatives. The general ordinary LR c1 problem, all LR coefficient positivity, whole ranks above six, and unrestricted KTT are not settled. The proof relies on the expressly cited total-residue and wall-crossing theorems, not fresh reproduction of their full external histories. New provider results remain subject to independent review.
