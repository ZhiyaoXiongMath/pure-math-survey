# Validation of a research project

Run the problem-formulation plan check before drafting and its release check on final expanded TeX. Read the opening for definitions, meaningful variations and ordered quantifiers before reading answers. Check user/input-to-opening-to-answer coverage, not only introduction/body consistency. Exact bindings and dependency checks detect specified regressions; they do not prove scope completeness or mathematical equivalence. See [problem formulation](problem-formulation.md).


Structural validation, source review, mathematical reading, compilation, visual inspection and archive checks answer different questions. Keep their evidence separate; none certifies the others.

## Runtime structural check

Run `python pure-math-survey/scripts/validate_project.py PROJECT`. The standard-library parser requires Python 3.10+. It checks the requested document set, safe literal braced inputs (including explicit `.bbl`), mapped component placements, labels, identity links and required audit rows. It does not interpret arbitrary TeX macros, verify evidence content or prove semantic equivalence. `--template-mode` is only an instructional preview, never publication acceptance. The real build must also resolve all dependencies.

Use [records and delivery](records-and-delivery.md) for the unchanged schema and conditional records. A file signature is not visual inspection. A completed audit row is a declared review outcome, not an independently discovered fact.

## Source and mathematical reading

Follow [research and evidence](research-and-evidence.md) for source identity, exact controlling versions, theorem locators and search limits. Review hypotheses, quantifiers, phase or parameter ranges, regularity, conclusions and status against the source. Include surrounding comparisons and claimed implications: a correct canonical theorem can still sit beside false prose. When a source version changes, review affected claims again; a fingerprint only detects identity drift.

Read each requested document without undelivered parts. Check the selected question and its principal answers against the architecture fixed before drafting. Use the introduction-only and reverse-coverage tests in [introduction](introduction.md), the passage-level rules in [writing style](writing-style.md), and the depth tests in [editions](editions.md). These are substantive reading tests, not keyword, heading, theorem-count or page-ratio tests.

For each selected method, identify the precise input, the object constructed or estimated, and the output used next. Apply [proofs and boundaries](proofs-and-boundaries.md) to distinguish a local derivation, an imported theorem, a proof route and a complete-proof claim. Do not require recursively reproving the literature; do not accept technique names as a promised explanation. Review each claimed frontier status using [core problems](core-problems.md), even when no numbered Problem is printed.

## Evidence in existing audit rows

Record located findings and repairs in `release-audit.csv`, linking a shared review note where useful. Do not add a parallel approval table.

| Row | What its completed review actually covers |
|---|---|
| `source_identity`, `statement_verification` | Sources/versions and retained mathematical statements; disclose access limits beside the relevant source. |
| `reader_outcomes`, `edition_depth` | Independent readability, introduction/body coverage and the requested depth of actual passages. For V use [the article guide](part-v-benchmark.md). |
| `proof_depth` | Only the argument treatment actually promised and supplied, with exact imported inputs and unresolved steps. |
| `edition_semantic_consistency` | Shared statement meanings and surrounding prose. In a single edition, compare against its sources; do not claim an absent companion was reviewed. |
| `frontier_status` | Supported status within the selected scope, including settled or refuted formulations and version-qualified preprints. |
| `build_requested_documents`, `visual_requested_documents` | Actual entrypoints, stable references, log findings and every rendered page. |
| `archive_integrity` | Reopened archive membership, dependencies, safety and recomputed checksums. |

`proof_framework` and `decisive_mechanisms` are required only when Part III is requested. For V-only they may be absent or reasoned `NOT_APPLICABLE`; V method explanations remain subject to reader/depth review. Paired editions need comparison of actual common content and deeper treatment, not a page-ratio verdict. Single-edition work needs no invented paired review.

## Body-structure review and regression

Under the existing `reader_outcomes`, `proof_depth` and `edition_depth` checks, perform two distinct readings: (a) local context plus statements, without proofs; (b) the dependency chain of the proofs and imported inputs. Record actual answers for each substantive body section. Inspect whether results are recoverable, hypotheses are nearby, statements have one logical role, proof boundaries are visible, imported inputs have exact sources, and every key output is used. A theorem wrapper around a mixed argument is a failed reading, not a repair.

