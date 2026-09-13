#!/usr/bin/env python3
"""Literal FRONTIER-026 residual/rewrite/terminal composition, independently coded.

No returned program is imported or executed. The accepted F025 census and its
original-preimage multiplicities are premises; this does not enumerate that
651,229,702-obligation census. It verifies the complete literal residual instead.
Horn edges establish sufficient feasible-parent/empty-parent sign implications.

Workflow (all output directories must exist outside --root):
  freeze --root NAMESPACES --output box_manifest.json
  index --root NAMESPACES --manifest box_manifest.json --database box_index.sqlite
        --source EXACT_MANIFEST_PATH --start 0 --limit 250000 --output index_01.json
  seal --root NAMESPACES --manifest box_manifest.json --database box_index.sqlite
       --output box_snapshot.json
  verify --root NAMESPACES --snapshot box_snapshot.json --gate original
         --source base/.../residual-00001.jsonl.gz --start 0 --limit 25000
         --output box_original_01.json
  requirements --root NAMESPACES --snapshot box_snapshot.json --reports CHECKS...
               --output box_requirements.json
  aggregate --root NAMESPACES --snapshot box_snapshot.json --reports CHECKS...
            --acceptances OWNER_ACCEPTED_JSONL... --output box_composition.json

For bounded aggregation use --phase membership, original-weights, horn-weights,
remaining, and acceptance separately. Then --phase final --aggregates PHASES...
requires those exact five passing phases, bound to the same verification roster.

Index each manifest source with index=true to EOF, resuming its reported stop.
Indexing is non-proving. Seal binds a read-only SQLite snapshot of literal rows.
Verify gates and their exact source rosters are listed in the frozen manifest.
Every verification receipt retains actual checked IDs and exact ordinal ranges;
hashes bind bytes and do not replace membership. Resume PARTIAL receipts at stop.
The 100-second internal deadline is separate from the owner's 120-second child
cap. No certificate PASS flag supplies scientific acceptance.

Owner acceptance JSONL records must contain schema='box-terminal-acceptance-v1',
terminal_id, predicate='entire_stretching_polynomial_nonnegative', binding equal
to the generated requirement's binding, and nonempty evidence=[{path,sha256}].
These are explicit owner-accepted premises backed by exact files, not a claim
that this composition checker reproved geometry/counts/algebra/bounds. Required
early U02/U03 numerical terminals and U04 detail/fallback bindings are included.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
from itertools import zip_longest
import json
from math import gcd
from pathlib import Path
import re
import sqlite3
import stat
import sys
import time


SCHEMA = "frontier-026-literal-composition-v1"
BASE = "base/methods/frontier-025-2026-09-10/"
RESIDUAL = BASE + "export-residual/"
ADOPTION = BASE + "ADOPTION.md"
NUMERICAL = {
    4: "final-science/UNIFORM-FOUR-COUNT-CERTIFICATES.jsonl.gz",
    5: "third-interior/COMPLETE-SEXTIC-CERTIFICATES.jsonl.gz",
    6: "final-science/UNIFORM-SEPTIC-CERTIFICATES.jsonl.gz",
    7: "final-science/UNIFORM-OCTIC-CERTIFICATES.jsonl.gz",
    8: "final-science-v2/UNIFORM-NONIC-CERTIFICATES.jsonl.gz",
    9: "final-science/COMPACT-CERTIFICATES.jsonl.gz",
    10: "final-science/COMPACT-CERTIFICATES.jsonl.gz",
    11: "final-science/COMPACT-CERTIFICATES.jsonl.gz",
}
RANK_FIELDS = ("target_rank", "lambda", "mu", "nu")
DECIMAL = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
PRE_REPAIR_SHA = "969d83d6845340e2811351da790e1875a09a7ea4b169599e3bc0701c056005ef"
PRE_REPAIR_FILE = "verify_box_composition.pre_repair_969d83d6845340e2.py"
UNCHANGED_PRE_REPAIR_GATES = {"original", "targets", "horn"}
U04_REPAIRS = "u04/DATA/U04/seven-dual-repairs/certificates.jsonl"
U04_REPAIRS_SHA = "a1f153e2c630b031dffa5e4c7875f8dea63d0eab3f08b6b52cd82003b7183604"


class CheckError(ValueError):
    pass


class DeadlineReached(Exception):
    pass


def need(test, message):
    if not test:
        raise CheckError(message)


def integer(value):
    if type(value) is str:
        need(bool(DECIMAL.fullmatch(value)), f"Malformed integer: {value!r}")
        value = int(value)
    need(type(value) is int, f"Expected exact integer: {value!r}")
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def decode(data):
    def bad(value):
        raise CheckError(f"Nonfinite JSON number: {value}")
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=bad)


def encoded(value):
    return json.dumps(value, separators=(",", ":"), sort_keys=True, allow_nan=False).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Deadline:
    def __init__(self, seconds=None):
        self.end = None if seconds is None else time.monotonic()+seconds

    def check(self):
        if self.end is not None and time.monotonic() >= self.end:
            raise DeadlineReached("Internal wall-clock deadline reached")

    def sqlite_progress(self):
        return int(self.end is not None and time.monotonic() >= self.end)


def file_binding(path, deadline):
    h, size = hashlib.sha256(), 0
    with Path(path).open("rb") as stream:
        while block := stream.read(2**20):
            deadline.check()
            h.update(block)
            size += len(block)
    return {"sha256":h.hexdigest(), "bytes":size}


def database_stamp(path):
    s = Path(path).lstat()
    need(stat.S_ISREG(s.st_mode) and not s.st_mode & 0o222,
         "The sealed index must be a regular read-only file")
    return [s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def path_inside(root, name):
    need(isinstance(name, str) and not Path(name).is_absolute() and ".." not in Path(name).parts,
         f"Input path escapes frozen root: {name!r}")
    path = (Path(root)/name).resolve()
    need(path.is_relative_to(Path(root).resolve()) and path.is_file(), f"Missing/escaping source: {name}")
    return path


def outside(root, path):
    path = Path(path).resolve()
    need(not path.is_relative_to(Path(root).resolve()), "Output/database must be outside the immutable namespace root")
    need(path.parent.is_dir(), "Output directory must already exist")
    return path


def trim(partition):
    p = tuple(integer(x) for x in partition)
    stop = len(p)
    while stop and p[stop-1] == 0:
        stop -= 1
    return p[:stop]


def ordinary_rank(triple):
    return max(map(len, triple))


def legal(triple, area_cap=None, rank_cap=7):
    need(len(triple) == 3 and (rank_cap is None or ordinary_rank(triple) <= rank_cap), "Invalid triple/rank")
    for p in triple:
        need(all(type(x) is int and x >= 0 for x in p) and all(a >= b for a, b in zip(p, p[1:])),
             "Not nonnegative integral partitions")
    need(sum(triple[0]) == sum(triple[1])+sum(triple[2]), "Unbalanced outer-lambda triple")
    if area_cap is not None:
        need(sum(triple[0]) <= area_cap, "Outer area outside accepted residual domain")
    return triple


def contained(triple):
    outer = triple[0]
    return all(len(p) <= len(outer) and all(x <= outer[i] for i, x in enumerate(p)) for p in triple[1:])


def canonical(triple):
    triple = tuple(trim(p) for p in triple)
    factor = gcd(*(x for p in triple for x in p)) or 1
    outer, first, second = (tuple(x//factor for x in p) for p in triple)
    return (outer, *sorted((first, second))), factor


def score(triple):
    return sum(triple[0]), ordinary_rank(triple), triple


def literal_key(triple):
    triple = legal(tuple(trim(p) for p in triple))
    values = [ordinary_rank(triple)] + [x for p in triple for x in p+(0,)*(7-len(p))]
    need(all(0 <= x <= 30 for x in values), "Literal key coordinate outside finite domain")
    return bytes(values)  # An injective full 22-coordinate encoding, not a hash.


def key_triple(key):
    need(type(key) is bytes and len(key) == 22, "Malformed full literal key")
    triple = tuple(trim(key[1+7*k:8+7*k]) for k in range(3))
    need(key[0] == ordinary_rank(triple), "Literal rank disagrees with padding")
    return legal(triple)


def row_triple(row):
    parts = []
    for name in ("lambda", "mu", "nu"):
        p = tuple(integer(x) for x in row[name].split(","))
        need(len(p) == 7, "A target roster must retain all seven padded coordinates")
        parts.append(trim(p))
    result = legal(tuple(parts))
    need(integer(row["target_rank"]) == ordinary_rank(result), "Target rank differs from literal partitions")
    return result


def bare_triple(value):
    return legal(tuple(trim(value[k]) for k in ("lambda", "mu", "nu")), 30)


def original_record(value):
    need(isinstance(value, list) and len(value) == 8, "Original residual must have all eight columns")
    idx, rank, outer, first, second, p6, p7, bound = value
    idx, rank, p6, p7, bound = map(integer, (idx, rank, p6, p7, bound))
    triple = legal(tuple(trim(p) for p in (outer, first, second)), 30)
    need(idx > 0 and rank in (6,7) and rank == ordinary_rank(triple), "Original residual identity/rank mismatch")
    need(p6 >= 0 and p7 >= 0 and p6+p7 > 0 and 5 <= bound <= 12, "Invalid original preimage weight/coordinate bound")
    return idx, triple, p6, p7, bound


def tensor_image(triple, padding, dual_all, outer_choice, exchange):
    need(max(1,ordinary_rank(triple)) <= padding <= 7 and dual_all in (0,1) and outer_choice in (0,1,2)
         and exchange in (0,1), "Illegal tensor orientation/padding")
    padded = tuple(p+(0,)*(padding-len(p)) for p in triple)
    star = lambda p: tuple(-x for x in reversed(p))
    factors = (padded[1], padded[2], star(padded[0]))
    if dual_all:
        factors = tuple(star(p) for p in factors)
    remaining = [i for i in range(3) if i != outer_choice]
    if exchange:
        remaining.reverse()
    outer = star(factors[outer_choice])
    first, second = (factors[i] for i in remaining)
    a, b = first[-1], second[-1]
    return tuple(map(trim, (tuple(x-a-b for x in outer), tuple(x-a for x in first), tuple(x-b for x in second)))), (a,b)


def clipped_gaps(triple):
    need(contained(triple), "Gap rewrite lacks full containment")
    outer, first, second = triple
    first = first+(0,)*(len(outer)-len(first))
    surviving = [(a-b,b) for a,b in zip(outer,first) if a != b]
    shifts = [0]*len(surviving)
    for j in range(len(surviving)-1):
        gap = min(surviving[j][1]-surviving[j+1][1], surviving[j+1][0])
        need(gap >= max(0, surviving[j+1][0]-surviving[j][0]), "Clipped shape ceased to be a partition")
        for i in range(j+1):
            shifts[i] += gap
    result = tuple(trim(p) for p in (tuple(s+row[0] for s,row in zip(shifts,surviving)), tuple(shifts), second))
    legal(result)
    need(sum(result[0]) <= sum(outer), "Gap rewrite increased area")
    return result


def rewrite(source, trace, terminal=None, expected=None, expected_scale=None):
    """Replay only supplied moves; do not search for or claim a canonical optimum."""
    current, scale = canonical(legal(source))
    words = [] if trace in ("", "-") else trace.split(";")
    need(len(words) <= 65, "Rewrite word exceeds the declared finite grammar")
    zero, steps = None, 0
    for number, word in enumerate(words):
        fields = word.split(",")
        is_zero = fields[0] == "Z"
        if is_zero:
            fields = fields[1:]
        need(len(fields) == 5 and zero is None, "Illegal rewrite or operation after a zero terminal")
        n, dual, outer, swap, clip = map(integer, fields)
        need(clip in (0,1), "Illegal gap flag")
        image, _ = tensor_image(current,n,dual,outer,swap)
        if is_zero:
            need(number == len(words)-1 and clip == 0, "Zero witness must be the final un-clipped operation")
            if image[0] and image[0][-1] < 0:
                zero = "ZN"
            else:
                legal(image)
                need(not contained(image), "False transformed noncontainment witness")
                current, zero = image, "ZT"
            continue
        legal(image)
        need(contained(image), "Nonzero rewrite passed an uncertified empty target")
        if clip:
            image = clipped_gaps(image)
        image, factor = canonical(image)
        need(score(image) < score(current), "Rewrite is not strictly decreasing")
        current, scale, steps = image, scale*factor, steps+1
        need(steps <= 64 and scale > 0, "Invalid rewrite count/positive scale")
    if terminal is not None:
        need(zero is None or terminal == zero, "Zero witness has a different terminal label")
        if terminal == "R5":
            need(ordinary_rank(current) <= 5, "False rank-five terminal")
        elif terminal == "A16":
            need(sum(current[0]) <= 16, "False area-sixteen terminal")
        elif terminal == "ZC":
            need(not contained(current), "False original noncontainment terminal")
        elif terminal in ("ZN", "ZT"):
            need(zero == terminal, "Missing/mistyped zero witness")
        else:
            need(terminal in ("F", "LIMIT") and zero is None, "Unknown or inconsistent terminal")
    if expected is not None:
        need(current == expected, "Rewrite literal target changed")
    if expected_scale is not None:
        need(scale == integer(expected_scale), "Rewrite grading scale changed")
    return current, scale, steps, zero


def pth(unit, relative):
    return f"u{unit:02}/DATA/U{unit:02}/{relative}"


def source_catalog():
    result = {}
    def add(path, role, fmt="tsv", gate=None):
        need(path not in result, "Duplicate declared source path")
        result[path] = {"role":role,"format":fmt,"index":fmt != "premise","gate":gate}
    for i in range(1,17):
        add(RESIDUAL+f"residual-{i:05}.jsonl.gz", "original", "jsonl", "original")
    for relative,role,fmt,gate in [
        ("normalization/all-keys.tsv","normal","tsv",None),
        ("normalization/groups.tsv","group3","tsv","targets"),
        ("coverage/positive-target-certificates.jsonl","positive3","jsonl","terminals"),
        ("coverage/REMAINING-TARGETS.tsv","remaining3","tsv",None),
        ("hybrid-verification-v3/certificates.jsonl","early3","jsonl",None),
        ("hybrid-verification-v3/known-join-explicit-words.json","known_join","records",None),
        ("known-join/source-roster.json","family","sources",None),
    ]:
        add(pth(3,relative),role,fmt,gate)
    add(pth(2,"two-model-mixed-certificate.json"),"early2","records")
    for relative,role,gate in [
        ("coverage/NEW-TARGET-CERTIFICATES.tsv","new4","terminals"),
        ("coverage/REMAINING-TARGETS.tsv","remaining4",None),
        ("terminal-scan.tsv","terminal4",None),
    ]:
        add(pth(4,relative),role,"tsv",gate)
    for i in range(19):
        add(pth(4,f"layer5-results/shard-{i:03}/certificates.jsonl"),"detail4","jsonl")
    for relative,role,gate in [
        ("horn-reduction.tsv","horn","horn"),
        ("horn-audit/ROW-DECISIONS.tsv","decision",None),
        ("horn-audit/REMAINING-TARGETS.tsv","group5",None),
    ]:
        add(pth(5,relative),role,"tsv",gate)
    for unit,relative in NUMERICAL.items():
        add(pth(unit,relative),f"cert{unit}","jsonl","certificates")
    for unit in range(3,12):
        name = "COVERED-KEYS.tsv" if unit in (3,4) else "NEW-COVERED-KEYS.tsv"
        add(pth(unit,"coverage/"+name),f"cover{unit}")
        if unit >= 5:
            add(pth(unit,"coverage/REMAINING-TARGETS.tsv"),f"remaining{unit}")
    add(pth(11,"coverage/RESIDUAL-KEY-IDS.txt"),"final_ids","ids")
    add(pth(11,"coverage/REMAINING-ORIGINAL-KEYS.jsonl.gz"),"final_original","jsonl")
    for name in (ADOPTION,RESIDUAL+"manifest.json",RESIDUAL+"global-cover-certificate.json",
                 BASE+"sources/DATA/P08/HORN-INDEX-CERTIFICATE.json"):
        add(name,"premise","premise")
    for n in (6,7):
        for kind in ("horn","masks"):
            add(pth(4,f"tables/{kind}{n}.txt"),"premise","premise")
        add(BASE+f"sources/DATA/P08/HORN{n}.txt","premise","premise")
        add(BASE+f"science/results/F025-MASK-R{n}-001.json","premise","premise")
    return result


CATALOG = source_catalog()


def freeze(root, deadline):
    catalog = {}
    for name, spec in CATALOG.items():
        catalog[name] = {**spec, **file_binding(path_inside(root,name),deadline)}
    residual = decode(path_inside(root,RESIDUAL+"manifest.json").read_bytes())
    need(residual["columns"] == ["id","rank","lambda","mu","nu","original_rank6_preimages","original_rank7_preimages","coordinate_bound"],
         "Accepted residual's eight-column contract changed")
    shards = residual["shards"]
    need([s["name"] for s in shards] == [f"residual-{i:05}.jsonl.gz" for i in range(1,17)], "Missing/duplicate residual shard identities")
    for shard in shards:
        binding = catalog[RESIDUAL+shard["name"]]
        need((binding["sha256"],binding["bytes"]) == (shard["compressed_sha256"],shard["compressed_bytes"]), "Residual compressed-byte binding mismatch")
    return {"schema":SCHEMA,"kind":"manifest","status":"FROZEN_INPUTS_ONLY","sources":catalog,
            "residual_shards":shards,"residual_source_tsv":residual["source_tsv"],
            "upstream_premise":{"adoption":ADOPTION,"original_census":651229702,
            "scope":"Owner-accepted F025 census/preimage bridge; not regenerated here"},
            "gate_sources":{gate:[p for p,s in catalog.items() if s["gate"] == gate]
                            for gate in ("original","horn","targets","terminals","certificates")}}


def validate_manifest(manifest):
    need(manifest.get("schema") == SCHEMA and manifest.get("kind") == "manifest", "Wrong composition manifest")
    need(set(manifest["sources"]) == set(CATALOG), "Manifest source identities changed")
    for path, original in CATALOG.items():
        current = manifest["sources"][path]
        need(all(current[k] == v for k,v in original.items()), "Manifest source role/gate changed")
        need(SHA.fullmatch(current["sha256"]) and integer(current["bytes"]) >= 0, "Malformed source binding")
    need(set(manifest["gate_sources"]) == {"original","horn","targets","terminals","certificates"},
         "Manifest omitted or added a required verification gate")
    for gate in manifest["gate_sources"]:
        need(manifest["gate_sources"][gate] == [p for p,s in CATALOG.items() if s["gate"] == gate], "Expected gate roster changed")


def read_records(path, fmt, start=0):
    if fmt in ("records","sources"):
        document = decode(Path(path).read_bytes())
        for ordinal, value in enumerate(document[fmt]):
            if ordinal >= start:
                yield ordinal, value, digest(encoded(value)), "canonical-json-object"
        return
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path,"rb") as stream:
        header = None
        if fmt == "tsv":
            header = next(csv.reader([stream.readline().decode().rstrip("\r\n")],delimiter="\t"))
            need(header and len(set(header)) == len(header), "Malformed/duplicate TSV header")
        for ordinal, raw in enumerate(stream):
            if ordinal < start:
                continue
            need(raw.endswith(b"\n") and raw.strip(), "Missing newline/empty record")
            if fmt == "tsv":
                fields = next(csv.reader([raw.decode().rstrip("\r\n")],delimiter="\t"))
                need(len(fields) == len(header), "TSV column count mismatch")
                value = dict(zip(header,fields))
            elif fmt == "ids":
                value = integer(raw.decode().strip())
            else:
                value = decode(raw)
            yield ordinal,value,digest(raw),"raw-line-with-newline"


KEY_ROLES = {"normal","group3","remaining3","remaining4","horn","group5",*(f"remaining{u}" for u in range(5,12))}
UNIQUE_KEYS = {"group3","remaining3","remaining4","positive3","group5",*(f"remaining{u}" for u in range(5,12))}


def project_record(role, ordinal, value):
    """Keep literal keys, needed proof fields and original eight-column records."""
    key, w6, w7, bound, aux = None, 0, 0, None, None
    if role in ("original","final_original"):
        idx,t,w6,w7,bound = original_record(value)
        return str(idx),literal_key(t),value,w6,w7,bound,None
    if role == "final_ids":
        return str(integer(value)),None,value,0,0,None,None
    if role in KEY_ROLES:
        key = literal_key(row_triple(value))
        idx = integer(value.get("id",value.get("group_id",value.get("ordinal",ordinal))))
        payload = {k:v for k,v in value.items() if k not in RANK_FIELDS}
    elif role == "positive3":
        target = dict(zip(RANK_FIELDS,value["target"]))
        key,idx,payload = literal_key(row_triple(target)),integer(value["seed_key"]),value
    elif role == "family":
        legal(tuple(trim(p) for p in value["triple"]),rank_cap=None)
        idx,payload = value["source_id"],value
    elif role == "known_join":
        idx, t, w6,w7,bound = original_record(value["raw_record"])
        need(integer(value["id"]) == idx, "Known-join original identity mismatch")
        key,payload = literal_key(t),value
    elif role.startswith("cover"):
        idx,payload = integer(value["id"]),value
    elif role in ("new4","terminal4","decision"):
        idx = integer(value.get("ordinal",value.get("u04_ordinal",ordinal)))
        payload = value
        if role == "decision":
            aux = integer(value["group_id"])
    elif role.startswith("cert") or role in ("detail4","early2","early3"):
        idx = integer(value.get("id",value.get("group_id",value.get("target_ordinal"))))
        if "bare_triple" in value:
            key = literal_key(bare_triple(value["bare_triple"]))
        payload = {k:value[k] for k in ("source","geometry","geometry_sha256","geometry_line_sha256","actual_dimension",
                   "actual_degree","degree_upper_bound","degree_bound","status","raw_record","full_coefficient_vector_computed") if k in value}
        bound = value.get("actual_dimension",value.get("actual_degree"))
        if bound is not None:
            bound = integer(bound)
    else:
        raise CheckError(f"Unknown input role: {role}")
    if isinstance(value,dict):
        if "rank6_preimages" in value:
            w6,w7 = integer(value["rank6_preimages"]),integer(value["rank7_preimages"])
            need(w6 >= 0 and w7 >= 0, "Negative target/preimage weight")
        if "degree_upper_bound" in value:
            bound = integer(value["degree_upper_bound"])
        if "source_coordinate_bound" in value:
            bound = integer(value["source_coordinate_bound"])
    if role in ("group5","horn","decision","terminal4"):
        need(integer(idx) == ordinal, "Declared table ordinal/group ID differs from its physical row identity")
    return str(idx),key,payload,w6,w7,bound,aux


SQL = """
CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS progress (source TEXT PRIMARY KEY,stop INTEGER NOT NULL,complete INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS records (
 role TEXT NOT NULL,id TEXT NOT NULL,source TEXT NOT NULL,ordinal INTEGER NOT NULL,
 literal BLOB,payload TEXT NOT NULL,record_sha256 TEXT NOT NULL,encoding TEXT NOT NULL,
 w6 INTEGER NOT NULL,w7 INTEGER NOT NULL,bound INTEGER,aux INTEGER,
 PRIMARY KEY(role,id),UNIQUE(source,ordinal));
CREATE INDEX IF NOT EXISTS by_literal ON records(role,literal);
CREATE INDEX IF NOT EXISTS by_id ON records(id,role);
"""


def open_database(path, deadline, readonly=False):
    if readonly:
        connection = sqlite3.connect(Path(path).resolve().as_uri()+"?mode=ro",uri=True)
    else:
        connection = sqlite3.connect(path)
        connection.executescript(SQL)
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("PRAGMA synchronous=FULL")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA temp_store=MEMORY")
    connection.set_progress_handler(deadline.sqlite_progress,10000)
    return connection


def index_source(root, manifest, manifest_sha, database, source, start, limit, deadline, report):
    need(source in manifest["sources"] and manifest["sources"][source]["index"], "Source is not in the exact index roster")
    spec = manifest["sources"][source]
    path = path_inside(root,source)
    need(file_binding(path,deadline) == {k:spec[k] for k in ("sha256","bytes")}, "Source changed before indexing")
    connection = open_database(database,deadline)
    try:
        row = connection.execute("SELECT value FROM metadata WHERE key='manifest'").fetchone()
        if row is None:
            connection.execute("INSERT INTO metadata VALUES ('manifest',?)",(manifest_sha,))
            connection.execute("INSERT INTO metadata VALUES ('indexer_sha256',?)",(digest(Path(__file__).read_bytes()),))
            connection.commit()
        else:
            need(row[0] == manifest_sha, "Database belongs to another manifest")
            version = connection.execute("SELECT value FROM metadata WHERE key='indexer_sha256'").fetchone()
            need(version is not None and version[0] == digest(Path(__file__).read_bytes()), "Indexing code changed; start a fresh index epoch")
        state = connection.execute("SELECT stop,complete FROM progress WHERE source=?",(source,)).fetchone()
        need(start == (state[0] if state else 0) and not (state and state[1]), "Index resume must equal its exact unfinished ordinal")
        report.update(start=start,stop=start,checked_ids=[],complete=False)
        complete, seen = False, start
        try:
            for ordinal,value,row_sha,encoding in read_records(path,spec["format"],start):
                deadline.check()
                if limit is not None and ordinal >= start+limit:
                    break
                idx,key,payload,w6,w7,bound,aux = project_record(spec["role"],ordinal,value)
                if spec["role"] in UNIQUE_KEYS:
                    need(connection.execute("SELECT 1 FROM records WHERE role=? AND literal=?",(spec["role"],key)).fetchone() is None,
                         f"Duplicate literal target in {source}")
                connection.execute("INSERT INTO records VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                                   (spec["role"],idx,source,ordinal,key,encoded(payload).decode(),row_sha,encoding,w6,w7,bound,aux))
                report["checked_ids"].append(idx)
                seen = ordinal+1
                report["stop"] = seen
            else:
                complete = True
        except DeadlineReached:
            report["interruption"] = "Index slice reached the internal deadline"
        # A complete prefix is useful indexing evidence even when the next
        # record exceeds the deadline. Any validation error rolls this slice back.
        connection.set_progress_handler(None,0)
        connection.execute("INSERT OR REPLACE INTO progress VALUES (?,?,?)",(source,seen,int(complete)))
        connection.commit()
        report.update(status="INDEXED_ONLY" if complete else "PARTIAL",complete=complete)
    except Exception:
        connection.rollback()
        report.update(stop=start,checked_ids=[],complete=False)
        raise
    finally:
        connection.close()


def check_residual_export(root, manifest, deadline):
    source = manifest["residual_source_tsv"]
    tsv = hashlib.sha256(source["header"].encode())
    tsv_bytes, total, last = len(source["header"].encode()),0,-1
    shards = []
    for shard in manifest["residual_shards"]:
        h,size,count,first = hashlib.sha256(),0,0,None
        with gzip.open(path_inside(root,RESIDUAL+shard["name"]),"rb") as stream:
            for raw in stream:
                if count % 4096 == 0:
                    deadline.check()
                value = decode(raw)
                need(isinstance(value,list) and len(value) == 8, "Original export lost an eight-column record")
                idx = integer(value[0])
                need(idx > last, "Original residual identities are not globally unique and increasing")
                first = idx if first is None else first
                last = idx
                text = "\t".join([str(integer(value[0])),str(integer(value[1])),
                         *(",".join(str(integer(x)) for x in p) for p in value[2:5]),
                         *(str(integer(x)) for x in value[5:])])+"\n"
                line = text.encode()
                tsv.update(line)
                tsv_bytes += len(line)
                h.update(raw)
                size += len(raw)
                count += 1
        need((count,size,h.hexdigest(),first,last) == (shard["records"],shard["expanded_bytes"],shard["expanded_sha256"],shard["first_id"],shard["last_id"]),
             "Original shard expanded bytes/identities disagree with adopted export")
        total += count
        shards.append({"source":RESIDUAL+shard["name"],"records":count,"expanded_sha256":h.hexdigest()})
    need((total,tsv_bytes,tsv.hexdigest()) == (source["records"],source["bytes"],source["sha256"]),
         "Literal eight-column export does not reconstruct the accepted original TSV bytes")
    return {"records":total,"reconstructed_source_tsv_sha256":tsv.hexdigest(),"shards":shards}


def seal(root, manifest, manifest_path, database, deadline):
    connection = open_database(database,deadline,True)
    try:
        states = {r["source"]:(r["stop"],r["complete"]) for r in connection.execute("SELECT * FROM progress")}
        expected = {p for p,s in manifest["sources"].items() if s["index"]}
        need(set(states) == expected and all(done for _,done in states.values()), "Snapshot lacks complete exact source indexing")
        need(connection.execute("SELECT value FROM metadata WHERE key='manifest'").fetchone()[0] == digest(Path(manifest_path).read_bytes()), "Snapshot manifest mismatch")
        indexer = connection.execute("SELECT value FROM metadata WHERE key='indexer_sha256'").fetchone()
        need(indexer is not None and indexer[0] == digest(Path(__file__).read_bytes()), "Index/seal code identity mismatch")
        for source,(total,_) in states.items():
            row = connection.execute("SELECT COUNT(*),MIN(ordinal),MAX(ordinal) FROM records WHERE source=?",(source,)).fetchone()
            need(row[0] == total and (total == 0 or (row[1],row[2]) == (0,total-1)), "Index contains omitted/duplicated source ordinals")
    finally:
        connection.close()
    for source,spec in manifest["sources"].items():
        need(file_binding(path_inside(root,source),deadline) == {k:spec[k] for k in ("sha256","bytes")}, "Changed source during snapshot seal")
    exported = check_residual_export(root,manifest,deadline)
    Path(database).chmod(0o444)
    return {"schema":SCHEMA,"kind":"snapshot","status":"INDEX_SNAPSHOT_ONLY","manifest_path":str(Path(manifest_path).resolve()),
            "manifest_sha256":digest(Path(manifest_path).read_bytes()),"database_path":str(Path(database).resolve()),
            "database":file_binding(database,deadline),"source_rows":{p:n for p,(n,_) in states.items()},"literal_export_binding":exported,
            "database_stamp":database_stamp(database),
            "indexer_sha256":indexer[0]}


class Lookup:
    def __init__(self, connection, root=None):
        self.db = connection
        self.root = root
        self.repair_rows = None

    def u04_repairs(self):
        if self.repair_rows is None:
            need(self.root is not None, "Repair source root was not declared")
            body = path_inside(self.root, U04_REPAIRS).read_bytes()
            need(digest(body) == U04_REPAIRS_SHA, "U04 seven-repair source bytes changed")
            self.repair_rows = [(decode(raw),digest(raw)) for raw in body.splitlines(keepends=True)]
            need(len(self.repair_rows) == 7 and len({integer(r['id']) for r,h in self.repair_rows}) == 7,
                 "U04 seven-repair roster changed")
        return self.repair_rows

    @staticmethod
    def object(row):
        if row is None:
            return None
        result = dict(row)
        result["data"] = decode(result.pop("payload"))
        return result

    def get(self, role, idx, optional=False):
        result = self.object(self.db.execute("SELECT * FROM records WHERE role=? AND id=?",(role,str(idx))).fetchone())
        need(optional or result is not None, f"Missing exact {role}/{idx} identity")
        return result

    def by_key(self, role, key, optional=False):
        rows = self.db.execute("SELECT * FROM records WHERE role=? AND literal=?",(role,key)).fetchall()
        need(len(rows) <= 1 and (optional or rows), f"Missing/duplicate literal target in {role}")
        return self.object(rows[0]) if rows else None

    def certificate(self, gid):
        rows = self.db.execute("SELECT * FROM records WHERE id=? AND role IN ('cert5','cert6','cert7','cert8','cert9','cert10','cert11')",(str(gid),)).fetchall()
        need(len(rows) == 1, f"Post-Horn target {gid} lacks a unique production certificate")
        return self.object(rows[0])


class Tables:
    def __init__(self, root):
        self.horn,self.masks = {},{}
        index = decode(path_inside(root,BASE+"sources/DATA/P08/HORN-INDEX-CERTIFICATE.json").read_bytes())
        for n in (6,7):
            copied = path_inside(root,pth(4,f"tables/horn{n}.txt")).read_bytes()
            adopted = path_inside(root,BASE+f"sources/DATA/P08/HORN{n}.txt").read_bytes()
            need(copied == adopted, "Horn table differs from adopted literal source")
            lines = copied.decode().splitlines()
            rows = [tuple(integer(x) for x in line.split()) for line in lines[1:]]
            need(len(rows) == integer(lines[0]) and rows == list(map(tuple,index["rank_data"][str(n)]["rows"])), "Adopted Horn index roster mismatch")
            for r,I,J,K in rows:
                need(0 < r < n and all(0 < mask < (1<<n) and bin(mask).count("1") == r for mask in (I,J,K)), "Malformed Horn subset masks")
            self.horn[n] = rows
            values = [integer(x) for x in path_inside(root,pth(4,f"tables/masks{n}.txt")).read_text().split()]
            need(values[0] == len(values)-1 == 1<<(3*(n-1)), "Mask roster cardinality mismatch")
            source = decode(path_inside(root,BASE+f"science/results/F025-MASK-R{n}-001.json").read_bytes())
            need(len(source["records"]) == values[0], "Adopted mask roster omitted identities")
            for i,row in enumerate(source["records"]):
                need(row["mask"] == i and integer(row["dimension_bound"]) == values[i+1], "Copied mask bound differs from adopted identity")
            self.masks[n] = values[1:]


def chart_check(triple, row, tables):
    n,dual,outer,swap,mask,bound = (integer(row[k]) for k in ("chart_n","dual","outer","swap","mask","chart_bound"))
    need(max(6,ordinary_rank(triple)) <= n <= 7, "Illegal chart padding")
    image,_ = tensor_image(triple,n,dual,outer,swap)
    legal(image)
    need(contained(image), "Chart is not a legal contained whole-LR orientation")
    padded = tuple(p+(0,)*(n-len(p)) for p in image)
    actual = sum(1<<(part*(n-1)+i) for part,p in enumerate(padded) for i in range(n-1) if p[i] == p[i+1])
    need(actual == mask and tables.masks[n][mask] == bound, "Chart mask/bound changed")
    return image,bound


def horn_children(triple, horn):
    n = ordinary_rank(triple)
    r,I,J,K = horn
    need(all(bin(mask).count("1") == r and 0 < mask < (1<<n) for mask in (I,J,K)), "Invalid Horn child index")
    padded = tuple(p+(0,)*(n-len(p)) for p in triple)
    children = []
    for selected in (True,False):
        child = tuple(trim(p[i] for i in range(n) if bool(mask & (1<<i)) == selected)
                      for p,mask in zip(padded,(K,I,J)))
        children.append(legal(child))
    return tuple(children)


def prior_route(lookup, key):
    positive = lookup.by_key("positive3",key,True)
    if positive:
        return {"unit":3,"seed":int(positive["id"]),"target":key,"anchor":positive["id"]}
    remaining = lookup.by_key("remaining3",key,True)
    if remaining and lookup.get("new4",remaining["id"],True):
        return {"unit":4,"target":key,"ordinal4":int(remaining["id"]),"anchor":remaining["id"]}
    return None


def after_horn_route(lookup, incoming):
    horn = lookup.get("horn",incoming["id"])
    decision = lookup.get("decision",incoming["id"])
    target = key_triple(horn["literal"])
    previous = prior_route(lookup,horn["literal"])
    direct = "R5" if ordinary_rank(target) <= 5 else "A16" if sum(target[0]) <= 16 else None
    if direct or previous:
        need(decision["data"]["status"] == "COVERED" and decision["aux"] == -1, "Horn covered/prior membership differs from literal target")
        claim = decode(decision["data"]["certificate"])
        if direct:
            need(claim == {"kind":direct}, "Changed direct Horn terminal descriptor")
        elif previous["unit"] == 3:
            need(claim["kind"] == "U03_VERIFIED" and integer(claim["seed"]) == previous["seed"], "Wrong U03 Horn reuse seed")
            need(claim["source"] == "DATA/U03/coverage/positive-target-certificates.jsonl", "Changed prior U03 source reference")
        else:
            need(claim["kind"] == "U04_VERIFIED" and integer(claim["ordinal"]) == previous["ordinal4"], "Wrong U04 Horn reuse ordinal")
            need(claim["certificate"] == lookup.get("new4",previous["ordinal4"])["data"], "Changed prior U04 proof descriptor")
        return {"unit":5,"group5":-1,"incoming4":int(incoming["id"]),"target":horn["literal"],"prior":previous,"direct":direct}
    need(decision["data"]["status"] == "REMAIN" and decision["data"]["certificate"] == "-", "False Horn terminal")
    group = lookup.get("group5",decision["aux"])
    need(group["literal"] == horn["literal"], "Horn output joined to an altered post-Horn target")
    certificate = lookup.certificate(group["id"])
    need(certificate["literal"] == group["literal"] and certificate["bound"] == group["bound"], "Post-Horn certificate triple/degree mismatch")
    return {"unit":int(certificate["role"][4:]),"group5":int(group["id"]),"incoming4":int(incoming["id"]),"target":horn["literal"]}


def final_route(lookup, key):
    previous = prior_route(lookup,key)
    return previous if previous else after_horn_route(lookup,lookup.by_key("remaining4",key))


def verify_horn(lookup, record, tables):
    incoming = lookup.get("remaining4",record["id"])
    source, target, row = key_triple(incoming["literal"]), key_triple(record["literal"]), record["data"]
    j = integer(row["horn_index"])
    steps = 0
    if j == -1:
        need(source == target and integer(row["scale"]) == 1 and row["terminal"] == "UNCHANGED" and row["trace"] == "-", "Illegal no-change Horn row")
        need(all(integer(row[k]) == 0 for k in ("horn_r","I","J","K","singleton_lambda","singleton_mu","singleton_nu")), "No-change row contains Horn data")
        child = tuple(trim(integer(x) for x in row[k].split(",")) for k in ("child_lambda","child_mu","child_nu"))
        need(child == source, "No-change child was altered")
    else:
        need(j >= 0 and ordinary_rank(source) == 7 and j < len(tables.horn[7]), "Invalid singleton-Horn index/rank")
        horn = tables.horn[7][j]
        need(horn == tuple(integer(row[k]) for k in ("horn_r","I","J","K")) and horn[0] in (1,6), "Horn index identity changed")
        selected,complement = horn_children(source,horn)
        one,child = (selected,complement) if horn[0] == 1 else (complement,selected)
        singleton = tuple(p[0] if p else 0 for p in one)
        need(all(len(p) <= 1 for p in one) and singleton[0] == singleton[1]+singleton[2], "Singleton factor is not the balanced coefficient-one factor")
        need(singleton == tuple(integer(row[k]) for k in ("singleton_lambda","singleton_mu","singleton_nu")), "Singleton literal changed")
        recorded_child = tuple(trim(integer(x) for x in row[k].split(",")) for k in ("child_lambda","child_mu","child_nu"))
        need(child == recorded_child, "Complementary child literal changed")
        _,_,steps,_ = rewrite(child,row["trace"],row["terminal"],target,row["scale"])
        need(row["terminal"] in ("F","R5","A16") and score(target) < score(source), "Horn target is not a strict permitted reduction")
    chart_check(target,row,tables)
    after_horn_route(lookup,incoming)
    return {"horn_changed":int(j >= 0),"U05_child_rewrite_steps":steps},[]


def check_target(lookup, record):
    key = record["literal"]
    positive = lookup.by_key("positive3",key,True)
    remaining = lookup.by_key("remaining3",key,True)
    need(bool(positive) != bool(remaining), "Normalized target missing or duplicated across covered/remaining rosters")
    if remaining:
        need((record["w6"],record["w7"],record["bound"],integer(record["data"]["keys"])) ==
             (remaining["w6"],remaining["w7"],remaining["bound"],integer(remaining["data"]["keys"])), "U03 remaining target weight/bound changed")
        closed = lookup.get("new4",remaining["id"],True)
        next_remaining = lookup.by_key("remaining4",key,True)
        need(bool(closed) != bool(next_remaining), "U04 target partition has a gap/overlap")
        if next_remaining:
            need((next_remaining["w6"],next_remaining["w7"],next_remaining["bound"],integer(next_remaining["data"]["keys"])) ==
                 (record["w6"],record["w7"],record["bound"],integer(record["data"]["keys"])), "U04 remaining weight/bound changed")
    route = final_route(lookup,key)
    return {f"first_unit_U{route['unit']:02}":1},[]


def verify_original(lookup, record):
    idx,source,p6,p7,bound = original_record(record["data"])
    normal = lookup.get("normal",idx)
    target = key_triple(normal["literal"])
    _,scale,steps,_ = rewrite(source,normal["data"]["trace"],normal["data"]["terminal"],target,normal["data"]["scale"])
    route = final_route(lookup,normal["literal"])
    unit = route["unit"]
    claims = {row["role"]:Lookup.object(row) for row in lookup.db.execute(
        "SELECT * FROM records WHERE id=? AND role IN ('cover3','cover4','cover5','cover6','cover7','cover8','cover9','cover10','cover11')",(str(idx),))}
    expected = {"cover3","cover4"} if unit == 3 else {f"cover{unit}"}
    need(set(claims) == expected, f"Original {idx} has missing/duplicate/wrong first-cover unit identities")
    for claim in claims.values():
        row = claim["data"]
        need((claim["w6"],claim["w7"]) == (p6,p7), "First-cover preimage weights changed")
        if claim["bound"] is not None:
            need(claim["bound"] == bound, "First-cover original coordinate bound changed")
        if claim["role"] == "cover3":
            proof = lookup.get("positive3",route["seed"])["data"]
            need(integer(row["positive_target_seed"]) == route["seed"] and integer(row["original_scale"]) == scale
                 and integer(row["seed_scale"]) == integer(proof["seed_stretch_scale"]) and row["proof_kind"] == proof["proof_kind"], "U03 seed/scale/proof join changed")
        elif claim["role"] == "cover4":
            need(row["proof_namespace"] == f"U{unit:02}" and integer(row["proof_reference"]) == integer(route["anchor"]), "U04 cumulative reference changed")
        else:
            need(integer(row["u05_group_id"]) == route["group5"], "First-cover post-Horn group ID changed")
            if unit == 5:
                need(integer(row["u04_ordinal"]) == route["incoming4"], "U05 incoming ordinal changed")
                want = "PRIOR_POSITIVE_AFTER_HORN" if route["group5"] == -1 else "U05_LOCAL_SIGN_CERTIFICATE"
                need(row["proof"] == want, "U05 first-cover proof category changed")
    return {"original_keys":1,"rank6_preimages":p6,"rank7_preimages":p7,"U03_rewrite_steps":steps,f"U03_scale_{scale}":1,
            f"U{unit:02}_keys":1,f"U{unit:02}_obligations":p6+p7},[]


def numerical_requirement(unit, idx):
    return f"production:U{unit:02}:{idx}"


def u04_source_link(record, detail, selected, repair_rows=None):
    source = detail["source"].split("/DATA/U04/",1)[1]+":"+str(detail["ordinal"]+1)
    need(selected["data"]["certificate"] == source, "U04 original coverage/detail source-line join changed")
    need(selected["data"]["kind"] == detail["data"]["status"], "U04 fallback/direct certificate type changed")
    if record["data"]["source"] == source:
        return None
    prefix = "seven-dual-repairs/certificates.jsonl:"
    reference = record["data"]["source"]
    need(reference.startswith(prefix) and repair_rows is not None, "U04 replacement source was not explicitly bound")
    line = integer(reference[len(prefix):])
    need(1 <= line <= len(repair_rows), "U04 repair line is outside the exact roster")
    repair,row_sha = repair_rows[line-1]
    need(integer(repair["id"]) == integer(record["id"])
         and repair["geometry_sha256"] == record["data"]["geometry_sha256"] == detail["data"]["geometry_sha256"]
         and literal_key(bare_triple(repair["bare_triple"])) == detail["literal"],
         "U04 repair changed its exact whole triple, geometry or terminal ID")
    return {"source":U04_REPAIRS,"source_sha256":U04_REPAIRS_SHA,"line":line,"record_sha256":row_sha,
            "meaning":"Later complete four-count proof replaces the old full-vector terminal for the same entire polynomial"}


def verify_certificate(lookup, record):
    unit = int(record["role"][4:])
    if unit == 4:
        detail = lookup.get("detail4",record["id"])
        target = lookup.get("remaining3",record["id"])
        selected = lookup.get("new4",record["id"])
        need(detail["literal"] == target["literal"], "U04 production certificate literal target changed")
        need(record["data"]["geometry_sha256"] == detail["data"]["geometry_sha256"], "U04 production/detail geometry binding changed")
        replacements = lookup.u04_repairs() if record["data"]["source"].startswith("seven-dual-repairs/") else None
        u04_source_link(record,detail,selected,replacements)
    else:
        target = lookup.get("group5",record["id"])
        need(record["literal"] == target["literal"] and record["bound"] == target["bound"], "Production target literal/actual degree changed")
        need(lookup.certificate(record["id"])["role"] == record["role"], "Duplicate production certificate across units")
    return {f"U{unit:02}_certificates":1},[numerical_requirement(unit,record["id"])]


def check_family_witness(lookup, joined, witness):
    origin = lookup.get("family",witness["source_id"])
    origin_triple = legal(tuple(map(trim,origin["data"]["triple"])))
    need(witness["family"] == origin["data"]["family"] and tuple(map(trim,witness["source_triple"])) == origin_triple, "Known-family source/triple changed")
    n,d,o = (integer(witness[k]) for k in ("padding","dual_all","outer"))
    others = [i for i in range(3) if i != o]
    order = list(map(integer,witness["inner_order"]))
    need(order in (others,others[::-1]), "Illegal family inner exchange")
    image,shifts = tensor_image(origin_triple,n,d,o,0)
    legal(image)
    need(list(shifts) == list(map(integer,witness["determinant_shifts"])), "Family determinant shifts changed")
    g = gcd(*(x for p in image for x in p)) or 1
    image = tuple(tuple(x//g for x in p) for p in image)
    if order != others:
        image = image[0],image[2],image[1]
    need(g == integer(witness["stretch_scale"]) > 0 and image == key_triple(joined["literal"]), "Family literal image/scale mismatch")
    return origin


def terminal3(lookup, record):
    seed = lookup.get("original",record["id"])
    normal = lookup.get("normal",record["id"])
    row = record["data"]
    need(normal["literal"] == record["literal"] and integer(normal["data"]["scale"]) == integer(row["seed_stretch_scale"]) > 0,
         "Positive target's literal seed/scale binding changed")
    need(row["rewrite_terminal"] == normal["data"]["terminal"], "Seed rewrite terminal changed")
    kind = row["proof_kind"]
    if kind in ("R5","A16","ZC","ZN","ZT"):
        need(kind == normal["data"]["terminal"], "Direct terminal does not match the checked rewrite")
        return {"adopted_or_exact_zero_terminals":1},[]
    if kind == "LOCAL_TWO_MODEL_HYBRID":
        local = lookup.get("early3",record["id"])
        need(local["data"]["raw_record"] == seed["data"] and local["literal"] == seed["literal"], "Early U03 certificate lost its full original identity")
        return {"early_U03_numerical_terminals":1},[f"numeric:U03:{record['id']}"]
    need(kind == "EXACT_FAMILY_OR_U02_JOIN", "Unrecognized positive seed authority")
    joined = lookup.get("known_join",record["id"])
    need(joined["data"]["raw_record"] == seed["data"], "Known-family seed original eight columns changed")
    usable = []
    for witness in joined["data"]["witnesses"]:
        origin = check_family_witness(lookup,joined,witness)
        if origin["data"]["family"] != "FRI-unresolved":
            usable.append(origin)
    need(usable, "Provider-only unresolved family supplied a positive terminal")
    chosen = usable[0]  # Literal source order; no new search or family hypothesis.
    family = chosen["data"]["family"]
    if family == "U02-local":
        need(chosen["id"].startswith("U02-"), "Malformed U02 source ID")
        idx = integer(chosen["id"][4:])
        local = lookup.get("early2",idx)
        need(local["literal"] == literal_key(tuple(map(trim,chosen["data"]["triple"]))), "U02 numerical vector/source triple mismatch")
        required = f"numeric:U02:{idx}"
    else:
        need(family in ("FRE","FRI","FRI-settled"), f"Unrecognized adopted family: {family}")
        required = f"adopted:{family}:{chosen['id']}"
    return {"known_family_terminals":1},[required]


def child_terminal(triple, witness, tables):
    if witness.startswith("rewrite:"):
        _,kind,trace = witness.split(":",2)
        need(kind in ("R5","A16","ZC","ZT","ZN"), "Unresolved child rewrite is not a terminal")
        rewrite(triple,trace,kind)
        return
    if witness.startswith("mask:"):
        _,operation,bound,word,trace = witness.split(":",4)
        need(word == "rewrite", "Malformed child mask witness")
        target,_,_,_ = rewrite(triple,trace)
        n,d,o,s,mask = map(integer,operation.split(","))
        image,D = chart_check(target,dict(zip(("chart_n","dual","outer","swap","mask","chart_bound"),(n,d,o,s,mask,integer(bound)))),tables)
        need(D <= 3 or (D == 4 and sum(image[0]) <= 30), "Child mask lacks an adopted positive terminal")
        return
    kind,j,word,trace = witness.split(":",3)
    need(word == "rewrite" and kind in ("horn_zero","horn_product"), "Unknown child terminal grammar")
    target,_,_,_ = rewrite(triple,trace)
    n = ordinary_rank(target)
    j = integer(j)
    need(n in tables.horn and 0 <= j < len(tables.horn[n]), "Child Horn index out of range")
    horn = tables.horn[n][j]
    padded = tuple(p+(0,)*(n-len(p)) for p in target)
    delta = sum(padded[1][i] for i in range(n) if horn[1]>>i&1)+sum(padded[2][i] for i in range(n) if horn[2]>>i&1)-sum(padded[0][i] for i in range(n) if horn[3]>>i&1)
    if kind == "horn_zero":
        need(delta < 0, "False child Horn emptiness witness")
    else:
        need(delta == 0 and n <= 6 and all(ordinary_rank(c) <= 5 for c in horn_children(target,horn)), "Child Horn factors lack the adopted rank-five terminal")


def terminal4(lookup, record, tables):
    target = lookup.get("remaining3",record["id"])
    triple = key_triple(target["literal"])
    row = record["data"]
    if row["kind"] not in ("BOX_MASK4","HORN_PRODUCT"):
        certificate = lookup.get("cert4",record["id"])
        _,requirements = verify_certificate(lookup,certificate)
        return {"U04_numerical_target_joins":1},requirements
    scan = lookup.get("terminal4",record["id"])
    witness = scan["data"]
    need(row["kind"] == witness["status"] and row["certificate"] == f"terminal-scan.tsv:{int(record['id'])+2}", "U04 terminal source-line binding changed")
    image,bound = chart_check(triple,witness,tables)
    if row["kind"] == "BOX_MASK4":
        need(bound == 4 and sum(image[0]) <= 30, "Mask-four terminal outside adopted area/domain")
    else:
        n,j = ordinary_rank(triple),integer(witness["horn_index"])
        need(n in tables.horn and 0 <= j < len(tables.horn[n]), "U04 Horn index out of range")
        horn = tables.horn[n][j]
        children = horn_children(triple,horn)
        if witness["child_witness"] == "both_children_rank_at_most_five":
            need(all(ordinary_rank(c) <= 5 for c in children), "U04 Horn rank terminal failed")
        else:
            need(n == 7 and horn[0] in (1,6), "Unexpected nonterminal U04 Horn split")
            one,large = children if horn[0] == 1 else children[::-1]
            need(ordinary_rank(one) <= 1, "U04 singleton factor malformed")
            child_terminal(large,witness["child_witness"],tables)
    return {"U04_adopted_mask_or_Horn_terminals":1},[]


def verify_slice(root, lookup, manifest, snapshot, gate, source, start, limit, deadline, report):
    need(gate in manifest["gate_sources"] and source in manifest["gate_sources"][gate], "Unexpected gate/source identity")
    total = snapshot["source_rows"][source]
    need(0 <= start <= total, "Verification start outside exact source roster")
    stop = total if limit is None else min(total,start+limit)
    report.update(start=start,stop=start,total=total,checked_ids=[],required_terminal_ids=[],derived_counts={})
    counts,requirements = Counter(),set()
    tables = Tables(root) if gate == "horn" or (gate == "terminals" and CATALOG[source]["role"] == "new4") else None
    try:
        rows = lookup.db.execute("SELECT * FROM records WHERE source=? AND ordinal>=? AND ordinal<? ORDER BY ordinal",(source,start,stop))
        for raw in rows:
            deadline.check()
            record = Lookup.object(raw)
            need(record["ordinal"] == report["stop"], "Verification source ordinal omitted")
            if gate == "original":
                measured,needed = verify_original(lookup,record)
            elif gate == "horn":
                measured,needed = verify_horn(lookup,record,tables)
            elif gate == "targets":
                measured,needed = check_target(lookup,record)
            elif gate == "certificates":
                measured,needed = verify_certificate(lookup,record)
            elif record["role"] == "positive3":
                measured,needed = terminal3(lookup,record)
            else:
                measured,needed = terminal4(lookup,record,tables)
            counts.update(measured)
            requirements.update(needed)
            report["checked_ids"].append(record["id"])
            report["stop"] = record["ordinal"]+1
    finally:
        report["derived_counts"] = dict(counts)
        report["required_terminal_ids"] = sorted(requirements)
    report["status"] = "SLICE_VERIFIED_CONDITIONAL_ON_TERMINALS" if start == 0 and stop == total else "PARTIAL"


def binding_of(record):
    literal = None if record["literal"] is None else [list(p) for p in key_triple(record["literal"])]
    if record["role"] == "family":
        literal = [list(trim(p)) for p in record["data"]["triple"]]
    return {"role":record["role"],"id":record["id"],"source":record["source"],"ordinal":record["ordinal"],
            "record_sha256":record["record_sha256"],"record_encoding":record["encoding"],
            "literal_triple":literal}


def terminal_requirement(lookup, terminal_id):
    kind,namespace,idx = terminal_id.split(":",2)
    if kind == "production":
        unit = integer(namespace[1:])
        need(namespace == f"U{unit:02}" and unit in NUMERICAL, "Unexpected production namespace")
        record = lookup.get(f"cert{unit}",idx)
        binding = binding_of(record)
        if unit == 4:
            detail = lookup.get("detail4",idx)
            binding["literal_triple"] = [list(p) for p in key_triple(detail["literal"])]
            binding["detail_record"] = binding_of(detail)
            binding["detail_status"] = detail["data"].get("status")
            if record["data"]["source"].startswith("seven-dual-repairs/"):
                binding["replacement_proof"] = u04_source_link(record,detail,lookup.get("new4",idx),lookup.u04_repairs())
        components = ["exact algebra","whole-model geometry and actual degree","counter/request bindings","all used finite bound premises"]
    elif kind == "numeric":
        need(namespace in ("U02","U03"), "Unknown early numerical namespace")
        record = lookup.get("early2" if namespace == "U02" else "early3",idx)
        binding = binding_of(record)
        components = ["complete vector or valid four-count sign proof","whole-model degree/geometry","exact determining/holdout count bindings"]
    else:
        need(kind == "adopted" and namespace in ("FRE","FRI","FRI-settled"), "Unknown adopted family requirement")
        record = lookup.get("family",idx)
        need(record["data"]["family"] == namespace, "Adopted family identity changed")
        binding,components = binding_of(record),["exact membership in the campaign-adopted finite family"]
    return {"terminal_id":terminal_id,"predicate":"entire_stretching_polynomial_nonnegative","binding":binding,
            "required_scientific_components":components}


def checked_reports(lookup, manifest, snapshot_sha, code_sha, reports, deadline):
    grouped,requirements,counts = defaultdict(list),set(),Counter()
    hashes = set()
    for path in reports:
        deadline.check()
        body = Path(path).read_bytes()
        need(digest(body) not in hashes, "Duplicate/retried verification receipt")
        hashes.add(digest(body))
        report = decode(body)
        compatible = report.get("checker_sha256") == code_sha or (
            report.get("checker_sha256") == PRE_REPAIR_SHA
            and report.get("gate") in UNCHANGED_PRE_REPAIR_GATES)
        need(report.get("schema") == SCHEMA and report.get("kind") == "verify" and report.get("snapshot_sha256") == snapshot_sha
             and compatible, "Receipt belongs to another snapshot/checker or an affected old gate")
        need(report["status"] in ("SLICE_VERIFIED_CONDITIONAL_ON_TERMINALS","PARTIAL"), "Failed/unstarted receipt cannot supply coverage")
        gate,source = report["gate"],report["source"]
        need(gate in manifest["gate_sources"] and source in manifest["gate_sources"][gate], "Receipt has an unexpected gate/source identity")
        if "checked_ids" not in report:
            continue  # A deadline before setup contributes no coverage.
        start,stop = integer(report["start"]),integer(report["stop"])
        expected = [r[0] for r in lookup.db.execute("SELECT id FROM records WHERE source=? AND ordinal>=? AND ordinal<? ORDER BY ordinal",(source,start,stop))]
        need(0 <= start <= stop and len(expected) == stop-start and expected == report["checked_ids"], "Receipt omitted/duplicated/changed exact checked identities")
        grouped[gate,source].append((start,stop))
        requirements.update(report["required_terminal_ids"])
        counts.update({k:integer(v) for k,v in report["derived_counts"].items()})
    missing = []
    for gate,sources in manifest["gate_sources"].items():
        for source in sources:
            total = lookup.db.execute("SELECT stop FROM progress WHERE source=?",(source,)).fetchone()[0]
            spans = sorted(grouped[gate,source])
            need(total != 0 or len(spans) <= 1, "Duplicate empty-roster receipt")
            cursor = 0
            for start,stop in spans:
                need(start >= cursor and stop <= total, "Overlapping or out-of-range verification slices")
                if start != cursor:
                    missing.append({"gate":gate,"source":source,"start":cursor,"stop":start})
                cursor = stop
            if cursor < total or not spans:
                missing.append({"gate":gate,"source":source,"start":cursor,"stop":total})
    return missing,requirements,counts


def membership_checks(lookup, deadline):
    db = lookup.db
    def empty(query,message,args=()):
        deadline.check()
        need(db.execute(query,args).fetchone() is None,message)
    empty("SELECT id FROM records WHERE role='original' EXCEPT SELECT id FROM records WHERE role='normal'", "Missing normalization identities")
    empty("SELECT id FROM records WHERE role='normal' EXCEPT SELECT id FROM records WHERE role='original'", "Unexpected normalization identities")
    empty("SELECT id FROM records WHERE role LIKE 'cover%' EXCEPT SELECT id FROM records WHERE role='original'", "Cover stream contains an out-of-domain original identity")
    empty("SELECT literal FROM records WHERE role='group3' EXCEPT SELECT literal FROM records WHERE role IN ('positive3','remaining3')", "Uncovered normalized target identity")
    empty("SELECT literal FROM records WHERE role IN ('positive3','remaining3') EXCEPT SELECT literal FROM records WHERE role='group3'", "Unexpected normalized target identity")
    for left,right in (("remaining3","terminal4"),("remaining4","horn"),("remaining4","decision")):
        empty("SELECT id FROM records WHERE role=? EXCEPT SELECT id FROM records WHERE role=?", "Missing exact table row identity",(left,right))
        empty("SELECT id FROM records WHERE role=? EXCEPT SELECT id FROM records WHERE role=?", "Unexpected exact table row identity",(right,left))
    empty("SELECT id FROM records WHERE role='detail4' EXCEPT SELECT id FROM records WHERE role='cert4'", "Unjoined U04 detail/fallback certificate")
    empty("SELECT id FROM records WHERE role='cert4' EXCEPT SELECT id FROM records WHERE role='detail4'", "Missing U04 detail/fallback certificate")
    empty("SELECT id FROM records WHERE role='group5' EXCEPT SELECT id FROM records WHERE role IN ('cert5','cert6','cert7','cert8','cert9','cert10','cert11')", "Post-Horn target missing a production terminal")
    empty("SELECT id FROM records WHERE role IN ('cert5','cert6','cert7','cert8','cert9','cert10','cert11') EXCEPT SELECT id FROM records WHERE role='group5'", "Unexpected post-Horn production terminal")
    for role in ("remaining11","final_ids","final_original"):
        empty("SELECT 1 FROM records WHERE role=?", "Literal final residual is not empty",(role,))
    return {}


def original_weight_checks(lookup, deadline):
    db = lookup.db
    measured,groups = Counter(),0
    query = """SELECT n.literal AS literal,COUNT(*) AS keys,SUM(o.w6) AS w6,SUM(o.w7) AS w7,MIN(o.bound) AS bound,
               MAX(CASE WHEN json_extract(n.payload,'$.terminal') IN ('R5','A16','ZC','ZT','ZN') THEN 1 ELSE 0 END) AS terminal
               FROM records o JOIN records n ON n.role='normal' AND n.id=o.id
               WHERE o.role='original' GROUP BY n.literal"""
    for row in db.execute(query):
        deadline.check()
        group = lookup.by_key("group3",row["literal"])
        need((row["keys"],row["w6"],row["w7"],row["bound"],row["terminal"]) ==
             (integer(group["data"]["keys"]),group["w6"],group["w7"],group["bound"],integer(group["data"]["direct_terminal"])), "Full original-to-target weights/minimum bound/terminal flag changed")
        measured.update(original_keys=row["keys"],rank6_preimages=row["w6"],rank7_preimages=row["w7"])
        groups += 1
    need(groups == db.execute("SELECT COUNT(*) FROM records WHERE role='group3'").fetchone()[0], "Omitted normalized target group")
    return {**measured,"normalized_targets":groups}


def horn_weight_checks(lookup, deadline):
    db = lookup.db
    query = """SELECT h.literal AS literal,COUNT(*) AS parents,SUM(CAST(json_extract(o.payload,'$.keys') AS INTEGER)) AS keys,
               SUM(o.w6) AS w6,SUM(o.w7) AS w7,MIN(o.bound) AS bound,
               MIN(CAST(json_extract(h.payload,'$.chart_bound') AS INTEGER)) AS chart_bound,
               MIN(CAST(o.id AS INTEGER)) AS representative
               FROM records o JOIN records h ON h.role='horn' AND h.id=o.id
               JOIN records d ON d.role='decision' AND d.id=o.id
               WHERE o.role='remaining4' AND d.aux>=0 GROUP BY h.literal"""
    post = 0
    for row in db.execute(query):
        deadline.check()
        group = lookup.by_key("group5",row["literal"])
        need((row["keys"],row["w6"],row["w7"],row["bound"],row["chart_bound"],row["representative"]) ==
             (integer(group["data"]["keys"]),group["w6"],group["w7"],group["bound"],integer(group["data"]["target_chart_bound"]),integer(group["data"]["representative_u04_ordinal"])),
             "Post-Horn literal group weights/minima/representative changed")
        post += 1
    need(post == db.execute("SELECT COUNT(*) FROM records WHERE role='group5'").fetchone()[0], "Omitted post-Horn group")
    return {"post_Horn_targets":post}


def remaining_checks(lookup, deadline):
    db = lookup.db
    # Each later remaining-target file is the exact complement of completed
    # production units, preserving every literal target, weight and bound.
    for unit in range(5,12):
        completed = tuple(f"cert{u}" for u in range(5,unit+1))
        placeholders = ",".join("?" for _ in completed)
        expected = {r[0] for r in db.execute(f"SELECT id FROM records WHERE role='group5' EXCEPT SELECT id FROM records WHERE role IN ({placeholders})",completed)}
        actual = {r[0] for r in db.execute("SELECT id FROM records WHERE role=?",(f"remaining{unit}",))}
        need(actual == expected, f"Unit {unit} remaining target identities differ from exact complement")
        for idx in actual:
            deadline.check()
            old,new = lookup.get("group5",idx),lookup.get(f"remaining{unit}",idx)
            need((old["literal"],old["w6"],old["w7"],old["bound"],integer(old["data"]["keys"])) ==
                 (new["literal"],new["w6"],new["w7"],new["bound"],integer(new["data"]["keys"])), "Retained target literal/weight/bound changed")
    return {}


GROUP_PHASES = {"membership":membership_checks,"original-weights":original_weight_checks,
                "horn-weights":horn_weight_checks,"remaining":remaining_checks}


def exact_group_checks(lookup, deadline, phase="all"):
    result = {}
    for name in GROUP_PHASES if phase == "all" else (phase,):
        result.update(GROUP_PHASES[name](lookup,deadline))
    return result


def complete_terminal_requirements(lookup, deadline):
    required = set()
    for row in lookup.db.execute("SELECT role,id FROM records WHERE role IN ('cert4','cert5','cert6','cert7','cert8','cert9','cert10','cert11')"):
        required.add(numerical_requirement(int(row["role"][4:]),row["id"]))
    for row in lookup.db.execute("SELECT * FROM records WHERE role='positive3'"):
        deadline.check()
        _,needed = terminal3(lookup,Lookup.object(row))
        required.update(needed)
    return required


def accepted_terminals(lookup, required, paths, deadline, bindings=None):
    accepted,checked_evidence = set(),{}
    input_files = {str(Path(p).resolve()):file_binding(p,deadline) for p in paths}
    for path in paths:
        with Path(path).open("rb") as stream:
            for raw in stream:
                deadline.check()
                entry = decode(raw)
                need(entry.get("schema") == "box-terminal-acceptance-v1", "Wrong owner terminal-acceptance schema")
                tid = entry["terminal_id"]
                need(tid in required and tid not in accepted, "Unexpected/duplicate owner terminal acceptance")
                expectation = terminal_requirement(lookup,tid)
                need(entry["predicate"] == expectation["predicate"] and entry["binding"] == expectation["binding"], "Owner acceptance has a changed literal/source/certificate binding")
                evidence = entry["evidence"]
                need(isinstance(evidence,list) and evidence, "Terminal acceptance lacks exact scientific evidence files")
                for item in evidence:
                    path = str(Path(item["path"]).resolve())
                    if path not in checked_evidence:
                        checked_evidence[path] = file_binding(path,deadline)["sha256"]
                    need(checked_evidence[path] == item["sha256"], "Changed/missing owner terminal evidence")
                accepted.add(tid)
    for path,sha in checked_evidence.items():
        need(file_binding(path,deadline)["sha256"] == sha, "Owner terminal evidence changed during aggregate")
    for path,binding in input_files.items():
        need(file_binding(path,deadline) == binding, "Owner acceptance file changed during aggregate")
    if bindings is not None:
        bindings.update(acceptance_files=input_files,evidence_files=checked_evidence)
    return required-accepted


def phase_receipts(paths, snapshot_sha, code_sha, verification_roster, deadline):
    expected = {*GROUP_PHASES,"acceptance"}
    seen,result = set(),{}
    for path in paths:
        deadline.check()
        record = decode(Path(path).read_bytes())
        name = record.get("phase")
        need(record.get("schema") == SCHEMA and record.get("kind") == "aggregate"
             and record.get("snapshot_sha256") == snapshot_sha and record.get("checker_sha256") == code_sha
             and record.get("status") == "AGGREGATE_PHASE_PASS", "Invalid or incomplete aggregate phase")
        need(name in expected and name not in seen, "Unexpected/duplicate aggregate phase identity")
        need(record["verification_receipts"] == verification_roster, "Aggregate phases used different exact verification rosters")
        seen.add(name)
        result[name] = record
    need(seen == expected, "Missing required aggregate phase identities")
    for path,binding in result["acceptance"]["terminal_evidence_bindings"]["acceptance_files"].items():
        need(file_binding(path,deadline) == binding, "Owner acceptance changed after phase verification")
    for path,sha in result["acceptance"]["terminal_evidence_bindings"]["evidence_files"].items():
        need(file_binding(path,deadline)["sha256"] == sha, "Owner scientific evidence changed after phase verification")
    return result


def load_snapshot(root, path, deadline):
    body = Path(path).read_bytes()
    snapshot = decode(body)
    need(snapshot.get("schema") == SCHEMA and snapshot.get("kind") == "snapshot", "Wrong snapshot format")
    code_sha = digest(Path(__file__).read_bytes())
    epoch_sha = snapshot.get("indexer_sha256")
    need(epoch_sha in (code_sha,PRE_REPAIR_SHA), "Current checker is not compatible with the frozen index epoch")
    if epoch_sha == PRE_REPAIR_SHA:
        predecessor = Path(__file__).with_name(PRE_REPAIR_FILE)
        need(digest(predecessor.read_bytes()) == PRE_REPAIR_SHA, "Approved predecessor source is missing or changed")
    manifest_body = Path(snapshot["manifest_path"]).read_bytes()
    need(digest(manifest_body) == snapshot["manifest_sha256"], "Snapshot manifest changed")
    manifest = decode(manifest_body)
    validate_manifest(manifest)
    need(manifest.get("checker_sha256") == epoch_sha, "Manifest and indexer epochs differ")
    need(file_binding(path_inside(root,U04_REPAIRS),deadline)["sha256"] == U04_REPAIRS_SHA,
         "Additional seven-repair source is missing or changed")
    # The POSIX read-only index has a full hash at seal and final aggregation.
    # Every intervening check binds device/inode/size and both modification
    # clocks, avoiding a multi-gigabyte reread before each small verification.
    need(database_stamp(snapshot["database_path"]) == snapshot["database_stamp"], "Sealed literal SQLite snapshot changed")
    # The sealed database contains the exact frozen literal rows. Fresh source
    # checks happen again at aggregate; individual reads use the immutable copy.
    return snapshot,manifest,digest(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command",choices=("freeze","index","seal","verify","requirements","aggregate"))
    parser.add_argument("--root",required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--database")
    parser.add_argument("--snapshot")
    parser.add_argument("--source")
    parser.add_argument("--gate",choices=("original","horn","targets","terminals","certificates"))
    parser.add_argument("--start",type=int,default=0)
    parser.add_argument("--limit",type=int)
    parser.add_argument("--reports",nargs="*",default=[])
    parser.add_argument("--acceptances",nargs="*",default=[])
    parser.add_argument("--phase",choices=("all",*GROUP_PHASES,"acceptance","final"),default="all")
    parser.add_argument("--aggregates",nargs="*",default=[])
    parser.add_argument("--budget-seconds",type=int,default=100)
    parser.add_argument("--output",required=True)
    args = parser.parse_args()
    started = time.monotonic()
    report = {"schema":SCHEMA,"kind":args.command,"status":"NOT_STARTED"}
    connection = None
    try:
        need(0 < args.budget_seconds <= 110 and args.start >= 0 and (args.limit is None or args.limit > 0), "Invalid budget/slice")
        deadline = Deadline(args.budget_seconds)
        root,output = Path(args.root).resolve(),outside(args.root,args.output)
        need(not output.exists(), "Refusing to overwrite an existing receipt")
        code_sha = digest(Path(__file__).read_bytes())
        report["checker_sha256"] = code_sha
        if args.command == "freeze":
            report.update(freeze(root,deadline))
        elif args.command in ("index","seal"):
            need(args.manifest and args.database, "Index/seal require --manifest and --database")
            body = Path(args.manifest).read_bytes()
            manifest = decode(body)
            validate_manifest(manifest)
            database = outside(root,args.database)
            report["manifest_sha256"] = digest(body)
            if args.command == "index":
                report["source"] = args.source
                index_source(root,manifest,digest(body),database,args.source,args.start,args.limit,deadline,report)
            else:
                report.update(seal(root,manifest,args.manifest,database,deadline))
        else:
            need(args.snapshot, "Verification/aggregation require --snapshot")
            snapshot,manifest,snapshot_sha = load_snapshot(root,args.snapshot,deadline)
            report["snapshot_sha256"] = snapshot_sha
            connection = open_database(snapshot["database_path"],deadline,True)
            lookup = Lookup(connection,root)
            report["additional_repair_source"] = {"path":U04_REPAIRS,"sha256":U04_REPAIRS_SHA}
            report["accepted_predecessor"] = {"sha256":PRE_REPAIR_SHA,"unchanged_receipt_gates":sorted(UNCHANGED_PRE_REPAIR_GATES),
                                               "index_projection_and_schema_unchanged":True}
            if args.command == "verify":
                need(args.gate and args.source, "Verify requires --gate and --source")
                report.update(gate=args.gate,source=args.source)
                verify_slice(root,lookup,manifest,snapshot,args.gate,args.source,args.start,args.limit,deadline,report)
            else:
                missing,required,counts = checked_reports(lookup,manifest,snapshot_sha,code_sha,args.reports,deadline)
                report.update(missing_slices=missing,derived_counts=dict(counts),required_terminal_count=len(required))
                if args.command == "requirements":
                    ordered = sorted(required)
                    chosen = ordered[args.start:None if args.limit is None else args.start+args.limit]
                    report.update(status="REQUIREMENTS_ONLY",requirements=[terminal_requirement(lookup,tid) for tid in chosen],
                                  start=args.start,stop=args.start+len(chosen),total=len(ordered))
                else:
                    report["phase"] = args.phase
                    verification_roster = sorted([{"path":str(Path(p).resolve()),**file_binding(p,deadline)} for p in args.reports],key=lambda x:x["path"])
                    report["verification_receipts"] = verification_roster
                    if missing:
                        report["status"] = "PARTIAL"
                    else:
                        if args.phase in ("all",*GROUP_PHASES):
                            measured = exact_group_checks(lookup,deadline,args.phase)
                            if "original_keys" in measured:
                                need(all(measured[k] == counts[k] for k in ("original_keys","rank6_preimages","rank7_preimages")),
                                     "Verified original populations disagree with exact literal joins")
                            report["literal_group_composition"] = measured
                            report["status"] = "AGGREGATE_PHASE_PASS"
                        if args.phase in ("all","acceptance"):
                            need(complete_terminal_requirements(lookup,deadline) == required,
                                 "Verification receipts omitted or added a terminal dependency")
                            evidence_bindings = {}
                            missing_terminals = accepted_terminals(lookup,required,args.acceptances,deadline,evidence_bindings)
                            report.update(missing_terminal_ids=sorted(missing_terminals),terminal_evidence_bindings=evidence_bindings,
                                          status="AGGREGATE_PHASE_PASS" if not missing_terminals else "TERMINAL_ACCEPTANCE_REQUIRED")
                        if args.phase == "final":
                            phases = phase_receipts(args.aggregates,snapshot_sha,code_sha,verification_roster,deadline)
                            report["literal_group_composition"] = {**phases["original-weights"]["literal_group_composition"],
                                                                   **phases["horn-weights"]["literal_group_composition"]}
                            report["status"] = "AGGREGATE_PHASE_PASS"
                        if args.phase in ("all","final"):
                            need(file_binding(snapshot["database_path"],deadline) == snapshot["database"],
                                 "Final sealed-index byte hash changed")
                            for path,spec in manifest["sources"].items():
                                need(file_binding(path_inside(root,path),deadline) == {k:spec[k] for k in ("sha256","bytes")}, "Source changed after frozen verification")
                            if report["status"] == "AGGREGATE_PHASE_PASS":
                                report["status"] = "COMPLETE_LITERAL_COMPOSITION_WITH_OWNER_ACCEPTED_TERMINALS"
                        report["Horn_scope"] = "Sufficient sign implication: infeasible parent is zero; otherwise valid Horn factorization applies. No unconditional count identity inferred."
                        report["upstream_scope"] = "F025 original census/preimage bridge and adopted mask/Horn/rank/area premises retained; no huge census rerun."
            need(database_stamp(snapshot["database_path"]) == snapshot["database_stamp"],
                 "Sealed index changed during this verification")
            need(file_binding(path_inside(root,U04_REPAIRS),deadline)["sha256"] == U04_REPAIRS_SHA,
                 "Additional seven-repair source changed during verification")
    except DeadlineReached as error:
        report.update(status="PARTIAL",interruption=str(error))
    except (CheckError,sqlite3.Error,KeyError,TypeError,ValueError,IndexError,OSError,EOFError) as error:
        if isinstance(error,sqlite3.OperationalError) and "interrupted" in str(error):
            report.update(status="PARTIAL",interruption="SQLite operation reached the internal deadline")
        else:
            report.update(status="FAIL",error=f"{type(error).__name__}: {error}")
    finally:
        if connection is not None:
            connection.close()
    report["elapsed_seconds"] = round(time.monotonic()-started,6)
    report["requested_slice_complete"] = (
        report["status"] == "PARTIAL" and "interruption" not in report
        and args.command in ("index","verify") and args.limit is not None
        and (report.get("stop") == args.start + args.limit
             or (args.command == "verify" and report.get("stop") == report.get("total"))))
    output = Path(args.output).resolve()
    if not output.is_relative_to(Path(args.root).resolve()) and not output.exists() and output.parent.is_dir():
        with output.open("x",encoding="utf-8") as stream:
            json.dump(report,stream,indent=2,sort_keys=True,allow_nan=False)
            stream.write("\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("sources","checked_ids","requirements","required_terminal_ids","missing_terminal_ids","source_rows","verification_receipts","terminal_evidence_bindings")},sort_keys=True))
    return 1 if report["status"] == "FAIL" else 2 if (report["status"] == "TERMINAL_ACCEPTANCE_REQUIRED"
        or (report["status"] == "PARTIAL" and not report["requested_slice_complete"])) else 0


if __name__ == "__main__":
    sys.exit(main())
