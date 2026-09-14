"""Bounded POSIX child ownership from the reviewed rank-six certificate runner."""

import hashlib, json, os, signal, subprocess, time
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")


class Runner:
    def __init__(self, out, seconds):
        self.out, self.limit, self.used, self.jobs = out, seconds, 0.0, []
        self.active_child = None
        self.spawning = False
        self.cancelled_signal = None

    def wait_child(self, process, timeout):
        stop = time.monotonic() + timeout
        while True:
            if self.cancelled_signal is not None:
                raise InterruptedError(f"Terminated by signal {self.cancelled_signal}")
            remaining = stop - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(process.args, timeout)
            try:
                return process.wait(timeout=min(0.05, remaining))
            except subprocess.TimeoutExpired:
                continue

    def run(self, name, command, *, input_path=None, expected=0, deadline=120):
        if self.cancelled_signal is not None:
            raise InterruptedError(f"Terminated by signal {self.cancelled_signal}")
        remaining = self.limit - self.used
        need(remaining > 0, "Cumulative child-time allocation exhausted")
        timeout = min(deadline, remaining)
        stdout, stderr = self.out / (name + ".stdout"), self.out / (name + ".stderr")
        start = time.monotonic()
        write_json(
            self.out / (name + ".launch.json"),
            {
                "argv": command,
                "deadline_seconds": timeout,
                "input": str(input_path) if input_path else None,
                "input_sha256": digest(input_path) if input_path else None,
                "executable_sha256": digest(command[0])
                if Path(command[0]).is_file()
                else None,
            },
        )
        source = Path(input_path).open("rb") if input_path else open(os.devnull, "rb")
        process = None
        failure = None
        code = None
        waited = False
        try:
            with source, stdout.open("xb") as fo, stderr.open("xb") as fe:
                try:
                    # The signal handler records cancellation during Popen; it
                    # cannot raise before the returned child is under this guard.
                    self.spawning = True
                    process = subprocess.Popen(
                        command,
                        stdin=source,
                        stdout=fo,
                        stderr=fe,
                        start_new_session=True,
                    )
                    self.active_child = process
                    self.spawning = False
                    write_json(
                        self.out / (name + ".spawn.json"),
                        {"pid": process.pid, "process_group": process.pid},
                    )
                    if self.cancelled_signal is not None:
                        raise InterruptedError(
                            f"Terminated by signal {self.cancelled_signal}"
                        )
                    code = self.wait_child(process, timeout)
                    waited = True
                except subprocess.TimeoutExpired:
                    if process.poll() is None:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    process.wait()
                    waited = True
                    code = 124
                except BaseException as error:
                    failure = error
                    if process is not None:
                        if process.poll() is None:
                            try:
                                os.killpg(process.pid, signal.SIGKILL)
                            except ProcessLookupError:
                                pass
                        code = process.wait()
                        waited = True
                finally:
                    self.spawning = False
                    self.active_child = None
        finally:
            elapsed = time.monotonic() - start
            self.used += elapsed
        record = {
            "argv": command,
            "pid": process.pid if process else None,
            "returncode": code,
            "waited": waited,
            "elapsed_seconds": elapsed,
            "deadline_seconds": timeout,
            "stdout_sha256": digest(stdout),
            "stderr_sha256": digest(stderr),
            "interruption_signal": self.cancelled_signal,
            "failure": str(failure) if failure is not None else None,
        }
        self.jobs.append(record)
        write_json(self.out / (name + ".process.json"), record)
        if failure is not None:
            raise failure
        need(code == expected, f"{name} returned {code}; see preserved {stderr.name}")
        return stdout


def install_termination_handlers(runner):
    def terminate(signum, frame):
        runner.cancelled_signal = signum
        # Asynchronous exceptions cannot escape a cleanup handler while a
        # child is owned. wait_child observes this flag with bounded polling.
        if not runner.spawning and runner.active_child is None:
            raise InterruptedError(f"Terminated by signal {signum}")

    for name in ["SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT"]:
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), terminate)
