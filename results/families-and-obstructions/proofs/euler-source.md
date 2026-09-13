# Euler preservation in the Chindris–Derksen–Weyman embedding construction

This note verifies the published premise and its hypotheses. The
negative-index calculations for the three-arm target and doubled-chain source
are supplied separately in [the obstruction proof](euler-embedding-obstruction.md).
No such index is calculated in this source note.

## 1. Exact theorem and numbering

The relevant result is Derksen-Weyman, *The combinatorics of quiver
representations*, Annales de l'Institut Fourier 61(3) (2011), 1061-1131,
**Theorem 2.38(a), pp.1082-1083**. In the arXiv version math/0608288v2
(31 August 2007), it is **Theorem 2.39(a), p.16**. Both versions were opened
and the Euler-preservation assertions agree.

- [Published Theorem 2.38](https://www.numdam.org/item/10.5802/aif.2636.pdf#page=23)
- [ArXiv Theorem 2.39](https://arxiv.org/pdf/math/0608288v2#page=16)

CDW, *Counterexamples to Okounkov's log-concavity conjecture*, Compositio
Mathematica 143 (2007), **Theorem 3.3, p.1551**, explicitly cites the older
Theorem 2.39 numbering. CDW states its two-vertex multiplicity specialization;
the full Euler assertion is in the Derksen-Weyman theorem above.

[CDW, Theorem 3.3](https://arxiv.org/pdf/math/0610819#page=7)

## 2. Hypotheses, map, and exact quantifiers

Work over C. Let Q be a finite quiver without oriented cycles. For vertex
vectors u,v, its Euler form is

    <u,v>_Q = sum_x u_x v_x - sum_(a in Q_1) u_(tail a) v_(head a).

Take an exceptional sequence E_1,...,E_s and write epsilon_i=dim E_i.
The precise requirements are

    End_Q(E_i)=C, Ext^1_Q(E_i,E_i)=0;
    Hom_Q(E_i,E_j)=Ext^1_Q(E_i,E_j)=0 for i<j;
    <epsilon_i,epsilon_j>_Q <= 0 for i>j.

Equivalently, the dimension vectors are real Schur roots, are left
perpendicular in the indicated order, and satisfy the last Euler inequalities.
“Schur sequence” with possibly imaginary members is not a replacement for
these exceptional-sequence hypotheses.

Define Q' with vertices 1,...,s and exactly
-<epsilon_i,epsilon_j>_Q arrows i -> j whenever i>j. Its dimension-vector map
is

    I: N^(Q'_0) -> N^(Q_0),
    I(beta)=sum_i beta_i epsilon_i.

Theorem 2.38(a) gives, for **every** beta,gamma in N^(Q'_0),

    <I(beta),I(gamma)>_Q = <beta,gamma>_(Q').          (1)

It also preserves the generic hom and ext numbers. Equation (1) has no
beta-perpendicular-gamma restriction. That additional condition belongs to
part (c), which asserts the multiplicity equality

    (I(beta) circle I(gamma))_Q = (beta circle gamma)_(Q')

when beta is left perpendicular to gamma.

The source definitions are published equation (2.2), p.1069; Definition 2.6,
p.1072; Definitions 2.24, 2.30, and 2.36, pp.1076,1079,1082. In the discussion
after Definition 2.30 the authors explicitly observe that the matrix
(<epsilon_i,epsilon_j>) is lower triangular with diagonal entries 1; therefore
the epsilon_i are linearly independent. Thus I is injective.

## 3. Consequence for the Euler-form obstruction

Let J have columns epsilon_i, and let E_Q,E_(Q') be the Euler matrices in
the chosen vertex bases. Bilinearity extends (1) from nonnegative integer
vectors to the full real vector spaces. In matrix form,

    J^T E_Q J = E_(Q'),
    J^T (E_Q+E_Q^T) J = E_(Q')+E_(Q')^T.             (2)

The theorem therefore gives an injective restriction of the symmetrized Euler
form, beyond a count equality on two chosen vectors. If a target T has
negative index at most one,
(2) excludes any such exceptional-sequence embedding of a source Q' with
at least two negative directions into T. A chain of these embeddings still
has the same Euler-preserving property by composition.

This is the exact implication verified here. The paper does not state the
doubled-chain negative-index result, and this source check does not
supply it.

## 4. The ordinary LR target really has three simple arms

Derksen-Weyman **Section 7.1, pp.1114-1116**, defines T_(p,q,r): three paths
with p-1, q-1, r-1 noncentral vertices meeting at one common central vertex,
with one arrow on each adjacent pair. There are p+q+r-2 vertices. The displayed
orientation points toward the common center. Its underlying graph is a
three-arm tree with simple edges.

[Derksen-Weyman, Section 7.1](https://www.numdam.org/item/10.5802/aif.2636.pdf#page=55)

The source gives an explicit ordinary LR identification on T_(r,r,r). Put
beta(x_i)=beta(y_i)=beta(z_i)=i for 1<=i<r and beta(center)=r. For partitions
lambda,mu,nu padded to length r, define the weight by

    sigma(x_i)=lambda_i-lambda_(i+1),
    sigma(y_i)=mu_i-mu_(i+1),
    sigma(z_i)=nu_(r-i)-nu_(r-i+1),
    sigma(center)=lambda_r+mu_r-nu_1.

Then the displayed formula on p.1115 is

    dim SI(T_(r,r,r),beta)_sigma = c^nu_(lambda,mu).   (3)

The map from partitions to sigma is linear. Replacing all three partitions
by their t-fold stretches replaces sigma by t*sigma, leaving this same
three-arm quiver and beta fixed. Thus the target is not only a one-count
description. The ordinary size condition and weakly decreasing partitions
are exactly the LR data being represented.

For shorter partial flags the source also gives the T_(p,q,r) description
through Definition 7.1 and Lemma 7.3, p.1116; the partition construction there
uses nondecreasing arm dimension sequences. These remain three simple paths
meeting at one center. The concrete CDW proof of Proposition 4.1 uses
T_(4,3,4), its specified exceptional pair, and the pairing -3; that pair
produces the three-arrow Kronecker quiver. See CDW pp.1553-1554.

Orientation choices do not change the symmetrized Euler form of the same
underlying graph. The source identification supports applying the
target-form argument to these ordinary LR flag quivers. It does not assert
that every possible quiver presentation of an LR count must be such a tree.

## 5. Exact ceiling on any resulting no-go statement

The admissible conclusion is a restriction on the **whole source quiver
embedding through this Euler-preserving exceptional-sequence route**.
It would not prove any of the following:

- that the source's particular flow polytope cannot be integrally affinely
  equivalent to an entire LR fiber;
- that its one stretched Hilbert function cannot equal an ordinary LR
  stretched Hilbert function;
- that its particular graded ray ring cannot have another quiver
  presentation or another full-LR realization;
- that a smaller category or a different quiver obtained by a separately
  proved count-preserving construction cannot realize the same target count;
- that an embedding into a different intermediate quiver, followed by a
  non-Euler-preserving realization argument, is impossible.

Equality of a selected weight-space dimension, of one entire Hilbert
function, or even an independently established isomorphism of selected ray
rings does not by itself preserve the full Euler form of the original
representation category. Those statements cannot be substituted for (1).

The source-flow and target-star inertia calculations are separate proof
obligations. This note does not assert a source-flow dimension vector, boundary
triple or numerical threshold.
