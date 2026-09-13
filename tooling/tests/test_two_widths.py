"""Literal whole-object controls, exact coefficient limits and input refusals."""
from fractions import Fraction
from math import comb
import unittest

from slr_ehrhart.two_widths import two_width_count, two_width_polynomial


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def literal_count(left, right, total, left_offset, right_offset, dilation):
    answer = 0
    for point in compositions(dilation * total, len(left)):
        left_width = dilation * left_offset + sum(a * u for a, u in zip(left, point))
        right_width = dilation * right_offset + sum(b * u for b, u in zip(right, point))
        for _x in range(left_width + 1):
            for _z in range(right_width + 1):
                answer += 1
    return answer


class TwoWidthTests(unittest.TestCase):
    def test_literal_complete_lattice_panel(self):
        panel = [
            ((3,), (5,), 2, 1, 2),
            ((7, 0), (0, 7), 1, 0, 0),
            ((6, 0), (0, 8), 1, 0, 0),
            ((1, 3), (2, 4), 2, 1, 2),
            ((0, 2, 1), (3, 1, 2), 2, 0, 1),
            ((0, 0, 0, 0), (0, 0, 0, 0), 2, 1, 0),
            ((3, 0, 1), (0, 2, 4), 0, 2, 3),
        ]
        for left, right, total, left_offset, right_offset in panel:
            options = dict(total=total, left_offset=left_offset, right_offset=right_offset)
            coefficients = two_width_polynomial(left, right, **options)
            self.assertIsInstance(coefficients, tuple)
            self.assertTrue(all(type(value) is Fraction for value in coefficients))
            for dilation in (0, 1, 2, 3):
                with self.subTest(left=left, right=right, dilation=dilation, **options):
                    expected = literal_count(left, right, total, left_offset,
                                             right_offset, dilation)
                    actual = two_width_count(left, right, dilation=dilation, **options)
                    self.assertIs(type(actual), int)
                    self.assertEqual(actual, expected)
                    self.assertEqual(sum(value * dilation**k
                                         for k, value in enumerate(coefficients)), expected)

    def test_negative_zero_and_overlapping_coefficients(self):
        self.assertEqual(two_width_polynomial((7, 0), (0, 7)),
                         (Fraction(1), Fraction(-1, 6), Fraction(7), Fraction(49, 6)))
        self.assertEqual(two_width_polynomial((6, 0), (0, 8)),
                         (Fraction(1), Fraction(0), Fraction(7), Fraction(8)))
        # Both coordinates contribute to both widths, with nonzero covariance.
        self.assertEqual(two_width_polynomial((1, 3), (2, 4)),
                         (Fraction(1), Fraction(20, 3), Fraction(12), Fraction(19, 3)))

    def test_degenerate_models_and_list_normalization(self):
        self.assertEqual(two_width_polynomial([2], (3,), total=4,
                                             left_offset=1, right_offset=2),
                         (Fraction(1), Fraction(23), Fraction(126)))
        left, right = [3, 0, 1], [0, 2, 4]
        self.assertEqual(two_width_polynomial(left, right, total=0,
                                             left_offset=2, right_offset=3),
                         (Fraction(1), Fraction(5), Fraction(6)))
        self.assertEqual(two_width_polynomial(left, right, total=0, left_offset=4),
                         (Fraction(1), Fraction(4)))
        self.assertEqual(two_width_polynomial(left, right, total=0), (Fraction(1),))
        self.assertEqual((left, right), ([3, 0, 1], [0, 2, 4]))
        self.assertEqual(two_width_polynomial((0,), (0,), total=8), (Fraction(1),))
        self.assertEqual(two_width_polynomial((0, 0, 0), (0, 0, 0), total=2),
                         (Fraction(1), Fraction(3), Fraction(2)))

    def test_huge_dilation_with_constant_widths_on_each_simplex(self):
        dilation = 10**30
        # Widths are 11*t and 19*t at every five-total composition.
        expected = comb(5 * dilation + 2, 2) * (11 * dilation + 1) * (19 * dilation + 1)
        self.assertEqual(two_width_count((2, 2, 2), (3, 3, 3), total=5,
                                         left_offset=1, right_offset=4, dilation=dilation),
                         expected)

    def test_input_refusals_before_degenerate_shortcuts(self):
        functions = (two_width_count, two_width_polynomial)
        bad_values = (-1, True, False, 1.0, Fraction(1), '1', None)
        for function in functions:
            for field in ('total', 'left_offset', 'right_offset'):
                for bad in bad_values:
                    options = dict(total=0)
                    options[field] = bad
                    with self.subTest(function=function.__name__, field=field, bad=bad):
                        with self.assertRaises(ValueError):
                            function((0,), (0,), **options)
            for bad in (None, '0', b'0', bytearray(b'0'), {}, {0}, 0, [],
                        [True], [False], [1.0], [Fraction(1)], [-1]):
                for slot in (0, 1):
                    vectors = [[0], [0]]
                    vectors[slot] = bad
                    with self.subTest(function=function.__name__, slot=slot, bad=bad):
                        with self.assertRaises(ValueError):
                            function(*vectors, total=0)
            for left, right in (((), ()), ((0,), (0, 0)), ((0, 0), (0,))):
                with self.assertRaises(ValueError):
                    function(left, right)
        for bad in bad_values:
            with self.subTest(dilation=bad), self.assertRaises(ValueError):
                two_width_count((0,), (0,), total=0, dilation=bad)


if __name__ == '__main__':
    unittest.main()
