# Complete six-face volumes in three actual ten-dimensional hives

Claim FR027-P09-C002. These are complete geometric and whole-count challenges of the new sixth-coefficient certificate. The underlying Csplit family is source-positive already; neither its positivity nor its whole polynomial formula is claimed as a new discovery. All-stretch identities determine the displayed vectors; they are not under-degree fits to the twelve low-stretch checks.

## Entire LR parents and complete integer coordinates

The three bare triples, with lambda outer, are

    C0: lambda=(37,33,25,15,9,5), mu=nu=(20,16,12,8,5,1);
    C1: lambda=(46,41,31,19,11,6), mu=nu=(25,20,15,10,6,1);
    C2: lambda=(74,66,50,30,18,10), mu=nu=(40,32,24,16,10,2).

They are balanced, have ordinary rank six, and outer sizes124,154,248. C2 is twice C0, retained deliberately as a sixth-power normalization challenge rather than an independent boundary direction. Their actual degrees are10 and codegrees9,5,5. The source complete split parameters (S,A,B) are respectively(1,1,1),(2,1,1),(2,2,2).

The fully read source A004-PRINCIPAL-SPLIT-CONE.md supplies the entire row-count construction. Here it is challenged directly against every original hive rhombus and the saturated integer lattice. Let Y=(y_ij) be a3-by3 nonnegative matrix with total S*t, row totals r_i and column totals c_j, and let

    0<=s<=A*t+c3,        0<=v<=B*t+r1.                    (1)

Nine y coordinates with their total eliminated, plus s,v, give ten integer coordinates. For a_i=lambda_i-mu_i at the current dilated boundary, the full row-count triangle X is

    x11=a1;
    (x21,x22)=(a2-nu2+c2+s, nu2-c2-s);
    (x31,x32,x33)=(A*t+c3-s, s, nu3-c3);
    (x41,x42,x43)=(y11,y12,y13),  x44=a4-r1;
    (x51,x52,x53)=(y21,y22,y23),  (x54,x55)=(v,a5-r2-v);
    (x61,x62,x63)=(y31,y32,y33),
    (x64,x65,x66)=(B*t+r1-v,nu5-a5+r2+v,nu6).

All other entries are zero. In these equations a,mu,nu already denote the boundary at stretch t; S,A,B remain unit parameters. Every row sum and content sum is checked. The complete hive map is

    h(i,j)=sum_(r=1)^(i+j)mu_r
             +sum_(r=1)^(i+j)sum_(ell=1)^j x_(r,ell).    (2)

It gives exactly the three fixed hive boundaries. In the ten selected coordinates z=(y11,y12,y13,y21,y22,y23,y31,y32,s,v), with y33=S*t-sum z1..z8, (2) is h=t*O+U*z. The complete matrices U and U inverse are saved; det U=+1 or-1 and both are integral. Thus no finite-index counting sublattice is substituted.

There are thirteen model inequalities: nine nonnegativities for y, two interval lower bounds and two upper bounds. Each one is literally one of the original45 hive rhombi after (2); all converse row identities are verified. Conversely, every original rhombus is nonnegative at every vertex of (1), proving that the entire model lies in the hive. This tests both directions, not only the image of a selected set of tableaux.

## Complete vertices, dimension and codegree

For S,A,B>0, a vertex has Y concentrated at one of its nine cells and each of s,v at a chosen endpoint. These36 points exhaust the vertices: if a base point is not a simplex vertex, the endpoint graph or interval fiber leaves a nontrivial local segment. Both widths are strictly positive, so the combinatorics is a simplex times two intervals, with affine rather than constant widths. Explicit relative strict points establish dimension10 before any coefficient comparison.

At an integral strict point all nine y entries are at least one, so S*t>=9 is necessary. At t=ceil(9/S), choose positive integral y with the required total. Since A,B>=1, both integral intervals in(1) have a strict integer point. These conditions are sufficient because all original nonzero rhombi are implied by the complete model and are strict at the stored interior points. The resulting true codegrees are9,5,5.

