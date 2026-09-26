"""Unchanged exact arithmetic from the campaign-owned independent transport checker.
Private packet/harness/source-history interfaces are excluded.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial
import hashlib
import json
import re
import time

class CheckError(ValueError):
    pass


class Refused(Exception):
    pass


def need(test, message):
    if not test:
        raise CheckError(message)


def integer(value):
    if type(value) is str and re.fullmatch(r"-?(0|[1-9][0-9]*)", value):
        value = int(value)
    need(type(value) is int, "Boolean, float or malformed integer")
    return value


def rational(value):
    need(type(value) in (int, str), "Expected an exact rational")
    if type(value) is str:
        need(re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", value), "Malformed rational")
    return Q(value)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Budget:
    def __init__(self, seconds=90, max_work=50000000):
        need(0 < seconds <= 110 and integer(max_work) > 0, "Invalid work/deadline cap")
        self.end = time.monotonic() + seconds
        self.max_work = max_work
        self.work = 0

    def tick(self, work=1):
        self.work += work
        if self.work > self.max_work or time.monotonic() >= self.end:
            raise Refused("Exact count incomplete at the frozen time/work cap")


def group_key(big, small, equal):
    return f"B{big}:S{small}:E" + ",".join(map(str, equal))


def assignment_groups(repeated=5):
    """Group a fresh literal enumeration, retaining every labelled assignment.

    Labels follow column order (large, distinguished small, repeated smalls).
    This enumeration does not use the provider's grouped IDs or multiplicities.
    """
    need(0 <= integer(repeated) <= 5, "Repeated-column population outside this bounded checker")
    groups = {}
    for labels in product(range(3), repeat=2 + repeated):
        big, small = labels[:2]
        equal = tuple(labels[2:].count(i) for i in range(3))
        key = group_key(big, small, equal)
        if key not in groups:
            n = [equal[i] + int(big == i) + int(small == i) for i in range(3)]
            groups[key] = {"id": key, "big": big, "small": small, "equal": list(equal),
                           "occupation": n, "sign": (-1) ** n[1], "labels": []}
        groups[key]["labels"].append("".join(map(str, labels)))
    result = []
    for key in sorted(groups):
        group = groups[key]
        group["weight"] = len(group["labels"])
        need(group["weight"] == factorial(repeated) //
             (factorial(group["equal"][0]) * factorial(group["equal"][1]) * factorial(group["equal"][2])),
             "Literal labels disagree with exact multinomial multiplicity")
        result.append(group)
    return result


def margins(u, v):
    u, v = integer(u), integer(v)
    need(u >= 1 and v >= 0, "Scalar margins require integer u >= 1 and v >= 0")
    return [7 * u + v, 5 * u, 4 * u, u], [4 * u + v, 3 * u] + [2 * u] * 5


def assignment_targets(group, rows, columns, grade):
    grade = integer(grade)
    need(grade >= 0 and len(rows) == 4 and len(columns) == 2 + sum(group["equal"])
         and sum(rows) == sum(columns) and min(rows) >= 0, "Invalid complete table margins")
    need(len(set(columns[2:])) <= 1, "Repeated columns have different margins")
    need(min(columns) >= rows[-1], "Class-4 exclusion has not been proved for these margins")
    repeated_margin = columns[2] if len(columns) > 2 else 0
    C = [repeated_margin * group["equal"][i] + columns[0] * int(group["big"] == i)
         + columns[1] * int(group["small"] == i) for i in range(3)]
    a, b, c = group["occupation"]
    return {"column_sums": C, "targets": [grade * (C[0] - rows[0]) - b - c,
                                            grade * (rows[2] + rows[3] - C[2]) - 2 * c,
                                            grade * rows[3]]}


def B(m, y):
    """Complete weak-composition count, including the zero-occupation stratum."""
    if y < 0:
        return 0
    return int(y == 0) if m == 0 else comb(y + m - 1, m - 1)


class AssignmentCounter:
    def __init__(self, budget):
        self.budget = budget
        self.cache = {}
        self.compositions = {}

    def b(self, m, y):
        key = m, y
        if key not in self.compositions:
            self.compositions[key] = B(m, y)
        return self.compositions[key]

    def a2(self, a, b, c, U, V):
        if U < 0 or V < 0:
            return 0
        key = a, b, c, U, V
        if key not in self.cache:
            total = 0
            for diagonal in range(min(U, V) + 1):
                self.budget.tick()
                total += self.b(a + c, diagonal) * self.b(a + b, U - diagonal) * self.b(b + c, V - diagonal)
            self.cache[key] = total
        return self.cache[key]

    def count(self, occupation, targets):
        self.budget.tick()
        a, b, c = occupation
        X, Y, Z = targets
        if min(X, Y, Z) < 0:
            return 0
        total = 0
        for y1 in range(min(X, Y, Z) + 1):
            for y2 in range(min(Z - y1, Y - y1) + 1):
                self.budget.tick()
                weight = self.b(a, y1) * self.b(b, y2) * self.b(c, Z - y1 - y2)
                if weight:
                    total += weight * self.a2(a, b, c, X - y1, Y - y1 - y2)
        return total


def bare_family(h):
    bare = {"lambda_outer": [27 + h, 22 + h, 18 + h, 17 + h, 13, 10, 8, 6, 4, 2],
            "mu": [17 + h] * 3 + [13, 10, 8, 6, 4, 2], "nu": [17 + h, 10, 5, 1]}
    need(all(part == sorted(part, reverse=True) and min(part) > 0 for part in bare.values())
         and sum(bare["lambda_outer"]) == 127 + 4 * h == sum(bare["mu"]) + sum(bare["nu"]), "Tail lift is not a balanced positive partition triple")
    return bare


def greedy_table(rows, columns):
    """Construct an integer table from nonnegative equal-total margins."""
    need(all(integer(x) >= 0 for x in rows + columns) and sum(rows) == sum(columns), "Infeasible nonnegative margins")
    left, right = list(rows), list(columns)
    table = [[0] * len(columns) for _ in rows]
    for i in range(len(rows)):
        for j in range(len(columns)):
            value = min(left[i], right[j])
            table[i][j] = value
            left[i] -= value
            right[j] -= value
    need(not any(left + right), "Incomplete constructive transport witness")
    return table


def chart_table(rows, columns, free):
    """Literal full-matrix integer chart and subtraction inverse."""
    nr, nc = len(rows), len(columns)
    need(sum(rows) == sum(columns) and len(free) == (nr - 1) * (nc - 1), "Wrong free chart dimension")
    table = [[0] * nc for _ in range(nr)]
    for i in range(nr - 1):
        for j in range(nc - 1):
            table[i][j] = free[i * (nc - 1) + j]
        table[i][-1] = rows[i] - sum(table[i][:-1])
    for j in range(nc):
        table[-1][j] = columns[j] - sum(table[i][j] for i in range(nr - 1))
    need([sum(row) for row in table] == rows, "Chart failed the complete row equations")
    return table


def geometry(h):
    rows, columns = margins(1, h)
    total = sum(rows)
    interior = [[Q(r * c, total) for c in columns] for r in rows]
    free = [interior[i][j] for i in range(3) for j in range(6)]
    need(chart_table(rows, columns, free) == interior and all(x > 0 for row in interior for x in row), "Missing full-dimensional rational interior")
    # The free entries are literal coordinate selections, hence the integer
    # chart has an integer inverse. Every incidence column has one +1 and one
    # -1 on a bipartite edge: the standard network TU theorem applies.
    incidence = [[int(i == r) - int(i == 4 + c) for r in range(4) for c in range(7)] for i in range(11)]
    need(all(sorted(incidence[i][j] for i in range(11)) == [-1] + [0] * 9 + [1] for j in range(28)), "Not a complete network incidence matrix")
    residual_rows = [7 * r - 7 for r in rows]
    residual_columns = [7 * c - 4 for c in columns]
    witness = [[x + 1 for x in row] for row in greedy_table(residual_rows, residual_columns)]
    need([sum(row) for row in witness] == [7 * r for r in rows]
         and [sum(row[j] for row in witness) for j in range(7)] == [7 * c for c in columns], "Codegree witness has wrong margins")
    return {"dimension": 18, "free_cells": [[i, j] for i in range(3) for j in range(6)],
            "lattice": "Z18 with literal integer coordinate inverse", "positive_rational_table": [[str(x) for x in row] for row in interior],
            "network_incidence_sha256": sha(encoded(incidence)), "integral_vertices_premise": "Bipartite network incidence total unimodularity",
            "codegree": 7, "lower_bound": "The unit row needs seven strictly positive integer entries, so t >= 7.",
            "grade_7_strict_integer_witness": witness, "known_roots": list(range(-6, 0)), "constant": "1",
            "root_premise": "Ehrhart reciprocity for the complete integral dimension-18 transportation polytope"}


def multiply(a, b):
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def evaluate(poly, x):
    result = Q(0)
    for value in reversed(poly):
        result = result * x + value
    return result


def interpolate(nodes):
    need(nodes and len({x for x, _ in nodes}) == len(nodes), "Repeated or empty interpolation sites")
    # Solve the exact Vandermonde system. This is independent of the source's
    # Lagrange/Newton implementations and uses only the supplied whole counts.
    size = len(nodes)
    matrix = [[Q(x) ** j for j in range(size)] + [Q(y)] for x, y in nodes]
    for col in range(size):
        pivot = next((i for i in range(col, size) if matrix[i][col]), None)
        need(pivot is not None, "Singular determining system")
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [v / scale for v in matrix[col]]
        for i in range(size):
            if i != col and matrix[i][col]:
                scale = matrix[i][col]
                matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[col])]
    return [row[-1] for row in matrix]


def reconstruct(values, degree=18, roots=tuple(range(-6, 0))):
    factor = [Q(1)]
    for root in roots:
        factor = multiply(factor, [-root, 1])
    sites = list(range(degree - len(roots) + 1))
    need(set(values) == set(sites), "Determining count roster missing or extra")
    quotient = interpolate([(x, Q(values[x]) / evaluate(factor, x)) for x in sites])
    return multiply(factor, quotient)


def final_shell(degree=18):
    result = [Q(1)]
    for k in range(degree):
        result = multiply(result, [k, 1])
    return [x / factorial(degree) for x in result]


def node_id(h, grade):
    return f"TF-{h}:t{grade}"


def family_nodes():
    return [{"id": node_id(h, grade), "h": h, "u": 1, "v": h, "grade": grade,
             "role": "determining" if grade <= 12 else "unused_hold"} for h in range(7) for grade in range(1, 15)]
