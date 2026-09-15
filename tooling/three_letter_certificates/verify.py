#!/usr/bin/env python3
"""Reproduce the entire finite certificate in a fresh standalone directory."""
import argparse
import csv
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import sys
import time

from runner import Runner,Refused,Stopped,digest,save,publish_json,handle_outer_signals,STOP_SIGNALS
import model

PACKAGE=Path(__file__).resolve().parent
TYPE_COUNTS=(9,129,1464,12288,74306,307461)
SUBSET_COUNTS=(32,496,4960,35960,201376,906192)
INDEPENDENT_COUNTS=(32,486,4622,30495,144914,484508)
FIELD_ROWS={3:4622,4:30495,5:144914,6:484508}
EPSILON=Fraction(1,100000000)


def code_sources():
    paths=sorted(PACKAGE.glob("*.py"))+sorted((PACKAGE/"src").glob("*.cpp"))+[PACKAGE/"data/manifest.json"]
    return {str(path):digest(path) for path in paths}


def unpack(output,runner):
    manifest=json.loads((PACKAGE/"data/manifest.json").read_text())
    if (manifest.get("schema")!="three-letter-lr-certificate/v1" or manifest.get("ambient_dimension")!=7
        or manifest.get("distinct_normals")!=32 or manifest.get("subsets")!=list(SUBSET_COUNTS)
        or manifest.get("types")!=list(TYPE_COUNTS) or manifest.get("independent_subsets")!=list(INDEPENDENT_COUNTS)
        or manifest.get("fields")!=[3,4,5,6] or Fraction(manifest.get("epsilon","0"))!=EPSILON):
        raise Refused("Mathematical manifest boundary mismatch")
    expected={"normals.txt"}|{f"q{q}.{suffix}" for q in range(1,7) for suffix in ("roster.tsv","keys.tsv","types.txt","expected.tsv")}|{f"field-q{q}.json" for q in range(3,7)}
    if len(manifest["files"])!=len(expected) or {row["name"] for row in manifest["files"]}!=expected:
        raise Refused("Incomplete or duplicate mathematical payload roster")
    data=output/"data";data.mkdir()
    for row in manifest["files"]:
        name=row["name"]
        if Path(name).name!=name or row["archive"]!=name+".gz":raise Refused("Unsafe mathematical payload name")
        archive=PACKAGE/"data"/row["archive"]
        if digest(archive)!=row["sha256"]:raise Refused("Compressed mathematical payload digest mismatch: "+name)
        runner.bind(archive)
        with gzip.open(archive,"rb") as source:content=source.read(row["uncompressed_bytes"]+1)
        if len(content)!=row["uncompressed_bytes"] or hashlib.sha256(content).hexdigest()!=row["uncompressed_sha256"]:
            raise Refused("Decompressed mathematical payload digest mismatch: "+name)
        with (data/name).open("xb") as stream:stream.write(content)
        runner.bind(data/name)
    tokens=list(map(int,(data/"normals.txt").read_text().split()))
    reconstructed=model.normal_roster()
    normals=[row["normal"] for row in reconstructed["normals"]]
    actual=[tokens[2+7*i:2+7*(i+1)] for i in range(32)]
    if tokens[:2]!=[32,7] or len(tokens)!=226 or actual!=[list(row) for row in normals] or reconstructed["original_row_count"]!=42 or len(reconstructed["zero_rows"])!=7:
        raise Refused("Original complete model/normal reconstruction failed")
    save(output/"MODEL-NORMALS.json",reconstructed)
    return data


def compiler_flags(prefix):
    if prefix is not None:
        prefix=prefix.resolve()
        if not (prefix/"include/gmpxx.h").is_file():raise Refused("Requested GMP prefix has no gmpxx.h")
        return ["-isystem",str(prefix/"include"),"-L"+str(prefix/"lib"),"-Wl,-rpath,"+str(prefix/"lib")]
    for candidate in (Path("/opt/homebrew"),Path("/usr/local")):
        if (candidate/"include/gmpxx.h").is_file():return compiler_flags(candidate)
    return []


