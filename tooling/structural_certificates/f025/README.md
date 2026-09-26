# Complete boundary forcing-table check

Read [FORCING.md](FORCING.md) for the proof, exact command, row convention,
controls and source dependencies. This checks every one of 32,768 rank-six
and 262,144 rank-seven boundary masks, using only Python's standard library.
The observed complete public-layout replay took 14.778 seconds.

The result is a sound dimension upper bound derived from original-row
identities. It is not a claim of actual dimension or of universal tight-row
closure. The rank-six complete closure theorem has its own
[103-identity checker](../../whole_rank_six/closure/README.md).

The two input tables are included in the [structural data archive](../README.md).
This full table recheck is a required finite premise of that module's selected
boundary-mask conclusions. It is separate from the normal/mask checker.

[Structural module](../README.md) · [All tools](../../README.md) ·
[Result catalog](../../../RESULTS.md)
