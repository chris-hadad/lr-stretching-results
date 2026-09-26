from fractions import Fraction as Q
from itertools import combinations,permutations
from math import comb

def rows():
    points = [(i,j) for i in range(1,6) for j in range(1,6-i)]
    unit = lambda i: [int(c == i) for c in range(28)]
    prefix = lambda start,k: [int(start <= c < start+k) for c in range(28)]
    h = {}
    for i in range(7):
        h[0,i] = prefix(6,i)
        h[i,0] = prefix(0,i)
    for i in range(1,6):
        h[i,6-i] = [x+y for x,y in zip(prefix(6,6),prefix(12,i))]
    for k,p in enumerate(points):
        h[p] = unit(18+k)
    result = []
    for i in range(5):
        for j in range(5-i):
            terms = [([(i+1,j),(i,j+1)],[(i,j),(i+1,j+1)]),
                     ([(i+1,j),(i+1,j+1)],[(i+2,j),(i,j+1)]),
                     ([(i,j+1),(i+1,j+1)],[(i+1,j),(i,j+2)])]
            for plus,minus in terms:
                result.append([sum(h[p][c] for p in plus)-sum(h[p][c] for p in minus) for c in range(28)])
    for start in (0,6,12):
        for i in range(6):
            r = unit(start+i)
            if i < 5:
                r[start+i+1] = -1
            result.append(r)
    return result

def dot(a,b):
 assert len(a)==len(b)
 return sum((Q(x)*Q(y) for x,y in zip(a,b)),Q(0))


def cuts():
 out=[]
 for k in range(1,6):
  for U in combinations(range(5),k):
   for I in combinations(range(6),k):
    for J in combinations(range(6),k):
     a=[0]*18
     for i in U:a[i]=-1
     for i in I:a[6+i]=1
     for i in J:a[12+i]=1
     out.append((U,I,J,a))
 assert len(out)==7591
 return out


def project(g,cut=None):
 e=[-1]*6+[1]*12;g=[Q(x)+Q(g[5])*e[i] for i,x in enumerate(g)]
 if cut is not None:
  pivot=next(i for i,v in enumerate(cut) if v)
  scale=g[pivot]/cut[pivot];g=[x-scale*v for x,v in zip(g,cut)]
 return g


def alpha(S):return [Q(3-s+i) for i,s in enumerate(S)]


def parity(p):return (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))


def factor(seed,U,I,J,h,mode='correct'):
 lam=[Q(seed[i]) for i in U];mu=[Q(seed[6+i]) for i in I];nu=[Q(seed[12+i]) for i in J]
 assert sum(lam)==sum(mu)+sum(nu)
 al=alpha(U);am=alpha(I);an=alpha(J);rho=[2,1,0];value=Q(0);grad=[Q(0)]*9;constant=0;selected=0;term_count=0
 for p in permutations(range(3)):
  for q in permutations(range(3)):
   term_count+=1
   if mode=='omit-identity' and p==q==(0,1,2):continue
   slope=[mu[p[i]]+nu[q[i]]-lam[i] for i in range(3)]
   assert all(x!=0 for x in slope),'nongeneric lower block'
   if slope[0]<0 or slope[2]>0:continue
   coord,sgn=(0,1) if slope[1]>0 else (2,-1)
   shift=3-Q(h,3)
   z=[am[p[i]]+an[q[i]]-al[i]-shift+(rho[p[i]]+rho[q[i]]-2*rho[i] if mode!='zero-rho' else 0) for i in range(3)]
   sign=parity(p)*parity(q);value+=sign*(1+sgn*z[coord]);constant+=sign*(1+sgn*(rho[p[coord]]+rho[q[coord]]-2*rho[coord]));selected+=1
   grad[coord]-=sign*sgn;grad[3+p[coord]]+=sign*sgn;grad[6+q[coord]]+=sign*sgn
 assert term_count==36
 # Independently derive min upper-minus-lower from the one-variable hive.
 x=lam+mu+nu;B=[v+3-Q(h,3) for v in al]+am+an
 upper=[[1,0,0,1,0,0,0,0,0],[0,0,0,1,1,0,1,0,0],[1,1,0,0,0,0,0,0,-1]]
 lower=[[0,1,0,1,0,0,0,0,0],[1,0,0,0,1,0,0,0,0],[0,0,0,1,0,1,1,0,0],[0,0,0,1,1,0,0,1,0],[1,0,1,0,0,0,0,0,-1],[1,1,0,0,0,0,0,-1,0]]
 forms=[[a-b for a,b in zip(u,l)] for u in upper for l in lower];lengths=[dot(g,x) for g in forms];length=min(lengths)
 if mode=='correct':
  if length<0:assert value==0 and constant==0 and all(v==0 for v in grad)
  else:
   assert length>0 and constant==1 and dot(grad,x)==length
   active=[g for g,l in zip(forms,lengths) if l==length]
   assert all(value==1+dot(g,B) for g in active)
 return value,{'value':str(value),'lower_constant':constant,'lower_length':str(length),'selected_A2_terms':selected,'all_A2_pairs':36,'lower_gradient':list(map(str,grad))}