def compile_programs(output,runner,cxx,gmp_prefix):
    executable=shutil.which(cxx)
    if not executable:raise Refused("A C++17 compiler is required")
    executable=str(Path(executable).resolve());runner.bind(executable)
    build=output/"build";build.mkdir()
    type_check=build/"type_check";bv=build/"bv"
    runner.run("compile-types",[executable,"-std=c++17","-O2","-Wall","-Wextra",str(PACKAGE/"src/type_check.cpp"),"-o",str(type_check)])
    runner.bind(type_check)
    runner.run("compile-bv",[executable,"-std=c++17","-O2","-Wall","-Wextra",*compiler_flags(gmp_prefix),str(PACKAGE/"src/bv.cpp"),"-lgmpxx","-lgmp","-o",str(bv)])
    runner.bind(bv)
    return type_check,bv


def exact_expected(path,total):
    values=[]
    with path.open() as stream:
        reader=csv.DictReader(stream,delimiter="\t")
        if reader.fieldnames!=["type_id","alpha"]:raise Refused("Expected-value schema mismatch")
        for row in reader:
            if int(row["type_id"])!=len(values):raise Refused("Missing, duplicate or reordered expected type")
            values.append(Fraction(row["alpha"]))
    if len(values)!=total:raise Refused("Expected-value population mismatch")
    return values


