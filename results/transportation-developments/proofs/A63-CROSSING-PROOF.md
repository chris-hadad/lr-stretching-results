# A63: a complete paid crossing of the first residual-cap wall

Curated mathematical proof from **A63**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

27 September 2026. Root derivation. No active provider theorem is a premise. The complete character bridge is the accepted A58 FIRST-WALL-PROOF Section 2; the subset derivation extends A60 Section 6. No worldwide novelty claim.

## 1. Complete original and exact scope

Use a separated two-pair C22 original with a isolated caps k_i, K their total, budgets P=K-r, Q=K-s and H=P+Q. Both deficits are nonnegative. Its ordered row widths are (u1,v1,k_1,...,k_a,u2,v2), with all four paired widths at least H, first/last overlaps P,Q and every other overlap zero. Construct upwards by lambda_n=w_n, mu_n=0, mu_i=lambda_(i+1)-e_i, lambda_i=mu_i+w_i; nu=(sum w_i-2H,H,H), lambda OUTER. These are legal partitions with exact trace. Every original row and both paired determinants are retained.

The ENTIRE original is


```text
C(k;r,s;t) = sum (Pt-U+1)(Qt-V+1),
u_i,v_i >= 0, u_i+v_i <= k_i t, U=sum u_i <= Pt, V=sum v_i <= Qt. (1)
```

Two slack compositions give the two weights. Eliminating one slack per budget leaves the saturated lattice Z^(2a+2) when all caps and budgets are positive. The count has a strict rational interior then and actual degree 2a+2. A physical zero cap contributes h_0=1 without removing the outer row; with precisely one zero cap the degree is 2a. No hive metric or facewise weight map is inferred.

The proposed sign/generator theorem assumes 3 <= a <= 8, d=max(r,s)>0, one distinguished cap x>=0 and every other cap at least d. The distinguished cap may cross either deficit. Increasing x while increasing BOTH budgets by the same amount, keeping r,s fixed and other caps fixed, has a strictly positive whole gain in every degree 1..2a+2 for every positive increment with positive endpoint. Constant gain is zero. The entire endpoint is strictly positive through actual degree. This is an all-magnitude, unequal-budget theorem at physical ranks 7..12 before extra zero-row insertion, not a finite sample or arbitrary-rank theorem. For x>=d the already accepted arbitrary-rank A62 theorem applies; this manuscript's new work is 0<=x<=d and its complete boundary joining. The d=0 chamber remains A62's separate no-tail result.

## 2. Complete all-cap correction and operation identity

For arbitrary positive caps with r,s>=0 and r+s<=K, put


```text
N=product binom(k_i t+2,2),
L=5K/4-r-s,
A=(2K/3-r)(2K/3-s)-sum k_i^2/36.
```

For a deficit h (r or s), other budget W (Q or P), and EVERY subset J of cap weight M_J<h, let q=|J|, z=(h-M_J)t+2a-2q-1, and e_l the elementary polynomial in (k_i t+2), i in J. Set


```text
T_J(h,W) = sum_(j=0)^q e_(q-j)
  [(2+(W-h/2)t) binom(z,2a-q+j+1)+binom(z,2a-q+j+2)].
```

The exact whole polynomial is


```text
C=N(1+Lt+At^2)
   +sum_(J:M_J<r)(-1)^|J| T_J(r,Q)
   +sum_(J:M_J<s)(-1)^|J| T_J(s,P).                (2)
```

Unrestricted triangle averages give N(1+Lt+At^2). The negative U and V tails are disjoint because P+Q>=K. Complementing a U tail gives residual total <=rt-2 and weight (rt-1-S)(Qt+1-S/2). Inclusion-exclusion of EVERY violated residual pair cap yields the displayed binomial sum; each cap violation shifts by k_i t+1 exactly once. V is symmetric. Early empty ranges are zero, and equality M_J=h contributes zero. This is A60's complete argument with the other budget retained separately, not an extrapolation of A62's no-intersection formula. A nonpositive deficit gives no tail. In the stated positive-cap domain, r,s<=K so no full subset enters.

Thus for a fixed-deficit increase x -> x+ell, K,P,Q all increase by ell. Subtract the full expression (2) at its two endpoints, with each endpoint's own subset roster. This gives an exact all-cap operation identity at arbitrary a. Subsets containing x may leave a tail as x increases; all other subsets remain and their W factor changes. No gain sign is asserted for arbitrary other small caps. A negative operation gain would not itself be a negative LR original.

## 3. First active-cap reduction

By symmetry take r=d>=s. All other caps are >=d, so the only possible nonempty tail subset is the singleton containing x. Write scaled variables X=xt, R=rt, S=st, Kt=K*t. Define


```text
B_m(Y)=binom(Y+m,m), b(Y)=binom(Y+2,2),
T_a(R,W)=(2+W-R/2)binom(R+2a-1,2a+1)+binom(R+2a-1,2a+2),
V_a(R,W,X)=(2+X)(2+W-R/2)binom(R-X+2a-3,2a)
   +(4+X+W-R/2)binom(R-X+2a-3,2a+1)
   +binom(R-X+2a-3,2a+2).
```

