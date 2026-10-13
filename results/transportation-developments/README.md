# Complete transportation compensation and selected higher coefficients

These results concern complete nonnegative tables and their entire ordinary
LR lifts. They preserve all physical zero margins, labels, original offsets,
supported intersections and actual degrees. They supplement the earlier
[all-margin 4-by-5 theorem](../transport-four-by-five/README.md).
Whole rank seven and unrestricted KTT remain open.

## The full linear coefficient at every table size

For positive row margins r of length p>=2 and column margins c of length N>=2,
with common total M, define


```text
w_k(I)=(|I|-1)!(k-|I|-1)!/[2(k-1)!],
D(r,c)=sum_(I,J proper nonempty) w_p(I)w_N(J)
              min(r(I),M-r(I),c(J),M-c(J)).
```

The ENTIRE linear coefficient is c1=D>0, and


```text
c1>=H_(p-1)H_(N-1) epsilon,
```

where epsilon is the smallest positive margin. The actual degree is
(p-1)(N-1). Delete forced-zero margins before applying this formula; at most
one active row or column gives the point polynomial one. The real cut extension
is homogeneous, concave and superadditive. Those properties concern the
transportation extension, not arbitrary LR c1.

This is the accepted Pro029/A006 all-row theorem of 13 September, not new A64
mathematics. The old [double-cut page](../families-and-obstructions/proofs/transport-double-cuts.md)
proved the one-/two-class core. The complete later proof shows that EVERY
higher-class first jet vanishes at its original assignment offset, with all
empty positions and closed walls retained. Its mathematical dependency chain is

1. [Complete two-class core](../families-and-obstructions/proofs/transport-double-cuts.md).
2. [Exact Lagrange primitive](proofs/TRANSPORT-PRIMITIVE.md).
3. [All-rank wall induction](proofs/TRANSPORT-WALL-INDUCTION.md), including the
   empty-singleton residue and the all-reversed crossing orientation.
4. [Whole transportation and LR bridge](proofs/TRANSPORT-C1.md).

