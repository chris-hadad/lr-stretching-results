"""Portable exact fixed-wall mathematics; no fixed filesystem, provider program or orchestration.
Definitions are AST-identical to independently exercised finite_v2.py math.
Requires m>=3; alternative six-kernel evaluation requires m>=6, with distinct m3..5 bases.
Use exact common gain/reserve scale (m+2)*(2m+3)!; integer export rejects bad scales.
Default standard-library integers/Fraction; installed Sage is optional multiplication acceleration.
"""
import math
from fractions import Fraction as F
ZBACKEND=None
def multiply(a,b):
    if len(a)==1:return [a[0]*x for x in b]
    if len(b)==1:return [b[0]*x for x in a]
    if ZBACKEND is not None:return [int(x) for x in (ZBACKEND(a)*ZBACKEND(b)).list()]
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i+j]+=x*y
    return out

class P:
    """Exact dense rational polynomial as an integer vector/positive denominator."""
    __slots__=('a','d')
    def __init__(self,a=0,d=1):
        if isinstance(a,P):self.a=a.a;self.d=a.d;return
        if isinstance(a,F):a,d=[a.numerator],a.denominator
        elif isinstance(a,int):a=[a]
        else:a=[int(v) for v in a]
        if d<0:a=[-v for v in a];d=-d
        assert d>0
        while len(a)>1 and not a[-1]:a.pop()
        if not a:a=[0]
        g=d
        for v in a:g=math.gcd(g,v)
        self.a=tuple(v//g for v in a);self.d=d//g
    def __add__(self,b):
        b=P(b);d=math.lcm(self.d,b.d);fa=d//self.d;fb=d//b.d
        return P([(self.a[i] if i<len(self.a) else 0)*fa+(b.a[i] if i<len(b.a) else 0)*fb for i in range(max(len(self.a),len(b.a)))],d)
    __radd__=__add__
    def __neg__(self):return P([-x for x in self.a],self.d)
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        b=P(b);return P(multiply(self.a,b.a),self.d*b.d)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=F(b);return P([x*b.denominator for x in self.a],self.d*b.numerator)
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        ans=P(1);a=self
        while n:
            if n%2:ans=ans*a
            n//=2
            if n:a=a*a
        return ans
    def __eq__(self,b):b=P(b);return self.a==b.a and self.d==b.d
    def __getitem__(self,i):return F(self.a[i] if i<len(self.a) else 0,self.d)
    def degree(self):return len(self.a)-1 if any(self.a) else -1
    def store(self):return {'numerator':[str(x) for x in self.a],'denominator':str(self.d)}
    @classmethod
    def load(cls,x):return cls([int(a) for a in x['numerator']],int(x['denominator']))

S=P([0,1])

def fall(a,b,k):
    assert k>=0
    p=P(1)
    for i in range(k):p=p*P([b-i,a])
    return p

def rise(a,b,k):
    assert k>=0
    p=P(1)
    for i in range(k):p=p*P([b+i,a])
    return p

def rise_int(b,k):return math.prod(range(b,b+k))

def binom(a,b,k):return fall(a,b,k)/math.factorial(k)

def factorial_product(k,a=1):return rise(a,1,k)/math.factorial(k)

def field(p,n,den):
    p=P(p);assert p.degree()<=n
    scaled=p*den;assert scaled.d==1
    return {'ordinary_degree':p.degree(),'dense_slots':n+1,'denominator':str(den),'coefficients_ascending_scaled':[str(scaled.a[i] if i<len(scaled.a) else 0) for i in range(n+1)],'negative_grades':[i for i in range(n+1) if p[i]<0],'zero_grades':[i for i in range(n+1) if not p[i]]}

def from_field(x):return P([int(v) for v in x['coefficients_ascending_scaled']],int(x['denominator']))

def full_original(m,omit_mask=None,strict_shift_delta=0,remove_lower_partner=False):
    """Unshortened four-mask (3), independently n! scaled with all p terms."""
    n=2*m+1;total=P(0);parts={};high=[]
    for j in range(4):
        aj=P(0)
        for p in range(j+1):
            shift=n-j-p+(strict_shift_delta if j else 0)
            aj=aj+(-1)**p*math.comb(j,p)*(S+2)**(j-p)*(S+1)**p*fall(4-j,shift,n)
        aj=aj*((-1)**j*math.comb(m,j))
        tj=P(0)
        for p in range(m+1):
            multiplier=math.comb(m,j)*math.comb(p+j,j)*math.comb(n,m-p)
            tj=tj+multiplier*fall(3-j,m-j+1,m-p)*fall(1,m,m+p+1)
        edge=tj*((-1)**j*3)
        parts[f'A{j}']=aj;parts[f'edge{j}']=edge
        if j!=omit_mask:total=total+aj-edge
    lower0=fall(2,2*m,n)
    lower1=m*n*(S+2)*fall(1,2*m-2,n-1)
    lower2=m*fall(1,2*m-2,n)
    parts.update(lower_diagonal_first=lower0,lower_diagonal_second=lower1,lower_diagonal_third=lower2)
    total=total-lower0+(P(0) if remove_lower_partner else lower1)+lower2
    if omit_mask is None and not strict_shift_delta and not remove_lower_partner:
        high=[{'grade':d,'coefficient':str(total[d])} for d in range(n+1,n+4)]
        assert all(total[d]==0 for d in range(n+1,n+4))
        assert total.d==1 and total.degree()==n
    return total/math.factorial(n),parts,high

def boundary_det(m):
    r=m-2
    return binom(1,m-2,r)**2-binom(1,m-3,r)*binom(1,m-1,r)

def boundary_product(m):
    p=P(1)
    for r in range(1,m-2):p=p*(S+r)*(S+r+1)/(r*(r+1))
    return p

def component(B,m):return B*(1+F(2*m*(m-1)+3,m*(m-1))*S+F(4*m-3,m*(m-1))*S**2)

class Cores:
    def __init__(self,saved=None):
        if saved:
            self.K=[P.load(p) for p in saved['Ktilde']];self.L=[P.load(p) for p in saved['Ltilde']]
            self.q=len(self.K)-1
            self.r1=rise(1,1,self.q);self.r2=rise(2,1,self.q);self.r3=rise(3,1,self.q)
        else:
            self.K=[1+S];self.L=[S];self.q=0;self.r1=self.r2=self.r3=P(1)
    def extend(self,target):
        while self.q<target:
            q=self.q;next_r3=self.r3*(3*S+q+1)
            k=(4*S+2*q+2)*(4*S+2*q+3)*self.K[-1]+3*math.comb(2*q+1,q)*S*(1+2*S)*self.r1*next_r3
            l=(3*S+2*q+1)*(3*S+2*q+2)*self.L[-1]+2*math.comb(2*q+2,q+1)*S**3*self.r1*self.r2
            assert k.d==l.d==1
            self.K.append(k);self.L.append(l);self.q+=1
            self.r1=self.r1*(S+q+1);self.r2=self.r2*(2*S+q+1);self.r3=next_r3
    def store(self):return {'last_index':self.q,'Ktilde':[p.store() for p in self.K],'Ltilde':[p.store() for p in self.L]}

def kernels(m):
    assert m>=6
    alpha2=(S+m-2)*(S+m-1)*(2*S+2*m-3)*((m+2)*S+3*m)/(2*m*(m-1)*(2*m-1)*(2*m+1))
    P2=(8*m*m-2)*S**2+(18*m**3-18*m*m-m+4)*S+(10*m**4-23*m**3+8*m*m+2*m)
    beta2=S*(S+m-3)*(S+m-1)*P2/(4*m*m*(m-1)**2*(2*m-1)*(2*m+1))
    P3=(m**3+6*m*m+11*m+6)*S**3+(18*m**3+33*m*m-27*m-42)*S**2+(77*m**3-93*m*m-98*m+72)*S+60*m**3-180*m*m+120*m
    alpha3=(S+2*m-7)*(S+2*m-6)*(S+2*m-5)*P3/(48*m*(m-2)*(m-1)*(2*m-3)*(2*m-1)*(2*m+1))
    Ds={}
    for j in (2,3):
        sm=P(0)
        for p in range(j+1):sm=sm+math.comb(j,p)*(S+2)**(j-p)*fall(4-j,-j,p)/rise_int(2*m-2*j+2,j+p)
        Ds[j]=(-1)**j*math.comb(m,j)*rise(4-j,2*m-3*j+2,j)*sm
    ell=-3*(3*S+2*m-1)*(m-(m-1)*S)/(4*(2*m-1)*(2*m+1))
    p3=-3*S*(3*S+2*m-1)*((7*m+5)*S+5*m+2)/(4*(2*m-1)*(2*m+1))
    p12=3*S**2*(2*S+m-1)*((3*m+1)*S+2*m*m+m)/(m*(m-1)*(2*m+1))
    p2=(Ds[2]-F(3*m*(m-1),4)*alpha2)*2*S*(2*S-1)/((2*m-3)*(2*m-4))-2*S*rise(2,2*m-4,5)/rise_int(2*m-4,6)
    p1=(Ds[3]+F(m*(m-1)*(m-2),2)*alpha3)*S*(S-1)*(S-2)/rise_int(2*m-7,3)+S*(S-1)*((m+1)*S+2*m)*rise(1,2*m-7,6)/((2*m-1)*(2*m+1)*rise_int(2*m-7,6))
    p11=-F(3*m*(m-1),2)*(alpha2*S**2*(S+m-3)**2/2+beta2*S*(S-1)*(S+m-3)*(S+m-2))/((m-2)**2*(m-3)**2)
    return {'l':ell,'p3':p3,'p12':p12,'p2':p2,'p11':p11,'p1':p1}

def small_original(m):
    """Full stable/adjacent/second-band moments; no interpolation or count calls."""
    assert m in (3,4,5)
    D=((S+1)*(S+2)/2)**m
    L=P(0)
    for j in range(m+1):L=L+(-1)**j*math.comb(m,j)*(S+1)**(m-j)*binom(1,m,m+j+1)
    # Alternative complete lower-diagonal moment form from U04 section 6.
    lower=2*S*factorial_product(2*m,2)/(2*m+1)-S*(S-1)*factorial_product(2*m-2)*((m+1)*S+2*m)/((2*m-1)*(2*m+1))
    whole=(1+(2-F(2*m-6,3))*S)*D-3*L-lower
    partners={'D':D,'L':L,'R':lower}
    if m==4:
        z=binom(1,2*m-1,2*m+1);whole=whole+3*z;partners['complete_Z']=z
    if m==5:
        z=binom(2,2*m-1,2*m+1);pm=P(0);r0=P(0)
        for j in range(m+1):
            pm=pm+(-1)**j*math.comb(m,j)*(S+1)**(m-j)*binom(1,m-1,m+j+1)
            r0=r0+binom(1,m,m-j)*binom(1,m-1,m+j+1)
        w=S*binom(1,2*m-3,2*m)-m*binom(1,2*m-3,2*m+1)
        whole=whole+3*z+pm-3*r0-3*m*w
        partners.update(complete_Z=z,complete_P=pm,complete_R0=r0,complete_W1=w)
    return whole,partners

def alternative_original(m,cores):
    if m<6:return small_original(m)
    cores.extend(m);ks=kernels(m)
    terms={'K':cores.K[m]/math.factorial(2*m+1),'lL':ks['l']*cores.L[m-1]/math.factorial(2*m-2),'p3V3':ks['p3']*factorial_product(2*m-2,3),'p12W12':ks['p12']*factorial_product(m-2,2)*factorial_product(m-1),'p2V2':ks['p2']*factorial_product(2*m-5,2),'p11W11':ks['p11']*factorial_product(m-4)**2,'p1V1':ks['p1']*factorial_product(2*m-8)}
    return sum(terms.values(),P(0)),terms

def set_backend(name="standard"):
    """Select only multiplication acceleration; no installation is attempted."""
    global ZBACKEND
    if name=="standard":
        ZBACKEND=None
        return {"backend":"standard-library integer/Fraction"}
    if name=="sage":
        from sage.all import PolynomialRing,ZZ
        from sage.env import SAGE_VERSION
        ZBACKEND=PolynomialRing(ZZ,"S")
        return {"backend":type(ZBACKEND([1,1])).__name__,"Sage_version":SAGE_VERSION}
    raise ValueError("Backend must be standard or sage")
