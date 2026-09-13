# Littlewood–Richardson stretching: proofs, results and exact verification

This collection documents a substantially AI-assisted mathematical research
campaign. Its main result is a computer-assisted proof that **the original
FrontierMath search box contains no counterexample**: every ordinary coefficient
is nonnegative when the outer partition has area at most 30 and all three
partitions have length at most seven. The unrestricted King–Tollu–Toumazet
positivity conjecture remains open, as do whole ranks six and seven.

Start with the [finite-box result](results/finite-box/README.md), its
[readable proof](results/finite-box/PROOF.md), and its verification instructions.
The proof covers every legal input, including empty cases and boundary strata.
It combines exhaustive reductions, exact closed/interior counts, coefficient
bounds and full vectors for the final tail. Complete data are distributed
separately from the small proof and code tree, with exact checksums.

**Alper Ferudun's positivity theorem through rank five is a central prior
result and an explicit dependency.** His theorem and correction methods,
along with the classical and recent mathematics used throughout the campaign,
are credited in [REFERENCES.md](REFERENCES.md). This repository does not claim
those contributions as its own.

| Where to go | What it contains |
|---|---|
| [Results and open questions](RESULTS.md) | Major theorems, exact domains, verification levels and unresolved questions |
| [Finite-box proof](results/finite-box/PROOF.md) | Why the bounded counterexample cannot exist and how the proof works |
| [Structural positivity](results/structural-positivity/README.md) | Normal corrections, boundary-coordinate theorems and whole-family results that guide the continuing search |
| [Families and obstructions](results/families-and-obstructions/README.md) | All-size low-degree theorems, unbounded positive families, exact cone domains, negative graph/LR faces and their complete selected evidence |
| [Exact tooling](tooling/README.md) | Complete LR/tableau and transportation counters, constructors, examples and proof premises |
| [Discovery and verification](PROVENANCE.md) | Human direction, AI assistance, independent checks and source identities |

The earlier standalone modules include a positive infinite LR family with
an exact transition to roots in the open right half-plane. That result rules
out universal Hurwitz stability as a proof strategy; it is not a negative
ordinary coefficient. The catalog keeps such obstructions distinct from
positivity theorems and genuine counterexample candidates.

The broader collection also includes the all-size actual-cubic theorem through
rank seven, uniform central two-row tensors, matching layers, strict gap
families, the full rank-six Horn release, an explicit clipped rank-eight region,
transportation coefficient theorems, and a primitive rank-24 example. Each has
its exact hypotheses and proof/evidence links in the result catalog. The tools
are organized by the mathematical object they count, with small examples and
explicit domain and verification limits.

The five small established modules run with Python 3.11+ and its standard
library, without network access or writes:

```sh
python3 -B reproduce.py
```

The much larger finite-box verification has its own explicit data, compiler,
workspace and resource instructions. The quick command above does not replay
the entire box. Each module states exactly what its commands establish.

The repository is currently private. Campaign mathematical and computational
review is complete for the accepted results at their stated scopes; independent
human review, historical novelty, publication and FrontierMath's own disposition
are separate matters. The campaign continues toward whole-rank positivity,
unrestricted KTT positivity and a rigorous ordinary-negative entire LR object
outside the closed box.
