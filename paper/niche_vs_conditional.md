# Niche overlap versus sign agreement — two different quantities, one of which predicts transfer

**What this is.** SDM's transferability instruments measure *where* presences sit in
environmental space (P(x|y=1) overlap); our conditional index measures *which way* the
feature–response relation points (P(y|x) direction). If the two were strongly correlated, the
conditional result would be a repackaged niche result. This analysis tests their distinctness at
pair level, gives supportive partial correlations, and packages the two-pair contrast that is the
paper's main figure. It also fixes the combined-table counts for the manuscript. Computed
2026-08-08 (environment and parquet sha256s recorded in the JSON).

**Result in one sentence: niche overlap and sign agreement are empirically distinct (pair-level
ρ between Schoener's D and the conditional indices ranges −0.36 to +0.45, all CIs spanning
zero), and when both are put against transfer, the conditional index retains its association
with niche overlap held fixed (partial ρ ≈ +0.82 [+0.40, +0.88]) while niche overlap retains
nothing with the conditional index held fixed (partial ρ ≈ −0.07 [−0.39, +0.37]).**

## Primary evidence — the two contrast pairs (logical, not statistical)

The load-bearing evidence is deliberately not a correlation. Two coexisting counterexamples
show niche overlap is **neither sufficient nor necessary** for transfer, independent of sample
size:

| | **Manavgat ~ Muğla** | **Bejís ~ Montiferru** |
|---|---|---|
| Schoener's D̄ (1D) | **0.826** — highest of all 10 pairs | **0.479** — lowest of all 10 pairs |
| Mahalanobis | 2.71 (closest) | 8.11 (farthest) |
| Sign agreement | 4/9; supported features 1/2, **elevation flips with support** | 7/9; no supported disagreement |
| Transfer | 0.470 [0.454, 0.486] and 0.401 [0.376, 0.426] — **both below chance** | 0.594 [0.558, 0.630] and 0.548 [0.521, 0.578] — **both above chance** |

Per-feature signed-AUC values with CIs for both pairs (the figure's underlying data) are in
`paper/figure_contrast_pairs.{csv,json}`: in Manavgat–Muğla the nine features' distributions
overlap heavily (per-feature D 0.72–0.92) while five of nine arrows point in opposite
directions (elevation, all four absolute thermal channels); in Bejís–Montiferru the
distributions barely overlap (per-feature D 0.30–0.68) while the arrows agree almost everywhere.
**Proposed reading for the Discussion: this is a measurable operationalisation of SDM's
"ecological stationarity" — stationarity is direction agreement in P(y|x), and it, not envelope
overlap, is what transfer requires.**

## Pair-level correlation between the two quantities (n = 10 / 8 pairs)

| Pair-level measures | n | Spearman ρ [95 % CI] |
|---|---|---|
| Schoener's D vs agreement fraction (supported) | 8 | +0.45 [−0.78, +0.90] |
| Schoener's D vs cosine (supported) | 8 | +0.31 [−0.88, +0.86] |
| Schoener's D vs cosine (all 9) | 10 | +0.01 [−0.73, +0.73] |
| Schoener's D vs agreement count (all 9) | 10 | −0.36 [−0.86, +0.30] |

No consistent association; the point estimates do not even share a sign. The two instruments
rank the ten pairs differently (rank data in the JSON's `pair_level_dataset`).

## Partial rank correlations with transfer — supportive only

Direction-level (n = 20 / 16), pair-resampled bootstrap; reported as a direction indicator, not
a test, per the pre-stated rule (effective n = 10/8 pairs):

| Partial | ρ [95 % CI] |
|---|---|
| **agreement fraction (supported) → transfer, D held fixed** | **+0.82 [+0.40, +0.88]** |
| Schoener's D → transfer, agreement fraction held fixed | −0.07 [−0.39, +0.37] |
| cosine₉ → transfer, D held fixed | +0.52 [−0.19, +0.83] |
| Schoener's D → transfer, cosine₉ held fixed | +0.28 [−0.36, +0.71] |

The asymmetry points one way: conditioning on niche overlap costs the conditional index nothing;
conditioning on the conditional index leaves niche overlap with nothing.

## Combined-table counts (the manuscript sentence)

From `all_diagnostics_vs_transfer.csv`: **20 diagnostic variants; 2 have bootstrap 95 % CIs
excluding zero (both conditional, P(y|x)); 17 span zero; 1 is not computable (supported-vector
Spearman, only one pair with ≥3 supported features).**

## Honest notes

- One pair breaks the raw agreement count while confirming the supported variant:
  Evia–Manavgat agrees on only 1/9 features yet transfers at 0.649/0.686 — but its single
  *supported* feature agrees (1/1). The noisy CI-crossing features dominate the raw count;
  this is the same lesson as Analysis 1 (restriction is necessary), now visible at pair level,
  and it is why "D vs agreement count" even goes negative.
- All caveats of the supported conditional index carry over: near-binary, tiny denominators,
  needs target labels, two Montiferru pairs undefined.
- Partial Spearman via the standard rank-correlation formula; with 10/8 effective pairs these
  are direction indicators only. The contrast pairs are the primary evidence by design.

## Files

- `paper/niche_vs_conditional.{json,csv}` — pair-level dataset, measure-vs-measure correlations,
  partials, combined-table counts.
- `paper/figure_contrast_pairs.{json,csv}` — per-feature signed AUCs + CIs for both contrast
  pairs, pair-level overlap/agreement/transfer summary (main-figure data).
- Script: `paper/niche_vs_conditional.mjs`.
