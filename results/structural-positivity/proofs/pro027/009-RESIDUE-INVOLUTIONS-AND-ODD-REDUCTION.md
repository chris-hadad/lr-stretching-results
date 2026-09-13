# Two exact residue involutions and the irreducible odd-multiplicity problem

This proof concerns the complete unrestricted insertion moment, an auxiliary functional distinct from a full LR polynomial. The source hypotheses and the separate relation to whole-parent counts retain their stated scope.

## The source functional and analytic form

For positive integers a,b,c, set N=a+b+c and B_m(x)=binom(x+m-1,m-1), interpreted as a polynomial when its argument is negative. Let F_A be the complete shifted A2 chamber polynomial in the A2 chamber derivation, equation(1), at offset(-b-c,-2c). Define

D_e(a,b,c)=[L] sum_(x+y+z=L) B_a(x+e)B_b(y)B_c(z)F_A(-x,-x-y).

The sum is polynomial at every nonnegative integral L. Its degree is at most 3N-3, and its dependence on e is polynomial of degree at most a-1. The unshifted actual insertion functional is e=0. Other e are explicit altered auxiliary weights, not legal LR operations.

By the source generating identity and negative-axis beta functional, put s=1+u and r=1+v to obtain

D_e(a,b,c)=-Res_(s=1) Res_(r=1) integral_0^infinity A^a B^b C^c s^e dw ds dr/(w s r),                 (1)

A=w²s³r/[(s-1)(1+ws)(1+wsr)],
B=1/[(r-1)(1+wr)(1+wsr)],
C=r/[(r-1)(1+w)(1+ws)].

Multiplying these factors recovers precisely the numerator w^(2a-1)s^(3a-1+e)r^(a+c-1) and all four source denominators, with poles(s-1)^a(r-1)^(b+c). Thus (1) is a direct rewriting, not a new source premise. The identity extends to integer e<0 by polynomial dependence on e (or directly by the finite coefficient extraction); these values remain auxiliary.

The residue extractions and integral commute for positive a,b,c. On sufficiently small complex neighborhoods of s=r=1, all factors1+w,1+ws,1+wr,1+wsr are bounded away from zero by constant multiples of1+w, uniformly for real w>=0. Each fixed residue derivative is therefore integrable, behaving as O(w^(2a-1)) at zero and O(w^(-2b-2c-1)) at infinity. Any terms of a subsequent finite expansion with exponent a=0 are instead assigned their identically zero s-residue *before* integration; they do not require a divergent off-residue integral.

## The positive-pair involution

Consider T:(w,s,r)->(ws,1/s,r). Direct rational multiplication gives

T(B)=B, T(C)=C, T(A)=1+B-C-A,                           (2)
T*(dw ds dr/(wsr))=-dw ds dr/(wsr).

For an explicit verification of the nontrivial identity, put X=w,Y=ws. Then
A=g(Y)/(Y-X), T(A)=-g(X)/(Y-X),
g(z)=rz³/[(1+z)(1+rz)]
=z-1-1/r+r/[(r-1)(1+z)]-1/[r(r-1)(1+rz)].
Taking the divided difference gives 1+B-C. The logarithmic Jacobian of T is-1.

Rescaling the w path is first valid for positive real s near 1 and then by analytic continuation throughout the residue neighborhood. The inversion s->1/s is an ordinary local holomorphic change of coordinate at s=1; its differential sign is already included in the Jacobian. There is no extra contour-orientation sign to insert.

For a>=1,b,c>=1 and every integer e, multinomial expansion now gives the finite uniform identity

D_e(a,b,c)=-sum_(i+j+k+h=a) a!/(i!j!k!h!) (-1)^(i+k) D_-e(i,b+j,c+k),                           (3)

where D_e(0,b,c):=0 denotes the vanishing residue, not an occupation-zero graph theorem. Every term with i>=1 is within the positive-parameter source functional. No boundary of a moving simplex has been omitted in (3).

At e=0, isolating the i=a term yields

[1+(-1)^a]D_0(a,b,c)
 =-sum_(i+j+k+h=a,1<=i<a) a!/(i!j!k!h!) (-1)^(i+k)D_0(i,b+j,c+k).                               (4)

For every even a, the multiplier on the left is 2. Consequently all even layers follow inductively from lower odd layers. The universal unshifted zero assertion is equivalent to its odd layers; after the source a=1 and a=3 the first genuinely new obligation is a=5. In particular the entire a=4 layer is zero for all positive b,c, using only the established source layers1,2,3. This is an all-parameter recurrence, not an extrapolation from numerical tables.

For odd a, the left multiplier is ZERO. Formula(4) supplies a compatibility identity among lower layers, not a solution for D_0(a,b,c). This loss of rank is a material generality challenge and is retained explicitly.

## The negative-pair involution

The different transformation U:(w,s,r)->(wr,s,1/r) gives

U(A)=A, U(B)=-C, U(C)=-B,
U*(dw ds dr/(wsr))=-dw ds dr/(wsr).

The same convergent change-of-variable argument gives

D_e(a,b,c)=(-1)^(b+c+1)D_e(a,c,b).                       (5)

Therefore
D_e(a,b,b)=0 for EVERY a,b>=1 and integer e.             (6)

This is a uniform all-a vanishing plane even for the deliberately altered weights. It does not imply that unequal b,c vanish. The source S_(a,e)(b,c) polynomial in the insertion-moment derivation, equation(5) has a symmetric positive factorial prefactor apart from(-1)^(b-a+1). Combining that prefactor with(5) gives
S_(a,e)(b,c)=-S_(a,e)(c,b).
The identity holds on the full positive integer grid, hence as a polynomial in b,c; in particular b-c divides S_(a,e). This conclusion concerns the numerator polynomial, not a claimed analytic continuation of lattice occupations.

## Actual chamber consequences and remaining bridges

On the strict C3 cone X>Z,Y>X+Z the complete empty-terminal assignment first jet is Z D_0(a,b,c). The source reversal gives C2's corresponding D_0(c,b,a). On C5 the full internal wall has normal derivative(-1)^(a+b-1)D_0(b,a,c)(X+Z-Y), including its initial band and every term. Thus any proved consecutive zero layers1,..., m extend the chamber conditions to a<=m on C3, c<=m on C2, and a,b<=m on C5. Formula(6) separately gives C3 zero for b=c with unrestricted a (and the corresponding source-reversed C2 condition). These statements retain exact support conditions; other chambers, empty positions and fully occupied sectors are not inferred.

The full transportation coefficient remains c1=D_cut+E_full. A zero unrestricted moment is not itself a whole-parent positivity theorem. The complete initial wall is generally nonzero at higher orders, as the source(2,3,2) example shows. Subsequent finite odd-layer certificates and whole-parent calculations are separate records.

## Challenges

The finite checks verify both rational maps at 64 non-pole rational points, the full recurrence at 28 nonzero altered-weight cases, the swap identity at those same cases, and 200 diagonal triples. Six negative auxiliary observations were recorded separately from the identity comparisons; none is an LR counterexample. The known e=1,a=2,b=1,c=4 value-1/74256 is reproduced and its swapped value is equal, exactly as(5) requires. Sixteen cases also agree with the independently expanded beta integral, which does not use source S or its Rodrigues reduction. These finite tests challenge the uniform derivation; they do not replace it or claim an independent arithmetic engine.
