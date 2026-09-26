## Statement, whole object and feasible cone

Let alpha=(alpha1,alpha2,alpha3) be a nonnegative integral partition and let w=(w1,...,wn) be nonnegative integral weights with sum W=sum alpha. The entire family is K_(t alpha,t w), equivalently the ordinary LR family with outer lambda_i=sum_(j>=i) w_j, inner mu_i=lambda_(i+1), and other inner partition alpha. Column-disjoint skew rows give the complete character product of h_(t w_i). This is the full suffix-LR object in the original integer grade and lattice.

The theorem asserted here is c1>=0 for every such nonempty family, at arbitrary label count and weights. More strongly its degree-one homogeneous rational extension is concave on the complete feasible cone. Empty families have the zero polynomial by the campaign convention; concavity is asserted on the feasible cone only. No general skew three-row-inner reduction or assertion about higher coefficients follows.

For fixed n, the feasible cone is

    w_i>=0, alpha1>=alpha2>=alpha3>=0, sum w=sum alpha,
    w_i<=alpha1, w_i+w_j<=alpha1+alpha2 for i!=j.          (1)

Necessity follows from column-strictness: a chosen label occurs at most once per column and two chosen labels at most twice. Sufficiency and the whole cone's generators are proved at the end. Zero labels may be deleted; n<=2 feasible families are points.

Stretching polynomiality is a classical premise: Rassart, `arXiv:math/0308101v2`, Theorem 4.1 and Corollary 4.2, with our outer-partition convention. For fixed n, the suffix lift is linear. The chamber-polynomial theorem supplies continuous piecewise polynomial dependence of all coefficients on the closed rational parameter cones: on a shared rational face, both restrictions count the same integer dilations, so their coefficient restrictions agree identically. The exact Astra007 first-jet formula makes c1 piecewise linear, and integral scaling makes it homogeneous of degree one. This defines the continuous real extension used for concavity; it asserts no Ehrhart polynomial of an irrational polytope.

It therefore suffices to prove concavity on the relative interior of (1), with positive labels, strict shape inequalities and strict single-/two-label inequalities. The result then extends to every face by continuity. For n=3 this relative interior exists as well. The generic internal walls are exactly w(S)=alpha_i, i=1,2,3; simultaneous walls are handled by limits of generic line segments.

## Complete one-, two- and three-occupation contributions

Use Astra007's exact assignment identity. The occupations are (p,q,r), the edge multiplicities (p+q-1,p+r-1,q+r-1), offsets (A0,B0)=(-q-r,-2r), and slopes

    A=v1-alpha1=alpha2+alpha3-v2-v3,
    B=alpha3-v3,
    A-B=alpha2-v2.

All numerator factors at an absent pair and every zero-multiplicity support remain in that identity. In the strict feasible interior, p<=1 cannot contribute because A<=0 and A0<0. If q=0 and r>0, p<=2 cannot contribute because v1<=alpha1+alpha2 makes B<=0 while B0<0. Thus every contributing three-occupied class has p>=2, and a middle-empty two-occupied class has p>=3.

For p,q>=1, p+q>=3 and r>=0 define the positive rational extension of the kernel by

    K(p,q,r)=(2p-3)!!(2q-3)!!(2r-1)!!
              /[2(p+q-2)(2(p+q+r)-5)!!].                (2)

Its use with p=1 or r=0 below is an auxiliary beta identity, not a claim that an excluded assignment has the three-occupied jet. For actual p>=2,q,r>=1 the new kernel proof gives the complete contribution K(p,q,r) max(0,min(A,B)).

For p>=2,q>=1 put

    C(p,q)=B(p-1,q)=(p-2)!(q-1)!/(p+q-2)!,
    L(p,q)=C(p,q)/2-K(p,q,0),
    D(p,q)=C(p,q)/2+K(p,q,0).                            (3)

The last-empty class r=0 has signed linear contribution

    -C(p,q) (alpha2-v2)_+
    -L(p,q) max(0,min(alpha3,alpha2+alpha3-v2)).           (4)

Here L>=0 and D>0. To check the complete jets directly when q>=2, the left chamber has zero constant, zero B derivative, and negative A derivative of magnitude

    L=sum_(j=0)^(q-2) binom(p+j-2,j) B(2p-2,q+j).         (5)

