# A59: every positive cap pattern at balanced budgets K-2

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation, 27 September 2026. The complete count bridge is the accepted
A58 balanced two-pair identity, independently rederived from Pro046 in
`methods/astra058-2026-09-27/root-science/FIRST-WALL-PROOF.md`, Section 2.
This new uniform reserve is A59 root work. ; no worldwide novelty claim is made.

## 1. Exact legal original and claim

Let a>=3, k_1,...,k_a>=1, K=sum k_i>=4, B=K-2, and s>=1 be integers.
Take a row-width list

    (u_1,v_1,s k_1,...,s k_a,u_2,v_2),

where all four paired widths are at least H=2sB. Only the first and last
adjacent pairs overlap, each by sB; all other overlaps are zero. Define
lambda_n=w_n, mu_n=0 and, upwards, mu_i=lambda_(i+1)-e_i,
lambda_i=mu_i+w_i. Set nu=(sum w_i-2H,H,H). Lambda is OUTER.

All partitions are legal: 0<=e_i<=min(w_i,w_(i+1)) gives both adjacent
partition inequalities and containment; sum w_i>=4H gives output dominance,
and balance is by construction. The last outer row is positive. Thus the
maximum trimmed original rank is a+4, with arbitrary cap order and unequal
paired widths within their floors. No unused row or physical inequality is
removed from this original.

Its whole stretched LR polynomial is P(s t), strictly positive in every
ordinary degree 0 through its actual degree 2a+2. The formula and proof below
apply to every positive cap pattern, not just (1^(a-1),2). Zero-width isolated
rows may additionally be inserted: they are retained in the physical original,
contribute h_0=1, and do not affect P. In that extension a counts positive
caps, the degree stays 2a+2, and the original rank is the total number of
listed cap rows plus four. The case with fewer than three positive caps is
outside this theorem. Common scaling means budgets s(K-2), not sK-2.

By the complete two-pair extraction, retaining its once-only Weyl shifts,


```text
P(t) = sum (Bt-U+1)(Bt-V+1),                         (1)
```

summed over u_i,v_i>=0, u_i+v_i<=k_i t, U=sum u_i<=Bt, V=sum v_i<=Bt.
Each weight is realized by two nonnegative slack variables with fixed sum;
eliminating one slack per budget gives the saturated lattice Z^(2a+2).
A strict interior exists since every cap and both budgets are positive.
The identity is an equality of entire original counts. No original-hive
metric isometry, face realization or local-weight transfer is inferred.

## 2. Full formula and all intersections

Write m=#{i:k_i=1}, S2=sum k_i^2 and


```text
N = product_i binom(k_i t+2,2),
L = 5K/4-4,
Q = (16(K-3)^2-S2)/36,
T = (Bt+1)binom(2t+2a-1,2a+1)
                     -a binom(2t+2a-1,2a+2),
C = (t+2)((B-1)t+2)binom(t+2a-3,2a)
      +(Bt+4)binom(t+2a-3,2a+1)
      +binom(t+2a-3,2a+2).
```

All binomials in these expressions are rational falling-product polynomials.
The COMPLETE polynomial is


```text
P = N(1+Lt+Qt^2)+2T-2mC.                            (2)
```

Here is a count proof, including why no unlisted intersections survive.
On each integer triangle u+v<=k t, the two means are kt/3 and their
covariance is -k^2 t^2/36-kt/12. Thus the unrestricted sum of the two
signed slack weights is N(1+Lt+Qt^2). Violations of both budgets cannot
coexist, because 2Bt+2>Kt for K>=4.

In a negative first-budget tail put x_i=k_i t-u_i-v_i. Its total residual
S=sum(x_i+v_i) is at most 2t-2, and the correction weight is
(2t-1-S)(Bt+1-V). The residual pairs still have every bound x_i+v_i<=k_i t.
If those pair caps are temporarily removed, the composition sum is T. This
identity follows by expanding V over the a symmetric v coordinates and
using the elementary composition and hockey-stick sums.

Every cap at least two is automatic since S<=2t-2. A unit-cap violation
has pair sum t+1+w. TWO such violations are impossible because their
sum would be at least 2t+2. For a chosen violated unit pair, writing r for
the other variables' total gives the exact correction


```text
sum_(w,r>=0; w+r<=t-3)
  (t+2+w) binom(r+2a-3,2a-3)
    ((2B-1)t+1-w-r)(t-2-w-r)/2.                    (3)
```

At n=w+r, its first multiplicity is
(t+2)binom(n+2a-2,2a-2)+binom(n+2a-2,2a-1).
Set g=t-3-n. The remaining weight is
(g+1)((B-1)t+2+g/2). The generating functions are therefore


```text
(t+2)/(1-z)^(2a-1)+z/(1-z)^(2a),
((B-1)t+2)/(1-z)^2+z/(1-z)^3.
```

