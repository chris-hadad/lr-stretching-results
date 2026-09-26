# Complete five-height factorization and projection

## Original hive, boundary and row labels

Let lambda, mu and nu be weakly decreasing nonnegative integral partitions,
padded to length six, with |lambda|=|mu|+|nu|. Lambda is outer. Write h[i,j]
for 0<=i<=j<=6. At grade t the boundary is

    h[0,j] = t sum_(k=1)^j mu_k,
    h[j,j] = t sum_(k=1)^j lambda_k,
    h[i,6] = t (|mu| + sum_(k=1)^i nu_k).

There are ten free integral heights. The original 45 rows, in the order used
below, are the following expressions, each constrained to be nonnegative:

    h[i,j]+h[i+1,j+1]-h[i+1,j]-h[i,j+1],
        i=0,...,5, j=i+1,...,5;
    h[i,j+1]+h[i+1,j+1]-h[i,j]-h[i+1,j+2],
        i=0,...,4, j=i,...,4;
    h[i+1,j]+h[i+1,j+1]-h[i,j]-h[i+2,j+1],
        i=0,...,5, j=i+1,...,5.

Within each block i precedes j. Thus row labels are zero-based 0 through 44.
Substituting the boundary writes each row as beta_r + N_r.h at grade one;
at grade t replace beta_r by t beta_r. This defines every beta in the formulas
without a hidden table or choice of numerical boundary. Integral points of this
whole hive are counted by the original LR coefficient. Coordinate projection
and insertion below use this literal saturated integer lattice.

## 2. Exact original coordinates and the row partition

Write the original ten heights as

    (a,b,c,d,e,f,g,h,i,j)
       =(h12,h13,h14,h15,h23,h24,h25,h34,h35,h45).

Let the original row, with the zero-based label above, be

    ell_r = beta_r(boundary) + N_r . (a,b,c,d,e,f,g,h,i,j) >= 0.

At grade `t`, evaluate the **original** boundary at `t boundary`; equivalently
replace each `beta_r` below by `t beta_r(boundary)`. Heights remain the original
integer heights, not differences or a nonsaturated quotient. Lambda is outer;
all partition and trace conditions remain original legality premises.

The complete disjoint row assignment is:

| Factor | Original zero-based rows |
| --- | --- |
| left `(a,b)` | 0, 1, 2, 5, 6, 15, 16, 17, 20, 21, 22, 30, 31, 32, 35, 36 |
| right `(j,i)` | 10, 11, 12, 13, 14, 25, 26, 27, 28, 29, 37, 40, 41, 42, 43, 44 |
| interval `d` | 3, 4, 7, 8, 18, 19, 23, 33, 34, 38 |
| base `(c,e,f,g,h)` | 9, 24, 39 |

These lists have sizes 16,16,10,3 and exhaust 0 through 44 once. Their support
property is a literal inspection of the complete original normal matrix, not
an assertion that some later rows are irrelevant. In particular row 36 belongs
to the left polygon and row 37 to the right polygon; the mixed-height gates
are retained in the endpoint formulas below.

For a generic legal original boundary, use its original beta functionals in
the formulas. This is a uniform statement about that fixed original normal
matrix, not an inference from numerical beta values at delta. Duplicate normals
may have different beta values and are NOT generically discarded.

## 3. Uniform endpoint formulas from all original rows

Define the integer polygon kernel

    K(A0,A1,B0,B1,D0,D1,S)
      = #{(x,z) in Z^2:
             A0<=x<=A1, B0<=z<=B1,
             D0<=x-z<=D1, x+z>=S}.                   (1)

Arguments are integral at integral boundary and integral base heights. Empty
intervals or inconsistent inequalities give zero.

For the left polygon `(x,z)=(a,b)`, the complete seven parameters are

    A0 = max(-beta0,-beta30,e-beta20),
    A1 = min(beta15,e+beta35),
    B0 = max(c-beta17,c+e-f-beta6,f-c-beta32),
    B1 = min(c+beta2,c+f-g+beta22,e+f-h+beta36),
    D0 = max(-beta16,-e-beta5),
    D1 = min(beta1,e-f+beta21),
    S  = e-beta31.                                    (2)

For the right polygon `(x,z)=(j,i)`, they are

    A0 = max(-beta14,-beta29,h-beta42),
    A1 = min(beta44,h+beta27),
    B0 = max(g+h-f-beta10,f-g-beta26,g-beta41),
    B1 = min(g+beta11,f+h-e+beta25,f+g-c+beta37),
    D0 = max(-h-beta12,-beta43),
    D1 = min(beta13,h-f+beta40),
    S  = h-beta28.                                    (3)

