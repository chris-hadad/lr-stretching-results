# All-rank higher-class first jets by complete wall induction

Curated mathematical proof from **Pro029/A006**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Unit7 provider proof, pending the separately recorded adversarial checks and any later independent campaign/human review. New argument: combine the general exact primitive with the complete polarized wall formula; an empty singleton boundary reduces to a lower-rank first jet instead of being declared zero. No finite-rank chamber census is used as a universal premise.

## 1. Object, lattice and theorem

Let p>=3 and n=(n_1,...,n_p) be nonnegative integers with at least three occupied indices. Put N=sum n_i. For i<j the directed edge i->j has multiplicity m_ij=n_i+n_j; multiplicity zero means no edge, not a suppressed positive edge. This graph is connected: every occupied vertex joins every other vertex. Its full incidence lattice is Gamma={b in Z^p:sum b_i=0}, saturated with a spanning-tree integer basis. Its directed incidence matrix is totally unimodular; repeated columns preserve this. All vectors lie in a common open halfspace, so its fibers are bounded. The chamber polynomial space has degree at most D=(p-1)N-(p-1)=(p-1)(N-1).

Define the exact assignment offset

 delta_i=(i-1)n_i-sum_(j>i)n_j.

For every full chamber polynomial F_C of this vector partition function, including polynomial continuations evaluated outside the actual count support, we prove

 F_C(delta)=0,   dF_C(delta)=0.                            (1)

A chamber is always the complete polynomial for the entire root graph. No actual count at a negative netflow is substituted for its polynomial continuation. Identically tied affine rays use a containing closed chamber, whose restriction equals the true unimodular count. Exterior chambers have polynomial zero.

## 2. Credited precise analytic inputs

We use two established results, with source versions and full operative statements recorded in unadopted source-NOTES.md.

(A) The unimodular vector-partition chamber formula as a Jeffrey-Kirwan functional on the total residue of

 exp(<b,z>)/product_(i<j)(1-exp(-(z_i-z_j)))^m_ij.

For type A and its subsystems each chamber functional is a finite linear combination of fixed nested iterated-residue tori around the diagonal. Products apply to disconnected block systems in their direct-sum lattice. For a subsystem with missing empty-empty edges, use a fixed full-type-A arrangement refinement for these residue tori. The same functional on the original meromorphic germ is retained. Additional poles of the primitive on missing diagonals are avoided by those fixed nested contours; no contour is deformed through such a pole. Stokes applies on each chosen torus, and its differentiated form is the original integrand. Thus no claim that a primitive has only the subsystem polar set is needed. Baldoni-Silva--Vergne, arXiv:math/0103097v1, Lemma18, Theorem39 and Theorem45 supply the residue representation, all closed chamber values and local analytic change of variables. Derivatives in b multiply the integrand by linear forms in z. The local replacement x_i=exp(z_i), with one node normalized to1, is legitimate and creates no new local divisor.

(B) The complete unimodular polarized wall-crossing formula, Boysal--Vergne, arXiv:0803.2810v1, Theorem28 and its discrete-convolution formulation (Theorem26/Remark29). It includes an exterior chamber (explicit in its proof). We state below our signed convention directly from 1/(1-e^u)=-e^(-u)/(1-e^(-u)); this fixes our shift sign directly, without relying on potentially ambiguous displayed kappa conventions. No new wall theorem is attributed to this unit.

In (A), after x=exp(z), the rational factor at b=delta is, up to the constant sign (-1)^(sum_i(i-1)n_i), exactly product_i f_i(x)^n_i, where f_i are the Lagrange weights of proof002. Indeed delta_i+outdegree_i=(p-1)n_i. Constants are residues of this form times Omega; first jets are its residues times sum_i h_i log x_i, sum h_i=0.

The primitive in proof002 already implies F_C(delta)=0 whenever at least two weights are occupied: it is a meromorphic primitive in a neighborhood of the diagonal, and all residue tori are closed. Its apparent 1/f factors introduce no additional local polar divisor, because x_i are near1 and nonzero. We nevertheless retain the constant terms in the induction below.

