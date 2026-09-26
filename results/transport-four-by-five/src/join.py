"""Complete fresh cover/field, actual-degree, BV and whole-baseline joins."""
from pathlib import Path
from fractions import Fraction as F
from functools import reduce
from math import gcd
import json, struct, sys
from portable_io import save

DEN = 479001600
TOTALS = {'U': 591214, 'F': 41482}
EXPECTED_C3 = {
    (2, 4, 4): '1/6', (2, 5, 5): '5/12', (3, 3, 3): '3/4', (3, 3, 4): '1',
    (3, 4, 4): '11/4', (3, 4, 5): '49/16', (3, 5, 5): '169/32',
    (3, 5, 6): '4037/720', (4, 2, 4): '1/6', (4, 3, 4): '11/4',
    (4, 3, 5): '49/16', (4, 4, 4): '35117/5670', (4, 4, 5): '797089/90720',
    (4, 4, 6): '13777/1512', (4, 5, 5): '5005039/362880',
    (4, 5, 6): '221771/13440', (4, 5, 7): '1271281/75600',
}


def dimension(ray):
    assert len(ray) == 8 and all(type(x) is int and x >= 0 for x in ray)
    assert ray[7] > 0 and reduce(gcd, ray) == 1
    rows = list(ray[:3]) + [ray[7] - sum(ray[:3])]
    columns = list(ray[3:7]) + [ray[7] - sum(ray[3:7])]
    assert rows == sorted(rows, reverse=True) and columns == sorted(columns, reverse=True)
    assert min(rows + columns) >= 0
    return max(sum(x > 0 for x in rows) - 1, 0) * max(sum(x > 0 for x in columns) - 1, 0)


def interpolate(values):
    assert len(values) == 15 and all(type(v) is int and v >= 0 for v in values)
    differences = values[:13]
    newton = []
    while differences:
        newton.append(differences[0])
        differences = [b-a for a,b in zip(differences, differences[1:])]
    ordinary = [F(0)] * 13
    basis = [F(1)]
    for degree, value in enumerate(newton):
        for i, coefficient in enumerate(basis):
            ordinary[i] += value * coefficient
        if degree < 12:
            following = [F(0)] * (len(basis) + 1)
            for i, coefficient in enumerate(basis):
                following[i] -= F(degree, degree + 1) * coefficient
                following[i+1] += F(1, degree + 1) * coefficient
            basis = following
    return ordinary


def baselines(data, work):
    roster = json.loads((data / 'baseline/BASELINE-ROSTER.json').read_text())['cases']
    assert len(roster) == 17
    literal = [tuple(line.split()) for line in (data / 'baseline/INPUT.txt').read_text().splitlines()]
    expected = [(case['id'], *map(str, (t, *case['rows'], *case['columns'])))
                for case in roster for t in range(15)]
    assert literal == expected and len(literal) == 255
    counts = {}
    for line in (work / 'baselines.txt').read_text().splitlines():
        row = line.split()
        assert len(row) == 5
        identity, grade = row[0], int(row[1])
        value, additions, maximum = map(int, row[2:])
        assert min(value, additions, maximum) >= 0 and 0 <= grade <= 14
        assert (identity, grade) not in counts
        counts[identity, grade] = value
    assert set(counts) == {(case['id'], t) for case in roster for t in range(15)}
    vectors = []
    seen = set()
    for case in roster:
        p,n,total = case['p'],case['N'],case['total']
        key = (p,n,total)
        assert key in EXPECTED_C3 and key not in seen and case['grades'] == list(range(15))
        seen.add(key)
        rows = [total-p+1] + [1]*(p-1) + [0]*(4-p)
        columns = [total-n+1] + [1]*(n-1) + [0]*(5-n)
        assert case['rows'] == rows and case['columns'] == columns
        values = [counts[case['id'],t] for t in range(15)]
        vector = interpolate(values)
        record = {'id':case['id'],'rows':rows,'columns':columns,'counts':values,
                  'coefficients':list(map(str,vector)),'status':'RECONSTRUCTED_UNCHECKED'}
        save(work / ('baseline-unchecked-' + case['id'] + '.json'), record)
        if any(v < 0 for v in vector):
            raise ArithmeticError('Preserved whole-baseline negative at ' + case['id'])
        degree = (p-1)*(n-1)
        assert vector[0] == 1 and all(v == 0 for v in vector[degree+1:])
        assert vector[3] == F(EXPECTED_C3[key]) > 0
        for t in (13,14):
            assert sum(v*t**i for i,v in enumerate(vector)) == values[t]
        vectors.append(record)
    assert seen == set(EXPECTED_C3)
    return vectors


