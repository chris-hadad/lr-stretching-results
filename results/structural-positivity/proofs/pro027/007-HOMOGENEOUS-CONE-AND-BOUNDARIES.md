# A complete homogeneous rank-six cone with forty positive joint coefficients

Claim FR027-P02-T004. This is a whole-family theorem, not a whole-rank theorem. Its main cone is larger than common dilations of integer x,y members: arbitrary nonnegative integral excesses need not be divisible by the base parameter.

## 1. Bare cone and full LR interpretation

For integers s,a,b>=0 define

    lambda=(27s+3a+9b,21s+2a+7b,15s+a+5b,9s+3b,6s+2b,3s+b),
    mu=(21s+2a+7b,15s+a+5b,9s+3b,6s+2b,3s+b),
    nu=(9s+2a+2b,7s+a+2b,5s+2b,4s+2b,2s+b).

Trim trailing zeros. These are balanced nonnegative partitions: outer size81s+6a+27b, inner sizes54s+3a+18b and27s+3a+9b. The complete tail lift gives the all-stretch Kostka identity with top nu and content

    beta=(6s+a+2b,6s+a+2b,6s+a+2b,3s+b,3s+b,3s+b).

The ordinary rank is six when s+b>0, three when s=b=0<a, and zero at the empty origin. No minimum-rank claim is made.

The exact ENTIRE polynomial is

    P_(s,a,b)(t)=P11(st)+(a+b)t Q1(st)+ab t^2 R(st).       (1)

Proof006 specifies all three full positive factors. In particular the count H(s,a,b)=P_(s,a,b)(1) has exactly40 nonzero ordinary monomials, all with positive rational coefficients:11 from P11(s), ten each from aQ1(s),bQ1(s), and nine from abR(s). No terms collide across those four supports.

## 2. Why(1) holds for independent widths, not only integer ratios

At a fixed stretch put T=st,A=at,B=bt. First suppose T>0. The first-block deficit simplex is |u|=3T. Its exact multiplicity is m_A(u)+1 when m_A>=0, where

    m_A=min(2T+A-u1+u2,2T+A-u2+u3,3T+A-u1,T+A+u3)
        =T+A+m0(u),
    m0=min(T-u1+u2,T-u2+u3,2T-u1,u3).

The entire detached tail F_B(u) has bottom shape

    (5T+2B,4T+2B,2T+B)/(5T+2B-u3),

and content(3T+B)^3. For A>=T, both first upper gaps are at least3T and all simplex states are admitted, so the full parent is sum_(u)(T+A+m0+1)F_B(u).

Now let0<=A<T and put L=2T+A. Only the first two upper single-overlap corrections can change this detached-tail formula. They cannot coexist, or coexist with a lower overlap, because their nonzero indices would require at least3T+2 total deficit. The two excluded regions E1:u1-u2>=L+1 and E2:u2-u3>=L+1 are disjoint. The last two forms of m_A are nonnegative on the full simplex.

For an admitted first-correction state u1>=L+1, set

    tau1(u)=(L+u2+1,u1-L-1,u3).

It is an involution onto the deeper excluded E1 region. Here u2<=T-A-1<T, so the first affine form is the minimum. The excluded weight is exactly the negative of the admitted weight. Its first two detached h factors are precisely the correction factors, while u3 and the entire lower skew shape remain unchanged. The inverse is nonnegative and satisfies the other three top inequalities; its second and third deficits are at mostT-A-1. Thus every term is paired, not just the total count.

For an admitted second-correction state u2>=L+1, use

    tau2(u)=(u1,L+u3+1,u2-L-1).

Again the weights are negatives, and the map exhausts the deeper E2 region. Both third deficits are<T, so the lower upper-overlap vanishes and the same bottom two-row Schur factor occurs on both sides. Excluded first layers have zero weight. This proves for EVERY integer A>=0, not only multiples of T,

    f(T,A,B)=f(T,0,B)+A Q(T,B),
    Q(T,B)=sum_u F_B(u).                                (2)

For B>=0 all residual contents are nonnegative because each detached total is at most3T and each content is3T+B. The complete two-row factor in either tail term is

    1+2T+B-sum_i(gamma_i-T)_+.

Every pair-subset hinge and the bottom second-subdiagonal term vanish by their actual endpoint inequalities. Therefore

    Q(T,B)=Q1(T)+B R(T).                                 (3)

The six-variable determinant-complement identity in proof005, now with c=9T+2A+2B, swaps A and B. Its complementary shape is exactly the same displayed family with A,B exchanged, and the two weight blocks swap. Thus f(T,0,B)=f(T,B,0)=P11(T)+B Q1(T). Substitution into(2)–(3) gives(1).

At T=0, the deficit simplex has only u=0. The top multiplicity is A+1. The bottom two-row shape(2B,B) with content(B,B,B) has multiplicity B+1 by the complete two-row formula. Hence the WHOLE count is(A+1)(B+1), which agrees with(1), since P11(0)=Q1(0)=R(0)=1. No strict-shape theorem is incorrectly applied at this degeneration.

## 3. Actual degree, saturated lattice and every zero parameter

