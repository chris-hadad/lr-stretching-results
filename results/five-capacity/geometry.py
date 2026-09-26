from fractions import Fraction
from itertools import combinations,permutations,product
from math import gcd
import hashlib,json
from arithmetic import bv,inverse

def need(condition, detail):
    if not condition:
        raise ValueError(detail)


def original_inequalities():
    # Bounds are coefficient vectors in (w1,...,w5,c,d), always multiplied by t.
    rows = []
    for variable in range(10):
        row = [0] * 10
        row[variable] = -1
        name = ('y' + str(variable + 1) if variable < 5 else 'z' + str(variable - 4))
        rows.append((name + '>=0', row, [0] * 7))
    for i in range(5):
        row, bound = [0] * 10, [0] * 7
        row[i] = row[5 + i] = bound[i] = 1
        rows.append((f'y{i + 1}+z{i + 1}<=w{i + 1}*t', row, bound))
    rows.append(('sum(y)<=d*t', [1] * 5 + [0] * 5, [0] * 6 + [1]))
    return rows


def construct_normals():
    rows, labels, bounds = [], [], []
    for label, row, bound in original_inequalities():
        free_row = row[:5] + [row[5 + j] - row[9] for j in range(4)]
        free_bound = bound[:]
        free_bound[5] -= row[9]
        rows.append(tuple(free_row))
        labels.append(label)
        bounds.append(tuple(free_bound))
    # Independent direct expression of every substituted inequality.
    direct = []
    for i in range(9):
        direct.append(tuple(-int(i == j) for j in range(9)))
    direct.append((0, 0, 0, 0, 0, 1, 1, 1, 1))
    for i in range(4):
        direct.append(tuple(int(j == i or j == 5 + i) for j in range(9)))
    direct.append((0, 0, 0, 0, 1, -1, -1, -1, -1))
    direct.append((1, 1, 1, 1, 1, 0, 0, 0, 0))
    need(rows == direct, 'Substitution/direct constructor mismatch')
    validate_normal_roster(rows)
    return rows, labels, bounds


def validate_normal_roster(rows):
    need(len(rows) == 16, 'Normal roster must contain all 16 literal rows')
    need(all(len(row) == 9 for row in rows), 'Malformed coordinate dimension')
    need(all(type(x) is int for row in rows for x in row), 'Noninteger normal')
    need(all(any(row) for row in rows), 'Zero normal')
    need(len(set(map(tuple, rows))) == 16, 'Repeated normal')


