# Positive double-cut core of transportation c1 at arbitrary size

Phase 7, branch SLR-GPT6-PRO-FRONTIER-024-P07-A01-9739f13c17c5. Status: PROVED by provider derivation with exact
challenges, not independent campaign acceptance. This theorem concerns the
complete sum of assignments occupying at most two partial-fraction classes.
It does NOT discard the assignments occupying three or more classes.

## 1. Statement and scope

Let p,N>=2, r in Z_{>0}^p and c in Z_{>0}^N, with common total M.
Let F_{r,c}(t) count the ENTIRE nonnegative p-by-N transportation table with
row margins tr and column margins tc. For a proper nonempty subset S of [k], set

    w_k(S) = (|S|-1)! (k-|S|-1)! / (2(k-1)!).                  (1)

Write H_j=sum_{i=1}^j 1/i. Define

    D_{p,N}(r,c) = sum_{I,J proper nonempty} w_p(I) w_N(J)
                    min(r(I), M-r(I), c(J), M-c(J)).          (2)

In the full Lagrange partial-fraction expansion of product_j h_{tc_j}(x),
the sum of all one-class and two-class ordinary LINEAR contributions is
EXACTLY D_{p,N}. Consequently there is an exact decomposition

    [t]F_{r,c}(t) = D_{p,N}(r,c) + E_{>=3}(r,c),              (3)

where E_{>=3} is the sum of the eventual-polynomial first jets of every
assignment using at least three classes. No sign or vanishing of E_{>=3}
is asserted in general. The core itself satisfies

    D_{p,N} >= H_{p-1} H_{N-1} min(min_i r_i,min_j c_j)>0.    (4)

It is symmetric separately in rows and columns, symmetric under transposition,
homogeneous, jointly concave, and superadditive on the closed balanced
nonnegative margin cone. The minimum in (2) is exactly the length of a complete
2-by-2 transportation interval with row totals r(I),M-r(I) and column totals
c(J),M-c(J). Thus (2) is a positive weighted aggregation of actual small fibers,
not positivity inferred from an arbitrary signed numerator.

This yields a necessary negative mechanism: E_{>=3} must be less than -D.
A negative individual assignment term, or a negative correction to an unrelated
three-row ansatz, does not meet that condition.

## 2. Exact partial fractions and constant shifts

For all nonnegative k,

    h_k(x_1,...,x_p) = sum_i x_i^{k+p-1}/prod_{j!=i}(x_i-x_j).

This follows from partial fractions of prod_i(1-x_i z)^(-1), or Lagrange
interpolation; it is a rational identity before expanding in ordered ratios.
Expand positive roots x_j/x_i, i<j. If class i is used n_i times and carries
column total C_i, the sign is (-1)^{sum_i(i-1)n_i}, the root (i,j) has
multiplicity n_i+n_j, and its vertex netflow target is

    a_i=t(C_i-r_i)+(i-1)n_i-sum_{j>i}n_j.                  (5)

The sum of these targets is zero. This agrees with the full A3 convention in
inherited proof 009. For positive r_1, an assignment without class1 has negative
first netflow eventually and contributes zero. The one-class1 assignment is

    prod_{i=2}^p binom(r_i t+N-1,N-1),

whose linear coefficient is H_{N-1}(M-r_1).

For two occupied classes 1,j, write a=n_1>0,b=n_j>0,N=a+b and let C=c(J)
be the total of the nonempty proper column subset assigned to class1. Let
l=j-2, d=p-2. The l empty rows BEFORE j are intermediate vertices; the other
d-l empty rows are terminal vertices. Set B_s(x)=binom(x+s-1,s-1).
An intermediate row k has flow x+r_k t+b from 1 and flow x into j, with weight

    B_a(x+r_k t+b) B_b(x),       x>=0.                    (6)

The constant b is required by (5); omitting it is wrong. A terminal row k has
flow x from 1 and flow r_k t-x from j, with weight

    B_a(x) B_b(r_k t-x),         0<=x<=r_k t.             (7)

The direct core edge has weight B_N(z). Conservation at 1 reads

    z+sum x = (C-r_1-sum_{2<=k<j}r_k)t-(l+1)b.            (8)

