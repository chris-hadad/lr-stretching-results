# A77 draft v2: uniform paid low envelope and enlarged unbounded star families

Curated mathematical proof from **A77**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation from accepted A73-A76 identities. No new Pro052 or Pro053 theorem is a premise.; the exact verification below is still pending. Every polynomial comparison is in ordinary coefficients of the same t. Physical originals remain integral; rational comparison slopes do not change their lattice.

## 1. Complete original and notation

Use balanced rows (A,B,R), specified 0<A<=B, N=n+1 positive labeled columns e, every positive e>=A. Retain all physical zero positions in the literal A65 lambda-outer constructor, its inverse, saturated upper-left chart and actual degree 2n. A nonempty triangle-free overlap graph (edges e_i+e_j<A+B) is a star centered at a minimum e0=A+alpha. Set C=B-A, L=C-2alpha>0 and its m heights H_i>0. Then H_i<=L and H_i+H_j<=L. N>=3 and R>0 follow from the full A76 graph argument. Keep both remaining-row bounds and every strict +1 in the full J. No higher intersection is supported because every triple contains a nonoverlapping pair.

The new complete-family hypotheses in section 4 are L<=2A or max H_i<=A. There is no bound on n, m, margins, or sum H_i. Individual original pairs retain their own bands. The separate complete equal-height-star inequality below has H<=A.

Write a_k(z)=prod_(i=1)^k(1+z/i), d_k(z)=z a_(k-1)(z)/k, a_0=d_0=1; x=At,h=Ht,y=alpha t. Let U_n(x,z)=a_n(x)a_n(x+z), V_n(x,z)=sum_(l=0)^(n-1)d_l(z)d_(2n-l)(x)+d_n(z)a_n(x), F=U-V, K=F(x,0)-n V(x,0).

## 2. A complete convex upper correction

For n>=3 put D=(2n-1)(2n-2), c=(2n-1)/n and d=(n-1)/(2n). The ENTIRE low-band pair is


```text
J_low(x,h)=h(h-1)a_(2n-3)(h)[x+c-dh]/D.
```

For 0<=h<=x its full lower bound is


```text
J_low >= -A_n(x,h),
A_n=h a_(2n-3)(h)(x+c)/D.
```

Indeed the omitted difference is h a_(2n-3)(h)[hx-dh^2+(c+d)h]/D, nonnegative after x=h+u. This is an exact payment retaining the adverse term, not count positivity. Define


```text
q_n(x,h)=V_n(x,h)-V_n(x,0)+A_n(x,h).
```

All its formal x,h coefficients are nonnegative and it vanishes at h=0. Each ordinary t coefficient is nondecreasing and convex as a function of numerical H. It bounds the COMPLETE correction g=V-V0-J_low from above only on H<=A.

## 3. Uniform entire equal-height-star reserve

The claim is


```text
Etilde=F_n(x,2h)-F_n(x,0)-n q_n(x,h) >= 0,
              n>=3, 0<=h<=x.
```

This pays the entire equal-height n-leaf star after replacing every full J by its explicit lower bound. The accepted complete product inequality is B_l=a_n(x)a_(n-l)(x)>=a_n(x)+(n+1)D_l, D_l=d_(2n-l)(x), for 1<=l<n. Hence, using the full terminal d_n(h)a_n(x),


```text
Etilde >= a_n(x) B(h)
   +n sum_(l=1)^(n-1)[d_l(2h)-d_l(h)]D_l -n A_n,
B(h)=a_(n-1)(2h)-1-h a_(n-1)(h).
```

We require the elementary all-n inequality


```text
B(h) >= (1/3)h a_(n-1)(h) -(4/3)h^n/(n-1)! .       (1)
```

For a_(n-1)=sum e_k h^k, double counting k-subsets of the positive slopes 1,1/2,...,1/(n-1) gives k e_k>=(n-k)e_(k-1)/(n-1). For n>=7, 2^k(n-k)>=3k(n-1)/2 for 1<=k<n: k=1,2,3,4,5 are direct linear inequalities in n; for k>=6 use n>=k+1 and 2^k>=3k^2/2 (induct from k=6). Thus 2^k e_k-e_(k-1)>=(1/2)e_(k-1), stronger than (1). For n=3,4,5,6 direct expansion of the four explicitly defined products checks (1); the leading negative coefficient is exactly -1/(n-1)!, retained by its displayed compensator. These four finite algebraic bases, not an increasing n cutoff, complete the arbitrary-n proof.

Every difference d_l(2h)-d_l(h) is coefficientwise nonnegative. Retain its l=n-1 top monomial and D_(n-1)=d_(n+1)(x)=x a_n(x)/(n+1). It contributes at least


```text
[n/(n+1)] [2^(n-1)-1] h^n a_n(x)/(n-1)!,
```

because x>=h. Its multiplier is at least 9/4>4/3 for n>=3, so it pays the full negative term in (1). Sorted denominators give a_n(x)a_(n-1)(h)>=(1+x)a_(2n-3)(h). Consequently


```text
Etilde >= h a_(2n-3)(h)
      [(1/3-1/(2n-2)) +(1/3-n/D)x] >= 0.           (2)
```

Both displayed constants are strictly positive for n>=3. At h=0 all terms vanish. No terminal coefficient or negative kernel has been omitted. K supplies strictness through actual degree 2n of the whole original; no unsupported strictness of every difference degree is claimed.

## 4. Full arbitrary star profiles in two enlarged domains

UNIFORM-G-v1 proves the ACTUAL complete g nondecreasing and convex for every n>=3, on both bands and across their full jump. Consequently the exact A76 common-weight reduction applies to every star profile. Its one-pair endpoint is paid at every height by the complete A75 theorem. Its symmetric endpoint has H=L/2 and is paid by (2) whenever L<=2A. The uniform alpha widening is the complete A76 theorem. Hence P>=K for EVERY selected-width triangle-free original with


```text
L=B-A-2alpha<=2A, equivalently B<=A+2e0.             (5)
```

A second sufficient domain is max_i H_i<=A, without a restriction on L. If L<=2A use (5). Otherwise, full G and its alpha-shift extension give sum_i g_alpha(H_i)<=n g_alpha(A). With alpha fixed, the complete core U(C)-V(C-alpha) is coefficientwise nondecreasing in C>=alpha: write it as F(C)+V(C)-V(C-alpha), and use nonnegative positive-C coefficients of F and of every difference of powers in V. Reducing C from L+2alpha to 2A+2alpha therefore gives the ENTIRE symmetric-star lower profile at H=A and the same alpha. Uniform widening and (2) pay it. Thus again P>=K.

Both are full whole-original theorems at arbitrary column count and overlap count. They include every selected-width triangle-free original with B<=3A and all stars whose individual pair heights are at most A. The earlier sum-H budget can fail arbitrarily badly with n. The complete equal-height original is separately paid for every 0<=H<=A, without the narrower version-1 profile restriction.

At n=2 use A76's full two-overlap boundary. An empty graph uses A73/A74. Zero-height leaves become nonleaves exactly. Every row, label, physical zero, tie, pair equality, actual degree and lattice remains. No unsupported triple or below-A selected width has entered.

## 5. Limits and verification obligations

Verify (1)'s four exact bases and all algebraic identities independently, the full cone bounds and widening/endpoint reduction, existing complete originals and boundary/negative controls, and every selected new legal original with prior degree and unused grades. Finite corroboration never supplies the unbounded quantifier. Source, scientific, numerical, formal and publication debts remain.
