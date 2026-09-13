"""Independently authenticate every P08 mask implication and dimension bound."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import time
from mask_model_v1 import model, closure, identifications, images


def main():
    p = argparse.ArgumentParser(); p.add_argument('--roster',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    roster=json.loads(a.roster.read_text());n=roster['rank'];source=json.loads(Path(roster['mask_source']).read_text());m=model(n)
    result={'status':'running','pid':os.getpid(),'pgid':os.getpgrp(),'native_calls':0,'rank':n,'start':roster['start'],'stop':roster['stop']}
    with a.output.open('x') as f:
        def save():f.seek(0);json.dump(result,f,indent=2);f.write('\n');f.truncate();f.flush();os.fsync(f.fileno())
        save();start=time.monotonic()
        assert source['n']==n and source['mask_count']==1<<(3*(n-1))
        points=[tuple(x) for x in source['points']];lookup={q:i for i,q in enumerate(m['points'])}
        assert [list(row[lookup[q]] for q in points) for row in m['full_rows']]==source['rows']
        assert m['gaps']==[x['zero_rows'] for x in source['gaps']]
        assert m['rules']==sorted(tuple(x) for x in source['rules'])
        expected={}
        for item in source['atlas']:
            for mask in item['boundary_masks']:
                assert type(mask) is int and mask not in expected
                expected[mask]=item
        assert set(expected)==set(range(1<<(3*(n-1))))
        cache={};records=[]
        for mask in range(roster['start'],roster['stop']):
            z=closure(mask,m); item=expected[mask];assert z==item['closed_rows_mask'],mask
            if z not in cache:
                free,components,ground,words=identifications(z,m)
                cache[z]=(len(free),components,ground)
            dim,components,ground=cache[z];assert dim==item['upper_dimension_from_identifications'],mask
            assert item['nonidentification_equations']==[]
            records.append({'mask':mask,'closed_rows_mask':z,'dimension_bound':dim})
        result.update(status='complete',records=records,checked_count=len(records),independent_full_vertex_relations=len(m['rules']),
                      distinct_closures_checked=len(cache),dimension_histogram=dict(Counter(x['dimension_bound'] for x in records)),
                      seconds=time.monotonic()-start,scope='Sound complete original-rhombus mask implications and unit coordinate identifications; dimension upper bounds, not actual dimensions or counts')
        assert len(records)==roster['stop']-roster['start'];save()
        print(json.dumps({k:result[k] for k in ['rank','checked_count','distinct_closures_checked','seconds']}),flush=True)


if __name__=='__main__':main()
