# Pure Math Survey 1.7.1

A source-grounded English mathematical survey skill. Start with [SKILL.md](SKILL.md).

Reconstruct the problem and ordered quantifiers before choosing answers. Research beyond the selected bibliography, distinguish mathematical status from editorial selection, and retain every principal answer in the shared core.

Default to Part V concise; select other parts or standard editions when requested. Both editions preserve core statements and key lemmas. Concise compresses proof interiors and routine calculations; standard develops the same mathematical routes in greater depth.

Copy this folder into your local skills directory and invoke `$pure-math-survey` with the topic, audience and requested parts or editions.

```sh
python scripts/create_project.py --output /absolute/new/project --topic my-topic --documents 5:concise
python scripts/validate_assets.py
python scripts/check_problem_formulation.py /absolute/new/project --stage plan
python scripts/check_survey_selection.py /absolute/new/project --stage plan
python scripts/check_reading_budget.py /absolute/new/project
python scripts/check_mathematical_structure.py /absolute/new/project --tex my-topic-part5-integrated-concise.tex --inventory
python scripts/validate_project.py /absolute/new/project
```

Creation produces a pending scaffold. Research, drafting, source review, compilation and visual inspection are required before delivery; structural checks do not certify mathematical correctness.

Python 3.10+ is required. TeX builds need pdfLaTeX and the packages in `assets/templates/math-review.sty`. STIX2 is preferred, with a reported Latin Modern fallback. PDF budgets and comparison utilities use PyMuPDF; pixel comparisons also use Pillow. No font files or restricted source papers are bundled.

Optional helpers include `scripts/bibliography.py` for reviewed bibliographic data, `scripts/build_checks.py` for stabilized TeX builds, and `scripts/package_release.py` for verified installation archives. See [layout and build](references/layout-and-build.md) and [template maintenance](references/template-maintenance.md).

Sample PDFs and TeX are optional, dated exposition references, not current mathematical authorities or independent proof certificates.
