# A70 independent adoption target: the complete Pro049 U12 operation

Curated mathematical proof from **A70**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Origin: completed Pro049 U12, full proof SHA-256 8bf014ee64307fad5c527f71e42458c9cb1afe2e1975aa96adf093540735bc96, authenticated by the A70 source index. Returned programs remain inert. A new campaign verifier reconstructs the physical system, exact cone and coefficient identities independently; complete passing mathematical checks are required as numerical evidence. This note never promotes the broader U09–U11 stabilized-quotient chain by association.

## Entire original and independently reconstructed coordinates

For integers s,u>=0 take


```text
lambda=(2s+4u,2s+3u,2s+2u,2s,s),
mu=(2s+2u,2s+u,2s,s,0),
nu=(s+3u,s+2u,u).
```

These are legal balanced partitions with lambda outer. At grade t put S=st,U=ut. The LR rule forces row one to be all ones and row two to have no threes. Write its number of ones as z+U, and the first two entries of rows four and five as (a,b),(d,e). Every row/content equation then forces the complete array

    (2U,0,0),
    (z+U,U-z,0),
    (S-a-d-z,S-b-e+z+U,U-2S+a+b+d+e),
    (a,b,S-a-b),
    (d,e,S-d-e).

The inverse takes four literal tail entries and z=x_(2,1)-U, so the integer lattice is exactly Z^5 in every fixed fiber. Sorted-row nonnegativity, every adjacent column inequality


```text
mu_(i-1)-mu_i+sum_(k<j)x_(i-1,k)-sum_(k<=j)x_(i,k)>=0,
```

and every ballot-prefix inequality


```text
sum_(k<i)x_(k,j)-sum_(k<=i)x_(k,j+1)>=0
```

are necessary and sufficient. The most restrictive prefix for a letter pair occurs after the larger-letter block; the adjacent row column tests enforce each complete skew column. Together with S,U>=0 there are 39 labeled occurrences, including zero and repeated forms. The verifier derives them from the literal partitions and array, before comparing source rays or formulas.

For s,u>0 let e=min(s,u)/4, use tail rows (s-2e,e,e) and (e,s-2e,e), and z=e-u/2. Direct substitution makes every nonconstant physical inequality strict. Thus the actual degree is five, established before any vector extraction. At u=0 the entire original has one tableau; at s=0 it has the interval -U<=z<=0 and polynomial 1+ut. All-zero parameters give a point. No generic degree is assigned at these boundaries.

## Why a finite cone certificate proves the all-parameter count

The parameter cone has lattice Z^7 in (S,U,z,a,b,d,e), lies in the orthant (S,U,-z,a,b,d,e)>=0, and has a bounded section S+U=1: 0<=a,b,d,e<=S and -U<=z<=0. Every nonzero ray has S+U>0. The independently generated physical inequalities therefore define a pointed full-dimensional rational cone.

The verifier uses exact double description from that orthant. At each new inequality, keep nonnegative rays and form every positive/negative pair on its zero hyperplane. This generates the entire intersection; discard only rays whose full active-normal rank is not six, with duplicate primitive rays merged. The accepted certificate must reproduce the complete 15-ray cone, then derive every facet from the original inequalities rather than trusting a listed count.

All 13 facets yield a recursive pulling triangulation of the section, taking the least-indexed vertex and every facet not containing it at each face. This constructs full coverage and face-to-face intersections. The 16 maximal ray matrices have determinant plus or minus one. The exact generic interior vector from the source fixes half-open ownership; every transformed coordinate is checked nonzero and every resulting numerator shift is recomputed. Perturbing a point into the interior along that vector selects exactly one cone, including on external boundaries. Unimodularity makes each half-open numerator a single integer shift. Thus the sum of all 16 rational cone series is the WHOLE bivariate count, including zeros and all residues.

The root-authored verifier clears complete denominators and checks the full rational identity with the source's nine-term generating function G. No finite grid or favorable ray count substitutes for that identity. Independent algebra then extracts the complete N below, including both parity branches of the (1-xy^2) term. The apparent residue dependence cancels before any ordinary coefficient is assigned.

## Complete count and sign certificate

Define


