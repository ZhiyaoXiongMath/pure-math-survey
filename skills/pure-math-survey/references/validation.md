# Validation of a research project

Use structural checks, mathematical/source review, compilation, visual inspection and archive checking for their distinct purposes. No one of these certifies the others.

## Runtime structural check

Run the installed `scripts/validate_project.py` with the project directory, for example from the directory containing the skill:

```sh
python pure-math-survey/scripts/validate_project.py review-project
```

The script requires Python 3.10 or later and only its standard library. It reads the manifest, requested files, literal braced TeX inputs, map/component placements, labels, identity links and the required audit status subset. `--template-mode` allows instructional placeholders for a structural preview, not a publishable review. It does not compile TeX, evaluate PDF layout, verify every registry or examine the mathematical content of an evidence note. Follow the [format reference](records-and-delivery.md) for schemas and conditional records.

Unsupported dynamic input syntax needs explicit handling rather than a false assertion of parser coverage. Check source dependencies through the real build as well. A PDF signature is only a file-type check, not a readable-PDF or visual verdict.

## Reader and explanation review

Read each requested document independently for the declared audience. Necessary specialized objects, notation, main hypotheses and imported inputs must be understandable within it. Do not demand a prerequisite course where the reader contract assumes background.

Start from the original task and architecture/proof promises, then inspect actual passages and entrypoints. Distinguish an absent promised explanation, a wrong location in a record and an optional elaboration. Content elsewhere in the series does not fulfill a standalone commitment. Review the introduction and major sections together: recover the central question, mathematical threads, their relationships and section duties, then verify that the body carries them out. A refined introduction pasted above a flat technical inventory does not satisfy this check.

Assess statements and prose claims for exact objects, assumptions, quantifiers, ranges, conclusions, source versions and status. Check surrounding comparisons, inferred implications, history and limitations even when canonical statements match byte-for-byte. A closed local proof cannot establish overall understanding if a promised interface is missing.

Record the following judgments in existing audit rows with actual manuscript locations:

| Check | Substantive scope |
|---|---|
| `reader_outcomes` | Each requested part's own reading task; independent readability; introduction/body organization; V's selected main-result understanding, relationships and method ideas |
| `proof_framework` | Required only with III: connected routes for the core proof families in each requested III edition |
| `decisive_mechanisms` | Required only with III: substantive explanation of the selected decisive arguments at the promised depth |
| `edition_depth` | Actual depth in every requested document; concise selection/organization and standard's deeper treatment of the same part-specific core |
| `proof_depth` | Arguments actually given versus their declared proof, route or schematic treatment; exact imported inputs and claims about closure |
| `edition_semantic_consistency` | Shared body/source/prose meanings; paired comparison where present, source consistency for a single edition |

V's method explanation does not activate III's proof rows. In V-only they may be absent or reasoned `NOT_APPLICABLE`; a mixed III/V request still requires the III reviews. Absence of technical proofs is not a V failure unless explicitly promised. Conversely, method names without their role cannot satisfy V. Do not record a fictitious complete-proof verification for an explanatory paragraph.

