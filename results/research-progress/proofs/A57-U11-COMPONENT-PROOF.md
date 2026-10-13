# A57 dependency: Pro045 U11 support-changing original component

Source credit: Pro045, original Unit 11. The complete Sections 1–9 construction below is used at the accepted A57 component scope, conditional on the original-hive/normal-cycle/BV premises. It proves a positive extractable component and an unsigned residual, and gives no whole coefficient sign. Historical provider assertions about their own checks remain source-qualified; fresh export verification uses independently authored A57 root checkers and all supplied arrays.

The precise two-sided transfer is [retained here](A57-TWO-SIDED-VALUATION.md). The underlying public premises are the [complete refined normal-cycle theorem](../../structural-positivity/proofs/pro027/025-COMPLETE-REFINED-NORMAL-CYCLE.md) and [dual-valuation strata proof](../../structural-positivity/proofs/pro027/022-HIDDEN-STRATA-BY-DUAL-VALUATION.md).

## 1. Main theorem and coefficient scope

Put m=D_n=(n-1)(n-2)/2 and k=n-5, so k>=2 at n>=7. The lattice is the ORIGINAL integer interior-height lattice L_n=Z^m, with its original Euclidean metric. Lambda is outer. All physical A,B,C rhombi and their complete boundary offsets remain distinct.

**Theorem U11-T1.** For every n>=7, the explicit grammar C_n in Section 2 has exactly


```text
4(k^2+3k+4)=4(n^2-7n+14)
```

independent physical five-supports. Their unit-weight assignment v_n cancels EVERY original primitive four-cofacet balance. Its normal span has dimension n-1, and its complete original-lattice BV pairing is


```text
alpha dot v_n = (k+2)(3k+5)/24 = (n-3)(3n-10)/24 > 0.      (1.1)
```

Every cell is retained. All cells occur simultaneously with positive actual (D_n-5)-face weights in one compatible positive generic original-row refinement of ONE legal integral parent of actual dimension and stretching degree D_n. A constructive common-boundary induction supplies that parent at every rank. Moreover there is an explicit full (3n-1)-dimensional neighborhood cone of boundary data with the same property.

**Theorem U11-T2.** The full signed balance kernel supported on C_n is exactly R v_n. Thus, for ANY legal original rank-n parent and fixed compatible refinement, a nonzero nonnegative balanced subassignment using only C_n exists iff every selected cell has positive actual weight. If w denotes the complete actual normal-cycle vector, putting zero on absent cells, its maximum such subassignment is lambda_* v_n with


```text
lambda_* = min_(I in C_n) w_I,
max alpha dot z = [(n-3)(3n-10)/24] lambda_* .             (1.2)
```

For the constructed parents lambda_*>0. Subtracting it leaves a nonnegative fully balanced remainder. That remainder need not be a second LR-parent cycle and its scalar pairing is NOT signed. No whole c_(D_n-5), c10, c1, whole-rank-seven or unrestricted KTT positivity theorem follows.

At n=7 this is exactly U10's 56-cell roster and its inherited sum11/6. At n=8 it has88 cells, pairing35/12 and whole parent degree21. The counts at n=9,10 are128,176 and pairings17/4,35/6. These are complete component pairings, not individual raw scalar signs or complete hive coefficients. The changed support is essential: U10's unchanged56-set roster has zero signed balance kernel at every n>=8.

## 2. Complete physical grammar

For all valid positions on T_n={(i,j):i,j>=0,i+j<=n}, use


```text
rho_Aij=-h(i,j)+h(i+1,j)+h(i,j+1)-h(i+1,j+1),
rho_Bij=-h(i,j)+h(i,j+1)+h(i-1,j+1)-h(i-1,j+2),
rho_Cij=-h(i,j)+h(i-1,j+1)+h(i-1,j)-h(i-2,j+1).
```

Write Aij for the physical row A_(i,j). Set


```text
P={A00,C20},  S={A03,B13},
a=B11,  -a=A01,  u=A02,  v=A11,  w=B21,
t_i=C(i,4),  2<=i<=n-4.
```

The symbol '-a' in the grammar denotes A01, whose INTERIOR normal is opposite to B11. It is not negation of the full affine physical row. There are k=n-5 path rows.

Take every p in P, every s in S, and add one of these triples:


```text
(-a,u,v), (-a,u,w), (u,v,w), (a,v,w);                    [four]
(-a,v,t), (-a,w,t), (a,v,t), (a,w,t), for every t;        [4k]
(-a,t_i,t_j), (a,t_i,t_j), for every i<j.                [2*C(k,2)]
```

