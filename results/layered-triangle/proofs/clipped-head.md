# Complete clipped head

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. Exact joint overlap, with ALL partners

Let h(s) be the distribution of the sum of r integers in[0,2x], and N(j)=sum_(s<j)h(s), with N=0 below support and N=Q above support. For current s, the large layer deletes the two disjoint tails of sizes N(p+s) and N(p-s); the complete current multiplicity is Q-N(p+s)-N(p-s). The formal untruncated whole endpoint expression is

    D=(2At+1)Q^3-3Q T_r(x),
    T_r(x)=sum_(j=0)^(r-1)(-1)^j binom(2r,j)
                            binom(2(r-j)x+2r-j,2r+1).        (1)

D is the actual dominant parent formula when A>=rb, as proved in U07. Below that threshold it is a signed continuation, NOT a count by itself. At current |s|<p both tails coexist. The difference of the complete cubes is

    (Q-u-v)^3-(Q-u)^3-(Q-v)^3+Q^3=3uv(2Q-u-v).

Summing the full overlap gives the exact all-grade identity

    P=D+R,
    R=3 sum_(j=1)^(2p-1)N(j)N(2p-j)[2Q-N(j)-N(2p-j)].       (2)

The endpoints j=0,2p vanish. At p=0 the overlap is empty. This formula also holds for a deeper balanced head if the COMPLETE bounded N is retained; replacing it by the unbounded tail outside its domain is forbidden. Equation(2) is equivalent to summing the literal positive part of the original common-current interval, over ALL small-flow configurations. It does not discard clipped configurations or multiply t full levels in their place.

For0<=p<=x, every nonzero argument in(2) is at most2x-1, so no small-flow upper bound is reached and N(j)=binom(j+r-1,r). Symmetry in j yields

    R=6Q A_r(p)-6 B_r(p),
    A_r(p)=binom(2p+2r-1,2r+1),
    B_r(p)=sum_(k=0)^r binom(r,k)^2
                            binom(2p+3r-k-1,3r+1).          (3)

This is the COMPLETE two-parameter coefficient field on the top balanced strip, for every r. It keeps all lower coefficients and every once-only shift. All top arguments at p=0 are nonnegative and smaller than the bottom arguments, so both polynomials vanish there. Inactive small positive p terms likewise vanish by genuine binomial zeros, not negative-top continuations.

Here is a full formal-series verification. sum_(j>=1)N(j)z^j=z/(1-z)^(r+1), hence its square gives A_r. Also

    sum_(n>=0)binom(n+r,r)^2 z^n
                = [sum_(k=0)^r binom(r,k)^2 z^k]/(1-z)^(2r+1).

To verify the last identity without an unproved positivity premise, its left coefficients satisfy n^2 c_n=(n+r)^2 c_(n-1) and c0=1. Writing theta=z d/dz, its differential equation is theta^2 F-z(theta+r+1)^2F=0. The numerator H obeys theta^2 H-z(theta-r)^2H=0 by k^2 binom(r,k)^2=(r-k+1)^2binom(r,k-1)^2. Product differentiation shows(1-z)^(-2r-1)H obeys the first equation and has constant1, proving equality of all coefficients. Multiplying the resulting series for N(j)^2 by that for N(j) gives exactly B_r and(3).
