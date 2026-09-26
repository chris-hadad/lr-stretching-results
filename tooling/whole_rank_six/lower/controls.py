#!/usr/bin/env python3
"""Deliberate missing/changed scalar, zero field, and H8 malformed/coefficient controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from replay import (A15, A17, C3, PRO33, available_memory, check_cancelled,
                    distinct_roots,
                    fresh_json, install_signal_handlers, refuse_optimized,
                    require, verify_assets)
from runtime import group_exists, stop_group

HERE=Path(__file__).resolve().parent


def rejected(argv, receipt, must_contain, timeout=120):
    require(not receipt.exists(), 'fresh control receipt')
    available=available_memory()
    require(available >= 4*2**30, 'control memory guard')
    start=time.monotonic()
    child=None
    try:
        check_cancelled()
        child=subprocess.Popen([str(x) for x in argv],stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,text=True,start_new_session=True,
                               env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1',
                                    'PYTHONDONTWRITEBYTECODE':'1','PYTHONOPTIMIZE':''})
        deadline=start+timeout
        while True:
            check_cancelled()
            remaining=deadline-time.monotonic()
            if remaining<=0:
                raise TimeoutError('control hard timeout')
            try:
                out,err=child.communicate(timeout=min(0.2,remaining))
                break
            except subprocess.TimeoutExpired:
                continue
        require(not group_exists(child.pid), 'control left live process group: '+str(child.pid))
        check_cancelled()
    except BaseException:
        if child is not None:
            stop_group(child)
        raise
    require(child.returncode != 0 and must_contain in (out+err),
            'control unexpectedly passed or wrong failure: '+out[-500:]+err[-500:])
    fresh_json(receipt,{'status':'PASS_EXPECTED_REFUSAL','argv':[str(x) for x in argv],
                        'returncode':child.returncode,'stdout':out.strip(),'stderr':err.strip(),
                        'seconds':time.monotonic()-start,'available_memory_before_bytes':available,
                        'child_waited':True,'owned_process_group_exited':True})
    return out


def shadow_assets(assets,phase,omit=None,replace=None):
    manifest=json.loads((HERE/'ASSETS.json').read_text())
    root=phase
    root.mkdir()
    for name in manifest['groups']['c2-field']:
        check_cancelled()
        if name==omit:continue
        dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True)
        if name==replace:
            shutil.copyfile(assets/name,dest)
        else:
            dest.symlink_to((assets/name).resolve())
    return root


def main():
    refuse_optimized()
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--asset-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();assets,out=distinct_roots(args.asset_root,args.output)
    require(out.is_dir(), 'existing replay output directory required')
    install_signal_handlers()
    require((out/'c2-field/COMPLETE.json').is_file() and (out/'h8/k3-COMPLETE.json').is_file(),
            'complete c2 field and fresh small H8 proof required')
    phase=out/'controls';phase.mkdir()
    manifest=json.loads((HERE/'ASSETS.json').read_text())
    scalar=str(A17/'full-rhs.tsv')
    field=str(A17/'full-cyclic-polish30.i64')
    missing=shadow_assets(assets,phase/'missing-scalar',omit=scalar)
    try:verify_assets(missing,'c2-field')
    except RuntimeError as exc:require('missing or wrong-size asset' in str(exc) and scalar in str(exc),'missing scalar refusal');fresh_json(phase/'missing-scalar.json',{'status':'PASS_EXPECTED_MISSING_SCALAR_REFUSAL','reason':str(exc)})
    else:raise RuntimeError('missing scalar accepted')
    changed=shadow_assets(assets,phase/'changed-scalar',replace=scalar)
    with (changed/scalar).open('r+b') as stream:
        first=stream.read(1);stream.seek(0);stream.write(b'9' if first!=b'9' else b'8')
    require((changed/scalar).stat().st_size==manifest['files'][scalar]['bytes'],'changed scalar size')
    try:verify_assets(changed,'c2-field')
    except RuntimeError as exc:require('changed asset' in str(exc) and scalar in str(exc),'changed scalar refusal');fresh_json(phase/'changed-scalar.json',{'status':'PASS_EXPECTED_CHANGED_SCALAR_REFUSAL','reason':str(exc)})
    else:raise RuntimeError('changed scalar accepted')
    zero=shadow_assets(assets,phase/'zero-field',replace=field)
    with (zero/field).open('r+b') as stream:stream.write(b'\0'*manifest['files'][field]['bytes'])
    try:verify_assets(zero,'c2-field')
    except RuntimeError as exc:require('changed asset' in str(exc) and field in str(exc),'zero field binding refusal');fresh_json(phase/'zero-field-binding.json',{'status':'PASS_EXPECTED_ZERO_FIELD_BINDING_REFUSAL','reason':str(exc)})
    else:raise RuntimeError('zero field accepted by binding')
    checker=out/'bin/field-original'
    require(checker.is_file() and not checker.is_symlink() and not (out/'bin').is_symlink(),
            'own compiled c2 checker')
    begin,end=0,100000
    stdout=rejected([checker,assets/C3/'U02/DATA',assets/A15,assets/PRO33/'U07/DATA/COLLATION/merge-02-00.types',
                     assets/A17/f'full-operator-{begin:08d}-{end:08d}-001.rows',begin,end,
                     assets/A17/'full-rhs.tsv',assets/A17/'full-rhs.offsets',zero/field,1000000000000,0,
                     phase/'zero-field.result.json'],phase/'zero-field-native.json','FAIL_EXACT_ORIGINAL_FIELD_RANGE')
    result=json.loads(stdout.strip());require(result['violations']>0,'zero field must cause an exact inequality failure')
    h8=out/'bin/h8-check';require(h8.is_file() and not h8.is_symlink(),'own compiled small H8 checker')
    source=(out/'h8/SOURCES.txt').read_text();bad=phase/'malformed-q1.layer8'
    original=(assets/PRO33/'U06/DATA/LAYER8/q1.layer8').read_text()
    require('0 1209600 1' in original,'expected q1 control row')
    bad.write_text(original.replace('0 1209600 1','0 0 1',1))
    line=source.splitlines()[0]
    parts=line.split();require(len(parts)==3 and parts[0]=='1','source list q1 shape')
    altered=source.replace(line,f'{parts[0]} {bad} {parts[2]}',1)
    altered_sources=phase/'SOURCES-MALFORMED.txt';altered_sources.write_text(altered)
    rejected([h8,assets/C3,altered_sources,out/'h8/LOWER-0.txt',phase/'malformed.rows','verify',1,0,4,'none',4],
             phase/'malformed-h8.json','REFUSED:')
    rejected([h8,assets/C3,out/'h8/SOURCES.txt',out/'h8/LOWER-0.txt',phase/'coefficient.rows','verify',1,0,4,'coefficient',4],
             phase/'coefficient-h8.json','REFUSED:')
    fresh_json(phase/'COMPLETE.json',{'status':'PASS_EXPECTED_NEGATIVE_CONTROLS',
                                     'controls':['missing-scalar','changed-scalar','zero-field-binding','zero-field-native',
                                                 'malformed-h8','coefficient-h8']})

if __name__=='__main__':main()
