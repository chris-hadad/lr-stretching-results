"""A54 independent exact hive-cone reconstruction; native artifacts are data only."""
from pathlib import Path
import hashlib, itertools, json, math, sys, time
from sage.all import ZZ, QQ, matrix, Polyhedron

ATLAS = Path(sys.argv[1])

def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def primitive(v):
    denominator = math.lcm(*(int(x.denominator()) for x in v))
    w = [int(x * denominator) for x in v]
    divisor = math.gcd(*w)
    assert divisor > 0
    return tuple(x // divisor for x in w)

def main():
    if sys.flags.optimize:
        raise ValueError('Run exact geometry with Python assertions enabled')
    start = time.monotonic()
    out = Path(sys.argv[2])
    assert out.is_dir() and not (out / 'RESULT.json').exists()
    points = [(i, j) for i in range(7) for j in range(7-i)]
    positions = {p:i for i,p in enumerate(points)}
    directions = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
    rows = set()
    for p in points:
        for u,v in itertools.combinations(directions, 2):
            if 2*u[0]*v[0]+u[0]*v[1]+u[1]*v[0]+2*u[1]*v[1] != 1:
                continue
            quad = [p,(p[0]+u[0],p[1]+u[1]),(p[0]+v[0],p[1]+v[1]),(p[0]+u[0]+v[0],p[1]+u[1]+v[1])]
            if not all(q in positions for q in quad):
                continue
            row = [0]*28
            for q,c in zip(quad,[-1,1,1,-1]):
                row[positions[q]] += c
            rows.add(tuple(row))
    rows = sorted(rows)
    atlas = json.loads(ATLAS.read_text())
    assert len(rows) == 45 and set(rows) == set(map(tuple, atlas['rhombi']))
    rows = [tuple(r) for r in atlas['rhombi']]  # Relabel only after independent set equality.
    interior = [p for p in points if p[0]>0 and p[1]>0 and sum(p)<6]
    assert interior == [tuple(p) for p in atlas['interior']]
    inner_rows = [tuple(r[positions[p]] for p in interior) for r in rows]
    normals = sorted(set(inner_rows))
    assert normals == [tuple(r) for r in atlas['normals']] and len(normals)==42
    row_to_normal = [normals.index(r) for r in inner_rows]
    assert row_to_normal == atlas['row_preimages']
    gauge = {(0,0),(1,0),(0,1)}
    free = [i for i,p in enumerate(points) if p not in gauge]
    full_matrix = matrix(ZZ, rows)
    assert full_matrix.rank()==25
    for f in (lambda i,j:1,lambda i,j:i,lambda i,j:j):
        assert all(sum(r[k]*f(*p) for k,p in enumerate(points))==0 for r in rows)
    reduced = [[r[i] for i in free] for r in rows]
    cone = Polyhedron(ieqs=[[0]+r for r in reduced], base_ring=QQ, backend='ppl')
    assert cone.dim()==25 and not cone.lines_list() and cone.vertices_list()==[[0]*25]
    reduced_rays = sorted(primitive(r) for r in cone.rays_list())
    rays=[]
    for r in reduced_rays:
        w=[0]*28
        for i,x in zip(free,r):w[i]=x
        rays.append(tuple(w))
    rays=sorted(rays)
    masks=[]
    for ray in rays:
        slacks=[sum(a*b for a,b in zip(r,ray)) for r in rows]
        assert min(slacks)>=0 and math.gcd(*ray)==1
        mask=sum(1<<i for i,s in enumerate(slacks) if s==0)
        assert matrix(QQ,[reduced[i] for i,s in enumerate(slacks) if s==0]).rank()==24
        masks.append(mask)
    dual = Polyhedron(rays=reduced_rays,vertices=[[0]*25],base_ring=QQ,backend='ppl')
    assert dual==cone
    assert sorted(primitive(h[1:]) for h in dual.inequalities_list())==sorted(primitive(list(map(QQ,r))) for r in reduced)
    permutations=[]
    for perm in itertools.permutations(range(3)):
        def transform(p):
            q=(p[0],p[1],6-p[0]-p[1]); t=tuple(q[i] for i in perm);return t[:2]
        point_action=[positions[transform(p)] for p in points]
        coordinate_action=[interior.index(transform(p)) for p in interior]
        moved_rows=[]
        for r in rows:
            t=[0]*28
            for i,c in enumerate(r):t[point_action[i]]=c
            moved_rows.append(tuple(t))
        assert set(moved_rows)==set(rows)
        normal_action=[]
        for n in normals:
            t=[0]*10
            for i,c in enumerate(n):t[coordinate_action[i]]=c
            normal_action.append(normals.index(tuple(t)))
        assert list(coordinate_action) in atlas['coordinate_actions']
        gi=atlas['coordinate_actions'].index(coordinate_action)
        assert normal_action==atlas['actions'][gi]
        permutations.append({'coordinates':coordinate_action,'normals':normal_action})
    payload={'schema':'astra054-hive-cone/v1','points':points,'interior':interior,'rows':rows,'normals':normals,'row_to_normal':row_to_normal,'rays':rays,'tight_masks':masks,'group':permutations}
    (out/'GEOMETRY.json').write_text(json.dumps(payload,indent=2)+'\n')
    with (out/'CLASSIFY.txt').open('x') as f:
        f.write(f'42 45 {len(rays)}\n')
        for n in normals:f.write(' '.join(map(str,n))+'\n')
        f.write(' '.join(map(str,row_to_normal))+'\n')
        f.write(' '.join(map(str,masks))+'\n')
    result={'status':'PASS_COMPLETE_HIVE_CONE','rhombi':45,'normal_directions':42,'ambient_after_gauge':25,'rays':len(rays),'H_V_H_exact_equal':True,'all_extreme_rank_certificates':True,'integral_isometries':6,'inputs':{str(ATLAS):sha(ATLAS)},'seconds':time.monotonic()-start,'outputs':{name:sha(out/name) for name in ['GEOMETRY.json','CLASSIFY.txt']}}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
