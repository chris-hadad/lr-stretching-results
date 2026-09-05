"""Exact low-coefficient certificate for the rank-18 family W004-CONE-01.

Python standard library only. The default command verifies in memory.
Run `python3 reproduce.py --output-dir DIRECTORY` to regenerate certificate.json,
numerator.json, and flow-polynomial.json. See README.md for the theorem,
full Littlewood-Richardson embedding, and proof.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
from math import comb, factorial
import json

SCALE = factorial(22)
FACTORS = [((4,1),(1,0),(0,0))]*3 + [((5,0),(3,0),(0,0))] + \
          [((3,0),(2,0),(0,0))]*2 + [((5,-1),(1,0),(0,0))]*3

def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)

def evaluate(coefficients, parameter):
    value = F(0)
    for coefficient in reversed(coefficients):
        value = value*parameter+coefficient
    return value

def numerator():
    states = {(0,0,0,0,0,0):1}
    delta = (2,1,0)
    for factor in FACTORS:
        next_states = defaultdict(int)
        for p in permutations(range(3)):
            sign = (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
            increment = (*factor[p[0]],*factor[p[2]],delta[p[0]],delta[p[2]])
            for state,coefficient in states.items():
                next_states[tuple(x+y for x,y in zip(state,increment))] += sign*coefficient
        states = {s:c for s,c in next_states.items() if c}
    return states

@lru_cache(None)
def original_sum():
    # P(A,B,k) = product_i=1..7 (A-k+i)(k+i)(B-k+i).
    poly = {(0,0,0):1}
    for i in range(1,8):
        factors = ({(1,0,0):1,(0,0,1):-1,(0,0,0):i},
                   {(0,0,1):1,(0,0,0):i},
                   {(0,1,0):1,(0,0,1):-1,(0,0,0):i})
        for factor in factors:
            new = defaultdict(int)
            for exponent,c in poly.items():
                for delta,d in factor.items():
                    new[tuple(x+y for x,y in zip(exponent,delta))] += c*d
            poly = {e:c for e,c in new.items() if c}
    # S_j(B)=sum_(k=0)^B k^j, by telescoping finite differences.
    sums = []
    for j in range(22):
        coefficients = [F(comb(j+1,i)) for i in range(j+2)]
        for i,previous in enumerate(sums):
            for k,c in enumerate(previous):
                coefficients[k] -= comb(j+1,i)*c
        sums.append([c/F(j+1) for c in coefficients])
    q = defaultdict(F)
    for (a,b,k),c in poly.items():
        for j,d in enumerate(sums[k]):
            q[a,b+j] += c*d*F(SCALE,factorial(7)**3)
    require(all(v.denominator == 1 for v in q.values()),'nonintegral 22! scaling')
    return {e:int(c) for e,c in q.items() if c}

@lru_cache(None)
def taylor(c,d):
    # Coefficients of 1,A,B,A^2,AB,B^2 in Q(A+c,B+d).
    return tuple(sum(v*comb(a,i)*comb(b,j)*c**(a-i)*d**(b-j)
                     for (a,b),v in original_sum().items() if a>=i and b>=j)
                 for i,j in ((0,0),(1,0),(0,1),(2,0),(1,1),(0,2)))

def critical_values(states):
    walls = {F(-3),F(4)}
    for a,da,b,db,c,d in states:
        for constant,slope in ((a-17,da),(17-b,-db),(a+b-34,da+db)):
            if slope and -3 <= F(-constant,slope) <= 4:
                walls.add(F(-constant,slope))
    return sorted(walls)

def coefficients(states,parameter):
    """Use parameter to choose eventual branches; retain symbolic s powers."""
    output = [[0],[0,0],[0,0,0]]
    u,v = parameter.numerator,parameter.denominator
    for (a,da,b,db,c,d),multiplicity in states.items():
        aa,ab,ba,bb,cc,dd = a-17,da,17-b,-db,c-18,-d
        at,bt = aa*v+ab*u,ba*v+bb*u
        if (at,cc)<(0,0) or (bt,dd)<(0,0):
            continue
        if (at,cc)<(bt,dd):
            aa,ab,ba,bb,cc,dd = ba,bb,aa,ab,dd,cc
        q,qa,qb,qaa,qab,qbb = taylor(cc,dd)
        terms = [[q],[qa*aa+qb*ba,qa*ab+qb*bb],
                 [qaa*aa*aa+qab*aa*ba+qbb*ba*ba,
                  2*qaa*aa*ab+qab*(aa*bb+ab*ba)+2*qbb*ba*bb,
                  qaa*ab*ab+qab*ab*bb+qbb*bb*bb]]
        for k,row in enumerate(terms):
            for j,value in enumerate(row):
                output[k][j] += multiplicity*value
    return [[F(value,SCALE) for value in row] for row in output]

def certificate():
    states = numerator()
    walls = critical_values(states)
    require(len(states)==67458,'numerator cardinality')
    require(len(original_sum())==156,'literal flow polynomial cardinality')
    require(len(walls)==29,'critical arrangement cardinality')
    pieces = [coefficients(states,(a+b)/2) for a,b in zip(walls,walls[1:])]
    wall_values = [[evaluate(row,s) for row in coefficients(states,s)] for s in walls]
    for i,piece in enumerate(pieces):
        require(piece[0]==[1],'constant coefficient')
        require(piece[2][2]<0,'quadratic slice second derivative')
        for j in (i,i+1):
            require([evaluate(row,walls[j]) for row in piece]==wall_values[j],
                    'actual wall value differs from its chamber limit')
    slopes = [p[1][1] for p in pieces]
    require(all(a>=b for a,b in zip(slopes,slopes[1:])),'linear slope increase')
    jumps = []
    for i,s in enumerate(walls[1:-1],start=1):
        a,b = pieces[i-1][2],pieces[i][2]
        jump = a[1]+2*a[2]*s-b[1]-2*b[2]*s
        require(jump>0,'quadratic derivative jump not downward')
        jumps.append(jump)
    minima = [min(w[j] for w in wall_values) for j in (1,2)]
    require(minima==[F(275511,20020),F(704687791,7207200)],'coefficient minima')
    require(wall_values[0][1:]==minima==wall_values[-1][1:],'endpoint attainment')
    return {'status':'PASS','source':'independent reconstruction from nine factors',
            'ordinary_indices':[0,1,2],'prior_full_stretch_degree_bound':19,
            'numerator_states':len(states),'original_sum_monomials':len(original_sum()),
            'chambers':[{'left':a,'right':b,'coefficients_in_s':p} for a,b,p in zip(walls,walls[1:],pieces)],
            'walls':[{'s':s,'coefficients':c} for s,c in zip(walls,wall_values)],
            'c1_slopes':slopes,'c2_second_derivatives':[2*p[2][2] for p in pieces],
            'c2_downward_derivative_jumps':jumps,'normalized_minima':minima,
            'consequence':'c1 and sqrt(c2) are concave homogeneous degree1 and superadditive',
            'higher_ordinary_coefficients':'uncomputed'}

def boundary_generators():
    """Recover the explicit ordinary LR boundary on the two generator rays."""
    result = {}
    for name,parameter,expected_size in (('x',4,225),('y',-3,477)):
        blocks = [[a+b*parameter for a,b in factor[:2]] for factor in FACTORS]
        outer,inner = [],[]
        for i,block in enumerate(blocks):
            offset = sum(later[0] for later in blocks[i+1:])
            outer.extend(offset+row for row in block)
            inner.extend([offset]*len(block))
        while inner and inner[-1] == 0:
            inner.pop()
        require(all(a>=b for a,b in zip(outer,outer[1:])),'outer partition')
        require(all(a>=b for a,b in zip(inner,inner[1:])),'inner partition')
        require(sum(outer)==expected_size and sum(inner)+51==sum(outer),'LR size balance')
        result[name] = {'lambda_outer':outer,'mu':inner,'nu':[17,17,17]}
    return result

def write_evidence(output_directory):
    """Write deterministic mathematical evidence; no data files are inputs."""
    from pathlib import Path
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True,exist_ok=True)
    result = complete_certificate()
    states = numerator()
    evidence = {
        'certificate.json':result,
        'numerator.json':{
            'state_coordinates':['first_constant','first_s','third_constant','third_s',
                                 'first_delta','third_delta','signed_multiplicity'],
            'terms':[[*state,coefficient] for state,coefficient in sorted(states.items())]},
        'flow-polynomial.json':{
            'meaning':'22! F_(8,8,8)(A,B) on A>=B>=0',
            'scale':str(SCALE),
            'monomials_A_B_integer_coefficient':[[a,b,c] for (a,b),c in sorted(original_sum().items())]}}
    for name,data in evidence.items():
        indentation = None if name == 'numerator.json' else 2
        separators = (',',':') if indentation is None else None
        (output_directory/name).write_text(
            json.dumps(data,indent=indentation,separators=separators,default=str)+'\n',
            encoding='utf-8')
    return result

def complete_certificate():
    """Verify the coefficient theorem and its ordinary LR boundary together."""
    result = certificate()
    result['ordinary_lr_generators'] = boundary_generators()
    result['normalization'] = {'h':'x+y','s':'(4x-3y)/(x+y)','interval':['-3','4']}
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',help='Optional directory for three regenerated mathematical JSON files')
    arguments = parser.parse_args()
    result = write_evidence(arguments.output_dir) if arguments.output_dir else complete_certificate()
    print('Verified both ordinary LR generators, 67,458 numerator states, 28 open chambers, 29 walls, and both coefficient bounds.')
