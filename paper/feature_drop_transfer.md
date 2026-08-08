# Dropping the direction-reversing features — does the concept-shift diagnosis yield a recipe?

**What this is.** Analysis 1 established two bootstrap-supported direction-reversing features:
`elevation_mean` (Manavgat vs Bejís, Manavgat vs Muğla) and `lst_anomaly_mean` (Bejís vs
Evia-extended). This analysis retrains the thermal transfer model in four configurations —
full (step9b reference), minus elevation, minus lst_anomaly, minus both — over all 20 ordered
directions and all five within-region CVs, to test whether removing the reversal carriers
converts the negative finding into an actionable feature-selection recipe. Computed 2026-08-08.

**Result in one sentence: there is no free lunch — dropping the reversal features trades
within-region skill (−0.06 to −0.08 mean AUC, bootstrap-supported in every region) for a
near-zero mean transfer gain (+0.005 to +0.014), because the same feature that reverses against
one partner is genuinely predictive toward the others; the gains concentrate exactly where the
reversal diagnosis says they should (Manavgat-involved directions +0.025 mean, up to +0.118),
and are cancelled by supported losses in the direction-aligned pairs.**

## Verification (all enforced as hard asserts; any deviation aborts)

- Full-config transfer AUC reproduces step9b **exactly (diff 0.0000)** in all 20 directions.
- Full-config within-region OOF AUC reproduces step8c TSG thermal **exactly (diff 0.0000)** in
  all five regions, by replicating repo `step8b` precisely: per-population training,
  `StratifiedGroupKFold(5, shuffle, random_state=42)` over 2-cell `spatial_block_id`, identical
  `ColumnTransformer` pipeline and feature order.
- Environment: scikit-learn 1.9.0 (see `sklearn_version_sensitivity.md` for why exact version
  parity is mandatory). Parquet sha256s match the step9b manifests (recorded in JSON).

## Trade-off table (the practical recipe view)

| Config | Mean within AUC (5 regions) | Mean transfer AUC (20 dirs) | Dirs >0.5 (point) | Dirs >0.5 (CI-supported) |
|---|---|---|---|---|
| full | **0.888** | 0.541 | 14 | 9 |
| drop elevation | 0.827 | 0.546 | 17 | 9 |
| drop lst_anomaly | 0.875 | 0.544 | 14 | 9 |
| drop both | 0.807 | **0.556** | 17 | **10** |

Dropping both reversal features buys +0.014 mean transfer and +1 CI-supported direction at the
price of −0.081 mean within-region AUC. The within cost is bootstrap-supported in **every**
region for elevation (delta CIs all below zero; largest Bejís −0.114 [−0.147, −0.079]) and in
4 of 5 regions for lst_anomaly (small, −0.002 to −0.035).

## Where the transfer deltas land (drop_elev; paired ~5 km-block bootstrap CIs)

**Supported gains (3):** Manavgat→Bejís **+0.118** [+0.048, +0.203], Evia→Bejís +0.075
[+0.023, +0.131], Montiferru→Manavgat +0.057 [+0.017, +0.092].
**Supported losses (5):** Evia→Manavgat −0.078 [−0.107, −0.040], Manavgat→Evia −0.071
[−0.122, −0.019], Muğla→Evia −0.038, Montiferru→Bejís −0.036, Muğla→Bejís −0.026.
Remaining 12 directions: CIs span zero.

**The Manavgat split confirms the mechanism.** Mean delta over the 8 Manavgat-involved
directions: **+0.025**; over the other 12: **−0.009**. Manavgat is the elevation dissenter
(signed AUC 0.374 vs 0.61–0.65 elsewhere), and removing elevation helps precisely the directions
that cross its reversal — most of all Manavgat→Bejís, the worst transfer in the matrix
(0.326 → 0.443). But where elevation's direction is shared and informative (both Evia↔Manavgat
directions ride on it; Muğla/Montiferru→Bejís use it), removal is a supported loss.

`drop_anom` behaves analogously but weakly, and pair-specifically: its only sizable supported
gain is Bejís→Evia (+0.046 alone; +0.063 [+0.026, +0.100] combined with elevation in
`drop_both`) — exactly the pair where `lst_anomaly` reverses with support. Isolating the two
features shows elevation carries nearly all of the `drop_both` effect; lst_anomaly's
contribution is confined to the Bejís–Evia pair.

## Honest reading

1. **As a universal recipe, feature-dropping fails**: mean transfer barely moves, CI-supported
   above-chance directions go 9 → 10, and the within cost is real and universal. The reversal
   features are not noise — they are locally genuine signal with locally opposite signs, which
   is the concept-shift diagnosis restated at the intervention level.
2. **As a targeted intervention, it works where — and only where — the diagnosis points**:
   drop the feature for direction-crossing pairs (Manavgat pairs for elevation, Bejís–Evia for
   lst_anomaly) and the worst transfers improve with bootstrap support. But knowing *which*
   pairs cross requires the target's signed direction — i.e. target labels — the same
   operational caveat as Analysis 1's diagnostic. Label-free application of the recipe would
   also destroy the five supported-loss directions.
3. This complements the adaptation story: z-score/CORAL compress indiscriminately; feature
   removal is the discrete analogue, and it shows the same conservation law — what transfer
   gains, the within-region model or the aligned pairs pay for.

## Files

- `paper/feature_drop_transfer.json` — metadata, parity evidence, all 20 transfer rows and
  5 within rows with per-config AUCs, deltas, paired CIs; trade-off summary.
- `paper/feature_drop_transfer.csv` — flat per-row table (transfer + within, all configs).
- Scripts: `paper/feature_drop.py`, `paper/feature_drop_merge.mjs`.
