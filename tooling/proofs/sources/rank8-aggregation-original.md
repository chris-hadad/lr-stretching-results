# Complete column-moment contraction of the three-cut LR count

Root derivation, FRI, 9 September 2026. This is a proposed exact contraction
of the adopted complete A05 tableau map, pending computational and independent
verification. It asserts no ordinary coefficient sign.

Write `m=M*t`, `s=S*t`, with integers `0<=s<=2m`. Group the cross matrix's
rows as row one, row two and the final two rows. Their totals are `p,q,r`,
where `p+q+r=s` and `r<=m` for a nonempty bottom child. The bottom count is

```text
F(m,q,r)=B(m-r)-V(m-r,max(0,q-m)),
B(x)=(x+1)(x+2)(x+3)/6,
V(L,k)=k(k+1)(3L+5-2k)/6.
```

Its value is zero at `r>m`. The original three-cut proof supplies all
domain and lattice premises; grouping retains every labeled matrix entry.

## Uncut top contribution

Conditional on `p,q,r`, the cross entries form independent uniform weak
compositions into four, four and eight labeled positions. Let `C` be the
total of columns three and four. Symmetry gives `E(C)=s/2`, zero third
centered moment, and

```text
Var(C) = p(p+4)/20 + q(q+4)/20 + r(r+8)/36.
E B(m+C) = B(m+s/2) + (1+(m+s/2)/2)*Var(C).
```

The variance follows directly from the weak-composition factorial moments
`E X_i=T/N`, `E X_i(X_i-1)=2T(T-1)/(N(N+1))` and
`E X_i X_j=T(T-1)/(N(N+1))` for distinct positions. This is a full exact
conditional average, with multiplicity
`binom(p+3,3)*binom(q+3,3)*binom(r+7,7)`.

## The three cuts collapse to two one-column tails

Let `z` denote a distinguished column total. Conditional on its entries and
the row-group totals, the other three columns are exchangeable. Thus each
has expected total `(s-z)/3`, even after weighting by the bottom count.

For the first top exclusion, take `z=c2` and `k=(s-m-z)_+`. Since
`E(C)=2(s-z)/3` conditionally,

```text
E V(m+C,k) = 5(m+1)*k(k+1)/6.
```

The second top exclusion and the intersection occur only at `z=c4>m`.
Put `ell=z-m`. Here `c2<=s-z<s-m`, so the first cut is automatically
active: `k=s-m-c2`. The adopted condition `s<=2m` makes the intersection
formula valid. Combining it with the second excluded volume gives

```text
W(k,ell)-V(m+C,ell)
 = ell(ell+1)*(3k-3(m+C)+ell-4)/6.
```

Taking the conditional mean `E(c2+c3)=2(s-z)/3` reduces this exactly to
`(s-7m-4)*ell(ell+1)/6`. No negative-width polynomial continuation is used.

For a group of `a` matrix rows with total `u`, the number of assignments
with distinguished column total `z` is

```text
H_(u,a)[z] = binom(z+a-1,a-1)*binom(u-z+3a-1,3a-1).
```

Convolve `H_(p,1)`, `H_(q,1)` and `H_(r,2)`, then sum with weight
`F(m,q,r)`. Call the resulting complete one-column distribution `D[z]`.
The entire LR count is the uncut contribution above minus

```text
sum_z D[z] * [5(m+1)*(s-m-z)_+*((s-m-z)_++1)
             +(7m+4-s)*(z-m)_+*((z-m)_++1)] / 6.
```

This computes at most quadratically many row-total groups, with polynomial
convolutions of degree at most `s`. The straightforward implementation uses
`O(s^4)` exact integer operations and polynomial storage, replacing the
`binom(s+15,15)` literal matrix enumeration. The cost includes large-integer
arithmetic and is not a universal LR complexity claim. Every value of `m,s`
in the supported integer domain, the walls and the origin is included.
