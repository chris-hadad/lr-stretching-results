"""Portable serial replay of all finite bases; no provider code is executed."""
from pathlib import Path
import argparse, gzip, hashlib, json, os, shlex, shutil, signal, subprocess, sys, tempfile, time
ROOT=Path(__file__).resolve().parent

def group_exists(pgid):
    try:os.killpg(pgid,0)
    except ProcessLookupError:return False
    except PermissionError:return True
    return True

def stop_group(child):
    """Stop and reap this exact new session, including any surviving children."""
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

def run(args, timeout=1800, capture=False):
    argv=list(map(str,args))
    caught=[None]
    def flag(signum,_frame):caught[0]=caught[0] or signum
    signals=(signal.SIGINT,signal.SIGTERM,signal.SIGHUP)
    previous={sig:signal.getsignal(sig) for sig in signals}
    child=None
    try:
        for sig in signals:signal.signal(sig,flag)
        try:
            if caught[0]:raise KeyboardInterrupt('Interrupted by signal '+str(caught[0]))
            child=subprocess.Popen(argv,start_new_session=True,
                                   stdout=subprocess.PIPE if capture else None,
                                   stderr=subprocess.PIPE if capture else None,text=True)
            deadline=time.monotonic()+timeout
            while True:
                if caught[0]:raise KeyboardInterrupt('Interrupted by signal '+str(caught[0]))
                remaining=deadline-time.monotonic()
                if remaining<=0:raise subprocess.TimeoutExpired(argv,timeout)
                try:
                    stdout,stderr=child.communicate(timeout=min(0.2,remaining))
                    break
                except subprocess.TimeoutExpired:continue
            if group_exists(child.pid):
                raise RuntimeError('Owned child left a live descendant: '+str(child.pid))
            if caught[0]:raise KeyboardInterrupt('Interrupted by signal '+str(caught[0]))
        except BaseException:
            if child is not None:stop_group(child)
            raise
        if not capture and child.returncode:
            raise subprocess.CalledProcessError(child.returncode,args)
        return subprocess.CompletedProcess(args,child.returncode,stdout,stderr)
    finally:
        for sig,handler in previous.items():signal.signal(sig,handler)
        if caught[0] and sys.exc_info()[0] is None:
            raise KeyboardInterrupt('Interrupted by signal '+str(caught[0]))

def interrupted(signum, frame):
    raise KeyboardInterrupt('Interrupted by signal '+str(signum))

def main():
    if sys.flags.optimize:
        raise RuntimeError('Run with assertions enabled; omit -O and PYTHONOPTIMIZE')
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--quick',action='store_true');mode.add_argument('--full',action='store_true')
    ap.add_argument('--scratch',type=Path)
    args=ap.parse_args()
    signals=(signal.SIGINT,signal.SIGTERM,signal.SIGHUP)
    previous={sig:signal.getsignal(sig) for sig in signals}
    try:
        for sig in signals:signal.signal(sig,interrupted)
        _replay(args)
    finally:
        for sig,handler in previous.items():signal.signal(sig,handler)

def _replay(args):
    run([sys.executable,'-B',ROOT/'scalar_controls.py'])
    if args.scratch:args.scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='layered-triangle-',dir=args.scratch) as tmp:
        work=Path(tmp);top=work/'top';top.mkdir()
        run([sys.executable,'-B',ROOT/'top_strip.py',top])
        got=json.loads((top/'RESULT.json').read_text());expected=json.loads((ROOT/'data/top.json').read_text())
        assert got['fields']==expected['fields'] and got['slots']==324 and got['holdouts']==18
        if not args.full:
            print('PASS quick controls: top strip 324 slots / 18 holdouts; second and third strips not run')
            return
        sources=json.loads((ROOT/'SOURCE-MAP.json').read_text())
        pins={x['path']:x for x in sources['files']}
        for strip in ['second','third']:
            out=work/strip;out.mkdir()
            for p in sorted((ROOT/'data'/strip).glob('*.gz')):
                raw=p.read_bytes();pin=pins[str(p.relative_to(ROOT))]
                assert hashlib.sha256(raw).hexdigest()==pin['sha256']
                unpacked=gzip.decompress(raw)
                assert hashlib.sha256(unpacked).hexdigest()==pin['origin']['sources'][0]['sha256']
                (out/p.stem).write_bytes(unpacked)
        compiler=shlex.split(os.environ.get('CXX','c++'))
        flags=[]
        if shutil.which('pkg-config'):
            p=run(['pkg-config','--cflags','--libs','gmpxx'],timeout=30,capture=True)
            if p.returncode==0:flags=shlex.split(p.stdout)
        if not flags and sys.platform=='darwin' and not os.environ.get('CPPFLAGS') and not os.environ.get('LDFLAGS'):
            for prefix in (Path('/opt/homebrew/opt/gmp'),Path('/usr/local/opt/gmp')):
                if (prefix/'include/gmpxx.h').is_file() and (prefix/'lib').is_dir():
                    flags=['-I'+str(prefix/'include'),'-L'+str(prefix/'lib'),'-lgmpxx','-lgmp']
                    break
        if not flags:flags=['-lgmpxx','-lgmp']
        binary=work/'verify-strips'
        run([*compiler,'-std=c++17','-O2',*shlex.split(os.environ.get('CPPFLAGS','')),ROOT/'verify_strips.cpp','-o',binary,*shlex.split(os.environ.get('LDFLAGS','')),*flags])
        for strip,lo,hi,number,slots,holdouts in [('second',2,14,2,5382,78),('third',3,43,3,130626,246)]:
            result=work/(strip+'.json')
            run([binary,work/strip,lo,hi,result,number])
            value=json.loads(result.read_text())
            assert (value['slots'],value['holdouts'])==(slots,holdouts)
        original=(work/'third/FIELD-r03.txt').read_text();symbol=(work/'third/SYMBOLIC-r03.txt').read_text()
        variants={'changed_count':original.replace('0 1 17181','0 1 17182',1),'changed_coefficient':original.replace('0 0 3628800','0 0 3628801',1),'omitted_slot':original.replace('0 1 17181\n','',1),'false_degree':original.replace('FIELD_V1 3 10','FIELD_V1 3 9',1)}
        for label,value in variants.items():
            assert value!=original
            bad=work/label;bad.mkdir();(bad/'FIELD-r03.txt').write_text(value);(bad/'SYMBOLIC-r03.txt').write_text(symbol)
            p=run([str(binary),str(bad),'3','3',str(bad/'result.json'),'3'],timeout=10,capture=True)
            assert p.returncode==2 and p.stderr.strip(),label
        print('PASS complete finite bases: 136332 slots, 342 holdouts, 4 corruption refusals')
if __name__=='__main__':main()
