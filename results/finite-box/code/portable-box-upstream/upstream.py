#!/usr/bin/env python3
"""Portable replay of the accepted F025 predecessor, with fresh local evidence.

prepare is metadata-only. run executes an explicit lane and its dependencies;
each child has a 120-second deadline. aggregate requires every exact planned
step, source identity, result and real clean exit. No old scientific receipt is
reused. External mathematical premises remain explicit in every final report.
"""
import argparse
from contextlib import contextmanager
import fcntl
import json
import math
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import common as U
import phases as P

def state_save(work,state):
 p=work/f'STATE.{os.getpid()}.tmp';U.save(p,state);os.replace(p,work/'STATE.json')
def report(work,kind,body):
 i=1
 while (work/f'{kind}-{i:06d}.json').exists():i+=1
 p=work/f'{kind}-{i:06d}.json';U.save(p,body);return U.pin(p)

def capture_adverse(ctx,item,step=None):
 identity=item['id'];U.need(re.fullmatch(r'f025-[0-9]{6}',identity),'Unsafe adverse observation attempt identity')
 if step is None:
  request_path=ctx.work/'requests'/(identity+'.json')
  try:step=U.read(request_path).get('step',{})
  except (OSError,ValueError,UnicodeError):step={}
 observations=P.durable_adverse(ctx.work/'jobs'/identity,step)
 holds=ctx.state.setdefault('mandatory_holds',{})
 if observations:
  old=holds.get(identity,{'attempt_id':identity,'step':step.get('id'),'requires_owner_disposition':True,
                          'authenticated_scientific_result':False,'observations':[]})
  unique={U.sha(U.encoded(r)):r for r in old['observations']}
  for row in observations:unique[U.sha(U.encoded(row))]=row
  new={**old,'observations':list(unique.values())}
  if new!=holds.get(identity):holds[identity]=new;state_save(ctx.work,ctx.state)
 if holds:ctx.fatal=holds
 return holds.get(identity)

def prepare(a):
 U.need(sys.version_info>=(3,11) and os.name=='posix' and not sys.flags.optimize,'Python 3.11+ POSIX with assertions enabled required')
 work,data=U.plain(a.work_root),U.plain(a.data_root)
 U.need(not work.exists() and not work.is_relative_to(data) and not work.is_relative_to(U.HERE),'Fresh work root outside data/code required')
 U.need(math.isfinite(a.total_seconds) and a.total_seconds>=120,'Explicit finite local child allocation required')
 U.need(1<=a.metric_chunk<=3937 and 1<=a.count_chunk<=10348 and 0<=a.max_fm_pairs<=10**12 and 0<=a.max_search_nodes<=10**12,'Invalid finite replay limits')
 I=U.Inputs(data,a.input_manifest,a.input_manifest_sha256)
 missing=[]
 for r in I.requirements.values():
  name=r['target'][5:];wanted={'bytes':r['bytes'],'sha256':r['sha256']}
  if I.files.get(name)!=wanted:missing.append(r)
 U.need(not missing,'Missing or stale exact input roles: '+json.dumps(missing,sort_keys=True))
 # Only the small configuration roster is read; no mathematical routine runs.
 old=U.read(I.role('cone_roster'));cone=json.loads(json.dumps(old))
 for key,entry in cone['inputs'].items():
  r=I.requirements['cone_'+key];U.need((entry['bytes'],entry['sha256'])==(r['bytes'],r['sha256']),'Original cone input identity differs')
  entry['path']=str(data/r['target'][5:])
 compiler=U.pin(a.compiler);U.need(os.access(compiler['path'],os.X_OK),'Explicit compiler is not executable')
 work.mkdir(parents=True);(work/'metadata').mkdir();(work/'jobs').mkdir();(work/'requests').mkdir()
 source=Path(a.input_manifest).read_bytes();U.need(U.sha(source)==a.input_manifest_sha256,'Manifest changed during preparation')
 with (work/'metadata/input-manifest.json').open('xb') as f:f.write(source)
 U.save(work/'metadata/cone-roster.json',cone)
 recipe={'schema':U.SCHEMA,'data_root':str(data),'work_root':str(work),'manifest':U.pin(work/'metadata/input-manifest.json'),
         'cone_roster':U.pin(work/'metadata/cone-roster.json'),'original_cone_roster':U.pin(I.role('cone_roster')),
         'compiler':compiler,'code':U.code_pins(),'steps':P.graph(a.metric_chunk,a.count_chunk),
         'total_child_seconds':a.total_seconds,'child_deadline_seconds':120,
         'max_fm_pairs':a.max_fm_pairs,'max_search_nodes':a.max_search_nodes,'prior_external_premises':U.PREMISES,
         'scientific_execution_during_prepare':False}
 I.after();U.save(work/'RECIPE.json',recipe)
 state_save(work,{'schema':U.SCHEMA,'recipe':U.pin(work/'RECIPE.json'),'attempts':[]})
 return {'status':'PREPARED_METADATA_ONLY','recipe':U.pin(work/'RECIPE.json'),'planned_steps':len(recipe['steps']),'prior_external_premises':U.PREMISES}

