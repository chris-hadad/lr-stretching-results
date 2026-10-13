# A57: global controls, complete graph coordinates, and positive component limits

Curated mathematical proof from **A57**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

26 September 2026. Root derivations for the originating reconstruction,
using the unchanged independently accepted A55 original-character bridge and
A56 complete closed width fan.
Pro045 and Fable origins are credited separately below. No novelty priority
or general KTT proof is asserted.

## 1. An exact obstruction to old-width refinement

For a nonnegative integer list w, delete its zeros and put W=sum(w). For a
layer list l define the COMPLETE count


```text
f_(l,t)(s) = [z^s] product_i (1+z+...+z^(2 t l_i)),
P_l(t) = sum_s f_(l,t)(s)^3,
G_w(t) = P_(w,W,W)(t) - P_(w,2W)(t),
g(w) = [t] G_w(t).
```

Centering each interval changes its index, not this sum. Both P's are entire
ordinary stretched LR polynomials. The exact original map is A55's map:
T=sum(l), h=(T,l), o_j=4 sum_(q>j) h_q,


```text
Lambda=(o_j+4h_j,o_j+2h_j)_j,
Mu=(o_j,o_j)_j, Nu=(6T,4T,2T).
```

It retains every row, the full character, the saturated integer flow lattice
and the once-only Weyl shifts. For L positive layers, the actual degree is
3L-2; the all-zero case is a point. This is a count identity, not a transfer
of the Euclidean hive metric.

Direct exact complete counts give


```text
g(1,2)=26/5,
g(1,1,1)=5204/1001,
g(1,1,1)-g(1,2)=-6/5005.
```

Thus subdividing an old width 2 into 1+1 need NOT increase even the first
coefficient of the complete initial-split gain. This refutes induction by
unqualified positive old-width refinement. The expression is a difference
of two complete gains, hence a signed combination of four complete original
parents. It is not an ordinary LR polynomial and is not a candidate.

The determining degree is fixed before reconstruction. Root code
global_controls_v1.py counts complete interval convolutions, reconstructs
with exact Newton differences, and extracts c1 independently by the identity


```text
c1 = sum_(j=1)^D (-1)^(j-1) binom(D,j)(P(j)-P(0))/j.
```

Separate bounded-composition inclusion-exclusion computes the entire sum at
0,1,2,D,D+1,D+2. D+1 and D+2 are unused positive-grade checks. Twelve complete
parent controls for six explicitly listed old lists retain every coefficient,
value, degree and literal original triple in GLOBAL-CONTROLS.json. Every
whole parent is positive. This is a decisive mechanism test, not new census
coverage and not an extension of A56's all-width theorem.

## 2. Global Jensen shortcuts fail in both directions

A56 makes g homogeneous and linear on each closed cone of the full subset-sum
fan, including zero-width faces. It does not make g globally concave or convex.
By permutation symmetry, the midpoint of x=(2,1,0) and y=(0,1,2) is (1,1,1),
and g(x)=g(y)=26/5. The preceding negative defect disproves concavity on the
closed nonnegative width cone. Hence one cannot obtain the all-width lower
bound by a global concavity argument from concentrated-width extremals.

Conversely, x=(2,0,0), y=(0,2,0) have midpoint (1,1,0). Exact counts give


```text
g(1,1)-g(2)=122/35-24/7=2/35>0,
```

which disproves global convexity. The comparisons retain a fixed ambient
old-width space with legitimate zero layers and actual degree drops. These
failures do not refute g(w)>=12W/7, which remains proved through five positive
old widths and open for arbitrary list length. They also do not retire a
signed-spline identity, a grouped moment inequality or a corrected refinement
with an explicitly paid defect.

## 3. Complete weighted-theta coordinates for the layered family

There is a direct lattice-coordinate description that can support those
surviving architectures. Take three paths of length L sharing their start
and end vertices. Fix the start potential to zero; let the end potential be
s and the internal path potentials be y_(a,i), a=1,2,3 and 1<=i<L. Require


```text
-l_i <= y_(a,i)-y_(a,i-1) <= l_i,
y_(a,0)=0, y_(a,L)=s.
```

There are 3L-2 free potentials. Taking differences sends them to three
integer edge lists with the same total. Taking prefix sums is its inverse.
Both maps have integral coefficients and are bijective on the complete
saturated lattices. Therefore the full polytope is integrally equivalent to
A55's three-parallel-edge flow model, with exactly the count P_l(t). All
constraints are retained difference bounds; zero widths contract forced
edges. Positive widths give an open neighborhood of zero and actual dimension
3L-2. For L=1 the three paths describe the same single interval, as required.

