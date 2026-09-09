"""Independent small-fiber controls and complete certificate refusal cases."""

from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import unittest

from slr_ehrhart.flow_support import (
    flow_support_certificate,
    verify_flow_support_certificate,
)


def integer_points(edges, totals):
    # Every interval is nonempty, so each coordinate is bounded by max(totals).
    bound = max((0,) + tuple(totals))
    return [point for point in product(range(bound + 1), repeat=len(edges))
            if tuple(sum(point[e] for e, (u, v) in enumerate(edges) if u <= i < v)
                     for i in range(len(totals))) == tuple(totals)]


def rational_rank(rows):
    # Eliminate differences of enumerated points, independently of graph rank
    # and of the producer/verifier's interval-column elimination.
    matrix = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for i in range(rank + 1, len(matrix)):
            multiplier = matrix[i][column]
            matrix[i] = [a - multiplier * b for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


def replaced(certificate, path, value):
    result = deepcopy(certificate)
    target = result
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return result


def integer_paths(value, prefix=()):
    if type(value) is int:
        yield prefix
    elif type(value) is list:
        for i, child in enumerate(value):
            yield from integer_paths(child, prefix + (i,))
    elif type(value) is dict:
        for key, child in value.items():
            yield from integer_paths(child, prefix + (key,))


class FlowSupportTests(unittest.TestCase):
    def test_all_small_edge_sets_totals_and_affine_dimensions(self):
        for n in range(4):
            all_edges = [(u, v) for u in range(n + 1) for v in range(u + 1, n + 1)]
            for mask in range(1 << len(all_edges)):
                edges = [edge for e, edge in enumerate(all_edges) if mask & (1 << e)]
                for totals in product(range(3), repeat=n):
                    with self.subTest(n=n, edges=edges, totals=totals):
                        points = integer_points(edges, totals)
                        certificate = flow_support_certificate(edges, totals)
                        self.assertEqual(certificate["feasible"], bool(points))
                        self.assertIs(verify_flow_support_certificate(edges, totals, certificate), True)
                        if not points:
                            self.assertNotIn("degree", certificate)
                            self.assertNotIn("dimension", certificate)
                            continue
                        active = [e for e in range(len(edges)) if any(point[e] for point in points)]
                        differences = [[a - b for a, b in zip(point, points[0])]
                                       for point in points[1:]]
                        dimension = rational_rank(differences)
                        self.assertEqual(certificate["active"], active)
                        self.assertIn(tuple(certificate["flow"]), points)
                        self.assertEqual(certificate["dimension"], dimension)
                        self.assertEqual(certificate["degree"], dimension)
                        self.assertEqual(certificate["rank"], len(active) - dimension)
                        self.assertEqual(set(certificate["forced_zero_cuts"]),
                                         {str(e) for e in range(len(edges)) if e not in active})

    def test_zero_and_empty_systems(self):
        for edges, totals in [([], []), ([], [0, 0]),
                              ([(0, 1), (0, 2), (1, 2)], [0, 0])]:
            with self.subTest(edges=edges, totals=totals):
                certificate = flow_support_certificate(edges, totals)
                self.assertTrue(certificate["feasible"])
                self.assertEqual(certificate["flow"], [0] * len(edges))
                self.assertEqual(certificate["active"], [])
                self.assertEqual(certificate["positive_cycles"], {})
                self.assertEqual(certificate["components"], len(totals) + 1)
                self.assertEqual((certificate["rank"], certificate["dimension"],
                                  certificate["degree"]), (0, 0, 0))

    def test_disconnected_support_forced_zero_and_isolated_vertex(self):
        edges = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 5)]
        certificate = flow_support_certificate(edges, [1, 1, 0, 2, 2, 0])
        self.assertEqual(certificate["active"], list(range(6)))
        self.assertEqual(set(certificate["forced_zero_cuts"]), {"6"})
        self.assertEqual((certificate["vertices_including_isolates"],
                          certificate["components"], certificate["rank"],
                          certificate["dimension"]), (7, 3, 4, 2))

    def test_positive_cycles_give_actual_integer_points(self):
        edges = [(0, 1), (0, 2), (1, 2)]
        totals = [1, 1]
        certificate = flow_support_certificate(edges, totals)
        self.assertEqual(certificate["flow"], [0, 1, 0])
        self.assertEqual(set(certificate["positive_cycles"]), {"0", "2"})
        points = integer_points(edges, totals)
        identities = {edge: e for e, edge in enumerate(edges)}
        for key, path in certificate["positive_cycles"].items():
            point = list(certificate["flow"])
            point[int(key)] += 1
            for u, v in zip(path, path[1:]):
                if (u, v) in identities:
                    point[identities[(u, v)]] += 1
                else:
                    point[identities[(v, u)]] -= 1
            self.assertGreater(point[int(key)], 0)
            self.assertIn(tuple(point), points)

    def test_infeasible_cuts_for_missing_edges_mismatched_and_negative_totals(self):
        for edges, totals in [([], [1, 1]), ([(0, 2)], [1, 2]),
                              ([(0, 1), (0, 2), (1, 2)], [-1, -1]),
                              ([(0, 1), (0, 2), (1, 2)], [0, -1])]:
            with self.subTest(edges=edges, totals=totals):
                certificate = flow_support_certificate(edges, totals)
                self.assertFalse(certificate["feasible"])
                self.assertEqual(integer_points(edges, totals), [])
                self.assertLess(certificate["cut_capacity"], certificate["supply"])
                self.assertIs(verify_flow_support_certificate(edges, totals, certificate), True)

    def test_reordered_edges_preserve_labeled_witnesses(self):
        edges = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 5)]
        totals = [1, 1, 0, 2, 2, 0]
        original = flow_support_certificate(edges, totals)
        reordered = edges[::-1]
        other = flow_support_certificate(reordered, totals)

        def labeled(certificate):
            return {tuple(edge): (certificate["flow"][e], e in certificate["active"],
                                  certificate["positive_cycles"].get(str(e)),
                                  certificate["forced_zero_cuts"].get(str(e)))
                    for e, edge in enumerate(certificate["interval_edges"])}

        self.assertEqual(labeled(original), labeled(other))
        for key in ("components", "rank", "dimension", "degree"):
            self.assertEqual(original[key], other[key])
        with self.assertRaises(ValueError):
            verify_flow_support_certificate(reordered, totals, original)

    def test_deterministic_json_round_trip_huge_ints_and_input_copies(self):
        edges = [[0, 1], [0, 2], [1, 2]]
        totals = [10**60, 10**60]
        saved_edges, saved_totals = deepcopy(edges), list(totals)
        certificate = flow_support_certificate(edges, totals)
        self.assertEqual(certificate, flow_support_certificate(edges, totals))
        self.assertEqual(certificate["dimension"], 1)
        decoded = json.loads(json.dumps(certificate))
        snapshot = deepcopy(decoded)
        self.assertIs(verify_flow_support_certificate(edges, totals, decoded), True)
        self.assertEqual(decoded, snapshot)
        self.assertEqual((edges, totals), (saved_edges, saved_totals))
        certificate["interval_edges"][0][0] = 99
        certificate["totals"][0] = 99
        self.assertEqual((edges, totals), (saved_edges, saved_totals))
        edges[0][0] = 98
        totals[0] = 98
        self.assertEqual((decoded["interval_edges"], decoded["totals"]),
                         (saved_edges, saved_totals))

    def test_invalid_inputs_refused_before_degenerate_shortcuts(self):
        class IntSubclass(int):
            pass

        for bad in [True, False, 1.0, "1", Fraction(1), None, IntSubclass(1)]:
            for edges, totals in [([], [bad]), ([(bad, 1)], [0]), ([(0, bad)], [0])]:
                with self.subTest(edges=edges, totals=totals), self.assertRaises(ValueError):
                    flow_support_certificate(edges, totals)
        for edges, totals in [(None, []), ({}, []), ("", []), ([], None), ([], ""),
                              ([], {}), ([(0, 1)], []), ([(0, 0)], [0]),
                              ([(-1, 1)], [0]), ([(0, 2)], [0]), ([(1, 0)], [0]),
                              ([(0,)], [0]), ([(0, 1, 2)], [0]), ([0], [0]),
                              ([(0, 1), [0, 1]], [0])]:
            with self.subTest(edges=edges, totals=totals), self.assertRaises(ValueError):
                flow_support_certificate(edges, totals)

    def test_every_numeric_certificate_slot_rejects_bool_and_coercion(self):
        cases = [([(0, 1), (0, 2), (1, 2), (0, 3)], [1, 1, 0]), ([], [1, 1])]
        for edges, totals in cases:
            certificate = flow_support_certificate(edges, totals)
            for path in integer_paths(certificate):
                value = certificate
                for key in path:
                    value = value[key]
                for bad in (bool(value), float(value), Fraction(value), str(value)):
                    with self.subTest(path=path, bad=bad), self.assertRaises(ValueError):
                        verify_flow_support_certificate(edges, totals, replaced(certificate, path, bad))

    def test_missing_unexpected_fields_and_non_json_containers_refuse(self):
        for edges, totals in [([(0, 1), (0, 2), (1, 2)], [1, 1]), ([], [1, 1])]:
            certificate = flow_support_certificate(edges, totals)
            for key in certificate:
                broken = deepcopy(certificate)
                del broken[key]
                with self.subTest(missing=key), self.assertRaises(ValueError):
                    verify_flow_support_certificate(edges, totals, broken)
            broken_cases = [None, [], True, {**certificate, "unverified_claim": 1},
                            {**certificate, "feasible": 1},
                            {**certificate, "feasible": "false"},
                            {**certificate, "totals": tuple(totals)}]
            if edges:
                broken_cases.append({**certificate, "interval_edges": [tuple(edge) for edge in edges]})
            for broken in broken_cases:
                with self.subTest(broken=broken), self.assertRaises(ValueError):
                    verify_flow_support_certificate(edges, totals, broken)

    def test_complete_original_identity_and_witness_partition_required(self):
        edges = [(0, 1), (0, 2), (1, 2), (0, 3)]
        totals = [1, 1, 0]
        certificate = flow_support_certificate(edges, totals)
        changes = [(("interval_edges",), certificate["interval_edges"][:-1]),
                   (("interval_edges", 1), [0, 1]),
                   (("flow",), certificate["flow"][:-1]),
                   (("flow", 0), 1),
                   (("active",), certificate["active"] + [certificate["active"][0]]),
                   (("active",), [-1]), (("active",), [len(edges)]),
                   (("active",), certificate["active"][:-1]),
                   (("positive_cycles",), {}),
                   (("positive_cycles",), {0: certificate["positive_cycles"]["0"],
                                            "2": certificate["positive_cycles"]["2"]}),
                   (("positive_cycles",), {"00": certificate["positive_cycles"]["0"],
                                            "2": certificate["positive_cycles"]["2"]}),
                   (("forced_zero_cuts",), {}),
                   (("forced_zero_cuts",), {**certificate["forced_zero_cuts"], "0": [1]}),
                   (("totals",), [2, 2, 0]), (("b", 0), 2)]
        for path, value in changes:
            with self.subTest(path=path, value=value), self.assertRaises(ValueError):
                verify_flow_support_certificate(edges, totals, replaced(certificate, path, value))
        with self.assertRaises(ValueError):
            verify_flow_support_certificate(edges + [edges[0]], totals, certificate)

    def test_tampered_paths_cuts_and_false_active_or_forced_claims_refuse(self):
        edges = [(0, 1), (0, 2), (1, 2), (0, 3)]
        totals = [1, 1, 0]
        certificate = flow_support_certificate(edges, totals)
        changes = [(("positive_cycles", "0"), []),
                   (("positive_cycles", "0"), [1, 0]),
                   (("positive_cycles", "0"), [1, 2, 0, 0]),
                   (("positive_cycles", "0"), [0, 2, 1]),
                   (("positive_cycles", "0"), [1, 4, 0]),
                   (("forced_zero_cuts", "3"), []),
                   (("forced_zero_cuts", "3"), [3, 3]),
                   (("forced_zero_cuts", "3"), [0, 3]),
                   (("forced_zero_cuts", "3"), [3, 4])]
        for path, value in changes:
            with self.subTest(path=path, value=value), self.assertRaises(ValueError):
                verify_flow_support_certificate(edges, totals, replaced(certificate, path, value))
        false_forced = deepcopy(certificate)
        false_forced["active"].remove(0)
        del false_forced["positive_cycles"]["0"]
        false_forced["forced_zero_cuts"]["0"] = [1]
        with self.assertRaises(ValueError):
            verify_flow_support_certificate(edges, totals, false_forced)
        false_active = deepcopy(certificate)
        false_active["active"].append(3)
        del false_active["forced_zero_cuts"]["3"]
        false_active["positive_cycles"]["3"] = [3, 0]
        with self.assertRaises(ValueError):
            verify_flow_support_certificate(edges, totals, false_active)

    def test_rank_components_dimension_and_degree_are_checked(self):
        edges, totals = [(0, 1), (0, 2), (1, 2)], [1, 1, 0]
        certificate = flow_support_certificate(edges, totals)
        for key in ("vertices_including_isolates", "components", "rank", "dimension", "degree"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_flow_support_certificate(edges, totals,
                                                {**certificate, key: certificate[key] + 1})

    def test_infeasible_witness_must_be_a_strict_source_sink_cut(self):
        edges, totals = [], [1]
        certificate = flow_support_certificate(edges, totals)
        for path, value in [(("cut",), []), (("cut",), [0]), (("cut",), [0, 2, 3]),
                            (("cut",), [0, 2, 2]), (("cut",), [0, 2, 4]),
                            (("cut_capacity",), 1), (("supply",), 2)]:
            with self.subTest(path=path, value=value), self.assertRaises(ValueError):
                verify_flow_support_certificate(edges, totals, replaced(certificate, path, value))
        # The source-only cut has capacity exactly the supply, so it is no proof.
        broken = {**certificate, "cut": [2], "cut_capacity": 1}
        with self.assertRaises(ValueError):
            verify_flow_support_certificate(edges, totals, broken)
        # Adding the missing original interval makes the old cut invalid.
        broken = {**certificate, "interval_edges": [[0, 1]]}
        with self.assertRaises(ValueError):
            verify_flow_support_certificate([(0, 1)], totals, broken)


if __name__ == "__main__":
    unittest.main()
