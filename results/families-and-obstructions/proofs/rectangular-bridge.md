# A08 rectangular reentry: whole-LR bridge and exact degree

This verifies the root-originated three-matrix construction for p=2 and p=3.
The nonvanishing gate is established by the root's independently frozen
weighted Weyl count: P_2(1)=20 and P_3(1)=266 in attempt
A002-RECTANGULAR-NONVANISHING-002. I read its completed result, runtime
receipt, and successful adapter return after the root supplied the result.
The result file also records the four (1,2) controls 1,3,6,10 at t=0,...,3.
[Frozen count result](../data/rectangular-nonvanishing.json)
[Runtime receipt](rectangular-evidence.md#historical-execution)
[Adapter return](rectangular-evidence.md#historical-execution)
No scientific program, count, native call, or external-model call was run by
this delegate. Prior delegate files remain frozen.

## 1. Result and grade

Put q=p+1, L=pq, and

    R_p = C[Mat_(p x q)^3]^(SL_p x SL_q),
    (R_p)_t = the matrix-entry degree L t part.

The proposed ordinary partitions are correct:

    lambda=((12p-6)^(2p),(10p-5)^p,(5p-2)^(2p-1),(4p-2)^(p+1)),
    mu=nu=((8p-4)^(2p),(4p-2)^(2p)).

Repetition exponents count rows. Their rank is 6p and

    |lambda|=24p(2p-1)=|mu|+|nu|.

With the stated nonvanishing gate met, the exact identity at every integer t>=0 is

    P_p(t):=c^(t lambda)_(t mu,t nu)=dim (R_p)_t.               (1)

The degree of this polynomial is exactly p(p+1). In particular:

| p | lambda | mu=nu | LR rank | sizes | entry grade | degree |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | (18^4,15^2,8^3,6^3) | (12^4,6^4) | 12 | 144=72+72 | 6t | 6 |
| 3 | (30^6,25^3,13^5,10^4) | (20^6,10^6) | 18 | 360=180+180 | 12t | 12 |

These are constructor calculations, not evaluations of LR coefficients.

## 2. Exceptional pair and source character

Use the inward-oriented Q=T_(3,3,4) from
[the frozen A08 derivation](rectangular-extension.md), with new outer source
v on the long arm. The old affine-E6 subquiver Q0 has null root delta with
outer/inner arm values 1,2 and central value 3. Let e be the old extending
endpoint adjacent to v. The exceptional representation E1 has dimension
2 delta+e on Q0 and zero at v; E2 is the simple at v. Thus E1 has short
arm values 2,4, extended-arm values 0,3,4, and central value 6.

The real-Schur premise is not inferred from a quadratic value alone. On
Q0, the exceptional pair consisting of the finite-E6 highest-root
representation of dimension delta-e and the simple at e embeds the
two-arrow Kronecker quiver. Its exceptional dimension (2,3), witnessed
by the standard pencil [I_2 0],[0 I_2], maps to 2 delta+e. Extending by
zero at v preserves rigidity. The supports and the single arrow v->e give

    Hom(E1,E2)=Hom(E2,E1)=0,
    Ext^1(E1,E2)=0,  dim Ext^1(E2,E1)=3.

Consequently this ordered pair embeds the three-arrow Kronecker quiver
Q', oriented from vertex 2 to vertex 1, with

    I(a,b)=a dim E1+b dim E2.

The embedding theorem preserves generic Hom, Ext, and the Euler form;
its multiplicity clause applies to left-perpendicular dimension vectors.
Here we use the published numbering, Theorem 2.38, pp.1082-1083.
[Derksen-Weyman](https://www.numdam.org/item/10.5802/aif.2636.pdf#page=23)

Take source dimension alpha=(p,q) and beta=(2p-1,p). Since Q' has three
arrows from 2 to 1,

    <beta,.>_(Q')=(-(p+1),p)=:theta,
    <beta,alpha>=-(p+1)p+p(p+1)=0.

The frozen count establishes dim SI(Q',alpha)_theta=P_p(1)>0.
Choose a nonzero polynomial f in this space. Its powers f^t are nonzero
for every t>=1, so t beta is left perpendicular to alpha. The theorem gives

    dim SI(Q',alpha)_(t theta)
      =dim SI(Q,I(alpha))_(<I(t beta),.>)                       (2)

for every t>=1. The equivalence between nonzero multiplicity and
perpendicularity is Definition 2.6 in the same source, p.1072. At t=0,
the zero-weight invariant rings of these acyclic quivers consist of
constants, so (2) also has value 1. No interpolation is used in (2).

## 3. The entry grade is the whole invariant ring

Let H=GL_p x GL_q act on the three matrices by A_i -> g A_i h^(-1), and
on polynomial functions by pullback with the inverse action. The
SL_p x SL_q invariant space is a sum of H characters

    (g,h) -> det(g)^a det(h)^b.

Common scalar matrices act trivially on matrix tuples, giving pa+qb=0.
Since gcd(p,q)=1, necessarily (a,b)=(-qt,pt) for an integer t. A scalar
g=s I_p acts on a homogeneous polynomial of entry degree N by s^(-N),
whereas this character gives s^(-pqt). Hence N=pqt and t>=0. Conversely,
at entry degree pqt every invariant has this same character.

Thus SI(Q',alpha)_(t theta) is exactly (R_p)_t. All other entry degrees
vanish. Regrading by L therefore retains the entire invariant ring; it
does not select a proper Veronese subring or alter the stretch parameter.

## 4. Target character and actual ordinary LR coefficient

The dimension I(alpha) and weight sigma=<I(beta),.> are:

| vertices, ordered toward the center | dimensions | weights |
| --- | --- | --- |
| either short arm | 2p,4p | 2(2p-1),2(2p-1) |
| extended arm | p+1,3p,4p | p,5p-3,2p-1 |
| center | 6p | -6(2p-1) |

Each weight is the value of I(beta) at that vertex minus the values at
the incoming tails. For example the middle extended weight is
3(2p-1)-p=5p-3. The central value is
6(2p-1)-3*4(2p-1)=-6(2p-1). Pairing sigma with E1 and E2 gives
(-q,p), as required.

For p=2,3 the dimensions strictly increase on all arms. A rank-failure
locus for an a-to-b arrow, a<b, has codimension b-a+1. All such
codimensions are at least 2. Functions on the injective-arrow locus
therefore extend to the whole affine representation space. Quotienting
by the noncentral frame groups gives actual partial flags of dimensions

    (2p,4p), (2p,4p), (p+1,3p,4p)

in C^(6p), with precisely the displayed positive Plucker weights.
The highest weights of the first two flags are mu and nu, each padded
with 2p zero rows. The third highest weight is

    tau=((8p-4)^(p+1),(7p-4)^(2p-1),(2p-1)^p,0^(2p)).

Each of mu,nu,tau has size 12p(2p-1). Their total is

    36p(2p-1)=(6p)w,  where w=6(2p-1)=12p-6.

Complementing tau, with its rows reversed, inside the rank-6p,
width-w rectangle gives exactly lambda in Section 1. In representation
terms V_tau=det^w tensor V_lambda^*. The central character supplies the
matching determinant power, so the tensor-invariant multiplicity is
c^lambda_(mu,nu). Scaling the arm weights by t scales every displayed
partition by exactly t. This proves (1).

The same flag construction preserves multiplication. Its total-size
condition gives descent of the original polarization to an ample Cartier
line bundle, by Theorem 2.3; no multiplicity-two hypothesis is part of
that theorem. [Sherman](https://arxiv.org/pdf/1505.06551#page=7)

One can also verify a graded-ring map here. Freeze E1^direct_sum_p on Q0;
its orbit is open by rigidity. The remaining arrow is arbitrary from
C^q to E1(e) tensor C^p=C^3 tensor C^p, precisely three p-by-q matrices.
The target-group saturation of this slice is dense. Restriction is
therefore injective, respects the characters above, and is surjective
in each grade by (2). Thus this particular LR section ring is isomorphic
to the regraded R_p, not merely equal in its Hilbert function.

## 5. Exact dimension without a square-family theorem

For the pair A=[I_p 0], B=[0 I_p], write X A=A Y and X B=B Y.
The first equation specifies rows 1,...,p of Y as [X 0]; the second
specifies rows 2,...,p+1 as [0 X]. On their overlap this gives

    X_(i+1,1)=0, X_(i,p)=0, X_(i+1,j)=X_(i,j-1)

for the applicable indices. The recurrence makes each diagonal constant;
the boundary equations kill every off-diagonal. Therefore X=c I_p and
Y=c I_q. The SL stabilizer has c^p=c^q=1, so c=1.

Already this pair has trivial SL stabilizer; adding a third matrix keeps
it trivial. The generic orbit dimension is consequently

    dim(SL_p x SL_q)=p^2+q^2-2=2pq-1.

For completeness the rational-quotient dimension can be seen directly.
The H orbit of (A,B) is open in Mat_(p x q)^2: its stabilizer is the common
scalar group K, and dim H-1=2pq. On this open orbit, straighten the first
two matrices by an element (S,T) of H. This element is unique modulo K,
so the normalized third matrix S^(-1) C T is well-defined and arbitrary.
The remaining quotient of H/K by SL_p x SL_q has one parameter

    z=det(S)^(-q) det(T)^p.

Indeed its character kernel is (SL_p x SL_q)K. If determinants a,b
satisfy a^(-q)b^p=1, then c=b/a satisfies c^p=a,c^q=b. After removing
this common scalar the two matrices have determinant 1. Thus the rational
quotient on this open set is Mat_(p x q) x G_m, of dimension pq+1.

Finally C(V)^G=Frac C[V]^G for this G. If an invariant rational function
is written a/b with coprime polynomials, invariance and unique
factorization force g(a)=chi(g)a and g(b)=chi(g)b for the same character
chi. The connected semisimple group G has no nontrivial character, so
both a and b are invariant. Finite generation then gives

    Krull dimension R_p=pq+1.

LR stretching is polynomial at every positive integer, by Corollary 4.2.
For a nonempty hive polytope its constant term is 1, so it includes t=0.
[Rassart](https://arxiv.org/pdf/math/0308101#page=10)
The Hilbert series of a positively graded finitely generated domain has
pole order its Krull dimension at z=1. A polynomial Hilbert function of
degree d has pole order d+1. Applying (1) therefore gives d=pq, exactly.

## 6. Reconstruction boundary

The root's degree-based reconstruction is justified: p=2 uses nodes
0,...,6 and holds 7,8; p=3 uses nodes 0,...,12 and holds 13,14. The
positive-node panel is exact once those independent counts pass. This
bridge does not use a canonical shift, reflection, square-family
a-invariant formula, or a conjectural numerator. The separate canonical
argument, if used, must supply its own descent and section-ring premises.
