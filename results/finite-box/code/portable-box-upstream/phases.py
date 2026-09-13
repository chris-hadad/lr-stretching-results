"""Explicit fresh F025 dependency graph and path-only invocation rosters."""
from pathlib import Path
from types import SimpleNamespace
from fractions import Fraction
import copy
import gzip
import json
import os
import subprocess
import time
import common as U

CPP={'census':'verification/census/original_box_census_v1.cpp','maps':'verification/maps/verify_maps.cpp',
     'counter':'verification/chart-counter/chart_counter_v3.cpp'}
LANES=('masks','inputs','census','maps','metrics','small','quartics','cover','all')


class ReconciliationMismatch(U.Invalid):
 """A durable, source-bound disagreement; not a proved LR counterexample."""


def adverse_event(folder,phase,predicate,identity,expected,observed,sources,kind='source_or_hold_mismatch'):
 event={'schema':'portable-f025-adverse-observation-v1','phase':phase,'kind':kind,'predicate':predicate,
        'identity':identity,'expected':expected,'observed':observed,'sources':sources,
        'adapter':U.pin(__file__),'requires_owner_disposition':True,'authenticated_scientific_result':False,
        'scope':'Whole-chart vector/count/source agreement observation; original boundary and complete proof premises still require validation.'}
 with (folder/'ADVERSE-OBSERVATIONS.jsonl').open('ab') as stream:
  stream.write(U.encoded(event)+b'\n');stream.flush();os.fsync(stream.fileno())
 raise ReconciliationMismatch(f'{phase}: {predicate}; exact identity {identity!r}; observed {observed!r}, expected {expected!r}')


def reconcile_equal(folder,phase,predicate,identity,expected,observed,sources):
 if expected!=observed:adverse_event(folder,phase,predicate,identity,expected,observed,sources)


def vector_observation(folder,phase,identity,record,sources,label):
 raw=record.get('coefficients')
 try:
  U.need(isinstance(raw,list) and raw and all(type(v) in (str,int) for v in raw),'Missing exact coefficient vector')
  co=list(map(Fraction,raw))
 except (ValueError,TypeError,ZeroDivisionError) as error:
  adverse_event(folder,phase,label+'_exact_vector',identity,'nonempty exact rational vector',{'coefficients':raw,'error':str(error)},sources)
 negative=[{'degree':i,'coefficient':str(c)} for i,c in enumerate(co) if c<0]
 if negative:
  adverse_event(folder,phase,label+'_ordinary_sign',identity,'no negative ordinary coefficients',
                {'coefficients':list(map(str,co)),'negative':negative},sources,'ordinary_negative_vector_observation')
 return co


def reconciliation_preflight(name,roster,folder):
 """Replay only the existing reconciliation assertions, preserving failures first.

 The original reconciler still runs unchanged after this check. No historical
 count or source result is promoted here. Fresh fitted vectors already exist in
 the dependency ledger before any source or held-value comparison below.
 """
 if name not in ('small_cert','quartic_cert'):return
 files={k:U.pin(roster[k]) for k in ('models','fit','holdouts')}
 documents={k:U.read(p['path']) for k,p in files.items()}
 model,fit,hold=(documents[k] for k in ('models','fit','holdouts'))
 identity={'phase':name};eq=lambda predicate,want,got,who=identity,refs=files:reconcile_equal(folder,name,predicate,who,want,got,refs)
 for label,doc in documents.items():eq(label+'_status','complete',doc.get('status'))
 if fit.get('candidates'):
  adverse_event(folder,name,'prior_fitted_candidates',identity,[],fit['candidates'],files,'ordinary_negative_vector_observation')
 for field in ('source_comparison_loaded','positive_holdouts_loaded'):eq('fit_'+field,False,fit.get(field))
 count=56 if name=='small_cert' else 10348
 for label,rows in (('models',model['records']),('fit',fit['records']),('holds',hold['counts'])):eq(label+'_record_count',count,len(rows))
 # Capture newly encountered fitted negatives before even loading source vectors.
 for i,row in enumerate(fit['records']):
  ident={'id':row.get('id'),'record_index':i,'boundary':row.get('original',row.get('original_boundary')),'rank':row.get('rank')}
  vector_observation(folder,name,ident,row,{**files,'fit_record':{'json_pointer':f'/records/{i}','record_sha256':U.sha(U.encoded(row))}},'fresh_fitted')
 source={}
 if name=='small_cert':
  for source_path in roster['source_vectors']:
   p=U.pin(source_path);doc=U.read(p['path']);eq('source_complete',True,doc.get('complete'),refs={'source':p})
   for i,row in enumerate(doc['records']):
    key=tuple(tuple(row[k]) for k in ('lambda','mu','nu'));ref={**p,'json_pointer':f'/records/{i}','record_sha256':U.sha(U.encoded(row))}
    who={'boundary':{k:row[k] for k in ('lambda','mu','nu')}}
    if key in source:adverse_event(folder,name,'duplicate_original_source',who,'unique literal source triple',row,{'source':ref})
    vector_observation(folder,name,who,row,{'source':ref},'original_source')
    source[key]=(row,ref)
  eq('source_record_count',56,len(source))
  for i,(m,f,h) in enumerate(zip(model['records'],fit['records'],hold['counts'])):
   who={'id':m['id'],'record_index':m['record_index'],'rank':m['rank'],'boundary':m['original']}
   refs={**files,'model_record':{'json_pointer':f'/records/{i}','record_sha256':U.sha(U.encoded(m))},
         'fit_record':{'json_pointer':f'/records/{i}','record_sha256':U.sha(U.encoded(f))},
         'hold_record':{'json_pointer':f'/counts/{i}','record_sha256':U.sha(U.encoded(h))}}
   eq('exact_fitted_identity',m['id'],f['id'],who,refs);eq('exact_held_identity',m['id'],h['id'],who,refs)
   eq('held_record_index',m['record_index'],h['record_index'],who,refs);eq('unused_positive_hold_nodes',[6,7],h['nodes'],who,refs)
   key=tuple(tuple(m['original'][k]) for k in ('lambda','mu','nu'))
   if key not in source:adverse_event(folder,name,'missing_original_source',who,'literal triple in selected source roster',None,refs)
   s,sref=source[key];refs={**refs,'original_source':sref};co=list(map(Fraction,f['coefficients']))
   expected=list(map(Fraction,s['coefficients']))+[Fraction(0)]*(len(co)-len(s['coefficients']))
   eq('entire_source_vector',list(map(str,expected)),list(map(str,co)),who,refs)
   for t,v in enumerate(s['values']):
    eq('source_scalar_at_grade',str(Fraction(v)),str(sum(c*t**j for j,c in enumerate(co))),{**who,'grade':t},refs)
   eq('held_value_count',2,len(h['counts']),who,refs)
   for t,v in zip(h['nodes'],h['counts']):
    eq('fresh_unused_hold',str(sum(c*t**j for j,c in enumerate(co))),str(Fraction(int(v))),{**who,'grade':t},refs)
 else:
  wanted=model['expected_ids'];eq('model_identity_roster_size',10348,len(wanted));eq('model_identity_roster_unique',len(wanted),len(set(wanted)))
  p=U.pin(roster['primary'])
  with Path(p['path']).open('rb') as stream:
   for line,raw in enumerate(stream,1):
    row=U.decode(raw);idx=row['id'];ref={**p,'line':line,'raw_record_sha256':U.sha(raw)}
    if idx in source:adverse_event(folder,name,'duplicate_original_source',{'id':idx},'unique literal source ID',row,{'source':ref})
    vector_observation(folder,name,{'id':idx},row,{'source':ref},'original_source')
    source[idx]=(row,ref)
  eq('source_literal_ids',sorted(wanted),sorted(source));eq('fitted_literal_ids',wanted,[r['id'] for r in fit['records']])
  holds={}
  for i,h in enumerate(hold['counts']):
   idx=int(h['id'])
   if idx in holds:adverse_event(folder,name,'duplicate_held_identity',{'id':idx},'unique held row',h,files)
   holds[idx]=(h,i)
  eq('held_literal_ids',sorted(wanted),sorted(holds));classes=set();preimages=[0,0];positive=[]
  for i,(m,row) in enumerate(zip(model['records'],fit['records'])):
   idx=row['id'];s,sref=source[idx];h,hi=holds[idx]
   who={'id':idx,'record_index':m['record_index'],'rank':row['rank'],'boundary':row['original_boundary']}
   refs={**files,'original_source':sref,'model_record':{'json_pointer':f'/records/{i}','record_sha256':U.sha(U.encoded(m))},
         'fit_record':{'json_pointer':f'/records/{i}','record_sha256':U.sha(U.encoded(row))},
         'hold_record':{'json_pointer':f'/counts/{hi}','record_sha256':U.sha(U.encoded(h))}}
   co=reconcile_quartic_row(folder,m,row,s,h,refs)
   classes.add(tuple(map(str,co)))
   for j,value in enumerate(row['preimages']):preimages[j]+=value
   positive.extend(c for j,c in enumerate(co) if j)
  eq('complete_vector_class_count',24,len(classes));eq('complete_preimage_populations',[6177,7153],preimages)
  eq('minimum_positive_nonconstant','1/24',str(min(positive)))


