# Nonconcavity and failure of superadditivity at rank six

Let the two inner partitions be fixed:

    mu = (91132,69492,52652,43668,21536,4128),
    nu = (73980,61072,51900,34532,13248,4692).

Take three outer partitions, in the indicated order:

    lambda_minus = (139471,121736,100368,70036,60832,29589),
    lambda_mid   = (139472,121736,100368,70036,60832,29588),
    lambda_plus  = (139473,121736,100368,70036,60832,29587).

All triples are legal and balanced, and the middle boundary is exactly the
average of the endpoints. Their common internal hive witness, in the original
A19/A20 ten-coordinate order, is

    (217800,274428,322344,348480,322344,
     374616,405108,418176,453024,483516).

Every one of the 45 original rhombus slacks and 18 legal partition slacks is
strictly positive at every point. Thus these are full-dimensional whole rank-six
hives; no face, auxiliary polytope or inconsistent model substitutes for them.
The full 7,591-cut check shows that the endpoints are generic and adjacent,
and only the following cut vanishes at the midpoint:

    U=I={1,2,3}, J={1,2,5},
    Phi=mu_1+mu_2+mu_3+nu_1+nu_2+nu_5
          -lambda_1-lambda_2-lambda_3.

Its values are +1,0,-1 at the displayed minus, middle and plus points. The
point labels follow the coordinate perturbation, not the sign of Phi.

## Exact complete first coefficients

Both accepted generic ray systems, with every original Weyl pair and rho
offset, independently agree on

    c1_minus = 3891613/63,
    c1_mid   = 38915803/630,
    c1_plus  = 22237417/360.

Consequently

    (c1_minus+c1_plus)/2-c1_mid = 1/336 > 0.            (1)

A concave function would require the opposite weak inequality. Hence the
actual continuous homogeneous rank-six c1 function is not concave, even on
the interior feasible boundary cone. Homogeneity also disproves superadditivity
on that cone:

    c1(b_minus+b_plus)-c1(b_minus)-c1(b_plus) = -1/168.

All three first coefficients are positive. This is not a counterexample to
ordinary coefficient positivity, and the independent candidate protocol is
not triggered. Padding preserves the same count and gives the corresponding
nonconcavity obstruction in rank-at-most-n cones for n >= 6.

The complete 3+3 wall identity provides a structurally distinct check. Here
h=2 and its two full rank-three chamber extrapolants are -1/3 and 1. Their
actual positive wall interval lengths are 4,012 and 9,204. Thus

    g_(Phi>0)-g_(Phi<0) = (1/168) Phi,

which gives exactly (1). Each factor is evaluated using all 36 A2 Weyl pairs
and separately checked against the literal rank-three hive interval formula.
The negative extrapolant is a polynomial extension at a shifted boundary,
not a negative actual lower-rank LR count.

## What survives the failed concavity route

Both actual generic gradients have exact nonnegative rational representations
in the complete original 45-rhombus/18-partition system, modulo trace:

    (g,0_internal) = sum_j w_j A_j + eta trace,  w_j >= 0.

Independent rational expansion checks all 28 coordinates, including cancellation
of all ten internal coordinates. Thus each of these TWO fixed functionals is
nonnegative on the entire legal real hive cone. The accepted A20 closed-cell
transfer identifies each with actual c1 on its own complete feasible closed
cut cell. Universal c2 through c10 then protects all coefficients on these two
closed domains. They do not form a complete cover.

Global-gradient nonnegativity is therefore distinct from concavity: the two
positive whole-cone gradients exhibit a positive jump. They do not satisfy the
concave supporting-plane condition across this wall. A universal supporting-plane or minimum-of-gradients representation is
therefore impossible on the whole feasible cone.

A useful exact reformulation remains: for a continuous piecewise-linear
homogeneous f on the convex feasible cone K, all generic gradients lie in K's
dual cone if and only if f(b+a) >= f(b) for all a,b in K. In the forward direction,
integrate each fixed gradient along the segment b+t a, using continuity across
its finitely many pieces. The reverse direction uses a generic interior point
of each cell and a sufficiently small positive step in an arbitrary direction
a in K. Boundary values follow by continuity. Applied to c1, this cone-order
monotonicity would imply nonnegativity from c1(0)=0. It is a precise stronger
route, not an established property of all rank-six hives.


## Proof dependencies and verification scope

The [complete first-jet formula](proofs/first-jet.md) retains all 518,400 Weyl
pairs, all 1,296 tree bases, original rho offsets and tied selection. The
[two-cell interpretation](proofs/cells.md) and [closed-boundary transfer](proofs/closed-cells.md)
retain the original lattice. The independent [3+3 wall proof](proofs/wall-3-plus-3.md)
yields the same jump. All source bytes and editorial transformations are mapped.
The earlier A14/Pro031 cone refutation is credited in the module introduction.
