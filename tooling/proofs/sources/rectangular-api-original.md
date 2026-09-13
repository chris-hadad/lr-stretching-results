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

```bash
PYTHONPATH=code/ehrhart/src python3 -m slr_ehrhart.cli count-rectangular-matrix-invariants 2 3 3 --t 1 --max-states 10000 --max-transitions 100000
```

This emits `value,p,q,m,t,entry_degree`, with value 20 and entry degree six.
The CLI uses the same exact JSON and error behavior as the square command.
This scalar API does not provide a general rectangular LR constructor or
degree theorem. The separate primitive p4q5 theorem and independently positive
degree-20 vector are in
[curated rectangular adoption and limits](rectangular-adoption.md).

The focused regression selectors are `test_matrix_invariants.py` and
`test_rectangular_matrix_invariants.py`; the owning FRG record contains the
42-test result, the 13-task same-input benchmark and exact review dispositions.
