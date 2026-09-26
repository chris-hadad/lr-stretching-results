# Correlated roots

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. Factor the complete sum before any absolute value

Every falling product in B has the common factors s-1,s,...,s+2r-1. Consequently

    (3r+1)! B_r(s/2)= [product_(j=-1)^(2r-1)(s+j)] H_r(s+r-1),       (1)

    H_r(v)=sum_(k=0)^r binom(r,k)^2
          (v-r-1)_(falling k) (v+r+1)_(rising r-k).                 (2)

No k-term has been discarded. H_r has degree r and positive leading coefficient
binom(2r,r). Define G_r(v)=(v+r+1)_(rising r)(v-r)_(rising r).
The backward product rule gives the exact discrete Rodrigues identity

    H_r(v)=nabla^r G_r(v)/r!.                                     (3)

Indeed nabla^k (v+r+1)_(rising r)=(r)_(falling k)
(v+r+1)_(rising r-k), while the other factor, differenced r-k times at v-k,
is (r)_(falling r-k)(v-r-k)_(rising k). The binomial coefficient in the
product rule, after division by r!, is binom(r,k)^2, yielding(2).

## 2. Orthogonality and the exact location of the roots

For integer v, let g(v)=G_r(v) on -r<=v<=0 and zero elsewhere.
G_r already vanishes on -2r,...,-r-1 and1,...,r. Hence on -r,...,r,
nabla^r g equals the polynomial nabla^r G_r, and outside that interval it
vanishes. Discrete summation by parts over the integers therefore gives, for
any polynomial q of degree<r,

    sum_(v=-r)^r H_r(v)q(v)=(-1)^r/r! sum_v g(v) Delta^r q(v)=0.     (4)

Thus H_r is a degree-r orthogonal polynomial for the positive uniform measure
on the2r+1 nodes -r,...,r. Here is the needed root argument. Form the product
q of all real sign-changing roots of H in(-r,r), each taken once. If fewer
than r exist, Hq has constant sign on[-r,r] and is nonzero at at least one
support node (degree H=r<2r+1). Its weighted sum is nonzero, contradicting(4).
Therefore all r roots are real, simple and strictly inside(-r,r).
There can be at most one root in(r-1,r): if there were two, multiplying H
by H divided by those two factors produces a nonnegative, nonzero function
on EVERY support node, again contradicting orthogonality to degree r-2.

Rodrigues gives the endpoint values, including all normalization factors,

    H_r(r)=(2r)!/r!,
    H_r(r-1)=-(r-1)H_r(r)/2.                                    (5)

For the first, only the final difference term is nonzero. For the second,
only the last two are nonzero: G_r(0)=(-1)^r(2r)!, and
G_r(-1)=(-1)^r r(r+1)(2r-1)!. Their signed combination proves(5).
For r>=2, exactly one root lies in(r-1,r), and all other roots are below r-1.
In s-coordinates that root is theta in(0,1); every other H root is negative.
For r=1,H_1(v)=2v, and set theta=0; the extra root coincides with s=0.

Accordingly there are positive a_1,...,a_(r-1) (an empty list for r1) and
K>0 for which

    B_r(s/2)=K s(s-1)(s-theta)
                product_(j=1)^(2r-1)(s+j) product_i(s+a_i).       (6)

This root description follows from the complete correlation, not from
numerical root approximations. In particular the original alternating
coefficients may have both signs even though the roots are controlled.

## 3. A uniform coefficient envelope of order r^-2

For a real polynomial F write |F|_coeff for the polynomial of absolute ordinary
coefficients. Let <=_coeff mean coefficientwise inequality. Multiplication by
nonnegative-coefficient polynomials preserves this order, and
|FG|_coeff <=_coeff |F|_coeff |G|_coeff.

At p=1, the k0 binomial in the original sum is1 and all others vanish, so
B_r(1)=1. Evaluating(6) at s=2 determines

    K=1/[(2-theta)(2r+1)! product_i(2+a_i)].                       (7)

Now0<=theta<1, so (s+theta)<=_coeff(1+s). For j>=1,
(s+j)<=_coeff j(1+s), and for a>0,
(s+a)<=_coeff max(1,a)(1+s), with max(1,a)/(2+a)<=1.
Take coefficient absolute values in(6) ONLY AFTER the complete factorization.
Using(7) and retaining the full common integer-root product gives

    |B_r(s/2)|_coeff
    <=_coeff s(1+s)^(3r)/[2r(2r+1)(2-theta)]
                            product_i max(1,a_i)/(2+a_i)
    <=_coeff s(1+s)^(3r)/[2r(2r+1)].                            (8)

Thus, for every r>=1,

    |B_r(p)|_coeff <=_coeff p(1+2p)^(3r)/[r(2r+1)].              (9)

The algebraic roots need not be computed to apply this rational bound.
The earlier exponential unsigned k-summand weight is absent because the
signed sum was combined before its roots or coefficient absolute values
were considered. This does not revive the failed U08 termwise argument.

For comparison, direct factorization of
    A_r(p)=binom(2p+2r-1,2r+1)
gives the companion full envelope

    |A_r(p)|_coeff <=_coeff p(1+2p)^(2r)/[r(2r+1)].              (10)

Its single zero factor is2p, its only negative shift is-1, and all other
nonzero shifts are1,...,2r-1. Their absolute product divided by(2r+1)!
is1/[2r(2r+1)], proving(10). No sign is assigned separately to A or B.
