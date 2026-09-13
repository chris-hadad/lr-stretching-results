# Two-column transportation cut theorem and the first two-sided case

This AI-assisted proof uses the complete
[transportation/LR bridge](transport-whole-lr-bridge.md). The inherited source proves the positive
linear-coefficient formula for three positive rows and arbitrary positive
columns. The result below is a separate two-column derivation. Together with
matrix transposition they force a structural threshold for any negative
transportation linear coefficient.

## 1. Exact two-column count

Let p>=2. Let r=(r_1,...,r_p) be strictly positive integral row margins, let
A,B be strictly positive integral column margins, and put

    M=sum_i r_i=A+B.

Let F(t) count all nonnegative integral p-by-2 matrices whose margins are
tr and (tA, tB). Since the full transportation constraint matrix is totally
unimodular and the positive matrix r_i(A,B)/M is relatively interior, F is an
Ehrhart polynomial of exact degree p-1 in the saturated solution lattice.
The complete LR construction in the transportation/LR theorem realizes this same F as an entire ordinary
LR stretch polynomial of ordinary rank p+1.

Write x_i for the entry of row i in the first column. The second entry is
tr_i-x_i, so the entire fiber is exactly

    0 <= x_i <= t r_i,
    sum_i x_i=tA.

For S subset [p], put r(S)=sum_(i in S) r_i and s=|S|. Ordinary bounded-
composition inclusion-exclusion gives, for every sufficiently large integer t,

    F(t)=sum_{S: r(S)<A} (-1)^s
          binom((A-r(S))t+p-1-s,p-1).                 (1)

Terms with r(S)>A are literally absent for all sufficiently large t. If
r(S)=A and S is nonempty, the top argument p-1-s is below p-1, so that term
is zero. Since both sides of (1) are polynomials and agree for infinitely many
t, (1) is an identity of the Ehrhart polynomial. No continuation of an
individual excluded term is being interpreted as a small-stretch count.

## 2. Extract the ordinary linear coefficient

Put d=p-1 and H_d=sum_(j=1)^d 1/j. The empty-set term is

    binom(At+d,d)=product_(j=1)^d(1+At/j),

so its linear coefficient is A H_d.

For a nonempty proper S, 1<=s<=d, the polynomial

    binom(ut+d-s,d),   u=A-r(S)>0,

has exactly one zero factor at t=0. Its ordinary linear coefficient is

    u (-1)^(s-1) (d-s)!(s-1)!/d!.

Multiplying by the inclusion-exclusion sign (-1)^s makes every nonempty
survivor contribute negatively. Therefore

    [t]F(t)=A H_(p-1)
      - sum_{empty!=S proper [p]}
        alpha_S (A-r(S))_+,                            (2)

where

    alpha_S=(|S|-1)!(p-|S|-1)!/(p-1)!.

The complement has the same alpha. Moreover

    sum_{empty!=S proper[p]} alpha_S = 2 H_(p-1).      (3)

Indeed the total contribution of subsets of size s is
p/[s(p-s)], and 1/[s(p-s)]=(1/p)(1/s+1/(p-s)).

Average (2) with its complement-indexed copy. Since r(S^c)=M-r(S) and
B=M-A,

    [t]F(t)
      = (1/2) sum_S alpha_S
          [A-(A-r(S))_+-(r(S)-B)_+].                  (4)

The bracket is exactly

    min(A,B,r(S),M-r(S)).

This can be checked in the four regions r(S)<=min(A,B), B<r(S)<A,
A<=r(S)<=B, and r(S)>=max(A,B), with the middle region appropriate to the
ordering of A and B. Hence the symmetric cut formula is

    [t]F(t)=sum_{empty!=S proper[p]} beta_S
       min(A,B,r(S),M-r(S)),                           (5)

    beta_S=(|S|-1)!(p-|S|-1)!/[2(p-1)!] > 0.

Every minimum is strictly positive under the stated positive-margin
hypotheses. Thus

    [t]F(t)>0.                                         (6)

In fact, because sum_S beta_S=H_(p-1),

    [t]F(t) >= H_(p-1) min(A,B,min_i r_i) > 0.         (7)

This lower bound is not asserted sharp in every margin class.

## 3. Consequence for all transportation polytopes with a small side

The three-row theorem proves [t]F>0 for three positive rows and arbitrary
positive columns. Transposition preserves the complete transportation count,
so the same theorem protects three positive columns and arbitrary positive
rows. Formula (5) protects two positive columns and, after transposition, two
positive rows.

Therefore:

> Every full positive p-by-N transportation Ehrhart/LR polynomial with
> min(p,N)<=3 has strictly positive ordinary linear coefficient.

The complete transportation/LR bridge has ordinary rank p+N-1 and exact degree
(p-1)(N-1). Consequently every positive transportation polynomial whose bridge
has ordinary LR rank six has c1>0: the possibilities are 2-by-5, 3-by-4,
4-by-3 and 5-by-2, all covered above.

The first full transportation class not covered by this small-side theorem is
4-by-4. Its complete LR bridge has ordinary rank seven and degree nine. This is
a structural threshold only for the transportation mechanism. It does not say
that generic rank-six LR c1 is settled, nor that rank-seven transportation c1
can be negative.

If a row or column margin is zero, delete it before applying the theorem and
recompute degree and ordinary rank. The positive-margin bridge and the rank
statement must not be applied unchanged to a dimension-dropping zero margin.

## 4. Why this answers the four-row fixture without a naive formula

For r=(1,1,1,1), (A,B)=(2,2), formula (5) gives

- four singleton cuts, each weight 1/6 and minimum 1: total 2/3;
- six two-two cuts, each weight 1/12 and minimum 2: total 1;
- four three-one cuts, again total 2/3.

Thus [t]F=7/3, exactly the source fixture. The old attempted four-row
substitution into the three-row *column-subset* formula gives 2. The correct
answer at two columns is controlled by a row-cut formula instead. This explains
the fixture without pretending that the three-row assignment cancellation
extends unchanged.

For the same rows and (A,B)=(1,3), every minimum in (5) equals 1, so
[t]F=H_3=11/6, whereas the same naive column formula gives 2. Hence the
correction relative to the naive formula is +1/3 at (2,2) but -1/6 at (1,3).
There cannot be a universal representation

    exact c1 = naive three-row extension + nonnegative connected correction.

The connected correction already changes sign inside this simplest four-row
family. Any general A3 formula must retain the full interaction, not merely add
a positive error term to the A2 cut formula.

## 5. Verification extent

`DATA/PHASE3/TWO-COLUMN-CHECK-RESULTS.json` uses a literal bounded-composition
counter on twelve frozen p-by-2 cases with p=2,...,7. The prior degree p-1 was
used; t=0,...,d determine each vector and t=d+1,d+2 are unused holdouts. Every
reconstructed c1 equals (5), and all 24 holdout occurrences agree.

This computation shares CPython integer/Fraction arithmetic with the other
checks but is combinatorially independent of the inclusion-exclusion derivative
proof. It is not an additive LR coverage increment and does not independently
reprove the transportation/LR bridge.
