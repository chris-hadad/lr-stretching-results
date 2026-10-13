# U01-01. A uniform whole-polynomial reserve for two capped residual pairs at rank seven

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

**Status:** PROVED in this return by the argument and finite exact rational certificate below, conditional on the A58 complete original/count theorem. This is not a claim of campaign adoption, human review, proof-assistant certification, or worldwide priority. The finite computations are part of a complete parameter-independent proof, not a finite parameter panel.

## 1. The original family and the conclusion

All parameters in this section are integers. Let

```math
k=(\kappa,\eta,k_3,k_4,k_5),\quad K=\sum_{i=1}^5 k_i,\quad \sigma_i=\sum_{j=i}^5 k_j,
```
where every cap is nonnegative and $`k_5>0`$. Assume

```math
b\ge c\ge1,\quad 0\le h\le b,\quad u,v\ge b,\quad d=K-c\ge0,\quad k_3,k_4,k_5\ge d.
```
Put $`p=b-h\ge0`$ and $`\delta=b-c\ge0`$. Form the **literal original**

```math
\begin{split} \lambda&=(K+u+v-h,K+v,\sigma_1,\sigma_2,\sigma_3,\sigma_4,\sigma_5),\\ \mu&=(K+v-h,K,\sigma_2,\sigma_3,\sigma_4,\sigma_5,0),\\ \nu&=(u+v+K-b-c,b,c). \end{split}                                                    \tag{1}
```
These are legal partitions with containment and size balance. In particular, the first two differences in $`\lambda`$ and $`\mu`$ are controlled by $`u-h\ge0`$, $`v-h\ge0`$, and the nonnegative suffix sums. The first content part is $`u+v+d-b\ge b`$. The last outer part is $`k_5>0`$, so the maximum trimmed original rank is **seven**, including zero interior caps.

Let $`P(t)=c^{t\lambda}_{t\mu,t\nu}`$. When $`d=0`$, $`P(t)=1`$. When $`d>0`$, let

```math
E=3+\mathbf1_{\kappa>0}+\mathbf1_{\eta>0},\qquad D=\begin{cases} E-1,&p=0,\\ 2E-2,&p>0,\ \delta=0,\\ 2E-1,&p>0,\ \delta>0. \end{cases}                                                     \tag{2}
```
Then $`D`$ is the actual degree, and the following **ordinary monomial coefficientwise** inequality holds:

```math
\boxed{\quad P(t)\ \succeq_c\ 1+\frac7{10}\binom{t+D-1}{D}.\quad} \tag{3}
```
Here $`f\succeq_c g`$ means every coefficient of $`f-g`$, in the ordinary powers of $`t`$, is nonnegative. Thus $`P`$ is strictly positive in every degree from zero through its actual degree. In the all-positive regime $`d,p,\delta,\kappa,\eta>0`$, the stronger reserve is

```math
P(t)\succeq_c1+\frac{121}{140}\min(d,\kappa)\binom{t+8}{9}.        \tag{4}
```
This covers arbitrary magnitudes, ties, integer scalings, and all the zero cases in (2), not just $`d=3`$ or the two new originals counted in this unit. The other three cap magnitudes disappear because their pair bounds are redundant under the total $`dt`$; this is exact redundancy, not cap-parameter monotonicity. The nonabsorber caps may be relabeled before forming (1). In particular, the result applies whenever an absorber has cap at least $`d`$ and at most two other caps are below $`d`$, provided the literal family has five isolated widths.

**Scope exclusions.** This theorem does not sign arbitrary rank-eight-or-higher two-cap families, three or more genuinely small nonabsorber caps, no-absorber originals, adjacent/triple-overlap originals, or arbitrary rank-seven LR polynomials. It is not an LR negative witness. No face metric, normal-cycle weight, or hive-face isometry is transported by the count map.

## 2. Accepted premise: the full original, with both once-only shifts

The load-bearing accepted input is

`S/methods/astra058-2026-09-27/root-science/COUPLED-PROOF.md`, Section 1,

