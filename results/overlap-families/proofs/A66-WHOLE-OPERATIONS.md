# A66 independent adoption: complete quantitative operations

Curated mathematical proof from **A66**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Provenance is completed Pro048 U11-01 and U11-02; exact originating bytes are recorded in this module's source map. The following proof was independently reconstructed. Provider code was not executed. Basic one-effective-cap positivity is older Pro046 SOURCE work, and some endpoint positivity also follows from accepted transportation terminals. The new adoption is the sharp whole-polynomial operation and reserve.

## Complete original and exact degree

Take nonnegative integral P,Q, H=P+Q, one distinguished physical cap k>=0 and m other positive caps ell_i>=H. Four paired widths are at least H. The row widths are (a,b,k,ell_1,...,ell_m,c,d), with overlaps P at the first pair and Q at the last, all others zero. Define lambda_n=w_n, mu_n=0 and upwards mu_i=lambda_(i+1)-e_i, lambda_i=mu_i+w_i; output nu=(sum w_i-2H,H,H). Retain zero physical rows and trim partitions only for reporting. All overlaps are bounded by their adjacent widths, so lambda and mu are partitions; total width at least 4H gives dominant nu and exact size balance. At H=0 one may choose positive paired widths and the whole one-letter count is 1.

The accepted A58 complete paired-character argument, including both Weyl partners and once-only shifts, identifies the ENTIRE count with the cap/slack sum. Every long cap is redundant because u_i+v_i<=U+V<=Ht. With L=m+2, the resulting complete count is


```text
C_L(P,Q,k;t)=sum_(u,v>=0,u<=Pt,v<=Qt,u+v<=kt)
  binom(Pt-u+L-1,L-1) binom(Qt-v+L-1,L-1).
```

The two factors are full weak compositions into L coordinates. Eliminating one coordinate per positive budget is a saturated integer chart. For every positive budget, a small strictly positive real allocation exists when k>0; k=0 forces the distinguished variables to zero. Thus actual degree is bL for k>0 and b(L-1) for k=0, where b is the number of positive budgets; if b=0 it is a point. This precedes every reconstruction. No hive metric or local face-volume assertion is used.

## Independent complete chamber derivation

Write A_n(z)=binom(z+n,n), R_n(z)=binom(z+n-1,n), R_0=1, and B_(a,b)=A_a A_b-R_(a+b). These are falling-product polynomials. Assume P<=Q by symmetry and set p=Pt,q=Qt,n=kt.

The complement of the weighted triangle in its n-by-n rectangle is obtained by reversing its two coordinates. Its new total is at most n-1, giving exactly R_(a+b)(n) after the two composition factors and slack are summed. Therefore its complete count is B_(a,b)(n). Rising Vandermonde gives


```text
binom(x+y+L-1,L-1)
  =sum_(i=0)^(L-1) R_i(x) binom(y+L-i-1,L-i-1).
```

Applying it to both weights, or reversing the whole rectangle complement, gives the following closed formulas:


```text
k<=P:
  C=sum_(i,j=0)^(L-1) R_i((P-k)t)R_j((Q-k)t)B_(L-i,L-j)(kt).
P<=k<=Q:
  C=A_L(p)A_L(q)
    -sum_(i=0)^(L-1)R_i((Q-k)t)R_(2L-i)(p)
    -R_L((Q-k)t)A_L(p).
Q<=k<=H:
  C=A_L(p)A_L(q)-R_(2L)((H-k)t).
H<=k:
  C=A_L(p)A_L(q).
```

For the middle formula one may instead expand its remaining rectangle about p, obtaining the positive expression


```text
sum_(i=0)^(L-1) R_i((Q-k)t)
  [B_(L,L-i)(p)+sum_(j=1)^(L-i)R_j((k-P)t)A_L(p)A_(L-i-j)(p)].
```

The upper formula expands positively about w=(H-k)t: B_(L,L)(w) plus all nonzero (i,j) terms R_i(p-w)R_j(q-w)A_(L-i)(w)A_(L-j)(w). All boundary formulas agree because R_i(0)=0 for i>0. Empty early sums have their actual zero values, and strict complement endpoints are shifted once. These count arguments prove all nonnegative integral grades, not an eventual fit. With one positive budget B the exact formula is A_L(Bt)-R_L(max(B-k,0)t).

Sort {1,...,a} union {1,...,b}. Its first denominator is 1 and its jth is at most j-1 for j>=2. Factor comparison therefore yields A_a A_b>=(1+z)A_(a+b-1) coefficientwise and B_(a,b)>=A_(a+b). The displayed positive chamber expansions prove C_L>=A_D(t) at integral parameters, using a positive integer argument in the diagonal B block, or the uncapped product when that argument vanishes. Zero k and one-budget boundaries use their actual lower degree. This is a reserve for each whole original.

## Sharp widening, including cancellation of decreasing factors

Differentiate the complete low chamber at fixed P,Q. The identity R_n'=sum_(d=1)^n R_(n-d)/d lets the negative derivatives of both remainder arguments reindex exactly:


