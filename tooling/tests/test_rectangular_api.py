"""Root-budgeted rectangular API tests; no Sage or external engine required."""

from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
from io import StringIO
from itertools import combinations_with_replacement, permutations
from math import comb, lcm
import json
import sys
import unittest
from unittest.mock import patch

from slr_ehrhart import matrix_invariants
from slr_ehrhart.matrix_invariants import (
    MatrixCountLimitError, matrix_invariant_count, rectangular_matrix_invariant_count,
)


def positive_root_denominator(rank):
    """Expand product_(i<j) (1 - x_i/x_j), without Weyl permutations."""
    terms = Counter({(0,) * rank: 1})
    for i in range(rank):
        for j in range(i + 1, rank):
            expanded = terms.copy()
            for exponent, coefficient in terms.items():
                shifted = list(exponent)
                shifted[i] += 1
                shifted[j] -= 1
                expanded[tuple(shifted)] -= coefficient
            terms = Counter({exponent: c for exponent, c in expanded.items() if c})
    return terms


def direct_monomial_character_count(p, q, m, t):
    """Enumerate degree-D monomials in all p*q*m independently labeled entries.

    Each monomial has coefficient one. Multiply its row/column weight by the
    two positive-root denominators and extract the determinant weight. This
    uses neither weighted transport tables nor permutation margin profiles.
    Only the explicitly small test cases below use this independent oracle.
    """
    degree = lcm(p, q) * t
    row_target, column_target = degree // p, degree // q
    rows = positive_root_denominator(p)
    columns = positive_root_denominator(q)
    variables = [(i, j) for _ in range(m) for i in range(p) for j in range(q)]
    answer = 0
    for monomial in combinations_with_replacement(range(len(variables)), degree):
        row_weight, column_weight = [0] * p, [0] * q
        for variable in monomial:
            i, j = variables[variable]
            row_weight[i] += 1
            column_weight[j] += 1
        row_shift = tuple(row_target - x for x in row_weight)
        column_shift = tuple(column_target - x for x in column_weight)
        answer += rows[row_shift] * columns[column_shift]
    return answer


