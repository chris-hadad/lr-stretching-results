"""Independent free-variable certificate derivation from allowed mathematical definitions.

Uses existing trusted SymPy only. Never imports or runs returned provider code.
No SOURCE arrays/proof appendices are read. Uniform coefficients are derived
from finite p/q/r formulas; positive-denominator shifted numerator and residual
certificates prove the stated inequalities for every real m>=3.
"""
import argparse
import json
from pathlib import Path
import time
import sympy as sy
m,S,r,x=sy.symbols('m S r x')

def fall(z,k):
    return sy.prod(z-i for i in range(k))

def rise(z,k):
    return sy.prod(z+i for i in range(k))

def vec(p,z=x):
    p=sy.Poly(sy.expand(p),z)
    return [str(p.nth(i)) for i in range(p.degree()+1)] if not p.is_zero else ['0']

def nonnegative(p,z=x,strict=False):
    cc=sy.Poly(sy.expand(p),z).all_coeffs()
    return all(c>0 if strict else c>=0 for c in cc)

def zero_certificate(expr,variables):
    n,d=sy.fraction(sy.cancel(expr))
    p=sy.Poly(sy.expand(n),*variables)
    assert p.is_zero, str(p)
    return dict(numerator='0',denominator=str(sy.factor(d)),free_variables=list(map(str,variables)),exact_zero=True)

c0=(S+3)*(S+2)/2
z=sy.Symbol('z')
d=[sy.expand((c0+(S+3)*z+z*z)**2).coeff(z,h) for h in range(5)]
pm=sy.Rational(2,3)*(c0+(S+3)*(2*S-1)/(3*m+1)+(2*S-1)*(2*S-2)/((3*m+1)*(3*m+2)))
qm=m/(6*(3*m-2))*sum(d[h]*fall(S-2,h)/rise(3*m-1,h) for h in range(5))
rm=sy.binomial(m,2)*sum(
    (-1)**h*sy.binomial(2,h)*sy.binomial(2-h,v)*(S+1)**v*
    sum(sy.binomial(4,3+h-i)*sy.binomial(2*m+1-h-v+i,i)*fall(S-2,i)*rise(S+3*m-3,2-h-v)/rise(3*m-3,4-h-v+i)
        for i in range(4+h))
    for h in range(3) for v in range(3-h))
# Expand only fixed-lower binomials as finite falling products. This is crucial:
# no gamma-based or integer-sample inference is used for free m.
rm=rm.replace(lambda e:e.func==sy.binomial,
              lambda e:fall(e.args[0],int(e.args[1]))/sy.factorial(int(e.args[1])))
pm=sy.Poly(sy.expand(pm),S)
qm=sy.Poly(sy.expand(qm),S)
rm=sy.Poly(sy.expand(rm),S)
hm=sy.Poly(sy.expand((3*S+1)*qm.as_expr()-4*rm.as_expr()),S)
PBAR=2+2*S+S*S/2
QBAR=sy.Rational(1411,1320)+sy.Rational(4457,2520)*S+sy.Rational(40049,36960)*S*S+sy.Rational(1009,3465)*S**3+sy.Rational(51,1760)*S**4
HBAR=sy.Rational(409,1458)+sy.Rational(1579,1215)*S+sy.Rational(45475,22176)*S*S+sy.Rational(34549,22176)*S**3+sy.Rational(3947,7392)*S**4+sy.Rational(2509,36960)*S**5
D=(3*m-2)*(3*m-1)*(3*m+1)*(3*m+2)

def coefficient_certificates(poly,common_denominators,bar,derive_max=False):
    out=[]
    for degree,den in enumerate(common_denominators):
        coeff=sy.cancel(poly.nth(degree))
        num=sy.cancel(coeff*den)
        assert sy.fraction(num)[1]==1, ('not polynomial common numerator',degree,num)
        nshift=sy.expand(num.subs(m,x+3));dshift=sy.expand(den.subs(m,x+3))
        assert nonnegative(nshift,strict=True) and nonnegative(dshift,strict=True)
        b=sy.Poly(bar,S).nth(degree)
        residual=sy.expand(b*dshift-nshift)
        assert nonnegative(residual), ('majorant residual',degree,residual)
        rec=dict(S_degree=degree,coefficient=str(sy.factor(coeff)),
                 common_numerator_m=str(sy.expand(num)),common_denominator_m=str(sy.expand(den)),
                 numerator_m_equals_x_plus_3=vec(nshift),denominator_m_equals_x_plus_3=vec(dshift),
                 numerator_coefficients_strictly_positive=True,denominator_coefficients_strictly_positive=True,
                 majorant=str(b),majorant_residual_m_equals_x_plus_3=vec(residual),
                 residual_coefficients_nonnegative=True)
        if derive_max:
            np=sy.Poly(nshift,x);dp=sy.Poly(dshift,x)
            ratios=[sy.cancel(np.nth(i)/dp.nth(i)) for i in range(dp.degree()+1)]
            derived=max(ratios)
            assert derived==b, ('independently derived coefficient majorant differs',degree,derived,b)
            rec.update(coefficient_ratios=list(map(str,ratios)),derived_maximum=str(derived),
                       maximum_indices=[i for i,c in enumerate(ratios) if c==derived])
        out.append(rec)
    return out

