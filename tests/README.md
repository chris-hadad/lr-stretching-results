# Publication verifier failure-path checks

From the complete repository root, using Python 3.11 or later on macOS/Linux:

```sh
python3 -B tests/test_publication_entrypoints.py -q
python3 -B tests/test_publication_runtime.py -q
python3 -B tests/test_publication_signal_paths.py -q
python3 -B tooling/whole_rank_six/lower/tests/test_adapter.py -q
```

These small tests use synthetic data and bounded real child processes. They
check optimized-Python refusals, negative local-value rejection, corruption of
H8 continuation records, missing or changed source bindings, exact child-group
cleanup on timeout and interruption, signals during launch/cleanup/restoration,
normal child signal masks and handler restoration. Scratch uses the caller's
temporary directory; set `TMPDIR` to another existing writable directory if needed.
No proof dataset download, network request, compiler or package installation is
performed by these tests.

These are software failure controls. They do not establish the mathematical
coefficient inequalities; use the [scientific verification routes](../REPRODUCING.md)
for that. Earlier successful scientific runs retain their recorded source
versions, while current interface repairs have their own focused tests.

[Tool guide](../tooling/README.md) · [Rank-six verification](../results/rank-six-positivity/VERIFYING.md)
