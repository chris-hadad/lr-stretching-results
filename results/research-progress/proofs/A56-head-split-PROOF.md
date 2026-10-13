# A56: complete closed width fan and the sharp first coefficient

Accepted scope: every old-width list with at most five positive entries, including zero layers and closed-cone boundaries. The [complete A55 parent bridge](A55-head-split-PROOF.md) is a mathematical premise. The proof below retains the full fan and exact first-coefficient reduction; ray signs do not prove higher-coefficient signs throughout cones.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

26 September 2026. Root derivation. The full original-parent construction and saturated K3 flow model are accepted A55 premises, originating in Pro044's complete layered family. The new contribution is the common width fan, a closed-cone linearity reduction, and its exhaustive exact first-coefficient certificate through five old widths. It is not an all-coefficient initial-split theorem or unrestricted KTT.

## 1. Statement with every original parent

Let w=(w_1,...,w_N) be any nonnegative integer list, N<=5, and W=sum w. Delete zero entries when determining actual degree. If W=0 both parents are points and their difference is zero. If W>0, put


```text
before = (w,2W),  after = (w,W,W),
P_l(t) = sum_s f_(l,t)(s)^3,
f_(l,t)(s) = [z^s] product_i sum_(r=-t l_i)^(t l_i) z^r,
G_w(t) = P_after(t)-P_before(t).
```

These are ENTIRE ordinary LR polynomials. For either list l, let T=sum l (=3W), h=(T,l), and o_j=4 sum_(q>j)h_q. Its original triple is


```text
Lambda=(o_j+4h_j,o_j+2h_j)_j,
Mu=(o_j,o_j)_j,  Nu=(6T,4T,2T).
```

Zero layers may be removed; no positive layer, boundary row or flow is omitted. The A55 character proof establishes the complete LR identity, not a hive-metric identification. All parts are nonnegative partitions, Mu is contained in Lambda, and the size difference is 6 sum h=12T=|Nu|. Both stretch homothetically with their literal integer lattice.

The new theorem is


```text
[t] G_w(t) >= (12/7) W.                         (1)
```

It holds for every width and every tie, not only bounded widths. It is strict for W>0. The constant 12/7 is sharp on the closed nonnegative domain because a single nonzero old width has equality. With m positive old widths, actual degrees are 3m+1 before and 3m+4 after; G has the latter degree and zero constant. The whole higher coefficients remain unproved for arbitrary width lists of length four or five. Positive higher coefficients at the determining fan rays do not extend by linearity.

## 2. A complete common fan from all original graph cuts

Orient the three edges of K3 cyclically and put one copy of each edge for every layer. Write x_e for its integer flow in [-l_i,l_i]. Delete one incidence equation. The full flow polytope is


```text
Q_l = {x: Bx=0, -l_i <= x_e <= l_i for every copy e of layer i}.
```

The incidence matrix B is totally unimodular of rank two. Choosing a spanning tree and solving its two edges gives integer affine coordinates for the entire kernel lattice. Box vertices of Q_l are integral: at a vertex the non-bound edges form a forest, which extends to a spanning tree; all other edges are at integer bounds, and the two tree equations are unimodular. This also covers degenerate vertices represented by more than one tree. Zero flow is strict for all positive layers, giving dimension 3L-2. Zero layers are exactly fixed edges, and their deletion preserves the saturated lattice and count.

Fix a spanning tree and signs for all non-tree bounds. Its two solved edges are linear in l. A feasibility wall occurs when one solved edge reaches either bound. Removing that tree edge gives a fundamental cut separating one K3 vertex from the other two. The other tree edge is internal to one side, so every crossing edge is now at a bound. For EACH layer precisely two edges cross this cut; their signed contribution is in {-2l_i,0,2l_i}. Dividing by two, every possible nontrivial wall has the form


```text
sum_i epsilon_i l_i = 0,  epsilon_i in {-1,0,1}.   (2)
```

This accounts for every tree, every bound sign, both solved edges and all degeneracies. No selected normal/star or favorable flow sector replaces the original polytope.

For the before list (w,2W), (2) is sum epsilon_i w_i + 2 eta W=0. In the strictly positive old orthant, eta!=0 cannot vanish; only old subset-sum walls survive. For the after list (w,W,W), it is sum epsilon_i w_i + kW=0 with k in {-2,-1,0,1,2}. Values |k|=2 cannot vanish. A k=1 wall can vanish in the positive orthant only when every old epsilon_i=-1, in which case it is identically zero; the k=-1 case is the reverse. Those permanent degeneracies impose no further subdivision. Every remaining wall is


