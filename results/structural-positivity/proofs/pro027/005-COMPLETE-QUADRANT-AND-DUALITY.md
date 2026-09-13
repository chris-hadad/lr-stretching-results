# Complete two-parameter LR compensation and determinant duality

This two-parameter construction extends the one-parameter family using the general eight-term branching law. The identities below count entire LR fibers. Coefficient vectors, formal determinant summands, and entire LR objects have distinct mathematical roles.

## 1. Bare family, lattice, degree and codegree

For integers x,y>=0 put

    alpha_xy=(2x+5+2y,x+4+2y,3+2y,2+2y,1+y),
    beta_xy=(x+3+2y,x+3+2y,x+3+2y,y+2,y+2,y+2),
    lambda_xy=(3x+15+9y,2x+12+7y,x+9+5y,6+3y,4+2y,2+y),
    mu_xy=(2x+12+7y,x+9+5y,6+3y,4+2y,2+y), nu_xy=alpha_xy.

Let P_xy(t)=c^(t lambda_xy)_(t mu_xy,t nu_xy), with lambda outer. The shapes are integral partitions, the inner/outer sizes balance, and the outer size is6x+48+27y. The ordinary rank is exactly six. This is a displayed rank, not a minimum-realization theorem.

Lambda is the tail-sum partition of beta and mu its one-position shift. Every row of lambda/mu is column-disjoint from the others, with lengths beta_i. Therefore s_(t lambda/t mu)=product_i h_(t beta_i), and its s_(t alpha) coefficient is exactly K_(t alpha,t beta). The equality includes every tableau at every integer t>=0; it is not a face or an asserted affine equivalence with a conventional hive chart.

Alpha has five strictly decreasing positive parts and beta has six sorted positive parts. The four relevant dominance gaps are(x+2,x+3,3,y+3). The full weighted-GT theorem gives actual degree 10 and its saturated Z^10 counting lattice: the fifteen nonterminal GT entries have five coefficient-one row-sum equations, eliminated integrally. The weighted-GT interior theorem supplies a strict-point argument and exact relative-interior staircase. The codegree is exactly3, since the middle dominance cost is9/3 and every other staircase cost is at most 3. Thus P_xy(0)=1 and P_xy(-1)=P_xy(-2)=0, without a reflection assumption.

The weighted-GT interior argument is given in [Defect two and weighted straight-GT interiors](../../replay/proofs/WEIGHTED-GT-INTERIORS.md), sections 2–3; the complete branching law is given in [Complete gap-three branching with all overlap clusters](001-COMPLETE-GAP3-CLUSTERS.md). External independent verification of the present extension is not claimed.

## 2. An exact involution of whole counts

Pad alpha by a sixth zero and let c=alpha_1=2x+5+2y. The bialternant determinant gives

    (z1*...*z6)^c s_alpha(z1^-1,...,z6^-1)
       =s_(c-alpha6,c-alpha5,...,c-alpha1)(z).

For completeness, this follows by reversing the columns of the alternant with exponents alpha_j+6-j, after replacing z_i by z_i^-1. Reversing the denominator columns introduces the same sign; the remaining common monomial factor is precisely (product z_i)^c. Thus the identity is exact as a Laurent-polynomial identity, not a conjectural symmetry of interpolation data.

The new shape, after trimming, is

    (2x+5+2y,2x+4+y,2x+3,2x+2,x+1)=alpha_yx.

The complementary weight c*1-beta consists of three x+2 entries and three 2x+y+3 entries. Schur symmetry permits exchanging these two equal blocks, giving beta_yx. Scaling the boundaries scales c by t, so

    P_xy(t)=P_yx(t) for every integer x,y,t>=0.              (1)

This uses determinant duality in exactly six variables. It is NOT simultaneous Ferrers conjugation, which does not commute with stretching. In particular the x=0 axis is the already established y=0 family, not an independent new positive-family discovery.

## 3. Complete affine dependence in x, including the sharp initial exception

For u>=0, |u|=3t, let F_y,t(u) be the whole three-letter tail consisting of two detached rows of lengths u1,u2 and the skew bottom shape

    ((3+2y)t,(2+2y)t,(1+y)t)/((3+2y)t-u3),

with content((y+2)t)^3. It includes every cap and lower overlap. Put

    m0(u)=min(t-u1+u2,t-u2+u3,2t-u1,u3),
    Q_y(t)=sum_(|u|=3t) F_y,t(u).

