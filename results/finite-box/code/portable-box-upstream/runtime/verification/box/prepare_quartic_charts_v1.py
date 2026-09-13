"""Rebuild complete saturated small hive charts without reading source counts."""
import argparse
from fractions import Fraction
from math import gcd
import hashlib
import json
import os
from pathlib import Path
import time
from slr_ehrhart.hive import interior_points
from mask_model_v1 import boundary_mask, whole_chart

def variants(lam, mu, nu, n):

    def dual(w):
        return tuple((-x for x in reversed(w)))
    weights = (tuple(mu), tuple(nu), dual(lam))
    for d in (0, 1):
        w = tuple((dual(x) for x in weights)) if d else weights
        for outer in range(3):
            others = [i for i in range(3) if i != outer]
            for first, second in (others, others[::-1]):
                L = dual(w[outer])
                M = w[first]
                N = w[second]
                a, b = (M[-1], N[-1])
                L = tuple((x - a - b for x in L))
                M = tuple((x - a for x in M))
                N = tuple((x - b for x in N))
                if min(L) < 0:
                    continue
                assert sum(L) == sum(M) + sum(N)
                yield ((L, M, N), {'dual_all': bool(d), 'outer': outer, 'inner_order': [first, second], 'determinant_shifts': [a, b]})

def compact(rows):
    kept = {}
    constant = []
    for row in rows:
        c, *a = row
        g = 0
        for x in a:
            g = gcd(g, abs(x))
        if not g:
            if c < 0:
                constant.append([-1, *[0] * len(a)])
            continue
        normal = tuple((x // g for x in a))
        bound = Fraction(c, g)
        if normal not in kept or bound < kept[normal][0]:
            kept[normal] = (bound, row)
    return sorted(constant + [row for _, row in kept.values()])

def run(a):
    r = json.loads(a.roster.read_text())
    start = time.monotonic()
    masks = {}
    for item in r['verified_masks']:
        q = json.loads(Path(item['path']).read_text())
        assert q['status'] == 'complete'
        masks[q['rank']] = {x['mask']: x for x in q['records']}
        assert set(masks[q['rank']]) == set(range(1 << 3 * (q['rank'] - 1)))
    cases = []
    for item in r['exceptions']:
        rows = json.loads(Path(item['path']).read_text())
        assert len(rows) == item['expected_count']
        cases += rows
    cases.sort(key=lambda x: x['id'])
    assert len(cases) == 10348 and len({x['id'] for x in cases}) == 10348
    result = {'status': 'running', 'pid': os.getpid(), 'pgid': os.getpgrp(), 'native_calls': 0, 'source_counts_read': False, 'records': []}
    text_path = Path(r['charts_output'])
    assert not text_path.exists()
    with a.output.open('x') as out, text_path.open('x') as text:

        def save():
            out.seek(0)
            json.dump(result, out, indent=2)
            out.write('\n')
            out.truncate()
            out.flush()
            os.fsync(out.fileno())
        save()
        text.write(str(len(cases)) + '\n')
        profiles = set()
        for index, case in enumerate(cases):
            n = case['rank']
            original = tuple((tuple(case[k]) for k in ['lambda', 'mu', 'nu']))
            assert all((len(x) == n for x in original))
            assert case['area'] == sum(original[0]) <= 30 and case['degree_bound'] == 4
            assert boundary_mask(*original, n) == case['mask']
            choices = []
            for triple, word in variants(*original, n):
                mask = boundary_mask(*triple, n)
                m = masks[n][mask]
                choices.append((m['dimension_bound'], sum(triple[0]), triple, word, mask))
            chosen = min(choices, key=lambda x: x[:3])
            d, area, triple, word, mask = chosen
            assert d == 4
            chart = whole_chart(*triple, n, masks[n][mask]['closed_rows_mask'])
            assert chart['dimension_bound'] == 4 and chart['forced_boundary_consistent']
            L, M, N = triple
            points = interior_points(n)
            translation = []
            for k in chart['free_original_coordinates']:
                i, j = points[k]
                translation.append(sum(M[:i]) + sum(L[:j]))
            translated = [[row[0] + sum((x * y for x, y in zip(row[1:], translation))), *row[1:]] for row in chart['rows']]
            count_rows = compact(translated)
            profiles.add(tuple(map(tuple, count_rows)))
            text.write(f"{case['id']} 4 {len(count_rows)}\n")
            for row in count_rows:
                text.write(' '.join(map(str, row)) + '\n')
            result['records'].append({'id': case['id'], 'record_index': index, 'original_boundary': dict(zip(['lambda', 'mu', 'nu'], original)), 'rank': n, 'preimages': case['preimages'], 'count_boundary': dict(zip(['lambda', 'mu', 'nu'], triple)), 'count_preserving_word': word, 'mask': mask, 'closed_rows_mask': masks[n][mask]['closed_rows_mask'], 'chart': chart, 'count_translation': translation, 'complete_compacted_count_rows': count_rows})
            if (index + 1) % 1000 == 0:
                save()
        text.flush()
        os.fsync(text.fileno())
        result.update(status='complete', expected_ids=[x['id'] for x in cases], record_count=len(cases), exact_translated_rowset_profiles=len(profiles), charts_file={'path': str(text_path), 'sha256': hashlib.sha256(text_path.read_bytes()).hexdigest(), 'bytes': text_path.stat().st_size}, seconds=time.monotonic() - start, scope='Complete original-rhombus all-stretch count charts and integral coordinate inverses for exactly the P09 exceptions; no scalar counts or coefficient signs computed')
        save()
        print(json.dumps({k: result[k] for k in ['status', 'record_count', 'exact_translated_rowset_profiles', 'seconds']}), flush=True)
