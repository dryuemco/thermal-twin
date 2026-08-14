# Do the internally normalised dryness channels transfer better?

**Why this was run.** The introduction argues that an internally normalised index should be less
exposed to absolute-temperature offsets between regions than raw land surface temperature, and says
that the theoretical portability advantage "is tested here". It was not. An internal referee round
identified the gap twice over: once as an untested claim, and once as an opportunity, because the two
channels that do **not** reverse sign between regions are exactly the two normalised ones,
`lst_anomaly_mean` and `tvdi_difference_mean`, while the four absolute-surface-state channels are the
ones that do. If the normalised pair transferred materially better, the paper would carry a design
rule a modeller could act on: use anomaly-referenced dryness, not absolute surface state, if the
model has to travel.

It does not. The claim is now tested, and the answer is no.

Run 2026-08-14 on the harness that already reproduces the frozen exports. Script `anomaly_only.py`,
result `anomaly_only_transfer.json`.

## Design

Three feature sets were added to the existing four-configuration comparison, holding the classifier,
the population, the folds and the bootstrap fixed:

- `baseline_only` — the four baseline predictors alone.
- `anomaly_only` — baseline plus `lst_anomaly_mean` and `tvdi_difference_mean`.
- `absolute_only` — baseline plus `current_lst_mean`, `current_tvdi_mean`, `downscaled_lst_mean` and
  `fused_lst_mean`.

The harness aborts unless its reference configuration lands on the frozen numbers. It did, exactly:
the maximum absolute difference between the `full` arm and the frozen step9b transfer AUCs across all
twenty directions is **0.000000**, and the within-region arm reproduces step8c to four decimals in
all five regions. The contrast below is therefore computed beside a reference arm that is on the
published values, not near them.

## Result

| Feature set | Mean transfer AUC (20 directions) | Directions > 0.5 (point) | Mean within-region AUC |
|---|---:|---:|---:|
| baseline only | 0.5371 | 16 | 0.7896 |
| **baseline + normalised anomalies** | **0.5442** | 15 | 0.8551 |
| **baseline + absolute surface state** | **0.5479** | 13 | 0.8564 |
| all ten features (reference) | 0.5414 | 14 | 0.8883 |
| reversing predictors removed | 0.5556 | 17 | 0.8072 |

Per direction, `anomaly_only` minus `absolute_only` has a mean of **−0.0037**. It is positive in 12
of 20 directions and runs from −0.099 to +0.094.

## Reading

**The normalised channels do not transfer better.** They transfer very slightly worse at the mean,
and the per-direction difference is scattered on both sides of zero with a span an order of magnitude
larger than the mean. Nothing here supports a design rule favouring anomaly-referenced dryness for
portability.

**The two blocks are near-equivalent in both roles.** Within region they are indistinguishable, at
0.8551 and 0.8564, and each recovers most of the gap between the baseline's 0.7896 and the full
model's 0.8883. Across regions they are also indistinguishable, at 0.5442 and 0.5479. Whatever
separates them in sign stability (the absolute channels reverse and the normalised ones do not) does
not translate into transferable skill.

**The baseline arm is confirmed independently.** Its mean transfer of 0.5371 was recomputed here from
the modelling datasets, and it matches the 0.537 read from the frozen per-direction export. That is
an independent path to the control the transfer paper now reports.

**The finding this strengthens is the negative one.** Section 4.3 reports that the static baseline
transfers no better than the thermal model. This adds that neither thermal sub-block transfers better
than the other, and that none of the four feature sets clears a mean of 0.548 against a within-region
range of 0.79 to 0.89. Nothing in this feature space travels, and the sentence is not a rhetorical
flourish: four differently constituted predictor sets were tried and all four behave the same way
across regions while differing sharply within them.

## What this closes

The introduction's portability claim can now be stated honestly. The advantage was hypothesised, it
was tested, and it was not found. That is a stronger position than the previous text, which asserted
that the test had been carried out when it had not.

## Limits

The comparison is between two sub-blocks of one thermal set on one cohort. It does not test
normalised dryness indices in general, and it does not test a normalisation fitted differently, for
instance against a pooled multi-region reference rather than each region's own four baseline years.
The pooled-edge variant of TVDI reported in the companion paper is the nearest such test, and it also
leaves the disagreement between regions intact.
