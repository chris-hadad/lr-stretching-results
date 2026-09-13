# W013 independent mathematical verification — WI-271

Status: independently checked in this lane; root adoption and independent review
remain pending. No ordinary-negative whole stretched LR polynomial is established.
The full negative object is a bounded-circulation polytope; it is also an explicit
face of an integral LR row-count triangle whose whole polynomial is uncomputed.
Lambda denotes the outer partition throughout.

## 1. Whole circulation, lattice, integrality and reflection (T01)

For integers n,p>=1, orient two edges v_(i-1)->v_i for each i=1,...,n and
p edges v_n->v_0. The incidence equations equate every bundle sum to one s.
For an integer t>=0, a double bundle has 2t+1-|s| choices for |s|<=2t;
the closing bundle has f_p(s,t) choices, where f_p is the coefficient of
x^(s+pt) in (1+x+...+x^(2t))^p. Thus the complete count is

    C_(n,p)(t)=sum_(s=-2t)^(2t)(2t+1-|s|)^n f_p(s,t).

There are no omitted configurations or weights. The zero-stretch count is 1.
The chart consisting of s, one edge from every double bundle, and the first
p-1 closing flows has n+p coordinates. The missing double flows are s-x_i;
the missing closing flow is s minus the chosen closing flows. Both directions
are integer-linear. Hence the chart identifies the actual cycle lattice with
Z^(n+p), without an index or congruence restriction. The origin is strictly
inside all box bounds, so this is the prior intrinsic dimension.

For completeness, incidence total unimodularity follows by expanding a square
minor along a column with at most one selected nonzero; if none exists, each
column contains its two opposite entries and the selected rows sum to zero.
Appending unit bound rows preserves the same determinant property. A vertex
is defined by a nonsingular augmented system with integral right-hand side,
so every vertex is integral. Ehrhart degree is therefore exactly n+p.

All relative interior lattice points of tP satisfy |f_e|<=t-1, and conversely,
because the relative interior is specified by strict nonredundant box bounds.
Edges with identically zero coordinates, if present in the general-graph form,
add only redundant inequalities. Thus interior count equals C(t-1), and
Ehrhart reciprocity gives C(-1-t)=(-1)^(n+p)C(t). Equivalently, in the cycle
lattice the polar is the convex hull of the restricted integral coordinate
functionals and their negatives. This also directly proves reflexivity.

The finite replay uses a new literal convolution implementation and exact
Newton interpolation at t=0,...,d; the prior degree comes from the geometry.
Both original unused holdouts d+1,d+2 are checked. All 165 frozen pairs
(n>=1,1<=p<=10,n+p<=22) agree: 2475 coefficients and 2805 scalar sites;
22 polynomials are negative somewhere, and the minimum negative degree in
this roster is 18. This is not a universal minimum or LR coverage.

## 2. The all-index p=1 sign theorem and graph realization (T02)

The full count reduces by u=2t+1-|s| to

    C_(n,1)(t)=(2t+1)^n+2 sum_(u=t+1)^(2t)u^n.

Let B_j be defined by z/(exp(z)-1), so B_1=-1/2. Bernoulli telescoping gives
2/(n+1)[B_(n+1)(2t+1)-B_(n+1)(t+1)] for the last term. Expanding at 1,
for 1<=k<=n and m=n+1-k, yields

    c_k=binom(n,k)[2^k+2(2^k-1)B_m(1)/m],
    c_0=1, c_(n+1)=2(2^(n+1)-1)/(n+1).

The only negative Bernoulli values are m divisible by four. For m=4,8,12,16,
the magnitudes 1/30,1/30,691/2730,3617/510 are all <m/2; hence the bracket
is >1. For m divisible by four and m>=20, Euler's even-zeta identity gives

    |B_m|/m=2(m-1)! zeta(m)/(2pi)^m.

The ratio at m+4 divided by that at m exceeds
m(m+1)(m+2)(m+3)/(2(44/7)^4), because pi<22/7 and 1<zeta(m)<2.
At m=20 this rational lower bound is 5798415/85184>1 and it increases.
Since |B_20|=174611/330>20, induction proves |B_m|>m thereafter.
The coefficient bracket is then strictly below 2-2^k<=0. Odd m>1 have zero
Bernoulli number; m=1 and m congruent2 mod4 have positive B_m(1).
Therefore c_k<0 exactly for m=0 mod4, m>=20; every other coefficient is
strictly positive. There are max(0,floor(n/4)-4) negative coefficients.
The finite 80-vector symbolic replay is corroboration of this all-n proof,
not its basis; all 479 supplied scalar controls agree.

