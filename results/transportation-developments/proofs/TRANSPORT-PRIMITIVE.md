# General-rank Lagrange Jacobian and an exact primitive

Curated mathematical proof from **Pro029/A006**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Unit7 provider argument. This is a differential-form statement; no all-p transportation remainder theorem is yet claimed. Every occupation is a nonnegative integer; at least three occupied indices are assumed in the endpoint assertion.

For p distinct nonzero nodes define f_i=x_i^(p-1)/product_(j!=i)(x_i-x_j). Then sum f_i=1. Fix x_p. The logarithmic derivative matrix M has off-diagonal entries x_j/(x_i-x_j), diagonal p-1-sum_(j!=i)x_i/(x_i-x_j), and zero row sum. On the Vandermonde vectors x^k, k=0,...,p-1,

```text
M x^k = k x^k - sum_(l=1)^k (sum_j x_j^l) x^(k-l).
```

Its eigenvalues are0,1,...,p-1. The normalized left/right null vectors are f and1. Therefore adj(M)=(p-1)! 1 f^T. Multiplying the appropriate principal minor by product_(i<p)f_i proves

```text
df_1 wedge ... wedge df_(p-1) = (p-1)! product_i f_i Omega,
 Omega=dlog x_1 wedge ... wedge dlog x_(p-1).
```

This is an identity of rational forms, not a claim that the weights are global coordinates or that an integration domain may be replaced by their image.

Choose two occupied indices j,k and let O be the other p-2 indices. Set L=f_j+f_k=1-sum_(ell in O)f_ell and

```text
H(L,z)=sum_(h=0)^(n_j-1) (-1)^h binom(n_j-1,h) L^(n_j-1-h) z^(n_k+h)/(n_k+h).
```

Since partial_z H=(L-z)^(n_j-1) z^(n_k-1), the (p-2)-form

```text
eta= +/- H(L,f_k)/(p-1)! * product_(ell in O) f_ell^(n_ell-1) * wedge_(ell in O)df_ell
```

has d eta=product_i f_i^n_i Omega. The sign is the orientation of the ordered index list. Differentiating coefficients involving only f_O contributes zero after wedging all df_O.

MULTIPLE EMPTY WEIGHTS are retained. The same form is

```text
eta= +/- H(L,f_k)/(p-1)! * product_(ell in O) f_ell^n_ell * wedge_(ell in O)dlog f_ell.
```

On a fixed compact torus at an endpoint, suppose every weight is epsilon^b_i times a uniformly nonzero analytic leading function, b_i>=0, with bounded tangential logarithmic derivatives. Then the apparent empty-weight poles are paired with their own differentials; they do not introduce negative epsilon powers. If k is occupied and shrinking at the first endpoint, H is divisible by f_k^n_k and eta vanishes there. If a different occupied i in O shrinks at the second endpoint, its positive factor proves vanishing there. A third occupied j allows these choices. Stokes on the truncated interval times torus then proves the complete period zero.

This lemma DOES NOT automatically handle an endpoint whose entire shrinking set is empty, nor identify every chamber first jet with such a period. Those two bridges remain explicit Unit7 work. The five-node2|3 concern must not be declared resolved just because the rational primitive exists.

## Later scope resolution

The prospective status above records this lemma's initial checkpoint. Proof003 subsequently closes both missing bridges by complete genuine-wall classification and empty-singleton lower-rank induction. Proof005 gives the whole all-row theorem. The lemma is not itself silently used as that full bridge.
