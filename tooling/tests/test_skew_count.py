"""Independent small-cell and limit-contract checks for the skew SSYT counter."""

from fractions import Fraction
from itertools import product
import unittest

from slr_ehrhart.skew_count import SkewCountLimitError, skew_tableau_count


def literal_tableaux(outer, inner, content, t=1):
    """Fill actual skew cells, checking rows weakly and columns strictly."""
    inner = tuple(inner) + (0,) * (len(outer) - len(inner))
    cells = [(i, j) for i, length in enumerate(outer)
             for j in range(t * inner[i], t * length)]
    expected = tuple(t * weight for weight in content)
    labels = range(1, len(content) + 1)
    answer = 0
    for entries in product(labels, repeat=len(cells)):
        if tuple(entries.count(label) for label in labels) != expected:
            continue
        filling = dict(zip(cells, entries))
        if any(((i, j + 1) in filling and value > filling[i, j + 1])
               or ((i + 1, j) in filling and value >= filling[i + 1, j])
               for (i, j), value in filling.items()):
            continue
        answer += 1
    return answer


class SkewTableauCountTests(unittest.TestCase):
    def test_small_shapes_and_every_three_label_content_against_cells(self):
        shapes = [((2, 1), ()), ((2, 2), (1,)), ((3, 2), (1, 1)),
                  ((3, 1), (1,)), ((2, 2, 1), (1, 1)), ((3, 2, 1), (2, 1))]
        for outer, inner in shapes:
            size = sum(outer) - sum(inner)
            for first in range(size + 1):
                for second in range(size - first + 1):
                    content = (first, second, size - first - second)
                    with self.subTest(outer=outer, inner=inner, content=content):
                        self.assertEqual(skew_tableau_count(outer, inner, content),
                                         literal_tableaux(outer, inner, content))

    def test_straight_tableaux_and_actual_column_constraints(self):
        for outer, content, expected in [((2, 1), (1, 1, 1), 2),
                                         ((2, 2), (1, 1, 1, 1), 2),
                                         ((3, 1), (1, 1, 1, 1), 3),
                                         ((1, 1), (1, 1), 1),
                                         ((1, 1), (2, 0), 0),
                                         ((1, 1, 1), (1, 2), 0)]:
            with self.subTest(outer=outer, content=content):
                self.assertEqual(literal_tableaux(outer, (), content), expected)
                self.assertEqual(skew_tableau_count(outer, (), content), expected)
        # These skew cells occupy three distinct columns despite using two rows.
        self.assertEqual(skew_tableau_count((3, 1), (1,), (3,)), 1)
        # The inner corner is absent: it must not create a spurious comparison.
        self.assertEqual(skew_tableau_count((2, 1), (1,), (1, 1)), 2)

    def test_content_order_zero_labels_and_input_copy(self):
        outer, inner, content = [3, 2, 0], [1, 0], [0, 1, 0, 2, 1, 0]
        original = (list(outer), list(inner), list(content))
        expected = literal_tableaux(outer, inner, content)
        self.assertEqual(skew_tableau_count(outer, inner, content), expected)
        self.assertEqual((outer, inner, content), original)
        for weights in ((1, 2, 1), (2, 1, 1), (1, 1, 2), (1, 0, 2, 0, 1)):
            with self.subTest(content=weights):
                self.assertEqual(skew_tableau_count(outer, inner, weights),
                                 literal_tableaux(outer, inner, weights))

    def test_scaling_matches_explicit_dilation_and_literal_cells(self):
        for outer, inner, content in [((2, 1), (1,), (1, 1)),
                                      ((2, 1), (), (1, 1, 1)),
                                      ((2, 2), (1, 1), (1, 1))]:
            for stretch in (0, 1, 2):
                with self.subTest(outer=outer, inner=inner, content=content, stretch=stretch):
                    expected = literal_tableaux(outer, inner, content, stretch)
                    self.assertEqual(skew_tableau_count(outer, inner, content, stretch), expected)
                    self.assertEqual(skew_tableau_count(tuple(stretch * x for x in outer),
                                                       tuple(stretch * x for x in inner),
                                                       tuple(stretch * x for x in content)), expected)

    def test_empty_zero_and_huge_trivial_fibers_use_no_dp_work(self):
        huge = 10 ** 60
        fixtures = [((), (), (0,), huge, 1), ((huge, huge), (huge, huge), (0, 0), huge, 1),
                    ((4,), (1,), (1, 0, 2), huge, 1),
                    ((3, 1), (1,), (0, 3, 0), huge, 1),
                    ((1, 1), (), (2,), huge, 0),
                    ((1, 1, 1), (), (1, 0, 2), huge, 0),
                    ((1, 1), (), (2,), 0, 1),
                    ((2, 1), (), (1, 1, 1), 0, 1)]
        for outer, inner, content, stretch, expected in fixtures:
            with self.subTest(outer=outer, inner=inner, content=content, stretch=stretch):
                self.assertEqual(skew_tableau_count(outer, inner, content, stretch,
                                                   max_states=0, max_transitions=0), expected)
        # A forced chain beyond the elementary shortcuts also stays bounded.
        self.assertEqual(skew_tableau_count((2, 1), (), (1, 2), huge,
                                           max_states=5, max_transitions=4), 1)

    def test_lab_132_cheap_family_control(self):
        s = 11
        outer = (2 * s + 8, 2 * s + 4, 3, 2, 1)
        content = (s + 3, s + 3, s + 3, s + 1, 1, 1, 1, 1, 1)
        self.assertEqual(skew_tableau_count(outer, (2, 1), content), 1805398)


