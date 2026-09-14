#!/usr/bin/env python3
"""Rebuild the complete fixed example roster and whole-direction quotients."""

import json
import math
from fractions import Fraction as F
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tooling"))
from three_row_coefficients import capped_polynomial, transport_polynomial

# Frozen independently of the input file; a smaller input is not a smaller complete claim.
FAMILIES = {
    "cap-four-active": ("cap", (2, 3, 5, 7), (4, 5), 7),
    "cap-equality-wall": ("cap", (1, 1, 2, 2), (3, 3), 7),
    "cap-zero-c": ("cap", (1, 2, 2, 3), (0, 3), 7),
    "cap-zero-d": ("cap", (1, 2, 2, 3), (3, 0), 7),
    "cap-zero-weight": ("cap", (0, 1, 2, 3), (2, 2), 5),
    "cap-point": ("cap", (0, 0, 0, 0), (0, 0), 0),
    "transport-3x4": ("transport", (2, 3, 4), (1, 2, 3, 3), 6),
    "transport-3x5": ("transport", (3, 4, 5), (1, 2, 2, 3, 4), 8),
    "transport-zero-row": ("transport", (0, 2, 3), (1, 1, 1, 1, 1), 4),
    "transport-zero-column": ("transport", (2, 2, 2), (0, 1, 1, 2, 2), 6),
    "transport-point": ("transport", (0, 0, 0), (0, 0, 0, 0, 0), 1),
}
DIRECTIONS = {1: ((1, 1, 0), (1, 1, 0, 0, 0), 2), 2: ((2, 1, 0), (1, 1, 1, 0, 0), 3)}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def vector(values):
    need(
        isinstance(values, list) and all(type(x) is int and x >= 0 for x in values),
        "Nonnegative exact integer vector required",
    )
    return tuple(values)


def grades(records, expected):
    need(isinstance(records, list), "Count records must be a list")
    need(
        all(
            isinstance(row, dict)
            and set(row) == {"t", "count"}
            and type(row["t"]) is int
            and type(row["count"]) is int
            and row["count"] >= 0
            for row in records
        ),
        "Malformed independent count",
    )
    need(
        [row["t"] for row in records] == expected,
        "Missing, duplicate or reordered independent count grades",
    )


def expected_triple(kind, first, second):
    if kind == "cap":
        c, d = second
        total = sum(first)
        suffix = [sum(first[i:]) for i in range(len(first))]
        return [
            [total + c + 2 * d, total + c + d, *suffix],
            [total + d, total, *suffix[1:], 0],
            [total + d, c + d, c],
        ]
    rows, columns = first, second
    total = sum(rows)
    rs = [sum(rows[i:]) for i in range(len(rows))]
    cs = [sum(columns[i:]) for i in range(len(columns))]
    result = [
        [*(total + x for x in rs[1:]), *cs],
        [*([total] * (len(rows) - 1)), *cs[1:]],
        rs,
    ]
    for part in result:
        while part and part[-1] == 0:
            part.pop()
    return result


