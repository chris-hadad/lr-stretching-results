# A55: a complete affine LR representation of every content-balancing gain

Curated mathematical proof from **A55**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

26 September 2026. Root derivation. This is an exact reduction, not a positivity theorem for the general
gain. The accepted FR044 all-two-row theorem is a premise and motivation, not
claimed as a discovery here. Jacobi–Trudi, Pieri and the complete skew Schur
interpretation are the classical ingredients.

## 1. Statement and the literal original boundary

Let alpha be any partition, let a,b be nonnegative integers with a>=b+2,
and let gamma=(gamma_1,...,gamma_r) be a possibly empty list of nonnegative
integers. Suppose |alpha|=a+b+C, where C=sum gamma. Put


```text
x=(a,b,gamma),  y=(a-1,b+1,gamma),
G(t)=K_(t alpha,t y)-K_(t alpha,t x),  t>=1.
```

Here K is the entire straight-tableau weight multiplicity. Reordering content
does not change it. Set c_i=sum_(j>=i) gamma_j and c_(r+1)=0, and define


```text
L0=(C+a, C+b+1, c_1,...,c_r),
M0=(C+1, C,     c_2,...,c_(r+1)).
```

For every positive integer t there is the exact FULL ordinary LR identity


```text
G(t)=c^(t L0-e_1)_(t M0-e_1, t alpha).               (1)
```

Every part here is literal; the simultaneous -1 in the first outer and inner
parts is indispensable. Trailing zero rows may be removed. Zero gamma slots
may also be deleted because their complete symmetric function is one. This is
one affine family of genuine original LR triples, not a selected face, signed
sector or formal cone polynomial. It is NOT a standard stretched LR family:
its boundary has a fixed intercept.

The partitions and containment are valid at every t>=1. The only potentially
tight outer comparison is (a-b-1)t-1>=0; the corresponding inner comparison
is t-1>=0. Comparisons with the lower rows follow from c_1=C and gamma_i>=0.
The difference of total boundary sizes is t(a+b+C)=t|alpha|. Thus neither
partition validity nor size balance is left to numerical checks. At a=b+2,
t=1 the two top outer rows tie legally; at t=1 the inner rows tie legally.

## 2. Proof retaining the once-only shifts

In the ring of symmetric functions, the two-row Jacobi–Trudi determinant gives


```text
s_((at-1,(b+1)t)/(t-1))
   = h_((a-1)t) h_((b+1)t) - h_(at) h_(bt).          (2)
```

The off-diagonal entries are exactly h_(at) and h_(bt). Translating either
-1 into -t, dropping it, or moving it into only one partition changes those
entries. The pair of top skew rows in (1) is (2) shifted C t columns right.
Its columns are disjoint from every lower skew row. The lower rows have
lengths t gamma_i and occupy mutually disjoint column intervals. Therefore
the COMPLETE skew Schur function of (tL0-e_1)/(tM0-e_1) is


```text
(h_((a-1)t) h_((b+1)t)-h_(at) h_(bt)) product_i h_(t gamma_i).
```

Taking the coefficient of s_(t alpha) proves (1), since the coefficient of a
Schur function in a product of complete symmetric functions is its Kostka
number. This uses all tableaux of the skew diagram. The ordinary LR lattice
word condition is supplied by the full skew-Schur coefficient identity; no
unrestricted weight count is mislabeled as an LR tableau bijection.

The equivalent full Pieri decomposition is


```text
G(t)=sum_(j=bt+1)^((b+1)t)
     [s_(t alpha)] s_((a+b)t-j,j) product_i h_(t gamma_i).       (3)
```

The lower endpoint is strict and contains the once-only +1. Formula (3)
identifies a complete positive sum of scalar counts, but does not sign its
ordinary polynomial coefficients.

## 3. General skew output and exact claim ceiling

