"""Bind every metric-certified normal list to complete independently reduced hives."""
import argparse
from functools import lru_cache
from itertools import permutations
from math import gcd
import hashlib, json, os, time
from pathlib import Path
from mask_model_v1 import model, identifications, images, reverse_bits

def normals_for(closed, m):
    free, components, ground, words = identifications(closed, m)
    assert len(free) == 4
    pos = {x: i for i, x in enumerate(free)}
    normals = set()
    for row in m['sparse']:
        a = [0] * 4
        for i, v in row:
            if components[i] != ground:
                a[pos[components[i]]] += v
        g = 0
        for v in a:
            g = gcd(g, abs(v))
        if g:
            normals.add(tuple((v // g for v in a)))
    return tuple(sorted(normals))

@lru_cache(None)
def coordinate_permutation(actual, expected):
    for p in permutations(range(4)):
        if tuple(sorted((tuple((row[i] for i in p)) for row in actual))) == expected:
            return p
    raise ValueError('Complete original normal list does not match the claimed atlas under any coordinate permutation')

def word_image(mask, n, dual, outer, step):
    w = n - 1
    bits = (1 << w) - 1
    L = mask & bits
    M = mask >> w & bits
    N = mask >> 2 * w
    v = (M, N, reverse_bits(L, w))
    if dual:
        v = tuple((reverse_bits(x, w) for x in v))
    return reverse_bits(v[outer], w) + (v[(outer + step) % 3] << w) + (v[(outer - step) % 3] << 2 * w)

def run(a):
    r = json.loads(a.roster.read_text())
    start = time.monotonic()
    aggregate = json.loads(Path(r['metric_aggregate']).read_text())
    assert aggregate['status'] == 'complete' and aggregate['all_3937_metric_identities_and_explicit_triple_rosters_complete']
    verified = set(aggregate['completed_ids'])
    expected = json.loads(Path(r['metric_expected']).read_text())['expected_metric_atlases']
    assert verified == {x['id'] for x in expected}
    admitted = {x['id']: x for x in expected}
    words = json.loads(Path(r['mask_words']).read_text())
    result = {'status': 'running', 'pid': os.getpid(), 'pgid': os.getpgrp(), 'native_calls': 0, 'strata': []}
    with a.output.open('x') as out:

        def save():
            out.seek(0)
            json.dump(result, out, indent=2)
            out.write('\n')
            out.truncate()
            out.flush()
            os.fsync(out.fileno())
        save()
        for entry in r['ranks']:
            n = entry['rank']
            m = model(n)
            source = json.loads(Path(entry['atlases']).read_text())
            maskdoc = json.loads(Path(entry['verified_masks']).read_text())
            assert maskdoc['status'] == 'complete'
            rows = {x['mask']: x for x in maskdoc['records']}
            four = {mask for mask, x in rows.items() if x['dimension_bound'] == 4}
            atlas_by_mask = {}
            bindings = []
            cache = {}
            assert source['n'] == n
            for atlas in source['normal_atlases']:
                id = f"R{n}-A{atlas['id']:04d}"
                normals = tuple(sorted(map(tuple, atlas['normals'])))
                if id in admitted:
                    assert normals == tuple(map(tuple, admitted[id]['normals']))
                for mask in atlas['masks']:
                    assert mask in four and mask not in atlas_by_mask
                    atlas_by_mask[mask] = id
                    closed = rows[mask]['closed_rows_mask']
                    if closed not in cache:
                        cache[closed] = normals_for(closed, m)
                    perm = coordinate_permutation(cache[closed], normals)
                    bindings.append({'mask': mask, 'atlas': id, 'coordinate_permutation': perm, 'complete_original_rows_verified': True, 'metric_admitted': id in admitted})
            assert set(atlas_by_mask) == four and source['four_coordinate_masks'] == len(four)
            assert {(x, int(id.split('-A')[1])) for x, id in atlas_by_mask.items()} == set(map(tuple, source['mask_map']))
            seen = {}
            certified = set()
            for row in words[str(n)]:
                assert isinstance(row, list) and len(row) == 6
                mask, image, dual, outer, step, atlas = row
                assert mask not in seen and 0 <= mask < len(rows) and (dual in (0, 1)) and (outer in (0, 1, 2)) and (step in (1, 2))
                assert word_image(mask, n, dual, outer, step) == image and image in atlas_by_mask
                id = f'R{n}-A{atlas:04d}'
                assert atlas_by_mask[image] == id and id in admitted
                seen[mask] = row
                certified.add(mask)
            all_image_eligible = {mask for mask in rows if any((atlas_by_mask.get(image) in admitted for image in images(mask, n)))}
            assert certified <= all_image_eligible
            expected_count = {6: 1887, 7: 20384}[n]
            assert len(certified) == expected_count
            scores = [int(mask in certified) for mask in range(len(rows))]
            path = Path(entry['admitted_output'])
            assert not path.exists()
            path.write_text(str(len(scores)) + '\n' + ' '.join(map(str, scores)) + '\n')
            result['strata'].append({'rank': n, 'full_four_masks': len(four), 'full_normal_atlases': len(source['normal_atlases']), 'verified_bindings': bindings, 'source_admitted_masks': len(certified), 'all_image_eligible_masks': len(all_image_eligible), 'additional_valid_images_not_used_in_source_cover': sorted(all_image_eligible - certified), 'exact_source_mask_words': list(seen.values()), 'admitted_bitmap': {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}})
            save()
            print(json.dumps({k: result['strata'][-1][k] for k in ['rank', 'full_four_masks', 'full_normal_atlases', 'source_admitted_masks', 'all_image_eligible_masks']}), flush=True)
        result.update(status='complete', seconds=time.monotonic() - start, scope='Every metric normal list is bound to the complete integral mask chart; source mask-word predicate reproduced exactly, with no extra population silently added')
        save()
