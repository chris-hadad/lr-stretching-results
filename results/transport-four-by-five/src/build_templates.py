#!/usr/bin/env python3
"""Derive every low jet from all 455 accepted original-offset Newton terms."""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement, product
import json
from math import factorial
from pathlib import Path
import sys
import time

from portable_io import check, output_directory, save, sha

DEN = factorial(12)
SITES = tuple((i, j, k) for i in range(13) for j in range(13 - i) for k in range(13 - i - j))
MONOMIALS = tuple(m for degree in range(4) for m in combinations_with_replacement(range(8), degree))
ROOT_MONOMIALS = tuple(m for degree in range(4) for m in combinations_with_replacement(range(3), degree))
RAYS = (
    ((1, 0, 0), (0, 0, 1), (1, 1, 1)),
    ((0, 0, 1), (0, 1, 1), (1, 1, 1)),
    ((1, 0, 0), (1, 1, 0), (1, 1, 1)),
    ((1, 1, 0), (0, 1, 0), (1, 2, 1)),
    ((0, 1, 1), (0, 1, 0), (1, 2, 1)),
    ((1, 1, 0), (1, 1, 1), (1, 2, 1)),
    ((0, 1, 1), (1, 1, 1), (1, 2, 1)),
)


def inverse(columns):
    rows = [[Fraction(columns[j][i]) for j in range(3)]
            + [Fraction(i == j) for j in range(3)] for i in range(3)]
    for c in range(3):
        pivot = next((i for i in range(c, 3) if rows[i][c]), None)
        if pivot is None:
            raise ValueError('Singular A3 chamber')
        rows[c], rows[pivot] = rows[pivot], rows[c]
        divisor = rows[c][c]
        rows[c] = [x / divisor for x in rows[c]]
        for i in range(3):
            if i != c:
                scale = rows[i][c]
                rows[i] = [a - scale * b for a, b in zip(rows[i], rows[c])]
    ans = tuple(tuple(row[3:]) for row in rows)
    if any(x.denominator != 1 for row in ans for x in row):
        raise ValueError('A3 inverse is not integral')
    ans = tuple(tuple(int(x) for x in row) for row in ans)
    matrix = tuple(zip(*columns))
    for left, right in ((matrix, ans), (ans, matrix)):
        if any(sum(left[i][k] * right[k][j] for k in range(3)) != int(i == j)
               for i in range(3) for j in range(3)):
            raise ValueError('A3 inverse product differs from identity')
    return ans


def product_value(monomial, values):
    result = 1
    for variable in monomial:
        result *= values[variable]
    return result


def evaluate_by_degree(polynomial, values):
    out = [0] * 4
    for monomial, coefficient in polynomial.items():
        out[len(monomial)] += coefficient * product_value(monomial, values)
    return out


def linear_substitute(polynomial, rows):
    """Literal products of linear forms; degree never changes in this step."""
    out = Counter()
    sparse = [tuple((i, value) for i, value in enumerate(row) if value) for row in rows]
    for monomial, coefficient in polynomial.items():
        if not coefficient:
            continue
        term = {(): coefficient}
        for variable in monomial:
            following = Counter()
            for key, value in term.items():
                for i, scale in sparse[variable]:
                    following[tuple(sorted(key + (i,)))] += value * scale
            term = following
        for key, value in term.items():
            out[key] += value
    return {k: v for k, v in out.items() if v}


def falling_at_offset(offset):
    """All 13 falling factorials, expanded after the original affine shift."""
    result = [[1, 0, 0, 0]]
    for step in range(12):
        old = result[-1]
        result.append([(offset - step) * old[d] + (old[d - 1] if d else 0) for d in range(4)])
    return result