For any fixed eta contained in alpha, the same argument applies to
K_(t alpha/t eta,t x), with |alpha|-|eta|=a+b+C: multiply (2) by
s_(t eta) and the remaining h factors, then concatenate a disjoint translated
copy of t eta with the preceding skew components. This constructs one full
affine LR triple at every t>=1. All offsets are integer linear functions of t,
apart from the same two -1 first-part offsets. Explicitly, if eta has s
positive parts and H=eta_1 (H=0,s=0 for the empty partition), the unshifted
boundary is


```text
L0=(C+H+a,C+H+b+1,c_1+H,...,c_r+H,eta_1,...,eta_s),
M0=(C+H+1,C+H,c_2+H,...,c_(r+1)+H,0,...,0),
```

with s terminal zeros in M0; the actual boundary is again tL0-e_1,
tM0-e_1,t alpha. Its components are disjoint in columns, and the last straight
component supplies s_(t eta). This also covers r=0. No new alphabet symmetry or
unproved positivity assertion is needed for this extension.

Each of the two unshifted Kostka families is polynomial in t by the accepted
complete LR embedding and stretching polynomiality. Thus their difference is
polynomial even though (1) is not homothetic. For a straight shape on n labels,
the GT ambient dimension bound is D=(n-1)(n-2)/2: n(n-1)/2 nonterminal GT
entries minus the n-1 independent weight equations. Degenerate shapes and
tight dominance faces lower actual degree; a finite reconstruction uses this
bound before looking at its coefficients.

If the before content is feasible, the after content is feasible by scalar
weight dominance, and both ordinary polynomials have constant one. Their gain
has constant zero. If the before family is empty but the after family is
nonempty, the polynomial gain instead has constant one. Equation (1) makes
no t=0 count assertion, because its formal outer/inner boundaries then contain
-1. The point/empty distinction must not be overwritten by evaluating (2) at
t=0 outside its skew-shape domain.

No affine isomorphism between different hive polytopes or inheritance of a BV
metric is asserted. Original lattice conventions are those of the complete
LR coefficient at each displayed integer boundary. Positivity of ordinary
stretched LR polynomials would not by itself establish positivity for these
affine intercept families. The proposed stronger mechanism remains open.

## 4. Exact discriminators and their limits

The root tested every dominance-feasible partition content for every nonempty straight
shape alpha with n=5, alpha_5=0 and alpha_1<=8. The complete declared domain is
15,117 pairs and 92,372 unit-transfer appearances, retaining duplicate transfers
when distinct coordinate choices give the same sorted content. Every entire
polynomial is positive and every gain nonnegative. The degree bound is six;
grades 0..6 determine and grades 7,8 are unused checks. Earlier n=4/max-part-six
and n=5/max-part-four domains overlap this domain and are not extra coverage.
The all-59-weight rank-seven staircase discriminator is a separate higher-degree
test, with exact primitive-face degrees and reciprocal counts in the tournament
proof. It also has no negative gain. These are finite adversarial tests of the
general mechanism, not a proof for arbitrary n, shape or parameter size.

The first five-letter max-part-eight attempt stopped at its prospective 120 s
deadline. It saved progress, not a complete vector file, and supports no complete
domain claim. The fresh streaming version completed in 343.20 s of arithmetic
and retains every exact vector, both holdouts and every compared gain. The old
attempt and its cost remain in the runtime record. No additive campaign total
changes. Verification of (1), invalid shift/endpoint controls and independent
count checks are recorded separately in VERIFICATION.json.

## 5. Consequence for the next proof attempt

KEEP coefficientwise balancing as a serious whole-parent operation. CHANGE its
missing premise to the precise affine family (1), or a coefficient-positive
evaluation of the complete strip interval (3). A solution must pay its strict
endpoint and preserve empty/point cases. The current exact data does not retire
the mechanism. A single negative gain would refute the proposed operation while
leaving both original KTT polynomials potentially positive; a negative whole
parent would instead take the ordinary candidate gate.
