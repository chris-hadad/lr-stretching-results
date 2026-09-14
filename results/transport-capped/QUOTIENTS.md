# Entire stabilized quotients of the positive families

Let b and a be feasible integral parameters in either the complete 3-by-5 transportation family or the four-capacity family of the [whole theorem](../../tooling/transport_certificates/PROOF.md). The entire direction polytope Q=P_a has actual dimension r>=1. Both parameter cones are closed under addition and use the original integer coordinate lattices Z^8 or Z^7.

## Complete stabilization

For each independent full basis of the fixed inequality matrix, its possible vertex at b+s*a is affine in s. Every original-row slack is also affine. Choose an integer S>=1 strictly beyond every nonnegative root of every nonconstant slack. The feasible basis set is then fixed for s>=S, including zero slacks and hidden affine strata. The slope of every eventual vertex satisfies every original direction inequality, so it belongs to the entire Q. Thus every vertex of P_(b+(S+u)a) belongs to P_(b+Sa)+u*Q. The reverse inclusion follows by adding all original inequalities. Hence the whole Minkowski identity holds for every real u>=0.

For transportation there is a smaller complete way to compute S. Every independent full vertex support extends to a spanning tree in the complete bipartite incidence graph. Removing any tree edge makes its coordinate a signed row-subset-minus-column-subset margin. It is therefore sufficient to retain ALL subset differences, including empty/full pairs, and choose S strictly beyond every nonnegative root of their nonconstant affine functions. This is a proof of the complete basis condition, not a sampled chamber test.

## Polynomial count and full quotient lattice

Choose an integer point z of Q, translate to Q-z, and put W=lin(Q-z). Project the ENTIRE P=P_(b+Sa) to K in the saturated quotient lattice Z^D/(Z^D intersect W). The quotient dimension is dim P-r. No initially empty integer fiber is omitted.

Because P and Q-z are integral, the Bernstein-McMullen multivariate Ehrhart theorem gives a polynomial F(x,y)=#((x*P+y*(Q-z)) intersect Z^D) for every nonnegative integer x,y, including both axes, with y-degree at most r. Thus the whole parent count at stretch t is F(t,u*t), and its u^r coefficient is divisible by t^r.

For a fixed positive integer t and each lattice point in t*K, choose an integer lift. Its initial nonempty real fiber may have no lattice point. Adding u*t*(Q-z) gives leading lattice-count growth u^r*t^r*V, where V is the normalized r-volume of Q. A translated-body lower bound and a bounded-thickening upper bound have the same leading term, including for such initially empty integer fibers. Summing all finitely many quotient lattice points proves

    [u^r] E_(b+(S+u)a)(t)=V*t^r*E_K(t),
    Delta_u^r E_(b+(S+u)a)(t)=r!*V*t^r*E_K(t).

The quotient count is therefore polynomial for positive integers t. Clearing K's vertex denominators and comparing with the resulting integral Ehrhart polynomial proves its constant is one and its degree is dim K.

## Positive coefficients, without losing the initial parents

Expose any actual j-face G of K by a quotient functional and pull it back. Its lifted parent face is F_G(0)+u*(Q-z), with dimension r+j. The direction lattices form the exact saturated sequence

    0 -> Z^D intersect W -> Z^D intersect lin(F_G-F_G)
      -> quotient lattice intersect lin(G-G) -> 0.

It admits an integral splitting. Normalized volume disintegrates with these measures, and division by u^r gives the limit V*vol_Z(G). Apply the complete parent face-volume bound at index r+j, keep ALL lifted j-faces, and take integral u to infinity. Division by V gives

    [t^j] E_K(t)>=epsilon*sum_(actual j-faces G) vol_Z(G)>0,

with epsilon=1/1000000 for transportation and 1/300 for capped families. Every positive quotient index is protected, including for r=1 and r=2. A point quotient has polynomial one. The whole-family theorem separately protects every initial/intermediate parent, because each remains in the same complete parameter family. No claim follows for a base outside these families.

Use the fixed-pad linear whole-LR constructors to obtain the corresponding LR parent family. Its parent and direction polynomials equal the table/cap polynomials at every stretch and parameter, so the normalized leading volumes and direction dimensions agree. The general fixed-rank hive stabilization gives the same quotient identity eventually; equality of the entire parameter polynomials identifies the quotient COUNT polynomials on both sides. This is not a geometric isomorphism assertion, and no ordinary LR rank is assigned to K.

## Exact examples

For base rows (2,2,2), columns (2,1,1,1,1), the direction rows (1,1,0), columns (1,1,0,0,0) is a primitive segment. Its polynomial is 1+t. The complete 256-cut scan gives S=2. In the eight free coordinates its primitive direction is (1,-1,0,0,-1,1,0,0), with a unit coordinate giving a saturated quotient section. Its quotient is

    1+(115/21)t+(4579/360)t^2+(11617/720)t^3
      +(433/36)t^4+(379/72)t^5+(451/360)t^6+(631/5040)t^7.

For the same base, direction rows (2,1,0), columns (1,1,1,0,0) is an entire integral two-simplex with polynomial binom(t+2,2) and V=1/2. Its generators (-1,0,1,0,1,0,-1,0) and (0,-1,1,0,0,1,-1,0) have a minus-identity coordinate block, proving saturation. The complete cut scan gives S=3. Its quotient is

    1+(31/6)t+(385/36)t^2+(91/8)t^3
      +(473/72)t^4+(47/24)t^5+(17/72)t^6.

The full parent vectors, two unused parameter values in each determining space and direct independent count checks are represented in examples.json. The companion reproduction command rebuilds the whole vectors and finite differences. These controls support the full proof; their positivity is not its universal quantifier.

The classical multivariate theorem is stated in Haase, Juhnke-Kubitzke, Sanyal and Theobald, [Mixed Ehrhart polynomials](https://arxiv.org/abs/1509.02254). Whole stabilization and the full saturated-fiber argument retain their separate hypotheses as proved above. General rank-six low-dimensional quotients outside these families remain open.

The quantitative quotient face-volume margins above concern the original table/cap quotient. The whole-LR consequence uses equality of polynomial counts to transfer positivity; it does not transfer that margin to a potentially different collection of LR quotient faces.