whose exact identity is in the accompanying source receipt. It proves the whole original/count equality and actual degree for arbitrary $`a`$, not a general sign theorem for interacting caps. A58's Section 3 signs one small cap only. The new sign argument here is not inferred from that one-cap result.

For the literal original, put
$`\Phi=\prod_i h_{k_it}(1,x,y)`$. The complete character expression is

```math
P(t)=[x^{pt}y^{ct}]\frac{\Phi}{1-x}      -[x^{bt+1}y^{(c-h)t-1}]\frac{\Phi}{1-y}.                    \tag{5}
```
Both affine offsets occur **once**. Complementing the first exact total gives pairs $`(U_i,Z_i)`$ with total $`dt`$, aggregate $`U`$-bound $`pt`$, and all pair caps. Complementing the second exact total gives total $`(d-\delta)t-1`$ and aggregate bound $`(p-\delta)t-1`$. Adding $`\delta t+1`$ to the absorber coordinate $`U_5`$ maps this second domain injectively onto the first-domain points with $`U_5\ge\delta t+1`$. Its inverse subtracts the same integer. The absorber cap is paid because $`k_5\ge d`$. Negative second-domain bounds give the empty image. Consequently the **entire original** is

```math
\begin{gathered} U_i,Z_i\ge0,\qquad \sum_{i=1}^5(U_i+Z_i)=dt,\\ \sum_{i=1}^5U_i\le pt,\qquad U_5\le\delta t,\\ U_1+Z_1\le\kappa t,\qquad U_2+Z_2\le\eta t.                      \end{gathered} \tag{6}
```
The other pair caps are automatic. This preserves the lattice, ties, affine offsets, and zero fibers. A58 proves integrality in the saturated residual lattice and gives exactly (2). No degree is inferred from observed interpolation agreement.

## 3. An exact simultaneous-cap coordinate order

There is an all-$`a`$ version of the following map, useful beyond this rank-seven theorem. When only caps 1 and 2 can be active and $`a\ge3`$, order the $`2a`$ residual increments as

```math
Z_1,U_1,U_3,\ldots,U_{a-1},U_a,U_2,Z_2,Z_3,\ldots,Z_a.
```
Take cumulative sums $`x_1,\ldots,x_{2a-1}`$, eliminating the final total. The inverse takes consecutive differences and finally $`Z_a=dt-x_{2a-1}`$. After the primitive total equation is eliminated, both maps are integral triangular maps with determinant one. The exact constraints become

```math
\begin{gathered} 0\le x_1\le\cdots\le x_{2a-1}\le dt,\qquad x_2\le\kappa t,\\ x_{a+1}-x_1\le pt,\qquad x_a-x_{a-1}\le\delta t,\qquad x_{a+2}-x_a\le\eta t.                                         \end{gathered} \tag{7}
```
The aggregate budget becomes a longer interval; it has **not** been omitted or treated as an independent flag. At $`a=5`$, there are nine cumulative coordinates and three interval rows

```math
(1,6,p),\quad(4,5,\delta),\quad(5,7,\eta).                     \tag{8}
```
A row $`(i,j,w)`$ means $`x_j-x_i\le wt`$. This is a complete unimodular count representation for all $`a\ge3`$ under the stated cap redundancy. Positivity below is proved only for $`a=5`$.

If an interval width is zero, identify every coordinate from its left endpoint through its right endpoint **before** introducing bands. If $`\kappa=0`$, identify $`x_1=x_2=0`$. If $`d=0`$, every coordinate is zero. These are primitive equalities between consecutive coordinates, so the quotient lattice is the full integer lattice in the surviving coordinates. Positive residual flags remain positive after collapse, possibly becoming flags from coordinate zero. The number of free coordinates is precisely (2). The complete sixteen-regime audit in Section 6 independently verifies these collapses.

## 4. A finite band decomposition valid for every parameter value

For $`t\ge1`$, write each positive free coordinate uniquely as

```math
x_i=(\beta_i-1)t+v_i,\qquad 1\le v_i\le t,
```
and use $`\beta_i=0`$ for a coordinate fixed at zero. The sequence $`\beta`$ is weakly increasing. It obeys the integer upper flags and, for each surviving positive-width interval, $`\beta_j-\beta_i\le w`$, with $`\beta_0=0`$. This is a finite population independent of $`t`$.