The complete middle interval has

    Ld = max(c-beta3,g-beta8,-beta19,c-g-beta23,
             g-c-beta33,-beta34),
    Ud = min(beta4,c-f+g+beta7,c+beta18,g+beta38),
    Nd = max(0,Ud-Ld+1).                              (4)

The remaining base indicator is exactly

    T(c,e,f,g,h) = 1{
        beta9+e-f+h>=0,
        beta24+e-h>=0,
        beta39-e+h>=0}.                              (5)

Every beta in (2)-(5) is its literal original-row boundary contribution. One
can verify each formula simply by substituting into the assigned original row;
no projection oracle is required.

Consequently the **complete original** count at every positive integer grade is

    P_boundary(t) = sum_(y=(c,e,f,g,h) in Z^5)
                    T(t,y) K_left(t,y) K_right(t,y) Nd(t,y).       (6)

The sum is finite because a nonzero summand lifts to the bounded original hive.
For execution it may be restricted to the projection of any certified box
containing the entire original hive. A box obtained from selected samples is
not a certificate. Formula (6) includes all original rows, rather than adding
an exterior after evaluating an unsectioned scalar.

## 4. Explicit six-branch arithmetic kernel

For (1), the lower and upper affine bounds on `x`, as functions of integer `z`,
are the ordered lists

    L0(z)=A0, L1(z)=z+D0, L2(z)=S-z;
    U0(z)=A1, U1(z)=z+D1.                            (7)

Choose the first index attaining the maximum lower bound and the first index
attaining the minimum upper bound. For each of the six index pairs `(l,u)`,
its complete integer branch is defined by

    B0<=z<=B1,
    Ll(z)-Lk(z) >= 1 if k<l, else >=0, for k!=l,
    Uk(z)-Uu(z) >= 1 if k<u, else >=0, for k!=u,
    Uu(z)-Ll(z)>=0.                                  (8)

All ones in (8) are once-only **selector tie assignments**, not stretched
facets. Original closed interfaces remain closed. No original lattice point
is discarded on a tie: its unique smallest-index selectors count it.

Each gate is `m z+q>=0`, with `m` in `{-2,-1,0,1,2}`. Starting from `[B0,B1]`,
update its integer endpoints as follows:

    m>0: low=max(low,ceil(-q/m));
    m<0: high=min(high,floor(q/(-m)));
    m=0,q<0: branch empty; m=0,q>=0: no restriction.   (9)

Let the surviving interval be `[v,w]`, let `n=w-v+1`, and write
`Uu-Ll = alpha z+gamma`. The branch's complete count is

    alpha * n*(v+w)/2 + (gamma+1)*n.                 (10)

When `v>w`, its count is zero. Otherwise the interval and (8) ensure every
fiber has at least one integer x. The arithmetic-series numerator is even;
all arithmetic is exact. Summing (10) over six branches proves (1) for every
integer input, including negative parameters, empty support, zero widths and
all ties. No polynomial fit or presumed eventual chamber is involved.

The affine maps back to original points are literal insertion:
choose `z` in the branch interval, choose integer `x` from `Ll(z)` through
`Uu(z)`, and place these into `(a,b)` or `(j,i)`. The inverse is original
coordinate projection. There is no Jacobian or lattice-index factor.

### Real support and integer lifting

For fixed integral parameters with `A0<=A1` and `D0<=D1`, the complete real
projection onto z is

    p=max(B0,A0-D1,S-A1,(S-D1)/2),
    q=min(B1,A1-D0),        p<=z<=q.                (11)

This follows from all six lower-versus-upper comparisons in (7). In particular
q is integral and p is at worst half-integral. A nonempty real fiber therefore
has the integer lift

    z=ceil(p),  x=max(A0,z+D0,S-z).                  (12)

Thus every integral point of the full real five-coordinate projection lifts
to the original integral hive. This is a genuine additional support fact;
we are not using it to erase parity in the number of lifts. Real projection
vertices may still be rational. Equations (8)-(10) retain that rationality.

## 5. Full first-failure fields on the SAME interface

A stronger closure property makes this a repair for loss of exterior information.
Give each original row status `+`, `-`, or `0`: keep its closed inequality,
keep its strict violation, or omit it. Always retain the certified original
box. A negative status means exactly

    ell_r <= -1, equivalently -ell_r-1>=0,           (13)

at each positive integer grade. The one is never multiplied by t. Rows with
positive status keep the original zero threshold. A first-failure sector is
the special status pattern `+` before one chosen row, `-` at that row, and
`0` after it.

At a fixed base y, a left or right group still uses only the normal directions

    (1,0), (0,1), (1,-1), (1,1), and their negatives.

