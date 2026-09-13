# A symmetric positive cut functional and an unbounded-rank whole-LR c1 cone

This is an AI-assisted symbolic proof. Source SHA-256:
`d7f3bef6d35d68f70cc89e1159c537a677e4de0d321035707bb41e418d4459ce`.
The universal remainder-vanishing statement is explicitly not proved.

## 1. Exact positive cut part

Let r and c be positive integral margins with p rows, N columns, total M, p,N>=2. For nonempty proper subsets use

    b_p(I)=beta(|I|,p-|I|),   b_N(S)=beta(|S|,N-|S|).

The complete sum of all one-class and two-class contributions from the complete partial-fraction source proof has linear coefficient

    C_(p,N)(r,c)=H_(N-1)(M-r_1)
      -sum_S b_N(S) sum_(proper I containing 1) b_p(I) (c(S)-r(I))_+.    (1)

Every proper I containing 1 occurs exactly once in the pair formula: j is its least missing row index and U consists of its indices above j. Thus (1) is the complete pair sum, not a selected set of favorable assignments.

Surprisingly, its distinguished-row appearance disappears:

    C_(p,N)(r,c)
       = (1/4) sum_(nonempty proper I,S) b_p(I)b_N(S)
          min(r(I),M-r(I),c(S),M-c(S)).                 (2)

This formula is symmetric under row/column permutations and transposition.

Here are complete normalization details. For any k>=2,

    sum_(proper nonempty I subset[k]) beta(|I|,k-|I|)=2H_(k-1).

For the row subsets containing 1 their weight sum is H_(p-1). For any i!=1 their total weight with i omitted is exactly 1: for each size a,

    binom(p-2,a-1) beta(a,p-a)=1/(p-1),

and there are p-1 sizes. Consequently

    sum_(I containing 1) b_p(I)(M-r(I))=M-r_1.           (3)

Put Phi(C)=sum_(I containing 1) b_p(I)(C-r(I))_+ and
A(C)=sum_(all proper nonempty I) b_p(I)(C-r(I))_+.
Complementing I and using x_+-(-x)_+=x gives

    Phi(C)+Phi(M-C)=A(C)+(M-r_1)-H_(p-1)C.              (4)

Column complementation gives sum_S b_N(S)c(S)=MH_(N-1). Substitution of (4) in (1), followed by x_+=(x+|x|)/2 and the same row symmetry, gives

    C_(p,N)=M H_(p-1)H_(N-1)/2
              -(1/4)sum_(I,S)b_p(I)b_N(S)|r(I)-c(S)|.  (5)

Finally, for a,b in [0,M],

    min(a,M-a,b,M-b)=(M-|a-b|-|a+b-M|)/2.

After summing, the two absolute-value terms have equal sums by column complementation. Their total weight is 4H_(p-1)H_(N-1), proving (2).

## 2. Positivity, concavity and a quantitative bound at exact scope

Each minimum in (2) is a minimum of linear forms. Thus C is a nonnegative, jointly concave, homogeneous function on the closed balanced nonnegative margin cone. It is superadditive there. If all margins are positive and

    epsilon=min(min_i r_i,min_j c_j),

every cut in (2) is at least epsilon, giving

    C_(p,N)(r,c)>=H_(p-1)H_(N-1) epsilon>0.             (6)

These properties are proved for the full positive cut functional. They are NOT asserted for the whole transportation coefficient outside the scope of Section 4.

## 3. The exact remainder and what would complete a general theorem

Let R_(p,N)(r,c) be the complete sum of signed ordinary first jets of every class assignment in (4) of the complete partial-fraction source proof with at least three occupied classes. Then

    [t]P_(r,c)(t)=C_(p,N)(r,c)+R_(p,N)(r,c).             (7)

This defines the remainder from a full finite count identity. It is not an unspecified error or an estimate on omitted tableaux. In four rows its exact evaluation is the A3 gradient at the affine offset given in the four-row chamber formula. For arbitrary p it is the corresponding type-A vector-partition chamber first jet, with the offset (5) of the complete partial-fraction source proof and the actual eventual chamber, including ties.

The conjecture R=0 for all positive margins is stronger than a claim justified here. The inherited three-row result and N=4 four-row certificate, together with the selected N=3,5,6 systems, support it. None proves arbitrary N. Another possible positive result would be R>=-C; a negative entire polynomial would require R<-C at a legal whole boundary. A negative assignment sector alone establishes neither.

For all-one n-by-n margins, (2) reduces without an exponential subset enumeration to

    C=(n^2/4)sum_(i,j=1)^(n-1)
             min(i,n-i,j,n-j)/(i(n-i)j(n-j)).            (8)

