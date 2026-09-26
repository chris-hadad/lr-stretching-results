# Whole rank-six first coefficient from tree cones

## Fixed original flow system and all bases

Let E be the 15 ordered edges (i,j), 1<=i<j<=6, in lexicographic order.
Let A have column e_i-e_j for each edge, with the sixth row removed. Its
integer kernel has dimension ten. For a in Z^6 with sum zero, let

    K(a)=#{x in Z^15 : x>=0, A x=(a_1,...,a_5)}.

This is the original complete positive-A5 root-flow count. It is zero unless
all five original prefixes of a are nonnegative. Conversely those conditions
suffice: use the adjacent-edge flow x_(i,i+1)=sum_(j<=i) a_j. Thus the support
rule is exact, including its zero-prefix faces.

The nonsingular five-column bases are exactly the labeled spanning trees T
on six vertices; there are 6^4=1,296, with no orientation choice because every
original edge is oriented upward. Let B_T be the five-by-five basis matrix.
It has determinant plus or minus one. Put

    x_T(a)=B_T^(-1)(a_1,...,a_5).

Each coordinate is a signed sum of a over one side of its tree-edge cut.
For each edge e outside T, the primitive tangent generator u_(T,e) has its
non-tree coordinate e equal to one, other non-tree coordinates zero, and
its five tree coordinates equal to -B_T^(-1) A_e. These ten columns form a
basis of the complete saturated integer flow kernel: non-tree coordinates
give an integer inverse, using the unimodularity of B_T.

Choose a single integer functional ell on all 15 edge coordinates with
ell_e=2^r for edge index r=0,...,14. Every u_(T,e) is a signed fundamental
cycle, with distinct nonzero coordinates in {1,-1}. Therefore

    w_(T,e)=ell(u_(T,e)) != 0.

Indeed the largest power of two exceeds the sum of all smaller powers that
could occur. One common ell is used for every vertex and every Weyl term.
Define q_T(a)=sum_(e in T) ell_e (x_T(a))_e.

## A polynomial attached to each tree cone

Define the finite univariate series, through degree ten,

    R_T(z)=product_(e outside T) z/(1-exp(w_(T,e) z))
          =sum_(h=0)^10 r_(T,h) z^h + O(z^11).

All coefficients are rational and every w is nonzero. Bernoulli series compute
them exactly, with all original denominator signs. The cone's ray-specialized
Brion constant is the polynomial

    F_T(s)=sum_(h=0)^10 r_(T,10-h) s^h/h!,
    J_T(s)=F_T'(s)=sum_(h=1)^10 r_(T,10-h) s^(h-1)/(h-1)!.

This one-variable constant operation is appropriate HERE because the COMPLETE
Brion sum is holomorphic and equals the finite lattice count. It is not used
as the multivariate BV scalar projection in DIRECT-SCALAR-PROJECTION.md.
The two roles of constant extraction must not be interchanged.

For an open root-flow chamber C, let Trees(C) be all bases whose five basic
flows are positive there. Every generic integer a in C gives a simple integral
flow polytope with exactly these vertices and the stated unimodular tangent
cones. Brion's identity, followed by constant extraction, gives

    K_C(a)=sum_(T in Trees(C)) F_T(q_T(a)).

This is its correct degree-at-most-ten chamber polynomial. The construction
requires no monomial expansion in five supply variables and no precomputed
chamber catalog. Trees can be enumerated completely by labeled Prufer words.

## Exact face selection without discarding offset terms

Let zeta=(1,1,1,1,1,-5), and take epsilon=1/12. For every tree, each coordinate
of x_T(zeta) is a nonzero signed integer of magnitude at most five. For any
integral supported a, the perturbed vector a+epsilon*zeta is strictly inside
the positive root cone and on no basis wall: its tree coordinates are integers
plus nonzero fractions of absolute value less than one. Let C(a) be its unique
open chamber.

The unimodular partition theorem supplies K_C on C-Z, where
Z=sum_(e in E)[0,1] A_e is the root zonotope. Since

    zeta=sum_(i=1)^5 i (e_i-e_(i+1)),

we have epsilon*zeta in Z. Hence a belongs to C(a)-Z and

    K(a)=K_(C(a))(a)
        =sum_(T: x_T(a+epsilon*zeta)>0) F_T(q_T(a)).

