"""Optional bounded controls for the unchanged kernel; compilation is external."""
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys

ID = re.compile(r"[A-Za-z0-9_.:-]{1,160}\Z")
DECIMAL = re.compile(r"(0|[1-9][0-9]*)\Z")
REFUSALS = {"REFUSED_INPUT", "REFUSED_OVERFLOW", "REFUSED_WORK", "REFUSED_TIME",
            "REFUSED_DEPTH", "REFUSED_MEMORY", "REFUSED_INTERNAL"}

def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("integer outside protocol range")
    return value

def request(identity, bounds, rows, *, max_states=100000, milliseconds=1000):
    if not isinstance(identity, str) or not ID.fullmatch(identity):
        raise ValueError("invalid protocol identity")
    n, m = len(bounds), len(rows)
    integer(n, 0, 64)
    integer(m, 0, 10000)
    integer(max_states, 1, 2**63-1)
    integer(milliseconds, 1, 110000)
    lines = [f"RECOUNT1 {identity} {n} {m} {max_states} {milliseconds}"]
    for pair in bounds:
        if len(pair) != 2:
            raise ValueError("bound pair required")
        lo, hi = (integer(x, -2**63, 2**63-1) for x in pair)
        if lo > hi:
            raise ValueError("reversed bounds")
        lines.append(f"{lo} {hi}")
    for row in rows:
        if len(row) != n+1:
            raise ValueError("complete row dimension differs from bounds")
        lines.append(" ".join(str(integer(x, -2**63, 2**63-1)) for x in row))
    return "\n".join(lines) + "\n"

def parse_responses(raw, identities):
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate expected identity")
    lines = raw.splitlines()
    if len(lines) != len(identities):
        raise ValueError("missing, extra or blank kernel response")
    responses = []
    for line, identity in zip(lines, identities):
        row = json.loads(line)
        if not isinstance(row, dict) or row.get("id") != identity:
            raise ValueError("kernel response identity mismatch")
        status, count = row.get("status"), row.get("count")
        if status == "complete":
            if not isinstance(count, str) or not DECIMAL.fullmatch(count):
                raise ValueError("complete result needs an exact nonnegative decimal count")
            if int(count) > 2**128-1:
                raise ValueError("count exceeds kernel arithmetic range")
        elif status not in REFUSALS or count is not None:
            raise ValueError("unknown status or numerical refusal")
        for field in ("visited_states", "row_work", "memo_hits"):
            integer(row.get(field), 0, 2**64-1)
        elapsed = row.get("elapsed_seconds")
        if type(elapsed) not in (int, float) or not 0 <= elapsed < float("inf"):
            raise ValueError("invalid elapsed time")
        responses.append(row)
    return responses

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    args = parser.parse_args(argv)
    binary = args.binary.resolve(strict=True)
    if not binary.is_file():
        raise ValueError("binary must be a regular file")
    cases = [
        ("interval", [(0, 3)], [[0, 1], [3, -1]], 4, 100000),
        ("triangle", [(0, 2), (0, 2)], [[2, -1, -1]], 6, 100000),
        ("negative-lower", [(-2, 3)], [[1, -2]], 3, 100000),
        ("work-refusal", [(0, 2), (0, 2)], [[2, -1, -1]], None, 1),
    ]
    payload = "".join(request(identity, bounds, rows, max_states=cap)
                      for identity, bounds, rows, _, cap in cases)
    # subprocess.run kills and waits for this direct, childless kernel on timeout.
    try:
        completed = subprocess.run([str(binary)], input=payload, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    except subprocess.TimeoutExpired as exc:
        for name, raw in (("stdout", exc.stdout), ("stderr", exc.stderr)):
            if raw:
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", errors="replace")
                print(json.dumps({"status": "TIMEOUT_RAW", "stream": name, "raw": raw}), flush=True)
        print(json.dumps({"status": "incomplete", "reason": "parent timeout; child killed and waited"}))
        return 2
    # Preserve every raw response in caller output before comparisons.
    print(completed.stdout, end="", flush=True)
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr, flush=True)
    if completed.returncode != 0 or completed.stderr:
        raise ValueError("kernel exit or stderr is not clean")
    results = parse_responses(completed.stdout, [case[0] for case in cases])
    for case, row in zip(cases, results):
        if case[3] is None:
            if row["status"] != "REFUSED_WORK" or row["count"] is not None:
                raise ValueError("expected explicit work refusal")
        elif row["status"] != "complete" or int(row["count"]) != case[3]:
            raise ValueError("complete control count mismatch: " + case[0])
    print(json.dumps({"status": "complete", "scope": "three tiny scalar controls and one refusal"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

