# A74: the full row-bound correction for every column-intersection order

Curated mathematical proof from **A74**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root extension of completed Pro051 U12, with its provenance preserved.. U12 derives the first expression below on 0 < H <= A. The additional tail and its closed first coefficient are derived here. No Pro052 working result is a premise. These are complete auxiliary intersections and an exact original recombination, not a general positivity theorem or a negative LR candidate.

## 1. Whole objects and all selected constraints

Fix balanced nonnegative integral three-row margins (A,B,R), 0 < A <= B, and N positive labeled columns e. Physical zero columns are retained in the literal buffered lambda-outer LR constructor of A65 and removed only from formulas. The full original has saturated upper-left integer chart and actual degree (p-1)(N-1), proved by its strict table r_i e_j/M and total unimodularity. The zero-total and single-active-row/column cases are points. A74's original roster retains its exact LR preimages before computation.

In the uncapped first-two-row composition relaxation select S of k columns, each e_j >= A. Set q=N-k and H=A+B-sum_S e_j. If H <= 0 the intersection is empty at every grade, since every selected column requires its own strict +1. In a complete legal original, S containing all columns has H=-R <= 0; hence every active S has q >= 1. For H > 0, selected widths imply H <= B. No restriction H <= A is now imposed.

Let I,J be the two row totals in the q unselected columns. Their multiplicities are binom(I+q-1,q-1) and binom(J+q-1,q-1). Write selected overshoots v_j >= 1. Their total is Ht-I-J and every first-row composition of At-I among k selected columns is allowed: each selected column total is at least At+1. The remaining second-row bound J <= Bt follows from J <= Ht-k <= Bt. The first-row bound I <= At remains ESSENTIAL. Thus the ENTIRE intersection is


```text
J_(q,k)(A,H;t) = sum_(0<=I<=At, J>=0, I+J<=Ht-k)
  binom(At-I+k-1,k-1) binom(I+q-1,q-1)
  binom(J+q-1,q-1) binom(Ht-I-J-1,k-1).               (1)
```

This is the full inclusion-exclusion intersection, allowing any status of unselected column caps. It is not an exact-violation sector. Every labeled allocation and both row bounds are accounted for. All k strict shifts appear as -k. Empty initial grades, including t=0, have count zero.

## 2. The complete two-band polynomial, at every grade

Define


```text
F_(q,k)(A,H;t) = sum_(l=0)^(k-1) (-1)^l binom(q+l-1,l)
  binom(At+k-1-l,k-1-l) binom(Ht+2q-1,2q+k+l-1),    (2)
```

and, for delta >= 0,


```text
T_(q,k)(A,delta;t) = sum_(l=0)^(q-1) binom(N-1+At,q-1-l)
  binom(k+l-1,l) binom(delta t+q-1,N+k+l-1).         (3)
```

Every binomial in (2)-(3) is its falling-product polynomial; at the nonnegative integer grades used here its upper entry is nonnegative. Consequently ordinary empty binomial zeros agree with those products. The full identity is


```text
J_(q,k)(A,H;t) = F_(q,k)(A,H;t)
   - (-1)^(k-1) T_(q,k)(A,(H-A)_+;t),              (4)
```

for H > 0. At delta=0 every final binomial in T is identically zero. In particular (4) includes H=A with no invented boundary term.

For (2), temporarily extend the I sum beyond At using the POLYNOMIAL binomial for the selected first row. Newton expansion in I, followed by the complete Vandermonde convolution with J and all positive overshoots, is exactly U12's derivation and gives F. It is a signed algebraic extension, not a count assigned to negative first-row margins.

The added terms with I=At+v vanish for 1 <= v <= k-1. For v=k+u, u>=0,


```text
binom(At-I+k-1,k-1) = (-1)^(k-1) binom(u+k-1,k-1).
```

After summing J and the overshoots their remaining total is delta t-2k. The other first-row multiplicity is binom(At+N-1+u,q-1). Expand it as


```text
sum_(l=0)^(q-1) binom(At+N-1,q-1-l) binom(u,l).
```

Multiplication by binom(u+k-1,k-1) gives binom(k+l-1,l) times binom(u+k-1,k+l-1), with generating series z^l/(1-z)^(k+l). Convolution with the remaining (1-z)^(-N) gives the last binomial in (3), including its original -2k threshold. Subtracting this ENTIRE signed tail proves (4). If delta <= 0 there is no tail. The proof is an exact finite identity at every t>=0; no degree fit or unsupported initial polynomial continuation enters.

