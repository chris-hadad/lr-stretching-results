# A60 grouped-sector discriminator and exact limit

Curated mathematical proof from **A60**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

Root work on the complete A59 originals, independent of both active provider
working proofs. The accepted A59 cumulative-coordinate map and full sector
polynomials are inputs; all sectors, cap spans, aggregate and absorber flags
remain present. This record gives a bounded coarsening result, not a theorem
for all two-cap originals.

For the complete a=5,d=3,k1=k2=1,p=2,delta=1 rank-seven control,
there are 134 admitted beta states. Group them by all beta coordinates except
some specified forgotten indices; the group polynomial is the EXACT sum of
all sectors sharing the retained key. No state is discarded or duplicated.
Exhausting all zero-, one- and two-coordinate coarsenings shows that no
single forgotten coordinate suffices for coefficientwise nonnegative groups.
Exactly three two-coordinate choices suffice: {3,4}, {3,5}, {4,5}, giving
72,83,78 groups respectively. In the balanced delta=0 variant, forgetting
coordinate 5 suffices and gives 83 groups. The other five A59 nonpoint
original controls already have nonnegative individual bands.

The transparent candidate rule forgets coordinates 4,...,a. These are the
cumulative coordinates through the uncapped U increments, including the
left endpoint of the second small-cap span. The group still sums every
literal admissible sector and retains the actual cap/aggregate/absorber
constraints in each. It does NOT replace that endpoint by a relaxed bound.
On the same two-unit-cap d=3,p=2 family, complete extension checks give:

| a | delta | Original rank | Degree | Bands | Negative bands | Groups | Negative groups |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 1 | 7 | 9 | 134 | 2 | 78 | 0 |
| 5 | 0 | 7 | 8 | 103 | 1 | 56 | 0 |
| 6 | 1 | 8 | 11 | 246 | 3 | 118 | 0 |
| 6 | 0 | 8 | 10 | 199 | 2 | 88 | 0 |
| 7 | 1 | 9 | 13 | 403 | 4 | 168 | 0 |
| 7 | 0 | 9 | 12 | 337 | 3 | 129 | 0 |

The a=5 beta/group counts are read back from the exact A59 decomposition;
its 77 bare-original/shifted-partner grades retain their prior evidence.
The a=6,7 checks independently compare the full group sum against the direct
complete residual-pair domain at every determining grade and two unused
holdouts. Each sector polynomial is also checked through two unused grades.
Those new computations do not call a new bare-triple engine; their original
interpretation uses the accepted exact A58/A59 count/lattice proof. Their
whole polynomials are positive, with the stated actual-degree rule. The
finite result does not cover arbitrary a,d,p,delta,k1,k2, or overlap gains.

`grouped-bands-v1.json` contains every minimal coarsening and failed named
single-coordinate candidate. `group-a6-v1.json` and `group-a7-v1.json`
contain all whole vectors, original triples, determining/unused counts and
negative-group rosters (empty). The checker sources and contained runtime
receipts are retained. Exact regrouping is an identity; positivity is only
proved for these finite parameter choices. A uniform grouped coefficient
certificate or a paid terminating overlap generator remains unpaid.

KEEP this grouping as the strongest concrete absorber competitor. Its first
proof test is to integrate the entire free-U block with both span endpoints
and the aggregate/absorber flags retained, then show coefficient positivity
uniformly, including zero caps, collapsed flags and initial parents. A
favorable isolated poset, one-coordinate relaxation or larger positive table
does not solve that obligation. The deficit-three reserve is the uniform
whole-original result earned in A60; the grouping is a separately scoped lead.
