"""Every frozen A71 F/J fixture and determining/unused grade, exact root cell arithmetic."""
import argparse,json,pathlib,time
from collections import Counter
import pro050_math as m
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
r=pathlib.Path(__file__).resolve().parents[1];d=json.loads((r/'data/pro050/DOMAIN.json').read_text())
assert d['fixtures']==m.expected_domain();rows=[];counts=Counter();cells=0;grades=0;started=time.monotonic()
for fixture in d['fixtures']:
 m.validate_fixture(fixture);build=m.cell_F if fixture['family']=='F' else m.cell_J;direct=m.direct_F if fixture['family']=='F' else m.direct_J
 seen=[];poly,coverage,bound=build(fixture,d['caps'],seen.append);cells+=len(seen)
 assert all(c>=0 for c in poly)
 for t in range(bound+3):
  value,_=direct(fixture,t,d['caps']['direct_terms_per_grade']);assert m.evaluate(poly,t)==value;(counts.update([fixture['family']]))
  grades+=1
 rows.append(dict(id=fixture['id'],bound=bound,coefficients=list(map(str,poly)),coverage=coverage,unused_grades=[bound+1,bound+2]))
assert len(rows)==1224 and cells==23940
with open(a.out,'x') as f:json.dump(dict(status='PASS',fixtures=len(rows),cells=cells,grades=grades,rows=rows,seconds=time.monotonic()-started),f,indent=2)
print(json.dumps(dict(status='PASS',fixtures=len(rows),cells=cells,grades=grades,seconds=time.monotonic()-started)))
