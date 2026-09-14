#!/usr/bin/env python3
"""Distinguishing parser and real-process termination checks for verify.py."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import verify

PROBE_SOURCE = r'''
import ast
import inspect
import json
import signal
import subprocess
import sys
import textwrap
from pathlib import Path
sys.path.insert(0, sys.argv[2])
import verify

out = Path(sys.argv[1])
out.mkdir()
mode = sys.argv[3]
injected = False

class ProbeRunner(verify.Runner):
    def wait_child(self, process, timeout):
        if mode == 'timeout':
            raise subprocess.TimeoutExpired(process.args, timeout)
        if mode == 'exception':
            raise OSError('Deliberate wait failure')
        return super().wait_child(process, timeout)

runner = ProbeRunner(out, 30)
verify.install_termination_handlers(runner)
if mode != 'signal':
    source, start = inspect.getsourcelines(verify.Runner.run)
    tree = ast.parse(textwrap.dedent(''.join(source)))
    wanted = 'TimeoutExpired' if mode == 'timeout' else 'BaseException'
    handlers = [node for node in ast.walk(tree) if isinstance(node, ast.ExceptHandler)
                and (getattr(node.type, 'attr', None) or getattr(node.type, 'id', None)) == wanted]
    verify.need(len(handlers) == 1, 'Unique cleanup entry required')
    target_line = start + handlers[0].body[0].lineno - 1
    def inject(frame, event, arg):
        global injected
        if (not injected and event == 'line' and frame.f_code is verify.Runner.run.__code__
                and frame.f_lineno == target_line):
            injected = True
            signal.raise_signal(signal.SIGTERM)
        return inject
    sys.settrace(inject)

try:
    runner.run('child', [sys.executable, '-c',
               'import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)'],
               deadline=30)
except Exception as error:
    sys.settrace(None)
    verify.write_json(out/'INTERRUPTED.json', {'error': str(error), 'mode': mode,
                      'recorded_jobs': len(runner.jobs), 'injected_at_cleanup_entry': injected})
    sys.exit(2)
raise SystemExit('The termination fixture was never interrupted')
'''


def absent(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiled-dir', type=Path, required=True,
                        help='Output of a successful quick or full run of this exact source')
    parser.add_argument('--out', type=Path, required=True, help='Fresh control output directory')
    args = parser.parse_args()
    out = args.out.absolute()
    verify.need(not out.exists() and out.parent.is_dir(), 'Fresh output with existing parent required')
    start = verify.read_json(args.compiled_dir / 'START.json')
    for name in ['verify.py', 'local_values.cpp', 'topology.cpp']:
        verify.need(start['source_hashes'][name] == verify.digest(verify.HERE / name), 'Compiled source version differs')
    out.mkdir()
    binary = args.compiled_dir / 'local_values'
    parser_results = []
    cases = [('empty', b'\n', 0, 0), ('valid', b'one 1 1 1 1\n', 0, 1),
             ('truncated-header', b'truncated 5 10', 2, 0),
             ('appended-truncated-header', b'one 1 1 1 1\ntruncated 5 10', 2, 1),
             ('truncated-normal', b'truncated 2 2 1 1 0 0', 2, 0)]
    for name, body, expected, rows in cases:
        result = subprocess.run([str(binary)], input=body, capture_output=True, timeout=10)
        verify.need(result.returncode == expected and len(result.stdout.splitlines()) == rows,
                    'Parser control failed: ' + name)
        if name.endswith('truncated-header'):
            verify.need(b'truncated or malformed input header' in result.stderr, 'Header fixture missed its invariant')
        (out / (name + '.stdout')).write_bytes(result.stdout)
        (out / (name + '.stderr')).write_bytes(result.stderr)
        parser_results.append({'case': name, 'returncode': result.returncode, 'preserved_rows': rows})
    probe = out / 'termination_probe.py'
    probe.write_text(PROBE_SOURCE)
    termination = []
    for name in ['SIGTERM', 'SIGHUP', 'SIGQUIT', 'SIGINT', 'cleanup-timeout', 'cleanup-exception']:
        target = out / name
        mode = name.removeprefix('cleanup-') if name.startswith('cleanup-') else 'signal'
        process = subprocess.Popen([sys.executable, '-B', str(probe), str(target), str(verify.HERE), mode],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        begin = time.monotonic()
        spawned = target / 'child.spawn.json'
        child_pid = None
        try:
            while not spawned.exists() and time.monotonic() - begin < 5:
                verify.need(process.poll() is None, 'Termination fixture exited before child spawn')
                time.sleep(0.01)
            verify.need(spawned.exists(), 'Termination fixture did not spawn a child')
            child_pid = verify.read_json(spawned)['pid']
            expected_signal = signal.SIGTERM if mode != 'signal' else getattr(signal, name)
            if mode == 'signal':
                os.kill(process.pid, expected_signal)
            stdout, stderr = process.communicate(timeout=5)
            (out / (name + '.stdout')).write_bytes(stdout)
            (out / (name + '.stderr')).write_bytes(stderr)
            record = verify.read_json(target / 'child.process.json')
            verify.need(process.returncode == 2 and record['waited'] and
                        record['interruption_signal'] == int(expected_signal),
                        'Signal was not routed through recorded cleanup')
            interruption = verify.read_json(target / 'INTERRUPTED.json')
            if mode != 'signal':
                verify.need(interruption['injected_at_cleanup_entry'], 'Cleanup-entry signal was never injected')
            verify.need(record['pid'] == child_pid and absent(child_pid), 'Owned child survived handled termination')
            try:
                os.killpg(child_pid, 0)
            except ProcessLookupError:
                pass
            else:
                raise ValueError('Owned child process group survived termination')
            termination.append({'signal': name, 'wrapper_returncode': process.returncode,
                                'child_pid': child_pid, 'waited_and_absent': True,
                                'injected_at_cleanup_entry': interruption['injected_at_cleanup_entry'],
                                'elapsed_seconds': time.monotonic()-begin})
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            if child_pid is not None and not absent(child_pid):
                os.killpg(child_pid, signal.SIGKILL)
    result = {'status': 'PASS_DISTINGUISHING_PARSER_AND_TERMINATION_CONTROLS',
              'parser_cases': parser_results, 'real_signal_cases': termination,
              'scope': 'Catchable signals and complete header framing; uncatchable host loss is outside this fixture.'}
    verify.write_json(out / 'RESULT.json', result)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
