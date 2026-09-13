# Independent root check of the coupled-simplex counts

Status: root derivation from the geometry lane's proposed displayed models;
conditional on its complete hive/lattice/domain certificate until reviewed.
No fitted arrays, LR values or native count implementation enter this argument.

For a uniform weak composition `(u0,...,u7)` of a nonnegative integer `w`, let
`X` be the sum of `r` of its eight coordinates. With falling/rising factorials,

    E[(X)_falling k] = (w)_falling k (r)_rising k / (8)_rising k.

Proof: mark the chosen coordinates with `z` in the composition generating
function `(1-zx)^(-r)(1-x)^(-(8-r))`, differentiate `k` times in `z`, and take
the coefficient of `x^w` at `z=1`. The result is
`(r)_rising k binom(w+7,7+k)`, divided by `binom(w+7,7)`. This gives the
identity for every `w>=0`, with the usual zero falling factorial at `w<k`.
This finite counting argument includes all zero-parameter boundary cases.

## 48-corner model

The proposed model is a `Delta7(w)` base, an independent interval of length
`a`, and a two-dimensional simplex whose total is `b+q0+q2` in the geometry
lane's coordinates; the last two terms select two base coordinates. The parameter
identification is `a=s14,b=s15,w=s16`; all must be nonnegative integers on
every integral boundary of the represented cone, not only integer ray sums.

For `r=2`, the factorial-moment identity gives

    E[X] = w/4,
    E[X^2] = w^2/12 + w/6.

Summing the interval and simplex gives

    E48(a,b,w) = (a+1) binom(w+7,7) E[binom(b+X+2,2)]
      = (a+1) binom(w+7,7)
        (12b^2+36b+24+6bw+11w+w^2)/24.

The numerator follows by expanding
`((b+X)^2+3(b+X)+2)/2` and inserting the two moments. It is the full
lattice count of this model, without polynomial interpolation.

## 32-corner model

The proposed model is a `Delta7(w)` base and a three-dimensional simplex of
total `a+q0+q1+q5+q8` in the geometry lane's explicit-coordinate indexing.
There are still eight base composition coordinates, including the implicit
one. Here `a=s15,w=s16`, with the same full integral-boundary obligation.

For `r=4`, independently from the general identity,

    E[X] = w/2,
    E[X^2] = 5w^2/18 + 2w/9,
    E[X^3] = w^3/6 + w^2/3.

Consequently

    E32(a,w) = binom(w+7,7) E[binom(a+X+3,3)]
      = binom(w+7,7)
        (6a^3+36a^2+66a+36+9a^2w+40aw+41w
          +5aw^2+12w^2+w^3)/36.

This uses `(z+1)(z+2)(z+3)/6=(z^3+6z^2+11z+6)/6` with `z=a+X`.
The cancellation of the linear term in `E[X^3]` is exact, not a rounded zero.

## Corner generation and ordinary coefficients

The simplex-fiber generation lemma can be proved directly. Suppose a base
point is `u=sum_i theta_i v_i` and the fiber is `z_j>=0,sum z_j<=L(u)`,
where `L` is affine and nonnegative on the whole base. If `L(u)>0`, put
`alpha_j=z_j/L(u)` and add `alpha_0=1-sum alpha_j`. The point `(u,z)` is
the convex combination with weights `theta_i alpha_j` of
`(v_i,L(v_i)e_j)` and `(v_i,0)`. Affineness gives
`sum_i theta_i L(v_i)=L(u)`. If `L(u)=0`, all positive-weight base vertices
have `L(v_i)=0`, and the zero fiber is already represented. Apply this lemma
successively with the independent interval. It generates `8*3*2=48` and
`8*4=32` symbolic corners, allowing collisions on parameter faces.

This proves generation for the displayed models. Identifying them with the
complete hives still requires the lane's selected-raw-row inclusion, every
raw slack at every symbolic corner/domain generator, full seed vertices and
unimodular lattice and integral-boundary certificates. No source-reported
vertex count alone supplies any of those premises.

Both displayed count formulas have nonnegative coefficients in their boundary
parameters: every displayed numerator coefficient is positive and
`binom(w+7,7)=prod_(j=1)^7(w+j)/7!` does too. After simultaneous stretching
`(a,b,w)->(ta,tb,tw)` or `(a,w)->(ta,tw)`, every ordinary coefficient in `t`
is nonnegative, including on zero-parameter faces. This also proves mixed
coefficient nonnegativity in these effective parameters in every degree;
expansion in all 17 ray parameters merely adjoins variables on which the count
does not depend. These statements are conditional on the precise parameter
identifications and represented cone verified by the geometry certificate.

The two formulas have generic degree ten. No real-rootedness, full-fan
coverage, rank-wide theorem, boxed cardinality or ordinary-negative witness
is inferred. The root's separate acceptance follows independent review.
