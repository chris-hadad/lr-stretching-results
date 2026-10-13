# A77: independent dominant-column quadratic adoption

Curated mathematical proof from **A77**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Independent root reconstruction of completed Pro052 U10-01 and U11-01. The exact source hashes are b04ece3018f9d5d771be49b67878f8d694d9ca365d202e77480e77ad5e7176d4 and c86bf42d549bebac19e94ac7d4652caf922e813bcec6085803bf084fcd2ffb8a. Their SOURCE facts remain SOURCE; the separately derived root theorem below requires complete mathematical checks. No provider program is imported or run.

## 1. Entire legal original, lattice and exact theorem

Take three positive rational rows r1,r2,r3 and a finite physical nonnegative column list C with equal total M>0. Retain the exact A65 literal lambda-outer suffix constructor and its full forced-buffer/tableau-table bijection, inverse, all grades and physical zeros. Positive row and column entries have strict table r_i C_j/M. The saturated upper-left free integer chart, incidence total unimodularity and positive interior give actual degree 2(q-1), q the positive-column count, before reconstruction. Rational data clear every denominator simultaneously; the quadratic coefficient scales by the square of that scale. Equal parameters do not quotient labels. One positive column and zero total are points. These are balanced nonempty tables; no empty general LR convention is changed.

THEOREM: If one positive column z satisfies z>=max_i r_i, the ENTIRE polynomial has c2>0 whenever q>=2. For q=1, P=1 and c2=0. The hypothesis includes z below M/2; there is no column-count or row-imbalance limit. This signs c2 only, not every ordinary coefficient.

## 2. Exact cap coefficient from every original subset

For positive old widths d_1,...,d_m, total D and W2=sum d_j^2, define the entire single-row violation count


```text
N_d(h;t)=[y^(ht-1)] (1-y)^(-1)
                     product_j sum_(v=0)^(d_jt)(v+1)y^v,
                   0<=h<=D.
```

The strict -1 occurs once, each width and its multiplicity remains. Expand the finite sum as [1-y^(dt+1)(1+(dt+1)(1-y))]/(1-y)^2. For every labeled J subset of old columns and K subset J the term has sign (-1)^|J|, factor product_(j in K)(d_jt+1), and falling-binomial polynomial


```text
binom((h-d_J)t+2m-1-|J|-|K|, 2m-|K|).
```

Only h>d_J is supported. The full subset is unsupported throughout h<=D, including h=D, and is removed BEFORE any polynomial or integral continuation. All proper supported binomials have nonnegative integer upper entries at every initial grade; their ordinary empty zeros are their polynomial zeros. At h=d_J proper subsets vanish. Thus the original cap and its quadratic coefficient retain every initial grade and wall.

With j=|J| and harmonic H_0=0, direct zero-factor extraction gives


```text
V_d(h)=sum_(J proper) [a_(m,j)(h-d_J)_+^2
                          +b_(m,j)d_J(h-d_J)_+],
F_(m,j,k)=(2m-1-j-k)! j!/(2m-k)!,
a_(m,j)=sum_(k=0)^j binom(j,k)F_(m,j,k)
                              [H_(2m-1-j-k)-H_j],
b_(m,j)=sum_(k=1)^j binom(j-1,k-1)F_(m,j,k).
```

The source's full finite coefficient formulas have been reconstructed here; independent falling-product and beta/log-moment checks are required. No signed piece is called a positive count outside its actual support.

## 3. Full integral, signed kernel and exact compensated merge

Let ell(u)=log(u/(1-u)), and independent X_j have probability 1-u^2 of being one. For S=sum d_jX_j the probability of the labeled selected set J is p_J=u^(2(m-j))(1-u^2)^j. The full beta derivative gives a_(m,j)=integral p_J ell/u, while summing the product-factor linear terms gives b_(m,j)=integral p_J/[u(1+u)] when j>=1. The j=0 b term is multiplied by d_empty=0. Hence


```text
V_d(h)=integral_0^1 E[(h-S)_+^2 ell(u)
                      +S(h-S)_+/(1+u)] du/u.       (1)
```

The full-subset integrand is identically zero on h<=D before integration; it is never zero times a divergent coefficient. Every remaining term is integrable at zero and one. Finite sums, bounded factors and these explicit endpoint bounds justify all interchanges.

Merge two positive widths a,b, retaining every rest width e. Define T(v)=v_++(v-a-b)_+-(v-a)_+-(v-b)_+, and T2 with the same four squared positive parts. Direct piecewise differentiation gives T>=0, T2'=2T, and 0<=T2<=2ab, with T2 strictly increasing from 0 to 2ab on (0,a+b). The merged-versus-split Bernoulli difference is u^2(1-u^2) times that four-term difference. Put R=sum e_j X_j, f(u)=E[T2(h-R)], g(u)=E[T(h-R)], w=u(1-u^2), k=ell-1/(1+u). Then the ENTIRE merge difference is


