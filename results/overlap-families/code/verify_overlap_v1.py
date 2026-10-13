"""Locally authored exact formal-polynomial verifier; no LR or SOURCE code execution.

Determining and validating phases never open another phase's output. Join is
explicit and follows both immutable freezes. Only the named proof inputs may be
hashed. Polynomial primitives are shared; the load-bearing constructions differ.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import time

TARGET = Path(__file__).resolve().parents[1]
METHOD = Path(__file__).resolve().parent
RAW = None  # A caller-selected fresh output root, never a private path.
SOURCES = ['proofs/A83-ORIGINALS-AND-BASES-v1.md','proofs/A83-OVERLAP-GENERATORS-v1.md']
DIM = 2

class P:
    def __init__(self, data=0):
        if isinstance(data, P):
            self.c = data.c
        elif isinstance(data, dict):
            self.c = {m:F(c) for m,c in data.items() if c}
        else:
            self.c = {(0,)*DIM:F(data)} if data else {}
        self._hash = None
    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(sorted(self.c.items())))
        return self._hash
    def __eq__(self, other):
        return self.c == P(other).c
    def __add__(self, other):
        b = P(other).c
        if not b: return self
        if not self.c: return P(other)
        out = self.c.copy()
        for m,c in b.items():
            out[m] = out.get(m,0)+c
            if not out[m]: del out[m]
        return P(out)
    __radd__ = __add__
    def __neg__(self): return P({m:-c for m,c in self.c.items()})
    def __sub__(self, other): return self + -P(other)
    def __rsub__(self, other): return P(other) + -self
    def __mul__(self, other):
        b = P(other).c
        if not b or not self.c: return P()
        zero = (0,)*DIM
        if list(b) == [zero]: return P({m:c*b[zero] for m,c in self.c.items()})
        if list(self.c) == [zero]: return P({m:c*self.c[zero] for m,c in b.items()})
        out = {}
        for m,c in self.c.items():
            for n,d in b.items():
                z = tuple(a+b for a,b in zip(m,n))
                out[z] = out.get(z,0)+c*d
        return P(out)
    __rmul__ = __mul__
    def __truediv__(self, other): return self*F(1,other)
    def diff(self, i):
        return P({tuple(k-(j==i) for j,k in enumerate(m)):c*m[i]
                  for m,c in self.c.items() if m[i]})
    def subzero(self,i): return P({m:c for m,c in self.c.items() if m[i]==0})
    def homogeneous(self,d): return P({m:c for m,c in self.c.items() if sum(m)==d})
    def evaluate(self, values):
        return sum(c*prod(v**e for v,e in zip(values,m)) for m,c in self.c.items())
    def positive(self): return all(c>=0 for c in self.c.values())
    def degree(self): return max((sum(m) for m in self.c),default=-1)

def prod(xs):
    z=1
    for x in xs:z=z*x
    return z

def var(i):
    return P({tuple(int(j==i) for j in range(DIM)):F(1)})

def reset(dim):
    global DIM
    DIM=dim
    for fn in (A,d,q,C,Sdet):fn.cache_clear()

@lru_cache(None)
def A(n,x):
    if n<0:return P()
    return prod((x+j)/j for j in range(1,n+1))*P(1)

@lru_cache(None)
def d(n,x):
    if n<0:return P()
    return prod((x+j)/(j+1) for j in range(n))*P(1)

@lru_cache(None)
def q(a,m,B,z):
    if a<0 or m < -1:return P()
    if m==-1:return A(a,B)
    if m>a-1:return P()
    return A(a,B)*d(m+1,z)-A(m,B+1)*(d(a+1,z)-d(a,z))

@lru_cache(None)
def C(n,k,l,B,z):
    return q(n,n-k-l-1,B,z)+sum((q(n-1-i,n+i-k-l,B,z)-q(n-1-i,n+i-k-l-1,B,z))
                                 for i in range(min(k,l)))

def r_series(k):
    out=Counter({(i,k-i):1 for i in range(k+1)})
    if k:
        out.subtract({(i+1,k-i):1 for i in range(k)})
    return {m:c for m,c in out.items() if c}

def series_product(a,b):
    out=Counter()
    for (i,j),c in a.items():
        for (k,l),e in b.items():out[i+k,j+l]+=c*e
    return {m:c for m,c in out.items() if c}

def C_aux(n,k,l,B,z):
    # Independent extraction of the complete rectangular series, not the q chain.
    out=P()
    for (i,j),weight in series_product(r_series(k),r_series(l)).items():
        out += weight*(d(n-i,B+2)*d(n-j,z)-d(n-1-i,B+2)*d(n+1-j,z))
    return out

def G(a,b,X,Y):
    return sum((d(i,X)*A(a+b+1-i,Y) for i in range(a+1)),P())

def Fconv(a,b,X,Y):
    return sum((d(i,X)*A(a+b+1-i,Y)*((a-i+1)*Y+a+b-i+2)/(a+b-i+2)
                for i in range(a+1)),P())

def G_antidifference(a,b,X,Y):
    # Newton's exact polynomial antidifference of the original finite integrand.
    values=[A(a,X+s)*A(b,Y-s) for s in range(a+b+1)]
    out=P()
    for order in range(a+b+1):
        falling=prod((Y+1-j)/(j+1) for j in range(order+1))*P(1)
        out += values[0]*falling
        values=[values[i+1]-values[i] for i in range(len(values)-1)]
    return out

def near_signed(n,a,v,w,r):
    return sum((d(i,w)*A(2*n-i,a+v+r) for i in range(n+1)),P()) \
      -sum((A(i,v+w+r)*d(2*n-i,a) for i in range(n)),P()) \
      -sum((A(i,a+w+r)*d(2*n-i,v) for i in range(n+1)),P())

def near_phi(n,k,l,a,v):
    T=n-k-l;N=2*n-k-l
    if T<0:return A(N,a+v)
    return A(T,a)*A(n-1,v)+sum((A(b,v)*d(N-b,a) for b in range(T,n)),P())

def near_positive(n,a,v,w,r):
    return sum((d(k,r)*d(l,w)*near_phi(n,k,l,a,v)
                for k in range(2*n+1) for l in range(min(n,2*n-k)+1)),P())

def near_full_cone(n,cone):
    a,v,w,r=[var(i) for i in range(4)]
    # One gap coordinate stays in the ordinary field even where independent.
    if cone=='both_unborn':
        U=v;ss=U+w;delta=U+r; vv=ww=P();rho=U;negative=True
    elif cone=='S_first':
        ss=v;U=v+w;delta=U+r;vv=P();ww=w;rho=v;negative=False
    elif cone=='delta_first':
        delta=v;U=v+w;ss=U+r;vv=w;ww=P();rho=v;negative=True
    else:
        vv=v;ww=w;rho=r;U=v+w+r;ss=v+r;delta=w+r;negative=False
    c=a+ss
    initial=A(2*n,a+U) if negative else G(n,n-1,U-ss,c)
    # Complete sector walls contain zero factors in these polynomial branches.
    complete=initial-G(n-1,n,U+1,a-1)
    if cone in ('delta_first','both_born'):
        complete-=G(n,n-1,a+delta+1,U-delta-1)
    return complete,near_positive(n,a,vv,ww,rho)

def far_raw(n,a,delta,ss,z):
    return G(n,n-1,delta+z,a+ss+z)-G(n-1,n,ss+delta+z+1,a+z-1) \
       -G(n,n-1,a+delta+z+1,ss+z-1)+G(n-1,n,a+ss+delta+z+2,z-2)

def far_Q(n,k,l,ss,z):
    T=2*n-k-l;Y=ss+z
    return sum((d(r,z)*A(T-r,Y) for r in range(n-l+1)),P()) \
      -sum((A(r,Y)*d(T-r,z) for r in range(n-l)),P()) \
      -sum((A(r,z)*d(T-r,Y) for r in range(n-k-l+1)),P()) \
      +sum((d(r,Y+2)*A(T-r,z-2) for r in range(n-k-l)),P())

def balanced_diff(lo,hi,target_lo,target_hi,z):
    assert lo+hi==target_lo+target_hi and lo<=target_lo<=target_hi<=hi
    out=P()
    while lo<target_lo:
        out += z*(F(1,lo+1)-F(1,hi))*A(lo,z)*A(hi-1,z)
        lo+=1;hi-=1
    assert (lo,hi)==(target_lo,target_hi)
    return out

def far_R_positive(n,p,q0,h,z,log=None):
    p,q0=max(p,q0),min(p,q0)
    t0=p+q0-n;M=p+q0-h;r=p-h-1;v=t0-h-1
    if r<0:out=P()
    elif v<0:out=A(q0,z)*A(r,z)
    else:
        out=balanced_diff(v,n,min(q0,r),max(q0,r),z)
        if v==0:out+=A(n-1,z)
        else:out+=A(v-1,z+1)*A(n-1,z)*(1+(1-F(v,n))*z)/v
    plus=set(range(t0+1,q0+1));minus=set(range(t0-h,q0-h))
    common=plus&minus; plus-=common;minus-=common
    assert len(plus)==len(minus)
    pairs=list(zip(sorted(minus),sorted(plus,reverse=True)))
    def f(i):return A(i,z)*d(M-i,z) if 0<=i<=M else P()
    for i,j in pairs:
        assert j>i
        if i<0:
            piece=f(j)
        else:
            assert i+j<=M-1 and 0<=i<=j<M
            piece=z/F(M-j)*balanced_diff(i,M-i-1,min(j,M-j-1),max(j,M-j-1),z) \
               +z*(F(1,M-j)-F(1,M-i))*A(i,z)*A(M-i-1,z)
        assert piece.positive()
        out+=piece
    if log is not None:
        log.append(dict(n=n,p=p,q=q0,h=h,M=M,determinant_v=v,
                        cancelled=sorted(common),pairs=pairs,remaining_fM=M in plus))
    return out

def far_positive(n,a,delta,ss,z,log=None):
    return sum((d(k,a)*d(l,delta)*d(h,ss)*far_R_positive(n,n-k,n-l,h,z,log)
                for k in range(n+1) for l in range(n+1) for h in range(n)),P())

def Qgain(p,X,Y):
    return sum((A(l,X)*d(2*p+1-l,Y) for l in range(p+1)),P())

def fixed_gain_raw(p,cone):
    a,e,x,y=[var(i) for i in range(4)]
    if cone=='first':return Qgain(p,a,e)
    if cone=='single':return Qgain(p,a,e+x)-Qgain(p,a+e,x)
    if cone=='middle':
        return Qgain(p,a,e+x+y)-Qgain(p,a+e+x,y)-Qgain(p,a+e+y,x)
    return Qgain(p,a+y,e+x+y)-Qgain(p,a+y+e,x+y) \
       -Qgain(p,a+y+x,e+y)+Qgain(p,a+y+e+x,y)

def sequence(i,j,r):
    return sum(1 for x in range(i) for y in range(j) if x+y==r)

@lru_cache(None)
def Sdet(u,v,z):
    if u<v or v<0:return P()
    return F(u-v+1,u+1)*A(u,z)*d(v,z)

def Sstep(u,v,z):
    return A(u,z)*d(v,z)*((u-v+2)*z+v)/((u+1)*(u+2))

def gain_R_paid(p,k,i,j,z,log=None):
    PP=p-k;N=2*p+1-k-i-j
    if N<0:return P()
    out=P()
    for r in range((N-1)//2+1):
        beta=sequence(i,j,PP-r)-sequence(i,j,p-r)
        gamma=sequence(i,j,p-1-r)-sequence(i,j,PP-r)
        assert beta>=0 and beta+gamma>=0
        out+=beta*Sstep(N-1-r,r,z)+(beta+gamma)*Sdet(N-1-r,r,z)
        if log is not None:log.append(dict(p=p,k=k,i=i,j=j,N=N,r=r,beta=beta,gamma=gamma))
    if N%2==0:
        r=N//2;beta=sequence(i,j,PP-r)-sequence(i,j,p-r)
        assert beta>=0
        out+=beta*Sdet(r,r,z)
        if log is not None:log.append(dict(p=p,k=k,i=i,j=j,N=N,r=r,beta=beta,gamma=None,terminal=True))
    return out

def gain_phi_paid(p,i,k,x,y):
    N=2*p+1-i-k;T=p-i-k;qq=p-i
    if T<0:
        if qq<0:return A(N,x+y)
        return sum((d(r,x+y) for r in range(qq+1,N+1)),P())
    out=P()
    for v in range(p+1):
        top=p if v<=T else N-v
        if v<=qq:
            tail=sum((d(j,y) for j in range(qq-v+1,top+1)),P())
        else:tail=A(top,y)
        out+=d(v,x)*tail
    return out

def fixed_gain_positive(p,cone,log=None):
    a,e,x,y=[var(i) for i in range(4)]
    if cone=='first':
        return sum((A(l,a)*d(2*p+1-l,e) for l in range(p+1)),P())
    if cone=='single':
        return sum((d(i,e)*A(l,a)*d(2*p+1-i-l,x)
                    for i in range(1,2*p+2)
                    for l in range(max(0,p-i+1),min(p,2*p+1-i)+1)),P())
    if cone=='middle':
        return sum((d(i,e)*d(k,a)*gain_phi_paid(p,i,k,x,y)
                    for k in range(p+1) for i in range(2*p+2-k)),P())
    return sum((d(k,a)*d(i,e)*d(j,x)*gain_R_paid(p,k,i,j,y,log)
                for k in range(p+1) for i in range(1,2*p+2-k)
                for j in range(1,2*p+2-k-i)),P())

def pre_raw(n,r,kind,cone):
    e,x,y=[var(i) for i in range(3)]
    D=n+r+(kind=='onezero');upper2=r if kind=='onezero' else r-1
    if cone=='first':return d(D,x)
    if cone=='single1':
        return d(D,e+x)-sum((A(i,e)*(d(D-i,x)-d(D-i-1,x)) for i in range(r)),P())
    if cone=='single2':
        return d(D,e+y)-sum((A(i,e)*(d(D-i,y)-d(D-i-1,y)) for i in range(upper2+1)),P())
    return d(D,e+x+y) \
       -sum((A(i,e+y)*(d(D-i,x)-d(D-i-1,x)) for i in range(r)),P()) \
       -sum((A(i,e+x)*(d(D-i,y)-d(D-i-1,y)) for i in range(upper2+1)),P())

def indicator_coefficient(n,r,kind,l,i,j):
    D=n+r+(kind=='onezero');sigma=l+i+j
    if sigma>=D:return F()
    I1=int(l+j<=r-1);I2=int(l+i<=(r if kind=='onezero' else r-1))
    result=F(1-I1-I2,D-sigma)
    if I1 and i<=(n if kind=='onezero' else n-1):result+=F(1,n+(kind=='onezero')-i)
    if I2 and j<=n-1:result+=F(1,n-j)
    return result

def pre_indicator(n,r,kind,log=None):
    e,x,y=[var(i) for i in range(3)];D=n+r+(kind=='onezero');out=P()
    for l in range(D):
        for i in range(D-l):
            for j in range(D-l-i):
                c=indicator_coefficient(n,r,kind,l,i,j)
                assert c>=0
                out+=c*d(l,e)*d(i,x)*d(j,y)
                if log is not None:
                    I1=l+j<=r-1;I2=l+i<=(r if kind=='onezero' else r-1)
                    if I1 and I2:
                        aa=D-l-i-j;bb=n+(kind=='onezero')-i;cc=n-j
                        assert aa-bb==r-l-j>=1
                        assert aa-cc==r+(kind=='onezero')-l-i>=1
                        log.append(dict(kind=kind,n=n,r=r,l=l,i=i,j=j,
                                        adverse_denominator=aa,partner_denominators=[bb,cc],
                                        strict_differences=[aa-bb,aa-cc],coefficient=str(c)))
    return out

def pre_positive_single(n,r,kind,which):
    e,x,y=[var(i) for i in range(3)]
    D=n+r+(kind=='onezero');v=x if which==1 else y
    cutoff=r if which==1 or kind=='balanced' else r+1
    lower=n+(kind=='onezero' and which==1)
    return sum((d(i,e)*d(D-i,v) for i in range(cutoff,D+1)),P())+A(cutoff-1,e)*d(lower,v)

def prefix_last(n,kind,algorithm):
    slack,z,H,G0=[var(i) for i in range(4)];B=slack+z
    if algorithm=='determining':
        if kind=='balanced':
            Z=H+G0+z
            out=G(n,n-1,B,Z-1)-G(n-1,n,B+H+1,Z-H-2) \
              -G(n-1,n,B+G0+1,Z-G0-2)+G(n-2,n+1,B+H+G0+2,z-3)
        else:
            Z=H+G0+z
            out=G(n,n,B,Z-1)-G(n-1,n+1,B+H+1,Z-H-2) \
              -G(n,n,B+G0+1,Z-G0-2)+G(n-1,n+1,B+H+G0+2,z-3)
    else:
        stop=n if kind=='balanced' else n+1
        out=sum((d(k,H)*d(l,G0)*C_aux(n,k,l if kind=='balanced' else max(l-1,0),B,z)
                  for k in range(n+1) for l in range(stop+1)),P())
    return out,out.diff(1)-out.diff(0)

def exponents(dim,total):
    if dim==1:
        yield (total,);return
    for a in range(total+1):
        for tail in exponents(dim-1,total-a):yield (a,)+tail

def dense(p,bound):
    assert p.degree()<=bound,(p.degree(),bound)
    roster=[m for t in range(bound+1) for m in exponents(DIM,t)]
    coefs=[str(p.c.get(m,F())) for m in roster]
    return dict(dim=DIM,total_degree_bound=bound,monomial_order='total degree then recursive ascending coordinates',
                coefficients=coefs,slots=len(coefs),nonzero=len(p.c),
                negative=sum(c<0 for c in p.c.values()),actual_formal_degree=p.degree())

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def persist(attempt,name,content):
    root=RAW/attempt;root.mkdir(parents=True,exist_ok=True)
    path=root/name
    with path.open('x') as f:json.dump(content,f,sort_keys=True,separators=(',',':'));f.write('\n')
    return dict(path=str(path),sha256=digest(path),bytes=path.stat().st_size)

def basis_stats(fields):
    return dict(fields=len(fields),slots=sum(x['slots'] for x in fields.values()),
                nonzero=sum(x['nonzero'] for x in fields.values()),
                negative=sum(x['negative'] for x in fields.values()))

def execute(section,algorithm,attempt):
    fields={};details=[];start=time.monotonic()
    def add(key,p,b):fields[key]=dense(p,b)
    if section=='two_r':
        reset(2);slack,z=[var(i) for i in range(2)]
        for n in range(1,11):
            for k in range(n+1):
                for l in range(n+1):
                    f=(C if algorithm=='determining' else C_aux)(n,k,l,slack+z,z)
                    dd=f.diff(1)-f.diff(0)
                    add(f'n{n}/k{k}/l{l}/C',f,2*n)
                    add(f'n{n}/k{k}/l{l}/D_fixed_A',dd,2*n-1)
        label='initial q plus all adjacent corrections' if algorithm=='determining' else 'rectangular extraction of complete r_k r_l series'
    elif section=='bases':
        reset(4)
        for n in range(2,7):
            for cone in ('both_unborn','S_first','delta_first','both_born'):
                raw,paid=near_full_cone(n,cone)
                add(f'n{n}/near/{cone}',raw if algorithm=='determining' else paid,2*n)
            a,delta,ss,z=[var(i) for i in range(4)]
            out=far_raw(n,a,delta,ss,z) if algorithm=='determining' else far_positive(n,a,delta,ss,z,details)
            add(f'n{n}/far',out,2*n)
        label='entire supported four-G original' if algorithm=='determining' else 'entire near Phi and far paired R positive expansions'
    elif section=='balanced_gain':
        reset(4)
        for p in range(1,6):
            for cone in ('first','single','middle','far'):
                out=fixed_gain_raw(p,cone) if algorithm=='determining' else fixed_gain_positive(p,cone,details)
                add(f'p{p}/{cone}',out,2*p+1)
        label='complete four supported Q sectors' if algorithm=='determining' else 'full product/tail expansions and paired determinant levels'
    elif section=='pre_return':
        reset(3)
        for kind in ('onezero','balanced'):
            for n in range(2,7):
                for r in range(n+1):
                    D=n+r+(kind=='onezero')
                    for cone in ('first','single1','single2','middle'):
                        if algorithm=='determining':
                            raw=pre_raw(n,r,kind,cone)
                            out=raw.diff(1) if cone in ('first','single1') else raw.diff(2) if cone=='single2' else -raw.diff(0)+raw.diff(1)+raw.diff(2)
                        elif cone=='middle':out=pre_indicator(n,r,kind,details)
                        elif cone=='first':out=d(D,var(1)).diff(1)
                        else:
                            which=1 if cone=='single1' else 2
                            out=pre_positive_single(n,r,kind,which).diff(which)
                        add(f'{kind}/n{n}/r{r}/{cone}/D_physical',out,D-1)
        label='direct physical differentiation of complete q_r' if algorithm=='determining' else 'indicator coefficients or complete single-birth telescope'
    elif section=='last_prefix':
        reset(4)
        for kind in ('onezero','balanced'):
            for n in range(2,7):
                out,dd=prefix_last(n,kind,algorithm)
                bound=2*n+(kind=='onezero')
                add(f'{kind}/n{n}/Q_full',out,bound)
                add(f'{kind}/n{n}/D_fixed_A',dd,bound-1)
        label='full four supported shifted G prefix' if algorithm=='determining' else 'physical rising indices and independent rectangular extraction'
    else:raise ValueError(section)
    record=dict(schema='a83-overlap-independent-freeze/v1',attempt=attempt,section=section,
                algorithm=algorithm,construction=label,shared_primitives='Exact Fraction arithmetic and finite products A/d only; no q-chain in auxiliary extraction',
                code_sha256=digest(Path(__file__)),sources={s:digest(TARGET/s) for s in SOURCES},
                no_source_expected_arrays_read=True,no_other_phase_output_read=True,
                zero_lr_oracle_calls=True,zero_new_named_originals=True,
                fields=fields,details=details,stats=basis_stats(fields),seconds=time.monotonic()-start)
    ptr=persist(attempt,'FIELDS.json',record)
    persist(attempt,'FREEZE.json',dict(immutable=True,**ptr,stats=record['stats'],seconds=record['seconds'],code_sha256=record['code_sha256']))
    print(json.dumps(dict(attempt=attempt,section=section,algorithm=algorithm,**record['stats'],seconds=record['seconds']),sort_keys=True),flush=True)

def price(attempt):
    cases={
      'two_r':dict(n=[1,10],chain_cases=sum((n+1)**2 for n in range(1,11)),dimensions=2,max_degree=20),
      'bases':dict(n=[2,6],near_cones=4,far_cones=1,dimensions=4,max_degree=12),
      'balanced_gain':dict(p=[1,5],cones=['first','single','middle','far'],dimensions=4,max_degree=11),
      'pre_return':dict(n=[2,6],r='0..n',versions=['onezero','balanced'],cones=['first','single1','single2','middle'],dimensions=3,max_degree=12),
      'last_prefix':dict(n=[2,6],versions=['onezero','balanced'],dimensions=4,max_degree=13),
    }
    persist(attempt,'PRICE.json',dict(schema='a83-overlap-price/v1',code_sha256=digest(Path(__file__)),
       planned=cases,per_phase_wall_seconds=240,per_phase_rss_bytes=2**30,
       scientific_oracle_calls=0,new_named_originals=0,source_expected_arrays_read=0,
       estimate='At most four formal variables and total degree 20 in two variables or 13 in four; dense output below 30 MiB. Fresh guarded phases are independently bounded; no grid narrowing permitted without this record and actual receipt.',
       all_zero_slots_retained=True,finite_quantifiers_separate=True))
    print(json.dumps(dict(attempt=attempt,planned=cases)))

def join(attempt,left,right):
    lpath=RAW/left/'FIELDS.json';rpath=RAW/right/'FIELDS.json'
    l=json.loads(lpath.read_text());r=json.loads(rpath.read_text())
    assert l['section']==r['section']
    assert l['algorithm']=='determining' and r['algorithm']=='validating'
    assert set(l['fields'])==set(r['fields'])
    mismatch=[]
    for k,a in l['fields'].items():
        b=r['fields'][k]
        assert (a['dim'],a['total_degree_bound'],a['monomial_order'])==(b['dim'],b['total_degree_bound'],b['monomial_order'])
        diffs=[i for i,(x,y) in enumerate(zip(a['coefficients'],b['coefficients'])) if x!=y]
        if diffs:mismatch.append(dict(field=k,slots=diffs[:50],count=len(diffs)))
    result=dict(schema='a83-overlap-full-join/v1',attempt=attempt,section=l['section'],
          left=dict(attempt=left,sha256=digest(lpath)),right=dict(attempt=right,sha256=digest(rpath)),
          complete_fields=l['stats']['fields'],all_ordinary_slots=l['stats']['slots'],
          determining_negative=l['stats']['negative'],validating_negative=r['stats']['negative'],
          mismatches=mismatch,status='PASS' if not mismatch else 'FAIL',
          source_expected_arrays_joined=0,source_status='SOURCE proof inputs only; no provider code or arrays executed/read',
          quantifier='Exact full-field agreement only at the recorded finite indices; unbounded identities are separate certificates.')
    persist(attempt,'JOIN.json',result)
    print(json.dumps(result,sort_keys=True));assert not mismatch