def child(path,expected):
 U.need(not sys.flags.optimize and __debug__,'Mathematical assertions must be enabled')
 rp=U.pin(path);U.need(rp['sha256']==expected,'Changed child request');request=U.read(path);U.check(request['recipe'])
 recipe=U.read(request['recipe']['path']);folder=U.plain(request['output_root'])
 U.need(folder==Path(recipe['work_root'])/'jobs'/request['id'] and not (folder/'result.json').exists(),'Wrong/nonfresh child output root')
 U.need(U.code_pins()==recipe['code'],'Child copied/adapted mathematical source changed')
 for p in [recipe['manifest'],recipe['cone_roster'],recipe['compiler'],*request['inputs']]:U.check(p)
 U.save(folder/'CHILD.json',{'schema':U.SCHEMA,'request':rp,'pid':os.getpid(),'assertions_enabled':True,
                            'code':recipe['code'],'data_root':recipe['data_root'],'before_mathematical_calls':True})
 accessed=[];error=None
 try:
  accessed=P.run_step(recipe,request['step'],folder,request['dependencies'])
  result=U.read(folder/'result.json');P.validate(request['step'],result,request['dependencies'],recipe)
 except BaseException as exc:
  error=f'{type(exc).__name__}: {exc}'
 finally:
  stable=True;failures=[]
  for p in [rp,request['recipe'],*recipe['code'],recipe['manifest'],recipe['cone_roster'],recipe['compiler'],*request['inputs'],*accessed]:
   try:U.check(p)
   except (OSError,ValueError) as exc:stable=False;failures.append(str(exc))
  U.save(folder/'CHILD-RESULT.json',{'schema':U.SCHEMA,'status':'complete' if error is None and stable else 'refused',
          'error':error,'source_bytes_unchanged':stable,'source_errors':failures,'accessed_inputs':accessed,
          'execution_class':P.execution_class(request['step']),'prior_external_premises':U.PREMISES})
 return 0 if error is None and stable else 2

class Context:
 def __init__(self,work):
  self.work=U.plain(work);self.state=U.read(self.work/'STATE.json');U.check(self.state['recipe']);self.recipe=U.read(self.state['recipe']['path'])
  U.need(self.recipe['schema']==self.state['schema']==U.SCHEMA and self.recipe['work_root']==str(self.work),'Wrong replay epoch')
  self.done={};self.failed={};self.elapsed=0.;self.executions=[];self.fatal=self.state.get('mandatory_holds') or None
  ids=[r['id'] for r in self.state['attempts']]
  U.need(ids==[f'f025-{i+1:06d}' for i in range(len(ids))],'Duplicate/missing/noncanonical execution identity')
  for item in self.state['attempts']:capture_adverse(self,item)
  self.stable()
 def stable(self):
  U.check(self.state['recipe']);U.need(U.code_pins()==self.recipe['code'],'Source/checker version changed')
  for name in ('manifest','cone_roster','compiler'):U.check(self.recipe[name])
 def dependencies(self,step):return {key:self.done[key] for key in step['needs']}
 def inputs(self,step,deps):
  I=U.Inputs(self.recipe['data_root'],self.recipe['manifest']['path'],self.recipe['manifest']['sha256'])
  for role in P.role_names(step):I.role(role)
  if step['kind']=='residual-join':
   manifest=U.read(I.path(U.BASE+'/export-residual/manifest.json'))
   for shard in manifest['shards']:I.path(U.BASE+'/export-residual/'+U.relative(shard['name']))
  values=list(I.used.values())
  for value in deps.values():
   values += [value['execution'],value['result'],*value['outputs']]
  return sorted({p['path']:p for p in values}.values(),key=lambda p:p['path'])
 def pending(self,lane):return [s for s in P.selected(self.recipe['steps'],lane) if s['id'] not in self.done]

