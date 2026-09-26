# Sharp all-rank area bound and rational cover

The [cap and factorization proof](CAP-PROOF.md) supplies the exact whole-count
premise. The following accepted root argument sharpens its all-rank size bound.

## Statement

Let n >= 2, put m = n - 1, and let P_0 = P_n = 0 and P_i >= 0 be the
prefixes of mu + nu - lambda. Set H = max P_i. For H > 0, the gap-capped
whole-polynomial representative obeys

    |lambda_capped| <= 2 floor(n^2 / 2) H.

The bound is sharp among legal cap images. Its normalization by H lies in a
union of at most (n - 1) F_(n+1) explicitly defined closed rational polyhedra,
where F_1 = F_2 = 1. Each has 8(n - 1) inequalities, one maximum-prefix
equality, and at most 3n - 4 free coordinates. The n = 6 case is 36H and 65
pieces, exactly the provider result. Every rational denominator remains
admissible. This proves no finite integer cutoff, positivity or rank reduction.

## Proof of the sharp area bound

The cap gives T_i = max(P_i, 2P_i - P_(i-1) - P_(i+1)) and inner gaps at most
T_i. Balance therefore gives outer area at most 2 sum i T_i. After dividing
by H, the function sum i T_i is convex on the full cube [0,1]^m: every T_i
is the maximum of two linear functions and every weight i is positive. Its
maximum is attained at a binary cube vertex.

At such a vertex, T_i is zero where P_i = 0, two at an isolated one, and one
at every site in a consecutive block of at least two ones. A singleton block
contributes twice its index. In any longer block, choose whichever parity
class has the larger sum of indices. Twice that sum is at least the block's
total contribution. The chosen indices over all blocks form an independent
set of the m-vertex path, since distinct blocks have at least one zero between
them. Consequently sum i T_i is at most twice the maximum weight of an
independent set for the path with vertex weights 1, 2, ..., m.

That maximum W_m satisfies W_0 = 0, W_1 = 1 and
W_m = max(W_(m-1), m + W_(m-2)). Induction gives W_(2k) = k(k+1) and
W_(2k+1) = (k+1)^2. Thus 2W_(n-1) = floor(n^2/2). Alternating ones whose
last one is at m attain the bound, because every one is isolated. Multiplying
back by 2H proves the displayed area inequality.

For sharpness, take P_i = H on that independent set and zero elsewhere, and
set both inner gaps equal to T_i. The cap reconstruction is legal: the outer
gap is 2T_i - d_i >= 0 since T_i >= d_i and T_i >= 0, and its last part is
P_(n-1) = H. Its total area equals 2 sum i T_i. The intermediate zero-prefix
cuts make these extremizers factorized terminals when n >= 3; they do not
provide new hard sign examples.

## Proof of the cover bound

Strict peaks satisfy P_i > P_(i-1) + P_(i+1), so adjacent strict peaks are
impossible. Independent subsets of an m-vertex path number F_(m+2). For each
such set and each of m possible maximum-prefix indices, take the closed
branch inequalities d_i >= P_i on peaks and d_i <= P_i otherwise; equality
ties can be assigned to the nonpeak side. Retain 0 <= P_i <= 1, each inner
gap between zero and its selected T_i, and their sum at least d_i. These
are eight inequalities per index, plus P_k = 1. They form a complete bounded
cover of normalized cap images. Empty or overlapping pieces are allowed;
no count of nonempty pieces or LR coefficient chambers is claimed.

A negative prefix gives the zero polynomial. H = 0 gives the Cartan polynomial
one by repeated zero-prefix factorization. For H > 0, the unchanged all-t
count and denominator-clearing homogeneity transfer every ordinary coefficient
sign to the full rational normalized cover. Neither compactness nor the
quadratic area bound bounds the denominators. Arbitrarily large rank remains
an independent general-KTT obligation.
