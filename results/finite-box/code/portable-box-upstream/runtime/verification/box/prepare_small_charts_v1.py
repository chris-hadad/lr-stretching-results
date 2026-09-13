"""Complete independent chart models for the entire small-area residual roster."""
import argparse, hashlib, json, os, time
from pathlib import Path
from slr_ehrhart.hive import interior_points
from mask_model_v1 import boundary_mask, whole_chart
from prepare_quartic_charts_v1 import variants, compact

def run(a):
    r = json.loads(a.roster.read_text())
    start = time.monotonic()
    source = json.loads(Path(r['small_roster']).read_text())['records']
    assert len(source) == 56
    masks = {}
    for path in r['verified_masks']:
        j = json.loads(Path(path).read_text())
        assert j['status'] == 'complete'
        masks[j['rank']] = {x['mask']: x for x in j['records']}
    records = []
    seen = set()
    text_path = Path(r['charts_output'])
    assert not text_path.exists()
    with text_path.open('x') as f:
        f.write('56\n')
        for i, case in enumerate(source):
            n = case['rank']
            original = tuple((tuple(case[k]) for k in ['lambda', 'mu', 'nu']))
            assert original not in seen
            seen.add(original)
            assert sum(original[0]) <= 16
            choices = []
            for triple, word in variants(*original, n):
                mask = boundary_mask(*triple, n)
                choices.append((masks[n][mask]['dimension_bound'], sum(triple[0]), triple, word, mask))
            d, area, triple, word, mask = min(choices, key=lambda x: x[:3])
            assert d <= case['degree_bound'] <= 5
            chart = whole_chart(*triple, n, masks[n][mask]['closed_rows_mask'])
            assert chart['dimension_bound'] == d and chart['forced_boundary_consistent']
            L, M, N = triple
            points = interior_points(n)
            translation = [sum(M[:points[k][0]]) + sum(L[:points[k][1]]) for k in chart['free_original_coordinates']]
            rows = compact([[row[0] + sum((x * y for x, y in zip(row[1:], translation))), *row[1:]] for row in chart['rows']])
            id = f'SMALL-{i:04d}'
            f.write(f'{id} {d} {len(rows)}\n')
            for row in rows:
                f.write(' '.join(map(str, row)) + '\n')
            records.append({'id': id, 'record_index': i, 'rank': n, 'original': dict(zip(['lambda', 'mu', 'nu'], original)), 'source_degree_bound': case['degree_bound'], 'degree_bound': d, 'count_boundary': dict(zip(['lambda', 'mu', 'nu'], triple)), 'word': word, 'chart': chart, 'count_translation': translation, 'count_rows': rows})
    result = {'status': 'complete', 'pid': os.getpid(), 'pgid': os.getpgrp(), 'native_calls': 0, 'record_count': len(records), 'records': records, 'charts_file': {'path': str(text_path), 'sha256': hashlib.sha256(text_path.read_bytes()).hexdigest(), 'bytes': text_path.stat().st_size}, 'seconds': time.monotonic() - start}
    with a.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({'record_count': 56, 'seconds': result['seconds']}))
