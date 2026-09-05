# Mathematical antecedents and selected references

This bibliography identifies the premises and closest comparisons used here.
It is not a complete priority audit. No article, external software package or
third-party source archive is redistributed in this repository.

1. Étienne Rassart, *A polynomiality property for Littlewood–Richardson
   coefficients*, JCTA107 (2004),161–179.
   [arXiv:math/0308101](https://arxiv.org/abs/math/0308101).
   Stretched-LR polynomiality underlies eventual-character identities.
   The degree bounds used in these modules are independently derived.
2. Jesús A. De Loera and Bernd Sturmfels, *Algebraic Unimodular Counting*.
   [arXiv:math/0104286](https://arxiv.org/pdf/math/0104286), Theorem1.1
   and the chamber-complex characterization. This supplies the unimodular
   chamber-polynomial premise for the A3 certificates; the relevant matrix
   minors and complete seven-cone refinement are explicitly checked here.
3. Tyrrell B. McAllister, *Degrees of stretched Kostka coefficients*.
   [arXiv:math/0603173](https://arxiv.org/abs/math/0603173).
   Degree/polyhedral context. The new root-cone degree31 proof also follows
   from its prior growth bound and independently positive leading terms.
4. Per Alexandersson, *Fast computation of Ehrhart polynomials of
   Gelfand–Tsetlin polytopes via Macdonald reciprocity*.
   [arXiv:2605.22378v2](https://arxiv.org/html/2605.22378v2).
   Weighted/skew GT models, horizontal-strip methods, reciprocity and
   Kostka-to-LR embeddings are antecedents, not inventions claimed here.
5. King–Tollu–Toumazet, *The hive model and the factorisation of Kostka
   coefficients*, SLC54A (2006),B54Ah, page8 equation(4.1).
   [Article](https://emis.de/ft/13885). Its example
   K_(t(3,2),t(1^5))=(t+1)(t^2+2t+2)/2 already has nonreal roots -1±i.
   Our root theorems concern positive real part, a different and stronger
   failure of root location.
6. Alper Ferudun, *Positivity of stretched Littlewood–Richardson coefficients
   for partitions of length at most five*, manuscript at GitHub commit
   c3a0795bd287dcca78fac2cc6ba4282144bb7813, 5 September2026.
   [Pinned manuscript](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/paper/ktt_positivity.tex).
   Cite this revision for the length-five extension. The research program
   independently checked its new linear certificate, cone completeness and
   transfer argument; earlier coefficient results remain source dependencies.
7. Ferudun, *General KTT proof status*, Hurwitz discussion at lines172–177.
   [Pinned note](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/proof/GENERAL_KTT_PROOF_STATUS.md).
   The note already considers the stronger global Hurwitz possibility but
   supplies no uniform proof or refutation. This prior discussion is credited;
   our result is not presented as originating that question or solving KTT.
8. Luis Ferroni and Daniel McGinnis, *Lattice points in slices of prisms*.
   [arXiv:2202.11808](https://arxiv.org/pdf/2202.11808), Theorems1.1–1.2.
   Integral prism-slice Ehrhart positivity covers relevant disjoint-row cases.
   The overlapping two-row formula subtracts two shifted slices and needs its
   own argument. Absence of an equivalent theorem in this bounded comparison
   does not establish novelty.

Weyl's character formula, Schur/Pieri/Jacobi–Trudi identities, Ehrhart–Macdonald
reciprocity, Routh root counting and Rouché's theorem are classical tools.
The proofs specify where they enter and verify the instance-specific hypotheses.
The isolated R18 result and the three subsequent research returns originated
in GPT 6 Pro explorations; independent implementation and verification were
performed with Codex. [PROVENANCE.md](PROVENANCE.md) explains the distinction
between mathematical independence and human peer review.
