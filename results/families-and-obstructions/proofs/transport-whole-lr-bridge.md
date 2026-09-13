# Whole transportation/LR counts and three-row coefficient positivity

This independent derivation proves the stated results rather than inferring
them from a finite positive panel. Source identities and the complete
fifteen-claim inventory are recorded separately. The independent calculation
does not use the original AI-derived implementation.

## 1. Full transportation lattice and the complete LR bridge

Let r=(r_1,r_2,r_3) and c=(c_1,...,c_N) be strictly positive integer margins,
with common total M and N>=2. Let T consist of every nonnegative real 3-by-N
matrix with those margins. The row/column equations have exactly one linear
dependence: after changing signs on the column equations, their matrix is the
oriented incidence matrix of K_(3,N), of rank N+2. The matrix with entries
r_i c_j/M is strictly positive. Thus no additional affine equation is hidden
in nonnegativity, and dim(T)=3N-(N+2)=2N-2.

The incidence matrix is totally unimodular. An elementary determinant proof
expands a square submatrix along any column containing at most one nonzero;
if every column has two nonzeros, all column sums vanish and the determinant
is zero. Induction gives determinants 0,+1,-1. Hence every vertex of T is
integral. Moreover its affine integer lattice is the whole solution lattice:
choose entries of the first two rows in the first N-1 columns freely over Z;
row totals force their last entries, and column totals force the third row,
with the final equation following from total balance. This is a saturated
lattice of rank 2N-2, with no lattice-index multiplier.

Consequently the full count F(t)=#(tT intersect Z^(3N)) is an integral-polytope
Ehrhart polynomial, exact degree d=2N-2 and F(0)=1. Exact degree uses positive
relative volume, not the observed interpolation degree. The same argument
gives degree (p-1)(N-1) for p positive rows.

Here is an independent complete LR realization. For arbitrary p>=2 put
R_i=sum_(k>=i) r_k, C_j=sum_(k>=j) c_k and alpha=(R_2,...,R_p). Define

    lambda=(M+R_2,...,M+R_p,C_1,...,C_N),
    mu=(M repeated p-1 times,C_2,...,C_N),
    nu=(R_1,...,R_p).

Lambda is outer. These are partitions, mu is contained in lambda, and

    |lambda|-|mu| = M+sum_(i=2)^p R_i = |nu|.

The maximum trimmed length is N+p-1. The top component of lambda/mu is alpha
translated past column M. The remaining skew rows have intervals
(C_(j+1),C_j], all disjoint from each other and from that component. Therefore

    s_(lambda/mu)=s_alpha product_j h_(c_j).

Likewise nu/alpha has disjoint rows with intervals (R_(i+1),R_i], so
s_(nu/alpha)=product_i h_(r_i). Hall adjointness gives

    c^lambda_(mu,nu)
       = <s_nu,s_alpha product_j h_(c_j)>
       = <product_i h_(r_i),product_j h_(c_j)>.

The Cauchy kernel product_(i,j)(1-x_i y_j)^(-1) identifies this last scalar
product with the coefficient of x^r y^c, counting every nonnegative matrix.
There is no chosen face, omitted summand, multiplier or extra count. All tail
formulas are homogeneous, so the equality holds for the same triple dilated
by every integer t>=0. At t=0 both sides are 1. This proves complete count
equality, without asserting a geometric hive/transportation isomorphism.
The p=1 case, if desired, is the same empty-alpha calculation and a point.

## 2. Exact scalar contraction and polynomial continuation

Write q_1=x_2/x_1 and q_2=x_3/x_2, expanding in their nonnegative powers.
Partial fractions for h_k(x_1,x_2,x_3) have three terms

    x_1^k / ((1-q_1)(1-q_1 q_2)),
    -x_2^(k+1)/x_1 / ((1-q_1)(1-q_2)),
    x_3^(k+2)/(x_1 x_2) / ((1-q_1 q_2)(1-q_2)).

Assign each column j to one of the three terms. Let n_i count assigned
columns, and S_i sum their margins. The full contribution is

    (-1)^n_2 K_(n_1+n_2,n_1+n_3,n_2+n_3)(u,v),
    u=(S_1-r_1)t-n_2-n_3,
    v=(r_3-S_3)t-2n_3,

where K_(a,b,c) extracts q_1^u q_2^v from
(1-q_1)^(-a)(1-q_1 q_2)^(-b)(1-q_2)^(-c).

