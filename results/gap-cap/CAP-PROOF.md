# A count-preserving cap and exact zero-prefix factorization

## 1. The exact cap theorem
Pad to n parts. Put a=mu+nu-lambda and P_i=sum_(j<=i)a_j, P0=Pn=0.
If some P_i<0, the entire positive-stretch family is infeasible: every permutation
loses a nonnegative amount from a highest prefix, so every Steinberg argument has
that negative prefix. Its polynomial is zero.

Otherwise determinant-normalize the two inners to last part zero. This is legal
for lambda because lambda_n-mu_n-nu_n=P_(n-1)>=0. Let m_i and n_i denote the
successive gaps in the normalized inners, and set

    d_i=a_i-a_(i+1)=2P_i-P_(i-1)-P_(i+1),
    T_i=max(P_i,d_i),
    m'_i=min(m_i,T_i), n'_i=min(n_i,T_i).

Reconstruct mu',nu' by suffix sums of m',n' and put lambda'=mu'+nu'-a.
These are legal balanced partitions and

    c^(t lambda)_(t mu,t nu) = c^(t lambda')_(t mu',t nu')

for EVERY positive integer t. Thus the entire ordinary coefficient vector,
actual stretching degree, feasibility and zero polynomial are preserved.
The maximum trimmed rank cannot increase. The map commutes with integral scaling.

### Legality proof
The original outer gap is m_i+n_i-d_i>=0. If neither gap changes it remains so.
If at least one changes, that new gap equals T_i>=d_i, and the other is
nonnegative, so the new outer gap is nonnegative. The last outer entry is
-a_n=P_(n-1)>=0. Traces match because sum a=0. No feasibility assumption was
used; infeasible but legal triples remain permissible inputs to the identity.

### Complete termwise proof
Suppose m_i>T_i was capped. Any permutation changing the top-i index set loses
at least tT_i+1 in the capped weight tmu'+rho, and at least tm_i+1 in the
original. Both exceed tP_i. The other permutation's prefix losses are nonnegative,
so the term is zero in BOTH entire sums. The same holds for a changed nu prefix.

For a permutation preserving every changed mu prefix, mu-mu' is a linear
combination of their indicator vectors and is fixed by that permutation.
Therefore sigma(tmu+rho)-tmu equals sigma(tmu'+rho)-tmu'. The analogous nu
identity and lambda'-mu'-nu'=-a show that every surviving literal Kostant
argument is identical on both sides. No Weyl term, offset, or support wall is
lost, and no eventual-only count agreement is used.

T_i, the map, and all its branches are homogeneous. Integrality is manifest.
A count identity is sufficient for the ordinary-vector transfer; no stronger
lattice/polytope map is asserted.

## 2. Zero prefixes factor the WHOLE LR polynomial
If P_k=0 for 1<=k<n, all permutations changing the top-k set vanish by their
strict rho loss. The remaining permutations split into S_k x S_(n-k) in each
inner. For their Kostant arguments, the kth prefix is zero, so every positive
root crossing that cut has coefficient zero. The partition function splits as
the product of the two complete within-block partition functions. The restrictions
of rho differ from the smaller-rank rho vectors only by blockwise constants,
which cancel. Hence the full Steinberg sum factors into the two ordinary LR
polynomials on the first k and last n-k entries of each boundary.
The blocks are balanced because P_k=0, and each block remains a partition.
This is an exact all-t proper-block factorization, including empty factors.
At rank six both block ranks are <=5, so these are inherited positive terminals.
When every P_i=0, the cap is the all-empty triple and the original Cartan
polynomial is one. Neither observation requires searching a protected family.

## 3. A compact global rank-six target, with rational directions retained
For H=max(P1,...,P5)>0 divide all capped boundaries by H. This is a rational
normalization, not an instruction to keep only integer H=1 cases.
In coordinates P1,...,P5,m1,...,m5,n1,...,n5, it suffices to consider

  0<=P_i<=1, max P_i=1, P0=P6=0,
  d_i=2P_i-P_(i-1)-P_(i+1), T_i=max(P_i,d_i),
  0<=m_i,n_i<=T_i, m_i+n_i>=d_i.

The reconstruction is explicit:
mu_i=sum_(j>=i)m_j, nu_i=sum_(j>=i)n_j for i<=5, mu6=nu6=0;
lambda_i=mu_i+nu_i-(P_i-P_(i-1)), including lambda6=P5.
This is a complete compact normalized parameter domain for the cap images.
The zero-prefix boundary is already a proper-block product as above.

Strict peak indices, at which d_i>P_i, are nonadjacent: this would require
P_i>P_(i-1)+P_(i+1)>=P_(i+1), incompatible with a strict adjacent peak.
There are13 independent subsets of the five-vertex path. For each such subset S
and each of five possible maximum indices k, define one closed polyhedron:
P_k=1; d_i>=P_i,T_i=d_i for i in S; d_i<=P_i,T_i=P_i for i not in S;
and the remaining inequalities displayed above. All rational normalized images
are covered, assigning equality ties to the nonpeak side if needed.
Thus AT MOST65 explicitly specified closed bounded polyhedra cover the domain.
Some may be empty or overlap; no feasible-piece or LR-polynomial-chamber census
is claimed. Each has at most14 free real coordinates.

At rank six the outer area has the sharper bound

    |lambda'| = sum_(i=1)^5 i(m'_i+n'_i)
                 <=2 sum_(i=1)^5 i T_i <=36 H.

For H=1, sum i T_i is convex on the cube [0,1]^5, so its maximum is achieved at
a binary vertex. The complete32-vertex rational certificate has maximum18,
attained only at (1,0,1,0,1). This proves the displayed all-parameter bound,
not a sample extrapolation. It is sharp for legal cap images: set this prefix
vector times H and m=n=(2H,0,2H,0,2H). The resulting outer partition is
(11H,9H,7H,5H,3H,H) and both inners are (6H,4H,4H,2H,2H,0).
That extremizer has zero prefixes and belongs to an already protected product
boundary; it is not offered as a new sign problem.

For rational boundaries, define their degree-j coefficient by denominator
clearing: f_j(b)=q^(-j)[t^j]P_(q b)(t). This is independent of q, since equality
of whole counts gives P_(k q b)(t)=P_(q b)(kt). Hence normalization preserves
signs. The homogeneous coefficient functions may therefore be studied on the
rational points of this compact cover. Arbitrarily large denominators remain:
THIS IS NOT A PROOF FROM INTEGER PARTITIONS OF OUTER AREA<=36, not an original
area-thirty box extension, and not a license to interpolate across LR chambers.
The compact cover by itself is not a coefficient-sign proof. The later
whole-rank-six theorem supplies its separate sign conclusion.
