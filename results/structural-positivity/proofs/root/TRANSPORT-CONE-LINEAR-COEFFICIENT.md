# The homogeneous transportation cone: a sharp linear-coefficient bound

Root derivation during return processing. **Pending independent argument review
and the seven endpoint polynomial receipts.** The all-parameter proof below
does not treat integer-h sampling as a proof on rational directions. The full
ordinary-coefficient question remains open in the stated complement.

## Statement

For integers u>=1 and v>=0, let T(u,v) be the entire nonnegative 4-by-7 matrix
polytope with row margins

`r=(7u+v,5u,4u,u)`

and column margins

`c=(4u+v,3u,2u,2u,2u,2u,2u)`.

Let E(u,v;t) count the integer points in t T(u,v), and write e_k(u,v) for
its ordinary coefficient of t^k. Put a_j=e_1(1,j), j=0,...,6.

For j=0,...,5 and ju<=v<=(j+1)u,

`e_1(u,v)=((j+1)u-v) a_j + (v-ju) a_(j+1)`.

For v>=6u,

`e_1(u,v)=u a_6`.

Consequently, after independently establishing the endpoint values and their
reported monotonicity, the sharp bound is

`e_1(u,v) >= (5279/360) u > 0`.

Equality holds at v=0 for every u>=1. The entire polytope has dimension eighteen,
so its leading two coefficients are positive. Section 6 also proves e16>0.
Thus an ordinary-negative member of this homogeneous LR cone, if one exists,
must have a negative coefficient among e2,...,e15. Endpoint positivity alone
does not settle that remaining range.

## 1. An explicit entire LR realization for every integer u,v

Use lambda outer and the balanced partitions

```text
lambda=(27u+v,22u+v,18u+v,17u+v,13u,10u,8u,6u,4u,2u),
mu=(17u+v,17u+v,17u+v,13u,10u,8u,6u,4u,2u),
nu=(17u+v,10u,5u,u).
```

Their sizes are 127u+4v, 94u+3v and 33u+v. All partitions are legal for
u>=1,v>=0 and the ordinary rank is ten.

The first three skew rows have common left offset 17u+v and lengths
10u, 5u, u. In an LR tableau they are forced to contain respectively labels
1,2,3 only: the first-row lattice-word condition forces label one; column
strictness and the lattice-word condition force labels two and then three in
the next rows. The same proof applies after every positive integer stretch.

The remaining seven skew rows have lengths c above. Each is disjoint in
columns from every other remaining row and from the initial block. For
successive rows the inner gap equals the next row's length. There are no
additional column comparisons.

After the first three rows, the remaining label multiplicities are exactly
r. The initial excesses of label i over i+1 are 5u, 4u, u. These respectively
equal the total remaining multiplicities of labels two, three and four.
Therefore every later word prefix satisfies the lattice-word inequalities,
even if all remaining copies of the larger label occur first. No ballot
restriction on the seven detached rows remains.

Record the number of each of the four labels in each of those seven rows.
This is precisely a nonnegative 4-by-7 integer matrix with margins r,c.
Conversely, sort each row's prescribed entries and adjoin the forced initial
block. The resulting tableau is semistandard and has a lattice word by the
preceding bounds. The maps are inverse and commute with stretching.

The same row-count equations and redundant inequalities give the entire real
polytope and integer lattice, not just a scalar identity. Three rows and six
columns of selected entries give eighteen free coordinates; the final row
and column are recovered by integer subtraction. All margins are positive,
and the matrix with entries r_i c_j / sum(r) is strictly positive. The actual
dimension is eighteen. Bipartite network-incidence total unimodularity gives
integral vertices, so ordinary Ehrhart theory applies without period collapse.

This full homogeneous realization extends the displayed integer-h
specialization in Pro027's proofs 011/012 by the explicit argument above.
The source size-133 parent is a different bare triple with the same h=0
transportation polynomial after row/column permutation; it is not this
size-127 lift's literal input.

## 2. Every possible feasibility wall has integer slope from zero to six

Use the full bipartite incidence equations A x=b(u,v), with one redundant
equation removed. A basic solution is supported on a spanning tree of K4,7;
any vertex support forest can be augmented by zero entries to such a tree.

Deleting a tree edge splits its vertices into a set S of row vertices and a
set C of column vertices. The corresponding basic entry, up to an orientation
sign, is the complete cut balance

`r(S)-c(C)=alpha u+beta v`,

where alpha is an integer and

`beta=1_(row1 in S)-1_(column1 in C) in {-1,0,1}`.

If beta=0, its sign is constant for u>0, unless it vanishes identically.
If beta=1, S contains the row of initial margin seven and C excludes the
column of initial margin four. Hence alpha>=7-13=-6. A nonnegative root
h=v/u=-alpha is therefore an integer at most six. If beta=-1, the row sum
excluding row one is at most ten and the column sum including column one
is at least four. Thus alpha<=10-4=6, and the nonnegative root h=alpha is
again an integer at most six.

These statements use all subsets, not a selected list of trees or observed
vertices. Therefore every basic entry has constant sign throughout each open
sector j<v/u<j+1, j=0,...,5. The entire feasible-basis roster is constant
there, including basic entries that vanish identically on the parameter plane.
There is no assertion that each of the possible seven wall slopes is a
genuine change of combinatorial type; this complete refinement suffices.

## 3. Whole Minkowski equality, including the sector walls

