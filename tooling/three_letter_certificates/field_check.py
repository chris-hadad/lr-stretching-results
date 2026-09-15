"""Exact full-field checking directly in the original normal lattice."""
import argparse
import csv
from fractions import Fraction
import json
from pathlib import Path
import time
from runner import digest as sha, save

def original_certificate(q):
    result={}
    with (TYPES/f"q{q}.verified.tsv").open() as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            index=int(row["image_index"])
            if index:
                result[int(row["mask"])]=(index,int(row["type_id"]))
    return result


def exact_number(value):
    if type(value) not in (str,int):raise ValueError("Field coefficients must be explicit exact rational strings or integers")
    return Fraction(value)


def check_field(q,field_path,output,zero_field=False):
    began=time.monotonic()
    data=json.loads(field_path.read_text())
    if data["q"]!=q or data["ambient_dimension"]!=7 or exact_number(data["epsilon"])!=Fraction(1,100000000):
        raise RuntimeError("Field boundary/epsilon differs from frozen proposed contract")
    epsilon=exact_number(data["epsilon"])
    raw=list(map(int,(DATA/"normals.txt").read_text().split()))
    if raw[:2]!=[32,7] or len(raw)!=226:raise RuntimeError("Normal boundary mismatch")
    normals=[raw[2+7*i:2+7*(i+1)] for i in range(32)]
    supports=original_certificate(q-1);rows=original_certificate(q)
    alpha={}
    for row in csv.DictReader((VALUES/f"q{q}.values.tsv").open(),delimiter="\t"):
        tid=int(row["type_id"])
        if tid in alpha:raise RuntimeError("Repeated independent alpha type")
        alpha[tid]=Fraction(row["alpha"])
    if set(alpha)!={tid for index,tid in rows.values()}:raise RuntimeError("Independent alpha type coverage mismatch")
    active={};kernel_equations=0
    for record in ([] if zero_field else data["field"]):
        mask=record["support_mask"]
        if type(mask) is not int or mask not in supports or mask in active:
            raise RuntimeError("Unknown, dependent or repeated ambient support")
        if len(record["g"])!=7:raise RuntimeError("Ambient vector dimension mismatch")
        g=tuple(exact_number(x) for x in record["g"])
        for i in range(32):
            if mask&(1<<i):
                if sum((g[j]*normals[i][j] for j in range(7) if normals[i][j]),Fraction(0)):
                    raise RuntimeError("Ambient kernel equation failed")
                kernel_equations+=1
        active[mask]=g
    actions={}
    for mask,g in active.items():
        actions[mask]=tuple(sum((g[j]*normals[i][j] for j in range(7) if normals[i][j]),Fraction(0)) for i in range(32))
    row_output=output.with_suffix(".rows.tsv")
    minimum=None;minimum_mask=None;bad=0;first_bad=[];incidences=0;nonunit=0;used_nonzero_support_incidences=0
    with row_output.open("x") as stream:
        stream.write("mask\ttype_id\talpha\tcorrection\tbeta\n")
        for mask,(index,tid) in rows.items():
            correction=Fraction(0)
            for i in range(32):
                if not mask&(1<<i):continue
                support=mask^(1<<i)
                if support not in supports:raise RuntimeError("Missing original primitive support")
                projected=supports[support][0]
                if index%projected:raise RuntimeError("Nonintegral original primitive divisor")
                divisor=index//projected;incidences+=1;nonunit+=divisor!=1
                if support in actions:
                    correction+=actions[support][i]/divisor;used_nonzero_support_incidences+=1
            value=alpha[tid]+correction
            if minimum is None or value<minimum:minimum=value;minimum_mask=mask
            if value<epsilon:
                bad+=1
                if len(first_bad)<20:first_bad.append(dict(mask=mask,type=tid,beta=str(value)))
            stream.write(f"{mask}\t{tid}\t{alpha[tid]}\t{correction}\t{value}\n")
    report=dict(schema="three-letter-ambient-field/v1",status="PASS" if bad==0 else "FAIL",q=q,epsilon=str(epsilon),
                rows=len(rows),full_original_supports=len(supports),listed_active_supports=len(active),
                omitted_zero_supports=len(supports)-len(active),kernel_equations=kernel_equations,
                original_incident_divisors=incidences,nonunit_original_divisors=nonunit,
                used_listed_support_incidences=used_nonzero_support_incidences,
                minimum_beta=str(minimum),minimum_mask=minimum_mask,below_epsilon=bad,first_bad=first_bad,
                mutation="zero-field" if zero_field else "none",field_sha256=sha(field_path),
                independent_values_sha256=sha(VALUES/f"q{q}.values.tsv"),
                row_evidence_sha256=sha(row_output),elapsed_s=time.monotonic()-began)
    save(output,report);print(json.dumps(report,sort_keys=True),flush=True)
    return int(bad!=0)


def main():
    global DATA,TYPES,VALUES
    parser=argparse.ArgumentParser()
    parser.add_argument("data",type=Path)
    parser.add_argument("types",type=Path)
    parser.add_argument("values",type=Path)
    parser.add_argument("q",type=int,choices=(3,4,5,6))
    parser.add_argument("output",type=Path)
    parser.add_argument("--zero-field",action="store_true")
    args=parser.parse_args();DATA,TYPES,VALUES=args.data,args.types,args.values
    return check_field(args.q,DATA/f"field-q{args.q}.json",args.output,args.zero_field)

if __name__=="__main__":raise SystemExit(main())