def newton_jet(coefficients, offset, inv):
    if len(coefficients) != 455 or any(type(x) is not int for x in coefficients):
        raise ValueError('A full exact 455-entry Newton array is required')
    constants = [sum(a * b for a, b in zip(row, offset)) - 1 for row in inv]
    falls = [falling_at_offset(a) for a in constants]
    jet = {m: 0 for m in ROOT_MONOMIALS}
    exponents = {m: tuple(m.count(i) for i in range(3)) for m in ROOT_MONOMIALS}
    for (i, j, k), coefficient in zip(SITES, coefficients):
        if not coefficient:
            continue
        divisor = factorial(i) * factorial(j) * factorial(k)
        if DEN % divisor:
            raise ArithmeticError('Newton denominator does not divide 12 factorial')
        scaled = coefficient * (DEN // divisor)
        for m, (p, q, r) in exponents.items():
            jet[m] += scaled * falls[0][i][p] * falls[1][j][q] * falls[2][k][r]
    return linear_substitute(jet, inv)


def physical_slope(assignment):
    """Construct beta in four labeled margins, then cumulative simple roots."""
    row_forms = [[int(i == j) for j in range(8)] for i in range(3)]
    row_forms.append([-1, -1, -1, 0, 0, 0, 0, 1])
    col_forms = [[int(3 + i == j) for j in range(8)] for i in range(4)]
    col_forms.append([0, 0, 0, -1, -1, -1, -1, 1])
    beta = [[-x for x in row] for row in row_forms]
    for j, label in enumerate(assignment):
        beta[label] = [a + b for a, b in zip(beta[label], col_forms[j])]
    if any(sum(beta[i][j] for i in range(4)) for j in range(8)):
        raise ArithmeticError('Assignment netflow does not balance')
    return (tuple(beta[0]), tuple(a + b for a, b in zip(beta[0], beta[1])), tuple(-x for x in beta[3]))


def direct_simple(assignment, y):
    rows = list(y[:3]) + [y[7] - sum(y[:3])]
    columns = list(y[3:7]) + [y[7] - sum(y[3:7])]
    beta = [-r for r in rows]
    for j, i in enumerate(assignment):
        beta[i] += columns[j]
    return (beta[0], beta[0] + beta[1], -beta[3])


def build(inputs_path, expected, output):
    started = time.monotonic()
    output = output_directory(output)
    check(inputs_path, expected)
    inputs = json.loads(Path(inputs_path).read_bytes())
    if inputs['degree_bound'] != 12:raise ValueError('Atlas degree changed')
    atlas=inputs['newton_arrays'];count_binding=sha(inputs_path)
    import transport_math as am
    inverses = [inverse(rays) for rays in RAYS]
    jets = {}
    linear_vanishing_cases = 0
    controls = 0
    damaged_high = damaged_offset = None
    for key in sorted(atlas):
        occupation = tuple(map(int, key))
        if len(occupation) != 4 or sum(occupation) != 5:
            raise ValueError('Unexpected occupation')
        _, n1, n2, n3 = occupation
        offset = (-n1 - n2 - n3, -2 * (n2 + n3), -3 * n3)
        for chamber, coefficients in enumerate(atlas[key]):
            inv = inverses[chamber]
            jet = newton_jet(coefficients, offset, inv)
            jets[key, chamber] = jet
            # The inherited complete c1 certificate has exactly 22 occupations
            # with first class occupied and at least three occupied classes.
            # Its 154 chamber gradients must vanish, using every Newton term.
            if occupation[0] >= 1 and sum(v > 0 for v in occupation) >= 3:
                if any(jet.get((i,), 0) for i in range(3)):
                    raise ArithmeticError('Inherited complete linear vanishing certificate failed')
                linear_vanishing_cases += 1
            # Retain degree=12 in the accepted function: degree=3 would shorten
            # the Newton determining roster and is expressly forbidden here.
            for direction in ((2, -1, 3), (-2, 3, 1)):
                forms = tuple((sum(a * b for a, b in zip(row, offset)) - 1,
                               sum(a * b for a, b in zip(row, direction))) for row in inv)
                complete = am.contract_newton(coefficients, forms, degree=12)
                if evaluate_by_degree(jet, direction) != [complete.get(i, 0) for i in range(4)]:
                    raise ArithmeticError(f'Full original-offset identity failed: {key}/{chamber}')
                controls += 1
            if damaged_high is None:
                damaged = [v if sum(s) <= 3 else 0 for s, v in zip(SITES, coefficients)]
                if newton_jet(damaged, offset, inv) != jet:
                    damaged_high = [key, chamber]
            if damaged_offset is None and newton_jet(coefficients, (0, 0, 0), inv) != jet:
                damaged_offset = [key, chamber]
    if len(jets) != 392 or damaged_high is None or damaged_offset is None:
        raise ArithmeticError('Complete jet roster or meaningful corruption controls failed')
    if linear_vanishing_cases != 154:
        raise ArithmeticError('Incomplete inherited linear certificate roster')
    save(output / 'root-jets.json', {'schema': 'pro030-original-offset-jets/v1', 'denominator': DEN,
         'monomials': [list(m) for m in ROOT_MONOMIALS], 'count_binding': count_binding,
         'jets': [{'occupation': key, 'chamber': c,
                   'coefficients': [jets[key, c].get(m, 0) for m in ROOT_MONOMIALS]}
                  for key, c in sorted(jets)],
         'full_newton_positions': 178360, 'full_univariate_identity_controls': controls,
         'detected_high_degree_truncation': damaged_high, 'detected_offset_erasure': damaged_offset})
    maximum = 0
    direct_controls = 0
    destination = output / 'templates.txt'
    with destination.open('x') as stream:
        stream.write(f'LFTEMPLATES1 1024 7 165 {DEN}\n')
        for inv in inverses:
            stream.write(' '.join(str(v) for row in inv for v in row) + '\n')
        for identity, assignment in enumerate(product(range(4), repeat=5)):
            occupation = ''.join(str(assignment.count(i)) for i in range(4))
            sign = -1 if sum(assignment) % 2 else 1
            masks = [sum(1 << j for j, label in enumerate(assignment) if label <= i) for i in range(3)]
            stream.write(' '.join(map(str, [identity] + masks)) + '\n')
            slopes = physical_slope(assignment)
            for chamber in range(7):
                field = linear_substitute(jets[occupation, chamber], slopes)
                for y in ((11, 7, 3, 13, 8, 5, 2, 29), (0, 0, 0, 0, 0, 0, 0, 1)):
                    if evaluate_by_degree(field, y) != evaluate_by_degree(jets[occupation, chamber], direct_simple(assignment, y)):
                        raise ArithmeticError('Physical assignment substitution identity failed')
                    direct_controls += 1
                values = [sign * field.get(m, 0) for m in MONOMIALS]
                maximum = max(maximum, *(abs(v) for v in values))
                if maximum > 10 ** 12:
                    raise OverflowError('Template exceeds declared exact-int64 accumulation bound')
                stream.write(' '.join(map(str, values)) + '\n')
        stream.flush()
    save(output / 'TEMPLATES-COMPLETE.json', {'schema': 'pro030-independent-templates/v1',
         'status': 'PASS', 'count_binding': count_binding, 'arrays': 392, 'newton_positions': 178360,
         'root_jet_positions': 7840, 'physical_template_positions': 1024 * 7 * 165,
         'maximum_absolute_template_entry': maximum, 'full_univariate_controls': controls,
         'physical_substitution_controls': direct_controls, 'degree_after_offset': 3,
         'original_degree_retained': 12, 'templates_sha256': sha(destination),
         'root_jets_sha256': sha(output / 'root-jets.json'), 'elapsed_seconds': time.monotonic() - started,
         'scope': 'Complete local low-field templates; no chamber census or positivity yet'})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs')
    parser.add_argument('expected_sha256')
    parser.add_argument('output')
    args = parser.parse_args()
    build(args.inputs, args.expected_sha256, args.output)


if __name__ == '__main__':
    main()
