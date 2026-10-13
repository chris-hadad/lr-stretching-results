# A65: positive quadratic payment on every three-occupied slope wall

Curated mathematical proof from **A65**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root-led derivation with an independent Astra analytic collaborator. This note proposes an all-occupation theorem, not an extrapolation from the finite probe. Let p=n1,q=n2,r=n3 be strictly positive, N=p+q+r, a=p+q,b=p+r,c=q+r. Use the COMPLETE chamber polynomials and original offsets of THREE-ROW-KERNEL.md. The assignment sign is (-1)^q.

The theorem is: on the slope wall x=y=s, the signed ordinary quadratic coefficient is A(p,q,r)s^2, where A(p,q,r)>0 for EVERY p,q,r>0. Thus a supported three-occupied assignment on that slope wall has strictly positive c2. This does not sign every off-wall assignment, the complete one/two-class remainder, or all three-row transportation polynomials.

## 1. Full arbitrary-occupation quadratic formulas

Let H_0=0 and H_m=sum_(i=1)^m 1/i. For L>0,d>=0 define


```text
v_d(L)=(-1)^d binom(L-1,d),                       d<L,
       0,                                        d>=L;
g_d(L)=-v_d(L)(H_(L-1)-H_(L-d-1)),                d<L,
       (-1)^(L-1)(d-L)!(L-1)!/d!,                d>=L.
```

These are exactly the constant and linear coefficients of binom(z+d-L,d). Set


```text
lambda_k=binom(b+k-1,k)(2p-1)!(c+k-1)!/(2p+c+k-1)!,
mu_k=binom(b+k-1,k)(a-1)!(2r+k-1)!/(b+c+k-1)!.
```

Then the SIGNED quadratic forms of the two complete chambers are


```text
Q_U(x,y)=L_U x^2+B_U xy,
B_U=(-1)^(r-1) sum_(k=0)^(c-1) lambda_k g_(c-1-k)(2r),
L_U=(-1)^(r-1) sum_(k=0)^(c-1) lambda_k v_(c-1-k)(2r)
                                  (H_(2p-1)-H_(c+k-1));

Q_V(x,y)=L_V y^2+B_V xy,
B_V=(-1)^(q-1) sum_(k=0)^(a-1) mu_k g_(a-1-k)(c),
L_V=(-1)^(q-1) sum_(k=0)^(a-1) mu_k v_(a-1-k)(c)
                                  (H_(a-1)-H_(2r+k-1)).
```

To obtain them expand every binomial of the kernel modulo t^3. If 0<=h<m,


```text
binom(zt+h,m)=(-1)^(m-h-1) h!(m-h-1)!/m!
     *[zt+z^2 t^2(H_h-H_(m-h-1))]+O(t^3).
```

This is obtained by factoring out its unique zero factor and taking the sum of reciprocals of the remaining integer factors. The other binomial gives v and g. In particular there is no y^2 term in Q_U, and no x^2 term in Q_V. No term or original shift has been dropped.

## 2. Exact diagonal polynomial and initial bands

Put F(M)=K(M-c,M-2r), without the assignment sign. BOTH chamber polynomials agree on this affine line. For large integers M, their upper limits differ by |q-r|. In the erroneously extended interval each added summand has a vanishing ordinary binomial: if q>=r its first multiplicity is a=p+q and the negative residual magnitude is at most q-r<a; the other case uses c=q+r and magnitude at most r-q<c. Thus both formulas equal the actual full sum for every sufficiently large M, which establishes their polynomial equality.

Let J=min(c-1,2q-1), and use rising factorial notation (a)_k. Then


```text
C_j=(2q-1)! (a)_(c-1-j)/[j!(c-1-j)!(2q-1-j)!],
F(M)=sum_(j=0)^J C_j binom(M+2p-1,2N-2-j).      (1)
```

For a direct derivation, put i=U-z in the full convolution. It gives the all-grade generating series


```text
sum_(M>=0) F(M) z^M
   =z^c/(1-z)^b
      sum_(i>=0) binom(i+a-1,a-1)binom(i+2q-1,c-1) z^i.
```

A negative initial residual contributes zero here because its ordinary binomial vanishes; no eventual-only series is substituted. The inner series equals

    z^(c-2q)/(c-1)! * d^(c-1)/dz^(c-1)
                         [z^(2q-1)(1-z)^(-a)].

Leibniz expansion gives C_j z^(2c-1-j)/(1-z)^(2N-1-j); its coefficients give (1). Every power 2c-1-j is positive. The polynomial binomial also vanishes in the corresponding initial band, so this series/polynomial join is valid including M=0.

Taking its signed quadratic coefficient gives


```text
A=(-1)^q sum_(j=0)^J (-1)^j C_j
      (2p-1)!(2c-2-j)!/(2N-2-j)!
      *(H_(2p-1)-H_(2c-2-j)).                   (2)
```

Consequently A=L_U+B_U=L_V+B_V. Thus


```text
Q_U=A x^2+B_U x(y-x),
Q_V=A y^2+B_V y(x-y).                           (3)
```

Equality of the two A expressions does not assert equality of the full off-wall Hessians.

## 3. Positive integral proof of A>0

Let n=2q-1 and