Fix a linear objective on the full matrix space and an optimal vertex at one
interior parameter in a sector. Choose a spanning-tree basis B representing
it. Its basic solution x_B(u,v) is linear in u,v. By section 2 it is feasible
on the whole closed sector. Every coordinate zero at the interior parameter
is identically zero on this sector: nonbasic entries are always zero, and a
basic entry cannot have a nonidentical zero at a strictly intermediate slope.

The normal cone at that vertex is generated by the active nonnegativity
normals and the equality row space. Thus the fixed objective is a row-space
functional plus a nonpositive linear combination of those active coordinate
functionals. The same representation certifies x_B(u,v) as optimal throughout
the closed sector, including degenerate endpoints. This is the usual exact
linear-programming optimality condition; no nondegeneracy assumption is used.

For every objective, its support value on T(u,v) is consequently linear in
the parameters in that sector. Writing

`a=(j+1)u-v`, `b=v-ju`,

gives a,b>=0, a+b=u, and (u,v)=a(1,j)+b(1,j+1). Equality of all support
functions proves the equality of the entire real polytopes

`T(u,v)=a T(1,j)+b T(1,j+1)`.

For integer u,v the coefficients a,b are nonnegative integers. This is a
polytope equality, not a claim that lattice-point counts simply add, nor a
claim of unique decomposition of their integer points.

## 4. First Ehrhart coefficients are Minkowski additive

For lattice polytopes P,Q the Bernstein–McMullen multivariate Ehrhart theorem
gives one polynomial F(a,b) counting aP+bQ for nonnegative integer a,b.
Substitute (ta, tb). The coefficient of t is the total-degree-one part of F,
namely a e1(P)+b e1(Q), as seen by setting either parameter to zero.
Therefore

`e1(aP+bQ)=a e1(P)+b e1(Q)`.

This works in the full matrix lattice even though the transportation polytopes
lie in affine subspaces. Their vertices are integral, and the theorem applies
to lower-dimensional lattice polytopes as well. Equivalently, integer
translations identify the affine fibers with the common saturated kernel
lattice. The formula in the statement now follows from section 3.

A primary exposition is Theorem 2.1 of Haase, Juhnke-Kubitzke, Sanyal and
Theobald, [Mixed Ehrhart polynomials](https://www.math.uni-frankfurt.de/~theobald/publications/mixedehrhart1.pdf).
The first-coefficient additivity itself is also stated explicitly in
[Minkowski valuations on lattice polytopes](https://dmg.tuwien.ac.at/ludwig/lattice.pdf).
This is established prior theory, not a new general additivity theorem.

## 5. The final sector is an exact translation

If v>=6u, the first-column sum is 4u+v and the other three row sums total
10u. Every feasible matrix therefore has x11>=v-6u. Subtract v-6u from x11.
The new first row and column margins are 13u and 10u; all other margins are
unchanged. This is an integer translation with inverse addition, giving

`T(u,v)=u T(1,6)+(v-6u) E11`,

where the last summand is a single matrix point. Integer translations do not
change an Ehrhart polynomial. Thus e1(u,v)=u a6.

The endpoint input is precisely the seven independent polynomials P_j for
j=0,...,6 from the full transport recount, their strict first-coefficient
increments and a0=5279/360. Their minimum is a0. The coefficients in section 3
sum to u, proving the sharp uniform bound in every finite sector, and the
translation proves it above slope six. The final acceptance must cite the
actual complete endpoint receipt; a provider's reported monotonicity is not
silently substituted for that check.

## 6. A direct third-highest-coefficient protection

Here is a useful corollary of the established complete two-normal BV formula.
Let P be full-dimensional in Z^d, d>=2, with a period-one rational Ehrhart
count. Suppose every primitive inward facet normal has entries in {-1,0,1}
in that specified lattice basis. Then

`[t^(d-2)] L_P(t) >= (1/12) sum_(dim F=d-2) vol_Z(F) > 0`.

For two independent such primitive normals u,v, put a=||u||^2,
b=||v||^2, c=<u,v>, and let q be the positive gcd of their 2-by-2 minors.
Those minors have absolute value at most two, so q is one or two. The
Dedekind correction s(p,q) is zero in both cases (p=1 modulo two in the
second). Moreover c<=min(a,b), since nonzero entries have absolute value one.
Consequently c(1/a+1/b)<=2. The complete quotient-lattice formula is

`alpha(u,v)=1/4+s(p,q)-c(1/a+1/b)/(12q) >= 1/12`.

Sum over actual codimension-two faces using their positive normalized volumes.
For rational period-one P, clear vertex denominators and divide the resulting
coefficient and face-volume bounds by the same positive dilation factor.
The proof does not assume that the individual undilated affine BV terms are
nonperiodic. This uses the formula and lattice convention already proved in
Pro025 proof 023; no source checker or local scalar table supplies the bound.

For T(u,v), select the first three rows and first six columns as free
coordinates. Nonnegativity of all twenty-eight entries has normals of four
forms: coordinate unit vectors, negative row sums, negative column sums and
the positive sum of all eighteen coordinates. Every entry is in {-1,0,1}.
Every facet is supported by one of these inequalities, so the criterion
applies in the proved Z^18 lattice and gives e16>0 for every u>=1,v>=0.
This corollary makes no worldwide novelty claim.

## Exact remaining question

The whole polytope decomposition opens a finite set of two-parameter mixed
Ehrhart problems. For k>=2, the coefficient e_k in a sector is a homogeneous
polynomial of degree k in a,b; its mixed terms are not determined by the two
endpoint Ehrhart polynomials. A proof of all their signs or a legal negative
specialization still requires new mathematics or exact complete computation.
The meaningful remaining range here is k=2,...,15. No new outside-the-box
count or negative search has been run to obtain this argument.