New scaffolds declare `skill_version: 1.7.1` and a per-document `structure_review` JSON path under `evidence/`. This is supporting evidence for the existing audit rows, not a second approval registry. Use `scripts/check_mathematical_structure.py PROJECT --tex FILE --review RECORD`. It checks literal-input expansion, real body environments (not comments or unused preamble macros), result and proof labels, coverage of the actual body results, section roles, citation-key presence and a fingerprint of the reviewed expanded source. A source edit invalidates the fingerprint; reread before updating it. The JSON format and machine limits are documented in [records and delivery](records-and-delivery.md).

`validate_project.py` invokes these checks for 1.5+ manifests. Its legacy path also detects the known introduction-only/body-empty failure when actual sections and introductory results exist. A legitimate context-only section needs a located reason, not a forced theorem. Counts describe layout; they are not quality scores.

Maintain negative tests for: introduction-only results; all body results removed; decorative/commented environments; a missing key-lemma wrapper; an argument left inside a statement with no proof boundary; a quoted input with no source; incomplete coverage despite an unchanged total count; stale review evidence; and unresolved draft records. Synthetic tests test the checker, not mathematical correctness. Run an actual old-manuscript regression and mutations of the final article as well.

## Findings and disposition

Repair mathematical errors, missing necessary hypotheses, unsupported core status claims and absent promised explanations before completing the affected check. A disclaimer does not repair a broken core. Apply the same local repair/recheck discipline to bloated statements, trivial transitions, ambiguous conditions, misleading notation or rendered overflow. Useful self-contained repetition is not a defect.

Keep source-access, reviewer-independence and search-coverage limits precise. With no independent agent, perform a separate source-first author reread and disclose that it is not independent review. Do not invent a reviewer or an additional gate. Reject an unsupported objection with a reason; sustain valid defects and recheck their dependents. Retain material findings and their actual disposition, not just a PASS label.

## Build, visual inspection and archive

Compile every requested entrypoint until references stabilize, including the required bibliography step. Inspect errors, undefined references/citations, duplicate labels, missing glyphs and substantive box overflow. Record commands, engine, dependency versions and actual results.

Render and inspect every page: title, theorem conditions and numbering, notation, equation breaks, references, bibliography and page boundaries. Repair local issues locally. A genuine shared-style change requires affected regression builds. Never shrink type or margins merely to satisfy a length limit. Check standalone exports as actual additional entrypoints, not as assumed copies.

Reopen the delivered archive, compare its intended member set and recompute hashes. Exclude unsafe paths, symlinks, font files, private data and omitted dependencies. Provide an external archive digest. Do not inherit an earlier archive or frozen-sample verdict.

## Honest conclusions and stopping

Use `DELIVERABLE_WITHIN_PROTOCOL` when the requested core and necessary checks are completed within scope; use `DELIVERABLE_WITH_LIMITATIONS` for a satisfied core with disclosed supplementary limits or the permitted author-reread fallback. Unresolved core defects or missing mandatory checks require `INCOMPLETE`, or `BLOCKED` when input/capability prevents continuation. Do not introduce new audit status names or weaken the protocol to pass.

A source-first reread is not independent review; checking a theorem is not checking its entire proof. Structural acceptance, successful builds, page counts and CSV statuses do not establish mathematical quality. Once the necessary checks and local repairs are complete, stop rather than expanding the requested task.

## Skill maintenance and regression limits

[Template maintenance](template-maintenance.md) owns current-style versus frozen-style staging and behavioral test requirements. Run `scripts/validate_assets.py`, then real `scripts/build_checks.py` builds. Run the development unit suite when working from a development distribution. Neither synthetic assertions nor maintenance builds are a new research-survey evaluation. Retain [semantic adversarial cases](../assets/exposition-examples/semantic-cases.md) as reading tests, not an automatic semantic grader.

Use `scripts/compare_pdf.py` for optional same-toolchain page/text/pixel comparisons. Pixel identity establishes reproduction, not correctness. Report separately which source/math review, rendering, historical reproduction, mutation regression and cross-topic generation evaluations actually occurred. One dHYM case does not demonstrate generalization to other mathematics.

## Selection and discovery in 1.7.0

For version 1.7.0 and later, run check_survey_selection.py PROJECT --stage plan and --stage release. Project validation invokes the release check. The checker reads actual registries and bound source spans. Semantic mutations need explicitly recorded source-based review: keywords cannot grade meaning. Legal zero-Problem accounts and justified secondary methods remain admissible.

Since 1.7.1 the declared shared core must contain every local principal answer, even when only one edition is requested. Synthetic paired tests allow additional secondary results while rejecting principal-answer omissions. They do not certify that the selected roles are mathematically appropriate.
