# Whole-bank ordinary positivity at unbounded rank

For every integer m>=2, every ordinary coefficient through actual degree 2m-1 of the entire LR family in [Complete positive-gap two-bank contraction](013-COMPLETE-BANK-CONTRACTION.md) is strictly positive. The rank 5 case at m2 is already known; m>=3 gives an unbounded-rank, unbounded-degree family. This does not establish positivity of every triple at any one rank.

## Exact complete pieces

Write k=m-1,u=2t+1 and define
T_k(t)=sum_(z>=0,sum z<=t) product_i(2t+1-z_i),
M_k(t)=sum_(z>=0,sum z<=t) (sum z_i) product_i(2t+1-z_i).
[Complete positive-gap two-bank contraction](013-COMPLETE-BANK-CONTRACTION.md) gives the complete parent identity
P_m(t)=((k+1)t+1)T_k(t)+(3/2)M_k(t).                       (1)
The weights are positive at integer sites, but that is not the sign proof. We establish the ordinary coefficient signs of BOTH complete pieces.

For independent formal s,L and positive c put
R_(c,l)(s,L)=sum_(j=0)^l (-1)^j binom(l,j)L^(l-j) (s falling j)/(c rising j),
S_l=(c rising l)R_(c,l).
Their exponential generating series is exp(Lz)Y(z), where the coefficient ratio of Y=sum (-s rising j)z^j/((c rising j)j!) proves
zY''+(c-z)Y'+sY=0.
Consequently
S_(l+1)=((c+2l)L+l-s)S_l-l(c+l-1)L(L+1)S_(l-1).          (2)
S0=1,S1=cL-s. This derivation is formal, requires no convergence or outside special-function hypothesis. The equation agrees with DLMF13.2.1 at a=-s,b=c. The earlier continuant proof for redundant leaves motivated this extension; credit for that theorem remains with its original derivation.

## Positive T certificate

Elementary symmetric moments give
T_k(t)=binom(t+k,k) R_(k+1,k)(t,2t+1).
For c=k+1,s=(u-1)/2, recurrence(2) is the continuant of the k-by-k tridiagonal J=B+uA with zero-based row i:
diag J=(c+2i-1/2)u+i+1/2,
J_(i,i+1)=-(i+1)(u+1), J_(i,i-1)=-(c+i-1)u.
B is upper bidiagonal with positive diagonal i+1/2 and upper -(i+1); B^-1 is upper triangular and strictly positive on its upper triangle. Write H_ij=(B^-1)_ij. Then C=B^-1 A is upper Hessenberg. Its subdiagonal is negative. For i<j<k-1,
C_ij=H_ij*(c-j-3)/(2j+3)>=0,
since j<=k-2 and c=k+1. In the last column above the diagonal,
C_(i,k-1)=H_(i,k-1)*(c+k-2)>0.
For i<k-1 its diagonal equals
H_ii*(i^2+3i/2+c/2-3/4)/(i+3/2)>0;
the last diagonal is H_last,last*(c+2k-5/2)>0.
The k1 case is the positive single entry(3u+1)/2 directly.

Every principal minor of an upper Hessenberg matrix with positive diagonal, nonnegative strictly upper entries, and negative subdiagonal is positive: split a selected index set into consecutive runs; the principal matrix is block upper triangular. Expanding a run along its first row, the determinant sign cancels the product of negative subdiagonal entries. Every term is nonnegative and the diagonal term is strictly positive inductively. Thus all coefficients of det(I+uC), being sums of principal minors, are strictly positive. det B>0, so S_k and R_(k+1,k) are coefficient-positive in u. Substitution u=2t+1 and multiplication by binom(t+k,k) prove T_k strictly positive through degree 2k.

## Positive M certificate with the full subtraction

Let c=k+2 and s=t-1=(u-3)/2. Differentiating the finite descending-width generating function, or elementary-symmetric moments, gives the EXACT polynomial identity
M_k(t)=k*t/(k+1)*binom(t+k,k)
        *[2R_(c,k)(s,u)-(u+1)R_(c,k-1)(s,u)].             (3)
This subtraction is retained. For k1, M1=t(t+1)(2t+1)/3 directly.

For k>=2 use recurrence(2) with diag J=(c+2i-1/2)u+i+3/2 and the same off-diagonals. The bracket in(3), after multiplication by(c rising k)/2, is its size-k determinant with the last diagonal decreased by (2k+1)(u+1)/2. That last diagonal becomes(2k-1)u. Extract u from the last row and take the Schur complement of its constant diagonal2k-1. The result is
bracket=2u(2k-1)/(c rising k) * L_k(u),
`L_k=S_(k-1)-[2k(k-1)/(2k-1)](u+1)S_(k-2),               (4)`
where S_i are the UNMODIFIED leading continuants at this fixed c,s,L.

It would be wrong to reuse the T principal-minor sign pattern on the modified Schur complement: at k3 one diagonal of B^-1 A is -91/3. The following positive recurrence repairs that failed certificate.
Set E_i=S_i-(i+1/2)(u+1)S_(i-1). Then
E1=(c-2)u,
E_i=u[(c-j-2)/(2j+1)*S_(i-1)
       +2j(c+j-1)/(2j+1)*E_(i-1)], j=i-1>=1.            (5)
This follows exactly by substituting recurrence(2), and all its scalar coefficients are positive for i<=k-1 because c=k+2. Starting with S0=1, (5) and
S_i=(i+1/2)(u+1)S_(i-1)+E_i
prove S_i coefficient-positive and E_i positive in all degrees 1..i. Finally
L_k=E_(k-1)+(u+1)S_(k-2)/(2(2k-1)),                     (6)
so L_k has strictly positive coefficients in every degree 0..k-1. Equations(3)-(6) show that M_k is t times a polynomial with strictly positive coefficients, of actual degree 2k+1. There is no ordinary constant term.

## Entire consequence and exact scope

Equation(1) now proves every ordinary coefficient of P_m strictly positive through 2k+1. In fact
P_m >=_coeff ((k+1)t+1)T_k >_coeff 0
in each supported degree, and P_m/binom(t+k,k) has all k+2 coefficients strictly positive. The factor roots -1,...,-k match the true codegree m=k+1 proved geometrically in [Complete positive-gap two-bank contraction](013-COMPLETE-BANK-CONTRACTION.md). No reflection is assumed.

The previously established g0 family had only dimensionm and unique support. This theorem retains g1,h0, all m-2 internal label3 coordinates and the bank coordinate, with actual dimension 2m-1. It does not prove the same claim for g>=2 or h>0. Nor does it equate one such bank with the synchronized product construction: the equations coupling its factors still require a whole-LR realization. The attempted leakage completion has yielded a positive full family, not an ordinary-negative LR counterexample.
