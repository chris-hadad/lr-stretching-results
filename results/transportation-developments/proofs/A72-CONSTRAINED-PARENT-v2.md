# A72: complete splitting with at most one constrained parent row

Curated mathematical proof from **A72**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root theorem. Premises are the accepted A65 complete transportation/LR formula and actual lattice/degree, A67 positive three-occupied quadratic kernels, A69 complete nonpositive wall jumps, and A70 complete weighted-cap convexity and terminal formula. No active provider result is a premise. The first-band derivation v1 remains immutable as an intermediate proof; this note removes its delta<=min d_j restriction by keeping every old-column cap. This is internal research, not external peer review, formal certification, priority or unrestricted KTT.

## 1. Entire object, theorem and complete all-margin defect

Let the labeled old widths d_j>=0 have sum D, and let three nonnegative integral row margins r_i have sum D+c, c>=0. Parent columns are (c,d), child columns (s,c-s,d), 0<=s<=c. Both are the ENTIRE transportation counts and hence entire lambda-outer LR polynomials under the accepted suffix-sum constructor


```text
lambda=(M+R_2,M+R_3,C_1,...,C_N),
mu=(M,M,C_2,...,C_N), nu=(R_1,R_2,R_3).
```

Here R_i,C_j are suffix sums of the original row/column lists and M their common total. Retain all physical zero positions; delete zero old columns only in the formulas. With p positive rows and q positive columns, actual degree is (p-1)(q-1), from the strictly positive active table r_i c_j/M, saturated free chart and total unimodularity. The zero-total table is a point. These degrees precede any coefficient reconstruction. Rational parameters always scale ALL margins to integers, then divide the quadratic coefficient by that scale squared; no lattice or residue is relaxed.

THEOREM. Suppose D>0 and at least two rows are >=D. Then every genuine split 0<s<c has strictly positive ENTIRE ordinary quadratic gain


```text
G(s)=[t^2](P_child(t)-P_parent(t)).
```

The child's whole c2 is also strictly positive. Identical-original split endpoints have zero gain. The case D=0 retains A71's actual-degree convention: a positive split has positive c2 for three positive rows and zero c2 for at most two. This theorem allows arbitrary depth of the one constrained row, every number/width of old columns, every split ratio and a zero constrained row. It does not sign arbitrary parents with two or three rows below D, higher coefficients, whole rank seven or unrestricted KTT.

The following complete identity remains valid even beyond this sign domain. At grade t and for each old allocation X, let u_i be its row totals and v_i=r_i t-u_i, so sum v_i=ct. The actual parent includes precisely the allocations with every v_i>=0. Its exact indicator is


```text
1-sum_i 1_(v_i<0)+sum_(i<j)1_(v_i<0,v_j<0).             (1)
```

No triple violation is possible. Define the finite signed Laurent polynomial


```text
B_v(q)=[z^q] product_i (1-z^(v_i+1))/(1-z).
```

For v_i=-1 its factor is zero; for v_i=-k<=-2 it is
-sum_(a=1)^(k-1) z^(-a). For nonnegative v_i it is the ordinary interval. Equivalently retain all eight inclusion-exclusion terms


```text
B_v(q)=sum_I (-1)^|I| binom(q-sum_(i in I)(v_i+1)+2,2)_+,
```

where binom(n,2)_+=0 for n<2. All shifts occur once.

If exactly one row i violates with v_i=-k, reflect its Laurent interval. For k>=2 this gives B_v(q)=-Q_(v,i)(q), where Q is the ENTIRE ordinary three-variable bounded-composition count with bounds (k-2,v_j,v_l) and total q+k-1. For k=1 it is zero. In general define Q by this reflection while retaining the other factors' signs; it is not then asserted to be an ordinary count.

If exactly two rows violate with magnitudes k_i,k_j, direct selection of their negative exponents gives


```text
B_v(q)=(k_i-1)(k_j-1) for EVERY 0<=q<=ct.                (2)
```

Indeed the third exponent always lies in its original interval [0,ct+k_i+k_j]. A magnitude-one factor makes both sides zero. Thus the two-violation difference, and each reflected signed difference, vanishes identically. For every original, all grades and all splits,


