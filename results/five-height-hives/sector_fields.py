#!/usr/bin/env python3
"""Literal original-row adapter for full first-failure fields; including exact once-only shifts.
Status +1 retains a closed original row, -1 takes its integer strict violation,
0 omits it. Every field retains the original certified box.
"""
import itertools
import json
import sys
import time
import interface_checker as ic

PRIVATE={'left':(0,1),'right':(9,8),'middle':(3,)}


def affine_sum(lower,upper,blo,bhi):
    total=0
    assert len(lower)*len(upper)<=6
    for li,(lm,lc) in enumerate(lower):
      for ui,(um,uc) in enumerate(upper):
        lo,hi=blo,bhi
        gates=[(lm-m,lc-c-int(k<li)) for k,(m,c) in enumerate(lower) if k!=li]
        gates += [(m-um,c-uc-int(k<ui)) for k,(m,c) in enumerate(upper) if k!=ui]
        gates += [(um-lm,uc-lc)]
        for m,c in gates:
            if m>0: lo=max(lo,ic.ceildiv(-c,m))
            elif m<0: hi=min(hi,c//(-m))
            elif c<0: lo,hi=1,0;break
        if lo<=hi:
            n=hi-lo+1
            value=(um-lm)*(lo+hi)*n//2+(uc-lc+1)*n
            assert value>=n>0
            total+=value
    return total


def modified(row,status,t,x):
    beta,n=row
    c=status*(beta*t+sum(n[j]*x[j] for j in ic.BASE))-int(status==-1)
    return c,tuple(status*a for a in n)


def field(rows,status,t,base,label):
    x=[0]*10
    for j,v in zip(ic.BASE,base):x[j]=v
    private=PRIVATE[label]
    if len(private)==1:
        a=private[0];lo,hi=(v*t for v in ic.BOX[a])
        for k in ic.GROUPS[label]:
            if not status[k]:continue
            c,n=modified(rows[k],status[k],t,x)
            assert n[a] in (-1,1)
            if n[a]==1:lo=max(lo,-c)
            else:hi=min(hi,c)
        return max(0,hi-lo+1)
    a,b=private
    lows={0:ic.BOX[a][0]*t};ups={0:ic.BOX[a][1]*t}
    blo,bhi=(v*t for v in ic.BOX[b])
    for k in ic.GROUPS[label]:
        if not status[k]:continue
        c,n=modified(rows[k],status[k],t,x)
        aa,bb=n[a],n[b]
        assert aa in (-1,0,1) and bb in (-1,0,1)
        if aa==1:
            slope=-bb;lows[slope]=max(lows.get(slope,-10**100),-c)
        elif aa==-1:
            slope=bb;ups[slope]=min(ups.get(slope,10**100),c)
        elif bb==1:blo=max(blo,-c)
        elif bb==-1:bhi=min(bhi,c)
        else:raise AssertionError('Unexpected private-free group row')
    return affine_sum(sorted(lows.items()),sorted(ups.items()),blo,bhi)


def base_ok(rows,status,t,base):
    x=[0]*10
    for j,v in zip(ic.BASE,base):x[j]=v
    for k in ic.GROUPS['base']:
        if status[k] and modified(rows[k],status[k],t,x)[0]<0:return False
    return True


def whole_field(rows,status,t,base):
    if not base_ok(rows,status,t,base):return 0
    ans=1
    for label in PRIVATE:ans*=field(rows,status,t,base,label)
    return ans


def direct_private(rows,status,t,base,label):
    x=[0]*10
    for j,v in zip(ic.BASE,base):x[j]=v
    ans=0
    for v in itertools.product(*(range(ic.BOX[j][0]*t,ic.BOX[j][1]*t+1) for j in PRIVATE[label])):
        for j,z in zip(PRIVATE[label],v):x[j]=z
        good=True
        for k in ic.GROUPS[label]:
            if not status[k]:continue
            beta,n=rows[k]
            slack=beta*t+sum(a*b for a,b in zip(n,x))
            if (slack<0 if status[k]==1 else slack>=0):good=False;break
        ans+=good
    return ans


def main():
    if sys.flags.optimize:
        raise RuntimeError('Optimized Python is refused for five-height sector fields')
    started=time.monotonic();rows,sha=ic.load_source(ic.DEFAULT_SOURCE)
    samples=list(itertools.product(*[(ic.BOX[j][0],ic.BOX[j][1]) for j in ic.BASE]))
    samples += [(36,36,42,46,46)]
    cases=0;empty=0
    for t in (0,1,2):
      bases=sorted(set(tuple(t*v for v in base) for base in samples))
      for base in bases:
        closed=[1]*45
        parts=[whole_field(rows,closed,t,base)]
        states=[closed]
        for k in range(45):states.append([1]*k+[-1]+[0]*(44-k))
        for status in states:
            for label in PRIVATE:
                actual=field(rows,status,t,base,label)
                expected=direct_private(rows,status,t,base,label)
                assert actual==expected,(t,base,status,label,actual,expected)
                empty+=int(actual==0);cases+=1
        parts += [whole_field(rows,s,t,base) for s in states[1:]]
        expected_box=1
        for private in PRIVATE.values():
            for j in private:expected_box*=(ic.BOX[j][1]*t-ic.BOX[j][0]*t+1)
        assert sum(parts)==expected_box,(t,base,parts,expected_box)
    print(json.dumps({'schema':'astra053-original-sector-fields/v1','source_sha256':sha,
        'grades':[0,1,2],'sample_base_rays':len(samples),'private_field_comparisons':cases,
        'empty_fields':empty,'all_45_first_failure_pointwise_partitions':True,
        'seconds':time.monotonic()-started},indent=2))

if __name__=='__main__':main()
