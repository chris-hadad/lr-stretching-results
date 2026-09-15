# Whole positivity for three-letter LR families through rank six

A computer-assisted finite certificate in the original integer lattice, with
complete independent numerical reconstruction. Verification and review limits
are stated in README.md.

## Theorem and exact domain

Let lambda, mu and nu be nonnegative integral partitions with
|lambda|=|mu|+|nu|, lengths at most six, and length(nu)<=3. Lambda is outer.
For every such triple, the ENTIRE ordinary stretched LR polynomial

    P(t)=c^(t lambda)_(t mu,t nu)

has nonnegative rational coefficients. If the positive-stretch family is
feasible, every coefficient through its actual degree is strictly positive;
the constant is one. Infeasible positive-stretch families have the zero
polynomial by convention. A point has polynomial one. No area bound,
genericity, strict-margin or integral-vertex assumption is imposed.

Inner symmetry also permits length(mu)<=3. Applying a separately proved
stretch-preserving tensor symmetry or determinant normalization transfers
this conclusion to its exact image; no Ferrers-conjugation stretching
symmetry is asserted. Whole ordinary rank six remains open outside the
admitted family, and no conclusion about general short-inner-three at ranks
above six follows from this finite certificate.

Let H be the full seven-coordinate row-letter polytope in MODEL.md.
Write c_k=[t^k]P(t). In its original saturated lattice, the stronger statement is

    c_k >= 1/100000000 * sum_(actual k-faces F of H) vol_Z(F),
                                                  1<=k<=7.   (1)

Normalized volume means volume divided by the covolume of the saturated
direction lattice, with no factorial. When k exceeds actual dimension both
sides vanish. When there is a k-face, its normalized volume is positive.
The model has dimension at most seven, with an explicit strict witness of
dimension seven. This is a whole family at the first open ordinary rank,
not positivity for every rank-six LR triple.

## Full model and source premises

MODEL.md proves both directions of the complete row-letter tableau
bijection, all column and lattice-word constraints, every original offset,
and the integral inverse in coordinates

    (a_22,a_32,a_42,a_52,a_33,a_43,a_53).

It retains 42 literal inequalities. Seven have zero normal; three pairs
have the same oriented normal but possibly different offsets. Thus the
normal computation uses 32 distinct oriented directions while the original
polytope keeps every offset. The map identifies the entire affine integer
solution lattice with Z^7, not a sublattice selected from it. Degenerate
faces use the intersection with their rational direction space.

The LR rule, its row-triangle encoding, saturation and stretching
polynomiality are classical premises. The explicit model is a specialization
of that structure. Neither an integer coordinate map nor LR polynomiality
asserts that all vertices are integral. The argument below handles rational
vertices by denominator clearing, retaining the original stretch.

## Complete local lattice and metric data

For an independent normal row set I, let N_I be its original row matrix,
L_I=N_I Z^7 its full image lattice, d_I=[Z^I:L_I] its index and
G_I=N_I N_I^T. The induced normal-coordinate metric is G_I^(-1).
Two rows are grouped only when a specified generator permutation identifies
both their complete image lattices and Gram metrics. Index alone is not a
lattice, and Gram alone is insufficient at higher index.

The independent checker enumerates EVERY original subset and computes its
index by gcds of maximal minors. It checks each grouped lattice by all seven
column inclusions and equality of independently computed indices. Explicit
admissible permutations are saved for every independent assignment. The
primary column-reduction organization is different. No original dependent
subset or higher-index case is omitted.

| q | All original subsets | Independent | Dependent | Complete lattice/metric types |
| --- | --- | --- | --- | --- |
| 1 | 32 | 32 | 0 | 9 |
| 2 | 496 | 486 | 10 | 129 |
| 3 | 4960 | 4622 | 338 | 1464 |
| 4 | 35960 | 30495 | 5465 | 12288 |
| 5 | 201376 | 144914 | 56462 | 74306 |
| 6 | 906192 | 484508 | 421684 | 307461 |

There are 1,149,016 original subsets, 665,057 independent subsets,
483,959 dependent subsets and 395,657 safe types. Image indices range from
one through eight. These are auxiliary normal populations, not LR triples
and not additive campaign coverage.

