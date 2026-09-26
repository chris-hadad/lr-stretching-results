#!/usr/bin/env python3
"""Regenerate the complete F025 forcing tables: sound dimension upper bounds only."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from forcing_model import model, closure, identifications
from forcing_rows import original_rows

HERE = Path(__file__).resolve().parent
TABLES = {
    6: {'path': 'f025/F025-MASK-R6-001.json', 'bytes': 3355507,
        'sha256': '6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0'},
    7: {'path': 'f025/F025-MASK-R7-001.json', 'bytes': 28416986,
        'sha256': 'bb595b3914ce05105743e9386f2cc64a4d2ae2d59df0d340c3221b8b74d7cd9c'},
}
ROW_CHECKER_SHA = 'bca0fefb46a54edba559278b0e1ca4f34722686b1b2fbc49cad7771801f32efe'
ACTIVE = None


def require(test, message):
    if not test:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def unique(items):
    out = {}
    for key, value in items:
        require(key not in out, 'Duplicate JSON key')
        out[key] = value
    return out


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique)


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def write_new(path, value):
    with Path(path).open('xb') as stream:
        stream.write(encoded(value))


def function_span(path, name):
    text = Path(path).read_text()
    lines = text.splitlines(keepends=True)
    nodes = [n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name]
    require(len(nodes) == 1, 'Missing or repeated reference function')
    node = nodes[0]
    first = min([node.lineno] + [d.lineno for d in node.decorator_list])
    return ''.join(lines[first-1:node.end_lineno])


def source_binding(row_checker, asset_manifest):
    require(pin(row_checker)['sha256'] == ROW_CHECKER_SHA, 'Structural row checker differs from accepted bytes')
    require(function_span(row_checker, 'original_rows') == function_span(HERE / 'forcing_rows.py', 'original_rows'),
            'Copied original_rows is not the actual structural checker function')
    asset = decode(Path(asset_manifest).read_bytes())
    for record in TABLES.values():
        member = asset['files'][record['path']]
        require(all(member[k] == record[k] for k in ('bytes', 'sha256')), 'Shared data manifest binds a different forcing table')
    names = ('verify_forcing.py', 'forcing_model.py', 'forcing_hive.py', 'forcing_rows.py')
    return {'code': {name: pin(HERE / name) for name in names},
            'structural_row_checker': pin(row_checker), 'shared_data_manifest': pin(asset_manifest),
            'tables': TABLES}


def exact_mask(mask, n):
    require(type(n) is int and n in TABLES and type(mask) is int and 0 <= mask < 1 << (3*(n-1)),
            'Invalid exact boundary mask or rank')
    return mask


def validate_table(doc, n):
    count = 1 << (3*(n-1))
    require(doc['status'] == 'complete' and doc['rank'] == n and doc['start'] == 0
            and doc['stop'] == doc['checked_count'] == count, 'Incomplete accepted table header')
    records = doc['records']
    require(isinstance(records, list) and len(records) == count, 'Omitted or extra mask record')
    row_count, dimension = 3*n*(n-1)//2, (n-1)*(n-2)//2
    for ordinal, row in enumerate(records):
        require(exact_mask(row['mask'], n) == ordinal, 'Duplicate, omitted or reordered mask record')
        z, d = row['closed_rows_mask'], row['dimension_bound']
        require(type(z) is int and 0 <= z < 1 << row_count and type(d) is int and 0 <= d <= dimension,
                'Invalid closed-row mask or dimension upper bound')
    return records


def load_table(data_root, n):
    entry = TABLES[n]
    path = Path(data_root) / entry['path']
    raw = path.read_bytes()
    require(len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256'],
            'Accepted forcing table size/hash differs')
    doc = decode(raw)
    validate_table(doc, n)
    return doc


def coordinate_binding(n, m):
    rows = original_rows(n)
    require(len(rows) == len(m['full_rows']) == 3*n*(n-1)//2, 'Incomplete original rhombus rows')
    combined = tuple(tuple(b) + tuple(a) for a, b in zip(m['A'], m['B']))
    require(combined == rows, 'Full boundary/interior coefficients or row ordering differ')
    dimension = (n-1)*(n-2)//2
    require(m['dimension'] == dimension, 'Interior coordinate dimension differs')
    # Boundary gaps are exact modulo the one original balance equality.
    # This explicitly includes the corner shared by the lambda and nu sides.
    balance = [1]*n + [-1]*(2*n) + [0]*dimension
    gap_balance_multiples = []
    for ordinal, bits in enumerate(m['gaps']):
        require(bits.bit_count() == 2, 'Boundary gap must use exactly two distinct rhombi')
        side, index = divmod(ordinal, n-1)
        expected = [0]*(3*n+dimension)
        expected[side*n+index], expected[side*n+index+1] = 1, -1
        actual = [sum(row[c] for r, row in enumerate(rows) if bits & (1 << r)) for c in range(len(expected))]
        difference = [a-b for a,b in zip(actual,expected)]
        multiple = difference[0]
        require(difference == [multiple*x for x in balance], 'Boundary-gap side/bit convention differs')
        gap_balance_multiples.append(multiple)
    return {'rhombus_rows': len(rows), 'interior_coordinates': dimension,
            'coordinate_order': '(lambda[0:n], mu[0:n], nu[0:n], lexicographic interior (i,j))',
            'all_boundary_linear_rows_sha256': hashlib.sha256(encoded(rows)).hexdigest(),
            'all_full_vertex_rows_sha256': hashlib.sha256(encoded(m['full_rows'])).hexdigest(),
            'boundary_gap_row_masks': m['gaps'], 'boundary_gap_balance_multiples': gap_balance_multiples,
            'positive_equal_sum_rules': len(m['rules']),
            'soundness_scope': 'Unit identifications in forced equations give an affine dimension upper bound; feasibility, actual dimension and universal forcing completeness are not claimed.'}


def compare_record(record, n, m, cache):
    mask = exact_mask(record['mask'], n)
    closed = closure(mask, m)
    if closed not in cache:
        free, components, ground, words = identifications(closed, m)
        cache[closed] = len(free)
    bound = cache[closed]
    require(type(record['closed_rows_mask']) is int and record['closed_rows_mask'] == closed,
            f'Closed-row mask differs at rank {n}, mask {mask}')
    require(type(record['dimension_bound']) is int and record['dimension_bound'] == bound,
            f'Dimension upper bound differs at rank {n}, mask {mask}')
    return {'mask': mask, 'closed_rows_mask': closed, 'dimension_bound': bound}


def check_rank(data_root, n, sample):
    require(type(n) is int and n in TABLES and type(sample) is int and (sample == 0 or 2 <= sample <= 4096),
            'Invalid frozen rank or calibration size')
    doc = load_table(data_root, n)
    m = model(n)
    binding = coordinate_binding(n, m)
    require(len(m['rules']) == doc['independent_full_vertex_relations'], 'Accepted rule population differs')
    total = 1 << (3*(n-1))
    masks = range(total) if sample == 0 else [i*(total-1)//(sample-1) for i in range(sample)]
    cache, hist = {}, Counter()
    observed, accepted = hashlib.sha256(), hashlib.sha256()
    started = time.monotonic()
    for mask in masks:
        raw = doc['records'][mask]
        fresh = compare_record(raw, n, m, cache)
        hist[fresh['dimension_bound']] += 1
        observed.update(encoded(fresh))
        accepted.update(encoded({k: raw[k] for k in ('mask','closed_rows_mask','dimension_bound')}))
    elapsed = time.monotonic()-started
    require(observed.digest() == accepted.digest(), 'Complete normalized record digest differs')
    if sample == 0:
        require(len(cache) == doc['distinct_closures_checked'], 'Accepted distinct-closure count differs')
        require(dict(hist) == {int(k):v for k,v in doc['dimension_histogram'].items()}, 'Accepted upper-bound histogram differs')
    return {'status': 'COMPLETE_FULL_FORCING_DOMAIN' if sample == 0 else 'COMPLETE_CALIBRATION_ONLY',
            'rank': n, 'masks_compared': len(masks), 'domain_size': total,
            'distinct_closures_checked': len(cache), 'dimension_upper_bound_histogram': dict(hist),
            'fresh_record_sha256': observed.hexdigest(), 'accepted_record_sha256': accepted.hexdigest(),
            'coordinate_binding': binding, 'computation_seconds': elapsed,
            'linear_full_domain_forecast_seconds': elapsed * total / len(masks),
            'table': TABLES[n], 'scope': 'Sound dimension upper bounds only; no actual dimension or universal closure claim.'}


def group_exists(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def stop_child(proc=None):
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


def child(argv, folder, deadline):
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
    timeout, interruption = False, None
    launch_written = False
    surviving_descendant = False
    receipt_owned = False
    stdout = stderr = b''
    try:
        for sig in signals:
            signal.signal(sig, flag)
        try:
            folder.mkdir()
            write_new(folder/'request.json', {'argv': argv, 'wall_deadline_seconds': deadline})
            check_signal()
            proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'},
                                    start_new_session=True)
            ACTIVE = proc
            write_new(folder/'launch.json', {'pid':proc.pid,'pgid':proc.pid})
            launch_written = True
            until = time.monotonic() + deadline
            while True:
                check_signal()
                remaining = until - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(argv, deadline)
                try:
                    stdout, stderr = proc.communicate(timeout=min(0.2, remaining))
                    break
                except subprocess.TimeoutExpired:
                    continue
            if group_exists(proc.pid):
                surviving_descendant = True
                raise RuntimeError('Unexpected surviving owned descendant')
            check_signal()
        except subprocess.TimeoutExpired:
            timeout = True
        except BaseException as exc:
            interruption = exc
        if proc is None:
            raise interruption
        if timeout or interruption is not None or caught[0] or proc.poll() is None or group_exists(proc.pid):
            stop_child(proc)
        else:
            proc.wait(timeout=0.2)
        if not group_exists(proc.pid):
            ACTIVE = None
        if not launch_written or surviving_descendant:
            raise interruption
        if timeout or interruption is not None:
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
        (folder/'stdout.txt').write_bytes(stdout); (folder/'stderr.txt').write_bytes(stderr)
        receipt={'pid':proc.pid,'pgid':proc.pid,'returncode':proc.returncode,'wait_completed':True,
                 'group_absent':True,'timed_out':timeout,
                 'interruption':None if interruption is None else str(interruption),
                 'elapsed_seconds':time.monotonic()-started}
        receipt_path=folder/'receipt.json'
        write_new(receipt_path,receipt)
        receipt_owned = True
        if caught[0] and interruption is None:
            receipt_path.unlink(missing_ok=True)
            raise RuntimeError('Interrupted by signal '+str(caught[0]))
        if interruption is not None:
            raise interruption
        require(not timeout, 'Child deadline exceeded; partial evidence retained')
        return receipt, stdout
    finally:
        if caught[0] and interruption is None and not timeout and receipt_owned:
            (folder/'receipt.json').unlink(missing_ok=True)
        if proc is not None and not group_exists(proc.pid):
            ACTIVE = None
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        if caught[0] and sys.exc_info()[0] is None:
            raise RuntimeError('Interrupted by signal ' + str(caught[0]))


def fresh_output(path, data_root):
    original = Path(os.path.abspath(path))
    require(not os.path.lexists(original), 'Output already exists')
    out = original.resolve()
    for protected in (HERE, Path(data_root).resolve()):
        require(not out.is_relative_to(protected) and not protected.is_relative_to(out), 'Output overlaps source or data tree')
    require(out.parent.is_dir(), 'Output parent must already exist')
    out.mkdir()
    return out


def main():
    require(__debug__, 'Optimized Python is refused; rerun without -O or PYTHONOPTIMIZE')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--calibrate', type=int, default=0, metavar='MASKS_PER_RANK')
    parser.add_argument('--deadline', type=int, default=600)
    parser.add_argument('--row-checker', type=Path, default=HERE.parent/'verify_pro027_masks.py')
    parser.add_argument('--data-manifest', type=Path, default=HERE.parent/'DATA-ASSET.json')
    parser.add_argument('--_rank', type=int, choices=(6,7), help=argparse.SUPPRESS)
    args = parser.parse_args()
    require(1 <= args.deadline <= 3600, 'Deadline must be in 1..3600 seconds')
    signals = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM)
    previous = {sig: signal.getsignal(sig) for sig in signals}
    try:
        for sig in signals:
            signal.signal(sig, interrupted)
        signal.setitimer(signal.ITIMER_REAL,args.deadline)
        _verify(args)
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def _verify(args):
    if args._rank:
        print(json.dumps(check_rank(args.data_root,args._rank,args.calibrate),sort_keys=True)); return
    require(args.output is not None, 'A fresh output directory is required')
    binding = source_binding(args.row_checker,args.data_manifest)
    out = fresh_output(args.output,args.data_root)
    write_new(out/'source-binding.json',binding)
    write_new(out/'configuration.json',{'argv':sys.argv,'pid':os.getpid(),'deadline_seconds':args.deadline,
                                       'serial_children':True,'python':pin(sys.executable)})
    started=time.monotonic(); result={'status':'INCOMPLETE','ranks':[]}
    try:
        for n in (6,7):
            remaining = args.deadline-(time.monotonic()-started)
            require(remaining>3,'Insufficient remaining whole-run deadline')
            receipt, raw = child([sys.executable,'-B',str(HERE/'verify_forcing.py'),'--data-root',str(args.data_root.resolve()),
                                   '--_rank',str(n),'--calibrate',str(args.calibrate),'--deadline',str(max(1,int(remaining)-2))],
                                  out/f'rank-{n}',remaining-1)
            require(receipt['returncode']==0,'Rank child failed; no complete-domain claim')
            record=decode(raw)
            require(record['rank']==n and record['status']==('COMPLETE_CALIBRATION_ONLY' if args.calibrate else 'COMPLETE_FULL_FORCING_DOMAIN'),
                    'Wrong rank or partial child status')
            result['ranks'].append(record)
            print(json.dumps({'rank':n,'masks':record['masks_compared'],'seconds':record['computation_seconds']}),flush=True)
        require(source_binding(args.row_checker,args.data_manifest)==binding,'Code or manifest changed during verification')
        for table in TABLES.values():
            require(pin(args.data_root/table['path']) == {k:table[k] for k in ('bytes','sha256')},
                    'Accepted table bytes changed during verification')
        result.update(status='COMPLETE_CALIBRATION_ONLY' if args.calibrate else 'COMPLETE_F025_FORCING_RECHECK',
                      source_bytes_unchanged=True,masks_compared=sum(r['masks_compared'] for r in result['ranks']))
    except BaseException as exc:
        result.update(status='FAILED_OR_INCOMPLETE',error=str(exc),exception=type(exc).__name__); raise
    finally:
        stop_child()
        result.update(elapsed_seconds=time.monotonic()-started,active_child=None)
        write_new(out/'result.json',result)
    print(json.dumps({'status':result['status'],'masks_compared':result['masks_compared'],'seconds':result['elapsed_seconds']}))


if __name__ == '__main__':
    main()
