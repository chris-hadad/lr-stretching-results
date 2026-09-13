# All ordinary coefficients in a complete unequal-weight two-row LR channel

All formulas apply to the entire LR count. The earlier central two-row theorem concerns the uniform shape (W/2,W/2); the present shape is (W-2,2) with n>=5, so W>=5 and it is a different component. The previously established rank 7 uniform (5,2) example is included as an overlap. Worldwide novelty is not claimed.

## 1. Bare triple, complete character and actual lattice

Let n>=5 and let w=(w1,...,wn) be arbitrary positive integers, in their given order. Put W=sum w_i and let u be the number of entries equal to one. Define

    lambda_i=sum_(j=i)^n w_j, 1<=i<=n;
    mu=(lambda_2,...,lambda_n);
    nu=(W-2,2), lambda outer.

Both lambda and mu are strictly decreasing positive partitions; nu is a positive strict partition since W>=5. The skew row lengths are exactly w_i and the rows are column-disjoint. The sizes satisfy |lambda|-|mu|=W=|nu|; outer size is sum_i i*w_i. Lambda has exactly n positive parts, so ordinary rank is n. This is not a minimum-rank or minimum-size claim.

At stretch t, the entire skew character is product_i h_(tw_i). The coefficient of s_((W-2)t,2t) is the complete Kostka count, hence the entire ordinary LR coefficient. In two variables, multiplying this product by 1-z and extracting the coefficient of the second-row degree gives

    P_(n,u)(t)=[z^(2t)](1-z) prod_i(1+z+...+z^(tw_i)). (1)

To see that the determinant extraction selects exactly this Schur component, a two-variable Schur polynomial of shape (a,b), a>=b, is (xy)^b sum_(j=0)^(a-b)x^(a-b-j)y^j. Its coefficient of y^k minus that of y^(k-1), with the first exponent complementary to total degree, is one for b=k and zero for every other b<=k. Here k=2t is on the lower half of the total. This proves (1), including both determinant terms and every content cap.

The complete GT chain has row totals tW_k, W_k=sum_(i<=k)w_i, and bottom entries a_k. Its exact saturated chart is

    a1=0, an=2t,
    a_k <= a_(k+1),
    a_(k+1) <= a_k+t*w_(k+1),
    a_k+a_(k+1) <= tW_k,                  1<=k<n.     (2)

The first row entry at level k is tW_k-a_k. Thus (2) gives both the full integer inverse and every interlacing inequality. Free coordinates are a2,...,a_(n-1), with lattice Z^(n-2). No congruence or unrecorded support restriction occurs.

## 2. Prior degree and true interiors, including both parities

All nontrivial inequalities in (2) can be strict. At n=2m+1 choose t=m and a_k=k-1. At n=2m choose t=m and let the n-1 successive increments a_(k+1)-a_k be one except for one increment equal to two. Each construction is strictly feasible for every positive weight: for odd n, m>=2; for even n, m>=3. The increment bound is strict because m*w_i>=2 in the first case and >=3 in the second. For the third inequalities, use W_k>=k; at even n the k=1 inequality is checked separately by a2<=2<=m*w1-1, while k>=2 gives a_k+a_(k+1)<=2k+1<=mk-1. Odd n gives a_k+a_(k+1)=2k-1<mk. These are complete strict points in the n-2 free coordinates, proving actual dimension

    d=n-2

before any numerical reconstruction. True relative-interior integer points satisfy the three inequalities with strict integer slack. In particular their n-1 successive bottom increments are at least one, so 2t>=n-1. The constructions just given attain the bound. Hence true codegree is

    q=ceil((n-1)/2)=floor(n/2).                       (3)

At first grade, the odd case has exactly one possible increment sequence, and the even case exactly n-1. All are strictly feasible as above. Therefore I(q)=1 for odd n and I(q)=n-1 for even n. These are actual lattice-interior statements, not roots guessed from a fit. The strict GT implementation independently checks them.

## 3. Complete cap contraction