This is a complete grouped flow count: every multiplicity group contributes
its full weak-composition count. There is no prescribed-support deletion.

## 3. Reflecting the terminal caps

Extend B_b(r_k t-x) as its polynomial to all x>=0. It vanishes at the first
b-1 outside integers. At x=r_k t+b+y, y>=0, it equals

    B_b(-b-y)=(-1)^{b-1}B_b(y).

Inclusion-exclusion over a subset S of reflected terminal rows therefore has
factor (-1)^{b|S|}. Let h=l+|S| and

    U=C-r_1-sum_{2<=k<j}r_k-sum_{k in S}r_k.

It has h factors of type (6), d-h factors of type (7) with the caps now removed,
and total composition size Ut-(h+1)b. If U<=0, that size is eventually negative
(including U=0), so the term is absent. This accounts for actual cap walls,
not just generic interiors. For U>0 apply the following polynomial identities.

The CORRECT rising-binomial Vandermonde identities are

 B_a(x+rt+b) B_b(x)
   = sum_{k=0}^{a-1} binom(rt+a-1-k,a-1-k)
                         binom(b+k-1,k) B_{b+k}(x),       (9)

 B_a(x) B_b(rt-x)
   = sum_{k=0}^{b-1} (-1)^k binom(rt+N-1,b-1-k)
                         binom(a+k-1,k) B_{a+k}(x).       (10)

For (9), take the coefficient of z^{a-1} in
(1+z)^{rt+a-1} sum_k binom(x+b+k-1,k)(z/(1+z))^k.
For (10), expand (1+z)^{rt+N-1}(1+z)^{-x-a}.
Multiplication by B_b(x), respectively B_a(x), then proves the displayed
composition identities. At t=0 the coefficient binomial in (9) equals ONE,
not binom(a-1,k). That distinction was caught by the fresh exact challenge;
the failed code and error disposition are retained. The selected proof uses
(9), and every subsequent finite beta check passes.

Let K be the sum of the chosen expansion indices. Summing all independent
compositions, including the core edge, gives the factor

 binom(Ut+(d-h+1)a+K-1, (d-h+1)a+(h+1)b+K-1).             (11)

At t=0 this binomial polynomial has a simple zero. Hence derivatives of the
other factors cannot affect the linear term. Its derivative has sign
(-1)^{(h+1)b-1} and absolute value

    U B((d-h+1)a+K,(h+1)b),                              (12)

where B(A,B)=(A-1)!(B-1)!/(A+B-1)!. Multiplying assignment sign
(-1)^{(l+1)b} and reflection sign (-1)^{|S|b} makes the final sign NEGATIVE.

## 4. Beta substitution eliminates all class multiplicities

Introduce polynomials

 Q_out(x)=sum_{k=0}^{b-1}(-1)^k binom(N-1,b-1-k)
                                      binom(a+k-1,k)x^k,
 Q_in(x)=sum_{k=0}^{a-1}binom(b+k-1,k)x^k.

Let I_x(a,b)=B(a,b)^(-1) integral_0^x u^{a-1}(1-u)^{b-1}du.
Finite binomial expansion or differentiation with the values at 0,1 proves

    x^a Q_out(x)=I_x(a,b),
    (1-x)^b Q_in(x)=1-I_x(a,b).                          (13)

Expanding (12) using its beta integral, the absolute normalized first jet is

 integral_0^1 x^{(d-h+1)a-1}(1-x)^{(h+1)b-1}
                 Q_out(x)^{d-h} Q_in(x)^h dx
 = integral_0^1 x^{a-1}(1-x)^{b-1}I_x^{d-h}(1-I_x)^h dx
 = B(a,b) integral_0^1 u^{d-h}(1-u)^h du
 = B(a,b) h!(d-h)!/(d+1)!.                               (14)

The substitution is legitimate since I_x increases continuously from 0 to1.
This is the sought ALL-a,b identity, not extrapolation from N=2 or4.
The complete reflected term's linear contribution is thus

    -U_+ B(a,b) h!(d-h)!/(d+1)!.                         (15)

It holds on the walls U=0 as well as both strict sides.

## 5. Sum assignments, then symmetrize

