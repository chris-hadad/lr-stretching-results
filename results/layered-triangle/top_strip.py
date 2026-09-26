"""Independent entire top-strip fields from original-equivalent convolution."""
from fractions import Fraction as F
from pathlib import Path
from math import comb,factorial
import json,sys,time

def whole(r,w,z):
 x=w+z;a=(r-1)*w+r*z;dist=[1]
 for h in [x]*r+[a]:
  new=[];window=0
  for k in range(len(dist)+2*h):
   if k<len(dist):window+=dist[k]
   if 0<=k-2*h-1<len(dist):window-=dist[k-2*h-1]
   new.append(window)
  dist=new
 return sum(v**3 for v in dist)

def falling(n):
 p=[1]
 for k in range(n):
  q=[0]*(len(p)+1)
  for i,v in enumerate(p):q[i]-=k*v;q[i+1]+=v
  p=q
 return [F(v,factorial(n)) for v in p]

def main():
 if sys.flags.optimize:
  raise RuntimeError('Optimized Python is refused for layered-triangle top strip')
 start=time.monotonic();out=Path(sys.argv[1]);results=[]
 for r in [3,4,5]:
  D=3*r+1;values=[[whole(r,i,j) for j in range(D-i+1)] for i in range(D+1)]
  N={(i,j):sum((-1)**(i+j-a-b)*comb(i,a)*comb(j,b)*values[a][b] for a in range(i+1) for b in range(j+1)) for i in range(D+1) for j in range(D-i+1)}
  basis=[falling(i) for i in range(D+1)];coeff={(i,j):F(0) for i in range(D+1) for j in range(D-i+1)}
  for (i,j),v in N.items():
   for a,x in enumerate(basis[i]):
    for b,y in enumerate(basis[j]):coeff[a,b]+=v*x*y
  assert all(v>0 for v in coeff.values()),(r,[(k,str(v)) for k,v in coeff.items() if v<=0])
  def ev(w,z):return sum(v*w**i*z**j for (i,j),v in coeff.items())
  assert all(ev(i,j)==values[i][j] for i in range(D+1) for j in range(D-i+1))
  hold=[(D+1,0),(0,D+1),(D+1,1),(1,D+1),(D//2+1,D//2+2),(D+1,D+2)]
  holdouts=[]
  for i,j in hold:
   v=whole(r,i,j);assert ev(i,j)==v;holdouts.append({'w':i,'z':j,'count':v})
  results.append({'r':r,'degree_bound_proved_before_determination':D,'coordinates':'b=w+z, A=(r-1)w+r z','determining_counts':values,'complete_coefficients':[[i,j,str(v)] for (i,j),v in coeff.items()],'complete_Newton_coefficients':[[i,j,v] for (i,j),v in N.items()],'holdouts':holdouts})
 result={'schema':'astra053-independent-topstrip-base/v1','fields':results,'slots':sum(len(x['complete_coefficients']) for x in results),'holdouts':18,'provider_code_executed':False,'claim':'Complete exact fields conditional on original map and explicit total-degree theorem','seconds':time.monotonic()-start}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'slots':result['slots'],'holdouts':18,'seconds':result['seconds']}))
if __name__=='__main__':main()
