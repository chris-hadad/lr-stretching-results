# A70: a convex complete weighted-cap quadratic

Curated accepted mathematical source; the module guide states its exact domain.

Let d=(d_1,...,d_m) be nonnegative integer widths, D=sum d_j, and h an integer. Define


```text
F_d(h;t) = sum_(0<=x_j<=d_j t) product_j(x_j+1)
                     binom(h t-sum_j x_j+1,2),
```

where the last factor is zero if h t-sum x_j<0. Its value at excess zero is also zero. For h<=0 the whole count is zero. Delete zero-width variables with their positions recorded: they have x_j=0 and weight one. For h>0 and all remaining widths positive, this is an integral polytope count with auxiliary splits giving each weight x_j+1, and a two-variable nonnegative composition with one strict coordinate. Its eventual polynomial has degree at most 2m+2; the following finite identity proves polynomiality on the entire ray. We do not use this degree ceiling to promote any larger original degree claim.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation. The count below retains every bounded variable and its integer endpoint. No provider working result is a premise. It is a complete auxiliary count, not by itself an ordinary LR polynomial. Its use in BALANCED-SPLITTING.md is through an exact whole-original identity.

## Complete generating function and every original offset

For each nonnegative integer a,


```text
sum_(x=0)^a (x+1)z^x
  =[1-z^(a+1){(a+2)-(a+1)z}]/(1-z)^2,
sum_(e>=0) binom(e+1,2)z^e=z/(1-z)^3.
```

Use (d_j t+2)-(d_j t+1)z=1+(d_j t+1)(1-z). The complete product gives


```text
F_d(h;t)=sum_(J subset[m]) (-1)^|J|
   sum_(K subset J) product_(j in K)(d_j t+1)
   binom((h-d_J)t+2m+1-|J|-|K|, 2m+2-|K|).       (1)
```

For the count at a particular t, the binomial is zero outside its ordinary nonnegative range. For the eventual polynomial retain exactly h>d_J, and interpret each surviving binomial as its falling-product polynomial. At h=d_J its upper constant is smaller than its lower index by |J|+1 and nonnegative, so the entire binomial is identically zero. For h>d_J, any positive integer t still below the support threshold gives an upper integer between zero and lower-index-minus-one; the polynomial binomial is then zero as well. Hence this eventual formula is the exact count at every t>=0, not merely an unverified initial-band continuation. At t=0 every binomial vanishes, as does F.

Put H_n=sum_(i=1)^n 1/i, H_0=0, and for 0<=k<=j<=m set


```text
a_(m,j,k)=(2m+1-j-k)! j!/(2m+2-k)!,
A_(m,j)=sum_(k=0)^j binom(j,k) a_(m,j,k)
                      [H_(2m+1-j-k)-H_j],
B_(m,j)=sum_(k=1)^j binom(j-1,k-1) a_(m,j,k).
```

The falling binomial in (1) has one zero factor at t=0. Its linear coefficient is (-1)^j a_(m,j,k)(h-d_J), and its quadratic coefficient is that number times (h-d_J)[H_(2m+1-j-k)-H_j]. Multiplication by product_(K)(1+d_j t), including the original sign (-1)^j, therefore gives the exact complete quadratic coefficient


```text
C_d(h)=[t^2]F_d(h;t)
  =sum_(J subset[m]) {A_(m,|J|)(h-d_J)_+^2
                   +B_(m,|J|)d_J(h-d_J)_+}.      (2)
```

Every labeled subset is retained. Equal widths can be grouped only with exact multiplicities. B_(m,0)=0 and B_(m,j)>0 for j>=1. The A coefficients need not be positive: A_(2,2)=-13/360. Dropping those terms changes the complete function.

Formula (2) also defines the unique homogeneous piecewise quadratic extension to rational widths and h: clear all denominators at once, compute the integer ray, and divide its quadratic coefficient by the square of that common scale. There is no rational-lattice or residue relaxation. Continuity extends the resulting identity to real parameters for the analytic argument; only the scaled integral originals support counting claims.

