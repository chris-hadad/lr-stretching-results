"""Bounded real-child controls for the four public reproduction wrappers.

Run with the caller's TMPDIR using unittest discovery for this file.
No scientific input bundle is needed.
"""
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    'layered': 'results/layered-triangle/reproduce.py',
    'transport': 'results/transport-four-by-five/reproduce.py',
    'fresh': 'results/structural-positivity/replay/fresh_counts.py',
    'forcing': 'tooling/structural_certificates/f025/verify_forcing.py',
}
CHILD = r'''
import json, os, pathlib, signal, subprocess, sys, time
mode, marker, parent, signum = sys.argv[1:]
pathlib.Path(marker).write_text(str(os.getpid()))
if mode == 'mask':
    blocked = signal.pthread_sigmask(signal.SIG_BLOCK, [])
    print(json.dumps({'blocked': sorted(int(s) for s in blocked)}), flush=True)
elif mode == 'nonzero':
    print('synthetic nonzero', flush=True)
    sys.exit(7)
elif mode == 'leftover':
    subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(10)'],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    print('leader exiting with a descendant', flush=True)
elif mode in ('term', 'hup', 'alarm', 'usr1', 'repeat'):
    os.kill(int(parent), int(signum))
    time.sleep(10)
elif mode == 'timeout':
    time.sleep(10)
elif mode == 'stdin_resume':
    time.sleep(0.35)
    print(json.dumps({'stdin_bytes': len(sys.stdin.buffer.read())}), flush=True)
else:
    print(json.dumps({'ok': True}), flush=True)
'''


