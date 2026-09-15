"""POSIX process containment for bounded local native-engine commands.

The parent stays outside the native interpreter. Children must retain the new
process group: this is a deadline/cleanup boundary, not a sandbox for hostile
code which calls setsid/setpgid. Never adopt a detached-engine topology here.
No multiprocessing children, shell evaluation, or background supervisor are used.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import math
import multiprocessing
import os
from pathlib import Path
import selectors
import signal
import subprocess
import threading
import time
from typing import Literal, Mapping, Protocol, Sequence


STOP_SIGNALS = (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT)


class Cancellation(Protocol):
    def is_set(self) -> bool: ...


class _OwnedPopen(subprocess.Popen):
    def __init__(self, owner, *args, **kwargs):
        # Publish the handle before initialization can create an OS child.
        owner.append(self)
        super().__init__(*args, **kwargs)


@contextmanager
def _defer_cancellation():
    """Defer parent INT/TERM/HUP/QUIT until cleanup without blocking them in the child.

    Caught signal dispositions reset on exec; the signal mask is unchanged.
    Keeping the handlers through cleanup also covers repeated cancellation.
    """
    pending, previous = [], {}

    def defer(signum, frame):
        if previous[signum] != signal.SIG_IGN:
            pending.append((signum, frame))

    try:
        for sig in STOP_SIGNALS:
            previous[sig] = signal.getsignal(sig)
            signal.signal(sig, defer)
        yield pending
    finally:
        # No child can be acquired here. Blocking only during restoration
        # prevents one restored handler interrupting restoration of the other.
        mask = signal.pthread_sigmask(signal.SIG_BLOCK, set(previous))
        try:
            for sig, handler in previous.items():
                signal.signal(sig, handler)
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, mask)
        # A received signal is returned as a partial result after cleanup.
        # The actual outer CLI records that result and exits with its signal.


@dataclass(frozen=True)
class CommandBinding:
    """Frozen *actual* child invocation and caller-declared source closure.

    Digests are supplied by the release owner, never silently blessed here.
    Hashes are checked before spawn and after cleanup. This does not replace
    exclusive ownership/immutability of source paths during execution.
    """

    argv: tuple[str, ...]
    cwd: str
    env: tuple[tuple[str, str], ...]
    source_sha256: tuple[tuple[str, str], ...]

    @property
    def sha256(self) -> str:
        payload = (self.argv, self.cwd, self.env, self.source_sha256)
        return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class ContainedResult:
    """Execution evidence only; ``complete`` does not certify engine mathematics."""

    status: Literal["complete", "partial", "error"]
    reason: str
    argv: tuple[str, ...]
    cwd: str
    pid: int | None
    returncode: int | None
    stdout: bytes
    stderr: bytes
    elapsed_s: float
    cleanup_verified: bool
    binding_sha256: str | None
    detail: str | None = None


def _invocation(argv: Sequence[str], cwd: str | os.PathLike[str], env: Mapping[str, str]):
    if isinstance(argv, (str, bytes)) or not argv or any(not isinstance(arg, str) for arg in argv):
        raise ValueError("argv must be a nonempty sequence of strings")
    command = tuple(argv)
    if not os.path.isabs(command[0]) or any("\0" in arg for arg in command):
        raise ValueError("argv needs an absolute executable and no NUL bytes")
    if not os.path.isabs(cwd):
        raise ValueError("cwd must be absolute")
    directory = str(Path(cwd).resolve(strict=True))
    if not Path(directory).is_dir():
        raise ValueError("cwd must be a directory")
    environment = dict(env)
    if any(not isinstance(k, str) or not isinstance(v, str) or not k or "=" in k
           or "\0" in k or "\0" in v for k, v in environment.items()):
        raise ValueError("env must contain valid string names and values")
    if environment.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise ValueError("explicit env must set PYTHONDONTWRITEBYTECODE=1")
    return command, directory, environment


def bind_command(
    argv: Sequence[str], *, cwd: str | os.PathLike[str], env: Mapping[str, str],
    source_sha256: Mapping[str | os.PathLike[str], str],
) -> CommandBinding:
    """Bind argv/cwd/env and an explicit, nonempty source digest roster.

    Include the actual script/module and its transitive local dependencies.
    For a private closure, argv and PYTHONPATH must select that exact closure.
    Interpreter/tool binaries can also be included in the digest roster.
    """
    command, directory, environment = _invocation(argv, cwd, env)
    sources = []
    for path, digest in source_sha256.items():
        if not os.path.isabs(path):
            raise ValueError("source paths must be absolute")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("source digests must be lowercase SHA256 hex")
        sources.append((os.fspath(path), digest))
    if not sources:
        raise ValueError("binding requires a nonempty source digest roster")
    return CommandBinding(command, directory, tuple(sorted(environment.items())), tuple(sorted(sources)))


def _binding_error(binding: CommandBinding, argv, cwd, env) -> str | None:
    if (binding.argv, binding.cwd, binding.env) != (argv, cwd, tuple(sorted(env.items()))):
        return "actual child argv/cwd/env does not match the frozen binding"
    for path, digest in binding.source_sha256:
        try:
            with open(path, "rb") as source:
                actual = hashlib.file_digest(source, "sha256").hexdigest()
        except OSError as exc:
            return f"cannot read bound source {path}: {exc}"
        if actual != digest:
            return f"bound source digest mismatch: {path}"
    return None


def _exited(pid: int) -> bool:
    # WNOWAIT reserves the child PID until *all* group signals have finished.
    # Popen.poll/communicate would reap it and permit unrelated PGID reuse.
    return os.waitid(os.P_PID, pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None


def _read_ready(selector, output, limit: int, wait: float) -> bool:
    """Read at most one bounded chunk per ready pipe; return output overflow."""
    overflow = False
    for key, _ in selector.select(wait):
        try:
            chunk = os.read(key.fd, 65536)
        except BlockingIOError:
            continue
        if not chunk:
            selector.unregister(key.fileobj)
            continue
        room = limit - sum(map(len, output))
        output[key.data].extend(chunk[:room])
        overflow |= len(chunk) > room
    return overflow


def _group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # macOS can report EPERM for a group containing only exiting/zombie
        # members. It is not proof of absence: retry until ESRCH or refuse.
        return True
    return True


def _cleanup(process: subprocess.Popen, grace_s: float, cleanup_s: float) -> str | None:
    """Signal only the reserved child group; wait direct child, then verify no group.

    Cleanup has its own bounded grace. All four ordinary termination signals are deferred in this thread
    until it finishes, so an ordinary parent cancellation cannot skip the reap.
    A supervisor SIGKILL or an unkillable OS process is outside this guarantee.
    """
    previous = signal.pthread_sigmask(signal.SIG_BLOCK, set(STOP_SIGNALS))
    try:
        # Refuse signaling if another reaper unexpectedly consumed our child.
        _exited(process.pid)
        signal_errors = []
        # Do not reap, including on the normal-success path, before this block.
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                pass
            except OSError as exc:
                signal_errors.append(f"signal {sig.name}: {exc}")
            if sig == signal.SIGTERM:
                time.sleep(grace_s)
        stop = time.monotonic() + cleanup_s
        try:
            process.wait(timeout=max(0.001, stop - time.monotonic()))
        except subprocess.TimeoutExpired:
            return "; ".join(signal_errors + ["direct child did not exit after SIGKILL"])
        # No more signals after wait: a later PGID reuse cannot kill bystanders.
        while _group_exists(process.pid):
            if time.monotonic() >= stop:
                return "process group still exists after SIGKILL and direct-child wait"
            time.sleep(0.01)
        # A raced ESRCH/EPERM while members exit is harmless only once the
        # direct child was reaped AND group absence was independently observed.
        return None
    except OSError as exc:
        return f"cleanup failed: {type(exc).__name__}: {exc}"
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, previous)


def run_contained(
    argv: Sequence[str], *, cwd: str | os.PathLike[str], env: Mapping[str, str],
    timeout_s: float, binding: CommandBinding | None = None,
    cancel: Cancellation | None = None, max_output_bytes: int = 4 * 1024 * 1024,
    terminate_grace_s: float = 0.0, cleanup_timeout_s: float = 2.0,
    on_start=None,
) -> ContainedResult:
    """Run one explicit command with a monotonic native-process deadline.

    At the deadline or cancellation the entire owned group gets TERM, then KILL
    after ``terminate_grace_s`` (zero by default for immediate hard cutoff). Cleanup can
    add up to that grace plus ``cleanup_timeout_s`` to elapsed time. Both output
    pipes share a strict byte budget. Nonzero exit/I/O/source/cleanup failures are
    errors; deadline, cancellation, and output overflow are partial outcomes.

    BaseException, including KeyboardInterrupt, propagates only after cleanup.
    An optional protected on_start callback may record child identity; numerical
    result parsing occurs only after cleanup. A
    caller must refuse adoption unless status is complete and cleanup_verified,
    then validate the engine's own evidence. A cleanup error requires stopping
    further work and reconciling the returned PID. The supervisor must run this
    on its main thread; daemon workers are refused. INT/TERM/HUP/QUIT are deferred through
    acquisition and cleanup, returned to the outer CLI after cleanup.
    """
    if os.name != "posix" or not all(hasattr(os, name) for name in ("waitid", "WNOWAIT", "P_PID")):
        raise RuntimeError("containment requires POSIX waitid/WNOWAIT")
    if multiprocessing.current_process().daemon:
        raise RuntimeError("containment must run in a non-daemon supervisor")
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError("containment must run on the supervisor main thread")
    if signal.pthread_sigmask(signal.SIG_BLOCK, set()) & set(STOP_SIGNALS):
        raise RuntimeError("supervisor termination signals must be unblocked before child acquisition")
    if signal.getsignal(signal.SIGCHLD) != signal.SIG_DFL:
        raise RuntimeError("containment requires exclusive child reaping and default SIGCHLD")
    for name, value, positive in (("timeout_s", timeout_s, True),
                                  ("terminate_grace_s", terminate_grace_s, False),
                                  ("cleanup_timeout_s", cleanup_timeout_s, True)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        if value < 0 or (positive and value == 0):
            raise ValueError(f"{name} is out of range")
    if type(max_output_bytes) is not int or max_output_bytes <= 0:
        raise ValueError("max_output_bytes must be a positive integer")
    command, directory, environment = _invocation(argv, cwd, env)
    started = time.monotonic()
    output = [bytearray(), bytearray()]
    process = None
    reason, detail, cleanup_error = "exited", None, None

    def result(status, why, message=None):
        return ContainedResult(status, why, command, directory,
                               getattr(process, "pid", None), getattr(process, "returncode", None),
                               bytes(output[0]), bytes(output[1]), time.monotonic() - started,
                               cleanup_error is None, binding.sha256 if binding else None, message)

    if binding:
        detail = _binding_error(binding, command, directory, environment)
        if detail:
            return result("error", "source_mismatch", detail)
    if cancel is not None and cancel.is_set():
        return result("partial", "cancelled")
    deadline = time.monotonic() + timeout_s
    owner = []
    with selectors.DefaultSelector() as selector, _defer_cancellation() as pending:
        try:
            _OwnedPopen(owner, command, cwd=directory, env=environment, stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0,
                        close_fds=True, start_new_session=True, shell=False)
            process = owner[0]
            if on_start is not None:
                on_start(process.pid)
            for index, pipe in enumerate((process.stdout, process.stderr)):
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, index)
            while True:
                if pending or (cancel is not None and cancel.is_set()):
                    reason = "cancelled"
                    if pending:
                        detail = "signal:" + str(pending[0][0])
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    reason = "deadline"
                    break
                if _read_ready(selector, output, max_output_bytes, min(0.02, remaining)):
                    reason = "output_limit"
                    break
                if time.monotonic() >= deadline:
                    reason = "deadline"
                    break
                if _exited(process.pid):
                    break
        except OSError as exc:
            reason = "spawn_error" if process is None else "io_error"
            detail = f"{type(exc).__name__}: {exc}"
        finally:
            process = owner[0] if owner else None
            try:
                if getattr(process, "pid", None) is not None:
                    if process.returncode is None:
                        cleanup_error = _cleanup(process, terminate_grace_s, cleanup_timeout_s)
                    elif _group_exists(process.pid):
                        # Popen already reaps a child whose exec failed. Never
                        # signal that unreserved PGID, even on a launch error.
                        cleanup_error = "process group remains after constructor reaped failed child"
                # Once the group has exited, bounded nonblocking reads cannot
                # wait for a native child. Keep draining queued output to EOF.
                while cleanup_error is None and selector.get_map():
                    before = len(selector.get_map()), sum(map(len, output))
                    if _read_ready(selector, output, max_output_bytes, 0):
                        reason = "output_limit"
                    after = len(selector.get_map()), sum(map(len, output))
                    if before == after:
                        break
            except OSError as exc:
                reason, detail = "io_error", f"{type(exc).__name__}: {exc}"
            finally:
                for name in ("stdout", "stderr"):
                    pipe = getattr(process, name, None)
                    if pipe is not None:
                        pipe.close()
    if pending:
        reason = "cancelled"
        detail = "signal:" + str(pending[0][0])
    if cleanup_error:
        return result("error", "cleanup_error", cleanup_error)
    if binding:
        source_error = _binding_error(binding, command, directory, environment)
        if source_error:
            return result("error", "source_mismatch", source_error)
    if reason in {"deadline", "cancelled", "output_limit"}:
        return result("partial", reason, detail)
    if reason in {"spawn_error", "io_error"} or process.returncode != 0:
        return result("error", reason if reason in {"spawn_error", "io_error"} else "nonzero_exit", detail)
    return result("complete", "exited")
