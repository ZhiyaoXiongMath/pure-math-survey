# Length and selection

## Defaults are selections, not ten automatic volumes

A single-topic request selects V concise. An explicit five-part series or five-part suite selects I–V concise. End-to-end testing of a specified part preserves that selection. The ten templates are a catalog; standard and paired editions require a request. The manifest must explicitly record the selected documents, even though the legacy validator retains its ten-document compatibility fallback.

| Part | Concise total-page review limit | Standard total-page review limit |
|---|---:|---:|
| I | 5 | 8 |
| II | 6 | 10 |
| III | 6 | 10 |
| IV | 5 | 8 |
| V | 10 | 16 |

Count all pages, including references. These limits are review triggers, not content quotas or targets to fill. User limits override them. Never lower the 12-point font, narrow the baseline margins, remove a necessary assumption or use unexplained abbreviations to fit. An indispensable overrun requires a specific reason in `architecture.md`, an adjusted user-agreed limit or an explicitly disclosed editorial exception. The budget script reports an overrun; it does not silently bless a justification.

## Select before expanding

Write one sentence describing the reader's mathematical task for each requested part. Select the principal answers and the minimum definitions needed to understand them. Keep a completed mechanism or model where the part promises one. Identify genuine side branches before drafting; do not demote a missing principal answer after writing the body.

I: retain the objects, question and a completed model. II: retain exact result statements and substantive relations. III: retain the decisive derivations and the actual closure of selected routes. IV: retain the organizing problem, strongest relevant settled boundary and exact remaining target. V: retain an independent thematic argument rather than concatenate the other parts.

For short parts, omit a contents page, separate title page, generic motivation, paper-by-paper tours, duplicated prose paraphrases of formulas, and inventories at the end. State a useful consequence once, outside the main theorem. A reader should not have to read an internal audit card to learn mathematics.

## Two reading passes

**First-page pass.** The reader can identify the objects, central question, selected actual answers and controlling status. I–IV introductions normally occupy at most one page; V normally at most two. If a precise main statement requires more space, cut side branches, not its hypotheses.

**Body pass.** Each section supplies a definition, result, completed inference, explanatory model, boundary or precise sourced question. Remove sections that only announce later sections. Every promised proof has an identified endpoint; every imported theorem has the hypotheses needed at its point of use.

Run `scripts/check_reading_budget.py PROJECT` after compiling. Review rendered pages as well: an empty final page or four dense pages of uninterrupted theorem statements can fail the reading task despite passing a numerical budget.

## Scope is not a length-control variable

Remove ancillary branches, duplicated statements and dispensable comparisons before reducing the agreed question. Do not replace a general problem with its simplest special case without the user changing the scope. A standard edition adds depth where a decisive inference occurs, not a mandatory final depth section. A manuscript below its target does not need padding.
