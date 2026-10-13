"""Complete A63 crossing bases and the separate A64 a=9 extension."""
import argparse,json,time
import crossing_math as m
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();s=time.monotonic()
result=dict(crossing=m.check_certificate(),zero_base=m.check_zero_base());a9=[]
for which in ('both','one'):
 got=m.chamber(9,which);assert all(q>=0 for q in got.values());degree=19
 axes=(0,) if which=='both' else (0,1)
 for j in range(degree+1):
  for axis in axes:assert got.get(tuple(j if i==axis else 0 for i in range(4)),0)>0
 a9.append(dict(chamber=which,coefficients=[dict(exponents=e,value=str(c)) for e,c in sorted(got.items())],omitted_coefficients='exact zero',total_degree=degree))
result.update(status='PASS',a9=a9,seconds=time.monotonic()-s)
with open(a.out,'x') as f:json.dump(result,f,indent=2)
print(json.dumps(dict(status='PASS',crossing_identities=result['crossing']['identities'],a9_chambers=2,seconds=result['seconds'])))