Within a positive equal-band block, the $`v`$'s form a weak chain. For an interval with positive left band, strict inequality $`\beta_j-\beta_i\lt w`$ is automatic for every choice of remainders; equality imposes the additional comparison $`v_j\le v_i`$. If its left band is zero, the interval is only the upper band restriction $`\beta_j\le w`$; no extra comparison is imposed. These assertions follow by substituting the displayed formula and using $`-(t-1)\le v_j-v_i\le t-1`$. A band difference greater than $`w`$ cannot be repaired by the remainders.

The resulting comparison relation is a poset: every cross-band comparison goes toward a strictly smaller band; comparisons within one band run in coordinate order. Let $`Q_\beta`$ denote it. The count of its weak order-preserving maps to $`\{1,\ldots,t\}`$ is its order polynomial $`\Omega_{Q_\beta}(t)`$. It is **not** $`\Omega(t+1)`$. Thus

```math
P(t)=\sum_{\beta\text{ admissible}}\Omega_{Q_\beta}(t).          \tag{9}
```
This identity holds at every positive integer $`t`$, hence as polynomials; the polynomiality and degree bounds also follow directly from the next elementary identity. The sole empty poset, the all-zero band assignment, contributes exactly one. Every nonempty band poset has constant coefficient zero.

For a poset $`Q`$ with $`n`$ elements let $`s_j(Q)`$ be the number of strict chains of order ideals

```math
\varnothing=I_0\subsetneq I_1\subsetneq\cdots\subsetneq I_j=Q.
```
Choosing the $`j`$ attained values of a weak map gives the all-$`t`$ identity

```math
\Omega_Q(t)=\sum_{j=0}^{n}s_j(Q)\binom{t}{j}.                  \tag{10}
```
This proves degree at most $`n`$ before any reconstruction. The $`s_j`$ are exact integers, computed by enumerating ideal subsets and strict inclusions. A second implementation uses natural-label linear-extension descents. The standalone audit instead counts weak maps by subset-zeta iteration at $`0,\ldots,n+2`$; only $`0,\ldots,n`$ determine the polynomial under (10), and the last two grades are unused checks. It imports neither producer's mathematics nor any floating optimizer.

## 5. Complete type coverage, not a bounded width experiment

Actual positive band values matter for admission, but $`Q_\beta`$ depends only on the zero prefix, the ordered partition of the positive tail into equal-band blocks, and which of the surviving interval rows are active. Normalize the distinct positive band values to $`1,\ldots,r`$. For each zero/positive regime, generate the following **superclass**:

```
for z = 0,...,n:
    for each ordered composition (m1,...,mr) of n-z:
        levels = z zeros followed by m1 ones, m2 twos, ..., mr copies of r
        eligible = interval rows (i,j) with 0 < levels[i] < levels[j]
        for each subset A of eligible:
            add the equal-block chain edges and v_j <= v_i for (i,j) in A
            compute the complete order polynomial using (10)
```

Coordinate zero has level zero. Impossible combinations of widths and active rows may be included; this only makes the certificate stronger. Every actual admitted band state is included, for arbitrary nonnegative integer parameters. Upper flags restrict admission but cannot create another poset type. This is why the subsequent finite calculation proves a uniform theorem rather than positivity on a width grid.

For all four widths positive the class has **1,964 types**, **1,952 distinct labeled posets**, and **284 distinct connected factors**. There are **31 types with a negative ordinary coefficient**. Every such type has all nine coordinates positive and has the budget row $`(1,6)`$ active. Negative coefficients of the whole type polynomials occur only in degrees 1, 2, or 3. The connected-factor list has 26 negative factors; their negative coefficient is linear. These different counts are deliberately not conflated.

Bandwise positivity is false. For example, normalized levels
$`(1,1,1,2,3,3,3,3,3)`$ with active rows $`(1,6),(4,5)`$ have $`[t]\Omega=-1/180`$. This band occurs in the supplied $`(\kappa,\eta,d,p,\delta)=(1,1,3,2,1)`$ original. It is a band contribution, not an ordinary LR counterexample. The whole original is positive. A new grouping argument must pay these negative contributions.

