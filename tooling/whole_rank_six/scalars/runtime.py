"""Bounded POSIX child groups for the published verification commands."""
from __future__ import annotations
import os
import signal
import subprocess
import threading
import time


def group_exists(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # A dying Darwin group can briefly return EPERM before ESRCH. Treat
        # this as present/unknown and keep waiting; never infer exit from it.
        return True


def stop_group(process, grace=5.0):
    """Stop only the new session created for this exact child and wait for exit."""
    pgid = process.pid
    if group_exists(pgid):
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    end = time.monotonic() + grace
    while time.monotonic() < end:
        process.poll()  # Reap the direct child even while descendants still exit.
        if not group_exists(pgid):
            process.wait()
            return
        time.sleep(0.05)
    if group_exists(pgid):
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=grace)
    end = time.monotonic() + grace
    while group_exists(pgid) and time.monotonic() < end:
        time.sleep(0.05)
    if group_exists(pgid):
        raise RuntimeError('owned process group did not exit: ' + str(pgid))


def run_owned(command, *, stdout, stderr, timeout, env):
    """Return an exit record only after the child and its whole group exit."""
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError('run_owned requires the main thread for signal supervision')
    signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)
    previous = {sig: signal.getsignal(sig) for sig in signals}
    interrupted = None

    def request_interrupt(signum, _frame):
        nonlocal interrupted
        interrupted = signum

    def check_interrupted():
        if interrupted is not None:
            raise KeyboardInterrupt('Interrupted by signal ' + str(interrupted))

    try:
        for sig in signals:
            signal.signal(sig, request_interrupt)
        check_interrupted()
        started = time.monotonic()
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   start_new_session=True, env=env)
        try:
            deadline = None if timeout is None else started + timeout
            while True:
                check_interrupted()
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    raise subprocess.TimeoutExpired(command, timeout)
                try:
                    rc = process.wait(timeout=0.2 if remaining is None else min(0.2, remaining))
                    break
                except subprocess.TimeoutExpired:
                    continue
            check_interrupted()
            if group_exists(process.pid):
                raise RuntimeError('command left a live descendant: ' + str(process.pid))
            check_interrupted()
        except BaseException:
            stop_group(process)
            raise
        result = {'argv': command, 'pid': process.pid, 'exit': rc,
                  'seconds': time.monotonic() - started, 'child_waited': True,
                  'owned_process_group_exited': True}
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    check_interrupted()
    return result