Each proper row subset I containing1 corresponds uniquely to j=min([p]\I)
and S=I intersect {j+1,...,p}. In (15), h=|I|-1 and U=c(J)-r(I).
Since B(a,b)=2w_N(J), the entire one/two-class sum is

 L2=H_{N-1}(M-r_1)
      -4 sum_J w_N(J) sum_{I proper,1 in I} w_p(I)(c(J)-r(I))_+.   (16)

Here every column assignment is counted exactly once. Define
F(s)=sum_J w_N(J)(c(J)-s)_+. Complementation gives

 sum_J w_N(J)=H_{N-1},
 sum_J w_N(J)c(J)=M H_{N-1}/2,
 F(M-s)=F(s)+(s-M/2)H_{N-1}.                              (17)

Also sum_{I:1 in I} w_p(I)=H_{p-1}/2 and, for i!=1,
sum_{I:1,i in I}w_p(I)=(H_{p-1}-1)/2. These follow by grouping subsets by size,
or by integrating their binomial sums in (1). Therefore

 sum_{I:1 in I}w_p(I)(r(I)-M/2)
       =M H_{p-1}/4-M/2+r_1/2.                           (18)

For 0<=s,C<=M,

 min(s,M-s,C,M-C)=C-(C-s)_+-(C-(M-s))_+.

Use this identity, (17), and (18) to expand (2). It is exactly (16).
This proves the positive double-cut identity, including both normalizations.

## 6. Positivity, LR bridge, and the unresolved term

Every proper row/column sum and its complement is at least the smallest
individual margin. Also sum_I w_p(I)=H_{p-1}, and similarly for columns.
This proves (4). A minimum of linear forms is concave; its positive sum (2)
is homogeneous and concave. Thus D(x+y)>=D(x)+D(y). These are statements
about the core's continuous extension, not a blanket identification of that
extension with every dimension-dropped boundary count.

The entire full transportation count has the inherited ordinary LR realization:
with R_i=sum_{k>=i}r_k and C_j=sum_{k>=j}c_k,

 lambda=(M+R_2,...,M+R_p,C_1,...,C_N),
 mu=(M repeated p-1 times,C_2,...,C_N),
 nu=(R_1,...,R_p).

These are partitions, balanced, and have maximum trimmed length p+N-1.
Its complete all-t character/count bridge is reproduced in
SOURCES/S13-TRANSPORTATION-PROOF.md, section2: the skew shape is a disjoint
component alpha plus horizontal rows; the Hall inner product removes the
full p-row rectangle and gives the coefficient of x^{tr} in product h_{tc_j}.
It is an entire count identity, not an asserted affine hive isomorphism.
The transportation lattice is saturated after deleting one redundant margin
equation: choose the first(p-1)(N-1) entries and reconstruct the others
integrally. Bipartite incidence is totally unimodular; ri*cj/M is strictly
positive. Hence degree=(p-1)(N-1), and F(0)=1. Zero rows/columns are deleted
before applying this positive-margin statement.

For general p,N, E_{>=3} remains a finite, precisely specified sum of first jets
from (5). The general full double-cut equality is CONJECTURED, not proved here.
The nonzero degree shift and saturated lattice do not remove this remainder.
For p=4,N=5, proof 018 checks ALL of the necessary higher-class gradients and
therefore obtains a whole-family theorem. Larger N and p remain distinct gates.

## 7. Verification and limitations

BETA-OUTPUT-V02.json contains 336 exact beta-integral checks (p=2..7,a,b=1..4,
all h) and 72 exact comparisons between (2) and (16). The binomial identities
were checked as exact polynomials, including parameters a>=3 that falsified
the earlier incorrect prefactor. The finite checks supplement the all-parameter
hand proof; they do not replace it. Mandatory 7/3,11/6,65/18 controls pass.

For the n-by-n unit-margin case the core reduces algebraically to

    D_n=sum_{k=1}^{floor(n/2)} (H_{n-k}-H_{k-1})^2.         (19)

This follows by writing the integer minimum as a sum of its level indicators.
The predictions agree with Pixton's published complete-polynomial linear
coefficients for n=2..9. This is a source comparison only. It does NOT prove
(19) is the full Birkhoff coefficient for arbitrary n, or that individual
higher-class terms vanish there. The general remainder may vanish only after
aggregation. No global novelty assertion or campaign acceptance is made.
