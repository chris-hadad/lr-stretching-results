# Full positivity in an arbitrary-row near-corner transportation/LR cone

Attempt: SLR-GPT6-PRO-FRONTIER-024-P07-A01-4820f3b5652d.
Parent SHA-256: d7f3bef6d35d68f70cc89e1159c537a677e4de0d321035707bb41e418d4459ce.
Status: provider hand proof with complete bounded combinatorial challenges. This is a sufficient whole family, not all transportation margins and not worldwide novelty or campaign acceptance.

## 1. Statement and exact all-t formula

Let m>=3, N>=2, a_1,...,a_m positive integers, A=sum_i a_i, and a_min=min_i a_i. Let c_1,...,c_N be positive integers with

    c_j>=A-a_min for every j,
    r_0=M-A>0,  M=sum_j c_j.

Take the complete (m+1)-by-N transportation polytope with row margins (r_0,a_1,...,a_m). Put D=m(N-1) and L_j=A-c_j. Its ENTIRE polynomial is

    P(t)=product_(i=1)^m binom(a_i t+N-1,N-1)
          -sum_(j: L_j>0) binom(L_j t+D-1,D).           (1)

Every ordinary coefficient through degree D is strictly positive. The entire LR rank under the complete bridge in proof 018 is m+N. All margins and exceptions are part of the hypothesis; columns with L_j=0 or L_j<0 contribute no subtraction.

The global cut theorem also applies: because A>=m a_min and m>=3,

    2 min_j c_j>=2(A-a_min)>=A.

Thus (1)'s c1 agrees with the symmetric cut formula. The all-coefficient conclusion below is strictly stronger than that c1 conclusion.

## 2. Count every table and every violation

Choose the m minor rows independently as weak compositions of a_i t into N entries. This gives the product in (1). The remaining row is uniquely determined by column subtraction. A choice is legal exactly when no minor-column total exceeds c_j t.

Two violated columns cannot coexist. Their total would be greater than

    (c_j+c_k)t>=2(A-a_min)t>=At,

the total of all minor entries. At t=0 there are no violations either. Thus ordinary inclusion-exclusion has only single-column terms: no signed higher intersections have been dropped.

For a violated column j, set u_i=a_i t-x_ij. Then u_i>=0 and

    sum_i u_i<=L_j t-1.

If L_j<=0 there is no such choice. Otherwise 0<L_j<=a_min. The upper bounds u_i<=a_i t are automatically satisfied by this displayed sum bound. The remaining N-1 entries of row i form a weak composition of u_i, counted by B_(N-1)(u_i). Adding a slack coordinate and applying the ordinary composition convolution gives

    sum_(sum u_i<=L_j t-1) product_i B_(N-1)(u_i)
        =binom(L_j t+D-1,D).

This is exact for every t>=1; its binomial polynomial also vanishes at t=0. It proves (1) for all stretches, with no eventual-to-initial gap.

## 3. A coefficientwise domination proof, not a numerator-sign shortcut

Let n=N-1. The product in (1) equals

    (1+a_min t) B(t),

where B is the product of the other D-1 positive linear factors a_i t/j+1, 1<=j<=n; remove the j=1 factor from one row of capacity a_min.

For 0<L<=a_min define

    C_L(t)=product_(k=1)^(D-1)(1+Lt/k).

Then

    B(t)>=_coeff C_L(t).                               (2)

To prove (2), order the D-1 slopes of B decreasingly. Its kth largest slope is at least a_min/k. If k<=n, before deletion each of the m rows supplies k slopes at least a_min/k; after deletion at least mk-1>=k remain. If k>n, every remaining slope is at least a_min/n>=a_min/k, and there are D-1>=k slopes. The kth slope is therefore at least L/k. Pair the ordered linear factors and multiply; coefficientwise comparison follows because all constants and slopes are nonnegative.

Moreover,

    binom(Lt+D-1,D)=(L/D)t C_L(t).

Let Lambda=sum_(j:L_j>0) L_j/D. Then

    Lambda<=N a_min/[m(N-1)]<a_min,                     (3)

