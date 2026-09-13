#!/usr/bin/env python3
"""New portable mathematical acceptance slices and exact final concatenation.

prepare freezes explicit roots/reports only. verify runs one bounded unit slice;
assemble requires all exact 624314 newly exported terminal bindings. Every run
gets a new private child request/launch/exit; old run_check receipts are neither
read nor translated. No lattice counter or build is launched by this program.

Layout: code-root contains portable-box-numerics/ and the current portable
controllers. core-code-root names the immutable mathematical checker directory;
prepare defaults it to code-root/portable-box-code. Component/numerical/acceptance work directories
must be descendants of composition-root, allowing its later acceptance phase
to authenticate every new evidence path without historical path rewriting.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import signal
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace

SCHEMA = "portable-box-acceptance-v1"
ROW_SCHEMA = "box-terminal-acceptance-v1"
PREDICATE = "entire_stretching_polynomial_nonnegative"
COUNTS = {"U04":150147,"U05":154408,"U06":143401,"U07":99212,"U08":51477,
          "U09":18424,"U10":2806,"U11":495,"U02":169,"U03":3478,"LEGACY":297}
TOTAL = 624314
COMPACT = {"U04":"final-science/UNIFORM-FOUR-COUNT-CERTIFICATES.jsonl.gz",
           "U05":"third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz",
           "U06":"final-science/UNIFORM-SEPTIC-CERTIFICATES.jsonl.gz",
           "U07":"final-science/UNIFORM-OCTIC-CERTIFICATES.jsonl.gz",
           "U08":"final-science-v2/UNIFORM-NONIC-CERTIFICATES.jsonl.gz",
           **{u:"final-science/COMPACT-CERTIFICATES.jsonl.gz" for u in ("U09","U10","U11")}}
COMPONENT_CHECKERS = {"geometry":"verify_box_geometry.py","algebra":"verify_box_algebra.py",
                      "bounds":"verify_box_bounds.py","early":"verify_early_terminals.py","final":"verify_box_final_bindings.py"}
COMPONENT_TOTALS = {"geometry":619875,"algebra":620370,"bounds":469728,"early":3647,"final":495}
MASKS = {6:"6476e879783b219411d69ccb015d1cbfdec7540834575d4ab593f5b3ad1701c0",
         7:"bb595b3914ce05105743e9386f2cc64a4d2ae2d59df0d340c3221b8b74d7cd9c"}
VERSIONS = {
    "portable-box-components.py":"b899b55f6a0304bc1890208c14ab311964146925f68e1f3431efa373213bfc7e",
    "portable-box-composition.py":"87eff618145c2d94d4f2dffe4d5267ed4f9f77e9988f72c80057ab5400b5358e",
    "portable-box-code/portable_run.py":"de2ae53528ea1819a5e8a41d5d4f5f811b377ce6155b40f2dc1e776485d2f2a7",
    "portable-box-code/verify_box_composition.py":"9e3f4bfac1ca9f57e4087ec7a37d06bdb4000d988312bf152a0ac08721cfc9c3",
    "portable-box-code/SOURCE-MAP.json":"5fa5b9d1e91de235fa59ec310bd0452c3598567d324986239aabbca3f9589fc9",
    "portable-box-numerics/common.py":"2766854c99969c2c2fead4217a2e35cb6f1e3069bb9ff3e045c0d73d4ee568d5",
    "portable-box-numerics/numerical_indices.py":"05f1426c541874a5b82a859b5282b0e4cd5f84967afdf9ce25c9f6a5bd1c1781",
    "portable-box-numerics/numerics.py":"a6d3cbb53409baa7fefdad19ee471d8c864428564d5d7988ac120a55347b7e50",
    "portable-box-numerics/SOURCE-MAP.json":"32544b17066bbf9c54c9931707328d7801088bc70454a10344016412825c9518",
    "portable-box-numerics/originals/accept_legacy_prefix.py":"a7c9304aa09a93083afd442d2f73de42fb68ac257ac98638789807a430311882",
    "portable-box-numerics/originals/index_legacy_tail_recounts.py":"1d019a0c9e2e27ba1c07480c045c4aec72d8f6e3e24a313419b6c6fec499e9af",
    "portable-box-numerics/originals/recount_records.py":"f62a78a78f1d38452fb805ca051c89fe1dabf26d0d2c0d6a900c9200fd6aa4e7",
    "portable-box-numerics/originals/v2_independent_hive_recount.cpp":"093c6a8eb69958aaea519c3946b3a2e6ee32636ba9dcb218cd5bc88b8fd12dcc",
}
NUMERICS_ADAPTER_SHA="bcd65c34e136c1ab51fe405a7851fc9dd9d82332a89c51d1027b51cfd696ef1e"
NUMERICS_SCHEDULED_SHA="8f89cfaa7f815d3e198abaa3aa7420725d9c3db46332a15358d6e5af25ded366"
AGGREGATE_ORIGINAL_AST_SHA="133111f509636c151d061107ae87fa9dbb19c2bd6de6b06503940f2b966baccc"
AGGREGATE_EXECUTED_AST_SHA="8e0f818ccdf2c459f750c0627caf667f4bc7167ced4d56697ad00ee96c5be8a5"


class Failure(ValueError):pass
class Missing(RuntimeError):pass
class Candidate(RuntimeError):pass


def need(ok,message):
    if not ok:raise Failure(message)
def encoded(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def json_pairs(items):
    out={}
    for k,v in items:
        need(k not in out,"Duplicate JSON key");out[k]=v
    return out
def decode(raw):return json.loads(raw,object_pairs_hook=json_pairs)
def integer(x):
    need(type(x) is int,"Exact integer identity/grade required");return x
def exact_count(x):
    if type(x) is str:
        need(re.fullmatch(r"0|[1-9][0-9]*",x),"Malformed decimal count");x=int(x)
    need(type(x) is int and x>=0,"A refusal/fraction/bool is not a count");return x
def rational(x):
    if isinstance(x,Q):return x
    need(type(x) is int or type(x) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?",x),"Exact rational required")
    return Q(x)
def plain(path):
    p=Path(path).absolute();need(not any(q.is_symlink() for q in (p,*p.parents)),"Symlink path refused");return p.resolve()
def relative(name):
    need(type(name) is str and name and "\\" not in name and ":" not in name and all(ord(x)>=32 for x in name),"Malformed relative source")
    p=Path(name);need(not p.is_absolute() and str(p)==name and all(x not in (".","..") for x in p.parts),"Source path escapes its declared root")
    return name
def signature(path):
    s=Path(path).stat();return s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns
def pin(path):
    p=plain(path);need(p.is_file(),"Missing regular file: "+str(p));before=signature(p);h=hashlib.sha256()
    with p.open("rb") as f:
        while raw:=f.read(1024*1024):h.update(raw)
    need(signature(p)==before,"File changed while hashing")
    return {"path":str(p),"bytes":before[2],"sha256":h.hexdigest()}
def save(path,value):
    with Path(path).open("xb") as f:f.write(encoded(value)+b"\n");f.flush();os.fsync(f.fileno())
def bare(value):
    if isinstance(value,dict):value=[value[k] for k in ("lambda","mu","nu")]
    need(isinstance(value,(list,tuple)) and len(value)==3,"Missing entire triple");out=[]
    for p in value:
        need(isinstance(p,(list,tuple)) and all(type(x) is int and x>=0 for x in p) and list(p)==sorted(p,reverse=True),"Malformed partition")
        p=list(p)
        while p and p[-1]==0:p.pop()
        out.append(p)
    need(sum(out[0])==sum(out[1])+sum(out[2]),"Unbalanced entire triple");return out
def record_id(z):return integer(z.get("group_id",z.get("target_ordinal",z.get("id"))))
def insert(table,key,value):
    need(key not in table,"Duplicate exact identity: "+str(key));table[key]=value
def option(words,flag,many=False):
    need(words.count(flag)==1,"Missing/duplicate option: "+flag);i=words.index(flag)+1
    if many:
        end=next((j for j in range(i,len(words)) if words[j].startswith("--")),len(words));return words[i:end]
    need(i<len(words),"Missing option argument");return words[i]
def pointer(value,text):
    if not text:return value
    need(text.startswith("/"),"Invalid JSON pointer")
    for part in text[1:].split("/"):
        part=part.replace("~1","/").replace("~0","~")
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value
def evidence(*groups):
    out={}
    for group in groups:
        for p in group if isinstance(group,list) else [group]:
            q={k:p[k] for k in ("path","sha256")}
            need(q["path"] not in out or out[q["path"]]==q,"Conflicting evidence hash");out[q["path"]]=q
    return [out[k] for k in sorted(out)]


class Guard:
    def __init__(self,recipe,seconds=100):
        self.recipe=recipe;self.end=time.monotonic()+seconds;self.used={};self.stats={};self.cache={};self.executions={};self.sealed_stamps={}
        self.roots=[plain(recipe[k]) for k in ("data_root","code_root","components_root","numerics_root","composition_root","work_root")]
        self.data,self.code=self.roots[:2];self.current=None
        self.core=plain(recipe["core_code_root"]);self.roots.append(self.core)
        self.tool_paths={str(Path(sys.executable).resolve())};self.declarations={}
    def tick(self):
        if time.monotonic()>=self.end:raise Missing("Internal deadline; unvisited terminals remain pending")
    def path(self,path):
        p=plain(path)
        need(any(p.is_relative_to(r) for r in self.roots) or str(p) in self.tool_paths,"Input escapes explicit portable roots: "+str(p))
        return p
    def pin(self,path):
        self.tick();p=self.path(path);name=str(p)
        if not p.is_file():raise Missing("Missing required portable source/body: "+name)
        if name not in self.used:
            self.used[name]=pin(p);self.stats[name]=signature(p)
        else:need(signature(p)==self.stats[name],"Source changed since its byte hash")
        return self.used[name]
    def bound(self,p):
        current=self.pin(p["path"])
        need(current["sha256"]==p["sha256"] and ("bytes" not in p or current["bytes"]==p["bytes"]),"Stale source/execution binding")
        return current
    def read(self,path):
        p=self.pin(path);need(p["bytes"]<150_000_000,"Large roster needs the streamed reader")
        raw=Path(p["path"]).read_bytes();need(sha(raw)==p["sha256"],"Input changed before parse");return decode(raw)
    def lines(self,path):
        p=self.pin(path);opener=gzip.open if p["path"].endswith(".gz") else open
        with opener(p["path"],"rb") as f:
            for n,raw in enumerate(f):
                self.tick();need(raw.endswith(b"\n") and raw.strip(),"Incomplete JSONL source")
                yield n,decode(raw),raw
    def finish(self):
        for path,stamp in self.stats.items():self.tick();need(signature(path)==stamp,"Input changed during acceptance")
        for path,stamp in self.sealed_stamps.items():
            self.tick();need(signature(path)==stamp and not Path(path).stat().st_mode&0o222,"Sealed composition index changed during acceptance")
        return [self.used[k] for k in sorted(self.used)]
    def manifest(self,p):
        document=self.read(self.bound(p)["path"]);need(document["schema"]=="early-input-manifest-v1","Portable relative source manifest is missing")
        for row in document["files"]:
            name=relative(row["path"]);wanted={"path":str(self.data/name),"bytes":row["bytes"],"sha256":row["sha256"]}
            need(name not in self.declarations or self.declarations[name]==wanted,"Conflicting source manifests")
            self.declarations[name]=wanted
    def source(self,name):
        name=relative(name)
        if name not in self.declarations:raise Missing("No portable whole-file source declaration for "+name)
        return self.bound(self.declarations[name])
    def artifact(self,execution,p):
        q=self.bound(p);need(execution["outputs"].get(Path(q["path"]).name)==q,"File is not an actual output of its execution")
        return q
    def portable_fixed_inputs(self,c):
        core=self.core;base=str(self.data/"namespaces/base");masks=[]
        if c["checker"] in ("verify_box_geometry.py","verify_early_terminals.py","verify_box_final_bindings.py"):
            for rank,expected in MASKS.items():
                p=self.pin(Path(base)/f"methods/frontier-025-2026-09-10/science/results/F025-MASK-R{rank}-001.json")
                need(p["sha256"]==expected,"Wrong original-mask premise bytes");masks.append(p)
        need(c["geometry_configuration"]=={"data_root":str(self.data),"box_geometry.CANONICAL":base,"box_geometry_early.CANONICAL":base,
             "mask_inputs":masks,"mask_validation":"exact_source_bytes" if masks else "not_used_by_this_command_or_help_only",
             "upstream_theorem_status_inferred":False},
             "Portable geometry configuration/mask roster differs")
        expected=[self.pin(core/"SOURCE-MAP.json"),self.pin(core/"portable_run.py"),*self.core_copies.values(),
                  self.pin(Path(sys.executable).resolve()),*masks]
        single={"--index","--manifest","--snapshot","--input","--source-manifest","--required-ids","--accepted-verifier-source"}
        many={"--results","--reports","--acceptances","--aggregates"}
        words=c["checker_argv"]
        for flag in single|many:
            if flag in words:
                values=option(words,flag,many=flag in many)
                if flag in many:expected.extend(self.pin(p) for p in values)
                else:expected.append(self.pin(values))
        if c["checker"]=="verify_box_composition.py" and "--source" in words:
            expected.append(self.pin(self.data/"namespaces"/relative(option(words,"--source"))))
        actual={}
        for p in c["fixed_inputs"]:insert(actual,p["path"],self.bound(p))
        need(actual=={p["path"]:p for p in expected},"Missing/extra exact declared portable input binding")
    def portable(self,result_path,checker,work_root):
        key=str(self.path(result_path))
        folder=Path(key).parent;need(folder.parent==plain(work_root),"Foreign portable execution root")
        if key in self.executions:
            cached=self.executions[key]
            need(cached.get("config",{}).get("checker")==checker and cached["config"]["work_root"]==str(plain(work_root)),
                 "Cached execution belongs to another checker/workspace")
            return cached
        ep=self.pin(folder/"EXECUTION.json");e=self.read(ep["path"]);cp=self.bound(e["configuration"]);c=self.read(cp["path"])
        need(cp==self.pin(folder/"CONFIGURATION.json"),"Configuration belongs to another execution directory")
        need(e["schema"]==c["schema"]=="portable-box-execution-v1" and e["checker"]==c["checker"]==checker and
             e["disposition"]=="exited" and e["cleanup_verified"] is True and e["fixed_inputs_unchanged"] is True and not e["source_errors"],
             "Missing/partial/stale portable checker execution")
        need(c["work_root"]==str(plain(work_root)) and c["data_root"]==str(self.data) and c["output_root"]==str(folder)
             and c["id"]==folder.name and c["help_only"] is False and not c["mutable_paths"],"Wrong portable checker roots/mutation scope")
        core=self.core;need(self.path(c["source_map"]["path"])==core/"SOURCE-MAP.json","Foreign code source map")
        self.bound(c["source_map"])
        for name,p in c["copied_sources"].items():
            need(self.path(p["path"])==core/relative(name),"Copied source escaped declared code root");self.bound(p)
        need(c["copied_sources"]==self.core_copies,"Incomplete/mixed copied checker source roster")
        need(checker in c["copied_sources"],"Missing exact checker code")
        self.portable_fixed_inputs(c)
        outputs={}
        for p in e["outputs"]:
            q=self.bound(p);need(Path(q["path"]).parent==folder,"Escaped checker output");insert(outputs,Path(q["path"]).name,q)
        need(set(outputs)=={p.name for p in folder.iterdir() if p.is_file() and p.name!="EXECUTION.json"} and
             all(p.is_file() and not p.is_symlink() for p in folder.iterdir()),"Missing/extra nonregular portable output member")
        need({"result.json","LAUNCH.json","CONFIGURATION.json","APPLIED-CONFIGURATION.json"}<=outputs.keys(),"Missing actual checker result/launch/configuration")
        launch=self.read(folder/"LAUNCH.json");applied=self.read(folder/"APPLIED-CONFIGURATION.json")
        need(integer(e["pid"])==integer(e["pgid"])==integer(launch["pid"])==integer(launch["pgid"])==integer(applied["pid"])>0
             and applied["configuration"]==cp and applied["before_mathematical_calls"] is True,"Wrong actual child identity")
        base=str(self.data/"namespaces/base")
        need(applied["applied"]=={"box_geometry.CANONICAL":base,"box_geometry_early.CANONICAL":base},"Old/canonical geometry root used")
        expected=[str(Path(sys.executable).resolve()),"-I","-S","-B",str(core/"portable_run.py"),"_child","--configuration",cp["path"],"--configuration-sha256",cp["sha256"]]
        need(launch["command"]==expected,"Wrong actual portable child command")
        result=None if checker=="verify_box_composition.py" else self.read(key)
        need(self.pin(key)==outputs["result.json"],"Wrong output result pin")
        need(c["checker_argv"]==c["requested_checker_args"]+["--output",key],"Checker argv/output was changed")
        early_prefix=checker=="verify_early_terminals.py" and result is not None and result.get("status") in ("CANNOT_CHECK","PARTIAL")
        need((integer(e["child_returncode"])==0 and e["status"]=="CHECKER_EXITED_ZERO") or
             (early_prefix and integer(e["child_returncode"])!=0 and e["status"]=="CHECKER_NONZERO_EXIT"),
             "A nonzero component has no authenticated reusable early prefix")
        if result is not None:need(result["status"]==e["checker_status"],"Component result/execution status differs")
        record={"body":result,"pin":outputs["result.json"],"execution":ep,"outputs":outputs,"config":c,"receipt":e,
                "evidence":evidence(outputs["result.json"],ep,cp,outputs["LAUNCH.json"])}
        self.executions[key]=record;return record
    def numeric(self,result_path,nrecipe):
        key=str(self.path(result_path))
        folder=Path(key).parent;nroot=Path(self.recipe["numerics_root"])
        need(folder.parent==nroot/"jobs","Foreign numerical execution root")
        if key in self.executions:
            cached=self.executions[key];rp=self.pin(nroot/"RECIPE.json")
            need(cached.get("request",{}).get("recipe")==rp and self.read(rp["path"])==nrecipe,"Cached numerical source epoch differs")
            return cached
        ep=self.pin(folder/"EXECUTION.json");e=self.read(ep["path"]);rp=self.bound(e["request"]);r=self.read(rp["path"])
        recipe_pin=self.bound(r["recipe"])
        need(recipe_pin==self.pin(nroot/"RECIPE.json") and self.read(recipe_pin["path"])==nrecipe,"Mixed numerical recipe")
        need(nrecipe["code"]==self.numeric_code,"Numerical code package differs from the frozen source roster")
        need(e["schema"]==r["schema"]=="portable-box-numerics-v1" and e["disposition"]=="exited" and
             e["cleanup_verified"] is True and e["sources_unchanged"] is True and not e["source_errors"],"Unfinished/stale numerical execution")
        ncode=self.code/"portable-box-numerics"
        driver=numeric_execution_source(self,nrecipe,r,rp)
        numeric_adapter_fields(r,e)
        expected=[str(Path(sys.executable).resolve()),"-I","-S","-B",driver["path"],"_child","--request",rp["path"],"--request-sha256",rp["sha256"]]
        need(e["command"]==expected and r["id"]==folder.name and r["output"]==key,"Wrong numerical child request/output")
        need(math.isfinite(e["elapsed_seconds"]) and e["elapsed_seconds"]>=0,"Missing actual elapsed execution")
        for p in [*r["inputs"],*nrecipe["code"],*nrecipe["metadata"].values()]:self.bound(p)
        outputs={}
        for p in e["outputs"]:
            q=self.bound(p);need(Path(q["path"]).parent==folder,"Escaped numerical output");insert(outputs,Path(q["path"]).name,q)
        need(set(outputs)=={p.name for p in folder.iterdir() if p.is_file() and p.name!="EXECUTION.json"} and
             all(p.is_file() and not p.is_symlink() for p in folder.iterdir()),"Numerical output member roster differs")
        need({"result.json","LAUNCH.json","CHILD.json"}<=outputs.keys(),"Missing actual numerical child/outputs")
        launch=self.read(folder/"LAUNCH.json");child=self.read(folder/"CHILD.json")
        numeric_adapter_fields(r,child)
        need(launch["command"]==expected and integer(launch["pid"])==integer(launch["pgid"])==integer(child["pid"])==integer(e["pid"])==integer(e["pgid"])>0
             and child["request"]==rp and child["code"]==nrecipe["code"] and child["before_mathematical_calls"] is True,"Wrong numerical actual PID/code/request")
        base=str(self.data/"namespaces/base")
        need(child["configured_geometry_roots"]=={"box_geometry":base,"box_geometry_early":base},"Numerical job used a historical geometry root")
        z=self.read(key);numeric_adapter_fields(r,z)
        need(z["source_bytes_verified_before_after"] is True and z["status"]==e["result_status"],"Numerical source finalization failed")
        if r.get("active_adapter") and z["kind"]=="aggregate":
            proof=z.get("aggregation_adapter")
            if z["status"]!="PARTIAL" or proof is not None:
                need(proof=={"active_adapter":r["active_adapter"],"original_wrapper":self.pin(ncode/"originals/recount_records.py"),
                    "original_aggregate_ast_sha256":AGGREGATE_ORIGINAL_AST_SHA,"executed_aggregate_ast_sha256":AGGREGATE_EXECUTED_AST_SHA,
                    "change":"One final matched_keys=set(matched); both original set(matched) expressions use that cache; exact inverse AST equality checked."},
                    "Aggregate lacks its exact executed adapter/preserved predicate provenance")
        expected_exit=0 if z["status"] in ("BUILT_OWN_COUNTER","FROZEN_LITERAL_ROSTER","FROZEN_RECOUNT_JOBS","SLICE_RECOUNTS_MATCH","COMPLETE_FROZEN_RECOUNTS_MATCH") else 2 if z["status"]=="PARTIAL" else 1
        need(integer(e["child_returncode"])==expected_exit,"Typed numerical result contradicts actual exit")
        for p in z.get("inputs",[]):self.bound(p)
        record={"body":z,"pin":outputs["result.json"],"execution":ep,"request":r,"outputs":outputs,"receipt":e,
                "evidence":evidence(outputs["result.json"],ep,rp,outputs["LAUNCH.json"])}
        self.executions[key]=record;return record


class JSONReader:
    def __init__(self,stream):self.stream,self.buf,self.pos,self.eof=stream,"",0,False;self.decoder=json.JSONDecoder(object_pairs_hook=json_pairs)
    def fill(self):
        self.buf=self.buf[self.pos:];self.pos=0;block=self.stream.read(1024*1024);self.eof=not block;self.buf+=block
        need(len(self.buf)<128_000_000,"Oversized individual metadata value")
    def peek(self):
        while True:
            while self.pos<len(self.buf) and self.buf[self.pos].isspace():self.pos+=1
            if self.pos<len(self.buf) or self.eof:return self.buf[self.pos:self.pos+1]
            self.fill()
    def char(self,c):need(self.peek()==c,"Malformed streamed JSON");self.pos+=1
    def value(self):
        self.peek()
        while True:
            try:
                value,end=self.decoder.raw_decode(self.buf,self.pos)
                if end==len(self.buf) and not self.eof:self.fill();continue
                self.pos=end;return value
            except json.JSONDecodeError:
                need(not self.eof,"Truncated JSON source");self.fill()


def array_records(path,key,metadata):
    with Path(path).open(encoding="utf-8") as f:
        r=JSONReader(f);r.char("{");seen=set()
        while r.peek()!="}":
            k=r.value();need(type(k) is str and k not in seen,"Duplicate metadata key");seen.add(k);r.char(":")
            if k==key:
                r.char("[")
                while r.peek()!="]":
                    yield r.value()
                    if r.peek()=="]":break
                    r.char(",");need(r.peek()!="]","Trailing array comma")
                r.char("]")
            else:metadata[k]=r.value()
            if r.peek()=="}":break
            r.char(",");need(r.peek()!="}","Trailing object comma")
        r.char("}");need(r.peek()=="" and r.eof and key in seen,"Incomplete/trailing source JSON")


class Journal:
    def __init__(self,path):self.path=Path(path);self.stream=self.path.open("xb");self.events=[]
    def record(self,event):
        self.events.append(event);self.stream.write(encoded(event)+b"\n");self.stream.flush();os.fsync(self.stream.fileno())
    def vector(self,tid,kind,values,details=None):
        values=[rational(x) for x in values];negative=[i for i,x in enumerate(values) if x<0]
        self.record({"terminal_id":tid,"kind":kind,"coefficients_low_to_high":list(map(str,values)),"ordinary_negative_indices":negative,"details":details or {}})
        if negative:raise Candidate("Preserved ordinary-negative "+kind+" before comparisons: "+tid)
        return values
    def close(self):self.stream.close()


def load_math(g):
    base=g.code/"portable-box-numerics/originals"
    path=base/"index_legacy_tail_recounts.py";need(g.pin(path)["sha256"]==VERSIONS["portable-box-numerics/originals/index_legacy_tail_recounts.py"],"Wrong preserved pure tail source")
    spec=importlib.util.spec_from_file_location("_portable_acceptance_tail",path);tail=importlib.util.module_from_spec(spec);spec.loader.exec_module(tail)
    # Inspected top level: stdlib imports, constants and definitions only.
    # Never call index/accept/receipt loaders, whose defaults retain old paths.
    p=base/"accept_legacy_prefix.py";need(g.pin(p)["sha256"]==VERSIONS["portable-box-numerics/originals/accept_legacy_prefix.py"],"Wrong preserved prefix source")
    names={"multiply","evaluate","interpolate_grid","reconstruct_one","original_model"}
    tree=ast.parse(p.read_bytes());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    need({n.name for n in nodes}==names,"Missing inspected pure prefix helper")
    namespace={"Q":Q,"geometry":tail,"triple":tail.triple,"need":need}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),"exec"),namespace)
    return tail,SimpleNamespace(**{n:namespace[n] for n in names})


def node_system(job,node):
    grade=integer(node["grade"]);strict=node["strict"];m=job["model"];d=integer(m["dimension"])
    need(type(strict) is bool and grade>=0 and (not strict or grade>0),"Invalid physical grade/strictness")
    bounds=[]
    for j,s in enumerate(m["unit_selections"]):
        need(s["variable"]==j and s["unit_row"]==[int(k==j) for k in range(d)],"Changed integer selection inverse")
        b=integer(s["base"]);bounds.append([-grade*b,grade*(integer(m["count_boundary_area"])-b)])
    rows=[[grade*integer(r[0])-int(strict and any(r[1:])),*[integer(x) for x in r[1:]]] for r in m["full_rows"]]
    need(len(bounds)==d and all(len(r)==d+1 for r in rows),"Incomplete whole node system")
    return sha(encoded({"bounds":bounds,"rows":rows}))


def physical_nodes(row):
    if row["unit"]=="U02":
        det={("I" if t<0 else "P")+str(abs(integer(t))) for t in row["determining_nodes"]}
        holds={m:{"P"+str(integer(t)) for t in row["unused_hold_nodes"]} for m in ("hive","rows")}
    elif row["kind"]=="FOUR_COUNT":det={"P1","P2","I1","I2"};holds={m:set() for m in ("hive","rows")}
    else:
        det={"P"+str(integer(t)) for t in row["determining_nodes"]};holds={h["model"]:{"P"+str(integer(t)) for t in h["physical_sites"]} for h in row["holdouts"]}
    need(set(holds)=={"hive","rows"} and all(not det&h for h in holds.values()),"Missing paired model or reused hold")
    wanted={(m,k) for m in holds for k in det|holds[m]};seen=set();nodes={}
    for b in row["count_bindings"]:
        if b["status"]!="complete":need(b["status"]=="preserved_refusal","Unknown count binding");continue
        if row["unit"]=="U02":signed=integer(b["signed_node"]);t,s,v=abs(signed),signed<0,exact_count(b["count"])
        else:t,s,v=integer(b.get("original_physical_grade",b["grade"])),b["strict"],exact_count(b["value"])
        need(type(s) is bool,"Nonboolean strict flag");kind=("I" if s else "P")+str(t);model=b["model"]
        need((model,kind) in wanted,"Extra physical source site")
        n=nodes.setdefault(kind,{"kind":kind,"grade":t,"strict":s,"stored":{},"role":"determining" if kind in det else "positive_holdout"})
        need(model not in n["stored"] or n["stored"][model]==v,"Conflicting recorded retry");n["stored"][model]=v;seen.add((model,kind))
    need(seen==wanted,"Missing complete paired source sites")
    return sorted(nodes.values(),key=lambda n:(n["strict"],n["grade"]))


def first_unused_policy(row,original_nodes):
    determining=[integer(t) for t in row["determining_nodes"]];need(len(set(determining))==len(determining),"Repeated determining node")
    new=[];t=1
    while len(new)<2:
        if t not in determining:new.append(t)
        t+=1
    fitting=[n for n in original_nodes if n["role"]=="determining"]
    old=[n for n in original_nodes if n["role"]=="positive_holdout"]
    need([n["grade"] for n in old]==row["unused_hold_nodes"] and len(old)==2,"Wrong original U02 holds")
    if new==row["unused_hold_nodes"]:return original_nodes,False
    coefficients=list(map(rational,row["coefficients"]));holds=[]
    for t in new:
        value=sum(c*t**i for i,c in enumerate(coefficients));need(value.denominator==1 and value>0,"Invalid held polynomial expectation")
        holds.append({"kind":"P"+str(t),"grade":t,"strict":False,"stored":{"polynomial_expectation":int(value)},"role":"replacement_positive_holdout"})
    return sorted(fitting+holds,key=lambda n:(n["strict"],n["grade"])),True


def validate_u02_policy(row,job,original,selected,changed):
    rule="first two positive integers outside the unchanged determining-node set"
    old=[n for n in original if n["role"]=="positive_holdout"]
    expected={"option":"first-unused","rule":rule,"determining_nodes":row["determining_nodes"],
              "geometry_sha256":row["geometry_check"]["original_geometry_sha256"],"certificate_reference":row["certificate"],
              "complete_source_coefficients":row["coefficients"],"original_nodes":original,"required_nodes":selected,"amendment":None}
    if changed:
        held=[n for n in selected if n["role"]=="replacement_positive_holdout"]
        expected["amendment"]={"schema":"portable-u02-exact-holdout-amendment-v1","parent_id":row["id"],"rule":rule,
            "removed_original_node_ids":[f"U02:{row['id']}:{n['kind']}" for n in old],
            "replacement_node_ids":[f"U02:{row['id']}:{n['kind']}" for n in held],"original_holds_remain_supplemental":old,
            "fresh_replacement_counts_still_required":True,"geometry_and_vector_preserved":{"geometry_check":row["geometry_check"],
                "certificate":row["certificate"],"coefficients":row["coefficients"]}}
    need(job["u02_holdout_policy"]==expected,"U02 amendment changed its exact parent/geometry/vector/held-site contract")


def four_count(values,journal,tid):
    A,B,U,V=map(exact_count,values);need(A>0,"Positive-grade nonemptiness is missing")
    d1,d2=8*(A+U)-B-V,16*(A-U)-B+V-30
    journal.record({"terminal_id":tid,"kind":"fresh_four_count_functionals","values":[A,B,U,V],"D1":d1,"D2":d2,"c2":str(Q(d2,24)),
                    "full_coefficient_vector_inferred":False})
    if d2<0:raise Candidate("Preserved a derived whole ordinary coefficient c2<0 before comparison")
    need(d1>=0,"Four-count sufficient c1 criterion is unproved; negative D1 alone is not a whole negative coefficient")
    return {"D1":d1,"D2":d2,"c2":str(Q(d2,24))}


def code_package(g):
    for name,expected in VERSIONS.items():
        path=g.core/name.removeprefix("portable-box-code/") if name.startswith("portable-box-code/") else g.code/name
        actual=g.pin(path)["sha256"]
        accepted={expected,NUMERICS_ADAPTER_SHA,NUMERICS_SCHEDULED_SHA} if name=="portable-box-numerics/numerics.py" else {expected}
        need(actual in accepted,"Wrong frozen code epoch: "+name)
    core=g.core;table=g.read(core/"SOURCE-MAP.json");g.core_copies={}
    need(table["schema"]=="portable-box-source-copies-v1","Missing portable checker source contract")
    for row in table["copies"]:
        name=relative(row["path"]);p=g.pin(core/name)
        need((p["bytes"],p["sha256"])==(row["portable_bytes"],row["portable_sha256"]),"Changed copied checker")
        insert(g.core_copies,name,p)
    ncode=g.code/"portable-box-numerics";table=g.read(ncode/"SOURCE-MAP.json")
    need(table["schema"]=="portable-numerics-originals-v1","Missing preserved pure-function source contract")
    g.numeric_code=[g.pin(ncode/name) for name in ("SOURCE-MAP.json","common.py","numerical_indices.py","numerics.py")]
    for row in table["copies"]:
        p=g.pin(ncode/relative(row["path"]));need((p["bytes"],p["sha256"])==(row["bytes"],row["sha256"]),"Changed original mathematical body")
        g.numeric_code.append(p)


def numeric_adapter_fields(request,record):
    if "active_adapter" in request:
        need(record.get("active_adapter")==request["active_adapter"] and record.get("adapter_transition")==request["adapter_transition"],
             "New numerical receipt/header lost its active adapter or transition")
    else:need("active_adapter" not in record and "adapter_transition" not in record,"Old numerical receipt was relabelled with an adapter")


def numeric_transition(g,p,recipe_pin,driver,adapter):
    nroot=Path(g.recipe["numerics_root"]);tp=g.bound(p)
    need(tp["path"]==str(nroot/"ADAPTER-TRANSITION.json"),"Foreign numerical transition")
    t=g.read(tp["path"])
    need(t["schema"]=="portable-numerics-adapter-transition-v1" and t["active_adapter"]==adapter and
         t["recipe"]==recipe_pin and t["predecessor_driver"]==driver and
         driver["sha256"]==VERSIONS["portable-box-numerics/numerics.py"] and
         t["mathematical_predicate_source"]==VERSIONS["portable-box-numerics/originals/recount_records.py"] and
         t["prior_recipe_receipts_and_counts_unchanged"] is True and integer(t["new_counts_or_aggregates_executed"])==0,
         "Wrong exact predecessor transition/source epoch")
    sp=g.bound(t["state_snapshot"]);old=g.read(sp["path"])
    need(sp["path"]==str(nroot/"ADAPTER-PREDECESSOR-STATE.json") and t["predecessor_state"]["path"]==str(nroot/"STATE.json") and
         all(sp[k]==t["predecessor_state"][k] for k in ("bytes","sha256")) and old["recipe"]==recipe_pin and not old.get("mandatory_holds"),
         "Transition lost its literal pre-existing state bytes")
    attempts=old["attempts"]
    need(integer(t["prior_attempts"])==len(attempts) and [r["id"] for r in attempts]==[f"numerics-{i+1:06d}" for i in range(len(attempts))],
         "Predecessor attempt prefix is incomplete or reordered")
    return {r["id"]:r["request"] for r in attempts}


def numeric_execution_source(g,nrecipe,request,request_pin=None):
    ncode=g.code/"portable-box-numerics";nroot=Path(g.recipe["numerics_root"])
    driver=g.pin(ncode/"numerics.py");recipe_pin=g.pin(nroot/"RECIPE.json")
    need(driver in nrecipe["code"] and driver["sha256"] in (VERSIONS["portable-box-numerics/numerics.py"],NUMERICS_ADAPTER_SHA,NUMERICS_SCHEDULED_SHA),
         "Numerical recipe has an unaccepted literal driver")
    adapter=request.get("active_adapter")
    if adapter is not None:
        ap=g.bound(adapter)
        if ap["sha256"]==NUMERICS_SCHEDULED_SHA:
            need(driver==ap and ap["path"]==str(ncode/"numerics.py") and request.get("adapter_transition") is None and
                 not (nroot/"ADAPTER-TRANSITION.json").exists(),"Scheduled driver requires its own fresh recipe and exact path")
        else:
            need(ap["sha256"]==NUMERICS_ADAPTER_SHA and ap["path"] in (str(ncode/"numerics.py"),str(ncode/"numerics_successor.py")),"Stale or foreign active numerical adapter")
        transition=request.get("adapter_transition")
        if driver==ap:need(transition is None,"Fresh successor recipe cannot inherit an old journal")
        else:
            need(transition is not None,"Missing exact predecessor transition")
            old=numeric_transition(g,transition,recipe_pin,driver,ap)
            if request_pin is not None:need(request["id"] not in old,"Old request was relabelled as a successor call")
        if request_pin is not None:
            need(ap in request["inputs"] and (transition is None or transition in request["inputs"]),"Active adapter/transition was not a declared prelaunch input")
        return ap
    need(driver["sha256"]==VERSIONS["portable-box-numerics/numerics.py"] and "adapter_transition" not in request,"Unpinned successor or relabelled old request")
    transition_path=nroot/"ADAPTER-TRANSITION.json"
    if request_pin is not None and transition_path.exists():
        tp=g.pin(transition_path);t=g.read(tp["path"]);ap=g.bound(t["active_adapter"])
        need(ap["sha256"]==NUMERICS_ADAPTER_SHA and ap["path"]==str(ncode/"numerics_successor.py"),"Unknown continuation adapter")
        old=numeric_transition(g,tp,recipe_pin,driver,ap)
        need(old.get(request["id"])==request_pin,"Old numerical request is outside the literal predecessor prefix")
    return driver


def requirement_unit(tid):
    parts=tid.split(":",2);need(len(parts)==3,"Malformed terminal ID")
    if parts[0]=="adopted":need(parts[1] in ("FRE","FRI-settled"),"Unaccepted family");return "LEGACY"
    need(parts[0] in ("numeric","production") and parts[1] in COUNTS,"Unknown requirement namespace");return parts[1]


def requirement_hash(row):return sha(encoded({k:row[k] for k in ("terminal_id","predicate","binding")}))


def required_rows(g,unit=None):
    path=g.recipe["requirements"]["path"];g.bound(g.recipe["requirements"])
    execution=g.portable(path,"verify_box_composition.py",g.recipe["composition_root"])
    need(execution["config"]["command"]=="requirements","An old/theorem flag cannot replace a new export")
    metadata={};selected=[];totals=Counter();last=None
    for row in array_records(path,"requirements",metadata):
        g.tick();tid=row["terminal_id"]
        need(type(tid) is str and (last is None or last<tid) and row["predicate"]==PREDICATE,"Missing/duplicate/unordered literal requirements")
        last=tid;u=requirement_unit(tid);totals[u]+=1
        if unit is None:selected.append((tid,requirement_hash(row)))
        elif u==unit:selected.append(row)
    need(metadata["status"]=="REQUIREMENTS_ONLY" and metadata["kind"]=="requirements" and not metadata["missing_slices"] and
         metadata["checker_sha256"]==VERSIONS["portable-box-code/verify_box_composition.py"] and
         metadata["start"]==0 and metadata["stop"]==metadata["total"]==metadata["required_terminal_count"]==TOTAL and dict(totals)==COUNTS,
         "Incomplete or foreign fresh requirement export")
    snapshot_path=option(execution["config"]["checker_argv"],"--snapshot");snapshot=g.read(snapshot_path)
    need(snapshot["kind"]=="snapshot" and snapshot["status"]=="INDEX_SNAPSHOT_ONLY" and
         g.pin(snapshot_path)["sha256"]==metadata["snapshot_sha256"],"Wrong freshly sealed composition index")
    db=g.path(snapshot["database_path"])
    need(db.is_relative_to(Path(g.recipe["composition_root"])) and not db.stat().st_mode&0o222 and list(signature(db))==snapshot["database_stamp"],
         "Sealed composition database identity changed")
    g.sealed_stamps[str(db)]=tuple(snapshot["database_stamp"])
    return selected,execution,metadata


def component_workspace(g,component,meta,require_frozen=True):
    need(component in COMPONENT_CHECKERS and meta["schema"]=="portable-box-components-v1" and meta["component"]==component and
         meta["status"]=="PASS_COMPONENT_CONDITIONAL_ON_RECORDED_COUNTS_AND_SEPARATE_PREMISES","Wrong completed component report interface")
    rp=g.bound(meta["recipe"]);recipe=g.read(rp["path"]);root=plain(recipe["work_root"])
    composition=plain(g.recipe["composition_root"])
    need(root!=composition and root.is_relative_to(composition) and rp["path"]==str(root/"RECIPE.json"),
         "Component recipe is outside its exact workspace beneath the composition root")
    need(recipe["schema"]=="portable-box-components-v1" and recipe["data_root"]==str(g.data) and recipe["code_root"]==str(g.core) and
         recipe["controller"]==g.pin(g.code/"portable-box-components.py") and recipe["controller"]["sha256"]==VERSIONS["portable-box-components.py"] and
         recipe["launcher"]==g.pin(g.core/"portable_run.py") and recipe["source_map"]==g.pin(g.core/"SOURCE-MAP.json") and
         recipe["copied_sources"]==g.core_copies and meta["aggregator"]==recipe["controller"],"Wrong component controller/core source epoch")
    workspace={"work_root":str(root),"recipe":rp}
    if require_frozen:
        mapping=g.recipe["component_workspaces"]
        need(set(mapping)==set(COMPONENT_CHECKERS) and mapping[component]==workspace,"Component workspace/recipe differs from the complete frozen map")
    return workspace,recipe


def component_rows(g,component,unit,wanted):
    path=g.recipe["component_reports"][component]["path"];g.bound(g.recipe["component_reports"][component]);meta={};selected={};seen=set();count=0
    for row in array_records(path,"exact_source_identities",meta):
        g.tick();key=(row["unit"],integer(row["id"]));need(key not in seen,"Duplicate component identity");seen.add(key);count+=1
        if key[0]==unit and key[1] in wanted:insert(selected,key[1],row)
    need(meta["schema"]=="portable-box-components-v1" and meta["status"]=="PASS_COMPONENT_CONDITIONAL_ON_RECORDED_COUNTS_AND_SEPARATE_PREMISES" and
         meta["component"]==component and meta["records"]==count==COMPONENT_TOTALS[component] and meta["all_literal_source_identities_once"] is True,
         "Component aggregate is incomplete or source-only")
    workspace,recipe=component_workspace(g,component,meta)
    g.manifest(recipe["metadata"]["source-manifest.json"])
    need(meta["aggregator"]==recipe["controller"] and meta["aggregator"]["sha256"]==VERSIONS["portable-box-components.py"],"Wrong component aggregator source")
    g.bound(meta["aggregator"]);g.bound(meta["frozen_roster"])
    for p in [recipe["controller"],recipe["launcher"],recipe["source_map"],*recipe["copied_sources"].values(),*recipe["metadata"].values()]:g.bound(p)
    for p in meta["checked_current_sources"].values():g.bound(p)
    need(set(selected)==wanted,"A requested component identity is missing")
    execution_refs={}
    for r in meta["executions"]:insert(execution_refs,r["result"]["sha256"],r)
    result={};by_execution={}
    for idx,row in selected.items():by_execution.setdefault(row["execution_id"],[]).append(idx)
    for eid,ids in by_execution.items():
        sample=selected[ids[0]];ref=execution_refs.get(sample["result_sha256"])
        if ref is None:raise Missing("Component aggregate lacks the exact scientific execution reference: "+eid)
        e=g.portable(ref["result"]["path"],COMPONENT_CHECKERS[component],workspace["work_root"])
        need(Path(e["pin"]["path"]).parent.name==eid and e["pin"]==ref["result"] and e["execution"]==ref["execution"],"Component execution source was swapped")
        z=e["body"];need(z["status"] in ("PASS_CONDITIONAL_ON_RECORDED_COUNTS","CANNOT_CHECK","PARTIAL") if component=="early" else z["status"]=="PASS","Unfinished component predicate")
        lp=e["outputs"].get("result.identities.jsonl")
        if lp is None:raise Missing("Missing execution-bound component identity JSONL: "+eid)
        ledger=g.artifact(e,lp);actual={}
        for _,r,raw in g.lines(ledger["path"]):
            idx=integer(r["id"])
            if idx in ids:insert(actual,idx,(r,raw))
        need(set(actual)==set(ids),"Component ledger omitted a required identity")
        for idx in ids:
            r,raw=actual[idx];declared=selected[idx]
            need(declared["result_sha256"]==e["pin"]["sha256"] and declared["execution_id"]==eid,"Component row names a different execution")
            component_identity(component,declared,r)
            result[idx]={"identity":r,"raw":raw,"declared":declared,"execution":e,
                                        "evidence":evidence(g.pin(path),ledger,e["evidence"])}
    return result


def component_identity(component,declared,row):
    fields={"algebra":["id","ordinal","unit","row_sha256","bare_triple"],
            "early":["id","ordinal","unit"],"geometry":["id","bare_triple","geometry_sha256","actual_degree"],
            "final":["id","bare_triple","geometry_sha256"],"bounds":["id","ordinal","geometry_sha256"]}[component]
    need(all(declared[k]==row[k] for k in fields),"Component declared identity differs from its exact execution ledger")
    if component=="early":need(declared["row_sha256"]==row["certificate"]["record_sha256"],"Early component source row differs")
    if component=="final":need(declared["row_sha256"]==row["certificate_sha256"],"Final component source row differs")
    if component=="bounds":need(declared["row_sha256"]==row["compact_source"]["sha256"],"Bound component source row differs")


def numerical_rows(g,unit,wanted):
    found={};fragment_refs={};nrecipe=None;report_pins=[]
    for declared in g.recipe["numerical_reports"]:
        g.bound(declared);meta={};seen=set();count=0;local={}
        for row in array_records(declared["path"],"exact_source_and_node_roster",meta):
            g.tick();key=(row["unit"],integer(row["id"]));need(key not in seen,"Duplicate numerical global identity");seen.add(key);count+=1
            if key[0]==unit and key[1] in wanted:insert(local,key[1],row)
        need(meta["schema"]=="portable-box-numerics-v1" and meta["kind"]=="global_count_evidence" and meta["mode"]=="full" and
             meta["status"]=="FULL_LITERAL_COUNT_EVIDENCE_COMPLETE_PENDING_MATHEMATICAL_JOINS" and meta["records"]==count,
             "Representative/partial/source-only numerical evidence cannot close the box")
        population={"all":TOTAL,"production":620370,"U02":169,"U03":3478,"legacy":297}
        need(meta["cohort"] in population and count==population[meta["cohort"]],"Numerical global cohort population is incomplete")
        if not local:continue
        r=g.read(g.bound(meta["recipe"])["path"])
        need(r["work_root"]==g.recipe["numerics_root"] and r["data_root"]==str(g.data) and r["mode"]=="full","Numerical roots/mode differ")
        numeric_execution_source(g,r,meta)
        if nrecipe is None:nrecipe=r
        else:need(nrecipe==r,"Mixed numerical recipe epochs")
        g.tool_paths.add(str(plain(r["compiler"]["path"])));g.bound(r["compiler"])
        for p in [*r["code"],*r["metadata"].values()]:g.bound(p)
        g.manifest(r["metadata"]["source_manifest"])
        for idx,row in local.items():insert(found,idx,row)
        report_pins.append(declared)
        for f in meta["fragments"]:
            key=f["index"]["sha256"]
            need(key not in fragment_refs or fragment_refs[key]==f,"Conflicting numerical fragment")
            fragment_refs[key]=f
    need(set(found)==wanted and nrecipe is not None,"Missing full numerical evidence for exact selected IDs")
    results={};groups={}
    for idx,row in found.items():groups.setdefault(row["index"]["sha256"],[]).append(idx)
    for key,ids in groups.items():
        f=fragment_refs.get(key)
        if f is None:raise Missing("Global numerical identity lacks its literal fragment contract")
        ix=g.numeric(f["index"]["path"],nrecipe);m=ix["body"]
        need(ix["pin"]==f["index"] and ix["execution"]==f["index_execution"] and m["kind"]=="manifest" and
             m["selection_complete"] is True and m["wrapper_sha256"]==VERSIONS["portable-box-numerics/originals/recount_records.py"],"Wrong numerical index execution")
        op=ix["request"]["operation"]
        need(op["kind"]=="index" and m["explicit_source_records"]==op["records"] and m["source_roster"]==op["roster"] and
             m["source_slice"]==op["slice"] and m["expected_record_ids"]==sorted(r["id"] for r in op["records"]) and
             [e["id"] for e in m["records"]]==[r["id"] for r in op["records"][:len(m["records"])]] and
             m["pending_index_ids"]==sorted(set(m["expected_record_ids"])-{e["id"] for e in m["records"]}),"Index did not preserve its complete requested source prefix")
        need(len({e["id"] for e in m["records"]})==len(m["records"]),"Duplicate emitted index record")
        need(f["accepted_actual_source_slice"]==[op["slice"][0],op["slice"][0]+len(m["records"])],"Global fragment has a skipped or fictitious source span")
        jobs_pin=g.artifact(ix,m["jobs"]);entries={};jobs={};offset=0
        with Path(jobs_pin["path"]).open("rb") as stream:
            for ordinal,entry in enumerate(m["records"]):
                need(entry["ordinal"]==ordinal and entry["offset"]==offset,"Index offsets/ordinals omit a physical record")
                raw=stream.read(integer(entry["bytes"]));offset+=len(raw);need(sha(raw)==entry["sha256"],"Index job bytes changed")
                job=decode(raw);idx=integer(job["id"])
                need(idx==entry["id"] and job["geometry_sha256"]==entry["geometry_sha256"] and
                     entry["node_ids"]==[f"{job['unit']}:{idx}:{n['kind']}" for n in job["nodes"]],"Wrong frozen physical node roster")
                if idx in ids:insert(entries,idx,entry);jobs[idx]=job
            need(stream.read(1)==b"" and offset==jobs_pin["bytes"],"Index job file has unaccounted bytes")
        need(set(entries)==set(ids),"Missing selected numerical job")
        for idx in ids:
            original={k:v for k,v in found[idx].items() if k not in ("roster_key","stream","node_ids","index","count_aggregate")}
            need(original==op["records"][entries[idx]["ordinal"]],"Global numerical identity was swapped from its exact source roster")
        aggregate=g.numeric(f["aggregate"]["path"],nrecipe);a=aggregate["body"]
        all_nodes=sorted(n for e in m["records"] for n in e["node_ids"])
        need(aggregate["pin"]==f["aggregate"] and aggregate["execution"]==f["aggregate_execution"] and
             a["status"] in ("COMPLETE_FROZEN_RECOUNTS_MATCH","PARTIAL") and a["manifest_sha256"]==key and
             a["complete_record_ids"]==sorted(e["id"] for e in m["records"]) and a["matched_node_ids"]==all_nodes and
             not a["pending_node_ids"] and not a["mismatches"] and a["pending_index_record_ids"]==m["pending_index_ids"],"Incomplete exact emitted-fragment aggregate")
        need(aggregate["request"]["operation"]["manifest"]==ix["pin"],"Aggregate used another index")
        expected_reports=aggregate["request"]["operation"]["reports"]
        need(expected_reports==[r["report"] for r in f["counts"]],"Global numerical fragment omitted/changed count report list")
        rows={};count_evidence=[]
        for ref in f["counts"]:
            run=g.numeric(ref["report"]["path"],nrecipe);z=run["body"]
            need(run["pin"]==ref["report"] and run["execution"]==ref["execution"] and z["kind"]=="run" and
                 z["manifest_sha256"]==key and run["request"]["operation"]["manifest"]==ix["pin"],"Wrong new count execution/index")
            need(ix["pin"] in run["request"]["inputs"] and jobs_pin in run["request"]["inputs"],"Counts lack pre-existing index/job source dependency")
            build=g.numeric(z["build_reference"]["path"],nrecipe);b=build["body"]
            need(build["pin"]==z["build_reference"] and b["status"]=="BUILT_OWN_COUNTER" and b["binary"]==z["build"] and
                 b["source"]==z["counter_source"] and b["source"]["sha256"]==VERSIONS["portable-box-numerics/originals/v2_independent_hive_recount.cpp"],"Counter binary/source/build epoch differs")
            need(b["command"]==[nrecipe["compiler"]["path"],"-std=c++17","-O2","-Wall","-Wextra",b["source"]["path"],"-o",b["binary"]["path"]],"Counter was not built by the declared exact compiler command")
            g.artifact(build,b["binary"]);g.bound(b["source"])
            lp=g.artifact(run,z["results"]);count_evidence.extend(evidence(run["evidence"],lp,build["evidence"]))
            for _,row,raw in g.lines(lp["path"]):
                idx=integer(row["id"])
                if idx not in jobs:continue
                job=jobs[idx];nodes={n["kind"]:n for n in job["nodes"]};kind=row["kind"]
                need(kind in nodes,"Extra physical count in selected parent");node=nodes[kind];nid=f"{unit}:{idx}:{kind}"
                need(row["node_id"]==row["counter"]["id"]==nid and integer(row["record_ordinal"])==entries[idx]["ordinal"] and
                     row["geometry_sha256"]==job["geometry_sha256"] and integer(row["grade"])==node["grade"] and type(row["strict"]) is bool and
                     row["strict"]==node["strict"] and row["stored"]==node["stored"] and row["full_system_sha256"]==node_system(job,node),
                     "Fresh count lost its exact geometry/grade/full-system binding")
                if row["counter"]["status"]=="complete":
                    exact_count(row["counter"]["count"]);insert(rows,nid,row)
                else:need(row["status"]=="REFUSED" and row["counter"]["status"].startswith("REFUSED_") and row["counter"].get("count") is None,"Refusal supplied a scalar")
        for idx in ids:
            needed=entries[idx]["node_ids"];need(all(n in rows for n in needed),"Missing complete fresh physical site")
            need(found[idx]["node_ids"]==needed and found[idx]["count_aggregate"]==aggregate["pin"],"Global numerical node/aggregate binding differs")
            results[idx]={"job":jobs[idx],"entry":entries[idx],"rows":{n:rows[n] for n in needed},"declared":found[idx],
                          "index":ix,"aggregate":aggregate,"recipe":nrecipe,"evidence":evidence(report_pins,ix["evidence"],aggregate["evidence"],count_evidence)}
    return results


def raw_compacts(g,unit,wanted,audit=False):
    if audit:name="namespaces/u12/AUDIT/U11-COMPLETE-VECTORS/COMPACT-CERTIFICATES.jsonl.gz"
    elif unit=="U02":name="namespaces/u02/DATA/U02/two-model-mixed-certificate.json"
    elif unit=="U03":name="namespaces/u03/DATA/U03/hybrid-verification-v3/certificates.jsonl"
    else:name=f"namespaces/{unit.lower()}/DATA/{unit}/{COMPACT[unit]}"
    source=g.source(name);out={};seen=set();total=0
    rows=((i,r,encoded(r)) for i,r in enumerate(g.read(source["path"])["records"])) if unit=="U02" else g.lines(source["path"])
    for ordinal,row,raw in rows:
        idx=record_id(row);need(idx not in seen,"Duplicate original compact ID");seen.add(idx);total+=1
        if idx in wanted:out[idx]=(ordinal,row,raw,source)
    need(total==({"U02":211,"U03":4131}.get(unit,COUNTS[unit])) and set(out)==wanted,"Missing/extra literal compact source IDs")
    return out


def compare_u11(original,audited):
    need(set(original)==set(audited),"U11/U12 field roster differs")
    differences={k for k in original if original[k]!=audited[k]}
    need(differences<={"determination_audit"},"U11/U12 changed a mathematical or used source field")
    return sorted(differences)


def count_agreement(numeric):
    job=numeric["job"]
    for node in job["nodes"]:
        row=numeric["rows"][f"{job['unit']}:{job['id']}:{node['kind']}"];value=exact_count(row["counter"]["count"])
        need(all(value==exact_count(v) for v in node["stored"].values()) and row["status"]=="MATCH" and
             row["matches"]=={k:True for k in node["stored"]},"Fresh complete count rejects a stored source/expectation")


def production_binding(required,ordinal,record,raw,algebra,geometry,bound,numeric):
    unit=required["terminal_id"].split(":")[1];idx=record_id(record);d=integer(record.get("actual_dimension",int(unit[1:])+1))
    need((bound is None)==(unit in ("U04","U11")),"A required formal-bound component is absent")
    gh=record["geometry"]["sha256"] if unit=="U05" else record["geometry_sha256"]
    geom=geometry["identity"];alg=algebra["identity"];job=numeric["job"]
    need(integer(geom["id"])==idx and integer(geom["actual_degree"])==d and geom["geometry_sha256"]==gh,
         "Production geometry/actual degree detached from compact")
    parts=bare(geom["bare_triple"])
    need(bare(job["bare_triple"])==parts and job["geometry_sha256"]==gh and job["id"]==idx and job["unit"]==unit and
         integer(job["model"]["dimension"])==d,"Count model is not the proved whole geometry")
    need(alg["unit"]==unit and integer(alg["id"])==idx and integer(alg["ordinal"])==ordinal and alg["row_sha256"]==sha(raw),
         "Algebra does not bind the literal compact bytes/ordinal")
    if record.get("bare_triple") is not None:need(bare(record["bare_triple"])==parts,"Compact original triple differs")
    if alg.get("bare_triple") is not None:need(bare(alg["bare_triple"])==parts,"Algebra original triple differs")
    binding=required["binding"]
    need(binding["id"]==str(idx) and integer(binding["ordinal"])==ordinal and binding["source"]==f"{unit.lower()}/DATA/{unit}/{COMPACT[unit]}" and
         binding["record_encoding"]=="raw-line-with-newline" and binding["record_sha256"]==sha(raw) and bare(binding["literal_triple"])==parts,
         "Fresh composition requirement has another literal/source identity")
    declared=numeric["declared"]
    need(declared["compact"]=="namespaces/"+binding["source"] and declared["compact_sha256"]==sha(raw) and declared["source_ordinal"]==ordinal,
         "Numerical original compact selector changed")
    cref=job["certificate_reference"];cref=cref["compact"] if "compact" in cref else cref
    need(cref["sha256"]==sha(raw),"Count index lacks the exact compact source binding")
    nodes=numeric["entry"]["node_ids"]
    need(len(nodes)==len(set(nodes))==(d+3 if unit=="U11" else d-1),"Wrong complete production physical-node roster")
    if bound is not None:
        b=bound["identity"]
        need(integer(b["id"])==idx and b["unit"]==unit and integer(b["actual_degree"])==d and
             b["geometry_sha256"]==gh and bare(b["bare_triple"])==parts and b["compact_source"]["sha256"]==sha(raw),
             "Formal interval premises detached from the exact geometry/compact")
    count_agreement(numeric)
    return {"geometry_sha256":gh,"actual_degree":d,"literal_triple":parts,"fresh_node_ids":nodes}


def prove_production(g,unit,required,numeric):
    wanted={int(r["binding"]["id"]) for r in required}
    algebra=component_rows(g,"algebra",unit,wanted)
    geometry=component_rows(g,"final" if unit=="U11" else "geometry",unit,wanted)
    bounds={} if unit in ("U04","U11") else component_rows(g,"bounds",unit,wanted)
    compacts=raw_compacts(g,unit,wanted);bridge={}
    if unit=="U11":
        # Even a requested U11 slice binds the complete 495-row bridge.
        all_ids={integer(r["id"]) for _,r,_ in g.lines(g.source("namespaces/u11/DATA/U11/"+COMPACT[unit])["path"])}
        original=raw_compacts(g,unit,all_ids);audited=raw_compacts(g,unit,all_ids,True)
        for idx in all_ids:
            a,b=original[idx],audited[idx];need(a[0]==b[0],"U11/U12 order changed")
            bridge[idx]={"differences":compare_u11(a[1],b[1]),"u11_raw_sha256":sha(a[2]),"u12_raw_sha256":sha(b[2])}
        need(len(bridge)==495,"Incomplete U11/U12 mathematical bridge")
    for required_row in required:
        g.tick();idx=int(required_row["binding"]["id"]);g.current=required_row["terminal_id"]
        ordinal,record,raw,source=compacts[idx];a=algebra[idx];geom=geometry[idx];b=bounds.get(idx)
        need(a["declared"]["row_sha256"]==sha(raw),"Algebra aggregate lost exact source row")
        if unit=="U11":need(geom["identity"]["certificate_sha256"]==bridge[idx]["u12_raw_sha256"],"Final raw binding lost U12 source row")
        if b:
            execution=b["execution"];z=execution["body"]
            index_path=option(execution["config"]["checker_argv"],"--index")
            ix=g.portable(index_path,"verify_box_bounds.py",g.recipe["component_workspaces"]["bounds"]["work_root"]);index=ix["body"]
            need(index["status"]=="FROZEN_INPUTS_NOT_VERIFIED" and z["index_sha256"]==ix["pin"]["sha256"] and
                 z["verifier_sha256"]==g.core_copies["verify_box_bounds.py"]["sha256"],"Wrong actual formal-bound checker/index epoch")
            frozen=index["expected"][integer(b["identity"]["ordinal"])]
            need(frozen["id"]==idx and frozen["compact_sha256"]==sha(raw) and frozen["sha256"]==b["identity"]["job_sha256"] and
                 frozen["proof_identities"]==[p["identity"] for p in b["identity"]["proofs"]],"Missing/replaced finite bound proof identity")
        details=production_binding(required_row,ordinal,record,raw,a,geom,b,numeric[idx])
        if unit=="U11":details["complete_U11_U12_bridge"]=bridge[idx]
        refs=evidence(source,a["evidence"],geom["evidence"],[] if b is None else b["evidence"],numeric[idx]["evidence"])
        yield required_row,refs,details


def early_required_binding(required,record,job):
    unit=record["unit"];idx=integer(record["id"]);ref=record["certificate"]
    need(job["unit"]==unit and job["id"]==idx and job["certificate_reference"]==ref,"Early source/index identity changed")
    source=ref["path"];need(source.startswith("namespaces/"),"Early source lacks portable relative namespace")
    match=re.fullmatch(r"records\[([0-9]+)\]",ref["locator"])
    if match:ordinal=int(match[1]);encoding="canonical-json-object"
    else:
        match=re.fullmatch(r"line:([1-9][0-9]*)",ref["locator"]);need(match is not None,"Unknown early source locator")
        ordinal=int(match[1])-1;encoding="raw-line-with-newline"
    expected={"role":"early2" if unit=="U02" else "early3","id":str(idx),"source":source.removeprefix("namespaces/"),"ordinal":ordinal,
              "record_sha256":ref["record_sha256"],"record_encoding":encoding,"literal_triple":bare(job["bare_triple"])}
    need(required["terminal_id"]==f"numeric:{unit}:{idx}" and required["binding"]==expected,"Early requirement literal/source binding changed")


def early_polynomial(record,job,rows,tail,journal,tid):
    original=physical_nodes(record)
    if record["unit"]=="U02":
        selected,changed=first_unused_policy(record,original);policy=job["u02_holdout_policy"]
        need(policy["option"]=="first-unused" and policy["original_nodes"]==original and policy["required_nodes"]==selected and
             policy["determining_nodes"]==record["determining_nodes"] and policy["complete_source_coefficients"]==record["coefficients"] and
             policy["geometry_sha256"]==job["geometry_sha256"] and bool(policy["amendment"])==changed,"U02 first-unused policy changed")
        validate_u02_policy(record,job,original,selected,changed)
    else:selected,changed=original,False
    need(job["nodes"]==selected,"Count index omitted or changed fitting/selected held nodes")
    values={n["kind"]:exact_count(rows[f"{job['unit']}:{job['id']}:{n['kind']}"]["counter"]["count"]) for n in selected}
    if record["kind"]=="FOUR_COUNT":
        geom=record["geometry_check"]
        need(record["unit"]=="U03" and geom["actual_dimension_proved"] is True and geom["short_normal_bound_checked"] is True and
             integer(geom["checked_chart_dimension_upper_bound"])==5==integer(job["model"]["dimension"]),"Four-count actual-degree/metric premise missing")
        fresh=four_count([values[k] for k in ("P1","P2","I1","I2")],journal,tid)
        need(all(str(record["algebra"][k])==str(v) for k,v in fresh.items()),"Recorded four-count algebra differs from fresh counts")
        return {"kind":"FOUR_COUNT","fresh_functionals":fresh,"full_coefficient_vector_inferred":False,"short_normal_top_three_premise_retained":True}
    need(record["kind"]=="FULL_VECTOR","Unknown early proof kind")
    nodes=[integer(t) for t in record["determining_nodes"]];d=integer(job["model"]["dimension"])
    need(len(nodes)==len(set(nodes))==d+1 and 0 in nodes,"Incomplete degree-bound interpolation roster")
    witness=next(((n["kind"],values[n["kind"]]) for n in selected if n["grade"]>0 and values[n["kind"]]>0),None)
    need(witness is not None,"Artificial grade zero cannot establish nonemptiness")
    need(values["P0"]==1,"Nonempty constant disagrees with complete zero-grade count")
    if any(t<0 for t in nodes):
        need(record["geometry_check"]["actual_dimension_proved"] is True and integer(record["actual_degree"])==d and
             job["model"]["actual_dimension_required_and_proved"] is True,"Reciprocity parity lacks actual dimension")
    samples=[[t,str(values[("I" if t<0 else "P")+str(abs(t))]*((-1)**d if t<0 else 1))] for t in nodes]
    coefficients=tail.interpolate(samples)
    journal.vector(tid,"fresh_reconstructed_early",coefficients,{"samples":samples,"nonempty_witness":witness,"held_values_not_used_in_interpolation":True})
    source=journal.vector(tid,"prior_early_source_vector",record["coefficients"])
    need(coefficients==source,"Fresh full early vector differs from prior source vector")
    holds=[]
    for n in selected:
        if n["role"] not in ("positive_holdout","replacement_positive_holdout"):continue
        t=n["grade"];need(t>0 and t not in nodes,"A held grade was used to fit")
        need(sum(c*t**k for k,c in enumerate(coefficients))==values[n["kind"]],"Fresh unused early hold rejects the vector")
        holds.append({"grade":t,"value":str(values[n["kind"]]),"provenance":list(n["stored"]),"used_for_interpolation":False})
    need(len(holds)>=2,"Missing unused early positive holds")
    return {"kind":"FULL_VECTOR","coefficients_low_to_high":list(map(str,coefficients)),"samples":samples,"unused_holds":holds,"U02_first_unused_amended":changed}


def prove_early(g,unit,required,numeric,tail,journal):
    wanted={int(r["binding"]["id"]) for r in required};components=component_rows(g,"early",unit,wanted)
    ledgers={}
    for requirement in required:
        g.tick();idx=int(requirement["binding"]["id"]);tid=requirement["terminal_id"];g.current=tid;n=numeric[idx];job=n["job"]
        ix=n["index"];lp=g.artifact(ix,ix["body"]["fresh_early_bindings"])
        if lp["path"] not in ledgers:ledgers[lp["path"]]={r["id"]:(r,raw,i) for i,r,raw in g.lines(lp["path"])}
        record,raw,local=ledgers[lp["path"]][idx]
        need(record["status"]=="PASS_CONDITIONAL_ON_RECORDED_COUNTS" and job["source_binding_record"]=={"path":lp["path"],"line":local+1,"sha256":sha(raw)},
             "Numerical index does not bind its prior complete early vector ledger")
        prior=components[idx]["identity"]
        excluded={"ordinal","source_references"}
        need({k:v for k,v in prior.items() if k not in excluded}=={k:v for k,v in record.items() if k not in excluded},"Portable early science and count-index predicates differ")
        need(job["geometry_sha256"]==record["geometry_check"]["original_geometry_sha256"] and
             job["model"]["dimension"]==record["geometry_check"]["checked_chart_dimension_upper_bound"],"Early whole-model geometry changed")
        if unit=="U02":
            need(n["recipe"]["holdouts"]=="first-unused","This acceptance requires the exact first-unused U02 rule")
            roster=n["index"]["request"]["operation"]["roster"]
            r=g.numeric(roster["path"],n["recipe"]);need(r["pin"]==roster and r["body"]["status"]=="FROZEN_LITERAL_ROSTER","First-unused policy lacks a preceding complete roster execution")
            source=n["index"]["body"]["explicit_source_records"][n["entry"]["ordinal"]]
            need(source["u02_holdout_policy"]==job["u02_holdout_policy"],"U02 policy changed after its pre-count source freeze")
        early_required_binding(requirement,record,job)
        details=early_polynomial(record,job,n["rows"],tail,journal,tid)
        count_agreement(n)
        details.update(geometry_sha256=job["geometry_sha256"],fresh_node_ids=n["entry"]["node_ids"],vector_precedes_count_requests_via_index_dependency=True)
        yield requirement,evidence(components[idx]["evidence"],lp,n["evidence"]),details


class LegacySources:
    def __init__(self,g,nrecipe):
        self.g=g;self.meta=nrecipe["metadata"];self.document=g.read(g.bound(self.meta["legacy_vectors"])["path"])
        self.chosen=g.read(g.bound(self.meta["chosen_terminals"])["path"]);self.catalog={};self.aliases={};self.cache={}
        for p in self.document["inputs"]:
            q={k:p[k] for k in ("path","bytes","sha256")};need(q["path"] not in self.catalog or self.catalog[q["path"]]==q,"Conflicting old source catalog")
            self.catalog[q["path"]]=q
        plan=g.read(g.bound(self.meta["copy_plan"])["path"])
        for p in plan["members"]:
            if p["action"]!="copy_bytes" or p.get("projection"):continue
            target=relative(p["target"]);need(target.startswith("data/"),"Whole source is outside data asset")
            self.aliases.setdefault((p["source_bytes"],p["source_sha256"]),[]).append(target[5:])
    def resolve(self,ref):
        old={k:ref[k] for k in ("path","bytes","sha256")}
        protected=("SLR-FQB-WI226-FABLE068-FRONTIER-REPAIR-001/delivery/SLR-FABLE-DISCOVERY-068/provider-output",
                   "SLR-FQF-WI230-FABLE068-METHOD-SEAL-001/delivery/provider-output",
                   "SLR-FQH-WI236-FABLE068-SOURCE-SEPARATED-001/delivery/.claude")
        need(not any(p in old["path"] for p in protected),"Protected owner-residue body is not an admissible dependency")
        need(self.catalog.get(old["path"])==old,"Source pointer lacks original whole-file catalog identity")
        # The historical path is only an opaque dictionary key.
        choices=sorted(self.aliases.get((old["bytes"],old["sha256"]),[]))
        if not choices:raise Missing("No whole-file portable source body for legacy SHA "+old["sha256"])
        name=choices[0];p=self.g.source(name);need((p["bytes"],p["sha256"])==(old["bytes"],old["sha256"]),"Portable source alias bytes differ")
        if name not in self.cache:
            raw=Path(p["path"]).read_bytes();self.cache[name]=decode(gzip.decompress(raw) if name.endswith(".gz") else raw)
        return self.cache[name],p
    def verify(self,source,journal):
        tid=source["terminal_id"];raw=journal.vector(tid,"selected_legacy_source",source["coefficients_low_to_high"])
        ref=source["vector_reference"];doc,p=self.resolve(ref);actual=pointer(doc,ref["json_pointer"])
        journal.vector(tid,"literal_original_legacy_source",actual)
        need(list(map(rational,actual))==raw and sha(encoded(pointer(doc,ref["record_pointer"])))==ref["record_sha256"],"Legacy original full source row/vector differs")
        tref=source["triple_reference"];t,tp=self.resolve(tref);need(bare(pointer(t,tref["json_pointer"]))==bare(source["bare_triple"]),"Legacy actual source triple pointer differs")
        refs=[p,tp]
        for extra in source.get("additional_vector_sources",[]):
            r={**ref,**extra} if extra.get("same_source_file") else extra;doc,p=self.resolve(r);v=pointer(doc,r["json_pointer"])
            journal.vector(tid,"alternate_original_legacy_source",v);need(list(map(rational,v))==raw,"Conflicting alternate source vector");refs.append(p)
        return refs


def reconstruct_legacy(source,job,count_rows,tail,prefix,journal):
    idx=integer(source["id"]);tid=source["terminal_id"]
    values={nid:exact_count(r["counter"]["count"]) for nid,r in count_rows.items()}
    if idx<272:
        model=prefix.original_model(source["bare_triple"]);need(model["rank"]<=7 and
             set(job["model"])==set(model)|{"geometry_premise"} and all(job["model"][k]==v for k,v in model.items()),"Prefix full ambient original model differs")
        d=model["dimension"];need(job["ambient_degree_upper_bound"]==d and
             [n["kind"] for n in job["nodes"]]==[f"P{t}" for t in range(d+3)] and not any(n["strict"] for n in job["nodes"]),"Prefix full ambient determining/unused grid incomplete")
        record={"id":idx,"terminal_id":tid,"bare_triple":job["bare_triple"],"terminal_source_triple":source["terminal_source_triple"],
                "binding":source["source_to_terminal_binding"],"geometry_sha256":job["geometry_sha256"],"degree_upper_bound":d}
        raw=prefix.reconstruct_one(record,values);coefficients=list(map(rational,raw["coefficients_low_to_high"]))
        journal.vector(tid,"fresh_reconstructed_legacy_prefix",coefficients,raw)
        holds=[[t,str(values[f"LEGACY:{idx}:P{t}"])] for t in (d+1,d+2)];actual=None
    else:
        gate=tail.verified_interpolation_samples(job,list(count_rows.values()))
        need(len(gate["samples"])==gate["degree_upper_bound"]+1 and
             len({p[0] for p in gate["samples"]})==len(gate["samples"]),"Tail interpolation does not fill the proven degree bound")
        coefficients=tail.interpolate(gate["samples"])
        journal.vector(tid,"fresh_reconstructed_legacy_tail",coefficients,{"gated_samples":gate,"actual_dimension_before_parity":gate["actual_dimension"]})
        holds=gate["unused_holds"];actual=gate["actual_dimension"];d=gate["degree_upper_bound"]
    source_vector=journal.vector(tid,"legacy_source_comparison",source["coefficients_low_to_high"])
    need(len(source_vector)<=len(coefficients) and coefficients==source_vector+[Q(0)]*(len(coefficients)-len(source_vector)),"Fresh entire legacy polynomial differs from original source vector")
    for t,value in holds:need(t>0 and sum(c*t**i for i,c in enumerate(coefficients))==rational(value),"Fresh unused legacy hold rejects the vector")
    return {"coefficients_low_to_high":list(map(str,coefficients)),"degree_upper_bound":d,"actual_dimension":actual,
            "actual_dimension_used_for_parity":idx>=272 and job["node_plan"]["mode"]=="mixed_pending_positive_anchor","unused_holds":holds}


def prove_legacy(g,required,numeric,tail,prefix,journal):
    reader=LegacySources(g,next(iter(numeric.values()))["recipe"]);document=reader.document
    sources={};chosen={}
    for r in document["records"]:insert(sources,integer(r["id"]),r)
    need(set(sources)==set(range(297)) and document["expected_record_ids"]==list(range(297)),"Incomplete exact legacy 272+25 source roster")
    for c in reader.chosen["choices"]:
        if c["family"] in ("FRE","FRI-settled"):insert(chosen,c["terminal_id"],c)
    by_terminal={r["terminal_id"]:r for r in sources.values()};need(len(by_terminal)==len(chosen)==297 and set(by_terminal)==set(chosen),"Legacy terminal/source selection differs")
    for requirement in required:
        tid=requirement["terminal_id"];g.current=tid;source=by_terminal[tid];idx=source["id"];n=numeric[idx];job=n["job"];choice=chosen[tid]
        journal.vector(tid,"selected_legacy_source_intake",source["coefficients_low_to_high"])
        need(job["terminal_id"]==tid and job["id"]==idx and job["source_id"]==source["source_id"]==choice["source_id"] and
             bare(job["bare_triple"])==bare(source["bare_triple"]) and bare(job["terminal_source_triple"])==bare(source["terminal_source_triple"])==bare(choice["source_triple"]),"Legacy source/terminal identity swapped")
        need(source["family"]==choice["family"]==tid.split(":")[1] and source["chosen_seed_key"]==choice["seed_key"],"Legacy family/selected source-order witness differs")
        need(job["source_to_terminal_binding"]==source["source_to_terminal_binding"]==tail.bind_triples(source["bare_triple"],source["terminal_source_triple"]),"Unsupported legacy source-to-terminal operation")
        need(job["certificate_reference"]==source["vector_reference"] and job["original_execution_identity"]==source["original_execution_identity"],"Legacy original source hash/identity changed")
        if idx>=272:
            original=tail.original_hive(source["bare_triple"]);rank=original["rank"]
            name=f"namespaces/base/methods/frontier-025-2026-09-10/science/results/F025-MASK-R{rank}-001.json"
            mp=g.source(name);need(mp["sha256"]==tail.MASK_SHA[rank],"Wrong adopted forcing table")
            accepted=tail.canonical_mask(g.read(mp["path"]),rank,original["boundary_mask"])
            ref={**mp,"json_pointer":f"/records/{original['boundary_mask']}","record_sha256":sha(encoded(accepted))}
            expected=tail.make_job(source,original,accepted,ref)
            need(all(job[k]==expected[k] for k in ("model","chart_proof","geometry_sha256","geometry_reference","degree_upper_bound")),
                 "Tail original whole hive/forcing/saturated chart differs")
        pointer_match=re.fullmatch(r"/sources/([0-9]+)",choice["family_source_pointer"])
        need(pointer_match is not None,"Missing exact adopted family source ordinal")
        ordinal=int(pointer_match[1])
        expected_binding={"role":"family","id":source["source_id"],"source":"u03/DATA/U03/known-join/source-roster.json","ordinal":ordinal,
                          "record_sha256":choice["family_source_record_sha256"],"record_encoding":"canonical-json-object","literal_triple":bare(source["terminal_source_triple"])}
        need(requirement["binding"]==expected_binding,"Fresh legacy requirement lost literal source membership")
        details=reconstruct_legacy(source,job,n["rows"],tail,prefix,journal)
        if idx>=272:need({k:v for k,v in job.items() if k not in ("portable_source_metadata","original_source_pointer_validation")}==expected,
                        "Tail selected source/node plan differs")
        refs=reader.verify(source,journal);count_agreement(n)
        details.update(original_legacy_id=idx,geometry_sha256=job["geometry_sha256"],source_vector_reference=source["vector_reference"],
                       source_to_terminal_binding=source["source_to_terminal_binding"])
        yield requirement,evidence(refs,n["evidence"],reader.meta["legacy_vectors"],reader.meta["chosen_terminals"]),details


PREMISES = [
    "The classical integer hive/LR-tableau correspondence identifies each checked full H-system with the entire LR coefficient.",
    "LR stretching is polynomial; the checked chart/ambient dimension bounds its degree, and positive-grade nonemptiness supplies constant one.",
    "Ehrhart reciprocity uses the actual dimension, proved before parity when strict nodes are used.",
    "The short-normal/top-coefficient positivity theorem is used only with the actual-dimensional metric hypotheses checked by the relevant component gate.",
    "The adopted F025 forcing/Horn/census and earlier Ferudun theorem premises retain their original externally reviewed scope; this acceptance does not repeat the huge census.",
    "Only proved trailing-zero and inner-exchange relations bind legacy source triples to their exact selected terminal identities.",
]


def child_verify(recipe,operation,output):
    g=Guard(recipe,operation.get("seconds",100));journal=Journal(output.with_suffix(".raw-vectors.jsonl"));rows_path=output.with_suffix(".bindings.jsonl")
    result={"schema":SCHEMA,"kind":"slice","status":"PARTIAL","unit":operation["unit"],"slice":[operation["start"],operation["stop"]],
            "checker_sha256":sha(Path(__file__).read_bytes()),"requirements":recipe["requirements"],"records":0,"complete":False,
            "ordinary_negative_observations":[],"premises":PREMISES,"fresh_counters_or_builds_performed":0,"whole_theorem_accepted":False}
    try:
        code_package(g);all_required,req_exec,meta=required_rows(g,operation["unit"])
        all_required.sort(key=lambda r:(integer(r["binding"]["ordinal"]),r["terminal_id"]))
        start,stop=operation["start"],operation["stop"]
        need(0<=start<stop<=len(all_required)==COUNTS[operation["unit"]],"Invalid/incomplete exact unit slice")
        required=all_required[start:stop];result["expected_terminal_ids"]=[r["terminal_id"] for r in required]
        unit=operation["unit"]
        if unit=="LEGACY":
            nrecipe=g.read(Path(recipe["numerics_root"])/"RECIPE.json")
            doc=g.read(g.bound(nrecipe["metadata"]["legacy_vectors"])["path"])
            lookup={r["terminal_id"]:integer(r["id"]) for r in doc["records"]}
            wanted={lookup[r["terminal_id"]] for r in required}
        else:wanted={int(r["binding"]["id"]) for r in required}
        numeric=numerical_rows(g,unit,wanted)
        tail,prefix=load_math(g) if unit in ("U02","U03","LEGACY") else (None,None)
        iterator=prove_production(g,unit,required,numeric) if unit in COMPACT else prove_early(g,unit,required,numeric,tail,journal) if unit in ("U02","U03") else prove_legacy(g,required,numeric,tail,prefix,journal)
        checked=[]
        with rows_path.open("xb") as stream:
            for requirement,refs,details in iterator:
                g.tick();tid=requirement["terminal_id"];need(tid not in checked,"Duplicate accepted slice terminal")
                row={"schema":ROW_SCHEMA,"terminal_id":tid,"predicate":requirement["predicate"],"binding":requirement["binding"],
                     "evidence":evidence(refs,req_exec["evidence"]),"mathematical_details":details}
                stream.write(encoded(row)+b"\n");checked.append(tid)
        need(checked==result["expected_terminal_ids"],"Slice omitted an exact required identity")
        result.update(status="COMPLETE_PORTABLE_TERMINAL_SLICE",complete=True,records=len(checked),checked_terminal_ids=checked,
                      bindings=pin(rows_path),input_pins=g.finish(),source_bytes_unchanged=True,
                      source_stability="Exact byte hashes at first read, full file identity/modification stamps rechecked at completion")
    except Candidate as exc:
        result.update(status="HOLD_ORDINARY_NEGATIVE",error=str(exc),current_terminal=g.current)
    except (Missing,KeyError,FileNotFoundError) as exc:
        result.update(status="CANNOT_CHECK",error=f"Required portable contract missing: {type(exc).__name__}: {exc}",current_terminal=g.current)
    except (Failure,ValueError,TypeError,IndexError,OSError) as exc:
        result.update(status="FAIL",error=f"{type(exc).__name__}: {exc}",current_terminal=g.current)
    finally:
        journal.close();result["raw_vectors"]=pin(journal.path)
        result["ordinary_negative_observations"]=[r for r in journal.events if r.get("ordinary_negative_indices") or r.get("kind")=="fresh_four_count_functionals" and rational(r["c2"])<0]
        save(output,result)
    return 0 if result["complete"] else 3 if result["status"]=="HOLD_ORDINARY_NEGATIVE" else 2


def acceptance_execution(g,path):
    folder=Path(path).parent;ep=g.pin(folder/"EXECUTION.json");e=g.read(ep["path"]);rp=g.bound(e["request"]);r=g.read(rp["path"])
    need(folder.parent==Path(g.recipe["work_root"])/"jobs" and r["id"]==folder.name and
         rp["path"]==str(Path(g.recipe["work_root"])/"requests"/(folder.name+".json")),"Acceptance execution escaped its exact new work epoch")
    need(e["schema"]==SCHEMA and e["kind"]=="execution" and e["disposition"]=="exited" and e["child_returncode"]==0 and
         e["cleanup_verified"] is True and e["sources_unchanged"] is True,"Unfinished new acceptance execution")
    need(r["recipe"]==g.recipe["recipe_pin"] and r["operation"]["kind"]=="verify" and r["output"]==str(Path(path)),"Acceptance belongs to another recipe/operation")
    outputs={}
    for p in e["outputs"]:
        q=g.bound(p);need(Path(q["path"]).parent==folder,"Escaped acceptance output");insert(outputs,Path(q["path"]).name,q)
    need(set(outputs)=={p.name for p in folder.iterdir() if p.is_file() and p.name!="EXECUTION.json"} and
         all(p.is_file() and not p.is_symlink() for p in folder.iterdir()),"Missing/extra acceptance output member")
    need({"result.json","CHILD.json","LAUNCH.json"}<=outputs.keys(),"Acceptance lacks actual child/launch/result")
    child=g.read(folder/"CHILD.json");launch=g.read(folder/"LAUNCH.json")
    expected_command=[str(Path(sys.executable).resolve()),"-I","-S","-B",g.recipe["checker_source"]["path"],"_child",
                      "--request",rp["path"],"--request-sha256",rp["sha256"]]
    need(integer(launch["pid"])==integer(launch["pgid"])==integer(child["pid"])==integer(e["pid"])==integer(e["pgid"])>0 and
         child["before_mathematical_calls"] is True and child["request"]==rp and child["checker_sha256"]==g.recipe["checker_sha256"] and
         launch["command"]==e["command"]==expected_command,"Wrong actual new acceptance child identity")
    z=g.read(path);need(z["status"]=="COMPLETE_PORTABLE_TERMINAL_SLICE" and z["complete"] is True and
                       z["checker_sha256"]==g.recipe["checker_sha256"] and z["requirements"]==g.recipe["requirements"],"Slice did not earn the exact fresh requirement epoch")
    op=r["operation"]
    need(z["unit"]==op["unit"] and z["slice"]==[op["start"],op["stop"]] and z["records"]==op["stop"]-op["start"] and
         not z["ordinary_negative_observations"],"Acceptance omitted its exact source slice or retains an undispositioned negative")
    for p in z["input_pins"]:g.bound(p)
    need(z["bindings"]==outputs.get("result.bindings.jsonl") and z["raw_vectors"]==outputs.get("result.raw-vectors.jsonl"),"Missing actual slice bindings or preserved raw vectors")
    return z,evidence(g.pin(path),ep,rp),outputs


def child_assemble(recipe,operation,output):
    g=Guard(recipe,operation.get("seconds",100));result={"schema":SCHEMA,"kind":"assembly","status":"PARTIAL","complete":False,
        "checker_sha256":sha(Path(__file__).read_bytes()),"requirements":recipe["requirements"],"whole_theorem_accepted":False,"premises":PREMISES}
    rows_path=output.with_suffix(".bindings.jsonl")
    try:
        code_package(g);items,req_exec,meta=required_rows(g);expected=dict(items);totals=Counter();parts=[]
        need(operation["parts"] and len({p["path"] for p in operation["parts"]})==len(operation["parts"]),"Missing/duplicate slice files")
        with rows_path.open("xb") as out:
            for p in operation["parts"]:
                g.bound(p);z,refs,_=acceptance_execution(g,p["path"]);local=[]
                for _,row,_raw in g.lines(z["bindings"]["path"]):
                    tid=row["terminal_id"];consume_binding(row,expected)
                    need(requirement_unit(tid)==z["unit"] and row["evidence"],"Slice belongs to another unit or lacks evidence")
                    for ref in row["evidence"]:g.bound(ref)
                    row["evidence"]=evidence(row["evidence"],refs);out.write(encoded(row)+b"\n")
                    local.append(tid);totals[z["unit"]]+=1
                need(local==z["checked_terminal_ids"]==z["expected_terminal_ids"] and len(local)==z["records"],"Slice ledger/accepted identity roster differs")
                parts.append(p)
        complete_union(expected,totals)
        result.update(status="COMPLETE_PORTABLE_BOX_TERMINAL_ACCEPTANCE",complete=True,records=TOTAL,counts=dict(totals),
                      bindings=pin(rows_path),slice_results=parts,input_pins=g.finish(),exact_expected_identities_once=True,
                      remaining="Run the fresh composition acceptance/final phases; upstream census/theorem premises and root publication review remain separate.")
    except (Missing,KeyError,FileNotFoundError) as exc:result.update(status="CANNOT_CHECK",error=f"{type(exc).__name__}: {exc}")
    except (Failure,ValueError,TypeError,IndexError,OSError) as exc:result.update(status="FAIL",error=f"{type(exc).__name__}: {exc}")
    save(output,result);return 0 if result["complete"] else 2


def consume_binding(row,expected):
    tid=row["terminal_id"]
    need(row["schema"]==ROW_SCHEMA and tid in expected and requirement_hash(row)==expected[tid],
         "Extra/duplicate/swapped fresh terminal binding")
    del expected[tid]


def complete_union(expected,totals):
    need(not expected and dict(totals)==COUNTS and sum(totals.values())==TOTAL,"Incomplete exact 624314-terminal union")


def prepare(args):
    fields=("data_root","code_root","components_root","numerics_root","composition_root","work_root")
    recipe={k:str(plain(getattr(args,k))) for k in fields};work=Path(recipe["work_root"]);composition=Path(recipe["composition_root"])
    recipe["core_code_root"]=str(plain(args.core_code_root if args.core_code_root is not None else Path(recipe["code_root"])/"portable-box-code"))
    need(not work.exists() and all(Path(recipe[k]).is_dir() for k in fields if k!="work_root"),"Fresh output root and existing explicit prerequisites required")
    need(Path(recipe["core_code_root"]).is_dir(),"Missing explicitly declared immutable core code root")
    need(all(Path(recipe[k]).is_relative_to(composition) and Path(recipe[k])!=composition for k in ("components_root","numerics_root","work_root")),
         "Component/numerical/acceptance evidence must be nested below the new composition root")
    need(all(not work.is_relative_to(Path(recipe[k])) and not Path(recipe[k]).is_relative_to(work)
             for k in ("data_root","code_root","core_code_root")),"Acceptance outputs must be disjoint from immutable data/code/core")
    recipe.update(schema=SCHEMA,checker_sha256=sha(Path(__file__).read_bytes()),checker_source=pin(__file__),
                  component_reports={},component_workspaces={},numerical_reports=[],prepared_without_mathematical_execution=True)
    g=Guard(recipe,600);recipe["requirements"]=g.pin(args.requirements)
    recipe["numerical_reports"]=[g.pin(p) for p in args.numerical_reports]
    code_package(g);g.bound(recipe["checker_source"])
    # Read only each report's component tag, without retaining its large roster.
    for p in args.component_reports:
        actual=g.pin(p)
        metadata={}
        for _ in array_records(p,"exact_source_identities",metadata):pass
        component=metadata["component"];need(component in COMPONENT_CHECKERS and component not in recipe["component_reports"],"Missing/duplicate component metadata")
        recipe["component_reports"][component]=actual
        workspace,_=component_workspace(g,component,metadata,False)
        need(plain(actual["path"]).is_relative_to(Path(workspace["work_root"])),"Aggregate report is outside its declared component workspace")
        recipe["component_workspaces"][component]=workspace
    need(set(recipe["component_reports"])==set(COMPONENT_CHECKERS),"All five completed component report interfaces are required")
    for p in [recipe["requirements"],*recipe["component_reports"].values(),*recipe["numerical_reports"]]:g.bound(p)
    g.finish()
    work.mkdir();(work/"jobs").mkdir();(work/"requests").mkdir();save(work/"RECIPE.json",recipe)
    return {"status":"PREPARED_PORTABLE_ACCEPTANCE_METADATA","recipe":pin(work/"RECIPE.json")}


def read_recipe(work):
    p=pin(plain(work)/"RECIPE.json");r=decode(Path(p["path"]).read_bytes())
    need(r["schema"]==SCHEMA and r["work_root"]==str(plain(work)) and r["checker_sha256"]==sha(Path(__file__).read_bytes()),"Wrong acceptance code/work epoch")
    need(pin(__file__)==r["checker_source"],"New acceptance source path/bytes changed; do not rewrite receipts")
    return {**r,"recipe_pin":p},p


def launch(args,operation):
    recipe,rp=read_recipe(args.work_root);work=Path(recipe["work_root"])
    need(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*",args.id),"Explicit safe fresh execution ID required")
    directory=work/"jobs"/args.id;request_path=work/"requests"/(args.id+".json")
    need(not directory.exists() and not request_path.exists(),"Never replace an old acceptance execution")
    g=Guard(recipe,600);code_package(g)
    request={"schema":SCHEMA,"id":args.id,"recipe":rp,"operation":operation,"output":str(directory/"result.json"),
             "checker_sha256":recipe["checker_sha256"]};save(request_path,request);request_pin=pin(request_path);directory.mkdir()
    path=g.core/"portable_run.py";spec=importlib.util.spec_from_file_location("_acceptance_portable_supervisor",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    # Only the reviewed process supervisor is reused; no old CLI, checker,
    # counter, compiler or mathematical module is invoked through this import.
    command=[str(Path(sys.executable).resolve()),"-I","-S","-B",str(Path(__file__).resolve()),"_child","--request",str(request_path),"--request-sha256",request_pin["sha256"]]
    outcome=module.supervise(command,directory,directory/"stdout.txt",directory/"stderr.txt",120,directory/"LAUNCH.json")
    stable=pin(request_path)==request_pin and pin(rp["path"])==rp and sha(Path(__file__).read_bytes())==recipe["checker_sha256"]
    outputs=[pin(p) for p in sorted(directory.iterdir()) if p.is_file()]
    record={"schema":SCHEMA,"kind":"execution","request":request_pin,"command":command,**outcome,
            "sources_unchanged":stable,"outputs":outputs,"whole_theorem_accepted":False};save(directory/"EXECUTION.json",record)
    return {"status":"CHILD_COMPLETE" if stable and outcome["disposition"]=="exited" and outcome["child_returncode"]==0 and outcome["cleanup_verified"] else "CHILD_NOT_ACCEPTED",
            "result":str(directory/"result.json"),"execution":str(directory/"EXECUTION.json"),"child_returncode":outcome["child_returncode"]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter);subs=parser.add_subparsers(dest="command",required=True)
    p=subs.add_parser("prepare")
    for key in ("data-root","code-root","components-root","numerics-root","composition-root","work-root"):
        p.add_argument("--"+key,type=Path,required=True)
    p.add_argument("--core-code-root",type=Path,help="Immutable checker root; defaults to code-root/portable-box-code")
    p.add_argument("--requirements",type=Path,required=True);p.add_argument("--component-reports",nargs="+",type=Path,required=True)
    p.add_argument("--numerical-reports",nargs="+",type=Path,required=True)
    for name in ("verify","assemble"):
        p=subs.add_parser(name);p.add_argument("--work-root",type=Path,required=True);p.add_argument("--id",required=True)
        p.add_argument("--seconds",type=int,default=100)
        if name=="verify":
            p.add_argument("--unit",choices=COUNTS,required=True);p.add_argument("--start",type=int,default=0);p.add_argument("--stop",type=int)
        else:p.add_argument("--parts",nargs="+",type=Path,required=True)
    p=subs.add_parser("_child",help=argparse.SUPPRESS);p.add_argument("--request",type=Path,required=True);p.add_argument("--request-sha256",required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=="prepare":result=prepare(args)
        elif args.command=="_child":
            request_pin=pin(args.request);need(request_pin["sha256"]==args.request_sha256,"Changed child request")
            request=decode(Path(args.request).read_bytes());rp=request["recipe"];need(pin(rp["path"])==rp,"Changed child recipe")
            recipe=decode(Path(rp["path"]).read_bytes());recipe["recipe_pin"]=rp
            output=plain(request["output"]);need(output.parent==Path(recipe["work_root"])/"jobs"/request["id"] and not output.exists(),"Wrong fresh child output")
            need(sha(Path(__file__).read_bytes())==recipe["checker_sha256"]==request["checker_sha256"],"Changed acceptance checker code")
            save(output.with_name("CHILD.json"),{"schema":SCHEMA,"request":request_pin,"pid":os.getpid(),"checker_sha256":recipe["checker_sha256"],"before_mathematical_calls":True})
            return child_verify(recipe,request["operation"],output) if request["operation"]["kind"]=="verify" else child_assemble(recipe,request["operation"],output)
        else:
            need(1<=args.seconds<=100,"Internal cap must be 1..100 seconds")
            op={"kind":args.command,"seconds":args.seconds}
            if args.command=="verify":op.update(unit=args.unit,start=args.start,stop=COUNTS[args.unit] if args.stop is None else args.stop)
            else:op["parts"]=[pin(p) for p in args.parts]
            result=launch(args,op)
        print(json.dumps(result,sort_keys=True),flush=True)
        return 0 if result["status"] in ("PREPARED_PORTABLE_ACCEPTANCE_METADATA","CHILD_COMPLETE") else 2
    except (Failure,Missing,ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print(json.dumps({"status":"CANNOT_CHECK" if isinstance(exc,(Missing,KeyError,FileNotFoundError)) else "REFUSED","error":f"{type(exc).__name__}: {exc}","whole_theorem_accepted":False}),file=sys.stderr,flush=True)
        return 2


if __name__=="__main__":raise SystemExit(main())
