"""Exact finite controls for the complete affine private-polygon projection."""
import itertools, json, random, sys
from fractions import Fraction as F
from pathlib import Path

def formula(am,ap,bm,bp,dm,dp,s):
    low=list(map(F,bm))+[F(a-d) for a in am for d in dp]+[F(s-a) for a in ap]+[F(s-d,2) for d in dp]
    high=list(map(F,bp))+[F(a-d) for a in ap for d in dm]
    assertions=[a<=b for a in am for b in ap]+[a<=b for a in dm for b in dp]+[a<=b for a in low for b in high]
    return all(assertions),max(low),min(high),len(assertions)

def literal(am,ap,bm,bp,dm,dp,s):
    return [(x,z) for x in range(max(am),min(ap)+1) for z in range(max(bm),min(bp)+1)
            if all(x-z>=d for d in dm) and all(x-z<=d for d in dp) and x+z>=s]

def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for five-height projection controls')
    counts={'cases':0,'empty':0,'singleton':0,'multiple':0,'half_integral_lower':0,'tied_lower_selectors':0,'full_101_presentations':0}
    inputs=[]
    for vals in itertools.product((-1,0,1),repeat=7):
        a0,a1,b0,b1,d0,d1,s=vals;inputs.append(([a0],[a1],[b0],[b1],[d0],[d1],s))
    rng=random.Random(540229)
    for k in range(10000):
        inputs.append(tuple([rng.randrange(-3,4) for _ in range(n)] for n in [3,2,3,3,2,2])+(rng.randrange(-3,4),))
    for am,ap,bm,bp,dm,dp,s in inputs:
        feasible,p,q,n=formula(am,ap,bm,bp,dm,dp,s);points=literal(am,ap,bm,bp,dm,dp,s)
        assert feasible==bool(points),(am,ap,bm,bp,dm,dp,s,feasible,points)
        counts['cases']+=1;counts['empty' if not points else 'singleton' if len(points)==1 else 'multiple']+=1
        counts['half_integral_lower']+=p.denominator==2;counts['full_101_presentations']+=n==101
        if points:
            z=-(-p.numerator//p.denominator);x=max(max(am),z+max(dm),s-z)
            assert (x,z) in points and z<=q
            counts['tied_lower_selectors']+=len({max(am),z+max(dm),s-z})<3
    assert counts['half_integral_lower'] and counts['singleton'] and counts['empty'] and counts['tied_lower_selectors']
    result={'status':'PASS','counts':counts,'complete_original_projection_inequality_occurrences':229,'scope':'private affine kernel controls, not LR coefficient sampling or a global sign proof'}
    print(json.dumps(result))

if __name__=='__main__':main()
