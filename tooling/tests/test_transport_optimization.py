"""Independent bounded checks for labeled transport and quotient optimization.

Scientific execution belongs to the session's root-owned bounded runner.
"""

from collections import defaultdict
from fractions import Fraction
import importlib.util
from itertools import product
from math import comb, factorial, prod
from pathlib import Path
import unittest
from unittest.mock import patch

from slr_ehrhart import transport


def literal_transport(rows, columns):
    """Enumerate independently bounded cells, retaining every label."""
    p, q = len(rows), len(columns)
    return sum(
        all(sum(entries[i * q:(i + 1) * q]) == rows[i] for i in range(p))
        and all(sum(entries[i * q + j] for i in range(p)) == columns[j]
                for j in range(q))
        for entries in product(*(range(min(row, column) + 1)
                                 for row in rows for column in columns))
    )


def literal_quotient(rows, columns, t=1):
    """Direct cell-product enumeration, independent of residual recursion."""
    rows = tuple(t * row for row in rows)
    columns = tuple(t * column for column in columns)
    p, q = len(rows), len(columns)
    answer = 0
    for entries in product(*(range(min(row, column) + 1)
                             for row in rows for column in columns)):
        slack = [rows[i] - sum(entries[i * q:(i + 1) * q]) for i in range(p)]
        slack += [columns[j] - sum(entries[i * q + j] for i in range(p))
                  for j in range(q)]
        if all(value >= 0 for value in slack):
            answer += prod(value + 1 for value in slack)
    return answer


def literal_interior(rows, columns, stretch):
    """Count strictly positive z,u,v with strict active caps directly."""
    rows = tuple(stretch * value for value in rows if value)
    columns = tuple(stretch * value for value in columns if value)
    p, q = len(rows), len(columns)
    answer = 0
    for entries in product(*(range(1, min(row, column))
                             for row in rows for column in columns)):
        choices = [rows[i] - sum(entries[i * q:(i + 1) * q]) - 1
                   for i in range(p)]
        choices += [columns[j] - sum(entries[i * q + j] for i in range(p)) - 1
                    for j in range(q)]
        if all(value > 0 for value in choices):
            answer += prod(choices)
    return answer


def plain_coefficients(caps, target, *, linear=False):
    """Ordinary nested-loop polynomial multiplication without prefix sums."""
    coefficients = [1] + [0] * target
    for cap in caps:
        following = [0] * (target + 1)
        for degree, coefficient in enumerate(coefficients):
            for used in range(min(cap, target - degree) + 1):
                weight = cap - used + 1 if linear else 1
                following[degree + used] += coefficient * weight
        coefficients = following
    return coefficients


def original_transport_module():
    """Load the preserved original algorithm, never a second optimized alias."""
    path = Path(__file__).resolve().parent / "fixtures/transport_before_shared_tools.py"
    specification = importlib.util.spec_from_file_location(
        "slr_ehrhart._shared_tools_original_transport", path,
    )
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load the preserved original transport: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    if module.transport_count is transport.transport_count:
        raise AssertionError("the original oracle must have an independent implementation")
    return module


class OrbitTransitionTests(unittest.TestCase):
    def test_labeled_transition_weights_and_unequal_cap_collisions(self):
        for caps in ((), (1, 2), (1, 1, 2), (1, 2, 3), (2, 2, 3)):
            for row in range(sum(caps) + 2):
                for exact in (False, True):
                    expected = defaultdict(int)
                    for allocation in product(*(range(cap + 1) for cap in caps)):
                        used = sum(allocation)
                        if used > row or (exact and used != row):
                            continue
                        residual = tuple(sorted(cap - value
                                                for cap, value in zip(caps, allocation)
                                                if cap != value))
                        expected[residual] += 1 if exact else row - used + 1
                    with self.subTest(caps=caps, row=row, exact=exact):
                        transitions = list(transport._row_residuals(caps, row, exact=exact))
                        self.assertEqual(len(transitions), len(dict(transitions)))
                        self.assertEqual(dict(transitions), dict(expected))
        # One orbit of multiplicity one and one of multiplicity two collide.
        self.assertEqual(dict(transport._row_residuals((1, 1, 2), 2, exact=True))[(1, 1)], 3)
        self.assertEqual(dict(transport._row_residuals((1, 1, 2), 3, exact=False))[(1, 1)], 6)


