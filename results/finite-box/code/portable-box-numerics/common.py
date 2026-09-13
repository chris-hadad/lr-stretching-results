"""Portable byte custody and explicit source resolution; no mathematics at import."""
from __future__ import annotations
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
SCHEMA = "portable-box-numerics-v1"
COHORTS = ("production", "U02", "U03", "legacy")
TOTALS = {"production": 620370, "U02": 169, "U03": 3478, "legacy": 297}
SCHEDULE = ((2000, 10000000), (10000, 50000000), (60000, 100000000))
SCOPE = ["Numerical completion means fresh exact counts of the declared full integer H-systems, conditional on their stated geometric/LR interpretation.",
         "Production geometry, algebra, formal bounds and composition require their separate exact identity joins.",
         "Legacy polynomial acceptance and positive strict-anchor/parity gates remain required; old acceptance receipt interfaces are not ported.",
         "No original census proof, whole-box theorem acceptance or historical receipt is inferred.",
         "Local replay budget accounting does not reset or replace an external campaign resource cap."]

class Invalid(ValueError): pass
def need(ok, message):
    if not ok: raise Invalid(message)
def encoded(z): return json.dumps(z, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
def sha(raw): return hashlib.sha256(raw).hexdigest()
def decode(raw):
    def unique(items):
        z = {}
        for k, v in items:
            need(k not in z, "Duplicate JSON field: " + k); z[k] = v
        return z
    def invalid(v): raise Invalid("Nonfinite JSON: " + v)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)
def plain(path):
    p = Path(path).absolute()
    need(not any(q.is_symlink() for q in (p, *p.parents)), "Symlink path refused: " + str(p))
    return p.resolve()
def relative(name):
    need(type(name) is str and name and "\\" not in name and ":" not in name
         and all(ord(x) >= 32 and ord(x) != 127 for x in name), "Invalid portable relative path")
    p = Path(name)
    need(not p.is_absolute() and str(p) == name and all(x not in (".", "..") for x in p.parts), "Escaping/noncanonical source")
    return name
