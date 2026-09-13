# Nonlinear row-column interaction and an entire rank-eight positive family

Root-originated Astra004 attack and repair, 9 September 2026. Independent review complete; see
review/DISPOSITIONS.md. The first negative below is an abstract complete polytope;
the later positive theorem has an explicit entire ordinary LR realization.
Neither establishes a whole-rank theorem or a probability for KTT failure.

## The first correlation that survives

Take a uniformly counted weak composition of an integer `T` into the entries
of a `p` by `q` matrix, with `N=p*q`. Let `R` be the total in a selected
fraction `a` of the rows, and `C` the total in a selected fraction `b` of
the columns. The overlap has `N*a*b` entries. Conditional on every column
total, symmetry gives `average(R)=a*T`, independent of those totals.
Consequently every affine row function has zero covariance with every
column function, and conversely. In particular

```text
average(R*C) = a*b*T^2,
average(R^2) = a^2*T^2 + a*(1-a)*T*(T+N)/(N+1).
```

The first nonlinear interaction has the exact value

```text
Delta = average(R^2*C^2)-average(R^2)*average(C^2)
      = 2*N*a*(1-a)*b*(1-b)
        * T*(T-1)*(T+N)*(T+N+1)
        / ((N+1)^2*(N+2)*(N+3)).                   (1)
```

This is positive at integer `T>=2` but has a negative ordinary linear
coefficient. Pointwise positive correlation is therefore not a coefficient
positivity argument.

For a complete derivation of (1), group the matrix entries into the four
row/column intersection classes, of sizes `N*a*b`, `N*a*(1-b)`,
`N*(1-a)*b` and `N*(1-a)*(1-b)`. If their totals are `X_i`, the exact
factorial-moment identity is

```text
average(product_i falling(X_i,k_i))
 = falling(T,sum k_i) * product_i rising(alpha_i,k_i)
   / rising(N,sum k_i).
```

It follows by differentiating the four factors `(1-z)^(-alpha_i)` and
extracting a coefficient. Expand `(X_11+X_10)^2*(X_11+X_01)^2` into its
nine terms and use `x^j=sum_k Stirling2(j,k)*falling(x,k)`. Subtract the
displayed second moments; clearing denominators gives (1). The frozen
independent algebra checks the full rational identity in `N,a,b,T`, not
just a finite parameter panel. Empty selected groups follow by setting their
factorial moments to zero; the applications here use positive groups.

## A complete negative model, with its LR bridge still missing

For a two-by-two matrix, add two independent intervals of width `g*R` and
two of width `g*C`, where `R` is its first-row total and `C` its first-column
total. At dilation `t` the complete count is

```text
sum(|matrix|=t) (g*R+1)^2*(g*C+1)^2.
```

This is an integral seven-dimensional polytope for positive integer `g`:
four composition coordinates give a three-simplex base and the four complete
affine intervals give four additional dimensions. Its vertices are integral;
the composition lattice and four interval coordinates form a saturated chart.
Applying (1) and the second moments gives

```text
c1 = 11/6 + 2*g + 2*g^2/5 - g^4/105.
```

The complete vector at `g=9` has `c1=-2153/210` and all its other
coefficients positive. At `g=8`, `c1=929/210>0`. The root program preserves
all six complete test vectors and sixty-six literal count comparisons.
This is a new discriminator within the session, not an asserted novel
polytope or an ordinary LR candidate. A valid full LR map is missing.

The construction shows why an explanation based only on zero pair covariance
is insufficient once both sides are nonlinear. It does not prove that rank
eight is the first possible counterexample rank. Even a lower-rank split can
have changing interval bounds or additional cuts that invalidate the affine
argument. Those failures remain separate routes.

## A stronger positive operation for actual simplex counts

Now select half the rows and half the columns, so the four groups have equal
size and `a=b=1/2`. Put

```text
B(x)=binom(x+3,3), K(x)=1+x/2, D(x)=B(x)-K(x),
V(T)=T*(T+N)/(4*(N+1)),
delta(T)=N*T*(T-1)*(T+N)*(T+N+1)
         /(8*(N+1)^2*(N+2)*(N+3)).
```

For `M>=S>=0`, take `T=S*t`, `a0=(M+S/2)*t`, `b0=(M-S/2)*t`.
Conditional symmetry of a half-row total about `T/2` kills its first and
third centered moments even after conditioning on all columns. Thus

