# Normal-cycle balance and exact local recurrence

For the five-capacity application, the main proof supplies every original
normal and saturated quotient lattice. A field assigns a kernel vector at
each codimension-one support and changes each local weight by the sum of its
primitive conormal pairings. All omitted support vectors are zero.

## 4. From finite local weights to every whole object

This uses the Berline-Vergne dual-solid valuation and the complete refined-normal-cycle argument, restated here for the original normal systems and coordinate lattices. Here the original polytopes are bounded and integral in their fixed saturated lattice.

For clarity, the full implication is as follows. Loosen ALL original inequalities by a generic positive small amount. The resulting polytope is bounded, full-dimensional and simple, and its fan gives a compatible pointed simplicial refinement of the original normal fan using only the original normal rays. Every surviving vertex basis limits to an original vertex, so no unrelated face is inserted. Only this fan is used; no Ehrhart polynomial of a perturbed object is transferred by continuity. This includes original hidden affine strata and non-simple walls.

Fix k>=1 and q=D-k. Give each q-cone of the refinement the saturated normalized volume of the actual k-face whose coarse normal cone contains its relative interior, or zero if there is no such face. These weights are nonnegative. At each (q-1)-support, their complete primitive quotient-conormal sum is zero: at an actual (k+1)-face this is lattice facet balance; inside a subdivided coarse q-cone the adjacent primitive directions cancel with equal weights; inside a larger coarse cone all weights are zero. These are the same original quotient lattices used in (5).

The BV dual-solid valuation adds the local constants over subdivision cells, with the actual ambient/subspace lattice compatibility. The local formula and balance give

    c_k=sum_I w_I alpha_I=sum_I w_I beta_I.                       (6)

The correction equality collects each h_J against its entire zero balanced sum. With the zero field, beta=alpha. If every beta is at least epsilon, each actual k-face contributes at least one cell, so (6) implies the full face-volume bound. When there is an actual k-face, its normalized volume is positive. For k=D the zero normal cone has weight one, giving ordinary volume. If actual degree is below k, both sides are zero. Constant one is established by nonempty integral Ehrhart counting, without a q=D computation.


## 6. Complete local recurrence and compact fields

For q independent original normal rows N and each row subset T, set L_T=N_T Z^D, I_T=[Z^T:L_T], and H_T=N_T N_T^T. The induced normal-coordinate metric is H_T^(-1). The primitive positive coordinate axis at i has length r_(T,i)=I_T/I_(T without i). The finite numerator consists of all points p in L_T with 0<=p_i<r_(T,i); its cardinality is product_i r_(T,i)/I_T. These indices and complete numerator sets retain the original lattice. They are all trivial numerators here because every independently admitted row system has index one.

Choose a generic vector w compatible across subsets and put c_T=H_T^(-1) w_T. Define

    S_T(s)=sum_p exp(s*c_T.p)/product_i(1-exp(s*r_(T,i)*c_(T,i))).

With mu_empty=1, the complete local Euler-Maclaurin recurrence is

    mu_T(s)=S_T(s)-sum_(nonempty U subset T)
      (-1)^|U| * I_(T without U)/I_T
      * mu_(T without U)(s)/(s^|U| product_(i in U)c_(T,i)).

The local weight is the constant term of mu_full. Multiplication by s^|T| permits a common normalized Taylor truncation through q; every smaller-face series is retained through exactly the degree required by its integral factor. The denominator expansion is

    1/(1-exp(z))=-1/z+1/2-z/12+z^3/720-z^5/30240+O(z^7).

After multiplying by z the next term is degree eight, so the displayed terms suffice for all q<=7. Pole cancellation is checked but does not by itself certify the constant: omission of the degree-six Bernoulli term can leave poles canceled and change a local value. Two independently organized exact implementations reproduce all 16,848 admitted constants, including every raw negative.

The BV local formula and dual-solid valuation are from Nicole Berline and Michele Vergne, [Local Euler-Maclaurin formula for polytopes](https://arxiv.org/abs/math/0507256). The lattice-coordinate recurrence is its exact specialization; numerical agreement does not substitute for the analytic theorem.
