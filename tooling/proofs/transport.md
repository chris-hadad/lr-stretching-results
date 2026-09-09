# Entire transportation and primitive-segment LR models

## 1. Independent real cut proof

Let r,c and s,d be nonnegative real margins of totals R and S, in the same p by q coordinate system, and put

    delta(r,c;I,J)=r(I)+c(J)-R.

For X in T(r+s,c+d), a decomposition X=Y+Z exists exactly when 0<=Y<=X with margins r,c. A source-row-column-sink capacity network gives the necessary and sufficient cut conditions

    X(I,J)>=delta(r,c;I,J), for every I,J.

This holds over real capacities: the feasible flow set is compact, a maximal flow exists, and a residual augmenting path would contradict maximality; absence of such a path supplies a saturated minimum cut. No algorithmic termination premise for arbitrary real augmentations is needed.

For any nonnegative margins u,v of total M,

    min_(X in T(u,v)) X(I,J)=max(0,u(I)+v(J)-M).

The lower bound follows from margins. Attainment follows by first forming the aggregated 2 by 2 table for I/I-complement and J/J-complement at the lower endpoint, then distributing each block proportionally to its row and column margins. A zero-total group has zero block mass and is filled with zeros; there is no division by zero.

Writing alpha=delta(r,c;I,J), beta=delta(s,d;I,J), universal extraction is therefore equivalent to max(0,alpha+beta)>=alpha for every cut. Complementing both subsets changes (alpha,beta) to (-alpha,-beta). Combining a cut and its complement is precisely alpha*beta>=0. Thus

    T(r+s,c+d)=T(r,c)+T(s,d)
    iff delta(r,c;I,J)delta(s,d;I,J)>=0 for all I,J.

This confirms the returned realization proof, lines 9–70, including zero margins. The 2^(p+q) gate is a finite test, not a variable-rank polynomial-time claim.

For segment margins e=f=(1,1,0,...,0), its delta equals the number of selected distinguished rows/columns minus two. Minimal cuts with positive segment delta select three distinguished indices. They impose exactly

    r1>=B, r2>=B, c1>=A, c2>=A,
    A=sum_(i>=3)r_i, B=sum_(j>=3)c_j.

Extra nondistinguished indices only increase the base cut; the four-selected cut is redundant. Complement cuts cover the negative segment delta. Therefore these conditions are necessary and sufficient, and scaling the segment margins proves the real equality for every m>=0. The source's degree D=(p-1)(q-1) assertion additionally requires its strictly positive base margins; the zero-margin gate itself does not require full dimension.

## 2. Entire transportation-to-LR-row map

Fix p,q>=1, n=p+q-1 and an ordered nonnegative margin sequence r,c of common total M. “Ordered” means fixed labeled order; the individual margins need not be sorted. Define R_i=sum_(u>=i)r_u, C_j=sum_(v>=j)c_v, with R_(p+1)=C_(q+1)=0. The tails are automatically weakly decreasing. Use the fixed rank-n padding of

    Lambda=(M+R2,...,M+Rp,C1,...,Cq),
    Mu=(M repeated p-1 times,C2,...,Cq,0),
    Nu=(R1,...,Rp,0,...,0).

For X in T(r,c), define a(i,j), the number of label i in LR row j, by

    a(j,j)=R_(j+1)                         for 1<=j<p,
    a(i,p-1+k)=X_(i,k)                    for 1<=i<=p,1<=k<=q,
    all other a(i,j)=0.

This is exactly the skew-content lift applied to the suffix skew shape (C1,...,Cq)/(C2,...,Cq), with ordered content r and H=M. Its lower rows have disjoint column intervals, so their semistandard conditions impose no constraint beyond nonnegative entries and the row/content equations. Its top p-1 rows are forced to be superstandard over the reals: inductively, the column inequality for symbol j-1 in top row j, whose inner offset equals that of row j-1, forces every smaller-label entry in row j to zero. The row sum fixes the diagonal entry. Row 1 has only label 1.

The buffer surplus between labels i and i+1 is R_(i+1)-R_(i+2)=r_(i+1). Any lower prefix uses at most the full remaining r_(i+1) entries of label i+1. Therefore all lower ballot inequalities are automatic. Conversely, deleting the forced buffer from any real LR row array gives a nonnegative table with column sums c and label/content sums r. The inverse is explicitly

    X_(i,k)=a(i,p-1+k).

