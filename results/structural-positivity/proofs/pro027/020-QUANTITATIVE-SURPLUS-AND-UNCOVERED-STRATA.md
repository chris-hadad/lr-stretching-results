# Complete quantitative surplus control without first-interior coverage

Originating claims FR027-P05-T004 and T005; the two-row family, lattice, degree and codegree are those of proof019. The inherited general surplus theorem only protects residual degree at most four. Here d-q+1 is unbounded, and a full family-specific coefficient bound is proved. Positive surplus alone is never used to deduce positivity of the parent.

## 1. Exact true-interior and surplus polynomials

Let d=n-2>=3, q=floor(n/2), u=#unit weights and P=B_d(2t)-u C_d(t). Integer reciprocity in the complete saturated GT model gives, for j>=1,

    I(j)=binom(2j-1,d)-u binom(j,d).                  (1)

This agrees with the strict-coordinate construction in proof019, including all zero grades before q. For t>=0 put S(t)=I(q+t)-P(t), M(t)=(I(q+t)+P(t))/2 and D(t)=binom(t+q,d). Then

    d odd:  S=u(C_d-D);
    d even: S=A_d+u(C_d-D),
              A_d(t)=binom(2t+d,d-1).               (2)

At odd d, 2q-1=d; at even d, 2q-1=d+1, and Pascal's identity gives the extra A_d. Omitting this parity term would already give the wrong first-interior type. The complete relation is P=M-S/2.

## 2. Absolute-root domination controls every shifted-binomial coefficient

Both C_d and D have the factor t. The remaining constant factors of C_d are1,2,...,d-1. Those of D are q,q-1,...,q-d+1 with zero removed. For the present q, arrange their absolute values increasingly as r1,...,r_(d-1). Each r_i<=i: the multiset consists of1..q together with1..(d-q-1), so repetitions can only lower the ordered list relative to1..d-1. The triangle inequality for elementary symmetric sums now proves

    |[t^j]D| <= [t^j]C_d, every j.                  (3)

Thus C_d-D and C_d+D are BOTH ordinary-nonnegative. In particular S>=_coeff0 in both parities, without any low-residual-degree hypothesis. For odd n=2m+1, m=2 gives C_d=D and S=0. For m>=3, at least one ordered root inequality is strict, so if u>0, S has strictly positive coefficients in degrees1..d-1 and zero constant and degree-d coefficient. At even n, A_d is strictly positive through degree d-1, so S has that strict positivity including its constant, independently of u.

Individual D polynomials can be ordinary-negative. For instance n7 gives

    D(t)=binom(t+3,5)
        =(t^5+5t^4+5t^3-5t^2-6t)/120.

Its linear and quadratic coefficients are -1/20 and -1/24. Its integer values are nonnegative; it is a shifted-binomial AUXILIARY, not an entire LR polynomial. All78 raw auxiliary D records with528 negative coefficient occurrences were saved by J03 before J04 comparisons.

## 3. A strict bound on the entire subtraction

Use the positive decomposition P=1+E_d+(2d-u)C_d of proof019 and (3). Write <=_coeff for ordinary coefficientwise comparison.

If d is odd, S<=_coeff2u C_d, while P>=_coeff(2d-u)C_d. Therefore

    (2d-u)S <=_coeff 2u P,
    S <=_coeff (u/d) M,
    S/2 <=_coeff rho M,  rho=u/(2d)<1.              (4)

The last notation denotes a scalar multiple of polynomials, not division of polynomials. The middle inequality also holds at the constant coefficient: S0=0, M0=1. At u=0, S=0 and rho=0.

If d is even, A_d=d B_d(2t)/(2t+1), so d B_d(2t)-A_d=2t A_d>=_coeff0. Set X=1+E_d>=_coeff0 and a=2d-u>0. Then

    P=X+a C_d,
    S<=_coeff dX+(2d^2+2u)C_d
      <=_coeff kappa P,
    kappa=2(d^2+u)/(2d-u),

because kappa>=d. Rearranging S<=kappa P with M=P+S/2 gives

    S/2 <=_coeff rho M,
    rho=(d^2+u)/(d(d+2))<1.                         (5)

