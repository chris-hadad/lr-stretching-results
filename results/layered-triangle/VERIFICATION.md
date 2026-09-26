# Reproducing the complete finite remainder

The proof first establishes one bivariate polynomial of total degree at most
D=3r+1 on each closed strip. The finite checks then establish its complete
ordinary coefficient signs. They recompute every determining count from the
full common-current convolution, convert every coefficient back through exact
Stirling and Pascal transforms, and compare unused whole-count holdouts.
The symbolic files supply a second stored organization; the second-strip
symbolic files are duplicate numeric adapters and are not independent evidence.

From the repository root:

```sh
python3 -B results/layered-triangle/reproduce.py --quick
python3 -B results/layered-triangle/reproduce.py --full
```

Python uses only its standard library. The complete second/third-strip replay
needs a C++17 compiler and GMP development headers/libraries. The command uses
`pkg-config` for GMP flags when available, detects an existing standard
Homebrew GMP installation on macOS, then falls back to `-lgmpxx -lgmp`;
`CXX`, `CPPFLAGS` and `LDFLAGS` may supply a local toolchain. It installs nothing.
`--scratch PATH` chooses the temporary build/decompression location. Runs are
serial with 30-minute child deadlines; interruption terminates the owned process
group and waits for its leader. All children are waited. About 90 MB of temporary uncompressed
field data are needed; no fixed execution-time claim is made across machines.

The quick command checks the original component bijections, rational threshold
identities and freshly regenerated top-strip fields. It does not close the
complete half-line theorem. The full command adds every second/third-strip
field: 136,332 slots and 342 holdouts in total. There are four malformed-carrier
controls. SHA-256 verification checks data identity, not mathematical validity.

The universal constructor, saturated lattice, total-degree statement and
analytic tail inequalities remain mathematical proof obligations addressed in
[PROOF.md](PROOF.md) and its analytic dependencies. Executing the finite replay
does not independently review those arguments or the global rank-six theorem.