Exactly ONE row in each group has a sum normal: row 31 on the left and row 28
on the right. Reversing or omitting rows therefore leaves at most one sum
wall, of either orientation. Combining parallel lower bounds by maximum and
parallel upper bounds by minimum yields at most three affine lower x bounds
and two upper bounds, or two lower and three upper bounds. Without a sum wall
there are at most two of each. The original box supplies finite coordinate
bounds even when later rhombi were omitted.

The same ordered-selector construction (8)-(10) therefore evaluates EVERY
such private field with at most six branches. A middle group is still an
integer interval. Base rows are still literal indicators with their exact
status shifts. Their product is the complete ten-height field at y, with all
shared exterior conditions retained. The checker `sector_fields.py` implements
this adapter directly from the admitted 45 normal rows, rather than from the
special closed formulas (2)-(4).

An elementary strengthening of the lift argument also survives these statuses.
A rectangle intersected with an integral difference strip is an integral
polygon: its active two-row determinants have absolute value at most one.
If its intersection with the one remaining integral sum halfspace is nonempty,
an integral vertex maximizing or minimizing the sum lies in that halfspace.
Thus real nonemptiness of each private polygon still implies an integer lift.
This statement is at a fixed integral base and retains the once-only shift;
it does not assert an integral vertex set after the sum cut.

For any row order, let `F_0(t,y)` be the complete original-box field, `F(t,y)`
the full retained field, and `D_r(t,y)` the first-failure fields evaluated by
this adapter. Then the usual partition becomes a **pointwise executable**
identity

    F_0(t,y)=F(t,y)+sum_r D_r(t,y).                  (14)

Each side is evaluated by explicit integer intervals and arithmetic sums of
bounded branch count. Any additional weight depending on the five retained
heights can multiply (14) before summation. A genuinely new exterior involving
one of the eliminated heights must be inserted into its private group and its
normal class checked; the six-branch claim is not made for arbitrary new rows.

This pointwise count identity does not license taking an ordinary coefficient
of a fiber before contracting its moving exterior. Residues, lower terms and
all interface multiplicities remain part of the complete sum.

## 6. Exact interface width and what its lower bound means

The primal graph has a vertex for each original height and an edge whenever
an original rhombus contains both heights. Every original row support is a
clique. The three corner vertices a,d,j are simplicial, with respective
neighbors `(b,e,f)`, `(c,f,g)`, `(f,h,i)`.

After deleting these corners, the seven-vertex induced graph has universal
vertex f and three opposite pairs with no edge inside a pair:

    (b,i), (c,h), (e,g).

Every other pair is an edge. It is exactly `K_{2,2,2,1}`. Its minimum degree
is five. Every graph of treewidth k has a vertex of degree at most k in each
nonempty induced subgraph: restrict a width-k decomposition, remove redundant
leaf bags, and take a vertex appearing only in a leaf bag. Its neighbors lie
in that bag. Thus treewidth of the original graph is at least five.

An attaining original-coordinate order is

    a,d,j,b,i,c,e,f,g,h.                             (15)

The separator sizes, after filling neighbors at every step, are

    3,3,3,5,5,4,3,2,1,0.                            (16)

More explicitly, after the corners are eliminated, b's remaining neighbors
are `(c,e,f,g,h)`. Eliminating b completes these five to a clique; i already
has precisely the same five neighbors. Eliminating i leaves that five-clique,
which can be eliminated in any order. This proves the upper bound five and
establishes equality. The accompanying checker reconstructs this graph directly from the rows.

Grouping `(a,b)` and `(j,i)` does not change this width claim. It is a compact
implementation of (15), evaluating the two two-dimensional messages directly.
A scalarized coordinate elimination cannot have all separators of size four.
A block with more internal coordinates can of course leave only four or fewer
external variables; its internal summation burden is precisely what the width
statement does not hide or forbid. No complexity lower bound for all possible
symbolic algorithms follows from treewidth.


## The 229-comparison real projection

For either private pair write its complete kernel as

    A0 <= x <= A1, B0 <= z <= B1,
    D0 <= x-z <= D1, x+z >= S.

Let A-, A+, B-, B+, D-, D+ be the FULL affine lists for its extrema:

    A0=max A-, A1=min A+, B0=max B-, B1=min B+,
    D0=max D-, D1=min D+.

For the left pair these lists are

    A- = (-beta0,-beta30,e-beta20),
    A+ = (beta15,e+beta35),
    B- = (c-beta17,c+e-f-beta6,f-c-beta32),
    B+ = (c+beta2,c+f-g+beta22,e+f-h+beta36),
    D- = (-beta16,-e-beta5),
    D+ = (beta1,e-f+beta21), S=e-beta31.

