#!/usr/bin/env python3
"""Authenticate and restore the complete versioned 4-by-5 companion data."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tarfile
import time

HERE = Path(__file__).resolve().parent
VERSION = 'transport-four-by-five-2026-09-25-v1'
SCHEMA = 'transport-four-by-five-data-assets-v1'
MATHEMATICAL_MANIFEST_SHA256 = '06133ae7c50c8e2bcb0e3a342fe8b99db6712ac3c0083b23372cec7e6445d582'
FILE_COUNT = 47
ASSET_MAX_BYTES = 2 ** 31


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + str(key))
        result[key] = value
    return result


def regular(path):
    path = Path(path)
    need(not path.is_symlink() and path.exists(), 'missing or symlink input: ' + str(path))
    need(stat.S_ISREG(path.stat().st_mode), 'ordinary input file required: ' + str(path))
    return path


def read_json(path):
    return json.loads(regular(path).read_text(), object_pairs_hook=unique_object)


def safe_name(name):
    need(type(name) is str and re.fullmatch(r'[A-Za-z0-9_.\-/]+', name) is not None,
         'unsafe data path: ' + str(name))
    path = PurePosixPath(name)
    need(not path.is_absolute() and '..' not in path.parts
         and path.as_posix() == name and name not in ('', '.') and not name.endswith('/'),
         'unsafe data path: ' + name)
    return path


def disjoint(left, right):
    return left != right and left not in right.parents and right not in left.parents


def bindings(assets_path, math_path, *, required_math_sha256=MATHEMATICAL_MANIFEST_SHA256):
    """The CLI pins the original mathematical manifest; tiny tests pass their own pin."""
    need(sha(regular(math_path)) == required_math_sha256, 'changed mathematical manifest')
    mathematical = read_json(math_path)
    need(mathematical['schema'] == 'complete-transport-4x5-companion/v1', 'mathematical schema')
    files = mathematical['files']
    need(type(files) is dict and len(files) == mathematical['file_count'] == FILE_COUNT,
         'complete 47-file mathematical declaration required')
    for name, spec in files.items():
        safe_name(name)
        need(type(spec) is dict and set(spec) == {'bytes', 'sha256'}, 'file binding keys')
        need(type(spec['bytes']) is int and spec['bytes'] >= 0
             and type(spec['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', spec['sha256']),
             'invalid mathematical file binding: ' + name)
    total = sum(spec['bytes'] for spec in files.values())
    need(mathematical['bytes'] == total, 'mathematical byte total')
    assets = read_json(assets_path)
    need(assets['schema'] == SCHEMA and assets['version'] == VERSION, 'asset schema or version')
    expected_math = assets['mathematical_manifest']
    need(expected_math == {'name': 'DATA-MANIFEST.json', 'bytes': Path(math_path).stat().st_size,
                           'sha256': required_math_sha256}, 'mathematical manifest binding')
    need(assets['file_count'] == FILE_COUNT and assets['uncompressed_bytes'] == total,
         'asset mathematical totals')
    archives = assets['archives']
    need(type(archives) is list and archives, 'archive roster required')
    names = []
    members = []
    for archive in archives:
        name = archive['name']
        need(type(name) is str and re.fullmatch(
            r'transport-four-by-five-data-2026-09-25-v1(?:-[0-9]{2})?\.tar\.gz', name),
            'archive filename')
        names.append(name)
        need(type(archive['bytes']) is int and 0 < archive['bytes'] < ASSET_MAX_BYTES
             and type(archive['sha256']) is str
             and re.fullmatch(r'[0-9a-f]{64}', archive['sha256']), 'archive byte/hash binding')
        need(type(archive['files']) is list and archive['files'], 'empty archive member roster')
        for member in archive['files']:
            safe_name(member)
        members.extend(archive['files'])
    need(len(names) == len(set(names)), 'duplicate archive name')
    need(len(members) == len(set(members)) and set(members) == set(files),
         'missing, unexpected or repeated declared member')
    return files, archives, assets


def restore(archives_root, out, assets_path, math_path, *, source_roots=(),
            required_math_sha256=MATHEMATICAL_MANIFEST_SHA256):
    raw_out = Path(out)
    need(not raw_out.exists() and not raw_out.is_symlink(), 'output already exists')
    archives_root = Path(archives_root).resolve(strict=True)
    need(archives_root.is_dir(), 'archive directory required')
    out = raw_out.resolve()
    need(out.parent.is_dir(), 'output parent must already exist')
    protected = [HERE, archives_root, Path(assets_path).resolve().parent,
                 Path(math_path).resolve().parent]
    protected.extend(Path(root).resolve(strict=True) for root in source_roots)
    need(all(disjoint(out, root) for root in protected),
         'output overlaps a source, manifest or archive root')
    files, archives, assets = bindings(assets_path, math_path,
                                     required_math_sha256=required_math_sha256)
    # Every compressed asset is authenticated before creating the output.
    for archive in archives:
        path = regular(archives_root / archive['name'])
        need(path.stat().st_size == archive['bytes'] and sha(path) == archive['sha256'],
             'changed archive: ' + archive['name'])
    out.mkdir()
    done = set()
    started = time.monotonic()
    status = 'FAILED_OR_PARTIAL'
    reason = None
    try:
        for archive in archives:
            wanted = set(archive['files'])
            seen = set()
            with tarfile.open(archives_root / archive['name'], 'r|gz') as stream:
                for member in stream:
                    rel = safe_name(member.name)
                    need(member.isreg() and not member.issparse() and not member.pax_headers
                         and member.offset_data - member.offset == 512,
                         'only plain regular archive files are accepted')
                    name = member.name
                    need(name in wanted and name not in seen and name not in done,
                         'unexpected or duplicate archive member: ' + name)
                    expected = files[name]
                    need(member.size == expected['bytes'], 'wrong member size: ' + name)
                    target = out / Path(*rel.parts)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    temporary = target.with_name(target.name + '.partial')
                    need(not target.exists() and not target.is_symlink()
                         and not temporary.exists() and not temporary.is_symlink(),
                         'occupied member destination: ' + name)
                    incoming = stream.extractfile(member)
                    need(incoming is not None, 'missing member stream: ' + name)
                    digest = hashlib.sha256()
                    count = 0
                    with temporary.open('xb') as destination:
                        for block in iter(lambda: incoming.read(1024 * 1024), b''):
                            count += len(block)
                            need(count <= expected['bytes'], 'oversized member: ' + name)
                            destination.write(block)
                            digest.update(block)
                        destination.flush()
                        os.fsync(destination.fileno())
                    need(count == expected['bytes'] and digest.hexdigest() == expected['sha256'],
                         'wrong member hash: ' + name)
                    os.replace(temporary, target)
                    seen.add(name)
                    done.add(name)
            need(seen == wanted, 'omitted archive members: ' + archive['name'])
        need(done == set(files), 'incomplete mathematical data union')
        status = 'PASS_COMPLETE_RESTORATION'
    except BaseException as error:
        reason = repr(error)
        raise
    finally:
        report = {'schema': 'transport-four-by-five-data-restoration-v1', 'version': VERSION,
                  'status': status, 'reason': reason, 'files_completed': len(done),
                  'files_required': FILE_COUNT,
                  'bytes_completed': sum(files[name]['bytes'] for name in done),
                  'seconds': time.monotonic() - started,
                  'mathematical_manifest_sha256': required_math_sha256,
                  'assets_manifest_sha256': sha(assets_path),
                  'mathematical_validity_asserted': False}
        with (out / 'RESTORE.json').open('x') as destination:
            json.dump(report, destination, indent=2)
            destination.write('\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archives', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True, help='fresh output outside source/archive roots')
    parser.add_argument('--assets-manifest', type=Path, default=HERE / 'DATA-ASSETS.json')
    parser.add_argument('--math-manifest', type=Path, default=HERE / 'DATA-MANIFEST.json')
    parser.add_argument('--source-root', type=Path, action='append', default=[],
                        help='additional uncompressed source roots to protect during publisher roundtrips')
    args = parser.parse_args()
    try:
        report = restore(args.archives, args.out, args.assets_manifest, args.math_manifest,
                         source_roots=args.source_root)
    except (ValueError, OSError, KeyError, TypeError, EOFError, tarfile.TarError) as error:
        print('RESTORE_REFUSED: ' + str(error), file=sys.stderr)
        return 2
    print(json.dumps(report), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