```text
P_child(t)-P_parent(t)
   =sum_X [B_v(st)-B_v(0)]
    +sum_i sum_(X:v_i<0) [Q_(v,i)(st)-Q_(v,i)(0)].      (3)
```

This preserves the entire constrained parent, including simultaneous violations in (1). Their cancellation in (3) is proved, not assumed. Equation (3) is a count identity; no ordinary sign is inferred from nonnegative count values.

## 2. Exact reduction when one row is constrained

A71 covers r_i>=D. Relabel the possible constrained row and put


```text
r_1=D-delta, 0<delta<=D, r_2,r_3>=D,
c=r_2+r_3-delta.
```

Delete zero old columns and let m>=1 be the positive old-column count. Only row 1 can violate. For its violation let u,v be the OTHER old row totals; each labeled old pair (u_j,v_j) obeys u_j,v_j>=0 and u_j+v_j<=d_jt. Put X=u+v. Violation means X<=delta t-1. Every such original triangular cap remains present below.

Let C_d(h) be A70's full weighted-cap quadratic, and write


```text
F(h)=h^2/2+Dh/12+sum_j d_j^2/36-11D^2/72,
E(s)=s^2/2+9Ds/4-sum_i C_d(s-r_i+D)
                  +sum_i [F(c-s-r_i+D)-C_d(c-s-r_i+D)]. (4)
```

The A70 moment/singleton/pair calculation is an identity over ALL old allocations in the signed Laurent expression. It does not require those allocations to be parent-admitted. Its triple cap is zero at s<=c with its original shift. Consequently [t^2]sum_X(B_v(st)-B_v(0))=E(s)-E(0), and here E(0)=-C_d(delta). Using E(s) without its endpoint normalization is invalid.

Define two COMPLETE auxiliary counts:


```text
M_d(delta;t)=sum_(old pairs X<=delta t-2) (delta t-X-1),

J_d(delta,h;t)=sum_(old pairs,z,w>=0,
                   X+z+w=delta t-2)
                   ((h-delta)t+u+z+1)_+.             (5)
```

Each labeled old-column bound remains. Let -L_d(delta) be the ordinary linear coefficient of M and let H_d(delta,h) be the quadratic coefficient of the EVENTUAL polynomial of J. Its exact eventual polynomial is derived below; no unproved all-grade continuation of a general affine auxiliary is needed. The entire original difference is a polynomial, so equality for every sufficiently large grade determines its exact coefficients, including its original early grades.

Reflection of the sole violating residual, followed by all four upper-cap terms, gives


```text
G(s)=E(s)+C_d(delta)-s L_d(delta)
          -H_d(delta,s+delta-r_2)-H_d(delta,s+delta-r_3). (6)
```

For completeness, at fixed old totals the reflected magnitude is k=delta t-X. Subtracting the s=0 count leaves st(k-1), minus, for each j=2,3,


```text
sum_(a=u+1)^(delta t-v-1) ((s-r_j)t+a)_+.
```

The strict shift is -1. Introduce z=a-u-1 and the remaining slack w to obtain exactly (5), with -2. Both baseline cap terms at s=0 vanish because r_j>=D>=delta. The simultaneous pair upper-cap term is unsupported for s<=c since the other residuals sum ct+k. This derives (6) while retaining every original cap.

### 2a. The entire linear defect is a convex hinge sum

The generating function of a labeled old column's complement is


```text
sum_(x=0)^(d_jt)(x+1)z^x
  =[1-z^(d_jt+1){1+(d_jt+1)(1-z)}]/(1-z)^2.
```

Multiply all of them by z^2/(1-z)^2. For 0<=delta<=D, only proper subsets J with d_J<delta contribute to the eventual polynomial of M. Its exact linear coefficient is


```text
L_d(delta)=sum_(J proper subset[m]) ell_(m,|J|)(delta-d_J)_+,
ell_(m,j)=sum_(k=0)^j binom(j,k)
                (2m-1-j-k)!(j+1)!/(2m+1-k)!.           (7)
```