def pin(path):
    p = plain(path); need(p.is_file(), "Missing regular file: " + str(p)); a = p.stat()
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1024**2), b""): h.update(b)
    z = p.stat()
    fields = lambda s: (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    need(fields(a) == fields(z), "File changed while hashing: " + str(p))
    return {"path": str(p), "bytes": a.st_size, "sha256": h.hexdigest()}
def check(p): need(pin(p["path"]) == p, "Changed bound file: " + p["path"])
def read(path): return decode(plain(path).read_bytes())
def save(path, z):
    with plain(path).open("xb") as f:
        f.write(encoded(z) + b"\n"); f.flush(); os.fsync(f.fileno())
def lines(path):
    p = plain(path)
    with (gzip.open(p,"rb") if p.suffix == ".gz" else p.open("rb")) as f:
        for i, raw in enumerate(f):
            need(raw.strip() and raw.endswith(b"\n"), "Malformed exact JSONL stream")
            yield i, decode(raw), raw
def original(name):
    name = relative(name)
    table = read(HERE / "SOURCE-MAP.json")
    declared = {r["path"]: r for r in table["copies"]}
    target = "originals/" + name + ".py"
    need(target in declared, "Module is outside preserved original allowlist")
    p = pin(HERE / target); row = declared[target]
    need((p["bytes"],p["sha256"]) == (row["bytes"],row["sha256"]), "Original module changed")
    module_name = name.replace("-", "_")
    if module_name in sys.modules:
        m = sys.modules[module_name]
        need(Path(m.__file__).resolve() == Path(p["path"]), "Scientific module import escaped originals")
        return m
    folder = str(HERE / "originals")
    if folder not in sys.path: sys.path.insert(0, folder)
    spec = importlib.util.spec_from_file_location(module_name, p["path"])
    m = importlib.util.module_from_spec(spec); sys.modules[module_name] = m; spec.loader.exec_module(m)
    return m
def code_pins():
    table = read(HERE / "SOURCE-MAP.json")
    need(table["schema"] == "portable-numerics-originals-v1", "Unknown original-source map")
    result = [pin(HERE / name) for name in ("SOURCE-MAP.json", "common.py", "numerical_indices.py", "numerics.py")]
    seen = set()
    for row in table["copies"]:
        name = relative(row["path"]); need(name not in seen, "Duplicate copied source"); seen.add(name)
        p = pin(HERE / name)
        need((p["bytes"],p["sha256"]) == (row["bytes"],row["sha256"]), "Copied source differs")
        result.append(p)
    return result
def record_id(z):
    x = z.get("group_id", z.get("target_ordinal", z.get("id")))
    need(type(x) is int, "Missing/noninteger record identity"); return x

class Inputs:
    def __init__(self, recipe):
        self.recipe = recipe; self.root = plain(recipe["data_root"])
        self.used = {}; self.documents = {}; self.resolutions = []
        self.meta = recipe["metadata"]
        for p in self.meta.values(): check(p)
        z = read(self.meta["source_manifest"]["path"])
        need(z.get("schema") == "early-input-manifest-v1", "Relative source manifest required")
        self.expected = {}
        for row in z["files"]:
            need(set(row) == {"path", "bytes", "sha256"}, "Malformed source declaration")
            name = relative(row["path"])
            need(name not in self.expected and type(row["bytes"]) is int and row["bytes"] >= 0
                 and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]), "Duplicate or invalid source declaration")
            self.expected[name] = {k: row[k] for k in ("bytes", "sha256")}
        self.aliases = {}
        plan = read(self.meta["copy_plan"]["path"])
        for row in plan["members"]:
            if row["action"] != "copy_bytes": continue
            target = relative(row["target"])
            need(target.startswith("data/"), "Copy-plan target is not inside portable data")
            name = target[5:]
            if name not in self.expected: continue
            need(self.expected[name] == {"bytes": row["source_bytes"], "sha256": row["source_sha256"]}, "Copy plan/source manifest disagrees")
            self.aliases.setdefault((row["source_bytes"], row["source_sha256"]), set()).add(name)
    def path(self, name):
        name = relative(name); need(name in self.expected, "Unmanifested source: " + name)
        if name not in self.used:
            p = pin(self.root / name)
            need({k:p[k] for k in ("bytes","sha256")} == self.expected[name], "Changed manifested source: " + name)
            self.used[name] = p
        return Path(self.used[name]["path"])
    def document(self, name):
        if name not in self.documents:
            p = self.path(name); raw = p.read_bytes(); need(sha(raw) == self.used[name]["sha256"], "Source changed before reading")
            self.documents[name] = decode(gzip.decompress(raw) if p.suffix == ".gz" else raw)
        return self.documents[name]
    def records(self, name): return lines(self.path(name))
    def resolve(self, reference, catalog):
        # Historical paths are exact catalog keys only. They are never opened,
        # resolved through the host filesystem, or substituted into old receipts.
        identity = {k: reference[k] for k in ("path","bytes","sha256")}
        need(catalog.get(identity["path"]) == identity, "Reference lacks its original source catalog binding")
        choices = sorted(self.aliases.get((identity["bytes"], identity["sha256"]), ()))
        if not choices:
            chosen = self.meta["chosen_terminals"]
            need((identity["bytes"],identity["sha256"]) == (chosen["bytes"],chosen["sha256"]),
                 "No preserved whole-file portable source for " + identity["sha256"] + "; projections cannot replace original bytes")
            check(chosen); doc = read(chosen["path"]); actual = chosen
        else:
            name = choices[0]; doc = self.document(name); actual = self.used[name]
        self.resolutions.append({"original": identity, "portable": actual, "binding": "identical whole-file SHA-256 and size"})
        return doc
    def after(self):
        for p in [*self.meta.values(), *self.used.values()]: check(p)