For paired editions, apply the [selection and depth tests](editions.md#depth-and-selection) to actual passages: read concise alone for its necessary understanding and inspect where standard deepens the common thread. Do not accept or reject a pair from shared headings, page ratios or the number of extra topics. Use the existing `edition_depth` evidence for located decisions and affected rechecks. For a single edition, do not create or claim a comparison with another document.

During the same reread, check full statements against adjacent prose and check notation in its rendered form. Remove redundant complete restatements, not useful previews, local assumption reminders or necessary definitions in independently readable documents. Keep material scope and uncertainty beside the affected claim. No duplicate-detection score or additional audit table is required.

## Problem formulation and frontier review

IV and V require an executed `frontier_status` review within their own selections. Check that core unresolved targets appear as visible named, numbered and labelled **Problem** environments, with precise objects, assumptions and goals. Check their source formulation separately from knowledge status. The discussion after each Problem identifies source and cutoff, importance, verified progress, decisive solved ranges and the remaining scope or limits of verification.

Compare shared IV/V Problems for meaning, sources and status, not identical collections. V need not reproduce IV's full frontier, but must fulfill its own advertised core. A verified settled narrow scope is a completed frontier review, not an automatic waiver. Failed searches, inaccessible sources and absent lists establish neither openness nor settlement. Do not invent Problems or claim that a review-proposed direction is a consensus conjecture.

## Independent review and adjudication

Use an available independent reviewing agent for source-based research review. Give the original task, reader contract, requested manuscripts and necessary primary sources in a fresh context, without author PASS judgments or proposed findings. Ask for located mathematical reasons and have the initial findings saved before revealing the author's self-assessment.

Then adjudicate each material disagreement against the actual promise, argument and source. A blocking objection identifies a real error or reading break, the missing necessary idea/condition/interface and a minimal repair. Requests merely for more detail are optional. Correctly stated external inputs, checked hypotheses and an explanation of their role permit stopping; do not demand recursive proofs of all literature. A short but decisive bridge is not inadequate merely because it is short.

Sustain valid defects, repair locally, and recheck affected passages, dependent conclusions and paired/shared statements. Reject unsupported objections with reasons rather than by vote. When no independent agent is available, perform a separate source-first author reread and disclose that it is not independent review. No additional approval gate, unlimited waiting or prearranged multi-round evaluation is required.

## Findings and disposition

Use existing review/adjudication notes and the `evidence`/`note` fields in `release-audit.csv`, not new status names or an extra review layer. Distinguish:

| Finding | Disposition |
|---|---|
| Mathematical error, missing necessary hypothesis, unsupported core status claim, or absent promised explanation | Repair and recheck the affected statements, passages and dependents before completing the relevant check. Disclosure alone cannot turn a broken core into a pass. |
| Redundant adjacent statement, misleading rendered notation, or another local copyedit | Make the minimal edit and recheck its actual printed location and affected uses. Purely optional stylistic preferences need not block delivery; a notation defect that changes meaning is a mathematical defect, not a cosmetic one. |
| Limit of source access, reviewer independence, search coverage, build or visual inspection | State precisely what was and was not done. Use the permitted fallback where one exists. A missing mandatory check remains incomplete, while a supplementary limitation can coexist with a satisfied core. |

Completed rows certify only their stated review scope. A source-first author reread is not independent review, inspecting a theorem is not checking its whole proof, a PDF signature is not visual inspection, and sampled pages are not an all-page check. Preserve the actual outcome and recheck locations, including rejected objections and their reasons where material. Do not introduce `PASS_WITH_WARNINGS` or change the existing schema to express these distinctions.

## Build, visual inspection and archive

Compile every requested entrypoint with an available TeX engine until references stabilize; include bibliography passes when needed. Check errors, undefined citations/references, duplicate labels, missing glyphs and substantive box overflow. Record engine, build commands and actual outcomes. Missing compilation is not a pass.

Render and inspect every page of the actual requested research outputs for title/abstract, hierarchy, contents, Problem titles/numbering/spacing, formulas, citations, running heads, bibliography and page boundaries. Fix local text or formula issues locally; change the shared style only for a reproduced shared defect, then recheck affected pages. Do not hide overflow or length by globally shrinking the type or margins. Instructional placeholders must not remain in finished work.

Reopen the rebuildable archive, compare its intended member set and recompute its checksums. Confirm no unsafe paths, symlinks, unintended private material or omitted rebuild dependencies. Provide an external archive digest.

## Honest conclusions and stopping

Program acceptance means structural records are present and internally placed, not that claims, explanations, evidence or Problems are correct or complete. Do not substitute keywords, page counts, proof counts, Problem counts or CSV PASS entries for substantive review.

Report the actual scope of source access, statement checking, argument treatment, reader/depth review, frontier checking, build, visual inspection and archive verification. Use the completion status justified by the requested core and disclose limitations. Use `DELIVERABLE_WITHIN_PROTOCOL` when requested outputs and required checks are satisfied within the agreed scope; use `DELIVERABLE_WITH_LIMITATIONS` for a satisfied core with disclosed supplementary limits or an explicitly permitted fallback. Unresolved core defects or unmet mandatory checks require `INCOMPLETE`, or `BLOCKED` when the missing input/capability prevents continuation. Do not weaken the protocol retroactively to pass. Concrete failures trigger local repair and affected rechecks. With necessary checks completed and no unresolved core defect, stop rather than expanding the task or creating a testing platform.

## Skill maintenance

When editing this skill, run `python -B -m unittest discover -s tests -v` from the skill root. The standard-library suite checks the package, document selections, placements and structural validation using temporary synthetic projects. It does not compile manuscripts or assess mathematics, writing quality or page layout. These maintenance checks are not extra deliverables for a survey request.