All resulting physical five-sets are distinct. The rows in the fixed P,S,a,u,v,w part use only positions in T5; the path rows exist through the original outer boundary. This is a complete generating definition, not a finite truncation of a q5 atlas. It gives the count in T1.

In the original normal lattice,


```text
n_C20=-n_A00=e11,
n_A03=-n_B13=e13-e14,
n_B11=-n_A01=-e11+e12,
n_v+n_w=n_u+n_a.                                      (2.1)
```

The last equality is also a literal FULL-HEIGHT identity rho_v+rho_w=rho_u+rho_a. The other opposite pairs retain distinct physical offsets.

Let z_1=e14, z_i=e_(i,4)-e_(i-1,5) for2<=i<=n-5, and z_(n-4)=0 in the interior-normal lattice. Then


```text
n_(t_i)=z_(i-1)-z_i,   sum_i n_(t_i)=e14.               (2.2)
```

The last equality uses the actual boundary status at rank n. Keeping the old endpoint fixed at higher rank would lose it. The full normal span is generated by e11,e12,e13,e14,e21-e22 and k-1 independent differences z_i, hence dimension k+4=n-1.

## 3. Original lattice and metric; complete balance

Contract successively the three primitive lineality directions e11, e13-e14, and a=-e11+e12. On the primal side this means the saturated sublattice


```text
x11=x12=0,  x13=x14.
```

The relevant remaining quotient coordinates are


```text
b=x13=x14, c=x21-x22,
z_i=x_(i,4)-x_(i-1,5), 2<=i<=n-5.
```

They map this sublattice ONTO Z^(k+1). The coordinates involve disjoint pairs except for the explicitly identified b pair, so a coordinate-selection integer right inverse exists. The inherited primal quotient metric is


```text
diag(2,1/2,...,1/2),
```

and its dual metric is diag(1/2,2,...,2). The identity metric is NOT substituted. In this quotient the rays


```text
R={bar(v)=c, bar(w)=-b-c, bar(t_2),...,bar(t_(n-4))}
```

form a positive circuit: their sum is zero, they span dimension d=k+1, and any d of the d+1=k+2 rays form an integer basis. The unit-basis assertion follows also by successively removing endpoints in the incidence path c,b,z_2,...,z_(n-5). Thus every proper subcollection, in particular every pair, has full integer image.

Before the stellar subdivision, take all pairs of R and lift each by every sign of the three primitive lineality directions, represented by the physical pairs P,S,{A01,B11}. This gives8*C(k+2,2) independent five-cones. All have full normal image Z^5: use the unimodular coordinate split for the three lineality rows and the unit pair image in the quotient. Equivalently there is an actual five-column minor +/-1. All four-cofacet images are Z^4 by projection, so every primitive quotient factor is ONE.

At a cofacet missing a lineality direction, the two signed partners have opposite primitive classes and equal weights. At a cofacet retaining all three lineality directions and one circuit ray r, the remaining rays sum to -r modulo those directions, so balance holds there too. These are all cofacet types; any global support not in this cofacet union has zero incidence.

Now subdivide each of the four cones {p,s,-a,v,w}, one for each p,s, along the ray


```text
u=v+w-a.
```

It is a positive sum of the three displayed generators -a,v,w. Its three subdivisions are {p,s,-a,u,v}, {p,s,-a,u,w}, {p,s,u,v,w}. The integer changes of the five generators have determinant +/-1. The opposite partners on every new internal cofacet cancel, and each old exterior primitive class is unchanged because the coefficients in u=v+w-a are all one in that cone. The subdivisions of the p/s boundary faces are identical on the two sides. Therefore every balance persists with unit weights. This adds eight cones and yields exactly the grammar of Section2. It also proves all its five-row image indices and all primitive quotient factors equal one at every rank.

This is an original-lattice fan subdivision argument. It neither identifies a conventional smaller hive nor asserts that an arbitrary physical cone can be removed because some whole parent is positive.

## 4. Complete BV pairing without an expanding scalar census

The accepted dual-solid valuation and inherited-subspace compatibility imply that the sum of the two cones pos(J,r) and pos(J,-r) equals the local value of the restricted cone in the saturated lattice ker r, with its inherited metric. This is the complete two-sided fiber identity already proved in U04; here all three contractions have their explicit integral splits in Section3.

