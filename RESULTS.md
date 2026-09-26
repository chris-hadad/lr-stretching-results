# Results and open questions

All coefficient signs here refer to ordinary powers of the stretching parameter.
A negative local weight, auxiliary quotient, mixed parameter coefficient or
root-location property is not, by itself, a counterexample to KTT positivity.

Start with the [rank-six paper](papers/rank-six/README.md) or jump to a category:

- [Main theorem and coefficient certificates](#main-theorem-and-complete-coefficient-certificates)
- [Positive families](#positive-families-at-arbitrary-size)
- [Geometry and coefficient behavior](#geometric-reductions-and-coefficient-behavior)
- [Examples and obstructions](#explicit-examples-and-realization-obstructions)

## Main theorem and complete coefficient certificates

| Result | Established scope | Verification and limit |
| --- | --- | --- |
| [Whole ordinary rank at most six](results/rank-six-positivity/README.md) | Every ordinary coefficient is nonnegative at every size and boundary, and strictly positive through actual degree for nonempty hives | Complete original-lattice proof, all exact finite premises and independent mathematical review; [paper](papers/rank-six/README.md) and [verification](results/rank-six-positivity/VERIFYING.md). Whole rank seven and unrestricted KTT remain open. |
| [Exact closure and legal realization](results/rank-six-positivity/GEOMETRY.md) | At every rank, retained independent physical branches occur for some legal integral boundary/refinement; at rank six, 103 positive identities generate every closure | Complete small certificate for all `2^45` physical row sets, minimum-six obstruction to the old calculus, and an exact constructive API. No field compression or every-boundary realization claim. |
| [Original finite box](results/finite-box/README.md) | Every legal balanced triple with maximum trimmed length seven and outer area at most 30 is coefficient-nonnegative | Complete original cover, whole-count reductions and 624,314 accepted terminal identities; explicit external rank-five theorem premise. Whole rank six is settled by the separate theorem above; whole rank seven remains open. |
| [Universal rank-six c2 and c3](results/rank-six-positivity/PROOF.md#4-the-exact-finite-premises) | Each has a lower bound of 1/200,000,000 times the complete actual two-/three-face lattice-volume sum | Complete finite fields and exact analytic inputs; coefficient-specific components of the whole rank-six theorem. |
| [Rank-six c4/c5 and actual-degree consequences](results/rank-six-coefficients/README.md) | Universal nonnegative c4/c5 at every rank-six area and boundary; whole nonnegativity through actual degree five at rank six and degree four at rank seven | Complete independent reconstruction of both finite fields, all 333,769 local types and every incidence; standalone replay about 10.4 minutes on the recorded host. The later whole-rank theorem closes c1,c2,c3; this earlier module retains its exact standalone scope. |
| [Ambient coefficient protection](results/structural-positivity/README.md#normal-corrections-and-boundary-classes) | With D_n=(n−1)(n−2)/2 and n=6,...,12, c_(D_n−4) has a positive complete face-volume lower bound whenever its actual degree reaches that index | All 34 normal-certificate rosters independently checked. Together with prior results this protects the top five ambient indices, not the top five actual coefficients of every degenerate hive. |
| [All actual cubics through rank seven](results/families-and-obstructions/README.md#positivity-at-arbitrary-size) | Every whole LR polynomial of ordinary rank at most seven and actual degree at most three is coefficient-nonnegative at every size | Complete 8,520-witness and orbit certificates included; distinct from the coordinate-bound sufficient classes. |
| [Boundary-coordinate classes](results/structural-positivity/README.md#normal-corrections-and-boundary-classes) | At arbitrary size: rank at most seven with the specified coordinate bound at most four, and rank at most six with bound at most five after tensor symmetry | Complete boundary-aware finite certificates. These sufficient classes do not exhaust whole rank six or every actual quartic/quintic. |

## Positive families at arbitrary size

| Result | Established scope | Verification and limit |
| --- | --- | --- |
| [Layered triangle positivity at unbounded rank](results/layered-triangle/README.md) | Layers `(A,b^r)`, integers `r>=3`, `b>=1`, `A>=(r-3)b`; positive layers have ordinary rank `2r+4` and degree `3r+1`; `r=3,A=0` trims to rank eight and degree seven | Complete analytic proof and all 136,332 finite coefficient slots, 342 holdouts and four corruption controls. Arbitrary unequal layer widths and unrestricted KTT remain open. |
| [All 4×5 transportation margins](results/transport-four-by-five/README.md) | Every coefficient positive through actual degree for all balanced nonnegative margins, transpose and active subrectangles; whole LR lift of rank at most eight | Complete 52-batch certificate and analytic boundary argument; separate 47-file companion data. This is a family theorem, not whole rank-eight LR positivity. |
| [Five-capacity LR families](results/five-capacity/README.md) | All coefficients positive through actual degree for the complete family with at most five coupled capacities; whole LR lift of rank at most seven | Full original-lattice proof, 26,332 subsets, 961 freshly computed local types and complete rational fields; all walls and zero parameters included at their stated scopes. |
| [Whole three-letter LR families through rank six](results/three-letter-rank-six/README.md) | Every coefficient through actual degree for every feasible rank<=6 triple with one inner partition of length<=3, all areas and walls; full stabilized quotients inside the family | Complete original lattice/model, 1,149,016 normal subsets, 395,657 independently reproduced local values and four exact fields; standalone reproduction. The separate whole-rank theorem now covers its complement; these family-specific tools and bounds remain useful. |
| [Whole transportation and capped LR families](results/transport-capped/README.md) | Every ordinary coefficient for all balanced nonnegative 3-by-5 transportation margins and the stated family with at most four coupled capacities; all walls and degree drops | Complete 22,063-subset / 16,848-local-value proof, three rational fields and independent whole counts; includes positive whole stabilized quotients along every actual direction dimension r>=1 in these exact families. Ordinary rank seven and unrestricted KTT remain open; the separate theorem covers rank at most six. |
| [Gap-three and two-row families](results/structural-positivity/README.md#whole-families) | Complete specified gap-three quadrant/cone; arbitrary positive weights in the slope-two and slope-three two-row channels | Whole-count identities and sign proofs, with finite numerical premises checked. General gap three and higher slopes remain open. |
| [Two-bank families](results/structural-positivity/README.md#whole-families) | All ordinary coefficients for the g=1, h=0 family at every m≥2; a positive linear coefficient throughout the full stated capped g domain | Exact whole formulas including walls. Other gaps and h>0 retain their open coefficient ranges. |
| [Transportation family and cone](results/structural-positivity/README.md#whole-families) | Every integer-h endpoint family is positive; the complete homogeneous nonnegative-parameter cone has c1≥5279u/360 and positive c16,c17,c18 | Seven endpoint polynomials and unused checks verified. Middle coefficients c2,...,c15 at noninteger v/u remain open. |
| [Uniform central two-row tensors](results/families-and-obstructions/README.md#positivity-at-arbitrary-size) | All n≥3, g≥1 with ng even, at the exact displayed ordinary triple | Symbolic all-parameter proof, both parities, independent finite controls; unequal weights require separate arguments. |
| [Matching layers and strict gaps one/two](results/families-and-obstructions/README.md#positivity-at-arbitrary-size) | Unbounded matching layers through min(q,r)=5; complete specified strict gap-one and gap-two strata | Exact shifts, full tableau identities and all 637 gap-two profiles. Larger matching layers and general gap three remain open. |
| [Rank-six Horn release](results/families-and-obstructions/README.md#positivity-at-arbitrary-size) | The complete displayed source–sink boundary family for 0≤s≤2M | Exact bivariate certificate with independent determining values and unused checks; not all rank-six triples. |
| [Clipped rank-eight region](results/families-and-obstructions/README.md#a-complete-rank-eight-positive-region) | The entire specified LR family across 0≤S≤2M | Complete tableau/lattice map and 253-term clipped-region polynomial; no whole-rank-eight assertion. |
| [Transportation c1 and near-corner theorems](results/families-and-obstructions/README.md#transportation-coefficient-theorems) | Small sides, 4-by-4 and 4-by-5 c1; unbounded cut regions; all coefficients in the near-corner family | Complete mathematical domains, source and independent 154-chamber 4-by-5 certificates included. |
| [Coupled-simplex cones and sparse constructor census](results/families-and-obstructions/README.md#positive-geometric-models-and-a-complete-constructor-census) | Two entire positive lattice models; all 5,861 original-box keys in the specified positive-R two-support grammar | Complete ray/maps and all 614 positive vectors included; the constructor census retains its finite scope. |
| [Three local rank-six cones](results/families-and-obstructions/README.md#three-earlier-local-rank-six-cones-with-their-full-domains) | Complete positive whole-count formulas and negative-real roots on their exact closed ray cones | All three 17-ray domains, parameter forms and integer lattice certificates supplied. |

## Geometric reductions and coefficient behavior

| Result | Established scope | Verification and limit |
| --- | --- | --- |
| [Complete five-height hive representation](results/five-height-hives/README.md) | Original rank-at-most-six hives with all 45 rows, two six-branch polygon kernels, one interval, 229 labelled projected comparisons and an integral lift; original-coordinate treewidth exactly five | Complete structural proof and small exact kernel, strict-field and projection controls. Fiber positivity alone does not sign a moving weighted sum. |
| [All-rank gap caps and zero-prefix reduction](results/gap-cap/README.md) | Whole-count-preserving gap cap/factorization; sharp outer-area bound `2 floor(n²/2) H` and at most `(n−1) F_(n+1)` closed rational pieces | Complete original-coordinate proof, all 65 rank-six matrix pieces and 32 binary vertices. Denominators remain unbounded; no finite unrestricted integer-search theorem follows. |
| [Entire saturated quotient positivity](results/rank-six-quotients/README.md) | Complete stabilized quotients along positive-dimensional feasible whole directions with final ordinary rank at most six; also the stated eventual segment threshold | Explicit stabilization, saturated-lattice transfer and parent coefficient bounds. A quotient is not assigned an ordinary LR rank. |
| [Stable flow–hive correspondence](results/structural-positivity/README.md#whole-families) | Complete integer affine map and interior-generation theorem on the specified stable M≥s≥0 domain | Geometric/counting theorem, with prior CRY/LR specialization credited. It does not prove all-rank coefficient positivity. |
| [Linear-coefficient nonconcavity and addition defect](results/linear-coefficient-geometry/README.md) | Actual rank-six c1 is neither concave nor superadditive: exact Jensen defect 1/336 and addition defect −1/168 | Strict original hives, six complete first-jet evaluations, exact rows/cuts/duals and a separate wall identity. The coefficients themselves remain positive. Earlier A14/Pro031 obstruction credited. |
| [Addition with a common two-row inner slot](results/linear-coefficient-geometry/TWO-ROW-ADDITION.md) | c1 is superadditive and monotone at every ambient rank for feasible whole parents with a two-row inner factor in the same fixed slot | Complete paired-interface proof, exact gains and whole-count controls. Independently changing slots or tensor symmetries is outside the theorem. |
| [Coefficient cone](results/coefficient-cone/README.md) | Sharp positive c1/c2 bounds on a rank-18 cone; c1 and sqrt(c2) are concave and superadditive | Exact complete chamber/wall verification. Higher coefficients in that cone remain unresolved. |
| [Two-row nonconcavity](results/two-row-nonconcavity/README.md) | Every index j≥2 admits raw weight-concavity failure | All-index argument and exact controls. Rooted-coefficient concavity and balancing monotonicity are not refuted. |
| [Interior surplus and its limits](results/families-and-obstructions/README.md#interior-surplus-theorems-and-their-limit) | Low-defect surplus/shifted-interior positivity, and full-polynomial positivity under an additional reflection law | Complete symbolic proofs and an integral negative-polytope challenge showing why the stronger conclusion needs its hypotheses. |

## Explicit examples and realization obstructions

| Result | Established scope | Verification and limit |
| --- | --- | --- |
| [Primitive rank-24 rectangular example](results/families-and-obstructions/README.md#a-primitive-rectangular-lr-polynomial) | The complete p=4,q=5 degree-20 polynomial is positive, with true codegree three | Full primitive-grading/section-ring premises and exact vector; no unrestricted rectangular-family theorem. |
| [Positive cone and root threshold](results/hurwitz-cone/README.md) | Degree 31; all 528 bivariate coefficients positive; an infinite region has roots in the open right half-plane | Full standalone exact reproduction. This refutes universal Hurwitz stability, not KTT positivity. |
| [R18 anchor](results/hurwitz-counterexample/README.md) | K_((7t,6t,5t),(t^18)) has 32 positive coefficients and exactly two roots in the open right half-plane | Full standalone exact reconstruction and root certificates; no minimum-rank claim. |
| [Parabolic A3](results/parabolic-a3/README.md) | Full LR realization; q1≥0 in every root direction for 24 multiplicity systems, q2≥0 for 16 | Complete specified chambers and exact reproduction. Other systems and higher coefficients remain open. |
| [Negative graphs and genuine LR faces](results/families-and-obstructions/README.md#negative-graphs-genuine-lr-faces-and-precise-obstructions) | Complete circulation sign families, including degree 18 with c1=−251/102; integral embeddings into LR faces | Entire graph/face result with evidence. The degree-480 LR parent remains uncomputed; no whole-LR negative is claimed. |
| [Precise realization obstructions](results/families-and-obstructions/README.md#negative-graphs-genuine-lr-faces-and-precise-obstructions) | Specified Euler-isometric quiver embeddings and direct affine-lattice flow realizations are impossible | The no-go scopes leave other maps, projections and equal-count constructions open. |

The structural section supplies the accepted theorem catalog, full selected
source proofs and [three standalone family checks](results/structural-positivity/replay/README.md).
Two-row finite proof cases and bounded character comparisons are freshly
computed. Gap-three and transport replay use exact historical count inputs
and regenerate complete coefficient algebra. The [dependency map](results/structural-positivity/replay/DEPENDENCIES.md)
states the full normal-atlas packaging and fresh-count replay work still open. The finite-box package has its own exhaustive reproduction interface.
The five older small modules run from the repository root with:

```sh
python3 -B reproduce.py
```

## Working with the results

The [families and obstructions collection](results/families-and-obstructions/README.md)
provides the precise statements, complete selected proof/certificate files and
verification limits for the additional major results. Its historical source
records are mathematical evidence, not new portable executions. The
[tool collection](tooling/README.md) supplies complete scalar methods,
selected whole-polynomial interfaces, geometric constructors and independent controls.
A successful scalar comparison verifies that value; it does not certify a
whole polynomial or its coefficient signs. Large positive panels retain their
exact finite scopes and are not extrapolated to all-size claims.

## What remains open and why it is worth pursuing

Whole ordinary rank seven and higher, unrestricted KTT positivity, and an
ordinary-negative entire LR polynomial outside the established domains remain
open. The rank-six theorem rules out such a negative at every size in rank at
most six. The earlier finite-box theorem supplies an additional rank-seven
terminal through outer size thirty.

Within rank six, smaller certificates, simpler positive constructions and
stronger structural explanations remain useful mathematical questions. A
four-letter-family sign proof is no longer needed to close rank six, although
its count formulas or stronger bounds could still be valuable. Higher-rank
three-letter, transportation, layered and capped families retain their exact
individual domains and open complements.

The strongest current proof directions are complete normal compensation,
uniform versions of the finite box's sign-completion bounds, and whole-count
or interior inequalities on unbounded chambers. Counterexample work must keep
the entire count and its cancellation: genuine parameter wings, irreducible
rank-seven domains beyond area 30, higher-rank couplings and legal whole
realizations of local defects remain serious routes.

The whole-rank-six result and its reusable mechanisms are the present preprint
focus. The finite-box theorem and the other families remain accessible as
independent supporting work. Journal suitability and novelty require external
assessment; neither follows from a benchmark consequence or internal review.