class TransportOptimizationTests(unittest.TestCase):
    def test_all_small_two_by_three_margins_against_cells(self):
        for rows in product(range(3), repeat=2):
            for columns in product(range(3), repeat=3):
                if sum(rows) != sum(columns):
                    continue
                expected = literal_transport(rows, columns)
                with self.subTest(rows=rows, columns=columns):
                    self.assertEqual(transport.transport_count(rows, columns), expected)
                    self.assertEqual(transport.transport_count(columns, rows), expected)
                    self.assertEqual(transport.transport_count(rows[::-1], columns[::-1]), expected)

    def test_orbit_recurrence_against_independent_cells(self):
        for rows, columns in [((1, 1, 2), (2, 1, 1)), ((2, 2, 1), (1, 2, 2)),
                              ((1, 2, 1), (1, 1, 1, 1)),
                              ((0, 1, 2, 1), (1, 0, 1, 2))]:
            expected = literal_transport(rows, columns)
            with self.subTest(rows=rows, columns=columns):
                self.assertEqual(transport.transport_count(rows, columns), expected)
                self.assertEqual(transport.transport_count(columns, rows), expected)
                self.assertEqual(transport.transport_count(rows[::-1], columns[::-1]), expected)

    def test_equal_caps_count_every_permutation_matrix(self):
        for n in (2, 3, 6, 12, 40):
            with self.subTest(n=n):
                self.assertEqual(transport.transport_count([1] * n, [1] * n), factorial(n))

    def test_two_row_coefficients_and_complements(self):
        for caps in product(range(4), repeat=3):
            total = sum(caps)
            expected = plain_coefficients(caps, total)
            for target, coefficient in enumerate(expected):
                with self.subTest(caps=caps, target=target):
                    self.assertEqual(transport.transport_count((target, total - target), caps),
                                     coefficient)
                    self.assertEqual(transport.transport_count(caps, (total - target, target)),
                                     coefficient)
        for n in (6, 15, 40):
            for target in (1, n // 2, n - 1):
                self.assertEqual(transport.transport_count((target, n - target), (1,) * n),
                                 comb(n, target))

    def test_explicit_work_selection_exercises_both_exact_algorithms(self):
        caps = tuple(range(1, 14))
        target = sum(caps) // 2
        expected = plain_coefficients(caps, target)[target]
        with patch.object(transport, "_bounded_composition_inclusion",
                          side_effect=AssertionError("expected prefix DP")), \
                patch.object(transport, "_bounded_composition_dp",
                             wraps=transport._bounded_composition_dp) as prefix:
            self.assertEqual(transport.transport_count((target, sum(caps) - target), caps),
                             expected)
            self.assertTrue(prefix.called)
        caps, target = (2,) * 30, 20
        expected = plain_coefficients(caps, target)[target]
        with patch.object(transport, "_bounded_composition_dp",
                          side_effect=AssertionError("expected grouped inclusion-exclusion")), \
                patch.object(transport, "_bounded_composition_inclusion",
                             wraps=transport._bounded_composition_inclusion) as inclusion:
            self.assertEqual(transport.transport_count((target, sum(caps) - target), caps),
                             expected)
            self.assertTrue(inclusion.called)

    def test_huge_forced_and_formula_only_controls(self):
        huge = 10 ** 60
        with patch.object(transport, "_row_residuals",
                          side_effect=AssertionError("unexpected row enumeration")), \
                patch.object(transport, "_bounded_composition_dp",
                             side_effect=AssertionError("unexpected cap-sized array")):
            self.assertEqual(transport.transport_count((huge,), (1, huge - 1)), 1)
            self.assertEqual(transport.transport_count((huge, huge), (huge, huge)), huge + 1)
            self.assertEqual(transport.transport_count((huge, 2 * huge), (huge,) * 3),
                             comb(huge + 2, 2))
            self.assertEqual(transport.transport_count((huge, 2 * huge + 1),
                                                       (1, huge, 2 * huge)), 2 * huge + 1)
            self.assertEqual(transport.transport_count((huge, huge), (huge - 1, huge + 1)),
                             huge)

    def test_session_k_native_tables_and_quotients_against_original(self):
        original = original_transport_module()
        self.assertIsNot(original.segment_quotient_count, transport.segment_quotient_count)
        for m in (0, 1, 4):
            for stretch in (1, 2):
                margins = tuple(stretch * value for value in (2 + m, 2 + m, 1, 1))
                with self.subTest(m=m, stretch=stretch):
                    self.assertEqual(transport.transport_count(margins, margins),
                                     original.transport_count(margins, margins))
        for stretch in range(6):
            with self.subTest(quotient_stretch=stretch):
                self.assertEqual(transport.segment_quotient_count((1, 1), (1, 1), stretch),
                                 original.segment_quotient_count((1, 1), (1, 1), stretch))


class QuotientOptimizationTests(unittest.TestCase):
    def test_all_small_two_by_two_caps_against_cells(self):
        for rows in product(range(3), repeat=2):
            for columns in product(range(3), repeat=2):
                expected = literal_quotient(rows, columns)
                with self.subTest(rows=rows, columns=columns):
                    self.assertEqual(transport.segment_quotient_count(rows, columns), expected)
                    self.assertEqual(transport.segment_quotient_count(columns, rows), expected)

    def test_unequal_caps_zeros_permutations_and_dilation(self):
        for rows, columns, stretch in [((1, 2), (1, 1, 2), 1), ((1, 1, 2), (1, 2), 1),
                                       ((1, 1, 1), (1, 1, 1), 1),
                                       ((0, 1, 2), (1, 0, 1), 2),
                                       ((1, 1), (1, 1), 3)]:
            expected = literal_quotient(rows, columns, stretch)
            with self.subTest(rows=rows, columns=columns, stretch=stretch):
                self.assertEqual(transport.segment_quotient_count(rows, columns, stretch), expected)
                self.assertEqual(transport.segment_quotient_count(columns, rows, stretch), expected)
                self.assertEqual(transport.segment_quotient_count(rows[::-1], columns[::-1], stretch),
                                 expected)

    def test_final_row_closure_includes_column_slack_and_empty_residual(self):
        with patch.object(transport, "_row_residuals", wraps=transport._row_residuals) as transitions:
            self.assertEqual(transport.segment_quotient_count((2, 2), (1, 1)),
                             literal_quotient((2, 2), (1, 1)))
            # The smaller column box leaves two rows, only the first enumerated.
            self.assertEqual(transitions.call_count, 1)
        for central in (0, 1, 7):
            self.assertEqual(transport._star_quotient_count(central, ()), central + 1)

    def test_star_algorithms_against_independent_cells(self):
        for leaves in product(range(1, 4), repeat=3):
            for central in range(1, sum(leaves) + 2):
                expected = literal_quotient((central,), leaves)
                with self.subTest(central=central, leaves=leaves):
                    self.assertEqual(transport._star_quotient_dp(central, leaves), expected)
                    self.assertEqual(transport._star_quotient_numerator(central, leaves), expected)
                    self.assertEqual(transport.segment_quotient_count((central,), leaves), expected)
                    self.assertEqual(transport.segment_quotient_count(leaves, (central,)), expected)

    def test_mixed_star_uses_prefix_moments_when_expansion_is_larger(self):
        central, leaves = 20, tuple(range(1, 9))
        coefficients = plain_coefficients(leaves, central, linear=True)
        expected = sum((central - degree + 1) * coefficient
                       for degree, coefficient in enumerate(coefficients))
        with patch.object(transport, "_star_quotient_numerator",
                          side_effect=AssertionError("expected prefix/moment DP")), \
                patch.object(transport, "_star_quotient_dp",
                             wraps=transport._star_quotient_dp) as prefix, \
                patch.object(transport, "_row_residuals",
                             side_effect=AssertionError("a star needs no residual states")):
            self.assertEqual(transport.segment_quotient_count((central,), leaves), expected)
            self.assertTrue(prefix.called)

    def test_huge_star_formulas_precede_cap_sized_arrays(self):
        huge = 10 ** 60
        with patch.object(transport, "_row_residuals",
                          side_effect=AssertionError("unexpected row enumeration")), \
                patch.object(transport, "_star_quotient_dp",
                             side_effect=AssertionError("unexpected cap-sized array")):
            expected = (huge + 1) * (huge + 2) * (2 * huge + 3) // 6
            self.assertEqual(transport.segment_quotient_count((huge,), (huge,)), expected)
            leaves = (huge, 2 * huge, 3 * huge)
            expected = (5 * huge + 1) * prod(comb(cap + 2, 2) for cap in leaves)
            self.assertEqual(transport.segment_quotient_count((7 * huge,), leaves), expected)
            self.assertEqual(transport.segment_quotient_count((2,), (huge, huge + 1, huge + 2)),
                             literal_quotient((2,), (huge, huge + 1, huge + 2)))
            # Splitting the cap-one leaf gives this independent square-sum identity.
            expected = (huge + 1) ** 2 * (huge + 2)
            self.assertEqual(transport.segment_quotient_count((huge,), (1, huge)), expected)
            self.assertEqual(transport.segment_quotient_count((1, huge), (huge,)), expected)

    def test_reciprocity_against_strict_interior_cells(self):
        fixtures = [((0, 2), (2, 0, 3), 1), ((0, 2), (2, 0, 3), 2),
                    ((4,), (4, 4), 1), ((4, 4), (4, 4), 1),
                    ((2, 0, 1), (2, 1, 0), 4),
                    ((), (2, 3), 2), ((0, 0), (0,), 9)]
        for rows, columns, stretch in fixtures:
            p, q = sum(value > 0 for value in rows), sum(value > 0 for value in columns)
            expected = (-1) ** (p * q + p + q) * literal_interior(rows, columns, stretch)
            with self.subTest(rows=rows, columns=columns, stretch=stretch):
                self.assertEqual(transport.segment_quotient_evaluate(rows, columns, -stretch), expected)
                self.assertEqual(transport.segment_quotient_evaluate(columns, rows, -stretch), expected)


class PreservedContractTests(unittest.TestCase):
    def test_empty_zero_and_original_active_geometry(self):
        for rows, columns in [((), ()), ((), (0, 0)), ((0, 0), ())]:
            self.assertEqual(transport.transport_count(rows, columns), 1)
            self.assertEqual(transport.segment_quotient_count(rows, columns), 1)
        self.assertEqual(transport.segment_quotient_count((), (2, 0, 3), 2), 35)
        self.assertEqual(transport.segment_quotient_count((2, 3), (4, 5), 0), 1)
        geometry = transport.segment_quotient_geometry((0, 2), (2, 0, 3))
        self.assertEqual((geometry["degree"], geometry["dimension"], geometry["codegree"]),
                         (5, 5, 2))
        self.assertEqual(geometry["active_row_indices"], [1])
        self.assertEqual(geometry["active_column_indices"], [0, 2])
        self.assertEqual(transport.segment_quotient_evaluate((4,), (4, 4), -1), -4)

    def test_exact_python_integer_rejections(self):
        class IntegerSubclass(int):
            pass

        for bad in (True, False, IntegerSubclass(1), Fraction(1), Fraction(1, 2),
                    "1", 1.0, None, -1):
            for function in (transport.transport_count, transport.transport_to_lr,
                             transport.segment_quotient_count, transport.segment_quotient_geometry):
                for arguments in (([bad], [1]), ([1], [bad])):
                    with self.subTest(function=function.__name__, arguments=arguments), \
                            self.assertRaises(ValueError):
                        function(*arguments)
            with self.subTest(stretch=bad), self.assertRaises(ValueError):
                transport.segment_quotient_count((1,), (1,), bad)
            if bad != -1:
                with self.subTest(signed_stretch=bad), self.assertRaises(ValueError):
                    transport.segment_quotient_evaluate((1,), (1,), bad)

    def test_sequence_balance_and_lift_premise_limits(self):
        for bad in ("1", b"1", bytearray(b"1"), {1}, {0: 1}, None, 1, iter([1])):
            for function in (transport.transport_count, transport.transport_to_lr,
                             transport.segment_quotient_count):
                with self.subTest(function=function.__name__, bad=bad), self.assertRaises(ValueError):
                    function(bad, [1])
        for rows, columns in [((1,), (2,)), ((), (1,)), ((1,), ())]:
            with self.subTest(rows=rows, columns=columns), self.assertRaises(ValueError):
                transport.transport_count(rows, columns)
        with self.assertRaises(ValueError):
            transport.transport_to_lr((), ())
        lifted = transport.transport_to_lr((0, 2, 1, 0), (1, 0, 2, 0))
        self.assertEqual(lifted["metadata"]["transportation"]["row_margins"], [0, 2, 1, 0])
        self.assertEqual(lifted["metadata"]["transportation"]["column_margins"], [1, 0, 2, 0])
        self.assertIsNone(lifted["metadata"]["dimension"])
        self.assertIsNone(lifted["metadata"]["degree"])
        self.assertIsNotNone(transport.minkowski_obstruction((1, 3, 1, 1), (2, 2, 1, 1),
                                                           (1, 1, 0, 0), (1, 1, 0, 0)))


if __name__ == "__main__":
    unittest.main()
