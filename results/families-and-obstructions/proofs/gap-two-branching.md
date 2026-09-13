# The complete Delta3=2 branching formula, with every overlap retained

Ordinary coefficient positivity depends on the finite certificate in
[the positivity proof](gap-two-positivity.md), rather than positivity of individual summands. All parameters below are integers, and t is the stretching variable.

## 1. Entire objects, degree, lattice, and prior reconstruction

Let alpha=(A1,A2,A3,a,b) be strictly decreasing and positive. Let beta=(B1,B2,B3,v1,v2,v3) be weakly decreasing and positive, with equal total. Assume every proper dominance gap is positive and Delta3=2. Write

    g1=A1-A2, g2=A2-A3, g3=A3-a,
    d=A1-B1, e=B3-A3.

Then g1,g2,g3,d>=1, e>=-1,

    B2=A2+d-e-2,
    g1>=2d-e-2, g2>=2e-d+2,                  (1)
    v1+v2+v3=a+b+2, max(v)<=a+1.

The complete fixed-weight GT chain has at most min(r,5) entries in row r, for r=1,...,6, terminal row alpha, prescribed row sums, and every weak interlacing inequality. Its 15 nonterminal coordinates have five disjoint coefficient-one sum equations. Eliminating one coordinate per row gives the saturated affine lattice Z^10. Boundedness follows from interlacing with the terminal shape.

The full nonuniform staircase proof is [the weighted GT interior argument](gap-staircase.md), together with its uniform-height premise. Its translation is delta_i^(r)=r+6-2i, terminal staircase (10,8,6,4,2), and content subtraction (5,5,5,5,5,5). It identifies strict integer chains at grade n with weak chains of top n alpha-(10,8,6,4,2), content n beta-5*1_6. Feasibility is exactly

    n beta6>=5; n b>=2; n(alpha_i-alpha_(i+1))>=2;
    n Delta_k>=k(6-k), 1<=k<=4.               (2)

For sufficiently large n these inequalities hold; add the staircase to a weak chain and divide by n to obtain a full strict real point. Thus the actual dimension is ten, not merely an equation-count bound. The relative-interior count is I(n)=P(-n) by rational reciprocity. Vertex integrality of the GT or conventional hive is not asserted.

At Delta3=2, its own cost is ceil(9/2)=5. Every other cost is at most five except Delta2=1 or Delta4=1, each costing eight. Consequently

    q=8 iff Delta2=1 or Delta4=1;
    q=5 otherwise.                            (3)

Equivalently q=8 iff e=-1 or max(v)=a+1. These statements and the prior degree were established before the scalar counts. They give the full reconstruction space

    P(t)=binom(t+q-1,q-1) R(t), deg R=11-q, R(0)=1.   (4)

Sites 0,...,11-q determine it; 12-q and 13-q are two separate positive holdouts. A negative coefficient of R alone is not an ordinary-negative P.

The entire ordinary LR constructor is

    kappa_j=sum_(i=j)^6 beta_i,
    lambda=(kappa1,...,kappa6),
    mu=(kappa2,...,kappa6), nu=alpha.           (5)

The skew rows lambda/mu are pairwise column-disjoint, of lengths beta_i. Thus their complete skew Schur function is product h_(beta_i); its s_alpha coefficient is K_(alpha,beta). The same identity holds after EVERY nonnegative integral stretch. It proves the complete count identity, with balance |lambda|-|mu|=|alpha|. All beta_i>0 give final trimmed ordinary rank six. Outer size is sum i beta_i. This is not an asserted affine equivalence to a conventional hive, a minimum-rank theorem, or a face embedding. Stretched-LR polynomiality is an explicitly inherited source premise.

## 2. Full 3+3 branching and the exact first-block weight

Restrict a tableau to its entries 1,2,3. Its shape is

    eta=(tA1-u1,tA2-u2,tA3-u3), u_i>=0, |u|=2t.

All these entries are nonnegative since A3>=3. Partition order and dominance over (tB1,tB2,tB3) are together equivalent to m(u)>=0, where

    m(u)=min(g1*t-u1+u2, g2*t-u2+u3,
             d*t-u1, e*t+u3).                  (6)

For a three-row shape eta and sorted three-letter weight w, eliminate the second GT row sum. Its remaining integer coordinate ranges from
max(eta2,w1+w2-eta2,w1,w2) to min(eta1,w1+w2-eta3).
Taking upper-minus-lower differences gives K_(eta,w)=1+min(eta1-eta2,eta2-eta3,eta1-w1,w3-eta3) whenever eta is a partition and dominance holds. Therefore the exact top multiplicity is m(u)+1 on m(u)>=0, and zero otherwise. It must not be replaced by one or an averaged constant before the rest of the count.

For each admitted eta, the remainder is the ENTIRE skew tableau of shape t alpha/eta with tail contents t v. Restriction to the two label sets and union are inverse: labels in the first shape are <=3, and every remaining label is >=4. This is a full bijection, including all column comparisons inside the remainder. Hence

    P(t)=sum_(u>=0, |u|=2t, m(u)>=0)
               (m(u)+1) [x^(t v)] s_(t alpha/eta)(x1,x2,x3).    (7)

