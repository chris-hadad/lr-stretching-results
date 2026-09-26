"""Exact complete-jet, original-row and wall-factor readback."""
from pathlib import Path
from fractions import Fraction as Q
import json,sys,copy
from math_support import rows,cuts,project,factor,dot
ROOT=Path(__file__).resolve().parent

def check(data, jets):
    points=data['points'];A=rows();E=[-1]*6+[1]*12+[0]*10;C=cuts()
    cut=[0]*18
    for i in data['U']:cut[i]=-1
    for i in data['I']:cut[6+i]=1
    for i in data['J']:cut[12+i]=1
    values=[]
    for p in points:
        b=p['boundary'];h=p['internal'];assert len(b)==18 and len(h)==10
        assert dot(E,b+h)==0 and min(dot(a,b+h) for a in A)>0
        cv=[dot(c,b) for _,_,_,c in C]
        assert sum(x==0 for x in cv)==int(p['id']=='stress-midpoint')
        if p['id']=='stress-midpoint':assert all(c==cut for (_,_,_,c),v in zip(C,cv) if v==0)
        a,z=[j[p['id']] for j in jets]
        assert a['weyl_pairs_considered']==z['weyl_pairs_considered']==518400
        assert Q(a['c1'])==Q(z['c1'])==dot(a['gradient'],b)==dot(z['gradient'],b)>0
        assert project([Q(x)-Q(y) for x,y in zip(a['gradient'],z['gradient'])],cut if p['id']=='stress-midpoint' else None)==[0]*18
        values.append(Q(a['c1']))
    assert values==list(map(Q,data['c1_values']))
    assert all(a+b==2*m for a,m,b in zip(*(p['boundary'] for p in points)))
    assert [dot(cut,p['boundary']) for p in points]==[1,0,-1]
    cv=[[dot(c,p['boundary']) for _,_,_,c in C] for p in points]
    assert sum((a>0)!=(b>0) for a,b in zip(cv[0],cv[2]))==1
    defect=(values[0]+values[2])/2-values[1];assert defect==Q(1,336)
    gplus=jets[0][points[0]['id']]['gradient'];gminus=jets[0][points[2]['id']]['gradient']
    assert project([Q(a)-Q(b) for a,b in zip(gplus,gminus)])==[Q(v,168) for v in cut]
    U,I,J=[data[k] for k in ['U','I','J']];complement=lambda a:[i for i in range(6) if i not in a]
    au,ru=factor(points[1]['boundary'],U,I,J,2);av,rv=factor(points[1]['boundary'],complement(U),complement(I),complement(J),7)
    assert (au,av)==(Q(-1,3),Q(1)) and (ru['lower_length'],rv['lower_length'])==('4012','9204')
    assert -au*av/Q(8*7)==Q(1,168)
    for cert in data['gradient_certificates']:
        g=list(map(Q,cert['gradient']));weights=cert['certificate'];assert len(g)==28 and g[18:]==[0]*10
        assert len({i for i,w in weights})==len(weights) and all(Q(w)>=0 and 0<=i<63 for i,w in weights)
        assert [sum((Q(w)*A[i][j] for i,w in weights),Q(0))+Q(cert['trace_weight'])*E[j] for j in range(28)]==g
        assert project(g[:18])==project(jets[0][cert['id']]['gradient'])
    return {'first_jets':list(map(str,values)),'jensen_defect':'1/336','addition_defect':'-1/168','complete_cut_checks':3*7591,'all_original_rows':63,'exact_duals':2}

def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for linear-coefficient witness checking')
    data=json.loads((ROOT/'data/witness.json').read_text())
    jets=[{r['id']:r for r in json.loads(Path(p).read_text())['cases']} for p in sys.argv[1:]]
    assert len(jets)==2 and all(set(j)=={p['id'] for p in data['points']} for j in jets)
    result=check(data,jets);bad=copy.deepcopy(data);bad['points'][1]['boundary'][0]+=1
    try:check(bad,jets)
    except AssertionError:pass
    else:raise AssertionError('Changed boundary accepted')
    bad=copy.deepcopy(data);bad['gradient_certificates'][0]['certificate'][0][1]='-1'
    try:check(bad,jets)
    except AssertionError:pass
    else:raise AssertionError('Negative dual weight accepted')
    print(json.dumps({'status':'PASS',**result,'negative_controls':2}))
if __name__=='__main__':main()
