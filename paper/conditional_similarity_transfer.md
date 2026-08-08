# Conditional similarity as a transfer predictor — the signed-AUC agreement index, formalised

**What this is.** The eight marginal diagnostics (predictor-space dissimilarity, AoA fractions,
climatic, geographic, domain-classifier AUC, two regime distances) all fail to order raw thermal
transfer (`regime_transfer_correlation.md`). Following Moreno-Torres et al. (2012), those are all
P(x)-side measures; this analysis tests the P(y|x) side — similarity of the *direction* of each
predictor's univariate relation to burning — as a formal rank predictor of transfer, with the same
pair-based bootstrap framework. Candidate set fixed in advance: sign-agreement count, signed-AUC
vector Spearman, signed-AUC cosine, each also in a variant restricted to features whose 95 % CI
excludes 0.5 in both regions of the pair. Computed 2026-08-08.

**Result in one sentence: the full-9-feature indices point the right way but their CIs span zero;
the CI-supported-features variants are the first diagnostics in the whole programme whose
bootstrap intervals exclude zero (agreement fraction ρ = 0.84 [0.58, 0.88]; cosine ρ = 0.81
[0.33, 0.88]) — with the honest caveats that the effective sample is 8 pairs, the restricted
index is nearly binary, and unlike the marginal measures it requires target labels.**

## Method

- **Signed AUC source:** Emrehan's five-region table
  `drive_new/diagnostics/multi_aoi_transfer_synthesis/bejis_2022__evia_2021_extended__manavgat_2021__montiferru_2021__mugla_2021/multi_aoi_feature_stability.csv`
  (sha256 `52a0b28e…`, full hash in the JSON), 9 features × 5 regions, TSG population, ~5 km
  spatial-block bootstrap CIs. Per-region values are identical in every pair row they appear in
  (enforced); agreement counts reproduce RESULTS_INVENTORY §5b.1 (7/9, 4/9, 4/9 — enforced);
  the supported-reversal set matches Emrehan's `reversal_status` flags exactly (enforced).
