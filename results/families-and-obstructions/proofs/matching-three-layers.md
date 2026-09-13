# All ordinary coefficients for three unbounded matching layers

FRONTIER-025 P06. Originating proof with exact symbolic polynomial certificates, awaiting campaign verification. This is not all matching parameters, all six-run flows, a whole ordinary rank, or a worldwide novelty assertion.

## 1. Whole object and the prior count, lattice, and degree

Let a,f>=1 and q,r>=0 be integers, and form the word

    w=A^a B^2 A^(q+1) B^(r+1) A^2 B^f,
    n=a+f+q+r+6.

Define the bare balanced partitions, with lambda outer,

    mu_i = number of A letters in w_i,...,w_n,
    nu_i = number of B letters in w_i,...,w_n,
                    1<=i<=n+1,
    lambda=(n-1,n-1,n-2,...,2,1,1).                         (12)

Trailing zeros are trimmed only after this construction. The final ordinary rank is n+1=a+f+q+r+7 and the outer size is n(n+1)/2. The factor partitions satisfy mu_i+nu_i=n-i+1 for i<=n and vanish at n+1. The adjustment to lambda is (-1,0,...,0,+1), preserving total size and giving a partition. Thus |lambda|=|mu|+|nu|.

The ENTIRE LR count is the integral source-sink flow count on vertices 0,...,n with an edge i->j exactly when w_(i+1),...,w_j contains both labels. The source is t and the sink is -t; all internal netflows are zero. The direct source-sink edge proves feasibility, including all parameter boundaries. At t=0 there is one zero flow.

For clarity, the source character bridge is an adopted premise, with its complete proof included at SOURCES/SELECTED/methods/frontier-024-2026-09-09/sources/SOURCES/PHASE6/NONNEGATIVE-M-LEMMA.md and re-specialized in source proof 013. Each cut belongs to exactly one of the A/B supports. A nonparabolic Weyl numerator loses at least t+1 on a selected cut, whereas the target exponent there is only t, so it cannot contribute. The remaining two character numerators and the extraction denominator leave precisely one reciprocal root on every mixed interval, and none on monochromatic intervals. The target is lambda in (12). This is an entire all-stretch character identity, not a proper face, selected term, or assertion of a conventional-hive affine isomorphism.

After inactive vertices are removed, the graph has q+r+7 vertices and qr+5q+5r+17 active edges. Source/sink edges occur at every active internal vertex, and ALL internal edges of the read source proof 013 are retained, including each Y_i->Z_j. Every edge lies on a source-sink path; averaging these paths gives a point positive on all active edges. An incidence forest basis is unimodular, so its full affine flow lattice is saturated, and the integral vertices follow by leaf elimination. Cut sums bound every edge by t. Its actual degree is therefore

    d=E-v+1=qr+4q+4r+11.                                  (13)

Inactive end-run vertices change n but not the polynomial. These degree/lattice facts precede all new evaluations.

The exact complete matching numerator from the read source proof 014 is

    h_(q,r)(z)=(1+z) sum_(k=0)^min(q,r)
         binom(q,k)binom(r,k)k! z^k
         [1+(r+2)z]^(q-k)[1+(q+2)z]^(r-k),                (14)
    sum_(t>=0)P_(q,r)(t)z^t=h_(q,r)(z)/(1-z)^(d+1).

It follows from complete row/column composition elimination: centering independent geometric matrix entries leaves exactly partial matchings, not a deletion of the central matrix. Both full source proofs 013 and 014 are included unchanged. Formula (14) is symmetric in q,r. Its numerator degree is q+r+1 and its actual codegree is d-q-r=qr+3q+3r+11. This last assertion uses the integral flow model and reciprocity; it is not needed to fit a vector here.

## 2. New theorem and its parameter normalization

If 1<=min(q,r)<=3, EVERY ordinary coefficient of the complete polynomial (14) is strictly positive. Zero q/r cases are separately inherited source-positive. Hence the whole p=u=1 matching family is now positive whenever min(q,r)<=3, at all end-run lengths.

By symmetry put 1<=q<=3 and r>=q. Set

    B=q+2,
    D=d-q=(q+4)r+3q+11,
    m=D-r=(q+3)r+3q+11,
    N=D+1=(q+4)r+3q+12.

Use the auxiliary G,Omega,W of proof 020 with these B,r,m. Its hypothesis holds because

    m-(B-1)r-1=2r+3q+10>0.

In particular G and both compensated bases are coefficient-positive at their exact scopes. The final whole-LR bound is

    P_(q,r)(t) >=_coeff G_(q,r)(t)
                  >=_coeff binom(t+m,m).                  (15)

All nonconstant coefficient differences P-G are strictly positive through degree d. In particular [t]P>H_m, where m is defined AFTER putting q=min(original q,original r). The source all-parameter c1 bound remains valid beyond this new all-coefficient domain.

## 3. A completely reproducible finite symbolic identity

The construction of the multipliers involves only polynomials in z with rational-function coefficients in r. It does not interpolate r or t.

