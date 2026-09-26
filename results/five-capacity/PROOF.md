# Whole five-capacity positivity

## Statement and scope

Let 1 <= m <= 5 and let w_1,...,w_m,c,d be nonnegative integers with s = sum w_i >= c+d. The entire polynomial counting

    y_i,z_i >= 0, sum z_i = c t, sum y_i <= d t,
    y_i+z_i <= w_i t

has positive ordinary coefficients through its actual degree, with constant one. A point has polynomial one. There is no area bound, omitted parameter wall or positive-capacity restriction. For the original nine-coordinate m=5 presentation and 2 <= k <= 9,

    [t^k] P(t) >= (1/1000000) sum_(actual k-faces F) vol_Z(F).

The volume has no factorial. Above actual dimension both sides are zero. The separate accepted all-m theorem gives c1 >= d; strictness when d=0 is justified below. No geometric c1 face-volume margin is inferred from that bound.

This is also positivity for the ENTIRE one-overlap LR family with five residual capacities on 0 <= c <= h, u,v >= h+d and s >= c+d. Its constructor below has ordinary rank at most seven and three content parts. It extends the accepted m<=4 family; it does not exhaust rank seven or establish general four-letter rank-six c1/c2.

## Full original polytope and lattice

At m=5 use free coordinates (y_1,...,y_5,z_1,...,z_4) and restore z_5 = c - sum_(i<5) z_i. The complete sixteen outward inequalities are

    -y_i <= 0 (five), -z_i <= 0 (four), sum_(i<5) z_i <= c,
    y_i+z_i <= w_i (i<5), y_5-sum_(i<5)z_i <= w_5-c,
    sum_i y_i <= d.

These are all constraints, with every original offset retained. Projection and restoration are inverse maps of the entire real boundary-equation space and its integer solution lattice. Thus the original lattice is Z9; lower-dimensional faces use the saturated intersection with their rational direction space. Boundedness follows from the coordinate capacities. Nonemptiness follows by distributing c within the w capacities and taking y=0.

For integrality, append a column to the three-row table whose original columns are (z_i,y_i,w_i-z_i-y_i). The appended column is (0, d-sum y_i, sum y_i); row totals are (c,d,s-c), and column totals are (w_1,...,w_5,d). This is exactly the transportation face with first appended entry zero. The inverse forgets the forced coordinates, preserving every integer point and the full affine lattice. The bipartite incidence matrix is totally unimodular, so the transportation polytope and this face have integral vertices. This face representation proves integrality; the whole LR interpretation comes from the independent count identity below.

When all five w_i,c,d are positive, take z_i=c*w_i/s and y_i=eta*w_i, where 0 < eta < min(d/s,1-c/s). Every literal inequality is strict, including when s=c+d. Thus actual dimension nine is attained. The universal bound concerns actual dimension and does not impose this strictness on other parameters. Smaller m is obtained by padding zero capacities in the same complete model.

## Complete local constants and correction

For every independent original normal subset I let N_I be its row matrix, G_I=N_I N_I^T, and L_I=N_I Z9. Every subset through order seven is classified, including the dependent complement. All independent images are Z^I. The primary computes complete maximal-minor image indices; the independent constructor separately verifies an explicit unit minor. Consequently all projected images and primitive quotient divisors have index one, and their full numerators are the singleton zero. A generator permutation identifying the entire Gram matrix therefore identifies both metric and full lattice. No index-only grouping is used.

| q | All subsets | Independent | Dependent | Full types | Minimum raw alpha |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | 16 | 16 | 0 | 4 | 1/2 |
| 2 | 120 | 120 | 0 | 15 | 3/20 |
| 3 | 560 | 555 | 5 | 42 | 1/24 |
| 4 | 1820 | 1755 | 65 | 93 | 9/800 |
| 5 | 4368 | 3977 | 391 | 178 | 50077/9374400 |
| 6 | 8008 | 6570 | 1438 | 282 | 189864769/86004737280 |
| 7 | 11440 | 7830 | 3610 | 347 | -417059/203212800 |

All 26,332 subsets, 20,823 independent values, 5,509 dependent cases and 961 complete types are retained. Two q7 types, representing ten original rows, have negative raw constants. These are auxiliary values, not whole LR negatives.

The local value is the constant term of the complete Berline–Vergne recurrence already stated in the [complete recurrence](proofs/normal-cycle.md). Its covector on a subset T is G_T^(-1) w_T; it keeps every proper-face term. Here each image index and numerator is one. The normalized Todd expansion through q<=7 is

    1/(1-exp(z)) = -1/z + 1/2 - z/12 + z^3/720 - z^5/30240 + O(z^7).

