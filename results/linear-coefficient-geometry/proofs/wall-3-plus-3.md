# Complete 3+3 chamber transition

## Original domain and orientation

Let b=(lambda;mu,nu) be a legal balanced rank-six boundary. Let U,I,J be subsets
of {1,...,6}, each of cardinality three, listed increasingly. Set

    b(S) = sum_(a=1)^3 (s_a-a),
    h = b(I)+b(J)-b(U),
    Phi(b) = sum_I mu + sum_J nu - sum_U lambda.

Take two generic cut cells meeting across Phi=0, at a wall point where no
other one of the 7,591 complementary cut groups vanishes. Both sides must be
feasible and full-dimensional in the original hive model. Positive partition
margins are retained. Write g_plus and g_minus for their actual c1 functionals,
with sides labeled by the sign of Phi. All polynomials below are extrapolated
chamber polynomials when evaluated outside their defining chambers; their
values are not silently replaced by actual counts there.

The original root wall is E_U(a)=sum_U a=0 in the A5 root lattice. Its internal
roots are exactly A2 x A2. Its transverse list contains ALL nine edges between
the two blocks. There are b(U) negative and 9-b(U) positive original roots
relative to E_U. The complete Weyl pairs that can change across this one
boundary wall are exactly those with p^{-1}(U)=I and q^{-1}(U)=J. There are
(3! 3!)^2 = 1,296 of them. Every other complete Steinberg term keeps its chamber.

## Full lower-wall polynomial and exact transverse moments

Polarize all transverse roots to beta_(u,v)=e_u-e_v, u in U, v outside U, and
put eta=-sum_(negative original transverse roots) psi. In sorted block order,

    eta_U,a = u_a-a,
    eta_Uc,a = -3+v_a-a,
    E_U(eta) = b(U).

The unimodular Boysal-Vergne jump is, initially at sufficiently large integral
n=E_U(a), the signed sum

    J(a) = (-1)^b(U) sum_(z>=0, sum z=n-b(U))
              k_12(a-eta-sum z_uv beta_uv).                    (1)

Each negative root contributes -sum_(q>=1) exp(q psi), fixing both the sign
and eta shift directly. This direct expansion avoids an apparent sign
inconsistency in the printed kappa-minus convolution discussion. The theorem's
residue definition, original lattice and complete transverse list are unchanged.
Polynomiality extends (1) to a polynomial identity.

The lower-wall polynomial is zero if either lower root chamber is exterior.
Otherwise it is exactly

    k_12(a) = (1+L(a))(1+M(a)),

where L=s a_u and M=t a_v select the first coordinate (sign +1) or negative
last coordinate (sign -1) in their respective ordered blocks. This is the
complete A2 Kostant polynomial: on supported generic supplies it is
1+min(a_1,-a_3), and it is zero on the exterior chamber.

Let N=n-b(U), X=1+L(a-eta), Y=1+M(a-eta). Over all weak compositions of N
into the nine transverse variables, there are binomial(N+8,8) terms. A selected
row sum R and column sum C obey

    E[R]=E[C]=N/3,    E[R C]=N^2/9.

For completeness, among the nine ordered pairs of row/column variables, one
is the same edge and eight are distinct. For nine composition variables,
E[z_i z_j]=N(N-1)/90 for i != j and
E[z_i^2]=2N(N-1)/90+N/9. Summing gives N^2/9 exactly. Thus all lower-wall
terms, including the product term, yield

    J(a) = (-1)^b(U) binomial(N+8,8)
              (X-s N/3)(Y+t N/3).                             (2)

No lower-wall term is truncated. This special factorization uses the complete
3-by-3 transverse list; it is not asserted for unequal block sizes.

## Whole Weyl grouping and the full stretching jump

Define alpha_S=(4-s_1,5-s_2,6-s_3). It is a partition inside the 3-by-3 box.
Define balanced effective triples, outer partition first,

    B_U  = (alpha_U +(3-h/3) 1; alpha_I, alpha_J),
    B_Uc = (alpha_Uc+(h/3) 1; alpha_Ic,alpha_Jc).              (3)

At the actual wall point, let p_U=1+ell_U be the selected complete rank-three
LR chamber polynomial for (lambda_U;mu_I,nu_J), when that lower triple is
feasible. Let p_U=0 for an exterior lower triple. Define p_Uc likewise. Set
A_U=p_U(B_U), A_Uc=p_Uc(B_Uc). For the zero polynomial its linear part is zero.

