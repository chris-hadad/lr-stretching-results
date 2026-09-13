"""Complete chart identities, exact source controls and domain refusals."""
from fractions import Fraction
import unittest

from slr_ehrhart import rank6_split as split


BOX = ((9, 8, 6, 4, 2, 1), (5, 4, 3, 2, 1), (5, 4, 3, 2, 1))
INTERIOR = ((37, 33, 25, 15, 9, 5), (20, 16, 12, 8, 5, 1), (20, 16, 12, 8, 5, 1))
NEIGHBOR = ((8, 7, 6, 4, 3, 2), BOX[1], BOX[2])
SPLIT_FACE = ((9, 8, 7, 3, 2, 1), BOX[1], BOX[2])
EXPECTED = (
    ('1', '2843/840', '1087/224', '16951/4320', '723869/362880', '1927/2880',
     '2599/17280', '113/5040', '257/120960', '1/8640', '1/362880'),
    ('1', '4523/840', '40169/3360', '432823/30240', '3706841/362880', '1643/360',
     '11261/8640', '2389/10080', '3203/120960', '5/3024', '1/22680'),
)


class Rank6SplitTests(unittest.TestCase):
    def test_known_whole_polynomials_and_interior_count(self):
        for subject, expected, parameters, count in zip(
                (BOX, INTERIOR), EXPECTED,
                ({'S': 1, 'A': 0, 'B': 0}, {'S': 1, 'A': 1, 'B': 1}), (16, 49)):
            with self.subTest(subject=subject):
                coefficients = tuple(Fraction(value) for value in expected)
                self.assertEqual(split.rank6_split_parameters(*subject), parameters)
                actual = split.rank6_split_polynomial(*subject)
                self.assertEqual(actual, coefficients)
                self.assertTrue(all(type(value) is Fraction and value > 0 for value in actual))
                self.assertEqual(split.rank6_split_count(*subject), count)
                for t in (0, 2, 11):
                    self.assertEqual(split.rank6_split_count(*subject, t),
                                     sum(value * t**power for power, value in enumerate(coefficients)))

    def test_zero_simplex_dimension_drop_padding_and_stretch(self):
        self.assertEqual(split.rank6_split_parameters([], [], []), {'S': 0, 'A': 0, 'B': 0})
        self.assertEqual(split.rank6_split_polynomial([], [], []), (Fraction(1),))
        self.assertEqual(split.rank6_split_count([], [], [], 100), 1)
        # Root-supplied FE/025: both rank-three Horn children have count t+1.
        self.assertEqual(split.rank6_split_parameters(*SPLIT_FACE), {'S': 0, 'A': 1, 'B': 1})
        self.assertEqual(split.rank6_split_polynomial(*SPLIT_FACE),
                         (Fraction(1), Fraction(2), Fraction(1)))
        for t in (0, 1, 7):
            self.assertEqual(split.rank6_split_count(*SPLIT_FACE, t), (t + 1)**2)
        padded = [list(part) + [0] * 3 for part in BOX]
        doubled = [[2 * value for value in part] for part in BOX]
        self.assertEqual(split.rank6_split_count(*padded, 2), split.rank6_split_count(*BOX, 2))
        self.assertEqual(split.rank6_split_count(*doubled, 2), split.rank6_split_count(*BOX, 4))

    def test_exact_complete_row_and_label_identities(self):
        chart = split._CHART
        x = chart['row_counts']
        self.assertEqual(set(x), {(i, j) for i in range(6) for j in range(6)})
        trace = [1] * 6 + [-1] * 12 + [0] * 11
        simplex = ([1] * 3 + [0] * 3 + [-1] * 3 + [0] * 3
                   + [-1] * 3 + [0] * 3 + [1] * 9 + [0] * 2)
        for kind in ('row', 'label'):
            for index in range(6):
                if kind == 'row':
                    forms = [x[index, j] for j in range(6)]
                    expected = [int(k == index) - int(k == 6 + index) for k in range(29)]
                else:
                    forms = [x[i, index] for i in range(6)]
                    expected = [int(k == 12 + index) for k in range(29)]
                residual = [sum(form[k] for form in forms) - expected[k] for k in range(29)]
                with self.subTest(kind=kind, index=index):
                    self.assertEqual(residual, [residual[5] * a + residual[26] * b
                                                for a, b in zip(trace, simplex)])
        for i in range(6):
            for j in range(i + 1, 6):
                self.assertEqual(x[i, j], (0,) * 29)
        for i in range(3):
            for j in range(3):
                self.assertEqual(x[i + 3, j], tuple(int(k == 18 + 3 * i + j) for k in range(29)))
        self.assertEqual(x[2, 1], tuple(int(k == 27) for k in range(29)))
        self.assertEqual(x[4, 3], tuple(int(k == 28) for k in range(29)))

    def test_all_51_parent_minima_against_explicit_vertices(self):
        constraints, domain = split._CHART['constraints'], split._CHART['domain']
        expected_names = {f'nonnegative_{i}_{j}' for i in range(1, 7) for j in range(1, i + 1)}
        expected_names.update(f'{kind}_{i}_{j}' for kind in ('column', 'ballot')
                              for i in range(2, 7) for j in range(1, i))
        self.assertEqual(len(constraints), 51)
        self.assertEqual(len(domain), 51)
        self.assertEqual({name for name, _ in constraints}, expected_names)
        self.assertEqual([name for name, _ in constraints], [name for name, _ in domain])
        for subject in (BOX, INTERIOR, SPLIT_FACE):
            boundary = tuple(value for part in subject for value in part + (0,) * (6 - len(part)))
            p = split.rank6_split_parameters(*subject)
            vertices = []
            for k in range(9):
                cross = tuple(p['S'] * int(j == k) for j in range(9))
                for s in (0, p['A'] + sum(cross[2::3])):
                    for v in (0, p['B'] + sum(cross[:3])):
                        vertices.append(boundary + cross + (s, v))
            for (name, form), (_, minimum) in zip(constraints, domain):
                with self.subTest(subject=subject, constraint=name):
                    observed = min(sum(a * b for a, b in zip(form, point)) for point in vertices)
                    self.assertEqual(observed, sum(a * b for a, b in zip(minimum, boundary)))

    def test_full_domain_refusal_is_not_a_zero_count(self):
        for function in (split.rank6_split_parameters, split.rank6_split_polynomial,
                         split.rank6_split_count):
            with self.assertRaisesRegex(ValueError, 'nonnegative_2_1'):
                function(*NEIGHBOR)
        with self.assertRaisesRegex(ValueError, 'nonnegative_2_1'):
            split.rank6_split_count(*NEIGHBOR, 0)
        with self.assertRaisesRegex(ValueError, 'rank at most six'):
            split.rank6_split_count([1] * 7, [1] * 7, [], 0)

    def test_strict_partition_trace_and_dilation_inputs(self):
        functions = (split.rank6_split_parameters, split.rank6_split_polynomial,
                     split.rank6_split_count)
        for function in functions:
            for bad in (True, False, 1.0, Fraction(1), '1', None, -1):
                for slot in range(3):
                    subject = [[0], [0], [0]]
                    subject[slot] = [bad]
                    with self.subTest(function=function.__name__, slot=slot, bad=bad):
                        with self.assertRaises(ValueError):
                            function(*subject)
            for subject in (([1, 2], [2, 1], []), ([1], [], []),
                            ('0', [], []), (None, [], [])):
                with self.assertRaises(ValueError):
                    function(*subject)
        for bad in (-1, True, False, 1.0, Fraction(1), '1', None):
            with self.subTest(t=bad), self.assertRaises(ValueError):
                split.rank6_split_count(*BOX, bad)


if __name__ == '__main__':
    unittest.main()
