# The complete shifted-interior surplus at low codegree defect

This is a symbolic derivation, without an independent computational check in
this note. No historical priority claim is made. The Ehrhart polynomial, its true reciprocity interiors, and the elementary interior-translation inclusion are the only mathematical premises. No nonnegative h-star assumption is made.

## 1. Complete objects and hypotheses

Let Q be a nonempty bounded rational polytope of actual dimension d, full dimensional in its specified lattice chart, with period-one Ehrhart polynomial P(t), P(0)=1. All statements also apply to an entire stretched LR count after the complete homogeneous real/integer chart, saturated lattice and actual dimension have been established. Let I(j) count the TRUE relative-interior lattice points of jQ. By reciprocity I(j)=(-1)^d P(-j) for positive integers j. Let q be the least j>0 with I(j)>0, and put

    B_q(t)=binom(t+q-1,q-1),  r=d-q+1.

Codegree gives the distinct roots -1,...,-(q-1), so q<=d+1 and P=B_q R with R(0)=1, degree r, and positive leading coefficient. Here r is the residual degree, not the ordinary LR rank. No degree is inferred from a few values.

Choose any lattice point w in relint(qQ). For each integer t>=0, translation by w injects every lattice point of tQ into relint((t+q)Q). Indeed every facet slack at w is strictly positive, every facet slack at a point of tQ is nonnegative, and they add under this translation. This is a complete inclusion, including t=0; it requires neither IDP nor unique first interiors.

Define the COMPLETE surplus and its symmetric average:

    S_q(t)=I(t+q)-P(t)=(-1)^d P(-t-q)-P(t),
    M_q(t)=(I(t+q)+P(t))/2=P(t)+S_q(t)/2.

Thus S_q(t)>=0 at all nonnegative integer t. This pointwise fact will NOT by itself be promoted to coefficient positivity.

## 2. Parity and exact polynomial classification

The factor B_q obeys B_q(-q-t)=(-1)^(q-1) B_q(t). Hence S_q=B_q K, where

    K(t)=(-1)^r R(-q-t)-R(t),
    deg K <= r-1,
    K(-q-t)=(-1)^(r+1)K(t),
    K(0)=kappa=I(q)-1>=0.

The leading term of R cancels in K. Moreover K(t)>=0 at every nonnegative integer t, because B_q(t)>0 there. Put z=t(t+q). Centering at -q/2 gives the following COMPLETE possibilities:

    r=0: K=0;
    r=1: K=kappa;
    r=2: K=kappa*(1+2t/q);
    r=3: K=kappa+lambda*z;
    r=4: K=(1+2t/q)*(kappa+lambda*z).

In the last two cases lambda>=0. A negative lambda would make K(t) negative for all sufficiently large positive integers, contradicting the proved injection. There is no missing term: centered even polynomials of degree at most two are affine in z, while centered odd polynomials of degree at most three have the factor t+q/2 and an affine residual in z.

### Surplus theorem

If q>=d-3, equivalently r<=4, every ordinary coefficient of the COMPLETE surplus S_q(t) is nonnegative.

This is a coefficientwise theorem obtained from the degree, roots, parity AND the complete translation inclusion. It is not a general assertion that positive counts or positive-count differences have nonnegative coefficients.

## 3. A positive averaged polynomial, without assuming reflection

If r<=3, define T=R+K/2. It obeys T(-q-t)=(-1)^r T(t), has constant 1+kappa/2 and the same positive leading term as R. Consequently

    M_q(t)=B_q(t)*(1+2t/q)^(r mod 2)
                    *(1+kappa/2+eta*t(t+q)),                 (1)

where eta=0 for r=0,1 and eta>0 for r=2,3. For r=0, kappa=0. Each factor is coefficient-positive through its actual degree. Thus if q>=d-2,

    M_q(t) is strictly coefficient-positive;
    I(t+q)=M_q(t)+S_q(t)/2 is strictly coefficient-positive.

Neither M_q nor the inhomogeneous polynomial I(t+q) is asserted to be an entire LR stretching polynomial. In particular their constant terms need not be one. Equation P=M_q-S_q/2 retains the full subtraction; their positivity does NOT prove P positive.

For r=4 the surplus conclusion remains proved, but the averaged residual has degree four and can have an uncontrolled middle parameter. The positive-average conclusion is NOT asserted there.

## 4. Finite reflection rigidity

The following equalities are equivalent to the COMPLETE reflection P(-t-q)=(-1)^d P(t), under the stated degree/codegree hypotheses:

* For r<=2, it suffices that I(q)=1. It is necessary as well.
* For r<=4, it suffices that I(q)=1 and I(q+1)=P(1). They are necessary as well.

For the first assertion kappa=0 makes every possible K of residual degree at most two vanish identically. For r=3 or 4, kappa=0 and S_q(1)=0 force lambda=0, since B_q(1)>0 and z(1)=q+1>0. The converse follows directly from S_q=0.

These are exact finite rigidity tests, not an inference from several favorable samples without a degree bound. They concern true interiors; a mistaken affine hull or parity invalidates them. Reflection plus r<=3 proves all coefficients of P positive by (1) with kappa=lambda=0. In particular:

    q>=d-1 and I(q)=1  ==> complete ordinary positivity;
    q>=d-2, I(q)=1, I(q+1)=P(1) ==> complete ordinary positivity.

At r=4 the same finite test proves reflection, but reflection alone is not promoted here to positivity. A separate source proof gives a quintic codegree-two coefficient test.

The previously recorded rank-seven finite-box control A has d=5,q=3,I(3)=1 but I(4)=21>P(1)=14. It is exactly the first residual degree where the single-count test is inadequate. Its surplus is

    S_3(t)=(7/12)*binom(t+2,2)*t(t+3),

which is nonzero and coefficientwise nonnegative.

## 5. Quantitative compensation instead of universal cancellation

For r=2 the entire residual is

    R(t)=1+eta*t(t+q)-kappa*t/q, eta>0.                      (2)

For r=3 it is

    R(t)=1+(2+kappa)*t/q
           +(eta-lambda/2)*t(t+q)
           +(2eta/q)*t^2(t+q), eta>0.                      (3)

Thus kappa<=q^2*eta in (2), or lambda<=2eta in (3), are sufficient coefficient-positive RESIDUAL criteria. They are stronger than positivity of the entire P, whose binomial factor can compensate a negative residual coefficient. No universal bound of that strength is inferred from the injection.

For r=3 there is also a complete, finite, exact threshold for the WHOLE polynomial. Let

    A(t)=B_q(t)*[1+(2+kappa)*t/q+eta*t(t+q)*(1+2t/q)],
    H(t)=B_q(t)*t(t+q).

Then P=A-(lambda/2)H. The coefficients of H are strictly positive in degrees 1 through d-1 and zero at degree d. Therefore P is coefficientwise nonnegative if and only if

    lambda <= min_(1<=k<=d-1) 2*[t^k]A/[t^k]H.             (4)

This finite symbolic coefficient threshold includes every completion term. It is not asserted satisfied by every LR family. [The twice-pyramided Reeve example](negative-pyramid-challenge.md) gives an entire integral polytope with positive M_q and S_q but negative P, showing why that missing bound matters.

## 6. Scope

This is an all-dimension theorem about low codegree defect, with conditional entire-LR applicability. It does not prove that all 1,279,898 bound-five evaluation keys have such codegree or satisfy the rigidity/compensation conditions. No new finite-box entries are verified here. A whole-box conclusion would
require actual membership in these hypotheses or a complete alternative certificate.
