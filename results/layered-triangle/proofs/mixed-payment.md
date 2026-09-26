# Mixed payment

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. Factor the complete mixed sum

Let s=2q. For 0<=h<r put

    H_(r,h)(s)=(h+1) sum_(j=0)^h [binom(r-1,j)binom(h,j)/(j+1)]
                         (s-3)_(fall j)(s+2r-1)_(rise h-j).

Factoring the common integer roots in the COMPLETE sum (the main proof(6)) gives

    (2r+h+1)! E_(r,h)(s/2)
          = product_(j=-2)^(2r-2)(s+j) H_(r,h)(s).             (9)

Set

    G(s)=(s-2)_(rise h+1)(s+r+h)_(rise r-1),
    W(s)=(s-2)(s+r+h)_(rise r-h-1).

The backward product rule gives exactly

    nabla^h G(s)/h! = W(s)H_(r,h)(s).                         (10)

Indeed, the jth term after division by the common W has the two displayed falling/rising factors; its coefficient is

    binom(h,j)(h+1)_(fall h-j)(r-1)_(fall j)/h!
          =(h+1)binom(h,j)binom(r-1,j)/(j+1).

Let g(s)=G(s) on the integer interval [-r-h+1,1-h], and zero elsewhere. G already vanishes on all h needed left boundary nodes and the h right boundary nodes. Thus nabla^h g equals nabla^h G on [-r-h+1,1] and vanishes outside. Summation by parts against any polynomial of degree<h proves H is orthogonal on these nodes for the positive measure -W(s). The measure is positive because s-2<0 and each factor s+r+h,... is positive there. H has degree h and positive leading coefficient.

The usual root argument is short: multiply H by the product of its real sign-changing roots in the open support interval. If there were fewer than h, this multiplier would have degree<h while its product with H had constant nonzero sign on the support and was nonzero at some node, contradicting orthogonality. Consequently every root is simple, real and strictly inside (-r-h+1,1). In particular EVERY extra root is <1.

For h=r the j=r term vanishes. The common integer product is longer:

    (3r+1)! E_(r,r)(s/2)
      =product_(j=-2)^(2r-1)(s+j) Htilde_r(s),                 (11)

where Htilde has degree r-1. Put

    Gtilde=(s-2)_(rise r)(s+2r-1)_(rise r),
    Wtilde=(s-2)(s+2r-1).

The same product rule gives

    Wtilde Htilde=(r+1)/r * nabla^(r-1)Gtilde/(r-1)!.         (12)

Restrict Gtilde to [-2r+2,2-r]. Its difference has support [-2r+2,1]. The positive measure is -Wtilde there. Orthogonality of degrees below r-1 proves that all r-1 extra roots are strictly below1. These assertions include h=0 (constant extra factor); r>=2 throughout.

## 2. Normalize before taking an envelope

At s=3, the convolution defining E has only u=v=1, so

    E_(r,h)(3/2)=h+1.                                       (13)

For any root theta<1,

    |s-theta|_c/(3-theta)<=_c 1+s,

since max(1,|theta|)<=3-theta. For the common product in (9),

    |product_(j=-2)^(2r-2)(s+j)|_c
      <=_c 2s(2r-2)!(1+s)^(2r),
    product_(j=-2)^(2r-2)(3+j)=(2r+1)!.

Equations (9)-(13) therefore prove, with M_r=(2r-1)(2r)(2r+1),

    |E_(r,h)(q)|_c <=_c 4q(h+1)(1+2q)^(2r+h)/M_r.           (14)

For h=r the longer product has larger normalizing denominator (2r)(2r+1)(2r+2), so the same slightly weaker bound (14) remains valid.

Use x=q+z, q,z>=0, y=1+2x. For k>=1,

    0<=_c binom(2x+k-1,k)<=_c (2x/k)y^(k-1).

Apply (14) to EVERY term in the main proof(7), using 2x<=_c y. With the harmonic number H_r=sum_(k=1)^r 1/k, this gives

    |D_r(q,x)|_c <=_c 4q[1+(r+1)H_r]y^(3r)/M_r.             (15)

