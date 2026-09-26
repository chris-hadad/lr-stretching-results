#!/usr/bin/env python3
"""Reconstruct the complete original hive cone using exact double description.

Python 3.11+ standard library only. No supplied ray list or external polyhedral
solver is used. The 45 input rhombi are regenerated before using atlas labels.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,itertools,json,math,sys,time


def need(ok,message):
    if not ok:raise ValueError(message)


def rank(rows):
    basis={}
    for row in rows:
        v=list(map(Q,row))
        for p,b in sorted(basis.items()):
            if v[p]:
                t=v[p];v=[x-t*y for x,y in zip(v,b)]
        p=next((i for i,x in enumerate(v) if x),None)
        if p is not None:
            t=v[p];basis[p]=[x/t for x in v]
    return len(basis)


def inverse(rows):
    n=len(rows)
    a=[list(map(Q,r))+[Q(i==j) for j in range(n)] for i,r in enumerate(rows)]
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        need(k is not None,'singular initial basis')
        a[j],a[k]=a[k],a[j]
        t=a[j][j];a[j]=[x/t for x in a[j]]
        for k in range(n):
            if k!=j and a[k][j]:
                t=a[k][j];a[k]=[x-t*y for x,y in zip(a[k],a[j])]
    return [r[n:] for r in a]


def primitive(v):
    v=list(map(Q,v));den=math.lcm(*(x.denominator for x in v))
    w=[int(x*den) for x in v];g=math.gcd(*w)
    need(g>0,'zero candidate ray')
    return tuple(x//g for x in w)


def dot(a,b):return sum(x*y for x,y in zip(a,b))


def complete_rays(rows):
    """Intersect a simplicial pointed cone with every remaining halfspace."""
    dimension=len(rows[0]);selected=[];basis=[]
    for i,r in enumerate(rows):
        if rank(basis+[r])>len(basis):selected.append(i);basis.append(r)
        if len(basis)==dimension:break
    need(len(basis)==dimension,'inequalities do not span the quotient')
    inv=inverse(basis)
    rays={primitive([inv[i][j] for i in range(dimension)]):0 for j in range(dimension)}
    for v in rays:
        need(all(dot(rows[i],v)>=0 for i in selected),'initial simplicial cone')
        rays[v]=sum(1<<i for i in selected if dot(rows[i],v)==0)
    pending=[i for i in range(len(rows)) if i not in selected]
    steps=[]
    while pending:
        # The order changes cost only; every original halfspace is eventually used.
        candidates=[]
        for i in pending:
            values={v:dot(rows[i],v) for v in rays}
            pos=sum(x>0 for x in values.values());neg=sum(x<0 for x in values.values())
            candidates.append((pos*neg,neg,i,values))
        _,_,i,values=min(candidates,key=lambda x:x[:3]);pending.remove(i)
        positive=[v for v in rays if values[v]>0]
        negative=[v for v in rays if values[v]<0]
        keep={v:mask|(1<<i if values[v]==0 else 0) for v,mask in rays.items() if values[v]>=0}
        adjacency={};pairs=0
        for p in positive:
            for n in negative:
                common=rays[p]&rays[n]
                if common.bit_count()<dimension-2:continue
                if common not in adjacency:
                    # A two-dimensional face has exactly two extreme rays. A
                    # higher-dimensional pointed face has at least three.
                    count=0
                    for mask in rays.values():
                        if mask&common==common:
                            count+=1
                            if count>2:break
                    adjacency[common]=count==2
                if not adjacency[common]:continue
                pairs+=1
                new=primitive([values[p]*y-values[n]*x for x,y in zip(p,n)])
                mask=common|(1<<i)
                need(dot(rows[i],new)==0,'cut intersection')
                need(new not in keep or keep[new]==mask,'duplicate ray incidence')
                keep[new]=mask
        need(keep,'empty nonzero cone during full-dimensional construction')
        selected.append(i)
        for v,mask in keep.items():
            slacks=[dot(rows[j],v) for j in selected]
            need(min(slacks)>=0,'negative accepted ray')
            need(mask==sum(1<<j for j,s in zip(selected,slacks) if s==0),'tight-row propagation')
        steps.append({'row':i,'before':len(rays),'positive':len(positive),'negative':len(negative),'crossing_edges':pairs,'after':len(keep)})
        rays=keep
    need(sorted(selected)==list(range(len(rows))),'omitted input halfspace')
    return sorted(rays),steps


def main():
    need(len(sys.argv)==3,'usage: geometry_stdlib.py atlas.json existing-fresh-output-dir')
    source=Path(sys.argv[1]);out=Path(sys.argv[2]);start=time.monotonic()
    need(out.is_dir() and not any(out.iterdir()),'empty existing output directory required')
    points=[(i,j) for i in range(7) for j in range(7-i)];positions={p:i for i,p in enumerate(points)}
    directions=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)];generated=set()
    for p in points:
        for u,v in itertools.combinations(directions,2):
            if 2*u[0]*v[0]+u[0]*v[1]+u[1]*v[0]+2*u[1]*v[1]!=1:continue
            quad=[p,(p[0]+u[0],p[1]+u[1]),(p[0]+v[0],p[1]+v[1]),(p[0]+u[0]+v[0],p[1]+u[1]+v[1])]
            if not all(q in positions for q in quad):continue
            row=[0]*28
            for q,c in zip(quad,[-1,1,1,-1]):row[positions[q]]+=c
            generated.add(tuple(row))
    atlas=json.loads(source.read_text());rows=list(map(tuple,atlas['rhombi']))
    need(len(rows)==len(generated)==45 and set(rows)==generated,'literal complete rhombi')
    interior=[p for p in points if min(p)>0 and sum(p)<6]
    need(interior==list(map(tuple,atlas['interior'])),'interior coordinates')
    inner=[tuple(r[positions[p]] for p in interior) for r in rows];normals=sorted(set(inner))
    need(len(normals)==42 and normals==list(map(tuple,atlas['normals'])),'primitive interior normals')
    row_to_normal=[normals.index(n) for n in inner]
    need(row_to_normal==atlas['row_preimages'],'physical preimages')
    for f in (lambda i,j:1,lambda i,j:i,lambda i,j:j):
        need(all(sum(r[k]*f(*p) for k,p in enumerate(points))==0 for r in rows),'affine kernel')
    free=[i for i,p in enumerate(points) if p not in {(0,0),(1,0),(0,1)}]
    reduced=[[r[i] for i in free] for r in rows]
    need(rank(reduced)==25,'exact quotient dimension')
    # This explicit strict hive proves full dimension throughout every cut.
    strict=[-(i*i+i*j+j*j) for i,j in points]
    need(all(dot(r,strict)>0 for r in rows),'strict hive witness')
    reduced_rays,steps=complete_rays(reduced)
    rays=[]
    for v in reduced_rays:
        w=[0]*28
        for i,x in zip(free,v):w[i]=x
        rays.append(tuple(w))
    rays.sort();masks=[]
    for ray in rays:
        slacks=[dot(r,ray) for r in rows]
        need(min(slacks)>=0 and math.gcd(*ray)==1,'primitive feasible ray')
        mask=sum(1<<i for i,s in enumerate(slacks) if s==0)
        need(rank([reduced[i] for i,s in enumerate(slacks) if s==0])==24,'extreme ray rank')
        masks.append(mask)
    need(len(rays)==166,'complete ray count')
    for i in range(45):
        need(rank([r for r in reduced_rays if dot(reduced[i],r)==0])==24,'original row is a facet')
    group=[]
    for perm in itertools.permutations(range(3)):
        def transform(p):
            q=(p[0],p[1],6-p[0]-p[1]);return tuple(q[i] for i in perm[:2])
        pa=[positions[transform(p)] for p in points];ca=[interior.index(transform(p)) for p in interior]
        moved=[]
        for r in rows:
            v=[0]*28
            for i,c in enumerate(r):v[pa[i]]=c
            moved.append(tuple(v))
        need(set(moved)==set(rows),'whole-row group action')
        na=[]
        for n in normals:
            v=[0]*10
            for i,c in enumerate(n):v[ca[i]]=c
            na.append(normals.index(tuple(v)))
        need(ca in atlas['coordinate_actions'],'interior isometry')
        gi=atlas['coordinate_actions'].index(ca)
        need(na==atlas['actions'][gi],'normal group action')
        group.append({'coordinates':ca,'normals':na})
    payload={'schema':'astra054-hive-cone/v1','points':points,'interior':interior,'rows':rows,'normals':normals,'row_to_normal':row_to_normal,'rays':rays,'tight_masks':masks,'group':group}
    (out/'GEOMETRY.json').write_text(json.dumps(payload,indent=2)+'\n')
    with (out/'CLASSIFY.txt').open('x') as f:
        f.write('42 45 166\n')
        for n in normals:f.write(' '.join(map(str,n))+'\n')
        f.write(' '.join(map(str,row_to_normal))+'\n'+' '.join(map(str,masks))+'\n')
    with source.open('rb') as f:source_hash=hashlib.file_digest(f,'sha256').hexdigest()
    result={'status':'PASS_COMPLETE_HIVE_CONE','method':'exact double description from regenerated original inequalities',
            'rhombi':45,'normal_directions':42,'ambient_after_gauge':25,'rays':len(rays),'H_V_H_exact_equal':True,
            'all_extreme_rank_certificates':True,'all_original_facet_rank_certificates':True,'integral_isometries':6,
            'input_sha256':source_hash,'cuts':steps,'seconds':time.monotonic()-start}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
