# Three-letter LR certificates

This module reproduces the finite certificate in [PROOF.md](PROOF.md) from
standalone mathematical inputs. The complete tableau model is in
[MODEL.md](MODEL.md); [INTERIOR.md](INTERIOR.md) and
[HESSENBERG.md](HESSENBERG.md) give the companion identities.

The full command reconstructs all 1,149,016 original normal subsets, checks
395,657 complete image-lattice and Gram types, recomputes every exact BV
constant, and checks all 664,539 original rows of the four ambient fields.
It retains dependent subsets, nontrivial image indices, every finite numerator,
every proper-face term, the degree-six Bernoulli term, and every omitted zero
field support. The common checked margin is `1/100000000`.

Requirements are Python 3.11 or newer, a C++17 compiler, GMP headers and
libraries, and a POSIX system with `waitid` and `WNOWAIT` (tested on macOS).
The verifier does not install software. Use a fresh output directory:

```sh
python3 verify.py full --output /path/to/new-run
```

Use `--gmp-prefix /path/to/gmp` when GMP is outside the compiler's usual search
path, or `--cxx /path/to/compiler` to select the compiler. The defaults allow
600 cumulative native seconds and 900 program seconds; the optional
`--native-seconds` and `--program-seconds` flags change those limits. Each
native child has a hard 60-second deadline; compilation and other program
children have deadlines of at most 120 seconds. Budget exhaustion is a refusal,
and a reused output directory is refused.

`COMPLETE.json` is written only after every required population, exact value,
field inequality, source check, and owned-child cleanup passes. It records
source and artifact hashes, actual counts, exact minima, and resource usage.
Completion and abort records are serialized before an exclusive temporary
file is written in the output directory. The temporary is flushed and closed
before an atomic rename publishes the complete record. Failures or interruptions
before publication retain staged evidence without publishing a complete marker;
malformed completion bytes cannot suppress abort evidence. The compressed input constants are comparison data: the full command
recomputes all of them and does not adopt a producer's receipt as proof.

Run the targeted semantic and process controls using an unchanged completed
run from this package:

```sh
python3 controls.py --verified-output /path/to/completed-run --output /path/to/new-controls
```

The controls cover missing rows, corrupted row indices and Gram data, a wrong full lattice
with unchanged index, missing Bernoulli degree six, omitted field correction,
changed sources, real deadlines, and cumulative-budget refusal. Finalization
controls exercise serialization and rename failures, partial temporary writes,
normal atomic publication, and interruptions at the publication boundary. They send
SIGINT, SIGTERM, SIGHUP, and SIGQUIT to the actual outer verifier process and
verify that its compute child and grandchild exit. `--runtime-only` runs the
process and source controls without requiring a completed mathematical run.
A controls report does not substitute for a full verification.

The actual outer CLI owns its compute processes directly. Launched programs
must retain their assigned process group; this is process containment, not a
sandbox for programs that deliberately detach. Ordinary termination signals
are handled through cleanup. SIGKILL and machine loss cannot run cleanup code.

`model.py` exposes the original affine model and its lattice inverse.
`hessenberg.py` and its sibling `affine.py` provide the bounded exact symbolic
helper described in HESSENBERG.md. They have no dependency on a private checkout.
The full certificate command makes no bare LR, tableau, or hive-count calls.
The mathematical implication and its exact family boundary are stated in
PROOF.md; a numerical success marker does not broaden that boundary.
