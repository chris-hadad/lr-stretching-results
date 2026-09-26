#!/usr/bin/env python3
"""Bounded malformed-record, coordinate-order and output/process controls."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import signal
import sys
import time

import verify_forcing as v


def main():
    v.require(__debug__, 'Optimized Python is refused')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=v.fresh_output(args.output,args.data_root)
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGALRM,signal.SIGUSR1):
        signal.signal(sig,v.interrupted)
    signal.setitimer(signal.ITIMER_REAL,120)
    started=time.monotonic()
    result={'status':'INCOMPLETE','positive':[],'negative':[],
            'source':{p.name:v.pin(p) for p in v.HERE.glob('*.py')},'pid':os.getpid()}
    def reject(name,fn,text=None):
        try:fn()
        except (ValueError,RuntimeError,KeyError,TypeError) as exc:
            v.require(text is None or text in str(exc),'Wrong rejection in '+name+': '+str(exc))
            result['negative'].append({'id':name,'error':str(exc)})
        else:raise RuntimeError('Bad fixture accepted: '+name)
    try:
        doc=v.load_table(args.data_root,6)
        m=v.model(6)
        for n in (6,7):
            v.coordinate_binding(n,v.model(n))
            result['positive'].append('full-coordinate-row-binding-rank-'+str(n))
        masks=[0,1,3,31,32,1023,21845,32767]
        for mask in masks:v.compare_record(doc['records'][mask],6,m,{})
        result['positive'].append('eight-original-mask-extremes')
        original=deepcopy(doc['records'][0])
        for field in ('closed_rows_mask','dimension_bound'):
            changed=dict(original);changed[field]+=1
            reject('changed-'+field,lambda changed=changed:v.compare_record(changed,6,m,{}))
        for mask in (-1,1<<15,True,'0'):
            reject('invalid-mask-'+str(mask),lambda mask=mask:v.exact_mask(mask,6))
        for field in ('closed_rows_mask','dimension_bound'):
            changed=dict(original);changed[field]=True
            reject('boolean-'+field,lambda changed=changed:v.compare_record(changed,6,m,{}))
        omitted=dict(doc);omitted['records']=doc['records'][:-1]
        reject('omitted-record',lambda:v.validate_table(omitted,6),'Omitted or extra')
        duplicate=dict(doc);duplicate['records']=doc['records'][:]
        duplicate['records'][1]=original
        reject('duplicate-record',lambda:v.validate_table(duplicate,6),'Duplicate, omitted or reordered')
        changed=deepcopy(m);changed['A'][0],changed['A'][1]=changed['A'][1],changed['A'][0]
        changed['B'][0],changed['B'][1]=changed['B'][1],changed['B'][0]
        reject('permuted-full-row-order',lambda:v.coordinate_binding(6,changed),'row ordering differ')
        changed=deepcopy(m);changed['gaps'][0]=changed['gaps'][1]
        reject('changed-boundary-gap-bit',lambda:v.coordinate_binding(6,changed),'side/bit convention differs')
        reject('existing-output',lambda:v.fresh_output(out,args.data_root),'already exists')
        reject('source-overlap-output',lambda:v.fresh_output(v.HERE/'fixture-forbidden-output',args.data_root),'overlaps')
        reject('data-overlap-output',lambda:v.fresh_output(args.data_root/'fixture-forbidden-output',args.data_root),'overlaps')
        reject('absent-output-parent',lambda:v.fresh_output(out/'absent-parent/child',args.data_root),'parent must already exist')
        reject('duplicate-json-key',lambda:v.decode('{"mask":0,"mask":1}'),'Duplicate JSON key')
        bad=out/'changed-data';(bad/'f025').mkdir(parents=True)
        raw=(args.data_root/v.TABLES[6]['path']).read_bytes()
        (bad/v.TABLES[6]['path']).write_bytes(raw+b' ')
        reject('changed-table-hash',lambda:v.load_table(bad,6),'size/hash differs')
        receipt,raw=v.child([sys.executable,'-O','-B',str(v.HERE/'verify_forcing.py'),'--data-root',str(args.data_root),
                             '--output',str(out/'optimized-output')],out/'optimized-python',10)
        v.require(receipt['returncode']!=0 and not (out/'optimized-output').exists(),'Optimized Python accepted or created output')
        v.require('Optimized Python is refused' in (out/'optimized-python/stderr.txt').read_text(),'Wrong optimized-Python rejection')
        result['negative'].append({'id':'optimized-python','returncode':receipt['returncode']})
        reject('child-timeout',lambda:v.child([sys.executable,'-B','-c','import time; time.sleep(10)'],out/'timeout',0.1),'deadline exceeded')
        receipt=v.decode((out/'timeout/receipt.json').read_bytes())
        v.require(receipt['returncode']<0 and receipt['wait_completed'] and receipt['group_absent'],'Timeout child survived')
        reject('child-signal',lambda:v.child([sys.executable,'-B','-c',
            'import os,signal,time; os.kill(int(__import__("sys").argv[1]),signal.SIGUSR1); time.sleep(10)',str(os.getpid())],out/'signal',10),'Interrupted by signal')
        receipt=v.decode((out/'signal/receipt.json').read_bytes())
        v.require(receipt['returncode']<0 and receipt['wait_completed'] and receipt['group_absent'],'Signaled child survived')
        result.update(status='COMPLETE_FORCING_CONTROLS',positive_cases=10,negative_cases=len(result['negative']))
    except BaseException as exc:
        result.update(status='FAILED',error=str(exc));raise
    finally:
        v.stop_child();signal.setitimer(signal.ITIMER_REAL,0)
        result.update(elapsed_seconds=time.monotonic()-started,active_child=None)
        v.write_new(out/'result.json',result)
    print(json.dumps({k:result[k] for k in ('status','positive_cases','negative_cases','elapsed_seconds','active_child')}))


if __name__=='__main__':main()
