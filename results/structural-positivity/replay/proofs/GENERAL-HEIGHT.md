# The interior staircase shift at arbitrary height

This arbitrary-height extension has independent verification and mathematical
review at the scope stated below. The earlier height-three derivation supplies
the starting argument; the generalization is a separate contribution.
Novelty and polytope integrality or reflexivity are not claimed. Verification
includes a fixed constructive witness check, not a new search for coefficients.

## Statement

Let h>=2, m>=h and w>=1 be integers, and let
alpha_1>...>alpha_h>0 be integers of sum mw. Set

    P(t)=K_{t alpha,((wt)^m)},
    D=(h-1)m-h(h+1)/2+1,
    delta^(r)_i=r+h+1-2i, 1<=i<=min(r,h).

In particular delta^(m)=(m+h-1,m+h-3,...,m-h+1), of total mh.
The entire Kostka count is the ordinary LR stretching coefficient with
outer lambda=w(m,m-1,...,1), inner mu=w(m-1,...,1), and nu=alpha.
Its actual degree is D. For every integer q>=1,

    (-1)^D P(-q)=K_{q alpha-delta^(m),((qw-h)^m)}.       (G1)

A negative content, nonpartition or negative shifted part means zero; zero
shape/content means one. Its exact interior codegree is

    q0=max(ceil(h/w), max_(i<h)ceil(2/(alpha_i-alpha_(i+1))),
           ceil((m-h+1)/alpha_h)).                     (G2)

The negative integer root set is precisely {-1,...,-(q0-1)}. For q>=q0,
(-1)^D P(-q)>0. Multiplicities of those integer roots are not specified.
Negative-argument values are not negative ordinary coefficients.

## Complete count and affine lattice

A semistandard tableau of shape alpha and content (L^m) is equivalent to
partitions x^(r), r=0..m, with x^(0)=0, x^(m)=alpha, sum x^(r)=rL,
at most min(r,h) parts, and

    x^(r+1)_i >= x^(r)_i >= x^(r+1)_(i+1).

The inequalities say that the boxes labelled r+1 are a horizontal strip.
They imply within-row partition order; nonnegativity is included by padding
missing coordinates with zero. Thus the chain is the full counting polytope,
not an auxiliary face or fitted model.

The nonterminal coordinates number

    sum_(r=1)^(m-1) min(r,h) = hm-h(h+1)/2.

The m-1 row-sum equations are independent, since their variable supports
are nonempty and disjoint. Eliminating one coordinate per row identifies the
affine integer lattice with Z^D: the coefficient of each eliminated coordinate
is one. This same elimination at stretch q is compatible with dilation.
All coordinates are bounded by the fixed nonnegative terminal shape, so this
is a bounded rational polytope. Full dimension is proved below, rather than
assumed from this ambient coordinate count.

The skew diagram lambda/mu consists of m column-disjoint rows of length w.
Its skew Schur function is h_w^m. The coefficient of s_alpha is the stated
uniform-content Kostka number, proving the full ordinary LR identity at
every nonnegative integer stretch. Stretched LR polynomiality is the standard
Rassart premise; it does not itself prove ordinary coefficient positivity.

## Uniform nonemptiness lemma

Every partition beta of mL with at most m rows admits content (L^m).
Here is a constructive proof, including degenerate beta. If L=0 everything
is empty. Otherwise let s be the number of positive parts of beta.
When m>s, remove the bottom cells in the rightmost L nonempty columns.
There are at least L columns since beta_1>=mL/s>=L. Column heights remain
nonincreasing after this suffix removal. The removed cells form one horizontal
strip and the remaining partition has at most s<=m-1 rows.
When m=s, first remove all beta_s cells of the last row (beta_s<=L), and
remove bottom cells in the rightmost L-beta_s columns strictly to their right.
There are enough columns since beta_1>=L; the two chosen column sets are
disjoint. The result is a partition of (m-1)L with at most m-1 rows.
Repeat and reverse the strips. Padding zeros supplies the required chain.
This proves sufficiency directly, without presuming feasible GT data.

## Strict chains and the exact integer translation

The staircase has row sum rh. Adjacent positive-coordinate interlacing gaps
are one. Zero-boundary positivity gaps need not all be one: for r>=h the
last coordinate is r-h+1. This distinction corrects an overly compressed
reading of the height-three argument; the integer bijection still holds.

In any integral strictly interlacing chain, x^(h)_h>=1. At row h, strict
interlacing through row h-1 gives x^(h)_i>=x^(h)_(i+1)+2, hence
x^(h)_i>=2(h-i)+1. Propagating strict diagonal inequalities backward to r<h
and strict same-coordinate inequalities forward to r>h yields

    x^(r)_i >= r+h+1-2i = delta^(r)_i.

Consequently subtracting delta makes every coordinate nonnegative. Each
adjacent-positive strict gap decreases by exactly one, producing weak
interlacing. The last-coordinate inequalities remain weak by the derived
coordinate lower bounds. Row sums decrease by rh, and the terminal shape
becomes q alpha-delta^(m). Conversely, adding delta to any such weak chain
makes all adjacent-positive gaps strict and all relevant zero-boundary gaps
positive. The two maps are inverse integer translations.

