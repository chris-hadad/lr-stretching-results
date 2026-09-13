"""Portable F025 custody utilities. No mathematical work at import."""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SCHEMA='portable-f025-replay-v1'
BASE='namespaces/base/methods/frontier-025-2026-09-10'
PREMISES=[
 'The ordinary LR/full integral hive identity, LR stretching polynomiality, and saturation.',
 'The previously accepted rank-at-most-five coefficient theorem and the exact supplied A004 family used by the census.',
 'The Horn inequality/factorization theorem; finite Horn index multiplicities are checked here.',
 'The short-normal coefficient theorem, closed-chamber transfer, and BV valuation on correct saturated quotient lattices.',
 'A single scalar product applies to an entire polytope for a given coefficient; lower-dimensional members and nonsimplicial valuations retain the source proof qualifications.',
 'F025 alone leaves the literal residual to the later box-theorem proof. This replay does not accept the whole box theorem.'
]
class Invalid(ValueError):pass
def need(ok,message):
 if not ok:raise Invalid(message)
def encoded(z):return json.dumps(z,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def decode(b):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'Duplicate JSON field');out[k]=v
  return out
 def bad(x):raise Invalid('Nonfinite JSON: '+x)
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def plain(path):
 p=Path(path).absolute();need(not any(x.is_symlink() for x in (p,*p.parents)),'Symlink path refused: '+str(p));return p.resolve()
def relative(name):
 need(type(name) is str and name and '\\' not in name and ':' not in name and all(ord(c)>=32 and ord(c)!=127 for c in name),'Invalid relative path')
 p=Path(name);need(not p.is_absolute() and str(p)==name and not any(x in ('.','..') for x in p.parts),'Escaping/noncanonical relative path');return name
def pin(path):
 p=plain(path);need(p.is_file(),'Missing regular file: '+str(p));before=p.stat();h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024**2),b''):h.update(b)
 after=p.stat();fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 need(fields(before)==fields(after),'Changed while hashing: '+str(p))
 return {'path':str(p),'bytes':before.st_size,'sha256':h.hexdigest()}
def check(p):need(pin(p['path'])==p,'Changed bound file: '+p['path'])
def read(path):return decode(plain(path).read_bytes())
def save(path,value):
 with plain(path).open('xb') as f:f.write(encoded(value)+b'\n');f.flush();os.fsync(f.fileno())
def code_pins():
 result=[pin(HERE/name) for name in ('common.py','phases.py','upstream.py','build_runtime.py','SOURCE-MAP.json','RUNTIME-MAP.json','INPUT-REQUIREMENTS.json')]
 original=read(HERE/'SOURCE-MAP.json');runtime=read(HERE/'RUNTIME-MAP.json')
 need(original['schema']=='portable-f025-originals-v1' and runtime['schema']=='portable-f025-runtime-v1','Wrong code maps')
 seen=set()
 for row in [*original['copies'],*runtime['files']]:
  name=relative(row['path']);need(name not in seen,'Duplicate code identity');seen.add(name)
  p=pin(HERE/name);need((p['bytes'],p['sha256'])==(row['bytes'],row['sha256']),'Changed preserved/adapted source');result.append(p)
 return result
def module(name):
 paths={'masks':'verification/box/verify_masks_v1.py','mask_model':'verification/box/mask_model_v1.py',
        'inputs':'verification/box/prepare_box_inputs_v1.py','small_charts':'verification/box/prepare_small_charts_v1.py',
        'quartic_charts':'verification/box/prepare_quartic_charts_v1.py','small_fit':'verification/box/fit_small_v1.py',
        'quartic_fit':'verification/box/fit_quartics_v1.py','small_cert':'verification/box/reconcile_small_v1.py',
        'quartic_cert':'verification/box/reconcile_quartics_v1.py','metric_bind':'verification/box/bind_metric_masks_v1.py',
        'cover':'verification/box/apply_global_cover_v1.py','small_join':'verification/check_r3_corrections_v1.py',
        'cones':'verification/local-cones/check_local_cones.py'}
 need(name in paths,'Unallowlisted mathematical module')
 root=HERE/'runtime'
 for path in (root,root/'verification/box'):
  if str(path) not in sys.path:sys.path.insert(0,str(path))
 import slr_ehrhart
 need(Path(slr_ehrhart.__file__).resolve()==root/'slr_ehrhart/__init__.py','Historical package initializer was selected')
 path=root/paths[name];key='portable_f025_'+name
 if key in sys.modules:return sys.modules[key]
 spec=importlib.util.spec_from_file_location(key,path);m=importlib.util.module_from_spec(spec);sys.modules[key]=m;spec.loader.exec_module(m);return m
def supervisor():
 path=HERE/'originals/portable_run.py';spec=importlib.util.spec_from_file_location('f025_owned_supervisor',path)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class Inputs:
 def __init__(self,data,manifest,expected_sha):
  self.root=plain(data);self.manifest=pin(manifest);need(self.manifest['sha256']==expected_sha,'Input manifest changed')
  doc=read(manifest);need(doc.get('schema')=='early-input-manifest-v1','Expected complete relative input manifest')
  self.files={};self.used={}
  for row in doc['files']:
   need(set(row)=={'path','bytes','sha256'},'Malformed input declaration');name=relative(row['path'])
   need(name not in self.files and type(row['bytes']) is int and row['bytes']>=0
        and type(row['sha256']) is str and len(row['sha256'])==64 and set(row['sha256'])<=set('0123456789abcdef'),'Duplicate/invalid input declaration')
   self.files[name]={'bytes':row['bytes'],'sha256':row['sha256']}
  self.requirements={r['role']:r for r in read(HERE/'INPUT-REQUIREMENTS.json')['files']}
 def declared(self,name):
  name=relative(name);need(name in self.files,'Missing portable input declaration: '+name)
  return {'path':str(self.root/name),**self.files[name]}
 def path(self,name):
  p=self.declared(name);check(p);self.used[name]=p;return Path(p['path'])
 def role(self,name):
  r=self.requirements[name];target=relative(r['target']);need(target.startswith('data/'),'Invalid frozen data target')
  name=target[5:];p=self.declared(name)
  need((p['bytes'],p['sha256'])==(r['bytes'],r['sha256']),'Role differs from exact original source: '+r['role'])
  return self.path(name)
 def after(self):
  check(self.manifest)
  for p in self.used.values():check(p)
