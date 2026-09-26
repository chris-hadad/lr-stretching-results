#!/usr/bin/env python3
"""Small archive, reader, and owned-group refusal fixtures for this package."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import warnings
import zipfile

import restore
import runtime

HERE = Path(__file__).resolve().parent


def need(value, message):
    if not value:
        raise RuntimeError(message)


def reject_value(label, function, contains):
    try:
        function()
    except ValueError as error:
        need(contains in str(error), label + ' wrong refusal: ' + str(error))
        return str(error)
    raise RuntimeError(label + ' was accepted')


def reject_command(label, argv, output, contains):
    stdout = output / (label + '.stdout')
    stderr = output / (label + '.stderr')
    with stdout.open('x') as out, stderr.open('x') as err:
        result = runtime.run_owned(argv, stdout=out, stderr=err, timeout=20, env=None)
    combined = stdout.read_text() + stderr.read_text()
    need(result['exit'] != 0 and contains in combined and result['owned_process_group_exited'],
         label + ' wrong refusal or live group')
    return {'exit': result['exit'], 'reason': contains}


def zipinfo(name):
    value = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
    value.compress_type = zipfile.ZIP_STORED
    value.external_attr = 0o100644 << 16
    value.create_system = 3
    return value


def fixture_zip(path, rows):
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_STORED) as archive:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            for name, payload in rows:
                archive.writestr(zipinfo(name), payload)


def group_control(output, timeout_case):
    pid_path = output / ('timeout.pid' if timeout_case else 'descendant.pid')
    if timeout_case:
        code = ('import os,time,pathlib;pathlib.Path(' + repr(str(pid_path)) +
                ').write_text(str(os.getpid()));time.sleep(30)')
        wanted = subprocess.TimeoutExpired
        timeout = 0.4
    else:
        code = ('import os,subprocess,sys,pathlib;child=subprocess.Popen([sys.executable,'
                "'-c','import time;time.sleep(30)']);pathlib.Path(" + repr(str(pid_path)) +
                ').write_text(str(os.getpid())+" "+str(child.pid))')
        wanted = RuntimeError
        timeout = 5
    stdout = output / ('timeout.stdout' if timeout_case else 'descendant.stdout')
    stderr = output / ('timeout.stderr' if timeout_case else 'descendant.stderr')
    with stdout.open('x') as out, stderr.open('x') as err:
        try:
            runtime.run_owned([sys.executable, '-B', '-c', code], stdout=out, stderr=err,
                              timeout=timeout, env=None)
        except wanted:
            pass
        else:
            raise RuntimeError('owned child/group cleanup was not triggered')
    pgid = int(pid_path.read_text().split()[0])
    need(not runtime.group_exists(pgid), 'owned process group survived cleanup: ' + str(pgid))
    return 'owned group exited after ' + ('timeout' if timeout_case else 'leader exited first')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-dir', type=Path, required=True)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--reader-run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    output = args.output
    a, b = 'packet/a.json', 'packet/b.json'
    payloads = {a: b'aaa', b: b'bbb'}
    files = {name: {'bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest()}
             for name, blob in payloads.items()}
    observed = {}
    missing = output / 'missing.zip'
    fixture_zip(missing, [(a, payloads[a])])
    with zipfile.ZipFile(missing) as archive:
        observed['missing_member'] = reject_value('missing member',
            lambda: restore.validate_members(archive, files), 'missing, duplicate or unexpected')
    duplicate = output / 'duplicate.zip'
    fixture_zip(duplicate, [(a, payloads[a]), (a, payloads[a]), (b, payloads[b])])
    with zipfile.ZipFile(duplicate) as archive:
        observed['duplicate_member'] = reject_value('duplicate member',
            lambda: restore.validate_members(archive, files), 'missing, duplicate or unexpected')
    unsafe = output / 'unsafe.zip'
    fixture_zip(unsafe, [('../escape', b'aaa'), (b, payloads[b])])
    with zipfile.ZipFile(unsafe) as archive:
        unsafe_files = {'../escape': files[a], b: files[b]}
        observed['unsafe_member'] = reject_value('unsafe member',
            lambda: restore.validate_members(archive, unsafe_files), 'unsafe archive member')
    corrupt = output / 'corrupt.zip'
    fixture_zip(corrupt, [(a, b'xxx'), (b, payloads[b])])
    target = output / 'corrupt-output'
    target.mkdir()
    with zipfile.ZipFile(corrupt) as archive:
        members = restore.validate_members(archive, files)
        observed['corrupt_member'] = reject_value('corrupt member',
            lambda: restore.copy_checked_member(archive, members[0], target / 'a.json', files[a]),
            'corrupt member')
    observed['archive_byte_binding'] = reject_value('changed archive',
        lambda: restore.archive_path(output, {'name': corrupt.name,
              'bytes': corrupt.stat().st_size, 'sha256': '0' * 64}), 'changed data archive')
    partial = output / 'partial-data'
    (partial / 'packet').mkdir(parents=True)
    (partial / a).write_bytes(payloads[a])
    observed['missing_restored'] = reject_value('missing restored file',
        lambda: restore.verify(partial, files), 'missing restored data members')
    (partial / b).write_bytes(b'xxx')
    observed['corrupt_restored'] = reject_value('corrupt restored file',
        lambda: restore.verify(partial, files), 'missing/corrupt restored member')
    observed['source_output'] = reject_command('source-output',
        [sys.executable, '-B', str(HERE / 'restore.py'), 'restore', '--archives',
         str(args.archive_dir), '--out', str(args.archive_dir / 'forbidden')],
        output, 'output overlaps source or archive root')
    observed['occupied_output'] = reject_command('occupied-output',
        [sys.executable, '-B', str(HERE / 'restore.py'), 'restore', '--archives',
         str(args.archive_dir), '--out', str(args.data)],
        output, 'fresh output and existing parent required')
    reader = [sys.executable, '-B', str(HERE / 'reader_replay.py'), 'calibrate',
              '--data', str(args.data)]
    observed['optimized_python'] = reject_command('optimized-python',
        [sys.executable, '-O', str(HERE / 'reader_replay.py'), 'calibrate',
         '--data', str(args.data), '--output-root', str(output / 'optimized')],
        output, 'Optimized Python is refused')
    observed['reader_source_output'] = reject_command('reader-source-output',
        reader + ['--output-root', str(args.data / 'forbidden')],
        output, 'Output overlaps source or data tree')
    observed['reader_occupied'] = reject_command('reader-occupied',
        reader + ['--output-root', str(args.reader_run)],
        output, 'Existing output requires --resume')
    fake = output / 'foreign-resume'
    fake.mkdir()
    marker = json.loads((args.reader_run / 'READER-RUN-IDENTITY.json').read_text())
    marker['source_sha256']['runtime.py'] = '0' * 64
    (fake / 'READER-RUN-IDENTITY.json').write_text(json.dumps(marker))
    observed['reader_changed_source'] = reject_command('reader-changed-source',
        reader + ['--resume', '--output-root', str(fake)], output,
        'identical reader/runtime/data-verifier identity')
    observed['leader_exit_descendant_cleanup'] = group_control(output, False)
    observed['timeout_group_cleanup'] = group_control(output, True)
    report = {'schema': 'structural-certificates-public-controls-v1',
              'status': 'ALL_CONTROLS_PASS', 'observed': observed}
    (output / 'RESULT.json').write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'controls': len(observed)}, sort_keys=True))

if __name__ == '__main__':
    main()
