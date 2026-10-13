# A59: exact two-cap bands and a legal-original obstruction to signing them separately

Curated mathematical proof from **A59**. The corresponding accepted scope
is stated in the module guide; [the source map](../SOURCE-MAP.json) binds its
original bytes and this editorial projection. Mathematical formulas and
physical-boundary conventions are retained.

**Originating mathematical scope and premises.** The module guide and claim lineage state the current scientific scope and status; originating proof qualifications remain explicit below.

Root derivation, 27 September 2026. This extends the complete accepted A58
absorber count, not its one-cap sign theorem. Both Weyl partners, all original
rows and once-only shifts have already been retained in that accepted map.
No provider working return was used in this derivation.

## 1. Complete two-small-cap original and saturated chain map

Use the literal A58 absorber original, with a>=3, caps k_1,k_2>=0, all
other caps k_i>=d, k_a>0, K=sum k_i, c=K-d>=1, b=c+delta>=c,
p=b-h>=0, 0<=h<=b, and paired row widths u,v>=b. The complete residual is


```text
U_i,Z_i>=0, sum_i(U_i+Z_i)=dt,
sum_i U_i<=pt, U_a<=delta t,
U_1+Z_1<=k_1 t, U_2+Z_2<=k_2 t.                   (1)
```

The other caps are automatic because k_i>=d, not discarded small caps.
The original remains lambda=(K+u+v-h,K+v,sigma_1,...,sigma_a),
mu=(K+v-h,K,sigma_2,...,sigma_a,0), nu=(u+v+K-b-c,b,c).
The A58 proof establishes legality and equality of the two shifted partners
with (1), including empty second domains and zero caps.

Order the 2a increments as

    Z_1,U_1,U_a,U_3,...,U_(a-1),U_2,Z_2,Z_3,...,Z_(a-1),Z_a,

and let x_1,...,x_(2a-1) be their cumulative sums. This is a unimodular
integer map after eliminating Z_a from the primitive total equation; the
inverse takes consecutive differences. The ENTIRE domain is


```text
0<=x_1<=...<=x_(2a-1)<=dt,
x_2<=k_1 t,
x_(a+2)-x_a<=k_2 t,
x_(a+1)-x_1<=pt,
x_3-x_2<=delta t.                                 (2)
```

Thus two small caps admit an exact interval-constraint representation, with
one long aggregate span and the absorber span both retained. Dropping those
spans would change the full original. Unlike A58's one-cap ordering, the
aggregate constraint is not an upper flag on a single cumulative coordinate.

For d=0 the result is a point. For d>0, if E is the number of positive caps,
the actual degree is E-1 at p=0, 2E-2 at p>0,delta=0, and 2E-1 at
p>0,delta>0. These are the saturated-lattice dimensions established by the
A58 full absorber map. Zero cap/flag equalities in (2) identify consecutive
coordinates or force a prefix to zero; they are primitive, not relaxed.

## 2. Exact fixed bands and their full order polynomials

For t>=1 write a positive coordinate uniquely as
x_i=(beta_i-1)t+v_i, 1<=v_i<=t; zero coordinates have beta_i=0 and x_i=0.
The beta sequence is weakly increasing in 0..d, with beta_2<=k_1.
For each remaining span x_j-x_i<=kt:

- if beta_i=0, require beta_j<=k;
- otherwise require beta_j-beta_i<=k, with the extra comparison v_j<=v_i
  exactly when equality holds.

Inside an equal positive band, preserve the forward chain comparisons.
Collapse strongly connected comparison classes: their coordinates are equal,
with a primitive inverse duplication map. Different zero-band coordinates
are fixed zero, never free order variables. This handles k=0, p=0 and
delta=0 without strict-endpoint or cyclic-order errors.

Let P_beta be the resulting finite poset on the free classes and
Omega_beta(t) its weak order polynomial for values 1,...,t. Every admitted
beta contributes exactly Omega_beta(t), and all integer points appear once.
Therefore the complete original polynomial equals


```text
sum_(all admitted beta) Omega_beta(t).              (3)
```

The all-zero beta pays the constant one. Empty/collapsed factors and actual
degree remain as above. Formula (3) is a uniform complete count reduction;
it does not assert that every summand is coefficient-positive.

## 3. Exact obstruction on the original rank-seven control

Take a=5, caps=(1,1,3,3,3), d=3,p=2,delta=1, b=9,c=8,h=7,u=v=9.
The literal original is


