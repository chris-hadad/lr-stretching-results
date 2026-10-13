# A66 independent adoption: interacting originals and the complete rank-seven certificate

Curated mathematical proof from **A66**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Completed Pro048 U04-01/U05-01 are the source; their exact original proof and full certificate byte identities are recorded in this module's source map. The complete character identity and prior degree bound were already adopted at A63 ACCEPTANCE item 5. Root rederived that premise below as a consistency check; A66 does not count it as a new theorem. The new selected adoption is the complete U05 sign, degree and operation certificate. A fresh campaign verifier, without executing provider code, must regenerate the complete finite certificate as numerical evidence. Complete numerical verification is separate evidence; a heading alone does not establish it.

## The complete all-rank character identity

Take m>=2, b>=c>=1, k>=0, 0<=h<=b, 0<=g<=min(c,k). There are m+2 skew rows of widths(u,v,k,w_1,...,w_(m-1)), every long width at least b, and adjacent overlaps(h,g,0,...,0). Construct lambda upwards by lambda_n=d_n, lambda_i=lambda_(i+1)+d_i-e_i, mu_i=lambda_i-d_i; set nu=(sum d_i-b-c,b,c). All overlaps are bounded by both adjacent widths, both shapes are partitions, and the size equation and output dominance follow from the width floors. Interior zero rows remain physical rows.

A nonempty tableau is explicit. Put j=max(h,c); take row multiplicities(u,0,0),(v-j,j,0),(k-g,0,g),(w_1-(b-j)-(c-g),b-j,c-g), followed by all ones. Its entries are nonnegative, the two overlap inequalities ensure strict columns, triple columns receive 1,2,3, and reading all 3s then 2s of row 4 never overtakes the accumulated 2s then 1s. Scaling proves nonemptiness at every positive grade, so P(0)=1.

Let H_j=h_j(1,x,y), D=(1-x)(1-y), R_j=h_j(x,y)-xyh_(j-1)(x,y), with H_j=0 at negative j and R_0=1. Geometric sums give DH_L=1-R_(L+1) and


```text
(1-y/x)R_j=x^j(1-y)-x^-1 y^(j+1)(1-x).
```

In the full dominant coefficient `[x^B y^C](1-y/x)R_j A`, B>=C>=0, j>B, and A with nonnegative exponents, both monomials vanish separately. This remains true with signed coefficients in A. Thus every long H_L, L>=B, may be replaced by1/D in the full highest-weight extraction. It is not a weightwise or raw-character equality.

The first-three-row Jacobi--Trudi matrix has rows

    (H_ut, H_((u+v-h)t+1), H_((u+v+k-h-g)t+2)),
    (H_(ht-1), H_vt, H_((v+k-g)t+1)),
    (H_((h+g-v)t-2), H_(gt-1), H_kt).

Its other five entries meet the long floor. Keeping all six terms and then applying the legitimate replacements gives C/D^2-B0/D^2-AC/D+E/D^2+AB0/D-E/D^2, where A=H_(ht-1), B0=H_(gt-1), C=H_kt, E=H_((h+g-v)t-2). The two triple-column E terms cancel only after full extraction. Multiplying the remaining long factors and the highest-weight prefactor yields


```text
P(t)=[x^(bt)y^(ct)](1-y/x)R_ht(H_kt-H_(gt-1))/D^m.
```

Define the complete band count


```text
F_m(X,Y;l,u)=sum_(a,b>=0,l<=a+b<=u,a<=X,b<=Y)
  binom(X-a+m-1,m-1)binom(Y-b+m-2,m-2).
```

Negative X or Y gives zero. The two monomials in R_ht and symmetry of the remaining band give the ENTIRE identity


```text
P(t)=F_m((b-h)t,ct;gt,kt)-F_m((c-h)t-1,bt+1;gt,kt).
```

Every once-only offset, triple determinant term, band endpoint and zero fiber is retained. Composition coordinates and the two unit-coefficient total equations give the saturated count lattice; no metric correspondence to the original hive is asserted. The first row has no 2s/3s, the second no 3s, and two content equations leave at most2(m+2)-5=2m-1 independent tableau multiplicities, a prior degree bound. The full finite-sum identity below supplies the same chamber degree independently.

## Rank seven: complete finite proof rather than a positive panel

Set m=5. The elementary coefficient of R_j/[(1-x)^(m+1)(1-y)^m] is


