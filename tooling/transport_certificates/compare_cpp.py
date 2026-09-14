#!/usr/bin/env python3
"""Independently replay every original normal through the C++/GMP recurrence."""

import argparse, json, sys
from fractions import Fraction as F
from pathlib import Path
from process import Runner, install_termination_handlers, write_json, digest, need
from verify import HERE, CERTIFICATE_SHA256, SYSTEMS


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--python-run", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--include-dir", action="append", default=[])
    ap.add_argument("--library-dir", action="append", default=[])
    ap.add_argument("--cxx", default="c++")
    args = ap.parse_args()
    prior = args.python_run.resolve()
    out = args.out.absolute()
    need(
        not out.exists() and not out.is_symlink() and out.parent.is_dir(),
        "Fresh output directory required",
    )
    need(
        out != HERE and HERE not in out.parents,
        "Keep generated outputs outside source module",
    )
    result = json.loads((prior / "RESULT.json").read_text())
    start = json.loads((prior / "START.json").read_text())
    need(
        result["status"] == "PASS_COMPLETE_TRANSPORT_AND_CAPPED_CERTIFICATES"
        and result["certificate_sha256"] == CERTIFICATE_SHA256,
        "Complete current Python verification is required",
    )
    need(
        set(start["sources"]) == {"verify.py", "arithmetic.py", "certificate.json"},
        "Incomplete Python source identity",
    )
    need(
        all(digest(HERE / name) == value for name, value in start["sources"].items()),
        "Python source changed since its verification",
    )
    expected_artifacts = {
        f"{name}-q{q}{suffix}"
        for name, (_, _, qmax, _) in SYSTEMS.items()
        for q in range(1, qmax + 1)
        for suffix in [".json", ".input"]
    }
    need(
        set(result["artifacts"]) == expected_artifacts,
        "Incomplete saved original roster",
    )
    need(
        all(
            digest(prior / name) == value for name, value in result["artifacts"].items()
        ),
        "Saved original input/output bytes changed",
    )
    out.mkdir()
    runner = Runner(out, 360)
    install_termination_handlers(runner)
    write_json(
        out / "START.json",
        {
            "schema": "transport-cap-cpp-comparison-v1",
            "python_result_sha256": digest(prior / "RESULT.json"),
            "sources": {
                name: digest(HERE / name)
                for name in ["compare_cpp.py", "local_values.cpp", "process.py"]
            },
            "native_child_seconds": 60,
            "compile_child_seconds": 120,
            "cumulative_child_seconds": 360,
        },
    )
    binary = out / "local_values"
    flags = [x for p in args.include_dir for x in ["-I", p]] + [
        x for p in args.library_dir for x in ["-L", p]
    ]
    for p in args.library_dir:
        flags += ["-Xlinker", "-rpath", "-Xlinker", str(Path(p).absolute())]
    runner.run(
        "compile",
        [
            args.cxx,
            "-O2",
            "-std=c++17",
            *flags,
            str(HERE / "local_values.cpp"),
            "-lgmpxx",
            "-lgmp",
            "-o",
            str(binary),
        ],
    )
    checked = 0
    for name, (_, _, qmax, _) in SYSTEMS.items():
        for q in range(1, qmax + 1):
            stamp = f"{name}-q{q}"
            expected = json.loads((prior / (stamp + ".json")).read_text())[
                "independent"
            ]
            path = runner.run(
                stamp, [str(binary)], input_path=prior / (stamp + ".input"), deadline=60
            )
            rows = [line.split() for line in path.read_text().splitlines()]
            need(len(rows) == len(expected), "Missing C++ output rows")
            for got, want in zip(rows, expected):
                need(
                    len(got) == 7
                    and got[0] == want["label"]
                    and int(got[1]) == want["index"]
                    and F(got[2]) == F(want["alpha"]),
                    "Independent C++ constant differs",
                )
            checked += len(rows)
    need(
        checked == 16848 and all(job["waited"] for job in runner.jobs),
        "Incomplete comparison or unjoined child",
    )
    write_json(
        out / "RESULT.json",
        {
            "status": "PASS_COMPLETE_CPP_COMPARISON",
            "local_constants": checked,
            "child_seconds": runner.used,
            "children": len(runner.jobs),
            "all_children_waited": True,
        },
    )
    print("PASS_COMPLETE_CPP_COMPARISON", checked, flush=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyboardInterrupt, InterruptedError) as error:
        print("REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
