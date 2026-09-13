# The R18 anchor: positive coefficients with two right-half-plane roots

For outer lambda=(18,17,...,1), inner mu=(17,16,...,1), nu=(7,6,5), the
ordinary LR stretch equals K_((7t,6t,5t),(t^18)). It has degree 31, all 32
ordinary coefficients strictly positive, and exactly two roots in the open
right half-plane.

```sh
python3 -B reproduce.py
```

The standard-library program independently recounts the 32 determining
values and three unused holdouts, reconstructs the polynomial and verifies
exact Routh and rational Rouche certificates. Small positive-tableau and
direct-convolution controls are included. The polynomial, historical count
table and mathematical certificates are the adjacent ROOT JSON files.

[ROOT-COUNTEREXAMPLE-PROOF.md](ROOT-COUNTEREXAMPLE-PROOF.md) gives the result;
[ROOT-DEGREE-AND-METHOD.md](ROOT-DEGREE-AND-METHOD.md) records the original
bare-triple derivation. They describe the independent derivation and exact certificates used
by the standalone reproduction.

This example is the v=0 anchor of the stronger
[two-parameter cone](../hurwitz-cone/README.md). It refutes universal Hurwitz
stability while preserving ordinary coefficient positivity. It does not
establish a minimal rank or publication priority. Discovery and verification
credits are in [PROVENANCE.md](../../PROVENANCE.md).