def authenticate(ctx,item):
 capture_adverse(ctx,item)
 U.check(item['request']);q=U.read(item['request']['path']);U.need(q['id']==item['id'] and q['recipe']==ctx.state['recipe'],'Request belongs to another epoch')
 expected={s['id']:s for s in ctx.recipe['steps']};step=q['step'];U.need(expected.get(step['id'])==step and step['id'] not in ctx.done,'Unknown/stale/repeated successful step')
 U.need(all(n in ctx.done for n in step['needs']) and q['dependencies']==ctx.dependencies(step),'Missing or changed prerequisite execution')
 inputs=ctx.inputs(step,q['dependencies']);U.need(q['inputs']==inputs,'Changed/missing exact request inputs')
 for p in inputs:U.check(p)
 folder=ctx.work/'jobs'/item['id'];ep=U.pin(folder/'EXECUTION.json');e=U.read(ep['path'])
 U.need(e['schema']==U.SCHEMA and e['request']==item['request'] and e['cleanup_verified'] is True
        and e['sources_unchanged'] is True,'Unresolved, unclean or stale execution')
 command=[str(Path(sys.executable).resolve()),'-I','-S','-B',str(U.HERE/'upstream.py'),'_child','--request',item['request']['path'],
          '--request-sha256',item['request']['sha256']]
 U.need(e['command']==command and math.isfinite(e['elapsed_seconds']) and e['elapsed_seconds']>=0,'Wrong child command or timing')
 outputs={}
 for p in e['outputs']:
  path=U.plain(p['path']);U.need(path.is_relative_to(folder) and path.name!='EXECUTION.json' and p['path'] not in outputs,'Escaped/duplicate output member')
  U.check(p);outputs[p['path']]=p
 actual={str(p) for p in folder.rglob('*') if p.is_file() and p.name!='EXECUTION.json'}
 U.need(set(outputs)==actual and all(not p.is_symlink() for p in folder.rglob('*')),'Missing/extra/symlink output membership')
 ctx.elapsed+=e['elapsed_seconds'];ctx.executions.append(ep)
 complete=False
 if ctx.fatal is not None:return False
 if e['disposition']=='exited' and e['child_returncode']==0:
  launch=U.read(folder/'LAUNCH.json');applied=U.read(folder/'CHILD.json');finish=U.read(folder/'CHILD-RESULT.json')
  U.need(launch['command']==command and launch['pid']==launch['pgid']==applied['pid']==e['pid']==e['pgid']
         and applied['request']==item['request'] and applied['code']==ctx.recipe['code']
         and applied['assertions_enabled'] is True and applied['before_mathematical_calls'] is True,'Missing real mathematical child/configuration binding')
  U.need(finish['status']=='complete' and finish['source_bytes_unchanged'] is True and not finish['source_errors'],'Incomplete source finalization')
  result=U.read(folder/'result.json');P.validate(step,result,q['dependencies'],ctx.recipe)
  if step['kind'] in ('build','census','maps','count'):
   program=U.read(folder/'PROGRAM-EXIT.json');U.need(program['returncode']==0 and type(program['pid']) is int,'Missing actual compiler/census/map/counter exit')
  ctx.done[step['id']]={'execution':ep,'request':item['request'],'result':outputs[str(folder/'result.json')],
                       'outputs':list(outputs.values()),'execution_class':P.execution_class(step)}
  complete=True
 else:
  ctx.failed[step['id']]=ctx.failed.get(step['id'],0)+1
 return complete

