# Positivity for five coupled capacities and its whole LR lift

For 1<=m<=5 and integral w_i,c,d>=0 with sum w_i>=c+d, count every pair of
nonnegative integer vectors satisfying

    sum z_i = c t, sum y_i <= d t, y_i+z_i <= w_i t.

Every ordinary coefficient through actual degree is positive; a point has
polynomial one. The complete one-overlap LR lift has ordinary rank at most
m+2, hence seven. Its parameters retain 0<=c<=h and u,v>=h+d. Zero capacities,
all walls and degree drops are included. This extends the earlier four-capacity
result; it does not prove all ordinary rank-seven LR positivity.

[Complete original model, finite certificate and LR lift](PROOF.md). The
linear coefficient uses a separate [all-capacity theorem](proofs/linear.md).
Strictness at d=0 additionally uses the existing
[3-by-5 transportation certificate](../../tooling/transport_certificates/README.md),
which includes every 2-by-m boundary needed here. From the complete repository,
its separate replay is `python3 -B tooling/transport_certificates/verify.py --out /path/to/new-transport-check`.
The finite m=5 certificate protects indices 2 through 9 by at least 1/1,000,000
times the complete actual face-volume sum in the original saturated lattice,
without factorial normalization. No geometric c1 margin is inferred.

```sh
python3 -B results/five-capacity/reproduce.py
```

The proposed portable replay uses only Python's standard library. It rebuilds
all 26,332 original subsets, full image lattices and 961 safe types; freshly
computes every exact BV value; and verifies all 7,830 corrected q7 inequalities,
54,810 incidences and 70 nonzero support vectors, with omitted supports zero.
It retains all 5,509 dependent cases. Small corruption controls distinguish
missing normals, wrong lattices, changed values and broken sparse fields.

Historical component costs total roughly twenty seconds for the961 BV values
and a few seconds for the complete geometry/field. This portable edition is
freshly replayed in the private candidate; independent publication review remains required. The theorem is accepted
A13 mathematics; no provider program, discovery LP, or hidden campaign path is
required by this replay. Its scientific limit is the finite premises: the
analytic normal-cycle, c1 and whole-LR map arguments remain in the proof files.

[All results](../../RESULTS.md) · [Main page](../../README.md) · [Tools](../../tooling/README.md)
