# Whole families, coefficient theorems and obstructions

This collection includes unbounded positive LR families, complete low-degree
classes, geometric count models, and examples that distinguish a negative
auxiliary polytope from a negative entire LR polynomial. The statements retain
their documented verification limits. No historical novelty or human peer-review
claim is made.

[ACCEPTED-SCOPES.json](ACCEPTED-SCOPES.json) preserves the precise mathematical
claims and verification levels. [SOURCE-MAP.json](SOURCE-MAP.json) binds the
selected proof and data files to their sources. Two rectangular proof
links are relocated in this edition without changing mathematical statements;
[the exact link projection](../../DOCUMENTATION-ADAPTATIONS.json) preserves
the earlier and current hashes. The original nonvanishing result is included. The complete
mathematical evidence is available for inspection; these historical records
are not new executions of a portable checker. The [tool collection](../../tooling/README.md)
provides usable counters and selected complete polynomial/certificate interfaces.
The [finite-box module](../finite-box/README.md) has its own exhaustive replay.

## Positivity at arbitrary size

| Result | Exact scope and useful consequence | Proof and evidence |
|---|---|---|
| Actual cubics through rank seven | Every whole LR polynomial of maximum ordinary rank at most seven and actual degree at most three is coefficient-nonnegative, at every size. This includes degree drops. | [Boundary-face proof](proofs/actual-cubics.md); [complete orbit certificate](data/actual-cubics/A005-FACE-ORBITS-001.json), the rank-six witnesses and all 32 rank-seven witness shards in `data/actual-cubics/`. The complete verification covered all 8,520 witnesses. |
| Uniform central two-row tensors | For n≥3, g≥1 and even ng, λ=(ng,(n−1)g,…,g), μ=((n−1)g,…,g), ν=(ng/2,ng/2), all coefficients through actual degree n−3 are positive. Both parity cases are included. | [All-parameter proof](proofs/uniform-two-row.md); [independent finite controls](data/astra-five/A005-UNIFORM-TENSOR-001.json). Unequal weights require another argument. |
| Six-run matching layers | The complete unit-flank family is positive for min(q,r)≤5, with arbitrary positive end runs and common positive integral dilation. A negative member of this constructor needs q,r≥6, displayed rank at least 21 and degree at least 95. | [Two new unbounded layers](proofs/matching-layers.md), [earlier layers](proofs/matching-three-layers.md), [positive-shift identity](proofs/matching-positive-shifts.md), [scope and bridge dependencies](proofs/matching-scope.md); exact rational controls in `data/astra-five/`. |
| Complete rank-six Horn release | With ρ=(5,4,3,2,1,0), μ=ν=Mρ and λ=2Mρ−s(1,0,0,0,0,−1), all coefficients are nonnegative for integers M≥0 and 0≤s≤2M. | [Whole-family proof](proofs/rank-six-horn-release.md); [63 positive bivariate terms](data/astra-five/A005-HORN-FIT-001.json), 66 determining sites and two unused checks. Degree is ten inside, eight at s=2M>0, and zero at s=0. |
| Strict gap one | The strict five-row, six-positive-label Kostka/LR stratum with strict dominance and Δ3=1 has the complete factorization binom(t+8,8)(1+pt)(1+qt), with p,q the exact source-defined minima. | [All-stretch tableau/interior proof](proofs/gap-one.md), with the [staircase premise](proofs/gap-staircase.md). The proof states the complete α,β and LR-lift conventions. |
| Strict gap two | Under the corresponding strict hypotheses and Δ3=2, every whole polynomial coefficientwise dominates binom(t+7,7)(t+4)(t²+8t+9)/36. | [Complete branching](proofs/gap-two-branching.md), [profile exhaustion](proofs/gap-two-profiles.md), [positive baseline](proofs/gap-two-positivity.md), and [all 637 inhabited profiles](data/gap-two/profiles.json). The stated determinant-column extension is included. |

