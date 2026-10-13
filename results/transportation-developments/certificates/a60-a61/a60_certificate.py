"""Complete accepted A60 finite bases, derivatives and product certificates."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,argparse,time
from polynomial_arithmetic import add,mul,scale,binpoly,at,serial,dominates

def correction(a,B,m1,m2):
    A=[2,F(2*B-3,2)]
    tail=add(mul(A,binpoly(3,2*a-1,2*a+1)),binpoly(3,2*a-1,2*a+2))
    cap=[]
    for k in (1,2):
        v=[2,k];s=3-k
        cap.append(add(mul(v,A,binpoly(s,2*a-3,2*a)),mul(add(v,A),binpoly(s,2*a-3,2*a+1)),binpoly(s,2*a-3,2*a+2)))
    v=[2,1]
    pair=add(mul(v,v,A,binpoly(1,2*a-5,2*a-1)),mul(add(mul(v,v),scale(mul(v,A),2)),binpoly(1,2*a-5,2*a)),mul(add(scale(v,2),A),binpoly(1,2*a-5,2*a+1)),binpoly(1,2*a-5,2*a+2))
    total=add(scale(tail,2),scale(cap[0],-2*m1),scale(cap[1],-2*m2),scale(pair,2*comb(m1,2)))
    return dict(total=total,tail=tail,C1=cap[0],C2=cap[1],pair=pair)

def formula(caps):
    a=len(caps);K=sum(caps);B=K-3
    N=mul(*[binpoly(k,2,2) for k in caps])
    L=F(5*K,4)-6;Q=F(4*(2*K-9)**2-sum(k*k for k in caps),36)
    R=correction(a,B,caps.count(1),caps.count(2))
    P=add(mul(N,[1,L,Q]),R['total'])
    return dict(a=a,K=K,B=B,N=N,L=L,Q=Q,P=P,**R)

def finite_bases():
    rows=[]
    for a in (3,4,5):
        for m1 in range(a+1):
            for m2 in range(a-m1+1):
                m3=a-m1-m2;caps=[1]*m1+[2]*m2+[3]*m3
                if sum(caps)<6:
                    if m3==0:continue
                    assert caps==[1,1,3]
                    caps[-1]=4
                d=formula(caps)
                assert d['L']>0 and d['Q']>0
                assert len(d['P'])==2*a+3 and all(x>0 for x in d['P']),(caps,'base',d['P'])
                derivative=None
                if m3:
                    j=len(caps)-1;k=caps[j]
                    Nj=mul(*[binpoly(v,2,2) for i,v in enumerate(caps) if i!=j],[0,F(3,2),k])
                    Qj=F(16*d['K']-72-k,18);assert Qj>0
                    delta=add(correction(a,d['B']+1,m1,m2)['total'],scale(d['total'],-1))
                    derivative=add(mul(Nj,[1,d['L'],d['Q']]),mul(d['N'],[0,F(5,4),Qj]),delta)
                    assert derivative[0]==0 and all(x>0 for x in derivative[1:]),(caps,'first-derivative',derivative)
                rows.append(dict(caps=caps,m1=m1,m2=m2,m3=m3,degree=2*a+2,coefficients=d['P'],large_cap_derivative=derivative,variable_domain='each cap >=3 grows independently from displayed base; the single (1,1,4) cap grows from 4'))
    assert len(rows)==40
    return rows

def E(n,s=1):return mul(*[[1,F(s,j)] for j in range(1,n+1)])

def large_base():
    a=6;N=mul(*[[1,1],[1,F(1,2)]]*a)
    e=E(2*a-1,3);m=mul(E(2*a-3,2),[1,2],[1,1],[1,1])
    assert dominates(scale(N,F(3,2)),e)
    assert dominates(scale(N,F(3,2)),m)
    return dict(a=a,N=N,E3=e,M2=m,E3_residual=add(scale(N,F(3,2)),scale(e,-1)),M2_residual=add(scale(N,F(3,2)),scale(m,-1)),E3_max_ratio=max(x/y for x,y in zip(e,N)),M2_max_ratio=max(x/y for x,y in zip(m,N)))

def factorizations(a,B):
    n=2*a;c=F(2*B-3,2);H=(n+1)*(n+2);D=n*(n-1)*(n-2);D4=(n-1)*(n-2)*(n-3)*(n-4)
    f0=F(4)-F(12,n+1)+F(12,H)
    result={};r=correction(a,B,a,0)
    for k in (1,2):
        s=3-k;f1=2*(k+c)+F(4*s,n+1)-F(3,n+1)*(k+c)-F(7*s,H);f2=k*c+F(s,n+1)*(k+c)+F(s*s,H)
        f=[f0,f1,f2];assert all(x>0 for x in f)
        fmax=mul([1,1],[f0,(2 if k==1 else 3)*B]);assert dominates(fmax,f)
        fact=scale(mul(E(n-3,s),[0,s],[-1,s],[-2,s],f),F(1,D));assert fact==r['C'+str(k)]
        result['f'+str(k)]=f
    fd=[F(8)-F(48,n)+F(120,n*(n+1))-F(120,n*(n+1)*(n+2)),4*c+8+(-16*c-20)/n+(20*c-14)/(n*(n+1))+F(74,n*(n+1)*(n+2)),4*c+2+(4-4*c)/n+(-9*c-12)/(n*(n+1))-F(15,n*(n+1)*(n+2)),c+(2*c+1)/n+(c+2)/(n*(n+1))+F(1,n*(n+1)*(n+2))]
    assert all(x>0 for x in fd) and 4<=fd[0]<=8
    assert dominates(mul([1,1],[1,1],[fd[0],4*B]),fd)
    fact=scale(mul(E(n-5),[0,1],[-1,1],[-2,1],[-3,1],fd),F(1,D4));assert fact==r['pair']
    result['fd']=fd
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();start=time.monotonic()
    rows=finite_bases();base=large_base();factor_checks=[]
    for a in (6,7,10,32):
        for B in (3,7,100):factor_checks.append(dict(a=a,B=B,**factorizations(a,B)))
    shapes=[[1]*6,[1]*7,[1]*20,[1,1,1,1,1,50],[1,2,2,3,4,7]]
    reserve=[]
    for caps in shapes:
        d=formula(caps);a=d['a'];r=d['K']-6
        ell=F(139,140)+F(5,4)*r;q=F(47,780)+F(2387,2340)*r+F(5,12)*r*r
        lower=mul(d['N'],[1,ell,q]);assert dominates(d['P'],lower),(caps,'large-reserve')
        reserve.append(dict(caps=caps,coefficients=d['P'],lower=lower,residual=add(d['P'],scale(lower,-1))))
    result=dict(status='PASS',schema='a60-k3-certificate/v1',finite_bases=rows,large_base=base,factor_checks=factor_checks,reserve_controls=reserve,seconds=time.monotonic()-start,scope='Exact finite base certificates and checked factorizations; the accompanying proof supplies all infinite quantifiers. No original LR count is computed here.')
    with args.out.open('x') as f:json.dump(serial(result),f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',finite_bases=len(rows),large_E_ratio=str(base['E3_max_ratio']),large_M_ratio=str(base['M2_max_ratio']),seconds=time.monotonic()-start)),flush=True)

if __name__=='__main__':main()
