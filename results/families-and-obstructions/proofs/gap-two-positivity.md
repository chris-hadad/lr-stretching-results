# Complete Delta3=2 positivity, sharp baseline, and the next overlap obstruction

This computer-assisted proof uses a finite rational certificate. No historical
priority claim is made. [The branching proof](gap-two-branching.md) and
[profile classification](gap-two-profiles.md) establish full lattice/count
membership and exhaustion, which are necessary to deduce an unbounded result.

## 1. The finite positive certificate

[The profile certificate](../data/gap-two/profiles.json) contains the exact 637 profiles, their complete balanced rank-six constructors, codegrees, determining values, two unused positive holdouts, and four coefficient arrays P00,W,V,Z in increasing ordinary powers t^0,...,t^10. The input and algorithm specifications preceded the calculations. The count formula is precisely (7)-(12) of the branching proof, evaluated using coefficients of the explicit product h_u1 h_u2 h_u3 in THREE variables; no large-boundary LR enumeration or guessed degree is involved.

There are 494 codegree-five profiles and 143 codegree-eight profiles. For codegree five the determining sites are 0,...,6 with unused holdouts 7,8; for codegree eight they are 0,...,3 with unused holdouts 4,5. The source dimension and reciprocity theorem establish these spaces before any fit. The derivative arrays are reconstructed in the SAME complete spaces, since (16) is an identity of actual whole polynomials.

The certificate verifies all 28,028 entries (637*4*11) are nonnegative, that all 7,007 base entries are positive, and that every base satisfies

    P00(t) >=_coeff Pmin(t),
    Pmin(t)=binom(t+7,7)*(t+4)*(t^2+8t+9)/36.     (17)

The exact coefficient vector of Pmin is

    (1,2351/630,5939/1008,58997/11340,518741/181440,
     1109/1080,2119/8640,73/1890,233/60480,1/4536,1/181440).

The independent checker j04_independent.py rebuilds every vector by Newton forward differences, rather than the producer's Lagrange interpolation, checks the entire 637-key Cartesian inventory minus the three justified exclusions, checks every holdout, and verifies the baseline subtraction. This is independent implementation of arithmetic on the same integer values, not an independent count model by itself. Its literal bare-LR row-word model separately agrees on all 1,274 base values at t=1,2. Complete direct weak-GT checks on five control families include determining values and unused holds, all four earlier control vectors, and the baseline. Additional full LR recounts and an interrupted attempt are recorded in the original data; the interruption provides no uncomputed verification.

The certificate algorithms are elementary: h_n is enumerated by every triple of nonnegative exponents summing to n; polynomial multiplication is integer convolution; (10) retains all clips; (12) is evaluated exactly with denominator three; interpolation uses Fraction. An independent source/arithmetic engine is not supplied. The explicit tables, literal counts and proof of finite exhaustion make this a reproducible finite certificate rather than an empirical assertion from 637 sampled boundaries.

## 2. The all-parameter theorem and exact scope

For EVERY strictly decreasing positive five-part alpha and every sorted positive six-part beta of equal total, with strict dominance and Delta3=2,

    K_(t alpha,t beta) >=_coeff Pmin(t),          (18)

and every ordinary coefficient through its actual degree ten is strictly positive. Indeed use the profile classification to find its profile, then (16) and the nonnegative four coefficient arrays. Widths x,y may be arbitrarily large. The positive baseline supplies strictness even when some direction coefficients vanish.

The exact polynomial spectrum of this stratum is the union of the 637 inhabited bilinear families (16); different profiles and parameter values can give the same polynomial. The 637 bases contain 342 distinct full vectors. This is not a classification of whole conventional-hive geometry. Nor is it a theorem about every degree-ten/codegree-five or -eight LR polynomial.

Every coefficient is nondecreasing in the profile's nonnegative width coordinates x,y, including the mixed xy term. These are specific count-preserving coordinates with legal whole-family constructors. No global coefficient monotonicity or concavity for arbitrary boundary changes is asserted.

## 3. Sharpness and actual bare triples

The baseline occurs at E-core (M=-1), gap g=2 and any of the three fixed pair tail profiles. A small realization is

    alpha=(6,5,4,2,1), beta=(5,5,3,3,1,1),
    lambda=(18,13,8,5,2,1),
    mu=(13,8,5,2,1), nu=(6,5,4,2,1).             (19)

It has ordinary rank six, outer size 47, actual degree ten and codegree eight. Another fully independently counted control is alpha=(8,7,6,4,3), beta=(7,7,5,5,2,2), with lambda=(28,21,14,9,4,2), mu=(21,14,9,4,2), nu=alpha. Both have the full polynomial (17). Its values at t=0,...,5 are

    1,20,174,980,4180,14652.

The first four values determine the normalized cubic in the prior codegree-eight space; it is (t^3+12t^2+41t+36)/36. The last two positive sites are unused holdouts. Factorization gives (17). Thus the coefficientwise bound and the linear bound c1>=2351/630 are attained, not just formal lower estimates.

