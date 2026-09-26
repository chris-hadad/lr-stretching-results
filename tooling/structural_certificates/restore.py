#!/usr/bin/env python3
"""Restore and independently verify the public normal/mask certificate asset."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time
import zipfile

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'DATA-ASSET.json'
SCHEMA = 'structural-certificates-data-v1'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def safe_name(name):
    need(isinstance(name, str) and name and '\\' not in name and '\x00' not in name,
         'unsafe archive member name')
    path = PurePosixPath(name)
    need(not path.is_absolute() and path.as_posix() == name and len(path.parts) > 1
         and path.parts[0] in ('packet', 'f025') and '..' not in path.parts,
         'unsafe archive member: ' + name)
    return path


def validate_manifest(manifest):
    need(manifest.get('schema') == SCHEMA and manifest.get('version') == 'normal-mask-2026-09-25-v1',
         'wrong data asset schema or version')
    files = manifest['files']
    need(type(files) is dict and len(files) == manifest['file_count'] == 10456,
         'incomplete data file declaration')
    need(sum(spec['bytes'] for spec in files.values()) == manifest['uncompressed_bytes'] == 269680674,
         'wrong complete byte total')
    for name, spec in files.items():
        safe_name(name)
        need(type(spec['bytes']) is int and spec['bytes'] >= 0
             and re.fullmatch('[0-9a-f]{64}', spec['sha256']) is not None,
             'invalid file binding: ' + name)
        provenance = spec['provenance']
        need(provenance['repository'] == 'stretched-lr-research', 'invalid source repository')
        source = PurePosixPath(provenance['path'])
        need(not source.is_absolute() and source.as_posix() == provenance['path']
             and '..' not in source.parts, 'absolute/escaping source provenance')
    archive = manifest['archive']
    need(archive['name'] == 'structural-certificates-data-v1.zip'
         and archive['format'] == 'deterministic ZIP_STORED'
         and type(archive['bytes']) is int and 0 < archive['bytes'] < 2**31
         and re.fullmatch('[0-9a-f]{64}', archive['sha256']) is not None,
         'invalid archive binding')
    return files, archive


def validate_members(archive, files):
    members = archive.infolist()
    names = [member.filename for member in members]
    need(len(names) == len(files) and len(set(names)) == len(names) and set(names) == set(files),
         'missing, duplicate or unexpected archive member')
    for member in members:
        name = member.filename
        safe_name(name)
        need(not member.is_dir() and not member.flag_bits & 1
             and member.compress_type == zipfile.ZIP_STORED,
             'directory, encrypted or compressed member: ' + name)
        mode = (member.external_attr >> 16) & 0o170000
        need(mode == stat.S_IFREG, 'nonregular archive member: ' + name)
        binding = files[name]
        need(member.file_size == binding['bytes'] and member.compress_size == binding['bytes'],
             'changed member size: ' + name)
    return members


def archive_path(archives_root, binding):
    root = Path(archives_root).resolve(strict=True)
    need(root.is_dir(), 'archive directory required')
    path = root / binding['name']
    need(path.is_file() and not path.is_symlink(), 'missing or linked data archive')
    need(path.stat().st_size == binding['bytes'] and sha(path) == binding['sha256'],
         'changed data archive bytes')
    return root, path


def check_destination(out, archives_root):
    out = Path(out).resolve()
    need(not out.exists() and not out.is_symlink() and out.parent.is_dir(),
         'fresh output and existing parent required')
    for source in (HERE.resolve(), Path(archives_root).resolve()):
        need(not (out.is_relative_to(source) or source.is_relative_to(out)),
             'output overlaps source or archive root')
    return out


def copy_checked_member(archive, member, target, binding):
    temporary = target.with_name(target.name + '.partial')
    need(not target.exists() and not temporary.exists(), 'occupied member: ' + member.filename)
    digest = hashlib.sha256()
    count = 0
    with archive.open(member, 'r') as source, temporary.open('xb') as destination:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            count += len(block)
            need(count <= binding['bytes'], 'oversized member: ' + member.filename)
            digest.update(block)
            destination.write(block)
    need(count == binding['bytes'] and digest.hexdigest() == binding['sha256'],
         'corrupt member: ' + member.filename)
    os.replace(temporary, target)


def restore(archives_root, out, files, binding):
    out = check_destination(out, archives_root)
    root, path = archive_path(archives_root, binding)
    with zipfile.ZipFile(path, 'r', allowZip64=False) as archive:
        members = validate_members(archive, files)
        out.mkdir()
        completed = set()
        status, reason = 'FAILED_OR_PARTIAL', None
        started = time.monotonic()
        try:
            for member in members:
                name = member.filename
                target = out.joinpath(*safe_name(name).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                copy_checked_member(archive, member, target, files[name])
                completed.add(name)
            need(completed == set(files), 'incomplete restored data union')
            status = 'PASS_COMPLETE_RESTORATION'
        except BaseException as error:
            reason = repr(error)
            raise
        finally:
            report = {'schema': 'structural-certificates-restoration-v1', 'status': status,
                      'reason': reason, 'files_completed': len(completed),
                      'files_required': len(files),
                      'bytes_completed': sum(files[name]['bytes'] for name in completed),
                      'manifest_sha256': sha(MANIFEST), 'archive_sha256': binding['sha256'],
                      'seconds': round(time.monotonic() - started, 3),
                      'mathematical_validity_asserted': False}
            (out / 'RESTORE.json').write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    return report


def verify(out, files):
    root = Path(out).resolve(strict=True)
    need(root.is_dir(), 'restored data directory required')
    seen = set()
    for path in root.rglob('*'):
        need(not path.is_symlink(), 'linked restored member')
        if path.is_dir():
            continue
        name = path.relative_to(root).as_posix()
        if name == 'RESTORE.json':
            continue
        safe_name(name)
        need(name in files and name not in seen, 'unexpected or repeated restored member: ' + name)
        binding = files[name]
        need(path.stat().st_size == binding['bytes'] and sha(path) == binding['sha256'],
             'missing/corrupt restored member: ' + name)
        seen.add(name)
    need(seen == set(files), 'missing restored data members')
    return {'status': 'PASS_COMPLETE_REHASH', 'files': len(seen),
            'bytes': sum(files[name]['bytes'] for name in seen),
            'manifest_sha256': sha(MANIFEST)}


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for certificate data verification')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('inspect', 'restore', 'verify'))
    parser.add_argument('--archives', type=Path, help='directory holding the downloaded ZIP')
    parser.add_argument('--out', type=Path, help='fresh restore output or existing verified data')
    args = parser.parse_args()
    files, binding = validate_manifest(json.loads(MANIFEST.read_text()))
    if args.command == 'verify':
        need(args.out is not None, '--out is required')
        result = verify(args.out, files)
    else:
        need(args.archives is not None, '--archives is required')
        if args.command == 'inspect':
            _, path = archive_path(args.archives, binding)
            with zipfile.ZipFile(path, 'r', allowZip64=False) as archive:
                validate_members(archive, files)
            result = {'status': 'PASS_COMPLETE_ARCHIVE', 'files': len(files),
                      'archive_sha256': binding['sha256']}
        else:
            need(args.out is not None, '--out is required')
            result = restore(args.archives, args.out, files, binding)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
