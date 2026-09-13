# An independent grouped-Schur count

Derivation dated 10 September 2026. This provides a second entire count model
for the fixed three-matrix rectangular family. It uses positive Schur branching
to perform the row-group projection, with no weighted-table row alternant.
The representation-theoretic identification and implementation checks are
separate verification requirements.

Set p = 4, q = 5, m = 3 and entry degree N = pqt. The Cauchy decomposition
of Sym(C^p tensor (C^q tensor C^m)) gives

    direct_sum_(lambda) S_lambda(C^p) tensor S_lambda(C^q tensor C^m).

The only SL_p-trivial summand at degree N has lambda = ((qt)^p), with
multiplicity one on the first factor. Thus the remaining column character is

    s_((qt)^p)(y1,y1,y1, y2,y2,y2, ..., yq,yq,yq).

Taking the determinant character det^(pt) on GL_q via its complete Weyl
denominator gives

    P(t) = sum_(tau in S_q) sign(tau) F(R, c(tau)),
    R = ((qt)^p),  c_j(tau) = pt + j - tau(j).                  (1)

Negative c_j give zero. F(R,c) is the number of semistandard tableaux of shape
R in q consecutive groups of three letters, with total content c_j in group j.
There is no restriction on the three individual contents within each group.
The Schur character is symmetric in the y_j, so sorted group totals may be
combined with their signed multiplicities. This retains the entire column
alternant and every tableau.

The complete positive branching recursion is

    F(lambda,(c1,...,ck)) = sum_mu s_(lambda/mu)(1,1,1)
                                      F(mu,(c1,...,c_(k-1))),

where mu ranges over every partition contained in lambda with size
c1 + ... + c_(k-1). The final group occupies precisely lambda/mu. Its
semistandard filling count is the exact Jacobi-Trudi determinant

    s_(lambda/mu)(1,1,1)
      = det_(i,j) h_(lambda_i-mu_j-i+j)(1,1,1),
    h_k(1,1,1) = binom(k+2,2) for k >= 0, and zero for k < 0.

Pad mu with zeros to the fixed p-row shape. A skew column of height greater
than three gives zero, equivalently lambda_(i+3) > mu_i for some valid i.
This is an exact early zero test. For one group the same determinant uses
mu = 0. For no groups the empty shape contributes one and all other shapes
zero. At t = 0 the full count is one.

The source tableau_count_v1.py enumerates precisely these subpartitions,
evaluates the integer determinants by fraction-free elimination, and caches
only within one scalar call. The integer division in elimination is checked.
Every positive branching and determinant count is nonnegative before the
final column alternant. Its work ceiling gives an incomplete result, never a
zero or a partially computed signed sum.

This second model counts grouped semistandard tableaux; the first counts
weighted nonnegative transportation tables and applies both Weyl alternants.
They share the whole representation-theoretic identification, but have distinct
count objects and elimination algorithms. Native bare LR checks remain a
third, more expensive route; their timeout does not invalidate either formula.
The exact determining space and unused positive holds are those proved in
[the primitive-family premises](rectangular-premises.md). They are applied only after these all-grade identities.