Every ell is strictly positive. To check the offsets, the full binomial term has upper (delta-d_J)t+2m-1-j-k and lower 2m+1-k, multiplied by (-1)^j product_(K)(1+d_jt). Its unique zero factor and j+1 negative factors give the negative linear coefficient in (7). For proper J all factorial indices are nonnegative and equality slopes give zero; the full subset is unsupported throughout delta<=D and must not be replaced by a binomial polynomial at upper -1. This establishes the coefficient of the entire count, with ties retained.

Thus L is convex, nonnegative and L(0)=0. At delta=D the exact complete count is


```text
M_d(D;t)=((D/3)t-1) product_j binom(d_jt+2,2)
                                  +product_j(d_jt+1).
```

This subtracts the untruncated old first moment and restores its sole negative boundary at X=Dt; the X=Dt-1 layer is zero. Its linear coefficient is -D/6. Convexity therefore gives


```text
0<=L_d(delta)<=delta/6,  0<=delta<=D.                    (8)
```

### 2b. The capped quadratic uses only positive occupations

In (5), write u=sum u_j,v=sum v_j. The entire generating function for J is


```text
[x^(delta t-2)y^(h t-2)]
    product_j h_(d_jt)(1,x,xy) /[(1-x)(1-xy)(1-y)^2].   (9)
```

The variable z contributes x, w contributes xy, and the positive-part factor is the number of two nonnegative variables totaling ht-v-w-2. This proves (9), including its scalar -2 offsets.

Use the COMPLETE three-term Lagrange identity for every old h:


```text
h_a(1,x,xy)=1/[(1-x)(1-xy)]
          -x^(a+1)/[(1-x)(1-y)]
          +x^(a+1)y^(a+2)/[(1-xy)(1-y)].
```

For every labeled old assignment with occupations n=(n_1,n_2,n_3) and width totals C_i, put n'=n+(0,1,1), x0=delta-C_2-C_3 and y0=h-C_3. Its edge multiplicities and ORIGINAL offsets are exactly A65's for n':


```text
U=x0 t-(n_2+n_3+2), V=y0 t-2(n_3+1).
```

Its old sign is the NEGATIVE of the A65 sign (-1)^(n_2+1). Hence


```text
H_d(delta,h)=-sum_(every labeled old assignment)
                           Q_(n')(x0,y0),              (10)
```

with complete eventual support and the offset-aware U/V choice. Group only identical states with their exact labeled multiplicities. If n_1=0 then x0=delta-D<=0, and U has a strictly negative offset: that entire term is unsupported. Every surviving term therefore has ALL THREE occupations positive. A67 proves its complete quadratic on the two chambers:


```text
Q_U=A(p,q,r)xy+A(p,r,q)x(y-x),
Q_V=A(p,q,r)xy+A(q,p,r)y(x-y),     A>0.
```

It vanishes on supported axes and matches on the diagonal, retaining ties and all integer offsets. Therefore H is continuous, H<=0, and on every smooth h interval H''>=0: its U term is affine in h, and its negative V term has quadratic coefficient A(q,p,r)>0. This is a smooth-curvature assertion; H's slope jumps need not be nonnegative.

Each complete Lagrange summand has its exact A65 eventual polynomial. Their finite sum proves the required eventual polynomial of (9), without a numerical degree fit or an assertion that an unsupported early affine count equals a chamber continuation. For h<=0 the count and H vanish. For h>=delta, all positive parts in (5) are untruncated. Exchanging every old u_j,v_j and z,w preserves all caps, so their mean u+z is (delta t-2)/2. Thus, at every grade,


```text
J_d(delta,h;t)=(h-delta/2)t M_d(delta;t),
H_d(delta,h)=-(h-delta/2)L_d(delta).                    (11)
```

## 3. Complementary curvature of the full weighted cap

For ANY real x,y with x+y>=D, away from subset-sum knots,


```text
C_d''(x)+C_d''(y)>=1.                                 (12)
```

This new lemma concerns the COMPLETE cap; no individual subset coefficient is discarded. A70 gives


