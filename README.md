# Littlewood–Richardson coefficient positivity

Proofs, exact computations and open questions about the coefficients of
stretched Littlewood–Richardson polynomials.

For partitions λ, μ and ν, with λ the outer partition, let
$`P(t)=c^{t\lambda}_{t\mu,t\nu}`$ for positive integers t. These integer values
come from a polynomial with rational coefficients. The King–Tollu–Toumazet
positivity conjecture asks whether its coefficients in ordinary powers of t
are always nonnegative.

**Main result: every ordinary coefficient is nonnegative when all three
partitions have length at most six, at every size and boundary.** The
[rank-six proof](results/rank-six-positivity/README.md) combines a complete
original-lattice normal-cycle argument with exact rational certificates.
The decisive realizability restriction removes sign constraints only after
proving their actual edge weights are zero. It yields a positive lower bound
of **1/2,000,000 times total actual lattice edge length** for the linear
coefficient.

The result includes nonsimple and lower-dimensional hives, padded lower ranks,
and every empty, point and actual-degree case. Rank seven and unrestricted KTT
positivity remain open. [The manuscript](papers/rank-six/README.md) develops
the geometric mechanism, scalar algorithms, coefficient assembly and provenance.
The strengthened theorem gives **strict positivity through the actual degree**
for every nonempty hive. Its complete exact finite premises have been checked,
with independent internal AI-assisted review and explicit source and execution records.

Alper Ferudun's rank-five theorem and normal-correction approach are important
antecedents, alongside the classical hive, polynomiality and Berline–Vergne
results. [Related work](results/rank-six-positivity/NOVELTY.md) and the
[contribution map](results/rank-six-positivity/CONTRIBUTIONS.md) distinguish those
inputs from the new mathematical and algorithmic steps.

## Start here

| Your purpose | Suggested route |
|---|---|
| Read the main result | [Rank-six statement](results/rank-six-positivity/README.md), [paper and PDF](papers/rank-six/README.md), [complete proof guide](results/rank-six-positivity/PROOF.md) |
| Verify it yourself | [Routes, data and costs](results/rank-six-positivity/VERIFYING.md); begin with the [five-second closure certificate](tooling/whole_rank_six/closure/README.md) |
| Explore other theorems | [Organized result catalog and open questions](RESULTS.md), with proof and verification links for every result |
| Count or construct examples | [Tool guide](tooling/README.md), [reproduction instructions](REPRODUCING.md), and [small examples](examples/sign_completion.py) |
| Understand the method and process | [Mathematical algorithms](results/rank-six-positivity/ALGORITHMS.md), [AI assistance](AI-ASSISTANCE.md), [formalization status](results/rank-six-positivity/FORMALIZATION.md) |
| Trace credit and evidence | [Contribution map](results/rank-six-positivity/CONTRIBUTIONS.md), [provenance](PROVENANCE.md), [references](REFERENCES.md) |

## Earlier results and reusable tools

The [complete finite-box theorem](results/finite-box/README.md) covers every
legal balanced triple of length at most seven and outer area at most thirty.
It remains a separate result with its own proof, data and external rank-five
premise. The [transportation and capped families](results/transport-capped/README.md)
include positive families above rank six. The [three-letter theorem](results/three-letter-rank-six/README.md)
retains its stronger family-specific bounds and count tools. The
[c4/c5 module](results/rank-six-coefficients/README.md) remains a compact
standalone component of the whole rank-six proof.

New supporting work includes the [complete five-height hive representation](results/five-height-hives/README.md),
an [unbounded-rank layered positive family](results/layered-triangle/README.md),
and [complete saturated quotient consequences](results/rank-six-quotients/README.md).
The collection also includes [all 4×5 transportation margins](results/transport-four-by-five/README.md),
[five-capacity LR families](results/five-capacity/README.md),
[all-rank gap caps](results/gap-cap/README.md), and
[sharp linear-coefficient obstructions and restricted addition](results/linear-coefficient-geometry/README.md).
Each has its own precise mathematical domain and verification route.

## Small reproducible checks

With Python 3.11 or later, from the repository root:

```sh
python3 -B examples/sign_completion.py
python3 -B reproduce.py
```

The first command derives the quintic coefficient identities used in the proof
and checks an illustrative lattice-simplex polynomial. The second runs the
five earlier standalone modules: a Hurwitz-instability example, its infinite
positive cone, parabolic A3 certificates, a coefficient cone, and two-row
nonconcavity. Both use only the Python standard library and make no network
requests. Neither reproduces the finite-box theorem.

For the complete small rank-six components, use
`python3 -B tooling/whole_rank_six/verify.py small --out /path/to/new-small-run`
with C++17 and GMP. This checks c6–c9; it does not certify the lower-coefficient
components. The [main verification guide](results/rank-six-positivity/VERIFYING.md)
separates this short route from the larger original-action checks and full
scalar regeneration. [REPRODUCING.md](REPRODUCING.md) gives the distinct routes
for the earlier finite box, families and other independent modules.

## What else is in the collection?

The result catalog includes unbounded positive families, normal-correction
theorems, actual low-degree results, transportation models and exact obstacles
to possible proof strategies. For example, an entire LR polynomial can have
positive ordinary coefficients and roots with positive real part. That
refutes universal Hurwitz stability without refuting coefficient positivity.
A negative graph polynomial, local weight or auxiliary quotient is also kept
distinct from a negative coefficient of an entire LR polynomial.

Every catalog entry links its hypotheses, mathematical argument, available
certificates, reproduction level and open complement. The guides distinguish
fresh counts, complete certificate replay, analytic premises and historical
controls, so readers can choose the evidence relevant to their question.

This is substantially AI-assisted research directed by Chris Hadad. The
[AI-assistance account](AI-ASSISTANCE.md) describes the models, research
environments, persistent plans and shared process used since July 2026. Separate
implementations and AI reviews have checked the stated finite premises and
arguments; external human mathematical review is still sought. No institutional
endorsement or historical novelty determination is implied. This collection records initial findings and provides a basis for
further results. See [versions and citation](SHARING.md) for citing a precise
research note, source snapshot or dataset.


## License

Software and executable examples are available under [MIT](LICENSE).
Research notes, proofs, documentation and data are available under
[CC BY 4.0](LICENSES/CC-BY-4.0.txt). See [licensing and attribution](LICENSING.md)
for the scopes, release archives and credit information.
