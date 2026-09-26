"""Exact fixed A5 tree data and an independent small root-flow reference."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import json, sys, time

EDGES = [(i,j) for i in range(6) for j in range(i+1,6)]
ZETA = (1,1,1,1,1,-5)
BERNOULLI = [F(1),F(-1,2),F(1,6),F(0),F(-1,30),F(0),F(1,42),F(0),F(-1,30),F(0),F(5,66)]

def save(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2); stream.write('\n')

def tree(word):
    degree = [1+word.count(i) for i in range(6)]
    edges = []
    for v in word:
        leaf = next(i for i in range(6) if degree[i] == 1)
        edges.append(tuple(sorted((leaf,v))))
        degree[leaf] -= 1; degree[v] -= 1
    edges.append(tuple(i for i in range(6) if degree[i] == 1))
    return tuple(sorted(edges))

def mask_sum(mask, a):
    return sum(a[i] for i in range(6) if mask >> i & 1)

def data(edges, base):
    ell = [base**i for i in range(15)]
    adj = [[] for _ in range(6)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    masks = []
    for u,v in edges:
        seen = {u}; stack = [u]
        while stack:
            a = stack.pop()
            for b in adj[a]:
                if {a,b} == {u,v} or b in seen: continue
                seen.add(b); stack.append(b)
        masks.append(sum(1 << a for a in seen))
    # Each cut functional is the corresponding integer inverse row.
    for i,mask in enumerate(masks):
        assert all(((mask >> u & 1)-(mask >> v & 1)) == int(i == j)
                   for j,(u,v) in enumerate(edges))
    q = [sum(ell[EDGES.index(e)] for e,mask in zip(edges,masks) if mask >> i & 1)
         for i in range(6)]
    q = [a-q[5] for a in q]
    weights = []
    for e in EDGES:
        if e in edges: continue
        u,v = e
        ray = [0]*15; ray[EDGES.index(e)] = 1
        for edge,mask in zip(edges,masks):
            ray[EDGES.index(edge)] = -((mask >> u & 1)-(mask >> v & 1))
        assert all(sum(x*((a == i)-(b == i)) for x,(a,b) in zip(ray,EDGES)) == 0 for i in range(6))
        weight = sum(a*b for a,b in zip(ell,ray))
        assert weight == ell[EDGES.index(e)]-q[u]+q[v] and weight != 0
        assert all(x in (-1,0,1) for x in ray)
        weights.append(weight)
    coeff = [F(1)] + [F(0)]*10
    for w in weights:
        factor = [-BERNOULLI[h]*F(w)**(h-1)/factorial(h) for h in range(11)]
        coeff = [sum(coeff[j]*factor[h-j] for j in range(h+1)) for h in range(11)]
    f = [coeff[10-h]/factorial(h) for h in range(11)]
    return {'edges':edges, 'masks':masks, 'q':q, 'weights':weights,
            'F':[str(x) for x in f], 'J':[str((h+1)*f[h+1]) for h in range(10)]}

def build(out, base):
    started = time.monotonic()
    trees = sorted({tree(tuple(w)) for w in product(range(6), repeat=4)})
    assert len(trees) == 1296 and base in (2,3)
    rows = [data(t,base) for t in trees]
    save(Path(out)/'TREES.json', {'base':base,'rows':rows})
    with (Path(out)/'TREES.txt').open('x') as stream:
        stream.write('A19TREE1 1296\n')
        for row in rows:
            stream.write(' '.join(map(str,row['masks']+row['q']))+'\n')
            stream.write(' '.join(row['F'])+'\n')
    save(Path(out)/'RESULT.json', {'status':'COMPLETE_TREE_DATA','trees':1296,
         'primitive_kernel_rays':12960,'ell_base':base,'elapsed_seconds':time.monotonic()-started,
         'cut_inverse_and_kernel_checks':True})

def horner(coeff,x):
    result = F(0)
    for c in reversed(coeff): result = result*x+c
    return result

@lru_cache(None)
def compositions(total, slots):
    if slots == 1: return ((total,),)
    return tuple((a,)+tail for a in range(total+1) for tail in compositions(total-a,slots-1))

@lru_cache(None)
def reference(a):
    if not a: return 1
    if a[0] < 0: return 0
    return sum(reference(tuple(a[i+1]+c[i] for i in range(len(a)-1)))
               for c in compositions(a[0], len(a)))

def roots(path,out):
    started = time.monotonic(); rows = json.loads(Path(path).read_text())['rows']
    for r in rows: r['coeff'] = list(map(F,r['F']))
    result = []
    for a0 in product((-1,0,1),repeat=5):
        a = a0+(-sum(a0),); supported = all(sum(a[:i]) >= 0 for i in range(1,6))
        selected = [r for r in rows if supported and all(12*mask_sum(mask,a)+mask_sum(mask,ZETA)>0 for mask in r['masks'])]
        value = sum((horner(r['coeff'],sum(x*y for x,y in zip(r['q'],a))) for r in selected),F(0))
        expected = reference(a0)
        assert value == expected, (a,value,expected)
        result.append({'a':a,'value':str(value),'trees':len(selected),'wall':any(sum(a[:i])==0 for i in range(1,6))})
    save(Path(out)/'RESULT.json', {'status':'PASS_COMPLETE_DECLARED_ROOT_CUBE','cases':result,
        'case_count':len(result),'support_faces_included':True,'elapsed_seconds':time.monotonic()-started})

if __name__ == '__main__':
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for linear-coefficient tree data')
    if sys.argv[1] == 'build': build(sys.argv[2],int(sys.argv[3]))
    elif sys.argv[1] == 'roots': roots(sys.argv[2],sys.argv[3])
    else: raise ValueError('Unknown fixed mode')
