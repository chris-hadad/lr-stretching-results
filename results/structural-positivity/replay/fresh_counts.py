#!/usr/bin/env python3
"""Fresh whole-object counts; Python standard library and C++17 only.

See README.md for the analytic premises and precise independent-engine scope.
All outputs are create-only. An interrupted or refused run is never complete.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import permutations
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import exact
import gap_algebra as ga
import gap_model as gm
import transport_math as tm

HERE = Path(__file__).resolve().parent
ACTIVE = None


def need(test, message):
    if not test:
        raise ValueError(message)


def unique(items):
    out = {}
    for key, value in items:
        need(key not in out, 'Duplicate JSON key')
        out[key] = value
    return out


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique)


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def save(path, value):
    with Path(path).open('xb') as stream:
        stream.write(encoded(value))


def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def binding():
    names = ['fresh_counts.py', 'gap3_jt_counter.cpp', 'gap_model.py',
             'exact.py', 'gap_algebra.py', 'transport_math.py',
             'data/gap-three.json', 'data/transport.json']
    return {name: pin(HERE / name) for name in names}


def group_exists(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def stop_child(proc=None):
    """Stop only the exact child session, then wait for its whole group."""
    target = proc if proc is not None else ACTIVE
    if target is None:
        return
    for sig in (signal.SIGTERM, signal.SIGKILL):
        if group_exists(target.pid):
            try:
                os.killpg(target.pid, sig)
            except ProcessLookupError:
                pass
        until = time.monotonic() + 5
        while group_exists(target.pid) and time.monotonic() < until:
            target.poll()
            time.sleep(0.05)
        if not group_exists(target.pid):
            target.wait(timeout=0.2)
            return
    raise RuntimeError('Owned process group did not exit: ' + str(target.pid))


def interrupted(signum, frame):
    raise RuntimeError('Interrupted by signal ' + str(signum))


def child(argv, folder, deadline, stdin=b''):
    """One owned child/group, a hard wall deadline, saved output and exact wait."""
    global ACTIVE
    caught = [None]
    def flag(signum, _frame):
        caught[0] = caught[0] or signum
    def check_signal():
        if caught[0]:
            raise RuntimeError('Interrupted by signal ' + str(caught[0]))
    signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGALRM, signal.SIGUSR1)
    previous = {sig: signal.getsignal(sig) for sig in signals}
    proc = None
    started = time.monotonic()
    timed_out = False
    interruption = None
    launch_written = False
    surviving_descendant = False
    receipt_owned = False
    stdout = stderr = b''
    try:
        for sig in signals:
            signal.signal(sig, flag)
        try:
            folder.mkdir()
            save(folder / 'request.json', {'argv': argv, 'deadline_seconds': deadline,
                 'stdin': stdin.decode(), 'stdin_sha256': hashlib.sha256(stdin).hexdigest()})
            check_signal()
            env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TMPDIR': str(folder)}
            proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, env=env, start_new_session=True)
            ACTIVE = proc
            save(folder / 'launch.json', {'pid': proc.pid, 'pgid': proc.pid})
            launch_written = True
            until = time.monotonic() + deadline
            first_input = stdin
            while True:
                check_signal()
                remaining = until - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(argv, deadline)
                try:
                    stdout, stderr = proc.communicate(first_input, timeout=min(0.2, remaining))
                    break
                except subprocess.TimeoutExpired:
                    first_input = None
            if group_exists(proc.pid):
                surviving_descendant = True
                raise RuntimeError('Unexpected descendant survived the exact child exit')
            check_signal()
        except subprocess.TimeoutExpired:
            timed_out = True
        except BaseException as exc:
            interruption = exc
        if proc is None:
            raise interruption
        if timed_out or interruption is not None or caught[0] or proc.poll() is None or group_exists(proc.pid):
            stop_child(proc)
        else:
            proc.wait(timeout=0.2)
        if not group_exists(proc.pid):
            ACTIVE = None
        if not launch_written:
            raise interruption
        if surviving_descendant:
            raise interruption
        if timed_out or interruption is not None:
            until = time.monotonic() + 5
            while True:
                try:
                    stdout, stderr = proc.communicate(timeout=0.2)
                    break
                except subprocess.TimeoutExpired:
                    if time.monotonic() >= until:
                        raise RuntimeError('Owned child output pipes did not close')
        if caught[0] and interruption is None:
            interruption = RuntimeError('Interrupted by signal ' + str(caught[0]))
        (folder / 'stdout.txt').write_bytes(stdout)
        (folder / 'stderr.txt').write_bytes(stderr)
        receipt = {'pid': proc.pid, 'pgid': proc.pid, 'returncode': proc.returncode,
                   'elapsed_seconds': time.monotonic() - started, 'timed_out': timed_out,
                   'interruption': None if interruption is None else str(interruption),
                   'wait_completed': True, 'group_absent': True}
        receipt_path = folder / 'receipt.json'
        save(receipt_path, receipt)
        receipt_owned = True
        if caught[0] and interruption is None:
            receipt_path.unlink(missing_ok=True)
            raise RuntimeError('Interrupted by signal ' + str(caught[0]))
        if interruption is not None:
            raise interruption
        need(not timed_out, 'Owned child exceeded its wall deadline; evidence retained')
        return receipt, stdout
    finally:
        if caught[0] and interruption is None and not timed_out and receipt_owned:
            (folder / 'receipt.json').unlink(missing_ok=True)
        if proc is not None and not group_exists(proc.pid):
            ACTIVE = None
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        if caught[0] and sys.exc_info()[0] is None:
            raise RuntimeError('Interrupted by signal ' + str(caught[0]))


def parse_counter(raw):
    need(raw.endswith(b'\n') and len(raw.splitlines()) == 1, 'Expected exactly one counter result')
    return decode(raw)


def compile_gap(out, cxx):
    binary = out / 'gap3_jt_counter'
    receipt, _ = child([cxx, '-std=c++17', '-O2', '-Wall', '-Wextra',
                       str(HERE / 'gap3_jt_counter.cpp'), '-o', str(binary)], out / 'compile', 90)
    need(receipt['returncode'] == 0 and binary.is_file(), 'C++ compilation failed')
    save(out / 'binary.json', pin(binary))
    return binary


def gap_sites(calibrate):
    return [('P00', 1), ('P11', 10)] if calibrate else [(p, t) for p in gm.PARENTS for t in range(1, 11)]


def transport_sites(calibrate):
    return [(0, 1), (0, 14), (6, 14)] if calibrate else [(h, t) for h in range(7) for t in range(1, 15)]


def gap_counts(out, calibrate, cxx):
    binary = compile_gap(out, cxx)
    records = []
    for parent, t in gap_sites(calibrate):
        identity = f'{parent}:t{t}'
        request = gm.query(parent, t, 2000000000, 100000, 1000000)
        receipt, raw = child([str(binary)], out / identity.replace(':', '-'), 110, request.encode())
        record = parse_counter(raw)
        count = gm.complete_counter_record(record, identity, t)
        need(receipt['returncode'] == 0, 'Failed counter process cannot supply a count')
        records.append({'id': identity, 'parent': parent, 't': t, 'value': str(count),
                        'counter': record, 'seconds': receipt['elapsed_seconds']})
        print(json.dumps({'complete': identity, 'seconds': receipt['elapsed_seconds']}), flush=True)
    save(out / 'fresh-counts.json', records)
    return records


def transport_node(h, t):
    need(h in range(7) and t in range(1, 15), 'Transport node outside frozen endpoint roster')
    budget = tm.Budget(seconds=100, max_work=50000000)
    counter = tm.AssignmentCounter(budget)
    rows, columns = tm.margins(1, h)
    records = []
    for group in tm.assignment_groups():
        targets = tm.assignment_targets(group, rows, columns, t)
        value = counter.count(group['occupation'], targets['targets'])
        records.append({'group_id': group['id'], 'occupation': group['occupation'],
                        'sign': group['sign'], 'weight': group['weight'], **targets,
                        'unsigned_count': str(value), 'signed_weighted_count': str(group['sign'] * group['weight'] * value),
                        'status': 'COMPLETE_ASSIGNMENT'})
    result = {'h': h, 't': t, 'id': tm.node_id(h, t), 'rows': rows, 'columns': columns,
              'status': 'COMPLETE_ALL_189_ASSIGNMENTS', 'work': budget.work, 'assignments': records}
    result['value'] = str(validate_transport_node(result, h, t))
    return result


def validate_transport_node(record, h, t):
    groups = tm.assignment_groups()
    rows, columns = tm.margins(1, h)
    need(record['h'] == h and record['t'] == t and record['id'] == tm.node_id(h, t)
         and record['status'] == 'COMPLETE_ALL_189_ASSIGNMENTS'
         and record['rows'] == rows and record['columns'] == columns, 'Wrong whole-node identity/status/margins')
    records = record['assignments']
    need(len(records) == len(groups) == 189, 'Incomplete assignment group roster')
    by_id = {row['group_id']: row for row in records}
    need(len(by_id) == 189 and set(by_id) == {g['id'] for g in groups}, 'Duplicate or omitted assignment')
    total = 0
    for group in groups:
        row = by_id[group['id']]
        targets = tm.assignment_targets(group, rows, columns, t)
        need(row['status'] == 'COMPLETE_ASSIGNMENT'
             and all(row[key] == group[key] for key in ('occupation', 'sign', 'weight'))
             and all(row[key] == targets[key] for key in targets), 'Changed assignment sign/weight/strict offset/status')
        value = tm.integer(row['unsigned_count'])
        need(value >= 0 and tm.integer(row['signed_weighted_count']) == group['sign'] * group['weight'] * value,
             'Invalid unsigned or signed assignment count')
        total += group['sign'] * group['weight'] * value
    need(total >= 0, 'A complete signed whole count is negative')
    if 'value' in record:
        need(tm.integer(record['value']) == total, 'Whole scalar disagrees with complete assignment sum')
    return total


def transport_counts(out, calibrate):
    save(out / 'groups.json', tm.assignment_groups())
    records = []
    for h, t in transport_sites(calibrate):
        folder = out / f'h{h}-t{t}'
        receipt, raw = child([sys.executable, '-B', str(HERE / 'fresh_counts.py'), '_transport-node',
                              '--h', str(h), '--t', str(t)], folder, 110)
        need(receipt['returncode'] == 0, 'Incomplete transport child; no scalar accepted')
        record = decode(raw)
        count = validate_transport_node(record, h, t)
        records.append({'h': h, 't': t, 'value': str(count), 'seconds': receipt['elapsed_seconds'],
                        'assignment_file': str(folder.relative_to(out) / 'stdout.txt'), 'assignment_pin': pin(folder / 'stdout.txt')})
        print(json.dumps({'complete': tm.node_id(h, t), 'seconds': receipt['elapsed_seconds']}), flush=True)
    save(out / 'fresh-counts.json', records)
    return records


def roster(records, wanted, key):
    keys = [key(row) for row in records]
    need(len(keys) == len(set(keys)) and set(keys) == set(wanted), 'Incomplete, duplicate or foreign positive-node roster')


def gap_algebra(out, records):
    roster(records, gap_sites(False), lambda r: (r['parent'], r['t']))
    counts = {row['id']: exact.integer(row['value']) for row in records}
    for row in records:
        need(gm.complete_counter_record(row['counter'], row['id'], row['t']) == counts[row['id']], 'Counter/whole scalar mismatch')
    priors = {p: gm.gt_hypotheses(gm.family(*xy)) for p, xy in gm.PARENTS.items()}
    polys = ga.reconstruct(counts)
    # Full vectors are preserved before unused-hold or accepted-value comparisons.
    save(out / 'raw-vectors.json', {'vectors': {p: list(map(str, v)) for p, v in polys.items()},
                                   'negative_observations': ga.negative_observations(polys), 'prior_geometry': priors})
    need(all(all(c > 0 for c in polys[p]) and len(polys[p]) == 11 for p in gm.PARENTS), 'Ordinary parent sign/actual degree fails')
    for p in gm.PARENTS:
        for t in (9, 10):
            need(exact.evaluate(polys[p], t) == counts[f'{p}:t{t}'], 'Fresh unused gap hold disagrees')
    data = decode((HERE / 'data/gap-three.json').read_bytes())
    result = ga.algebra(polys, data['factor_arrays'])
    need({p: list(map(str, v)) for p, v in polys.items()} == data['expected_vectors'], 'Accepted full gap vectors disagree')
    for parent in data['parents']:
        for row in parent['positive_counts']:
            need(counts[f"{parent['id']}:t{row['t']}"] == exact.integer(row['value']), 'Accepted gap count differs')
    result.update(status='COMPLETE_FRESH_GAP_THREE_RECOUNT', positive_nodes=40, determining_nodes=32,
                  unused_positive_holds=8, complete_parent_vectors=4,
                  gap_counter='All 120 JT permutations and complete three-column table counts')
    save(out / 'algebra.json', result)
    return result


def transport_algebra(out, records):
    roster(records, transport_sites(False), lambda r: (r['h'], r['t']))
    totals = {(r['h'], r['t']): tm.integer(r['value']) for r in records}
    vectors = {h: tm.reconstruct({0: 1, **{t: totals[h, t] for t in range(1, 13)}}) for h in range(7)}
    save(out / 'raw-vectors.json', {'vectors': {str(h): list(map(str, v)) for h, v in vectors.items()},
                                   'geometry': {str(h): tm.geometry(h) for h in range(7)},
                                   'negative_indices': {str(h): [i for i, c in enumerate(v) if c < 0] for h, v in vectors.items()}})
    need(all(len(v) == 19 and all(c > 0 for c in v) for v in vectors.values()), 'Full ordinary transport vector sign/degree fails')
    for h in range(7):
        for t in (13, 14):
            need(tm.evaluate(vectors[h], t) == totals[h, t], 'Fresh unused transport hold disagrees')
    shells = [[b - a for a, b in zip(vectors[h], vectors[h+1])] for h in range(6)]
    save(out / 'raw-differences.json', {'scope': 'Auxiliary complete-parent differences; not separate LR objects',
                                      'vectors': [list(map(str, v)) for v in shells]})
    need(all(v[0] == 0 and all(c > 0 for c in v[1:]) for v in shells), 'Complete cap-release shell positivity fails')
    need(shells[-1] == tm.final_shell() and tm.evaluate(shells[-1], 1) == 1, 'Sharp last shell differs')
    # Historical accepted numbers are read only after primary preservation and holds.
    data = decode((HERE / 'data/transport.json').read_bytes())
    need(len(data['parents']) == 7 and {p['h'] for p in data['parents']} == set(range(7)), 'Accepted parent roster differs')
    for parent in data['parents']:
        h = parent['h']
        need(parent['bare'] == tm.bare_family(h) and list(map(tm.rational, parent['coefficients'])) == vectors[h], 'Accepted bare triple or vector differs')
        for row in parent['counts']:
            need(tm.integer(row['value']) == (1 if row['t'] == 0 else totals[h, row['t']]), 'Accepted transport count differs')
    result = {'status': 'COMPLETE_FRESH_INTEGER_H_TRANSPORT_RECOUNT', 'positive_nodes': 98,
              'determining_nodes': 84, 'unused_positive_holds': 14, 'assignment_groups_per_node': 189,
              'labeled_assignments_per_node': 2187, 'complete_assignment_records': 98 * 189,
              'full_vectors': 7, 'ordinary_coefficients': 133, 'positive_nonconstant_shell_coefficients': 108,
              'last_shell': 'binomial(t+17,18)', 'sharp_integer_stabilization_threshold': 6,
              'analytic_premises': 'Proofs 011 and 012: whole LR/table and signed-assignment identities, plus full-cap stabilization; network TU and reciprocity',
              'limits': 'Endpoint integer-h family only. No whole cone coefficient positivity at noninteger h, no independently recomputed BV cut functional.'}
    save(out / 'algebra.json', result)
    return result


def run(args):
    out = args.output.resolve()
    need(not out.exists() and not out.is_relative_to(HERE), 'Output must be fresh and outside the source tree')
    out.mkdir(parents=True)
    before = binding()
    started = time.monotonic()
    save(out / 'source-binding.json', before)
    save(out / 'configuration.json', {'argv': sys.argv, 'mode': args.mode,
         'calibration_only': args.calibrate, 'whole_run_deadline_seconds': args.deadline,
         'serial_children': True, 'pid': os.getpid(), 'python': pin(Path(sys.executable))})
    signal.setitimer(signal.ITIMER_REAL, args.deadline)
    result = {'status': 'INCOMPLETE', 'mode': args.mode, 'calibration_only': args.calibrate}
    try:
        if args.mode == 'gap':
            records = gap_counts(out, args.calibrate, args.cxx)
            if not args.calibrate:
                result.update(gap_algebra(out, records))
        else:
            records = transport_counts(out, args.calibrate)
            if not args.calibrate:
                result.update(transport_algebra(out, records))
        if args.calibrate:
            result.update(status='COMPLETE_CALIBRATION_ONLY', nodes=len(records),
                          node_seconds=[r['seconds'] for r in records])
        need(binding() == before, 'Source or accepted data changed during execution')
        result['source_bytes_unchanged'] = True
    except BaseException as exc:
        result.update(status='FAILED_OR_INCOMPLETE', error=str(exc), exception=type(exc).__name__)
        raise
    finally:
        stop_child()
        signal.setitimer(signal.ITIMER_REAL, 0)
        result.update(elapsed_seconds=time.monotonic()-started, active_child=None)
        save(out / 'result.json', result)
    print(json.dumps(result, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['gap', 'transport', '_transport-node'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--calibrate', action='store_true')
    parser.add_argument('--deadline', type=int, default=1800)
    parser.add_argument('--cxx', default=os.environ.get('CXX', 'c++'),
                        help='C++ compiler executable, without embedded flags (default: CXX or c++)')
    parser.add_argument('--h', type=int)
    parser.add_argument('--t', type=int)
    args = parser.parse_args()
    signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGALRM)
    previous = {sig: signal.getsignal(sig) for sig in signals}
    try:
        for sig in signals:
            signal.signal(sig, interrupted)
        if args.mode == '_transport-node':
            print(json.dumps(transport_node(args.h, args.t), sort_keys=True))
        else:
            need(args.output is not None and 1 <= args.deadline <= 7200, 'A fresh output and a bounded deadline are required')
            run(args)
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


if __name__ == '__main__':
    main()