The all-1 assignment contributes
binom(r_2 t+N-1,N-1) binom(r_3 t+N-1,N-1). Every other eventual survivor
has n_1>0, S_1>r_1, S_3<r_3 and a,b,c>0. Equality in either slope condition is
excluded by its negative offset. For such a survivor,

    K_(a,b,c)(u,v)
      = sum_(k=0)^min(u,v) binom(u-k+a-1,a-1)
          binom(k+b-1,b-1) binom(v-k+c-1,c-1).

For 0<=u<=v set l=u-k. Expand the last binomial by Vandermonde in binom(l,j).
Use binom(l+a-1,a-1) binom(l,j)
=binom(a+j-1,j) binom(l+a-1,a+j-1), then convolve in l. This gives

    sum_(j=0)^(c-1) binom(a+j-1,j)
       binom(v-u+c-1,c-1-j) binom(u+a+b-1,a+b+j-1).

The other chamber interchanges (a,u) and (c,v). The comparison of u-v must
retain both its slope and its offset: at a slope tie the offset decides.
Integral nonzero slopes have absolute value at least 1, while relevant
offsets have magnitude below 2N; thus t>=2N is a safe uniform stabilization
bound. Each contracted product has total binomial degree a+b+c-2=d.

The signed sum of these eventual polynomials equals the literal full count
for infinitely many integer t, hence equals F identically, including t=0.
Continuing individual summands to small t does not turn them into literal
counts there. The factorial d! clears their ordinary coefficient denominators:
the product denominators k! l! divide (k+l)!=d!.

The independent evaluator uses scalar contractions only at t>=2N, then an
integer finite-difference/Newton conversion to recover every coefficient.
The implementation differs from the original coefficient accumulator and
uses an independent implementation. Literal transportation DP and bare lrcalc
controls are separate count models; scalar contraction and Newton interpolation
share the just-proved mathematical identity.

## 3. Both linear cancellation kernels and all assignment boundaries

Use a=n_1, b=n_2, c=n_3 in this section. Set U=S_1-r_1, V=r_3-S_3 and
W_(a,b)=(a-1)!(b-1)!/(2(a+b-1)!). Nontrivial survivors have U,V>0.
For 0<=h<k the unique zero falling-factorial term gives

    [t] binom(st+h,k)=s (-1)^(k-h-1) h!(k-h-1)!/k!.

In the U<=V chamber, the two polynomial binomials are

    binom((V-U)t+2b-1,b+c-1-j),
    binom(Ut+2a-1,2a+b+c+j-1).

For b>=1 the second has one zero factor. Its derivative reduces the signed
assignment coefficient to (-1)^(c-1) U S_(b+c), where

    S_m=sum_(j=0)^(m-1) (-1)^j binom(a+b+j-1,j)
          binom(2b-1,m-1-j) B(2a,m+j).

Here B(p,q)=(p-1)!(q-1)!/(p+q-1)! for positive integers. To evaluate S_m,
take the coefficient of z^(m-1) in

    integral_0^1 (1-y)^(2a-1)(1+zy)^(2b-1)/(1+zy^2)^(a+b) dy.

The beta integral follows by expanding both factors. Set
X=(1-y)^2/(1+zy^2). Then
(1+zy)^2/(1+zy^2)=1+z-zX and
dX/dy=-2(1-y)(1+zy)/(1+zy^2)^2. Near z=0 the substitution sends y=0,1
to X=1,0 and transforms the integral into

    (1/2) integral_0^1 X^(a-1)(1+z-zX)^(b-1) dX.

This is a polynomial in z of degree b-1. Its coefficient is

    S_m=(a-1)!(b-1)!/[2(a+m-1)!(b-m)!]  if 1<=m<=b,
    S_m=0 otherwise.

Thus a,b,c>0 yields zero, whereas c=0 yields -W_(a,b)U.

In the V<=U chamber, the corresponding two factors are

    binom((U-V)t+a+c-1,a+b-1-j),
    binom(Vt+a+b-1,a+b+2c+j-1).

For c>=1 the second has a zero factor. The derivative is
(-1)^(b-1) V D(a,b,c), with

    D=sum_(j=0)^(a+b-1) (-1)^j binom(b+c+j-1,j)
           binom(a+c-1,a+b-1-j) B(a+b,2c+j).

Let H=a+b+c, Q_0(k)=1/k and
Q_b(k)=k product_(q=1)^(b-1)(k^2-q^2) for b>=1. Cancelling factorials rewrites D
as the positive prefactor (a+c-1)!(a+b-1)!/(b+c-1)! times

    sum_(k=c)^(H-1) (-1)^(k-c) Q_b(k)Q_c(k)
                       /[(H+k-1)!(H-k-1)!].

