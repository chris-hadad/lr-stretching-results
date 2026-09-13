# A3 first-jet reduction and positivity of every positive 4-by-4 transportation linear coefficient

Attempt: SLR-GPT6-PRO-FRONTIER-024-P04-A01-0f60b1b10c7b
Parent archive SHA-256: `1c3da888e9972f4cd21d808fc8f0bdf1e6608cd9d665346c1e68c2bb4e7b2880`.
Status: provider proof with an exact finite A3 chamber certificate; not independent campaign acceptance.

This is the material H03 deepening promised after Phase 3. It derives the
complete four-row linear-coefficient functional at four columns, rather than
inferring a sign from the eight positive controls. The complete transportation/LR
bridge remains the inherited S13 theorem. No additive original-box coverage is
claimed.

## 1. Four-row partial fractions and the exact A3 assignment

For four variables use `q1=x2/x1`, `q2=x3/x2`, `q3=x4/x3`. Lagrange partial
fractions give, for every nonnegative integer k,

    h_k(x1,x2,x3,x4) = T1+T2+T3+T4,

with

    T1 = x1^k /
         [(1-q1)(1-q1 q2)(1-q1 q2 q3)],

    T2 = - x2^(k+1)/x1 /
         [(1-q1)(1-q2)(1-q2 q3)],

    T3 = + x3^(k+2)/(x1 x2) /
         [(1-q1 q2)(1-q2)(1-q3)],

    T4 = - x4^(k+3)/(x1 x2 x3) /
         [(1-q1 q2 q3)(1-q2 q3)(1-q3)].

Let the N positive column margins be `c_1,...,c_N`, and assign each column to
one of these four terms. Let `n_i` be the number assigned to class i and `C_i`
the sum of their column margins. Put `n_1+...+n_4=N`. The six A3 positive-root
multiplicities, ordered as 100,010,001,110,011,111, are exactly

    m = (n1+n2, n2+n3, n3+n4, n1+n3, n2+n4, n1+n4).       (1)

The assignment sign is

    eps = (-1)^(n2+n4).                                    (2)

If rows are `r_1,...,r_4`, exact exponent balance gives the A3 target

    U = (C1-r1)t                 - n2-n3-n4,
    V = (C1+C2-r1-r2)t           - 2n3-2n4,
    W = (r4-C4)t                 - 3n4.                    (3)

Hence the complete scalar contribution is

    eps K_m(U,V,W),                                      (4)

where K_m is the coefficient of

    (1-q1)^(-m100) (1-q2)^(-m010) (1-q3)^(-m001)
    (1-q1q2)^(-m110) (1-q2q3)^(-m011)
    (1-q1q2q3)^(-m111).                                  (5)

A direct positive formula, used by the exact certificate, is

    K_m(X,Y,Z) = sum_(a,b,c>=0)
      B_m110(a) B_m011(b) B_m111(c)
      B_m100(X-a-c) B_m010(Y-a-b-c) B_m001(Z-b-c),        (6)

where `B_s(z)=binom(z+s-1,s-1)` for s>0 and nonnegative z, `B_0(0)=1`, and
all other invalid arguments contribute zero.

Formula (4) is not a selected face: summing it over all 4^N assignments is
exactly the full coefficient of `x^(tr)` in `product_j h_(t c_j)`, and S13
identifies that coefficient with the entire transportation count and with its
whole LR polynomial. Terms whose slope cannot enter the nonnegative A3 cone are
absent for all sufficiently large t. The remaining finite sum agrees with the
whole count at infinitely many t, hence its polynomial continuation is the
whole Ehrhart/LR polynomial.

The six distinct A3 roots are totally unimodular. The seven cones in the
selected A3 source refine their basis walls. Positive repetitions preserve the
chamber fan. If some multiplicity in (1) is zero, every remaining nonsingular
basis is still among the same sixteen A3 bases, so the strict interior of one
of these seven cones is either contained in one polynomiality chamber or lies
outside support. Boundary values are deliberately not used to reconstruct a
full-dimensional chamber polynomial below.

## 2. First-jet lemma: no stretch interpolation is needed

Let G be the unimodular 3-by-3 generator matrix of an eventual A3 cone, and let

    K_m(G x) = P_(m,G)(x)                                  (7)

be its chamber polynomial. Write the affine target (3) as `t R + delta`, and
put

    x_R = G^(-1) R,        x_delta = G^(-1) delta.

Once `tR+delta` stays in this chamber, its complete assignment polynomial is

    eps P_(m,G)(t x_R+x_delta).

Therefore its ordinary linear coefficient is exactly

    eps grad P_(m,G)(x_delta) . x_R.                       (8)

