"""Complete serial transportation replay using the separate numerical bundle."""
from pathlib import Path
import argparse, hashlib, json, os, shlex, signal, subprocess, sys, time, uuid

ROOT = Path(__file__).resolve().parent


def group_exists(pgid):
    try:os.killpg(pgid,0)
    except ProcessLookupError:return False
    except PermissionError:return True
    return True


def stop_group(child):
    pgid=child.pid
    for sig in (signal.SIGTERM,signal.SIGKILL):
        if group_exists(pgid):
            try:os.killpg(pgid,sig)
            except ProcessLookupError:pass
        deadline=time.monotonic()+5
        while group_exists(pgid) and time.monotonic()<deadline:
            child.poll()
            time.sleep(0.05)
        if not group_exists(pgid):
            child.wait(timeout=0.2)
            return
    raise RuntimeError('Owned process group did not exit: '+str(pgid))


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def save(path,value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())


def run(argv,work,label,*,timeout=180,expected=0,contains=None,stdout=None):
    argv=list(map(str,argv));started=time.monotonic()
    output=Path(stdout) if stdout else work/(label+'.stdout.txt')
    error=work/(label+'.stderr.txt')
    caught=[None]
    def flag(signum,_frame):caught[0]=caught[0] or signum
    def check_signal():
        if caught[0]:raise KeyboardInterrupt('Interrupted by signal '+str(caught[0]))
    signals=(signal.SIGINT,signal.SIGTERM,signal.SIGHUP)
    previous={sig:signal.getsignal(sig) for sig in signals}
    child=None
    receipt=work/(label+'.run.json')
    receipt_owned=False
    try:
        for sig in signals:signal.signal(sig,flag)
        with output.open('x') as so,error.open('x') as se:
            try:
                check_signal()
                child=subprocess.Popen(argv,stdout=so,stderr=se,start_new_session=True,cwd=work)
                deadline=time.monotonic()+timeout
                while True:
                    check_signal()
                    remaining=deadline-time.monotonic()
                    if remaining<=0:raise subprocess.TimeoutExpired(argv,timeout)
                    try:
                        code=child.wait(timeout=min(0.2,remaining))
                        break
                    except subprocess.TimeoutExpired:continue
                if group_exists(child.pid):
                    raise RuntimeError('Owned child left a live descendant: '+str(child.pid))
                check_signal()
            except BaseException:
                if child is not None:stop_group(child)
                raise
        check_signal()
        elapsed=time.monotonic()-started
        record={'argv':argv,'returncode':code,'expected_returncode':expected,
                'seconds':elapsed,'child_waited':True,'stdout_sha256':sha(output),'stderr_sha256':sha(error)}
        check_signal()
        save(receipt,record)
        receipt_owned=True
        check_signal()
        if code!=expected or (contains is not None and contains not in error.read_text()):
            raise RuntimeError('Replay child refused or failed: '+label+'; see '+str(error))
        print(label+' completed in '+format(elapsed,'.3f')+' seconds',flush=True)
        check_signal()
        return elapsed
    finally:
        if caught[0] and receipt_owned:receipt.unlink(missing_ok=True)
        for sig,handler in previous.items():signal.signal(sig,handler)
        if caught[0] and sys.exc_info()[0] is None:
            raise KeyboardInterrupt('Interrupted by signal '+str(caught[0]))


def compile_source(source,destination,work):
    argv=[*shlex.split(os.environ.get('CXX','c++')),'-std=c++17','-O2',
          *shlex.split(os.environ.get('CPPFLAGS','')),source,'-o',destination,
          *shlex.split(os.environ.get('LDFLAGS','')),'-lgmpxx','-lgmp']
    return run(argv,work,'compile-'+destination.name,timeout=120)


