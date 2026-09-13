# An exact obstruction to an isometry-only patch rule

This obstruction applies to one precisely specified correction space. It is not a negative whole LR coefficient or a theorem excluding every enlarged correction space.

## Space tested

Start with the 381 selected supporting triples of the complete rank-seven atlas. Keep functionals supported on their actual nonzero coordinate unions and zero on other supports. Identify their 58 signed ambient-coordinate cone-isometry types; require each local vector to be invariant under its type's signed-coordinate stabilizer, and transport it through the explicit isometry words. This leaves 36 scalar parameters. Generator permutations are permitted, individual normal sign reversals are not.

The qualification about selected supports is important. Allowing new supports, a different metric, or additional geometric context is NOT excluded. An abstract isometry of one cone is not an isomorphism of the entire hive incidence system.

## Two exact constraints

Use the canonical60-normal rank-seven atlas in HISTORY/P10-A01/DATA/ATLAS-R7.json. The independent quadruples

    I_A=(1,2,43,56), I_B=(1,3,42,43)

have complete raw constants

    alpha_A=-3443/604800,
    alpha_B=10403/1310400.

In the above 36-dimensional space ALL their possible corrections reduce to x and -2x, respectively. The only active scalar is the invariant direction (-2,-1,-1,1) for the canonical triple

    (0,0,1,1), (0,1,0,1), (1,-1,0,1).

Other selected facets of these cones have zero invariant local kernel. The full geometric embeddings, stabilizer equations, quotient divisors and pairing rows are in DATA/INVARIANT-SYSTEM.json.gz and ISOMETRY-OBSTRUCTION-DUAL.json. The second cone has only its named facet in the selected support list; no extra support is silently made zero outside that declared hypothesis.

Consequently any putative nonnegative corrected array would satisfy

    alpha_A+x>=0,
    alpha_B-2x>=0.

Multiplying by2/3 and 1/3 gives the exact contradiction

    (2/3)(alpha_A+x)+(1/3)(alpha_B-2x)
       = -271/235872 <0.                                (1)

This excludes nonnegative correction in this space with UNBOUNDED real or rational coefficients. It is not merely a failed bounded numerical proposal. The gap between the necessary lower and upper bounds on x is271/157248>0.

The dual calculation records the exact nonnegative dual weights and all 36 vanishing moments. The independent verification recomputes both pairing rows and exhaustively enumerates all signed-coordinate stabilizers of the four relevant template types (five facet occurrences); all six relevant automorphisms and complete invariant nullspaces agree. It rechecks (1) exactly. The two raw BV constants are inherited fully verified local constants; no co-realization as two complete faces of one LR parent is asserted.

## A successful larger correction space and other limitations

The stronger geometric-support model allows vectors to distinguish actual triangular placement and boundary context. It passes both complete atlases; [Intrinsic boundary-patch compensation in complete hive atlases](038-INTRINSIC-BOUNDARY-PATCH-COMPENSATION.md) states every affected-cone condition.

Tying directed translated patches without their boundary-touch flags is still too restrictive for the saved proposal: the complete trial has 619 negative corrected occurrences at rank 6 and 539 at rank 7, with common minimum -3834134620169/4306500000000000. These are exact A02 trial arrays. That numerical result alone is NOT an unbounded-space impossibility theorem. Adding the three flags yields the successful399-template certificate.

An earlier literal transport that retained boundary distances truncated at TWO, rather than just contact flags, failed to match351 rank-six supports. Its resulting132 negative entries reflect missing corrections, not an impossible theorem. That overqualified signature and every output survive. A missing template match establishes neither nonmembership nor a new negative original coefficient.

All negative trial observations are local-certificate data. The inherited original local negatives, the 237 isometry-tied trial negatives, the 1158 translation-trial occurrences, and the 132 incomplete-transport negatives are overlapping diagnostic populations, not independent discoveries. No entire LR counterexample was observed.
