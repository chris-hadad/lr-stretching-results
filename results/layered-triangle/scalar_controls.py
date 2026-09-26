"""Exact original GT/flow inverse and uniform-threshold controls."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json,sys

def main():
 if sys.flags.optimize:
  raise RuntimeError('Optimized Python is refused for layered-triangle scalar controls')
 # Literal full component GT versus every bounded cyclic triangle flow.
 maps=[]
 for h in range(4):
  gt={(u,v,z) for u in range(2*h,4*h+1) for v in range(2*h+1) for z in range(v,u+1)};images=set()
  for f12,f23,k in product(range(-h,h+1),repeat=3):
   r1=f12-k;r3=k-f23;L=max(-h,-h-r1,-h+r3);V0=max(0,-r3);v=V0+k-L;u=4*h-r3-v;z=2*h+r1
   assert (u,v,z) in gt and (z-2*h,4*h-u-v)==(r1,r3)
   kk=L+v-V0;assert (kk+r1,kk-r3,kk)==(f12,f23,k);images.add((u,v,z))
  assert images==gt and len(gt)==(2*h+1)**3;maps.append({'h':h,'full_component_points':len(gt)})
 # Preserve the claimed exact threshold and all denominators, independently symbolic.
 # After multiplication by the common denominator the claimed identity is
 # a polynomial of degree at most five. Six exact values determine it fully.
 def numerator_at(r):
  r=F(r);H=r/10;den=(2*r-1)*(2*r)*(2*r+1);den2=(2*r-2)*den
  SD=(2+(r+1)*(2*H+1))/4;S1=(r+2+(r+1)*H)/3;S2=(r+1)*(3*r+5)/6;c=r*(r-1)/2
  delta=192*r*(SD+1)/den+64*r*(r-1)/den
  theta=72*(r*(2*r-1)+r*(r-1)*S2+r*r*(r-3)*S1+c*(c+1)-r**3)/den2
  value=r*(r-1)/(2*r+1)-6-F(2673,2)/(r*(2*r+1))-2*delta-theta
  return value*10*r*(r-1)*(2*r-1)*(2*r+1)
 coefficients=[-13365,43175,-28229,-642,-569,14]
 for r in range(44,50):assert numerator_at(r)==sum(c*r**i for i,c in enumerate(coefficients))
 ascending=[sum(coefficients[j]*comb(j,i)*44**(j-i) for j in range(i,6)) for i in range(6)]
 assert ascending==[68707375,62318223,5203283,170254,2511,14]
 harmonic=sum(F(1,k) for k in range(1,45));assert harmonic<F(22,5)
 print(json.dumps({'component_bijections':maps,'shifted_quintic':ascending,'harmonic44':str(harmonic)}))

if __name__=='__main__':main()
