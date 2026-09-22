# Pure Mathematics Systematic Review

Version 1.0.1. An installable skill for source-grounded English mathematical reviews in five parts and two depths. New projects default to ten PDF/TeX reader documents; any nonempty requested subset is supported, including V-only. Part V is an independently organized thematic review, not a requirement to reproduce I–IV.

## Installable directory

The exact installation subtree is `skills/pure-math-systematic-review/`. Use that directory with a compatible skill host, or extract the installation ZIP, which contains one `pure-math-systematic-review/` root. This repository contains no installation hooks, remote configuration or automatic publishing. The user chooses the repository owner, license and remote destination; no repository URL or license grant is implied.

Runtime instructions, references, templates, registry formats and the project validator are self-contained in the skill subtree. A real manuscript build needs the TeX packages documented in the [writing guide](skills/pure-math-systematic-review/references/writing-style.md). Python tools require Python 3.10 or later; the runtime validator uses only the standard library. Full development metadata checking also uses PyYAML. A local `pdflatex` is needed for the required template compilation; `pdftotext` is used when available.

## Development checks

From the repository root:

```sh
python -B dev/validate_skill.py skills/pure-math-systematic-review --require-yaml
python -B dev/tests/test_validation.py
python -B dev/run_regression.py --require-tex --keep-build ../pmsr-template-build
```

The runner invokes the existing structural fixtures and compiles all ten short template entrypoints in an isolated copy with shell escape disabled. `--keep-build` must be outside the repository and installable tree. Its report leaves visual inspection pending: render the changed pages and inspect them separately. A missing TeX engine is not a passed build; `--require-tex` makes it a failure. The fixtures use synthetic metadata and PDF signatures, not mathematical evidence or finished PDFs.

An explicit skill path can be passed to the runner. It forwards that path to the fixtures through `PMSR_SKILL_ROOT`, so an independently extracted installation tree can be checked without copying development tools into it. Real research-project checks are documented inside the skill and do not depend on `dev/`.

Keep validation proportionate: focused fixtures for changed behavior, ten short template builds, affected visual pages and a bounded content trial where writing behavior changes. Do not regenerate a full research corpus, enumerate every document subset, or add a testing or publishing platform. Automated checks are structural, never certification of mathematics, source coverage or exposition quality.

## File-only packaging

Use an ordinary ZIP tool. Archive only `skills/pure-math-systematic-review/` as a single `pure-math-systematic-review/` root for installation. For repository source, include this README, `.gitignore`, `skills/` and `dev/` under one repository root; omit `.git`, caches, preview PDFs, build output, trial material and private source collections. Do not put development verification or release stories inside the installation tree.

Reopen each ZIP, compare the intended members, reject unsafe paths/duplicates/symlinks and compare bytes. Run `dev/validate_skill.py` on the installation ZIP. Compute each ZIP's SHA-256 externally after packaging. The developer's final verification report distinguishes fixture checks, template builds, bounded content review, independent-review limitations and any prior E2E evidence.
