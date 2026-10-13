# A73: complete admission compensation and a central concavity theorem

Curated mathematical proof from **A73**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root research. This note starts
from the accepted A72 all-margin Laurent identity and complete capped kernels.
The normalized correction and the central argument were derived in the root
before the Pro051 U08 admission notice; U08 was subsequently read as independent
SOURCE corroboration, not a premise. The selected Pro051 operation/base adoption
is separately attributed and never becomes a root-only result by reconstruction.

## 1. The entire original and all boundaries

Let the three nonnegative integral row margins be r_i, let labeled old widths
d_j have total D, and let c=sum r_i-D>=0. Parent columns are (c,d); child columns
are (s,c-s,d), 0<=s<=c. These are the complete transportation counts and the
complete buffered lambda-outer LR originals of A65. The suffix-sum constructor,
physical zero positions, saturated free chart, total unimodularity and actual
degree (p-1)(q-1) remain unchanged. The zero-total table is a point. Rational
parameters are interpreted only after scaling ALL margins to integers and
dividing c2 by the square of that scale; no residue or lattice is relaxed.

All coefficient formulas below are exact eventual-polynomial identities whose
finite sum equals the whole Ehrhart polynomial. No unsupported early affine
count is assigned its chamber continuation as a literal count. The whole
original does have its exact polynomial at every grade, including P(0)=1.

Delete zero old widths only within formulas, retaining their positions. For
D>0 use A72's complete functions C_d(h), F_d(h), L_d(delta), H_d(delta,h):


```text
F_d(h)=h^2/2+Dh/12+sum d_j^2/36-11D^2/72;
L_d(delta)=-[t] M_d(delta;t);
H_d(delta,h)=[t^2] J_d(delta,h;t),
```

where M and J retain every old triangular column cap and the original -2
offset. Put delta_i=D-r_i and omit a correction exactly when delta_i<=0.
For active delta_i, 0<delta_i<=D. The all-margin formula uses delta_i=D
at a zero row; the central concavity theorem below has three positive rows.

Write


```text
E(s)=s^2/2+9Ds/4-sum_i C_d(s+delta_i)
      +sum_i [F_d(c-s+delta_i)-C_d(c-s+delta_i)].       (1)
```

This is the complete signed unrestricted-old-allocation expression. In
particular E(0) is generally NOT zero and is not always -sum C_d(delta_i).

THE EXACT ALL-MARGIN QUADRATIC GAIN IS


```text
G(s)=E(s)-E(0)-s sum_(i:delta_i>0) L_d(delta_i)
   -sum_(i:delta_i>0) sum_(j!=i)
      [H_d(delta_i,s+delta_i-r_j)-H_d(delta_i,delta_i-r_j)]. (2)
```

Both ordered row corrections survive. The common pair argument is
s+D-r_i-r_j, and its baseline D-r_i-r_j can be positive. Discarding these
baselines is invalid precisely in important simultaneous-violation strata.

## 2. Derivation with shared admission retained

At grade t take EVERY old allocation X. Let u_i be its row totals and
v_i=r_i t-u_i, so sum v_i=ct. The parent is admitted iff all v_i>=0.
Its exact indicator is 1-sum 1_(v_i<0)+sum 1_(v_i<0,v_j<0);
three simultaneous violations are impossible. Use the complete finite signed
Laurent intervals B_v from A72, with every +1 shift and all eight partners.

For v_i=-k<0, reflect that one interval. Its signed reflected polynomial
Q_i retains the other two interval signs; it is an ordinary count only when
the other residuals are nonnegative. For any 0<=q<=ct, including a second
negative residual,


```text
Q_i(q)-Q_i(0)=q(k-1)
   -sum_(j!=i) sum_(b=1)^(k-1)
                [(q+b-v_j)_+-(b-v_j)_+].             (3)
```

Indeed the reflected factor is the interval 0..k-2. The unrestricted other
two factors give q(k-1) on taking the difference. Their two individual upper
caps give the displayed positive parts. The joint cap is unsupported because
v_j+v_l=ct+k: its target after both shifts is q-ct-3<0. The k=1 factor is zero
and every displayed sum is empty. This is an exact finite algebraic identity,
not an argument that signed counts are nonnegative.

If two rows violate, direct selection of their two negative exponents gives
B_v(q)=(k_i-1)(k_j-1) for the ENTIRE interval 0<=q<=ct. Both reflected
differences and the signed B difference are therefore zero. Their parent
inclusion-exclusion terms were retained; their differences cancel exactly.
Consequently A72's complete normalized identity is still


```text
P_child-P_parent=sum_X[B_v(st)-B_v(0)]
      +sum_i sum_(X:v_i<0)[Q_i(st)-Q_i(0)].             (4)
```

