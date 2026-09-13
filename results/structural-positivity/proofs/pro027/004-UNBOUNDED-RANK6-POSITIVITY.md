# An unbounded rank-six LR family with exact complete compensation

Claim FR027-P01-T004. Every ordinary coefficient through degree ten is strictly positive for every integer x>=0 in the following entire LR family. This is a new originating mission theorem supported by two complete counting models and exact arithmetic. It is not a claim of independent campaign acceptance, worldwide novelty, all rank-six positivity, or closure of every gap-three family.

## Bare partitions and whole-object premises

Set

lambda_x=(3x+15,2x+12,x+9,6,4,2),
mu_x=(2x+12,x+9,6,4,2),
nu_x=(2x+5,x+4,3,2,1),
P_x(t)=c^(t lambda_x)_(t mu_x,t nu_x), lambda outer.

All parts are nonnegative integral partitions; lambda and nu are strictly decreasing after zero padding. The sizes are6x+48,3x+33,3x+15, respectively. Thus the bare triple is balanced, has ordinary rank six, and lies outside the original area-thirty box for every x>=0. No lower-rank realization or size minimality is claimed.

Let alpha_x=nu_x and beta_x=(x+3,x+3,x+3,2,2,2). Lambda and mu are its complete tail lift. The column-disjoint-row Schur identity proves P_x(t)=K_(t alpha_x,t beta_x) for every t>=0. The strict weighted-GT theorem gives a saturated Z^10 counting lattice and actual degree ten; its dominance gaps are(x+2,x+3,3,3), and its shape gaps are(x+1,x+1,1,1). The exact staircase formula gives true codegree three. In particular P_x(-1)=P_x(-2)=0 and P_x(0)=1. No reflection or unique-interior assumption is used.

For direct source references, see proof001 and the fully retained Phase0 source application HISTORY/P00-A02/NOTES/GAP3-ANCHOR-PREMISES.md. Every source/input digest is in SOURCES/INDEX.json and the individual job launch records. The actual GT lattice, not an unproved ordinary-hive coordinate map, is the counted model.

## The complete affine completion

Let F_t(u), |u|=3t, be the complete tail count with two detached rows of lengths u1,u2 and the bottom skew shape(3t,2t,t)/(3t-u3), with total tail content(2t,2t,2t). It includes all lower overlaps and all caps. Put

m0(u)=min(t-u1+u2,t-u2+u3,2t-u1,u3),
Q(t)=sum_(u>=0, |u|=3t) F_t(u).

For x>=2, m0>=-2t, so the complete top multiplicity is xt+m0+1 on the entire deficit simplex. The two upper shape gaps are(x+1)t>=3t, so those two rows are detached; the tail F is independent of x. Therefore, at every nonnegative integer stretch,

P_x(t)=P_2(t)+(x-2)t Q(t), x>=2.

The complete nine-dimensional homogeneous saturated lattice model for Q, including Q(0)=1 and its period collapse, is given in proof002. This premise was established before using its zero grade in interpolation. A positive-grade identity alone would not justify that step. Q is not assigned an ordinary LR rank: its role here is the complete quotient count in the actual parent formula.

The threshold improves to x>=1 by exact cancellation, not by extrapolation. Proof003 supplies two explicit involutions pairing negative weights in the formal extended first-block sum with the two subtracted upper-overlap determinant terms. The excluded zero-weight first layers contribute zero; deeper excluded weights are the negatives of their paired admitted overlap weights. All lower-tail factors agree. Consequently

P_1=P_2-tQ,
P_x=P_1+(x-1)tQ for EVERY integer x>=1.                 (1)

This is an all-stretch identity. It exhibits a complete compensation mechanism that a positive-pieces argument would miss: negative weights created by extending a chamber are exactly canceled by whole determinant corrections.

## Exact positive certificates

Let A0,A1,B denote polynomials specified by their ascending integer coefficient arrays:

A0=[20160,80856,168078,225141,203951,125298,50372,11937,1247],
A1=[20160,103896,273390,447917,480307,337610,149764,37649,4027],
B =[3360,13296,23590,23081,12975,3871,467].

The complete exact polynomials are

P_0(t)=(t+1)(t+2) A0(t)/40320,
P_1(t)=(t+1)(t+2) A1(t)/40320,
Q(t)=(t+1)^2(t+2) B(t)/6720.                           (2)

