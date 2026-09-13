# Co-realized negative cells, complete compensation, and an offset falsifier

All negative observations here concern local cones or abstract non-LR polytopes. No ordinary-negative entire LR coefficient was observed. The local observations and complete-object comparisons are recorded separately.

## The actual rank-six edge

Take the balanced entire ordinary LR triple, lambda outer,

    lambda=(13,11,8,8,5,3), mu=(8,5,5),
    nu=(10,8,5,5,2).

Its rank is six, outer size 48, boundary mask4932, saturated chart Z4 and actual degree four. The point (38,44,25,34) is strict for every nonzero complete chart row. At the selected edge point (38,44,24,34), the original nonzero active row indices are 1,2,13,26,27 (zero-based indexing in the fixed symbolic rhombus list).

Two independent selected normal triples are

    (-1,0,1,0),(-1,0,2,0),(-1,0,1,1),  alpha=-1/144,
    (0,0,1,0),(-1,0,2,0),(0,0,1,-1),   alpha=-1/48.

All three rows of each selection really are tight at this legal full-hive edge. They do NOT form the full normal cone. The complete indexed transverse cone, with every active row, has

    alpha_complete=5/144>0.

In the stored saturated normal basis its four primitive tangent rays are

    (-1,1,0),(-1,1,1),(1,0,-1),(1,0,0).

The complete affine slack identity is

    r13(b,x)=r1(b,x)+r2(b,x).                            (1)

There is no discarded boundary-dependent constant in (1). Consequently r13=0 forces both other slacks to zero. Its direction cannot replace those two actual extreme normals. The second problematic row obeys the separate full identity

    r17(b,x)=r12(b,x)+r14(b,x).                          (2)

At the other saved edge point (37,44,25,34), the active nonzero rows are 12,14,17,19,20; the selected negative constants are again -1/144 and -1/48, while the full cone again has 5/144. Equations (1) and (2) are verified on all boundary and chart coordinates in DATA/J11-EXPLICIT-FORCED-COMPENSATION.json.

The whole unit hive has 21 exact vertices and 52 edges. Its entire polynomial is

    P(t)=1+29t/6+32t^2/3+35t^3/3+35t^4/6.

The complete counts at 0,...,6 are

    1,34,240,899,2431,5396,10494.

Nodes0..4 determine in the prior degree-four space; 5 and 6 are unused checks. The true first-interior count is one, so codegree is one; that fact is not used as a reflection premise. Full edge-volume aggregation gives c1=29/6, matching the independent literal LR reconstruction. A size 60 control has the same entire polynomial by a stored count symmetry and is not a second polynomial discovery.

## Complete cone comparisons

The first eight exact seed geometries were already covered by positivity in the bounded domain. None had a negative complete edge weight. Testing the existence of an ISOLATED bad triple at arbitrary legal boundaries returned exact Farkas infeasibility certificates. The subsequent relaxed test allowed all additional normals annihilating the same edge direction to become tight. This produced 46 coactive-negative-subcone occurrences.

Every such occurrence was saved before completion. Their full cone constants are among

    1/12,1/16,13/72,19/72,5/144,

all positive. The data label `ACTUAL_NEGATIVE_LOCAL` refers to a selected negative triple with a coactive witness, not to a negative complete edge cone. DATA/J04-COMPLETE-CONES.json records all complete cones and their positive constants.

The discarded isolated-triple formulation, relaxed simultaneous-incidence formulation and universal whole-row implication repair are distinct preserved attempts. Their outcomes concern the tested eight normal lists and the later 29 representative certificates, not all possible higher-rank incidence systems.

## Independent-offset challenge

Keep the SAME unreduced primitive normal list of mask4932, but allow its affine constants to vary independently of any LR boundary. For the three directions

    (-1,0,1,0),(-1,0,2,0),(-1,0,1,1)

set the constant to zero; for every other primitive direction set it to one. DATA/J11-ABSTRACT-OFFSET-RAW.json contains all twenty inequalities, not just these three. This produces a bounded full four-polytope with 19 rational vertices and 49 edges. Its edge from (0,-1,0,0) to (0,1,0,0) has the three displayed directions as its ACTUAL complete normal cone and has constant -1/144. Its normalized length is2, so its weighted contribution is -1/72.

This is a genuine negative complete local weight, unlike the coactive selected cells above. It is still not a negative entire coefficient and has no asserted LR realization. The independent constants violate the required affine slack identities; short normals or the same list alone do not justify the LR row-removal certificate.

The least common denominator of the saved vertices is 12. After this integral dilation the entire lattice polynomial is

    1+81t/2+1491t^2/2+7182t^3+30396t^4,

with values at 0..6

    1,38365,546856,2662822,8253115,19914091,40971610.

The two unused positive checks pass, and c1=81/2 is 12 times the complete undilated face sum 27/8. Thus the whole abstract control is positive despite its one negative complete edge weight. This does not prove positivity for arbitrary independent offsets or supply an ordinary LR counterexample.

The original mass-admissible source triple

    (-2,-1,-1,0),(-1,-2,0,0),(-1,-1,0,0)

also reproduces the inherited -55/1008 by the primary indexed formula and independently by the full parallelepiped Laurent subtraction. It is an inherited control, not a new discovery. DATA/J11-SHORT-MASS-NEGATIVE-CONTROL.json preserves both complete evaluations.

## Six whole-polynomial checks

DATA/J08-ROSTER.json and DATA/J10-INDEPENDENT-WHOLE-LR.json preserve six full bare triples, ordinary ranks, prior exact dimensions, complete values and coefficient vectors. Every complete hive c1 matches its full face sum. The independent LR recount matches42 count sites, including 12 unused positive sites, using a literal LR reading-word rule and independent Newton interpolation.

The initial literal LR calculation completed 26 original-triple sites before a rank-seven t5 call reached its 1,800,000-state cap. It raised a work-limit exception and returned no partial scalar. An exact invariant-tensor permutation, simultaneous duality, and determinant normalization reduce the number of positive content labels from six to three in the difficult case. This preserves the entire polynomial at every stretch. A separate completed recount supplies every determining and reserved node. Reusing the literal LR kernel after this symmetry does not constitute a third independent counting model.

No highest-rank conclusion or box increment follows from these selected checks. Their purpose is to challenge the full mathematical certificate, its genuine LR bridge, actual lattice normalization, and the tempting false extension from full boundary identities to arbitrary offsets.
