# A67: all positive-occupation transverse quadratics

Curated accepted mathematical source; the module guide states its exact domain.


Proposed root theorem, pending the A67 independent gate. Let p,q,r be positive integers, N=p+q+r, a=p+q, b=p+r, c=q+r. Use the complete A65 assignment chambers with ORIGINAL offsets U=xt-c, V=yt-2r and assignment sign (-1)^q. Let A(p,q,r)>0 be the accepted equal-slope quadratic from A65 QUADRATIC-WALL.md, with A(p,q,r)=A(r,q,p).

Then, for EVERY positive occupation,


```text
B_U(p,q,r)=A(p,q,r)+A(p,r,q),
B_V(p,q,r)=A(p,q,r)+A(q,p,r).
```

Consequently the complete signed quadratic forms are


```text
Q_U=A(p,q,r)xy+A(p,r,q)x(y-x),    0<x<=y,
Q_V=A(p,q,r)xy+A(q,p,r)y(x-y),    0<y<=x.
```

They are strictly positive on the full supported slope cones. This removes the transverse sign obstruction for all occupations and all numbers of columns. It does not by itself sign the complete one/two/three-class sum.

## 1. A full polynomial specialization proves the first identity

A65 gives the exact chamber polynomial


```text
F_U(U,V)=sum_(k=0)^(c-1) (-1)^k binom(b+k-1,k)
  binom(V+c-1-k,c-1-k) binom(U+a+b-1,a+b+k-1).
```

Set U=M-c and V=-2r as a POLYNOMIAL specialization, without claiming a supported count there. The reflection identity binom(-h,d)=(-1)^d binom(h+d-1,d) gives


```text
binom(-2r+c-1-k,c-1-k)
   =(-1)^(c-1-k) binom(2r-1,c-1-k).
```

Write j=c-1-k. Terms j>2r-1 are zero. Thus


```text
(-1)^q F_U(M-c,-2r)
  =(-1)^(r-1) sum_(j=0)^min(c-1,2r-1)
      binom(2r-1,j) binom(b+c-2-j,c-1-j)
      binom(M+2p-1,2N-2-j).
```

The sum on the right is EXACTLY A65's complete diagonal polynomial F(M) for the permuted occupation (p,r,q), before its assignment sign (-1)^r. Therefore the entire displayed polynomial is the negative of that signed diagonal polynomial. Taking its M^2 coefficient proves


```text
L_U(p,q,r)=-A(p,r,q).
```

Since A65 already proves L_U+B_U=A(p,q,r), the first identity follows. No finite occupation check supplies this quantifier; the binomial identity proves it for arbitrary positive p,q,r. No extrapolation of a negative-flow count is made.

## 2. Chamber reciprocity proves the second identity

For positive integers a,b,c, the root-flow polytope has a variables on edge 12, b on 13 and c on 23, all nonnegative, with edge sums U and V. At U,V>0 it has a strictly positive real point and dimension d=a+b+c-2. Its incidence lattice is saturated and totally unimodular. Subtracting one from EVERY edge coordinate maps its relative-interior integer points at margins (U,V) onto the complete closed count at

    (U-a-b,V-b-c).

Fix a rational slope strictly inside one of the two chambers and clear its denominators. Ehrhart--Macdonald reciprocity on that complete integral root-flow polytope, followed by the eventual chamber formula, gives the following polynomial identity on every such integer ray. As a polynomial identity it then holds on the entire chamber polynomial:


```text
F_C(-U-a-b,-V-b-c)=(-1)^d F_C(U,V).
```

Here d=2N-2 is even. To justify polynomial identity rather than an informal continuation: reciprocity gives F_C(-tU,-tV)=F_C(tU-a-b,tV-b-c) for every sufficiently large positive integer t. Both sides are polynomials in t, so they agree identically; evaluating at t=1 and using all positive integer pairs in the open chamber proves bivariate polynomial equality, then translate variables. Neither the negative point nor the shifted point at a small t is assigned a spurious combinatorial count.

Swapping edge multiplicities a and c and U,V exchanges F_U and F_V. Combining this with reciprocity and keeping the ORIGINAL offsets gives


```text
F_V^(p,q,r)(xt-c,yt-2r)
   =F_U^(r,q,p)(-yt-a,-xt-2p).
```

Both occupation signs are (-1)^q. The coefficient of t^2 is invariant under simultaneously negating x and y, so


```text
Q_V^(p,q,r)(x,y)=Q_U^(r,q,p)(y,x).
```

Apply section 1 and A65's outer-occupation symmetry of A to obtain L_V=-A(q,p,r) and the asserted B_V formula.

The only external theorem used in this step is ordinary Ehrhart--Macdonald reciprocity. A primary-source proof is Beck and Develin, On Stanley's reciprocity theorem for rational cones, https://arxiv.org/abs/math/0409562. The application above establishes its dimension, integral lattice, relative interior and every translation explicitly. A65's complete finite convolution can also verify the polynomial identity directly at any specified occupation.

## 3. Complete-original scope and the next obligation

For every supported three-occupied original assignment, c>0 and r>0 make the constant offsets negative. Eventual nonnegativity therefore requires x>0 and y>0. At unequal slopes the indicated cone applies. At equal slopes the original offsets select the chamber, but both quadratic restrictions equal A x^2. Exterior assignments contribute zero. All labels, assignment multiplicities and offsets remain in the complete sum.

It follows that the ENTIRE three-occupied subtotal has nonnegative c2, strictly positive when a supported three-occupied assignment exists. The full table is this subtotal plus its complete one- and two-occupied subtotals. A65 T1 already has a negative two-occupied subtotal. The argument does not discard it, assign free compensation weights, or assert a whole transportation, rank-seven or unrestricted KTT theorem. Zero occupations remain in their separate exact kernels; no assertion here extends the positive-occupation integral to them.

## Verification plan

Independently compare the identities to full falling-product chamber jets for all positive occupations with N=3..18; verify full specialized diagonal and reciprocity polynomials through N=10; include permutations, ties and deliberately wrong offsets. These checks test the implementation and the delicate identities; the proof above, together with the accepted A65 analytic positivity, supplies the infinite quantifier. The A67 complete-original tests retain all one/two/three-class terms, prior dimension, every determining and two unused grades, and an independent original count.