```text
average(B(M*t+C)) = B(a0)+V(T)*K(a0),
average(B(M*t-R)) = B(b0)+V(T)*K(b0),
Cov(B(M*t+C),B(M*t-R)) = delta(T)*K(a0)*K(b0).
```

The last equality follows by expanding each cubic about its centered total;
only the two quadratic terms survive the conditional cancellations. The
entire normalized count is consequently

```text
B(a0)*B(b0)
 + V(T)*(D(a0)*K(b0)+D(b0)*K(a0))
 + (2*V(T)+V(T)^2+delta(T))*K(a0)*K(b0).            (2)
```

Every displayed term has nonnegative ordinary coefficients. Indeed
`D(x)=4*x/3+x^2+x^3/6`, while `a0,b0` have nonnegative slopes. The only
negative coefficient of `delta(T)` is its linear one, since

```text
T*(T-1)*(T+N)*(T+N+1)
 = T^4+2*N*T^3+(N^2-N-1)*T^2-N*(N+1)*T.
```

For `N>=2`, the linear coefficient of `2*V+V^2+delta` is

```text
N/(2*(N+1)) - N^2/(8*(N+1)*(N+2)*(N+3)) > 0,
```

and every higher coefficient is nonnegative. This proves (2) coefficientwise.
Multiplication by the positive simplex count `binom(S*t+N-1,N-1)` proves
ordinary positivity of the full two-simplex-fiber operation. The complete
geometric interpretation requires `M>=S`, so both fiber totals stay
nonnegative. This proof does not substitute a polynomial continuation for
negative-width fibers.

## Complete ordinary rank-eight realization

For integers `M>=S>=0`, use

```text
lambda=(50M-S,46M,36M,32M,23M+S,19M,9M,5M),
mu=(27M,23M,19M,15M,13M,9M,5M,M),
nu=(25M,22M,19M,14M,12M,9M,6M,M).
```

For `M>0` this has ordinary rank eight and outer area `220M`. The principal
four-plus-four Horn slack is `S`. Let `y_ij`, `1<=i,j<=4`, be the counts
of the first four labels in the bottom four rows. They are nonnegative and
sum to `S`; write their row and column totals as `r_i,c_j`.

The top four-row LR child has boundaries
`(lambda_top,mu_top,nu_top-c)`, and the bottom child has
`(lambda_bottom,mu_bottom+r,nu_bottom)`. The full row-count construction
in `rank8_simplex_v1.py` gives each child a primitive three-simplex chart.
For any four-row child `(l,m,n)`, with row lengths `a_i=l_i-m_i`, that chart is

```text
X=x32, Y=x42, Z=x31,
L=n1+n2-a1-a2,
row1: a1
row2: a2-n2+X+Y, n2-X-Y
row3: Z, X, a3-X-Z
row4: L-X-Y-Z, Y, n3-a3+X+Z, n4.
```

The complete child domain is `X,Y,Z>=0`, `X+Y+Z<=L`. In this parent its
two totals are exactly

```text
L_top=M+c3+c4, L_bottom=M-r3-r4.
```

For completeness, the root certificate substitutes both child charts and
all sixteen cross entries into **every** original rank-eight tableau
inequality: thirty-six nonnegativity, twenty-eight column and twenty-eight
ballot rows. For each of these ninety-two linear forms, minimize first over
the two three-simplices, then over `sum y=S`. Its minimum is a linear form
in `M-S` and `S`, with both coefficients nonnegative. All ninety-two forms
and minima are serialized. All sixteen row/content identities are checked
exactly. The inverse reads the cross entries and the three selected entries
of each child; deleting one cross coordinate gives the saturated `Z^21`
chart. Thus no extra tableau or missing cross constraint is hidden in the
count identity.

The complete parent polynomial is therefore

```text
P_(M,S)(t)=sum(|y|=S*t)
  binom(M*t+c3+c4+3,3)*binom(M*t-r3-r4+3,3).        (3)
```

Equation (2) at `N=16` proves every ordinary coefficient positive through
actual degree: twenty-one for `S>0`, six for `S=0<M`, and zero at the
origin. The first term in (2) already has positive coefficients through
degree six when `M>0`; the simplex factor supplies the remaining degrees.
The linear coefficient is

```text
c1 = (11/3)*M + (H_15+8/17-16/2907)*S > 0.
```

