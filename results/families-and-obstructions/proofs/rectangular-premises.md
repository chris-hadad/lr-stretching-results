# The primitive p4q5 entire LR family

Derivation dated 10 September 2026. This specializes and checks every varying
premise of the exceptional-pair construction. No historical novelty is claimed.

Let V be three 4-by-5 complex matrices, H = GL4 times GL5 acting by
A -> g A h^(-1), and G = SL4 times SL5. Functions carry inverse pullback.
Put chi(g,h) = det(g)^(-5) det(h)^4 and R = C[V]^G, with R_t the entry-degree
20t component. The entire ordinary LR family is

    lambda = (42^8, 35^4, 18^7, 14^5),
    mu = nu = (28^8, 14^8),
    P(t) = c^(t lambda)_(t mu, t nu).

The final ordinary rank is 24 and outer area 672 = 336 + 336. These are well
outside the original box and the rank-at-most-five positivity theorem.

## Whole LR bridge and nonvanishing

Use precisely the exceptional pair E1 = 2 delta + e, E2 = simple(v) on the
inward star T_(3,3,4) from [the exceptional-pair construction](rectangular-extension.md) and
[rectangular bridge](rectangular-bridge.md).
Its three-arrow embedding is fixed, independent of p. Rigidity is established
there by the two-arrow exceptional (2,3) representation, not merely an Euler
quadratic calculation. The Hom spaces both vanish and Ext(E2,E1) has dimension
three, with Ext(E1,E2) zero. Write I for the embedding on dimension vectors.

On the source three-Kronecker quiver, oriented from vertex 2 to vertex 1,
alpha = (4,5), beta = (7,4), and

    <beta, .> = (-5,4),     <beta, alpha> = 0.

The weighted transportation Weyl extraction retains both complete alternants
and gives dim SI(alpha)_chi = 6798 at grade one in the source count record `FRG-P4Q5-T1-001`. Its exact
definition is a count of the entire invariant component, not a selected LR
summand. The separately frozen bare-triple check has no predicted count input.
The positive count makes the semistable locus nonempty. Powers of a nonzero
semi-invariant prove nonvanishing at each t beta, so the perpendicularity
hypothesis in Derksen-Weyman's embedding theorem holds for every t >= 1.
The original theorem application and sign conventions are in the retained
[rectangular bridge](rectangular-bridge.md), sections 2 and 3. Thus every weight t chi has exactly the same
multiplicity after embedding. At t = 0, acyclicity gives the constants.

The embedded dimensions and character, toward the center, are now:

| Arm | Dimensions | Weights |
| --- | --- | --- |
| Each short arm | 8, 16 | 14, 14 |
| Long arm | 5, 12, 16 | 4, 17, 7 |
| Center | 24 | -42 |

All arm dimensions increase strictly. Rank-failure codimensions are at least
five on the long arm and at least nine on the short arms/central arrows, so
removing those loci loses no regular functions. The partial-flag construction
gives the displayed mu, nu, and

    tau = (28^5, 24^7, 7^4, 0^8).

Each has size 336. Their total 1008 is 24 times 42. Complementing tau inside
the width-42, rank-24 rectangle gives exactly lambda. The central determinant
character cancels the tensor determinant, leaving the entire LR multiplicity.
Scaling the character by t scales all partitions by exactly t. Consequently

    dim R_t = P(t)  for every integer t >= 0.                  (1)

This uses the same fixed exceptional pair and flag multiplicity theorem as
the p2/p3 proofs, with every p-dependent dimension, weight, complement,
codimension and nonvanishing premise checked here.

## Primitive grade and quotient dimension

Every G-invariant polynomial decomposes under H into characters det(g)^a
det(h)^b. The ineffective common scalar requires 4a + 5b = 0, so
(a,b) = (-5t,4t). On g = s I4, an entry-degree-N function has weight s^(-N),
which forces N = 20t. Conversely every invariant in that entry degree has
that weight. Hence R includes all invariant degrees after this regrading;
there is no proper Veronese selection.

The matrices A = [I4 0] and B = [0 I4] have only common scalar endomorphisms.
Indeed XA = AY and XB = BY make overlapping rows of Y equal to [X 0] and
[0 X]. The resulting shift recurrence makes diagonals of X constant and
kills all off-diagonals at the two boundaries. In G the common scalar obeys
c^4 = c^5 = 1, hence c = 1. Adding the third matrix preserves a trivial
stabilizer on a nonempty open set. The affine quotient dimension is

    60 - (15 + 24) = 21.