def audit(ctx):
 for item in ctx.state['attempts']:capture_adverse(ctx,item)
 for item in ctx.state['attempts']:authenticate(ctx,item)
 return ctx

def execute(ctx,step):
 U.need(ctx.fatal is None,'A preserved negative observation requires owner disposition before further replay')
 ctx.stable();U.need(ctx.elapsed+120<=ctx.recipe['total_child_seconds'],'Cannot reserve a full 120-second child in the remaining local allocation')
 U.need(ctx.failed.get(step['id'],0)<3,'Three unsuccessful attempts exhausted; exact step remains pending')
 deps=ctx.dependencies(step);inputs=ctx.inputs(step,deps)
 identity=f'f025-{len(ctx.state["attempts"])+1:06d}';folder=ctx.work/'jobs'/identity
 U.need(not folder.exists(),'Output identity is not fresh')
 q={'schema':U.SCHEMA,'id':identity,'recipe':ctx.state['recipe'],'step':step,'dependencies':deps,'inputs':inputs,
    'output_root':str(folder),'reserved_seconds':120,'elapsed_before':ctx.elapsed}
 qp=ctx.work/'requests'/(identity+'.json');U.save(qp,q);item={'id':identity,'request':U.pin(qp)}
 ctx.state['attempts'].append(item);state_save(ctx.work,ctx.state);folder.mkdir()
 command=[str(Path(sys.executable).resolve()),'-I','-S','-B',str(U.HERE/'upstream.py'),'_child','--request',str(qp),'--request-sha256',item['request']['sha256']]
 outcome=U.supervisor().supervise(command,folder,folder/'stdout.txt',folder/'stderr.txt',120,folder/'LAUNCH.json')
 capture_adverse(ctx,item,step)
 stable=True;errors=[]
 for p in [item['request'],ctx.state['recipe'],*ctx.recipe['code'],ctx.recipe['manifest'],ctx.recipe['cone_roster'],ctx.recipe['compiler'],*inputs]:
  try:U.check(p)
  except (OSError,ValueError) as error:stable=False;errors.append(str(error))
 outputs=[U.pin(p) for p in sorted(folder.rglob('*')) if p.is_file()]
 U.save(folder/'EXECUTION.json',{'schema':U.SCHEMA,'request':item['request'],'command':command,**outcome,
       'sources_unchanged':stable,'source_errors':errors,'outputs':outputs,'execution_class':P.execution_class(step),
       'whole_box_theorem_accepted':False})
 return authenticate(ctx,item)

def run(ctx,lane,max_jobs):
 count=0
 for step in ctx.pending(lane):
  if max_jobs is not None and count>=max_jobs:break
  okay=execute(ctx,step);count+=1
  print(json.dumps({'step':step['id'],'completed':okay,'elapsed_child_seconds':round(ctx.elapsed,3)}),flush=True)
  if not okay:break
 pending=ctx.pending(lane)
 body={'schema':U.SCHEMA,'lane':lane,'status':'HELD_ADVERSE_OBSERVATION' if ctx.fatal else 'COMPLETE_STEPS_PENDING_AGGREGATE' if not pending else 'PENDING',
       'recipe':ctx.state['recipe'],'pending_exact_steps':pending,'failed_attempts':ctx.failed,
       'candidate_hold':ctx.fatal,
       'elapsed_child_seconds':ctx.elapsed,'prior_external_premises':U.PREMISES}
 return {'status':body['status'],'report':report(ctx.work,'progress',body),'pending_steps':len(pending)}