For x>=2, the first two upper gaps are at least 3t and the full state set is admitted. The complete count is sum_(u)(xt+m0(u)+1)F_y,t(u), so it is affine in x. At x=1 the two exact involutions for the one-parameter family still apply. The first leaves u3, hence the entire lower skew factor, unchanged. In the second, both third deficits are<t, so both corresponding lower upper-overlaps are absent and the common lower factor is s_((2+2y)t,(1+y)t). Their weights and all other factors pair exactly. The two negative extended-state regions are disjoint; their zero-weight first layers contribute zero. The complete determinant corrections, not a truncated diagonal sum, therefore give

    P_xy=P_1y+(x-1)t Q_y,  x>=1,y>=0.                     (2)

The general-width version in [A complete homogeneous rank-six cone with forty positive joint coefficients](007-HOMOGENEOUS-CONE-AND-BOUNDARIES.md) proves this without assuming x-1 is an integer multiple of the base gap. At x=0 a separate wall is necessary; [Negative initial walls and an explicit positive finite-difference basis](008-INITIAL-WALLS-AND-POSITIVE-DIFFERENCES.md) gives its complete correction. Thus no conclusion is drawn from extending(2) to x=0.

## 4. Complete affine dependence in y

Take y>=1. In every active block of the eight-term determinant, the detached three-row total S is at most 3t, and the remaining two-row shape has smaller row D=(y+1)t. For a three-by-three detached matrix with column sums gamma, the residual weight is

    w_i=(y+2)t-gamma_i >=0.

The complete bounded-composition formula for the two-row Kostka number gives

    K_((C,D),w)=sum_(J subset [3])(-1)^|J|
                         (D-w(J)-|J|+1)_+.

All pair-subset terms vanish because their arguments are

    gamma_i+gamma_j-(y+3)t-1 <= -yt-1 <0.

The triple-subset term also vanishes. The singleton terms are(gamma_i-t)_+. Therefore, on each complete size-matched term,

    K_((C,D),w)=1+(y+1)t-sum_i(gamma_i-t)_+.              (3)

The bottom second-subdiagonal determinant entry has index
u3-(y+2)t-2<0 and vanishes for every state. The other seven terms, including all upper cycles and intersecting overlaps on x=0, are retained. Their indices and top multiplicities are independent of y. Hence the complete P_xy is affine in y for every x>=0 and y>=1. This assertion is stronger than detachment of the first two rows and does not omit the x=0 interactions.

In the detached tail, its y-slope is tG(u), where

    G(u)=prod_i binom(ui+2,2)
       -1_(u3>=t+1)binom(u1+2,2)binom(u2+2,2)
                                      binom(u3-t+1,2).

Summing over u and using the generating function(1-z)^-9 gives

    R(t)=sum_u G(u)=binom(3t+8,8)-binom(2t+7,8),
    Q_y=Q_1+(y-1)tR.                                    (4)

This retains the entire lower overlap; dropping its second binomial would give a different mixed coefficient.

## 5. The whole quadrant law and axes

By(1), P_12=P_21; by(2), P_21-P_11=tQ_1. Thus the y-slope at x=1 equals the x-slope exactly, not just at sampled sites. Combining(2)–(4),

    P_xy=P_11+(x+y-2)tQ_1+(x-1)(y-1)t^2R,
                               x,y>=1.                  (5)

Write P00,P10,Q0 for the one-parameter family's P0,P1,Q. The entire remaining boundary is

    P_x0=P10+(x-1)tQ0, x>=1;
    P_0y=P10+(y-1)tQ0, y>=1;
    P_00=P00.                                           (6)

[Complete quotient, exact hinge moments and positive certificates](006-QUOTIENT-MOMENTS-AND-POSITIVE-CERTIFICATE.md) supplies positive P11,Q1,R certificates; the one-parameter family supplies positive P00,P10,Q0. Hence ALL eleven ordinary coefficients of EVERY integer-quadrant member are strictly positive, including both initial axes and the corner. [Negative initial walls and an explicit positive finite-difference basis](008-INITIAL-WALLS-AND-POSITIVE-DIFFERENCES.md) further gives coefficientwise monotonicity and supermodularity. [A complete homogeneous rank-six cone with forty positive joint coefficients](007-HOMOGENEOUS-CONE-AND-BOUNDARIES.md) gives a genuinely homogeneous three-parameter cone with all its dimension-drop boundaries.

The theorem does not establish positivity of all strict gap-three profiles, all rank six, or full KTT. All members in(5) have outer size at least 81, and the original displayed quadrant has size at least 48. This yields no additional cases in the original area-thirty domain.