First undo the stellar subdivision by valuation. Sum both P signs, both S signs and both a signs, using the complete two-sided identity each time. The WHOLE pairing becomes


```text
sum_{i<j} alpha_2(pos(r_i,r_j))
```

on the positive-circuit rays R in the inherited quotient metric. All pair images are Z^2. For such a unimodular pair with dual Gram entries G_ij, the degree-two specialization of the accepted finite Bernoulli/holomorphic-projection formula is


```text
alpha_2(r_i,r_j)=1/4-(1/12)(G_ij/G_ii+G_ij/G_jj).       (4.1)
```

For clarity, the degree-zero generating expression is1/4+(c_i/c_j+c_j/c_i)/12. Metric projection sends c_i/c_j to -G_ij/G_ii and c_j/c_i to -G_ij/G_jj, giving (4.1). This projection precedes a one-variable specialization. The independent finite checker instead evaluates full Euler--Maclaurin Laurent jets, including every subset image, on every pair at n=7,...,10.

Since sum_j r_j=0, sum_{j!=i}G_ij=-G_ii. With d+1 rays,


```text
sum_{i<j}alpha_2
  = C(d+1,2)/4+(d+1)/12
  = (d+1)(3d+2)/24.
```

Substituting d=k+1 proves (1.1). It is valid in the inherited metric; the cancellation is why the COMPLETE sum has this simple form. It is not a claim that individual BV constants transfer unchanged with rank. No new complete q5 field or exterior raw scalar census is computed.

## 5. The entire signed kernel is one-dimensional

This section gives an all-rank proof, not only finite kernel computations. At any four-cofacet obtained by removing p, exactly its two P partners occur; their primitive classes are opposite. Thus any signed balanced weights on the grammar agree on these partners. The same holds for the S signs.

Inside the stellar subdivision, the three subdivided cones must have equal weight: the new cofacets containing u and one or two of -a,v,w have only the corresponding two incident cones, with opposite primitive classes. The cofacet {p,s,v,w} then equates that common weight to the remaining cone {p,s,a,v,w}, because u=-a modulo span(v,w). Hence the subdivision can be undone for the purpose of balanced weights, not just for the unit assignment.

The analogous two-partner cofacets equate both a signs for every other circuit pair. After these equalities, weights correspond to values z_ij on unordered pairs of R. At ray r_i, the d other rays modulo r_i span dimension d-1 and have their unique linear relation with all coefficients one. The complete balance therefore says all z_ij with fixed i are equal. The complete graph of pairs is connected, so every z_ij has the same value. This applies to signed weights too. Conversely unit weights are balanced by Section3. The full signed kernel is exactly the line claimed in T2.

The independent checker regenerates ALL physical cofacets and every rational quotient equation for the finite n=7,...,10 controls and computes rank |C_n|-1 in a separate sparse echelon order. It also rejects padding the original56 weights to rank8 without changing support.

## 6. Base original parent and exact zero-set invariant

The n=7 base is the authenticated U10 parent, whose complete checker was rerun in U11. Its boundary is


```text
lambda=(12440,11144,10712,8552,8120,5852,3584),
mu=(6283,5851,4771,3403,2515,1519,1),
nu=(9625,8107,7129,5365,3565,2269,1), trace60404.
```

Its57 integral heights comprise one strict parent and56 face witnesses on ONE boundary. The parent has all63 slacks at least216. Each selected face has precisely its five seed rows zero, with only these possible extras:

    if {u,v,w} is present, a is also zero;
    if {a,v,w} is present, u is also zero.

There are exactly eight such extra-row instances, all explained by the literal identity rho_v+rho_w=rho_u+rho_a. No other zero row is suppressed. These identities do not add an independent interior normal. Every face has tight-normal rank five. The corresponding saturated kernel and its original Gram matrix are preserved.

The invariant for induction is this exact zero-set description, shared integral boundary, all other slacks positive integers, and a strictly feasible integral parent point on that boundary. It does NOT demand that every face's outer strip be strict: a selected path endpoint can be tight there. Only the shared boundary gaps need strict lower bounds, supplied by the strict parent.

## 7. New simultaneous collar: preserve the old cells and create the new endpoint pairs

Assume the invariant at rank n>=7. Put t_old=C(n-4,4), t_new=C(n-3,4). Scale every old height, including the parent, by SIX, giving one shared boundary6b.

Prepare a core on T_n for every new selected support:

