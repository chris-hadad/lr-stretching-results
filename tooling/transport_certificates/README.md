# Whole transportation and capped-family certificates

This compact module verifies every ordinary coefficient of every balanced nonnegative 3-by-5 transportation polytope, including smaller and transposed sizes, and the stated whole LR family with at most four coupled capacities. It includes all margins, walls and actual degree drops. The [complete proof](PROOF.md) gives the entire LR constructors: rank-six degree-six transport, rank-seven degree-eight transport, and rank-six degree-seven capped families. Whole ordinary rank six/seven and unrestricted KTT remain open.

The three complete rational correction fields occupy about 58 KB. Verification requires Python 3.11 or later and only its standard library. Choose a fresh output directory with an existing parent, outside this source module:

```sh
python3 -B verify.py --out /path/to/new-transport-check
```

Success is `PASS_COMPLETE_TRANSPORT_AND_CAPPED_CERTIFICATES` in RESULT.json. The command independently generates all 22,063 original normal subsets, including 5,215 dependent subsets; reconstructs all 16,848 independent local constants with their original lattice and metric; and checks every rational inequality at every coefficient. The output preserves all original rosters, local negatives, corrected values and source hashes. A partial/interrupted run has no complete result. The Python verifier creates no child processes.

An independently written C++/GMP recurrence can replay every local constant from the complete Python run. Requirements are C++17 and GMP development headers/libraries:

```sh
python3 -B compare_cpp.py --python-run /path/to/new-transport-check --out /path/to/new-cpp-check
```

For GMP in a nonstandard location, add `--include-dir /path/to/gmp/include --library-dir /path/to/gmp/lib`. Runtime library search paths are set explicitly. Every native child is limited to 60 seconds, compilation to 120 seconds, and cumulative child time to 360 seconds. Handled termination signals stop and wait the active child. The comparison requires exact saved input/output hashes and every original row; it finishes only with `PASS_COMPLETE_CPP_COMPARISON`. Host loss or an uncatchable parent kill cannot execute cleanup; the exact child identity is recorded at spawn.

The Python and C++ programs independently organize exact arithmetic for the same classical BV recurrence. They are separate implementations, not independent proofs of the underlying analytic theorem. No solver, network access, private research checkout, original raw return or rank-six certificate dataset is needed. The optional C++ source admits q<=7 only; the Python arithmetic enforces the same cutoff.

The [three-row coefficient module](../three_row_coefficients/README.md) computes entire example polynomials and supplies independent count controls. Certificate verification, a complete coefficient calculation and a single count have distinct scopes. Source identities, exact margins and attribution accompany the proof; no worldwide priority or human expert acceptance is asserted.

After both complete runs, the targeted parser, corruption and real-interruption command is:

```sh
python3 -B test_controls.py --python-run /path/to/new-transport-check --cpp-run /path/to/new-cpp-check --out /path/to/new-controls
```

Supply the same optional GMP include/library flags when required. This checks the actual dependent-complement refusal, all three negative raw complements, native parser bounds, the discriminating sixth-order Bernoulli omission, and real termination with no complete result or surviving owned child.

The controls command also handles its own SIGINT, SIGTERM, SIGHUP and SIGQUIT while a subject is being launched, awaited or closed. Eight live outer-command probes cover both the Python subject and the nested C++ supervisor, checking that all observed owned process groups have exited.
