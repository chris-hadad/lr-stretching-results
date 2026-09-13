# Precise locations in the prior literature

Primary-source statements checked 13 September 2026. These notes identify
the premises and closest comparisons used in the exposition, with theorem
and page locations. The bibliography is selective; it does not establish
priority for every component of the work. [REFERENCES.md](REFERENCES.md) supplies the main bibliography.


### Ferudun: exact adopted theorem and current paper

The [current arXiv record](https://arxiv.org/abs/2607.22301) still identifies v2,
revised 5 September 2026. In [v2](https://arxiv.org/html/2607.22301v2), Theorem 2
states coefficientwise nonnegativity for all balanced triples of length at
most five. Theorems 5–7 separate the full-dimensional five-part inputs, linear
coefficient certificate and closed-chamber transfer. Theorem 4 protects the top
four coefficients of full-dimensional hives. It does not directly state top
four actual-coefficient positivity for arbitrary degenerate hives.

The [adopted manuscript at c3a0795bd287dcca78fac2cc6ba4282144bb7813](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/paper/ktt_positivity.tex)
contains the same main and transfer statements under labels `thm:main` and
`thm:transfer`. That manuscript uses nu as outer; this repository uses lambda. The Git
revision and arXiv v2 identify the sources consulted; their file formats have
not been compared byte for byte. The earlier coefficient theorems remain
external dependencies, and their codimension-four generators have not been
independently regenerated here. Ferudun's normal-correction and transfer
methods are also antecedents to the arguments in this collection.

The [pinned general-status note](https://github.com/AlperTheKing/ktt-positivity/blob/c3a0795bd287dcca78fac2cc6ba4282144bb7813/proof/GENERAL_KTT_PROOF_STATUS.md),
item 6, discusses Hurwitz stability as a stronger possible route without
proving or refuting it. Its earlier discussion predates the length-five theorem. The section
heading identifies the passage independently of rendered line numbering.

### Alexandersson: reciprocity and computation antecedents

The [current record](https://arxiv.org/abs/2605.22378) identifies v2, revised
28 May 2026. In [the paper](https://arxiv.org/html/2605.22378v2), section 1 gives
the skew-Kostka-to-LR disjoint-shape embedding; sections 2.1–2.3 give reciprocity
and strictness only for inequalities not forced on the affine hull; section 3,
Algorithm 1, selects positive/negative evaluation sites and interpolates;
section 4 describes horizontal-strip dynamic programming. These are direct
antecedents to the publication's counting strategy. The finite proof's
one-unknown sign bounds need their own argument; they are not asserted by this
paper. The mathematical citation is separate from the source versions and
executions recorded for the verification programs.

### Thawinrak and the CRY family

Warut Thawinrak's [2025 UC Davis dissertation](https://escholarship.org/content/qt59t710m1/qt59t710m1_noSplash_b1df85b1cb34ea4306c3d40eb1397754.pdf),
*On the Faces and Ehrhart Polynomials of Polytopes*, section 3.4, printed
pages 41–42 (PDF pages 50–51), explicitly states the CRY polynomial equality
for inner partitions `(k-1,k-2,...,1)` and outer partition
`(2k-3,2(k-2),2(k-3),...,2,1)`. This is the accepted stable family's
`M = s = 1` specialization after padding. The passage states polynomial
agreement; it does not provide the general `M >= s >= 0` affine integer
equivalence or its complete interior-generation transfer. Those stronger
claims keep their own proof and bounded novelty language. Its Conjecture 3.4.2
credits Morales for CRY Ehrhart positivity.

Mészáros–Morales, [*Volumes and Ehrhart polynomials of flow polytopes*](https://arxiv.org/pdf/1710.00701),
section 1.2, case II(a), printed page 3, identifies the complete-graph netflow
`(1,0,...,0,-1)` as CRY; equation (1.7) credits the Catalan-product volume
formula and its earlier proof. Its reference [7] is Chan–Robbins–Yuen,
*On the volume of a certain polytope*, Experimental Mathematics 9(1) (2000),
91–99. This source gives a direct flow antecedent beyond the dissertation.
Neither a volume formula nor a general flow formula settles every ordinary
LR coefficient sign.

### Classical inputs

| Input | Exact source location checked | Supported statement and boundary |
|---|---|---|
| Stretching polynomiality | Derksen–Weyman, *On the Littlewood–Richardson polynomials*, [author-hosted paper](https://bpb-us-e1.wpmucdn.com/sites.northeastern.edu/dist/7/497/files/2020/12/A.I.a.13.pdf), Corollary 3, printed p. 256 | The stretched LR count is polynomial. This does not assert integral hive vertices or ordinary-coefficient positivity. The zero positive-stretch polynomial and isolated zero-stretch LR coefficient have the separate conventions stated in the proof. |
| Closed chamber polynomiality | Rassart, [arXiv math/0308101](https://arxiv.org/pdf/math/0308101), Theorem 4.1, preprint p. 10; Proposition 3.3 and following paragraph, p. 9 | LR coefficients are polynomial on the cones of the stated chamber complex. The nearby arrangement-interior statement is distinct, and the text explicitly discusses the discontinuity on crossing outside support. It does not assert continuity of arbitrary count functions outside their support. |
| Vector partition chambers | Sturmfels, [*On vector partition functions*](https://sites.math.washington.edu/~billey/classes/lie/bulletins/sturmfels.1995.pdf), Theorem 1, p. 304; unimodular remark, p. 305 | Chamber formulas apply to lattice points in the support chamber; unimodularity removes residue corrections. An exterior region is not a closed support chamber. |
| Unimodular counting | De Loera–Sturmfels, [*Algebraic Unimodular Counting*](https://arxiv.org/pdf/math/0104286), Theorem 1.1, p. 1; boundary discussion, p. 10 | Chamber polynomiality assumes the declared unimodular matrix and finite fibers. The paper explains lower-dimensional chamber handling. The instance-specific matrix and complete chamber refinement require the certificates supplied with the corresponding result. |
| Honeycomb model and saturation | Knutson–Tao, [arXiv math/9807160v4](https://arxiv.org/pdf/math/9807160v4), saturation corollary, pp. 29–30; Appendix 1, Theorem 4, p. 32 | Lattice honeycombs give the invariant multiplicity, and a positive stretched multiplicity implies positivity at grade one. Saturation does not make every vertex integral. |
| Explicit LR–hive map | Pak–Vallejo, [sections 3–4 and 6](https://arxiv.org/html/math/0407170), Lemma 3.1, Theorem 4.1 and Corollary 4.2 | The LR-triangle/hive correspondence preserves complete fibers; section 6 gives a determinant-one map and integer inverse. This correspondence is an antecedent to the coordinate constructions used here. |
| Essential Horn facets | Knutson–Tao–Woodward, [arXiv math/0107011](https://arxiv.org/pdf/math/0107011), Theorems 2–3 and the section 6 synthesis, pp. 24–25 | Puzzle inequalities supply the cone's facets and multiplicity-one structure. This does not make every partition wall a factorization terminal. |
| Whole-count Horn factorization | Ressayre, [*Reductions for branching coefficients*](https://math.univ-lyon1.fr/~ressayre/PDFs/reduction.pdf), section 4.1, Theorem 5, equation (16), p. 9 | The invariant-form selected/complementary product assumes the point-class intersection condition (14) and balance equality (15). The following example rejects replacing multiplicity one by a larger intersection number. Publication's feasible-parent qualification and explicit conversion to outer-partition conventions are retained. |
| BV local formula | Berline–Vergne, [arXiv math/0507256v3](https://arxiv.org/html/math/0507256v3), Propositions 12–14, Definition 22, Corollary 23 and Theorem 26 | Quotient-space construction, lattice-isometry invariance, orthogonal products, solid normal-cone subdivision and the full face integral formula. These properties retain the scalar product and quotient lattices. General integral coordinate changes are not automatically BV isometries; period-one rational transport requires the stated dilation argument. Numbering is explicitly v3. |
| Normal-cone refinement | Castillo–Liu, [arXiv 1509.07884](https://arxiv.org/pdf/1509.07884), Lemma 3.3, p. 9; section 3.3, p. 10 | Under the stated fan refinement, BV weights add across the full normal-cone subdivision. The quotient lattice is the projected integer lattice. This supports the presentation; it does not establish that a supplied cone roster is exhaustive. |
| Ehrhart–Macdonald reciprocity | Beck–Develin, [arXiv math/0409562v3](https://arxiv.org/pdf/math/0409562v3), Theorem 5, p. 8 | Reciprocity for rational polytopes uses actual dimension and relative interior. It supports the proof's parity/interior premise even when vertices are not integral. Macdonald's original 1971 article is credited; its full publisher text was inaccessible in this audit. |
| Multivariate lattice counting | Haase–Juhnke-Kubitzke–Sanyal–Theobald, [*Mixed Ehrhart polynomials*](https://www.math.uni-frankfurt.de/~theobald/publications/mixedehrhart1.pdf), Theorem 2.1, p. 3 | The Bernstein–McMullen polynomial counts nonnegative integer Minkowski combinations of lattice polytopes; its separate degrees and total degree have the stated dimensions. It requires the actual whole Minkowski identity used by the publication. |
| Linear Ehrhart additivity | Böröczky–Ludwig, [*Minkowski valuations on lattice polytopes*](https://dmg.tuwien.ac.at/ludwig/lattice.pdf), Theorem 22 and Corollary 23, p. 14; acknowledgments, p. 41 | The first Ehrhart coefficient is Minkowski additive on lattice polytopes. The authors explicitly credit Raman Sanyal for the observation and proof. The particular transportation lower bound proved here is a separate result. |

The two 2006 King–Tollu–Toumazet SLC articles are correctly distinguished:
[B54Ad](https://www.mat.univie.ac.at/~slc/wpapers/s54Akitoto1.html) is the
stretched-LR article; [B54Ah](https://emis.de/ft/13885) is the Kostka
factorization article. B54Ah, p. 8, equation (4.1), has the cited polynomial
`(t+1)(t^2+2t+2)/2`; the roots of its quadratic factor are `-1 ± i`.
That antecedent does not establish roots with positive real part.


## Bibliographic coverage

The original Macdonald article and full KTT 2009 article were not accessible
through the checked pages. The directly inspected Beck–Develin and Ressayre
statements supply the relevant reciprocity and factorization interfaces.
The bibliography supplies the mathematical premises; the reproduction
scope of each computational result is described with that result.
