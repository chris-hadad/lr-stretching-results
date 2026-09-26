# Top strip

Curated mathematical proof from Pro042; the original source is byte-bound in
`../SOURCE-MAP.json`. The main proof fixes the complete family and conventions.

## 1. Exact original subject and inherited complete field

Use the complete original U07 tableau-to-flow constructor, whose full proof is
included in this module. For r>=1, b>=1 and
A>0 take the r+1 layers(A,b,...,b). Put W=A+rb. The straight components are
(4W,2W),(4A,2A), followed by r copies of(4b,2b). For each component let its
horizontal offset equal the sum of the first rows of all later components.
Concatenate offset+component rows to make outer Lambda, concatenate each offset
twice to make M, and take Nu=(6W,4W,2W), padded only to the actual rank.

All boundaries are legal partitions. The forced first component pays every
ballot prefix. Every within-component column and the prescribed total content
remain. The included U07 proof gives a homogeneous, continuous piecewise
integral-unimodular map and inverse to r+1 bounded triangle layers whose three
aggregate currents agree. It preserves the entire count, saturated lattice,
actual dimension and original grade. It is not an additive map or a claim
that every original LR polytope has integral vertices.

For positive A,b the original rank is2r+4 and actual dimension3r+1. With A=0,
remove that component first; in the domain A>=(r-1)b this can occur only at
r=1. That parent is the rank-four segment with polynomial2bt+1. If b=0 and
A>0 only the large layer remains, giving2At+1. If both vanish the empty
boundary triple has rank0, dimension0 and polynomial1. No infeasible family
is assigned that constant convention.

Set x=bt,p=(rb-A)t,y=1+2x. On the entire top balanced strip0<=p<=x, the
complete inherited U08 field is

    P=Pcritical(x)-2p y^(3r)+6y^r A_r(p)-6B_r(p),                 (1)
    A_r(p)=binom(2p+2r-1,2r+1),
    B_r(p)=sum_(k=0)^r binom(r,k)^2 binom(2p+3r-k-1,3r+1).

Its complete all-grade count proof, all endpoints and bounded-tail hypotheses
are included unchanged. It is not a selected correction or a fitted field.
For p>x this specific unbounded-tail substitution is not a count formula.

## 2. Pay the original lower edge uniformly

The included U07 critical-parent proof gives the EXPLICIT positive expansion

    Pcritical(x)=y^(3r)+2x[c_r y^(3r)+E_r(y)],
    c_r=r(r-1)/[2(2r+1)],                                      (2)

where E_r(y) is the supplied nonnegative weighted sum of power differences
    y^(3r)-y^(r+2ell+1+j), with the lower exponent<=3r.
Every coefficient of E_r(1+2x) is nonnegative. Its weights, central-difference
sign proof and exact moment payment are supplied in the inherited full proof;
E_r is not an unknown positive capacity.

the main proof establishes the COMPLETE correlated envelope
    |B_r(p)|_coeff <= p(1+2p)^(3r)/[r(2r+1)],
and the companion bound
    |A_r(p)|_coeff <= p(1+2p)^(2r)/[r(2r+1)].
Substitute x=p+q, p,q>=0. All comparisons below are COEFFICIENTWISE in p,q,
not inequalities of positive integer values. Since(1+2p)^n<=_coeff y^n,

    |6y^r A_r(p)-6B_r(p)|_coeff
          <=_coeff 12p y^(3r)/[r(2r+1)].                       (3)

Combining ALL partners in(1)-(3) gives the independently checkable lower bound

    P >=_coeff y^(3r)
      +{2c_r q+[2c_r-2-12/(r(2r+1))]p}y^(3r)
      +2x E_r(y).                                             (4)

The remaining scalar reserve is

    2c_r-2-12/[r(2r+1)]
      =[(r-6)(r^2+r+4)+12]/[r(2r+1)] >0,  r>=6.              (5)

Thus the ENTIRE top-strip polynomial has nonnegative coefficients for EVERY
r>=6, including p=x (A=(r-1)b). In fact every coefficient through degree3r+1
is positive for b>0: y^(3r) supplies all lower degrees, and the positive
p or q reserve supplies the top degree. This proof pays the initial lower
edge directly. It does not infer that edge from positive width increments.
