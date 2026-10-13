"""Fresh exact free-index identities, full intermediate fields and hostile controls.
No SOURCE arrays/code, LR oracle, original-count or interpolation calls.
"""
import argparse
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
import time
import verify_overlap_v1 as v


def check(out,name,left,right,bound,meaning):
    assert left==right, name
    out[name]=dict(left=v.dense(left,bound),right=v.dense(right,bound),
                   difference=v.dense(left-right,bound),meaning=meaning,status='PASS')


def free_identities():
    v.reset(5);u,z,x,y,w=[v.var(i) for i in range(5)]
    cases={
      'slack_increment':((x+u)*y-(z+u)*w-u*(y-w),z*(y-w)+(x-z)*y,
          'a K increment after multiplying by positive a; y=A_(a-1), w=A_(M-1)(A+1)R_(a-1,M)(z)'),
      'birth_recurrence':((u+1)*(z+u+1)*x-u*((z+u)*x+y),(z+2*u+1)*x-u*y,
          'Multiply by r+1; x=d_r derivative, y=d_r; rising derivative recurrence'),
      'terminal_H':((u+1)*(z+1)*x-u*(y+(z+u)*x)+u*(u+1)*x,(z+2*u+1)*x-u*y,
          'Distinct terminal H_a coefficient; multiplication by a(a+1)'),
      'strict_witness':(((u+1)*(y+1)+u*(u+1)-u*(z+u))*x-u*w,((u+1)*(y-z)+z+2*u+1)*x-u*w,
          'q_(n,n-1) fixed-A derivative after clearing n(n+1)'),
      'A_adjacent':((x+u+1)*y-u*y,(x+1)*y,
          'A_j(A+1)-A_(j-1)(A+1)=A_j(A) after multiplying by j'),
      'balanced_product_step':((z+x+1)*y-(z+y)* (x+1),z*(y-x-1),
          'Clear (i+1)j in A_(i+1)A_(j-1)-A_i A_j'),
      'far_residual':((z+1)*(z+u)-(z+x+1)*z,u+(u-x)*z,
          'A_v A_n-A_v(z+1)d_n after factoring A_(v-1)(z+1)A_(n-1)/(vn)'),
      'determinant_ratio':((u+1)*(z+x)-(z+u+1)*x,(u-x+1)*z,
          'S_(u,v) ratio, multiplied by (u+1)(z+v); v=0 retained separately'),
      'determinant_increment':((u-x+2)*(z+u+1)-(u-x+1)*(u+2),(u-x+2)*z+x,
          'S_(u+1,v)-S_(u,v), clear (u+1)(u+2)'),
      'indicator_shift':((1-x-w)+(1-y-z)-(1-y-w),1-x-z,
          'I1 and I2 unchanged/shifted indicator cancellation at arbitrary integer q>=1'),
    }
    result={}
    for name,(left,right,meaning) in cases.items():
        check(result,name,left,right,3,meaning)
    return result


def rising_extract(poly,axis):
    result={};residual=poly
    maximum=max((m[axis] for m in residual.c),default=0)
    basis=v.var(axis)
    for h in range(maximum,-1,-1):
        coeff=v.P({tuple(0 if i==axis else a for i,a in enumerate(m)):c*factorial(h)
                   for m,c in residual.c.items() if m[axis]==h})
        result[h]=coeff
        residual-=coeff*v.d(h,basis)
    assert not residual.c
    return result


