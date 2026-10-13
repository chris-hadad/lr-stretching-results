# A56: full branching, a paid two-letter fiber, and exact generation obstructions

Curated mathematical proof from **A56**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

26 September 2026. Root derivations. A55's complete affine LR gain and FR044's all-two-row theorem remain accepted antecedents. The compatible-cycle coefficient formula originates in Ferroni--McGinnis, *Lattice points in slices of prisms*, Theorem 1.2 (https://arxiv.org/html/2202.11808v2); the proof below rederives the formula needed here. This is an extension/clarification of the campaign mechanism, not a worldwide novelty claim.

## 1. Keep the entire affine object

For partitions eta contained in alpha and content x=(a,b,gamma), let a>=b+2 and |alpha|-|eta|=a+b+sum gamma. The unit-balanced y=(a-1,b+1,gamma) gives


```text
G(t)=K_(t alpha/t eta,t y)-K_(t alpha/t eta,t x).
```

A55 writes this as a single literal original affine LR coefficient at every t>=1 with the simultaneous first-part -1 outer/inner offsets. Those two fixed offsets and the full strict Pieri interval bt<j<=(b+1)t are retained. The affine family is not an ordinary homothetic LR family. If both before and after are feasible G(0)=0; if the before is empty and after feasible G(0)=1. Formal negative boundary parts at t=0 are never counted.

The complete Schur branching identity is


```text
G(t)=sum_(t eta <= beta <= t alpha, |beta|-t|eta|=(a+b)t)
       D_beta(t) K_(t alpha/beta,t gamma),            (1)
D_beta(t)=K_(beta/t eta,((a-1)t,(b+1)t))
                   -K_(beta/t eta,(at,bt)).
```

The sum includes EVERY intermediate partition and its entire remaining tableau count. It follows by splitting a semistandard tableau at its first two labels. The inner region has shape beta/t eta and the complement has the remaining labels; gluing is the unique inverse. No lattice-word tableau is inferred from a bare weight count: A55's full skew-Schur coefficient construction supplies the literal LR interpretation. Reordering the two balanced labels to the first two positions uses symmetry of the entire skew Schur character, not a rowwise relabeling bijection.

## 2. Uniform ordinary positivity of each homothetic two-letter fiber

Fix ANY skew diagram rho/eta of area a+b. A column of height at least three makes both two-letter counts zero. Otherwise define overlaps h_i=max(rho_(i+1)-eta_i,0), H=sum h_i, and free row lengths w_i=rho_i-eta_i-h_(i-1)-h_i. Columns of height two are forced (1,2), leaving independent free intervals. Hence, after deleting zero w_i,


```text
s_(t rho/t eta)(x,y)=(xy)^(tH) product_i h_(t w_i)(x,y).
```

This is the whole character. Put C=sum w_i=a+b-2H and


```text
E_(w,k)(t)=[z^(kt)] product_i(1+z+...+z^(t w_i)).
```

The balanced difference is E_(w,b+1-H)-E_(w,b-H), with the zero convention outside 0<=k<=C. Since a>=b+2, the new k is at most C/2. Feasible endpoints k=0,C are points. Every interior slice has dimension m-1 for m positive widths: the all-positive proportional point x_i=kw_i/C is strict, the sum equation has saturated lattice, and its box/sum matrix is totally unimodular.

For m>=1 and 0<k<C, let G_q(z)=1+...+z^(q-1), and A_h(z) be the Eulerian descent polynomial (A_0=1). Define


```text
W_(m,h+1,w)(z)=sum_(sigma in S_m with h+1 cycles)
                              product_(cycles B) G_(sum_(i in B) w_i)(z).
```

For 0<=h<=m-1 the COMPLETE ordinary coefficient formula is


```text
(m-1)! [t^h]E_(w,k)(t)
     =[z^(k-1)] A_h(z) W_(m,h+1,w)(z).           (2)
```

Here is an algebraic verification, including the endpoints that matter. Bounded compositions give the full inclusion-exclusion sum


```text
E_(w,k)(t)=sum_(I: w(I)<k) (-1)^|I|
          binom((k-w(I))t+m-1-|I|,m-1).
```

At positive integer t its polynomial binomial equals the combinatorial one, including early zero counts; excluded nonpositive slopes contribute zero. For j=|I| the binomial product has factors q t+1-j,...,q t+m-1-j. The cycle identity


```text
sum_sigma u^(#cycles) product_B (1-z^w(B))
 =sum_I (-1)^|I| z^w(I) u product_(r=1-|I|)^(m-1-|I|)(u+r)
```

follows by marking whole cycles whose union is I and using rising-factorial cycle enumerators on I and its complement. Divide by u, take its u^h coefficient, and multiply by sum_(q>=1)q^h z^q=z A_h(z)/(1-z)^(h+1). Cancelling the h+1 cycle factors (1-z) proves (2). h=0 gives E's constant one directly; outside the stated k range use the explicit point/empty cases, not polynomial extrapolation.

For h>=1 every individual product on the right of (2) is symmetric and unimodal with common center (C-2)/2: its cycle intervals have total degree C-h-1 and A_h has degree h-1. Products and nonnegative sums of symmetric unimodal sequences with aligned centers remain symmetric unimodal (decompose each into sums of centered interval indicators). Eulerian symmetry follows by complementing permutation entries; unimodality follows inductively from the insertion recurrence. In particular, if a_j=A_(n-1,j), the adjacent difference in A_n at k is

    (k+1)(a_k-a_(k-1))+(n-k+1)(a_(k-1)-a_(k-2)),

which is nonnegative up to the new center, using the old symmetry at the central tie. Thus every positive ordinary coefficient of E_(w,k) is nondecreasing for integral 0<=k<=floor(C/2). The constant is one on all feasible slices. A newly feasible point/interior slice has nonnegative coefficients by (2). Therefore the complete TWO-LETTER SKEW balancing gain has nonnegative ordinary coefficients for every skew shape, every width and every degree, with all empty/point exceptions retained.

This is a fully paid terminal for (1) when beta=t rho is fixed. It does NOT prove the whole general gain: the actual sum includes beta not divisible by t, and the remaining weights and chamber limits vary with beta and t. Replacing that entire moving sum by its homothetic fibers would discard lattice points. An exact full control is alpha=(3,1,0,0), eta empty, (a,b,gamma)=(3,0,(0,1)), t=2: the full gain is 2, but the subsum with beta divisible by t is only 1. The legal intermediate beta=(5,1,0,0) contributes the missing 1. This is checked by the full branch count in VERIFICATION.json.

## 3. Exact original obstruction to a free stretch-orbit normalization

The tempting generation operation G(t)=t times an integer-counting homogeneous parent is false already at a paid two-row shape. Take alpha=(3,1,0,0), x=(2,0,1,1), y=(1,1,1,1). Two-row Jacobi--Trudi gives


```text
K_(t alpha,t x)=t+1,
K_(t alpha,t y)=binom(t+2,2),
G(t)=t(t+1)/2.                                  (3)
```

Indeed the (1-z) coefficient at z^t in the product of the positive content row series has no active cap, giving binom(t+d-2,d-2) with d=3 or 4. This is an all-t identity, not a fitted vector. In A55's literal affine embedding the original boundaries are


```text
Lambda=(4t-1,3t,2t,t), Mu=(3t-1,2t,t,0),
Nu=(3t,t,0,0).
```

At t=2 the complete gain is 3, so G(2)/2=3/2. Consequently there is no free cyclic action with every orbit of size t on this gain set, and no identity G(t)=t times an integer-valued counting family. Rational coefficient certificates and more general generation operations remain possible. This is not a negative gain or a negative LR candidate.

## 4. A full affine gain can have a negative Ehrhart-series numerator

Keep the same content pair but take alpha=(2,1,1,0). The before weight is a permutation of the highest weight, so its complete multiplicity is one. For the after weight, use the complete GL4 GT array. Its top row is (2t,t,t,0), its row of length three is (u,t,v) with u+v=2t, t<=u<=2t, and its row of length two is (x,2t-x) with t<=x<=u; the bottom entry is t. These are all inequalities and row sums, in a saturated integer (u,x) lattice. Thus


```text
K_(t alpha,t y)=sum_(u=t)^(2t)(u-t+1)=binom(t+2,2),
G(t)=t(t+3)/2,
sum_(t>=0)G(t)z^t=(2z-z^2)/(1-z)^3.              (4)
```

The literal original affine boundaries are the same Lambda,Mu as above, with Nu=(2t,t,t,0). In particular the once-only shifts and legal ties at t=1 remain original. This complete degree-two gain has positive ordinary coefficients but a NEGATIVE z^2 coefficient in its unique degree-two Ehrhart-series numerator. It cannot be given a nonnegative h-star expansion in binom(t+2-j,2), nor can a proof assume the numerator of its standard graded series is the nonnegative h-vector of a Cohen--Macaulay module of dimension three. This refutes those named whole-generation shortcuts only. It does not refute general weighted valuation, ordinary coefficient positivity, or unrestricted KTT.

A second exact warning concerns summing over a strict moving endpoint. The full half-open count sum_(r=1)^t r^4 is


```text
t^5/5+t^4/2+t^3/3-t/30.
```

It counts 0<=x_i<r<=t for four coordinates, with every integer point retained. Its negative linear coefficient proves that nonnegative ordinary fiber polynomials alone do not survive arbitrary strict-endpoint summation. This auxiliary object is not claimed to be an LR gain or counterexample. The complete LR example (4) and this auxiliary obstruction have deliberately different claim ceilings.

## 5. Direction after the two architectures

Architecture A supplies a complete branching identity and an unbounded paid fiber theorem, but has not paid the moving-weight sum. Architecture B's free t-orbit and nonnegative Ehrhart-numerator candidates are exactly refuted by full affine original controls; the weaker weighted valuation route survives with its strict endpoint and full signed combination. Neither failure retires coefficientwise content balancing.

The root therefore deepens the complete initial-split competitor through its global width fan and an exhaustive c1 certificate, rather than inflating A55's already-positive tableau panel. The strongest affine reentry is a simultaneous coefficient kernel for (1), retaining all nonhomothetic beta and their complement counts; the exact controls (3),(4) must survive unchanged. Marked-order positivity in Jochemko--Menon (https://arxiv.org/html/2604.08394v2, Theorems 1.3 and 3.5) does not automatically cover prescribed content sums; a valid bridge must explicitly retain them. No theorem about those sums is attributed to that paper.
