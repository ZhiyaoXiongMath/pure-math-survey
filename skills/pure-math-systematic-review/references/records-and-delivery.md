# Project format, records and delivery

## Manifest and source layout

The skill version is 1.0.1; the project manifest schema is `0.9.0`. They identify different objects. `project-manifest.json` has `language: "en"` and a `documents` array whose records contain integer `part` 1–5, `edition` (`concise` or `standard`), `tex_file` and `pdf_file`. Paths are safe project-relative POSIX paths.

Without `requested_documents`, the schema requires all ten part/edition combinations. Otherwise that field is a nonempty list of unique objects with exactly `part` and `edition`; `documents` must match it exactly. Record the user's selection before drafting, never infer it from finished files. Preserve the actual scope of an update. A V-only standard manifest is:

```json
{
  "schema_version": "0.9.0",
  "language": "en",
  "requested_documents": [{"part": 5, "edition": "standard"}],
  "documents": [
    {"part": 5, "edition": "standard",
     "tex_file": "topic-part5-integrated-standard.tex",
     "pdf_file": "topic-part5-integrated-standard.pdf"}
  ]
}
```

Names may follow `<topic>-part1-foundations-concise.tex` and the matching stems for `part2-results`, `part3-methods`, `part4-boundaries` and `part5-integrated`, each at its requested depth. Deliver matching PDFs and all rebuild dependencies: the shared style, canonical components, bibliography and any actual additional inputs. V-only needs no standalone I–IV artifacts and no companion edition. Its own selected survey contract governs its content.

## Mathematical ownership and placements

`publication-map.csv` defines each substantive selected statement's mathematical identity and principal public placements. Its fields are:

```text
node_id,kind,owner_part,canonical_component,source_ids,proof_ids,
concise_file,concise_label,standard_file,standard_label,
concise_treatment,standard_treatment,limitation_note,
integrated_concise_file,integrated_concise_label,integrated_concise_treatment,
integrated_standard_file,integrated_standard_label,integrated_standard_treatment
```

`owner_part` is 1–4 and identifies the mathematical role, not a demanded deliverable: elementary facts may be owned by I, main results by II, technical arguments by III and frontier Problems by IV. A node can appear only in V. The unprefixed concise/standard slots refer to the owner; each `integrated_*` slot refers to the corresponding V edition. Each file must match that actual manifest document. Locations use descriptive mathematical labels rather than internal IDs. Source/proof IDs link their registries; use semicolons for lists.

A canonical component is body-only TeX: no document or theorem-like wrapper, including no `problem` wrapper. Put the environment, name, numbering and label around its `\input` in the manuscript. The same complete mathematical statement is reused wherever `FULL_STATEMENT` is selected. Other prose can be rewritten or reorganized.

| Treatment | Valid requested placements | Coordinates and body |
|---|---|---|
| `FULL_STATEMENT` | All parts and editions | The actual document and a unique semantic label; exactly one input of the canonical body |
| `REFERENCE_ONLY` | I–IV concise and both V editions | Actual document and unique label, accurate source/locator and independently usable local explanation; no body input; reason in `limitation_note` |
| `OMITTED_WITH_REASON` | I–IV concise and both V editions | Empty file and label; no input of the component in this actual part/edition; substantive reason in `limitation_note` |
| `NOT_REQUESTED` | Only an unrequested document | Empty file and label; never a substitute for treatment inside a requested document |

I–IV standard placements retain `FULL_STATEMENT`. V may omit side branches, intermediate lemmas or minor examples outside its own core in either edition. It may reference accurately with the assumptions needed for independent reading, not delegate necessary content to an undelivered volume. Its own advertised main-result understanding and core Problems cannot be omitted to satisfy a parser. Explain reasons separately by placement in the existing note when they differ. Core selection and adequacy of reasons are human judgments.

Every node needs at least one actual requested full or referenced placement; do not create unused placeholder nodes. Ordinary local cross-references are not additional map rows. Extra cross-part placements can use `canonical-crosswalk.csv`. After fixing a shared statement, check actual affected documents, their surrounding prose and status claims.

## Required and conditional records

Use [registry templates](../assets/registries/) as formats, not as a demand to instantiate every collection. For runtime structural validation the project needs `bibliographic-identity.csv`, `proof-mechanism-registry.csv`, `publication-map.csv` and `release-audit.csv`. The proof registry can be header-only when no proof nodes are used; a method explanation is not a fabricated complete-proof record. Bibliographic identities and publication nodes must be real and nonempty.

