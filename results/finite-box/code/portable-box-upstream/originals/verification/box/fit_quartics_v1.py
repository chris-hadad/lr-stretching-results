"""Complete independent vectors, persisted before source comparisons or holdouts."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import json,os
from pathlib import Path
import time


def polynomial(values):
    if len(values)!=5:raise ValueError('Quartic determining space requires five nodes')
    dif=list(values);first=[]
    while dif:first.append(dif[0]);dif=[b-a for a,b in zip(dif,dif[1:])]
    coeff=[Q(0)]*5;basis=[Q(1)]
    for k,c in enumerate(first):
        for i,v in enumerate(basis):coeff[i]+=c*v
        if k<4:
            new=[Q(0)]*(len(basis)+1)
            for i,v in enumerate(basis):new[i]-=k*v/Q(k+1);new[i+1]+=v/Q(k+1)
            basis=new
    assert all(sum(c*Q(t)**k for k,c in enumerate(coeff))==v for t,v in enumerate(values))
    return coeff


def main():
    p=argparse.ArgumentParser();p.add_argument('--roster',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=json.loads(a.roster.read_text());model=json.loads(Path(r['models']).read_text());assert model['status']=='complete'
    by_id={x['id']:x for x in model['records']};wanted=r['expected_ids'];assert wanted and len(wanted)==len(set(wanted));values={}
    for path in r['determining_results']:
        j=json.loads(Path(path).read_text());assert j['status']=='complete'
        for row in j['counts']:
            id=int(row['id']);assert id not in values and row['nodes']==[0,1,2,3,4] and row['dimension']==4
            assert id in by_id and row['record_index']==by_id[id]['record_index'];values[id]=list(map(int,row['counts']))
    assert set(values)==set(wanted)
    result={'status':'running','pid':os.getpid(),'pgid':os.getpgrp(),'native_calls':0,'expected_ids':wanted,'records':[],
            'source_comparison_loaded':False,'positive_holdouts_loaded':False,'candidates':[]}
    with a.output.open('x') as out:
        def save():out.seek(0);json.dump(result,out,indent=2);out.write('\n');out.truncate();out.flush();os.fsync(out.fileno())
        save();start=time.monotonic()
        for id in wanted:
            vals=values[id];m=by_id[id];assert vals[0]==1
            if vals[1]==0:
                assert vals[2:]==[0,0,0];co=[Q(0)];state='proved_empty_by_saturation'
            else:co=polynomial(vals);state='nonempty'
            record={'id':id,'original_boundary':m['original_boundary'],'rank':m['rank'],'preimages':m['preimages'],
                    'degree_bound':4,'determining_nodes':[0,1,2,3,4],'values':vals,'coefficients':[str(x) for x in co],
                    'actual_degree':max([k for k,x in enumerate(co) if x] or [0]),'state':state}
            negative=[k for k,x in enumerate(co) if x<0];record['negative_indices']=negative;result['records'].append(record)
            if negative:
                result['candidates'].append(record);result['status']='candidate_interrupt';save();raise SystemExit(3)
            if len(result['records'])%512==0:save()
        positive=[(Q(c),x['id'],i) for x in result['records'] for i,c in enumerate(x['coefficients']) if i>0 and Q(c)>0]
        result.update(status='complete',record_count=len(wanted),actual_degree_histogram=dict(Counter(x['actual_degree'] for x in result['records'])),
                      distinct_vectors=len({tuple(x['coefficients']) for x in result['records']}),positive_nonconstant_occurrences=len(positive),
                      minimum_positive={'value':str(min(positive)[0]),'id':min(positive)[1],'index':min(positive)[2]} if positive else None,
                      seconds=time.monotonic()-start)
        save();print(json.dumps({k:result[k] for k in ['status','record_count','distinct_vectors','actual_degree_histogram','minimum_positive','seconds']}),flush=True)

if __name__=='__main__':main()
