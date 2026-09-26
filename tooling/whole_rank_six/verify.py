#!/usr/bin/env python3
"""Run the complete small rank-six certificate components in a fresh directory."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,signal,subprocess,sys,time
from pathlib import Path
from runtime import run_owned

HERE=Path(__file__).resolve().parent
EXPECTED={f'{d}/{n}' for d in ('top','c6') for n in ('forward.cpp','verify.py','local_values.cpp')}
EXPECTED|={f'c6/data/{n}.json.gz' for n in ('raw','incidence','field')}

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['small'])
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--cxx',default='c++')
    parser.add_argument('--gmp-prefix',type=Path)
    args=parser.parse_args()
    out=args.out.resolve()
    need(not out.exists() and out.parent.is_dir(),'output must be a fresh directory with an existing parent')
    need(out!=HERE and HERE not in out.parents,'keep generated output outside the source tree')
    need(not sys.flags.optimize,'run with Python assertions enabled')
    manifest=json.loads((HERE/'DATA-SMALL.json').read_text())
    need(set(manifest['files'])==EXPECTED,'incomplete or unexpected small-component manifest')
    for rel,record in manifest['files'].items():
        p=HERE/rel
        need(p.is_file() and not p.is_symlink(),'missing or nonregular input: '+rel)
        need(p.stat().st_size==record['bytes'] and sha(p)==record['sha256'],'changed input: '+rel)
    out.mkdir();started=time.monotonic();records=[]
    def stop(sig,frame):raise InterruptedError('received signal '+str(sig))
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,stop)
    def run(label,command,seconds=600):
        with (out/(label+'.stdout')).open('wb') as stdout,(out/(label+'.stderr')).open('wb') as stderr:
            record=run_owned(command,stdout=stdout,stderr=stderr,timeout=seconds,
                env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
        record['label']=label;records.append(record)
        need(record['exit']==0,'component refused: '+label+'; see '+str(out/(label+'.stderr')))
    status='FAILED';reason=None
    try:
        spec=importlib.util.spec_from_file_location('rank_six_top',HERE/'top/verify.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        normals=module.hive_normals()
        (out/'atlas.txt').write_text('42 10\n'+'\n'.join(' '.join(map(str,r)) for r in normals)+'\n')
        prefix=args.gmp_prefix
        if prefix is None and Path('/opt/homebrew/include/gmpxx.h').is_file():prefix=Path('/opt/homebrew')
        flags=[] if prefix is None else ['-I',str(prefix/'include'),'-L',str(prefix/'lib')]
        for part in ('top','c6'):
            binary=out/(part+'-forward')
            run('compile-'+part,[args.cxx,'-std=c++17','-O2',*flags,str(HERE/part/'forward.cpp'),'-lgmpxx','-lgmp','-o',str(binary)],120)
            run('forward-'+part,[str(binary),str(out/'atlas.txt')])
            command=[sys.executable,'-B',str(HERE/part/'verify.py'),'--reference',str(out/('forward-'+part+'.stdout'))]
            if part=='top':command+=['--output',str(out/'top.json')]
            else:command+=['--data',str(HERE/'c6/data'),'--geometry-module',str(HERE/'top/verify.py'),'--out',str(out/'c6.json')]
            run('check-'+part,command)
        top=json.loads((out/'top.json').read_text());c6=json.loads((out/'c6.json').read_text())
        need(top['status']=='PASS_COMPLETE' and c6['status']=='PASS_COMPLETE_C6','incomplete component')
        for rel,record in manifest['files'].items():need(sha(HERE/rel)==record['sha256'],'input changed during run')
        status='PASS_COMPLETE_SMALL_COMPONENTS'
    except BaseException as error:
        reason=repr(error)
        raise
    finally:
        result={'schema':'rank-six-small-replay-v1','status':status,'reason':reason,
                'scope':'complete c6,c7,c8,c9 numerical certificates; c10 is the volume term',
                'whole_rank_six_verified':False,'remaining_components':['c1','c2','c3','c4','c5'],
                'seconds':time.monotonic()-started,'all_completed_command_groups_exited':all(r['owned_process_group_exited'] for r in records),'commands':records}
        (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='commands'}))

if __name__=='__main__':main()
