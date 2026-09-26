# Third correction

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. Expand the complete bounded tails before cancellation

The whole interval identity is

    P=Pcritical(x)-2pQ^3+3 sum_(j=1)^(2p-1) F(N(j),N(2p-j)),
    F(f,g)=fg(2Q-f-g).

On this strip 2p<=6x, so j<=6x-1. The COMPLETE bounded cumulative count is therefore exactly

    N(j)=U(j)-rU(j-L)+cU(j-2L).

There is no third subtraction, whose first nonzero argument would require j>=3L+1=6x+4. Write

    f=U(j), g=U(2p-j), d=rU(j-L), e=rU(2p-j-L),
    a=cU(j-2L), b'=cU(2p-j-2L).

Products ab', ae and b'd vanish identically: their simultaneous strict support would require 2p>=3L+2, already greater than6x. In contrast de can be nonzero and MUST remain.

The original second-strip polynomial, denoted P2cont, retains the unshifted F and both single first-subtraction terms. Its formal evaluation is well-defined here, but it is no longer a count by itself. The exact extra difference is the sum of

    de(2Q-2f-2g+d+e)

and

    a g(2Q-2f+2d-g-a) + b' f(2Q-2g+2e-f-b').

These identities follow by expanding the cubic F. All products eliminated above are justified by literal supports, not by assigning signs to them.

## 2. Regroup all terms at their true common endpoint

Define, for ell=1,2,

    Dcal_ell(w,x)=sum_(u=1)^(2w-3)
          U(u)U(2w-2-u)U(u+ell L),

with empty sums zero. Let A_r(z), B_r(z) be the COMPLETE inherited auxiliaries:

    A_r(z)=binom(2z+2r-1,2r+1),
    B_r(z)=sum_(k=0)^r binom(r,k)^2 binom(2z+3r-k-1,3r+1).

After translating the first-shift intersection by j=L+u and the second-tail region by j=2L+u, BOTH have u+v=2w-2. Reflection interchanges u,v. The simultaneous first-shift term becomes

    6r^2[Q A_r(w-1)-2 Dcal_1(w,x)+r B_r(w-1)],

while the complete second-tail term becomes

    6c[2Q A_r(w-1)-2 Dcal_2(w,x)+2r Dcal_1(w,x)
                                         -(c+1)B_r(w-1)].

Therefore, at every homogeneous grade,

    P=P2cont+Theta_r(w,x),
    Theta_r=6r(2r-1)Q A_r(w-1)
          -6r(r-1)Dcal_2(w,x)
          +6r^2(r-3)Dcal_1(w,x)
          +6[r^3-c(c+1)]B_r(w-1).                         (T)

This is the complete correction. Neither summand above can be omitted.

There is a finite polynomial form, not an unevaluated growing sum. With the exact mixed E_(r,h) from U10,

    Dcal_ell(w,x)=sum_(k=0)^r
         binom(ell(2x+1)+k-2,k) E_(r,r-k)(w-1/2).           (D)

Vandermonde expands U(u+ell L), and the complete mixed generating series gives (D). Every term has degree at most3r+1. The arguments w-1 and w-1/2 retain the literal2w-2 endpoint; they are not altered original boundaries or lattices.

For w=0 or1 the true sums are empty. The polynomials vanish there by their common integer-root factors, including all terms of (D). At x=w=0, binom(-1,0)=1 is the empty falling product; it must not be rejected by a count-only nonnegative-top guard. All other affected binomial factors vanish. Hence Theta has zero constant and the WHOLE polynomial retains constant1. This does not identify the constants of separately collapsed strict regions with literal zero-grade sets.