For s>0, all five top parts are strictly decreasing, all six contents positive, and the four dominance gaps are

    (3s+a,4s+a,3s,4s+b).

The complete weighted-GT lattice is saturated Z^10 with actual dimension10. Applying the full staircase formula, including its shape and smallest-content conditions, gives true codegree ceil(3/s):3 at s=1,2 at s=2,1 at s>=3. The term9/(3s) is controlling; every other ceiling is no larger. Thus increasing s does NOT leave the codegree fixed at3.

Because P11 has11 strictly positive coefficients, all eleven ordinary coefficients of(1) are strictly positive for every s>0, even when a=0 or b=0.

For s=0,a,b>0, the full count is(at+1)(bt+1), degree2. For exactly one of a,b positive it is an integral segment count, degree1; the origin has degree0 and count1. These are the actual degrees by the all-stretch count identity and Ehrhart degree theorem; no ten-dimensional fit is used on them. Their true codegrees are respectively max(ceil(2/a),ceil(2/b)), ceil(2/a) or ceil(2/b), and1 at the point, as follows directly from reciprocity. Their affine lattice is the full integer GT row-sum lattice at its actual affine hull; the complete product count and whole LR identity, not a falsely retained Z^10 chart, prove the boundary signs.

A separate x=0 homogeneous edge cone has

    lambda=(24s+9b,19s+7b,14s+5b,9s+3b,6s+2b,3s+b),
    mu=the tail of lambda,
    nu=(7s+2b,6s+2b,5s+2b,4s+2b,2s+b).

Its full count is Unit1 P10(st)+bt Q0(st). Determinant duality takes it to the old y=0 direction; the same independent-width proof establishes the required extension, not an unproved substitution at a nonintegral ratio. At s>0 it has degree10 and codegree ceil(3/s); at s=0 it is bt+1. It is a boundary reduction, not counted as an independent new family discovery.

## 4. Concrete generality and boundary challenges

The integer-width involutions were checked for102 pairs(T,A), T=1,...,12 and0<=A<=T+1, including widths strictly between0 and T. There are581 paired states in each region and406 zero-weight excluded first-layer states. Every image set, inverse weight and lower-tail exclusion agrees.

The complete two-row hinge formula passed1388 independent bounded-composition checks, with all three possible detached total types retained. Thirty-six independent entire-GT counts test12 main-cone triples at t=0,1,2, including s=2,a=b=1, s=3,a=1,b=2, asymmetric excesses and all dimension drops. Nine additional literal ordinary-LR reading-word counts check the final bare triples; in particular(s,a,b)=(2,1,1) gives50859 at t=1. These are challenges of the proof, not a substitute for all-parameter reasoning.

The nonnegative-excess condition cannot simply be erased. The LEGAL bare triple at(s,a,b)=(2,-1,0) is

    lambda=(51,40,29,18,12,6),
    mu=(40,29,18,12,6), nu=(16,13,10,8,4).

At t=1 the formal extension happens to agree at20481. At t=2 it predicts2877435 but the whole count is2878857, a missing1422. At t=3 it predicts76673533 instead of76705786. These are scalar failures of an overextended formula, NOT negative ordinary-coefficient observations or a full vector for this outside member. The separate(2,-1,1) challenge likewise agrees at t=1 and fails later. All records remain preserved, including favorable early coincidences.

The literal direction pair differs from the fixed Pro025 displayed pair, but no claim of inequivalence under every possible LR symmetry is made. Pro025's positive common-cap quotient does not by itself supply this complete base, these single slopes or these initial walls. The simple capped R model is already of a protected type; the new result is complete compensation with the legal whole parent.

## 5. Explicit saturated affine inverse on the s=0 boundary

To make the boundary lattice completely explicit, work at a fixed stretch with A=at,B=bt. The whole six-label GT chain is parametrized by integers r,z with0<=r<=A,0<=z<=B:

    x^(0)=0,
    x^(1)=(A+2B),
    x^(2)=(A+2B+r,A+2B-r),
    x^(3)=(2A+2B,A+2B,2B),
    x^(4)=(2A+2B,A+2B,2B,B),
    x^(5)=(2A+2B,A+2B,2B,B+z,B-z),
    x^(6)=(2A+2B,A+2B,2B,2B,B).

Zeros are harmless padding. Dominance equality at the first three labels forces x^(3) to be the first three fixed top rows. Their determinant-2B deletion leaves the entire three-letter shape(2A,A,0) of weight(A,A,A), whose one free second-row coordinate is r. The remaining bottom straight shape(2B,B) of weight(B,B,B) similarly has the one free coordinate z. Equivalently, direct interlacing and row-sum elimination gives exactly the displayed chain; the inequalities reduce to the four interval endpoints and no other restriction.

The integer inverse reads r=x^(2)_1-(A+2B), z=x^(5)_4-B. This proves the entire real square/rectangle and the saturated Z^2 lattice when A,B>0, with the forced coordinate deleted for an interval or point. Thus the dimensional and codegree boundary claims above have an explicit whole affine-lattice model, not just a product of numerical counts.