- **Vectors:** per region, the 9-dim vector of (signed AUC − 0.5).
- **Pair measures (symmetric):** (a) sign-agreement count 0–9; (b) Spearman between the two
  vectors; (c) cosine similarity. Restricted variants use only features whose CI excludes 0.5 in
  *both* regions (Emrehan's step9g support criterion); agreement is then reported as a fraction.
- **Transfer quantity:** raw thermal ROC-AUC, TSG, source-only RF, 20 ordered directions (step9b).
- **Correlation:** Spearman ρ and Kendall τ-b, pair-based bootstrap (10 unordered pairs resampled
  with replacement, both directions carried, 2000 replicates, seed 42, percentile 95 % CI) —
  identical framework, code and seed policy as the marginal-measure table.

## Per-pair conditional similarity

| Pair | Agree /9 | Vector ρ₉ | Cosine₉ | Supported n | Agree supported | Mean transfer AUC |
|---|---|---|---|---|---|---|
| Bejís–Manavgat | 4 | −0.02 | −0.26 | 1 | 0/1 | 0.385 |
| Manavgat–Muğla | 4 | −0.23 | −0.21 | 2 | 1/2 | 0.436 |
| Evia–Manavgat | 1 | −0.35 | −0.19 | 1 | 1/1 | 0.649 |
| Manavgat–Montiferru | 4 | −0.33 | −0.14 | 0 | — | 0.550 |
| Bejís–Muğla | 7 | +0.70 | +0.48 | 1 | 1/1 | 0.601 |
| Bejís–Evia | 6 | +0.17 | +0.13 | 1 | 0/1 | 0.415 |
| Bejís–Montiferru | 7 | +0.47 | +0.49 | 0 | — | 0.571 |
| Evia–Muğla | 6 | +0.62 | +0.81 | 5 | 5/5 | 0.615 |
| Montiferru–Muğla | 9 | +0.87 | +0.90 | 2 | 2/2 | 0.575 |
| Evia–Montiferru | 6 | +0.72 | +0.54 | 1 | 1/1 | 0.616 |

Bootstrap-supported reversals in the five-region set (both CIs exclude 0.5, opposite sides):
`elevation_mean` Manavgat↔Bejís and Manavgat↔Muğla; `lst_anomaly_mean` Bejís↔Evia-extended.
**Feature set for Analysis 3 config (iii): {elevation_mean, lst_anomaly_mean}.**

## Correlation with transfer — conditional vs marginal, one table

Marginal rows quoted from `regime_transfer_correlation.csv` (same framework, same seed policy).

| Diagnostic | Side | n dir | Spearman ρ [95 % CI] | Kendall τ-b [95 % CI] |
|---|---|---|---|---|
| **Agreement fraction, supported features** | **P(y·x)** | **16** | **+0.84 [+0.58, +0.88]** | **+0.71 [+0.50, +0.77]** |
| **Cosine, supported features** | **P(y·x)** | **16** | **+0.81 [+0.33, +0.88]** | **+0.67 [+0.31, +0.77]** |
| Cosine, all 9 features | P(y·x) | 20 | +0.50 [−0.17, +0.83] | +0.37 [−0.12, +0.69] |
| Vector Spearman, all 9 features | P(y·x) | 20 | +0.27 [−0.36, +0.77] | +0.20 [−0.29, +0.60] |
| Agreement count, all 9 features | P(y·x) | 20 | +0.18 [−0.40, +0.72] | +0.14 [−0.31, +0.58] |
| Vector Spearman, supported (needs ≥3 feats) | P(y·x) | 2 | not computable | — |
| Domain-classifier AUC | P(x) | 20 | −0.32 [−0.78, +0.33] | −0.24 [−0.63, +0.23] |
| Regime distance, log effN | — | 20 | +0.29 [−0.38, +0.74] | +0.20 [−0.30, +0.58] |
| Predictor-space mean dissimilarity | P(x) | 12 | −0.10 [−0.54, +0.43] | −0.03 [−0.44, +0.40] |
| Fraction inside weighted AoA | P(x) | 12 | +0.22 [−0.48, +0.59] | +0.09 [−0.35, +0.31] |
| Climatic distance | P(x) | 12 | +0.06 [−0.76, +0.79] | +0.03 [−0.64, +0.63] |
| Geographic distance | P(x) | 12 | −0.24 [−0.84, +0.73] | −0.16 [−0.71, +0.63] |

## Honest reading

1. **The only diagnostics in the entire programme whose intervals exclude zero are conditional.**
   Both CI-supported variants (agreement fraction, cosine) have bootstrap 95 % CIs entirely above
   zero; every marginal measure's interval spans zero. This is the marginal-vs-conditional
   contrast of POSITIONING §5, now with intervals on both sides.
2. **The full-9 variants do *not* clear the bar.** Cosine₉ is the best (+0.50) but its CI spans
   zero. The noisy, CI-crossing features (the four absolute LST channels are interval-uncertain
   in 3 of 5 regions) dilute the index — exactly the motivation for the pre-specified restricted
   variant, but the honest statement is "restriction was necessary, the raw index is not enough".
3. **Caveats that must ship with the headline.** (a) Effective sample: 8 pairs / 16 directions —
   the two Montiferru pairs with no supported features drop out (Montiferru's CIs are wide;
   539 burned cells). (b) The restricted index is nearly binary: 6 of 8 pairs have denominator 1
   or 2, so the result is close to "pairs with any supported-sign disagreement (0.385–0.436 AUC)
   versus pairs without (0.55–0.65)". Clean, but coarse; a different region set could easily
   move it. (c) The narrow CI on the agreement fraction reflects heavy ties under pair
   resampling, not high precision.
4. **This index is not label-free.** Signed AUCs require burned labels in *both* regions;
   as an operational pre-transfer tool it needs a labelled probe in the target (connects to the
   few-shot analysis). The marginal measures it beats are label-free. The fair claim is
   mechanistic: *the failure the marginal diagnostics cannot see is visible in the conditional
   structure* — not that we have a deployable label-free predictor.
5. Per the honesty rule, no measures beyond the six pre-specified candidates were computed.

## Files

- `paper/conditional_similarity_transfer.json` — metadata, provenance (source sha256), per-region
  signed AUC vectors, per-direction table, correlations with replicate counts, supported-reversal
  list, Analysis-3 feature set.
- `paper/conditional_similarity_transfer.csv` — correlation table, flat.
- Script: `paper/conditional_similarity.mjs`.