For the right pair they are

    A- = (-beta14,-beta29,h-beta42),
    A+ = (beta44,h+beta27),
    B- = (g+h-f-beta10,f-g-beta26,g-beta41),
    B+ = (g+beta11,f+h-e+beta25,f+g-c+beta37),
    D- = (-h-beta12,-beta43),
    D+ = (beta13,h-f+beta40), S=h-beta28.

## An explicit finite affine presentation

For each pair form the ordered list of thirteen lower affine expressions

    L = B-
        concatenated with (a-d : a in A-, d in D+)
        concatenated with (S-a : a in A+)
        concatenated with ((S-d)/2 : d in D+),

and the list of seven upper expressions

    U = B+ concatenated with (a-d : a in A+, d in D-).

Its full real support is given by the following 101 labelled affine
inequality occurrences:

    a <= a'        for all a in A-, a' in A+       (6),
    d <= d'        for all d in D-, d' in D+       (4),
    l <= u         for all l in L, u in U          (91).

Keep all occurrences, including any identical or redundant ones. Multiplying
an inequality containing a half by two makes its coefficients integral. There
is no irredundancy, facet count or projected-vertex denominator claim here.

The middle coordinate contributes the 24 comparisons between the complete lists

    Ld = (c-beta3,g-beta8,-beta19,c-g-beta23,g-c-beta33,-beta34),
    Ud = (beta4,c-f+g+beta7,c+beta18,g+beta38).

The three remaining original base rows are

    beta9+e-f+h >= 0, beta24+e-h >= 0, beta39-e+h >= 0.

Together these are 2*101+24+3 = 229 explicitly indexed affine inequality
occurrences in five original coordinates. All 45 original rows occur in their
literal factors or in the base. In particular the mixed-height bounds from
rows 36 and 37 remain present. No selected exterior is applied afterward.

## Projection proof and lattice statement

For fixed z, the full pair is feasible exactly when

    max(A0,z+D0,S-z) <= min(A1,z+D1), B0<=z<=B1.

The six lower-versus-upper comparisons give A0<=A1, D0<=D1, and

    max(B0,A0-D1,S-A1,(S-D1)/2)
      <= z <= min(B1,A1-D0).

Expanding each maximum and minimum into its literal list gives exactly L and U
above. Thus the 101 comparisons are equivalent to real feasibility of that
private polygon. The interval comparisons and three base rows are also exact.
Because the two pairs and interval share only the retained base, their choices
combine independently into a point satisfying ALL original inequalities.
This proves equality with the real coordinate projection, in both directions.

For integral original boundary and integral base y, all A/B/D/S extrema are
integers. Put p=max L and q=min U. The upper endpoint q is integral; when
p<=q, z=ceil(p)<=q and

    x=max(A0,z+D0,S-z)

is an integer between its complete lower and upper bounds. Apply this to both
pairs and choose d=max Ld. Inserting these five private coordinates gives an
original integral hive. Conversely every original integral hive projects to
an integral point satisfying the 229 comparisons. The kernel of the coordinate
projection Z^10 -> Z^5 is saturated. This existence selector is piecewise affine
with rounding; it is not a global additive hive section.

The full lattice COUNT still needs the two complete polygon fields above and the
interval length, summed over the projected base. Integral lifting at each base
does not make projected vertices integral, remove parity from the private
counts, bound the period of moving sectors by two, or prove the sign of a
weighted coefficient. Empty supports, ties and zero-width polygons obey the
same weak comparisons and the same integer lifting proof. All original count
and first-failure kernels, residues and negative weighted/exterior controls
remain unchanged and retain their separate source credit.


## Residues, dimensions and scope

At an integral fixed base ray, the private polygon's active determinants have
absolute value one or two. Its vertex denominators divide two, so its count may
have period two. This assertion concerns each fixed private polygon, not the
whole hive or sectors over a moving base. On a fixed parity and fixed selector
region each polygon formula has degree at most two; the product with the
interval has degree at most five. All constants and lower terms are retained.

For example, 0<=z<=x<=t with x+z>=t has count (k+1)^2 at t=2k and
(k+1)(k+2) at t=2k+1. The constituents are t^2/4+t+1 and t^2/4+t+3/4.
Replacing the odd constant by the literal value at t=0 is incorrect.

Points, segments, zero-width fibers and empty supports retain their actual
dimensions. At every positive integer t the formula counts the complete
original hive. A nonempty whole LR family has constant one; a positive-stretch
infeasible family has the zero polynomial by convention; the all-empty triple
has polynomial one. Whole LR polynomiality does not assign period one to
intermediate sectors.

The treewidth lower bound applies to original-coordinate elimination with
scalar factor separators. It does not exclude a different chart, a more
complicated block kernel, symbolic compression, or a four-variable final formula.
No complexity lower bound for every possible algorithm is asserted.
