"""Only tiny synthetic/degenerate models and interface controls."""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys
import unittest

import slr_ehrhart as api

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("h_system_control", HERE / "cpp" / "control.py")
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)

def response(identity="a", status="complete", count="4"):
    return {"id": identity, "status": status, "count": count, "visited_states": 1,
            "row_work": 2, "memo_hits": 0, "elapsed_seconds": 0.001}

class CurrentContractTests(unittest.TestCase):
    def test_public_exports_and_import_closure(self):
        names = {"rank6_split_parameters", "rank6_split_count", "rank6_split_polynomial",
                 "rank8_clipped_boundary", "rank8_clipped_count", "rank8_clipped_polynomial",
                 "two_width_count", "two_width_polynomial", "rectangular_matrix_invariant_count"}
        self.assertTrue(names <= set(api.__all__))
        self.assertEqual(len(api.__all__), len(set(api.__all__)))
        for name in api.__all__:
            self.assertTrue(hasattr(api, name), name)
        for forbidden in ("horn", "engines", "census", "census_native", "cli"):
            self.assertNotIn("slr_ehrhart." + forbidden, sys.modules)

    def test_two_width_literal_tiny_composition(self):
        # Explicitly list all u0+u1=t for two tiny gain vectors.
        for t in range(4):
            expected = sum((1 + u0) * (1 + 2*(t-u0)) for u0 in range(t+1))
            self.assertEqual(api.two_width_count((1, 0), (0, 2), dilation=t), expected)
            vector = api.two_width_polynomial((1, 0), (0, 2))
            self.assertEqual(sum(c*t**i for i, c in enumerate(vector)), expected)

    def test_two_width_degenerate_rectangle(self):
        self.assertEqual(api.two_width_polynomial((0,), (0,), total=0,
                         left_offset=2, right_offset=3), (Fraction(1), Fraction(5), Fraction(6)))
        self.assertEqual(api.two_width_count((0,), (0,), total=0,
                         left_offset=2, right_offset=3, dilation=2), 35)

    def test_two_width_strict_input_contract(self):
        for left, right in (([], []), ([1], [1, 2]), ([True], [1]), ("1", [1])):
            with self.assertRaises(ValueError):
                api.two_width_count(left, right, dilation=0)
        with self.assertRaises(ValueError):
            api.two_width_count([0], [0], dilation=Fraction(0))

    def test_split_empty_origin(self):
        self.assertEqual(api.rank6_split_parameters([], [], []), {"S": 0, "A": 0, "B": 0})
        self.assertEqual(api.rank6_split_polynomial([], [], []), (Fraction(1),))
        self.assertEqual(api.rank6_split_count([], [], [], 0), 1)

    def test_split_rejects_invalid_triple_before_zero(self):
        for triple in (([1], [], []), ([1, 2], [2, 1], []), ([True], [1], [])):
            with self.assertRaises(ValueError):
                api.rank6_split_count(*triple, 0)

    def test_clipped_empty_origin_and_outside_refusal(self):
        self.assertEqual(api.rank8_clipped_boundary(0, 0), ((), (), ()))
        self.assertEqual(api.rank8_clipped_polynomial(0, 0), (Fraction(1),))
        self.assertEqual(api.rank8_clipped_count(0, 0, 0), 1)
        for m, s in ((0, 1), (2, 1), (1, 3), (True, 1)):
            with self.assertRaises(ValueError):
                api.rank8_clipped_count(m, s, 0)

    def test_matrix_elementary_cases_and_validation(self):
        self.assertEqual(api.rectangular_matrix_invariant_count(2, 3, 1, 1), 0)
        self.assertEqual(api.rectangular_matrix_invariant_count(2, 3, 2, 0), 1)
        self.assertEqual(api.matrix_invariant_count(1, 2, 2), 3)
        for bad in (True, 1.0, Fraction(1), "1"):
            with self.assertRaises(ValueError):
                api.rectangular_matrix_invariant_count(bad, 3, 1, 0)

    def test_matrix_work_refusal_has_no_partial_value(self):
        # Zero admitted transitions: no table enumeration or scalar calculation.
        with self.assertRaises(api.MatrixCountLimitError) as caught:
            api.rectangular_matrix_invariant_count(2, 3, 2, 1, max_transitions=0)
        self.assertEqual(caught.exception.resource, "transitions")
        self.assertEqual(caught.exception.statistics["transitions"], 0)
        self.assertFalse(hasattr(caught.exception, "count"))
        self.assertFalse(hasattr(caught.exception, "value"))

    def test_cpp_request_preserves_every_mixed_row(self):
        self.assertEqual(control.request("tiny", [(0, 2), (0, 2)], [[2, -1, -1]],
                         max_states=5, milliseconds=7),
                         "RECOUNT1 tiny 2 1 5 7\n0 2\n0 2\n2 -1 -1\n")
        for args in (("bad id", [(0, 1)], [[0, 1]]),
                     ("a", [(0, 1)], [[0, 1, 0]]),
                     ("a", [(2, 1)], [[0, 1]]),
                     ("a", [(0, 1)], [[0, 2**63]])):
            with self.assertRaises(ValueError):
                control.request(*args)

    def test_cpp_complete_and_refusal_parsing(self):
        self.assertEqual(control.parse_responses(json.dumps(response()), ["a"])[0]["count"], "4")
        refused = response(status="REFUSED_WORK", count=None)
        self.assertEqual(control.parse_responses(json.dumps(refused), ["a"])[0]["count"], None)
        refused["count"] = "0"
        with self.assertRaises(ValueError):
            control.parse_responses(json.dumps(refused), ["a"])

    def test_cpp_missing_duplicate_altered_or_partial_output(self):
        for raw, ids in (("", ["a"]), (json.dumps(response()), ["a", "b"]),
                         (json.dumps(response()), ["b"]), (json.dumps(response()), ["a", "a"]),
                         (json.dumps(response(count=None)), ["a"]),
                         (json.dumps(response(status="partial")), ["a"])):
            with self.assertRaises(ValueError):
                control.parse_responses(raw, ids)

if __name__ == "__main__":
    unittest.main()