Each term follows by deleting the single zero factor in the A-binomial; the B-binomial equals one. The right chamber has A derivative -C from j=0, and the shifted-wall line identity from the kernel proof gives B derivative C-L=D. At q=1 the missing c edge is supported only on B<=A: direct multiplication gives -C(A-B), with L=0,D=C. These prove (4), including its support boundaries by continuity.

For completeness, (5) equals (3). For q>=2 let f=x^(p-2)(1-x)^(q-2), F(x)=B(p-1,q-1)^(-1) integral_0^x f. The elementary negative-binomial identity gives

    L=integral_0^1 (1-x) f(x) F(x) dx.

The identity is obtained by differentiating x^(p-1) sum_(j=0)^(q-2) binom(p+j-2,j)(1-x)^j; its endpoints are zero and one. Put s=p+q-2. Since

    (1-x)f=(q-1)f/s + [x^(p-1)(1-x)^(q-1)]'/s,

integration by parts, with zero endpoint terms, yields

    L=C/2-B(2p-2,2q-2)/[s B(p-1,q-1)] = C/2-K(p,q,0).

The last equality is the factorial/double-factorial identity. Formula (5) proves L>0 for q>=2, and q=1 gives L=0. It also gives C-L>0 by comparison with the full positive binomial series x^(-(p-1)); alternatively (3) proves this immediately.

For the middle-empty class q=0, write s=p-2>=1 and define

    E(p,r)=(s-1)!/[2(r)_s] + (3/2)_s/[2s(r+1/2)_s] >0.   (6)

Its signed contribution is -E(p,r) B_+. The only internal chamber is B<A because A-B=alpha2>0. Its constant and A derivative vanish by the same single-zero-factor argument, and the B derivative is -E.

At r=1 the missing edge is handled directly: the product B_(p-1)(A-B) B_p(B) at (-1,-2) has zero constant, zero A derivative and B derivative -1/(p-2), which equals (6). The following summation argument may therefore be restricted to r>=2.

Here is an explicit summation check of (6). Apply the right-chamber finite sum (1) in [the occupation-kernel proof](occupation-kernel.md) with q=0,p=s+2. To evaluate it, treat its fixed-s finite rational sum as a function of an auxiliary real q and set p=s+2-q; initially take r>s and q>0. With the notation C0=binom(q+r-1,s)B(s,2r), D0 and V0 of that proof, Dixon simplifies to

    C0 D0=(2r+s)(q-s)_s/[2rs(r+1)_s].

At q=0 this is (-1)^s(2r+s)(s-1)!/[2r(r+1)_s]. The contiguous relation is

    R=(-1)^(s+1)[(r+s) C0 D0/(2r+s) + r C0 V0/(2r+s)]

at the desired q=0. Its first term becomes -(s-1)!/[2(r)_s]. Rogers–Dougall gives the second term -(3/2)_s/[2s(r+1/2)_s]. Finite rational continuation in q and then r removes apparent hypergeometric poles; both final expressions are regular for every integer s>=1,r>=1. This is exactly (6). No convergence assertion at a nonterminating boundary is used: the finite degree s is fixed throughout.

Finally the one-occupied term, including its missing-edge numerator, is Astra007 equation (7). For d=n-2 it contributes

    (alpha2+alpha3) H_d - (1+1/d) alpha3.                 (7)

Equations (2), (4), (6), (7), summed over every labeled assignment or subset, are the whole coefficient. They retain the negative two-occupied terms. The implementation three_row_linear.py is precisely this sum; independent whole counts, rather than these algebraic simplifications, verify its finite controls.

## A weighted intersecting-family lemma

