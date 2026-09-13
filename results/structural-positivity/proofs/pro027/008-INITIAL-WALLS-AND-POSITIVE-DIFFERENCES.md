# Negative initial walls and an explicit positive finite-difference basis

The signs of entire ordinary LR polynomials and those of auxiliary corrections are different assertions. The negative auxiliary coefficients below are retained explicitly.

## 1. The whole initial wall for every y>=1

Use the full quadrant notation in [Complete two-parameter LR compensation and determinant duality](005-COMPLETE-QUADRANT-AND-DUALITY.md). Let P00,P10,Q0 be the one-parameter family's P0,P1,Q, and define

    W1=P01-P11+tQ1,
    Z=Q0-Q1+tR.

Direct exact polynomial arithmetic, with full vectors retained, gives

    W1=t(t-1)(t+1)(t+2)(t+3)(t+4)(t+5)
                        *(30+99t+116t^2+41t^3)/20160,
    Z =t(t-1)(t+1)^2(t+2)(t+3)(t+4)(t+5)
                        *(54+31t)/20160.                (1)

The ordinary coefficients of W1 in degrees 1–4 are

    -5/28, -275/336, -577/420, -13733/20160.

Those of Z in degrees 1–3 are

    -9/28, -1543/1680, -3541/5040.

Both polynomials vanish at 0 and 1 and are strictly positive at every integer t>=2. Thus they are complete count-correction polynomials with negative ordinary coefficients, not entire LR counterexamples. Their exact coefficient vectors are retained in DATA/wall-W1-raw.json and DATA/wall-slope-Z-raw.json.

The complete wall at x=0 is

    W_y=P_0y-P_1y+tQ_y=W1+(y-1)t Z, y>=1.              (2)

It follows in particular that

    [t]W_y=-5/28,
    [t^2]W_y=-275/336-(y-1)*9/28.

The latter tends without bound in the negative direction as y increases, even though every integer count W_y(t) is positive for t>=2 and every complete P_0y is ordinary-positive. This is a precise example of why neither positive sampled differences nor a positive mixed quotient controls an omitted initial wall.

At t=2, W1=255 and Z=87, so W_y(2)=255+174(y-1). In particular an extension of the interior-quadrant law to(0,1) would give11301 rather than the actual 11556. At y=0 the separate one-parameter correction W0 has value 90 at t=2 and its previously saved negative coefficients. Both wall corrections remain auxiliary polynomials and do not constitute LR counterexamples.

## 2. Complete positive differences, rather than positivity of the wrong pieces

Define the entire polynomial differences

    D=P10-P00,
    C=P11-2P10+P00,
    E=t(Q1-Q0).

The following ascending arrays specify exact positive factorizations:

    D=t(t+1)^2(t+2)*Dbar(t)/10080,
    Dbar=[5760,20568,35126,33963,19115,5733,695];

    C=t(t+1)(t+2)*Cbar(t)/40320,
    Cbar=[720,32364,145678,297412,323367,188033,54563,6183];

    E=t^2(t+1)(t+2)*Ebar(t)/40320,
    Ebar=[26640,137892,299428,330767,191969,55381,6243].     (3)

Every listed coefficient is strictly positive. D and C are strictly positive in every nonconstant degree 1–10; E is strictly positive in degrees 2–10 and has zero constant/linear terms. These conclusions come from exact full-vector identities, not the positivity of the separate parents alone.

For each integer x,y>=0 put

    i=1_(x>0), j=1_(y>0), a=max(x-1,0), b=max(y-1,0).

The complete count has the exact representation

    P_xy=P00+(i+j)D+(a+b)tQ0+ij C+(aj+bi)E+ab t^2R.      (4)

Checking the corner, the two axes and the positive quadrant against [Complete two-parameter LR compensation and determinant duality](005-COMPLETE-QUADRANT-AND-DUALITY.md) proves(4) exhaustively. Every multiplier is nonnegative, and every polynomial factor in(4) is ordinary-nonnegative; P00 is strictly positive through degree 10. This supplies an explicit ordinary-positive construction, with the initial corner and both walls included.

## 3. Monotonicity and supermodularity

At y=0 the first x-step is D and all later x-steps are tQ0. For y>=1, the first x-step is D+C+(y-1)E and later steps are tQ1+(y-1)t^2R. The analogous y statements follow from exact symmetry. Consequently every nonconstant ordinary coefficient strictly increases whenever either integer parameter increases by one.

The mixed first difference

    P_(x+1,y+1)-P_(x+1,y)-P_(x,y+1)+P_xy

is C at(x,y)=(0,0), E on the rest of either initial axis, and t^2R in the interior. All are ordinary-nonnegative. Thus the family is coefficientwise supermodular on the complete integer quadrant. This is a local whole-family statement, not the false universal LR coefficient-concavity claim and not a universal positivity-preserving summation theorem.

The positive C,D,E factors exhibit the compensation: individual wall polynomials in(1) remain negative in ordinary coordinates, but the complete allowable increments contain the compensating parent and slope contributions. An all-rank conclusion would still require a generation or coverage theorem; none is asserted.
