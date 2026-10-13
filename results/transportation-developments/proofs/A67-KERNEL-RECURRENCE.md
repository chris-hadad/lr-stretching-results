# A67: a positive zero-column recurrence at every occupation

Curated accepted mathematical source; the module guide states its exact domain.


Proposed root corollary of the complete original Lagrange expansion and A65's positive wall integral, pending the A67 gate. For every p,q,r>=1,


```text
A(p,q,r)=A(p+1,q,r)+A(p,q+1,r)+A(p,q,r+1).          (1)
```

This is an exact identity, not a recurrence guessed from a finite positive table. It keeps the actual column-labeled expansion; it does not permit arbitrarily selected compensation weights in a whole table.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Proposed root corollary of the complete original Lagrange expansion and A65's positive wall integral. For every p,q,r>=1,

## Complete rational identity with the original offsets

For three formal variables z1,z2,z3 put


```text
L_i=z_i^2 / product_(j!=i)(z_i-z_j).
```

Quadratic Lagrange interpolation gives L1+L2+L3=1, the complete identity for h_0. For a fixed assignment with occupations n and column totals C, its whole rational summand before coefficient extraction is


```text
product_i z_i^(t C_i) L_i^(n_i).
```

Multiplying this by L1+L2+L3 adds one labeled zero-width column in its three possible classes. The resulting terms have occupations n+e_i, unchanged column totals and unchanged original row margins. All are expanded in the SAME formal orientation z2/z1,z3/z1,z3/z2. Thus the original sign and offset changes arise automatically, once, from the factors L_i; they are not held artificially fixed.

Coefficient extraction therefore gives an exact count identity on every integer grade. On an open positive slope cone all four terms eventually use their full A65 chamber polynomials, so their finite polynomial identity follows. On the equal-slope line both complete diagonal restrictions agree for positive occupations by the accepted A65 initial-band argument. Taking the quadratic term there yields (1). In fact the same argument gives the full off-wall quadratic recurrence on either slope cone. No zero-occupation positivity is asserted by this argument.

Because all three terms are strictly positive, increasing any one occupation strictly decreases A. This is a structural constraint useful for aggregation, not an inequality for whole table polynomials with columns removed.

## A single positive measure represents all wall coefficients

There is a unique finite positive measure mu on the closed simplex


```text
Delta={u1,u2,u3>=0, u1+u2+u3=1}
```

such that


```text
A(p,q,r)=integral_Delta u1^(p-1)u2^(q-1)u3^(r-1) dmu,
mu(Delta)=A(1,1,1)=1/12.                           (2)
```

This follows from (1) and positivity without requiring an unproved density formula. For m>=1 define the positive finite discrete measure


```text
mu_m=sum_(k1+k2+k3=m) multinomial(m;k1,k2,k3)
      A(k1+1,k2+1,k3+1) delta_(k/m).
```

Repeated use of (1) gives its total mass 1/12. For nonnegative d_i with D=sum d_i and m>=D, factorial cancellation and the same recurrence give exactly


```text
sum_k multinomial(m;k) A(k+1)
      product_i (k_i)_(d_i)/(m)_D = A(d1+1,d2+1,d3+1),
```

where these factorials are FALLING factorials. On the compact simplex, replacing the factorial ratio by product_i(k_i/m)^(d_i) introduces a uniformly vanishing O(1/m) error for fixed d. The measures have a weakly convergent subsequence because their masses are fixed on a compact set. Its limit has the asserted moments. Polynomials are dense in continuous functions on Delta, so these moments determine the finite measure uniquely and all subsequences have the same limit. A65's outer-occupation symmetry makes mu invariant under swapping u1 and u3. No full permutation symmetry or boundary density is claimed.

Verification: the exact recurrence passes all 680 positive occupations through total 17 using the independently checked A67 wall coefficients. The separate recurrence verifier checks full original-offset polynomial identities on both open cones and their tie, and the factorial-moment normalization on its complete declared finite domain. These are implementation checks of the all-occupation proof, not a substitute for it.
