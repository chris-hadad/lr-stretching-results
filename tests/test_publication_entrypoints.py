"""Regression checks for public replay entrypoint safety."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TRANSPORT = ROOT / 'results/transport-four-by-five'
STRUCTURAL = ROOT / 'tooling/structural_certificates'
sys.path.insert(0, str(STRUCTURAL))
import reader_replay as reader
import runtime


def fixture_local_values(root: Path, negative: bool):
    data, work, module = (root / name for name in ('data', 'work', 'module'))
    for path in (data, work, module / 'src'):
        path.mkdir(parents=True)
    records = [{'p': 1, 'N': 1, 'q': 1, 'type': i,
                'alpha': '-1' if negative and i == 0 else '1'}
               for i in range(317)]
    (data / 'local-certificate.json').write_text(json.dumps(records))
    rows = [f'T1-1-1-{i} 1 {record["alpha"]} 0 0 0 0\n'
            for i, record in enumerate(records)]
    (work / 'bv-values.txt').write_text(''.join(rows))
    (work / 'bv-controls.txt').write_text('SIMPLEX-8 1 1 0 0 0 0\n')
    (work / 'bv-omit-eighth.txt').write_text('SIMPLEX-8 1 2 0 0 0 0\n')
    (module / 'src/CONTROL-EXPECTATIONS.json').write_text(
        json.dumps({'values': {'SIMPLEX-8': '1'}}))
    return data, work, module


def load_transport_join():
    sys.path.insert(0, str(TRANSPORT / 'src'))
    spec = importlib.util.spec_from_file_location('publication_transport_join',
                                                  TRANSPORT / 'src/join.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TransportEntryTests(unittest.TestCase):
    def test_all_assertion_entrypoints_refuse_optimization(self):
        entrypoints = [TRANSPORT / 'reproduce.py',
                       *(TRANSPORT / 'src' / name for name in (
                           'atlas_replay.py', 'encode_quadratic.py',
                           'verify_topology.py', 'join.py')),
                       *(ROOT / name for name in (
                           'results/five-capacity/reproduce.py',
                           'results/five-height-hives/interface_checker.py',
                           'results/five-height-hives/projection_controls.py',
                           'results/five-height-hives/sector_fields.py',
                           'results/gap-cap/reproduce.py',
                           'results/layered-triangle/scalar_controls.py',
                           'results/layered-triangle/top_strip.py',
                           'results/linear-coefficient-geometry/check_witness.py',
                           'results/linear-coefficient-geometry/tree_data.py',
                           'results/linear-coefficient-geometry/two_row_controls.py',
                           'tooling/whole_rank_six/closure/test_constructive_hive_closure.py'))]
        for path in entrypoints:
            for mode in ('-O', 'environment'):
                with self.subTest(path=path.name, mode=mode):
                    env = os.environ.copy()
                    env['PYTHONPATH'] = str(path.parent) + os.pathsep + env.get('PYTHONPATH', '')
                    argv = [sys.executable, '-B']
                    if mode == '-O':
                        argv.append('-O')
                    else:
                        env['PYTHONOPTIMIZE'] = '1'
                    result = subprocess.run([*argv, str(path)], env=env,
                                            capture_output=True, text=True,
                                            timeout=5)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn('Optimized Python is refused', result.stderr)

        for name in ('results/five-height-hives/interface_checker.py',
                     'tooling/whole_rank_six/closure/test_constructive_hive_closure.py'):
            with self.subTest(normal_help=name):
                path = ROOT / name
                env = os.environ.copy()
                env['PYTHONPATH'] = str(path.parent) + os.pathsep + env.get('PYTHONPATH', '')
                result = subprocess.run([sys.executable, '-B', str(path), '--help'],
                                        env=env, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('usage:', result.stdout.lower())

    def test_negative_local_fixture_and_unoptimized_valid_behavior(self):
        join = load_transport_join()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            valid = fixture_local_values(base / 'valid', negative=False)
            self.assertEqual(join.local_values(*valid)['minimum'], '1')
            invalid = fixture_local_values(base / 'negative', negative=True)
            with self.assertRaises(AssertionError):
                join.local_values(*invalid)

            refused = subprocess.run(
                [sys.executable, '-B', '-O', str(TRANSPORT / 'src/join.py'),
                 *map(str, invalid)], capture_output=True, text=True, timeout=5)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn('Optimized Python is refused', refused.stderr)

        help_result = subprocess.run(
            [sys.executable, '-B', str(TRANSPORT / 'reproduce.py'), '--help'],
            capture_output=True, text=True, timeout=5)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn('--data', help_result.stdout)


def controlled_reader_fixture(root: Path):
    module, data, output = (root / name for name in ('module', 'data', 'output'))
    module.mkdir()
    data.mkdir()
    for name in ('reader_replay.py', 'runtime.py'):
        shutil.copy2(STRUCTURAL / name, module / name)
    for name in ('verify_normal_certificates.py', 'verify_pro027_masks.py'):
        shutil.copy2(STRUCTURAL / name, module / name)
    (module / 'DATA-ASSET.json').write_text('{"fixture": true}\n')
    (module / 'JOBS.json').write_text(
        json.dumps({'schema': 'structural-certificates-job-roster-v1',
                    'stages': {}}) + '\n')
    (module / 'restore.py').write_text(
        "import os,sys,time\n"
        "from pathlib import Path\n"
        "out=Path(sys.argv[sys.argv.index('--out')+1])\n"
        "(out/'child.pid').write_text(str(os.getpid()))\n"
        "time.sleep(30)\n")
    return module, data, output


class ReaderCancellationTests(unittest.TestCase):
    def test_reader_optimized_refusal_and_supervisor_timeout(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            module, data, output = controlled_reader_fixture(root)
            refused = subprocess.run(
                [sys.executable, '-B', '-O', str(module / 'reader_replay.py'),
                 'calibrate', '--data', str(data), '--output-root', str(output)],
                capture_output=True, text=True, timeout=5)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn('Optimized Python is refused', refused.stderr)
            self.assertFalse(output.exists())

            pid_path = root / 'timeout.pid'
            code = ('import os,time;from pathlib import Path;'
                    f'Path({str(pid_path)!r}).write_text(str(os.getpid()));'
                    'time.sleep(30)')
            with self.assertRaises(subprocess.TimeoutExpired):
                reader.run_cancelable(
                    [sys.executable, '-B', '-c', code],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    timeout=0.4, env=None)
            self.assertTrue(pid_path.is_file())
            self.assertFalse(runtime.group_exists(int(pid_path.read_text())))

    def test_outer_cli_term_and_hup_clean_exact_child_group(self):
        for signum in (signal.SIGTERM, signal.SIGHUP):
            with self.subTest(signum=signum):
                with tempfile.TemporaryDirectory() as temporary:
                    module, data, output = controlled_reader_fixture(Path(temporary))
                    process = subprocess.Popen(
                        [sys.executable, '-B', str(module / 'reader_replay.py'),
                         'calibrate', '--data', str(data), '--output-root', str(output)],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    try:
                        pid_path = data / 'child.pid'
                        deadline = time.monotonic() + 5
                        while not pid_path.exists() and time.monotonic() < deadline:
                            self.assertIsNone(process.poll(), 'reader exited before child launch')
                            time.sleep(0.01)
                        self.assertTrue(pid_path.exists(), 'controlled child did not launch')
                        child_pgid = int(pid_path.read_text())
                        os.kill(process.pid, signum)
                        _, errors = process.communicate(timeout=8)
                        self.assertNotEqual(process.returncode, 0)
                        self.assertIn('Interrupted by signal', errors)
                        self.assertFalse(runtime.group_exists(child_pgid))
                        self.assertTrue((output / 'READER-RUN-IDENTITY.json').is_file())
                        self.assertTrue((output / 'ASSET-VERIFICATION-0001.json').is_file())
                        self.assertFalse(list(output.glob('INVOCATION-*.json')))
                    finally:
                        if process.poll() is None:
                            process.send_signal(signal.SIGTERM)
                            try:
                                process.communicate(timeout=3)
                            except subprocess.TimeoutExpired:
                                process.kill()
                                process.communicate(timeout=3)
                        if pid_path.is_file():
                            owned_pgid = int(pid_path.read_text())
                            if runtime.group_exists(owned_pgid):
                                os.killpg(owned_pgid, signal.SIGKILL)

    def test_launch_signal_and_repeated_cleanup_signals(self):
        previous = {sig: signal.getsignal(sig) for sig in reader.CANCEL_SIGNALS}
        child_pid = None
        child_process = None
        true_popen = reader.subprocess.Popen
        true_stop = reader.stop_group

        def request(signum, _frame):
            reader.cancel_signal = signum

        def launch(*args, **kwargs):
            nonlocal child_pid, child_process
            child = true_popen(*args, **kwargs)
            child_process = child
            child_pid = child.pid
            os.kill(os.getpid(), signal.SIGTERM)
            return child

        def cleanup(child):
            os.kill(os.getpid(), signal.SIGHUP)
            os.kill(os.getpid(), signal.SIGTERM)
            true_stop(child)

        try:
            reader.cancel_signal = None
            for sig in reader.CANCEL_SIGNALS:
                signal.signal(sig, request)
            with mock.patch.object(reader.subprocess, 'Popen', launch), \
                 mock.patch.object(reader, 'stop_group', cleanup):
                with self.assertRaises(KeyboardInterrupt):
                    reader.run_cancelable(
                        [sys.executable, '-B', '-c', 'import time; time.sleep(30)'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        timeout=3, env=None)
            self.assertIsNotNone(child_pid)
            self.assertFalse(runtime.group_exists(child_pid))
        finally:
            for sig, handler in previous.items():
                signal.signal(sig, handler)
            reader.cancel_signal = None
            if child_process is not None and runtime.group_exists(child_process.pid):
                true_stop(child_process)

    def test_main_restores_handlers_and_normal_supervisor_succeeds(self):
        before = {sig: signal.getsignal(sig) for sig in reader.CANCEL_SIGNALS}

        def interrupted_replay():
            self.assertTrue(all(signal.getsignal(sig) != before[sig]
                                for sig in reader.CANCEL_SIGNALS))
            os.kill(os.getpid(), signal.SIGTERM)
            reader.check_cancelled()

        with mock.patch.object(reader, 'replay', interrupted_replay):
            with self.assertRaises(KeyboardInterrupt):
                reader.main()
        self.assertEqual({sig: signal.getsignal(sig) for sig in reader.CANCEL_SIGNALS}, before)
        self.assertIsNone(reader.cancel_signal)
        result = reader.run_cancelable(
            [sys.executable, '-B', '-c', 'print("ok")'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=3, env=None)
        self.assertEqual(result['exit'], 0)
        self.assertTrue(result['child_waited'])
        self.assertTrue(result['owned_process_group_exited'])
        self.assertFalse(runtime.group_exists(result['pid']))


if __name__ == '__main__':
    unittest.main()