Every summand in (2) and (3) has total t degree <=2N-2. The original intersection (1) has degree exactly 2N-2: choose an open positive region I/t < min(A,H), J/t > 0, I/t+J/t < H, with positive selected first-row mass and overshoot mass. It has positive leading integral, including q=1 or k=1 with the corresponding constant factors. This proves degree before reconstruction. The tail's possible negative coefficients do not affect this geometric conclusion.

## 3. Closed linear coefficient, including the omitted-bound band

Let


```text
b_(q,k) = B(q,k)/2
         = (q-1)!(k-1)!/[2(N-1)!]
         = 1/[2(N-1) binom(N-2,k-1)].
```

U12's complete beta calculation gives [t]F=(-1)^(k-1) H b_(q,k). For the new tail, its final binomial has one zero factor and 2k+l-1 negative factors. All other factors contribute their constants, so


```text
[t]T = -delta integral_0^1 z^(q-1)(1-z)^(2k-1) P(z) dz,
P(z)=sum_(l=0)^(q-1) (-1)^l binom(N-1,q-1-l)
                                  binom(k+l-1,l)(1-z)^l.
```

The elementary truncated binomial transformation is


```text
P(z)=sum_(j=0)^(q-1) binom(k+j-1,j) z^j.              (5)
```

One proof takes the coefficient of u^(q-1) in
(1+u)^(q+k-1)/(1+(1-z)u)^k, then expands
1+(1-z)u=(1+u)[1-zu/(1+u)]. The remaining binomial coefficient is one for each j<=q-1, proving (5) without interpolation.

Let G(z)=(1-z)^k P(z). Finite differentiation telescopes to


```text
G'(z)=-z^(q-1)(1-z)^(k-1)/B(q,k), G(0)=1, G(1)=0.
```

The integral is -B(q,k) integral G'G = B(q,k)/2. Hence


```text
[t]T = -delta b_(q,k),
[t]J = (-1)^(k-1) [H+(H-A)_+] b_(q,k),
[t]((-1)^k J) = -[H+(H-A)_+] b_(q,k) < 0.           (6)
```

EVERY active intersection satisfying the selected-width hypothesis contributes adversely to the full original's linear coefficient, even in the previously omitted H>A band. The entire nonnegative count does not imply positive ordinary coefficients. In particular the missing tail doubles the excess H-A contribution; deleting it changes the complete original.

## 4. Entire original recombination and exact ceiling

If EVERY positive column is >=A, all its nonempty intersections satisfy the selected-width hypothesis. The exact all-grade ORIGINAL polynomial is


```text
P_e(t)=a_(N-1)(At)a_(N-1)(Bt)
         +sum_(nonempty proper S, H_S>0) (-1)^|S|
                                  J_(N-|S|,|S|)(A,H_S;t).  (7)
```

All subsets retain their labels and multiplicities. Equation (7) includes every simultaneous violation and both remaining-row bounds through (4); the all-selected intersection is empty because R>=0. Its exact linear specialization is


```text
c1(P_e)=(A+B) H_(N-1)
   -sum_(nonempty proper S, H_S>0)
      [H_S+(H_S-A)_+]/[2(N-1) binom(N-2,|S|-1)].      (8)
```

This is a complete coefficient identity, not a new general c1 sign theorem; the accepted all-rank transportation c1 theorem already supplies that sign at its own scope. The value of (4)-(8) is the full correction and an explicit obstruction to paying intersections term by term. Higher coefficients and the complete one-active-pair expression still need JOINT payment with the uncapped product and all bounded singleton terms.

The selected complete one-pair cases separately test H<=A and H>A. A complete three-narrow-column case tests all three pair incidences and the triple in H>A. These have all polynomial coefficients checked against the A65 entire-character formula and two independent count engines, with prior degree and unused grades. Auxiliary algebra checks cover both bands, equality, k=1, q=1, all empty early grades, the beta identity and the explicit wrong omitted-tail formula. Finite checks corroborate only their named domain; the finite derivations above supply arbitrary q,k and margin quantifiers.

A positive column below A with active overlaps is outside (7). The adopted U11 no-overlap primitive theorem pays its unique-small-column class, but arbitrary such overlaps remain open. A negative J coefficient, signed intersection, full gain or failure of a sufficient contraction is not an LR candidate. Only a negative ordinary coefficient of a complete legal original invokes candidate handling. No whole-rank, unrestricted KTT, external review, formalization, priority or publication claim is made.
