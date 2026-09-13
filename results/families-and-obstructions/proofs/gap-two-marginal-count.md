# Independent gap-two count by one-column marginals

Root derivation for Frontier025 return verification, 10 September 2026. This
counts the complete family of source proof 017. It replaces the source's
three-column convolution, while retaining its full branching and every
Jacobi–Trudi correction. The full LR character identity, saturated GT lattice,
actual dimension ten and codegree classification are separate proof premises.

For detached row lengths `u=(u1,u2,u3)` with sum `2t`, let

\[
 W_s=[z^s]\prod_{j=1}^3\sum_{x=0}^{u_j}(u_j-x+1)z^x,
 \qquad C_u=\sum_s W_s=\prod_j\binom{u_j+2}{2}.
\]

The factor `u_j-x+1` counts the ways to split the remainder of row `j` between
the other two labels. Thus `W_s` is the complete marginal for any one fixed
tail label, with no omitted matrices. Permuting columns preserves the matrix
set. Conditional on that label having total `s`, each other label has mean
`(2t-s)/2`; without conditioning each label has mean `2t/3`.

Use source proof 017's notation: active labels `A`, unit-cap labels `C`, single
hinge labels `S`, and pair-complement labels `J`; write their cardinalities
`p,k,h,j`. Here `j` is zero or one, `C` is contained in `A`, and the sets `S`
and `J` are disjoint from `A` and from each other. These facts follow from
`a>b>=1`, positive tail entries, their sum `a+b+2`, and maximum at most `a+1`.
The full two-row multiplicity at valid tail content is

\[
 1+Bt-\gamma(A)
 -\sum_{i\in S}(\gamma_i-t)_+
 +\sum_{i\in J}(t-\gamma_i-1)_+.
\]

Only labels in `C` can violate content validity, at `gamma_i>t`. Two such
violations cannot coincide because the total is `2t`. A cap violation also
cannot coincide with a single hinge: its label differs from the cap label,
and their totals would exceed `2t`. The unrestricted linear part sums to
`C_u(1+Bt-2pt/3)`. For one violated cap with total `s>t`, its conditional linear
mean is `1+Bt-s-(p-1)(2t-s)/2`. The unrestricted single-hinge sums are
`W_s(s-t)` at `s>t`.

For a pair-complement label, the unrestricted hinge sum is
`sum_{s=0}^{t-2} W_s(t-s-1)`. When a different cap label has total `s>t`, the
pair label has total at most `2t-s<=t-1`; its hinge is therefore linear,
including the zero endpoint. Its conditional mean is `s/2-1`. Subtract this
cap intersection as well. We obtain the complete identity

\[
\begin{aligned}
L_u={}&C_u(1+Bt-2pt/3)\\
&-k\sum_{s>t}W_s\{1+Bt-s-(p-1)(2t-s)/2\}\\
&-h\sum_{s>t}W_s(s-t)\\
&+j\left\{\sum_{s=0}^{t-2}W_s(t-s-1)
       -k\sum_{s>t}W_s(s/2-1)\right\}.
\end{aligned}
\]

Empty sums are zero. The implementation multiplies by six and uses integer
arithmetic before the final exact division. It applies this identity to the
leading detached rows and to both upper adjacent-overlap substitutions, which
still have total `2t`. The bottom overlap has row sum `t-1`; all its caps and
hinges disappear and its complete count is

\[
 \prod_j\binom{v'_j+2}{2}\{1+Bt-p(t-1)/3\}.
\]

All three overlap terms are retained, including the bottom determinant's
three-cycle contribution. Finally multiply the complete tail expression by
the actual top multiplicity `m(u)+1` on `m(u)>=0` and sum over all `u`.
At `t=0` this gives the point count one. No auxiliary summand is identified
with a separate LR stretching family.

The independent implementation is `gap2_marginal_v1.py`. Literal enumeration
of three-by-three matrices checks 352 tail cases and 14 whole-count controls.
It reconstructs all 637 source profiles at all four parameter corners in the
prior degree/codegree space, persists their coefficients, then verifies
separately reserved positive sites. The final certificate checks all 28,028
coefficient entries against the source and finds 7,007 positive base entries.
These corner occurrences are not claimed to be distinct bare triples.

This closes the second-model count obligation for this gap-two family once
the proof and parameter-classification gate is accepted. It does not repair
historical missing provider process receipts. Extension to larger gaps must
retain coincident cap violations and additional determinant corrections; the
one-column formula above is confined to gap two.
