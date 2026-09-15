"""One direct outer-CLI owner for hard-bounded compute process groups."""
from contextlib import contextmanager
from dataclasses import asdict
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import sys
import tempfile
import time

from _runtime import STOP_SIGNALS, bind_command, run_contained, _group_exists


class Stopped(BaseException):
    def __init__(self, number):self.number=number


class Refused(RuntimeError):pass


def digest(path):
    with Path(path).open("rb") as stream:return hashlib.file_digest(stream,"sha256").hexdigest()


def save(path,value):
    with Path(path).open("x",encoding="utf-8") as stream:
        json.dump(value,stream,indent=2,sort_keys=True);stream.write("\n")


def _write_json_payload(stream,payload):
    if stream.write(payload)!=len(payload):
        raise OSError("Incomplete JSON temporary-file write")


def publish_json(path,value):
    """Publish a complete JSON record in an exclusively owned output directory.

    Serialization cannot expose a target. Failed writes retain their exclusive
    same-directory temporary file as evidence; only a flushed, closed record
    reaches the atomic rename. Existing records are never intentionally replaced.
    """
    path=Path(path)
    if os.path.lexists(path):raise FileExistsError(str(path))
    payload=(json.dumps(value,indent=2,sort_keys=True)+"\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(mode="wb",prefix="."+path.name+".",suffix=".tmp",dir=path.parent,delete=False) as stream:
        temporary=Path(stream.name)
        _write_json_payload(stream,payload)
        stream.flush();os.fsync(stream.fileno())
    if os.path.lexists(path):raise FileExistsError(str(path))
    os.rename(temporary,path)


@contextmanager
def handle_outer_signals():
    old={sig:signal.getsignal(sig) for sig in STOP_SIGNALS}
    def stop(number,frame):raise Stopped(number)
    try:
        for sig in STOP_SIGNALS:signal.signal(sig,stop)
        yield
    finally:
        mask=signal.pthread_sigmask(signal.SIG_BLOCK,set(old))
        try:
            for sig,handler in old.items():signal.signal(sig,handler)
        finally:signal.pthread_sigmask(signal.SIG_SETMASK,mask)


class Runner:
    def __init__(self,output,sources,*,native_limit=600,program_limit=900):
        self.output=Path(output);self.sources=dict(sources)
        self.limits={"native":native_limit,"program":program_limit}
        for value in self.limits.values():
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<=0:
                raise ValueError("Cumulative limits must be finite and positive")
        self.used={"native":0.0,"program":0.0};self.receipts=[];self.active=None
        (self.output/"jobs").mkdir(exist_ok=False);(self.output/"tmp").mkdir(exist_ok=False)
        self.env={name:os.environ[name] for name in ("HOME","USER","LOGNAME","LANG","LC_ALL") if name in os.environ}
        self.env.update(PATH=os.defpath+os.pathsep+"/opt/homebrew/bin",PYTHONDONTWRITEBYTECODE="1",PYTHONNOUSERSITE="1",
                        TMPDIR=str(self.output/"tmp"),OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1")
        save(self.output/"OUTER.json",{"pid":os.getpid(),"argv":sys.argv,"source_sha256":self.sources,"limits":self.limits})

    def bind(self,path):self.sources[str(Path(path).resolve())]=digest(path)

    def intact(self):
        return all(digest(path)==expected for path,expected in self.sources.items())

    def run(self,label,command,*,category="program",timeout=120,expected_code=0,expected_error=None,terminate_grace=0):
        if category not in self.limits:raise ValueError("Unknown compute category")
        cap=60 if category=="native" else 120
        if isinstance(timeout,bool) or not isinstance(timeout,(int,float)) or not math.isfinite(timeout) or not 0<timeout<=cap:
            raise ValueError("Per-child deadline exceeds the declared category bound")
        if isinstance(terminate_grace,bool) or not isinstance(terminate_grace,(int,float)) or not math.isfinite(terminate_grace) or terminate_grace<0 or timeout+terminate_grace>cap:
            raise ValueError("Termination grace exceeds the hard category bound")
        if self.used[category]+timeout+terminate_grace+2>self.limits[category]:
            raise Refused("Cumulative "+category+" budget admission refused")
        if not label or Path(label).name!=label:raise ValueError("Job label must be a simple basename")
        receipt_path=self.output/"jobs"/(label+".json")
        if receipt_path.exists():raise Refused("Job identity already used")
        command=[str(x) for x in command];start=time.monotonic();self.active=None
        binding=bind_command(command,cwd=str(self.output),env=self.env,source_sha256=self.sources)
        def acquired(pid):
            self.active=pid
            save(self.output/"jobs"/(label+".STARTED.json"),{"pid":pid,"pgid":pid,"outer_pid":os.getpid(),"argv":command,"category":category})
        try:
            result=run_contained(command,cwd=str(self.output),env=self.env,timeout_s=timeout,binding=binding,
                                 max_output_bytes=4*1024*1024,cleanup_timeout_s=2,terminate_grace_s=terminate_grace,on_start=acquired)
        except Stopped as stop:
            # Before acquisition or after protected cleanup: never signal a
            # possibly reused group. A live group is an explicit failed cleanup.
            elapsed=time.monotonic()-start
            clean=self.active is None or not _group_exists(self.active)
            record={"label":label,"status":"partial","reason":"outer_signal","signal":stop.number,"pid":self.active,
                    "elapsed_s":elapsed,"cleanup_verified":clean,"category":category,"argv":command}
            self.used[category]+=elapsed;self.receipts.append(record);save(receipt_path,record)
            self.active=None
            if not clean:raise Refused("Outer interruption did not establish child-group exit")
            raise
        record=asdict(result);record["stdout"]=result.stdout.decode("utf-8","replace");record["stderr"]=result.stderr.decode("utf-8","replace")
        record.update(label=label,category=category,expected_code=expected_code,expected_error=expected_error,outer_pid=os.getpid())
        self.used[category]+=result.elapsed_s;self.receipts.append(record);save(receipt_path,record);self.active=None
        if not result.cleanup_verified:raise Refused("Owned child cleanup not verified")
        if result.reason=="cancelled" and (result.detail or "").startswith("signal:"):
            raise Stopped(int(result.detail.split(":",1)[1]))
        expected_status="complete" if expected_code==0 else "error"
        if result.status!=expected_status or result.returncode!=expected_code or result.reason!=("exited" if expected_code==0 else "nonzero_exit"):
            raise Refused(label+" did not complete its exact execution contract: "+result.reason)
        if expected_error and expected_error not in record["stderr"]:
            raise Refused(label+" did not reach the intended semantic refusal")
        return record