This proves the actual original-lattice count on every support face, including
a=0. It is not a continuity assertion or a claim that any arbitrary adjacent
polynomial gives the same off-chamber count. Unsupported a still has count zero.
The only external extension premise is the cited unimodular C-Z theorem.

## Whole Steinberg expression and a uniform eventual grade

Let b=(lambda;mu,nu) be any balanced legal integral partitions padded to six
parts, lambda outer. For every pair p,q in S6, with rho=(5,4,3,2,1,0), set

    gamma_(p,q)=p mu+q nu-lambda,
    delta_(p,q)=p rho+q rho-2rho.

The complete Steinberg formula at positive integer stretch t is

    P_b(t)=sum_(p,q) sign(p) sign(q) K(t gamma_(p,q)+delta_(p,q)).

All 720-by-720 pairs and all rho offsets are retained before an exact support
rule is applied. No particular inner-gap region or actual dimension is assumed.
For any subset of m coordinates, the corresponding sum of delta has absolute
value at most 2m(6-m), whose maximum is 18. This follows by comparing the
smallest and largest m-element sums of rho in each of the two permutations.
Every tree basic-flow coordinate of delta is such a signed cut sum, so the
same bound applies. Every basic-flow coordinate of gamma is integral.

It follows that for every integer t>=19 the actual root support is determined
by the lexicographic signs of each prefix pair (prefix(gamma),prefix(delta)).
A negative pair makes the whole term zero. On an admitted pair, a tree belongs
to C(t gamma+delta) exactly when all five triples

    ((x_T(gamma))_i, (x_T(delta))_i, (x_T(zeta))_i)

are lexicographically positive. A first nonzero gamma component dominates its
delta and perturbation because 19-18-5/12>0. If gamma is zero, the integer
delta sign dominates; if both vanish, zeta supplies the exact face choice.
Thus one fixed complete tree set B_(p,q)(b) works for all t>=19, including
zero slopes and every tied wall.

Consequently the original WHOLE LR polynomial agrees at all integers t>=19
with the finite polynomial

    sum_(p,q admitted) sign(p) sign(q)
        sum_(T in B_(p,q)(b)) F_T(t q_T(gamma_(p,q))+q_T(delta_(p,q))).

Whole LR polynomiality makes this equality an identity. Individual root terms
need not be polynomial at their initial grades for this inference. Differentiating
the complete identity at zero proves the explicit first-jet formula

    c1(P_b)=sum_(p,q admitted) sign(p) sign(q)
        sum_(T in B_(p,q)(b))
            q_T(gamma_(p,q)) J_T(q_T(delta_(p,q))).

No coefficient-extraction oracle, unknown chamber polynomial, asymptotic limit
of c1 or interpolation is hidden in the formula: all 1,296 tree inverses,
primitive cycle weights and eleven rational series coefficients are fixed
finite data, and all input-dependent tests are exact integer sign tests.
An implementation can group identical terms only after retaining their signed
multiplicities. The formula automatically gives zero for gamma=0 contributions.
Point, infeasible and lower-degree whole families follow from the same whole
polynomial identity; the all-empty triple has c1=0 separately.


## Primary and accepted premises

- Brion's lattice generating identity and the unimodular-basis counting construction are classical; see De Loera and Sturmfels, Algebraic Unimodular Counting, sections 2-4: https://arxiv.org/pdf/math/0104286 .
- The exact unimodular chamber extension to C-Z is Theorem 13 in Baldoni and Vergne, Kostant partitions functions and flow polytopes: https://webusers.imj-prg.fr/~michele.vergne/publications/kostant.pdf . Its degree-ten A5 context and actual root-zonotope convention are retained.
- The complete original Steinberg formula, ordinary LR polynomiality, padding and balanced outer-partition conventions are already accepted campaign premises, used with all original offsets in A18 STRUCTURAL-FACTOR-PROOF.md. No regional suppression from that theorem is assumed here.
- Labeled-tree enumeration, incidence-matrix unimodularity and the fundamental-cycle kernel basis are standard finite graph facts, made explicit above. This campaign derivation asserts no worldwide novelty or external expert acceptance.