def reconcile_quartic_row(folder,model,row,source,hold,refs):
 """The exact unchanged per-record quartic predicates, with durable failures."""
 who={'id':row['id'],'record_index':model['record_index'],'rank':row['rank'],'boundary':row['original_boundary']}
 eq=lambda p,w,g,identity=who:reconcile_equal(folder,'quartic_cert',p,identity,w,g,refs)
 co=vector_observation(folder,'quartic_cert',who,row,refs,'fresh_fitted')
 expected_co=vector_observation(folder,'quartic_cert',who,source,refs,'original_source')
 eq('nonempty_fitted_state','nonempty',row['state']);eq('actual_degree',4,row['actual_degree'])
 eq('complete_quartic_vector_length',5,len(co));eq('strict_coefficient_positivity',True,all(c>0 for c in co))
 eq('literal_original_boundary',{k:source[k] for k in ('lambda','mu','nu')},row['original_boundary'])
 for field in ('rank','preimages'):eq('source_'+field,source[field],row[field])
 for field,value in (('degree_bound',4),('actual_degree',4),('determining_nodes',[0,1,2,3,4]),('unused_positive_holdouts',[5,6])):
  eq('source_'+field,value,source[field])
 eq('unused_positive_hold_nodes',[5,6],hold['nodes']);eq('held_record_index',model['record_index'],hold['record_index'])
 eq('held_dimension',4,hold['dimension']);eq('held_value_count',2,len(hold['counts']))
 for t,v in zip(hold['nodes'],hold['counts']):
  eq('fresh_unused_hold',str(sum(c*Fraction(t)**j for j,c in enumerate(co))),str(Fraction(int(v))),{**who,'grade':t})
 eq('entire_source_vector',list(map(str,expected_co)),list(map(str,co)))
 eq('entire_source_value_roster',source['values'],row['values']+list(map(int,hold['counts'])))
 return co