def local_values(data, work, module):
    records = json.loads((data / 'local-certificate.json').read_text())
    expected = {f'T{r["p"]}-{r["N"]}-{r["q"]}-{r["type"]}': F(r['alpha']) for r in records}
    assert len(records) == len(expected) == 317
    def parse(path):
        values = {}
        for line in path.read_text().splitlines():
            row = line.split()
            assert len(row) == 7 and row[0] not in values and int(row[1]) == 1
            values[row[0]] = F(row[2])
        return values
    actual = parse(work / 'bv-values.txt')
    assert actual == expected and min(actual.values()) > F(1,1000)
    control = parse(work / 'bv-controls.txt')
    correct = {k:F(v) for k,v in json.loads((module/'src/CONTROL-EXPECTATIONS.json').read_text())['values'].items()}
    assert control == correct
    damaged = parse(work / 'bv-omit-eighth.txt')
    assert set(damaged) == set(correct) and damaged['SIMPLEX-8'] != correct['SIMPLEX-8']
    return {'types':317,'minimum':str(min(actual.values())),'analytic_controls':len(correct),
            'eighth_order_omission_detected':True}


def join(data, work, module):
    roster = json.loads((module / 'batches.json').read_text())
    assert len(roster) == 52
    joined = {}
    for kind in ('cover','fields'):
        selected = []
        for job in roster:
            if job['kind'] != kind:
                continue
            folder = work / f'{kind}-{job["part"]}-{job["lo"]:06d}-{job["hi"]:06d}'
            name = 'COVER-BATCH.json' if kind == 'cover' else 'FIELD-BATCH.json'
            report = json.loads((folder/name).read_text())
            assert report['schema'] == f'pro030-independent-{kind[:-1] if kind=="fields" else kind}-batch/v1'
            assert report['status'] == 'PASS'
            assert (report['part'],report['lo'],report['hi']) == (job['part'],job['lo'],job['hi'])
            assert report['cells'] == job['hi']-job['lo']
            selected.append((folder,report))
        assert len(selected) == 26
        for part,total in TOTALS.items():
            cursor = 0
            for _,report in sorted((x for x in selected if x[1]['part']==part),key=lambda x:x[1]['lo']):
                assert report['lo'] == cursor and cursor < report['hi'] <= total
                cursor = report['hi']
            assert cursor == total
        joined[kind] = selected
    signatures = set()
    volume = F(0)
    simplex_count = 0
    for folder,report in joined['cover']:
        path = folder/'signatures.bin'
        assert path.stat().st_size == 40*report['cells']
        with path.open('rb') as stream:
            for identity in range(report['lo'],report['hi']):
                raw = stream.read(40)
                cid,a,b,c,d = struct.unpack('<q4Q',raw)
                assert cid == identity and d>>18 == 0 and raw[8:] not in signatures
                signatures.add(raw[8:])
            assert not stream.read(1)
        numerator = simplices = count = 0
        with (folder/'volumes.txt').open() as stream:
            for identity,line in enumerate(stream,report['lo']):
                row = list(map(int,line.split()))
                assert len(row)==4 and row[0]==identity and row[1]>=8 and min(row[2:])>0
                count+=1;simplices+=row[2];numerator+=row[3]
        assert count==report['cells'] and simplices==report['simplices'] and numerator==int(report['volume_numerator'])
        volume += F(numerator,int(report['denominator']))
        simplex_count += simplices
    assert len(signatures)==632696 and simplex_count==4209661 and volume==F(7,576)
    rays = {}
    counters = {k:0 for k in ('pairs','triples','ray_occurrences','positions','assignment_visits',
                             'c2_column_checks','c2_row_checks','c3_column_checks','c3_row_checks')}
    for folder,report in joined['fields']:
        path=folder/'fields.bin'
        assert path.stat().st_size==32+report['cells']*166*8
        with path.open('rb') as stream:
            assert struct.unpack('<4q',stream.read(32))==(report['lo'],report['hi'],165,DEN)
        assert report['positions']==report['cells']*165 and report['assignment_visits']==report['cells']*1024
        assert report['c2_column_checks']==10*report['ray_occurrences'] and report['c2_row_checks']==6*report['ray_occurrences']
        assert report['c3_column_checks']==10*report['pairs'] and report['c3_row_checks']==6*report['pairs']
        for key in counters:counters[key]+=report[key]
        seen=set();occurrences=0
        with (folder/'rays.txt').open() as stream:
            for line in stream:
                row=list(map(int,line.split()));assert len(row)==13
                identity=row[0];ray=tuple(row[1:9]);d,q2,q3,occ=row[9:]
                assert identity not in seen and occ>0 and min(q2,q3)>=0 and d==dimension(ray)
                seen.add(identity);occurrences+=occ
                value=(d,q2,q3)
                assert ray not in rays or rays[ray]==value
                rays[ray]=value
        assert occurrences==report['ray_occurrences'] and len(seen)==report['distinct_rays_in_batch']
    assert counters['pairs']==46616414 and counters['triples']==248939603
    assert counters['ray_occurrences']==7008446 and len(rays)==15573
    q2data=json.loads((data/'source/UNIT04/DATA/GLOBAL-RAY-QUADRATICS.json').read_text())['records']
    q3data=json.loads((data/'source/UNIT05/DATA/GLOBAL-RAY-CUBICS.json').read_text())['records']
    q2rows={tuple(r['coordinates']):(r['actual_dimension'],r['c2_numerator']) for r in q2data}
    q3rows={tuple(r['ray']):(r['actual_dimension'],int(r['numerator_over_6_factorial12'])) for r in q3data}
    assert len(q2rows)==len(q2data)==len(q3rows)==len(q3data)==15573
    assert set(q2rows)==set(q3rows)==set(rays) and all(r['denominator']==DEN for r in q2data)
    for ray,(d,q2,q3) in rays.items():
        assert q2rows[ray]==(d,q2) and q3rows[ray]==(d,6*q3)
        assert not(d<2 and q2) and not(d<3 and q3)
    z2={r:v[0] for r,v in rays.items() if v[1]==0};segment=(1,1,0,1,1,0,0,2)
    assert len(z2)==9 and z2.get(segment)==1 and all(d==0 for r,d in z2.items() if r!=segment)
    z3={r:v[0] for r,v in rays.items() if v[2]==0}
    assert len(z3)==15 and all(d<3 for d in z3.values())
    vectors=baselines(data,work);bv=local_values(data,work,module)
    return {'status':'PASS_COMPLETE_FINITE_PREMISES','cells':632696,'simplices':4209661,
            'seven_factorial_volume':str(volume),'volume':'1/414720','rays':15573,
            'counters':counters,'baseline_vectors':len(vectors),'ordinary_positions':221,
            'unused_whole_counts':34,'higher_local_values':bv}


if __name__ == '__main__':
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for transport join')
    data,work,module=map(Path,sys.argv[1:])
    result=join(data,work,module)
    save(work/'RESULT.json',result)
    print(json.dumps(result),flush=True)