## 6. Zero parameters and the complete finite roster

In this table the four bits mean positivity of $`(p,\delta,\kappa,\eta)`$; a zero bit denotes equality to zero, not a small positive value. Always $`d>0`$. The quotient dimension $`n`$ equals (2).

| Positive mask | n | Complete types | Types needing payment |
|---|---:|---:|---:|
| 0000 | 2 | 4 | 0 |
| 0001 | 3 | 8 | 0 |
| 0010 | 3 | 8 | 0 |
| 0011 | 4 | 20 | 0 |
| 0100 | 2 | 4 | 0 |
| 0101 | 3 | 8 | 0 |
| 0110 | 3 | 8 | 0 |
| 0111 | 4 | 20 | 0 |
| 1000 | 4 | 16 | 0 |
| 1001 | 6 | 100 | 0 |
| 1010 | 6 | 92 | 0 |
| 1011 | 8 | 648 | 3 |
| 1100 | 5 | 44 | 0 |
| 1101 | 7 | 296 | 0 |
| 1110 | 7 | 280 | 7 |
| 1111 | 9 | 1,964 | 31 |

There are **3,520 total types**. The standalone audit regenerated their entire key sets, their primitive quotients, and their complete polynomials, using **2,340 cached distinct poset polynomials** across all regimes. The all-zero-total case $`d=0`$ is the direct point argument, not another enumerated width case. Full type records and exact arithmetic are retained in `FACTOR-CLASS.json`, `BOUNDARY-CLASS.json`, and `INDEPENDENT-CERTIFICATE-AUDIT.json`.

## 7. Injective contractions of several band gaps

Let a bad actual band state have distinct positive values
$`B_1\lt \cdots\lt B_r`$ and gaps $`g_h=B_{h+1}-B_h>0`$, $`1\le h\lt r`$. Let $`\ell_i\in\{1,\ldots,r\}`$ be its normalized levels. Choose a subset $`J`$ of gaps. Define

```math
\beta'_i=\beta_i-\sum_{h\in J,\ h<\ell_i}g_h.                 \tag{11}
```
The operation merges the selected neighboring blocks. It decreases coordinates and cannot increase an interval difference. Therefore every original upper flag, aggregate bound, and cap bound remains satisfied. It leaves the smallest positive band unchanged. An active row $`e=(i,j)`$ remains active exactly when none of the removed gaps lies between its endpoints; every other previously active row becomes strict. A previously strict row stays strict. These facts show that (11) has exactly the target type recorded in the certificate, with no unrecorded active edges.

For each source active row define the incidence matrix

```math
A_{e,h}=\mathbf1_{\ell_i\le h<\ell_j},\qquad h\in J.            \tag{12}
```
Only contractions whose selected columns are linearly independent are used. The certificate supplies an exact nonzero square minor; all the selected minors here are units. Given a target actual band vector and the fixed original widths, the removed gaps must satisfy

```math
\sum_{h\in J}A_{e,h}g_h=w_e-(\beta'_j-\beta'_i)                \tag{13}
```
for each original active row. Independence gives at most one solution. Equation (11) then reconstructs the original vector uniquely. Hence **for a fixed source type and a fixed certified contraction, every actual target band has at most one preimage**. This injectivity statement is parameter-uniform. It does not assume that every formal source type is realizable or that an inverse always gives positive gaps; such failures only reduce the actual demand.

Every used positive-regime contraction removes a gap across the long budget row. Its target has inactive budget and is coefficientwise nonnegative by the complete type calculation. Boundary contractions have the analogous property after primitive collapse. This is a map on band populations used to control multiplicity, not a claim that their remainder polytopes are integrally equivalent.

## 8. Exact fractional payment and the surviving reserve

For each bad source type $`q`$, write its coefficientwise negative part as

```math
N_q(t)=\sum_{j\ge0}\max\{- [t^j]\Omega_q,0\}\,t^j.
```
The positive-width certificate assigns nonnegative rational weights $`\alpha_e`$ to selected contractions out of $`q`$, with

