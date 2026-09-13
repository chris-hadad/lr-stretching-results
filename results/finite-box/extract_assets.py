#!/usr/bin/env python3
"""Extract only the complete archive/member union pinned by the module config."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile

CONFIG_SCHEMA="finite-box-recipient-config-v1"
MAX_EXPANDED=30_000_000_000
MAX_FILE=2_000_000_000
MAX_ARCHIVE=1_800_000_000

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
def plain(path):
    p=Path(path).absolute();need(not any(x.is_symlink() for x in (p,*p.parents)),"Symlink input/output path refused")
    return p.resolve()
def relative(name):
    need(type(name) is str and name and "\\" not in name and ":" not in name and all(32<=ord(c)!=127 for c in name),"Malformed relative filename")
    p=PurePosixPath(name);need(not p.is_absolute() and p.as_posix()==name and all(x not in (".","..") for x in p.parts),"Escaping/noncanonical filename")
    return p
def signature(path):
    s=Path(path).stat();return s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns
def pin(path):
    path=plain(path);need(path.is_file(),"Missing regular file: "+str(path));before=signature(path);h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024**2),b""):h.update(block)
    need(before==signature(path),"Source changed during byte hashing")
    return {"path":str(path),"bytes":before[2],"sha256":h.hexdigest()}
def check(value):need(pin(value["path"])==value,"Changed pinned source: "+value["path"])
def digest(value):need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}",value),"Expected an exact SHA256");return value
def natural(value):need(type(value) is int and value>=0,"Expected an exact nonnegative integer");return value
def bound(root,value,required_path=None):
    name=relative(value["path"]).as_posix()
    if required_path is not None:need(name==required_path,"Wrong configured module-relative source path")
    current=pin(plain(root)/name)
    need(current["bytes"]==natural(value["bytes"]) and current["sha256"]==digest(value["sha256"]),"Stale configured metadata/tool bytes")
    return current
def config(root):
    p=pin(plain(root)/"REPRODUCTION-CONFIG.json");body=decode(Path(p["path"]).read_bytes())
    need(body.get("schema")==CONFIG_SCHEMA,"Missing recipient configuration contract")
    return body,p

def catalog_contract(assets,source,expected):
    need(assets.get("schema")=="finite-box-data-assets-v1" and source.get("schema")=="early-input-manifest-v1","Wrong archive/source manifest schema")
    need(0<natural(expected["count"])<=100 and 0<natural(expected["members"])<=150000 and
         0<natural(expected["expanded_bytes"])<=MAX_EXPANDED,"Invalid configured extraction bounds")
    rows={}
    for row in source["files"]:
        need(set(row)=={"path","bytes","sha256"},"Malformed exact source member record")
        name=relative(row["path"]).as_posix();need(name not in rows and natural(row["bytes"])<=MAX_FILE,"Duplicate/oversized source member")
        digest(row["sha256"]);rows[name]=row
    need(len(rows)==expected["members"]==assets["members"] and sum(r["bytes"] for r in rows.values())==expected["expanded_bytes"]==assets["expanded_bytes"],
         "Configured archive/source union size differs")
    files={}
    for row in assets["assets"]:
        need(set(row)=={"name","bytes","sha256","members"},"Malformed exact archive record")
        name=relative(row["name"]).as_posix();need("/" not in name and name.endswith(".tar.gz") and name not in files,"Duplicate or unsafe archive filename")
        need(0<natural(row["bytes"])<=MAX_ARCHIVE and 0<natural(row["members"])<=expected["members"],"Invalid archive bounds")
        digest(row["sha256"]);files[name]=row
    need(len(files)==expected["count"] and sum(r["members"] for r in files.values())==expected["members"],"Incomplete exact archive roster")
    # A source file may never also be a directory needed by another member.
    for name in rows:
        need(not any(p.as_posix() in rows for p in PurePosixPath(name).parents if p.as_posix()!="."),"Source file/directory prefix collision")
    return files,rows

class LimitedReader:
    def __init__(self,stream,limit):self.stream,self.limit,self.total=stream,limit,0
    def read(self,size):
        need(type(size) is int and size>=0,"Unbounded decompression read refused")
        block=self.stream.read(min(size,self.limit-self.total+1));self.total+=len(block)
        need(self.total<=self.limit,"Expanded TAR stream exceeded its fixed bound")
        return block

def write_member(root_fd,name,member,stream,expected):
    directory=os.dup(root_fd)
    try:
        parts=PurePosixPath(name).parts
        for part in parts[:-1]:
            try:os.mkdir(part,0o755,dir_fd=directory)
            except FileExistsError:pass
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=directory)
            os.close(directory);directory=child
        fd=os.open(parts[-1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=directory)
        h=hashlib.sha256();size=0
        with os.fdopen(fd,"wb") as output:
            with stream.extractfile(member) as inp:
                while size<member.size:
                    block=inp.read(min(1024**2,member.size-size));need(block,"Truncated regular TAR member")
                    output.write(block);h.update(block);size+=len(block)
                need(not inp.read(1),"Member stream exceeded its declared size")
            need(size==expected["bytes"] and h.hexdigest()==expected["sha256"],"Member bytes/hash differ from the exact source manifest")
            output.flush();os.fsync(output.fileno());os.fchmod(output.fileno(),0o444)
        fd=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=directory)
        with os.fdopen(fd,"rb") as inp:
            s=os.fstat(inp.fileno());need(stat.S_ISREG(s.st_mode) and not s.st_mode&0o222 and not s.st_mode&0o111,"Extracted data/code is not inert and read-only")
            readback=hashlib.file_digest(inp,"sha256").hexdigest()
        need(s.st_size==size and readback==expected["sha256"],"Written member failed complete readback")
    finally:os.close(directory)

def extract(assets_dir,data,catalog,source,expected,inputs):
    """No CLI can replace the pinned configuration; small fixtures call this core."""
    need(sys.version_info>=(3,11) and os.name=="posix" and hasattr(os,"O_NOFOLLOW"),"Python 3.11+ and POSIX no-follow directory descriptors are required")
    assets_dir,data=plain(assets_dir),plain(data);need(assets_dir.is_dir() and not data.exists(),"An asset directory and fresh logical data root are required")
    receipt=data.with_name(data.name+".EXTRACTION.json");need(not receipt.exists() and not receipt.is_symlink(),"Extraction receipt must be fresh")
    archives,members=catalog_contract(catalog,source,expected)
    need({p.name for p in assets_dir.glob("*.tar.gz")}==set(archives),"Missing or extra asset archives")
    pinned=[]
    # Authenticate every complete compressed archive before interpreting TAR data.
    for name,row in archives.items():
        p=pin(assets_dir/name);need((p["bytes"],p["sha256"])==(row["bytes"],row["sha256"]),"Stale/corrupt compressed asset: "+name);pinned.append(p)
    for p in inputs:check(p)
    data.mkdir(parents=True);root_fd=os.open(data,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    seen=set();completed=[];decompressed=0
    try:
        for p in pinned:
            count=0
            with Path(p["path"]).open("rb") as compressed,gzip.GzipFile(fileobj=compressed,mode="rb") as inflated:
                bounded=LimitedReader(inflated,MAX_EXPANDED-decompressed)
                with tarfile.open(fileobj=bounded,mode="r|") as stream:
                    for member in stream:
                        need(count<archives[Path(p["path"]).name]["members"],"Extra archive member")
                        path=relative(member.name)
                        need(len(path.parts)>1 and path.parts[0]=="data" and member.type in (tarfile.REGTYPE,tarfile.AREGTYPE) and not member.linkname and
                             member.sparse is None and not any(k.startswith("GNU.sparse") for k in member.pax_headers),"Nonregular, sparse, linked or escaping TAR member")
                        name=PurePosixPath(*path.parts[1:]).as_posix()
                        need(name in members and name not in seen and type(member.size) is int and member.size==members[name]["bytes"],"Extra, duplicate or wrong-size literal data member")
                        write_member(root_fd,name,member,stream,members[name]);seen.add(name);count+=1
                    # tarfile stops at an end marker; require only zero padding
                    # afterward and consume gzip to its checked CRC/footer.
                    tail=0
                    while block:=stream.fileobj.read(1024**2):
                        need(not any(block),"Unexpected data after the TAR end marker");tail+=len(block)
                    need(tail>=512 and tail%512==0,"Missing complete TAR end padding")
                decompressed+=bounded.total
            need(count==archives[Path(p["path"]).name]["members"],"Missing exact archive member")
            check(p);completed.append({**p,"members":count})
            print(json.dumps({"asset":Path(p["path"]).name,"members_read_back":count}),flush=True)
        need(seen==set(members) and len(seen)==expected["members"],"Incomplete exact global data union")
        for p in inputs:check(p)
        result={"schema":"finite-box-extraction-v1","status":"COMPLETE_EXACT_DATA_UNION","data_root":str(data),"archives":completed,
                "inputs":inputs,"files":[members[k] for k in sorted(members)],"members":len(seen),"expanded_bytes":expected["expanded_bytes"],
                "all_members_read_back":True,"extracted_files_mode":"0444","mathematical_checks_executed":False}
        with receipt.open("xb") as out:out.write(encoded(result)+b"\n");out.flush();os.fsync(out.fileno())
        return {"status":result["status"],"data_root":str(data),"members":len(seen),"receipt":pin(receipt),"mathematical_checks_executed":False}
    finally:os.close(root_fd)

def run(assets,data,module_root=None):
    root=plain(module_root or Path(__file__).parent);cfg,cp=config(root)
    own=bound(root,cfg["tools"]["extract_assets"],"extract_assets.py")
    ap=bound(root,cfg["assets"]["catalog"],"DATA-ASSETS.json")
    sp=bound(root,cfg["metadata"]["source_manifest"],"code/metadata/source_manifest.json")
    expected={k:cfg["assets"][k] for k in ("count","members","expanded_bytes")}
    return extract(assets,data,decode(Path(ap["path"]).read_bytes()),decode(Path(sp["path"]).read_bytes()),expected,[cp,own,ap,sp])
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--assets",type=Path,required=True);p.add_argument("--data",type=Path,required=True)
    a=p.parse_args(argv)
    try:result=run(a.assets,a.data);print(json.dumps(result,sort_keys=True),flush=True);return 0
    except (OSError,ValueError,KeyError,TypeError,tarfile.TarError,EOFError) as error:
        print(json.dumps({"status":"EXTRACTION_REFUSED","error":f"{type(error).__name__}: {error}","mathematical_checks_executed":False}),file=sys.stderr,flush=True);return 2

if __name__=="__main__":raise SystemExit(main())
