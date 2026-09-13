# Implementation sources and verification

These tools were developed in the underlying research software and adapted
into a standalone package. [SOURCE-MAP.json](../SOURCE-MAP.json) records source
versions, original and included hashes, and the transformations used here.
Mathematical exposition has been edited for this collection; executable code
and numerical data retain their stated source versions.

The transport, strip and certificate implementations were developed with
Codex assistance from the mathematical arguments cited in the proof notes.
They are separate implementations from the initial programs proposed with
those arguments. Some comparison tests use earlier chart functions developed
with Claude, with small standard-library wrappers. Each comparison identifies
which algorithms and inputs it uses.

The hive, skew-content, matrix-invariant and support-planning components have
their own source records and mathematical contracts. The sparse Cdagger data
retain every domain row and all thirty-six implication identities. The verifier
reconstructs the complete hive matrix and checks the integer chart and each
implication.

The skew-tableau counter uses partial-row aggregation and exact pruning. It
was checked against forward and row-sweep methods, literal small tableaux and
specified research inputs. Historical source timings and fresh paired
measurements are distinguished in [BENCHMARKS.md](BENCHMARKS.md). Agreement at
selected scalar values does not authenticate a full high-degree polynomial.

The mathematical antecedents include the LR hive/tableau correspondence,
network flows and total unimodularity, the transportation Minkowski criterion,
rising-binomial identities and the stated whole-polytope constructions. The
proof notes distinguish these premises from finite checks and open extensions.
[PROVENANCE.md](../PROVENANCE.md) explains AI assistance and verification scope.

The standalone code uses Python's standard library. Optional Sage hooks in
`hive.py` are not used by the examples or checks. No third-party implementation
is bundled as an undeclared dependency.


The program sources and executable examples are licensed under
[MIT](../LICENSE). The explanatory notes and mathematical data use
[CC BY 4.0](../LICENSES/CC-BY-4.0.txt), with the scopes and attribution
requirements described in [LICENSING.md](../LICENSING.md).
