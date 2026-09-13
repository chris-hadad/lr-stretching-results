# Low-defect reflection implies positivity of every coefficient

This is an elementary symbolic derivation. Source polynomiality/reciprocity and the definition of true codegree are retained; no universal Gorenstein property or nonnegative numerator is assumed. This is not a worldwide-priority assertion.

## 1. Precise polynomial theorem

Let P be the period-one Ehrhart polynomial of a nonempty rational lattice polytope, with actual dimension d and true codegree q>=1. Suppose the COMPLETE reflection identity

    P(-t-q)=(-1)^d P(t)                                    (1)

holds. If q>=d-2, then every ordinary coefficient of P through its actual degree is strictly positive.

Proof: codegree gives the distinct roots -1,...,-(q-1). Put

    Bq(t)=binom(t+q-1,q-1),  r=d-q+1.

Since the leading coefficient is positive, q<=d+1; therefore 0<=r<=3. Write P=Bq*R with R(0)=1. The factors of Bq give Bq(-q-t)=(-1)^(q-1)*Bq(t), so

    R(-q-t)=(-1)^r R(t).

After centering at -q/2, R is even for even r and odd for odd r. Its complete possible form is consequently

    P(t)=Bq(t)*(1+2*t/q)^(r mod 2)*(1+eta*t*(t+q)),        (2)

where eta=0 for r=0,1, and eta>0 for r=2,3. For r=2 the quadratic is reflection-invariant and has constant one, so it is 1+eta*t*(t+q); eta is positive by the leading coefficient. For r=3 the centered odd polynomial has a factor 1+2*t/q, and its reflection-invariant quadratic quotient has constant one and positive leading coefficient. This proves (2), whose factors all have positive constant terms and nonnegative coefficients, strictly positive through their degrees. Every root has negative real part as well: the nontrivial quadratic has positive constant and linear terms and negative real part for both roots. This conclusion is confined to (1) and r<=3, without implying universal LR Hurwitz stability.

For an actual quintic with q=3, (2) becomes

    P(t)=binom(t+2,2)*(1+2*t/3)*(1+eta*t*(t+3)), eta>0.

It implies

    I(3)=1,  eta=(P(1)-5)/20,  P(2)=7*P(1)-21.            (3)

Conversely, for an actual quintic with I(1)=I(2)=0, the additional equalities I(3)=1 and P(2)=7*P(1)-21 force this factorization through the complete six-node interpolation identity in the source proof. The SINGLE condition I(3)=1 does not force reflection; the recorded rank-seven finite-box example is an actual LR counterexample to that inference.

## 2. A complete geometric hypothesis proving reflection

Use the ACTUAL full-dimensional affine lattice of the entire polytope, identified with Z^d, and its complete bounded facet description at stretch j:

    a_i . x + j*b_i >= 0,

with a_i and b_i integral. Homogenized rows can be made primitive before applying the following condition; primitive a_i alone is not a substitute for integral b_i. Globally forced equalities have already been eliminated by an exact saturated affine chart. Constant rows are treated separately.

Suppose an integer q>0 and a lattice vector w satisfy

    a_i . w + q*b_i = 1                                   (4)

for EVERY facet row. It is also sufficient to satisfy (4) for every nonconstant row of a complete retained inequality description, which is a stronger requirement if redundant rows are present. A selected subset of inequalities is insufficient.

An integer point is in the true relative interior at grade j exactly when all facet slacks are at least one. Subtracting w converts those inequalities into

    a_i . (x-w) + (j-q)*b_i >= 0.

Addition is the inverse. Hence for every j>=q there is an exact complete lattice bijection

    relint(jP) intersect Z^d  <->  w+((j-q)P intersect Z^d). (5)

At j=q, the grade-zero recession cone is {0}, because P is bounded. Thus I(q)=1. There are no earlier interior lattice points: boundedness makes the facet normals positively span the dual, so positive real beta_i exist with sum beta_i*a_i=0. Equation (4) gives

    sum beta_i*b_i = (sum beta_i)/q > 0.

A weak solution at negative grade j-q would then imply 0<=(j-q)*sum beta_i*b_i<0, a contradiction. Consequently q is the actual codegree. Reciprocity and (5), first at every sufficiently large integer grade and then as a polynomial identity, prove (1).

This theorem retains all facets, the primitive homogenized normalization, the actual affine hull and the saturated lattice. A unique first interior lattice point does NOT imply (4). A unit shift on non-forced facets of a guessed ambient chart is not a valid replacement.

## 3. Entire LR applicability and inherited control

The theorem applies to an entire stretched LR count only after the complete affine-interior translation or reflection is proved for that same family. No statement is made that all codegree-three quintics or all five-coordinate hives have reflection.

A previously certified whole-LR control has

    lambda=(5,4,3,2,1,1), mu=(2,2,1,1), nu=(4,3,2,1).

Its rank is six and outer area sixteen. The preserved complete coefficient vector is

    (1,67/30,11/6,3/4,1/6,1/60)

and factors exactly as

    binom(t+3,3)*(1+t*(t+4)/10).

Its positive leading coefficient gives actual degree five; reciprocity gives codegree four and the factorization proves the reflection. This is a previously computed illustrative positive member; no new count or finite-box coverage is asserted. The recorded vector is in DATA/P08/SMALL16-VECTORS.json.

Reflection and the source coefficient inequalities are different mechanisms.
The latter also cover nonreflective members, including the unique-first-interior
example. Complete unit-slack recognition and the two-dilation test require
separate checks; neither their cost nor whole-box membership is evaluated here.