```text
partial_k C=t sum_(i,j=0)^(L-1)R_i((P-k)t)R_j((Q-k)t)E_(L-i,L-j)(kt),
E_(a,b)=B_(a,b)'-sum_(d<a)B_(a-d,b)/d-sum_(d<b)B_(a,b-d)/d.
```

For a<=b direct cancellation of product derivatives gives


```text
E_(a,b)=A_b/a+sum_(d<a)R_(a+b-d)/d
   +sum_(j=0)^a(1/b-1/(a+b-j))R_j.
```

Every term is nonnegative; every coefficient through degree a+b-1 is positive. This pays the terms that would be lost by differentiating only increasing factors. Middle and upper derivatives are nonnegative by the complete negative-complement expressions. Shared-wall equality permits coefficientwise integration.

Put Phi(k)=3k-(k-P)_+-(k-Q)_+-(k-H)_+. For P,Q>0 and integral k2>=k1,


```text
C_L(k2)-C_L(k1)>=[Phi(k2)-Phi(k1)]R_(2L)(t).
```

It suffices to treat integral unit steps, since every wall is integral. Below both budgets write k=a+s, 0<=s<=1: the positive derivative above dominates P=Q=1,k=s, because its decreasing arguments are at least(1-s)t and its increasing argument at least st. Its integral is B_(L,L)(t)-A_(L-1)(t)^2>=3R_(2L)(t). After removing positive factors the last inequality reduces to


```text
(1+t)(1+t/(2L)) >= (1+t/(2L-2))(1+t/(2L-1)), L>=2.
```

Both coefficients follow directly after clearing positive denominators. In a middle unit step, the last complement term alone contributes at least R_L(t)A_L(t)>=2R_(2L)(t); every other change is nonnegative. In an upper step the exact gain is R_(2L)(jt)-R_(2L)((j-1)t)>=R_(2L)(t), j>=1. Above H it is zero. For one positive budget the same argument gives [min(k2,B)-min(k1,B)]R_L(t).

The linear coefficient is exactly H*H_(L-1)+Phi(k)/(2L); here H_n is harmonic. Thus each displayed nonzero comparison has exactly the linear coefficient of its reserve, proving optimality of that chain factor for that comparison. Positive widening is strict in every degree1..2L (or1..L) and zero after saturation. Starting with cap 0 and transferring width from a paired row down to its final legal width realizes the whole sequence with fixed total skew size and fixed output. No arbitrary row redistribution is inferred.

## Sharp saturated splitting

Split one long cap ell=r+s with r,s>=H, retaining at most the one distinguished effective cap. Both pieces are still redundant in the complete count, so this is C_L -> C_(L+1), L>=3, with output unchanged. Let D be the after actual degree. For two positive budgets the complete gain is at least 4R_D(t); for one positive budget at least R_D(t); with both zero it vanishes.

Here is the full factor proof. First


```text
B_(a+1,b)-B_(a,b)
  =z A_a A_b/(a+1)-z(z-1)A_(a+b-1)/[(a+b)(a+b+1)].
```

Replacing A_a A_b by(1+z)A_(a+b-1) gives positive linear and quadratic factors, so every common block in the positive chamber expansions increases; newly present blocks are nonnegative. The diagonal block obeys B_(L+1,L+1)-B_(L,L)>=4R_(2L+2). On dividing its lower bound by zA_(2L-1), its coefficients are


```text
1/[2L(L+1)],
(16L^3+12L^2-13L-5)/[4L(L+1)^2(2L+1)],
(8L^2-L-5)/[4L(L+1)^2(2L+1)].
```

The last two numerators at L=v+1 are16v^3+60v^2+59v+10 and8v^2+15v+2, hence positive for all L>=1. Uncapped products give the same4R reserve by the same denominator matching; their remainder after removing tA_(2L-1) has zero constant and positive higher coefficients. At k=0 use the uncapped formula with L-1 and degree2L. In the one-budget case the diagonal A increment is exactly R_(L+1), or R_L at k=0. These cases cover every wall and degree change.

Sharpness of 4 follows at P=Q=1,k>=2: the linear gain is 2/(L+1), exactly 4 times c1(R_(2L+2)). Sharpness of 1 follows at one unit budget and saturated k, where the entire gain is R_(L+1). A gain is a difference of whole originals, not itself asserted to be one LR polynomial.

## Verification and ceiling

The fresh algebra check independently expands all factor identities with 1<=a<=b<=12, 320 closed-chamber controls, 1,920 direct count values and640 complete-vector operations. The written identities and positive cleared polynomials supply the infinite quantifiers. Eleven named complete originals cover all widening chambers, saturation, unequal budgets, the rank8/9 split pair, zero caps, one budget and a point. All grades0..D+2 are compared to the campaign-authored bare original tableau engine; the last two are unused by reconstruction. Exact receipts and runtime counts govern completion; calibration alone is not full verification.

The mixed comparison R_8-R_4 still has c1=-1/8. A below-floor original has actual count 61 versus the invalid formula's 66. Malformed triples and the bare state-limit refuse rather than emit partial values. These controls preserve the hypotheses. This adoption does not sign several effective caps, arbitrary splitting, generic quadratic gain, arbitrary interacting overlaps, whole rank seven or unrestricted KTT.
