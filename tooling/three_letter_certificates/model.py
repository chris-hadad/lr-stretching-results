"""Complete six-row, three-letter LR model in the original integer lattice.

An inequality is b + A*x >= 0. No positivity
of ordinary coefficients, vertex integrality, or full dimension is assumed.
"""

from itertools import product

FREE = ((2, 2), (3, 2), (4, 2), (5, 2), (3, 3), (4, 3), (5, 3))
DIMENSION = 7


class WorkLimit(ValueError):
    pass


def partition(values, size):
    p = tuple(values)
    if len(p) > size or any(type(x) is not int or x < 0 for x in p):
        raise ValueError("Expected bounded-length nonnegative integer partition")
    if any(a < b for a, b in zip(p, p[1:])):
        raise ValueError("Partition must be weakly decreasing")
    return p + (0,) * (size - len(p))


def const(c):
    return (c,) + (0,) * DIMENSION


def plus(*terms):
    return tuple(sum(t[k] for t in terms) for k in range(DIMENSION + 1))


def neg(term):
    return tuple(-x for x in term)


def model(outer, inner, content):
    la, mu, nu = partition(outer, 6), partition(inner, 6), partition(content, 3)
    if sum(la) != sum(mu) + sum(nu):
        raise ValueError("Unbalanced LR boundary")
    d = tuple(a - b for a, b in zip(la, mu))
    a = {(i, j): const(0) for i in range(1, 7) for j in range(1, 4)}
    for k, ij in enumerate(FREE):
        a[ij] = (0,) + tuple(int(h == k) for h in range(DIMENSION))
    a[6, 2] = plus(const(nu[1]), *(neg(a[i, 2]) for i in range(2, 6)))
    a[6, 3] = plus(const(nu[2]), *(neg(a[i, 3]) for i in range(3, 6)))
    for i in range(1, 7):
        a[i, 1] = plus(const(d[i - 1]), neg(a[i, 2]), neg(a[i, 3]))
    inequalities = []

    def add(label, expression):
        inequalities.append({"label": label, "b": expression[0], "A": expression[1:]})

    for i in range(1, 7):
        for j in range(1, min(i, 3) + 1):
            add(f"nonnegative({i},{j})", a[i, j])
    for i in range(2, 7):
        for j in range(1, 4):
            add(
                f"column({i},{j})",
                plus(const(mu[i - 2] - mu[i - 1]),
                     *(a[i - 1, k] for k in range(1, j)),
                     *(neg(a[i, k]) for k in range(1, j + 1))),
            )
    for i in range(1, 7):
        for j in range(1, 3):
            add(
                f"word({i},{j})",
                plus(*(a[r, j] for r in range(1, i)),
                     *(neg(a[r, j + 1]) for r in range(1, i + 1))),
            )
    return {"outer": la, "inner": mu, "content": nu, "row_lengths": d,
            "entries": a, "inequalities": inequalities, "free": FREE}


def evaluate(expression, coordinates):
    return expression[0] + sum(a * x for a, x in zip(expression[1:], coordinates))


def restore(data, coordinates):
    x = tuple(coordinates)
    if len(x) != DIMENSION:
        raise ValueError("Expected all seven coordinates")
    return {ij: evaluate(expr, x) for ij, expr in data["entries"].items()}


def feasible(data, coordinates):
    x = tuple(coordinates)
    if len(x) != DIMENSION:
        raise ValueError("Expected all seven coordinates")
    return all(row["b"] + sum(a * z for a, z in zip(row["A"], x)) >= 0
               for row in data["inequalities"])


def integer_count(outer, inner, content, *, max_nodes=2_000_000, return_points=False):
    """Exact bounded DFS in all seven original coordinates, with inequality pruning.

    The node limit includes failed partial assignments; exhaustion raises before
    any result is returned. No child process or file is created by this function.
    """
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")
    data = model(outer, inner, content)
    if any(d < 0 for d in data["row_lengths"]):
        return {"count": 0, "nodes": 0, "points": [] if return_points else None}
    bounds = [min(data["row_lengths"][i - 1], data["content"][j - 1]) for i, j in FREE]
    rows = data["inequalities"]
    suffix = [[sum(max(0, a) * bounds[k] for k, a in enumerate(row["A"]) if k >= level)
               for row in rows] for level in range(DIMENSION + 1)]
    nodes, count, points = 0, 0, []

    def visit(level, x, slacks):
        nonlocal nodes, count
        nodes += 1
        if nodes > max_nodes:
            raise WorkLimit("Integer-point node limit exceeded; no complete count")
        if any(value + suffix[level][r] < 0 for r, value in enumerate(slacks)):
            return
        if level == DIMENSION:
            count += 1
            if return_points:
                points.append(tuple(x))
            return
        for z in range(bounds[level] + 1):
            visit(level + 1, x + [z], [v + row["A"][level] * z for v, row in zip(slacks, rows)])

    visit(0, [], [row["b"] for row in rows])
    return {"count": count, "nodes": nodes, "points": points if return_points else None}


def normal_roster():
    """Every original row, grouping only identical oriented normal vectors.

    Multiple offsets at an identical normal are retained. Zero normal rows
    are explicit boundary inequalities, not silently discarded constraints.
    """
    data = model((0,) * 6, (0,) * 6, (0,) * 3)
    grouped, zero = {}, []
    for row in data["inequalities"]:
        n = tuple(-v for v in row["A"])
        if not any(n):
            zero.append(row["label"])
        else:
            grouped.setdefault(n, []).append(row["label"])
    return {"dimension": DIMENSION,
            "normals": [{"normal": n, "labels": labels} for n, labels in sorted(grouped.items())],
            "zero_rows": zero, "original_row_count": len(data["inequalities"])}
