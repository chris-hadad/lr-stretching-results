"""Bounded checks of the exact c2 margin fold over range receipts."""
from argparse import Namespace
from fractions import Fraction
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import replay

END = 10480218
SPLIT = 5000000
EPSILON = '1/200000000'
CERTIFICATE_MINIMUM = ('24825324385226107946765127095421513511423465909470146108411/'
                       '2827810858868907481115714320001048479611331101093378048000000000000')


def receipt(begin, end, minimum):
    """One range result in the field checker's own JSON layout."""
    return {'status':'PASS_EXACT_ORIGINAL_FIELD_RANGE','begin':begin,'end':end,'rows':end-begin,
            'nnz':3,'original_multiplicity':2,'violations':0,'minimum_beta':minimum,'epsilon':'0'}


def receipts(first, second):
    return [receipt(0,SPLIT,first), receipt(SPLIT,END,second)]


def write_receipts(directory, results):
    directory.mkdir()
    for result in results:
        name = f"{result['begin']:08d}-{result['end']:08d}.result.json"
        (directory/name).write_text(json.dumps(result)+'\n', encoding='utf-8')
    return directory


class C2MarginFoldTests(unittest.TestCase):
    def test_passing_fold_records_exact_minimum_and_epsilon(self):
        summary = replay.c2_field_summary(receipts('1/100000000', '3/400000000'))
        self.assertEqual(summary['exact_minimum_beta'], '3/400000000')
        self.assertEqual(summary['theorem_epsilon'], EPSILON)
        self.assertEqual((summary['rows'], summary['ranges'], summary['violations']), (END, 2, 0))
        self.assertEqual(summary['status'], 'PASS_COMPLETE_C2_ORIGINAL_FIELD_REPLAY')

    def test_minimum_equal_to_epsilon_passes(self):
        summary = replay.c2_field_summary(receipts(EPSILON, '1'))
        self.assertEqual(Fraction(summary['exact_minimum_beta']), Fraction(1, 200000000))

    def test_minimum_below_epsilon_refused(self):
        below = str(Fraction(1, 200000000)-Fraction(1, 10**30))
        with self.assertRaisesRegex(RuntimeError, 'below the theorem epsilon 1/200000000'):
            replay.c2_field_summary(receipts('1/100000000', below))
        with self.assertRaisesRegex(RuntimeError, 'below the theorem epsilon'):
            replay.c2_field_summary(receipts('0', '1'))

    def test_missing_minimum_beta_refused(self):
        results = receipts('1/100000000', '1/100000000')
        del results[1]['minimum_beta']
        with self.assertRaisesRegex(RuntimeError, 'has no exact minimum_beta string'):
            replay.c2_field_summary(results)
        results[1]['minimum_beta'] = 1e-8
        with self.assertRaisesRegex(RuntimeError, 'has no exact minimum_beta string'):
            replay.c2_field_summary(results)

    def test_malformed_minimum_beta_refused(self):
        for text, message in (('0.00000001', 'is not an exact rational'),
                              ('1e-8', 'is not an exact rational'),
                              (' 1/100000000', 'is not an exact rational'),
                              ('one', 'is not an exact rational'),
                              ('1/0', 'has a zero denominator'),
                              ('2/200000000', 'is not in lowest terms'),
                              ('-0', 'is not in lowest terms')):
            with self.subTest(text=text):
                with self.assertRaisesRegex(RuntimeError, message):
                    replay.c2_field_summary(receipts('1/100000000', text))

    def test_incomplete_or_failing_ranges_refused(self):
        with self.assertRaisesRegex(RuntimeError, 'incomplete or failing c2 original field'):
            replay.c2_field_summary(receipts('1/100000000', '1/100000000')[:1])
        results = receipts('1/100000000', '1/100000000')
        results[1]['violations'] = 1
        with self.assertRaisesRegex(RuntimeError, 'incomplete or failing c2 original field'):
            replay.c2_field_summary(results)
        results = receipts('1/100000000', '1/100000000')
        results[0]['status'] = 'FAIL_EXACT_ORIGINAL_FIELD_RANGE'
        with self.assertRaisesRegex(RuntimeError, 'is not a passing exact field range'):
            replay.c2_field_summary(results)
        with self.assertRaisesRegex(RuntimeError, 'field receipt range'):
            replay.c2_field_summary(list(reversed(receipts('1/100000000', '1/100000000'))))