No external face or additional tableau is admitted. Both maps are linear in the table entries and margins, with integer coefficients, so they identify the whole real polytopes and their full affine integer lattices. The same proof handles zero rows, zero columns, zero content entries and M=0. At M=0 both fibers are points.

The accepted proof is the included skew-lift note. Canonical `constructions.py:33–39` states the lift, and lines 54–64 implement its tail/buffer formula while preserving the ordered content. The matching maintained entrypoint is `skew_content_to_lr(C,C[1:],r)`; its nonnegative ordered-content contract includes the segment. Lines 84–87 and 103–110 explicitly identify disconnected-row tableaux with transportation entries in the capped-matrix use. The present argument applies that accepted lift directly to general transportation margins; it does not depend on the Schur scalar product alone.

## 3. Explicit conventional-hive chart and inverse

For 0<=i<=j<=n, write

    H(i,j)=sum_(v=1)^j Mu_v
              + sum_(u=1)^i sum_(v=u)^j a(u,v),
    h(x,y)=H(y,x+y),       x,y>=0, x+y<=n.

Then

    h(x,0)=sum_(v<=x)Mu_v,
    h(0,y)=sum_(v<=y)Lambda_v,
    h(n-y,y)=|Mu|+sum_(u<=y)Nu_u.

These are exactly `hive.py:7–18` and `hive_boundary` lines 203–218, with Mu on the x-axis and Nu on the diagonal. Mu and Nu have not been interchanged.

The inverse uses integer differences:

    a(i,i)=h(0,i)-h(1,i-1),
    a(i,j)=h(j-i,i)+h(j-i,i-1)
             -h(j-i+1,i-1)-h(j-i-1,i),       i<j.

To verify that this is an isomorphism of the **entire** polytopes, match all three rhombus orientations from `hive.py:159–170`:

1. For x+y+2<=n, the rhombus
   h(x+1,y)+h(x,y+1)-h(x,y)-h(x+1,y+1)
   is the LR column slack in row j=x+y+2 for symbol k=y+1.
2. For y>=1, the rhombus
   h(x,y)+h(x+1,y)-h(x,y+1)-h(x+1,y-1)
   is the ballot slack for label k=y at row j=x+y+1.
3. For x>=1, the rhombus
   h(x,y)+h(x,y+1)-h(x+1,y)-h(x-1,y+1)
   equals a(y+1,x+y+1).

Thus every off-diagonal a(i,j) is nonnegative. The diagonal ballot inequalities give a(i,i)>=a(i+1,i+1), and a(n,n)=Nu_n>=0, so all diagonal entries are nonnegative as well. The remaining column inequalities, with symbol k>=j, reduce to Lambda_(j-1)>=Lambda_j. Boundary telescoping supplies exactly the row and content equations. These identities prove both directions over the reals and show that all hive lattice points, including those in a degenerate affine span, have integral inverse row arrays. No hive condition has been omitted.

Composing with section 2 gives the promised entire transportation-to-conventional-hive isomorphism. Since it and its inverse have integer coefficients, it identifies affine spans intersected with their ambient integer lattices; this is a full lattice statement, not just a count bijection.

## 4. Boundary linearity transfers the real Minkowski gate

Denote the composition by Phi_(r,c). At fixed p,q and padding, every tail, buffer entry and hive partial sum is linear. Hence

    Phi_(r+s,c+d)(X+Y)=Phi_(r,c)(X)+Phi_(s,d)(Y).

The inverse extracts the same fixed row-count coordinates at every boundary and is likewise additive. Therefore the cut criterion of section 1 is equivalent to

    H(Lambda(r+s,c+d),Mu(r+s,c+d),Nu(r+s,c+d))
      = H(Lambda(r,c),Mu(r,c),Nu(r,c))
        +H(Lambda(s,d),Mu(s,d),Nu(s,d))

as entire real conventional hive polytopes in the same rank-n coordinates. This proves more than the returned count bridge. It applies to this explicit tail-constructed family; it does not furnish a cut test for arbitrary hive boundaries.

Fixed padding is essential. `constructions.py:24–26,62–64,148–152` trims trailing partition zeros, while `hive.py:199–200` chooses rank from the lengths supplied to `hive_boundary`. The theoretical family must retain or restore rank n=p+q-1 before coordinate addition. Trimming may change the standalone rank of the segment from seven to five. Re-padding restores the forced empty rows and the common chart; silently adding two different ambient hive vectors is not meaningful. The formulas extend to real margins analytically; this does not assert that the integer-only constructor API accepts arbitrary real inputs.

