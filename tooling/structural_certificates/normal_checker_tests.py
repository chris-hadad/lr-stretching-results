"""Small self-authored fixtures; no returned scientific data is read or run."""

from __future__ import annotations

import copy
import gzip
import importlib.util
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import random
import sys
import tempfile
import unittest


spec = importlib.util.spec_from_file_location("normal_checker", Path(__file__).with_name("verify_normal_certificates.py"))
c = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = c
spec.loader.exec_module(c)


def one_ray_trace():
    return {"alpha": "1/2", "tangent_rays": [[1]], "metric": [["1"]], "generic_covector": ["1"],
            "faces": [{"face": [], "quotient_basis": [[1]], "quotient_metric": [["1"]],
                       "projected_rays": [[1]], "covector": ["1"], "fundamental_points": [[0]],
                       "S_series": {"-1": "-1", "0": "1/2"}, "mu_series": {"-1": "0", "0": "1/2"},
                       "face_subtractions": [{"local_face": [0], "global_face": [0], "index": 1,
                                              "integral_prefactor": "-1"}]}]}


def orthant_trace():
    faces = []
    for face, basis, value in (([0], [[0], [1]], c.Q(2)), ([1], [[1], [0]], c.Q(1))):
        faces.append({"face": face, "quotient_basis": basis, "quotient_metric": [["1"]],
                      "projected_rays": [[1]], "covector": [str(value)], "fundamental_points": [[0]],
                      "S_series": {"-1": str(-1/value), "0": "1/2", "1": str(-value/12)},
                      "mu_series": {"-1": "0", "0": "1/2", "1": str(-value/12)},
                      "face_subtractions": [{"local_face": [0], "global_face": [0, 1], "index": 1,
                                             "integral_prefactor": str(-1/value)}]})
    faces.append({"face": [], "quotient_basis": [[1, 0], [0, 1]], "quotient_metric": [["1", "0"], ["0", "1"]],
                  "projected_rays": [[1, 0], [0, 1]], "covector": ["1", "2"], "fundamental_points": [[0, 0]],
                  "S_series": {"-2": "1/2", "-1": "-3/4", "0": "11/24"},
                  "mu_series": {"-2": "0", "-1": "0", "0": "1/4"},
                  "face_subtractions": [{"local_face": [0], "global_face": [0], "index": 1, "integral_prefactor": "-1"},
                                         {"local_face": [1], "global_face": [1], "index": 1, "integral_prefactor": "-1/2"},
                                         {"local_face": [0, 1], "global_face": [0, 1], "index": 1, "integral_prefactor": "1/2"}]})
    return {"alpha": "1/4", "tangent_rays": [[1, 0], [0, 1]], "metric": [["1", "0"], ["0", "1"]],
            "generic_covector": ["1", "2"], "faces": faces}


def fixture_type():
    return {"key": [1, "g", [[1]]], "representative": [[1]], "index": 1, "alpha": "1/2", "trace": one_ray_trace()}


def index_two_type():
    # Hand-derived two-dimensional cone: primitive rays (1,0),(1,2),
    # fundamental points (0,0),(1,1), and BV constant 3/10.
    trace = orthant_trace()
    trace.update(alpha="3/10", tangent_rays=[[1,0],[1,2]], generic_covector=["1","1"])
    trace["faces"][0].update(covector=["1"],
        S_series={"-1":"-1","0":"1/2","1":"-1/12"},
        mu_series={"-1":"0","0":"1/2","1":"-1/12"})
    trace["faces"][0]["face_subtractions"][0]["integral_prefactor"] = "-1"
    trace["faces"][1].update(quotient_basis=[[2],[-1]], quotient_metric=[["1/5"]], covector=["1/5"],
        S_series={"-1":"-5","0":"1/2","1":"-1/60"},
        mu_series={"-1":"0","0":"1/2","1":"-1/60"})
    trace["faces"][1]["face_subtractions"][0]["integral_prefactor"] = "-5"
    empty = trace["faces"][2]
    empty.update(projected_rays=[[1,0],[1,2]], covector=["1","1"], fundamental_points=[[0,0],[1,1]],
        S_series={"-2":"2/3","-1":"-2/3","0":"7/18"},
        mu_series={"-2":"0","-1":"0","0":"3/10"})
    empty["face_subtractions"][1]["integral_prefactor"] = "-1/3"
    empty["face_subtractions"][2].update(index=2, integral_prefactor="2/3")
    return {"key":[2,"s",[[2,-1],[0,1]]], "representative":[[2,-1],[0,1]],
            "index":2, "alpha":"3/10", "trace":trace}