This is the **A3 first jet**. The assignment's entire degree can be as high as
`3N-3`, but its contribution to c1 is only one fixed gradient dotted with a
three-coordinate margin slope. The gradient depends on the class-count vector
n and the eventual chamber, not on the actual column magnitudes. Thus at fixed
N the full four-row c1 is a finite signed piecewise-linear functional of the
margins.

If a chamber wall is met identically, the vector-partition polynomiality on the
closed wall gives the same tangent value. A slope inequality that is not tied
has an integral difference of absolute value at least one, while every offset
in (3) has magnitude at most 3N; `t>=3N+1` therefore decides every eventual
strict side. This bound is only for chamber selection, not for interpolation of
the transportation polynomial.

## 3. Exact N=4 chamber certificate and the vanishing interaction

For N=4, every assignment system has sum(m)=12 and rank three, so degree at
most nine. There are 35 class-count vectors n and seven A3 cones: 245 chamber
polynomials. The exact checker reconstructs each one in the multivariate Newton
basis from the strict-interior nodes

    x = (1,1,1)+e,        e>=0, |e|<=9,                   (9)

220 nodes per chamber. The shift by `(1,1,1)` is load-bearing: the first failed
implementation sampled the cone vertex and allowed lower-dimensional wall
values of root-degenerate systems to contaminate a full-dimensional polynomial.
That failed attempt is preserved. One additional strict-interior point
`(1,1,1)+(10,0,0)` is unused in each reconstruction; all 245 holdouts agree
with the independent positive sum (6).

The resulting first-jet table has two decisive exact properties.

**Three-or-four-class vanishing.** There are thirteen N=4 class-count vectors
using at least three classes. Every one of their seven chamber gradients at its
assignment offset is zero: 91 exact zero gradient vectors. Thus every such
assignment has zero ordinary linear contribution, including the fully
four-class terms. The first genuinely A3-looking assignments do not survive at
linear order.

**Two-class factorization.** Every surviving two-class assignment must use
class 1. For classes `{1,j}`, j=2,3,4, let `s=n1`, `b=4-s` and

    W_s = (s-1)!(b-1)!/[2*3!].                            (10)

After including the assignment sign, the ambient first-jet gradient is `W_s`
times a vector depending only on j and the A3 chamber. It is independent of
`s=1,2,3`. The same normalized gradient is independently obtained at N=2,
`s=1`. `DATA/PHASE4/HINGE-CERTIFICATE.json` checks all 84 normalized gradient
entries and the 91 zero jets exactly.

The N=2 calculation uses degree three, 20 strict-interior nodes per chamber and
70 unused chamber holdouts. It is a challenge of the normalization, not a proof
by extrapolation from N=2.

## 4. Closed hinge formula for every positive 4-by-4 margin pair

Now specialize to four positive columns, but leave all margin magnitudes
arbitrary. For a nonempty proper column subset S put

    C = c(S),       s=|S|,
    w_S = (s-1)!(3-s)!/[2*3!].                            (11)

Thus w_S=1/6 for s=1 or 3 and w_S=1/12 for s=2. Write `x_+=max(x,0)` and define

    X = C-r1,
    Y = C-r1-r2,
    Z = C-r1-r2-r3,

    Phi12 = [2 X_+ +(X-r3)_+ +(X-r4)_+
             +2(X-r3-r4)_+]/3,                           (12)

    Phi13 = [Y_+ +2(Y-r4)_+]/3,                           (13)

    Phi14 = 2 Z_+/3.                                      (14)

Then the exact ordinary linear coefficient of the complete 4-by-4
transportation polynomial is

    c1(r,c) = (11/6)(r2+r3+r4)
              - sum_(empty!=S proper[4])
                    w_S (Phi12+Phi13+Phi14).              (15)

Here is why (15) is complete.

* If all columns use class 1, (3) has zero offset and the three root-group
  totals are `r2 t`, `r3 t`, `r4 t`. The contribution factors as

      binom(r2 t+3,3) binom(r3 t+3,3) binom(r4 t+3,3),

  whose c1 is `H_3(r2+r3+r4)=(11/6)(r2+r3+r4)`.
* A one-class assignment not using class 1 has negative first slope and never
  survives.
* Three- and four-class assignments contribute zero by the 91-jet certificate.
* A two-class assignment not using class 1 likewise has negative first slope.
  The three possible pairs `{1,2}`, `{1,3}`, `{1,4}` give, after the sign in
  (2), respectively `-w_S Phi12`, `-w_S Phi13`, `-w_S Phi14`.

