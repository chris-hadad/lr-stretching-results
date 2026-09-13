# Six-run whole-flow elimination and the positive zero-parameter strata

This AI-assisted derivation establishes complete flow identities. No
historical novelty claim is made. All ordinary ranks below refer to the final trimmed
ordinary LR triple, with lambda outer. Source artifact SHA-256:
`ecafc737896425606f6c6a6ece31c1f057010c781abf4253616a798811f71eee`.

## 1. Exact family and the whole LR count

Let a,f>=1 and p,q,r,u>=0 be integers. Place two disjoint supports on the n cuts
of the word

    w=A^a B^(p+1) A^(q+1) B^(r+1) A^(u+1) B^f,
    n=a+f+p+q+r+u+4.

A and B label the two supports. An interval has multiplicity one precisely when
it contains both labels and zero otherwise. Identify an interval of cuts with
an edge i->j on vertices 0,...,n, where its cuts are i+1,...,j. Use direction
R=(1,...,1). Let F_w(t) be the COMPLETE nonnegative integral flow count with
source amount t at vertex 0, sink amount t at vertex n, and zero netflow at
all other vertices. The all-zero flow is the convention at t=0.

Here are explicit ordinary LR boundaries, not a skew rank or graph rank. Set

    mu_i = #{j>=i : w_j=A},
    nu_i = #{j>=i : w_j=B},               1<=i<=n+1,
    lambda=(n-1,n-1,n-2,n-3,...,2,1,1).

Trim trailing zeros in mu and nu only after writing the formulas. Then

    F_w(t)=c^(t lambda)_(t mu,t nu),       every integer t>=0.       (1)

The ordinary rank is n+1 and outer size n(n+1)/2. The sums balance because
mu_i+nu_i=n-i+1 for i<=n and both vanish at n+1. The source/sink adjustment
from this sum to lambda is (-1,0,...,0,+1), of total zero. Lambda is a partition.

For completeness, (1) is an application of the entire support-count character
identity in [the nonnegative-multiplicity lemma](matching-character-premise.md), not an identification of a
coordinate face. Its hypotheses hold as follows. Every cut is covered by
exactly one support, so m_ii=0. For unit R the dominance inequalities
(m_ii-1)R_i+R_(i-1)+R_(i+1)>=0 are zero at the end cuts and one inside.
For the factor of a given support, a Weyl term leaving a selected support cut
loses at least t+1 there, beyond the target exponent t. It cannot contribute
when multiplied by other nonnegative root-series exponents. The surviving
parabolic numerators cancel roots avoiding the support. Multiplying the two
factors and the final Weyl denominator therefore leaves exactly one reciprocal
root for a mixed interval and no root for a monochromatic interval. Extraction
of the dominant target is precisely (1). This is a complete all-t character
count proof, rather than a claim of an affine hive/flow coordinate isomorphism.

The direct source-sink edge is allowed, proving feasibility. An edge is active
if and only if it lies on a source-sink path. Vertices inside the initial run,
and the vertex immediately after that run, cannot receive flow. Vertices at
or after the start of the final run cannot send flow to the sink. The remaining
active vertices are exactly

    source; X(p), L(1), Y(q), U(1), Z(r), V(1), W(u); sink.         (2)

All active interior vertices have both a source edge and a sink edge. In
addition to these and the direct source-sink edge, the COMPLETE internal list is

    X -> Y,U,Z,V,W;
    L -> Z,V,W;
    Y -> Z,V,W;
    U -> W;
    Z -> W.                                                     (3)

A displayed group-to-group arrow means all pairs; no further internal arrows
exist. For example L->U, U->V, and V->W are forbidden because their intervals
are monochromatic. Empty groups in (2) are allowed; L,U,V remain.
The list follows simply by checking whether the corresponding interval
crosses one of the five label changes. Every arrow in (3) lies on a
source-sink path using its source and sink edges, so the list is fully active.

The active graph is connected. If E is its number of edges and v its number
of vertices, averaging its source-sink paths gives a real point positive on
every edge. Hence its affine dimension is E-v+1. Reduced incidence matrices
have forest bases; leaf elimination makes every full-rank forest minor +/-1.
The active incidence lattice is saturated, and all vertices at integral t
are integral. Cut bounds bound every edge by t. Consequently the complete
integral flow polytope has degree

    d=pu+3p+3u+4+qr+(q+r)(p+u+2).                               (4)

For reference v=p+q+r+u+5 and the number of internal edges is
pq+pr+pu+qr+qu+ru+2p+q+r+2u+1. There are 2(v-2)+1 external edges.
Thus (4) is proved before any numerical count. It is independent of a and f,
although the final ordinary rank is not. Common positive integral direction g
replaces F_w(t) by F_w(gt), preserving all signs and scaling c_k by g^k.
The direction g=0 is the separate constant-one case.

## 2. The complete coupled composition identity

Define

    H_(b,c)(z)=sum_(j>=0) binom(b,j)binom(c,j) z^j,
    K=pu+2p+2u+4.

For a q-by-r nonnegative integral matrix M let rho_i and gamma_j be its row
and column sums. Let x in Z_>=0^q and y in Z_>=0^r. Set

 T_(p,u)^(q,r)(z)
 = sum_(x,y,M>=0) z^(sum x+sum y+|M|)
   product_i [binom(x_i+rho_i+p,p) binom(x_i+u+1,u+1)]
   product_j [binom(y_j+p+1,p+1) binom(y_j+gamma_j+u,u)].          (5)