To evaluate these pieces away from the wall, use the balanced projected triples

    b_U^0  = (lambda_U +Phi(b)/3 1; mu_I,nu_J),
    b_Uc^0 = (lambda_Uc-Phi(b)/3 1; mu_Ic,nu_Jc).

Let L_U(b) and L_Uc(b) be the respective linear parts evaluated at those
projected triples. They restrict to actual rank-three c1 on the wall.
The difference of the two complete rank-six stretching chamber polynomials is

    Delta P_b(t) = (-1)^h binomial(t Phi(b)+8-h,8)
                       (A_U+t L_U(b))(A_Uc+t L_Uc(b)).        (4)

If a lower chamber is exterior the associated factor is identically zero.
The identity is between chamber polynomials; it does not equate actual counts
at an arbitrary off-chamber shifted argument.

Here are the offset and sign details. With rho=(5,4,3,2,1,0), every affected
pair has the same transverse offset

    E_U(p rho+q rho-2rho) = 2b(U)-b(I)-b(J) = b(U)-h.

Thus N=t Phi-h in (2). Decompose p and q into sorted block shuffles and their
four S3 permutations. Their sign product is (-1)^(b(I)+b(J)) times the four
internal signs. Combining it with (-1)^b(U) gives (-1)^h. The two remaining
36-term alternating sums separate, including their exterior terms. Their
arguments, after (2)'s exact N/3 correction, are precisely the original rank-
three Steinberg arguments for B_U+t b_U^0 and B_Uc+t b_Uc^0. This proves (4),
including every rho offset and signed multiplicity.

An explicit independent way to evaluate A_U is to retain all sigma,tau in S3.
At the actual wall slope a=sigma mu_I+tau nu_J-lambda_U, use zero if a_1<0 or
a_3>0; use 1+z_1 if a_1>0, a_3<0, a_2>0; and 1-z_3 if a_1>0, a_3<0, a_2<0.
Evaluate that chosen affine polynomial at

    z = sigma(alpha_I+rho_3)+tau(alpha_J+rho_3)
          -alpha_U-(3-h/3)1-2rho_3,    rho_3=(2,1,0),

and sum with both permutation signs. The complementary rule substitutes
complements and 9-h. No tie occurs under the generic-wall hypothesis.

## Complete c1 transition

For 1 <= h <= 8 the binomial polynomial has a simple zero at t=0, and

    derivative_N binomial(N+8,8) at N=-h
       = (-1)^(h-1) / (8 binomial(7,h-1)).

Taking the first coefficient in (4) gives the exact identity

    g_plus-g_minus = - A_U A_Uc Phi / (8 binomial(7,h-1)).     (5)

The derivatives of the lower factors disappear because they multiply the
binomial's zero. Their complete constant extrapolants remain; replacing them
by one or by positive actual counts would be invalid. This class is locally
concave exactly when A_U A_Uc >= 0.

For h outside {1,...,8}, the binomial's constant B_h=binomial(8-h,8) is nonzero.
Both adjacent feasible whole-LR polynomials have c0=1, so (4) implies
A_U A_Uc=0. The accepted A20 closed-cell transfer implies that g_plus-g_minus
vanishes on the common feasible wall. At a generic wall point with both lower
triples feasible, both rank-three interval lengths L_U and L_Uc are strictly
positive. Equation (4)'s first coefficient on that wall then gives
A_U L_Uc + A_Uc L_U=0. Together these force A_U=A_Uc=0. Consequently the c1 jump
is identically zero. If either lower triple is exterior, the complete factor
was already zero. Thus outside-strip 3+3 transitions vanish at c1 under the
stated two-sided feasible generic hypotheses. This does not assert the
hyperplanes themselves are absent, or discard a whole boundary stratum.

The strict positive lower lengths used here follow because a feasible rank-three
hive is an integral interval. A zero length forces equality in one of its
Weyl inequalities or a partition gap. That is another original rank-six cut
or a forbidden partition tie, excluded at the stated wall point.


The classical premises are Boysal–Vergne, *Paradan’s wall crossing formula for
partition functions and Khovanskii–Pukhlikov differential operator*, sections
2, 3, 4.3 and 5.1–5.3, and Rassart, *A polynomiality property for
Littlewood–Richardson coefficients*. The full original first-jet and closed-cell
arguments are supplied beside this proof. This theorem is a chamber-polynomial
identity, not an instruction to replace an extrapolated factor by an actual
shifted lower-rank count.