```math
\sum_{e\text{ out of }q}\alpha_e=1.                           \tag{14}
```
For every used good target type $`s`$, the exact certificate verifies

```math
\Omega_s(t)-\sum_{e\text{ into }s}\alpha_e N_{q(e)}(t) \ \succeq_c\ \frac{121}{140}\Omega_s(t).                       \tag{15}
```
It has **48 positive rational weights**, covering all **31 bad types**, into **30 used good target types**. The weights have denominators at most 420. There were 146 eligible candidate contractions into 84 possible target types; unused candidates are not needed for the proof. The fixed rational weights, source and target levels, active rows, selected gaps, unit minors, full polynomials, and coefficientwise remainders are printed in the companion certificate tables and encoded in `MULTIGAP-MERGE-RESERVE.json`.

A floating linear program was used only to discover a candidate allocation. Its reported margin is not a proof. The exported rational weights were then checked with `Fraction` arithmetic; a separate implementation regenerated all source/target posets and checked every coefficient, weight sum, and minor. The exact minimum retained ratio is $`121/140`$, explicitly asserted by the final standalone verifier. No optimizer is imported by that verifier.

For any fixed actual good target band, injectivity from Section 7 bounds the actual incoming payment by the sum in (15): at most one source band per certified edge. Each actual bad band has its whole negative part distributed by (14). Subtracting these debts leaves at least the displayed fraction of every good target polynomial, and the nonnegative parts of bad polynomials remain available. Unused good types retain their entire polynomial. Thus the uniform bound is on the **sum over the complete original**, not on a negative term in isolation.

Two boundary regimes need payment. With $`\delta=0`$ and $`p,\kappa,\eta>0`$, the quotient has dimension eight, with active rows $`(1,5),(4,6)`$ for each of its three bad types. With $`\eta=0`$ and $`p,\delta,\kappa>0`$, it has dimension seven, with active rows $`(1,5),(4,5)`$ for each of its seven bad types. For either regime, remove gap 1 and the gap at the level of the second row's left endpoint. The two-column active incidence matrix is

```math
\begin{pmatrix}1&1\\0&1\end{pmatrix}.
```
Both rows become inactive, and the target is a union of chains. Assign weight one. The exact certificate groups all resulting preimages into three target types in the first regime and five in the second. It proves

```math
\Omega_s-\sum_{q\text{ into }s}N_q\succeq_c\frac7{10}\Omega_s. \tag{16}
```
The exact minimum ratio across these groups is $`7/10`$. `BOUNDARY-MERGE-RESERVE.json` contains all ten source types, their contractions, the eight grouped target records, and full rational reserves. The standalone verifier checks complete coverage of the negative types, the displayed determinant, target type membership, and all coefficients. In each of the other thirteen zero regimes, every type polynomial is coefficientwise nonnegative by the complete finite calculation. This includes, but does not need to invoke, the already accepted one-small-cap cases.

Equations (14)–(16), injectivity, and complete type coverage prove nonnegativity uniformly on the entire domain of (1).

## 9. Strictness and the quantitative bounds

Suppose $`d>0`$, and perform all primitive zero collapses. Put all $`D`$ free coordinates in the first positive band. Every surviving interval has positive integer width and therefore admits this state; every surviving flag admits band one. Its remainder poset is a single chain with polynomial

```math
W_D(t)=\binom{t+D-1}{D}.
```
This good type retains at least $`7/10`$ of its polynomial by the preceding payment proof. The unique all-zero band contributes one and is never charged, because every bad type and every contraction target used for payment has all its free coordinates positive. Every remaining contribution after payment is coefficientwise nonnegative. This proves (3). The product $`W_D=t(t+1)\cdots(t+D-1)/D!`$ has positive coefficients in every positive degree through $`D`$, while $`P(0)=1`$, establishing strictness. The degree equals (2), both from the accepted whole-count premise and from the dimension of the primitive chain quotient; the strictly positive leading term also witnesses that this bound is attained.

In the all-positive regime, all nine coordinates may occupy any single positive band from 1 through $`\min(d,\kappa)`$. These are distinct admitted good states, each with polynomial $`W_9`$, and each retains at least $`121/140`$. This proves (4). No upper-flag monotonicity or cap-parameter monotonicity is needed or claimed.

