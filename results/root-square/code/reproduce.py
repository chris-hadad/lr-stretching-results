"""Selected finite bridge/accounting; does not regenerate every large endpoint."""
import argparse,json,pathlib,time,gzip
from fractions import Fraction as Q
import fixed_wall_math as m
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=pathlib.Path(__file__).resolve().parents[1];s=time.monotonic()
eps={};fresh=[]
for k in range(3,97):
 d=json.loads(gzip.decompress((r/('data/endpoints/m%03d.json.gz'%k)).read_bytes()));field=d['primary'];C,E,J=(m.from_field(field[n]) for n in ['C','E','J'])
 assert C.degree()==E.degree()==2*k+1 and C[0]==1 and E[0]==0 and C==E+J
 assert all(C[i]>0 for i in range(2*k+2)) and all(E[i]>0 for i in range(1,2*k+2))
 eps[k]=(C,E,J)
 if k<=6:
  c,_,_=m.full_original(k);assert c==C;fresh.append(k)
for k in range(3,96):
 d=json.loads(gzip.decompress((r/('data/gains/m%03d.json.gz'%k)).read_bytes()));f=d['fields'];G,H,J,D,T,ST=(m.from_field(f[n]) for n in ['G','H','Jnext_minus_J','D','T','S_T'])
 assert G==eps[k+1][0]-eps[k][0] and H==eps[k+1][1]-eps[k][1] and J==eps[k+1][2]-eps[k][2] and G==H+J
 assert G.degree()==H.degree()==2*k+3 and G[0]==H[0]==0 and T==D*(1+m.S/(k+2)) and ST==m.S*T
 assert all((4*k*G-ST)[i]>0 for i in range(1,2*k+4))
 if k>=4:assert all((4*k*H-ST)[i]>0 for i in range(1,2*k+4))
 else:assert H[1]==Q(-499,2520) and J[1]==Q(5,4) and G[1]==Q(2651,2520)
 assert all(J[i]>=0 for i in range(J.degree()+1))
result=dict(status='PASS',selected_endpoints=94,selected_gains=93,positive_complement_gains=92,fresh_full_mask_endpoints=fresh,seconds=time.monotonic()-s,full_high_index_regeneration=False)
with open(a.output,'x') as f:json.dump(result,f,indent=2)
print(json.dumps(result))
