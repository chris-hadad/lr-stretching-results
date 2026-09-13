"""Full independent score, Horn-index and generating-function source verification."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import time
from mask_model_v1 import images
from slr_ehrhart.horn import index_partition, lr_tableaux

def part_counts(n):
    size = 1 << n - 1
    direct = [[0] * 31 for _ in range(size)]
    zero = [[0] * 31 for _ in range(size)]

    def visit(parts, left, upper, slots):
        if left == 0:
            q = parts + [0] * slots
            m = sum((1 << i for i in range(n - 1) if q[i] == q[i + 1]))
            area = sum(parts)
            direct[m][area] += 1
            if q[-1] == 0:
                zero[m][area] += 1
            return
        if not slots:
            return
        for x in range(1, min(left, upper) + 1):
            visit(parts + [x], left - x, x, slots - 1)
    for area in range(31):
        visit([], area, area, n)
    for mask in range(size):
        steps = [i + 1 for i in range(n - 1) if not mask & 1 << i]
        base = sum(steps)

        def series(weights):
            a = [0] * 31
            if base <= 30:
                a[base] = 1
            for w in weights:
                for j in range(w, 31):
                    a[j] += a[j - w]
            return a
        assert direct[mask] == series(steps + [n]) and zero[mask] == series(steps)
    return (direct, zero)

def verify_cover(n, scores, expected):
    full, zero = part_counts(n)
    size = len(full)
    hist = Counter()
    profiles = {x['mask']: x for x in expected['mask_profiles']}
    seen = set()
    for mu in range(size):
        for nu in range(size):
            conv = [0] * 31
            conv0 = [0] * 31
            for total in range(2, 31):
                conv[total] = sum((full[mu][a] * full[nu][total - a] for a in range(1, total)))
                conv0[total] = sum((zero[mu][a] * zero[nu][total - a] for a in range(1, total)))
            for lam in range(size):
                mask = lam + (mu << n - 1) + (nu << 2 * (n - 1))
                ordered = sum((full[lam][a] * conv[a] - zero[lam][a] * conv0[a] for a in range(2, 31)))
                diagonal = 0
                if mu == nu:
                    diagonal = sum((full[lam][a] * full[mu][a // 2] - zero[lam][a] * zero[mu][a // 2] for a in range(2, 31, 2)))
                if mask in profiles:
                    row = profiles[mask]
                    assert row['oriented_root_count'] == ordered and row['diagonal_root_count'] == diagonal, mask
                    assert row['chart_dimension_bound'] == scores[mask], mask
                    seen.add(mask)
                else:
                    assert ordered == diagonal == 0, (mask, ordered, diagonal)
                hist[scores[mask]] += ordered + diagonal
    assert seen == set(profiles)
    assert all((v % 2 == 0 for v in hist.values()))
    hist = {k: v // 2 for k, v in sorted(hist.items())}
    assert sum(hist.values()) == expected['total_roots']
    assert sum((v for k, v in hist.items() if k <= 3)) == expected['covered_by_dimension_at_most_three_certificate']
    return {'total_roots': sum(hist.values()), 'mask_terminal_roots': sum((v for k, v in hist.items() if k <= 3)), 'dimension_bound_histogram': hist, 'profile_count': len(profiles)}

def run(a):
    r = json.loads(a.roster.read_text())
    start = time.monotonic()
    out = {'status': 'running', 'pid': os.getpid(), 'pgid': os.getpgrp(), 'native_calls': 0, 'strata': []}
    with a.output.open('x') as f:

        def save():
            f.seek(0)
            json.dump(out, f, indent=2)
            f.write('\n')
            f.truncate()
            f.flush()
            os.fsync(f.fileno())
        save()
        inventory = json.loads(Path(r['accepted_horn_inventory']).read_text())['records_by_rank']
        for item in r['ranks']:
            n = item['rank']
            m = json.loads(Path(item['verified_masks']).read_text())
            assert m['status'] == 'complete' and m['rank'] == n
            assert [x['mask'] for x in m['records']] == list(range(1 << 3 * (n - 1)))
            direct = [x['dimension_bound'] for x in m['records']]
            scores = [min((direct[j] for j in images(mask, n))) for mask in range(len(direct))]
            expected = json.loads(Path(item['cover_source']).read_text())
            assert scores == expected['all_mask_scores']
            values = list(map(int, Path(item['score_source']).read_text().split()))
            assert values == [len(scores), *scores]
            for mask in range(len(direct)):
                w = n - 1
                L = mask & (1 << w) - 1
                mu = mask >> w & (1 << w) - 1
                nu = mask >> 2 * w
                assert scores[mask] == scores[L + (nu << w) + (mu << 2 * w)]
            checked = verify_cover(n, scores, expected)
            text = Path(item['score_output'])
            assert not text.exists()
            text.write_text(str(len(scores)) + '\n' + ' '.join(map(str, scores)) + '\n')
            hrows = [list(map(int, x.split())) for x in Path(item['horn_source']).read_text().splitlines()]
            assert hrows[0] == [len(hrows) - 1]
            horns = []
            for row in hrows[1:]:
                assert len(row) == 4
                k, im, jm, km = row
                assert 1 <= k < n
                indices = []
                for mask in [im, jm, km]:
                    assert mask >= 0 and mask < 1 << n and (mask.bit_count() == k)
                    indices.append(tuple((i + 1 for i in range(n) if mask & 1 << i)))
                I, J, K = indices
                assert lr_tableaux(index_partition(K, n), index_partition(I, n), index_partition(J, n)) == 1
                horns.append((I, J, K))
            assert len(horns) == len(set(horns)) == {6: 521, 7: 2042}[n]
            known = {(tuple(x['I']), tuple(x['J']), tuple(x['K'])) for x in inventory[str(n)]}
            assert set(horns) == known
            checked.update(rank=n, all_masks=len(scores), score_output=str(text), score_sha256=hashlib.sha256(text.read_bytes()).hexdigest(), verified_horn_indices=len(horns), tiny_index_counts='Proof-index tableaux only; no installed/native or whole-parent bare-LR oracle calls')
            out['strata'].append(checked)
            save()
            print(json.dumps(checked), flush=True)
        out.update(status='complete', seconds=time.monotonic() - start)
        save()
