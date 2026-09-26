"""Complete original-subset, exact-BV and sparse-field replay; standard library."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import gzip,json,time,copy,sys
from geometry import construct_normals,full_image_index,safe_type,gram,controls
from arithmetic import bv
ROOT=Path(__file__).resolve().parent

def field_values(normals,own,data):
    assert data['normals']==[list(r) for r in normals] and data['dimension']==9 and F(data['epsilon'])==F(1,1000000)
    field={}
    for rec in data['field']:
        s=tuple(rec['support']);v=tuple(map(F,rec['ambient']))
        assert s==tuple(sorted(set(s))) and len(s)==6 and s in own and own[s]['image_index']==1
        assert s not in field and len(v)==9 and any(v)
        assert all(sum(a*b for a,b in zip(normals[i],v))==0 for i in s)
        field[s]=v
    assert len(field)==70
    values=[];incidences=0
    for ids in combinations(range(16),7):
        r=own[ids]
        if not r['image_index']:continue
        x=F(r['numerator'],r['denominator'])
        for i in ids:
            support=tuple(j for j in ids if j!=i);assert own[support]['image_index']==1
            x+=sum(a*b for a,b in zip(normals[i],field.get(support,[F(0)]*9)));incidences+=1
        values.append(x)
    assert len(values)==7830 and incidences==54810
    assert values==list(map(F,data['full_corrected_values']))
    assert min(values)==F(26684096221433977,2668409622144333204480)>F(1,1000000)
    return values

def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for five-capacity replay')
    start=time.monotonic();normals,_,_=construct_normals();bad_controls=controls()
    records=[json.loads(s) for s in gzip.decompress((ROOT/'data/subsets.jsonl.gz').read_bytes()).decode().splitlines()]
    assert len(records)==26332
    own={};types={};ind=0;dep=0;ordinal=0
    for q in range(1,8):
        for ids in combinations(range(16),q):
            r=records[ordinal];assert r['subset_ordinal']==ordinal and r['normal_indices']==list(ids) and r['q']==q;ordinal+=1
            rows=tuple(normals[i] for i in ids);image=full_image_index(rows)
            assert r['rank']==image['rank'] and r['image_index']==image['image_index']
            if image['image_index']:
                assert image['image_index']==1;tid,key,order=safe_type(rows,1)
                assert r['type_id']==tid and r['canonical_generator_order']==list(order)
                types.setdefault(tid,key);ind+=1
            else:dep+=1
            assert ids not in own;own[ids]=r
    assert (ordinal,ind,dep,len(types))==(26332,20823,5509,961)
    listed=json.loads((ROOT/'data/types.json').read_text());expected=json.loads((ROOT/'data/values.json').read_text())
    assert len(listed)==len(expected)==961 and {x['type_id'] for x in listed}==set(types)
    values={}
    for ordinal,(typ,exp) in enumerate(zip(listed,expected)):
        tid=typ['type_id'];assert typ['type_ordinal']==exp['type_ordinal']==ordinal and exp['type_id']==tid
        assert json.loads(json.dumps(types[tid]))==typ['key']
        rows=tuple(normals[i] for i in typ['representative_normal_indices'])
        assert safe_type(rows,full_image_index(rows)['image_index'])[0]==tid
        for base in (37,41,43):
            try:value,evidence=bv(tuple(map(tuple,typ['key']['gram'])),base=base);break
            except ValueError as e:
                if 'Nongeneric specialization' not in str(e):raise
        else:raise ValueError('All exact specializations refused')
        assert value==F(exp['value'])==F(exp['numerator'],exp['denominator'])
        values[tid]=value
    for r in records:
        if r['image_index']:
            v=values[r['type_id']];assert v==F(r['numerator'],r['denominator'])==F(r['value'])
            if r['q']<7:assert v>F(1,1000000)
    data=json.loads((ROOT/'data/field.json').read_text());result=field_values(normals,own,data)
    bad=copy.deepcopy(data);support=bad['field'][0]['support'];coordinate=next(i for i,x in enumerate(normals[support[0]]) if x)
    bad['field'][0]['ambient'][coordinate]=str(F(bad['field'][0]['ambient'][coordinate])+1)
    try:field_values(normals,own,bad)
    except AssertionError:pass
    else:raise AssertionError('Broken annihilation accepted')
    bad=copy.deepcopy(data);bad['full_corrected_values'][0]=str(F(bad['full_corrected_values'][0])+1)
    try:field_values(normals,own,bad)
    except AssertionError:pass
    else:raise AssertionError('Changed corrected value accepted')
    print(json.dumps({'status':'PASS_COMPLETE_FINITE_PREMISES','subsets':26332,'independent':ind,'dependent':dep,'types':961,'field_rows':7830,'incidences':54810,'nonzero_supports':70,'minimum':str(min(result)),'geometry_controls':bad_controls,'field_negative_controls':2,'seconds':time.monotonic()-start}))
if __name__=='__main__':main()
