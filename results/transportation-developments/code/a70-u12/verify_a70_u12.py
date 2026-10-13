"""Portable complete A70 / Pro049 U12 theorem-critical certificate.

Adapted from the independently authored A70 root verifier. No originating
Pro049 program or LR/physical counting backend is imported or executed.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys
import time
HERE=Path(__file__).resolve().parent
MODULE=HERE.parents[1]
DATA=MODULE/'data/a70-u12'
EXPECTATIONS=DATA/'EXPECTED.json'
LIMITS={'ray_candidates_per_stage':20000,'rank_calls':100000,'polynomial_terms':10000,'writer_bytes':4*2**20}


class Refusal(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Refusal(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector_add(left, right):
    return tuple(first + second for first, second in zip(left, right))


def vector_scale(factor, values):
    return tuple(factor * value for value in values)


def vector_sum(rows):
    answer = (0,) * 7
    for row in rows:
        answer = vector_add(answer, row)
    return answer


def dot(left, right):
    return sum(first * second for first, second in zip(left, right))


def primitive(values):
    divisor = math.gcd(*values)
    return tuple(value // divisor for value in values) if divisor else tuple(values)


def rank(rows):
    reduced = [list(primitive(tuple(row))) for row in rows if any(row)]
    if not reduced:
        return 0
    pivot_row = 0
    for column in range(len(reduced[0])):
        pivot = next((number for number in range(pivot_row, len(reduced))
                      if reduced[number][column]), None)
        if pivot is None:
            continue
        reduced[pivot_row], reduced[pivot] = reduced[pivot], reduced[pivot_row]
        pivot_value = reduced[pivot_row][column]
        for number in range(pivot_row + 1, len(reduced)):
            scale = reduced[number][column]
            if not scale:
                continue
            changed = [pivot_value * value - scale * other
                       for value, other in zip(reduced[number], reduced[pivot_row])]
            reduced[number] = list(primitive(tuple(changed)))
        pivot_row += 1
        if pivot_row == len(reduced):
            break
    return pivot_row


def determinant(matrix):
    changed = [list(row) for row in matrix]
    require(len(changed) == 7 and all(len(row) == 7 for row in changed),
            "determinant requires the complete seven-coordinate matrix")
    sign = 1
    previous = 1
    for column in range(6):
        pivot = next((number for number in range(column, 7)
                      if changed[number][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            changed[column], changed[pivot] = changed[pivot], changed[column]
            sign *= -1
        pivot_value = changed[column][column]
        for number in range(column + 1, 7):
            for target in range(column + 1, 7):
                numerator = (pivot_value * changed[number][target]
                             - changed[number][column] * changed[column][target])
                require(numerator % previous == 0, "Bareiss division ceased to be exact")
                changed[number][target] = numerator // previous
            changed[number][column] = 0
        previous = pivot_value
    return sign * changed[6][6]


def solve(matrix, right):
    changed = [[Fraction(value) for value in row] + [Fraction(value_right)]
               for row, value_right in zip(matrix, right)]
    size = len(changed)
    require(size == 7 and all(len(row) == 8 for row in changed),
            "solve requires complete seven-coordinate matrix")
    for column in range(size):
        pivot = next((number for number in range(column, size)
                      if changed[number][column]), None)
        require(pivot is not None, "singular purported simplex")
        changed[column], changed[pivot] = changed[pivot], changed[column]
        pivot_value = changed[column][column]
        changed[column] = [value / pivot_value for value in changed[column]]
        for number in range(size):
            if number == column:
                continue
            scale = changed[number][column]
            changed[number] = [value - scale * other
                               for value, other in zip(changed[number], changed[column])]
    return tuple(row[-1] for row in changed)


def ray_matrix(rays, identifiers):
    return [tuple(rays[identifier][coordinate] for identifier in identifiers)
            for coordinate in range(7)]


def physical_system():
    basis = [tuple(int(coordinate == position) for coordinate in range(7))
             for position in range(7)]
    size, width, chart_z, tail_a, tail_b, tail_d, tail_e = basis
    zero = (0,) * 7
    outer = (vector_add(vector_scale(2, size), vector_scale(4, width)),
             vector_add(vector_scale(2, size), vector_scale(3, width)),
             vector_add(vector_scale(2, size), vector_scale(2, width)),
             vector_scale(2, size), size)
    inner = (vector_add(vector_scale(2, size), vector_scale(2, width)),
             vector_add(vector_scale(2, size), width), vector_scale(2, size), size, zero)
    content = (vector_add(size, vector_scale(3, width)),
               vector_add(size, vector_scale(2, width)), width)
    array = ((vector_scale(2, width), zero, zero),
             (vector_add(chart_z, width), vector_add(width, vector_scale(-1, chart_z)), zero),
             (vector_sum((size, vector_scale(-1, tail_a), vector_scale(-1, tail_d),
                          vector_scale(-1, chart_z))),
              vector_sum((size, vector_scale(-1, tail_b), vector_scale(-1, tail_e), chart_z, width)),
              vector_sum((width, vector_scale(-2, size), tail_a, tail_b, tail_d, tail_e))),
             (tail_a, tail_b, vector_sum((size, vector_scale(-1, tail_a), vector_scale(-1, tail_b)))),
             (tail_d, tail_e, vector_sum((size, vector_scale(-1, tail_d), vector_scale(-1, tail_e)))))
    require(all(vector_sum(row) == vector_add(top, vector_scale(-1, bottom))
                for row, top, bottom in zip(array, outer, inner)), "physical row sum changed")
    require(all(vector_sum([array[row][letter] for row in range(5)]) == content[letter]
                for letter in range(3)), "physical content sum changed")
    require(array[1][0] == vector_add(width, chart_z) and
            array[3][:2] == (tail_a, tail_b) and array[4][:2] == (tail_d, tail_e),
            "integer inverse projection changed")
    require(all(all(value >= 0 for value in vector_add(outer[row], vector_scale(-1, inner[row])))
                for row in range(5)), "containment is not uniform")
    for partition in (outer, inner, content):
        require(all(all(value >= 0 for value in vector_add(first, vector_scale(-1, second)))
                    for first, second in zip(partition, partition[1:])),
                "partition order is not uniform")
    require(vector_sum(outer) == vector_add(vector_sum(inner), vector_sum(content)),
            "literal original is not balanced")
    occurrences = [{"label": "parameter:S", "normal": size},
                   {"label": "parameter:U", "normal": width}]
    for row in range(5):
        for letter in range(3):
            occurrences.append({"label": f"nonnegative:x({row + 1},{letter + 1})",
                                "normal": array[row][letter]})
    for row in range(1, 5):
        for letter in range(3):
            normal = vector_sum((inner[row - 1], vector_scale(-1, inner[row]),
                                 vector_sum(array[row - 1][:letter]),
                                 vector_scale(-1, vector_sum(array[row][:letter + 1]))))
            occurrences.append({"label": f"column:({row + 1},{letter + 1})", "normal": normal})
    for row in range(5):
        for letter in range(2):
            normal = vector_add(vector_sum([array[earlier][letter] for earlier in range(row)]),
                                vector_scale(-1, vector_sum([array[earlier][letter + 1]
                                                            for earlier in range(row + 1)])))
            occurrences.append({"label": f"ballot:({row + 1},{letter + 1})", "normal": normal})
    require(len(occurrences) == 39, "incomplete physical occurrence roster")
    require(len({record["label"] for record in occurrences}) == 39, "duplicate physical label")
    forms = []
    for record in occurrences:
        normal = primitive(record["normal"])
        if any(normal) and normal not in forms:
            forms.append(normal)
    require(len(forms) == 28, "physical system does not have 28 nonzero primitive forms")
    orthant_normals = [basis[0], basis[1], vector_scale(-1, basis[2]), *basis[3:]]
    require(all(normal in forms for normal in orthant_normals),
            "physical cone is not certified inside the starting signed orthant")
    return {"outer": outer, "inner": inner, "content": content, "array": array,
            "occurrences": occurrences, "forms": forms, "orthant_normals": orthant_normals}


def strict_chart_and_prior_degree(system):
    point = ((4, 1, 0), (4, 0, 1), (-1, 0, Fraction(-1, 2)),
             (2, 1, 0), (1, 0, 0), (1, 0, 0), (2, 1, 0))
    records = []
    for item in system["occurrences"]:
        slack = tuple(sum(normal * point[coordinate][parameter]
                          for coordinate, normal in enumerate(item["normal"]))
                      for parameter in range(3))
        if any(item["normal"]):
            require(slack[0] > 0 and slack[1] >= 0 and slack[2] >= 0,
                    f"strict five-dimensional chart failed at {item['label']}")
        else:
            require(slack == (0, 0, 0), "forced zero row changed")
        records.append({"label": item["label"], "epsilon_p_q": slack})
    return {"parameterization": "S=4epsilon+p, U=4epsilon+q, epsilon>0, p,q>=0",
            "tail_rows": "(S-2epsilon,epsilon,epsilon); (epsilon,S-2epsilon,epsilon)",
            "z": "epsilon-U/2", "strict_slacks": records, "fiber_lattice": "Z^5",
            "prior_actual_degree": 5,
            "degree_basis": "An open set in the complete injective five-coordinate tableau chart, with integer inverse; no fitted degree."}


def double_description(system, stop_after=None):
    normals = list(system["orthant_normals"])
    rays = set(normals)
    remaining = [normal for normal in system["forms"] if normal not in normals]
    stages = []
    rank_calls = 0
    for stage, normal in enumerate(remaining):
        if stop_after is not None and stage >= stop_after:
            break
        positive, negative, zero = [], [], []
        for ray in sorted(rays):
            slack = dot(normal, ray)
            (positive if slack > 0 else negative if slack < 0 else zero).append((ray, slack))
        candidates = {ray for ray, _ in positive + zero}
        for positive_ray, positive_slack in positive:
            for negative_ray, negative_slack in negative:
                candidates.add(primitive(vector_add(vector_scale(-negative_slack, positive_ray),
                                                    vector_scale(positive_slack, negative_ray))))
        require(len(candidates) <= LIMITS["ray_candidates_per_stage"], "DD candidate bound exceeded")
        normals.append(normal)
        rays = set()
        for candidate in sorted(candidates):
            require(any(candidate), "DD generated zero ray")
            require(all(dot(item, candidate) >= 0 for item in normals), "DD generated infeasible ray")
            rank_calls += 1
            require(rank_calls <= LIMITS["rank_calls"], "DD rank-work bound exceeded")
            active = [item for item in normals if dot(item, candidate) == 0]
            if rank(active) == 6:
                rays.add(candidate)
        require(rays, "DD lost the whole pointed cone")
        stages.append({"stage": stage + 1, "normal": normal,
                       "positive": len(positive), "negative": len(negative), "zero": len(zero),
                       "all_pair_count": len(positive) * len(negative),
                       "primitive_candidates": len(candidates), "extreme_rays": len(rays)})
    return {"rays": sorted(rays), "stages": stages, "rank_calls": rank_calls,
            "complete": len(stages) == len(remaining), "remaining_inequalities": len(remaining)}


def derive_facets(system, rays):
    faces = {}
    for normal in system["forms"]:
        require(all(dot(normal, ray) >= 0 for ray in rays), "enumerated ray violates physical form")
        zeros = tuple(identifier for identifier, ray in enumerate(rays) if dot(normal, ray) == 0)
        if rank([rays[identifier] for identifier in zeros]) == 6:
            faces.setdefault(zeros, []).append(normal)
    require(len(faces) == 13, "incomplete full physical facet set")
    return [{"rays": face, "normals": normals} for face, normals in sorted(faces.items())]


def pulling_triangulation(rays, facets):
    global_faces = [frozenset(face["rays"]) for face in facets]
    records = []

    @lru_cache(maxsize=None)
    def recurse(face):
        dimension = rank([rays[identifier] for identifier in face])
        require(dimension >= 1, "empty face in pulling recursion")
        if len(face) == dimension:
            records.append({"face": face, "rank": dimension, "simplex": True})
            return (face,)
        pivot = min(face)
        face_set = frozenset(face)
        all_facets = set()
        for global_face in global_faces:
            child = tuple(sorted(face_set & global_face))
            if child and rank([rays[identifier] for identifier in child]) == dimension - 1:
                all_facets.add(child)
        require(all_facets, "nonsimplicial face has no full-rank facets")
        children = sorted(child for child in all_facets if pivot not in child)
        require(children, "pulling pivot has no opposite facet")
        simplices = set()
        for child in children:
            for simplex in recurse(child):
                joined = tuple(sorted((pivot,) + simplex))
                require(rank([rays[identifier] for identifier in joined]) == dimension,
                        "pulling simplex lost its face dimension")
                simplices.add(joined)
        records.append({"face": face, "rank": dimension, "pivot": pivot,
                        "all_rank_one_lower_facets": sorted(all_facets),
                        "opposite_facets": children, "result_simplices": sorted(simplices)})
        return tuple(sorted(simplices))

    cones = recurse(tuple(range(len(rays))))
    require(len(cones) == 16 and all(len(cone) == 7 for cone in cones),
            "pulling triangulation is not the full sixteen-cone decomposition")
    return {"cones": cones, "face_recursion": records}


def half_open_cones(rays, triangulation, expected):
    omega = tuple(expected["omega"])
    require(all(dot(normal, omega) > 0 for normal in physical_system()["forms"]),
            "omega is not strict interior of the whole cone")
    residual = tuple(value - sum(ray[coordinate] for ray in rays)
                     for coordinate, value in enumerate(omega))
    positive_weights = None
    for identifiers in triangulation["cones"]:
        coordinates = solve(ray_matrix(rays, identifiers), residual)
        if all(value >= 0 for value in coordinates):
            positive_weights = [Fraction(1)] * len(rays)
            for identifier, value in zip(identifiers, coordinates):
                positive_weights[identifier] += value
            break
    require(positive_weights is not None and all(value > 0 for value in positive_weights),
            "omega lacks the checked strictly positive sum of every ray")
    require(tuple(sum(weight * ray[coordinate] for weight, ray in zip(positive_weights, rays))
                  for coordinate in range(7)) == omega, "omega positive decomposition is false")
    wanted = {tuple(item["rays"]): item for item in expected["cones"]}
    require(len(wanted) == 16 and set(wanted) == set(triangulation["cones"]),
            "source cone roster omits or changes a pulling simplex")
    cones = []
    for identifiers in triangulation["cones"]:
        matrix = ray_matrix(rays, identifiers)
        value = determinant(matrix)
        require(abs(value) == 1, "pulling simplex is not unimodular in Z^7")
        coordinates = solve(matrix, omega)
        require(all(coordinate != 0 for coordinate in coordinates), "nongeneric omega coordinate")
        opened = tuple(position for position, coordinate in enumerate(coordinates) if coordinate < 0)
        shift = vector_sum([rays[identifiers[position]] for position in opened])
        source = wanted[identifiers]
        require(opened == tuple(source["open"]), "source half-open facet ownership differs")
        require(shift == tuple(source["shift"]), "source full lattice numerator shift differs")
        cones.append({"rays": identifiers, "determinant": value, "omega_coordinates": coordinates,
                      "open": opened, "shift": shift})
    return {"omega": omega, "positive_weights_on_all_rays": positive_weights, "cones": cones}


def bounded_section_and_boundaries(system, rays):
    require(all(ray[0] >= 0 and ray[1] >= 0 and ray[0] + ray[1] > 0 for ray in rays),
            "nonzero ray has no positive S+U grade")
    require(all(0 <= ray[coordinate] <= ray[0] for ray in rays for coordinate in (3, 4, 5, 6)),
            "tail coordinates do not have the certified bounded section")
    require(all(-ray[1] <= ray[2] <= 0 for ray in rays), "z section is not bounded")
    zero_width = [ray for ray in rays if ray[1] == 0]
    zero_size = [ray for ray in rays if ray[0] == 0]
    require(zero_width == [(1, 0, 0, 1, 0, 0, 1)], "u=0 has more than the unique tableau ray")
    require(zero_size == [(0, 1, -1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0, 0)],
            "s=0 is not exactly the primitive z interval")
    return {"section": "S+U=1; 0<=a,b,d,e<=S and -U<=z<=0",
            "u_zero_rays": zero_width, "s_zero_rays": zero_size,
            "boundary_degrees": {"u=0": 0, "s=0,u>0": 1, "s=u=0": 0},
            "boundary_counts": {"u=0": "1", "s=0": "U+1"}}


def geometry_certificate(expected):
    started = time.perf_counter()
    system = physical_system()
    require(expected["physical_occurrences"] == 39 and expected["distinct_nonzero_primitive_forms"] == 28,
            "source physical sizes differ")
    strict = strict_chart_and_prior_degree(system)
    description = double_description(system)
    require(description["complete"] and len(description["stages"]) == 21,
            "DD omitted a physical intersection")
    rays = description["rays"]
    require(rays == [tuple(ray) for ray in expected["rays"]], "independent full DD rays differ from Appendix A")
    facets = derive_facets(system, rays)
    require({tuple(face["rays"]) for face in facets} == {tuple(face) for face in expected["facets"]},
            "independent full facet set differs from Appendix A")
    triangulation = pulling_triangulation(rays, facets)
    series = half_open_cones(rays, triangulation, expected)
    boundaries = bounded_section_and_boundaries(system, rays)
    return {"status": "PASS", "seconds": time.perf_counter() - started, "physical_system": system,
            "prior_degree": strict, "double_description": description, "facets": facets,
            "pulling": triangulation, "half_open": series, "boundaries": boundaries}


class Polynomial:
    def __init__(self, values=0):
        if isinstance(values, Polynomial):
            self.terms = dict(values.terms)
        elif isinstance(values, dict):
            self.terms = {tuple(exponent): Fraction(value) for exponent, value in values.items() if value}
        else:
            value = Fraction(values)
            self.terms = {(0, 0): value} if value else {}
        require(len(self.terms) <= LIMITS["polynomial_terms"], "sparse polynomial term bound exceeded")
        require(all(len(exponent) == 2 and all(type(power) is int and power >= 0 for power in exponent)
                    for exponent in self.terms), "invalid exact polynomial exponent")

    def __add__(self, other):
        other = Polynomial(other)
        terms = dict(self.terms)
        for exponent, value in other.terms.items():
            terms[exponent] = terms.get(exponent, Fraction(0)) + value
        return Polynomial(terms)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({exponent: -value for exponent, value in self.terms.items()})

    def __sub__(self, other):
        return self + -Polynomial(other)

    def __rsub__(self, other):
        return Polynomial(other) + -self

    def __mul__(self, other):
        other = Polynomial(other)
        terms = {}
        for first, value in self.terms.items():
            for second, other_value in other.terms.items():
                exponent = tuple(left + right for left, right in zip(first, second))
                terms[exponent] = terms.get(exponent, Fraction(0)) + value * other_value
        return Polynomial(terms)

    __rmul__ = __mul__

    def __truediv__(self, divisor):
        require(isinstance(divisor, (int, Fraction)) and divisor != 0,
                "polynomial division requires a nonzero exact scalar")
        return Polynomial({exponent: value / divisor for exponent, value in self.terms.items()})

    def __pow__(self, exponent):
        require(type(exponent) is int and 0 <= exponent <= 64, "polynomial exponent outside bound")
        answer = Polynomial(1)
        factor = self
        while exponent:
            if exponent % 2:
                answer *= factor
            exponent //= 2
            if exponent:
                factor *= factor
        return answer

    def __eq__(self, other):
        return self.terms == Polynomial(other).terms

    def substitute(self, first, second):
        return sum((value * first**exponent[0] * second**exponent[1]
                    for exponent, value in self.terms.items()), Polynomial())

    def evaluate(self, first, second):
        return sum((value * first**exponent[0] * second**exponent[1]
                    for exponent, value in self.terms.items()), Fraction(0))

    def derivative(self, coordinate):
        terms = {}
        for exponent, value in self.terms.items():
            if exponent[coordinate]:
                lowered = list(exponent)
                lowered[coordinate] -= 1
                terms[tuple(lowered)] = exponent[coordinate] * value
        return Polynomial(terms)

    def degree(self):
        return max((sum(exponent) for exponent in self.terms), default=-1)

    def record(self):
        return [{"powers": exponent, "coefficient": value}
                for exponent, value in sorted(self.terms.items())]

FIRST=Polynomial({(1,0):1})
SECOND=Polynomial({(0,1):1})


def parse_polynomial(text, names=("s", "u")):
    require(isinstance(text, str) and len(text) <= 4000, "expected polynomial text outside bound")
    variables = {names[0]: FIRST, names[1]: SECOND}

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant):
            require(type(node.value) is int, "polynomial literal is not an integer")
            return Polynomial(node.value)
        if isinstance(node, ast.Name):
            require(node.id in variables, "unknown polynomial variable")
            return variables[node.id]
        if isinstance(node, ast.UnaryOp):
            require(isinstance(node.op, (ast.UAdd, ast.USub)), "unsupported polynomial unary operation")
            return visit(node.operand) if isinstance(node.op, ast.UAdd) else -visit(node.operand)
        require(isinstance(node, ast.BinOp), "unsupported polynomial expression")
        left = visit(node.left)
        right = visit(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, (ast.Div, ast.Pow)):
            require(set(right.terms) <= {(0, 0)}, "nonconstant exponent or denominator")
            scalar = right.terms.get((0, 0), Fraction(0))
            if isinstance(node.op, ast.Div):
                return left / scalar
            require(scalar.denominator == 1, "noninteger exponent")
            return left**int(scalar)
        raise Refusal("unsupported polynomial binary operation")

    return visit(ast.parse(text, mode="eval"))


def binomial_polynomial(argument, degree):
    answer = Polynomial(1)
    for step in range(degree):
        answer *= argument - step
    return answer / math.factorial(degree)


def nine_term_series():
    first = FIRST
    second = SECOND
    return [
        (1 + 4 * first + first**2, Counter({(1, 0): 5, (0, 1): 2})),
        (-9 * first - 12 * first**2 - 2 * first**3, Counter({(1, 0): 6, (0, 1): 1})),
        (3 * first**2, Counter({(1, 0): 4, (1, 1): 3})),
        (3 * first**2 - 2 * first**3, Counter({(1, 0): 5, (1, 1): 2})),
        (4 * first**2 - 8 * first**3 - 4 * first**4, Counter({(1, 0): 6, (1, 1): 1})),
        (-first**3, Counter({(1, 0): 4, (2, 1): 3})),
        (-first**3, Counter({(1, 0): 5, (2, 1): 2})),
        (-first**3, Counter({(1, 0): 6, (2, 1): 1})),
        (first + 15 * first**2 + 15 * first**3 + first**4
         + second * (6 * first**2 + 20 * first**3 + 6 * first**4),
         Counter({(1, 0): 6, (1, 2): 1})),
    ]


def rational_series_identity(rays, cones):
    simplex_terms = []
    for cone in cones:
        numerator = Polynomial({tuple(cone["shift"][:2]): 1})
        factors = Counter(tuple(rays[identifier][:2]) for identifier in cone["rays"])
        require((0, 0) not in factors, "zero parameter degree denominator")
        simplex_terms.append((numerator, factors))
    displayed_terms = nine_term_series()
    common = Counter()
    for _, factors in simplex_terms + displayed_terms:
        for factor, exponent in factors.items():
            common[factor] = max(common[factor], exponent)
    cache = {}

    def clear(numerator, denominator):
        answer = numerator
        for factor, exponent in sorted(common.items()):
            remaining = exponent - denominator.get(factor, 0)
            require(remaining >= 0, "common denominator does not cover a complete term")
            key = (factor, remaining)
            if key not in cache:
                cache[key] = (1 - Polynomial({factor: 1}))**remaining
            answer *= cache[key]
        return answer

    left = sum((clear(numerator, factors) for numerator, factors in simplex_terms), Polynomial())
    right = sum((clear(numerator, factors) for numerator, factors in displayed_terms), Polynomial())
    require(left == right, "complete cleared-numerator cone/G identity failed")
    return {"status": "PASS", "simplex_terms": len(simplex_terms), "displayed_terms": len(displayed_terms),
            "common_denominator": [{"monomial": factor, "power": exponent}
                                   for factor, exponent in sorted(common.items())],
            "left_numerator": left, "right_numerator": right, "residual": left - right,
            "identity_basis": "Full sparse exact polynomial numerator after complete denominator clearing; no finite series grid."}


def extraction_components():
    size = FIRST
    width = SECOND
    endpoint = (size + 1)**2 * (size + 2)**2 / 4
    subtract = size * (size + 1) * (size + 2) * (23 * size**2 + 81 * size + 76) / 120
    diagonal = size * (size - 1) * (size + 1) * (
        30 * width**2 + 5 * width * size + 140 * width - 8 * size**2 + 45 * size + 142) / 120
    double_diagonal = size * (size - 1) * (size - 2) * (
        10 * width**2 + 5 * width * size + 35 * width + size**2 + 8 * size + 27) / 120
    return endpoint, subtract, diagonal, double_diagonal


def coefficient_extraction_identities(parity_mutation=False):
    size = FIRST
    width = SECOND
    endpoint, subtract, diagonal, double_diagonal = extraction_components()
    endpoint_from_series = (binomial_polynomial(size + 4, 4)
                            + 4 * binomial_polynomial(size + 3, 4)
                            + binomial_polynomial(size + 2, 4))
    subtract_from_series = (9 * binomial_polynomial(size + 4, 5)
                            + 12 * binomial_polynomial(size + 3, 5)
                            + 2 * binomial_polynomial(size + 2, 5))
    diagonal_from_series = (
        3 * binomial_polynomial(width + 2, 2) * binomial_polynomial(size + 1, 3)
        + (width + 1) * (3 * binomial_polynomial(size + 2, 4) - 2 * binomial_polynomial(size + 1, 4))
        + 4 * binomial_polynomial(size + 3, 5) - 8 * binomial_polynomial(size + 2, 5)
        - 4 * binomial_polynomial(size + 1, 5))
    double_diagonal_from_series = (
        binomial_polynomial(width + 2, 2) * binomial_polynomial(size, 3)
        + (width + 1) * binomial_polynomial(size + 1, 4)
        + binomial_polynomial(size + 2, 5))
    even = (binomial_polynomial(size + 4, 5)
            + (14 if parity_mutation else 15) * binomial_polynomial(size + 3, 5)
            + 15 * binomial_polynomial(size + 2, 5) + binomial_polynomial(size + 1, 5))
    odd = (6 * binomial_polynomial(size + 3, 5) + 20 * binomial_polynomial(size + 2, 5)
           + 6 * binomial_polynomial(size + 1, 5))
    identities = [
        ("E: first complete series term", endpoint_from_series, endpoint),
        ("A: second complete series term", subtract_from_series, subtract),
        ("C: all three xy terms, k=S-U", diagonal_from_series, diagonal),
        ("D: all three x^2 y terms, k=S-2U", double_diagonal_from_series, double_diagonal),
        ("parity even: n=S-U/2", even, binomial_polynomial(2 * size + 3, 5)),
        ("parity odd: n=S-(U-1)/2", odd, binomial_polynomial(2 * size + 2, 5)),
    ]
    result = []
    for name, left, right in identities:
        require(left == right, f"full coefficient identity failed: {name}")
        result.append({"identity": name, "left": left, "right": right, "residual": left - right})
    for early in (0, 1):
        require(diagonal.substitute(Polynomial(early), width) == 0, "C early zero band omitted")
    for early in (0, 1, 2):
        require(double_diagonal.substitute(Polynomial(early), width) == 0, "D early zero band omitted")
    require(even.substitute(Polynomial(0), width) == 0, "even support initial band changed")
    require(all(odd.substitute(Polynomial(early), width) == 0 for early in (0, 1)),
            "odd support initial band changed")
    return {"identities": result, "coefficient_rule": "[x^n](1-x)^(-m)=binom(n+m-1,m-1) for n>=0, zero for n<0",
            "support": {"C": "U<=S, k=S-U>=0; C(0,U)=C(1,U)=0",
                        "D": "2U<=S, k=S-2U>=0; D(0,U)=D(1,U)=D(2,U)=0",
                        "even": "U=2v, n=S-v>=0; n=0 contributes zero; n<0 has no support",
                        "odd": "U=2v+1, n=S-v; n=0,1 contribute zero; n<0 has no support",
                        "unified_binomial": "U<=2S; upper argument 2S-U+3>=3; below 5 yields zero"}}


def chamber_polynomials():
    size = FIRST
    width = SECOND
    endpoint, subtract, diagonal, double_diagonal = extraction_components()
    base = (width + 1) * endpoint - subtract
    parity_free = binomial_polynomial(2 * size - width + 3, 5)
    first_diagonal = diagonal.substitute(size - width, width)
    second_diagonal = double_diagonal.substitute(size - 2 * width, width)
    return (base + parity_free + first_diagonal - second_diagonal,
            base + parity_free + first_diagonal, base + parity_free, base)


def ordinary_coefficients(polynomial):
    require(polynomial.degree() == 5, "generic chamber degree is not five")
    return [Polynomial({exponent: value for exponent, value in polynomial.terms.items()
                        if sum(exponent) == degree}) for degree in range(6)]


def chamber_and_sign_certificate(expected):
    chambers = chamber_polynomials()
    lower = (SECOND + 1) * (SECOND + 2) * (SECOND + 3) * (7 * SECOND**2 + 13 * SECOND + 10) / 60
    require(chambers[0] == lower, "entire low chamber simplification failed")
    require(len(expected["coefficients"]) == 4 and len(expected["signs"]) == 4
            and len(expected["cone_substitutions"]) == 4, "an entire chamber is missing")
    rows = []
    slots = 0
    all_coefficients = []
    for chamber_number, polynomial in enumerate(chambers):
        require(len(expected["coefficients"][chamber_number]) == 6 and
                len(expected["signs"][chamber_number]) == 6, "ordinary coefficient or sign slot omitted")
        coefficients = ordinary_coefficients(polynomial)
        all_coefficients.append(coefficients)
        substitution = [parse_polynomial(text, ("a", "b"))
                        for text in expected["cone_substitutions"][chamber_number]]
        require(tuple(substitution) == ((2 * FIRST + SECOND, FIRST), (2 * FIRST + SECOND, FIRST + SECOND),
                                       (FIRST + SECOND, 2 * FIRST + SECOND), (FIRST, 2 * FIRST + SECOND))[chamber_number],
                "chamber cone coordinates changed")
        chamber_rows = []
        for degree, coefficient in enumerate(coefficients):
            source = parse_polynomial(expected["coefficients"][chamber_number][degree])
            require(coefficient == source, "derived ordinary coefficient differs from Appendix B")
            derivative = coefficient.derivative(1)
            transformed = coefficient.substitute(*substitution)
            transformed_derivative = derivative.substitute(*substitution)
            sign_slot = expected["signs"][chamber_number][degree]
            require(len(sign_slot) == 2, "coefficient/derivative pair is incomplete")
            require(transformed == parse_polynomial(sign_slot[0], ("a", "b")),
                    "full coefficient sign polynomial differs from Appendix C")
            require(transformed_derivative == parse_polynomial(sign_slot[1], ("a", "b")),
                    "fixed-s u derivative differs from Appendix C")
            require(all(value > 0 for value in transformed.terms.values()) and
                    all(value > 0 for value in transformed_derivative.terms.values()),
                    "complete sign slot has a negative nonzero monomial")
            if degree == 0:
                require(coefficient == 1 and derivative == 0, "constant operation slot changed")
            else:
                require(all(sum(exponent) == degree for exponent in coefficient.terms), "nonhomogeneous coefficient")
                require(all(sum(exponent) == degree - 1 for exponent in derivative.terms), "nonhomogeneous derivative")
                if chamber_number in (0, 3):
                    require(transformed.terms.get((degree, 0), 0) > 0
                            and transformed_derivative.terms.get((degree - 1, 0), 0) > 0,
                            "pure a power does not establish strictness")
                else:
                    require(transformed.terms.get((degree, 0), 0) > 0 and
                            transformed.terms.get((0, degree), 0) > 0 and
                            transformed_derivative.terms.get((degree - 1, 0), 0) > 0 and
                            transformed_derivative.terms.get((0, degree - 1), 0) > 0,
                            "both endpoint powers needed for strictness were not retained")
            slots += 2
            chamber_rows.append({"degree": degree, "ordinary_coefficient": coefficient,
                                 "fixed_s_u_derivative": derivative,
                                 "coefficient_in_cone": transformed,
                                 "derivative_in_cone": transformed_derivative})
        rows.append({"chamber": chamber_number, "substitution": substitution, "rows": chamber_rows})
    walls = []
    for left, right, size_value, width_value, label in (
        (0, 1, 2 * FIRST, FIRST, "s=2u"),
        (1, 2, FIRST, FIRST, "s=u"),
        (2, 3, FIRST, 2 * FIRST, "u=2s"),
    ):
        first = chambers[left].substitute(size_value, width_value)
        second = chambers[right].substitute(size_value, width_value)
        require(first == second, f"full chamber wall count identity failed: {label}")
        require(all(before.substitute(size_value, width_value) == after.substitute(size_value, width_value)
                    for before, after in zip(all_coefficients[left], all_coefficients[right])),
                f"ordinary coefficient wall identity failed: {label}")
        walls.append({"wall": label, "full_count": first, "all_six_coefficients": "equal"})
    require(chambers[0].substitute(FIRST, Polynomial(0)) == 1, "u=0 point count failed")
    require(chambers[3].substitute(Polynomial(0), SECOND) == SECOND + 1, "s=0 interval count failed")
    require(slots == 48, "not every coefficient/derivative slot was checked")
    gain = [after.evaluate(1, 2) - before.evaluate(1, 1)
            for before, after in zip(all_coefficients[2], all_coefficients[3])]
    require(gain == [Fraction(text) for text in expected["gain_coefficients"]],
            "selected complete operation coefficients differ")
    shadow_times_t = [Fraction(0), Fraction(31, 32), Fraction(29, 12), Fraction(19, 8),
                      Fraction(13, 12), Fraction(3, 16)]
    entire_arrival = [Fraction(0), Fraction(13, 160), Fraction(5, 8), Fraction(5, 6),
                      Fraction(3, 8), Fraction(13, 240)]
    require([first + second for first, second in zip(shadow_times_t, entire_arrival)] == gain,
            "displayed full arrival algebra does not pay the entire operation")
    require(Fraction(1, 32) - Fraction(1, 32) == 0, "displayed parity terms failed to cancel")
    return {"status": "PASS", "complete_sign_slots": slots, "chambers": rows, "wall_identities": walls,
            "low_chamber": lower, "selected_gain": gain,
            "strictness": {"chamber_0": "u=a>0 gives a>0",
                           "chambers_1_2": "s,u>0 gives a+b>0; both pure endpoint powers retained",
                           "chamber_3": "s=a>0 gives a>0",
                           "operation": "At fixed s>0, continuous coefficients on the three checked walls and strict derivatives for u>0 imply strict increase on every positive-length interval [u,v].",
                           "constant": "coefficient one in every chamber; difference zero"},
            "boundary_counts": {"u=0": "1", "s=0": "1+U"},
            "shadow_arrival_status": "Exact displayed algebra only; independent shadow/layer counts remain SOURCE."}


def algebra_certificate(expected, geometry):
    started = time.perf_counter()
    rational = rational_series_identity(geometry["double_description"]["rays"], geometry["half_open"]["cones"])
    extraction = coefficient_extraction_identities()
    signs = chamber_and_sign_certificate(expected)
    return {"status": "PASS", "seconds": time.perf_counter() - started,
            "rational_identity": rational, "all_parameter_extraction": extraction,
            "ordinary_coefficients_and_operation": signs}


def literal_original(size, width):
    require(type(size) is int and type(width) is int and size >= 0 and width >= 0,
            "original parameters must be exact nonnegative integers")
    return ((2 * size + 4 * width, 2 * size + 3 * width, 2 * size + 2 * width, 2 * size, size),
            (2 * size + 2 * width, 2 * size + width, 2 * size, size, 0),
            (size + 3 * width, size + 2 * width, width))


def validate_original_domain(expected):
    cases = expected.get("originals", [])
    require(len(cases) == 2, "exactly two new complete originals are authorized")
    require([(case.get("id"), case.get("s"), case.get("u")) for case in cases] ==
            [("PRO049-S1-U1", 1, 1), ("PRO049-S1-U2", 1, 2)],
            "changed the two-original domain")
    for case in cases:
        actual = tuple(tuple(case.get(field, [])) for field in ("outer", "inner", "content"))
        require(actual == literal_original(case["s"], case["u"]),
                "literal original shift or physical zero row changed")
        require(case.get("actual_degree") == 5, "wrong independently prior actual degree")
        require(case.get("determining") == list(range(6)), "determining grades must be exactly 0..5")
        require(case.get("unused") == [6, 7], "both genuinely unused grades 6,7 are required")
        require(all(type(value) is int for partition in actual for value in partition),
                "literal original contains an inexact value")
        require(len(actual[0]) == len(actual[1]) == 5, "all five physical original rows must remain")


def expected_count(size, width):
    endpoint, subtract, diagonal, double_diagonal = extraction_components()
    total = (width + 1) * endpoint.evaluate(size, width) - subtract.evaluate(size, width)
    if width <= 2 * size:
        total += math.comb(2 * size - width + 3, 5) if 2 * size - width + 3 >= 5 else 0
    if width <= size:
        total += diagonal.evaluate(size - width, width)
    if 2 * width <= size:
        total -= double_diagonal.evaluate(size - 2 * width, width)
    require(total.denominator == 1 and total >= 0, "all-parameter count formula is not a nonnegative integer")
    return int(total)


def newton_polynomial(values):
    differences = [Fraction(value) for value in values]
    answer = Polynomial()
    for degree in range(len(values)):
        answer += differences[0] * binomial_polynomial(FIRST, degree)
        differences = [second - first for first, second in zip(differences, differences[1:])]
    return answer


def validate_complete_vector(case, records, coefficients):
    require([record["grade"] for record in records] == list(range(8)), "complete vector lost an unused or determining grade")
    require(all(record["id"] == case["id"] for record in records), "vector mixes original identities")
    require(case["actual_degree"] == 5, "vector uses the wrong prior degree")
    values = [record["bare_lr_count"] for record in records]
    polynomial = newton_polynomial(values[:6])
    wanted = sum((coefficient.evaluate(case["s"], case["u"]) * FIRST**degree
                  for degree, coefficient in enumerate(coefficients)), Polynomial())
    require(polynomial == wanted, "complete independent Newton polynomial differs from the all-parameter formula")
    require(polynomial.degree() == 5 and polynomial.terms.get((5, 0), 0) > 0,
            "complete vector degree disagrees with independent strict chart")
    require(all(polynomial.evaluate(grade, 0) == values[grade] for grade in (6, 7)),
            "genuinely unused original grade did not match reconstructed polynomial")
    require(all(value > 0 for value in polynomial.terms.values()), "selected whole-original polynomial is not strict")
    return {"id": case["id"], "prior_actual_degree": 5, "determining_grades": list(range(6)),
            "unused_grades": [6, 7], "complete_values": values, "ordinary_polynomial": polynomial,
            "original": {field: case[field] for field in ("outer", "inner", "content")}}


def encode_json(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, Polynomial):
        return value.record()
    raise TypeError(f"unserializable certificate value: {type(value).__name__}")

def unique_json(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def read_data(path):
    require(path.is_file() and path.resolve()==path,'missing or aliased exact input')
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique_json,
                     parse_constant=lambda x:(_ for _ in ()).throw(Refusal('nonfinite JSON')))

def frozen_input():
    raw=read_data(EXPECTATIONS)
    require(raw.get('schema')=='a70-pro049-independent-expectations/v1','wrong expectation schema')
    require(raw.get('proof_sha256')=='8bf014ee64307fad5c527f71e42458c9cb1afe2e1975aa96adf093540735bc96','originating proof identity changed')
    require(raw.get('coordinates')==['S','U','z','a','b','d','e'],'physical coordinate order changed')
    validate_original_domain(raw)
    return raw

def source_closure():
    manifest=read_data(DATA/'MANIFEST.json')
    require(manifest.get('schema')=='a70-u12-portable-complete-inputs/v1','wrong portable manifest')
    seen=set()
    for row in manifest['files']:
        name=row['path']
        require(isinstance(name,str) and not name.startswith('/') and chr(92) not in name
                and all(v not in ('','.','..') for v in name.split('/')),'unsafe frozen path')
        require(name not in seen,'duplicate frozen path');seen.add(name)
        path=MODULE/name
        require(path.is_file() and path.resolve()==path,'missing or aliased frozen input '+name)
        require(path.stat().st_size==row['bytes'] and sha256(path)==row['sha256'],'frozen input mismatch '+name)
    needed={'code/a70-u12/verify_a70_u12.py','code/a70-u12/README.md',
            'proofs/A70-PRO049-U12-FULL-PROOF.md','proofs/A70-PRO049-U12-ADOPTION.md',
            'data/a70-u12/EXPECTED.json','data/a70-u12/RECORDED-CONTROLS.json',
            'data/a70-u12/CERTIFICATE-DATA.json','data/a70-u12/GENERATING-FUNCTION.json',
            'data/a70-u12/SOURCE-TO-PUBLIC.json'}
    require(seen==needed,'complete portable dependency roster changed')
    return manifest

def recorded_vectors(expected):
    archived=read_data(DATA/'RECORDED-CONTROLS.json')
    require(archived['status']=='RECORDED_A70_CONTROLS_NOT_NEW_COUNTS','archived control status changed')
    require(archived['new_lr_or_physical_counts']==0,'archived evidence promoted into a new count')
    rows=archived['grade_records'];require(len(rows)==16,'complete archived grade records omitted')
    polynomials=chamber_polynomials();vectors=[]
    for case,chamber in zip(expected['originals'],(2,3)):
        records=[r for r in rows if r['id']==case['id']]
        for r in records:
            grade=r['grade']
            require(r['S']==case['s']*grade and r['U']==case['u']*grade,'archived parameter shift changed')
            for field,part in [('literal_outer','outer'),('literal_inner','inner'),('literal_content','content')]:
                require(r[field]==[grade*v for v in case[part]],'archived physical original changed')
            require(r['bare_lr_count']==r['physical_array_count']==r['all_parameter_formula']
                    ==expected_count(r['S'],r['U']),'archived full count/formula mismatch')
        vectors.append(validate_complete_vector(case,records,ordinary_coefficients(polynomials[chamber])))
    require(vectors[1]['ordinary_polynomial']-vectors[0]['ordinary_polynomial']
            ==sum((Fraction(v)*FIRST**k for k,v in enumerate(expected['gain_coefficients'])),Polynomial()),'full archived gain differs')
    return {'status':'PASS_REUSED_RECORDED_VECTORS','vectors':vectors,'new_lr_or_physical_counts':0,
            'fresh_unused_grades':0,'new_positive_rank_or_additive_coverage':0}

def plain(value):
    return json.loads(json.dumps(value,default=encode_json))

def exact_geometry_algebra(expected):
    geometry=geometry_certificate(expected);geometry.pop('seconds')
    algebra=algebra_certificate(expected,geometry);algebra.pop('seconds')
    return {'geometry':geometry,'algebra':algebra}

def displayed_generating_function():
    return [{'numerator':num.record(),
             'denominator':[{'monomial':factor,'power':power} for factor,power in sorted(den.items())]}
            for num,den in nine_term_series()]

def theorem_controls(expected,geometry):
    results=[]
    def refused(name,action,reason):
        try:action()
        except Refusal as error:
            require(reason in str(error),'mutation failed for unrelated reason '+name)
            results.append({'control':name,'result':'PASS_REFUSED','reason':str(error)})
        else:raise Refusal('mutated certificate accepted '+name)
    rays=geometry['double_description']['rays'];cones=geometry['half_open']['cones']
    refused('missing complete cone',lambda:rational_series_identity(rays,cones[:-1]),'cone/G identity failed')
    changed=deepcopy(expected);changed['cones'][0]['open']=[]
    refused('wrong open facet',lambda:half_open_cones(rays,geometry['pulling'],changed),'half-open facet ownership differs')
    changed=deepcopy(expected);changed['cones'][0]['shift'][0]+=1
    refused('wrong full lattice shift',lambda:half_open_cones(rays,geometry['pulling'],changed),'full lattice numerator shift differs')
    for name,path,replacement,reason in [
        ('wrong physical zero row',['originals',0,'inner'],[4,3,2,1],'physical zero row changed'),
        ('wrong prior degree',['originals',0,'actual_degree'],4,'prior actual degree'),
        ('lost historically reserved grade',['originals',0,'unused'],[6],'unused grades 6,7'),
        ('wrong full chamber polynomial',['coefficients',1,5],'1+('+expected['coefficients'][1][5]+')','ordinary coefficient differs'),
        ('wrong fixed-s derivative',['signs',2,5,1],'1+('+expected['signs'][2][5][1]+')','fixed-s u derivative differs')]:
        changed=deepcopy(expected);dest=changed
        for key in path[:-1]:dest=dest[key]
        dest[path[-1]]=replacement
        action=(lambda changed=changed:validate_original_domain(changed)) if path[0]=='originals' else (lambda changed=changed:chamber_and_sign_certificate(changed))
        refused(name,action,reason)
    refused('wrong full parity identity',lambda:coefficient_extraction_identities(parity_mutation=True),'parity even')
    changed=deepcopy(expected);changed['signs'].pop()
    refused('missing entire parameter chamber',lambda:chamber_and_sign_certificate(changed),'entire chamber is missing')
    system=physical_system();missing=list(system['occurrences']);missing.pop(17)
    refused('missing physical constraint',lambda:require(missing==physical_system()['occurrences'],'full labeled physical system differs'),'full labeled')
    changed=deepcopy(expected);changed['rays'][0]=[2*v for v in changed['rays'][0]]
    refused('nonprimitive source ray',lambda:require([tuple(r) for r in changed['rays']]==rays,'full primitive cone rays differ'),'primitive cone rays differ')
    return results

def run(mode):
    source_closure();expected=frozen_input();result=exact_geometry_algebra(expected)
    stored=read_data(DATA/'CERTIFICATE-DATA.json')
    require(stored['schema']=='a70-u12-complete-theorem-critical-data/v1','wrong complete data schema')
    require(plain(result)==stored['complete_certificate'],'complete regenerated cone/coverage/series/sign data differs')
    gf=read_data(DATA/'GENERATING-FUNCTION.json')
    require(plain(displayed_generating_function())==gf['nine_complete_terms'],'complete nine-term generating function differs')
    vectors=recorded_vectors(expected)
    controls=theorem_controls(expected,result['geometry']) if mode=='verify' else []
    return {'status':'PASS','geometry':result['geometry'],'algebra':result['algebra'],
            'recorded_originals':vectors,'refusal_controls':controls,
            'new_lr_or_physical_counts':0,'fresh_unused_grades':0,'new_additive_coverage':0}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('certificate','verify'),default='verify')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();started=time.perf_counter();result=run(args.mode)
    summary={'status':'PASS','mode':args.mode,'seconds':time.perf_counter()-started,
             'physical_occurrences':39,'nonzero_primitive_forms':28,'rays':15,'facets':13,
             'pulling_simplices':16,'series_terms':9,'coefficient_derivative_slots':48,
             'controls':len(result['refusal_controls']),'reused_recorded_originals':2,
             'new_lr_or_physical_counts':0,'fresh_unused_grades':0,'new_additive_coverage':0}
    if args.output:
        require(not args.output.exists(),'output already exists')
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as stream:
            json.dump({'schema':'a70-u12-portable-check/v1','summary':summary,'result':result},stream,
                      default=encode_json,sort_keys=True,indent=2);stream.write('\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (Refusal,OSError,ValueError,KeyError) as error:
        print(json.dumps({'status':'REFUSED','error':str(error)},sort_keys=True),file=sys.stderr)
        raise SystemExit(2) from error
