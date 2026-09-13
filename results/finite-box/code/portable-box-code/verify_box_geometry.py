"""Bind one complete production shard to independent geometry and both raw models."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

from box_geometry import check, need

CERTIFICATES = {
    'U04': 'DATA/U04/final-science/UNIFORM-FOUR-COUNT-CERTIFICATES.jsonl.gz',
    'U05': 'DATA/U05/third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz',
    'U06': 'DATA/U06/final-science/UNIFORM-SEPTIC-CERTIFICATES.jsonl.gz',
    'U07': 'DATA/U07/final-science/UNIFORM-OCTIC-CERTIFICATES.jsonl.gz',
    'U08': 'DATA/U08/final-science-v2/UNIFORM-NONIC-CERTIFICATES.jsonl.gz',
    'U09': 'DATA/U09/final-science/COMPACT-CERTIFICATES.jsonl.gz',
    'U10': 'DATA/U10/final-science/COMPACT-CERTIFICATES.jsonl.gz',
}


def exact_integer(x):
    if type(x) is int:
        return x
    need(type(x) is str and x and x.lstrip('-').isdigit(), 'Noninteger count')
    return int(x)


def raw_index(path):
    data = {}
    with path.open() as f:
        for number, line in enumerate(f, 1):
            z = json.loads(line)
            request, response = z['request'], z['response']
            key = (request.split()[0], json.dumps(response, sort_keys=True, separators=(',', ':')))
            need(key not in data or data[key][0] == request, 'One response has different requests')
            data[key] = (request, number, hashlib.sha256(line.encode()).hexdigest())
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--unit', required=True, choices=CERTIFICATES)
    p.add_argument('--shard', required=True)
    p.add_argument('--expected-selected', required=True, type=int)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    need(Path(a.shard).name == a.shard and a.shard.startswith('shard'), 'Invalid shard')
    source = a.root / CERTIFICATES[a.unit]
    selected = {}
    with gzip.open(source, 'rt') as f:
        for line in f:
            z = json.loads(line)
            key = z.get('group_id', z.get('target_ordinal', z.get('id')))
            need(key not in selected, 'Duplicate complete certificate identity')
            if a.unit == 'U04':
                counts, gh = [z[k] for k in ('A', 'B', 'I1', 'I2')], z['geometry_sha256']
            elif a.unit == 'U05':
                counts, gh = [z[k] for k in ('A', 'B', 'C', 'I1', 'I2')], z['geometry']['sha256']
            else:
                fields = [k for k in z if k.startswith('counts_')]
                need(len(fields) == 1, 'Ambiguous count order')
                counts, gh = z[fields[0]], z['geometry_sha256']
            selected[key] = (counts, gh, z.get('bare_triple'))
    if a.unit == 'U04':
        folder = a.root / 'DATA/U04/layer5-results' / a.shard
        raw_names = {'hive': 'hive-queries.jsonl', 'rows': 'rows-queries.jsonl'}
    else:
        folder = a.root / 'DATA' / a.unit / 'production' / a.shard / 'counts'
        raw_names = {'hive': 'hive.jsonl', 'rows': 'rows.jsonl'}
    raw = {model: raw_index(folder / name) for model, name in raw_names.items()}
    repairs, repair_raw = {}, {}
    if a.unit == 'U04':
        r = a.root / 'DATA/U04/seven-dual-repairs'
        with (r / 'certificates.jsonl').open() as f:
            repairs = {z['id']: z for z in map(json.loads, f)}
        for model in ('hive', 'rows'):
            name = r / (model + '-queries.jsonl')
            repair_raw[model] = raw_index(name if name.exists() else r / (model + '.jsonl'))
    d = int(a.unit[1:]) + 1
    expected_sites = [(f'P{t}', t, False) for t in range(1, d // 2 + 1)]
    expected_sites += [(f'I{t}', t, True) for t in range(1, d - d // 2)]
    seen, query_count, total = set(), 0, 0
    identities = a.output.with_suffix('.identities.jsonl')
    with gzip.open(folder / 'geometry.jsonl.gz', 'rb') as gf, (folder / 'certificates.jsonl').open() as cf, identities.open('x') as out:
        for gl, cl in zip(gf, cf, strict=True):
            c, r = json.loads(gl), json.loads(cl)
            total += 1
            need(c['id'] == r['id'], 'Geometry/certificate identity mismatch')
            key = c['id']
            gh = hashlib.sha256(gl).hexdigest()
            need(gh == r['geometry_sha256'], 'Geometry source bytes mismatch')
            if key not in selected:
                continue
            need(key not in seen, 'Duplicate selected identity')
            seen.add(key)
            values, expected_gh, triple = selected[key]
            need(gh == expected_gh and (triple is None or triple == c['original'])
                 and r['bare_triple'] == c['original'], 'Selected whole-object mismatch')
            if key in repairs:
                r = repairs[key]
                need(r['geometry_sha256'] == gh and r['bare_triple'] == c['original'], 'Repair changed object')
            flags = check(c)
            need(c['actual_dimension'] == c['degree_bound'] == d, 'Unexpected actual degree')
            sites_out = []
            for model in ('hive', 'rows'):
                sites = r['model_sites'][model]
                need([(s['kind'], s['physical_grade'], s['strict']) for s in sites] == expected_sites,
                     'Wrong or incomplete physical-grade/strictness roster')
                need([exact_integer(s['response']['value']) for s in sites] == values, 'Compact/raw value mismatch')
                index = repair_raw[model] if key in repairs else raw[model]
                for site in sites:
                    response = site['response']
                    need(response['status'] == 'complete' and exact_integer(response['value']) >= 0,
                         'Incomplete or invalid count used')
                    raw_key = (response['id'], json.dumps(response, sort_keys=True, separators=(',', ':')))
                    need(raw_key in index, 'Missing physical raw response')
                    request, line, rhash = index[raw_key]
                    tok = request.split()
                    grade, strict = site['physical_grade'], site['strict']
                    if model == 'hive':
                        rows = c['count_rows']
                        expected_rows = [[grade * x[0] - int(any(x[1:])), *x[1:]] for x in rows] if strict else rows
                        need(list(map(int, tok[1:4])) == [d, len(rows), 1 if strict else grade], 'Wrong full hive request header')
                        need(list(map(int, tok[5:])) == [v for row in expected_rows for v in row], 'Wrong complete hive request rows')
                    else:
                        n = c['rank']
                        thresholds = flags if strict else [[[0] * n for _ in range(n)] for _ in range(3)]
                        need(list(map(int, tok[1:3])) == [n, grade], 'Wrong tableau request rank/grade')
                        wanted = [v for k in ('lambda', 'mu', 'nu') for v in c['count_boundary'][k]]
                        wanted += [v for block in thresholds for row in block for v in row]
                        need(list(map(int, tok[4:])) == wanted, 'Wrong complete tableau boundary/strictness')
                    sites_out.append([model, site['kind'], response['id'], line, rhash])
                    query_count += 1
            out.write(json.dumps({'id': key, 'bare_triple': c['original'], 'geometry_sha256': gh,
                                  'actual_degree': d, 'queries': sites_out}, separators=(',', ':')) + '\n')
    need(len(seen) == a.expected_selected, 'Selected shard population differs from frozen identity inventory')
    need(query_count == 2 * (d - 1) * len(seen), 'Incomplete paired query coverage')
    result = {'status': 'PASS', 'unit': a.unit, 'shard': a.shard, 'selected': len(seen),
              'total_geometry_records': total, 'paired_count_occurrences': query_count // 2,
              'physical_model_query_occurrences': query_count,
              'identity_file': str(identities),
              'complete_geometry_actual_degree_short_normals': True,
              'complete_row_hive_integer_maps_and_strictness': True,
              'raw_numerical_models_rebound': True,
              'new_lattice_recounts': 0, 'formal_bound_checks': 0,
              'source_premise': 'Previously accepted full boundary-mask forcing tables',
              'returned_code_executed': False}
    with a.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({'status': 'PASS', 'unit': a.unit, 'shard': a.shard, 'selected': len(seen)}))


if __name__ == '__main__':
    main()
