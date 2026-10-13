"""Portable exact replay of the full retained A55/A56 initial-split certificates.

No LR backend, optimizer, network, or provider program is used. Run with
--a55, --a56 --rays-replay FILE, or --global, and an explicit --output FILE.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb
from pathlib import Path
import argparse,hashlib,json,time
from flow_counts import count,interpolate,ev,triple
DATA=Path(__file__).resolve().parents[2]/'data'
def insist(condition,message):
 if not condition:raise AssertionError(message)
def independent_count(widths,t):
 d=len(widths);lengths=[2*w*t+1 for w in widths];shifts=[(0,1)]
 for length in lengths:shifts += [(offset+length,-sign) for offset,sign in list(shifts)]
 total=0
 for s in range(sum(lengths)-d+1):
  value=sum(sign*comb(s-shift+d-1,d-1) for shift,sign in shifts if s>=shift)
  insist(value>=0,'negative bounded-composition multiplicity');total+=value**3
 return total
def first(values):
 D=len(values)-1;return sum(Q((-1)**(t-1)*comb(D,t)*(values[t]-values[0]),t) for t in range(1,D+1))
def degree(values):return max(i for i,x in enumerate(values) if x)
def original(widths):
 x=triple(widths);L,M,N=x['lambda_'],x['mu'],x['nu']
 insist(all(a>=b>=0 for a,b in zip(L,L[1:])) and all(a>=b>=0 for a,b in zip(M,M[1:])),'partitions')
 insist(all(a>=b for a,b in zip(L,M)) and sum(L)-sum(M)==sum(N),'literal containment/size')
 return x
def full_row(row,kind):
 old=tuple(row['old']);W=sum(old);m=len(old);D=3*m+4
 insist(W==row['W'] and all(x>0 for x in old),'positive old list')
 insist(row['degree_before']==3*m+1 and row['degree_after']==D,'prior actual degrees')
 before=(*old,2*W);after=(*old,W,W)
 bv=[count(before,t) for t in range(D+3)];av=[count(after,t) for t in range(D+3)]
 insist(bv==row['before_values'] and av==row['after_values'],'complete determining/holdout values')
 bp=interpolate(bv[:D+1]);ap=interpolate(av[:D+1]);gain=[a-b for a,b in zip(ap,bp)]
 insist(bp==list(map(Q,row['before_coefficients'])) and ap==list(map(Q,row['after_coefficients'])) and gain==list(map(Q,row['gain'])),'complete ordinary coefficient vectors')
 insist(degree(bp)==3*m+1 and degree(ap)==D and bp[0]==ap[0]==1 and gain[0]==0,'constants and actual degrees')
 insist(original(before)==row['before_triple'] and original(after)==row['after_triple'],'all literal original entries')
 insist(all(ev(bp,t)==bv[t] and ev(ap,t)==av[t] for t in (D+1,D+2)),'unused positive holdouts')
 insist(first([a-b for a,b in zip(av[:D+1],bv[:D+1])])==gain[1],'independent full c1 extraction')
 for t in (1,2):insist(independent_count(before,t)==bv[t] and independent_count(after,t)==av[t],'complete independent slice counts')
 if kind=='a56':insist(gain[1]>=Q(12,7)*W and Q(row['c1_over_W'])==gain[1]/W,'complete c1 ray bound')
 return dict(old=list(old),prior_degrees=[3*m+1,D],full_vectors_checked=2,determining_values=2*(D+1),holdouts=4,independent_slice_counts=4,c1=str(gain[1]),c1_over_W=str(gain[1]/W))
def kernel(h,x,y):
 M=x+y;p=x*y;u=2*h-M
 return (u+Q(4,3)*M+Q(7,2)*u*u+Q(19,3)*u*M+Q(23,12)*M*M+Q(7,6)*p
 +2*u**3+6*u*u*M+4*u*M*M+Q(2,3)*M**3+2*u*p+p*M
 +Q(1,2)*u**4+2*u**3*M+2*u*u*M*M+Q(2,3)*u*M**3+Q(1,12)*M**4+u*u*p+u*M*p+Q(1,6)*M*M*p+Q(1,6)*p*p)
def a55():
 source=json.loads((DATA/'a55/PILOT.json').read_text());rows=[full_row(r,'a55') for r in source['rows']];insist(len(rows)==12 and len({tuple(r['old']) for r in rows})==11,'complete retained A55 domain and duplicate')
 cases=0
 for h in range(8):
  for x in range(2*h+1):
   for y in range(2*h-x+1):
    f=lambda z:max(0,2*h+1-abs(z));actual=sum(f(z)*f(z+x)*f(z+x+y) for z in range(-2*h,2*h+1))-(4*h+1-x-y)
    insist(kernel(h,x,y)==actual,'entire four-interval kernel');cases+=1
 values=[6*sum((2*t-r+1)*r**5 for r in range(1,2*t+1)) for t in range(10)];moment=interpolate(values[:8]);saved=json.loads((DATA/'a55/HEAD-SPLIT-VERIFICATION.json').read_text())
 insist(moment==list(map(Q,saved['R4_coefficients'])) and moment[1]==Q(-2,7),'complete fourth-range moment')
 insist(all(ev(moment,t)==values[t] for t in (8,9)) and values[8:]==saved['R4_holdouts'],'moment holdouts')
 insist(cases==372 and Q(rows[0]['c1'])==Q(12,7),'kernel domain and whole-parent payment')
 return dict(status='PASS',rows=rows,distinct_original_inputs=11,logical_inputs=12,complete_kernel_cases=cases,R4_coefficients=list(map(str,moment)),M4_first_contribution='-1/42',whole_unit_old_gain_c1='12/7',no_general_moment_or_split_sign_inferred=True)
def a56(replay):
 source=json.loads((DATA/'a56/RAYS5.json').read_text());independent=json.loads((DATA/'a56/RAYS5-INDEPENDENT.json').read_text());fresh=json.loads(replay.read_text())
 normals=[]
 for h in product((-1,0,1),repeat=5):
  if 1 in h and -1 in h and next(x for x in h if x)!=-1:normals.append(list(h))
 normals += [[int(i==j) for i in range(5)] for j in range(5)];normals.sort()
 insist(normals==source['normals'] and len(normals)==95 and comb(95,4)==3183545,'complete fan normals')
 for key in ('n','normal_count','intersection_tests','full_rank_intersections','nonnegative_intersections','sorted_primitive_rays'):insist(source[key]==independent[key]==fresh[key],'exhaustive exact ray enumeration '+key)
 small=json.loads((DATA/'a56/RAYS4.json').read_text());insist({tuple([0]+r) for r in small['sorted_primitive_rays']}<=set(map(tuple,source['sorted_primitive_rays'])),'all zero-layer boundaries')
 cert=json.loads((DATA/'a56/RAY5-POLYNOMIALS.json').read_text());insist(len(cert['rows'])==125 and {tuple(r['ray']) for r in cert['rows']}==set(map(tuple,source['sorted_primitive_rays'])),'entire ray domain')
 rows=[full_row(r,'a56') for r in cert['rows']];by_old={tuple(r['old']):r for r in cert['rows']}
 lower=json.loads((DATA/'a56/RAY4-POLYNOMIALS.json').read_text())
 for r in lower['rows']:
  target=by_old[tuple(r['old'])]
  for key in ('before_values','after_values','before_coefficients','after_coefficients','gain','before_triple','after_triple'):insist(r[key]==target[key],'lower fan full-vector reuse')
 historical=json.loads((DATA/'a56/VERIFICATION.json').read_text());compatible=[]
 for pair in historical['same_closed_cone_sum_controls']:
  left,right=pair['left'],pair['right'];insist(all(sum(x*y for x,y in zip(h,left))*sum(x*y for x,y in zip(h,right))>=0 for h in normals),'closed-cone common signs')
  widths=tuple(x+y for x,y in zip(left,right) if x+y);W=sum(widths);D=3*len(widths)+4;values=[count((*widths,W,W),t)-count((*widths,2*W),t) for t in range(D+1)]
  insist(first(values)==Q(pair['c1']),'complete compatible ray-sum coefficient');compatible.append(pair)
 insist(len(compatible)==6 and sum(r['determining_values'] for r in rows)==4886 and sum(r['holdouts'] for r in rows)==500,'complete certificate totals')
 return dict(status='PASS',ray_orbits=125,intersection_tests=3183545,complete_parent_vectors=250,determining_values=4886,unused_positive_holdouts=500,independent_slice_counts=500,independent_c1_extractions=125,minimum_c1_over_W=str(min(Q(r['c1_over_W']) for r in rows)),closed_cone_sum_controls=compatible,native_LR_backend_called=False,all_higher_sign_claims_limited_to_retained_rays=True)
def global_controls():
 saved=json.loads((DATA/'a57/GLOBAL-CONTROLS.json').read_text());rows=[];gains={}
 for row in saved['rows']:
  parents={}
  for side in ('before','after'):
   r=row[side];widths=tuple(r['widths']);D=3*len(widths)-2;insist(D==r['actual_degree'],'prior whole-parent degree');values=[count(widths,t) for t in range(D+3)];coeff=interpolate(values[:D+1])
   insist(values[:D+1]==r['determining_values'] and coeff==list(map(Q,r['coefficients'])),'whole global control values/vectors')
   insist([[t,values[t]] for t in (D+1,D+2)]==r['unused_positive_holdouts'],'global whole holdouts')
   tr=original(widths);insist(dict(lambda_=r['original_triple']['lambda'],mu=r['original_triple']['mu'],nu=r['original_triple']['nu'])==tr,'complete global literal original')
   for t in r['independent_count_grades']:insist(independent_count(widths,t)==values[t] and ev(coeff,t)==values[t],'independent complete global count')
   parents[side]=coeff
  ap,bp=parents['after'],parents['before'];bp=bp+[Q(0)]*(len(ap)-len(bp));gain=[a-b for a,b in zip(ap,bp)];insist(gain==list(map(Q,row['gain'])) and str(gain[1])==row['c1_gain'],'whole global gain');gains[tuple(row['old'])]=gain[1];rows.append(dict(old=row['old'],c1_gain=str(gain[1])))
 insist(len(rows)==6 and gains[(1,1,1)]-gains[(1,2)]==Q(-6,5005) and gains[(1,1)]-gains[(2,)]==Q(2,35),'refinement and both Jensen obstructions')
 skeleton=[]
 for d in range(1,13):
  p=[Q(1)]
  for j in range(1,d+1):
   out=[Q(0)]*(len(p)+1)
   for i,v in enumerate(p):out[i]+=v;out[i+1]+=v/j
   p=out
  for codim in range(d+1):
   fac=1
   for j in range(1,d-codim+1):fac*=j
   value=p[d-codim]*fac;insist(value>0,'complete simplex skeleton');skeleton.append(dict(dimension=d,codimension=codim,sum=str(value)))
 insist(skeleton==saved['simplex_skeleton_coefficients'],'every full skeleton control')
 return dict(status='PASS',complete_parent_controls=12,rows=rows,refinement_defect='-6/5005',convexity_defect='2/35',complete_simplex_skeleton_slots=len(skeleton),whole_coefficient_or_generic_KTT_sign_inferred=False)
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--a55',action='store_true');g.add_argument('--a56',action='store_true');g.add_argument('--global',dest='global_check',action='store_true');p.add_argument('--rays-replay',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();start=time.monotonic()
 if a.a56:insist(a.rays_replay is not None,'complete fresh enumeration required');result=a56(a.rays_replay)
 elif a.a55:result=a55()
 else:result=global_controls()
 result.update(seconds=time.monotonic()-start,claim_boundary='Exact replay of existing full certificates; no new LR original/backend call, additive coverage or mathematical scope expansion.');a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('rows','closed_cone_sum_controls')}))
if __name__=='__main__':main()