In (1), each cap of weight at least two starts at tw_i+1>2t and cannot occur. A unit cap starts at t+1. Two unit caps would require 2t+2>2t, so no pair intersection is present at ANY nonnegative stretch. Expanding all numerator factors thus gives exactly

    P_(n,u)(t)=binom(2t+d,d)-u binom(t+d-1,d).        (4)

The second binomial vanishes at t=0, so the zero grade is one. This is not a large-t expression or a truncation by observed zeros. All omitted terms have strictly negative extraction degree at every stretch. At t=1 it gives binom(n,2)-u>0, so the family is nonempty.

For fixed n, the polynomial depends only on u, not on the magnitudes or positions of weights >=2. All n+1 values u=0,...,n are realized and are distinct already at t=1. Consequently this is an unbounded-rank family with exactly n+1 polynomial values at each fixed n; arbitrarily large weights at fixed n do not create infinitely many new polynomials.

The full negative cap block is -u*C_d(t), C_d=binom(t+d-1,d). For u>0 every ordinary coefficient of that auxiliary block in degrees 1..d is negative. It is retained in (4), with zero constant, and is not an entire LR counterexample.

## 4. A coefficientwise lower bound, not positive-sample inference

Write B_d(t)=binom(t+d,d), C_d(t)=binom(t+d-1,d), and let b_j,c_j be their coefficients. Then c0=0, b0=1, and c_j>0 for1<=j<=d. From B_d=(t+d)C_d/t,

    b_j=c_j+d*c_(j+1).

Set a_i=1/i, 1<=i<=d-1, and write e_j for the elementary symmetric sums of these d-1 positive numbers. Then c_j=e_(j-1)/d. Counting each j-element product j times gives

    j e_j=sum_(|S|=j-1) (prod_(i in S)a_i)
                         sum_(i notin S)a_i
          >= (d-j)/(d-1) e_(j-1).

This also holds at j=d with e_d=0. Therefore

    b_j/c_j >= 1+d(d-j)/(j(d-1)) >= d/j.

Since 2^j>=2j for every integer j>=1,

    [t^j]B_d(2t) >= 2d [t^j]C_d(t).

The complete polynomial

    E_d(t)=B_d(2t)-1-2d C_d(t)

is thus ordinary-nonnegative, with zero constant. Keeping the full subtraction in (4) yields the EXACT positive decomposition

    P_(n,u)=1+E_d+(2d-u)C_d,
    P_(n,u) >=_coeff 1+(2d-u)C_d
              >=_coeff 1+(n-4)C_d.                 (5)

Here 2d-u>=2n-4-n=n-4>0. Hence every coefficient through actual degree d is strictly positive. The leading coefficient is (2^d-u)/d!>0, consistent with the independent dimension argument. The linear coefficient is exactly

    c1=2H_d-u/d.

The proof controls the whole negative cap block by an explicit coefficient-positive remainder. It does not invoke root stability, nonnegative h-star for general hives, or a positive-summation principle.

## 5. Exact evidence and applicability

The formula calculation records 91 complete raw coefficient vectors before the independent comparisons: every u at n5..12 and three u values at each of n16,25,40,65,101. All 1338 ordinary entries are positive. The GT calculation obtains all 1520 full GT scalar values in their prior degree spaces, including 182 unused positive checks. Integer Newton reconstruction from the determining sites reproduces every coefficient; 874 direct strict-interior sites verify reciprocity, codegree and first-interior type. The largest saved rank is101, actual degree 99; the largest saved outer size is 25549. The all-parameter theorem is the proof above, not extrapolation from this finite set.

Literal LR enumeration adds20 literal bare LR counts for five unequal-weight triples, in addition to its 17 separate source-sink checks. Its implementation uses full row reading-word ballot and column inequalities, not the specialized GT count. The n7,(5,2) example and the rank<=5 cases retain their previously established positivity. No additional coverage of the original bounded domain or whole-rank/full-KTT theorem follows.
