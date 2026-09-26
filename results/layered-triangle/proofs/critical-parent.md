# Critical parent

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. Exact whole count, including the critical endpoint

Set x=bt, y=2x+1, and Q=y^r. The sum of the r small-layer edge variables, after translation, has generating polynomial (1+z+...+z^(2x))^r; write its coefficients h(s), 0<=s<=2rx. Put N(j)=sum_(s<j)h(s). The large edge of bound At creates a flat interval of bundle sums of size 2(A-rb)t+1. Every other bundle count is one of Q-N(j), j=1,...,2rx, on each side. Thus, for the ENTIRE three-bundle flow and hence original LR count,

    P_(A;b,r)(t)=[2(A-rb)t+1]Q^3+2 sum_(j=1)^(2rx)[Q-N(j)]^3.       (1)

All three bundles have the SAME list of widths; conservation says that their three aggregate currents are equal. There are no unspecified complementary flows. Symmetry of h gives N(2rx+1-j)=Q-N(j), including j=1 and2rx. Pairing the entire cube sum therefore gives

    P_(A;b,r)(t)=(2At+1)Q^3-3Q T_r(x),
    T_r(x)=sum_(j=1)^(2rx) N(j)[Q-N(j)].                          (2)

To count T, take two small-layer configurations of totals u<v. There are v-u separating integers j. Therefore T=sum_(u<v)(v-u)h(u)h(v). Reflection of one configuration identifies this with

    sum_(s=0)^(2rx) (2rx-s) [z^s](1+...+z^(2x))^(2r).

Complete inclusion-exclusion and the twice-cumulative stars-and-bars identity yield

    T_r(x)=sum_(j=0)^(r-1) (-1)^j binom(2r,j)
                    binom(2(r-j)x+2r-j,2r+1).                  (3)

This is a polynomial identity at EVERY integer x>=0. Indeed the j>=r actual counts vanish because their remaining sum 2(r-j)x-j is negative. For j<r the top binomial argument is nonnegative and its ordinary polynomial zeros give exactly all inactive small grades. The omitted j>=r terms are not evaluated as negative-top polynomial binomials. The once-only -j from the finite upper bounds remains in (3). The weight convention gives T_r(0)=0 and P(0)=1.

Equations(2)-(3) are the COMPLETE two-parameter ordinary coefficient field, of actual degree3r+1. They are not a fitted polynomial or a selected moment. In particular, for D=A-rb>=0,

    P_(A;b,r)(t)=P_(rb;b,r)(t)+2Dt(2bt+1)^(3r).                  (4)

The initial critical parent in (4), not just the positive increment, is treated next.

## 2. The exact signs of the central finite differences

For 0<=ell<r put

    S_(r,ell)=sum_(j=0)^(r-1)(-1)^j binom(2r,j)(r-j)^(2ell+1).

Then (-1)^(r+ell+1) S_(r,ell)>0. Here is a full argument rather than an appeal to observed signs.

For integer ell>=0 the absolutely convergent integral identity is

    |v|^(2ell+1) = (-1)^(ell+1) 2(2ell+1)!/pi
      integral_0^infinity [cos(vu)-sum_(a=0)^ell (-1)^a(vu)^(2a)/(2a)!]
                                         u^(-2ell-2) du.       (5)

Near zero the bracket is O(u^(2ell+2)); at infinity its largest polynomial term divided by u^(2ell+2) is O(u^-2). For v=0 both sides vanish; for nonzero v scale u by |v|. Repeated integration by parts reduces the remaining constant integral to (-1)^(ell+1)/(2ell+1)! times integral_0^infinity sin(u)/u du. The latter is pi/2: inserting exp(-epsilon u), differentiating the absolutely convergent integral with respect to the frequency gives epsilon/(epsilon^2+a^2), and integration from a=0 to1 gives arctan(1/epsilon). Integration by parts bounds the oscillatory tail uniformly and justifies the epsilon-down-to-zero limit. Every intermediate integration-by-parts boundary term in (5) vanishes by the same near-zero/at-infinity estimates.

Apply sum_(j=0)^(2r)(-1)^j binom(2r,j) to (5) at v=r-j. All even polynomial terms in the bracket have degree<=2ell<2r and vanish under this finite difference. The cosine sum is

    Re[e^(iru)(1-e^(-iu))^(2r)] = (-1)^r 2^(2r) sin^(2r)(u/2).