```text
V_(e,a+b)(h)-V_(e,a,b)(h)
                     =integral w k f+h integral w g/(1+u). (2)
```

Common-uniform coupling makes R nonincreasing with u, so f is nondecreasing; k is strictly increasing. The exact moments are integral w=1/4 and integral w k=-1/8: integral w ell=1/24 and integral w/(1+u)=1/6. In particular the signed mass is negative and cannot be dropped. The finite covariance identity gives


```text
C(f,k)=2 integral integral w(u)w(v)
                     [k(u)-k(v)][f(u)-f(v)] du dv>=0,
integral w k f=-(1/2)integral w f+C(f,k).
```

Therefore the EXACT paid gap is


```text
V_(e,a+b)-V_(e,a,b)+ab/4
   =C(f,k)+(1/2)integral w(2ab-f)
                                  +h integral w g/(1+u)>=0. (3)
```

Every term is absolutely integrable. This is an auxiliary difference bound, not monotone merging and not a whole-original split-gain theorem.

## 4. Telescoping, full envelope and equality

For any finite labeled binary merge tree, sum_nodes a*b=(D^2-W2)/2. The one-width cap is exactly V_(D)(h)=h^2/2. Thus


```text
E_d(h)=h^2/2+(D^2-W2)/8-V_d(h)
                  =sum_nodes compensated gaps>=0.          (4)
```

At h=D every node has h-R>=a+b, f=2ab,g=0 and constant-f covariance zero; equality holds. For m>=2 and h<D the last merge has no rest, so its contribution is


```text
[2ab-T2(h)]/8+h T(h)/6>0.
```

This proves strict E_d(h)>0 on 0<=h<D for m>=2, equality only at h=D. For m=1 the tree is empty and E=0 throughout. At h=0 the gap is exactly (D^2-W2)/8. At h=D the complete count excludes only the all-maximal corner, giving V_d(D)=(5D^2-W2)/8. No envelope is asserted beyond D.

## 5. Restore the ENTIRE dominant-column original

Select the actual distinguished z by an explicit table-column permutation, retaining its inverse and physical positions. Put D=M-z and d the other positive widths. Their unrestricted triangular allocations have product binom(d_jt+2,2); the residuals determine z uniquely. An old row i violates exactly when its old total exceeds r_i t, and its complete count is N_d(delta_i;t), delta_i=(D-r_i)_+. Because z>=r_k, every pair r_i+r_j=M-r_k>=D. Two strict violations are therefore impossible, including equality because their two +1 shifts remain. No missing pair compensation has been discarded. At EVERY grade,


```text
P=product_j binom(d_jt+2,2)-sum_(i=1)^3 N_d(delta_i;t).
```

The product's c2 is (9D^2-5W2)/8. Substituting (4) gives the exact entire-original identity


```text
c2(P)=(3D^2-W2)/4-(1/2)sum_i delta_i^2
                                      +sum_i E_d(delta_i). (5)
```

All three actual gaps are retained and each cap is paid once; a zero cap may carry a loose envelope bound but is never changed to a nonzero actual cap. Since r_i>0, every delta_i<D. For m>=2 every E term is strictly positive.

If z>=M/2, the actual row-pair bounds and M>=2D give sum delta_i<=D for one, two or three positive deficits. Hence


```text
c2(P)>(D^2-W2)/4,                 m>=2.             (6)
```

If z<M/2, every row<=z<D and all deficits are positive. Necessarily z>=M/3. Write e_i=z-r_i>=0, sum e_i=3z-M; then sum e_i^2<=(3z-M)^2 proves sum r_i^2<=2z^2+(M-2z)^2. Equation (5) yields


```text
c2(P)>(D^2-W2)/4+(M-2z)(2z-M/2)>0, m>=2.           (7)
```

For m=1 the whole original has actual degree two and a strict rational interior, so c2 is its positive leading coefficient. For m=0 it is a point. This completes both sides of M/2, all equalities, arbitrary positive-column count, rational scaling and the stated complete original.

## 6. Verification, reach and retained limits

The frozen six-original roster combines three star controls with three new complete dominant-column originals below/at/above M/2; every literal triple and actual degree precedes counts. The latter include physical zeros, row-pair equality and inactive cap arguments. Independent full direct-table and bare-LR vectors, determining grades and two unused grades each must agree with the full root character formula and (5). Independent full cap jets/moments, complete auxiliary cells, m=12 nonconvexity and negative merge controls verify the actual weaker envelope and support/label/shift boundaries. Returned code remains inert. Exact measured attempts and failures accompany the checks.

The accepted scope is this complete dominant-column theorem and exact cap gap. Pro052's 7M/15 seed cover, low-overlap c1/c2 and other new claims remain unadopted source with explicit independent reentry; this note does not silently ratify them. No arbitrary all-small-column transportation positivity, all-row split gain, higher-coefficient or unrestricted LR/KTT theorem follows. General shapes, longer content, whole rank seven and all earlier debts remain. No candidate or additive-coverage increment; no formal, external peer-review, novelty or public-release claim.
