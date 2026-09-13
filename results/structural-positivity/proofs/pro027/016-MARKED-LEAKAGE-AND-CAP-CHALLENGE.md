# Marked complete leakage, a negative cap correction, and verification scope

The complete marked count in proof015 retains the actual statistic B=sum_(i<m)z_i. It is not a fugacity assigned to an unproved submodel. In the source's full row inverse, the coordinates z1=zm=0 are forced at h0; z2,...,z_(m-1), and the bank coordinate u are not discarded. The complete polynomial in q at each fixed integer stretch is

P_(m,g)(t;q)=sum_(A>=B>=0) q^B N(A,B) W_g(A,B),
N(A,B)=M(A,B)-M(A+1,B-1),
M(A,B)=[x^A y^B]h_(2t)(1,x,y)^(m-1),
W_g=(min(gt,A)-B+1)_+*(2mt-max(gt,A)+1).

N is the nonnegative complete two-row Pieri multiplicity. The source map recovers the last edge and both banks for every counted choice. Setting q=1 gives the entire parent; q=0 forces precisely B=0. For k=m-1>=2 and g>0 this is a proper coordinate face, not a whole negative realization. No claim is made that fixing arbitrary q gives a polynomial in the stretch.

At g1 the zero face has the exact all-t count

F_k(t)=(t+1)((k+2)t+1)(2t+1)^k
       -2((k+1)t+1)binom(t+k,k+1).                       (1)

Proof: at B0, N(A,0) counts k entries y_i in[0,2t] of total A. Extend the A>t weight (t+1)(2mt-A+1) over the entire box. Conditional reflection gives mean A=kt and the first term of(1). For A<=t the actual-minus-extended weight is -2(mt+1)(t-A); the upper caps are automatic. Summing (t-A)binom(A+k-1,k-1) gives binom(t+k,k+1), proving the subtraction. It is not valid to replace P by F or to infer ordinary signs of P-F from its nonnegative values.

## The cap-free continuation is false

At k3,m4,g3 the bare triple is
lambda=(30,22,20,18,16,16,8),
mu=(22,20,18,16,11,8), nu=(19,8,8).
It is balanced, rank7, outer size130, degree7, codegree2. The complete polynomial differs from the a0-only continuation of proof015 by the exact auxiliary correction

C(t)=t(t-1)(t+1)(t+2)
     *(2101t^3+3813t^2+2168t+354)/840.                    (2)

Its ordinary linear coefficient is -59/70. This is a complete cap-correction polynomial, NOT an entire ordinary LR candidate. Its full vector was written as CAP-k3-g3-high1 in NEGATIVE-AUXILIARIES.jsonl before any favorable comparison. Formula(2) is reconstructed by exact polynomial division from that preserved vector, not fitted to the displayed two sites.

Both expressions give1032 at t1. At t2 the independent literal ordinary LR row count is29748, while the false cap-free continuation gives28698. The correction is1050. Thus positive early agreement does not remove the missing individual cap. At every integer t>=2 the correction is positive, while its linear coefficient is negative. This tests the generality of the g1 theorem in the actual legal family, rather than at an artificial shifted parameter.

The full c1 remains positive by proof015's complete tent identity. No global higher-coefficient statement for all positive g follows from this single correction or the bounded positive panel.

## Numerical and implementation evidence

J02 saves43 full g1 parent vectors before comparison: k1,...,40,50,60,80. All2106 ordinary entries and all1096 entries of their binomial residuals are positive. The largest saved case is m81, ordinary rank84, outer size33856, degree161. Prior actual degree and codegree are the geometric premises of proof013, not observed numerical degrees.

J08 independently determines those same43 vectors by Newton finite differences from complete contracted integer counts. Its prior nodes are -k,...,-1 (true reciprocity zeros),0,...,k+1, giving2k+2 determining sites. Positive nodes k+2,k+3 are unused checks. All2106 coefficients agree, with86 positive unused checks. This is independent arithmetic and count-vs-formula evidence, but both count and formula use the complete contraction in proof013.

J06 supplies a genuinely different complete nonnegative counting representation: the unsigned two-row Pieri prefix recurrence with the full last-edge/bank weight, implemented in fresh C++ arbitrary-precision integers. It agrees at all63 sites for k1,2,3,5,9,19 and t0,...,k+3. These are six complete prior mixed-node determinations with12 positive unused checks, not63 different LR polynomials. J04 additionally counts16 bare ordinary LR sites from the full row/content/column/ballot inequalities, without importing the specialized bank chart. Its rank23 control k19,t1 is355652008902. The larger vectors' whole-count identity and signs rely on the all-t proofs, not a falsely claimed second-model recount at every one of43 parameters.

J07 saves173 complete general-gap records: all1<=k<=12,0<=g<=2k and the five declared larger pairs. All3270 ordinary entries are positive;12 records overlap the main g1 roster. Each is checked against the complete integer capped convolution, with two reserved positive checks and its correct prior degree/codegree; the tiny subset also has direct unsigned chart comparisons. This panel does not establish all-gap higher positivity. All595 negative auxiliary cap blocks, comprising5775 negative coefficient occurrences, were saved before parent comparisons. These are overlapping parts of the same finite calculation, not595 discoveries or LR candidates.

J03 checks the full continuant identities through k40 and502 principal minors through k8, including the preserved failed moment-minor control. J09 reconciles all raw vectors, all63 independent prefix sites and the cap challenge. It also checks48 marked histograms at k2..5 and g1,3,2k, t0..3, including exact q0-face and q1-whole specialization. The codegree strict witnesses and balanced bare triples pass1560 checks at m2..40,1<=g<=2m-2. These are finite challenges of the universal proofs, not their generality premise.

All code used in this unit is fresh or reviewed own administrative continuation code. Source, mathematical-model, implementation and arithmetic independence are distinguished. No external campaign acceptance, worldwide novelty, whole-rank theorem, full KTT, original-area-thirty increment or ordinary-negative entire LR candidate is asserted.
