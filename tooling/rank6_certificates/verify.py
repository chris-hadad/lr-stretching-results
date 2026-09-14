#!/usr/bin/env python3
"""Reproduce the finite rank-six c4/c5 certificates in a fresh output directory."""
from __future__ import annotations

import argparse
from array import array
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import struct
import subprocess
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
DIMENSIONS = {
    'q5': (39974, 121241, 102990, 1307258, 10**10, 1893, 580),
    'q6': (293795, 675721, 606205, 8139966, 10**12, 127124, 9850),
}
FULL_MODES = [('q5', 850668), ('q6', 5245786), ('types6', 675721),
              ('matrix5', 121241), ('matrix6', 675721)]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')


def extract_data(out):
    metadata = read_json(HERE / 'DATA.json')
    need(metadata['schema'] == 'rank6-c4-c5-data-v1', 'Unsupported dataset schema')
    source = HERE / 'data.zip'
    need(source.stat().st_size == metadata['archive']['bytes'] and
         digest(source) == metadata['archive']['sha256'], 'Dataset archive changed')
    files = metadata['files']
    need(len(files) == 24, 'Incomplete finite dataset manifest')
    need(sum(x['bytes'] for x in files.values()) <= 300 * 1024**2, 'Expanded dataset bound')
    destination = out / 'data'
    destination.mkdir()
    with zipfile.ZipFile(source) as archive:
        infos = archive.infolist()
        need(len(infos) == len(files) and set(archive.namelist()) == set(files), 'Dataset namespace differs')
        for info in infos:
            name = info.filename
            need(name == info.orig_filename and name and '/' not in name and '\\' not in name and
                 ':' not in name and name not in {'.', '..'} and not any(ord(c) < 32 for c in name),
                 'Unsafe dataset name')
            mode = (info.external_attr >> 16) & 0o170000
            need(not info.is_dir() and mode in {0, 0o100000} and not info.flag_bits & 1,
                 'Nonregular or encrypted dataset member')
            row = files[name]
            need(info.file_size == row['bytes'] and 0 <= info.file_size <= 64 * 1024**2,
                 'Dataset member size differs')
            h = hashlib.sha256()
            size = 0
            target = destination / name
            with archive.open(info) as f, target.open('xb') as g:
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    size += len(block)
                    need(size <= row['bytes'], 'Expanded member exceeds bound')
                    h.update(block)
                    g.write(block)
            target.chmod(0o600)
            need(size == row['bytes'] and h.hexdigest() == row['sha256'] and
                 digest(target) == row['sha256'], 'Dataset member hash/readback differs: ' + name)
    return destination, metadata


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
                raise InterruptedError(f'Terminated by signal {self.cancelled_signal}')
            remaining = stop - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(process.args, timeout)
            try:
                return process.wait(timeout=min(0.05, remaining))
            except subprocess.TimeoutExpired:
                continue

    def run(self, name, command, *, input_path=None, expected=0, deadline=120):
        if self.cancelled_signal is not None:
            raise InterruptedError(f'Terminated by signal {self.cancelled_signal}')
        remaining = self.limit - self.used
        need(remaining > 0, 'Cumulative child-time allocation exhausted')
        timeout = min(deadline, remaining)
        stdout, stderr = self.out / (name + '.stdout'), self.out / (name + '.stderr')
        start = time.monotonic()
        write_json(self.out / (name + '.launch.json'), {
            'argv': command, 'deadline_seconds': timeout,
            'input': str(input_path) if input_path else None,
            'input_sha256': digest(input_path) if input_path else None,
            'executable_sha256': digest(command[0]) if Path(command[0]).is_file() else None,
        })
        source = Path(input_path).open('rb') if input_path else open(os.devnull, 'rb')
        process = None
        failure = None
        code = None
        waited = False
        try:
            with source, stdout.open('xb') as fo, stderr.open('xb') as fe:
                try:
                    # The signal handler records cancellation during Popen; it
                    # cannot raise before the returned child is under this guard.
                    self.spawning = True
                    process = subprocess.Popen(command, stdin=source, stdout=fo, stderr=fe, start_new_session=True)
                    self.active_child = process
                    self.spawning = False
                    write_json(self.out / (name + '.spawn.json'), {'pid': process.pid, 'process_group': process.pid})
                    if self.cancelled_signal is not None:
                        raise InterruptedError(f'Terminated by signal {self.cancelled_signal}')
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
        record = {'argv': command, 'pid': process.pid if process else None, 'returncode': code, 'waited': waited,
                  'elapsed_seconds': elapsed, 'deadline_seconds': timeout,
                  'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr),
                  'interruption_signal': self.cancelled_signal,
                  'failure': str(failure) if failure is not None else None}
        self.jobs.append(record)
        write_json(self.out / (name + '.process.json'), record)
        if failure is not None:
            raise failure
        need(code == expected, f'{name} returned {code}; see preserved {stderr.name}')
        return stdout


