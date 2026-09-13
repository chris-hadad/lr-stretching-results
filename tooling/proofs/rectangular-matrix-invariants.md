# Rectangular matrix invariant scalar counts

`rectangular_matrix_invariant_count(p,q,m,t)` counts the degree
`lcm(p,q)*t` invariant multiplicity for m labeled p-by-q matrices under
the specified `SL(p) × SL(q)` action. It requires positive exact integer
p,q,m and nonnegative exact integer t. Divisibility of the entry degree does
not imply that the invariant space is nonzero.

Writing d=lcm(p,q)*t, the exact Weyl extraction uses all signed pairs
`sigma in S_p, tau in S_q` and all nonnegative integer tables X with margins

```text
row_i(X) = d/p + i - sigma(i),
col_j(X) = d/q + j - tau(j),
weight(X) = product_ij binom(X_ij+m-1,m-1).
```

Negative margins contribute zero. Sorting margin profiles preserves their
full signed multiplicities; equal-cap allocation orbits retain their exact
labeled weights. The implementation keeps the complete Cartesian pairing of
row and column Weyl profiles. It returns an integer, not a partial signed sum.

The [maintained API source contract](sources/rectangular-api-original.md)
and [adoption excerpt](sources/rectangular-adoption.md) document the
rectangular extension and work controls. The existing
[square proof](matrix-invariants.md) gives the underlying weighted-table
extraction. When p=q the rectangular API delegates to the square API. Its
scalar size/grade exchange is not extended to nonsquare rectangles.

Optional `max_states` and `max_transitions` are nonnegative integer
ceilings. Exhaustion raises `MatrixCountLimitError` with the resource and
statistics; there is no count/value attribute. Work ceilings do not bound wall
time, integer bit complexity or total memory. Caches are local to a call, with
a bounded number of completed allocation schedules, not a global byte cap.

At t=0 the scalar is 1. For m=1 and p unequal to q, positive grades give zero.
The separate `matrix_invariants_to_lr(n,m)` constructs a complete LR family
only for square matrices, n>=1 and m>=2, retaining the original n and entry
grade n*t. General rectangular inputs have no constructor, actual-degree
routine or polynomial/positivity assertion in this API.