since m>=3 and N>=2. Substitution into (1) gives the exact positive decomposition

    P(t)=B(t)+t[(a_min-Lambda)B(t)
                   +sum_(j:L_j>0)(L_j/D)(B(t)-C_(L_j)(t))].        (4)

B has strictly positive coefficients through degree D-1; (3) supplies a strictly positive coefficient of tB, including degree D. Equation (2) makes every remaining term nonnegative. Thus all D+1 coefficients of P are strictly positive.

Neither a positive h-star numerator nor pointwise count domination is being used as a substitute for coefficientwise domination. The latter is proved directly at the level of linear factors.

## 4. Lattice and whole LR interpretation

The positive-margin lattice, exact degree and full balanced ordinary LR triple are those in proof 018 Section 5, with p=m+1. Its tail constructor applies to all parameters in this theorem. In particular the claimed rank is m+N, not the number of minor rows or the incidence rank. This is an all-t whole count identity, not a supported face or a stabilized projection.

The historical three-minor-row and other small protected families remain closed at their own scopes. This theorem may overlap them; no overlapping control is credited as an independent discovery or new box coverage. Its stated generality includes an arbitrary number of nonuniform minor rows but imposes the displayed near-corner column bounds. Arbitrary four-minor-row or general transportation positivity does not follow.

## 5. A broader-cone challenge with an active deficiency bound

Rows (11,1,2,2), columns (3,3,3,3,4) lie in proof 018's cone but violate the stronger hypothesis here: A=5, a_min=1, and min c_j=3<4. It would be wrong to use (1) unchanged. Single-column inclusion-exclusion is still exact, since two violated columns would require more than 6t minor entries, exceeding 5t.

For a column of capacity 3, L=2. The unrestricted deficiency count is binom(2t+11,12), but the first deficiency u_1 is capped at t. In its violating part substitute u_1=t+1+v. Then v+u_2+u_3<=t-2, and expand

    B_4(t+1+v)=binom(t+v+4,3)
               =sum_(j=0)^3 binom(t+4,3-j)binom(v,j).

The other two rows and the slack coordinate contribute (1-z)^(-9). Summing the v binomials and then the inequality gives the exact correction

    E(t)=sum_(j=0)^3 binom(t+4,3-j)binom(t+7,9+j).

It is zero at t=0,1, as required by the empty tail. For the column of capacity 4 the unrestricted L=1 count has no lost deficiency bound. Hence the complete polynomial is

    P(t)=binom(t+4,4)binom(2t+4,4)^2
          -4binom(2t+11,12)+4E(t)-binom(t+11,12).        (5)

The missing +4E(t) shows exactly why (1) cannot be extended merely because single-column violations are still disjoint. B02 expands (5), finds all thirteen coefficients positive and c1=19/2, and obtains literal matrix counts 1072 and 71747 at t=1,2. These sites are checks of an all-t identity, not determining sites in an interpolation.

## 6. Exact controls and independence

B02 saves complete ordinary rational vectors, full balanced LR triples, degree and direct matrix checks for:

* Minor rows (1,1,1), columns (2,2,2,2,2): rank 8, degree 12, c1=35/6; counts 120 and 3310.
* Minor rows (1,2,3), columns (5,6,6,7): rank 7, degree 9, c1=98/9; counts 799 and 29390.
* Minor rows (1,1,1,1), columns (3,3,3,4): rank 8, degree 12, c1=85/12; counts 253 and 9961.
* The broader-cone challenge (5): rank 8, degree 12, c1=19/2; counts 1072 and 71747.

All four vectors are positive. Literal matrix enumeration does not use the bounded-composition subtraction formula. Both implementations use CPython exact integer/Fraction arithmetic; no second arithmetic engine or fresh bare LR tableau count is claimed. The whole-LR interpretation rests on the full inherited count map, not on relabeling a proper subset.

These positive results do not change additive campaign coverage 4554 and are not whole-rank classifications. General higher-class first jets, broader finite caps, and higher coefficients outside this cone remain open.