Their coefficient at z^(t-3) is C. The early empty ranges also agree with
the polynomial binomials. There are m such cap corrections in each of two
disjoint budget tails. This proves (2), including every possible cap/budget
intersection and each integer endpoint. There is no independence assumption
between the two retained caps in the original count.

Dropping C is a false formula even though it agrees at t=1,2: at t=3
it overcounts by 10m(3B-1). This is an exact negative-formula control.

## 3. One coefficient reserve pays the entire correction

Use <=_c for coefficientwise inequality in ordinary powers of t and put
E_j(t)=product_(l=1)^j(1+t/l),


```text
D_a=2a(2a-1)(2a-2),    H_a=(2a+1)(2a+2),
f0=4-12/(2a+1)+12/H_a=2(2a-1)/(a+1),
f1=2B+(4-3B)/(2a+1)-7/H_a,
f2=B-1+B/(2a+1)+1/H_a.
```

Exact factorization gives


```text
C=E_(2a-3)(t)t(t-1)(t-2)(f0+f1 t+f2 t^2)/D_a.     (4)
```

For B>=2 and a>=3 all f_i are positive, f1<=2B and f2<=2B. Hence
f<=_c(1+t)(f0+2Bt). Also t(t-1)(t-2)<=_c t(t+1)(t+2).
The product bound


```text
E_(2a-3)(t)(1+t)^2(1+t/2) <=_c N                  (5)
```

holds already against N0=((1+t)(1+t/2))^a. After matching the extra
(1+t)^2(1+t/2), match j=1,...,a-2 to the remaining a-2 slope-one
factors and j=a-1,...,2a-3 to the remaining a-1 slope-one-half factors.
Each factor difference is nonnegative; product telescoping proves (5).
To avoid multiplying an inequality by a signed factor, first replace
t(t-1)(t-2) by t(t+1)(t+2), multiplying by the nonnegative E*f.
Only then replace f by (1+t)(f0+2Bt), multiplying by the now
nonnegative cubic. Equation (5) finishes the comparison:


```text
C <=_c (2/D_a) N t(f0+2Bt).                        (6)
```

For the other tail set A=B-a/(a+1)>0, F=(2a+1)/(a+1). Directly,


```text
2T=E_(2a-1)(2t) 2t(2t-1)(At+F)/(a(2a+1)).        (7)
```

The cubic coefficient outside E is positive, its linear coefficient is
-2/[a(a+1)], and its possible negative quadratic coefficient has magnitude


```text
tau=max(0,(2B(a+1)-10a-4)/(a(a+1)(2a+1))).
```

For a>=4, E_(2a-1)(2t)<=_c N0: pay the first slope-two factor with
(1+t)^2, j=2,...,a-1 with the remaining a-2 slope-one factors, and
j=a,...,2a-1 with the a slope-one-half factors. For a=3, K>=4 guarantees
at least one cap of size two or greater. N then dominates the factors with
slopes (2,1,1,1,1/2,1/2), which also pay E_5(2t), whose slopes are
(2,1,2/3,1/2,2/5). Dropping only the positive terms in (7) therefore gives


```text
2T >=_c -N(2t/[a(a+1)]+tau t^2).                  (8)
```

Combining complete expressions (2), (6), (8),


```text
P >=_c N(1+ell t+q t^2),
ell=L-2/[a(a+1)]-4m f0/D_a,
q=Q-tau-8mB/D_a.                                 (9)
```

For a>=4, m<=a yields ell>=23/30. Packing the cap sum into four
positive caps gives S2<=(K-3)^2+3. Also


```text
tau+8mB/D_a
  <= B(2/[a(2a+1)]+4/[(2a-1)(2a-2)]) <= 19B/126.
```

With r=K-4>=0, this proves


```text
q >= 2/63+(43/63)r+(5/12)r^2 >= 2/63.             (10)
```

For a=3,K>=5, m<=2 and S2<=(K-2)^2+2 give ell>=23/12. The corresponding
subtraction is at most 8B/35. With r=K-5>=0,


```text
q >= 991/1260+(871/630)r+(5/12)r^2 >0.             (11)
```

The remaining case a=3,K=4 is (1,1,2) up to ordering. In (4) f0=5/2,
f1=201/56,f2=73/56; use f<=_c(1+t)(f0+(73/56)t) instead of 2B.
Equations (6)-(9) then give ell=2/3 and q=481/2520, as in A58.

N has strictly positive coefficients in all degrees 0..2a. Equations
(9)-(11) therefore prove positivity through 2a+2, and (2) has no larger
degree. This proves the stated whole-original theorem and its actual degree.
For the unscaled count the exact first coefficient is


```text
c1=11K/4-4-2/[a(a+1)]-2m/[a(a^2-1)].              (12)
```

The all-unit a=4 original has c1=203/30. This is a uniform cap theorem on
the stated balanced budget family. Arbitrary budgets, more distant budget
walls, all multiple-cap absorber signs, whole rank seven and general KTT
remain open. The proof does not sign each tail or each fixed band separately.
