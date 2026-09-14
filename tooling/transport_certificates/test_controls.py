#!/usr/bin/env python3
"""Corruption and interruption checks, including termination of this harness."""

import argparse
import copy
from contextlib import contextmanager
from fractions import Fraction as F
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import arithmetic as a
import verify


class Cancellation:
    """Defer asynchronous exceptions until every owned runtime is under a guard."""

    def __init__(self):
        self.signal = None
        self.critical_depth = 0
        for name in ("SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT"):
            if hasattr(signal, name):
                signal.signal(getattr(signal, name), self.receive)

    def receive(self, signum, frame):
        self.signal = signum
        if self.critical_depth == 0:
            self.check()

    def check(self):
        if self.signal is not None:
            raise InterruptedError(
                f"Controls command terminated by signal {self.signal}"
            )

    @contextmanager
    def owned(self):
        self.critical_depth += 1
        try:
            yield
        finally:
            self.critical_depth -= 1


def group_alive(group):
    try:
        os.killpg(group, 0)
    except ProcessLookupError:
        return False
    return True


def kill_group(group):
    try:
        os.killpg(group, signal.SIGKILL)
    except ProcessLookupError:
        pass


def pending_native_groups(directory):
    result = []
    for path in directory.glob("*.spawn.json"):
        finished = path.with_name(path.name.replace(".spawn.json", ".process.json"))
        if finished.exists() and json.loads(finished.read_text()).get("waited") is True:
            continue
        try:
            record = json.loads(path.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            continue
        result.append(record["process_group"])
    return result


def wait_exit(process, seconds, cancellation):
    end = time.monotonic() + seconds
    while process.poll() is None:
        cancellation.check()
        a.need(time.monotonic() < end, "Owned process exit deadline exceeded")
        time.sleep(0.01)
    return process.wait()


def stop_owned(process, native_directory, extra_groups=()):
    """Ask the guarded supervisor to close its child before any hard fallback."""
    if process is not None and process.poll() is None:
        process.send_signal(signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            for group in pending_native_groups(native_directory):
                kill_group(group)
            for group in extra_groups:
                kill_group(group)
            kill_group(process.pid)
            process.wait(timeout=10)
    # Only unreconciled groups from this fresh owned command are eligible.
    for group in pending_native_groups(native_directory):
        kill_group(group)
    for group in extra_groups:
        if group_alive(group):
            kill_group(group)


def wait_marker(process, directory, pattern, cancellation):
    end = time.monotonic() + 20
    while True:
        cancellation.check()
        paths = sorted(directory.glob(pattern))
        for path in paths:
            try:
                record = json.loads(path.read_text())
            except (json.JSONDecodeError, FileNotFoundError):
                continue
            if isinstance(record, dict):
                return path
        a.need(process.poll() is None, "Process exited before interruption marker")
        a.need(time.monotonic() < end, "Interruption marker timeout")
        time.sleep(0.01)


def assert_groups_exited(groups):
    end = time.monotonic() + 3
    while any(group_alive(group) for group in groups):
        a.need(time.monotonic() < end, "Owned process group survived termination")
        time.sleep(0.02)


def subject_command(subject, directory, prior, flags):
    if subject == "python":
        return [
            sys.executable,
            "-B",
            str(verify.HERE / "verify.py"),
            "--out",
            str(directory),
        ], "START.json"
    return [
        sys.executable,
        "-B",
        str(verify.HERE / "compare_cpp.py"),
        "--python-run",
        str(prior),
        "--out",
        str(directory),
        *flags,
    ], "*.spawn.json"


def interrupted_subject(subject, directory, prior, flags, cancellation, *, hold=False):
    command, marker = subject_command(subject, directory, prior, flags)
    process = None
    native_groups = []
    with cancellation.owned():
        try:
            cancellation.check()
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
            wait_marker(process, directory, marker, cancellation)
            native_groups = pending_native_groups(directory)
            if hold:
                verify.write(
                    directory.parent / "READY.json",
                    {"subject_pid": process.pid, "native_groups": native_groups},
                )
                # A probe can only end by cancellation or refusal, never a complete PASS.
                end = time.monotonic() + 20
                while True:
                    cancellation.check()
                    a.need(
                        time.monotonic() < end,
                        "Outer-termination probe was not interrupted",
                    )
                    time.sleep(0.01)
            process.send_signal(signal.SIGTERM)
            wait_exit(process, 20, cancellation)
            stdout, stderr = process.communicate()
            a.need(
                process.returncode != 0 and not (directory / "RESULT.json").exists(),
                "Interrupted subject claimed completion",
            )
            assert_groups_exited(native_groups)
            if subject == "cpp":
                records = [
                    json.loads(p.read_text()) for p in directory.glob("*.process.json")
                ]
                a.need(
                    records and all(row["waited"] for row in records),
                    "Missing joined-child record",
                )
            cancellation.check()
            return {
                "pid": process.pid,
                "returncode": process.returncode,
                "native_groups": native_groups,
                "stdout": stdout.decode(errors="replace"),
                "stderr": stderr.decode(errors="replace"),
                "quiescent": True,
            }
        finally:
            stop_owned(process, directory)
    cancellation.check()


def outer_probe(subject, signum, directory, prior, cpp_run, flags, cancellation):
    process = None
    groups = []
    command = [
        sys.executable,
        "-B",
        str(Path(__file__).resolve()),
        "--python-run",
        str(prior),
        "--cpp-run",
        str(cpp_run),
        "--out",
        str(directory),
        "--termination-probe",
        subject,
        *flags,
    ]
    with cancellation.owned():
        try:
            cancellation.check()
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
            marker = wait_marker(process, directory, "READY.json", cancellation)
            ready = json.loads(marker.read_text())
            groups = [ready["subject_pid"], *ready["native_groups"]]
            a.need(
                all(group_alive(group) for group in groups),
                "Probe runtime exited before signal",
            )
            process.send_signal(signum)
            wait_exit(process, 20, cancellation)
            stdout, stderr = process.communicate()
            a.need(
                process.returncode != 0 and not (directory / "RESULT.json").exists(),
                "Outer interruption claimed a complete controls result",
            )
            a.need(
                not (directory / "subject" / "RESULT.json").exists(),
                "Outer interruption left a complete subject result",
            )
            assert_groups_exited(groups)
            if subject == "cpp":
                records = [
                    json.loads(p.read_text())
                    for p in (directory / "subject").glob("*.process.json")
                ]
                a.need(
                    records and all(row["waited"] for row in records),
                    "Outer cancellation did not join the native child",
                )
            cancellation.check()
            return {
                "subject": subject,
                "signal": signum,
                "pid": process.pid,
                "returncode": process.returncode,
                "owned_groups": groups,
                "quiescent": True,
                "stdout": stdout.decode(errors="replace"),
                "stderr": stderr.decode(errors="replace"),
            }
        finally:
            # The probe publishes only exact children of this owned command.
            stop_owned(process, directory / "subject", groups)
    cancellation.check()


def reject(fn):
    try:
        fn()
    except (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError):
        return
    raise AssertionError("Corruption was accepted")


def controls(prior, out, cpp_run):
    data = verify.read_certificate(verify.HERE / "certificate.json")
    fields = verify.validate_certificate(data)
    checks = []
    a.need(a.bv(((1,),))[0] == F(1, 2), "Half-line control")
    a.need(a.bv(((1, 0), (0, 1)))[0] == F(1, 4), "Orthant control")
    a.need(a.image_index(((2, 0), (0, 1))) == 2, "Nonprimitive lattice control")
    reject(lambda: a.bv(tuple(tuple(int(i == j) for j in range(8)) for i in range(8))))
    checks += ["half_line", "orthant", "index_two", "order_eight_refusal"]
    bad = copy.deepcopy(data)
    del bad["fields"]["7"]
    reject(lambda: verify.validate_certificate(bad))
    checks.append("missing_coefficient_field")
    bad = copy.deepcopy(data)
    bad["fields"]["5"].append(bad["fields"]["5"][0])
    reject(lambda: verify.validate_certificate(bad))
    checks.append("duplicate_support")
    bad = copy.deepcopy(data)
    row = bad["fields"]["6"][0]
    normals, _ = a.normals("transport_3x5")
    normal = normals[row["support"][0]]
    j = next(j for j, x in enumerate(normal) if x)
    row["ambient"][j] = str(F(row["ambient"][j]) + 1)
    reject(lambda: verify.validate_certificate(bad))
    checks.append("wrong_annihilator")
    bad = copy.deepcopy(data)
    bad["systems"]["capped_m4"]["qmax"] = 5
    reject(lambda: verify.validate_certificate(bad))
    checks.append("missing_normal_order")
    bad = copy.deepcopy(data)
    bad["systems"]["capped_m4"]["counts"][2][2] = 0
    reject(lambda: verify.validate_certificate(bad))
    checks.append("miscounted_dependent_complement")
    complete = json.loads((prior / "RESULT.json").read_text())
    a.need(
        complete["status"] == "PASS_COMPLETE_TRANSPORT_AND_CAPPED_CERTIFICATES",
        "Complete baseline needed",
    )
    for q in [5, 6, 7]:
        body = json.loads((prior / f"transport_3x5-q{q}.json").read_text())
        rows = body["independent"]
        normals = body["normals"]
        a.need(any(F(row["alpha"]) < 0 for row in rows), "Negative complement absent")
        a.need(
            all(
                verify.corrected(F(row["alpha"]), row["ids"], normals, fields[q])
                >= F(1, 1000000)
                for row in rows
            ),
            "Full field control",
        )
        a.need(
            any(
                verify.corrected(F(row["alpha"]), row["ids"], normals, {}) < 0
                for row in rows
            ),
            "Removing field failed to expose raw negative",
        )
        checks.append(f"complete_field_and_negative_complement_q{q}")
    cpp = json.loads((cpp_run / "RESULT.json").read_text())
    launch = json.loads((cpp_run / "capped_m4-q1.launch.json").read_text())
    binary = cpp_run / "local_values"
    a.need(
        cpp["status"] == "PASS_COMPLETE_CPP_COMPARISON"
        and verify.digest(binary) == launch["executable_sha256"],
        "Exact compared binary required",
    )
    invalid = [
        (["--unknown"], b""),
        ([], b"x"),
        ([], b"x 7"),
        ([], b"x 8 8 1\n"),
        ([], b"x 1 1 1\n-9223372036854775808\n"),
        ([], b"x 1 1 1\n9\n"),
        ([], b"x 1 1 2\n1\n"),
    ]
    for args, body in invalid:
        result = subprocess.run(
            [str(binary), *args], input=body, capture_output=True, timeout=5
        )
        a.need(
            result.returncode == 2 and b"REFUSED:" in result.stderr,
            "Malformed native input accepted",
        )
    checks.append("seven_native_parser_refusals")
    # The independently frozen sixth-order control must expose B6 omission.
    found = False
    for name in ["capped_m4", "transport_3x5"]:
        dataset = json.loads((prior / f"{name}-q6.json").read_text())
        for row in dataset["independent"]:
            if F(row["alpha"]) == F(7596671, 1210809600):
                N = dataset["normals"]
                ids = row["ids"]
                body = (
                    " ".join(
                        map(
                            str,
                            [
                                row["label"],
                                6,
                                len(N[0]),
                                1,
                                *[v for i in ids for v in N[i]],
                            ],
                        )
                    )
                    + "\n"
                )
                result = subprocess.run(
                    [str(binary), "--omit-sixth-control"],
                    input=body.encode(),
                    capture_output=True,
                    timeout=5,
                )
                a.need(
                    result.returncode == 0
                    and F(result.stdout.split()[2].decode()) != F(row["alpha"]),
                    "B6 omission not distinguished",
                )
                found = True
                break
        if found:
            break
    a.need(found, "Frozen sixth-order control missing")
    checks.append("B6_omission_changes_constant")
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-run", type=Path, required=True)
    parser.add_argument("--cpp-run", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--include-dir", action="append", default=[])
    parser.add_argument("--library-dir", action="append", default=[])
    parser.add_argument(
        "--termination-probe", choices=["python", "cpp"], help=argparse.SUPPRESS
    )
    args = parser.parse_args()
    cancellation = Cancellation()
    prior, cpp_run, out = (
        args.python_run.resolve(),
        args.cpp_run.resolve(),
        args.out.absolute(),
    )
    a.need(not out.exists() and out.parent.is_dir(), "Fresh controls output required")
    out.mkdir()
    flags = [x for p in args.include_dir for x in ["--include-dir", p]] + [
        x for p in args.library_dir for x in ["--library-dir", p]
    ]
    if args.termination_probe:
        interrupted_subject(
            args.termination_probe,
            out / "subject",
            prior,
            flags,
            cancellation,
            hold=True,
        )
        raise AssertionError("A termination probe must never return a complete result")
    checks = controls(prior, out, cpp_run)
    python_result = interrupted_subject(
        "python", out / "python-interrupted", prior, flags, cancellation
    )
    cpp_result = interrupted_subject(
        "cpp", out / "cpp-interrupted", prior, flags, cancellation
    )
    probes = []
    for subject in ["python", "cpp"]:
        for name in ["SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT"]:
            if hasattr(signal, name):
                probes.append(
                    outer_probe(
                        subject,
                        getattr(signal, name),
                        out / (subject + "-outer-" + name),
                        prior,
                        cpp_run,
                        flags,
                        cancellation,
                    )
                )
    cancellation.check()
    verify.write(
        out / "RESULT.json",
        {
            "status": "PASS_TARGETED_CORRUPTION_AND_INTERRUPTION_CONTROLS",
            "arithmetic_and_corruption_controls": checks,
            "python_interruption": python_result,
            "cpp_interruption": cpp_result,
            "outer_command_interruption_controls": probes,
        },
    )
    print(
        "PASS_TARGETED_CORRUPTION_AND_INTERRUPTION_CONTROLS",
        len(checks),
        "OUTER_SIGNALS",
        len(probes),
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, InterruptedError, KeyboardInterrupt) as error:
        print("REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