def validate_examples(data):
    need(
        isinstance(data, dict)
        and set(data) == {"schema", "families", "directions"}
        and data["schema"] == "transport-capped-examples-v1",
        "Example schema differs",
    )
    families = data["families"]
    directions = data["directions"]
    need(
        isinstance(families, list) and len(families) == len(FAMILIES),
        "Incomplete family population",
    )
    need(
        all(isinstance(row, dict) and type(row.get("id")) is str for row in families),
        "Family identity missing",
    )
    identities = [row["id"] for row in families]
    need(
        len(set(identities)) == len(identities) and set(identities) == set(FAMILIES),
        "Missing, duplicate or unexpected family identity",
    )
    for row in families:
        kind, first, second, D = FAMILIES[row["id"]]
        need(
            row["kind"] == kind
            and type(row["prior_degree"]) is int
            and row["prior_degree"] == D,
            "Frozen family kind or prior degree differs",
        )
        if kind == "cap":
            need(
                vector(row["w"]) == first
                and type(row["c"]) is int
                and type(row["d"]) is int
                and (row["c"], row["d"]) == second,
                "Frozen capped parameters differ",
            )
        else:
            need(
                vector(row["rows"]) == first and vector(row["columns"]) == second,
                "Frozen transportation margins differ",
            )
        need(
            row["unused_check_grades"] == [D + 2, D + 3], "Unused family grades differ"
        )
        need(
            row["triple"] == expected_triple(kind, first, second),
            "Whole LR triple does not match its frozen parameters",
        )
        grades(row["count_sites"], list(range(1, D + 4)))
        grades(row["literal_LR"], [1, 2] if kind == "cap" else [])
        need(
            isinstance(row["coefficients"], list)
            and 1 <= len(row["coefficients"]) <= D + 1,
            "Incomplete coefficient vector",
        )
    need(
        isinstance(directions, list) and len(directions) == len(DIRECTIONS),
        "Incomplete direction population",
    )
    need(
        all(
            isinstance(row, dict) and type(row.get("direction_dimension")) is int
            for row in directions
        ),
        "Direction identity missing",
    )
    identities = [row["direction_dimension"] for row in directions]
    need(
        len(set(identities)) == len(identities) and set(identities) == set(DIRECTIONS),
        "Missing, duplicate or unexpected direction",
    )
    for row in directions:
        r = row["direction_dimension"]
        ar, ac, S = DIRECTIONS[r]
        need(
            vector(row["base_rows"]) == (2, 2, 2)
            and vector(row["base_columns"]) == (2, 1, 1, 1, 1),
            "Frozen base differs",
        )
        need(
            vector(row["direction_rows"]) == ar
            and vector(row["direction_columns"]) == ac
            and type(row["S"]) is int
            and row["S"] == S,
            "Frozen direction or stabilization differs",
        )
        need(
            row["complete_cut_pairs"] == 256
            and row["max_nonnegative_cut_root"] == str(S - 1),
            "Complete cut roster differs",
        )
        need(
            row["unused_parameter_checks"] == [r + 1, r + 2],
            "Unused parameter values differ",
        )
        need(
            isinstance(row["parents"], list) and len(row["parents"]) == r + 3,
            "Incomplete parent vector population",
        )
        checks = row["independent_parent_counts"]
        need(
            isinstance(checks, list)
            and all(type(x["u"]) is int for x in checks)
            and [x["u"] for x in checks] == list(range(r + 3)),
            "Missing or duplicated independent parent",
        )
        for record in checks:
            grades(record["checks"], list(range(1, 12)))
            need(
                record["unused_grades"] == [10, 11], "Unused parent count grades differ"
            )


def evaluate(poly, t):
    return sum(x * t**j for j, x in enumerate(poly))


def verify_examples(data):
    validate_examples(data)
    for row in data["families"]:
        poly = (
            capped_polynomial(row["w"], row["c"], row["d"])
            if row["kind"] == "cap"
            else transport_polynomial(row["rows"], row["columns"])
        )
        need(
            list(map(str, poly)) == row["coefficients"],
            "Whole coefficient vector differs",
        )
        for site in [*row["count_sites"], *row["literal_LR"]]:
            need(
                evaluate(poly, site["t"]) == site["count"],
                "Independent saved count differs",
            )
    for row in data["directions"]:
        r, S = row["direction_dimension"], row["S"]
        parents = []
        direction = transport_polynomial(
            row["direction_rows"], row["direction_columns"]
        )
        need(
            list(map(str, direction)) == row["direction_polynomial"]
            and len(direction) == r + 1,
            "Whole direction polynomial or actual degree differs",
        )
        for u in range(r + 3):
            rr = [
                b + (S + u) * a for b, a in zip(row["base_rows"], row["direction_rows"])
            ]
            cc = [
                b + (S + u) * a
                for b, a in zip(row["base_columns"], row["direction_columns"])
            ]
            parents.append(transport_polynomial(rr, cc))
        need(
            [list(map(str, p)) for p in parents] == row["parents"],
            "Complete parent vectors differ",
        )
        for record in row["independent_parent_counts"]:
            for site in record["checks"]:
                need(
                    evaluate(parents[record["u"]], site["t"]) == site["count"],
                    "Independent whole-direction count differs",
                )
        for _ in range(r):
            need(
                all(len(p) == 9 for p in parents),
                "Incomplete eight-degree parent vector",
            )
            parents = [
                tuple(y - x for x, y in zip(a, b)) for a, b in zip(parents, parents[1:])
            ]
        need(
            all(p == parents[0] for p in parents) and not any(parents[0][:r]),
            "Whole finite-difference identity differs",
        )
        quotient = [
            str(x / (math.factorial(r) * direction[-1])) for x in parents[0][r:]
        ]
        need(quotient == row["quotient_polynomial"], "Whole quotient differs")
        need(
            row["all_quotient_coefficients_positive"] is True
            and all(F(x) > 0 for x in quotient),
            "Quotient sign record differs",
        )
    return {"families": len(FAMILIES), "directions": len(DIRECTIONS)}


def main():
    data = json.loads((HERE / "examples.json").read_text(), object_pairs_hook=unique)
    result = verify_examples(data)
    print(
        "PASS_COMPLETE_EXAMPLE_VECTORS",
        result["families"],
        "STABILIZED_DIRECTIONS",
        result["directions"],
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, IndexError) as error:
        print("REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
