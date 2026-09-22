# Concise and standard editions

Both editions are English mathematical articles. The user's requested part/edition set governs delivery; a single edition is assessed against its own scope and sources, not against an invented counterpart. Paired editions share a part-specific mathematical core, not every supplementary topic.

## Invariants of common content

Keep the same source identity, controlling version, cutoff, notation, conventions and truth status. Every common full statement uses the same body-only component and preserves objects, hypotheses, quantifiers, exceptional cases, range, conclusion and qualifications. Keep material uncertainty and citations with the claim. A narrower corollary or stronger theorem is a separate result with a justified relationship, not an editorial paraphrase.

A correct common component does not validate surrounding prose. Check comparisons, historical judgments, failed converses, prose consequences and Problem status separately. Different labels and numbering across documents are acceptable; meanings and sources must agree.

## Depth and selection

| Part | Concise preserves | Standard deepens |
|---|---|---|
| I | Necessary concepts, a completed core model and its bridge to the general question | Foundations, model arguments and revealing variations |
| II | Core results, relationships and substantive proof ideas | Comparisons, conditions and explanations, then useful supplementary results |
| III | Connected routes and substantive explanation of selected decisive mechanisms | Key derivations, supporting claims, dependencies and closure |
| IV | Meaningful uses, established boundaries and the agreed core Problems | Applications, progress, relationships, remaining ranges and evidenced difficulties |
| V | A short self-contained thematic review: background, necessary language, selected results, method ideas and core Problems | Background links, result comparisons, key ideas and frontier discussion along the same thread |

Concise reduces reading burden through selection and organization. Start with its mathematical thread and principal section duties; merge local technical sections, omit side branches and repeated reminders, and choose representative material. Test a suspected detour by removing or compressing it: can the intended reader still understand the selected results, their necessary conditions and the promised explanation? If yes, shorten or omit it; if not, retain or reorganize the needed bridge. This is an editorial test, not permission to delete promised core content or essential qualifications. Identical headings are not themselves a defect, and fewer pages are not themselves success. Do not achieve brevity through smaller type, tighter margins or lost hypotheses.

Standard adds understanding before breadth. For a substantial addition, identify what it enables the reader to understand: the role of a hypothesis, a missing inference, a result comparison, a revealing example or the remaining range of a Problem. More citations or neighboring topics alone do not demonstrate depth. III's complete route and selected mechanisms must remain intelligible in concise; optional supporting proofs may be cited. V's method ideas must remain intelligible in concise, but V does not owe III's technical development in either edition. V standard does not automatically restore omitted technical proofs or all I–IV nodes.

For example, V concise can explain what a construction produces and how it supports a main result, while leaving a technical sublemma to a precisely located source; V standard can clarify why a key hypothesis is needed through a checked comparison. By contrast, copying every technical branch into concise and adding an unrelated bibliography tour to standard does not serve either edition. A short decisive derivation belongs in concise when omitting it would break the chosen explanation.

Record the main selection decisions and locations of added understanding briefly in the existing architecture/edition note. Do not make a new per-paragraph ledger, score, page target, section quota or fixed length ratio. For a single requested edition, apply only its own test; do not create a counterpart.

## Coverage and placement

The [publication-map definition](records-and-delivery.md#mathematical-ownership-and-placements) is authoritative for fields and treatment rules. `FULL_STATEMENT` imports the canonical body once. `REFERENCE_ONLY` is a located explanation with usable local conditions and a reason for reduced treatment. `OMITTED_WITH_REASON` has empty file/label fields and a substantive reason; no component may still be imported at that omitted placement.

I–IV standard placements require full statements. Concise placements and both V editions may select among the three treatments within their own contracts. Standard-only supplements need not be forced into concise. Likewise, a technical III node need not be forced into V standard. V core main results or Problems may not be hidden through convenient omission or delegated to absent volumes. A reference must preserve the assumptions needed to use it within this document. Every map node has at least one requested full or referenced location; a completely unused node does not belong in the publication map.

An unrequested document uses `NOT_REQUESTED` and empty coordinates, separately for each owner or V edition. This is not a treatment for skipping content inside a requested document. A V-only selection can use I–IV-owned nodes without creating those volumes.

## Reconciliation review

First compare common bodies, conventions and sources, then check surrounding prose for altered logical force. Read concise alone and apply the selection test to actual passages: can the reader follow its selected central ideas without borrowing missing necessities from standard? Read standard for located added understanding, not just extra topics. Compare the introduction, major section roles and body to ensure that promised organization is real in each edition. Record any necessary local repair and its recheck in the existing `edition_depth` evidence; a shared outline or a page-count difference cannot settle the judgment.

For V, assess its independently chosen main-result understanding, method ideas and Problems under `reader_outcomes` and `edition_depth`. `proof_depth` describes the argument treatment actually used. Only a request including III requires `proof_framework` and `decisive_mechanisms`. Shared content with other delivered parts still needs reconciliation, but those other parts do not expand V's scope automatically.

IV editions keep their own agreed core Problems. V editions keep theirs; common IV/V Problems have identical mathematical conditions, sources and status. A narrow verified settled scope is explained rather than populated with fabricated Problems. A failed search or inaccessible source proves neither openness nor settlement.
