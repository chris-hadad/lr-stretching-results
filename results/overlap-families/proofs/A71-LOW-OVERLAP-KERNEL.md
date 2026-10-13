# A71: the entire low-overlap kernel beyond the one-sided strip

Curated accepted mathematical source; the module guide states its exact domain.

Let L>=1, 0<=H<=G, X>=0 and 0<=C<=B=X+H+G be integers. Put

```text
A_n(z)=binom(z+n,n), R_n(z)=binom(z+n-1,n), R_0=1,
D=(1-x)(1-y), r_n=h_n(x,y)-xy h_(n-1)(x,y).
```

The complete dominant coefficient

```text
K_L(B,C;H,G)=[x^B y^C](1-y/x) r_H r_G / D^(L+2)
```

is

```text
K = R_(L+1)(X) A_L(C)
    +sum_(w=0)^min(H,C) A_L(X+w) A_L(C-w)
    -sum_(w=G+1)^C A_L(X+w) A_L(C-w)
    +sum_(q=0)^(C-H-G-2) A_(L-1)(B+2+q)
                                  A_(L+1)(C-H-G-2-q).    (1)
```

Every sum with upper endpoint below its lower endpoint is zero. The strict G+1, reflected -2 and B+2 are scalar integer offsets, applied ONCE, not extra stretch shifts. Formula (1) includes H=0, G=0, X=0 and all equality boundaries.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation from the full rational character. This independently reconstructs the escaped strict prefix from completed Pro050 and retains the returning reflected correction. It is a COMPLETE COUNT IDENTITY, not a coefficient-sign theorem outside the accepted one-sided region. No provider program is used.

## Direct complete extraction

Use

```text
r_n=[x^(n+1)(1-y)-y^(n+1)(1-x)]/(x-y).
```

After multiplying both complete numerators and the Weyl factor, expand
1/(x-y)=x^(-1)sum_(q>=0)(y/x)^q. At fixed y^C the sum is finite, so coefficient extraction is legitimate in the iterated Laurent field. The four numerator terms give:


```text
T0=sum_(q=0)^C A_(L+1)(X+q) A_(L-1)(C-q),
TH=sum_(w=H+1)^C A_L(X+w) A_L(C-w),
TG=sum_(w=G+1)^C A_L(X+w) A_L(C-w),
TR=sum_(q=0)^(C-H-G-2) A_(L-1)(B+2+q)
                                  A_(L+1)(C-H-G-2-q),
```

with K=T0-TH-TG+TR. These are the four entire numerator contributions. They are not four independently positive ordinary-coefficient summands.

Pascal summation, including the first endpoint, gives

```text
A_(L+1)(X+q)=R_(L+1)(X)+sum_(w=0)^q A_L(X+w).
```

Substitute into T0 and sum every remaining A_(L-1) term. Then

```text
T0=R_(L+1)(X)A_L(C)+sum_(w=0)^C A_L(X+w)A_L(C-w).
```

Combining with TH proves (1) without discarding either TG or TR.

If C<=G, TG and TR are both zero, recovering the A71 one-sided positive primitive. For G<C<=H+G+1, TR is still empty and the whole missing correction is

```text
TG=sum_(z=0)^(C-G-1) A_L(X+C-z)A_L(z).
```

Thus the first strict prefix has exactly the source's once-only -1 endpoint, and the identity in fact states its zero-reflection band precisely. At C>=H+G+2 the complete reflected term returns. The general sign of their fully aggregated original contribution is unpaid.

## Complete original extension and its additional residual bound

Keep PRO050-ADOPTION.md's physical backward original with L>=1, b>=c>=1,
h,g>=0, h+g<=c, three long widths u,v,k>=b, but now permit EVERY
0<=j<=b and s>=j, with each detached width at least b+c-h-g-j.
There is no U<=G condition. Define A=c-h-g, delta=b-c, U=b-j,
V=max(b-s,0), H=min(h,g), G=max(h,g).

The entire determinant, annihilator and tail-cap argument in that note did
not use U<=G. Its complete highest-weight expression therefore still holds.
The horizontal-strip telescope, before simplifying its support, gives EXACTLY

```text
P(t)=sum K_L(ct+x,y; Ht,Gt),                         (2)
```

over

```text
x,y>=0, x<=delta t, y<=ct, Vt<=x+y<=Ut.
```

Here X=At+x>=0 in (1), and the bound y<=ct retains the telescope's i<=q
condition. It is automatic in the one-sided class U<=G<=c, but is NOT
automatic for this larger class and may not be removed. All arguments of K
remain dominant B>=C. Substituting every term of (1) into (2) is a finite
exact all-grade formula for the entire original with all old floors and
the new complete correction structure explicit.

At t=0 the sole residual state is x=y=0 and K=1. The construction preserves
legal partitions, the size equation, original physical zeros and all integer
coordinates. No independent actual-degree formula or coefficient signs for
the enlarged class are asserted; they require their own full cancellation
and degree arguments. (2) is a count/coefficient-extraction identity, not a
hive isometry or a replacement lattice.

## Verification and decision

A fresh root checker compares (1) with independent direct polynomial
multiplication of BOTH r factors and binomial coefficient extraction of
D^(-L-2), for the complete frozen finite domain L=1..4, H=0..3,
G=H..4, X=0..4 and every C=0..X+H+G. It keeps all low, escaped and
reflected strata, and detects omitted TG, omitted TR and an incorrect
strict endpoint. These are auxiliary coefficient kernels, not new numerical
LR originals or an enlarged candidate search. The algebra above provides
the arbitrary-parameter quantifier.

This gives Pro052 an exact complete next object rather than a favorable
one-sided formula extrapolated into an unpaid region. It does not sign that
object or the middle overlap c<h+g<b, remove the three long floors or
effective detached caps, or settle unrestricted KTT. Local A72 remains
directed at nonfree transportation parents; these character corrections are
a complementary serious route and a possible switch if that gain fails.
