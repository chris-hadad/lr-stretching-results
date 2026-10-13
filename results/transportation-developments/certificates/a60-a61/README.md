# Complete A60/A61 finite theorem certificates

This directory supplies every finite certificate required by the two
mathematical arguments. It uses Python 3 and its standard library only.
From any working directory, run the checker with a fresh output directory:

```
python3 -B check_certificates.py --output /path/to/new-certificate-output
```

The complete package includes:

- A60's forty base records: seven at a=3, thirteen at a=4 and twenty at a=5.
  All thirty-one applicable first large-cap derivatives are present. Nine
  bases have no large-cap direction; their derivative is explicitly absent.
  Every ordinary coefficient through the prior actual degree is retained,
  including each derivative's zero constant. The a=6 full dominance bases,
  all twelve recorded factor controls and five complete reserve controls are
  also preserved and replayed.
- A61's five entire four-variable degree-eight chamber polynomials and all
  fifteen entire fixed-total cap-balancing polynomials. Missing sparse entries
  mean zero, and replay writes the full dense zero/nonzero fields. It checks
  every pure-power strictness certificate used in the proof, integral
  unimodularity of each chamber, both Gauss/Cramer directions and all four
  complete shared-wall identities.
- The five full historical independently reconstructed coefficient maps and
  their thirty originally recorded holdouts. They are reused records, not new
  observations. No count reconstruction, LR/table oracle or bare-original
  count is run by this checker.

The mathematical dependencies are the full retained arguments in
[the A58 character/first-wall proof](../../proofs/A58-FIRST-WALL-PROOF.md),
[the A59 balanced-cap proof](../../proofs/A59-BALANCED-CAPS-PROOF.md),
[the A60 complete deficit-three proof](../../proofs/A60-K3-RESERVE-PROOF.md), and
[the A61 uniform/three-cap proof](../../proofs/A61-UNIFORM-PROOF.md).
Their original domains, paired-width floors, actual degrees, zero rows, ties,
common scaling, complete cap/budget intersections and same-coefficient
compensation remain explicit. The higher coefficients for arbitrary a>=4,
below-half-budget tails, whole rank seven and unrestricted KTT remain open.
A formal degree-eight chamber field does not assign degree eight to a collapsed
physical zero/point face.

The generators are mathematical ports of the accepted root code. Their
function bodies are unchanged; the A60 arithmetic module contains only the
complete rational polynomial primitives, with counting/engine/runtime code
excluded. The historical map audit uses its original exact Cramer arithmetic.
This fresh replay is not a newly independent method, new original count,
newly unused observation or additive coverage. The unbounded quantifiers come
from the complete written arguments and their structural reductions, not from
sampling positive inputs.

All three required original certificate JSON files are byte-preserved.
PROVENANCE.json lists original hashes, complete function-extraction spans,
path-only adaptations and private-prose exclusions. The independent map export
removes only top-level absolute source locators; all coefficient/holdout objects
remain complete. MANIFEST.json authenticates every code/data/proof input before
replay. No private filesystem path, optional library, service, runtime policy
or original LR engine is needed.

Replay also saves full signed correction/payment fields and meaningful controls:
missing an A60 base, A61 chamber or balancing polynomial; a wrong input hash;
and omission of the entire compulsory pair correction in each family. A
changed auxiliary coefficient or invalid formula is not an LR counterexample.
