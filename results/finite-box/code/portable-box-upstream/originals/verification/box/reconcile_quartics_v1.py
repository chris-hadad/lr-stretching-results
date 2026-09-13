"""Bind every fresh full-chart polynomial and unused holdout to its source identity."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import json,os,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--roster',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();r=json.loads(a.roster.read_text());start=time.monotonic()
fit=json.loads(Path(r['fit']).read_text());hold=json.loads(Path(r['holdouts']).read_text());models=json.loads(Path(r['models']).read_text())
assert fit['status']==hold['status']==models['status']=='complete' and not fit['candidates']
assert fit['source_comparison_loaded'] is False and fit['positive_holdouts_loaded'] is False
wanted=models['expected_ids'];assert len(wanted)==10348 and len(set(wanted))==10348
source={}
for line in Path(r['primary']).read_text().splitlines():
 row=json.loads(line);assert row['id'] not in source;source[row['id']]=row
assert set(source)==set(wanted)
assert [x['id'] for x in fit['records']]==wanted
holds={int(x['id']):x for x in hold['counts']};assert len(holds)==len(hold['counts'])==len(wanted) and set(holds)==set(wanted)
records=[];classes=Counter();preimages=[0,0];positive=[]
for m,row in zip(models['records'],fit['records']):
 id=row['id'];s=source[id];h=holds[id];co=list(map(Q,row['coefficients']))
 assert row['state']=='nonempty' and row['actual_degree']==4 and len(co)==5 and all(x>0 for x in co)
 assert row['original_boundary']=={k:s[k] for k in ['lambda','mu','nu']} and row['rank']==s['rank'] and row['preimages']==s['preimages']
 assert s['degree_bound']==s['actual_degree']==4 and s['determining_nodes']==[0,1,2,3,4] and s['unused_positive_holdouts']==[5,6]
 assert h['nodes']==[5,6] and h['record_index']==m['record_index'] and h['dimension']==4
 assert all(sum(c*Q(t)**i for i,c in enumerate(co))==int(v) for t,v in zip(h['nodes'],h['counts']))
 assert co==list(map(Q,s['coefficients'])) and row['values']+list(map(int,h['counts']))==s['values']
 classes[tuple(map(str,co))]+=1
 for i,x in enumerate(row['preimages']):preimages[i]+=x
 positive.extend((c,id,i) for i,c in enumerate(co) if i)
 records.append({'id':id,'boundary':row['original_boundary'],'rank':row['rank'],'preimages':row['preimages'],'degree':4,'coefficients':list(map(str,co)),'unused_positive_holdouts':dict(zip([5,6],map(int,h['counts']))),'whole_chart_second_model':True})
result={'status':'complete','pid':os.getpid(),'pgid':os.getpgrp(),'native_calls':0,'expected_ids':wanted,'records':records,
 'record_count':len(records),'positive_nonconstant_coefficients':len(positive),'distinct_vectors':len(classes),
 'minimum_positive':{'value':str(min(positive)[0]),'id':min(positive)[1],'index':min(positive)[2]},
 'independent_whole_chart_count_sites':7*len(records),'unused_positive_holdouts':2*len(records),
 'original_preimages_by_rank':preimages,'original_preimages':sum(preimages),'source_vectors_all_equal':True,
 'missing_full_second_count_debt_closed':True,'historical_process_waits_reconstructed':False,
 'algorithmic_independence':'Fresh saturated-hive-chart Fourier-Motzkin lattice enumeration versus provider row-block LR tableaux; exact arithmetic shared, not independent arithmetic hardware.',
 'scope':'Every P09 quartic exception is independently positive. Complete global box coverage and original-to-key maps are separate prerequisites.',
 'seconds':time.monotonic()-start}
assert len(classes)==24 and preimages==[6177,7153] and min(positive)[0]==Q(1,24)
with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['record_count','positive_nonconstant_coefficients','distinct_vectors','independent_whole_chart_count_sites','unused_positive_holdouts','original_preimages','seconds']}))