The strict inequality follows from u<=d+2<2d at d>=4. The constants are included: S0=d and M0=(d+2)/2.

M is strictly ordinary-positive, either from its explicit positive decomposition P+S/2 or directly from (2),(3),(5) of proof019. Equations (4)-(5) therefore control EVERY subtracted coefficient:

    P=M-S/2 >=_coeff (1-rho)M >_coeff0

through actual degree. These are uniform, deliberately nonsharp quantitative bounds on a complete LR family. They prove what positivity of M and S alone would not prove. The source's negative Reeve two-pyramid remains an abstract counterexample to the unqualified inference and is not being realized here.

## 4. An unbounded family of genuinely uncovered interiors

Let n=2m+1 be odd. The unique first-interior point in bottom GT coordinates is

    a_k=k-1, k=2,...,n-1.

Translation by it injects P(t)'s entire lattice set into the true interiors at q+t. Because there is only one first point, the COMPLETE uncovered count is exactly S(t), not merely an upper bound. For m>=3,

    S(t)=u[binom(t+2m-2,2m-1)-binom(t+m,2m-1)],
    S(1)=u.                                        (6)

Consequently first-grade generation holds throughout this odd-n family if u=0, and also for m=2; it fails already at the next grade whenever m>=3 and u>0. For the failed cases it leaves a strictly positive uncovered count at every positive stretch. The residual degree d-q+1=m is unbounded. Thus neither unique first interiors nor their full translate supplies a universal LR coverage explanation; the actual uncovered strata coexist with strict ordinary positivity and the quantitative bound above.

The source's n7 uniform (5,2) control has u=7 and is one overlap with (6), not a new independent example. A genuinely unequal example is w=(1,1,1,2,3,4,5), with

    lambda=(17,16,15,14,12,9,5),
    mu=(16,15,14,12,9,5), nu=(15,2).

It has rank7, outer size88, degree5 and codegree3. Its complete polynomial is binom(2t+5,5)-3binom(t+4,5), its first positive count is18, and I(4)=21. Exactly three interior points lie outside the sole first translate. All its coefficients are positive, with c1=119/30. No area-thirty increment follows.

At even n, S is the complement of any ONE first-interior translate, not the complement of the union of all n-1 translates. J05 preserves that union separately in its full point-set data. A finite union failure is not silently replaced by S.

## 5. Equal polynomials do not determine the overlap geometry

There is a sharper finite challenge in the same complete family. Compare n8 weights

    w=(1,1,1,2,2,2,2,2),
    w'=(1,1,2,1,2,2,2,2).

Both have u=3, W=13 and the ENTIRE polynomial binom(2t+6,6)-3binom(t+5,6). Both have actual degree6, codegree4, seven first-interior points, P(1)=25 and I(5)=84. Nevertheless their complete GT first-translate unions at the next grade omit respectively FOUR and THREE points. J06 enumerates all56 placements of the three unit weights, and J07 preserves the two complete witness point sets and all membership tests.

This demonstrates that even the full Ehrhart polynomial, P/S/q and the first-interior count do not determine the translated-interior incidence data of a chosen complete counting model. In particular these two GT polytopes have no dilation-compatible affine lattice equivalence, since such an equivalence would preserve the number of uncovered points. No analogous inequivalence of their conventional hive models is asserted without an actual GT-to-hive affine map.

## 6. Complete evidence and exact remaining bridge

The coefficient and strict-interior gates in J04 cover91 prior-space vectors,1520 whole GT sites,182 unused positive holds and874 strict-interior sites. J05 saves the complete first, parent, later-interior and uncovered point sets for114 parameter/grade records. The even-case uncovered counts in that finite roster are observations, not an all-weight classification. The all-n claims in Sections1–4 rest on the full formulas and inequalities, not this finite table.

The result does not cover arbitrary two-row shapes, general LR boundaries, all gap-three fibers, the new matching q6 obstruction, or the released higher-rank Horn families. Increasing the second-row slope to three activates simultaneous unit-cap violations; the next note retains their full correction. The independent source-sink generation theorem of proof017 and the non-generated family here show why the complete geometric premises and actual subtraction must both be kept.