For n>=2, take vertices S_i,U_i,M_i around one cycle and edges
S_i->U_i->M_i, S_i->M_i, M_i->S_(i+1), cyclic in i. This is a simple graph
with 3n vertices and 4n edges. Its Hamiltonian boundary visits
S_0,U_0,M_0,S_1,U_1,M_1,...; each added chord S_i M_i lies inside its own
three-vertex arc, so the chords do not cross. Degrees are 3,2,3 per block.
All connectors carry the same s in [-t,t]; each triangle then contributes
the same double-bundle factor. Integer subdivision/contraction maps preserve
the entire count and lattice. At n=20, c1=-168011/165 and degree21.
The independent generic incidence counter verifies the returned 60-vertex
80-edge realization at t=0,1,2. The six additional provider small-n bare
outerplanar controls are not separately recounted here; the general proof,
80 symbolic vectors and these three graph controls are the adopted evidence.

## 3. The p=3 witness and infinite subsequence (T03)

Direct bounded-composition counting gives
f_3(s,t)=3t^2+3t+1-s^2 for 0<=s<=t, and
f_3(s,t)=binom(3t-s+2,2) for t<=s<=3t. They agree at s=t.
Insert these into the complete common-current sum, separating s=0,
1<=s<=t and t+1<=s<=2t. For a polynomial g(s), the linear coefficient
of sum_(s=1)^t g(s) is the functional ell(s^j)=B_j(1).
The range t+1,...,2t has the same linear functional (multiplier2-1).
Every summand with an explicit factor t contributes no linear term because
the sum at t=0 is zero. At t=0 the two kernels times (1-s)^n reduce to
2(1-s)^(n+1)-(1-s)^(n+2) and
((1-s)^(n+1)+(1-s)^(n+2))/2, respectively.
Using ell((1-s)^j)=(-1)^j B_j gives

    [t]C_(n,3)=2n+3+(-1)^(n+1)(5B_(n+1)+B_(n+2)).

At n=15 this is 33+5(-3617/510)=-251/102. The full vector is

    (1,-251/102,151673/204,75595/12,123725/4,3884503/24,
     49288333/72,8449207/4,20276425/4,474808763/48,251027777/16,
     237911869/12,703219907/36,117727253/8,66625533/8,41811965/12,
     1056768,59637763/272,59637763/2448).

It has only one negative coefficient. Fresh complete bivariate Bernoulli
expansion, fresh convolution/interpolation and a new generic edge-list
counter agree. The latter receives only the 49-vertex66-edge simple
subdivision and checks t=0,1,2,3,4,18,19,20, including both unused holdouts.
The chart s,x_1,...,x_15,y,z has inequalities
|x_i|,|s-x_i|,|y|,|z-y|,|s-z|<=1. Its flows are
(x_i,s-x_i) and (y,z-y,s-z), with an integral inverse; it is Z^18.

For m=n+1 divisible by four and m>=16, the Bernoulli magnitude ratio
|B_(m+4)|/|B_m| exceeds
(m+1)(m+2)(m+3)(m+4)/(2(44/7)^4). At m=16 this is
34898535/937024>2. The threshold ratio (2m+9)/(2m+1) is <2.
Since 5|B_16|>33, negativity propagates to n=15,19,23,... .
This is a complete graph-flow theorem; no ordinary LR sign follows yet.

## 4. Entire real LR triangle equals full transportation (T04)

Take r>=2,q>=1 and positive integer margins alpha,beta of common total T.
Put kappa_i=sum_(j=i)^r alpha_j and B=(kappa_2,...,kappa_r).
Use disconnected straight components B,(beta_1),...,(beta_q), from top
to bottom. Offset each component horizontally by the sum of the widths
of components below it: an outer row is h+c and its inner row is h.
This produces partitions Lambda,Mu: across a boundary the next component's
largest outer row equals or lies below the preceding inner row. Let Nu=kappa.
The skew size is |B|+T=|kappa|. All constants scale with t.

Here is the real-coordinate argument, independent of integer counting.
Let a_(h,i)>=0 be the number of label i in row h. Impose row sums,
content sums, the semistandard inequalities

    t Mu_h + sum_(i<=k)a_(h,i)
       <= t Mu_(h-1)+sum_(i<k)a_(h-1,i),