def durable_adverse(folder,step):
 """Read persisted adverse output even when no final result or exit is usable."""
 observations=[]
 if not folder.is_dir() or folder.is_symlink():return observations
 def walk(value,location='$'):
  if isinstance(value,dict):
   if value.get('status') in ('candidate_interrupt','HOLD_CANDIDATE','HOLD_ORDINARY_NEGATIVE','COUNT_MISMATCH','MISMATCH','FAIL','failed','mismatch') or value.get('candidates') or value.get('requires_owner_disposition') is True or any(value.get(k) for k in ('mismatches','bound_mismatches','missing_expected_identities','extra_expected_identities')):
    return [{'location':location,'record':value,'scope':value.get('scope','source-declared observation; not an accepted whole-LR counterexample')}]
   if str(value.get('error','')).startswith(('AssertionError:','ReconciliationMismatch:')):
    return [{'location':location,'record':value,'scope':'Unresolved mathematical assertion failure; no counterexample or missing identity is inferred'}]
   if step.get('kind') in ('small-fit','quartic-fit') and isinstance(value.get('coefficients'),list):
    try:
     if any(Fraction(c)<0 for c in value['coefficients']):return [{'location':location,'record':value,'scope':'fresh whole-chart fitted vector observation; original correspondence and receipt remain unaccepted'}]
    except (ValueError,TypeError,ZeroDivisionError):return [{'location':location,'record':value,'scope':'unreadable fitted vector observation'}]
   return [r for k,v in value.items() if isinstance(v,(dict,list)) for r in walk(v,location+'/'+k)]
  if isinstance(value,list):return [r for i,v in enumerate(value) for r in walk(v,location+'/'+str(i))]
  return []
 for path in sorted(folder.rglob('*')):
  named='candidate' in path.name or 'source-negative' in path.name or 'mismatch' in path.name or path.name=='ADVERSE-OBSERVATIONS.jsonl'
  if not (named or path.name in ('result.json','report.json','CHILD-RESULT.json','result.raw-vectors.jsonl','result.raw-counts.jsonl')):continue
  source=None
  try:
   source=U.pin(path)
   if path.suffix=='.jsonl':
    with path.open('rb') as stream:
     for line,raw in enumerate(stream,1):
      try:
       U.need(raw.endswith(b'\n'),'Incomplete durable observation line');value=U.decode(raw);rows=walk(value,f'line:{line}')
       if named and not rows:rows=[{'location':f'line:{line}','record':value,'scope':'adverse-labelled observation; receipt and mathematical scope remain unaccepted'}]
      except (ValueError,UnicodeError):rows=[{'location':f'line:{line}','record_sha256':U.sha(raw),'scope':'unreadable durable observation; no mathematical verdict'}]
      observations += [{'artifact':source,**r} for r in rows]
   else:
    value=U.read(path);rows=walk(value)
    if named and not rows:rows=[{'location':'$','record':value,'scope':'candidate-labelled observation; receipt and mathematical scope remain unaccepted'}]
    observations += [{'artifact':source,**r} for r in rows]
  except (OSError,ValueError,UnicodeError) as error:
   observations.append({'path':str(path),'artifact':source,'error':str(error),'scope':'unreadable adverse/result artifact; no mathematical verdict'})
 return observations

def graph(metric_chunk=250,count_chunk=512):
 steps=[]
 def add(name,kind,needs=(),**kw):steps.append({'id':name,'kind':kind,'needs':list(needs),**kw});return name
 for name in CPP:add('build-'+name,'build',program=name)
 masks=[add(f'masks-{n}','masks',rank=n) for n in (6,7)]
 add('inputs','inputs',masks)
 for n in (6,7):add(f'census-{n}','census',['inputs','build-census'],rank=n)
 add('maps','maps',['build-maps'])
 add('types','types')
 metrics=[add(f'metrics-{i:04d}','metrics',['types'],start=i,stop=min(i+metric_chunk,3937)) for i in range(0,3937,metric_chunk)]
 add('metric-aggregate','metric-aggregate',['types',*metrics])
 add('metric-bind','metric-bind',[*masks,'metric-aggregate'])
 add('small-charts','small-charts',masks)
 add('small-determine','count',['small-charts','build-counter'],family='small',nodes=list(range(6)),start=0,stop=56)
 add('small-fit','small-fit',['small-charts','small-determine'])
 add('small-hold','count',['small-fit','small-charts','build-counter'],family='small',nodes=[6,7],start=0,stop=56)
 add('small-cert','small-cert',['small-charts','small-fit','small-hold'])
 add('quartic-charts','quartic-charts',masks)
 fits=[add(f'quartic-determine-{i:05d}','count',['quartic-charts','build-counter'],family='quartic',nodes=list(range(5)),
           start=i,stop=min(i+count_chunk,10348)) for i in range(0,10348,count_chunk)]
 add('quartic-fit','quartic-fit',['quartic-charts',*fits])
 holds=[add(f'quartic-hold-{i:05d}','count',['quartic-fit','quartic-charts','build-counter'],family='quartic',nodes=[5,6],
            start=i,stop=min(i+count_chunk,10348)) for i in range(0,10348,count_chunk)]
 add('quartic-holds','count-join',holds,family='quartic',nodes=[5,6])
 add('quartic-cert','quartic-cert',['quartic-charts','quartic-fit','quartic-holds'])
 add('cover','cover',['census-6','census-7','maps','inputs','metric-bind','small-cert','quartic-cert'])
 add('small-join','small-join',['small-cert','cover'])
 add('residual-join','residual-join',['cover','small-join'])
 return steps

def selected(steps,lane):
 ends={'masks':['masks-6','masks-7'],'inputs':['inputs'],'census':['census-6','census-7'],'maps':['maps'],
       'metrics':['metric-bind'],'small':['small-cert'],'quartics':['quartic-cert'],'cover':['residual-join'],'all':['residual-join']}
 by={s['id']:s for s in steps};wanted=set()
 def visit(name):
  if name not in wanted:
   wanted.add(name)
   for dep in by[name]['needs']:visit(dep)
 for name in ends[lane]:visit(name)
 return [s for s in steps if s['id'] in wanted]

