# U05-01 — All-ratio rank-seven interacting-original positivity and paid operations

Curated mathematical proof from **Pro048/A66 accepted dependency**. The corresponding accepted scope
is stated in the module guide; [the source map](../../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

**Status: PROVED in this return by the complete character argument and exact finite certificate.** The complete original bridge is U04-01, retained byte-for-byte and summarized below. No independent human review, formal proof-assistant certification, campaign adoption, or priority claim is inferred. This theorem does not use A61's unadopted stage as a mathematical premise.

## 1. Entire original, hypotheses, and result

Let b>=c>=1, k>=0, 0<=h<=b and 0<=g<=min(c,k) be integers. Choose any six long widths u,v,w1,w2,w3,w4>=b. Put


```text
d=(u,v,k,w1,w2,w3,w4), e=(h,g,0,0,0,0), T=sum d.
lambda7=d7,
lambda_i=lambda_(i+1)+d_i-e_i  (i=6,...,1),
mu_i=lambda_i-d_i,             nu=(T-b-c,b,c).
```

Lambda is OUTER. These are legal, size-balanced original partitions: every overlap is at most both neighboring widths, and T>=6b+k makes nu dominant. The positive last outer row makes the maximum trimmed original rank seven, even if the interior short row has zero width. The first three rows may have a triple-column interval of length max(0,h+g-v). All subsequent skew rows are mutually column-disjoint and disjoint from that block.

A nonempty tableau can be given explicitly. Set j=max(h,c). Its row multiplicities of letters1,2,3 are

    (u,0,0), (v-j,j,0), (k-g,0,g),
    (w1-(b-j)-(c-g),b-j,c-g), (w2,0,0),(w3,0,0),(w4,0,0).

Nonnegativity, column strictness and every ballot prefix follow from the stated floors, j>=h,c, and g<=c,k. In particular triple columns have1,2,3. Scaling gives a tableau at every positive grade. Thus the zero-grade convention is P(0)=1.

Let P(t)=c^(t lambda)_(t mu,t nu). Write >=_c for coefficientwise comparison in the **ordinary monomial basis in t**. The complete result is


```text
P(t) >=_c binom(t+D,D),                                     (1)
```

where D is the actual degree, specified in Section6. In particular every ordinary coefficient through actual degree is strictly positive. Long widths may be unequal and arbitrarily large above b; the entire count depends only on (b,c,k,h,g).

This closes all ratios of b,c,k for this rank-seven family, not just U04's3:2:1 template. It is not arbitrary rank-seven positivity, positivity with four or more interacting rows, below-floor width stability, arbitrary cap monotonicity, or unrestricted LR positivity. No absorber is assumed.

For the algebraic closure below we also allow c=0 (then g=0) and b=0. These cases are valid count/partition limits and are explicitly included in the certificate. They are lower-rank or two-row-inner terminal controls, not additional unsigned original coverage. When b=0, c=h=g=0 and the whole count is1, even if k>0.

## 2. Both shifted partners and the complete determinant

Here we record the all-m identity underlying the proof. Replace four remaining long rows by m-1 long rows, m>=2; there are m+2 physical rows. Write H_j=h_j(1,X,Y), H_j=0 for j<0, D0=(1-X)(1-Y), and


```text
R_j=h_j(X,Y)-XY h_(j-1)(X,Y), R_0=1.
```

The elementary exact identities are


```text
D0 H_L=1-R_(L+1),
(1-Y/X) R_j=X^j(1-Y)-X^(-1)Y^(j+1)(1-X).
```

For dominant B>=C>=0, the complete highest-weight extraction is


```text
c^lambda_(mu,(A,B,C))=[X^B Y^C]D0(1-Y/X)s_(lambda/mu)(1,X,Y).
```

If j>B and the remaining series has only nonnegative exponents, both monomials in the displayed formula for (1-Y/X)R_j vanish at that extraction. Hence a long H_L with L>=B may be replaced by1/D0 inside the full extraction. This is not equality of individual weights or raw characters.

At grade t the interacting block's full Jacobi–Trudi matrix is

    [ H_ut       H_((u+v-h)t+1)    H_((u+v+k-h-g)t+2) ]
    [ H_(ht-1)   H_vt              H_((v+k-g)t+1)      ]
    [ H_((h+g-v)t-2) H_(gt-1)      H_kt                 ].

Every +1,-1,+2,-2 occurs ONCE, not multiplied by t. Retain all six determinant terms. Valid long-factor replacements give, with A=H_(ht-1), B0=H_(gt-1), C0=H_kt and E=H_((h+g-v)t-2),


```text
C0/D0^2-B0/D0^2-A C0/D0+E/D0^2+A B0/D0-E/D0^2.
```

The two E contributions cancel only as full highest-weight contributions. Deleting one or suppressing the bottom-left entry before this calculation is invalid. The retained expression equals R_ht(H_kt-H_(gt-1))/D0^2. Including all other rows and the leading D0 yields the ENTIRE original


```text
P(t)=[X^(bt)Y^(ct)] (1-Y/X) R_ht (R_gt-R_(kt+1))/D0^(m+1).  (2)
```

Equivalently, for


```text
F_m(X,Y;L,K)=sum_{a,b>=0,L<=a+b<=K,a<=X,b<=Y}
            binom(X-a+m-1,m-1) binom(Y-b+m-2,m-2),
```

with a negative total giving zero,


```text
P(t)=F_m((b-h)t,ct;gt,kt)
     -F_m((c-h)t-1,bt+1;gt,kt).                           (3)
```

Both partners have the same band. At h=c the second is zero because its first total is -1. There is no continuation of a negative-slope count, discarded second cap, or separated-pair substitute. Unit4's complete proof also supplies the literal tableau affine-space prior bound2m-1; no hive metric is transferred by these count identities.

## 3. A universal finite-sum formula and PRIOR chamber degree

For nonnegative integer X,Y,j let


```text
A_j^(m)(X,Y)=
   sum_{i=max(0,j-Y)}^{min(j-1,X)}
      binom(X-i+m-1,m-1) binom(Y-j+i+m-1,m-1)
   +1_{X>=j} binom(X-j+m,m) binom(Y+m-1,m-1).             (4)
```

Negative X,Y or j gives zero; an empty sum is zero. This is exactly the coefficient of R_j/[(1-Xvar)^(m+1)(1-Yvar)^m]. To prove it, expand both h_j and -Xvar Yvar h_(j-1). Pair the terms at each i<j and apply Pascal's identity to the Xvar binomials. The unpaired i=j term is precisely the endpoint in(4).

Applying the two-monomial R_ht identity in(2) gives


```text
P(t)= A_gt((b-h)t,ct) - A_(kt+1)((b-h)t,ct)
      -A_gt((c-h)t-1,bt+1) + A_(kt+1)((c-h)t-1,bt+1).    (5)
```

Equation(4) is an exact complete numerator formula, not an inclusion-exclusion truncation. On a fixed choice of its lower/upper endpoints, its summand has total degree2m-2 in the parameters and summation variable. Exact polynomial summation raises total degree by at most one. The unpaired endpoint has degree2m-1. Therefore each parameter piece in(5) has PRIOR total degree at most2m-1, and for m=5 at most9. This proves the degree bound before any values are fit. It is not a mixed-Ehrhart assumption or a guess from interpolation.

In parameter order (b,c,k,h,g), the base cone has nonnegative forms

    g, c-g, b-c, k-g, h, b-h.

The complete additional homogeneous wall roster is

    c-h, b-h-g, c-h-g, k-c, k-b, k-b+h, k-c+h, k-b-c+h.       (6)

These are all the possible changes of X's sign, lower endpoint max(0,j-Y), upper endpoint min(j-1,X), or support j<=X+Y in the four terms of(5). In particular the lower-cut terms j=g cannot exceed X+Y on any legal full-dimensional domain; g<=c<=b eliminates an otherwise spurious wall.

### Closed walls and once-only offsets

The selected formulas hold on CLOSED cones, including all integral boundary nodes. This point is consequential. At a homogeneous wall X0=j0 the affine difference X-j is0,-1 or-2. If X=j, extending the sum to i=j contributes exactly the endpoint; if X=j-1 or j-2 the spurious endpoint or extra summand has a binomial with top below its nonnegative lower index and is zero. At j0=Y0, the possible extra i=0 term when j-Y=1 vanishes because binom(m-2,m-1)=0. The potentially troublesome j-Y=-1 case belongs only to j=g,Y=b+1; its opposite half-space g>b is absent from the legal cone, so that endpoint is never selected. At the upper-cap support wall k=X0+Y0, the true j is X+Y+1, making the sum exactly empty and its endpoint zero. At h=c the second X=-1; endpoint and adjacent boundary terms vanish. These arguments work for m>=3 (and the direct count controls also cover m=2). Nonnegative lower-cap support boundaries are never set to zero by an inaccessible opposite chamber.

Thus ordinary polynomial finite-sum formulas, with their exact constants, apply on each entire closed cone. Shared faces have the same all-integer counts and consequently the same polynomial restriction. They are independently checked coefficient by coefficient below.

## 4. Complete finite fan: no missing magnitude, lattice residue, or ray

The exact construction uses all256 signs of the eight walls and all1001 choices of four rows among the fourteen base/wall rows. Exact rank-four nullspaces give all primitive rays feasible in the base cone. A pointed five-dimensional cell has every extreme ray at such an intersection, so this population is complete. There are16 rays, listed in U05-02 and the certificate tables, and27 full-dimensional cells.

Triangulate each cell by the same global pulling order on its rays. In a nonsimplicial face choose its least ray, recursively triangulate each facet not containing that ray, and cone those simplices from it. This gives30 simplicial cones in total. It covers every cell and induces the same triangulation on each common face. Every five-column ray matrix has determinant+1 or-1; the exact integer inverse is retained. Consequently every nonnegative integral parameter vector belongs to a simplex and has **nonnegative integer** cone coordinates. There are no unexamined cosets or fractional-coordinate omissions.

`DATA/WALL-FAN.json` retains all rows,256 sign population through its construction, the16 rays,27 nonempty full-dimensional cells,30 simplices, signs, determinants and inverse matrices. `NEW/independent_global.py` regenerates nullspaces independently of the producer's signed-minor routine and independently checks the face lattice and pulling rule. Lower-dimensional cells lie in the union of closures and are not discarded as exceptions.

## 5. Exact full-polynomial certificate and independent audit

For a simplex with ray matrix V, write parameter vector p=Vz with z>=0. Let H_V(z) be the whole grade-one count given by(5). Its PRIOR total degree is at most9. All2002 integer points with sum z_i<=9 determine it uniquely by multivariate Newton differences. These values were obtained by the complete band formula(3). The next two complete shells sum z_i=10 or11,2366 points per cone, are UNUSED checks.

Each `DATA/CONE-00.json` through `CONE-29.json` preserves all2002 ordinary mixed coefficient slots, their exact Newton coefficients, all determining and unused integer values, and an explicit literal original preimage at every occurrence. The canonical preimage uses every long width equal to b. Boundary originals with zero rows and terminal output are preserved; they are not counted as new search coverage.

The complete population contains60060 mixed slots:

    24968 positive, 35092 zero, 0 negative.

The independently authored `NEW/independent_symbolic.py` does NOT import producer mathematics. It expands the full binomial products in(4), evaluates exact Faulhaber polynomial sums, and compares every resulting rational coefficient with the certificate. It separately recomputes all60060 determining and70980 unused count occurrences from(4), checks every original preimage, and compares using an independent nested polynomial evaluator. This symbolic expansion independently verifies the asserted degree bound for all thirty pieces; the preceding finite-sum argument supplies its all-m reason.

`NEW/independent_global.py` additionally checks435 pairwise shared-face restrictions, all930 nonempty cone-coordinate supports and193050 derivative slots. The receipts are `AUDIT/INDEPENDENT-CONE-*.json` and `AUDIT/INDEPENDENT-GLOBAL.json`. No floating computation enters this proof certificate. Numerical values on a favorable grid are not the justification for an infinite parameter domain: the exact closed formulas, complete fan and coefficient identities are.

For every legal integer p=Vz, the full stretched original is H_V(tz). Nonnegative mixed coefficients immediately imply ordinary coefficient nonnegativity. The next section supplies strictness and the quantitative reserve, including actual-degree boundaries.

## 6. Actual degree and complete simplex reserve

For b>=c>=1, apply these cases in the displayed order:


```text
If h=b:
    D=0 if g=c;
    D=4 if g<c and k>g;
    D=3 if g<c and k=g.
Otherwise h<b:
    D=4 if b=c=g;
    if k=0: D=6 if b=c, and D=7 if b>c;
    otherwise k>0:
        if b=c: D=7 if k=g, and D=8 if k>g;
        if b>c: D=8 if k=g, and D=9 if k>g.
```

For the c=0 closure with h<b, D=5 if k>0 and D=4 if k=0. When h=b and c=0, D=0. All b=0 cases are the point1.

These are actual degrees, not generic expected dimensions. The potentially easy-to-miss stratum b=c=g,h<b has the exact identity


```text
P(t)=binom((b-h)t+m-1,m-1)                              (7)
```

for every m, since k>=g=b makes the upper R_(kt+1) term vanish and the two-monomial R_bt identity consumes the entire X exponent in(2). At m=5 it has degree4, not7 or8. The initial exploratory degree heuristic missed this stratum; its explicit mismatches remain in `DATA/SUPPORT-RESERVES.json`. The corrected independent support table is `DATA/CORRECTED-DEGREE-SUPPORTS.json`.

Here is a finite but complete proof of every remaining degree and reserve case. For each cone and each of the31 nonempty supports S of its five coordinates, set z=1_S. The exact certificate checks the ordinary polynomial H_V(t1_S), determines its degree, and subtracts binom(t+D,D). All930 resulting coefficient vectors are nonnegative, and all indicated leading coefficients are positive. Every base equality in the degree classification is a nonnegative linear form on the cone, so its vanishing depends only on S, not on the positive magnitudes. Thus the degree classification at1_S is the classification on that whole relative support.

For any nonnegative integer z with support S, every nonzero z_i>=1. Because every mixed coefficient is nonnegative, H_V(tz)>=_c H_V(t1_S). No new monomial support appears and no nonzero top term disappears. Therefore the actual degree stays D and inequality(1) follows. At z=0, H_V(0)=1, which is its own degree-zero reserve. This proves all magnitudes, zero short rows, all overlaps, all ties and every degree drop. The proof does not infer strict high coefficients just from a positive c1 or from the generator below.

## 7. Complete fixed-output overlap generator, with sharp reserves

Differentiate H_V in the physical parameter directions by V^(-1). In every cone all mixed coefficients of -partial_h H_V and -partial_g H_V are nonnegative. Their constant coefficients are at least13/12 and77/60 respectively. Constant terms here are the derivatives of the original c1; the derivative of the original constant1 is zero. Subtracting these constants leaves a nonnegative exact mixed derivative polynomial. The full coefficient maps, including all zeros, are retained in `DATA/DERIVATIVES.json` and independently checked.

Each ordinary t-coefficient is a continuous piecewise polynomial in p on the closed fan. Integrate its appropriate directional derivative along the straight coordinate segments. Shared-wall agreement pays every crossing, including a segment lying on a wall. This yields


```text
P_(b,c,k,h',g')(t)-P_(b,c,k,h,g)(t)
   >=_c [(13/12)(h-h')+(77/60)(g-g')] t,
   h'<=h, g'<=g.                                      (8)
```

Both constants are sharp separately: at (b,c,k)=(3,2,1), reducing h from1 to0 with g=0 gives linear gain13/12; reducing g from1 to0 with h=1 gives77/60. All relevant originals and full exact gain vectors are in `DATA/OPERATION-CONTROLS.json`.

The literal row widths are held fixed in this comparison. Thus T and nu are fixed, not just rank or a rescaled content. The original at maximal legal overlaps h=b,g=min(c,k) has


```text
P_start(t)=binom((c-k)t+3,3) if k<c,
P_start(t)=1                 if k>=c.                 (9)
```

Indeed the first total in(3) is zero and the band either fixes b=kt or b=ct; the second partner is absent. Every family member is reached by decreasing h and then g within the legal domain. Each gain in(8) is a complete original-polynomial difference; a gain is NOT asserted to be itself one affine LR family. This is a paid fixed-output operation on the whole original, not cap-wise positivity of an auxiliary summand.

## 8. Short-row widening, exact saturation, and its fixed-output implementation

Set


```text
k_star=min(b,b+c-h)=b-max(h-c,0).
```

For h<=c, any k>=b is invisible in(2) because the upper R_(kt+1) contribution is killed by the complete highest-weight annihilator. For h>=c the second partner in(3) is zero; the first band's pair sum cannot exceed(b-h+c)t, so k>=b+c-h is redundant. These statements include h=c and prove exact saturation at k_star for every m.

At m=5, every mixed coefficient of partial_k H_V is nonnegative. In each unsaturated full-dimensional cone its constant coefficient is at least1/9; in each saturated cone the derivative is identically zero. The global audit checks all branches, not just a selected k interval. Integration gives, for k2>=k1>=g at fixed b,c,h,g,


```text
P_k2(t)-P_k1(t)
   >=_c [min(k2,k_star)-min(k1,k_star)] t/9.            (10)
```

The constant1/9 is sharp. At b=2,c=1,h=g=1, increase k from1 to2. The linear gain is exactly1/9 and all higher gain coefficients are positive. A fixed-output literal realization uses paired/long widths(2,2,3,2,2,2) before, and(2,2,2,2,2,2) after; the short width rises by one and a long row loses one while remaining at its floor. T and nu remain exactly unchanged.

More generally an increase in k may be paid by equal total decreases among long rows, provided all remain>=b. The count's proved stability under unequal long widths makes(10) an entire fixed-output original operation whenever that slack exists. Without slack it remains a comparison of complete originals with changed T. It is not a claim about arbitrary LR row redistribution or A61's distinct separated C22 cap-splitting operation.

The same audit also gives nonnegative partial_b H_V and a linear rate at least25/12 on this domain. A b comparison changes nu unless additional original modifications are specified. We do not label it a fixed-output operation. Its equality constant is attained on the c=0 closure, a known terminal control.

## 9. A genuine failed extension: increasing c

There are2316 negative mixed entries in the thirty partial_c maps. Negative mixed coordinates alone do not refute physical monotonicity. Here an actual complete original-polynomial difference does:


```text
(b,c,k,h,g)=(2,1,1,0,0) -> (2,2,1,0,0),
all six long widths fixed at2.
```

Both endpoints are legal and their whole polynomials are strictly positive through their actual degrees9 and8. The second-minus-first ordinary vector, through degree9, is


```text
(0,5/6,137/36,1043/144,133/18,2465/576,
 191/144,43/288,-1/48,-1/192).
```

Thus c-increase is NOT coefficientwise monotone in general. The outer/inner shapes are fixed and the content changes. This is a negative **signed gain**, not a negative coefficient in either whole original. Both endpoints were literally checked at grades1,2,3 and reconstructed by two complete auxiliary formulas using the prior bound and unused grades.

## 10. Bare originals, exact controls and evidence ceiling

The frozen new discriminator is


```text
lambda=(24,21,18,16,12,8,4),
mu=(20,17,16,12,8,4,0), nu=(19,4,3),
(b,c,k,h,g)=(4,3,2,1,1).
```

Its prior degree bound is9, from the whole formula and original tableau affine space, before fitting. Its complete ordinary vector is


```text
(1,281/30,14287/360,26759/270,230003/1440,
 15427/90,87871/720,9979/180,20947/1440,181/108).
```

Every bare original grade0..12 was counted. Grades0..9 determine;10,11,12 are UNUSED, equal3825852173,8396558182,17299186281. The first combined job was interrupted after completing grade11, without a final wrapper receipt or observed exit. A separate successful grade12 job completed the vector. Partial data and unknown wrapper cost remain preserved. There is no claim that one uninterrupted thirteen-grade job passed.

A named-terminal check used the retained exact2062 positive Schubert triples; every relevant Horn inequality was strict with minimum slack2. Rank/area/two-row/absorber/old-ratio/separated-family terminals were also checked at their exact hypotheses. This is not an exhaustive classifier for every source theorem.

Thirteen structural/operation parents have complete auxiliary values0..12 from two independent formulas, prior degree9, and unused10..12. For each, only grades1,2,3 were literally counted and compared with the full six-term determinant:39 additional literal calls. Repeated endpoints and terminal controls are retained and are not additive census coverage. Initial discriminator calibration added four literal calls0..3, including repeats. All failed old shift/floor/cap controls remain in the cumulative archive unchanged.

## 11. Exact scope, recovery and follow-on

This proof closes one entire all-ratio, interacting/no-absorber rank-seven family with six long widths above b. It does not close arbitrary original rank seven, m>=6 higher coefficients, four-row interactions, the full compact normal-cycle c9, general mixed negative-shape realization, or unrestricted KTT. U05-02 separately proves a sharp all-rank **linear** theorem; positivity of ray polynomials alone cannot pay arbitrary higher mixed coefficients.

The all-cap whole splitting bridge in A61 remains a distinct structural alternative. No A61 code was executed and its pending gate was not promoted. All new exact data, executable independently authored verifiers, failed degree heuristic, signed-gain failure, original counts and unknown charges are preserved. No whole-negative candidate was found.
