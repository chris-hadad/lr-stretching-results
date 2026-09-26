"""Independent complete table-normal census and literal integer right inverses.

Provider records supply candidate representatives only. Every subset is
independently classified; omitted or duplicate classes fail the exact cover.
No provider program or numerical local value is imported or executed.
"""
from collections import Counter, deque
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path
import sys
import time

GROUPS = {(3, 5, 3): (5, 450, 5), (3, 5, 4): (10, 1305, 60),
          (4, 4, 3): (6, 560, 0), (4, 4, 4): (14, 1812, 8),
          (4, 4, 5): (19, 4272, 96), (4, 5, 3): (6, 1140, 0),
          (4, 5, 4): (15, 4840, 5), (4, 5, 5): (25, 15420, 84),
          (4, 5, 6): (49, 38100, 660), (4, 5, 7): (70, 74280, 3240),
          (4, 5, 8): (98, 114840, 11130)}


def save(path, data):
    with path.open('x') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def basis(p, n):
    rows = [[0] * ((p - 1) * (n - 1)) for _ in range(p * n)]
    for i in range(p - 1):
        for j in range(n - 1):
            k = i * (n - 1) + j
            for a, b, v in ((i, j, 1), (i, n - 1, -1),
                            (p - 1, j, -1), (p - 1, n - 1, 1)):
                rows[a * n + b][k] = v
    return rows


def graph(p, n, selected):
    adj = [[] for _ in range(p + n)]
    for e in range(p * n):
        if e not in selected:
            i, j = divmod(e, n)
            adj[i].append((p + j, e))
            adj[p + j].append((i, e))
    return adj


def component(adj, start):
    seen = {start}
    todo = [start]
    for x in todo:
        for y, edge in adj[x]:
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def right_inverse(p, n, ids, rows):
    adj = graph(p, n, set(ids))
    answer = []
    for edge in ids:
        i, j = divmod(edge, n)
        start = p + j
        previous = {start: None}
        queue = deque([start])
        while queue and i not in previous:
            x = queue.popleft()
            for y, e in adj[x]:
                if y not in previous:
                    previous[y] = (x, e)
                    queue.append(y)
        assert i in previous, 'No compensating path'
        path = []
        x = i
        while x != start:
            x, e = previous[x]
            path.append(e)
        path.reverse()
        full = [0] * (p * n)
        full[edge] = 1
        for k, e in enumerate(path):
            full[e] = -1 if k % 2 == 0 else 1
        assert all(sum(full[a*n:(a+1)*n]) == 0 for a in range(p))
        assert all(sum(full[a*n+b] for a in range(p)) == 0 for b in range(n))
        coordinates = [full[a*n+b] for a in range(p-1) for b in range(n-1)]
        assert [sum(a*b for a,b in zip(row,coordinates)) for row in rows] == full
        assert [full[e] for e in ids] == [int(e == edge) for e in ids]
        answer.append({'selected_edge': edge, 'path': path, 'full_table': full,
                       'free_coordinates': coordinates})
    return answer


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for transport topology replay')
    source, output = Path(sys.argv[1]), Path(sys.argv[2])
    started = time.monotonic()
    records = json.loads(source.read_text())
    assert len(records) == 317
    assert set((r['p'], r['N'], r['q']) for r in records) == set(GROUPS)
    witnesses, summaries, cases = [], [], []
    for (p, n, q), expected in GROUPS.items():
        group = [r for r in records if (r['p'], r['N'], r['q']) == (p, n, q)]
        assert [r['type'] for r in group] == list(range(expected[0]))
        original = basis(p, n)
        owner, multiplicities = {}, Counter()
        for row in group:
            ids = row['ids']
            assert ids == sorted(set(ids)) and len(ids) == q and 0 <= min(ids) <= max(ids) < p*n
            assert row['mask'] == sum(1 << x for x in ids)
            assert row['normals'] == [original[x] for x in ids]
            scaled_gram = [[(p*n if x == y else 0) - (p if x//n == y//n else 0)
                           - (n if x%n == y%n else 0) + 1 for y in ids] for x in ids]
            assert scaled_gram == row['H']
            inverses = right_inverse(p, n, ids, original)
            orbit = set()
            for rp in permutations(range(p)):
                for cp in permutations(range(n)):
                    orbit.add(sum(1 << (rp[e//n]*n+cp[e%n]) for e in ids))
            assert len(orbit) == row['multiplicity']
            assert not any(mask in owner for mask in orbit), 'Duplicate orbit representatives'
            for mask in orbit:
                owner[mask] = row['type']
            witnesses.append({'p': p, 'N': n, 'q': q, 'type': row['type'],
                              'integer_right_inverse': inverses, 'orbit_size': len(orbit)})
            cases.append(' '.join(map(str, [f'T{p}-{n}-{q}-{row["type"]}', 'T', p, n, q, *ids])))
        independent = dependent = 0
        for ids in combinations(range(p*n), q):
            mask = sum(1 << x for x in ids)
            seen = component(graph(p, n, set(ids)), 0)
            if len(seen) == p+n:
                assert mask in owner, 'Missing independent subset'
                independent += 1
                multiplicities[owner[mask]] += 1
            else:
                assert mask not in owner, 'Dependent subset assigned a local value'
                relation = [int(e//n in seen) - int(p+e%n in seen) for e in ids]
                assert any(relation)
                assert all(sum(weight*original[e][k] for weight,e in zip(relation,ids)) == 0
                           for k in range((p-1)*(n-1)))
                dependent += 1
        assert (len(group), independent, dependent) == expected
        assert all(multiplicities[r['type']] == r['multiplicity'] for r in group)
        summary = {'p': p, 'N': n, 'q': q, 'types': len(group),
                   'independent_subsets': independent, 'dependent_subsets': dependent,
                   'all_dependencies_checked': True, 'all_orbit_multiplicities_checked': True}
        summaries.append(summary)
        print(json.dumps(summary), flush=True)
    save(output / 'RIGHT-INVERSES.json', witnesses)
    with (output / 'TABLE-CASES.txt').open('x') as stream:
        stream.write('\n'.join(cases) + '\n')
    result = {'status': 'COMPLETE_INDEPENDENT_NORMAL_SUBSET_AND_INTEGER_LATTICE_CHECK',
              'groups': summaries, 'elapsed_seconds': time.monotonic() - started,
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'scope': 'All 272307 subsets and 317 table-normal orbits; no local BV values computed by this program.'}
    save(output / 'RESULT.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
