# Mathematical antecedents and selected references

**Alper Ferudun's recent rank-four/five positivity work is a central
contribution to the conjecture and an indispensable input to the finite-box proof.**
The finite-box theorem uses his all-size length-at-most-five theorem as an
explicit external premise. See [arXiv: 2607.22301v2](https://arxiv.org/abs/2607.22301v2)
and the [pinned manuscript](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/paper/ktt_positivity.tex).
His normal-correction and chamber methods receive method credit as well.

The complete finite-box bibliography is supplied as
[REFERENCES.bib](results/finite-box/REFERENCES.bib), with the particular
premises explained in its readable proof. The prior lower-rank generator
reproduction limitation is documented, rather than represented as a new
verification of Ferudun's entire source theorem.

This bibliography identifies the premises and closest comparisons used here.
It is not a complete priority audit. No article, external software package or
third-party source archive is redistributed in this repository.

1. Étienne Rassart, *A polynomiality property for Littlewood–Richardson
   coefficients*, JCTA 107 (2004), 161–179.
   [arXiv: math/0308101](https://arxiv.org/abs/math/0308101).
   Stretched-LR polynomiality underlies eventual-character identities.
   The degree bounds used in these modules are independently derived.
2. Jesús A. De Loera and Bernd Sturmfels, *Algebraic Unimodular Counting*.
   [arXiv: math/0104286](https://arxiv.org/pdf/math/0104286), Theorem 1.1
   and the chamber-complex characterization. This supplies the unimodular
   chamber-polynomial premise for the A3 certificates; the relevant matrix
   minors and complete seven-cone refinement are explicitly checked here.
3. Tyrrell B. McAllister, *Degrees of stretched Kostka coefficients*.
   [arXiv: math/0603173](https://arxiv.org/abs/math/0603173).
   Degree/polyhedral context. The new root-cone degree 31 proof also follows
   from its prior growth bound and independently positive leading terms.
4. Per Alexandersson, *Fast computation of Ehrhart polynomials of
   Gelfand–Tsetlin polytopes via Macdonald reciprocity*.
   [arXiv: 2605.22378v2](https://arxiv.org/html/2605.22378v2).
   Weighted/skew GT models, horizontal-strip methods, reciprocity and
   Kostka-to-LR embeddings are antecedents, not inventions claimed here.
5. King–Tollu–Toumazet, *The hive model and the factorisation of Kostka
   coefficients*, SLC 54A (2006), B54Ah, page 8 equation (4.1).
   [Article](https://emis.de/ft/13885). Its example
   K_(t(3,2),t(1^5))=(t+1)(t^2+2t+2)/2 already has nonreal roots -1±i.
   Our root theorems concern positive real part, a different and stronger
   failure of root location.
6. Alper Ferudun, *Positivity of stretched Littlewood–Richardson coefficients
   for partitions of length at most five*, manuscript at GitHub commit
   c3a0795bd287dcca78fac2cc6ba4282144bb7813, 5 September 2026.
   [Pinned manuscript](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/paper/ktt_positivity.tex).
   This revision supplies the length-five extension. Independent verification
   checked its new linear certificate, cone completeness and
   transfer argument; earlier coefficient results remain source dependencies.
7. Ferudun, *General KTT proof status*, Hurwitz discussion at lines 172–177.
   [Pinned note](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/proof/GENERAL_KTT_PROOF_STATUS.md).
   The note already considers the stronger global Hurwitz possibility but
   supplies no uniform proof or refutation. This prior discussion is credited;
   our result is not presented as originating that question or solving KTT.
8. Luis Ferroni and Daniel McGinnis, *Lattice points in slices of prisms*.
   [arXiv: 2202.11808](https://arxiv.org/pdf/2202.11808), Theorems 1.1–1.2.
   Integral prism-slice Ehrhart positivity covers relevant disjoint-row cases.
   The overlapping two-row formula subtracts two shifted slices and needs its
   own argument. Absence of an equivalent theorem in this bounded comparison
   does not establish novelty.

Weyl's character formula, Schur/Pieri/Jacobi–Trudi identities, Ehrhart–Macdonald
reciprocity, Routh root counting and Rouché's theorem are classical tools.
The proofs specify where they enter and verify the instance-specific hypotheses.
The rank-eighteen example, root-cone and coefficient-geometry results were
proposed with GPT 6 Pro assistance; independent implementation and verification were
performed with Codex. [PROVENANCE.md](PROVENANCE.md) explains the distinction
between mathematical independence and human peer review.

Additional antecedents for the new structural results include:

- Thawinrak's 2025 dissertation, section 3.4, already gives the relevant
  M=s=1 LR specialization of the Chan–Robbins–Yuen flow family. The general
  stable map and its domain must be compared with that prior specialization;
  the CRY connection itself is not a new discovery claimed here. The exact
  source is listed in the finite-box bibliography.
- Christian Haase, Martina Juhnke-Kubitzke, Raman Sanyal and Thorsten Theobald,
  [*Mixed Ehrhart polynomials*](https://www.math.uni-frankfurt.de/~theobald/publications/mixedehrhart1.pdf),
  Theorem 2.1, for the Bernstein–McMullen multivariate counting premise.
- Károly J. Böröczky and Monika Ludwig,
  [*Minkowski valuations on lattice polytopes*](https://dmg.tuwien.ac.at/ludwig/lattice.pdf),
  Theorem 22 and Corollary 23, for the additivity of the linear Ehrhart
  coefficient. The authors credit Raman Sanyal for the observation and proof.
  That additivity is an established input to the transport argument.

The [posted FrontierMath problem](https://epoch.ai/frontiermath/open-problems/stretched-lr-coefficients)
defines the finite bounds addressed by the box theorem. Epoch's
[FAQ](https://epoch.ai/frontiermath/open-problems/about/faq) says that it cannot
adjudicate nonexistence claims and relies on the mathematical community.
The computational verification recorded here is separate from mathematical
community acceptance or an institutional determination.

## Exact source locations and flow antecedents

[REFERENCE-NOTES.md](REFERENCE-NOTES.md) records the theorem and page locations
checked for the premises above. In particular, Derksen–Weyman Corollary 3
(printed p. 256), Rassart Theorem 4.1 (preprint p. 10), Ressayre Theorem 5
and equation (16) (p. 9), and Beck–Develin Theorem 5 (p. 8) supply the
polynomiality, chamber, factorization and rational-reciprocity statements.

Karola Mészáros and Alejandro H. Morales, [*Volumes and Ehrhart polynomials of flow polytopes*](https://arxiv.org/abs/1710.00701),
Compositio Mathematica 155 (2019), 1270–1291, section 1.2, case II(a),
identify the complete-graph source–sink flow family as the Chan–Robbins–Yuen
polytope. Thawinrak’s dissertation section 3.4 (printed pp. 41–42) already
gives its stated LR polynomial specialization. The more general stable
affine integer map and interior theorem in this collection have their own
proofs; the CRY connection itself is prior work.

Thawinrak’s short polynomiality proof also appeared in *Ars Combinatoria*
162 (2025), 205–212, [DOI: 10.61091/ars162-15](https://doi.org/10.61091/ars162-15).
This metadata update does not replace Derksen–Weyman’s earlier theorem.

## Rank-six coefficient update

Ferudun's length-five theorem is available in
[version 2 of the preprint](https://arxiv.org/abs/2607.22301v2), dated
5 September 2026, and at the pinned source revision
[c3a0795](https://github.com/AlperTheKing/ktt-positivity/tree/c3a0795bd287dcca78fac2cc6ba4282144bb7813).
The new [rank-six entry](results/rank-six-coefficients/README.md) states its
additional c4/c5 scope, the exact use of prior results, and a
[bounded novelty assessment](results/rank-six-coefficients/NOVELTY.md).

## Sources used in the new whole-family note

- Nicole Berline and Michele Vergne, [Local Euler-Maclaurin formula for polytopes](https://arxiv.org/abs/math/0507256): the local valuation and analytic recurrence.
- Christian Haase, Martina Juhnke-Kubitzke, Raman Sanyal and Thorsten Theobald, [Mixed Ehrhart polynomials](https://arxiv.org/abs/1509.02254): the classical Bernstein-McMullen multivariate polynomiality statement used in the complete quotient proof.
- Stefan Trandafir, [External Columns and Chambers of Vector Partition Functions](https://link.springer.com/article/10.1007/s00454-025-00762-1): precise matrix/chamber/saturation hypotheses and the separate LR example/future-work scope.

These references support the named premises and comparison. The new finite normal fields are supplied with their own complete verification, and the [novelty note](results/transport-capped/NOVELTY.md) keeps the literature check bounded.