class WorkLimitTests(unittest.TestCase):
    fixture = ((2, 1), (), (1, 1, 1))

    def test_initial_state_is_charged_and_zero_transition_budget_is_respected(self):
        with self.assertRaises(SkewCountLimitError) as caught:
            skew_tableau_count(*self.fixture, max_states=0)
        self.assertEqual(caught.exception.resource, "states")
        self.assertEqual(caught.exception.limit, 0)
        self.assertEqual(caught.exception.statistics, {"states": 0, "transitions": 0})
        with self.assertRaises(SkewCountLimitError) as caught:
            skew_tableau_count(*self.fixture, max_transitions=0)
        self.assertEqual(caught.exception.resource, "transitions")
        self.assertEqual(caught.exception.statistics, {"states": 1, "transitions": 0})

    def test_admission_checks_are_atomic_and_never_exceed_either_cap(self):
        with self.assertRaises(SkewCountLimitError) as caught:
            skew_tableau_count(*self.fixture, max_states=1, max_transitions=100)
        self.assertEqual(caught.exception.statistics, {"states": 1, "transitions": 0})
        with self.assertRaises(SkewCountLimitError) as caught:
            skew_tableau_count(*self.fixture, max_states=100, max_transitions=1)
        self.assertEqual(caught.exception.statistics, {"states": 2, "transitions": 1})
        for name in ("count", "value", "partial_count", "partial_value"):
            self.assertFalse(hasattr(caught.exception, name))
        self.assertIn("incomplete", str(caught.exception))
        self.assertEqual(skew_tableau_count(*self.fixture, max_states=100, max_transitions=100), 2)
        self.assertEqual(skew_tableau_count(*self.fixture), 2)

    def test_exception_statistics_are_copied(self):
        statistics = {"states": 4, "transitions": 9}
        error = SkewCountLimitError("states", 4, statistics)
        statistics["states"] = 999
        self.assertEqual(error.statistics, {"states": 4, "transitions": 9})
        error.statistics["transitions"] = 0
        self.assertEqual(statistics["transitions"], 9)


class ValidationTests(unittest.TestCase):
    def test_exact_entry_rejections(self):
        class IntegerSubclass(int):
            pass

        for bad in (True, False, IntegerSubclass(1), Fraction(1), Fraction(1, 2),
                    1.0, "1", None, -1):
            for position in range(3):
                arguments = [[1], [0], [1]]
                arguments[position] = [bad]
                with self.subTest(bad=bad, position=position), self.assertRaises(ValueError):
                    skew_tableau_count(*arguments)

    def test_sequence_rejections(self):
        for bad in ("1", b"1", bytearray(b"1"), {1}, {0: 1}, None, 1, iter([1])):
            for position in range(3):
                arguments = [[1], [], [1]]
                arguments[position] = bad
                with self.subTest(bad=bad, position=position), self.assertRaises(ValueError):
                    skew_tableau_count(*arguments)

    def test_partition_containment_alphabet_and_size_checks_precede_zero_dilation(self):
        fixtures = [((1, 2), (), (3,)), ((2, 2), (0, 1), (3,)),
                    ((2, 1), (3,), (0,)), ((1,), (1, 1), (0,)),
                    ((), (), ()), ((1,), (), (0,)), ((1,), (), (2,))]
        for outer, inner, content in fixtures:
            for stretch in (0, 1):
                with self.subTest(outer=outer, inner=inner, content=content, stretch=stretch), \
                        self.assertRaises(ValueError):
                    skew_tableau_count(outer, inner, content, stretch)

    def test_scalar_and_limit_validation_precedes_all_shortcuts(self):
        for name in ("t", "max_states", "max_transitions"):
            for bad in (True, False, Fraction(0), 0.0, "0", -1):
                with self.subTest(name=name, bad=bad), self.assertRaises(ValueError):
                    skew_tableau_count((), (), (0,), **{name: bad})
        with self.assertRaises(ValueError):
            skew_tableau_count((), (), (0,), None)
        with self.assertRaises(ValueError):
            skew_tableau_count((1,), (), (1,), 0, max_states=False)


if __name__ == "__main__":
    unittest.main()
