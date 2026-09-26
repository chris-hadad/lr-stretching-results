#!/usr/bin/env python3
"""Exact original-row and six-branch polygon controls; Python standard library."""
import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

NAMES = ['h12','h13','h14','h15','h23','h24','h25','h34','h35','h45']
GROUPS = {
    'left': [0,1,2,5,6,15,16,17,20,21,22,30,31,32,35,36],
    'right': [10,11,12,13,14,25,26,27,28,29,37,40,41,42,43,44],
    'middle': [3,4,7,8,18,19,23,33,34,38],
    'base': [9,24,39],
}
BASE = (2,4,5,6,7)
BOX = [(23,25),(29,33),(34,38),(38,40),(34,38),(39,46),(44,48),(44,48),(49,53),(53,55)]
DEFAULT_SOURCE = Path(__file__).resolve().parent / 'data/delta-rows.json'


def ceildiv(a, b):
    assert b > 0
    return -((-a)//b)


def polygon(A0, A1, B0, B1, D0, D1, S, with_branches=False):
    """All integer (a,b): rectangle, D0<=a-b<=D1, a+b>=S.
    Lower/upper selector ties choose the first listed affine function.
    """
    if A0>A1 or B0>B1 or D0>D1:
        return (0, []) if with_branches else 0
    lower = [(0,A0),(1,D0),(-1,S)]
    upper = [(0,A1),(1,D1)]
    total, records = 0, []
    for li,(lm,lc) in enumerate(lower):
        for ui,(um,uc) in enumerate(upper):
            lo,hi = B0,B1
            conditions = [(lm-m, lc-c-int(k<li)) for k,(m,c) in enumerate(lower) if k!=li]
            conditions += [(m-um, c-uc-int(k<ui)) for k,(m,c) in enumerate(upper) if k!=ui]
            conditions += [(um-lm, uc-lc)]
            feasible=True
            for m,c in conditions:
                # m*b+c >= 0, including once-only tie shifts above.
                if m>0: lo=max(lo,ceildiv(-c,m))
                elif m<0: hi=min(hi,c//(-m))
                elif c<0:
                    feasible=False
                    break
            if feasible and lo<=hi:
                n=hi-lo+1
                count=(um-lm)*(lo+hi)*n//2+(uc-lc+1)*n
                assert count>=n>0
                total+=count
                if with_branches:
                    records.append({'lower':li,'upper':ui,'lo':lo,'hi':hi,'count':count})
    return (total,records) if with_branches else total


def left_parameters(t,c,e,f,g,h):
    return (max(23*t,e-13*t), min(25*t,e-11*t),
            max(c-6*t,c+e-f,24*t-c+f), min(c-4*t,c+f-g,e+f-h),
            max(-8*t,28*t-e), min(-6*t,e-f), e+18*t)


def right_parameters(t,c,e,f,g,h):
    return (max(53*t,h+7*t), min(55*t,h+9*t),
            max(g+h-f,54*t+f-g,g+4*t), min(g+6*t,-e+f+h,-c+f+g),
            max(48*t-h,2*t), min(4*t,h-f), 58*t+h)


def middle(t,c,e,f,g,h):
    lo=max(38*t,c+2*t,g-8*t,48*t+c-g,28*t-c+g)
    hi=min(40*t,c+4*t,c-f+g,g-6*t)
    return max(0,hi-lo+1)


def base_points(t):
    # Original certified box; original rows 24/39 tighten h, row 9 tightens f.
    for c in range(34*t,38*t+1):
      for e in range(34*t,38*t+1):
        for h in range(max(44*t,e+9*t),min(48*t,e+11*t)+1):
          for f in range(39*t,min(46*t,e+h-39*t)+1):
            for g in range(44*t,48*t+1):
              yield c,e,f,g,h


def load_source(path):
    raw=path.read_bytes()
    obj=json.loads(raw)
    assert obj['box_bounds']==[list(b) for b in BOX]
    rows=[(int(r['beta']),tuple(r['normal'])) for r in obj['original_rows']]
    assert len(rows)==45
    return rows,hashlib.sha256(raw).hexdigest()


def graph_check(rows):
    adj=[set() for _ in NAMES]
    for _,normal in rows:
        support=[i for i,v in enumerate(normal) if v]
        for i in support:
            adj[i].update(j for j in support if j!=i)
    assert sorted(i for group in GROUPS.values() for i in group)==list(range(45))
    for label,private in [('left',{0,1}),('right',{8,9}),('middle',{3})]:
        expected=[i for i,(_,n) in enumerate(rows) if any(n[j] for j in private)]
        assert expected==GROUPS[label],(label,expected)
    core={1,2,4,5,6,7,8}
    opposite={frozenset(p) for p in [(1,8),(2,7),(4,6)]}
    for u,v in itertools.combinations(core,2):
        assert (v in adj[u])==(frozenset((u,v)) not in opposite)
    assert min(len(adj[v]&core) for v in core)==5
    order=[0,3,9,1,8,2,4,5,6,7]
    work=[set(v) for v in adj]
    alive=set(range(10)); separators=[]
    for v in order:
        sep=sorted(work[v]&alive)
        separators.append({'variable':NAMES[v],'separator':[NAMES[u] for u in sep]})
        for u in sep: work[u].update(w for w in sep if w!=u)
        alive.remove(v)
    assert max(len(s['separator']) for s in separators)==5
    return {'treewidth':5,'lower_certificate':'induced K_{2,2,2,1} has minimum degree 5',
            'order':separators,'groups':GROUPS,'core_opposite_pairs':[[NAMES[v] for v in p] for p in [(1,8),(2,7),(4,6)]]}


def direct(rows, group, t, base, private):
    x=[0]*10
    for j,v in zip(BASE,base): x[j]=v
    count=0
    for values in itertools.product(*(range(BOX[j][0]*t,BOX[j][1]*t+1) for j in private)):
        for j,v in zip(private,values): x[j]=v
        if all(beta*t+sum(a*b for a,b in zip(n,x))>=0 for beta,n in (rows[i] for i in GROUPS[group])):
            count+=1
    return count


def verify_fields(rows,t):
    checked=0; empty={'left':0,'right':0,'middle':0}; selector_ties=0
    # All original base-box lattice points, including failures of the base rows.
    for base in itertools.product(*(range(BOX[j][0]*t,BOX[j][1]*t+1) for j in BASE)):
        vals={'left':polygon(*left_parameters(t,*base)), 'right':polygon(*right_parameters(t,*base)), 'middle':middle(t,*base)}
        for label,private in [('left',(0,1)),('right',(8,9)),('middle',(3,))]:
            expected=direct(rows,label,t,base,private)
            assert vals[label]==expected,(t,base,label,vals[label],expected)
            empty[label]+=int(expected==0)
        checked+=1
    # Literal polygon fixtures: zero, empty, a strict once-only selector tie,
    # and period-two triangle with odd analytic constant 3/4.
    for s in range(9):
        expected=(s+1)*(s+2)//2 # integer triangle a+b>=s in [0,s]^2.
        assert polygon(0,s,0,s,-s,s,s)==expected
        # a>=b and a+b>=s; direct bare polygon as independent control.
        got=polygon(0,s,0,s,0,s,s)
        bare=sum(a>=b and a+b>=s for a in range(s+1) for b in range(s+1))
        assert got==bare
    assert polygon(0,0,0,0,0,0,0)==1
    assert polygon(0,0,0,0,0,0,1)==0
    return {'grade':t,'base_box_fields':checked,'empty_fields':empty,'fixture_grades':list(range(9))}


def count(t):
    total=0; visited=0; nonzero=0
    for base in base_points(t):
        visited+=1
        m=middle(t,*base)
        if not m: continue
        l=polygon(*left_parameters(t,*base))
        if not l: continue
        r=polygon(*right_parameters(t,*base))
        if not r: continue
        total+=l*r*m; nonzero+=1
    return {'grade':t,'whole_count':total,'base_states':visited,'nonzero_states':nonzero}


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for five-height interface checking')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=DEFAULT_SOURCE)
    ap.add_argument('--verify-fields',type=int,action='append',default=[])
    ap.add_argument('--count-grade',type=int,action='append',default=[])
    args=ap.parse_args(); started=time.monotonic()
    rows,sha=load_source(args.source)
    result={'schema':'astra053-five-height-interface/v1','source_sha256':sha,'structure':graph_check(rows),'field_checks':[],'counts':[]}
    for t in args.verify_fields:
        assert t>=0; result['field_checks'].append(verify_fields(rows,t))
    for t in args.count_grade:
        assert t>=0; result['counts'].append(count(t))
    result['seconds']=time.monotonic()-started
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
