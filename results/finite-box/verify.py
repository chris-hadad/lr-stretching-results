#!/usr/bin/env python3
"""Recipient facade: extract, inventory, sample, or full with pinned configuration."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys

CONFIG_SCHEMA="finite-box-recipient-config-v1"
PARAM_SCHEMA="finite-box-facade-parameters-v1"
ENTRY_SCHEMA="portable-box-reproduction-v1"
META=("source_manifest","chosen_terminals","geometry_jobs","legacy_vectors","copy_plan")
MODES={"inventory":"quick","sample":"representative","full":"full"}

class Refused(ValueError):pass
def need(ok,message):
    if not ok:raise Refused(message)
def encoded(value):return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def decode(raw):
    def pairs(items):
        result={}
        for k,v in items:need(k not in result,"Duplicate JSON field");result[k]=v
        return result
    return json.loads(raw,object_pairs_hook=pairs)
def read(path):return decode(Path(path).read_bytes())
def plain(path):
    p=Path(path).absolute();need(not any(x.is_symlink() for x in (p,*p.parents)),"Symlink path refused")
    return p.resolve()
def relative(name):
    need(type(name) is str and name and "\\" not in name and ":" not in name and all(32<=ord(c)!=127 for c in name),"Malformed module-relative path")
    p=PurePosixPath(name);need(not p.is_absolute() and p.as_posix()==name and all(x not in (".","..") for x in p.parts),"Escaping module-relative path")
    return p
def signature(path):
    s=Path(path).stat();return s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns
def pin(path):
    p=plain(path);need(p.is_file(),"Missing regular file: "+str(p));before=signature(p);h=hashlib.sha256()
    with p.open("rb") as stream:
        for block in iter(lambda:stream.read(1024**2),b""):h.update(block)
    need(signature(p)==before,"File changed while hashing")
    return {"path":str(p),"bytes":before[2],"sha256":h.hexdigest()}
def check(p):need(pin(p["path"])==p,"Changed frozen file: "+p["path"])
def bound(root,record,required=None):
    name=relative(record["path"]).as_posix()
    if required is not None:need(name==required,"Wrong configured module layout path")
    need(type(record["bytes"]) is int and record["bytes"]>=0 and type(record["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}",record["sha256"]),"Malformed configured source pin")
    p=pin(root/name);need((p["bytes"],p["sha256"])==(record["bytes"],record["sha256"]),"Configured metadata/tool hash mismatch")
    return p
def integer(value,low,high,label):
    need(type(value) is int and low<=value<=high,label+" is outside its exact finite range");return value
def allocation(value,label):
    need(type(value) in (int,float) and math.isfinite(value) and value>=120,label+" requires an explicit finite allocation of at least 120 seconds in REPRODUCTION-CONFIG.json")
    return float(value)
def module_contract(root):
    root=plain(root);cp=pin(root/"REPRODUCTION-CONFIG.json");cfg=read(cp["path"])
    need(cfg.get("schema")==CONFIG_SCHEMA,"Missing recipient configuration contract")
    tools={}
    for name in ("reproduce","extract_assets"):
        record=cfg["tools"][name];path=relative(record["path"])
        need(path.as_posix()=="extract_assets.py" if name=="extract_assets" else path.parts[0]=="code" and path.name=="reproduce.py", "Wrong configured tool location")
        tools[name]=bound(root,record)
    need(set(cfg["metadata"])==set(META),"Configuration must pin all five exact metadata files")
    metadata={k:bound(root,cfg["metadata"][k],"code/metadata/"+k+".json") for k in META}
    ap=bound(root,cfg["assets"]["catalog"],"DATA-ASSETS.json")
    integer(cfg["assets"]["count"],1,100,"Configured asset count")
    integer(cfg["assets"]["members"],1,150000,"Configured member count")
    integer(cfg["assets"]["expanded_bytes"],1,30_000_000_000,"Configured expanded bytes")
    catalog=read(ap["path"])
    need(catalog.get("schema")=="finite-box-data-assets-v1" and len(catalog["assets"])==cfg["assets"]["count"] and
         catalog["members"]==cfg["assets"]["members"] and catalog["expanded_bytes"]==cfg["assets"]["expanded_bytes"],"Asset/source epoch configuration differs from its pinned catalog")
    return {"root":root,"config":cfg,"configuration":cp,"tools":tools,"metadata":metadata,"asset_catalog":ap}

def parameters(module,mode,data,work,compiler=None,jobs=None):
    need(mode in MODES,"Unknown recipient mode")
    cfg=module["config"];profile=cfg["profiles"][mode]
    batch=integer(profile["jobs_per_call"] if jobs is None else jobs,1,4096,"jobs-per-call")
    numeric,upstream,chunk=0.0,0.0,1
    if mode=="full":
        need(profile.get("calibration_status")=="CALIBRATED","Full execution remains unpriced; root must freeze calibrated allocations and acceptance chunk in REPRODUCTION-CONFIG.json")
        numeric=allocation(profile["numerical_seconds"],"Full numerical work")
        upstream=allocation(profile["upstream_seconds"],"Full upstream work")
        chunk=integer(profile["acceptance_chunk"],1,8192,"Calibrated acceptance chunk")
    elif mode=="sample":
        need(profile.get("calibration_status") in ("CALIBRATED","UNPRICED"),"Unknown sample calibration state")
        numeric=allocation(profile["numerical_seconds"],"Sample numerical work")
    cp=None
    if mode!="inventory":
        need(compiler is not None,"An explicit installed compiler path is required")
        cp=pin(Path(compiler).resolve(strict=True));need(os.access(cp["path"],os.X_OK),"Compiler is not executable")
    data,work=plain(data),plain(work);root=module["root"]
    need(data.is_dir(),"Logical data root is missing; run extract first or supply the complete data directory")
    need(all(not work.is_relative_to(p) and not p.is_relative_to(work) for p in (data,root/"code")),"Work must be disjoint from immutable data and code")
    return {"schema":PARAM_SCHEMA,"requested_mode":mode,"mode":MODES[mode],"module_root":str(root),"data_root":str(data),"work_root":str(work),
            "code_root":str(root/"code"),"core_code_root":str(root/"code/portable-box-code"),"configuration":module["configuration"],
            "tools":module["tools"],"metadata":module["metadata"],"asset_catalog":module["asset_catalog"],"asset_contract":cfg["assets"],
            "python":pin(Path(sys.executable).resolve()),"compiler":cp,"numerical_seconds":numeric,"upstream_seconds":upstream,
            "acceptance_chunk":chunk,"jobs_per_call":batch,"calibration_status":profile.get("calibration_status","INVENTORY_ONLY"),
            "facade":pin(__file__)}

def prepare_command(p):
    cmd=[p["python"]["path"],"-I","-S","-B",p["tools"]["reproduce"]["path"],"prepare","--mode",p["mode"]]
    for k in ("data_root","code_root","core_code_root","work_root"):
        cmd += ["--"+k.replace("_","-"),p[k]]
    for key in META:cmd += ["--"+key.replace("_","-"),p["metadata"][key]["path"]]
    cmd += ["--source-manifest-sha256",p["metadata"]["source_manifest"]["sha256"],"--numerical-seconds",str(p["numerical_seconds"]),
            "--upstream-seconds",str(p["upstream_seconds"]),"--acceptance-chunk",str(p["acceptance_chunk"]),"--jobs-per-call",str(p["jobs_per_call"])]
    if p["compiler"]:cmd += ["--compiler",p["compiler"]["path"]]
    return cmd
def check_plan(p):
    work=Path(p["work_root"]);plan_pin=pin(work/"PLAN.json");plan=read(plan_pin["path"])
    need(plan.get("schema")==ENTRY_SCHEMA,"Existing work is not a recipient entrypoint epoch")
    for key in ("mode","data_root","code_root","core_code_root","work_root","metadata","python","compiler","numerical_seconds","upstream_seconds","acceptance_chunk","jobs_per_call"):
        need(plan.get(key)==p[key],"Frozen reproduction parameter changed: "+key)
    need(plan.get("old_receipt_adoption") is False and plan.get("scientific_execution_during_prepare") is False,"Wrong reproduction scope")
    state=read(work/"STATE.json")
    need(state.get("schema")==ENTRY_SCHEMA and state.get("plan")==plan_pin,"Native cursor is not bound to the exact frozen plan")
    ids=[r["id"] for r in state["calls"]]
    need(ids==[f"call-{i+1:06d}" for i in range(len(ids))],"Missing/duplicate/reordered native caller cursor")
    calls=plain(work/"calls");need(calls.is_dir(),"Missing native call journal")
    need({x.name for x in calls.iterdir() if x.is_dir()}==set(ids) and not any(x.is_symlink() for x in calls.iterdir()),"Native call directories differ from the frozen cursor")
    need(not state.get("mandatory_holds"),"Preserved adverse observations require disposition")
    # The unchanged entrypoint performs the complete call/receipt/code audit.
    return plan_pin
def check_parameters(p):
    for item in [p["configuration"],p["asset_catalog"],p["facade"],p["python"],*p["tools"].values(),*p["metadata"].values()]:check(item)
    if p["compiler"]:check(p["compiler"])
def call(command):
    # Keep this facade until the existing controller has observed its own exit.
    interrupted=[];old=signal.signal(signal.SIGINT,lambda *_:interrupted.append(True))
    try:return subprocess.run(command,check=False).returncode
    finally:signal.signal(signal.SIGINT,old)

def reproduce(module,mode,data,work,compiler=None,jobs=None,max_calls=None,runner=call):
    p=parameters(module,mode,data,work,compiler,jobs)
    batch=integer(module["config"]["profiles"][mode]["max_calls"] if max_calls is None else max_calls,1,1000000,"max-calls")
    root=Path(p["work_root"]);marker=root/"FACADE-PARAMETERS.json"
    check_parameters(p)
    if root.exists():
        need(root.is_dir() and marker.is_file() and not marker.is_symlink(),"Existing work lacks this facade's frozen parameters; historical or incomplete preparation cannot be adopted")
        need(read(marker)==p,"Complete frozen facade parameters differ; do not rewrite an old plan or receipt")
        check_plan(p)
    else:
        rc=runner(prepare_command(p))
        if rc!=0:return rc
        check_parameters(p);check_plan(p)
        with marker.open("xb") as out:out.write(encoded(p)+b"\n");out.flush();os.fsync(out.fileno())
    command=[p["python"]["path"],"-I","-S","-B",p["tools"]["reproduce"]["path"],"run","--work-root",p["work_root"],"--max-calls",str(batch)]
    rc=runner(command);check_parameters(p)
    return rc

def main(argv=None,module_root=None,runner=call):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("extract");p.add_argument("--assets",type=Path,required=True);p.add_argument("--data",type=Path,required=True)
    for mode in MODES:
        p=sub.add_parser(mode);p.add_argument("--data",type=Path,required=True);p.add_argument("--work",type=Path,required=True)
        p.add_argument("--compiler",type=Path);p.add_argument("--jobs-per-call",type=int);p.add_argument("--max-calls",type=int)
    a=parser.parse_args(argv)
    try:
        module=module_contract(module_root or Path(__file__).parent)
        if a.command=="extract":
            cmd=[str(Path(sys.executable).resolve()),"-I","-S","-B",module["tools"]["extract_assets"]["path"],"--assets",str(plain(a.assets)),"--data",str(plain(a.data))]
            rc=runner(cmd);check(module["configuration"]);return rc
        return reproduce(module,a.command,a.data,a.work,a.compiler,a.jobs_per_call,a.max_calls,runner)
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({"status":"RECIPIENT_COMMAND_REFUSED","error":f"{type(error).__name__}: {error}","mathematical_acceptance_inferred":False}),file=sys.stderr,flush=True);return 2

if __name__=="__main__":raise SystemExit(main())