def intermediate():
    out={};details=[]
    v.reset(2);x,z=v.var(0),v.var(1)
    for a in range(1,11):
        H=(z+2*a+1)*v.d(a,z).diff(1)-a*v.d(a,z)
        deleted=sum(((2*a+1-i)*v.prod(z+j for j in range(a) if j!=i)/factorial(a)
                      for i in range(a)),v.P())
        check(out,f'H/a{a}',H,deleted,a-1,'Whole deleted-factor positivity, including H_1=3')
        for M in range(1,a+1):
            R=v.F(factorial(M-1),factorial(a))*(z+1)*v.prod(z+r for r in range(M+1,a+1))
            B=R*v.d(M,z).diff(1)-v.d(a+1,z).diff(1)+v.d(a,z).diff(1)
            paid=H/(a*(a+1))
            for r in range(M,a):
                Hr=(z+2*r+1)*v.d(r,z).diff(1)-r*v.d(r,z)
                paid+=(z+1)*v.F(factorial(r-1),(r+1)*factorial(a))*v.prod(z+j for j in range(r+2,a+1))*Hr
            check(out,f'B/a{a}/M{M}',B,paid,a,'Entire birth telescope; distinct terminal coefficient retained')
            assert paid.positive()
    for N in range(1,13):
        for T in range(N):
            rect=v.A(N,x+z)-sum((v.A(i,x)*v.d(N-i,z) for i in range(T+1)),v.P()) \
              -sum((v.A(i,z)*v.d(N-i,x) for i in range(N-T)),v.P())
            check(out,f'rect/N{N}/T{T}',rect,v.A(T,x)*v.A(N-T-1,z),N,
                  'Complete finite rectangle; shared corner once')
    for T in range(2,15):
        for e in range(T-1):
            left=sum((v.d(r,x+2)*v.A(T-r,z-2) for r in range(e+1)),v.P())
            right=sum((v.A(i,x)*v.d(T-i,z) for i in range(e+1)),v.P())-v.A(e,x+1)*v.d(T-e-1,z)
            check(out,f'return/T{T}/e{e}',left,right,T,'Entire +2/-2 returning telescope with last endpoint')
    for a in range(0,7):
        for b in range(0,8):
            check(out,f'convolution/a{a}/b{b}',v.G(a,b,x,z),v.G_antidifference(a,b,x,z),a+b+1,
                  'Vandermonde vs exact Newton antidifference of original full finite integrand')
    for n in range(2,7):
        for k in range(n+2):
            for l in range(n+2):
                raw=v.far_Q(n,k,l,x,z)
                coeffs=rising_extract(raw,0)
                paid=sum((v.d(h,x)*v.far_R_positive(n,n-k,n-l,h,z,details)
                          for h in range(n)),v.P()) if k<=n and l<=n else v.P()
                check(out,f'far_Q/n{n}/k{k}/l{l}',raw,paid,2*n,'All k,l including outside zeros; full S rising expansion')
                for h in range(max(n+2,max(coeffs,default=0)+1)):
                    expected=v.far_R_positive(n,n-k,n-l,h,z) if k<=n and l<=n and h<n else v.P()
                    check(out,f'far_R/n{n}/k{k}/l{l}/h{h}',coeffs.get(h,v.P()),expected,2*n,
                          'Independent triangular extraction from whole Q; every h>=n coefficient zero')
    v.reset(1);z=v.var(0)
    for p in range(1,6):
        for k in range(p+1):
            P=p-k;M=2*p+1-k
            for i in range(M+2):
                for j in range(M+2):
                    raw=sum((v.A(r,z)*v.d(M-r-i-j,z)-v.A(r-i,z)*v.d(M-r-j,z)
                              -v.A(r-j,z)*v.d(M-r-i,z)+v.A(r-i-j,z)*v.d(M-r,z)
                              for r in range(P+1)),v.P())
                    paid=v.gain_R_paid(p,k,i,j,z,details) if i>=1 and j>=1 else v.P()
                    check(out,f'gain_R/p{p}/k{k}/i{i}/j{j}',raw,paid,max(M,0),
                          'Uncollected full four ranges vs BOTH determinant levels, terminal and exterior zeros')
                    assert paid.positive()
    return out,details


