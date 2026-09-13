# Direct ordinary-LR gap reduction and a terminating whole-count rewrite

## Inherited mechanism and new bridge

The packet's `methods/astra-wildcard-003-2026-09-08/A03/FIXED-AREA.md` proves a complete real/integer row-count normal form for semistandard skew tableaux by deleting empty rows and clipping inactive horizontal gaps. Its source constructor then uses a skew-content buffer for an ordinary LR realization. The present use is more direct: the same row-word-preserving map restricts to the **entire original LR lattice-word fiber**. Thus the new target is an ordinary LR triple without adding a buffer or increasing ordinary rank. This is a new concrete application/implementation in this mission, not a claim to have invented the generic inactive-gap mechanism or classical LR rule.

Write lambda outer, mu inner, nu content; all are balanced nonnegative integral partitions. A tableau is read right-to-left in each row and top-to-bottom across rows. LR tableaux are precisely semistandard tableaux whose reading word is a lattice word. All claims below use the original physical stretch t, not conjugated or relabeled stretching parameters.

## Complete row-word bijection

First remove each empty skew row lambda_i=mu_i=a. Every cell in a row above it is in a column strictly greater than a, and every cell in a row below it is in a column at most a. Consequently no new column comparison is introduced by deleting that row. The reading word is unchanged. Reinsert the row as the inverse. This holds for chains of empty rows and after multiplying the boundary by every positive real or integer t in the row-count model.

For the remaining m nonempty rows, put s_i=lambda_i-mu_i>0 and g_i=mu_i-mu_(i+1)>=0. Define g'_i=min(g_i,s_(i+1)), mu'_m=0, mu'_i=sum_(j=i)^(m-1) g'_j, and lambda'_i=mu'_i+s_i. Partition validity follows from g_i>=max(0,s_(i+1)-s_i), a bound retained by g'_i. Keep nu unchanged. This produces another balanced partition triple, with outer area no greater than the original and maximum trimmed length no greater than the original.

Let a_(i,k) be the number of letters k in row i. Nonnegativity, each row total s_i*t, and each content total nu_k*t are unchanged. For adjacent nonempty rows, the complete column condition is

    sum_(j<=k) a_(i+1,j) - sum_(j<k) a_(i,j) <= t*g_i.

The left side is at most t*s_(i+1), by the lower row total and upper row nonnegativity. Therefore replacing g_i by min(g_i,s_(i+1)) leaves the complete real feasible set unchanged: for g_i<s_(i+1) the inequality is identical; otherwise both old and new inequalities are redundant. Every label k is retained; no support or active-cut guess is made.

Place exactly the same weakly ordered row words in the new skew rows. The reading word is literally unchanged, so every lattice-word/ballot condition holds in the new shape if and only if it held in the old one. The inverse repositions those same rows. Thus the map is a bijection of **all** original LR tableaux, not a face, a section, a selection of contents, or an equality inferred from small counts:

    c^(t*lambda)_(t*mu,t*nu) = c^(t*lambda')_(t*mu',t*nu)  for every integer t>=0.

For t=0 this is the scalar LR identity. Empty positive-stretch families separately have the zero polynomial; this identity does not license fitting a zero family through constant one.

The full real row-count polytopes are identified by the identity on surviving row entries, plus insertion/deletion of identically zero rows. The maps are integral and have integral inverses on their full affine spans. They therefore preserve the saturated affine integer lattices. Any triangular constraints k<=row index after deleting an empty row are consequences of the unchanged lattice-word conditions, rather than newly imposed support restrictions. The construction is homogeneous: min(t*g_i,t*s_(i+1))=t*min(g_i,s_(i+1)). Hence equality is an all-stretch whole-polynomial identity; degree and ordinary signs transfer.

## Tensor operations and positive scale

For padding n>=the ordinary rank, interpret the LR coefficient as the invariant multiplicity of weights (mu,nu,-reverse(lambda)) for GL_n. Permuting the three factors and simultaneously taking their duals preserve this multiplicity. Choose a factor to be the dual of the new outer partition. Subtract the last entries a,b of the other two factors and subtract a+b from the proposed outer partition. This determinant normalization preserves the entire invariant multiplicity. If the normalized outer has a negative last entry, the multiplicity is zero: the other two factors are polynomial GL_n representations and cannot have such a highest weight in their tensor product. A noncontained inner partition likewise proves zero by the full LR rule. Neither a numerical refusal nor an unknown process outcome is used as a zero proof.

For a legal nonnegative target, divide all three partitions by their positive common gcd g and optionally exchange the two inners. The exact identity is P_before(t)=P_after(g*t); g is retained in the trace. Coefficient c_k is multiplied by g^k, so degree and signs, but not necessarily numerical coefficient values, are unchanged.

The implemented grammar permits every legal padding from current rank through seven, both simultaneous-duality choices, each of the three outer choices, both inner orders, and either retaining the gaps or applying the complete gap reduction. Every step is backed by one of these exact identities.

## Termination and admitted terminals

Select a strictly smaller target in the lexicographic measure (outer area, ordinary rank, three trimmed partitions after primitive/inner-order normalization). Every accepted target is a nonnegative integral partition triple of area at most the starting area. This finite set has no infinite strictly decreasing chain. Repeatedly selecting the smallest available strictly decreasing move therefore terminates. The implementation has a separate 64-step guard; reaching it is an unresolved implementation state, not a mathematical theorem terminal.

A fixed point is only irreducible in this chosen decreasing grammar. It is **not** claimed to be a globally canonical representative of every possible LR count identity. Equal literal final triples, with recorded positive scales, nevertheless give a safe shared entire-polynomial representative. The independent verifier need not reproduce the optimizer: it replays each displayed legal step, checks strict decrease, recomputes its target and accumulated scale, and validates the actual terminal.

Rank at most five and outer area at most sixteen use the precisely adopted source theorems. Certified noncontainment or negative normalized outer gives the zero polynomial. A fixed point by itself proves no sign. The source coordinate bound on each original transfers to its final target as an upper bound on polynomial degree; it is not silently treated as actual dimension. Distinct incoming scales must be retained when comparing polynomial values.

## Challenges and evidence limits

Two independently written normalizers (Python and C++) are compared on the entire frozen 4,131-key pilot, with complete traces saved before numerical comparison. Literal small LR checks challenge empty rows, inactive and nearest-active gaps, common dilations and zero families. Complete original-vs-target counts at physical stretches one and two corroborate the pilot's transformations; these finite checks do not replace the all-t proof above. All census membership/trace checks and their measured costs are separate machine-readable evidence.

The original area-thirty census, old terminal proofs and original-preimage multiplicities remain inherited source premises. A new reduction census is a full identity cover only when every expected original residual key is mapped exactly once or retained with an explicit failure. It is not a whole-box positivity certificate until every remaining target's ordinary coefficients are certified. No original bare-triple preimage list is inferred from the multiplicity columns.
