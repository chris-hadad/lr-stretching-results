#!/usr/bin/env python3
"""Targeted exact checks for the constructive closure API (run by integrator)."""

import argparse
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

from constructive_hive_closure import analyze_branch, load_verified_certificate, normal_rank


SOURCE_EDGE = (14, 12, 16, 17, 15, 36, 44, 7, 2)
MISSING_RULE_SEED = (4, 17, 18, 23, 31, 41)


def fraction(pair):
    return Fraction(pair[0], pair[1])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def run(certificate: Path, atlas: Path, receipt: Path) -> None:
    data = load_verified_certificate(certificate, atlas, receipt)

    missing = analyze_branch(data, MISSING_RULE_SEED)
    assert missing["classification"] == "excluded_rank_increase"
    assert (missing["rank_selected"], missing["rank_closure"]) == (6, 8)
    assert missing["closure_physical_rows"] == [2, 3, 4, 7, 8, 9, 11, 17, 18,
                                                 23, 24, 26, 31, 35, 39, 40, 41, 44]

    # The atlas gives rows 7 and 9 the same interior normal label, but their
    # physical rows remain distinct. The API must classify their joint branch.
    assert data.normals[7] == data.normals[9]
    dependent = analyze_branch(data, (7, 9))
    assert dependent["classification"] == "dependent"
    assert dependent["rank_selected"] == 1

    edge_case = analyze_branch(data, SOURCE_EDGE, expand_fractions=True)
    assert edge_case["classification"] == "retained_independent"
    assert edge_case["rank_selected"] == edge_case["rank_closure"] == 9
    witness = edge_case["witness"]
    boundary = witness["boundary"]
    assert sum(boundary["lambda_outer"]) == sum(boundary["mu"]) + sum(boundary["nu"])
    for word in (boundary["lambda_outer"], boundary["mu"], boundary["nu"]):
        assert len(word) == 6 and all(word[i] >= word[i + 1] >= 0 for i in range(5))
    legal = boundary["legal_height"]
    assert witness["physical_slacks_at_legal_height"] == [dot(row, legal) for row in data.rows]
    assert [i for i, value in enumerate(witness["physical_slacks_at_legal_height"]) if value == 0] == edge_case["closure_physical_rows"]

    face = witness["face"]
    assert face["dimension"] == 1
    edge = face["edge"]
    direction = edge["primitive_direction"]
    assert gcd(*direction) == 1
    assert all(dot(data.normals[r], direction) == 0 for r in edge_case["closure_physical_rows"])
    lo, hi = map(fraction, edge["parameter_interval"])
    assert lo < 0 < hi and hi - lo == fraction(edge["saturated_length"])
    for endpoint in edge["endpoints"]:
        height = list(map(fraction, endpoint["full_height"]))
        assert all(dot(row, height) >= 0 for row in data.rows)
        assert all(dot(data.rows[r], height) == 0 for r in SOURCE_EDGE)

    recipe = witness["positive_generic_relaxation"]
    expanded = recipe["expanded"]
    Y = [list(map(fraction, row)) for row in recipe["right_inverse_Y_rows"]]
    selected = sorted(SOURCE_EDGE)
    for i, row_id in enumerate(selected):
        for j in range(len(selected)):
            assert sum(data.normals[row_id][k] * Y[k][j] for k in range(10)) == int(i == j)
    tau = fraction(recipe["tau"])
    delta = list(map(fraction, expanded["delta_by_physical_row"]))
    for r in range(45):
        assert delta[r] == recipe["integral_a_by_physical_row"][r] + tau ** (r + 1)
    ydelta = list(map(fraction, expanded["ydelta"]))
    assert ydelta == [recipe["integral_y0"][k] - sum(Y[k][s] * tau ** (row + 1)
                      for s, row in enumerate(selected)) for k in range(10)]
    epsilon = fraction(recipe["epsilon"])
    for r, recorded in enumerate(expanded["perturbed_slacks_by_physical_row"]):
        exact = dot(data.rows[r], legal) + epsilon * (dot(data.normals[r], ydelta) + delta[r])
        assert fraction(recorded) == exact
        assert exact == 0 if r in selected else exact > 0

    # At an endpoint of this positive-length edge, a newly tight independent
    # physical row gives a full-rank point face in the SAME nonpoint parent.
    endpoint_height = list(map(fraction, edge["endpoints"][0]["full_height"]))
    extra = next(r for r in range(45) if r not in selected
                 and dot(data.rows[r], endpoint_height) == 0
                 and normal_rank([data.normals[s] for s in selected + [r]]) == 10)
    full_rank = analyze_branch(data, selected + [extra])
    assert full_rank["classification"] == "retained_independent"
    assert full_rank["rank_selected"] == full_rank["rank_closure"] == 10
    assert full_rank["witness"]["face"]["dimension"] == 0
    assert fraction(edge["saturated_length"]) > 0
    assert all(dot(data.rows[r], endpoint_height) == 0 for r in selected + [extra])
    print("PASS: obstruction, physical dependency, exact edge/perturbation, and full-rank point in a nonpoint parent")


if __name__ == "__main__":
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for constructive hive closure checking')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--atlas", type=Path, required=True)
    parser.add_argument("--verification-receipt", type=Path, required=True)
    args = parser.parse_args()
    run(args.certificate, args.atlas, args.verification_receipt)
