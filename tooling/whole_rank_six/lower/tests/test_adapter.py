"""Proposed bounded adapter failure checks. Root runs these after integration."""
from argparse import Namespace
import json
import os
from pathlib import Path
import signal
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import replay
from runtime import group_exists


def h8_range_fixture(work):
    """Small files with the genuine public checker's per-type JSON layout."""
    asset_root = work/'assets'
    data = asset_root/replay.C3
    (data/'U02/DATA').mkdir(parents=True)
    (data/'NUMERATORS').mkdir()
    (data/'U02/DATA/q1.types').write_bytes(bytes([1])+bytes(72))
    with (data/'U02/DATA/q1.types').open('ab') as stream:
        stream.write((bytes([1])+bytes(72))*3)
    (data/'NUMERATORS/q1.nidx').write_bytes(struct.pack('<5Q',0,1,2,3,4))
    phase = work/'h8'; phase.mkdir()
    checker = work/'bin/h8-check'; checker.parent.mkdir()
    checker.write_bytes(b'checker')
    checker.with_suffix('.binding.json').write_text('{}')
    sources = phase/'SOURCES.txt'; sources.write_text('public-layout-source\n')
    lower = phase/'LOWER-0.txt'; lower.write_text(replay.h8_lower_contents(0))
    rows = phase/'k1-0000000-0000004.rows.jsonl'
    entries = [{'k':1,'id':id,'index':1,'numerator_points':1,'new_slots':1,
                'determining_sites':1,'unused_sites':2,'proper_children':0,
                'prepare_seconds':0.000001,'check_seconds':0.00001}
               for id in range(4)]
    rows.write_text(''.join(json.dumps(entry)+'\n' for entry in entries))
    result = {'status':'PASS_EXACT_H8_RANGE','k':1,'begin':0,'end':4,'types':4,
              'new_coefficient_slots':4,'determining_sites':4,'unused_sites':8,
              'numerator_points':4,'loading_seconds':0.1,'checking_seconds':0.1,
              'whole_LR_calls':0}
    receipt = phase/'k1-0000000-0000004.process.json'
    process = {'argv':replay.h8_argv(checker,asset_root,sources,lower,rows,1,0,4),
               'status':'PASS_EXACT_H8_RANGE','result':result,
               'child_waited':True,'owned_process_group_exited':True,
               'h8_binding':{'schema':'rank-six-h8-output-v1',
                             'rows_sha256':replay.digest(rows),
                             'identity':replay.h8_identity(checker,sources,lower)}}
    receipt.write_text(json.dumps(process))
    return {'phase':phase,'asset_root':asset_root,'checker':checker,'sources':sources,
            'lower':lower,'rows':rows,'receipt':receipt,'entries':entries,'process':process}


def inspect_h8_fixture(fixture):
    return replay.h8_existing_range(fixture['phase'],1,0,4,fixture['checker'],
                                    fixture['sources'],fixture['lower'],fixture['asset_root'])