## 3. Every genuine wall and why an empty pair is not one

A wall is a hyperplane spanned by a rank-(p-2) subset of the graph's incidence roots. The rank of incidence roots of a graph with c connected components is p-c. Thus each genuine wall is

 W_S={b:sum_(i in S)b_i=0}

for a bipartition S|T into two connected induced subgraphs. Conversely connected induced subgraphs furnish spanning trees and hence rank p-2. A singleton is connected in dimension0. An induced set of size>=2 is connected exactly when it contains an occupied vertex: empty vertices have no edges between them.

Consequently, if one side is entirely empty, it MUST be a singleton. The proposed five-node2|3 split with two empty nodes does not span a wall. This does not assert that an arbitrary period attached to that artificial split vanishes; it proves that no transition of the actual complete chamber polynomial is owed to such a split. The empty classes remain in the graph throughout.

Put s=|S|, t=|T|, N_S=sum_S n, N_T=sum_T n. Let A be the total multiplicity of original edges directed S->T and B the total multiplicity directed T->S. Polarize every crossing edge to S->T, denoting its root psi. Let kappa be the SUM of the reversed roots, including every multiplicity, so E(kappa)=B for E(b)=sum_S b_i. Then

 M_cross=A+B=t N_S+s N_T,
 E(delta)=B-s N_T.                                      (2)

The second identity follows by writing delta=sum_(i<j)n_j(e_j-e_i) and checking each crossing pair. Both formulae include every repeated edge and every zero multiplicity.

The tangent lattice is Gamma_S direct-sum Gamma_T; adjoining e=e_s0-e_t0, with s0 in S,t0 in T, gives Gamma with index1. All normalization is therefore primitive; there is no omitted lattice index.

## 4. The complete crossing polynomial and all initial bands

Let F_0 be the wall polynomial for the full internal root system; it is the product of the appropriate internal chamber polynomials on S,T, or zero if that wall chamber has no supported count. The complete jump J=F_+-F_- is, up to the fixed orientation sign, the POLYNOMIAL continuation of

 (-1)^B sum_(q_e>=0; sum q_e=E(b)-B)

```text
   [product_cross B_(m_e)(q_e)]
   F_0(b-kappa-sum_cross q_e psi_e),                 (3)
```

where crossing copies may be grouped into a bundle of multiplicity m_e, B_m(q)=binom(q+m-1,m-1), and zero-multiplicity bundles are omitted. This is the full Paradan convolution. It is not a claim that either chamber formula agrees with an actual out-of-support count at arbitrary b. When E is reversed the jump changes orientation; (3) remains its polynomial continuation with the directly polarized sign and shift.

### One-sided orientation and the printed convolution hypothesis

