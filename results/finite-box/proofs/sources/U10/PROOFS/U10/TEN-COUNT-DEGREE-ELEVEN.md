# Complete degree-eleven signs from ten counts and a sixth-interior enclosure

Let P(t)=sum_{k=0}^{11} c_k t^k be the entire nonempty stretched LR polynomial with lambda outer, in the original physical grading. Require a complete saturated eleven-coordinate chart of the whole hive, an independently checked full affine hull and integral inverse, and an explicit strict integer point establishing actual dimension eleven. All primitive inward normals must have squared norm at most six. The source certificate collection's precise complete two-cone theorem then gives c9>0; intrinsic leading and second-leading positivity give c11,c10>0. Nonemptiness gives c0=1. These geometric hypotheses are not inferred from a coordinate bound or fitted degree.

Write the ten actually observed counts in order v=(P1,P2,P3,P4,P5,I1,I2,I3,I4,I5), where I is true relative interior. Odd actual dimension gives P(-j)=-I(j). Leave Z=I6 unknown. Exact interpolation on the prior complete space at -6,-5,...,5 expresses

    d_k c_k = N_k(v) + a_k Z.

The whole integer matrix, including the constant term, is supplied in DATA/U10/inputs/DUAL-CONTROLS.json. It is independently derived by rational Vandermonde elimination and tested on all 144 monomial actions. For the four unprotected odd coefficients the identities are

    27720 c1 = N1 - 10 Z,
    907200 c3 = N3 + 479 Z,
    725760 c5 = N5 - 139 Z,
    1209600 c7 = N7 + 31 Z.

Here N1=4620+19800P1-4950P2+1100P3-165P4+12P5+27720I1-9900I2+3300I3-825I4+132I5. Every even coefficient is exactly determined by the ten values. The protected odd identities are

    725760 c9 = N9 - Z,
    39916800 c11 = N11 + Z,

with N9=462-288P1+117P2-28P3+3P4+504I1-378I2+192I3-63I4+12I5 and N11=-462+330P1-165P2+55P3-11P4+P5-462I1+330I2-165I3+55I4-11I5.

The unknown kernel is

    K(t)=t product_{j=1}^5 (t^2-j^2) / 11!.

It has mixed signs. Ten counts do not determine a complete vector, and Z is never set to zero merely because early interiors vanish. Because all numerators and Z are integers, the protected strict coefficients imply

    max(0,1-N11) <= Z <= N9-1.

Intersect this with any completely verified integer enclosure [l,h] of I6. On a nonempty resulting interval, strict positivity of each unprotected numerator at its minimizing endpoint, together with the separately protected top coefficients, proves the entire polynomial ordinary-positive. The exact even coefficients are checked, not assumed positive. A negative lower bound fails a sufficient test; only a negative exact coefficient or negative upper bound of a whole coefficient establishes an ordinary-negative result.

The complete sixth-interior H-system replaces each homogeneous row c*t+a*x>=0 by 6c+a*x>=1 exactly when a is nonzero, leaving forced constant rows unshifted after full affine-hull verification. Every original row and the saturated lattice are retained. Formal box proofs derive necessary integer bounds, split finite intervals exhaustively and disjointly, and add leaf cardinality bounds. Wholly feasible boxes give lower bounds; every leaf gives a complete upper cover. The separate checker validates every rounding endpoint by multiplication inequalities, all splits and every original row. A changed search order changes neither proof rules nor mathematical hypotheses.

The independent hive and complete semistandard/ballot-row counters supply every consequential numerical premise, with raw requests/responses bound to the exact physical-grade objects and orientation-specific interior thresholds. A separate full-vector comparison counts I6, preserves each entire vector before comparison and checks, and retains positive holds P6,P7. Closed P6 is not determining interior I6. Refused or uncomputed numerical holds remain unresolved until repaired at their original sites.

This is a generally sound sufficient criterion at the stated whole-chart scope. The actual finite population, tests, exceptions and coverage are separate evidence. This derivation alone does not claim every boxed degree-eleven object satisfies it, nor all-size positivity, priority, or whole-box completion.
