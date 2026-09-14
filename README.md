# Littlewood–Richardson stretching

Proofs, exact computations and open questions about the coefficients of
stretched Littlewood–Richardson polynomials.

For partitions λ, μ and ν, with λ the outer partition, let
$P(t)=c^{t\lambda}_{t\mu,t\nu}$ for positive integers t. These integer values
come from a polynomial with rational coefficients. The King–Tollu–Toumazet
positivity conjecture asks whether its coefficients in ordinary powers of t
are always nonnegative.

**Main result: every such coefficient is nonnegative if
$|\lambda|=|\mu|+|\nu|\leq30$ and all three partitions have length at most seven.**
The collection gives a computer-assisted proof, the exact certificates and
independently written verification programs. Thus the counterexample requested
within the [posted FrontierMath bounds](https://epoch.ai/frontiermath/open-problems/stretched-lr-coefficients)
does not exist. Positivity at arbitrary size in ranks six and seven, and the
unrestricted conjecture, remain open.

Alper Ferudun's all-size positivity theorem through rank five is an essential
prior result. The new finite calculation handles the remaining rank-six/seven
inputs using whole-count reductions, relative-interior counts and rigorous
coefficient bounds. [Prior work and precise dependencies](REFERENCES.md) are
part of the proof, including the limits of our independent reproduction.

**Rank-six progress:** the fourth and fifth ordinary coefficients are now
nonnegative at every area and boundary. A [new result page](results/rank-six-coefficients/README.md)
gives the full scope and low-degree consequences, with a
[complete standalone verifier](tooling/rank6_certificates/README.md) and compact
certificate data. The first three coefficients remain the whole-rank-six
question. This is a partial advance alongside the completed finite-box theorem.

## Start here

| Your purpose | Suggested route |
|---|---|
| Understand the finite result | [Research-note draft](papers/finite-box.md), then the [detailed proof](results/finite-box/PROOF.md) |
| Check the argument | [Guide for mathematical review](results/finite-box/REVIEWER-GUIDE.md), [dependencies](results/finite-box/DEPENDENCIES.md), and [verification guide](REPRODUCING.md) |
| Try a small exact calculation | [Sign-completion example](examples/sign_completion.py) or the five established standalone modules below |
| Explore the wider mathematics | [Results and open questions](RESULTS.md), [structural families](results/structural-positivity/README.md), and [companion outline](papers/families-and-compensation.md) |
| Use the counting code | [Tools organized by mathematical object](tooling/README.md) |
| Understand how the work was done | [AI assistance and research process](AI-ASSISTANCE.md), [finite-box methodology](METHODS.md) |
| Trace contributions and sources | [Result-specific attribution and verification scope](PROVENANCE.md) |

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

The [complete finite verification](results/finite-box/README.md) has ten data
archives, a C++17 compiler requirement, and substantial disk and runtime needs.
[REPRODUCING.md](REPRODUCING.md) distinguishes extraction, inventory, fresh
sample counts, algebra checks and exhaustive verification. It also explains
which commands have actually been run.

## What else is in the collection?

The result catalog includes unbounded positive families, normal-correction
theorems, actual low-degree results, transportation models and exact obstacles
to possible proof strategies. For example, an entire LR polynomial can have
positive ordinary coefficients and roots with positive real part. That
refutes universal Hurwitz stability without refuting coefficient positivity.
A negative graph polynomial, local weight or auxiliary quotient is also kept
distinct from a negative coefficient of an entire LR polynomial.

Every catalog entry links its hypotheses, mathematical argument, available
certificates, reproduction level and open complement. Some large historical
certificates still have source-proof documentation without a standalone replay;
the catalog states that limitation.

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
