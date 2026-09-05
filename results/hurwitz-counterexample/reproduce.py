"""Standalone exact reproduction; no external dependencies or file writes."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
sys.dont_write_bytecode=True
import r18_count
import check_root

def main():
    root=Path(__file__).resolve().parent
    expected=list(map(F,json.loads((root/'ROOT-POLYNOMIAL.json').read_text())['coefficients']))
    values=[]
    for t in range(32):
        value=r18_count.triangular(t)
        if check_root.evaluate(expected,t)!=value:raise ValueError('count mismatch at '+str(t))
        values.append(F(value))
    if r18_count.triangular(1,True)!=int(values[1]) or r18_count.tableau(1)!=int(values[1]):
        raise ValueError('small independent control mismatch')
    if r18_count.tableau(8)!=r18_count.triangular(8):raise ValueError('tableau holdout mismatch')
    for t in (32,33,37):
        if r18_count.triangular(t)!=check_root.evaluate(expected,t):raise ValueError('holdout mismatch')
    differences=[];work=values
    while work:
        differences.append(work[0]);work=[b-a for a,b in zip(work,work[1:])]
    actual=[F(0)]*32;basis=[F(1)]
    for k,coefficient in enumerate(differences):
        for j,x in enumerate(basis):actual[j]+=coefficient*x
        next_basis=[F(0)]*(len(basis)+1)
        for j,x in enumerate(basis):next_basis[j]-=k*x/F(k+1);next_basis[j+1]+=x/F(k+1)
        basis=next_basis
    if actual!=expected:raise ValueError('independent Newton reconstruction mismatch')
    check_root.main()
    print('BARE-TRIPLE_COUNTS_POLYNOMIAL_AND_ROOT_CERTIFICATES_REPRODUCED')

if __name__=='__main__':main()