## The entire smooth curvature is nonnegative

The elementary beta logarithmic integral gives


```text
a_(m,j,k)[H_(2m+1-j-k)-H_j]
  = integral_0^1 x^j(1-x)^(2m+1-j-k)
                              log((1-x)/x) dx.
```

Summing over k and putting u=1-x yields the single exact representation


```text
A_(m,j)=integral_0^1 u^(2(m-j)+1)(1-u^2)^j
                                  log(u/(1-u)) du.       (3)
```

All integrals converge: exponents at zero are at least one, and powers times logarithms at one are integrable, including j=0. In an open h interval between ALL subset sums, (2) has


```text
C_d''(h)/2 = integral_0^1 u f_h(u) log(u/(1-u)) du,
f_h(u)=Prob(sum_j d_j X_j<h),
```

where the independent X_j have Prob(X_j=1)=1-u^2. This retains the entire subset sum: the probability of a particular J is (1-u^2)^|J| u^(2(m-|J|)). Couple every X_j using fixed independent uniforms. As u increases, each X_j decreases. Since d_j>=0, f_h is nondecreasing. The logarithm is also strictly increasing.

For the positive measure u du, Chebyshev's integral inequality follows directly by integrating


```text
(f_h(u)-f_h(v))
   [log(u/(1-u))-log(v/(1-v))]>=0
```

against u v du dv. Here integral u du=1/2 and integral u log(u/(1-u))du=1/2. Consequently


```text
C_d''(h)/2 >= integral_0^1 u f_h(u)du >=0.       (4)
```

For h>0 the empty subset alone gives f_h(u)>=u^(2m), so on every positive open interval


```text
C_d''(h)>=1/(m+1)>0.
```

At a subset-sum knot, each coincident J contributes the derivative jump B_(m,|J|)d_J>=0. The squared hinges contribute no jump. Thus C_d is convex on the ENTIRE real h line, not just on chamber interiors, and strictly increasing for h>0. At h=0 it and its first derivative are zero. All coincident labeled subsets add; zero widths may be removed before the argument. This proof supplies the arbitrary-m/width quantifier; finite rational checks do not.

## Exact terminal polynomial and useful chord bound

For h>=D the final cap is never truncated. Let P(t)=product_j binom(d_j t+2,2). Under weights product(x_j+1), direct finite sums give


```text
sum weight*x_total = (2D/3)t P(t),
sum weight*x_total^2
  =[(4D^2/9+sum d_j^2/18)t^2+(D/6)t]P(t).
```

Also P(0)=1 and [t]P=3D/2. Substitute into the full quadratic binomial to obtain


```text
C_d(h)=h^2/2+Dh/12+(sum d_j^2)/36-11D^2/72,
                                                  h>=D.       (5)
```

At h=D every truncated boundary summand is zero, so the formula includes equality. In particular, for D>0,


```text
C_d(D)=31D^2/72+(sum d_j^2)/36 <=11D^2/24,
0<=C_d(h)<=h C_d(D)/D<=11Dh/24,     0<=h<=D.   (6)
```

The second line is the chord inequality of the proved complete convex function, and uses sum d_j^2<=D^2. It pays a moving weighted sum with all endpoints present. It is not an inference from pointwise nonnegative counts. For m=0, D=0, the separate exact formula is C_empty(h)=h_+^2/2.

## Limits and discriminators

The unbounded result is convexity and (6) for this full auxiliary cap. Arbitrary transportation split gains still have coupled cap/complement terms and are not settled by it. A stronger bound C_d'(h)<=13h/12 for h>=0 would give useful derivative control; the initial exact unit-width probe supports it through m=24 at the complete half-integer node roster, but no such theorem is claimed. Local negative A coefficients remain a mandatory countercontrol. A convexity claim made by dropping them is false reasoning even when the whole result happens to be true.