Here ordinary rank is measured on the final ordinary triple, with λ outer,
after trailing zeros are removed. It is distinct from the number of active
flow variables, the number of skew rows, or polynomial degree. Source-defined
strictness and boundary hypotheses remain part of each theorem.

The matching family also includes its [complete character bridge](proofs/matching-whole-bridge.md),
[nonnegative-parameter character premise](proofs/matching-character-premise.md),
and [exact operator coefficients](data/astra-five/matching-operator-certificate.json).

For gap two, the [marginal-count derivation](proofs/gap-two-marginal-count.md)
is useful independently of positivity. It reduces the complete branching count
to one-column marginals while retaining every cap, single/pair hinge and
determinant-overlap term. It supplies no generic gap-three oracle.

## A complete rank-eight positive region

For the explicit family

```text
lambda = (50M-S,46M,36M,32M,23M+S,19M,9M,5M),
mu     = (27M,23M,19M,15M,13M,9M,5M,M),
nu     = (25M,22M,19M,14M,12M,9M,6M,M),
```

the [whole tableau map and compensation proof](proofs/rank-eight-map.md)
establish positivity for integers M≥S≥0. The
[clipped-region argument](proofs/rank-eight-polynomiality.md), using the
[complete aggregation](proofs/rank-eight-aggregation.md), extends positivity
through 0≤M≤S≤2M. In the latter region, u=2M−S and v=S−M give a polynomial
of degree at most 21 with all 253 ordinary bivariate coefficients positive.
The nonzero ray polynomials are positive; the origin gives one.

The [full coefficient table](data/rank-eight/FRI-R8-BIVARIATE-001.json),
[253 independent determining sites](data/rank-eight/FRI-R8-COLUMN-POISED-001.json)
and [four unused sites](data/rank-eight/FRI-R8-COLUMN-HOLDOUTS-001.json) are
included. There is no S>2M or whole-rank-eight assertion. The maintained
`rank8_clipped` tool exposes the specified count/certificate contract.

## Transportation coefficient theorems

The [whole transportation/LR bridge](proofs/transport-whole-lr-bridge.md)
retains the entire polytope and its integer lattice. For positive balanced
p-by-N margins, the complete linear coefficient is positive when
min(p,N)≤3, and also for 4-by-4 and 4-by-5 margins and their transposes.
The sharp positive-integral minima in the last two cases are 65/18 and 325/72.

Read the [small-side argument](proofs/transport-small-side.md),
[4-by-4 formula](proofs/transport-four-by-four.md), and
[4-by-5 theorem](proofs/transport-four-by-five.md), with its
[positive double-cut premise](proofs/transport-double-cuts.md). The last result
uses all 22 multiplicity systems and seven A3 chambers for each system. Both
the [154-chamber source certificate](data/transport/four-by-five-source.json)
and [independent reconstruction](data/transport/four-by-five-independent.json)
are supplied. The [seven-cone mathematical premise](proofs/transport-a3-premise.md)
is separate from fitting or a favorable baseline value.

There are also unbounded margin regions where the complete linear coefficient
equals an explicit positive weighted double-cut sum. The
[whole-region proof](proofs/transport-cut-regions.md) covers a minor-row total
at most the two smallest columns' sum. For four rows, the
[enlarged region with two margin conditions](proofs/transport-two-gates.md) needs only
`r4 <= c_(1)` and `r3+r4 <= c_(1)+c_(2)` after the stated row ordering.
Outside the proved regions, the higher-class remainder remains part of c1.

A stronger [near-corner theorem](proofs/transport-near-corner.md) proves every
ordinary coefficient positive for arbitrary m≥3 minor rows a_i>0 and N≥2
columns satisfying `c_j >= A-min(a_i)`, where `A=sum(a_i)` and the major row
`sum(c_j)-A` is positive. Its degree is m(N−1), and its displayed LR rank is
m+N. These whole-family conclusions differ from the separate 4-by-7 family
and homogeneous cone in the [structural result collection](../structural-positivity/README.md).

