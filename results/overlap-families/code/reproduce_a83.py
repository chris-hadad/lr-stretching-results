"""Complete selected A83 finite joins and all-index algebraic certificate checks."""
import argparse,json,pathlib,sys,time
import verify_overlap_v1 as v
import prefix_support_v1 as ps
import certificates_v1 as c
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=False);v.RAW=out
started=time.monotonic();joined=[]
for section in ('two_r','bases','balanced_gain','pre_return','last_prefix'):
 for algorithm in ('determining','validating'):v.execute(section,algorithm,section+'-'+algorithm)
 v.join(section+'-join',section+'-determining',section+'-validating');joined.append(json.loads((out/(section+'-join')/'JOIN.json').read_text()))
for algorithm in ('determining','validating'):
 sys.argv=['prefix','--phase','compute','--attempt','prefix-'+algorithm,'--algorithm',algorithm];ps.main()
v.join('prefix-join','prefix-determining','prefix-validating');joined.append(json.loads((out/'prefix-join/JOIN.json').read_text()))
for phase in ('free','intermediate','controls'):
 sys.argv=['certificates','--phase',phase,'--attempt','cert-'+phase];c.main()
assert sum(j['complete_fields'] for j in joined)==1355 and sum(j['all_ordinary_slots'] for j in joined)==267796
result=dict(status='PASS',full_joins=6,complete_fields=1355,ordinary_slots=267796,seconds=time.monotonic()-started,scientific_adoption='NOT_DECIDED_BY_THIS_CHECKER')
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
