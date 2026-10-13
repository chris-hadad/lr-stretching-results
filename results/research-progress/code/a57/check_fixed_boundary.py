"""Portable exact replay of every retained fixed-boundary witness and Farkas row.

No optimizer is imported or run. The one unresolved source cell stays unresolved.
"""
from fractions import Fraction as Q
from pathlib import Path
import json,sys
from check_u11 import DATA,rows,slack,boundary,unit_pivot,split
from check_p3_parent import roster

def main():
 probe=json.loads((DATA/'p3-probe-v1.json').read_text());dual=json.loads((DATA/'p3-dual-v2.json').read_text());h=json.loads((DATA/'U11-COLLAR-FAMILY.json').read_text())['cases'][0];pts,ints,labs,full,norm=rows(7);pidx={p:i for i,p in enumerate(pts)};base=[h['parent'][j] if p not in set(ints) else 0 for j,p in enumerate(pts)];constants={r:slack(base,full[r]) for r in labs};possible=roster();seen=set();good=0;slacks_checked=0
 for case in probe['cases']:
  seed=tuple(map(tuple,case['seed']));assert seed in possible and seed not in seen;seen.add(seed);unit_pivot([norm[r] for r in seed])
  if case.get('exact_status')!='verified':continue
  height=list(map(Q,case['height']));assert len(height)==len(pts) and boundary(height,7,pidx)==probe['fixed_boundary'];sv={r:slack(height,full[r]) for r in labs};forced=set(map(tuple,case['forced_zero_rows']));assert all(sv[r]==0 for r in forced) and all(sv[r]>=Q(case['exact_margin'])>0 for r in labs if r not in forced);assert min(sv[r] for r in labs if r not in forced)==Q(case['minimum_off_face_slack']);good+=1;slacks_checked+=len(labs)
 assert seen==possible and good==41
 certified=set();objectives=[]
 for cert in dual['certificates']:
  seed=tuple(map(tuple,cert['seed']));assert seed in possible and seed not in certified;certified.add(seed);yw=[(tuple(v['row']),Q(v['weight'])) for v in cert['inequality_weights']];ew=[(tuple(v['row']),Q(v['weight'])) for v in cert['seed_equality_weights']];assert all(r in labs and r not in seed and v>=0 for r,v in yw) and all(r in seed for r,v in ew);assert sum(v for _,v in yw)==1
  assert all(sum(v*norm[r][j] for r,v in yw+ew)==0 for j in range(len(ints)));value=sum(v*constants[r] for r,v in yw+ew);assert value==Q(cert['constant_objective'])<0;objectives.append(str(value))
 assert len(certified)==6 and not dual['unrecovered'];assert '-432' in objectives
 unresolved=[c for c in probe['cases'] if c.get('exact_status')!='verified' and tuple(map(tuple,c['seed'])) not in certified];assert len(unresolved)==1
 output=Path(sys.argv[1]) if len(sys.argv)>1 else Path('a57-fixed-boundary-replay.json');output.parent.mkdir(parents=True,exist_ok=True);result=dict(status='PASS',complete_roster=48,exact_witnesses=good,full_original_rows_checked=slacks_checked,exact_Farkas_certificates=6,objectives=objectives,unresolved_source_cells=1,new_common_boundary_still_separate=True,optimizer_or_LR_backend_called=False)
 with output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result))
if __name__=='__main__':main()