For each subset T of I, put r_(T,i)=d_T/d_(T without i). The complete finite
numerator consists of p in L_T with 0<=p_i<r_(T,i), with cardinality
product_i r_(T,i)/d_T. For generic compatible covectors c_T=G_T^(-1)w_T,

    S_T(s)=sum_p exp(s*c_T.p)
                    / product_i(1-exp(s*r_(T,i)*c_(T,i))).

The full image-lattice Euler-Maclaurin recurrence is

    mu_empty=1,
    mu_T(s)=S_T(s)-sum_(nonempty U subset T)
       (-1)^|U| d_(T without U)/d_T
       * mu_(T without U)(s)/(s^|U| product_(i in U)c_(T,i)).   (2)

Its constant term for full I is alpha_I. This is the classical BV local
formula in these exact image coordinates. Every proper-face term and
numerator point remains. Normalized Taylor truncation through q<=6 uses

    1/(1-exp(z))=-1/z+1/2-z/12+z^3/720-z^5/30240+O(z^7).

The degree-six Bernoulli contribution is required. The independent program
uses reverse-subset adjoint elimination and integer-scaled Todd polynomials;
its source was frozen before it read any primary value or evaluator source.
All 395,657 constants agree exactly and all poles cancel. Pole cancellation
alone would not establish a correct constant, so a deliberate omitted-term
control is separately checked.

The original core refused an index-seven numerator exceeding its 4096-point
bound. That attempt is preserved. The new model-only core admits D=7,q<=6,
entries in [-2,2], index<=8 and at most 32768 numerator points per subset:
every axis length divides its image index I, giving at most I^(q-1)<=8^5.
It retains the complete actual 16807-point index-seven case. No omitted
point is treated as zero or as a completed local value.

## Four complete rational fields

The full primitive quotient divisor follows from the lattice exact sequence: If J=I without n,
then M_J=ker(N_J) intersect Z^7 is saturated, and the image of n on M_J is
delta Z with

    delta=d_I/d_J.

Projection of L_I onto the J coordinates is surjective onto L_J and its
kernel in the last coordinate is delta Z. The finite cokernel exact sequence
therefore has orders d_I=d_J*delta. This proves the divisor in the original
integer lattice, including every higher-index case.

At every independent support J choose an arbitrary rational g_J in ker N_J.
This is the entire field space. A nonunit integer kernel basis is permitted
as a real/rational basis; it is not mislabeled a saturated integer basis.
For every original independent I set

    beta_I=alpha_I+sum_(n in I)
                  g_(I without n).n /(d_I/d_(I without n)).   (3)

Four supplied rational fields cover q=3,4,5,6. Unlisted supports are the
zero field. The verifier checks every g_J annihilation equation, every
original primitive divisor and every beta_I, with all positive and negative
raw complements included. The full discovery matrices impose no symmetry
or restricted support space. Floating solvers only propose fields; exact
rational inequalities establish (3).

| q | Protected coefficient | Raw negative original rows | Active ambient supports | Verified epsilon |
| --- | --- | --- | --- | --- |
| 3 | c4 | 13 | 10 | 1/100000000 |
| 4 | c3 | 544 | 611 | 1/100000000 |
| 5 | c2 | 8593 | 14360 | 1/100000000 |
| 6 | c1 | 62669 | 97273 | 1/100000000 |

Every exact corrected minimum exceeds this common epsilon. Orders one and
two have raw minima 1/2 and 1/20; no correction is needed. The q3 field
makes this seven-coordinate proof self-contained. It does not reopen or
replace the earlier, broader universal rank-six c4/c5 theorem.

The two large direct LP queries timed out, and the active-row IPM attempt
was stopped by its hard child deadline. None proved infeasibility. Full-row
sparse projection and a complete affected-row repair supplied the successful
q5/q6 proposals. Those optimization attempts remain part of the source research record; no
solver is needed to verify the supplied rational fields.

## From the full finite certificate to every polynomial

First take an integral nonempty polytope P given by the complete original
normals in Z^7, with arbitrary original offsets. Loosen ALL inequalities
by sufficiently small generic positive amounts. This produces a bounded,
full-dimensional simple polytope whose normal fan refines the original fan
using only original normal directions. Every surviving vertex basis limits
to an original face. Only the fan refinement is used; no coefficient of the
perturbed polytope is transferred by continuity.