1. If t_new is absent, use its six-scaled old face witness unchanged.
2. If t_new is present but t_old is absent, take the old witness with t_new replaced by t_old, scale by six, and DECREASE h(n-4,4) by one. This makes the old endpoint slack positive and leaves every other old seed/extra row unchanged.
3. If both endpoints occur, the new support is {p,s,epsilon*a,t_old,t_new}, epsilon*a represented by A01 or B11. Take THREE times the sum of the two old witnesses {p,s,epsilon*a,v,t_old} and {p,s,epsilon*a,w,t_old}. Their common zeros are exactly {p,s,epsilon*a,t_old}; every other slack is at least three. Decrease BOTH h(n-4,4) and h(n-5,4) by one. The old endpoint slack is unchanged, its predecessor (if present in the row system) increases, and every other nonzero slack changes by at most two. Thus all nonseed old rows stay strictly positive.

These cases are disjoint and exhaust the grammar at n+1. Case2 produces all one-endpoint replacements and pairs with any earlier path row; case3 supplies the eight new adjacent-endpoint cells. All affected coordinates are outside the fixed base rows (already at n=7 they have sums7 and6). Full original-row feasibility follows from the positive-margin bounds, not from selected-row tests alone.

Let H_i=h(i,n-i),0<=i<=n, be the shared OLD diagonal of the scaled parent, and a_i=H_i-H_(i-1). Its integral gaps g_i=a_(i-1)-a_i,2<=i<=n, are at least12: each is a sum of two strict parent slacks before the factor-six scaling.

Choose ONE new diagonal z_i=h(i,n+1-i) with consecutive differences


```text
d_i=a_i+1                 (1<=i<=n, i!=i0),
d_(i0)=a_(i0-1)-1,        i0=n-3,
d_(n+1)=a_n-1.
```

First integrate with z_0=0, then subtract a common integer K from EVERY z_i, large enough to make every new A row at least one for ALL prepared cores and the parent. There are finitely many cores; K is explicitly the maximum required loss plus one.

All new physical rows, indexed as in U02, are


```text
A_i=U_i-z_i,
B_i=d_i-a_i              (1<=i<=n),
C_i=a_(i-1)-d_i          (2<=i<=n+1).
```

For an unmodified core every B,C row is positive: B_(i0)=g_(i0)-1 and C_(i0)=1; the other interior values are1 or g_i-1, and endpoint values are1.

Every modified core has only its diagonal H_(i0-1)=h(n-4,4) lowered by one. Hence a_(i0-1) decreases by one, a_(i0) increases by one. Exactly C_(i0) becomes zero; B_(i0-1) increases, B_(i0) falls from g_(i0)-1 to g_(i0)-2>=10, and C_(i0+1) increases. No other B/C value becomes zero. The additional h(n-5,4) change in case3 is on the inner diagonal and affects only new A bounds, already handled by common K. The new zero row C_(i0) is precisely physical t_new.

Thus the prepared cores extend to hives with EXACTLY the desired seed/extra zeros. All old modified diagonal positions are now interior; old side boundaries were unchanged and the new diagonal is common. They have ONE new entire boundary. A common affine addition makes all final boundary parts positive without altering any slack. The strict parent remains strict. Actual parent dimension is D_(n+1); every selected face has dimension D_(n+1)-5 by the unit image proof and the exact zero sets. This proves the all-rank simultaneous ORIGINAL-PARENT realization invariant.

Every independent seed has universal closure rank exactly five: its closure lies in the full zero set of this feasible witness, which has rank five. No unperformed all-rank closure census is assumed.

The complete constructive data are independently checked at n=7,8,9,10:448 face heights and four parents. A separate bounded common-boundary solve at n=8 supplies an additional89-height exact degree21 witness; its numerical optimizer status is not used as a proof. These finite controls support the implementation. The infinite quantifier is the preceding induction.

## 8. One shared compatible positive generic refinement

At every rank the only extra zero rows are the fixed identity in Section6. Put a_u=2 and a_r=1 for every other physical row. Let


```text
B=2^m, M=8B+1,
delta_r=a_r+M^(-r-1),
eta=1/(16*m*B^2*3),
```

in the actual rank-n physical row order. Use ONE such delta and eta for every selected face.

A unit five-minor gives an integral right inverse Y_I supported on those five coordinate rows. Every inverse entry is a four-minor of normal rows of norm at most2, so is at most16 in magnitude. Set the original interior displacement to -eta Y_I delta_I. Each selected physical row becomes zero exactly. An extra row has margin

    delta_u+delta_a-delta_v-delta_w,

