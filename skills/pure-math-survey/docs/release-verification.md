# Verification of release 1.2.0

Executed 24 September 2026. These are results for this release, not automatic guarantees about future generated manuscripts.

| Check | Actual result | Evidence |
|---|---|---|
| Unit tests | 113 passed; includes 29 new selection, budget and template-depth checks beyond the 84-test baseline | `verification/unit-tests.txt` |
| Maintenance builds | 14 passed: ten general templates, one two-result fixture, frozen original and shared-style rebuilds, compact dHYM adaptation | `verification/maintenance-builds.json` |
| Frozen style adapter | All 21 pages pixel-identical at 90 dpi | `verification/frozen-style-comparison.json` |
| Compact dHYM reference | 3 pages, all rendered and inspected; no clipping or missing glyphs observed | `assets/reference-samples/dhym-compact/` and companion visual evidence |
| Real topic | Five Griffiths manuscripts, 3/3/4/3/6 pages; all compiled, structurally validated, within budget and visually inspected | Separate `griffiths-survey-2026-09-24.zip` |
| Clean project reconstruction | Final project ZIP extracted and all five PDFs rebuilt; all 19 pages pixel-identical | Companion `verification/final-project-archive.json` |

The preferred STIX2 font was available; no fallback occurred. General templates remain instructional previews. The two-result fixture intentionally tests a contents page and extended recalls as style features; it is not the concise manuscript page model. Final standard III/IV/V previews were inspected again after adding real depth modules and optional canonical Problem slots. The compact sample's original-number recall is intentional.

The input branches were separately tested: 1.1.0 had 84 passing tests and 1.1.1 had 66. Counts indicate tested behavior, not mathematical superiority. The final branch uses 1.1.0's stronger canonical/packaging implementation and the other branch's useful introduction/core-problem guidance.

The companion project records source-level self-review. No independent expert review or complete proof certification of the September 2026 preprints was performed. Identity, statement provenance, declared proof depth, semantics, typography, page counts and archive integrity are separate judgments. The skill package's final archive checksums and extraction-test result are recorded outside that ZIP to avoid self-referential checksums.
