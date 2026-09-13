"""Root-derived full hive boundary-mask implications and integer identifications."""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations

from slr_ehrhart.hive import hive_linear_system, interior_points, rhombus_terms


@lru_cache(None)
def model(n):
    if n not in (6, 7):
        raise ValueError('Only the frozen rank-six/seven domain is admitted')
    points = [(i, j) for i in range(n + 1) for j in range(n + 1 - i)]
    index = {p: i for i, p in enumerate(points)}
    rows = []
    for terms in rhombus_terms(n):
        row = [0] * len(points)
        for p, sign in terms:
            row[index[p]] += sign
        rows.append(tuple(row))
    sums = defaultdict(list)
    for k, row in enumerate(rows):
        sums[row].append(1 << k)
    for i, j in combinations(range(len(rows)), 2):
        sums[tuple(a + b for a, b in zip(rows[i], rows[j]))].append((1 << i) | (1 << j))
    rules = []
    for masks in sums.values():
        union = 0
        for mask in masks:
            union |= mask
        for mask in masks:
            if mask != union:
                rules.append((mask, union))
    gaps = []
    for side in range(3):
        edge = ([(0, i) for i in range(n + 1)] if side == 0 else
                [(i, 0) for i in range(n + 1)] if side == 1 else
                [(n - i, i) for i in range(n + 1)])
        for k in range(1, n):
            row = [0] * len(points)
            row[index[edge[k]]] = 2
            row[index[edge[k - 1]]] -= 1
            row[index[edge[k + 1]]] -= 1
            candidates = sums.get(tuple(row), [])
            if len(candidates) != 1 or candidates[0].bit_count() != 2:
                raise ValueError('Boundary gap has no unique complete two-rhombus identity')
            gaps.append(candidates[0])
    A, B, dim = hive_linear_system(n)
    sparse = [tuple((i, x) for i, x in enumerate(row) if x) for row in A]
    return {'points': points, 'full_rows': rows, 'rules': sorted(set(rules)), 'gaps': gaps,
            'A': A, 'B': B, 'sparse': sparse, 'dimension': dim}


def closure(mask, m):
    z = 0
    while mask:
        bit = mask & -mask
        z |= m['gaps'][bit.bit_length() - 1]
        mask ^= bit
    while True:
        previous = z
        for premise, conclusion in m['rules']:
            if z & premise == premise:
                z |= conclusion
        if z == previous:
            return z


def identifications(closed, m):
    """Eliminate only coefficient-one coordinates/differences; record every step."""
    dim = m['dimension']
    parent = list(range(dim + 1))
    words = []
    active = [i for i in range(len(m['sparse'])) if closed & (1 << i)]
    def find(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    while True:
        changed = False
        for row_id in active:
            reduced = {}
            for i, a in m['sparse'][row_id]:
                q = find(i)
                if q != find(dim):
                    reduced[q] = reduced.get(q, 0) + a
            reduced = {i: a for i, a in reduced.items() if a}
            if len(reduced) == 1 and abs(next(iter(reduced.values()))) == 1:
                x, coefficient = next(iter(reduced.items()))
                y = find(dim)
            elif len(reduced) == 2 and sorted(reduced.values()) == [-1, 1]:
                x, y = sorted(reduced)
                coefficient = reduced[x]
            else:
                continue
            words.append({'row': row_id, 'eliminated': x, 'kept': y, 'coefficient': coefficient})
            parent[x] = y
            changed = True
        if not changed:
            break
    ground = find(dim)
    components = [find(i) for i in range(dim)]
    for row_id in active:
        reduced = {}
        for i, a in m['sparse'][row_id]:
            q = find(i)
            if q != ground:
                reduced[q] = reduced.get(q, 0) + a
        if any(reduced.values()):
            raise ValueError('Forced equations do not admit the asserted complete identification chart')
    free = sorted(set(components) - {ground})
    return free, components, ground, words


def boundary_mask(lam, mu, nu, n):
    ans = 0
    for s, p in enumerate((lam, mu, nu)):
        q = tuple(p) + (0,) * (n - len(p))
        if len(q) != n or any(x < 0 for x in q) or any(a < b for a, b in zip(q, q[1:])):
            raise ValueError('Invalid padded partition')
        for i in range(n - 1):
            if q[i] == q[i + 1]:
                ans |= 1 << (s * (n - 1) + i)
    return ans


def reverse_bits(mask, n):
    return int(f'{mask:0{n}b}'[::-1], 2)


def images(mask, n):
    width = n - 1
    full = (1 << width) - 1
    L, M, N = mask & full, (mask >> width) & full, mask >> (2 * width)
    weights = (M, N, reverse_bits(L, width))
    result = set()
    for dual in (False, True):
        w = tuple(reverse_bits(a, width) for a in weights) if dual else weights
        for outer in range(3):
            others = [i for i in range(3) if i != outer]
            for i, j in (others, others[::-1]):
                result.add(reverse_bits(w[outer], width) | (w[i] << width) | (w[j] << (2 * width)))
    return result


def whole_chart(lam, mu, nu, n, closed=None):
    """Exact all-stretch chart from original forced rows, including boundary contradictions."""
    m = model(n)
    b = [*lam, *mu, *nu]
    if len(b) != 3 * n or sum(lam) != sum(mu) + sum(nu):
        raise ValueError('Invalid full boundary')
    if closed is None:
        closed = closure(boundary_mask(lam, mu, nu, n), m)
    free, components, ground, words = identifications(closed, m)
    # Replay the unit eliminations numerically at t=1; every constant scales by t.
    dim = m['dimension']
    offset = [0] * dim
    coefficient = [[int(i == j) for j in range(dim)] for i in range(dim)]
    remaining = list(range(dim))
    for word in words:
        row_id, original_pivot = word['row'], word['eliminated']
        p = remaining.index(original_pivot)
        old_a = m['A'][row_id]
        a = [sum(old_a[i] * coefficient[i][j] for i in range(dim)) for j in range(len(remaining))]
        c = sum(x * y for x, y in zip(m['B'][row_id], b)) + sum(old_a[i] * offset[i] for i in range(dim))
        pivot = a[p]
        if abs(pivot) != 1:
            raise ValueError('Nonunit recorded pivot')
        replacement = [-x // pivot for x in a]
        replacement[p] = 0
        shift = -c // pivot
        for i in range(dim):
            factor = coefficient[i][p]
            offset[i] += factor * shift
            coefficient[i] = [x + factor * y for x, y in zip(coefficient[i], replacement)]
            coefficient[i].pop(p)
        remaining.pop(p)
    if remaining != free:
        raise ValueError('Direction and affine replay selected different coordinates')
    for j, i in enumerate(free):
        if offset[i] != 0 or coefficient[i] != [int(k == j) for k in range(len(free))]:
            raise ValueError('Missing coordinate-selection inverse')
    rows = []
    forced_zero = True
    for row_id, (a, beta) in enumerate(zip(m['A'], m['B'])):
        c = sum(x * y for x, y in zip(beta, b)) + sum(a[i] * offset[i] for i in range(dim))
        reduced = [sum(a[i] * coefficient[i][j] for i in range(dim)) for j in range(len(free))]
        if closed & (1 << row_id) and (any(reduced) or c != 0):
            forced_zero = False
        rows.append([c, *reduced])
    return {'dimension_bound': len(free), 'free_original_coordinates': free, 'offset': offset,
            'basis_rows': coefficient, 'rows': rows, 'forced_boundary_consistent': forced_zero}