For `{1,2}`, the eventual slope is `(X,r3+r4,r4)`. The applicable A3 cones
make the positive penalty have slopes 2/3, 1, 4/3 and 2 as X crosses the two
row values `r3,r4` and their sum. This is exactly the hinge expression (12).
For `{1,3}`, the strict identity between its first two slopes leaves only the
break at `Y=r4`, producing (13). For `{1,4}` the three slope coordinates are
strictly ordered whenever the term survives, producing (14). The finite
ambient-gradient table is the exact certificate for these chamber statements;
there is no fit to transportation c1 values.

As mandatory challenges, (15) gives

    rows (1,1,1,1), columns (2,2):       c1=7/3,
    rows (1,1,1,1), columns (1,3):       c1=11/6,
    rows (1,1,1,1), columns (1,1,1,1):   c1=65/18.         (16)

The first two reproduce the Phase-3 sign-changing correction fixtures. The
third is the independently counted Birkhoff-4 whole polynomial. All eight
Phase-3 4-by-4 controls agree with the jet formula; those values were not used
to reconstruct any chamber polynomial.

## 5. Concavity and the sharp global positive lower bound

Every map `ell -> ell_+` is convex. Equations (12)-(14) are nonnegative sums of
positive parts of linear forms. Equation (15) is therefore a linear function
minus positive weights times convex functions. Hence:

> The exact 4-by-4 transportation c1 has a jointly concave, homogeneous,
> piecewise-linear extension to the closed balanced nonnegative margin cone.

Homogeneous concavity implies superadditivity:

    c1(x+y) = 2 c1((x+y)/2) >= c1(x)+c1(y).               (17)

Direct substitution into (15) gives zero on every unit edge boundary: one row
margin and one column margin equal one and all other margins zero. Any balanced
nonnegative integral margin vector is a sum of such unit edge boundaries (take
any nonnegative integer table with those margins and decompose its entries into
unit cells). Therefore the extension of (15) is nonnegative on the whole
nonnegative integral margin cone.

For positive integral 4-by-4 margins, subtract one from each row and one from
each column. The residual margins are nonnegative and balanced. With
`u=(1,1,1,1;1,1,1,1)`, (17) and (16) give

    c1(r,c) >= c1(u) + c1((r,c)-u)
            >= 65/18.                                    (18)

The bound is sharp because equality is attained at the all-one margins.
Consequently **every positive integral 4-by-4 transportation polytope has
strictly positive ordinary linear coefficient**.

## 6. LR consequence and what remains open

The inherited complete S13 construction sends a positive p-by-N transportation
polytope to an entire ordinary LR stretch with rank `p+N-1` and degree
`(p-1)(N-1)`. Phase 3 already protected every transportation c1 with
`min(p,N)<=3`. The present theorem closes the first missing case p=N=4:
ordinary LR rank seven, degree nine.

Thus a negative linear coefficient arising from a **full positive
transportation polytope** cannot first appear at ordinary rank seven. The first
unprotected transportation sizes are 4-by-5 and 5-by-4, whose whole-LR bridge
has ordinary rank eight and degree twelve.

This does **not** prove generic rank-seven LR c1 positivity, any other ordinary
coefficient of 4-by-4 transportation polytopes, all transportation c1, or a
principal campaign endpoint. The finite scan through separately sorted positive
4-by-4 margins of total at most 16 (3,241 cases) found no negative and observed
minimum 65/18, but that scan is diagnostic only; theorem (18), not the scan,
settles the entire 4-by-4 class.

The natural H03 reentry is now to prove the same two-class/zero-higher-class
first-jet pattern for arbitrary column count N. N=2 and N=4 normalized pair
jets already coincide exactly. If that symbolic N-proof succeeds, (15) has a
credible all-N analogue and could push transportation c1 much farther. A
separate next attack should nevertheless move to H04 or H05 so this mission
does not spend all remaining effort on one mechanism.

## 7. Verification and failure accounting

`CODE/P04-A3-FIRST-JET.py` uses only Python standard-library exact integer and
Fraction arithmetic. A01 failed before producing a scientific result because
closed-cone interpolation included boundary points for root-degenerate systems.
The repaired A02 moved every determining and holdout site into strict chamber
interiors. A02 exited 0 in 13.46 wall seconds with peak RSS 104,620 KiB. The
failed A01 exited 1 in 0.69 seconds with peak RSS 93,868 KiB. A separate earlier
exploratory notebook roster timed out at 60 seconds and is not used as evidence.
All these resource charges are retained.

No dependency was installed, no historical returned program was executed, and
no external compute service, native campaign job, public action or external
message was used. The selected source bodies are copied inert under
`SOURCES/PHASE4/`; their original packet hashes and the copied hashes are
recorded separately. The exact A3 checker is independent of the Phase-3 literal
transportation DP in combinatorial representation, while both rely on Python
integer arithmetic rather than independent arithmetic engines.
