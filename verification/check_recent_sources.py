"""Byte authentication for one curated recent module, not theorem verification."""
import argparse,hashlib,json,pathlib
MODULES=('two-row-inner','transportation-developments','overlap-families','root-square','four-letter','research-progress')
def verify(root,manifest=None):
 manifest=json.loads((root/'SOURCE-MAP.json').read_text()) if manifest is None else manifest
 rows=manifest['files'];names=[row['path'] for row in rows]
 if len(set(names))!=len(names):raise ValueError('duplicate manifest member')
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='SOURCE-MAP.json' and '__pycache__' not in p.parts}
 if set(names)!=actual:raise ValueError('omitted or unexpected module file: '+repr(sorted(set(names)^actual)))
 for row in rows:
  rel=pathlib.Path(row['path'])
  if rel.is_absolute() or '..' in rel.parts:raise ValueError('unsafe manifest member')
  p=root/rel
  if p.is_symlink():raise ValueError('module symlink')
  b=p.read_bytes()
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('file size/hash mismatch: '+row['path'])
 return len(rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--module',choices=MODULES,required=True);a=p.parse_args()
 root=pathlib.Path(__file__).resolve().parents[1]/'results'/a.module
 print(json.dumps(dict(status='PASS',module=a.module,files=verify(root),scope='bytes and complete membership only')))
