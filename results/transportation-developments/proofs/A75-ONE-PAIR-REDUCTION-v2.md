# A75: a complete one-pair extremal reduction and uniform low-band payment

Curated mathematical proof from **A75**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root research built on the accepted Pro051-derived A73 complete V/product identities and the A74 complete two-band intersection. No Pro052 premise is used.. Every comparison is in ordinary coefficients of the same t; formal x=At and h=Ht never change the lattice or grade. The result below is a full original comparison, not an isolated-sector sign.

## 1. Original and complete domain

Take balanced integral nonnegative rows (A,B,R), 0<A<=B, and labeled physical columns e. Delete forced zeros only in formulas and let N=n+1 be the positive-column count. Every positive e_j>=A. Exactly one pair has e_1+e_2<A+B; every other pair has sum at least A+B. Relabel the exceptional pair so e_1<=e_2. The complete A65 buffered lambda-outer LR constructor, its inverse, saturated free table chart, total unimodularity and positive active table r_i e_j/M apply unchanged. N>=3: at N=2 balance would give R<0. Also R>=e_2>0 because any third column has e_1+e_3>=A+B. Thus the actual degree is 2n, established before reconstruction. Labels and all physical zero positions are retained. No assumption that (A,B) are the smallest two rows is necessary.

Write C=B-A, alpha=e_1-A, beta=e_2-A, H=A+B-e_1-e_2=C-alpha-beta>0. Then 0<=alpha<=beta, C>=H and 0<=alpha<=(C-H)/2. The other shortfalls delta_j=(B-e_j)_+ satisfy delta_j<=alpha because e_1+e_j>=A+B. Both exceptional columns are below B, with shortfalls C-alpha and H+alpha. Set x=At, h=Ht. Use the full A73 polynomials a_n,d_n,V_n, including V's terminal d_n(z)a_n(x), and let J=J_(n-1,2)(A,H;t) be the ENTIRE A74 pair intersection, including its first-row tail when H>A.

Every higher intersection is empty: a subset of size at least three contains a nonoverlapping pair, and its strict +1 shifts force impossibility. Hence the actual original is


```text
P=U(Ct)-V(x,(C-alpha)t)-V(x,(H+alpha)t)
   -sum_(j>=3) V(x,delta_j t)+J
   +sum_(j>=3)[d_(2n)(x)-d_(2n)(h_j t)],
U(z)=a_n(x)a_n(x+z), h_j=min(A,(A+B-e_j)_+).
```

The final height improvements are nonnegative. Both singleton row bounds and the complete pair intersection remain. There are n-1 other positive columns, not n or n+1.

## 2. Common two-profile comparison

For every ordinary coefficient, V(x,z) is nondecreasing and convex in the numerical nonnegative slope z/t. Bound every other delta_j by alpha. The sum

    V(x,(C-alpha)t)+V(x,(H+alpha)t)+(n-1)V(x,alpha t)

is convex in alpha on [0,(C-H)/2]. Its chord therefore gives one COMMON coefficientwise convex combination of the endpoint polynomials


```text
Q0=U(Ct)-V(x,Ct)-V(x,h)-(n-1)V(x,0)+J,
Qsym=U(h+2y)-2V(x,h+y)-(n-1)V(x,y)+J,
y=(C-H)t/2.
```

For C>H the weights are 1-2alpha/(C-H) and 2alpha/(C-H), respectively. If C=H the interval is one point and both endpoints coincide; no division occurs. This is a single complete polynomial comparison with common numerical weights, not a separate choice per coefficient.

## 3. Both profiles dominate ONE complete canonical original

Define


```text
S_n(x,h)=U(h)-2V(x,h)-(n-1)V(x,0)+J.                 (1)
```

It is the entire original with rows (A,A+H,A+(n-2)(A+H)) and columns (A,A,(A+H) repeated n-1 times). It retains exactly N=n+1 positive columns and the same actual degree 2n. Integral A,H produce a literal legal original; the rational comparison variable y is not a new table grade.

A73 proves U(z)-V(x,z) has nonnegative coefficients in x,z in positive z degrees: its exact expansion is a z-independent term plus


```text
sum_(l=1)^(n-1) d_l(z)[a_n(x)a_(n-l)(x)-d_(2n-l)(x)].
```

Thus Q0-S_n=[U(Ct)-V(x,Ct)]-[U(h)-V(x,h)]>=0 since C>=H.

For Qsym write u_j(x)=[z^j]U(z), v_j(x)=[z^j]V(x,z). The terms of Qsym-S_n with no positive h power form exactly A73's complete Q_half-K_n, which is coefficientwise nonnegative. For h^i y^j with i,j>=1 the coefficient is


```text
binom(i+j,i)[2^j u_(i+j)-2v_(i+j)]
  =binom(i+j,i)[2(u_(i+j)-v_(i+j))+(2^j-2)u_(i+j)]>=0.
```

These inequalities follow from the full A73 product comparisons, including the terminal order; no value-positivity inference enters. Terms with j=0 cancel. Therefore Qsym>=S_n, and altogether


```text
ENTIRE P >=_coef S_n(At,Ht)                         (2)
```

