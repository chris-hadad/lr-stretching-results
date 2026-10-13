# A70: exact unequal-row dominant-parent bridge and a negative paired cap

Curated accepted mathematical source; the module guide states its exact domain.

Let old widths d_j>=0 have total D. Take arbitrary row margins r_1,r_2,r_3>=D and merged width c=sum r_i-D. Every allocation of the old columns gives a legal parent, so P_parent(t)=product_j binom(d_j t+2,2), with its complete original table/LR correspondence. For 0<=s<=c split the merged column into s,c-s. Retain every zero row/column at its actual degree. Rational parameters are interpreted by scaling ALL margins.

Write C(h) for the full weighted-cap quadratic of CONVEX-CAP.md and let


```text
F(h)=h^2/2+Dh/12+(sum d_j^2)/36-11D^2/72.
```

F is the UNTRUNCATED finite weighted-binomial quadratic for every h, not the actual truncated cap when h<D. The complete gain is exactly


```text
G(s)=s^2/2+9Ds/4
   -sum_i C(s-r_i+D)
   +sum_i [F(c-s-r_i+D)-C(c-s-r_i+D)].          (1)
```

This includes every singleton and pair cap; the triple cap is zero because s<=c, with its original strict shift retained. It is a finite scalar-cap reduction for all these unequal-row parents, not a sign inference from convexity alone.

To prove the pair term, fix its complementary row i and write Z for that row's total among the old columns. Its original inclusion-exclusion binomial is binom((s-c+r_i)t-Z,2). Put x_j=d_j t-(row-i entry), X=sum x_j and h'=c-s-r_i+D. Its argument is -(h't-X). The exact polynomial identity


```text
binom(-e,2)=binom(e+1,2)
```

identifies the pair contribution with the negative-excess part of the UNTRUNCATED weighted sum. At e=0 and e=-1 both sides vanish; at e<=-2 this is exactly the ordinary nonzero pair range. Thus the full pair quadratic is F(h')-C(h'). The singletons are the earlier exact C terms and the uncapped factor gives the first line of (1). This proves (1) at every grade before extraction, including all integer initial bands and ties.

The formula is symmetric under s -> c-s. Directly,


```text
sum_i [F(c-s-r_i+D)-F(s-r_i+D)]
   =(c-2s)(c/2+9D/4),
```

which is exactly the difference between the two uncapped quadratics. It gives G(0)=G(c)=0 without silently moving a boundary term. When r_i=R>=D and s<=c/2, every paired argument h'>=D, so F(h')=C(h') and (1) reduces to BALANCED-SPLITTING.md.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation. This extends the complete count identity, not the balanced-family sign theorem. It identifies the next unpaid compensation explicitly.

## The paired correction cannot be declared coefficient-positive

For a single old width d=2 and h=1, the full cap is


```text
F_d(1;t)=binom(t+3,4),
```

by the entire convolution z/(1-z)^5; its old upper bound 2t is redundant on the supported range. The corresponding UNTRUNCATED weighted sum is


```text
(t^2/6) binom(2t+2,2).
```

Their complete paired remainder is therefore


```text
t(t-1)(t+1)(7t+6)/24
   =7t^4/24+t^3/4-7t^2/24-t/4.                (2)
```

It is a nonnegative integer count at every nonnegative integer t and has negative ordinary quadratic coefficient -7/24. It is not a complete LR polynomial. The earlier convex cap theorem is true, but an attempt to extend the balanced proof by discarding these allegedly positive paired remainders is false. Formula (2) is an all-grade algebraic countercontrol, not an extra selected original or an LR-negative candidate.

The next complete sign question is (1) with all three coupled row margins, or a stronger equivalent functional. Parents with some r_i<D introduce still more coupling because their old-column allocations are themselves constrained. The existing six-original numerical roster is not enlarged for this symbolic bridge. Its proof is exact; numerical unequal-row verification and the full sign law remain successor obligations, with the paired countercontrol retained.