Every entry in the three arrays is strictly positive. Hence every coefficient of P0 and P1 is strictly positive, and every coefficient of Q is strictly positive. Equation(1) proves strict positivity of all eleven coefficients of P_x for every integer x>=1. Together with P0, this proves the entire x>=0 theorem. The family has unbounded outer size and is not a common-dilation orbit: for example its constant tail boundary parts remain fixed while the first parts change.

In particular c1(P0)=1543/280, c1(P1)=1863/280, and c1(P_x)=1863/280+(x-1) for x>=1. Full raw vectors, including determining data and prior premises, are in DATA/*-vector-raw.json. Positivity of the factorizations is an exact coefficient argument, not root stability or a positive-sample inference.

## Determination, unused checks and independent models

The degree-ten parent space was fixed in advance by the strict GT theorem. Known values at-2,-1,0 are0,0,1. Positive stretches1,...,8 determine the remaining eight parameters;9 and10 are unused checks. P0 determining counts are

132,4464,62416,507129,2873484,12611191,45762804,143364852.

Its unused checks are P0(9)=399564748 and P0(10)=1012438977. P1's checks are1245276208 and3169029237; P2's are2100846088 and5350111107; P3's are2956415968 and7531192977.

For Q, actual degree nine, Q(0)=1 and roots-1,-2 were proved before fitting. Values at-2,-1,0,...,7 determine it. Q(8)=38071053 and Q(9)=95063320 are unused checks; Q(10)=218108187 is extra. Its complete sequence at0,...,10 is

1,144,3591,38224,247980,1164294,4352992,13742064,38071053,95063320,218108187.

Two complete models agree at all44 parent sites x=0,1,2,3 and t=0,...,10: (a) full signed Jacobi–Trudi/three-column matrix counts in fresh C++ exact integers, and (b) the allowlisted canonical unsigned horizontal-strip tableau count in Python integers. Independent direct enumeration of the nine-dimensional row lattice agrees at all11 Q sites. Exact Fraction Lagrange and separately implemented Newton reconstruction agree. Sixteen additional literal ordinary-LR reading-word counts at x=0,...,3, t=0,...,3 agree; they are low-stretch bridge checks, not separately computed bare-LR full vectors. All determining and reserved counts, roster identities and complete source versions survive in the checkpoint.

The symbolic eight-term proof was challenged against all120 determinant permutations, and the sharp-threshold involutions were checked on1378 paired states in each of the two regions through t=25, including338 excluded zero-weight states. No original source vector was used as a favorable comparison before preserving a new raw vector. Scientific independence here means different complete counting representations and implementations within this originating unit; independent external campaign review remains unclaimed.

## The initial boundary is different, and its correction is ordinary-negative

The affine formula does not extend to x=0. Define the complete auxiliary polynomial W0=P0-P1+tQ. Exact subtraction gives

W0=t(t-1)(t+1)^2(t+2)(t+3)(t+4)(t+5)(11t^2+26t+24)/20160. (3)

Its ordinary coefficients in degrees1,2,3,4 are respectively

-1/7, -101/210, -2741/5040, -151/2520.

Every observation was saved at auxiliary scope in NEGATIVE-AUXILIARIES.jsonl and DATA/wall-vector-raw.json before subsequent favorable reconciliation. W0 is not an entire LR polynomial and is not a candidate. It vanishes at t=0,1 and is positive at every integer t>=2. Thus positive count differences themselves do not establish ordinary positivity.

At t=2 the putative extension gives P1(2)-2Q(2)=11556-7182=4374, whereas the complete P0(2)=4464; W0(2)=90. Threshold1 in(1) is therefore sharp among allowed integer x. The actual complete initial parent P0 remains strictly ordinary-positive by(2). This challenge preserves a negative auxiliary mechanism while showing exactly why it does not become a negative entire parent in this family.

## Protected terminals and limits

For x=0,1,2,3,4,10 the checked Cdagger and Csplit sufficient recognizers refuse both inner orders, and the checked multiplicity-one proper Horn factorization routine finds no terminal equality. These exact finite domain results are recorded, not promoted to nonmembership in every positive model. Actual dimension ten and codegree three independently exclude lower-dimensional and high-codegree terminals. Rank-at-most-five positivity and the original area-thirty closures do not cover these displayed triples. The gap-one/gap-two theorems do not apply because Delta3=3.

The result does not classify all strict gap-three profiles, all rank six, arbitrary higher rank, or full KTT. Candidate count is zero and frozen additive original-box coverage remains4554. The next useful extension varies genuine tail margins while retaining every cap and initial wall, as proposed in NOTES/TWO-PARAMETER-NEXT.md; its new coefficient signs are not supplied here.