```text
A_j(X,Y)=sum_(i=max(0,j-Y))^min(j-1,X)
  binom(X-i+m-1,m-1)binom(Y-j+i+m-1,m-1)
  +1_(X>=j)binom(X-j+m,m)binom(Y+m-1,m-1).
```

Pascal pairing of h_j and-xyh_(j-1) proves the sum and its one unpaired endpoint. Therefore P=A_g(b-h,c)-A_(k+1)(b-h,c)-A_g(c-h-1,b+1)+A_(k+1)(c-h-1,b+1) at grade1, and the corresponding homogeneous parameter substitutions at all grades. Fixed endpoint order makes each summand degree8 and its exact polynomial sum degree at most9. This is a PRIOR mixed-degree bound.

The base forms in parameter order(b,c,k,h,g) are g,c-g,b-c,k-g,h,b-h. All endpoint/sign changes are the eight forms c-h,b-h-g,c-h-g,k-c,k-b,k-b+h,k-c+h,k-b-c+h. At closed walls the possible extra endpoint terms vanish through binomial factors with top below a nonnegative lower index. In particular h=c leaves the second X=-1; k=X0+Y0 leaves upper j=X+Y+1; j=Y0 and X0=j0 retain their once-only offsets. The inaccessible g>b half-space is never used. Thus every chamber formula restricts correctly to its entire closure, not just generic integer interiors.

The finite proof obligations are explicit: enumerate all 1001 four-row intersections among fourteen forms, primitive exact nullspace rays, all 256 wall signs, every full-dimensional feasible cell, and a common pulling triangulation. The expected complete arrangement has 16 rays,27 cells and 30 simplices. Every five-column ray matrix is unimodular, so each integral parameter in a simplex has integral nonnegative coordinates z. Lower-dimensional faces are covered by closures; no coset or magnitude is omitted.

In each cone the degree-nine polynomial H(z) is uniquely determined by all 2002 integral points sum z_i<=9. Independently recover every coefficient and compare every one of the60060 slots with the pinned certificate, including zeros. Then test both UNUSED complete shells sum z_i=10,11:2366 nodes per cone,70980 in total. Full exact symbolic/finite-difference identity, complete cone coverage and the prior degree justify every magnitude. Cardinality or agreement on rays alone does not.

For each of 30 cones and all 31 nonempty coordinate supports, evaluate H(t1_S), recover its actual degree, and prove H(t1_S)>=binom(t+D,D). All930 supports are required. Since each nonzero integral z_i>=1 and all mixed coefficients are nonnegative, H(tz)>=H(t1_S) coefficientwise. The same monomial supports show the degree cannot change within that relative support. The zero support is the point 1. This proves the whole-original simplex reserve through actual degree for every parameter and every closed face.

For b>=c>=1 the degree rules, checked in this ordered form, are: if h=b, degree 0 when g=c, otherwise 4 for k>g and 3 for k=g. If h<b and b=c=g, degree 4. Otherwise at k=0 it is 6 for b=c and 7 for b>c; at k>0 it is 7 for b=c,k=g,8 for b=c,k>g or b>c,k=g, and 9 for b>c,k>g. The c=0 closure with h<b gives 5 for k>0 and 4 for k=0; h=b or b=0 gives a point. The exceptional b=c=g stratum has the exact all-m identity binom((b-h)t+m-1,m-1). It must never be assigned a generic degree.

## Optional operation adoption requires its entire derivative certificate

The source also asserts sharp whole-overlap gains with linear rates 13/12 for decreasing h and 77/60 for decreasing g, and cap-widening rate 1/9 up to k_star=min(b,b+c-h). These enter A66 adoption only if all corresponding mixed derivative maps, shared-face identities and saturation branches are independently verified. With V the cone ray matrix, the physical derivative is obtained using V^-1; its constant coefficient in the parameter polynomial is the derivative of the ORIGINAL linear stretch coefficient. Shared-wall equality then permits integrating each ordinary coefficient. Holding widths fixed preserves output for h/g moves. Increasing k preserves output only with compensating long-width decreases that stay above b. No general row transfer or gain-as-LR claim follows.

The complete ordinary gain at fixed long widths 2 from(b,c,k,h,g)=(2,1,1,0,0) to(2,2,1,0,0) has c8=-1/48 and c9=-1/192, although both endpoints are positive. Thus output-content increase is not coefficientwise monotone. Negative mixed coordinates alone would not prove that failure; the literal full original difference does.

## Exact ceiling and evidence