For row i let u,v be the other old row totals. Its magnitude is
k=delta_i t-u-v. Substituting q=st into (3), the first term sums to
st M_d(delta_i;t). In a cap for row j set z=b-1 and let the remaining
slack be w. Then u+v+z+w=delta_i t-2, and the positive part is
((s-r_j)t+u+z+1)_+. It is exactly J_d(delta_i,s+delta_i-r_j;t).
The baseline is exactly the same J at delta_i-r_j, not an omitted
parent-independent constant. Extracting t^2 proves (2). All identities hold
on shared old-allocation domains; no two independently favorable counts have
been substituted for that common original.

For D=0 use the complete bounded three-variable composition directly and
the accepted A71 actual-degree convention; (2) is not extended through an
empty-width factorial formula. Identical split endpoints have G=0. Forced
zero rows retain (2) and their smaller actual degrees; the following theorem
does not make a generic three-row assertion there.

## 3. Central concavity with TWO OR THREE constrained rows

THEOREM. Let all three rows be positive, let r_1=min_i r_i<D, and suppose
c>=2r_1. Then the ENTIRE G is concave on [r_1,c-r_1]. No other row is
required to be at least D. A point interval at equality is harmless.

Put delta_1=D-r_1 in (0,D), and for j=2,3 set


```text
h_1j=s+D-r_1-r_j.
```

On the claimed interval the singleton C_d(s+delta_1) is terminal because
s>=r_1. The pair complementary to row 1 has argument
c-s+delta_1=r_2+r_3-s>=D because s<=c-r_1; hence F-C there vanishes.
Its correction argument h_23=s-(c-r_1)<=0, so both H terms for that pair
vanish as well. For a constrained row j=2 or 3,


```text
h_1j-delta_j=s-r_1>=0,
```

so H_d(delta_j,h_1j)=-(h_1j-delta_j/2)L_d(delta_j) is affine throughout
the interval, including its endpoint. For an unconstrained row that ordered
correction is absent. These are exact support statements for the full object.

A72 proves global concavity, including EVERY jump, of the complete function


```text
T_delta(h)=F_d(D-h)-C_d(D-h)
                -C_d(D-delta+h)-H_d(delta,h),          (5)
```

for 0<delta<D. Grouping (2) using ONLY the preceding terminal/zero identities
gives on [r_1,c-r_1]


```text
G(s)=an affine polynomial in s
           +T_delta1(h_12)+T_delta1(h_13).             (6)
```

The affine polynomial contains -E(0), all H baselines, the linear L terms,
the terminal singleton, and the terminal H corrections from rows 2 and 3.
In particular none of those baseline constants is discarded when comparing
the value of the gain. Each T uses the same complete old-column caps.
Equation (6) proves the theorem with the full A72 complementary-curvature
and A69 physical-wall arguments already inside T. There is no need to sign
an isolated H jump or infer global concavity from smooth intervals alone.

The actual column-exchange bijection gives G(s)=G(c-s). Thus when c>2r_1,


```text
G(s)>=G(r_1) on [r_1,c-r_1].                           (7)
```

Paying the full endpoint band 0<=s<=r_1 therefore pays every split of this
parent. If c<2r_1, the unpaid half-band is the entire interval 0<=s<=c/2.
The general all-margin gain-sign problem has been reduced, without loss, to


```text
0<=s<=min(r_min,c/2),
```

together with already accepted dominant-row cases. This is a reduction and
an unbounded central-concavity result, not a proof of the remaining endpoint
sign or arbitrary three-row c2 positivity. A69's positive-curvature dominant
endpoint controls continue to rule out universal whole-curve concavity.

## 4. Complete verification and source boundary

Allmargin_v1.py tests (3)-(4) on the complete frozen residual domain, including
k=1 and two negative rows, with wrong-baseline controls. The six selected
original records are checked by the full A65 kernel and the independent
direct-table/bare-LR engines. Three ENTIRE curves retain every knot, label,
offset, reflection, exact interval polynomial and unused rational node.
No finite panel supplies either theorem's unbounded quantifier.

P12 tests the U08 source-derived all-coefficient operation; P34 tests the
U10 source-derived primitive base beyond its earlier total-deficit condition.
Their sources and adoption are in PRIMITIVE-ADOPTION.md and they are excluded
from Pro052 updates. P56 is a root-selected complete all-three-constrained
original outside both source theorem classes and with empty central interval.
It tests the remaining hard band rather than expanding a settled positive
census. All prior negative sector/rest/pair/intercept/birth/residue controls
remain at their exact scopes. Only a negative coefficient of a complete legal
original triggers candidate handling; a failed sufficient gain is not KTT.