The exact values at n=2,...,9 agree with the author-maintained Birkhoff table (see source record). This is a primary-source regression, not an independent recount and not a proof of R=0 for all n. In particular, it would be improper to promote it to general transportation c1 positivity.

## 4. A whole-family theorem without assuming any cancellation

Distinguish any row r_1 and put rho=M-r_1. Let c_(1)<=c_(2) be the two smallest column margins. Assume

    rho<=c_(1)+c_(2).                                  (9)

Every assignment using at least three classes has at least two columns outside class 1, provided it uses class 1 at all. Their total C_out is at least c_(1)+c_(2). Its first simple-root target is

    (rho-C_out)t-n_out,

where n_out>=2. This is negative for all t>=0 under (9). Assignments not using class 1 also have negative first target. Thus EVERY higher-class scalar term is actually absent, not merely conjecturally zero at linear order. Equality in (9) is covered because the negative offset persists.

Therefore on this entire closed homogeneous margin cone,

    [t]P_(r,c)(t)=C_(p,N)(r,c)
      >=H_(p-1)H_(N-1)epsilon>0.                       (10)

The number of rows and columns is arbitrary. The inequality is sufficient, not necessary; it does not characterize all positive transportation coefficients. Zero rows or columns are outside the statement and must first be deleted. In (1)-(6) they are allowed only as boundary arguments of the defined functional, not by silently keeping the wrong polynomial degree.

## 5. Entire LR bridge, actual rank, degree, and lattice

The complete transportation/LR construction is
[the whole-count theorem](transport-whole-lr-bridge.md). Its hypotheses and
count map are given explicitly below.

Set row tails R_i=sum_(k=i)^p r_k and column tails C_j=sum_(k=j)^N c_k. Define

    lambda=(M+R_2,...,M+R_p,C_1,...,C_N),
    mu=(M repeated p-1 times,C_2,...,C_N),
    nu=(R_1,...,R_p).                                  (11)

These are weakly decreasing integral partitions. The size difference is sum_i R_i=|nu|, so they are balanced with lambda outer. The skew Schur function for the outer/inner pair is a product of h_(c_j) and the Schur function indexed by (R_2,...,R_p), on disjoint row/column components. The skew diagram (R_1,...,R_p)/(R_2,...,R_p) is in turn a disjoint collection of rows of lengths r_i. Hall adjunction therefore makes its LR coefficient the inner product of product_i h_(r_i) and product_j h_(c_j). The Cauchy identity identifies this with ALL nonnegative matrices of margins r,c. Every shape and offset scales by t, so the equality holds for every nonnegative integer stretch; t=0 is 1. This is a complete alternative count proof, not a claimed affine isomorphism of all hive and matrix coordinates.

For positive margins the ordinary rank of (11) is p+N-1: lambda has exactly that many positive parts, mu has one less and nu has p. Its size is

    (p-1)M+sum_(i=2)^p R_i+sum_(j=1)^N C_j.

For the matrix lattice, the upper-left (p-1)-by-(N-1) entries are free integer coordinates. The last row and column are integral affine functions of them. Thus this is the saturated lattice Z^((p-1)(N-1)), not a finite-index sublattice. The real point x_ij=r_i c_j/M is strictly positive, giving full dimension

    D=(p-1)(N-1).

The bipartite incidence matrix is totally unimodular (orient the edges and delete one redundant conservation row); hence the margin polytope is integral. Its entire Ehrhart polynomial, and therefore (11)'s entire LR polynomial, has degree D. These facts are independent of a fit.

Theorem (10) is consequently a whole-LR c1 theorem at unbounded ordinary rank, not a face/projection claim. It does not settle any whole ordinary rank or the general KTT conjecture.

## 6. A separating example and the unresolved remainder

The cone (9) is larger than the all-coefficient subcone of [the near-corner proof](transport-near-corner.md). Rows (11,1,2,2), columns (3,3,3,3,4) satisfy rho=5<=6, while their smallest column 3 is below rho-min(1,2,2)=4. The near-corner proof derives a separate full polynomial for this challenge, and the independent comparison verifies its c1=19/2 against both (1) and (2) and literal full-matrix counts.

Whether the higher-class first jets vanish in (7) remains unresolved; a
normalized two-class table does not decide it. A possible negative-integer Dyson/residue explanation requires a valid map from that identity to these individual chamber continuations and their shifts. An analytic continuation of a global constant term alone would not prove the needed sector statement. No such map is claimed here.
