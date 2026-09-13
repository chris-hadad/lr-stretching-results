# Complete LR row recurrence and its relation to the frozen hive charts

This is a fresh derivation and implementation certificate for U01, not a claim that the classical LR rule or row-multiplicity encoding is new. The original bare boundary convention is lambda outer, |lambda|=|mu|+|nu|, all entries integral nonnegative and weakly decreasing. The code implements rank at most seven and stretched outer area at most 300, with explicit work refusal. The recurrence itself is a finite exact identity at every nonnegative stretch for arbitrary finite partitions.

## Entire tableau object

At a positive stretch t consider **all** semistandard tableaux of skew shape t lambda / t mu, ordered content t nu, whose word, read from right to left in each row and from top row to bottom row, is a lattice word. This is the full classical LR set, not a skew Kostka set and not a selected support. Every word prefix has at least as many entries k as k+1. Noncontainment gives an empty set. Scalar t=0 is one after balanced input validation; an empty positive-stretch LR family has the separate identically zero polynomial. No fit substitutes the scalar one for that zero-polynomial constant.

Write L_i=t lambda_i, M_i=t mu_i, N_k=t nu_k. Let a_(i,k) be the number of entries k in row i. Nonnegative integral row counts determine a unique weakly increasing row. They must satisfy sum_k a_(i,k)=L_i-M_i and sum_i a_(i,k)=N_k. Thus a whole tableau is specified exactly once by its ordered row-count array.

## Complete column constraints

For adjacent rows i-1 and i, semistandardness is equivalent to, for every k,

    M_i + sum_(j<=k) a_(i,j) <= M_(i-1) + sum_(j<k) a_(i-1,j).             (C)

Indeed the left side is the rightmost column occupied in the lower row by entries at most k (or its skew starting column when that prefix is empty). Any such column beyond M_(i-1) has an upper cell, since L_(i-1)>=L_i. The upper entry must be at most k-1. Upper cells with that property end at the right side of (C). Columns at or before M_(i-1) have no upper skew cell and impose no extra condition. This proves both directions, including empty rows and nonoverlapping skew portions. No assumed connectivity or omitted cut is used.

## Complete ballot constraints

Let C_k=sum_(r<i) a_(r,k) be the cumulative content before row i. Entries within this row are encountered in decreasing label order. The smallest difference between the number of k's and k+1's occurs after the new k+1 block has been read but before the k block. The necessary and sufficient row condition is therefore

    a_(i,k+1) <= C_k-C_(k+1)   for every k.                              (B)

The previous prefix is already ballot by induction. Reading labels other than k or k+1 does not change this adjacent difference; adding k later only improves it. Thus checking these block endpoints checks **every** cell-word prefix. In particular row one contains only label one, and labels greater than the row index are forced absent rather than discarded heuristically.

## State and recurrence

The state before row i is (i,C,a_(i-1,*)); the previous row is needed for (C), and all earlier rows enter (B) and the final content only through C. For each legal row array a satisfying its row sum, nonnegativity, N-C content caps, (C), and (B), add the exact count of state (i+1,C+a,a). The terminal state contributes one precisely when C=N. No multiplicity factor is attached to a because its weakly increasing row is unique. Summing all children is consequently a disjoint and exhaustive enumeration of the entire LR set. Memoization identifies only states with identical complete future conditions; it does not identify different polynomials from early scalar values.

The implementation fills labels from largest to smallest. At a partial prefix of size r it checks the corresponding column upper bound and the sum of the remaining content/ballot caps. The lower and upper bounds on the next entry are just rearrangements of these necessary inequalities, and the next recursion checks them again. At the final row the remaining content is forced and is checked against every cap, prefix and row sum. A finite branch-work limit raises a typed exception; it never returns a partial number as an exact count.

