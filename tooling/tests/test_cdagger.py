"""The complete fixed certificate, actual whole-hive vectors and domain refusals."""
from fractions import Fraction
import unittest
from unittest.mock import patch

from slr_ehrhart import cdagger


OLD = ([43, 38, 33, 20, 12, 6], [22, 17, 16, 12, 6], [26, 21, 16, 12, 4])
NEIGHBOR = ([25, 22, 19, 11, 7, 3], [13, 10, 9, 7, 3], [15, 12, 9, 7, 2])
EXPECTED = (
    ('1', '3053/210', '5927/63', '325931/945', '211867/270', '104159/90',
     '101201/90', '224828/315', '89596/315', '60952/945', '856/135'),
    ('1', '3403/420', '17933/630', '1701871/30240', '260747/3780', '315221/5760',
     '164177/5760', '194531/20160', '41101/20160', '5893/24192', '1517/120960'),
)


class CdaggerTests(unittest.TestCase):
    def test_all_36_implications_and_complete_unimodular_hive_map(self):
        result = cdagger.verify_cdagger_certificate()
        self.assertEqual(result, {'domain_rows': 553, 'hive_rows': 45, 'model_rows': 15,
                                  'parameter_implications': 6, 'omitted_hive_implications': 30,
                                  'integer_chart_dimension': 10})

    def test_complete_archived_normaliz_vectors_and_large_stretch(self):
        for triple, expected in zip((OLD, NEIGHBOR), EXPECTED):
            coefficients = tuple(Fraction(value) for value in expected)
            self.assertEqual(cdagger.cdagger_polynomial(*triple), coefficients)
            for t in (0, 1, 2, 11, 12, 1000):
                self.assertEqual(cdagger.cdagger_count(*triple, t),
                                 sum(value * t**power for power, value in enumerate(coefficients)))
        self.assertEqual(cdagger.cdagger_parameters(*OLD),
                         {'x': 1, 'T': 4, 'Bcap': 2, 'C': 2, 'D': 2})

    def test_zero_point_boundary_and_dilation(self):
        self.assertEqual(cdagger.cdagger_polynomial([], [], []), (Fraction(1),))
        point = ([2, 2, 2, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1])
        self.assertEqual(cdagger.cdagger_polynomial(*point), (Fraction(1),))
        doubled = [[2 * value for value in part] for part in OLD]
        padded = [part + [0] * 3 for part in OLD]
        self.assertEqual(cdagger.cdagger_count(*doubled, 2), cdagger.cdagger_count(*OLD, 4))
        self.assertEqual(cdagger.cdagger_count(*padded, 2), cdagger.cdagger_count(*OLD, 2))

    def test_complete_domain_is_required_beyond_nonnegative_parameters(self):
        # Swapping inner partitions preserves the LR value, but changes its
        # conventional hive. This orientation is outside the certified sector.
        with self.assertRaises(cdagger.OutsideCdaggerError):
            cdagger.cdagger_count(OLD[0], OLD[2], OLD[1])
        with self.assertRaises(cdagger.OutsideCdaggerError):
            cdagger.cdagger_count([1] * 7, [1] * 7, [], 0)

    def test_invalid_inputs_are_not_zero_counts(self):
        for bad in [True, 1.0, Fraction(1), '1']:
            with self.assertRaises(ValueError):
                cdagger.cdagger_count([bad], [1], [])
            with self.assertRaises(ValueError):
                cdagger.cdagger_count(*OLD, bad)
        for triple in [([1, 2], [2, 1], []), ([1], [], []), ([-1], [], [])]:
            with self.assertRaises(ValueError):
                cdagger.cdagger_parameters(*triple)

    def test_missing_duplicate_and_false_certificate_rows_refuse(self):
        with patch.object(cdagger.data, 'DUALS', cdagger.data.DUALS[:-1]):
            with self.assertRaises(ValueError):
                cdagger.verify_cdagger_certificate()
        with patch.object(cdagger.data, 'DUALS', cdagger.data.DUALS[:-1] + cdagger.data.DUALS[:1]):
            with self.assertRaises(ValueError):
                cdagger.verify_cdagger_certificate()
        first = cdagger.data.DUALS[0]
        changed = (first[0], first[1], ((first[2][0][0], '-1'),), first[3])
        with patch.object(cdagger.data, 'DUALS', (changed,) + cdagger.data.DUALS[1:]):
            with self.assertRaises(ValueError):
                cdagger.verify_cdagger_certificate()
        with patch.object(cdagger.data, 'DOMAIN_ROWS', cdagger.data.DOMAIN_ROWS[:-1]):
            with self.assertRaises(ValueError):
                cdagger.verify_cdagger_certificate()


if __name__ == '__main__':
    unittest.main()
