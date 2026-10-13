# A71 independent reconstruction of the completed Pro050 one-sided overlap theorem

Curated mathematical proof from **A71**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Origin: completed Pro050 U10-02 and U11-01/02/03, retained with their exact originating byte identities. This note independently derives the entire physical character reduction, full coefficient kernel, positive finite cells and prior degree/strictness. Returned programs remain inert. Independent campaign code must compare complete cells, direct scalar sums and the two declared bare originals as numerical evidence. U09's separate high-overlap theorem and all unselected provider results remain SOURCE.

## 1. Whole originals and exact theorem

Fix integers L>=1, b>=c>=1, h,g>=0 with h+g<=c. Put H=min(h,g), G=max(h,g). Let u,v,k>=b, b-G<=j<=b and s>=j. The physical skew rows have widths
    (u,v,k,s,w_1,...,w_L)
and adjacent overlaps
    (h,g,j,0,...,0),
where every detached width independently satisfies w_i>=b+c-h-g-j. Widths may be unequal. Construct backwards

```text
lambda_n=d_n,
lambda_i=lambda_(i+1)+d_i-e_i,
mu_i=lambda_i-d_i,
nu=(sum_i d_i-b-c,b,c),
```

with lambda OUTER. Each overlap is at most both neighboring widths, so lambda and mu are nonnegative partitions, and nu_1>=b follows from the three long widths. The size equation is exact. Keep physical zero rows and trim only for reporting ordinary rank.

Set

```text
A=c-h-g, delta=b-c, U=b-j, V=max(b-s,0).
```

Then A,delta>=0, 0<=V<=U<=G, and the detached floor is A+U. EVERY ordinary coefficient of the entire original polynomial is strictly positive through its actual degree, with the complete ordered degree rule:

```text
U=0: degree L+1 if A>0, otherwise degree 0;
U>0, delta>0: degree 2L+3 if U>V, otherwise 2L+2;
U>0, delta=0, A+H>0: degree 2L+2 if U>V, otherwise 2L+1;
U>0, delta=A=H=0: degree L+1 if U>V, otherwise L.
```

The polynomial is nonempty and P(0)=1 in every case. This is an unbounded-row FAMILY theorem, not whole-rank or unrestricted KTT. Its width, overlap, content and tail hypotheses are substantive. No universal full A_degree reserve is adopted for the general enlarged strip.

## 2. Reconstruct the full four-row determinant

Use h_n(x,y), H_n=h_n(1,x,y), both zero for n<0, and Dxy=(1-x)(1-y). Put r_n=h_n-xy h_(n-1), so r_0=1. Direct geometric summation gives

```text
Dxy H_n=1-r_(n+1),
(1-y/x)r_n=x^n(1-y)-x^(-1)y^(n+1)(1-x).
```

For B>=C>=0 and n>B, both monomials on the right have unsupported target exponents when multiplied by ANY formal series with nonnegative exponents, even one with signed coefficients. Thus in the full dominant extraction every H_q with q>=B may be replaced by 1/Dxy. This is a highest-weight coefficient identity, not a raw character equality.

The accepted full skew Jacobi-Trudi and three-letter highest-weight extraction give coefficient x^(bt)y^(ct) of Dxy(1-y/x) times the entire skew determinant. Detached rows make the matrix block upper triangular: every lower-left entry across a zero overlap has negative index. Their diagonal factors are H_(w_i t).

In the leading 4-by-4 block, every diagonal/upper entry in the first three rows has index at least bt. For example the upper indices are (u+v-h)t+1, (v+k-g)t+1, (k+s-j)t+1 and their full consecutive sums; the long floors and s>=j prove the bound. The (3,1) and (4,1) entries are zero since their indices are (h+g-v)t-2 and (h+g+j-v-k)t-3. The (4,2) entry may be nonzero and MUST be retained. After all legitimate long replacements, the COMPLETE matrix is
    [ Z, Z, Z, Z ]
    [ B, Z, Z, Z ]
    [ 0, C, Z, Z ]
    [ 0, E, J, S ],
