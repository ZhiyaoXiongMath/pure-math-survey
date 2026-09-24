# English mathematical exposition and typesetting

Use English research-level prose in every requested manuscript. Templates are scaffolds, not finished text. Replace their insertion text, metadata and functional titles with mathematics. These writing rules apply to all parts and editions and override generic narrative, transition or deduplication preferences.

## Mathematical structure without compulsory narrative

Make the central question and selected answers clear. State the setting and the definitions needed to understand them. An introduction may consist of definitions followed by principal theorems, with only the sentences needed to interpret the mathematics. This is a complete introduction, not a defect to repair with narrative.

Use a substantive transition only when it supplies information: a change of objects, a nontrivial implication, the need for a hypothesis or the reason two results differ. Apply the deletion test: if removing a transition loses no mathematical information and causes no reading break, delete it. Sentences merely announcing the next heading or saying that results are important are reading burden. A section may open immediately with a definition, display, statement or proof step.

Do not confuse trivial editorial transitions with necessary mathematical reasoning. State and justify a real implication, construction or change of setting even when the proof is short. Use a formula or compact inference where that is sufficient. Do not fabricate a thematic connection among results that are only adjacent in the literature.

Group local lemmas, calculations and variants under the mathematical tasks they serve. File sharing and `\input` boundaries do not determine printed hierarchy. A definition-and-theorem introduction still selects and orders material by a coherent mathematical question; it is not an unscreened catalog of papers. Section roadmaps and explanatory lead-ins are optional, not quotas.

The abstract briefly identifies the subject and principal content. The introduction makes the question and main statements readable. The contents provides navigation. Keep audit procedures out of all three. Place `abstract` before `\maketitle` in `amsart`; use verified author/date metadata. Each independently readable part has its own necessary setting, not a copied project description.

## Compact and self-contained statements

State explicit objects, indispensable assumptions, quantifiers, parameter ranges and the core conclusion. Define specialized notation locally or in a clearly identified definition within the same document. Repeating a short setting or needed definition is preferable to forcing the reader through a chain of references. Do not use unexplained phrases such as "under the assumptions above" to make a theorem appear short.

Use `itemize` for separable mathematical hypotheses and `enumerate` for conditions that will be referenced, alternative cases or an equivalence. Introduce their logical relationship explicitly: "Assume all of the following", "Assume at least one of the following", or "The following are equivalent". Use formulas inside items when clearer. Split long sentences; keep each item a complete condition with its quantifiers and dependencies. Do not force a single simple hypothesis into a list or prescribe a number of items.

Put the essential answer in the theorem, not a miscellaneous collection of its by-products. Immediate estimates, examples, specializations, explanations and secondary consequences normally follow in the surrounding prose or displays, with the needed hypotheses and proof or citation. Use a separate corollary or proposition for a substantial independent result. Never move a hypothesis or qualification essential to the main conclusion outside the theorem merely to shorten it.

An equivalence, classification, existence-and-uniqueness statement or other logically unified conclusion may need several clauses. Keep that main structure together. Do not split a result mechanically into one sentence per theorem; distinguish substantive unity from unrelated additions. A shorter independent claim obtained by splitting a bundled canonical result needs its own correctly related node and support; do not silently discard a registered conclusion.

Cite the controlling source and precise theorem, lemma, section or formula where available. Preserve material version qualifications and uncertainty beside the claim. Do not put proof sketches, history, comparison essays or audit records inside the statement. A nearby explanation cannot broaden its logical force. Verify convention translations before claiming an implication or equivalence.

## Useful repetition and canonical reuse

Repetition is allowed when it improves self-contained reading. An introduction and a distant proof section may both state the same result. Repeating hypotheses at their point of use or across independently readable parts is legitimate. The criterion is reader effort and mathematical clarity, not a similarity score or a blanket ban on complete restatements.

Remove an adjacent prose duplicate when it merely translates the entire theorem into words and adds nothing. Retain a needed recall even when it repeats the full statement. There is no mandatory explanatory paragraph before or after every theorem. After a theorem, give an actual consequence, comparison or proof idea, or proceed directly to the next mathematical object.

