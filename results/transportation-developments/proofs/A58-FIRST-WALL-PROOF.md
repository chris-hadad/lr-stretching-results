# A58: strict whole-polynomial positivity beyond the first residual-cap wall

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

27 September 2026. Root derivation for the originating reconstruction.
This closes the uniform sign question left open in Pro046 U09-04 and retained
in its final U12 report. Pro046 originated the exact original family and its
corrected complete formula. The coefficientwise reserve below is root work.
; no novelty priority
or unrestricted KTT claim is made.

## 1. Complete original theorem

Let a >= 3 and s >= 1 be integers. Set H = 2(a-1)s. Choose four paired
row widths u1,v1,u2,v2 >= H and an arbitrary ordering of the a isolated
widths consisting of a-1 copies of s and one copy of 2s. Form the row list


```text
w = (u1,v1,k1,...,ka,u2,v2),       n = a+4.
```

Only the first and last adjacent pairs overlap, each by (a-1)s. All other
adjacent overlaps e_i are zero. Starting at the bottom, define


```text
lambda_n = w_n,    mu_n = 0,
mu_i = lambda_(i+1)-e_i,    lambda_i = mu_i+w_i,
T = sum_i w_i,    nu = (T-2H,H,H).
```

Lambda is OUTER. These are legal partitions, mu is contained in lambda,
and their sizes balance. Indeed 0 <= e_i <= min(w_i,w_(i+1)) proves both
partition inequalities, and T >= 4H proves output dominance. The last
outer part is positive, so the maximum trimmed original rank is exactly
a+4. Interior zero padding is not used to lower this rank.

The entire ordinary stretched LR polynomial is P_a(s t), where P_a is
defined below. It has actual degree 2a+2, constant one, and every ordinary
coefficient through that degree is STRICTLY positive. This is a theorem
for the stated all-size original family at every rank >= 7, not for all
originals at any of those ranks. In particular it is not whole-rank-seven
positivity. The four paired widths and the isolated ordering may vary as
specified; no general cap or overlap operation is inferred.

## 2. Independently checked complete character and lattice bridge

Write D=(1-x)(1-y), h_j=h_j(x,y), and R_j=h_j-xy h_(j-1), with negative
indices zero. Finite geometric sums give


```text
D h_L(1,x,y)=1-R_(L+1),
(1-y/x)R_j=x^j(1-y)-x^(-1)y^(j+1)(1-x).
```

Inside the FULL dominant extraction `[x^B y^C](1-y/x)`, B >= C, a term
R_j A with j>B vanishes for every nonnegative-power series A. This follows
separately for the two displayed monomials; it is not a weightwise removal.
For a paired component of widths U,V and overlap J, its Jacobi--Trudi
character is h_U h_V-h_(U+V-J+1)h_(J-1). Multiplication by D^2 leaves
R_J plus terms containing R indices strictly above B when U,V >= B and
J <= B. All +1 and +2 indices occur once.

The ordinary three-letter Schur extraction, with the complete skew character,
is [x^B y^C]D(1-y/x)s_(lambda/mu)(1,x,y). For the two separated pairs take
B=C=(p+q)t. Their entire original count becomes


```text
[x^((p+q)t)y^((p+q)t)] (1-y/x) R_(pt) R_(qt) Phi/D^3,
Phi = product_i h_(k_i t)(1,x,y).
```

For every symmetric nonnegative-power series S and P,Q >= 0,


```text
[x^(P+Q)y^(P+Q)](1-y/x)R_P R_Q S = [x^P y^Q]D S.
```

One direct verification uses R_P R_Q=R_(P+Q)+xyD h_(P-1)h_(Q-1).
Assume P<=Q. In the second product the coefficients of h_(P-1)h_(Q-1)
rise by one to P, remain constant, then fall by one. The (1-y/x)
difference cancels the two equal symmetric coefficient ranges of D S,
leaving (D S)_(P,Q)-(D S)_(0,P+Q). The first R term supplies the latter
coefficient. If either P or Q is zero, the second product vanishes and
the same result follows from the displayed two-monomial identity.

Thus the COMPLETE original count, for arbitrary retained caps, is


```text
C_22(t) = sum (pt-U+1)(qt-V+1),
```

where the sum is over all nonnegative (u_i,v_i) satisfying
u_i+v_i <= k_i t, U=sum u_i <= pt, and V=sum v_i <= qt.
Equivalently retain two nonnegative slack variables for each of the two
budgets. Eliminating one slack per budget gives the full saturated integer
lattice Z^(2a+2). At the present positive parameters there is a rational
strict interior, so the count domain has dimension 2a+2. No generic hive
metric, affine hive-face equivalence or weighted-cycle identity is asserted.
The equality transports entire counts and actual degree.

These identities independently rederive the selected count bridge of
Pro046 U05-01. For the theorem, p=q=a-1 and caps (1^(a-1),2); multiplying
all those parameters by s replaces t by s t. Paired-width changes only
change nu_1 and keep this full extraction unchanged within the proved floors.

## 3. Exact formula, retaining the missing cap correction

It suffices to take s=1. Put


```text
N_a(t) = binom(t+2,2)^(a-1) binom(2t+2,2),
L_a = (5a-11)/4,
Q_a = (2a-4)^2/9-(a+3)/36,
T_a(t) = ((a-1)t+1) binom(2t+2a-1,2a+1)
                 -a binom(2t+2a-1,2a+2),
B_a(t) = (t+2)((a-2)t+2) binom(t+2a-3,2a)
         +((a-1)t+4) binom(t+2a-3,2a+1)
         +binom(t+2a-3,2a+2).
```

