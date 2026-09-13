# Short primitive normals protect the third-highest coefficient

FRONTIER-025 P07. Originating derivation, subject to campaign verification; no worldwide-priority claim. The local Euler–Maclaurin/Berline–Vergne (BV) face formula and its quotient-lattice convention are source premises, not new theorems here. See P07-SOURCE-DEPENDENCIES.md. All inequalities below are proved symbolically; the finite controls are not their logical basis.

## 1. Statement and lattice convention

Let P be a bounded, full-dimensional rational polytope of dimension d>=2 in a specified saturated lattice, identified with Z^d by an integral basis. Suppose its Ehrhart count is a polynomial (period one). Give this chosen coordinate space the standard Euclidean scalar product. If every primitive inward facet normal u satisfies ||u||^2<=6, then

    [t^(d-2)] L_P(t) > 0.                                      (1)

More quantitatively, in this metric every codimension-two BV weight is at least 1/100. Thus

    [t^(d-2)] L_P(t) >= (1/100) sum_(dim F=d-2) vol_Z(F) > 0.   (2)

The volumes are normalized in the face lattices. This does not assert the signs of lower coefficients, primitive generators of an arbitrary normal atlas, or arbitrary rational quasipolynomial constituents. An affine lattice change need not preserve BV weights: the metric is deliberately chosen AFTER choosing the lattice basis. Ehrhart coefficients themselves are unchanged by the coordinate identification.

## 2. The complete two-dimensional local constant, with its index

Let u,v be the two extreme primitive inward normals at a codimension-two face. Put

    a=||u||^2, b=||v||^2, c=<u,v>,
    q=[(span_R(u,v) intersect Z^d) : Zu+Zv].

Equivalently q is the positive gcd of the 2-by-2 minors of the two-row matrix (u;v). Since u is primitive, choose an integer vector w with <u,w>=1 and put p=<v,w> modulo q. This is independent of that choice modulo q, and gcd(p,q)=1; use p=0 when q=1. In a basis of the saturated dual plane, u=(1,0), v=(p,q). One way to see this is to complete primitive u to a basis (u,e), write v=p*u+q*e, and use the definition of the lattice index. Primitivity of v makes p coprime to q. This also proves the Bezout-vector description of p.

Define the finite sum

    s(p,q)=sum_(k=1)^(q-1) (k/q-1/2)*((p*k mod q)/q-1/2).

It is zero for q=1. The complete local weight is

    alpha(u,v) = 1/4 + s(p,q) - c*(1/a+1/b)/(12*q).           (3)

This is the weight of the TANGENT quotient dual to the two inward normals, not the BV value obtained by treating the normals as primal tangent rays. Both the minus sign and q matter.

Here is a direct derivation from the BV recursion, including the finite-lattice correction. The tangent quotient uses the projected lattice, whose dual is precisely the saturated normal plane; it is not generally the intersection of the ambient integer lattice with the orthogonal plane. In the dual basis above its primitive tangent rays are

    e=(0,1), f=(q,-p).

Their fundamental half-open parallelogram contains q lattice points. In coordinates alpha*e+beta*f these have

    beta_k=k/q, alpha_k=(p*k mod q)/q, 0<=k<q.

Let A=<xi,e>, B=<xi,f>, nonzero for the formal calculation. Expanding the ENTIRE parallelogram numerator divided by (1-exp(A))*(1-exp(B)), its degree-zero part is

    S0=sum_k [1/4+A/(12B)+B/(12A)
              -(alpha_k*A+beta_k*B)*(1/A+1/B)/2
              +(alpha_k*A+beta_k*B)^2/(2AB)].                (4)

The complete finite moment identities are

    sum alpha_k=sum beta_k=(q-1)/2,
    sum alpha_k^2=sum beta_k^2=(q-1)*(2q-1)/(6q),
    sum alpha_k*beta_k=(q-1)/4+s(p,q).

They reduce (4) to 1/4+s(p,q)+(A/B+B/A)/(12q). In the projected one-dimensional quotient along e, the primitive generator is the projection of f/q, not f; along f it is the projection of e/q. The two edge terms subtracted in the BV recursion consequently have degree-zero sum

    (B-<e,f>*A/||e||^2)/(12qA)
      +(A-<e,f>*B/||f||^2)/(12qB).                           (5)