Maintain one canonical mathematical body for each shared full statement. The publication map records its primary semantic label in each requested document. That same body may be input again for a useful local recall; the primary label still occurs once. Do not make independent copies that can drift or repeat labels in a canonical body. Use `theoremrecall` for an unnumbered recall of a theorem by its original label; see the [examples](exposition-examples.md). For other statement kinds, use a corresponding local recall wrapper or a precise local reference with the needed assumptions. Mapped omissions and reference-only placements still cannot input the body.

## Formulas, lists and sentence length

Prefer a mathematical formula to a long verbal description of an inequality, domain, range, implication, equivalence, dependence or variational problem. Define the objects and explain only what is not already clear from the formula. Keep short incidental notation inline; use displays for central conditions and conclusions. Do not impose an equation count, prose quota or fixed sentence length.

Use `align`, `aligned`, `gathered` or `cases` for structured expressions. An implication chain must contain valid arrows with the relevant assumptions, proof or citation. A list of desired arrows is not an argument. Distinguish logical equivalence from isomorphism, equality and analogy. Do not compress a genuine gap into notation or introduce opaque shorthand just to reduce words.

Prefer short complete sentences and shallow lists over nested subordinate clauses. Use enumerated steps when they clarify a proof's dependencies; do not reduce the proof to unexplained slogans. Lists are especially useful for parallel conditions, cases and comparisons. Keep mathematical punctuation and logical connectives, and avoid deeply nested lists or a list item for every ordinary sentence.

## Part V and editorial freedom

V is a thematic review with its own selected central question. It may write directly from shared research or adapt I–IV without requiring their prior production. Supply the background, necessary language, selected main results, method ideas and Problems needed for its own scope. Its introduction may use definitions and theorems directly.

Use one notation system, contents, numbering and bibliography. Reuse canonical statements, with useful local recalls allowed; reorganize prose freely. New synthetic claims need support. Concise selects a short complete thread, merges local sections and omits side branches, not hypotheses. Standard deepens relevant comparisons, key ideas or frontier progress, not verbal padding or an automatic import of III's proofs or I's foundations course.

At the promised depth, explain what an idea does and how it supports the conclusion. A short formula-based argument may be sufficient. A list of method names is not. State usable external inputs precisely and check their hypotheses. Label sketches, cited inputs and review-derived reconstructions honestly.

## Problems and their discussion

Use the numbered and labelled `problem` environment for core unresolved targets, with upright body text:

```latex
\begin{problem}
\label{prob:descriptive-name}
% Precise objects, hypotheses, quantifiers and unresolved target.
% Use itemize or enumerate when it clarifies the conditions.
\end{problem}
```

Keep the target concise and self-contained; use `Problem~\ref{prob:descriptive-name}` to refer to it. For a mapped statement, put the wrapper and label outside its body-only canonical input. Give formulation source, cutoff status, importance, verified progress and precise remaining scope afterward, using formulas for parameter ranges. Do not force an obstacle or strategy for every Problem or repeat the entire target in its discussion.

Substantively different Problems need distinct statements; related subquestions may stay together. IV covers its agreed core frontier, while V selects what its own thread needs. Preserve shared assumptions, sources and status. Distinguish sourced Problems from review-proposed directions. An explicitly verified settled scope is preferable to an invented open question.

## Applications, sources and evidence

Give examples a mathematical purpose and enough verification to support it. Failure of an assumption is not failure of a conclusion; failure of one proof is not impossibility. Distinguish counterexamples, open ranges, scope exclusions and evidence gaps.

Keep citations with the relevant claims. Historical explanation needs sources, not just dates or chronology. Detailed retrieval and audit records belong in the rebuildable bundle, not theorem bodies or a compulsory narrative. Include a short source/version appendix only when it helps explain the mathematics.

## Layout and dependencies

