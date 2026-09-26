# The complete original construction

## Original boundary, full inverse, saturated lattice and dimension

Let the positive layer widths be w_1,...,w_N and W=sum w_j. Use straight
components `(4W,2W)` followed by `(4w_j,2w_j)`. The offset o_j is the sum of the
first-row lengths of all later components. Concatenate `(o_j+4w_j,o_j+2w_j)`
for outer Lambda and `(o_j,o_j)` for M, with the first component's width W.
The final content is Nu=(6W,4W,2W). Lambda is outer; its total skew size is
12W, exactly the prescribed content sum. Boundary scaling is the ORIGINAL t.

The next component's rightmost column is the previous component's inner
endpoint, so different components have disjoint columns. The first component
is forced superstandard: its rows have colors 1 and 2 respectively. It gives
content `(4Wt,2Wt,0)` and adjacent-color surpluses 2Wt. Each remaining color's
total content is 2Wt; any later prefix can consume at most that many of the
next color. Hence EVERY later ballot prefix is paid. Columns within each
component remain exactly the original columns. Deleting/inserting this prefix
is a full original-row inverse, not a restriction to selected tableaux.

For one later component, write h=tw. Its complete GT coordinates satisfy

    2h<=u<=4h, 0<=v<=2h, v<=z<=u.

The two original rows have color counts

    (z,u-z,4h-u), (0,v,2h-v).

Set r1=z-2h and r3=4h-u-v. For fixed excess content, its entire remaining
original interval is

    V0=max(0,-r3),
    V1=min(2h,2h-r3,2h+r1,2h-r1-r3), V0<=v<=V1.

For cyclic triangle edge flows `(f12,f23,f31)` in `[-h,h]^3`, set k=f31,
so f12=k+r1 and f23=k-r3. Its whole interval is

    L=max(-h,-h-r1,-h+r3),
    U=min(h,h-r1,h+r3), L<=k<=U.

Both signed widths are exactly
`2h-max(|r1|,|r3|,|r1+r3|)`. Thus empty fibers match, as do zero widths and
all endpoint ties. The full maps are

    v=V0+k-L, u=4h-r3-v, z=2h+r1;
    k=L+v-V0, f12=k+r1, f23=k-r3, f31=k.

On each max-selector region this is an integral shear in `(r1,r3,k)`, with
determinant absolute value one. The other displayed changes are unimodular,
and the maps agree at ties. It is a continuous homogeneous piecewise integral
bijection, with literal integer inverse. It is not globally affine or additive.

The original fixed content becomes

    sum z_j=2Wt, sum(u_j+v_j)=4Wt,

which maps precisely to equality of the three aggregate flow currents.
Both pairs of equations can solve two last-layer coordinates with coefficient
one. Their lattices are saturated; no hidden congruence or index is introduced.
The strict original point `(u_j,v_j,z_j)=(3tw_j,tw_j,2tw_j)` proves actual
dimension 3N-2 for positive widths. The equivalent flow has 3N coordinates,
two independent incidence equations and a strict zero-flow point.

The full graph incidence matrix together with coordinate-bound rows is totally
unimodular. Thus the bounded flow polytope has integral vertices in its saturated
cycle lattice and a polynomial Ehrhart count of degree 3N-2. This proves the
counting/degree statement without asserting integral vertices of the original
GT polytope through a piecewise map. Original rank is 2N+2; here N=r+1 when
A>0. Delete zero-width components before this accounting. With one remaining
positive width the count is 2wt+1; with none it is 1. An unrelated infeasible
positive-grade family retains the zero-polynomial convention.

Finally, translate every edge coordinate in layer j by tw_j. The three bundle
sums are equal if and only if the translated sums are equal. If

    f(k)=[z^k] product_j(1+z+...+z^(2tw_j)),

then the ENTIRE original count is `sum_k f(k)^3`. Each bundle chooses every
layer coordinate independently; the common-current constraint is retained by
the same k in all three factors. This is the independent integer organization
the finite verifier uses, and is justified by the full inverse above.

