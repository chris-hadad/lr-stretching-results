"""POSIX process-group and signal controls for the publication runtime."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / 'tooling/whole_rank_six/runtime.py'
spec = importlib.util.spec_from_file_location('publication_runtime_under_test', RUNTIME_PATH)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
SIGNALS = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)


def handlers():
    return {sig: signal.getsignal(sig) for sig in SIGNALS}


def run_python(code, *, timeout=3, stdout=subprocess.DEVNULL):
    return runtime.run_owned([sys.executable, '-B', '-c', code], stdout=stdout,
                             stderr=subprocess.DEVNULL, timeout=timeout, env=None)


class PublicationRuntimeTests(unittest.TestCase):
    def test_success_nonzero_and_normal_child_signal_mask(self):
        before = handlers()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'mask.json'
            code = ('import json,signal;'
                    'print(json.dumps([int(s) for s in '
                    'signal.pthread_sigmask(signal.SIG_BLOCK, [])]))')
            with output.open('x') as stream:
                success = run_python(code, stdout=stream)
            self.assertEqual(success['exit'], 0)
            self.assertEqual(set(success), {'argv', 'pid', 'exit', 'seconds',
                                            'child_waited', 'owned_process_group_exited'})
            self.assertEqual(success['argv'][0], sys.executable)
            self.assertTrue(success['child_waited'])
            self.assertTrue(success['owned_process_group_exited'])
            self.assertGreaterEqual(success['seconds'], 0)
            self.assertFalse(runtime.group_exists(success['pid']))
            self.assertFalse(set(json.loads(output.read_text())) & set(SIGNALS))
            self.assertEqual(handlers(), before)

            nonzero = run_python('import sys;sys.exit(7)')
            self.assertEqual(nonzero['exit'], 7)
            self.assertTrue(nonzero['owned_process_group_exited'])
            self.assertFalse(runtime.group_exists(nonzero['pid']))
            self.assertEqual(handlers(), before)

            unbounded = run_python('print(1)', timeout=None)
            self.assertEqual(unbounded['exit'], 0)
            self.assertFalse(runtime.group_exists(unbounded['pid']))
            self.assertEqual(handlers(), before)

    def test_timeout_and_descendant_cleanup_restore_handlers(self):
        before = handlers()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            timeout_pid = root / 'timeout.pid'
            code = ('import os,time;from pathlib import Path;'
                    f'Path({str(timeout_pid)!r}).write_text(str(os.getpid()));'
                    'time.sleep(30)')
            with self.assertRaises(subprocess.TimeoutExpired):
                run_python(code, timeout=0.4)
            self.assertTrue(timeout_pid.is_file())
            self.assertFalse(runtime.group_exists(int(timeout_pid.read_text())))
            self.assertEqual(handlers(), before)

            descendant_pids = root / 'descendant.pids'
            code = ('import os,subprocess,sys;from pathlib import Path;'
                    "child=subprocess.Popen([sys.executable,'-B','-c',"
                    "'import time;time.sleep(30)']);"
                    f'Path({str(descendant_pids)!r}).write_text('
                    'str(os.getpid())+" "+str(child.pid))')
            with self.assertRaisesRegex(RuntimeError, 'live descendant'):
                run_python(code)
            self.assertTrue(descendant_pids.is_file())
            leader_pid, descendant_pid = map(int, descendant_pids.read_text().split())
            self.assertGreater(descendant_pid, 0)
            self.assertFalse(runtime.group_exists(leader_pid))
            self.assertEqual(handlers(), before)

    def test_term_hup_int_during_active_child(self):
        for signum in SIGNALS:
            with self.subTest(signal=signum):
                with tempfile.TemporaryDirectory() as temporary:
                    pid_path = Path(temporary) / 'active.pid'
                    code = ('import os,time;from pathlib import Path;'
                            f'Path({str(pid_path)!r}).write_text(str(os.getpid()));'
                            'time.sleep(30)')
                    original = handlers()
                    outside = []
                    stop = threading.Event()

                    def prior_handler(received, _frame):
                        outside.append(received)

                    def send_after_launch():
                        deadline = time.monotonic() + 5
                        while not stop.is_set() and not pid_path.is_file() and time.monotonic() < deadline:
                            time.sleep(0.01)
                        if not stop.is_set() and pid_path.is_file():
                            os.kill(os.getpid(), signum)

                    thread = threading.Thread(target=send_after_launch)
                    try:
                        for sig in SIGNALS:
                            signal.signal(sig, prior_handler)
                        previous = handlers()
                        thread.start()
                        with self.assertRaisesRegex(KeyboardInterrupt, 'Interrupted by signal'):
                            run_python(code, timeout=6)
                        self.assertTrue(pid_path.is_file())
                        self.assertFalse(runtime.group_exists(int(pid_path.read_text())))
                        self.assertEqual(handlers(), previous)
                        self.assertFalse(outside)
                    finally:
                        stop.set()
                        if thread.ident is not None:
                            thread.join(timeout=6)
                        for sig, handler in original.items():
                            signal.signal(sig, handler)
                        self.assertFalse(thread.is_alive())

    def test_signal_during_popen_assignment_and_repeated_cleanup(self):
        original = handlers()
        outside = []
        process = None
        true_popen = runtime.subprocess.Popen
        true_stop = runtime.stop_group

        def prior_handler(signum, _frame):
            outside.append(signum)

        def launch(*args, **kwargs):
            nonlocal process
            process = true_popen(*args, **kwargs)
            os.kill(os.getpid(), signal.SIGTERM)
            return process

        def repeated_cleanup(child):
            os.kill(os.getpid(), signal.SIGHUP)
            os.kill(os.getpid(), signal.SIGINT)
            true_stop(child)

        try:
            for sig in SIGNALS:
                signal.signal(sig, prior_handler)
            previous = handlers()
            with mock.patch.object(runtime.subprocess, 'Popen', launch), \
                 mock.patch.object(runtime, 'stop_group', repeated_cleanup):
                with self.assertRaisesRegex(KeyboardInterrupt, 'Interrupted by signal'):
                    run_python('import time;time.sleep(30)')
            self.assertIsNotNone(process)
            self.assertFalse(runtime.group_exists(process.pid))
            self.assertEqual(handlers(), previous)
            self.assertFalse(outside)
        finally:
            for sig, handler in original.items():
                signal.signal(sig, handler)
            if process is not None and runtime.group_exists(process.pid):
                true_stop(process)

    def test_popen_error_restores_handlers(self):
        before = handlers()
        with mock.patch.object(runtime.subprocess, 'Popen', side_effect=OSError('launch refused')) as launch:
            with self.assertRaisesRegex(OSError, 'launch refused'):
                run_python('print(1)')
        launch.assert_called_once()
        self.assertEqual(handlers(), before)

    def test_signal_during_first_handler_restore_is_not_lost(self):
        original = handlers()
        outside = []
        process = None
        calls = []
        true_signal = signal.signal
        true_popen = runtime.subprocess.Popen

        def prior_term(signum, _frame):
            outside.append(signum)

        def launch(*args, **kwargs):
            nonlocal process
            process = true_popen(*args, **kwargs)
            return process

        def signal_during_restore(signum, handler):
            calls.append(signum)
            if len(calls) == 4:
                self.assertEqual(signum, signal.SIGTERM)
                self.assertIs(handler, prior_term)
                self.assertIsNot(signal.getsignal(signum), prior_term)
                os.kill(os.getpid(), signal.SIGTERM)
            return true_signal(signum, handler)

        try:
            signal.signal(signal.SIGTERM, prior_term)
            previous = handlers()
            with mock.patch.object(runtime.signal, 'signal', signal_during_restore), \
                 mock.patch.object(runtime.subprocess, 'Popen', launch):
                with self.assertRaisesRegex(KeyboardInterrupt, 'Interrupted by signal'):
                    run_python('print(1)')
            self.assertEqual(calls, [*SIGNALS, *SIGNALS])
            self.assertEqual(handlers(), previous)
            self.assertFalse(outside)
            self.assertIsNotNone(process)
            self.assertFalse(runtime.group_exists(process.pid))
        finally:
            signal.signal(signal.SIGTERM, original[signal.SIGTERM])

    def test_cleanup_error_restores_handlers(self):
        before = handlers()
        process = None
        true_popen = runtime.subprocess.Popen
        true_stop = runtime.stop_group

        def launch(*args, **kwargs):
            nonlocal process
            process = true_popen(*args, **kwargs)
            return process

        def fail_after_cleanup(child):
            true_stop(child)
            raise RuntimeError('synthetic cleanup refusal')

        with mock.patch.object(runtime.subprocess, 'Popen', launch), \
             mock.patch.object(runtime, 'stop_group', fail_after_cleanup):
            with self.assertRaisesRegex(RuntimeError, 'synthetic cleanup refusal'):
                run_python('import time;time.sleep(30)', timeout=0.3)
        self.assertIsNotNone(process)
        self.assertFalse(runtime.group_exists(process.pid))
        self.assertEqual(handlers(), before)

    def test_non_main_thread_refuses_before_launch(self):
        before = handlers()
        caught = []

        def in_worker():
            try:
                run_python('print(1)')
            except BaseException as error:
                caught.append(error)

        with mock.patch.object(runtime.subprocess, 'Popen') as launch:
            thread = threading.Thread(target=in_worker)
            thread.start()
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            launch.assert_not_called()
        self.assertEqual(len(caught), 1)
        self.assertIsInstance(caught[0], RuntimeError)
        self.assertIn('main thread', str(caught[0]))
        self.assertEqual(handlers(), before)


if __name__ == '__main__':
    unittest.main()
