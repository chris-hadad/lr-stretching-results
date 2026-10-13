# A77: failed high-core reserve comparison

Curated mathematical proof from **A77**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

This is an exact obstruction to one proposed sufficient auxiliary inequality. It is not a negative LR original, a negative whole-star coefficient, or a reason to abandon the high-star route.

Use the COMPLETE high-band contraction W_n(x,x+z)=sum_j d_j(z) C_(n,j)(x). Define the complete shifted core coefficients


```text
F_n(x,2x+z)=sum_j d_j(z) R_(n,j)(x),
R_(n,j)=sum_(l=j)^(n-1) d_(l-j)(2x)
                   [a_n(x)a_(n-l)(x)-d_(2n-l)(x)].
```

The terminal R_(n,n-1)=C_(n,n-1) is retained. A proposed analogue of the earlier A76 product bound was R_(n,j)>=n C_(n,j)+C_(n,n-1) for j<n-1. It is FALSE. At n=4,j=2 its ENTIRE exact difference is


```text
-8x/15 -71x^2/45 -7x^3/4 -65x^4/72
                              -13x^5/60 -7x^6/360.
```

Both full R and C definitions include every original constrained-column term; no coefficient was selected from a truncated series. The exact formal probe saved all coefficients at n=3..12, all j=0..n-2, and exited normally. Its negative block rejects this stronger inequality only. The complete n=4 high-star polynomial itself is paid by A76's complete finite all-margin certificate, so treating this block as a negative original would contradict its actual scope.
