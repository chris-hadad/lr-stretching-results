# Structural positivity and complete whole-family counts

This section collects normal-correction theorems and complete positive LR
families. Their arguments and finite numerical premises have independent
AI-assisted and computational verification. The source proofs have been
edited for mathematical exposition; [ACCEPTED-SCOPES.json](ACCEPTED-SCOPES.json) gives the
precise scope of the 60 accepted mathematical claim records. Illustrative numerical controls retain their stated finite scope.

The [standalone family replay](replay/README.md) provides exact two-row proof
checks, gap-three algebra and transportation endpoint reconstruction, with
their [complete dependency map](replay/DEPENDENCIES.md). Run:

```sh
python3 -B results/structural-positivity/replay/reproduce.py --module all
python3 -B results/structural-positivity/replay/failure_cases.py
```

Two-row checks freshly expand the finite proof cases and compare complete
character formulas on a bounded roster. Gap-three and transportation modes
recompute exact algebra from explicitly historical accepted count values;
they do not freshly enumerate those underlying counts. All parameter domains,
whole-LR constructions and open complements are stated in the module guide.

A standalone replay of every normal
certificate and family count is a separate packaging task; the repository's
quick reproduction command does not perform that replay. Source proofs that
refer to numbered data files should be read with this limitation. The
[finite-box package](../finite-box/README.md) has its own complete data and
reproduction contract.

## Normal corrections and boundary classes

For n=6,...,12, let D_n=(n−1)(n−2)/2. The accepted theorem bounds the ordinary
coefficient c_(D_n−4) below by 1/3000 times the complete normalized actual
(D_n−4)-face-volume sum. It is strictly positive for a nonempty family whose
actual degree reaches that index, and zero below it. Together with the earlier
ambient top-four theorem, this protects ambient indices D_n−4 through D_n.
Degenerate hives require that explicit ambient-index qualification.

Read the [complete refined normal cycle](proofs/pro027/025-COMPLETE-REFINED-NORMAL-CYCLE.md),
the [rank-six coefficient argument](proofs/pro027/031-ALL-RANK6-SIXTH-COEFFICIENT.md),
and the [rank-seven extension](proofs/pro027/034-ALL-RANK7-ELEVENTH-COEFFICIENT.md),
followed by the later rank-extension proofs in the source index. The finite
verification checked 34 complete rosters, 1,508,387 independent occurrences, 34,761
dependent occurrences, 127,467 incidences and 5,480 referenced complete types.
Those are certificate populations, not numbers of LR triples.

At arbitrary size, the complete boundary-identification criteria prove
ordinary nonnegativity for rank at most seven with coordinate bound at most
four, and rank at most six with bound at most five after exact tensor symmetry.
See the [four-coordinate theorem](proofs/pro027/023-ALL-SIZE-FOUR-COORDINATE-LR-POSITIVITY.md)
and [five-coordinate rank-six theorem](proofs/pro027/028-ALL-RANK6-FIVE-COORDINATE-POSITIVITY.md).
Coordinate bounds need not equal actual dimension. These results do not
establish positivity for every actual quartic or quintic with a looser chart. The
[new actual-degree argument](../rank-six-coefficients/LOW-DEGREE.md) supplies the
additional Horn/strict-witness bridge: rank-six degree at most five and
rank-seven degree at most four are now nonnegative.

The normal-certificate collection distributed in this section covers ranks
six through twelve. Extensions beyond that scope require their corresponding
proof, source and verification package. The newer
[rank-six c4/c5 fields](../rank-six-coefficients/README.md) have a separate
complete standalone verifier. Negative local
weights are retained as structural information, with no claim that they alone
produce a negative entire LR coefficient.

## Whole families

- **Gap three:** the exact specified nonnegative integer quadrant and homogeneous
  three-ray cone are positive, including their initial axes. The full four
  parent bases were reconstructed from 32 determining positive values and eight
  unused checks: 40 positive count sites in total. General gap-three and fractional wings remain open.
- **Two banks:** the complete g=1, h=0 family has positive ordinary coefficients
  for every m≥2, rank m+3 and degree 2m−1. The complete capped g formula gives
  c1≥3m−1 on its stated full domain. Read the
  [all-rank sign argument](proofs/pro027/014-ALL-RANK-BANK-POSITIVITY.md)
  and [complete walls](proofs/pro027/015-COMPLETE-GAP-WALLS-AND-LINEAR-TENTS.md).
- **Unequal-weight two rows:** the suffix-sum LR lift with positive weights
  and ν=(W−2,2) is positive for n≥5. See the
  [complete formula and proof](proofs/pro027/019-UNEQUAL-WEIGHT-NONCENTRAL-POSITIVITY.md).
  The [slope-three extension](proofs/root/SLOPE-THREE-PROOF.md)
  proves positivity for ν=(W−3,3), n≥6. Its all-unit n=6 case has actual
  degree three. The count formula and the later slope-three sign proof have separate
  contributions described in the provenance account.
- **Transportation/LR:** all integer-h polynomials for rows (7+h,5,4,1)
  and columns (4+h,3,2,2,2,2,2) are positive; they stabilize after h=6.
  See the [complete family](proofs/pro027/011-COMPLETE-RANK10-CAP-RELEASE-FAMILY.md).
  On rows (7u+v,5u,4u,u), columns (4u+v,3u,2u,2u,2u,2u,2u), u≥1,v≥0,
  the [closed-sector proof](proofs/root/TRANSPORT-CONE-LINEAR-COEFFICIENT.md)
  gives c1≥5279u/360 and positive c16,c17,c18. Coefficients c2,...,c15
  at noninteger v/u are not settled by the seven endpoints.
- **Stable source–sink flows:** the complete hive/flow map holds for
  (2Mρ−sθ; Mρ; Mρ) with M≥s≥0 and includes its original lattice and
  interior-generation statement. Read the
  [whole-map proof](proofs/pro027/035-STABLE-FLOW-HIVE-MAP.md).
  The map fails as an uncut count outside the stable range. Thawinrak's
  earlier M=s=1 LR specialization and the CRY literature are prior work;
  no all-rank coefficient theorem follows from the map alone.

The complete auxiliary W0 in the gap-three analysis has negative coefficients
−1/7, −101/210, −2741/5040 and −151/2520 in degrees one through four, while
its entire P0 parent is positive. This distinction illustrates why local or
auxiliary negativity must be joined to the complete parent before a
counterexample claim.

The [source map](SOURCE-MAP.json) binds all 44 principal proof documents. Their use of classical LR models, reciprocity, Berline–Vergne
theory and Minkowski valuation results is credited in the repository
[references](../../REFERENCES.md). Alper Ferudun's rank-four/five positivity
and correction work are central antecedents. No human endorsement or worldwide
novelty claim is implied by these verification records.