```text
lambda=(22,20,11,10,9,6,3),
mu=(13,11,10,9,6,3,0),    nu=(12,9,8).
```

Its full degree-nine polynomial is positive (independently rechecked here).
Nevertheless its ADMITTED band


```text
beta=(1,1,1,1,2,3,3,3,3)
```

has ordinary linear coefficient -1/420. Write W_j for its free coordinates
in order, 1..9. Its relations are the chains 1<=2<=3<=4 and 6<=7<=8<=9,
plus 6<=1 and 7<=5. There is no relation from 5 to the other low band.
The absorber span is slack within the first band. The cap-2 and aggregate
spans give precisely 7<=5 and 6<=1 respectively. Thus the sector retains
all inequalities of the full original, not a favorable partial extraction.

A natural labeling is given by the topological order (6,1,2,3,4,7,5,8,9).
Enumerating its 210 linear extensions gives descent histogram
(1,26,96,76,11), so its COMPLETE polynomial is


```text
Omega(t)=binom(t+8,9)+26binom(t+7,9)+96binom(t+6,9)
                     +76binom(t+5,9)+11binom(t+4,9).
```

This identity follows directly by sorting weak maps by their values and
breaking ties with the natural labels: each descent forces one strict gap.
It is not an interpolation argument. Expanding gives


```text
-t/420 + t^2/48 + 31t^3/216 + 173t^4/576
+293t^5/960 +49t^6/288 +107t^7/2016 +5t^8/576+t^9/1728.
```

Independent enumeration directly in (U_i,Z_i) gives 1,36,411,2686 at
t=1,2,3,4. The second admitted negative band
(1,1,1,2,2,3,3,3,3) has linear coefficient -1/840; its full identity
and descent histogram are in `sector-verify-v1.json`. The balanced
original (delta=0,b=c=8,p=2,h=6) has a degree-eight band with c1=-1/280.

This is a decisive obstruction to the proposed certificate that signs every
fixed-band factor on complete two-cap originals. It is NOT a negative LR
polynomial: the full sum (3) is positive in the tested originals. In the
rank-seven p=2 control there are 134 admitted beta states and 106 distinct
labeled factors; exactly two factors have a negative coefficient, both
linear. A repaired method must group or pay these complete sectors.

The overlap-gain analogue fails termwise too: 23 surviving band transitions
in the checked p=1->2 and p=2->3 changes have negative coefficients, while
all three complete overlap gains p=0->1->2->3 are positive. Increasing
an interval bound can remove an order comparison within an existing beta;
it does not merely select additional unchanged positive bands as in A58's
upper-flag theorem. No cap- or overlap-monotonicity theorem follows here.

## 4. Exact verification and surviving direction

`two_cap_bands_v1.py` enumerates every beta and exact ideal poset, counts
all determining grades plus two unused holdouts, and compares every full
count to both an independent residual-pair DP and the separate bare-original
LR tableau engine. Eight complete originals cover p=0,1,2,3, balanced
output, either zero small cap, and the point. The 175 distinct factors have
three negative linear-coefficient cases; no whole negative is found.
`sector_verify_v1.py` independently derives the three full polynomial
identities from finite linear extensions and verifies their integer sectors
without the chain-map counter. `partner_controls_v1.py` checks all 77
full shifted-partner differences. At grade two the correct value 2902
changes to 3472,3379,3008,2584,2993,2146 when respectively deleting
the second cap, aggregate flag or absorber flag, omitting or stretching
the once-only offsets, or making the second cap endpoint strict.
Runtime and source receipts retain exact scope.

An earlier selected three-chain subfamily tested c1>0 for a=3..40 and every
coefficient for a=3..10. That incomplete selection missed the actual negative
bands above; it is preserved in `band_probe_v1.py` and its receipt as a bounded
failed discriminator, not evidence of full factor positivity.

KEEP the uniform complete count reduction, CHANGE the factor-sign architecture
to grouped sectors or a joint reserve, and retain no-absorber/interacting-overlap
parents as competing general routes. The balanced arbitrary-cap K-2 theorem
is an independent whole-original reserve result; it does not sign (1) in
general. Whole rank seven and general KTT remain open; candidate count stays
zero and

The source title Pro046 U06 two-cap operator concerns a different balanced
two-overlap count with two short factors and all remaining caps at least
p+q. Its exact domain is not the absorber count (1). The negative sectors
here do not contradict that unadopted source theorem or A58's accepted one-span theorem.
