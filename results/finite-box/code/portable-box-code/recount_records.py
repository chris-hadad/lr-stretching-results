#!/usr/bin/env python3
"""Freeze and independently recount the actual Pro026 closed/interior requests.

Commands:
  build --cpp-source independent_hive_recount.cpp --binary OUT/recount --output OUT/build.json
  index --root UNIT_ROOT --unit U05 --shard shard-000 --output OUT/shard.json
  index --root U11_ROOT --unit U11 --input DATA/U11/inputs/degree11-holds.jsonl.gz
        --output OUT/u11.json
  run --manifest OUT/shard.json --build OUT/build.json --start 0 --limit 10
      --node-ms 500 --max-states 1000000 --output OUT/recount-000.json
  aggregate --manifest OUT/shard.json --reports OUT/recount-*.json --output OUT/aggregate.json

index writes an adjacent .jobs.jsonl file. run writes and flushes an adjacent
.counts.jsonl after every node. --resume-from prior run reports skips their
complete matching nodes; refused nodes remain eligible. --site P1 or I2 selects
one physical node kind for calibration. All output directories must exist.

The geometry theorem and its full row-count identification remain an explicit
premise. Optional --geometry-identities files bind the already verified geometry
IDs and SHA-256 values. This wrapper independently reconstructs the final affine
substitution, requires a literal unit selection row for every variable, and uses
0 <= h <= t*sum(count_boundary.lambda) to derive a proved enclosing box. It
counts ALL full original rhombus rows in that chart, including mixed rows.
No provider program is imported, compiled or executed. Build occurs only through
the explicit build command. No count limit or overflow can be interpreted as zero.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from itertools import zip_longest
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import time


SCHEMA = "pro026-independent-hive-recount-v1"
I64_LOW,I64_HIGH = -(1<<63),(1<<63)-1
COMPACT = {
    "U04":"final-science/UNIFORM-FOUR-COUNT-CERTIFICATES.jsonl.gz",
    "U05":"third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz",
    "U06":"final-science/UNIFORM-SEPTIC-CERTIFICATES.jsonl.gz",
    "U07":"final-science/UNIFORM-OCTIC-CERTIFICATES.jsonl.gz",
    "U08":"final-science-v2/UNIFORM-NONIC-CERTIFICATES.jsonl.gz",
    "U09":"final-science/COMPACT-CERTIFICATES.jsonl.gz",
    "U10":"final-science/COMPACT-CERTIFICATES.jsonl.gz",
    "U11":"final-science/COMPACT-CERTIFICATES.jsonl.gz",
}


class CheckError(ValueError):
    pass


class DeadlineReached(Exception):
    pass


def need(test,message):
    if not test:
        raise CheckError(message)


def integer(value):
    if type(value) is str:
        need(re.fullmatch(r"-?(0|[1-9][0-9]*)",value) is not None,"Malformed exact integer")
        value=int(value)
    need(type(value) is int,"Boolean/float is not an exact integer field")
    return value


def signed64(value):
    value=integer(value)
    need(I64_LOW<=value<=I64_HIGH,"Input exceeds the counter's declared signed 64-bit range")
    return value


def unique_pairs(pairs):
    result={}
    for key,value in pairs:
        need(key not in result,"Duplicate JSON field")
        result[key]=value
    return result


def decode(data):
    return json.loads(data,object_pairs_hook=unique_pairs)


def encoded(value):
    return json.dumps(value,separators=(",",":"),sort_keys=True,allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Deadline:
    def __init__(self,seconds=100):
        self.end=time.monotonic()+seconds

    def remaining(self):
        return self.end-time.monotonic()

    def check(self):
        if self.remaining()<=0:
            raise DeadlineReached("Internal wrapper deadline reached")


def file_pin(path,deadline):
    path=Path(path).resolve()
    before=path.stat()
    h=hashlib.sha256()
    with path.open("rb") as stream:
        while block:=stream.read(1024*1024):
            deadline.check()
            h.update(block)
    after=path.stat()
    need((before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns),"Source changed while hashing")
    return {"path":str(path),"bytes":before.st_size,"sha256":h.hexdigest()}


def check_pin(pin,deadline):
    need(file_pin(pin["path"],deadline)==pin,"Frozen source or binary changed")


class Sources:
    def __init__(self,root,deadline):
        self.root=Path(root).resolve()
        self.deadline=deadline
        self.pins={}
        self.lines={}

    def path(self,name):
        p=Path(name)
        need(not p.is_absolute() and ".." not in p.parts,"Source path escapes unit root")
        path=(self.root/p).resolve()
        need(path.is_relative_to(self.root) and path.is_file(),"Missing or escaping source")
        if name not in self.pins:
            self.pins[name]=file_pin(path,self.deadline)
        return path

    def records(self,name):
        path=self.path(name)
        with (gzip.open(path,"rb") if name.endswith(".gz") else path.open("rb")) as stream:
            for number,raw in enumerate(stream,1):
                self.deadline.check()
                need(raw.endswith(b"\n") and raw.strip(),"Malformed JSONL line")
                yield number,raw,decode(raw)

    def line(self,name,number):
        need(integer(number)>0,"Invalid source line")
        if name not in self.lines:
            path=self.path(name)
            with (gzip.open(path,"rb") if name.endswith(".gz") else path.open("rb")) as stream:
                self.lines[name]=list(stream)
        need(number<=len(self.lines[name]),"Missing referenced source line")
        raw=self.lines[name][number-1]
        return raw,decode(raw)


def relative_source(value,unit):
    need(isinstance(value,str),"Missing source location")
    if value.startswith("/"):
        match=re.fullmatch(r"/mnt/data/FR026_"+unit+r"[A-Z]?/return/(DATA/.*)",value)
        need(match is not None,"Unknown historical source root")
        value=match[1]
    need(value.startswith(f"DATA/{unit}/") and ".." not in Path(value).parts,"Cross-unit source reference")
    return value


def matrix(value,width=None):
    need(isinstance(value,list),"Expected matrix")
    result=[[integer(x) for x in row] for row in value]
    if width is None and result:
        width=len(result[0])
    need(all(len(row)==width for row in result),"Ragged matrix")
    return result


def derive_geometry(c):
    n,d=integer(c["rank"]),integer(c["degree_bound"])
    need(n in (6,7) and 0<=d<=(n-1)*(n-2)//2,"Out-of-scope hive chart")
    need(integer(c["actual_dimension"])==d,"Strict recount requires the verified final actual affine dimension")
    parts=[c["count_boundary"][k] for k in ("lambda","mu","nu")]
    for part in parts:
        need(len(part)==n and all(type(x) is int and x>=0 for x in part)
             and part==sorted(part,reverse=True),"Invalid count-boundary partition")
    area=sum(parts[0])
    need(area==sum(parts[1])+sum(parts[2]),"Count-boundary trace mismatch")
    chart=c["chart"]
    original_dimension=(n-1)*(n-2)//2
    T=matrix(chart["basis_rows"],d)
    off=[integer(x) for x in chart["offset"]]
    translation=[integer(x) for x in c["translation"]]
    need(len(T)==len(off)==original_dimension and len(translation)==d,"Final affine chart shape mismatch")
    base=[b+sum(a*x for a,x in zip(row,translation)) for b,row in zip(off,T)]
    selections=[]
    for j in range(d):
        unit=[int(k==j) for k in range(d)]
        choices=[i for i,row in enumerate(T) if row==unit]
        need(choices,"No literal unit selection row for a surviving coordinate; bounds cannot be inferred")
        k=choices[0]
        selections.append({"variable":j,"original_hive_coordinate":k,"base":base[k],"unit_row":unit})
    raw=matrix(c["original_rhombus_rows"],original_dimension+1)
    need(len(raw)==3*n*(n-1)//2,"Incomplete original rhombus roster")
    rows=[]
    for row in raw:
        rows.append([row[0]+sum(a*b for a,b in zip(row[1:],base)),
                     *[sum(a*T[k][j] for k,a in enumerate(row[1:])) for j in range(d)]])
    need(rows==matrix(c["full_translated_rows"],d+1),"Final full H-system differs from original affine substitution")
    return {"dimension":d,"rank":n,"count_boundary_area":area,"full_rows":rows,"unit_selections":selections,
            "geometry_premise":"Verified complete saturated chart and full nonnegative row-count map; 0 <= h <= t*sum(lambda)."}


def node_system(job,node):
    grade=integer(node["grade"])
    strict=node["strict"]
    need(type(strict) is bool and grade>=0 and (not strict or grade>0),"Illegal physical grade/strictness")
    model=job["model"]
    bounds=[]
    for j,selection in enumerate(model["unit_selections"]):
        need(selection["variable"]==j and selection["unit_row"]==[int(k==j) for k in range(model["dimension"])],"Changed unit selection")
        b=integer(selection["base"])
        bounds.append([signed64(-grade*b),signed64(grade*(integer(model["count_boundary_area"])-b))])
    rows=[[signed64(grade*row[0]-int(strict and any(row[1:]))),*[signed64(x) for x in row[1:]]]
          for row in model["full_rows"]]
    need(len(bounds)==model["dimension"] and all(len(row)==model["dimension"]+1 for row in rows),"Frozen node dimensions changed")
    return bounds,rows


def compact_values(record,unit):
    if unit=="U04":
        return [integer(record[k]) for k in ("A","B","I1","I2")]
    if unit=="U05":
        return [integer(record[k]) for k in ("A","B","C","I1","I2")]
    fields=[k for k in record if k.startswith("counts_")]
    need(len(fields)==1,"Ambiguous compact count vector")
    return [integer(x) for x in record[fields[0]]]


def regular_nodes(record,compact,unit):
    models=record["model_sites"]
    nodes=[]
    seen=set()
    for left,right in zip_longest(models["hive"],models["rows"]):
        need(left is not None and right is not None,"Paired model node roster length differs")
        key=(left["kind"],integer(left["physical_grade"]),left["strict"])
        need(key==(right["kind"],integer(right["physical_grade"]),right["strict"]),"Paired physical requests differ")
        kind,grade,strict=key
        need(type(strict) is bool and grade>0 and kind==("I" if strict else "P")+str(grade) and kind not in seen,"Duplicate or illegal count node identity")
        seen.add(kind)
        values={}
        references={}
        for model,site in (("hive",left),("rows",right)):
            response=site["response"]
            need(response["status"]=="complete","Stored reference is not a completed count")
            values[model]=integer(response["value"])
            need(values[model]>=0,"Negative stored lattice count")
            references[model]=response["id"]
        nodes.append({"kind":kind,"grade":grade,"strict":strict,"stored":values,"response_ids":references})
    wanted=compact_values(compact,unit)
    need([node["stored"]["hive"] for node in nodes]==wanted and [node["stored"]["rows"] for node in nodes]==wanted,
         "Compact certificate and actual paired node values differ")
    return nodes


def u11_nodes(item,compact,sources):
    d=integer(compact["actual_dimension"])
    need(item["determining_nodes"]==compact["determining_nodes"]==item["determination"]["nodes"],"U11 determining nodes changed")
    need(item["determination"]["values"]==compact["values"],"U11 determining model values changed")
    nodes=[]
    for signed in compact["determining_nodes"]:
        signed=integer(signed)
        strict=signed<0
        sign=(-1)**d if strict else 1
        values={model:sign*integer(compact["values"][model][str(signed)]) for model in ("hive","rows")}
        need(all(value>=0 for value in values.values()),"Invalid signed/interior determining value")
        nodes.append({"kind":("I" if strict else "P")+str(abs(signed)),"grade":abs(signed),"strict":strict,
                      "stored":values,"role":"determining","signed_polynomial_node":signed})
    held={}
    held_references={}
    for reference in compact["held_evidence"]:
        path=relative_source(reference["path"],"U11")
        raw,record=sources.line(path,integer(reference["line"]))
        need(sha(raw)==reference["sha256"],"Changed U11 held response bytes")
        model,grade=reference["model"],integer(reference["grade"])
        need(model in ("hive","rows") and grade>0,"Illegal U11 hold identity")
        response=record["response"]
        need(response["status"]=="complete" and integer(response["t"])==grade,"U11 hold is not a completed physical request")
        value=integer(response["value"])
        need(value>=0,"Negative U11 held lattice count")
        key=(grade,model)
        need(key not in held or held[key]==value,"Conflicting repeated U11 hold value")
        held[key]=value
        held_references.setdefault(key,[]).append({"path":path,"line":integer(reference["line"]),"sha256":reference["sha256"]})
    need(set(held)=={(integer(t),m) for t in compact["positive_held_values"] for m in ("hive","rows")},"U11 held model roster incomplete")
    for value in sorted(map(integer,compact["positive_held_values"])):
        values={model:held[value,model] for model in ("hive","rows")}
        need(all(x==integer(compact["positive_held_values"][str(value)]) for x in values.values()),"U11 paired hold value mismatch")
        nodes.append({"kind":"P"+str(value),"grade":value,"strict":False,"stored":values,"role":"positive_holdout",
                      "validated_references":{model:held_references[value,model] for model in ("hive","rows")}})
    need(len({node["kind"] for node in nodes})==len(nodes),"Determining and held request identities overlap")
    return nodes


def geometry_receipts(paths,deadline):
    entries={}
    pins=[]
    for path in paths:
        pins.append(file_pin(path,deadline))
        with Path(path).open("rb") as stream:
            for raw in stream:
                row=decode(raw)
                key=(integer(row["id"]),row["geometry_sha256"])
                need(key not in entries,"Duplicate geometry acceptance identity")
                entries[key]=row
    return entries,pins


def index_jobs(args,deadline,result):
    sources=Sources(args.root,deadline)
    unit=args.unit
    need(unit in COMPACT,"Unsupported production unit")
    if unit!="U11":
        need(args.shard and re.fullmatch(r"shard-?[0-9]{2,3}",args.shard),"Select a literal production shard")
    compact_path=f"DATA/{unit}/"+COMPACT[unit]
    physical_u04_ids = None
    if unit == "U04":
        physical_u04_ids = set()
        for line,raw,record in sources.records(f"DATA/U04/layer5-results/{args.shard}/certificates.jsonl"):
            idx = integer(record["id"])
            need(idx not in physical_u04_ids,"Duplicate U04 physical source identity")
            physical_u04_ids.add(idx)
    selected={}
    all_ids=set()
    for line,raw,row in sources.records(compact_path):
        idx=integer(row.get("group_id",row.get("target_ordinal",row.get("id"))))
        need(idx not in all_ids,"Duplicate final production certificate ID")
        all_ids.add(idx)
        if unit=="U04":
            use=idx in physical_u04_ids
        elif unit=="U11":
            use=args.input is None or relative_source(row["geometry_input"],unit)==args.input
        else:
            directory=str(Path(relative_source(row["geometry"]["path"],unit)).parent) if unit=="U05" else relative_source(row["evidence_directory"],unit)
            use=directory==f"DATA/{unit}/production/{args.shard}/counts"
        if use:
            selected[idx]=(row,{"path":compact_path,"line":line,"sha256":sha(raw)})
    need(selected,"Selected production stream has no exact certificate identities")
    accepted,acceptance_pins=geometry_receipts(args.geometry_identities,deadline)
    output=Path(args.output).resolve()
    jobs_path=output.with_suffix(".jobs.jsonl")
    need(not jobs_path.exists(),"Refusing to overwrite frozen jobs")
    entries,seen=[],set()
    result.update(kind="manifest",status="PARTIAL",unit=unit,stream=args.input if unit=="U11" else args.shard,
                  input_root=str(sources.root),expected_record_ids=sorted(selected),records=entries,selection_complete=True,index_complete=False)
    def emit(geometry,compact,geometry_sha,geometry_ref,certificate_ref,nodes,jobs):
        idx=integer(geometry["id"])
        need(idx not in seen,"Duplicate selected geometry identity")
        seen.add(idx)
        original=geometry["original"]
        if "bare_triple" in compact:
            need(original==compact["bare_triple"],"Selected original whole triple changed")
        if "actual_dimension" in compact:
            need(integer(compact["actual_dimension"])==integer(geometry["degree_bound"]),"Compact and final chart dimensions differ")
        if args.geometry_identities:
            need((idx,geometry_sha) in accepted and accepted[idx,geometry_sha]["bare_triple"]==original,
                 "Selected geometry lacks its exact independent acceptance binding")
        job={"id":idx,"unit":unit,"bare_triple":original,"geometry_sha256":geometry_sha,
             "geometry_reference":geometry_ref,"certificate_reference":certificate_ref,
             "model":derive_geometry(geometry),"nodes":nodes,
             "geometry_acceptance":"EXACT_IDENTITIES_BOUND" if args.geometry_identities else "REQUIRES_GEOMETRY_JOIN"}
        offset=jobs.tell()
        body=encoded(job)+b"\n"
        jobs.write(body)
        entries.append({"ordinal":len(entries),"id":idx,"geometry_sha256":geometry_sha,"offset":offset,"bytes":len(body),
                        "sha256":sha(body),"node_ids":[f"{unit}:{idx}:{node['kind']}" for node in nodes]})
    try:
        with jobs_path.open("xb") as jobs:
            if unit=="U11":
                paths=sorted({relative_source(row["geometry_input"],unit) for row,_ in selected.values()})
                for path in paths:
                    for line,raw,item in sources.records(path):
                        idx=integer(item["id"])
                        if idx not in selected:
                            continue
                        compact,cref=selected[idx]
                        if relative_source(compact["geometry_input"],unit)!=path:
                            continue
                        geometry=item["geometry"]
                        gh=sha(json.dumps(geometry,separators=(",",":"),allow_nan=False).encode())
                        need(gh==compact["geometry_sha256"] and integer(geometry["id"])==idx,"U11 embedded geometry binding changed")
                        emit(geometry,compact,gh,{"path":path,"line":line,"input_line_sha256":sha(raw),"embedded_geometry_sha256":gh},
                             cref,u11_nodes(item,compact,sources),jobs)
            else:
                folder=f"DATA/{unit}/layer5-results/{args.shard}" if unit=="U04" else f"DATA/{unit}/production/{args.shard}/counts"
                repairs={}
                if unit=="U04":
                    path="DATA/U04/seven-dual-repairs/certificates.jsonl"
                    for line,raw,row in sources.records(path):
                        idx=integer(row["id"])
                        need(idx not in repairs,"Duplicate U04 repair identity")
                        repairs[idx]=(row,{"path":path,"line":line,"sha256":sha(raw)})
                for gi,ri in zip_longest(sources.records(folder+"/geometry.jsonl.gz"),sources.records(folder+"/certificates.jsonl")):
                    need(gi is not None and ri is not None,"Geometry/raw-certificate roster length mismatch")
                    gline,graw,geometry=gi
                    rline,rraw,record=ri
                    idx=integer(geometry["id"])
                    need(integer(record["id"])==idx and gline==rline,"Geometry/raw record identity/order mismatch")
                    if idx not in selected:
                        continue
                    compact,cref=selected[idx]
                    gh=sha(graw)
                    expected_sha=compact["geometry"]["sha256"] if unit=="U05" else compact["geometry_sha256"]
                    need(gh==record["geometry_sha256"]==expected_sha and record["bare_triple"]==geometry["original"],"Production geometry/raw/compact binding changed")
                    rref={"path":folder+"/certificates.jsonl","line":rline,"sha256":sha(rraw)}
                    if idx in repairs:
                        record,rref=repairs[idx]
                        need(record["geometry_sha256"]==gh and record["bare_triple"]==geometry["original"],"Repair changed its complete parent")
                    emit(geometry,compact,gh,{"path":folder+"/geometry.jsonl.gz","line":gline,"sha256":gh},
                         {"compact":cref,"raw_model_sites":rref},regular_nodes(record,compact,unit),jobs)
        need(seen==set(selected),"Missing selected geometry/certificate identities")
        result.update(status="FROZEN_RECOUNT_JOBS",index_complete=True)
    finally:
        # These hashes remain usable for the complete prefix if indexing hits
        # its deadline. Unindexed identities remain explicit in the manifest.
        result["pending_index_ids"]=sorted(set(selected)-{row["id"] for row in entries})
        result["inputs"]=list(sources.pins.values())+acceptance_pins
        result["jobs"]={"path":str(jobs_path),"bytes":jobs_path.stat().st_size,"sha256":sha(jobs_path.read_bytes())}
        result["wrapper_sha256"]=sha(Path(__file__).read_bytes())


def compile_counter(source,binary,compiler,deadline):
    source=Path(source).resolve()
    binary=Path(binary).resolve()
    need(source.name.endswith("independent_hive_recount.cpp"),"Build only the explicitly owned independent counter source")
    need(not binary.exists() and binary.parent.is_dir(),"Build destination must be new in an existing directory")
    started=time.monotonic()
    command=[compiler,"-std=c++17","-O2","-Wall","-Wextra",str(source),"-o",str(binary)]
    process=subprocess.run(command,capture_output=True,text=True,timeout=max(.1,deadline.remaining()))
    need(process.returncode==0,"Independent counter compile failed: "+process.stderr[-6000:])
    return {"schema":SCHEMA,"kind":"build","status":"BUILT_OWN_COUNTER","command":command,"source":file_pin(source,deadline),
            "binary":file_pin(binary,deadline),"wrapper_sha256":sha(Path(__file__).read_bytes()),
            "compile_seconds":time.monotonic()-started,"compiler_diagnostics":process.stderr}


class Engine:
    def __init__(self,binary):
        self.process=subprocess.Popen([str(binary)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.selector=selectors.DefaultSelector()
        self.selector.register(self.process.stdout,selectors.EVENT_READ)
        self.buffer=b""

    def request(self,request_id,bounds,rows,max_states,milliseconds,timeout):
        need(0<max_states<=(1<<63)-1 and 0<milliseconds<=110000,"Invalid counter resource limit")
        n=len(bounds)
        parts=[f"RECOUNT1 {request_id} {n} {len(rows)} {max_states} {milliseconds}\n"]
        parts += [f"{signed64(lo)} {signed64(hi)}\n" for lo,hi in bounds]
        parts += [" ".join(str(signed64(x)) for x in row)+"\n" for row in rows]
        self.process.stdin.write("".join(parts).encode())
        self.process.stdin.flush()
        end=time.monotonic()+timeout
        while b"\n" not in self.buffer:
            left=end-time.monotonic()
            if left<=0 or not self.selector.select(left):
                raise TimeoutError("Owned counter did not return before the wrapper timeout")
            chunk=os.read(self.process.stdout.fileno(),65536)
            if not chunk:
                raise CheckError("Owned counter exited without a complete result")
            self.buffer+=chunk
        line,self.buffer=self.buffer.split(b"\n",1)
        result=decode(line)
        need(result.get("id")==request_id,"Counter response identity changed")
        if result["status"]=="complete":
            need(integer(result["count"])>=0,"Counter returned a negative count")
        else:
            need(result.get("count") is None and result["status"].startswith("REFUSED_"),"A partial/refused result supplied a count")
        return result

    def close(self):
        try:
            if self.process.stdin:
                self.process.stdin.close()
            try:
                self.process.wait(timeout=.5)
            except subprocess.TimeoutExpired:
                self.process.terminate()
                try:
                    self.process.wait(timeout=.5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=1)
        finally:
            self.selector.close()
            for pipe in (self.process.stdout,self.process.stderr):
                if pipe:
                    pipe.close()


def load_manifest(path,deadline):
    raw=Path(path).read_bytes()
    manifest=decode(raw)
    need(manifest.get("schema")==SCHEMA and manifest.get("kind")=="manifest" and manifest.get("selection_complete"),"No complete source-selection roster")
    need(manifest.get("status") in ("FROZEN_RECOUNT_JOBS","PARTIAL"),"Failed indexing cannot supply a recount cohort")
    need(manifest["wrapper_sha256"]==sha(Path(__file__).read_bytes()),"Wrapper changed after job freezing")
    check_pin(manifest["jobs"],deadline)
    need(len({r["id"] for r in manifest["records"]})==len(manifest["records"]),"Duplicate frozen record identities")
    need(manifest["expected_record_ids"]==sorted(set(manifest["expected_record_ids"])) and
         {r["id"] for r in manifest["records"]}<=set(manifest["expected_record_ids"]),"Changed expected source-record roster")
    offset=0
    for ordinal,row in enumerate(manifest["records"]):
        need(row["ordinal"]==ordinal and row["offset"]==offset,"Frozen job ordinal/offset gap")
        need(len(set(row["node_ids"]))==len(row["node_ids"]),"Duplicate node roster")
        offset+=row["bytes"]
    need(offset==manifest["jobs"]["bytes"] and set(manifest["pending_index_ids"])==set(manifest["expected_record_ids"])-{r["id"] for r in manifest["records"]},"Frozen index completeness mismatch")
    need(not manifest["index_complete"] or (not manifest["pending_index_ids"] and manifest["status"]=="FROZEN_RECOUNT_JOBS"),"False complete-index status")
    return manifest,sha(raw)


def read_job(stream,expected):
    stream.seek(expected["offset"])
    raw=stream.read(expected["bytes"])
    need(sha(raw)==expected["sha256"],"Frozen recount job changed")
    job=decode(raw)
    need(job["id"]==expected["id"] and job["geometry_sha256"]==expected["geometry_sha256"],"Job parent identity changed")
    need([f"{job['unit']}:{job['id']}:{x['kind']}" for x in job["nodes"]]==expected["node_ids"],"Job node identities changed")
    return job


def prior_results(paths,manifest_sha,deadline):
    matched={}
    all_rows=[]
    for path in paths:
        report=decode(Path(path).read_bytes())
        need(report.get("schema")==SCHEMA and report.get("kind")=="run" and report.get("manifest_sha256")==manifest_sha,"Count report belongs to another frozen cohort")
        need(report.get("wrapper_sha256")==sha(Path(__file__).read_bytes()),"Prior count report used another wrapper")
        check_pin(report["build_reference"],deadline)
        build=decode(Path(report["build_reference"]["path"]).read_bytes())
        need(build.get("schema")==SCHEMA and build.get("kind")=="build" and build["binary"]==report["build"]
             and build["source"]==report["counter_source"],"Prior counter build identity changed")
        check_pin(build["source"],deadline)
        check_pin(build["binary"],deadline)
        check_pin(report["results"],deadline)
        with Path(report["results"]["path"]).open("rb") as stream:
            for raw in stream:
                row=decode(raw)
                all_rows.append(row)
                if row["status"]=="MATCH":
                    need(row["counter"]["status"]=="complete" and all(integer(row["counter"]["count"])==v for v in row["stored"].values()),"A prior MATCH contains no complete matching count")
                    need(row["node_id"] not in matched,"Duplicate successful recount identity")
                    matched[row["node_id"]]=row
    return matched,all_rows


def run_jobs(args,deadline,result):
    manifest,manifest_sha=load_manifest(args.manifest,deadline)
    result["input_root"]=manifest["input_root"]
    need(not Path(args.output).resolve().is_relative_to(Path(manifest["input_root"])),"Never write into the immutable unit root")
    build=decode(Path(args.build).read_bytes())
    need(build.get("schema")==SCHEMA and build.get("kind")=="build" and build["wrapper_sha256"]==sha(Path(__file__).read_bytes()),"Build provenance does not match this wrapper")
    check_pin(build["source"],deadline)
    check_pin(build["binary"],deadline)
    for pin in manifest["inputs"]:
        check_pin(pin,deadline)
    records=manifest["records"]
    need(0<=args.start<=len(records) and (args.limit is None or args.limit>0),"Invalid record slice")
    stop=len(records) if args.limit is None else min(len(records),args.start+args.limit)
    if args.site is not None:
        need(any(node.rsplit(":",1)[1]==args.site for record in records[args.start:stop] for node in record["node_ids"]),
             "Requested site is absent from the exact selected record slice")
    previous,_=prior_results(args.resume_from,manifest_sha,deadline)
    expected_all={node for record in records for node in record["node_ids"]}
    need(set(previous)<=expected_all,"Resume contains an unexpected node identity")
    destination=Path(args.output).resolve().with_suffix(".counts.jsonl")
    need(not destination.exists(),"Refusing to replace durable recount results")
    result.update(kind="run",manifest_sha256=manifest_sha,build=build["binary"],start=args.start,requested_stop=stop,
                  build_reference=file_pin(args.build,deadline),counter_source=build["source"],
                  matched_node_ids=[],refused_node_ids=[],status="PARTIAL",counter_pid=None,
                  attempted_nodes=0,counter_elapsed_seconds=0.0,visited_states=0)
    completed=set(previous)
    engine=None
    try:
        with Path(manifest["jobs"]["path"]).open("rb") as stream,destination.open("xb") as output:
            engine=Engine(build["binary"]["path"])
            result["counter_pid"]=engine.process.pid
            for expected in records[args.start:stop]:
                deadline.check()
                job=read_job(stream,expected)
                for node in job["nodes"]:
                    node_id=f"{job['unit']}:{job['id']}:{node['kind']}"
                    if node_id in previous or (args.site is not None and node["kind"]!=args.site):
                        continue
                    deadline.check()
                    if deadline.remaining()<=1:
                        raise DeadlineReached("Insufficient time to launch the next bounded count")
                    bounds,rows=node_system(job,node)
                    milliseconds=min(args.node_ms,max(1,int((deadline.remaining()-.75)*1000)))
                    host_failure=None
                    try:
                        response=engine.request(node_id,bounds,rows,args.max_states,milliseconds,min(deadline.remaining()-.1,milliseconds/1000+.5))
                    except (TimeoutError,OSError,CheckError) as error:
                        host_failure=error
                        response={"id":node_id,"status":"REFUSED_HOST_TIMEOUT" if isinstance(error,TimeoutError) else "REFUSED_PROCESS",
                                  "count":None,"detail":str(error)}
                    entry={"record_ordinal":expected["ordinal"],"id":job["id"],"node_id":node_id,"geometry_sha256":job["geometry_sha256"],
                           "kind":node["kind"],"grade":node["grade"],"strict":node["strict"],"stored":node["stored"],
                           "full_system_sha256":sha(encoded({"bounds":bounds,"rows":rows})),"counter":response,
                           "geometry_acceptance":job["geometry_acceptance"]}
                    if response["status"]=="complete":
                        count=integer(response["count"])
                        entry["matches"]={model:count==value for model,value in node["stored"].items()}
                        entry["status"]="MATCH" if all(entry["matches"].values()) else "MISMATCH"
                    else:
                        entry["status"]="REFUSED"
                    output.write(encoded(entry)+b"\n")
                    output.flush()
                    result["attempted_nodes"]+=1
                    result["counter_elapsed_seconds"]+=response.get("elapsed_seconds",0.0)
                    result["visited_states"]+=response.get("visited_states",0)
                    if entry["status"]=="MATCH":
                        completed.add(node_id)
                        result["matched_node_ids"].append(node_id)
                    elif entry["status"]=="MISMATCH":
                        result.update(status="COUNT_MISMATCH",mismatch=entry)
                        return
                    else:
                        result["refused_node_ids"].append(node_id)
                    if host_failure is not None:
                        raise host_failure
            selected={node for record in records[args.start:stop] for node in record["node_ids"] if args.site is None or node.rsplit(":",1)[1]==args.site}
            result["status"]="SLICE_RECOUNTS_MATCH" if selected<=completed else "PARTIAL"
    finally:
        if engine is not None:
            engine.close()
            result["counter_exit_code"]=engine.process.returncode
        result["pending_node_ids"]=sorted(expected_all-completed)
        result["pending_index_record_ids"]=manifest["pending_index_ids"]
        if destination.exists():
            result["results"]={"path":str(destination),"bytes":destination.stat().st_size,"sha256":sha(destination.read_bytes())}


def aggregate(args,deadline,result):
    manifest,manifest_sha=load_manifest(args.manifest,deadline)
    result["input_root"]=manifest["input_root"]
    need(not Path(args.output).resolve().is_relative_to(Path(manifest["input_root"])),"Never write into the immutable unit root")
    matched,rows=prior_results(args.reports,manifest_sha,deadline)
    expected={}
    with Path(manifest["jobs"]["path"]).open("rb") as stream:
        for record in manifest["records"]:
            job=read_job(stream,record)
            for node in job["nodes"]:
                expected[f"{job['unit']}:{job['id']}:{node['kind']}"]=(job,node)
    mismatches=[]
    for row in rows:
        deadline.check()
        need(row["node_id"] in expected,"Unexpected recount node identity")
        job,node=expected[row["node_id"]]
        bounds,system=node_system(job,node)
        need(row["id"]==job["id"] and row["kind"]==node["kind"] and row["grade"]==node["grade"] and row["strict"]==node["strict"]
             and row["counter"].get("id")==row["node_id"] and row["geometry_sha256"]==job["geometry_sha256"] and row["stored"]==node["stored"]
             and row["full_system_sha256"]==sha(encoded({"bounds":bounds,"rows":system})),"Recount record/source/whole-system binding changed")
        if row["status"]=="MATCH":
            need(row["counter"]["status"]=="complete" and all(integer(row["counter"]["count"])==v for v in node["stored"].values()),"False successful recount status")
        elif row["status"]=="MISMATCH":
            need(row["counter"]["status"]=="complete" and any(integer(row["counter"]["count"])!=v for v in node["stored"].values()),"False count mismatch status")
            mismatches.append(row["node_id"])
        else:
            need(row["status"]=="REFUSED" and row["counter"]["status"].startswith("REFUSED_") and row["counter"]["count"] is None,"A refusal supplied a partial count")
    for pin in manifest["inputs"]:
        check_pin(pin,deadline)
    missing=sorted(set(expected)-set(matched))
    result.update(manifest_sha256=manifest_sha,matched_node_ids=sorted(matched),pending_node_ids=missing,
                  pending_index_record_ids=manifest["pending_index_ids"],mismatches=mismatches,
                  complete_record_ids=sorted(record["id"] for record in manifest["records"] if set(record["node_ids"])<=set(matched)),
                  status="COUNT_MISMATCH" if mismatches else "COMPLETE_FROZEN_RECOUNTS_MATCH" if not missing and manifest["index_complete"] else "PARTIAL",
                  scope="Fresh exact integer counts of each full H-system inside its proved enclosing box; whole-LR interpretation retains the verified geometry/row-map premise.")


def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command",choices=("build","index","run","aggregate"))
    parser.add_argument("--root")
    parser.add_argument("--unit",choices=COMPACT)
    parser.add_argument("--shard")
    parser.add_argument("--input")
    parser.add_argument("--geometry-identities",nargs="*",default=[])
    parser.add_argument("--manifest")
    parser.add_argument("--build")
    parser.add_argument("--cpp-source",default=str(Path(__file__).with_name("independent_hive_recount.cpp")))
    parser.add_argument("--compiler",default="/usr/bin/c++")
    parser.add_argument("--binary")
    parser.add_argument("--start",type=int,default=0)
    parser.add_argument("--limit",type=int)
    parser.add_argument("--site")
    parser.add_argument("--node-ms",type=int,default=500)
    parser.add_argument("--max-states",type=int,default=1000000)
    parser.add_argument("--budget-seconds",type=float,default=100)
    parser.add_argument("--resume-from",nargs="*",default=[])
    parser.add_argument("--reports",nargs="*",default=[])
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    started=time.monotonic()
    result={"schema":SCHEMA,"kind":args.command,"status":"NOT_STARTED"}
    try:
        need(0<args.budget_seconds<=110 and 0<args.node_ms<=110000 and 0<args.max_states<=(1<<63)-1,"Invalid explicit resource limits")
        deadline=Deadline(args.budget_seconds)
        output=Path(args.output).resolve()
        need(output.parent.is_dir() and not output.exists(),"Output must be new in an existing directory")
        if args.root:
            need(not output.is_relative_to(Path(args.root).resolve()),"Never write into the immutable input root")
        result["wrapper_sha256"]=sha(Path(__file__).read_bytes())
        if args.command=="build":
            need(args.binary,"Build requires a binary destination")
            result.update(compile_counter(args.cpp_source,args.binary,args.compiler,deadline))
        elif args.command=="index":
            need(args.root and args.unit,"Index requires a unit root and unit")
            index_jobs(args,deadline,result)
        elif args.command=="run":
            need(args.manifest and args.build,"Run requires frozen jobs and a build receipt")
            run_jobs(args,deadline,result)
        else:
            need(args.manifest,"Aggregate requires frozen jobs")
            aggregate(args,deadline,result)
    except DeadlineReached as error:
        result.update(status="PARTIAL",interruption=str(error))
    except (TimeoutError,subprocess.TimeoutExpired) as error:
        result.update(status="PARTIAL",interruption=str(error))
    except (CheckError,KeyError,TypeError,ValueError,OSError,EOFError,IndexError) as error:
        result.update(status="FAIL",error=f"{type(error).__name__}: {error}")
    result["elapsed_seconds"]=round(time.monotonic()-started,6)
    output=Path(args.output).resolve()
    input_root=args.root or result.get("input_root")
    if output.parent.is_dir() and not output.exists() and (not input_root or not output.is_relative_to(Path(input_root).resolve())):
        with output.open("x",encoding="utf-8") as stream:
            json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
            stream.write("\n")
    summary={k:v for k,v in result.items() if k not in ("records","expected_record_ids","pending_index_ids","matched_node_ids","pending_node_ids","inputs","complete_record_ids")}
    print(json.dumps(summary,sort_keys=True))
    return 1 if result["status"] in ("FAIL","COUNT_MISMATCH") else 2 if result["status"]=="PARTIAL" else 0


if __name__=="__main__":
    sys.exit(main())
