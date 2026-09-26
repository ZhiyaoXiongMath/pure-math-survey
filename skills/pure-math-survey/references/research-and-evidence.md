# Research, sources, and evidence

## Scope and search

[Core problems](core-problems.md) governs discovery and status. Record the question, alternative terminology, primary-source search and screening decisions in existing notes. An explicit part/edition selection determines delivery even when the literature search is wider.

## Identity and conventions

Identify every controlling source by authors, title, publication or preprint identity, exact version and usable locator. A journal theorem number and an arXiv theorem number may differ. Do not combine them without checking concordance. Keep notation translations with the first affected claim.

Prefer the source's actual theorem and relevant proof passage over an abstract, secondary summary or search snippet. When a newer version exists, either review it or explicitly pin the reviewed version and qualify current-status claims. Access failures must be recorded, not filled by invented details.

## Verification and proof provenance

Separate bibliographic identity, statement applicability, selected mechanism review and complete proof verification. These are different checks. A cited theorem remains an imported input unless its proof is actually reproduced.

The optional `scripts/bibliography.py` helper generates `.bib` and `.bbl` from `references.json`. Each record may carry verification date, locator, status and a fingerprint of identity/version/locator. Changed fields invalidate the recorded review and make the helper stop. This is a stale-evidence guard, not a verifier of mathematical truth. Set or renew fingerprints only after the corresponding source review, never just to silence a failed test.

## Frontier and history

Attribute original contributions separately from the selected exposition route. Use exact original problem formulations when relevant. Do not infer that a topic is settled or open from absence of search results. Important neighboring problems require correct relationship labels; broad conjectures do not become established equivalences through analogy.

## Updates and reproducibility

A changed source or mathematical claim triggers review of affected hypotheses, introduction, abstract, canonical statements and boundary language. Freeze the old evidence, identify new input hashes and record actual new commands. Do not copy old PASS rows into a modified article without rerunning their checks.

Distribute lawful locators, not restricted source papers or font files. Keep source-derived facts cited in the manuscript and the detailed verification trail outside reader prose.

## Organizing questions before local directions

Use the screening decisions from [core problems](core-problems.md). Do not create a competing status taxonomy or require a fixed number of Problems, references or recent papers.
