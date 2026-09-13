"""Freeze the first-two-unused-positive-grades rule for complete U02 checks.

This changes only independent held evaluation sites. Every original fitting
node, entire original hive, saturated chart and source polynomial is retained.
Original larger held observations remain supplemental source observations.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path

import recount_records as R

W = Path(__file__).resolve().parent
RULE = 'first two positive integers outside the unchanged determining-node set'


def replacement_grades(determining):
    R.need(all(type(t) is int for t in determining),'Nonintegral determining grade')
    held, t = [], 1
    while len(held) < 2:
        if t not in determining:
            held.append(t)
        t += 1
    return held


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    deadline = R.Deadline(100)
    original = W/'science/F2627-EARLY-U02-INDEX-001/result.json'
    manifest, _ = R.load_manifest(original,deadline)
    R.need(len(manifest['records']) == 169 and manifest['unit'] == 'U02','Wrong original cohort')
    source_verification = Path(manifest['source_verification']['path'])
    verification = R.decode(source_verification.read_bytes())
    ledger = Path(verification['identities']['path'])
    ledger_pin = R.file_pin(ledger,deadline)
    R.need(ledger_pin['sha256'] == verification['identities']['sha256'],'Changed persisted vector ledger')
    rows = ledger.read_bytes().splitlines(keepends=True)
    R.need(len(rows) == 169,'Wrong whole early identity ledger')
    entries, amendments, removed_ids = [], [], []
    output = args.output.resolve()
    jobs_path = output.with_suffix('.jobs.jsonl')
    with Path(manifest['jobs']['path']).open('rb') as old_jobs, jobs_path.open('xb') as out:
        for original_ordinal,(entry,raw) in enumerate(zip(manifest['records'],rows)):
            verified = R.decode(raw)
            R.need(entry['ordinal'] == original_ordinal and entry['id'] == verified['id']
                   and verified['unit'] == 'U02' and verified['status'] == 'PASS_CONDITIONAL_ON_RECORDED_COUNTS',
                   'Changed exact original source order/status')
            grades = replacement_grades(verified['determining_nodes'])
            if grades == verified['unused_hold_nodes']:
                continue
            job = R.read_job(old_jobs,entry)
            ref = job['source_binding_record']
            R.need(ref == {'path':str(ledger),'line':original_ordinal+1,'sha256':R.sha(raw)},
                   'Job detached from its original persisted polynomial')
            old_holds = [n for n in job['nodes'] if n['role'] == 'positive_holdout']
            R.need([n['grade'] for n in old_holds] == verified['unused_hold_nodes']
                   and len(old_holds) == 2,'Wrong exact old held-site roster')
            coefficients = [Fraction(x) for x in verified['coefficients']]
            R.need(all(x >= 0 for x in coefficients) and coefficients[0] == 1,
                   'Previously checked coefficient vector changed')
            holds = []
            for t in grades:
                value = sum(c*t**i for i,c in enumerate(coefficients))
                R.need(value.denominator == 1 and value > 0,'Nonintegral or empty held prediction')
                holds.append({'kind':'P'+str(t),'grade':t,'strict':False,
                    'stored':{'polynomial_expectation':int(value)},'role':'replacement_positive_holdout'})
            idx = entry['id']
            amendment = {'schema':'u02-exact-holdout-amendment-v1','parent_id':idx,
                'original_ordinal':original_ordinal,'original_job':entry,
                'geometry_sha256':job['geometry_sha256'],'actual_degree':verified['actual_degree'],
                'bare_triple':job['bare_triple'],'determining_nodes':verified['determining_nodes'],
                'removed_source_hold_nodes':[n['kind'] for n in old_holds],
                'new_hold_nodes':[n['kind'] for n in holds],
                'persisted_vector':{'ledger':ledger_pin,'line':original_ordinal+1,
                    'line_sha256':R.sha(raw),'coefficients':verified['coefficients']},
                'rule':RULE,'fresh_counts_still_required':True}
            job['nodes'],job['holdout_amendment'] = holds,amendment
            body = R.encoded(job)+b'\n'
            entries.append({'ordinal':len(entries),'id':idx,'geometry_sha256':job['geometry_sha256'],
                'offset':out.tell(),'bytes':len(body),'sha256':R.sha(body),
                'node_ids':[f'U02:{idx}:{n["kind"]}' for n in holds]})
            out.write(body)
            amendments.append(amendment)
            removed_ids += [f'U02:{idx}:{n["kind"]}' for n in old_holds]
    R.need(amendments and any(a['parent_id'] == 4042284 for a in amendments),'Missing measured hard parent')
    source_paths = [original,Path(manifest['jobs']['path']),ledger,source_verification,Path(__file__),Path(R.__file__)]
    sources = [R.file_pin(p,deadline) for p in source_paths]
    result = {'schema':R.SCHEMA,'kind':'manifest','status':'FROZEN_RECOUNT_JOBS','unit':'U02',
        'stream':'systematic-fresh-unused-U02-holds','input_root':manifest['input_root'],
        'expected_record_ids':sorted(r['id'] for r in entries),'records':entries,
        'selection_complete':True,'index_complete':True,'pending_index_ids':[],
        'jobs':R.file_pin(jobs_path,deadline),'inputs':sources,
        'wrapper_sha256':R.sha(Path(R.__file__).read_bytes()),'indexer':R.file_pin(Path(__file__),deadline),
        'source_verification':manifest['source_verification'],
        'site_role_counts':{'replacement_positive_holdout':2*len(entries)},'new_counts_performed':0,
        'ordinary_positive_proof_still_requires_fresh_counts':True,'amendment_rule':RULE,
        'original_index':R.file_pin(original,deadline),'amendments':amendments,
        'removed_original_node_ids':sorted(removed_ids),
        'scope':'All original determining sites remain required; only named held sites change. Original held observations/unfinished recounts remain supplemental.'}
    for p in sources:
        R.check_pin(p,deadline)
    with output.open('x') as f:
        json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'status':result['status'],'amended_parents':len(entries),'fresh_unused_sites':2*len(entries)}))


if __name__ == '__main__':
    main()
