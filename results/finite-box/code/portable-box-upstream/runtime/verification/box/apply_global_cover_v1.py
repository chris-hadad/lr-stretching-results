"""Independent full-key application of verified sign terminals and exact residue."""
import argparse
from collections import Counter, defaultdict
import hashlib, json, os, time
from pathlib import Path

def run(a):
    r = json.loads(a.roster.read_text())
    start = time.monotonic()
    for name in ['census6', 'census7']:
        j = json.loads(Path(r[name]).read_text())
        assert j['status'] == 'complete' and j['residual_exact_match'] and j['enumeration_performed']
    mapdoc = json.loads(Path(r['map_report']).read_text())
    assert mapdoc['status'] == 'PASS' and mapdoc['mode'] == 'full' and (mapdoc['original6_transformations_verified'] == 1615508) and (mapdoc['original7_transformations_verified'] == 3728012)
    small = json.loads(Path(r['small_certificate']).read_text())
    quarter = json.loads(Path(r['quartic_certificate']).read_text())
    binding = json.loads(Path(r['metric_binding']).read_text())
    assert small['status'] == quarter['status'] == binding['status'] == 'complete'
    qrows = {x['id']: x for x in quarter['records']}
    assert len(qrows) == 10348
    scores = {}
    admitted = {}
    for n in [6, 7]:
        x = list(map(int, Path(r[f'scores{n}']).read_text().split()))
        assert x[0] == 1 << 3 * (n - 1) and len(x) == x[0] + 1
        scores[n] = x[1:]
        x = list(map(int, Path(r[f'admitted{n}']).read_text().split()))
        assert x[0] == len(scores[n]) and len(x) == x[0] + 1 and (set(x[1:]) <= {0, 1})
        admitted[n] = x[1:]
    source_new = {}
    with Path(r['source_new_keys']).open() as f:
        assert next(f).rstrip('\n') == 'global_id\tarea\tmask\trank6_preimages\trank7_preimages'
        for line in f:
            id, area, mask, p6, p7 = map(int, line.split())
            assert id not in source_new
            source_new[id] = (area, mask, p6, p7)
    assert len(source_new) == 801555
    result = {'status': 'running', 'pid': os.getpid(), 'pgid': os.getpgrp(), 'native_calls': 0, 'branches': {}, 'source_new_matched': 0}
    counts = {k: {'keys': 0, 'rank6_keys': 0, 'rank7_keys': 0, 'original_rank6': 0, 'original_rank7': 0} for k in ['small', 'metric', 'quartic', 'remaining']}
    hist = Counter()
    area_hist = Counter()
    last = 0
    quartic_seen = set()
    panel = []
    panel_masks = defaultdict(set)
    totals = [0, 0]
    expected_bound = {}
    residual = Path(r['residual_output'])
    assert not residual.exists()
    with a.output.open('x') as out, residual.open('x') as residual_file, Path(r['global_keys']).open() as inp:

        def save():
            out.seek(0)
            json.dump(result, out, indent=2)
            out.write('\n')
            out.truncate()
            out.flush()
            os.fsync(out.fileno())
        save()
        assert next(inp).rstrip('\n') == 'id\trank\tlambda\tmu\tnu\toriginal_rank6_preimages\toriginal_rank7_preimages'
        residual_file.write('id\trank\tlambda\tmu\tnu\toriginal_rank6_preimages\toriginal_rank7_preimages\tcoordinate_bound\n')
        for line in inp:
            fields = line.rstrip('\n').split('\t')
            assert len(fields) == 7
            id = int(fields[0])
            n = int(fields[1])
            assert id == last + 1 and n in (6, 7)
            last = id
            parts = [tuple(map(int, x.split(','))) for x in fields[2:5]]
            assert all((len(x) == n and all((0 <= z <= 30 for z in x)) and all((x[i] >= x[i + 1] for i in range(n - 1))) for x in parts))
            area = sum(parts[0])
            assert area == sum(parts[1]) + sum(parts[2]) <= 30
            p6, p7 = map(int, fields[5:])
            assert min(p6, p7) >= 0 and p6 + p7 > 0
            totals[0] += p6
            totals[1] += p7
            mask = 0
            for side, q in enumerate(parts):
                for i in range(n - 1):
                    if q[i] == q[i + 1]:
                        mask |= 1 << side * (n - 1) + i
            bound = scores[n][mask]
            if area <= 16:
                kind = 'small'
            elif admitted[n][mask]:
                kind = 'metric'
                assert source_new.pop(id) == (area, mask, p6, p7)
                result['source_new_matched'] += 1
            elif id in qrows:
                kind = 'quartic'
                q = qrows[id]
                assert q['rank'] == n and q['degree'] == 4 and (q['preimages'] == [p6, p7]) and (bound == 4)
                assert [tuple(q['boundary'][k]) for k in ['lambda', 'mu', 'nu']] == parts
                quartic_seen.add(id)
            else:
                kind = 'remaining'
                assert bound >= 5
                residual_file.write(line.rstrip('\n') + '\t' + str(bound) + '\n')
                hist[n, bound] += 1
                area_hist[n, area] += 1
                bucket = (n, area)
                if bound == 5 and len(panel_masks[bucket]) < 8 and (mask not in panel_masks[bucket]):
                    panel_masks[bucket].add(mask)
                    panel.append({'id': id, 'rank': n, 'lambda': parts[0], 'mu': parts[1], 'nu': parts[2], 'area': area, 'degree_bound': 5, 'mask': mask, 'preimages': [p6, p7]})
            c = counts[kind]
            c['keys'] += 1
            c[f'rank{n}_keys'] += 1
            c['original_rank6'] += p6
            c['original_rank7'] += p7
            if id % 1000000 == 0:
                result['processed_keys'] = id
                result['branches'] = counts
                save()
        assert last == 4747974 and totals == [1615508, 3728012] and (not source_new) and (quartic_seen == set(qrows))
        assert counts['small']['keys'] == 56 and counts['metric']['keys'] == 801555 and (counts['quartic']['keys'] == 10348) and (counts['remaining']['keys'] == 3936015)
        assert counts['remaining']['original_rank6'] + counts['remaining']['original_rank7'] == 4360228
        assert sum((v for (n, b), v in hist.items() if b == 5)) == 1279898
        residual_file.flush()
        os.fsync(residual_file.fileno())
        panel_path = Path(r['pricing_panel_output'])
        assert not panel_path.exists()
        panel_path.write_text(json.dumps({'selection': 'First eight distinct original masks per evaluation-rank/area bin in verified global order, restricted to bound five; bounded method pricing, not representative sampling or a full-layer search.', 'records': panel}, indent=2) + '\n')
        result.update(status='complete', processed_keys=last, branches=counts, original_preimages=totals, remaining_bound_histogram={str(n): {str(b): v for (nn, b), v in sorted(hist.items()) if nn == n} for n in [6, 7]}, remaining_area_histogram={str(n): {str(area): v for (nn, area), v in sorted(area_hist.items()) if nn == n} for n in [6, 7]}, residual={'path': str(residual), 'sha256': hashlib.sha256(residual.read_bytes()).hexdigest(), 'bytes': residual.stat().st_size}, pricing_panel={'path': str(panel_path), 'sha256': hashlib.sha256(panel_path.read_bytes()).hexdigest(), 'records': len(panel)}, seconds=time.monotonic() - start, scope='Complete conservative cover under the exact verified P08/P09/P10 predicates, not minimal feasible unknown population and not a whole-box sign conclusion')
        save()
        print(json.dumps({'branches': counts, 'seconds': result['seconds'], 'pricing_panel_records': len(panel)}), flush=True)
