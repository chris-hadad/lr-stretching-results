"""Independent full-object and raw-query binding for the final 495 vectors."""
import argparse
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

from box_geometry import check, need
from verify_box_algebra import basis


class Sources:
    def __init__(self, root):
        self.root = root
        self.pins, self.reads, self.lines_cache = {}, {}, {}
        with (root / 'MEMBERS.jsonl').open() as f:
            for line in f:
                x = json.loads(line)
                if x.get('state') == 'restored_inert' and x.get('output_path'):
                    self.pins[str(Path(x['output_path']).resolve())] = x['sha256']

    def lines(self, namespace, relative):
        p = (self.root / 'namespaces' / namespace / relative).resolve()
        need(p.is_relative_to(self.root / 'namespaces') and str(p) in self.pins, 'Unmanifested input path')
        key = str(p)
        if key not in self.lines_cache:
            b = p.read_bytes()
            need(hashlib.sha256(b).hexdigest() == self.pins[key], 'Changed manifested source')
            self.reads[key] = self.pins[key]
            if p.suffix == '.gz':
                b = gzip.decompress(b)
            self.lines_cache[key] = [(json.loads(line), line) for line in b.splitlines(keepends=True) if line.strip()]
        return self.lines_cache[key]


def bind(c, flags, model, site, raw):
    need(raw['response'] == site['response'], 'Raw response mismatch')
    tok = raw['request'].split()
    need(tok[0] == site['response']['id'], 'Request identity mismatch')
    t, strict = site['physical_grade'], site['strict']
    need(type(t) is int and t > 0 and type(strict) is bool, 'Invalid physical grade/strictness')
    if model == 'hive':
        rows = c['count_rows']
        expected = [[t * row[0] - int(any(row[1:])), *row[1:]] for row in rows] if strict else rows
        need(list(map(int, tok[1:4])) == [c['degree_bound'], len(rows), 1 if strict else t], 'Hive header mismatch')
        need(list(map(int, tok[5:])) == [v for row in expected for v in row], 'Full hive rows mismatch')
    else:
        n = c['rank']
        L, M, N = [c['count_boundary'][k] for k in ('lambda', 'mu', 'nu')]
        if site.get('swapped_inners'):
            need(not strict, 'Unsupported strictness swap')
            M, N = N, M
        threshold = flags if strict else [[[0] * n for _ in range(n)] for _ in range(3)]
        need(list(map(int, tok[1:3])) == [n, t], 'Tableau rank/grade mismatch')
        need(list(map(int, tok[4:])) == L + M + N + [v for block in threshold for row in block for v in row],
             'Complete tableau boundary/threshold mismatch')
    need(site['response']['status'] == 'complete', 'Incomplete response used')
    value = site['response']['value']
    need(type(value) is int or (type(value) is str and value.isdigit()), 'Noninteger count')
    need(int(value) >= 0, 'Negative scalar')
    return -t if strict else t, int(value) * ((-1)**c['actual_dimension'] if strict else 1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--restored', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    S = Sources(a.restored.resolve())
    compact = S.lines('u12', 'AUDIT/U11-COMPLETE-VECTORS/COMPACT-CERTIFICATES.jsonl.gz')
    need(len(compact) == 495, 'Final certificate population changed')
    input_maps, raw_maps, source_records = {}, {}, {}

    def raw_map(namespace, relative):
        key = (namespace, relative)
        if key not in raw_maps:
            data = {}
            for row, line in S.lines(namespace, relative):
                identity = (row['response']['id'], json.dumps(row['response'], sort_keys=True))
                need(identity not in data or data[identity] == row, 'Conflicting duplicate response')
                data[identity] = row
            raw_maps[key] = data
        return raw_maps[key]

    old_maps = {m: {} for m in ('hive', 'rows')}
    for shard in range(3):
        for model in old_maps:
            for key, value in raw_map('u10', f'DATA/U10/production/shard{shard:03d}/counts/{model}.jsonl').items():
                need(key not in old_maps[model] or old_maps[model][key] == value, 'Conflicting old count identity')
                old_maps[model][key] = value
    seen, determined, held, reused = set(), 0, 0, 0
    bases, vectors = {}, set()
    out = a.output.with_suffix('.identities.jsonl')
    with out.open('x') as identities:
        for z, zline in compact:
            key = z['group_id']
            need(key not in seen, 'Duplicate final identity')
            seen.add(key)
            input_path = z['geometry_input']
            if input_path not in input_maps:
                rows = S.lines('u11', input_path)
                input_maps[input_path] = {r['id']: r for r, line in rows}
                need(len(input_maps[input_path]) == len(rows), 'Duplicate geometry input')
            x = input_maps[input_path][key]
            c = x['geometry']
            gh = hashlib.sha256(json.dumps(c, separators=(',', ':')).encode()).hexdigest()
            need(gh == z['geometry_sha256'] and c['original'] == z['bare_triple'], 'Final geometry binding')
            flags = check(c, require_short_normals=False)
            d, nodes = c['actual_dimension'], z['determining_nodes']
            need(d == z['actual_dimension'] and d in (11, 12), 'Final degree')
            need(nodes == x['determining_nodes'] and len(nodes) == d + 1 and len(set(nodes)) == d + 1, 'Complete determining space')
            need(set(x['reserved_positive_holdouts']) == set(map(int, z['positive_held_values'])), 'Holdout roster changed')
            origin = x['determination_source']
            if origin['path'] not in source_records:
                source_records[origin['path']] = {hashlib.sha256(line).hexdigest(): r
                                                for r, line in S.lines('u11', origin['path'])}
            determination = x['determination']
            need(source_records[origin['path']][origin['line_sha256']] == determination, 'Determination source body changed')
            need(determination['bare_triple'] == c['original'] and determination['degree'] == d
                 and determination['nodes'] == nodes, 'Determination object changed')
            for model in ('hive', 'rows'):
                values = {0: 1}
                if x.get('previous_counts_complete'):
                    prior_source = x['prior_record_source']
                    namespace, relative = prior_source.split('/', 1)
                    row, line = S.lines(namespace, relative)[x['prior_record_line'] - 1]
                    need(hashlib.sha256(line).hexdigest() == x['prior_record_line_sha256'] and row == x['prior_record'], 'Prior record line binding')
                    need(len(row['model_sites'][model]) == 10, 'Prior determining roster')
                    for site in row['model_sites'][model]:
                        rk = (site['response']['id'], json.dumps(site['response'], sort_keys=True))
                        t, value = bind(c, flags, model, site, old_maps[model][rk])
                        need(t not in values, 'Duplicated prior determining grade')
                        values[t] = value
                        reused += 1
                directory = str(Path(origin['path']).parent)
                queries = raw_map('u11', directory + '/' + model + '.jsonl')
                for site in determination['queries'][model]:
                    rk = (site['response']['id'], json.dumps(site['response'], sort_keys=True))
                    t, value = bind(c, flags, model, site, queries[rk])
                    need(t not in values and t in nodes, 'Repeated or extraneous determining grade')
                    values[t] = value
                need(set(values) == set(nodes) and {str(k): v for k, v in values.items()} == z['values'][model], 'Incomplete final determining values')
                need(z['values'][model] == determination['values'][model], 'Compact/physical determination mismatch')
                determined += len(values) - 1
            if d not in bases:
                bases[d] = basis(nodes)
            vals = [Fraction(z['values']['hive'][str(t)]) for t in nodes]
            poly = [sum(a * b for a, b in zip(row, vals)) for row in bases[d]]
            if any(v < 0 for v in poly):
                with a.output.with_suffix('.candidate.json').open('x') as f:
                    json.dump({'bare_triple': c['original'], 'nodes': nodes,
                               'values': z['values']['hive'], 'coefficients': list(map(str, poly))}, f)
                raise ValueError('Ordinary-negative observation preserved before comparison')
            need(poly == list(map(Fraction, z['coefficients'])) and all(v > 0 for v in poly), 'Final vector arithmetic')
            vectors.add(tuple(poly))
            successful = {m: {} for m in ('hive', 'rows')}
            for ref in z['held_evidence']:
                raw, line = S.lines('u11', ref['path'])[ref['line'] - 1]
                need(hashlib.sha256(line).hexdigest() == ref['sha256'], 'Held raw line hash')
                t, model = ref['grade'], ref['model']
                need(t > 0 and t not in nodes and t in x['reserved_positive_holdouts'], 'Unreserved holdout')
                site = {'response': raw['response'], 'physical_grade': t, 'strict': False,
                        'swapped_inners': raw['request'].split()[0].endswith('_swap')}
                _, value = bind(c, flags, model, site, raw)
                need(value == sum(v * t**k for k, v in enumerate(poly)), 'Held count disagrees with polynomial')
                need(t not in successful[model] or successful[model][t] == value, 'Conflicting repeated holdout')
                successful[model][t] = value
            need(successful['hive'] == successful['rows'] == {int(k): v for k, v in z['positive_held_values'].items()},
                 'Incomplete paired holdout population')
            held += len(successful['hive'])
            identities.write(json.dumps({'id': key, 'bare_triple': c['original'], 'geometry_sha256': gh,
                                          'actual_degree': d, 'certificate_sha256': hashlib.sha256(zline).hexdigest()}, separators=(',', ':')) + '\n')
    need(len(seen) == 495 and determined == 2 * 5596 and held == 990 and reused == 2 * 3390, 'Final exact count population')
    result = {'status': 'PASS', 'records': 495, 'paired_determining_sites': determined // 2,
              'paired_reused_sites': reused // 2, 'paired_positive_holdouts': held,
              'distinct_vectors': len(vectors), 'source_inputs': S.reads,
              'new_lattice_recounts': 0, 'returned_code_executed': False,
              'complete_geometry_and_both_raw_count_models_bound': True}
    with a.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'source_inputs'}))


if __name__ == '__main__':
    main()
