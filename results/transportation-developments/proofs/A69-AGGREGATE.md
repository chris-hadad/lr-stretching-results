# A69 complete aggregate and the failure of universal concavity

Curated mathematical proof from **A69**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation. Accepted A65/A67/A68 premises apply at their exact scopes. No current Pro049/Pro050 source is used here.

## Full all-margin measure before taking signs

For fixed balanced nonnegative original rows r and parent columns (c,d_1,...,d_m), first retain original zero positions and use every labeled rest assignment f. Let its occupation n, totals C and exact multiplicity w be as in A68. For each pair i<j use n'=n+e_i+e_j and x(s)=C_1+c 1_(i=1)-r_1+s(1_(j=1)-1_(i=1)), y(s)=r_3-C_3-c 1_(i=3)+s(1_(i=3)-1_(j=3)). On each open interval determined by ALL roots of x,y,x-y, use the original eventual support and lexicographic offsets U=(x,-n'_2-n'_3), V=(y,-2n'_3). The exact kernel is a quadratic q20 x^2+q11 xy+q02 y^2; unsupported terms are zero. Define its interval polynomial p_fij(s) by substitution, without fitting.

The complete interval polynomial U_I is the sum of w p_fij. The quadratic coefficient of G(s)=U(s)+U(c-s)-U(0)-U(c) is beta_I+beta_reflected(I). At an interior knot k its derivative jump is J_U(k)+J_U(c-k). Here J_U(k) is the full sum of w[p_right'(k)-p_left'(k)] over every assignment and pair, including kernels which enter or leave support. A68's admissible-direction continuity proves there are no value steps or isolated corrections. This is a finite all-margin signed measure, with no missing zero-occupation terms. The implementation forms these sums symbolically, combines equal knots and then differentiates; determining/unused points are separate checks.

For three-positive n', the accepted A67 formulas make the pair-direction quadratic coefficients explicit. In the U chamber they are -A(p,r,q), A(p,q,r), 0 for pairs (1,2),(1,3),(2,3); in V they are 0,A(p,q,r),-A(q,p,r). Each is used with that pair's OWN increased occupation. The positive A67 measure represents each A, but the aggregate retains positive and negative weights as well as separate two-occupied boundary terms. It is not a nonpositive measure by construction.

## A whole-original infinite convex family

Let the remaining positive columns d_j have sum D and suppose every r_i>D. Set c=sum(r)-D. For 0<=s<=min(r)-D, every arbitrary nonnegative allocation of each small column d_j and the new column s leaves a nonnegative entry r_i-minus-the-small-row-total in the remaining column c-s. This is an integer bijection in the original saturated table chart, including the closed upper endpoint. Consequently, for integral margins and every grade t,


```text
P_parent(t) = product_j binom(d_j t+2,2),
P_child(s;t) = P_parent(t) binom(s t+2,2).
```

The parent constant is one and its linear coefficient is 3D/2. The ENTIRE quadratic gain is therefore


```text
G(s)=s^2/2+9Ds/4.                         (1)
```

The rational-s statement follows by scaling ALL margins to integers and quadratic homogeneity of the exact coefficient. It also holds for m=0 (the one-column point) and at s=0 where the split column vanishes. For positive margins the prior actual degrees are 2m and 2(m+1); an interior positive table r_i c_j/sum(r) and the free chart prove these before any coefficient extraction. Every original offset in the A65 representation must reproduce this exact product identity; the product proof itself needs no continuation.

Thus G''=1 on a nonempty interval for infinitely many COMPLETE legal LR originals, of arbitrarily many columns. For example r=(D+1,D+1,D+1), c=2D+3 works for every positive old list. This refutes universal aggregate concavity. It is not a negative gain, not a negative polynomial, and not new positivity coverage for the already elementary product chamber. It is a decisive obstruction to the proposed proof architecture. Both reflected endpoint bands are strictly convex. The upper band retains all ties.

## The exact weaker criterion

For any continuous piecewise quadratic zero-endpoint G on [0,c], define its full second-derivative measure nu_G, including every slope jump, and the nonnegative Dirichlet Green kernel


```text
H_c(s,u)=min(s,u)(c-max(s,u))/c.
```

Twice integrating on each interval and matching all derivative jumps proves


```text
G(s) = - integral_[0,c] H_c(s,u) dnu_G(u).   (2)
```

Only interior jump atoms are included; interval curvature is ordinary 2 beta du. The kernel vanishes at u=0,c, so endpoint atoms are immaterial. This formula is equivalent to the full curve, not a new positivity theorem. A useful sufficient condition is G'(s)>=0 on [0,c/2], combined with symmetry and G(0)=0. It is strictly weaker than concavity and accommodates (1); its all-margin sign remains open until proved. Exact complete curves must test interval endpoint derivatives and every one-sided derivative at the complete knot roster; positivity of a few endpoint gains is insufficient.

The current work compares this derivative/Green criterion with complete character transitions and the fixed positive occupation measure. No all-parent gain or unrestricted KTT sign is claimed.
