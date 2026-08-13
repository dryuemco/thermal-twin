# House style for the manuscript

Set 2026-08-13. Applies to `00_abstract.md` through `06_conclusions.md`, `S1_few_shot_recovery.md`,
`highlights.md` and `figure_captions.tex`. It does not apply to drafting notes, DRAFT-NOTES comment
blocks, `STATUS.md`, `LITERATURE.md`, or the mail files, which are internal records.

## The rules

1. **No em dashes and no en dashes in prose.** Not `—`, not `–`. Use a full stop, a comma, a colon,
   or brackets instead. A dash almost always marks a sentence that should have been two sentences.
2. **Short, simple sentences.** Aim for a mean of about 15 words and keep the longest under about
   25. One idea per sentence.
3. **Passive voice where it reads naturally.** "Five regions were analysed", not "we analysed five
   regions". This is the normal register for a methods-heavy paper and it keeps the focus on the
   procedure rather than on the authors.
4. **Plain words.** Prefer the everyday word: *use* over *utilise*, *show* over *demonstrate*,
   *about* over *approximately*, *needs* over *necessitates*. Target roughly B1 reading level.
5. **Technical terms are exempt.** `spatially blocked cross-validation`, `bootstrap interval`,
   `covariate shift`, `concept shift`, `ROC-AUC`, `CORAL`, `conditional`, `marginal` and the like
   stay as they are. Simplifying them would lose the meaning, and the readership of *Ecological
   Informatics* expects them. Plain language is about sentence construction and general vocabulary,
   not about removing the vocabulary of the field.

## Number ranges

Rule 1 creates a question for ranges, which were previously written with an en dash
(`2017–2020`, `0.962–0.9999`).

- **In prose:** write `2017 to 2020`, `0.06 to 0.15`.
- **In tables and in bracketed confidence intervals:** a hyphen or `to` is used, because
  `[+0.055, +0.078]` and column widths do not tolerate the longer form. Table cells are data, not
  prose.

## Why this is not a loosening of standards

Nothing about this rule changes a number, a claim, or a hedge. Where the draft says an interval
excludes zero, or that a reversal is point-level only and not bootstrap-supported, that precision
is kept word for word. Plain sentences make those distinctions easier to see, not easier to blur.
If a simplification would soften a claim, the claim wins and the sentence stays as it is.

## Checking

`node paper/tex/check_style.mjs` reports, per file: dash count, sentence-length distribution, and
the longest sentences. It is a report, not a gate. Judgement still applies.