and the ballot inequalities

    sum_(g<h)a_(g,k) >= sum_(g<=h)a_(g,k+1).

For top-buffer row h, induction gives the previous rows supported only at
their own row labels. Ballot inequalities force labels >h to zero. For
h>=2 the column inequality at k=h-1 has equal inner offsets and zero
previous-row contribution below h-1, forcing labels <h to zero. The first
row has no smaller label. Thus a_(h,h)=t B_h and all other entries vanish.
The top component's own remaining inequalities hold because B is a partition.
This induction is valid for nonnegative real coordinates, including t=0.

For a lower component row, its full outer endpoint is <= the preceding
inner endpoint. Therefore every intercomponent column inequality is
automatic. Top label-i minus label-(i+1) surplus is
B_i-B_(i+1)=alpha_(i+1). The total residual content of label i is alpha_i.
At any later ballot prefix, the additional number of i+1 is <=t alpha_(i+1),
and additional i is nonnegative. Every ballot inequality is therefore
automatic for every nonnegative real residual matrix with those contents.

Consequently the q lower rows, read as matrix columns, are EXACTLY all
nonnegative r-by-q real matrices M with row margins t alpha and column
margins t beta. The map fixes the buffer coordinates and inserts M; the
inverse selects those lower coordinates. Both directions are integral with
translation tB. They identify the entire affine integer lattices, so this
is an actual affine lattice isomorphism of the complete LR triangle, not
only a scalar count match. Positive matrix alpha_i beta_j/T proves dimension
(r-1)(q-1); transportation integrality follows from the bipartite incidence
TU proof. Its entire LR stretching count has this degree and P(0)=1.
No other ordinary coefficient signs are implied by integrality.

## 5. True face, explicit parent and exact scope (T05)

For any connected loopless graph with r>=2 vertices, q labelled edges, set
alpha_v=deg(v), beta_e=2. Set M_(v,e)=0 only at nonincident vertex-edge pairs.
These are supporting coordinate equalities of the nonnegative transportation
polytope; the intersection is a nonempty face because M=1 on incidences
satisfies all margins. Given oriented edge u->v at stretch t, assign
M_(u,e)=t+f_e and M_(v,e)=t-f_e. Row margins hold exactly when divergence
is zero. Nonnegativity is exactly the box bound; inverse f_e=M_(u,e)-t is
integral. This is a dilation-compatible affine lattice isomorphism of the
whole bounded-flow polytope to the face. The face dimension is q-r+1.
Transporting through Section4 makes it a face of an actual LR triangle.

For C_(15,3), r=16,q=33, sorted margins are alpha=(5,5,4^14), beta=(2^33).
The explicit full triple is in portable/evidence.json. It independently
reconstructs outer size2593, inner sizes2046 and547, rank48, whole degree
15*32=480, face degree18, codimension462, and66 allowed matrix coordinates.
The negative vector belongs to the face. The full degree480 vector and all
its ordinary signs remain UNKNOWN and were never counted here.

For p=1, alpha=(4^(n-1),3,3), q=2n+1; rank3n+1, degree2n^2,
outer size10n^2+8n+3. For p=3, alpha=(5,5,4^(n-1)), q=2n+3;
rank3n+3, degree2n(n+1), outer size10n^2+22n+13.
There are n buffer rows with total outer size n(2q)+|B| and q lower rows
with outer size q(q+1). Here |B| is 2n^2+1 for p=1 and2n^2+2n+1 for p=3,
which proves the size formulas algebraically. Thus faces of integral LR
triangles have unboundedly many negative ordinary Ehrhart coefficients.
This does not establish the same statement for entire LR polynomials.

## 6. Complete graph tensor repair is genuinely whole LR (T06)

Let m>=2,N>=1, rho=(m-1,...,0). Factoring the alternant gives

    s_(2t rho)(x)=(x_1...x_m)^(t(m-1))
      product_(i<j) sum_(k=-t)^t (x_i/x_j)^k.

Indeed each Vandermonde ratio is
(x_i^(2t+1)-x_j^(2t+1))/(x_i-x_j), and taking out x_i^t x_j^t
produces the centered geometric sum. The uniform weight
(tN(m-1),...,tN(m-1)) in the Nth power is exactly the circulation
count on N distinct copies of every K_m edge. Its prior degree is
N*binom(m,2)-m+1; the zero-dimensional m=2,N=1 case is included.

