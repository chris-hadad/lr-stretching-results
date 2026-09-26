#!/usr/bin/env python3
"""Small independent integer table controls and deliberate incomplete-input tests."""
import argparse
from copy import deepcopy
from functools import lru_cache
from itertools import permutations
import json
import os
from pathlib import Path
import signal
import sys
import time

import fresh_counts as fc
import gap_model as gm
import transport_math as tm


def direct_tables(rows, columns):
    """Literal bounded row enumeration, independent of both production recurrences."""
    @lru_cache(None)
    def count(left_rows, left_columns):
        if not left_rows:
            return int(not any(left_columns))
        if len(left_rows) == 1:
            return int(sum(left_columns) == left_rows[0] and min(left_columns, default=0) >= 0)
        total = 0
        def fill(j, remaining, next_columns):
            nonlocal total
            if j == len(left_columns):
                if remaining == 0:
                    total += count(left_rows[1:], tuple(next_columns))
                return
            for value in range(min(remaining, left_columns[j]) + 1):
                fill(j + 1, remaining - value, next_columns + [left_columns[j] - value])
        fill(0, left_rows[0], [])
        return total
    return 0 if min([*rows, *columns], default=0) < 0 or sum(rows) != sum(columns) else count(tuple(rows), tuple(columns))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gap-run', type=Path, required=True)
    parser.add_argument('--transport-run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGALRM, signal.SIGUSR1):
        signal.signal(sig, fc.interrupted)
    signal.setitimer(signal.ITIMER_REAL, 180)
    out = args.output.resolve()
    fc.need(not out.exists() and not out.is_relative_to(fc.HERE), 'Fresh controls output required')
    out.mkdir(parents=True)
    started = time.monotonic()
    original = fc.binding()
    result = {'status': 'INCOMPLETE', 'positive': [], 'negative': [], 'source_binding': original,
              'controls_source': fc.pin(__file__)}
    def reject(name, fn, message=None):
        try:
            fn()
        except (ValueError, tm.Refused, RuntimeError, KeyError, TypeError) as exc:
            fc.need(message is None or message in str(exc), 'Refusal occurred at the wrong check: ' + name + ': ' + str(exc))
            result['negative'].append({'id': name, 'exception': type(exc).__name__, 'message': str(exc)})
        else:
            raise AssertionError('Bad fixture accepted: ' + name)
    try:
        for folder in (args.gap_run, args.transport_run):
            fc.need(fc.decode((folder / 'source-binding.json').read_bytes()) == original, 'Run source binding differs')
            accepted = fc.decode((folder / 'result.json').read_bytes())
            fc.need(accepted['status'].startswith('COMPLETE_FRESH_') and accepted['source_bytes_unchanged'], 'Incomplete full run')
        binary = args.gap_run / 'gap3_jt_counter'
        fc.need(fc.pin(binary) == fc.decode((args.gap_run / 'binary.json').read_bytes()), 'Counter binary differs')
        def query(name, mode, payload, limits='2000000000 10000 1000000'):
            receipt, raw = fc.child([str(binary)], out / name, 15,
                                    f'GAP3JT1 {name} {mode} {limits} {payload}\n'.encode())
            return receipt, fc.parse_counter(raw)
        receipt, signs = query('permutations', 'SIGNS', '')
        expected = [{'permutation': list(p), 'sign': (-1) ** sum(p[i] > p[j] for i in range(5) for j in range(i+1, 5))}
                    for p in permutations(range(5))]
        fc.need(receipt['returncode'] == 0 and signs['permutation_roster'] == expected, 'Literal 120 permutation signs differ')
        result['positive'].append({'id': 'all-120-permutation-signs', 'cases': 120})
        examples = [([0], [0,0,0]), ([1], [1,0,0]), ([1,1], [1,1,0]),
                    ([2,2], [2,1,1]), ([2,2,2], [2,2,2]), ([1,2,1,2,1], [3,2,2]),
                    ([0,2,0,1,1], [1,1,2]), ([3,2], [0,4,1]), ([1,1], [3,0,0]),
                    ([1,1], [-1,2,1])]
        for i, (rows, columns) in enumerate(examples):
            payload = ' '.join(map(str, [len(rows), *columns, *rows]))
            receipt, response = query('matrix-' + str(i), 'MATRIX', payload)
            fc.need(receipt['returncode'] == 0 and tm.integer(response['count']) == direct_tables(rows, columns), 'Three-column recurrence disagrees with literal tables')
        result['positive'].append({'id': 'three-column-literal-table-controls', 'cases': len(examples)})
        for name, mode, payload, limits, status in [
            ('overflow', 'ARITH', f'ADD {2**127-1} 1', '1000 10000 1000', 'REFUSED_OVERFLOW'),
            ('work', 'FAMILY', '1 1 10', '1 10000 1000000', 'REFUSED_WORK'),
            ('parent', 'FAMILY', '3 0 1', '1000000 10000 1000000', 'REFUSED_PARENT_SCOPE'),
            ('grade', 'FAMILY', '1 1 11', '1000000 10000 1000000', 'REFUSED_SCOPE'),
            ('cells', 'FAMILY', '1 1 10', '1000000000 10000 1', 'REFUSED_TABLE_SIZE'),
            ('extra', 'ARITH', 'ADD 1 2 trailing', '1000 10000 1000', 'REFUSED_EXTRA_INPUT')]:
            receipt, response = query('refuse-' + name, mode, payload, limits)
            fc.need(receipt['returncode'] == 2 and response['count'] is None and response['status'] == status,
                    'Incorrect typed refusal: ' + name + ': ' + str(response))
            result['negative'].append({'id': 'counter-' + name, 'status': status, 'count': None})
        table_cases = 0
        for rows, columns in [([1,1,1,1], [2,2]), ([2,2,1,1], [2,2,2]), ([3,2,2,1], [2,2,2,2]),
                              ([4,2,1,1], [3,3,2])]:
            groups = tm.assignment_groups(len(columns)-2)
            for t in (0,1,2):
                budget = tm.Budget(seconds=10)
                counter = tm.AssignmentCounter(budget)
                signed = sum(g['sign'] * g['weight'] * counter.count(g['occupation'], tm.assignment_targets(g, rows, columns, t)['targets']) for g in groups)
                fc.need(signed == direct_tables([t*r for r in rows], [t*c for c in columns]), 'Signed complete assignment formula disagrees with literal tables')
                table_cases += 1
        result['positive'].append({'id': 'four-row-literal-table-controls', 'cases': table_cases})
        node = fc.decode((args.transport_run / 'h0-t1/stdout.txt').read_bytes())
        fc.validate_transport_node(node, 0, 1)
        for name, edit in [
            ('omitted-group', lambda r: r['assignments'].pop()),
            ('duplicate-group', lambda r: r['assignments'].__setitem__(0, deepcopy(r['assignments'][1]))),
            ('wrong-sign', lambda r: r['assignments'][0].__setitem__('sign', -r['assignments'][0]['sign'])),
            ('wrong-offset', lambda r: r['assignments'][0]['targets'].__setitem__(0, r['assignments'][0]['targets'][0]+1)),
            ('partial-assignment', lambda r: r['assignments'][0].__setitem__('status', 'PARTIAL')),
            ('wrong-whole-scalar', lambda r: r.__setitem__('value', str(int(r['value'])+1))),
            ('boolean-count', lambda r: r['assignments'][0].__setitem__('unsigned_count', True))]:
            changed = deepcopy(node); edit(changed)
            reject(name, lambda changed=changed: fc.validate_transport_node(changed, 0, 1))
        gaps = fc.decode((args.gap_run / 'fresh-counts.json').read_bytes())
        transports = fc.decode((args.transport_run / 'fresh-counts.json').read_bytes())
        for name, rows, sites, key in [('gap', gaps, fc.gap_sites(False), lambda r:(r['parent'], r['t'])),
                                      ('transport', transports, fc.transport_sites(False), lambda r:(r['h'], r['t']))]:
            reject(name + '-missing-node', lambda rows=rows,sites=sites,key=key: fc.roster(rows[:-1], sites, key))
            reject(name + '-duplicate-node', lambda rows=rows,sites=sites,key=key: fc.roster(rows + [rows[0]], sites, key))
        bad_gap = deepcopy(gaps)
        row = next(r for r in bad_gap if r['parent']=='P00' and r['t']==9)
        row['value'] = row['counter']['count'] = str(int(row['value'])+1)
        folder = out / 'changed-gap-unused-hold'; folder.mkdir()
        reject('changed-gap-unused-hold', lambda: fc.gap_algebra(folder, bad_gap), 'Fresh unused gap hold')
        bad_transport = deepcopy(transports)
        row = next(r for r in bad_transport if r['h']==0 and r['t']==13)
        row['value'] = str(int(row['value'])+1)
        folder = out / 'changed-transport-unused-hold'; folder.mkdir()
        reject('changed-transport-unused-hold', lambda: fc.transport_algebra(folder, bad_transport), 'Fresh unused transport hold')
        reject('duplicate-json-key', lambda: fc.decode('{"a":1,"a":2}'))
        reject('transport-work-budget', lambda: tm.AssignmentCounter(tm.Budget(seconds=1, max_work=1)).count([2,2,3], [7,7,7]))
        reject('class-four-exclusion', lambda: tm.assignment_targets(tm.assignment_groups()[0], [7,5,4,1], [0,7,2,2,2,2,2], 1))
        reject('hard-child-deadline', lambda: fc.child([sys.executable, '-B', '-c', 'import time; time.sleep(10)'], out / 'timeout', 0.1))
        deadline = fc.decode((out / 'timeout/receipt.json').read_bytes())
        fc.need(deadline['timed_out'] and deadline['returncode'] < 0 and deadline['wait_completed'] and deadline['group_absent'], 'Timeout cleanup not complete')
        # Exercise the actual signal handler while an owned child is active.
        # The child notifies this parent; the handler must kill and wait it.
        reject('signal-child-cleanup', lambda: fc.child([sys.executable, '-B', '-c',
               'import os,signal,time; os.kill(int(__import__("sys").argv[1]),signal.SIGUSR1); time.sleep(10)',
               str(os.getpid())], out / 'signal', 10))
        interrupted = fc.decode((out / 'signal/receipt.json').read_bytes())
        fc.need(interrupted['interruption'] and interrupted['returncode'] < 0
                and interrupted['wait_completed'] and interrupted['group_absent'], 'Signal cleanup not complete')
        fc.need(fc.binding() == original, 'Controls changed science sources or accepted data')
        result.update(status='COMPLETE_CONTROLS', source_bytes_unchanged=True,
                      positive_cases=sum(p['cases'] for p in result['positive']), negative_cases=len(result['negative']))
    except BaseException as exc:
        result.update(status='FAILED', exception=type(exc).__name__, error=str(exc))
        raise
    finally:
        fc.stop_child()
        signal.setitimer(signal.ITIMER_REAL, 0)
        result.update(elapsed_seconds=time.monotonic()-started, active_child=None)
        fc.save(out / 'result.json', result)
    print(json.dumps({k:result[k] for k in ('status','positive_cases','negative_cases','elapsed_seconds','active_child')}))


if __name__ == '__main__':
    main()
