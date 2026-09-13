# Exhaustive compression to 637 inhabited coefficient profiles

FRONTIER-025 P05. Originating proof. All definitions are those of proof 017. This is a count-preserving reduction, not an affine-hive classification or a bounded parameter search.

## 1. Ten and only ten first-block types

The constraints (1) of proof 017 reduce the minimum (6) as follows. Here u=(x,y,z), x+y+z=2t. A type is identified by the displayed exact integer conditions; its width M is not the stretch variable.

| Type | Conditions | M | m(u) |
|---|---|---|---|
| D | d<=e, g1>=d | d | Mt-x |
| G1 | d<=e, g1<=d-2 | g1 | Mt-x+y |
| DH | d<=e, g1=d-1 | d-1 | Mt-x+min(y,t) |
| E | d>=e+2, g2>=e+2 | e | Mt+z |
| G2 | d>=e+2, g2<=e | g2 | Mt-y+z |
| EH | d>=e+2, g2=e+1 | e | Mt+z-(y-t)_+ |
| T00 | d=e+1, g1>=e+1, g2>=e+2 | e | Mt+z-(t-y)_+ |
| T10 | d=e+1, g1=e, g2>=e+2 | e | Mt+z-2(t-y)_+ |
| T01 | d=e+1, g1>=e+1, g2=e+1 | e | Mt+z-|t-y| |
| T11 | d=e+1, g1=e, g2=e+1 | e | Mt+z-2(t-y)_+-(y-t)_+ |

Proof of exhaustion and formulas: if d<=e, the fourth form dominates the third. The second does also, because g2>=2e-d+2>=d+2. Comparing the remaining first and third forms leaves (g1-d)t+y; its three integer cases give D/G1/DH. If d>=e+2, the third and first dominate the fourth: use x+z<=2t and g1>=2d-e-2>=e+2. Compare the second and fourth forms through (g2-e)t-y, giving E/G2/EH. In the remaining integer case d=e+1, (1) forces g1>=e and g2>=e+1. When g1>=e+1 the first dominates the third; otherwise g1=e. When g2>=e+2 the second dominates the fourth; otherwise g2=e+1. Split at y=t. For y<=t the possible minima are the third or first; for y>=t they are the fourth or second. Direct subtraction gives the four T rows. Ties are retained and agree. No noninteger strip has been rounded away: boundary parameters are integral throughout.

The admissible widths have one core and one unbounded branch:

| Type | Core M | Unbounded M=M0+x, x>=0 |
|---|---|---|
| D,G1,DH,G2 | 1 | M0=2 |
| E | -1 | M0=0 |
| EH,T00,T01 | 0 | M0=1 |
| T10,T11 | 1 | M0=2 |

These are 20 top profiles. On every unbounded branch m>=0 on the entire u-simplex, and its slope in M is exactly t. Neither upper overlap remains active there. Hence the entire count is affine in M on that branch; it is not claimed affine across its exceptional core.

## 2. Exact top representatives and the overlap gates

Each type can be represented by the following (g1,g2,d,e), preserving m(u) for every t,u:

    D:   (M,M+2,M,M)
    G1:  (M,M+4,M+2,M+2)
    DH:  (M,M+3,M+1,M+1)
    E:   (M+2,M+2,M+2,M)
    G2:  (M+2,M,M+2,M)
    EH:  (M+2,M+1,M+2,M)
    T00: (M+1,M+2,M+1,M)
    T10: (M,M+2,M+1,M)
    T01: (M+1,M+1,M+1,M)
    T11: (M,M+1,M+1,M).                       (13)

The representative also preserves every nonzero upper overlap in (8). For G1/DH/T10/T11, an active first-gap-one flag occurs exactly at M=1; for G2 it occurs at the second gap at M=1; for EH/T01 at the second gap at M=0. Any apparent first-gap-one ambiguity in D at M=1 or T00/T01 at M=0 is irrelevant, because m>=0 forces u1<=t there. In E at M=-1, m>=0 forces u3>=t, so neither u1 nor u2 can exceed t. Every other relevant gap is at least two. These implications follow directly from the table, so this is not an inference from finite agreement.

The third gap enters (8) only through whether it is one or at least two. Use representative g=1 or g=2 accordingly. No count dependence on a larger A3-a remains.

## 3. Sixteen and only sixteen tail profiles

The product of h's and the two-row Schur function are symmetric in the three tail letters. Relabel them canonically so the p active indices A come first, their k=|C| unit-cap indices first among these, then the s=|S| single-hinge indices; a surviving pair flag occupies the last inactive index. The exact kernel (10)-(12) depends only on

    p, k, s, j=|J|, and the integer B.

Here j is zero or one. The complete possibilities are:

