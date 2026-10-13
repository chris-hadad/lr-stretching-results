# A complete four-letter family at arbitrary rank

For every integer m>=3, s>0 and u>=3s, retain every displayed physical row:


```text
lambda=(ms+6u,ms+5u,ms+4u,ms+3u,ms,(m-1)s,...,s),
mu=(ms+3u,ms+2u,ms+u,ms,(m-1)s,(m-2)s,...,0),
nu=((m-3)s+6u,s+3u,s+2u,s+u).
```

Lambda is outer. The entire original stretching polynomial is strictly
positive in ordinary degrees zero through its actual degree 3m+3, at physical
rank m+4. Its complete tableau chart has saturated lattice Z^(3m+3), every
coupled tail capacity, original inner zero and all three ballot-prefix families.
At s=0 the entire original is 1+ut, with degree one when u>0 and the point at u=0.

## An entire paid height cover

There is a complete W_m, strict in degrees zero through 3m+2, for which


```text
C_m(S,U+V)-C_m(S,U)=V W_m(S), U>=3S,V>=0.
```

On original stretching rays the gain is vt W_m(st), strict in every nonconstant
degree through 3m+3 when s,v>0. The actual baseline u=3s is paid. Reversing
integral height steps decreases u-3s and terminates there, so this is a complete
original-generating cover of this exact family.

[The full proof](proofs/A82-FOUR-LETTER-HEIGHT-v1.md) derives the original chart,
eighteen complete interval comparisons, degree, whole symmetry moment,
zero-/one-/two-cap inclusion-exclusion, positive one-cap telescoper, full
same-coefficient double-cap payment and uniform rational majorants. It proves
all-grade polynomiality directly. No unverified period-one premise is imported.
The complete signed sufficient-bound negatives remain paired with their
positive parent and all five compensation terms.

Two exact independent defining representations agree on every required finite
base. The full G^W_3 has 12 strict slots and G^F_12 has 40; the nine full F bases
m=3..11 have 225 slots. Positive consecutive-factor recurrences supply the
unbounded m quantifier. The stored complete data also contains all 265 F and
255 W slots at m=3..12, their masks, moments, omissions, boundary conventions
and the 94 negative sufficient-bound slots with full compensation.

## Portable reproduction

With Python 3.11+ and SymPy for the symbolic command:

```sh
python3 -B verification/check_recent_sources.py --module four-letter
python3 -B results/four-letter/code/exact_arithmetic.py --phase full --output /path/to/new-four-letter-finite
python3 -B results/four-letter/code/symbolic_certificates.py --output /path/to/new-four-letter-symbolic
```

The first arithmetic program uses only the standard library. The second clears
positive denominators and reconstructs free-variable numerator/residual
certificates, complete telescopers and consecutive-factor ratios. Both are
trusted separately authored root implementations, with portable output paths;
neither imports or executes provider code. Their arithmetic is exact.
[Verification status](VERIFICATION.json) records the actual fresh-export checks.
The proof and source map credit Pro057 Phase 0/U03/U04 and the subsequent Codex
reconstruction; internal AI review is not human peer review or formal certification.

All lower four-letter heights s<=u<3s, raw index gains, arbitrary shapes/content,
whole rank seven and unrestricted KTT remain open. A formal stable-interval
extension below 3S is not the complete original and is retained only as a control.

The complete original-geometry controls are also portable: `python3 -B results/four-letter/code/verify_geometry.py /path/to/new-four-letter-geometry` checks every simplex comparison, all original row/column/ballot slacks, strict witnesses, full symmetry orbits and both omission witnesses without an LR backend.
