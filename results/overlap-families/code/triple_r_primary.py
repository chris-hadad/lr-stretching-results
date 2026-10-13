"""Complete formal auxiliary fields. No LR original/backend is counted."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import json,time,hashlib,sys

def umul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
@lru_cache(None)
def a_shift(n):
 p=[F(1)]
 for r in range(1,n+1):p=umul(p,[F(r+1,r),F(1,r)])
 return p
@lru_cache(None)
def dr(n):
 p=[F(1)]
 for r in range(n):p=umul(p,[F(r,r+1),F(1,r+1)])
 return [F(j)*x for j,x in enumerate(p)][1:]
def smul(a,b):
 c={}
 for (i,j),x in a.items():
  for (k,l),y in b.items():c[i+k,j+l]=c.get((i+k,j+l),0)+x*y
 return {k:v for k,v in c.items() if v}
@lru_cache(None)
def rpoly(k):
 p={(i,k-i):1 for i in range(k+1)}
 if k:
  for i in range(k):p[i+1,k-i]=-1
 return p
@lru_cache(None)
def base_derivative(a,b):
 p={}
 for e,v in enumerate(a_shift(a)):
  for i in range(e+1):
   for j,w in enumerate(dr(b)):
    key=(i,e-i+j);p[key]=p.get(key,F(0))+v*comb(e,i)*w
 return {k:v for k,v in p.items() if v}
def field(n,idx):
 weight={(0,1):1,(1,0):-1}
 for i in idx:weight=smul(weight,rpoly(i))
 out={}
 for (a,b),w in weight.items():
  a=n-a;b=n+1-b
  if a<0 or b<1:continue
  for key,v in base_derivative(a,b).items():out[key]=out.get(key,F(0))+w*v
 return {k:v for k,v in out.items() if v}

def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
 nmax=int(sys.argv[2]);records=[];bad=[];start=time.monotonic()
 for n in range(1,nmax+1):
  for idx in combinations_with_replacement(range(n+1),3):
   p=field(n,idx);neg=[{'x':a,'z':b,'coefficient':str(c)} for (a,b),c in sorted(p.items()) if c<0]
   row={'n':n,'indices':idx,'complete_nonzero_coefficients':[[a,b,str(c)] for (a,b),c in sorted(p.items())],'negative':neg}
   records.append(row)
   if neg:bad.append({'n':n,'indices':idx,'negative':neg})
  print(json.dumps({'n':n,'completed_fields':len(records),'negative_fields':len(bad),'seconds':time.monotonic()-start}),flush=True)
 data={'schema':'a83-triple-r-formal-probe/v1','scope':'Every symmetric triple 0<=i<=j<=k<=n at n=1..nmax; entire physical fixed-A derivative, then A=x+z. Coefficient of (v-u)(1-u)^(-A-2)(1-v)^(-z)log(1/(1-v)) r_i r_j r_k at u^n v^(n+1). Formal auxiliaries only.','nmax':nmax,'records':records,'negative_fields':bad,'new_originals':0,'LR_backend_calls':0,'all_index_theorem':False,'seconds':time.monotonic()-start,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (out/'COMPLETE-FIELDS.json').write_text(json.dumps(data,indent=2)+'\n')
 summary={k:v for k,v in data.items() if k!='records'};summary['complete_fields']=len(records);summary['nonzero_slots']=sum(len(r['complete_nonzero_coefficients']) for r in records)
 (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary))
if __name__=='__main__':main()
