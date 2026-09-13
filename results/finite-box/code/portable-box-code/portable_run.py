#!/usr/bin/env python3
"""Lower-level portable checker launcher, not a whole-theorem reproduce command.

  python3 -B portable_run.py run --data-root ../data --work-root ../replay \
    --id geometry-u04-000 --checker verify_box_geometry.py -- \
    --root ../data/namespaces/u04 --unit U04 --shard shard-000 --expected-selected 8192

Paths in checker arguments are explicit and resolved from the invoking cwd.
The launcher supplies --output, and supplies a fresh --binary for recount build.
Mutable composition databases must be named explicitly inside --work-root.
Every other output is confined to the new work-root/id directory.

Only two mathematical-module configuration values are set: the CANONICAL
attributes of the copied box_geometry and box_geometry_early modules. The new
configuration, actual child exit/cleanup, code hashes and declared file inputs
are recorded. No filesystem API is patched and no historical receipt is edited.
Input artifact sequencing, indirect-reference closure and whole-roster theorem
acceptance remain obligations of a future portable replay controller.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import re
import runpy
import signal
import subprocess
import sys
import time


CODE = Path(__file__).resolve().parent
SCHEMA = "portable-box-execution-v1"
CHECKERS = {
    "verify_box_geometry.py": {"commands": (), "options": "root unit shard expected-selected"},
    "verify_box_algebra.py": {"commands": (), "options": "input unit start stop expected-total"},
    "verify_box_bounds.py": {"commands": ("index", "verify", "aggregate"),
        "options": "root unit shard expected-selected index index-sha256 start stop results accepted-verifier-source accepted-verifier-sha256 max-seconds"},
    "verify_box_composition.py": {"commands": ("freeze", "index", "seal", "verify", "requirements", "aggregate"),
        "options": "root manifest database snapshot source gate start limit reports acceptances phase aggregates budget-seconds"},
    "verify_early_terminals.py": {"commands": (),
        "options": "root unit source-manifest source-manifest-sha256 start stop required-ids required-ids-sha256 max-seconds"},
    "verify_box_final_bindings.py": {"commands": (), "options": "restored source-manifest source-manifest-sha256"},
    "recount_records.py": {"commands": ("build", "index", "run", "aggregate"),
        "options": "root unit shard input geometry-identities manifest build cpp-source compiler start limit site node-ms max-states budget-seconds resume-from reports"},
}
MULTI = {"--results", "--reports", "--acceptances", "--aggregates", "--geometry-identities", "--resume-from"}
ARTIFACT_FILES = {"--index", "--manifest", "--snapshot", "--build", *MULTI}
DATA_FILES = {"--input", "--source-manifest", "--required-ids"}
MASKS = {6: "6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0",
         7: "bb595b3914ce05105743e9386f2cc64a4d2ae2d59df0d340c3221b8b74d7cd9c"}
GEOMETRY_USERS = {"verify_box_geometry.py", "verify_early_terminals.py", "verify_box_final_bindings.py"}


class LaunchError(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise LaunchError(message)


def decode(raw):
    def unique(items):
        result = {}
        for key, value in items:
            need(key not in result, "Duplicate JSON field")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def save(path, value):
    with Path(path).open("xb") as stream:
        stream.write(encoded(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def utc():
    return datetime.now(timezone.utc).isoformat()


def no_links(path):
    path = Path(path).absolute()
    need(not any(p.is_symlink() for p in (path, *path.parents)), "Symlink path is not a portable declared source/output")
    return path.resolve()


def pin(path):
    path = no_links(path)
    before = path.stat()
    need(path.is_file(), "Declared input is not a regular file")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while data := stream.read(1024 * 1024):
            h.update(data)
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), "File changed while hashing")
    return {"path": str(path), "bytes": before.st_size, "sha256": h.hexdigest()}


def check_pin(value):
    need(pin(value["path"]) == value, "Declared source/input changed: " + value["path"])


def relative(name):
    need(isinstance(name, str) and name and "\\" not in name and ":" not in name
         and all(ord(c) >= 32 and ord(c) != 127 for c in name), "Invalid portable relative source name")
    p = Path(name)
    need(p.parts and not p.is_absolute() and str(p) == name and all(x not in (".", "..") for x in p.parts), "Escaping/noncanonical source name")
    return name


def read_copy_map():
    path = CODE / "SOURCE-MAP.json"
    identity = pin(path)
    table = decode(path.read_bytes())
    need(table["schema"] == "portable-box-source-copies-v1", "Unknown source-copy map")
    files = {}
    for record in table["copies"]:
        name = relative(record["path"])
        need(name not in files, "Duplicate source-copy identity")
        current = pin(CODE / name)
        need(current["bytes"] == record["portable_bytes"] and current["sha256"] == record["portable_sha256"], "Copied checker/dependency differs from its exact source map")
        files[name] = current
    need(set(CHECKERS) <= set(files) and {"box_geometry.py", "box_geometry_early.py", "v2_independent_hive_recount.cpp"} <= set(files),
         "Source-copy map omitted a required checker/helper")
    return identity, files


def portable_manifest(path, expected_sha, data_root):
    identity = pin(path)
    need(re.fullmatch(r"[0-9a-f]{64}", expected_sha or "") and identity["sha256"] == expected_sha, "Portable source-manifest hash differs")
    document = decode(Path(path).read_bytes())
    need(isinstance(document, dict) and document.get("schema") == "early-input-manifest-v1"
         and isinstance(document.get("files"), list), "Historical absolute MEMBERS is not a portable relative manifest")
    seen = set()
    for row in document["files"]:
        need(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"}, "Portable manifest entry must contain exactly path/bytes/sha256")
        name = relative(row["path"])
        need(name not in seen, "Duplicate portable source path")
        seen.add(name)
        need(type(row["bytes"]) is int and row["bytes"] >= 0 and isinstance(row["sha256"], str)
             and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]), "Malformed portable byte declaration")
        need((data_root / name).is_relative_to(data_root), "Portable manifest escaped data root")
    check_pin(identity)
    return identity


def parse_checker_args(checker, words):
    need(checker in CHECKERS and isinstance(words, list) and all(isinstance(x, str) and "\0" not in x for x in words), "Checker is not allowlisted")
    spec = CHECKERS[checker]
    allowed = {"--" + name for name in spec["options"].split()}
    position, command, options, order, help_only = 0, None, {}, [], False
    if words and not words[0].startswith("-"):
        need(words[0] in spec["commands"], "Unsupported checker command")
        command, position = words[0], 1
    while position < len(words):
        flag = words[position]
        if flag in ("--help", "-h"):
            need(not help_only, "Duplicate help option")
            help_only = True
            position += 1
            continue
        need(flag in allowed and flag not in options, "Unknown, duplicate, abbreviated or output-overriding checker option: " + flag)
        position += 1
        if flag in MULTI:
            end = position
            while end < len(words) and not words[end].startswith("--") and words[end] != "-h":
                end += 1
            values, position = words[position:end], end
        else:
            need(position < len(words) and not words[position].startswith("--"), "Missing checker option value: " + flag)
            values = [words[position]]
            position += 1
        options[flag] = values
        order.append(flag)
    need(help_only or not spec["commands"] or command in spec["commands"], "Explicit checker command required")
    return command, options, order, help_only


def path_argument(value, cwd, roots, *, directory=False, exists=True):
    path = no_links(Path(value) if Path(value).is_absolute() else cwd / value)
    need(any(path.is_relative_to(root) for root in roots), "CLI path is outside the portable data/code/work roots")
    if exists:
        need(path.is_dir() if directory else path.is_file(), "Declared input path is absent or has the wrong type: " + str(path))
    return path


def prepare_arguments(checker, words, data_root, work_root, output_root, cwd):
    command, options, order, help_only = parse_checker_args(checker, words)
    inputs, mutable = {}, []
    resolved = {key: list(value) for key, value in options.items()}
    unit = options.get("--unit", [None])[0]
    for flag in ("--root", "--restored"):
        if flag not in options:
            continue
        root = path_argument(options[flag][0], cwd, [data_root], directory=True)
        if checker == "verify_box_composition.py":
            expected = data_root / "namespaces"
        elif checker in ("verify_early_terminals.py", "verify_box_final_bindings.py"):
            expected = data_root
        else:
            need(unit is not None and re.fullmatch(r"U(?:0[2-9]|1[012])", unit), "A root-based namespace command needs its explicit unit")
            expected = data_root / "namespaces" / unit.lower()
        need(root == expected, "Checker root does not match the single declared portable data root")
        resolved[flag] = [str(root)]
    for flag, values in options.items():
        if flag in ("--root", "--restored"):
            continue
        if checker == "recount_records.py" and command == "index" and flag == "--input":
            need("--root" in resolved, "Relative recount input needs an explicit unit root")
            name = relative(values[0])
            actual = path_argument(str(Path(resolved["--root"][0]) / name), cwd, [data_root])
            inputs[str(actual)] = pin(actual)
            continue  # This option is a literal relative selector, not an absolute filename.
        if checker == "verify_box_composition.py" and flag == "--source":
            name = relative(values[0])
            actual = path_argument(str(data_root / "namespaces" / name), cwd, [data_root])
            inputs[str(actual)] = pin(actual)
        elif flag in ARTIFACT_FILES:
            resolved[flag] = []
            for value in values:
                actual = path_argument(value, cwd, [work_root])
                inputs[str(actual)] = pin(actual)
                resolved[flag].append(str(actual))
        elif flag in DATA_FILES:
            actual = path_argument(values[0], cwd, [data_root, work_root])
            inputs[str(actual)] = pin(actual)
            resolved[flag] = [str(actual)]
        elif flag == "--accepted-verifier-source":
            actual = path_argument(values[0], cwd, [CODE])
            need(actual.name in ("verify_box_bounds.py", "verify_box_bounds.pre_r2_10d71fc01a6c5f31.py"), "Unapproved bound-verifier source")
            inputs[str(actual)] = pin(actual)
            resolved[flag] = [str(actual)]
        elif flag == "--cpp-source":
            actual = path_argument(values[0], cwd, [CODE])
            need(actual == CODE / "v2_independent_hive_recount.cpp", "Only the copied v2 recount source is allowed")
            inputs[str(actual)] = pin(actual)
            resolved[flag] = [str(actual)]
        elif flag == "--compiler":
            # System compiler aliases are resolved explicitly; this does not
            # create aliases or relax data/code path handling.
            actual = (Path(values[0]) if Path(values[0]).is_absolute() else cwd / values[0]).resolve(strict=True)
            need(actual.is_file() and os.access(actual, os.X_OK), "Compiler must be an explicit installed executable path")
            inputs[str(actual)] = pin(actual)
            resolved[flag] = [str(actual)]
        elif flag == "--database":
            actual = path_argument(values[0], cwd, [work_root], exists=False)
            need(actual.parent.is_dir() and not actual.is_relative_to(data_root) and not actual.is_relative_to(CODE), "Database must be an explicit work artifact")
            need(actual.suffix in (".sqlite", ".db"), "Mutable database must have an explicit SQLite filename, not a receipt/output name")
            if actual.exists():
                with actual.open("rb") as stream:
                    need(stream.read(16) == b"SQLite format 3\0", "Existing mutable file is not a SQLite database")
            resolved[flag] = [str(actual)]
            mutable.extend([str(actual) + suffix for suffix in ("", "-journal", "-wal", "-shm")])
    if not help_only:
        if checker in ("verify_box_geometry.py", "verify_early_terminals.py", "verify_box_composition.py"):
            need("--root" in resolved, "Checker requires its explicit portable root")
        if checker == "verify_box_final_bindings.py":
            need("--restored" in resolved, "Final binding requires --restored equal to the portable data root")
        if checker in ("verify_early_terminals.py", "verify_box_final_bindings.py"):
            need("--source-manifest" in resolved and "--source-manifest-sha256" in resolved, "Explicit relative source manifest and hash are required")
            identity = portable_manifest(resolved["--source-manifest"][0], resolved["--source-manifest-sha256"][0], data_root)
            inputs[identity["path"]] = identity
        if checker == "recount_records.py" and command == "build":
            need("--cpp-source" in resolved and "--compiler" in resolved, "Portable recount build requires explicit copied v2 source and installed compiler")
    final = [command] if command is not None else []
    for flag in order:
        final += [flag, *resolved[flag]]
    if help_only:
        final.append("--help")
    if checker == "recount_records.py" and command == "build" and not help_only:
        final += ["--binary", str(output_root / "recount")]
    final += ["--output", str(output_root / "result.json")]
    return {"argv": final, "command": command, "help_only": help_only,
            "declared_inputs": list(inputs.values()), "mutable_paths": mutable}


def geometry_configuration(data_root, checker, help_only):
    base = data_root / "namespaces" / "base"
    need(base.is_dir(), "Portable data root lacks namespaces/base")
    masks = []
    if checker in GEOMETRY_USERS and not help_only:
        for rank, expected in MASKS.items():
            value = pin(base / f"methods/frontier-025-2026-09-10/science/results/F025-MASK-R{rank}-001.json")
            need(value["sha256"] == expected, "Portable mask table differs from the exact previously accepted source bytes")
            masks.append(value)
    return {"data_root": str(data_root), "box_geometry.CANONICAL": str(base), "box_geometry_early.CANONICAL": str(base),
            "mask_inputs": masks, "mask_validation": "exact_source_bytes" if masks else "not_used_by_this_command_or_help_only",
            "upstream_theorem_status_inferred": False}


def configure_modules(configuration):
    if str(CODE) not in sys.path:
        sys.path.insert(0, str(CODE))
    G = importlib.import_module("box_geometry")
    G_early = importlib.import_module("box_geometry_early")
    need(Path(G.__file__).resolve() == CODE / "box_geometry.py"
         and Path(G_early.__file__).resolve() == CODE / "box_geometry_early.py", "Geometry import escaped the copied code directory")
    G.CANONICAL = Path(configuration["box_geometry.CANONICAL"])
    G_early.CANONICAL = Path(configuration["box_geometry_early.CANONICAL"])
    return {"box_geometry.CANONICAL": str(G.CANONICAL), "box_geometry_early.CANONICAL": str(G_early.CANONICAL)}


def child_main(path, expected_sha):
    identity = pin(path)
    need(identity["sha256"] == expected_sha, "Frozen child configuration changed")
    config = decode(Path(path).read_bytes())
    need(config["schema"] == SCHEMA and config["checker"] in CHECKERS, "Unallowlisted child request")
    for value in config["fixed_inputs"]:
        check_pin(value)
    source_map, code = read_copy_map()
    need(source_map == config["source_map"] and code == config["copied_sources"], "Child source copies changed")
    expected = geometry_configuration(Path(config["data_root"]), config["checker"], config["help_only"])
    need(expected == config["geometry_configuration"], "Child data-root configuration changed")
    applied = configure_modules(expected)
    output_root = Path(config["output_root"])
    need(output_root == Path(config["work_root"]) / config["id"] and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", config["id"]),
         "Child execution/output identity changed")
    prepared = prepare_arguments(config["checker"], config["requested_checker_args"], Path(config["data_root"]),
                                 Path(config["work_root"]), output_root, Path(config["invocation_cwd"]))
    need(prepared["argv"] == config["checker_argv"] and prepared["help_only"] == config["help_only"]
         and prepared["mutable_paths"] == config["mutable_paths"], "Child arguments differ from the explicit frozen request")
    need(path.parent.resolve() == output_root and not (output_root / "result.json").exists(), "Child output is not fresh")
    save(output_root / "APPLIED-CONFIGURATION.json", {"schema": SCHEMA, "configuration": identity,
                                                     "applied": applied, "pid": os.getpid(), "before_mathematical_calls": True})
    sys.argv = [str(CODE / config["checker"]), *config["checker_argv"]]
    runpy.run_path(str(CODE / config["checker"]), run_name="__main__")
    return 0


def group_alive(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False


def supervise(command, cwd, stdout_path, stderr_path, timeout, launch_path):
    """Only the exact newly owned process group is terminated and waited."""
    need(os.name == "posix" and math.isfinite(timeout) and 0 < timeout <= 120, "A POSIX host and a child deadline of at most 120 seconds are required")
    started, process, disposition, interrupted, error_detail = time.monotonic(), None, "not_launched", False, None
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env.update(PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
               VECLIB_MAXIMUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
    try:
        with Path(stdout_path).open("xb") as out, Path(stderr_path).open("xb") as err:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdout=out, stderr=err, start_new_session=True)
            save(launch_path, {"pid": process.pid, "pgid": process.pid, "started_utc": utc(), "command": command})
            try:
                process.wait(timeout=timeout)
                disposition = "exited"
            except subprocess.TimeoutExpired:
                disposition = "timeout"
            except KeyboardInterrupt:
                disposition, interrupted = "interrupted", True
    except (OSError, ValueError) as error:
        disposition = "launch_error" if process is None else "supervisor_error"
        error_detail = f"{type(error).__name__}: {error}"
    finally:
        if process is not None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=.5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    error_detail = "Owned child did not reap after SIGKILL"
            # A checker may have left its own compiler/counter descendant.
            if group_alive(process.pid):
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            deadline = time.monotonic() + 1
            while group_alive(process.pid) and time.monotonic() < deadline:
                time.sleep(.02)
            cleanup = not group_alive(process.pid)
        else:
            cleanup = True
    return {"disposition": disposition, "pid": process.pid if process else None, "pgid": process.pid if process else None,
            "child_returncode": process.returncode if process else None, "cleanup_verified": cleanup,
            "elapsed_seconds": round(time.monotonic() - started, 6), "interrupted": interrupted, "supervisor_error": error_detail}


def run(args):
    need(args.checker in CHECKERS and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", args.id or "") and args.id not in (".", ".."), "Invalid checker or new execution identity")
    need(math.isfinite(args.timeout) and 0 < args.timeout <= 120, "Child timeout must be at most 120 seconds")
    data_root, work_root = no_links(args.data_root), no_links(args.work_root)
    need(data_root.is_dir() and (data_root / "namespaces" / "base").is_dir(), "Expected portable data/namespaces/base layout")
    need(not work_root.is_relative_to(data_root) and not work_root.is_relative_to(CODE), "Work outputs must be outside data and copied source directories")
    work_root.mkdir(parents=True, exist_ok=True)
    output_root = work_root / args.id
    need(not output_root.exists(), "Execution ID already exists; use a new ID, never overwrite an old receipt")
    words = args.checker_args[1:] if args.checker_args[:1] == ["--"] else args.checker_args
    source_map, sources = read_copy_map()
    prepared = prepare_arguments(args.checker, words, data_root, work_root, output_root, Path.cwd().resolve())
    geometry = geometry_configuration(data_root, args.checker, prepared["help_only"])
    fixed = {v["path"]: v for v in [source_map, *sources.values(), pin(__file__), pin(Path(sys.executable).resolve()),
                                    *prepared["declared_inputs"], *geometry["mask_inputs"]]}
    output_root.mkdir()
    mutable_before = {p: pin(p) if Path(p).exists() else None for p in prepared["mutable_paths"]}
    config = {"schema": SCHEMA, "id": args.id, "checker": args.checker, "data_root": str(data_root), "work_root": str(work_root),
              "output_root": str(output_root), "requested_checker_args": words, "checker_argv": prepared["argv"],
              "invocation_cwd": str(Path.cwd().resolve()),
              "command": prepared["command"], "help_only": prepared["help_only"], "timeout_seconds": args.timeout,
              "source_map": source_map, "copied_sources": sources, "geometry_configuration": geometry,
              "fixed_inputs": list(fixed.values()), "mutable_paths": prepared["mutable_paths"], "mutable_before": mutable_before,
              "historical_receipts_rewritten": False, "whole_theorem_accepted": False, "created_utc": utc()}
    config_path = output_root / "CONFIGURATION.json"
    save(config_path, config)
    cp = pin(config_path)
    command = [str(Path(sys.executable).resolve()), "-I", "-S", "-B", str(Path(__file__).resolve()),
               "_child", "--configuration", str(config_path), "--configuration-sha256", cp["sha256"]]
    outcome = supervise(command, output_root, output_root / "stdout.txt", output_root / "stderr.txt", args.timeout, output_root / "LAUNCH.json")
    stable, errors = True, []
    for value in [cp, *fixed.values()]:
        try:
            check_pin(value)
        except (OSError, ValueError) as error:
            stable = False
            errors.append(str(error))
    outputs = []
    for path in sorted(output_root.iterdir()):
        if path.is_file() and path.name != "EXECUTION.json":
            outputs.append(pin(path))
    result_path = output_root / "result.json"
    semantic = None
    if result_path.exists():
        try:
            semantic = decode(result_path.read_bytes()).get("status")
        except (OSError, ValueError, AttributeError):
            semantic = "INVALID_RESULT_JSON"
    clean = outcome["cleanup_verified"] and stable
    if not clean:
        status = "INVALID_EXECUTION"
    elif outcome["disposition"] != "exited":
        status = "PARTIAL_" + outcome["disposition"].upper()
    elif outcome["child_returncode"] != 0:
        status = "CHECKER_NONZERO_EXIT"
    elif prepared["help_only"]:
        status = "HELP_ONLY"
    elif semantic is None or semantic == "INVALID_RESULT_JSON":
        status = "MISSING_OR_INVALID_CHECKER_RESULT"
    else:
        status = "CHECKER_EXITED_ZERO"
    record = {"schema": SCHEMA, "status": status, "configuration": cp, "checker": args.checker,
              "geometry_configuration": geometry, "checker_status": semantic, **outcome,
              "fixed_inputs_unchanged": stable, "source_errors": errors, "outputs": outputs,
              "mutable_after": {p: pin(p) if Path(p).exists() else None for p in prepared["mutable_paths"]},
              "ended_utc": utc(), "whole_theorem_accepted": False, "historical_receipts_rewritten": False,
              "scope": "One newly executed copied checker with explicit data-root configuration; its own mathematical predicate and remaining premises still govern."}
    save(output_root / "EXECUTION.json", record)
    print(json.dumps({"status": status, "checker_status": semantic, "execution": str(output_root / "EXECUTION.json"),
                      "child_returncode": outcome["child_returncode"], "cleanup_verified": outcome["cleanup_verified"],
                      "whole_theorem_accepted": False}), flush=True)
    return 0 if status in ("CHECKER_EXITED_ZERO", "HELP_ONLY") else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="mode", required=True)
    parent = commands.add_parser("run")
    parent.add_argument("--data-root", type=Path, required=True)
    parent.add_argument("--work-root", type=Path, required=True)
    parent.add_argument("--id", required=True)
    parent.add_argument("--checker", choices=CHECKERS, required=True)
    parent.add_argument("--timeout", type=float, default=120)
    parent.add_argument("checker_args", nargs=argparse.REMAINDER)
    child = commands.add_parser("_child", help=argparse.SUPPRESS)
    child.add_argument("--configuration", type=Path, required=True)
    child.add_argument("--configuration-sha256", required=True)
    args = parser.parse_args()
    try:
        return child_main(args.configuration, args.configuration_sha256) if args.mode == "_child" else run(args)
    except (LaunchError, OSError, ValueError, KeyError, TypeError) as error:
        status = "CHILD_EXCEPTION" if args.mode == "_child" else "LAUNCH_REFUSED"
        print(json.dumps({"status": status, "error": f"{type(error).__name__}: {error}", "whole_theorem_accepted": False}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