def write_json(root, name, value):
    path = Path(root) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(value).encode()
    path.write_bytes(gzip.compress(body) if name.endswith(".gz") else body)


def write_roster(root):
    path = "DATA/A02/A-R3-Q1.json.gz"
    points, normals, _ = c.atlas(3)
    records = [{"ids": [i], "index": 1, "raw": "1/2", "corrected": "1/2", "events": [],
                "type_source": "fixture_type.json"} for i in range(len(normals))]
    data = {"rank": 3, "gate": "A", "points": points, "normals": normals,
            "supports": [], "records": records, "dependent": []}
    write_json(root, path, data)
    write_json(root, "fixture_type.json", fixture_type())
    return path, data, {"path": path, "gate": "A", "rank": 3, "q": 1, "records": 2, "dependent": 0}


class ExactLatticeTests(unittest.TestCase):
    def test_integer_column_reduction_matches_all_minors(self):
        rng = random.Random(9471)
        for q in range(1, 5):
            for width in range(q, q+3):
                for _ in range(20):
                    rows = tuple(tuple(rng.randrange(-3, 4) for _ in range(width)) for _ in range(q))
                    expected = 0
                    for cols in combinations(range(width), q):
                        minor = tuple(tuple(row[j] for j in cols) for row in rows)
                        expected = gcd(expected, int(c.determinant(minor)))
                    self.assertEqual(c.lattice_index(rows), expected, rows)

    def test_saturated_kernel_and_primitive_divisor(self):
        for rows, divisor in [(((1,0,0,0),(0,1,0,0),(0,0,1,1),(0,0,1,-1)), 2),
                              (((1,0,0,0),(0,1,0,0),(0,0,2,0),(0,0,1,3)), 3)]:
            self.assertEqual(c.primitive_divisor(c.normalized_columns(rows), (0,1,2)), divisor)
            _, transform = c.column_reduce(rows[:3], track=True)
            kernel = tuple((row[3],) for row in transform)
            self.assertEqual(c.matmul(rows[:3], kernel), ((0,), (0,), (0,)))
            self.assertEqual(c.lattice_index(c.transpose(kernel)), 1)
            self.assertEqual(abs(c.determinant(transform)), 1)

    def test_singular_matrix_and_fractional_primitive(self):
        self.assertEqual(c.lattice_index(((1,2),(2,4))), 0)
        with self.assertRaises(c.CheckError):
            c.inverse(((1,2),(2,4)))
        self.assertEqual(c.primitive((c.Q(-1,2), c.Q(3,4))), (-2,3))

    def test_half_open_complete_roster(self):
        rays = ((1,0),(1,2))
        self.assertEqual(c.check_fundamental_points(rays, [[0,0],[1,1]]), [(0,0),(1,1)])
        for wrong in ([[0,0]], [[0,0],[0,0]], [[0,0],[2,2]]):
            with self.assertRaises(c.CheckError):
                c.check_fundamental_points(rays, wrong)