The wall/residue antecedents and their operative hypotheses are linked in the
[reference notes](../../REFERENCE-NOTES.md#transportation-wall-and-residue-inputs).
No arbitrary higher-coefficient sign follows from this first-jet theorem.

## C22 is a full table, with every budget and cap retained

For original isolated caps k_i>=0, budgets P,Q>=0, K=sum k_i and H=P+Q,
the complete C22 count is exactly the full table with


```text
rows=(k_1,...,k_a,H,H), columns=(P,Q,K+H).
```

The cap rows are (u_i,v_i,k_i t-u_i-v_i). Two complete slack rows resolve
(Pt-sum u_i+1)(Qt-sum v_i+1); their third entries are automatically
nonnegative. [The inverse and saturated lattice proof](proofs/C22-FULL-TABLE.md)
retains every table entry, wall and physical zero row.

If m caps are positive, H>0 gives degree 2m+2 with two positive budgets and
m+1 with exactly one positive budget. H=0 is a point. The all-size theorem pays
c1 for every cap/budget pattern. All coefficients are strict through actual
degree when m<=3 at arbitrary budgets (the 4-by-5 table theorem), or when only
one budget is positive at arbitrary m (the two-row-inner theorem).
A C22 negative therefore requires at least four positive caps, both budgets
positive and coefficient index at least two. These are C22 restrictions.

The [cap proof collection](PROOF-INDEX.md#cap-endpoints-and-operations) retains
A58-A64's additional endpoint, high-budget, balancing, growth and crossing
results. The deficit, cap floors and finite crossing ranges remain distinct.
A natural dimension recurrence is exactly refuted; no arbitrary-cap recurrence
is claimed. The complete finite crossing/absorber certificate closures and their trusted checkers are
[included](DEPENDENCIES.md).

## Selected-width overlap families at arbitrary column count

Take balanced positive rows (A,B,R) with 0<A<=B. Every positive labeled column
must be at least A. Draw every edge e_i+e_j<A+B, retaining equality as
nonoverlap. With N positive columns and R>0, degree is 2(N-1).

- The entire triangle-free family is strict through actual degree, for arbitrary
  N, margins, heights and star height sum. The complete lower reserve is
  K_(N-1)(At), with


```text
  K_n(x)=a_n(x)^2-(n+1)d_(2n)(x)
         >=a_(2n-1)(x)[1+(n-1)x/(2n)].
```

- Exactly one triangle plus isolated vertices is strict through actual degree
  for N>=4. The full triple intersection, all three pairs and each isolated
  singleton remain in the proof. Its reserve is the same K_(N-1).

[The full triangle-free proof](proofs/A78-HIGH-STAR-ADOPTION-v1.md) includes
the entire high-star payment and uses the exported A73-A77 chain.
[The full one-triangle proof](proofs/A79-UNIFORM-TRIANGLE-v1.md) has the complete
Pro053 U03/U05/U11/U12 dependencies and both fixed sign appendices in
[the proof index](PROOF-INDEX.md#triangle-dependencies). Earlier one-pair,
two-pair, height-budget and bounded-column theorems are supporting components.
Empty graphs, zero rows, N<=2, points and degree drops retain the exact
primitive-base classifications; a generic degree is never assigned to them.
Extra edges/cliques and overlapping columns below A remain open.

## Restricted c2 and operation theorems

The three-row assignment kernel keeps every labeled one-, two- and three-class
term at its original offsets. Full polarized wall jumps are paid, but universal
smooth concavity is refuted. This does not prove arbitrary-margin c2.

| Accepted development | Exact scope and complete proof |
| --- | --- |
| Balanced dominant splitting | [A70](proofs/A70-BALANCED-SPLITTING.md), with the original balanced rows and dominance hypotheses |
| Unequal dominant rows | [A71](proofs/A71-DOMINANT-SPLITTING.md), with its complete compensated pair correction |
| One constrained row | [A72](proofs/A72-CONSTRAINED-PARENT-v2.md), arbitrary depth, at least two rows at least the old column total D |
| Central-band concavity | [A73](proofs/A73-ALL-MARGIN.md), including two/three constrained rows, with the displayed central cap region |
| Dominant column | [A77](proofs/A77-DOMINANT-COLUMN-ADOPTION-v1.md), one column at least the largest row, including its below-half range |
| Stable whole quotient | [A70](proofs/A70-STABILIZED-QUOTIENT.md), arbitrary-rank short-inner-three quotient with explicit safe height; no sign theorem for its starting or prestable boundary |
| Fixed rank-five operation | [A70](proofs/A70-PRO049-U12-ADOPTION.md), the entire two-parameter operation; its endpoints were already protected by rank five |

The [structural proof index](PROOF-INDEX.md#quadratic-structure-and-obstructions)
contains A65-A69's full assignment, wall, transverse, coarsening, split and
curvature arguments. Negative components and signed gains retain their complete
positive endpoints and same-coefficient payments.

## Reproduction and provenance

```sh
python3 -B verification/check_recent_sources.py --module transportation-developments
python3 -B results/transportation-developments/code/verify_triangle.py --output /path/to/new-triangle-check
```

The triangle checker uses exact standard-library polynomial arithmetic and a
restricted mathematical-data parser. It authenticates only local curated proof
bytes and runs the complete fixed-certificate and initial-slope audit; it neither
runs provider code nor calls an LR engine. The analytic proofs, not bounded
index arrays, supply the arbitrary-index statements. Other complete computational
premises have the precise scopes in [DEPENDENCIES.md](DEPENDENCIES.md).
[Verification status](VERIFICATION.json) distinguishes observed export replay,
mathematical proof and inherited evidence. Pro029/Frontier024, Pro048-Pro053,
Codex derivations and classical wall/character methods retain distinct credit.

## Full finite certificate routes

```sh
python3 -B results/transportation-developments/code/verify_high_star.py --output /path/to/new-star
python3 -B results/transportation-developments/code/verify_crossing.py --out /path/to/new-crossing.json
python3 -B results/transportation-developments/code/reproduce_two_cap.py --out /path/to/new-two-cap.json
```

The crossing command reconstructs every A63 chamber/zero base and the complete
A64 a=9 one-small-cap extension. The two-cap command checks every slot in all
40 chamber identities at a=4..8. Their analytic high-excess/domain arguments
remain in the full proofs; neither command extrapolates arbitrary a from a panel.