```text
C_d''(a)=2 integral_0^1 u f_a(u) log(u/(1-u)) du,
```

where f_a(u)=Prob(sum_j d_j X_j<a) and independent X_j have probability 1-u^2. Each f_a is nondecreasing in u by coupling. Let v=sqrt(1-u^2), so complementing every subset swaps u and v. Since x+y>=D, outside equality knots every subset obeys S<x or D-S<y. Hence


```text
f_x(u)+f_y(v)>=1,
F(u)+F(v)>=2,  F=f_x+f_y.
```

For u>=1/sqrt(2), v<=u, so F(u)>=F(v). Write l(u)=log(u/(1-u)). Both l(u)-l(v)>=0 and l(u)+l(v)>=0; the latter is equivalent to u+v>=1. It follows pointwise that


```text
F(u)l(u)+F(v)l(v)
  = (F(u)+F(v))(l(u)+l(v))/2
    +(F(u)-F(v))(l(u)-l(v))/2
  >= l(u)+l(v).
```

The substitution v=sqrt(1-u^2) preserves the measure u du up to reversal. Integrating the paired half interval therefore gives integral u F(u)l(u)du>=integral u l(u)du=1/2, proving (12). All logarithms are integrable. Knots are treated by their separate jumps below, never by assigning a smooth derivative across a wall.

## 4. A concave whole paired function, including every jump

Fix 0<delta<D and define, for EVERY real h,


```text
T(h)=F(D-h)-C_d(D-h)-C_d(D-delta+h)-H_d(delta,h).        (13)
```

It is concave on the entire line. For h<0 it is -C_d(D-delta+h). For h>delta the two F quadratics cancel to an affine function and H is affine by (11), leaving -C_d(D-h) plus affine terms. Both regions are concave. On every smooth interval 0<h<delta, (10) and (12) give


```text
T''=1-C_d''(D-h)-C_d''(D-delta+h)-H_d''(delta,h)<=0,
```

because the two cap arguments sum to 2D-delta>=D.

Every remaining derivative jump of T is nonpositive. This uses the already accepted A69 COMPLETE wall theorem, not a sign claim on an isolated correction. Realize T as the only nonconstant paired function in a whole split curve: take the SAME old widths, r_1=D-delta, r_2=D+a with any a>0, and choose r_3 sufficiently large that, on an open neighborhood of h in [0,delta],


```text
s=D-delta+a+h,  D-delta<s<c-(D-delta),
D-delta+(s+delta-r_3)<0.
```

One fixed sufficiently large rational r_3 works for the entire compact interval. Scale all data together for integer originals. Then the second T argument is in its identically-zero far-left range, C_d(s+delta) is strictly terminal, and the pair complementary to row 1 is inactive. The exact formula (6) becomes affine in s plus T(h) on that neighborhood. The parameter a>0 is essential: it keeps h=0 strictly inside the central interval, so no extra terminal-cap jump is hidden there. A69 applies to every physical wall and all collisions of this COMPLETE positive-margin original. Thus each T jump, including h=0,delta and coincident old-subset walls, is <=0. No new numerical original or independent lattice is introduced by this analytic realization.

Continuity follows from C and the all-positive kernels in (10). Piecewise nonpositive curvature plus every nonpositive jump proves the claimed global concavity.

## 5. Pay the entire gain and its zero-row boundary

First take r_1=R=D-delta>0. For 0<s<=R, every paired cap and both H terms vanish. The exact formula becomes


```text
G(s)=s^2/2+(9D/4-L_d(delta))s
   -[C_d(s+delta)-C_d(delta)]
   -C_d(s-r_2+D)-C_d(s-r_3+D).
```

A70 convexity and the exact right derivative C_d'(D+)=13D/12 bound the first difference by 13Ds/12. The two other complete caps are each at most 11Ds/24 by monotonicity and the chord bound. Using (8),


```text
G(s)>=s^2/2+(D/4-L_d(delta))s>=s^2/2+Ds/12>0.          (14)
```

On the ENTIRE central interval R<=s<=c-R, the singleton at s+delta is terminal and the pair complementary to row 1 is inactive. Equations (6) and (13) give