## 3. The complete cubic correction and its finite degree

For the third strip put

    x=bt, w=((r-2)b-A)t, p=2x+w, q=x+w,
    L=2x+1, Q=L^r, c=binom(r,2), 0<=w<=x.

Let `U(j)=binom(j+r-1,r)` for integer j>=1 and zero otherwise. The complete
bounded cumulative small-layer count over every argument in the common-current
identity is

    N(j)=U(j)-rU(j-L)+cU(j-2L).

Indeed j<=2p-1<=6x-1, whereas a third bounded subtraction requires
j>=3L+1=6x+4. This is a support proof; negative-top polynomial continuation is
not being applied to omitted inclusion-exclusion tails.

The [whole interval identity](proofs/clipped-head.md), is

    P=Pcritical(x)-2pQ^3+3 sum_(j=1)^(2p-1) F(N(j),N(2p-j)),
    F(f,g)=fg(2Q-f-g).

For completeness write f=U(j), g=U(2p-j), d=rU(j-L), e=rU(2p-j-L),
a=cU(j-2L), b'=cU(2p-j-2L). Products ab', ae and b'd vanish by their literal
support inequalities: they would require 2p>=3L+2 or an even larger threshold.
The product de CAN occur and is retained. Relative to the whole second-strip
continuation, direct cubic expansion leaves exactly

    de(2Q-2f-2g+d+e)
      +a g(2Q-2f+2d-g-a)+b' f(2Q-2g+2e-f-b').

Translating first-shift overlap by j=L+u and second-tail overlap by j=2L+u
gives the same complete endpoint `u+v=2w-2`, with u,v>=1. Symmetry yields

    Theta=6r(2r-1)Q A_r(w-1)
          -6r(r-1) Dcal_2
          +6r^2(r-3) Dcal_1
          +6[r^3-c(c+1)] B_r(w-1).                  (1)

I independently checked these coefficients: the first-shift part contributes
`6r^2(QA-2Dcal_1+rB)` and the second-tail part contributes
`6c(2QA-2Dcal_2+2rDcal_1-(c+1)B)`. Their sum is (1).

The second-strip correction is

    Delta=12rD_r(q,x)-6r(r-1)B_r(q-1/2)-12rQ A_r(q-1/2).

All binomial expressions below mean their full falling-product polynomials,
with an empty product equal to one. Explicitly,

    A_r(v)=binom(2v+2r-1,2r+1),
    B_r(v)=sum_(j=0)^r binom(r,j)^2 binom(2v+3r-j-1,3r+1).

The remaining auxiliary polynomials are

    E_(r,h)(v)=sum_j binom(r-1,j)binom(h+1,j+1)
                         binom(2v+2r+h-2-j,2r+h+1),
    D_r=sum_(k=0)^r binom(2x+k-1,k)E_(r,r-k)(q),
    Dcal_l=sum_(k=0)^r binom(l(2x+1)+k-2,k)
                                      E_(r,r-k)(w-1/2).

The complete identity is

    P=Pcritical(x)-2pQ^3+6Q A_r(p)-6B_r(p)+Delta+Theta.     (2)

The [complete mixed convolution](proofs/second-strip.md) follows from rising-factorial Vandermonde and
the explicit generating function for `U(u)binom(u+h,h)`. Its numerator weights
simplify to the displayed integral `binom(r-1,j)binom(h+1,j+1)`; no rational
normalization is lost. This is a finite polynomial identity for the entire
original object, including all ordinary partners.

Every term has total degree at most D=3r+1: E_(r,h) has degree 2r+h+1 and its
mixed prefactor has degree k with h=r-k; Q A and B have the same bound.
The critical parent has that bound separately. This proves the BIVARIATE
polynomial statement before any determining sites are selected. A univariate
Ehrhart degree bound alone would not prove one polynomial across the complete
parameter strip; the all-grade identity (2) is essential here.

