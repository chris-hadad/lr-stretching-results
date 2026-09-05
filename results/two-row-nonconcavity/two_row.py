"""Independent exact two-row counts and ordinary coefficients (stdlib only)."""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial


def require(ok, message):
    if not ok:
        raise ValueError(message)


def domain(beta, v, w):
    require(len(beta) >= 2 and all(type(x) is int and x >= 0 for x in beta),
            "nonnegative integer weights, at least two entries")
    require(type(v) is int and type(w) is int and 0 <= w <= v,
            "integer 0 <= w <= v")
    total = sum(beta)
    require(2*v <= total and max(beta) <= total-w, "feasible two-row domain")


def count(beta, v, w, t):
    """Positive bounded-composition DP, followed by Jacobi--Trudi subtraction."""
    domain(beta, v, w)
    require(type(t) is int and t >= 0, "nonnegative integer stretch")
    limit = v*t
    values = [1]+[0]*limit
    for weight in beta:
        cap = weight*t
        following, window = [], 0
        for j, value in enumerate(values):
            window += value
            if j > cap:
                window -= values[j-cap-1]
            following.append(window)
        values = following
    result = values[limit]-(values[w*t-1] if w*t else 0)
    require(result >= 0, "negative two-row count")
    return result


def pieri(beta, v, w, t):
    """Positive two-row horizontal-strip chain, with no slice subtraction."""
    domain(beta, v, w)
    require(type(t) is int and t >= 0, "nonnegative integer stretch")
    top = (sum(beta)-w)*t
    bottom = v*t
    size = (v-w)*t
    states = {0: 1}
    for weight in beta:
        added = weight*t
        following = defaultdict(int)
        for old_bottom, multiplicity in states.items():
            old_top = size-old_bottom
            low = max(old_bottom, size+added-top)
            high = min(bottom, old_top, old_bottom+added)
            for new_bottom in range(low, high+1):
                following[new_bottom] += multiplicity
        states = following
        size += added
    return states.get(bottom, 0)


def subset_counts(beta):
    groups = {(0, 0): 1}
    for value in beta:
        following = dict(groups)
        for (size, total), multiplicity in groups.items():
            key = size+1, total+value
            following[key] = following.get(key, 0)+multiplicity
        groups = following
    return groups


def binomial_polynomial(slope, offset, degree):
    coefficients = [1]
    for j in range(degree):
        following = [0]*(len(coefficients)+1)
        for k, value in enumerate(coefficients):
            following[k] += (offset-j)*value
            following[k+1] += slope*value
        coefficients = following
    divisor = factorial(degree)
    return [F(value, divisor) for value in coefficients]


def coefficients(beta, v, w):
    domain(beta, v, w)
    degree = len(beta)-1
    output = [F(v == 0)]+[F(0)]*degree
    for (size, total), multiplicity in subset_counts(beta).items():
        sign = (-1)**size*multiplicity
        for target, offset, multiplier in ((v, degree-size, sign),
                                            (w, degree-1-size, -sign)):
            if total < target:
                term = binomial_polynomial(target-total, offset, degree)
                for j, value in enumerate(term):
                    output[j] += multiplier*value
    return output


def quadratic(beta, v, w):
    domain(beta, v, w)
    d = len(beta)-1
    harmonic = [F(0)]
    for j in range(1, d+1):
        harmonic.append(harmonic[-1]+F(1, j))
    result = F(v*v, 2)*(harmonic[d]**2-sum(F(1, j*j) for j in range(1, d+1)))
    for (s, total), multiplicity in subset_counts(beta).items():
        if 1 <= s <= d and total < v:
            result -= multiplicity*(v-total)**2*(harmonic[d-s]-harmonic[s-1])/(s*comb(d, s))
        if s <= d-1 and total < w:
            result -= multiplicity*(w-total)**2*(harmonic[d-1-s]-harmonic[s])/((d-s)*comb(d, s))
    return result


def evaluate(coefficients, t):
    result = F(0)
    for value in reversed(coefficients):
        result = result*t+F(value)
    return result


def embedded_triple(row_lengths, target):
    """Disjoint rows with consecutive, nonoverlapping column intervals."""
    outer, inner, running = [], [], 0
    for width in reversed(row_lengths):
        require(type(width) is int and width >= 0, "nonnegative row length")
        inner.append(running)
        running += width
        outer.append(running)
    return ([x for x in reversed(outer) if x],
            [x for x in reversed(inner) if x], list(target))


def reproduce():
    fixture_values = 0
    gaps = 0
    for k in range(2, 11):
        for scale, xs in ((2, (0, 1, 2)), (3, (1, 2, 3))):
            C = scale*(k+1)
            rows = []
            for x in xs:
                beta = (C-k*x, C-x)+ (x,)*(k+1)
                expected = binomial_polynomial(x, k, k)
                actual = coefficients(beta, C, C)
                require(actual == expected+[F(0)]*(len(actual)-len(expected)), "symbolic identity")
                require(quadratic(beta, C, C) == expected[2], "quadratic identity")
                for t in range(k+5):
                    a, b = count(beta, C, C, t), pieri(beta, C, C, t)
                    require(a == b == comb(x*t+k, k), "independent count identity")
                    fixture_values += 1
                rows.append(expected)
            for j in range(2, k+1):
                require(rows[1][j]-(rows[0][j]+rows[2][j])/2 < 0, "strict concavity gap")
                gaps += 1
    # Endpoint and zero-weight coverage for the general skew formula.
    endpoint_values = 0
    for beta in ((0, 0), (1, 1), (2, 0, 3), (1, 2, 3, 0), (4, 1, 1), (2, 2, 2, 2)):
        W = sum(beta)
        for v in range(W//2+1):
            for w in range(min(v, W-max(beta))+1):
                cs = coefficients(beta, v, w)
                require(quadratic(beta, v, w) == (cs[2] if len(cs)>2 else 0), "harmonic formula")
                for t in range(len(beta)+2):
                    require(evaluate(cs, t) == count(beta, v, w, t) == pieri(beta, v, w, t), "endpoint")
                    endpoint_values += 1
    require(embedded_triple((4, 5, 1, 1, 1), (6, 6)) ==
            ([12, 8, 3, 2, 1], [8, 3, 2, 1], [6, 6]), "ordinary LR embedding")
    return {"status": "PASS", "family_count_checks": fixture_values,
            "negative_midpoint_gaps": gaps, "endpoint_count_checks": endpoint_values,
            "negative_ordinary_coefficients": 0, "coverage_added": 0}


if __name__ == "__main__":
    import json
    print(json.dumps(reproduce(), sort_keys=True))