where Z=1/Dxy, B=H_(ht-1), C=H_(gt-1), E=H_((g+j-k)t-2), J=H_(jt-1), S=H_(st).
Its full determinant is Z(Z-B)(Z-C)(S-J). In particular E cancels between its two full determinant terms; it is not assumed zero. Therefore, after the full Weyl prefactor,

```text
P(t)=[x^(bt)y^(ct)](1-y/x)
       r_(ht) r_(gt) (H_(st)-H_(jt-1))
       product_i H_(w_i t) / Dxy^2.                       (1)
```

The entire band H_(st)-H_(jt-1)=sum_(q=jt)^(st) h_q has minimum total degree jt; r_(ht)r_(gt) has minimum total degree (h+g)t. The Weyl factor 1-y/x has degree zero. At the target total degree (b+c)t, the remaining degree is at most (A+U)t. Each detached discrepancy from 1/Dxy starts in total degree w_i t+1>(A+U)t. Hence ALL detached factors may simultaneously be replaced, yielding

```text
P(t)=[x^(bt)y^(ct)](1-y/x)
       r_(ht)r_(gt)(H_(st)-H_(jt-1))/Dxy^(L+2).            (2)
```

All shifts occurred once; every determinant term and detached capacity has a reason for cancellation or inactivity. The identities include t=0, when unsupported negative indices remain zero.

## 3. Independently extract the complete one-sided kernel

Let B0>=C0>=0, 0<=H0<=G0, C0<=G0, and X=B0-H0-G0>=0. Write A_n(z)=binom(z+n,n), R_n(z)=binom(z+n-1,n), with R_0=1. For supported nonnegative integer z these have their ordinary counting meanings. Define

```text
K=[x^B0 y^C0](1-y/x) r_H0 r_G0 / Dxy^(L+2).
```

The EXACT answer is

```text
K=R_(L+1)(X) A_L(C0)
   +sum_(w=0)^min(C0,H0) A_L(X+w) A_L(C0-w).              (3)
```

Here is a direct derivation independent of the provider's earlier correction formula. Use

```text
r_n=[x^(n+1)(1-y)-y^(n+1)(1-x)]/(x-y)
```

and expand 1/(x-y)=x^(-1)sum_(q>=0)(y/x)^q in the iterated formal Laurent field. Only finitely many q can reach y^C0. The terms containing y^(G0+1) or y^(H0+G0+2) vanish since C0<=G0. The remaining two coefficients are

```text
sum_(q=0)^C0 A_(L+1)(X+q) A_(L-1)(C0-q)
  -sum_(w=H0+1)^C0 A_L(X+w) A_L(C0-w).                   (4)
```

The second sum is empty when H0>=C0. L>=1 makes every displayed binomial valid. Pascal's full sum gives

```text
A_(L+1)(X+q)=R_(L+1)(X)+sum_(w=0)^q A_L(X+w).
```

Substitution into the FIRST sum of (4), with every endpoint retained, changes it to

```text
R_(L+1)(X)A_L(C0)+sum_(w=0)^C0 A_L(X+w)A_L(C0-w).
```

Subtract the complete suffix in (4), proving (3). This establishes the kernel at all magnitudes, zero parameters and ties. No positive-coefficient claim for an isolated omitted correction is used.

For any symmetric supported series Q, let `e(B,C;Q)=[x^B y^C](1-y/x)Q`. Direct telescoping of (1-y/x)h_q=x^q-x^(-1)y^(q+1) gives

```text
e(B,C;h_q Q)
  =sum_(i=max(0,q-C))^min(q,B-C) e(B-i,C-q+i;Q).          (5)
```

The full interval may be empty, in particular when q>B. Symmetry handles the first endpoint when q>B-C; negative exponents eliminate the other when q>C. This holds for signed Q too.

Apply (5) to every q in (2), set x=bt-i-ct and y=ct-q+i, and distinguish these integer residual variables from the two formal coefficient variables. The complete residual domain is

```text
x,y>=0, x<=delta t, Vt<=x+y<=Ut.
```

Its target for (3) is (ct+x,y), so X=At+x and y<=Ut<=Gt. No residual term lies outside the kernel's proved cone. Therefore

