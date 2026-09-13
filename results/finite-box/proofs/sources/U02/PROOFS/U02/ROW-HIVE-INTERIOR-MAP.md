# A complete integer row–hive map for genuine relative interiors

## Explicit whole-object map

Fix lambda outer and balanced partitions mu,nu, padded to n. Use hive coordinates with h(i,0)=sum_(r<=i)mu_r, h(0,j)=sum_(r<=j)lambda_r and h(n-j,j)=|mu|+sum_(k<=j)nu_k. Let a_(r,k) be the complete LR row-count array; a_(r,k)=0 for k>r. Define

    h(i,j)=sum_(r<=i+j) mu_r
             +sum_(r<=i+j, k<=j) a_(r,k).

At the three sides, the row/content equations give exactly those three boundaries. Put Q(r,k)=h(r-k,k)-h(r-k+1,k-1). Then Q(r,k)=sum_(s<=r)a_(s,k), and

    a_(r,k)=Q(r,k)-Q(r-1,k)     for r>k,
    a_(k,k)=Q(k,k).

Both directions are integer linear/affine, homogeneous in the physical stretch. Row sums and content sums telescope to the fixed boundaries; substituting either formula into the other recovers the entire object. In particular the map is not an arbitrary skew-content replacement for an LR family.

Off-diagonal nonnegativity, the complete column inequalities, and the complete lattice-word inequalities are the three hive rhombus orientations under this map. Diagonal nonnegativity is additionally implied by

    a_(r,r)>=a_(r+1,r+1)>=...>=a_(n,n)=nu_n>=0,

using the corresponding complete ballot inequalities. All extra column inequalities beyond the triangular active range reduce to nonnegative partition differences. Therefore the complete real LR row polytope and complete hive coincide under these maps, as do their integer points. The maps do not merely embed a face or a selected support.

## Concrete chart and full row checks

For each of the211 frozen keys, the source program substitutes the already-certified U01 map h=t*b+T*z (including its recorded integer translation) into the displayed formulas. It verifies every row equation, every content equation, the inverse reconstruction of every hive coordinate, and every original rhombus against the full row-constraint roster. Every nonconstant row constraint not itself a raw rhombus is a diagonal nonnegativity implication as above. These coefficientwise comparisons include constants and all free-coordinate coefficients, not merely sample points.

The original U01 selected-coordinate inverse expresses each z as an integer combination of h and t. Combining it with the row–hive inverse gives an integer inverse on the entire affine lattice. Thus the chart's saturated integer lattice is preserved. The tensor count_boundary used in some keys is recorded separately from the original bare triple; its all-stretch polynomial equality remains the exact source tensor word, not a claimed geometric symmetry of arbitrary hives.

## Correct strictness thresholds

A full-dimensional chart is required before using this section. U02 proves that condition for179 keys by explicit strict points, independently replayed in every original rhombus. In that chart each full row inequality has form c*t+a.z>=0. If a is nonzero, it must be strict at relative-interior points and the integer threshold is1. If a is zero, it is a constant boundary condition; a forced zero remains equality, while a positive constant is already satisfied. No coordinate-bound parity is guessed for the32 remaining charts.

These substitutions produce three exact threshold arrays: nonnegative cell counts, column inequalities and ballot inequalities. The independent tableau recurrence uses a_(i,k)>=delta_A, current-prefix upper bounds lowered by delta_C, and ballot caps lowered by delta_B. It keeps all row and content equations. Unused labels are also checked, rather than silently dropping threshold rows. It never swaps the inner partitions of a chart carrying orientation-specific thresholds.

The last-two-row reduction extends exactly. With residual content R, next row a, final row b=R-a and G=M_current-M_last, it uses

    a_k>=max(delta_A(current,k), N_(k+1)-C_k+delta_B(last,k+1)),
    a_k<=R_k-delta_A(last,k),
    2*Aprefix_k-a_k>=Rprefix_k-G+delta_C(last,k).

Together with the complete current-row bounds, these imply every final row condition. Their final two-label intersection is still the exact integer interval from TWO-ROW-TAIL.md with the shifted bounds. Earlier rows retain their full thresholds and future cell-minimum capacities. This gives a complete, independently constructed count of **true relative interiors**, rather than deriving them retrospectively from a fitted polynomial.

## Reconstruction and independence

The H-system counter counts the strict fixed-grade inequalities directly. The row-tableau counter instead counts complete semistandard lattice-word arrays with these exact thresholds. Both count the same whole relative-interior object through the proved maps, but their finite counting representations and algorithms differ. They do not just perform two arithmetic conversions of one count vector. All numerical negative-node values used in the repaired reconstruction are computed by both models, including the proved zeros; signed reciprocity then gives P(-j)=(-1)^D I(j).

For full-dimensional keys, the frozen complete D+1-node grid combines consecutive negative interior sites, zero and smaller positive sites. Hidden-dimensional keys retain the full positive-node fallback. The two positive holdouts are frozen **before mixed determination** and chosen outside both the fit and prior successful positive count observations in this mission for that key. This avoids relabeling earlier determining values as newly reserved checks. The exact amended node roster and all old roles remain preserved.

The classical LR row–hive correspondence is not claimed as a worldwide discovery. The mission contribution is its concrete complete-chart compiler, coefficientwise211-key verification, orientation-specific true-interior recurrence and the measured mixed-node repair. Current timing, full vectors, failures and checks are separate evidence files; this proof alone does not claim whole-box coverage or a universal cheap interior count.
