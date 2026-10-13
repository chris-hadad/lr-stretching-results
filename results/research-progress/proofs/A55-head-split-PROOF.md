# A55: complete initial split and its moment obstruction

Accepted mathematical scope: the complete original parent/count bridge, range/slack kernel and moment-sign obstruction. Origin: Pro044 layered kernels and the independent A55 derivation. General all-coefficient initial splitting remains open.

26 September 2026. Root derivation from the complete Pro044 U09/U10 source kernels and open initial-parent problem. Source credit is retained. The whole character/count bridge is independently rederived below; returned code is inert. This does not prove general sharp head splitting or all K3 positivity.

## 1. Complete original parents and their degree

For any positive integral layer list l=(l_1,...,l_L), put T=sum l and
h=(T,l_1,...,l_L). For each h_j put o_j=4 sum_(q>j) h_q and concatenate


```text
Lambda=(o_j+4h_j,o_j+2h_j)_j,
Mu=(o_j,o_j)_j,  Nu=(6T,4T,2T).                    (1)
```

The skew components are disjoint translated shapes (4h_j,2h_j). Their full
skew Schur function is the product of those Schur functions. Multiply the
leading s_(4T,2T,0) by its Weyl denominator to extract s_(6T,4T,2T). In its
alternant, the exponent 4T+2 must occupy the first coordinate: any later
coordinate would leave a negative exponent. Then 2T+1 must occupy the second
coordinate, for the same reason. Thus only the identity permutation survives,
leaving weight (2T,2T,2T) in the product over the old layers. This argument
holds with T replaced by tT; the offending exponents remain -1, so no affine
shift is discarded.

The bialternant of each s_(4tl_i,2tl_i,0) is the product of three centered
integer root intervals [-tl_i,tl_i]. If f_l,t(s) is the complete convolution
of these one-dimensional intervals over all layers, the full original count is


```text
P_l(t)=sum_s f_l,t(s)^3.                            (2)
```

The underlying flow graph has three vertices and L parallel copies of each
of its three edges. Incidence has rank two, the zero flow is strict for every
positive width, and solving a spanning tree gives a saturated integer lattice.
The degree is therefore 3L-2, and the original rank is 2L+2. This proves a count
identity and actual degree, not an affine hive-metric equivalence. Remove zero
layers before using the rank/degree formula; the all-empty list is a point.

For old positive widths w with N entries and W=sum w, compare the complete
parents with layers (w,W,W) and (w,2W). Their difference G_W has zero constant
and degrees at most 3N+4; the two parents have degrees 3N+4 and 3N+1. Pro044
proved in SOURCE a positive widening derivative and the sharp initial split
through three old widths. Four or more old widths are the open initial problem.

## 2. An exact positive polynomial in range, spread and slack

Let X,Y,Z be three old edge sums, order them, and let x,y be their consecutive
gaps. Put M=x+y, p=xy and u=2h-M. For the two equal new heads of width h,
their whole kernel is


```text
K_h(x,y)=sum_z f_h(z) f_h(z+x) f_h(z+M),
f_h(z)=(2h+1-|z|)_+.
```

At the initial head h=Wt, the complete old range satisfies M<=2Wt, so u>=0.
The merged single head of width 2h has kernel 4h+1-M on this ENTIRE old domain.
Using the four disjoint intervals z<-M, -M<=z<-x, -x<=z<0 and z>=0 in the
full sum, and summing the cubic polynomial on each interval, gives


```text
K_h-(4h+1-M) =
  u + (4/3)M
  + (7/2)u^2 + (19/3)uM + (23/12)M^2 + (7/6)p
  + 2u^3 + 6u^2 M + 4u M^2 + (2/3)M^3 + 2up + pM
  + (1/2)u^4 + 2u^3 M + 2u^2 M^2 + (2/3)u M^3
  + (1/12)M^4 + u^2 p + uMp + (1/6)M^2 p + (1/6)p^2.       (3)
```

This is a formal polynomial identity after 2h=u+M and p=xy, and therefore
holds on every tie, endpoint and parity coset. Integer h entails u+M even;
no extra half-integral lattice points are counted. The complete G_W is the
sum of (3) over ALL old X,Y,Z, with multiplicity f_w,t(X)f_w,t(Y)f_w,t(Z).
This retains the whole initial object and its coupled quartic.

## 3. The precise obstruction to signing these terms separately

The coefficients of (3) are nonnegative, but weighted lattice summation is
not coefficient-positive in the ordinary t basis. Already for one old unit
width, the full fourth-range moment is


```text
R4(t)=sum_(X,Y,Z in [-t,t]) (max(X,Y,Z)-min(X,Y,Z))^4
     =6 sum_(r=1)^(2t) (2t-r+1) r^5.                (4)
```

For a positive range r, there are 2t-r+1 possible minima and 6r labelled
triples with those extrema, including both kinds of ties exactly once.
Faulhaber expansion of (4) has ordinary linear coefficient -2/7. Equivalently,
the derivative at zero is 12*(B_5-B_6)=-2/7. Thus the positive M^4/12 term in
(3) alone contributes -1/42 to the linear coefficient. The whole true split
instead has linear coefficient 12/7 in this control and a positive complete
vector. This is a moment-sign obstruction, not a negative LR polynomial.

The earlier Pro044 coupled-moment obstructions remain distinct source results.
Equation (3) changes the retained complete kernel basis, but does not make its
moments independently positive. Any successful proof from (3) must group/pay
them. Neither pointwise positivity nor positivity of all integer count values
is the missing ordinary-coefficient theorem.

## 4. Exact tests and next discriminator

The root reconstructs both complete original parents before subtracting them.
For N=1..6, equal unit widths and widths (1,2,...,N), all tested sharp initial
differences and both full parents are coefficient-positive. The two N=1 entries
are the same input and are recorded as overlap. The degree bounds above precede
interpolation and two positive grades per parent are unused. These tests extend
the finite adversarial surface; they do not extend Pro044's all-parameter
three-old-width theorem to arbitrary lists. Direct kernel sums, the full R4
polynomial and deliberate endpoint mutations are checked independently in
VERIFICATION.json.


The complete retained finite controls and a portable replay are [PILOT.json](../data/a55/PILOT.json) and [check_initial_split.py](../code/a55_a56/check_initial_split.py). The fresh replay regenerates every retained parent vector and all 372 kernel controls without an LR backend.
