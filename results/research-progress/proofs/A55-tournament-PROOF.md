# A55: complete staircase LR families with their actual score lattice

Curated mathematical proof from **A55**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

26 September 2026. Root derivation and exact discriminator. The accepted complete-graph flow proof at
methods/frontier-011-013-2026-09-06/roots/PROOF.md is the even-cap predecessor.
The general-height interior theorem at methods/frontier-008-010-2026-09-06/
roots/GENERAL-HEIGHT.md is another antecedent. The Weyl-character/tournament
connection is classical. No worldwide novelty is claimed. The contribution
here is a complete all-score, all-boundary treatment of odd as well as even
edge caps, exact original LR tests, and a priced discriminator of the negative
and content-balancing routes.

## 1. Whole original LR construction, all caps

Let n>=2, k>=1 be integers. Let g=(g_1,...,g_n) be nonnegative integers of
sum k*n*(n-1)/2, and let delta=(n-1,n-2,...,0). Define


```text
Lambda_i=sum_(j>=i) g_j,  Mu_i=sum_(j>i) g_j,  Nu=k delta.
```

These are partitions even when g is not sorted; the skew rows are disjoint in
columns, and its complete skew Schur function is product_i h_(g_i). Hence


```text
P_(k,g)(t)=c^(t Lambda)_(t Mu,t Nu)=K_(kt delta,tg).       (1)
```

The bialternant for the complete character is


```text
s_(kt delta)(z)=product_(i<j)
       (z_i^(kt+1)-z_j^(kt+1))/(z_i-z_j)
  =product_(i<j) sum_(x=0)^(kt) z_i^(kt-x) z_j^x.       (2)
```

Thus (1) counts ALL arrays x_ij, i!=j, satisfying


```text
x_ij>=0,  x_ij+x_ji=kt,  sum_(j!=i) x_ij=t g_i.        (3)
```

There is one choice of an integer match score, not binomial multiplicity for
kt separately labelled games. This distinction is part of the model. The count
identity is entire at all t>=0 for feasible data, with P(0)=1. Infeasible
positive-stretch data have the zero polynomial by the campaign convention.
No proper face or quotient is substituted for the original LR parent.

The real graph polytope need not be identified affinely with the original hive.
The proof identifies all integer counts and their stretching polynomials.
Actual degree transfers through equality of these polynomials, not through a
claim about hive face metrics.

## 2. Feasibility, every tight cut and the saturated lattice

Sort g increasingly; vertex permutation preserves (3). The exact feasibility
conditions are


```text
sum_(i=1)^j g_i >= k*j*(j-1)/2,  1<=j<n,               (4)
```

together with the total-sum equality. For any subset S the internal games
contribute exactly k*choose(|S|,2); excess score counts wins against its
complement. Necessity follows. Sufficiency is the standard capacitated
orientation max-flow argument: send k units from each match node to its two
endpoint nodes, whose demands are g_i. Every cut reduces to the subset lower
inequality and its complementary upper inequality. For a fixed cardinality,
the smallest sorted prefix has the smallest score sum, so (4) covers every
subset. Integral capacities admit integral augmenting paths.

If equality holds at a prefix of size j, that prefix wins no match against the
complement. All its cross entries are forced, not discarded. It follows that
the ENTIRE graph count factors into its two internal counts; the later scores
are reduced by k*j. Cutting at every tight prefix partitions g into primitive
blocks b, with the earlier-block offset subtracted. This is an integral affine
product decomposition, with a unique inverse restoring all forced matches.

In a primitive block of size m>=2 all proper cut inequalities are strict.
There is a point with every match entry strictly between 0 and k: subtract a
sufficiently small epsilon from both directions of every match, reducing total
capacity to k-2 epsilon and each score by (m-1) epsilon. All finitely many
strict cut slacks survive, so the real max-flow argument supplies that point.
The incidence equations have rank m-1, giving dimension


```text
D_m=choose(m,2)-(m-1)=(m-1)(m-2)/2.                  (5)
```

Choose all edges among the first m-1 vertices freely and solve the star edges
to the last vertex from the score equations. The resulting affine formulas
have integer coefficients and coefficient one on the solved edges. They give
the entire affine integer lattice Z^D_m, not a finite-index sublattice. The
reduced incidence matrix is totally unimodular; adding integral box bounds
therefore gives an integral graph polytope. Its actual Ehrhart degree is (5).
A singleton block is a point, degree zero. For general feasible g the exact
degree is the sum of (5) over its primitive blocks. This retains every degree
drop and all boundary factors.

## 3. Interior counts and codegree before interpolation

