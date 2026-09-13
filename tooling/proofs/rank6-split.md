# Complete principal rank-six split sector

The public input is an ordinary triple `(lambda,mu,nu)`, lambda outer.
Partitions are validated and padded to six after trimming trailing zeros.
Trace is required. The API does not swap the two inner partitions to seek a
different supported presentation.

Set

```text
S = sum(mu[:3]) + sum(nu[:3]) - sum(lambda[:3]),
A = lambda[2] - mu[2] - nu[2],
B = mu[3] + nu[3] - lambda[3].
```

The implementation requires S,A,B nonnegative and checks all 51 original
parent minima: 21 nonnegativity, 15 column and 15 ballot inequalities. This
is the complete sufficient domain check for the displayed chart. Requiring just
S,A,B nonnegative would be unsound.

The [whole tableau argument](sources/rank6-split-original.md) supplies nine
nonnegative cross entries y of total S, plus
`0<=s<=A+column_3(y)` and `0<=v<=B+row_1(y)`. Its real/integer inverse
selects literal row counts; deleting one cross entry gives the saturated
composition lattice. Every original parent inequality is retained.

For an affine parent row `d+sum(w_ij*y_ij)+e*s+f*v`, its exact minimum is

```text
d + min(e,0)*A + min(f,0)*B
  + S*min_ij(w_ij + min(e,0)*[j=3] + min(f,0)*[i=1]).
```

The runtime constructs and evaluates every such domain check before count shortcuts,
including t=0. On the accepted domain, the entire LR polynomial is

```text
P(t) = binom(S*t+8,8) * (1+(A+S/3)*t) * (1+(B+S/3)*t).
```

For S>0 its actual degree is 10 and every coefficient is positive. For S=0
it is the product `(1+A*t)*(1+B*t)`, with its actual degree 0, 1 or 2.
A rejected domain check raises `ValueError`; it asserts neither infeasibility nor a
negative count. The domain is not the whole rank-six space or a full fan.

The sole packaging adaptation changes the partition-validation import to
two exact internal partition-validation helpers. The chart, inequalities and all mathematical
function bodies are unchanged.

