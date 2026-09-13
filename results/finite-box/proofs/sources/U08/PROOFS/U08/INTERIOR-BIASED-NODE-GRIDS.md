# Moving the determining grid without losing the protected upper bound

Let P be an entire nonempty period-one polynomial of independently proved actual dimension d. Choose integers m>=1,p>=0 with m+p=d. Use the d+1 nodes -m,...,p, keep P(0)=1, count P(1),...,P(p) and true interiors I(1),...,I(m-1), and leave Z=I(m) unknown. There are d-1 numerical premises. This is a whole-polynomial identity in a prior degree space, with P(-j)=(-1)^d I(j), not an assumption of reflection or empty interiors.

The denominator of the left-endpoint Lagrange term at -m is (-1)^d d!, so reciprocity cancels that sign. The exact coefficient kernel of the unknown count is

    K_(d,m)(t) = product(t-r, r=-m+1,...,p) / d!.

Let S1=sum(r) and S2=sum(r^2) over those d roots. Then

    [t^d] K = 1/d!,
    [t^(d-1)] K = -S1/d!,
    [t^(d-2)] K = (S1^2-S2)/(2d!).

In particular, a separately protected strict c_(d-2)>0 gives a finite upper bound on integer Z whenever S1^2<S2; leading positivity supplies a lower bound. Multiply by the actual exact coefficient denominators before integer rounding. This extends U07's balanced kernel formula to a movable complete grid. It gives no signs for an untested LR member by itself.

For even d=2q, both choices (p,m)=(q,q) and (q-1,q+1) have

    (S1^2-S2)/2 = -q(2q-1)(q-1)/6 < 0  for q>=2.

The root sets are reflections of one another. Therefore an interior-biased degree-ten certificate may count P1,...,P4 and I1,...,I5, leaving I6 unknown, while RETAINING a protected finite upper bound from c8. It replaces an expensive closed P5 count by a true I5 count; whether that actually saves cost must be measured on identical complete objects. The mixed grid is -6,...,4; a full-vector baseline must keep its complete determining grid and unused positive holds fixed before counting.

For odd d, moving the symmetric known-root set one unit inward instead gives

    (S1^2-S2)/2 = -d(d-1)(d-11)/24.

This is positive at d=9, zero at d=11, and negative for odd d>=13. Thus simply shifting the present nonic grid loses this particular top-coefficient upper-bound certificate. At d=11 the protected c9 kernel vanishes, so a finite upper bound would need actual geometric information or another separately justified premise. That is a limitation of this certificate, not an impossibility theorem about another grid or positivity.

The decisive next test is a same-target, actual-geometry comparison of the two even-degree grids at degree ten, including independent interior counts, formal-bound costs, numerical refusals and full-vector fallbacks. No degree-ten numerical result, unseen source value, or coverage increment is claimed in this proposal. The argument is exact interpolation algebra; the originating contribution is the concrete cost-adaptive grid choice with its proved protected-bound condition, not a worldwide novelty claim.

For the interior-biased degree-ten grid specifically, the kernel is

    K_(10,6)(t) = t(t+5)(t^2-1)(t^2-4)(t^2-9)(t^2-16)/10!
               = (t^10+5t^9-30t^8-150t^7+273t^6+1365t^5
                  -820t^4-4100t^3+576t^2+2880t)/10!.

Thus a separately justified weak c7>=0 can ALSO impose an upper bound on I6, without the strict-sign unit decrement. Where the inherited ambient-rank-six top-four theorem is applicable, its precise weak/strict form should be used in the next test rather than discarded or silently strengthened. That is an additional source-specific inequality, not an assertion that all degree-ten/rank-seven c7 are already protected. The displayed kernel is included in the completed exact grid controls; its LR application and performance remain uncomputed.
