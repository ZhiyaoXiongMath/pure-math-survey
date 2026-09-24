# Pure Math Survey 1.2.0

A concise-first research and writing skill for English pure-mathematics surveys. Follow [SKILL.md](SKILL.md). User interaction and release reports may be in the user's language.

## Generate only what was requested

```sh
python scripts/create_project.py --output ../my-survey --topic my-topic
# Default: Part V concise only.
python scripts/create_project.py --output ../my-suite --topic my-topic --documents suite
# Explicit series: Parts I–V concise.
python scripts/create_project.py --output ../my-pair --topic my-topic --documents 5:concise,5:standard
```

Creation produces an **unverified scaffold**, never a researched manuscript or a PASS report. Replace all insertion text, verify primary sources and current status, write the selected mathematical content and populate the existing records. See [length and selection](references/length-and-selection.md), [introduction](references/introduction.md) and [core problems](references/core-problems.md).

Concise total-page review limits, including references: I 5, II 6, III 6, IV 5, V 10. Do not pad, shrink fonts or suppress hypotheses. Standard editions are optional. The frozen full dHYM sample sets mathematical quality; the compact adaptation demonstrates shorter scope.

## Maintenance and delivery

```sh
python -m unittest discover -s tests -v
python scripts/build_checks.py --output ../maintenance-build
python scripts/check_reading_budget.py ../my-survey
python scripts/validate_project.py ../my-survey
python scripts/package_release.py --output ../pure-math-survey-1.2.0.zip
```

Builds require pdfLaTeX and ordinary AMS/LaTeX packages. The preferred font is STIX2; an unavailable STIX2 font triggers a reported Latin Modern fallback. PDF budget/visual utilities additionally use PyMuPDF; comparisons use Pillow. No font files are bundled. The 1.2 page-budget unit tests also require PyMuPDF; packaging uses the Python standard library.

Read [template maintenance](references/template-maintenance.md) and [release verification](docs/release-verification.md). Technical checks do not certify mathematical correctness. The end-to-end Griffiths companion project records actual source-level checks and explicitly limits its treatment of very recent preprints; it is distributed separately, not silently loaded as a universal template.

## Compatibility and provenance

Release **1.2.0**; data schema **1.0.0** unchanged. Based on the 1.1.0 branch, with the 1.1.1 branch's introduction/core-problem guidance and adapted project generator. These were parallel branches, not a sequential upgrade. Preserve the frozen sample's original provenance and the established structural validator. See [change log](CHANGELOG.md).