Retain the research records actually used: scope/protocol, architecture and edition plan; search replay, source manifest, screening, identity/version decisions and conventions; canonical results and proof provenance; relevant theory/history relationships; frontier claims and reverse searches; and verification/build/visual evidence. Update dispositions, prospective holdouts and insertion checks are conditional on the actual task. Do not manufacture unrelated empty audit tables. Existing filenames containing theorem, estimate or geometry terminology do not impose a kind of mathematics. Choose CSV or JSONL representations as useful rather than duplicating evidence without purpose.

`release-audit.csv` has `check,status,evidence,note`. Never prefill PASS. Required checks are `source_identity`, `statement_verification`, `proof_depth`, `reader_outcomes`, `edition_depth`, `edition_semantic_consistency`, `frontier_status`, `build_requested_documents`, `visual_requested_documents` and `archive_integrity`.

Only a request containing III requires `proof_framework` and `decisive_mechanisms`, covering the requested III editions. Without III these rows may be omitted or use `NOT_APPLICABLE` with a reason, including in V-only projects. If III and V are both requested, V's lighter contract does not waive III's checks. V method explanations and relationships are reviewed in `reader_outcomes` and `edition_depth`, not a new audit table.

For IV or V, `frontier_status` requires completed review within the part's own scope, including a supported settled-scope conclusion when appropriate. It cannot be waived for lack of a problem list. Without IV/V a genuinely inapplicable frontier check may be `NOT_APPLICABLE` with a reason. All other required checks remain applicable: for example, single-edition semantic consistency checks the actual source/body/prose scope rather than claiming a comparison with an absent counterpart.

`proof_depth` records actual argument treatment and declared bounds. A V method sketch does not require a full proof; its evidence should describe the sketch and imports actually reviewed. `reader_outcomes` checks document-specific promises and locations; `edition_depth` checks the selected backbone, real concise selection and standard's added understanding. Accepted completed statuses are `PASS`, `VERIFIED` and `COMPLETE`, each with nonempty evidence. The program verifies records, not the truth or adequacy of the judgments.

### Architecture and proof notes

Use the architecture/proof notes for core questions, document commitments, routes, selected targets and permitted imports. The proof registry's descriptive fields include `supports_node_ids`, `method_family`, `declared_inputs`, `dependencies`, `proof_treatment`, `closure_status`, `core_question`, `explanation_role`, `decisive_mechanism`, `route_locations`, `mechanism_locations`, `application_or_boundary` and `early_explanation_check`. A linked note can hold the same explanation; no extra table is required.

Locations identify the document edition and actual section, label or page, not just a shared filename. For an executed explanation check, retain its date, draft passage, outputs, first unsupported inference or checked closure, source/proof locators, revision and affected recheck. Match its depth to the actual promise: V without a deep-proof commitment needs a method account, not an imported III checklist.

## Format compatibility

The small read-only manifest branch accepts `0.8.0` with parts 1–4; an absent selection means eight documents. Missing V columns in such a map are interpreted as empty with `NOT_REQUESTED`, without modifying files. Only the exact full-eight selection accepts `build_all_eight` and `visual_all_eight` aliases. Keep an existing selection; a deliberate schema change must preserve it explicitly unless the user changes scope. No old PASS is inherited as a new review and no migration tool is required.

Optional JSONL records carrying `schema_version: "0.8.0"` identify their retained record format, not the project manifest or skill version. The concept field `geometric_intuition` accepts the relevant algebraic, structural, combinatorial or other intuition; omit unused intuition with a note. Existing records may point to architecture/proof notes instead of populating optional descriptive columns. Compatibility does not authorize new documents, silent file rewrites or invented prospective checks.

## Rebuildable archive and final delivery

Include requested PDFs and TeX, actual rebuild dependencies, the manifest/map, scope and architecture, shared research records and applicable verification evidence. If delivered PDFs are external to the archive by explicit design, identify and checksum-link them. Keep author-only reasoning, confidential documents and restricted source text out; preserve lawful locators instead.

Record the TeX engine, bibliography procedure and exact build commands. Use ordinary ZIP and Python tools. Hash the explicit selected member set in `artifact-checksums.txt`, excluding the checksum file itself. Reopen the ZIP, reject unsafe paths, duplicates and symlinks, compare members and recompute hashes. Provide the archive SHA-256 outside it. An exit code does not certify mathematics.

List all requested reader documents and disclose any absent requested item. Unrequested parts and editions are outside scope, not missing. Give a reasoned completion status and actual limitations.