for EVERY n>=2 and both H bands. This reduces the entire one-pair sign problem to one two-parameter canonical family, uniformly in all other widths and B-A. Neither endpoint positivity alone nor a changed original offset is used. Equation (2) supplies no sign outside the one-pair/selected-width domain and no sign for an arbitrary split gain.

## 4. Uniform payment for 0<H<=A

Here x>=h>=0 and the complete pair tail is zero. Let K_n(x)=a_n(x)^2-(n+1)d_(2n)(x), already strictly positive through degree 2n for n>=2 and x>0. Rising addition gives


```text
S_n-K_n=sum_(l=1)^(n-1) d_l(h)
                [a_n(x)a_(n-l)(x)-2d_(2n-l)(x)]
              -d_n(h)a_n(x)+J.                    (3)
```

For p,q>=1, sorted denominators imply


```text
a_p(x)a_q(x)-2d_(p+q)(x)
  >=a_(p+q-1)(x)[1+(1-2/(p+q))x]>=0.
```

For n>=3 retain the l=n-1 term in (3) together with the negative terminal term. Their exact sum is


```text
R=d_(n-1)(h)a_n(x)
          [1/n+(n-1)x/(n+1)-h/n].                 (4)
```

The bracket is >=1/n+lambda_n x, where
lambda_n=(n^2-2n-1)/(n(n+1))>0. Also


```text
a_(n-2)(h)a_n(x)>=a_(n-2)(h)a_n(h)
                       >=a_(2n-3)(h).
```

All factors compared are nonnegative polynomials after x=h+(A-H)t. Therefore


```text
R>=h a_(2n-3)(h)/(n-1)[1/n+lambda_n x].             (5)
```

The COMPLETE low-band pair polynomial simplifies exactly to


```text
J=h(h-1)a_(2n-3)(h)/D_n
          [x+c_n-d_n^* h],
D_n=(2n-1)(2n-2), c_n=(2n-1)/n,
d_n^*=(n-1)/(2n).
```

The symbol d_n^* is a number, not the rising polynomial d_n. Expanding (h-1) and using hx-d_n^*h^2>=0 for x>=h proves the coefficientwise LOWER bound


```text
J>=-h a_(2n-3)(h)(x+c_n)/D_n.                      (6)
```

The terms discarded in this lower bound are h a/D_n times
hx-d_n^*h^2+(c_n+d_n^*)h, all nonnegative. Thus (5)+(6) pays the entire adverse J:


```text
S_n>=K_n+h a_(2n-3)(h)
     [1/(2n(n-1))+(lambda_n/(n-1)-1/D_n)x].         (7)
```

The x coefficient is positive for every n>=3. After positive denominators its numerator is 4n^3-11n^2-n+2; at n=m+3 it is 4m^3+25m^2+41m+8>0. Every earlier l term in (3) is nonnegative. This proves (7) uniformly, not by testing n.

At n=2 use the actual row permutation (A,A+H,A)->(A,A,A+H). A73's entire no-overlap formula gives


```text
S_2=K_2(x)+d_4(x)-d_4(x-h)>=K_2(x)
```

for 0<=H<=A. This retains the low-dimensional case instead of applying the n>=3 bound. At H=0 there is no pair and the same S_n is exactly K_n. Equality H=A is included in the low-band proof with no invented tail.

Consequently EVERY complete original in section 1 with H<=A has strictly positive ordinary coefficients in all degrees 0..2n, for arbitrary positive-column count. This is an unbounded all-coefficient theorem in its stated original family. The original lattice, degree, strict shifts, simultaneous incidence and zero physical columns remain unchanged.

## 5. Complete high-band bridge and final theorem

HIGH-BAND-CONTRACTION.md proves the entire unequal-free-slot auxiliary W_(n,m) coefficient-positive by retaining both singleton caps, their complete pair intersection and the terminal a_n term. Rising addition in the nonnegative excess z=(H-A)t then gives the exact complete-original identity


```text
S_n(x,x+z)=S_n(x,x)
       +sum_(l=1)^(n-2) d_l(z) W_(n,n-l)(x).
```

Every added term is nonnegative; the n=2 sum is empty. Together with (2) and the low-band theorem this proves P>=S_n>=K_n for every n>=2 in BOTH bands, with strict coefficients through the actual degree 2n. The full quantitative reserve is a_(2n-1)(At)[1+(n-1)At/(2n)]. No number-of-columns bound remains.

The initial exact n=2..12 sparse cone calculation is retained in pair-cones-v1.json. Independent dense integer arithmetic checks every coefficient, the full boundary identity and pure-ray strictness. This supplies an additional bounded multivariate coefficient certificate, not the unbounded ordinary theorem's quantifier. Six frozen complete originals independently check formula/character/direct-table/bare-LR agreement and their two unused grades each. The A74 controls and historical adverse pieces remain authenticated evidence.

THEOREM: For balanced three-row margins with specified 0<A<=B, every positive column at least A, and exactly one pair summing below A+B, the ENTIRE transportation/LR original is strictly ordinary-coefficient-positive through actual degree. The accepted zero-overlap family extends this statement to at most one pair. Forced zero columns and labels are retained; no claim for an overlapping column below A, arbitrary split gains, multiple-overlap originals, arbitrary three-letter LR shapes, whole rank seven or unrestricted KTT follows.