The common sums are empty at w=0 and w=1. Their displayed polynomials vanish
there through genuine common factors. Half shifts encode the once-only
endpoint `2w-2` or `2q-1`; they are not fractional LR boundaries or lattice
changes. At x=w=0, the k=0 empty product `binom(-1,0)` equals one. A guard that
rejects all negative upper binomial arguments would corrupt this identity.
The full polynomial has constant one; separately collapsed strict pieces are
not assigned that convention automatically.

## 4. Critical-parent reserve is explicit and pays the initial parent

The U07 complete critical formula is

    Pcritical=(2rx+1)y^(3r)-3y^r T_r(x), y=1+2x,
    T_r(x)=sum_(j=0)^(r-1)(-1)^j binom(2r,j)
                       binom(2(r-j)x+2r-j,2r+1).

For ell<r, its central finite-difference sum

    S_(r,ell)=sum_(j=0)^(r-1)(-1)^j binom(2r,j)(r-j)^(2ell+1)

has sign `(-1)^(r+ell+1)`. The [critical-parent proof](proofs/critical-parent.md) derives this from the convergent
cosine remainder integral for `|v|^(2ell+1)`: lower even powers vanish under
2r differences, and the cosine sum is
`(-1)^r 2^(2r) sin^(2r)(u/2)`. The remaining integral is strictly positive;
its zero-end exponent is `2r-2ell-2>=0` and its tail is integrable. Thus this
is an all-r sign proof, not an observed finite-difference pattern.

Consequently, with the explicit positive rational weights

    beta_(r,ell)=e_(r-ell)(1^2,...,r^2)*abs(S_(r,ell))/(2r+1)!,

where e_k is the elementary symmetric polynomial of degree k,

    T_r((y-1)/2)=sum beta_(r,ell)
                       [y^(2r+1)-y^(2ell+1)].

Differentiating the original finite expression at x=0 gives

    T'_r(0)=r(r+1)/(2r+1),
    2 sum beta_(r,ell)(r-ell)=r(r+1)/[2(2r+1)].

The factor 1/2 from x=(y-1)/2 is retained. Adding/subtracting the total lower
power weight gives

    Pcritical=y^(3r)+k_r x y^(3r)+2x Eplus_r(y),
    k_r=r(r-1)/(2r+1),
    Eplus_r(y)=3 sum beta_(r,ell)
       sum_(j=0)^(2(r-ell)-1)[y^(3r)-y^(r+2ell+1+j)].    (3)

All lower exponents are at most 3r. Hence Eplus_r(1+2x) is coefficientwise
nonnegative, with fully specified positive weights. It is an actual initial
parent reserve. For A>=rb the whole count adds the explicit nonnegative term
`2(A-rb)t(2bt+1)^(3r)`. No monotonicity premise is needed to sign that cone.

## 5. Rodrigues identities, support measures and root separation

### Direct extraction of every common factor

Here is an independent elementary derivation of the factors and normalization
identities, rather than an appeal to a named Hahn family. In a falling product
for B's k-th summand, the integer shifts run from -k-1 through 3r-k-1.
Their common interval over k=0,...,r is -1,...,2r-1. Removing it leaves
`(s-2)_(fall k)(s+2r)_(rise r-k)`, exactly the H expression below after
v=s+r-1. There are no unexamined residual factors.

The backward product rule is

    nabla^n(FG)(v)=sum_k binom(n,k)
                          (nabla^k F)(v)(nabla^(n-k)G)(v-k).

Apply it to F=(v+r+1)_(rise r), G=(v-r)_(rise r), n=r.
The second factor becomes `(r)_(fall r-k)(v-r-1)_(fall k)` and the first
becomes `(r)_(fall k)(v+r+1)_(rise r-k)`. Dividing by r! gives exactly
`binom(r,k)^2`. The residual leading coefficient is
`sum binom(r,k)^2=binom(2r,r)>0` by coefficient extraction in
`(1+z)^r(1+z)^r`.

For E_(r,h), the j-th summand's shifts run from -2-j through
2r+h-2-j. If h<r, the common shifts are -2,...,2r-2; removing them leaves
`(s-3)_(fall j)(s+2r-1)_(rise h-j)`. The exact coefficient is

    binom(r-1,j)binom(h+1,j+1)
       =(h+1)binom(r-1,j)binom(h,j)/(j+1).

