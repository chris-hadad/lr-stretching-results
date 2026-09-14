"""Exact BV arithmetic in original integer lattices, at orders one through seven.

Adapted from an independently authored Fraction checker, frozen before primary
C++ values were read. The classical recurrence is stated in PROOF.md.
"""

from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
from math import comb, factorial, gcd, prod


def need(condition, message):
    if not condition:
        raise ValueError(message)


def normals(name):
    """Outward rows derived directly from the original listed inequalities."""
    if name == "capped_m4":
        dimension = 7
        rows, labels = [], []
        for i in range(4):
            row = [0] * dimension
            row[i] = -1
            rows.append(row)
            labels.append(f"y{i + 1}>=0")
        for i in range(3):
            row = [0] * dimension
            row[4 + i] = -1
            rows.append(row)
            labels.append(f"z{i + 1}>=0")
        rows.append([0, 0, 0, 0, 1, 1, 1])
        labels.append("z4=c-z1-z2-z3>=0")
        for i in range(4):
            row = [0] * dimension
            row[i] = 1
            if i < 3:
                row[4 + i] = 1
            else:
                row[4:] = [-1, -1, -1]
            rows.append(row)
            labels.append(f"y{i + 1}+z{i + 1}<=w{i + 1}")
        rows.append([1, 1, 1, 1, 0, 0, 0])
        labels.append("sum(y)<=d")
        return rows, labels
    need(name in {"transport_3x4", "transport_3x5"}, "Unknown normal system")
    columns = 3 if name == "transport_3x4" else 4
    dimension = 2 * columns
    rows, labels = [], []
    for i in range(2):
        for j in range(columns):
            row = [0] * dimension
            row[i * columns + j] = -1
            rows.append(row)
            labels.append(f"entry({i},{j})>=0")
    for i in range(2):
        rows.append([int(k // columns == i) for k in range(dimension)])
        labels.append(f"free row {i} sum <= row margin")
    for j in range(columns):
        rows.append([int(k % columns == j) for k in range(dimension)])
        labels.append(f"free column {j} sum <= column margin")
    rows.append([-1] * dimension)
    labels.append("minus total free sum <= corner margin difference")
    return rows, labels


def gram(rows):
    return tuple(tuple(sum(a * b for a, b in zip(x, y)) for y in rows) for x in rows)


def determinant(matrix):
    """Exact fraction-free determinant, with explicit division checks."""
    n = len(matrix)
    if not n:
        return 1
    a = [list(row) for row in matrix]
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                need(numerator % previous == 0, "Nonexact Bareiss division")
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def pivots(rows):
    """Independent exact row elimination, retaining a full-rank minor."""
    if not rows:
        return []
    a = [list(row) for row in rows]
    rank, columns = 0, []
    for column in range(len(a[0])):
        pivot_row = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot_row is None:
            continue
        a[rank], a[pivot_row] = a[pivot_row], a[rank]
        pivot = a[rank][column]
        if pivot == -1:
            a[rank] = [-x for x in a[rank]]
        elif pivot != 1:
            a[rank] = [F(x, pivot) for x in a[rank]]
        for i in range(rank + 1, len(a)):
            factor = a[i][column]
            if factor:
                a[i] = [x - factor * y for x, y in zip(a[i], a[rank])]
        columns.append(column)
        rank += 1
        if rank == len(a):
            break
    return columns


def image_index(rows):
    if not rows:
        return 1
    selected = pivots(rows)
    if len(selected) != len(rows):
        return 0
    minor = determinant([[row[j] for j in selected] for row in rows])
    index = abs(minor)
    if index == 1:
        return 1
    for columns in combinations(range(len(rows[0])), len(rows)):
        index = gcd(index, determinant([[row[j] for j in columns] for row in rows]))
        if index == 1:
            break
    return index


@lru_cache(maxsize=16000)
def inverse(matrix):
    n = len(matrix)
    a = [
        [F(value) for value in row] + [F(int(i == j)) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot_row = next((i for i in range(column, n) if a[i][column]), None)
        need(pivot_row is not None, "Singular metric")
        a[column], a[pivot_row] = a[pivot_row], a[column]
        pivot = a[column][column]
        a[column] = [value / pivot for value in a[column]]
        for i in range(n):
            if i != column and a[i][column]:
                factor = a[i][column]
                a[i] = [value - factor * other for value, other in zip(a[i], a[column])]
    return tuple(tuple(row[n:]) for row in a)


def canonical(matrix):
    """Exhaust generator permutations, grouped only by exact invariants."""
    n = len(matrix)
    groups = {}
    for i in range(n):
        signature = (
            matrix[i][i],
            tuple(sorted((matrix[j][j], matrix[i][j]) for j in range(n) if i != j)),
        )
        groups.setdefault(signature, []).append(i)
    choices = []
    for _, group in sorted(groups.items()):
        outside = [j for j in range(n) if j not in group]
        uniform = len({matrix[i][j] for i in group for j in group if i != j}) <= 1
        twins = len({tuple(matrix[i][j] for j in outside) for i in group}) <= 1
        choices.append(
            (tuple(group),) if uniform and twins else tuple(permutations(group))
        )
    best, order = None, None
    for choice in product(*choices):
        perm = tuple(i for group in choice for i in group)
        key = tuple(matrix[perm[i]][perm[j]] for i in range(n) for j in range(i, n))
        if best is None or key < best:
            best, order = key, perm
    return tuple(tuple(matrix[i][j] for j in order) for i in order), order


def type_id(matrix):
    return hashlib.sha256(
        json.dumps(matrix, separators=(",", ":")).encode()
    ).hexdigest()


def multiply(a, b, degree):
    result = [F(0)] * (degree + 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b[: degree + 1 - i]):
                if y:
                    result[i + j] += x * y
    return result


def residue_points(rows, axes, index):
    points = []
    for point in product(*(range(axis) for axis in axes)):
        enlarged = tuple(tuple(row) + (point[i],) for i, row in enumerate(rows))
        if image_index(enlarged) == index:
            points.append(point)
    need(len(points) * index == prod(axes), "Incomplete image-lattice numerator")
    return points


def bv(matrix, *, rows=None, base=37, omit_numerator=False):
    """Laurent recurrence organized by face dimension and original subsets.

    With rows=None, every image lattice is already certified Z^T. The metric
    H_T^-1 is computed separately for every T; a single w=(1,base,...) supplies
    compatible covectors. Returned values include explicit pole checks.
    """
    q = len(matrix)
    need(1 <= q <= 7, "BV order outside 1..7")
    w = tuple(base**i for i in range(q))
    subsets = [tuple(i for i in range(q) if mask >> i & 1) for mask in range(1 << q)]
    indices = [
        1 if rows is None else image_index(tuple(rows[i] for i in subset))
        for subset in subsets
    ]
    need(all(index > 0 for index in indices), "Nonindependent lattice in BV")
    covectors = {}
    for mask in range(1, 1 << q):
        subset = subsets[mask]
        metric = inverse(tuple(tuple(matrix[i][j] for j in subset) for i in subset))
        c = tuple(
            sum(metric[i][j] * w[node] for j, node in enumerate(subset))
            for i in range(len(subset))
        )
        need(all(c), f"Nongeneric specialization at {mask}; choose a new base")
        covectors[mask] = c
    scaled = {0: [F(1)] + [F(0)] * q}
    pole_checks = 0
    for size in range(1, q + 1):
        for mask, subset in enumerate(subsets):
            if len(subset) != size:
                continue
            c = covectors[mask]
            axes = [indices[mask] // indices[mask ^ (1 << node)] for node in subset]
            need(
                all(
                    indices[mask] % indices[mask ^ (1 << node)] == 0 for node in subset
                ),
                "Nonintegral primitive axis",
            )
            series = [F(1)] + [F(0)] * q
            for axis, covector in zip(axes, c):
                z = axis * covector
                factor = [F(0)] * (q + 1)
                factor[0] = -1 / z
                if q >= 1:
                    factor[1] = F(1, 2)
                if q >= 2:
                    factor[2] = -z / 12
                if q >= 4:
                    factor[4] = z**3 / 720
                if q >= 6:
                    factor[6] = -(z**5) / 30240
                series = multiply(series, factor, q)
            if rows is not None:
                selected = tuple(rows[i] for i in subset)
                points = residue_points(selected, axes, indices[mask])
                if omit_numerator:
                    points = [points[0]]
                exponential = [
                    sum((sum(x * y for x, y in zip(c, point))) ** k for point in points)
                    / F(factorial(k))
                    for k in range(q + 1)
                ]
                series = multiply(series, exponential, q)
            # Every proper face uses its complete, already computed Laurent
            # series. A degree q truncation is shared across all subset sizes.
            for child, child_subset in enumerate(subsets):
                if child == mask or child & mask != child:
                    continue
                removed = [
                    i for i, node in enumerate(subset) if not (child >> node & 1)
                ]
                factor = F((-1) ** len(removed) * indices[child], indices[mask])
                factor /= prod(c[i] for i in removed)
                for degree in range(q + 1):
                    series[degree] -= factor * scaled[child][degree]
            need(
                all(value == 0 for value in series[:size]),
                f"Uncancelled pole at subset {mask}",
            )
            pole_checks += size
            scaled[mask] = series
    return scaled[(1 << q) - 1][q], {
        "base": base,
        "w": list(w),
        "pole_coefficients_checked": pole_checks,
        "subsets_checked": (1 << q) - 1,
    }
