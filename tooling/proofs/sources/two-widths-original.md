# Two affine intervals: the compensation term and its failure

Root derivation, Astra004, 9 September 2026. Independent review complete; see review/DISPOSITIONS.md.
The statements concern complete polytopes in the explicitly specified lattice.
An application to LR requires a complete hive map; no such map is asserted for
the negative example. No claim of worldwide novelty is made.

## Complete model and exact moment identity

Let `n>=1` be an integer, let `T,y,w` be nonnegative integers, and let `a,b`
be nonnegative integral vectors of length `n`. Every count identity below is
for nonnegative integer stretches `t`. In the composition lattice consider
the entire polytope

```text
u_i >= 0, sum_i u_i = T,
0 <= x <= y + sum_i a_i u_i,
0 <= z <= w + sum_i b_i u_i.
```

Deleting one composition coordinate gives its saturated ambient integer chart.
At dilation `t`, the complete count is the sum of the two interval counts over
every composition of `T*t`. No independence of the two widths is assumed.
Write

```text
A = sum a_i, B = sum b_i, C = sum a_i*b_i,
alpha = (A*B+C)/(n*(n+1)), beta = (n*C-A*B)/(n*(n+1)),
B_n(s) = binom(s+n-1,n-1).
```

Then the exact all-t identity is

```text
E(t) = B_n(T*t) * (1 + L*t + Q*t^2),
L = y+w + T*(A+B)/n + T*beta,
Q = y*w + T*(y*B+w*A)/n + T^2*alpha.
```

For completeness, over the uniform set of weak compositions of an integer
`s`, symmetry and the generating functions for first and second factorial
moments give

```text
average(u_i) = s/n,
average(u_i*u_j) = s*(s-1)/(n*(n+1))                 (i != j),
average(u_i^2) = 2*s*(s-1)/(n*(n+1)) + s/n.
```

These are identities of finite sums: use
`sum(k>=0) k*z^k = z/(1-z)^2` and
`sum(k>=0) k*(k-1)*z^k = 2*z^2/(1-z)^3`, multiply by the
remaining geometric factors, and extract `z^s`. Consequently

```text
average((a.u)*(b.u)) = alpha*s^2 + beta*s.
```

Expanding `(y*t+1+a.u)*(w*t+1+b.u)` proves the formula, including `n=1`,
`T=0`, zero widths and every dimension drop. Polynomial degree is read from
this complete identity, rather than estimated from a fit.

## A positive operation with a concrete restriction

All ordinary coefficients are nonnegative whenever

```text
(n+1)*(A+B) + n*C - A*B >= 0.                       (1)
```

Indeed (1) makes `L>=0` for every nonnegative `T,y,w`, while `Q>=0` is
automatic. Every factor of `B_n(T*t)` has positive constant and nonnegative
slope. Their product proves the claim. The condition is sufficient, not an
assertion that every failure of (1) is a negative polynomial.

This is also the exact condition for coefficientwise nonnegativity of the
displayed quadratic residual at all nonnegative offsets and totals: set
`T=1,y=w=0` for necessity. It is not a necessary condition for nonnegativity
of the full product, whose simplex factor can compensate a negative residual.

A convenient uniform consequence is that **all gains at most four are safe**.
More precisely, suppose `0<=a_i,b_i<=G`. Put `S=A+B`. Since
`A*B<=S^2/4` and

```text
C >= max(0, G*(S-G*n)),
```

we have `A*B-n*C <= G*n*S/4`. To verify the last step, if `S<=G*n` use
`S^2/4<=G*n*S/4`. If `G*n<=S<=2*G*n`, the desired upper bound follows from

```text
S^2 - 5*G*n*S + 4*G^2*n^2 = (S-G*n)*(S-4*G*n) <= 0.
```

The lower bound for `C` follows termwise from
`(G-a_i)*(G-b_i)>=0`. Therefore the left side of (1) is at least
`(n+1-G*n/4)*S`. In particular `G<=4*(n+1)/n` suffices, and `G<=4`
works simultaneously at every `n`. This is a sufficient gain bound for two
intervals; no assertion about arbitrarily many intervals follows.

The hidden compensation is explicit. The potentially negative linear moment
is `n*C-A*B`: large opposing widths make it negative, while sufficient overlap
raises `C`. The endpoint terms `(n+1)*(A+B)` supply the remaining protection.
Counting widths without their overlap loses precisely this information.

## A complete negative join in dimension three

Take `n=2`, `T=1`, `y=w=0`, `a=(a,0)` and `b=(0,b)`, with positive integer
gains `a,b`. The polytope in coordinates `(k,x,z)` is

```text
0 <= k <= 1, 0 <= x <= a*k, 0 <= z <= b*(1-k).
```

It is exactly the convex hull of
`(0,0,0),(0,0,b),(1,0,0),(1,a,0)`. Its four vertices are integral and
affinely independent, its affine lattice is `Z^3`, and its normalized volume
is `a*b`. Its whole count is

```text
sum(k=0..t) (a*k+1)*(b*(t-k)+1)
 = 1 + (1+(a+b)/2-a*b/6)*t + (a+b)*t^2/2 + a*b*t^3/6.
```

Only the linear coefficient can be negative. It is negative precisely when
`a*b>3*a+3*b+6`, equivalently `(a-3)*(b-3)>15`. Thus `(a,b)=(7,7)` gives

```text
E(t) = 1 - t/6 + 7*t^2 + 49*t^3/6,
E(0..4) = 1,16,94,284,635.
```

The boundary `(6,8)` has zero linear coefficient; `(4,19)` has `c1=-1/6`.
These are exact sign thresholds in this family, not a global minimum-size or
minimum-rank assertion. In particular an LR realization would have ordinary
rank at least six by the adopted all-size rank-five theorem.

The example is not relying on a failure of integer decomposition. An integer
point of its `t`-fold dilate has integer `k` and can be written as `k` height-one
points carrying its `x` coordinate in pieces between `0` and `a`, plus `t-k`
height-zero points carrying its `z` coordinate in pieces between `0` and `b`.
This proves IDP directly. Subdivide each of the two endpoint intervals into
unit intervals; the joins of their unit subintervals triangulate the polytope
into `a*b` lattice tetrahedra of determinant one. Thus IDP and a unimodular
triangulation do not prevent this particular ordinary negative. Neither
property was assumed to be universal or sufficient for LR positivity here.

## Native inputs and scientific limits

The native F2 examples identified by the source helper explain why this is
relevant. For rng33, `n=9,A=B=3,C=1`; for rng24 seed 2,
`n=9,A=6,B=9,C=6`. In both cases `n*C=A*B`, so the quadratic residual factors
into the product of the two mean interval counts. These arithmetic parameters
must be rebound to each actual chart before campaign adoption. The native
nineteen stored towers already have individual source proofs on their stored
cones; the present result is a general operation and explanation, with no new
whole-rank coverage inferred.

The root program's first exact check compares the moment formula with 88,560
literal composition counts over its explicitly bounded controls, and retains
seven split-width examples. This supports the implementation; the all-parameter
argument above supplies the theorem. The maintained API and its own bounded
tests are separately reviewed. A02 addresses the missing negative realization.

The independent literature check found Liu, Tao and Xin's
[2026 paper on joins](https://arxiv.org/html/2606.18794v1), which discusses
failure of Ehrhart positivity under joins and preservation of IDP and
triangulations. The formulas and elementary proofs here were derived directly;
the source prevents treating the general join phenomenon as a novelty claim.