## 5. The exact rank-seven segment and quotient lattice

For p=q=4 and e=f=(1,1,0,0), the padded boundary is

    a: Lambda=(3,2,2,2,1,0,0),
       Mu=(2,2,2,1,0,0,0), Nu=(2,1,0,0,0,0,0).

Write its 2 by 2 table as (z,1-z;1-z,z). In LR rows, changing z affects only labels 1,2 in rows p,p+1. In the hive formula it changes only h(p-1,1), with coefficient +1. Thus its entire conventional hive is exactly an integral endpoint plus [0,1] times that coordinate unit vector. At rank seven this is h(3,1). The varying coordinate runs from 8 to 9 in this rank-seven chart. This establishes primitivity directly in the conventional integer hive lattice.

For a strictly positive base satisfying the four inequalities, projection of the table difference lattice that forgets the distinguished 2 by 2 block has kernel Z times (+1,-1;-1,+1). Any signed integer outside array obeying the nondistinguished row and column equations leaves balanced integer 2 by 2 margins; assigning one integer entry determines the other three integrally. This proves saturation of the quotient image. Under the four inequalities every nonnegative outside array has nonnegative remaining distinguished margins, so it has a real and integral 2 by 2 completion. The image is the entire claimed outside polytope.

Writing a=(r3,...,rp), b=(c3,...,cq), its lattice count is exactly

    q_(a,b)(t)=sum_Z product_i(t*a_i-row_i(Z)+1)
                      product_j(t*b_j-column_j(Z)+1),

where Z has nonnegative integer entries and the indicated exterior row/column caps. Each factor counts a split of one remaining slack between two distinguished coordinates. Its degree is D-1 with D=(p-1)(q-1), because the strictly positive base has dimension D and this projection removes exactly the one direction. The integral transportation polytope projects integrally in the certified quotient lattice. The hive isomorphism identifies this with the corresponding conventional-hive quotient along h(p-1,1), including its lattice.

Real fibers grow by m times the primitive segment. At integer m,t, endpoint translations are integral and each nonempty integer quotient fiber gains exactly m*t lattice points. Hence, for the **whole** conventional hive and ordinary LR count,

    P_m(t)=P_0(t)+m*t*q_(a,b)(t).

For the base r=c=(2,2,1,1), this gives the source's b+m*a family, with b=((10,8,7,6,4,2,1),(6,6,6,4,2,1,0),(6,4,2,1,0,0,0)), degree nine and quotient degree eight. If an actual quotient ordinary coefficient q_j<0 is later certified, choosing an integer m> [t^(j+1)]P_0/(-q_j), and m>=0, gives the negative full coefficient. The present argument supplies the geometric and lattice bridge, not that missing negative coefficient.

## 6. Asymmetric failure and its valid chamber repair

For r'=(1,3,1,1), c'=(2,2,1,1), the cut I={1}, J={1,2} has base delta=-1 and segment delta=+1. The gate fails. The supplied table

    X=((0,0,1,1),(2,2,0,0),(1,0,0,0),(0,1,0,0))

belongs to T(r'+e,c'+f). Its distinguished first row contains zero main-block mass, while every segment table requires one unit there, so no segment summand lies below X. Its positive-support graph is a forest, making it a transportation vertex. The new integral affine isomorphism takes it to a conventional-hive vertex outside H(b')+H(a); its explicit interior coordinates are retained in the check output. Thus failure is transferred geometrically too, without native enumeration or a t=1 count argument.

For m>=1, margins (1+m,3+m,1,1),(2+m,2+m,1,1) satisfy the four inequalities. The source's repaired branch B_m=B_1+(m-1)t*q22 follows. The m=0 branch must remain separate. At m=0, using the larger unrestricted q22 instead of the actual constrained projection is invalid. The returned low-dilation numerical cancellation does not repair that geometric failure.

The computation proof's generic 2 by 2 completion interval is correct: for balanced nonnegative remaining margins R1,R2,C1,C2 its lattice count is min(R1,C1)-max(0,R1-C2)+1. In the symmetric case it becomes Lt-max(U,V,S-U,S-V)+1, and summing threshold intervals gives its stated aggregated formula. These elementary identities have no missing configurations. The geometry and count identities do not supply any missing negative quotient coefficient or unauthenticated full polynomial.

