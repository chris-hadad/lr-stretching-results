"""Portable campaign-owned root arithmetic; requires the two adjacent ROOT JSON files."""
from fractions import Fraction as F
from math import comb,gcd,lcm
from pathlib import Path
import json

def require(ok,why):
    if not ok:raise ValueError(why)

def rational(x):
    require(type(x) is int or isinstance(x,str),'inexact rational input')
    return F(x)

def add(z,w):return z[0]+w[0],z[1]+w[1]

def multiply(z,w):return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]

def norm1(z):return abs(z[0])+abs(z[1])

def evaluate(coeffs,t):
    value=F(0)
    for c in reversed(coeffs):value=value*t+c
    return value

def positive_normalize(row):
    denominator=lcm(*(x.denominator for x in row))
    integers=[int(x*denominator) for x in row]
    divisor=gcd(*integers)
    require(divisor>0,'zero Routh row: standard nonzero-pivot method not applicable')
    return [F(x//divisor) for x in integers]

def routh(coeffs):
    require(coeffs and coeffs[-1]!=0,'nonzero leading coefficient required')
    descending=list(reversed(coeffs));n=len(descending)-1;width=(n+2)//2
    rows=[]
    for offset in (0,1):
        row=descending[offset::2]
        rows.append(positive_normalize(row+[F(0)]*(width-len(row))))
    for _ in range(n-1):
        a,b=rows[-2:];require(b[0]!=0,'zero Routh pivot requires a separate certificate')
        row=[(b[0]*a[j+1]-a[0]*b[j+1])/b[0] for j in range(width-1)]+[F(0)]
        rows.append(positive_normalize(row))
    first=[r[0] for r in rows];require(all(first),'zero first column')
    signs=[1 if x>0 else -1 for x in first]
    return rows,sum(a!=b for a,b in zip(signs,signs[1:])),signs

def main():
    root=Path(__file__).resolve().parent
    p=json.loads((root/'ROOT-POLYNOMIAL.json').read_text())
    certificate=json.loads((root/'ROOT-CERTIFICATE.json').read_text())
    coefficients=list(map(rational,p['coefficients']))
    require(len(coefficients)==32 and all(c>0 for c in coefficients),'degree/sign')
    center=tuple(map(rational,certificate['disk_center']));r=rational(certificate['disk_radius'])
    require(center[0]-r>0 and center[1]>r and r>0,'disk domain')
    powers=[(F(1),F(0))]
    for _ in range(31):powers.append(multiply(powers[-1],center))
    taylor=[]
    for k in range(32):
        value=(F(0),F(0))
        for j in range(k,32):
            factor=coefficients[j]*comb(j,k);z=powers[j-k]
            value=add(value,(factor*z[0],factor*z[1]))
        taylor.append(value)
    upper=norm1(taylor[0])+sum(norm1(taylor[k])*r**k for k in range(2,32))
    lower=max(abs(taylor[1][0]),abs(taylor[1][1]))*r
    require(upper<lower and upper/lower==rational(certificate['rouche_ratio']),'Rouche')
    rows,changes,signs=routh(coefficients)
    require(changes==2 and signs==certificate['routh_signs'],'Routh')
    require(routh([F(2),F(2),F(1)])[1]==0 and routh([F(2),F(-2),F(1)])[1]==2,'controls')
    print('EXACT_POLYNOMIAL_ROOT_CERTIFICATE_VERIFIED: two right-half-plane roots; all coefficients positive')
if __name__=='__main__':main()
