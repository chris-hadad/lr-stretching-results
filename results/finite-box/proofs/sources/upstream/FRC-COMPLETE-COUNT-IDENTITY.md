# Exact positive-R two-support experiment

This note proves the certificates used by `attempt-001`. Its scope is exactly
two nonempty supports covering n=5 or 6 cuts, positive integral R, direct outer
size at most 30, and the explicit dominance inequalities below. This finite
experiment does not cover zero-coordinate directions, three or more factors,
higher ranks, or larger sizes. Parameter enumeration is separate from ordinary
coefficient coverage. Independent review of the complete certificate remains a separate requirement.

## Complete finite grammar and direct ordinary LR identity

For each cut choose S1-only, S2-only, or both. Exclude the two assignments
making a support empty, then quotient support exchange. Only the all-both
assignment is fixed by exchange, giving (3^N-1)/2=121/364 pairs. The producer
uses increasing positive bit masks with bitwise union all cuts, an equivalent
complete enumeration; no support pairs are sampled. It verifies both adopted
interval-hit inverses against the coverage F for every support pair.

Write F_ij for the number of supports meeting [i,j] and m_ij=F_ij-1. Here
m is binary and nonnegative. The recursion enumerates every positive integer
R with sum_i i F_ii R_i<=30 exactly once. The planning bound replaces each
F_ii by 1: R=1+u leaves weighted budgets15/9, yielding408/90 possible vectors
per support pair and the stated total upper bound 82,128. The actual smaller
size-bounded domain has 19,013 tuples, including 9,929/3,208 dominance rejects
at n5/6. A separate checker rebuilds the grammar by ternary assignments and
the unweighted u recursion, then filters the actual weighted size.

Pad R0=R_(n+1)=0. For each support a put eta^a_i=sum_{j in S_a,j>=i}R_j and
theta_i=eta1_i+eta2_i+R_(i-1)-R_i. Consecutive differences of theta equal
(m_ii-1)R_i+R_(i-1)+R_(i+1), so the exact retained inequalities make theta a
partition. Its last part is R_n>0, giving ordinary rank exactly n+1. Both
inner partitions are nonempty. Telescoping gives

    |theta| = |eta1|+|eta2| = sum_i i F_ii R_i <=30.

The adopted `source/NONNEGATIVE-M-LEMMA.md` then supplies the complete-count
identity, for all integers t>=0,

    c^(t theta)_(t eta1,t eta2) = #{x>=0 integral : A_m x=tR}.

This uses dominance and nonnegative m, and says nothing by itself about
feasibility. A dominant compiled triple can have an inner partition not
contained in theta; such a case must reach the infeasibility check rather
than be discarded as a producer error. In feasible cases, direct inner
containment is independently checked as a necessary identity consequence.

## Exact flow feasibility, including infeasible cut certificates

Replace the interval column [i,j] by the directed edge i->j+1 on vertices
0,...,n, using zero-based cuts. Applying successive differences to A_m x=R
gives outgoing-minus-incoming incidence b=(R1,R2-R1,...,Rn-R_(N-1),-Rn).
The graph is acyclic. Set M=sum_v max(b_v,0). Add source arcs of capacity b_v
where b_v>0 and sink arcs of capacity -b_v where b_v<0; give every original
edge capacity M. Any feasible nonnegative flow decomposes into paths from
positive to negative supply, so no original edge can exceed M. These finite
capacities therefore do not alter feasibility.

An exact integer augmenting-path maximum flow either saturates all supply
or returns a source/sink cut of capacity<M. Every infeasible record contains
that cut, total supply, achieved flow and cut capacity. The checker rebuilds
the capacity from the graph and b and verifies the strict inequality. Every
feasible record contains a nonnegative integral original-edge witness whose
interval sums equal R exactly. No dominance inference enters this step.

An infeasible record has zero LR values at every positive stretch: a real
point in any positive dilation would scale to a feasible point at R. At t=0
the formal count identity is 1, so this case is not assigned a nonempty
Ehrhart polynomial. The infeasible positive-stretch zero-polynomial
convention is a separate convention, not a fit through t=0.

## Complete active-edge certificate and exact intrinsic degree

Fix the feasible integer flow x. Form the original graph with every forward
edge present, together with the reversed edges whose x_e>0. Forward arcs
are treated as unbounded here, including when x_e equals the artificial
max-flow cap M; that cap is not a constraint on allowable affine variations.

Every edge with x_e>0 is active. For an edge u->v with x_e=0, it is active
if and only if this residual graph has a path v->u. A recorded path plus
u->v is a residual cycle. Adding an integral unit along its forward arcs
and subtracting one from its reverse arcs preserves b and nonnegativity,
and makes the previously zero edge positive. This supplies a feasible
witness for every declared active edge, not merely a graph heuristic.

