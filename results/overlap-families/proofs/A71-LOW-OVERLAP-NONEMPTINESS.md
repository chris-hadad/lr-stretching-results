# A71: nonemptiness throughout the enlarged low-overlap count class

Curated mathematical proof from **A71**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

Root corollary to LOW-OVERLAP-KERNEL.md, at its accepted scope. This proves integer-count nonemptiness, not ordinary coefficient positivity in the enlarged class. It resolves the zero-polynomial convention before the next sign problem.

Keep L>=1, B>=C>=0, H,G>=0 and B>=H+G. Since

```text
r_H/((1-x)(1-y)) = sum_(p>=H) h_p(x,y),
```

the ENTIRE kernel is the dominant coefficient of

```text
(sum_(p>=H) h_p)(sum_(q>=G) h_q)
                     (sum_(z>=0) h_z)^L.                 (1)
```

At a fixed total degree only finitely many terms contribute.

There is no unproved positivity premise here. Direct two-variable polynomial multiplication gives

```text
h_a h_b = sum_(k=0)^min(a,b) (xy)^k h_(a+b-2k).           (2)
```

Each (xy)^k h_(n-2k) is the complete two-row Schur polynomial. The highest-weight operator `[x^B y^C](1-y/x)` extracts its coefficient at (B,C): its two endpoint monomials are x^A y^K and -x^(K-1)y^(A+1), and the second cannot hit B>=C. Repeated application of (2), retaining the determinant powers, proves every complete product in (1) has nonnegative dominant coefficients.

Moreover choose

```text
p=max(H,C-G), q=G, v=p+q=max(H+G,C),
z=B+C-v.
```

Then C<=v<=B and C<=z<=B. Choose the k=0 term h_v in h_p h_q, and the k=C term in h_v h_z. It is exactly the Schur term for (B,C) with coefficient one. Take h_0 from the other L-1 free factors. This is a legal contribution to (1), so the full integer kernel satisfies K>=1 on this entire cone. The argument works when any of H,G,C,X is zero and uses L>=1 essentially. It supplies no sign law for the coefficients of K along a scaling ray or for a moving sum.

Now use the COMPLETE physical class in LOW-OVERLAP-KERNEL.md: h+g<=c, all 0<=j<=b, s>=j, three long rows at least b, detached widths at least b+c-h-g-j. For each positive grade t, choose in its residual domain

```text
x=max(0,(V-c)t), y=min(V,c)t.
```

Their sum is Vt, x<=delta t because V<=b, y<=ct and V<=U. The kernel target B0=ct+x is at least C0=y and (h+g)t. Thus this actual residual contribution is at least one. Every other residual kernel is nonnegative by (1)-(2). The ENTIRE LR count is therefore at least one at every positive grade. At t=0 its literal count is one and the nonempty polynomial's P(0)=1 convention agrees.

This extends nonemptiness, with the exact original boundary/lattice conventions, beyond the one-sided coefficient-positive theorem. The complete correction identity still contains ordinary-coefficient obligations: the strict prefix, returning reflected term and moving original sum cannot be signed from these positive integer values. Actual degree outside the selected positive class remains to be established before any future vector reconstruction.

The independent finite check reuses every one of the 1,880 authenticated full kernel values and separately checks (2) by exact polynomial multiplication for all a,b=0..12, including zeros. These controls introduce no new numerical LR original. The displayed arbitrary-parameter argument supplies the theorem.
**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root corollary to LOW-OVERLAP-KERNEL.md. This proves integer-count nonemptiness, not ordinary coefficient positivity in the enlarged class. It resolves the zero-polynomial convention before the next sign problem.