def group_exists(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def load(kind):
    path = ROOT / MODULES[kind]
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location('signal_path_' + kind, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def driver(kind, case, work):
    module = load(kind)
    signals = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]
    if kind in ('fresh', 'forcing'):
        signals.extend((signal.SIGALRM, signal.SIGUSR1))
    previous = {sig: signal.getsignal(sig) for sig in signals}
    real_popen = subprocess.Popen
    signum = {'term': signal.SIGTERM, 'hup': signal.SIGHUP,
              'alarm': signal.SIGALRM, 'usr1': signal.SIGUSR1,
              'repeat': signal.SIGTERM}.get(case, 0)
    child_case = 'success' if case in ('launch', 'launch_write', 'receipt_signal') else case
    argv = [sys.executable, '-B', '-c', CHILD, child_case,
            str(work / 'child-pid'), str(os.getpid()), str(int(signum))]
    original_save = getattr(module, 'save', None)
    original_write = getattr(module, 'write_new', None)
    def observed_popen(*args, **kwargs):
        proc = real_popen(*args, **kwargs)
        (work / 'launched-pid').write_text(str(proc.pid))
        if case == 'launch':
            os.kill(os.getpid(), signal.SIGTERM)
        return proc
    def save_with_failure(path, value):
        if kind == 'fresh':
            original_save(path, value)
        else:
            original_write(path, value)
        if Path(path).name == 'launch.json':
            raise OSError('synthetic launch record failure')
    def save_with_signal(path, value):
        if kind == 'transport':
            original_save(path, value)
        elif kind == 'fresh':
            original_save(path, value)
        else:
            original_write(path, value)
        if Path(path).name in ('receipt.json', 'probe.run.json'):
            os.kill(os.getpid(), signal.SIGTERM)
    def repeated_signals(pgid, sig):
        real_killpg(pgid, sig)
        if sig == signal.SIGTERM and not (work / 'repeat-injected').exists():
            (work / 'repeat-injected').write_text('HUP and INT during group cleanup\n')
            os.kill(os.getpid(), signal.SIGHUP)
            os.kill(os.getpid(), signal.SIGINT)
    real_killpg = os.killpg
    report = {'kind': kind, 'case': case}
    module.subprocess.Popen = observed_popen
    if case == 'launch_write' and kind in ('fresh', 'forcing'):
        if kind == 'fresh':
            module.save = save_with_failure
        else:
            module.write_new = save_with_failure
    if case == 'receipt_signal' and kind != 'layered':
        if kind in ('transport', 'fresh'):
            module.save = save_with_signal
        else:
            module.write_new = save_with_signal
    if case == 'repeat':
        module.os.killpg = repeated_signals
    try:
        if kind == 'layered':
            result = module.run(argv, timeout=0.1 if case == 'timeout' else 5,
                                capture=True)
            report.update(returncode=result.returncode, stdout=result.stdout)
        elif kind == 'transport':
            module.run(argv, work, 'probe', timeout=0.1 if case == 'timeout' else 5)
        elif kind == 'fresh':
            receipt, raw = module.child(argv, work / 'probe',
                                        0.1 if case == 'timeout' else 5,
                                        b'held input' if case == 'stdin_resume' else b'')
            report.update(returncode=receipt['returncode'], stdout=raw.decode())
        else:
            receipt, raw = module.child(argv, work / 'probe',
                                        0.1 if case == 'timeout' else 5)
            report.update(returncode=receipt['returncode'], stdout=raw.decode())
    except BaseException as exc:
        report.update(exception=type(exc).__name__, message=str(exc))
    report['handlers_restored'] = all(signal.getsignal(sig) == handler
                                      for sig, handler in previous.items())
    report['active_cleared'] = getattr(module, 'ACTIVE', None) is None
    report['repeat_injected'] = (work / 'repeat-injected').exists()
    receipt_path = work / ('probe.run.json' if kind == 'transport' else 'probe/receipt.json')
    report['receipt_exists'] = receipt_path.is_file()
    if receipt_path.is_file():
        report['receipt'] = json.loads(receipt_path.read_text())
    output_path = work / ('probe.stdout.txt' if kind == 'transport' else 'probe/stdout.txt')
    if output_path.is_file():
        report['stdout'] = output_path.read_text()
    (work / 'driver.json').write_text(json.dumps(report, sort_keys=True) + '\n')


class PublicationSignalPaths(unittest.TestCase):
    def run_driver(self, kind, case):
        with tempfile.TemporaryDirectory(prefix='publication-signals-') as scratch:
            work = Path(scratch)
            command = [sys.executable, '-B', str(Path(__file__).resolve()),
                       '--driver', kind, case, str(work)]
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, start_new_session=True,
                                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            timed_out = False
            try:
                stdout, stderr = proc.communicate(timeout=12)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                stdout, stderr = proc.communicate(timeout=2)
                timed_out = True
            launched = work / 'launched-pid'
            leftover = False
            pgid = None
            if launched.is_file():
                pgid = int(launched.read_text())
                leftover = group_exists(pgid)
                if leftover:
                    try:
                        os.killpg(pgid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    until = time.monotonic() + 2
                    while group_exists(pgid) and time.monotonic() < until:
                        time.sleep(0.05)
            self.assertFalse(timed_out, f'{kind}/{case} driver hung: {stdout} {stderr}')
            self.assertEqual(proc.returncode, 0, f'{kind}/{case}: {stdout} {stderr}')
            report_path = work / 'driver.json'
            self.assertTrue(report_path.is_file(), f'{kind}/{case}: {stdout} {stderr}')
            report = json.loads(report_path.read_text())
            self.assertFalse(leftover, f'{kind}/{case} left group {pgid}')
            self.assertTrue(report['handlers_restored'], f'{kind}/{case} changed handlers')
            self.assertTrue(report['active_cleared'], f'{kind}/{case} retained ACTIVE')
            return report

    def test_success_nonzero_and_unblocked_child_masks(self):
        for kind in MODULES:
            with self.subTest(kind=kind, case='success'):
                result = self.run_driver(kind, 'success')
                self.assertNotIn('exception', result)
                self.assertIn('"ok": true', result['stdout'])
                if kind != 'layered':
                    self.assertTrue(result['receipt_exists'])
            with self.subTest(kind=kind, case='nonzero'):
                result = self.run_driver(kind, 'nonzero')
                if kind == 'transport':
                    self.assertEqual(result['exception'], 'RuntimeError')
                    self.assertEqual(result['receipt']['returncode'], 7)
                else:
                    self.assertEqual(result['returncode'], 7)
            with self.subTest(kind=kind, case='mask'):
                result = self.run_driver(kind, 'mask')
                self.assertNotIn('exception', result)
                blocked = set(json.loads(result['stdout'])['blocked'])
                self.assertTrue(blocked.isdisjoint({signal.SIGTERM, signal.SIGINT,
                                                    signal.SIGHUP, signal.SIGALRM}))

    def test_timeout_and_normal_descendant_refusal(self):
        for kind in MODULES:
            with self.subTest(kind=kind, case='timeout'):
                result = self.run_driver(kind, 'timeout')
                self.assertIn('exception', result)
                if kind in ('fresh', 'forcing'):
                    self.assertTrue(result['receipt']['timed_out'])
                    self.assertTrue(result['receipt']['group_absent'])
                else:
                    self.assertFalse(result['receipt_exists'])
            with self.subTest(kind=kind, case='leftover'):
                result = self.run_driver(kind, 'leftover')
                self.assertIn('exception', result)
                self.assertIn('descendant', result['message'])
                self.assertFalse(result['receipt_exists'])

    def test_fresh_stdin_survives_multiple_communicate_polls(self):
        result = self.run_driver('fresh', 'stdin_resume')
        self.assertNotIn('exception', result)
        self.assertEqual(json.loads(result['stdout'])['stdin_bytes'], len(b'held input'))

    def test_term_hup_launch_and_repeated_cleanup_signals(self):
        for kind in MODULES:
            for case in ('term', 'hup', 'launch', 'repeat'):
                with self.subTest(kind=kind, case=case):
                    result = self.run_driver(kind, case)
                    self.assertIn('exception', result)
                    self.assertIn('Interrupted by signal', result['message'])
                    if case == 'repeat':
                        self.assertTrue(result['repeat_injected'])
                    if kind in ('fresh', 'forcing'):
                        self.assertTrue(result['receipt_exists'])
                        self.assertTrue(result['receipt']['interruption'])
                        self.assertTrue(result['receipt']['group_absent'])
                    else:
                        self.assertFalse(result['receipt_exists'])
        for kind in ('fresh', 'forcing'):
            with self.subTest(kind=kind, case='alarm'):
                result = self.run_driver(kind, 'alarm')
                self.assertIn('Interrupted by signal', result['message'])
                self.assertTrue(result['receipt']['group_absent'])
            with self.subTest(kind=kind, case='usr1'):
                result = self.run_driver(kind, 'usr1')
                self.assertIn('Interrupted by signal', result['message'])
                self.assertTrue(result['receipt']['group_absent'])
            with self.subTest(kind=kind, case='launch_write'):
                result = self.run_driver(kind, 'launch_write')
                self.assertIn('synthetic launch record failure', result['message'])
                self.assertFalse(result['receipt_exists'])
        for kind in ('transport', 'fresh', 'forcing'):
            with self.subTest(kind=kind, case='receipt_signal'):
                result = self.run_driver(kind, 'receipt_signal')
                self.assertIn('Interrupted by signal', result['message'])
                self.assertFalse(result['receipt_exists'])

    def test_main_restores_original_handlers(self):
        for kind in MODULES:
            with self.subTest(kind=kind):
                module = load(kind)
                signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGALRM)
                previous = {sig: signal.getsignal(sig) for sig in signals}
                argv = ['reproduce.py', '--quick'] if kind == 'layered' else (
                    ['reproduce.py', '--data', '.', '--scratch', '.'] if kind == 'transport' else (
                    ['fresh_counts.py', 'gap', '--output', 'unused', '--deadline', '1'] if kind == 'fresh' else
                    ['verify_forcing.py', '--data-root', '.', '--_rank', '6', '--deadline', '1']))
                method = '_replay' if kind in ('layered', 'transport') else (
                    'run' if kind == 'fresh' else '_verify')
                with patch.object(sys, 'argv', argv), patch.object(module, method,
                        side_effect=RuntimeError('test stop')):
                    with self.assertRaisesRegex(RuntimeError, 'test stop'):
                        module.main()
                self.assertTrue(all(signal.getsignal(sig) == handler
                                    for sig, handler in previous.items()))
                if kind == 'forcing':
                    self.assertEqual(signal.getitimer(signal.ITIMER_REAL)[0], 0)


if __name__ == '__main__':
    if len(sys.argv) == 5 and sys.argv[1] == '--driver':
        driver(sys.argv[2], sys.argv[3], Path(sys.argv[4]))
    else:
        unittest.main()
