"""Stored whole-family controls, exact evaluation, and strict input contracts."""

from fractions import Fraction
import unittest
from unittest.mock import patch

from slr_ehrhart import rank8_clipped as clipped


# Distinct prior positive-family formula, A004-RANK8-SIMPLEX-001, case R8M1S1.
# These 22 fixed coefficients were transcribed from its ordinary polynomial;
# the tests never read research artifacts or derive a control from the new data.
M_EQUALS_S = tuple(map(Fraction, (
    "1", "867149951/116396280", "902987891123/36664828200",
    "70854284616539/1466593128000", "176055244888643/2778808032000",
    "146408462472323/2470051584000", "121218288949553/2942267328000",
    "2639055969313/120708403200", "212503805287247/23538138624000",
    "36906195601757/12553673932800", "459776413387/603542016000",
    "84735102509/536481792000", "95098176137/3621252096000",
    "6861507071/1961511552000", "1093373119/2942267328000",
    "979419893/31384184832000", "8010829/3923023104000",
    "4022099/39520825344000", "1491407/400148356608000",
    "147299/1559552569344000", "899/608225502044160", "109/10137091700736000",
)))


def _prior_polynomial_at(t):
    result = Fraction(0)
    for coefficient in reversed(M_EQUALS_S):
        result = result * t + coefficient
    return result


class IntegerSubclass(int):
    pass


class Rank8ClippedTests(unittest.TestCase):
    def test_exact_boundary_and_partition_invariants(self):
        self.assertEqual(clipped.rank8_clipped_boundary(2, 3), (
            (97, 92, 72, 64, 49, 38, 18, 10),
            (54, 46, 38, 30, 26, 18, 10, 2),
            (50, 44, 38, 28, 24, 18, 12, 2),
        ))
        for M, S in ((1, 1), (1, 2), (2, 3), (10**30, 2 * 10**30)):
            with self.subTest(M=M, S=S):
                boundary = clipped.rank8_clipped_boundary(M, S)
                self.assertIs(type(boundary), tuple)
                for partition in boundary:
                    self.assertIs(type(partition), tuple)
                    self.assertEqual(len(partition), 8)
                    self.assertTrue(all(type(value) is int and value > 0 for value in partition))
                    self.assertEqual(partition, tuple(sorted(partition, reverse=True)))
                lam, mu, nu = boundary
                self.assertEqual(tuple(map(sum, boundary)), (220 * M, 112 * M, 108 * M))
                self.assertEqual(sum(lam), sum(mu) + sum(nu))
                self.assertTrue(all(inner <= outer for inner, outer in zip(mu, lam)))

    def test_stored_complete_counts(self):
        controls = (
            (1, 2, (1, 1678, 236305, 10771720, 250633155)),
            (2, 3, (1, 69083, 44649478)),
            (1, 1, (1, 280, 13910, 310856)),
        )
        for M, S, expected in controls:
            self.assertEqual(clipped.rank8_clipped_count(M, S), expected[1])
            for t, count in enumerate(expected):
                with self.subTest(M=M, S=S, t=t):
                    actual = clipped.rank8_clipped_count(M, S, t)
                    self.assertIs(type(actual), int)
                    self.assertEqual(actual, count)

    def test_origin_and_zero_dilation(self):
        self.assertEqual(clipped.rank8_clipped_boundary(0, 0), ((), (), ()))
        self.assertEqual(clipped.rank8_clipped_polynomial(0, 0), (Fraction(1),))
        self.assertIs(type(clipped.rank8_clipped_polynomial(0, 0)[0]), Fraction)
        for t in (0, 1, 10**50):
            self.assertEqual(clipped.rank8_clipped_count(0, 0, t), 1)
        self.assertEqual(clipped.rank8_clipped_count(10**50, 2 * 10**50, 0), 1)

    def test_prior_polynomial_and_huge_exact_inputs(self):
        self.assertEqual(clipped.rank8_clipped_polynomial(1, 1), M_EQUALS_S)
        M, t = 10**30 + 7, 10**20 + 3
        expected = _prior_polynomial_at(M * t)
        self.assertEqual(expected.denominator, 1)
        self.assertEqual(clipped.rank8_clipped_count(M, M, t), expected.numerator)
        self.assertEqual(clipped.rank8_clipped_polynomial(M, M),
                         tuple(value * M**degree for degree, value in enumerate(M_EQUALS_S)))

    def test_coefficients_are_ordinary_low_to_high_and_positive(self):
        for M, S, at_one, at_two in ((1, 1, 280, 13910), (1, 2, 1678, 236305),
                                     (2, 3, 69083, 44649478)):
            with self.subTest(M=M, S=S):
                coefficients = clipped.rank8_clipped_polynomial(M, S)
                self.assertIs(type(coefficients), tuple)
                self.assertEqual(len(coefficients), 22)
                self.assertEqual(coefficients[0], Fraction(1))
                self.assertTrue(all(type(value) is Fraction and value > 0 for value in coefficients))
                self.assertEqual(sum(coefficients), at_one)
                self.assertEqual(sum(value * 2**k for k, value in enumerate(coefficients)), at_two)

    def test_invalid_parameters_including_zero_dilation(self):
        bad_values = (True, False, 1.0, Fraction(1), IntegerSubclass(1), "1", b"1",
                      None, [], {}, 1 + 0j, -1)
        functions = (clipped.rank8_clipped_boundary, clipped.rank8_clipped_polynomial,
                     clipped.rank8_clipped_count)
        for bad in bad_values:
            for M, S in ((bad, 1), (1, bad)):
                for function in functions:
                    with self.subTest(function=function.__name__, M=M, S=S):
                        with self.assertRaises(ValueError):
                            function(M, S)
                with self.assertRaises(ValueError):
                    clipped.rank8_clipped_count(M, S, 0)
        for M, S in ((0, 1), (1, 0), (2, 1), (1, 3), (-1, -1)):
            for function in functions:
                with self.subTest(function=function.__name__, M=M, S=S):
                    with self.assertRaises(ValueError):
                        function(M, S)
            with self.assertRaises(ValueError):
                clipped.rank8_clipped_count(M, S, 0)

    def test_invalid_dilation_including_origin(self):
        for t in (-1, True, False, 1.0, Fraction(1), IntegerSubclass(1), "1", None, [], {}):
            for M, S in ((0, 0), (1, 1)):
                with self.subTest(M=M, S=S, t=t), self.assertRaises(ValueError):
                    clipped.rank8_clipped_count(M, S, t)

    def test_nonintegral_data_are_not_silently_truncated(self):
        with patch.object(clipped, "NUMERATOR_TERMS", ((0, 0, 1),)), \
                patch.object(clipped, "DENOMINATOR", 2):
            with self.assertRaises(ArithmeticError):
                clipped.rank8_clipped_count(1, 1)


if __name__ == "__main__":
    unittest.main()
