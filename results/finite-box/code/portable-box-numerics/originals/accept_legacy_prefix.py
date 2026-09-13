#!/usr/bin/env python3
"""Independent polynomial acceptance for old legacy source IDs 0..271 ONLY.

command --id F2627-LEGACY-PREFIX-ACCEPT-001 [--reports REPORT...]
accept --output REPORT [--reports REPORT...] [--budget-seconds 95]

command prints the exact run_check argv and never launches it. With no explicit
reports, only the named auxiliary LEGACY starts 0,8,...264 and retries 0..2 are
discovered. All starts >=272 and all foreign/duplicate successful sites are
rejected. The old tail is not read, accepted, backfilled or recounted here.

Only the pinned root-owned tail module's original_hive utility is called;
neither its indexing/acceptance routines nor the old generator are executed.
Geometry is rebuilt from the literal bare triple, independently of source
coefficients. The complete ordinary hive, classical coordinate bounds and LR
polynomiality/ambient degree bound are explicit premises. No actual hull,
strict interior or parity claim is made.

Every source-negative observation is saved before vector comparisons. A fresh
positive-grade witness precedes use of P(0)=1. Full vectors reconstructed from
0..D and all ordinary-negative observations are saved before any fresh hold or
source-vector/value comparison. Grades D+1,D+2 remain interpolation holdouts.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

sys.dont_write_bytecode=True
import index_legacy_tail_recounts as geometry

W=Path(__file__).resolve().parent
C=Path("/Volumes/SLR-Research/stretched-lr-research")
SCHEMA="pro026-legacy-prefix-polynomial-acceptance-v1"
COUNT_SCHEMA="pro026-independent-hive-recount-v1"
PREFIX=tuple(range(272))
EXCLUDED=tuple(range(272,297))
DEFAULT_INDEX=W/"science/F2627-LEGACY-INDEX-001/result.json"
DEFAULT_SOURCES=W/"publication-staging/LEGACY-VECTOR-SOURCES.json"
DEFAULT_SELECTION=W/"publication-staging/CHOSEN-TERMINALS.json"
DEFAULT_BUILD=W/"science/F2627-RECOUNT-V2-BUILD-002/result.json"
PINS={
    "index_legacy_recounts.py":"984d04f0fcac56ebab3980ec30ccec02070f498b63b579fd9a8ebf4561ddc83f",
    "recount_records.py":"f62a78a78f1d38452fb805ca051c89fe1dabf26d0d2c0d6a900c9200fd6aa4e7",
    "v2_independent_hive_recount.cpp":"093c6a8eb69958aaea519c3946b3a2e6ee32636ba9dcb218cd5bc88b8fd12dcc",
    "run_check.py":"0cd793c5aad6e988dd56333c21dd326a197cab13864fa7e4f7f4c2cfdd70540b",
    "run_auxiliary_recounts.py":"8dd4640599cc01186694210f4ec8d639f4572c2afa261289494af8baf68199ef",
    "box_geometry.py":"988ea146f001f93a0b5a1a2a8b78076d710b9bb494a2e894189e273391426f8c",
    "index_legacy_tail_recounts.py":"1d019a0c9e2e27ba1c07480c045c4aec72d8f6e3e24a313419b6c6fec499e9af",
}
DATA_PINS={"index":"2e9c64c5305d0465794a8a4dcfa9433ef743d996d3033f004c185e23ee8f3233",
           "source_map":"225c66d78739d69780d97f7849101cfeb7191e153261da0864156a6ccb2657fa",
           "selection":"befde4781652edbb93465e76667fa556c57bb4f7af4c484effcdc3b775f3be53",
           "build":"e139da741be027c8a76179f6d83e745a324fd2f48f848e2cb9a1fff386959b2f"}
SCHEDULE=((2000,10000000),(10000,50000000),(60000,100000000))
PROTECTED=(
    C/"results/runs/SLR-FQB-WI226-FABLE068-FRONTIER-REPAIR-001/delivery/SLR-FABLE-DISCOVERY-068/provider-output",
    C/"results/runs/SLR-FQF-WI230-FABLE068-METHOD-SEAL-001/delivery/provider-output",
    C/"results/runs/SLR-FQH-WI236-FABLE068-SOURCE-SEPARATED-001/delivery/.claude",
)
PREMISES=[
    "The complete ordinary integral hive counts the whole LR coefficient, with lambda outer.",
    "Every original hive coordinate is in 0..t*sum(lambda), by the complete nonnegative tableau-row interpretation.",
    "LR stretching is polynomial with degree at most D=(n-1)(n-2)/2. No old minimal degree, actual hull or interior parity is used.",
    "A fresh positive-grade count proves nonemptiness before using the nonempty polynomial constant one; the artificial t=0 hive is not that witness.",
    "Only trailing-zero padding/trim and LR inner commutativity bind the original source triple to the selected terminal.",
    "Final composition transport, the separate new tail 272..296 and campaign acceptance belong to their owning gates.",
]

class Invalid(ValueError):pass
class DeadlineReached(Exception):pass
class SourceNegative(Exception):
    def __init__(self,observation):self.observation=observation
def need(value,message):
    if not value:raise Invalid(message)
def integer(value):
    if type(value) is str:
        need(re.fullmatch(r"-?(0|[1-9][0-9]*)",value) is not None,"Malformed exact integer")
        return int(value)
    need(type(value) is int,"Boolean/float is not an exact integer")
    return value
def rational(value):
    need(type(value) is int or type(value) is str and re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?",value),
         "Non-exact source coefficient")
    return Q(value)
def encoded(value):return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def decode(raw):
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,"Duplicate JSON key");result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs)
def pin(path):
    path=Path(path).resolve(strict=True)
    need(not any(path.is_relative_to(p) for p in PROTECTED),"Protected residue may not be read or hashed")
    before=path.stat();h=hashlib.sha256()
    with path.open("rb") as stream:
        while block:=stream.read(1024*1024):h.update(block)
    after=path.stat()
    need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
         (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),"Source changed while hashing")
    return {"path":str(path),"bytes":before.st_size,"sha256":h.hexdigest()}
def bare_pin(value):return {key:value[key] for key in ("path","bytes","sha256")}
def merge_pins(values):
    result={}
    for value in values:
        p=bare_pin(value)
        need(p["path"] not in result or result[p["path"]]==p,"Conflicting source pin")
        result[p["path"]]=p
    return [result[key] for key in sorted(result)]
def save(path,value):
    path=Path(path);need(path.parent.is_dir() and not path.exists(),"Fresh output in an existing directory required")
    with path.open("xb") as stream:stream.write(encoded(value)+b"\n")
class Deadline:
    def __init__(self,seconds=95):
        need(0<seconds<=100,"Internal cap must be at most 100 seconds");self.end=time.monotonic()+seconds
    def check(self):
        if time.monotonic()>=self.end:raise DeadlineReached("Bounded acceptance deadline reached")
class Inputs:
    def __init__(self):self.used={};self.documents={}
    def bind(self,value):
        p=bare_pin(value);need(pin(p["path"])==p,"Frozen input changed: "+p["path"])
        need(p["path"] not in self.used or self.used[p["path"]]==p,"Input version changed during acceptance")
        self.used[p["path"]]=p;return p
    def read(self,path,expected=None):
        candidate=bare_pin(expected) if expected is not None else pin(path)
        if candidate["path"] in self.used:
            need(candidate==self.used[candidate["path"]],"Changed cached input identity");p=candidate
        else:p=self.bind(candidate)
        if p["path"] not in self.documents:
            need(p["bytes"]<=128*1024*1024,"JSON input exceeds declared byte bound")
            self.documents[p["path"]]=decode(Path(p["path"]).read_bytes())
        return self.documents[p["path"]]
    def after(self):
        for p in self.used.values():need(pin(p["path"])==p,"Source changed during acceptance: "+p["path"])


def pointer(doc,expression):
    if expression=="":return doc
    need(type(expression) is str and expression.startswith("/"),"Invalid exact source pointer")
    for part in expression[1:].split("/"):
        need(re.search(r"~(?![01])",part) is None,"Invalid JSON pointer escape")
        part=part.replace("~1","/").replace("~0","~")
        if isinstance(doc,list):
            need(re.fullmatch(r"0|[1-9][0-9]*",part) is not None,"Invalid source list index");doc=doc[int(part)]
        else:doc=doc[part]
    return doc
def triple(value):
    if isinstance(value,dict):
        need(set(value)=={"lambda","mu","nu"},"Incomplete or extra triple fields")
        value=[value[k] for k in ("lambda","mu","nu")]
    need(isinstance(value,(list,tuple)) and len(value)==3,"A complete bare triple is required")
    parts=[]
    for p in value:
        need(isinstance(p,(list,tuple)) and all(type(x) is int and x>=0 for x in p)
             and list(p)==sorted(p,reverse=True),"Invalid integral partition")
        p=list(p)
        while p and not p[-1]:p.pop()
        parts.append(p)
    need(sum(parts[0])==sum(parts[1])+sum(parts[2]) and 1<=max(map(len,parts))<=7,"Unbalanced/out-of-range ordinary triple")
    return dict(zip(("lambda","mu","nu"),parts))
def bind_triples(source,terminal):
    source,terminal=triple(source),triple(terminal)
    need(source["lambda"]==terminal["lambda"],"Source-to-terminal outer partition differs")
    if source==terminal:operation="identity_after_trailing_zero_trim"
    else:
        need(source["mu"]==terminal["nu"] and source["nu"]==terminal["mu"],"Source-to-terminal relation needs an unapproved transformation")
        operation="inner_exchange_after_trailing_zero_trim"
    return source,terminal,{"operation":operation,"common_dilation_or_affine_reduction_used":False,
                         "premise":"Classical LR inner commutativity and zero-padding invariance"}
def source_negative_gate(record,values,reference,output):
    need(isinstance(values,list) and values,"Missing complete source vector")
    coefficients=list(map(rational,values))
    negative=[{"degree":i,"coefficient":str(c)} for i,c in enumerate(coefficients) if c<0]
    if negative:
        path=Path(output).with_suffix(".source-negative.json")
        observation={"schema":SCHEMA,"kind":"source_negative_observation","status":"HOLD_UNACCEPTED_SOURCE_NEGATIVE",
                     "id":record["id"],"terminal_id":record["terminal_id"],"bare_triple":record.get("bare_triple"),
                     "coefficients_low_to_high":values,"negative":negative,"source":reference,
                     "preserved_before_vector_or_count_comparison":True,
                     "scope":"Unaccepted historical source claim, not a newly confirmed LR counterexample"}
        save(path,observation);raise SourceNegative(pin(path))
    return coefficients
def metadata_roster(document,selection,prefix_ids=PREFIX,total=297):
    need(document["schema"]=="legacy-adopted-source-vectors-v1"
         and document["status"]=="SOURCE_VECTORS_EXTRACTED_UNACCEPTED"
         and document["source_vector_acceptance_asserted"] is False,"Wrong/already accepted source metadata")
    records=document["records"];need(len(records)==total,"Incomplete source identity roster")
    need([integer(r["id"]) for r in records]==list(range(total)) and document["expected_record_ids"]==list(range(total)),
         "Missing, duplicate or reordered legacy source IDs")
    ids=[r["terminal_id"] for r in records]
    need(all(type(x) is str and x for x in ids) and len(set(ids))==total and ids==document["expected_terminal_ids"],
         "Missing/duplicate literal terminal identities")
    chosen=[r for r in selection["choices"] if r["family"] in ("FRE","FRI-settled")]
    need(len(chosen)==total and [r["terminal_id"] for r in chosen]==ids,"Source-order selected terminal roster differs")
    answer=[]
    for i in prefix_ids:
        r,c=records[i],chosen[i]
        need(r["source_vector_accepted"] is False and r["status"]=="SOURCE_VECTOR_UNACCEPTED_PENDING_FRESH_RECOUNT","Incomplete or silently accepted source vector")
        need(r["family"]==c["family"] and r["source_id"]==c["source_id"] and r["chosen_seed_key"]==c["seed_key"],
             "Selected terminal/source key changed")
        source,terminal,binding=bind_triples(r["bare_triple"],r["terminal_source_triple"])
        need(triple(c["source_triple"])==terminal and r["source_to_terminal_binding"]==binding,"Exact selected terminal triple/binding differs")
        answer.append(r)
    return answer
def alternate_reference(record,reference):
    if 'same_source_file' in reference:
        need(type(reference['same_source_file']) is bool,'Malformed same-file source declaration')
    if reference.get('same_source_file'):
        need(set(reference)=={'same_source_file','json_pointer'},'Conflicting same-file source identity')
        return {**record['vector_reference'],'json_pointer':reference['json_pointer']}
    need(all(k in reference for k in ('path','bytes','sha256','json_pointer')),
         'Alternate source lacks a complete file identity')
    return reference


def source_documents(records,document,inputs,output,deadline):
    catalog={p["path"]:bare_pin(p) for p in merge_pins(document["inputs"])}
    evidence=[]
    def fetch(reference):
        identity=bare_pin(reference)
        path=Path(identity["path"]).resolve()
        need(str(path)==identity["path"] and (path.is_relative_to(C) or path.is_relative_to(W)),
             "Original source pointer escaped its declared approved roots")
        need(catalog.get(identity["path"])==identity,"Source pointer lacks its immutable catalog binding")
        return inputs.read(path,identity)
    for r in records:
        deadline.check()
        source_negative_gate(r,r["coefficients_low_to_high"],r["vector_reference"],output)
    for r in records:
        deadline.check();ref=r["vector_reference"];doc=fetch(ref)
        actual=pointer(doc,ref["json_pointer"])
        source_negative_gate(r,actual,ref,output)
        need(actual==r["coefficients_low_to_high"],"Source-map coefficients differ from exact original source pointer")
        body=pointer(doc,ref["record_pointer"]) if ref["record_pointer"] else doc
        need(sha(encoded(body))==ref["record_sha256"],"Original source row hash changed")
        tref=r["triple_reference"]
        need(triple(pointer(fetch(tref),tref["json_pointer"]))==triple(r["bare_triple"]),"Original source triple pointer changed")
        for extra in r.get("additional_vector_sources",[]):
            resolved=alternate_reference(r,extra)
            actual=pointer(fetch(resolved),resolved["json_pointer"])
            source_negative_gate(r,actual,resolved,output)
            need(list(map(rational,actual))==list(map(rational,r["coefficients_low_to_high"])),"Additional original vector source differs")
        if "adopted_disposition_reference" in r:
            ar=r["adopted_disposition_reference"];pointer(fetch(ar),ar["json_pointer"])
        evidence.append({"id":r["id"],"terminal_id":r["terminal_id"],"source_id":r["source_id"],
                         "vector_reference":ref,"triple_reference":tref,
                         "original_execution_identity":r["original_execution_identity"]})
    return evidence


def original_model(bare):
    bare=triple(bare);n=max(map(len,bare.values()))
    if n==1:
        h={"rank":1,"ambient_dimension":0,"rows":[],"points":[],
           "padded_boundary":{k:v+[0]*(1-len(v)) for k,v in bare.items()},"count_boundary_area":sum(bare["lambda"])}
    else:h=geometry.original_hive(bare)
    d=(n-1)*(n-2)//2
    need(h["rank"]==n and h["ambient_dimension"]==d and len(h["rows"])==3*n*(n-1)//2,"Full original hive geometry mismatch")
    return {"rank":n,"dimension":d,"count_boundary_area":h["count_boundary_area"],"full_rows":h["rows"],
            "padded_boundary":h["padded_boundary"],"original_hive_coordinate_points":h["points"],
            "unit_selections":[{"variable":j,"original_hive_coordinate":j,"base":0,"unit_row":[int(j==k) for k in range(d)]} for j in range(d)],
            "degree_is_ambient_upper_bound_not_actual_dimension":True,"affine_reduction_used":False,"strict_interior_used":False}
def validate_job(job,index,source):
    sid=integer(source["id"]);bare,terminal,binding=bind_triples(source["bare_triple"],source["terminal_source_triple"])
    need(job["unit"]=="LEGACY" and integer(job["id"])==sid==integer(index["id"])==integer(index["ordinal"]),
         "Job changed original local/physical identity")
    need(job["terminal_id"]==source["terminal_id"] and job["source_id"]==source["source_id"]
         and triple(job["bare_triple"])==bare and triple(job["terminal_source_triple"])==terminal
         and job["source_to_terminal_binding"]==binding,"Job lost its literal terminal/source/triple binding")
    model=original_model(bare)
    def integer_tree(value):
        if isinstance(value,dict):return all(integer_tree(x) for x in value.values())
        if isinstance(value,list):return all(integer_tree(x) for x in value)
        return type(value) is int
    need(all(integer_tree(job["model"][key]) for key in
             ("rank","dimension","count_boundary_area","full_rows","unit_selections","padded_boundary","original_hive_coordinate_points")),
         "Noninteger original geometry/coordinate arithmetic")
    need(set(job["model"])==set(model)|{"geometry_premise"} and isinstance(job["model"]["geometry_premise"],str)
         and all(job["model"][k]==value for k,value in model.items()),"Job is not the freshly rebuilt full original ordinary hive")
    d=model["dimension"]
    need(job["source_vector_accepted"] is False and integer(job["ambient_degree_upper_bound"])==d
         and job["determining_grades"]==list(range(d+1)) and job["unused_positive_grades"]==[d+1,d+2],"Wrong ambient degree bound or closed interpolation grid")
    gh=sha(encoded({"bare_triple":bare,"model":job["model"]}))
    need(gh==job["geometry_sha256"]==index["geometry_sha256"],"Original model/whole-triple geometry hash changed")
    need(job["certificate_reference"]==source["vector_reference"]
         and job["source_coefficients_low_to_high"]==source["coefficients_low_to_high"]
         and job["original_execution_identity"]==source["original_execution_identity"],"Job changed the selected source-vector provenance")
    nodes=job["nodes"]
    need(len(nodes)==d+3,"Incomplete full original-hive grade roster")
    expected=[]
    for grade,node in enumerate(nodes):
        need(node["kind"]==f"P{grade}" and integer(node["grade"])==grade and node["strict"] is False
             and node["role"]==("determining" if grade<=d else "positive_holdout"),"Non-closed, omitted or stale physical grade")
        need(set(node["stored"])=={"source_polynomial"} and integer(node["stored"]["source_polynomial"])>=0,"Invalid source-value provenance/model")
        expected.append(f"LEGACY:{sid}:P{grade}")
    need(index["node_ids"]==expected,"Index node identities differ from the complete regenerated grade roster")
    return {"id":sid,"terminal_id":source["terminal_id"],"bare_triple":bare,"terminal_source_triple":terminal,
            "binding":binding,"degree_upper_bound":d,"model":model,"geometry_sha256":gh,"nodes":nodes,
            "actual_hull_computed":False,"actual_dimension":None,"interior_parity_used":False}
def physical_system(record,grade):
    m=record["model"]
    bounds=[[0,grade*m["count_boundary_area"]] for _ in range(m["dimension"])]
    rows=[[grade*row[0],*row[1:]] for row in m["full_rows"]]
    return bounds,rows
def validate_count_row(row,record):
    sid=integer(row["id"]);grade=integer(row["grade"])
    need(sid==record["id"] and integer(row["record_ordinal"])==sid and 0<=grade<=record["degree_upper_bound"]+2,"Wrong physical record/grade")
    node=record["nodes"][grade];nid=f"LEGACY:{sid}:P{grade}"
    need(row["node_id"]==nid and row["kind"]==node["kind"] and row["strict"] is False
         and row["stored"]==node["stored"] and row["geometry_sha256"]==record["geometry_sha256"]
         and row["counter"]["id"]==nid,"Count is detached from its exact full original parent/model")
    need(row["geometry_acceptance"]=="CLASSICAL_FULL_AMBIENT_HIVE_AND_COORDINATE_BOUND_PREMISES","Unexpected old geometry acceptance premise")
    bounds,rows=physical_system(record,grade)
    need(row["full_system_sha256"]==sha(encoded({"bounds":bounds,"rows":rows})),"Count full-system hash differs from independently rebuilt ordinary hive")
    counter=row["counter"]
    if counter["status"]=="complete":
        need(row["status"] in ("MATCH","MISMATCH"),"Complete counter scalar has an invalid status")
        value=integer(counter["count"]);need(value>=0,"Negative scalar lattice count")
        return nid,value
    need(row["status"]=="REFUSED" and counter["status"].startswith("REFUSED_") and counter.get("count") is None,
         "Refusal contains a fabricated partial scalar")
    return nid,None


def report_name(path):
    path=Path(path).resolve()
    match=re.fullmatch(r"F2627-AUX-LEGACY-(\d{5})-(\d{2})-001",path.parent.name)
    need(path.name=="result.json" and match is not None,"Foreign or non-direct auxiliary report")
    start,retry=map(int,match.groups())
    need(start in range(0,272,8),"OLD_TAIL_EXCLUDED: only starts 0,8,...264 belong to the prefix")
    need(0<=retry<len(SCHEDULE),"Unknown auxiliary retry schedule")
    return start,retry
def discover_reports():
    return [W/"science"/f"F2627-AUX-LEGACY-{start:05d}-{retry:02d}-001"/"result.json"
            for start in range(0,272,8) for retry in range(3)
            if (W/"science"/f"F2627-AUX-LEGACY-{start:05d}-{retry:02d}-001"/"result.json").is_file()]
def envelope(path,inputs,code,expected_script,timeout):
    path=Path(path).resolve();report=inputs.read(path)
    folder=path.parent
    need(folder.parent==Path(code["run_check.py"]["path"]).parent/"science","Report escaped the original science root")
    config=inputs.read(folder/"config.json");receipt=inputs.read(folder/"receipt.json");launch=inputs.read(folder/"launch.json")
    need(receipt["id"]==config["id"]==folder.name and receipt["cleanup_verified"] is True
         and receipt["source_input_bytes_unchanged"] is True,"Unclean or changed-source actual caller receipt")
    need(type(receipt["pid"]) is int and receipt["pid"]>0 and receipt["pid"]==launch["pid"]==launch["pgid"]
         and type(receipt["returncode"]) is int,"Missing exact real child/exit identity")
    need(receipt["outputs"].get(path.name)==pin(path)["sha256"]
         and receipt["outputs"].get("launch.json")==pin(folder/"launch.json")["sha256"],"Unreceipted/changed semantic output or child launch")
    need(config["arm"]=="algebra" and config["native_calls"]==0 and config["deadline_seconds"]==timeout
         and config["declared_output_root"]==str(folder),"Caller resource or output ownership changed")
    argv=config["argv"];need(isinstance(argv,list) and all(type(x) is str for x in argv)
                            and argv[1:3]==["-B",code[expected_script]["path"]],"Caller used another source/entrypoint")
    python=inputs.bind(pin(argv[0]))
    need(config["sources"].get(python["path"])==python["sha256"],"Historical Python executable changed")
    return report,config,receipt,python
def check_envelope_maps(config,source_pins,input_pins):
    need(config["sources"]=={p["path"]:p["sha256"] for p in merge_pins(source_pins)}
         and config["inputs"]=={p["path"]:p["sha256"] for p in merge_pins(input_pins)},"Caller source/config/input hash map differs")
def resolve_from_config(value,config):
    p=Path(value)
    return (Path(config["cwd"])/p).resolve() if not p.is_absolute() else p.resolve()
def fixed_inputs(args,inputs):
    code={}
    for name,digest in PINS.items():
        p=inputs.bind(pin(W/name));need(p["sha256"]==digest,"Frozen source version changed: "+name);code[name]=p
    need(Path(geometry.__file__).resolve()==Path(code["index_legacy_tail_recounts.py"]["path"]),"Wrong imported geometry utility")
    code["accept_legacy_prefix.py"]=inputs.bind(pin(__file__))
    values={}
    for label,path in (("index",args.index),("source_map",args.source_map),("selection",args.selection),("build",args.build)):
        value=inputs.bind(pin(path));need(value["sha256"]==DATA_PINS[label],"Different immutable source version: "+label);values[label]=value
    values["amendment"]=inputs.bind(pin(W/"RESOURCE-AMENDMENT-001.md"))
    return code,values
def authenticate_index(args,inputs,code,pins):
    m,c,r,python=envelope(args.index,inputs,code,"index_legacy_recounts.py",120)
    need(m["schema"]==COUNT_SCHEMA and m["kind"]=="manifest" and m["status"]=="FROZEN_RECOUNT_JOBS"
         and m["unit"]=="LEGACY" and m["stream"]=="297-chosen-adopted-source-polynomials"
         and m["index_complete"] is True and m["selection_complete"] is True and not m["pending_index_ids"]
         and m["source_vectors_accepted"] is False and m["lattice_counts_performed"]==0,"Incomplete or wrong old legacy index")
    need(r["state"]=="complete" and r["returncode"]==0,"Original index lacks a successful actual caller")
    need(m["wrapper_sha256"]==code["recount_records.py"]["sha256"] and m["required_consumer"]==code["recount_records.py"]
         and bare_pin(m["indexer"])==code["index_legacy_recounts.py"] and m["indexer"]["command"]=="index","Old generator/consumer identity changed")
    need(c["argv"]==[python["path"],"-B",*m["indexer"]["argv"]],"Original index argv/source record differs")
    parser=argparse.ArgumentParser(add_help=False)
    parser.add_argument("command",choices=["index"]);parser.add_argument("--input",default=str(DEFAULT_SOURCES))
    parser.add_argument("--wrapper",default=str(W/"recount_records.py"));parser.add_argument("--geometry-helper",default=str(W/"box_geometry.py"))
    parser.add_argument("--budget-seconds",type=float,default=100);parser.add_argument("--output",required=True)
    try:old=parser.parse_args(c["argv"][3:])
    except SystemExit as error:raise Invalid("Malformed original index argv") from error
    need(resolve_from_config(old.input,c)==Path(pins["source_map"]["path"])
         and resolve_from_config(old.output,c)==Path(pins["index"]["path"])
         and resolve_from_config(old.wrapper,c)==Path(code["recount_records.py"]["path"])
         and resolve_from_config(old.geometry_helper,c)==Path(code["box_geometry.py"]["path"]),"Original index input/output/helper changed")
    check_envelope_maps(c,[python,*[code[k] for k in ("index_legacy_recounts.py","recount_records.py","box_geometry.py","run_check.py")]],
                        [pins["amendment"],pins["source_map"],pins["selection"]])
    records=m["records"]
    need(len(records)==297 and [integer(x["id"]) for x in records]==list(range(297))
         and m["expected_record_ids"]==list(range(297)),"Incomplete exact original 297 index roster")
    offset=0
    for ordinal,record in enumerate(records):
        need(integer(record["ordinal"])==ordinal and integer(record["offset"])==offset and integer(record["bytes"])>0,
             "Old job ordinal/offset roster changed")
        offset+=record["bytes"]
    need(offset==m["jobs"]["bytes"],"Old complete jobs byte coverage differs")
    inputs.bind(m["jobs"])
    need(r["outputs"].get(Path(m["jobs"]["path"]).name)==m["jobs"]["sha256"],"Old jobs file has no original output receipt")
    return m
def authenticate_build(args,inputs,code,pins):
    b,c,r,python=envelope(args.build,inputs,code,"recount_records.py",30)
    need(b["schema"]==COUNT_SCHEMA and b["kind"]=="build" and b["status"]=="BUILT_OWN_COUNTER"
         and b["wrapper_sha256"]==code["recount_records.py"]["sha256"] and b["source"]==code["v2_independent_hive_recount.cpp"]
         and r["state"]=="complete" and r["returncode"]==0,"Changed/unsuccessful original v2 build")
    binary=inputs.bind(b["binary"])
    need(Path(binary["path"]).parent==Path(args.build).resolve().parent
         and r["outputs"].get(Path(binary["path"]).name)==binary["sha256"],"Build binary is not a receipted immutable output")
    expected=[python["path"],"-B",code["recount_records.py"]["path"],"build","--cpp-source","v2_independent_hive_recount.cpp",
              "--binary","science/F2627-RECOUNT-V2-BUILD-002/recount","--output",pins["build"]["path"]]
    need(c["argv"]==expected and resolve_from_config(c["argv"][5],c)==Path(b["source"]["path"])
         and resolve_from_config(c["argv"][7],c)==Path(binary["path"]),"Original compiler wrapper argv differs")
    need(b["command"]==["/usr/bin/c++","-std=c++17","-O2","-Wall","-Wextra",b["source"]["path"],"-o",binary["path"]],
         "Original actual compile command changed")
    check_envelope_maps(c,[python,*[code[k] for k in ("recount_records.py","v2_independent_hive_recount.cpp","run_check.py")]],
                        [pins["amendment"]])
    return b
def load_prefix_jobs(index,records,inputs,deadline):
    out={}
    with Path(index["jobs"]["path"]).open("rb") as stream:
        for source in records:
            deadline.check();entry=index["records"][source["id"]]
            stream.seek(entry["offset"]);raw=stream.read(entry["bytes"])
            need(raw.endswith(b"\n") and sha(raw)==entry["sha256"],"Original prefix job bytes changed")
            job=decode(raw);out[source["id"]]=validate_job(job,entry,source)
    return out
def collect_reports(paths,index,models,build,inputs,code,pins,deadline):
    keyed={}
    for path in paths:
        key=report_name(path);need(key not in keyed,"Duplicate exact auxiliary attempt")
        keyed[key]=Path(path).resolve()
    actual={};rows_by_node={};evidence=[];refusals=[];seen_starts=set();history=defaultdict(list);label_matches=defaultdict(set)
    all_nodes={nid for record in index["records"] for nid in record["node_ids"]}
    for (start,retry),path in sorted(keyed.items()):
        deadline.check();seen_starts.add(start)
        need(retry==len(history[start]),"Omitted/reordered same-slice retry prefix")
        report,c,r,python=envelope(path,inputs,code,"recount_records.py",120)
        stop=start+8
        previous=[str(p) for p in history[start]]
        milliseconds,states=SCHEDULE[retry]
        expected=[python["path"],"-B",code["recount_records.py"]["path"],"run","--manifest",pins["index"]["path"],
                  "--build",pins["build"]["path"],"--start",str(start),"--limit","8","--node-ms",str(milliseconds),
                  "--max-states",str(states),"--budget-seconds","90","--resume-from",*previous,"--output",str(path)]
        need(c["argv"]==expected,"Auxiliary original manifest/slice/retry/resources argv changed")
        check_envelope_maps(c,[python,*[code[k] for k in ("recount_records.py","run_auxiliary_recounts.py","run_check.py")]],
                            [pins["amendment"],pins["index"],pins["build"],*[pin(p) for p in previous]])
        need(report["schema"]==COUNT_SCHEMA and report["kind"]=="run"
             and report["manifest_sha256"]==pins["index"]["sha256"] and report["wrapper_sha256"]==code["recount_records.py"]["sha256"]
             and report["build_reference"]==pins["build"] and report["build"]==build["binary"]
             and report["counter_source"]==build["source"] and integer(report["start"])==start
             and integer(report["requested_stop"])==stop,"Wrong source-bound complete physical slice")
        status=report["status"]
        need((status=="SLICE_RECOUNTS_MATCH" and r["state"]=="complete" and r["returncode"]==0)
             or (status=="PARTIAL" and r["state"]=="invalid_input_or_output" and r["returncode"]==2)
             or (status=="COUNT_MISMATCH" and r["state"]=="invalid_input_or_output" and r["returncode"]==1),
             "Reported count/refusal status has no exact actual caller exit")
        need(type(report["counter_pid"]) is int and report["counter_pid"]>0
             and type(report["counter_exit_code"]) is int,"Counter process exit is unobserved")
        if status=="SLICE_RECOUNTS_MATCH":need(report["counter_exit_code"]==0,"Successful slice has a failed counter exit")
        ledger=inputs.bind(report["results"])
        need(Path(ledger["path"]).parent==path.parent and r["outputs"].get(Path(ledger["path"]).name)==ledger["sha256"],
             "Count ledger is not an exact receipted output")
        local=set();matched_labels=[];refused_labels=[];count=0
        report_pin=pin(path);receipt_pin=pin(path.parent/"receipt.json")
        with Path(ledger["path"]).open("rb") as stream:
            for line,raw in enumerate(stream,1):
                deadline.check();need(raw.endswith(b"\n") and raw.strip(),"Malformed count JSONL")
                row=decode(raw);sid=integer(row["id"])
                need(0<=sid<272 and start<=sid<stop and sid in models,"OLD_TAIL_EXCLUDED or foreign physical record")
                nid,value=validate_count_row(row,models[sid])
                need(nid not in local,"Duplicate physical site within one direct run");local.add(nid);count+=1
                row_evidence={"report":report_pin,"ledger":ledger,"line":line,"line_sha256":sha(raw),
                              "wrapper_pid":r["pid"],"counter_pid":report["counter_pid"],
                              "counter_exit_code":report["counter_exit_code"],"caller_receipt":receipt_pin}
                if value is None:
                    refused_labels.append(nid);refusals.append({"node_id":nid,"counter":row["counter"],**row_evidence})
                else:
                    need(nid not in actual,"Duplicate successful physical site, including agreeing same-slice retries")
                    actual[nid]=value;rows_by_node[nid]={"row":row,"evidence":row_evidence}
                    if row["status"]=="MATCH":matched_labels.append(nid)
        need(integer(report["attempted_nodes"])==count and sorted(report["matched_node_ids"])==sorted(matched_labels)
             and sorted(report["refused_node_ids"])==sorted(refused_labels),"Direct count summary drops/duplicates physical rows")
        label_matches[start].update(matched_labels)
        need(report["pending_node_ids"]==sorted(all_nodes-label_matches[start]),"Original global pending roster differs from its exact same-slice prefix")
        wanted={node for rec in index["records"][start:stop] for node in rec["node_ids"]}
        if status=="SLICE_RECOUNTS_MATCH":need(wanted<=label_matches[start],"Claimed complete slice has unaccounted nodes")
        history[start].append(path)
        evidence.append({"start":start,"stop":stop,"retry":retry,"status":status,"report":pin(path),
                         "config":pin(path.parent/"config.json"),"receipt":pin(path.parent/"receipt.json"),
                         "launch":pin(path.parent/"launch.json"),"results":ledger,"wrapper_pid":r["pid"],
                         "counter_pid":report["counter_pid"],"counter_exit_code":report["counter_exit_code"],
                         "supervising_auxiliary_process_exit":"Not separately recorded by the old launcher; no invented outer caller PID or wait"})
    expected={nid for sid in PREFIX for nid in index["records"][sid]["node_ids"]}
    need(set(actual)<=expected,"Foreign counted node in prefix union")
    return actual,rows_by_node,sorted(expected-set(actual)),sorted(set(range(0,272,8))-seen_starts),evidence,refusals


def add_poly(a,b):
    return [(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0)) for i in range(max(len(a),len(b)))]
def multiply(a,b):
    result=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):result[i+j]+=x*y
    return result
def evaluate(coefficients,t):
    result=Q(0)
    for c in reversed(coefficients):result=result*t+c
    return result
def interpolate_grid(values):
    d=len(values)-1;difference=list(map(Q,values));basis=[Q(1)];answer=[Q(0)]*(d+1)
    for k in range(d+1):
        if k:basis=[c/Q(k) for c in multiply(basis,[-(k-1),1])]
        for j,c in enumerate(basis):answer[j]+=difference[0]*c
        difference=[b-a for a,b in zip(difference,difference[1:])]
    # A separately structured Lagrange reconstruction cross-checks arithmetic.
    second=[Q(0)]*(d+1)
    for i,value in enumerate(values):
        term=[Q(1)];den=1
        for j in range(d+1):
            if i!=j:term=multiply(term,[-j,1]);den*=i-j
        for j,c in enumerate(term):second[j]+=Q(value)*c/den
    need(answer==second,"Independent exact polynomial reconstructions disagree")
    return answer
def reconstruct_one(record,counts):
    sid=record["id"];d=record["degree_upper_bound"]
    need(all(f"LEGACY:{sid}:P{t}" in counts for t in range(d+3)),"Missing physical determining/hold site")
    witness=counts[f"LEGACY:{sid}:P1"]
    need(witness>0,"EMPTY_POSITIVE_GRADE: artificial t=0 count cannot prove nonemptiness")
    need(counts[f"LEGACY:{sid}:P0"]==1,"Nonempty polynomial constant disagrees with the observed zero-grade count")
    coefficients=interpolate_grid([counts[f"LEGACY:{sid}:P{t}"] for t in range(d+1)])
    return {"id":sid,"terminal_id":record["terminal_id"],"bare_triple":record["bare_triple"],
            "terminal_source_triple":record["terminal_source_triple"],"source_to_terminal_binding":record["binding"],
            "geometry_sha256":record["geometry_sha256"],"degree_upper_bound":d,
            "coefficients_low_to_high":list(map(str,coefficients)),
            "reconstructed_polynomial_degree":max(i for i,c in enumerate(coefficients) if c),
            "nonempty_witness":{"grade":1,"count":str(witness),"fresh_complete_counter_required":True},
            "determining_grades":list(range(d+1)),"unused_positive_grades":[d+1,d+2],
            "actual_hull_computed":False,"actual_dimension":None,"interior_parity_used":False,
            "source_and_hold_comparisons_performed":False}
def raw_vectors(models,counts,output,deadline,prefix_ids=PREFIX,progress=None):
    records=[];negative=[]
    journal=Path(output).with_suffix(".raw-vectors.jsonl")
    with journal.open("xb") as stream:
        for sid in prefix_ids:
            deadline.check();r=reconstruct_one(models[sid],counts);records.append(r)
            observed=[{"id":sid,"terminal_id":r["terminal_id"],"bare_triple":r["bare_triple"],
                       "degree":degree,"coefficient":value,"scope":"Entire fresh original-hive polynomial under the stated classical premises"}
                      for degree,value in enumerate(r["coefficients_low_to_high"]) if rational(value)<0]
            negative += observed
            stream.write(encoded({"record":r,"ordinary_negative_observations":observed,
                                  "source_or_hold_comparisons_performed":False})+b"\n")
            stream.flush();os.fsync(stream.fileno())
            if progress is not None:
                progress["pending_polynomial_ids"]=[i for i in prefix_ids if i>sid]
                progress["ordinary_negative_observations"]=list(negative)
            if observed:
                break  # the whole negative is durable; return the root hold now
    raw=Path(output).with_suffix(".raw-vectors.json")
    save(raw,{"schema":SCHEMA,"kind":"raw_vectors","status":"PRESERVED_BEFORE_SOURCE_OR_HOLD_COMPARISONS",
              "records":records,"ordinary_negative_observations":negative,
              "constant_gate":"Every parent has a fresh complete grade-one count greater than zero",
              "source_and_hold_comparisons_performed":False,"raw_journal":pin(journal),"premises":PREMISES})
    return records,negative,pin(raw)
def compare_one(raw,source,model,counts,rows):
    d=raw["degree_upper_bound"];fresh=list(map(rational,raw["coefficients_low_to_high"]))
    original=list(map(rational,source["coefficients_low_to_high"]))
    need(len(original)<=d+1 and len(original)==integer(source["source_declared_degree"])+1,"Source coefficient roster exceeds its bound or declared full length")
    expected=original+[Q(0)]*(d+1-len(original))
    need(fresh==expected,"Entire source polynomial differs from independently reconstructed vector")
    holds=[]
    for grade in (d+1,d+2):
        nid=f"LEGACY:{raw['id']}:P{grade}";value=counts[nid]
        need(evaluate(fresh,grade)==value,"Unused positive-grade holdout differs")
        holds.append({"grade":grade,"count":str(value),"used_for_interpolation":False,
                      "used_only_as_boolean_nonempty_witness":grade==1,"evidence":rows[nid]["evidence"]})
    for grade,node in enumerate(model["nodes"]):
        nid=f"LEGACY:{raw['id']}:P{grade}";value=counts[nid]
        expected_value=evaluate(original,grade)
        need(expected_value.denominator==1 and expected_value==integer(node["stored"]["source_polynomial"])==value,
             "Source vector, frozen expected scalar and fresh complete count differ")
        row=rows[nid]["row"]
        need(row["status"]=="MATCH" and row["matches"]=={"source_polynomial":True},"False original successful comparison status")
    return {"id":raw["id"],"terminal_id":source["terminal_id"],"source_id":source["source_id"],
            "bare_triple":raw["bare_triple"],"terminal_source_triple":raw["terminal_source_triple"],
            "source_to_terminal_binding":raw["source_to_terminal_binding"],"degree_upper_bound":d,
            "coefficients_low_to_high":raw["coefficients_low_to_high"],"unused_holds":holds,
            "nonempty_witness":{**raw["nonempty_witness"],"evidence":rows[f"LEGACY:{raw['id']}:P1"]["evidence"]},
            "vector_reference":source["vector_reference"],"original_execution_identity":source["original_execution_identity"],
            "fresh_node_ids":[f"LEGACY:{raw['id']}:P{t}" for t in range(d+3)],
            "actual_hull_computed":False,"actual_dimension":None,"interior_parity_used":False}


def declared_files(args):
    reports=args.reports if args.reports is not None else discover_reports()
    for path in reports:report_name(path)  # reject old tail BEFORE opening a count ledger
    need(reports,"No direct prefix count reports supplied")
    reader=Inputs()
    m=reader.read(args.index);document=reader.read(args.source_map)
    selected=document["records"][:272]
    base=[args.index,args.source_map,args.selection,args.build,m["jobs"]["path"],W/"RESOURCE-AMENDMENT-001.md"]
    build=reader.read(args.build);base.append(build["binary"]["path"])
    for path in [args.index,args.build,*reports]:
        base += [path,*[Path(path).parent/name for name in ("config.json","receipt.json","launch.json")]]
    for path in reports:
        report=reader.read(path)
        if "results" in report:base.append(report["results"]["path"])
    for record in selected:
        refs=[record["vector_reference"],record["triple_reference"],
              *[alternate_reference(record,r) for r in record.get("additional_vector_sources",[])]]
        if "adopted_disposition_reference" in record:refs.append(record["adopted_disposition_reference"])
        base += [r["path"] for r in refs]
    files=merge_pins(pin(p) for p in base);reader.after()
    return reports,files
def command(args):
    need(re.fullmatch(r"F2627-[A-Za-z0-9-]+",args.id) is not None,"Invalid fresh harness ID")
    reports,files=declared_files(args)
    py=str(Path(sys.executable).resolve())
    argv=[py,"-B",str(W/"run_check.py"),"--id",args.id,"--arm","algebra","--timeout","120","--python",py]
    for path in [Path(__file__),*[W/name for name in PINS]]:argv += ["--dependency",str(path.resolve())]
    for value in files:argv += ["--input",value["path"]]
    argv += ["--expectation","Exact legacy prefix 0..271: complete original hives, positive-grade nonemptiness, negative-first full polynomial/hold/source acceptance; old tail excluded",
             str(Path(__file__).resolve()),"accept","--index",str(args.index.resolve()),"--source-map",str(args.source_map.resolve()),
             "--selection",str(args.selection.resolve()),"--build",str(args.build.resolve()),
             "--budget-seconds",str(args.budget_seconds),"--reports",*[str(Path(p).resolve()) for p in reports]]
    return {"argv":argv,"launches_nothing":True,"prefix_ids":[0,271],"excluded_old_tail_ids":[272,296],
            "expected_output":str(W/"science"/args.id/"result.json"),"declared_input_count":len(files)}
def accept(args):
    output=args.output.resolve()
    need(output.parent.is_dir() and not output.exists() and not output.is_relative_to(args.source_map.resolve().parent),
         "Fresh acceptance output outside immutable source metadata is required")
    need(not output.is_relative_to(C) or output.is_relative_to(C/"results/raw"),"Acceptance output cannot overwrite canonical source/method trees")
    deadline=Deadline(args.budget_seconds);inputs=Inputs()
    reports=args.reports if args.reports is not None else discover_reports()
    for path in reports:report_name(path)
    result={"schema":SCHEMA,"status":"PARTIAL","source_vectors_accepted":False,"accepted":[],
            "expected_record_ids":list(PREFIX),"excluded_old_record_ids":list(EXCLUDED),"pending_record_ids":list(PREFIX),
            "pending_polynomial_ids":list(PREFIX),
            "premises":PREMISES,"lattice_counts_performed":0,"source_bytes_verified_before_after":False,
            "scope":"Exact old prefix only; new tail 272..296 requires its separate complete acceptance",
            "argv":[str(Path(__file__).resolve()),*sys.argv[1:]]}
    try:
        code,pins=fixed_inputs(args,inputs);result["code"]=code;result["frozen_inputs"]=pins
        document=inputs.read(args.source_map,pins["source_map"]);selection=inputs.read(args.selection,pins["selection"])
        need(bare_pin(document["selection_reference"])==pins["selection"],"Source metadata selected another terminal roster")
        records=metadata_roster(document,selection)
        result["expected_terminal_ids"]=[r["terminal_id"] for r in records]
        # Scan the newly read map itself before any old-vector reconciliation.
        for r in records:source_negative_gate(r,r["coefficients_low_to_high"],r["vector_reference"],output)
        result["literal_source_evidence"]=source_documents(records,document,inputs,output,deadline)
        index=authenticate_index(args,inputs,code,pins)
        need(index["terminal_id_mapping"]==[{"id":r["id"],"terminal_id":r["terminal_id"],"source_id":r["source_id"]} for r in document["records"]],
             "Old index-to-literal-terminal mapping changed")
        build=authenticate_build(args,inputs,code,pins)
        models=load_prefix_jobs(index,records,inputs,deadline)
        result["regenerated_original_hives"]=len(models)
        counts,rows,missing,missing_slices,evidence,refusals=collect_reports(reports,index,models,build,inputs,code,pins,deadline)
        result.update(count_evidence=evidence,refusals=refusals,pending_node_ids=missing,missing_slice_starts=missing_slices,
                      complete_physical_sites=len(counts),pending_record_ids=[i for i in PREFIX if any(nid in missing for nid in index["records"][i]["node_ids"])])
        empty=[{"id":i,"terminal_id":models[i]["terminal_id"],"grade":1,"count":"0",
                "evidence":rows[f"LEGACY:{i}:P1"]["evidence"]} for i in PREFIX if counts.get(f"LEGACY:{i}:P1")==0]
        if empty:
            result.update(status="EMPTY_POSITIVE_GRADE_REJECTED",empty_positive_grade_observations=empty,
                          constant_one_used=False,reason="The artificial t=0 hive is not a nonempty-family witness")
            return result
        if missing or missing_slices:return result
        raw,negative,raw_pin=raw_vectors(models,counts,output,deadline,progress=result)
        result.update(raw_reconstructed_vectors=raw_pin,ordinary_negative_observations=negative)
        if negative:
            result.update(status="ORDINARY_NEGATIVE_OBSERVED",source_or_hold_comparisons_performed=False)
            return result
        accepted=[]
        for source,vector in zip(records,raw):
            deadline.check();accepted.append(compare_one(vector,source,models[source["id"]],counts,rows))
        need([r["id"] for r in accepted]==list(PREFIX)
             and [r["terminal_id"] for r in accepted]==result["expected_terminal_ids"]
             and len({r["terminal_id"] for r in accepted})==272,"Incomplete final exact prefix terminal union")
        result.update(status="COMPLETE_LEGACY_PREFIX_POLYNOMIALS_VERIFIED",source_vectors_accepted=True,accepted=accepted,
                      accepted_terminal_ids=[r["terminal_id"] for r in accepted],
                      accepted_terminal_ids_sha256=sha(encoded([r["terminal_id"] for r in accepted])),
                      pending_record_ids=[],pending_node_ids=[],source_or_hold_comparisons_performed=True,
                      no_actual_hull_or_parity_claim=True,
                      remaining_join="Separate fresh tail acceptance for 272..296, then root's exact 297-terminal/composition join")
    except SourceNegative as error:
        result.update(status="HOLD_SOURCE_NEGATIVE",source_negative_observation=error.observation,
                      source_or_hold_comparisons_performed=False)
    except DeadlineReached as error:
        result.update(status="PARTIAL",interruption=str(error))
    except (Invalid,geometry.CheckError,KeyError,TypeError,ValueError,OSError,IndexError,ZeroDivisionError) as error:
        result.update(status="FAIL",error=f"{type(error).__name__}: {error}")
    finally:
        raw=output.with_suffix(".raw-vectors.json")
        if raw.exists():result["raw_reconstructed_vectors"]=pin(raw)
        journal=output.with_suffix(".raw-vectors.jsonl")
        if journal.exists():result["raw_reconstructed_journal"]=pin(journal)
        try:
            inputs.after();result["source_bytes_verified_before_after"]=True
        except (Invalid,OSError) as error:
            result.update(status="FAIL",source_vectors_accepted=False,source_error=str(error))
        result["read_inputs"]=merge_pins(inputs.used.values())
        save(output,result)
    return result
def parser():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command",choices=("accept","command"))
    p.add_argument("--index",type=Path,default=DEFAULT_INDEX)
    p.add_argument("--source-map",type=Path,default=DEFAULT_SOURCES)
    p.add_argument("--selection",type=Path,default=DEFAULT_SELECTION)
    p.add_argument("--build",type=Path,default=DEFAULT_BUILD)
    p.add_argument("--reports",type=Path,nargs="+")
    p.add_argument("--budget-seconds",type=float,default=95)
    p.add_argument("--id")
    p.add_argument("--output",type=Path)
    return p
def main():
    args=parser().parse_args();started=time.monotonic()
    try:
        if args.command=="command":
            need(args.id,"command requires a fresh --id");print(json.dumps(command(args),indent=2));return 0
        need(args.output is not None,"accept requires --output")
        result=accept(args)
    except (Invalid,KeyError,TypeError,ValueError,OSError) as error:
        print(json.dumps({"status":"FAIL","error":f"{type(error).__name__}: {error}"}),file=sys.stderr);return 1
    print(json.dumps({"status":result["status"],"accepted":len(result["accepted"]),
                      "pending_record_ids":result["pending_record_ids"],"output":str(args.output.resolve()),
                      "lattice_counts_performed":0,"elapsed_seconds":time.monotonic()-started}))
    return 0 if result["status"]=="COMPLETE_LEGACY_PREFIX_POLYNOMIALS_VERIFIED" else 2 if result["status"]=="PARTIAL" else 1


if __name__=="__main__":
    raise SystemExit(main())
