# A70: complete Green compensation for every balanced dominant parent

Curated accepted mathematical source; the module guide states its exact domain.

Let d_1,...,d_m be nonnegative integer old column widths, D=sum d_j, and R a positive integer with R>=D. Start with the COMPLETE three-row transportation parent


```text
rows (R,R,R), columns (c,d_1,...,d_m), c=3R-D.
```

Split c into a,b>=0 with a+b=c. The ENTIRE ordinary quadratic gain is nonnegative, and it is strictly positive if a,b>0. This is uniform in m and all widths, including R=D, every subset-sum tie, zero old columns and all rational splits after scaling every margin. It settles the full Green payment at this exact family, not just its wall atoms. General arbitrary-row parents and unrestricted KTT remain open.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root theorem. Premises: the accepted whole LR/table constructor and original lattice/degree proof in A65 THREE-ROW-KERNEL.md; the complete split-gain/Green identities in A68/A69; and the newly independently reviewed CONVEX-CAP.md. No active provider result is a premise.

## Exact full count before the coefficient

Every allocation of the old columns has row totals z_i>=0 with sum z_i=Dt and z_i<=Dt<=Rt. It determines a unique parent table with merged entries v_i=Rt-z_i. Thus


```text
P_parent(t)=product_j binom(d_j t+2,2).
```

The parent is nonempty even at R=D and on rest-allocation boundaries v_i=0. Its free active table chart is saturated. If all m old widths are positive, parent degree is 2m and a genuine interior split has child degree 2m+2, by the strictly positive real table r_i c_j/sum r and total unimodularity. Delete zero columns first and retain their original positions. The accepted A65 constructor supplies a literal whole LR triple, lambda outer, without a metric equivalence claim.

Set s=min(a,b), so 0<=s<=c/2. A parent's split fiber is the FULL weakly capped composition


```text
w_1+w_2+w_3=st, 0<=w_i<=Rt-z_i.
```

Its inclusion-exclusion count is the uncapped binomial binom(st+2,2) minus the three singleton caps binom((s-R)t+z_i+1,2), plus pair and triple terms. Every pair threshold is at least (2R-D)t. Since


```text
s<=c/2=(3R-D)/2<=2R-D,
```

no pair term contributes, including equality: its original shifted binomial vanishes there. The triple term is likewise zero. No row constraint has been dropped.

For each singled-out row, put x_j=d_j t-(that row's entry in old column j). The other two entries in that column have exactly x_j+1 allocations. The singleton cap is therefore precisely F_d(s-R+D;t) of CONVEX-CAP.md. The three rows have identical full sums, hence the exact whole polynomial identity


```text
P_child(s;t)=P_parent(t) binom(st+2,2)
                     -3 F_d(s-R+D;t).          (1)
```

It holds at every integer t and all boundaries. Rational s requires clearing ALL margins, not altering the table lattice. As [t]P_parent=3D/2 and P_parent(0)=1, its ENTIRE quadratic gain is


```text
G(s)=s^2/2+9Ds/4-3 C_d(s-R+D).                 (2)
```

This sum includes every old-column allocation and every full fiber. It is exactly the A68/A69 complete gain, so proving (2) nonnegative pays both the smooth and atomic Green contributions without signing or omitting them separately.

## All split ratios, not only one chamber

If 0<=s<=R-D, the cap vanishes and G=s^2/2+9Ds/4.

If R-D<=s<=R and D>0, put h=s-R+D in [0,D]. The proved complete cap chord bound gives


```text
G(s)>=s^2/2+9Ds/4-11D(s-R+D)/8
      =s^2/2+7Ds/8+11D(R-D)/8.                (3)
```

This is strictly positive for s>0. In particular R=D is included, where the transition band starts immediately at zero; no stable-region or initial-band assumption is added.

If R<=s<=c/2, substitute the exact terminal cap polynomial (5). The result has quadratic coefficient -1 and linear coefficient c, so


```text
G'(s)=c-2s>=0
```

on this entire last half-band. Its initial value at s=R is already positive by (3), proving positivity throughout. At R=D this last band collapses to one point and causes no missing case. Symmetry under exchanging a and b covers the other half. Endpoints a=0 or b=0 give the identical original and G=0 at its actual lower degree.

If D=0, the parent is a point. Formula (2) becomes s^2/2-(3/2)(s-R)_+^2 on 0<=s<=3R/2. It is positive on (0,R], and from R to 3R/2 its derivative is 3R-2s>=0. Thus the no-old-column case is included without dividing by D. If R=0 too, every margin is zero and both tables are points with gain zero; this degenerate case is stated separately from the positive-R theorem.

## Exact ceiling and what comes next

This proves a full original-to-original c2 operation at unbounded column count and includes the difficult transition bands missed by the elementary product chamber and two-long-column chamber. It does not prove positivity of every coefficient of the child, monotonicity of G on its transition band, or a terminating cover of arbitrary parents. The family condition R>=D is substantive: removing it introduces nontrivial pair caps before the midpoint and prevents free old-column allocation in the parent. The full arbitrary-margin Green-payment inequality, all three-row transportation c2, whole rank seven and unrestricted KTT remain open.

The selected independent checks use four complete endpoints L1..L4 (prior degrees 10/12), every determining grade plus two unused grades, and complete split curves. Existing K12 is reused because it belongs to this family; other A68/A69 curves remain general regression/countercontrols, not extra evidence for an unproved family extension. The proof supplies the infinite quantifier; finite comparisons check the original identity, offset, lattice and implementation.