def role_names(step):
 k=step['kind'];n=step.get('rank')
 if k=='masks':return [f'mask{n}']
 if k=='inputs':return ['horn_inventory',*[x+str(n) for n in (6,7) for x in ('cover_source','score_source','horn_source')]]
 if k=='census':return ['horn_source6','horn_source7',f'BOX{n}-RESIDUAL.tsv','census_expected']
 if k=='maps':return ['map_expected',*[x for x in ('BOX6-RESIDUAL.tsv','BOX7-RESIDUAL.tsv','CANON6-KEYS.tsv','CANON7-KEYS.tsv',
                                                    'CANON6-MAP.tsv','CANON7-MAP.tsv','GLOBAL-MAP6.txt','GLOBAL-MAP7.txt','GLOBAL-KEYS.tsv')]]
 if k in ('types','metrics','metric-aggregate'):return ['cone_roster',*['cone_'+x for x in ('atlas6','atlas7','primary_types','repaired_types','metric0','metric1500','metric3000','reconciliation')]]
 if k=='metric-bind':return ['mask_words','cone_roster','cone_atlas6','cone_atlas7']
 if k=='small-charts':return ['small_roster']
 if k=='small-cert':return ['small_vectors0','small_vectors1']
 if k=='quartic-charts':return ['quartic_cases0','quartic_cases1']
 if k=='quartic-cert':return ['quartic_primary']
 if k=='cover':return ['GLOBAL-KEYS.tsv','source_new_keys']
 if k=='small-join':return ['BOX6-RESIDUAL.tsv','BOX7-RESIDUAL.tsv','GLOBAL-KEYS.tsv']
 return []

def execution_class(step):
 if step['kind']=='census':return 'fresh_original_identity_enumeration'
 if step['kind']=='count':return 'fresh_whole_chart_scalar_counts'
 if step['kind']=='maps':return 'fresh_exact_original_local_global_maps'
 if step['kind']=='build':return 'fresh_toolchain_build'
 return 'finite_certificate_or_exact_identity_replay'

def call_external(command,folder):
 started=time.monotonic()
 with (folder/'program.stdout.txt').open('xb') as out,(folder/'program.stderr.txt').open('xb') as err:
  process=subprocess.Popen(command,stdout=out,stderr=err)
  code=process.wait()
 record={'command':command,'pid':process.pid,'returncode':code,'elapsed_seconds':time.monotonic()-started}
 U.save(folder/'PROGRAM-EXIT.json',record)
 U.need(code==0,'Owned compiler/program returned nonzero: '+str(code))

def box(name,roster,folder):
 path=folder/'ROSTER.json';U.save(path,roster)
 reconciliation_preflight(name,roster,folder)
 result=U.module(name).run(SimpleNamespace(roster=path,output=folder/'result.json'))
 U.need(result in (None,0),'Mathematical checker returned nonzero')

def counter_rows(model,documents,nodes,first=0,last=None):
 expected=model['records'];last=len(expected) if last is None else last
 U.need(0<=first<last<=len(expected),'Invalid exact count interval')
 rows=[];seen=set()
 for document in documents:
  U.need(document.get('status')=='complete','Incomplete/refused count result')
  for row in document['counts']:
   i=row['record_index'];U.need(type(i) is int and first<=i<last and i not in seen,'Extra/duplicated count record index')
   m=expected[i];identity=str(m['id'])
   U.need(str(row['id'])==identity and row['nodes']==nodes,'Count result differs from literal source ID/node roster')
   d=m.get('degree_bound',m['chart']['dimension_bound'])
   U.need(row['dimension']==d and len(row['counts'])==len(nodes),'Wrong complete chart dimension/count length')
   for value in row['counts']:
    U.need(type(value) in (int,str) and str(int(value))==str(value) and int(value)>=0,'Noninteger or negative count scalar')
   seen.add(i);rows.append(row)
 U.need(seen==set(range(first,last)),'Missing literal count records')
 return sorted(rows,key=lambda row:row['record_index'])

# Format adapter only. The original counter, models, fitters, reconciliations
# and their mathematical predicates are unchanged.
COUNTER_ENVELOPE='portable-f025-counter-jsonl-envelope-v1'
COUNTER_RAW_NAME='result.raw-counts.jsonl'
COUNTER_ROW_FIELDS={'schema_version','status','id','record_index','dimension','input_rows',
 'normalized_rows','native_calls','nodes','counts','cache_hit','cache_source_record_index',
 'fm_pairs','peak_projected_rows','search_nodes','final_intervals'}
COUNTER_LINE_LIMIT=1024*1024

class CounterOutputRefusal(U.Invalid):
 """Counter transport/completion refusal, not a mathematical sign mismatch."""

def counter_command(step,charts,binary,limits,raw_path):
 U.need(set(limits)=={'max_fm_pairs','max_projected_rows','max_search_nodes'} and
        all(type(v) is int and v>=0 for v in limits.values()) and limits['max_projected_rows']==100000,
        'Invalid exact counter work-limit binding')
 return [binary['path'],'--input',charts['path'],'--start',str(step['start']),'--stop',str(step['stop']),
         '--nodes',','.join(map(str,step['nodes'])),'--max-fm-pairs',str(limits['max_fm_pairs']),
         '--max-projected-rows',str(limits['max_projected_rows']),
         '--max-search-nodes',str(limits['max_search_nodes']),'--output',str(raw_path)]

def counter_refusal(folder,step,error,sources):
 event={'schema':'portable-f025-adverse-observation-v1','phase':'count',
        'kind':'counter_output_format_or_completion_refusal','predicate':'complete_raw_jsonl_and_exact_envelope',
        'identity':{k:step.get(k) for k in ('id','family','start','stop','nodes')},
        'expected':'Every complete literal schema/ID/index/dimension/node/count row and unchanged model/program bindings',
        'observed':{'error_type':type(error).__name__,'error':str(error)},'sources':sources,
        'adapter':U.pin(__file__),'requires_owner_disposition':True,'authenticated_scientific_result':False,
        'scope':'Format/completion/source-binding refusal; not an ordinary-negative observation or established scalar mismatch. Raw output and prior completed rows remain unchanged.'}
 with (folder/'ADVERSE-OBSERVATIONS.jsonl').open('ab') as stream:
  stream.write(U.encoded(event)+b'\n');stream.flush();os.fsync(stream.fileno())
 raise CounterOutputRefusal(str(error))

