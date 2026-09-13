# A coefficient-positive shift-difference operation

This is an algebraic derivation without a historical priority claim. Ordinary coefficients throughout are in the variable t. The auxiliary polynomials in this note are not individually assigned an LR realization. [The matching-layer proof](matching-three-layers.md) supplies actual whole-LR membership.

## 1. A complete algebraic base

Let B,r,m be integers with B>=1, r>=1 and m>=(B-1)r+2. Set D=m+r. Define G by its exact all-t generating series

    sum_(t>=0) G(t) z^t = (1+B z)^r/(1-z)^(D+1).

Equivalently, as a polynomial for every real t,

    G(t) = sum_(j=0)^r binom(r,j) B^j binom(t+D-j,D)
         = [(t+1)...(t+m)/D!] R_(r,m,B)(t),                 (1)

where

    R_(s,m,B)(t) = sum_(j=0)^s binom(s,j) B^j
                       t_under(j) (t+m+1)_over(s-j).       (2)

Here t_under(j)=t(t-1)...(t-j+1), and (x)_over(k)=x(x+1)...(x+k-1); empty products are one. Formula (1) factors the common factors t+1,...,t+m from every entire binomial term. There is no partial interpolation.

The exponential generating identity, as a formal identity in x, is

    sum_(s>=0) R_(s,m,B)(t) x^s/s!
       = (1+B x)^t (1-x)^(-t-m-1).                         (3)

Indeed write s=j+l in (2), and the two sums separate into the generalized binomial and rising-factorial series. Differentiate (3), multiply by (1-x)(1+B x), and compare x^k/k!. This gives the exact recurrence

    R_0=1,
    R_(k+1)=[(B+1)t+m+1-(B-1)k] R_k
                 +B k(k+m) R_(k-1),                      (4)

with the last term absent for k=0. The derivative numerator is
m+1+(B+1)t+B(m+1)x, which independently fixes both shifts and signs.

Replace t by t-1 in (4). For 0<=k<=r-1 the affine constant is

    m-B-(B-1)k >= m-(B-1)r-1 >= 1.

Thus induction proves that EVERY coefficient of R_(r,m,B)(t-1), through degree r, is strictly positive. The same holds for R(t), and every coefficient through degree r-1 of R(t)-R(t-1) is strictly positive: writing R(t-1)=sum p_k t^k with p_k>0 makes the latter difference sum p_k[(t+1)^k-t^k]. This is a coefficient argument, not a pointwise monotonicity inference.

## 2. The exact compensated difference

Put

    Omega(t)=G(t-1),
    W(t)=tG(t)-(t+m)G(t-1).                               (5)

Since m>=2, G(-1)=0; the sequence Omega(t) on t>=0 has exact generating series z times that of G. Formula (1) gives

    Omega(t)= t(t+1)...(t+m-1) R(t-1)/D!,
    W(t)= t(t+1)...(t+m) [R(t)-R(t-1)]/D!.                 (6)

Consequently G has strictly positive coefficients in degrees 0,...,D, with G(0)=1. Both Omega and W have constant zero and strictly positive coefficients in degrees 1,...,D. In W the apparent degree D+1 cancels exactly; its actual degree is D. In particular

    tG(t) >=_coeff (t+m)Omega(t).                          (7)

Also R(0)=(m+1)_over(r)=D!/m!, so

    G(t) >=_coeff binom(t+m,m).                           (8)

The quotient R(t)/R(0) has positive coefficients and constant one. This proves (8) without dividing a coefficientwise inequality by a polynomial.

## 3. A sufficient full-coefficient operation

Let A(t)=1+a_1t+...+a_qt^q, and let Bop(t)=b_0+...+b_qt^q. These are multiplier polynomials, not the numerator parameter B. Suppose an entire count identity is proved:

    P(t)=A(t)G(t)+Bop(t)Omega(t).                         (9)

Define

    L(t)=(A(t)-1)/t,
    C(t)=Bop(t)+(A(t)-1)+m(A(t)-1)/t.                     (10)

Then exactly

    P(t)=G(t)+L(t)W(t)+C(t)Omega(t).                      (11)

If L and C have nonnegative ordinary coefficients, P>=_coeff G. If in addition every coefficient of C through degree q is positive, every ordinary coefficient of P through its degree D+q is strictly positive. For each 1<=k<=D+q a positive term of C times a positive nonconstant coefficient of Omega supplies positivity, while P(0)=1. No sign condition on b_0,...,b_q separately is necessary.

This is the compensation identity used here. The naive two-shift formula has negative b_0 for q=2, and negative b_0,b_1 for q=3. They cannot be dropped. The complete difference W absorbs them with an exact coefficientwise identity. Positive values of G and Omega at integer arguments alone would not justify this operation.

The criterion is sufficient and does not assert that every LR polynomial belongs to it. [The matching-layer proof](matching-three-layers.md) gives complete membership for three unbounded six-run layers. [The scope analysis](matching-scope.md) gives a legal next-layer failure of this particular certificate.
