---
name: pure-math-survey
description: Develop source-grounded English mathematical surveys and substantive revisions. Select any requested parts and concise/standard editions of a five-part series; organize around core research questions, precise principal answers, proof mechanisms and verified boundaries; deliver rebuildable TeX and inspected PDFs.
---

# Pure Math Survey

**Version:** 1.5.0

## Scope and selection

Write around a research question, not the union of available references. Fix objects, parameter range, prerequisites and depth before selecting sections. Preserve the user's mathematical scope. Both editions preserve the core statements and key lemmas. Concise compresses proof interiors and routine calculations, not mathematical structure. Standard expands the same proof routes and constructions for deeper study. Historical examples never override the request.

For an ordinary single-topic survey, default to Part V concise. An explicitly requested five-part series selects I–V concise. An end-to-end **test** of a specified part does not request the whole series. Standard or paired editions require a request; any nonempty subset is valid. Mathematical manuscripts and skill instructions are English; discussion and delivery notes may follow the user's language.

Read [length and selection](references/length-and-selection.md) and [editions](references/editions.md), then record the selection in the project manifest and existing architecture note. Use `scripts/create_project.py --documents 5:concise` for a V-only scaffold. All generated audit rows begin pending. Page limits include references and trigger editorial review; never shrink the shared readable typography to meet them.

## Research before drafting

Read [research and evidence](references/research-and-evidence.md) and [core problems](references/core-problems.md). Discover organizing questions, original formulations, principal theorems and counterexamples before choosing the bibliography. Search established alternative names. Trace claims to primary sources and check current versions when their status may have changed. Separate solved statements, refuted formulations, verified open problems, unverified status and out-of-scope material. Failed search proves neither openness nor settlement.

An important neighboring problem may deserve a short sourced explanation without a new theory chapter. Do not invent an open problem to fill a template. For every V request, read [the Part V guide](references/part-v-benchmark.md) before drafting; every sample is optional for both editions. Part III owes its selected proof routes; Part V owes its own integrated explanation, not unrequested volumes.

## Introduction and statements

[Introduction](references/introduction.md) governs principal-answer coverage. Define indispensable notation first and state the actual principal answers with their necessary hypotheses. A roadmap or citation does not replace a statement. Perform an introduction-only reading test and check coverage in both directions: every principal promise is delivered, and every principal body conclusion is visible in the introduction. Supporting lemmas need not become principal theorems.

[Writing style](references/writing-style.md) governs expression. Do not invent decorative names for definitions or results; author attribution is useful. Keep each statement focused on its essential conclusion. Use short clauses or itemized independent hypotheses rather than long sentences. Put secondary consequences afterward unless essential to the result. A repeated statement is acceptable when it reduces real backtracking; preserve local understanding and reuse a label-free canonical body when practical. There is no fixed theorem count. This does not license an introduction-only theorem structure: independently usable body results and essential proof inputs must remain explicit statements, followed by a clearly bounded proof, proof sketch or sourced explanation.

## Mechanisms and editions

[Proofs and boundaries](references/proofs-and-boundaries.md) governs explanation depth. For each selected mechanism identify its input, the object constructed or estimated, and the output used next. Explain a difficult interface with a calculation, lemma or precisely located imported theorem. Technique names alone are not an explanation. Outline the result/lemma dependencies before writing explanatory prose; do not retrofit a few theorem wrappers around an unchanged essay. Separate survey derivations from quoted results and preserve the latter's actual range.

Prefer formulas to wordy paraphrases. Omit trivial transitions; a definition or substantive mathematical sentence is often sufficient. Retain examples only when they compute a model, explain an assumption, distinguish formulations or exhibit failure. Do not impose quotas for examples or Problems. Concise compresses depth, not branch conditions, regularity or truth status.

## Verification and delivery

Use [records and delivery](references/records-and-delivery.md) for file/schema details and [validation](references/validation.md) for checks and finding dispositions. Reuse existing records rather than adding parallel audit tables. Canonical components serve actual reuse or export, not compulsory fragmentation of every lemma. Keep bibliography identity, controlling version, locator and status traceable. A changed bibliographic fingerprint requires source review; a matching fingerprint does not certify mathematics.

Review twice: first read local definitions and statements without proofs to recover the knowledge; then follow proof inputs, intermediate outputs and closure. Record located answers in the existing reader/depth evidence, and run `scripts/check_mathematical_structure.py`. Its fingerprint and coverage checks do not certify those answers. Compile from clean inputs until references stabilize; inspect all rendered pages and recheck affected pages after repairs. Reopen archives, verify member hashes and exclude font files, private data and restricted source texts. Keep production notes out of the article. Distinguish source checking, mathematical review, compilation, rendering and reproduction. Disclose when independent review is unavailable; an author reread is not independent review.

Report the actual evidence, remaining limitations and requested deliverables using the statuses in validation. Stop after necessary checks and repairs; do not add unrequested volumes. A single successful topic is not evidence of general mathematical reliability.

## Maintenance

Read [template maintenance](references/template-maintenance.md) and [layout and build](references/layout-and-build.md). Run `scripts/validate_assets.py` and `scripts/build_checks.py`, then inspect renders. Current-style regression must use `assets/templates/math-review.sty`; frozen reproduction must use the sample's bundled style in a separate target. Test with deliberately different dependencies so a stale copy cannot pass unnoticed. Preserve frozen evidence unchanged and date new verification separately.
