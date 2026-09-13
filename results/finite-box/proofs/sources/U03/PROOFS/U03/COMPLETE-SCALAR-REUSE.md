# Exact cross-key scalar reuse and its measured limits

## Entire fixed-grade integer systems

The U02 bounded H-system counter first propagates necessary integer coordinate bounds, substitutes coordinates fixed by those bounds, and translates every remaining integer interval to [0,w_i]. Each remaining inequality c+sum(a_i*x_i)>=0 is divided by gcd(a_i), replacing the constant by floor(c/g); this is an exact integer-point predicate. Among parallel primitive normals it retains the strongest constant, and it discards a row only when its exact minimum over the entire retained integer box is nonnegative. The cache key is the complete ordered width list and complete sorted resulting inequality list, with dimension. Coefficient types, signs and constants are retained. Complete remaining constraint components can factor only when no retained row crosses between components.

Two identical keys define identical finite integer sets in the translated coordinates, hence have the same scalar count. This remains valid across different original boundaries, different physical grades and closed/interior encodings: all changes affect the complete integer system. Integer-floor normalization is not asserted to preserve the real polytope, its lattice facets, or an all-stretch polynomial. The cache therefore cannot establish a parent-polynomial identity or replace the separate complete chart, lattice, degree and reciprocity premises.

Only fully evaluated subproblem answers enter the cache. A failed outer count may leave completed subproblem values, but no partial outer total is returned as a count. Work, state, coefficient-range, time and memory refusals remain explicit. One synchronous request is processed at a time; retained idle engines do not provide extra active scientific threads.

## Exact remaining-row completion descriptors

For the complete LR row recurrence, fix a physical grade and suppose rows before i have been filled. Let C_k be the number of letters k already used, prev_k the previous row counts, and R_k=N_k-C_k the remaining content. The full remaining row problem is determined by:

- n, the active label count, and the number of remaining rows;
- every R_k and every already-used difference C_(k-1)-C_k;
- every remaining row length and every nonnegative/ballot threshold;
- for the first remaining row, all bounds M_(i-1)-M_i+sum_(j<k)prev_j-column_threshold_(i,k), or the explicit top-row flag;
- for later rows, every inner-row gap and every column threshold.

To see completeness, introduce variables b_(r,k) for **all** remaining cells. Row and content equations have exactly the retained right-hand sides. Nonnegative constraints use the retained thresholds. A ballot constraint is

    [C_(k-1)-C_k] + sum_(i<=s<r)b_(s,k-1) - sum_(i<=s<=r)b_(s,k)
         >= ballot_threshold_(r,k).

The first remaining column constraints are precisely the retained prefix upper bounds. Later column constraints are

    sum_(j<=k)b_(r,j) - sum_(j<k)b_(r-1,j)
         <= M_(r-1)-M_r-column_threshold_(r,k).

No old entry or boundary quantity outside the descriptor occurs in this entire system. Therefore equal descriptors give a literal bijection, the identity on the remaining row arrays. Zero-content labels and all thresholds are retained. This is a complete conditional count identity, not multiplication of marginal profiles or an inference from equal early LR values.

The implemented descriptor deliberately retains some redundant data. It is sufficient, not claimed minimal. The local within-request memo remains separate. A proposed future normalization could remove only **proved** content-budget redundancies from this descriptor; that further compression was not implemented in U03.

## Collision and scope challenges

The first shared caches use ordered maps with full vector keys. A second version changes only the lookup container to a hash table. Full vector equality still resolves every collision. A deliberately constant hash, forcing all keys to collide, is separately compiled and tested against all 312 H-system and 1,920 tableau control requests, including the explicit range refusal. This test would not protect a digest-only cache; the implementation does not use one.

Literal controls also challenge changed offsets, changed widths, equal integer floor predicates next to unequal ones, translated/reordered rows, redundant cuts, empty and hidden-dimensional systems, and a rational non-period-one interval. The common 4,131-key workload supplies actual closed and genuine-interior comparisons in both counting models. Every complete four-count record is preserved before comparison or a coefficient-sign observation.

## Result-driven disposition

The original ordered warm caches were slower than their cold counterparts on this workload despite many more hits. That negative performance observation is saved before the hash repair. The hash version removes much of the ordered-lookup penalty in the hive model, but end-to-end worker time is not materially improved, and the warm row cache remains slower. Neither method has earned a whole-population speed claim. Exact complete-key reuse is mathematically sound; its present implementation is not the main reason to reduce millions of obligations.

The stronger U03 repair instead proves a complete **all-stretch** gap/tensor rewrite and joins literal final triples, retaining scales. That is a different level of reuse. It also clears six previously refused tableau holdouts at their unchanged physical grades, using smaller complete LR boundaries without raising the engine's state limit. All original refusals and prices are retained. See INACTIVE-GAP-DIRECT-LR.md and the exact per-job/data records.