def boundaries_controls():
    out={};controls=[]
    v.reset(4);a,e,x,y=[v.var(i) for i in range(4)]
    for p in range(1,6):
        for cone in ('first','single','middle'):
            gain=v.fixed_gain_raw(p,cone).subzero(0)
            U=e if cone=='first' else e+x if cone=='single' else e+x+y
            complete=v.A(p,U)+gain
            assert gain.positive()
            assert all(complete.homogeneous(j).evaluate([0,1,1,1])>0 for j in range(2*p+2))
            out[f'degree_loss/p{p}/{cone}']=dict(full=v.dense(complete,2*p+1),gain=v.dense(gain,2*p+1),
                 merged=v.dense(v.A(p,U),2*p+1),prior_original_degree=2*p+1,merged_degree=p,
                 strictly_positive_by_total_degree_on_positive_cone=True,
                 scope='Formal A=0 cone field; no named original or LR count')
        gain=v.fixed_gain_raw(p,'middle').subzero(0).subzero(1)
        rect=v.A(p,x+y)+gain
        check(out,f'rectangle_boundary/p{p}',rect,v.A(p,x)*v.A(p,y),2*p,
              'Actual A=0,e=0 complete rectangular face has degree 2p')
    quadratic=v.fixed_gain_raw(1,'middle').subzero(0).homogeneous(2)
    check(out,'p1_full_quadratic',quadratic,e*e+v.F(3,2)*e*(x+y)+x*y,2,
          'Complete p=1 low coefficient pays degree-loss gap')
    for n in range(2,7):
        for kind in ('onezero','balanced'):
            full,der=v.prefix_last(n,kind,'determining')
            # Both support-wall polynomial return continuations vanish at z=0.
            B=a+e
            ret=v.G(n-1,n+1,B+x+y+2,e-3) if kind=='onezero' else v.G(n-2,n+1,B+x+y+2,e-3)
            assert not ret.subzero(1).c
            out[f'return_wall/{kind}/n{n}']=dict(return_field=v.dense(ret,2*n+(kind=='onezero')),
                         wall_zero=v.dense(ret.subzero(1),2*n+(kind=='onezero')),status='PASS')
    def hostile(name,complete,wrong,bound,why):
        diff=wrong-complete
        assert diff.c,name
        controls.append(dict(name=name,complete=v.dense(complete,bound),wrong=v.dense(wrong,bound),
                 difference=v.dense(diff,bound),detected=True,why=why))
    far=v.far_raw(3,a,e,x,y)
    hostile('missing_return',far,far-v.G(2,3,a+e+x+y+2,y-2),6,
            'Dropping entire far return changes the full fixed original')
    near=v.near_positive(3,a,e,x,y)
    hostile('double_counted_near_corner',near,near+v.A(3,a)*v.A(2,e),6,
            'Shared finite-rectangle corner may be paid once only')
    full,dd=v.prefix_last(3,'onezero','validating')
    hostile('wrong_physical_derivative',dd,full.diff(1),6,
            'Differentiating at fixed slack adds partial_x; physical A is fixed')
    missing=v.d(1,y)*sum((v.d(k,x)*v.C_aux(3,k,0,a+e,e) for k in range(4)),v.P())
    hostile('missing_delta_index_one',full,full-missing,7,
            'Physical delta=0 and delta=1 rising indices are distinct equal-C occurrences')
    v.reset(3);e,x,y=[v.var(i) for i in range(3)]
    for kind in ('onezero','balanced'):
        n=r=3;D=n+r+(kind=='onezero');r2=r if kind=='onezero' else r-1
        complete=v.pre_raw(n,r,kind,'middle')
        wrong=v.d(D,e+x+y)-sum((v.A(i,e+y)*v.d(D-i,x) for i in range(r)),v.P()) \
              -sum((v.A(i,e+x)*v.d(D-i,y) for i in range(r2+1)),v.P())
        dc=-complete.diff(0)+complete.diff(1)+complete.diff(2)
        dw=-wrong.diff(0)+wrong.diff(1)+wrong.diff(2)
        hostile('missing_both_lower_partners/'+kind,dc,dw,D-1,
                'Top beta=-1 debt needs both same-coefficient lower products')
        assert not dw.positive()
    v.reset(2);x,z=[v.var(i) for i in range(2)]
    constant=v.C(3,3,3,x+z,z)
    assert constant==v.P(1)
    hostile('erased_constant_endpoint',constant,v.P(),6,'C_(n;n,n)=1 remains in each actual prefix endpoint')
    return out,controls


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--attempt',required=True);ap.add_argument('--phase',choices=['price','free','intermediate','controls'],required=True);args=ap.parse_args()
    start=time.monotonic()
    pins=dict(code_sha256=v.digest(Path(__file__)),engine_sha256=v.digest(Path(v.__file__)))
    if args.phase=='price':
        result=dict(schema='a83-overlap-certificate-price/v1',**pins,
            free_index_identities=10,intermediate_ranges=dict(a=[1,10],N=[1,12],return_T=[2,14],convolution_a=[0,6],convolution_b=[0,7],far_n=[2,6],gain_p=[1,5]),
            controls='Full fields and derivative failures; no selected-slot-only checks',wall_cap_seconds=240,rss_cap_bytes=2**30,
            scientific_oracle_calls=0,new_named_originals=0,source_expected_arrays_read=0)
    elif args.phase=='free':result=dict(certificates=free_identities(),**pins)
    elif args.phase=='intermediate':
        out,details=intermediate();result=dict(fields=out,details=details,**pins)
    else:
        out,controls=boundaries_controls();result=dict(fields=out,controls=controls,**pins)
    result.update(schema='a83-overlap-certificates/v1',phase=args.phase,attempt=args.attempt,
           finite_cases_supply_no_unbounded_quantifier=True,source_expected_arrays_read=0,
           scientific_oracle_calls=0,new_named_originals=0,seconds=time.monotonic()-start)
    ptr=v.persist(args.attempt,'CERTIFICATES.json',result)
    v.persist(args.attempt,'FREEZE.json',dict(**ptr,**pins,seconds=result['seconds']))
    print(json.dumps(dict(attempt=args.attempt,phase=args.phase,seconds=result['seconds'],fields=len(result.get('fields',{})),controls=len(result.get('controls',[])),status='PASS')))

if __name__=='__main__':main()