def rank_columns(rows):
    if not rows:
        return []
    a = [list(row) for row in rows]
    pivot_columns = []
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for i in range(rank + 1, len(a)):
            if a[i][col]:
                p, f = a[rank][col], a[i][col]
                a[i] = [p * x - f * y for x, y in zip(a[i], a[rank])]
                common = 0
                for x in a[i]:
                    common = gcd(common, x)
                if common > 1:
                    a[i] = [x // common for x in a[i]]
        pivot_columns.append(col)
        rank += 1
        if rank == len(a):
            break
    return pivot_columns


def determinant(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    a = [list(row) for row in matrix]
    previous, sign = 1, 1
    for k in range(n - 1):
        p = next((r for r in range(k, n) if a[r][k]), None)
        if p is None:
            return 0
        if p != k:
            a[k], a[p] = a[p], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                need(numerator % previous == 0, 'Bareiss nonexact division')
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def full_image_index(rows):
    columns = rank_columns(rows)
    q = len(rows)
    if len(columns) < q:
        return {'rank': len(columns), 'image_index': 0,
                'minor_columns': None, 'minor_determinant': 0, 'minors_examined': 0}
    det = determinant([[row[j] for j in columns] for row in rows])
    need(det != 0, 'Selected full-rank minor vanished')
    index, examined = abs(det), 1
    witness_columns, witness_det = columns, det
    if index != 1:
        for cols in combinations(range(len(rows[0])), q):
            if tuple(cols) == tuple(columns):
                continue
            value = determinant([[row[j] for j in cols] for row in rows])
            examined += 1
            index = gcd(index, value)
            if abs(value) == 1:
                witness_columns, witness_det = list(cols), value
            if index == 1:
                break
    return {'rank': q, 'image_index': index, 'minor_columns': witness_columns,
            'minor_determinant': witness_det, 'minors_examined': examined}


def gram(rows):
    return tuple(tuple(sum(rows[i][k] * rows[j][k] for k in range(len(rows[0])))
                       for j in range(len(rows))) for i in range(len(rows)))


def canonical_permutation(matrix):
    # An isomorphism must preserve each signature. Within a uniform twin class,
    # every order gives the identical matrix; all other orders are enumerated.
    q = len(matrix)
    groups = {}
    for i in range(q):
        signature = (matrix[i][i], tuple(sorted((matrix[j][j], matrix[i][j])
                                                 for j in range(q) if j != i)))
        groups.setdefault(signature, []).append(i)
    options = []
    for signature in sorted(groups):
        group = groups[signature]
        outside = [j for j in range(q) if j not in group]
        twins = all(matrix[i][j] == matrix[group[0]][j] for i in group for j in outside)
        offdiagonals = {matrix[i][j] for i in group for j in group if i != j}
        options.append([tuple(group)] if twins and len(offdiagonals) <= 1
                       else list(permutations(group)))
    best, best_order = None, None
    for selections in product(*options):
        order = tuple(i for selection in selections for i in selection)
        key = tuple(matrix[i][j] for i in order for j in order)
        if best is None or key < best:
            best, best_order = key, order
    canonical = tuple(tuple(matrix[i][j] for j in best_order) for i in best_order)
    need(sorted(best_order) == list(range(q)), 'Malformed generator permutation')
    return canonical, best_order


def safe_type(rows, index):
    need(index == 1, 'Gram-only reuse requires verified full image lattice Z^q')
    canonical, order = canonical_permutation(gram(rows))
    key = {'q': len(rows), 'gram': canonical, 'full_image_lattice': 'Z^q'}
    type_id = hashlib.sha256(json.dumps(key, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return type_id, key, order


def must_refuse(fn):
    try:
        fn()
    except ValueError as e:
        return str(e)
    raise ValueError('Distinguishing control failed to refuse malformed input')


def controls():
    rows, _, _ = construct_normals()
    result = {}
    result['missing_literal'] = must_refuse(lambda: validate_normal_roster(rows[:-1]))
    result['duplicate_literal'] = must_refuse(lambda: validate_normal_roster(rows[:-1] + [rows[0]]))
    result['malformed_dimension'] = must_refuse(lambda: validate_normal_roster([rows[0][:-1]] + rows[1:]))
    zero = [(0,) * 9] + rows[1:]
    result['zero_normal'] = must_refuse(lambda: validate_normal_roster(zero))
    noninteger = [tuple([False] + list(rows[0][1:]))] + rows[1:]
    result['boolean_coordinate'] = must_refuse(lambda: validate_normal_roster(noninteger))
    dependent = (rows[0], rows[0])
    need(full_image_index(dependent)['image_index'] == 0, 'Dependent control not detected')
    result['dependent_index'] = 0
    saturated = ((3, 1, 4), (0, 1, 0))
    nonsaturated = ((5, 1, 0), (0, 1, 0))
    need(gram(saturated) == gram(nonsaturated), 'Same-Gram fixture is malformed')
    sat_index = full_image_index(saturated)['image_index']
    nonsat_index = full_image_index(nonsaturated)['image_index']
    need((sat_index, nonsat_index) == (1, 5), 'Full image-index control failed')
    result['same_gram_nonsaturated_refusal'] = must_refuse(lambda: safe_type(nonsaturated, nonsat_index))
    sat_value, sat_checks = bv(gram(saturated), rows=saturated)
    nonsat_value, nonsat_checks = bv(gram(nonsaturated), rows=nonsaturated)
    need(sat_value != nonsat_value, 'Same-Gram different-lattice values did not distinguish')
    result['same_gram_lattice_control'] = {
        'saturated_rows': saturated, 'nonsaturated_rows': nonsaturated,
        'gram': gram(saturated), 'indices': [sat_index, nonsat_index],
        'values': [str(sat_value), str(nonsat_value)],
        'checks': [sat_checks, nonsat_checks]}
    result['omitted_nonprimitive_numerator'] = must_refuse(
        lambda: bv(gram(nonsaturated), rows=nonsaturated, omit_numerator=True))
    original_type, _, _ = safe_type(saturated, sat_index)
    permuted_type, _, _ = safe_type(tuple(reversed(saturated)), sat_index)
    need(original_type == permuted_type, 'Generator-permutation control failed')
    result['permutation_reuse'] = True
    return result
