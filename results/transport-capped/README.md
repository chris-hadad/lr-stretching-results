# Whole transportation and capped LR families

Every ordinary coefficient is nonnegative for every balanced nonnegative transportation polytope with at most three rows and five columns, including smaller or transposed sizes. The same is true of the complete coupled-capacity LR family below with at most four capacities. Coefficients through actual degree are strictly positive; a point has polynomial one. These are all-margin, all-area family results. Whole ordinary rank six/seven and unrestricted KTT remain open.

| Entire object | Ordinary LR realization | Complete certificate |
| --- | --- | --- |
| 3-by-4 transportation matrices | Rank six, actual degree six for positive margins | Every raw local weight is positive; uniform face-volume margin 1/720 |
| 3-by-5 transportation matrices | Rank seven, actual degree eight for positive margins | Three complete rational corrections protect c1,c2,c3; all higher weights are positive; uniform margin 1/1000000 |
| Four coupled capacities | The displayed rank-six, actual-degree-seven one-overlap family when capacities,c,d are positive | Every raw local weight is positive; uniform face-volume margin 1/300 |

The coupled-capacity object counts ALL nonnegative y,z satisfying sum z_i=c*t, sum y_i<=d*t and y_i+z_i<=w_i*t, for nonnegative integer data with sum w>=c+d. Its exact entire LR constructor, all boundary cases and full proof are in [the certificate proof](../../tooling/transport_certificates/PROOF.md). The capacity inequalities are retained; they are not dropped by extrapolating the easier binomial chamber. General one-overlap LR families and five or more capacities keep their separate open coefficient questions.

The complete finite proof uses 22,063 original normal subsets, of which 16,848 are independent. Every dependent complement, original lattice, metric and local constant is reconstructed. At 3-by-5, the 70, 56 and 28 negative raw weights at q5,q6,q7 are all retained and corrected. The three fields fit in a 58 KB JSON file and require no numerical solver to verify. [Verification and review](VERIFICATION.json) states the exact executed scope and its limits.

## Reproduce

From the repository root, with Python 3.11+:

```sh
python3 -B tooling/transport_certificates/verify.py --out /path/to/new-check
PYTHONPATH=tooling python3 -B -m unittest three_row_coefficients.test_coefficients
python3 -B results/transport-capped/reproduce_examples.py
python3 -B results/transport-capped/test_examples.py
```

The first command reconstructs the complete finite certificate using only the standard library; a first source run took about eight seconds on the recorded host. The second performs independent count, affine-offset, boundary and refusal controls. The third reproduces the full example and quotient vectors. The fourth rejects missing/duplicate families, directions, parent records and count grades. [The module guide](../../tooling/transport_certificates/README.md) also gives the optional independent C++/GMP comparison and its process limits. A favorable sample is not the all-margin proof.

## Whole low-dimensional quotients

The complete parent face-volume bounds imply positive entire stabilized quotients along every feasible whole direction of actual dimension at least one in these precise families, including the one- and two-dimensional directions. [The full argument and examples](QUOTIENTS.md) retain the saturated lattice, stabilization and every parent coefficient. They do not identify an arbitrary projection or proper face with a whole LR object, and no ordinary LR rank is assigned to a quotient.

The whole-family theorem also protects each initial and intermediate parent inside the family. General rank-six c1,c2,c3 and bases outside these constructors remain open. [Point rays and actual chambers](POINT-RAYS.md) explains a useful reduction and an exact failure of deleting point rays without its complete chamber hypothesis.

## Sources and assessment

The work uses the classical Berline-Vergne local formula, Alper Ferudun's correction approach, complete normal-cycle balance, and full Schur/Pieri/tableau identities. The independent Python and C++ programs use different exact arithmetic implementations of the same mathematical recurrence. The coefficient program is separately checked against unsigned counts. These are computer-assisted results available for scrutiny, without a claim of external human acceptance.

[The bounded novelty assessment](NOVELTY.md) distinguishes this finite family advance from prior results and from a worldwide priority claim. Software is MIT; original exposition and data are CC BY 4.0, under the repository's [license and attribution policy](../../LICENSING.md). [Source mapping](SOURCE-MAP.json) binds the complete selected bytes.