After multiplying by z, the next contribution has degree eight. B7 is zero; B8 is not needed at these orders. The primary exact GMP recurrence and independently frozen Fraction recurrence agree on all 961 constants and every original assignment. Their common classical analytic formula remains a credited premise; separate implementations are not two different analytic theorems.

The q7 field assigns an ambient rational vector g_J annihilating each independent q6 support J. Unlisted supports have g_J=0. Define on EVERY independent original q7 set

    beta_I = alpha_I + sum_(n in I) g_(I without n) dot n.

All primitive divisors are one, proved from full image lattices. The complete unconstrained field has 6,570 supports, 19,710 coordinates and 7,830 rows. Root first found a passing full proposal, then a smaller proposal using supports incident to low rows. Proposal sparsity restricts discovery only; the final inequality check retains every original row and every omitted zero. The final field has 70 nonzero supports. The complete independently checked minimum is

    26684096221433977 / 2668409622144333204480 > 1/1000000.

The independent checker verifies all 54,810 primitive incidences, all support-annihilation equations and all 7,830 corrected values. It reproduces the entire saved vector and retains all 3,610 dependent q7 subsets. Floating solver success is not used as a mathematical premise. The original full proposal remains preserved.

## From the finite certificate to all parameters and boundaries

Apply the complete fixed-normal dual-solid valuation argument from the [normal-cycle proof](proofs/normal-cycle.md) in this ORIGINAL Z9 geometry. For completeness, use a generic outward perturbation only to obtain a compatible simple fan refinement using original normal rays; no Ehrhart coefficient of a perturbed polytope is transferred by continuity. On each q-cone assign the normalized volume of the actual k-face whose normal cone it refines, or zero where there is no such face, with q=9-k. These form the complete refined normal cycle, including nonsimple and lower-dimensional fibers.

At every (q-1)-support the weighted primitive quotient conormals sum to zero: this is lattice facet balance on an actual (k+1)-face, cancellation on internal subdivision boundaries, and zero on larger coarse cones. The BV dual-solid valuation is additive over the full-dimensional pieces. Hence

    c_k = sum_I vol_I alpha_I = sum_I vol_I beta_I.

For q1 through q6 the field is zero and each alpha exceeds 1/1000000. The final q7 field gives that bound for k=2. Every actual k-face contributes a positive-volume refinement cell, proving the stated inequality and strictness for 2 <= k <= actual degree. The top coefficient is normalized volume. Integral vertices were proved above; no rational-vertex or quasipolynomial exception is hidden.

For c1 use [the complete all-capacity linear proof](proofs/linear.md). It gives c1>=d on the entire closed domain. If d>0 this is strict. If d=0, y=0 and the whole count is exactly the 2-by-m transportation polynomial with row margins (c,s-c) and columns w. The separately published [complete 3-by-5 transportation theorem](../transport-capped/README.md) gives strict positivity through actual degree, including zero-row/column deletion. Its [complete proof and finite certificate](../../tooling/transport_certificates/README.md) are an explicit prerequisite at this boundary. Thus c1 is also strictly positive whenever the original family is nonconstant. Constant one follows from integral nonempty Ehrhart counting. No q8 arithmetic or unproved B8 extension is used.

## Entire ordinary LR lift

Put U=u+v and use suffix_i(w)=sum_(j>=i) w_j. Define

    lambda=(s+U-h,s+v,suffix_1(w),...,suffix_m(w)),
    mu=(s+v-h,s,suffix_2(w),...,suffix_m(w),0),
    nu=(U+s-h-d-c,h+d,c).

All partitions are nonnegative, dominant and balanced when 0<=c<=h, u,v>=h+d and s>=c+d. The exact top-pair character is

    h_(ut)h_(vt) - h_((U-h)t+1)h_(ht-1)
      = sum_(k=ht)^min(ut,vt) s_(Ut-k,k).

Schur adjunction and containment leave exactly k=ht+j, 0<=j<=dt. The residual three rows have lengths (s-c-d)t+j, dt-j and ct. They are column-disjoint under the displayed inequalities. Their weight multiplicity counts all x_i,y_i,z_i>=0 with x_i+y_i+z_i=w_i*t, sum z_i=ct, sum y_i=dt-j. Summing every j is bijective with the full cap count; j is the unique slack. Every original offset and every point is retained. Empty rows and zero boundaries satisfy the same formulas. This proves equality of the entire ordinary LR polynomial, not a face polynomial or a partial character. Ordinary rank is at most m+2, hence seven; no rank compression is inferred.