```text
f(u)=u^(p+q-1)(1-u)^(q+r-1),
D=(p+r-1)!/[(p+q-1)!(q+r-1)!]>0.
```

The elementary Leibniz/Rodrigues polynomial identity is


```text
u^(2p-1) sum_(j=0)^J (-1)^j C_j(1-u)^(2c-2-j)
   =D f(u) f^(2q-1)(u).                        (4)
```

It follows by expanding the derivative of u^(a-1)(1-u)^(c-1), collecting powers of (1-u), and the binomial convolution. Terms whose differentiation order exceeds a factor's degree are zero. This identity is polynomial and does not require p>=q or r>=q. The independent verifier expands both sides directly, separately from the C_j construction, on the full bounded verification domain.

The beta integral and its logarithmic derivative give, for positive integers A0,B0,


```text
integral_0^1 u^(A0-1)(1-u)^(B0-1) log(u/(1-u)) du
  =(A0-1)!(B0-1)!/(A0+B0-1)! * (H_(A0-1)-H_(B0-1)).
```

This identity follows by differentiating the beta integral in its two positive parameters, or by integration of finite harmonic recurrences; its integrals converge at both endpoints. Applying it termwise to (2) and using (4) yields


```text
A=(-1)^q D integral_0^1 f(u) f^(2q-1)(u)
                                  log(u/(1-u)) du.     (5)
```

For v>0 write f=(u+v)g. Every derivative of g through order q-1 vanishes at both endpoints, because f has zero order at least q there. Odd-order integration by parts, with all boundary terms retained and then zero by these orders, gives


```text
integral (u+v)g g^(n)=-n/2 integral g g^(n-1),
integral f f^(n)/(u+v)
  =(-1)^(q-1) n/2 integral [g^(q-1)]^2.          (6)
```

For the first equality, integration by parts n times gives the negative of the original integral minus n integral g g^(n-1). Add the two expressions. The second equality uses f^(n)=(u+v)g^(n)+n g^(n-1), followed by q-1 integrations by parts. With denominator 1-u+v, the derivative of its linear factor is -1, and the sign in (6) is reversed.

Finally use the convergent difference representation


```text
log(u/(1-u))=integral_0^infinity
              [1/(1-u+v)-1/(u+v)] dv.
```

Equations (5) and (6) give the strictly positive representation


```text
A=D(2q-1)/2 * integral_(v=0)^infinity integral_(u=0)^1
   { [d^(q-1)/du^(q-1)(f(u)/(u+v))]^2
    +[d^(q-1)/du^(q-1)(f(u)/(1-u+v))]^2 } du dv >0.   (7)
```

Here the analytic limits matter. For v>0 all integrations by parts have zero boundary terms, by endpoint order at least q. At infinity the squared derivatives are O(v^-2). As v decreases to zero, the derivative of order q-1 near its singular endpoint is uniformly bounded by a constant times u^(p-1), or (1-u)^(r-1) at the other endpoint, with harmless smooth remaining factors; p,r>=1 make these square-integrable. Truncate v first, then use dominated convergence in (5) and these bounds in (7). No divergent individual logarithmic integral is separated. The derivatives cannot all vanish: a function with zero order q at each endpoint and identically zero derivative of order q-1 would be the zero polynomial, whereas f/(u+v) is nonzero. Thus strictness is genuine.

This also yields an independent three-row first-jet check. The diagonal linear coefficient is proportional to integral f f^(2q-1)=0, by odd-order integration by parts. In the U chamber the only possible linear term is proportional to x, and in the V chamber to y, so their diagonal vanishing proves both full first jets vanish. The accepted all-rank first-jet theorem is therefore consistent with, but not required to extrapolate into, this quadratic argument.

When q=1, (5) integrated once gives the explicit positive value


```text
A(p,1,r)=(p+r-1)!(2p-1)!(2r-1)!
            /[2 p! r! (2p+2r-1)!].
```

The general integral also gives A(p,q,r)=A(r,q,p). For example A111=1/12, A112=1/40, A212=3/560.

## 4. Exact remaining obligation

For a supported three-occupied assignment at positive margins, x,y>0. On x=y=s, the theorem pays the entire signed quadratic term A s^2. Off the wall, (3) leaves precisely B_U>=0 and B_V>=0 as sufficient and necessary conditions for positivity on their full positive slope cones. Their finite factorial/harmonic sums are explicit. All 1,120 chamber forms for occupations N=3..16 have positive A,B and zero square coefficient in the transverse variable. This is bounded evidence; the two unbounded B inequalities are CONJECTURED, not proved here.

The full original still includes its one- and two-occupied sectors. The first is a positive product; the second can be adverse, as the complete T1 decomposition shows. Even proving both B inequalities does not pay the entire polynomial. The next complete sign question must retain actual column allocations and legal margins and pay their complete one/two/three-class sum. General three-row c2, higher coefficients, whole rank seven and unrestricted KTT remain open.

Verification/quadratic_wall_v1.py independently checks both factorial/harmonic formulas against the original falling-product jets, the complete Rodrigues identity, the diagonal coefficient formula and q=1 special case for every occupation N=3..16. Both full diagonal chamber polynomials are also joined through N=9. These finite checks support the explicit analytic proof; they do not supply its all-occupation quantifier. The corresponding mathematical data and trusted checking route are described in the module guide.