```text
E(S)=(S+1)^2(S+2)^2/4,
A(S)=S(S+1)(S+2)(23S^2+81S+76)/120,
C(k,U)=k(k-1)(k+1)(30U^2+5Uk+140U-8k^2+45k+142)/120,
D(k,U)=k(k-1)(k-2)(10U^2+5Uk+35U+k^2+8k+27)/120.
```

For ALL integers S,U>=0 the complete original count is


```text
N(S,U)=(U+1)E(S)-A(S)
   +1_(U<=2S) binom(2S-U+3,5)
   +1_(U<=S) C(S-U,U)
   -1_(2U<=S) D(S-2U,U).                         (1)
```

The C and D factors retain their zero initial bands. Every active binomial has a nonnegative integer upper argument, and is zero below its lower index. Full even/odd polynomial binomial identities give the same binom(2S-U+3,5), with its actual support. The verifier checks these identities, the rational generating functions of C/D and the untruncated E/A parts, then the four full chamber polynomials and every shared wall.

Substitute S=st,U=ut. The four closed parameter cones have coordinates


```text
(s,u)=(2a+b,a), (2a+b,a+b), (a+b,2a+b), (a,2a+b),
```

with a,b>=0. For all coefficients k=0..5, first take the fixed-s derivative with respect to u, then substitute the cone coordinates. Every one of the 48 COMPLETE coefficient/derivative slots is checked as a polynomial; zero monomials and zero constant derivatives remain explicit. All nonzero coefficients are positive. The endpoint pure powers prove strictness for s,u>0; integration across the verified continuous walls gives


```text
[t^k](P_(s,v)-P_(s,u))>0,
   s>0, 0<=u<v, k=1,...,5.                     (2)
```

The constant difference is zero. At s=0 only the linear coefficient changes. Positive endpoints alone would not prove (2); the complete derivative certificate does.

## Scope and retained obstructions

This independently adopted result, at its accepted scope, is an ALL-PARAMETER OPERATION theorem for this fixed rank-five family. Its endpoints were already within rank-at-most-six positivity. It creates no new positive rank coverage and no LR-negative candidate. The whole cone, exact generating function and polynomial certificate supply the unbounded quantifier; only two selected numerical originals, (s,u)=(1,1),(1,2), are independently counted here, with their prior degree, all determining grades and two unused grades each. The provider's larger finite populations remain unadopted source.

For those two originals the complete gain is


```text
21t/20+73t^2/24+77t^3/24+35t^4/24+29t^5/120.
```

The source's complete projected shadow has a period-two term, and its entire arrival sum has the opposite term. Neither clipped piece is declared an ordinary polynomial. Its stable auxiliary intercept has negative higher coefficients while the complete original and operation are positive. These remain constraints on any attempted generalization.

STABILIZED-QUOTIENT.md separately reconstructs the arbitrary-three-letter quotient and coarse stabilization theorem at its exact A70 gate. U10's sharper support threshold, positive quotient realization and primitive-wall cover remain serious completed unadopted source leads. Neither the selected coarse theorem nor those stronger source claims sign noncollapsed primitive bases or pre-stable bands. The source's arbitrary-transportation wall embedding remains at its own adoption boundary.

## Complete cone, generating function and portable verification

The complete [originating proof](A70-PRO049-U12-FULL-PROOF.md) supplies every
primitive ray, all 13 facets, all 16 unimodular half-open cells and full lattice
shifts, the nine-term bivariate generating function, every extraction and parity
identity, all chamber coefficients and all fixed-s derivative certificates.
The [portable checker](../code/a70-u12/verify_a70_u12.py) independently regenerates
the complete 39-occurrence physical system, cone coverage and these identities.
Its [reproduction guide](../code/a70-u12/README.md), [frozen inputs](../data/a70-u12/MANIFEST.json),
[complete certificate data](../data/a70-u12/CERTIFICATE-DATA.json),
[generating-function terms](../data/a70-u12/GENERATING-FUNCTION.json) and
[source-to-public map](../data/a70-u12/SOURCE-TO-PUBLIC.json) close every dependency.

The checker uses exact integer/rational arithmetic and Python's standard library.
It verifies two archived A70 complete vectors by exact reconstruction and formula
comparison; it performs no fresh LR or physical-array counts and adds no new
unused-grade, positive-rank or additive-coverage claim. The all-parameter theorem
rests on the complete cone and exact identities, rather than those finite records.
