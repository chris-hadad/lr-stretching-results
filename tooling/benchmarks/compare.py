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
    from slr_ehrhart import transport, skew_count
    if case['operation'] == 'skew':
        module = skew_count
        path = Path(skew_count.__file__)
        if implementation in ('native_forward', 'native_row_sweep'):
            name = 'skew_forward' if implementation == 'native_forward' else 'skew_row_sweep'
            path = HERE / 'baselines' / (name + '.py')
            spec = importlib.util.spec_from_file_location('frozen_' + name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        outer, inner, content, t = case['args']
        def evaluate():
            if implementation == 'native_forward':
                return module.count(outer, inner, content, t)[0]
            if implementation == 'native_row_sweep':
                return module.strip_kostka([t*x for x in outer], [t*x for x in inner], [t*x for x in content])
            if implementation == 'optimized':
                return module.skew_tableau_count(outer, inner, content, t)
            raise ValueError('invalid skew implementation')
    else:
        module = transport
        path = Path(transport.__file__)
        if implementation == 'baseline':
            path = TOOLING / 'tests/fixtures/transport_before_shared_tools.py'
            spec = importlib.util.spec_from_file_location('slr_ehrhart._benchmark_baseline', path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        elif implementation != 'optimized':
            raise ValueError('invalid table implementation')
        if case['operation'] not in ('transport', 'quotient'):
            raise ValueError('unknown count operation')
        function = module.transport_count if case['operation'] == 'transport' else module.segment_quotient_count
        def evaluate():
            return function(*case['args'])
    started = time.perf_counter()
    value = evaluate()
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
    parser.add_argument('--child', choices=['baseline', 'optimized', 'native_forward', 'native_row_sweep'], help=argparse.SUPPRESS)
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
        implementations = case.get('implementations', ['baseline', 'optimized'])
        if len(implementations) != len(set(implementations)) or 'optimized' not in implementations or len(implementations) < 2:
            raise ValueError('invalid comparison roster')
        records = {name: [] for name in implementations}
        failed = False
        for repetition in range(args.repetitions):
            order = implementations if repetition % 2 == 0 else implementations[::-1]
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
        source_sets = {name: {row['source_sha256'] for row in rows} for name, rows in records.items()}
        if len(values) != 1 or any(len(hashes) != 1 for hashes in source_sets.values()) or len({next(iter(hashes)) for hashes in source_sets.values()}) != len(implementations):
            print(json.dumps({'case': case['id'], 'status': 'disagreement_or_aliased_sources', 'measurements': records}))
            complete = False
            continue
        medians = {implementation: statistics.median(row['count_seconds'] for row in group)
                   for implementation, group in records.items()}
        print(json.dumps({'case': case['id'], 'status': 'agree', 'value': next(iter(values)),
                          'median_count_seconds': medians,
                          'count_ratios_over_optimized': {name: value / medians['optimized'] for name, value in medians.items()},
                          'measurements': records}))
    return 0 if complete else 1


if __name__ == '__main__':
    raise SystemExit(main())