```text
G(s)=s^2/2+9Ds/4-F(s+delta)+C_d(delta)-s L_d(delta)
                         +T(s+delta-r_2)+T(s+delta-r_3). (15)
```

The first line is affine, and both T terms are concave. Thus G is concave on this whole interval. Its endpoints agree by the actual column-exchange bijection G(s)=G(c-s); both are strictly positive by (14). Their common chord pays the entire center, including two active paired terms. Reflection pays the final endpoint band. This proves every split ratio without asserting global concavity in the endpoint bands.

For r_1=0, delta=D, use the COMPLETE two-row reduction directly. The parent is product_j(d_jt+1). Let Z_d(h) be the quadratic coefficient of sum_(0<=x_j<=d_jt)(ht-sum x_j)_+. Its full generating function gives


```text
Z_d(h)=sum_J alpha_(m,|J|)(h-d_J)_+^2,
alpha_(m,j)=(m-j)!j!/(m+1)! [H_(m-j)-H_j].             (16)
```

At every subset-sum knot the slope is continuous. The beta-log representation is


```text
Z_d''(h)/2=integral_0^1 f_h(u) log(u/(1-u))du,
```

now with inclusion probability 1-u. Since f_h and the logarithm are nondecreasing and the logarithm has integral zero, the double-integral covariance identity gives Z_d''>=0, strictly positive on every open interval 0<h<D. Exact full moments give Z_d(h)=D(h-D/2) for h>=D. Thus Z_d is convex and


```text
Z_d(h)<Dh/2 for 0<h<D,  Z_d(0)=0, Z_d(D)=D^2/2.
```

The entire two-row split gain is


```text
G(s)=Ds-Z_d(s-r_2+D)-Z_d(s-r_3+D).                    (17)
```

On 0<s<=c/2 put a=r_2-D,b=r_3-D, so c=D+a+b. If both cap arguments are <=D, the strict chord bound gives G>0: two endpoint-only arguments cannot both equal D in this half interval, and if neither is positive then Ds>0. If one argument, say s-a, exceeds D, the half-interval inequality forces s-b<0; then G=D a+D^2/2>0. Reflection and exact zero endpoints finish this boundary. Original degrees are m for the parent and m+1 for a genuine child. No generic three-row degree is assigned to the zero row.

To obtain the child's WHOLE c2, use a noncircular complete-original construction. Starting with one column, split off the old d_j one at a time, retaining the eventual main column c as the remainder. At every step the current old-column total D' is <=D, so the SAME two rows remain >=D'. Each step therefore uses either A71's dominant result or the proved one-constrained-row gain. The first split at D'=0 has its actual-degree leading c2 when all three rows are positive; with two positive rows it has degree one and c2=0. Every later genuine split has D'>0 and strict gain. This constructs the exact parent and then the child, with all columns and zeros retained. The child has at least three positive columns and two positive rows here, so its c2 is strict. No parent positivity was used to prove the gain itself.

## 6. Independent checks, remaining reach and source boundary

The all-margin count identity (3) retains cases with two deficient rows; only its sign remains open there. The next boundary is genuinely two constrained rows: two H corrections must be coupled, and a favorable single T cannot replace their entire common original. The full low-overlap character and primitive/global original-generating routes remain serious alternatives. Positive integer counts, positive active sectors and stable quotients do not pay a whole original's ordinary coefficients.

Six frozen full originals in ORIGINALS.json test two first-band and one deeper-deficit parent/child pairs, with prior degrees 8/10, 10/12 and 10/12. Complete curves retain all knots, ties and slope jumps; determining and unused bare/table grades remain separate. Auxiliary checks must test (7), (10), (12), all T walls, general old-cap activation, strict -1/-2 offsets, omitted E(0), the zero residual factor and simultaneous violations. The earlier negative rest/pair/sector/intercept and birth/residue controls retain their exact meanings. Analytic arguments supply unbounded quantifiers; finite verification validates only its frozen domains. A negative correction or full gain is not an LR counterexample. Only an ordinary negative coefficient of a complete legal original triggers candidate handling.
