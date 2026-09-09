"""Exact transportation and quotient count regression tests."""

from fractions import Fraction
from itertools import product
from math import factorial, prod
import unittest

from slr_ehrhart.transport import (
    minkowski_obstruction, segment_quotient_count, transport_count, transport_to_lr,
)


def literal_tables(rows, columns):
    """Tiny independent cell-product enumeration, without residual recursion."""
    p, q = len(rows), len(columns)
    bounds = [min(r, c) for r in rows for c in columns]
    for entries in product(*(range(bound + 1) for bound in bounds)):
        if (all(sum(entries[i * q:(i + 1) * q]) == rows[i] for i in range(p))
                and all(sum(entries[i * q + j] for i in range(p)) == columns[j]
                        for j in range(q))):
            yield entries


def literal_quotient(rows, columns, t=1):
    """Tiny direct weighted sum over every independently bounded cell."""
    rows, columns = [t * x for x in rows], [t * x for x in columns]
    p, q = len(rows), len(columns)
    result = 0
    for entries in product(*(range(min(r, c) + 1) for r in rows for c in columns)):
        row_slack = [rows[i] - sum(entries[i * q:(i + 1) * q]) for i in range(p)]
        col_slack = [columns[j] - sum(entries[i * q + j] for i in range(p)) for j in range(q)]
        if all(value >= 0 for value in row_slack + col_slack):
            result += prod(value + 1 for value in row_slack + col_slack)
    return result


class TransportTests(unittest.TestCase):
    def test_labeled_counts_against_literal_cells(self):
        fixtures = [([], []), ([], [0, 0]), ([0, 0], []), ([0, 1, 0], [1, 0]),
                    ([2], [1, 0, 1]), ([1, 1], [1, 1]), ([2, 1], [1, 2]),
                    ([1, 2, 1], [2, 1, 1]), ([1, 1, 1], [1, 1, 1])]
        for rows, columns in fixtures:
            with self.subTest(rows=rows, columns=columns):
                expected = sum(1 for _ in literal_tables(rows, columns))
                self.assertEqual(transport_count(rows, columns), expected)
                self.assertEqual(transport_count(columns, rows), expected)
                self.assertEqual(transport_count(rows[::-1], columns[::-1]), expected)

    def test_equal_residuals_keep_labeled_multiplicity(self):
        for n in (2, 3, 6, 10):
            self.assertEqual(transport_count([1] * n, [1] * n), factorial(n))

    def test_two_by_two_completion_interval(self):
        for rows, columns in [([3, 2], [1, 4]), ([0, 5], [2, 3]), ([4, 4], [3, 5])]:
            expected = min(rows[0], columns[0]) - max(0, rows[0] - columns[1]) + 1
            self.assertEqual(transport_count(rows, columns), expected)

    def test_arbitrary_precision_forced_table_and_empty(self):
        huge = 10 ** 60
        self.assertEqual(transport_count([huge], [0, huge - 1, 1]), 1)
        self.assertEqual(transport_count([0, 0], [0, 0, 0]), 1)
        self.assertEqual(transport_count([], []), 1)

    def test_tail_lift_order_zero_padding_and_copy(self):
        rows, columns = [0, 2, 1, 0], [1, 0, 2, 0]
        got = transport_to_lr(rows, columns)
        self.assertEqual(got["metadata"]["input"], {
            "outer": [3, 2, 2, 0], "inner": [2, 2, 0], "content": rows,
        })
        self.assertEqual(got["metadata"]["transportation"], {
            "row_margins": rows, "column_margins": columns, "ambient_rank": 7,
            "domain": "entire nonnegative transportation polytope with these labeled margins",
            "lattice_preservation": "disconnected-row tableau identification, then integral skew-content lift",
        })
        self.assertIsNone(got["metadata"]["dimension"])
        self.assertIsNone(got["metadata"]["degree"])
        rows[0] = columns[0] = 99
        self.assertEqual(got["metadata"]["transportation"]["row_margins"], [0, 2, 1, 0])
        self.assertEqual(got["metadata"]["transportation"]["column_margins"], [1, 0, 2, 0])

    def test_segment_lift_and_zero_total(self):
        segment = [1, 1, 0, 0]
        got = transport_to_lr(segment, segment)
        self.assertEqual([got[key] for key in ("lambda", "mu", "nu")],
                         [[3, 2, 2, 2, 1], [2, 2, 2, 1], [2, 1]])
        self.assertEqual(got["metadata"]["transportation"]["ambient_rank"], 7)
        zero = transport_to_lr([0, 0, 0], [0, 0])
        self.assertEqual([zero[key] for key in ("lambda", "mu", "nu")], [[], [], []])
        self.assertEqual(zero["metadata"]["transportation"]["ambient_rank"], 4)
        self.assertIsNone(zero["metadata"]["dimension"])

    def test_asymmetric_obstruction_and_repair(self):
        rows, columns, segment = [1, 3, 1, 1], [2, 2, 1, 1], [1, 1, 0, 0]
        self.assertEqual(minkowski_obstruction(rows, columns, segment, segment), {
            "row_indices": [0], "column_indices": [0, 1], "delta1": -1, "delta2": 1,
        })
        repaired_rows = [r + e for r, e in zip(rows, segment)]
        repaired_columns = [c + e for c, e in zip(columns, segment)]
        self.assertIsNone(minkowski_obstruction(repaired_rows, repaired_columns, segment, segment))
        self.assertIsNone(minkowski_obstruction(columns, columns, segment, segment))

    def test_cut_matches_entire_tiny_minkowski_sum(self):
        fixtures = [([1, 0], [1, 0], [0, 1], [0, 1]),
                    ([1, 1], [1, 1], [1, 1], [1, 1]),
                    ([0, 1], [1, 0], [0, 0], [0, 0]),
                    ([], [0], [], [0])]
        for r, c, s, d in fixtures:
            with self.subTest(margins=(r, c, s, d)):
                sums = {tuple(x + y for x, y in zip(a, b))
                        for a in literal_tables(r, c) for b in literal_tables(s, d)}
                whole = set(literal_tables([x + y for x, y in zip(r, s)],
                                           [x + y for x, y in zip(c, d)]))
                self.assertEqual(minkowski_obstruction(r, c, s, d) is None, sums == whole)

    def test_empty_zero_and_large_integer_cut(self):
        self.assertIsNone(minkowski_obstruction([], [], [], []))
        self.assertIsNone(minkowski_obstruction([], [0, 0], [], [0, 0]))
        huge = 10 ** 60
        got = minkowski_obstruction([huge, 0], [huge, 0], [0, huge], [0, huge])
        self.assertIsNotNone(got)
        self.assertLess(got["delta1"] * got["delta2"], 0)


