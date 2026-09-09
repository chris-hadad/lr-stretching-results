# Square-matrix invariants: exact counts and whole LR realization

## Weighted transportation formula

Let R(n,m) be the invariant ring of m matrices of size n under SL_n times
SL_n, and write P(n,m;t) for its component of entry degree nt. After dualizing
one factor if needed, the torus character of the polynomial ring is

    product_(i,j) (1-z*x_i*y_j)^(-m).

The coefficient of a monomial with row exponents r and column exponents c
is the weighted transportation count

    M_m(r,c) = sum_(X>=0, row(X)=r, col(X)=c)
                    product_(i,j) binom(X_ij+m-1,m-1).

This follows by choosing the total degree X_ij among m independent variables.
The weights are dimensions of the complete symmetric powers of C^m.

For GL_n, multiplying a symmetric character by
product_(i<j)(1-x_j/x_i) and taking the coefficient of x_1^t...x_n^t extracts
the multiplicity of det^t. Expand this Vandermonde determinant on both sides:

    P(n,m;t) = sum_(sigma,tau in S_n) sign(sigma) sign(tau)
           M_m((t+i-sigma(i))_i, (t+j-tau(j))_j).             (1)

Here indices are zero-based. A negative margin contributes zero. Formula (1)
holds at every nonnegative integer t, including t=0, and it keeps the original
entry degree nt. It is an exact signed sum, not a polynomial fit.

M_m is invariant under independent permutations of its rows and columns and
under transposition. Therefore equal sorted margin profiles can be combined
with their signed multiplicities before computing any table. Symmetric pairs
of row/column profiles need be evaluated only once. Within the residual DP,
sorting remaining column margins is an exact orbit identification: each
labeled allocation still contributes its own product of binomial weights.
The first row is eliminated, its allocation weight is multiplied, and every
feasible residual table is retained. A last row or column is uniquely forced.
Deleting zero margins also has weight one. These observations prove the
recursion used by matrix_weyl_v001.py over the entire table set.

For n=3 and t>=2, the five sorted profiles are

    (t,t,t): +1,
    (t-1,t,t+1): -2,
    (t-2,t,t+2): -1,
    (t-2,t+1,t+1): +1,
    (t-1,t-1,t+2): +1.

Negative margins are omitted for smaller t. The implementation generates the
permutations directly, so this displayed simplification is not a hard-coded
special case. Native checks, independent n=2 Weyl extraction, and the A06
all-t n=3,m=3 proof provide independent controls for the new counter.


## Scalar matrix-size and stretch exchange

Let R(n,m) be the ring of
invariants of m matrices of size n under SL_n times SL_n. For n,t>=1,

    dim R(n,m)_(nt) = dim R(t,m)_(nt).                        (1)

Equivalently, in the stretch grading,

    P_(n,m)(t) = P_(t,m)(n).

This exchanges the matrix size with the stretch. It does not identify the
graded rings or the polarized varieties for different matrix sizes.

## Complete multiplicity argument

Put d=nt. The degree-d polynomial representation on m matrices decomposes
under GL_n times GL_n times GL_m as

    Sym^d(C^n tensor C^n tensor C^m)
      = direct_sum_(alpha,beta,lambda partitions of d)
          g(alpha,beta,lambda) S_alpha(C^n) tensor S_beta(C^n)
                                tensor S_lambda(C^m).

One may dualize either n-dimensional factor to match the left-right action;
the SL_n-invariant multiplicities do not change. The only SL_n-trivial Schur
functor of degree d is det^t, indexed by the rectangle (t^n). Hence

    P_(n,m)(t) = sum_lambda g((t^n),(t^n),lambda) dim S_lambda(C^m).

Conjugating a partition tensors its Specht module with the sign character.
Tensoring BOTH rectangular Specht factors by sign has no effect, because
sign squared is trivial. Consequently

    g((t^n),(t^n),lambda) = g((n^t),(n^t),lambda)

for every lambda. Substitution proves (1), including its entire GL_m module,
without an exceptional-pair convention or a numerical assumption. At t=0 the
original count is separately one; no matrix size zero is introduced.

The construction below makes both sides specified ordinary LR counts. Equation
(1) is therefore a whole-LR equality between two explicit families, at the
indicated different integer parameters. It is not a homogeneous identity
obtained by silently changing a fixed boundary triple.


## Whole LR construction

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
root's proposed vector is

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

For clarity, the two-Kronecker vector (q,q+1) is genuinely exceptional. It
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


The formulas apply to this specialized square-matrix invariant family. They do
not provide an arbitrary-flow-quiver embedding or a global ordinary-positivity
theorem. Source theorem hypotheses and the equal-dimension edge case remain
part of the construction.
