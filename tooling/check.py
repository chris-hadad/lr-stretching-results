"""Run this publication's explicitly selected small exact checks; no native engines."""
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / 'tests'))


def main():
    names = ['test_strip', 'test_cdagger', 'test_flow_support',
             'test_transport_optimization', 'test_transport', 'test_consumers', 'test_skew_count']
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.testsRun != 75 or result.skipped:
        raise ValueError('the exact expected publication test population was not executed')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