The integral row-count model has row-sum and column-sum equations with integer right sides. Their homogeneous difference lattice is saturated: if an integer multiple of an integer vector is in their kernel, then the vector itself is in the kernel. Equivalently the row/column incidence system admits the usual spanning-forest integral coordinates after redundant equations are removed. Inequalities may force additional affine equalities; this proof does not infer actual dimension or a primitive basis for each such hidden face. Only the full integral count is used here. Actual degree/parity for interiors is a separate requirement.

## Independent whole-hive determining space

The current packet supplies the entire hive/LR integer-count identity and LR stretching polynomiality. Its proof 027 derives forced rhombi from zero boundary gaps and sound positive-row-sum identities. Unit coordinate eliminations leave a complete map x=t*b+T*z, with integer b,T and a selected-original-coordinate integer inverse. Every original rhombus is retained. Hence its number of surviving coordinates is a **prior upper bound** for the whole polynomial degree, even if its actual dimension is smaller.

U01 rebuilds every selected mask closure, each unit elimination and all original inequalities for 211 frozen keys. It independently substitutes the resulting map into `hive_system` and checks equality with the derived chart rows. A further integral translation z=y+t*s leaves the full integer counts unchanged. Parallel rows may be compacted only when the discarded inequality is weaker for every t>=0, retaining constants and orientation. The supplied exact projection counter counts these complete bounded H-systems but does not itself assert polynomiality.

The optional tensor variant used to obtain a small chart preserves the entire stretch count. Write the original coefficient as dim(V_mu tensor V_nu tensor V_lambda^*)^GL(n). Permuting the three factors and simultaneously dualizing preserves invariant dimension. Subtracting each inner last part is a determinant twist, and the outer is shifted by their sum. All these shifts commute with stretching t, and all accepted variants are checked balanced integral partitions. These are the exact source proof 029 symmetries, not Ferrers conjugation. The word and every boundary are stored per record.

For each nonempty bound-five member, six values at t=0,...,5 determine the complete polynomial in degree at most five. Two reserved positive sites t=6,7 are computed later in separate calls, never used to choose the fitted degree. The row recurrence does not read hive rows or hive counts. Its values are therefore a different complete counting model; the Newton coefficient converter is shared arithmetic and is **not** advertised as independent arithmetic. U01's reconciliation additionally uses a fresh rational Vandermonde elimination to check the complete determining-space conversion independently.

## Controls and limits

The fresh row recurrence, its inner-order optimization, and a separately written literal-cell DFS agree on the complete 1,912-case balanced partition roster with outer area at most seven and all lengths at most four. Noncontainment and empty cases are included. Malformed partitions, unbalanced sizes, invalid dilation and work-limit refusals are tested. These are finite implementation controls, not a new small-rank positivity theorem or a proof that no programming defect can remain.

The independent LR commutativity optimization selects the inner ordering minimizing content length, then content area; it is recorded at every call and uses the standard complete coefficient identity, not sorting the entries of a general ordered skew content. This optimization is separate from the chosen hive tensor variant. The mandatory keys 4037909, 4037916 and the inherited hidden-quartic key 1508873 remain on the shared full-degree workload. No direct interior count or all-key runtime conclusion is supplied by this recurrence or these controls.

## Sources

Frozen packet: `methods/frontier-025-2026-09-10/sources/PROOFS/027-BOUNDARY-MASK-POSITIVE-TERMINAL.md`; source proof 029 and the complete source pins in the Phase 0 reading records; `code/ehrhart/src/slr_ehrhart/hive.py`; the exact execution-eligible mask and chart helpers. These remain adopted mathematical premises, not a fresh replay of every source certificate.

Public primary-source discovery in U01: Igor Pak and Ernesto Vallejo, *Combinatorics and geometry of Littlewood-Richardson cones*, arXiv:math/0407170 (abstract inspected, not a full-paper verification here); Olga Azenhas, R. C. King and I. Terada, *The involutive nature of the Littlewood-Richardson commutativity bijection*, arXiv:1603.05037 (abstract inspected), explicitly identifies full LR tableau and hive counting models. The recurrence (C),(B) and completeness proof above are derived here, not quoted from these abstracts.
