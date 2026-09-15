"""Complete equal-row, successive-overlap LR polynomial by block compensation.

Every affine shift is retained. This is a bounded exact whole-count formula,
not a general sign theorem. The accompanying proof works at every row count;
this bounded interface supports three through eight rows only.
"""
from collections import Counter
from fractions import Fraction as Q
from math import factorial
from .affine import affine_kostka_polynomial, PolynomialResourceLimit


def partitions(total, maximum=None):
    if total==0:
        yield ()
        return
    for first in range(min(total,maximum if maximum is not None else total),0,-1):
        for rest in partitions(total-first,first):
            yield (first,)+rest


def hessenberg_polynomial(n,u,v,alpha,*,max_total_assignments=1000000,max_degree=24,drop_offsets=False):
    if any(type(x)is not int for x in (n,u,v,max_total_assignments,max_degree)):
        raise ValueError('Exact integer parameters required')
    if not 3<=n<=8 or not 0<=v<=u<=2*v or max_total_assignments<1 or max_degree<0:
        raise ValueError('Outside supported shape or resource domain')
    alpha=tuple(alpha)
    if len(alpha)>3 or any(type(x)is not int or x<0 for x in alpha) or any(x<y for x,y in zip(alpha,alpha[1:])) or sum(alpha)!=n*u:
        raise ValueError('Expected balanced three-row target partition')
    alpha=alpha+(0,)*(3-len(alpha))
    specs=[];cost=0
    for blocks in partitions(n):
        m=len(blocks);multiplicities=Counter(blocks)
        coefficient=(-1)**(n-m)*factorial(m)
        for number in multiplicities.values():coefficient//=factorial(number)
        weights=tuple(u+(k-1)*v for k in blocks)+(u-v,)*(n-m)
        offsets=tuple(k-1 for k in blocks)+(-1,)*(n-m)
        reason=None
        if u==v and n>m and not drop_offsets:reason='negative fixed subdiagonal degree'
        if not drop_offsets and any(w>alpha[0] or (w==alpha[0] and b>0) for w,b in zip(weights,offsets)):
            reason='Pieri first-row containment'
        if drop_offsets:offsets=(0,)*n
        price=0 if reason else 3**sum((w,b)!=(0,0) for w,b in zip(weights,offsets))
        cost+=price;specs.append((blocks,coefficient,weights,offsets,reason,price))
    if cost>max_total_assignments:
        raise PolynomialResourceLimit('complete Hessenberg assignments',cost,max_total_assignments)
    total=[Q(0)];records=[]
    for blocks,sign,weights,offsets,reason,price in specs:
        p=(Q(0),) if reason else affine_kostka_polynomial(weights,offsets,alpha,max_assignments=max_total_assignments,max_degree=max_degree)
        while len(total)<len(p):total.append(Q(0))
        for i,x in enumerate(p):total[i]+=sign*x
        records.append({'blocks':blocks,'multiplicity_with_sign':sign,'weights':weights,'offsets':offsets,
                        'zero_reason':reason,'assignment_cost':price,'coefficients':p})
    while len(total)>1 and total[-1]==0:total.pop()
    return {'coefficients':tuple(total),'terms':records,'assignment_cost':cost,'drop_offsets_control':drop_offsets,
            'outer':tuple((n-i-1)*v+u for i in range(n)),'inner':tuple((n-i-1)*v for i in range(n)),
            'content':alpha,'whole_object':not drop_offsets}
