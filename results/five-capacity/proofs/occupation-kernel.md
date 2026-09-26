# Complete positive three-occupation kernel

Accepted Astra008 derivation of the auxiliary kernel. The complete character,
lattice, offsets and eventual polynomiality are supplied by the
[three-row character proof](character-three-row.md). The kernel alone does
not sign the whole LR polynomial.

Let p >= 2 and q,r >= 1 be integers, n=p+q+r. Set a=p+q-1, b=p+r-1, c=q+r-1 and (A0,B0)=(-q-r,-2r). Let F_L and F_R be the complete chamber polynomials in the cited proof. Define

    kappa = (2p-3)!! (2q-3)!! (2r-1)!!
            / [2(p+q-2)(2n-5)!!],

with (-1)!!=1. The claim is

    (-1)^q F_L(A0,B0) = (-1)^q F_R(A0,B0) = 0,
    (-1)^q grad F_L(A0,B0) = (kappa,0),
    (-1)^q grad F_R(A0,B0) = (0,kappa).

Thus a supported positive-slope occupation contributes kappa min(A1,B1). At A1=0 or B1=0 the original negative offsets give eventual empty support, agreeing with zero. At A1=B1>0 the offset picks a chamber, and both jets agree along that direction. The complete contribution is kappa max(0,min(A1,B1)).

## Right chamber as a finite derivative sum

Write s=p+q-2 >= 1. In the reflected chamber formula the binomial involving B has top s-1 at B0 and degree s+2r+j-1. It has a single zero factor, for every j=0,...,s. Therefore all constants and the partial derivative with respect to A vanish. Its derivative with respect to B is

    (-1)^(j-1) (s-1)! (2r+j-1)! / (s+2r+j-1)!.

The other binomial has top p-r-2-j and degree s-j. Use

    binom(p-r-2-j,s-j) = (-1)^(s-j) binom(q+r-1,s-j).

After the original assignment sign, the exact right kernel is

    R = (-1)^(p-1) sum_(j=0)^s (-1)^j
          binom(p+r+j-2,j) binom(q+r-1,s-j) B(s,2r+j),       (1)

where B(s,x)=(s-1)!/[x(x+1)...(x+s-1)]. This formula has no singular denominator at any positive integer r and includes every zero binomial endpoint.

## A contiguous Dixon–Dougall evaluation

This step uses the classical Dixon and Rogers–Dougall sums, DLMF equations 16.4.4 and 16.4.9, respectively. They are source premises, not new campaign summation theorems:

- https://dlmf.nist.gov/16.4.E4
- https://dlmf.nist.gov/16.4.E9

First hold integer p,q fixed and take real r>p-2, r>0, so the displayed hypergeometric denominators below avoid nonpositive integers. Put

    a=2r, b=p+r-1, h=r-p+2=1+a-b,
    T_j=(a)_j (b)_j (-s)_j/[j! (h)_j (1+a+s)_j],
    D=sum_(j=0)^s T_j,
    V=sum_(j=0)^s (a+2j)T_j/a.

Dixon gives D=0. Indeed its gamma quotient contains 1/Gamma(2-p), with every other gamma factor finite at this initial domain. Its convergence condition is a-2b+2s=2q-2>-2. The series terminates, and the same conclusion follows by continuous parameter specialization inside that convergent domain; no nonzero tail is retained.

Insert c=(a+1)/2 in Rogers–Dougall and d=-s. The c numerator and its matching denominator cancel, and (1+a/2)_j/(a/2)_j=(a+2j)/a. The terminating sum is

    V = (1+a)_s (3/2-p)_s / [(h)_s (r+1/2)_s].            (2)

The condition Re(b+c+d-a)<1 is 3/2-q<1 and holds for every q>=1; termination is also sufficient. This is the terminating 5F4 specialization of the cited formula.

In (1), factor C=binom(q+r-1,s) B(s,2r). The remaining finite series has denominator (a+s)_j instead of (1+a+s)_j. Their ratio is (a+s+j)/(a+s), so

    R = (-1)^(p-1) C [D + sum_j j T_j/(a+s)]
      = (-1)^(p-1) C a V/[2(a+s)].                      (3)

Since binom(q+r-1,s)/(h)_s=1/s!, the beta and rising-factorial factors cancel exactly, yielding

    R = (-1)^(p-1) (3/2-p)_s / [2s (r+1/2)_s].          (4)

Both (1) and (4) are rational functions of r for fixed integer p,q. Their equality on the open interval r>max(0,p-2) is a rational identity. The finite expression (1) and denominator in (4) are regular for every r>0. This proves equality at all positive integer r, including h=0,-1,..., without evaluating an undefined hypergeometric series there. Taking the p-1 negative half-integer factors in (4) gives exactly the positive double-factorial formula for kappa.

## Left chamber and the complete shifted-wall bridge

In F_L the A-binomial has upper value 2p-3>=1 and degree 2p+q+r+j-3>2p-3. Hence every constant and every partial derivative with respect to B vanish.

For arbitrary positive integers a,b,c, the two chamber polynomials agree identically on each affine line

    B-A=h,  -(c-1) <= h <= a-1, h integer.                (5)

For h>=0, take arbitrarily large integers A and B=A+h. The reflected polynomial F_R equals the finite sum over z=0,...,B using the polynomial binomial B_a(A-z). This identity holds for every A as a polynomial: for each fixed B it follows first from the actual supported count for all integers A>=B. The additional terms beyond z=A have A-z in {-1,...,-h}; if h<=a-1 all those binomials vanish. Thus F_R=F_L on the entire integer tail of the line, and hence as polynomials on the line. For negative h interchange a,c and A,B. This proves (5) without treating an out-of-support polynomial as a literal count.

Here h=B0-A0=q-r lies in the full interval (5): q-r>=1-c because q>=1, and q-r<=a-1 because p+r>=2. Differentiate that line identity in direction (1,1) at (A0,B0). The known zero transverse derivatives imply

    partial_A F_L(A0,B0)=partial_B F_R(A0,B0).

This supplies the left kernel and both chamber constants. It retains offset ties, all integer p,q,r in the stated domain, and the original lattice and stretching grade.
