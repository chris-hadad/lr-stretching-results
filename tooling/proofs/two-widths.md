# Two independent widths over a composition simplex

`two_width_count(a,b,total=T,left_offset=y,right_offset=w,dilation=t)`
counts exactly the integer points

```text
u_i >= 0, sum_i u_i = T*t,
0 <= x <= y*t + sum_i a_i*u_i,
0 <= z <= w*t + sum_i b_i*u_i.
```

The gain vectors have the same positive length n. All gains, offsets and T
are nonnegative integers. The two interval coordinates are independent once
u is fixed. Their coupling through the composition is retained.

Write `A=sum(a)`, `B=sum(b)`, `C=sum(a_i*b_i)`,
`alpha=(A*B+C)/(n*(n+1))` and
`beta=(n*C-A*B)/(n*(n+1))`. Exact first and second composition moments give

```text
P(t) = binom(T*t+n-1,n-1) * (1 + L*t + Q*t^2),
L = y+w + T*(A+B)/n + T*beta,
Q = y*w + T*(y*B+w*A)/n + T^2*alpha.
```

The evaluator uses exact rational arithmetic and checks scalar integrality.
The polynomial API multiplies the factors and trims trailing zeros; it does
not fit sampled values. The degree is at most n+1 and can drop when T or
widths vanish. For T=0 the answer is `(1+y*t)*(1+w*t)`.

The [complete moment derivation](sources/two-widths-original.md) also gives
the sufficient coefficient condition
`(n+1)*(A+B)+n*C-A*B >= 0`. It is not a necessary condition for positivity
of the complete product. These abstract lattice polytopes admit ordinary
negative coefficients. For `a=(7,0), b=(0,7), T=1, y=w=0`, the complete
vector is `(1,-1/6,7,49/6)`. This is an abstract example, with no asserted
whole LR realization. The dated source discusses antecedents; no novelty
claim is attached to this API.

