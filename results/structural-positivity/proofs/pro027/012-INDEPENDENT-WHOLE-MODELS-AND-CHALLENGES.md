# Two entire counting models and their exact limits

## Unsigned full-table product

The fresh Python implementation multiplies the complete column generating polynomials h_n(x,y,z,1), retaining every coefficient in the three minor-row cap box. Its Kronecker spacing in the first two exponents is respectively2r1+1 and(2r1+1)(2r2+1), so multiplying two capped arrays cannot wrap an excess first/second exponent into a false legal monomial. The digit base is a power of 256 larger than the product of all column composition counts binom(n+3,3); no coefficient carry is possible. Masking discards exactly entries above a row cap, which can never return to a legal exponent under nonnegative convolution.

The generic table product passed 133 brute-force checks and produced all 15 reference-parent values. Completion of that preliminary computation could not be confirmed, so the comparison below uses a separate completed computation.

The implementation sharing the six small-column factors reconstructs all 105 family parameter/stretch values through t14, including the reference parent at h0. It checks 14 tiny shared/generic comparisons first. The full terminal cap in [Complete ordinary positivity of a rank-ten cap-release family](011-COMPLETE-RANK10-CAP-RELEASE-FAMILY.md)(1) is applied after coefficient extraction; omitting it would replace every initial parent by P6 and is false already at h5,t1 by 1.

## Signed complete assignment model

Use the source Lagrange identity h_n(x1,...,x4)=sum_i x_i^(n+3)/product_(j!=i)(x_i-x_j). At occupations(n1,...,n4) the full graph has ni+nj labeled edges on i->j, sign(-1)^(n2+2n3+3n4), and target t(C_i-r_i)+(i-1)ni-sum_(j>i)nj. These constants are retained exactly.

Order rows(7+h,5,4,1). A class4 assignment has last target 3n4+t(C4-1)>0 whenever n4>0, because every column is at least 2. No acyclic flow can have a positive sink netflow. Thus those assignments are exactly zero at all nonnegative stretches, not silently discarded as an approximation. The remaining3^7=2187 labeled assignments are represented by 189 grouped records: choose classes for the two distinguished columns, and a three-part allocation of the five equal columns, with its exact multinomial weight. All 189 records survive in every node's raw output, including zero counts.

Let(a,b,c)=(n1,n2,n3), with total 7. The three simple-root targets are
X=t(C1-7-h)-b-c, Y=t(5-C3)-2c, Z=t.
The full empty-sink contraction is
sum_(y1+y2+y3=t) B_a(y1)B_b(y2)B_c(y3)
 K_A2(X-y1,Y-y1-y2),
where K_A2(U,V)=sum_(z=0)^min(U,V) B_(a+c)(z)B_(a+b)(U-z)B_(b+c)(V-z).
This uses the actual full nonnegative A2 count, not one chamber polynomial outside its range. Negative targets count zero. B_0(y) is 1 for y0 and 0 otherwise, so occupation-zero strata retain the right dimension and all counts.

The fresh C++ program computes K_A2 from the independent horizontal/vertical composition grid and a diagonal prefix pass for EVERY repeated(1,1) edge copy. This is exactly the complete root-flow generating product. It uses Boost cpp_int, separately from the Python carry-free integer encoding. Complete assignment summation then yields the whole table polynomial. A separate implementation recounted the reference parent at all 15 sites and computed all 105 family sites with 189 exact assignment records each. Both computations completed.

## Reconciliation and polynomial determination

The comparison verifies all 105 distinct family parameter/stretch agreements, all 189 grouped records per node and their total labeled weight 2187, and the complete signed sum. Separate Newton forward differences at the consecutive mixed nodes-6,...,12 reconstruct all seven vectors and agree with the original Lagrange arithmetic on all 133 coefficients. The 14 positive unused holds13/14 pass in both models. Fifteen additional reference-parent checks are permutation-overlap evidence, not15 new independent family sites.

The six full cap-shell differences have 108 strictly positive nonconstant entries. Independent multiplication of t(t+1)...(t+17)/18! reproduces the last-shell vector. The complete cut functional equals all seven independently reconstructed c1 values. DATA/RECONCILIATION.json preserves the full arrays and all qualifications.

Model independence here is full positive matrices versus complete signed repeated-root assignments. Arithmetic independence is CPython integers/Fractions versus Boost multiprecision integers for the counts; both polynomial reconstructions use Python Fraction with distinct Lagrange/Newton algorithms. External independent verification, a generic speed guarantee, and independence from the source formulas are not claimed. The fast grouped assignment count benefits from this exact unit last row, five equal columns and small complete A2 grids; its cost does not establish performance for arbitrary transportation instances.

## Research limits and negative observations

The original general S_(a,0)=0 problem is not solved: [Two exact residue involutions and the irreducible odd-multiplicity problem](009-RESIDUE-INVOLUTIONS-AND-ODD-REDUCTION.md) reduces even layers and protects b=c, while [The odd fifth layer and the complete six-layer consequence](010-ODD-FIVE-CERTIFICATE-AND-SIX-LAYERS.md) establishes a5 and consequently a6. Odd a>=7 off the diagonal, the other support chambers, other empty positions and the generic whole E_full remain open. The specified pilot's448 unshifted zeros are bounded evidence only.

The nonzero altered-weight values in the pilot and involution checks are preserved at auxiliary linear-coefficient scope with exact source/parameters and both finite coefficient formulas. They are not whole LR polynomials. None of the new whole parents or their six shell vectors is ordinary-negative. No LR counterexample is obtained, and the original-box coverage is unchanged.