## Exhaustive six- and seven-face rosters

Specify a nonempty support K of r simplex cells, and for each interval specify lower endpoint, upper endpoint or free. If f intervals are free, the face dimension is r-1+f. Positivity of the interval widths excludes additional face collapses.

For six-faces, the three cases are

    f=0,r=7: binom(9,7)*4=144;
    f=1,r=6: binom(9,6)*4=336;
    f=2,r=5: binom(9,5)=126.

Thus every parent has606 actual six-faces. For seven-faces the counts are36,144,84, totaling264. The complete vertex incidences, inward normals and face labels survive in DATA/J06-CONTROLi-GEOMETRY-RAW.json.gz for i=0,1,2. All three parents share the same fixed combinatorial and normal fan; their normalized face volumes differ. They are not three unrelated fans.

Let a count cells of K in column3, b count cells in row1, and o count their common cell in K. The base simplex has normalized volume

    V0=S^(r-1)/(r-1)!.

If neither interval is free, the face volume is V0. If only s is free it is V0*(A+a*S/r); if only v is free it is V0*(B+b*S/r). If both are free it is

    V0*[A*B+(A*b+B*a)*S/r+(a*b+o)*S^2/(r*(r+1))].      (3)

The formula follows by integrating the complete affine widths. On the uniform continuous simplex, E[y_i]=S/r and E[y_i*y_j]=(1+delta_ij)S^2/(r(r+1)). In particular the overlap term o is retained. Omitting it would not be the same complete face volume. The graph/coordinate-selection maps are integral on the saturated face lattice, so these integrals use fundamental-parallelepiped volume one, not factorial-normalized volume. Multiplying six-face volumes by6! would incorrectly multiply the full coefficient sum by720.

## Complete corrected and uncorrected sums

Each six-face has four independent actual extreme normals drawn from the original42-normal atlas. Its full transverse constant is therefore one of the independently verified Unit9 entries, not a selected cell of a larger cone. All606 actual constants in each control are positive before correction, with minimum1363/71400. No negative actual local weight is claimed for these controls.

For each seven-face, restrict every incident six-face conormal to its full saturated rank-seven quotient, divide the gcd of every restricted vector, and weight it by the complete volume(3). Every vector sum is exactly zero. There are264 complete balance equations per parent,792 occurrences in total. Both original and corrected six-face sums agree:

    C0: c6=11261/8640;
    C1: c6=40621/1080;
    C2: c6=11261/135=64*c6(C0).                          (4)

The respective sums of six-face volumes are199/15,5932/15,12736/15, so all three satisfy the new1/3000 bound. Every original weight, corrected weight, volume, saturated quotient and zero balance is stored. The aggregate contains1818 six-face occurrences. These are complete face rosters, not a selection of favorable contributions.

## Independent whole counting and its precise overlap

The inherited complete all-stretch formula is

    P(t)=binom(S*t+8,8)
          *(1+(A+S/3)*t)*(1+(B+S/3)*t).                 (5)

Its full vectors were frozen, and all three sixth entries agree with(4). Their complete values at t=0,1,2,3 are respectively

    C0: 1,49,605,4125;
    C1: 1,320,9295,108108;
    C2: 1,605,19855,243243.

Every value agrees independently between literal ordinary LR reading-word enumeration and the unsigned complete nine-cell/interval sum. The12 sites are occurrence counts: all zero dilations coincide, and C2 at t=1 is C0 at t=2, leaving9 distinct dilated bare triples including the origin. The proof of(5), not a four-node fit, determines each degree-ten polynomial. No additional determining or unused-holdout claim is attached to these low-grade tests.

This gives a material check of higher-face lattice normalization and the complete codimension-four aggregation beyond the earlier edge-length tests. It does not create a new sign discovery in the already proved Csplit family or classify all realized six-face local weights.
