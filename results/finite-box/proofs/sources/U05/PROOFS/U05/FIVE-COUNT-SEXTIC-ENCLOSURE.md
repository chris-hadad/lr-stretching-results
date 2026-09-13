# A five-count enclosure for a complete sextic LR polynomial

Assume the whole nonempty period-one LR hive has an explicit complete saturated
six-coordinate affine chart and a strict point proving actual dimension six.
Assume every primitive inward normal has squared Euclidean norm at most six in
that chart. The precisely inherited complete two-cone theorem then gives c4>0;
intrinsic top coefficients give c5,c6>0. No coordinate upper bound alone gives
these premises, and an identification of a face is insufficient.

Let A=P(1), B=P(2), C=P(3), U=I(1), V=I(2). All are whole counts and the actual
dimension parity is even, so I(j)=P(-j). Define exact rational numbers

    a = (8(A-U)-(B-V))/12,
    b = ((B-V)-2(A-U))/12,
    e = (16(A+U)-(B+V)-30)/24,
    f = ((B+V)-4(A+U)+6)/24,
    h = (C-1-3a-27b-9e-81f)/120.

Set x=c6, which is not determined by these five counts. Direct coefficient
algebra on the full degree-at-most-six space, with c0=1, gives

    (c1,c2,c3,c4,c5,c6)
      = (a+4h-12x, e+4x, b-5h+15x, f-5x, h-3x, x).

Thus P(t)=P0(t)+x N(t), with

    P0(t)=1+(a+4h)t+e t^2+(b-5h)t^3+f t^4+h t^5,
    N(t)=t(t^2-1)(t^2-4)(t-3).

This identity is checked at every affine coefficient-space coordinate, not
inferred by fitting a sample of LR polynomials. N vanishes at the five observed
grades -2,-1,1,2,3 and at 0. The remaining one-dimensional uncertainty is explicit.

Every genuine relative-interior count is nonnegative. For each chosen integer
q>=3, N(-q)=q(q^2-1)(q^2-4)(q+3)>0. Consequently

    x >= -P0(-q)/N(-q).

The adopted geometric signs additionally imply x>=0, x<=f/5 and x<=h/3. Hence,
using q=3,...,7 (any fixed finite such set is sound), let

    lo=max(0, max_q -P0(-q)/N(-q)),    hi=min(f/5,h/3).

The true x lies in [lo, hi]. No I(q) for q>=3 is computed, or asserted zero, in
this screen. The resulting rigorous coefficient lower bounds are

    c1 >= a+4h-12hi,   c2 >= e+4lo,   c3 >= b-5h+15lo.

If all are nonnegative, the complete polynomial is ordinary nonnegative, with
c0=1 and its independently protected c4,c5,c6. Positive lower bounds give strict
positivity through degree six. This does not reconstruct a coefficient vector.
A negative lower bound is only an inconclusive sufficient test. Conversely,
a strictly negative maximum over this same interval for one coefficient would
be an actual negative whole-LR observation under all these premises, under the stated complete-object hypotheses.

The simplex polynomial binomial(3t+6,6) challenges universality: this particular
five-count enclosure is inconclusive even though its complete product formula
is ordinary positive. The first implementation's test incorrectly demanded
that all scaled simplex controls pass; the failed test and corrected, unchanged
algebraic method are retained. This failure does not refute soundness or imply
an LR negative. The simplex is auxiliary unless an entire LR bridge is supplied.

For a valid sextic on which this criterion is inconclusive, a complete
D+1-node reconstruction on -3,...,3 additionally evaluates I(3), with positive
holdouts 4,5 in both models. That procedure reconstructs the full polynomial.
Hidden-dimensional or unresolved-affine charts require an actual-dimension
certificate or reconstruction in the full prior positive-node space.

Provenance: the degree-five analysis's incomplete-count sign-dual design and the original accepted
LR polynomiality/reciprocity, intrinsic top signs and short-normal theorem.
The construction combines a five-count, one-free-coefficient enclosure with
these geometric sign premises.