Q_b Q_c is an even polynomial, including b=0 after cancelling its factor k.
Its degree is below 2H-2. Its zeros allow the lower endpoint to become 1.
The complete alternating binomial sum over -(H-1)<=k<=H-1 is a finite
difference of too high order, hence zero. Pair positive and negative k:
the positive half is minus half the k=0 term. That term vanishes for b>=1;
for b=0 it is (-1)^(c-1)((c-1)!)^2. Therefore D=0 when b>=1 and
D=W_(a,c) when b=0. The latter gives -W_(a,c)V.

The missing-last-class case c=0 cannot be inserted into B(a+b,2c+j) at j=0.
Isolate that term: the second binomial has constant 1, and the first contributes
-2W_(a,b)(U-V) after its assignment sign. For j>=1 the same finite-difference
calculation uses the even polynomial Q_b(k)/k with constant
(-1)^(b-1)((b-1)!)^2; the resulting contribution is -W_(a,b)V. The complete
boundary contribution is -W_(a,b)(2U-V), agreeing with -W_(a,b)U at U=V.
When b=0, actual positive margins imply V=U-r_2<U, so the other chamber
and its tie do not arise. Missing first class a=0 never survives.

We have therefore checked the full list:

| Assignment type | Complete signed ordinary linear contribution |
|---|---|
| a,b,c>0 | 0 in both chambers and slope ties |
| a,b>0, c=0 | -W_(a,b)(U+(U-V)_+) |
| a,c>0, b=0 | -W_(a,c)V on its actual domain V<U |
| a=0 | no surviving assignment |
| all columns assigned to 1 | (r_2+r_3) H_(N-1) |

## 4. Positive subset formula and quantitative geometry of c1

For every nonempty proper S subset [N] put s=c(S) and
w_S=(|S|-1)!(N-|S|-1)!/[2(N-1)!]. Summing the preceding list gives

    L=(r_2+r_3)H - sum_S w_S[(s-r_1)_+
                           +(s-(M-r_2))_+ +(s-(M-r_3))_+],
    H=H_(N-1).

Binomial cardinality summation and complementary subsets give
sum_S w_S=H, sum_S w_S s=MH/2 and w_S=w_(S complement). Replace S by its
complement in the final two hinges and use x_+-(-x)_+=x in the first. Then

    L=MH/2-sum_S w_S sum_i(r_i-s)_+
     =sum_S w_S [sum_(i=1)^3 min(r_i,c(S))-c(S)].

For 0<s<M let phi(s)=sum_i min(r_i,s)-s. If zero, one or at least two rows
are at least s, respectively, phi(s) equals M-s, equals M-max_i r_i, or is
at least s. Hence phi(s)>=min(s,M-s,M-max_i r_i)>0. Since both a proper
nonempty subset and its complement weigh at least min_j c_j,

    L>=H_(N-1) min(min_j c_j,M-max_i r_i)>0.

Every min of two linear functions is concave in all margins jointly. The
formula is therefore a jointly concave, homogeneous, piecewise-linear real
extension at fixed total, separately symmetric in rows and columns. This is
the extension defined by the formula; rational margins do not thereby acquire
a period-one undilated counting polynomial. N=1 is separately a point with
c1=0. Zero margins must be deleted before computing dimension; the strict
three-positive-row theorem cannot be transferred unchanged to such inputs.

## 5. Sharp extrema and a complete ordinary-positive family

For positive integral rows and integer 1<=s<=M-2, the same elementary cases
give phi(s)>=2; at s=M-1 every row is at most M-2 and phi=1. Rows
(M-2,1,1) attain these bounds simultaneously. If u counts unit columns, the
subsets with sum M-1 are exactly their complements, each weighted 1/(2N-2).
Thus, at fixed columns,

    min_r L=2H_(N-1)-u/(2N-2).

For M=N all columns are units. For M>N at most N-1 are units, attainable
with (M-N+1,1,...,1). This proves the two claimed global integer minima.
No uniqueness classification is implied.

At these row extrema the entire polynomial is

    F(t)=binom(t+N-1,N-1)^2-u binom(t+2N-3,2N-2).

To count, choose each minor row as a composition of t; the major row is
forced. Only unit columns can violate nonnegativity. Two violations would
require more than the total 2t, so inclusion-exclusion stops after single
violations. For one violating column write A=t-x, B=t-y. Its condition is
A+B<=t-1, and its other entries have count
binom(A+N-2,N-2) binom(B+N-2,N-2). Summation gives the displayed subtracted
binomial by convolution and the hockey-stick identity. This is a full count.