def aggregate(ctx,lane):
 U.need(ctx.fatal is None and not ctx.pending(lane),'Required exact replay steps or candidate disposition remain pending')
 chosen=P.selected(ctx.recipe['steps'],lane)
 mathematical=[s for s in chosen if s['kind']!='build']
 result={'schema':U.SCHEMA,'status':'F025_PREDECESSOR_REPLAY_COMPLETE_CONDITIONAL_ON_NAMED_EXTERNAL_THEOREMS' if lane in ('all','cover') else 'REQUESTED_F025_LANE_REPLAY_COMPLETE',
         'lane':lane,'recipe':ctx.state['recipe'],'exact_steps':[s['id'] for s in chosen],
         'evidence':{s['id']:ctx.done[s['id']] for s in chosen},
         'fresh_census_ranks':[s['rank'] for s in chosen if s['kind']=='census'],
         'fresh_whole_chart_scalar_sites':sum((s['stop']-s['start'])*len(s['nodes']) for s in chosen if s['kind']=='count'),
         'certificate_replay_steps':[s['id'] for s in mathematical if P.execution_class(s)=='finite_certificate_or_exact_identity_replay'],
         'elapsed_child_seconds':ctx.elapsed,'prior_external_premises':U.PREMISES,'whole_box_theorem_accepted':False}
 ctx.stable()
 return {'status':result['status'],'aggregate':report(ctx.work,'aggregate',result),'fresh_whole_chart_scalar_sites':result['fresh_whole_chart_scalar_sites']}

@contextmanager
def lock(work):
 with U.plain(U.plain(work)/'LOCK').open('a') as f:
  try:fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise U.Invalid('Another controller owns the replay journal') from None
  yield

def main():
 parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='mode',required=True)
 p=commands.add_parser('prepare');p.add_argument('--data-root',type=Path,required=True);p.add_argument('--work-root',type=Path,required=True)
 p.add_argument('--input-manifest',type=Path,required=True);p.add_argument('--input-manifest-sha256',required=True)
 p.add_argument('--compiler',type=Path,required=True);p.add_argument('--total-seconds',type=float,required=True)
 p.add_argument('--metric-chunk',type=int,default=250);p.add_argument('--count-chunk',type=int,default=512)
 p.add_argument('--max-fm-pairs',type=int,default=2000000);p.add_argument('--max-search-nodes',type=int,default=100000000)
 for name in ('run','status','aggregate'):
  p=commands.add_parser(name);p.add_argument('--work-root',type=Path,required=True);p.add_argument('--lane',choices=P.LANES,required=True)
  if name=='run':p.add_argument('--max-jobs',type=int)
 p=commands.add_parser('_child',help=argparse.SUPPRESS);p.add_argument('--request',type=Path,required=True);p.add_argument('--request-sha256',required=True)
 a=parser.parse_args();ctx=None
 try:
  if a.mode=='_child':return child(a.request,a.request_sha256)
  if a.mode=='prepare':result=prepare(a)
  else:
   with lock(a.work_root):
    ctx=Context(a.work_root);audit(ctx)
    if a.mode=='run':
     U.need(a.max_jobs is None or a.max_jobs>0,'max-jobs must be positive');result=run(ctx,a.lane,a.max_jobs)
    elif a.mode=='aggregate':result=aggregate(ctx,a.lane)
    else:
     pending=ctx.pending(a.lane);result={'status':'HELD_ADVERSE_OBSERVATION' if ctx.fatal else 'PENDING' if pending else 'COMPLETE_STEPS',
       'report':report(ctx.work,'status',{'recipe':ctx.state['recipe'],'lane':a.lane,'pending_exact_steps':pending,
                                       'failed_attempts':ctx.failed,'elapsed_child_seconds':ctx.elapsed,'mandatory_holds':ctx.state.get('mandatory_holds',{})})}
  print(json.dumps(result,sort_keys=True),flush=True);return 0
 except Exception as error:
  failure={'schema':U.SCHEMA,'status':'REFUSED','error':f'{type(error).__name__}: {error}','prior_external_premises':U.PREMISES}
  if ctx is not None:
   failure.update(recipe=ctx.state['recipe'],journal_snapshot=ctx.state,pending_exact_steps=ctx.pending(a.lane),
                  mandatory_holds=ctx.state.get('mandatory_holds',{}),candidate_hold=ctx.fatal)
   if ctx.fatal:failure['status']='HELD_ADVERSE_OBSERVATION'
   failure['report']=report(ctx.work,'refusal',failure)
  print(json.dumps(failure,sort_keys=True),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
