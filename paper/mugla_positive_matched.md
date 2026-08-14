# Muğla matched to Manavgat on population size and positive count

The frozen `mugla_subsampling` diagnostic cuts Muğla to Manavgat's total cell count while preserving
prevalence, and states its own limitation plainly: "Prevalence is preserved, not equalised. Muğla's
positive count remains far above Manavgat's. Any residual difference between regions may still be a
positive-count difference, which this analysis does not separate."

That is the sharper test, because the variance of an ROC-AUC is dominated by the minority class.
Muğla carries 2,911 burned cells against Manavgat's 784, so matching only the total leaves Muğla with
roughly 3.7 times the positives. This arm matches both.

## Design

Ten seeded stratified draws from Muğla's primary population, each taking exactly 784 burned and
19,727 unburned cells, so every draw has Manavgat's population size **and** its positive count. The
pipeline's own `step8b` feature lists, model, folds and seed are used for the within-region arm; the
Muğla-as-source arms fit the same pipeline on the draw and apply it to each frozen target population
unchanged.

This is not the frozen diagnostic's sampling design and is not presented as one. The frozen design
allocates by an integer-exact Hamilton largest-remainder rule over 636 strata and inherits the
full-Muğla fold mapping; this is a plain stratified draw. What the two share is the question.

## Result

| Quantity | Full population | Matched median | Matched range over 10 draws | Reference position |
|---|---:|---:|---|---|
| Within-region ΔAUC | +0.1157 | +0.0978 | +0.0880 to +0.1048 | **above the range** |
| Muğla → Manavgat, thermal | 0.4010 | 0.3972 | 0.3754 to 0.4149 | inside |
| Muğla → Bejís, thermal | 0.5830 | 0.5763 | 0.5183 to 0.5941 | inside |

**Muğla's transfer behaviour does not depend on its positive count.** Both directions sit inside the
matched range, as they did under size-matching alone. The direction that fails keeps failing at about
0.40 and the direction that works keeps working at about 0.58, with Manavgat's own positive count in
the training set.

**Part of its within-region increment does.** Equalising the positives moves ΔAUC from +0.116 to a
median +0.098, and the full-population value lies above the matched range rather than inside it. So
roughly 0.018 of Muğla's increment is attributable to having more burned cells to learn from. The
remainder, about +0.098, is still among the larger increments in the cohort and still far above zero.

## Why this matters for the argument

Section 4.7j uses the subsampling to rule out the mundane explanation that Muğla behaves as it does
because it is bigger. Size-matching alone left a positive-count difference open; matching both closes
it for the transfer arms, which are the ones the argument rests on. The within-region arm is where
size does show through, and that is stated rather than smoothed over.

## Limits

1. Ten draws, and the range is a selection range over draws, not an uncertainty interval. No
   bootstrap and no probability statement.
2. The draw is unstratified by block, unlike the frozen design, so it does not preserve the spatial
   arrangement of positives as carefully. The consistency with the frozen size-matched result is
   reassuring on that point rather than proof.
3. The Muğla-as-target direction is not re-run here; the frozen diagnostic already found it
   insensitive, with all four combinations inside its range.

## Provenance

`paper/mugla_positive_matched.json`. Inputs are the frozen `step8a_500m_modeling_dataset.parquet`
files for Muğla, Manavgat and Bejís, and Muğla's frozen `step8b_model_comparison_metrics.json` for
the full-population reference; the transfer references are the thermal raw values of Table 4.