If there is no path v->u, let C be the vertices reachable from v. The record
stores C. Then v is in C, u is not, and no residual arc leaves C. In particular
no original forward edge leaves C, and no positive incoming original edge
enters C (its reverse would leave). Hence sum_{w in C}b_w=0 at the recorded
flow. For any feasible flow y, conservation gives zero total incoming flow
across this same cut, so every such edge, including u->v, is forced zero.
The checker verifies closure, sum b=0 and edge separation for every declared
inactive edge. Active and forced-zero sets partition all edges exactly.

Average the finitely many feasible witnesses that make each active edge
positive. The resulting point is positive on all active edges, so there are
no additional affine equations caused by nonnegativity. The affine hull is
A_active x=R and its dimension is E_active-rank(A_active). The difference map
identifies this rank with directed incidence rank, V-c, counting all n+1
vertices and all components including isolated vertices. Each record stores
E_active, components, rank and degree; exact rational Gaussian elimination
on the original interval columns independently checks the graph rank. Thus

    degree = E_active-(n+1)+components.

The interval matrix is totally unimodular: its columns have consecutive ones,
equivalently its difference transform is a directed network matrix. With
integral R every vertex is integral. Nonzero nonnegative interval columns also
bound each variable by some R_i, so the feasible fiber is a bounded integral
polytope. The complete-count identity therefore gives an ordinary Ehrhart
polynomial of precisely the certified intrinsic degree, at every t>=0.

## Canonicalization and proof terminals

Trim trailing zeros, sort the two inner partitions lexicographically, and
divide all three partitions by their common positive gcd. This uses only
inner exchange and common dilation. If a raw triple is g times a primitive
one, P_raw(t)=P_primitive(gt); positive g preserves every ordinary coefficient
sign. All original parameter indices remain attached to their canonical key.
The gcd divides R because the recurrence R_i=R_(i-1)+eta1_i+eta2_i-theta_i
recovers R from the three padded partitions. Consequently the primitive
parameter is itself inside the same positive-R grammar and the same size
bound. Different parameterizations of one key must have the same feasibility
and intrinsic degree; the producer refuses any disagreement.

Every feasible integral polytope of intrinsic dimension 0 has polynomial 1;
in dimension 1 its polynomial is 1+Lt with positive lattice length L; in
dimension 2 Pick's theorem in the saturated relative lattice gives
A t^2+(B/2)t+1 with A,B positive. These fully justified d<=2 cases terminate.

The authenticated adopted rank<=5 source package gives ordinary coefficient
nonnegativity for all such LR triples, including degenerate ones. The Horn
reduction uses the already adopted Ressayre formula (Theorem 5, section 4.1,
equation 16): for increasing equal-size proper subsets I,J,K with
c^tau(K)_(tau(I),tau(J))=1 and

    sum lambda[K] = sum mu[I]+sum nu[J],

The stretched parent polynomial is the product of the selected and complement
LR polynomials. Here tau(I)=(i_r-r,...,i_1-1). The producer enumerates every
subset size 1,..., N-1, retains only exact multiplicity-one index triples,
and independently re-counts those small index tableaux by the separate
row-based portable LR function. It caches only these validated index
certificates. Each accepted parent equality rebuilds both balanced partition
children through the frozen verifier and requires both trimmed ranks<=5.
No dense historical edge DAG is loaded. No claim is made that failure to find
such a terminal proves Horn irreducibility through every possible recursive
representation.

The canonical dataset has 5,861 keys: 1,848 infeasible, 2,439 intrinsic d<=2,
960 with verified rank<=5 Horn children, and 614 residual. Rank<=5 direct
terminals do not arise because positive R forces rank 6/7. The residual is
ordered by decreasing certified degree, increasing primitive outer size,
then the tuple-of-tuples canonical key. The first at most 32 per rank are
selected, with at most 64 overall. The selected-file SHA256 is frozen before
any native result. The full residual remains recorded; unselected rows have
no polynomial claim.

## Numerical verification and its scope

Each selected row first requests a complete Normaliz hive polynomial under a
hard 60-second contained child deadline. A negative ordinary coefficient in a primary calculation is a provisional
result requiring independent whole-polynomial verification. Period 1, dimension equal to the
proved flow degree d, full d+1 coefficient vector, constant 1 and positive
leading coefficient are required before any polynomial can be accepted.

An independent LR/tableau batch uses t=1,...,d+2. With the proved P(0)=1,
sites 0,..., d determine the complete degree-d polynomial; d+1,d+2 are unused
holdouts. Exact interpolation and all holdouts must match every Normaliz
coefficient. Failed batches remain explicitly incomplete. The two models are LR tableaux and hives; the independent
complete-count proof bridges the interval-flow degree to this bare triple.

The selected row order and computational limits were fixed before evaluation.
Rows with timeouts or incomplete calculations remain unresolved; no cheaper
replacement row is substituted. A failed holdout, source mismatch or invalid
output cannot supply a complete certificate. Exact requests, responses,
exit status and elapsed time are retained with the calculation.
