# How to verify the rank-six result

The proof has a short geometric core and a larger exact computation. Start with
the [paper](../../papers/rank-six/README.md) or [complete proof account](PROOF.md).
The support lemma shows why excluded normal supports have zero actual face
weight; the complete balanced identity keeps every incidence. The
[legal-realization converse and closure calculus](GEOMETRY.md) explain exactly
what the retained physical branches mean.

## Choose a route

| Your question | What to read or run | Scope |
| --- | --- | --- |
| Is the new geometric mechanism sound? | Paper Sections 3–4; [closure checker and witness API](../../tooling/whole_rank_six/closure/README.md) | Complete closure for all `2^45` row sets in about five seconds; inspect the separate analytic support/converse arguments |
| Can I independently reconstruct the cone? | `python3 -B tooling/whole_rank_six/geometry.py --out /path/to/new-run` | Exact 45-row/166-ray reconstruction and original-boundary examples, about 3.5 seconds |
| Can I try a complete coefficient certificate quickly? | `python3 -B tooling/whole_rank_six/verify.py small --out /path/to/new-run` | Every finite premise for c6–c9, about 96 seconds; c10 is volume |
| Do the supplied fields satisfy every required inequality? | [Complete field commands](../../tooling/whole_rank_six/README.md#check-all-coefficient-fields) | All c1–c5 domains, original lattices, primitive actions and exact inequalities; includes c4/c5 scalar regeneration |
| Can I derive every supplied scalar too? | [Complete lower chain](../../tooling/whole_rank_six/lower/README.md), then [q9 scalar check](../../tooling/whole_rank_six/scalars/README.md) | Every analytic scalar and proper lower dependency; the expensive route |
| What was actually executed and reviewed? | [Verification record](../../tooling/whole_rank_six/VERIFICATION.json), [contribution map](CONTRIBUTIONS.md) | Complete scientific replay, exact wrapper-test scope and independent AI review; human peer review and formalization remain distinct |

All example output paths must be fresh and have existing parents. Run shell
commands from the repository root unless a module explicitly says otherwise.
The [tool guide](../../tooling/whole_rank_six/README.md) lists prerequisites,
data restoration, exact phase order, storage and measured costs. The closure
checker needs only Python; the larger coefficient checks need C++17 and GMP.

## What has been checked

The linear component covers all 27,230,728 nine-normal orbit rows and all
46,327,714 physical-row branches. Its retained domain is 13,325,662 rows,
representing 79,940,357 original supports. The field has 20,960,436 integer
coordinates and denominator 60,000,000,000. Its exact minimum is

$$\frac{40142888690844119591010700379369}
{40149066134252712057708583296000000000}
>\frac1{2\,000\,000}.$$

The full original action was reconstructed independently of the stored sparse
operator. Complete q7→q8→q9 extension joins establish coverage rather than
relying on row counts alone. All 455 q9 scalar ranges were independently
recomputed, including every original image lattice and exceptional character.

The lower chain separately checks all 1,988,979 q1–q7 types, their 4,706,329
analytic jet slots and 19,271,753 additional H8 slots; it regenerates all
6,958,562 q8 scalar types at two covectors. Every one of the 8,947,541 entries
in the q9 lower cache is matched to those exact sources. Complete c2/c3 fields,
the standalone c4/c5 reconstruction and the compact c6–c9 certificates finish
the finite assembly. The constant term, actual degree, padding, empty/point
cases and finite-to-universal implication are proved in the manuscript.

## Data and measured cost

The main data package has nine archives totaling 4,985,772,426 downloaded bytes
and 14,054,651,154 restored bytes. It contains every one of the 1,842 required
input files, identified by [the asset manifest](../../tooling/whole_rank_six/DATA-ASSETS.json).
No private research checkout is required. The small geometry and c6–c9 checks
use only the Git source snapshot.

The fresh public c1 geometry/classifier/action/coverage run took 21.49 minutes;
the complete fresh c4/c5 run took 23.06 minutes under concurrent load. The final
portable c3 core and c2 field phases took about 58 and 111 seconds. Full q9
scalar checking took 3.49 wall hours with up to six children and 20.66 aggregate
child-hours. Complete c3/H8/q8 analytic stages add about 5.76 aggregate
child-hours. These sums use elapsed child timers, not measured CPU time, and
do not predict performance on another host.

The public adapters make these routes portable. Complete long mathematical
engines were run on isolated source/data copies. The final lower convenience
wrapper also ran complete c3 core, complete c2 field, small H8, six scientific
controls and a diagnostic q8 shard. Its entire long H8/q8 orchestration was not
repeated after the portability changes. The final scalar parallel wrapper
completed actual ranges and passed cancellation/partial-result controls;
the complete 455-range scientific run used the separately recorded full driver.
The verification record preserves those distinctions and source equivalence.

## What the trust boundaries mean

File hashes establish identity. Supplied-scalar field checks establish exact
inequalities and complete geometry conditional on those scalars. Full scalar
regeneration establishes the scalar predicates from the stated analytic
recurrences. The manuscript connects those finite predicates to the LR theorem.

Missing rows or tails, changed values, malformed lattice data, zero fields,
invalid propositional additions, and altered identities have explicit refusal
controls. Failed or interrupted runs cannot yield complete coverage. These
tests seek plausible failure modes; their success is not a guarantee against
every possible implementation error.

The theorem has received independent Astra mathematical review, including the
integrated geometric strengthening. It has not received external human peer
review or a whole-theorem Lean/Coq/HOL formalization. The
[formalization assessment](FORMALIZATION.md) describes a concrete finite Lean
target and the remaining mathematical bridge. To report an issue, give the
source version, exact claim or row, command and observed output.

[Main result](README.md) · [Algorithms](ALGORITHMS.md) · [All results](../../RESULTS.md)