def prepare(data,work):
    src=ROOT/'src'
    for source,binary in [('check_cover.cpp','cover'),('check_fields.cpp','fields'),
                          ('table_bv.cpp','bv'),('count_tables.cpp','count-tables')]:
        compile_source(src/source,work/binary,work)
    atlas=work/'atlas';atlas.mkdir()
    run([sys.executable,'-B',src/'atlas_replay.py',data/'atlas.json',atlas],work,'atlas')
    templates=work/'templates';templates.mkdir()
    run([sys.executable,'-B',src/'build_templates.py',atlas/'atlas.json',sha(atlas/'atlas.json'),templates],work,'templates')
    assert sha(templates/'templates.txt')==sha(data/'derived/templates.txt')
    for part,name in [('U','Q-UNFORCED-COMPLETE.raw.txt'),('F','Q-FORCED-COMPLETE.raw.txt')]:
        run([sys.executable,'-B',src/'encode_quadratic.py',data/'source/UNIT04/DATA'/name,part,work/f'quadratic-{part}.bin'],work,'quadratic-'+part)
        assert sha(work/f'quadratic-{part}.bin')==sha(data/f'derived/quadratic-{part}.bin')
    topology=work/'topology';topology.mkdir()
    run([sys.executable,'-B',src/'verify_topology.py',data/'local-certificate.json',topology],work,'topology')
    run([work/'bv',topology/'TABLE-CASES.txt'],work,'bv-values',stdout=work/'bv-values.txt')
    run([work/'bv',src/'CONTROLS.txt'],work,'bv-controls',stdout=work/'bv-controls.txt')
    run([work/'bv',src/'CONTROLS.txt','--omit-eighth-control'],work,'bv-omit-eighth',stdout=work/'bv-omit-eighth.txt')
    run([work/'count-tables',data/'baseline/INPUT.txt'],work,'baselines',stdout=work/'baselines.txt')


def batch_argv(job,data,work,output,replacements=None):
    replacements=replacements or {}
    pick=lambda key,path:replacements.get(key,path)
    part=job['part'];lo=job['lo'];hi=job['hi']
    inputs=[data/name for name in job['inputs']]
    if job['kind']=='cover':
        full,forced,cells,simplices,signs=inputs
        return [work/'cover',pick('full_state',full),pick('state',forced),part,lo,hi,
                pick('cells',cells),pick('simplices',simplices),pick('signs',signs),output]
    state,cubic=inputs
    return [work/'fields',pick('state',state),pick('templates',work/'templates/templates.txt'),
            pick('quadratic',work/f'quadratic-{part}.bin'),pick('cubic',cubic),part,lo,hi,output]


def negative_controls(data,work):
    """Run changed mathematical carriers through the actual compiled consumers."""
    import shutil,struct
    roster=json.loads((ROOT/'batches.json').read_text())
    cover=next(j for j in roster if j['kind']=='cover' and j['part']=='F' and j['lo']==0)
    field=next(j for j in roster if j['kind']=='fields' and j['part']=='F' and j['lo']==0)
    cover={**cover,'hi':1};field={**field,'hi':1}
    fixtures=work/'negative-inputs';fixtures.mkdir()
    paths={'templates':work/'templates/templates.txt','state':data/field['inputs'][0],
           'quadratic':work/'quadratic-F.bin','cubic':data/field['inputs'][1],
           'cells':data/cover['inputs'][2],'simplices':data/cover['inputs'][3],'signs':data/cover['inputs'][4]}
    specifications=[
        ('wrong-inverse','templates',1,0,lambda x:int(x)+1,'A3 inverse identity failed','fields'),
        ('template-overflow','templates',9,0,lambda x:10**12+1,'Template overflow bound exceeded','fields'),
        ('wrong-cut-sign','signs',0,1,lambda x:int(x)^1,'Independent strict cut signs disagree','cover'),
        ('degenerate-simplex','simplices',0,9,None,'Degenerate returned simplex roster','cover'),
        ('wrong-volume','cells',1,3,lambda x:int(x)+1,'Exact cell volume disagrees','cover'),
        ('vertex-overflow','state',1,0,lambda x:1000001,'Vertex coordinate outside exact bound','fields'),
    ]
    records=[]
    for label,key,line_id,column,change,message,kind in specifications:
        destination=fixtures/(label+'.txt')
        with paths[key].open() as incoming,destination.open('x') as output:
            for i,line in enumerate(incoming):
                if i==line_id:
                    row=line.split();row[column]=str(change(row[column])) if change else row[2]
                    line=' '.join(row)+'\n'
                output.write(line)
        records.append((label,key,destination,message,kind))
    for label,key,message in [('wrong-cubic','cubic','Cubic field identity mismatch'),
                              ('wrong-constant','quadratic','Complete low-field identity mismatch')]:
        destination=fixtures/(label+'.bin');shutil.copyfile(paths[key],destination)
        with destination.open('r+b') as target:
            target.seek(40);value,=struct.unpack('<q',target.read(8));target.seek(40);target.write(struct.pack('<q',value+1))
        records.append((label,key,destination,message,'fields'))
    destination=fixtures/'truncated-cubic.bin';shutil.copyfile(paths['cubic'],destination)
    with destination.open('r+b') as target:target.truncate(destination.stat().st_size-1)
    records.append(('truncated-cubic','cubic',destination,'Truncated or trailing binary field data','fields'))
    destination=fixtures/'missing-template-row.txt'
    with paths['templates'].open() as incoming,destination.open('x') as target:
        previous=None
        for line in incoming:
            if previous is not None:target.write(previous)
            previous=line
    records.append(('missing-template-row','templates',destination,'Missing or out-of-range integer','fields'))
    for label,key,destination,message,kind in records:
        out=work/('negative-'+label);out.mkdir()
        job=cover if kind=='cover' else field
        run(batch_argv(job,data,work,out,{key:destination}),work,'negative-'+label,
            timeout=30,expected=2,contains=message)
    save(work/'NEGATIVE-CONTROLS.json',{'status':'PASS','actual_consumer_refusals':len(records)})


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for transport replay')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--scratch',type=Path,required=True)
    parser.add_argument('--calibrate',action='store_true')
    parser.add_argument('--batch-budget',type=float,default=364.0,
                        help='Measured batch seconds or calibrated forecast above this stop with preserved outputs.')
    args=parser.parse_args()
    def interrupted(signum,frame):raise KeyboardInterrupt('Interrupted by signal '+str(signum))
    signals=(signal.SIGINT,signal.SIGTERM,signal.SIGHUP)
    previous={sig:signal.getsignal(sig) for sig in signals}
    try:
        for sig in signals:signal.signal(sig,interrupted)
        _replay(args)
    finally:
        for sig,handler in previous.items():signal.signal(sig,handler)


