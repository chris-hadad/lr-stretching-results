# A62 complete original operations and a rank-uniform unequal-budget reserve

Curated mathematical proof from **A62**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

27 September 2026. Root derivation from the accepted A58 complete C22 character/count bridge and A60 complete subset identity. No active provider theorem is a premise.  No worldwide novelty or unrestricted KTT claim is made.

## 1. Literal entire original and its lattice

Let a>=3, with positive integer isolated caps k_1,...,k_a, total K. Take nonnegative integer budgets P,Q, H=P+Q, and four paired widths u1,v1,u2,v2>=H (positive at all theorem instances below). The ordered row widths are (u1,v1,k_1,...,k_a,u2,v2). The first and last adjacent overlaps are P and Q; all others are zero. Construct upwards: lambda_n=w_n, mu_n=0, mu_i=lambda_(i+1)-e_i, lambda_i=mu_i+w_i. Set nu=(sum w_i-2H,H,H), lambda OUTER. The width floors imply all partition, containment and trace inequalities, and sum w_i>=4H ensures nu_1>=H. Rank is a+4 before any physical zero-row insertion.

A58 FIRST-WALL-PROOF Section 2 derives the complete identity, with both paired determinants and every once-only Weyl shift:


```text
C(k;P,Q;t)=sum (Pt-U+1)(Qt-V+1),
u_i,v_i>=0, u_i+v_i<=k_i t, U=sum u_i<=Pt, V=sum v_i<=Qt.  (1)
```

The two factors count two slack compositions. Eliminate one slack per budget to obtain the saturated lattice Z^(2a+2). When all caps and both budgets are positive there is a strict relative interior and actual degree 2a+2. Below we also exhibit a positive coefficient in that top degree. Isolated physical zero rows contribute h_0=1 to counting, retain their outer rows and physical rank, and may be reinserted after applying a theorem to the positive caps. Cap permutations, unequal legal paired widths, and common scaling retain (1). No generic hive-face isometry, metric or local-weight transport follows.

## 2. Exact all-cap splitting identity, and the remaining obligation

For balanced P=Q=B, K/2<=B<=K, put r=K-B. The accepted A60 formula (10) is


```text
C=N(1+Lt+Qt^2)+2 sum_J (-1)^|J| T_J^(a),
N=product binom(k_i t+2,2), L=5K/4-2r,
Q=(4(2K-3r)^2-sum k_i^2)/36.
```

Here J ranges over every cap subset of weight below r. Use Q only in this section for the quadratic coefficient, distinct from Section 1's second budget. T_J^(a) is exactly A60 (10), zero when its subset weight is >=r. Let one cap k=x+y be split, and J range over subsets of all unchanged caps. The COMPLETE correction difference is


```text
2 sum_J (-1)^|J| [T_J^(a+1)-T_(J+x)^(a+1)-T_(J+y)^(a+1)
   +T_(J+x+y)^(a+1)-T_J^(a)+T_(J+k)^(a)].             (2)
```

No small-cap intersection is omitted. All terms use their own actual dimension, elementary factors and once-only binomial offsets. With N_R the product on unchanged caps and N_xy=binom(xt+2,2)binom(yt+2,2), the unrestricted part of the gain is


```text
N_R xy t^2 [(5+3kt+xy t^2)(1+Lt+Qt^2)/4+N_xy/18].    (3)
```

Indeed N_xy-binom(kt+2,2)=xy t^2(5+3kt+xy t^2)/4, and the quadratic coefficient increases by xy/18. Equations (2)+(3) are a complete gain identity, not a sign theorem. Q>=0 and L>0 under the balanced hypotheses, so (3) is coefficientwise nonnegative; the remaining problem is its payment of (2). A61 pays the linear gain. Eight exact complete discriminators do not pay every higher coefficient.

## 3. All-cap balancing of two caps that cannot enter a tail intersection

