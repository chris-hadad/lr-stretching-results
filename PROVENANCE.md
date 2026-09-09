# Discovery, verification and source provenance

GPT 6 Pro proposed the isolated R18 example and the subsequent construction,
root-family and coefficient-geometry results. Codex independently derived the
arguments and implementations used in the verification modules. Returned
programs were kept inert; these checkers are separately written from the
mathematics and explicit numerical witness data.

For the original R18 example, a fresh verification lane received only the
ordinary LR triple, established the degree/count method and sealed the
polynomial before comparison. For the later returns, independent reasoning
lanes read the proposed proofs and data after capture, then rederived formulas,
reconstructed polynomials/certificates and used additional counting models.
Those later lanes are not described as blind verification. Repeated sessions
of the same model are not different-model evidence or human peer review.

The complete source mapping for the included mathematical artifacts is
[SOURCE-MAP.json](SOURCE-MAP.json). It gives source commit, repository-relative
path, source SHA-256, included SHA-256 and any packaging transformation.

| Source repository | Pinned commit | Scope |
|---|---|---|
| stretched-lr-research | 57218642d9b758478feb8f6c847157ffb3dc10f2 | Original R18 package and earlier local-result catalog sources |
| stretched-lr-research | cf20c0d73c056df6b90faa5004de4f3ac444aa5c | Independent verification of CONSTRUCTIONS-002, ROOTS-003 and WILDCARD-004 |
| codex-workbench | 6ea08fe477742e4abe53082d4250802351dbfb63 | Prior framework and Ferudun source/route audit |
| AlperTheKing/ktt-positivity | c3a0795bd287dcca78fac2cc6ba4282144bb7813 | Ferudun's length-five theorem and prior Hurwitz discussion |

The source repositories' operational history is not needed to reproduce this
tree. No raw provider archive, private conversation, research-run history,
credentials or workflow configuration is included. The repository is a fresh
collection of selected mathematics and independently written checkers.

## What each reproduction establishes

- **R18:** 32 independently recounted determining values, three unused
  holdouts, ordinary-coefficient reconstruction and exact root certificates.
- **Root cone:** the full degree-bounded profile polynomial, all528 H
  coefficients, 23 exact Routh tables, seven uniform rational Rouche
  certificates, and separate literal-flow/positive-character controls.
  The 528 reconstruction inputs evaluate the proved profile polynomial;
  they are not a second native-tableau count grid.
- **A3:** complete independent grouped-flow reconstruction of all376
  ray/pair polynomials needed by the24 linear and16 quadratic certificates,
  including8,035 determining counts and752 unused positive holdouts;
  matrix and complete chamber-refinement checks.
- **Coefficient cone:** the entire nine-factor numerator, original flow
  polynomial, all28 coefficient chambers and29 actual walls, continuity,
  derivative signs and exact minima. Broader independent positive-GT count
  controls were performed in the source verification; they are not rerun by
  this focused certificate module.
- **Two-row:** independent positive count recurrences, symbolic and harmonic
  formulas, 90 strict midpoint gaps and endpoint checks. The all-index result
  follows from its proof, not a numerical extrapolation.

The root-cone and A3 data are selected mathematical witnesses and independently
reconstructed coefficient tables. Rational disk centers originated as numerical
proposals; every included root conclusion uses exact rational inequalities.
The coefficient-cone default program was adjusted during packaging to write no
files unless an output directory is explicitly supplied; its mathematics is
unchanged. The root module additionally rejects incomplete count rosters and
inexact count values; its root calculations are unchanged. The eight original R18 proof/data/code members retain their source
bytes and historical audit wording, with a new reader-facing README.

The three local rank-six formulas in RESULTS.md come from the source framework
and `methods/fra-2026-09-04/acceptance.md`; their complete cone definitions and
proof modules are not included. E34 identifies cone
393b7353283d7ab32e353e4fd8c1a049fcf67d64467b3d111f218b231229d31c.
The separately catalogued two-row linear theorem is sourced from
`methods/frontier-gpt6-pro-001/processed-return.md` and `method-amendments.md`.

No human expert has endorsed these results through this repository, and
historical novelty remains unresolved. AI assistance is disclosed without
assigning models human authorship. A future paper's authorship, licensing,
expert review and public release are separate owner decisions.

## Shared mathematical tooling — 9 September 2026

The tooling section is a versioned projection of maintained source at research
commit `5cd399564def6bd5ec4160471678ceaf0fda99dd`. Its source map covers the exact selected code, tests,
comparison fixtures, proof notes and measured benchmark data. Arithmetic is
unchanged during packaging; the initializer selects the standalone surface and
constructor provenance links are made local. Native execution adapters and the
census supervisor are excluded.

The new counters retain complete whole-object domains and exact integer
multiplicities. The Cdagger verifier replays all thirty-six implications against
the conventional hive. Existing native Fable oracle functions and selected
Codex support objects provide actual comparison inputs; executing these in
Codex does not claim native deployment or adoption of this version. Full source,
AI-assistance and licensing context is in [SOURCE-LICENSES.md](tooling/SOURCE-LICENSES.md).