## Positive geometric models and a complete constructor census

The [two coupled-simplex cones](proofs/coupled-simplex.md) have entire
ten-dimensional saturated-lattice models and explicit positive parameter
polynomials with 54 and 38 terms. Their exact 17-ray domains, maps and all
transformed inequalities are in the corresponding `data/coupled-simplex/`
geometry records; complete count derivations are supplied beside them. These
examples demonstrate positive coupled fibers beyond direct products.
The [separate count derivation](proofs/coupled-simplex-independent-count.md)
and the [source identities](data/coupled-simplex/source-manifest.json) are included.

The positive-R two-support grammar has a [complete constructor proof](proofs/sparse-constructor.md)
and [final closure](proofs/sparse-complete.md), with the
[nonnegative-parameter extension](proofs/sparse-nonnegative-parameters.md).
Within its original-box census there are exactly 5,861 canonical keys:
1,848 empty families, 3,399 cases covered by proofs and 614 complete positive vectors.
The [canonical roster](data/sparse/canonical.json),
[parameter grammar](data/sparse/parameters.json),
[614-vector residual](data/sparse/residual-614.json), continuation maps and
all 614 completed vector records are included in `data/sparse/`.
The first 64 and the last 550 have complete vector records; earlier incomplete
attempts supply no replacement evidence.
This is a finite constructor census, not arbitrary-size two-support positivity.

## A primitive rectangular LR polynomial

The three-matrix 4-by-5 example has
`lambda=(42^8,35^4,18^7,14^5)` and `mu=nu=(28^8,14^8)`, where exponent
notation means repeated parts. Its ordinary rank is 24, outer area 672,
actual degree 20 and true codegree three. The whole polynomial is
`P(t)=(t+1)(t+2)Q(t(t+3))`, with all ten coefficients of Q positive;
all 21 ordinary coefficients of P are positive.

The [primitive grading and full LR premises](proofs/rectangular-premises.md)
and [complete tableau model](proofs/rectangular-tableau.md) are essential:
the original entry degree is 20t. The
[complete independently reconstructed polynomial](data/rectangular/full-polynomial.json)
is supplied. Two complete models agree at grades 0 through 11, with grades
10 and 11 unused in reconstruction. A timed-out third native attempt provides
no additional value. This example supplies no unrestricted rectangular-family
positivity theorem.
The earlier [rectangular bridge](proofs/rectangular-bridge.md),
[canonical/section-ring argument](proofs/rectangular-canonical.md), and
[exceptional-pair extension](proofs/rectangular-extension.md) supply the
explicit dependencies used by the primitive case.

## Negative graphs, genuine LR faces and precise obstructions

The [bounded-circulation theorem](proofs/negative-graphs-and-lr-faces.md)
gives complete graph Ehrhart polynomials with negative ordinary coefficients.
In particular C_(15,3) has degree 18 and linear coefficient −251/102.
For C_(n,1), the complete all-index sign rule gives unboundedly many negative
coefficients as n grows. [Exact evidence](data/negative-graphs/evidence.json)
and integral affine embeddings into genuine LR faces are included.

The explicit degree-18 face lies in a rank-48, area-2,593 LR parent of degree
480. That entire parent polynomial remains uncomputed. Face negativity and
whole-parent negativity are distinct: this is a structural obstruction to
several easy positivity arguments, with no KTT counterexample claimed.

Two useful limits on attempted transfers are also proved. The
[Euler-form obstruction](proofs/euler-embedding-obstruction.md) excludes the
specified higher-index negative-flow quivers from Euler-isometric exceptional-
sequence embeddings into three-arm LR flag quivers. It leaves other maps and
single Hilbert-function identities open. The
[primitive-edge obstruction](proofs/flow-lattice-obstruction.md) excludes
the stated Q_ab lattice models from direct affine-lattice realizations as
complete standard single-commodity network flows when max(a,b)>2. It leaves
projections, sections and different equal-count constructions open.
The complete [source Euler-form calculation](proofs/euler-source.md) is included.