Set a=N(m-1), top buffer B=a rho, and N lower straight components
Gamma=2rho. Apply the same diagonal offsets as Section4 and set
Nu=(ma,(m-1)a,...,a). The top buffer is uniquely superstandard; remaining
content is uniform (a,...,a), with adjacent-label buffer surplus a.
Every semistandard filling of the lower components with that content is
ballot by the same prefix bound. Distinct components have no shared columns.
Hence the complete ordinary stretched LR coefficient equals the complete
bounded-flow count at every integer t>=0. This uses a full tableau bijection
and a character count identity; it does not assert an unproved flow-to-hive
lattice isomorphism. The N=1 character mechanism is inherited campaign work.

Integrality and reflection apply as before. Writing u=t+1/2 makes the
polynomial even or odd according to d, so
F(t)=(2t+1)^(d mod2)Q(t(t+1)), deg Q=floor(d/2).
The distinct nodes t(t+1) at t=0,...,floor(d/2) determine Q.
The next two nodes are unused holdouts. The new replay reconstructs all
20 frozen vectors (m=3,N1..16; m=4,N1..4),266 scalar sites and444 strictly
positive ordinary coefficients, maximum degree46. This is exactly the finite
roster, with no all-m,N positivity assertion. Full tableaux/character proof
plus independent graph-model computation establishes the full polynomials;
the bare LR checks below are implementation controls, not complete native
reconstructions of the high-degree vectors.

## 7. Bare LR controls, source premises and disposition

The full transport control alpha=(4,3,3),beta=(2^5) has degree8 and vector
(1,95/12,15473/504,5243/72,16157/144,8135/72,647/9,473/18,4243/1008).
A new matrix-margin DP recomputes t=0..10, including unused9,10. The exact
bare triple is ((16,13,10,8,6,4,2),(10,10,8,6,4,2),(10,6,3)).

All12 frozen bare LR sites were independently recounted by the installed
lrcalc2.1 native library: Weyl(3,1) at0..3 gives1,3,5,7; Weyl(3,2) at1,2
gives45,325; Weyl(4,1) at1,2 gives15,65; transport(n,p)=(1,1) at1,2
gives7,19; transport(2,1) at1,2 gives440,15175. Each was a hard-contained
single scalar child with source hashes and verified cleanup. The provider's
copied tableau counter was never executed, imported or used as a local source.

Classical Bernoulli definitions/signs are checked against
[DLMF24.2](https://dlmf.nist.gov/24.2); difference/reflection/power sums against
[DLMF24.4](https://dlmf.nist.gov/24.4); Euler's even-zeta formula against
[DLMF25.6.2](https://dlmf.nist.gov/25.6#E2), all accessed6September2026.
General flow reflexivity is prior art, explicitly confirmed in
[Breuer–Dall, §8 Proposition13/Corollary14](https://arxiv.org/html/1004.3470v1).
The new graph and buffer implications are independently derived above.
Integral Ehrhart polynomiality/reciprocity and the standard LR tableaux rule
remain named classical premises. No novelty or publication-priority audit
was performed. Provider runtime/history/422-input-file-reading statements
remain recorded source assertions, distinct from this lane's live evidence.

## 8. Nonsymmetry obstruction and the remaining bridge (T07/U01)

The sparse graph generating product is product_e h_(2t)(x_u,x_v).
Its largest possible exponent of variable x_v is 2t deg(v): all incident
factors attain that exponent, with positive coefficient. C_(15,3) has degree5
and degree4 vertices, so for t>0 their variable degrees are10t and8t.
Swapping these variables cannot preserve the generating polynomial. Thus it
cannot equal an ordinary straight/skew Schur polynomial in those same16
variables. This excludes exactly that full-character identity, not one
coefficient, a larger alphabet, or extra fixed-content symbols.

The promising remaining obligation is a dilation-compatible ordinary LR
encoding of every edge's two-symbol support, including the nonadjacent
closing pair, as an ENTIRE fiber. It must provide both integer directions,
all ballot/column constraints and t=0, without imposed coordinate zeros,
additional uncontrolled fillings or a sum over LR fibers. The present face
embedding leaves462 dimensions and does not settle this obligation.
Larger Weyl parameters, nonidentical factors, nonuniform weights, alternate
flag/buffer encodings and signs of the degree480 parent remain uncomputed.
No full-negative LR candidate or added original-box coverage is claimed.