There is no hidden affine-face premise. For sufficiently large q the shifted
terminal data are a nonnegative partition of m(qw-h), and the preceding
nonemptiness lemma produces a weak chain. Adding delta supplies a point strict
in every interlacing inequality except forced equalities between omitted zero
coordinates. Dividing by q gives a strictly feasible real point in the original
row-sum affine space. Thus its affine hull has exactly dimension D, and its
relative interior is described by these strict inequalities. This also covers
D=0: all remaining inequalities are strictly satisfied at the unique point.

The shifted data are valid exactly when

    qw>=h,
    q(alpha_i-alpha_(i+1))>=2 for all i<h,
    q alpha_h>=m-h+1.

They are monotone in q and sufficient by the constructive lemma. Hence the
integer translation and rational Ehrhart-Macdonald reciprocity prove (G1),
(G2), and the complete negative-integer-root set. Rational leading growth has
order t^D; LR polynomiality then gives actual polynomial degree D. No lattice-
polytope or reflexivity assertion is required for reciprocity.

## Reflection families and half-degree reconstruction

Specialize alpha=delta^(m) and w=h, and call the full LR count J_(m,h)(t).
The translated interior at q has count J_(m,h)(q-1). Therefore

    J_(m,h)(t)=(-1)^D J_(m,h)(-1-t).

Let e be D modulo2. The invariant ring for t->-1-t is Q[t(t+1)], and its
anti-invariant polynomials are (2t+1) times that ring. Explicitly, put y=t+1/2
and use even/odd powers of y. Thus a unique rational R_(m,h) satisfies

    J_(m,h)(t)=(2t+1)^e R_(m,h)(t(t+1)),
    deg R_(m,h)=floor(D/2), R_(m,h)(0)=1.                (G3)

For positive scalar reconstruction, evaluating J at t=0..floor(D/2) determines
R at distinct arguments t(t+1), after dividing by (2t+1)^e. Two further t values
are genuinely unused checks. This halves the determining degree only for
families with the proved reflection identity, not arbitrary LR polynomials.
It is a mathematical reduction here; no new set of higher-height counts was computed.

For each root xi=u+iv of R, its two preimages are (-1+/-sqrt(1+4xi))/2.
Exactly one has positive real part iff u+v^2>0. This follows by solving
Re sqrt(1+4xi)>1 and squaring only when 1-4u>=0; if 1-4u<0 both inequalities
already hold. The double preimage xi=-1/4 is t=-1/2 and contributes no RHP root.
Counting multiplicities, J's RHP count therefore equals the number of R roots
outside u+v^2<=0, for either parity e. The additional odd factor lies at -1/2.
This is a root-location equivalence, not an ordinary-sign equivalence.

This generalizes the height-three family J_m. Codegree one by itself does not imply
reflection; the specialization alpha=delta^(m), w=h supplies it. Nor does this
functional equation establish an integral/reflexive polytope or a uniform
instability/positivity theorem.

## Natural family and an explicit deflation boundary

At h=3,m=3a,w=1,alpha=(a+1,a,a-1), a>=2, (G2) gives q0=4 and D=6a-5.
The full count factors as binom(t+3,3)Q_a(t), with Q_a(0)=1 and degree 6a-8.
At q=4, the shifted shape is (a+2,a,a-2) and content (1^(3a)). The standard-
tableau determinant gives

    -P_a(-4)=54(3a)!/((a+4)!(a+1)!(a-2)!).

The three negative integer roots are exactly -1,-2,-3; their possible extra
multiplicities remain in Q after division once each. The root count in the
open right half-plane is unchanged. There is no automatic LR realization for Q.
Indeed the independently verified a=2 scalar P_2(2)=135 gives

    Q_2(2)=135/binom(5,3)=27/2.

Thus this particular unscaled quotient cannot be any ordinary LR stretching
polynomial: its value at an integer is not integral. This excludes neither a
rescaled/otherwise altered construction nor quotients at other a. It is not an
ordinary-negative example. A constant or alternating-basis sign cannot replace
full ordinary coefficient verification.

## Sources and verification scope

The starting point is the height-three interior-shift derivation and its
independent reconstructions. The arbitrary-height proof is the extension given
here.
Its standard premises are Rassart, Corollary4.2 (arXiv math/0308101), and rational
Ehrhart reciprocity (for example Beck--Ehrenborg, arXiv math/0504230). The
standard-tableau formula is used only on the displayed explicit three-row shape.
No publication-priority search or novelty claim has been made.

A fixed constructive witness check covers h2..8, m=h..h+4, two specified shape
families, and q=q0,q0+1. It verifies row sums, every strict/weak inequality,
forward/inverse translation and degree bookkeeping. It counts no tableaux or
new polynomial coefficients. All uniform claims rest on the complete argument
and its independent mathematical review, not on this finite check.