## 10. Independent original checks and counter-controls

The theorem is not extrapolated from these examples. They are independent checks that the complete original, both character partners, the residual model, the band decomposition, and the coefficient conventions coincide.

The three frozen rank-seven originals have $`(d,p,\delta)=(3,2,1)`$, caps $`(\kappa,\eta,3,3,3)`$, and $`(\kappa,\eta)=(1,1),(1,2),(2,2)`$. Their original partitions and exact ordinary vectors are in the unit report and `A-pair-*-bare.json`. Prior actual degree is nine. Every grade 0 through 12 was counted by the authenticated **bare-original** tableau engine. Grades 0 through 9 determine each polynomial; 10, 11, 12 are unused positive holdouts. All 39 original counts agree with the independently authored residual arithmetic, complete complementary partner difference, and exact band polynomial. The direct character partners were also checked at grades 1, 2, and 3.

The known $`(1,1)`$ control was replayed, not counted as a new original. The two other originals are finite new computations in this return, not campaign adoption or an enlarged census. All three coefficient vectors are positive. A complete strict-Horn screen for these originals is retained with its original Schubert populations; no terminal conflict occurred.

The final independent certificate audit checked all 3,520 types, all rational allocation edges, both boundary certificates, and all three original polynomials. Additional fixed controls checked 83,600 weak-composition coordinate tuples across the sixteen zero regimes; 144 nonunit-gap inverse examples; and both wrong once-only-offset variants on the three same originals. Those are map and implementation controls, not another whole-original search panel. At grade two the correct whole values are 2,902, 3,431, 3,973; omitting the offset gives 2,584, 3,092, 3,613, while replacing it by two gives 2,993, 3,524, 4,068. None is substituted for the correct value.

## 11. Failed approaches and what remains open

Bandwise positivity fails exactly as described in Section 5. A proposed first-gap merge with fivefold whole-source payment failed on 20 of the 31 bad types. Some first-gap targets have zero coefficients in degrees that need payment, so that individual target cannot pay the source's negative part by any scalar. An attempted single-target assignment and a single-gap fractional discovery program did not yield the needed reserve. The latter numerical infeasibility report is retained as a failed discovery attempt, **not** promoted to an exact Farkas no-go theorem. Allowing several gaps, proving injectivity through the active-width incidence matrix, and splitting negative parts rather than demanding a whole-source pairing produced the successful proof.

The all-$`a`$ coordinate map (7) survives beyond this theorem, but its finite poset class grows and the present certificate does not apply there. Higher rank, more active cap pairs, no absorber, interacting overlaps, full normal-cycle weights, and entire negative-shape realizations remain questions outside this theorem at their exact stated scopes. A finite positive panel would not establish the theorem; the uniform injection-and-reserve proof supplies its complete parameter-independent justification.

## 12. Exact certificate and portable checking

The complete [factor-class roster](../../data/absorber/FACTOR-CLASS.json), [zero-regime roster](../../data/absorber/BOUNDARY-CLASS.json), [positive-width allocation](../../data/absorber/MULTIGAP-MERGE-RESERVE.json), [boundary allocation](../../data/absorber/BOUNDARY-MERGE-RESERVE.json) and [readable certificate tables](U01-01-CERTIFICATE-TABLES.md) are included. The [module source map](../../SOURCE-MAP.json) authenticates their full current bytes and original provenance.

From the repository root, run:

```sh
python3 -B verification/check_recent_sources.py --module overlap-families
python3 -B results/overlap-families/code/reproduce_absorber.py --out /path/to/new-absorber.json
```

The trusted root checker verifies the full type generation, rational allocations, capacities, zero regimes and coefficientwise charging; it also recounts the frozen original fixtures. Byte authentication alone does not prove the original/count premise, band identity, exhaustive type generation, injective gap recovery or charging argument. Finite rational verification and the unbounded mathematical proof have distinct roles.

The conclusion is whole-original uniform strict positivity with reserve (3), within the displayed domain. It is not a negative LR candidate.