The power absolute values pair about j=r, giving twice S_(r,ell). Thus

    S_(r,ell)=(-1)^(r+ell+1) 2^(2r)(2ell+1)!/pi
           integral_0^infinity sin^(2r)(u/2) u^(-2ell-2) du.     (6)

This last integral is finite: its zero-end exponent is2r-2ell-2>=0, and its tail is O(u^-2ell-2). It is strictly positive on intervals. This proves the exact sign for all r and ell in the stated range, including r=1,ell=0. No numerical integration is required.

## 3. Full y-polynomial and the exact moment payment

Let e_k denote the k-th elementary symmetric polynomial in 1^2,...,r^2. Replacing x by(y-1)/2 in (3) gives

    T_r((y-1)/2)=1/(2r+1)! sum_(j=0)^(r-1)(-1)^j binom(2r,j)
                     (r-j)y product_(k=1)^r[((r-j)y)^2-k^2].   (7)

The sign in (6) shows that ALL coefficients below the highest y-power are negative. More precisely define the explicit positive rational numbers

    beta_(r,ell)= e_(r-ell) |S_(r,ell)|/(2r+1)! >0,
                                           0<=ell<r.

There is a positive rational a_r such that

    T_r((y-1)/2)=a_r y^(2r+1)-sum_(ell=0)^(r-1) beta_(r,ell)y^(2ell+1),
    a_r=sum beta_(r,ell).                                    (8)

The last equality follows from T_r(0)=0, i.e. y=1, and proves a_r>0 without another sign assumption. These are completely specified finite rational sums, not unknown capacities.

The first derivative of (3) at x=0 is especially simple. At the simple root top argument2r-j, the derivative of the binomial is

    2(r-j)(-1)^j(2r-j)!j!/(2r+1)!.

Multiplication by (-1)^j binom(2r,j) leaves2(r-j)/(2r+1). Summing gives

    T'_r(0)=r(r+1)/(2r+1),
    2 sum_(ell=0)^(r-1) beta_(r,ell)(r-ell)
                                 =r(r+1)/[2(2r+1)].           (9)

The second equation includes the factor1/2 from x=(y-1)/2. Dropping that factor destroys the following compensation.

## 4. A positive expansion of the ENTIRE critical parent

Define c_r=r(r-1)/[2(2r+1)]>=0 and

    R_r(y)=c_r y^(3r)
      +3 sum_(ell=0)^(r-1) beta_(r,ell)
             sum_(j=0)^(2(r-ell)-1)[y^(3r)-y^(r+2ell+1+j)].    (10)

Then the COMPLETE critical polynomial is

    P_(rb;b,r)(t)=y^(3r)+(y-1)R_r(y),     y=1+2bt.             (11)

To prove (11), use y^M-y^m=(y-1)sum_(j=0)^(M-m-1)y^(m+j) on each term of(8). Formula(2) at A=rb starts as

    [1+r(y-1)]y^(3r)-3 sum beta_(r,ell)[y^(3r+1)-y^(r+2ell+1)].

Factoring y-1 leaves r y^(3r) minus the complete sum of lower powers. Adding and subtracting its coefficient sum times y^(3r), and applying(9), gives r-3r(r+1)/[2(2r+1)]=c_r and exactly(10). This retains every term of the original field.

For any integers M>=m>=0, (1+2bt)^M-(1+2bt)^m has NONNEGATIVE ordinary coefficients, since binom(M,k)>=binom(m,k) for every k. Every exponent inside(10) is <=3r. Equations(6),(9)-(11) therefore give a coefficient-positive valuation with explicit positive rational weights. They do not infer ordinary signs from positive integer values.

It follows that EVERY ordinary coefficient of P_(A;b,r) is nonnegative on A>=rb, b>=0. For b>0 all coefficients through actual degree3r+1 are strictly positive. For r>=2 the leading degree is supplied by c_r(y-1)y^(3r); lower degrees already appear in y^(3r). For r=1, c_r=0 but beta_(1,0)=1/6 and (11) becomes y^2(y^2+1)/2, also strictly positive through degree4. Formula(4) preserves the conclusion. In feasible coordinates (D,b), the ENTIRE coefficient field, not merely each numerical evaluation, is monomial nonnegative.

The complete first coefficient is

    [t]P_(A;b,r)=2A+3b r(3r+1)/(2r+1),
    [t]P_(rb;b,r)=b r(13r+5)/(2r+1).                          (12)

These follow either from(2),(9) or from(10)-(11). They are consequences of the whole-polynomial theorem, not substitutes for it.