Let V_0(z)=1 and, for 0<=k<q, set

 V_(k+1)=z*{[(r-k)B(1-z)+(N+k)(1+Bz)]V_k
                          +(1-z)(1+Bz)V'_k}.
 U_k=V_k (1-z)^(q-k)(1+Bz)^(q-k).

Euler differentiation theta=z d/dz of F(z)=(1+Bz)^r/(1-z)^N gives

 theta^k F=(1+Bz)^(r-q) U_k/(1-z)^(N+q).

Since G(-1)=0, the sequence G(t-1) has generating function zF, and theta^k(zF)=z(theta+1)^kF. Define

 T_(q,r)(z)=(1+z) sum_(k=0)^q binom(q,k) r_under(k) z^k
                        [1+(r+2)z]^(q-k)(1+Bz)^(q-k).

For the multipliers A(t)=sum_(k=0)^q a_k t^k and Bop(t)=sum b_k t^k below, the certificate is the FULL polynomial identity

 T_(q,r)(z) = sum_(k=0)^q a_k U_k(z)
           + z sum_(k=0)^q b_k sum_(l=0)^k binom(k,l)U_l(z). (16)

The common prefactor is (1+Bz)^(r-q)/(1-z)^(d+1), so (16) proves P=A G+Bop Omega at every t>=0, including zero. Every term of (14) survives this identity. No extra count, asymptotic limit, or omitted residue is involved.

The complete coefficients a_k,b_k and the compensated coefficients c_k are in DATA/P06/OPERATOR-CERTIFICATE.json as exact numerator/denominator arrays in ascending powers of r. Its convention is

    a_0=1;
    c_0=b_0+m a_1;
    c_k=b_k+a_k+m a_(k+1)  (1<=k<q);
    c_q=b_q+a_q.

The printed tables below give a_1,...,a_q (the coefficients of L) and c_0,...,c_q (the coefficients of C). All their numerator and denominator coefficients in r are positive at r>=q; the separate certificate also expands in y=r-q and records the exact positive arrays. Thus L,C satisfy proof 020.

Identity (16) for q=1,2,3 was derived by exact rational-function linear algebra and then verified independently by clearing all denominators with standard-library Fraction polynomial arrays. The latter implementation generates V,U,T independently and finds zero in EVERY coefficient of z and r. It separately verifies the c_k relations and sign arrays. It also verifies the exact q=4 challenge identity without declaring that case positive. These are symbolic all-r checks, not evaluations on a finite r grid. The six entire vectors used as diagnostics are derived directly from (14), not fitted.


### Exact table q=1

```text
a_1 = (10*r + 27)/(40*r + 120)
c_0 = (5*r**2 + 34*r + 54)/(5*(r + 3))
c_1 = (5*r + 12)/(10*(r + 3))
```

### Exact table q=2

```text
a_1 = (1630*r + 4993)/(4500*r + 14250)
a_2 = (90*r**2 + 512*r + 738)/((6*r + 19)*(375*r + 1125))
c_0 = (1610*r**2 + 10573*r + 16925)/(150*(6*r + 19))
c_1 = (60*r**3 + 706*r**2 + 2531*r + 2875)/(50*(r + 3)*(6*r + 19))
c_2 = (36*r**2 + 179*r + 225)/(75*(r + 3)*(6*r + 19))
```

### Exact table q=3

```text
a_1 = (95856*r**3 + 899148*r**2 + 2809559*r + 2924471)/((7*r + 22)*(7*r + 23)*(4536*r + 13608))
a_2 = (15624*r**3 + 144613*r**2 + 446461*r + 459786)/((7*r + 22)*(7*r + 23)*(4536*r + 13608))
a_3 = (343*r**3 + 3031*r**2 + 9022*r + 9028)/((7*r + 22)*(7*r + 23)*(1512*r + 4536))
c_0 = (70110*r**4 + 890781*r**3 + 4234148*r**2 + 8924462*r + 7038252)/(567*(r + 3)*(7*r + 22)*(7*r + 23))
c_1 = (22869*r**4 + 313548*r**3 + 1583882*r**2 + 3506948*r + 2879550)/(1134*(r + 3)*(7*r + 22)*(7*r + 23))
c_2 = (1029*r**4 + 16135*r**3 + 87293*r**2 + 199867*r + 166212)/(756*(r + 3)*(7*r + 22)*(7*r + 23))
c_3 = (343*r**3 + 2625*r**2 + 6752*r + 5832)/(756*(r + 3)*(7*r + 22)*(7*r + 23))
```

## 4. Exact exceptions, rank, and scope

The theorem keeps p=u=1 and constant unit direction. A common positive integral direction g replaces P(t) by P(gt), preserving every ordinary sign and multiplying coefficient k by g^k. Direction g=0 is separately the point polynomial one. End-run lengths a,f>=1 affect only inactive vertices. Cases q=0 or r=0 use the already-proved complete zero-run formula, not the r>=q>=1 multiplier tables. Neither this proof nor an individual G/Omega/W is a generic LR positive operation without membership (16).

For unit ends the final ordinary rank is q+r+9, not q+r+6, the active incidence rank. G has degree D=d-q and is only an auxiliary count/basis polynomial here; it is not substituted for the parent degree d. Arbitrary larger flanks p/u, nonconstant directions, general q,r>=4, and seven-plus runs remain open. The q=r=1 anchor was already closed in the source; it is not claimed newly discovered.

The smallest displayed unit-end matching constructor has n=8, outer size 36. Every genuinely coupled member q,r>=1 has n>=10 and size >=55. Larger ends and positive common dilation cannot enter the original outer-size<=30 box. This is a bound on this displayed construction, not a minimum over all other LR realizations of the same polynomial. No whole-rank theorem, box census, or additive increment follows.

A concrete positive member q=1,r=2 has rank 12, size 66, degree 25 and bare partitions

    lambda=(10,10,9,8,7,6,5,4,3,2,1,1),
    mu=(5,4,4,4,3,2,2,2,2,1),
    nu=(6,6,5,4,4,4,3,2,1,1,1).

Its exact entire polynomial is

    product_(j=1)^21(t+j)
        *(303600+186944t+43036t^2+4444t^3+176t^4)/25!.

Its linear coefficient is 150296389/35271600 and its counts at 0,1,2,3 are 1,39,740,9240. The entire degree 25 vector is retained. The full graph and full numerator agree at these sites; literal bare-LR row words additionally agree at 1,2. Those scalars are not asserted as an independent high-degree reconstruction.