whose integer part is1 and whose perturbation tail is less than1/2. Every other original slack is at least1, while |n_r Y_I delta_I|+delta_r is bounded by963; the displayed eta is smaller than1/(2*963) for all m>=15. They stay strict.

Genericity and compatibility use the accepted finite-basis argument, with its hypotheses explicit. Primitive circuits have at most m+1 rows and coefficients bounded byB=2^m. The earliest inverse-power term dominates when c dot a=0; otherwise the integer part has absolute value at least1 and the tail is smaller than1/2. Thus c dot delta never vanishes. At an integral boundary every nonzero basis slack has magnitude at least1/B. The amplitude is strictly below1/(8*m*B^2*3), so an originally infeasible limiting basis cannot become feasible. The relaxation is bounded, nonempty, simple and compatible. All constructed selected cells are consequently positive-weight cells of ONE such refinement of ONE original parent.

The finite certificates retain all saturated kernels, their original Gram matrices, every extra-row relation and complete shifted-slack readback hashes. Those hashes bind vectors that the independent checker actually recomputes; they do not replace the positivity checks.

## 9. Open boundary regions, positive extraction, and the exact residual limitation

For each constructed rank-n parent b_n fix h00=0. There are3n-1 independent remaining boundary-height coordinates. For integer s>=1 and an integral perturbation z satisfying


```text
|z_j|<=s/2568,
```

put b=s b_n+z. At a selected face use interiors s x_I-Y_I R_(I,b)z; at the parent keep its scaled interiors. Every selected equation still holds exactly. All extra tight rows are FULL-HEIGHT combinations of its seed, so remain zero on every such perturbed boundary, not merely on the original boundary.

Here is a uniform conservative bound, chosen for proof rather than numerical sharpness. A right-inverse row has at most five entries of magnitude16. Every physical row has l1 norm at most4. Thus each row of

    R_b-N Y_I R_(I,b)

has l1 norm at most4+4*5*16*4=1284. Old positive slacks, scaled by s, are at least s; the new off-face margins are at least s/2. Parent variations are bounded by4s/2568. Boundary final parts were at least1 and adjacent gaps at least2; their variations are at most2s/2568 and4s/2568. Hence the three words remain strict positive partitions with exact trace and final ordinary rank n. This is a full-dimensional region of rational boundary heights; the displayed integral subfamily is obtained directly, and denominators can be cleared for other rational points.

All zero sets and their shared shift condition persist. The same delta and eta still preserve the off-face margins for s>=1. The parent is full-dimensional throughout this region.

For a unit five-minor, let K_I be the saturated kernel basis with identity on the m-5 free coordinate rows. Every pivot row has l1 norm at most16*20=320, so ||N_r K_I||_1<=1280 for every physical row. The parameter cube


```text
|u_j|<=s/5120, 1<=j<=m-5
```

therefore lies in each selected face: its possible loss is at most s/4 against margins at least s/2. Its saturated lattice volume is (s/2560)^(m-5), with no factorial normalization. Thus


```text
lambda_* >= (s/2560)^(D_n-5)>0
```

throughout the displayed boundary family. Unperturbed constructed parents also admit the slightly stronger bound1280^(-(D_n-5)). The numerical constants are conservative and not asserted sharp.

By the kernel theorem, any balanced subassignment supported on C_n is a scalar multiple of v_n. Nonnegativity and z<=w are exactly0<=lambda<=min w_I. This proves T2 and the positive extractable pairing. Multiple refined cells may carry the same full coarse-face volume; they are not assigned fractions of that volume or artificially set to one. The residual w-lambda_*v_n remains nonnegative and fully balanced, but its alpha pairing is UNSIGNED. A positive extractable summand is not a lower bound on the complete coefficient.


Full n=7..10 heights, induction records, saturated kernels, inherited Grams, common shifts and pair arrays are [U11-COLLAR-FAMILY.json](../data/a57/U11-COLLAR-FAMILY.json), [U11-GEOMETRY-FAMILY.json](../data/a57/U11-GEOMETRY-FAMILY.json) and [U11-SIMPLEX-PAIR-VALUES.json](../data/a57/U11-SIMPLEX-PAIR-VALUES.json). [check_u11.py](../code/a57/check_u11.py) checks every face, original/shifted row and restricted balance kernel.
