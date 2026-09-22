# English mathematical exposition and typesetting

Use English research-level prose in every requested manuscript. The ten compilable templates are starting scaffolds; replace their instructional text, metadata and functional titles with actual mathematics. Writing rules are self-contained and impose no discipline-specific contents.

## Central question, themes and hierarchy

Begin with a concrete mathematical problem, its significance and the article's perspective. Explain the larger mathematical threads and their relationships before introducing technical subdivisions. Then identify major sections' roles and connections using actual references or natural groupings. A list of invariants, formulas or subsection titles is not an organizing account.

The hierarchy is logical: overall perspective, principal section tasks, local subsection developments. Group a lemma, example or technical variation under the larger question it serves. File sharing and `\input` granularity must not set the printed structure. Do not add empty levels for appearance. Revise the body with the introduction and keep their promises consistent. Concise may merge sections and select fewer branches than standard.

The abstract briefly states content and perspective; the introduction explains mathematical organization; the contents provides navigation. Keep these roles distinct. Do not fill the abstract with search procedures, audit results or document counts. Introduce only the notation needed to read the central question, then define further symbols near their use.

Place the `abstract` environment before `\maketitle` in `amsart`. Include the part and edition in the title and use only authorized, verified author/date metadata. Each part needs its own introduction, not a copied project description.

## Statements and connected reasoning

Use mathematical environments as appropriate for results, constructions, comparisons, classifications and examples. Preserve exact objects, assumptions, quantifiers, scope and conclusions. A nearby explanation must not silently broaden a theorem or turn an analogy into an implication. Verify translations of conventions before comparing results. Cite the precise point of dependence, including a source theorem, lemma, section or formula when available.

Keep notation coherent across requested documents, defining specialized meanings within each independently readable piece. Cross-volume references supplement navigation; they do not carry indispensable assumptions. Use descriptive mathematical labels and names, not internal record IDs as printed headings.

At the depth promised by the part, explain what an idea does and how it supplies a conclusion. III develops its agreed routes and selected mechanisms; V gives method ideas and their logical role. State usable external inputs precisely and check their hypotheses. Explain essential dependencies without forcing every discipline into estimates, flows or analytic terminology. A short decisive argument can suffice; a list of names cannot replace an explanation. Label proof sketches, derived reconstructions and cited technical inputs honestly.

## Part V and editorial freedom

V is a thematic review organized around its own central question. Explain background, necessary language, accurate selected main conclusions and their relationships, method ideas, and worthwhile Problems or directions. It can write directly from shared research or adapt other parts. Do not require prior completion of I–IV, impose a generation order, or infer resource use from visible reuse.

Use one introduction, notation system, contents, numbering and bibliography. Reuse full canonical statements once and refer locally thereafter with the necessary assumptions. Narrative passages may be reused, compressed, rewritten or reorganized. New synthetic claims in an introduction or closing perspective need mathematical support like other claims.

Concise chooses and organizes a short complete thread. Merge repetitive local sections, discard side branches and compress secondary computations; keep conditions, sources and essential ideas intact. Do not merely remove standard addenda from an unchanged exhaustive outline. A compact method paragraph often supplies what V needs; retain a short derivation only when it materially aids understanding. Standard deepens comparisons, background relationships, key ideas and frontier discussions, without automatically importing III's detailed proofs or I's full foundations course.

## Problems and their discussion

Use `problem`, not `question`, as the environment for core unresolved targets. The shared `amsthm` definition style gives a bold title and number with upright body text. Each Problem has a short mathematical name and a semantic label:

```latex
\begin{problem}[A descriptive mathematical title]
\label{prob:descriptive-name}
% Precise objects, hypotheses, quantifiers, and unresolved target.
\end{problem}
```

Refer to it as `Problem~\ref{prob:descriptive-name}`. In mapped content the environment/name/label surround a body-only canonical input. Keep lengthy history outside the statement. Follow it with formulation source, cutoff status, importance, major verified progress, precise solved and remaining ranges, and evidenced relationships or difficulties where useful. Do not force an obstacle or strategy for every Problem.

Different core targets need distinct environments; related subquestions may share one. Do not count environments to certify coverage. V selects the frontier serving its own thread; IV covers its agreed frontier systematically. Shared targets must remain accurate across parts and editions. Distinguish established source Problems from the review author's proposed directions. An explicit verified settled scope is preferable to an invented open question.

## Applications, sources and evidence

Give examples a mathematical purpose and enough verification to support it. Failure of an assumption alone does not refute a conclusion; failure of one proof does not establish impossibility. Keep counterexamples, open cases, scope exclusions and evidence gaps distinct.

Preserve citations and material version qualifications beside the relevant claim. A short source/version appendix is useful when mathematical meaning depends on it; detailed retrieval and audit records belong in the rebuildable bundle. Do not turn Part IV into an audit report. Historical explanation needs sources, not merely dates or author chronology.

## Layout and dependencies

Use `amsart` with `12pt,reqno`, A4 paper, a centered 6.1-inch text block, 1.2-inch top/bottom margins and 1.1 line spacing. The shared style prefers STIX2 and issues an explicit warning when it uses a fallback; Latin Modern is preferred when available. Optional microtype improves spacing. Theorem-like statements share a section-based counter and equations are numbered by section. Definitions, examples and Problems use upright text.

Display formulas according to mathematical role and length; number those that need reference. Prefer `align`, `aligned`, `gathered` or `cases` for structured expressions. Keep short incidental notation inline. Do not rely on global `\sloppy`, negative spacing, large `samepage` blocks or wholesale font reduction to hide defects. Check long formulas, citation spacing and numbering in the actual rendered pages; local issues call for local fixes unless a common defect is reproduced.

Keep `math-review.sty` beside the template entrypoints. They compile without additional input files or bibliography databases and intentionally contain visible `\placeholder` text. A TeX distribution must supply `amsart`, AMS packages, `mathtools`, `geometry`, `enumitem` and `hyperref`; STIX2, Latin Modern and microtype are optional. The templates support pdfLaTeX; actual projects record the engine they use. No personal font file is bundled.

Replace all insertion text, title/author/date markers and `\templatereferences` in a finished manuscript. Add only real sourced or justified claims and real bibliography entries. A successful scaffold build is not a completed mathematical review.