class GeometryTests(unittest.TestCase):
    def test_first_hive(self):
        points, normals, full = c.atlas(3)
        self.assertEqual(points, ((1,1),))
        self.assertEqual(normals, ((-1,), (1,)))
        self.assertTrue(all(len(row) == 4 for choices in full.values() for row in choices))

    def test_nonzero_support_graph_not_gram_graph(self):
        normals = ((1,1,0), (1,-1,0), (0,0,1))
        self.assertEqual(c.connected_tuples(normals, 2, c.Deadline()), {(0,1)})

    def test_frontier_enumerator_matches_brute_force(self):
        _, normals, _ = c.atlas(4)
        support = [{j for j, x in enumerate(row) if x} for row in normals]
        for q in range(1,5):
            expected = set()
            for ids in combinations(range(len(normals)), q):
                seen = {ids[0]}
                while True:
                    added = {i for i in ids if any(support[i] & support[j] for j in seen)} - seen
                    if not added:
                        break
                    seen.update(added)
                if seen == set(ids):
                    expected.add(ids)
            self.assertEqual(c.connected_tuples(normals, q, c.Deadline()), expected)


class TraceTests(unittest.TestCase):
    def test_one_and_two_dimensional_constants(self):
        self.assertEqual(c.verify_trace(one_ray_trace(), c.Deadline())["alpha"], "1/2")
        self.assertEqual(c.verify_trace(orthant_trace(), c.Deadline())["alpha"], "1/4")
        self.assertEqual(c.verify_type(fixture_type(), c.Deadline())["alpha"], "1/2")
        self.assertEqual(c.verify_type(index_two_type(), c.Deadline())["alpha"], "3/10")

    def test_formal_exponential_reciprocal(self):
        self.assertEqual(c.exponential_denominator(c.Q(3), 4),
                         [c.Q(-1,3), c.Q(1,2), c.Q(-1,4), c.Q(0), c.Q(3,80)])

    def test_trace_negative_fixtures(self):
        mutations = [lambda t: t["faces"].pop(), lambda t: t["faces"].append(copy.deepcopy(t["faces"][0])),
                     lambda t: t["faces"][0]["fundamental_points"].append([0]),
                     lambda t: t["faces"][0]["mu_series"].update({"0": "7/12"}),
                     lambda t: t["faces"][0]["S_series"].update({"-1": "0"}),
                     lambda t: t["faces"][0]["face_subtractions"].clear(),
                     lambda t: t["faces"][0].update({"quotient_basis": [[2]]}),
                     lambda t: t.update({"metric": [["2"]]}),
                     lambda t: t.update({"alpha": "0.5"})]
        for mutate in mutations[:-1]:
            trace = one_ray_trace()
            mutate(trace)
            with self.assertRaises(c.CheckError):
                c.verify_trace(trace, c.Deadline())
        # A decimal string remains exact; an actual JSON float is rejected at
        # mathematical fields, while timing metadata may contain floats.
        trace = one_ray_trace()
        trace["alpha"] = 0.5
        with self.assertRaises(c.CheckError):
            c.verify_trace(trace, c.Deadline())

    def test_embedding_changes_fail(self):
        record = fixture_type()
        record["trace"]["metric"] = [["2"]]
        with self.assertRaises(c.CheckError):
            c.verify_type(record, c.Deadline())
        signed = index_two_type()
        signed.update(representative=[[4,-1],[0,1]], index=4)
        signed["key"][2] = [[4,-1],[0,1]]
        with self.assertRaisesRegex(c.CheckError, "not saturated"):
            c.verify_type(signed, c.Deadline())