class AdapterFailureTests(unittest.TestCase):
    def test_bad_compiler_refused_before_assets_or_output(self):
        with tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch)/'unused-run'
            command = [sys.executable, '-B', str(HERE/'replay.py'),
                       '--asset-root', str(Path(scratch)/'no-assets'),
                       '--output', str(output), '--phase', 'c3-core',
                       '--cxx', 'definitely-no-such-cxx-for-adapter-test']
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('compiler not found or not executable', result.stderr)
            self.assertFalse(output.exists())

    def test_optimized_parent_refused_before_help_or_data(self):
        result = subprocess.run([sys.executable, '-O', '-B', str(HERE/'replay.py'), '--help'],
                                capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Python assertions must be enabled', result.stderr)

    def test_checker_optimized_direct_refusal(self):
        result = subprocess.run([sys.executable, '-O', '-B', str(HERE/'src/check_field.py')],
                                capture_output=True, text=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('REFUSED: Python assertions must be enabled', result.stderr)

    def test_missing_and_malformed_analytic_ranges_refused(self):
        ranges = json.loads((HERE/'RANGES.json').read_text())['c3_analytic']
        self.assertEqual(len(replay.validated_analytic_ranges(ranges)), 65)
        with self.assertRaisesRegex(RuntimeError, 'complete c3 analytic range roster'):
            replay.validated_analytic_ranges(ranges[:-1])
        wrong = [dict(item) for item in ranges]
        wrong[1]['begin'] = 1
        with self.assertRaisesRegex(RuntimeError, 'analytic range gap'):
            replay.validated_analytic_ranges(wrong)

    def test_missing_and_malformed_operator_shards_refused(self):
        manifest = json.loads((HERE/'ASSETS.json').read_text())
        shards = sorted(Path(name) for name in manifest['files']
                        if Path(name).name.startswith('full-operator-') and
                        Path(name).name.endswith('.rows'))
        self.assertEqual(len(replay.validated_operator_shards(shards)), 105)
        with self.assertRaisesRegex(RuntimeError, 'complete c2 operator shard roster'):
            replay.validated_operator_shards(shards[:-1])
        wrong = list(shards)
        wrong[1] = wrong[1].with_name('full-operator-malformed.rows')
        with self.assertRaisesRegex(RuntimeError, 'operator shard name'):
            replay.validated_operator_shards(wrong)

    def test_macos_memory_does_not_double_count_purgeable(self):
        vm_stat = ('Mach Virtual Memory Statistics: (page size of 4096 bytes)\n'
                   'Pages free: 100.\nPages inactive: 200.\n'
                   'Pages speculative: 300.\nPages purgeable: 9999.\n')
        with patch.object(replay.sys, 'platform', 'darwin'):
            with patch.object(replay.subprocess, 'run', return_value=Namespace(stdout=vm_stat)) as run:
                self.assertEqual(replay.available_memory(), 600 * 4096)
                self.assertEqual(run.call_args.kwargs['timeout'], 5)

    def test_h8_bound_range_and_completed_level(self):
        with tempfile.TemporaryDirectory() as scratch:
            fixture = h8_range_fixture(Path(scratch))
            record = inspect_h8_fixture(fixture)
            complete = {'status':'PASS_COMPLETE_H8_LEVEL','k':1,'types':4,
                        'slots':4,'ranges':[record]}
            (fixture['phase']/'k1-COMPLETE.json').write_text(json.dumps(complete))
            self.assertEqual(replay.validate_completed_level(
                fixture['phase'],1,fixture['checker'],fixture['sources'],
                fixture['asset_root']),complete)
            token = replay.lower_token(fixture['phase'],1,fixture['checker'],
                                       fixture['sources'],fixture['asset_root'])
            self.assertEqual(token.read_text(),replay.h8_lower_contents(1))
            token.unlink()
            fixture['rows'].write_text('not even json\n'*4)
            fixture['process']['h8_binding']['rows_sha256'] = replay.digest(fixture['rows'])
            fixture['receipt'].write_text(json.dumps(fixture['process']))
            with self.assertRaises((RuntimeError,ValueError)):
                replay.validate_completed_level(fixture['phase'],1,fixture['checker'],
                                                fixture['sources'],fixture['asset_root'])
            with self.assertRaises((RuntimeError,ValueError)):
                replay.lower_token(fixture['phase'],1,fixture['checker'],
                                   fixture['sources'],fixture['asset_root'])

    def test_h8_legacy_and_changed_identities_refused(self):
        with tempfile.TemporaryDirectory() as scratch:
            fixture = h8_range_fixture(Path(scratch))
            del fixture['process']['h8_binding']
            fixture['receipt'].write_text(json.dumps(fixture['process']))
            with self.assertRaisesRegex(RuntimeError,'production binding'):
                inspect_h8_fixture(fixture)
        with tempfile.TemporaryDirectory() as scratch:
            fixture = h8_range_fixture(Path(scratch))
            fixture['checker'].write_bytes(b'changed checker')
            with self.assertRaisesRegex(RuntimeError,'production binding'):
                inspect_h8_fixture(fixture)
        with tempfile.TemporaryDirectory() as scratch:
            fixture = h8_range_fixture(Path(scratch))
            fixture['sources'].write_text('changed source list\n')
            with self.assertRaisesRegex(RuntimeError,'production binding'):
                inspect_h8_fixture(fixture)
        with tempfile.TemporaryDirectory() as scratch:
            fixture = h8_range_fixture(Path(scratch))
            fixture['process']['h8_binding']['identity']['controller_sha256'] = '0'*64
            fixture['receipt'].write_text(json.dumps(fixture['process']))
            with self.assertRaisesRegex(RuntimeError,'production binding'):
                inspect_h8_fixture(fixture)

    def test_h8_rebound_corrupt_rows_refused(self):
        def corrupt(name, entries):
            if name=='garbage':return 'not even json\n'*4
            if name=='duplicate_id':entries[1]['id']=0
            if name=='omitted_id':entries[1]['id']=2
            if name=='out_of_range_id':entries[3]['id']=4
            if name=='wrong_index':entries[2]['index']=2
            if name=='wrong_numerator_count':entries[2]['numerator_points']=2
            if name=='wrong_slots':entries[2]['new_slots']=2
            if name=='rational_string':entries[2]['index']='1/1'
            if name=='missing_field':del entries[2]['proper_children']
            if name=='negative_elapsed':entries[2]['check_seconds']=-1
            if name=='nonfinite_elapsed':entries[2]['check_seconds']=float('nan')
            if name=='duplicate_field':
                lines=[json.dumps(entry) for entry in entries]
                lines[2]=lines[2].replace('"id": 2', '"id": 2, "id": 2')
                return '\n'.join(lines)+'\n'
            return ''.join(json.dumps(entry)+'\n' for entry in entries)
        for name in ('garbage','duplicate_id','omitted_id','out_of_range_id',
                     'wrong_index','wrong_numerator_count','wrong_slots',
                     'rational_string','missing_field','negative_elapsed',
                     'nonfinite_elapsed','duplicate_field'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as scratch:
                fixture = h8_range_fixture(Path(scratch))
                fixture['rows'].write_text(corrupt(name,fixture['entries']))
                # A matching edited receipt hash still cannot make altered row semantics valid.
                fixture['process']['h8_binding']['rows_sha256'] = replay.digest(fixture['rows'])
                fixture['receipt'].write_text(json.dumps(fixture['process']))
                with self.assertRaises((RuntimeError,ValueError)):
                    inspect_h8_fixture(fixture)

    def test_sigterm_stops_exact_child_group(self):
        with tempfile.TemporaryDirectory() as scratch:
            work = Path(scratch)
            subject = subprocess.Popen([sys.executable, '-B', str(HERE/'tests/term_subject.py'), str(work)],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                       start_new_session=True,
                                       env={**os.environ, 'PYTHONOPTIMIZE': ''})
            pgid = None
            try:
                pid_file = work/'child-pgid'
                deadline = time.monotonic() + 10
                while not pid_file.exists() and subject.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(pid_file.is_file(), 'subject never launched its child')
                pgid = int(pid_file.read_text())
                mask = {int(x) for x in (work/'child-mask').read_text().split(',') if x}
                self.assertTrue(mask.isdisjoint({signal.SIGINT, signal.SIGTERM, signal.SIGHUP}),
                                'compiler/checker child inherited blocked cancellation signals')
                os.kill(subject.pid, signal.SIGTERM)
                _stdout, stderr = subject.communicate(timeout=20)
                self.assertEqual(subject.returncode, 23, stderr)
                self.assertFalse(group_exists(pgid), 'owned child group survived TERM')
                self.assertFalse((work/'child.process.json').exists(), 'cancelled child gained a receipt')
            finally:
                if subject.poll() is None:
                    os.kill(subject.pid, signal.SIGTERM)
                    try:
                        subject.communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(subject.pid, signal.SIGKILL)
                        subject.communicate(timeout=5)
                if pgid is not None and group_exists(pgid):
                    os.killpg(pgid, signal.SIGTERM)
                    deadline = time.monotonic() + 2
                    while group_exists(pgid) and time.monotonic() < deadline:
                        time.sleep(0.02)
                    if group_exists(pgid):
                        os.killpg(pgid, signal.SIGKILL)
                    deadline = time.monotonic() + 2
                    while group_exists(pgid) and time.monotonic() < deadline:
                        time.sleep(0.02)
                    self.assertFalse(group_exists(pgid), 'synthetic child group survived cleanup')


if __name__ == '__main__':
    unittest.main()
