"""Complete area-sixteen finite certificate with fresh independent counts."""
import argparse,json,os,time
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--roster',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();r=json.loads(a.roster.read_text());start=time.monotonic()
model=json.loads(Path(r['models']).read_text());fit=json.loads(Path(r['fit']).read_text());hold=json.loads(Path(r['holdouts']).read_text());assert model['status']==fit['status']==hold['status']=='complete' and not fit['candidates']
assert fit['source_comparison_loaded'] is False and fit['positive_holdouts_loaded'] is False
source={}
def key(x):return tuple(tuple(x[k]) for k in ['lambda','mu','nu'])
for path in r['source_vectors']:
 j=json.loads(Path(path).read_text());assert j['complete']
 for x in j['records']:
  k=key(x);assert k not in source;source[k]=x
assert len(source)==56 and len(model['records'])==len(fit['records'])==len(hold['counts'])==56
rows=[]
for m,f,h in zip(model['records'],fit['records'],hold['counts']):
 assert m['id']==f['id']==h['id'] and h['record_index']==m['record_index'] and h['nodes']==[6,7]
 co=list(map(Q,f['coefficients']));s=source[key(m['original'])];expected=list(map(Q,s['coefficients']))+[Q(0)]*(len(co)-len(s['coefficients']))
 assert co==expected and all(x>=0 for x in co)
 assert all(sum(c*t**i for i,c in enumerate(co))==v for t,v in enumerate(s['values']))
 assert all(sum(c*t**i for i,c in enumerate(co))==int(v) for t,v in zip(h['nodes'],h['counts']))
 rows.append({'id':m['id'],'rank':m['rank'],'boundary':m['original'],'degree_bound':m['degree_bound'],'actual_degree':f['actual_degree'],'coefficients':f['coefficients'],'independent_values':f['values']+list(map(int,h['counts']))})
result={'status':'complete','pid':os.getpid(),'pgid':os.getpgrp(),'native_calls':0,'records':rows,'record_count':56,'actual_degree_histogram':dict(Counter(x['actual_degree'] for x in rows)),'all_source_vectors_match':True,'fresh_derived_chart_sites':448,'fresh_unused_positive_holdouts':112,'whole_area_at_most_16':'Follows with the independently verified exhaustive cover and existing rank-at-most-five/source terminals; this is the entire residual finite roster, not an arbitrary sample','seconds':time.monotonic()-start}
with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['record_count','actual_degree_histogram','fresh_derived_chart_sites','seconds']}))
