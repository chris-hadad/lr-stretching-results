#!/usr/bin/env python3
"""Fresh, serial q8 scalar regeneration with exact comparison to isolated accepted rows."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import mmap
from pathlib import Path
import struct
import time

from replay import (A17, C3, H8IDX, PRO33, add_toolchain_arguments, binary,
                    cancel_pool, check_cancelled, digest, fresh_json, install_signal_handlers,
                    prepare_roots, refuse_optimized, require, run_one,
                    stop_active_children, validate_toolchain, verify_assets)

COUNT = 6958562
STEP = 16384
HERE = Path(__file__).resolve().parent


def check_shard(path, begin, end, rhs, offsets):
    rows = 0
    with path.open() as stream:
        for tid in range(begin, end):
            line = stream.readline()
            require(bool(line), 'missing regenerated scalar row '+str(tid))
            row = json.loads(line)
            a = struct.unpack_from('<Q', offsets, 8*tid)[0]
            b = struct.unpack_from('<Q', offsets, 8*(tid+1))[0]
            require(a < b <= len(rhs), 'invalid isolated accepted scalar offset')
            accepted = rhs[a:b].split()
            require(len(accepted) == 3, 'malformed isolated accepted scalar row')
            require(row['type_id'] == tid and row['index'] == int(accepted[1]) and
                    row['alpha'] == accepted[2].decode() and accepted[0] == str(tid).encode(),
                    'regenerated scalar/index/type mismatch at '+str(tid))
            require(row['control'] == 'none' and row['covectors'] == 2 and
                    row['spread_alpha'] == row['alpha'] and row['proper_terms'] == 254,
                    'incomplete independent scalar checks at '+str(tid))
            rows += 1
        require(not stream.readline(), 'regenerated scalar tail')
    return rows


def produce_range(args,checker,phase,begin,end):
    generated=phase/f'{begin:07d}-{end:07d}.jsonl'
    receipt=phase/f'{begin:07d}-{end:07d}.process.json'
    require(not generated.is_symlink() and not receipt.is_symlink(),
            'q8 range output symlink refused')
    if generated.exists() or receipt.exists():
        require(generated.is_file() and receipt.is_file(), 'unadmitted partial q8 scalar output')
        record=json.loads(receipt.read_text())
        result=record['result']
        require(record['status']=='COMPUTED_EXACT_Q8_RHS_SHARD_REQUIRES_ADMISSION', 'existing q8 producer receipt')
    else:
        result=run_one([checker,args.asset_root/C3/'U02/DATA',args.asset_root/PRO33,
                        args.asset_root/H8IDX,begin,end,generated,8192,'dual','none'],
                       receipt,'COMPUTED_EXACT_Q8_RHS_SHARD_REQUIRES_ADMISSION',120)
    require((result['begin'],result['end'],result['types'])==(begin,end,end-begin),'q8 scalar child range')
    return result


def main():
    refuse_optimized()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asset-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sample', action='store_true', help='one 16,384-type calibration with no coverage credit')
    parser.add_argument('--workers', type=int, choices=[1,2], default=1)
    add_toolchain_arguments(parser)
    args = parser.parse_args()
    validate_toolchain(args)
    args.asset_root,args.output=prepare_roots(args.asset_root,args.output)
    install_signal_handlers()
    try:
        replay(args)
    except BaseException:
        stop_active_children()
        raise


def replay(args):
    verify_assets(args.asset_root, 'h8')
    verify_assets(args.asset_root, 'c2-field')
    if not args.sample:
        h8 = json.loads((args.output/'h8/COMPLETE.json').read_text())
        require(h8['status'] == 'PASS_COMPLETE_H8_REPLAY' and h8['types'] == 1988979 and
                h8['slots'] == 19271753, 'own complete lower h8 proof required')
        require((args.output/'h8/LOWER-7.txt').is_file(), 'missing own final lower token')
    phase = args.output/('q8-rhs-sample' if args.sample else 'q8-rhs')
    require(not phase.is_symlink(), 'q8 phase symlink refused')
    if phase.exists():
        require(not (phase/'COMPLETE.json').exists() and not (phase/'SAMPLE.json').exists(), 'q8 replay already complete')
    checker = binary(args.output, 'rhs-range', 'rhs_range_v1.cpp', args)
    if not phase.exists():phase.mkdir()
    rhsfile = args.asset_root/A17/'full-rhs.tsv'
    offsetfile = args.asset_root/A17/'full-rhs.offsets'
    with rhsfile.open('rb') as rhs_stream, offsetfile.open('rb') as offset_stream:
        rhs = mmap.mmap(rhs_stream.fileno(), 0, access=mmap.ACCESS_READ)
        offsets = mmap.mmap(offset_stream.fileno(), 0, access=mmap.ACCESS_READ)
        require(len(offsets) == 8*(COUNT+1) and struct.unpack_from('<Q', offsets, 8*COUNT)[0] == len(rhs),
                'isolated accepted scalar population')
        end_domain = STEP if args.sample else COUNT
        cursor = compared = 0
        total_child_seconds = 0.0
        spans=[(begin,min(begin+STEP,end_domain)) for begin in range(0,end_domain,STEP)]
        batches=[[span] for span in spans] if args.workers==1 else [spans[i:i+2] for i in range(0,len(spans),2)]
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            try:
                for batch in batches:
                    check_cancelled()
                    futures=[pool.submit(produce_range,args,checker,phase,begin,end) for begin,end in batch]
                    for (begin,end),future in zip(batch,futures):
                        check_cancelled()
                        require(begin==cursor,'q8 scalar range gap')
                        result=future.result()
                        check_cancelled()
                        generated=phase/f'{begin:07d}-{end:07d}.jsonl'
                        compared_receipt=phase/f'{begin:07d}-{end:07d}.compared.json'
                        started=time.monotonic()
                        rows=check_shard(generated,begin,end,rhs,offsets)
                        check_cancelled()
                        require(rows==end-begin,'q8 scalar comparison population')
                        comparison={'status':'PASS_FRESH_Q8_RHS_RANGE','begin':begin,'end':end,'rows':rows,
                                    'generated_sha256':digest(generated)}
                        if compared_receipt.exists():
                            old=json.loads(compared_receipt.read_text())
                            require(all(old.get(key)==value for key,value in comparison.items()),
                                    'existing q8 comparison changed')
                        else:
                            comparison['comparison_seconds']=time.monotonic()-started
                            fresh_json(compared_receipt,comparison)
                        cursor=end;compared+=rows;total_child_seconds+=result['total_seconds']
            except BaseException:
                cancel_pool(pool)
                raise
        require(cursor == end_domain and compared == end_domain,'incomplete regenerated q8 scalar union')
        if not args.sample:
            fresh_json(phase/'COMPLETE.json',
                       {'status':'PASS_COMPLETE_FRESH_Q8_RHS_COMPARISON','types':compared,
                        'ranges':(COUNT+STEP-1)//STEP,'child_seconds':total_child_seconds,
                        'accepted_rhs_sha256':digest(rhsfile)})
        else:
            fresh_json(phase/'SAMPLE.json',{'status':'PASS_Q8_SAMPLE_NO_COVERAGE_CREDIT','types':compared,
                                            'child_seconds':total_child_seconds})
        rhs.close();offsets.close()


if __name__ == '__main__':
    main()
