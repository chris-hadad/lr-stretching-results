#!/usr/bin/env python3
"""Fresh portable numerical evidence. No old receipts and no theorem promotion.

prepare freezes metadata and finite settings only. run launches serial bounded
roster/index/build/count/aggregate children; status and aggregate authenticate
their exact outputs. Use separate fresh work roots for representative and full
epochs. A refused node is pending, never zero. Mathematical acceptance joins
listed in every result remain separate from numerical evidence completion.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from fractions import Fraction
import fcntl
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import time
from types import SimpleNamespace

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as U

METADATA = ('source_manifest','chosen_terminals','geometry_jobs','legacy_vectors','copy_plan')


def replace_state(work,state):
    p=work/f'STATE.{os.getpid()}.tmp'; U.save(p,state); os.replace(p,work/'STATE.json')


def fresh_report(work,kind,result):
    i=1
    while (work/f'{kind}-{i:06d}.json').exists(): i+=1
    p=work/f'{kind}-{i:06d}.json'; U.save(p,result); return U.pin(p)


def adverse_records(value,location='$',vectors=False):
    """Retain an observation without treating an incomplete receipt as proof."""
    if isinstance(value,dict):
        reason=None;scope='source/count agreement only; no whole negative coefficient inferred'
        if value.get('status') in ('FAIL','MISMATCH','COUNT_MISMATCH','HOLD_CANDIDATE','HOLD_ORDINARY_NEGATIVE','candidate_interrupt'):
            reason='persisted_adverse_status'
        if any(value.get(k) for k in ('candidates','ordinary_negative_observations','negative_indices','ordinary_negative_indices','mismatches')):
            reason='persisted_negative_or_mismatch_observation'
            scope=value.get('scope','source-declared observation; mathematical scope still requires validation')
        c=value.get('counter');stored=value.get('stored')
        if isinstance(c,dict) and c.get('status')=='complete' and isinstance(stored,dict):
            try:
                def scalar(v):
                    U.need(type(v) in (int,str) and re.fullmatch(r'0|[1-9][0-9]*',str(v)), 'Invalid complete scalar')
                    return int(v)
                if any(scalar(c.get('count'))!=scalar(v) for v in stored.values()):reason='persisted_complete_count_mismatch'
            except (ValueError,TypeError):reason='unreadable_complete_scalar_observation'
        if vectors or value.get('kind')=='FULL_VECTOR':
            for name in ('coefficients','coefficients_low_to_high'):
                values=value.get(name)
                if isinstance(values,list):
                    try:
                        if any(type(v) in (int,str) and Fraction(v)<0 for v in values):
                            reason='persisted_negative_vector';scope=value.get('scope','ordinary source/reconstructed vector observation; not an accepted counterexample')
                    except (ValueError,ZeroDivisionError):reason='unreadable_vector_observation'
        if reason:
            yield {'location':location,'reason':reason,'scope':scope,'record':value};return
        for key,child in value.items():
            if isinstance(child,(dict,list)):yield from adverse_records(child,location+'/'+key,vectors)
    elif isinstance(value,list):
        for i,child in enumerate(value):yield from adverse_records(child,location+'/'+str(i),vectors)


def capture_adverse(ctx,identity):
    U.need(re.fullmatch(r'numerics-[0-9]{6}',identity),'Unsafe observation attempt identity')
    folder=ctx.work/'jobs'/identity;observations=[]
    if folder.is_dir() and not folder.is_symlink():
        for path in sorted(folder.iterdir()):
            named='candidate' in path.name or 'source-negative' in path.name
            vectors='raw-vector' in path.name or 'negative' in path.name
            if not (named or path.name in ('result.json','result.counts.jsonl','result.early-bindings.jsonl','result.raw-vectors.jsonl')):continue
            source=None
            try:
                source=U.pin(path)
                if path.suffix=='.jsonl':
                    with path.open('rb') as stream:
                        for line,raw in enumerate(stream,1):
                            try:
                                U.need(raw.endswith(b'\n'),'Incomplete durable observation line')
                                found=list(adverse_records(U.decode(raw),f'line:{line}',vectors))
                            except (ValueError,UnicodeError):
                                found=[{'location':f'line:{line}','reason':'unreadable_durable_observation','record_sha256':U.sha(raw),
                                        'scope':'unresolved persisted bytes; no negative coefficient inferred'}]
                            observations += [{'artifact':source,**r} for r in found]
                else:
                    value=U.read(path);found=list(adverse_records(value,vectors=vectors))
                    if named and not found:found=[{'location':'$','reason':'persisted_candidate_artifact','record':value,
                        'scope':'candidate-labelled observation; mathematical scope still requires validation'}]
                    observations += [{'artifact':source,**r} for r in found]
            except (OSError,ValueError,UnicodeError) as error:
                observations.append({'path':str(path),'artifact':source,'reason':'unreadable_adverse_or_result_artifact','error':str(error),
                                     'scope':'unresolved persisted bytes; no mathematical claim accepted'})
    holds=ctx.state.setdefault('mandatory_holds',{})
    if observations:
        old=holds.get(identity,{'attempt_id':identity,'requires_owner_disposition':True,'authenticated_scientific_result':False,'observations':[]})
        unique={U.sha(U.encoded(r)):r for r in old['observations']}
        for row in observations:unique[U.sha(U.encoded(row))]=row
        new={**old,'observations':list(unique.values())}
        if new!=holds.get(identity):holds[identity]=new;replace_state(ctx.work,ctx.state)
    if holds:ctx.fatal=holds
    return holds.get(identity)


def prepare(args):
    U.need(sys.version_info>=(3,10) and os.name=='posix','Python 3.10+ on POSIX required')
    work,data=U.plain(args.work_root),U.plain(args.data_root)
    U.need(not work.exists() and not work.is_relative_to(data) and not work.is_relative_to(U.HERE),'Fresh work root outside data/code required')
    U.need(math.isfinite(args.total_seconds) and args.total_seconds>=120,'Explicit finite local child budget of at least 120 seconds required')
    settings={k:getattr(args,k) for k in ('production_index_chunk','production_count_chunk','early_chunk','legacy_chunk','u11_chunk')}
    U.need(all(type(v) is int and v>0 for v in settings.values()),'Positive explicit chunk sizes required')
    raw_meta={}
    for name in METADATA:
        path=getattr(args,name); p=U.pin(path); expected=getattr(args,name+'_sha256')
        U.need(p['sha256']==expected,'Metadata hash differs: '+name)
        raw=Path(path).read_bytes(); U.need(U.sha(raw)==expected,'Metadata changed during read'); raw_meta[name]=(raw,p)
    C=U.original('portable-box-components')
    streams=C.geometry_recipe(U.decode(raw_meta['geometry_jobs'][0]))
    plan=U.decode(raw_meta['copy_plan'][0])
    U.need(all(m['action']=='copy_bytes' and not m.get('projection') for m in plan['members']),
           'This route requires the whole-file copy plan; historical projections are unsupported')
    chosen=U.decode(raw_meta['chosen_terminals'][0]); legacy=U.decode(raw_meta['legacy_vectors'][0])
    P=U.original('accept_legacy_prefix')
    P.metadata_roster(legacy,chosen,prefix_ids=tuple(range(297)))
    for unit in ('U02','U03'):
        ids=chosen[C.EARLY_KEYS[unit]]
        U.need(len(ids)==U.TOTALS[unit] and len(set(ids))==len(ids) and all(type(i) is int for i in ids),'Missing/duplicate selected early IDs')
    compiler=U.pin(args.compiler)
    U.need(os.access(compiler['path'],os.X_OK),'Explicit compiler is not executable')
    work.mkdir(parents=True); (work/'metadata').mkdir(); (work/'requests').mkdir(); (work/'jobs').mkdir()
    metadata={}
    for name,(raw,p) in raw_meta.items():
        target=work/'metadata'/(name+'.json')
        with target.open('xb') as f: f.write(raw)
        U.check(p); metadata[name]=U.pin(target)
    recipe={'schema':U.SCHEMA,'data_root':str(data),'work_root':str(work),'mode':args.mode,'holdouts':args.holdouts,
            'code':U.code_pins(),'metadata':metadata,'compiler':compiler,'geometry_streams':streams,
            'settings':{**settings,'internal_seconds':100,'parent_seconds':120,'total_child_seconds':args.total_seconds,
                        'retry_schedule':[list(s) for s in U.SCHEDULE],'max_zero_progress_index_attempts':3},
            'scope':U.SCOPE,'prepared_without_scientific_execution':True}
    I=U.Inputs(recipe)  # Schema/alias metadata only; no data file is opened.
    refs=[]
    for record in legacy['records']:
        refs += [record[k] for k in ('vector_reference','triple_reference','adopted_disposition_reference') if k in record]
        refs += [r for r in record.get('additional_vector_sources',[]) if not r.get('same_source_file')]
    for ref in refs:
        U.need((ref['bytes'],ref['sha256']) in I.aliases,'Required original legacy file has no whole-file portable target: '+ref['sha256'])
    U.save(work/'RECIPE.json',recipe)
    replace_state(work,{'schema':U.SCHEMA,'recipe':U.pin(work/'RECIPE.json'),'attempts':[]})
    return {'status':'PREPARED_METADATA_ONLY','recipe':U.pin(work/'RECIPE.json'),'mode':args.mode,'scope':U.SCOPE}


def child(request_path,expected_sha):
    rp=U.pin(request_path); U.need(rp['sha256']==expected_sha,'Child request changed')
    request=U.read(request_path); U.check(request['recipe']); recipe=U.read(request['recipe']['path'])
    output=U.plain(request['output']); work=U.plain(recipe['work_root'])
    U.need(output.parent==work/'jobs'/request['id'] and not output.exists(),'Child output is not fresh inside its exact reserved directory')
    for p in [*recipe['code'],*recipe['metadata'].values(),recipe['compiler'],*request['inputs']]: U.check(p)
    U.need(U.code_pins()==recipe['code'],'Child code copies/adapters changed')
    R=U.original('recount_records'); import numerical_indices as N
    G,GE=N.configure_geometry(recipe)
    U.save(output.with_name('CHILD.json'),{'schema':U.SCHEMA,'request':rp,'pid':os.getpid(),
           'configured_geometry_roots':{'box_geometry':str(G.CANONICAL),'box_geometry_early':str(GE.CANONICAL)},
           'code':recipe['code'],'before_mathematical_calls':True})
    op=request['operation']; result={'schema':R.SCHEMA,'kind':op['kind'],'status':'PARTIAL',
          'wrapper_sha256':U.pin(R.__file__)['sha256'],'portable_request':rp,'scope':U.SCOPE}
    def expired(*_): raise R.DeadlineReached('Portable child internal deadline reached')
    signal.signal(signal.SIGALRM,expired); signal.setitimer(signal.ITIMER_REAL,recipe['settings']['internal_seconds'])
    deadline=R.Deadline(recipe['settings']['internal_seconds'])
    try:
        if op['kind']=='build':
            result.update(R.compile_counter(U.HERE/'originals/v2_independent_hive_recount.cpp',output.with_name('recount'),
                                            recipe['compiler']['path'],deadline))
        elif op['kind']=='roster':
            result.update(N.metadata_roster({**recipe,'_current_output':str(output)},op['cohort'],deadline,op.get('unit_filter')))
        elif op['kind']=='index':
            N.index(recipe,op,output,deadline,result)
        elif op['kind']=='count':
            args=SimpleNamespace(manifest=op['manifest']['path'],build=op['build']['path'],output=str(output),
                  start=op['slice'][0],limit=op['slice'][1]-op['slice'][0],site=None,
                  node_ms=op['node_ms'],max_states=op['max_states'],resume_from=[p['path'] for p in op['resume']])
            result['kind']='run'; R.run_jobs(args,deadline,result)
        else:
            U.need(op['kind']=='aggregate','Unallowlisted child operation')
            args=SimpleNamespace(manifest=op['manifest']['path'],reports=[p['path'] for p in op['reports']],output=str(output))
            R.aggregate(args,deadline,result)
    except R.DeadlineReached as error:
        result.update(status='PARTIAL',interruption=str(error))
    except Exception as error:
        status='HOLD_CANDIDATE' if type(error).__name__ in ('CandidateObservation','SourceNegative') else 'FAIL'
        result.update(status=status,error=f'{type(error).__name__}: {error}')
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        try:
            for p in [rp,request['recipe'],*recipe['code'],*recipe['metadata'].values(),*request['inputs'],*result.get('inputs',[])]: U.check(p)
            result['source_bytes_verified_before_after']=True
        except Exception as error:
            result.update(status='FAIL',source_bytes_verified_before_after=False,source_error=str(error))
        U.save(output,result)
    if result['status'] in ('BUILT_OWN_COUNTER','FROZEN_LITERAL_ROSTER','FROZEN_RECOUNT_JOBS','SLICE_RECOUNTS_MATCH','COMPLETE_FROZEN_RECOUNTS_MATCH'): return 0
    return 2 if result['status']=='PARTIAL' else 1


class Context:
    def __init__(self,work):
        self.work=U.plain(work); self.state=U.read(self.work/'STATE.json'); U.check(self.state['recipe'])
        self.recipe=U.read(self.state['recipe']['path'])
        U.need(self.recipe['schema']==self.state['schema']==U.SCHEMA and self.recipe['work_root']==str(self.work),'Wrong local replay epoch')
        self.build=None; self.rosters={}; self.groups={}; self.elapsed=0.0; self.fatal=self.state.get('mandatory_holds') or None
        self.zero_attempts=CounterLike(); self.job_cache={}; self.receipts=[]
        U.need([a['id'] for a in self.state['attempts']]==[f'numerics-{i+1:06d}' for i in range(len(self.state['attempts']))],
               'Duplicate/missing journal execution identity')
        for item in self.state['attempts']:capture_adverse(self,item['id'])
        self.stable()
    def stable(self):
        U.check(self.state['recipe'])
        U.need(U.code_pins()==self.recipe['code'],'Changed source copies/adapters')
        for p in [*self.recipe['metadata'].values(),self.recipe['compiler']]: U.check(p)
    def roster_keys(self,cohort):
        requested=U.COHORTS if cohort=='all' else (cohort,)
        keys=[]
        for c in requested:
            keys += [(f'production/U{i:02d}',c,f'U{i:02d}') for i in range(4,12)] if c=='production' else [(c,c,None)]
        return keys
    def count_chunk(self,unit):
        s=self.recipe['settings']
        return s['u11_chunk'] if unit=='U11' else s['legacy_chunk'] if unit=='LEGACY' else s['early_chunk'] if unit in ('U02','U03') else s['production_count_chunk']
    def next(self,cohort):
        U.need(self.fatal is None,'A persisted mismatch/candidate/failure requires owner disposition: '+str(self.fatal))
        if self.build is None: return {'kind':'build'}
        for key,c,unit in self.roster_keys(cohort):
            if key not in self.rosters: return {'kind':'roster','key':key,'cohort':c,'unit_filter':unit}
            roster=self.rosters[key]
            for group in roster['result']['selected_groups']:
                g=self.groups[(key,group['key'])]
                if g['cursor']==len(group['records']): continue
                a=g['active']
                if a is None:
                    s=self.recipe['settings']; n=s['production_index_chunk'] if c=='production' else self.count_chunk(group['unit'])
                    if group['unit']=='U11': n=s['u11_chunk']
                    start=g['cursor']; stop=min(start+n,len(group['records']))
                    return {'kind':'index','key':key,'cohort':c,'stream':group['key'],'unit':group['unit'],'shard':group['shard'],
                            'roster':roster['result_pin'],'slice':[start,stop],'records':group['records'][start:stop]}
                entries=a['manifest']['records']; size=self.count_chunk(group['unit'])
                for start in range(0,len(entries),size):
                    stop=min(start+size,len(entries)); ids={n for e in entries[start:stop] for n in e['node_ids']}
                    if ids<=set(a['matched']): continue
                    previous=[r for r in a['runs'] if r['operation']['slice']==[start,stop]]
                    U.need(len(previous)<len(U.SCHEDULE),'Finite node retry schedule exhausted; pending nodes: '+str(sorted(ids-set(a['matched']))))
                    ms,states=U.SCHEDULE[len(previous)]
                    return {'kind':'count','key':key,'cohort':c,'stream':group['key'],'manifest':a['index']['result_pin'],
                            'build':self.build['result_pin'],'slice':[start,stop],'node_ms':ms,'max_states':states,
                            'resume':[r['result_pin'] for r in previous if r.get('usable_count_report')]}
                return {'kind':'aggregate','key':key,'cohort':c,'stream':group['key'],'manifest':a['index']['result_pin'],
                        'reports':[r['result_pin'] for r in a['runs'] if r.get('usable_count_report')]}
        return None
    def jobs(self,manifest):
        p=manifest['jobs']; U.check(p)
        if p['sha256'] not in self.job_cache:
            R=U.original('recount_records'); jobs=[]
            with Path(p['path']).open('rb') as f:
                for expected in manifest['records']: jobs.append(R.read_job(f,expected))
            self.job_cache[p['sha256']]=jobs
        return self.job_cache[p['sha256']]


class CounterLike(dict):
    def increment(self,key): self[key]=self.get(key,0)+1; return self[key]


def expected_inputs(ctx,op):
    pins={}
    for name in ('roster','manifest','build'):
        if name in op: pins[op[name]['path']]=op[name]
    for name in ('resume','reports'):
        for p in op.get(name,[]): pins[p['path']]=p
    if 'manifest' in op:
        manifest=U.read(op['manifest']['path'])
        for p in [manifest['jobs'],*manifest['inputs']]: pins[p['path']]=p
    if 'build' in op:
        build=U.read(op['build']['path'])
        for p in (build['source'],build['binary']): pins[p['path']]=p
    return [pins[k] for k in sorted(pins)]


def execute(ctx,request,request_pin):
    U.need(ctx.fatal is None,'A persisted adverse observation requires owner disposition before any numerical execution')
    directory=ctx.work/'jobs'/request['id']; U.need(not directory.exists(),'Execution output already exists'); directory.mkdir()
    P=U.original('portable_run')
    command=[str(Path(sys.executable).resolve()),'-I','-S','-B',str(U.HERE/'numerics.py'),'_child',
             '--request',request_pin['path'],'--request-sha256',request_pin['sha256']]
    outcome=P.supervise(command,directory,directory/'stdout.txt',directory/'stderr.txt',120,directory/'LAUNCH.json')
    capture_adverse(ctx,request['id'])
    stable=True; errors=[]
    for p in [request_pin,request['recipe'],*ctx.recipe['code'],*ctx.recipe['metadata'].values(),ctx.recipe['compiler'],*request['inputs']]:
        try: U.check(p)
        except (OSError,ValueError) as error: stable=False; errors.append(str(error))
    outputs=[U.pin(p) for p in sorted(directory.iterdir()) if p.is_file()]
    try:result=U.read(directory/'result.json') if (directory/'result.json').exists() else None
    except (OSError,ValueError,UnicodeError):result={'status':'UNREADABLE_PERSISTED_RESULT'}
    record={'schema':U.SCHEMA,'kind':'execution','request':request_pin,'command':command,**outcome,
            'sources_unchanged':stable,'source_errors':errors,'outputs':outputs,
            'result_status':None if result is None else result.get('status'),'whole_theorem_accepted':False}
    U.save(directory/'EXECUTION.json',record)


def authenticate(ctx,item):
    capture_adverse(ctx,item['id'])
    U.check(item['request']); request=U.read(item['request']['path'])
    U.need(request['id']==item['id'] and request['recipe']==ctx.state['recipe'],'Request belongs to another epoch')
    for p in request['inputs']: U.check(p)
    directory=ctx.work/'jobs'/item['id']; ep=U.pin(directory/'EXECUTION.json'); e=U.read(ep['path'])
    U.need(e['schema']==U.SCHEMA and e['request']==item['request'] and e['cleanup_verified'] is True
           and e['sources_unchanged'] is True and not e['source_errors'],'Unclean or changed execution')
    command=[str(Path(sys.executable).resolve()),'-I','-S','-B',str(U.HERE/'numerics.py'),'_child',
             '--request',item['request']['path'],'--request-sha256',item['request']['sha256']]
    U.need(e['command']==command,'Wrong actual child command')
    outputs={}
    for p in e['outputs']:
        path=U.plain(p['path']); U.need(path.parent==directory and path.name not in outputs,'Duplicate/escaped output member')
        U.check(p); outputs[path.name]=p
    U.need(all(p.is_file() and not p.is_symlink() for p in directory.iterdir()) and
           set(outputs)=={p.name for p in directory.iterdir() if p.name!='EXECUTION.json'},'Missing/extra execution member')
    U.need(math.isfinite(e['elapsed_seconds']) and e['elapsed_seconds']>=0,'Missing measured elapsed child time')
    ctx.elapsed+=e['elapsed_seconds']; ctx.receipts.append(ep)
    if e['disposition']!='exited': return request,None
    U.need(type(e['child_returncode']) is int and e['pid']==e['pgid'],'No real child exit identity')
    launch=U.read(directory/'LAUNCH.json'); applied=U.read(directory/'CHILD.json')
    U.need(launch['command']==command and launch['pid']==launch['pgid']==applied['pid']==e['pid']
           and applied['request']==item['request'] and applied['code']==ctx.recipe['code']
           and applied['before_mathematical_calls'] is True,'Missing actual child/configuration binding')
    base=str(Path(ctx.recipe['data_root'])/'namespaces/base')
    U.need(applied['configured_geometry_roots']=={'box_geometry':base,'box_geometry_early':base},'Wrong original-mask data root')
    if 'result.json' not in outputs: return request,None
    z=U.read(directory/'result.json')
    U.need(z.get('source_bytes_verified_before_after') is True and e['result_status']==z.get('status'),'Source finalization failed')
    wanted=0 if z['status'] in ('BUILT_OWN_COUNTER','FROZEN_LITERAL_ROSTER','FROZEN_RECOUNT_JOBS','SLICE_RECOUNTS_MATCH','COMPLETE_FROZEN_RECOUNTS_MATCH') else 2 if z['status']=='PARTIAL' else 1
    U.need(e['child_returncode']==wanted,'Typed result contradicts actual child exit')
    return request,{'result':z,'result_pin':outputs['result.json'],'execution_pin':ep,'outputs':outputs,'operation':request['operation']}


def validate_manifest(ctx,op,record):
    z=record['result']; R=U.original('recount_records')
    U.need(z['schema']==R.SCHEMA and z['kind']=='manifest' and z['selection_complete'] is True
           and z['wrapper_sha256']==U.pin(R.__file__)['sha256'],'Invalid/changed recount manifest')
    ids=[r['id'] for r in op['records']]; entries=z['records']
    U.need(z['expected_record_ids']==sorted(ids) and [r['id'] for r in entries]==ids[:len(entries)]
           and z['pending_index_ids']==sorted(set(ids)-{r['id'] for r in entries})
           and z['source_roster']==op['roster'] and z['source_slice']==op['slice']
           and z['explicit_source_records']==op['records'],'Index omitted/reordered/staled its literal source selection')
    U.need(z['jobs']==record['outputs'].get('result.jobs.jsonl'),'Unbound index jobs file')
    # The preserved consumer also checks contiguous ordinals, offsets, sizes,
    # exact node identities and source hashes; only actual emitted jobs count.
    R.load_manifest(record['result_pin']['path'],R.Deadline(100))
    jobs=ctx.jobs(z)
    for expected,job in zip(op['records'],jobs):
        U.need(job['id']==expected['id'] and job['unit']==op['unit']
               and (expected['bare_triple'] is None or job['bare_triple']==expected['bare_triple']),'Job/source whole identity differs')
        if op['cohort']=='production':
            ref=job['certificate_reference']; ref=ref['compact'] if 'compact' in ref else ref
            U.need(ref['sha256']==expected['compact_sha256'] and job['geometry_sha256']==expected['geometry_sha256'],
                   'Job detached from its exact final compact record')
        elif op['cohort'] in ('U02','U03'):
            U.need(job['certificate_reference']['record_sha256']==expected['compact_sha256'],'Early job source changed')
            if op['cohort']=='U02' and ctx.recipe['holdouts']=='first-unused':
                U.need(job['u02_holdout_policy']==expected['u02_holdout_policy'] and
                       job['nodes']==expected['u02_holdout_policy']['required_nodes'],
                       'Count job omitted or changed its frozen first-unused hold/determining roster')
        else: U.need(job['terminal_id']==expected['terminal_id'],'Legacy job changed literal terminal')
    for p in z['inputs']:
        path=U.plain(p['path']); U.need(path.is_relative_to(Path(ctx.recipe['data_root'])) or path.is_relative_to(ctx.work)
              or path.is_relative_to(U.HERE),'Manifest input escaped portable data/work/code roots'); U.check(p)


def validate_count(ctx,op,record,active):
    z=record['result']; manifest=active['manifest']; R=U.original('recount_records')
    if 'results' not in z: return False
    U.need(z['schema']==R.SCHEMA and z['kind']=='run' and z['manifest_sha256']==op['manifest']['sha256']
           and z['wrapper_sha256']==U.pin(R.__file__)['sha256'] and z['start']==op['slice'][0]
           and z['requested_stop']==op['slice'][1] and type(z['counter_exit_code']) is int,'Count report has wrong manifest/range/exit')
    build=ctx.build['result']
    U.need(z['build_reference']==ctx.build['result_pin'] and z['build']==build['binary'] and z['counter_source']==build['source'],
           'Count report mixed source/binary/build epochs')
    U.need(z['results']==record['outputs'].get('result.counts.jsonl'),'Unbound numerical count ledger')
    jobs=ctx.jobs(manifest); expected={}
    start,stop=op['slice']
    for ordinal in range(start,stop):
        job=jobs[ordinal]
        for node in job['nodes']: expected[f"{job['unit']}:{job['id']}:{node['kind']}"]=(ordinal,job,node)
    seen=set(); matched=[]; refused=[]
    for _i,row,_raw in U.lines(z['results']['path']):
        nid=row['node_id']; U.need(nid in expected and nid not in seen,'Extra/duplicated count attempt within a slice'); seen.add(nid)
        ordinal,job,node=expected[nid]
        U.need(type(row['record_ordinal']) is int and type(row['id']) is int and type(row['grade']) is int and type(row['strict']) is bool
               and row['record_ordinal']==ordinal and row['id']==job['id'] and row['geometry_sha256']==job['geometry_sha256']
               and all(row[k]==node[k] for k in ('kind','grade','strict','stored')) and row['counter']['id']==nid,'Count belongs to another full source/node')
        c=row['counter']
        if c['status']=='complete':
            value=R.integer(c['count']); U.need(value>=0,'Negative lattice scalar')
            agrees=all(value==v for v in node['stored'].values())
            U.need(row['status']==('MATCH' if agrees else 'MISMATCH'),'False numerical agreement status')
            if not agrees:
                ctx.fatal=record['result_pin']['path']; U.need(z['status']=='COUNT_MISMATCH' and z['mismatch']==row,'Mismatch was not preserved immediately')
            else:
                U.need(nid not in active['matched'],'Duplicate successful recount, including agreeing retries')
                active['matched'][nid]={'row':row,'report':record['result_pin']}; matched.append(nid)
        else:
            U.need(row['status']=='REFUSED' and c['status'].startswith('REFUSED_') and c.get('count') is None,'Refusal supplied a partial scalar')
            refused.append(nid)
    U.need(z['matched_node_ids']==matched and z['refused_node_ids']==refused and z['attempted_nodes']==len(seen),
           'Count report omitted or added physical outcomes')
    record['usable_count_report']=True
    return True


def apply(ctx,op,record):
    if ctx.fatal is not None:return False
    token=U.sha(U.encoded(op))
    if record is None:
        ctx.zero_attempts.increment(token); return False
    z=record['result']; status=z['status']
    candidate=any('candidate' in name or 'source-negative' in name for name in record['outputs'])
    if status in ('FAIL','HOLD_CANDIDATE') or candidate:
        ctx.fatal=record['result_pin']['path']; return False
    if op['kind']=='build':
        if status!='BUILT_OWN_COUNTER': ctx.zero_attempts.increment(token); return False
        R=U.original('recount_records')
        U.need(z['source']==U.pin(U.HERE/'originals/v2_independent_hive_recount.cpp')
               and z['binary']==record['outputs'].get('recount') and z['wrapper_sha256']==U.pin(R.__file__)['sha256'], 'Stale build/source/binary')
        U.need(z['command']==[ctx.recipe['compiler']['path'],'-std=c++17','-O2','-Wall','-Wextra',z['source']['path'],'-o',z['binary']['path']], 'Wrong actual compiler command')
        ctx.build=record; return True
    if op['kind']=='roster':
        if status!='FROZEN_LITERAL_ROSTER': ctx.zero_attempts.increment(token); return False
        U.need(z['cohort']==op['cohort'] and z['unit_filter']==op['unit_filter'] and z['mode']==ctx.recipe['mode']
               and (op['cohort']!='U02' or z['u02_holdouts']==ctx.recipe['holdouts']), 'Wrong roster scope')
        C=U.original('portable-box-components')
        total=C.COUNTS[op['unit_filter']] if op['cohort']=='production' else U.TOTALS[op['cohort']]
        full=[r for g in z['full_source_groups'] for r in g['records']]
        U.need(len(full)==total==z['full_source_population'] and len({(r['unit'],r['id']) for r in full})==total,'Incomplete/duplicate full source roster')
        available={(g['key'],r['id']):r for g in z['full_source_groups'] for r in g['records']}
        chosen=[(g['key'],r) for g in z['selected_groups'] for r in g['records']]
        U.need(chosen and len(chosen)==z['selected_population'] and len({(k,r['id']) for k,r in chosen})==len(chosen)
               and all(available.get((k,r['id']))==r for k,r in chosen),'Selected representative/full roster is not literal')
        if ctx.recipe['mode']=='full': U.need(z['selected_groups']==z['full_source_groups'],'Full mode skipped source identities')
        for p in z['inputs']: U.check(p)
        ctx.rosters[op['key']]=record
        for g in z['selected_groups']:
            ctx.groups[(op['key'],g['key'])]={'cursor':0,'active':None,'fragments':[]}
        return True
    group=ctx.groups[(op['key'],op['stream'])]
    if op['kind']=='index':
        if status not in ('FROZEN_RECOUNT_JOBS','PARTIAL') or not z.get('records'):
            ctx.zero_attempts.increment(token); return False
        validate_manifest(ctx,op,record)
        group['active']={'index':record,'manifest':z,'matched':{},'runs':[],'source_start':op['slice'][0]}
        return status=='FROZEN_RECOUNT_JOBS'
    active=group['active']
    if op['kind']=='count':
        U.need(status in ('SLICE_RECOUNTS_MATCH','PARTIAL','COUNT_MISMATCH'),'Unknown count status')
        validate_count(ctx,op,record,active); active['runs'].append(record)
        if status=='COUNT_MISMATCH': ctx.fatal=record['result_pin']['path']
        return status=='SLICE_RECOUNTS_MATCH'
    U.need(op['kind']=='aggregate','Unknown operation')
    expected={n for e in active['manifest']['records'] for n in e['node_ids']}
    U.need(status in ('COMPLETE_FROZEN_RECOUNTS_MATCH','PARTIAL') and z['manifest_sha256']==active['index']['result_pin']['sha256']
           and z['matched_node_ids']==sorted(expected) and not z['pending_node_ids'] and not z['mismatches']
           and z['complete_record_ids']==sorted(e['id'] for e in active['manifest']['records']), 'Numerical fragment aggregate has missing/refused/extra nodes')
    # A deadline-limited index's pending source IDs are not hidden. This fragment
    # covers only emitted records; the next source slice covers the remaining
    # literal roster. No PARTIAL receipt or old path is rewritten to PASS.
    U.need(z['pending_index_record_ids']==active['manifest']['pending_index_ids'],'Aggregate changed unindexed source obligations')
    group['fragments'].append({'index':active['index'],'aggregate':record,'runs':active['runs'],
                              'source_slice':[active['source_start'],active['source_start']+len(active['manifest']['records'])]})
    group['cursor']+=len(active['manifest']['records']); group['active']=None
    return True


def audit(ctx):
    for item in ctx.state['attempts']:
        request,record=authenticate(ctx,item); op=request['operation']
        cohort=request['requested_cohort']; U.need(cohort in (*U.COHORTS,'all'),'Unknown requested cohort')
        U.need(op==ctx.next(cohort),'Repeated successful, skipped, stale or foreign operation')
        U.need(request['inputs']==expected_inputs(ctx,op),'Missing/stale child input roster')
        apply(ctx,op,record)
    return ctx


def remaining(ctx,cohort):
    result=[]
    for key,c,unit in ctx.roster_keys(cohort):
        if key not in ctx.rosters:
            result.append({'key':key,'state':'UNRESOLVED_LITERAL_SOURCE_ROSTER','cohort':c,'unit':unit}); continue
        for group in ctx.rosters[key]['result']['selected_groups']:
            g=ctx.groups[(key,group['key'])]; active=g['active']
            if g['cursor']==len(group['records']): continue
            pending=[]
            if active: pending=sorted({n for e in active['manifest']['records'] for n in e['node_ids']}-set(active['matched']))
            result.append({'key':key,'stream':group['key'],'source_roster':ctx.rosters[key]['result_pin'],
                           'remaining_source_slice':[g['cursor'],len(group['records'])],
                           'remaining_source_records':group['records'][g['cursor']:],
                           'active_manifest':None if active is None else active['index']['result_pin'],
                           'pending_active_node_ids':pending})
    return result


def run(ctx,cohort,max_jobs):
    launched=0
    while max_jobs is None or launched<max_jobs:
        op=ctx.next(cohort)
        if op is None: break
        token=U.sha(U.encoded(op))
        U.need(ctx.zero_attempts.get(token,0)<3,'Three zero-progress attempts exhausted; exact operation remains pending')
        U.need(ctx.elapsed+120<=ctx.recipe['settings']['total_child_seconds'],'Cannot reserve the entire next 120-second child deadline within this local epoch budget')
        ctx.stable(); inputs=expected_inputs(ctx,op)
        for p in inputs: U.check(p)
        identity=f'numerics-{len(ctx.state["attempts"])+1:06d}'
        request={'schema':U.SCHEMA,'id':identity,'recipe':ctx.state['recipe'],'operation':op,'requested_cohort':cohort,
                 'inputs':inputs,'output':str(ctx.work/'jobs'/identity/'result.json'),
                 'reservation_seconds':120,'charged_elapsed_before':ctx.elapsed}
        path=ctx.work/'requests'/(identity+'.json'); U.save(path,request); rp=U.pin(path)
        item={'id':identity,'request':rp}; ctx.state['attempts'].append(item); replace_state(ctx.work,ctx.state)
        execute(ctx,request,rp); actual,record=authenticate(ctx,item); complete=apply(ctx,op,record); launched+=1
        print(json.dumps({'id':identity,'operation':op['kind'],'cohort':op.get('cohort'),'status':None if record is None else record['result']['status'],
                          'child_seconds_used':round(ctx.elapsed,3)}),flush=True)
        # A partial explicit prefix can be reused by the next owner invocation.
        # No refusal, timeout or mismatch automatically starts another child.
        if not complete: break
    pending=remaining(ctx,cohort)
    report={'schema':U.SCHEMA,'mode':ctx.recipe['mode'],'cohort':cohort,'status':'COUNT_ENGINE_STEPS_COMPLETE_PENDING_GLOBAL_JOIN' if not pending else 'PENDING',
            'recipe':ctx.state['recipe'],'remaining':pending,'fatal':ctx.fatal,'child_seconds_used':ctx.elapsed,'scope':U.SCOPE}
    p=fresh_report(ctx.work,'progress',report)
    return {'status':report['status'],'report':p,'remaining_streams':len(pending),'scope':U.SCOPE}


def global_aggregate(ctx,cohort):
    U.need(ctx.fatal is None and not remaining(ctx,cohort),'Global numerical coverage still has pending/fatal identities')
    identities=[]; node_ids=set(); seen=set(); fragments=[]
    for key,c,unit in ctx.roster_keys(cohort):
        for group in ctx.rosters[key]['result']['selected_groups']:
            g=ctx.groups[(key,group['key'])]; cursor=0
            for f in g['fragments']:
                start,stop=f['source_slice']; U.need(start==cursor,'Missing or overlapping numerical source fragment'); cursor=stop
                manifest=f['index']['result']; source=group['records'][start:stop]
                U.need([e['id'] for e in manifest['records']]==[r['id'] for r in source],'Fragment differs from literal source IDs')
                for source_row,entry in zip(source,manifest['records']):
                    identity=(source_row['unit'],source_row['id']); U.need(identity not in seen,'Duplicate successful source record'); seen.add(identity)
                    U.need(not node_ids.intersection(entry['node_ids']),'Duplicate successful physical node across manifests'); node_ids.update(entry['node_ids'])
                    identities.append({**source_row,'roster_key':key,'stream':group['key'],'node_ids':entry['node_ids'],
                                       'index':f['index']['result_pin'],'count_aggregate':f['aggregate']['result_pin']})
                fragments.append({'index':f['index']['result_pin'],'index_execution':f['index']['execution_pin'],
                                  'aggregate':f['aggregate']['result_pin'],'aggregate_execution':f['aggregate']['execution_pin'],
                                  'original_index_pending_source_ids':manifest['pending_index_ids'],
                                  'accepted_actual_source_slice':[start,stop],
                                  'counts':[{'report':r['result_pin'],'execution':r['execution_pin']} for r in f['runs']]})
            U.need(cursor==len(group['records']),'Full source stream has an uncounted suffix')
    if ctx.recipe['mode']=='full':
        expected=sum(U.TOTALS.values()) if cohort=='all' else U.TOTALS[cohort]
        U.need(len(identities)==expected,'Full literal source population differs at final numerical union')
    ctx.stable()
    result={'schema':U.SCHEMA,'kind':'global_count_evidence','status':'FULL_LITERAL_COUNT_EVIDENCE_COMPLETE_PENDING_MATHEMATICAL_JOINS'
            if ctx.recipe['mode']=='full' else 'REPRESENTATIVE_COUNTS_MATCH_ONLY',
            'mode':ctx.recipe['mode'],'cohort':cohort,'u02_holdouts':ctx.recipe['holdouts'],'recipe':ctx.state['recipe'],'build':ctx.build['result_pin'],
            'exact_source_and_node_roster':identities,'records':len(identities),'physical_nodes':len(node_ids),
            'fragments':fragments,'child_seconds_used':ctx.elapsed,'whole_theorem_accepted':False,'scope':U.SCOPE}
    p=fresh_report(ctx.work,'aggregate',result)
    return {'status':result['status'],'records':len(identities),'physical_nodes':len(node_ids),'aggregate':p,'scope':U.SCOPE}


@contextmanager
def lock(work):
    with U.plain(U.plain(work)/'LOCK').open('a') as f:
        try: fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise U.Invalid('Another controller owns this epoch') from None
        yield


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    prep=sub.add_parser('prepare'); prep.add_argument('--work-root',type=Path,required=True); prep.add_argument('--data-root',type=Path,required=True)
    prep.add_argument('--mode',choices=('representative','full'),required=True); prep.add_argument('--compiler',type=Path,required=True)
    prep.add_argument('--holdouts',choices=('first-unused','original'),default='first-unused',
                      help='U02: source-bound first two unused positive grades (recommended), or all original physical holds')
    prep.add_argument('--total-seconds',type=float,required=True)
    for field in METADATA:
        flag=field.replace('_','-'); prep.add_argument('--'+flag,type=Path,required=True); prep.add_argument('--'+flag+'-sha256',required=True)
    for name,default in (('production-index-chunk',32768),('production-count-chunk',512),('early-chunk',64),('legacy-chunk',4),('u11-chunk',4)):
        prep.add_argument('--'+name,type=int,default=default)
    for name in ('run','status','aggregate'):
        cmd=sub.add_parser(name); cmd.add_argument('--work-root',type=Path,required=True); cmd.add_argument('--cohort',choices=(*U.COHORTS,'all'),required=True)
        if name=='run': cmd.add_argument('--max-jobs',type=int)
    c=sub.add_parser('_child',help=argparse.SUPPRESS); c.add_argument('--request',type=Path,required=True); c.add_argument('--request-sha256',required=True)
    args=p.parse_args(); ctx=None
    try:
        if args.command=='_child': return child(args.request,args.request_sha256)
        if args.command=='prepare': result=prepare(args)
        else:
            U.need(sys.version_info>=(3,10) and os.name=='posix','Python 3.10+ POSIX required')
            with lock(args.work_root):
                ctx=Context(args.work_root); audit(ctx)
                if args.command=='run':
                    U.need(args.max_jobs is None or args.max_jobs>0,'max-jobs must be positive'); result=run(ctx,args.cohort,args.max_jobs)
                elif args.command=='aggregate': result=global_aggregate(ctx,args.cohort)
                else:
                    result={'schema':U.SCHEMA,'cohort':args.cohort,'mode':ctx.recipe['mode'],'remaining':remaining(ctx,args.cohort),
                            'fatal':ctx.fatal,'child_seconds_used':ctx.elapsed,'scope':U.SCOPE}
                    result={'status':'PENDING' if result['remaining'] or result['fatal'] else 'COUNT_STEPS_COMPLETE','report':fresh_report(ctx.work,'status',result)}
        print(json.dumps(result,sort_keys=True),flush=True); return 0
    except Exception as error:
        failure={'schema':U.SCHEMA,'status':'REFUSED','error':f'{type(error).__name__}: {error}','scope':U.SCOPE}
        if ctx is not None:
            failure.update(recipe=ctx.state['recipe'],journal_snapshot=ctx.state,remaining=remaining(ctx,args.cohort),fatal=ctx.fatal)
            failure['report']=fresh_report(ctx.work,'refusal',failure)
        print(json.dumps(failure,sort_keys=True),file=sys.stderr); return 2


# EXACT_SUCCESSOR_EXTENSION_BOUNDARY
"""Source-guarded continuation; the exact a6d3 controller above stays preserved.

