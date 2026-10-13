# U04-01 — Complete three-row-block character with adjacent and triple overlaps

Curated mathematical proof from **Pro048/A66 accepted dependency**. The corresponding accepted scope
is stated in the module guide; [the source map](../../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

**Status: PROVED in this return.** This is an all-rank identity for the entire original LR count, not a general coefficient-sign theorem or a generic hive metric/lattice isomorphism. The highest-weight identity and long-factor annihilator already appear in the accepted A58 bridge. The new step here is their complete application to the interacting three-row block, including the two triple-column determinant terms. No absorber is assumed.

## 1. Original hypotheses and literal construction

Let m>=2, b>=c>=1, k>=0, u,v>=b and w_1,...,w_(m-1)>=b be integers. Choose


```text
0<=h<=b,       0<=g<=min(c,k).
```

The row widths are d=(u,v,k,w_1,...,w_(m-1)), and adjacent overlaps are e=(h,g,0,...,0). There are n=m+2 physical rows. Define backwards


```text
lambda_n=d_n,
lambda_i=lambda_(i+1)+d_i-e_i,
mu_i=lambda_i-d_i,
T=sum_i d_i,          nu=(T-b-c,b,c).
```

All overlaps are at most both adjacent widths, so lambda and mu are partitions, containment holds, and |lambda|-|mu|=|nu|. Also T>= (m+1)b+k, giving nu_1>=mb+k-c>=b. The last width is positive, so the maximum trimmed original rank is n, even when k=0 is an interior zero skew row. All three original partitions scale homogeneously.

The first three rows can have a genuine triple-column interval of length max(0,h+g-v). No formula for separated pairs is applied to this block. Every remaining row is column-disjoint from the block and the other remaining rows.

Nonemptiness can be established directly. Set j=max(h,c). At grade one take row multiplicities (number of 1s,2s,3s)

    row1: (u,0,0),
    row2: (v-j,j,0),
    row3: (k-g,0,g),
    row4: (w_1-(b-j)-(c-g), b-j, c-g),
    later rows: (w_i,0,0).

All entries are nonnegative because j>=c and w_1>=b. Column strictness follows from j>=h and the exact second overlap g; the potential triple columns receive 1,2,3. Ballot prefixes hold because u>=j, j>=c>=g, and before row4 the number of 1s is u+v-j+k-g>=b. The 3s of row4 see at least c preceding 2s in total after row3's g threes, and its 2s never overtake the preceding 1s. Scaling this filling proves nonemptiness at every positive grade. Consequently the polynomial's zero convention is P(0)=1.

## 2. Exact highest-weight elimination, not weightwise elimination

Write H_j=h_j(1,X,Y), with H_j=0 for j<0. Put D=(1-X)(1-Y), and for j>=0 define


```text
R_j=h_j(X,Y)-XY h_(j-1)(X,Y),       R_0=1.
```

Finite geometric sums give


```text
D H_L=1-R_(L+1),
(1-Y/X)R_j=X^j(1-Y)-X^(-1)Y^(j+1)(1-X).
```

For B>=C>=0 and a nonnegative-exponent formal series A, the entire coefficient `[X^B Y^C](1-Y/X)R_j A` is zero when j>B. Both monomials in the second identity vanish separately. Coefficients of A need not have a sign.

Thus an H_L with L>=B can be replaced by 1/D **inside that complete highest-weight extraction**, with all other factors retained. The error is R_(L+1)/D and is annihilated. This is not equality of individual weights or characters.

The full three-letter highest-weight identity is


```text
c^lambda_(mu,(A,B,C)) = [X^B Y^C] D(1-Y/X) s_(lambda/mu)(1,X,Y).
```

It applies to the full homogeneous skew character and the dominant, size-balanced output, not a selected Schur sector.

## 3. Retain all six determinant terms before cancellation

At stretch t the complete first-three-row Jacobi--Trudi matrix is

    [ H_(ut)                    H_((u+v-h)t+1)        H_((u+v+k-h-g)t+2) ]
    [ H_(ht-1)                  H_(vt)               H_((v+k-g)t+1)     ]
    [ H_((h+g-v)t-2)            H_(gt-1)             H_(kt)              ].

The +1,-1,+2,-2 occur ONCE. The bottom-left entry must not be discarded when the triple interval is positive. At t=0 the same negative-index convention applies.

Let A=H_(ht-1), B0=H_(gt-1), C0=H_(kt), and E=H_((h+g-v)t-2). All five remaining matrix entries have index at least bt under the stated width/overlap floors. After valid complete-extraction replacement, the six determinant terms are


```text
C0/D^2 - B0/D^2 - A*C0/D + E/D^2 + A*B0/D - E/D^2.
```

The two E terms cancel. Their cancellation is an equality of their complete highest-weight contributions under the long-width hypotheses; they do NOT cancel as raw characters. The result factors as


```text
(C0-B0)(1-D*A)/D^2 = R_(ht)(H_(kt)-H_(gt-1))/D^2.
```

Each of the m-1 remaining long rows contributes another 1/D inside the same extraction. Therefore the entire original polynomial is, for every nonnegative integer t,


```text
P(t)=[X^(bt)Y^(ct)]
      (1-Y/X) R_(ht) (H_(kt)-H_(gt-1)) / D^m.        (1)
```

Equivalently,


```text
P(t)=[X^(bt)Y^(ct)]
      (1-Y/X) R_(ht)(R_(gt)-R_(kt+1)) / D^(m+1).     (2)
```

This proves stability under arbitrary unequal changes of u,v,w_i within their floors. Such changes alter nu_1 through the original constructor; they do not keep the original output fixed. The signs of the ordinary coefficients in this all-parameter identity are NOT proved here.

## 4. Both affine-shifted partners and the retained band

For nonnegative X,Y and 0<=L<=K define the integer count


```text
F_m(X,Y;L,K)=
  sum_(a,b>=0; L<=a+b<=K; a<=X,b<=Y)
    binom(X-a+m-1,m-1) binom(Y-b+m-2,m-2).
```

If either total is negative, the count is zero. These binomials count complete weak compositions, including all zero totals. There is no change of lattice or residue: each summation and composition coordinate is an integer and both total equations have a unit coefficient.

Applying the exact two-monomial identity for R_(ht) to (1), and swapping X,Y in the second symmetric band factor, gives


```text
P(t)=F_m((b-h)t,ct;gt,kt)
      -F_m((c-h)t-1,bt+1;gt,kt).                    (3)
```

This is the ENTIRE original count. The second count is genuinely absent only when its first total is negative. At h=c it is absent because that total is -1, not because a negative-slope polynomial has been continued. The first and second partners carry the SAME band gt<=a+b<=kt. Removing g changes the original. Omitting or stretching the once-only endpoints changes the answer.

No positive integer injection between these partners, generic original hive isometry, or all-parameter sign rule is asserted. The two composition domains individually have at most 2m-1 free coordinates; with the accepted original polynomiality premise this also gives a prior polynomial degree bound 2m-1. The separate literal tableau argument in PRIOR-DEGREE-AND-DOMAIN.md gives the same bound from n=m+2 original rows, without this formula.

## 5. Exact controls and failed shortcuts

The three Phase0 originals at (b,c,k)=(3,2,1), m=5 and (h,g)=(1,0),(1,1),(3,1) were independently counted from bare original tableaux at EVERY grade0..12. Grades0..9 determine under the prior dimension bound;10,11,12 are unused. The complete polynomials have actual degrees9,8,3 respectively. The full six-term determinant was independently evaluated at grades0..3, and 36 further fixed structural grade occurrences retain unequal long widths, the long-floor boundary, a triple interval appearing/disappearing, zero short rows and general-m controls. These checks are evidence for implementation; Sections1–4 are the all-parameter proof.

At the no-absorber control, grade2 has whole count5496. Omitting the Weyl offsets gives3591; stretching them gives6631; erasing the short cap gives6840. The offset-stretching error agrees at grade1, so a single grade cannot detect it. At the adjacent control, removing the second overlap gives205 instead of90 at grade1.

At the triple control's grade2, the two triple determinant terms contribute +3150 and -3150; the complete result is10. Omitting only the positive term produces -3140, a deliberately invalid formula, NOT an original-negative candidate. Both original terms are retained before the exact cancellation proof.

The floors are consequential. A legal control with one long row of width2<b=3 has true grade1 count200 rather than the invalid reduced value205. Lowering the paired v to2 gives191 rather than205. These reject the unsupported floor relaxation, not the entire interacting-overlap method.

## 6. Scope and attribution

The basic highest-weight/annihilator identities are explicit accepted A58 premises and are rederived above. The original one-overlap control was already supplied at unadopted source/control scope. The new result is the full interacting three-row determinant reduction and its exact count language. It uses no A58 absorber where d exceeds every cap, no separated-pair surrogate, no A59/A60 all-deficit sign extrapolation, and no inaccessible Pro047 work. U04-02 supplies a separate complete sign certificate only for its stated rank-seven three-parameter specialization. All other magnitudes/ranks remain unsigned by this proof.
