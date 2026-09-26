#!/usr/bin/env python3
"""Reconstruct the complete hive cone and exact branch/boundary examples."""
from pathlib import Path
import argparse,hashlib,json,os,signal,sys,time
from runtime import run_owned
HERE=Path(__file__).resolve().parent


def need(ok,message):
    if not ok:raise ValueError(message)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    out=args.out.resolve();need(not out.exists() and out.parent.is_dir(),'fresh output and existing parent required')
    need(out!=HERE and HERE not in out.parents,'output must be outside source tree')
    need(not sys.flags.optimize,'use unoptimized Python')
    pins=json.loads((HERE/'GEOMETRY-INPUTS.json').read_text())
    need(set(pins['files'])=={'atlas.json','controls_geometry.py','src/portable/geometry_stdlib.py'},'complete small geometry inputs')
    for rel,record in pins['files'].items():
        p=HERE/rel;need(p.is_file() and not p.is_symlink(),'regular geometry input')
        with p.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
        need(actual==record['sha256'] and p.stat().st_size==record['bytes'],'changed geometry input: '+rel)
    out.mkdir();(out/'cone').mkdir();records=[];status='FAILED_OR_PARTIAL';reason=None;started=time.monotonic()
    def stop(sig,frame):raise InterruptedError('received signal '+str(sig))
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,stop)
    try:
        for label,command in [('cone',[sys.executable,'-B',str(HERE/'src/portable/geometry_stdlib.py'),str(HERE/'atlas.json'),str(out/'cone')]),
                              ('controls',[sys.executable,'-B',str(HERE/'controls_geometry.py'),str(out/'cone/GEOMETRY.json'),str(out/'CONTROLS.json')])]:
            with (out/(label+'.stdout')).open('wb') as so,(out/(label+'.stderr')).open('wb') as se:
                record=run_owned(command,stdout=so,stderr=se,timeout=120,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':''})
            record['label']=label;records.append(record);need(record['exit']==0,'component refused: '+label)
        need(json.loads((out/'cone/RESULT.json').read_text())['status']=='PASS_COMPLETE_HIVE_CONE','complete cone')
        need(json.loads((out/'CONTROLS.json').read_text())['status']=='PASS_EXACT_ORIGINAL_HIVE_CONTROLS','all branch and boundary cases')
        status='PASS_COMPLETE_CONE_AND_EXACT_EXAMPLES'
    except BaseException as error:reason=repr(error);raise
    finally:
        result={'status':status,'reason':reason,'scope':'complete universal cone and exact branch/boundary examples; no coefficient field or full theorem verification',
                'whole_rank_six_verified':False,'seconds':time.monotonic()-started,'commands':records}
        (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(status)


if __name__=='__main__':main()
