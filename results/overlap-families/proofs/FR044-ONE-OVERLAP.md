# Independent adoption: complete one-overlap three-letter parents

Curated mathematical proof from **FR044**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

26 September 2026. Root rederived the complete
original-character count and paired-product argument from the captured U11
proofs. Pro044 is the source of the new coupled-branch/overlap-operation
argument; A008 owns the full pair character and A009 the earlier product
branch. Classical Pieri and the original LR rule are mathematical premises.

## Exact domain and original object

Let m>=1, d=m-1, integer b>=c>=1, 0<=h<=b, u,v>=b, and each w_i>=b+c-h.
Write s=sum(w_i), T=u+v+s, and sigma_i=sum_{j>=i}w_j. Define


```text
lambda=(s+u+v-h, s+v, sigma_1,...,sigma_m),
mu=(s+v-h, s, sigma_2,...,sigma_m,0),
nu=(T-b-c,b,c).
```

These are partitions: the first lambda inequality is u>=h, the first mu
inequality is v>=h, and the remaining ones are immediate from positive widths.
They are balanced; nu_1>=2b-h>=b. The skew rows have lengths u,v,w_1,...,w_m,
with exactly h columns shared by the first pair and no other shared column.
Consequently their whole skew character, at grade t>=1, is


```text
(h_(ut) h_(vt)-h_((u+v-h)t+1) h_(ht-1)) product_i h_(w_i t).
```

The affine shifts are once only. For h=0 the second term is zero. Pieri makes
the pair precisely the sum of s_((u+v)t-j,j) over ht<=j<=min(ut,vt).
To contribute to t nu, exactly ht<=j<=bt are admissible. Necessity follows
from the second row of t nu; sufficiency uses u,v>=b and s>=b+c-h.
The channel's first row is at least bt, making the residual top row disjoint
from its two lower rows. Its residual lower character is the full difference
h_(bt-j)h_(ct)-h_(bt+1)h_(ct-j-1), with the second term absent for j>=ct.

Adjunction now counts assignments of those two lower rows to m labels.
For either term the combined lower total is (b+c)t-j<= (b+c-h)t<=w_i t.
Thus every individual capacity is redundant. The top multiplicity is exactly
the remaining content for that label and is automatically nonnegative.
This argument removes no sign partner or admissible integer assignment.
The two complete sums are


```text
sum_{j=ht}^{bt} C(bt-j+m-1,m-1) C(ct+m-1,m-1)
-sum_{j=ht}^{ct-1} C(bt+m,m-1) C(ct-j+m-2,m-1).
```

Hockey-stick summation gives, for h<=c,


```text
P_h(t)=C((b-h)t+m,m) C(ct+m-1,m-1)
        -C(bt+m,m-1) C((c-h)t+m-1,m).
```

For c<=h<=b the subtracted count is zero; at h=c its polynomial is identically
zero too. Continuing it with negative slope at h>c would be invalid.
This proves equality at every positive integer grade in the actual tableau
lattice, and hence the polynomial identity, without interpolation or a changed
lattice residue. The polynomial constant is one and equals the empty filling
at t=0. If h>b while h<=min(u,v), no channel fits, so the positive-stretch
family instead has the zero polynomial. That separate empty convention is not
inferred from the value of the all-empty grade-zero tableau.

## Full positive certificate and actual degree

For h<=c put X=b-h, Y=c-h, H=h, L=b-c; thus X=Y+L>=Y>=0. Let


```text
T_j=(Xt+j)(ct+j-1), S_j=(bt+j)(Yt+j-1), 2<=j<=d+1.
```

Multiplying P by Z=(d+1)!d! gives


```text
Z P=(Xt+1) product T_j-Yt product S_j
   =(Lt+1) product T_j+Yt (product T_j-product S_j).
```

Direct expansion gives T_j-S_j=Ht(Lt+1). For a fixed ordering,


```text
product T-product S=sum_j (T_j-S_j) product_{i<j}S_i product_{i>j}T_i.
```

Every factor is ordinary-coefficient nonnegative, including all boundary
values. This is a uniform finite identity for arbitrary m, not an extrapolated
panel. At h>=c, the original product formula has nonnegative factors directly.
When b>c and h<b the leading positive product has all coefficients positive
through 2d+1; when b=c and h<b the degree is 2d and every coefficient is
positive; h=b gives C(ct+d,d), of degree d. This also proves actual degree
and strictness at d=0, including point cases.

## Whole-parent overlap reduction

Hold rows and output fixed. For 0<=h_1<=h_2<=b, require w_i>=b+c-h_1, so
all intermediate original triples remain in the domain. In the coupled branch,
differentiate toward decreasing h with b,c fixed. Relabel j=1,...,d so that
T_j=(Xt+j+1)(ct+j), S_j=(bt+j+1)(Yt+j). The derivative of ZP divided by t is


```text
product T-product S
+sum_j ((Xt+1)(ct+j) product_{i!=j}T_i
         -Yt(bt+j+1) product_{i!=j}S_i).
```

Each distinguished-front difference is


```text
(Xt+1)(ct+j)-Yt(bt+j+1)=LHt^2+(Lj+H)t+j.
```

Split each bracket into this nonnegative difference times product T and
Yt(bt+j+1) times the omitted-product difference. The same telescoping proof
signs every bracket. For h>=c, differentiating the first positive binomial
product in the decreasing-h direction is a sum of nonnegative products.
Both polynomial fields coincide at h=c; coefficientwise integration includes
the interface and yields P_(h1)-P_(h2)>=0. The displayed rational polynomial
fields themselves justify real differentiation; only integral parameter points
are called original triples. Starting at h=b, whose complete polynomial is
C(ct+d,d), successive unit reductions give a finite paid operation. Strict
gain is not asserted on constant branches.

## Quantified failed extension

The uncapped formula cannot be used after omitting its capacity hypotheses.
For lambda=(7,6,4,2), mu=(5,4,2,0), nu=(3,3,2), the original values at t=1..4
are 3,6,10,15. The inadmissible formula with m=2,b=3,c=2,h=1 instead gives 13
at t=1. This is an incorrect formula outside its domain, not an LR negative.
A further exact whole-branch obstruction has
lambda=(6,4,2), mu=(4,2,0), nu=(4,1,1): the whole family is one while its
H11 branch is -t+t^2/2+t^3/2. The four Weyl partners must remain coupled.

## Evidence and boundary

Fresh root script verify.py uses exact rational polynomial arithmetic and an
independently written literal LR-tableau row enumerator: weak rows, strict
original overlapping columns and the right-to-left lattice-word condition.
It imports no returned program. INDEPENDENT-CHECKS.json records 1,344 exact
polynomials, 15,582 ordinary coefficient slots, 1,092 overlap comparisons,
and 101 original grade counts, including point, empty and floor-omission
controls. The uniform proof above supplies the all-rank quantifiers; these
checks are error controls. No census, new whole-rank theorem, generic
three-row-inner theorem, arbitrary-capacity theorem or KTT conclusion follows.