class QuotientTests(unittest.TestCase):
    def test_literal_weighted_unequal_and_equal_caps(self):
        fixtures = [([], [], 1), ([], [1, 2], 2), ([2, 0], [], 3),
                    ([1], [2], 3), ([1, 1], [1, 1], 2),
                    ([0, 2], [1, 0, 1], 1), ([1, 2], [2, 1], 1),
                    ([1, 1, 1], [1, 1, 1], 1), ([1, 2, 1], [2, 1, 1], 1)]
        for rows, columns, t in fixtures:
            with self.subTest(rows=rows, columns=columns, t=t):
                expected = literal_quotient(rows, columns, t)
                self.assertEqual(segment_quotient_count(rows, columns, t), expected)
                self.assertEqual(segment_quotient_count(columns, rows, t), expected)
                self.assertEqual(segment_quotient_count(rows[::-1], columns[::-1], t), expected)

    def test_one_by_one_closed_sum(self):
        for a, b, t in [(1, 1, 1), (2, 5, 3), (0, 7, 2)]:
            a, b = a * t, b * t
            n = min(a, b)
            expected = ((n + 1) * (a + 1) * (b + 1)
                        - (a + b + 2) * n * (n + 1) // 2
                        + n * (n + 1) * (2 * n + 1) // 6)
            self.assertEqual(segment_quotient_count([a], [b]), expected)

    def test_empty_products_zero_caps_and_zero_stretch(self):
        huge = 10 ** 60
        self.assertEqual(segment_quotient_count([], [huge, 0], 2), 2 * huge + 1)
        self.assertEqual(segment_quotient_count([huge], [0]), huge + 1)
        self.assertEqual(segment_quotient_count([], [], huge), 1)
        self.assertEqual(segment_quotient_count([2, 7], [3, 1], 0), 1)
        self.assertEqual(segment_quotient_count([0, 0], [0, 0, 0]), 1)

    def test_whole_transport_segment_slope_in_valid_chamber(self):
        base, segment = [1, 1, 1], [1, 1, 0]
        self.assertIsNone(minkowski_obstruction(base, base, segment, segment))
        for t, m in [(0, 2), (1, 1), (2, 1), (1, 2)]:
            enlarged = [t * (r + m * e) for r, e in zip(base, segment)]
            unshifted = [t * r for r in base]
            self.assertEqual(transport_count(enlarged, enlarged)
                             - transport_count(unshifted, unshifted),
                             m * t * segment_quotient_count([1], [1], t))


class InputTests(unittest.TestCase):
    def test_exact_entry_rejections_across_apis(self):
        for bad in (True, False, Fraction(1), Fraction(1, 2), "1", 1.0, None, -1):
            for fn in (transport_count, transport_to_lr, segment_quotient_count):
                for args in (([bad], [1]), ([1], [bad])):
                    with self.subTest(fn=fn.__name__, args=args), self.assertRaises(ValueError):
                        fn(*args)
            for position in range(4):
                args = [[1], [1], [1], [1]]
                args[position] = [bad]
                with self.subTest(cut_position=position, bad=bad), self.assertRaises(ValueError):
                    minkowski_obstruction(*args)
            with self.subTest(t=bad), self.assertRaises(ValueError):
                segment_quotient_count([1], [1], bad)

    def test_sequence_rejections(self):
        for bad in ("1", b"1", bytearray(b"1"), {1}, {0: 1}, None, 1):
            for fn in (transport_count, transport_to_lr, segment_quotient_count):
                for args in ((bad, [1]), ([1], bad)):
                    with self.subTest(fn=fn.__name__, args=args), self.assertRaises(ValueError):
                        fn(*args)
            with self.subTest(cut=bad), self.assertRaises(ValueError):
                minkowski_obstruction(bad, [1], [1], [1])

    def test_imbalance_empty_lift_and_incompatible_chart(self):
        for fn in (transport_count, transport_to_lr):
            for rows, columns in [([1], [2]), ([], [1]), ([1], [])]:
                with self.subTest(fn=fn.__name__, margins=(rows, columns)), self.assertRaises(ValueError):
                    fn(rows, columns)
        for rows, columns in [([], []), ([], [0]), ([0], [])]:
            with self.subTest(lift=(rows, columns)), self.assertRaises(ValueError):
                transport_to_lr(rows, columns)
        for args in [([1], [1], [1, 0], [1]), ([1], [1], [1], [1, 0]),
                     ([1], [2], [1], [1]), ([1], [1], [1], [2])]:
            with self.subTest(cut=args), self.assertRaises(ValueError):
                minkowski_obstruction(*args)


if __name__ == "__main__":
    unittest.main()
