"""Literal whole-tableau controls of the accepted paired-interface theorem."""
from fractions import Fraction as F
from itertools import combinations
import math,json,sys
def widths(b):
 la,mu,nu=[b[i:i+6] for i in [0,6,12]];lower=[max(mu[i],la[i+1] if i<5 else 0) for i in range(6)];upper=[la[0]]+[min(la[i],mu[i-1]) for i in range(1,6)]
 C=sum(max(0,la[i+1]-mu[i]) for i in range(5));return [u-l for u,l in zip(upper,lower)],nu[1]-C


def coeff(w,k):
 return F(k)*sum(F(1,i) for i in range(1,5))-sum(F(max(0,k-sum(w[i] for i in J)),j*math.comb(4,j)) for j in range(1,5) for J in combinations(range(6),j))


def overlap(X,Y):
 w,k=X;v,l=Y;terms=[]
 for j in range(1,5):
  for J in combinations(range(6),j):
   a=k-sum(w[i] for i in J);b=l-sum(v[i] for i in J);terms.append(F(max(a,0)+max(b,0)-max(a+b,0),j*math.comb(4,j)))
 assert all(x>=0 for x in terms);return terms


def transport(b,c):
 X=widths(b);Y=widths(c);eps=[max(0,b[i+1]-b[i+6])+max(0,c[i+1]-c[i+6])-max(0,b[i+1]+c[i+1]-b[i+6]-c[i+6]) for i in range(5)]
 w=[a+z for a,z in zip(X[0],Y[0])];k=X[1]+Y[1];terms=overlap(X,Y)
 for i,e in enumerate(eps):
  v=[0]*6;v[i]=v[i+1]=e;assert coeff(v,e)==0
  terms+=overlap((w,k),(v,e));w=[a+z for a,z in zip(w,v)];k+=e
 assert (w,k)==widths([a+z for a,z in zip(b,c)])
 assert coeff(w,k)-coeff(*X)-coeff(*Y)==sum(terms)
 return eps,terms


def count(b,t):
 la,mu,nu=[[t*x for x in b[i:i+6]] for i in [0,6,12]]
 if sum(la)!=sum(mu)+sum(nu) or any(a<b for a,b in zip(la,mu)):return 0
 cells=[(i,j) for i in range(6) for j in range(la[i],mu[i],-1)];filled={};used=[0]*6;answer=0
 def visit(pos):
  nonlocal answer
  if pos==len(cells):
   if used==nu:answer+=1
   return
  i,j=cells[pos];right=filled.get((i,j+1),6);above=filled.get((i-1,j),0)
  for a in range(above+1,right+1):
   k=a-1
   if used[k]>=nu[k] or (k and used[k]+1>used[k-1]):continue
   used[k]+=1;filled[i,j]=a;visit(pos+1);used[k]-=1;del filled[i,j]
 visit(0);return answer


def main():
 if sys.flags.optimize:
  raise RuntimeError('Optimized Python is refused for linear-coefficient two-row controls')
 b=[10,9,8,6,4,3,8,7,5,4,2,0,8,6,0,0,0,0];r=[1,1,0,0,0,0]*2+[0]*6;upper=[a+c for a,c in zip(b,r)];eps,terms=transport(b,r)
 expected=[[F(1),F(7,3),F(2),F(2,3)],[F(1),F(13,4),F(37,8),F(13,4),F(7,8)]];counts=[]
 for parent,pol in zip([b,upper],expected):
  values=[count(parent,t) for t in range(7)];assert values==[sum(c*t**i for i,c in enumerate(pol)) for t in range(7)];counts.append(values)
 assert sum(terms)==F(11,12) and coeff(*widths(upper))-coeff(*widths(b))==F(11,12)
 mu=[2,2,1,1,0,0];nu=[3,2,1,0,0,0];ca=[4,4,2,2,0,0]+mu+nu;cb=[3,3,2,2,1,1]+mu+nu
 assert widths(ca)==widths(cb)
 three=[[count(parent,t) for t in range(13)] for parent in [ca,cb]];assert three==[[1]*13,list(range(1,14))]
 left=[2,2,1,1,0,0,1,1,0,0,0,0,2,2,0,0,0,0];right=[2,1,1,0,0,0]*2+[0]*6
 e2,t2=transport(left,right);assert e2==[1,0,1,0,0] and sum(t2)==1
 controls={'changed_original_content':count(b[:-12]+b[6:12]+[7,6,0,0,0,0],1)==0,'omitted_interface_correction':sum(terms)!=0,'three_label_width_collapse':three[0]!=three[1]}
 assert all(controls.values())
 print(json.dumps({'status':'PASS','whole_counts':counts,'three_label_counts':three,'sharp_gain':'1','coefficient_gain':'11/12','negative_controls':controls}))

if __name__=='__main__':main()