An independent direct factorial-moment expansion through order six agrees
with (2). Its expansion after `M=(M-S)+S` has 133 positive nonzero mixed
monomials. Sixteen full matrix/simplex counts at four fixed controls agree.
The `M=2,S=2` control is explicitly a dilation of `M=1,S=1`; it is not
independent discovery or a new normalized family. Bare-LR checks are recorded
separately from this all-parameter proof.

## Where to seek a failure next

The abstract negative proves that nonlinear interaction can overcome endpoint
terms. The actual LR family proves a precise opposite rule: the cubic
simplex factors provide enough positive lower-order terms to dominate it.
The simple rank-four cube-block idea is also protected whenever only one
width per block depends on the cross margins, since the remaining factors
are independent and the affine conditional average applies.

A live negative route must change that structure: actual clipped child
polytopes, a different nonlinear child count, or coupling that is not absorbed
by (2). The same bare rank-eight construction remains a legitimate question
outside `M>=S`, where its simple model is no longer proved. Applying (3)
there without all clips would reproduce precisely the old face-versus-parent
mistake. No claim about those whole polynomials is made by this theorem.

## Material repair outside the positive region: retain exactly three cuts

The next test uses the same entire LR construction on `M<=S<=2M`, where its
partitions remain legal. At `M=1,S=2`, an independent exact strict hive point
has all eighty-four rhombus slacks at least `1/12`, proving actual degree
twenty-one before the polynomial attempt. The sixty-second Normaliz attempt
expired without a polynomial; its partial file and cleanup receipt are retained.

The full tableau map still has an exact count description. Examination of
every one of the ninety-two original inequalities shows that all except the
following three are redundant over the two simplex fibers for `S<=2M`:

```text
top:    X+Y >= (S-M)*t-c2,
top:    X+Z >= c4-M*t,
bottom: U+V >= r2-M*t.
```

This statement uses their actual linear minima, not sampled agreement. For
each remaining row the minimum `a*(M-S)+b*S` has `a,b>=0` and `2*b>=a`;
it is consequently nonnegative when `M>=S/2`. The bottom simplex is empty
when `L_bottom=M*t-r3-r4<0`, and that emptiness is retained explicitly.

Let

```text
V(L,k)=k*(k+1)*(3*L+5-2*k)/6,
W(k,l)=l*(l+1)*(3*k-l+1)/6.
```

The first counts the excluded region `X+Y<=k-1` in a three-simplex of total
at most `L`. For two such lower cuts with `k>=l`, their intersection has
count `W(k,l)`, provided its total bound is redundant. Here that bound is
redundant because `k+l-2<=L_top`, as follows from `S<=2M`.
Summing `sum(X=0..l-1) (k-X)*(l-X)` proves the intersection formula.

The exact entire top and bottom child counts are therefore

```text
L_top=M*t+c3+c4,
k=max(0,(S-M)*t-c2), l=max(0,c4-M*t),
top=B(L_top)-V(L_top,k)-V(L_top,l)+W(k,l);

L_bottom=M*t-r3-r4,
h=max(0,r2-M*t),
bottom=0 if L_bottom<0, otherwise B(L_bottom)-V(L_bottom,h).
```

The required inequalities `0<=l<=k<=L_top` and `0<=h<=L_bottom` in the
nonempty bottom case follow from the nonnegative margins and `S<=2M`.
The complete parent count sums their product over all sixteen cross entries
of total `S*t`. This is an all-t count identity on the enlarged domain; it
does not assert a positive ordinary coefficient expansion.

The root implementation independently enumerates the complete three-coordinate
LR child tableaux for every relevant margin. It checks all ninety-two parent
inequalities on every one of the 1,678 reconstructed parent tableaux at the
first outside control. The full outside values at `M=1,S=2`, `t=0,...,4`, are

```text
1, 1678, 236305, 10771720, 250633155.
```

Two other parameter controls are retained, including the protected region
as a calibration. The full twelve-site run, with 604,641 cross-matrix
occurrences and all child checks, took about 3.13 contained algebra seconds.
Those child-tableau operations are internal to the exact count model;
independent external bare-LR oracle requests are accounted separately.
The first two outside values have separately frozen bare-LR checks.

The four-site necessary-positivity functional is positive on the two controls
where it was tested. That is not a coefficient-positive certificate or an
exclusion of negativity. The outside full polynomial remains unknown. The
next bottleneck is exact coefficient extraction from these complete clipped
cubic counts, avoiding enumeration of every sixteen-entry composition at
large stretch. The three concrete cuts and the full LR bridge make this a
specific counterexample route to develop, rather than another abstract face.
