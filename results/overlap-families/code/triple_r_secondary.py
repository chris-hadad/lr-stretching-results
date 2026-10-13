"""Independent complete primitive organizer; exact Fraction arithmetic only."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import json,sys,time,hashlib

def add(a,b,scale=1):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,Q(0))+scale*v
 return {k:v for k,v in c.items() if v}
def mul(a,b):
 c={}
 for (i,j),x in a.items():
  for (k,l),y in b.items():c[i+k,j+l]=c.get((i+k,j+l),Q(0))+x*y
 return {k:v for k,v in c.items() if v}
@lru_cache(None)
def rising(index,variable,offset):
 if index<0:return {}
 p={(0,0):Q(1)}
 for j in range(index):
  factor={(0,0):Q(offset+j,j+1),(1,0) if variable=='A' else (0,1):Q(1,j+1)}
  p=mul(p,factor)
 return p
@lru_cache(None)
def primitive(a,m):
 if a<0 or m<-1 or m>=a:return {}
 if m==-1:return rising(a,'A',1)
 return add(mul(rising(a,'A',1),rising(m+1,'z',0)),mul(rising(m,'A',2),add(rising(a+1,'z',0),rising(a,'z',0),-1)),-1)
def derivative(p,var=1):
 out={}
 for (a,b),v in p.items():
  if var==1 and b:out[a,b-1]=b*v
  if var==0 and a:out[a-1,b]=a*v
 return out
def substitute(p):
 out={}
 for (a,b),v in p.items():
  for i in range(a+1):out[i,a-i+b]=out.get((i,a-i+b),Q(0))+v*comb(a,i)
 return {k:v for k,v in out.items() if v}
def length(lo,hi):return max(0,hi-lo+1)
def bands(k,l,m,s):
 alpha=k+l
 B=length(max(0,s-m),min(k,s,alpha-s))
 U=length(max(0,s-m+1),min(k,s,alpha-s-1))
 V=length(max(0,s-m),min(k-1,s,alpha-s-1))
 W=length(max(0,s-m+1),min(k-1,s,alpha-s-2))
 return B,U+V,W
@lru_cache(None)
def entire(n,idx,drop_W=False):
 k,l,m=idx;K=k+l+m;p={}
 for s in range(K+2):
  B,C,W=bands(k,l,m,s);N=n-s;M=n-K+s
  for scale,a in [(B,N),(-C,N-1),(0 if drop_W else W,N-2)]:
   if scale:p=add(p,primitive(a,M-1),scale)
 return p

def reduce(n,idx):
 idx=list(idx);steps=[]
 while True:
  idx.sort()
  if min(idx)<0 or max(idx)>n:return {'zero':True,'n':n,'idx':idx,'steps':steps}
  if n==0:return {'constant':True,'n':n,'idx':idx,'steps':steps}
  pair=next(((i,j) for i in range(3) for j in range(i+1,3) if idx[i]+idx[j]>n),None)
  if pair is None:return {'n':n,'idx':idx,'steps':steps}
  i,j=pair;a,b=idx[i],idx[j];old=n;n=2*n-a-b;idx[i]=old-b;idx[j]=old-a
  steps.append({'from_n':old,'pair':[a,b],'to_n':n,'idx':list(idx)})
  assert n<old

def encoded(p):return [[a,b,str(v)] for (a,b),v in sorted(p.items())]
def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);nmax=int(sys.argv[2]);start=time.monotonic();rows=[];controls=[];canonical_small=[]
 for n in range(1,nmax+1):
  for idx in combinations_with_replacement(range(n+1),3):
   E=entire(n,idx);F=substitute(derivative(E));d=2*n-sum(idx);red=reduce(n,idx)
   if red.get('zero'):assert not E,(n,idx,'reflection zero')
   else:
    E2=entire(red['n'],tuple(red['idx']))
    assert E==E2,(n,idx,'complete reflection')
   if not red.get('zero') and not red.get('constant'):
    nr=red['n'];ir=red['idx'];assert 2*nr-sum(ir)==d and nr<=2*d
    if d<=4:
     assert nr<=8 and all(v>=0 for v in F.values())
     if nr==n and list(idx)==ir:canonical_small.append([n,list(idx),d,len(F)])
    if max(ir)<nr and d>=2:
     assert max(a+b for a,b in F)==d-1
     assert all(v>=0 for (a,b),v in F.items() if a+b>=d-2)
   if not controls and entire(n,idx,True)!=E:controls.append({'mutation':'omit complete W contribution','n':n,'indices':idx,'changes_whole_primitive':True})
   rows.append({'n':n,'indices':idx,'deficit':d,'primitive':encoded(E),'derivative':encoded(F),'reflection':red})
 # Freeze independently reconstructed complete outputs BEFORE reading the primary fields.
 secondary={'schema':'a83-triple-r-secondary/v1','nmax':nmax,'records':rows,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 sp=out/'SECONDARY-FIELDS.json';sp.write_text(json.dumps(secondary,indent=2)+'\n')
 frozen={'path':str(sp),'bytes':sp.stat().st_size,'sha256':hashlib.sha256(sp.read_bytes()).hexdigest()}
 (out/'SECONDARY-FREEZE.json').write_text(json.dumps(frozen,indent=2)+'\n')
 primary_path=Path(sys.argv[3]);primary=json.loads(primary_path.read_text());lookup={(r['n'],tuple(r['indices'])):r for r in primary['records']}
 assert len(lookup)==len(rows)
 for r in rows:assert r['derivative']==lookup[r['n'],tuple(r['indices'])]['complete_nonzero_coefficients'],(r['n'],r['indices'],'independent mismatch')
 right=substitute(derivative(entire(1,(0,0,0))))
 wrong=add(right,substitute(derivative(entire(1,(0,0,0)),0)))
 assert right!=wrong
 controls.append({'mutation':'differentiate holding x fixed','n':1,'indices':[0,0,0],'correct':encoded(right),'wrong':encoded(wrong)})
 # Negative adjacent pair is retained with its whole terminal compensation.
 def chain(n,k,l):
  p=primitive(n,n-k-l-1)
  for i in range(min(k,l)):
   p=add(p,primitive(n-1-i,n+i-k-l));p=add(p,primitive(n-1-i,n+i-k-l-1),-1)
  return p
 pair=add(chain(3,2,1),chain(2,1,1),-1);terminal=chain(2,0,1)
 dp=substitute(derivative(pair));dt=substitute(derivative(terminal));parent=add(dp,dt)
 assert dp.get((0,0))==Q(-1,3) and dt.get((0,0))==Q(7,6) and parent==substitute(derivative(entire(3,(1,1,1))))
 controls.append({'control':'adverse full pair and actual complete terminal','paired':encoded(dp),'terminal':encoded(dt),'parent':encoded(parent)})
 summary={'schema':'a83-triple-r-secondary-checks/v1','status':'PASS','complete_fields':len(rows),'derivative_nonzero_slots':sum(len(r['derivative']) for r in rows),'whole_primitive_nonzero_slots':sum(len(r['primitive']) for r in rows),'primary':{'path':str(primary_path),'bytes':primary_path.stat().st_size,'sha256':hashlib.sha256(primary_path.read_bytes()).hexdigest()},'secondary_freeze':frozen,'all_complete_joins_equal':True,'complete_reflections_checked':len(rows),'canonical_deficit_le_four':canonical_small,'controls':controls,'new_named_originals':0,'LR_backend_calls':0,'scientific_scope':'Auxiliary exact full fields; unbounded deficit<=4 follows only with proved terminating reflection and canonical n<=2d. Top two layers require separate symbolic proof.','seconds':time.monotonic()-start}
 (out/'CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k not in ['canonical_deficit_le_four','controls']}))
if __name__=='__main__':main()
