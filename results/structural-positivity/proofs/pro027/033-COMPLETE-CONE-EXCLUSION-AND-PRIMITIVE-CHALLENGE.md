# Exact complete-cone exclusion and a quotient-normalization falsifier

Claims FR027-P09-T002 and F001. This proof concerns complete LOCAL cones, their realizability and the normalization of a trial correction. No negative ordinary coefficient of an entire LR polynomial is observed. The global sixth-coefficient theorem does not depend on the exclusion in this note; it retains all negative abstract cones and corrects the complete array.

## What is actually excluded

Among the102297 independent quadruples in the unreduced42-normal rank-six hive atlas,132 have negative complete transverse BV constants in the fixed standard metric. None can be the COMPLETE SIMPLICIAL codimension-four normal cone of a six-dimensional face of a full-dimensional legal six-part hive.

This statement does not exclude their occurrence as selected coactive cones or subdivision cells of a larger nonsimplicial normal cone. It does not classify the original BV weights of all complete nonsimplicial cones, and it does not make a failed sufficient correction into an LR counterexample. Hidden affine strata are covered by the separate normal-cycle theorem, not by extending this full-dimensional feasibility test beyond its hypotheses.

## Full boundary and every actual rhombus stay attached

Use28 variables: the18 boundary parts b=(lambda,mu,nu) and the10 original interior hive coordinates x. The entire45 rhombi are homogeneous forms r_i(b,x)>=0. Include all18 nonnegative-partition constraints: fifteen adjacent gaps and three last parts, and impose the trace equality. No selected boundary slice or size bound is introduced.

A genuinely full-dimensional six-part hive necessarily has all fifteen adjacent padded boundary gaps strictly positive, by the adopted zero-gap forcing identities. This is a necessary condition only; strict partitions do not by themselves prove a ten-dimensional hive. At a point in the relative interior of a six-face with a specified complete normal cone C, every row whose normal lies outside C is strictly positive. A finite positive dilation can make all those strictly positive gaps and slacks at least one simultaneously. The remaining last parts need only be nonnegative. Thus requiring these positive lower bounds in the homogeneous existence test loses no prospective realization of the stated full-dimensional type.

For a negative independent quadruple I, compute exactly

    C=pos{n_i:i in I},
    closure(I)={j:n_j is in C}.

The coefficients in the positive span are obtained with exact Gram elimination and verified by reconstructing the full normal. For each extreme generator select an actual original rhombus having that primitive direction, and impose that row to be zero. Duplicate original rows having the same direction retain their different boundary forms and are all considered. Across all132 quadruples this gives192 complete choices.

For each choice the system contains63 inequalities:18 partition conditions and45 complete original rhombi. The rhombi whose normal is in closure(I) have lower bound zero; all others have lower bound one. The five equalities are trace plus the four chosen active rows. If an actual complete simplicial cone I existed, an appropriate one of these192 systems would be feasible. Conversely, nothing about a merely selected negative cone is inferred from these stricter systems.

## Exact dual certificates, not floating infeasibility

Write one such system as A*z>=b, E*z=0. The saved certificate provides rational y>=0 and unrestricted rational v with

    A^T*y+E^T*v=0,           b^T*y=1.                    (1)

Multiplying a purported feasible point by(1) gives0>=1, an exact contradiction. Every original boundary coefficient and chart coefficient appears in(1).

DATA/J09-EXACT-FARKAS-CERTIFICATE.json.gz contains all192 complete certificates, their full original45-row roster, exact closure lists, chosen row identities and every nonzero dual multiplier. A separate verifier rebuilds the original rhombi from the canonical hive convention, recomputes each positive-span closure with exact SymPy matrices, enumerates every duplicate-row choice, checks y>=0, and verifies every coefficient of(1). DATA/J10-FARKAS-VERIFIED.json records complete132-tuple/192-choice coverage. The finite proof bodies are sufficient to replay this exclusion without the floating optimizer.

The earlier J08 optimization refusals alone had no exclusion status. J09 supplied rational identities and J10 independently checked them. The stronger current conclusion is not retrospectively assigned to the earlier floating records.

## The wrong quotient normalization changes the certificate

The successful global correction uses a ten-by-seven saturated kernel M_J for each supporting triple and

    u=primitive(M_J^T*n),

not the unnormalized vector M_J^T*n. There are210 actual incidence occurrences in the complete correction roster at which the latter vector has gcd greater than one.

Holding every correct h_J fixed but using the unnormalized vector instead produces11 negative trial-corrected local weights among the same102297 constraints. All eleven negatives and the COMPLETE wrong-value array were saved before comparing with the valid correction. For the quadruple with literal atlas IDs(0,1,34,36), the original complete constant is positive,

    alpha=31681/632016,

but the incorrect operation gives

    alpha_wrong=-936977403864679/19750500000000000.        (2)

Equation(2) is the minimum of the wrong array. The correct primitive array has minimum164999999111/491400000000000>1/3000. The failure is a local trial-certificate failure, not a negative entire LR coefficient, and not a claim that the original cone in(2) is negative.

DATA/J08-UNPRIMITIVE-CHALLENGE.json.gz preserves every raw restriction, gcd, primitive restriction and wrong corrected value; DATA/J08-UNPRIMITIVE-TRIAL-NEGATIVES.jsonl preserves the eleven observations at their actual scope. Primitive normalization is essential to the lattice-normalized face-balance identity and cannot be replaced by ambient primitivity.

## Process failure and repaired attempt

The initial J07 driver raised an exact list-versus-tuple ID error before it tested any boundary. Its source, stderr and observed failed wait are retained. It supplies no failed feasibility instance or partial scalar. J08 uses a fresh source/attempt/output identity with the ID normalization repaired. It completes the full132/192 feasibility challenge and every wrong-primitive constraint. J09 and J10 then establish and independently verify the exact exclusion certificates. All four attempts have observed worker-PID waits; no missing wait or failed scalar is relabelled successful.

The132-negative count happens to match an inherited rank-five codimension-four count. This unit has NOT proved a rank-five embedding classification of those132 literal rank-six cones. That possible structural comparison is retained as a future idea, not a theorem inferred from equal cardinalities.
