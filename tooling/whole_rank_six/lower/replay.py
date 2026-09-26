#!/usr/bin/env python3
"""Portable, serial exact replay of accepted rank-six c2/c3 numerical inputs.

All campaign data are inert, hash-bound external assets under --asset-root.
This program compiles only the copied campaign-owned checkers in src/.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import struct
import subprocess
import sys
import threading
import time

from runtime import group_exists, stop_group

HERE = Path(__file__).resolve().parent
C3 = Path('results/runs/SLR-PRO031-C3-VERIFY-20260916-001/data')
A17 = Path('results/runs/SLR-ASTRA017-20260917-001/correction/full-q8/v2/output')
A15 = Path('results/runs/SLR-ASTRA015-20260917-001/q8/operator-data')
PRO33 = Path('results/runs/SLR-PRO033-PACKET-20260916-001/science-restored-check')
H8IDX = Path('results/runs/SLR-ASTRA017-20260917-001/h8/adapter-v5-final/indices')
H8_COUNTS = [0, 4, 36, 386, 4279, 39908, 293306, 1651060]
TOPOLOGY = [0, 42, 861, 11480, 111930, 850668, 5245786, 26978328]
CANCELLED = False
ACTIVE = {}
ACTIVE_LOCK = threading.Lock()


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fresh_json(path, value):
    check_cancelled()
    created = False
    try:
        with path.open('x') as stream:
            created = True
            json.dump(value, stream, sort_keys=True, indent=2)
            stream.write('\n')
        check_cancelled()
    except BaseException:
        if created:
            path.unlink(missing_ok=True)
        raise


def refuse_optimized():
    require(not sys.flags.optimize, 'Python assertions must be enabled; omit -O and PYTHONOPTIMIZE')


def distinct_roots(asset_root, output):
    """Resolve paths before any output creation and keep all three trees disjoint."""
    source = HERE.resolve()
    assets = asset_root.resolve()
    out = output.resolve()
    roots = (source, assets, out)
    for i, left in enumerate(roots):
        for right in roots[i+1:]:
            require(left != right and left not in right.parents and right not in left.parents,
                    'source, asset and output roots must be distinct and disjoint')
    require(assets.is_dir(), 'asset root required')
    require(out.is_dir() or (not out.exists() and out.parent.is_dir()),
            'output must be a directory or a fresh child of an existing directory')
    return assets, out


def prepare_roots(asset_root, output):
    assets, out = distinct_roots(asset_root, output)
    if not out.exists():
        out.mkdir()
    return assets, out


def add_toolchain_arguments(parser):
    parser.add_argument('--cxx', default='c++', help='C++17 compiler on PATH or an executable path')
    parser.add_argument('--gmp-prefix', type=Path, help='GMP installation prefix')
    parser.add_argument('--gmp-include', type=Path, help='GMP header directory')
    parser.add_argument('--gmp-lib', type=Path, help='GMP library directory')


def validate_toolchain(args):
    require(shutil.which(args.cxx) is not None, 'compiler not found or not executable: '+args.cxx)


def _received_signal(sig, _frame):
    # Python handles this in the main thread. A plain assignment cannot
    # reenter a lock held by interrupted launch or cancellation code.
    global CANCELLED
    CANCELLED = True


def install_signal_handlers():
    require(threading.current_thread() is threading.main_thread(), 'signal handlers require main thread')
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, _received_signal)


def check_cancelled():
    if CANCELLED:
        raise InterruptedError('replay cancelled')


def stop_active_children():
    """Main-thread cancellation waits for every exact session-owned group."""
    global CANCELLED
    CANCELLED = True
    with ACTIVE_LOCK:
        owned = list(ACTIVE.values())
    errors = []
    for child, stop_lock in owned:
        try:
            with stop_lock:
                stop_group(child)
        except Exception as exc:
            errors.append(repr(exc))
    with ACTIVE_LOCK:
        for child, _stop_lock in owned:
            if not group_exists(child.pid):
                ACTIVE.pop(child.pid, None)
    require(not errors, 'failed to stop owned process groups: '+', '.join(errors))


def cancel_pool(pool):
    global CANCELLED
    CANCELLED = True
    pool.shutdown(wait=False, cancel_futures=True)
    try:
        stop_active_children()
    finally:
        pool.shutdown(wait=True, cancel_futures=True)
    with ACTIVE_LOCK:
        require(not ACTIVE, 'owned children still registered after cancellation')


def available_memory():
    if sys.platform == 'darwin':
        stats = subprocess.run(['/usr/bin/vm_stat'], capture_output=True, text=True,
                               check=True, timeout=5).stdout
        page_match = re.search(r'page size of (\d+) bytes', stats)
        require(page_match, 'cannot read vm_stat page size')
        page = int(page_match.group(1))
        values = dict((key, int(number)) for key, number in
                      re.findall(r'^(Pages (?:free|inactive|speculative)):\s+(\d+)\.', stats, re.M))
        require(all('Pages '+name in values for name in ('free', 'inactive', 'speculative')),
                'cannot read complete vm_stat available-page categories')
        # Purgeable overlaps other categories in vm_stat; adding it counts pages twice.
        return page * sum(values['Pages '+name] for name in ('free', 'inactive', 'speculative'))
    with open('/proc/meminfo') as stream:
        found = re.search(r'^MemAvailable:\s+(\d+) kB', stream.read(), re.M)
    require(found, 'cannot measure available memory')
    return int(found.group(1)) * 1024


def run_one(argv, receipt, expected, timeout, receipt_extra=None):
    require(not receipt.exists(), 'fresh receipt required: '+str(receipt))
    check_cancelled()
    measured = available_memory()
    require(measured >= 4 * 2**30, 'less than 4 GiB measured available memory')
    started = time.monotonic()
    child = None
    stop_lock = threading.Lock()
    try:
        check_cancelled()
        child = subprocess.Popen([str(x) for x in argv], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, start_new_session=True,
                                 env={**os.environ, 'OMP_NUM_THREADS':'1', 'OPENBLAS_NUM_THREADS':'1',
                                      'PYTHONDONTWRITEBYTECODE':'1', 'PYTHONOPTIMIZE':''})
        with ACTIVE_LOCK:
            ACTIVE[child.pid] = (child, stop_lock)
        check_cancelled()
        deadline = started + timeout
        while True:
            check_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('hard timeout: '+str(argv))
            try:
                stdout, stderr = child.communicate(timeout=min(0.2, remaining))
                break
            except subprocess.TimeoutExpired:
                continue
        require(not group_exists(child.pid), 'child left a live process group: '+str(child.pid))
        check_cancelled()
    except BaseException:
        if child is not None:
            with stop_lock:
                stop_group(child)
        raise
    finally:
        if child is not None:
            with ACTIVE_LOCK:
                if not group_exists(child.pid):
                    ACTIVE.pop(child.pid, None)
    require(child.returncode == 0, 'child failed '+str(child.returncode)+': '+stderr[-2000:])
    parsed = json.loads(stdout.strip()) if expected else {'stdout':stdout.strip()}
    if expected:
        require(parsed.get('status') == expected, 'unexpected result: '+stdout[-2000:])
    check_cancelled()
    record = {'argv': [str(x) for x in argv], 'status': parsed.get('status'), 'result': parsed,
              'seconds': time.monotonic()-started, 'available_memory_before_bytes': measured,
              'stderr': stderr.strip(), 'child_waited': True,
              'owned_process_group_exited': True}
    if receipt_extra is not None:
        record.update(receipt_extra(parsed))
    fresh_json(receipt, record)
    return parsed


def verify_assets(root, group):
    manifest = json.loads((HERE/'ASSETS.json').read_text())
    require(manifest['schema'] == 'rank-six-c2-c3-assets-v1', 'asset manifest schema')
    for name in manifest['groups'][group]:
        check_cancelled()
        spec = manifest['files'][name]
        path = root/name
        require(path.is_file() and path.stat().st_size == spec['bytes'], 'missing or wrong-size asset: '+name)
        require(digest(path) == spec['sha256'], 'changed asset: '+name)
    return manifest


def source_closure(name):
    return {
        'geometry':['check_geometry.cpp'],
        'analytic':['check_analytic.cpp','check_geometry.cpp'],
        'field-original':['field_original_v1.cpp','operator.cpp'],
        'h8-check':['h8_check_range.cpp','check_geometry.cpp'],
        'rhs-range':['rhs_range_v1.cpp','q8_indexed_v3.cpp'],
    }[name]


def verify_sources(names=None):
    source_map=json.loads((HERE/'SOURCE-MAP.json').read_text())['entries']
    for name in (names or source_map):
        require(digest(HERE/'src'/name)==source_map[name]['portable_sha256'],
                'portable source changed: '+name)


def validated_analytic_ranges(ranges):
    require(isinstance(ranges, list) and len(ranges) == 65,
            'complete c3 analytic range roster required')
    seen = {k: 0 for k in range(1, 8)}
    prior_k = 1
    for item in ranges:
        require(isinstance(item, dict) and set(item) == {'k', 'begin', 'end'},
                'malformed analytic range')
        k, begin, end = (item[key] for key in ('k', 'begin', 'end'))
        require(all(type(x) is int for x in (k, begin, end)) and 1 <= k <= 7 and k >= prior_k,
                'invalid analytic range level')
        require(begin == seen[k] and begin < end <= H8_COUNTS[k],
                'analytic range gap, overlap or bound')
        seen[k] = end
        prior_k = k
    require(all(seen[k] == H8_COUNTS[k] for k in seen),
            'incomplete analytic range domain')
    return ranges


def validated_operator_shards(shards):
    require(len(shards) == 105, 'complete c2 operator shard roster')
    cursor = 0
    result = []
    for shard in shards:
        match = re.fullmatch(r'full-operator-(\d{8})-(\d{8})-001\.rows', shard.name)
        require(match, 'operator shard name')
        begin, end = map(int, match.groups())
        require(begin == cursor and 0 < end-begin <= 100000,
                'operator shard partition gap, overlap or bound')
        result.append((shard, begin, end))
        cursor = end
    require(cursor == 10480218, 'incomplete c2 operator domain')
    return result


def gmp_flags(args):
    prefix = args.gmp_prefix
    if prefix is None and args.gmp_include is None and args.gmp_lib is None and sys.platform == 'darwin':
        for candidate in (Path('/opt/homebrew/opt/gmp'), Path('/usr/local/opt/gmp')):
            if (candidate/'include/gmpxx.h').is_file() and (candidate/'lib').is_dir():
                prefix = candidate
                break
    include = args.gmp_include or (prefix/'include' if prefix else None)
    library = args.gmp_lib or (prefix/'lib' if prefix else None)
    flags = []
    if include is not None:
        require(include.is_dir(), 'GMP include directory missing: '+str(include))
        flags += ['-I', str(include.resolve())]
    if library is not None:
        require(library.is_dir(), 'GMP library directory missing: '+str(library))
        flags += ['-L', str(library.resolve())]
    return flags


def compile_binary(name, source, output, args):
    output.parent.mkdir(exist_ok=True)
    require(not output.exists() and not output.is_symlink(), 'fresh binary required: '+str(output))
    verify_sources(source_closure(name))
    argv = [args.cxx, '-std=c++17', '-O3', '-DNDEBUG']
    if name != 'geometry':
        argv += gmp_flags(args)
    argv += [str(HERE/'src'/source)]
    if name != 'geometry':
        argv += ['-lgmpxx', '-lgmp']
    argv += ['-o', str(output)]
    receipt=output.with_suffix('.compile.json')
    run_one(argv, receipt, None, 120)
    fresh_json(output.with_suffix('.binding.json'),
               {'schema':'rank-six-portable-binary-v1','binary_sha256':digest(output),
                'compile_receipt_sha256':digest(receipt),
                'sources':{source_name:digest(HERE/'src'/source_name) for source_name in source_closure(name)}})
    return output


def binary(out, name, source, args):
    target = out/'bin'/name
    require(not (out/'bin').is_symlink() and not target.is_symlink(),
            'compiled output must stay in its own directory')
    verify_sources(source_closure(name))
    if not target.exists():
        compile_binary(name, source, target, args)
    else:
        binding=json.loads(target.with_suffix('.binding.json').read_text())
        require(binding['binary_sha256']==digest(target) and
                binding['compile_receipt_sha256']==digest(target.with_suffix('.compile.json')) and
                all(binding['sources'][x]==digest(HERE/'src'/x) for x in source_closure(name)),
                'compiled binary/source binding changed: '+name)
    return target


def c3_core(args, out):
    verify_assets(args.asset_root, 'c3-core')
    data = args.asset_root/C3
    require(not (out/'c3-core').exists(), 'c3-core phase already occupied')
    verify_sources(['check_field.py'])
    geo = binary(out, 'geometry', 'check_geometry.cpp', args)
    phase = out/'c3-core'; phase.mkdir()
    for k in range(1,8):
        result = run_one([geo, 'topology', data/'U02/DATA', k, 0, TOPOLOGY[k]], phase/f'topology-q{k}.json', 'PASS_EXACT_TOPOLOGY_RANGE', 120)
        require((result['begin'],result['end']) == (0,TOPOLOGY[k]), 'topology coverage')
    op = run_one([geo, 'operator', data/'U02/DATA', 2999563], phase/'operator.json', 'PASS_EXACT_GEOMETRIC_OPERATOR', 120)
    require(op['rows']==2999563, 'operator coverage')
    field = run_one([sys.executable, '-B', HERE/'src/check_field.py', data, 2999563, phase, 'field'], phase/'field-process.json', 'PASS_EXACT_DECLARED_FIELD_ROWS', 180)
    require(field['rows']==2999563 and field['below_epsilon']==0 and field['zero_corrected_rows']==0, 'field coverage')
    fresh_json(phase/'COMPLETE.json', {'status':'PASS_COMPLETE_C3_CORE_REPLAY','topology_levels':list(range(1,8)),
                                      'operator_rows':op['rows'], 'field_rows':field['rows'], 'field_nnz':field['nonzeros']})


def c3_analytic(args, out):
    verify_assets(args.asset_root, 'c3-analytic')
    data = args.asset_root/C3
    require(not (out/'c3-analytic').exists(), 'c3-analytic phase already occupied')
    ranges = validated_analytic_ranges(json.loads((HERE/'RANGES.json').read_text())['c3_analytic'])
    checker = binary(out, 'analytic', 'check_analytic.cpp', args)
    phase=out/'c3-analytic';phase.mkdir()
    seen={k:0 for k in range(1,8)};types=slots=0
    for item in ranges:
        k,b,e=(item[key] for key in ('k','begin','end'))
        require(b==seen[k] and e>b and e<=H8_COUNTS[k], 'analytic range union')
        record=phase/f'q{k}-{b:07d}-{e:07d}.json'
        result=run_one([checker,data,k,b,e],record,'PASS_FRESH_COMPLETE_ANALYTIC_RANGE',120)
        require((result['k'],result['begin'],result['end'])==(k,b,e), 'analytic receipt range')
        seen[k]=e;types+=result['types'];slots+=result['complete_coefficients']
    require(all(seen[k]==H8_COUNTS[k] for k in seen), 'incomplete analytic domain')
    require(types==1988979 and slots==4706329, 'analytic population or slot mismatch')
    fresh_json(phase/'COMPLETE.json', {'status':'PASS_COMPLETE_C3_ANALYTIC_REPLAY','types':types,'coefficient_slots':slots,'level_ends':seen})


def c2_field(args,out):
    verify_assets(args.asset_root,'c2-field')
    require(not (out/'c2-field').exists(), 'c2-field phase already occupied')
    original=args.asset_root/A17
    shards=validated_operator_shards(sorted(original.glob('full-operator-*.rows')))
    checker=binary(out,'field-original','field_original_v1.cpp',args)
    phase=out/'c2-field';phase.mkdir()
    cursor=rows=nnz=originals=violations=0
    for shard,begin,end in shards:
        result=run_one([checker,args.asset_root/C3/'U02/DATA',args.asset_root/A15,
                        args.asset_root/PRO33/'U07/DATA/COLLATION/merge-02-00.types',shard,begin,end,
                        original/'full-rhs.tsv',original/'full-rhs.offsets',original/'full-cyclic-polish30.i64',
                        1000000000000,0,phase/f'{begin:08d}-{end:08d}.result.json'],
                       phase/f'{begin:08d}-{end:08d}.process.json','PASS_EXACT_ORIGINAL_FIELD_RANGE',120)
        require((result['begin'],result['end'],result['rows'])==(begin,end,end-begin),'field receipt range')
        cursor=end;rows+=result['rows'];nnz+=result['nnz'];originals+=result['original_multiplicity'];violations+=result['violations']
    require(cursor==10480218 and rows==10480218 and violations==0,'incomplete or failing c2 original field')
    fresh_json(phase/'COMPLETE.json', {'status':'PASS_COMPLETE_C2_ORIGINAL_FIELD_REPLAY','rows':rows,'nnz':nnz,
                                      'original_multiplicity':originals,'violations':violations,'ranges':len(shards)})


def h8_sources(root, phase):
    lines=[]
    for k in range(1,8):
        folder='U06/DATA/LAYER8' if k<=5 else 'U08/DATA/COMPLETE' if k==6 else 'U09/DATA/COMPLETE'
        lines.append(f'{k} {root/PRO33/folder/f"q{k}.layer8"} {root/H8IDX/f"q{k}.offsets"}\n')
    path=phase/'SOURCES.txt'
    with path.open('x') as stream:stream.writelines(lines)
    return path


def unique_json_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, 'duplicate H8 JSON field: '+key)
        value[key] = item
    return value


def reject_json_constant(value):
    raise RuntimeError('nonfinite H8 JSON value: '+value)


def read_h8_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_json_object,
                      parse_constant=reject_json_constant)


def h8_identity(checker, sources, lower):
    require(not sources.is_symlink() and not lower.is_symlink(),
            'H8 source list or lower token symlink refused')
    return {'controller_sha256':digest(HERE/'replay.py'),
            'runtime_sha256':digest(HERE/'runtime.py'),
            'asset_manifest_sha256':digest(HERE/'ASSETS.json'),
            'source_map_sha256':digest(HERE/'SOURCE-MAP.json'),
            'checker_sha256':digest(checker),
            'checker_binding_sha256':digest(checker.with_suffix('.binding.json')),
            'source_list_sha256':digest(sources),
            'lower_token_sha256':digest(lower)}


def h8_argv(checker, asset_root, sources, lower, rows, k, begin, end):
    return [str(x) for x in (checker,asset_root/C3,sources,lower,rows,'verify',k,begin,end,
                             'none',H8_COUNTS[k])]


def h8_lower_contents(through):
    return f'A17_CERTIFIED_LOWER {through}\n'+''.join(
        f'{j} {H8_COUNTS[j]}\n' for j in range(1,through+1))


def valid_elapsed(value):
    if type(value) not in (int, float) or value < 0:
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def validate_h8_rows(rows, asset_root, k, begin, end):
    """Check every emitted field against the manifest-verified checker inputs."""
    slots = math.comb(7,k-1)
    data = asset_root/C3/'U02/DATA'
    row_hash = hashlib.sha256()
    points = 0
    fields = {'k','id','index','numerator_points','new_slots','determining_sites',
              'unused_sites','proper_children','prepare_seconds','check_seconds'}
    with rows.open('rb') as output, (data/f'q{k}.types').open('rb') as types, \
            (asset_root/C3/'NUMERATORS'/f'q{k}.nidx').open('rb') as offsets:
        types.seek(73*begin)
        offsets.seek(8*begin)
        previous = offsets.read(8)
        require(len(previous)==8, 'H8 numerator offset missing')
        previous = struct.unpack('<Q',previous)[0]
        for expected_id in range(begin,end):
            check_cancelled()
            line = output.readline()
            require(line.endswith(b'\n') and len(line)<=4096,
                    'H8 row missing, unterminated or oversized')
            row_hash.update(line)
            try:
                row = json.loads(line.decode('utf-8'), object_pairs_hook=unique_json_object,
                                 parse_constant=reject_json_constant)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError('invalid H8 row JSON') from exc
            require(type(row) is dict and set(row)==fields, 'H8 row fields')
            type_record = types.read(73)
            next_offset = offsets.read(8)
            require(len(type_record)==73 and len(next_offset)==8,
                    'H8 type or numerator input missing')
            next_offset = struct.unpack('<Q',next_offset)[0]
            require(next_offset>=previous, 'H8 numerator offset order')
            expected = {'k':k, 'id':expected_id, 'index':type_record[0],
                        'numerator_points':next_offset-previous,
                        'new_slots':slots, 'determining_sites':slots,
                        'unused_sites':2, 'proper_children':(1<<k)-2}
            require(all(type(row[key]) is int and row[key]==value
                        for key,value in expected.items()),
                    'H8 row identity or exact count')
            require(valid_elapsed(row['prepare_seconds']) and valid_elapsed(row['check_seconds']),
                    'H8 row elapsed value')
            points += next_offset-previous
            previous = next_offset
        require(output.readline()==b'', 'H8 rows exceed range')
    return {'sha256':row_hash.hexdigest(),'numerator_points':points}


def validate_h8_result(result, k, begin, end, points):
    require(type(result) is dict and set(result)=={
        'status','k','begin','end','types','new_coefficient_slots',
        'determining_sites','unused_sites','numerator_points',
        'loading_seconds','checking_seconds','whole_LR_calls'}, 'H8 result fields')
    require(result['status']=='PASS_EXACT_H8_RANGE', 'H8 result status')
    expected = {'k':k,'begin':begin,'end':end,'types':end-begin,
                'new_coefficient_slots':(end-begin)*math.comb(7,k-1),
                'determining_sites':(end-begin)*math.comb(7,k-1),
                'unused_sites':2*(end-begin),'numerator_points':points,
                'whole_LR_calls':0}
    require(all(type(result[key]) is int and result[key]==value
                for key,value in expected.items()), 'H8 result coverage or count')
    require(valid_elapsed(result['loading_seconds']) and
            valid_elapsed(result['checking_seconds']), 'H8 result elapsed value')


def validate_completed_level(phase, k, checker, sources, asset_root):
    complete=read_h8_json(phase/f'k{k}-COMPLETE.json')
    require(complete['status']=='PASS_COMPLETE_H8_LEVEL' and complete['k']==k and
            complete['types']==H8_COUNTS[k] and complete['slots']==H8_COUNTS[k]*math.comb(7,k-1),
            'lower level population and slots')
    cursor=0
    for entry in complete['ranges']:
        begin,end=entry['begin'],entry['end']
        require(begin==cursor and end>begin, 'lower range union gap')
        require(entry['rows']==f'k{k}-{begin:07d}-{end:07d}.rows.jsonl' and
                entry['process']==f'k{k}-{begin:07d}-{end:07d}.process.json',
                'lower range output names')
        record=h8_existing_range(phase,k,begin,end,checker,sources,
                                 phase/f'LOWER-{k-1}.txt',asset_root)
        require(record is not None and entry==record, 'lower range byte drift')
        cursor=end
    require(cursor==H8_COUNTS[k], 'incomplete lower range union')
    return complete


def lower_token(phase, through, checker, sources, asset_root):
    path=phase/f'LOWER-{through}.txt'
    check_cancelled()
    created=False
    try:
        with path.open('x') as stream:
            created=True
            stream.write(f'A17_CERTIFIED_LOWER {through}\n')
            for k in range(1,through+1):
                check_cancelled()
                validate_completed_level(phase,k,checker,sources,asset_root)
                stream.write(f'{k} {H8_COUNTS[k]}\n')
        check_cancelled()
    except BaseException:
        if created:
            path.unlink(missing_ok=True)
        raise
    return path


def h8_existing_range(phase,k,begin,end,checker,sources,lower,asset_root):
    rows=phase/f'k{k}-{begin:07d}-{end:07d}.rows.jsonl'
    receipt=phase/f'k{k}-{begin:07d}-{end:07d}.process.json'
    require(not rows.is_symlink() and not receipt.is_symlink(), 'H8 range output symlink refused')
    if not rows.exists() and not receipt.exists():return None
    require(rows.is_file() and receipt.is_file(), 'unadmitted partial H8 output')
    require(lower.is_file() and lower.read_text()==h8_lower_contents(k-1),
            'H8 lower token changed')
    process=read_h8_json(receipt)
    require(type(process) is dict and process.get('status')=='PASS_EXACT_H8_RANGE' and
            process.get('child_waited') is True and
            process.get('owned_process_group_exited') is True,
            'existing H8 range process receipt')
    require(process.get('argv')==h8_argv(checker,asset_root,sources,lower,rows,k,begin,end),
            'existing H8 range command identity')
    binding=process.get('h8_binding')
    require(type(binding) is dict and binding.get('schema')=='rank-six-h8-output-v1' and
            type(binding.get('rows_sha256')) is str and
            binding.get('identity')==h8_identity(checker,sources,lower),
            'H8 range production binding missing or changed')
    summary=validate_h8_rows(rows,asset_root,k,begin,end)
    require(summary['sha256']==binding['rows_sha256'], 'H8 row bytes changed since production')
    validate_h8_result(process.get('result'),k,begin,end,summary['numerator_points'])
    return {'begin':begin,'end':end,'rows':rows.name,'rows_sha256':summary['sha256'],
            'process':receipt.name,'process_sha256':digest(receipt)}


def execute_h8_range(args,checker,phase,sources,lower,k,begin,end):
    record=h8_existing_range(phase,k,begin,end,checker,sources,lower,args.asset_root)
    if record is not None:return record
    rows=phase/f'k{k}-{begin:07d}-{end:07d}.rows.jsonl'
    receipt=phase/f'k{k}-{begin:07d}-{end:07d}.process.json'
    identity=h8_identity(checker,sources,lower)
    def production_binding(result):
        require(h8_identity(checker,sources,lower)==identity,
                'H8 checker, controller or input identity changed during range')
        summary=validate_h8_rows(rows,args.asset_root,k,begin,end)
        validate_h8_result(result,k,begin,end,summary['numerator_points'])
        return {'h8_binding':{'schema':'rank-six-h8-output-v1',
                              'rows_sha256':summary['sha256'],'identity':identity}}
    run_one(h8_argv(checker,args.asset_root,sources,lower,rows,k,begin,end),
            receipt,'PASS_EXACT_H8_RANGE',120,receipt_extra=production_binding)
    return h8_existing_range(phase,k,begin,end,checker,sources,lower,args.asset_root)


def h8_levels(args,out,upper):
    verify_assets(args.asset_root,'h8')
    phase=out/'h8'
    require(not phase.is_symlink(), 'H8 phase symlink refused')
    continuing=phase.exists()
    checker=binary(out,'h8-check','h8_check_range.cpp',args)
    if continuing:
        require(upper>=4 and not (phase/'COMPLETE.json').exists(), 'existing H8 phase is already complete or not continuable')
        sources=phase/'SOURCES.txt'
        lines=sources.read_text().splitlines()
        require(len(lines)==7, 'lower source list')
        for k,line in enumerate(lines,1):
            folder='U06/DATA/LAYER8' if k<=5 else 'U08/DATA/COMPLETE' if k==6 else 'U09/DATA/COMPLETE'
            require(line==f'{k} {args.asset_root/PRO33/folder/f"q{k}.layer8"} {args.asset_root/H8IDX/f"q{k}.offsets"}',
                    'lower source root or path drift')
        first_level=1
        for k in range(1,8):
            if not (phase/f'k{k}-COMPLETE.json').exists():break
            validate_completed_level(phase,k,checker,sources,args.asset_root)
            token=phase/f'LOWER-{k}.txt'
            expected=h8_lower_contents(k)
            require(token.is_file() and token.read_text()==expected,'completed lower token changed')
            first_level=k+1
        require(first_level>=4,'small H8 proof incomplete')
        lower=phase/f'LOWER-{first_level-1}.txt'
    if not continuing:
        phase.mkdir()
        sources=h8_sources(args.asset_root,phase)
        lower=lower_token(phase,0,checker,sources,args.asset_root)
        first_level=1
    for k in range(first_level,upper+1):
        seen=slots=0
        records=[]
        step=10000 if k>=6 else 4000 if k==5 else H8_COUNTS[k]
        spans=[(begin,min(begin+step,H8_COUNTS[k])) for begin in range(0,H8_COUNTS[k],step)]
        if args.workers==1:
            batches=[[span] for span in spans]
        else:
            batches=[spans[i:i+2] for i in range(0,len(spans),2)]
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            try:
                for batch in batches:
                    check_cancelled()
                    futures=[pool.submit(execute_h8_range,args,checker,phase,sources,lower,k,begin,end)
                             for begin,end in batch]
                    for (begin,end),future in zip(batch,futures):
                        check_cancelled()
                        require(begin==seen,'h8 contiguous range')
                        record=future.result()
                        check_cancelled()
                        require(record is not None,'missing H8 range record')
                        records.append(record)
                        seen=end;slots+=(end-begin)*math.comb(7,k-1)
            except BaseException:
                cancel_pool(pool)
                raise
        require(seen==H8_COUNTS[k] and slots==H8_COUNTS[k]*math.comb(7,k-1),'h8 complete level')
        fresh_json(phase/f'k{k}-COMPLETE.json',{'status':'PASS_COMPLETE_H8_LEVEL','k':k,'types':seen,
                                               'slots':slots,'ranges':records})
        lower=lower_token(phase,k,checker,sources,args.asset_root)
    if upper==7:
        require(sum(H8_COUNTS[1:])==1988979 and sum(H8_COUNTS[k]*math.comb(7,k-1) for k in range(1,8))==19271753,
                'h8 population')
        fresh_json(phase/'COMPLETE.json',{'status':'PASS_COMPLETE_H8_REPLAY','types':1988979,
                                         'slots':19271753,'level_tokens':[f'LOWER-{k}.txt' for k in range(1,8)]})


def main():
    refuse_optimized()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--asset-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--phase',required=True,choices=['c3-core','c3-analytic','c2-field','h8-small','h8-through4','h8-through5','h8-full'])
    parser.add_argument('--workers',type=int,choices=[1,2],default=1)
    add_toolchain_arguments(parser)
    args=parser.parse_args()
    validate_toolchain(args)
    args.asset_root,args.output=prepare_roots(args.asset_root,args.output)
    install_signal_handlers()
    try:
        {'c3-core':c3_core,'c3-analytic':c3_analytic,'c2-field':c2_field,
         'h8-small':lambda a,o:h8_levels(a,o,3),'h8-through4':lambda a,o:h8_levels(a,o,4),
         'h8-through5':lambda a,o:h8_levels(a,o,5),'h8-full':lambda a,o:h8_levels(a,o,7)}[args.phase](args,args.output)
    except BaseException:
        stop_active_children()
        raise

if __name__=='__main__':
    main()