def _replay(args):
    data=args.data.resolve(strict=True)
    manifest=json.loads((ROOT/'DATA-MANIFEST.json').read_text())
    assert manifest['file_count']==len(manifest['files']) and manifest['bytes']==sum(r['bytes'] for r in manifest['files'].values())
    for name,rec in manifest['files'].items():
        path=data/name
        assert path.is_file() and path.stat().st_size==rec['bytes'] and sha(path)==rec['sha256'],name
    args.scratch.mkdir(parents=True,exist_ok=True)
    work=args.scratch.resolve()/('transport-replay-'+uuid.uuid4().hex[:12]);work.mkdir()
    save(work/'SOURCE-PINS.json',{str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file()})
    print('Replay output: '+str(work),flush=True)
    prepare(data,work)
    roster=json.loads((ROOT/'batches.json').read_text())
    assert len(roster)==52
    if args.calibrate:
        selected=[next(j for j in roster if j['kind']==kind and j['part']==part and j['lo']==0)
                  for kind in ('cover','fields') for part in ('F','U')]
    else:selected=roster
    seconds=0.0;measurements=[]
    for job in selected:
        label=f'{job["kind"]}-{job["part"]}-{job["lo"]:06d}-{job["hi"]:06d}'
        out=work/label;out.mkdir()
        elapsed=run(batch_argv(job,data,work,out),work,label,timeout=60)
        seconds+=elapsed;measurements.append({**job,'seconds':elapsed})
        if seconds>args.batch_budget:
            save(work/'BUDGET-STOP.json',{'complete':False,'measured_batch_seconds':seconds,'budget':args.batch_budget})
            raise RuntimeError('Batch budget exceeded; complete outputs preserved for repricing')
    if args.calibrate:
        forecast=sum(m['seconds']/(m['hi']-m['lo'])*({'U':591214,'F':41482}[m['part']]) for m in measurements)
        save(work/'CALIBRATION.json',{'complete_certificate':False,'samples':measurements,'forecast_batch_seconds':forecast,'batch_budget':args.batch_budget})
        print('CALIBRATION ONLY: forecast '+format(forecast,'.3f')+' batch seconds',flush=True)
        if forecast>args.batch_budget:raise RuntimeError('Calibrated forecast requires repricing')
        return
    negative_controls(data,work)
    run([sys.executable,'-B',ROOT/'src/join.py',data,work,ROOT],work,'complete-join',timeout=120)
    print((work/'RESULT.json').read_text(),flush=True)
    print('Complete replay outputs retained at '+str(work),flush=True)


if __name__ == '__main__':
    main()