def counter_request_roster(model,step):
 U.need(type(model) is dict and model.get('status')=='complete' and type(model.get('records')) is list,
        'Counter requires a complete source model document')
 first,last,nodes=step['start'],step['stop'],step['nodes']
 U.need(type(first) is int and type(last) is int and 0<=first<last<=len(model['records']),
        'Invalid exact counter source slice')
 U.need(type(nodes) is list and 1<=len(nodes)<=256 and all(type(t) is int and t>=0 for t in nodes)
        and len(nodes)==len(set(nodes)),'Invalid literal counter node roster')
 expected=[]
 for index in range(first,last):
  m=model['records'][index]
  U.need(type(m) is dict and type(m.get('record_index')) is int and m['record_index']==index,
         'Source model record index differs from its literal position')
  U.need(type(m.get('id')) in (str,int) and str(m['id']), 'Source model lacks a literal ID')
  U.need(type(m.get('chart')) is dict and type(m['chart'].get('dimension_bound')) is int,
         'Source model lacks its complete chart dimension')
  dimension=m.get('degree_bound',m['chart']['dimension_bound'])
  U.need(type(dimension) is int and 0<=dimension<=5 and dimension==m['chart']['dimension_bound'],
         'Source dimension outside or inconsistent with the complete counter chart')
  expected.append({'record_index':index,'id':str(m['id']),'dimension':dimension,
                   'model_record_sha256':U.sha(U.encoded(m))})
 U.need(len({r['id'] for r in expected})==len(expected),'Duplicate literal source-model ID')
 return expected

def counter_raw_schema(row):
 U.need(type(row) is dict and set(row)==COUNTER_ROW_FIELDS,'Malformed chart_counter_v3 row schema')
 U.need(type(row['schema_version']) is int and row['schema_version']==1 and row['status']=='complete',
        'Counter raw row is not schema-version-one complete output')
 U.need(type(row['id']) is str and 1<=len(row['id'])<=128 and
        all(33<=ord(c)<=126 for c in row['id']),'Invalid literal raw counter ID')
 for key in ('record_index','dimension','input_rows','normalized_rows','native_calls',
             'cache_source_record_index','fm_pairs','peak_projected_rows'):
  U.need(type(row[key]) is int and row[key]>=0,'Invalid integer counter field: '+key)
 U.need(row['dimension']<=5 and row['native_calls']==0,'Invalid raw counter dimension/native-call field')
 U.need(type(row['cache_hit']) is bool,'Invalid raw counter cache flag')
 U.need(type(row['nodes']) is list and 1<=len(row['nodes'])<=256 and
        all(type(t) is int and t>=0 for t in row['nodes']) and
        len(row['nodes'])==len(set(row['nodes'])),'Invalid raw counter node list')
 U.need(type(row['counts']) is list and len(row['counts'])==len(row['nodes']), 'Incomplete raw scalar count list')
 for count in row['counts']:
  U.need(type(count) is str and count and count.isascii() and count.isdecimal() and
         (count=='0' or not count.startswith('0')),'Counter count is not a canonical nonnegative decimal string')
 for key in ('search_nodes','final_intervals'):
  U.need(type(row[key]) is list and len(row[key])==len(row['nodes']) and
         all(type(v) is int and v>=0 for v in row[key]),'Invalid raw counter work array: '+key)

def read_counter_jsonl(raw_pin,model,step):
 """Every raw byte remains on disk before any model/source comparison."""
 U.check(raw_pin);rows=[];references=[]
 with Path(raw_pin['path']).open('rb') as stream:
  line=0
  while True:
   raw=stream.readline(COUNTER_LINE_LIMIT+1)
   if not raw:break
   line+=1
   U.need(len(raw)<=COUNTER_LINE_LIMIT and raw.endswith(b'\n'),
          'Incomplete/oversized raw counter JSONL line: '+str(line))
   row=U.decode(raw)
   references.append({'line':line,'bytes':len(raw),'sha256':U.sha(raw),
                      'record_index':row.get('record_index') if type(row) is dict else None})
   counter_raw_schema(row)
   source=row['cache_source_record_index'];index=row['record_index']
   U.need((step['start']<=source<index) if row['cache_hit'] else source==index,
          'Raw cache provenance differs from the exact counter slice/order')
   rows.append(row)
 U.check(raw_pin)
 counter_request_roster(model,step)
 checked=counter_rows(model,[{'status':'complete','counts':rows}],step['nodes'],step['start'],step['stop'])
 return checked,references

def counter_bound_document(ref):
 U.check(ref);raw=Path(ref['path']).read_bytes()
 U.need(len(raw)==ref['bytes'] and U.sha(raw)==ref['sha256'],'Changed document while reading counter binding')
 result=U.decode(raw);U.check(ref);return result

def counter_output_envelope(folder,step,request):
 """Validate complete JSONL and exact input/program bindings, then emit JSON."""
 U.need(not (folder/'result.json').exists(),'Counter envelope destination is not fresh')
 U.need(request.get('schema')=='portable-f025-counter-request-v1','Wrong counter request schema')
 for ref in (request['model'],request['charts'],request['counter_build'],
             request['program']['source'],request['program']['binary']):U.check(ref)
 model=counter_bound_document(request['model']);build=counter_bound_document(request['counter_build'])
 U.need(build.get('status')=='complete' and build.get('program')=='counter','Incomplete/wrong counter build source')
 U.need(model['charts_file']==request['charts'] and
        {k:build[k] for k in ('source','binary')}==request['program'],'Counter model/build source binding differs')
 expected=counter_request_roster(model,step)
 U.need(request['expected_records']==expected and request['query']=={k:step[k] for k in ('family','start','stop','nodes')},
        'Counter request differs from the literal source slice/node roster')
 U.need(request['command']==counter_command(step,request['charts'],request['program']['binary'],request['limits'],folder/COUNTER_RAW_NAME),
        'Counter command does not count the exact bound input/node/slice')
 raw_pin=U.pin(folder/COUNTER_RAW_NAME)
 rows,raw_records=read_counter_jsonl(raw_pin,model,step)
 exit_pin=U.pin(folder/'PROGRAM-EXIT.json');exit_doc=counter_bound_document(exit_pin)
 U.need(type(exit_doc.get('returncode')) is int and exit_doc['returncode']==0 and
        type(exit_doc.get('pid')) is int and exit_doc['pid']>0 and exit_doc['command']==request['command'],
        'Counter program did not exit zero for the exact frozen command')
 for ref in (request['model'],request['charts'],request['counter_build'],
             request['program']['source'],request['program']['binary'],raw_pin,exit_pin):U.check(ref)
 result={'schema':COUNTER_ENVELOPE,'status':'complete','counts':rows,
         'raw_output':raw_pin,'raw_records':raw_records,'model':request['model'],'charts':request['charts'],
         'counter_build':request['counter_build'],'program':request['program'],'program_exit':exit_pin,
         'request':U.pin(folder/'COUNTER-REQUEST.json'),'query':request['query'],'expected_records':expected,
         'limits':request['limits'],
         'scope':'Complete fresh scalar rows for this literal chart slice only. Raw JSONL is retained before comparisons; original mathematical and whole-box premises remain separate.'}
 U.need(counter_bound_document(result['request'])==request,'Counter request bytes changed')
 U.save(folder/'result.json',result)
 return result

