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
has n_1>0, S_1>r_1, S_3<r_3 and a,b,c>0. Equality in either slope gate is
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
The implementation differs from the returned coefficient accumulator and
uses no returned executable. Literal transportation DP and bare lrcalc
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