In the product rule applied h times to
`(s+r+h)_(rise r-1)(s-2)_(rise h+1)`, the j-th differentiated positive
block leaves the common `(s+r+h)_(rise r-h-1)` and then
`(s+2r-1)_(rise h-j)`. The other block, evaluated at s-j, leaves
`(s-2)(s-3)_(fall j)`. The coefficient after division by h! is

    binom(h,j)(r-1)_(fall j)(h+1)_(fall h-j)/h!
       =binom(r-1,j)binom(h+1,j+1).

This proves the mixed Rodrigues identity with every scalar retained.

If h=r, j ranges only through r-1. The common shifts extend through 2r-1,
and the residual is explicitly

    Htilde(s)=sum_(j=0)^(r-1) binom(r-1,j)binom(r+1,j+1)
                        (s-3)_(fall j)(s+2r)_(rise r-1-j).

Apply r-1 differences instead to
`(s+2r-1)_(rise r)(s-2)_(rise r)`. After removing
`(s-2)(s+2r-1)`, the product-rule coefficient, multiplied by (r+1)/r,
is exactly `binom(r-1,j)binom(r+1,j+1)`. This proves the exceptional
normalization, and its degree r-1 follows from the positive leading sum.
The h<r formula is never evaluated at a negative factorial length.

### Positive measures and root ranges

The load-bearing identities below permit a direct symbolic check rather than a numerical root audit.

For B_r(s/2), its common factor is `product_(j=-1)^(2r-1)(s+j)` and its
residual in v=s+r-1 is

    H_r(v)=sum_(k=0)^r binom(r,k)^2
             (v-r-1)_(fall k)(v+r+1)_(rise r-k)
          =nabla^r[(v+r+1)_(rise r)(v-r)_(rise r)]/r!.

Truncate the product to integer v in [-r,0]. Its required r exterior boundary
nodes on each side are zeros. Summation by parts proves orthogonality against
degrees below r on the uniform positive nodes [-r,r]. The degree is r with
positive leading coefficient. Endpoint evaluation gives

    H_r(r)=(2r)!/r!, H_r(r-1)=-(r-1)H_r(r)/2.

Thus for r>=2 exactly one residual s-root is in (0,1), and the other r-1
roots lie in (-2r+1,0). The normalization is B_r(1)=1: only the k=0 original
binomial term survives there. The r=1 extra root is zero, treated separately
by the earlier top-strip proofs; U12 uses r>=3 and its uniform bound r>=40.

For h<r, factor E_(r,h)(s/2) by

    C=product_(j=-2)^(2r-2)(s+j).

The residual H has degree h and satisfies

    nabla^h G/h! = W H,
    G=(s-2)_(rise h+1)(s+r+h)_(rise r-1),
    W=(s-2)(s+r+h)_(rise r-h-1).

The backward product rule yields exactly the binomial weights in section 3.
Truncate G to [-r-h+1,1-h]; its h necessary exterior nodes are zeros because
h<r. The resulting measure -W on [-r-h+1,1] is strictly positive. This proves
h simple real residual roots in (-r-h+1,1), including the h=0 constant case.
The positive Hahn identification is

    Q_h(s+r+h-1; alpha=r-h-1, beta=1, N=r+h).

For h=r, the common product extends through j=2r-1 and the residual has degree
r-1. The correct exceptional identity is

    Wtilde Htilde=(r+1)/r * nabla^(r-1)Gtilde/(r-1)!,
    Gtilde=(s-2)_(rise r)(s+2r-1)_(rise r),
    Wtilde=(s-2)(s+2r-1).

The truncated support is [-2r+2,2-r], and the positive measure -Wtilde is on
[-2r+2,1]. The roots are in (-2r+2,1). Its Hahn parameters are alpha=beta=1,
N=2r-1, with variable s+2r-2. Using the h<r formula past its negative-length
factorial would be wrong. Both branches normalize as E_(r,h)(3/2)=h+1,
because only the j=0 original binomial term survives at s=3.