def run_counter(step,recipe,folder,dependencies):
 sources={};raw_path=folder/COUNTER_RAW_NAME
 try:
  U.need(not raw_path.exists() and not (folder/'result.json').exists(),'Raw/envelope counter outputs must be fresh')
  model_ref=dependencies[step['family']+'-charts']['result'];build_ref=dependencies['build-counter']['result']
  sources={'model':model_ref,'counter_build':build_ref}
  model=counter_bound_document(model_ref);build=counter_bound_document(build_ref)
  charts=model['charts_file'];U.check(charts)
  U.need(build.get('status')=='complete' and build.get('program')=='counter','Wrong counter build dependency')
  U.need(build['source']==U.pin(U.HERE/'originals'/CPP['counter']),'Counter source differs from preserved C++')
  U.check(build['binary'])
  limits={'max_fm_pairs':recipe['max_fm_pairs'],'max_projected_rows':100000,'max_search_nodes':recipe['max_search_nodes']}
  command=counter_command(step,charts,build['binary'],limits,raw_path)
  request={'schema':'portable-f025-counter-request-v1','query':{k:step[k] for k in ('family','start','stop','nodes')},
           'model':model_ref,'charts':charts,'counter_build':build_ref,
           'program':{k:build[k] for k in ('source','binary')},'command':command,
           'limits':limits,
           'expected_records':counter_request_roster(model,step)}
  sources={k:request[k] for k in ('model','charts','counter_build','program')}
  U.save(folder/'COUNTER-REQUEST.json',request)
  call_external(command,folder)
  return counter_output_envelope(folder,step,request)
 except (OSError,ValueError,KeyError,TypeError,UnicodeError) as error:
  for name in (COUNTER_RAW_NAME,'COUNTER-REQUEST.json','PROGRAM-EXIT.json','program.stdout.txt','program.stderr.txt'):
   try:
    if (folder/name).is_file():sources[name]=U.pin(folder/name)
   except (OSError,ValueError) as pin_error:sources[name]={'pin_error':str(pin_error)}
  counter_refusal(folder,step,error,sources)

def validate_counter_envelope(step,result,dependencies,recipe):
 U.need(result.get('schema')==COUNTER_ENVELOPE,'Missing typed counter JSONL envelope')
 model_ref=dependencies[step['family']+'-charts']['result'];model=counter_bound_document(model_ref)
 build_ref=dependencies['build-counter']['result'];build=counter_bound_document(build_ref)
 U.need(result['model']==model_ref and result['charts']==model['charts_file'] and result['counter_build']==build_ref
        and result['program']=={k:build[k] for k in ('source','binary')},'Stale counter envelope model/program binding')
 request=counter_bound_document(result['request'])
 U.need(request['schema']=='portable-f025-counter-request-v1' and
        request['query']==result['query']=={k:step[k] for k in ('family','start','stop','nodes')}
        and request['expected_records']==result['expected_records']==counter_request_roster(model,step),
        'Counter envelope differs from exact request/source identities')
 for key in ('model','charts','counter_build','program'):U.need(request[key]==result[key],'Request/envelope source differs: '+key)
 raw_path=Path(result['request']['path']).parent/COUNTER_RAW_NAME
 U.need(result['raw_output']['path']==str(raw_path),'Counter envelope references a different raw filename')
 limits={'max_fm_pairs':recipe['max_fm_pairs'],'max_projected_rows':100000,'max_search_nodes':recipe['max_search_nodes']}
 U.need(request['limits']==result['limits']==limits and
        request['command']==counter_command(step,result['charts'],result['program']['binary'],limits,raw_path),
        'Counter command/limits differ from the actual recipe or chart input')
 rows,refs=read_counter_jsonl(result['raw_output'],model,step)
 U.need(rows==result['counts'] and refs==result['raw_records'],'Envelope does not preserve every exact raw counter row')
 exit_doc=counter_bound_document(result['program_exit'])
 U.need(type(exit_doc.get('returncode')) is int and exit_doc['returncode']==0 and
        type(exit_doc.get('pid')) is int and exit_doc['pid']>0 and exit_doc['command']==request['command'],
        'Counter envelope lacks its actual zero-exit command binding')
 for ref in (result['model'],result['charts'],result['counter_build'],result['program']['source'],result['program']['binary']):U.check(ref)

