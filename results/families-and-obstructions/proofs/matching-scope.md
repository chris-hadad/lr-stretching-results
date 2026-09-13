# Limits of sufficient positivity criteria for matching families

No negative expression in this note is an ordinary-negative entire LR example. The complete parent and the chosen sufficient certificate remain different objects.

## 1. A tempting universal residual lemma is false

The initial trial proposed extending the source first-coefficient criterion for negative-real-rooted h to coefficient positivity of the factored residual. It fails even for

    h(z)=(1+28z)^4, d=43, s=4,
    d-s-(h1+s)/3=1/3>0.

After removing the positive factor product_(j=1)^39(t+j)/43!, the EXACT residual is

    2961840+3622390t+4308443t^2-48778t^3+707281t^4.

The negative cubic disproves the proposed residual implication. The full polynomial in this test had no negative ordinary coefficient; this formal numerator has no assigned LR realization. The correct base theorem in [the shift-difference proof](matching-positive-shifts.md) uses a stronger explicit dimension condition, not just the source c1 criterion. The residual diagnostic record preserves this and two further examples, along
with 81 complete matching residuals. Those finite positive residuals are not an all-q,r theorem.

## 2. The first two-chain positive cone is not universal

With H_(u,v)(z)=sum_k binom(u,k)binom(v,k)z^k, the inherited ordinal-sum theorem motivates

    h(z)=sum_(j=0)^s alpha_j(1-z)^j H_(s-j,d-s-j)(z),
    s=deg h.

Every nonnegative alpha_j would yield a positive ordinary polynomial at this degree. The expansion is uniquely triangular at z=1. Actual matching h_(11,11), d=220, s=23, has a negative alpha_2. The two-chain comparison record includes other failures, including (10,13). This is a certificate nonmembership, not an LR sign. The exact rational coefficient arrays are preserved.

The balanced-cone comparison checks eighteen expansions across six fixed parameter pairs. Choosing the balanced U=floor(d/2) repairs all six pairs, while several unbalanced choices remain failures, explicitly recorded. No uniform balanced-cone membership proof has been established, and no claim of a full parameter census is made. The balanced representation remains an open alternative; failure of an
unbalanced cone does not exclude it.

## 3. Negative first multipliers are essential, and compensation repairs them

In the exact q=2 shift identity, the constant coefficient of Bop is

    b_0=-(50r^2-95r+128)/(375(6r+19))<0.

Its quadratic numerator has negative discriminant and positive leading coefficient. For q=3, both b_0 and b_1 are negative throughout r>=3. Thus the direct claim that A and Bop separately have nonnegative coefficients is false. Dropping these terms changes the complete count.

The shift-difference proof's exact W absorbs these negative multipliers. The earlier matching-layer proof's C coefficients, including every compensation term, are strictly positive for all r>=q at q=1,2,3. The conclusion follows from an exact compensation identity, not from finite
sampling or pointwise count positivity.

## 4. A genuine next-layer obstruction to THIS compensated certificate

Applying exactly the same construction to q=4 gives the full rational shift identity, verified by an independent symbolic checker. All coefficients of A-1 remain positive on r>=4, but the resulting constant coefficient of C is

 C_0(r)=-[57624r^6-779444862r^5-12457839282r^4
              -79524503555r^3-253524288721r^2
              -403669081503r-256812354981]
          /[941192(r+3)(4r+13)(8r+25)(8r+27)].

In particular

    lim_(r->infinity) C_0(r)/r^2=-3/12544,
    C_0(1000000)=
      -18948180893360397747640102536553894881673
       /80316074688455620528179594959800 <0.

These are coefficients of a multiplier in a SUFFICIENT decomposition, not coefficients of P_(4,r). The source all-q,r linear coefficient theorem still proves [t]P_(4,r)>0 at every such r. No high-degree parent vector was computed at r=1000000, and no negative whole-LR observation follows. This example rules out simply announcing that this exact one-step certificate works for every q.

An all-q identity with a richer compensated-difference basis, or
coefficient-specific bounds retaining the surplus in W, could extend this
criterion. A different baseline, uniform balanced two-chain membership, and
other complete couplings remain open alternatives.

## 5. Exact whole controls and independence

The complete-vector check derives six ordinary vectors directly from the all-t numerator identity, at

    (q,r)=(1,2),(1,5),(2,2),(2,4),(3,3),(3,5),
    degrees 25,40,31,43,44,58.

Every coefficient is positive; every computed P-G difference is coefficient-nonnegative. Complete unsimplified mixed-interval flow counts independently agree at t=0,1,2,3 for all six, yielding 24 scalar agreements. Two additional sites d+1,d+2 per vector verify the full algebraic expansion against the same generating series; they are NOT independent flow counts or holdouts from a fit, because no fitting occurred. Full G, Omega, W arrays are retained too.

The direct tableau check counts literal LR tableaux, with row weak order, column strict order, exact content and lattice-word inequalities, at t=1,2 for (1,2),(2,2),(3,3). All six scalar values agree: 39,740; 53,1350; 85,3447. These are complete scalar counts, not a second high-degree reconstruction.

The whole source character identity, complete composition formula and exact symbolic identities prove the all-t result; a larger finite count panel is not its logical basis. The symbolic derivation and an independent checker verify the symbolic rational identities, clearing every coefficient in r and z with different implementations. Both ultimately use CPython exact integers/Fractions; SymPy uses that installed arithmetic stack here. This is not verification by an independent arithmetic engine.

## 6. Computational and source limitations

Eleven computational attempts are recorded: ten completed successfully. The
attempt identified as `J04` failed while serializing a SymPy BooleanTrue after
its initial symbolic calculation and before exporting a result, so it supplies
no exported mathematical certificate. The corrected attempt `J05` reran all
three identities. Missing process records for the earlier gap-two computation
remain a separate provenance limitation.

Scripts, inputs and listed data/dependency identities were recorded before
calculation. The execution script preceded `J01`, but its separate hash was
recorded afterward. The records identify the installed SymPy `__init__` source,
not its entire installed source tree.

Public primary-source searches on generic real-rooted/Ehrhart and matching/Legendre connections returned only background leads; no external theorem from those search results is used by the new proof. The residual recurrence, positive difference, symbolic membership and exact q4 obstruction are derived here. The source-only alternate Laguerre argument remains at its inherited status and is not established here as an independently verified universal analytic proof.

No ordinary-negative whole-LR example, additive-box increment, whole-rank positivity, full KTT proof, or original-box exhaustion is established. Positivity or negativity outside the three-layer domain requires separate
arguments; the later fourth- and fifth-layer results are given in
[the second-shift proof](matching-layers.md).
