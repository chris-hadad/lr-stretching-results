# A balanced one-interior kernel and its protected finite interval

Let an entire nonempty period-one polytope have independently established dimension d. Put p=floor(d/2), m=ceil(d/2), so d=p+m. Interpolation on the consecutive nodes -m,...,p has d+1 sites. Treat P(0)=1 as known, count P(1),...,P(p) and the genuine interiors I(1),...,I(m-1), and leave Z=I(m) uncomputed. There are d-1 numerical premises. Reciprocity is P(-j)=(-1)^d I(j); it is not an assumption about geometric reflection.

The Lagrange denominator at the missing left endpoint -m is (-1)^d d!. Its reciprocity sign cancels this denominator sign. Therefore the complete polynomial is

    P(t)=Q(t)+Z K_d(t),
    K_d(t)= product(t-r, r=-m+1,...,p) / d!,

where Q is the unique degree-at-most-d interpolant with the missing value set to zero ONLY as an algebraic coordinate origin. This does not assert the actual interior is empty. All other determining values are unchanged. Q's coefficients are exact rational linear functionals of the d-1 complete counts and c0.

At odd d=2p+1,

    K_d(t)=t product(t^2-j^2,j=1,...,p)/d!.

At even d=2p,

    K_d(t)=t(t-p) product(t^2-j^2,j=1,...,p-1)/d!.

Thus the ordinary kernel has alternating signs; retaining one unknown count is a one-dimensional coefficient interval problem, not automatic positivity. Its leading coefficient is 1/d!, its next coefficient is zero at odd degree and -p/d! at even degree. At either parity d>=3, its coefficient at degree d-2 is strictly negative: respectively -sum(j^2,j=1..p)/d! and -sum(j^2,j=1..p-1)/d!.

Consequently, whenever a separately proved complete geometric theorem protects c_(d-2)>0, that coefficient supplies a finite upper bound on Z. Leading positivity supplies a lower bound, together with Z>=0; at even degree, c_(d-1)>0 may sharpen the upper bound. Multiply each coefficient identity by its exact denominator before exploiting numerator integrality. All complete count values are integers; integer strict positive numerators are at least one. The resulting initial interval is finite and explicit. No top-coefficient sign is inferred from numerical observations.

For each unprotected coefficient, evaluate its affine numerator at the endpoint minimizing it. Every sign is certified if all resulting minima are nonnegative (or positive for strict positivity). If not, refine only the relevant endpoint through a complete geometric upper cover or an explicitly disjoint feasible lower subset. A negative lower endpoint is not an ordinary-negative observation. An inconsistent interval is a premise/count conflict. A negative coefficient upper bound on a nonempty valid interval is an entire-coefficient observation to preserve before comparison.

This single derivation explains the sextic, septic and octic kernels already used in U05–U07. It supplies the correct prospective degree-nine-through-twelve coefficient spaces without assuming future success, emptiness, actual dimension or cheap counts. At degree8 specifically K8 has positive linear and negative quadratic/cubic terms, so a genuine lower bound can be needed for c1 while upper bounds control c2,c3. The target149499 lower-slice repair illustrates that necessity for the sufficient certificate, not a universal need for an extra count.

The formula is elementary interpolation and reciprocity, not a worldwide novelty claim. Its mission role is a uniform sound template for adaptive complete-count certificates. The exact remaining finite populations must still pass their own geometry, paired numerical premises, all exceptions and original-key coverage joins. No further original layer is closed by the formula alone.