class RosterTests(unittest.TestCase):
    def test_frozen_roster_is_exact_not_count_only(self):
        self.assertEqual(len(c.EXPECTED), 34)
        self.assertEqual(c.EXPECTED["DATA/A02/A-R3-Q0.json.gz"], ("A",3,3))
        self.assertEqual(c.EXPECTED["DATA/C-R5-Q0.json.gz"], ("C",5,4))

    def test_valid_and_partial_file_checks(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            path, _, spec = write_roster(root)
            out = {}
            c.check_file(c.Inputs(root), spec, 0, None, c.Deadline(), out)
            self.assertEqual(out["status"], "FILE_ARITHMETIC_PASS")
            self.assertEqual(out["independent"], 2)
            partial = {}
            c.check_file(c.Inputs(root), spec, 1, 1, c.Deadline(), partial)
            self.assertEqual(partial["status"], "PARTIAL")
            self.assertEqual((partial["start"], partial["stop"]), (1,2))

    def test_omitted_duplicate_wrong_class_and_changed_normal(self):
        mutations = [lambda d: d["records"].pop(),
                     lambda d: d["records"].append(copy.deepcopy(d["records"][0])),
                     lambda d: d["dependent"].append(d["records"].pop()["ids"]),
                     lambda d: d["normals"][0].__setitem__(0, 2),
                     lambda d: d["records"][0].update({"corrected": "1/3"}),
                     lambda d: d["records"][0].update({"events": [[[0], 1, "1", "0", 0]]})]
        for mutate in mutations:
            with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
                path, data, spec = write_roster(root)
                data = json.loads(json.dumps(data))
                mutate(data)
                write_json(root, path, data)
                if data["dependent"]:
                    spec = {**spec, "records": 1, "dependent": 1}
                with self.assertRaises(c.CheckError):
                    c.check_file(c.Inputs(root), spec, 0, None, c.Deadline(), {})

    def test_source_drift_duplicate_json_and_path_escape(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            write_json(root, "value.json", {"value": 1})
            inputs = c.Inputs(root)
            inputs.read("value.json")
            bound = c.Inputs(root, dict(inputs.reads))
            write_json(root, "value.json", {"value": 2})
            with self.assertRaisesRegex(c.CheckError, "Changed source"):
                bound.read("value.json")
            with self.assertRaises(c.CheckError):
                inputs.read("../outside.json")
        with self.assertRaises(c.CheckError):
            c.decode('{"a":1,"a":2}')

    def test_manifest_rejects_missing_or_replaced_identity(self):
        files = [{"path": path, "gate": gate, "rank": n, "q": q, "records": 0, "dependent": 0}
                 for path, (gate,n,q) in c.EXPECTED.items()]
        required = set(c.EXPECTED) | {c.SEALED, c.PATCH_SYSTEM, c.PATCH_VECTORS, c.EXCEPTIONS}
        manifest = {"schema": c.SCHEMA, "kind": "manifest", "files": files, "type_paths": [],
                    "inputs": {p: {"sha256": "fixture", "bytes": 0} for p in required}}
        c.validate_manifest(manifest)
        for replace in (False, True):
            wrong = copy.deepcopy(manifest)
            if replace:
                wrong["files"][0] = copy.deepcopy(wrong["files"][1])
            else:
                wrong["files"].pop()
            with self.assertRaises(c.CheckError):
                c.validate_manifest(wrong)

    def test_freeze_complete_source_closure_and_omitted_sealed_file(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            checks = []
            for path, (gate, n, q) in c.EXPECTED.items():
                write_json(root, path, {"gate":gate, "rank":n, "records":[], "dependent":[]})
                checks.append({"path":path, "gate":gate, "rank":n, "q":q})
            write_json(root, c.SEALED, {"checks":checks, "elapsed_seconds":0.125})
            for path in (c.PATCH_SYSTEM, c.PATCH_VECTORS, c.EXCEPTIONS):
                write_json(root, path, {})
            frozen = c.freeze(root, c.Deadline())
            c.validate_manifest(frozen)
            self.assertEqual(frozen["status"], "FROZEN_INPUTS_ONLY")
            self.assertEqual(set(frozen["inputs"]), set(c.EXPECTED) | {c.SEALED,c.PATCH_SYSTEM,c.PATCH_VECTORS,c.EXCEPTIONS})
            write_json(root, c.SEALED, {"checks":checks[:-1]})
            with self.assertRaisesRegex(c.CheckError, "file identities"):
                c.freeze(root, c.Deadline())


class AggregateTests(unittest.TestCase):
    def run_fixture(self, root, slices):
        path, _, spec = write_roster(root)
        inputs = c.Inputs(root)
        inputs.read(path)
        inputs.read("fixture_type.json")
        manifest = {"files":[spec], "type_paths":["fixture_type.json"], "inputs":dict(inputs.reads)}
        reports = []
        for index, (start, limit) in enumerate(slices):
            reader = c.Inputs(root, manifest["inputs"])
            report = {"schema":c.SCHEMA, "kind":"file", "file":path,
                      "manifest_sha256":"fixture_manifest", "checker_sha256":"fixture_code"}
            c.check_file(reader, spec, start, limit, c.Deadline(), report)
            report["read_inputs"] = reader.reads
            filename = f"normal_report_{index}.json"
            write_json(root, filename, report)
            reports.append(str(Path(root)/filename))
        return manifest, reports

    def test_missing_and_disjoint_slice_identity_coverage(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            manifest, reports = self.run_fixture(root, [(0,1),(1,1)])
            partial = {}
            c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, reports[:1], "fixture_manifest", "fixture_code", c.Deadline(), partial)
            self.assertFalse(partial["files"][0]["complete"])
            self.assertEqual(partial["files"][0]["missing_intervals"], [[1,2]])
            joined = {}
            c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, reports, "fixture_manifest", "fixture_code", c.Deadline(), joined)
            self.assertTrue(joined["files"][0]["complete"])
            self.assertEqual(joined["status"], "PARTIAL")
            self.assertEqual(joined["missing_type_paths"], ["fixture_type.json"])

    def test_duplicate_retry_overlap_and_changed_receipt(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            manifest, reports = self.run_fixture(root, [(0,1),(0,2)])
            for chosen in ([reports[0],reports[0]], reports):
                with self.assertRaises(c.CheckError):
                    c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, chosen,
                                "fixture_manifest", "fixture_code", c.Deadline(), {})
            bad = json.loads(Path(reports[0]).read_text())
            bad["checked_ids_sha256"] = "wrong"
            write_json(root, "normal_bad.json", bad)
            with self.assertRaisesRegex(c.CheckError, "identity digest"):
                c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, [str(Path(root)/"normal_bad.json")],
                            "fixture_manifest", "fixture_code", c.Deadline(), {})

    def test_stale_checker_and_changed_source(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            manifest, reports = self.run_fixture(root, [(0,None)])
            with self.assertRaisesRegex(c.CheckError, "another manifest/checker"):
                c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, reports,
                            "fixture_manifest", "other_code", c.Deadline(), {})
            write_json(root, "fixture_type.json", {"changed":True})
            with self.assertRaisesRegex(c.CheckError, "Changed source"):
                c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, reports,
                            "fixture_manifest", "fixture_code", c.Deadline(), {})

    def test_type_reports_are_bound_and_not_count_only(self):
        with tempfile.TemporaryDirectory(prefix="normal_fixture_") as root:
            manifest, reports = self.run_fixture(root, [(0,None)])
            inputs = c.Inputs(root, manifest["inputs"])
            report = {"schema":c.SCHEMA, "kind":"types", "manifest_sha256":"fixture_manifest",
                      "checker_sha256":"fixture_code"}
            c.check_types(inputs, manifest["type_paths"], 0, None, c.Deadline(), report)
            report["read_inputs"] = inputs.reads
            filename = str(Path(root)/"normal_types.json")
            write_json(root, "normal_types.json", report)
            combined = {}
            c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, [*reports,filename],
                        "fixture_manifest", "fixture_code", c.Deadline(), combined)
            self.assertEqual(combined["missing_type_paths"], [])
            self.assertEqual(combined["status"], "PARTIAL")  # Exception gate remains absent.
            report["checked"][0]["alpha"] = "0"
            write_json(root, "normal_types.json", report)
            with self.assertRaisesRegex(c.CheckError, "metadata/value"):
                c.aggregate(c.Inputs(root,manifest["inputs"]), manifest, [*reports,filename],
                            "fixture_manifest", "fixture_code", c.Deadline(), {})


if __name__ == "__main__":
    unittest.main()
