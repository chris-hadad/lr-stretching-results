### Rectangular invariant components

`rectangular_matrix_invariant_count(p,q,m,t,*,max_states=None,max_transitions=None)`
counts the full invariant component for m p-by-q matrices under SL_p times
SL_q at entry degree lcm(p,q)*t. It requires exact Python integers p,q,m>=1
and t>=0, with the same work-limit and per-call cache contract as the square
API. Square inputs use the existing square implementation and its proven
size/stretch exchange. Unequal sides retain both original ranks.

The two Weyl margin targets are lcm(p,q)*t/p and lcm(p,q)*t/q. Their separate
signed profiles use the complete Cartesian pairing. Grade zero returns one;
one unequal-sided matrix has zero invariants at every positive grade. Grade
divisibility alone does not imply nonvanishing. Empty components return exact
zero; an exhausted work limit raises an exception without a numerical count.
Rectangular diagnostics count both Weyl groups; `margin_profiles` is the sum
of their two completed profile-list sizes. Square diagnostics are unchanged.

```sh
PYTHONPATH=tooling python3 -B -c 'from slr_ehrhart import rectangular_matrix_invariant_count; print(rectangular_matrix_invariant_count(2, 3, 3, 1))'
```

This prints the exact count 20 at entry degree six. The scalar API uses
the same exact arithmetic and work-limit behavior as the square case.
This scalar API does not provide a general rectangular LR constructor or
degree theorem. The separate [primitive 4-by-5 theorem](../../../results/families-and-obstructions/proofs/rectangular-premises.md)
and its [positive degree-20 vector](../../../results/families-and-obstructions/data/rectangular/full-polynomial.json)
concern the complete rank-twenty-four LR family.

The focused regression selectors are `test_matrix_invariants.py` and
`test_rectangular_matrix_invariants.py`; the original verification record contains
the 42-test result and 13-task same-input benchmark.
