from pathlib import Path
from itertools import product
import json,sys
ROOT=Path(__file__).resolve().parent

def cap_domain():
 p=json.loads((ROOT/'data/COMPACT-DOMAIN.json').read_text())
 sets=[tuple(i+1 for i in range(5) if mask>>i&1) for mask in range(32) if not(mask&(mask<<1))]
 assert {tuple(x) for x in p['independent_peak_sets']}==set(sets) and len(sets)==13
 vals=[]
 for v in product(range(2),repeat=5):
  w=(0,)+v+(0,);t=[max(w[i],2*w[i]-w[i-1]-w[i+1]) for i in range(1,6)];vals.append((v,sum((i+1)*t[i] for i in range(5))))
 assert max(n for v,n in vals)==18 and [v for v,n in vals if n==18]==[(1,0,1,0,1)]
 matrix=json.loads((ROOT/'data/COMPACT-MATRICES.json').read_text())
 assert len(matrix['pieces'])==65
 def e(i):return [int(j==i) for j in range(15)]
 for piece in matrix['pieces']:
  peak=set(piece['peak_set']);k=piece['normalized_maximum_index'];expected=[]
  for i in range(5):
   pi=e(i);di=[2*x for x in pi]
   for j in [i-1,i+1]:
    if 0<=j<5:di[j]-=1
   ti=di if i+1 in peak else pi
   choice=[x-y for x,y in zip(di,pi)]
   if i+1 not in peak:choice=[-x for x in choice]
   expected += [(tuple(pi),0),(tuple(-x for x in pi),-1),(tuple(choice),0)]
   for j in [5+i,10+i]:expected += [(tuple(e(j)),0),(tuple(x-y for x,y in zip(ti,e(j))),0)]
   expected.append((tuple(e(5+i)[j]+e(10+i)[j]-di[j] for j in range(15)),0))
  assert sorted(expected)==sorted((tuple(z['row']),z['rhs']) for z in piece['inequalities'])
  assert piece['equalities']==[{'row':e(k-1),'rhs':1}]
 assert {(tuple(z['peak_set']),z['normalized_maximum_index']) for z in matrix['pieces']}==set(product(sets,range(1,6)))
 return {'pieces':65,'rows_per_piece':40,'binary_vertices':32,'max_weighted_threshold':18,'normalized_area_bound':36,'unbounded_rational_denominators':True,'polynomial_chambers_certified':False}


if __name__=='__main__':
 if sys.flags.optimize:
  raise RuntimeError('Optimized Python is refused for gap-cap replay')
 print(json.dumps(cap_domain(),indent=2))
