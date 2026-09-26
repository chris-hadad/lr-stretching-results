# The complete first coefficient on one cut cell

Write a balanced boundary vector x=(lambda,mu,nu) in eighteen coordinates.
For equally sized nonempty proper subsets U,I,J of {1,...,6}, define
Phi(U,I,J)=sum(mu_i,i in I)+sum(nu_j,j in J)-sum(lambda_u,u in U).
Trace balance makes the complementary form its negative. It suffices to use
U contained in {1,...,5}. There are exactly
sum(k=1,...,5) binomial(5,k) binomial(6,k)^2 = 7,591 such forms.
Every cut of every slope p(mu)+q(nu)-lambda is one of these forms or its
negative. In particular, this roster includes every prefix support test and
every selected tree cut for every one of the 720-by-720 Weyl pairs.

Fix an exact legal seed x0. The relative cell keeps each nonzero Phi at
its seed sign and each zero Phi identically zero. Impose balance and legal
partition order, retaining the seed's zero gaps and positive gaps as equalities
and strict inequalities respectively; treat each final coordinate similarly.
Thus the recorded system is E x=0 and A x>0. It is nonempty because x0
satisfies it. This strict cell includes all its prescribed tied strata;
new equalities on its remaining faces are not silently included.

All tree and support selections in the accepted formula are constant on
this cell. At zero slope cuts, the original offset and inward perturbation
are unchanged. Each selected term is a fixed rational number J_T(q_T(delta))
times the linear form q_T(p(mu)+q(nu)-lambda), with its Weyl sign. Therefore
the complete c1 is one exact rational linear functional g.x on this cell.
Retain selected terms even when their slope happens to vanish at the seed:
that numerical zero does not justify discarding its gradient.

Suppose exact nonnegative rational multipliers w satisfy

g - sum_j w_j A_j in the row span of E.

Then c1(x)=sum_j w_j (A_j.x)>=0 on every legal member of the cell. If any
w_j is positive, it is strictly positive there. This is an exact algebraic
certificate; a floating LP may suggest its support, but its status and
approximate values provide no scientific acceptance. All final equations
and multiplier signs must be checked independently over Q. The same cell
functional under a second generic ray must agree modulo the equality row
span. Such agreement is a control, not a replacement for the complete
original identity or coefficient derivation.
