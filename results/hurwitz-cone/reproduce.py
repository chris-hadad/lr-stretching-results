#!/usr/bin/env python3
"""Reconstruct the cone polynomial and verify its exact root certificates."""
import argparse
import json
from pathlib import Path
import sys

import checker as c

if hasattr(sys, "set_int_max_str_digits"):
    # Some exact rational certificate numerators exceed Python's display limit.
    sys.set_int_max_str_digits(0)


def reproduce():
    data = json.loads((Path(__file__).resolve().parent / "data/theorem-data.json").read_text())
    H, values, differences = c.construct_H()
    c.require(H == c.decode_poly(data["H"], ("u_degree", "v_degree")), "H coefficient table mismatch")
    c.require(len(H) == 528 and all(value > 0 for value in H.values()), "H support or positivity failure")
    c.require(H[0, 0] == 1 and max(i + j for i, j in H) == 31, "wrong constant or degree")
    F = c.linear_substitution(H, 2, -1, -1, 1)
    c.require(F == c.decode_poly(data["F"], ("x_degree", "y_degree")), "F coefficient table mismatch")

    fixtures = c.selftest(H, data["disks"])
    fixtures["invalid_count_data_rejected"] = c.count_data_selftest(H, data["q_records"])
    controls = c.count_controls(H)
    threshold = c.q_threshold(H, data["q_records"])

    endpoints = [c.Q(0), c.Q(1, 50), c.Q(3, 100), c.Q(9, 250), c.Q(1, 25), c.Q(21, 500), c.Q(43, 1000), c.Q(1, 23)]
    c.require(len(data["disks"]) == 7, "expected seven root certificates")
    certificates = []
    for i, disk in enumerate(data["disks"]):
        c.require(list(map(c.Q, disk["epsilon_interval"])) == endpoints[i:i + 2], "parameter cover gap or incorrect endpoint")
        certificates.append(c.rouche(H, disk))

    return {
        "degree": 31,
        "positive_H_coefficients": 528,
        "reconstructed_H": c.encode_poly(H, ("u_degree", "v_degree")),
        "reconstructed_F": c.encode_poly(F, ("x_degree", "y_degree")),
        "simplex_reconstruction": [
            {"u": a, "v": b, "polynomial_value": str(value), "newton_difference": str(differences[a, b])}
            for (a, b), value in sorted(values.items())
        ],
        "fixtures": fixtures,
        "count_controls": controls,
        "primitive_threshold": threshold,
        "uniform_root_certificates": certificates,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON file containing the full reconstructed mathematical certificates.")
    args = parser.parse_args()
    result = reproduce()
    if args.output is not None:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "degree": result["degree"],
        "positive_H_coefficients": result["positive_H_coefficients"],
        "F_and_H_coefficient_tables_match": True,
        "literal_count_controls": len(result["count_controls"]["literal_counts"]),
        "positive_character_grid_controls": len(result["count_controls"]["independent_positive_character_grid_counts"]),
        "short_flow_identity_controls": result["count_controls"]["short_flow_identity_cases"],
        "known_root_controls": result["fixtures"]["known_root_routh_controls"],
        "negative_fixtures_rejected": len(result["fixtures"]["negative_fixtures_rejected"]),
        "invalid_count_data_fixtures_rejected": len(result["fixtures"]["invalid_count_data_rejected"]),
        "regular_q_Routh_tables": result["primitive_threshold"]["regular_tables"],
        "strictly_Hurwitz_q_range": [1, 22],
        "q23_RHP_roots": result["primitive_threshold"]["q23_rhp_count"],
        "uniform_Rouche_certificates": len(result["uniform_root_certificates"]),
        "uniform_parameter_interval": ["0", "1/23"],
        "uniform_RHP_root_lower_bound": 2,
    }, indent=2))


if __name__ == "__main__":
    main()