The root-location argument needs only positive orthogonality on more nodes
than the degree. If the product of the sign-changing real roots inside the
support interval had lower degree, multiplying by it would have constant
nonzero sign on support, contradicting orthogonality. This gives simplicity
and all roots in the open hull.

For the stronger separation, if consecutive roots alpha<beta had no integer
node strictly between, the polynomial `H^2/[(s-alpha)(s-beta)]` would be
nonnegative on every support node and positive at some node. It equals H
times a polynomial of degree n-2, contradicting orthogonality. At a root node
the polynomial is zero, so endpoint coincidences do not evade the proof.
This proves at most one root in [k,k+1), and at most two roots in
[k,k+2), for integer k. Every required root bound below
comes from these measures and separation, not sampled root locations.

## 6. Independently re-derived U12 product attenuation

All coefficient comparisons are after x=w+z, with w,z>=0 formal. Put Z=2x,
y=1+Z, so `2q<=_c2Z`, `2p<=_c3Z` and `2w<=_cZ`.
For a normalized negative root -a and variable s<=_c C Z, the factor bound is

    |s+a|_c/(m+a) <=_c [max(C,a)/(m+a)] y.           (4)

Nonnegative exceptional roots use `max(C,theta)/(m-theta)` instead. Bounds
multiply only AFTER the complete residual has been factored.

Let M=(2r-1)(2r)(2r+1), N=(2r-2)M. The following table records all factors,
including the exceptional h=r degree change. It is valid for r>=40.

| Complete factor | Common-product envelope | Residual payment |
| --- | --- | --- |
| E_(r,h)(q) | 16q(h+1)y^(2r+h)/M | at most 1/2 if h>=r/2; otherwise 1 |
| E_(r,h)(w-1/2) | 12w(h+1)y^(2r+h)/N | at most 1/3 if h>=r/2; otherwise 1 |
| B_r(q-1/2) | 16q y^(2r)/M before residual powers | exceptional cost 2, negative product at most 1/3 |
| B_r(w-1) | 12w y^(2r)/N before residual powers | exceptional cost 3, negative product at most 1/3 |

For the first row normalize at s=3. Common shifts -2,-1 and +1 each cost an
extra factor under s<=2Z, giving 16q/M after the zero factor is retained.
At most one residual root is nonnegative. Uniformly across h<r and h=r,
there are at least h-2 negative roots, each a<=r+h-1. Since r<=2h and h>=20,
(4) bounds their product by

    ((3h-1)/(3h+2))^(h-2).

Its reciprocal exceeds the first three binomial terms of
`(1+3/(3h-1))^(h-2)`. At h=20 those terms sum to 8044/3481>2.
They increase thereafter: each ratio `(h-a)/(3h-1)` involved has positive
derivative for a>=2. Every remaining residual factor is at most one.

For the second row use current s=2w and normalize at s=4. The common shifts
are -3,-2,-1,0,...,2r-3; their constant product is 6(2r-3)!, giving 12w/N.
Residual roots shift up by one and are <2. At most two are nonnegative;
at least h-3 are negative with a<=r+h-2. The product is at most
`((3h-2)/(3h+2))^(h-3)`. The first four reciprocal-binomial terms at h20 are
74199/24389>3, increasing since `(h-a)/(3h-2)` increases for a>=3.
For h=r the common product is longer and improves the denominator; the stated
looser bound keeps the correct total y exponent.

For B_r(q-1/2), the distinguished root shifts into (1,2), costing at most two
when normalized at current s=3 with s<=2Z. Of the other r-1 roots, at most one
is nonnegative; at least r-2 negative roots have a<=2r-2. Their product is at
most `((2r-2)/(2r+1))^(r-2)`. Its first three reciprocal-binomial terms at
r40 are 2367/676>3 and increase. Therefore

    |B_r(q-1/2)|_c <=_c 32q y^(3r)/(3M),
    |A_r(q-1/2)|_c <=_c 16q y^(2r)/M.               (5)

