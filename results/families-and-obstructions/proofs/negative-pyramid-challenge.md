# Complete positive surplus and positive average do not settle the parent

This is an exact hand derivation in the standard integer lattice. This is a classical Reeve/pyramid construction, not a newly discovered negative polytope and not an ordinary LR counterexample. No whole-LR realization is supplied. It tests the surplus/average operation at its complete-object scope.

## 1. The entire lattice polytope and its exact series

For an integer m>=2 take the Reeve tetrahedron

    T_m=conv(0,e1,e2,(1,1,m)) in Z^3.

Its affine span is R^3 and its ambient affine lattice is Z^3. In the homogenized vertex cone, the fundamental half-open parallelepiped has one degree-zero lattice point and m-1 degree-two lattice points. Explicitly, for k=1,...,m-1, coefficients

    (k/m,1-k/m,1-k/m,k/m)

on the four degree-one vertices give the lattice point with spatial coordinates (1,1,k) and total degree two. The z-coordinate fixes k and the integrality of the other coordinates fixes the other three coefficients, so this is the complete list. Hence

    sum_(t>=0) L_T(t) z^t = [1+(m-1)z^2]/(1-z)^4.

Form TWO successive unit-height lattice pyramids. Equivalently, in Z^5 take the simplex whose six vertices are the four vertices of T_m padded by two zeros, together with e4 and e5. All six vertices are integral and affinely independent; the saturated ambient lattice is Z^5. Its normalized volume is m.

For a unit-height pyramid, slicing by the integer apex coordinate gives the complete identity L_pyr(t)=sum_(s=0)^t L_base(s). This is a bijection on every integer slice, not a proper-face approximation. Thus the entire five-dimensional polynomial is

    P_m(t)=binom(t+5,5)+(m-1)binom(t+3,5)
          =binom(t+3,3)*[1+(10-m)t/20+m t^2/20].            (1)

This is valid for every nonnegative integer t, including the zero binomial endpoints. The positive coefficient m/120 proves actual degree five, consistently with the vertex determinant. Roots -1,-2,-3 and P_m(-4)=-(m-1) prove actual codegree four by reciprocity.

## 2. Complete coefficients and exact boundary

Expansion of (1) gives

    P_m(t)=1+(140-3m)t/60+(46-m)t^2/24
             +(m+16)t^3/24+(m+2)t^4/24+m t^5/120.         (2)

At m=46, c1=1/30, c2=0 and every other coefficient is positive. At m=47,

    P_47(t)=1-t/60-t^2/24+21t^3/8+49t^4/24+47t^5/120.    (3)

Thus the first two coefficients are strictly negative even though all counts are nonnegative. The complete positive counts P_m(1)=6 and P_m(2)=m+20 are immediate from the full series. The first interior is I_m(4)=m-1.

The source codegree-four coefficient conditions give U<=min(4*6+21,10*6-15)=45. They accept m=46 and reject m=47 exactly. The displayed higher coefficients are positive directly; this example is not claimed to satisfy the LR short-normal chart hypothesis.

## 3. The complete surplus and the average are nevertheless positive

Put B_4(t)=binom(t+3,3). Direct substitution, or [the surplus theorem's](interior-surplus.md) complete residual-degree-two formula, gives

    S_4(t)=I_m(t+4)-P_m(t)
          =(m-2)*B_4(t)*(1+t/2),
    M_4(t)=[I_m(t+4)+P_m(t)]/2
          =(m/20)*B_4(t)*(t^2+4t+10).                    (4)

For every m>=2, S_4 is coefficientwise nonnegative and M_4 is strictly coefficient-positive. Yet P_m=M_4-S_4/2 has the two negative coefficients in (3) at m=47. This is a full-polytope challenge, not a negative local weight or an incorrect count formula.

At m=46 even the quadratic RESIDUAL in (1) has a negative linear term while the entire P has no negative coefficient. The binomial factor supplies real compensation; positivity of each formal residual is not necessary.

## 4. What this rules out and what it does not

The false inference 'positive reflected average plus positive shifted-interior surplus implies a positive original polynomial' is ruled out. So is replacing the combined coefficient inequality by a test of only the average or only a finite set of positive counts. The actual LR question remains the missing constraint that bounds the entire surplus relative to its positive average.

This construction has no declared ordinary LR rank, no homogeneous full-LR inverse, and no ordinary-negative LR example. It is not a new negative inside the finite LR box. The general availability of negative lower Ehrhart coefficients is already documented in Hibi--Higashitani--Tsuchiya--Yoshida, arXiv: 1506.00467; the elementary full construction above is included so no unexamined theorem from that paper is load bearing.