def reproduce(output,runner,cxx,gmp_prefix):
    data=unpack(output,runner);type_check,bv=compile_programs(output,runner,cxx,gmp_prefix)
    types=output/"types";types.mkdir();type_results=[]
    runner.run("arithmetic-controls",[str(type_check),"--self-test"])
    for q,total in enumerate(SUBSET_COUNTS,1):
        record=runner.run(f"types-q{q}",[str(type_check),str(data/"normals.txt"),str(q),str(data/f"q{q}.roster.tsv"),str(data/f"q{q}.keys.tsv"),str(data/f"q{q}.types.txt"),str(types/f"q{q}"),str(total)])
        result=json.loads(record["stdout"].splitlines()[-1])
        if (result.get("status")!="PASS" or result.get("q")!=q or result.get("total")!=total
            or result.get("independent")!=INDEPENDENT_COUNTS[q-1] or result.get("types")!=TYPE_COUNTS[q-1]):
            raise Refused("Complete original type population not verified")
        type_results.append(result)
        runner.bind(types/f"q{q}.verified.tsv");runner.bind(types/f"q{q}.types-verified.tsv")
        print(json.dumps({"phase":"types","q":q,"subsets":total}),flush=True)
    cache=output/"cache.bin"
    runner.run("prepare-cache",[str(bv),"prepare",str(data),str(types),str(cache)])
    runner.bind(cache)
    values=output/"values";values.mkdir();slices=output/"slices";slices.mkdir();value_results=[]
    for q,total in enumerate(TYPE_COUNTS,1):
        expected=exact_expected(data/f"q{q}.expected.tsv",total);actual=[];maximum_numerator=0;proper_faces=0
        for start in range(0,total,10000):
            stop=min(start+10000,total);label=f"values-q{q}-{start}-{stop}";prefix=slices/label
            record=runner.run(label,[str(bv),"evaluate",str(data),str(cache),str(q),str(start),str(stop),str(prefix),"2","none"],category="native",timeout=60)
            result=json.loads(record["stdout"])
            if (result.get("status")!="COMPLETE" or result.get("q")!=q or result.get("start")!=start or result.get("stop")!=stop
                or result.get("types")!=stop-start or result.get("nonzero_pole_rows")!=0 or result.get("mutation")!="none"
                or result.get("proper_face_terms")!=(stop-start)*(3**q-2**q)):
                raise Refused("Incomplete proper-face recurrence or value population")
            seen=0
            with Path(str(prefix)+".values.tsv").open() as stream:
                for row in csv.DictReader(stream,delimiter="\t"):
                    tid=int(row["type_id"])
                    if tid!=start+seen:raise Refused("Missing, duplicate or reordered independent value")
                    alpha=Fraction(row["alpha"])
                    if alpha!=expected[tid]:raise Refused("Independent recurrence value mismatch at q="+str(q)+", type="+str(tid))
                    poles=row["poles"].rstrip(",").split(",")
                    if len(poles)!=q or any(Fraction(value)!=0 for value in poles):raise Refused("Uncancelled independent recurrence pole")
                    actual.append(alpha);seen+=1
            if seen!=stop-start:raise Refused("Independent value slice truncated")
            maximum_numerator=max(maximum_numerator,result["maximum_full_numerator"]);proper_faces+=result["proper_face_terms"]
            print(json.dumps({"phase":"values","q":q,"verified_types":stop,"required_types":total}),flush=True)
        if len(actual)!=total:raise Refused("Complete independent value population missing")
        if q<=2 and any(value<EPSILON for value in actual):raise Refused("Uncorrected q1/q2 coefficient margin fails")
        path=values/f"q{q}.values.tsv"
        with path.open("x") as stream:
            stream.write("type_id\talpha\n")
            for tid,value in enumerate(actual):stream.write(f"{tid}\t{value}\n")
        runner.bind(path)
        value_results.append({"q":q,"types":total,"minimum":str(min(actual)),"negative":sum(x<0 for x in actual),"zero":sum(x==0 for x in actual),"maximum_numerator":maximum_numerator,"proper_face_terms":proper_faces})
    field_results=[]
    for q in (3,4,5,6):
        path=output/f"field-q{q}.json"
        runner.run(f"field-q{q}",[str(Path(sys.executable).resolve()),str(PACKAGE/"field_check.py"),str(data),str(types),str(values),str(q),str(path)])
        result=json.loads(path.read_text())
        if (result.get("status")!="PASS" or result.get("q")!=q or result.get("rows")!=FIELD_ROWS[q]
            or result.get("full_original_supports")!=INDEPENDENT_COUNTS[q-2] or result.get("below_epsilon")!=0
            or Fraction(result["minimum_beta"])<EPSILON):
            raise Refused("Complete original field population or exact margin failed")
        field_results.append(result)
        print(json.dumps({"phase":"field","q":q,"rows":result["rows"],"minimum_beta":result["minimum_beta"]}),flush=True)
    if not runner.intact():raise Refused("Source or mathematical input changed during verification")
    artifacts={str(path.relative_to(output)):digest(path) for path in output.rglob("*") if path.is_file() and "tmp" not in path.relative_to(output).parts}
    report={"schema":"three-letter-lr-complete/v1","status":"PASS","original_subsets":sum(row["total"] for row in type_results),
            "independent_subsets":sum(row["independent"] for row in type_results),"dependent_subsets":sum(row["dependent"] for row in type_results),
            "types_reproduced":sum(row["types"] for row in value_results),"field_rows":sum(row["rows"] for row in field_results),
            "epsilon":str(EPSILON),"type_results":type_results,"value_results":value_results,"field_results":field_results,
            "source_sha256":runner.sources,"artifact_sha256":artifacts,"resource_seconds":runner.used,
            "all_owned_child_cleanup_verified":all(row["cleanup_verified"] for row in runner.receipts),"bare_LR_values":0,
            "mathematical_implication":"See PROOF.md and MODEL.md; numerical completion does not replace their analytic hypotheses."}
    if report["original_subsets"]!=1149016 or report["types_reproduced"]!=395657 or report["field_rows"]!=664539:
        raise Refused("Final complete population sentinel refused")
    publish_json(output/"COMPLETE.json",report)
    return report