```text
P(t)=sum_residual [
   R_(L+1)(At+x) A_L(y)
   +sum_(w=0)^min(y,Ht) A_L(At+x+w) A_L(y-w)].           (6)
```

At least the state x=0,y=Vt,w=0 contributes. This proves nonemptiness and the count's constant convention.

## 4. Complete F and J, with finite positive cells

Define the WHOLE primitives

```text
F_(r,n)=sum_(x,y>=0,x<=delta t,Vt<=x+y<=Ut) R_r(x)A_n(y),
J_(n,m)=sum_(x,w,z>=0,x<=delta t,w<=Ht,
              Vt<=x+w+z<=Ut) A_n(x+w)A_m(z).
```

Full rising Vandermonde in (6), including its zero-index terms, gives

```text
P(t)=sum_(ell=0)^(L+1) R_ell(At) F_(L+1-ell,L)
     +sum_(ell=0)^L R_ell(At) J_(L-ell,L).               (7)
```

The sign of these moving sums requires their entire finite cell decomposition.

For F with r=0, cumulative composition coordinates form a weak chain of M=n+2 variables, with the first <=delta t and the last in [Vt,Ut]. For r>0, R_r(x) counts r+1 composition coordinates of total x with the first STRICTLY positive. Append n+1 coordinates of total y; cumulative sums form a chain of M=r+n+2 positive variables, its (r+1)-th node <=delta t and last in [Vt,Ut]. Every map and inverse uses integral differences and a unit-coefficient eliminated equation.

For t>=1 represent zero coordinates by beta=0 fixed at zero, and every positive coordinate uniquely as (beta-1)t+v, 1<=v<=t. Beta is a weakly increasing sequence in 0..U (in 1..U for positive chains). Equal positive beta blocks carry independent weak residual chains. The internal cap is exactly beta_f<=delta. If V>0, beta_M<V is excluded, beta_M>V is free, and beta_M=V fixes ONLY the final residual node to t. Delete that last node, not its entire block. Every resulting cell is a product of W_a(t)=binom(t+a-1,a), with W_0=1. There are finitely many beta cells independently of t, and every product is coefficientwise nonnegative. The constants are F_(0,n)(0)=1 and F_(r,n)(0)=0 for r>0; the same unique fixed-cell rule reproduces them.

For J, let q=x+w and M=n+m+2, f=n+1<M. Its entire chart is

```text
0<=X_1<=...<=X_M<=Ut, X_M>=Vt,
q=X_f, 0<=x<=q, x<=delta t, q-x<=Ht.
```

The extra x node is NOT ordered against other chain nodes. Use the same beta sequence for the chain and an independent extra-band e in 0..min(delta,U); let b0=beta_f. Retain precisely:

```text
e=0: x=0, requiring b0<=H;
e>0: e<=b0 and b0-e<=H;
H=0: b0=e and x=q, identifying the extra node;
H>0,e=b0: extra residual x<=q;
H>0,b0-e=H: residual q<=x;
0<b0-e<H: an independent singleton.
```

The last three cases are disjoint when H>0. For the upper-residual edge, x may have an earlier beta but gains NO edge to the chain block at that beta. It links only to q. The final V flag deletes just X_M when fixed; f<M guarantees q survives.

A residual chain of a>=1 nodes with a singleton below its k-th node has complete polynomial W_(a+1)+(k-1)E_(a+1); above it the polynomial is W_(a+1)+(a-k)E_(a+1), where E_n=binom(t+n-2,n). Unique natural-label tie breaking gives one increasing insertion and the stated number with one strict junction, proving the counts without interpolation. For every 0<=z<=a-1 their COMPLETE factor is

```text
W_(a+1)+z E_(a+1)
   =W_a(t)*[(z+1)t+a-z]/(a+1).                         (8)
```

All its coefficients in degrees 1..a+1 are positive. E alone need not be coefficient-positive. Equality contributes the unchanged chain, and an independent singleton contributes t. Use the actual shortened q block after final-node deletion.

