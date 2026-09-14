# Fourth and fifth coefficients at ordinary rank six

Research record: 14 September 2026. This is a computer-assisted partial result
toward whole rank-six coefficient positivity.

For every balanced ordinary Littlewood-Richardson triple with lambda outer
and maximum trimmed length at most six, write

    P(t)=c^(t lambda)_(t mu,t nu)=sum_j c_j*t^j.

Then c4 and c5 are nonnegative at every area and boundary. More precisely,

    c_k >= (1/2000000) sum_(actual k-faces F) vol_Z(F), k=4,5,

in the original saturated hive and face lattices. For a nonempty hive, c_k is
strictly positive when its actual dimension is at least k, and zero below k.
Empty positive-stretch families give polynomial zero; the all-empty triple
gives polynomial one. Volumes use lattice normalization, not factorial
normalization.

The [complete argument](../../tooling/rank6_certificates/PROOF.md) explains
the passage from the finite certificate to every whole hive, including hidden
affine strata and rational period collapse. The
[standalone reproduction guide](../../tooling/rank6_certificates/README.md)
and [exact dataset description](../../tooling/rank6_certificates/DATA.json)
supply the accompanying tooling and all finite inputs.

## Why this is an advance

The earlier ambient bounds protect c6 through c10 at rank six. These two fields
extend that protection to c4 and c5 without an area cutoff or a restriction to
selected hives. The [actual-degree consequences](LOW-DEGREE.md) close degree at most five
at rank six and degree at most four at rank seven. The remaining rank-six
coefficients c1,c2,c3 at actual degrees six through ten require further arguments;
whole rank-six positivity and unrestricted KTT remain open.

The proof uses complete normal-cycle compensation. It retains raw negative
local constants and modifies them by a field whose entire weighted correction
vanishes. All 121,241 c5 inequalities and 675,721 c4 inequalities are checked
exactly, together with every original normal subset, safe lattice type,
primitive quotient and matrix entry. All 333,769 local constants are freshly
reconstructed. An original-ray triangulation, a local positive sample or a
solver success flag is not used as a whole-coefficient proof.

## Reproducibility and scope

The complete fresh-export verification took about 10.4 minutes on the recorded
24 GiB Mac. The dataset is about 44.8 MB compressed. These measurements concern
rechecking the supplied finite certificates; certificate discovery and
arbitrary LR counting have different costs. The full command and its explicit
dependencies, limits and failure output are documented in the tool guide.

This is an incrementally shared, independently checked computational research
result. [Novelty and prior work](NOVELTY.md) records the actual comparison and
its limits. Independent code and mathematical argument review are recorded;
human peer review, institutional acceptance and worldwide priority are not
claimed. The [provenance account](../../PROVENANCE.md) remains applicable.

Alper Ferudun's rank-five theorem and correction methods are foundational
sources. The analytic local formula is due to Berline and Vergne. The complete
refined normal-cycle argument and the new finite fields retain their respective
campaign origins in the proof documentation. Software and research data use
the repository's existing licenses.
