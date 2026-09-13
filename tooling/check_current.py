"""Run exact selected test populations; no subprocesses, engines or writes."""
from pathlib import Path
import argparse
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "tests"))

POPULATIONS = {
    "test_current_contracts": 12,
    "test_rank6_split": 6,
    "test_rank8_clipped": 8,
    "test_two_widths": 5,
    "test_matrix_api": 19,
    "test_rectangular_api": 10,
}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-controls", action="store_true",
                        help="also run all 48 selected maintained mathematical controls")
    args = parser.parse_args(argv)
    names = list(POPULATIONS) if args.research_controls else ["test_current_contracts"]
    suite = unittest.TestSuite()
    for name in names:
        part = unittest.defaultTestLoader.loadTestsFromName(name)
        if part.countTestCases() != POPULATIONS[name]:
            raise ValueError("test population changed or failed to import: " + name)
        suite.addTests(part)
    expected = sum(POPULATIONS[name] for name in names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.testsRun != expected or result.skipped:
        raise ValueError("the complete selected test population was not executed")
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())