For B_r(w-1), the distinguished root shifts into (2,3), costing at most three
at current normalization s=4 with s<=Z. At most two other roots are nonnegative;
at least r-3 negative roots have a<=2r-3. The product is at most
`((2r-3)/(2r+1))^(r-3)`. Its first three reciprocal-binomial terms at r40 are
27981/5929>3 and increase. This pays the exceptional factor completely:

    |B_r(w-1)|_c <=_c 12w y^(3r)/N,
    |A_r(w-1)|_c <=_c 12w y^(2r)/N.                (6)

The monotonicity claims in the last two paragraphs follow by writing each
binomial term as a positive constant times products `(r-a)/(2r-b)`; their
derivatives are positive because 2a-b>0 in all used factors.

For unshifted p, s=2p<=3Z and normalization is s=2. The common factor's
negative unit shift costs 3; positive shifts 1 and 2 cost 3 and 3/2.
Thus

    |A_r(p)|_c <=_c (27/2)p y^(2r)/[r(2r+1)].

B's distinguished root costs at most three. At most one other root has
0<a<1, costing at most 3/2; all others satisfy `max(3,a)/(2+a)<=1`.
Consequently

    |B_r(p)|_c <=_c (243/4)p y^(3r)/[r(2r+1)].     (7)

These constants were checked root by root. Replacing `(1+2p)` by y would be
invalid here; (7) does not make that replacement.

## 7. Every mixed term and the rank-44 scalar threshold

For k>=1 the positive prefactors obey

    binom(2x+k-1,k)<=_c (2x/k)y^(k-1)<=_c y^k/k,
    binom(4x+k,k)<=_c 2y^k;

the k=0 factors are one. The first complete weighted sum is
`1+(r+1)H_r`. Its low-h part h<r/2 is at most (r+1)/2. Applying the half or
third contraction from section 6 therefore gives exactly the safe budgets

    Sdelta=[2+(r+1)(2H_r+1)]/4,
    S1=[r+2+(r+1)H_r]/3.

The second prefactor has total weight (r+1)^2. Its low-h weight is m(m+1),
m=ceil(r/2)<=(r+1)/2. Applying the third contraction yields

    S2=(r+1)(3r+5)/6.

Substitution in ALL terms of Delta and Theta gives

    |Delta|_c<=_c delta_r q y^(3r),
    delta_r=[192r(Sdelta+1)+64r(r-1)]/M;

    |Theta|_c<=_c theta_r w y^(3r),
    theta_r=72[r(2r-1)+r(r-1)S2+r^2(r-3)S1
                                +|r^3-c(c+1)|]/N.       (8)

There is no discarded cubic partner. For r>=40,
`|r^3-c(c+1)|=c(c+1)-r^3`, and the latter equals
`(r^4-6r^3+3r^2-2r)/4>0`.

Combining (2)-(3), (7)-(8) and p<=3x,q<=2x,w<=x gives

    P>=_c y^(3r)+F_r x y^(3r)+2x Eplus_r(y),
    F_r=r(r-1)/(2r+1)-6-2673/[2r(2r+1)]-2delta_r-theta_r. (9)

The factor 2673/2 comes from `3*6*(27/2+243/4)`. In particular this pays the
ENTIRE lower-edge parent w=x, not only a width derivative or correction.

At r44 the exact harmonic value supplied for root scalar checking is

    H44=5884182435213075787/1345655451257488800 < 22/5.

Induction then gives H_r<r/10 for every r>=44, because 1/(r+1)<1/10.
Both envelopes increase with H. Replacing H by r/10 produces

    delta_bar=8(3r^2+38r+85)/[5(4r^2-1)],
    theta_bar=3(2r^4+61r^3-66r^2+15r-140)
                              /[10(r-1)(4r^2-1)].       (10)

I independently expanded (8) to obtain (10), then used the common denominator
`10r(r-1)(2r-1)(2r+1)` in (9). Its numerator is exactly

    N(r)=14r^5-569r^4-642r^3-28229r^2+43175r-13365.

