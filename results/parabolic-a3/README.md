# Exact A3 ray and quadratic certificates

This standalone module reconstructs 376 complete ray/pair polynomials for
the six-root vector partition function

```
K_m(X,Y,Z) = [U^X V^Y W^Z]
 (1-U)^(-p) (1-V)^(-q) (1-W)^(-r)
 (1-UV)^(-u) (1-VW)^(-v) (1-UVW)^(-w),
m=(p,q,r,u,v,w).
```

For the 24 multiplicity systems in the data, it certifies nonnegativity of
`[t] K_m(tR)` for every integral nonnegative R. For the designated subset of
16 systems, it certifies the same conclusion for `[t^2] K_m(tR)`. A parabolic
character construction realizes these counts as full ordinary stretched
Littlewood–Richardson coefficients; `PROOF.md` gives the construction and
the mathematical dependencies.

## Reproduce

Place these four files together and run:

```
python3 a3_reproduce.py
```

The program uses the Python standard library, reads only `a3-data.json`,
writes no files, and needs no network or additional software. An optional
single argument selects the mathematical JSON file explicitly. Successful
completion prints the exact scope reconstructed; disagreement raises an
error and exits unsuccessfully.

The reconstruction checks all 83 root minors and 112 cone/basis comparisons,
then independently counts enough signed determining values for every full
polynomial using a prior geometric degree bound. Each polynomial also has
two directly counted unused positive holdouts. All 168 linear ray values
and 672 quadratic cone monomial coefficients are reconstructed and compared
with the attached certificates.

The complete reconstruction uses 8,035 signed determining values and 752
unused positive holdouts. The mathematical data file is approximately
656 KB; no external data files are needed.

## Files and data conventions

- `PROOF.md`: whole-count realization, admissibility, lattice and degree,
  seven-cone argument, sign certificates and counting derivation.
- `a3_reproduce.py`: positive grouped-flow counting and exact rational
  reconstruction.
- `a3-data.json`: roots, rays, cones, fixed system rosters, complete rational
  coefficient vectors, prior degrees, two positive holdouts per polynomial,
  and the linear/quadratic certificates.

Polynomial coefficient vectors are in increasing powers of t. Quadratic
`diagonal` entries follow the listed cone generators; `mixed` entries are
the coefficients of XY, XZ, YZ in that order. Every supplied polynomial is
complete through its actual degree. A coefficient above that degree is
zero, including linear or quadratic coefficients of constant polynomials.

This is an independently implemented computation from the mathematical
grouped-flow formula, packaged with independently reconstructed coefficient
records. It is not an additional independent implementation of that
verification. Classical Weyl characters, unimodular chamber polynomiality
and Ehrhart reciprocity are explicit premises. No novelty claim is made.
The infinite-direction conclusions concern exactly the named fixed systems
and coefficient indices. Higher coefficients at uncomputed directions and
other multiplicity systems remain outside these certificates.