def install_termination_handlers(runner):
    def terminate(signum, frame):
        runner.cancelled_signal = signum
        # Asynchronous exceptions cannot escape a cleanup handler while a
        # child is owned. wait_child observes this flag with bounded polling.
        if not runner.spawning and runner.active_child is None:
            raise InterruptedError(f'Terminated by signal {signum}')
    for name in ['SIGINT', 'SIGTERM', 'SIGHUP', 'SIGQUIT']:
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), terminate)


def integers(path, signed=False):
    data = array('i' if signed else 'I')
    with Path(path).open('rb') as f:
        body = f.read()
    need(len(body) % 4 == 0 and data.itemsize == 4, 'Invalid 32-bit array')
    data.frombytes(body)
    if sys.byteorder != 'little':
        data.byteswap()
    return data


def alphas(data, q):
    values = (data / (q + '-alpha.txt')).read_text().splitlines()
    need(len(values) == DIMENSIONS[q][0], 'Incomplete local-value roster')
    parsed = [Fraction(v) for v in values]
    need(sum(v < 0 for v in parsed) == DIMENSIONS[q][6] and all(v != 0 for v in parsed),
         'Local sign population differs')
    return parsed


def primal(data, q, *, mutation=None):
    types, rows, columns, entries, denominator, nonzero, _ = DIMENSIONS[q]
    a = alphas(data, q)
    indptr = integers(data / (q + '-indptr.bin'))
    col = integers(data / (q + '-indices.bin'))
    values = integers(data / (q + '-data.bin'), signed=True)
    typemap = integers(data / ('q5-type_ids.bin' if q == 'q5' else 'q6-ORBIT-TYPE.bin'))
    certificate = read_json(data / (q + '-certificate.json'))
    need(certificate['rows'] == rows and certificate['columns'] == columns and
         certificate['denominator'] == denominator, 'Certificate dimensions or denominator differ')
    raw = certificate['nonzero']
    need(len(raw) == nonzero, 'Sparse field count differs')
    field = [0] * columns
    previous = -1
    for index, value in raw:
        need(type(index) is int and previous < index < columns and type(value) is int and value != 0,
             'Invalid or duplicate sparse coordinate')
        field[index] = value
        previous = index
    if mutation == 'zero-field':
        field = [0] * columns
    if mutation == 'missing-last-row':
        indptr.pop()
    if mutation == 'wrong-type':
        typemap[0] = types
    scale = 5 if mutation == 'wrong-scale' else 6
    need(len(indptr) == rows + 1 and indptr[0] == 0 and indptr[-1] == entries and
         len(col) == len(values) == entries and len(typemap) == rows, 'Incomplete CSR or type map')
    minimum = None
    minimum_row = None
    for i in range(rows):
        need(indptr[i] <= indptr[i+1] and typemap[i] < types, 'CSR order or type range')
        correction = 0
        previous = -1
        for j in range(indptr[i], indptr[i+1]):
            need(previous < col[j] < columns and values[j] != 0, 'Noncanonical sparse matrix row')
            correction += values[j] * field[col[j]]
            previous = col[j]
        alpha = a[typemap[i]]
        numerator = scale * denominator * alpha.numerator + alpha.denominator * correction
        bottom = scale * denominator * alpha.denominator
        need(bottom > 0 and 2000000 * numerator >= bottom, f'Insufficient corrected margin at {q} row {i}')
        if minimum is None or numerator * minimum.denominator < minimum.numerator * bottom:
            minimum, minimum_row = Fraction(numerator, bottom), i
    return {'rows': rows, 'columns': columns, 'nonzero_entries': entries,
            'minimum': str(minimum), 'minimum_row': minimum_row, 'margin': '1/2000000'}