def telescopers():
    D1=9*(m+1)*(2*m+1)*(3*m+1)*(3*m+2)
    q0=((23*m**3+82*m*m+85*m+26)*S*S+(97*m**3+262*m*m+205*m+48)*S+102*m**3+192*m*m+116*m+22)/D1
    q1=-((2*m*m+20*m+14)*S+15*m*m+27*m+12)/(9*(m+1)*(2*m+1)*(3*m+2))
    q2=-(m-1)/(9*(m+1)*(2*m+1))
    qtel=q0+q1*r+q2*r*r
    R=sy.Rational(2,9)*((2*m*m+10*m+12)*S**3+(21*m*m+51*m+18)*S*S+(46*m*m+41*m+6)*S+12*m*m+6*m)/((3*m+1)*(3*m+2))
    Q=2*((4*m**3+10*m*m+15*m+7)*S*S+(26*m**3+83*m*m+71*m+18)*S+51*m**3+96*m*m+58*m+11)/D1
    f=(S-r)*(S-r+1)*((2*m+4)*S+7*m+2+(m-1)*r)/(3*(2*m+1))
    T=2*S-1;l=2*m+1
    one=zero_certificate(f-((r+m)*(T-r)*qtel.subs(r,r+1)-r*(T-r+l)*qtel+R),(r,m,S))
    endpoint=zero_certificate(qtel.subs(r,S)-Q,(m,S))
    k,L,T0=sy.symbols('k ell T')
    uncapped=zero_certificate((r+k)*(T0-r)-r*(T0-r+L)-(k*T0-(k+L)*r),(r,k,L,T0))
    return dict(one_cap_free_variable_telescoper=one,one_cap_q_at_S_equals_Q=endpoint,
                uncapped_free_variable_telescoper=uncapped,
                one_cap_R_coefficients=[str(sy.factor(sy.Poly(R,S).nth(i))) for i in range(4)],
                one_cap_Q_coefficients=[str(sy.factor(sy.Poly(Q,S).nth(i))) for i in range(3)])

def ratio_certificates():
    RM=sy.prod(1+3*S/(3*m+3+i) for i in range(3))
    RA=sy.prod(1+2*S/(3*m+i) for i in range(3))
    RB=sy.prod(1+S/(3*m-3+i) for i in range(3))
    out=[]
    for name,expr in [('R_M_minus_R_A',RM-RA),('R_M_minus_R_B',RM-RB)]:
        rows=[]
        for degree in range(4):
            coeff=sy.cancel(sy.expand(expr).coeff(S,degree))
            n,d0=sy.fraction(coeff)
            ns=sy.expand(n.subs(m,x+3));ds=sy.expand(d0.subs(m,x+3))
            assert nonnegative(ns) and nonnegative(ds,strict=True)
            rows.append(dict(S_degree=degree,numerator_m_equals_x_plus_3=vec(ns),
                             denominator_m_equals_x_plus_3=vec(ds),numerator_nonnegative=True,denominator_positive=True))
        out.append(dict(name=name,coefficients=rows))
    return dict(factor_slope_cross_differences=[dict(i=i,A=str(3*m+i-6),B=str(6*m+2*i-12),
                                                  at_m3_A=3+i,at_m3_B=6+2*i) for i in range(3)],
                exact_coefficient_ratios=out)

def main(output):
    output=Path(output)
    assert not output.exists(), "Choose a fresh output directory"
    output.mkdir(parents=True,exist_ok=False)
    started=time.monotonic()
    cert=dict(schema='a82-four-letter-free-variable-certificates/v1',sympy_version=sy.__version__,
              telescopers=telescopers(),
              p=coefficient_certificates(pm,[3*(3*m+1)*(3*m+2)]*3,PBAR),
              q=coefficient_certificates(qm,[6*D,18*D,72*D,12*D,24*D],QBAR),
              H=coefficient_certificates(hm,[18*D,90*D,648*D,648*D,648*D,3240*D],HBAR,True),
              r_coefficients=[str(sy.factor(sy.cancel(rm.nth(i)))) for i in range(rm.degree()+1)],
              derived_degrees=dict(p=pm.degree(),q=qm.degree(),r=rm.degree(),H=hm.degree()),
              qbar_absolute_factor_majorant_identity=zero_certificate(QBAR-sum(d[h]*rise(S+2,h)/rise(8,h) for h in range(5))/14,(S,)),
              ratios=ratio_certificates(),
              domain='m=x+3, x>=0; all coefficient inequalities use positive common denominators',
              provider_numeric_arrays_read=False,returned_programs_executed=False)
    cert['seconds']=time.monotonic()-started
    (output/'SYMBOLIC-CERTIFICATES.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',seconds=cert['seconds'],p_coefficients=3,q_coefficients=5,H_coefficients=6,
                          free_variable_telescoper=True,majorant_residuals_nonnegative=True)),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();main(a.output)
