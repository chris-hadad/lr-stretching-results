"""Independent exact A78 high-star arithmetic, reconstructed from mathematical prose.

The primary complete P/E arrays use the first-row identity (15). No producer,
provider program, count engine, or symbolic algebra package is imported.
Finite panels corroborate; they do not supply an unbounded quantifier.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import time

TARGET = Path(__file__).resolve().parents[1]
METHOD = Path(__file__).resolve().parent
BASE_JSON = 'data/HIGH-STAR-BASES.json'
BASE_SHA = 'fec3fce068efd7dd45596ba683e5528e54b5d413e64a94a3339aac2f3c961cdd'
BASE_TEXT = 'proofs/pro053/U10-BASES.md'


def exact(value):
    if type(value) is int or isinstance(value, Q):
        return Q(value)
    raise TypeError('Only exact integers and rational numbers are accepted')


class P:
    """Sparse exact polynomial; dimensions have no implicit scientific meaning."""
    def __init__(self, values=0, dim=2):
        self.dim = dim
        if isinstance(values, dict):
            self.c = {tuple(k): exact(v) for k, v in values.items() if v}
            assert all(len(k) == dim and all(type(i) is int and i >= 0 for i in k) for k in self.c)
        else:
            v = exact(values)
            self.c = {(0,) * dim: v} if v else {}

    def coerce(self, other):
        if isinstance(other, P):
            assert self.dim == other.dim
            return other
        return P(other, self.dim)

    def __add__(self, other):
        other = self.coerce(other)
        out = self.c.copy()
        for k, v in other.c.items():
            out[k] = out.get(k, Q(0)) + v
        return P(out, self.dim)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()}, self.dim)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        if len(other.c) == 1 and (0,) * self.dim in other.c:
            scale = other.c[(0,) * self.dim]
            return P({k: v * scale for k, v in self.c.items()}, self.dim)
        if len(self.c) == 1 and (0,) * self.dim in self.c:
            return other * self.c[(0,) * self.dim]
        out = {}
        for ka, va in self.c.items():
            for kb, vb in other.c.items():
                k = tuple(a + b for a, b in zip(ka, kb))
                out[k] = out.get(k, Q(0)) + va * vb
        return P(out, self.dim)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (1 / exact(other))

    def __pow__(self, power):
        assert type(power) is int and power >= 0
        out = P(1, self.dim)
        base = self
        while power:
            if power % 2:
                out = out * base
            base = base * base
            power //= 2
        return out

    def __eq__(self, other):
        return self.c == self.coerce(other).c

    def degree(self):
        return max((sum(k) for k in self.c), default=-1)

    def evaluate(self, *values):
        assert len(values) == self.dim
        values = tuple(exact(v) for v in values)
        return sum((c * math.prod(v ** e for v, e in zip(values, key)) for key, c in self.c.items()), Q(0))

    def compose(self, *values):
        assert len(values) == self.dim and values
        out = P(0, values[0].dim)
        powers = [{0: P(1, v.dim)} for v in values]
        for key, c in self.c.items():
            term = P(c, values[0].dim)
            for i, e in enumerate(key):
                if e not in powers[i]:
                    powers[i][e] = values[i] ** e
                term = term * powers[i][e]
            out = out + term
        return out


def variable(index, dim=2):
    key = [0] * dim
    key[index] = 1
    return P({tuple(key): 1}, dim)


X, Z = variable(0), variable(1)


def binomial(top, bottom):
    assert type(bottom) is int and bottom >= 0
    result = P(1, top.dim)
    for i in range(bottom):
        result = result * (top - i) / (i + 1)
    return result


@lru_cache(None)
def affine_binomial(ax, az, constant, bottom):
    return binomial(ax * X + az * Z + constant, bottom)


def a(m, value=X):
    return binomial(value + m, m)


def d(m, value=X):
    return P(1, value.dim) if m == 0 else binomial(value + m - 1, m)


@lru_cache(None)
def ax(m):
    return a(m)


@lru_cache(None)
def dx(m):
    return d(m)


def t(n):
    return ax(n) * (1 + Q(n, n + 1) * X)


def kernel(n):
    return ax(n) ** 2 - (n + 1) * dx(2 * n)


@lru_cache(None)
def primary(n, central_shift=0):
    """Whole first-row identity (15), with a named strict-shift control."""
    result = ax(n) * affine_binomial(3, 2, n, n)
    for q in range(n + 1):
        first = affine_binomial(1, 0, n, n + q)
        result = result - first * affine_binomial(2, 2, n - 1 + central_shift, n - q)
        result = result - n * first * affine_binomial(1, 1, n - 1, n - q)
        result = result + n * (q + 1) * first * affine_binomial(0, 1, n - 2, n - q)
    return result


def singleton(n, height, omit_terminal=False):
    result = sum((d(l, height) * dx(2 * n - l) for l in range(n)), P(0))
    return result if omit_terminal else result + d(n, height) * ax(n)


def pair_low(n, height):
    return (X + 1) * binomial(height + 2 * n - 3, 2 * n - 1) - (n - 1) * binomial(height + 2 * n - 3, 2 * n)


def pair_tail(n, height, cutoff_shift=0):
    return sum(((l + 1) * binomial(X + n + cutoff_shift, n - 2 - l) * binomial(height - X + n - 2, n + 2 + l) for l in range(n - 1)), P(0))


def correction(n):
    h = X + Z
    return singleton(n, h) - pair_low(n, h) - pair_tail(n, h)


def reconstructed(n, omit_tail=False, omit_terminal=False, cutoff_shift=0):
    h = X + Z
    free = ax(n) * a(n, X + 2 * h) - singleton(n, 2 * h, omit_terminal)
    pair = pair_low(n, h)
    if not omit_tail:
        pair = pair + pair_tail(n, h, cutoff_shift)
    return free - n * (singleton(n, h, omit_terminal) - pair)


def c_complete(n, k):
    if k == 1:
        return t(n)
    L = n + k
    return (ax(n) * dx(k)
            + sum((dx(n + k - p) * dx(p) for p in range(2, k)), P(0))
            + dx(L - 2) * ((L * L - 2 * k) + (L * L - 3 * L + 3 * k) * X + n * X ** 2) / (L * (L - 1)))


def b(n, r):
    result = X / (n + r)
    for i in range(n + 1, n + r):
        result = result * (1 + X / i)
    return result


def c_quotient(n, k):
    if k == 2:
        return dx(2) + X * (n * X + n + 4) / ((n + 1) * (n + 2))
    L = n + k
    product = X
    for i in range(n + 1, n + k - 2):
        product = product * (1 + X / i)
    denominator = L * (L - 1) * (L - 2)
    bracket = Q(L * L - 2 * k, denominator) + Q(L * L - 3 * L + 3 * k, denominator) * X + Q(n, denominator) * X ** 2
    return dx(k) + sum((b(n, k - p) * dx(p) for p in range(2, k)), P(0)) + product * bracket


def all_rows(poly, degree):
    assert poly.degree() <= degree
    return [[str(poly.c.get((i, j), Q(0))) for j in range(degree + 1 - i)] for i in range(degree + 1)]


def full_sites(poly, degree):
    return [{'x_power': i, 'z_power': j, 'coefficient': str(poly.c.get((i, j), Q(0)))}
            for i in range(degree + 1) for j in range(degree + 1 - i)]


def read_rational(value):
    if type(value) is not str or not re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?', value):
        raise ValueError('Not a canonical exact rational string')
    result = Q(value)
    if str(result) != value:
        raise ValueError('Noncanonical rational string')
    return result


def validate_record(record, expected_n):
    if record['n'] != expected_n or record['total_degree'] != 2 * expected_n or record['variables'] != ['x', 'z']:
        raise ValueError('Changed index, degree or variable order')
    expected_keys = [(i, j) for i in range(2 * expected_n + 1) for j in range(2 * expected_n + 1 - i)]
    sites = record['E_sites']
    actual_keys = [(row['x_power'], row['z_power']) for row in sites]
    if actual_keys != expected_keys:
        raise ValueError('Missing, duplicate, shifted or unordered coefficient site')
    values = [read_rational(row['coefficient']) for row in sites]
    expected = primary(expected_n) - kernel(expected_n)
    if values != [expected.c.get(key, Q(0)) for key in expected_keys]:
        raise ValueError('Changed complete coefficient array')
    return True


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


class Audit:
    def __init__(self):
        self.counts = Counter()
        self.controls = []
        self.failures = []

    def check(self, condition, family, detail):
        self.counts[family] += 1
        if not condition:
            self.failures.append({'family': family, 'detail': detail})
            raise AssertionError((family, detail))

    def equal(self, left, right, family, detail):
        self.check(left == right, family, detail)

    def nonnegative(self, poly, family, detail):
        negatives = {str(key): str(value) for key, value in poly.c.items() if value < 0}
        self.check(not negatives, family, {'case': detail, 'negative': negatives})

    def detects(self, condition, kind, detail):
        self.check(condition, 'failure_controls', {'kind': kind, 'detail': detail})
        self.controls.append({'kind': kind, 'detail': detail, 'detected': True})

    def refusal(self, record, n, kind):
        try:
            validate_record(record, n)
        except (ValueError, KeyError, TypeError):
            self.detects(True, kind, {'n': n})
        else:
            self.detects(False, kind, {'n': n})


def source_bases(audit):
    audit.equal(digest(TARGET / BASE_JSON), BASE_SHA, 'source_authentication', 'fixed-base JSON')
    payload = json.loads((TARGET / BASE_JSON).read_text())
    # Mathematical arrays are located by family labels and parsed as data only.
    return payload


def compare_source_text(audit, primary_arrays):
    body = (TARGET / BASE_TEXT).read_text()
    for n in range(3, 7):
        block = body.split('## HIGH-E-' + str(n) + '\n', 1)[1].split('\n## ', 1)[0]
        degree = int(re.search(r'Total degree bound: (\d+)\.', block).group(1))
        source = []
        indices = []
        for match in re.finditer(r'x\^(\d+): denominator (\d+); numerators (\[[^\n]+\])', block):
            i, denominator = int(match.group(1)), int(match.group(2))
            indices.append(i)
            source.append([str(Q(v, denominator)) for v in json.loads(match.group(3))])
        audit.equal(indices, list(range(degree + 1)), 'source_fixed_bases', {'n': n, 'check': 'complete row order'})
        audit.equal(degree, 2 * n, 'source_fixed_bases', {'n': n, 'check': 'prior degree'})
        audit.equal(source, primary_arrays[n]['E_rows'], 'source_fixed_bases', {'n': n, 'check': 'all coefficients including zeros'})


def symbolic_checks(audit):
    # The variables here are independent indices L,k, not x,z.
    L, k = X, Z
    for name, numerator in [('f0', L ** 2 - 2 * k), ('f1', L ** 2 - 3 * L + 3 * k), ('f2', L - k)]:
        audit.nonnegative(numerator.compose(2 * (X + 3) + Z, X + 3), 'uniform_positive_quotient_numerators', name)
    audit.equal((L ** 2 - 2 * k) * (L + 1) - ((L + 1) ** 2 - 2 * k) * (L - 2), L ** 2 + 3 * L + 2 - 6 * k, 'uniform_scalar_identities', 'f0 forward numerator')
    audit.equal((L ** 2 - 3 * L + 3 * k) * (L + 1) - ((L + 1) ** 2 - 3 * (L + 1) + 3 * k) * (L - 2), L ** 2 - 3 * L + 9 * k - 4, 'uniform_scalar_identities', 'f1 forward numerator')
    audit.equal((L - k) * (L + 1) - (L + 1 - k) * (L - 2), 2 * L - 3 * k + 2, 'uniform_scalar_identities', 'f2 forward numerator')
    for index, numerator in enumerate([L ** 2 + 3 * L + 2 - 6 * k, L ** 2 - 3 * L + 9 * k - 4, 2 * L - 3 * k + 2]):
        audit.nonnegative(numerator.compose(2 * (X + 3) + Z, X + 3), 'uniform_positive_index_substitution', {'index': index, 'k': 'r+3', 'L': '2k+s'})
    n = X
    audit.equal((n + 4) * (n + 3) - (n + 5) * (n + 1), n + 7, 'uniform_scalar_identities', 'k2 constant forward numerator')
    audit.equal(n * (n + 3) - (n + 1) ** 2, n - 1, 'uniform_scalar_identities', 'k2 linear forward numerator')
    audit.equal(n * (n - 1) - (n + 1), n ** 2 - 2 * n - 1, 'uniform_scalar_identities', 'diagonal slope inequality k>=3 numerator')
    audit.nonnegative((n ** 2 - 2 * n - 1).compose(X + 3, Z), 'uniform_positive_index_substitution', 'diagonal slope numerator')
    audit.equal(2 * (2 * n - 1) - (n + 1), 3 * n - 3, 'uniform_scalar_identities', 'diagonal adverse-pair scalar slope numerator')
    audit.nonnegative((3 * n - 3).compose(X + 3, Z), 'uniform_positive_index_substitution', 'diagonal adverse-pair scalar slope')
    # Exact common-denominator identity for the subset-based dilation payment.
    m, degree, exponential = variable(0, 3), variable(1, 3), variable(2, 3)
    audit.equal(-(m + degree + 1) * exponential + m * exponential + (degree + 1), -(degree + 1) * (exponential - 1), 'uniform_scalar_identities', 'F forward identity after exact a/d recursions')
    numerator = (exponential - 1) * (m - degree) * m + (exponential - 2 * m - 3) * degree * (m - 1)
    audit.equal(numerator, (exponential - 1 - 2 * degree) * m ** 2 - degree * (exponential - 3), 'uniform_scalar_identities', 'dilation coefficient lower-bound numerator')
    audit.equal((2 * exponential - 2 * (degree + 1) - 3) - (exponential - 2 * degree - 3), exponential - 2, 'uniform_scalar_identities', 'exponential inequality induction increment')
    audit.equal(2 * (n + 1) - n, n + 2, 'uniform_scalar_identities', 'dilation linear forward numerator')
    audit.equal(n ** 2 - (n + 1), n ** 2 - n - 1, 'uniform_scalar_identities', 'final reserve slope common numerator')
    audit.nonnegative((n ** 2 - n - 1).compose(X + 2, Z), 'uniform_positive_index_substitution', 'final reserve slope n>=2')
    # Positive quotient slopes decrease after every forward index step.
    audit.equal((n + Z + 1) - (n + Z), P(1), 'uniform_scalar_identities', '1/(n+r) forward numerator')


def finite_triangle_checks(audit):
    for x in range(5):
        for r in range(1, 6):
            for s in range(1, 6):
                actual = sum(d(r).evaluate(I, 0) * d(s).evaluate(J, 0) for I in range(x + 1) for J in range(x + 1) if I + J >= x)
                expected = (d(r + 1) * d(s + 1) - d(r + s + 2, X - 2)).evaluate(x, 0)
                audit.equal(actual, expected, 'triangle_positive_indices', {'x': x, 'r': r, 's': s})
            actual = sum(d(r).evaluate(I, 0) for I in range(x + 1) for J in range(x + 1) if I + J >= x)
            expected = (2 * d(r + 1) + (r + 1) * d(r + 2, X - 1)).evaluate(x, 0)
            audit.equal(actual, expected, 'triangle_zero_index', {'x': x, 'r': r})
    for n in range(2, 13):
        for x in range(5):
            actual = sum((I + 1) * a(n - 1).evaluate(I, 0) for I in range(x + 1))
            audit.equal(actual, t(n).evaluate(x, 0), 'triangle_terminal_zero_index', {'n': n, 'x': x})
            for s in range(1, n):
                actual = sum(a(n - 1).evaluate(I, 0) * d(s).evaluate(J, 0) for I in range(x + 1) for J in range(x + 1) if I + J >= x)
                expected = (a(n) * d(s + 1) - d(n + s + 1, X - 1)).evaluate(x, 0)
                audit.equal(actual, expected, 'triangle_terminal_positive_indices', {'n': n, 'x': x, 's': s})


def proof_panels(audit):
    h = X + Z
    for n in range(2, 13):
        audit.equal(ax(n) * dx(1) - dx(n + 1) + ax(n), t(n), 'F_terminal', {'n': n})
        W = correction(n)
        expanded = sum((d(n - k, Z) * c_complete(n, k) for k in range(1, n + 1)), P(0))
        audit.equal(W, expanded, 'full_high_contraction', {'n': n})
        audit.equal(c_complete(n, 1), t(n), 'C_terminal', {'n': n})
        for k in range(2, n + 1):
            C = c_complete(n, k)
            cq = c_quotient(n, k)
            audit.equal(ax(n) * cq, C, 'positive_quotient_identity', {'n': n, 'k': k})
            audit.nonnegative(cq, 'positive_quotient_coefficients', {'n': n, 'k': k})
            audit.nonnegative(c_quotient(k, k) - cq, 'positive_quotient_diagonal_decrease', {'n': n, 'k': k})
            audit.nonnegative(cq - c_quotient(n + 1, k), 'positive_quotient_forward_decrease', {'n': n, 'k': k})
            audit.nonnegative(2 * t(n) * dx(k - 1) - C, 'factor_two_C_bound', {'n': n, 'k': k})
            if k == 2:
                audit.nonnegative(t(n) * dx(1) - C, 'k2_factor_one_bound', {'n': n})
            for r in range(1, k):
                audit.equal(ax(n) * b(n, r), dx(n + r), 'b_exact_quotient', {'n': n, 'r': r})
                audit.nonnegative(b(n, r) - b(n + 1, r), 'b_forward_decrease', {'n': n, 'r': r})
        audit.equal(c_quotient(2, 2), (1 + Q(2, 3) * X) * dx(1), 'k2_exact_base', {'n': n})
        F = [None] + [ax(n) * ax(k) - dx(n + k) for k in range(1, n + 1)]
        for k in range(1, n + 1):
            audit.nonnegative(ax(n) * ax(k) - (1 + X) * ax(n + k - 1), 'sorted_factor_F_payment', {'n': n, 'k': k})
            audit.nonnegative(F[k] - t(n), 'F_lower_terminal', {'n': n, 'k': k})
            if k < n:
                rhs = X * F[k] / (k + 1) + dx(n + k) * (Q(n, (k + 1) * (n + k + 1)) * X + Q(1, n + k + 1))
                audit.equal(F[k + 1] - F[k], rhs, 'F_exact_forward_identity', {'n': n, 'k': k})
                audit.nonnegative(rhs, 'F_forward_sign', {'n': n, 'k': k})
        Dw = ax(n) * a(n, X + Z) - singleton(n, Z)
        audit.equal(Dw, sum((d(j, Z) * F[n - j] for j in range(n)), P(0)), 'D_full_convolution', {'n': n})
        audit.equal(sum((d(j, Z) for j in range(n)), P(0)), a(n - 1, Z), 'full_hockey_stick', {'n': n})
        convolution = sum((d(j, Z) * dx(n - j - 1) for j in range(n - 1)), P(0)) + d(n - 1, Z)
        audit.equal(convolution, d(n - 1, h), 'W_full_convolution', {'n': n})
        D2h = ax(n) * a(n, X + 2 * h) - singleton(n, 2 * h)
        audit.nonnegative(D2h - t(n) * a(n - 1, 2 * h), 'D_whole_lower_bound', {'n': n})
        Wupper = t(n) * (2 * d(n - 1, h) - d(n - 1, Z))
        audit.nonnegative(Wupper - W, 'W_whole_upper_bound', {'n': n})
        budget = t(n) * (a(n - 1, 2 * h) - 2 * n * d(n - 1, h) + n * d(n - 1, Z))
        Pwhole = D2h - n * W
        audit.nonnegative(Pwhole - budget, 'one_whole_star_budget', {'n': n})
        if n >= 7:
            audit.nonnegative(Pwhole - t(n) * a(n - 1, h), 'dilation_whole_original_payment', {'n': n})
        audit.nonnegative(t(n) * (a(n - 1, h) - ax(n - 1)), 'height_reserve_monotonicity', {'n': n})
        audit.nonnegative(t(n) * ax(n - 1) - ax(n) ** 2, 'final_product_payment', {'n': n})
        strict = ax(2 * n - 1) * (1 + Q(n - 1, 2 * n) * X)
        audit.nonnegative(kernel(n) - strict, 'K_explicit_strict_reserve', {'n': n})
        audit.check(all(strict.c.get((i, 0), 0) > 0 for i in range(2 * n + 1)), 'strict_reserve_all_degrees', {'n': n})
        # Literal center triangle: both residual margins and all multiplicities.
        generic_V = singleton(n - 1, Z)
        for x in range(5):
            for z in range(4):
                actual = sum(generic_V.evaluate(x - ca, x + z - cb)
                             for ca in range(x + 1) for cb in range(x - ca + 1))
                audit.equal(actual, W.evaluate(x, z), 'literal_center_contraction', {'n': n, 'x': x, 'z': z})
    for k in range(3, 13):
        Qwall = ax(2 * k - 3)
        c, e, Delta = Q(2 * k - 1, k), Q(k + 1, 2 * k), 2 * (k - 1) * (2 * k - 1)
        J = pair_low(k, X)
        audit.equal(J, X * (X - 1) * Qwall * (c + e * X) / Delta, 'full_wall_pair_identity', {'k': k})
        audit.equal(singleton(k, X), (d(2 * k, 2 * X) - dx(k) ** 2) / 2 + dx(k) * ax(k), 'diagonal_full_V_identity', {'k': k})
        audit.equal(c_complete(k, k), singleton(k, X) - J, 'diagonal_complete_C_identity', {'k': k})
        audit.equal(X * Qwall * (c + e * X) / Delta + J, X ** 2 * Qwall * (c + e * X) / Delta, 'adverse_pair_explicit_removed_positive', {'k': k})
        audit.nonnegative(ax(k) * ax(k - 2) - (1 + X) * Qwall, 'diagonal_sorted_product_bound', {'k': k})
        audit.nonnegative(c * (1 + X) - (c + e * X), 'diagonal_scalar_slope_bound', {'k': k})
        audit.nonnegative(Q(1, 2 * k) * t(k) * dx(k - 1) + J, 'diagonal_full_adverse_pair_payment', {'k': k})
        audit.nonnegative(Q(k - 1, k) * t(k) * dx(k - 1) - dx(k) * ax(k), 'diagonal_full_terminal_payment', {'k': k})
        audit.nonnegative(Q(2 * k - 2, 2 * k - 1) * t(k) * dx(k - 1) - d(2 * k, 2 * X) / 2, 'diagonal_even_odd_payment', {'k': k})
        audit.nonnegative((2 - Q(1, 2 * k - 1) - Q(1, 2 * k)) * t(k) * dx(k - 1) - c_complete(k, k), 'diagonal_combined_payment', {'k': k})
        odd = [Q(2 * i + 1, 2) for i in range(k)]
        target = sorted([Q(1), Q(k + 1, k), *[Q(i) for i in range(2, k - 1)], Q(k)])
        audit.check(len(odd) == len(target) == k and all(target[i] <= odd[i] for i in range(1, k - 1)), 'odd_middle_denominator_comparison', {'k': k})
        audit.equal(Q(1, 2 * k) * 2 * Q(k, 1) / odd[-1] / Q(1, k - 1), Q(2 * k - 2, 2 * k - 1), 'odd_endpoint_exact_multiplier', {'k': k})


def dilation_panels(audit):
    rows = []
    for m in range(1, 13):
        delta = a(m, 2 * X) - 2 * (m + 1) * dx(m) - ax(m)
        rows.append({'m': m, 'difference_coefficients': [str(delta.c.get((i, 0), Q(0))) for i in range(m + 1)]})
        if m >= 6:
            audit.nonnegative(delta, 'dilation_complete_coefficients', {'m': m})
            base = ax(m - 1)
            for k in range(1, m + 1):
                bk = base.c.get((k, 0), Q(0))
                previous = base.c.get((k - 1, 0), Q(0))
                audit.check(k * bk >= Q(m - k, m - 1) * previous, 'dilation_subset_coefficient_bound', {'m': m, 'k': k})
                coefficient = (2 ** k - 1) * bk + Q(2 ** k - 2 * m - 3, m) * previous
                audit.equal(coefficient, delta.c.get((k, 0), Q(0)), 'dilation_exact_coefficient_identity', {'m': m, 'k': k})
                if k >= 3:
                    numerator = (2 ** k - 1 - 2 * k) * m * m - k * (2 ** k - 3)
                    audit.check(numerator >= 0, 'dilation_numerator_sign', {'m': m, 'k': k, 'numerator': numerator})
                    if k >= 4:
                        audit.check(2 ** k - 1 >= 2 * k + 2, 'dilation_exponential_bound', {'k': k})
            H = sum((Q(1, i) for i in range(1, m)), Q(0))
            audit.equal(delta.c[(1, 0)], H - 2 - Q(1, m), 'dilation_exact_linear_coefficient', {'m': m})
            audit.equal(delta.c[(2, 0)], 3 * base.c[(2, 0)] - (2 - Q(1, m)) * H, 'dilation_exact_quadratic_coefficient', {'m': m})
        if m >= 5:
            H = sum((Q(1, i) for i in range(1, m)), Q(0))
            old = ax(m - 1).c[(2, 0)] - Q(2, 3) * H
            next_H = H + Q(1, m)
            new = ax(m).c[(2, 0)] - Q(2, 3) * next_H
            audit.equal(new - old, Q(1, m) * (H - Q(2, 3)), 'dilation_quadratic_induction_identity', {'m': m})
            audit.check(new >= old > 0, 'dilation_quadratic_induction_sign', {'m': m})
    audit.equal(ax(4).c[(2, 0)] - Q(2, 3) * sum((Q(1, i) for i in range(1, 5)), Q(0)), Q(5, 72), 'dilation_quadratic_exact_base', 'm5')
    audit.equal((a(6, 2 * X) - 14 * dx(6) - ax(6)).c[(1, 0)], Q(7, 60), 'dilation_linear_exact_base', 'm6')
    failed = a(5, 2 * X) - 12 * dx(5) - ax(5)
    audit.equal(failed.c[(1, 0)], Q(-7, 60), 'dilation_preserved_failed_m5', 'linear coefficient')
    audit.detects(any(value < 0 for value in failed.c.values()), 'dilation_m5_failure', {'linear': '-7/60'})
    return rows


def certificate_controls(audit, record):
    n = record['n']
    audit.check(validate_record(record, n), 'complete_schema_roundtrip', {'n': n})
    mutations = {}
    changed = deepcopy(record); changed['E_sites'][0]['coefficient'] = '1'; mutations['coefficient_mutation'] = changed
    changed = deepcopy(record); changed['E_sites'].pop(); mutations['missing_site'] = changed
    changed = deepcopy(record); changed['E_sites'].append(deepcopy(changed['E_sites'][-1])); mutations['duplicate_site'] = changed
    changed = deepcopy(record); changed['E_sites'][1]['z_power'] += 1; mutations['shifted_site'] = changed
    changed = deepcopy(record); changed['E_sites'][1], changed['E_sites'][2] = changed['E_sites'][2], changed['E_sites'][1]; mutations['wrong_site_order'] = changed
    changed = deepcopy(record); changed['total_degree'] -= 1; mutations['wrong_degree'] = changed
    changed = deepcopy(record); changed['variables'] = ['z', 'x']; mutations['wrong_variable_order'] = changed
    changed = deepcopy(record); changed['n'] += 1; mutations['wrong_index'] = changed
    for kind, changed in mutations.items():
        audit.refusal(changed, n, kind)
    whole = primary(n)
    removed_C_terminal = d(n - 1, Z) * t(n)
    audit.detects(removed_C_terminal != 0, 'dropped_C_terminal', {'n': n, 'complete_missing_term_rows': all_rows(removed_C_terminal, 2 * n)})
    for kind, bad in [('dropped_full_high_tail', reconstructed(n, omit_tail=True)), ('dropped_all_V_terminals', reconstructed(n, omit_terminal=True)), ('wrong_strict_shift', primary(n, central_shift=1)), ('wrong_first_row_cutoff', reconstructed(n, cutoff_shift=1))]:
        residual = bad - whole
        audit.detects(residual != 0, kind, {'n': n, 'difference_coefficients': len(residual.c), 'difference_rows': all_rows(residual, 2 * n)})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path, required=True)
    args = parser.parse_args()
    out=args.output
    out.mkdir(parents=True,exist_ok=False)
    args.attempt='public-export'
    started = time.monotonic()
    audit = Audit()
    try:
        roster=json.loads((TARGET/'SOURCE-MAP.json').read_text())
        for row in roster['files']:
            audit.equal(digest(TARGET/row['path']),row['sha256'],'source_authentication',row['path'])
        payload = source_bases(audit)
        symbolic_checks(audit)
        records = {}
        for n in range(3, 13):
            whole = primary(n)
            E = whole - kernel(n)
            audit.equal(whole, reconstructed(n), 'whole_first_row_vs_full_caps', {'n': n})
            audit.nonnegative(E, 'complete_high_E_coefficients', {'n': n})
            audit.equal(whole.degree(), 2 * n, 'complete_P_prior_degree', {'n': n})
            audit.equal(E.degree(), 2 * n, 'complete_E_prior_degree', {'n': n})
            audit.equal(whole.evaluate(0, 0), Q(1), 'whole_grade_zero', {'n': n})
            audit.equal(E.evaluate(0, 0), Q(0), 'reserve_grade_zero', {'n': n})
            audit.equal(pair_tail(n, X + Z).compose(X, P(0)), P(0), 'full_wall_tail_zero', {'n': n})
            wall_low = ax(n) * a(n, 3 * X) - singleton(n, 2 * X) - n * (singleton(n, X) - pair_low(n, X))
            audit.equal(whole.compose(X, P(0)), wall_low, 'full_H_equals_A_boundary', {'n': n})
            audit.equal(pair_low(n, P(0)), P(0), 'zero_height_pair', {'n': n})
            zero_height = ax(n) ** 2 - singleton(n, P(0)) - n * (singleton(n, P(0)) - pair_low(n, P(0)))
            audit.equal(zero_height, kernel(n), 'full_zero_height_E_exact_zero', {'n': n})
            record = {'n': n, 'variables': ['x', 'z'], 'total_degree': 2 * n,
                      'original_rows': ['A', 'A+2H', '(n-1)A+(n-2)H'],
                      'labeled_positive_columns': ['A'] + ['A+H'] * n,
                      'positive_column_count': n + 1, 'affine_lattice_index': 1,
                      'physical_zeros': 'reinsert in recorded positions; no extra positive support or degree',
                      'actual_degree_before_algebra': 2 * n, 'primary_identity': 'U10 (15)',
                      'E_rows': all_rows(E, 2 * n), 'P_rows': all_rows(whole, 2 * n),
                      'E_sites': full_sites(E, 2 * n), 'nonzero_E': len(E.c),
                      'zero_E': (2 * n + 1) * (2 * n + 2) // 2 - len(E.c)}
            records[n] = record
            certificate_controls(audit, record)
        compare_source_text(audit, records)
        for n in range(3, 7):
            source_record = payload['HIGH-E-' + str(n)]
            audit.equal(source_record['variables'], ['x', 'z'], 'source_fixed_JSON', {'n': n, 'check': 'variables'})
            audit.equal(source_record['total_degree_bound'], 2 * n, 'source_fixed_JSON', {'n': n, 'check': 'degree'})
            audit.equal(source_record['coefficients'], records[n]['E_rows'], 'source_fixed_JSON', {'n': n, 'check': 'all coefficients including zeros'})
            audit.equal(source_record['nonzero'], records[n]['nonzero_E'], 'source_fixed_JSON', {'n': n, 'check': 'nonzero count'})
        write_new(out / 'SOURCE-DATA-SHAPE.json', {'json_path': BASE_JSON, 'json_sha256': BASE_SHA, 'selected_mathematical_records': ['HIGH-E-' + str(n) for n in range(3, 7)], 'exact_arrays_compared': 4})
        finite_triangle_checks(audit)
        proof_panels(audit)
        dilation = dilation_panels(audit)
        factor_one = t(3) * dx(2) - c_complete(3, 3)
        audit.equal(factor_one.c[(1, 0)], Q(-1, 12), 'preserved_factor_one_failure', 'n=k=3')
        audit.detects(any(v < 0 for v in factor_one.c.values()), 'factor_one_C_failure', {'n': 3, 'k': 3, 'complete_difference_coefficients': all_rows(factor_one, 6), 'linear': '-1/12'})
        uncancelled = 1 - X + X ** 2
        cancelled_product = (1 + X) * uncancelled
        audit.equal(cancelled_product, 1 + X ** 3, 'positive_cancellation_counterexample_identity', 'all coefficients')
        audit.detects(any(v < 0 for v in uncancelled.c.values()) and all(v >= 0 for v in cancelled_product.c.values()), 'positive_polynomial_cancellation_invalid', {'difference': ['1', '-1', '1'], 'positive_product': ['1', '0', '0', '1']})
        for value in [0.5, 1.0, float('inf')]:
            try:
                P(value)
            except TypeError:
                audit.detects(True, 'floating_input_refusal', {'input': repr(value)})
            else:
                audit.detects(False, 'floating_input_refusal', {'input': repr(value)})
        for value in ['1.0', '2/2', '1/0', 'NaN', '00']:
            try:
                read_rational(value)
            except (ValueError, ZeroDivisionError):
                audit.detects(True, 'noncanonical_rational_refusal', {'input': value})
            else:
                audit.detects(False, 'noncanonical_rational_refusal', {'input': value})
        arrays = {'schema': 'a78-independent-high-star-arrays/v1', 'status': 'PROPOSED_ARITHMETIC_ONLY', 'scope': 'n3..6 fixed bases; n7..12 finite corroboration only', 'records': list(records.values()), 'dilation': dilation}
        write_new(out / 'ARRAYS-v1.json', arrays)
        write_new(out / 'CONTROLS-v1.json', {'count': len(audit.controls), 'kinds': dict(Counter(row['kind'] for row in audit.controls)), 'controls': audit.controls})
        summary = {'status': 'PASS', 'scientific_status': 'PROPOSED_UNTIL_ASTRA_GATE', 'attempt': args.attempt, 'elapsed_child_seconds': time.monotonic() - started, 'assertions_total': sum(audit.counts.values()), 'assertion_families': dict(audit.counts), 'controls_total': len(audit.controls), 'full_array_sites': sum((2 * n + 1) * (2 * n + 2) // 2 for n in records), 'fixed_base_sites': sum((2 * n + 1) * (2 * n + 2) // 2 for n in range(3, 7)), 'n': list(records), 'failures': audit.failures, 'arrays_sha256': digest(out / 'ARRAYS-v1.json'), 'controls_sha256': digest(out / 'CONTROLS-v1.json'), 'limitations': ['Finite algebra is corroboration, not an infinite-parameter theorem or adoption.', 'No bare LR/direct-table engine, provider code, root producer code, Sage, or broad suite was used.', 'Original realization/lattice and uniform scientific assembly remain root/Astra judgment.', 'All four complete provider mathematical JSON arrays and their associated mathematical text arrays were compared exactly; they remain SOURCE.']}
        write_new(out / 'CHECKS-v1.json', summary)
        print(json.dumps(summary, sort_keys=True), flush=True)
    except BaseException as error:
        write_new(out / 'FAILURE.json', {'attempt': args.attempt, 'elapsed_child_seconds': time.monotonic() - started, 'error': repr(error), 'assertion_counts_before_failure': dict(audit.counts), 'controls_before_failure': audit.controls, 'failures': audit.failures})
        raise


if __name__ == '__main__':
    main()
