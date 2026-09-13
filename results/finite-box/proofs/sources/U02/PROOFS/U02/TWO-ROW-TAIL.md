# Exact two-row tail reduction of the complete LR recurrence

The full row recurrence and its complete semistandard/ballot proof are retained in PROOFS/U01-COMPLETE-ROW-RECURRENCE.md. This refinement concerns only its last two remaining rows, not a restriction of the LR object.

Let C_k be content already read, N_k final content, a_k the next row, and b_k=N_k-C_k-a_k the final row. The next row has its original row sum and all original column and ballot bounds. Write R_k=N_k-C_k, and let G=M_current-M_last. For the final row, nonnegativity is a_k<=R_k. Its full ballot constraints are exactly

    a_k >= N_(k+1)-C_k                      (k below the last label),

because b_(k+1)<=C_k+a_k-C_(k+1)-a_(k+1). The upper bound from the current row and the nonnegative lower bound remain present. For the final column conditions, put Rprefix_k=sum_(j<=k)R_j and Aprefix_k=sum_(j<=k)a_j. The exact condition is

    2*Aprefix_k-a_k >= Rprefix_k-G.

During largest-label-first filling, Aprefix_k is the known remaining total r. Consequently the added constraint is simply a_k<=2r-(Rprefix_k-G). Every final row constraint is retained. There is no independent-factor assumption or omitted ballot wall.

At the last two labels, a_0+a_1=r. Let m_j and u_j be the full lower/upper individual bounds, p_0 the current-row first-prefix upper bound, and h_j=Rprefix_j-G. The possible a_1 form exactly the integer interval

    max(m_1, r-u_0, r-p_0)
        <= a_1 <= min(u_1, r-m_0, 2r-h_1, r-h_0).

Its length, clipped at zero, is the whole two-row completion count for this fixed higher-label prefix. The current-row prefix at label1 and every already-filled higher-label prefix are checked before this step. When only label0 remains, the same conditions are checked directly. Row/content size balance makes the final row sum automatic. This proves the interval summation, including zero labels, empty rows, nonoverlapping skew rows and all equality endpoints.

The version3 implementation uses these bounds and this exact final interval rather than building a memoized final-row state for every possible a_1. Counts use arbitrary-precision integers; row quantities are bounded by the explicit stretched-outer-area450 guard, sufficient for the frozen original-box holdouts through grade14. Unscaled partition and balance validation occurs before t=0 scaling. The older area300 guard and all older C++ sources remain preserved, not silently overwritten.

The repaired implementation is checked against the complete1912-case literal LR roster, large-area low-rank controls and the unchanged full U01/initial-pilot results wherever those determining values are available. These finite tests do not make implementation independence into counting-model independence. The independently derived full H-system model supplies the separate whole-object count comparison. Exact test outcomes are in DATA/U02, and failed/unfinished vector portions stay explicit.