def completion_published(output):
    """Recognize a complete serialized record without replaying its mathematics."""
    try:
        record=json.loads((output/"COMPLETE.json").read_text())
    except (OSError,ValueError,TypeError):
        return False
    if not isinstance(record,dict):return False
    expected={"schema":"three-letter-lr-complete/v1","status":"PASS",
              "original_subsets":sum(SUBSET_COUNTS),"independent_subsets":sum(INDEPENDENT_COUNTS),
              "dependent_subsets":sum(SUBSET_COUNTS)-sum(INDEPENDENT_COUNTS),
              "types_reproduced":sum(TYPE_COUNTS),"field_rows":sum(FIELD_ROWS.values()),
              "epsilon":str(EPSILON),"bare_LR_values":0}
    if any(record.get(key)!=value for key,value in expected.items()):return False
    if record.get("all_owned_child_cleanup_verified") is not True:return False
    for name,orders in (("type_results",list(range(1,7))),("value_results",list(range(1,7))),("field_results",[3,4,5,6])):
        rows=record.get(name)
        if not isinstance(rows,list) or [row.get("q") if isinstance(row,dict) else None for row in rows]!=orders:return False
    return all(isinstance(record.get(name),dict) and record[name] for name in ("source_sha256","artifact_sha256"))


def record_abort(output,record):
    """An invalid or truncated completion pathname cannot suppress abort evidence."""
    previous=signal.pthread_sigmask(signal.SIG_BLOCK,set(STOP_SIGNALS))
    try:
        if not completion_published(output) and not os.path.lexists(output/"ABORTED.json"):
            try:publish_json(output/"ABORTED.json",record)
            except (OSError,ValueError,TypeError) as error:
                print("ABORT record could not be published: "+str(error),file=sys.stderr)
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK,previous)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("command",choices=("full","_interrupt-probe","_timeout-probe","_budget-probe"))
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--native-seconds",type=float,default=600)
    parser.add_argument("--program-seconds",type=float,default=900)
    parser.add_argument("--cxx",default="c++")
    parser.add_argument("--gmp-prefix",type=Path)
    args=parser.parse_args();output=args.output.resolve();runner=None;started=time.monotonic();owns_output=False
    try:
        with handle_outer_signals():
            output.mkdir(exist_ok=False)
            owns_output=True
            runner=Runner(output,code_sources(),native_limit=args.native_seconds,program_limit=args.program_seconds)
            if args.command=="full":
                report=reproduce(output,runner,args.cxx,args.gmp_prefix)
                print(json.dumps({"status":"PASS","types":report["types_reproduced"],"field_rows":report["field_rows"],"resource_seconds":runner.used}),flush=True)
            elif args.command=="_interrupt-probe":
                runner.run("interrupt-probe",[str(Path(sys.executable).resolve()),str(PACKAGE/"probe.py"),str(output/"PROBE-READY.json")],timeout=60)
                raise Refused("An interruption probe must be interrupted")
            elif args.command=="_timeout-probe":
                runner.run("timeout-probe",[str(Path(sys.executable).resolve()),"-c","import time; time.sleep(5)"],timeout=0.1)
                raise Refused("Timeout control unexpectedly completed")
            else:
                runner.run("budget-probe",[str(Path(sys.executable).resolve()),"-c","pass"],category="native",timeout=60)
                raise Refused("Budget control unexpectedly completed")
        return 0
    except FileExistsError as error:
        if owns_output:record_abort(output,{"status":"refused","error":type(error).__name__,"message":str(error),"resource_seconds":runner.used if runner else {},"elapsed_s":time.monotonic()-started})
        print("REFUSED: output directory or member already exists: "+str(error),file=sys.stderr);return 2
    except Stopped as stop:
        if owns_output:record_abort(output,{"status":"interrupted","signal":stop.number,"resource_seconds":runner.used if runner else {},"elapsed_s":time.monotonic()-started})
        print("INTERRUPTED: "+signal.Signals(stop.number).name,file=sys.stderr)
        return 128+stop.number
    except BaseException as error:
        if owns_output:record_abort(output,{"status":"refused","error":type(error).__name__,"message":str(error),"resource_seconds":runner.used if runner else {},"elapsed_s":time.monotonic()-started})
        print("REFUSED: "+type(error).__name__+": "+str(error),file=sys.stderr);return 2


if __name__=="__main__":raise SystemExit(main())