| Profiles | p | k | s | j | B |
|---|---:|---:|---|---:|---|
| P0-Ss | 0 | 0 | 0,1,2,3 | 0 | >=1 |
| P1-C1-Ss | 1 | 1 | 0,1,2 | 0 | 1 |
| P1-C0-Ss | 1 | 0 | 0,1,2 | 0 | >=2 |
| P2-S1 | 2 | 0 | 1 | 0 | >=2 |
| P2-S0 | 2 | 0 | 0 | 0 | >=2 |
| P2-PAIR-Ck | 2 | 0,1,2 | 0 | 1 | 1 |
| P3 | 3 | 0 | 0 | 0 | >=3 |

There are 4+3+3+1+1+3+1=16 rows after expanding the finite choices.

Proof: at p=0, B=b>=1. At p=1, B equals the sole active vi; it is one precisely at a unit-cap label. No pair can survive, because its complementary pair then has sum greater than b+1. At p=2, B is the sum of the two active contents minus b. Since the remaining content is at most a+1, B>=1, and B=1 holds exactly when that remaining content equals a+1. It is then at least b+2, not a single hinge. If any active content is one, the other is <=b, forcing B<=1; so that case is necessarily this pair profile. If neither is one and B>=2, the remaining content can be b+1 or >=b+2, giving P2-S1/S0. At p=3, B=a-b+2>=3. A content one would force sum(v)<=2b+1, contradicting sum(v)=a+b+2>=2b+3. Thus there are no cap labels. At most one content can equal a+1: two such contents would force sum(v)>=2a+3>a+b+2. This exhausts all sorted positive tails, including equalities.

On each tail profile the kernel and the correction (12) are affine in B, with flags fixed. Its unbounded branch starts at B0=1,2 or3 in the table; otherwise B=1 is fixed.

## 4. Every profile is a whole LR family, not just a sufficient formal cone

For each allowed B construct (a,b,v) as follows. Sort v decreasing after making the listed multiset.

- p=0: b=B, use s copies of b+1 and 3-s copies of b+2.
- p=1: b=B, use one B, s copies of b+1, and 2-s copies of b+2.
- p=2 without a pair: b=B, v=(B,B,B+1) at s=1, or (B,B,B+2) at s=0.
- p=2 with a pair: at k=0 take b=3, v=(2,2,5); at k=1 take b=2, v=(1,2,4); at k=2 take b=1, v=(1,1,3).
- p=3: b=B, v=(B,B,B).

In each case set a=sum(v)-b-2. The displayed B range gives a>b>=1 and max(v)<=a+1, and substitution verifies every profile flag and the specified B. These formulas realize ALL values on each unbounded branch, not merely its starting point.

Choose a top representative (13) and g=1 or2. Set

    A3=a+g, A2=A3+g2, A1=A2+g1,
    alpha=(A1,A2,A3,a,b),
    beta=(A1-d,A2+d-e-2,A3+e,v1,v2,v3).        (14)

The first three beta entries are sorted by (1), positive, and their sum is A1+A2+A3-2. Their connection to the tail needs A3+e>=v1. This is automatic when g>=2 or e>=0. In the sole remaining case E-core, e=-1, g=1, it requires v1<=a, thereby excluding the three pair profiles. No other exclusion is needed. The first dominance gaps are d, e+2, 2, 2+a-v1, all positive. The fifth is beta6>0. Thus (14) gives legal strict data and the whole rank-six constructor (5) for every allowed parameter pair.

There are therefore exactly

    20 * 16 * 2 - 3 = 637                      (15)

inhabited profiles in THIS count classification. It is not 637 distinct polynomials or 637 affine-equivalence classes of hives. Some profiles yield identical polynomials.

Conversely, every strict five-row/six-label boundary with Delta3=2 has one top-table type and width, one tail-table profile and width, and one third-gap flag. Its full count is preserved by (13)-(14), using the proof of overlap-gate preservation and the exact kernels, at every t. This is the exhaustion bridge that turns the finite certificate into an all-parameter theorem.

## 5. Bilinear ordinary-positive membership: the remaining finite test

Let a profile have top M=M0+x if unbounded, otherwise x=0, and tail B=B0+y if unbounded, otherwise y=0. Both x,y are nonnegative integers. Equations (7)-(12) give exactly

    P_(x,y)(t)=P00(t)+x V(t)+y W(t)+xy Z(t).    (16)

There is no x^2 or y^2 term: on the top branch all u are admitted, the multiplicity increases by xt, and the overlap gates are fixed; the complete tail is affine in B. Inhomogeneous endpoint corrections remain in P00,V,W,Z. Each of these polynomials lies in the prior space (4), because it is an exact difference of actual whole LR counts of the same degree and codegree profile. For example V=P10-P00 and Z=P11-P10-P01+P00; it is their ORDINARY coefficients that need checking. Positivity of the four corner counts alone would not suffice.

Proof 019 verifies P00>=_coeff Pmin>0 and V,W,Z>=_coeff0 in all 637 profiles, using every determining site of the prior space. This proves actual membership, not a hypothetical positive cone without a coverage or realization argument. It also proves coefficientwise monotonicity in these two profile widths only, not in arbitrary LR boundary coordinates.