This file may remain beside the old numerics.py for explicit continuation, or
be installed as numerics.py in a fresh publication. No predecessor process,
receipt, recipe or scientific source is rewritten. Only the aggregate matched
key-set cache changes mathematical execution; the predicate is AST-guarded.
"""
import ast
import copy

PREDECESSOR_SHA='a6d3cbb53409baa7fefdad19ee471d8c864428564d5d7988ac120a55347b7e50'
WRAPPER_SHA='f62a78a78f1d38452fb805ca051c89fe1dabf26d0d2c0d6a900c9200fd6aa4e7'
COMMON_SHA='2766854c99969c2c2fead4217a2e35cb6f1e3069bb9ff3e045c0d73d4ee568d5'
BOUNDARY=b'# EXACT_SUCCESSOR_EXTENSION_BOUNDARY\n'
OLD_FOOTER=b"if __name__=='__main__': sys.exit(main())\n"
BASE_SOURCE=Path(__file__).read_bytes().split(BOUNDARY,1)[0]+OLD_FOOTER
U.need(U.sha(BASE_SOURCE)==PREDECESSOR_SHA,'Exact preserved controller prefix changed')
U.need(Path(U.__file__).resolve()==Path(__file__).resolve().with_name('common.py') and U.pin(U.__file__)['sha256']==COMMON_SHA,
       'Successor must use the exact sibling common source')
BASE_TREE=ast.parse(BASE_SOURCE)
_base_context=Context
_base_apply=apply
_base_main=main
_base_prepare=prepare
_transition_creation=False
PATCHES={}
_linear_cache={}

def active_adapter():
    return U.pin(__file__)

def recipe_driver(recipe):
    path=str(U.HERE/'numerics.py');rows=[p for p in recipe['code'] if p['path']==path]
    U.need(len(rows)==1,'Recipe must identify its literal numerics.py source')
    driver=rows[0];U.check(driver)
    U.need(driver['sha256']==PREDECESSOR_SHA or driver==active_adapter(),'Unaccepted numerical driver epoch')
    return driver

def check_transition(work,state,recipe):
    driver=recipe_driver(recipe)
    if driver==active_adapter():
        U.need(not (work/'ADAPTER-TRANSITION.json').exists(),'Fresh successor recipe cannot import a prior transition')
        return None,{}
    path=work/'ADAPTER-TRANSITION.json'
    if not path.exists():
        U.need(_transition_creation,'Exact predecessor continuation needs an explicit pinned transition first')
        return None,{x['id']:x['request'] for x in state['attempts']}
    tp=U.pin(path);t=U.read(path)
    U.need(t['schema']=='portable-numerics-adapter-transition-v1' and t['active_adapter']==active_adapter() and
           t['recipe']==state['recipe'] and t['predecessor_driver']==driver,'Transition belongs to another source/recipe epoch')
    U.check(t['state_snapshot']);old=U.read(t['state_snapshot']['path'])
    U.need(t['state_snapshot']['path']==str(work/'ADAPTER-PREDECESSOR-STATE.json') and
           t['predecessor_state']['path']==str(work/'STATE.json') and
           all(t['predecessor_state'][k]==t['state_snapshot'][k] for k in ('bytes','sha256')),
           'Transition snapshot is not the original exact state bytes')
    U.need(old['recipe']==state['recipe'] and not old.get('mandatory_holds') and
           state['attempts'][:len(old['attempts'])]==old['attempts'] and t['prior_attempts']==len(old['attempts']),
           'Predecessor execution prefix changed after transition')
    return tp,{x['id']:x['request'] for x in old['attempts']}

class Context(_base_context):
    def __init__(self,work):
        self.transition=None;self.old_requests={};self.unearned_aggregates=[]
        super().__init__(work)
    def stable(self):
        super().stable()
        self.transition,self.old_requests=check_transition(self.work,self.state,self.recipe)

def adapter_inputs(original,adapter=None,transition=None):
    rows={p['path']:p for p in original}
    for p in (adapter,transition):
        if p is not None:
            U.check(p);U.need(p['path'] not in rows or rows[p['path']]==p,'Conflicting active source/transition pin');rows[p['path']]=p
    return [rows[k] for k in sorted(rows)]

def decorate_request(ctx,request):
    p=active_adapter();transition=ctx.transition
    U.need(recipe_driver(ctx.recipe)==p or transition is not None,'Missing predecessor transition')
    return {**request,'active_adapter':p,'adapter_transition':transition,
            'inputs':adapter_inputs(request['inputs'],p,transition)}

def request_driver(ctx,request,request_pin):
    driver=recipe_driver(ctx.recipe);adapter=request.get('active_adapter')
    if adapter is None:
        U.need(driver['sha256']==PREDECESSOR_SHA and request.get('adapter_transition') is None and
               ctx.old_requests.get(request['id'])==request_pin,'Unpinned old driver call outside the exact predecessor prefix')
        return driver
    U.need(adapter==active_adapter() and request.get('adapter_transition')==ctx.transition and
           adapter in request['inputs'] and (ctx.transition is None or ctx.transition in request['inputs']),
           'Wrong active adapter/transition/input binding')
    U.need(request['id'] not in ctx.old_requests,'A predecessor request was relabelled as an adapter execution')
    return adapter

def adapter_fields(request,record):
    if 'active_adapter' in request:
        U.need(record.get('active_adapter')==request['active_adapter'] and record.get('adapter_transition')==request['adapter_transition'],
               'Actual child/execution lost its active source/transition declaration')
    else:U.need('active_adapter' not in record and 'adapter_transition' not in record,'Old receipt acquired a fictitious adapter declaration')

def validate_new_request(recipe,request,rp):
    U.need(request.get('active_adapter')==active_adapter(),'Successor child requires its own exact active-adapter pin')
    state=U.read(Path(recipe['work_root'])/'STATE.json')
    transition,old=check_transition(Path(recipe['work_root']),state,recipe)
    ctx=SimpleNamespace(recipe=recipe,transition=transition,old_requests=old)
    request_driver(ctx,request,rp)

def linear_function(R):
    source=U.pin(R.__file__);U.need(source['sha256']==WRAPPER_SHA,'Changed original mathematical wrapper')
    if source['sha256'] in _linear_cache:return _linear_cache[source['sha256']]
    tree=ast.parse(Path(R.__file__).read_bytes());original=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='aggregate')
    old=ast.dump(original,include_attributes=False);patched=copy.deepcopy(original)
    U.need(not any(isinstance(n,ast.Name) and n.id=='matched_keys' for n in ast.walk(original)),'Cache name already exists in original predicate')
    class Cache(ast.NodeTransformer):
        def __init__(self):self.changed=0
        def visit_Call(self,node):
            if isinstance(node.func,ast.Name) and node.func.id=='set' and len(node.args)==1 and isinstance(node.args[0],ast.Name) and node.args[0].id=='matched' and not node.keywords:
                self.changed+=1;return ast.copy_location(ast.Name(id='matched_keys',ctx=ast.Load()),node)
            return self.generic_visit(node)
    change=Cache();patched=change.visit(patched);U.need(change.changed==2,'Original matched-set sites differ from the reviewed two sites')
    at=[i for i,n in enumerate(patched.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='missing' for t in n.targets)]
    U.need(len(at)==1,'Missing exact final aggregation boundary')
    assignment=ast.parse('matched_keys=set(matched)').body[0];patched.body.insert(at[0],assignment)
    # Inverting this one cache transformation must restore every original AST node.
    inverse=copy.deepcopy(patched);del inverse.body[at[0]]
    class Restore(ast.NodeTransformer):
        def visit_Name(self,node):
            if node.id=='matched_keys':return ast.copy_location(ast.parse('set(matched)',mode='eval').body,node)
            return node
    inverse=Restore().visit(inverse)
    U.need(ast.dump(inverse,include_attributes=False)==old,'Aggregation predicate changed beyond the cache')
    module=ast.fix_missing_locations(ast.Module(body=[patched],type_ignores=[]));namespace=dict(R.__dict__)
    exec(compile(module,str(Path(__file__).resolve())+'::exact-linear-aggregate','exec'),namespace)
    proof={'original_wrapper':source,'original_aggregate_ast_sha256':U.sha(old.encode()),
           'executed_aggregate_ast_sha256':U.sha(ast.dump(patched,include_attributes=False).encode()),
           'change':'One final matched_keys=set(matched); both original set(matched) expressions use that cache; exact inverse AST equality checked.'}
    _linear_cache[source['sha256']]=(namespace['aggregate'],proof)
    return _linear_cache[source['sha256']]

def linear_aggregate(R,args,deadline,result):
    function,proof=linear_function(R)
    result['aggregation_adapter']={'active_adapter':active_adapter(),**proof}
    return function(args,deadline,result)

AGGREGATE_FIELDS={'manifest_sha256','matched_node_ids','pending_node_ids','pending_index_record_ids','mismatches','complete_record_ids'}
def apply(ctx,op,record):
    if ctx.fatal is not None:return False
    if op['kind']=='aggregate' and record is not None:
        z=record['result'];missing=AGGREGATE_FIELDS-set(z)
        if z.get('status')=='PARTIAL' and missing:
            U.need(z.get('kind')=='aggregate' and z.get('schema')=='pro026-independent-hive-recount-v1' and
                   z.get('wrapper_sha256')==WRAPPER_SHA and z.get('source_bytes_verified_before_after') is True and
                   type(z.get('interruption')) is str and bool(z['interruption']),
                   'Incomplete aggregate is not the source-bound interrupted predicate')
            ctx.unearned_aggregates.append({'result':record['result_pin'],'missing_success_fields':sorted(missing),'accepted':False})
            ctx.zero_attempts.increment(U.sha(U.encoded(op)));return False
    return _base_apply(ctx,op,record)

def patch_function(name,changes):
    node=next(n for n in BASE_TREE.body if isinstance(n,ast.FunctionDef) and n.name==name)
    original=ast.get_source_segment(BASE_SOURCE.decode(),node);text=original
    for before,after in changes:
        U.need(text.count(before)==1,'Controller patch site changed: '+name+' / '+before[:80]);text=text.replace(before,after,1)
    generated=ast.parse(text);U.need(len(generated.body)==1 and generated.body[0].name==name,'Invalid bounded controller patch')
    PATCHES[name]={'original_source_sha256':U.sha(original.encode()),'executed_source_sha256':U.sha(text.encode()),'exact_replacements':len(changes)}
    exec(compile(generated,str(Path(__file__).resolve())+'::'+name,'exec'),globals())

patch_function('child',[
 ("request=U.read(request_path); U.check(request['recipe']); recipe=U.read(request['recipe']['path'])",
  "request=U.read(request_path); U.check(request['recipe']); recipe=U.read(request['recipe']['path'])\n    validate_new_request(recipe,request,rp)"),
 ("'code':recipe['code'],'before_mathematical_calls':True}",
  "'code':recipe['code'],'active_adapter':request['active_adapter'],'adapter_transition':request['adapter_transition'],'before_mathematical_calls':True}"),
 ("'wrapper_sha256':U.pin(R.__file__)['sha256'],'portable_request':rp,'scope':U.SCOPE}",
  "'wrapper_sha256':U.pin(R.__file__)['sha256'],'portable_request':rp,'scope':U.SCOPE,\n          'active_adapter':request['active_adapter'],'adapter_transition':request['adapter_transition']}") ,
 ("R.aggregate(args,deadline,result)","linear_aggregate(R,args,deadline,result)")])
patch_function('execute',[
 ("str(U.HERE/'numerics.py')","request['active_adapter']['path']"),
 ("'schema':U.SCHEMA,'kind':'execution','request':request_pin,'command':command,**outcome,",
  "'schema':U.SCHEMA,'kind':'execution','request':request_pin,'command':command,**outcome,\n            'active_adapter':request['active_adapter'],'adapter_transition':request['adapter_transition'],")])
patch_function('authenticate',[
 ("U.need(request['id']==item['id'] and request['recipe']==ctx.state['recipe'],'Request belongs to another epoch')",
  "U.need(request['id']==item['id'] and request['recipe']==ctx.state['recipe'],'Request belongs to another epoch')\n    driver=request_driver(ctx,request,item['request'])"),
 ("e=U.read(ep['path'])","e=U.read(ep['path']); adapter_fields(request,e)"),
 ("str(U.HERE/'numerics.py')","driver['path']"),
 ("launch=U.read(directory/'LAUNCH.json'); applied=U.read(directory/'CHILD.json')",
  "launch=U.read(directory/'LAUNCH.json'); applied=U.read(directory/'CHILD.json'); adapter_fields(request,applied)"),
 ("z=U.read(directory/'result.json')","z=U.read(directory/'result.json'); adapter_fields(request,z)")])
patch_function('run',[
 ("path=ctx.work/'requests'/(identity+'.json'); U.save(path,request); rp=U.pin(path)",
  "request=decorate_request(ctx,request)\n        path=ctx.work/'requests'/(identity+'.json'); U.save(path,request); rp=U.pin(path)")])
patch_function('audit',[
 ("request['inputs']==expected_inputs(ctx,op)","request['inputs']==adapter_inputs(expected_inputs(ctx,op),request.get('active_adapter'),request.get('adapter_transition'))")])
patch_function('global_aggregate',[
 ("'recipe':ctx.state['recipe'],'build':ctx.build['result_pin'],",
  "'recipe':ctx.state['recipe'],'build':ctx.build['result_pin'],\n            'active_adapter':active_adapter(),'adapter_transition':ctx.transition,")])

def transition(work,expected_state_sha256):
    global _transition_creation
    work=U.plain(work);before=U.pin(work/'STATE.json')
    U.need(before['sha256']==expected_state_sha256,'Exact predecessor STATE hash differs')
    U.need(not (work/'ADAPTER-TRANSITION.json').exists() and not (work/'ADAPTER-PREDECESSOR-STATE.json').exists(),'Transition destinations must be fresh')
    _transition_creation=True
    try:
        ctx=Context(work);U.need(recipe_driver(ctx.recipe)['sha256']==PREDECESSOR_SHA,'Only the exact a6d3 predecessor can transition')
        audit(ctx)
        U.need(ctx.fatal is None and U.pin(work/'STATE.json')==before,'Adverse or changed state cannot transition')
        for item in ctx.state['attempts']:
            U.need('active_adapter' not in U.read(item['request']['path']),'Predecessor prefix already contains another adapter')
        snapshot=work/'ADAPTER-PREDECESSOR-STATE.json'
        with snapshot.open('xb') as stream:stream.write(Path(before['path']).read_bytes());stream.flush();os.fsync(stream.fileno())
        record={'schema':'portable-numerics-adapter-transition-v1','active_adapter':active_adapter(),'recipe':ctx.state['recipe'],
                'predecessor_driver':recipe_driver(ctx.recipe),'predecessor_state':before,'state_snapshot':U.pin(snapshot),
                'prior_attempts':len(ctx.state['attempts']),'prior_elapsed_child_seconds':ctx.elapsed,
                'unearned_aggregates':ctx.unearned_aggregates,'mathematical_predicate_source':WRAPPER_SHA,
                'prior_recipe_receipts_and_counts_unchanged':True,'new_counts_or_aggregates_executed':0}
        U.save(work/'ADAPTER-TRANSITION.json',record)
        return {'status':'EXACT_PREDECESSOR_TRANSITION_RECORDED','transition':U.pin(work/'ADAPTER-TRANSITION.json'),
                'prior_attempts':record['prior_attempts'],'unearned_aggregates':ctx.unearned_aggregates}
    finally:_transition_creation=False

def successor_main():
    if len(sys.argv)>1 and sys.argv[1]=='transition':
        parser=argparse.ArgumentParser(description='Explicit exact-source transition; no counts or aggregates are run')
        parser.add_argument('command',choices=['transition']);parser.add_argument('--work-root',type=Path,required=True)
        parser.add_argument('--expected-state-sha256',required=True);args=parser.parse_args()
        try:
            with lock(args.work_root):result=transition(args.work_root,args.expected_state_sha256)
            print(json.dumps(result,sort_keys=True),flush=True);return 0
        except Exception as error:
            print(json.dumps({'status':'TRANSITION_REFUSED','error':f'{type(error).__name__}: {error}'}),file=sys.stderr,flush=True);return 2
    return _base_main()

# FRESH_FINITE_SCHEDULING_EXTENSION
"""Fresh-only finite scheduling successor. Old bcd/a6 bodies and math remain preserved.
The parent retains its one audited Context across usable PARTIAL count retries.
Fresh run requires --max-jobs and --total-seconds; old transitions are refused.
"""
SCHEDULING_BCD_SHA='bcd65c34e136c1ab51fe405a7851fc9dd9d82332a89c51d1027b51cfd696ef1e'
SCHEDULING_RUN_SHA='1a3b507989ce893f281dfe3d13796aa7a476c5034a91cba8c5f2b97a8d06204e'
SCHEDULING_BOUNDARY=b'# FRESH_FINITE_SCHEDULING_EXTENSION\n'
SCHEDULING_BCD_SOURCE=Path(__file__).read_bytes().split(SCHEDULING_BOUNDARY,1)[0]+b"if __name__=='__main__':sys.exit(successor_main())\n"
U.need(U.sha(SCHEDULING_BCD_SOURCE)==SCHEDULING_BCD_SHA,'Preserved exact bcd source changed')
_scheduling_base_recipe_driver=recipe_driver

def recipe_driver(recipe):
    driver=_scheduling_base_recipe_driver(recipe)
    U.need(driver==active_adapter(),'Scheduled publication driver requires its own fresh recipe; no old transition adoption')
    return driver

def scheduling_limits(max_jobs,total_seconds):
    if not (type(max_jobs) is int and max_jobs>0 and type(total_seconds) in (int,float)
            and math.isfinite(total_seconds) and total_seconds>=120):
        raise ValueError('Explicit positive finite max-jobs and total-seconds >= 120 are required')

def usable_count_partial(ctx,op,record,schedule):
    if (ctx.fatal is not None or op['kind']!='count' or record is None or
            record['result'].get('status')!='PARTIAL' or record.get('usable_count_report') is not True):
        return False
    active=ctx.groups[(op['key'],op['stream'])]['active']
    previous=[r for r in active['runs'] if r['operation']['slice']==op['slice']]
    if not (previous and previous[-1] is record and record['operation']==op and
            len(previous)<=len(schedule) and
            [op['node_ms'],op['max_states']]==list(schedule[len(previous)-1])):
        raise ValueError('Usable partial did not consume exactly its existing finite retry rung')
    return True

def scheduled_run(ctx,cohort,max_jobs,call_deadline,source_guard,source_profile):
    if type(max_jobs) is not int or max_jobs<=0 or not math.isfinite(call_deadline):
        raise ValueError("Finite scheduling invocation required")
    source_guard()
    launched=0; stop_reason="MAX_JOBS"
    while launched<max_jobs:
        op=ctx.next(cohort)
        if op is None:
            stop_reason="EXISTING_COUNT_CURSOR_COMPLETE"; break
        source_guard()
        if time.monotonic()+120>call_deadline:
            stop_reason="LOCAL_CALL_BUDGET"; break
        token=U.sha(U.encoded(op))
        U.need(ctx.zero_attempts.get(token,0)<3,'Three zero-progress attempts exhausted; exact operation remains pending')
        U.need(ctx.elapsed+120<=ctx.recipe['settings']['total_child_seconds'],'Cannot reserve the entire next 120-second child deadline within this local epoch budget')
        ctx.stable(); inputs=expected_inputs(ctx,op)
        for p in inputs: U.check(p)
        source_guard()
        if time.monotonic()+120>call_deadline:
            stop_reason="LOCAL_CALL_BUDGET_AFTER_INPUT_CHECKS"; break
        identity=f'numerics-{len(ctx.state["attempts"])+1:06d}'
        request={'schema':U.SCHEMA,'id':identity,'recipe':ctx.state['recipe'],'operation':op,'requested_cohort':cohort,
                 'inputs':inputs,'output':str(ctx.work/'jobs'/identity/'result.json'),
                 'reservation_seconds':120,'charged_elapsed_before':ctx.elapsed}
        request=decorate_request(ctx,request)
        path=ctx.work/'requests'/(identity+'.json'); U.save(path,request); rp=U.pin(path)
        item={'id':identity,'request':rp}; ctx.state['attempts'].append(item); replace_state(ctx.work,ctx.state)
        execute(ctx,request,rp); actual,record=authenticate(ctx,item); complete=apply(ctx,op,record); launched+=1
        print(json.dumps({'id':identity,'operation':op['kind'],'cohort':op.get('cohort'),'status':None if record is None else record['result']['status'],
                          'child_seconds_used':round(ctx.elapsed,3)}),flush=True)
        # Only this authenticated usable PARTIAL count can continue. Context.next
        # alone chooses the unchanged finite retry ladder; fatal holds always stop.
        if not complete and not usable_count_partial(ctx,op,record,U.SCHEDULE):
            stop_reason="UNUSABLE_OR_NONCOUNT_PARTIAL_OR_HOLD"; break
    ctx.stable(); source_guard()
    pending=remaining(ctx,cohort)
    report={'schema':U.SCHEMA,'mode':ctx.recipe['mode'],'cohort':cohort,'status':'COUNT_ENGINE_STEPS_COMPLETE_PENDING_GLOBAL_JOIN' if not pending else 'PENDING',
            'recipe':ctx.state['recipe'],'remaining':pending,'fatal':ctx.fatal,'child_seconds_used':ctx.elapsed,'scope':U.SCOPE}
    report['scheduling']={'source_profile':source_profile,'max_jobs':max_jobs,'launched_jobs':launched,
                          'stop_reason':stop_reason,'call_deadline_monotonic':call_deadline,
                          'count_retry_schedule_unchanged':True}
    p=fresh_report(ctx.work,'progress',report)
    return {'status':report['status'],'report':p,'remaining_streams':len(pending),'scope':U.SCOPE}

def fresh_scheduled_main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    prep=sub.add_parser('prepare'); prep.add_argument('--work-root',type=Path,required=True); prep.add_argument('--data-root',type=Path,required=True)
    prep.add_argument('--mode',choices=('representative','full'),required=True); prep.add_argument('--compiler',type=Path,required=True)
    prep.add_argument('--holdouts',choices=('first-unused','original'),default='first-unused',
                      help='U02: source-bound first two unused positive grades (recommended), or all original physical holds')
    prep.add_argument('--total-seconds',type=float,required=True)
    for field in METADATA:
        flag=field.replace('_','-'); prep.add_argument('--'+flag,type=Path,required=True); prep.add_argument('--'+flag+'-sha256',required=True)
    for name,default in (('production-index-chunk',32768),('production-count-chunk',512),('early-chunk',64),('legacy-chunk',4),('u11-chunk',4)):
        prep.add_argument('--'+name,type=int,default=default)
    for name in ('run','status','aggregate'):
        cmd=sub.add_parser(name); cmd.add_argument('--work-root',type=Path,required=True); cmd.add_argument('--cohort',choices=(*U.COHORTS,'all'),required=True)
        if name=='run':
            cmd.add_argument('--max-jobs',type=int,required=True)
            cmd.add_argument('--total-seconds',type=float,required=True)
    c=sub.add_parser('_child',help=argparse.SUPPRESS); c.add_argument('--request',type=Path,required=True); c.add_argument('--request-sha256',required=True)
    args=p.parse_args(); ctx=None; scheduling_started=time.monotonic()
    try:
        if args.command=='_child': return child(args.request,args.request_sha256)
        if args.command=='prepare': result=prepare(args)
        else:
            U.need(sys.version_info>=(3,10) and os.name=='posix','Python 3.10+ POSIX required')
            if args.command=='run':
                scheduling_limits(args.max_jobs,args.total_seconds)
                scheduling_deadline=scheduling_started+args.total_seconds
                scheduling_source=active_adapter()
            with lock(args.work_root):
                ctx=Context(args.work_root); audit(ctx)
                if args.command=='run':
                    result=scheduled_run(ctx,args.cohort,args.max_jobs,scheduling_deadline,
                        lambda:U.check(scheduling_source),{'fresh_parent_and_child_source':scheduling_source,
                        'base_bcd_source_sha256':SCHEDULING_BCD_SHA,'executed_run_sha256':SCHEDULING_RUN_SHA})
                elif args.command=='aggregate': result=global_aggregate(ctx,args.cohort)
                else:
                    result={'schema':U.SCHEMA,'cohort':args.cohort,'mode':ctx.recipe['mode'],'remaining':remaining(ctx,args.cohort),
                            'fatal':ctx.fatal,'child_seconds_used':ctx.elapsed,'scope':U.SCOPE}
                    result={'status':'PENDING' if result['remaining'] or result['fatal'] else 'COUNT_STEPS_COMPLETE','report':fresh_report(ctx.work,'status',result)}
        print(json.dumps(result,sort_keys=True),flush=True); return 0
    except Exception as error:
        failure={'schema':U.SCHEMA,'status':'REFUSED','error':f'{type(error).__name__}: {error}','scope':U.SCOPE}
        if ctx is not None:
            failure.update(recipe=ctx.state['recipe'],journal_snapshot=ctx.state,remaining=remaining(ctx,args.cohort),fatal=ctx.fatal)
            failure['report']=fresh_report(ctx.work,'refusal',failure)
        print(json.dumps(failure,sort_keys=True),file=sys.stderr); return 2

if __name__=='__main__':sys.exit(fresh_scheduled_main())
