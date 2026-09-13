# Repairing the remaining sign uncertainty by a formal interior upper cover

Assume all the complete sextic/lattice/normal premises and the five numerical
counts in FIVE-COUNT-SEXTIC-ENCLOSURE.md. That screen can fail even when the
whole polynomial is positive; its failures remain negative lower bounds only.
The four pilot failures concern c1, not c2 or c3. No true I3 count or full vector
was available to this repair when its proofs were generated.

Write K=10-5A+B-10U+5V and W0=K-120h. The same exact coefficient algebra gives

    I(3)=W0+720c6,
    60c1=60a+120h+K-I(3).

Therefore any proved upper bound I(3)<=B3 supplies

    c6 <= (B3-W0)/720,
    c1 >= (60a+120h+K-B3)/60.

The upper bound need not be sharp and is not set equal to I(3). A requested
integer threshold strictly below T=60a+120h+K is chosen from the five counts;
ceil(T)-1 is sufficient for a positive c1 bound. Tighten the previous c6
interval with this extra inequality and retain all previous c2/c3 bounds.

## Complete fixed-grade covering proof

The entire true third interior in its complete saturated chart is the integer
system 3c_r+a_r.z>=1 for every nonconstant defining row; constant rows keep their
unshifted boundary condition. Begin with no assumed coordinate bounds. The
proof producer derives finite integral coordinate bounds from the full rows:
maximizing the other terms over previously derived bounds gives a necessary
one-coordinate inequality, rounded inward to its exact integer endpoint.
Each deduction names the original row, coordinate, endpoint and direction.
A contradiction leaf has cardinality zero. Otherwise every admissible point
lies in the finite displayed integer box, whose product of side cardinalities
is a valid upper bound, whether or not all box points satisfy the full rows.

When the current sum of box cardinalities is too large, partition one box at an
integer midpoint in a selected coordinate into two disjoint exhaustive boxes.
Apply the same sound propagation in both. Every split retains both children;
no difficult branch may be omitted. The final sum of leaf cardinalities bounds
all interior points. Stop once that sum meets the threshold, or retain a valid
but insufficient complete upper cover if the finite node/time budget expires.
The algorithm does not enumerate a complete feasible-point count or provide a
new determining scalar. A cover can happen to be exact (including zero), but
no equality is inferred from the upper-bound label.

The independent checker does not invoke search or counting. It proves a proposed
lower endpoint v by a(v-1)+S<0<=av+S, and an upper endpoint by a(v+1)+S<0<=av+S.
It replays every deduction, checks each contradiction, derives each leaf's
integer box cardinality, verifies each two-child exhaustive partition, rejects
extra/unreachable nodes, and recomputes the aggregate. Whole geometry and the
strict-system hash bind this proof to the actual LR interior, not an auxiliary
section. The full integer row--hive map transports the same bound to the complete
row fiber. This is a shared formal geometric premise, not a claim of two newly
computed I3 values. The five numerical premises still have two complete counting
models with every raw request and response independently bound to that geometry.

## Scope and inconclusive cases

This is a direct complete sign proof from incomplete numerical information,
not a relabelled six-site reconstruction. In particular, the first four repaired
pilot bounds were I3<=4,8,3,4, obtained from single boxes, and none was assumed
an equality. A full-vector baseline separately counts I3 and checks the original fixed unused
positive sites 4,5; its cost and any refusal remain distinct evidence.

A valid insufficient upper cover does not imply a negative coefficient. A
strictly negative upper bound on an ordinary coefficient after interval
refinement would establish a negative ordinary coefficient of the entire LR polynomial under the stated premises.
The finite upper-cover proof rules are valid for arbitrary integral fixed-grade
systems when finite boxes are actually derived; LR polynomiality, parity,
complete normal/lattice hypotheses and the all-coefficient bridge are additional
requirements of their present use, not automatic properties of an H-system.

## Final clarification about zero bounds and determining information

There are 573 certified zero upper bounds in the production population. Because
I3 is nonnegative, those formal complete contradictions do prove I3=0 and pin
the leading coefficient. They are not merely approximate counts, and their exact
information is not concealed. The other positive upper bounds are never assumed
tight. The phrase 'no new determining scalar' above describes the absence of a
sixth numerical point-counting call, not an absence of mathematical information
from an exact empty-interior proof. All 573 point intervals and the other 153,835
nontrivial intervals are recorded. The production certificate is a direct sign
proof and does not report full vectors for the 154,408 targets. The final simpler
integer-linear form is THIRD-INTERIOR-SEXTIC-CERTIFICATE.md; all 6,157 formal
covers are independently replayed again in that final assay.
