# Complete quotient, exact hinge moments and positive certificates

Claims FR027-P02-T003/C001. All coefficient arrays below are ascending. Finite calculations have complete prior polynomial spaces and separate positive unused checks. The closed quotient formula is an all-grade proof, not a fit.

## 1. Complete saturated nine-dimensional quotient

At y=1 let z_ij>=0, i=1,...,5,j=1,2,3. Columns sum3t; row4 sums4t; row5 sums2t; z51=0. Let ui be the first three row sums, hence |u|=3t. Retain exactly

    5t-u3+sum_(k<j)z3k >= sum_(k<=j)z4k, j=1,2,3,
    sum_(k<j)z4k >= sum_(k<=j)z5k, j=2,3.

These are the full bottom-row SSYT comparisons for(5t,4t,2t)/(5t-u3), with the first two rows detached. The missing lower j=1 condition is precisely z51=0, not a discarded inequality. Union over every u identifies this full polytope count with Q1.

Its integer lattice has nine selected coordinates: the six entries in rows1,2 and z41,z42,z52. The inverse is

    z43=4t-z41-z42, z53=2t-z52, z51=0,
    z31=3t-z11-z21-z41,
    z32=3t-z12-z22-z42-z52,
    z33=-3t-z13-z23+z41+z42+z52.

The inverse is integral; every remaining condition is the original nonnegativity or one of the five displayed inequalities. The polytope is bounded by0<=zij<=3t. At t=6, rows1,2,3 each(2,2,2), row4=(12,8,4), row5=(0,4,8) make every non-forced inequality strict. Therefore its actual dimension is nine and its saturated lattice is Z^9. It is not assigned an ordinary LR rank merely because it is a quotient count.

The independent unsigned counter writes row4=(a,b,c), c=4t-a-b, row5=(0,d,2t-d), with0<=d<=min(2t,a), a+b>=2t. Residual column margins for rows1–3 are

    R1=3t-a, R2=3t-b-d, R3=t-c+d.

Reject negative margins. The third row r=(r1,r2,r3) satisfies0<=ri<=Ri,

    r1+r2+r3<=5t-a, r2+r3<=t+c, r3<=t.

For each r, the first two rows have exactly product_i(Ri-ri+1) fillings. The r1 sum is evaluated by a finite arithmetic sum; the other variables are enumerated completely. At t<=12, each of the nine selected coordinates is at most3t and(3t+1)^9<2^63, so uint64 arithmetic is certified for every nonnegative intermediate sum. This count uses no determinant subtraction.

## 2. All-t closed moment formula

Let

    M(S,t)=sum_(r=t+1)^S (r-t)binom(r+2,2)binom(S-r+5,5).

The unrestricted nine-entry matrix has three entries in one chosen column and six in the other two. Thus M is the COMPLETE first-column hinge moment of all matrices of total S, not a mean substituted inside a nonlinear cap.

Write r=t+1+k. The exact polynomial identity

    (k+1)binom(k+t+3,2)
      =binom(t+1,2)binom(k+1,1)
        +2t binom(k+2,2)+3binom(k+3,3)

and Vandermonde convolution give

    M(S,t)=binom(t+1,2)binom(S-t+6,7)
                  +2t binom(S-t+7,8)+3binom(S-t+8,9).     (1)

Combinatorial binomials with upper index below their lower index are zero. For S=3t and S=2t-1, the displayed generalized-binomial polynomials agree with that convention at every integer t>=0, including the absent negative-total correction at t=0.

The complete tail has three detached h factors and two-row factor s_(4t,2t), minus the lower-overlap term with detached total2t-1 and s_(5t+1,2t). By proof005(3), the weight in either term is1+2t minus its three column hinges. Hence

    R(t)=binom(3t+8,8)-binom(2t+7,8),
    Q1(t)=(1+2t)R(t)-3[M(3t,t)-M(2t-1,t)].              (2)

All caps, all three hinges and the lower overlap are included. Equation(2) proves period-one polynomiality at zero as well; Q1(0)=1 follows from its complete polytope, not an assumption imposed on a positive-grade quotient. The complete parent difference also gives Q1(-1)=Q1(-2)=0. R has a separate saturated Z^8 model: nine nonnegative coordinates of sum3t with one coordinate at mostt. This simple capped-composition positivity is not claimed as a new general cap theorem or as a conventional-hive double-projection isomorphism.

## 3. Explicit positive factor arrays

Define

    A=[20160,127656,411066,816371,1054075,873289,437189,117924,12990],
    B=[20160,126576,359208,579454,547103,293045,81409,9045],
    C=[20160,129096,301698,338711,196117,56233,6305].

Then the complete polynomials are

    P11(t)=(t+1)(t+2)A(t)/40320,
    Q1(t) =(t+1)(t+2)B(t)/40320,
    R(t)  =(t+1)(t+2)C(t)/40320.                         (3)

Every entry is strictly positive. Thus P11,Q1,R have respectively11,10,9 strictly positive ordinary coefficients. Q1 and R follow by exact expansion of(2); P11 is determined in its prior entire-LR degree-ten space as follows. Strict positivity follows from the actual arrays, not positive samples, h-star signs or root stability.

## 4. Complete determination and independent verification

Before any comparison, the full120-permutation skew Jacobi–Trudi expansion was aggregated over every admitted three-letter first-block state with its exact multiplicity. The fresh three-column matrix kernel counts each h-product in arbitrary-precision C++ integers. The preserved roster includes every signed h-term, its target content, bare triple, parameter and source identity. It does not use only the eight-term law under test.

The four parents P01,P02,P11,P12 have actual degree10, constant1 and known roots-1,-2. Values at positive1,...,8 therefore determine their remaining eight parameters. Stretches9,10 were excluded from reconstruction. P11's determining positive counts are

    576,29661,488875,4313655,25644704,116077183,430257807,1368807630.

Its unused checks are3859428925 and9867777282. All determining and holdout counts for all four parents independently agree with the allowlisted unsigned horizontal-strip model, giving44 parent-site agreements. Both are complete whole-count models under the exact tail LR identity. They are different mathematical counting representations and implementations within this originating mission, not external campaign verification.

Q1,H0=(P02-P01)/t and H1=(P12-P11)/t have prior degree at most9 and roots-1,-2. They were reconstructed using1,...,8 and those two negative roots; NO polynomial value at zero was inserted. Stretches9,10 were unused checks. The resulting constants equal1; the closed model separately proves Q1(0)=1. Duality proves H0=Unit1 Q0 and H1=Q1. The latter equality is also reconciled entry by entry, not inferred from a few sites.

The nine-coordinate unsigned quotient model agrees at all11 sites0,...,10 with the full determinant count and the closed expression. Independent Newton divided differences agree with the separate Fraction Lagrange arrays for all seven new raw vectors. The closed moment identity additionally passes169 literal finite-sum checks. Full integer arrays, signed rosters, unused data and code are retained.

One long P12 independent count lost its supervising tool call. Its complete eleven-row output survives, but no successful wait receipt survives. It is not used as if properly reaped. A newly supervised, separately identified full recount supplied all11 agreeing values and an observed exact-PID wait. The old120-second reservation remains quarantined; no mathematical success is substituted for the missing process evidence.