The full cone integral has degree -2 and no constant. Subtracting (5) from (4) gives

    alpha=1/4+s(p,q)+<e,f>*(1/||e||^2+1/||f||^2)/(12q).

The Gram matrix of the duals of u,v is (1/(ab-c^2))*[[b,-c],[-c,a]]. The two primitive tangent rays are q times these dual vectors, in opposite order. Therefore the last inner-product ratio is -c*(1/a+1/b), proving (3). The covector A,B has disappeared, as required. This calculation is valid for every integral q, not just unimodular cones.

## 3. Bounds forced by short integral normals

Assume a,b<=6. Cauchy–Binet gives

    q^2 <= ab-c^2 = sum_(i<j) (u_i*v_j-u_j*v_i)^2 <= 36.

If q=6, equality holds throughout: a=b=6, c=0, and exactly one minor is +/-6 while all other minors are zero. The two columns of that nonzero minor are independent, so every other column must vanish. Each of u,v would then be an integer two-coordinate vector of squared norm six. This is impossible: six is not the sum of two integer squares. Thus

    1<=q<=5.                                                 (6)

Also

    c*(1/a+1/b) <= 12/5.                                     (7)

For c<=0 this is immediate. Otherwise assume a<=b. If a>=2, Cauchy–Schwarz gives a strict bound by sqrt(b/a)+sqrt(a/b), at most 4/sqrt(3)<12/5 because b/a<=3. If a=1, integrality and c^2<b imply c<=1 for b=2,3,4, and c<=2 for b=5,6; the largest resulting ratio is 12/5 at b=5,c=2. For a=b=1 independence forces c=0.

Multiplication by p permutes 1,...,q-1. Cauchy–Schwarz applied to the two centered finite sequences gives

    s(p,q) >= -(q-1)*(q-2)/(12q).                            (8)

Using (6)-(8) in (3), the lower bounds for q=1,2,3,4,5 respectively are

    1/20, 3/20, 23/180, 3/40, 1/100.

All are positive. No realization assumption on the pair has been used; therefore the statement covers every actual codimension-two face without enumerating its incidences. Such a face has exactly two extreme normal rays even when other normal cones of P are nonsimplicial. Each extreme ray is an actual facet normal, so no conormal from a triangulation has been substituted.

## 4. From the local bound to the entire coefficient

First assume P has integral vertices. The BV local Euler–Maclaurin formula gives

    [t^(d-2)]L_P = sum_(dim F=d-2) alpha(F,P)*vol_Z(F).

Every summand has a positive relative volume and a weight bounded below as above, proving (1)-(2). For rational period-one P choose an integer m clearing all vertex denominators. The facets and primitive normals of mP are the same, its face volumes scale by m^(d-2), and

    L_(mP)(t)=L_P(mt).

Thus its coefficient scales by the SAME positive factor m^(d-2); dividing proves both assertions for P. This step does not assume that the individual affine BV terms of an undilated rational polytope are nonperiodic, or that the original vertices are integral.

## 5. A usable sufficient whole-hive chart

Suppose every original hive interior coordinate is an integer constant plus one selected free coordinate, or an integer constant alone. Suppose also that the selected free coordinates give an integer inverse and that ALL original rhombus inequalities are retained. Then the whole affine lattice is Z^d in those selected coordinates. Each rhombus has at most two positive and two negative unit entries. After coordinate identification its positive coordinate mass and negative coordinate mass are each at most two.

Every nonzero primitive integer vector with these two mass bounds has squared norm at most six. Before primitive reduction the only way to attain a squared norm exceeding six is the pattern (2,-2), which reduces to (1,-1). The largest remaining pattern is (2,-1,-1), of squared norm six. Therefore every actual facet normal of this whole chart satisfies the theorem. Redundant inequalities can be retained; a facet is supported by one of the original nonconstant inequalities.

This is a genuine lattice-membership condition, not an assertion about arbitrary affine elimination. Substitutions involving sums, negative copies, fractions, or a nonsaturated inverse require a new check. In P07 every one of the 206 actual degree-twelve boxed hives passes the full condition with its explicit chart and strict point.
