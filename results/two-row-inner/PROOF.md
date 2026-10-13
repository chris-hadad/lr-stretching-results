# Independent proof audit: all two-row-inner ordinary LR coefficients

Curated mathematical proof from **FR044**. The corresponding accepted scope
is stated in the module guide; [the source map](SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Date: 2026-09-26.

This
memo independently reconstructs the complete proof from the supplied U07
sources. No mathematical gap or counterexample was found. The originating memo alone does not establish campaign adoption, publication, human endorsement or an independent review outcome.

The conclusion is uniform in outer rank, size, number of free rows, and
coefficient index. The finite controls below are disconfirmation checks of the
identities and boundaries, not a finite basis for that conclusion.

## 1. Exact theorem and source boundary

For partitions `lambda`, `mu`, `nu`, with lambda outer and at least one of mu,
nu of length at most two, the complete ordinary stretched LR counting family
has nonnegative monomial coefficients. More precisely:

- An infeasible positive-stretch family has the zero polynomial by convention.
- A feasible point family has polynomial one.
- Every other feasible family has strictly positive coefficients in every
  degree from zero through its actual degree.

One may commute the inner factors to write `nu=(A,B)`, `A>=B>=0`. The complete
recognition and degree test is in Sections 2 and 7. No Ferrers conjugation is
used. No assertion is made about arbitrary three-row-inner families, arbitrary
rank seven, unrestricted KTT, affine hive-face metric transfer, or a negative
LR candidate. There is no dependence on missing rank-six numerical fields.

The mathematical antecedents are the complete A006 skew reduction/linear argument and A050 marked-endpoint identity using compatible cycles. The U07 comparison and terminating application are rederived below. The [public source map](SOURCE-MAP.json) pins this complete proof and the trusted [checker](code/check_two_row.py); original source hashes remain provenance, distinct from mathematical verification.

Attribution is preserved: the original complete two-row skew reduction and
point classification are A006 work; the marked/distinguished endpoint identity
is credited in U07 to Pro042/A050, using the Ferroni–McGinnis compatible-cycle
method. The new U07 step is the endpoint symmetric-unimodal comparison and its
terminating whole-parent application. This audit rederives those steps; it makes
no worldwide novelty claim and does not treat provider self-audits as adoption.

## 2. Complete original skew character and feasibility

First check containment `mu subset lambda`, area balance
`|lambda|-|mu|=A+B`, and the partition hypotheses. Failure gives zero at every
positive integer stretch. Pad lambda and mu by zeros to a common length n.

A skew column has at least three cells exactly when
`lambda[i+2] > mu[i]` for some i. Indeed the cells of a fixed skew column form a
consecutive interval of rows: it is the difference between the initial row
intervals occupied by the outer and inner partitions. Three consecutive rows
have a common skew column precisely at that displayed inequality. It scales
by the same positive t. Two-letter column-strict tableaux are then impossible,
so the complete family is zero.

Otherwise put


```text
h_i = max(lambda_(i+1) - mu_i, 0),  h_0=h_n=0,
H = sum h_i,
ell_i = lambda_i - mu_i - h_(i-1) - h_i.
```

The overlap of rows i and i+1 is the prefix of the upper skew row and the
suffix of the lower skew row. Every such two-cell column is forced to `(1,2)`.
In one row, a forced prefix of ones and a forced suffix of twos cannot overlap,
because that would make a three-cell column. Consequently every `ell_i>=0`.
The remaining cells form a single free row interval; free intervals from
different rows share no column. Choosing an arbitrary weak word of ones then
twos in each interval gives every semistandard tableau exactly once. Thus the
full two-variable skew character, not a selected subfamily, is


```text
s_(lambda/mu)(x,y) = (xy)^H product_i h_(ell_i)(x,y).
```

For each positive integer t, all overlaps, intervals and determinant shifts
are exactly t times these original quantities. Delete zero free lengths and
call the remaining list w, with total W. Set `k=B-H`. The prescribed
highest weight after determinant removal is `(W-k,k)`.

Let `h_q(z)=1+z+...+z^q`. The two-variable irreducible character of shape
`(N-j,j)` is `z^j h_(N-2j)(z)` after setting x=1, y=z. For `j<=N/2`, multiplying
by `(1-z)` and extracting `z^j` recovers its multiplicity: the second endpoint
of every dominant character lies strictly to the right of the extraction.
The classical full skew Schur expansion therefore gives, at every positive t,


```text
c^(t lambda)_(t mu,t(A,B))
  = K(w;k;t) := [z^(kt)] (1-z) product_i h_(t w_i)(z).       (2.1)
```

This is an equality of entire original LR counts, with the original integer
stretch and all ballot/column constraints encoded by the complete character.
It does not assert an affine map of hive metrics.

If `k<0`, the determinant shift already exceeds the requested lower part and
the family is zero. Otherwise `2k<=W` follows from A>=B. The remaining exact
admissibility condition is `max(w)<=W-k`. Necessity can be seen directly: if a
largest factor has width L>W-k and the remaining factors have total R=W-L<k,
then `kt<=Lt` and the coefficients of the product at kt and kt-1 both equal
the sum of all coefficients of the remaining factors. Their difference is
zero at every t. Sufficiency follows constructively from the majorization
argument in Section 6, starting from a multiplicity-one parent. The empty list
is admitted only with k=0 and has K=1. Thus no external saturation theorem is
needed for feasibility here.

## 3. Exact transfer identity, shifts, and polynomiality

For a fixed shape `(T-k,k)`, take admissible content
`(w_1,...,w_d,U,V)`, where every unchanged w_i is positive, U>=V>=0, and
`0<delta<=floor((U-V)/2)`. Set


```text
b=delta, c=U-V-delta, C=sum w_i, kappa=k-V.
```

Here b,c>0. The new content `(w,U-b,V+b)` has the same sum and cannot have a
larger maximum, so it remains admissible. Exact multiplication of the four
finite geometric series gives


```text
h_((U-b)t) h_((V+b)t) - h_(Ut) h_(Vt)
   = z^(Vt+1) h_(bt-1) h_(ct-1).                          (3.1)
```

Consequently the difference of the two complete parents is


```text
Delta(t) = [z^(kappa t-1)]
    (1-z^(bt))(1-z^(ct)) product_i h_(w_i t)/(1-z).         (3.2)
```

The offset is the integer `-1`, not `-t`; the two extra cap exclusions are bt
and ct, not bt+1 and ct+1. These details govern the ordinary coefficients.
If kappa<=0, the extraction is at a negative index and Delta is zero. Old
admissibility for U implies k<=C+V, hence kappa<=C. Also `2k<=T` gives


```text
2 kappa <= C+b+c.                                        (3.3)
```

If d=0, admissibility gives k<=V and the zero case has already settled the
transfer. We may therefore suppose d>=1 and `0<kappa<=C`.

For a subset I of the d unchanged labels, put j=|I| and w(I)=sum_(i in I)w_i.
Expand every coordinate exclusion and both extra caps in (3.2). Each of the
four partners has q equal to `kappa-w(I)`, `kappa-b-w(I)`,
`kappa-c-w(I)`, or `kappa-b-c-w(I)` and contributes, with its proper sign,


```text
F_j(q;t) = binom(qt+d-1-j,d) if q>0, and zero if q<=0.      (3.4)
```

The full difference is `sum_I (-1)^j(F_j(kappa-w(I))-F_j(kappa-b-w(I))
-F_j(kappa-c-w(I))+F_j(kappa-b-c-w(I)))`.

There is no nonpositive-slope extrapolation: its actual coefficient index is
negative at every positive t. The full subset j=d is absent since kappa<=C.
Every active upper binomial argument is nonnegative at t>=1, so the product
polynomial agrees with the combinatorial binomial even at early zero grades.
For j<=d-1 the factors `(qt-j),...,(qt+d-1-j)` include qt. Thus every active
term has constant zero. We have proved, before sampling, that Delta is an
ordinary polynomial of degree at most d with constant zero.

## 4. Independent marked-cycle coefficient derivation

Write `G_a(z)=1+...+z^(a-1)`. Let A_h(z) be the descent polynomial of the
permutations of h labels, with A_0=1. For each permutation sigma of the d
unchanged labels, its cycles partition those labels; write w(D) for a cycle's
full capacity. Define


```text
W_(d,h) = sum_(sigma with h cycles) product_D G_(w(D)),
V_(d,h) = sum_(sigma with h+1 cycles) sum_(cycle D)
             |D| z^w(D) product_(E != D) G_(w(E)).
```

Impossible cycle counts contribute zero. V distinguishes both a cycle and one
of its labels. The complete identity is


```text
d! [t^h] Delta
  = [z^(kappa-1)] (1-z^c) G_b(z) A_h(z)
                                  (W_(d,h)+V_(d,h)).      (4.1)
```

Here is the algebra, including the sign of V. Put


```text
f_h(j) = [y^h] product_(r=-j)^(d-1-j)(y+r),
Q_h(z) = sum_I (-1)^|I| f_h(|I|) z^w(I).
```

Taking the ordinary t^h coefficient in (3.4) contributes q^h f_h(j)/d!.
Thus the full coefficient is the coefficient of z^kappa in


```text
(1-z^b)(1-z^c) Q_h(z) sum_(q>=1) q^h z^q / d!.
```

The last series is `z A_h(z)/(1-z)^(h+1)`, including h=0. This follows either
by z d/dz induction or by the Eulerian insertion recurrence below.

Consider


```text
N(y,z) = sum_sigma y^(number of cycles) product_D (1-z^w(D)).
```

Expand by marking an arbitrary set of complete cycles. Fix their union to be
I of size j. The permutations on I and its complement are independent; their
cycle enumerator is


```text
(-y)^(rising j) y^(rising(d-j))
   = (-1)^j y product_(r=1-j)^(d-1-j)(y+r).                (4.2)
```

The rising factorial is proved by adding the largest label either as a new
singleton cycle or in one of the existing cyclic insertion positions. The
identity also holds at j=0,d by cancelling the polynomial endpoint factors.
To obtain the desired product beginning at -j, multiply (4.2) by `(y-j)/y`.
It follows that the required marked sum is N minus `1/y` times its version
weighted by the number j of marked labels.

To count those marked labels, choose a distinguished marked cycle D and one
of its |D| labels. Its factor is `-|D|z^w(D)`; all remaining cycles retain
`(1-z^w(E))`. The preceding subtraction changes this sign to plus. We obtain


```text
N(y,z) + sum_sigma sum_D |D| y^(number of cycles-1)
                                  z^w(D) product_(E!=D)(1-z^w(E)).
```

Its y^h coefficient is `(1-z)^h(W_(d,h)+V_(d,h))`. Cancel this factor against
the power-sum denominator, and cancel `(1-z^b)/(1-z)=G_b`, proving (4.1).
No cycle, subset, distinguished label, or endpoint partner is omitted.
For h=0, W=0 and V=d! z^C, since there are (d-1)! single-cycle permutations
and d choices of distinguished label. Extraction at kappa-1<C gives zero,
independently confirming the constant term.

## 5. Why every ordinary transfer coefficient is nonnegative

A nonnegative symmetric unimodal sequence a centered at mu, extended by zero
at all other indices, satisfies


```text
x>=y and x+y<=2mu  =>  a_x>=a_y.                          (5.1)
```

The hypotheses say exactly that x is no farther from the center than y. This
holds for half-integral centers and for indices outside the support.

Each G_a is symmetric unimodal. For h>=1, A_h has degree h-1 and is symmetric
unimodal as well. For completeness, its coefficients satisfy


```text
a(n,r)=(r+1)a(n-1,r)+(n-r)a(n-1,r-1).
```

Complementing permutation labels proves symmetry. Adjacent subtraction gives


```text
a(n,r)-a(n,r-1)
  =(r+1)(a(n-1,r)-a(n-1,r-2))
   +(n-2r)(a(n-1,r-1)-a(n-1,r-2)).
```

For `1<=r<=floor((n-1)/2)`, both differences are nonnegative by induction,
using symmetry at the possible middle pair; n=1 starts the induction.

Products preserve this property. To see it without invoking a root theorem,
write a symmetric unimodal polynomial of degree L as


```text
a(z)=sum_(r=0)^floor(L/2) (a_r-a_(r-1)) z^r G_(L-2r+1),
a_(-1)=0.
```

All coefficients in this expansion are nonnegative, and every interval has
the same center. The convolution of two interval indicators is symmetric
trapezoidal. Hence every product has the common summed center and is unimodal.
Monomial shifts move that center by their exponent.

For h>=1 every individual W summand multiplied by G_b A_h has degree
`(C-h)+(b-1)+(h-1)=C+b-2`, and therefore center `(C+b-2)/2`.
For a V term with distinguished cycle D, the full shifted product has center
`(C+b+w(D)-2)/2`. The factor |D| is positive. Set


```text
x=kappa-1, y=kappa-c-1.
```

By (3.3), `x+y<=C+b-2`, so (5.1) applies separately to every full W and V
term. Thus (4.1) is nonnegative for every h>=1. We separately proved h=0 is
zero. All ordinary coefficients of the complete transfer are nonnegative.

This also gives a positive integer object for `d![t^h]Delta`: decompose each
full term into centered intervals as above and count its intervals containing
x but not y, with their nonnegative integer multiplicities. An interval
containing y cannot fail to contain x under (5.1)'s hypotheses. This explains
positivity after the complete signed cancellation, rather than assigning
signs to individual inclusion-exclusion terms.

At the balanced boundary `2kappa=C+b+c`, every W contribution cancels exactly
by symmetry. V is then essential; since V_(d,d)=0, the degree-d coefficient
also vanishes. For unchanged weights (1,1), b=c=1, kappa=2, the true difference
is t; W alone predicts zero. The check suite detects this mutation.

## 6. Terminating admissible majorization and paid initial parent

Let x and y be integral content vectors of the same length, total T, and
admissible for `(T-k,k)`. Suppose x majorizes y, meaning its decreasingly
sorted prefix sums dominate those of y. Sort both. If x differs from y, let
i be the first unequal coordinate, so x_i>y_i; let j>i be the first coordinate
with x_j<y_j. Such j exists because the totals agree. For i<=l<j one has
x_l>=y_l, and every affected prefix therefore has surplus at least one.
Moreover


```text
x_i>=y_i+1>=y_j+1>=x_j+2.
```

Replace x_i by x_i-1 and x_j by x_j+1. This is the admitted transfer of
Sections 3–5. The unsorted new vector still has every prefix at least the
corresponding target prefix; sorting can only increase prefix sums. Its
maximum does not increase, so every intermediate parent is admissible.

Before sorting, the integer L1 distance from y decreases by exactly two.
Sorting against a sorted target cannot increase it: if a>=b and c>=d, then
`|a-c|+|b-d|<=|a-d|+|b-c|`, so removing an inversion cannot increase the
matching distance. Thus each step decreases the nonnegative integer distance
by at least two. The procedure terminates at y in at most half the initial
distance, with a nonnegative complete polynomial gain at every step.

For any admitted target y, after padding zeros as needed, take
`x0=(T-k,k,0,...)`. The maximum condition gives its first majorization
inequality, and every longer prefix is bounded by total T. Its complete
polynomial is one, by the explicit two-factor identity


```text
h_a(z)h_b(z)=sum_(j=0)^min(a,b) z^j h_(a+b-2j)(z).
```

This follows by comparing the two triangular/trapezoidal coefficient
sequences. The desired j=kt occurs exactly once when a=(T-k)t, b=kt.
The zero/one-factor cases have the same direct interpretation.

Consequently every admitted target has


```text
K(y;k;t)=1+sum_(finitely many transfers) Delta_step(t).
```

This proves feasibility and ordinary polynomiality for every t, constant one,
and coefficientwise nonnegativity at arbitrary content length. It also proves
`K(y)-K(x)>=0` whenever x majorizes y at fixed T,k. Splitting a weight into
two is included by padding a zero; permutations of contents do not matter.
No changing-shape or arbitrary product-insertion comparison has been made.

## 7. Parity lattice, exact point cases, actual degree, and strictness

For admitted w,k, append `u0=W-2k` to w and delete all zeros. Let m be the
remaining length, and put `S=(sum u_i)/2=W-k`. The list u has even integer
total and every u_i<=S. Tensoring the complete original SL2 character by
`Sym^(t u0)` selects exactly the irreducible of highest weight t u0, since
irreducibles are self-dual and the two-factor formula contains the invariant
once precisely for equal highest weights. Thus K is exactly the invariant
multiplicity of `product_i Sym^(t u_i)`.

If m<=3, the invariant is multiplicity-free and feasible: the triangle
inequalities follow from u_i<=S and the total is even. If one u_i=S, the
other factors have total highest weight S; their unique top component is the
only component that can pair with that factor. Both cases have K=1. The
all-zero list is included. These are the complete point cases, because the
remaining case below has positive degree.

Suppose m>=4, all u_i>0 and all u_i<S. Resolve the tensor product along a
trivalent tree with m labeled leaves. The two-factor identity proves that
the invariant multiplicity counts every nonnegative internal edge label
satisfying the three triangle inequalities and even incident sum at each
vertex. There are exactly m-3 internal edges; all labels are bounded by the
scaled sum of the leaf weights, giving an O(t^(m-3)) upper bound.

The parity of an internal edge is t times the sum of the leaf weights on
one side of its cut, modulo two. These cut parities are necessary by summing
the vertex equations. They are sufficient: at any vertex its three branches
partition the leaves, whose total is even, so the prescribed edge parities
satisfy that vertex equation. The internal edge cosets are otherwise
independent. For a fixed integer cut sum s_e, set


```text
label_e = t s_e + 2 z_e,  z_e in Z.
```

This is an exact affine bijection between the allowed parity lattice and
`Z^(m-3)`. Its translation varies with t; no residue class is thrown away.
There is no assertion that this is a hive-metric isometry.

There exists a point where all vertex triangle inequalities are strict.
For three leaves this is exactly the strict polygon condition. Inductively
separate two positive lengths b,c; the other lengths have sum C and maximum
M. Choose rational v in

    (|b-c|, b+c) intersection (max(0,2M-C), C).

The intersection is nonempty: `|b-c|<C` and `2M-C<b+c` follow from the full
strict polygon inequalities; `2M-C<C` follows from M<C, because at least two
other leaves remain. All other cross-endpoint comparisons are immediate
from positivity. The shorter list consisting of the other lengths and v
still has strict polygon inequalities. Induction gives its strict tree,
and attaching the strict triangle (b,c,v) gives the desired original tree.

A small open box around this strict internal-label point remains feasible.
Scaling that box by t contains a positive constant times t^(m-3) points in
*every prescribed parity coset* for all sufficiently large integer t: each
coordinate interval has length proportional to t and mesh two. Together
with the upper bound and the already-proved ordinary polynomiality, this
proves actual degree m-3 and positive leading coefficient.

Finally prove strict positivity of all coefficients. For m=4, the degree is
one, the leading coefficient is positive, and the constant is one. For m>=5,
merge the two smallest augmented coordinates. Their sum is at most
`4S/m<S`; every other coordinate is already less than S. The merged parent
has m-1 positive coordinates, the same half-total S, and stays strictly
admissible. By induction its degrees 0 through m-4 are strictly positive.
Reversing the merge is a complete admitted split at the invariant shape
`(S,S)`, so Sections 3–6 give a coefficientwise nonnegative gain. The final
parent retains all those positive coefficients and has its new positive
leading coefficient in degree m-3. This proves the exact strict theorem.

For the original triple, therefore, compute H, w, W and k as in Section 2;
then trim zeros from `(W-2k,w)`. A feasible original is a point exactly when
m<=3 or max u_i=S. Otherwise its actual degree is m-3, and every coefficient
through that degree is strictly positive.

## 8. Fresh exact checks and limitations

`check_two_row.py` and `check_translation.py` were newly written for this
adoption. They use only the Python standard library and import no returned
program. The first checker compares ordinary coefficient products to literal
permutation/cycle enumeration, full finite-interval counts, complete
majorization paths, independent tensor-state parity counts, and literal
original LR tableaux read in ballot order. The tableaux routine works on the
original scaled lambda/mu cells; it does not use the skew reduction.

The base roster contains 1,643 transfer vectors with 7,451 coefficient slots,
4,929 direct positive-grade comparisons, and 145 balanced W cancellations.
It checks 717 admitted Kostka vectors (136 points and 581 nonpoints), their
actual degrees and strict coefficients, 5,420 majorization steps, and 2,151
independent interval/parity comparisons. For all contained original shapes
in a 3-by-4 box with skew area at most seven and all two-row contents, it
checks 1,083 triples: 691 empty and 392 feasible, at t=1,2, for 2,166 complete
original comparisons. There are also 12 literal higher-rank original counts
and 21 explicit boundary/invalid-input comparisons.

Dropping V fails on the entire four-unit original family, and replacing the
once-only endpoint shift by -t fails at t=2. The auxiliary six-unit subset
term has c1=-5/4, while its entire parent has
`1+2t+(3/2)t^2+(1/2)t^3`; this confirms that the method must not sign sectors
independently. Additional exact checks retain positive smaller coordinates V,
zero padding, no-unchanged-coordinate point moves, and parity cosets that
change with t; their precise counts are in `EVIDENCE.json`.

The proof, including all shifts, boundaries, parity and actual-degree cases,
is the basis of the recommendation. The remaining required action is root
integration and its fresh independent consequential review, not a missing
mathematical premise. Dependent higher-letter claims still require their own
complete arguments; this memo does not adopt them by association.
