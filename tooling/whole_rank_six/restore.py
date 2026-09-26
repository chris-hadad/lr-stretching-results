#!/usr/bin/env python3
"""Restore the complete versioned rank-six data, checking every byte binding."""
from __future__ import annotations
import argparse,hashlib,json,os,re,tarfile,time
from pathlib import Path,PurePosixPath

HERE=Path(__file__).resolve().parent
SCHEMA='rank-six-data-assets-v1'


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def safe_name(name):
    path=PurePosixPath(name)
    need(isinstance(name,str) and not path.is_absolute() and '..' not in path.parts
         and path.as_posix()==name and len(path.parts)>1 and path.parts[0] in ('c1','lower'),
         'unsafe mathematical data path: '+str(name))
    return path


def validate_manifest(manifest):
    need(manifest['schema']==SCHEMA and manifest['version']=='rank-six-2026-09-25-v1','data version')
    files=manifest['files'];archives=manifest['archives']
    need(len(files)==1842 and len(archives)>0,'complete data declaration')
    listed=[];names=[]
    for name,spec in files.items():
        safe_name(name)
        need(type(spec['bytes']) is int and spec['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',spec['sha256']),
             'invalid file binding: '+name)
    for spec in archives:
        name=spec['name'];names.append(name)
        need(re.fullmatch(r'rank-six-data-\d{2}\.tar\.gz',name) is not None,'archive name')
        need(type(spec['bytes']) is int and 0<spec['bytes']<2**31
             and re.fullmatch('[0-9a-f]{64}',spec['sha256']),'archive binding')
        need(isinstance(spec['files'],list) and spec['files'],'empty asset')
        listed.extend(spec['files'])
    need(len(names)==len(set(names)),'duplicate archive name')
    need(len(listed)==len(set(listed)) and set(listed)==set(files),'missing or repeated mathematical data')
    need(sum(x['bytes'] for x in files.values())==manifest['uncompressed_bytes'],'declared data total')
    return files,archives


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archives',type=Path,required=True,help='directory containing all downloaded data archives')
    ap.add_argument('--out',type=Path,required=True,help='fresh output directory, outside source and archive roots')
    args=ap.parse_args();archives_root=args.archives.resolve(strict=True);out=args.out.resolve()
    need(archives_root.is_dir(),'archive directory required')
    need(not out.exists() and out.parent.is_dir(),'fresh output and existing parent required')
    need(all(out!=p and p not in out.parents and out not in p.parents for p in (HERE,archives_root)),
         'output must be separate from source and archive roots')
    manifest_path=HERE/'DATA-ASSETS.json';manifest=json.loads(manifest_path.read_text())
    files,archives=validate_manifest(manifest);started=time.monotonic()
    # Authenticate every archive before creating any destination.
    for spec in archives:
        path=archives_root/spec['name']
        need(path.is_file() and not path.is_symlink(),'missing archive: '+spec['name'])
        need(path.stat().st_size==spec['bytes'] and sha(path)==spec['sha256'],'changed archive: '+spec['name'])
    out.mkdir();done=set();status='FAILED_OR_PARTIAL';reason=None
    try:
        for spec in archives:
            wanted=set(spec['files']);seen=set()
            with tarfile.open(archives_root/spec['name'],'r|gz') as archive:
                for member in archive:
                    name=member.name;rel=safe_name(name)
                    need(member.isreg() and not member.issparse(),'only ordinary files are accepted')
                    need(name in wanted and name not in seen and name not in done,'unexpected or repeated member: '+name)
                    expected=files[name];need(member.size==expected['bytes'],'member size: '+name)
                    target=out/Path(*rel.parts);target.parent.mkdir(parents=True,exist_ok=True)
                    temporary=target.with_name(target.name+'.partial')
                    need(not target.exists() and not temporary.exists(),'occupied member: '+name)
                    stream=archive.extractfile(member);need(stream is not None,'missing file stream')
                    digest=hashlib.sha256();count=0
                    with temporary.open('xb') as destination:
                        while True:
                            block=stream.read(1024*1024)
                            if not block:break
                            count+=len(block);need(count<=expected['bytes'],'oversized member')
                            digest.update(block);destination.write(block)
                    need(count==expected['bytes'] and digest.hexdigest()==expected['sha256'],'changed data: '+name)
                    os.replace(temporary,target);seen.add(name);done.add(name)
            need(seen==wanted,'missing archive members: '+spec['name'])
            print('RESTORED',spec['name'],len(seen),'files',flush=True)
        need(done==set(files),'incomplete data union')
        status='PASS_COMPLETE_RESTORATION'
    except BaseException as error:
        reason=repr(error);raise
    finally:
        report={'schema':'rank-six-data-restoration-v1','status':status,'reason':reason,
                'version':manifest['version'],'files_completed':len(done),'files_required':len(files),
                'bytes_completed':sum(files[n]['bytes'] for n in done),'seconds':time.monotonic()-started,
                'manifest_sha256':sha(manifest_path),'mathematical_validity_asserted':False}
        (out/'RESTORE.json').write_text(json.dumps(report,indent=2)+'\n')
    print(status)


if __name__=='__main__':main()
