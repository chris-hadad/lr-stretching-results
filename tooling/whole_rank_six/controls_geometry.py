#!/usr/bin/env python3
"""Exact original-hive boundary and physical-branch controls, without a solver."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement,product
from pathlib import Path
import importlib.util,json,math,sys


def need(ok,message):
    if not ok:raise ValueError(message)


def affine_rows(geometry,lam,mu,nu):
    need(sum(lam)==sum(mu)+sum(nu),'balanced boundary')
    need(all(len(v)==6 and all(v[i]>=v[i+1]>=0 for i in range(5)) for v in (lam,mu,nu)),'partitions')
    points=list(map(tuple,geometry['points']));inside=list(map(tuple,geometry['interior']))
    boundary={}
    for i in range(7):boundary[(i,0)]=sum(mu[:i])
    for j in range(7):boundary[(0,j)]=sum(lam[:j])
    for j in range(7):
        p=(6-j,j);value=sum(mu)+sum(nu[:j])
        need(p not in boundary or boundary[p]==value,'consistent corner')
        boundary[p]=value
    ns=[];cs=[]
    for row in geometry['rows']:
        ns.append(tuple(row[points.index(p)] for p in inside))
        cs.append(sum(row[points.index(p)]*v for p,v in boundary.items()))
    return ns,cs


def reduction(rows,rhs,width):
    a=[list(map(Q,row))+[Q(c)] for row,c in zip(rows,rhs)]
    pivots=[]
    for col in range(width):
        at=len(pivots);p=next((i for i in range(at,len(a)) if a[i][col]),None)
        if p is None:continue
        a[at],a[p]=a[p],a[at];v=a[at][col];a[at]=[x/v for x in a[at]]
        for i in range(len(a)):
            if i!=at and a[i][col]:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[at])]
        pivots.append(col)
    need(all(any(r[:-1]) or not r[-1] for r in a),'inconsistent affine equalities')
    base=[Q(0)]*width
    for r,p in zip(a,pivots):base[p]=r[-1]
    directions=[]
    for f in range(width):
        if f in pivots:continue
        v=[Q(0)]*width;v[f]=1
        for r,p in zip(a,pivots):v[p]=-r[f]
        directions.append(v)
    return base,directions,len(pivots)


def short_positive_certificates(ns,cs):
    """Search short nonnegative row sums; returned identities are checked exactly."""
    by_full={};min_constant={}
    for k in (1,2,3):
        for support in combinations_with_replacement(range(45),k):
            normal=tuple(sum(ns[i][j] for i in support) for j in range(10))
            constant=sum(cs[i] for i in support);key=normal+(constant,)
            by_full.setdefault(key,[]).append(support)
            if normal not in min_constant or constant<min_constant[normal][0]:
                min_constant[normal]=(constant,support)
    forced=set();certificates=[];empty=None
    for normal,(constant,support) in min_constant.items():
        opposite=tuple(-x for x in normal)
        if opposite in min_constant and constant+min_constant[opposite][0]<0:
            empty=support+min_constant[opposite][1];break
    for key,supports in by_full.items():
        opposite=tuple(-x for x in key)
        if opposite not in by_full:continue
        other=by_full[opposite][0]
        for support in supports:
            joint=support+other
            if set(joint)<=forced:continue
            need(all(sum(ns[i][j] for i in joint)==0 for j in range(10)) and sum(cs[i] for i in joint)==0,'zero row-sum certificate')
            certificates.append(list(joint));forced.update(joint)
    if empty is not None:
        need(all(sum(ns[i][j] for i in empty)==0 for j in range(10)) and sum(cs[i] for i in empty)<0,'empty-fiber Farkas certificate')
    return sorted(forced),certificates,empty


def main():
    need(len(sys.argv)==3,'usage: controls_geometry.py GEOMETRY.json new-result.json')
    geometry=json.loads(Path(sys.argv[1]).read_text());out=Path(sys.argv[2]);need(not out.exists(),'fresh control output')
    spec=importlib.util.spec_from_file_location('cone',Path(__file__).parent/'src/portable/geometry_stdlib.py')
    cone=importlib.util.module_from_spec(spec);spec.loader.exec_module(cone)
    lam=(40,39,27,22,17,10);mu=(34,18,17,11,1,0);nu=(28,21,15,9,1,0)
    ns,cs=affine_rows(geometry,lam,mu,nu)
    # The supplied witness puts lambda on the horizontal edge. Transpose BOTH
    # heights and physical rows into this package's vertical-lambda convention.
    inside=list(map(tuple,geometry['interior']));points=list(map(tuple,geometry['points']))
    coordinate_action=[inside.index((j,i)) for i,j in inside]
    point_action=[points.index((j,i)) for i,j in points]
    source_point=(73,90,101,108,100,117,128,127,140,144);point=[0]*10
    for i,value in enumerate(source_point):point[coordinate_action[i]]=value
    row_action=[]
    for row in geometry['rows']:
        moved=[0]*28
        for i,value in enumerate(row):moved[point_action[i]]=value
        row_action.append(geometry['rows'].index(moved))
    edge_coordinate=coordinate_action[8]
    slacks=[c+sum(a*b for a,b in zip(n,point)) for n,c in zip(ns,cs)]
    need(min(slacks)>=0,'legal hostile witness')
    source_support=(2,3,4,5,6,17,21,30,40)
    preimages=[[r for r,n in enumerate(geometry['row_to_normal']) if n==i] for i in source_support]
    ranks=[];closures=[];actual=[]
    for source_branch in product(*preimages):
        branch=tuple(row_action[r] for r in source_branch)
        survivors=[mask for mask in geometry['tight_masks'] if all(mask>>r&1 for r in branch)]
        closure=[r for r in range(45) if all(mask>>r&1 for mask in survivors)]
        rank=cone.rank([ns[r] for r in closure]);ranks.append(rank);closures.append(closure)
        if all(slacks[r]==0 for r in branch):actual.append(list(branch));need(rank==9,'actual positive-weight branch retained')
    need(ranks==[10,10,10,10,9,9,9,9] and actual,'all eight physical branches')
    need(not all(r==9 for r in ranks) and ranks[0]!=9 and any(r==9 for r in ranks),'first-branch and AND countercontrols')
    low=None;high=None
    for n,c in zip(ns,cs):
        a=c+sum(n[j]*point[j] for j in range(10) if j!=edge_coordinate);v=n[edge_coordinate]
        if v>0:low=max(low,Q(-a,v)) if low is not None else Q(-a,v)
        elif v<0:high=min(high,Q(-a,v)) if high is not None else Q(-a,v)
        else:need(a>=0,'fixed edge rows')
    need((low,high)==(Q(138),Q(143)) and cone.rank([ns[r] for r in actual[0]])==9,'complete primitive edge')
    hostile={'lambda':lam,'mu':mu,'nu':nu,'point':point,'source_normal_support':source_support,'closure_ranks_in_transported_source_order':ranks,
             'source_to_paper_coordinate_permutation':coordinate_action,'source_to_paper_physical_row_permutation':row_action,
             'actual_branches':actual,'primitive_edge_coordinate':edge_coordinate,'edge_interval':[138,143],'lattice_length':5}
    cases=[]
    for name,lam,mu,nu,expected in [
        ('padded-rank-three',(3,2,1,0,0,0),(2,1,0,0,0,0),(2,1,0,0,0,0),1),
        ('all-empty',(0,)*6,(0,)*6,(0,)*6,0),
        ('empty-positive-stretch',(1,1,0,0,0,0),(2,0,0,0,0,0),(0,)*6,-1)]:
        ns,cs=affine_rows(geometry,lam,mu,nu);forced,certs,empty=short_positive_certificates(ns,cs)
        record={'name':name,'lambda':lam,'mu':mu,'nu':nu,'zero_row_sums':certs}
        if expected==-1:
            need(empty is not None,'exact empty-fiber certificate');record.update(contradictory_row_sum=list(empty),constant=sum(cs[i] for i in empty),positive_stretch_polynomial='0')
        else:
            need(empty is None,'feasible boundary not empty')
            base,directions,rank=reduction([ns[r] for r in forced],[-cs[r] for r in forced],10)
            need(len(directions)==expected and all(x.denominator==1 for x in base),'complete forced affine hull')
            if expected==0:
                need(base==[0]*10 and all(cs[i]+sum(ns[i][j]*base[j] for j in range(10))>=0 for i in range(45)),'unique zero hive')
                record.update(affine_rank=rank,polynomial='1')
            else:
                direction=directions[0];need(all(x.denominator==1 for x in direction) and math.gcd(*(int(x) for x in direction))==1,'saturated interval parameter')
                lo=None;hi=None
                for n,c in zip(ns,cs):
                    a=c+sum(x*y for x,y in zip(n,base));v=sum(x*y for x,y in zip(n,direction))
                    if v>0:lo=max(lo,-a/v) if lo is not None else -a/v
                    elif v<0:hi=min(hi,-a/v) if hi is not None else -a/v
                    else:need(a>=0,'all remaining fixed rows')
                need(lo is not None and hi is not None and lo.denominator==hi.denominator==1 and hi-lo==1,'whole unit interval')
                # The free coordinate equals the integer parameter. Homogeneous
                # dilation multiplies base and endpoints by t, giving t+1 points.
                record.update(affine_rank=rank,base=list(map(int,base)),primitive_direction=list(map(int,direction)),interval=[int(lo),int(hi)],polynomial='t+1')
        cases.append(record)
    result={'status':'PASS_EXACT_ORIGINAL_HIVE_CONTROLS','whole_rank_six_verified':False,'hostile_branch_example':hostile,'homogeneous_boundary_cases':cases}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
