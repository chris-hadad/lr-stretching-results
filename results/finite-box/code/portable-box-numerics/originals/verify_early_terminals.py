#!/usr/bin/env python3
"""Exact early U02/U03 certificate, geometry and raw-count binding checks.

  python3 verify_early_terminals.py --root RESTORED_ROOT --unit U02 \
    --source-manifest RESTORED_ROOT/MEMBERS.jsonl --source-manifest-sha256 SHA \
    --start 0 --stop 50 --output OUT/u02-000.json

U02's exact roster has 211 IDs; U03's has 4,131 IDs. Slices are half-open.
--required-ids plus --required-ids-sha256 may select the explicit used subset
(including CHOSEN-TERMINALS.json). Slice ordinals then follow the selected IDs
in their original certificate order; selection does not confer acceptance.
Each completed ID is flushed to an adjacent .identities.jsonl. Missing sources,
refused evidence without a completed replacement, and interrupted slices cannot
produce a complete result. All consumed source files are authenticated before
use and rehashed afterwards. The manifest can alternatively be JSON with
schema='early-input-manifest-v1' and files=[{path,bytes,sha256}], with paths
relative to --root. No returned source is imported, compiled or executed.

This independently checks geometry, count-request identities, exact interpolation
and coefficient signs. It does NOT perform new numerical lattice counts. Correct
recorded counter values remain an explicit premise pending independent recount.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
import gzip
import hashlib
from itertools import zip_longest
import json
import os
from math import gcd
from pathlib import Path
import re
import signal
import time

import box_geometry_early as G


SCHEMA="pro026-early-terminal-verification-v1"
ROSTERS={"U02":("DATA/U02/two-model-mixed-certificate.json",211),
         "U03":("DATA/U03/hybrid-verification-v3/certificates.jsonl",4131)}
SHA=re.compile(r"[0-9a-f]{64}\Z")
PREMISES=[
    "The recorded raw counter outputs are correct; no fresh lattice recount is performed here.",
    "The adopted hive/LR correspondence, stretching polynomiality and Ehrhart reciprocity.",
    "The independently adopted complete forced-boundary-mask tables.",
    "For four-count cases only: the adopted short-normal theorem protects the top three coefficients.",
    "For gap repairs only: the adopted whole-count gap/empty-row and tensor identities.",
]


class SourceGap(ValueError):
    pass


class CandidateObservation(ValueError):
    pass


def need(value,message):
    if not value:
        raise ValueError(message)


def integer(value):
    if type(value) is str:
        need(re.fullmatch(r"-?(0|[1-9][0-9]*)",value) is not None,"Malformed integer")
        value=int(value)
    need(type(value) is int,"Boolean/float is not an exact integer")
    return value


def rational(value):
    need(type(value) in (int,str),"Nonexact rational coefficient")
    return Q(value)


def encoded(value):
    return json.dumps(value,separators=(",",":"),sort_keys=True,allow_nan=False).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_data(data):
    def unique(pairs):
        result={}
        for key,value in pairs:
            need(key not in result,"Duplicate JSON key")
            result[key]=value
        return result
    def constant(value):
        raise ValueError("Nonfinite JSON number: "+value)
    return json.loads(data,object_pairs_hook=unique,parse_constant=constant)


def pin(path):
    path=Path(path)
    need(path.is_file() and not path.is_symlink(),"Missing/nonregular bound source: "+str(path))
    before=path.stat()
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):
            h.update(block)
    after=path.stat()
    need((before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
         (after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),"Source changed while hashing")
    return {"bytes":before.st_size,"sha256":h.hexdigest()}


class Inputs:
    def __init__(self,root,manifest,expected_sha):
        self.root=Path(root).resolve()
        self.manifest=Path(manifest).resolve()
        need(SHA.fullmatch(expected_sha or ""),"An explicit source-manifest SHA-256 is required")
        self.manifest_pin=pin(self.manifest)
        need(self.manifest_pin["sha256"]==expected_sha,"Source manifest changed")
        raw=self.manifest.read_bytes()
        need(digest(raw)==expected_sha,"Source manifest changed before parsing")
        self.expected={}
        if self.manifest.suffix==".jsonl":
            declarations=[json_data(line) for line in raw.splitlines() if line.strip()]
            for row in declarations:
                if row.get("state")!="restored_inert":
                    continue
                output=Path(row["output_path"])
                need(output.is_absolute(), "Restored member output must be absolute")
                output=output.resolve()
                need(output.is_relative_to(self.root),
                     "Restored member output is outside the declared source root")
                name=str(output.relative_to(self.root))
                self._declare(name,{"bytes":row["bytes"],"sha256":row["sha256"]})
        else:
            declaration=json_data(raw)
            need(declaration.get("schema")=="early-input-manifest-v1","Unknown explicit input manifest")
            for row in declaration["files"]:
                self._declare(row["path"],{k:row[k] for k in ("bytes","sha256")})
        self.used={}
        self.cache={}
        self.tables={}
        self.query_tables={}
        self.references=[]
        self.candidate_path=None
        self.candidate_context=None

    def capture_candidate(self,observation):
        need(self.candidate_path is not None and self.candidate_context is not None,
             "Negative observation lacks its declared durable output")
        body={"schema":"early-LR-primary-negative-observation-v1",
              "status":"HOLD_CANDIDATE_PENDING_INDEPENDENT_COUNT_VERIFICATION",
              **self.candidate_context,"observation":observation,
              "source_manifest":self.manifest_pin,"accessed_sources":self.used,
              "source_references":self.references,
              "recorded_counts_not_yet_independently_recounted":True,
              "captured_before_vector_or_other_model_comparison":True}
        with self.candidate_path.open('x') as stream:
            json.dump(body,stream,indent=2,sort_keys=True)
            stream.write('\n');stream.flush();os.fsync(stream.fileno())
        raise CandidateObservation("Ordinary-negative primary whole-LR observation preserved at "+str(self.candidate_path))

    def _declare(self,name,binding):
        p=Path(name)
        need(not p.is_absolute() and ".." not in p.parts and str(p)==name,"Escaping/noncanonical manifest path")
        need(integer(binding["bytes"])>=0 and SHA.fullmatch(binding["sha256"] or ""),"Malformed manifest file binding")
        need(name not in self.expected or self.expected[name]==binding,"Conflicting source manifest entries")
        self.expected[name]=binding

    def has(self,name):
        return name in self.expected

    def path(self,name):
        if name not in self.expected:
            raise SourceGap("Source is not bound by the provided manifest: "+name)
        path=self.root/name
        if not path.is_file():
            raise SourceGap("Bound source is missing: "+name)
        need(path.resolve().is_relative_to(self.root) and not path.is_symlink(),"Escaping source link")
        if name not in self.used:
            actual=pin(path)
            need(actual==self.expected[name],"Stale source bytes: "+name)
            self.used[name]=actual
        return path

    def raw(self,name):
        if name not in self.cache:
            self.cache[name]=self.path(name).read_bytes()
            need({"bytes":len(self.cache[name]),"sha256":digest(self.cache[name])}==self.used[name],"Source changed before reading")
        return self.cache[name]

    def ref(self,name,locator="file",body=None,raw=None,*,track=True):
        self.path(name)
        result={"path":name,"source_sha256":self.used[name]["sha256"],"locator":locator}
        if raw is not None:
            result.update(record_sha256=digest(raw),record_encoding="raw-line-with-newline")
        elif body is not None:
            result.update(record_sha256=digest(encoded(body)),record_encoding="canonical-json-object")
        if track:
            self.references.append(result)
        return result

    def json(self,name):
        data=self.raw(name)
        return json_data(gzip.decompress(data) if name.endswith(".gz") else data)

    def records(self,name,field=None):
        if field is not None:
            document=self.json(name)
            rows=document if field=="$" else document[field]
            need(isinstance(rows,list),"Expected a literal record array")
            return [(row,self.ref(name,f"{field}[{i}]",body=row,track=False)) for i,row in enumerate(rows)]
        data=self.raw(name)
        if name.endswith(".gz"):
            data=gzip.decompress(data)
        out=[]
        for number,line in enumerate(data.splitlines(keepends=True),1):
            need(line.strip() and line.endswith(b"\n"),"Malformed source JSONL record")
            row=json_data(line)
            out.append((row,self.ref(name,f"line:{number}",raw=line,track=False)))
        return out

    def index(self,name,field=None):
        cache_key=(name,field)
        if cache_key not in self.tables:
            table={}
            for row,ref in self.records(name,field):
                idx=integer(row["id"])
                need(idx not in table,"Duplicate source record ID: "+name)
                table[idx]=(row,ref)
            self.tables[cache_key]=table
        return self.tables[cache_key]

    def get(self,name,idx,field=None):
        table=self.index(name,field)
        if idx not in table:
            raise SourceGap(f"Required record {idx} is absent from {name}")
        row,ref=table[idx]
        self.references.append(ref)
        return row,ref

    def queries(self,name,response):
        if name not in self.query_tables:
            table=defaultdict(list)
            for row,ref in self.records(name):
                need(isinstance(row.get("request"),str) and isinstance(row.get("response"),dict),"Malformed raw query entry")
                table[row["response"]["id"]].append((row,ref))
            self.query_tables[name]=table
        candidates=self.query_tables[name].get(response["id"],[])
        if not any(row["response"]==response for row,_ in candidates):
            raise SourceGap("No exact raw response/request binding for "+str(response["id"]))
        for _,ref in candidates:
            self.references.append(ref)
        return candidates

    def finish(self):
        for name,binding in self.used.items():
            need(pin(self.root/name)==binding,"Source changed after verification: "+name)
        need(pin(self.manifest)==self.manifest_pin,"Source manifest changed during verification")


def relative(unit,name):
    need(isinstance(name,str) and name.startswith(f"DATA/{unit}/") and ".." not in Path(name).parts,"Cross-unit or escaping source reference")
    return "namespaces/"+unit.lower()+"/"+name


def padded(part,n):
    part=[integer(x) for x in part]
    need(len(part)<=n and all(x>=0 for x in part) and part==sorted(part,reverse=True),"Invalid literal partition")
    return part+[0]*(n-len(part))


def check_identity(record,geometry):
    need(integer(record["id"])==integer(geometry["id"]) and record["bare_triple"]==geometry["original"],"Different bare triple or original identity")
    if "raw_record" in record:
        need(record["raw_record"]==geometry["raw_record"],"Changed original eight-column record")
    if "count_boundary" in record:
        need(record["count_boundary"]==geometry["count_boundary"],"Changed count boundary")


def normalize_geometry(geometry,unit,needs_dimension):
    chart=geometry["chart"]
    mathematical_rows=[*geometry["original_rhombus_rows"],*geometry["full_translated_rows"],
                       *geometry["count_rows"],*chart["basis_rows"],*chart["rows"],
                       chart["offset"],geometry["translation"]]
    need(all(type(x) is int for row in mathematical_rows for x in row),"Noninteger original-lattice chart coefficient")
    adapted=deepcopy(geometry)
    changes=[]
    if "affine_repair" not in adapted:
        # The source supplies the full chart, translation and all substituted
        # rows. The copied checker proves their exact direct substitution.
        adapted["affine_repair"]={}
        changes.append({"field":"affine_repair","normalization":"legacy direct full-chart substitution; no added repair steps"})
    if unit=="U02" and needs_dimension:
        premises=geometry["interior_premises"]
        need(integer(premises["id"])==integer(geometry["id"]),"Dimension witness identity mismatch")
        if premises.get("actual_dimension") is None:
            raise SourceGap("Negative node needs a sourced actual dimension and strict witness")
        d=integer(premises["actual_dimension"])
        need(d==integer(geometry["degree_bound"]),"Interior dimension differs from the chart dimension")
        selected=[(i,w) for i,w in enumerate(premises["checked_grades"])
                  if w.get("status")=="verified_strict_point" and w.get("t")==premises["witness_grade"]]
        need(len(selected)==1,"Missing/duplicate selected strict dimension witness")
        number,witness=selected[0]
        fields=("t","point","whole_hive_point","all_original_rhombus_slacks")
        need(all(k in witness for k in fields),"Missing literal strict witness fields")
        adapted["actual_dimension"]=d
        adapted["dimension_gate"]={k:deepcopy(witness[k]) for k in fields}
        changes.append({"field":"actual_dimension","source_field":"interior_premises.actual_dimension"})
        changes.append({"field":"dimension_gate","source_field":f"interior_premises.checked_grades[{number}]",
                        "source_record_sha256":digest(encoded(witness))})
    return adapted,{"original_geometry_sha256":digest(encoded(geometry)),"normalized_geometry_sha256":digest(encoded(adapted)),"normalizations":changes}


def geometry_check(inputs,geometry,unit,needs_dimension,short_normals):
    n=integer(geometry["rank"])
    mask_file=f"namespaces/base/methods/frontier-025-2026-09-10/science/results/F025-MASK-R{n}-001.json"
    inputs.path(mask_file)
    inputs.ref(mask_file,body={"mask":geometry["mask"],"closed_rows_mask":geometry["closed_rows_mask"]})
    G.CANONICAL=inputs.root/"namespaces/base"
    adapted,binding=normalize_geometry(geometry,unit,needs_dimension)
    checked=G.check(adapted,require_short_normals=short_normals,require_dimension=needs_dimension)
    binding.update(checked_chart_dimension_upper_bound=integer(geometry["degree_bound"]),actual_dimension_proved=needs_dimension,
                   true_interior_flags_claimed=needs_dimension,short_normal_bound_checked=short_normals)
    return checked if needs_dimension else None,binding


def multiply(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out


def interpolate(nodes,values,bound):
    nodes=[integer(t) for t in nodes]
    values=[rational(v) for v in values]
    need(len(nodes)==len(values)==integer(bound)+1 and len(set(nodes))==len(nodes),"Incomplete/duplicate determining nodes")
    result=[Q(0)]*len(nodes)
    for i,t in enumerate(nodes):
        basis,den=[Q(1)],Q(1)
        for j,u in enumerate(nodes):
            if i!=j:
                basis=multiply(basis,[-u,1])
                den*=t-u
        for k,coefficient in enumerate(basis):
            result[k]+=values[i]*coefficient/den
    need(all(evaluate(result,t)==v for t,v in zip(nodes,values)),"Independent interpolation identity failed")
    return result


def evaluate(coefficients,t):
    result=Q(0)
    for value in reversed(coefficients):
        result=result*t+value
    return result


def check_vector(nodes,values,bound,claimed,actual_degree,capture=None):
    coefficients=interpolate(nodes,values,bound)
    negative=[k for k,x in enumerate(coefficients) if x<0]
    if negative and capture is not None:
        capture({"kind":"complete_polynomial","coefficients":list(map(str,coefficients)),
                 "negative_indices":negative,"degree_upper_bound":bound,
                 "determining_nodes":nodes,"determining_values":list(map(str,values))})
    need(coefficients==[rational(x) for x in claimed],"Claimed coefficient vector differs from independent Lagrange reconstruction")
    degree=max((k for k,x in enumerate(coefficients) if x),default=-1)
    need(degree==integer(actual_degree),"Claimed actual polynomial degree differs")
    need(all(x>=0 for x in coefficients),"Negative ordinary coefficient in the bound recorded data")
    return coefficients


def expected_rows(geometry,grade,strict):
    rows=geometry["count_rows"]
    if strict:
        return [[integer(row[0])*grade-int(any(row[1:])),*[integer(a) for a in row[1:]]] for row in rows]
    return [[integer(a) for a in row] for row in rows]


def request_check(request,geometry,model,grade,strict,response,flags,*,legacy=False,closed_original=False,boundary=None,expected_id=None):
    grade=integer(grade)
    need(grade>=0 and (not strict or grade>0),"Invalid physical count grade")
    if strict:
        need(flags is not None,"True-interior request without a proved actual affine dimension")
    tokens=request.split()
    d,n=integer(geometry["degree_bound"]),integer(geometry["rank"])
    computational=1 if strict and model=="hive" else grade
    if legacy:
        need(tokens and tokens[0]=="1","Legacy input does not contain exactly one request")
        tokens=tokens[1:]
    request_id=response["id"] if response is not None else expected_id
    need(tokens and request_id is not None and tokens[0]==request_id,"Raw request/response ID mismatch")
    if response is not None:
        need(integer(response["t"])==computational,"Raw response physical grading mismatch")
    if model=="hive":
        rows=expected_rows(geometry,grade,strict)
        prefix=3 if legacy else 5
        need([integer(x) for x in tokens[1:3]]==[d,len(rows)],"H-system request dimension/row count mismatch")
        if not legacy:
            need(integer(tokens[3])==computational and rational(tokens[4])>0,"Wrong H-system computational grade")
        need([integer(x) for x in tokens[prefix:]]==[x for row in rows for x in row],"Raw hive request omits/changes full bound chart rows")
    else:
        if boundary is not None:
            n=max(len(p) for p in boundary)
            parts=[padded(p,n) for p in boundary]
        else:
            b=geometry["original"] if closed_original and not strict else geometry["count_boundary"]
            parts=[padded(b[k],n) for k in ("lambda","mu","nu")]
        prefix=2 if legacy else 4
        need(integer(tokens[1])==n,"Row-counter request rank mismatch")
        if not legacy:
            need(integer(tokens[2])==grade and rational(tokens[3])>0,"Row-counter request physical grade mismatch")
        flat=[x for part in parts for x in part]
        if strict:
            flat += [x for block in flags for row in block for x in row]
        elif not legacy:
            flat += [0]*(3*n*n)
        need([integer(x) for x in tokens[prefix:]]==flat,"Raw row request has a wrong triple or threshold array")


def modern_count(inputs,path,response,geometry,model,grade,strict,flags,*,boundary=None,allow_refused=False):
    refs=[]
    completed_values=set()
    refused=0
    for query,ref in inputs.queries(path,response):
        request_check(query["request"],geometry,model,grade,strict,query["response"],flags,boundary=boundary)
        if query["response"]["status"]=="complete":
            completed_values.add(integer(query["response"]["value"]))
        else:
            refused+=1
        refs.append(ref)
    need(len(completed_values)<=1,"Conflicting completed raw query retries")
    if response["status"]!="complete":
        need(allow_refused,"Uncompleted raw count used as numerical evidence")
        return None,{"status":"preserved_refusal","model":model,"grade":grade,"references":refs}
    value=integer(response["value"])
    need(value>=0,"Negative lattice count")
    return value,{"status":"complete","model":model,"grade":grade,"strict":strict,"value":str(value),
                 "references":refs,"preserved_refused_references":refused}


def legacy_count(inputs,prefix,site,geometry,model,flags,*,allow_refused=False):
    node=integer(site["signed_node"])
    grade=abs(node)
    path=f"{prefix}-n{node}"
    input_path=path+".input"
    response_path=path+".jsonl"
    input_raw=inputs.raw(input_path)
    input_ref=inputs.ref(input_path)
    if site["status"]!="complete":
        need(allow_refused,"Uncompleted U02 determining count")
        request_check(input_raw.decode(),geometry,model,grade,node<0,None,flags,legacy=True,closed_original=True,
                      expected_id=f"K{integer(geometry['id'])}")
        if "source_input_sha256" in site:
            need(site["source_input_sha256"]==digest(input_raw),"Refused U02 attempt has changed input bytes")
        refs=[input_ref]
        if inputs.has(response_path):
            refs.extend(ref for _,ref in inputs.records(response_path))
        return None,{"status":"preserved_refusal","model":model,"signed_node":node,"references":refs,
                    "request_geometry_checked":True,"counter_value_used":False,"recorded_status":site["status"]}
    rows=inputs.records(response_path)
    need(len(rows)==1,"Missing/duplicate U02 raw response")
    raw,raw_ref=rows[0]
    need(raw["status"]=="complete" and all(k in site and site[k]==v for k,v in raw.items()),"U02 recorded site differs from its full raw response")
    need(site["source_input_sha256"]==digest(input_raw),"U02 source input hash mismatch")
    need(integer(site["physical_grade"])==grade and integer(site["computational_grade"])==(1 if node<0 and model=="hive" else grade),"U02 signed/physical/computational grade mismatch")
    need(site["whole_count_kind"]==("true_relative_interior" if node<0 else "closed"),"U02 count kind changed")
    request_check(input_raw.decode(),geometry,model,grade,node<0,raw,flags,legacy=True,closed_original=True)
    count=integer(raw["value"])
    need(count>=0,"Negative recorded lattice count")
    value=count*((-1)**integer(geometry["degree_bound"]) if node<0 else 1)
    need(rational(site["polynomial_value"])==value,"U02 interior reciprocity sign mismatch")
    return value,{"status":"complete","model":model,"signed_node":node,"physical_grade":grade,"polynomial_value":str(value),"count":str(count),"references":[input_ref,raw_ref]}


def record_identity_u02(record,geometry,model,roster_sha):
    check_identity(record,geometry)
    need(record["model"]==model and integer(record["rank"])==integer(geometry["rank"]),"U02 model/rank identity mismatch")
    need(record["count_boundary_for_interiors"]==geometry["count_boundary"],"U02 interior boundary changed")
    need(integer(record["prior_degree_bound"])==integer(geometry["degree_bound"]) and record["roster_sha256"]==roster_sha,"U02 degree/roster source mismatch")
    need(record["actual_full_chart_dimension"]==geometry["interior_premises"]["actual_dimension"],"U02 sourced actual-dimension metadata changed")


def verify_u02(inputs,certificate,certificate_ref):
    idx=integer(certificate["id"])
    original,geometry_ref=inputs.get(relative("U02","DATA/U02/mixed-roster.json"),idx,"records")
    fresh_path=relative("U02","DATA/U02/mixed-freshholds-roster.json")
    geometry,fresh_ref=inputs.get(fresh_path,idx,"records")
    structural=("id","rank","original","raw_record","degree_bound","source_bound","count_boundary","count_preserving_word",
                "mask","closed_rows_mask","unit_eliminations","chart","translation","original_rhombus_rows","full_translated_rows",
                "count_rows","actual_dimension","row_chart","interior_premises")
    need(all(original.get(k)==geometry.get(k) for k in structural),"Fresh hold roster changed the original geometry")
    check_identity(certificate,geometry)
    nodes=[integer(t) for t in certificate["determining_nodes"]]
    holds=[integer(t) for t in certificate["holdout_nodes"]]
    need(nodes==geometry["mixed_nodes"] and holds==geometry["mixed_holdout_nodes"],"U02 literal determining/hold roster changed")
    need(len(holds)==2 and len(set(holds))==2 and all(t>0 and t not in nodes for t in holds),"U02 held grade reused or missing")
    need(not set(holds)&set(geometry["prior_successfully_evaluated_positive_grades"]),"U02 declared fresh hold was already a successful positive site")
    needs_dimension=original["interior_premises"].get("actual_dimension") is not None
    if any(t<0 for t in nodes) and not needs_dimension:
        raise SourceGap("Negative determining node has no sourced strict dimension witness")
    flags,geometry_check_result=geometry_check(inputs,original,"U02",needs_dimension,False)
    if needs_dimension:
        need(certificate["actual_dimension_witness"]==geometry["interior_premises"]["witness_grade"],"Selected strict witness grade changed")
    need(certificate["evidence_prefixes"]==[f"DATA/U02/mixed-{m}-det/{idx}" for m in ("hive","rows")],"U02 determining prefix roster changed")
    paired_values=[]
    bindings=[]
    held_counts={}
    d=integer(geometry["degree_bound"])
    for model,prefix0 in zip(("hive","rows"),certificate["evidence_prefixes"]):
        prefix=relative("U02",prefix0)
        record=inputs.json(prefix+".record.json")
        vector=inputs.json(prefix+".vector.json")
        inputs.ref(prefix+".record.json",body=record)
        inputs.ref(prefix+".vector.json",body=vector)
        record_identity_u02(record,geometry,model,inputs.used[fresh_path]["sha256"])
        record_identity_u02(vector,geometry,model,inputs.used[fresh_path]["sha256"])
        need(record["mode"]==vector["mode"]=="determine" and record["status"]=="complete", "U02 determining record is not complete")
        need([s["signed_node"] for s in record["site_results"]]==nodes and vector["site_results"]==record["site_results"],"U02 determining site identities changed")
        values=[]
        for site in record["site_results"]:
            value,binding=legacy_count(inputs,prefix,site,geometry,model,flags)
            values.append(value)
            bindings.append(binding)
        need(vector["nodes"]==nodes and [rational(x) for x in vector["values"]]==values and vector["unused_positive_holdout_nodes"]==holds,"U02 frozen vector/node/hold binding changed")
        if vector["empty_polynomial"]:
            raise SourceGap("Empty-polynomial scalar-zero convention requires a separate positive-node determination")
        coefficients=check_vector(nodes,values,d,vector["coefficients"],certificate["actual_degree"],inputs.capture_candidate)
        if needs_dimension:
            need(integer(certificate["actual_degree"])==d and coefficients[d]>0,"Recorded polynomial degree contradicts the independently proved actual dimension")
        need(coefficients==[rational(x) for x in certificate["coefficients"]],"Final U02 vector differs from a paired determining vector")
        paired_values.append(values)
        base=relative("U02",f"DATA/U02/mixed-{model}-holds/{idx}.record.json")
        need(inputs.has(base),"Missing original U02 hold attempt")
        pattern=re.compile(r"namespaces/u02/DATA/U02/mixed-"+model+r"-holds(?:-[a-z0-9_-]+)?/"+str(idx)+r"\.record\.json\Z")
        attempts=sorted((path for path in inputs.expected if pattern.fullmatch(path)),key=lambda path:(path!=base,path))
        successful={}
        for path in attempts:
            record=inputs.json(path)
            record_identity_u02(record,geometry,model,inputs.used[fresh_path]["sha256"])
            need(record["mode"]=="hold", "U02 hold record has a different role")
            inputs.ref(path,body=record)
            sites=record["site_results"]
            need([s["signed_node"] for s in sites]==holds[:len(sites)] and len(sites)<=len(holds),"U02 hold attempt duplicated/changed its ordered sites")
            for site in sites:
                value,binding=legacy_count(inputs,path[:-len(".record.json")],site,geometry,model,flags,allow_refused=True)
                bindings.append(binding)
                if value is not None:
                    t=integer(site["signed_node"])
                    need(t not in successful or successful[t]==value,"Conflicting U02 hold retries")
                    need(evaluate(coefficients,t)==value,"Unused U02 positive hold does not match the reconstructed polynomial")
                    successful[t]=value
        if set(successful)!=set(holds):
            raise SourceGap("No complete bound raw count for every U02 unused hold grade/model")
        held_counts[model]=[successful[t] for t in holds]
    need(paired_values[0]==paired_values[1]==[rational(x) for x in certificate["determining_values"]],"Paired/final U02 determining values differ")
    need(held_counts["hive"]==held_counts["rows"] and [held_counts[m] for m in ("hive","rows")]==[[integer(x) for x in v] for v in certificate["hold_values"]],"Paired/final U02 hold counts differ")
    return {"id":idx,"unit":"U02","kind":"FULL_VECTOR","certificate":certificate_ref,"geometry_sources":[geometry_ref,fresh_ref],
            "geometry_check":geometry_check_result,"coefficients":list(map(str,coefficients)),"actual_degree":certificate["actual_degree"],
            "determining_nodes":nodes,"unused_hold_nodes":holds,"count_bindings":bindings}


def four_count_algebra(values,claimed_d1=None,claimed_d2=None,capture=None):
    A,B,U,V=[integer(x) for x in values]
    need(all(x>=0 for x in (A,B,U,V)) and A>0,"Invalid/nonpositive closed four-count reference")
    # Derive the functionals from their evaluation vectors in degree at most 5.
    first=[8*(1**k-(-1)**k)-(2**k-(-2)**k) for k in range(6)]
    second=[16*(1**k+(-1)**k)-(2**k+(-2)**k) for k in range(6)]
    need(first==[0,12,0,0,0,-48] and second==[30,0,24,0,0,0],"Four-count polynomial identity derivation failed")
    D1,D2=8*(A+U)-B-V,16*(A-U)-B+V-30
    if D2<0 and capture is not None:
        capture({"kind":"exact_ordinary_coefficient","index":2,"value":str(Q(D2,24)),
                 "four_counts_P1_P2_I1_I2":[A,B,U,V],"actual_degree":5,
                 "identity":"24*c2 = 16*(P1-I1)-P2+I2-30"})
    if claimed_d1 is not None:
        need(D1==integer(claimed_d1) and D2==integer(claimed_d2),"Claimed D1/D2 changed")
    need(D1>=0 and D2>=0,"Four-count sufficient sign criterion did not pass")
    return {"D1":D1,"D2":D2,"c2":str(Q(D2,24)),"c1_identity":"D1/12 + 4*c5",
            "protected_positive_coefficients":[3,4,5],"top_three_short_normal_premise_required":True,
            "full_coefficient_vector_inferred":False}


def trim(p):
    p=tuple(integer(x) for x in p)
    while p and p[-1]==0:
        p=p[:-1]
    return p


def canonical(parts):
    parts=tuple(map(trim,parts))
    g=gcd(*(x for p in parts for x in p)) or 1
    a,b,c=(tuple(x//g for x in p) for p in parts)
    return (a,*sorted((b,c))),g


def gap_transport(original,repair):
    current,scale=canonical([original[k] for k in ("lambda","mu","nu")])
    def score(t):
        return sum(t[0]),max(map(len,t)),t
    for step in repair["proof_trace"]:
        n=integer(step["padding"])
        need(max(map(len,current))<=n<=7 and type(step["dual"]) is int and step["dual"] in (0,1)
             and integer(step["outer"]) in (0,1,2) and type(step["swap"]) is int and step["swap"] in (0,1)
             and type(step["clip"]) is bool,"Illegal gap/tensor word")
        parts=[padded(p,n) for p in current]
        star=lambda p:tuple(-x for x in reversed(p))
        weights=[tuple(parts[1]),tuple(parts[2]),star(parts[0])]
        if step["dual"]:
            weights=list(map(star,weights))
        other=[i for i in range(3) if i!=step["outer"]]
        if step["swap"]:
            other.reverse()
        outer,first,second=star(weights[step["outer"]]),weights[other[0]],weights[other[1]]
        a,b=first[-1],second[-1]
        image=tuple(map(trim,([x-a-b for x in outer],[x-a for x in first],[x-b for x in second])))
        need(all(p==tuple(sorted(p,reverse=True)) and all(x>=0 for x in p) for p in image)
             and sum(image[0])==sum(image[1])+sum(image[2]),"Invalid tensor target partitions")
        need(all(len(p)<=len(image[0]) and all(x<=image[0][j] for j,x in enumerate(p)) for p in image[1:]),"Noncontained gap target")
        if step["clip"]:
            outer,first,content=image
            first=first+(0,)*(len(outer)-len(first))
            rows=[(l-m,m) for l,m in zip(outer,first) if l!=m]
            shifted=[0]*len(rows)
            for j in range(len(rows)-2,-1,-1):
                shifted[j]=shifted[j+1]+min(rows[j][1]-rows[j+1][1],rows[j+1][0])
            image=(tuple(x+s for (x,_),s in zip(rows,shifted)),trim(shifted),content)
        image,g=canonical(image)
        need(all(p==tuple(sorted(p,reverse=True)) and all(x>=0 for x in p) for p in image)
             and sum(image[0])==sum(image[1])+sum(image[2]),"Gap clipping changed partition legality or balance")
        need(g==integer(step["gcd"]) and image==tuple(map(trim,step["target"])) and score(image)<score(current),"Gap repair target/scale/decrease mismatch")
        current,scale=image,scale*g
    need(current==tuple(map(trim,repair["target"])) and scale==integer(repair["scale"])>0,"Final whole-count gap transport changed")
    return current,scale


def verify_u03(inputs,certificate,certificate_ref):
    idx=integer(certificate["id"])
    geometry_path=relative("U03",certificate["geometry_file"])
    geometry,geometry_ref=inputs.get(geometry_path,idx)
    need(geometry_ref["record_sha256"]==certificate["geometry_line_sha256"],"U03 geometry source-line hash mismatch")
    check_identity(certificate,geometry)
    need(certificate["tensor_word"]==geometry["count_preserving_word"] and integer(certificate["degree_upper_bound"])==5==integer(geometry["degree_bound"]),"U03 tensor/upper-degree binding changed")
    bindings=[]
    if certificate["status"]=="TWO_MODEL_FOUR_COUNT_POSITIVE":
        flags,geometry_result=geometry_check(inputs,geometry,"U03",True,True)
        need(integer(certificate["actual_degree"])==5 and certificate["full_coefficient_vector_computed"] is False,"Wrong four-count certificate scope")
        paired=[]
        for model in ("hive","rows"):
            directory=f"DATA/U03/direct-hash-{model}-warm"
            decision,ref=inputs.get(relative("U03",directory+"/decisions.jsonl"),idx)
            check_identity(decision,geometry)
            need(decision["geometry_file"]==certificate["geometry_file"] and decision["geometry_line_sha256"]==certificate["geometry_line_sha256"]
                 and integer(decision["actual_dimension"])==5,"Four-count decision geometry changed")
            expected=[("P1",1,False),("P2",2,False),("I1",1,True),("I2",2,True)]
            need([(s["kind"],integer(s["physical_grade"])) for s in decision["sites"]]==[(k,t) for k,t,_ in expected],"Four-count site roster changed")
            values=[]
            for site,(kind,t,strict) in zip(decision["sites"],expected):
                value,binding=modern_count(inputs,relative("U03",directory+"/queries.jsonl"),site["record"],geometry,model,t,strict,flags)
                need(site["record"]["id"]==f"K{idx}_{kind}","Four-count query ID changed")
                values.append(value)
                bindings.append(binding)
            need(values==[integer(decision[k]) for k in ("A","B","U","V")],"Four-count decision values changed")
            four_count_algebra(values,decision["D1"],decision["D2"],inputs.capture_candidate)
            paired.append(values)
        need(paired[0]==paired[1]==[integer(certificate["counts"][k]) for k in ("P1","P2","I1","I2")],"Paired/final four-count values differ")
        algebra=four_count_algebra(paired[0],certificate["D1"],certificate["D2"],inputs.capture_candidate)
        return {"id":idx,"unit":"U03","kind":"FOUR_COUNT","certificate":certificate_ref,"geometry_source":geometry_ref,
                "geometry_check":geometry_result,"algebra":algebra,"count_bindings":bindings}
    need(certificate["status"]=="TWO_MODEL_FULL_VECTOR_POSITIVE" and certificate["full_coefficient_vector_computed"] is True,"Unknown U03 numeric certificate kind")
    _,geometry_result=geometry_check(inputs,geometry,"U03",False,False)
    nodes=[integer(t) for t in certificate["determining_sites"]]
    need(nodes==list(range(6)),"Quartic fallback must determine in the full degree-at-most-five space")
    paired=[]
    models={h["model"]:h for h in certificate["holdouts"]}
    need(len(certificate["holdouts"])==len(models)==2 and set(models)=={"hive","rows"},"Missing/duplicate fallback hold model")
    for model in ("hive","rows"):
        directory=f"DATA/U03/fallback-{model}-determine"
        record,record_ref=inputs.get(relative("U03",directory+"/records.jsonl"),idx)
        check_identity(record,geometry)
        need(record["model"]==model and record["geometry_line_sha256"]==geometry_ref["record_sha256"] and record["geometry_file"]==certificate["geometry_file"],"Fallback determining geometry/model changed")
        need([integer(s["t"]) for s in record["sites"]]==nodes,"Fallback determining site roster changed")
        values=[]
        for t,site in zip(nodes,record["sites"]):
            need(site["id"]==f"F{idx}_T{t}","Fallback determining query ID changed")
            value,binding=modern_count(inputs,relative("U03",directory+"/queries.jsonl"),site,geometry,model,t,False,None)
            values.append(value)
            bindings.append(binding)
        need(values==[integer(x) for x in record["values"]],"Fallback determining value list changed")
        coefficients=check_vector(nodes,values,5,record["coefficients"],record["actual_degree"],inputs.capture_candidate)
        need(coefficients==[rational(x) for x in certificate["coefficients"]] and integer(certificate["actual_degree"])==4,"Final quartic vector/degree changed")
        paired.append(values)
        hold_directory=f"DATA/U03/fallback-{model}-holdouts"
        held,held_ref=inputs.get(relative("U03",hold_directory+"/records.jsonl"),idx)
        check_identity(held,geometry)
        need(held["model"]==model and held["geometry_line_sha256"]==geometry_ref["record_sha256"] and held["geometry_file"]==certificate["geometry_file"],"Fallback hold geometry/model changed")
        vector_path=relative("U03",directory+f"/vectors/{idx}.json")
        vector=inputs.json(vector_path)
        inputs.ref(vector_path,body=vector)
        need(digest(inputs.raw(vector_path))==held["determining_sha256"],"Held source does not bind its frozen determining vector")
        need(vector==record,"Frozen per-ID vector differs from its determining record")
        holds=[integer(t) for t in models[model]["physical_sites"]]
        need(len(holds)==len(set(holds))==2 and all(t>0 and t not in nodes for t in holds),"Fallback hold reused a determining node")
        need(len(held["sites"])<=len(holds) and [integer(s["t"]) for s in held["sites"]]==holds[:len(held["sites"])],
             "Original fallback hold attempt is not a literal prefix of its declared roster")
        successful={}
        for t,site in zip(holds,held["sites"]):
            value,binding=modern_count(inputs,relative("U03",hold_directory+"/queries.jsonl"),site,geometry,model,t,False,None,allow_refused=True)
            bindings.append(binding)
            if value is not None:
                need(evaluate(coefficients,t)==value,"Unused original fallback hold failed")
                successful[t]=value
        repaired=models[model]["gap_identity_used"]
        need(type(repaired) is bool,"Invalid gap-repair flag")
        if repaired:
            need(model=="rows","Unexpected repaired model")
            repair,repair_ref=inputs.get(relative("U03","DATA/U03/fallback-rows-gap-repair/records.json"),idx,"$")
            target,scale=gap_transport(geometry["original"],repair)
            need(repair["positive_holdouts"]==holds and len(repair["sites"])==len(holds),"Gap-repair held roster changed")
            for t,site in zip(holds,repair["sites"]):
                need(site["id"]==f"G{idx}_{t}","Gap-repair query identity changed")
                value,binding=modern_count(inputs,relative("U03","DATA/U03/fallback-rows-gap-repair/queries.jsonl"),site,geometry,model,t*scale,False,None,boundary=target)
                need(t not in successful or successful[t]==value,"Conflicting completed fallback hold retry")
                need(evaluate(coefficients,t)==value,"Gap-repaired whole-count hold failed")
                binding.update(original_physical_grade=t,whole_count_scale=scale,transport_source=repair_ref)
                bindings.append(binding)
                successful[t]=value
        if set(successful)!=set(holds):
            raise SourceGap("Fallback model still lacks a complete unused hold")
        need([successful[t] for t in holds]==[integer(x) for x in models[model]["values"]],"Final fallback held values differ")
    need(paired[0]==paired[1]==[integer(x) for x in certificate["determining_values"]],"Paired/final quartic determining values differ")
    return {"id":idx,"unit":"U03","kind":"FULL_VECTOR","certificate":certificate_ref,"geometry_source":geometry_ref,
            "geometry_check":geometry_result,"coefficients":list(map(str,coefficients)),"actual_degree":4,
            "determining_nodes":nodes,"holdouts":certificate["holdouts"],"count_bindings":bindings}


def select_required(rows,unit,path=None,expected_sha=None):
    if path is None:
        return rows,None
    source=Path(path).resolve()
    source_pin=pin(source)
    need(SHA.fullmatch(expected_sha or "") and source_pin["sha256"]==expected_sha,"Required-ID selection must have its exact declared SHA-256")
    raw=source.read_bytes()
    need(digest(raw)==expected_sha,"Required-ID selection changed before parsing")
    document=json_data(raw)
    if isinstance(document,list):
        ids=[integer(x) for x in document]
    elif document.get("schema")=="finite-box-chosen-terminal-sources-v1":
        key="chosen_u02_numeric_ids" if unit=="U02" else "source_order_early_u03_numeric_ids"
        ids=[integer(x) for x in document[key]]
    else:
        need(document.get("schema")=="early-required-ids-v1" and document["unit"]==unit,"Unknown required-ID selection schema")
        ids=[integer(x) for x in document["ids"]]
    need(ids and len(set(ids))==len(ids),"Missing/duplicate required terminal IDs")
    available={integer(record["id"]) for record,_ in rows}
    need(set(ids)<=available,"Required terminal ID is outside the advertised source roster")
    # Preserve the certificate's stable physical order for resumable slices.
    wanted=set(ids)
    return [(record,ref) for record,ref in rows if integer(record["id"]) in wanted],{
        "path":str(source),**source_pin,"required_ids":ids,"scope":"Exact selection metadata only; transport and sign acceptance are separate"}


def run(args):
    inputs=Inputs(args.root,args.source_manifest,args.source_manifest_sha256)
    unit=args.unit
    path,population=ROSTERS[unit]
    rows=inputs.records(relative(unit,path),"records" if unit=="U02" else None)
    advertised_ids=[integer(row["id"]) for row,_ in rows]
    need(len(advertised_ids)==population and len(set(advertised_ids))==population,"Missing/duplicate full early-terminal roster identities")
    rows,selection=select_required(rows,unit,args.required_ids,args.required_ids_sha256)
    ids=[integer(row["id"]) for row,_ in rows]
    need(0<=args.start<args.stop<=len(ids),"Invalid or empty exact slice")
    output=Path(args.output)
    need(not output.resolve().is_relative_to(Path(args.root).resolve()),"Never write into the restored input root")
    ledger=output.with_suffix(".identities.jsonl")
    inputs.candidate_path=output.with_suffix(".candidate.json")
    need(not output.exists() and not ledger.exists() and output.parent.is_dir(),"Outputs must be fresh with an existing parent")
    source_pins={str(Path(__file__).resolve()):pin(Path(__file__)),str(Path(G.__file__).resolve()):pin(Path(G.__file__))}
    G.accepted_masks.cache_clear()
    G.linear_template.cache_clear()
    checked=[]
    counts=Counter()
    result={"schema":SCHEMA,"status":"PARTIAL","unit":unit,"slice":[args.start,args.stop],"expected_ids":ids,
            "advertised_ids":advertised_ids,"required_id_selection":selection,
            "source_manifest":{"path":str(inputs.manifest),**inputs.manifest_pin},"code_sources":source_pins,
            "copied_geometry_source_sha256":G.COPIED_SOURCE_SHA256,"checked_ids":checked,
            "separate_premises":PREMISES,"new_numerical_recounts":0,"returned_code_executed":False}
    try:
        with ledger.open("xb") as stream:
            for ordinal in range(args.start,args.stop):
                certificate,reference=rows[ordinal]
                idx=ids[ordinal]
                inputs.candidate_context={"id":idx,"unit":unit,"bare_triple":certificate['bare_triple'],
                                          "certificate_source":reference}
                start_ref=len(inputs.references)
                try:
                    record=verify_u02(inputs,certificate,reference) if unit=="U02" else verify_u03(inputs,certificate,reference)
                except (ValueError,KeyError,IndexError,TypeError,FileNotFoundError) as error:
                    failure={"id":idx,"unit":unit,"ordinal":ordinal,"status":"HOLD_CANDIDATE" if isinstance(error,CandidateObservation) else "CANNOT_CHECK" if isinstance(error,(SourceGap,FileNotFoundError)) else "FAIL",
                             "error":f"{type(error).__name__}: {error}","source_references":inputs.references[start_ref:]}
                    stream.write(encoded(failure)+b"\n")
                    stream.flush()
                    result.update(status=failure["status"],failure=failure)
                    break
                record.update(ordinal=ordinal,status="PASS_CONDITIONAL_ON_RECORDED_COUNTS",source_references=inputs.references[start_ref:])
                stream.write(encoded(record)+b"\n")
                stream.flush()
                checked.append(idx)
                counts[record["kind"]]+=1
            else:
                result["status"]="PASS_CONDITIONAL_ON_RECORDED_COUNTS"
        inputs.finish()
        if selection is not None:
            need(pin(Path(selection["path"]))=={k:selection[k] for k in ("bytes","sha256")},"Required-ID selection changed during verification")
        for name,binding in source_pins.items():
            need(pin(Path(name))==binding,"Checker source changed during verification")
    except (Exception,KeyboardInterrupt) as error:
        result.update(status="CANNOT_CHECK" if isinstance(error,(SourceGap,FileNotFoundError,KeyboardInterrupt)) else "FAIL",
                      error=f"{type(error).__name__}: {error}")
    finally:
        result.update(pending_slice_ids=[idx for idx in ids[args.start:args.stop] if idx not in checked],counts=dict(counts),
                      accessed_sources=inputs.used)
        if ledger.exists():
            result["identities"]={"path":str(ledger.resolve()),**pin(ledger)}
        with output.open("x",encoding="utf-8") as stream:
            json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
            stream.write("\n")
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root",required=True,type=Path)
    parser.add_argument("--unit",required=True,choices=ROSTERS)
    parser.add_argument("--source-manifest",required=True,type=Path)
    parser.add_argument("--source-manifest-sha256",required=True)
    parser.add_argument("--start",required=True,type=int)
    parser.add_argument("--stop",required=True,type=int)
    parser.add_argument("--output",required=True,type=Path)
    parser.add_argument("--required-ids",type=Path)
    parser.add_argument("--required-ids-sha256")
    parser.add_argument("--max-seconds",type=float,default=100)
    args=parser.parse_args()
    started=time.monotonic()
    def expired(_signal,_frame):
        raise SourceGap("Declared verification time budget exhausted")
    try:
        need(0<args.max_seconds<=110,"Invalid bounded verification budget")
        signal.signal(signal.SIGALRM,expired)
        signal.setitimer(signal.ITIMER_REAL,args.max_seconds)
        result=run(args)
        print(json.dumps({"status":result["status"],"unit":args.unit,"checked":len(result["checked_ids"]),"output":str(args.output),"elapsed_seconds":time.monotonic()-started}))
        return 0 if result["status"]=="PASS_CONDITIONAL_ON_RECORDED_COUNTS" else 1
    except Exception as error:
        failure={"schema":SCHEMA,"status":"CANNOT_CHECK" if isinstance(error,(SourceGap,FileNotFoundError)) else "FAIL",
                 "error":f"{type(error).__name__}: {error}","elapsed_seconds":time.monotonic()-started,"new_numerical_recounts":0}
        if not args.output.exists() and args.output.parent.is_dir() and not args.output.resolve().is_relative_to(args.root.resolve()):
            args.output.write_text(json.dumps(failure,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(failure))
        return 1
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)


if __name__=="__main__":
    raise SystemExit(main())