```text
H_epsilon: sum_i epsilon_i w_i=0,
epsilon in {-1,0,1}^N, with both signs present.    (3)
```

Include coordinate hyperplanes to obtain a complete closed fan on w>=0. Its zero-coordinate faces contain any formerly impossible or identical cut degeneracies. This fan refines the simultaneous feasibility/type chambers of both COMPLETE parent polytopes.

## 3. Why c1 is linear on each CLOSED cone

Let C be one full-dimensional cone of this fan. Every tree-bound basis has constant feasibility in its interior. For any linear objective in the full ambient flow space, choose a dual-optimal feasible basis at one interior parameter. Its reduced-cost optimality depends only on the fixed constraint matrix and objective, while feasibility persists on C. Thus its optimal value is a linear function of w throughout C. Continuity extends that same support-function formula to the closure. It follows for w,v in the closed cone and nonnegative scalars that


```text
Q_(w+v) = Q_w + Q_v,  Q_(a w)=a Q_w,             (4)
```

separately for both parent constructions in their respective fixed ambient lattices. Point and dimension-drop limits are included. This is a statement about the full flow polytopes, not about an original hive metric.

The lattice Minkowski/Ehrhart polynomial theorem says that, for lattice polytopes P_1,...,P_k in a fixed lattice, the count of n_1 P_1+...+n_k P_k is a polynomial in nonnegative integral n_i. Its total degree-one part is sum_i c1(P_i)n_i: set all but one n_i to zero to identify these coefficients. Consequently c1(P+Q)=c1(P)+c1(Q), including lower-dimensional summands in their induced saturated lattices. This is the standard mixed-Ehrhart premise also used in the accepted A006 closed-chamber continuation; no sign property of higher mixed coefficients is assumed.

Apply this fact and (4). The functions c1(P_after), c1(P_before), and their difference are linear in w on each closed cone. Every pointed cone is generated by its extremal rays. Rational ray combinations can be cleared to integers, and c1 scales linearly, so verifying (1) on primitive integral rays verifies (1) on every integral w in the cone. Covering all cones covers all widths and boundary faces.

## 4. Exhaustive ray domain and finite certificate

For dimension N, generate every distinct hyperplane normal with entries in {-1,0,1}, both signs present, first nonzero entry positive; then add the N coordinate normals. Any one-dimensional fan cone is the common nullspace of N-1 independent normals from this COMPLETE roster. Conversely every such nonnegative null vector is a fan ray. Thus exhaustive intersections enumerate all rays without enumerating all chambers.

For N=4 there are 29 normals and 3,654 triples. For N=5 there are 95 normals and 3,183,545 quadruples. The exact cofactor enumerator rejects rank-deficient intersections and mixed-sign null vectors, divides by the gcd, and only then quotients by permutation of old widths. It yields 12 and 125 primitive ray orbits respectively. The N=5 boundary ray set contains the entire N=4 set padded by zero; lower dimensions are included likewise. Every orbit stands for the full permutation orbit, since both parent counts and (1) are symmetric in the old widths.

For each ray with m positive old coordinates, degree D=3m+4 is known BEFORE interpolation. Compute both full parents at grades 0..D and reconstruct with exact rational Newton differences. Grades D+1,D+2 are unused positive checks for EACH parent. Verify the before degree is exactly 3m+1, the after degree D, both constants one, and the gain constant zero. All 125 N=5 ray ratios c1(G)/W are at least 12/7; equality is attained at (0,0,0,0,1). [RAYS5.json](../data/a56/RAYS5.json) and [RAY5-POLYNOMIALS.json](../data/a56/RAY5-POLYNOMIALS.json) contain the full determining domain, literal original triples and every value/coefficient.

The exhaustive portable [ray enumerator](../code/a55_a56/enumerate_width_rays.cpp) and [complete polynomial checker](../code/a55_a56/check_initial_split.py) replay every ray and full vector. Historical independent original-LR controls and their timeouts remain in [VERIFICATION.json](../data/a56/VERIFICATION.json); this export does not rerun the LR backend.

## 5. Reach, limitations and next mathematical test

This pays a whole first coefficient of the complete sharp initial difference with arbitrary old widths through five positive entries, despite A55's negative fourth-range moment. It does not separately sign those moments. It does not establish an entire ordinary-negative LR polynomial, an all-coefficient initial-split theorem, whole rank seven or unrestricted KTT. The original rank after is 2m+6 (at most sixteen here), before 2m+4; the full gap is between those particular literal parents.

The same complete fan and first-coefficient linearity hold at arbitrary N. The sign certificate here is exhaustive only through five positive old widths. The all-N inequality remains open, and higher coefficients need their full mixed forms.
