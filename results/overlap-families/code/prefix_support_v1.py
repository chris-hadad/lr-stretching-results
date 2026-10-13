"""Independent whole eight-mask bridge to both pre-return rising expansions.
Source proof text supplies definitions only; no expected arrays are opened.
"""
import argparse
import json
from pathlib import Path
import time
import verify_overlap_v1 as v


def setup(kind,cone):
    aa,e,x,y=[v.var(i) for i in range(4)]
    if cone=='first':
        Z=e;T1=Z+x;T2=Z+y;active1=active2=False;axis=1
    elif cone=='single1':
        T1=e;Z=e+x;T2=Z+y;active1=True;active2=False;axis=2
    elif cone=='single2':
        T2=e;Z=e+x;T1=Z+y;active1=False;active2=True;axis=2
    else:
        T1=e+y;T2=e+x;Z=e+x+y;active1=active2=True;axis=None
    H=v.P() if kind=='onezero' else T1
    G=T1 if kind=='onezero' else T2
    delta=T2 if kind=='onezero' else v.P()
    return aa,Z,H,G,delta,T1,T2,active1,active2,axis


def active_mask(kind,eh,eg,ed,on1,on2):
    if kind=='onezero':
        return (not eg or on1) and (not ed or on2) and not (eg and ed)
    return (not eh or on1) and (not eg or on2) and not (eh and eg)


def full_masks(n,kind,cone):
    aa,Z,H,G,delta,T1,T2,on1,on2,axis=setup(kind,cone)
    out=v.P();count=0
    for eh in range(2):
        for eg in range(2):
            for ed in range(2):
                if not active_mask(kind,eh,eg,ed,on1,on2):continue
                m=eh+eg;k=m+ed;R=eh*H+eg*G+ed*delta
                out+=(-1)**k*v.Fconv(n-m,n-1+m,aa+R+k,Z-R-k-1)
                count+=1
    return out,count


def four_G(n,kind,cone):
    aa,Z,H,G,delta,T1,T2,on1,on2,axis=setup(kind,cone)
    out=v.G(n,n if kind=='onezero' else n-1,aa,Z-1)
    if on1:
        out-=v.G(n-1,n+1 if kind=='onezero' else n,aa+T1+1,Z-T1-2)
    if on2:
        out-=v.G(n if kind=='onezero' else n-1,n if kind=='onezero' else n,aa+T2+1,Z-T2-2)
    return out


def rising_Q(n,kind,cone):
    aa,Z,H,G,delta,T1,T2,on1,on2,axis=setup(kind,cone)
    out=v.P()
    for K in range(n+1):
        r=n-K;D=n+r+(kind=='onezero')
        q=v.d(D,Z)
        if on1:
            q-=sum((v.A(i,T1)*(v.d(D-i,Z-T1)-v.d(D-i-1,Z-T1))
                    for i in range(r)),v.P())
        if on2:
            q-=sum((v.A(i,T2)*(v.d(D-i,Z-T2)-v.d(D-i-1,Z-T2))
                    for i in range(r+(kind=='onezero'))),v.P())
        out+=v.d(K,aa)*q
    return out


def derivative(q,cone):
    if cone=='middle':return -q.diff(1)+q.diff(2)+q.diff(3)
    return q.diff(1 if cone=='first' else 2)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['price','compute'],required=True)
    ap.add_argument('--attempt',required=True);ap.add_argument('--algorithm',choices=['determining','validating'])
    args=ap.parse_args();start=time.monotonic()
    pins=dict(code_sha256=v.digest(Path(__file__)),engine_sha256=v.digest(Path(v.__file__)))
    if args.phase=='price':
        r=dict(schema='a83-overlap-prefix-price/v1',**pins,n=[2,6],
            versions=['onezero','balanced'],cones=['first','single1','single2','middle'],
            full_Q_and_physical_derivative=True,fields=80,max_dimension=4,max_total_degree=13,
            primary='All supported labeled eight masks with every scalar shift',
            secondary='Complete rising coefficients for every K, both retained lower partners',
            wall_seconds=240,rss_bytes=2**30,new_named_originals=0,scientific_oracle_calls=0)
        v.persist(args.attempt,'PRICE.json',r);print(json.dumps(r));return
    fields={};details=[];v.reset(4)
    for kind in ('onezero','balanced'):
        for n in range(2,7):
            for cone in ('first','single1','single2','middle'):
                bound=2*n+(kind=='onezero')
                if args.algorithm=='determining':
                    q,count=full_masks(n,kind,cone)
                    folded=four_G(n,kind,cone)
                    assert q==folded,(kind,n,cone,'mask folding')
                    details.append(dict(kind=kind,n=n,cone=cone,supported_labeled_masks=count,
                                        complete_four_G_fold_agrees=True,coincident_occurrences_retained=True))
                else:q=rising_Q(n,kind,cone)
                dd=derivative(q,cone)
                assert dd.positive(),(kind,n,cone,'physical derivative')
                for suffix,out,degree in [('Q_full',q,bound),('D_full',dd,bound-1)]:
                    fields[f'{kind}/n{n}/{cone}/{suffix}']=v.dense(out,degree)
    record=dict(schema='a83-overlap-independent-freeze/v1',attempt=args.attempt,section='whole_pre_prefix',
        algorithm=args.algorithm,**pins,fields=fields,details=details,stats=v.basis_stats(fields),
        no_source_expected_arrays_read=True,no_other_phase_output_read=True,
        zero_lr_oracle_calls=True,zero_new_named_originals=True,
        seconds=time.monotonic()-start,
        construction='whole eight masks plus complete four-G fold' if args.algorithm=='determining' else 'all complete rising q_r coefficients')
    ptr=v.persist(args.attempt,'FIELDS.json',record)
    v.persist(args.attempt,'FREEZE.json',dict(**ptr,**pins,stats=record['stats'],seconds=record['seconds']))
    print(json.dumps(dict(attempt=args.attempt,**record['stats'],seconds=record['seconds'],status='PASS')))

if __name__=='__main__':main()