def run_step(recipe,step,folder,dependencies):
 I=U.Inputs(recipe['data_root'],recipe['manifest']['path'],recipe['manifest']['sha256'])
 role=lambda name:str(I.role(name))
 path=lambda name:dependencies[name]['result']['path']
 doc=lambda name:U.read(path(name))
 k=step['kind'];out=folder/'result.json'
 if k=='build':
  source=U.HERE/'originals'/CPP[step['program']];binary=folder/'program'
  command=[recipe['compiler']['path'],'-std=c++17','-O2','-Wall','-Wextra',str(source),'-o',str(binary)]
  call_external(command,folder);U.save(out,{'status':'complete','program':step['program'],'source':U.pin(source),'binary':U.pin(binary),'command':command})
 elif k=='masks':
  n=step['rank'];box('masks',{'rank':n,'start':0,'stop':1<<(3*(n-1)),'mask_source':role(f'mask{n}')},folder)
 elif k=='inputs':
  box('inputs',{'accepted_horn_inventory':role('horn_inventory'),'ranks':[
   {'rank':n,'verified_masks':path(f'masks-{n}'),'cover_source':role(f'cover_source{n}'),
    'score_source':role(f'score_source{n}'),'horn_source':role(f'horn_source{n}'),'score_output':str(folder/f'scores{n}.txt')} for n in (6,7)]},folder)
 elif k=='census':
  n=step['rank'];scores={x['rank']:x['score_output'] for x in doc('inputs')['strata']}
  command=[doc('build-census')['binary']['path'],'--rank',str(n),'--max-area','30','--scores6',scores[6],'--scores7',scores[7],
           '--horn6',role('horn_source6'),'--horn7',role('horn_source7'),'--expected-residual',role(f'BOX{n}-RESIDUAL.tsv'),'--output',str(out)]
  call_external(command,folder)
 elif k=='maps':
  files=[I.role(n) for n in role_names(step) if n!='map_expected'];root=files[0].parent
  U.need(all(p.parent==root and p.name==n for p,n in zip(files,[n for n in role_names(step) if n!='map_expected'])),'P08 map files require one exact declared sibling directory')
  command=[doc('build-maps')['binary']['path'],'--input',str(root),'--output',str(folder/'maps'),
           '--expected',role('map_expected'),'--binding',recipe['manifest']['sha256'],'--mode','full']
  call_external(command,folder)
  U.save(out,U.read(folder/'maps/report.json'))
 elif k in ('types','metrics','metric-aggregate'):
  # One fresh input roster is shared across every type/metric launch. Its
  # original expected identities and normals are preserved verbatim.
  for name in role_names(step):I.role(name)
  args=SimpleNamespace(roster=recipe['cone_roster']['path'],mode='aggregate' if k=='metric-aggregate' else k,
       output=str(out),triples_output=str(folder/'triples.jsonl') if k=='metrics' else None,
       type_certificate=path('types') if k=='metrics' else None,type_sha256=dependencies['types']['result']['sha256'] if k=='metrics' else None,
       begin=step.get('start'),end=step.get('stop'),results_roster=None)
  if k=='metric-aggregate':
   roster={'type_certificate':dependencies['types']['result'],'metric_batches':[
           {'job':name,**dependencies[name]['result']} for name in step['needs'] if name!='types']}
   args.results_roster=str(folder/'RESULTS-ROSTER.json');U.save(args.results_roster,roster)
  code=U.module('cones').run(args);U.need(code==0,'Cone checker did not complete')
 elif k=='metric-bind':
  box('metric_bind',{'metric_aggregate':path('metric-aggregate'),'metric_expected':recipe['cone_roster']['path'],
      'mask_words':role('mask_words'),'ranks':[{'rank':n,'atlases':role(f'cone_atlas{n}'),'verified_masks':path(f'masks-{n}'),
      'admitted_output':str(folder/f'admitted{n}.txt')} for n in (6,7)]},folder)
 elif k=='small-charts':
  box('small_charts',{'small_roster':role('small_roster'),'verified_masks':[path('masks-6'),path('masks-7')],
                     'charts_output':str(folder/'charts.txt')},folder)
 elif k=='quartic-charts':
  box('quartic_charts',{'verified_masks':[{'path':path(f'masks-{n}')} for n in (6,7)],
       'exceptions':[{'path':role('quartic_cases0'),'expected_count':4670},{'path':role('quartic_cases1'),'expected_count':5678}],
       'charts_output':str(folder/'charts.txt')},folder)
 elif k=='count':
  run_counter(step,recipe,folder,dependencies)
 elif k=='count-join':
  # The count producers already checked model identity. The final reconciliation
  # independently checks the complete model/source/node membership again.
  rows=[];seen=set()
  for name in step['needs']:
   d=doc(name);U.need(d['status']=='complete','Partial scalar result cannot be joined')
   for row in d['counts']:
    U.need(row['record_index'] not in seen and row['nodes']==step['nodes'],'Duplicate/stale held count')
    seen.add(row['record_index']);rows.append(row)
  U.need(seen==set(range(10348)),'Missing exact quartic held record indices')
  U.save(out,{'status':'complete','counts':sorted(rows,key=lambda r:r['record_index']),'fresh_source_results':[dependencies[n]['result'] for n in step['needs']]})
 elif k=='small-fit':box('small_fit',{'models':path('small-charts'),'counts':path('small-determine')},folder)
 elif k=='small-cert':box('small_cert',{'models':path('small-charts'),'fit':path('small-fit'),'holdouts':path('small-hold'),
                                      'source_vectors':[role('small_vectors0'),role('small_vectors1')]},folder)
 elif k=='quartic-fit':
  box('quartic_fit',{'models':path('quartic-charts'),'expected_ids':doc('quartic-charts')['expected_ids'],
                    'determining_results':[path(n) for n in step['needs'] if n!='quartic-charts']},folder)
 elif k=='quartic-cert':box('quartic_cert',{'models':path('quartic-charts'),'fit':path('quartic-fit'),
                           'holdouts':path('quartic-holds'),'primary':role('quartic_primary')},folder)
 elif k=='cover':
  scores={x['rank']:x['score_output'] for x in doc('inputs')['strata']}
  admitted={x['rank']:x['admitted_bitmap']['path'] for x in doc('metric-bind')['strata']}
  roster={'census6':path('census-6'),'census7':path('census-7'),'map_report':path('maps'),
      'small_certificate':path('small-cert'),'quartic_certificate':path('quartic-cert'),'metric_binding':path('metric-bind'),
      'global_keys':role('GLOBAL-KEYS.tsv'),'source_new_keys':role('source_new_keys'),
      'residual_output':str(folder/'residual.tsv'),'pricing_panel_output':str(folder/'pricing-panel.json')}
  for n in (6,7):roster.update({f'scores{n}':scores[n],f'admitted{n}':admitted[n]})
  box('cover',roster,folder)
 elif k=='small-join':box('small_join',{'certificate':path('small-cert'),'cover':path('cover'),'original6':role('BOX6-RESIDUAL.tsv'),
                                    'original7':role('BOX7-RESIDUAL.tsv'),'global':role('GLOBAL-KEYS.tsv')},folder)
 else:
  U.need(k=='residual-join','Unknown replay phase')
  residual_join(I,doc('cover'),out)
 I.after()
 return list(I.used.values())

