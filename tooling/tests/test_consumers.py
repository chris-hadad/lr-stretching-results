"""Existing Codex and native Fable objects exercised through maintained tools.

Running these checks in Codex does not assert native deployment or acceptance.
"""
import importlib.util
import json
from pathlib import Path
import unittest

from slr_ehrhart.flow_support import flow_support_certificate, verify_flow_support_certificate
from slr_ehrhart.transport import transport_count, segment_quotient_count

FIXTURES = Path(__file__).resolve().parent / 'fixtures'


def native_oracles():
    spec = importlib.util.spec_from_file_location('native_k_oracles', FIXTURES / 'native_k_oracles.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExistingConsumerTests(unittest.TestCase):
    def test_six_native_chart_tables_against_original_native_algorithm(self):
        original = native_oracles()
        for m in [0, 1, 3]:
            for t in [1, 2]:
                margins = tuple(t * value for value in [2 + m, 2 + m, 1, 1])
                self.assertEqual(transport_count(margins, margins), original.table_count(margins, margins))

    def test_nine_native_quotient_nodes_against_both_native_oracles(self):
        original = native_oracles()
        for t in range(9):
            expected = original.quotient_count_enumerated(t)
            self.assertEqual(original.quotient_count_closed_form(t), expected)
            self.assertEqual(segment_quotient_count([1, 1], [1, 1], t), expected)

    def test_complete_selected_frc_support_identity_and_degree_controls(self):
        fixture = json.loads((FIXTURES / 'frc_support_controls.json').read_text())
        controls = fixture['controls']
        self.assertEqual(len(controls), 26)
        self.assertEqual(len({row['parameter_index'] for row in controls}), 26)
        for row in controls:
            actual = flow_support_certificate(row['edges'], row['totals'])
            self.assertTrue(verify_flow_support_certificate(row['edges'], row['totals'], actual))
            self.assertEqual(actual['feasible'], row['feasible'])
            if row['feasible']:
                self.assertEqual(actual['active'], row['active'])
                self.assertEqual(actual['degree'], row['degree'])
            else:
                self.assertNotIn('degree', actual)


if __name__ == '__main__':
    unittest.main()
