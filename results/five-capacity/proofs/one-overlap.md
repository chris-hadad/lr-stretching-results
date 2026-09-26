# A complete one-overlap chamber and its whole polynomial

Accepted Astra009 derivation, retained here as a mathematical dependency. Classical ingredients are the Pieri rule, Schur scalar-product adjunction, and the full one-overlap Jacobi-Trudi identity established in Astra008. No novelty claim is made.

Let m>=1, h,c,d,u,v and w_1,...,w_m be nonnegative integers with

    0<=c<=h, d>=0, u,v>=h+d, and every w_i>=c+d.

Set U=u+v and s=sum_i w_i. Require s>=c+d. For nontrivial shared columns take h>0; the h=0,c=0 boundary is included if the partitions below are valid. Set

    alpha=(U+s-h-d-c, h+d, c).

The entire skew shape consists of a top adjacent pair of row lengths u,v sharing h columns, followed by m column-disjoint rows of lengths w_i. A concrete ordinary LR triple is

    lambda=(s+U-h, s+v, suffix_1(w),...,suffix_m(w)),
    mu=(s+v-h, s, suffix_2(w),...,suffix_m(w),0),
    nu=alpha,

with trailing zeros removed. These are partitions: u,v>=h+d>=h, and the suffix rows are decreasing. Balance is immediate. Also alpha is dominant since U>=2h+2d and s>=c+d, and c<=h+d. Zero rows may be retained as formal empty rows.

The claimed full ordinary polynomial, in the ORIGINAL integer stretch, is

    P(t)=binom(c t+m-1,m-1) binom(d t+m,m).                 (1)

For m=1 the first factor is one, including c=0. If c=d=0 the count is one. The formula is a product of polynomial binomials with nonnegative ordinary coefficients. When m>=2,c>0,d>0 it has actual degree 2m-1 and strictly positive coefficients in every degree through it. When a parameter is zero, retain the actual degree drop.

## Complete proof

By the two-row Pieri rule, the full pair character is exactly

    h_(ut) h_(vt)-h_((U-h)t+1) h_(ht-1)
      = sum_(k=ht)^min(ut,vt) s_(Ut-k,k).                 (2)

At h=0 the subtracted h_(-1) is zero. Equation (2) also includes t=0. This telescopes the two full Pieri expansions; no affine shift is discarded.

To extract s_(t alpha) after multiplying by the remaining h_(w_i t), a channel beta=(Ut-k,k) must fit inside t alpha. In particular k<=alpha_2 t=(h+d)t. The hypotheses u,v>=h+d make every k=ht+j with 0<=j<=dt available in (2). Every such beta fits: its first row is (U-h)t-j, and the difference from alpha_1 t is (s-d-c)t+j>=0.

For this channel the scalar product is the weight multiplicity

    <s_(t alpha/beta), product_i h_(w_i t)>.

The skew shape t alpha/beta has row lengths

    (s-d-c)t+j, dt-j, ct.

They share no columns. The start of its top row lies strictly after beta_1=(U-h)t-j, and beta_1>=alpha_2 t follows from U>=2h+2d and j<=dt. The second row starts strictly after beta_2=ht+j>=ct, so it is disjoint from the third. Empty rows cause no exception. Its whole character is therefore the product of the three homogeneous characters of those row lengths.

Its weight multiplicity is the number of nonnegative integers x_i,y_i,z_i with

    x_i+y_i+z_i=w_i t,
    sum z_i=ct, sum y_i=dt-j.

Summing all channels j=0,...,dt is a bijection with all y,z satisfying

    sum z_i=ct, sum y_i<=dt, y_i+z_i<=w_i t.               (3)

The last inequalities are automatic under w_i>=c+d, because each y_i+z_i<=sum y+sum z<=(c+d)t. The z coordinates give binom(ct+m-1,m-1) possibilities. The y coordinates together with the unique slack j=dt-sum y give binom(dt+m,m) possibilities. This proves (1) as a full count at every nonnegative integer t. Every map is integral and preserves t; no face count or partial sum is substituted for the whole LR polynomial.

## Stronger exact reduction without the capacity floor

If the w_i are arbitrary nonnegative integers with s>=c+d, while u,v>=h+d and 0<=c<=h, the same proof gives (3) with its original capacities. Thus the ENTIRE LR family is the lattice count of two nonnegative m-vectors with one fixed total, one bounded total, and coupled coordinate capacities. Formula (1) is asserted only when every capacity floor holds. Removing capacities outside that domain changes the whole count and is not a positivity argument.

At d=0 this exact reduction is a complete 2-by-m transportation fiber: z_i+x_i=w_i t and sum z_i=ct. Its c1 follows from the previously accepted whole transportation theorem at its stated domain, with point/empty reductions retained. Higher signs outside the binomial subchamber do not follow from that linear theorem.