def residual_join(I,cover,output):
 manifest_name=U.BASE+'/export-residual/manifest.json';manifest=U.read(I.path(manifest_name))
 columns=['id','rank','lambda','mu','nu','original_rank6_preimages','original_rank7_preimages','coordinate_bound']
 U.need(manifest['schema']=='f025-residual-portable/v1' and manifest['columns']==columns and len(manifest['shards'])==16,'Wrong literal residual export manifest')
 U.check(cover['residual']);seen=set();total=0;weights=0;bindings=[];last=0
 with Path(cover['residual']['path']).open() as fresh:
  U.need(next(fresh).rstrip('\n')=='\t'.join(columns),'Wrong fresh residual header')
  for shard in manifest['shards']:
   name=U.relative(shard['name']);U.need(name not in seen,'Duplicate residual shard');seen.add(name)
   path=I.path(U.BASE+'/export-residual/'+name);actual=U.pin(path)
   U.need(actual['bytes']==shard['compressed_bytes'] and actual['sha256']==shard['compressed_sha256'],'Export shard compressed identity changed')
   import hashlib
   h=hashlib.sha256();size=0;ids=[]
   with gzip.open(path,'rb') as stream:
    for raw in stream:
     h.update(raw);size+=len(raw);record=U.decode(raw)
     text=fresh.readline();U.need(text,'Export has an extra source identity')
     fields=text.rstrip('\n').split('\t');U.need(len(fields)==8,'Malformed fresh original residual')
     expected=[int(fields[0]),int(fields[1]),*[list(map(int,x.split(','))) for x in fields[2:5]],*map(int,fields[5:])]
     exact_residual_record(record,expected,last)
     last=record[0];ids.append(last);total+=1;weights+=record[5]+record[6]
   U.need(len(ids)==shard['records'] and ids[0]==shard['first_id'] and ids[-1]==shard['last_id']
          and size==shard['expanded_bytes'] and h.hexdigest()==shard['expanded_sha256'],'Incomplete/changed expanded shard roster')
   bindings.append({'source':actual,'records':len(ids),'first_id':ids[0],'last_id':ids[-1]})
  U.need(not fresh.readline(),'Fresh residual has omitted export identities')
 U.need(total==3936015 and weights==4360228,'Final original/preimage populations differ')
 U.save(output,{'status':'complete','exact_eight_column_records_compared':total,'original_preimage_weight':weights,
                'fresh_residual':cover['residual'],'export_manifest':U.pin(I.path(manifest_name)),'shards':bindings,
                'scope':'Every literal exported initial residual identity equals the freshly derived F025 residual; later terminal closure remains separate.'})

def exact_residual_record(record,expected,last):
 U.need(type(record) is list and len(record)==8 and
        all(type(record[k]) is int for k in (0,1,5,6,7)) and
        all(type(record[k]) is list and all(type(x) is int for x in record[k]) for k in (2,3,4)),
        'Residual has noninteger or malformed identity fields')
 U.need(record==expected and record[0]>last,'Residual identity, full triple, weights, bound or order differs')

def validate(step,result,dependencies,recipe):
 k=step['kind'];U.need(result.get('status')==('PASS' if k=='maps' else 'complete'),'Partial/failed/noncomplete mathematical result')
 if k=='masks':
  n=step['rank'];U.need(result['rank']==n and [r['mask'] for r in result['records']]==list(range(1<<(3*(n-1)))),'Incomplete mask identity roster')
 elif k=='census':
  n=step['rank'];U.need(result['rank']==n and result['max_area']==30 and result['enumeration_performed'] is True
       and result['residual_exact_match'] is True and not any(result[x] for x in ('missing_expected_identities','extra_expected_identities','bound_mismatches')),
       'Census is validation-only, partial or mismatched')
  expected={6:(252489578,1615508),7:(398740124,3728012)}[n]
  U.need(result['totals']['total']==expected[0] and result['matched_identities']==result['expected_rows']==expected[1]
         and [r['area'] for r in result['per_area']]==list(range(2,31)),'Wrong full domain or exact residual comparison population')
 elif k=='maps':U.need(result['mode']=='full' and result['source_binding_supplied_by_caller']==recipe['manifest']['sha256']
       and result['original6_transformations_verified']==1615508 and result['original7_transformations_verified']==3728012
       and result['global_keys']==4747974,'Partial/stale original/local/global map proof')
 elif k in ('types','metrics','metric-aggregate'):
  U.need(result['expected_ids']==result['completed_ids'] and len(set(result['completed_ids']))==len(result['completed_ids']), 'Incomplete/duplicate cone identity roster')
 elif k=='count':
  validate_counter_envelope(step,result,dependencies,recipe)
  model=U.read(dependencies[step['family']+'-charts']['result']['path'])
  counter_rows(model,[result],step['nodes'],step['start'],step['stop'])
 elif k=='small-cert':
  rows=result['records'];U.need(len(rows)==56 and len({r['id'] for r in rows})==56 and all(len(r['coefficients'])==6 for r in rows),'Incomplete small full vectors')
 elif k=='quartic-cert':
  rows=result['records'];U.need(len(rows)==10348 and [r['id'] for r in rows]==result['expected_ids'] and len(set(result['expected_ids']))==10348
       and all(len(r['coefficients'])==5 and all(Fraction(v)>0 for v in r['coefficients']) for r in rows),'Incomplete/invalid quartic full vectors')
 elif k=='small-join':U.need(len(result['records'])==56 and result['small_original_preimages']==1082,'Missing small-certificate exact population join')
