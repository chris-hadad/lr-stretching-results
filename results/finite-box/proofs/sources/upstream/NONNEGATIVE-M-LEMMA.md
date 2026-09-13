# Campaign-derived extension: nonnegative multiplicities with explicit dominance

Status: independently derived in this verification lane from the submitted character arguments. This is **not a claim contained in either return**, and it requires the root's scheduled independent mathematical review before campaign acceptance. No additional search or positive-stretch counting was performed for this extension.

## Lemma and exact hypotheses

Let n>=1 and let nonempty supports S_1,...,S_N, with repeated occurrences allowed, satisfy

```
F_ij = #{a : S_a intersects [i,j]},       m_ij=F_ij-1 >= 0
```

for every positive type-A interval [i,j]. Let R be an integral nonnegative vector and set R_0=R_(n+1)=0. Require the explicit inequalities

```
(m_ii-1)R_i + R_(i-1) + R_(i+1) >= 0,       1<=i<=n.       (D)
```

Define partitions and target vectors by

```
eta^a_i = sum_(j in S_a,j>=i) R_j,
T = sum_a eta^a,
theta_i = T_i + R_(i-1)-R_i,                 1<=i<=n+1.
```

Then theta is a partition, and for every integer t>=0 the **whole count identity** is

```
[s_(t theta)] product_a s_(t eta^a) =
K_m(tR) = #{x in Z_>=0^E : A_m x=tR}.                         (1)
```

Here A_m contains exactly m_ij copies of the interval column [i,j], E=sum m_ij, and multiplicity zero means that root factor is absent. Fixing support decomposition and factor order, the disconnected-skew construction gives integral ordinary LR boundaries lambda,mu,nu=theta, linear in the padded R coordinates, with

```
c^(t lambda)_(t mu,t nu) = K_m(tR)       for every t>=0.       (2)
```

No feasibility or coefficient sign follows from (D) alone.

If the additional hypothesis

```
P(R) = {x>=0 : A_m x=R} is nonempty                           (F)
```

holds, then P(R) is a bounded integral polytope and (1)–(2) are its Ehrhart polynomial at every t>=0. Let

```
J = {e : there exists x in P(R) with x_e>0},
q = rank(A_m restricted to columns J).
```

The exact degree is

```
d = |J|-q.                                                   (3)
```

This includes R=0: J is empty and d=0. In graph coordinates q is the rank of the active-edge incidence matrix, namely |V_active|-c_active, with isolated vertices either consistently included or consistently omitted. Thus d=E_active-|V_active|+c_active. Parallel copies are separate variables and edges.

## Proof

The difference between consecutive theta parts is exactly the left side of (D), and theta_(n+1)=R_n>=0. Sizes telescope. Therefore theta is dominant and has the same size as the tensor product.

Normalize each character by its highest monomial in simple-root variables. All Weyl numerator deficits have nonnegative simple-root coordinates. A Weyl permutation not preserving every support cut j changes a top-j prefix at some j in S_a; the strictly decreasing vector t eta^a+rho loses at least the adjacent gap tR_j+1 there. Its monomial cannot reach the target exponent tR_j after multiplication by any remaining numerator terms, denominator power series, or the final extraction denominator, whose exponents are all nonnegative. At R_j=0 the strict rho gap is still one. Hence the only contributing numerator subgroup cancels roots avoiding S_a. Multiplication over supports and by the final Weyl denominator leaves reciprocal exponent F_ij-1=m_ij on every interval. Exponent zero leaves the factor one; no positivity assumption m_ij>=1 was used. Dominance ensures that Weyl highest-weight extraction returns the tensor multiplicity, proving (1).

For fixed factor order, set h_a=max(S_a), w_a=eta^a_1 and o_a=sum_(b>a)w_b. Concatenate lambda rows o_a+eta^a_i and mu rows o_a for 1<=i<=h_a. Both are partitions, and their nonempty skew components occupy distinct rows and columns. The skew Schur function factors as product_a s_eta^a, including empty zero-width components. All formulas are linear in R before trailing-zero trimming. Dilation preserves the factorization, proving (2).

The columns of A_m are nonzero and coordinatewise nonnegative, so every coordinate in a feasible fiber is bounded by some entry of R. The interval matrix is totally unimodular and R is integral. Under (F), every vertex is integral, so a real feasible point implies an integer feasible point. Consequently positive-stretch fibers are nonempty, and their lattice-point counts form the Ehrhart polynomial of P(R).

Every coordinate outside J is identically zero. Choose one feasible point making each coordinate in J positive and average those finitely many points. The result is strictly positive on all J. Thus nonnegativity contributes no extra affine equation on those coordinates, and the affine hull is A_J x=R with dimension |J|-rank(A_J). This proves (3) and gives positive leading Ehrhart coefficient in its intrinsic degree. It gives no sign assertion for intermediate ordinary coefficients.

## Why the new obligations cannot be omitted

**Dominance without nonemptiness.** In A2 use one full support {1,2}. Then F=(1,1,1), m=(0,0,0), and at R=(1,1), eta=(2,1,0), theta=(1,1,1). Condition (D) holds with equality. Nevertheless there are no root columns to carry R, and the tensor product with its single factor has zero multiplicity at theta. Both sides of (1) are zero at every positive stretch and one at t=0. They do not define one polynomial on all nonnegative integers. Thus (F), or a separate treatment of empty positive-stretch fibers, is essential before coefficient or degree claims.

**Positive R without full row rank.** In A2 use the two supports {1} and {2}. Then F=(1,1,2), m=(0,0,1), and R=(1,1) again satisfies (D). The sole full-interval coordinate is forced to x=1, so P(R) is an integral point. Here E=1, n=2 and the naive expression E-n=-1 is wrong; the active matrix rank is one and (3) gives d=0. The tensor identity is the elementary occurrence of s_(1,1,1) in s_(1)s_(1,1), with multiplicity one. This control is established algebraically, without running a new count job.

With zeros in R, deleting all intervals that meet them remains a necessary first reduction. With vanishing singleton multiplicities, it is no longer sufficient for degree: further variables may be forced zero and the surviving matrix need not have full rank. An exact feasible point and active-column certificate, or an equivalent proved graph-flow description, must precede interpolation.

## Consequence for a sharper construction question

The support inverse already works for unshifted F>=0, so it can enumerate or certify the F>=1 region needed here without requiring m>=1. The extension makes it reasonable to seek a *specified* low-degree, nonempty, support-realizable fiber satisfying (D), with a complete-count ordinary LR bridge. A proposed experiment must freeze its support multiplicities and R, independently certify (F), identify all active edges, establish degree by (3), and then derive or count only the named complete coefficient.

This does not revive the exact doubled-chain cube pyramid inside the support class. Inclusion-monotonicity of F, and therefore of m, still holds. Its singleton multiplicity two and full-interval multiplicity one violate that necessary condition. Nor does this lemma claim global rooted-coefficient curvature, any fixed-outer-boundary statement, ordinary negativity, or a search result.
