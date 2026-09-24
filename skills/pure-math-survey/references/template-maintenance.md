# Template maintenance

## Three different reference levels

The ten files in `assets/templates/` are general-purpose, compilable writing scaffolds. Their two canonical statement slots illustrate wiring, not a minimum theorem count. Delete or change the environment to match the selected mathematical content; a historical problem or preprint claim must not become a theorem merely because the scaffold uses that environment.

The frozen `assets/reference-samples/dhym-v6/` is the unmodified 1.1.0 baseline. Preserve its hashes and provenance. It demonstrates full statements, canonical repetition, proof interfaces and the Thomas–Yau program, but its 21-page extent is not a concise-page model.

The `assets/reference-samples/dhym-compact/` adaptation is a narrow worked example of scope reduction. It is not an updated comprehensive dHYM literature review. Its README states what was omitted, why the main conclusion is still complete, and what remains a contextual rather than a selected proof commitment.

## What every general template must demonstrate

Use a label-free mathematical body in the preamble or a canonical component file. Put the selected principal statement in the Introduction. If a full body repetition helps, reuse the same body through `theoremrecall` and keep its original number. Do not introduce two independently editable copies or increment the theorem counter for a recall. A referenced statement alone does not discharge the introduction's reading contract.

Each template must contain its part-specific reader task, a concrete prompt for the actual output, an explicit selection/budget reminder, and distinct concise/standard explanation ambitions. Do not solve cross-part readability by requiring the reader to open another part.

For a real project, move shared mathematical statements to the existing canonical components and record their placements in `publication-map.csv`. Do not create a second introduction or knowledge registry. Bodies contain mathematics, source/status qualifications and necessary assumptions, not environment wrappers, labels or audit cards.

## Required maintenance sequence

After changing a rule, inspect all ten templates, the two-result fixture, the compact dHYM adaptation and affected reference instructions. Run all unit tests and the fourteen maintenance builds. Review representative rendered template pages and every page of the compact sample; inspect changed frozen-sample pages when the style changes. Then run a real topic through creation, source verification, writing, compilation, budget checking, semantic review, rendering, validation and clean-archive reconstruction.

Record what was actually run. A scaffolding build is not a new-topic test. A regex assertion is not a semantic judge. A source-level self-review is not an independent expert review. A correct-looking PDF does not validate a research proof.

The IV and V templates include an actual optional, canonically defined Problem environment in the Introduction. Delete it when the selected scope has no unresolved core target; it is not a Problem quota. Standard templates contain part-specific substantive depth sections, not merely a different title or page limit.
