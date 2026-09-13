# Independent review of the researcher edition

An independent read-only Codex reviewer examined publication commit
`64e18347b1bbd7cb3e881d61b369aaa27d5dc602` and the frozen correspondence,
source audit and selected-content proposal on 13 September 2026. The scope
covered mathematical presentation, exact verification claims, attribution,
recipient access and public-content risks. This was one edition review round,
separate from the earlier finite-box scientific gates and from human review.

The reviewer returned one **Low** finding: the documentation-adaptation
manifest attributed the preimage of the newly authored `REPRODUCING.md` to
the older baseline commit, where that file did not exist.

**Disposition: implemented.** The entry now explicitly identifies an
unpublished draft correction. The baseline guarantee applies only to entries
whose earlier bytes are actually in that Git snapshot. Local verification
checked every published preimage against its Git blob and the new draft
against its retained preparation bytes. This is a metadata repair; no
mathematical statement, executable checker or numerical input changed.
The same frozen review returned no other findings. No extra review round was
used for this locally verified correction.

The completed [publication checks](PUBLICATION-CHECKS.md) retain their exact
scope. Neither this review nor the previous AI-assisted scientific review
constitutes external human endorsement or a worldwide novelty determination.
