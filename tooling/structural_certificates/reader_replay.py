#!/usr/bin/env python3
"""Fresh portable normal-atlas and boundary-mask certificate replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import time

from runtime import group_exists, stop_group

HERE = Path(__file__).resolve().parent
ENGINE_HASHES = {
    'verify_normal_certificates.py': '580de0e067be93d0d0c96b2d85acb4c11ef5b7996647552f3717a452c0c40420',
    'verify_pro027_masks.py': 'bca0fefb46a54edba559278b0e1ca4f34722686b1b2fbc49cad7771801f32efe',
}
STAGES = ('normal', 'p07', 'p08', 'p06')
CHILD_TIMEOUT = 125
ASSET_VERIFY_TIMEOUT = 120
CANCEL_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
cancel_signal = None


def check_cancelled():
    if cancel_signal is not None:
        raise KeyboardInterrupt('Interrupted by signal ' + str(cancel_signal))


def run_cancelable(command, *, stdout, stderr, timeout, env):
    """Supervise one separate-session child while outer signals request cleanup."""
    check_cancelled()
    started = time.monotonic()
    deadline = started + timeout
    process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                               start_new_session=True, env=env)
    try:
        while True:
            check_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(command, timeout)
            try:
                rc = process.wait(timeout=min(0.2, remaining))
                break
            except subprocess.TimeoutExpired:
                continue
        check_cancelled()
        if group_exists(process.pid):
            raise RuntimeError('command left a live descendant: ' + str(process.pid))
    except BaseException:
        stop_group(process)
        raise
    return {'argv': command, 'pid': process.pid, 'exit': rc,
            'seconds': time.monotonic() - started, 'child_waited': True,
            'owned_process_group_exited': True}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def identity():
    files = ['reader_replay.py', 'runtime.py', 'restore.py', 'DATA-ASSET.json', 'JOBS.json',
             *ENGINE_HASHES]
    return {'schema': 'structural-certificates-reader-identity-v1',
            'source_sha256': {name: sha(HERE / name) for name in files}}


def check_sources():
    for name, wanted in ENGINE_HASHES.items():
        need(sha(HERE / name) == wanted, 'Mathematical checker changed: ' + name)


def output_root(data, output, resume):
    data, output = data.resolve(strict=True), output.resolve()
    need(data.is_dir(), 'restored data directory required')
    for root in (data, HERE):
        root = root.resolve()
        need(not (output.is_relative_to(root) or root.is_relative_to(output)),
             'Output overlaps source or data tree')
    marker = output / 'READER-RUN-IDENTITY.json'
    binding = identity()
    if output.exists():
        need(resume and marker.is_file() and json.loads(marker.read_text()) == binding,
             'Existing output requires --resume and the identical reader/runtime/data-verifier identity')
    else:
        need(output.parent.is_dir(), 'Output parent must exist')
        output.mkdir()
        marker.write_text(json.dumps(binding, sort_keys=True, indent=2) + '\n')
    return data, output


def stderr_path(output):
    path = output.with_suffix('.stderr')
    ordinal = 1
    while path.exists():
        path = output.with_suffix('.stderr.' + str(ordinal))
        ordinal += 1
    return path


def child(argv, output, timeout=CHILD_TIMEOUT):
    check_cancelled()
    need(not output.exists(), 'Refusing to overwrite report: ' + str(output))
    error_path = stderr_path(output)
    with error_path.open('x') as errors:
        record = run_cancelable(argv, stdout=subprocess.DEVNULL, stderr=errors,
                                timeout=timeout, env=None)
    need(record['exit'] == 0 and output.is_file(),
         'Bounded child failed or omitted output: ' + str(output) + '; stderr ' + str(error_path))
    return {'seconds': round(record['seconds'], 3), 'child_waited': record['child_waited'],
            'owned_process_group_exited': record['owned_process_group_exited']}


def verify_data(data, output):
    check_cancelled()
    ordinal = 1
    while (output / f'ASSET-VERIFICATION-{ordinal:04d}.json').exists():
        ordinal += 1
    result = output / f'ASSET-VERIFICATION-{ordinal:04d}.json'
    error = stderr_path(result)
    with result.open('x') as summary, error.open('x') as errors:
        record = run_cancelable([sys.executable, '-B', str(HERE / 'restore.py'), 'verify',
                                 '--out', str(data)], stdout=summary, stderr=errors,
                                timeout=ASSET_VERIFY_TIMEOUT, env=None)
    need(record['exit'] == 0 and record['owned_process_group_exited'],
         'Complete data rehash failed; stderr ' + str(error))
    content = json.loads(result.read_text())
    need(content['status'] == 'PASS_COMPLETE_REHASH' and content['files'] == 10456,
         'Data verifier did not finish complete population')
    return round(record['seconds'], 3)


def engine(stage):
    return HERE / ('verify_normal_certificates.py' if stage == 'normal' else 'verify_pro027_masks.py')


def freeze_args(stage, data, output):
    root = data / 'packet'
    if stage == 'normal':
        return [sys.executable, '-B', str(engine(stage)), 'freeze', '--root', str(root),
                '--output', str(output), '--budget-seconds', '100']
    argv = [sys.executable, '-B', str(engine(stage)), 'freeze', '--root', str(root),
            '--stage', stage, '--f025-r6', str(data / 'f025/F025-MASK-R6-001.json')]
    if stage == 'p06':
        argv += ['--f025-r7', str(data / 'f025/F025-MASK-R7-001.json')]
    return argv + ['--output', str(output), '--seconds', '95']


def slice_args(stage, job, data, manifest, output):
    argv = [sys.executable, '-B', str(engine(stage)), job['command'],
            '--root', str(data / 'packet'), '--manifest', str(manifest),
            *job['args'], '--output', str(output)]
    return argv + (['--budget-seconds', '100'] if stage == 'normal' else ['--seconds', '95'])


def aggregate_args(stage, data, manifest, reports, output, p07_aggregate):
    argv = [sys.executable, '-B', str(engine(stage)), 'aggregate',
            '--root', str(data / 'packet'), '--manifest', str(manifest),
            '--reports', *map(str, reports)]
    if stage == 'p08':
        argv += ['--adopt-p07', str(p07_aggregate)]
    return argv + ['--output', str(output)] + (
        ['--budget-seconds', '100'] if stage == 'normal' else ['--seconds', '95'])


def calibration_indices(jobs, stage):
    kinds = ('file', 'types') if stage == 'normal' else (
        ('cones', 'types', 'scope') if stage == 'p06' else ('cones', 'types'))
    return {max((job for job in jobs if job['command'] == kind),
                key=lambda job: job['accepted_seconds'])['ordinal'] for kind in kinds}


def check_manifest(stage, manifest):
    record = json.loads(manifest.read_text())
    need(record.get('status') == 'FROZEN_INPUTS_ONLY', 'Incomplete freeze: ' + str(manifest))
    if stage == 'normal':
        need(record['checker_sha256_at_freeze'] == ENGINE_HASHES[engine(stage).name],
             'Normal freeze engine changed')
    else:
        need(record['checker_versions'] == ENGINE_HASHES,
             'Mask freeze engines changed')
    return record


def check_slice(stage, job, manifest, report):
    record = json.loads(report.read_text())
    expected = job['expected']
    need(record.get('manifest_sha256') == sha(manifest) and record.get('status') == expected['status'],
         'Wrong manifest or slice status: ' + str(report))
    if stage == 'normal':
        need(record.get('checker_sha256') == ENGINE_HASHES[engine(stage).name]
             and record.get('stop') == expected['stop'], 'Wrong normal engine or interval')
        if record['status'] == 'PARTIAL':
            need(record.get('requested_slice_complete'), 'Incomplete requested normal slice')
    else:
        need(record.get('checker_versions') == ENGINE_HASHES
             and record.get('next_start') == expected['next_start']
             and record.get('obligation') == expected['obligation']
             and record.get('inputs_unchanged'), 'Wrong mask engine, interval or source')


def check_aggregate(stage, path):
    record = json.loads(path.read_text())
    wanted = 'COMPLETE_FINITE_CERTIFICATE_PASS' if stage == 'normal' else 'FINITE_CERTIFICATES_VERIFIED'
    need(record.get('status') == wanted, 'Incomplete aggregate: ' + str(path))
    if stage == 'normal':
        need(len(record['files']) == 34 and all(row['complete'] for row in record['files'])
             and len(record['type_paths_verified']) == 5480
             and record['exceptional_preimages_complete'], 'Incomplete normal join')
    else:
        need(record['missing_intervals'] == {}, 'Incomplete mask join')
    return record


def replay():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for certificate replay')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('calibrate', 'all'))
    parser.add_argument('--data', type=Path, required=True, help='independently restored data directory')
    parser.add_argument('--output-root', type=Path, required=True, help='fresh, disjoint output directory')
    parser.add_argument('--resume', action='store_true', help='continue only an identical reader run')
    args = parser.parse_args()
    check_sources()
    jobs = json.loads((HERE / 'JOBS.json').read_text())
    need(jobs.get('schema') == 'structural-certificates-job-roster-v1', 'Wrong job roster')
    data, output = output_root(args.data, args.output_root, args.resume)
    check_cancelled()
    record = {'schema': 'structural-certificates-reader-invocation-v1',
              'mode': args.mode, 'children': [], 'aggregate_status': {}}
    record['data_rehash_seconds'] = verify_data(data, output)
    p07_aggregate = output / 'p07' / 'aggregate.json'
    for stage in STAGES:
        directory = output / stage
        directory.mkdir(exist_ok=True)
        manifest = directory / 'manifest.json'
        if not manifest.exists():
            timing = child(freeze_args(stage, data, manifest), manifest)
            record['children'].append({'stage': stage, 'kind': 'freeze', **timing})
        check_manifest(stage, manifest)
        rows = jobs['stages'][stage]['jobs']
        selected = calibration_indices(rows, stage) if args.mode == 'calibrate' else {
            row['ordinal'] for row in rows}
        for job in rows:
            if job['ordinal'] not in selected:
                continue
            report = directory / f"slice-{job['ordinal']:04d}.json"
            if not report.exists():
                timing = child(slice_args(stage, job, data, manifest, report), report)
                record['children'].append({'stage': stage, 'kind': 'slice',
                                           'ordinal': job['ordinal'], **timing})
            check_slice(stage, job, manifest, report)
        if args.mode == 'calibrate':
            continue
        reports = [directory / f"slice-{row['ordinal']:04d}.json" for row in rows]
        aggregate = directory / 'aggregate.json'
        if not aggregate.exists():
            timing = child(aggregate_args(stage, data, manifest, reports, aggregate, p07_aggregate),
                           aggregate)
            record['children'].append({'stage': stage, 'kind': 'aggregate', **timing})
        record['aggregate_status'][stage] = check_aggregate(stage, aggregate)['status']
    record['status'] = 'CALIBRATED' if args.mode == 'calibrate' else 'COMPLETE_FINITE_REPLAY'
    record['children_run'] = len(record['children'])
    suffix = 1
    while (output / f'INVOCATION-{suffix:04d}.json').exists():
        suffix += 1
    check_cancelled()
    report = output / f'INVOCATION-{suffix:04d}.json'
    report.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': record['status'], 'children_run': record['children_run'],
                      'data_rehash_seconds': record['data_rehash_seconds'],
                      'report': str(report)}, sort_keys=True))


def main():
    global cancel_signal
    previous = {sig: signal.getsignal(sig) for sig in CANCEL_SIGNALS}
    cancel_signal = None

    def request_cancel(signum, _frame):
        global cancel_signal
        cancel_signal = signum

    try:
        for sig in CANCEL_SIGNALS:
            signal.signal(sig, request_cancel)
        replay()
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        cancel_signal = None


if __name__ == '__main__':
    main()
