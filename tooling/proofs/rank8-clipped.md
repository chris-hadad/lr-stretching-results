# Complete clipped rank-eight family

The API accepts exact integers `0<=M<=S<=2M`, and nonnegative integer
stretch t. Its ordinary boundary is

```text
lambda = (50M-S,46M,36M,32M,23M+S,19M,9M,5M),
mu     = (27M,23M,19M,15M,13M,9M,5M,M),
nu     = (25M,22M,19M,14M,12M,9M,6M,M).
```

For M>0 the outer area is 220M, the actual degree is 21, and every ordinary
coefficient is positive. At M=S=0 the boundary is empty and P(t)=1.
Parameters outside this interval are refused even at t=0. The API makes no
claim about S>2M and does not implement the separate M>S family.

The [whole tableau map](sources/rank8-tableau-map-original.md) retains all
92 parent inequalities and 16 row/content equations. Its saturated chart has
16 cross entries of total S and two three-simplex children. In the supported
clipped domain the three additional cuts, and the potentially empty bottom
fiber, must all be retained. The
[aggregation proof](sources/rank8-aggregation-original.md) does so.
The [polynomiality proof](sources/rank8-polynomiality-original.md) gives total
degree at most 21 in `u=2M-S, v=S-M` without parity subchambers.

The supplied certificate has exactly all 253 pairs `(i,j)` with
`i+j<=21`. The complete grid `u,v>=0, u+v<=21` determines that bivariate
polynomial. The two recorded count models agree on every grid site and four
unused sites. Its 253 monomial coefficients are positive. Evaluating at
`(u*t,v*t)` yields the full ordinary vector; for every nonzero supported
parameter pair the degree-21 term is positive.

[The source certificate](sources/rank8-certificate-original.md) and
[later adoption scope](sources/rank8-adoption.md) distinguish the completed
result from historical pending-review wording. The exact coefficient table
is in `slr_ehrhart/_rank8_clipped_data.py`. The JSON in
[data/](data/) preserves the complete mathematical chart, three cuts, strict
witness, coefficients, determining counts and unused counts while excluding
specified operational fields. Source hashes and transformations are recorded
in the tooling source map.

`check_rank8_data.py` compares the literal full coefficient and count
rosters with that table and evaluator. It checks recorded-data consistency;
it does not re-count tableaux, regenerate the chart proof or provide a new
independent mathematical acceptance. Source proof links to historical research
paths are provenance. The named proof texts and mathematical evidence above
are included locally.