For a primitive nonpoint block, strictness in all coordinate bounds describes
the entire relative interior. At positive integer t, subtract one from every
directed match entry. This is an integral bijection onto a score problem with

    match capacity kt-2,  scores t b_i-(m-1).             (6)

If the new capacity or a required score is negative the interior is empty.
For k=1, grade one is empty. The exact cut inequalities for (6) simplify to


```text
t*(sum_(i=1)^j b_i-k*j*(j-1)/2) >= j*(m-j).
```

Consequently the codegree is the maximum, over proper prefixes, of the ceilings
of j*(m-j) divided by its positive original slack. Singleton point factors
have interior count one and do not create a zero. Ehrhart reciprocity gives
P(-t)=(-1)^D times the complete relative-interior count. This is why negative
grades in the reconstruction are legitimate; they are not negative ordinary
coefficients and not fitted zeros.

For k=1 and odd n=2r+1, the regular score g=(r,...,r) turns (6) into the SAME
family at t-2. Therefore its entire polynomial satisfies


```text
P(-2-t)=(-1)^D P(t),  D=r*(2r-1), codegree 2.         (7)
```

The all-ones match array is the unique interior point at grade two. There is
no integral regular score at odd k and even n, so that case is not silently
assigned this formula. The familiar even-cap centered circulation instead has
its own scaling and center. In particular, setting y_ij=2x_ij-t when k=1
restricts y_ij to the parity coset y_ij congruent to t modulo 2. It does NOT
count every integer edge in [-t,t]. The codegree-two reflection in (7) is
centered at -1, whereas the unscaled integer circulation family is centered
at -1/2. Mixing these two lattices would change the polynomial.

## 4. Exact recurrence and complete finite discriminator

For fixed capacity c and a sorted score list s on m labelled vertices, remove
one vertex. Choose its wins z_i in [0,c] summing to its score. Remaining scores
are s_i-c+z_i. Their counts depend only on their multiset, so sorting is valid.
Within an equal-score group, enumerate a sorted z multiset and multiply by its
multinomial number of labelled assignments. Global reversal sends s_i to
(m-1)c-s_i and also preserves counts. Neither quotient loses multiplicities.
The three-vertex terminal is the length of the complete intersection

    [0,c] intersect [s_1-c,s_1] intersect [c-s_2,2c-s_2].

The inequalities used for early rejection are necessary cut conditions; a
false sufficiency shortcut does not replace enumeration. This recurrence and
the interior map above are implemented independently of provider code.

At k=1,n=7, every nondecreasing feasible integral score list in [0,6]^7 is
included: 59 full weights. Their 34 primitive score inputs produce 26 distinct coefficient vectors,
including lower-rank boundary blocks. For each nonpoint input of degree D,
D+1 specified positive/negative points determine its polynomial, and two further
positive grades are unused holdouts. The singleton point polynomial one is
established directly and has no numerical holdouts. All whole coefficients and all 677 recorded balancing-edge
appearances are nonnegative. Point and proper-boundary cases retain their
actual degrees. This is a complete finite staircase-weight domain, not all
rank-seven boundaries and not an all-cap or all-rank sign theorem.

The regular n=7 original is


```text
Lambda=(21,18,15,12,9,6,3), Mu=(18,15,12,9,6,3,0),
Nu=(6,5,4,3,2,1,0).
```

Its full degree-15 polynomial has first coefficient 17804/2145. Writing u=t+1,
the exact identity is


```text
P(t)=u^3*(554/6435 + (331/1782)u^2 + (5531/25920)u^4
    + (4213/20736)u^6 + (17677/103680)u^8
    + (22933/228096)u^10 + (601421/14826240)u^12).
```

Thus every ordinary coefficient is strictly positive. The observed triple
root at -1 is certified for THIS polynomial; it is not inferred for arbitrary
n. Its determining grades 0..7 and unused grades 8,9 are in N7-POLYNOMIAL.json.
The direct symmetry computation agrees with the separate mixed-grade full
staircase reconstruction. Independent original-count and mutation controls
are in VERIFICATION.json.

The n=9 through-grade-four pilot is incomplete coefficient evidence. It prices
a future domain and supplies no degree-28 sign claim. General n, arbitrary
larger edge caps and unrestricted original LR boundaries remain open.

## 5. What this does and does not advance

This is a full negative-realization test surface whose original LR bridge is
already paid, whose dimension/lattice/reciprocity are proved, and whose weak
boundary strata factor exactly. A negative coefficient here would immediately
be a literal original candidate, unlike a hostile equality face. The declared
rank-seven discriminator found none. The proof also supplies original-model
tests of the independent content-balancing route. Further expansion should
target a concrete coefficient mechanism or a new asymmetric cap, rather than
automatically extending this positive list.
