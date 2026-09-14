"""Scoped, independent whole-count and refusal controls; Python stdlib only."""

import unittest
from fractions import Fraction as F
from itertools import product
from unittest.mock import patch
from . import affine
from . import (
    affine_kostka_polynomial,
    capped_polynomial,
    flow_polynomial,
    jacobi_trudi_polynomial,
    one_overlap_polynomial,
    transport_polynomial,
    PolynomialResourceLimit,
)
from .literal import lr_count


def value(poly, t):
    return sum(c * t**i for i, c in enumerate(poly))


def table_count(rows, columns):
    states = {(0, 0): 1}
    a, b, c = tuple(rows) + (0,) * (3 - len(rows))
    for total in columns:
        nxt = {}
        for (x, y), count in states.items():
            for i in range(min(total, a - x) + 1):
                for j in range(min(total - i, b - y) + 1):
                    if total - i - j <= c:
                        k = x + i, y + j
                        nxt[k] = nxt.get(k, 0) + count
        states = nxt
    return states.get((a, b), 0)


def cap_count(weights, c, d, t):
    states = {(0, 0): 1}
    for w in weights:
        nxt = {}
        for (z, y), number in states.items():
            for a in range(min(w * t, c * t - z) + 1):
                for b in range(min(w * t - a, d * t - y) + 1):
                    k = z + a, y + b
                    nxt[k] = nxt.get(k, 0) + number
        states = nxt
    return sum(v for (z, y), v in states.items() if z == c * t)


class CompleteCoefficientTests(unittest.TestCase):
    def test_whole_overlap_and_independent_lr(self):
        p = one_overlap_polynomial(2, 2, 1, (2, 2), (4, 2, 2))["coefficients"]
        self.assertEqual(p, (F(1), F(5, 2), F(3, 2)))
        for t in range(1, 7):
            self.assertEqual(
                value(p, t),
                lr_count(
                    (7 * t, 6 * t, 4 * t, 2 * t),
                    (5 * t, 4 * t, 2 * t),
                    (4 * t, 2 * t, 2 * t),
                ),
            )
        wrong = tuple(
            x - y
            for x, y in zip(
                affine_kostka_polynomial((2, 2, 2, 2), (0, 0, 0, 0), (4, 2, 2)),
                affine_kostka_polynomial((3, 1, 2, 2), (0, 0, 0, 0), (4, 2, 2)),
            )
        )
        self.assertEqual(wrong, (F(0), F(3, 2), F(3, 2)))
        self.assertNotEqual(p, wrong)

    def test_full_jacobi_trudi(self):
        out = jacobi_trudi_polynomial((7, 6, 4, 2), (5, 4, 2), (4, 2, 2))
        self.assertEqual(out["coefficients"], (F(1), F(5, 2), F(3, 2)))
        self.assertEqual(len(out["signed_terms"]), 24)

    def test_all_coefficients_transport(self):
        for rows, cols in [
            ((1, 1, 2), (1, 1, 1, 1)),
            ((1, 2, 2), (1, 1, 1, 1, 1)),
            ((0, 2, 3), (1, 1, 1, 1, 1)),
            ((2, 2, 2), (0, 1, 1, 2, 2)),
        ]:
            p = transport_polynomial(rows, cols)
            D = max(0, (sum(x > 0 for x in rows) - 1) * (sum(x > 0 for x in cols) - 1))
            for t in range(1, D + 4):
                self.assertEqual(
                    value(p, t),
                    table_count(tuple(t * x for x in rows), tuple(t * x for x in cols)),
                )

    def test_capped_all_coefficients_and_walls(self):
        for w, c, d in [
            ((1, 1, 1, 1), 1, 1),
            ((1, 1, 2, 2), 3, 3),
            ((1, 2, 2, 3), 0, 3),
            ((1, 2, 2, 3), 3, 0),
            ((0, 1, 2, 3), 2, 2),
        ]:
            p = capped_polynomial(w, c, d)
            D = max(0, 2 * sum(x > 0 for x in w) - 1)
            for t in range(1, D + 4):
                self.assertEqual(value(p, t), cap_count(w, c, d, t))

    def test_empty_point_and_eventual_affine(self):
        self.assertEqual(transport_polynomial((0, 0, 0), (0, 0)), (F(1),))
        self.assertEqual(capped_polynomial((0, 0, 0, 0), 0, 0), (F(1),))
        self.assertEqual(affine_kostka_polynomial((1, 0), (-2, 2), (1,)), (F(1),))
        self.assertEqual(
            jacobi_trudi_polynomial((3,), (0,), (2, 1))["coefficients"], (F(0),)
        )

    def test_complete_affine_flow_ties(self):
        for m, slope, offset in [
            ((1, 2, 1), (1, 0, -1), (0, 0, 0)),
            ((1, 2, 1), (1, 0, -1), (1, 0, -1)),
            ((0, 2, 1), (2, -1, -1), (0, 0, 0)),
            ((1, 1, 0), (1, 0, -1), (0, 0, 0)),
        ]:
            p = flow_polynomial(m, slope, offset)
            for t in range(3, 10):
                A = slope[0] * t + offset[0]
                B = -slope[2] * t - offset[2]
                count = 0
                from math import comb

                def bundle(n, k):
                    return (
                        int(k == 0)
                        if n == 0
                        else (comb(k + n - 1, n - 1) if k >= 0 else 0)
                    )

                for z in range(max(0, min(A, B) + 1)):
                    count += bundle(m[0], A - z) * bundle(m[1], z) * bundle(m[2], B - z)
                self.assertEqual(value(p, t), count)

    def test_malformed_and_exact_caps(self):
        for call in [
            lambda: transport_polynomial((1, 1), (1,)),
            lambda: transport_polynomial((1, 1, 1, 1), (4,)),
            lambda: capped_polynomial((1, 2), 2, 2),
            lambda: capped_polynomial((1, 2), True, 1),
            lambda: transport_polynomial((1, 1), (2,), max_degree=True),
            lambda: flow_polynomial((1, 1, 1), (1, 0, 0), (0, 0, 0)),
        ]:
            with self.assertRaises(ValueError):
                call()
        for call in [
            lambda: transport_polynomial((1, 1, 1), (1, 1, 1), max_assignments=26),
            lambda: transport_polynomial((1, 1, 1), (1, 1, 1), max_degree=3),
            lambda: jacobi_trudi_polynomial(
                (7, 6, 4, 2), (5, 4, 2), (4, 2, 2), max_permutations=23
            ),
        ]:
            with self.assertRaises(PolynomialResourceLimit):
                call()
        self.assertEqual(
            transport_polynomial((1, 1, 1), (1, 1, 1), max_assignments=27),
            (F(1), F(9, 4), F(15, 8), F(3, 4), F(1, 8)),
        )

    def test_refusal_before_arithmetic(self):
        with patch.object(
            affine,
            "_affine_polynomial",
            side_effect=AssertionError("arithmetic entered"),
        ):
            with self.assertRaises(PolynomialResourceLimit):
                affine_kostka_polynomial(
                    (1,) * 8, (0,) * 8, (4, 3, 1), max_assignments=10
                )


if __name__ == "__main__":
    unittest.main()
