# Rectangular p=2,3: independent canonical shift and codegree three

This gives the canonical argument for three p-by-(p+1) matrices, p=2,3,
over C. The independently computed nonvanishing values are P_2(1)=20 and
P_3(1)=266, as documented in [the rectangular bridge](rectangular-bridge.md).
No square-matrix canonical formula is used. The degree-based reconstruction
and unused checks remain separate from these geometric conclusions.

## 1. Precise statement

With q=p+1, V=Mat_(p x q)^3, H=GL_p x GL_q, G=SL_p x SL_q, and

    chi(g,h)=det(g)^(-q) det(h)^p,
    R=direct_sum_(t>=0) C[V]_(chi^t)=C[V]^G,

the grade t on R is entry degree pqt. Let Q=Proj R. Then Q is smooth,
irreducible, projective of dimension D=pq, and the original grading
corresponds to an ample line bundle L with

    R_t=H^0(Q,L^t) for every t>=0,
    K_Q=L^(-3).                                                   (1)

Consequently the actual LR polynomial from [the rectangular bridge](rectangular-bridge.md) satisfies

    P_p(-t-3)=P_p(t),
    P_p(-1)=P_p(-2)=0,  P_p(-3)=1.                               (2)

The same whole LR hive polytope has Ehrhart codegree exactly 3: its
relative interior has no lattice points at dilations 1 and 2, and exactly
one at dilation 3. This conclusion is for these constructed whole LR
polytopes, with their original stretch lattice.

## 2. Coprimality removes all strictly semistable points

Use the inverse-pullback convention for the action on functions. The
weight is theta=(-q,p). The quiver stability criterion says that a
semistable representation has theta(a,b)<=0 on every subrepresentation;
it is stable when the inequality is strict on nonzero proper ones.
The numerical equality is

    -qa+pb=0.

Because gcd(p,q)=1, with 0<=a<=p and 0<=b<=q it has only the solutions
(0,0) and (p,q). Thus semistable equals stable for this specific theta.
The assumption R_1!=0 makes this common open locus U nonempty. It is
irreducible because it is open in V. This argument checks the chosen
weight; it does not merely invoke a generic-weight statement.

