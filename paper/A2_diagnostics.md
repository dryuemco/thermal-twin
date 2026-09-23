# Appendix A. Where the rest of the appendices are

Two appendices are printed here: **Appendix B**, the diagnostic tables below, and **Appendix C.5**,
the thirteen limitations. They carry the per-direction numbers and the limitations against which the
claims are checked, so the paper can be assessed without leaving it.

**Appendix A and the protocol sections C.1 to C.4, C.6 and C.7 are released with the paper rather
than printed in it**, at `paper/supplementary_appendices.md` in the repository named in the
declarations. They keep their section names there, so a pointer such as Appendix A(c) or Appendix
C.2 in the text resolves in that document unchanged. Nothing in them is evidence a claim depends on
that appears nowhere else; every number in them also sits in a frozen artefact named in the text.
The lettering of this appendix is kept for that reason: renaming would have broken 148 references
between the paper, the supplementary appendices and the supplementary material.

# Appendix B. Supporting tables

These are the per-region and per-direction numbers the Results sections quote, given in full so that
every claim can be checked against the values it rests on rather than against a summary of them.

**Table B2. Signed univariate AUC of each predictor against `burned`, by region.** Primary
natural-vegetation population; 10-cell (~5 km) spatial-block bootstrap, 1000 replicates, seed 42.
The AUC is never folded to max(AUC, 1 − AUC), so a value below 0.5 means lower values rank burned
and is a direction rather than weakness. **Bold** marks a region whose own interval excludes 0.5.
Corrected Manavgat label; source `paper/labelfix_rerun/round5/tables/step9g_multi_aoi_feature_stability.csv`
(the pipeline's Step9G five-region synthesis, sha256 c864cd7d…), checked row by row by
`paper/code/appendix_tables.py`. Only the Manavgat column differs from the frozen table.

| Feature | Manavgat | Bejís | Muğla | Evia | Montiferru |
|---|---|---|---|---|---|
| `elevation_mean` | **0.232** [0.179, 0.288] | **0.643** [0.558, 0.729] | **0.611** [0.532, 0.690] | 0.541 [0.448, 0.626] | 0.584 [0.395, 0.762] |
| `slope_mean` | **0.400** [0.340, 0.459] | 0.521 [0.439, 0.605] | **0.637** [0.582, 0.686] | 0.487 [0.418, 0.554] | **0.652** [0.506, 0.771] |
| `ndvi_mean` | 0.564 [0.499, 0.628] | 0.559 [0.497, 0.619] | **0.662** [0.616, 0.704] | **0.639** [0.575, 0.701] | 0.586 [0.450, 0.704] |
| `lst_anomaly_mean` | 0.509 [0.460, 0.560] | **0.418** [0.364, 0.480] | 0.485 [0.395, 0.566] | **0.640** [0.567, 0.710] | 0.395 [0.285, 0.535] |
| `current_lst_mean` | **0.665** [0.608, 0.719] | 0.477 [0.401, 0.547] | **0.325** [0.271, 0.382] | **0.377** [0.301, 0.456] | 0.370 [0.248, 0.513] |
| `current_tvdi_mean` | **0.677** [0.622, 0.733] | 0.517 [0.429, 0.595] | **0.336** [0.275, 0.398] | **0.362** [0.285, 0.442] | **0.356** [0.233, 0.499] |
| `tvdi_difference_mean` | 0.460 [0.409, 0.510] | 0.512 [0.443, 0.583] | 0.490 [0.396, 0.575] | 0.519 [0.444, 0.589] | **0.378** [0.282, 0.497] |
| `downscaled_lst_mean` | **0.683** [0.626, 0.739] | 0.484 [0.400, 0.560] | **0.307** [0.253, 0.366] | **0.377** [0.297, 0.459] | 0.365 [0.240, 0.511] |
| `fused_lst_mean` | **0.666** [0.610, 0.721] | 0.481 [0.404, 0.551] | **0.325** [0.272, 0.383] | **0.376** [0.300, 0.456] | 0.370 [0.248, 0.513] |

**What counts as a reversal.** A pair of regions is called a reversal only when their signed
associations point to opposite sides of 0.5 **and each region's own interval excludes 0.5**. That is
stricter than requiring the two regions' intervals to be disjoint, and the difference matters: for
`current_lst_mean` between Manavgat and Bejís the two intervals are disjoint, [0.608, 0.719] against
[0.401, 0.547], but Bejís's own interval includes 0.5, so Bejís has no established direction to
reverse from. That pair is a point reversal, not a supported one.

**Table B3. The cross-region reversals that meet the stricter criterion.** Corrected Manavgat label.
The strict criterion is applied to Table B2's intervals. Difference intervals are the paired 10-cell
block bootstrap of `paper/code/ems_inference_multiplicity.py`
(`paper/labelfix_rerun/inference/reversal_family_holm.csv`, 1000 replicates), which flags the same
fourteen pairs. The frozen table's intervals came from `paper/signed_auc_bootstrap.mjs`, a different
resampling stream that differs from this one by at most 0.007 on the frozen data. Checked row by row
by `paper/code/appendix_tables.py`.

| Feature | Region A | AUC | Region B | AUC | Difference [95 % CI] |
|---|---|---:|---|---:|---|
| `elevation_mean` | Manavgat | 0.232 | Bejís | 0.643 | +0.411 [+0.312, +0.509] |
| `elevation_mean` | Manavgat | 0.232 | Muğla | 0.611 | +0.379 [+0.274, +0.476] |
| `slope_mean` | Manavgat | 0.400 | Muğla | 0.637 | +0.237 [+0.158, +0.313] |
| `slope_mean` | Manavgat | 0.400 | Montiferru | 0.652 | +0.252 [+0.100, +0.389] |
| `lst_anomaly_mean` | Bejís | 0.418 | Evia | 0.640 | +0.222 [+0.129, +0.316] |
| `current_lst_mean` | Muğla | 0.325 | Manavgat | 0.665 | +0.340 [+0.260, +0.413] |
| `current_lst_mean` | Evia | 0.377 | Manavgat | 0.665 | +0.288 [+0.195, +0.384] |
| `current_tvdi_mean` | Muğla | 0.336 | Manavgat | 0.677 | +0.341 [+0.253, +0.422] |
| `current_tvdi_mean` | Evia | 0.362 | Manavgat | 0.677 | +0.315 [+0.221, +0.413] |
| `current_tvdi_mean` | Montiferru | 0.356 | Manavgat | 0.677 | +0.322 [+0.161, +0.453] |
| `downscaled_lst_mean` | Muğla | 0.307 | Manavgat | 0.683 | +0.376 [+0.295, +0.451] |
| `downscaled_lst_mean` | Evia | 0.377 | Manavgat | 0.683 | +0.307 [+0.209, +0.405] |
| `fused_lst_mean` | Muğla | 0.325 | Manavgat | 0.666 | +0.341 [+0.261, +0.413] |
| `fused_lst_mean` | Evia | 0.376 | Manavgat | 0.666 | +0.291 [+0.198, +0.386] |

Fourteen pair-level reversals across **seven** features, thirteen of them involving Manavgat. Under
the frozen label there were three, across two features, elevation and the LST anomaly. Section 3.11
removes exactly those two, and that selection was fixed under the frozen label and is kept, not
re-selected (Section 4.6). Twenty-six further pairs reverse at the point estimate only, and they are
not counted. The frozen text gave twenty-nine for that count, but the frozen Step9G values give
thirty-three: a pre-existing count error, independent of the label. The conservative criterion costs
the paper findings rather than manufacturing them: a difference interval on the pair, which is the
instrument Appendix A(m) uses, would support seventeen further reversals.

## B4. The transfer matrix in precision-recall terms

ROC-AUC is reported throughout the main text for comparability with the susceptibility literature.
A susceptibility surface is used as a ranked area budget, so precision-recall is the operational
quantity, and at target prevalences of 7.0 to 28.7 % the two can differ sharply. Read from the step9b
exports of the re-frozen outputs (`paper/labelfix_rerun/round5/tables/corrected/*/step9b_metrics.json`).

**Table B4. Thermal transfer, PR-AUC against the no-skill baseline.** The baseline is the target's
burned prevalence. Lift is PR-AUC divided by that baseline; a lift of 1 is no better than random ranking. Ordered by lift.
Corrected Manavgat label. Checked row by row by `paper/code/appendix_tables.py`. Two frozen cells did not equal their source rounded to 3 dp,
Bejís → Muğla ROC-AUC (printed 0.619, source 0.6185) and Montiferru → Manavgat PR-AUC (printed 0.043,
source 0.0425): a pre-existing rounding error, independent of the label.

| Direction | ROC-AUC | PR-AUC | No-skill | Lift |
|---|---:|---:|---:|---:|
| Evia → Manavgat | 0.677 | 0.321 | 0.143 | **2.24** |
| Manavgat → Evia | 0.654 | 0.407 | 0.287 | 1.42 |
| Bejís → Montiferru | 0.594 | 0.289 | 0.212 | 1.36 |
| Evia → Montiferru | 0.647 | 0.283 | 0.212 | 1.34 |
| Bejís → Muğla | 0.618 | 0.093 | 0.070 | 1.33 |
| Muğla → Evia | 0.653 | 0.379 | 0.287 | 1.32 |
| Montiferru → Bejís | 0.548 | 0.093 | 0.072 | 1.28 |
| Montiferru → Muğla | 0.619 | 0.089 | 0.070 | 1.27 |
| Evia → Muğla | 0.577 | 0.086 | 0.070 | 1.23 |
| Muğla → Bejís | 0.583 | 0.088 | 0.072 | 1.22 |
| Manavgat → Montiferru | 0.518 | 0.243 | 0.212 | 1.15 |
| Montiferru → Evia | 0.586 | 0.317 | 0.287 | 1.11 |
| Muğla → Montiferru | 0.531 | 0.214 | 0.212 | 1.01 |
| Manavgat → Muğla | 0.438 | 0.060 | 0.070 | **0.85** |
| Evia → Bejís | 0.448 | 0.059 | 0.072 | **0.82** |
| Montiferru → Manavgat | 0.404 | 0.113 | 0.143 | **0.79** |
| Bejís → Evia | 0.383 | 0.226 | 0.287 | **0.79** |
| Manavgat → Bejís | 0.396 | 0.054 | 0.072 | **0.75** |
| Muğla → Manavgat | 0.345 | 0.101 | 0.143 | **0.70** |
| Bejís → Manavgat | 0.314 | 0.098 | 0.143 | **0.68** |
| **Mean** | **0.527** | **0.181** | **0.157** | **1.13** |

Seven directions fall below their own no-skill baseline, and only one exceeds twice it. The seven are
the same seven that are below chance on ROC-AUC, which is what a reversed ranking predicts in either
metric. Section 4.4 shows that this count is largely a property of the evaluation frames rather than
of a reversed predictor-burning relationship.

## B5. The same-geography event pair, in full

Appendix A(m) reports this arm and Section 4.4 withdraws its **elevation** reversal as a frame
artefact; Appendix A(o) explains why the thermal channels of this arm carry no verdict either way. The
per-feature values are kept here because the arm is what motivated the frame test, and because
its structural asymmetries have no analogue in the twenty-direction matrix.

**Table B5. Signed univariate feature-burned AUC, Muğla 2021 versus 2022.** Raw AUC against
`burned`, never folded to max(AUC, 1 − AUC); 10-cell (≈ 5 km) spatial-block bootstrap, 1,000
replicates, seed 42 (Section 3.14). Analysis population 41,730 rows / 2,911 burned (2021) and
38,790 rows / 331 burned (2022). **Positive-carrying 5 km blocks: 70 for the 2021 arm and 11 for the
2022 arm.** Table 1's note sets sixteen as the floor this design supports at that blocking, so the
2022 intervals here fall below the paper's own standard and are read as indicative, exactly as the
20-cell row of Table 1 is. The 2022 arm is additionally a single compact scar, so its eleven blocks
are contiguous. Read from
`paper/step9g_raw/.../mugla_2021__mugla_2022_event_relative/step9g_direction_reversal_table.csv`.

| Feature | 2021 AUC [95 % CI] | 2022 AUC [95 % CI] | Reversal |
|---|---|---|---|
| **elevation_mean** | **0.611 [0.532, 0.690]** | **0.296 [0.230, 0.355]** | **bootstrap-supported** |
| current_lst_mean | 0.325 [0.271, 0.382] | 0.515 [0.434, 0.580] | point only |
| current_tvdi_mean | 0.336 [0.275, 0.398] | 0.594 [0.475, 0.674] | point only |
| downscaled_lst_mean | 0.307 [0.253, 0.366] | 0.508 [0.435, 0.571] | point only |
| fused_lst_mean | 0.325 [0.272, 0.383] | 0.519 [0.436, 0.583] | point only |
| ndvi_mean | 0.662 [0.616, 0.704] | 0.707 [0.624, 0.777] | none |
| slope_mean | 0.637 [0.582, 0.686] | 0.558 [0.468, 0.634] | none |
| lst_anomaly_mean | 0.485 [0.395, 0.566] | 0.380 [0.249, 0.502] | none |
| tvdi_difference_mean | 0.490 [0.396, 0.575] | 0.397 [0.265, 0.514] | none |

## B6. The evaluation frames, and the signed associations they produce

Section 4.4 states these results; the per-region values are here.

**Table B6. Evaluation-frame geometry of the five study regions.** Primary natural-vegetation
population. Distance is Euclidean to the nearest burned cell on the 500 m grid, at 0.45 km per cell.
Corrected Manavgat label. Computed by `paper/code/appendix_tables.py` from the step8a tables (read
through `paper/code/_canonical.py`, which verifies each file's sha256), as
`paper/code/verify_aoi_frame.py` does; the frozen computation reproduces the frozen table exactly.

| Region | cells | burned | median distance to burned | share beyond 10 km |
|---|---:|---:|---:|---:|
| Manavgat | 20,511 | 2,935 | 13.1 km | **58.5 %** |
| Bejís | 15,190 | 1,100 | 13.5 km | **63.1 %** |
| Muğla | 41,730 | 2,911 | 11.3 km | 55.3 % |
| Evia | 9,298 | 2,664 | 8.0 km | 43.7 % |
| Montiferru | 2,544 | 539 | 2.7 km | **2.1 %** |

**Table B7. Signed univariate AUC, frame as drawn against a 10 km collar.** Point estimates; the
intervals that decide the reversal question are given in the text below and in
`collar_frame_bootstrap.csv` (10-cell blocks, 1000 replicates, seed 42). Signed and never folded to
max(AUC, 1 − AUC), so a value below 0.5 is a direction, not weakness. The collar drops no burned cells in any region. Corrected Manavgat label; full frame from Table B2's
source, collar from `paper/labelfix_rerun/code/aoi_frame_auc_frozen_mugla.csv`. Checked row by row by `paper/code/appendix_tables.py`. On the
corrected label Manavgat sits on the other side of 0.5 on every row, the collar rows included.

| Signed univariate AUC | Manavgat | Bejís | Muğla | Evia | Montiferru | straddles 0.5 |
|---|---:|---:|---:|---:|---:|---|
| elevation, full frame (Table B2) | **0.232** | 0.643 | 0.611 | 0.541 | 0.584 | **yes** |
| elevation, 10 km collar | **0.376** | 0.614 | 0.606 | 0.648 | 0.581 | **yes** |
| current LST, full frame | **0.665** | 0.477 | 0.325 | 0.377 | 0.370 | **yes** |
| current LST, 10 km collar | **0.522** | 0.405 | 0.332 | 0.286 | 0.376 | **yes** |
| current TVDI, full frame | **0.677** | 0.517 | 0.336 | 0.362 | 0.356 | **yes** |
| current TVDI, 10 km collar | **0.527** | 0.454 | 0.342 | 0.250 | 0.361 | **yes** |

**Table B8. Region summary: populations and gate outcomes.** Counts from each
region's Step 8A dataset statistics; gate fractions from each region's burned-landcover gate output.
TSG = the primary natural-vegetation population. The TSG columns use the canonical modelled
population, `burnable_tree_shrub_grass` **and** `valid_for_modeling == True`, which is the
population every model in this paper was fitted and scored on. Corrected Manavgat label. Counts are
computed from the step8a tables and gate fractions read from each region's gate output
(`paper/labelfix_rerun/round5/tables/corrected/gates/`). Checked row by row by `paper/code/appendix_tables.py`.

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 3,046 | 0.126 | 20,511 | 2,935 | 0.143 | 0.955 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,026 | 0.041 | 41,730 | 2,911 | 0.070 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,788 | 0.122 | 9,298 | 2,664 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 697 | 0.220 | 2,544 | 539 | 0.212 | 0.723 | pass |

**Table B9. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with 2-cell
spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise z-scoring (λ =
10⁻⁵). Updated 2026-09-23 for the corrected Manavgat label: the eight Manavgat rows are regenerated
by `paper/code/table_b9.py` from the re-frozen outputs, and the twelve others are unchanged. The same
script reproduces the frozen table exactly from `drive_new`.

| Direction | Raw | Region-wise z-score | CORAL |
|---|---|---|---|
| Manavgat→Bejís | 0.396 [0.373, 0.422] | 0.450 [0.423, 0.477] | 0.467 [0.441, 0.491] |
| Bejís→Manavgat | 0.314 [0.296, 0.332] | 0.302 [0.282, 0.323] | 0.406 [0.388, 0.423] |
| Manavgat→Muğla | 0.438 [0.418, 0.456] | 0.427 [0.408, 0.444] | 0.417 [0.398, 0.436] |
| Muğla→Manavgat | 0.345 [0.331, 0.359] | 0.485 [0.468, 0.502] | 0.476 [0.460, 0.493] |
| Manavgat→Evia | 0.654 [0.633, 0.676] | 0.529 [0.504, 0.553] | 0.504 [0.481, 0.528] |
| Evia→Manavgat | 0.677 [0.658, 0.697] | 0.404 [0.386, 0.421] | 0.417 [0.399, 0.435] |
| Bejís→Muğla | 0.618 [0.601, 0.635] | 0.518 [0.501, 0.535] | 0.507 [0.489, 0.524] |
| Muğla→Bejís | 0.583 [0.561, 0.607] | 0.535 [0.512, 0.557] | 0.560 [0.538, 0.581] |
| Bejís→Evia | 0.383 [0.363, 0.402] | 0.532 [0.509, 0.551] | 0.499 [0.479, 0.518] |
| Evia→Bejís | 0.448 [0.426, 0.470] | 0.549 [0.524, 0.575] | 0.549 [0.525, 0.573] |
| Muğla→Evia | 0.653 [0.636, 0.671] | 0.561 [0.543, 0.580] | 0.563 [0.545, 0.582] |
| Evia→Muğla | 0.577 [0.560, 0.593] | 0.501 [0.485, 0.518] | 0.530 [0.515, 0.546] |
| Montiferru→Manavgat | 0.404 [0.385, 0.422] | 0.388 [0.367, 0.408] | 0.436 [0.416, 0.456] |
| Manavgat→Montiferru | 0.518 [0.474, 0.563] | 0.527 [0.484, 0.568] | 0.505 [0.461, 0.547] |
| Montiferru→Bejís | 0.548 [0.521, 0.578] | 0.574 [0.552, 0.596] | 0.569 [0.548, 0.591] |
| Bejís→Montiferru | 0.594 [0.560, 0.631] | 0.550 [0.500, 0.601] | 0.574 [0.530, 0.621] |
| Montiferru→Muğla | 0.619 [0.604, 0.634] | 0.576 [0.562, 0.589] | 0.565 [0.550, 0.579] |
| Muğla→Montiferru | 0.531 [0.495, 0.568] | 0.587 [0.549, 0.624] | 0.584 [0.547, 0.623] |
| Montiferru→Evia | 0.586 [0.565, 0.606] | 0.630 [0.611, 0.649] | 0.624 [0.605, 0.641] |
| Evia→Montiferru | 0.647 [0.608, 0.682] | 0.568 [0.528, 0.609] | 0.581 [0.539, 0.623] |

