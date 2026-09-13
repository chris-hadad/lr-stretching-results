"""Full small-area vectors, persisted before independent holds or source comparison."""
import argparse,json,os,time
from fractions import Fraction as Q
from pathlib import Path

def interpolate(v):
 dif=list(map(Q,v));first=[]
 while dif:first.append(dif[0]);dif=[b-a for a,b in zip(dif,dif[1:])]
 out=[Q(0)]*len(v);basis=[Q(1)]
 for k,c in enumerate(first):
  for i,x in enumerate(basis):out[i]+=c*x
  new=[Q(0)]*(len(basis)+1)
  for i,x in enumerate(basis):new[i]-=Q(k,k+1)*x;new[i+1]+=x/Q(k+1)
  basis=new
 return out
p=argparse.ArgumentParser();p.add_argument('--roster',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();r=json.loads(a.roster.read_text());models=json.loads(Path(r['models']).read_text());counts=json.loads(Path(r['counts']).read_text());assert models['status']==counts['status']=='complete';assert len(models['records'])==len(counts['counts'])==56
result={'status':'running','pid':os.getpid(),'pgid':os.getpgrp(),'native_calls':0,'records':[],'candidates':[],'source_comparison_loaded':False,'positive_holdouts_loaded':False}
with a.output.open('x') as f:
 def save():f.seek(0);json.dump(result,f,indent=2);f.write('\n');f.truncate();f.flush();os.fsync(f.fileno())
 save()
 for m,c in zip(models['records'],counts['counts']):
  assert m['id']==c['id'] and m['record_index']==c['record_index'] and c['nodes']==list(range(6))
  values=list(map(int,c['counts']));assert values[0]==1 and values[1]>0
  co=interpolate(values);assert all(co[i]==0 for i in range(m['degree_bound']+1,len(co)))
  row={'id':m['id'],'original':m['original'],'rank':m['rank'],'degree_bound':m['degree_bound'],'values':values,'coefficients':[str(x) for x in co],'actual_degree':max(i for i,x in enumerate(co) if x)};result['records'].append(row)
  if any(x<0 for x in co):result['candidates'].append(row);result['status']='candidate_interrupt';save();raise SystemExit(3)
 result['status']='complete';save()
print(json.dumps({'status':'complete','records':len(result['records'])}))
