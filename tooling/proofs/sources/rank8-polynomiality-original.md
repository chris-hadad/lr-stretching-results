# Polynomiality on the complete clipped parameter cone

Root derivation, FRI. Proposed proof for independent review. Write
`s=m+b`, where `0<=b<=m` are integers. The contraction in
RANK8-AGGREGATION.md is one polynomial of total degree at most 21 in `m,b`
on this entire closed cone. No extra chamber or exceptional small parameter
is needed. This permits a finite, exact two-parameter coefficient certificate.

## Base contribution

In the uncut top contribution, use `p=m+b-r-q` and separate the bottom
factor into its simplex count and its exclusion. The first sum has
`0<=r<=m`, `0<=q<=m+b-r`. Its summand is the product of the polynomial
weight `binom(p+3,3)*binom(q+3,3)*binom(r+7,7)`, of degree 13, and the
bottom cubic and conditional top cubic, of combined degree six.

For the bottom exclusion put `q=m+h`. It occurs precisely when
`h>=1`, `r>=0`, `r+h<=b`. Here `r<=m` is automatic. Its summand is again
a polynomial of degree at most 19. These two nested sums have affine
integer endpoints and therefore give polynomials of degree at most 21.

The conditional top cubic used here is the exact expression
`B(m+s/2)+(1+(m+s/2)/2)*(p(p+4)/20+q(q+4)/20+r(r+8)/36)`.
There is no parity-dependent summation limit; the halves are rational
coefficients only.

## Both column tails

The lower tail uses one column and the upper tail uses its three-column
complement. In either case let the selected total be `z`, with
`0<=z<=b-1`, and the positive cut depth be `b-z`. Call the number of
selected columns `a`, equal to one or three.

First take the bottom simplex term, which depends only on the last two row
totals `r`. Let `x` be the total in their selected columns. The four disjoint
blocks have sizes `2a`, `8-2a`, `2a`, `8-2a` and totals
`x`, `r-x`, `z-x`, `s-r-z+x`. Thus their complete labeled-entry weight is

```text
J_a(r,z,x) = binom(x+2a-1,2a-1)
            * binom(r-x+7-2a,7-2a)
            * binom(z-x+2a-1,2a-1)
            * binom(s-r-z+x+7-2a,7-2a).
```

Since `r<=m` and `z<=b-1`, one has `r+z<s`; the exact intersection range
is `0<=x<=min(r,z)`. Split it into `0<=r<=z` and `z+1<=r<=m`. All the
resulting endpoints are affine integer expressions; `z<m` includes the
wall `b=m`. Multiplying `J_a` by `B(m-r)` and `(b-z)(b-z+1)` gives degree
at most 17, so the triple sum has degree at most 20.

Now subtract the bottom exclusion. Put `q=m+h` and `w=b-h`, with
`0<=w<=b-1`; the other three rows total `w`. Conditional on their selected
column entries, those three rows are exchangeable. The expected total of
the last two rows is exactly `2w/3`. The bottom exclusion therefore has
the conditional average

```text
E V(m-r,h) = h(h+1)*(3m-2b+5)/6.
```

If `v` is the selected-column total in the other three rows, their exact
four-block weight is

```text
K_a(w,z,v) = binom(v+3a-1,3a-1)
            * binom(w-v+11-3a,11-3a)
            * binom(z-v+a-1,a-1)
            * binom(m+b-w-z+v+3-a,3-a).
```

Here `0<=v<=min(w,z)`; the fourth block is nonnegative because
`m+b-w>=m+1>z`. Split `w<=z` and `w>=z+1`. The product of `K_a`, the
displayed exclusion average and `(b-z)(b-z+1)` has degree at most 17;
its triple sum has degree at most 20.

The complete lower and upper tails are the respective simplex sums minus
these exclusion sums, multiplied by `5(m+1)/6` and `(6m+4-b)/6`.
Their degrees are therefore at most 21. This is exactly the contraction's
two tails, with every original cut and bottom-empty branch retained.

## Why finite summation is a polynomial proof

For every nonnegative integer power `k`, the exact sum of `i^k` over an
integer interval is the difference of its rational polynomial discrete
antiderivative at the two endpoints. Applying this successively to the
regions above proves polynomiality and the degree bound. Each eliminated
summation index raises total degree by at most one. An upper endpoint one
below the lower endpoint gives zero by the same difference identity.
Consequently `b=0`, `m=b`, and the origin are included; the two tails are
empty when `b=0`. Every binomial in a summand has fixed nonnegative lower
index and is evaluated on a nonnegative block total before it is expanded.

Set `u=m-b`, `v=b`. The cone becomes `u,v>=0`, and the whole count is a
polynomial `G(u,v)` of total degree at most 21. Its 253 values at
`i,j>=0`, `i+j<=21` determine it uniquely in the triangular Newton basis
`binom(u,i)*binom(v,j)`. Exact conversion to ordinary powers is a finite
coefficient certificate. Independent nonnegative column-transfer counts
can check that complete determining set and separate positive holdouts.

If all ordinary coefficients of `G` are nonnegative, then every ordinary
coefficient of `G(U*t,V*t)` is nonnegative for all nonnegative integers
`U,V`. That final sign assertion is conditional on the actual certificate,
not implied by polynomiality or by positive values on the grid.
