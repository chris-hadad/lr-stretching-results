"""Locally authored exact arithmetic for the full four by five table polynomial.

The only imported code is Python's standard library. Returned programs are never
read, imported, or run. Mathematical sources and numeric schema are in README.md.
Polynomials below use packed base-16 exponent tuples and denominator degree!.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import factorial, gcd, lcm

DEGREE = 12
DENOMINATOR = factorial(DEGREE)
ROW_PERTURBATION = (1, 2, 4, 8)
COLUMN_PERTURBATION = (16, 32, 64, 128, -225)

# Columns of V, in the numerical dataset's chamber order. The inequalities
# of each independently derived inverse partition the positive simple-root cone.
RAYS = (
    ((1, 0, 0), (0, 0, 1), (1, 1, 1)),
    ((0, 0, 1), (0, 1, 1), (1, 1, 1)),
    ((1, 0, 0), (1, 1, 0), (1, 1, 1)),
    ((1, 1, 0), (0, 1, 0), (1, 2, 1)),
    ((0, 1, 1), (0, 1, 0), (1, 2, 1)),
    ((1, 1, 0), (1, 1, 1), (1, 2, 1)),
    ((0, 1, 1), (1, 1, 1), (1, 2, 1)),
)


def dot(a, b):
    if len(a) != len(b):
        raise ValueError("dot product dimensions differ")
    return sum(x * y for x, y in zip(a, b))


def solve(matrix, rhs):
    """Rational Gauss elimination; singular systems return None."""
    size = len(rhs)
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("solve requires a square matrix")
    rows = [[Fraction(x) for x in row] + [Fraction(b)]
            for row, b in zip(matrix, rhs)]
    for col in range(size):
        pivot = next((r for r in range(col, size) if rows[r][col]), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x / divisor for x in rows[col]]
        for r in range(size):
            if r != col and rows[r][col]:
                scale = rows[r][col]
                rows[r] = [x - scale * y for x, y in zip(rows[r], rows[col])]
    return tuple(row[-1] for row in rows)


def rank(matrix):
    if not matrix:
        return 0
    rows = [[Fraction(x) for x in row] for row in matrix]
    answer = 0
    for col in range(len(rows[0])):
        pivot = next((r for r in range(answer, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        divisor = rows[answer][col]
        rows[answer] = [x / divisor for x in rows[answer]]
        for r in range(answer + 1, len(rows)):
            if rows[r][col]:
                scale = rows[r][col]
                rows[r] = [x - scale * y for x, y in zip(rows[r], rows[answer])]
        answer += 1
        if answer == len(rows):
            break
    return answer


def determinant(matrix):
    rows = [[Fraction(x) for x in row] for row in matrix]
    size = len(rows)
    answer = Fraction(1)
    for col in range(size):
        pivot = next((r for r in range(col, size) if rows[r][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            rows[col], rows[pivot] = rows[pivot], rows[col]
            answer = -answer
        divisor = rows[col][col]
        answer *= divisor
        for r in range(col + 1, size):
            scale = rows[r][col] / divisor
            for c in range(col + 1, size):
                rows[r][c] -= scale * rows[col][c]
    return answer


@lru_cache(None)
def inverse(chamber):
    matrix = list(zip(*RAYS[chamber]))
    columns = [solve(matrix, [int(i == j) for i in range(3)]) for j in range(3)]
    result = tuple(tuple(columns[j][i] for j in range(3)) for i in range(3))
    if abs(determinant(matrix)) != 1 or any(x.denominator != 1 for row in result for x in row):
        raise ArithmeticError("A3 cone does not have a saturated unimodular chart")
    return tuple(tuple(int(x) for x in row) for row in result)


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


@lru_cache(None)
def sites(variables=3, degree=DEGREE):
    if variables == 0:
        return ((),)
    return tuple((i,) + tail for i in range(degree + 1)
                 for tail in sites(variables - 1, degree - i))


def occupation_key(occupation):
    if len(occupation) != 4 or any(type(n) is not int or n < 0 for n in occupation) or sum(occupation) != 5:
        raise ValueError("occupation must be a weak composition of five into four")
    return "".join(str(n) for n in occupation)


def strict_site(chamber, site):
    return tuple(sum(RAYS[chamber][j][i] * (site[j] + 1) for j in range(3)) for i in range(3))


def strict_chamber(slope):
    """The exterior has value None. Positive interior ties are refused."""
    x, y, z = slope
    if min(slope) < 0:
        return None
    if not all((x, y, z, x - y, y - z, x - z, x + z - y)):
        raise ValueError("chamber selector received an unresolved wall")
    hits = [c for c in range(7) if all(dot(row, slope) > 0 for row in inverse(c))]
    if len(hits) != 1:
        raise ArithmeticError(f"positive generic A3 point has {len(hits)} chambers")
    return hits[0]


def edge_vectors(occupation):
    """Each parallel edge is a separate unbounded nonnegative variable."""
    return tuple(tuple(int(i <= k < j) for k in range(3))
                 for i in range(4) for j in range(i + 1, 4)
                 for _ in range(occupation[i] + occupation[j]))


def repeated_edge_counts(occupation, points):
    """Complete 3D coin-change DP; no wall values or source counts are used.

    All roots have nonnegative simple coordinates, so a path ending in this
    box cannot leave and re-enter it. Forward updates count every allocation
    of each labeled parallel edge once. Zero multiplicities add no variables.
    """
    points = tuple(tuple(p) for p in points)
    if not points or any(len(p) != 3 or any(type(x) is not int or x < 0 for x in p) for p in points):
        raise ValueError("count points must be nonempty nonnegative integer triples")
    bounds = tuple(max(p[i] for p in points) for i in range(3))
    x_max, y_max, z_max = bounds
    y_stride, x_stride = z_max + 1, (y_max + 1) * (z_max + 1)
    table = [0] * ((x_max + 1) * x_stride)
    table[0] = 1
    operations = 0
    edges = edge_vectors(occupation)
    anchor = next(i for i, n in enumerate(occupation) if n > 0)
    saturation_basis = [tuple(int(min(anchor, j) <= k < max(anchor, j)) for k in range(3))
                        for j in range(4) if j != anchor]
    saturation_minor = determinant(saturation_basis)
    if abs(saturation_minor) != 1 or any(root not in edges for root in saturation_basis):
        raise ArithmeticError("original root lattice saturation witness failed")
    for dx, dy, dz in edges:
        shift = dx * x_stride + dy * y_stride + dz
        for x in range(dx, x_max + 1):
            for y in range(dy, y_max + 1):
                start = x * x_stride + y * y_stride
                for z in range(dz, z_max + 1):
                    index = start + z
                    table[index] += table[index - shift]
                    operations += 1
    counts = [table[x * x_stride + y * y_stride + z] for x, y, z in points]
    return counts, {"bounds": bounds, "box_positions": len(table), "labeled_edges": len(edges),
                    "edge_rank": rank(edges), "saturation_basis": saturation_basis,
                    "saturation_minor": int(saturation_minor), "updates": operations}


def newton_from_values(values, degree=DEGREE):
    """Tensor binomial inversion on the lower simplex, without a fitted sign."""
    order = sites(3, degree)
    if len(values) != len(order) or any(type(v) is not int for v in values):
        raise ValueError("wrong complete determining array")
    differences = dict(zip(order, values))
    for axis in range(3):
        other_axes = [i for i in range(3) if i != axis]
        for u, v in sites(2, degree):
            available = degree - u - v
            for step in range(1, available + 1):
                for coordinate in range(available, step - 1, -1):
                    here = [0, 0, 0]
                    here[axis], here[other_axes[0]], here[other_axes[1]] = coordinate, u, v
                    before = here.copy()
                    before[axis] -= 1
                    differences[tuple(here)] -= differences[tuple(before)]
    return tuple(differences[s] for s in order)


def generalized_binomial(value, degree):
    result = Fraction(1)
    for i in range(degree):
        result *= Fraction(value - i, i + 1)
    return result


def newton_value(coefficients, point, degree=DEGREE):
    factors = [[generalized_binomial(v, k) for k in range(degree + 1)] for v in point]
    return sum(coefficient * factors[0][i] * factors[1][j] * factors[2][k]
               for (i, j, k), coefficient in zip(sites(3, degree), coefficients))


def pack(exponents):
    if any(type(e) is not int or e < 0 or e >= 16 for e in exponents):
        raise ValueError("invalid base-16 exponent")
    return sum(e << (4 * i) for i, e in enumerate(exponents))


def unpack(key, variables):
    if type(key) is not int or key < 0 or key >= (1 << (4 * variables)):
        raise ValueError("packed exponent exceeds variable count")
    return tuple((key >> (4 * i)) & 15 for i in range(variables))


def add_polynomial(target, source, weight=1):
    for key, value in source.items():
        target[key] = target.get(key, 0) + weight * value
    # Removing exact zeros is a sparse representation operation, never clipping.
    return target


def multiply_affine(polynomial, form, subtract=0):
    constant = form[0] - subtract
    output = {}
    nonzero_terms = [(1 << (4 * axis), value) for axis, value in enumerate(form[1:]) if value]
    for key, coefficient in polynomial.items():
        if not coefficient:
            continue
        if constant:
            output[key] = output.get(key, 0) + coefficient * constant
        for shift, value in nonzero_terms:
            new_key = key + shift
            output[new_key] = output.get(new_key, 0) + coefficient * value
    return output


def contract_newton(coefficients, forms, degree=DEGREE):
    """Return degree! times the COMPLETE affine substitution as integers.

    Nested falling-factorial Horner is derived directly from the Newton basis.
    No returned implementation supplies this routine, and no degrees are cut.
    """
    if len(forms) != 3 or len({len(f) for f in forms}) != 1:
        raise ValueError("three equally sized affine forms required")
    order = sites(3, degree)
    if len(coefficients) != len(order) or any(type(v) is not int for v in coefficients):
        raise ValueError("incomplete or inexact Newton array")
    if any(type(x) is not int for f in forms for x in f):
        raise ValueError("affine coefficients must be exact integers")
    denominator = factorial(degree)
    scaled = {}
    for (i, j, k), coefficient in zip(order, coefficients):
        divisor = factorial(i) * factorial(j) * factorial(k)
        if denominator % divisor:
            raise ArithmeticError("factorial denominator is not integral")
        scaled[i, j, k] = coefficient * (denominator // divisor)
    outer = {}
    for i in range(degree, -1, -1):
        middle = {}
        for j in range(degree - i, -1, -1):
            inner = {}
            for k in range(degree - i - j, -1, -1):
                inner = multiply_affine(inner, forms[2], k)
                inner[0] = inner.get(0, 0) + scaled[i, j, k]
            middle = multiply_affine(middle, forms[1], j)
            add_polynomial(middle, inner)
        outer = multiply_affine(outer, forms[0], i)
        add_polynomial(outer, middle)
    return {k: v for k, v in outer.items() if v}


def original_offset(occupation):
    _, n1, n2, n3 = occupation
    return (-n1 - n2 - n3, -2 * (n2 + n3), -3 * n3)


def simple_coordinates(netflow):
    if len(netflow) != 4 or sum(netflow) != 0:
        raise ValueError("netflow must have four entries summing to zero")
    return (netflow[0], netflow[0] + netflow[1], -netflow[3])


def substitution_forms(occupation, chamber, slope_rows):
    inv = inverse(chamber)
    offset = original_offset(occupation)
    variables = len(slope_rows[0])
    return tuple((dot(row, offset) - 1,) +
                 tuple(sum(row[j] * slope_rows[j][i] for j in range(3)) for i in range(variables))
                 for row in inv)


def validate_margins(rows, columns):
    if len(rows) != 4 or len(columns) != 5:
        raise ValueError("requires exactly four rows and five columns")
    if any(type(n) is not int for n in (*rows, *columns)):
        raise ValueError("margins must be integers, excluding booleans")
    if min(rows) < 0 or min(columns) <= 0 or sum(rows) != sum(columns):
        raise ValueError("nonnegative rows, positive columns, and balance required")


def whole_polynomial(rows, columns, atlas):
    """All 1024 labeled assignments, exact boundary continuation, all degrees.

    Returns a 13-entry numerator vector, denominator 12!, and assignment counts.
    This is an evaluator identity conditional on the stated chamber/lattice
    theorems and exact atlas binding. It imposes no positivity assertion.
    """
    rows, columns = tuple(rows), tuple(columns)
    validate_margins(rows, columns)
    perturbed_rows = tuple(1024 * r + d for r, d in zip(rows, ROW_PERTURBATION))
    perturbed_columns = tuple(1024 * c + d for c, d in zip(columns, COLUMN_PERTURBATION))
    return whole_polynomial_from_generic_margins(rows, columns, perturbed_rows, perturbed_columns, atlas)


def whole_polynomial_from_generic_margins(rows, columns, chamber_rows, chamber_columns, atlas):
    """Core contraction with caller-supplied generic positive selection margins.

    The root requested this seam for its separately proved zero-column boundary
    extension. This function does not itself establish that extension. It checks
    exact integrality, balance, positivity of the selection margins, all strict
    transportation cuts, and preservation of every nonzero original cut sign.
    The original margins may have zero columns or be the origin. All 1024
    assignments and the original offsets and slopes are retained as before.
    The default wrapper's positive-column contract remains unchanged.
    """
    rows, columns = tuple(rows), tuple(columns)
    perturbed_rows, perturbed_columns = tuple(chamber_rows), tuple(chamber_columns)
    if len(rows) != 4 or len(columns) != 5:
        raise ValueError("core requires four original rows and five original columns")
    if any(type(x) is not int or x < 0 for x in rows + columns) or sum(rows) != sum(columns):
        raise ValueError("original core margins must be balanced nonnegative integers")
    validate_margins(perturbed_rows, perturbed_columns)
    if min(perturbed_rows) <= 0:
        raise ValueError("selection rows must all be positive")
    for row_mask in range(1, 15):
        original_row_cut = sum(r for i, r in enumerate(rows) if row_mask & (1 << i))
        selected_row_cut = sum(r for i, r in enumerate(perturbed_rows) if row_mask & (1 << i))
        for column_mask in range(32):
            before = original_row_cut - sum(c for i, c in enumerate(columns) if column_mask & (1 << i))
            after = selected_row_cut - sum(c for i, c in enumerate(perturbed_columns) if column_mask & (1 << i))
            if not after or (before and before * after <= 0):
                raise ValueError("selection does not preserve and strictly resolve every full transportation cut")
    aggregate, cache = {}, {}
    supported = 0
    for assignment in product(range(4), repeat=5):
        occupation = tuple(assignment.count(i) for i in range(4))
        original = [-r for r in rows]
        perturbed = [-r for r in perturbed_rows]
        for j, i in enumerate(assignment):
            original[i] += columns[j]
            perturbed[i] += perturbed_columns[j]
        chamber = strict_chamber(simple_coordinates(perturbed))
        if chamber is None:
            continue
        supported += 1
        slope = simple_coordinates(original)
        cache_key = (occupation, chamber, slope)
        if cache_key not in cache:
            forms = substitution_forms(occupation, chamber, tuple((x,) for x in slope))
            coefficients = atlas[occupation_key(occupation)][chamber]
            cache[cache_key] = contract_newton(coefficients, forms)
        add_polynomial(aggregate, cache[cache_key], (-1) ** sum(assignment))
    if any(key > DEGREE for key in aggregate):
        raise ArithmeticError("univariate polynomial escaped the proven degree bound")
    return tuple(aggregate.get(i, 0) for i in range(DEGREE + 1)), {
        "assignments": 4 ** 5, "supported_assignments": supported,
        "distinct_substitutions": len(cache),
        "dimension": (sum(r > 0 for r in rows) - 1) * (sum(c > 0 for c in columns) - 1) if sum(rows) else 0,
        "selection": "caller-supplied positive generic margins with every transportation cut checked",
    }


def table_lr_lift(rows, columns):
    """Literal entire Hall-Cauchy lift, with the original labeled column order."""
    total = sum(rows)
    row_tails = [sum(rows[i:]) for i in range(1, 4)]
    column_tails = [sum(columns[j:]) for j in range(5)]
    return {"lambda": [total + x for x in row_tails] + column_tails,
            "mu": [total] * 3 + column_tails[1:], "nu": [total] + row_tails}


def family_margins(unit, parameter):
    if unit == 10:
        b, a, c_small, c_large = parameter
        return (5 * b - a - c_small - c_large, c_large, c_small, a), (b,) * 5
    b, a, c_small, c_large, d = parameter
    return (d, c_large, c_small, a), (a + c_small + c_large + d - 4 * b, b, b, b, b)


def family_dimension(unit, parameter):
    if not any(parameter):
        return 0
    rows, columns = family_margins(unit, parameter)
    if min(rows) < 0 or min(columns) < 0 or sum(rows) != sum(columns):
        raise ValueError("family parameter has illegal margins")
    return (sum(r > 0 for r in rows) - 1) * (sum(c > 0 for c in columns) - 1)


def primitive_ray(vertex):
    rational = (Fraction(1),) + tuple(Fraction(x) for x in vertex)
    denominator = lcm(*(x.denominator for x in rational))
    ray = tuple(int(x * denominator) for x in rational)
    if gcd(*ray) != 1:
        raise ArithmeticError("denominator clearing did not produce a primitive ray")
    return ray


def family_groups(unit):
    """Derive every group directly from the complete assignment identity."""
    if unit == 10:
        for n in compositions(5, 4):
            weight = factorial(5) // product_factorials(n)
            yield {"n": n, "weight": weight, "sign": (-1) ** sum(i * v for i, v in enumerate(n)),
                   "L": ((n[0] - 5, 1, 1, 1), (n[0] + n[1] - 5, 1, 1, 0), (-n[3], 1, 0, 0))}
    elif unit == 11:
        for occupation in compositions(4, 4):
            for distinguished in range(4):
                n = tuple(o + int(i == distinguished) for i, o in enumerate(occupation))
                beta = []
                for i in range(4):
                    linear = [occupation[i], 0, 0, 0, 0]
                    linear[4 - i] -= 1
                    if i == distinguished:
                        linear = [linear[0] - 4] + [x + 1 for x in linear[1:]]
                    beta.append(tuple(linear))
                slope = (beta[0], tuple(x + y for x, y in zip(beta[0], beta[1])), tuple(-x for x in beta[3]))
                yield {"o": occupation, "distinguished_class": distinguished, "n": n,
                       "weight": factorial(4) // product_factorials(occupation),
                       "sign": (-1) ** sum(i * v for i, v in enumerate(n)), "L": slope}
    else:
        raise ValueError("unit must be 10 or 11")


def product_factorials(values):
    result = 1
    for v in values:
        result *= factorial(v)
    return result


def contract_group(group, rays, center, atlas):
    chamber = strict_chamber(tuple(dot(row, center) for row in group["L"]))
    if chamber is None:
        return {}, None
    slope = tuple(tuple(dot(row, ray) for ray in rays) for row in group["L"])
    forms = substitution_forms(group["n"], chamber, slope)
    polynomial = contract_newton(atlas[occupation_key(group["n"])][chamber], forms)
    multiplier = group["sign"] * group["weight"]
    return {k: v * multiplier for k, v in polynomial.items()}, chamber
