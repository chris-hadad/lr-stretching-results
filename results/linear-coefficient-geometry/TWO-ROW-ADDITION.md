# Addition with a common two-row inner-factor slot

## Pro039: original two-row interface transport

Let b=(lambda;mu,nu) and b'=(lambda';mu',nu') be feasible, with
nu=(p,q,0,...,0) and nu'=(p',q',0,...,0) in the same fixed inner slot.
The two-row partitions may have different parts. The accepted A006/A007 entire character reduction
defines free row widths w, forced double-column count C and k=q-C. It gives

    P_b(t)=[z^(tk)](1-z) product_i(1+z+...+z^(t w_i)).

Its complete first coefficient
F(w,k) is the inherited homogeneous concave hinge formula. No new positivity
territory is attributed to Pro039 merely for using those accepted premises.

The new original-boundary argument is the paired defect. At interface i put
x_i=lambda_(i+1)-mu_i and epsilon_i=(x_i)_+ +(x'_i)_+ -(x_i+x'_i)_+.
The elementary identity min(a,b)=a-(a-b)_+ proves, with epsilon_0=epsilon_n=0,

    w_i(b+b')=w_i(b)+w_i(b')+epsilon_(i-1)+epsilon_i,
    k(b+b')=k(b)+k(b')+sum_i epsilon_i.

Each epsilon is nonnegative, including every tie. In augmented polygon
coordinates a=(p-q,w_1,...,w_n), every correction is exactly
epsilon_i(e_i+e_(i+1)). It has F=0 and lies in the polygon cone. Thus the whole
original-boundary map, including its changing overlap interfaces, preserves
the superadditive comparison for F. In detail, for X=(w,k), Y=(v,l),

    F(X+Y)-F(X)-F(Y)
      = sum_J ((k-w(J))_+ +(l-v(J))_+ -(k+l-w(J)-v(J))_+)
               / (|J| binom(n-2,|J|)),

over every subset with 1<=|J|<=n-2. Every summand is nonnegative. Insert the
paired corrections sequentially and add these exact identities. This proves
f(b+b')>=f(b)+f(b') on the entire stated subcone, at arbitrary size and ambient
rank; rank two is the constant case. At rank six there are at most 336 terms.
All zero widths, degree drops and ties are literal. A fixed integral tensor
symmetry or determinant normalization commutes with addition and transfers
the statement to its corresponding fixed short-factor piece. Parents using
different transforms or inner slots cannot be mixed under this theorem.

Two nonadjacent interface losses contain a times four distinct polygon
coordinates, where a is their minimum. The associated complete polynomial
is 1+a t; the remainder is a nonnegative sum of polygon edges. The same
superadditivity argument therefore proves a lower bound of a on the gain.
The two source point parents with epsilon_1=epsilon_3=1 attain equality.

The included literal checker enumerates literal skew cells in row-reading order,
imposing weak rows, strict columns, complete content and every ballot prefix.
It imports no source enumerator or reduced-width producer. For the supplied
rank-six parent and its height-two-column addition, complete counts at t=0..6
are (1,6,19,44,85,146,231) and (1,13,66,211,520,1086,2023). The proved
degree<=4 and five determining counts plus two unused holdouts independently
recover the whole displayed polynomials. Their first-coefficient gain is 11/12,
also exactly eight hinge terms 1/12 and one term 1/4. These controls verify the
original-count bridge; the all-parent proof is the argument above.

For the three-label countercontrol, both parents have mu=(2,2,1,1,0,0),
nu=(3,2,1,0,0,0), zero free widths and three double columns. Outer shapes
(4,4,2,2,0,0) and (3,3,2,2,1,1) have entire polynomials 1 and 1+t.
For the first, the top rectangle forces rows 1/2 to be ones/twos, and the
remaining rectangle is forced to be ones/threes. For the second, the three
separated rectangles force rows 1/2 and row 3; row 4 can contain k twos then
t-k threes, row 5 is all ones and row 6 contains t-k twos then k threes,
with exactly 0<=k<=t. Every choice satisfies the full word and exhausts it.
Literal independent complete counts at all 26 fibers t=0..12 agree. Thus this
specific width coarsening loses necessary three-color incidence, even with
both inner partitions retained. It does not refute richer encodings or KTT.

Global superadditivity remains false by the previously accepted actual upward
wall: two endpoints around its unit crossing have merge defect -1/168, with
positive original coefficients. The restricted theorem must not be promoted
to the full cone. Monotonicity under feasible addition is a weaker open target.


## Complete inherited inputs

The [whole two-row reduction](proofs/two-row-reduction.md) fixes the original
rows, columns, content, ballot and zero-family conventions. The
[complete hinge proof](proofs/two-row-linear.md) proves concavity and
nonnegativity on the polygon cone used above. These hypotheses concern the
fixed slot; choosing unrelated tensor symmetries for the two inputs is outside
the theorem. Since each feasible summand has nonnegative c1, superadditivity
also gives monotonicity under adding a feasible summand in this same domain.
