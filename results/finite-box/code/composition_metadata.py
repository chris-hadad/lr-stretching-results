#!/usr/bin/env python3
"""Source-pinned metadata-only launcher over unchanged portable core sources.

Only composition aggregate acceptance/final is supported. All other operations
continue through the original launcher. The invocation records the original
sources and each exact function adaptation; it never rewrites old receipts.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

RUNNER_SHA='de2ae53528ea1819a5e8a41d5d4f5f811b377ce6155b40f2dc1e776485d2f2a7'
COMPOSITION_SHA='9e3f4bfac1ca9f57e4087ec7a37d06bdb4000d988312bf152a0ac08721cfc9c3'
CHECKER='verify_box_composition.py'
SCHEMA='portable-composition-metadata-invocation-v1'


def need(ok,message):
    if not ok:raise ValueError(message)


def load(path,expected,name):
    path=Path(path).absolute()
    need(not any(p.is_symlink() for p in (path,*path.parents)), 'Symlink source refused')
    path=path.resolve();raw=path.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==expected,'Wrong exact original source: '+str(path))
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    exec(compile(raw,str(path),'exec'),module.__dict__)
    need(path.read_bytes()==raw,'Original source changed while loading')
    return module


def function(module,name,edits,extra):
    raw=Path(module.__file__).read_bytes()
    expected=RUNNER_SHA if Path(module.__file__).name=='portable_run.py' else COMPOSITION_SHA
    need(hashlib.sha256(raw).hexdigest()==expected,'Original source changed before adaptation')
    nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name==name]
    need(len(nodes)==1,'Missing/duplicate exact source function')
    original=ast.get_source_segment(raw.decode(),nodes[0]);adapted=original
    for before,after in edits:
        need(adapted.count(before)==1,'Exact function adaptation site changed: '+name)
        adapted=adapted.replace(before,after,1)
    inverse=adapted
    for before,after in reversed(edits):inverse=inverse.replace(after,before,1)
    need(inverse==original,'Unexpected function predicate changes')
    namespace=dict(vars(module));namespace.update(extra)
    exec(compile(adapted,str(Path(__file__).resolve())+'::'+name,'exec'),namespace)
    return namespace[name],{'original_source':{'path':str(Path(module.__file__).resolve()),'bytes':len(raw),'sha256':expected},
        'function':name,'original_function_sha256':hashlib.sha256(original.encode()).hexdigest(),
        'executed_function_sha256':hashlib.sha256(adapted.encode()).hexdigest(),
        'exact_replacements':[{'before':a,'after':b} for a,b in edits]}


def validate_words(U,checker,words,timeout):
    need(checker==CHECKER,'Metadata launcher cannot invoke another checker')
    command,options,_,help_only=U.parse_checker_args(checker,words)
    need(command=='aggregate' and not help_only and options.get('--phase') in (['acceptance'],['final']),
         'Metadata launcher supports only acceptance/final aggregate phases')
    budget=options.get('--budget-seconds',[])
    need(len(budget)==1 and budget[0].isdigit() and str(int(budget[0]))==budget[0] and 1<=int(budget[0])<=600,
         'Explicit metadata budget must be an integer in 1..600')
    need(type(timeout) in (int,float) and math.isfinite(timeout) and int(budget[0])<timeout<=660,
         'Metadata child timeout must exceed its budget and be at most 660')
    return options['--phase'][0]


def build(core):
    core=Path(core).absolute();need(not any(p.is_symlink() for p in (core,*core.parents)),'Symlink core root refused')
    core=core.resolve();U=load(core/'portable_run.py',RUNNER_SHA,'_unchanged_metadata_runner')
    C=load(core/CHECKER,COMPOSITION_SHA,'_unchanged_metadata_composition')
    supervisor,supervision=metadata_supervisor(U)
    accepted,cache_proof=accepted_terminals_adapter(C)
    profile={}
    main,main_proof=function(C,'main',[
        ('need(0 < args.budget_seconds <= 110 and args.start >= 0 and (args.limit is None or args.limit > 0), "Invalid budget/slice")',
         'need(args.command == "aggregate" and args.phase in ("acceptance","final") and 0 < args.budget_seconds <= 600 and args.start >= 0 and (args.limit is None or args.limit > 0), "Invalid metadata phase/budget/slice")'),
        ('report = {"schema":SCHEMA,"kind":args.command,"status":"NOT_STARTED"}',
         'report = {"schema":SCHEMA,"kind":args.command,"status":"NOT_STARTED","metadata_adapter":_metadata_profile()}')],
        {'accepted_terminals':accepted,'_metadata_profile':lambda:profile})
    def execute_core(config):
        validate_words(U,config['checker'],config['requested_checker_args'],config['timeout_seconds'])
        need(config['metadata_adapter']==profile,'Changed metadata child source profile')
        raise SystemExit(main())
    def validate_config(config):
        need(config.get('metadata_adapter')==profile,'Missing or stale metadata invocation profile')
        validate_words(U,config['checker'],config['requested_checker_args'],config['timeout_seconds'])
    child,child_proof=function(U,'child_main',[
        ('config = decode(Path(path).read_bytes())','config = decode(Path(path).read_bytes());_validate_config(config)'),
        ('"applied": applied, "pid": os.getpid(), "before_mathematical_calls": True}',
         '"applied": applied, "pid": os.getpid(), "before_mathematical_calls": True,"metadata_adapter":_metadata_profile()}'),
        ('runpy.run_path(str(CODE / config["checker"]), run_name="__main__")','_execute_core(config)')],
        {'_validate_config':validate_config,'_execute_core':execute_core,'_metadata_profile':lambda:profile})
    run,run_proof=function(U,'run',[
        ('need(math.isfinite(args.timeout) and 0 < args.timeout <= 120, "Child timeout must be at most 120 seconds")',
         '_validate_words(args.checker,args.checker_args[1:] if args.checker_args[:1] == ["--"] else args.checker_args,args.timeout)'),
        ('pin(__file__), pin(Path(sys.executable).resolve()),','pin(__file__),pin(_adapter_path), pin(Path(sys.executable).resolve()),'),
        ('"historical_receipts_rewritten": False, "whole_theorem_accepted": False, "created_utc": utc()}',
         '"historical_receipts_rewritten": False, "whole_theorem_accepted": False, "created_utc": utc(),"metadata_adapter":_metadata_profile()}'),
        ('str(Path(__file__).resolve()),\n               "_child", "--configuration",',
         'str(_adapter_path),\n               "--core-code-root",str(CODE),"_child", "--configuration",')],
        {'supervise':supervisor,'_validate_words':lambda checker,words,timeout:validate_words(U,checker,words,timeout),
         '_adapter_path':Path(__file__).resolve(),'_metadata_profile':lambda:profile})
    profile.update(schema=SCHEMA,adapter=U.pin(__file__),core_root=str(core),original_runner=U.pin(core/'portable_run.py'),
                   original_checker=U.pin(core/CHECKER),supervision=supervision,terminal_path_cache=cache_proof,
                   function_adaptations=[main_proof,child_proof,run_proof],metadata_internal_max=600,metadata_physical_max=660,
                   whole_theorem_accepted=False)
    return U,run,child,profile


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--core-code-root',type=Path);sub=p.add_subparsers(dest='mode',required=True)
    q=sub.add_parser('run')
    for name in ('core-code-root','data-root','work-root'):q.add_argument('--'+name,type=Path,required=True)
    q.add_argument('--id',required=True);q.add_argument('--checker',required=True);q.add_argument('--timeout',type=float,default=660)
    q.add_argument('checker_args',nargs=argparse.REMAINDER)
    q=sub.add_parser('_child')
    q.add_argument('--configuration',type=Path,required=True);q.add_argument('--configuration-sha256',required=True)
    args=p.parse_args(argv)
    try:
        _,run,child,_=build(args.core_code_root)
        return child(args.configuration,args.configuration_sha256) if args.mode=='_child' else run(args)
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(json.dumps({'status':'METADATA_INVOCATION_REFUSED','error':f'{type(error).__name__}: {error}','whole_theorem_accepted':False}),file=sys.stderr)
        return 2


def metadata_supervisor(module):
    path=Path(module.__file__).resolve();raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if digest!=RUNNER_SHA:raise ValueError('Unexpected original process-supervisor source')
    nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='supervise']
    if len(nodes)!=1:raise ValueError('Missing/duplicate exact supervisor function')
    original=ast.get_source_segment(raw.decode(),nodes[0])
    if original.count(OLD_GUARD)!=1:raise ValueError('Original supervisor guard differs')
    adapted=original.replace(OLD_GUARD,NEW_GUARD,1)
    if adapted.replace(NEW_GUARD,OLD_GUARD,1)!=original:raise ValueError('Supervisor changed beyond its deadline guard/message')
    ns=dict(vars(module));exec(compile(adapted,str(Path(__file__).resolve())+'::metadata-supervise-660','exec'),ns)
    proof={'original_supervisor_source':{'path':str(path),'bytes':len(raw),'sha256':digest},
           'original_function_sha256':hashlib.sha256(original.encode()).hexdigest(),
           'executed_function_sha256':hashlib.sha256(adapted.encode()).hexdigest(),
           'exact_replacement':{'before':OLD_GUARD,'after':NEW_GUARD},'process_and_cleanup_behavior_unchanged':True}
    return ns['supervise'],proof


def accepted_terminals_adapter(module):
    path=Path(module.__file__).resolve();raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=COMPOSITION_SHA:raise ValueError('Wrong original composition source')
    nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='accepted_terminals']
    if len(nodes)!=1:raise ValueError('Missing/duplicate exact terminal-acceptance function')
    original=ast.get_source_segment(raw.decode(),nodes[0])
    edits=[('    accepted,checked_evidence = set(),{}','    accepted,checked_evidence,resolved_paths = set(),{},{}'),
           ('                    path = str(Path(item["path"]).resolve())',
            '                    raw_path = item["path"]\n                    if raw_path not in resolved_paths:\n                        resolved_paths[raw_path] = str(Path(raw_path).resolve())\n                    path = resolved_paths[raw_path]')]
    adapted=original
    for before,after in edits:
        if adapted.count(before)!=1:raise ValueError('Exact accepted-terminals cache site changed')
        adapted=adapted.replace(before,after,1)
    inverse=adapted
    for before,after in reversed(edits):inverse=inverse.replace(after,before,1)
    if inverse!=original:raise ValueError('Terminal predicate changed beyond the exact path-resolution cache')
    ns=dict(vars(module));exec(compile(adapted,str(Path(__file__).resolve())+'::accepted-terminals-path-cache','exec'),ns)
    proof={'original_composition_source':{'path':str(path),'bytes':len(raw),'sha256':COMPOSITION_SHA},
           'original_function_sha256':hashlib.sha256(original.encode()).hexdigest(),
           'executed_function_sha256':hashlib.sha256(adapted.encode()).hexdigest(),
           'exact_replacements':[{'before':a,'after':b} for a,b in edits],
           'per_reference_hash_equality_and_initial_final_rehash_unchanged':True}
    return ns['accepted_terminals'],proof

OLD_GUARD='need(os.name == "posix" and math.isfinite(timeout) and 0 < timeout <= 120, "A POSIX host and a child deadline of at most 120 seconds are required")'
NEW_GUARD='need(os.name == "posix" and math.isfinite(timeout) and 0 < timeout <= 660, "A POSIX host and a metadata deadline of at most 660 seconds are required")'

if __name__=="__main__":raise SystemExit(main())
