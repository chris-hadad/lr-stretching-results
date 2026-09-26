#!/usr/bin/env python3
"""Complete supplied-scalar c1 certificate check from the versioned data bundle.

This verifies the original cone, every physical branch, the primitive field
action, and q8/q9 extension coverage. Complete q7 topology and analytic scalar
regeneration are separately required components of whole-theorem verification.
"""
from __future__ import annotations
import argparse,hashlib,json,os,shutil,signal,subprocess,sys,time
from pathlib import Path
from runtime import run_owned

HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',type=Path,required=True,help='Expanded versioned asset root, containing data/')
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--sage',help='Optional independent Sage cross-check; otherwise Python standard library suffices')
    ap.add_argument('--cxx',default='c++')
    ap.add_argument('--gmp-prefix',type=Path)
    args=ap.parse_args();data=args.data.resolve();out=args.out.resolve();started=time.monotonic()
    need(not sys.flags.optimize,'Python assertions must be enabled')
    need(not out.exists() and out.parent.is_dir(),'fresh output directory required')
    need(out!=data and data not in out.parents and out!=HERE and HERE not in out.parents,'keep generated output outside the source and data trees')
    if args.sage:need(shutil.which(args.sage) is not None,'specified Sage executable is unavailable')
    inputs=json.loads((HERE/'C1-INPUTS.json').read_text())
    need(inputs['schema']=='rank-six-c1-inputs-v1' and len(inputs['files'])==1570,'complete input declaration')
    for rel,spec in inputs['files'].items():
        path=Path(rel)
        need(not path.is_absolute() and '..' not in path.parts,'unsafe relative input')
        p=data/path
        need(p.is_file() and not p.is_symlink(),'missing or nonregular input: '+rel)
        need(p.stat().st_size==spec['bytes'] and digest(p)==spec['sha256'],'changed input: '+rel)
    authentication_seconds=time.monotonic()-started
    out.mkdir();records=[];status='FAILED';reason=None
    for n in ('bin','geometry','classification','tmp','sage'):(out/n).mkdir()
    def stop(sig,frame):raise InterruptedError('received signal '+str(sig))
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,stop)
    def run(label,cmd,timeout):
        with (out/(label+'.stdout')).open('wb') as stdout,(out/(label+'.stderr')).open('wb') as stderr:
            rec=run_owned(cmd,stdout=stdout,stderr=stderr,timeout=timeout,
                env={**os.environ,'DOT_SAGE':str(out/'sage'),'TMPDIR':str(out/'tmp'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':'','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
        rec['label']=label
        records.append(rec)
        (out/'PROGRESS.json').write_text(json.dumps({'completed':records},indent=2)+'\n')
        need(rec['exit']==0,'verification refused: '+label+'; see '+str(out/(label+'.stderr')))
        print('PASS',label,round(rec['seconds'],2),flush=True)
    try:
        prefix=args.gmp_prefix
        if prefix is None and Path('/opt/homebrew/include/gmpxx.h').is_file():prefix=Path('/opt/homebrew')
        flags=[] if prefix is None else ['-I',str(prefix/'include'),'-L',str(prefix/'lib')]
        cxx=[args.cxx,'-std=c++17','-O3',*flags]
        src=HERE/'src'
        run('compile-classify',cxx+[str(src/'astra054-2026-09-25/geometry/classify_v1.cpp'),'-o',str(out/'bin/classify')],180)
        run('compile-field',cxx+[str(src/'astra054-2026-09-25/field-check/retained_field_check_v1.cpp'),'-lgmpxx','-lgmp','-o',str(out/'bin/field')],180)
        run('compile-coverage',cxx+[str(src/'portable/coverage.cpp'),'-lgmpxx','-lgmp','-o',str(out/'bin/coverage')],180)
        run('geometry',[sys.executable,'-B',str(src/'portable/geometry_stdlib.py'),str(data/'data/geometry/atlas.json'),str(out/'geometry')],300)
        if args.sage:
            (out/'geometry-sage').mkdir()
            run('geometry-sage',[args.sage,'-python',str(src/'portable/geometry.py'),str(data/'data/geometry/atlas.json'),str(out/'geometry-sage')],300)
            for name in ('GEOMETRY.json','CLASSIFY.txt'):
                need((out/'geometry'/name).read_bytes()==(out/'geometry-sage'/name).read_bytes(),'independent Sage mismatch: '+name)
        run('classification',[str(out/'bin/classify'),str(out/'geometry/CLASSIFY.txt'),str(data/'data/c1/q9.rows'),str(data/'data/c1/cls.class.u8'),'0','27230728',str(out/'classification')],600)
        ranges=[]
        for p in (data/'data/c1/rhs').iterdir():
            h=(p/'HEADER.txt').read_text().split()
            need(len(h)==4 and h[:2]==['A19_RHS_V1','original'],'RHS header')
            ranges.append((int(h[2]),int(h[3]),p))
        ranges.sort()
        need(len(ranges)==455 and ranges[0][0]==0 and ranges[-1][1]==27230728,'complete RHS endpoints')
        need(all(a[0]<a[1] and a[1]==b[0] for a,b in zip(ranges,ranges[1:])),'RHS gaps or overlaps')
        (out/'rhs.txt').write_text(''.join(str(p)+'\n' for a,b,p in ranges))
        run('field',[str(out/'bin/field'),str(data/'data/geometry/atlas.txt'),str(data/'data/c1/q9.rows'),str(data/'data/c1'),str(data/'data/c1/matrix'),str(out/'rhs.txt'),str(data/'data/c1/prune_b.numerators.i64'),str(out/'classification/RETAIN.u8'),'10000000000',str(out/'FIELD.json')],3600)
        run('coverage',[str(out/'bin/coverage'),str(data/'data/geometry/atlas.txt'),str(data/'data/geometry'),str(data/'data/q7-kernels'),str(data/'data/c1'),str(data/'data/c1/q9.rows')],3600)
        geometry=json.loads((out/'geometry/RESULT.json').read_text())
        classified=json.loads((out/'classification/RESULT.json').read_text())
        field=json.loads((out/'FIELD.json').read_text())
        coverage=json.loads((out/'coverage.stdout').read_text())
        need(geometry['H_V_H_exact_equal'] and geometry['rays']==166,'complete universal cone')
        need(classified['status']=='PASS' and classified['rows']==27230728 and classified['branches_checked']==46327714 and classified['retained']==13325662,'complete original branches')
        need(field['scope']=='original' and field['status']=='PASS_RETAINED_AT_LEAST_EPSILON' and field['begin']==0 and field['end']==27230728 and field['rows']==27230728,'complete original field scope')
        need(field['retained_rows']==13325662 and field['retained_below_epsilon']==0 and field['primitive_incidences']==119963492,'complete primitive field')
        need(field['retained_minimum']['value']=='40142888690844119591010700379369/40149066134252712057708583296000000000','exact field minimum')
        need(coverage['status']=='PASS_COMPLETE_EXTENSIONS_GIVEN_COMPLETE_Q7' and coverage['original_q8']==62868270 and coverage['original_q9']==163364983,'complete extension coverage')
        for rel,spec in inputs['files'].items():
            need((data/rel).stat().st_size==spec['bytes'] and digest(data/rel)==spec['sha256'],'input changed during verification: '+rel)
        status='PASS_COMPLETE_C1_SUPPLIED_SCALAR_CERTIFICATE'
    except BaseException as error:
        reason=repr(error)
        raise
    finally:
        summary={'schema':'rank-six-c1-replay-v1','status':status,'reason':reason,
                 'whole_rank_six_verified':False,'requires':['complete q7 topology','complete local-scalar and lower-cache analytic certification','remaining coefficient components','mathematical implication'],
                 'seconds':time.monotonic()-started,'initial_authentication_seconds':authentication_seconds,'commands':records,'all_completed_command_groups_exited':all(r['owned_process_group_exited'] for r in records),
                 'input_manifest_sha256':digest(HERE/'C1-INPUTS.json')}
        (out/'RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(status)

if __name__=='__main__':main()
