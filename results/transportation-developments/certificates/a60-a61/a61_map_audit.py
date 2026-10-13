"""Accepted exact Cramer derivative and complete wall arithmetic."""
from fractions import Fraction
from itertools import permutations

def poly(rows):
    return {tuple(row['powers']): Fraction(row['coefficient']) for row in rows}

def determinant(matrix):
    total = 0
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        total += (-1) ** inversions * matrix[0][p[0]] * matrix[1][p[1]] \
                 * matrix[2][p[2]] * matrix[3][p[3]]
    return total

def direction(matrix, small, big):
    # Cramer's rule for A dz = e_small - e_big.  This does not use the
    # root probe's inverse matrix implementation.
    rhs = tuple(int(i == small) - int(i == big) for i in range(4))
    den = determinant(matrix)
    if not den:
        raise AssertionError('singular chamber matrix')
    return tuple(Fraction(determinant([[rhs[i] if j == col else matrix[i][j]
                                        for j in range(4)] for i in range(4)]), den)
                 for col in range(4))

def derivative(P, d):
    out = {}
    for powers, coefficient in P.items():
        for axis in range(4):
            if not powers[axis] or not d[axis]:
                continue
            exponent = list(powers)
            exponent[axis] -= 1
            exponent = tuple(exponent)
            out[exponent] = out.get(exponent, Fraction(0)) \
                            + coefficient * powers[axis] * d[axis]
    return {p: c for p, c in out.items() if c}

def rays(matrix):
    return [tuple(row[i] for row in matrix) for i in range(4)]

def restriction(P, included):
    omitted = set(range(4)) - set(included)
    return {tuple(p[i] for i in included): c for p, c in P.items()
            if all(p[i] == 0 for i in omitted)}
