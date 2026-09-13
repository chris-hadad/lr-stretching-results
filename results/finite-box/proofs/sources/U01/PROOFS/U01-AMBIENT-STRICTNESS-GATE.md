# A finite ambient-strictness criterion before genuine interior counting

## Statement and proof

Let P be the entire rational hive model in a complete saturated D-coordinate chart, defined by finitely many integral inequalities c_r+a_r.z>=0. Its positive-stretch integer count is an LR polynomial of degree at most D. Assume either that P is known nonempty or leave the empty case as an unresolved/zero alternative. Define the finite strict-point sets, for t=1,...,D+1,

    W_t = {z in Z^D : c_r*t+a_r.z>=1 when a_r!=0,
                       c_r*t>=0 when a_r=0}.

An element of any W_t proves that P is nonempty and full-dimensional in the given chart: dividing its coordinates by t makes every nonconstant defining inequality strict, so a small real D-ball is contained in P. The lattice is the inherited saturated coordinate lattice; no parity is guessed from the upper bound.

Conversely, if P is full-dimensional, simultaneous strictness of every nonconstant defining inequality characterizes its interior. Redundant inequalities cause no difficulty: a nonconstant valid inequality cannot vanish at an ambient interior point. Thus W_t is precisely the interior lattice set of tP. If W_1,...,W_(D+1) were all empty, Ehrhart reciprocity for the period-one count polynomial would give D+1 distinct roots -1,...,-(D+1) of a nonzero polynomial of degree D with P(0)=1. This is impossible. Therefore a full-dimensional period-one chart has a strict integer point at one of these finitely many grades.

A nonempty lower-dimensional polytope has at least one nonconstant defining inequality identically tight. Otherwise choosing a point where each separate inequality is strict and averaging the finitely many points would yield simultaneous strictness and an ambient open ball. It therefore has no point in any W_t. Consequently, with complete finite searches and the stated LR polynomiality premise, the criterion distinguishes ambient-full charts from the remaining empty/hidden-dimensional charts without reconstructing the full polynomial or enumerating their facets. A work-limit refusal is not a completed empty search.

The period-one premise is essential. The rational half interval [0,1/2] has dimension one but first strict integer point at t=3, beyond D+1=2; its lattice count is a quasipolynomial. It is included as a control of the search implementation, not admitted to the LR criterion.

## Direct low-coefficient decision in dimension five

For D=5, a checked strict witness establishes actual dimension five and epsilon=-1 independently of any earlier coefficient vector. The same full chart then computes genuine I(1),I(2) by shifting every nonconstant integral row from >=0 to >=1. At a fixed physical grade t each such problem is supplied to the homogeneous counter with constant c_r*t-1 and computational dilation one. This is a fixed-grade encoding; it is not asserted to be a new LR stretching family or a period-one polynomial in that computational dilation.

Together with complete closed counts A=P(1), B=P(2), put U=I(1), V=I(2). The adopted source identities become

    D1 = 8(A+U)-(B+V) = 12c1-48c5,
    D2 = 16(A-U)-(B-V)-30 = 24c2.

The full coordinate-identification chart has primitive normals of squared norm at most six; the initial chart construction explicitly checks this on every admitted row system. The source short-normal theorem supplies c3>0, while intrinsic top-coefficient positivity supplies c4,c5>0. Therefore D1,D2>=0 prove the whole polynomial ordinary-nonnegative. D1 alone being negative does not establish a negative c1. Negative D2 with these complete premises is a genuine c2 observation at the stated geometric scope.

The initial chart construction's 35-key test reads only the frozen chart data, not previous vectors or counts. It searches for explicit strict points at grades one through six, retaining integer points, original count-boundary hive coordinates and all original rhombus slacks. On admitted full-dimensional charts it independently counts A,B,U,V. Three charts have no ambient-strict point and are not forced into the quintic formula. Their actual quartic degree is established separately by the independent complete-vector certificate, not by assuming that a five-coordinate bound is actual dimension five.

If a tensor variant was used for the small chart, the explicit point belongs to the stored **count_boundary** hive. Its all-stretch LR polynomial equals that of the original bare triple by the recorded tensor word. Both hive dimensions equal that polynomial's degree, so reciprocity also identifies their true interior counts. This does not assert an unrecorded affine isomorphism between the two hives.

## Verification and computational limits

`strict_witness_u01.py` uses exact real Fourier–Motzkin prefix projections followed by bounded integral prefix search. A returned point is independently checked by direct substitution in every defining row and mapped back through the recorded integer inverse. Its 25 fixtures cover cubes and simplices through dimension five, the first-interior threshold, negative coordinates, an empty interval, a hidden line and the non-period-one half interval.

The direct interior counts use the same exact H-system counter as the closed-hive lane. They are corroborated after preservation against reciprocity values from the independent full LR row-model polynomials. That is valid finite corroboration, but it does **not** price an independent interior-only production method: obtaining the independent full vector costs additional work. A whole-family proof of the D1/D2 bounds or a cheaper independent direct interior model is not established here. No all-key membership or million-key runtime extrapolation follows.

Sources: complete chart and polynomiality premises in the source certificate collection, especially proofs 027, 029, 036–038 and the hive-count and quintic coefficient certificates (ROOT-F025-COUNTER / FR025-QUINTIC-DECISIONS). The strict-point argument above supplies the criterion independently of previously computed counts.
