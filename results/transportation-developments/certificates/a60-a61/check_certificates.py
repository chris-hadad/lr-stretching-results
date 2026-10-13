"""Portable complete A60/A61 certificate replay; Python standard library only.

The mathematical generators are ports of accepted root arithmetic. This replay
is not a new independent LR method and makes no LR/count/oracle calls.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import time

BASE=Path(__file__).resolve().parent
PUBLIC_ROOT=BASE.parents[3]


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def verify_manifest(manifest=None):
    if manifest is None:manifest=json.loads((BASE/'MANIFEST.json').read_text())
    for row in manifest['files']:
        p=PUBLIC_ROOT/row['path']
        require(p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'Frozen input hash mismatch: '+row['path'])
    return manifest


def mathematical(value):
    if isinstance(value,dict):return {k:mathematical(v) for k,v in value.items() if k not in ('seconds','elapsed_seconds','source_sha256','scope')}
    if isinstance(value,list):return [mathematical(v) for v in value]
    return value


def simplex(dim,degree):
    if dim==1:
        yield (degree,);return
    for x in range(degree+1):
        for tail in simplex(dim-1,degree-x):yield (x,)+tail


def dense(P,degree,dim):
    if dim==1:
        values=list(P)+[F(0)]*(degree+1-len(P))
        require(len(values)==degree+1,'Univariate degree bound exceeded')
        return dict(dim=1,total_degree_bound=degree,coefficients=list(map(str,values)),slots=degree+1)
    require(all(len(p)==dim and sum(p)<=degree for p in P),'Multivariate degree bound exceeded')
    order=[p for n in range(degree+1) for p in simplex(dim,n)]
    return dict(dim=dim,total_degree_bound=degree,monomial_order='total degree then ascending coordinates',coefficients=[str(P.get(p,F(0))) for p in order],slots=len(order))


def cardinality(a60,chambers,balancing):
    require(len(a60['finite_bases'])==40,'A60 requires all forty base records')
    require(sum(r['large_cap_derivative'] is not None for r in a60['finite_bases'])==31,'A60 requires all thirty-one applicable derivative vectors')
    require(len(chambers['chambers'])==5,'A61 requires all five complete chambers')
    require(len(balancing['rows'])==15,'A61 requires all fifteen complete balancing polynomials')


def expected_refusal(label,function):
    try:function()
    except (ValueError,AssertionError) as e:return dict(control=label,result='EXPECTED_REFUSAL',reason=str(e))
    raise AssertionError('Missing refusal: '+label)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    start=time.monotonic();manifest=verify_manifest()
    # Authenticate frozen code/data before loading the local mathematical ports.
    k3=importlib.import_module('a60_certificate')
    ch=importlib.import_module('a61_chambers')
    bal=importlib.import_module('a61_balancing')
    audit=importlib.import_module('a61_map_audit')
    expected60=json.loads((BASE/'k3-certificate-v1.json').read_text())
    expected_ch=json.loads((BASE/'chambers-v1.json').read_text())
    expected_bal=json.loads((BASE/'balancing-probe-v1.json').read_text())
    historical=json.loads((BASE/'historical-chamber-maps.json').read_text())
    cardinality(expected60,expected_ch,expected_bal)
    require(not args.output.exists(),'Fresh output directory required')
    args.output.mkdir(parents=True)
    fields={};support=[];controls=[]
    def checkpoint(label):
        with (args.output/'PROGRESS.jsonl').open('a') as stream:stream.write(json.dumps(dict(phase=label,fields=len(fields),seconds=time.monotonic()-start))+'\n')
        with (args.output/'PARTIAL-FIELDS.json').open('w') as stream:json.dump(dict(completed_phase=label,fields=fields),stream,sort_keys=True);stream.write('\n')
    rows=k3.finite_bases()
    require(k3.serial(rows)==expected60['finite_bases'],'Complete A60 base/derivative vector mismatch')
    for row in rows:
        key='A60/'+','.join(map(str,row['caps']));degree=row['degree']
        fields[key+'/base']=dense(row['coefficients'],degree,1)
        if row['large_cap_derivative'] is not None:fields[key+'/large-cap-derivative']=dense(row['large_cap_derivative'],degree,1)
        else:support.append(dict(caps=row['caps'],branch='No large cap; no derivative direction is claimed'))
        # Entire same-coefficient correction decomposition, including signed debt.
        f=k3.formula(row['caps'])
        pieces={name:f[name] for name in ('N','tail','C1','C2','pair','total')}
        pieces['unrestricted']=k3.mul(f['N'],[1,f['L'],f['Q']])
        pieces['full']=f['P']
        support.append(dict(caps=row['caps'],complete_terms={name:dense(p,degree,1) for name,p in pieces.items()}))
    base=k3.large_base();require(k3.serial(base)==expected60['large_base'],'Complete A60 a=6 product-dominance base mismatch')
    factor=[]
    for a in (6,7,10,32):
        for B in (3,7,100):factor.append(dict(a=a,B=B,**k3.factorizations(a,B)))
    require(k3.serial(factor)==expected60['factor_checks'],'A60 complete factor controls differ')
    reserve=[]
    for caps in [[1]*6,[1]*7,[1]*20,[1,1,1,1,1,50],[1,2,2,3,4,7]]:
        f=k3.formula(caps);r=f['K']-6
        lower=k3.mul(f['N'],[1,F(139,140)+F(5,4)*r,F(47,780)+F(2387,2340)*r+F(5,12)*r*r])
        require(k3.dominates(f['P'],lower),'A60 full reserve control fails')
        reserve.append(dict(caps=caps,coefficients=f['P'],lower=lower,residual=k3.add(f['P'],k3.scale(lower,-1))))
    require(k3.serial(reserve)==expected60['reserve_controls'],'A60 full reserve control vectors differ')
    checkpoint('A60_complete_bases_derivatives_support_controls')
    hist={row['chamber']:row for row in historical['chambers']}
    target={(r['chamber'],r['small'],r['big']):r for r in expected_bal['rows']}
    full_ch=[];full_bal=[];walls=[]
    strict_axes={'zero-small':(0,1),'one-small':(0,),'two-small-no-pair':(0,1),'two-small-pair':(0,),'three-small':(0,2,3)}
    for row in expected_ch['chambers']:
        name=row['chamber'];matrix=ch.CHAMBERS[name]
        require(list(map(list,matrix))==row['parameter_rows'],'Complete chamber matrix differs')
        require(abs(audit.determinant(matrix))==1,'Chamber map is not unimodular')
        P,terms=ch.formula(matrix)
        require(P==audit.poly(row['coefficients']),'Complete chamber ordinary map differs: '+name)
        require(list(map(list,terms))==row['active_subsets'],'Complete chamber subsets differ: '+name)
        require(P==audit.poly(hist[name]['coefficients']),'Historical full independently reconstructed map differs: '+name)
        require(all(v>=0 for v in P.values()),'Adverse complete chamber coefficient')
        fields['A61/'+name+'/whole']=dense(P,8,4)
        for axis in strict_axes[name]:
            for degree in range(1,9):
                powers=tuple(degree if i==axis else 0 for i in range(4))
                require(P.get(powers,F())>0,'Missing pure-power strictness certificate')
        full_ch.append(dict(chamber=name,coefficients=row['coefficients'],active_subsets=terms,pure_power_axes=strict_axes[name],full_zero_slots_retained=True))
        inverse=bal.inv(matrix)
        for small,big in ((0,1),(0,2),(1,2)):
            direction=[r[small]-r[big] for r in inverse]
            independent=audit.direction(matrix,small,big)
            require(tuple(direction)==independent,'Gauss/Cramer direction disagreement')
            D=audit.derivative(P,independent);record=target[name,small,big]
            require(D==audit.poly(record['coefficients']) and [str(x) for x in direction]==record['direction'],'Complete balancing map mismatch')
            require(all(v>=0 for v in D.values()),'Negative full balancing certificate')
            fields[f'A61/{name}/balancing-{small}-{big}']=dense(D,7,4)
            full_bal.append(dict(chamber=name,small=small,big=big,direction=list(map(str,direction)),coefficients=record['coefficients']))
        checkpoint('A61_complete_chamber_and_three_balancing_'+name)
    for left,right in combinations(expected_ch['chambers'],2):
        common=[(i,j) for i,a in enumerate(audit.rays(left['parameter_rows'])) for j,b in enumerate(audit.rays(right['parameter_rows'])) if a==b]
        if len(common)!=3:continue
        li,ri=zip(*common)
        L=audit.restriction(audit.poly(hist[left['chamber']]['coefficients']),li)
        R=audit.restriction(audit.poly(hist[right['chamber']]['coefficients']),ri)
        require(L==R,'Complete shared-wall restriction differs')
        walls.append(dict(left=left['chamber'],right=right['chamber'],matched_rays=common,complete_coefficients=[dict(powers=p,coefficient=str(v)) for p,v in sorted(L.items())]))
    require(len(walls)==4,'All four shared-wall identities required')
    checkpoint('A61_all_five_fifteen_and_four_walls')
    # Missing complete inputs are refused even when their byte pins are ignored.
    controls.append(expected_refusal('missing_A60_base',lambda:cardinality({**expected60,'finite_bases':expected60['finite_bases'][:-1]},expected_ch,expected_bal)))
    controls.append(expected_refusal('missing_A61_chamber',lambda:cardinality(expected60,{**expected_ch,'chambers':expected_ch['chambers'][:-1]},expected_bal)))
    controls.append(expected_refusal('missing_A61_balancing',lambda:cardinality(expected60,expected_ch,{**expected_bal,'rows':expected_bal['rows'][:-1]})))
    bad=json.loads(json.dumps(manifest));bad['files'][0]['sha256']='0'*64
    controls.append(expected_refusal('changed_frozen_input_hash',lambda:verify_manifest(bad)))
    f=k3.formula([1,1,4]);wrong=k3.add(f['P'],k3.scale(f['pair'],-2))
    require(wrong!=f['P'],'A60 pair omission not exposed')
    controls.append(dict(control='omit_A60_complete_unit_pair',result='DETECTED_FULL_VECTOR_MISMATCH',correct=dense(f['P'],8,1),omitted=dense(wrong,8,1),difference=dense(k3.add(wrong,k3.scale(f['P'],-1)),8,1)))
    original_combinations=ch.combinations
    ch.combinations=lambda pool,q: (() if q==2 else original_combinations(pool,q))
    wrong,_=ch.formula(ch.CHAMBERS['two-small-pair']);ch.combinations=original_combinations
    correct=audit.poly(next(r for r in expected_ch['chambers'] if r['chamber']=='two-small-pair')['coefficients'])
    require(wrong!=correct,'A61 pair omission not exposed')
    controls.append(dict(control='omit_A61_complete_pair',result='DETECTED_FULL_FIELD_MISMATCH',correct=dense(correct,8,4),omitted=dense(wrong,8,4),difference=dense(ch.sub(wrong,correct),8,4)))
    verify_manifest()
    stats=dict(A60_bases=40,A60_applicable_large_cap_derivatives=31,A60_no_large_cap_branches=9,
        A60_base_ordinary_slots=sum(len(r['coefficients']) for r in rows),A60_derivative_ordinary_slots=sum(len(r['large_cap_derivative']) for r in rows if r['large_cap_derivative'] is not None),
        A61_complete_chambers=5,A61_complete_balancing_polynomials=15,A61_chamber_dense_slots=5*comb(12,4),A61_balancing_dense_slots=15*comb(11,4),
        A61_chamber_nonzero=sum(len(r['coefficients']) for r in expected_ch['chambers']),A61_balancing_nonzero=sum(len(r['coefficients']) for r in expected_bal['rows']),
        shared_wall_identities=4,omission_and_hash_controls=len(controls),full_dense_ordinary_slots=sum(row['slots'] for row in fields.values()))
    report=dict(status='PASS_COMPLETE_FROZEN_ARITHMETIC_REPLAY',scope=stats,seconds=time.monotonic()-start,
        methods='Accepted root symbolic/product generators; exact Gauss/Cramer balancing audit; comparison with full historical independently reconstructed coefficient maps. No new independent LR method is claimed.',
        new_LR_or_original_counts=0,new_named_originals=0,new_unused_observations=0,additive_coverage_increment=0,
        original_domains_and_actual_degrees='See the complete exported mathematical proofs; no generic degree is assigned to a physical zero/point face.',
        inputs_rechecked_unchanged=True,all_coefficient_fields=fields,complete_A60_same_coefficient_terms=k3.serial(support),
        all_A61_chambers=full_ch,all_A61_balancing=full_bal,all_shared_walls=walls,controls=controls)
    with (args.output/'CHECKS.json').open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(dict(status=report['status'],scope=stats,seconds=report['seconds']),sort_keys=True))

if __name__=='__main__':main()