To prove every ordinary sign, write A(t)=product_(j=1)^(N-1)(1+t/j)^2,
C(t)=product_(j=1)^(2N-3)(1+t/j), alpha=u/(2N-2), and A=(1+t)B.
In descending order the slopes of B are
1,1/2,1/2,1/3,1/3,...,1/(N-1),1/(N-1), each at least the corresponding
slope 1/k of C. Hence B-C is coefficientwise nonnegative. Also alpha<1:
for N>=3, u<=N<2N-2; for N=2, M>=3 implies u<=1<2. Therefore

    F=(1+t)(B-C)+C+(1-alpha)tC

has strictly positive coefficients through degree 2N-2. This proves the
unbounded full family, not just its six additional test vectors.

Concavity and separate symmetry put the real fixed-total maximum at equal
rows and columns. Set q=ceil(N/3)-1. At uniform margins, grouping subsets
by size gives

    max L=(M/2)[sum_(k=1)^q 2/(N-k)+sum_(k=q+1)^(N-1)1/k]
         =(M/2)[3H_(N-1)-H_q-2H_(N-q-1)].

At k=N/3 the two terms agree, so either breakpoint convention works.
Pairwise integer balancing is a convex combination of a vector and its
transposition and cannot decrease a symmetric concave function. Repeating
it produces integral maximizing rows and columns with differences at most 1.
The uniform real value is attained integrally when 3 and N both divide M;
other totals need not attain it. These extrema concern only c1.

## 6. Complete absorber and structural failures

For N>=2, b,c>=1, q>=b+c, use columns (q,1^(N-1)) and rows
(q+N-1-b-c,b,c). The two minor-row entries x_j,y_j in unit columns obey

    x_j,y_j>=0, x_j+y_j<=t, sum x_j<=bt, sum y_j<=ct.

Their heavy-column entries are forced to bt-sum x and ct-sum y. Their sum
is at most (b+c)t<=qt, so the remaining heavy entry is automatically
nonnegative. Every other entry is forced integrally. This is a bijection
of the full affine lattice fiber; the complete polynomial is independent
of q in the stated range. The threshold is a premise, and no general
ordinary sign beyond c1 is inferred for this larger family.

For rows (1,1,2), columns (2,1,1), assignment (1,2,2), the local derivative
is -1/4. The six simultaneous row/class orderings have contributions
(-1/4,0,-1/4,0,0,0), averaging -1/12. The full polynomial is nonetheless

    1+(5/2)t+(7/3)t^2+t^3+(1/6)t^4.

The four-row fixture r=(1,1,1,1), c=(2,2) is independently counted by
choosing four integers between 0 and t with sum 2t. Single cap subtraction
gives binom(2t+3,3)-4binom(t+2,3), or

    1+(7/3)t+2t^2+(2/3)t^3.

The naive four-row replacement in the three-row subset formula gives 2,
so that proposed formula is falsified. This positive full polynomial is
not an ordinary-negative example; an A3 correction remains possible.

## 7. Verification limits, source overlap and open questions

Independent arithmetic verifies all 39 main vectors and all 1,679 rational
coefficients, degrees 2 through 126, using 1,679 determining stabilized scalar
evaluations and 78 unused holdouts. All 111 named literal transportation-DP
sites agree. Five degree 4,6,8,4,3 controls have the separate 40-value bare
lrcalc panel (30 determining values, ten unused holdouts); final receipt joins
are reported in verification-summary.json. Higher-degree vectors are proved
identity-backed reconstructions, not full independent bare-LR interpolations.

Checks include all 90 source linear-only cases, 1,024 beta-A and 576 beta-B
sums, 1,600 literal-vs-contracted A2 scalars, 768 assignment boundary/tie
derivatives, the two complete structural fixtures, and 63 uniform maxima.
These finite checks corroborate the proof; they do not replace its premises
or enlarge the original-box coverage. The 16 absorber records remain a
finite higher-coefficient positive panel.

The source character note and nonnegative-multiplicity lemma match their
recorded source bytes. The scalar partial-fraction setup is inherited. The
transportation LR embedding and its 3-by-8 example already appear in
[Ferudun, arXiv: 2607.22301v1, section 7](https://arxiv.org/html/2607.22301v1),
checked on 6 September 2026. This overlap establishes attribution only;
this version does not replace the separately specified rank-five source.
No worldwide novelty, expert endorsement or publication priority is claimed.

The proof excludes a negative linear coefficient in the entire stated
three-row transportation family. It does not exclude higher ordinary
negativity there, all LR linear negativity, or negativity with four rows.
The complete A2 contraction's c2 retains three-way terms whose c1
cancellation no longer suffices. Four-row A3 corrections require the exact
7/3 reference value. Six-run constant-direction flows, bounded complete-graph
constructions and a one-exceptional-column chamber roster are not computed in
this note. The result does not exclude them or add finite-box coverage.