All displayed strict-five-row tail lifts in this stratum have outer size at least 42. Here is a boundary proof, not an inference from the representative roster. A3>=3 and e>=-1 give B3>=2. The first-three beta total is at least 10, so B1>=4. If B2<=2, sortedness forces B2=B3=2, e=-1,A3=3; but B2=A2+d-1>=4, contradiction. If B2=3 and B3=2 the same contradiction holds. Thus either (B2,B3)=(3,3), or B2>=4. In the first case the top weighted content cost is at least 19, and the positive tail of sum at least five has weighted cost 4v1+5v2+6v3 at least 23. In the second case, if B3>=3 the top cost is at least 21, already enough; if B3=2, every tail entry is at most 2, so tail cost is at least 24 and top cost at least 18. In every case outer size is at least 42. Equality is realized, for example, by alpha=(5,4,3,2,1), beta=(4,4,2,2,2,1). This is a lower bound for these displayed tail constructors, not for every other possible LR realization of the same polynomial.

Strict six-row/six-label data at Delta3=2 have the same determinant-column extension as the gap-one family: remove the alpha6 full-height determinant columns. They are forced to contain labels 1,...,6, and the inverse restores them. It is an exact integer GT translation at every stretch. Strict Delta5 ensures beta6-alpha6>=1; the remaining five-part shape and all six contents are positive and preserve all dominance gaps. Therefore (18) applies with the same degree, polynomial and baseline. The original six-row displayed lift has size at least 42+21 alpha6>=63. Repeated parts, zero labels and non-strict dominance need separate affine-hull analysis and are not covered by this extension.

## 4. The overlap correction is substantial, not optional

At alpha=(5,4,3,2,1), beta=(4,3,3,2,2,1), dropping (8)'s overlap corrections gives 52 instead of 48 at t=1, and 908 instead of 826 at t=2. The actual removed count is 436564 at t=8. At the left codegree-eight boundary alpha=(5,4,3,2,1), beta=(4,4,2,2,2,1), it gives 32 instead of 28 at grade one, 383 instead of 327 at grade two. These are complete counts for the stated invalid simplification, not negative ordinary LR observations.

The central family has q=5 and a degree-six normalized residual, not the gap-one quadratic. Its whole polynomial vector is

    (1,631/140,2998/315,62219/5040,3376/315,1537/240,
     1897/720,409/560,109/840,67/5040,1/1680).

The complete count includes every top multiplicity, content cap, single hinge, pair endpoint and overlap. None may be erased because the final coefficients are positive.

## 5. A new coupling appears at Delta3=3: an exact challenge to extending this proof

This subsection gives a symbolic obstruction to extending the positivity proof. Take the legal strict data alpha=(5,4,3,2,1), beta=(3,3,3,2,2,2), whose third gap is three. For every t>=3, the first-block deficit

    u=(t+1,t+1,t-2)

has eta=(4t-1,3t-1,2t+2), an admitted partition of size 9t dominating (3t,3t,3t). Its exact top multiplicity is t-2. The first TWO upper overlaps now coexist. Their determinant on the first three remainder rows is

    h_(t+1)^2 h_(t-2)
       -h_(2t+2) h_(t-2)
       -h_(t+1) h_(2t-1)
       +h_(3t).                                (20)

The positive three-cycle term h_(3t) would be missed by extending a formula that subtracts individual overlaps only. Multiplying by the complete bottom s_(2t,t) and extracting content (2t,2t,2t) gives for this missing term s_(2t,t)(1,1,1)=(t+1)^3. To see this without any pointwise approximation, every weight of this shape uses a fixed letter at most 2t times (at most one occurrence in each column), so h_(3t) fills exactly the complementary content. Directly, its Jacobi-Trudi value is binom(2t+2,2) binom(t+2,2)-binom(2t+3,2) binom(t+1,2)=(t+1)^3. This uses the same complete two-row identity, not a new external dimension premise. Including the first-block multiplicity, the omitted contribution of this ONE admitted state is

    (t-2)(t+1)^3,

equal to 64 at t=3. Thus the Delta3=2 single-overlap mechanism cannot be transferred to Delta3=3 without an additional interaction term. It does not prove positivity or negativity of that whole family; it identifies the term required by an extension of the count formula.

## 6. Scope and provenance

This is a complete all-coefficient theorem at ordinary rank six for the stated full strict Kostka/LR stratum and its determinant extension. Together with the gap-one theorem it covers the corresponding third gaps 1 and 2. It is not all rank-six LR triples, all strict rank-six Kostka data, a whole-box certificate, or full KTT. No ordinary-negative entire LR example or additional finite-box count is supplied. The recorded negative-example count remains zero; the prior additive coverage count remains 4554.

The exact positive profiles give a substantive full-count compensation mechanism beyond transportation c1: boundary order and the small total deficit force a finite set of overlap types; whole polynomiality and the complete signed count then place EVERY admitted boundary in an inhabited ordinary-positive coefficient cone. General compensation, negative completion, other codegrees and broader matching-family or whole-rank positivity require separate arguments.