Stable representations are Schur. Their H stabilizer is exactly the
common scalar subgroup K={(c I_p,c I_q)}. Hence H_eff=H/K acts freely on
U. The quiver has no relations and its representation space is smooth,
so its stable quotient is smooth; the quotient map is an H_eff torsor
in the etale topology. Projectivity follows from the acyclic quiver's
constant H-invariant ring. These are the stable hereditary-quiver
consequences in Proposition 3.1, Proposition 4.3, the paragraph following
it, and Proposition 5.3. [King, pp.521,523-526](https://www.math.uni-bielefeld.de/~sek/sem/stability/king.pdf#page=7)

For King's opposite sign convention on functions, replace theta by its
negative; the equality test and the stable open set above are unchanged
when the linearization convention is changed with it.

## 3. The descended bundle has the original grade

The character chi is trivial on K and so is a character of H_eff.
Moreover the natural map G->H_eff is injective: its kernel consists of
common scalars with c^p=c^q=1, hence c=1. Its image is exactly ker chi.
To check the latter assertion, if a=det(g), b=det(h) and a^(-q)b^p=1,
set c=b/a. Since q=p+1, one has c^p=a and c^q=b. Removing c from both
g and h leaves an element of G. Therefore

    1 -> G -> H_eff --chi--> G_m -> 1                             (3)

is exact. The final character is surjective and primitive.

The trivial line on U with fiber character chi^(-1) descends, since
H_eff acts freely. Call its descent L. A function f of weight chi^t
satisfies f(hx)=chi(h)^(-t) f(x); therefore it defines a section of
L^t. This fixes the sign. Some positive power of L is the ample GIT
polarization, so L itself is ample. No power of chi was inserted in
this descent.

As a sign check only, the same group calculation at dimensions (1,2)
gives three 2-by-2 minors as the stretch-degree-one coordinates. Their
projective quotient is P^2 with L=O(1), agreeing with K=O(-3).

## 4. Why no sections are lost in passing to Proj

Set X=Spec R and let o be its homogeneous vertex. The algebra R is a
finitely generated normal domain. Normality follows directly: an
element of Frac R integral over R is also integral over C[V], hence is
in C[V]; since it is G-invariant it lies in R. Finite generation uses
reductivity in characteristic zero. The dimension from [the rectangular bridge](rectangular-bridge.md) is
D+1, namely 7 or 13, so o has codimension at least 2. Normality gives
the S2 depth condition and therefore

    Gamma(X minus {o},O)=R.                                     (4)

Equivalently, H^0_(R_+)(R)=H^1_(R_+)(R)=0. The punctured-spectrum
extension used here is the depth-two statement in Lemma 58.20.1, applied
locally at o and glued away from o.
[Stacks Project](https://stacks.math.columbia.edu/tag/0BM7)

It remains to identify the grading with the actual bundle L; S2 alone
would not establish that for an arbitrary weighted Proj. The affine
G quotient V->X has preimage U above X minus {o}: this is exactly the
condition that some positive-degree invariant be nonzero. On U every
G orbit is closed. Indeed a G orbit lies in a stable H_eff orbit, its
closure cannot leave U because some G-invariant is a fixed nonzero
value, and it is closed within that H_eff orbit as a fiber of chi.
Thus U/G=X minus {o} is a geometric quotient. By (3) the residual G_m
action on X minus {o} is free, and its quotient is Q=U/H_eff.

This identifies X minus {o}->Q with the principal G_m bundle associated
to L^(-1). Its regular functions homogeneous of degree t are exactly
the sections of L^t. Equation (4) now proves

    R_t=H^0(Q,L^t)

in every integer degree (the negative degree pieces are zero). It also
identifies the sheaf O_Proj R(1) with L. Thus the argument uses the
original stretch line, even if that line is not generated by its
degree-one sections.

## 5. The tangent determinant proves K_Q=L^(-3)

The smooth principal quotient has the H_eff-equivariant tangent
sequence on U

    0 -> Lie(H_eff) tensor O_U -> V tensor O_U -> pi^* T_Q -> 0.

On each of the three matrix summands the determinant character of the
linear action is det(g)^q det(h)^(-p). Hence

    det(V)=det(g)^(3q) det(h)^(-3p)=chi^(-3).

The determinant of the adjoint representation of H_eff is 1. One can
check this on its Lie algebra sl_p direct_sum sl_q direct_sum C:
the off-diagonal conjugation weights occur in inverse pairs and the
toral directions have weight 1. Taking determinants in the equivariant
tangent sequence and descending gives

    det T_Q = descent(chi^(-3)) = L^3.

This is (1). The determinant calculation is on the effective GL
quotient, including its one-dimensional relative scalar direction;
using the SL quotient here would give the affine dimension instead.

## 6. Vanishing, reflection, and the precise codegree claim

For every integer t>=-2,

    L^t=K_Q tensor L^(t+3),

where L^(t+3) is ample. Kodaira vanishing therefore gives
H^i(Q,L^t)=0 for i>0. The smoothness, projectivity, and characteristic
zero hypotheses were established above. For a proof and algebraic
statement, see Theorem 50 in
[Mathew's notes, pp.25-26](https://math.uchicago.edu/~amathew/kodaira.pdf#page=25).

The Euler polynomial E(t)=chi(Q,L^t) thus equals R_t=P_p(t) at every
t>=0, by Section 4, and so is the same polynomial. Serre duality gives

    E(-t-3)=(-1)^D E(t).

Here D=p(p+1) is even, proving the reflection in (2). As Q has positive
dimension and L is ample, L^(-1) and L^(-2) have no global sections;
their higher cohomology also vanishes by the preceding Kodaira step.
Hence P_p(-1)=P_p(-2)=0. Since Q is irreducible projective,
H^0(Q,O_Q)=C; Kodaira gives its higher cohomology zero. Thus

    P_p(-3)=chi(Q,K_Q)=(-1)^D chi(Q,O_Q)=1.

Finally (1) of [the rectangular bridge](rectangular-bridge.md) is the full ordinary LR coefficient, hence
the Ehrhart function of its nonempty rational hive polytope. Its
dimension is D because its Ehrhart polynomial has degree D. Ehrhart
reciprocity, valid for rational polytopes in their affine lattice,
identifies the relative-interior counts at integer dilation k with
(-1)^D P_p(-k). This proves the exact codegree-three assertion above.
No assertion of integral hive vertices is needed for reciprocity.

The bridge, coprimality, descent, and determinant calculations therefore
establish the independent low-codegree premise for p=2,3 with
the stated P_p(1)>0 established. This is not a bound or classification
for arbitrary rectangular dimensions or other arrow counts.
