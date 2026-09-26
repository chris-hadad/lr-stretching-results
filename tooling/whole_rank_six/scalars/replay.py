#!/usr/bin/env python3
"""Portable exact c1 scalar replay, conditional on the lower analytic proofs.

The check-all mode authenticates the complete supplied q1..q8 cache and checks
every accepted q9 scalar. Full additionally rebuilds the cache and q8 index,
then freshly produces each q9 scalar before checking it. Neither mode proves
the supplied lower scalar tables are analytic truth; see README.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import time

from runtime import group_exists, run_owned, stop_group

HERE = Path(__file__).resolve().parent
TOTAL_TYPES = 8_947_541
TOTAL_ROWS = 27_230_728
Q8_JOIN_ROWS = 10_480_218
CACHE_FILES = 48
CACHE_BYTES = 1_488_841_394
LOWER_C3 = 'results/runs/SLR-PRO031-C3-VERIFY-20260916-001/data/U03-A05/DATA/CACHE'
LOWER_PRO33 = 'results/runs/SLR-PRO033-PACKET-20260916-001/science-restored-check/U07/DATA/COLLATION/merge-02-00.types'
LOWER_A17 = 'results/runs/SLR-ASTRA017-20260917-001/correction/full-q8/v2/output/full-rhs.tsv'
JOIN_PREFIX = 'results/runs/SLR-ASTRA015-20260917-001/q8/operator-data/join-'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load_json(path):
    return json.loads(path.read_text())


def dump_fresh(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def safe_file(root, relative):
    rel = Path(relative)
    need(not rel.is_absolute() and '..' not in rel.parts and relative == rel.as_posix(),
         'unsafe relative input: '+relative)
    path = root / rel
    need(path.resolve(strict=True).is_relative_to(root) and not path.is_symlink(),
         'input escapes root: '+relative)
    mode = path.stat().st_mode
    need(stat.S_ISREG(mode), 'input is not a regular file: '+relative)
    return path


def verify_files(root, specs):
    for relative, expected in specs.items():
        path = safe_file(root, relative)
        need(path.stat().st_size == expected['bytes'] and digest(path) == expected['sha256'],
             'changed input: '+relative)


def select_files(manifest, mode, range_index):
    distribution = manifest['distribution_files']
    lower = manifest['lower_files']
    cache_keys = [key for key in distribution if key.startswith('data/scalar-cache/')]
    type_keys = [f'data/geometry/q{k}.types' for k in range(1, 8)]
    q8_source = [LOWER_PRO33, LOWER_A17]
    jet_keys = [f'{LOWER_C3}/q{k}.jets' for k in range(1, 8)]
    need(len(cache_keys) == CACHE_FILES, 'exact 48-file supplied cache')
    need(len(manifest['q9_ranges']) == 455 and manifest['q9_ranges'][0]['begin'] == 0 and
         manifest['q9_ranges'][-1]['end'] == TOTAL_ROWS, 'full original range declaration')
    previous = 0
    for row in manifest['q9_ranges']:
        need(row['begin'] == previous and row['begin'] < row['end'], 'range gap, overlap, or empty range')
        previous = row['end']
    need(previous == TOTAL_ROWS, 'missing q9 tail')
    dkeys = set(cache_keys + type_keys)
    lkeys = set(q8_source + jet_keys)
    if mode in ('full', 'check-all', 'diagnostic'):
        dkeys.update(['data/geometry/atlas.txt', 'data/c1/q8-index.bin', 'data/c1/q9.rows'])
        dkeys.update(f'data/geometry/q{k}.lookup' for k in range(1, 8))
        rows = (manifest['q9_ranges'] if mode in ('full', 'check-all') else
                [manifest['q9_ranges'][range_index]])
        for row in rows:
            dkeys.update([row['header'], row['tsv']])
    if mode == 'full':
        lkeys.update(key for key in lower if key.startswith(JOIN_PREFIX) and key.endswith('.bin'))
        need(len([key for key in lkeys if key.startswith(JOIN_PREFIX)]) == 70,
             'exact 70 original q8 join shards')
    need(dkeys <= distribution.keys() and lkeys <= lower.keys(), 'undeclared required asset')
    return ({key:distribution[key] for key in sorted(dkeys)},
            {key:lower[key] for key in sorted(lkeys)})


def inspect_manifest(manifest):
    need(manifest['schema'] == 'pub-rank-six-c1-scalar-inputs-v1', 'input manifest schema')
    need(manifest['population_by_dimension'] == [0, 4, 36, 386, 4279, 39908,
                                                293306, 1651060, 6958562], 'type populations')
    need(sum(manifest['population_by_dimension']) == TOTAL_TYPES and
         manifest['q9_rows'] == TOTAL_ROWS, 'complete declared domains')
    need(len(manifest['distribution_files']) == 975 and len(manifest['lower_files']) == 79,
         'exact manifest file populations')
    need(len({row['header'] for row in manifest['q9_ranges']}) == 455 and
         len({row['tsv'] for row in manifest['q9_ranges']}) == 455,
         'duplicate original range path')
    for row in manifest['q9_ranges']:
        need(row['header'].endswith('/HEADER.txt') and row['tsv'].endswith('/exact.tsv') and
             row['header'].rsplit('/',1)[0] == row['tsv'].rsplit('/',1)[0],
             'original range file pairing')


def check_headers(root, ranges):
    for row in ranges:
        fields = (root / row['header']).read_text().split()
        need(fields == ['A19_RHS_V1', 'original', str(row['begin']), str(row['end'])],
             'exact original range header: '+row['header'])


def verify_sources():
    source_map = load_json(HERE/'SOURCE-MAP.json')
    need(source_map['schema'] == 'pub-rank-six-c1-scalar-source-map-v1' and
         len(source_map['files']) == 6, 'exact source map')
    verify_files(HERE, source_map['files'])
    return source_map


def environment(tmp):
    return {**os.environ, 'PYTHONDONTWRITEBYTECODE':'1', 'PYTHONOPTIMIZE':'',
            'TMPDIR':str(tmp), 'OMP_NUM_THREADS':'1', 'OPENBLAS_NUM_THREADS':'1'}


def available_bytes():
    """Conservative host headroom on the supported macOS/Linux POSIX hosts."""
    if sys.platform == 'darwin':
        result = subprocess.run(['/usr/bin/vm_stat'], capture_output=True, text=True,
                                timeout=5, check=True)
        match = re.search(r'page size of (\d+) bytes', result.stdout)
        need(match is not None, 'vm_stat page size')
        pages = {}
        for line in result.stdout.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                value = value.strip().rstrip('.')
                if value.isdecimal():
                    pages[key.strip()] = int(value)
        return int(match.group(1)) * sum(pages[key] for key in
                                         ('Pages free', 'Pages inactive', 'Pages speculative'))
    if sys.platform.startswith('linux'):
        match = re.search(r'^MemAvailable:\s+(\d+) kB$',
                          Path('/proc/meminfo').read_text(), re.MULTILINE)
        need(match is not None, 'Linux MemAvailable')
        return int(match.group(1)) * 1024
    raise RuntimeError('parallel headroom check unsupported on '+sys.platform)


def active_rss_bytes(pids):
    if not pids:
        return {}
    result = subprocess.run(['/bin/ps', '-o', 'pid=,rss=', '-p',
                             ','.join(map(str,pids))], capture_output=True,
                            text=True, timeout=5)
    need(result.returncode in (0,1), 'process RSS sample refused')
    measured = {}
    for line in result.stdout.splitlines():
        pid, kib = map(int,line.split())
        measured[pid] = kib * 1024
    return measured


def parse_single_json(path):
    text = path.read_text()
    decoder = json.JSONDecoder()
    value, end = decoder.raw_decode(text.lstrip())
    need(not text.lstrip()[end:].strip() and isinstance(value, dict),
         'native stdout must be exactly one JSON object: '+str(path))
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--distribution', type=Path, required=True,
                        help='versioned data root containing DATA.json and data/; checker sources ship beside this program')
    parser.add_argument('--lower-assets', type=Path, required=True,
                        help='isolated c2-c3/assets root with repository-relative source paths')
    parser.add_argument('--out', type=Path, required=True, help='fresh output directory')
    parser.add_argument('--mode', choices=('cache', 'check-all', 'full', 'diagnostic'), required=True)
    parser.add_argument('--range-index', type=int, help='0..454, diagnostic only')
    parser.add_argument('--workers', type=int, choices=range(1,9), default=1,
                        help='1..8 for check-all only; default serial')
    parser.add_argument('--cxx', default='c++')
    parser.add_argument('--gmp-prefix', type=Path)
    args = parser.parse_args()
    need(not sys.flags.optimize, 'Python assertions must be enabled')
    distribution = args.distribution.resolve(strict=True)
    lower = args.lower_assets.resolve(strict=True)
    out = args.out.resolve()
    need(distribution.is_dir() and lower.is_dir(), 'input roots must be directories')
    need(not out.exists() and out.parent.is_dir(), 'fresh output directory required')
    need(all(out != root and root not in out.parents and out not in root.parents
             for root in (distribution, lower, HERE)), 'output must be separate from input/source roots')
    need(args.range_index is None if args.mode != 'diagnostic' else
         args.range_index is not None and 0 <= args.range_index < 455,
         '--range-index is required only for one diagnostic range')
    need(args.workers == 1 or args.mode == 'check-all',
         'parallel workers are available only for complete check-all')
    need(shutil.which(args.cxx) is not None, 'C++ compiler unavailable')
    started = time.monotonic()
    manifest = load_json(HERE/'INPUTS.json')
    inspect_manifest(manifest)
    verify_sources()
    need(digest(distribution/'DATA.json') == manifest['distribution_manifest_sha256'],
         'versioned distribution manifest changed')
    distribution_specs, lower_specs = select_files(manifest,args.mode,args.range_index)
    verify_files(distribution,distribution_specs)
    verify_files(lower,lower_specs)
    ranges = manifest['q9_ranges'] if args.mode in ('full', 'check-all') else (
        [manifest['q9_ranges'][args.range_index]] if args.mode == 'diagnostic' else [])
    check_headers(distribution,ranges)
    authenticated_seconds = time.monotonic() - started
    out.mkdir()
    for name in ('bin','tmp','logs'):
        (out/name).mkdir()
    if args.mode == 'full':
        (out/'ranges').mkdir()
    records=[]
    status='FAILED_OR_PARTIAL'
    reason=None
    completed_rows=0
    completed_indices=[]
    monitor={'minimum_available_bytes':None,'peak_child_rss_bytes':0,
             'cleaned_process_groups':[]}

    def stop(signum, frame):
        raise InterruptedError('received signal '+str(signum))
    old_handlers = {sig:signal.signal(sig, stop) for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP)}

    def run(label, command, timeout, expected=None):
        stdout_path = out/'logs'/(label+'.stdout')
        stderr_path = out/'logs'/(label+'.stderr')
        with stdout_path.open('xb') as stdout, stderr_path.open('xb') as stderr:
            record = run_owned([str(part) for part in command], stdout=stdout, stderr=stderr,
                               timeout=timeout, env=environment(out/'tmp'))
        record.update(label=label,stdout_sha256=digest(stdout_path),stderr_sha256=digest(stderr_path))
        records.append(record)
        dump_fresh(out/'logs'/(label+'.process.json'),record)
        (out/'PROGRESS.json').write_text(json.dumps({'completed':len(records),'last':record},indent=2)+'\n')
        need(record['exit']==0, 'child refused: '+label+'; see '+str(stderr_path))
        if expected is not None:
            actual=parse_single_json(stdout_path)
            for key,value in expected.items():
                need(actual.get(key)==value,'unexpected native result '+label+' '+key)
            return actual
        return None

    def check_all_parallel(binary, cache, geometry, q8_index):
        """Main-thread bounded child schedule; fresh output gives no resume credit."""
        active={}
        completed={}
        next_index=0
        wall_start=time.monotonic()

        def sample_headroom():
            headroom=available_bytes()
            old=monitor['minimum_available_bytes']
            monitor['minimum_available_bytes']=headroom if old is None else min(old,headroom)
            need(headroom>=4*1024**3, 'parallel host headroom below 4 GiB')

        def launch(index):
            row=ranges[index]
            label=f'q9-{index:04d}-check'
            command=[str(part) for part in
                     (binary,'check',cache,geometry,q8_index,
                      distribution/'data/c1/q9.rows',row['begin'],row['end'],
                      distribution/row['tsv'],'none')]
            stdout_path=out/'logs'/(label+'.stdout')
            stderr_path=out/'logs'/(label+'.stderr')
            stdout=stdout_path.open('xb')
            try:
                stderr=stderr_path.open('xb')
            except BaseException:
                stdout.close()
                raise
            old_mask=signal.pthread_sigmask(signal.SIG_BLOCK,
                                            {signal.SIGINT,signal.SIGTERM,signal.SIGHUP})
            def restore_child_mask():
                # Popen inherits the parent's temporary launch mask. Restore
                # its prior mask before exec so TERM can stop the native child.
                signal.pthread_sigmask(signal.SIG_SETMASK,old_mask)
            try:
                try:
                    process=subprocess.Popen(command,stdout=stdout,stderr=stderr,
                                             start_new_session=True,env=environment(out/'tmp'),
                                             preexec_fn=restore_child_mask)
                except BaseException:
                    stdout.close();stderr.close()
                    raise
                active[process.pid]={'process':process,'index':index,'label':label,
                                     'argv':command,'stdout':stdout,'stderr':stderr,
                                     'stdout_path':stdout_path,'stderr_path':stderr_path,
                                     'started':time.monotonic()}
            finally:
                signal.pthread_sigmask(signal.SIG_SETMASK,old_mask)

        def finish(pid,item):
            nonlocal completed_rows
            process=item['process']
            exit_code=process.wait()
            if group_exists(pid):
                stop_group(process)
                raise RuntimeError('q9 child left a live descendant: '+str(pid))
            item['stdout'].close();item['stderr'].close()
            del active[pid]
            record={'argv':item['argv'],'pid':pid,'exit':exit_code,
                    'seconds':time.monotonic()-item['started'],'child_waited':True,
                    'owned_process_group_exited':True,'label':item['label'],
                    'stdout_sha256':digest(item['stdout_path']),
                    'stderr_sha256':digest(item['stderr_path'])}
            records.append(record)
            dump_fresh(out/'logs'/(item['label']+'.process.json'),record)
            need(exit_code==0,'child refused: '+item['label']+'; see '+str(item['stderr_path']))
            result=parse_single_json(item['stdout_path'])
            row=ranges[item['index']]
            for key,value in {'status':'PASS_EXACT_ORIGINAL_SCALAR_CHECK',
                              'begin':row['begin'],'end':row['end'],
                              'rows':row['end']-row['begin'],
                              'proper_terms_each':511}.items():
                need(result.get(key)==value,'unexpected native result '+item['label']+' '+key)
            need(item['index'] not in completed,'duplicate q9 range completion')
            completed[item['index']]=result['rows']
            completed_indices.append(item['index'])
            completed_rows+=result['rows']
            (out/'PROGRESS.json').write_text(json.dumps(
                {'completed_q9_ranges':len(completed),'completed_q9_rows':completed_rows,
                 'last':record},indent=2)+'\n')

        try:
            while len(completed)<len(ranges):
                need(time.monotonic()-wall_start<=90_000,'complete q9 wall limit')
                sample_headroom()
                for pid,item in list(active.items()):
                    if item['process'].poll() is not None:
                        finish(pid,item)
                for pid,item in active.items():
                    need(time.monotonic()-item['started']<=600,
                         'q9 range timeout: '+item['label'])
                for pid,rss in active_rss_bytes(active).items():
                    monitor['peak_child_rss_bytes']=max(monitor['peak_child_rss_bytes'],rss)
                    need(rss<=3*1024**3,'q9 child RSS above 3 GiB: '+str(pid))
                while len(active)<args.workers and next_index<len(ranges):
                    # Drain an exit before refilling; a failed range never
                    # authorizes another launch in the same scheduler turn.
                    if any(item['process'].poll() is not None for item in active.values()):
                        break
                    sample_headroom()
                    launch(next_index)
                    next_index+=1
                if active:
                    time.sleep(0.25)
                elif next_index==len(ranges) and len(completed)<len(ranges):
                    raise RuntimeError('missing q9 range completion')
            need(next_index==455 and sorted(completed)==list(range(455)),
                 'incomplete or duplicate q9 range union')
            return sum(completed.values())
        finally:
            cleanup=[]
            for pid,item in list(active.items()):
                try:
                    stop_group(item['process'])
                    monitor['cleaned_process_groups'].append(pid)
                except BaseException as error:
                    cleanup.append((pid,repr(error)))
                item['stdout'].close();item['stderr'].close()
                del active[pid]
            if cleanup:
                raise RuntimeError('owned q9 groups did not exit: '+repr(cleanup))

    try:
        prefix = args.gmp_prefix
        if prefix is None and Path('/opt/homebrew/include/gmpxx.h').is_file():
            prefix = Path('/opt/homebrew')
        flags = [] if prefix is None else ['-I',str(prefix/'include'),'-L',str(prefix/'lib')]
        cxx = [args.cxx,'-std=c++17','-O3',*flags]
        cache_binary = out/'bin/production-cache-v2'
        run('compile-cache',cxx+[str(HERE/'src/production_cache_v2.cpp'),
                                 '-lgmpxx','-lgmp','-o',str(cache_binary)],180)
        if args.mode == 'full':
            join_binary = out/'bin/cache-prepare-v2'
            run('compile-joins',cxx+[str(HERE/'src/cache_prepare_v2.cpp'),
                                     '-lgmpxx','-lgmp','-o',str(join_binary)],180)
        if args.mode in ('full','check-all','diagnostic'):
            range_binary = out/'bin/production-range-v2'
            run('compile-range',cxx+[str(HERE/'src/production_range_v2.cpp'),
                                     '-lgmpxx','-lgmp','-o',str(range_binary)],180)
        geometry = distribution/'data/geometry'
        jets = lower/LOWER_C3
        type8 = lower/LOWER_PRO33
        scalar8 = lower/LOWER_A17
        supplied_cache = distribution/'data/scalar-cache'
        cache = supplied_cache
        if args.mode == 'full':
            cache = out/'cache-new'
            run('build-cache',[cache_binary,'build',geometry,jets,type8,scalar8,'FULL',cache,'none'],300,
                {'status':'PASS_STREAMED_EXACT_CACHE_BUILD','full':True,
                 'types':TOTAL_TYPES,'files':CACHE_FILES,'total_disk_bytes':CACHE_BYTES})
        for command_mode, label, expected_status in (
            ('check-alpha','check-alpha','PASS_STREAMED_EXACT_CACHE_ALPHA_CHECK'),
            ('check-weight','check-weight','PASS_STREAMED_EXACT_CACHE_WEIGHT_CHECK')):
            run(label,[cache_binary,command_mode,geometry,jets,type8,scalar8,'FULL',cache,'none'],300,
                {'status':expected_status,'full':True,'types':TOTAL_TYPES,
                 'files':CACHE_FILES,'total_disk_bytes':CACHE_BYTES})
        if args.mode == 'full':
            cache_keys=sorted(key for key in distribution_specs if key.startswith('data/scalar-cache/'))
            need(len(cache_keys)==CACHE_FILES, 'complete cache byte comparison')
            for key in cache_keys:
                regenerated=cache/Path(key).name
                need(regenerated.is_file() and not regenerated.is_symlink() and
                     regenerated.stat().st_size==distribution_specs[key]['bytes'] and
                     digest(regenerated)==distribution_specs[key]['sha256'],
                     'rebuilt cache differs: '+key)
            join_keys=sorted(key for key in lower_specs if key.startswith(JOIN_PREFIX))
            join_list=out/'q8-join-list.txt'
            join_list.write_text(''.join(str(lower/key)+'\n' for key in join_keys))
            q8_index=out/'q8-index-new.bin'
            run('rebuild-q8-index',[join_binary,'sort-joins',join_list,q8_index,Q8_JOIN_ROWS],300,
                {'status':'PASS_REUSABLE_Q8_LOOKUP','records':Q8_JOIN_ROWS,
                 'source_files':70,'bytes':Q8_JOIN_ROWS*12})
            need(digest(q8_index)==distribution_specs['data/c1/q8-index.bin']['sha256'],
                 'rebuilt original q8 index differs')
        else:
            q8_index=distribution/'data/c1/q8-index.bin'
        if args.mode=='check-all' and args.workers>1:
            check_all_parallel(range_binary,cache,geometry,q8_index)
        else:
            for index,row in enumerate(ranges):
                label=(f'q9-{index:04d}' if args.mode in ('full','check-all') else
                       f'diagnostic-{args.range_index:04d}')
                exact=distribution/row['tsv']
                if args.mode=='full':
                    exact=out/'ranges'/f'r{index:04d}.tsv'
                    run(label+'-produce',[range_binary,'produce',cache,geometry,q8_index,
                                          distribution/'data/c1/q9.rows',row['begin'],row['end'],
                                          exact,'none'],600,
                        {'status':'PASS_EXACT_ORIGINAL_SCALAR_RANGE','begin':row['begin'],
                         'end':row['end'],'rows':row['end']-row['begin'],
                         'proper_terms_each':511})
                    supplied=distribution_specs[row['tsv']]
                    need(exact.stat().st_size==supplied['bytes'] and
                         digest(exact)==supplied['sha256'],
                         'fresh producer differs from accepted exact TSV: '+row['tsv'])
                actual=run(label+'-check',[range_binary,'check',cache,geometry,q8_index,
                                           distribution/'data/c1/q9.rows',row['begin'],row['end'],
                                           exact,'none'],600,
                           {'status':'PASS_EXACT_ORIGINAL_SCALAR_CHECK','begin':row['begin'],
                            'end':row['end'],'rows':row['end']-row['begin'],
                            'proper_terms_each':511})
                if args.mode=='full':
                    need(exact.stat().st_size==supplied['bytes'] and
                         digest(exact)==supplied['sha256'],
                         'fresh exact TSV changed during checker: '+row['tsv'])
                completed_rows += actual['rows']
                completed_indices.append(index if args.mode!='diagnostic' else args.range_index)
                if args.mode in ('full','check-all') and (index+1)%10==0:
                    print('q9 ranges',index+1,'/455',flush=True)
        if args.mode in ('full','check-all'):
            need(completed_rows==TOTAL_ROWS and len(ranges)==455 and
                 sorted(completed_indices)==list(range(455)),
                 'incomplete q9 scalar regeneration')
        elif args.mode=='diagnostic':
            need(completed_rows==ranges[0]['end']-ranges[0]['begin'],
                 'incomplete diagnostic range')
        verify_files(distribution,distribution_specs)
        verify_files(lower,lower_specs)
        verify_sources()
        status={'cache':'PASS_FULL_LOWER_CACHE_SOURCE_EQUALITY_CONDITIONAL',
                'check-all':'PASS_COMPLETE_Q9_CHECK_FROM_AUTHENTICATED_LOWER_CACHE_CONDITIONAL',
                'full':'PASS_COMPLETE_Q9_PRODUCED_AND_CHECKED_FROM_REBUILT_LOWER_CACHE_CONDITIONAL',
                'diagnostic':'PASS_ONE_Q9_RANGE_DIAGNOSTIC_NO_COVERAGE_CREDIT'}[args.mode]
    except BaseException as error:
        reason=repr(error)
        raise
    finally:
        for sig, handler in old_handlers.items():
            signal.signal(sig,handler)
        result={'schema':'pub-rank-six-c1-scalar-replay-v1','status':status,
                'mode':args.mode,'reason':reason,'completed_q9_rows':completed_rows,
                'completed_q9_ranges':len(completed_indices),
                'completed_q9_range_indices':sorted(completed_indices),
                'requested_workers':args.workers,
                'monitor':monitor,
                'lower_analytic_truth_verified_here':False,
                'requires':'Complete c3 q1..q7 analytic and H8/q8 scalar replay from the isolated lower package',
                'input_manifest_sha256':digest(HERE/'INPUTS.json'),
                'source_map_sha256':digest(HERE/'SOURCE-MAP.json'),
                'initial_authentication_seconds':authenticated_seconds,
                'total_seconds':time.monotonic()-started,
                'commands':records,
                'all_recorded_groups_exited':bool(records) and
                    all(r['owned_process_group_exited'] for r in records)}
        (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(status)

if __name__ == '__main__':
    main()
