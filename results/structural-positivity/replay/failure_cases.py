"""Targeted failure fixtures for the public structural replay.

Run separately from reproduce.py. All changes are in-memory; source data and
proof files remain unchanged. Temporary JSON syntax fixtures use no files.
"""
from copy import deepcopy
import json
from pathlib import Path
import time

from exact import CheckError
import reproduce as r


def main():
    started = time.monotonic()
    passed = []

    def refuses(label, call):
        try:
            call()
        except (CheckError, OSError):
            passed.append(label)
            return
        raise RuntimeError(f"Did not refuse: {label}")

    g = r.decode(r.HERE / "data/gap-three.json")
    t = r.decode(r.HERE / "data/transport.json")
    refuses("slope-three below stated rank", lambda: r.two_row_polynomial([1] * 5, 3))
    refuses("unsupported slope", lambda: r.two_row_polynomial([1] * 8, 4))
    refuses("zero weight", lambda: r.two_row_polynomial([0, 1, 1, 1, 1], 2))
    refuses("inexact weight", lambda: r.two_row_polynomial([1.0, 1, 1, 1, 1], 2))
    refuses("boolean weight", lambda: r.two_row_polynomial([True, 1, 1, 1, 1], 2))
    refuses("negative stretch", lambda: r.direct_character_count([1] * 6, 3, -1))
    bad = deepcopy(g)
    bad["parents"].pop()
    refuses("missing gap-three parent", lambda: r.check_gap(bad))
    bad = deepcopy(g)
    bad["parents"][0]["positive_counts"][-1] = deepcopy(bad["parents"][0]["positive_counts"][0])
    refuses("duplicate gap-three site replacing a hold", lambda: r.check_gap(bad))
    bad = deepcopy(g)
    bad["parents"][0]["positive_counts"][-1]["value"] = str(int(bad["parents"][0]["positive_counts"][-1]["value"]) + 1)
    refuses("wrong unused gap-three hold", lambda: r.check_gap(bad))
    bad = deepcopy(g)
    bad["parents"][0]["positive_counts"][0]["value"] = 132.0
    refuses("floating-point count", lambda: r.check_gap(bad))
    bad = deepcopy(t)
    bad["parents"][0]["counts"].pop(0)
    refuses("missing transport zero grade", lambda: r.check_transport(bad))
    bad = deepcopy(t)
    bad["parents"][1] = deepcopy(bad["parents"][0])
    refuses("duplicate transport endpoint", lambda: r.check_transport(bad))
    bad = deepcopy(t)
    bad["parents"][0]["strict_grade_seven_witness"][0][0] -= 1
    refuses("wrong strict-interior witness margin", lambda: r.check_transport(bad))
    bad = deepcopy(t)
    bad["parents"][0]["counts"][-1]["value"] = str(int(bad["parents"][0]["counts"][-1]["value"]) + 1)
    refuses("wrong unused transport hold", lambda: r.check_transport(bad))
    # This path is a child of a regular file, so it cannot resolve to a real data directory.
    refuses("missing count inputs", lambda: r.authenticate("transport", Path(__file__) / "absent"))
    print(json.dumps({"status": "PASS", "targeted_refusals": passed,
                      "elapsed_seconds": time.monotonic() - started}, indent=2))


if __name__ == "__main__":
    main()
