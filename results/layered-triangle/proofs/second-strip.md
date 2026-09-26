# Second strip

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. The entire original family

Use the U07 whole-row construction, given in the main proof. For positive widths w_1,...,w_N, let W=sum w_j. Take the straight components (4W,2W), followed by (4w_j,2w_j). Offset each component to the right by the sum of the first rows of all later components. Concatenating offset+component rows gives outer Lambda; concatenating each offset twice gives M. The content is (6W,4W,2W). Omit zero-width components before counting the original rank.

The first straight component is forced superstandard. Its adjacent-color surplus is 2Wt; the remaining total of each color is exactly 2Wt, so all subsequent ballot prefixes hold. All columns inside every later component remain; different components have disjoint columns. The full source proof gives a homogeneous piecewise integral-unimodular map and inverse from each component to three cyclic triangle flows in [-tw_j,tw_j]. The two original content equations say that the three bundle currents agree. This identifies the ENTIRE original tableau set with the complete bounded circulation set, not a face or selected coefficient. It does not imply globally affine equivalence, additivity, or integral original GT vertices.

Take r>=2, b>=1, and (r-2)b<=A<=(r-1)b. There are r copies of b and one distinguished width A. Put

    x=bt, p=(rb-A)t, q=p-x=((r-1)b-A)t, y=1+2x, Q=y^r.

Thus 0<=q<=x and p=x+q. When A,b>0, original rank is 2r+4 and actual dimension is 3r+1. If A=0 (possible here only at r=2), remove its component: rank6, dimension4. The whole source map and dimension proof, rather than the three-color count, own those quantities.

Let U_r(j)=binom(j+r-1,r) for integers j>=1 and zero for j<=0. Let N(j) count r integers in [0,2x] with sum strictly below j. The complete U08 interval identity, included unchanged, is

    P=Pcritical(x)-2pQ^3+R,
    R=3 sum_(j=1)^(2p-1) N(j)N(2p-j)[2Q-N(j)-N(2p-j)].       (1)

The critical parent is A=rb, and its full positive compensation is supplied in the included U07 proof. Identity (1) retains the positive part of the joint common-current interval; it is not a tail-only positivity assertion.

## 2. Restore the first bounded subtraction before regrouping

Write L=2x+1. For every argument occurring in (1), j<=4x-1, so at most one small-coordinate upper bound is violated. Consequently

    N(j)=U_r(j)-r U_r(j-L).                                  (2)

Both shifted factors U_r(j-L) and U_r(2p-j-L) cannot be nonzero together: that would require 2p>=2L+2=4x+4, contradicting p<=2x. This exact empty-product fact is essential; it does not survive unchanged in deeper strips.

For f=U_r(j), g=U_r(2p-j), d=rU_r(j-L), the difference on the side where d is nonzero is

    (f-d)g[2Q-f+d-g]-fg[2Q-f-g]
          =dg[2f+g-2Q-d].                                   (3)

The opposite side is its reflection. Set u=j-L and v=2q-1-u. Both are positive on the entire changed range u=1,...,2q-2. Define the full polynomial auxiliaries

    A_r(z)=binom(2z+2r-1,2r+1),
    B_r(z)=sum_(j=0)^r binom(r,j)^2 binom(2z+3r-j-1,3r+1),
    D_r(q,x)=sum_(u=1)^(2q-2) U_r(u)U_r(2q-1-u)U_r(u+2x+1)  (4)

at nonnegative integer parameters, with empty sums zero. The all-grade identity is

    P=Pcritical(x)-2(x+q)Q^3
          +6Q A_r(x+q)-6B_r(x+q)+Delta_r(q,x),
    Delta_r=12r D_r(q,x)-6r(r-1)B_r(q-1/2)-12rQ A_r(q-1/2). (5)

To prove (5), sum (3) and its reflection, then use symmetry in u,v. The terms sum U(u)U(v), sum U(u)^2U(v) are respectively A_r(q-1/2), B_r(q-1/2). Their complete formal-series identities are in U08 and are also reconstructed below. The q-1/2 is an AUXILIARY notation for the literal 2q-1 endpoint. It is not a half-integer LR boundary, a denominator change, or a replacement of the original stretch.

## 3. A finite complete mixed polynomial, not an unevaluated growing sum

For 0<=h<=r define

    E_(r,h)(q)=(h+1) sum_(j=0)^min(r-1,h)
       [binom(r-1,j)binom(h,j)/(j+1)]
                          binom(2q+2r+h-2-j,2r+h+1).        (6)

Then

    D_r(q,x)=sum_(k=0)^r binom(2x+k-1,k) E_(r,r-k)(q),       (7)

where the k=0 factor is1. These are finite full coefficient polynomials, retaining all lower-order terms.

Here are elementary derivations. Rising-factorial Vandermonde gives

    binom(u+2x+r,r)=sum_(k=0)^r
             binom(2x+k-1,k)binom(u+r-k,r-k).

Also

    sum_(u>=1)U_r(u)binom(u+h,h) z^u
     =(h+1)z/(1-z)^(r+h+1)
          sum_(j=0)^min(r-1,h) binom(r-1,j)binom(h,j)z^j/(j+1). (8)

To verify (8) without importing a parameter-specific hypergeometric claim, apply (1/h!)d^h/dz^h to z^(h+1)/(1-z)^(r+1). Leibniz expansion gives numerator

    (h+1) sum_(l=0)^h binom(h,l)binom(r+l,l)z^l(1-z)^(h-l)/(l+1).

Its z^j coefficient is (h+1)binom(h,j) times

    sum_(l=0)^j (-1)^(j-l)binom(j,l)binom(r+l,l)/(l+1)
          = binom(r-1,j)/(j+1).

The last equality is the jth forward difference of binom(r+l,r-1)/r; repeated Pascal differences prove it. Multiplying (8) by z/(1-z)^(r+1) and extracting degree 2q-1 proves (6). Vandermonde then proves (7).

For q=0 or1 all terms in (6) vanish as genuine binomial zeros; all upper arguments at q=0 are nonnegative for r>=2. Both shifted A and B also vanish there. Thus the polynomial identities include the first empty overlap grades, rather than merely eventual equality. At t=0, q=x=0, the whole expression has constant1. It is not the literal count of separately collapsed strict regions.

Equations (1)-(8) are a complete all-grade two-parameter field on the stated strip. The flow incidence matrix and bound rows give a separate integral-polytope polynomiality and degree bound. No original LR polynomial is fitted to establish these identities.
