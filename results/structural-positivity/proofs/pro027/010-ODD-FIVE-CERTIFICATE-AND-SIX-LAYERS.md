# The odd fifth layer and the complete six-layer consequence

This computer-assisted proof concerns the auxiliary insertion functional. This is not an ordinary-negative LR observation, a complete seven-chamber theorem, or universal transportation cancellation.

Let S_(a,e)(b,c) be the EXACT finite polynomial in the insertion-moment derivation, equations(4)-(5), with every source factorial and endpoint convention retained. The prefactor in equation(6) of that derivation is nonzero at all positive integers a,b,c, so D_0(a,b,c)=0 is equivalent to S_(a,0)(b,c)=0. The prior total-degree bound is8a-6, independently of numerical values. At a=5 this is 34.

## Complete monomial certificate

The monomial calculation constructs the entire polynomial 576*S_(5,0), clearing the j!k! denominators by576=(4!)². There are 190 complete (j,k,l) summands. Each is a product of the explicitly specified linear factors in b,c, with its exact integer binomial coefficient and sign. The five complete k-blocks each have 260 nonzero monomials; DATA/odd5-polynomial-certificate.json supplies all 1300 signed coefficients as triples(exponent_b,exponent_c,integer_coefficient). Their coefficientwise sum is identically zero, with no omitted nonzero entries. Therefore S_(5,0)=0 as a polynomial.

The source formula is reconstructed directly with repeated exact multiplication by A*b+B*c+C. No b,c grid is used to generate this certificate. No factorial of a negative integer or floating coefficient is evaluated. The complete source formula and each intermediate polynomial block are retained.

## Independent beta-integral determination

The beta-integral calculation does not use the monomial certificate, the S polynomial, Rodrigues differentiation, or integration by parts. It expands the finite u,v coefficients of the source's convergent integral directly. With B=b+c,q=B-1,p=2a+j+k-1,m=a+c+k-1,K=a+2b+k, its inner expression is

sum_(v=0)^q (-1)^v binom(m,q-v)binom(K+v-1,v) Beta(p+v+1,2B),

multiplied by the full outer factor from equation(3) of that derivation, including its minus sign. This independently gives D_0(5,b,c)=0 at all 630 specified points(b,c)=(1+i,1+j), i,j>=0,i+j<=34. Exact individual rational outputs are in DATA/odd5-beta-grid-raw.jsonl.

These nodes are unisolvent for total degree at most 34: the basis binom(b-1,i)binom(c-1,j), i+j<=34, has a triangular evaluation matrix on the same lower set, with diagonal1. Thus the source degree bound and nonzero prefactor prove S_(5,0)=0 from this second route as well. The four specified unused points(37,1),(1,37),(20,20),(43,17) also give zero. This is an exact polynomial determination of an unbounded b,c theorem, not finite-range extrapolation. Both arithmetic implementations use CPython integers/Fractions; they are not falsely called separate arithmetic engines.

## Consequence

The source layers a=1,2,3 are already established. [Two exact residue involutions and the irreducible odd-multiplicity problem](009-RESIDUE-INVOLUTIONS-AND-ODD-REDUCTION.md)'s uniform even-layer recurrence supplies a=4. The new complete a=5 identity then supplies a=6 by that same recurrence. Therefore

D_0(a,b,c)=0 for every1<=a<=6 and every b,c>=1.

Every even layer is reducible to lower odd layers. The remaining universal assertion is equivalent to proving the odd layers a>=7 at unequal b,c; the diagonal b=c is already zero for arbitrary a by [Two exact residue involutions and the irreducible odd-multiplicity problem](009-RESIDUE-INVOLUTIONS-AND-ODD-REDUCTION.md). Neither the 452-case pilot nor this a=5 certificate proves any remaining odd layer.

For the actual full A3 graph with occupations(a,b,c,0), multiplicities(a+b,b+c,c,a+c,b,a), offset(-b-c,-2c,0), the prior integral incidence lattice is saturated of rank 3 and strict-chamber dimension3(a+b+c)-3. The existing complete insertion and wall identities now imply zero value and full first gradient on strict C3 when a<=6, on source-reversed C2 when c<=6, and on C5 when a,b<=6. Each positive remaining parameter is unbounded. The source's nonzero higher-order wall remains in every count; it was not dropped because its first jet vanishes.

These are chamber-sector statements. A final ordinary LR rank belongs only to a completed transportation constructor, not to the graph's rank 3. Other support chambers, other empty-class positions, four occupied classes and the complete generic higher-class remainder still need their own proof.