## 3. Why exactly three possible new overlap corrections suffice

Let h_n be the complete homogeneous polynomial in the three tail variables, with h_0=1 and h_n=0 for n<0. The skew Jacobi-Trudi matrix has entries h_(t alpha_i-eta_j-i+j), padding eta by zeros. A self-contained justification is the usual path cancellation: expand the determinant into signed systems of north/east paths, with horizontal steps of weight x_k at height k, starting at (eta_j-j,1) and ending at (t alpha_i-i,3). Each entry counts all weak row words of the indicated length. On a system with an intersection, exchange the two tails at its first ordered intersection. This preserves its monomial and reverses the permutation sign, is an involution, and leaves precisely the nonintersecting systems with the ordered endpoints. These are exactly the skew semistandard tableaux. Thus no numerical approximation or omitted permutation is used in the determinant identity.

For j<=3 and i>=j+2, its index is

    u_j-t(A_j-alpha_i)-(i-j)<=2t-2t-2<0.

For an adjacent pair j,j+1 with j<=3, the lower entry is h_(u_j-g_j*t-1). It can be nonzero only if g_j=1 and u_j>=t+1. Since sum u=2t, AT MOST ONE of these three adjacent lower entries can be nonzero. The bottom straight two-row determinant remains fully present. Expanding accordingly gives exactly

    s_(t alpha/eta)=h_u1 h_u2 h_u3 s_(at,bt)
      - 1_(g1=1,u1>t) h_(t+u2+1) h_(u1-t-1) h_u3 s_(at,bt)
      - 1_(g2=1,u2>t) h_u1 h_(t+u3+1) h_(u2-t-1) s_(at,bt)
      - 1_(g3=1,u3>t) h_u1 h_u2 h_(u3-t-1) s_((a+1)t+1,bt).  (8)

The final Schur factor retains BOTH terms of its two-row determinant. In particular the bottom three-cycle is not discarded. The first two substitutions preserve total detached-row size 2t. The last has detached size t-1 and an inhomogeneous compensating shape. Each correction is a count term in a complete signed identity, not a separate ordinary LR stretching family.

## 4. Complete tail content and endpoint formula

For nonnegative w of total (a+b)t, the two-row Schur identity or the same reflection involution gives K_((at, bt), w) as the difference between bounded three-composition counts of totals bt and bt-1. Its inclusion-exclusion is

    sum_(S subset [3]) (-1)^|S| (bt-w(S)-|S|+1)_+,

where z_+=max(z,0). Now put w=t v-gamma with |gamma|=2t. Define

    A={i:vi<=b}, C={i:vi=1}, S={i:vi=b+1},
    J={i:vi=a+1}, p=|A|,
    B=b-sum_(i in A)(b-vi).                     (9)

If any gamma_i>t vi the content is invalid and its count is zero. Otherwise the COMPLETE formula reduces to

    K=1+B*t-sum_(i in A) gamma_i
        -sum_(i in S)(gamma_i-t)_+
        +sum_(k in J)(t-gamma_k-1)_+.             (10)

Indeed a single with vi>=b+2 vanishes because gamma_i<=2t; vi=b+1 retains its hinge. For a pair complementary to k, its argument is (vk-a)t-gamma_k-1. Strict Delta4 says vk<=a+1, so only vk=a+1 can survive, exactly as displayed. The triple term is always zero. Invalid contents need be checked only at vi=1, because every other vi>=2 and gamma_i<=2t. All zero endpoints, including the minus ONE in the pair hinge, are essential.

For u, let N_u(gamma)=[x^gamma] h_u1 h_u2 h_u3. It is the full number of 3-by-3 nonnegative integer matrices with row margins u and column margins gamma. Define

    L_u(t;B)=sum_(|gamma|=2t, gamma_i<=t for i in C)
                     N_u(gamma) * (the expression (10)).      (11)

This finite exact definition counts the leading product in (8), and the same definition counts its first two corrections with their changed row margins. No support has been silently restricted beyond its stated content requirements.

In the last correction, its row lengths v'=(u1,u2,u3-t-1) sum to t-1. Thus every residual content is nonnegative and no single hinge or pair term survives. The remaining expression is 1+Bt-gamma(A). Permuting the three tail letters shows, for these fixed row lengths, that the weighted mean of gamma(A) is p(t-1)/3. Therefore the complete last correction is

    C_u(t;B)=product_(j=1)^3 binom(v'_j+2,2)
                          * (1+B*t-p*(t-1)/3).                (12)

It is used only when u3>t and g3=1. The factorial product is the total number of independent weak row words. Its rational appearance is an exact average, not a separately assumed count factor.

Equations (6)-(12), together with the full partition constructors (5), are an all-parameter, all-stretch entire count formula. [The profile classification](gap-two-profiles.md) exhausts its integer boundary types;
[the positivity proof](gap-two-positivity.md) supplies the exact finite positive coefficient certificate. The target is EVERY ordinary coefficient, not merely a linear term.