All binomials are their rational falling-product polynomials. The whole
polynomial is exactly


```text
P_a = N_a(1+L_a t+Q_a t^2)+2T_a-2(a-1)B_a.          (1)
```

Here is a full count derivation, rather than a fitted formula. Uniformly over
the integer triangle u+v<=k t, the means are k t/3 and the mixed covariance
is -k^2 t^2/36-k t/12. Summing the unrestricted product of the two slack
weights therefore gives N_a(1+L_a t+Q_a t^2), since sum k_i=a+1 and
sum k_i^2=a+3. The two budget violations cannot coexist: their total would
be at least 2(a-1)t+2>(a+1)t for a>=3.

For a violation in the first budget, complement each u_i in its triangle.
The resulting 2a residual variables have total S<=2t-2 and correction
weight (2t-1-S)((a-1)t+1-V). Without residual pair caps, summing this
weight gives T_a by the elementary composition and hockey-stick identities.
The cap of size two is automatic. A unit residual pair can violate only
when its total is t+1+w. Two such violations cannot coexist. For a chosen
violating pair the remaining total is r, with w+r<=t-3, and its exact
weighted contribution is


```text
sum_(w,r>=0; w+r<=t-3)
  (t+2+w) binom(r+2a-3,2a-3)
  * ((2a-3)t+1-w-r)(t-2-w-r)/2.                     (2)
```

Summing first at w+r=n gives multiplicity
(t+2)binom(n+2a-2,2a-2)+binom(n+2a-2,2a-1). Put g=t-3-n.
The generating functions for this multiplicity and its remaining weight are


```text
(t+2)/(1-z)^(2a-1)+z/(1-z)^(2a),
((a-2)t+2)/(1-z)^2+z/(1-z)^3.
```

Their coefficient at z^(t-3) is exactly B_a. Empty early ranges give zero.
There are a-1 possible unit-cap violations in each of the two budget tails,
which proves (1), retaining every cap and every once-only endpoint. In
particular, omitting the final correction agrees at t=1,2 but errs at t=3
by exactly 10(a-1)(3a-4). A two-grade control cannot detect that omission.

## 4. A coefficientwise reserve for the complete correction

Write f <=_c g when every ordinary coefficient of g-f is nonnegative, and
write E_m(t)=product_(j=1)^m(1+t/j). Set


```text
D_a=(2a)(2a-1)(2a-2),    H_a=(2a+1)(2a+2),
f_0=(16a^2-4)/H_a = 2(2a-1)/(a+1),
f_1=(8a^3-2a^2+3)/H_a,
f_2=(4a^3-10a-5)/H_a,
f(t)=f_0+f_1 t+f_2 t^2.
```

Factoring (1)'s correction, exactly,


```text
B_a = E_(2a-3)(t) t(t-1)(t-2) f(t)/D_a.             (3)
```

All three f_i are positive. Choose C_a=73/56 at a=3 and C_a=2a at a>=4.
Direct substitution, or clearing the positive H_a, proves
C_a>=f_2 and C_a>=f_1-f_0. Hence f <=_c (1+t)(f_0+C_a t).
Also t(t-1)(t-2) <=_c t(t+1)(t+2). Finally


```text
E_(2a-3)(t)(1+t)^2(1+t/2) <=_c N_a.                 (4)
```

For an explicit factor matching in (4), remove the last three factors
on the left. The remaining factors of N_a have slopes
2, a-2 copies of 1, and a-2 copies of 1/2. Match them respectively with
1/j at j=1, j=2,...,a-1, and j=a,...,2a-3. Every difference is
nonnegative. Product-difference telescoping proves (4). Equations (3)-(4)
therefore pay the ENTIRE correction by


```text
B_a <=_c (2/D_a) N_a t(f_0+C_a t).                   (5)
```

For the other tail, let A=(a^2-a-1)/(a+1)>0 and C=(2a+1)/(a+1). Exact
factorization gives


```text
2T_a = E_(2a-1)(2t) 2t(2t-1)(A t+C)/(a(2a+1)).     (6)
```

The cubic coefficient in the factor outside E is positive; its linear
coefficient is -2/[a(a+1)]. Define


```text
tau_a=max(0,(2a^2-10a-6)/(a(a+1)(2a+1))).
```

We have E_(2a-1)(2t) <=_c N_a. Match its j=1 factor with slope 2,
j=2,...,a+1 with the a slope-1 factors, and j=a+2,...,2a-1 with
a-2 slope-1/2 factors; one positive factor remains. Dropping positive
terms of (6), then using this matching, proves


```text
2T_a >=_c -N_a(2t/[a(a+1)]+tau_a t^2).              (7)
```

Combining (1), (5), and (7), without assigning signs to individual tails,


```text
P_a >=_c N_a(1+ell_a t+q_a t^2),
ell_a=(5a-11)/4-4/[a(a+1)],
q_a=Q_a-C_a/[a(2a-1)]-tau_a.                         (8)
```

At a=3, ell_a=2/3 and q_a=481/2520. At every a>=4, ell_a>0;
Q_a>=19/12, 2/(2a-1)<=2/7 and tau_a<=1/a<=1/4, so q_a>=22/21>0.
The factors of N_a are strictly positive in every degree 0 through 2a.
Thus (8) proves strict positivity in every degree 0 through 2a+2, and (1)
has no larger degree. This proves the complete original theorem. As an
additional exact consequence,


```text
[t]P_a=(11a-5)/4-4/[a(a+1)].                         (9)
```

No positivity assertion for arbitrary signed endpoint terms was used. The
proof controls their complete joint subtraction and preserves the cap
correction that the short formula missed.
