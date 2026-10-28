"""Bounded checks of the exact c7-c9 margin gate in the small-component driver."""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import signal
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('rank_six_small_driver', HERE/'verify.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

EPSILON = {'c7':'1/144', 'c8':'1/9', 'c9':'1/2'}


def top_record(c9='1/2', c8='1/9', c7='1/144'):
    """The small top verifier's report layout: results keyed by normal-subset size."""
    return {'status':'PASS_COMPLETE',
            'results':{'1':{'minimum':c9}, '2':{'minimum':c8}, '3':{'minimum':c7}}}


class TopMarginTests(unittest.TestCase):
    def test_minima_equal_to_epsilon_pass_and_are_recorded(self):
        margins = driver.top_margins(top_record())
        self.assertEqual(margins, {k:{'exact_minimum':v, 'theorem_epsilon':v} for k, v in EPSILON.items()})

    def test_minima_above_epsilon_pass(self):
        margins = driver.top_margins(top_record(c9='1', c8='2/9', c7='1/100'))
        self.assertEqual(margins['c7'], {'exact_minimum':'1/100', 'theorem_epsilon':'1/144'})

    def test_minimum_below_epsilon_refused(self):
        for name, record in (('c7', top_record(c7='1/145')), ('c8', top_record(c8='1/10')),
                             ('c9', top_record(c9=str(Fraction(1, 2)-Fraction(1, 10**20))))):
            with self.subTest(coefficient=name):
                with self.assertRaisesRegex(ValueError, name+' exact minimum .* is below the theorem epsilon '+EPSILON[name]):
                    driver.top_margins(record)

    def test_missing_or_malformed_minimum_refused(self):
        record = top_record()
        del record['results']['3']['minimum']
        with self.assertRaisesRegex(ValueError, 'c7 small receipt has no exact minimum string'):
            driver.top_margins(record)
        with self.assertRaisesRegex(ValueError, 'c8 small receipt has no exact minimum string'):
            driver.top_margins({'status':'PASS_COMPLETE', 'results':{'1':{'minimum':'1/2'}, '3':{'minimum':'1/144'}}})
        for text, message in (('0.5', 'is not an exact rational'), ('None', 'is not an exact rational'),
                              ('1/0', 'has a zero denominator'), ('2/4', 'is not in lowest terms')):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, message):
                    driver.top_margins(top_record(c9=text))


class SmallDriverTests(unittest.TestCase):
    def run_driver(self, scratch, top):
        """Run the driver with fake children that write the given small receipts."""
        out = scratch/'small'

        def fake_owned(command, stdout, stderr, timeout, env):
            if '--output' in command:
                Path(command[command.index('--output')+1]).write_text(json.dumps(top), encoding='utf-8')
            if '--out' in command:
                Path(command[command.index('--out')+1]).write_text(
                    json.dumps({'status':'PASS_COMPLETE_C6'}), encoding='utf-8')
            return {'exit':0, 'owned_process_group_exited':True}

        handlers = {sig:signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT)}
        try:
            with patch.object(driver, 'run_owned', side_effect=fake_owned), \
                    patch.object(sys, 'argv', ['verify.py', 'small', '--out', str(out)]), \
                    patch('builtins.print'):
                driver.main()
        finally:
            for sig, handler in handlers.items():
                signal.signal(sig, handler)
        return json.loads((out/'RESULT.json').read_text(encoding='utf-8'))

    def test_driver_records_margins(self):
        with tempfile.TemporaryDirectory() as scratch:
            result = self.run_driver(Path(scratch), top_record())
            self.assertEqual(result['status'], 'PASS_COMPLETE_SMALL_COMPONENTS')
            self.assertEqual(result['margins']['c8'], {'exact_minimum':'1/9', 'theorem_epsilon':'1/9'})

    def test_driver_refuses_below_epsilon(self):
        with tempfile.TemporaryDirectory() as scratch:
            with self.assertRaisesRegex(ValueError, 'c7 exact minimum 1/145 is below the theorem epsilon 1/144'):
                self.run_driver(Path(scratch), top_record(c7='1/145'))
            result = json.loads((Path(scratch)/'small/RESULT.json').read_text(encoding='utf-8'))
            self.assertEqual(result['status'], 'FAILED')


if __name__ == '__main__':
    unittest.main()