This is a weighted graph Lipschitz polytope with a theta graph. Unit widths
give the polar of that graph's symmetric edge polytope in the anchored lattice.
It is not the same object as an arbitrary marked-order polytope or a general
LR hive. The relation is established by the explicit inverse maps above;
it needs no hypothesis about hive-metric equivalence.

The existing corpus already proposed planar-dual/marked-order interpretations
in Pro044's idea record; this derivation makes one complete count/lattice map
explicit, without claiming a new external theorem. The primary literature
check of Kounoike's 2024/2025 paper, *A new class of magic positive Ehrhart
polynomials of reflexive polytopes*, establishes selected graph classes and
partial cycle results, and includes failures of a stronger magic-positivity
proposal. It does not provide a weighted-theta subdivision theorem. A positive
h-star vector or alcove triangulation would still not sign ordinary
coefficients or the difference G. The next graph test must control the full
three-path operator and its strict endpoints, not replace them by separate
positive path factors.

Source: https://arxiv.org/abs/2409.16648 and the checked proceedings text
https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2025/148.pdf .

## 4. A positive simplex skeleton in every codimension

Let r_0,...,r_d be primitive dual-lattice vectors, d>=1, satisfying
sum r_i=0, with any d of them an integer basis. For 0<=p<=d consider ALL
p-element subsets, with the original induced metric on each cone. Under
the accepted BV local Euler--Maclaurin identity,


```text
S_(d,p)=sum_(|I|=p) alpha(pos(r_i:i in I))
       =(d-p)! [t^(d-p)] binom(t+d,d) > 0.
```

Proof: choose r_1,...,r_d as lattice coordinates. The inequalities r_i(x)>=0
for i>=1 and r_0(x)>=-1 define a unimodular d-simplex. Its codimension-p
normal cones are EXACTLY the listed subsets, and every corresponding face
has lattice volume 1/(d-p)!. The full local formula and the complete simplex
Ehrhart polynomial give the equality. Its positivity follows from the product
binom(t+d,d)=product_(j=1)^d(1+t/j). The metric may be arbitrary positive
definite: the complete coefficient and equal face volumes are metric
independent even when individual local weights vary or are negative.

In particular S_(d,2)=(d+1)(3d+2)/24. This independently explains the positive
circuit-pair sum in Pro045 U11; it extends the algebraic building block to
every p. GLOBAL-CONTROLS.json checks the complete elementary coefficients
for d=1,...,12 as arithmetic controls, while the preceding proof carries
the infinite quantifier.

This theorem concerns the COMPLETE skeleton of a specified unimodular
simplex fan. It supplies neither original-hive realization nor coverage of
actual normal cycles. Any proposed suspension, subdivision or transfer must
retain its lattice indices, inherited quotient metric, physical rows and
joint original-parent realization. Those obligations cannot be inferred from
the positive formula. The first higher-skeleton original-row test is recorded
separately in component-check; its exact result governs what can be promoted.

## 5. Pro045's independently checked component and residual

The finalized Pro045 U11 construction supplies a concrete stronger original
bridge for p=2, with n>=7 and the complete physical grammar C_n. Its source
proof gives 4(n^2-7n+14) five-supports, a signed restricted balance kernel
equal to the line generated by their unit vector v_n, and pairing


```text
alpha dot v_n=(n-3)(3n-10)/24>0.
```

Unlike a formal local scalar or flat fan alone, its simultaneous collar
constructs ONE legal integral full-dimensional original parent containing
every support in one compatible positive refinement. It includes every
physical rhombus, all extra zero rows, a saturated integer image, the inherited
metric, exact perturbation and a full-dimensional boundary neighborhood.
The source's unchanged-support rank-raising failure remains valid; C_n changes
its support at the new endpoint.

Root checked the all-rank grammar, quotient-circuit, rank-changing collar and
restricted-kernel arguments. The independently authored checker regenerates
the domain through signed suspension and stellar subdivision, verifies all
original and shifted rows, actual degrees and primitive images, recomputes
the restricted balance kernel and inherited pair values at n=7,...,10, and
rejects the named invalid controls. Returned provider code is never imported
or run. The exact finite receipt and all failed checker attempts are in
component-check. Adoption is limited to the theorem supported by that proof
and the A57 independent review; it never promotes unrelated Pro045 claims.

For any actual complete cycle w on the same primitive balance system, extend
it by zero on absent cells and set lambda=min_(I in C_n) w_I. Then


```text
w=lambda v_n+r, r>=0, B^T r=0,
alpha dot w=lambda (n-3)(3n-10)/24 + alpha dot r.
```

The restricted kernel proves maximality of this extraction; it also makes
v_n an extreme ray of the formal nonnegative balanced cone. This is the
elementary U12 deduction, independently rederived: in a nonnegative
decomposition of v_n both summands vanish outside its support and hence lie
on its one-dimensional kernel. Maximal subtraction zeros a selected
coordinate, so repeating the same component cannot progress.

