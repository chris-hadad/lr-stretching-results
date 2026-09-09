# An exact bare-triple counter on the Cdagger sector

`cdagger_count(lam, mu, nu, t=1)` evaluates the whole ordinary LR count on the
proved Cdagger sector. `cdagger_polynomial(lam, mu, nu)` returns every ordinary
coefficient as an exact rational. Lambda is outer; inner partitions are never
silently exchanged. Inputs are exact integer partitions with size balance and
maximum trimmed length six. Trailing zero padding is immaterial.

The original triple must satisfy the complete domain, even when `t=0`.
`OutsideCdaggerError` means the valid triple is outside this sufficient sector.
It does not mean its hive is empty, its coefficients are negative, or a more
general count is impossible. Invalid partitions and inexact inputs are refused.

```python
from slr_ehrhart import cdagger_count, cdagger_polynomial

lam = [43, 38, 33, 20, 12, 6]
mu = [22, 17, 16, 12, 6]
nu = [26, 21, 16, 12, 4]
assert cdagger_count(lam, mu, nu) == 4590
assert len(cdagger_polynomial(lam, mu, nu)) == 11
```

## Whole-object premise and fixed proof data

The adopted whole-cone proof is Astra003 A01/WHOLE-CONE-POSITIVITY.md and its
successful A003-STRIP-EXTENSION-003 certificate. Cdagger retains all 521
essential Horn inequalities, 18 partition inequalities and 17 of the original
19 source facets on the rank-six trace section. Removing exactly source facets
0 and 6 permits the two complete strip cuts. Duplicate projected inequalities
leave 553 distinct domain rows. The implementation checks all of them.

The common integer slack chart uses original rhombus rows
`(22, 17, 34, 41, 27, 30, 37, 39, 10, 43)`. Its integer inverse identifies
the full ten-coordinate hive lattice. Fifteen selected rhombus inequalities
give one interval of length `x` and the complete strip with group sizes
`h=q1=q2=3`. Thirty exact nonnegative implications recover every omitted
rhombus. Six further implications establish all physical parameter premises.
No selected vertex set or scalar agreement supplies these missing directions.

`verify_cdagger_certificate()` reconstructs the full conventional hive matrix,
checks both integer inverse identities, authenticates the fifteen model rows,
and replays all thirty-six ambient identities with their trace multipliers.
The shipped data keeps every domain row and every nonzero rational multiplier.
Source SHA and the mechanical sparse projection are recorded separately.

For padded boundaries define

```text
H3 = sum(mu[i] + nu[i] - lam[i] for i in range(3))
s5 = lam[4] - mu[4] - nu[5]
s6 = lam[5] - mu[5] - nu[5]
Dnu = nu[4] - nu[5]
x = mu[1] - mu[2]
T = H3; B = s5-Dnu; C = H3+Dnu-s6; D = s6-H3.
```

The exact matrix forms in the implementation agree with these on the trace
section. They satisfy `x,T,B,C,D>=0` and `T<=B+C+D`. The full count is
`(t*x+1) * strip_count(3,3,3,T,B,C,D,t)`. The all-parameter binomial identity
has degree at most ten. Finite differences at that proved bound recover the
complete polynomial, including all dimension drops.

## Integer evaluation of the general strip

The maintained `strip_count` also accepts general groups `h>=0`, `q1,q2>=1`.
Write `N=h+q1+q2`. At stretch one its interval length is

```text
D+1 - V + min(C,U+V) + min(B,V),
```

after clamping B and C to T. Sum the constant and first moment over all
N-part compositions. Each capped moment has the adopted rising-binomial
expansion with N terms. Its only denominator disappears through

```text
(W/r) * binom(W+r-1,r-1) = binom(W+r-1,r).
```

This gives at most `2*N` integer binomial terms, without loops over the
parameter magnitude. It is faster than the positive rational expansion and
the grouped direct sum on the measured controls. It uses exact subtraction;
ordinary positivity comes from the separate complete positive expansion,
not from numerical cancellation or a claim that subtraction preserves signs.
Integer bit cost and dimension still matter.

Both original whole-hive degree-ten vectors match all eleven coefficients.
Four fresh bare-triple LR calls agree at t=1,2 for the original and neighbor
controls. A transposed-inner control is correctly refused by the domain even
though its LR count agrees by inner symmetry. The exact source cone, all-rank
positivity and full original-box coverage remain distinct claims.
