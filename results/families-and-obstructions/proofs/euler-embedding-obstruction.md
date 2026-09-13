# A07 — an Euler-signature obstruction to the naive quiver bridge

Root-originated route and proof, 7 September 2026. Independent mathematics
review is pending. The exact source premise is preserved in
../../delegates/actual-lr-geometry/SOURCE-EULER-EMBEDDING.md.

## 1. The ordinary LR target has at most one negative Euler direction

For an acyclic quiver Q, the symmetrized Euler matrix is 2I minus its
undirected adjacency matrix, counting parallel arrows with multiplicity.
The orientation does not affect this symmetric matrix. Ordinary LR numbers
are semi-invariant multiplicities on the three-arm flag tree T_(p,q,r),
with arm lengths p-1,q-1,r-1; full flags use p=q=r.

Remove the central vertex. The three remaining diagonal blocks are the
positive-definite A_(p-1), A_(q-1), A_(r-1) Cartan matrices. For a path of
length a, the entry of its inverse at an end is a/(a+1). Eliminating those
blocks by real congruence leaves the one-by-one Schur complement

    2-(p-1)/p-(q-1)/q-(r-1)/r = -1+1/p+1/q+1/r.       (1)

Thus the negative index of every LR flag Euler form is at most one. The
form is positive definite when (1)>0, has one null direction when it is zero,
and has exactly one negative direction when it is negative. This is a direct
matrix argument; no classification of all quiver representations is needed.

## 2. The familiar negative-flow sources have several negative directions

Let Q_(ell,m,k) have vertices 0,...,ell, m parallel arrows from i-1 to i
on each chain link, and k additional arrows from 0 directly to ell. Use
dimension one at every vertex and netflow t at 0, -t at ell, zero elsewhere.
If s is the flow through the chain, every link independently splits s among
m arrows, while the direct arcs split t-s among k arrows. Its entire count is

    F_(ell,m,k)(t)=sum_(s=0)^t binom(s+m-1,m-1)^ell
                                     binom(t-s+k-1,k-1).     (2)

This is a full acyclic-flow count, not an LR realization. The doubled-chain
cube pyramid is m=2,k=1. The accepted abstract ell=17,k=2 negative window is
m=2 with two direct arcs: (2) has degree 19 and c1=-30301/798. The usual
ell=20,m=2,k=1 example has degree 21 and c1=-168011/330.

Delete the two endpoints from the symmetric Euler matrix. The remaining
(ell-1)-by-(ell-1) principal block has diagonal 2 and adjacent entries -m.
Its eigenvalues are

    2-2m cos(j*pi/ell), j=1,...,ell-1.

For m>=2, each j<ell/3 gives a strictly negative eigenvalue. Thus this block,
and hence the full form by restriction, has at least floor((ell-1)/3)
negative directions. In particular, every such source with ell>=7 has at
least two, regardless of k. The two displayed negative examples have at
least five and six, respectively.

## 3. The exact embedding obstruction

Derksen–Weyman's published Theorem 2.38(a) states that the exceptional-sequence
dimension-vector map I satisfies

    <I(beta),I(gamma)>_Q = <beta,gamma>_(Q')

for all dimension vectors beta,gamma. The map is injective. Its symmetrization
therefore realizes the source Euler form as a restriction of the target form.
The negative index cannot increase under restriction. Combining this premise
with sections 1–2 proves:

    No Euler-isometric exceptional-sequence embedding takes
    Q_(ell,m,k), ell>=7, m>=2, k>=1, into any three-arm LR flag quiver.   (3)

The source theorem's multiplicity assertion has additional hypotheses; they
cannot rescue an embedding already excluded by its Euler-isometry assertion.
The three-arrow Kronecker quiver used in A04 has only one negative Euler
direction, so that successful LR bridge does not conflict with (3).

[Derksen–Weyman, Theorem 2.38 and section 7.1](https://www.numdam.org/item/10.5802/aif.2636.pdf)

## 4. What this explains, and what it does not

Wild representation type is not permission to transport any negative flow
polytope into an ordinary LR fiber. This specific whole-quiver route is
blocked for the familiar long doubled chains before one attempts a large
flag construction. The obstruction connects the successful three-arrow
bridge with an explicit failure of a tempting negative-flow generalization.

It does not prove that these flow polytopes lack another full LR realization.
An equality of one stretched Hilbert function, a direct tableau map or a
different representation-theoretic construction need not preserve the whole
Euler pairing. Negative-index-at-most-one is neither a sufficient LR
realization criterion nor a positivity theorem. It must not become a filter
on the campaign's arbitrary LR search.

The next discriminators are a negative acyclic-flow family with negative
Euler index at most one, an explicit non-isometric whole-tableau bridge, or
a proof that a proposed new embedding falls outside the isometric contract.
Do not repeat the universal-wildness shortcut or silently retire the broader
negative-flow mechanism. All original graph/face evidence remains valid.
