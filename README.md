# Pure Math Survey

**Version 1.5.0 — clean distribution.** A skill for source-grounded English mathematical surveys and substantive revisions, delivered as rebuildable TeX and inspected PDFs.

Default to Part V concise. An explicitly requested series selects Parts I–V concise; any nonempty part/edition selection is supported. Both concise and standard preserve core statements and key lemmas. Concise compresses proof interiors and routine calculations; standard develops the same mathematical routes more fully.

| Part | Reading task |
|---|---|
| I. Foundations and Models | Understand the objects, questions and explanatory models. |
| II. Results and Relations | Understand precise conclusions, conditions and relationships. |
| III. Proofs and Methods | Understand selected proof routes and decisive mechanisms. |
| IV. Applications, Boundaries and Problems | Understand applications, established limits and verified open problems. |
| V. A Thematic Review | Read one integrated account organized around a central question. |

## Install and use

Copy [skills/pure-math-survey](skills/pure-math-survey/) into your local skills directory, then invoke:

```text
Use $pure-math-survey to write Part V concise on [topic] for [audience].
```

See [SKILL.md](skills/pure-math-survey/SKILL.md) for the workflow and the [skill README](skills/pure-math-survey/README.md) for commands and dependencies. Python 3.10+ is required; TeX builds use pdfLaTeX. PDF utilities additionally use PyMuPDF and, for pixel comparisons, Pillow.

## Contents

The installable directory contains functional instructions, scripts, templates, reusable exposition fixtures and optional reference samples. Development reports, change logs, historical verification outputs, unit-test source files and unrelated delivery artifacts are excluded. Samples retain their mathematical content and dated qualifications; they are not current mathematical authorities.

From the skill directory, run `python scripts/validate_assets.py` to check asset structure. Use `python scripts/build_checks.py --output /absolute/new/build-directory` to check template and sample compilation. Research, source review and visual inspection remain separate tasks; successful scripts do not certify mathematical correctness.

To create a verified installation archive, run `python scripts/package_release.py --output /absolute/path/pure-math-survey-1.5.0-clean.zip` from the skill directory. Keep output outside the skill tree.
