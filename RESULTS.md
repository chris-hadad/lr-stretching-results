# Results and open questions

Every coefficient below is in the ordinary monomial basis of the stretch
parameter. A negative root-location property or concavity gap is not a
negative ordinary coefficient.

| Module | Established result | Important limit | Reproduce from repository root |
|---|---|---|---|
| [Positive cone and root threshold](results/hurwitz-cone/README.md) | Degree31, all528 bivariate coefficients positive; u>=22v gives at least2 open-RHP roots; primitive q slice stable exactly1..22 | No uniform exact root count, crossing uniqueness, varying-rank theorem or priority claim | `python3 -B results/hurwitz-cone/reproduce.py` |
| [R18 anchor](results/hurwitz-counterexample/README.md) | K_((7t,6t,5t),(t^18)) has32 positive coefficients and exactly2 open-RHP roots | No minimum-rank/size result | `python3 -B results/hurwitz-counterexample/reproduce.py` |
| [Parabolic A3](results/parabolic-a3/README.md) | Full ordinary LR realization; q1>=0 in every root direction for24 specified multiplicity systems, q2>=0 for16 | Other multiplicities and higher coefficients remain open | `python3 -B results/parabolic-a3/a3_reproduce.py` |
| [Coefficient cone](results/coefficient-cone/README.md) | On an explicit rank18 cone, sharp positive c1/c2 lower bounds; c1 and sqrt(c2) concave and superadditive | c3..c19 and full-polynomial positivity uncomputed | `python3 -B results/coefficient-cone/reproduce.py` |
| [Two-row nonconcavity](results/two-row-nonconcavity/README.md) | Every index j>=2 admits a raw weight-concavity failure; exact symbolic/quadratic formulas | Rooted-coefficient concavity and balancing monotonicity not refuted | `python3 -B results/two-row-nonconcavity/two_row.py` |

The two-variable root theorem is the most developed candidate for a focused
write-up. It extends the isolated R18 example to a full positive cone and an
infinite family that survives common-dilation and determinant-twist
identifications. Mathematical novelty remains a question for literature
comparison and expert feedback.

## Other verified work, catalogued without standalone modules

Three specific real closed rank-six boundary cones have exact count formulas

    E32 = ((x+1)(y+1)(x+y+2)/2) binom(z+7,7),
    E33 = (x+1+z/3)(y+1+z/3) binom(z+8,8),
    E34 = (b+1)(c+1)(a+1+(b+c+z)/2) binom(z+7,7).

The source proofs use integral GT/simplex and interval/rectangle/simplex
lattice maps. Their domain cones and boundary-coordinate maps are essential
hypotheses, not supplied by the formulas alone. Each stretching specialization
is coefficient-nonnegative and has only negative real zeros when nonconstant.
The full cone definitions and proof packages are not included here. The exact
source identities are recorded in [PROVENANCE.md](PROVENANCE.md).

A separately verified theorem gives nonnegative, symmetric concave ordinary
linear coefficient on its specified capped two-row skew-weight domain. Its
full concavity proof is not included. The general coefficient formula and
endpoint correction are in the two-row module, together with the higher-index
obstruction. Positivity of a difference of prism-slice counts does not follow
from positivity of the two slices individually.

Three degree-16 central GL3 controls were fully verified with independent
count models and unused holdouts. They validate the character/reciprocity/
direct-coefficient instruments but are not claimed as novel positive families.
Large finite positive panels are likewise evidence at their exact rosters,
not proofs of unrestricted KTT positivity.

## Live mathematical questions

- Complete the homogeneous cubic on the seven A3 cones for
  m=(7,7,7,11,11,13); existing data and exact symmetries leave nine new
  direction values. Negative mixed coefficients alone are insufficient:
  an exact negative value at a legal direction is required.
- Extend the rank18 coefficient cone through c3 and determine the appropriate
  rooted-coefficient geometry, retaining every chamber and wall.
- Explain the varying-rank natural root family: finite data suggest a
  reciprocal Hurwitz determinant sign, but no all-rank proof is established.
- Seek whole-LR counterexamples beyond the tested multiplicity systems,
  weighted fibers and higher-rank constructions, while pursuing rank-six/seven
  positivity certificates independently.

Ferudun's rank-at-most-five source theorem is an established dependency of
the research program, with earlier certificate inputs explicit. This repository
does not reproduce that source theorem. The smallest unresolved rank under
that adopted theorem is six. See [REFERENCES.md](REFERENCES.md).