class C2FieldPhaseTests(unittest.TestCase):
    def run_phase(self, scratch, worst):
        asset_root = scratch/'assets'
        original = asset_root/replay.A17
        original.mkdir(parents=True)
        ends = list(range(100000, END, 100000))+[END]
        for begin, end in zip([0]+ends, ends):
            (original/f'full-operator-{begin:08d}-{end:08d}-001.rows').touch()
        out = scratch/'run'; out.mkdir()

        def fake_run(argv, record, expected, timeout):
            begin, end = argv[5], argv[6]
            return receipt(begin, end, worst if begin == 8100000 else '1/100000000')

        with patch.object(replay, 'verify_assets'), \
                patch.object(replay, 'binary', return_value=scratch/'bin/field-original'), \
                patch.object(replay, 'run_one', side_effect=fake_run):
            replay.c2_field(Namespace(asset_root=asset_root), out)
        return out/'c2-field/COMPLETE.json'

    def test_phase_records_exact_margin(self):
        with tempfile.TemporaryDirectory() as scratch:
            complete = json.loads(self.run_phase(Path(scratch), CERTIFICATE_MINIMUM).read_text(encoding='utf-8'))
            self.assertEqual(complete['exact_minimum_beta'], CERTIFICATE_MINIMUM)
            self.assertEqual(complete['theorem_epsilon'], EPSILON)
            self.assertEqual((complete['rows'], complete['ranges']), (END, 105))

    def test_phase_below_epsilon_writes_no_complete_record(self):
        with tempfile.TemporaryDirectory() as scratch:
            with self.assertRaisesRegex(RuntimeError, 'below the theorem epsilon'):
                self.run_phase(Path(scratch), '1/200000001')
            self.assertFalse((Path(scratch)/'run/c2-field/COMPLETE.json').exists())


class C2RecheckTests(unittest.TestCase):
    def test_recheck_folds_written_receipts(self):
        with tempfile.TemporaryDirectory() as scratch:
            directory = write_receipts(Path(scratch)/'c2-field', receipts('1/100000000', '3/400000000'))
            (directory/'00000000-05000000.process.json').write_text('{}', encoding='utf-8')
            summary = replay.recheck_c2_receipts(directory)
            self.assertEqual(summary['exact_minimum_beta'], '3/400000000')
            self.assertEqual(summary['ranges'], 2)

    def test_recheck_refuses_empty_misnamed_or_mislabelled_receipts(self):
        with tempfile.TemporaryDirectory() as scratch:
            empty = Path(scratch)/'empty'; empty.mkdir()
            with self.assertRaisesRegex(RuntimeError, 'no c2 range receipts'):
                replay.recheck_c2_receipts(empty)
            directory = write_receipts(Path(scratch)/'c2-field', receipts('1/100000000', '1/100000000'))
            (directory/'00000000-05000000.result.json').rename(directory/'00000000-04000000.result.json')
            with self.assertRaisesRegex(RuntimeError, 'does not match its file name'):
                replay.recheck_c2_receipts(directory)

    def test_command_line_recheck(self):
        with tempfile.TemporaryDirectory() as scratch:
            good = write_receipts(Path(scratch)/'good', receipts('1/100000000', '3/400000000'))
            bad = write_receipts(Path(scratch)/'bad', receipts('1/100000000', '1/400000000'))
            command = [sys.executable, '-B', str(HERE/'replay.py'), '--recheck-c2-receipts']
            passed = subprocess.run(command+[str(good)], capture_output=True, text=True, timeout=10)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertEqual(json.loads(passed.stdout)['exact_minimum_beta'], '3/400000000')
            refused = subprocess.run(command+[str(bad)], capture_output=True, text=True, timeout=10)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn('below the theorem epsilon 1/200000000', refused.stderr)
            mixed = subprocess.run(command+[str(good), '--phase', 'c2-field'],
                                   capture_output=True, text=True, timeout=10)
            self.assertEqual(mixed.returncode, 2)
            self.assertIn('takes no replay arguments', mixed.stderr)


class C2CertificateTests(unittest.TestCase):
    def test_shipped_certificate_margin(self):
        summary = replay.check_c2_certificate()
        self.assertEqual(summary['exact_minimum_beta'], CERTIFICATE_MINIMUM)
        self.assertEqual((summary['rows'], summary['ranges'], summary['original_multiplicity']),
                         (END, 105, 62868270))
        ratio = Fraction(CERTIFICATE_MINIMUM)/Fraction(1, 200000000)
        self.assertTrue(Fraction(17, 10) < ratio < Fraction(18, 10))

    def test_changed_certificate_or_range_copy_refused(self):
        with tempfile.TemporaryDirectory() as scratch:
            copy = Path(scratch)/'c2-certificate'
            shutil.copytree(replay.C2_CERTIFICATE, copy)
            first = sorted((copy/'ranges').iterdir())[0]
            first.write_text(first.read_text(encoding='utf-8').replace('"violations":0', '"violations":1'),
                             encoding='utf-8')
            with self.assertRaisesRegex(RuntimeError, 'c2 certificate range result missing or changed'):
                replay.check_c2_certificate(copy)
            shutil.copyfile(replay.C2_CERTIFICATE/'ranges'/first.name, first)
            certificate = copy/'GLOBAL-C2-CERTIFICATE.json'
            certificate.write_bytes(certificate.read_bytes().replace(b'"ranges": 105', b'"ranges": 104'))
            with self.assertRaisesRegex(RuntimeError, 'changed c2 certificate'):
                replay.check_c2_certificate(copy)


if __name__ == '__main__':
    unittest.main()