The residual is unsigned and need not be an LR-parent cycle. A positive
extracted term is therefore NOT a lower bound on the whole coefficient.
Finite positive-component peeling terminates after at most the number of
positive support coordinates, but termination alone proves neither coverage
nor positivity. This exact limitation is the central frontier obligation.

## 6. Evidence-driven direction

The old-width monotonicity and global Jensen shortcuts are now refuted on
complete original controls. The weighted-theta model and complete signed
moment/spline route survive without a global inequality. The simplex formula
gives a uniform positive algebraic component; Pro045 supplies a nontrivial
original realization at one codimension. Neither supplies the residual
coverage theorem needed for general KTT.

Fable W adds unadopted source downward field compatibility, chart-local correction
certificates and specific rank-seven/rank-eight obstructions. Its source
claims and replay limitations remain separate. In particular A55's LR count
bridge does not identify the original hive metric with a flow metric, so
one cannot directly substitute its coefficient objects into a native
normal-cycle field. A valid comparison must construct that missing map.

A uniform complete-cycle certificate or a complete parent-generation theorem
remains a mathematical question for the unsigned residual. A negative result
would require an actual original parent with a negative full residual pairing
or complete ordinary coefficient, beyond the proved classes. A negative formal
balanced ray, local alpha, affine gain, face or order polynomial remains an
obstruction or lead, never a KTT counterexample.

## 7. New rank-seven codimension-six original component

The p=3 extension at n=7 uses R={v,w,C24,C34}, the complete three-subset
skeleton, all three physical signed lineality pairs, and the same stellar
subdivision along u=v+w-a. The 32 initial cones become 48: eight cones
containing the subdivided face are replaced by three each. The full signed
kernel is one-dimensional, with all unit primitive quotient factors.

The first fixed-boundary test fails exactly. On U11's boundary, the original
row identity for seed {A00,A01,A02,A03,A11,C24} is


```text
B24-A00-A01-A02-A03-C24
  =h25-h16+h00-h10-h04+h05=-432.
```

This makes that cell impossible there. Root independently expanded all six
rows and checked the boundary substitution. It is not a universal obstruction.
Six fixed-boundary rational Farkas certificates, 41 exact witnesses and one
initial unresolved cell remain in the finite record.

Allowing a NEW common boundary succeeds. The complete original system has 755
variables, 2799 inequalities and 288 selected equations. A numerical proposal
is rounded after scaling, then every selected equation is repaired with a
unit-minor integer inverse. Exact rational verification of every original
row, boundary, saturated image and strict parent is the evidence, not the
optimizer status. The resulting legal integral parent has trace 439000004,
actual degree 15 and all 48 codimension-six faces, each of dimension 9.

A separate certificate-only checker verifies the complete roster and heights.
All 144 original five-cofacets balance and 252 nonzero quotient equations have
rank 47. One common delta has a_u=2, other base entries 1 and lexicographic
M=262145 tails, with eta=1/(48*15*2^30). Every selected shifted row is exactly
zero; all 2736 offseed shifted rows, including 16 previously tight in-span
extras, and all 63 shifted parent rows are positive. The Hadamard circuit
bound B=2^15 and the displayed amplitude give genericity and compatibility
by the same explicit finite-basis argument as U11. Complete arrays and
checks are in component-check/certificates, not inferred from labels.

The dual-solid valuation identity from Pro045 U04 section 2 uses BOTH
lineality signs in a fixed span, then restricts to ker(r) with its INHERITED
metric; it is not ordinary lower-dimensional intersection additivity with
the old metric. Applying it three times and undoing unimodular stellar
subdivision reduces the ENTIRE pairing to the complete simplex p=3 fan.
Section 4 gives S_(3,3)=1, so this original 48-cell component has positive
pairing 1. The same support/kernel argument as U12 makes its maximal
subtraction the minimum actual selected-face weight, leaving a nonnegative
balanced but unsigned residual. No c9 or whole-parent positivity follows.

This proves a new bounded original realization of the uniform algebraic
block, beyond Pro045's p=2 component. It does not prove all-rank p=3
realization or full cycle coverage. The failed fixed boundary remains a
useful constraint; the exact new boundary shows why changing the complete
parent is a substantive mathematical option.

## Complete component and parent certificates

The [full all-rank component construction](A57-U11-COMPONENT-PROOF.md),
[complete two-sided valuation](A57-TWO-SIDED-VALUATION.md) and
[literal rank-seven parent realization](A57-P3-REALIZATION.md) supply the complete
premises of Sections 5 and 7. The [data and checking guide](../A55-A57-REPRODUCIBILITY.md)
includes every component, face height and shared shift certificate. The residual
outside the signed component remains unsigned; this does not sign the whole
rank-seven polynomial or a whole coefficient layer.
