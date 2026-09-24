# Pure Math Survey

**Version 1.2.0.** A Codex skill for evidence-grounded English surveys of pure-mathematics topics, result families and proof methods.

## What it produces

The skill supports five parts, each in concise and standard editions:

| Part | Purpose |
|---|---|
| I. Foundations and Models | Explain the objects, questions and models leading to the general theory. |
| II. Results and Relations | State the main conclusions precisely and explain their relationships. |
| III. Proofs and Methods | Develop the agreed proof routes and selected decisive mechanisms. |
| IV. Applications, Boundaries and Problems | Explain uses, established limits and precise open Problems. |
| V. A Thematic Review | Present an independently readable account organized around its own central question. |

New projects default to Part V concise, delivered as PDF and rebuildable TeX. An explicitly requested suite produces Parts I–V concise. All ten templates remain available, and any nonempty selection of parts and editions is supported; standard editions are optional.

Concise page review limits, including references, are I: 5, II: 6, III: 6, IV: 5 and V: 10. Shortening should reduce scope while preserving necessary hypotheses and readable mathematics.

Concise editions select and organize the material needed to understand the chosen thread. Standard editions deepen that understanding. Part V explains selected results, method ideas and Problems without automatically taking on Part III's detailed proof obligations.

The workflow verifies primary sources and relevant versions, preserves exact mathematical conditions, distinguishes established results from unresolved questions, and records what was actually checked. Delivery includes the TeX sources and dependencies needed to rebuild the requested manuscripts, together with research and verification records.

## Install and use

The installable skill is [skills/pure-math-survey/](skills/pure-math-survey/). Install that directory in your Codex skills location, then invoke `$pure-math-survey` and describe the topic, audience and requested parts or editions.

For example:

```text
Use $pure-math-survey to write only Part V concise on [topic] for [audience].
```

See [SKILL.md](skills/pure-math-survey/SKILL.md) for the workflow and the [release notes](skills/pure-math-survey/CHANGELOG.md) for changes. Python helpers require Python 3.10 or later. PDF budget and visual utilities additionally use PyMuPDF; comparisons use Pillow. Manuscript builds require pdfLaTeX and the packages described in the [skill README](skills/pure-math-survey/README.md).

## Maintenance

From the repository root:

```sh
cd skills/pure-math-survey
python -B -m unittest discover -s tests -v
```

These tests check package and project structure using synthetic projects. They do not establish mathematical correctness, source coverage or exposition quality, and do not replace manuscript compilation or visual inspection.

For this installation on Windows, 111 tests passed with UTF-8 enabled; two symlink tests were skipped because the host lacks symlink creation privileges. The supplied archive's 92 member checksums and skill metadata validation passed. The skill files are unchanged from the supplied 1.2.0 archive. The [upstream release verification](skills/pure-math-survey/docs/release-verification.md) records its separate build and visual checks; those were not repeated during this installation.

## Packaging

For an installation ZIP, archive only `skills/pure-math-survey/` as a single `pure-math-survey/` root. Exclude repository metadata, caches and generated build files. Reopen the archive and verify its members and contents before distributing it.
