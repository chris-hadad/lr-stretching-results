# Closed-cell transfer in the original lattice

## Fixed whole models have a closed Minkowski subdivision

Consider a fixed complete rational inequality model

    H_b = {x : A x + M b >= 0},

on a rational polyhedral cone of feasible boundary parameters. Every H_b is
nonempty and bounded, the original lattice is fixed, and H_0 = {0}.
This includes the complete LR row-letter family used here. Every invertible
ambient row basis I gives a candidate vertex v_I(b), linear in b. Its entire
feasibility condition consists of finitely many homogeneous linear slack
inequalities in b. Subdivide the parameter cone by all those signs.

On an open cell the feasible basis list is constant. On its closure every
basis from that list is still feasible. These vertices also exhaust every
boundary fiber. To see this at b0 in the closure, choose b1 in the relative
interior of the cell and use b0+epsilon*b1. Every point of H_b0 plus epsilon
times any fixed point of H_b1 lies in that fiber. Conversely each feasible
basis vertex has a finite linear limit as epsilon tends to zero. Its convex
hull therefore limits to exactly H_b0, so no additional boundary point is lost.

For a fixed linear objective choose a feasible basis whose normal cone contains
that objective. Such a basis exists by linear programming at an interior
parameter. Its normal cone uses only A, so it remains optimal at every point
of the closed cell. The support function is consequently linear in the
boundary parameters throughout that closed cell. It follows that

    H_(b+b') = H_b + H_b',  H_(s*b) = s*H_b

for b,b' in one closed cell and real s >= 0. This proves actual whole-polytope
Minkowski equality. Point-ray values across different cells do not supply it.

## Homogeneous coefficient functions extend to the whole boundary

Choose finitely many rational generators for one such closed cell and clear
their boundary and vertex denominators by a common positive integer L. The
resulting whole polytopes are lattice polytopes in the fixed original lattice.
Bernstein–McMullen multivariate Ehrhart polynomiality holds for all nonnegative
integer coefficients in their Minkowski sum, including coefficients zero.
Substituting each coefficient as t times a parameter shows that the coefficient
of original t^k is homogeneous of parameter degree k.

For LR fibers, original stretching polynomiality and the exact scaling factor
L^k identify this with the original c_k at every integral boundary. Rational
homogeneous extension is well-defined by clearing a boundary denominator;
the continuous polynomial extension agrees on shared closed cells because
it agrees at every rational point there. Thus on the feasible parameter cone
the ordinary c_k has a continuous, piecewise homogeneous polynomial extension.
This conclusion does not use continuity of Ehrhart coefficients under
arbitrary perturbations or changing lattices/quasipolynomial constituents.

The primary premise is Theorem 2.3 of Haase, Juhnke-Kubitzke, Sanyal and
Theobald, [Mixed Ehrhart polynomials](https://arxiv.org/abs/1509.02254v2). It includes all
nonnegative coefficient tuples and degree in each Minkowski variable.
Rassart's LR polynomiality and the complete original model remain separate
premises. The paper's canonical archived PDF and Astra013 source receipt are
retained; its Theorem 2.3 was checked again during Astra014.

## Applying a sufficient character-wall subdivision

On any open cell where every full original-offset determinant and affine A3
flow branch comparison has constant sign, the accepted complete character
identity makes c_k a homogeneous polynomial of degree k in the boundary
parameters. This cell need not itself be a Minkowski cell. The continuous
extension above nevertheless proves that this same polynomial agrees with
the actual whole LR c_k on its closure. Subdividing further is harmless.
Original-offset wall values remain independent checks; no affine summand is
asserted continuous separately.

For a three-dimensional simplicial parameter cone with linearly independent
integral rays r1,r2,r3, the complete c1 is therefore determined by its three
actual ray values. If all are nonnegative, every point of the closed cone has
c1 >= 0. This uses complete cells and a proved determining space, rather than
an arbitrary positive panel. The origin has c1=0.

For c2 the six actual values at r1,r2,r3 and r1+r2,r1+r3,r2+r3 determine the
whole homogeneous quadratic. In local ray coordinates its diagonal terms are
c2(r_i), and its mixed coefficient for i,j is

    c2(r_i+r_j) - c2(r_i) - c2(r_j).

Nonnegative local monomial coefficients are a sufficient sign certificate;
failure of that sufficient certificate is not a negative LR coefficient.
An indefinite quadratic can remain nonnegative on a cone and would require
a complete copositivity argument or a different positive decomposition.
Unused interior values and independent whole counts remain verification
requirements. Rational local ray coordinates do not change the original
stretch variable or the original polytope lattice.
