"""Freeze fresh-count jobs from complete independently checked early terminals."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import recount_records as R
import verify_early_terminals as E


def chart_model(g, actual_required):
    """A closed count needs a saturated chart, not a claim of minimal dimension."""
    n,d=R.integer(g['rank']),R.integer(g['degree_bound'])
    R.need(n in (6,7) and 1<=d<=(n-1)*(n-2)//2,'Invalid early chart rank/bound')
    if actual_required:
        R.need(R.integer(g['actual_dimension'])==d,'Interior needs proved actual dimension')
    parts=[g['count_boundary'][k] for k in ('lambda','mu','nu')]
    for p in parts:
        R.need(len(p)==n and all(type(x) is int and x>=0 for x in p) and p==sorted(p,reverse=True),'Invalid whole count boundary')
    area=sum(parts[0])
    R.need(area==sum(parts[1])+sum(parts[2]),'Unbalanced whole count')
    chart=g['chart'];T=R.matrix(chart['basis_rows'],d)
    off=list(map(R.integer,chart['offset']));translation=list(map(R.integer,g['translation']))
    D=(n-1)*(n-2)//2
    R.need(len(T)==len(off)==D and len(translation)==d,'Incomplete original affine map')
    base=[b+sum(a*x for a,x in zip(row,translation)) for b,row in zip(off,T)]
    selections=[]
    for j in range(d):
        unit=[int(k==j) for k in range(d)]
        choices=[i for i,row in enumerate(T) if row==unit]
        R.need(choices,'No integer coordinate selection inverse')
        i=choices[0]
        selections.append({'variable':j,'original_hive_coordinate':i,'base':base[i],'unit_row':unit})
    raw=R.matrix(g['original_rhombus_rows'],D+1)
    R.need(len(raw)==3*n*(n-1)//2,'Omitted original rhombus')
    rows=[[row[0]+sum(a*b for a,b in zip(row[1:],base)),
           *[sum(a*T[i][j] for i,a in enumerate(row[1:])) for j in range(d)]] for row in raw]
    R.need(rows==R.matrix(g['full_translated_rows'],d+1),'Whole original affine substitution changed')
    return {'rank':n,'dimension':d,'count_boundary_area':area,'full_rows':rows,'unit_selections':selections,
            'actual_dimension_required_and_proved':actual_required,
            'geometry_premise':'Complete independently checked saturated whole chart and row/hive inverse; 0 <= h <= t*sum(lambda). Closed-only jobs do not claim minimal affine dimension.'}


def physical_nodes(record):
    unit=record['unit'];nodes={};seen=set()
    if unit=='U02':
        determining={('I' if t<0 else 'P')+str(abs(t)) for t in record['determining_nodes']}
        holds={m:{'P'+str(t) for t in record['unused_hold_nodes']} for m in ('hive','rows')}
    elif record['kind']=='FOUR_COUNT':
        determining={'P1','P2','I1','I2'};holds={m:set() for m in ('hive','rows')}
    else:
        determining={'P'+str(t) for t in record['determining_nodes']}
        holds={h['model']:{'P'+str(t) for t in h['physical_sites']} for h in record['holdouts']}
        R.need(set(holds)=={'hive','rows'},'Missing held model')
    wanted={(m,k) for m in ('hive','rows') for k in determining|holds[m]}
    for binding in record['count_bindings']:
        if binding['status']!='complete':
            R.need(binding['status']=='preserved_refusal','Unknown early count status')
            continue
        model=binding['model']
        if unit=='U02':
            signed=R.integer(binding['signed_node']);grade=abs(signed);strict=signed<0
            value=R.integer(binding['count'])
        else:
            grade=R.integer(binding.get('original_physical_grade',binding['grade']))
            strict=binding['strict'];value=R.integer(binding['value'])
        R.need(type(strict) is bool and grade>=0 and (not strict or grade>0) and value>=0,'Bad physical count')
        kind=('I' if strict else 'P')+str(grade)
        R.need((model,kind) in wanted,'Unexpected source count outside exact early roster')
        node=nodes.setdefault(kind,{'kind':kind,'grade':grade,'strict':strict,'stored':{},
                                  'role':'determining' if kind in determining else 'positive_holdout'})
        R.need((node['grade'],node['strict'])==(grade,strict),'Physical kind collision')
        R.need(model not in node['stored'] or node['stored'][model]==value,'Conflicting early count retry')
        node['stored'][model]=value;seen.add((model,kind))
    R.need(seen==wanted,'Missing required early determining or unused-held model/site')
    return sorted(nodes.values(),key=lambda node:(node['strict'],node['grade']))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--source-manifest',type=Path,required=True)
    parser.add_argument('--source-manifest-sha256',required=True)
    parser.add_argument('--verification',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();deadline=R.Deadline(100)
    verification=E.json_data(args.verification.read_bytes())
    receipt=E.json_data(args.verification.with_name('receipt.json').read_bytes())
    R.need(receipt['state']=='complete' and receipt['cleanup_verified'] and receipt['source_input_bytes_unchanged']
           and receipt['outputs']['result.json']==R.sha(args.verification.read_bytes()),'Unaccepted or changed early verifier return')
    R.need(verification['status']=='PASS_CONDITIONAL_ON_RECORDED_COUNTS' and not verification['pending_slice_ids'],
           'Early source/geometry/algebra gate is incomplete')
    for name,binding in verification['code_sources'].items():
        R.need(E.pin(name)==binding,'Early verifier source changed after its full run')
    unit=verification['unit'];expected=verification['expected_ids']
    R.need(unit in ('U02','U03') and verification['checked_ids']==expected,'Only a complete exact used early roster may be indexed')
    R.need(len(expected)==(169 if unit=='U02' else 3478),'Early required population changed')
    identity=verification['identities'];identity_path=Path(identity['path'])
    R.need(E.pin(identity_path)=={k:identity[k] for k in ('bytes','sha256')},'Changed early identity ledger')
    inputs=E.Inputs(args.root,args.source_manifest,args.source_manifest_sha256)
    sources=[R.file_pin(p,deadline) for p in [args.verification,args.verification.with_name('receipt.json'),identity_path,
                                            args.source_manifest,Path(__file__),Path(R.__file__),Path(E.__file__),Path(E.G.__file__)]]
    output=args.output.resolve();jobs_path=output.with_suffix('.jobs.jsonl')
    R.need(not output.exists() and not jobs_path.exists() and not output.is_relative_to(args.root.resolve()),'Invalid output ownership')
    entries=[];seen=[];kinds=Counter()
    with identity_path.open('rb') as source,jobs_path.open('xb') as jobs:
        for ordinal,raw in enumerate(source):
            deadline.check();record=E.json_data(raw)
            R.need(record['status']=='PASS_CONDITIONAL_ON_RECORDED_COUNTS' and record['unit']==unit and record['id']==expected[ordinal],
                   'Early identity order/status changed')
            idx=R.integer(record['id']);seen.append(idx)
            ref=record['geometry_sources'][0] if unit=='U02' else record['geometry_source']
            g,gref=inputs.get(ref['path'],idx,'records' if unit=='U02' else None)
            R.need(gref==ref and E.digest(E.encoded(g))==record['geometry_check']['original_geometry_sha256'],
                   'Early geometry body/source binding changed')
            nodes=physical_nodes(record);actual=any(n['strict'] for n in nodes)
            R.need(not actual or record['geometry_check']['actual_dimension_proved'],'True interior lacks a verified actual hull')
            adapted,binding=E.normalize_geometry(g,unit,actual)
            if actual:
                R.need(binding['normalized_geometry_sha256']==record['geometry_check']['normalized_geometry_sha256'],
                       'Sourced actual-dimension normalization changed')
            model=chart_model(adapted,actual)
            job={'id':idx,'unit':unit,'bare_triple':g['original'],'geometry_sha256':record['geometry_check']['original_geometry_sha256'],
                 'geometry_reference':ref,'certificate_reference':record['certificate'],'model':model,'nodes':nodes,
                 'geometry_acceptance':'EXACT_COMPLETE_EARLY_VERIFIER_IDENTITY_BOUND',
                 'source_binding_record':{'path':str(identity_path),'line':ordinal+1,'sha256':R.sha(raw)},
                 'source_refusals_preserved':sum(b['status']!='complete' for b in record['count_bindings'])}
            body=R.encoded(job)+b'\n';offset=jobs.tell();jobs.write(body)
            entries.append({'ordinal':ordinal,'id':idx,'geometry_sha256':job['geometry_sha256'],'offset':offset,'bytes':len(body),
                            'sha256':R.sha(body),'node_ids':[f"{unit}:{idx}:{n['kind']}" for n in nodes]})
            kinds.update(n['role'] for n in nodes)
    R.need(seen==expected,'Omitted early identity')
    inputs.finish()
    sources.extend({'path':str(inputs.root/name),**binding} for name,binding in inputs.used.items())
    for p in sources:R.check_pin(p,deadline)
    result={'schema':R.SCHEMA,'kind':'manifest','status':'FROZEN_RECOUNT_JOBS','unit':unit,'stream':'complete-used-early-terminals',
            'input_root':str(args.root.resolve()),'expected_record_ids':sorted(expected),'records':entries,
            'selection_complete':True,'index_complete':True,'pending_index_ids':[],
            'jobs':R.file_pin(jobs_path,deadline),'inputs':list({p['path']:p for p in sources}.values()),
            'wrapper_sha256':R.sha(Path(R.__file__).read_bytes()),'indexer':R.file_pin(Path(__file__),deadline),
            'source_verification':R.file_pin(args.verification,deadline),'site_role_counts':dict(kinds),
            'new_counts_performed':0,'ordinary_positive_proof_still_requires_fresh_counts':True}
    with output.open('x') as stream:json.dump(result,stream,indent=2,sort_keys=True);stream.write('\n')
    print(json.dumps({'status':result['status'],'unit':unit,'records':len(entries),'sites':sum(kinds.values())}))


if __name__=='__main__':
    main()
