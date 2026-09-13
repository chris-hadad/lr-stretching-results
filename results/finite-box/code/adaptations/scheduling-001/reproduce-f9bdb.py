#!/usr/bin/env python3
"""Serial recipient entrypoint over the byte-preserved portable controllers.

prepare freezes explicit inputs and code. run resumes at most --max-calls
controller invocations (default one); each scientific controller receives the
frozen --jobs-per-call batch and retains its own deadlines, cursor and holds.
quick is inventory only. representative never closes the box. full requires
fresh upstream, components, composition, counts, acceptance and final joins.
No network, installation, historical receipt conversion or source fallback.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import fcntl
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
sys.dont_write_bytecode=True

SCHEMA="portable-box-reproduction-v1"
META=("source_manifest","chosen_terminals","geometry_jobs","legacy_vectors","copy_plan")
COMPONENTS={"geometry":619875,"algebra":620370,"bounds":469728,"early":3647,"final":495}
UNITS={"U04":150147,"U05":154408,"U06":143401,"U07":99212,"U08":51477,"U09":18424,
       "U10":2806,"U11":495,"U02":169,"U03":3478,"LEGACY":297}
FULL=624314
SCOPE={"quick":"File inventory and code-byte closure only; data content is rechecked by the scientific controllers.",
       "representative":"Selected fresh count evidence only; no exhaustive coverage or terminal acceptance.",
       "full":"The finite original box, conditional on the explicitly named classical and prior external theorem premises. No all-parameter or campaign-wide theorem promotion."}

class Refused(ValueError):pass
class Unresolved(RuntimeError):pass
def need(ok,message):
    if not ok:raise Refused(message)
def encode(v):return json.dumps(v,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def decode(raw):
    def pairs(rows):
        out={}
        for k,v in rows:need(k not in out,"Duplicate JSON key");out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs)
def plain(value):
    p=Path(value).absolute();need(not any(q.is_symlink() for q in (p,*p.parents)),"Symlink paths are not portable inputs or outputs")
    return p.resolve()
def relative(value):
    p=Path(value);need(type(value) is str and value and not p.is_absolute() and str(p)==value and
        all(x not in (".","..") for x in p.parts) and "\\" not in value and ":" not in value,"Escaping relative source path")
    return p
def stamp(p):
    s=Path(p).stat();return s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns
def pin(path):
    p=plain(path);need(p.is_file(),"Missing regular file: "+str(p));before=stamp(p);h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1024**2),b""):h.update(block)
    need(stamp(p)==before,"File changed while hashing")
    return {"path":str(p),"bytes":before[2],"sha256":h.hexdigest()}
def check(p):need(pin(p["path"])==p,"Changed bound file: "+p["path"])
def read(p):return decode(plain(p).read_bytes())
def save(p,value):
    with plain(p).open("xb") as f:f.write(encode(value)+b"\n");f.flush();os.fsync(f.fileno())
def state_save(work,value):
    p=work/f"STATE.{os.getpid()}.tmp";save(p,value);os.replace(p,work/"STATE.json")
def within(p,root):
    p=plain(p);need(p.is_relative_to(plain(root)),"Artifact escaped its newly created workspace");return p
def adapter(code):
    path=plain(code)/"portable-box-acceptance.py"
    spec=importlib.util.spec_from_file_location("_reproduction_metadata_reader",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module  # Only its streamed JSON reader is called here.
def metadata(path,array,reader):
    if array is None:return read(path)
    result={};count=0
    for _ in reader.array_records(path,array,result):count+=1
    result["_streamed_records"]=count;return result

def code_closure(code,core):
    files=[pin(__file__)]
    for name in ("portable-box-components.py","portable-box-composition.py","portable-box-acceptance.py"):
        files.append(pin(code/name))
    for directory,names in ((core,("portable_run.py","SOURCE-MAP.json")),
         (code/"portable-box-numerics",("common.py","numerical_indices.py","numerics.py","SOURCE-MAP.json")),
         (code/"portable-box-upstream",("common.py","phases.py","upstream.py","build_runtime.py","SOURCE-MAP.json","RUNTIME-MAP.json","INPUT-REQUIREMENTS.json"))):
        files.extend(pin(directory/name) for name in names)
        mapping=read(directory/"SOURCE-MAP.json")
        for row in mapping["copies"]:
            p=pin(directory/relative(row["path"]));expected=(row.get("portable_bytes",row.get("bytes")),row.get("portable_sha256",row.get("sha256")))
            need((p["bytes"],p["sha256"])==expected,"Changed preserved core or original mathematical source");files.append(p)
        if (directory/"RUNTIME-MAP.json").is_file():
            for row in read(directory/"RUNTIME-MAP.json")["files"]:
                p=pin(directory/relative(row["path"]));need((p["bytes"],p["sha256"])==(row["bytes"],row["sha256"]),"Changed upstream runtime mathematical body");files.append(p)
    return sorted({p["path"]:p for p in files}.values(),key=lambda p:p["path"])

def inventory(data,manifest):
    doc=read(manifest["path"]);need(doc.get("schema")=="early-input-manifest-v1","Expected the relative whole-file source manifest")
    seen=set();total=0
    for row in doc["files"]:
        name=relative(row["path"]);need(str(name) not in seen,"Duplicate manifest source");seen.add(str(name))
        need(type(row["bytes"]) is int and row["bytes"]>=0 and isinstance(row["sha256"],str) and len(row["sha256"])==64 and set(row["sha256"])<=set("0123456789abcdef"),"Malformed source identity")
        path=plain(data/name);need(path.is_file() and path.stat().st_size==row["bytes"],"Missing or wrong-size data member: "+str(name));total+=row["bytes"]
    return {"status":"INVENTORY_ONLY","files":len(seen),"declared_bytes":total,"all_named_files_present_with_declared_sizes":True,
            "bulk_data_content_hashes_checked":False,"source_manifest":manifest,"whole_theorem_accepted":False}

def jobs_per_call(value):
    need(type(value) is int and 1<=value<=64,"Jobs per controller call must be an exact integer in 1..64")
    return value

def prepare(a):
    batch=jobs_per_call(a.jobs_per_call)
    data,code,core,work=map(plain,(a.data_root,a.code_root,a.core_code_root or Path(a.code_root)/"portable-box-code",a.work_root))
    need(not work.exists() and all(p.is_dir() for p in (data,code,core)),"Existing explicit data/code/core roots and a fresh work root are required")
    need(all(not work.is_relative_to(p) and not p.is_relative_to(work) for p in (data,code,core)),"Work must be disjoint from immutable data and code")
    inputs={}
    for k in META:
        p=plain(getattr(a,k));need(p.is_relative_to(data) or p.is_relative_to(code),"Metadata must belong to the declared distribution data/code roots");inputs[k]=pin(p)
    if a.source_manifest_sha256:need(inputs["source_manifest"]["sha256"]==a.source_manifest_sha256,"Wrong supplied source-manifest hash")
    inv=inventory(data,inputs["source_manifest"]);sources=code_closure(code,core)
    compiler=None
    if a.mode!="quick":
        need(a.compiler is not None,"An explicit installed compiler is required for fresh counts; no compiler is installed automatically")
        compiler=pin(Path(a.compiler).resolve(strict=True));need(os.access(compiler["path"],os.X_OK),"Compiler is not executable")
        need(math.isfinite(a.numerical_seconds) and a.numerical_seconds>=120,"Explicit finite numerical allocation must reserve at least 120 seconds")
        if a.mode=="full":need(math.isfinite(a.upstream_seconds) and a.upstream_seconds>=120,"Explicit finite upstream allocation must reserve at least 120 seconds")
    need(1<=a.acceptance_chunk<=8192,"Acceptance slice must be 1..8192")
    plan={"schema":SCHEMA,"mode":a.mode,"data_root":str(data),"code_root":str(code),"core_code_root":str(core),"work_root":str(work),
          "metadata":inputs,"code":sources,"compiler":compiler,"python":pin(Path(sys.executable).resolve()),"inventory":inv,
          "numerical_seconds":a.numerical_seconds,"upstream_seconds":a.upstream_seconds,"acceptance_chunk":a.acceptance_chunk,"jobs_per_call":batch,
          "scope":SCOPE[a.mode],"old_receipt_adoption":False,"scientific_execution_during_prepare":False}
    work.mkdir(parents=True);(work/"calls").mkdir();save(work/"PLAN.json",plan)
    state_save(work,{"schema":SCHEMA,"plan":pin(work/"PLAN.json"),"calls":[]})
    return {"status":"PREPARED_INVENTORY_ONLY","plan":pin(work/"PLAN.json"),"inventory":inv,"scope":plan["scope"]}

def stages(plan):
    mode=plan["mode"]
    if mode=="quick":return []
    out=[]
    def add(key,kind,**kw):out.append({"key":key,"kind":kind,**kw})
    if mode=="full":
        add("composition-init","composition-init")
        for name in ("prepare","run","aggregate"):add("upstream-"+name,"upstream-"+name)
        add("components-prepare","components-prepare")
        for component in COMPONENTS:
            for name in ("run","aggregate"):add(component+"-"+name,"component-"+name,component=component)
        add("composition-run","composition-run")
    for name in ("prepare","run","aggregate"):add("numerics-"+name,"numerics-"+name)
    if mode=="full":
        add("acceptance-prepare","acceptance-prepare")
        for unit,total in UNITS.items():
            chunk=min(plan["acceptance_chunk"],4 if unit=="LEGACY" else 64 if unit in ("U02","U03") else 8192)
            for start in range(0,total,chunk):add(f"accept-{unit}-{start}","acceptance-verify",unit=unit,start=start,stop=min(start+chunk,total))
        add("acceptance-assemble","acceptance-assemble");add("composition-finalize","composition-finalize")
    return out

def roots(plan):
    work=Path(plan["work_root"]);composition=work/"composition"
    parent=composition if plan["mode"]=="full" else work
    return {"composition":composition,"components":parent/"components","numerics":parent/"numerics","upstream":parent/"upstream","acceptance":parent/"acceptance"}
def kind_root(stage):
    k=stage["kind"]
    return "components" if k.startswith("component") else k.split("-")[0]
def native_state(root):return root/"STATE.json" if (root/"STATE.json").exists() else None
def native_recipe(root):
    for name in ("RECIPE.json","PLAN.json"):
        if (root/name).exists():return root/name
    return None
def body_pin(value,root):
    p=pin(within(value["path"],root));need(p==value,"Stale emitted report binding");return p

class Context:
    def __init__(self,work):
        self.work=plain(work);self.state=read(self.work/"STATE.json");check(self.state["plan"]);self.plan=read(self.state["plan"]["path"])
        need(self.plan["schema"]==self.state["schema"]==SCHEMA and self.plan["work_root"]==str(self.work),"Wrong reproduction epoch")
        jobs_per_call(self.plan["jobs_per_call"])
        self.graph=stages(self.plan);self.done={};self.last_states={};self.held=[];self.cursor=0
        need(not self.state.get("mandatory_holds"),"This epoch has preserved adverse observations requiring owner disposition")
        self.workspace=roots(self.plan);self.reader=None
        self.checked={}
        self.stable();self.reader=adapter(self.plan["code_root"])
    def bound(self,p):
        old=self.checked.get(p["path"])
        if old is None:check(p);self.checked[p["path"]]=(dict(p),stamp(p["path"]))
        else:need(old==(p,stamp(p["path"])),"Previously hashed source/evidence changed")
        return p
    def stable(self):
        for p in [self.state["plan"],self.plan["python"],*self.plan["code"],*self.plan["metadata"].values()]:self.bound(p)
        if self.plan["compiler"]:self.bound(self.plan["compiler"])
        for p,s in self.checked.values():need(stamp(p["path"])==s,"Bound source/evidence changed during this batch")
    def current(self):return self.graph[self.cursor] if self.cursor<len(self.graph) else None
    def command(self,task,identity):
        p=self.plan;code=Path(p["code_root"]);core=p["core_code_root"];r=self.workspace;k=task["kind"];m=p["metadata"]
        py=[p["python"]["path"],"-I","-S","-B"];batch=str(jobs_per_call(p["jobs_per_call"]))
        def meta(keys):return [v for key in keys for v in ("--"+key.replace("_","-"),m[key]["path"],"--"+key.replace("_","-")+"-sha256",m[key]["sha256"])]
        if k.startswith("composition"):
            name="finalize" if k.endswith("finalize") else "run"
            cmd=py+[str(code/"portable-box-composition.py"),name,"--data-root",p["data_root"],"--code-root",core,"--work-root",str(r["composition"]),"--max-jobs",batch]
            if k=="composition-run" or k=="composition-init" and str(r["composition"]) in self.last_states:cmd+=["--resume"]
            if name=="finalize":cmd += ["--acceptances",self.done["acceptance-assemble"]["bindings"]["path"]]
            return cmd
        if k.startswith("upstream"):
            cmd=py+[str(code/"portable-box-upstream/upstream.py"),k.split("-")[1],"--work-root",str(r["upstream"])]
            if k.endswith("prepare"):
                return cmd+["--data-root",p["data_root"],"--input-manifest",m["source_manifest"]["path"],"--input-manifest-sha256",m["source_manifest"]["sha256"],
                            "--compiler",p["compiler"]["path"],"--total-seconds",str(p["upstream_seconds"])]
            return cmd+["--lane","all"]+(["--max-jobs",batch] if k.endswith("run") else [])
        if k.startswith("component"):
            cmd=py+[str(code/"portable-box-components.py"),"prepare" if k=="components-prepare" else k.split("-")[1],"--work-root",str(r["components"])]
            if k=="components-prepare":return cmd+["--data-root",p["data_root"],"--code-root",core]+meta(("source_manifest","chosen_terminals","geometry_jobs"))
            return cmd+["--component",task["component"]]+(["--max-jobs",batch] if k.endswith("run") else [])
        if k.startswith("numerics"):
            cmd=py+[str(code/"portable-box-numerics/numerics.py"),k.split("-")[1],"--work-root",str(r["numerics"])]
            if k.endswith("prepare"):
                return cmd+["--data-root",p["data_root"],"--mode",p["mode"],"--compiler",p["compiler"]["path"],"--holdouts","first-unused","--total-seconds",str(p["numerical_seconds"])]+meta(META)
            return cmd+["--cohort","all"]+(["--max-jobs",batch] if k.endswith("run") else [])
        cmd=py+[str(code/"portable-box-acceptance.py"),k.split("-")[1],"--work-root",str(r["acceptance"])]
        if k=="acceptance-prepare":
            return cmd+["--data-root",p["data_root"],"--code-root",p["code_root"],"--core-code-root",core,
                        "--composition-root",str(r["composition"]),"--components-root",str(r["components"]),"--numerics-root",str(r["numerics"]),
                        "--requirements",self.done["composition-run"]["requirements"]["path"],"--component-reports",
                        *[self.done[c+"-aggregate"]["result"]["path"] for c in COMPONENTS],"--numerical-reports",self.done["numerics-aggregate"]["result"]["path"]]
        cmd += ["--id",identity,"--seconds","100"]
        if k=="acceptance-verify":return cmd+["--unit",task["unit"],"--start",str(task["start"]),"--stop",str(task["stop"])]
        need(k=="acceptance-assemble","Unknown frozen stage")
        return cmd+["--parts",*[v["result"]["path"] for key,v in self.done.items() if key.startswith("accept-")]]
    def evidence(self):
        return list({p["path"]:p for v in self.done.values() for p in v["evidence"]}.values())

def reply_from(folder,returncode):
    path=folder/("stdout.txt" if returncode==0 else "stderr.txt")
    lines=path.read_bytes().splitlines()
    for raw in reversed(lines):
        try:
            value=decode(raw)
            if isinstance(value,dict) and "status" in value:return value
        except (ValueError,UnicodeError):pass
    return None

def validate_stage(ctx,task,reply,execution):
    """Require a real fresh controller exit plus its exact current report contract."""
    k=task["kind"];root=ctx.workspace[kind_root(task)];refs=[];out={}
    def get(value,array=None):
        p=body_pin(value,root);refs.append(p);return metadata(p["path"],array,ctx.reader),p
    if not isinstance(reply,dict):return None
    if reply.get("status") in ("HELD_ADVERSE_OBSERVATION","HOLD_ORDINARY_NEGATIVE","HOLD_CANDIDATE"):
        ctx.held.append({"task":task,"execution":execution,"reply":reply});return None
    if k.startswith("acceptance") and k!="acceptance-prepare":
        result_path=within(reply.get("result",root/"missing-result"),root)
        if result_path.is_file():
            z,p=get(pin(result_path))
            if z.get("ordinary_negative_observations") or z.get("status")=="HOLD_ORDINARY_NEGATIVE":
                ctx.held.append({"task":task,"execution":execution,"result":p});return None
    if execution["returncode"]!=0:return None
    if k.endswith("prepare"):
        expected="PREPARED_PORTABLE_ACCEPTANCE_METADATA" if k=="acceptance-prepare" else "PREPARED_METADATA_ONLY"
        need(reply["status"]==expected,"Wrong preparation outcome")
        z,p=get(reply["recipe"]);need(p["path"]==str(root/"RECIPE.json") and z["work_root"]==str(root) and z["data_root"]==ctx.plan["data_root"],"Prepared recipe has another data/work root")
        if k=="numerics-prepare":need(z["mode"]==ctx.plan["mode"] and z["holdouts"]=="first-unused","Changed count scope or held-site policy")
        if k=="components-prepare":need(z["code_root"]==ctx.plan["core_code_root"],"Wrong immutable component core")
        out["recipe"]=p
    elif k.startswith("composition"):
        expected="COMPLETE_LITERAL_COMPOSITION_WITH_CALLER_ACCEPTANCES" if k=="composition-finalize" else "READY_FOR_EARNED_ACCEPTANCES"
        native=execution.get("native_state")
        need(native is not None,"Composition did not persist its exact native cursor")
        state=read(native["snapshot"]["path"]);need(state["status"]==reply["status"],"Composition caller/status snapshot differs")
        if k=="composition-init":
            need(reply["status"] in ("PAUSED_AT_EXACT_CURSOR",expected),"Composition initialization did not earn a resumable state")
        else:
            if reply["status"]=="PAUSED_AT_EXACT_CURSOR":return None
            need(reply["status"]==expected,"Composition did not complete its required boundary")
            boundary,bp=get(state["boundary"]);need(boundary["status"]==expected and boundary["progress"]==state["progress"] and boundary["source_rechecks"],"Composition lacks exact final source rechecks")
            progress=boundary["progress"];required=progress["requirements"]
            rp=pin(within(required["path"],root));need(all(rp[x]==required[x] for x in rp) and required["records"]==FULL,"Incomplete exact newly exported terminal requirement population")
            refs.append(rp);out["requirements"]=rp
            need(set(progress["phases"])=={"membership","original-weights","horn-weights","remaining"},"Missing nonacceptance composition phase")
            if k=="composition-finalize":
                final,fp=get(progress["final"]);need(final["status"]=="COMPLETE_LITERAL_COMPOSITION_WITH_OWNER_ACCEPTED_TERMINALS","Final literal join did not earn its exact terminal predicate")
                out["result"]=fp
    elif k.endswith("run"):
        z,p=get(reply["report"])
        preparation="components-prepare" if k=="component-run" else "numerics-prepare" if k=="numerics-run" else "upstream-prepare"
        need(z["recipe"]==ctx.done[preparation]["recipe"],"Progress report belongs to a different prepared source epoch")
        if k=="component-run":
            need(z["component"]==task["component"] and not z.get("mandatory_holds"),"Wrong component or held observations")
            complete=reply["status"]==z["status"]=="COMPONENT_STEPS_COMPLETE_PENDING_AGGREGATE" and not z["remaining_steps"]
        elif k=="numerics-run":
            need(z["cohort"]=="all" and z["mode"]==ctx.plan["mode"] and not z["fatal"],"Wrong numerical scope or held observations")
            complete=reply["status"]==z["status"]=="COUNT_ENGINE_STEPS_COMPLETE_PENDING_GLOBAL_JOIN" and not z["remaining"]
        else:
            need(z["lane"]=="all" and not z["candidate_hold"],"Wrong upstream lane or held observations")
            complete=reply["status"]==z["status"]=="COMPLETE_STEPS_PENDING_AGGREGATE" and not z["pending_exact_steps"]
        if not complete:return None
        out["result"]=p
    elif k.endswith("aggregate"):
        array="exact_source_identities" if k=="component-aggregate" else "exact_source_and_node_roster" if k=="numerics-aggregate" else None
        z,p=get(reply["aggregate"],array)
        if k=="component-aggregate":
            c=task["component"];need(z["status"]==reply["status"]=="PASS_COMPONENT_CONDITIONAL_ON_RECORDED_COUNTS_AND_SEPARATE_PREMISES" and
                z["component"]==c and z["records"]==z["_streamed_records"]==COMPONENTS[c] and z["all_literal_source_identities_once"] is True,"Incomplete component aggregate")
            need(z["recipe"]==ctx.done["components-prepare"]["recipe"] and z["executions"],"Component aggregate lost its exact recipe/executions")
        elif k=="numerics-aggregate":
            status="FULL_LITERAL_COUNT_EVIDENCE_COMPLETE_PENDING_MATHEMATICAL_JOINS" if ctx.plan["mode"]=="full" else "REPRESENTATIVE_COUNTS_MATCH_ONLY"
            need(z["status"]==reply["status"]==status and z["cohort"]=="all" and z["mode"]==ctx.plan["mode"] and z["records"]==z["_streamed_records"]>0 and z["fragments"],"Incomplete numerical evidence")
            need(z["recipe"]==ctx.done["numerics-prepare"]["recipe"],"Numerical aggregate changed recipe")
            if ctx.plan["mode"]=="full":need(z["records"]==FULL,"Full numerical aggregate omitted original terminals")
        else:
            recipe=read(ctx.done["upstream-prepare"]["recipe"]["path"])
            need(z["status"]==reply["status"]=="F025_PREDECESSOR_REPLAY_COMPLETE_CONDITIONAL_ON_NAMED_EXTERNAL_THEOREMS" and z["lane"]=="all" and
                z["exact_steps"]==[s["id"] for s in recipe["steps"]] and set(z["evidence"])==set(z["exact_steps"]) and z["fresh_census_ranks"]==[6,7],"Missing fresh exhaustive predecessor obligations")
            need(z["recipe"]==ctx.done["upstream-prepare"]["recipe"] and z["prior_external_premises"],"Upstream predicate lost its source epoch or external premise boundary")
        out["result"]=p
    else:
        need(k in ("acceptance-verify","acceptance-assemble") and reply["status"]=="CHILD_COMPLETE","Acceptance child did not complete")
        z,p=get(pin(within(reply["result"],root)));ep=body_pin(pin(within(reply["execution"],root)),root);refs.append(ep);e=read(ep["path"])
        need(e["disposition"]=="exited" and e["child_returncode"]==0 and e["cleanup_verified"] is True and e["sources_unchanged"] is True,"Acceptance lacks an actual clean child exit")
        need(z["complete"] is True and z["requirements"]==ctx.done["composition-run"]["requirements"],"Acceptance belongs to another requirement export")
        if k=="acceptance-verify":
            need(z["status"]=="COMPLETE_PORTABLE_TERMINAL_SLICE" and z["unit"]==task["unit"] and z["slice"]==[task["start"],task["stop"]] and
                z["records"]==task["stop"]-task["start"] and z["checked_terminal_ids"]==z["expected_terminal_ids"],"Acceptance omitted its exact literal slice")
        else:need(z["status"]=="COMPLETE_PORTABLE_BOX_TERMINAL_ACCEPTANCE" and z["records"]==FULL and z["counts"]==UNITS and z["exact_expected_identities_once"] is True,"Incomplete exact terminal acceptance union")
        out.update(result=p,bindings=body_pin(z["bindings"],root));refs.append(out["bindings"])
    out["evidence"]=[*refs,execution["_pin"]];return out

def collect_native(folder,root):
    path=native_state(root)
    if path is None:return None
    original=pin(path);raw=path.read_bytes();need(sha(raw)==original["sha256"],"Native state changed during capture")
    with (folder/"NATIVE-STATE-AFTER.json").open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return {"origin":original,"snapshot":pin(folder/"NATIVE-STATE-AFTER.json")}

def acceptance_observations(ctx,task,identity):
    if task["kind"] not in ("acceptance-verify","acceptance-assemble"):return
    folder=ctx.workspace["acceptance"]/"jobs"/identity
    path=folder/"result.raw-vectors.jsonl"
    if not path.exists():return
    source=pin(path);found=[]
    with path.open("rb") as stream:
        for line,raw in enumerate(stream,1):
            try:
                need(raw.endswith(b"\n"),"Incomplete raw-vector observation")
                row=decode(raw)
                adverse=row.get("ordinary_negative_indices") or row.get("kind")=="fresh_four_count_functionals" and Fraction(row["c2"])<0
                if adverse:found.append({"line":line,"row":row,"artifact":source,"authenticated_scientific_result":False})
            except (ValueError,KeyError,TypeError,ZeroDivisionError):
                found.append({"line":line,"record_sha256":sha(raw),"artifact":source,"scope":"Unresolved durable raw-vector bytes; no mathematical verdict"})
    if found:ctx.held.append({"call":identity,"observations":found,"requires_owner_disposition":True})

def native_hold_observations(ctx,root,identity):
    path=native_state(root)
    if path is None:return
    try:
        value=read(path)
        if value.get("mandatory_holds"):
            ctx.held.append({"call":identity,"native_state":pin(path),"mandatory_holds":value["mandatory_holds"],"authenticated_scientific_result":False})
    except (OSError,ValueError,UnicodeError):
        ctx.held.append({"call":identity,"path":str(path),"scope":"Unresolved native state bytes; no acceptance or retry inferred"})

def invoke(ctx,task,runner=None):
    need(not ctx.held,"Adverse observations require disposition; a new lane cannot bypass them")
    ctx.stable();identity=f"call-{len(ctx.state['calls'])+1:06d}";folder=ctx.work/"calls"/identity;folder.mkdir()
    root=ctx.workspace[kind_root(task)];before=pin(native_state(root)) if native_state(root) else None
    need(before==ctx.last_states.get(str(root)),"Native cursor changed outside the exact recorded controller calls")
    command=ctx.command(task,identity);request={"schema":SCHEMA,"id":identity,"plan":ctx.state["plan"],"task":task,"command":command,
                                             "before_state":before,"prerequisites":ctx.evidence()}
    save(folder/"REQUEST.json",request);rp=pin(folder/"REQUEST.json");ctx.state["calls"].append({"id":identity,"request":rp});state_save(ctx.work,ctx.state)
    started=time.monotonic();process=None;rc=None;interrupted=[]
    old=signal.signal(signal.SIGINT,lambda *_:interrupted.append(True))
    try:
        with (folder/"stdout.txt").open("xb") as out,(folder/"stderr.txt").open("xb") as err:
            process=subprocess.Popen(command,stdout=out,stderr=err,cwd=ctx.work) if runner is None else runner(command,out,err,ctx.work)
            save(folder/"LAUNCH.json",{"command":command,"pid":process.pid,"pgid":os.getpgid(process.pid),"started_unix":time.time()})
            rc=process.wait()
    finally:signal.signal(signal.SIGINT,old)
    elapsed=time.monotonic()-started;stable=True;error=None
    try:ctx.stable()
    except (OSError,ValueError) as exc:stable=False;error=str(exc)
    ns=collect_native(folder,root);reply=reply_from(folder,rc)
    save(folder/"RETURN.json",reply)
    result={"schema":SCHEMA,"request":rp,"command":command,"pid":process.pid,"returncode":rc,"actual_controller_exit_observed":True,
            "elapsed_seconds":elapsed,"controller_interrupted":bool(interrupted),"sources_unchanged":stable,"source_error":error,
            "native_state":ns,"outputs":[pin(p) for p in sorted(folder.iterdir()) if p.is_file()]}
    save(folder/"EXECUTION.json",result)
    return folder

def consume_call(ctx,item):
    identity=f"call-{len(ctx._consumed)+1:06d}"
    need(item["id"]==identity,"Missing/duplicate/reordered top-level invocation")
    folder=ctx.work/"calls"/identity;check(item["request"]);request=read(item["request"]["path"])
    task=ctx.current();need(task is not None and request["task"]==task and request["plan"]==ctx.state["plan"] and request["command"]==ctx.command(task,identity),"Changed exact controller call/step")
    need(request["prerequisites"]==ctx.evidence(),"Controller call lost its already earned prerequisite report identities")
    for p in request["prerequisites"]:ctx.bound(p)
    acceptance_observations(ctx,task,identity)
    native_hold_observations(ctx,ctx.workspace[kind_root(task)],identity)
    if ctx.held:
        ctx.state["mandatory_holds"]=ctx.held;state_save(ctx.work,ctx.state)
    if not (folder/"EXECUTION.json").is_file():raise Unresolved("Controller call has no observed exit; reconcile "+str(folder))
    ep=pin(folder/"EXECUTION.json");e=read(ep["path"]);launch=read(folder/"LAUNCH.json")
    need(e["schema"]==SCHEMA and e["request"]==item["request"] and e["command"]==launch["command"]==request["command"] and
        type(e["pid"]) is int and e["pid"]==launch["pid"] and type(e["returncode"]) is int and e["actual_controller_exit_observed"] is True and
        e["sources_unchanged"] is True and not e["source_error"] and math.isfinite(e["elapsed_seconds"]) and e["elapsed_seconds"]>=0,"Unfinished/stale actual controller execution")
    outputs={}
    for p in e["outputs"]:
        within(p["path"],folder);check(p);need(p["path"] not in outputs,"Duplicate caller output");outputs[p["path"]]=p
    need(set(outputs)=={str(p) for p in folder.iterdir() if p.is_file() and p.name!="EXECUTION.json"},"Missing/extra caller output member")
    root=ctx.workspace[kind_root(task)];need(request["before_state"]==ctx.last_states.get(str(root)),"Broken native cursor chain")
    native=e["native_state"]
    if native:
        check(native["snapshot"]);need(native["origin"]["path"]==str(root/"STATE.json") and
             all(native["origin"][k]==native["snapshot"][k] for k in ("bytes","sha256")),"Native state snapshot detached from original bytes")
        ctx.last_states[str(root)]=native["origin"]
        state=read(native["snapshot"]["path"])
        if state.get("mandatory_holds"):ctx.held.append({"call":identity,"mandatory_holds":state["mandatory_holds"],"snapshot":native["snapshot"]})
    reply=read(folder/"RETURN.json");need(reply==reply_from(folder,e["returncode"]),"Reply differs from actual controller output")
    e["_pin"]=ep
    outcome=validate_stage(ctx,task,reply,e)
    if ctx.held:ctx.state["mandatory_holds"]=ctx.held;state_save(ctx.work,ctx.state)
    if outcome is not None and not ctx.held:ctx.done[task["key"]]=outcome;ctx.cursor+=1
    ctx._consumed.append(identity)
    return outcome is not None,e["returncode"],e["controller_interrupted"]

def audit(ctx):
    ctx._consumed=[]
    for item in ctx.state["calls"]:consume_call(ctx,item)
    for root,wanted in ctx.last_states.items():check(wanted)
    return ctx
def result(ctx):
    if ctx.plan["mode"]=="quick":
        need(inventory(Path(ctx.plan["data_root"]),ctx.plan["metadata"]["source_manifest"])==ctx.plan["inventory"],"Quick inventory changed after preparation")
    complete=ctx.current() is None and not ctx.held
    label="INVENTORY_ONLY" if ctx.plan["mode"]=="quick" else "REPRESENTATIVE_FRESH_COUNTS_ONLY" if ctx.plan["mode"]=="representative" else "FULL_FINITE_BOX_REPLAY_WITH_NAMED_EXTERNAL_PREMISES"
    return {"schema":SCHEMA,"status":"HELD_ADVERSE_OBSERVATION" if ctx.held else label if complete else "PAUSED_AT_EXACT_CONTROLLER_STEP",
            "complete_at_declared_claim_level":complete,"mode":ctx.plan["mode"],"scope":ctx.plan["scope"],"plan":ctx.state["plan"],
            "completed_stage_keys":list(ctx.done),"pending":ctx.current(),"mandatory_holds":ctx.held,
            "evidence":ctx.evidence(),"old_receipt_adoption":False,"campaign_or_unbounded_theorem_accepted":False}
@contextmanager
def lock(work):
    with (plain(work)/"LOCK").open("a") as stream:
        try:fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise Unresolved("Another recipient controller owns this epoch") from None
        yield
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("prepare");p.add_argument("--mode",choices=SCOPE,required=True)
    for name in ("data-root","code-root","work-root"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--core-code-root",type=Path);p.add_argument("--compiler",type=Path)
    for name in META:p.add_argument("--"+name.replace("_","-"),type=Path,required=True)
    p.add_argument("--source-manifest-sha256");p.add_argument("--numerical-seconds",type=float,default=0);p.add_argument("--upstream-seconds",type=float,default=0)
    p.add_argument("--acceptance-chunk",type=int,default=2048)
    p.add_argument("--jobs-per-call",type=int,default=16,help="Frozen scientific jobs per controller run/finalize call, 1..64 (default 16)")
    for name in ("run","status"):
        p=sub.add_parser(name);p.add_argument("--work-root",type=Path,required=True)
        if name=="run":p.add_argument("--max-calls",type=int,default=1)
    a=parser.parse_args(argv);ctx=None
    last_rc=0
    try:
        if a.command=="prepare":out=prepare(a)
        else:
            with lock(a.work_root):
                ctx=audit(Context(a.work_root))
                if a.command=="run":
                    need(type(a.max_calls) is int and a.max_calls>0,"Explicit positive finite batch size required")
                    for _ in range(a.max_calls):
                        if ctx.current() is None or ctx.held:break
                        invoke(ctx,ctx.current());_okay,rc,interrupted=consume_call(ctx,ctx.state["calls"][-1])
                        last_rc=rc
                        print(json.dumps({"calls":len(ctx.state["calls"]),"completed_stages":ctx.cursor,"next":ctx.current(),"returncode":rc}),flush=True)
                        if rc!=0 or interrupted:break
                ctx.stable();out=result(ctx)
                path=ctx.work/f"REPORT-{len(list(ctx.work.glob('REPORT-*.json')))+1:06d}.json";save(path,out);out={**out,"report":pin(path)}
        print(json.dumps(out,sort_keys=True),flush=True);return 2 if out.get("mandatory_holds") or last_rc else 0
    except (OSError,ValueError,KeyError,TypeError,Unresolved) as error:
        print(json.dumps({"schema":SCHEMA,"status":"UNRESOLVED" if isinstance(error,Unresolved) else "REFUSED","error":f"{type(error).__name__}: {error}",
                          "work_root":str(getattr(a,"work_root","")),"campaign_or_unbounded_theorem_accepted":False}),file=sys.stderr,flush=True);return 2

if __name__=="__main__":raise SystemExit(main())