The sum of scalar payments is exact:
(r+1)+sum_(k=1)^r(r-k+1)/k=1+(r+1)H_r. No state or mixed coefficient was discarded before its bound.

## 3. Bound both shifted and unshifted complete partners

The included U09 factor proves that B_r(s/2) has roots s=0,1, theta in[0,1), the negative integers -1,...,-(2r-1), and r-1 further strictly negative roots. It is normalized by B_r(1)=1.

For B_r(q-1/2), the common integer factors are s-2,s-1,s,...,s+2r-2, with s=2q. Exactly one extra root lies in[1,2); the others are <1. Normalize at s=3. The exceptional factor has envelope ratio at most2(1+s), while all other extra factors have ratio at most1+s. Hence

    |B_r(q-1/2)|_c <=_c 8q y^(3r)/M_r,
    |A_r(q-1/2)|_c <=_c 4q y^(2r)/M_r.                      (16)

For p=x+q<=_c2x, the unshifted factors must NOT be bounded by replacing (1+2p) with y. Instead bound their roots individually. Put Z=2x, so 2p<=_c2Z. The factors with shifts 1 and theta cost at most2y each; the positive integer product costs 2(2r-1)!y^(2r-1). For every further negative root -a, max(2,a)/(2+a)<=1. The same normalization used in U09 thus proves

    |A_r(p)|_c <=_c 4p y^(2r)/[r(2r+1)],
    |B_r(p)|_c <=_c 8p y^(3r)/[r(2r+1)].                    (17)

This is a fixed factor increase, not an exponential (1+4x)^(3r) estimate.

Apply (15)-(16) to the COMPLETE Delta in the main proof(5). The result is

    |Delta_r(q,x)|_c <=_c T_r q y^(3r),
    T_r=24(r+1)(H_r+1)/[(2r-1)(2r+1)].                      (18)

Here T_r is a scalar envelope, not the earlier critical-parent polynomial with a similar historical letter. Every current use of T_r below refers only to (18).

## 4. Pay the whole original lower edge uniformly

The included U07 proof supplies the explicit expansion

    Pcritical(x)=y^(3r)+2x[c_r y^(3r)+E_r(y)],
    c_r=r(r-1)/[2(2r+1)],

where E_r is its fully specified positive weighted sum of power differences and has nonnegative coefficients after y=1+2x. Its weights and exact moment identity are part of the included proof, not an assumed unknown capacity.

Combining ALL terms of the main proof(5), (17), and (18), with x=q+z and p=2q+z, yields

    P >=_c y^(3r)+[F_r q+G_r z]y^(3r)+2x E_r(y),             (19)
    F_r=r(r-1)/(2r+1)-4-144/[r(2r+1)]-T_r,
    G_r=r(r-1)/(2r+1)-2-72/[r(2r+1)].

F_r>0 for EVERY r>=15. Here is an elementary exact threshold argument. The first term increases with r, and the rational reciprocal term decreases. Also T_r strictly decreases: if g_r=(r+1)/[(2r-1)(2r+1)], then

    g_r-g_(r+1)=(2r+5)/[(2r-1)(2r+1)(2r+3)],
    [g_(r+1)/(r+1)]/[g_r-g_(r+1)]
          =(r+2)(2r-1)/[(r+1)(2r+5)]<1,

whereas H_r+1>=2. Therefore g_(r+1)(H_(r+1)+1)<g_r(H_r+1). The exact rational sum H_15<10/3 gives

    F_15>210/31-4-144/465-1664/899
          =85498/139345>0.                                 (20)

Finally G_r-F_r=2+72/[r(2r+1)]+T_r>0. Thus (19) proves every coefficient nonnegative for every r>=15, INCLUDING q=x (z=0), the ORIGINAL lower edge A=(r-2)b. It is not inferred from a width increment. For b>0 all coefficients through degree3r+1 are strictly positive: y^(3r) supplies all lower degrees, and a positive q or z reserve supplies the highest one.
