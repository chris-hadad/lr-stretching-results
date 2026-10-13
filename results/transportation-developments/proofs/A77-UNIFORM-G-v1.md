# A77 draft: uniform full leaf monotonicity and convexity G

Curated mathematical proof from **A77**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation from the complete accepted V/J formulas.. The uniform argument below plus six fixed exact base polynomials proves G for every n>=3, with the entire H=A jump from HIGH-LEAF-CONTRACTION-v1. No new provider theorem is a premise.

## 1. Complete correction and a positive-product derivative lemma

Let g_n(x,h)=V_n(x,h)-V_n(x,0)-J_n(x,h), with the full low/high J including its entire high tail. Write q=a_(n-1), so d_n=h q/n and a_n=(1+h/n)q. Ordinary coefficient comparisons give


```text
d_n'' a_n >= (d_n a_n)''/6,
d_n'' a_n' >= (d_n a_n)'''/8.                       (1)
```

Here primes are univariate h derivatives and n>=2. These compare full positive polynomials, not values alone.

To prove them, pair the two identical copies of q. Conditional on selecting total s factors in the product q*q, classify each underlying slope as selected twice, once, or zero times. If d slopes are selected twice, the s-2d singleton selections independently choose either labeled copy with probability 1/2; all choices have identical coefficient weight. Thus for the two selected counts p,r, p+r=s, E[p]=s/2, Var(p)=(s-2d)/4, and E[pr]=s(s-1)/4+d/2>=s(s-1)/4. This is a finite weighted coefficient identity, with no probabilistic approximation.

Expand d_n a_n=(h/n)q^2+(h^2/n^2)q^2. For the first term, two derivatives on the first factor have relative weight E[p(p+1)]/[k(k-1)] at total degree k=s+1; it is at least 1/4. For the second term k=s+2 the same relative weight is at least s/[4(s+1)], hence at least 1/6 for s>=2; at s=1 its exact value is 1/6. The only remaining degree k=2 combines the first contribution 2H_(n-1)/n with the second: 2H_(n-1)/n >= [4H_(n-1)/n+2/n^2]/6, since 4H_(n-1)>=1/n. This proves the first inequality.

For two first-factor and one second-factor derivatives, symmetrize p,r. In the first term the numerator is `E[pr](s+2)/2`, so its relative weight is at least (k+1)/(8k)>=1/8. In the second it is s E[(p+1)(r+1)]/2, at least s(s^2+3s+4)/8; divide by (s+2)(s+1)s to obtain at least 1/8 whenever the third derivative exists. This proves the second inequality. The n=2 edge and zero derivative orders follow from the same actual coefficients.

Sorted denominators give q(h)^2 >= (1+h)a_(2n-3)(h). Therefore


```text
d_n a_n >= [h/n](1+h/n)(1+h)a_(2n-3)(h).            (2)
```

All derivatives preserve these coefficientwise inequalities.

## 2. Low-band curvature for every n>=9

Set a=a_(2n-3)(h), D=(2n-1)(2n-2), c=(2n-1)/n, d=(n-1)/(2n), and x=h+u with u>=0. The full J_low is


```text
J_low=a[-d h^3+(x+c+d)h^2-(x+c)h]/D.
```

It is linear in x. Every coefficient of u^k, k>=2, in (partial_h^2 V)(h+u,h) is nonnegative, and J contributes none there. It suffices to pay the u^0 and u^1 coefficients, always differentiating h at fixed x BEFORE substitution.

For u^0, the entire low J curvature obeys


```text
J_hh(h,h) <= [(1-d)(h^3 a)''+(c+d)(h^2 a)'']/D.    (3)
```

Indeed its exact diagonal expression is


```text
D J_hh=(1-d)(h^3a)''+(c+d-1)(h^2a)''-c(ha)''
                                  -2(h^2a)'+2(ha)',
```

and 2(ha)'<=(h^2a)'' coefficientwise. Keep the positive terminal d_n''(h)a_n(h) inside V_hh and apply (1)-(2). The difference from (3) is bounded below by the second derivative of


```text
h a [1/(6n)
   +((n+1)/(6n^2)-(c+d)/D)h
   +(1/(6n^2)-(1-d)/D)h^2].                       (4)
```

All coefficients in its bracket are nonnegative for n>=9. After positive denominators the latter two numerators are 4n^3-17n^2+5n+2 and n^2-9n+2. With n=9+r these are 4r^3+91r^2+671r+1586 and r^2+9r+2.

For u^1, J_xhh=[(h^2-h)a]''/D<=(h^2a)''/D. Keep the full terminal d_n''a_n' inside V_xhh, use the second inequality of (1), and retain the cubic term of (2). Since (h^3a)'''>=3(h^2a)'',


```text
V_xhh >= 3(h^2a)''/(8n^2) >= J_xhh
```

whenever 3D>=8n^2. This holds for n>=9 (already for n>=5), since 3D-8n^2=4n^2-18n+6. All discarded V terms are nonnegative. Thus the complete low curvature is coefficientwise nonnegative for arbitrary n>=9, in the full closed cone x=h+u.

At h=0, g_h is the positive polynomial sum_(l=1)^(n-1)d_(2n-l)(x)/l+a_n(x)/n+(x+c)/D. Integrating each nonnegative numerical-height curvature from zero establishes monotonicity on 0<=H<=A. g(0)=0. This integration is coefficientwise in t with A fixed, not a lattice change.

## 3. Six fixed bases, high band and the full boundary

For n=3,4,5,6,7,8 use the COMPLETE low-cone curvature and first-derivative arrays from the accepted A76 certificate, with every coefficient including zeros and derivative-before-substitution rule. A77 independently reconstructs and compares these exact bases; no positive parameter sampling can replace this gate. These fixed bases combine with section 2 into the all-n proof; increasing the old finite n cutoff is not a premise.

HIGH-LEAF-CONTRACTION-v1 proves high-band derivative and curvature nonnegative for EVERY n>=2, by a full positive rising expansion of V-J. It also proves full H=A continuity and the entire nonnegative first-derivative jump as sum_(j=0)^(n-2)(j+1)a_(n-2-j)(x)B(n-1+j,4). Combining both bands proves G for every n>=3 and every H>=0, including the equality wall and zero height.

This settles the actual uniform G bottleneck. The separate low-envelope argument settles E for H<=A. E for H>A remains unpaid. The n=2 original star case is already signed by the complete two-overlap theorem and needs no assertion of G at a new auxiliary domain. All complete original/lattice/degree/row-bound/strict-shift/label/physical-zero and source boundaries remain.
