# Complete quotient polytope and its zero-grade premise

This supplies a needed premise beyond the pre-test segment-family note. Agreement of (P3-P2)/t at positive integers alone would not justify inserting Q(0)=1 into a fit. The following complete homogeneous lattice model does.

For t>=0 introduce z_ij>=0, i=1,...,5 and j=1,2,3. Require each column sum2t, row4 sum2t, row5 sumt, and z51=0. Write ui=sum_j zij for i=1,2,3; their sum is3t. The only remaining column inequalities are

3t-u3 + sum_(k<j) z3k >= sum_(k<=j) z4k, j=1,2,3,
sum_(k<j) z4k >= sum_(k<=j) z5k, j=2,3.

The omitted j=1 lower inequality is exactly0>=z51, already retained as equality. These are all the conditions for a three-letter SSYT in the bottom three rows of skew shape(3t,2t,t)/(3t-u3), together with two detached weak row words of lengths u1,u2. The three first-row lengths are allowed to vary freely subject to their total, and all content is(2t,2t,2t). Restriction/union gives the exact Q count defined in the segment identity. At x>=2 the first two skew rows of the parent are detached, because their separating gaps are(x+1)t>=3t and every ui<=3t; therefore this model omits no parent-tail comparison.

This is a bounded homogeneous rational polytope. Every variable is at most2t. Its saturated lattice has nine free integer coordinates: all six entries in rows1 and2, z41,z42,z52. Read these coordinates for the integer inverse. The remaining entries are

z43=2t-z41-z42, z53=t-z52, z51=0,
z31=2t-z11-z21-z41,
z32=2t-z12-z22-z42-z52,
z33=-t-z13-z23+z41+z42+z52.

All defining equalities are thereby eliminated integrally. At t=6 take rows1,2,3 each(2,2,2), row4=(6,4,2), row5=(0,2,4). Every non-forced nonnegativity and each of the five remaining column inequalities is strict. Consequently the actual dimension is nine; no hidden affine equation remains.

Its Ehrhart quasipolynomial has Q(0)=1. The complete parent identity P3(t)-P2(t)=t Q(t) for all positive integer t, and inherited LR polynomiality, force period collapse: each residue-class constituent agrees with the same degree-at-most-nine polynomial on infinitely many positive integers, hence identically. In particular the residue-zero constituent at0 equals that polynomial and equals1. Thus Q is a genuine degree-nine polynomial with constant1, not a formal positive-grade fit. P3 and P2 have roots-1,-2; the polynomial identity forces Q(-1)=Q(-2)=0. Ten sites-2,-1,0,...,7 determine it. Positive8,9 are unused holds;10 is extra.

An independent direct finite count follows from this model. Write row4=(a,b,c), c=2t-a-b, row5=(0,d,t-d), with0<=d<=min(t,a), a+b>=t. Let R=(2t-a,2t-b-d,t-c+d), all components nonnegative. Sum over r=(z31,z32,z33), 0<=ri<=Ri, satisfying r1+r2+r3<=3t-a, r2+r3<=t+c and r3<=t. For each such r the detached rows have exactly product_i(Ri-ri+1) fillings. Summing these weights is the ENTIRE Q(t); it is independent of Jacobi–Trudi cancellation. This count is not claimed to preserve ordinary positivity term-by-term.
