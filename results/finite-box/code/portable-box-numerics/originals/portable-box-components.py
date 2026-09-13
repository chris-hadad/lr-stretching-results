#!/usr/bin/env python3
"""Serial component replay over the frozen portable_run.py, not a theorem gate.

prepare reads metadata only. run executes one explicitly selected component;
status and aggregate recheck exact source/receipt/identity membership. Outputs
are fresh; STATE.json is the sole replaceable journal. Interrupted launches
without a completed portable execution must be resolved by their owner.

Python 3.10+ and the portable launcher's POSIX requirements apply. No scientific
checker is imported. Geometry/final bindings cannot be sliced. Bounds/algebra
timeouts have no authenticated partial cursor and leave their entire range
pending. Early CANNOT_CHECK prefixes are reusable only after a real child exit,
successful source finalization, and exact checked/pending/ledger agreement.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys


SCHEMA = "portable-box-components-v1"
COMPONENTS = ("geometry", "algebra", "bounds", "early", "final")
COUNTS = dict(zip((f"U{i:02d}" for i in range(4, 12)),
                  (150147, 154408, 143401, 99212, 51477, 18424, 2806, 495)))
COMPACT = {
    "U04": "DATA/U04/final-science/UNIFORM-FOUR-COUNT-CERTIFICATES.jsonl.gz",
    "U05": "DATA/U05/third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz",
    "U06": "DATA/U06/final-science/UNIFORM-SEPTIC-CERTIFICATES.jsonl.gz",
    "U07": "DATA/U07/final-science/UNIFORM-OCTIC-CERTIFICATES.jsonl.gz",
    "U08": "DATA/U08/final-science-v2/UNIFORM-NONIC-CERTIFICATES.jsonl.gz",
    "U09": "DATA/U09/final-science/COMPACT-CERTIFICATES.jsonl.gz",
    "U10": "DATA/U10/final-science/COMPACT-CERTIFICATES.jsonl.gz",
    "U11": "DATA/U11/final-science/COMPACT-CERTIFICATES.jsonl.gz",
}
FINAL_COMPACT = "namespaces/u12/AUDIT/U11-COMPLETE-VECTORS/COMPACT-CERTIFICATES.jsonl.gz"
EARLY = {"U02": "DATA/U02/two-model-mixed-certificate.json",
         "U03": "DATA/U03/hybrid-verification-v3/certificates.jsonl"}
EARLY_KEYS = {"U02": "chosen_u02_numeric_ids", "U03": "source_order_early_u03_numeric_ids"}
CHECKERS = {"geometry": "verify_box_geometry.py", "algebra": "verify_box_algebra.py",
            "bounds": "verify_box_bounds.py", "early": "verify_early_terminals.py",
            "final": "verify_box_final_bindings.py"}
SCOPE = {
    "new_numerical_recounts": 0, "whole_box_theorem_accepted": False,
    "recorded_count_correctness_proved": False,
    "remaining": ["Fresh complete numerical recounts and their exact node joins",
                  "Original census and adopted mathematical predecessor proofs",
                  "Legacy vectors, source terminals, composition and final theorem join",
                  "Every-record bridge from U11 algebra compact to the U12 final-binding audit compact"],
}


class Refusal(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise Refusal(message)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            need(k not in result, "Duplicate JSON field: " + k)
            result[k] = v
        return result
    def invalid(x):
        raise Refusal("Nonfinite JSON: " + x)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def read(path):
    return decode(plain(path).read_bytes())


def relative(value):
    need(isinstance(value, str) and value and "\\" not in value and ":" not in value
         and all(ord(x) >= 32 and ord(x) != 127 for x in value), "Invalid relative path")
    p = Path(value)
    need(not p.is_absolute() and str(p) == value and all(v not in (".", "..") for v in p.parts),
         "Noncanonical or escaping relative path")
    return value


def plain(path):
    p = Path(path).absolute()
    need(not any(x.is_symlink() for x in (p, *p.parents)), "Symlink path: " + str(p))
    return p.resolve()


def pin(path):
    p = plain(path)
    need(p.is_file(), "Missing regular file: " + str(p))
    before = p.stat()
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    after = p.stat()
    fields = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    need(fields(before) == fields(after), "File changed during hashing: " + str(p))
    return {"path": str(p), "bytes": before.st_size, "sha256": h.hexdigest()}


def check_pin(p):
    need(pin(p["path"]) == p, "Changed bound input/output: " + p["path"])


def write(path, value):
    with Path(path).open("xb") as f:
        f.write(encoded(value) + b"\n")
        f.flush()
        os.fsync(f.fileno())


def replace_state(work, state):
    # Unique temporary path; no old execution, result or diagnostic is replaced.
    temp = work / ("STATE." + str(os.getpid()) + ".tmp")
    write(temp, state)
    os.replace(temp, work / "STATE.json")


def fresh_report(work, prefix, value):
    number = 1
    while (work / f"{prefix}-{number:06d}.json").exists():
        number += 1
    p = work / f"{prefix}-{number:06d}.json"
    write(p, value)
    return p


def manifest(raw):
    z = decode(raw)
    need(z.get("schema") == "early-input-manifest-v1" and isinstance(z.get("files"), list),
         "A portable early-input-manifest-v1 is required")
    result = {}
    for p in z["files"]:
        need(set(p) == {"path", "bytes", "sha256"}, "Malformed source declaration")
        name = relative(p["path"])
        need(name not in result, "Duplicate manifested path: " + name)
        need(type(p["bytes"]) is int and p["bytes"] >= 0 and
             isinstance(p["sha256"], str) and re.fullmatch("[0-9a-f]{64}", p["sha256"]), "Invalid source pin")
        result[name] = {k: p[k] for k in ("bytes", "sha256")}
    return result


def compact_path(unit):
    return "namespaces/" + unit.lower() + "/" + COMPACT[unit]


def geometry_path(unit, shard):
    folder = f"DATA/U04/layer5-results/{shard}" if unit == "U04" else f"DATA/{unit}/production/{shard}/counts"
    return f"namespaces/{unit.lower()}/{folder}/geometry.jsonl.gz"


def one_option(words, flag):
    values = [words[i + 1] for i, word in enumerate(words[:-1]) if word == flag]
    need(len(values) == 1, "Missing or duplicate recipe option: " + flag)
    return values[0]


def geometry_recipe(document):
    """Translate only the explicit historical metadata; never run its argv."""
    rows, seen, old_ids = [], set(), set()
    for job in document["jobs"]:
        unit, shard, count, words = job["unit"], job["shard"], job["expected_selected"], job["argv"]
        need(unit in COUNTS and unit != "U11" and re.fullmatch(r"shard-?\d+", shard)
             and type(count) is int and count > 0, "Invalid geometry stream")
        need((unit, shard) not in seen and job["id"] not in old_ids, "Duplicate geometry stream/launch identity")
        seen.add((unit, shard)); old_ids.add(job["id"])
        need(one_option(words, "--unit") == unit and one_option(words, "--shard") == shard
             and one_option(words, "--expected-selected") == str(count), "Geometry metadata/argv mismatch")
        old_root = Path(one_option(words, "--root"))
        need(old_root.is_absolute() and old_root.name == unit.lower() and old_root.parent.name == "namespaces",
             "Unexpected historical namespace layout")
        paths = []
        for i, word in enumerate(words[:-1]):
            if word != "--input":
                continue
            p = Path(words[i + 1])
            if p.is_relative_to(old_root.parent):
                name = "namespaces/" + str(p.relative_to(old_root.parent))
            elif p.name == "GEOMETRY-JOBS.json":
                continue  # The exact metadata bytes are bound separately.
            elif re.fullmatch(r"F025-MASK-R[67]-001.json", p.name) and p.parts[-4:-1] == (
                    "frontier-025-2026-09-10", "science", "results"):
                name = "namespaces/base/methods/frontier-025-2026-09-10/science/results/" + p.name
            else:
                raise Refusal("Unmapped historical input: " + str(p))
            name = relative(name)
            need(name not in paths, "Duplicate declared geometry source")
            paths.append(name)
        need(compact_path(unit) in paths and geometry_path(unit, shard) in paths, "Missing literal compact/geometry source")
        folder = str(Path(geometry_path(unit, shard)).parent)
        required = {folder + "/certificates.jsonl", compact_path(unit), geometry_path(unit, shard)}
        required |= {folder + "/" + m + ("-queries.jsonl" if unit == "U04" else ".jsonl") for m in ("hive", "rows")}
        required |= {f"namespaces/base/methods/frontier-025-2026-09-10/science/results/F025-MASK-R{n}-001.json" for n in (6, 7)}
        if unit == "U04":
            required |= {"namespaces/u04/DATA/U04/seven-dual-repairs/" + name for name in
                         ("certificates.jsonl", "hive-queries.jsonl", "rows-queries.jsonl")}
        need(required <= set(paths), "Historical recipe omitted an actually read geometry/raw/mask source: " + str(sorted(required - set(paths))))
        rows.append({"key": unit + "/" + shard, "unit": unit, "shard": shard, "count": count,
                     "compact": compact_path(unit), "geometry": geometry_path(unit, shard),
                     "inputs": paths, "historical_job_id": job["id"]})
    need(len(rows) == 62 and document["expected_total"] == sum(r["count"] for r in rows) == 619875,
         "Expected the exact 62-stream production geometry recipe")
    for unit in list(COUNTS)[:-1]:
        need(sum(r["count"] for r in rows if r["unit"] == unit) == COUNTS[unit], "Wrong per-unit geometry population")
    return rows


def prepare(args):
    need(sys.version_info >= (3, 10), "Python 3.10+ is required by frozen checkers")
    work, data, code = plain(args.work_root), plain(args.data_root), plain(args.code_root)
    need(not work.exists() and not work.is_relative_to(data) and not work.is_relative_to(code),
         "prepare requires a fresh work root outside data/code")
    metadata = {}
    for name, path, sha in (("source-manifest.json", args.source_manifest, args.source_manifest_sha256),
                            ("chosen-terminals.json", args.chosen_terminals, args.chosen_terminals_sha256),
                            ("geometry-jobs.json", args.geometry_jobs, args.geometry_jobs_sha256)):
        p = pin(path)
        need(p["sha256"] == sha, "Metadata SHA-256 mismatch: " + name)
        raw = Path(path).read_bytes()
        need(digest(raw) == sha, "Metadata changed while reading")
        metadata[name] = (raw, p)
    declarations = manifest(metadata["source-manifest.json"][0])
    chosen = decode(metadata["chosen-terminals.json"][0])
    need(chosen.get("schema") == "finite-box-chosen-terminal-sources-v1", "Unknown chosen-terminal metadata")
    for unit, total in (("U02", 169), ("U03", 3478)):
        ids = chosen[EARLY_KEYS[unit]]
        need(len(ids) == total and all(type(x) is int for x in ids) and len(set(ids)) == total,
             "Missing/duplicate exact chosen early IDs")
    geometry = geometry_recipe(decode(metadata["geometry-jobs.json"][0]))
    streams = {
        "geometry": geometry,
        "algebra": [{"key": u, "unit": u, "count": n, "compact": compact_path(u), "inputs": [compact_path(u)]}
                    for u, n in COUNTS.items()],
        "bounds": [dict(r) for r in geometry if r["unit"] != "U04"],
        "early": [{"key": u, "unit": u, "count": len(chosen[EARLY_KEYS[u]]),
                   "compact": f"namespaces/{u.lower()}/{EARLY[u]}",
                   "inputs": [f"namespaces/{u.lower()}/{EARLY[u]}"]} for u in EARLY],
        "final": [{"key": "U11", "unit": "U11", "count": 495,
                   "compact": FINAL_COMPACT, "inputs": [FINAL_COMPACT]}],
    }
    need(len(streams["bounds"]) == 43 and sum(s["count"] for s in streams["bounds"]) == 469728,
         "Wrong bounds stream recipe")
    for group in streams.values():
        for stream in group:
            for name in stream["inputs"]:
                need(name in declarations, "Missing planned source in portable manifest: " + name)
    map_pin = pin(code / "SOURCE-MAP.json")
    copies = read(map_pin["path"])
    need(copies["schema"] == "portable-box-source-copies-v1", "Unknown frozen code map")
    code_pins = {}
    for item in copies["copies"]:
        name = relative(item["path"])
        need(name not in code_pins, "Duplicate frozen code identity")
        p = pin(code / name)
        need((p["bytes"], p["sha256"]) == (item["portable_bytes"], item["portable_sha256"]), "Stale copied checker")
        code_pins[name] = p
    need(set(CHECKERS.values()) <= set(code_pins), "Missing copied component checker")
    settings = {"algebra": args.algebra_chunk, "bounds": args.bounds_chunk, "early": args.early_chunk,
                "timeout": args.timeout, "internal_seconds": args.internal_seconds}
    need(all(type(settings[k]) is int and settings[k] > 0 for k in ("algebra", "bounds", "early"))
         and math.isfinite(args.timeout) and 0 < args.internal_seconds <= 110
         and args.internal_seconds < args.timeout <= 120,
         "Invalid finite chunk/deadline settings")
    work.mkdir(parents=True)
    (work / "metadata").mkdir(); (work / "attempts").mkdir()
    copied = {}
    for name, (raw, p) in metadata.items():
        target = work / "metadata" / name
        with target.open("xb") as f:
            f.write(raw)
        check_pin(p)
        copied[name] = pin(target)
    recipe = {"schema": SCHEMA, "data_root": str(data), "work_root": str(work), "code_root": str(code),
              "controller": pin(__file__), "launcher": pin(code / "portable_run.py"), "source_map": map_pin,
              "copied_sources": code_pins, "metadata": copied, "streams": streams, "settings": settings,
              "preparation_executed_checkers": False, "scope": SCOPE}
    write(work / "RECIPE.json", recipe)
    replace_state(work, {"schema": SCHEMA, "recipe": pin(work / "RECIPE.json"), "rosters": {}, "attempts": []})
    return {"status": "PREPARED_METADATA_ONLY", "recipe": pin(work / "RECIPE.json"), "scope": SCOPE}


def json_lines(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rb") as f:
        for ordinal, raw in enumerate(f):
            need(raw.strip(), "Blank record in exact source/identity stream")
            yield ordinal, decode(raw), raw


def record_id(row):
    value = row.get("group_id", row.get("target_ordinal", row.get("id")))
    need(type(value) is int, "Missing/noninteger record identity")
    return value


def exact_rows(expected, actual, fields):
    need(len(expected) == len(actual), "Missing/extra identity records")
    seen = set()
    for want, got in zip(expected, actual):
        need(type(got.get("id")) is int and got["id"] not in seen, "Duplicate/invalid identity")
        seen.add(got["id"])
        for e, a in fields:
            need(e in want and a in got and want[e] == got[a], "Source/identity field differs: " + a)


def early_prefix(result, ledger, ids, start, stop):
    need(result["slice"] == [start, stop] and result["expected_ids"] == ids,
         "Early slice/complete chosen roster mismatch")
    checked = result["checked_ids"]
    end = start + len(checked)
    need(end <= stop and checked == ids[start:end] and result["pending_slice_ids"] == ids[end:stop],
         "Early prefix cursor omitted/reordered identities")
    need("error" not in result, "Early source finalization or outer check failed; prefix is unusable")
    passed = ledger[:len(checked)]
    need([r.get("id") for r in passed] == checked and
         [r.get("ordinal") for r in passed] == list(range(start, end)) and
         all(r.get("status") == "PASS_CONDITIONAL_ON_RECORDED_COUNTS" for r in passed),
         "Early ledger does not authenticate the exact prefix")
    if result["status"] == "PASS_CONDITIONAL_ON_RECORDED_COUNTS":
        need(end == stop and len(ledger) == len(checked) and "failure" not in result, "Incomplete early PASS")
    else:
        need(result["status"] in ("CANNOT_CHECK", "PARTIAL") and end < stop
             and len(ledger) == len(checked) + 1 and result.get("failure") == ledger[-1]
             and ledger[-1].get("status") == "CANNOT_CHECK"
             and ledger[-1].get("id") == ids[end] and ledger[-1].get("ordinal") == end,
             "Missing or unauthenticated early failure boundary")
    return passed, end


class Context:
    def __init__(self, work):
        self.work = plain(work)
        self.state = read(self.work / "STATE.json")
        check_pin(self.state["recipe"])
        self.recipe = read(self.work / "RECIPE.json")
        r = self.recipe
        need(r["schema"] == self.state["schema"] == SCHEMA and r["work_root"] == str(self.work), "Wrong recipe/state root")
        self.data, self.code = plain(r["data_root"]), plain(r["code_root"])
        self.fixed = [r["controller"], r["launcher"], r["source_map"], *r["copied_sources"].values(), *r["metadata"].values()]
        need(r["controller"]["path"] == str(Path(__file__).resolve()), "Different controller source path")
        self.stable()
        self.sources = manifest(Path(r["metadata"]["source-manifest.json"]["path"]).read_bytes())
        self.chosen = read(r["metadata"]["chosen-terminals.json"]["path"])
        self.cache, self.compacts, self.used = {}, {}, {}
        ids = [a["id"] for a in self.state["attempts"]]
        need(ids == [f"component-{i + 1:06d}" for i in range(len(ids))], "Duplicate, missing or noncanonical journal execution identity")
        need(all(a["component"] in COMPONENTS for a in self.state["attempts"]), "Unknown journal component")

    def stable(self):
        check_pin(self.state["recipe"])
        for p in self.fixed:
            check_pin(p)

    def source(self, name):
        name = relative(name)
        need(name in self.sources, "Unmanifested input: " + name)
        p = pin(self.data / name)
        need({k: p[k] for k in ("bytes", "sha256")} == self.sources[name], "Changed manifested source: " + name)
        self.used[name] = p
        return p

    def compact(self, stream):
        name = stream["compact"]
        if name not in self.compacts:
            p = self.source(name)
            rows, seen = [], set()
            if stream["unit"] == "U02":
                values = [(i, z, encoded(z)) for i, z in enumerate(read(p["path"])["records"])]
            else:
                values = json_lines(p["path"])
            for ordinal, z, raw in values:
                key = record_id(z)
                need(key not in seen, "Duplicate compact/early source identity")
                seen.add(key)
                row = {"id": key, "ordinal": ordinal, "unit": stream["unit"],
                       "row_sha256": digest(raw), "bare_triple": z.get("bare_triple", z.get("triple"))}
                geometry = z.get("geometry")
                gh = z.get("geometry_sha256", geometry.get("sha256") if isinstance(geometry, dict) else None)
                if gh is not None:
                    row["geometry_sha256"] = gh
                if "actual_dimension" in z:
                    row["actual_degree"] = z["actual_dimension"]
                rows.append(row)
            expected = {"U02": 211, "U03": 4131}.get(stream["unit"], COUNTS.get(stream["unit"]))
            need(len(rows) == expected, "Literal compact source population changed")
            check_pin(p)
            self.compacts[name] = rows
        return self.compacts[name]

    def expected(self, component, stream):
        cache_key = (component, stream["key"])
        if cache_key not in self.cache:
            compact = self.compact(stream)
            if component in ("geometry", "bounds"):
                chosen = {r["id"]: r for r in compact}
                p = self.source(stream["geometry"])
                rows = []
                seen = set()
                for physical, z, raw in json_lines(p["path"]):
                    key = record_id(z)
                    if key not in chosen:
                        continue
                    need(key not in seen, "Duplicate physical selected geometry")
                    seen.add(key)
                    c = chosen[key]
                    need(digest(raw) == c["geometry_sha256"] and
                         (c["bare_triple"] is None or c["bare_triple"] == z["original"]), "Compact/physical geometry source changed")
                    rows.append({**c, "ordinal": len(rows), "compact_ordinal": c["ordinal"],
                                 "physical_ordinal": physical, "bare_triple": z["original"],
                                 "actual_degree": int(stream["unit"][1:]) + 1})
                check_pin(p)
            elif component == "early":
                wanted = set(self.chosen[EARLY_KEYS[stream["unit"]]])
                rows = [{**r, "source_ordinal": r["ordinal"], "ordinal": i}
                        for i, r in enumerate(r for r in compact if r["id"] in wanted)]
                need({r["id"] for r in rows} == wanted, "Missing chosen early source ID")
            else:
                rows = compact
            need(len(rows) == stream["count"], "Selected physical source population changed")
            self.cache[cache_key] = rows
        return self.cache[cache_key]

    def used_sources(self, component, stream, result):
        names = set(stream["inputs"])
        if component == "bounds" and "sources" in result:
            for name, value in result["sources"].items():
                full = f"namespaces/{stream['unit'].lower()}/" + relative(name)
                need(full in self.sources and value == self.sources[full], "Bound index used stale/unmanifested source")
                names.add(full)
        elif component == "early":
            for name, value in result["accessed_sources"].items():
                need(name in self.sources and value == self.sources[name], "Early checker used stale/unmanifested source")
                names.add(name)
        elif component == "final":
            for path, sha in result["source_inputs"].items():
                p = plain(path)
                need(p.is_relative_to(self.data), "Final checker source escaped data root")
                name = relative(str(p.relative_to(self.data)))
                need(name in self.sources and self.sources[name]["sha256"] == sha, "Final checker source differs from manifest")
                names.add(name)
        return [self.source(n) for n in sorted(names)]


def initial_progress(ctx, component):
    result = {}
    all_ids = {}
    for stream in ctx.recipe["streams"][component]:
        expected = ctx.expected(component, stream)
        unit_seen = all_ids.setdefault(stream["unit"], set())
        ids = {r["id"] for r in expected}
        need(not unit_seen & ids, "Duplicate component ID across shard streams")
        unit_seen.update(ids)
        result[stream["key"]] = {"stream": stream, "expected": expected, "cursor": 0,
                                 "index": None, "aggregate": None, "accepted": [], "fatal": None}
    if component in ("geometry", "bounds", "algebra", "final"):
        for group in result.values():
            stream = group["stream"]
            need(all_ids[stream["unit"]] == {r["id"] for r in ctx.compact(stream)}, "Component union omitted/added a compact certificate ID")
    names = {g["stream"]["compact"] for g in result.values()}
    if component in ("geometry", "bounds"):
        names |= {g["stream"]["geometry"] for g in result.values()}
    inventory = {"schema": SCHEMA, "component": component, "recipe": ctx.state["recipe"],
                 "exact_expected_streams": {key: g["expected"] for key, g in result.items()},
                 "sources": {name: ctx.source(name) for name in sorted(names)},
                 "predicate": "Literal source identity inventory only; no mathematical checker executed"}
    path = ctx.work / ("ROSTER-" + component + ".json")
    inventories = ctx.state.setdefault("rosters", {})
    if component in inventories:
        need(inventories[component]["path"] == str(path), "Escaped frozen roster")
        check_pin(inventories[component])
    if path.exists():
        need(read(path) == inventory, "Literal source roster changed")
    else:
        write(path, inventory)
    if component not in inventories:
        inventories[component] = pin(path)
        replace_state(ctx.work, ctx.state)
    return result


def operation(ctx, component, progress):
    for group in progress.values():
        s = group["stream"]
        if group["fatal"]:
            raise Refusal("Fatal prior checker result requires owner disposition: " + group["fatal"])
        if component == "bounds" and group["index"] is None:
            return {"stream": s["key"], "kind": "index", "slice": [0, s["count"]]}
        if group["cursor"] < s["count"]:
            start = group["cursor"]
            stop = min(s["count"], start + ctx.recipe["settings"].get(component, s["count"]))
            return {"stream": s["key"], "kind": "verify", "slice": [start, stop]}
        if component == "bounds" and group["aggregate"] is None:
            return {"stream": s["key"], "kind": "aggregate", "slice": [0, s["count"]]}
    return None


def checker_arguments(ctx, component, op, group):
    s, settings = group["stream"], ctx.recipe["settings"]
    start, stop = op["slice"]
    root = str(ctx.data / "namespaces" / s["unit"].lower())
    common = ["--unit", s["unit"]]
    sliced = ["--start", str(start), "--stop", str(stop)]
    if component == "geometry":
        return ["--root", root, *common, "--shard", s["shard"], "--expected-selected", str(s["count"])]
    if component == "algebra":
        return ["--input", str(ctx.data / s["compact"]), *common, *sliced, "--expected-total", str(s["count"])]
    if component in ("early", "final"):
        meta = ctx.recipe["metadata"]
        args = ["--root" if component == "early" else "--restored", str(ctx.data),
                "--source-manifest", meta["source-manifest.json"]["path"],
                "--source-manifest-sha256", meta["source-manifest.json"]["sha256"]]
        if component == "early":
            args += [*common, *sliced, "--required-ids", meta["chosen-terminals.json"]["path"],
                     "--required-ids-sha256", meta["chosen-terminals.json"]["sha256"],
                     "--max-seconds", str(settings["internal_seconds"])]
        return args
    if op["kind"] == "index":
        return ["index", "--root", root, *common, "--shard", s["shard"], "--expected-selected", str(s["count"]),
                "--max-seconds", str(settings["internal_seconds"])]
    index = group["index"]["result_pin"]
    args = [op["kind"], "--index", index["path"], "--index-sha256", index["sha256"]]
    if op["kind"] == "verify":
        args += sliced
    else:
        sha = ctx.recipe["copied_sources"][CHECKERS["bounds"]]["sha256"]
        args += ["--results", *[a["result_pin"]["path"] for a in group["accepted"]],
                 "--accepted-verifier-source", str(ctx.code / CHECKERS["bounds"]), "--accepted-verifier-sha256", sha]
    return args + ["--max-seconds", str(settings["internal_seconds"])]


def execution(ctx, request):
    """Authenticate the actual portable child exit and all declared output bytes."""
    path = ctx.work / request["id"]
    call_path = ctx.work / "attempts" / (request["id"] + ".caller.json")
    caller = read(call_path) if call_path.exists() else None
    if caller is not None:
        need(caller["request"] == pin(ctx.work / "attempts" / (request["id"] + ".json"))
             and type(caller["returncode"]) is int, "Caller identity changed")
    if not (path / "EXECUTION.json").exists():
        need(caller is not None and caller["returncode"] != 0, "Unresolved launch has no real completed execution; owner must reconcile it")
        return None
    receipt_pin = pin(path / "EXECUTION.json")
    receipt = read(receipt_pin["path"])
    need(receipt.get("schema") == "portable-box-execution-v1" and receipt["cleanup_verified"] is True
         and receipt["fixed_inputs_unchanged"] is True and not receipt["source_errors"], "Unclean/stale portable execution")
    need(receipt["configuration"] == pin(path / "CONFIGURATION.json"), "Changed execution configuration")
    config = read(receipt["configuration"]["path"])
    r = ctx.recipe
    need(config["schema"] == "portable-box-execution-v1" and config["id"] == request["id"]
         and config["checker"] == request["checker"] == receipt["checker"]
         and config["requested_checker_args"] == request["checker_args"] and not config["help_only"]
         and config["data_root"] == r["data_root"] and config["work_root"] == str(ctx.work)
         and config["output_root"] == str(path) and config["timeout_seconds"] == r["settings"]["timeout"]
         and config["source_map"] == r["source_map"] and config["copied_sources"] == r["copied_sources"],
         "Portable execution is not the exact requested copied checker/configuration")
    expected_argv = request["checker_args"] + ["--output", str(path / "result.json")]
    need(config["checker_argv"] == expected_argv and config["mutable_paths"] == [], "Changed checker argv or unexpected mutation")
    geometry = config["geometry_configuration"]
    base = str(ctx.data / "namespaces/base")
    need(geometry["box_geometry.CANONICAL"] == geometry["box_geometry_early.CANONICAL"] == base,
         "Historical host geometry configuration used")
    masks = [ctx.source(f"namespaces/base/methods/frontier-025-2026-09-10/science/results/F025-MASK-R{rank}-001.json")
             for rank in (6, 7)] if request["component"] in ("geometry", "early", "final") else []
    need(geometry["mask_inputs"] == masks, "Portable mask input roster differs")
    expected_fixed = [r["source_map"], r["launcher"], *r["copied_sources"].values(),
                      pin(Path(sys.executable).resolve()), *masks]
    words = request["checker_args"]
    for i, flag in enumerate(words):
        if flag in ("--input", "--source-manifest", "--required-ids", "--index", "--accepted-verifier-source"):
            expected_fixed.append(pin(words[i + 1]))
        elif flag == "--results":
            j = i + 1
            while j < len(words) and not words[j].startswith("--"):
                expected_fixed.append(pin(words[j])); j += 1
    fixed = {p["path"]: p for p in config["fixed_inputs"]}
    need(len(fixed) == len(config["fixed_inputs"]) and fixed == {p["path"]: p for p in expected_fixed},
         "Missing, extra or stale directly declared child input/code pin")
    for p in config["fixed_inputs"]:
        check_pin(p)
    outputs = {}
    for p in receipt["outputs"]:
        q = plain(p["path"])
        need(q.parent == path and q.name not in outputs, "Duplicate or escaped execution output")
        check_pin(p)
        outputs[q.name] = p
    need(all(p.is_file() and not p.is_symlink() for p in path.iterdir()), "Unexpected nonregular execution member")
    need(set(outputs) == {p.name for p in path.iterdir() if p.name != "EXECUTION.json"},
         "Missing/extra portable output roster")
    if receipt["disposition"] != "exited":
        return None
    need(type(receipt["child_returncode"]) is int and receipt["pid"] == receipt["pgid"], "Missing actual child exit")
    for name in ("LAUNCH.json", "APPLIED-CONFIGURATION.json", "CONFIGURATION.json", "result.json"):
        need(name in outputs, "Missing required completed-execution member: " + name)
    launch, applied = read(path / "LAUNCH.json"), read(path / "APPLIED-CONFIGURATION.json")
    need(launch["pid"] == launch["pgid"] == applied["pid"] == receipt["pid"]
         and applied["configuration"] == receipt["configuration"] and applied["before_mathematical_calls"] is True
         and applied["applied"] == {k: base for k in ("box_geometry.CANONICAL", "box_geometry_early.CANONICAL")},
         "Missing actual child/configuration application binding")
    expected_launch = [str(Path(sys.executable).resolve()), "-I", "-S", "-B", r["launcher"]["path"], "_child",
                       "--configuration", receipt["configuration"]["path"],
                       "--configuration-sha256", receipt["configuration"]["sha256"]]
    need(launch["command"] == expected_launch, "Changed actual child command")
    result = read(path / "result.json")
    need(receipt["checker_status"] == result.get("status"), "Receipt/result status mismatch")
    return {"id": request["id"], "receipt": receipt, "execution_pin": receipt_pin,
            "result": result, "result_pin": outputs["result.json"], "outputs": outputs,
            "caller_returncode": None if caller is None else caller["returncode"],
            "caller_exit_observed": caller is not None}


def ledger_rows(record):
    p = record["outputs"].get("result.identities.jsonl")
    need(p is not None, "Missing execution-bound identity ledger")
    result = record["result"]
    if "identities" in result:
        need(result["identities"] == p, "Result identity ledger pin differs")
    if "identity_file" in result:
        need(result["identity_file"] == p["path"], "Result identity ledger path differs")
    return [z for _n, z, _raw in json_lines(p["path"])]


def accept(ctx, component, op, group, record):
    if record is None:
        return False
    z, s = record["result"], group["stream"]
    expected = group["expected"]
    start, stop = op["slice"]
    status = z.get("status")
    if status in ("FAIL", "HOLD_CANDIDATE") or "result.candidate.json" in record["outputs"]:
        group["fatal"] = record["id"]
        return False
    allowed = "FROZEN_INPUTS_NOT_VERIFIED" if op["kind"] == "index" else "PASS_CONDITIONAL_ON_RECORDED_COUNTS" if component == "early" else "PASS"
    partial = component == "early" and status in ("CANNOT_CHECK", "PARTIAL") and "checked_ids" in z
    if status != allowed and not partial:
        return False
    receipt = record["receipt"]
    need(receipt["status"] == ("CHECKER_NONZERO_EXIT" if partial else "CHECKER_EXITED_ZERO")
         and (receipt["child_returncode"] != 0 if partial else receipt["child_returncode"] == 0),
         "Semantic result lacks the corresponding actual child exit")
    need(record["caller_returncode"] in ((None, 2) if partial else (None, 0)), "Failed launcher cannot be reused as success")
    if component != "final":
        need(z.get("unit") == s["unit"], "Cross-unit result")
    if component in ("geometry", "bounds"):
        need(z.get("shard") == s["shard"], "Cross-shard result")
    if component == "bounds":
        sha = ctx.recipe["copied_sources"][CHECKERS["bounds"]]["sha256"]
        if op["kind"] == "index":
            need(z["indexer_sha256"] == sha and z["selected"] == s["count"]
                 and z["root"] == str(ctx.data / "namespaces" / s["unit"].lower()), "Stale/incomplete bounds index")
            exact_rows(expected, z["expected"], [("id", "id"), ("ordinal", "ordinal"),
                       ("geometry_sha256", "geometry_sha256"), ("row_sha256", "compact_sha256")])
            need(z["jobs"] == record["outputs"].get("result.jobs.jsonl"), "Unbound bounds jobs file")
            record["sources"] = ctx.used_sources(component, s, z)
            group["index"] = record
            return True
        idx = group["index"]
        need(z["index_sha256"] == idx["result_pin"]["sha256"] and z["verifier_sha256"] == sha, "Stale bounds verifier/index")
        for p in idx["sources"]:
            check_pin(p)
        if op["kind"] == "aggregate":
            need(z["checked"] == s["count"] and z["complete_expected_identities_once"] is True
                 and z["indexer_sha256"] == z["aggregator_sha256"] == sha
                 and z["accepted_verifier_source"] == ctx.recipe["copied_sources"][CHECKERS["bounds"]]
                 and z["aggregator_source"] == ctx.recipe["copied_sources"][CHECKERS["bounds"]]
                 and z["slice_receipts"] == [a["result_pin"] for a in group["accepted"]], "Bounds aggregate lost exact current-source/slice provenance")
            group["aggregate"] = record
            return True
    rows = ledger_rows(record)
    selected = expected[start:stop]
    if component == "early":
        rows, end = early_prefix(z, rows, [r["id"] for r in expected], start, stop)
        selected = expected[start:end]
        meta = ctx.recipe["metadata"]
        need(z["source_manifest"] == meta["source-manifest.json"], "Early manifest binding changed")
        selection = z["required_id_selection"]
        need(all(selection[k] == meta["chosen-terminals.json"][k] for k in ("path", "bytes", "sha256"))
             and selection["required_ids"] == ctx.chosen[EARLY_KEYS[s["unit"]]], "Early required selection changed")
        exact_rows(selected, rows, [("id", "id"), ("ordinal", "ordinal"), ("unit", "unit")])
        for want, row in zip(selected, rows):
            ref = row["certificate"]
            need(ref["path"] == s["compact"] and ref["source_sha256"] == ctx.sources[s["compact"]]["sha256"]
                 and ref["record_sha256"] == want["row_sha256"], "Early original certificate source record changed")
        record["sources"] = ctx.used_sources(component, s, z)
    elif component == "algebra":
        exact_rows(selected, rows, [(k, k) for k in ("id", "ordinal", "unit", "row_sha256", "bare_triple")])
        need(z["slice"] == [start, stop] and z["checked"] == stop - start and z["input_total"] == s["count"]
             and z["source"] == str(ctx.data / s["compact"]), "Wrong algebra range/source")
        need(z["identity_sha256"] == digest(b"".join(encoded(r) + b"\n" for r in rows)), "Algebra ledger digest differs")
        end = stop
    elif component in ("geometry", "final"):
        fields = [(k, k) for k in ("id", "bare_triple", "geometry_sha256")]
        fields += [("row_sha256", "certificate_sha256")] if component == "final" else [("actual_degree", "actual_degree")]
        exact_rows(selected, rows, fields)
        need(z["records" if component == "final" else "selected"] == s["count"], "Incomplete whole binding")
        record["sources"] = ctx.used_sources(component, s, z)
        end = stop
    else:
        exact_rows(selected, rows, [("id", "id"), ("ordinal", "ordinal"), ("geometry_sha256", "geometry_sha256")])
        need(z["slice"] == [start, stop] and z["checked"] == stop - start, "Incomplete bounds slice")
        for row, frozen in zip(rows, group["index"]["result"]["expected"][start:stop]):
            need(row["job_sha256"] == frozen["sha256"] and row["compact_source"]["sha256"] == frozen["compact_sha256"]
                 and [p["identity"] for p in row["proofs"]] == frozen["proof_identities"], "Missing/stale formal proof obligation")
        end = stop
    need(start == group["cursor"], "Duplicate/overlapping successful slice")
    record["accepted_slice"] = [start, end]
    if end > start:
        group["accepted"].append(record)
        group["cursor"] = end
    return not partial


def audit(ctx, component):
    progress = initial_progress(ctx, component)
    for item in ctx.state["attempts"]:
        if item["component"] != component:
            continue
        request_path = ctx.work / "attempts" / (item["id"] + ".json")
        need(item["request"] == pin(request_path), "Changed journal request")
        request = read(request_path)
        need(request["recipe"] == ctx.state["recipe"] and request["id"] == item["id"]
             and request["component"] == component and request["checker"] == CHECKERS[component], "Cross-recipe request")
        op = request["operation"]
        current = operation(ctx, component, progress)
        need(op == current, "Extra, repeated-success, reordered or skipped component operation")
        group = progress[op["stream"]]
        need(request["checker_args"] == checker_arguments(ctx, component, op, group)
             and request["expected_roster_sha256"] == digest(encoded(group["expected"]))
             and request["frozen_roster"] == ctx.state["rosters"][component], "Changed exact requested roster/arguments")
        need(request["command"] == launcher_command(ctx, item["id"], component, request["checker_args"]),
             "Changed requested launcher command")
        expected_inputs = {str(ctx.data / n): {"path": str(ctx.data / n), **ctx.sources[n]}
                           for n in group["stream"]["inputs"]}
        if component == "bounds" and group["index"]:
            expected_inputs.update({p["path"]: p for p in group["index"]["sources"]})
        need(len(request["inputs"]) == len(expected_inputs) and
             {p["path"]: p for p in request["inputs"]} == expected_inputs, "Missing or changed prelaunch source roster")
        for p in request["inputs"]:
            check_pin(p)
        accept(ctx, component, op, group, execution(ctx, request))
    return progress


def pending(progress, component):
    rows = []
    for key, g in progress.items():
        s, cursor = g["stream"], g["cursor"]
        if cursor < s["count"] or (component == "bounds" and g["aggregate"] is None):
            rows.append({"stream": key, "source": s["compact"], "index_pending": component == "bounds" and g["index"] is None,
                         "remaining_slice": [cursor, s["count"]],
                         "remaining_identities": g["expected"][cursor:],
                         "aggregate_pending": component == "bounds" and g["aggregate"] is None,
                         "fatal_attempt": g["fatal"]})
    return rows


def call_launcher(command, stdout, stderr):
    # The existing launcher alone owns child deadlines and process cleanup. A
    # terminal SIGINT reaches it too; defer this parent's interruption until its
    # actual exit is observed instead of abandoning a live launcher.
    interrupted = []
    old = signal.signal(signal.SIGINT, lambda *_: interrupted.append(True))
    try:
        with stdout.open("xb") as out, stderr.open("xb") as err:
            code = subprocess.run(command, stdout=out, stderr=err, check=False).returncode
            return {"returncode": code, "interrupted": bool(interrupted)}
    finally:
        signal.signal(signal.SIGINT, old)


def launcher_command(ctx, identity, component, args):
    return [str(Path(sys.executable).resolve()), "-B", ctx.recipe["launcher"]["path"], "run",
            "--data-root", str(ctx.data), "--work-root", str(ctx.work), "--id", identity,
            "--checker", CHECKERS[component], "--timeout", str(ctx.recipe["settings"]["timeout"]), "--", *args]


def run_component(ctx, component, max_jobs, runner=call_launcher):
    progress = audit(ctx, component)
    launched = 0
    while max_jobs is None or launched < max_jobs:
        op = operation(ctx, component, progress)
        if op is None:
            break
        g = progress[op["stream"]]
        ctx.stable()
        inputs = [ctx.source(name) for name in g["stream"]["inputs"]]
        if component == "bounds" and g["index"]:
            for p in g["index"]["sources"]:
                check_pin(p)
            inputs += g["index"]["sources"]
        inputs = list({p["path"]: p for p in inputs}.values())
        identity = f"component-{len(ctx.state['attempts']) + 1:06d}"
        need(not (ctx.work / identity).exists(), "Fresh execution identity already exists")
        args = checker_arguments(ctx, component, op, g)
        command = launcher_command(ctx, identity, component, args)
        request = {"schema": SCHEMA, "id": identity, "component": component, "operation": op,
                   "recipe": ctx.state["recipe"], "checker": CHECKERS[component], "checker_args": args,
                   "expected_roster_sha256": digest(encoded(g["expected"])), "frozen_roster": ctx.state["rosters"][component],
                   "inputs": inputs, "command": command}
        path = ctx.work / "attempts" / (identity + ".json")
        write(path, request)
        check_pin(request["frozen_roster"])
        ctx.state["attempts"].append({"id": identity, "component": component, "request": pin(path)})
        replace_state(ctx.work, ctx.state)
        outcome = runner(command, path.with_suffix(".stdout.txt"), path.with_suffix(".stderr.txt"))
        rc = outcome["returncode"] if isinstance(outcome, dict) else outcome
        interrupted = isinstance(outcome, dict) and outcome.get("interrupted", False)
        need(type(rc) is int, "Launcher did not return an actual process exit code")
        write(path.with_suffix(".caller.json"), {"request": pin(path), "returncode": rc,
              "actual_launcher_exit_observed": True, "controller_interrupted": interrupted})
        launched += 1
        ctx.stable()
        check_pin(request["frozen_roster"])
        for p in inputs:
            check_pin(p)
        passed = accept(ctx, component, op, g, execution(ctx, request))
        print(json.dumps({"component": component, "id": identity, "operation": op,
                          "cursor": g["cursor"], "launcher_exit": rc, "accepted_complete_requested_step": passed}), flush=True)
        if not passed or interrupted:
            break
    rest = pending(progress, component)
    report = {"schema": SCHEMA, "component": component, "recipe": ctx.state["recipe"],
              "status": "COMPONENT_STEPS_COMPLETE_PENDING_AGGREGATE" if not rest else "PENDING",
              "launched": launched, "remaining_steps": rest, "scope": SCOPE}
    path = fresh_report(ctx.work, component + "-progress", report)
    return {"status": report["status"], "report": pin(path), "remaining_streams": len(rest), "scope": SCOPE}


def aggregate_component(ctx, component, progress):
    rest = pending(progress, component)
    need(not rest, "Component has pending exact identities/index/aggregate steps")
    receipts, roster = [], []
    for stream, g in progress.items():
        seen = set()
        for record in g["accepted"]:
            start, stop = record["accepted_slice"]
            for expected in g["expected"][start:stop]:
                need(expected["ordinal"] not in seen, "Repeated successful identity during aggregate")
                seen.add(expected["ordinal"])
                roster.append({"stream": stream, **expected, "execution_id": record["id"],
                               "result_sha256": record["result_pin"]["sha256"]})
            receipts.append({"execution": record["execution_pin"], "result": record["result_pin"],
                             "accepted_slice": record["accepted_slice"],
                             "caller_exit_observed": record["caller_exit_observed"],
                             "caller_returncode": record["caller_returncode"]})
        need(seen == set(range(g["stream"]["count"])), "Missing literal source ordinal at aggregation")
        if component == "bounds":
            for kind in ("index", "aggregate"):
                r = g[kind]
                receipts.append({"kind": kind, "execution": r["execution_pin"], "result": r["result_pin"]})
    ctx.stable()
    for p in ctx.used.values():
        check_pin(p)
    result = {"schema": SCHEMA, "status": "PASS_COMPONENT_CONDITIONAL_ON_RECORDED_COUNTS_AND_SEPARATE_PREMISES",
              "component": component, "recipe": ctx.state["recipe"], "aggregator": pin(__file__),
              "frozen_roster": ctx.state["rosters"][component],
              "exact_source_identities": roster, "records": len(roster), "streams": list(progress),
              "executions": receipts, "checked_current_sources": ctx.used,
              "all_literal_source_identities_once": True, "scope": SCOPE}
    p = fresh_report(ctx.work, component + "-aggregate", result)
    return {"status": result["status"], "component": component, "records": len(roster), "aggregate": pin(p), "scope": SCOPE}


@contextmanager
def lock(work):
    with plain(plain(work) / "LOCK").open("a") as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Refusal("Another controller owns this work journal") from None
        yield


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="mode", required=True)
    p = commands.add_parser("prepare")
    p.add_argument("--work-root", type=Path, required=True)
    p.add_argument("--data-root", type=Path, required=True)
    p.add_argument("--code-root", type=Path, default=Path(__file__).resolve().parent / "portable-box-code")
    for field in ("source-manifest", "chosen-terminals", "geometry-jobs"):
        p.add_argument("--" + field, type=Path, required=True)
        p.add_argument("--" + field + "-sha256", required=True)
    p.add_argument("--algebra-chunk", type=int, default=8192)
    p.add_argument("--bounds-chunk", type=int, default=4096)
    p.add_argument("--early-chunk", type=int, default=64)
    p.add_argument("--timeout", type=float, default=120)
    p.add_argument("--internal-seconds", type=float, default=100)
    for mode in ("run", "status", "aggregate"):
        q = commands.add_parser(mode)
        q.add_argument("--work-root", type=Path, required=True)
        q.add_argument("--component", choices=COMPONENTS, required=True)
        if mode == "run":
            q.add_argument("--max-jobs", type=int)
    args = parser.parse_args()
    try:
        if args.mode == "prepare":
            result = prepare(args)
        else:
            need(sys.version_info >= (3, 10), "Python 3.10+ required")
            if args.mode == "run":
                need(args.max_jobs is None or args.max_jobs > 0, "max-jobs must be positive")
            with lock(args.work_root):
                ctx = Context(args.work_root)
                if args.mode == "run":
                    result = run_component(ctx, args.component, args.max_jobs)
                else:
                    progress = audit(ctx, args.component)
                    if args.mode == "aggregate":
                        result = aggregate_component(ctx, args.component, progress)
                    else:
                        rest = pending(progress, args.component)
                        path = fresh_report(ctx.work, args.component + "-status", {
                            "schema": SCHEMA, "recipe": ctx.state["recipe"], "component": args.component,
                            "remaining_steps": rest, "scope": SCOPE})
                        result = {"status": "STEPS_COMPLETE" if not rest else "PENDING", "report": pin(path), "remaining_streams": len(rest)}
        print(json.dumps(result, sort_keys=True), flush=True)
        return 0
    except (Refusal, OSError, ValueError, KeyError, TypeError) as error:
        failure = {"schema": SCHEMA, "status": "REFUSED", "mode": args.mode,
                   "component": getattr(args, "component", None), "error": f"{type(error).__name__}: {error}", "scope": SCOPE}
        if args.mode != "prepare" and Path(args.work_root).is_dir():
            try:
                state = read(Path(args.work_root) / "STATE.json")
                failure["recipe"] = state["recipe"]
                failure["attempt_journal_snapshot"] = state
                roster = state.get("rosters", {}).get(args.component)
                if roster:
                    check_pin(roster)
                    failure["exact_identity_roster_requiring_valid_revalidation"] = roster
                else:
                    failure["identity_resolution"] = "Blocked before a source-bound literal roster could be completed; exact recipe sources/selectors remain pending"
            except (OSError, ValueError, KeyError, TypeError):
                failure["identity_resolution"] = "The recipe/journal could not be authenticated; no completion accepted"
            failure["preserved_failure"] = str(fresh_report(Path(args.work_root), "refusal", failure))
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