Here W is also a scaled budget. The whole scaled polynomial is


```text
F=N[1+5Kt/4-R-S+(2Kt/3-R)(2Kt/3-S)-sum(k_i t)^2/36]
  +T_a(R,Kt-S)+T_a(S,Kt-R)
  -1_(X<R)V_a(R,Kt-S,X)-1_(X<S)V_a(S,Kt-R,X).       (3)
```

The common binomial tops are below the lower indices when their slope is zero; hence V=0 at X=R or X=S. The polynomial pieces agree on each wall; their one-sided derivatives need not agree. Only continuous coefficient functions, which follow directly from (3), are used in integrating the piecewise derivative. All widths remain legal by holding paired widths at the final H floor.

There are exactly two new chambers: 0<=X<=S<=R, and 0<=S<=X<=R. On each differentiate F with respect to X while holding R,S and all other caps fixed. The actual derivative with respect to x is t times this scaled derivative. The derivative includes changes to BOTH budgets and every active singleton.

## 4. Complete finite certificates for infinite parameter chambers

Let every other scaled cap be R+Z_i, Z_i>=0. Terms in the tail correction are at most affine in the entire excess vector Z_i. Consequently terms of total Z-degree at least two in the derivative come entirely from the unrestricted derivative


```text
N_R [(3/2+X)(1+L+A)+b(X)(5/4+(16Kt-12(R+S)-X)/18)], (4)
```

where N_R=product_(i!=x)b(R+Z_i), Kt=X+(a-1)R+sum Z_i. For a>=3, each factor in (4) has nonnegative coefficients in X,R,R-S,Z_i. In particular, at S=R the constant large-cap part of A has R^2 coefficient [4(2a-5)^2-(a-1)]/36, positive for a>=3; all X/excess-square and mixed coefficients are positive. Reducing S only increases L,A and the derivative factor with nonnegative coefficients. Thus every Z-degree at least two is paid for all a>=3.

Only Z-degree zero and one require a finite certificate. By permutation symmetry among the a-1 large caps, one representative excess Z suffices. Retain only degrees 0 and 1 in Z, with caps (X,R,...,R,R+Z). Expand the exact derivative of (3), then substitute:

- Both singletons active: X=u, S=u+v, R=u+v+w.
- Only the larger-deficit singleton active: S=u, X=u+v, R=u+v+w.

All u,v,w,Z are nonnegative. The crossing certificate records EVERY rational coefficient of u^i v^j w^k Z^l, l=0,1, for each a=3,4,5,6,7,8 and both chambers. Zero coefficients are included by the declared full exponent domain, even when sparse storage omits them. Every coefficient must be nonnegative. This is twelve entire polynomial identities over four variables, not interpolation at sampled cap patterns.

For strictness, the both-active certificate has a positive pure-u coefficient in every parameter degree 0..2a+1. The one-active certificate has positive pure-u and pure-v coefficients in those degrees. When x>0, these furnish a positive derivative in every ordinary degree 1..2a+2. Other nonnegative parameters and arbitrary large-cap excesses cannot reduce it. Integrating each coefficient over x across both chambers and then the accepted A62 chamber proves the gain, including ties and crossings. The starting x=0 original is already paid: for a>=4, A62 applies to a-1 positive caps while the zero row survives. For a=3, substitute r=u+v, s=u, k1=r+z1, k2=r+z2 in the complete two-positive-cap no-intersection formula (2). The separate ZERO-BASE-CERTIFICATE-v1.json records all 200 nonzero rational coefficients through total degree 6, all positive, with every omitted coefficient exactly zero. Positive pure-u and pure-v support occurs in every degree 0..6. Since d=r=u+v>0, this pays the entire two-positive-cap count. Multiplication by the physical zero row h_0=1 preserves that count and its degree 6 in the literal seven-row original. No general rank-six theorem is needed as a premise. The reverse operation terminates at x=0, followed for a>=4 by A62's paid reduction of the other caps to d. No fixed-degree claim at the zero cap is made.

The independent verifier must regenerate these identities without importing the producer's polynomial implementation, verify the full exponent domain and strict supports, and match complete original/count vectors including unused grades. Its report controls whether the proposed certificate passed. Exact executed producer versions and all failures are retained.

## 5. Uniform-rank attempt and limits

A root attempted an all-a absolute envelope using E_n(y)=product_(j=1)^n(1+y/j), n=2a-3, the bounds E_n(y)<=_c b(dt)^(a-2)(1+dt/n) and E_n'(y)<=_c ((n+1)/2)b(dt)^(a-2), and the full signed singleton derivative. The bound separates positive and negative falling-factor pieces and loses their high-degree cancellation at x=0. The exact envelope probe retains negative pure-gap degree-five coefficients for every tested threshold a0=3..16. This rejects that particular envelope; it neither refutes cap-growth nor gives a negative original. The complete chamber certificate is a rigorous bounded-a replacement, not evidence of a proved all-a result. An all-a cancellation-preserving recurrence is a serious successor competitor to more active small caps.