Multiplying complete factors over blocks and summing EVERY admissible beta/e cell proves J coefficientwise nonnegative and polynomial at all positive grades. Its constant is one: only the all-fixed cell survives, with all zeros if V=0 or the zero prefix and fixed final node if V>0. Hence J(0)=1 too. Cap inclusion in delta adds whole cells, and exchanging x,w gives H inclusion; both complete primitive gains are coefficientwise nonnegative. This does not sign a change of the final lower flag.

## 5. Prior actual degree and strictness of the entire original

The constant is one. A single chain C_(M,f) with upper cap X_f<=d t, final band [Vt,Ut], U,d>0 and f<=M-2 has strict coefficients through degree M when U>V, or M-1 when U=V>0. If U=1, the all-positive beta=1 cell is W_M or W_(M-1). If U>1, choose the first f betas equal to 1 and the rest U: its polynomial is W_f W_(M-f), or W_f W_(M-f-1) with the fixed last node. It pays degrees 2 through the full degree. A separate admitted cell pays t: only the last beta is V+1 in a moving band, or only the last TWO betas are U in a fixed band. The condition f<=M-2 preserves its upper flag. These finite-cell witnesses give degree and every sign before any original fitting.

When U=0, (7) is A_(L+1)(At), giving the first degree branch.

When U>0,delta>0, the full sum (7) dominates its A=H=0 expression by nonnegative R factors and complete H-cap inclusion. Pascal's R_(L+1)(x)+A_L(x)=A_(L+1)(x) makes that expression

```text
sum_(x,y>=0,x<=delta t,Vt<=x+y<=Ut) A_(L+1)(x)A_L(y).
```

It is C_(2L+3,L+2), so the strictness lemma attains degree 2L+3 or 2L+2. Every general F/J term in (7), multiplied by R_ell(At), has at most that degree: its chart uses at most 2L+3-ell variables before the ell-degree factor; a fixed positive total removes one. This proves the second branch.

If delta=0,A>0, the H=0 expression is the complete product
    A_(L+1)(At) [A_(L+1)(Ut)-R_(L+1)(Vt)].
The bracket is coefficient-positive through L+1 when U>V, by rising Vandermonde and cancellation of the sole R_(L+1)(Vt) term; at U=V it is A_L(Ut). This product attains degree 2L+2 or 2L+1, while the x=0 chart gives the matching upper bound. Complete H-cap inclusion preserves every strict coefficient.

If delta=A=0,H>0, (7) is J_(L,L)(0,H). Exchange x,w to recognize C_(2L+2,L+1) with cap H. The same strictness lemma gives degrees 2L+2 or 2L+1.

Finally if delta=A=H=0, the entire original is A_(L+1)(Ut)-R_(L+1)(Vt), proving the last degree branch. All-zero residual cases are points. Each count chart is integral with a saturated difference-coordinate lattice; the full coefficient identities are not claimed as hive isometries. Polynomial degree follows from exact all-grade counts and the displayed nonzero leading cells, with no numerical degree guess.

## 6. Exact adoption ceiling and next obstruction

Adopt, only after the passing independent gate: the entire physical reduction (2), complete kernel (3), whole original (6)-(7), full F/J polynomial/cap inclusion, and strict positivity with the exact ordered actual degrees for the stated original family. Do not adopt a generic full simplex reserve, arbitrary width-two/order-polytope positivity, longer-content lift, hive metric equivalence, or signs outside the stated overlaps/floors.

At U>G the residual domain can have y>Gt, so (3) is no longer the whole kernel. The complete strict prefix identified by Pro050, and later reflected corrections, must be restored before a sign can be assigned. Those escaped formulas remain unadopted source unless separately rederived. Likewise c<h+g<b, deficient long rows and effective detached caps are genuinely unpaid. The completed U09 high-overlap proof is preserved and seriously considered but is not silently adopted by this note.

Two frozen complete original controls, S1 at ordinary rank seven and S2 at ordinary rank eight after literal trimming, test the enlarged H<U<=G strip, unequal widths, and a fixed-total/degree-drop case. Both have prior degree nine, all ten determining grades and two unused grades per independent engine. The full finite auxiliary F/J domain and negative controls have separate prospective receipts. No provider numerical population is counted as a campaign replay, and
