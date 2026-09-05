# A positive Littlewood–Richardson cone with a sharp root threshold

Let \(\rho_m=(m,m-1,\ldots,1)\). For integers \(u,v\ge0\), \(u+v>0\), define

\[
\lambda=(u+v)\rho_{18},\qquad
\mu=(u+v)\rho_{17},\qquad
\nu=(7u+8v,6u+6v,5u+4v),
\]

with lambda the outer partition. The ordinary stretching polynomial
\(T_{u,v}(t)=c^{t\lambda}_{t\mu,t\nu}\) has degree 31 and all 32 coefficients
strictly positive. It has at least two zeros in the open right half-plane
whenever \(u\ge22v\).

On the primitive slice \((u,v)=(q-1,1)\), the polynomial is strictly Hurwitz
stable exactly for positive integers \(q\le22\), and unstable for every
\(q\ge23\). The complete bivariate polynomial
\(T_{u,v}(t)=H(ut,vt)\) has all 528 coefficients strictly positive.

The [proof](PROOF.md) gives the full LR realization, prior degree bound,
closed-chamber formula, coefficient argument, uniform Rouché cover, exact
Routh threshold, and existence of a nonzero imaginary-axis crossing between
the normalized parameters 1/23 and 1/22. The uniform assertion is at least
two RHP roots; exactly two is certified at q=23. Crossing uniqueness and
transversality are not claimed.

## Reproduce the arithmetic

Python 3.10 or later and its standard library are sufficient:

```sh
python3 reproduce.py
```

Successful completion prints the verified polynomial degree, positivity count,
control counts, finite root threshold, and seven-certificate uniform cover.
To save all reconstructed coefficients, Routh tables, count controls, and
exact rational Rouché inequalities:

```sh
python3 reproduce.py --output reproduction.json
```

[checker.py](checker.py) constructs H from the finite profile formula using a
degree-31 simplex and exact Newton conversion. It then reconstructs F and
compares every rational coefficient with [theorem-data.json](data/theorem-data.json).
Those simplex values are evaluations of the profile polynomial, not a native
tableau-count grid. Additional checks compute 31 literal-flow counts and nine
positive character-grid counts by separate formulas, and verify 10,816 finite
instances of the short-flow identity.

The checker specializes its reconstructed H for q=1,...,23 and calculates
regular exact Routh tables. It reconstructs every Taylor coefficient needed
by the seven proposed disks, using exact rational modulus bounds and strict
squared Rouché inequalities. Six known-root controls and five negative
fixtures exercise the root checks. Eight additional negative fixtures reject
missing determining/holdout data, wrong holdout sites and inexact count values.

The data file contains the complete F and H tables, the seven rational disk
proposals and parameter intervals, and all 23 q coefficient/value records.
Every root conclusion is recalculated. Floating root approximations are not
part of the verification.