Fix k>=1, q=7-k. Give each q-cone of the refinement the nonnegative
normalized volume of the actual k-face whose coarse normal cone contains
its relative interior, or zero when no such face exists. These weights
w_I form the complete refined normal cycle. At each (q-1)-support their
sum of primitive quotient conormals is zero: on an actual (k+1)-face this
is normalized lattice facet balance; across an internal subdivision the
two primitive directions cancel; in larger coarse cones the weights vanish.
This includes nonsimple walls and the lineality of degenerate normal cones.

The BV dual-solid valuation adds its local constants over the full-dimensional
pieces of a normal subdivision. The local coefficient formula and the
entire primitive balance therefore give

    c_k(P)=sum_I w_I alpha_I=sum_I w_I beta_I.                 (4)

Each actual k-face contributes at least one cell. Using (3), or the raw
orders one/two, proves (1) for k=1,...,6. For k=7 the coefficient is
ordinary normalized volume, so (1) is immediate. The constant is one.

For a rational model polytope H, choose a positive integer L clearing all
vertex denominators. The integral polytope LH has the same normal fan and
original direction lattices. LR polynomiality gives E_(LH)(t)=P(Lt), and
normalized k-face volumes scale by L^k. Divide the integral inequality by
L^k to obtain (1) for H. No unsupported continuity or integral-vertex
assumption enters. A rational feasible H has an integral point at some
positive dilation; LR saturation supplies feasibility at dilation one.

This proves all coefficients through actual degree for the entire stated
family, including every zero-content, empty-row and parameter-wall case.

## Whole stabilized quotient consequence

The admitted boundary family is closed under addition. For feasible integral
base b and direction a within it, let the entire direction polytope have
actual dimension r>=1. Translate it by an integer point, use its direction
span W and the saturated quotient Z^7/(Z^7 intersect W). After a finite
integer stabilization S, the complete fixed-system basis-slack argument gives

    H_(b+(S+u)a)=H_(b+Sa)+u H_a, u>=0.

For the ENTIRE stabilized quotient K and normalized r-volume V of H_a,
the full fiber limit and denominator-cleared multivariate counting identity give

    [u^r] P_(b+(S+u)a)(t)=V*t^r*E_K(t).                       (5)

Initially empty integer fibers are retained: every quotient lattice class
has an integer lift, and the growing full r-dimensional direction controls
its leading count. No proper face or early projection is substituted.

For each actual j-face G of K, the lifted parent face has dimension r+j
and its normalized volume divided by u^r tends to V*vol_Z(G). This follows
from the exact sequence of saturated fiber/quotient lattices. Apply (1) to
all these parent faces, divide by u^r, and use (5). Every coefficient of
E_K through its actual degree is positive, with the same epsilon bound on
its complete actual face-volume sum. A point quotient has polynomial one.
Its degree is at most 7-r. The initial and intermediate parents are also
positive because the whole-family theorem already covers them.

The corresponding stabilized whole-hive quotient has the same count
polynomial: full parent and direction polynomials agree, hence so do the
leading coefficient identity (5) and V. This transfers positivity, not an
unproved isomorphism or a face-volume bound between different quotient
geometries. No ordinary LR rank is assigned to a quotient. Bases outside
the admitted family remain outside this consequence.

## Verification, credit and remaining scope

The complete finite data, independent reconstruction, full rational fields,
literal-tableau/lrcalc/whole-hive controls and exact failure records accompany
this theorem. The review scope and result are reported with the public verification record. The finite populations are not a sampled parameter proof.

The foundations are the classical LR rule and LR triangles, Knutson-Tao
saturation, Derksen-Weyman/Rassart polynomiality, Berline-Vergne local
Euler-Maclaurin and dual-solid valuations, and the complete normal-cycle
correction method used in the prior campaign. Alper Ferudun's rank-five
theorem and correction approach and Pro027/Pro028's prior normal work retain
credit. The new work is the complete three-letter chart analysis, its four
full rational fields and exact whole-family consequences, with the explicit
interior and compensation developments in their companion notes.

Whole ordinary ranks above five, unrestricted KTT, general higher-rank
short-inner-three and an entire negative outside the completed box remain
open. Computer-assisted checking and model review are not external human
acceptance or worldwide priority. No ordinary-negative LR polynomial was
observed, and no new finite-box coverage is asserted.
