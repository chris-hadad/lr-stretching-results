# A57 dependency: complete two-sided lattice and inherited-metric transfer

Source credit: Pro045 U04, Section 2. Only this complete transfer is exported; other provider star claims are outside this dependency. The BV dual-solid valuation and ambient/subspace compatibility premises are stated in the [complete refined normal-cycle proof](../../structural-positivity/proofs/pro027/025-COMPLETE-REFINED-NORMAL-CYCLE.md) and [hidden-strata dual-valuation proof](../../structural-positivity/proofs/pro027/022-HIDDEN-STRATA-BY-DUAL-VALUATION.md). All quotient lattices and inherited metrics below remain part of the argument.

## 2. Complete two-sided lattice and metric transfer

Let L be a lattice with a fixed rational positive-definite metric. Let r be a primitive element of L*, and let v_1,...,v_q be integral elements of L* that, together with r, are linearly independent. Put


```text
C_+ = pos(v_1,...,v_q,r),
C_- = pos(v_1,...,v_q,-r),
L_0 = {x in L : r(x)=0}.
```

Restriction pi:L* -> L_0* is onto: primitiveness of r supplies an integral complement to its kernel. Its kernel is Zr. Let bar(v_i) be the restricted normals and equip L_0 with the INHERITED metric. Then


```text
alpha_L(C_+) + alpha_L(C_-)
   = alpha_{L_0}(pos(bar(v_1),...,bar(v_q))).                 (2.1)
```

Proof. The two cones subdivide C=pos(v_1,...,v_q)+Rr, intersecting in the q-dimensional cone pos(v_1,...,v_q). Their common span has dimension q+1. Dual solid valuation in this fixed span adds the two full-dimensional cells, with no extra term for their lower-dimensional intersection. The lineality of C is exactly Rr by independence. The SOURCE ambient/subspace compatibility identifies its dual local value with the restricted primal lattice L_0 and its inherited metric. This proves (2.1). It uses the entire two-cell fiber, not a favorable half. It is not a lattice-count factorization and does not identify the right side with a conventional smaller-rank hive.

For each K obtained by omitting one v_j, the quotient lattices for K+r and K-r identify canonically with


```text
L_0* / (L_0* intersect span(pi K)).
```

Indeed the restriction preimage of the denominator is L* intersect span(K,r). Both quotients are free and the induced group map is an isomorphism. It carries the primitive class of v_j to the primitive class of pi(v_j), without an index multiplier. On the primal side both are the same saturated lattice

    L intersect ker r intersect intersection_{v in K} ker v.

Thus their induced metrics agree as well. These equalities prove that every cofacet partner in the two-cell correction formula has been included with the right primitive normalization.

If h_{K+r} and h_{K-r} are transported to this common quotient, set


```text
bar(h)_K = h_{K+r} + h_{K-r}.
```

The h_tau contributions on r and -r cancel. Consequently the COMPLETE corrected two-cell sum is the corrected restricted-cone scalar using bar(h). Conversely any restricted field on these facets lifts by splitting each bar(h)_K in half between the two supports. This is a linear transfer identity for the complete fiber, including all q pairs of cofacets. Its sign consequence is only a sign for the SUM of the two cells. Making both cells nonnegative and preserving every other incident cone requires additional global inequalities; the split is not, by itself, a global positive field.

For integral matrix computations, let M_r be a saturated kernel basis of r and D=M_r^T M_r in the Euclidean original lattice. The projected row matrix is N'=N_tau M_r and its dual Gram matrix is


```text
G' = N' D^(-1) (N')^T
   = N_tau N_tau^T - (N_tau r^T)(r N_tau^T)/(r r^T).        (2.2)
```

Replacing D by an identity matrix generally changes the local value. The example below makes that error reverse its sign.