## Interior-surplus theorems and their limit

For a nonempty rational period-one polytope of actual dimension d and true
codegree q, the complete surplus `I(t+q)-P(t)` is coefficient-nonnegative when
`d-q+1 <= 4`. At residual degree at most three, its reflected average and
shifted interior polynomial are strictly positive. The
[interior-surplus proof](proofs/interior-surplus.md) uses complete interior
translation and exact reflection parity; it does not assume a nonnegative
h-star numerator. With the additional full codegree-q reflection and
`q >= d-2`, the [low-defect factorization](proofs/low-defect-reflection.md)
proves positivity of P itself.

Those qualifications matter. The
[twice-pyramided Reeve example](proofs/negative-pyramid-challenge.md) has
`P(t)=binom(t+5,5)+46 binom(t+3,5)`, with ordinary coefficients
`c1=-1/60` and `c2=-1/24`, even though its shifted-interior surplus and reflected
average are positive. This is a complete integral five-polytope, with no LR
realization asserted and no novelty claim. It explains why an interior criterion needs additional structure to establish
positivity for whole LR polynomials.

## Three earlier local rank-six cones, with their full domains

Let β concatenate the six padded λ, μ and ν coordinates, with λ outer.
Each domain is the set of integral β in the real nonnegative span of its
certificate's 17 explicit rays. The ray matrices are part of the theorem;
nonnegative values of a few displayed parameters do not define the domain.

| Cone | Complete polynomial | Exact domain and proof |
|---|---|---|
| E32, chamber `3103fe3d0905e0a2aff0f4548e1eae8272d87ff901888888837353ddf29eed39` | `((x+1)(y+1)(x+y+2)/2) binom(z+7,7)` | `rng32` in [the certificate](data/local-cones/first-two.json), with [the proof](proofs/three-local-cones-first-two.md) |
| E33, chamber `e696628ff86a1ce2048f731e90fd6ab8120385a81fe395d56f3c56fa70c900a7` | `(x+1+z/3)(y+1+z/3) binom(z+8,8)` | `rng33` in [the certificate](data/local-cones/first-two.json), with [the proof](proofs/three-local-cones-first-two.md) |
| E34, chamber `393b7353283d7ab32e353e4fd8c1a049fcf67d64467b3d111f218b231229d31c` | `(b+1)(c+1)(a+1+(b+c+z)/2) binom(z+7,7)` | `rays` and `model.parameters` in [the certificate](data/local-cones/third.json), with [the proof](proofs/three-local-cones-third.md) |

The certificates give every parameter as an exact linear form in β, together
with the full integer chart and transformed inequalities. Substitute the
scaled parameters to obtain a ray's stretching polynomial. Every ordinary
coefficient is nonnegative, and all roots on nonconstant rays are real and
negative. All three original-box intersections have degree at most two.
The coupled-simplex models above refer to different cones.

## Reading and verification

Each proof above states the full mathematical domain. The data include complete
coefficient vectors, witness rosters or chamber certificates where the proof
needs them. The claim index records the verification level of each result.
Source identifiers in the certificates identify earlier evidence; they are not
portable execution paths.

Some source checkers need an explicit path adaptation before their historical
commands can be rerun from this tree. The usable tool APIs and the finite-box
replay are documented separately. No command here is advertised as freshly
replaying every family certificate. Independent human review, a literature
priority audit and journal acceptance remain future assessments.

The source arguments use substantial prior LR/hive, Ehrhart, quiver, character,
reciprocity and valuation mathematics. See the repository
[references](../../REFERENCES.md) and the citations in each source proof.
Alper Ferudun's rank-four/five results are central prior inputs. The
[AI-assisted discovery and verification](../../PROVENANCE.md) are explicit.
