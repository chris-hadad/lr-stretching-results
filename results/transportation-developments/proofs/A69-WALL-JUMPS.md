# A69: every complete transportation wall has a nonpositive quadratic slope jump

Curated mathematical proof from **A69**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root theorem. The only sign premise is the accepted all-positive-occupation A65/A67 kernel theorem. This result concerns the ordinary quadratic coefficient of the ENTIRE three-row transportation original. It does not sign its smooth interval curvature or the full column-splitting gain.

## 1. A symmetric signed boundary kernel

For integers p>=1 and q,r>=0 with L=q+r>=1, let B(p,q,r) be the coefficient of xy in the complete SIGNED U-chamber quadratic


```text
[t^2] (-1)^q F_U(xt-L,yt-2r)
   = E(p,q,r)x^2+B(p,q,r)xy.
```

The edge multiplicities are a=p+q,b=p+r,c=L, all positive. The last falling binomial in every A65 term has its unique zero factor at t=0: its upper offset is 2p-1, its lower index 2p+L+k-1. Thus there is no y^2 term, including q=0 or r=0. We prove three identities/signs:


```text
B(p,q,r)=B(p,r,q),
sum_(r=0)^L binom(L,r) B(p,L-r,r)=0,
B(p,q,r)=A(p,q,r)+A(p,r,q)>0  when q,r>0.       (1)
```

The last equality is exactly A67, with both positive occupations required. The first two are complete polynomial identities, proved next, so they also determine the empty-class terms. In particular the two endpoint values agree and are strictly negative for L>=2; both are zero for L=1.

### Reflection, including the empty classes

Write B_j(v)=binom(v+j-1,j-1), always as a polynomial here. For each integer U>=0 the complete U-chamber polynomial is the finite convolution


```text
F_U^(a,b,c)(U,V)=sum_(z=0)^U B_a(U-z)B_b(z)B_c(V-z).
```

This equality holds polynomially in V, since it holds for every integer V>=U. Substitute z -> U-z and use B_c(-w-c)=(-1)^(c-1)B_c(w). Polynomial equality for all U>=0 then gives the full bivariate identity


```text
F_U^(a,b,c)(U,V)
  =(-1)^(c-1) F_U^(b,a,c)(U,U-V-c).
```

The ORIGINAL offsets transform as U=xt-L and U-V-c=(x-y)t-2q. Multiplying by the original signs therefore yields


```text
(-1)^q F_U^(p,q,r)(x,y)
  =-(-1)^r F_U^(p,r,q)(x,x-y),                 (2)
```

where this shorthand denotes the displayed affine t substitutions. Comparing xy in its quadratic part proves the first identity in (1). The transformed argument is a polynomial specialization, not a count assigned to an unsupported negative flow.

### Zero sum, with the original offsets changed once

Use A67's exact Lagrange factors L_i=z_i^2/((z_i-z_j)(z_i-z_k)), with L_1+L_2+L_3=1. For fixed p,L,


```text
sum_(q+r=L) binom(L,r) L_1^p L_2^q L_3^r
  =L_1^p(1-L_1)^L
  =sum_(j=0)^L (-1)^j binom(L,j)L_1^(p+j).     (3)
```

Extract the same formal Laurent coefficient on both sides, with slope coordinates 0<x<y. The left terms eventually have their exact U-chamber polynomial with occupation (p,q,r). On the right each one-occupied term has the missing edge 23 and requires x>=y, so it is zero for every sufficiently large grade. Hence the entire signed left polynomial is zero for each such rational ray, and then as a bivariate polynomial. The xy coefficient is the second identity in (1).

Equation (3) is a kernel identity. Its coefficient specialization can have negative original row exponents; no legal-original positivity or count is inferred there. It merely proves the algebraic cancellation used below on legal margins. Every occupation's original shift follows from its own Lagrange power; none is frozen across a changed occupation.

## 2. The full jump on a physical wall

Now take an ENTIRE transportation original with three positive rows r_1,r_2,r_3 and N positive labeled columns w_j. Let J be a nonempty proper subset of columns, p=|J|, L=N-p, and consider its physical wall


```text
delta=sum_(j in J) w_j-r_1=0.
```

First work at a generic point of this wall with no other physical wall present. In the complete A65 expansion, the only terms changing chamber here assign exactly J to color 1. The complement is assigned in every possible way to colors 2 and 3. Write S for the set assigned to color 3, z=sum_(j in S) w_j, h=r_3 and W=sum_(j notin J)w_j=r_2+r_3. Each such assignment enters support at delta=0 only when h-z>0. Its quadratic term on the supported side is E delta^2+B(p,L-|S|,|S|)delta(h-z). The jump of the derivative with respect to delta, positive side minus negative side, is therefore


```text
J_(1,J)=sum_(S subset J^c)
      B(p,L-|S|,|S|)(h-z)_+.                  (4)
```

This contains the adverse empty class, every positive class and their exact labeled multiplicities. It is a derivative jump of the complete original coefficient, not a subtotal being credited as the answer.

Let


```text
H_W(h,z)=min(h,z)(W-max(h,z))/W
        =h(1-z/W)-(h-z)_+.
```

It is nonnegative for 0<=h,z<=W, strictly positive when both are interior. The symmetric weights in (1) give


```text
sum_S B(p,L-|S|,|S|)=0,
sum_S B(p,L-|S|,|S|)z=0.
```

For the second equality, pair S with its complement: their masses sum to W and their weights agree, so the weighted sum is W/2 times the first sum. Subtract the affine chord h(1-z/W) in (4). Its weighted sum vanishes, and the two endpoint Green values vanish. This proves the exact positive-payment formula


```text
J_(1,J)=-sum_(empty != S proper subset J^c)
   [A(p,L-|S|,|S|)+A(p,|S|,L-|S|)] H_W(h,z)
   <=0.                                      (5)
```

