# Linear-coefficient geometry of whole LR families

The ordinary linear coefficient c1 is nonnegative throughout ordinary rank at
most six, but it is **not concave or superadditive** on the full feasible
boundary cone. A21 supplies strict full-dimensional hives and adjacent generic
boundaries with Jensen defect 1/336 and addition defect -1/168. The displayed
first coefficients are all positive. They are complete first jets, not complete
polynomial vectors. [Exact witness and proof](NONCONCAVITY.md).

The earlier A14 cone already provided a -1/1260 addition defect on three
positive whole vectors, accepted in the Pro031 final verification. A21 adds
the strict-interior and generic-adjacency witness and its wall formula; no
worldwide novelty claim or external human review is asserted.

There is also a useful positive boundary: for feasible parents whose two-row
inner partition occupies the **same slot**, c1 is superadditive and monotone
under their addition at every ambient rank. Changing overlap interfaces is
part of the proof. [Restricted addition and sharp gain](TWO-ROW-ADDITION.md).
A fixed tensor symmetry may be applied to all parents together; independently
changing slots or symmetries does not preserve this theorem's hypotheses.

From the complete repository, the proposed fresh replay is:

```sh
python3 -B results/linear-coefficient-geometry/reproduce.py --scratch /your/scratch
```

It needs Python's standard library, a C++17 compiler and GMP. Set CPPFLAGS and
LDFLAGS if GMP is not in compiler search paths. It regenerates both 1,296-tree
systems, checks all six complete first jets/gradients and the exact original
rows/cuts, then checks the distinct 3+3 wall factors and two original-row duals.
The two costs use the same formula. The wall proof supplies the structurally
different check. Separate literal tableau controls exercise the restricted
addition map; they are not its all-rank proof.

Historical arithmetic suggests tens of seconds on the original host, including
compilation. The staged edition has passed a fresh replay; publication review remains required. It executes no provider program and includes no discovery LP.

[All results](../../RESULTS.md) · [Main page](../../README.md) · [Tools](../../tooling/README.md)
