#!/usr/bin/env python3
"""Hostile publication-boundary controls; these do not run new mathematics."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from unittest.mock import patch

import runner as runtime_owner
from runner import Runner,Refused,Stopped,digest,save,publish_json,handle_outer_signals
from _runtime import _OwnedPopen,_defer_cancellation,_cleanup
import verify


def absent(pid):
    try:os.kill(pid,0)
    except ProcessLookupError:return True
    return False


def probe(mode,output):
    """Replace numerical work only; exercise the real CLI finalization handlers."""
    original_writer=runtime_owner._write_json_payload
    original_rename=runtime_owner.os.rename
    child_record={}

    def state(stage,temporary,payload_length):
        save(output/"WRITE-STATE.json",{"stage":stage,"outer_pid":os.getpid(),"temporary":str(temporary),
             "payload_length":payload_length,"child_pid":child_record.get("pid"),
             "child_cleanup_verified":child_record.get("cleanup_verified")})

    def write_record(stream,payload):
        if b'"publication_control":' not in payload:
            return original_writer(stream,payload)
        if mode in ("partial-write","interrupt"):
            stream.write(payload[:64]);stream.flush();os.fsync(stream.fileno())
            state("partial-temporary-write",stream.name,len(payload))
            if mode=="partial-write":raise OSError("injected completion failure after partial temporary writing")
            time.sleep(30)
            raise AssertionError("Publication interruption probe was not interrupted")
        return original_writer(stream,payload)

    def rename_record(source,target):
        if mode=="rename-failure" and Path(target).name=="COMPLETE.json":
            state("before-rename",source,Path(source).stat().st_size)
            raise OSError("injected complete-record rename failure")
        return original_rename(source,target)

    def staged_reproduce(path,owner,cxx,gmp_prefix):
        nonlocal child_record
        child_record=owner.run("finalization-child",[str(Path(sys.executable).resolve()),"-c","pass"],timeout=2)
        if mode=="legacy-truncated-marker":
            (path/"COMPLETE.json").write_text('{"schema":')
            raise OSError("injected failure with a legacy truncated completion pathname")
        if mode=="invalid-marker-collision":
            (path/"COMPLETE.json").write_text('{"status":"not-complete"}\n')
        value={"publication_control":mode,"padding":"x"*65536}
        if mode=="serialization":value["unsupported"]={1,2}
        verify.publish_json(path/"COMPLETE.json",value)
        raise AssertionError("Fault-injection branch unexpectedly published a completion")

    with patch.object(runtime_owner,"_write_json_payload",write_record),patch.object(runtime_owner.os,"rename",rename_record),patch.object(verify,"reproduce",staged_reproduce):
        old=sys.argv
        try:
            sys.argv=[str(verify.PACKAGE/"verify.py"),"full","--output",str(output)]
            return verify.main()
        finally:sys.argv=old


def inspect_failure(output,mode,code,signum=None):
    aborted=json.loads((output/"ABORTED.json").read_text())
    child=json.loads((output/"jobs/finalization-child.json").read_text())
    if not child["cleanup_verified"] or not absent(child["pid"]):raise Refused("Finalization probe child survived")
    if verify.completion_published(output):raise Refused("A failed finalization is recognized as complete")
    legacy=mode in ("legacy-truncated-marker","invalid-marker-collision")
    if not legacy and (output/"COMPLETE.json").exists():raise Refused("Failure exposed a COMPLETE pathname")
    temporary=list(output.glob(".COMPLETE.json.*.tmp"))
    if mode=="serialization" and temporary:raise Refused("Serialization failure acquired a publication temporary")
    if mode in ("partial-write","interrupt","rename-failure"):
        if len(temporary)!=1:raise Refused("Failed publication did not retain its single temporary")
        state=json.loads((output/"WRITE-STATE.json").read_text())
        if Path(state["temporary"])!=temporary[0]:raise Refused("Temporary identity mismatch")
        size=temporary[0].stat().st_size
        if mode in ("partial-write","interrupt"):
            if not 0<size<state["payload_length"]:raise Refused("Partial-write control did not write a strict payload prefix")
            try:json.loads(temporary[0].read_text())
            except ValueError:pass
            else:raise Refused("Partial-write control unexpectedly retained a complete JSON record")
        elif size!=state["payload_length"]:
            raise Refused("Rename control did not retain the complete temporary record")
    if signum is not None:
        if code!=128+signum or aborted.get("signal")!=signum or aborted.get("status")!="interrupted":raise Refused("Finalization signal was not retained in abort evidence")
    elif code!=2 or aborted.get("status")!="refused":
        raise Refused("Finalization error was not retained in abort evidence")
    if mode=="invalid-marker-collision" and aborted.get("error")!="FileExistsError":raise Refused("Owned output collision did not retain abort evidence")
    return {"mode":mode,"exit_code":code,"signal":signum,"completion_path_absent":not (output/"COMPLETE.json").exists(),
            "valid_completion_absent":True,"abort_sha256":digest(output/"ABORTED.json"),"temporary_files":[{"name":p.name,"bytes":p.stat().st_size,"sha256":digest(p)} for p in temporary],
            "child_pid":child["pid"],"child_cleanup_verified":True}


def signal_case(output,signum):
    argv=[str(Path(sys.executable).resolve()),str(Path(__file__).resolve()),"--probe","interrupt","--output",str(output)]
    env=dict(os.environ);env["PYTHONDONTWRITEBYTECODE"]="1";env["PYTHONNOUSERSITE"]="1";env.pop("PYTHONPATH",None)
    owned=[];process=None;error=None;cleanup_error=None;record=None;started=time.monotonic()
    with (output.parent/(output.name+".stdout")).open("xb") as stdout,(output.parent/(output.name+".stderr")).open("xb") as stderr,_defer_cancellation() as pending:
        try:
            _OwnedPopen(owned,argv,cwd=str(output.parent),env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,start_new_session=True)
            process=owned[0]
            deadline=time.monotonic()+10
            while time.monotonic()<deadline:
                if pending:raise Refused("Publication control was itself interrupted")
                ready=output/"WRITE-STATE.json"
                if ready.exists():
                    try:
                        state=json.loads(ready.read_text())
                        break
                    except ValueError:pass
                time.sleep(0.01)
            else:raise Refused("Publication probe did not reach its partial-write boundary")
            if state["outer_pid"]!=process.pid or not state["child_cleanup_verified"] or not absent(state["child_pid"]):raise Refused("Publication probe ownership boundary mismatch")
            if (output/"COMPLETE.json").exists():raise Refused("Publication exposed its target before rename")
            os.kill(process.pid,signum);process.wait(timeout=10)
            record=inspect_failure(output,"interrupt",process.returncode,signum)
        except BaseException as failure:
            error=type(failure).__name__+": "+str(failure)
        finally:
            process=owned[0] if owned else None
            if getattr(process,"pid",None) is not None and process.returncode is None:
                cleanup_error=_cleanup(process,3.0,2.0)
    receipt={"signal":signal.Signals(signum).name,"outer_pid":getattr(process,"pid",None),"returncode":getattr(process,"returncode",None),
             "argv":argv,"result":record,"error":error,"cleanup_error":cleanup_error,"elapsed_s":time.monotonic()-started,
             "outer_absent":bool(process and absent(process.pid))}
    save(output.parent/(output.name+".json"),receipt)
    if pending:raise Stopped(pending[0][0])
    if error or cleanup_error or not receipt["outer_absent"]:raise Refused("Finalization interruption control failed")
    return receipt


def normal_publication(output):
    output.mkdir();target=output/"PUBLISHED.json";value={"complete_record":[1,2,3],"padding":"z"*4096}
    payload=(json.dumps(value,indent=2,sort_keys=True)+"\n").encode()
    original_writer=runtime_owner._write_json_payload;original_rename=runtime_owner.os.rename;observations=[]
    def staged_write(stream,content):
        if content!=payload:return original_writer(stream,content)
        middle=len(content)//2;stream.write(content[:middle]);stream.flush()
        if target.exists():raise Refused("Normal publication exposed a partial target")
        observations.append({"stage":"partial","target_absent":True})
        stream.write(content[middle:])
    def checked_rename(source,destination):
        if Path(destination)==target:
            if target.exists() or Path(source).parent!=target.parent or Path(source).read_bytes()!=payload:raise Refused("Rename did not receive an exclusive complete same-directory record")
            observations.append({"stage":"rename","complete_serialized_bytes":len(payload)})
        return original_rename(source,destination)
    with patch.object(runtime_owner,"_write_json_payload",staged_write),patch.object(runtime_owner.os,"rename",checked_rename):
        publish_json(target,value)
    if json.loads(target.read_text())!=value or list(output.glob(".PUBLISHED.json.*.tmp")):raise Refused("Normal atomic publication did not complete")
    before=target.read_bytes()
    try:publish_json(target,{"replacement":True})
    except FileExistsError:pass
    else:raise Refused("Atomic publication replaced existing evidence")
    if target.read_bytes()!=before:raise Refused("Existing published evidence changed")
    return {"status":"PASS","observations":observations,"published_sha256":digest(target),"existing_record_preserved":True}


def run_controls(output,verified_output=None):
    output=Path(output);output.mkdir(exist_ok=False);started=time.monotonic()
    owner=Runner(output,verify.code_sources(),native_limit=10,program_limit=100)
    normal=normal_publication(output/"normal")
    if verified_output is not None and not verify.completion_published(Path(verified_output)):
        raise Refused("A legitimate completed verification record was not recognized")
    failures=[]
    for mode in ("serialization","partial-write","rename-failure","legacy-truncated-marker","invalid-marker-collision"):
        case=output/mode
        receipt=owner.run(mode,[str(Path(sys.executable).resolve()),str(Path(__file__).resolve()),"--probe",mode,"--output",str(case)],timeout=10,terminate_grace=3,expected_code=2)
        failures.append(inspect_failure(case,mode,receipt["returncode"]))
    interrupted=[signal_case(output/("signal-"+signal.Signals(number).name),number) for number in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP,signal.SIGQUIT)]
    report={"schema":"three-letter-finalization-controls/v1","status":"PASS","normal_publication":normal,"failures":failures,"interruptions":interrupted,
            "valid_prior_completion_recognized":verified_output is not None,"resource_seconds":owner.used,"elapsed_s":time.monotonic()-started,"bare_LR_values":0}
    save(output/"FINALIZATION-CONTROLS.json",report);return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--verified-output",type=Path)
    parser.add_argument("--probe",choices=("serialization","partial-write","rename-failure","legacy-truncated-marker","invalid-marker-collision","interrupt"))
    args=parser.parse_args()
    if args.probe:return probe(args.probe,args.output.resolve())
    try:
        with handle_outer_signals():
            result=run_controls(args.output.resolve(),args.verified_output)
            print(json.dumps({"status":result["status"],"elapsed_s":result["elapsed_s"]}),flush=True)
        return 0
    except Stopped as stop:return 128+stop.number
    except BaseException as error:
        print("REFUSED: "+str(error),file=sys.stderr);return 2


if __name__=="__main__":raise SystemExit(main())