All formal coefficients are finite. Then the WHOLE series is

    sum_(t>=0) F_w(t)z^t
       = H_(p,u)(z) T_(p,u)^(q,r)(z)/(1-z)^(K+p+u+1).           (6)

This identity is not a product guess. Here is a full inverse-preserving
elimination. Eliminate source->X and source->L by their outgoing sums;
eliminate W->sink and V->sink by their incoming sums. The remaining bypass
scalars, each independently nonnegative, are

    source->sink;
    X->sink; source->W; X->W;
    L->sink; L->W; source->V; X->V; L->V.

Their count is exactly K. At U let k be its total through-flow. Its incoming
composition uses source and X, hence p+1 entries, and its outgoing composition
uses W and sink, hence u+1 entries. This contributes

    sum_(k>=0) binom(k+p,p)binom(k+u,u) z^k
       = H_(p,u)(z)/(1-z)^(p+u+1).                             (7)

At Y_i keep M_ij=flow(Y_i->Z_j). Let x_i be its total OTHER outgoing flow,
using V, W, sink: u+2 entries. Its incoming amount x_i+rho_i has p+1 entries,
from source and X. These give the first product in (5). At Z_j let y_j be its
incoming flow not from Y, using source, X, L: p+2 entries. Its outgoing amount
y_j+gamma_j uses W and sink: u+1 entries. These give the second product.

The source amount is exactly the sum of the K scalars, k, all x_i, all y_j,
and |M|. In particular each Y->Z unit is counted ONCE, not once at each end.
Conversely any such nonnegative compositions and M reconstruct every original
edge: the eliminated four types are filled by their indicated sums. These
sums are nonnegative, all vertex equations hold, and the total source and sink
amount agree. This proves both real feasibility correspondence and the
integer count bijection. There is no hidden capacity inequality.

The composition series (7) is the standard two-chain shuffle identity; it is
proved and normalized in the source theorem on ordinal sums of pairs of chains. It also follows by taking
the diagonal coefficients of (1-x)^(-p-1)(1-y)^(-u-1), or by the terminating
binomial identity. Empty parameters give H_(0,c)=1, as required.

As an independent elimination-order check, reverse the active graph, exchange
source and sink, and swap (p,q,r,u) with (u,r,q,p). The same construction now
keeps M^T, swaps x with y, and swaps the two composition factors. Formula (5)
is exactly invariant under this operation. This is an equality of the entire
flow count, not an assertion that different elimination implementations alone
provide arithmetic-engine independence.

## 3. All ordinary signs when any middle run has length one

If at least one of p,q,r,u is zero, the entire series numerator in (6) is a
product of two-chain H factors. Its denominator is (1-z)^(d+1), with d from (4).
The four identities are

    q=0: h=H_(p,u) H_(p+1,u)^r;
    r=0: h=H_(p,u) H_(p,u+1)^q;
    p=0: h=H_(q+1,u)^r;
    u=0: h=H_(p,r+1)^q.                                       (8)

For q=0 or r=0, M is empty and the products in (5) separate, giving (8) from
(7). For p=0, each x_i contributes (1-z)^(-u-2). In each column of M, summing
y_j together with its q entries, with weight y_j+1, gives
binom(h+q+1,q+1) at their combined amount h. Multiplying by binom(h+u,u)
and applying (7) gives the third identity. Graph reversal gives the fourth.
These derivations include intersections of the cases; their numerators agree
there. No nonzero coupling has been discarded in obtaining p=0 or u=0.

Use the cited theorem on ordinal sums of pairs of chains: if an Ehrhart
series has numerator product H_(b_i,c_i) and denominator (1-z)^(D+1), and
D-sum_i(b_i+c_i) is a nonnegative integer, its count equals the order Ehrhart
polynomial of an ordinal sum of pairs of chains followed by that many chain
elements. Every ordinary coefficient is strictly positive. This theorem uses
squared unitary projection norms to obtain nonnegative linear order terms,
and ideal/filter closure plus the order-polynomial coefficient recurrence
for the higher terms. Its strict conclusion is for the Ehrhart shift
Omega(t+1), not an unshifted arbitrary order polynomial. Neither arbitrary
width-two posets nor fixed-weight slices are asserted to satisfy it.

The necessary chain-suffix lengths in (8) are respectively

    pu+2p+2u+4+r,
    pu+2p+2u+4+q,
    3u+4+q(u+2)+r,
    3p+4+r(p+2)+q.

All are nonnegative. This proves:

**Theorem 13.** Every ordinary coefficient of every entire LR polynomial (1)
is strictly positive if at least one of p,q,r,u is zero. This is an
unbounded-rank six-run class, including all simultaneous zero cases, arbitrary
end-run lengths and positive constant integral directions.

Positivity of the entire six-run class remains unresolved. A negative coefficient in this
class must have p,q,r,u>=1. With minimal end lengths its ordinary rank is
therefore at least 11. This is only a six-run constraint. Seven or more runs,
and nonconstant directions, are not excluded at smaller ordinary rank.

## 4. Evidence and premise boundary

The independent check derives allowed edges directly from the word, verifies (4), and compares
full graph counts against (5)-(8) at t=0,1,2 for all 65 parameters in
{0,1,2}^4 with at least one zero. These are regression tests of the proved
identities, not a census or the basis for the infinite theorem. Further graph and
direct LR controls are documented in the source verification record. All arithmetic is CPython exact
integers/rationals. The support character identity and ordinal-sum order-polynomial
positivity are inherited source theorems; their complete proofs are the premises used here, and not all historical
certificates were reproduced.
