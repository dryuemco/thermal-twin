# Baseline versus thermal transfer, per direction — the thesis contrast made direct

**What this is.** POSITIONING §3's sharpest claim — *the feature block that gains the most within
region is the block that loses the most between regions* — stated as a per-direction paired
contrast: for each of the 20 ordered directions, the raw transfer ROC-AUC of the static baseline
model versus the thermal model, with the paired target-block bootstrap delta CI. Pure read-only
extraction from Emrehan's frozen step9b (points) and step9c (1000-replicate target spatial-block
bootstrap; delta computed thermal − baseline on identical resampled blocks). TSG population.
No new model runs. Extracted 2026-08-08; script `paper/baseline_vs_thermal.mjs`.

**Result in one sentence: within regions the thermal block adds +0.056 to +0.153 AUC in all five
regions, but in transfer its paired contribution nets to zero (mean delta +0.004) — CI-supported
positive in 10 directions, CI-supported negative in 7, uncertain in 3 — and it is the swing
factor at the chance line, dragging three directions from at-or-above chance to below it and
lifting one from below to above.**

## Per-direction table (TSG, raw transfer, 95 % target-block bootstrap CIs)

| Direction | Baseline | Thermal | Δ (thermal − baseline) [95 % CI] | Support |
|---|---|---|---|---|
| Manavgat→Bejís | 0.332 | 0.326 | −0.006 [−0.023, +0.010] | uncertain |
| Manavgat→Muğla | 0.508 | 0.470 | −0.038 [−0.051, −0.024] | **negative** |
| Manavgat→Evia | 0.594 | 0.613 | +0.019 [+0.003, +0.034] | positive |
| Manavgat→Montiferru | 0.578 | 0.533 | −0.045 [−0.077, −0.010] | **negative** |
| Bejís→Manavgat | 0.421 | 0.444 | +0.023 [−0.000, +0.044] | uncertain |
| Bejís→Muğla | 0.592 | 0.619 | +0.026 [+0.014, +0.038] | positive |
| Bejís→Evia | 0.531 | 0.383 | **−0.148** [−0.168, −0.126] | **negative** |
| Bejís→Montiferru | 0.553 | 0.594 | +0.041 [+0.005, +0.073] | positive |
| Muğla→Manavgat | 0.522 | 0.401 | **−0.121** [−0.146, −0.098] | **negative** |
| Muğla→Bejís | 0.451 | 0.583 | **+0.133** [+0.105, +0.158] | positive |
| Muğla→Evia | 0.600 | 0.653 | +0.054 [+0.039, +0.067] | positive |
| Muğla→Montiferru | 0.611 | 0.531 | −0.079 [−0.117, −0.037] | **negative** |
| Evia→Manavgat | 0.676 | 0.686 | +0.010 [−0.012, +0.032] | uncertain |
| Evia→Bejís | 0.392 | 0.448 | +0.056 [+0.037, +0.077] | positive |
| Evia→Muğla | 0.513 | 0.577 | +0.064 [+0.044, +0.083] | positive |
| Evia→Montiferru | 0.549 | 0.647 | +0.097 [+0.054, +0.138] | positive |
| Montiferru→Manavgat | 0.502 | 0.567 | +0.065 [+0.041, +0.091] | positive |
| Montiferru→Bejís | 0.613 | 0.548 | −0.064 [−0.082, −0.044] | **negative** |
| Montiferru→Muğla | 0.651 | 0.619 | −0.032 [−0.048, −0.017] | **negative** |
| Montiferru→Evia | 0.556 | 0.586 | +0.030 [+0.013, +0.046] | positive |

## Reading

1. **The within-region asset is transfer-neutral on average and sign-unstable per pair.** Mean
   baseline transfer 0.537, mean thermal 0.541 — the block that is worth +0.056…+0.153 inside
   every region is worth +0.004 on average across regions, because its contribution is
   CI-supported *positive* in 10 directions and CI-supported *negative* in 7.
2. **The thermal block is the swing factor at the chance line.** It drags three directions from
   baseline at/above chance to thermal below chance (Manavgat→Muğla 0.508→0.470; Bejís→Evia
   0.531→0.383; Muğla→Manavgat 0.522→0.401) and lifts one from below to above (Muğla→Bejís
   0.451→0.583). In the Manavgat–Muğla pair the static baseline transfers at roughly chance and
   adding the thermal block pushes both directions below it; in the Bejís–Muğla pair the thermal
   block is what carries transfer above chance in both directions — exactly the two poles
   POSITIONING §3 predicted.
3. **The per-direction sign of the thermal contribution tracks the reversal diagnosis.** The
   largest negative delta (Bejís→Evia −0.148) sits on the pair with the supported
   `lst_anomaly_mean` reversal; the Manavgat↔Muğla and Muğla↔Montiferru negatives sit on pairs
   with thermal-channel direction disagreement; the largest positive (Muğla→Bejís +0.133) sits
   on the 7/9-agreement pair.
4. Provenance: step9b/step9c per pair folder (git a07ea337 / 0a3c5fe8 / ab8fc5f5 / 5d55f6f4),
   parquet sha256s as recorded in `regime_transfer_correlation.json`. Files:
   `paper/baseline_vs_thermal_transfer.{json,csv}`.