Use `amsart` with `12pt,reqno`, A4 paper, a centered 6.1-inch text block, 1.2-inch top/bottom margins and 1.1 line spacing. The shared style prefers STIX2 and warns when a fallback is used; Latin Modern is preferred when available. Microtype is optional. Theorem-like statements share a section-based counter and equations are numbered by section. Definitions, examples and Problems have upright bodies. `itemize` and `enumerate` are provided through `enumitem`.

Number formulas that need reference. Do not hide overflow with global `\sloppy`, negative spacing, large `samepage` blocks, wholesale font reduction or cramped lists. Inspect actual rendered formulas, theorem/list boundaries, citation spacing and numbering. Fix local defects locally. Read notation after macro expansion: a definition must not accidentally print the same expanded expression on both sides. Legitimate identities are not forbidden.

Keep `math-review.sty` beside template entrypoints. They compile without other inputs or bibliography databases and intentionally contain visible `\placeholder` text. The TeX distribution must supply `amsart`, AMS packages, `mathtools`, `geometry`, `enumitem`, `needspace` and `hyperref`; STIX2, Latin Modern and microtype are optional. Templates support pdfLaTeX; actual projects record their engine. No personal font is bundled.

Replace insertion text, title/author/date markers and `\templatereferences` before publication. Use real, verified or justified mathematics and bibliography entries. A successful scaffold build is not a completed survey. See [validation](validation.md) for the substantive writing reread; a parser cannot certify clarity.

## Introduction as mathematical knowledge

Narrative is optional; selected principal conclusions are required. State the actual mathematical content, not an author list, topic list, table of contents or future-tense promise. For each selected principal conclusion give its objects, fixed data, necessary conditions, quantifiers, parameter/branch range, actual conclusion and material source status. Define specialized notation locally. A later-section reference is for deeper reading, not for recovering missing conditions.

A compact full statement is preferred. An explicitly delimited precise special case can be used when the general language would obscure the selected thread; it must not hide a range that is itself central. Separate proof details and secondary consequences, not essential hypotheses or logical force. Full repeated statements use the same label-free canonical body and original-number recall. A single-file export can assemble a body-only macro from that source; the mapped project still retains its canonical source files for validation and rebuilding.

Read only the introduction first. Then read the body for missing principal conclusions. Preserve the results of both tests in existing evidence, not a theorem-count score. An introduction containing one impeccable theorem can still fail by omitting another independent main thread.

## Logical dependency and first use

Introduce data and definitions before the equations and statements that use them. A structural identity that supplies the mathematical reason for an equation precedes that equation. Not every subject requires an equation, and a valid dependency order need not be unique. Do not turn the dependency principle into a rigid paragraph template.

At first use of a principal equation, specify fixed data, unknowns, their spaces and the relevant normalization, branch or positivity conditions. Distinguish changing a representative in a fixed class from changing the class. Specialized definitions for one result group can be placed near that group rather than front-loading a textbook.

An explanation must give a definition, quantifier, deduction, restriction, meaningful comparison or actual interface. “This provides a link” without the link does not qualify. Complete it mathematically or remove it. Use the deletion test on ordinary prose; never remove a necessary inference merely because it is short.

## Statement titles and attribution

Do not invent descriptive optional titles for theorem-like environments, definitions, Problems or conjectures. Use a plain numbered environment and a semantic label. Verified author attribution and established eponymous names are allowed with the source; a historical name such as Thomas--Yau is not an invented title. Mathematical section headings remain useful. Do not remove citations or labels when removing an invented name.

For example, write `\begin{theorem}` or a verified author/source optional argument, not a newly coined title. The same rule applies in templates, smoke fixtures and reference instructions. Keep standard concepts defined in the body.

## V benchmark and actual pages

Read [the Part V benchmark](part-v-benchmark.md) and use [the layout profile](layout-and-build.md). Both V editions need developed mathematical content as well as v6-level presentation. Finished formulas, statement lists, references and page breaks are part of delivery. A short method explanation is adequate only when the necessary input/output interface is really supplied; do not use the absence of a full-proof obligation to justify an empty mechanism account.
