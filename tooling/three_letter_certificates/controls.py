#!/usr/bin/env python3
"""Targeted semantic and real outer-command interruption controls."""
import argparse
import csv
from fractions import Fraction
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

from runner import Runner,Refused,Stopped,digest,save,handle_outer_signals
from _runtime import _OwnedPopen,_defer_cancellation,_cleanup
from verify import PACKAGE,code_sources


def absent(pid):
    try:os.kill(pid,0)
    except ProcessLookupError:return True
    return False


def interrupt_probe(output,signum):
    probe_output=output/("outer-"+signal.Signals(signum).name)
    argv=[str(Path(sys.executable).resolve()),str(PACKAGE/"verify.py"),"_interrupt-probe","--output",str(probe_output)]
    env=dict(os.environ);env["PYTHONDONTWRITEBYTECODE"]="1";env["PYTHONNOUSERSITE"]="1";env.pop("PYTHONPATH",None)
    stdout=output/("outer-"+signal.Signals(signum).name+".stdout")
    stderr=output/("outer-"+signal.Signals(signum).name+".stderr")
    owner=[];process=None;ready=None;failure=None;cleanup_result=None;started=time.monotonic()
    with stdout.open("xb") as out,stderr.open("xb") as err,_defer_cancellation() as pending:
        try:
            _OwnedPopen(owner,argv,cwd=str(output),env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
            process=owner[0]
            deadline=time.monotonic()+10
            while time.monotonic()<deadline:
                if pending:raise Refused("Interruption control itself was interrupted")
                ready_path=probe_output/"PROBE-READY.json"
                if ready_path.exists():
                    try:ready=json.loads(ready_path.read_text());break
                    except json.JSONDecodeError:pass
                time.sleep(0.01)
            if ready is None:raise Refused("Outer CLI did not acquire its descendant probe")
            start_record=json.loads((probe_output/"jobs/interrupt-probe.STARTED.json").read_text())
            if start_record["outer_pid"]!=process.pid or start_record["pid"]!=ready["pid"] or ready["pgid"]!=ready["pid"]:
                raise Refused("Outer/leaf/group identity mismatch")
            if absent(ready["pid"]) or absent(ready["grandchild_pid"]):raise Refused("Probe was not live before the outer signal")
            os.kill(process.pid,signum)
            process.wait(timeout=10)
            for _ in range(200):
                if absent(ready["pid"]) and absent(ready["grandchild_pid"]):break
                time.sleep(0.01)
            aborted=json.loads((probe_output/"ABORTED.json").read_text())
            receipt=json.loads((probe_output/"jobs/interrupt-probe.json").read_text())
            if (process.returncode!=128+signum or aborted.get("signal")!=signum or not receipt.get("cleanup_verified")
                or not absent(ready["pid"]) or not absent(ready["grandchild_pid"]) or (probe_output/"COMPLETE.json").exists()):
                raise Refused("Actual outer-command interruption/descendant cleanup failed")
        except BaseException as error:
            failure=type(error).__name__+": "+str(error)
        finally:
            process=owner[0] if owner else None
            if getattr(process,"pid",None) is not None and process.returncode is None:
                cleanup_result=_cleanup(process,3.0,2.0)
            # A failed test must not leave the exact fixed probe alive. Signals
            # here are a recorded fallback and never count as passing evidence.
            if ready and (not absent(ready["pid"]) or not absent(ready["grandchild_pid"])):
                check=subprocess.run(["/bin/ps","-p",str(ready["pid"])+","+str(ready["grandchild_pid"]),"-o","pid=,pgid=,args="],capture_output=True,text=True,timeout=3)
                matched=False
                for line in check.stdout.splitlines():
                    parts=line.split(None,2)
                    if len(parts)==3 and int(parts[1])==ready["pgid"] and str(probe_output/"PROBE-READY.json") in parts[2]:matched=True
                if matched:
                    try:os.killpg(ready["pgid"],signal.SIGTERM);os.killpg(ready["pgid"],signal.SIGKILL)
                    except ProcessLookupError:pass
                    for _ in range(200):
                        if absent(ready["pid"]) and absent(ready["grandchild_pid"]):break
                        time.sleep(0.01)
                failure=failure or "Probe required fallback cleanup"
    record={"signal":signal.Signals(signum).name,"argv":argv,"outer_pid":getattr(process,"pid",None),"probe":ready,
            "returncode":getattr(process,"returncode",None),"error":failure,"fallback_cleanup_error":cleanup_result,
            "elapsed_s":time.monotonic()-started,"outer_and_descendants_absent":bool(process and absent(process.pid) and ready and absent(ready["pid"]) and absent(ready["grandchild_pid"])),
            "complete_marker_absent":not (probe_output/"COMPLETE.json").exists()}
    save(output/("interruption-"+signal.Signals(signum).name+".json"),record)
    if pending:raise Stopped(pending[0][0])
    if failure or cleanup_result or not record["outer_and_descendants_absent"]:raise Refused("Real interruption control failed: "+str(record))
    return record


def read_values(path):
    with path.open() as stream:return {int(row["type_id"]):row for row in csv.DictReader(stream,delimiter="\t")}


def verified_artifact(run,report,name):
    path=run/name
    if report["artifact_sha256"].get(name)!=digest(path):raise Refused("Completed-run artifact authentication failed: "+name)
    return path


def semantic_controls(output,runner,verified):
    report=json.loads((verified/"COMPLETE.json").read_text())
    if report.get("status")!="PASS" or report.get("types_reproduced")!=395657 or report.get("original_subsets")!=1149016 or report.get("field_rows")!=664539:
        raise Refused("A complete verified run is required for targeted semantic controls")
    if not all(digest(path)==expected for path,expected in report["source_sha256"].items()):raise Refused("Completed-run bound sources changed")
    checker=verified_artifact(verified,report,"build/type_check");bv=verified_artifact(verified,report,"build/bv")
    cache=verified_artifact(verified,report,"cache.bin")
    runner.bind(checker);runner.bind(bv);runner.bind(cache)
    data=verified/"data";types=verified/"types";values=verified/"values"
    for q in range(1,7):
        for suffix in ("roster.tsv","keys.tsv","types.txt","expected.tsv"):
            runner.bind(verified_artifact(verified,report,f"data/q{q}.{suffix}"))
        runner.bind(verified_artifact(verified,report,f"types/q{q}.verified.tsv"))
    runner.bind(verified_artifact(verified,report,"data/normals.txt"))
    runner.bind(verified_artifact(verified,report,"data/field-q3.json"))
    runner.bind(verified_artifact(verified,report,"values/q3.values.tsv"))
    fixtures=output/"fixtures";fixtures.mkdir()
    missing=fixtures/"missing.roster.tsv";missing.write_bytes((data/"q1.roster.tsv").read_bytes().split(b"\n",1)[1]);runner.bind(missing)
    runner.run("missing-original-row",[str(checker),str(data/"normals.txt"),"1",str(missing),str(data/"q1.keys.tsv"),str(data/"q1.types.txt"),str(fixtures/"missing"),"32"],expected_code=2,expected_error="Missing, duplicated, or reordered original mask")
    wrong_index=fixtures/"index.roster.tsv";lines=(data/"q1.roster.tsv").read_text().splitlines();fields=lines[0].split("\t");fields[1]=str(int(fields[1])+1);lines[0]="\t".join(fields);wrong_index.write_text("\n".join(lines)+"\n");runner.bind(wrong_index)
    runner.run("corrupt-original-index",[str(checker),str(data/"normals.txt"),"1",str(wrong_index),str(data/"q1.keys.tsv"),str(data/"q1.types.txt"),str(fixtures/"index"),"32"],expected_code=2,expected_error="Original image index mismatch")
    wrong_gram=fixtures/"gram.keys.tsv";lines=(data/"q1.keys.tsv").read_text().splitlines();left,right=lines[0].split("|");prefix,value=left.rsplit(":",1);lines[0]=prefix+":"+str(int(value.rstrip(","))+1)+",|"+right;wrong_gram.write_text("\n".join(lines)+"\n");runner.bind(wrong_gram)
    runner.run("corrupt-gram",[str(checker),str(data/"normals.txt"),"1",str(data/"q1.roster.tsv"),str(wrong_gram),str(data/"q1.types.txt"),str(fixtures/"gram"),"32"],expected_code=2,expected_error="Representative Gram mismatch")
    wrong_image=fixtures/"image.keys.tsv";lines=(data/"q2.keys.tsv").read_text().splitlines();mutation=None
    for number,line in enumerate(lines):
        prefix,basis=line.split("|");h=list(map(int,basis.rstrip(",").split(",")))
        if h[3]>1:
            old=h[:];h[2]=(h[2]+1)%h[3];lines[number]=prefix+"|"+",".join(map(str,h))+",";mutation={"type":number,"old_basis":old,"new_basis":h,"same_index":h[0]*h[3]};break
    if mutation is None:raise Refused("Required nontrivial image control missing")
    wrong_image.write_text("\n".join(lines)+"\n");runner.bind(wrong_image)
    runner.run("wrong-full-lattice",[str(checker),str(data/"normals.txt"),"2",str(data/"q2.roster.tsv"),str(wrong_image),str(data/"q2.types.txt"),str(fixtures/"image"),"496"],expected_code=2,expected_error="Representative full image lattice mismatch")
    b6=fixtures/"without-b6"
    record=runner.run("missing-bernoulli-degree-six",[str(bv),"evaluate",str(data),str(cache),"6","0","20",str(b6),"2","omit-b6"],category="native",timeout=60)
    altered=read_values(Path(str(b6)+".values.tsv"));baseline=read_values(verified_artifact(verified,report,"values/q6.values.tsv"))
    changed=[tid for tid,row in altered.items() if Fraction(row["alpha"])!=Fraction(baseline[tid]["alpha"])]
    if len(altered)!=20 or len(changed)!=20 or json.loads(record["stdout"])["nonzero_pole_rows"]!=0:
        raise Refused("Missing-B6 control failed to distinguish constants despite pole cancellation")
    field_output=fixtures/"zero-field.json"
    runner.run("omitted-field",[str(Path(sys.executable).resolve()),str(PACKAGE/"field_check.py"),str(data),str(types),str(values),"3",str(field_output),"--zero-field"],expected_code=1)
    field=json.loads(field_output.read_text())
    if field.get("status")!="FAIL" or field.get("below_epsilon")!=13:raise Refused("Omitted-field control did not distinguish the full field")
    return {"missing_row_rejected":True,"corrupt_original_index_rejected":True,"corrupt_gram_rejected":True,"same_index_wrong_lattice_rejected":mutation,
            "B6_changed_constants":changed,"B6_poles_still_cancelled":True,"omitted_field_failed_rows":field["below_epsilon"]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verified-output",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--runtime-only",action="store_true")
    args=parser.parse_args();output=args.output.resolve();started=time.monotonic();runner=None
    try:
        with handle_outer_signals():
            output.mkdir(exist_ok=False)
            runner=Runner(output,code_sources(),native_limit=120,program_limit=300)
            interruptions=[interrupt_probe(output,number) for number in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP,signal.SIGQUIT)]
            timeout_out=output/"timeout"
            timeout=runner.run("real-deadline",[str(Path(sys.executable).resolve()),str(PACKAGE/"verify.py"),"_timeout-probe","--output",str(timeout_out)],expected_code=2,expected_error="deadline",timeout=20,terminate_grace=3)
            if (timeout_out/"COMPLETE.json").exists():raise Refused("Timeout produced a complete marker")
            budget_out=output/"budget"
            runner.run("cumulative-refusal",[str(Path(sys.executable).resolve()),str(PACKAGE/"verify.py"),"_budget-probe","--output",str(budget_out),"--native-seconds","1"],expected_code=2,expected_error="budget admission refused",timeout=20,terminate_grace=3)
            if list((budget_out/"jobs").glob("*.STARTED.json")) or (budget_out/"COMPLETE.json").exists():raise Refused("Refused budget acquired a child or completed")
            runner.run("existing-output-refusal",[str(Path(sys.executable).resolve()),str(PACKAGE/"verify.py"),"full","--output",str(budget_out)],expected_code=2,expected_error="already exists",timeout=20,terminate_grace=3)
            source_results=[]
            for mode in ("before","after"):
                directory=output/("source-"+mode);directory.mkdir()
                source=directory/"bound.txt";source.write_text("one\n")
                owner=Runner(directory,{str(source):digest(source)},native_limit=10,program_limit=10)
                if mode=="before":
                    source.write_text("two\n");command=[str(Path(sys.executable).resolve()),"-c","pass"]
                else:
                    command=[str(Path(sys.executable).resolve()),"-c","from pathlib import Path; import sys; Path(sys.argv[1]).write_text('two\\n')",str(source)]
                try:owner.run("source-change",command,timeout=2)
                except Refused:pass
                else:raise Refused("A changed frozen source was accepted")
                record=json.loads((directory/"jobs/source-change.json").read_text())
                if record["reason"]!="source_mismatch" or not record["cleanup_verified"] or (mode=="before" and record["pid"] is not None):
                    raise Refused("Source integrity control did not reach the expected refusal")
                source_results.append({"phase":mode,"receipt":record})
            from finalization_controls import run_controls as check_finalization
            finalization=check_finalization(output/"finalization",args.verified_output)
            semantic=None
            if not args.runtime_only:
                if args.verified_output is None:raise Refused("--verified-output is required for full targeted controls")
                semantic=semantic_controls(output,runner,args.verified_output.resolve())
            result={"schema":"three-letter-controls/v1","status":"PASS","scope":"runtime-only" if args.runtime_only else "runtime-and-semantic",
                    "interruptions":interruptions,"source_integrity":source_results,"finalization":finalization,"semantic":semantic,"resource_seconds":runner.used,"elapsed_s":time.monotonic()-started,
                    "all_owned_child_cleanup_verified":all(row["cleanup_verified"] for row in runner.receipts),"bare_LR_values":0}
            save(output/"CONTROLS.json",result);print(json.dumps({"status":"PASS","scope":result["scope"],"elapsed_s":result["elapsed_s"]}),flush=True)
        return 0
    except FileExistsError as error:print("REFUSED: "+str(error),file=sys.stderr);return 2
    except Stopped as stop:
        if output.is_dir() and not (output/"ABORTED.json").exists():save(output/"ABORTED.json",{"signal":stop.number})
        return 128+stop.number
    except BaseException as error:
        if output.is_dir() and not (output/"ABORTED.json").exists():save(output/"ABORTED.json",{"error":type(error).__name__,"message":str(error)})
        print("REFUSED: "+str(error),file=sys.stderr);return 2


if __name__=="__main__":raise SystemExit(main())
