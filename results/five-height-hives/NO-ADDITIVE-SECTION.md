# Integral lifts need not admit an additive global selector

## 2. No additive original-hive section; exact two-chart control

Use the literal rank-three boundary family

    lambda = (S+X,S,S-X), mu = (S,Y,0), nu = (S,S-Y,0),
    S >= 0, 0 <= X,Y <= S.

In the original saturated height coordinate h12 = 2S+Z the nine rhombi give

    max(0,X+Y-S) <= Z <= min(X,Y).

The full row list is (S+Z-X-Y,Y-Z,S+Z-X-Y,X-Z,Z,Z,Z,Z,X-Z).
Every bound is integral, with inverse insertion of h12; the entire count is
1 + t min(X,Y,S-X,S-Y). Literal tableaux independently realize the same interval:
put z = Z+S-X-Y, with row multiplicities 1^X; 1^z 2^(S-Y-z);
1^(S-X-z) 2^z. Nonnegative row lengths, content, columns and ballot give exactly
the stated interval after translation. Empty padded rows preserve rank-six
hives through the standard original tableau/hive bijection.

At (S,X,Y) = (1,1,0),(1,0,1),(1,0,0),(1,1,1), call the boundaries A,B,C,D.
Their unique h12 values are 2,2,2,3, but A+B = C+D. Every additive selector would
preserve that relation, an impossibility. An affine selector on the convex
square also preserves it because each side has coefficient sum two. These
are point families at all grades, not just four isolated count observations.
The section Z = max(0,X+Y-S) has two unimodular charts, with nonnegative
coordinates (X,Y,S-X-Y) or (S-Y,S-X,X+Y-S). They agree on X+Y=S.
One chart is impossible and two suffice on this precise control cone.


This obstruction complements the constructive five-height lift. It excludes
a global additive or affine original-hive selector on the displayed cone;
piecewise integral selectors remain available. It is not an obstruction to
LR coefficient positivity. The argument is credited to Pro041 U12 and its
independent A53 reconstruction.
