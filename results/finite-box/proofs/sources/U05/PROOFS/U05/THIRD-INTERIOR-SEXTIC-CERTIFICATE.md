# Complete sextic positivity from five counts and a bounded third interior

Let P(t)=sum_{j=0}^6 c_j t^j be the entire nonempty LR stretching polynomial.
Require its actual dimension to be six in a complete saturated integer chart,
with all primitive inward normals of squared Euclidean norm at most six. In
this chart the adopted complete two-cone theorem gives c4>0, while intrinsic
leading and second-leading positivity give c6,c5>0. These are genuine whole
geometric premises, not a fitted degree or a chart of a selected face.

Write A=P(1), B=P(2), C=P(3), U=I(1), V=I(2), W=I(3), with true relative
interiors in that lattice. Actual dimension six makes reciprocity I(j)=P(-j).
Nonemptiness gives c0=1. All six counts are nonnegative integers, but only the
first five will be numerically counted. Put E1=A+U, E2=B+V, O1=A-U, O2=B-V.

The following integer forms involve only those five observed counts:

    T  = 45 O1 - 9 O2 + C,
    L2 = 270 E1 - 27 E2 + 2 C - 490,
    L3 = -13 O1 + 8 O2 - C,
    G4 = -39 E1 + 12 E2 - C + 56,
    G5 = 5 O1 - 4 O2 + C,
    G6 = 15 E1 - 6 E2 + C - 20.

Exact coefficient identities on the complete degree-at-most-six space are

    60 c1  = T - W,
    360 c2 = L2 + 2 W,
    48 c3  = L3 + W,
    144 c4 = G4 - W,
    240 c5 = G5 - W,
    720 c6 = G6 + W.

For example, the first is the odd-part cancellation
45(P(1)-P(-1))-9(P(2)-P(-2))+P(3)-P(-3)=60c1. The other five follow by the same
coefficient comparison. The accompanying checker substitutes every monomial
1,t,...,t^6, with the displayed constants multiplied by c0 for that linear test.
Thus these are full coefficient-space identities, not observed fits.

Because W and every G are integers, strict positivity of c4,c5 yields

    W <= min(G4-1, G5-1).

Likewise c6>0 implies W>=1-G6, in addition to W>=0. The six identities also
show the coefficient lattices directly: 60c1,360c2,48c3,144c4,240c5,720c6 are
integers. This justifies the unit decrements above; a strict real inequality
must not be rounded to an unsupported non-strict bound without integrality.

If L2>=0 and L3>=0, then c2,c3>=0 from W>=0. If an independently proved
upper bound W<=H also satisfies T-H>=0, then c1>=0. The three remaining
coefficients have their separate whole-geometric protections. For strict
positivity, it suffices that L2,L3,T-H are positive. No value is substituted
for an uncomputed W.

The initial upper bound H=min(G4-1,G5-1) costs no additional counting. When
it is insufficient, construct the complete third-interior fixed-grade integer
system and a formal finite box cover as in ADAPTIVE-INTERIOR-UPPER-COVER.md.
Its verified upper cardinality B3 permits H=min(G4-1,G5-1,B3). All inequalities,
rounding deductions, exhaustive two-child splits and contradiction leaves are
retained and independently checked. This is a formal geometric certificate,
not a second numerical I3 computation. A zero bound genuinely proves I3=0;
a positive bound is not assumed sharp.

## Complete finite application

The frozen degree-six roster contains exactly 154,408 normalized target groups. Every
one has a complete whole-hive chart, integer inverse, full forced affine-space
check, explicit strict integer point and the required norm bound. Both complete
counting models independently evaluate A,B,C,U,V. Every request and response
was separately rebound to the complete chart or complete row/content/column/
ballot system. First interiors are actually counted zero; the 93 nonempty
second interiors (maximum two points) are retained in E1,E2,O1,O2.

On all records, the final uniform checker establishes

    L2 >= 799,      L3 >= 49,      T-H >= 1.

The geometric upper bound alone works on 148,251 records. The other 6,157 use
the saved complete formal upper covers, all replayed by the final checker.
Consequently every target's entire polynomial has the uniform lower bounds

    c1>=1/60, c2>=799/360, c3>=49/48,
    c4>=1/144, c5>=1/240, c6>=1/720.

The higher lower bounds follow from their strict signs and integer coefficient
lattices, not from numerical estimation of volume. In 573 cases a zero upper
cover proves I3=0 and the leading interval collapses; 153,835 retain genuine
leading-coefficient uncertainty. No full-vector reconstruction is claimed for
this production class. The separate 256-key complete-vector baseline has its
own determining values, original unused positive holds, and independent check.

DATA/U05/third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz supplies the final
integer forms, entire bare triples, geometry locations/hashes, every fifth-count
premise and the actual upper-cover dependencies. Geometry and independent raw
model bodies remain in DATA/U05/production, not replaced by hashes.

## Scope and provenance

This is a finite whole-count proof for that exact original-box target roster,
plus a generally sound sufficient criterion for complete sextics satisfying the
stated normal/lattice premises. It is not all-size sextic positivity or an
all-rank theorem. The original five-count leading-coefficient enclosure,
failed universal-simplex test, integer-grid refinement and formal-cover repair
remain preserved as substantive intermediate arguments. Elementary finite
differences and reciprocity are inherited; the concrete application here is
the complete checked geometry/count application and the adaptive upper-bound
certificate. The source certificate collection's accepted short-normal, polynomiality and
intrinsic-sign source premises remain mandatory.