For this connected semisimple group the invariant rational field is Frac R:
write an invariant rational function as relatively prime polynomials a/b;
unique factorization makes numerator and denominator semi-invariants of the
same character, and G has no nontrivial character. Thus the generic rational
quotient dimension is the Krull dimension. The standard whole LR stretching
polynomial and (1) imply its exact degree is 20 by Hilbert-series pole order.

## Original line bundle, sections and canonical shift

For theta = (-5,4), the only subdimension vectors (a,b) with
0 <= a <= 4, 0 <= b <= 5 and -5a + 4b = 0 are (0,0) and (4,5).
King stability therefore identifies semistable and stable loci for this
weight. Their nonempty common locus U is smooth and irreducible. Stable
representations have exactly the common scalar stabilizer K in H. Thus
H_eff = H/K acts freely and the acyclic stable quotient Q is smooth projective
of dimension 20. It is irreducible as a quotient of the nonempty open U.

The map G -> H_eff is injective. Its image is ker chi: for determinants a,b
with a^(-5)b^4 = 1, c = b/a satisfies c^4 = a and c^5 = b, so removing the
common scalar leaves an element of G. The character is primitive and
surjective, giving 1 -> G -> H_eff -> G_m -> 1.

The line with fiber character chi^(-1) descends to a line bundle L on Q.
With the inverse-pullback function convention, a weight-chi^t polynomial
satisfies f(hx) = chi(h)^(-t) f(x), exactly the equivariance of a section of
L^t. A positive power is the GIT polarization, hence L itself is ample.
There is no multiplication of the original character in this descent.

For completeness the section-ring issue is essential. R is a normal finitely
generated domain: an element of Frac R integral over R lies in the normal
C[V] and is invariant. Its homogeneous vertex in X = Spec R has codimension
21, so normality/S2 gives Gamma(X minus vertex, O) = R. The preimage of the
punctured cone is U, since some positive-degree invariant must be nonzero.
G-orbits on U are closed: they are fibers of chi within stable H_eff-orbits,
and a fixed nonzero invariant prevents closure from leaving U. The residual
G_m action on U/G is free by the exact sequence. Thus X minus vertex -> Q
is the principal G_m bundle for L^(-1), and homogeneous functions identify

    R_t = H^0(Q,L^t)  for every integer t.                     (2)

This is the original line, even without generation in degree one. The same
punctured-cone argument and its detailed references are in the
[canonical argument](rectangular-canonical.md), sections 3 and 4; its dimension condition is stronger
here, not weaker.

The tangent sequence of the smooth principal quotient is

    0 -> Lie(H_eff) -> V -> pi^* T_Q -> 0.

The determinant of the adjoint action on Lie(H_eff) is one. The determinant
of V is det(g)^15 det(h)^(-12) = chi^(-3). Descent therefore gives
det T_Q = L^3 and K_Q = L^(-3), retaining the relative scalar direction in
the effective GL quotient. This also agrees independently with Corollary 5.2
of [Franzen, Reineke and Sabatini, Fano quiver moduli](https://arxiv.org/pdf/2001.10556),
whose hypotheses here are three arrows, coprime dimensions and nonemptiness.
The explicit argument above identifies their index with the original grade.

Kodaira vanishing applies to L^t = K_Q tensor L^(t+3) for every integer
t >= -2. By (2), the Euler polynomial equals P(t) at every t >= 0.
Serre duality in even dimension 20 then gives

    P(-t-3) = P(t),  P(-1) = P(-2) = 0,  P(-3) = P(0) = 1.    (3)

Negative ample powers have no sections; Kodaira supplies the needed higher
vanishing at -1 and -2. Rational-polytope Ehrhart reciprocity in the original
hive's relative integer lattice now gives interior counts 0, 0, 1 at grades
1, 2, 3. Its actual dimension is 20 and its codegree is exactly three.
No assertion that every hive vertex is integral is needed or made.

## Complete determining space

Let y = t(t+3). A polynomial invariant under t -> -t-3 is a polynomial in y.
Equation (3) implies

    P(t) = (t+1)(t+2) Q(t(t+3)),  deg Q = 9.                   (4)

The ten grades t = 0,...,9 have distinct y values and nonzero prefactors,
so they uniquely determine Q. Grades 10 and 11 remain separately unused
positive holdouts. No value at either holdout may enter the fit. A complete second count model or verified all-t argument is required to
establish the entire numerical vector. The
[grouped-Schur model](rectangular-tableau.md) supplies the second count formula;
its documented comparison scope is given in the collection README. Partial
nodes do not settle a missing coefficient sign.
