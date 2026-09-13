"""Independent Lagrange-basis check of Pro026 sign and full-vector certificates.

This checks algebra, identities and exact member bytes. Geometry, counts and
formal bounds are separate premises; it never imports returned programs.
"""
import argparse
from fractions import Fraction as Q
import gzip
import hashlib
import json
import math
from pathlib import Path


def multiply(a, b):
    c = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def basis(nodes):
    columns = []
    for t in nodes:
        p, den = [Q(1)], 1
        for u in nodes:
            if u != t:
                p = multiply(p, [-u, 1])
                den *= t - u
        columns.append([c / den for c in p])
    for i, col in enumerate(columns):
        for j, t in enumerate(nodes):
            assert sum(c * t**k for k, c in enumerate(col)) == int(i == j)
    return list(map(list, zip(*columns)))


def integer_weights(d):
    p, m = d // 2, d - d // 2
    nodes = [0] + list(range(1, p + 1)) + list(range(-1, -m - 1, -1))
    rows = basis(nodes)
    rows = [[x * ((-1)**d if t < 0 else 1) for x, t in zip(row, nodes)] for row in rows]
    ds = [math.lcm(*(x.denominator for x in row)) for row in rows]
    return ds, [[int(x * den) for x in row] for den, row in zip(ds, rows)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_record(z, unit, matrices, full_bases, candidate_path):
    key = z.get('group_id', z.get('target_ordinal', z.get('id')))
    require(type(key) is int, 'Missing integer certificate identity')
    if unit == 'U04':
        A, B, U, V = [z[k] for k in ('A', 'B', 'I1', 'I2')]
        require(all(type(v) is int and v >= 0 for v in (A, B, U, V)) and A > 0,
                'Invalid quintic count')
        d1, d2 = 8 * (A + U) - B - V, 16 * (A - U) - B + V - 30
        n1 = 30 * A - 3 * B + 60 * U - 15 * V + 20
        require((z['D1'], z['D2'], z['L1']) == (d1, d2, n1), 'Quintic functional mismatch')
        require(n1 > 0 and d2 > 0, 'Quintic sufficient bound did not prove signs')
        return key, 5, [Q(1), Q(n1, 60), Q(d2, 24)], None
    if unit == 'U11':
        d, nodes = z['actual_dimension'], z['determining_nodes']
        require(d in (11, 12), 'Unexpected full-vector degree')
        expected = list(range(-6, 6)) if d == 11 else list(range(-8, 5))
        require(nodes == expected, 'Determining nodes changed')
        if d not in full_bases:
            full_bases[d] = basis(nodes)
        counts = z['values']['hive']
        require(set(counts) == set(map(str, nodes)), 'Incomplete/extra determining values')
        require(all(type(v) is int for v in counts.values()) and counts['0'] == 1,
                'Noninteger count or incorrect constant')
        require(all(v * ((-1)**d if int(t) < 0 else 1) >= 0 for t, v in counts.items()),
                'Invalid closed/interior count sign')
        values = [Q(counts[str(t)]) for t in nodes]
        coefficients = [sum(a * b for a, b in zip(row, values)) for row in full_bases[d]]
        # Persist an exact negative observation before source-vector comparison.
        if any(c < 0 for c in coefficients):
            with candidate_path.open('x') as f:
                json.dump({'certificate_id': key, 'bare_triple': z.get('bare_triple'),
                           'nodes': nodes, 'values': counts,
                           'coefficients': list(map(str, coefficients)),
                           'state': 'ordinary_negative_observation_requires_candidate_protocol'}, f)
            raise ValueError('Candidate observation preserved; stop before comparisons')
        require(counts == z['values']['rows'], 'Independent determining model disagreement')
        require(coefficients == list(map(Q, z['coefficients'])), 'Source vector mismatch')
        require(coefficients[0] == 1 and all(c > 0 for c in coefficients), 'Full-vector strict sign failure')
        holds = z['positive_held_values']
        require(set(map(int, holds)) == ({6, 7} if d == 11 else {5, 6}), 'Missing/changed positive holdouts')
        for ts, value in holds.items():
            t = int(ts)
            require(t > 0 and t not in nodes, 'Holdout reused in fit')
            require(sum(c * t**k for k, c in enumerate(coefficients)) == Q(value), 'Holdout failure')
        return key, d, coefficients, tuple(coefficients)
    d = int(unit[1:]) + 1
    require(z['actual_dimension'] == d, 'Unexpected certificate degree')
    if unit == 'U05':
        values = [z[k] for k in ('A', 'B', 'C', 'I1', 'I2')]
        low, high = z['proved_I3_interval']
        saved = [Q(1)] + list(map(Q, z['all_six_ordinary_coefficient_lower_bounds']))
    elif unit in ('U06', 'U07', 'U08'):
        fields = [k for k in z if k.startswith('counts_P')]
        require(len(fields) == 1, 'Ambiguous count field')
        values = z[fields[0]]
        low, high = z['I' + str(d - d // 2) + '_interval']
        saved = list(map(Q, z['coefficient_lower_bounds']))
    else:
        values = z['counts_in_frozen_site_order']
        low, high = z['interior_interval']
        saved = list(map(Q, z['coefficient_lower_bounds']))
    require(len(values) == d - 1 and all(type(x) is int and x >= 0 for x in values)
            and values[0] > 0, 'Invalid determining counts')
    require(type(low) is int and type(high) is int and 0 <= low <= high, 'Invalid interior interval')
    den, rows = matrices[d]
    bounds = []
    for k, (divisor, row) in enumerate(zip(den, rows)):
        n = row[0] + sum(w * value for w, value in zip(row[1:-1], values))
        n += row[-1] * (low if row[-1] >= 0 else high)
        # Strict top-three signs are an explicitly separate geometric premise.
        if k >= d - 2:
            n = max(n, 1)
        bounds.append(Q(n, divisor))
    require(all(c > 0 for c in bounds), 'Interval does not prove all coefficient signs')
    require(len(saved) == d + 1 and all(a <= b for a, b in zip(saved, bounds)),
            'Saved lower bound stronger than derived bound')
    return key, d, bounds, None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, type=Path)
    p.add_argument('--unit', required=True, choices=['U04', 'U05', 'U06', 'U07', 'U08', 'U09', 'U10', 'U11'])
    p.add_argument('--start', type=int, default=0)
    p.add_argument('--stop', type=int)
    p.add_argument('--expected-total', type=int, required=True)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    require(a.start >= 0 and (a.stop is None or a.stop > a.start), 'Invalid slice')
    matrices = {d: integer_weights(d) for d in range(6, 12)}
    full_bases, ids, vectors, minima = {}, set(), set(), {}
    total, checked, coefficient_occurrences = 0, 0, 0
    identity_hash, rows_hash = hashlib.sha256(), hashlib.sha256()
    identity_path = a.output.with_suffix('.identities.jsonl')
    candidate_path = a.output.with_suffix('.candidate.json')
    with gzip.open(a.input, 'rb') as f, identity_path.open('x') as out:
        for ordinal, line in enumerate(f):
            total += 1
            if ordinal < a.start or (a.stop is not None and ordinal >= a.stop):
                continue
            rows_hash.update(line)
            z = json.loads(line)
            key, degree, bounds, vector = check_record(z, a.unit, matrices, full_bases, candidate_path)
            require(key not in ids, 'Duplicate certificate identity')
            ids.add(key)
            record = {'unit': a.unit, 'ordinal': ordinal, 'id': key,
                      'bare_triple': z.get('bare_triple', z.get('triple')),
                      'row_sha256': hashlib.sha256(line).hexdigest()}
            text = json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n'
            identity_hash.update(text.encode())
            out.write(text)
            checked += 1
            if vector is not None:
                vectors.add(vector)
                coefficient_occurrences += len(vector)
            for k, value in enumerate(bounds):
                pair = (degree, k)
                minima[pair] = min(minima.get(pair, value), value)
    require(total == a.expected_total, 'Input total differs from frozen expected population')
    require(checked == min(total, a.stop if a.stop is not None else total) - a.start and checked > 0,
            'Incomplete or empty slice')
    result = {'status': 'PASS', 'unit': a.unit, 'source': str(a.input),
              'input_total': total, 'slice': [a.start, min(total, a.stop if a.stop is not None else total)],
              'checked': checked, 'identity_sha256': identity_hash.hexdigest(),
              'checked_rows_sha256': rows_hash.hexdigest(),
              'distinct_full_vectors': len(vectors),
              'full_positive_coefficient_occurrences': coefficient_occurrences,
              'minima': {str(d) + ':' + str(k): str(v) for (d, k), v in minima.items()},
              'premises_not_checked_here': ['whole geometry and actual degree',
                    'raw count request/response bindings and algorithm correctness',
                    'formal interior upper/lower certificate validity', 'upstream exhaustive coverage'],
              'returned_code_executed': False}
    with a.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'unit': a.unit, 'checked': checked}))


if __name__ == '__main__':
    main()
