"""Root-budgeted tests only: independent formulas, API boundaries and CLI."""

from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
from io import StringIO
from itertools import permutations
from math import comb
import json
import sys
import unittest
from unittest.mock import patch

from slr_ehrhart import matrix_invariants
from slr_ehrhart.matrix_invariants import (
    MatrixCountLimitError, matrix_invariant_count, matrix_invariants_to_lr,
)


def rank_two_character(m, t):
    """Independent four-weight SL2 character extraction, with no table DP."""
    def w(x):
        return comb(x + m - 1, m - 1)
    u0 = sum(w(a) ** 2 * w(t - a) ** 2 for a in range(t + 1))
    u1 = sum(w(a) * w(a + 1) * w(t - 1 - a) * w(t - a) for a in range(t))
    u2 = sum(w(a) * w(a + 2) * w(t - 1 - a) ** 2 for a in range(t))
    return u0 - 2 * u1 + u2


def a06_polynomial(t):
    """Entire n=m=3 formula proved from the independent hive-cone model."""
    return comb(t + 10, 10) - comb(t + 9, 10) + comb(t + 8, 10)


class MatrixCountTests(unittest.TestCase):
    def test_elementary_cases_need_no_permutations_or_budgets(self):
        with patch.object(matrix_invariants, "permutations", side_effect=AssertionError("unexpected Weyl work")):
            cases = [(20, 5, 0, 1), (7, 1, 9, 1),
                     (1, 5, 6, comb(10, 4)), (20, 2, 30, comb(50, 20)),
                     (50, 4, 1, comb(53, 3)), (1, 3, 10 ** 30, comb(10 ** 30 + 2, 2))]
            for n, m, t, expected in cases:
                with self.subTest(n=n, m=m, t=t):
                    self.assertEqual(matrix_invariant_count(n, m, t, max_states=0, max_transitions=0), expected)

    def test_rank_two_independent_character_formula(self):
        for m in (3, 4, 5):
            for t in (2, 3, 4):
                with self.subTest(m=m, t=t):
                    self.assertEqual(matrix_invariant_count(2, m, t), rank_two_character(m, t))

    def test_rank_two_elementary_series_controls(self):
        for t in (2, 3, 5):
            self.assertEqual(matrix_invariant_count(2, 3, t), comb(t + 5, 5))
            self.assertEqual(matrix_invariant_count(2, 4, t), comb(t + 9, 9) + comb(t + 7, 9))

    def test_a06_entire_hive_formula(self):
        for t in (0, 1, 2, 3, 4, 6):
            with self.subTest(t=t):
                self.assertEqual(matrix_invariant_count(3, 3, t), a06_polynomial(t))

    def test_proved_swap_uses_smaller_weyl_rank_and_keeps_value(self):
        with patch.object(matrix_invariants, "permutations", wraps=permutations) as observed:
            self.assertEqual(matrix_invariant_count(4, 3, 3), 781)
            self.assertEqual(list(observed.call_args.args[0]), [0, 1, 2])
        self.assertEqual(matrix_invariant_count(5, 3, 3), a06_polynomial(5))

    def test_transition_ceiling_covers_profile_generation(self):
        with self.assertRaises(MatrixCountLimitError) as caught:
            matrix_invariant_count(3, 3, 3, max_transitions=1)
        error = caught.exception
        self.assertEqual((error.resource, error.limit), ("transitions", 1))
        self.assertEqual(error.statistics["transitions"], 1)
        self.assertEqual(error.statistics["permutations"], 1)
        self.assertEqual(error.statistics["states"], 0)
        self.assertFalse(hasattr(error, "value"))

    def test_transition_ceiling_covers_allocation_orbits(self):
        with self.assertRaises(MatrixCountLimitError) as caught:
            matrix_invariant_count(2, 3, 2, max_transitions=2)
        self.assertEqual(caught.exception.statistics["permutations"], 2)
        self.assertEqual(caught.exception.statistics["allocation_orbits"], 0)
        self.assertEqual(caught.exception.statistics["states"], 1)
        self.assertEqual(caught.exception.statistics["transitions"], 2)

    def test_orbit_budget_reports_represented_labeled_multiplicity(self):
        # Two Weyl permutations precede the first allocation orbit (0,2) of
        # equal caps (2,2). It represents the two labeled allocations (0,2)
        # and (2,0), not one labeled allocation.
        with self.assertRaises(MatrixCountLimitError) as caught:
            matrix_invariant_count(2, 3, 2, max_transitions=3)
        stats = caught.exception.statistics
        self.assertEqual(stats["permutations"], 2)
        self.assertEqual(stats["allocation_orbits"], 1)
        self.assertEqual(stats["represented_labeled_allocations"], 2)
        self.assertEqual(stats["transitions"], 3)
        self.assertEqual(stats["transitions"], stats["permutations"] + stats["allocation_orbits"]
                         + stats["residual_terms"])
        self.assertNotIn("allocations", stats)

    def test_state_limit_and_failed_call_do_not_poison_next_call(self):
        for limit in (0, 1):
            with self.subTest(limit=limit), self.assertRaises(MatrixCountLimitError) as caught:
                matrix_invariant_count(2, 3, 2, max_states=limit)
            self.assertEqual(caught.exception.resource, "states")
            self.assertEqual(caught.exception.statistics["states"], limit)
        self.assertEqual(matrix_invariant_count(2, 3, 2), 21)

    def test_exception_statistics_are_copied(self):
        statistics = {"states": 1}
        error = MatrixCountLimitError("states", 1, statistics)
        statistics["states"] = 99
        self.assertEqual(error.statistics, {"states": 1})

    def test_exact_integer_validation_precedes_elementary_branches(self):
        for bad in (True, False, Fraction(1), 1.0, "1", None, -1):
            for position in range(3):
                args = [1, 1, 0]
                args[position] = bad
                with self.subTest(args=args), self.assertRaises(ValueError):
                    matrix_invariant_count(*args)
        for args in ((0, 1, 0), (1, 0, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                matrix_invariant_count(*args)
        for name in ("max_states", "max_transitions"):
            for bad in (True, False, Fraction(1), 1.0, "1", -1):
                with self.subTest(name=name, value=bad), self.assertRaises(ValueError):
                    matrix_invariant_count(1, 1, 0, **{name: bad})


class AllocationScheduleTests(unittest.TestCase):
    @staticmethod
    def capture_caches(records):
        """Observe completed schedules during the call, without changing them."""
        def factory(*args, **kwargs):
            def decorate(function):
                cached = lru_cache(*args, **kwargs)(function)
                observed = {}
                records.append((cached, observed))

                def lookup(*key):
                    result = cached(*key)
                    observed[key] = result
                    return result

                return lookup
            return decorate
        return factory

    def test_schedule_aggregates_distinct_cap_groups_and_reuses_terms(self):
        records = []
        with patch.object(matrix_invariants, "lru_cache", side_effect=self.capture_caches(records)):
            self.assertEqual(matrix_invariant_count(3, 3, 3), 231)
        self.assertEqual(len(records), 1)
        cached, observed = records[0]
        self.assertEqual(cached.cache_parameters()["maxsize"], 256)
        self.assertGreater(cached.cache_info().hits, 0)
        # For caps (2,3,4) and total 2, allocations (0,0,2) and
        # (0,1,1) have one sorted residual, with weights 6 and 9.
        # Allocations (0,2,0) and (1,1,0) likewise combine as 6+9.
        self.assertEqual(dict(observed[((2, 3, 4), 2)]), {
            (2, 2, 3): 15, (1, 2, 4): 15, (1, 3, 3): 9, (3, 4): 6,
        })

    def test_schedule_keeps_orbit_multiplicity_and_m_is_per_call(self):
        records = []
        with patch.object(matrix_invariants, "lru_cache", side_effect=self.capture_caches(records)):
            self.assertEqual(matrix_invariant_count(2, 3, 2), 21)
            self.assertEqual(matrix_invariant_count(2, 4, 2), 56)
        self.assertEqual(len(records), 2)
        self.assertIsNot(records[0][0], records[1][0])
        self.assertEqual(dict(records[0][1][((2, 2), 2)]), {(2,): 12, (1, 1): 9})
        self.assertEqual(dict(records[1][1][((2, 2), 2)]), {(2,): 20, (1, 1): 16})

    def test_residual_consumption_has_its_own_budget_charge(self):
        for limit, consumed in ((4, 0), (5, 1)):
            with self.subTest(limit=limit), self.assertRaises(MatrixCountLimitError) as caught:
                matrix_invariant_count(2, 3, 2, max_transitions=limit)
            stats = caught.exception.statistics
            self.assertEqual(stats["permutations"], 2)
            self.assertEqual(stats["allocation_orbits"], 2)
            self.assertEqual(stats["represented_labeled_allocations"], 3)
            self.assertEqual(stats["residual_terms"], consumed)
            self.assertEqual(stats["schedule_cache_misses"], 1)
            self.assertEqual(stats["transitions"], limit)
            self.assertEqual(stats["transitions"], stats["permutations"]
                             + stats["allocation_orbits"] + stats["residual_terms"])


class CanonicalTableStateTests(unittest.TestCase):
    def test_transposition_length_and_lexical_tie_break(self):
        canonicalize = matrix_invariants._canonical_table_state
        fixtures = [((1, 1, 2), (2, 2)), ((1, 3), (2, 2)),
                    ((1, 2, 3), (1, 2, 3)), ((6,), (1, 2, 3)), ((), ())]
        for rows, columns in fixtures:
            with self.subTest(rows=rows, columns=columns):
                result = canonicalize(rows, columns)
                self.assertEqual(result, canonicalize(columns, rows))
                self.assertEqual(result, canonicalize(*result))
                self.assertGreaterEqual(len(result[0]), len(result[1]))
                if len(result[0]) == len(result[1]):
                    self.assertLessEqual(result[0], result[1])
        self.assertEqual(canonicalize((2, 2), (1, 1, 2)), ((1, 1, 2), (2, 2)))
        self.assertEqual(canonicalize((2, 2), (1, 3)), ((1, 3), (2, 2)))


class MatrixConstructorTests(unittest.TestCase):
    def test_n1_m3_explicit_entire_family(self):
        result = matrix_invariants_to_lr(1, 3)
        self.assertEqual([result[k] for k in ("lambda", "mu", "nu")],
                         [[12, 12, 10, 5, 5, 4], [8, 8, 4, 4], [8, 8, 4, 4]])
        self.assertEqual(result["metadata"]["entry_degree_per_stretch"], 1)
        self.assertEqual(result["metadata"]["source_bounds"], {"n_min": 1, "m_min": 2, "t_min": 0})

    def test_m2_contracted_edge_and_independent_partition_lists(self):
        result = matrix_invariants_to_lr(2, 2)
        self.assertEqual(result["lambda"], [3, 3, 2, 2, 1, 1])
        self.assertEqual(result["mu"], [2, 2, 1, 1])
        result["mu"][0] = 99
        self.assertEqual(result["nu"], [2, 2, 1, 1])

    def test_original_size_grade_and_partition_identity(self):
        for n, m in ((4, 3), (3, 4), (1, 5)):
            with self.subTest(n=n, m=m):
                result = matrix_invariants_to_lr(n, m)
                meta = result["metadata"]
                self.assertEqual((meta["matrix_size"], meta["matrix_count"]), (n, m))
                self.assertEqual(meta["entry_degree_per_stretch"], n)
                self.assertEqual(meta["ambient_rank"], 3 * (m - 1) * n)
                self.assertEqual(len(result["lambda"]), meta["ambient_rank"])
                self.assertEqual(sum(result["lambda"]), 6 * (m - 1) ** 3 * n)
                self.assertEqual(sum(result["lambda"]), sum(result["mu"]) + sum(result["nu"]))
                for key in ("lambda", "mu", "nu"):
                    self.assertEqual(result[key], sorted(result[key], reverse=True))
                self.assertIsNone(meta["dimension"])
                self.assertIsNone(meta["degree"])

    def test_constructor_domain_rejections(self):
        for args in ((0, 2), (1, 1), (True, 2), (1, True), (Fraction(1), 2), (1, "2"), (1, 2.0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                matrix_invariants_to_lr(*args)




if __name__ == "__main__":
    unittest.main()
