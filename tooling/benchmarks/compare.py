"""Reproduce exact paired counts on the bundled inputs, one bounded child at a time."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
TOOLING = HERE.parent
sys.path.insert(0, str(TOOLING))


def child(case, implementation):
    from slr_ehrhart import transport
    module = transport
    path = Path(transport.__file__)
    if implementation == 'baseline':
        path = TOOLING / 'tests/fixtures/transport_before_shared_tools.py'
        spec = importlib.util.spec_from_file_location('slr_ehrhart._benchmark_baseline', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    function = module.transport_count if case['operation'] == 'transport' else module.segment_quotient_count
    started = time.perf_counter()
    value = function(*case['args'])
    elapsed = time.perf_counter() - started
    if type(value) is not int:
        raise ValueError('exact integer count required')
    print(json.dumps({'case': case['id'], 'implementation': implementation, 'value': str(value),
                      'count_seconds': elapsed, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}))


def main():
    cases = json.loads((HERE / 'cases.json').read_text())
    by_id = {case['id']: case for case in cases}
    if len(by_id) != len(cases):
        raise ValueError('duplicate bundled case identity')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=sorted(by_id))
    parser.add_argument('--repetitions', type=int, default=1)
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--child', choices=['baseline', 'optimized'], help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not 1 <= args.repetitions <= 10 or not 0 < args.timeout <= 120:
        parser.error('repetitions must be 1..10 and child timeout in (0,120] seconds')
    if args.child:
        if not args.case:
            parser.error('a child requires one case')
        child(by_id[args.case], args.child)
        return 0
    selected = [by_id[args.case]] if args.case else cases
    complete = True
    for case in selected:
        records = {'baseline': [], 'optimized': []}
        failed = False
        for repetition in range(args.repetitions):
            order = ['baseline', 'optimized'] if repetition % 2 == 0 else ['optimized', 'baseline']
            for implementation in order:
                started = time.perf_counter()
                command = [sys.executable, '-B', str(Path(__file__).resolve()), '--child', implementation, '--case', case['id']]
                try:
                    proc = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout, check=True)
                    row = json.loads(proc.stdout)
                    if row['case'] != case['id'] or row['implementation'] != implementation:
                        raise ValueError('child identity mismatch')
                    row['whole_child_seconds'] = time.perf_counter() - started
                    records[implementation].append(row)
                except (subprocess.SubprocessError, ValueError, KeyError) as error:
                    print(json.dumps({'case': case['id'], 'implementation': implementation,
                                      'status': type(error).__name__, 'count': None}))
                    failed = True
                    complete = False
                    break
            if failed:
                break
        if failed:
            continue
        values = {row['value'] for group in records.values() for row in group}
        if len(values) != 1 or {row['source_sha256'] for row in records['baseline']} == {row['source_sha256'] for row in records['optimized']}:
            print(json.dumps({'case': case['id'], 'status': 'disagreement_or_aliased_sources', 'measurements': records}))
            complete = False
            continue
        medians = {implementation: statistics.median(row['count_seconds'] for row in group)
                   for implementation, group in records.items()}
        print(json.dumps({'case': case['id'], 'status': 'agree', 'value': next(iter(values)),
                          'median_count_seconds': medians,
                          'count_ratio_baseline_over_optimized': medians['baseline'] / medians['optimized'],
                          'measurements': records}))
    return 0 if complete else 1


if __name__ == '__main__':
    raise SystemExit(main())
