#!/usr/bin/env python3
"""Extract unaccepted legacy vectors, then freeze complete ambient-hive jobs.

extract is administrative source parsing only: no geometry or evaluations.
index constructs real job systems and polynomial evaluations; root must run it
through the scientific harness. Neither command counts lattice points, imports
returned code, or executes historical commands. The consumer remains the exact
separately pinned recount_records.py, not this manifest's creator.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
import time


W = Path(__file__).resolve().parent
C = Path("/Volumes/SLR-Research/stretched-lr-research")
R = C / "results/raw/SLR-FRONTIER-026-RESTORED-20260911-001/namespaces"
SELECTION = W / "publication-staging/CHOSEN-TERMINALS.json"
FRE_MAP = W / "publication-staging/FRE-SELECTED-SOURCE-MAP.json"
OUTPUT_SOURCES = W / "publication-staging/LEGACY-VECTOR-SOURCES.json"
FRI_FINAL = C / "methods/fri-2026-09-09/science/results/FRI-BOX-CERTIFICATE-003.json"
FRI_AUDIT = C / "methods/fri-2026-09-09/science/results/FRI-BOX-SOURCE-AUDIT-001.json"
SCHEMA = "pro026-independent-hive-recount-v1"
VECTOR_SCHEMA = "legacy-adopted-source-vectors-v1"
EXPECTED_COUNTS = {"FRE": 185, "FRI-settled": 112}
CLASSICAL_PREMISES = [
    "The conventional full integral triangular hive with lambda outer counts the entire ordinary LR coefficient.",
    "For each original ambient hive coordinate, 0 <= h <= t*sum(lambda), by the complete nonnegative tableau-row interpretation.",
    "LR stretching is period one and has degree at most the ambient dimension D=(n-1)(n-2)/2; no old minimal affine dimension is used.",
    "Exact inner exchange and trailing zero padding preserve the whole LR polynomial when needed to bind an old source triple to the selected terminal.",
]


class SourceError(ValueError):
    pass


class DeadlineReached(Exception):
    pass


def need(condition, message):
    if not condition:
        raise SourceError(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, f"Duplicate source JSON field: {key}")
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs)


class Deadline:
    def __init__(self, seconds=100):
        need(0 < seconds <= 100, "Internal indexing cap must be at most 100 seconds")
        self.end = time.monotonic() + seconds

    def check(self):
        if time.monotonic() >= self.end:
            raise DeadlineReached("Indexing deadline reached; unindexed IDs remain explicit")


def file_pin(path, deadline=None):
    path = Path(path).resolve(strict=True)
    need(path.is_file(), f"Non-file input: {path}")
    before = path.stat()
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(1024**2), b""):
            if deadline:
                deadline.check()
            h.update(data)
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), "Input changed while hashing")
    return {"path": str(path), "bytes": before.st_size, "sha256": h.hexdigest()}


def load(path):
    return decode(Path(path).read_bytes())


def write_json(path, value):
    path = Path(path)
    need(not path.exists() and path.parent.is_dir(), "Fresh output with an existing parent is required")
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def pointer(document, expression):
    need(expression.startswith("/"), "JSON pointer must be absolute")
    for part in expression[1:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def trim(partition):
    need(isinstance(partition, (list, tuple)) and all(type(v) is int and v >= 0 for v in partition), "Invalid exact partition")
    need(all(a >= b for a, b in zip(partition, partition[1:])), "Partition is not decreasing")
    result = list(partition)
    while result and result[-1] == 0:
        result.pop()
    return result


def triple(value):
    if isinstance(value, dict):
        need(set(value) == {"lambda", "mu", "nu"}, "Unexpected triple fields")
        value = [value[k] for k in ("lambda", "mu", "nu")]
    need(isinstance(value, (list, tuple)) and len(value) == 3, "Missing full triple")
    parts = [trim(p) for p in value]
    need(sum(parts[0]) == sum(parts[1]) + sum(parts[2]), "Unbalanced source triple")
    need(1 <= max(map(len, parts)) <= 7, "Source ordinary rank is outside 1..7")
    return dict(zip(("lambda", "mu", "nu"), parts))


def bind_source_triple(source, terminal):
    source, terminal = triple(source), triple(terminal)
    need(source["lambda"] == terminal["lambda"], "Source/terminal outer partition differs")
    if source == terminal:
        operation = "identity_after_trailing_zero_trim"
    else:
        need(source["mu"] == terminal["nu"] and source["nu"] == terminal["mu"], "Source/terminal binding requires an unsupported transformation")
        operation = "inner_exchange_after_trailing_zero_trim"
    return source, terminal, {"operation": operation, "common_dilation_or_affine_reduction_used": False,
                             "premise": "Classical LR inner commutativity and zero-padding invariance"}


def raw_vector(value):
    need(isinstance(value, list) and value, "Complete source vector is missing")
    for coefficient in value:
        need(type(coefficient) is int or (type(coefficient) is str and re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", coefficient)),
             "Source coefficient is not exact integer/rational text")
    return value


def source_key(row):
    s = row["source"]
    return s["benchmark_file"], s["index_1based"], s["line_sha256"]


def resolve_origin(origin):
    for prefix, base in (("research:", C), ("restored-pro026:", R)):
        if origin.startswith(prefix):
            relative = origin[len(prefix):]
            need(not Path(relative).is_absolute() and ".." not in Path(relative).parts, "Source origin escapes its allowed root")
            return base / relative
    raise SourceError("Unrecognized source origin; protected roots are not opened")


def extract_sources(selection_path=SELECTION, fre_map_path=FRE_MAP, fri_final_path=FRI_FINAL, fri_audit_path=FRI_AUDIT):
    """Administrative extraction; deliberately never calls geometry/evaluation."""
    selected = load(selection_path)
    wanted = [x for x in selected["choices"] if x["family"] in EXPECTED_COUNTS]
    need(Counter(x["family"] for x in wanted) == EXPECTED_COUNTS and len({x["terminal_id"] for x in wanted}) == 297,
         "Exact chosen FRE/FRI terminal cohort differs")
    fre_records = load(fre_map_path)
    fre = {x["terminal_id"]: x for x in fre_records}
    need(len(fre) == len(fre_records) == 185, "FRE source map is incomplete or duplicated")
    final, audit = load(fri_final_path), load(fri_audit_path)
    dispositions = {x["id"]: (i, x) for i, x in enumerate(final["dispositions"])}
    need(len(dispositions) == len(final["dispositions"]), "Duplicate FRI disposition identity")
    audit_by_source = {}
    for i, row in enumerate(audit["rows"]):
        key = source_key(row)
        need(key not in audit_by_source, "Ambiguous original FRI source index")
        audit_by_source[key] = (i, row)
    repairs = {x["id"]: (i, x) for i, x in enumerate(final["repaired_vectors"])}
    inputs = {str(Path(p).resolve()): file_pin(p) for p in (selection_path, fre_map_path, fri_final_path, fri_audit_path)}
    records, missing = [], []
    for local_id, chosen in enumerate(wanted):
        item = {"id": local_id, "terminal_id": chosen["terminal_id"], "family": chosen["family"],
                "source_id": chosen["source_id"], "chosen_seed_key": chosen["seed_key"],
                "terminal_source_triple": triple(chosen["source_triple"]), "source_vector_accepted": False,
                "status": "SOURCE_VECTOR_UNACCEPTED_PENDING_FRESH_RECOUNT"}
        try:
            if chosen["family"] == "FRE":
                origin = fre[chosen["terminal_id"]]
                path = resolve_origin(origin["origin"])
                identity = file_pin(path)
                need({k: identity[k] for k in ("bytes", "sha256")} == {k: origin[k] for k in ("bytes", "sha256")}, "FRE source bytes differ from exact selected source map")
                document = load(path)
                need(document["selected_index"] == origin["original_selected_index"], "FRE original execution index changed")
                source_triple, terminal, binding = bind_source_triple(document["key"], chosen["source_triple"])
                coefficients = raw_vector(document["coefficients_low_to_high"])
                primary = raw_vector(document["primary_normaliz"]["coeffs_low_to_high"])
                need(coefficients == primary, "Conflicting full vectors in the selected FRE source")
                need(type(document["certified_degree"]) is int and len(coefficients) == document["certified_degree"] + 1,
                     "FRE source vector does not contain its full declared coefficient roster")
                inputs[identity["path"]] = identity
                item.update(bare_triple=source_triple, terminal_source_triple=terminal, source_to_terminal_binding=binding,
                            coefficients_low_to_high=coefficients, source_declared_degree=document["certified_degree"],
                            vector_reference={**identity, "json_pointer": "/coefficients_low_to_high", "record_pointer": "",
                                              "record_sha256": sha(encoded(document))},
                            triple_reference={**identity, "json_pointer": "/key"},
                            original_execution_identity={"group": origin["original_execution_group"], "selected_index": origin["original_selected_index"],
                                                         "command_indices": document.get("command_indices"), "origin": origin["origin"]},
                            additional_vector_sources=[{"json_pointer": "/primary_normaliz/coeffs_low_to_high", "same_source_file": True}],
                            source_provenance_limit="Source-certificate values are copied, not newly accepted; old counters/commands are not executed.")
            else:
                position, disposition = dispositions[chosen["source_id"]]
                need(disposition["state"] != "remaining_vector_authentication", "Unresolved FRI source was selected")
                need(triple(disposition["canonical_identity"]) == triple(chosen["source_triple"]), "FRI selected terminal source key differs")
                audit_position, row = audit_by_source[source_key(disposition)]
                need(row["canonical_identity"] == disposition["canonical_identity"], "FRI source-index/canonical-identity mismatch")
                source_triple, terminal, binding = bind_source_triple(row["original_triple"], chosen["source_triple"])
                need(source_triple == triple({k: row["source_row"][k] for k in ("lambda", "mu", "nu")}), "FRI copied original triple differs")
                coefficients = raw_vector(row["exact_source_coefficients"])
                need(coefficients == raw_vector(row["source_row"]["coeffs_low_to_high"]), "FRI source audit contains conflicting vectors")
                need(type(row["source_dim"]) is int and len(coefficients) == row["source_dim"] + 1,
                     "FRI source vector does not contain its full declared coefficient roster")
                alternate = []
                if chosen["source_id"] in repairs:
                    repair_position, repair = repairs[chosen["source_id"]]
                    need(coefficients == raw_vector(repair["coefficients_low_to_high"]), "FRI fresh repair and old source vectors differ; explicit source disposition is needed")
                    alternate.append({**inputs[str(Path(fri_final_path).resolve())], "json_pointer": f"/repaired_vectors/{repair_position}/coefficients_low_to_high"})
                identity = inputs[str(Path(fri_audit_path).resolve())]
                item.update(bare_triple=source_triple, terminal_source_triple=terminal, source_to_terminal_binding=binding,
                            coefficients_low_to_high=coefficients, source_declared_degree=row["source_dim"],
                            vector_reference={**identity, "json_pointer": f"/rows/{audit_position}/exact_source_coefficients",
                                              "record_pointer": f"/rows/{audit_position}", "record_sha256": sha(encoded(row))},
                            triple_reference={**identity, "json_pointer": f"/rows/{audit_position}/original_triple"},
                            adopted_disposition_reference={**inputs[str(Path(fri_final_path).resolve())], "json_pointer": f"/dispositions/{position}"},
                            original_execution_identity={"benchmark_file": row["source"]["benchmark_file"], "source_line": row["source"]["line"],
                                                         "source_line_sha256": row["source"]["line_sha256"], "original_file_sha256": row["source"]["sha256"]},
                            additional_vector_sources=alternate,
                            source_provenance_limit="The canonical audit explicitly did not accept every old source vector. No protected slr-lab source is opened; these are unaccepted exact expected polynomials for a new recount.")
        except (SourceError, KeyError, FileNotFoundError) as error:
            item.update(status="MISSING_OR_AMBIGUOUS_SOURCE_VECTOR", error=f"{type(error).__name__}: {error}")
            missing.append({"id": local_id, "terminal_id": chosen["terminal_id"], "error": item["error"]})
        records.append(item)
    return {"schema": VECTOR_SCHEMA, "status": "SOURCE_VECTORS_EXTRACTED_UNACCEPTED" if not missing else "SOURCE_VECTOR_GAPS",
            "expected_terminal_ids": [x["terminal_id"] for x in wanted], "expected_record_ids": list(range(297)),
            "selection_reference": inputs[str(Path(selection_path).resolve())], "inputs": list(inputs.values()),
            "records": records, "missing_sources": missing,
            "source_scope_counts": {"expected": 297, "FRE": 185, "FRI-settled": 112, "located_unaccepted": 297 - len(missing)},
            "geometry_generated": False, "polynomial_evaluations_performed": False, "lattice_counts_performed": 0,
            "source_vector_acceptance_asserted": False, "creator": {**file_pin(Path(__file__)), "command": "extract", "argv": sys.argv}}


def validate_identities(document, *, expected_count=297):
    need(document.get("schema") == VECTOR_SCHEMA, "Wrong legacy source schema")
    records = document["records"]
    need(all(type(r.get("id")) is int and isinstance(r.get("terminal_id"), str) and r["terminal_id"] for r in records),
         "Local and terminal identities require exact types")
    need(len(records) == expected_count and [r["id"] for r in records] == list(range(expected_count)), "Missing, reordered or duplicate local identities")
    ids = [r["terminal_id"] for r in records]
    need(len(set(ids)) == expected_count and ids == document["expected_terminal_ids"], "Exact terminal identity roster changed")
    need(document["expected_record_ids"] == list(range(expected_count)), "Expected local identity roster changed")
    need(all(r.get("source_vector_accepted") is False for r in records), "A source vector was silently accepted")
    return records


def ambient_model(bare, geometry_helpers):
    """Root-only real-corpus generation; tests use tiny self-authored triples."""
    bare = triple(bare)
    rank = max(len(p) for p in bare.values())
    dimension = (rank - 1) * (rank - 2) // 2
    area = sum(bare["lambda"])
    padded = [bare[k] + [0] * (rank - len(bare[k])) for k in ("lambda", "mu", "nu")]
    points, stencil = geometry_helpers.triangle(rank)
    need(len(points) == dimension and len(stencil) == 3 * rank * (rank - 1) // 2, "Full triangular coordinate/rhombus roster differs")
    H = geometry_helpers.boundaries(rank, padded, dimension)
    for j, point in enumerate(points):
        H[point] = [0] + [int(i == j) for i in range(dimension)]
    rows = geometry_helpers.rhombi(H, stencil)
    need(len(rows) == 3 * rank * (rank - 1) // 2 and all(len(row) == dimension + 1 and all(type(v) is int for v in row) for row in rows), "Incomplete or noninteger ambient hive rows")
    return {"rank": rank, "dimension": dimension, "count_boundary_area": area, "full_rows": rows,
            "unit_selections": [{"variable": j, "original_hive_coordinate": j, "base": 0,
                                 "unit_row": [int(i == j) for i in range(dimension)]} for j in range(dimension)],
            "original_hive_coordinate_points": [list(p) for p in points],
            "padded_boundary": dict(zip(("lambda", "mu", "nu"), padded)),
            "degree_is_ambient_upper_bound_not_actual_dimension": True,
            "affine_reduction_used": False, "strict_interior_used": False,
            "geometry_premise": CLASSICAL_PREMISES[0] + " " + CLASSICAL_PREMISES[1]}


def polynomial_values(raw, maximum_grade, ambient_degree):
    raw_vector(raw)
    need(len(raw) <= ambient_degree + 1, "Source polynomial exceeds the complete ambient degree upper bound")
    coefficients = [Fraction(v) for v in raw]
    result = []
    for grade in range(maximum_grade + 1):
        value = Fraction(0)
        for coefficient in reversed(coefficients):
            value = value * grade + coefficient
        need(value.denominator == 1 and value >= 0, f"Source polynomial gives a negative/noninteger expected count at grade {grade}")
        result.append(value.numerator)
    need(result[0] == 1, "Requested zero-containing grid requires the selected nonempty source-polynomial convention")
    return result


def make_job(record, geometry_helpers, helper_pin):
    need(record["status"] == "SOURCE_VECTOR_UNACCEPTED_PENDING_FRESH_RECOUNT", "Missing source vector cannot become a recount job")
    source, terminal, binding = bind_source_triple(record["bare_triple"], record["terminal_source_triple"])
    need(binding == record["source_to_terminal_binding"], "Source-to-terminal binding changed")
    model = ambient_model(source, geometry_helpers)
    D = model["dimension"]
    values = polynomial_values(record["coefficients_low_to_high"], D + 2, D)
    nodes = [{"kind": f"P{grade}", "grade": grade, "strict": False,
              "stored": {"source_polynomial": value},
              "role": "determining" if grade <= D else "positive_holdout",
              "expected_value_provenance": "Exact evaluation of one unaccepted source vector; not two independent recorded models"}
             for grade, value in enumerate(values)]
    model_hash = sha(encoded({"bare_triple": source, "model": model}))
    return {"unit": "LEGACY", "id": record["id"], "terminal_id": record["terminal_id"],
            "source_id": record["source_id"], "bare_triple": source, "terminal_source_triple": terminal,
            "source_to_terminal_binding": binding, "geometry_sha256": model_hash,
            "geometry_reference": {"kind": "fresh_full_ambient_model_from_literal_source_triple", "helper": helper_pin,
                                   "older_minimal_geometry_or_raw_adapter_used": False},
            "certificate_reference": record["vector_reference"], "source_coefficients_low_to_high": record["coefficients_low_to_high"],
            "original_execution_identity": record["original_execution_identity"], "model": model, "nodes": nodes,
            "geometry_acceptance": "CLASSICAL_FULL_AMBIENT_HIVE_AND_COORDINATE_BOUND_PREMISES",
            "source_vector_accepted": False, "ambient_degree_upper_bound": D,
            "determining_grades": list(range(D + 1)), "unused_positive_grades": [D + 1, D + 2]}


def validate_source_record(record, documents):
    reference = record["vector_reference"]
    document = documents[reference["path"]]
    need(pointer(document, reference["json_pointer"]) == record["coefficients_low_to_high"], "Metadata vector differs from exact source pointer")
    body = pointer(document, reference["record_pointer"]) if reference["record_pointer"] else document
    need(sha(encoded(body)) == reference["record_sha256"], "Metadata source record hash differs")
    tref = record["triple_reference"]
    source = triple(pointer(documents[tref["path"]], tref["json_pointer"]))
    need(source == record["bare_triple"], "Metadata original triple differs from exact source pointer")


def index_jobs(input_path, wrapper_path, helper_path, output, *, seconds=100, expected_count=297, argv=None):
    # Only the root-owned geometry module is imported. The actual path is
    # explicit and pinned in both the manifest and every generated model.
    import importlib.util
    deadline = Deadline(seconds)
    input_path, output = Path(input_path).resolve(), Path(output).resolve()
    wrapper_path, helper_path = Path(wrapper_path).resolve(), Path(helper_path).resolve()
    need(helper_path.parent == W and helper_path.name == "box_geometry.py", "Use only the named root-owned geometry helper")
    need(wrapper_path.parent == W and wrapper_path.name == "recount_records.py", "Use only the named required recount consumer")
    need(not output.exists() and output.parent.is_dir() and not output.is_relative_to(input_path.parent), "Fresh scientific outputs must be outside immutable source metadata root")
    document = load(input_path)
    records = validate_identities(document, expected_count=expected_count)
    sources = [file_pin(input_path, deadline), file_pin(wrapper_path, deadline), file_pin(helper_path, deadline), file_pin(Path(__file__), deadline)]
    originals = {}
    for identity in document["inputs"]:
        need(file_pin(identity["path"], deadline) == identity, "Legacy source input changed")
        sources.append(identity)
        if any(r.get("vector_reference", {}).get("path") == identity["path"] or r.get("triple_reference", {}).get("path") == identity["path"] for r in records):
            originals[identity["path"]] = load(identity["path"])
    selected = load(document["selection_reference"]["path"])
    by_terminal = {r["terminal_id"]: r for r in selected["choices"] if r["family"] in EXPECTED_COUNTS}
    need(set(by_terminal) == {r["terminal_id"] for r in records}, "Legacy metadata no longer matches exact chosen adopted identities")
    helper_pin = file_pin(helper_path, deadline)
    spec = importlib.util.spec_from_file_location("root_owned_legacy_geometry", helper_path)
    geometry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    jobs_path = output.with_suffix(".jobs.jsonl")
    need(not jobs_path.exists(), "Fresh legacy jobs file is required")
    entries, seen, problems = [], set(), []
    result = {"schema": SCHEMA, "kind": "manifest", "status": "PARTIAL", "unit": "LEGACY",
              "stream": "297-chosen-adopted-source-polynomials", "input_root": str(input_path.parent),
              "expected_record_ids": document["expected_record_ids"], "records": entries,
              "selection_complete": True, "index_complete": False,
              "terminal_id_mapping": [{"id": r["id"], "terminal_id": r["terminal_id"], "source_id": r["source_id"]} for r in records],
              "wrapper_sha256": file_pin(wrapper_path, deadline)["sha256"], "required_consumer": file_pin(wrapper_path, deadline),
              "indexer": {**file_pin(Path(__file__), deadline), "argv": list(argv if argv is not None else sys.argv), "command": "index"},
              "classical_premises": CLASSICAL_PREMISES, "source_vectors_accepted": False, "lattice_counts_performed": 0}
    try:
        with jobs_path.open("xb") as jobs:
            for record in records:
                deadline.check()
                if record["status"] != "SOURCE_VECTOR_UNACCEPTED_PENDING_FRESH_RECOUNT":
                    problems.append({"id": record["id"], "terminal_id": record["terminal_id"], "reason": record.get("error", "missing source vector")})
                    continue
                chosen = by_terminal[record["terminal_id"]]
                need(triple(chosen["source_triple"]) == record["terminal_source_triple"] and chosen["source_id"] == record["source_id"], "Selected terminal literal source key changed")
                validate_source_record(record, originals)
                negative=[k for k,value in enumerate(record['coefficients_low_to_high']) if Fraction(value)<0]
                if negative:
                    candidate=output.with_suffix('.candidate.json')
                    write_json(candidate,{'schema':'legacy-primary-LR-negative-observation-v1',
                                          'status':'HOLD_PENDING_FRESH_INDEPENDENT_COUNTS',
                                          'terminal_id':record['terminal_id'],'bare_triple':record['bare_triple'],
                                          'coefficients_low_to_high':record['coefficients_low_to_high'],
                                          'negative_indices':negative,'source':record['vector_reference'],
                                          'captured_before_new_count_comparisons':True})
                    result.update(status='HOLD_CANDIDATE',candidate=str(candidate))
                    break
                job = make_job(record, geometry, helper_pin)
                need(record["id"] not in seen, "Duplicate legacy local job identity")
                seen.add(record["id"])
                offset, body = jobs.tell(), encoded(job) + b"\n"
                jobs.write(body)
                entries.append({"ordinal": len(entries), "id": job["id"], "geometry_sha256": job["geometry_sha256"],
                                "offset": offset, "bytes": len(body), "sha256": sha(body),
                                "node_ids": [f"LEGACY:{job['id']}:{node['kind']}" for node in job["nodes"]]})
        result["index_complete"] = len(seen) == expected_count
        if result['status']!='HOLD_CANDIDATE':
            result["status"] = "FROZEN_RECOUNT_JOBS" if result["index_complete"] else "PARTIAL"
    except DeadlineReached as error:
        result["interruption"] = str(error)
    except (SourceError, KeyError, ValueError, OSError) as error:
        result.update(status="FAIL", error=f"{type(error).__name__}: {error}")
    finally:
        result["pending_index_ids"] = sorted(set(document["expected_record_ids"]) - seen)
        result["source_problems"] = problems
        result["jobs"] = file_pin(jobs_path)
        result["inputs"] = list({x["path"]: x for x in sources}.values())
        write_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    extract = commands.add_parser("extract")
    extract.add_argument("--output", type=Path, default=OUTPUT_SOURCES)
    index = commands.add_parser("index")
    index.add_argument("--input", type=Path, default=OUTPUT_SOURCES)
    index.add_argument("--wrapper", type=Path, default=W / "recount_records.py")
    index.add_argument("--geometry-helper", type=Path, default=W / "box_geometry.py")
    index.add_argument("--output", type=Path, required=True)
    index.add_argument("--budget-seconds", type=float, default=100)
    args = parser.parse_args()
    if args.command == "extract":
        need(args.output.resolve() == OUTPUT_SOURCES.resolve(), "Administrative extraction owns only LEGACY-VECTOR-SOURCES.json")
        result = extract_sources()
        write_json(args.output, result)
        print(json.dumps({"status": result["status"], "counts": result["source_scope_counts"], "missing": result["missing_sources"]}, indent=2))
    else:
        result = index_jobs(args.input, args.wrapper, args.geometry_helper, args.output, seconds=args.budget_seconds)
        print(json.dumps({"status": result["status"], "indexed": len(result["records"]), "pending_ids": result["pending_index_ids"], "counts_executed": 0}, indent=2))
    return 0 if result["status"] in ("SOURCE_VECTORS_EXTRACTED_UNACCEPTED", "FROZEN_RECOUNT_JOBS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