The printed Theorem26 assumes at least one originally positive crossing root. We do NOT invoke that assertion unchanged when A=0. Here is the exact extension needed. In its contour proof, put n=E(b). After applying the finite polynomial differential operator for F_0, the one-variable integrand is

 u^(-n-1) [F_0(partial_x) exp(<b,x>) /

```text
        product_cross(1-exp(-<alpha,x>)u^(E(alpha)))]_(x=0) du.
```

If A=0, every E(alpha)=-1. The bracket is O(1) at u=infinity, including after every finite x derivative. Therefore for n>0 the integrand is O(u^(-n-1))du and has no residue at infinity. Its only other poles are at0 and1. The SAME residue argument as the printed proof consequently establishes C=Par for n>0 in this all-reversed case. No assertion at n=0 follows from this extension or is needed.

The wall theorem's orientation is also respected: apply its printed Theorem28 with -E, whose positive crossing set is nonempty. The defining normal residue gives Par(F_0,Psi,-E)=-Par(F_0,Psi,E) by z->-z, and reversing the jump changes the same sign. Hence(3) is the correct polynomial jump also in our orientation E when A=0. Its weighted-composition continuation is a polynomial, and equality on a sufficiently deep positive integral halfspace identifies it everywhere.

All uses of the generating function below satisfy the strict-grade condition when A=0. We name the sides with N_S>0. Then B=M_cross=tN_S+sN_T and equation(2) gives E(delta)=tN_S>0. Consequently E(delta+Le)>0 for EVERY L>=0, including the initial grade. An empty singleton on the other named side is handled by the same relabeling/reversed orientation in section6. This closes the exceptional source hypothesis without discarding a class, adding an initial value, or assuming an identity at an inadmissible grade.

Expanding the polynomial weight in falling factorials of all crossing q_e proves that the polynomial in Q=E(b)-B is divisible by

 (Q+1)...(Q+M_cross-1),                                (4)

with other tangent coordinates as polynomial parameters. Every term has a factor binom(Q+M_cross-1,M_cross+h-1). This derivation proves the whole negative-grade band, not only one root.

If N_S,N_T>0, set h=sN_T. Equation(2) gives Q(delta)=-h, with1<=h<=M_cross-1. Thus J(delta) and all tangent derivatives vanish. Only its normal derivative can remain. Define g(L)=J(delta+Le). Its polynomial g(0)=0, and (3),(4) show that its ALL-GRADE generating series is

 H(z)=(-1)^B z^h R_0[
 x^(delta-kappa) /
 {product_internal(1-x_j/x_i)^m_ij
  product_polarized_cross(1-z x_j/x_i)^m_ij}],           (5)

where i in S,j in T on each polarized crossing factor, anchors x_s0=x_t0=1, and R_0 denotes the fixed internal chamber residue functional with its full logarithmic measures. The first h grades are exactly zero by(4); hence (5) is not merely an eventual series. For h=0 the same formula is valid at every L>=0 directly from(3).

For ANY polynomial g with g(0)=0, finite Newton expansion proves

 g'(0)=-integral_0^infinity H(-w)dw/w.                 (6)

Indeed sum_(L>=0)binom(L,j)z^L=z^j/(1-z)^(j+1), and minus its integral is (-1)^(j-1)/j, exactly the derivative at0. The expansion is finite. Initial bands above justify this use without adding a spurious constant.

## 5. Identification of the full period, including signs and shifts

On each internal residue torus let x_i be close to1, with nested nonzero radii avoiding every internal coincidence. In the FULL p-node weights set

 X_i=x_i for i in S,    X_j=-w x_j for j in T.

Use X_s0=1 as the global normalization; the second group anchor is X_t0=-w. The full logarithmic volume is, up to orientation, dw/w wedge Omega_S wedge Omega_T. All cross factors are nonzero for w>0: choose the tori small enough that all x_j/x_i have positive real part.

Polarizing the original denominator gives the factor (-1)^B X^(-kappa). Since sum_T delta=-E(delta), scaling the T nodes contributes (-w)^(B-E(delta))=(-w)^h. Therefore the integrand in(5) at z=-w is EXACTLY the original assignment rational factor

 X^delta/product_original(1-X_j/X_i)^m_ij
   = constant sign * product_i f_i(X)^n_i.             (7)

Every exponent is the original offset; no new artificial grading is introduced. The equality includes all crossing and all internal bundles. The chamber residue functional R_0 is fixed, not changed with w.

At w->0 the T weights shrink to order s, and the S weights tend to their complete s-node Lagrange weights. At w->infinity the S weights shrink to order t and the T weights tend to their t-node weights. Leading coefficients are uniformly nonzero on the fixed tori, and every tangential logarithmic derivative is bounded. These statements follow by factoring w in the defining denominators. They remain valid for singleton groups.

If N_S,N_T>0, choose k occupied in T and i occupied in S, then a third occupied j. Proof002's primitive has vanishing endpoint restrictions at both0 and infinity, even when many other occupations vanish. Stokes on each truncated cylinder, followed by the uniform limits and the finite residue sum, proves (6) is zero. Thus the complete jump has zero constant and full first jet in this case.

## 6. The empty-singleton boundary is NOT discarded

The only remaining genuine-wall case has, after naming the two sides, T={v}, n_v=0. All at least three occupied indices remain in S. Put q=|S|=p-1. In the polarized formula h=0 and at L=0 the only crossing allocation is zero. Directly,

 delta-kappa restricted to S = delta^(S),

where delta^(S) uses the ORIGINAL relative index order after deleting v. For i>v exactly n_i is subtracted by kappa; for i<v no subtraction is made. The v component becomes0. Hence

 J(delta+xi)=constant sign*F_S(delta^(S)+xi)

for tangent xi, proving the constant and all tangent first jets zero by the smaller-rank induction.

For the normal derivative use the same full period(5)-(7). Choose occupied j,k in S and another occupied index in O. The endpoint at infinity vanishes because all S weights shrink and that O factor has a positive exponent. At zero, write g_i for the q-node weights on S. Then

 f_i -> g_i (i in S),
 f_v = w^q/product_(i in S)x_i * (1+O(w)),
 d_tan log f_v -> -sum_(i in S)dlog x_i.

The complete boundary form of proof002 is therefore, up to orientation,

 lim_(w->0) eta_p = 1/q * eta_S wedge d ell,
 ell=-sum_(i in S)log x_i,                             (8)

where eta_S is EXACTLY the lower-rank primitive with the same occupied j,k and the full remaining occupations. The factor is(q-1)!/q!=1/q. This is an equality of tangential forms on the residue tori, not a pointwise assertion that eta tends to zero.

The logarithms in ell have their single-valued analytic branches near1. Stokes on the CLOSED internal torus gives

 R_S[eta_S wedge d ell] = +/- R_S[ell d eta_S]

```text
                    = +/- R_S[ell product g_i^n_i Omega_S].   (9)
```

By analytic input(A), the last quantity is a linear combination of the complete smaller-rank first derivatives at delta^(S). Explicitly, in the gauge x_s0=1, ell represents the tangent direction h_S=(q-1)e_s0-sum_(i in S,i!=s0)e_i, whose coordinate sum is zero. The residue in(9) is the directional derivative dF_S(delta^(S))[h_S], up to the displayed orientation. Every such derivative is zero by induction. Thus the boundary RESIDUE is zero, although the form itself need not vanish. This is the missing endpoint contribution, accounted for rather than suppressed.

The identity g(0)=0, already proved above, makes (6) convergent after the finite residue functional. No interchange of a divergent unintegrated limit is made: first apply Stokes on [epsilon,R], take each finite residue, and then use the uniform boundary limit(8) and(9). The possible logarithmic divergence before taking a residue has zero leading residue by g(0)=0.

If the empty singleton is named S instead, the same argument applies with w inverted, or with the orientation of the complete jump reversed. The polynomial signed convention is fixed by(3), not an assumption that an actual count continues across a support facet.

## 7. Exhaustive rank induction and chamber propagation

For p<=2 the assertion with at least three occupied weights is vacuous. At p=3 every genuine cut has positive occupation on both sides; section5 proves all jump first jets zero. In general assume(1) for every smaller p and every occupation with at least three positive entries. Section5 settles every occupied/occupied cut, and section6 settles every possible empty-side cut by the smaller-rank assertion. Section3 exhausts genuine walls.

Extend the chamber polynomial by zero to the exterior of the pointed support cone, as in the wall theorem. A generic path from an exterior chamber to any desired full chamber crosses finitely many walls and avoids their codimension>=2 intersections. Across every such transition both the constant and gradient at delta are unchanged and start at zero. Therefore(1) holds in every chamber. No enumeration of the number of chambers, and no unproved coverage of an auxiliary fan, is used.

The original count on a tied affine ray is its containing closed chamber restriction by the unimodular chamber theorem. An eventual ray outside support is identically zero. Thus all eventual affine rays required by whole transportation assignments are covered, not only nonnegative-netflow Lidskii rays.

## 8. What has and has not been proved

The proof establishes zero constant and first jet for every higher-class assignment chamber at its original offset, at arbitrary rank and with all empty positions allowed. Quadratic and higher coefficients may be nonzero or negative. Arbitrary shifted weights are outside the theorem. The full all-row transportation consequence uses the separately credited complete one-/two-class cut formula and entire LR bridge; it is written separately, not assumed in this auxiliary proof.