Keep K,B,r fixed as in Section 2. Choose two caps x<=y with x,y>=r, and replace them by x'=x+s, y'=y-s for 0<=s<=(y-x)/2. The two new caps are also >=r. No subset of weight below r contains either chosen cap before or after the operation. Every correction in A60 (10), including every subset of the other arbitrarily small caps, is therefore unchanged.

Write S=x+y, v=xy, v'=x'y', Delta=v'-v=s(y-x-s)>=0, and N'_xy=binom(x't+2,2)binom(y't+2,2). The exact WHOLE gain is


```text
Delta t^2 N_R [ (5+3St+(v+v')t^2)(1+Lt+Qt^2)/4
                     +N'_xy/18 ].                  (4)
```

This follows by subtracting N_xy=1+3St/2+(S^2/2+5v/4)t^2+3Sv t^3/4+v^2 t^4/4 and using Q'=Q+Delta/18. Every coefficient is nonnegative. For positive caps and Delta>0 it is strictly positive in degrees 2 through 2a+2; constant and linear gains are zero. This proves a complete arbitrary-cap-count operation even when other caps have active simultaneous intersections. It does not sign its starting original if the remaining caps are arbitrary.

For fixed small caps <r, fixed number of large caps >=r and fixed K,B, repeated balancing starts at a vector with all but one large cap equal to r and the remaining large cap carrying their remaining total. Hence the whole polynomial is coefficientwise at least that of this concentrated large-cap base. Reorder caps as needed; every endpoint is a complete legal original, not a relaxed panel. When r=0 one may append zero slots for this fixed-slot balancing statement, with the physical-rank qualification in Section 1.

## 4. A complete asymmetric chamber without residual cap intersections

Return Q to its meaning as the second budget. Set r=K-P, s=K-Q and d=max(r,s). Assume


```text
a>=3, 0<=r,s<=min_i k_i, d>0.                       (5)
```

Thus every cap is at least d, K>=ad, and P,Q>=K-d>0. Both negative budget tails are disjoint, since P+Q=2K-r-s>=K. In a negative U tail, complement u_i inside its original triangle. The residual total is at most rt-2. Since k_i>=r, every original residual pair cap is automatically satisfied, including equality. The same argument holds for s on the other side. There is no discarded cap or simultaneous budget intersection in this chamber.

Put E_m(z)=product_(j=1)^m(1+z/j), N=product_i binom(k_i t+2,2), and


```text
L=P+Q-3K/4=5K/4-r-s,
A=(P-K/3)(Q-K/3)-sum_i k_i^2/36,
F=(2a+1)/(a+1),
T_r(Q)=r t(rt-1)E_(2a-1)(rt)
          [F+(Q-ar/(2a+2))t]/[2a(2a+1)].
```

A zero deficit contributes zero. The ENTIRE polynomial is


```text
C=N(1+Lt+At^2)+T_r(Q)+T_s(P).                       (6)
```

For completeness, unrestricted averaging in each triangle gives E(u)=E(v)=k_i t/3 and Cov(u,v)=-(k_i^2 t^2+3k_i t)/36, yielding the first term. On a negative U tail, if residual total is S then exact u/v interchange averages V to S/2, so the correction weight is (rt-1-S)(Qt+1-S/2). Summing every weak composition gives


```text
[2+(Q-r/2)t] binom(rt+2a-1,2a+1)
                   +binom(rt+2a-1,2a+2)=T_r(Q).
```

This identity includes early empty ranges and the zero deficit. The second tail is symmetric. Thus (6) holds at every integer grade and is a polynomial identity.

## 5. A uniform reserve pays the entire two-tail correction

Factor matching gives E_(2a-1)(rt)<=_c E_(2a-1)(dt)<=_c N and likewise for s. Match the first a factors with the a slope-d factors of binom(dt+2,2)^a, and the remaining a-1 with slope d/2; one positive half-slope factor remains. Each actual cap k_i>=d only increases its factors.

The linear coefficient outside E in T_r is -r/[2a(a+1)]. Its quadratic coefficient is at least -rQ/[2a(2a+1)] and its cubic coefficient is nonnegative, because Q-ar/(2a+2)>0 under (5). Therefore


```text
T_r(Q)+T_s(P)
  >=_c -N [ d t/[a(a+1)] + dK t^2/[a(2a+1)] ].      (7)
```

Here r+s<=2d, rQ+sP<=d(P+Q)<=2dK. Put z=K-ad>=0. Concentrating the nonnegative excess k_i-d into one cap proves


```text
sum k_i^2 <= (d+z)^2+(a-1)d^2.
```

Consequently


```text
A >= [(16a^2-49a+36)d^2+(32a-50)dz+15z^2]/36.
```

For a>=3, the first coefficient is at least 11/12 and the mixed coefficient at least 23/18. Subtracting the quadratic loss in (7) uses 1/(2a+1)<=1/7 and 1/[a(2a+1)]<=1/21. The full reserve is


```text
C >=_c N [1+(5d/3+5z/4)t
             +(65d^2/84+155dz/126+5z^2/12)t^2].     (8)
```

Every displayed coefficient is positive when d>0. N is strict through degree 2a, so every ordinary coefficient of the COMPLETE original through actual degree 2a+2 is strictly positive. This theorem covers arbitrary integer cap magnitudes above d and unequal budgets; it is not restricted to scaling one cap pattern or to one deficit. It is a family theorem at unbounded original rank, not whole-rank positivity.

If d=0, P=Q=K and both bounds are redundant except for their exact slack factors. Formula (6) has no tail. L=5K/4>0 and A=(16K^2-sum k_i^2)/36>0 for K>0, giving the same strictness directly. No division by d is used. If every cap is zero and both budgets zero, the count is the point polynomial 1; physical rows are not deleted to infer rank.

## 6. A paid whole-original generator through every ordinary degree

Fix a>=3 and deficits r,s with d=max(r,s)>0. Starting from k_i=d, choose each target k_i>=d by successive integer increases of individual caps, increasing BOTH budgets by the same amount. Thus r,s stay fixed. Four paired widths may be held at the final target floor P+Q; all intermediate originals remain legal by Section 1. The nonnegative integer sum(k_i-d) decreases in the reverse direction, so this is a terminating reduction to an explicitly paid entire starting original.

For continuous parameters inside (5), write N_j=partial_(k_j)N. Differentiating the complete identity at fixed r,s gives


```text
partial_j C = N_j(1+Lt+At^2)+N[(5/4)t+A_j t^2]
                   +t binom(rt+2a-1,2a+1)
                   +t binom(st+2a-1,2a+1),
A_j=(16K-12(r+s)-k_j)/18.
```

The two derivative tails are bounded below by -d t^2 N/[a(2a+1)], using the same exact factor matching. Since k_j<=d+z,


```text
A_j-d/[a(2a+1)] >= 155d/126+5z/6>0.                (9)
```

N_j=(3t/2+k_j t^2)product_(i!=j)binom(k_i t+2,2) has positive coefficients in every degree 1..2a. Also L,A>0. Thus partial_j C is strictly positive in every degree 1..2a+2, and has zero constant. Integrating each coefficient over any positive increment proves the full coefficientwise gain, retaining integer endpoints as literal LR originals. This is a proof of a legal paid original operation, not monotonicity deduced from count inclusion or a finite panel.

## 7. Limits and verification obligations

Section 3 retains arbitrary other small caps but pays only the stated balancing gain. Sections 4–6 sign a complete infinite chamber and generator, but require every cap at least the larger deficit. In particular, they do not pay active residual cap intersections. The general all-cap split gain (2), arbitrary-cap higher signs in the balanced high-budget region, lower joint-budget tails, no-absorber/interacting originals, whole rank seven and unrestricted KTT remain open. A negative gain would refute an operation, not automatically an original or KTT.

Exact checks must cover (2), (4), (6) and (8)–(9); all determining and unused grades on named complete originals; unequal budgets, cap equality, d=0, inserted zero rows, permutation, legal paired-width changes and common scaling; and invalid omitted-intersection, below-floor or wrong once-only-shift controls. All finite results and prices remain separate from the quantified proof.
