"""Whole-object counts, independently enumerated controls and exact limits."""
from fractions import Fraction
from itertools import product
from math import comb
import unittest

from slr_ehrhart.strip import strip_count, strip_polynomial


def compositions(total, parts):
    if not parts:
        if total == 0:
            yield ()
        return
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def literal_count(h, q1, q2, total, lower, upper, height, t):
    answer = 0
    for point in compositions(t * total, h + q1 + q2):
        u, v = sum(point[:h]), sum(point[h:h + q1])
        answer += len(range(max(0, v - t * lower), t * height + min(t * upper, u + v) + 1))
    return answer


class StripTests(unittest.TestCase):
    def test_complete_small_lattices_and_all_closed_cut_cases(self):
        for h, q1, q2 in [(0, 1, 1), (0, 2, 1), (1, 1, 2), (2, 1, 1)]:
            for total, lower, upper, height in product(range(3), repeat=4):
                if total > lower + upper + height:
                    continue
                for t in [0, 1, 2]:
                    with self.subTest(parameters=(h, q1, q2, total, lower, upper, height, t)):
                        self.assertEqual(strip_count(h, q1, q2, total, lower, upper, height, t),
                                         literal_count(h, q1, q2, total, lower, upper, height, t))

    def test_inactive_cuts_and_huge_dilation(self):
        t = 10**30
        # Three-part compositions; U+V has two coordinates.
        expected = comb(t + 2, 2) + 2 * comb(t + 2, 3)
        self.assertEqual(strip_count(1, 1, 1, 1, 1, 1, 0, t), expected)

    def test_dimension_drops_and_independent_intervals(self):
        self.assertEqual(strip_polynomial(0, 1, 1, 0, 0, 0, 0), (Fraction(1),))
        self.assertEqual(strip_polynomial(0, 1, 1, 0, 0, 0, 3), (Fraction(1), Fraction(3)))
        # h=0, B=C=D=0 is only admissible at T=0. A zero upper cap
        # and inactive lower cut also leave the whole interval a point.
        self.assertEqual(strip_polynomial(0, 1, 1, 2, 2, 0, 0), (Fraction(1), Fraction(2)))
        self.assertEqual(strip_polynomial(0, 1, 1, 0, 0, 0, 3, interval_lengths=[0, 2]),
                         (Fraction(1), Fraction(5), Fraction(6)))

    def test_full_coefficients_unused_holdouts_and_linear_formula(self):
        for h, q1, q2, total, lower, upper, height in [
                (0, 2, 3, 3, 1, 1, 1), (1, 1, 4, 2, 3, 1, 2),
                (3, 3, 3, 4, 2, 2, 1), (1, 4, 1, 3, 2, 1, 0)]:
            coefficients = strip_polynomial(h, q1, q2, total, lower, upper, height)
            self.assertTrue(all(value > 0 for value in coefficients))
            n = h + q1 + q2
            harmonic = sum((Fraction(1, j) for j in range(1, n)), Fraction(0))
            c1 = (height + (harmonic - Fraction(q1, n)) * total
                  + Fraction(h + q1, n) * min(upper, total)
                  + Fraction(q1, n) * min(lower, total))
            self.assertEqual(coefficients[1], c1)
            for t in [n + 1, n + 2]:
                self.assertEqual(sum(value * t**k for k, value in enumerate(coefficients)),
                                 strip_count(h, q1, q2, total, lower, upper, height, t))

    def test_input_refusals_before_degenerate_shortcuts(self):
        for bad in [True, False, 1.0, '1', Fraction(1), None]:
            for slot in range(8):
                args = [0, 1, 1, 0, 0, 0, 0, 0]
                args[slot] = bad
                with self.subTest(slot=slot, bad=bad), self.assertRaises(ValueError):
                    strip_count(*args)
        for args in [(0, 0, 1, 0, 0, 0, 0), (0, 1, 1, 1, 0, 0, 0),
                     (-1, 1, 1, 0, 0, 0, 0)]:
            with self.assertRaises(ValueError):
                strip_count(*args)
        for intervals in [None, '12', [True], [-1], [Fraction(1)]]:
            with self.assertRaises(ValueError):
                strip_count(0, 1, 1, 0, 0, 0, 0, interval_lengths=intervals)


if __name__ == '__main__':
    unittest.main()