It is strictly negative when L>=2, since every complement column and both other rows are positive. It is zero when L=1. The formula is symmetric in the two other rows because H_W(W-h,W-z)=H_W(h,z) and complements pair.

Row permutation is an integer bijection on the WHOLE original, so (5) holds for every row wall sum_J w_j=r_i. It is valid for arbitrary widths and any number of columns, without a finite occupation ceiling.

## 3. Complete splitting curves, collisions and boundaries

On a split curve w_1=c-s,w_2=s, all other w_j fixed, the normal speed of a wall is epsilon=1_(2 in J)-1_(1 in J). A transverse crossing contributes |epsilon| J_(i,J) to the derivative jump. A wall with epsilon=0 is not crossed. At a collision, sum the contributions from every crossed labeled (i,J); do not choose only one. To justify the collision rule, allow arbitrarily small generic rational perturbations of BOTH the positive row margins and EVERY labeled fixed column width d_j. Set the perturbed merged width c'=sum(r')-sum(d'), and use the same split coordinate s with columns c'-s,s,d'_1,...,d'_m. Positivity of all rows, old widths and both split parts holds on a sufficiently small neighborhood of each original interior knot. These parameters range over an open set, so this balanced perturbation does not force equal widths to remain equal.

For a crossed wall, its knot is either r_i-sum_(j in S)d_j (the subset contains s) or sum_(h!=i)r_h-sum_(j in S)d_j (the subset contains c-s, after complementing its old columns). Distinct crossed labeled walls have distinct linear forms in the independent r_i,d_j variables: their row coefficient vectors are e_i or (1,1,1)-e_i, six distinct vectors, and their old-column indicator vectors distinguish the remaining cases. Thus all unequal-wall coincidences lie in a finite union of proper hyperplanes. Constant-wall relations are likewise proper linear equations. A sequence of positive rational perturbations avoiding this union separates every crossed labeled wall and avoids any wall containing the path. Clear ALL denominators when interpreting each rational member as an integer original; homogeneity returns its exact quadratic coefficient to the original parameter scale. No extra numerical original or relaxed lattice is used.

Choose fixed outer points just to the left and right of the old collision, with no other knot between them and the collision. The finitely many full chamber quadratics have coefficients continuous in the margins and uniformly bounded Hessians on this local compact neighborhood. At either outer point, the derivative of a nearby generic curve tends to the original one-sided derivative: away from crossed walls the same polynomial applies, and across a constant wall the tangential derivatives agree because the complete coefficient has equal polynomial restrictions on that wall. That equality follows within positive row/column margins from the A65 quadratic kernels: their U/V restrictions match; supported-axis restrictions vanish unless the corresponding occupation is empty, in which case the apparent discontinuity lies on a forced-zero ROW boundary outside this positive neighborhood.

For each perturbed curve the derivative difference between the two outer points is the sum of its generic wall jumps plus the integral of its bounded smooth curvature. First let the perturbations tend to zero, then let the outer points approach the original collision. Formula (5) is continuous on each wall, and the smooth-curvature integral tends to zero with the interval length. The limiting jump is therefore the sum of ALL coincident crossed-wall contributions. Walls with epsilon=0 never create an atom. In particular, equal-width subset ties such as K12's five sets of mass s+4 are separated by the labeled-width perturbation and all five survive the limit; their labels are never quotiented away.

A68 already proves that all full splitting kernels are continuous and that every possible knot comes from these support/chamber walls. Consequently EVERY interior derivative jump of the complete three-row splitting gain is nonpositive. Its parent coefficient is constant in s, so it has the same jumps as the child coefficient. Its one-column starting parent and all interior positive split parts are included.

Forced-zero columns are deleted with original positions recorded. With at most two positive rows, complete bounded-composition inclusion-exclusion gives the quadratic coefficient as a finite linear combination of (a-linear-subset-sum)_+^2: take the t^2 coefficient of each full binomial with its once-only |S| shift. A degree-two term at an identically zero slope is zero. Each squared hinge is C1, so no derivative-jump atom occurs. A one-row table or a point has no quadratic term. Split endpoints s=0,c retain their actual degree and the exact A68 zero gain; only interior atoms enter the Green formula. There is no lattice/residue relaxation anywhere: the complete table chart remains saturated, and rational parameters are cleared by scaling ALL margins.

## 4. What this pays, and what it leaves open

The theorem signs the entire ATOMIC part of the split curvature measure. A69 AGGREGATE.md proves that its smooth part can be positive for infinitely many complete originals: G(s)=s^2/2+9Ds/4 in a dominant-column endpoint band. Therefore nonpositive atoms do not prove concavity or nonnegative gain.

Combining (5) with the exact Green formula yields


```text
G(s)=positive_atomic_payment(s)
      -sum_intervals 2 beta_I integral_I H_c(s,u) du,
```

where positive_atomic_payment is the sum of H_c(s,k) times the positive right side of -J_k in (5). This is an exact whole-original formula with every wall contribution now explicitly paid. The remaining question is whether this payment and the negative smooth intervals dominate the positive smooth intervals for every legal original. A universal derivative sign on [0,c/2] is a sufficient alternative, not a theorem of this note. Complete finite curves support it at their stated margins only.

Verification: wall_v1.py checks all occupation boundary identities through total 18, 210 separate falling-product B values, 308 full reflection identities and 42 full zero-sum polynomial identities. It reconstructs every derivative jump of the three selected complete split curves from 366 physical-wall contributions at all 23 interior knots, and retains a negative control that drops the empty-class endpoint. The analytic argument supplies the unbounded quantifier; the checks validate it and its implementation. The exact final receipts and independent gate govern acceptance.