class RectangularMatrixCountTests(unittest.TestCase):
    def test_small_rectangles_against_direct_labeled_monomials(self):
        cases = [(1, 2, 3, 1), (1, 2, 3, 2), (1, 3, 2, 1),
                 (1, 3, 3, 2), (2, 3, 2, 1), (2, 3, 3, 1),
                 (2, 4, 2, 1), (2, 4, 3, 1)]
        for p, q, m, t in cases:
            with self.subTest(p=p, q=q, m=m, t=t):
                self.assertEqual(rectangular_matrix_invariant_count(p, q, m, t),
                                 direct_monomial_character_count(p, q, m, t))

    def test_transposition_preserves_full_count(self):
        for p, q, m, t in ((1, 3, 4, 2), (2, 3, 2, 1), (2, 4, 3, 1)):
            with self.subTest(p=p, q=q, m=m, t=t):
                self.assertEqual(rectangular_matrix_invariant_count(p, q, m, t),
                                 rectangular_matrix_invariant_count(q, p, m, t))

    def test_square_equality_including_swap_and_elementary_values(self):
        for n, m, t in ((1, 5, 6), (7, 1, 9), (20, 2, 30),
                        (50, 4, 1), (2, 3, 2), (4, 3, 3), (3, 3, 0)):
            with self.subTest(n=n, m=m, t=t):
                self.assertEqual(rectangular_matrix_invariant_count(n, n, m, t),
                                 matrix_invariant_count(n, m, t))
        for limits in ({"max_states": 0}, {"max_transitions": 3}):
            with self.assertRaises(MatrixCountLimitError) as square:
                matrix_invariant_count(2, 3, 2, **limits)
            with self.assertRaises(MatrixCountLimitError) as rectangular:
                rectangular_matrix_invariant_count(2, 2, 3, 2, **limits)
            self.assertEqual(rectangular.exception.statistics, square.exception.statistics)
            self.assertEqual(rectangular.exception.resource, square.exception.resource)
            self.assertEqual(rectangular.exception.limit, square.exception.limit)

    def test_zero_grade_and_single_matrix_use_no_weyl_work(self):
        with patch.object(matrix_invariants, "permutations", side_effect=AssertionError("unexpected Weyl work")):
            for p, q, m, t, expected in ((4, 5, 7, 0, 1), (5, 4, 1, 0, 1),
                                         (4, 5, 1, 9, 0), (5, 4, 1, 9, 0),
                                         (1, 3, 1, 2, 0), (3, 3, 1, 9, 1),
                                         (1, 1, 4, 3, comb(6, 3))):
                with self.subTest(p=p, q=q, m=m, t=t):
                    self.assertEqual(rectangular_matrix_invariant_count(
                        p, q, m, t, max_states=0, max_transitions=0,
                    ), expected)
        self.assertEqual(direct_monomial_character_count(2, 3, 1, 1), 0)
        self.assertEqual(direct_monomial_character_count(3, 2, 1, 1), 0)

    def test_divisible_positive_grade_can_still_be_empty(self):
        # Fewer than q vectors in C^q have no positive-degree SL_q invariant.
        for p, q, m in ((1, 3, 2), (3, 1, 2), (1, 4, 3)):
            with self.subTest(p=p, q=q, m=m):
                self.assertEqual(rectangular_matrix_invariant_count(p, q, m, 1), 0)
        # The three maximal minors of a 2-by-3 vector array are independent.
        self.assertEqual(rectangular_matrix_invariant_count(1, 2, 3, 2), 6)

    def test_rectangular_profiles_keep_both_original_ranks_at_t_one(self):
        with patch.object(matrix_invariants, "permutations", wraps=permutations) as observed:
            rectangular_matrix_invariant_count(2, 3, 2, 1)
        self.assertEqual([list(call.args[0]) for call in observed.call_args_list],
                         [[0, 1], [0, 1, 2]])

    def test_exact_integer_domain_precedes_zero_grade_and_elementary_paths(self):
        class IntSubclass(int):
            pass

        for bad in (True, False, Fraction(1), Decimal(1), 1.0, "1", None, -1, IntSubclass(1)):
            for position in range(4):
                args = [1, 2, 1, 0]
                args[position] = bad
                with self.subTest(args=args), self.assertRaises(ValueError):
                    rectangular_matrix_invariant_count(*args)
        for position in range(3):
            args = [1, 2, 1, 0]
            args[position] = 0
            with self.subTest(args=args), self.assertRaises(ValueError):
                rectangular_matrix_invariant_count(*args)
        for name in ("max_states", "max_transitions"):
            for bad in (True, False, Fraction(1), Decimal(1), 1.0, "1", -1, IntSubclass(1)):
                with self.subTest(name=name, value=bad), self.assertRaises(ValueError):
                    rectangular_matrix_invariant_count(1, 2, 1, 0, **{name: bad})
        self.assertEqual(rectangular_matrix_invariant_count(2, 3, 1, 0,
                                                           max_states=None, max_transitions=None), 1)

    def test_limits_charge_both_weyl_groups_and_return_no_partial_value(self):
        for limit in (0, 2, 7):
            with self.subTest(limit=limit), self.assertRaises(MatrixCountLimitError) as caught:
                rectangular_matrix_invariant_count(2, 3, 2, 1, max_transitions=limit)
            error = caught.exception
            self.assertEqual((error.resource, error.limit), ("transitions", limit))
            self.assertEqual(error.statistics["transitions"], limit)
            self.assertEqual(error.statistics["permutations"], limit)
            self.assertEqual(error.statistics["states"], 0)
            self.assertEqual(error.statistics["margin_profiles"], 0 if limit == 0 else 2)
            self.assertFalse(hasattr(error, "value"))
        for limit in (0, 1):
            with self.subTest(limit=limit), self.assertRaises(MatrixCountLimitError) as caught:
                rectangular_matrix_invariant_count(2, 3, 2, 1, max_states=limit)
            stats = caught.exception.statistics
            self.assertEqual(caught.exception.resource, "states")
            self.assertEqual(stats["states"], limit)
            self.assertEqual(stats["permutations"], 8)
            self.assertEqual(stats["transitions"], stats["permutations"]
                             + stats["allocation_orbits"] + stats["residual_terms"])
        self.assertEqual(rectangular_matrix_invariant_count(2, 3, 2, 1),
                         direct_monomial_character_count(2, 3, 2, 1))

    def test_rectangular_schedule_orbits_and_consumption_keep_separate_charges(self):
        # The first state has rows (2,2,2), columns (3,3). Its total-2
        # allocations have orbits (0,2), multiplicity 2, and (1,1), multiplicity 1.
        for limit, orbits, represented, consumed in ((8, 0, 0, 0), (9, 1, 2, 0),
                                                    (10, 2, 3, 0), (11, 2, 3, 1)):
            with self.subTest(limit=limit), self.assertRaises(MatrixCountLimitError) as caught:
                rectangular_matrix_invariant_count(2, 3, 2, 1, max_transitions=limit)
            stats = caught.exception.statistics
            self.assertEqual(stats["permutations"], 8)
            self.assertEqual(stats["allocation_orbits"], orbits)
            self.assertEqual(stats["represented_labeled_allocations"], represented)
            self.assertEqual(stats["residual_terms"], consumed)
            self.assertEqual(stats["transitions"], limit)
            self.assertEqual(stats["transitions"], stats["permutations"]
                             + stats["allocation_orbits"] + stats["residual_terms"])

    def test_schedule_cache_is_per_call_and_failure_does_not_install_a_partial_schedule(self):
        caches = []

        def observe_lru(*args, **kwargs):
            def decorate(function):
                cached = lru_cache(*args, **kwargs)(function)
                caches.append(cached)
                return cached
            return decorate

        with patch.object(matrix_invariants, "lru_cache", side_effect=observe_lru):
            with self.assertRaises(MatrixCountLimitError):
                rectangular_matrix_invariant_count(2, 3, 2, 1, max_transitions=9)
            self.assertEqual(caches[0].cache_info().currsize, 0)
            for p, q, m, t in ((2, 3, 2, 1), (2, 3, 3, 1), (3, 2, 2, 1)):
                self.assertEqual(rectangular_matrix_invariant_count(p, q, m, t),
                                 direct_monomial_character_count(p, q, m, t))
        self.assertEqual(len(caches), 4)
        self.assertEqual(len({id(cached) for cached in caches}), 4)
        for cached in caches:
            self.assertEqual(cached.cache_parameters()["maxsize"], 256)




if __name__ == "__main__":
    unittest.main()
