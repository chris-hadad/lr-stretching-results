"""Fresh original first jets and restricted-addition controls, serially."""
from pathlib import Path
import argparse,json,os,shlex,signal,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent

def run(argv,timeout=180):
    p=subprocess.Popen(list(map(str,argv)),start_new_session=True)
    try:
        code=p.wait(timeout=timeout)
    except BaseException:
        try:os.killpg(p.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        try:p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            p.wait()
        raise
    if code:raise subprocess.CalledProcessError(code,argv)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--scratch',type=Path);args=ap.parse_args()
    def stop(signum,frame):raise KeyboardInterrupt('Interrupted')
    for sig in (signal.SIGINT,signal.SIGTERM):signal.signal(sig,stop)
    if args.scratch:args.scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='lr-linear-',dir=args.scratch) as temp:
        out=Path(temp);binary=out/'tree-gradient';data=json.loads((ROOT/'data/witness.json').read_text())
        case=out/'cases.txt';case.write_text(''.join(p['id']+' '+' '.join(map(str,p['boundary']))+'\n' for p in data['points']))
        run([*shlex.split(os.environ.get('CXX','c++')),'-std=c++17','-O2',*shlex.split(os.environ.get('CPPFLAGS','')),ROOT/'tree_gradient.cpp','-o',binary,*shlex.split(os.environ.get('LDFLAGS','')),'-lgmpxx','-lgmp'])
        jets=[]
        for base in [2,3]:
            d=out/str(base);d.mkdir();run([sys.executable,'-B',ROOT/'tree_data.py','build',d,base])
            result=d/'jets.json';run([binary,d/'TREES.txt',case,result,'correct']);jets.append(result)
        run([sys.executable,'-B',ROOT/'check_witness.py',*jets])
        run([sys.executable,'-B',ROOT/'two_row_controls.py'])
    print('PASS: complete first jets and exact restricted-addition controls; analytic scope is in the proofs')
if __name__=='__main__':main()