Direct shift r=44+s gives ascending coefficients

    (68707375,62318223,5203283,170254,2511,14).

For example Horner evaluation gives N(44)=68707375, and differentiation gives
N'(44)=62318223. All coefficients are positive. The denominator is positive;
at r44 the resulting lower margin is 1249225/2663592. Thus F_r>0 for ALL
r>=44. No roots of N or sampled scalar values are used to infer this quantifier.
The scalar checker verifies the displayed harmonic and rational identities;
the all-r proof is the displayed algebra and positive shifted polynomial.

For b>0, y^(3r) supplies every degree through 3r, while the strictly positive
F_r x y^(3r) supplies degree 3r+1. The preserved Eplus term is nonnegative.
This establishes strict ordinary coefficient positivity on the complete
third strip for every r>=44, including its initial lower edge.

## 8. Earlier analytic strips and exact finite-field logic

The [top-strip comparison](proofs/top-strip.md) in p,q>=0, x=p+q, has scalar reserve

    r(r-1)/(2r+1)-2-12/[r(2r+1)]
      =[(r-6)(r^2+r+4)+12]/[r(2r+1)]>0 for r>=6.

It uses the complete correlated B factor, the companion A factor and the
same explicit critical reserve. This part is uniform and valid without a
finite top-strip sample. The three needed low-r fields are included in the finite certificate.

For the second strip, use x=q+z and A=(r-2)q+(r-1)z. The [mixed-factor proof](proofs/mixed-payment.md)
gives the complete scalar

    T_r=24(r+1)(H_r+1)/[(2r-1)(2r+1)],
    F_r=r(r-1)/(2r+1)-4-144/[r(2r+1)]-T_r,
    G_r=r(r-1)/(2r+1)-2-72/[r(2r+1)].

The harmonic term strictly decreases. With
`g_r=(r+1)/[(2r-1)(2r+1)]`, the ratio

    [g_(r+1)/(r+1)]/[g_r-g_(r+1)]
       =(r+2)(2r-1)/[(r+1)(2r+5)]<1

and H_r+1>=2 prove this directly. The reserve increases, the remaining negative
reciprocal decreases, and H15<10/3 gives
`F15>85498/139345>0`; also G_r>F_r. Thus the whole second strip is paid
uniformly at r>=15. Again this is the initial-parent bound, not a derivative
of a substituted coefficient envelope.

For each finite strip field, its all-grade polynomial identity proves total
degree <=D=3r+1 BEFORE reconstruction. Values on
`{(u,v) in Z_+^2:u+v<=D}` uniquely determine the field because
`binom(u,i)binom(v,j)`, i+j<=D, are a triangular basis. Exact mixed forward
differences give the Newton coefficients. Signed first-kind Stirling
coefficients convert this entire field to ordinary monomials. Since i!j!
divides D! for i+j<=D, a common denominator D! is valid. An independent
reverse conversion can use second-kind Stirling numbers and exact Pascal
values at all determining and unused sites.

The parameter maps are unimodular and preserve original width semantics:

    top:    b=p+q, A=(r-1)p+r q;
    second: b=q+z, A=(r-2)q+(r-1)z;
    third:  b=w+z, A=(r-3)w+(r-2)z.

Each matrix has determinant absolute value one. Under original stretch t the
whole count is F(tu,tv), so each ordinary t coefficient is the sum of all
monomials of its total degree evaluated at nonnegative u,v. Complete monomial
nonnegativity therefore proves the full continuum of integer parameters on
the strip; a table of positive counts alone would not.

The third-strip field contains 130626 coefficient slots: 130620 positive and
six zero. The second strip (including the extra r=2 control) contains 5382
slots, and the top strip contains 324. All determining whole counts and 342
unused holdouts were checked in the accepted A53 verification. The portable
replay recomputes them from the complete common-current distribution.
For r=3, the zero-large-layer edge has degree seven. Positive pure-z terms
supply strict positivity through degree ten when A>0. For r>=4 both pure
edge sequences are positive through degree 3r+1. Omitted slots are exact zero;
they are never dropped from verification.