def local_input(data, q, selected):
    atlas = [[int(v) for v in line.split()] for line in (data / 'atlas.txt').read_text().splitlines()[1:43]]
    need(len(atlas) == 42 and all(len(v) == 10 for v in atlas), 'Atlas dimensions')
    records = (data / ('q5-types.bin' if q == 'q5' else 'q6-TYPES.bin')).read_bytes()
    orbits = (data / 'q6-orbits.bin').read_bytes() if q == 'q6' else None
    for ident in selected:
        need(0 <= ident < DIMENSIONS[q][0], 'Local type ID outside roster')
        if q == 'q5':
            index = struct.unpack_from('<H', records, 67*ident)[0]
            ids = records[67*ident+2:67*ident+7]
        else:
            index = records[71*ident]
            first = struct.unpack_from('<I', records, 71*ident+61)[0]
            ids = orbits[12*first:12*first+6]
        n = int(q[-1])
        need(len(ids) == n and len(set(ids)) == n and max(ids) < 42, 'Bad normal representative')
        yield ' '.join(map(str, [f'{q}-{ident}', n, 10, index,
                                *(x for j in ids for x in atlas[j])])) + '\n'


def local_values(data, out, runner, binary, full, batch_size):
    results = {}
    for q in DIMENSIONS:
        values = alphas(data, q)
        selected = list(range(len(values))) if full else sorted({0, 1, len(values)-1, *range(0, len(values), max(1, len(values)//20)),
                                                                *([273359, 277053] if q == 'q6' else [])})
        count = 0
        for batch, start in enumerate(range(0, len(selected), batch_size)):
            ids = selected[start:start+batch_size]
            inp = out / f'{q}-local-{batch:03d}.input'
            inp.write_text(''.join(local_input(data, q, ids)))
            primary = runner.run(f'{q}-local-{batch:03d}', [str(binary)], input_path=inp)
            lines = primary.read_text().splitlines()
            need(len(lines) == len(ids), 'Missing or extra local output')
            for ident, line in zip(ids, lines):
                fields = line.split()
                need(len(fields) == 7 and fields[0] == f'{q}-{ident}', 'Changed local output identity')
                need(Fraction(fields[2]) == values[ident], f'Local-value disagreement at {q} type {ident}')
            count += len(ids)
            if full and batch % 20 == 0:
                print(f'{q}: {count}/{len(selected)} local constants independently reconstructed', flush=True)
        results[q] = {'checked': count, 'total_types': len(values), 'complete': full}
    return results


def controls(data, out, runner, topology, local):
    rejected = []
    topology_rejections = []
    for mode, mutation, reason in [
        ('q5','normal','FRESH_NORMAL_ATLAS_DISAGREEMENT'),
        ('q5','index','Q5_FRESH_NORMAL_INDEX_DISAGREEMENT'),
        ('q6','index','Q6_COMPLETE_FRESH_QUOTIENT_INDEX_DISAGREEMENT'),
        ('q5','orbit','ORBIT_ORIGINAL_ORDINAL_IDENTITY'),
        ('types6','orbit','ORBIT_ORIGINAL_ORDINAL_IDENTITY'),
        ('q5','type-permutation','INVALID_Q5_GENERATOR_PERMUTATION'),
        ('types6','type-permutation','INVALID_Q6_GENERATOR_PERMUTATION'),
        ('matrix5','kernel','KERNEL_NOT_ANNIHILATED_BY_SUPPORT'),
        ('matrix6','kernel','KERNEL_NOT_ANNIHILATED_BY_SUPPORT'),
        ('matrix5','primitive-divisor','PRIMITIVE_QUOTIENT_DIVISOR_IDENTITY'),
        ('matrix6','primitive-divisor','PRIMITIVE_QUOTIENT_DIVISOR_IDENTITY'),
        ('matrix5','matrix-entry','COMPLETE_MATRIX_ROW_OR_OMITTED_ZERO_MISMATCH'),
        ('matrix6','matrix-entry','COMPLETE_MATRIX_ROW_OR_OMITTED_ZERO_MISMATCH'),
        ('matrix5','omitted-matrix-entry','COMPLETE_MATRIX_ROW_OR_OMITTED_ZERO_MISMATCH'),
        ('matrix6','omitted-matrix-entry','COMPLETE_MATRIX_ROW_OR_OMITTED_ZERO_MISMATCH')]:
        result = runner.run('refusal-'+mode+'-'+mutation,
                            [str(topology), str(data), mode, '100', mutation], expected=2)
        text = result.read_text()
        need('MUTATION_WAS_NOT_REJECTED' not in text, 'Topology mutation escaped its intended invariant')
        record = read_json(result)
        need(record['status'] == 'REFUSED_OR_INCOMPLETE' and record['reason'] == reason,
             'Topology mutation did not reach its distinguishing invariant')
        topology_rejections.append({'mode': mode, 'mutation': mutation, 'result': record})
    for q in DIMENSIONS:
        for mutation in ['zero-field', 'missing-last-row', 'wrong-type', 'wrong-scale']:
            try:
                primal(data, q, mutation=mutation)
            except ValueError as error:
                expected_reason = {'zero-field': 'Insufficient corrected margin',
                                   'wrong-scale': 'Insufficient corrected margin',
                                   'missing-last-row': 'Incomplete CSR or type map',
                                   'wrong-type': 'CSR order or type range'}[mutation]
                need(str(error).startswith(expected_reason), 'Primal mutation did not reach its arithmetic invariant')
                rejected.append(q + ':' + mutation)
            else:
                raise ValueError('Mutation accepted: ' + q + ':' + mutation)
    # The sixth Bernoulli term is invisible to easy orthant controls.
    inp = out / 'sixth-term.input'
    inp.write_text(''.join(local_input(data, 'q6', [0, 1, 273359, 277053])))
    changed = runner.run('sixth-term-mutant', [str(local), '--omit-sixth-control'], input_path=inp)
    reference = alphas(data, 'q6')
    differences = []
    for line in changed.read_text().splitlines():
        fields = line.split()
        ident = int(fields[0].split('-')[1])
        if Fraction(fields[2]) != reference[ident]:
            differences.append(ident)
    need(differences, 'The missing-sixth-term control did not distinguish the algorithms')
    return {'refused_topology_mutations': topology_rejections,
            'refused_primal_mutations': rejected, 'missing_sixth_term_detected_at': differences,
            'scope': 'Corrupted local/certificate controls are not negative LR candidates.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--full', action='store_true', help='Reproduce every finite predicate and local constant')
    mode.add_argument('--quick', action='store_true', help='Integrity, all rational inequalities, and bounded diagnostic prefixes only')
    parser.add_argument('--out', type=Path, required=True, help='New output directory; existing paths are refused')
    parser.add_argument('--cxx', default='c++')
    parser.add_argument('--include-dir', action='append', default=[])
    parser.add_argument('--library-dir', action='append', default=[])
    parser.add_argument('--child-seconds', type=int, default=1300, help='Finite cumulative child wall-time ceiling')
    parser.add_argument('--batch-size', type=int, default=2000, help='Local constants per bounded child, 1 through 2000')
    args = parser.parse_args()
    need(args.child_seconds > 0, 'Positive child-time allocation required')
    need(1 <= args.batch_size <= 2000, 'Batch size must be between 1 and 2000')
    out = args.out.absolute()
    need(not out.exists() and not out.is_symlink() and out.parent.is_dir(), 'A fresh output path with an existing parent is required')
    need(out != HERE and HERE not in out.parents, 'Keep generated work outside the distributed source directory')
    out.mkdir(mode=0o700)
    started = time.monotonic()
    runner = Runner(out, args.child_seconds)
    install_termination_handlers(runner)
    try:
        write_json(out / 'START.json', {'mode': 'full' if args.full else 'quick', 'platform': platform.platform(),
                                      'python': sys.version, 'child_seconds': args.child_seconds,
                                      'source_hashes': {n: digest(HERE/n) for n in ['verify.py', 'local_values.cpp', 'topology.cpp', 'DATA.json', 'data.zip']}})
        data, metadata = extract_data(out)
        common = [args.cxx, '-O2', '-std=c++17']
        topology, local = out/'topology', out/'local_values'
        runner.run('compile-topology', common + [str(HERE/'topology.cpp'), '-o', str(topology)], deadline=120)
        flags = [x for d in args.include_dir for x in ['-I', d]] + [x for d in args.library_dir for x in ['-L', d]]
        for directory in args.library_dir:
            flags += ['-Xlinker', '-rpath', '-Xlinker', str(Path(directory).absolute())]
        runner.run('compile-local', common + flags + [str(HERE/'local_values.cpp'), '-lgmpxx', '-lgmp', '-o', str(local)], deadline=120)
        geometry = {}
        for name, total in FULL_MODES:
            count = total if args.full else min(2000, total)
            result = runner.run('topology-'+name, [str(topology), str(data), name, str(count), 'none'])
            record = read_json(result)
            expected = 'PASS_COMPLETE_FINITE_PREDICATES' if args.full else 'PASS_COMPLETE_PILOT_PREFIX'
            need(record['status'] == expected, 'Wrong topology completeness status')
            geometry[name] = record
        rational = {q: primal(data, q) for q in DIMENSIONS}
        numerical = local_values(data, out, runner, local, args.full, args.batch_size)
        failures = controls(data, out, runner, topology, local)
        report = {'status': 'PASS_COMPLETE_C4_C5_FINITE_CERTIFICATES' if args.full else 'PASS_QUICK_DIAGNOSTICS_NOT_THEOREM',
                  'complete': args.full, 'mathematical_scope': 'Rank-six c4/c5 finite certificate predicates; analytic whole-hive bridge is stated separately in PROOF.md. Whole rank-six positivity is not claimed.',
                  'topology': geometry, 'rational': rational, 'local_values': numerical, 'failure_controls': failures,
                  'child_wall_seconds': runner.used, 'elapsed_seconds': time.monotonic()-started,
                  'children': len(runner.jobs), 'every_child_waited': True, 'data_archive_sha256': metadata['archive']['sha256']}
        write_json(out/'RESULT.json', report)
        print(json.dumps({k:v for k,v in report.items() if k not in {'topology','failure_controls'}}), flush=True)
    except BaseException as error:
        write_json(out/'FAILURE.json', {'status':'INCOMPLETE_OR_REFUSED', 'error':str(error),
                                       'child_wall_seconds':runner.used,'completed_child_records':len(runner.jobs),
                                       'outputs_retained':True})
        raise


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, IndexError, RuntimeError) as error:
        print('REFUSED: ' + str(error), file=sys.stderr)
        sys.exit(2)
