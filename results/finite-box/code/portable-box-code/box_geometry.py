"""Independent certificate mathematics for the complete boxed hive and row model.

Only the previously accepted forced-mask table is an external geometric premise.
No returned source module is imported. Rows are literal integer affine forms.
"""
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

CANONICAL = Path('/Volumes/SLR-Research/stretched-lr-research')


def need(b, message):
    if not b:
        raise ValueError(message)


def add(*rows):
    return [sum(v) for v in zip(*rows)]


def minus(a, b):
    return [x - y for x, y in zip(a, b)]


def rank(matrix):
    a = [list(map(Fraction, row)) for row in matrix]
    r = 0
    for j in range(len(a[0]) if a else 0):
        pivot = next((k for k in range(r, len(a)) if a[k][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        den = a[r][j]
        a[r] = [x / den for x in a[r]]
        for k in range(r + 1, len(a)):
            factor = a[k][j]
            if factor:
                a[k] = [x - factor * y for x, y in zip(a[k], a[r])]
        r += 1
    return r


@lru_cache(None)
def triangle(n):
    interior = tuple((i, j) for i in range(1, n) for j in range(1, n - i))
    # Up-triangle plus each adjacent down-triangle, in the source row order.
    stencil = []
    for i in range(n):
        for j in range(n - i):
            if i + j < n - 1:
                stencil.append((((i + 1, j), 1), ((i, j + 1), 1), ((i, j), -1), ((i + 1, j + 1), -1)))
            if j:
                stencil.append((((i, j), 1), ((i + 1, j), 1), ((i, j + 1), -1), ((i + 1, j - 1), -1)))
            if i:
                stencil.append((((i, j), 1), ((i, j + 1), 1), ((i + 1, j), -1), ((i - 1, j + 1), -1)))
    need(len(stencil) == 3 * n * (n - 1) // 2, 'Incomplete rhombus stencil')
    return interior, tuple(stencil)


@lru_cache(None)
def accepted_masks(n):
    p = CANONICAL / f'methods/frontier-025-2026-09-10/science/results/F025-MASK-R{n}-001.json'
    records = json.loads(p.read_text())['records']
    return tuple((r['closed_rows_mask'], r['dimension_bound']) for r in records)


def boundaries(n, partitions, width):
    L, M, N = partitions
    H = {}
    def put(point, value):
        row = [value] + [0] * width
        need(point not in H or H[point] == row, 'Inconsistent hive corner')
        H[point] = row
    for i in range(n + 1):
        put((i, 0), sum(M[:i]))
        put((0, i), sum(L[:i]))
        put((n - i, i), sum(M) + sum(N[:i]))
    return H


def rhombi(H, stencil):
    return [[sum(sign * H[p][k] for p, sign in row) for k in range(len(next(iter(H.values()))))]
            for row in stencil]


@lru_cache(None)
def linear_template(n, mask, closed, T, free):
    points, stencil = triangle(n)
    dim, m = len(free), len(points)
    need(accepted_masks(n)[mask] == (closed, dim), 'Forced-mask premise mismatch')
    need(len(T) == m and all(len(row) == dim for row in T), 'Chart shape')
    for j, k in enumerate(free):
        need(T[k] == tuple(int(q == j) for q in range(dim)), 'No integer coordinate left inverse')
    H = {p: [0] * (m + 1) for row in stencil for p, s in row}
    for j, point in enumerate(points):
        H[point][j + 1] = 1
    A = [r[1:] for r in rhombi(H, stencil)]
    E = [row for i, row in enumerate(A) if closed >> i & 1]
    need(rank(E) == m - dim, 'Incomplete forced affine hull')
    projected = [[sum(x * T[k][j] for k, x in enumerate(row)) for j in range(dim)] for row in A]
    need(all(not any(row) for i, row in enumerate(projected) if closed >> i & 1), 'Chart leaves forced affine hull')
    return A


def compact(rows):
    out = {}
    for row in rows:
        g = math.gcd(*row[1:])
        if not g:
            need(row[0] >= 0, 'Contradictory constant inequality')
            continue
        key = tuple(x // g for x in row[1:])
        value = Fraction(row[0], g)
        out[key] = min(out.get(key, value), value)
    return out


def check(c, require_short_normals=True):
    n, d = c['rank'], c['degree_bound']
    need(n in (6, 7) and 1 <= d <= (n - 1) * (n - 2) // 2, 'Out-of-scope chart')
    parts = [c['original'][k] for k in ('lambda', 'mu', 'nu')]
    for p in parts:
        need(len(p) == n and all(type(v) is int and v >= 0 for v in p)
             and p == sorted(p, reverse=True), 'Invalid original partition')
    need(sum(parts[0]) == sum(parts[1]) + sum(parts[2]) <= 30, 'Original area/trace')
    dual = lambda p: [-v for v in reversed(p)]
    weights = [parts[1], parts[2], dual(parts[0])]
    word = c['count_preserving_word']
    if word['dual_all']:
        weights = list(map(dual, weights))
    outer, (i, j) = word['outer'], word['inner_order']
    need(sorted((outer, i, j)) == [0, 1, 2], 'Invalid tensor permutation')
    a, b = weights[i][-1], weights[j][-1]
    target = [[v - a - b for v in dual(weights[outer])],
              [v - a for v in weights[i]], [v - b for v in weights[j]]]
    need([a, b] == word['determinant_shifts'], 'Determinant shift')
    need(target == [c['count_boundary'][k] for k in ('lambda', 'mu', 'nu')], 'Tensor count boundary')
    mask = sum(1 << (s * (n - 1) + k) for s, p in enumerate(target)
               for k in range(n - 1) if p[k] == p[k + 1])
    need(mask == c['mask'], 'Boundary mask')
    ar = c['affine_repair']
    initial = ar.get('initial_chart', c['chart'])
    tr = ar.get('initial_translation', c['translation'])
    T, off, free = initial['basis_rows'], initial['offset'], initial['free_original_coordinates']
    dim = initial['dimension_bound']
    need(dim == len(free) == len(tr) and len(set(free)) == dim, 'Initial dimension/coordinates')
    A = linear_template(n, mask, c['closed_rows_mask'], tuple(map(tuple, T)), tuple(free))
    points, stencil = triangle(n)
    H = boundaries(n, target, len(points))
    for k, point in enumerate(points):
        H[point] = [0] + [int(j == k) for j in range(len(points))]
    raw = rhombi(H, stencil)
    need(raw == c['original_rhombus_rows'], 'Original complete rhombus system')
    chart_rows = [[r[0] + sum(v * x for v, x in zip(r[1:], off)),
                   *[sum(v * row[j] for v, row in zip(r[1:], T)) for j in range(dim)]] for r in raw]
    need(chart_rows == initial['rows'], 'Initial affine row substitution')
    need(all(not any(r) for i, r in enumerate(chart_rows) if c['closed_rows_mask'] >> i & 1),
         'Forced affine constants')
    need(all(off[k] == 0 for k in free), 'Initial inverse offset')
    rows = [[r[0] + sum(v * x for v, x in zip(r[1:], tr)), *r[1:]] for r in chart_rows]
    base = [v + sum(x * y for x, y in zip(row, tr)) for v, row in zip(off, T)]
    T = [row[:] for row in T]
    for step in ar.get('unit_eliminations', []):
        need(hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()
             == step['before_rows_sha256'], 'Affine repair source')
        rel = step['positive_zero_relation']
        need(bool(rel) and all(type(w) is int and w > 0 and 0 <= r < len(rows) for r, w in rel),
             'Invalid positive forcing relation')
        need(all(sum(w * rows[r][k] for r, w in rel) == 0 for k in range(len(rows[0]))),
             'Invalid zero forcing relation')
        r = step['equation_row']
        need(r in [x for x, w in rel], 'Equation not forced')
        g = math.gcd(*rows[r])
        need(g > 0 and g == step['equation_divisor'], 'Equation divisor')
        equation = [x // g for x in rows[r]]
        pivot = step['pivot_current_column']
        v = equation[pivot + 1]
        need(v in (-1, 1) and v == step['pivot'], 'Nonsaturated repair pivot')
        shift = -equation[0] // v
        coeff = [-x // v for x in equation[1:]]
        coeff[pivot] = 0
        need(shift == step['shift'] and coeff == step['replacement_coefficients'], 'Repair inverse')
        base = [x + row[pivot] * shift for x, row in zip(base, T)]
        T = [[row[k] + row[pivot] * coeff[k] for k in range(len(coeff)) if k != pivot] for row in T]
        rows = [[row[0] + row[pivot + 1] * shift,
                 *[row[k + 1] + row[pivot + 1] * coeff[k] for k in range(len(coeff)) if k != pivot]] for row in rows]
    need(rows == c['full_translated_rows'] and T == c['chart']['basis_rows'], 'Final repaired chart')
    need(all(len(row) == d for row in T), 'Actual chart dimension')
    need(base == [v + sum(x * y for x, y in zip(row, c['translation']))
                  for v, row in zip(c['chart']['offset'], T)], 'Final chart offset')
    need(compact(rows) == compact(c['count_rows']), 'Count rows omit a constraint')
    if require_short_normals:
        for row in c['count_rows']:
            g = math.gcd(*row[1:])
            if g:
                need(sum((v // g)**2 for v in row[1:]) <= 6, 'Short-normal theorem inapplicable')
    H = boundaries(n, target, d)
    for k, point in enumerate(points):
        H[point] = [base[k], *T[k]]
    zero = [0] * (d + 1)
    entries = [[zero[:] for _ in range(n)] for _ in range(n)]
    for r in range(1, n + 1):
        for k in range(1, r + 1):
            first = minus(H[(r - k, k)], H[(r - k + 1, k - 1)])
            previous = zero if r == k else minus(H[(r - k - 1, k)], H[(r - k, k - 1)])
            entries[r - 1][k - 1] = minus(first, previous)
    need(entries == c['row_chart']['row_forms'], 'Full row/hive inverse')
    C = lambda v: [v] + [0] * d
    for r in range(n):
        need(add(*entries[r]) == C(target[0][r] - target[1][r]), 'Row-size equation')
    for k in range(n):
        need(add(*(entries[r][k] for r in range(n))) == C(target[2][k]), 'Content equation')
    for (i, j), v in H.items():
        need(add(C(sum(target[1][:i + j])), *(entries[r][k] for r in range(i + j) for k in range(j))) == v,
             'Forward row/hive map')
    forms, flags = [], [[[0] * n for _ in range(n)] for _ in range(3)]
    for r in range(n):
        for k in range(n):
            choices = [('nonnegative', entries[r][k], 0)]
            if r:
                left = add(C(target[1][r - 1] - target[1][r]), *entries[r - 1][:k])
                right = add(*entries[r][:k + 1])
                choices.append(('column', minus(left, right), 1))
            if k:
                left = add(zero, *(entries[j][k - 1] for j in range(r)))
                right = add(*(entries[j][k] for j in range(r + 1)))
                choices.append(('ballot', minus(left, right), 2))
            for kind, form, index in choices:
                strict = int(any(form[1:]))
                forms.append({'kind': kind, 'row': r + 1, 'label': k + 1, 'form': form, 'strict': strict})
                flags[index][r][k] = strict
    need(forms == c['row_chart']['all_constraint_forms'], 'Complete row constraint system')
    need(flags == [c['row_chart'][k] for k in ('nonnegative_thresholds', 'column_thresholds', 'ballot_thresholds')],
         'True-interior threshold mismatch')
    raw_set, form_set = set(map(tuple, rows)), {tuple(x['form']) for x in forms}
    need(all(tuple(r) in form_set or (not any(r[1:]) and r[0] >= 0) for r in rows), 'Missing rhombus in row constraints')
    for x in forms:
        if any(x['form'][1:]) and tuple(x['form']) not in raw_set:
            need(x['kind'] == 'nonnegative' and x['row'] == x['label'], 'Extra unsupported row constraint')
    for r in range(n):
        need(add(C(target[2][-1]), *(minus(entries[j][j], entries[j + 1][j + 1]) for j in range(r, n - 1))) == entries[r][r],
             'Diagonal nonnegativity telescoping')
    gate = c['dimension_gate']
    need(c['actual_dimension'] == d, 'Actual dimension missing')
    t, point = gate['t'], gate['point']
    need(type(t) is int and t > 0 and len(point) == d and all(type(x) is int for x in point), 'Strict witness type')
    need(all(t * row[0] + sum(a * b for a, b in zip(row[1:], point)) >= int(any(row[1:])) for row in rows),
         'Not strict in the complete relative affine hull')
    hp = [t * b + sum(x * y for x, y in zip(row, point)) for b, row in zip(base, T)]
    need(hp == gate['whole_hive_point'], 'Strict witness forward image')
    slacks = [t * row[0] + sum(a * b for a, b in zip(row[1:], hp)) for row in raw]
    need(slacks == gate['all_original_rhombus_slacks'] and min(slacks) >= 0, 'Whole hive witness')
    return flags
