# An affine-E6 construction for every arrow count at least two

The construction is verified for integers q,n>=1, with the q=1
equal-dimension edge treated explicitly below. The argument is symbolic.

## 1. Result

Let R(n,q+1) be the polynomial invariant ring of q+1 n-by-n matrices under
SL_n x SL_n, and let its stretch grade t mean matrix-entry degree nt.
Define ordinary partitions

    mu=nu=((2q^2)^(qn),(q^2)^(qn)),

    lambda=((3q^2)^(qn),
            (2q^2+q)^((q-1)n),
            (q^2+1)^(qn),
            (q^2)^n).

Zero repetitions are omitted. These are nonincreasing partitions for q>=1,
with maximum length 3qn and size

    |lambda|=6q^3 n=|mu|+|nu|.

Then, for every integer t>=0,

    c^(t lambda)_(t mu,t nu) = dim R(n,q+1)_(nt).                    (1)

The proof below checks the real Schur root, exceptional pair, source weight,
all-dilation nonvanishing, and actual flag character. It also gives a graded
restriction-ring isomorphism for this particular construction; it does not
infer that stronger statement from (1) alone.

## 2. Ambient graphs and the crucial rigid-root premise

Orient Q=T_(3,3,4) inward toward its central vertex. Let v be the outermost
vertex of its arm with three noncentral vertices, and let e be the neighbor
of v. Deleting v leaves Q0=T_(3,3,3), the affine E6 quiver. In Q0, e is an
extending source vertex.

The primitive null root delta of Q0 has central value 3 and values 1,2 along
each arm, from its outer endpoint toward the center. Thus delta_e=1. The
proposed vector is

    alpha_q=q delta+e

on Q0, extended by zero at v when viewed on Q. We must show that alpha_q is
real Schur and rigid; its quadratic value 1 alone is not the proof.

### 2.1 A constructive two-Kronecker proof

Let I be the simple representation at e. Because e is a source, I is simple
injective. Let P be the indecomposable representation of dimension delta-e
supported on Q0-e. This is the highest-root representation of the remaining
finite E6 quiver. Gabriel's theorem gives P, and finite-Dynkin
indecomposables are exceptional. Extend P by zero at e.

The finite-root assertion can be recognized directly from the affine
extension: removing an extending vertex of coefficient 1 leaves the finite
highest root delta-e. Alternatively, delta-e is a positive integral vector
of quadratic value 1 on the finite E6 root lattice, and hence a positive
root there. This use of quadratic value 1 is in finite Dynkin type, not a
claim that every quadratic-value-one vector in the wild target is Schur.

Since the supports of I and P are disjoint at e, both Hom(I,P) and Hom(P,I)
vanish. The Euler formula at the source e gives

    Ext^1(P,I)=0,
    dim Ext^1(I,P)=2.

Thus (P,I), in this order, is an exceptional sequence giving the two-arrow
Kronecker quiver, with the sink simple mapped to P and the source simple
mapped to I. Derksen-Weyman's embedding theorem preserves generic Hom,
Ext, the Euler form, and the Schur-root property.

For clarity, the two-Kronecker vector (q,q+1) is exceptional. It
has the standard pencil

    A=[I_q  0],    B=[0  I_q],    A,B:C^(q+1)->C^q.

If X A=A Y and X B=B Y, the overlapping entries force X to be constant
along its diagonals. The boundary equations force every off-diagonal entry
to be zero; hence X and Y are the same scalar multiples of their identity
matrices. Therefore its endomorphism algebra is C. Its Euler self-pairing
is 1, so its self-Ext space vanishes.

The embedded dimension vector is

    q dim P+(q+1) dim I=q(delta-e)+(q+1)e=q delta+e.

This proves the required real Schur and rigid property of alpha_q. Extending
by zero at the newly attached source v preserves the Hom/Ext complex, so
alpha_q remains exceptional as a dimension vector for the full quiver Q.

### 2.2 The nonzero-defect check