The following classical probability bound is the biased Erdos–Ko–Rado inequality. We include the short spectral proof (credited to Friedgut in Filmus's Analysis of Boolean Functions notes, section 3.1) to fix its full hypotheses. If F is an intersecting family of subsets of an m-element set and 0<=z<=1/2, then its Bernoulli product measure satisfies mu_z(F)<=z. Empty F is included; an intersecting family contains no empty set.

For 0<z<=1/2, generate a disjoint pair of random subsets coordinatewise by probabilities P(1,0)=P(0,1)=z and P(0,0)=1-2z. Each marginal is Bernoulli(z). The conditional Markov operator is reversible and has eigenvalues 1 and -z/(1-z); its m-fold tensor product has eigenvalues (-z/(1-z))^k. Thus its smallest eigenvalue is -z/(1-z). If f is the indicator of F with mean u, disjointness and intersection give <f,Tf>=0. Orthogonal decomposition into the constant and mean-zero parts yields

    0 >= u^2 - z u(1-u)/(1-z),

hence u<=z. The z=0 endpoint is direct. Also mu_z(F)+mu_(1-z)(F)<=1, since F cannot contain both a subset and its complement.

For p>=2,m>=1, these facts imply

    sum_(J in F) K(p,|J|,m-|J|) <= C(p,m)/2.             (8)

Use the exact beta-integral representation on x1+x2+x3=1:

    K(p,q,r)=1/(2 pi) integral
       x1^(p-3/2) x2^(q-3/2) x3^(r-1/2)/(x1+x2) dx1 dx2.

All exponents and denominators are integrable at the stated p>=2,q>=1,r>=0 scope. It follows by x1=y u,x2=y(1-u), then two beta integrals; factorial duplication gives (2).

Set t=x1 and z=x2/(1-t). The sum over F is the integral of mu_z(F) against a positive multiple of

    h_t(z)=z^(-3/2)(1-z)^(-1/2)/[t+(1-t)z].

For 0<z<=1/2, h_t(z)>=h_t(1-z). Pair z with 1-z. The two probability inequalities imply

    h_t(z)mu_z(F)+h_t(1-z)mu_(1-z)(F)
      <= h_t(z)z+h_t(1-z)(1-z).

The right side is attained by a star (all subsets containing one fixed element). Every integral converges: mu_z(F)=O(z) near zero and the star majorant is integrable. For the star, summing monomials gives x2(x2+x3)^(m-1). After setting x1=t,x2=(1-t)y, the elementary integral

    integral_0^1 [y(1-y)]^(-1/2)/[t+(1-t)y] dy = pi/sqrt(t)

reduces its total to B(p-1,m)/2=C(p,m)/2. The integral follows by y=sin^2(theta) and then tan(theta). This proves (8), including m=1.

A second elementary identity, for m>=3,r>=1, is

    (1/2) sum_(p=1)^(m-1) binom(m,p) K(p,m-p,r)
       = (3/2)_(m-2)/[2(m-2)(r+1/2)_(m-2)].             (9)

Indeed factor B(m-2,r+1/2)/(2 pi) out of the sum. The remaining beta sum is the integral of [1-u^m-(1-u)^m]/[u(1-u)]^(3/2). Integrate by parts using [(2u-1)/sqrt(u(1-u))]'=1/[2(u(1-u))^(3/2)]. The endpoint terms vanish and symmetry gives 4(m-1)B(m-1/2,1/2). Substitution yields (9).

## Every whole wall bends in the concave direction

The function is continuous and linear between the declared walls. A slope jump is recorded as the coefficient multiplying a positive-part hinge in its increasing normal direction. Nonpositive jumps prove concavity. Work at a generic internal wall; all unrelated assignment pieces remain linear nearby.

At w(I)=alpha1, let p=|I|>=2 and m=n-p>=1. The last-empty contribution has jump -L(p,m) as A=w(I)-alpha1 crosses zero. The three-occupied contributions add K(p,q,r) for each proper nonempty subset K of the complement with w(K)<alpha3; write J=complement minus K. On this wall the complement weighs alpha2+alpha3 and w(J)>alpha2>half its total. Thus the family of such J, with the full complement included, is intersecting. Equation (8), minus the full-set term K(p,m,0), bounds the positive jump by

    C(p,m)/2-K(p,m,0)=L(p,m).

The net jump is nonpositive. At m=1 both proper-subset sum and L vanish.

At w(K)=alpha3, write r=|K|>=1, m=n-r>=3. The middle-empty contribution has jump -E(m,r) as B=alpha3-w(K) crosses zero. Three-occupied additions require w(I)>alpha1 among the complementary m labels. Their complement J has w(J)<alpha2. Since alpha1>alpha2, a proper I and its complement cannot both qualify. K(p,q,r)=K(q,p,r), so complementary pairing bounds the sum of positive jumps by the left side of (9), even after including the noncontributing p=1 terms as an upper bound. By (6), the net jump is at most

    -(m-3)!/[2(r)_(m-2)] < 0.

The m<=2 cases are boundary faces of the dominance cone, not generic internal walls.

At w(J)=alpha2, let q=|J|>=1 and p=n-q>=2. The last-empty term changes from its left to its right slope with jump -D(p,q)<0 in h=alpha2-w(J). Every active three-occupied min(A,B) contributes an additional nonpositive jump -K(p',q,r). All other terms are linear locally. Thus this wall is also concave. Cases p<=1 cannot occur in the strict feasible interior.

There are no other internal walls: A=0, B=0 and A-B=0 in the complete assignment formula are exactly the three listed kinds, and the absent-middle support has A-B=alpha2>0. One-occupied terms are linear. A generic line crosses finitely many walls, each with nonincreasing directional slope. Hence the whole c1 is concave on the interior. Continuity extends the conclusion to all intersections, empty support faces of individual summands, shape ties, zero weights and dominance equalities in (1).

## From concavity to nonnegativity on the entire cone

Pad alpha to n entries, with zeros after the third; take n>=3. Put d_h=alpha_h-alpha_(h+1) for h=1,2,3, alpha4=0. The constraints (1) say exactly that w belongs to the permutahedron conv{permutations of alpha}. To verify this without an extra premise, sort any real test vector u. Summation by parts expresses u dot w in terms of subset sums of w; (1), balance and nonnegativity bound each by the matching initial sum of alpha. The rearrangement maximum is u dot alpha in that order. Separation therefore gives the convex-hull assertion. Its converse follows from the same inequalities.

The support function of

    sum_(h=1)^3 d_h conv{1_S: |S|=h}

is sum_h d_h sum_(i=1)^h u_(i), exactly the support function of that permutahedron. Thus the two convex sets coincide. The full pair (alpha, w) is a nonnegative combination of rays ((1^h),1_S), h<=3, |S|=h. Rational parameters have a rational such decomposition because the defining finite polytopes are rational. This real-cone decomposition is sufficient for superadditivity, but integer feasibility requires the following additional argument.

For integral (alpha, w), form d_h distinguishable columns of height h. Make a bipartite network: the source supplies w_i units to label i, each label-to-column edge has capacity one, and each column sends its height to the sink. The total required flow is W. For any subset S of labels, its outgoing capacity after optimally placing columns on either side of a cut is

    sum_columns min(|S|,height) = sum_(j=1)^min(|S|,3) alpha_j.

Thus every cut has capacity at least W exactly when the subset inequalities hold. At |S|=1,2 these are (1); at |S|>=3 they follow from nonnegativity and balance. The elementary integral max-flow theorem (unit augmentations with integer capacities) therefore gives a flow of value W. Each column receives its required number of DISTINCT labels, and each label has exactly its prescribed multiplicity.

Arrange the columns in nonincreasing height and sort the labels in each column. This gives column-strict fillings with the required row lengths, although rows need not yet be weakly increasing. Now sort each row increasingly, without changing its label multiset. Column strictness survives: between two adjacent rows, every lower-row entry was paired with a strictly smaller upper entry. The k smallest lower entries have k distinct paired upper entries strictly below the kth lower entry. The kth smallest entry of the entire upper row is therefore strictly smaller than the kth smallest lower entry, including the possibility of extra upper-row entries. This applies at every shared column and every adjacent row. The sorted filling is a semistandard tableau of shape alpha and content w at the ORIGINAL integer grade one. This proves the claimed sufficiency and nonemptiness without inferring integrality from a rational generator decomposition.

Every ray has stretching polynomial one: its shape is an h-by-t rectangle with exactly h positive labels of multiplicity t, so every column is forced. Therefore c1 is zero on every generator. Concavity and positive homogeneity imply superadditivity. Applying it to the complete generator decomposition proves c1>=0 everywhere on (1). The all-zero and n<=2 cases are points; inadmissible data has its separate zero polynomial. This proves the whole stated theorem.

The result expands the complete two-row c1 theorem to every straight three-row Kostka family, and hence its entire suffix-LR realization at arbitrary ordinary outer rank. It does not turn every skew three-row-inner LR coefficient into this class, establish higher coefficients, close a whole ordinary rank, or settle unrestricted KTT. Those remain explicit future bridges.