The defect on the affine subquiver Q0 is partial(x)=<delta,x>_(Q0).
Because e is a source and delta_e=1,

    partial(alpha_q)=q<delta,delta>+<delta,e>=1.

Thus the resulting indecomposable lies in the preinjective part of affine
E6. This agrees with the constructive proof; it is not a regular real-root
case where rigidity could fail. The defect is being used on Q0, not as a
purported affine defect for the wild eight-vertex quiver Q.

Hubery's *Hall polynomials for affine quivers*, Section 1, arXiv pp.4-5,
explicitly states the defect classification and that indecomposable
preprojectives and preinjectives are exceptional. It also describes the
exact Kronecker subcategory associated with an orthogonal exceptional pair.

[Hubery, Section 1](https://arxiv.org/pdf/math/0703178v2#page=4)
[Derksen-Weyman, Theorem 2.38](https://www.numdam.org/item/10.5802/aif.2636.pdf#page=23)

## 3. Adding the new leaf produces q+1 arrows

Choose an exceptional E1 of dimension alpha_q, extended by zero at v, and
let E2 be the simple at v. The supports give Hom(E1,E2)=Hom(E2,E1)=0.
Since v is a source with its sole arrow v -> e,

    Ext^1(E1,E2)=0,
    dim Ext^1(E2,E1)=dim E1(e)=q+1.

The ordered pair (E1,E2) therefore satisfies the exact hypotheses of
Derksen-Weyman Theorem 2.38. Its embedded source Q' is the (q+1)-arrow
Kronecker quiver with arrows from vertex 2 to vertex 1, and

    I(a,b)=a alpha_q+b dim E2.

This proof controls the orientation and order of the pair, not merely the
absolute value of an Euler pairing.

## 4. The source weight and every dilation

Fix source dimension alpha=(n,n). For each t>=1 put beta=(qt,t). On the
(q+1)-arrow quiver,

    <beta,.>=(-t,t),    <beta,alpha>=0.

The weight space is nonzero: det(A_1)^t is a nonzero semi-invariant of that
weight. Thus beta is left perpendicular to alpha, exactly the hypothesis
needed for the multiplicity part of the embedding theorem. It yields

    dim SI(Q',alpha)_(-t,t)
      = dim SI(Q,I(alpha))_(<I(beta),.>).                             (2)

This is the left-Euler weight convention. It must not be replaced by the
right-Euler convention used for the earlier symmetric CDW construction.

The scalar actions show that the left side of (2) is R(n,q+1)_(nt).
At t=0 both sides are constants, of dimension 1: the representation spaces
are affine spaces of acyclic quivers and the weight is zero. No t=0
extrapolation or change of stretch grade is needed.

## 5. Target dimension and exact character

Write sigma=<q alpha_q+dim E2,.>_Q. The target dimension I(n,n) is

    short arms: qn,2qn;
    extended arm: n,(q+1)n,2qn;
    center: 3qn.

Computing each left-Euler coefficient as its vertex value minus the sum
of values at incoming tails gives exactly the proposed character:

    short arms: q^2,q^2 on each arm;
    extended arm: 1,q^2+q-1,q^2-q;
    center: -3q^2.

These weights are all nonnegative on the arms for q>=1. They pull back
to (-1,1) on the source: sigma(E1)=q-(q+1)=-1 and sigma(E2)=1.

## 6. Actual flag conversion and the q=1 edge

For q>=2 all target dimensions strictly increase toward the center.
The noninjective-arrow complement has codimension at least 2, so regular
semi-invariants extend across it. Quotienting the injective-arrow locus by
the noncentral frame groups gives the three actual partial flags

    Fl(qn,2qn;3qn),
    Fl(qn,2qn;3qn),
    Fl(n,(q+1)n,2qn;3qn).

The first two highest weights are the proposed mu and nu, padded by qn
zeros. The third highest weight before converting the triple invariant
to an ordinary LR coefficient is

    tau=((2q^2)^n,
         (2q^2-1)^(qn),
         (q^2-q)^((q-1)n),
         0^(qn)).

Each of mu,nu,tau has size 3q^3 n. Their total size is 9q^3 n, equal to
rank 3qn times the central determinant power 3q^2. Complementing tau in
the width-3q^2 rectangle gives exactly lambda in Section 1. This proves
the ordinary LR identification at every t, with the original dilation.
The same total-size condition satisfies Sherman's Theorem 2.3 with rank
3qn and box width 3q^2, so the original polarization descends as an ample
Cartier line bundle on its LR quotient.

[Sherman, Theorem 2.3](https://arxiv.org/pdf/1505.06551#page=7)

For q=1 the two consecutive extended-arm dimensions (q+1)n and 2qn
are both 2n. Their common-square edge has a rank-failure divisor, so the
codimension-two extension argument cannot be applied to that edge as stated.
However the inner of these two vertices has weight q^2-q=0 and can be
eliminated exactly.

Write A:C^(2n)->C^(2n) for this edge and B:C^(2n)->C^(3n) for the next
edge. Under the weight-zero intermediate GL_(2n), an invariant polynomial
f(A,B) equals f(I,BA) on the open set det A!=0, and hence everywhere by
polynomial identity. Conversely every polynomial in BA is invariant.
Therefore this elimination is an isomorphism of the relevant coordinate
invariant algebras, respecting the other group characters. It leaves a
strictly increasing arm n,2n,3n and its correct Plucker weights.

The resulting partitions at q=1 are

    lambda=(3^n,2^n,1^n),    mu=nu=(2^n,1^n),

and (1) remains valid. The equal-dimension edge is therefore a necessary
proof case, not an obstruction to the proposed construction.

## 7. Multiplication can also be preserved here

For this new-leaf construction the same rigid-slice proof as in
the source spectral-fibre argument applies. E1^direct_sum_n has an open orbit on the quiver
with v deleted. Fix it there, and let the new arrow be an arbitrary map

    C^n -> E1(e) tensor C^n = C^(q+1) tensor C^n.

This is precisely q+1 matrices. The target-group saturation of the slice is
dense, so restriction of semi-invariants is injective. The character check
in Section 5 makes it graded, and (2) makes it surjective in every grade.
The flag conversion in Section 6 preserves products, including its explicit
weight-zero contraction when q=1. Thus this particular actual LR section
ring is isomorphic to R(n,q+1) with stretch grade t=entry degree/n.

This is a concrete map argument plus the source theorem. It is not an
inference of ring structure from isolated coefficient coincidences.

## 8. An explicit q=2,n=1 example

Substitution gives

    lambda=(12,12,10,5,5,4),
    mu=nu=(8,8,4,4),
    |lambda|=48=24+24.

Since SL_1 is trivial, R(1,3) is a polynomial ring in three degree-one
variables. Hence the entire stretched LR polynomial for this triple is

    c^(t lambda)_(t mu,t nu)=binom(t+2,2),    t>=0.

This is a theoretical consequence of the full bridge above, not a newly
executed LR count or a fit to initial values.

## 9. Source and claim limits

The exact embedding theorem and its Euler/multiplicity hypotheses are
Derksen-Weyman Theorem 2.38(a)-(c), published pp.1082-1083; its older
arXiv numbering is 2.39. Their Section 7.1, pp.1114-1116, supplies the
three-arm flag/Schur framework. Hubery's primary paper supplies the tame
defect/exceptional classification used as a cross-check of the constructive
rigid-root argument.

[Derksen-Weyman, Section 7.1](https://www.numdam.org/item/10.5802/aif.2636.pdf#page=55)
[Hubery, Hall polynomials for affine quivers](https://arxiv.org/pdf/math/0703178v2)

This verifies an arbitrary-arrow-count **two-vertex Kronecker** construction.
It does not embed every flow quiver into a flag quiver and does not bypass
the Euler-index obstruction to whole-quiver embeddings with multiple
negative directions. No ordinary-negative polynomial or additional finite-box coverage is claimed.
