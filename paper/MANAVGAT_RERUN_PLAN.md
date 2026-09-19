# Manavgat label correction: re-run plan

Written 2026-09-19. This is a read-only audit: nothing was run and nothing else was edited. It covers
Paper 1 in `paper/`: 00–06, A2, A3, the supplementary appendices, S1, the highlights, the figure
captions and figures.

## What changes

The frozen Manavgat label drops every burn dated DOY 209–212 (28–31 July 2021). This is the
`filterDate` month-boundary defect documented in `step6_validate_fire_relation.py`. The corrected
counts come from `ems_analyses/labels/r5_manavgat_labelwindow.json`:

| Cell set | Burned, frozen | Burned, corrected | Cells gained | Cells lost |
|---|---:|---:|---:|---:|
| All cells | 796 | 3,046 | 2,250 | 0 |
| TSG (primary population) | 784 | 2,935 | 2,151 | 0 |

Consequences:

- **The population is fixed.** `valid_for_modeling`, `analysis_eligible` and `burnable_*` do not depend on the label, so no cell enters or leaves.
- **TSG prevalence rises from 0.038 to about 0.143**, and all-valid prevalence from 0.033 to about 0.126.
- **The label window is unchanged** (2021-07-28 to 08-31). DOY 209 is 28 July, so every gained burn falls inside the window.

### Scope rule

A quantity depends on Manavgat if any of these holds:

- Manavgat is its region.
- Manavgat is a source or target of any transfer direction.
- It is a mean, count, range, correlation or interval over a set that contains any such value.
- It was fitted on a pool that contains Manavgat. This covers LORO, `d_per_source` and row D of Table 2.
- It depends on cross-region global binning or PCA. This covers niche overlap, which bins and runs a PCA over all five regions' burned cells.

### Classes

| Class | Meaning |
|---|---|
| A | A `paper/code/*.py` or `ems_*` script that reads through `_canonical`. It can be re-run once `_canonical` accepts the corrected table (§3.0). |
| A-stg | A paper-root harness: `feature_drop.py`, `loro_pooled.py`, `niche_overlap.py`, `scar_control.py`, `matched_holdout.py`, root `anomaly_only.py`. It reads `{STAGING}/{region}.parquet` and `{STAGING}/comparison_inputs.json`, not `_canonical`. It re-runs as easily as A, once the staging directory is rebuilt. |
| A-s10 | Our own `thermal-twin/step10/` code. It reads through `config10.REGIONS`, not `_canonical`. |
| B | Derived from the pipeline (drive_new). It must be recomputed by running `repo/` code on a staging tree (§3). |
| B→M | A B output read through a paper-side `.mjs` aggregator. The aggregator is re-run after B (§2). |
| C | A figure. |
| D | A text statement whose number, range endpoint, count or verdict depends on an A or B quantity. |

---

## 1. Inventory

The Location column uses these short codes:

| Code | File |
|---|---|
| Abs | `00_abstract.md` |
| HL | `highlights.md` |
| 1–6 | `01_introduction.md` … `06_conclusions.md` |
| B | `A2_diagnostics.md` (Appendix B) |
| C5 | `A3_protocol.md` |
| Supp | `supplementary_appendices.md` |
| S1 | `S1_few_shot_recovery.md` |
| Cap | `figure_captions.tex` |

"(Man)" marks a range whose endpoint or member is a Manavgat value.

### 1.1 Abstract, highlights, introduction, conclusions

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 1 | Frame cost 0.143 ROC-AUC [+0.077, +0.208] (model held fixed, region-wide vs scar + 2 km) | Abs; HL1; 1.3; 4.3; Supp A(z); 6; graphical abstract | `matched_holdout.json` (rows A−B) | `code/verify_matched.py` (= root `matched_holdout.py`) | A |
| 2 | "negative pool, not prevalence: +0.155 against −0.000" | HL2; 4.3; Supp A(i) Table A4, A(z) | `prevalence_control.json` | `code/prevalence_control.py` | A |
| 3 | Equalised mean transfer 0.541 → 0.616 | Abs; HL4; 6; 4.4 Table 3 | `aoi_frame_transfer_frozen_mugla.csv` | `code/regen_transfer_ci.py` (+ `frozen_mugla_verify_aoi_transfer.py`) | A |
| 4 | Within-region increment "+0.045 to +0.148 at 5 km blocking" (Man +0.050 inside the range) | Abs | Table 1, block-10 rows | step8 big-block / large-block robustness | B |
| 5 | "+0.06 to +0.15 AUC in five regions" under blocked CV (1 km) | HL3 | step8c (Table 1, block 2) | step8b→8c | B |
| 6 | Thermal gain across 20 directions +0.004 [−0.028, +0.036] | Abs; HL5; 4.3; 4.5; Supp A(o), A(z); graphical abstract | Point: `baseline_vs_thermal_transfer.csv`. Interval: `transfer_delta_ci.json` (formerly `referee2_numbers.mjs` block A) | Point: step9b/9c → `baseline_vs_thermal.mjs`. Interval: `code/transfer_delta_ci.py` | B→M + A |
| 7 | Static baseline 0.537 against 0.541 | Abs; 4.5; 5.2; 5.5; Supp A(ix), A(f) | `baseline_vs_thermal_transfer.csv` (cross-checked by the `anomaly_only` baseline arm, 0.5371) | step9b → `baseline_vs_thermal.mjs` | B→M |
| 8 | "withdraws five claims"; "falls 0.155 short" | 1.3; 5.1; 6 | Rows 45 and 54 | — | D |
| 9 | "they transfer no better than the absolute ones" (A(f)) | 1.2 | `no_coord_channels.json` / `anomaly_only_transfer.json` | `code/anomaly_only.py` | D |
| 10 | "hotter pre-fire surfaces burned less in every region"; "holding temperature reverses greenness in two regions" | 6; 4.4; Supp A(k), A(o), A(w) | `matched_frame_gap.csv`, `collar_frame_bootstrap.csv` | `code/verify_matched_gap.py`, `code/verify_collar_ci.py` | A |
| 11 | "leaves no sign reversal supported between regions" | 6; 4.4 | `collar_frame_bootstrap.csv` | `code/verify_collar_ci.py` | A |
| 12 | "reduces the directions below chance" (6 → 1) | 6; 4.4 | Table 3 | as row 3 | D |

### 1.2 Methods

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 13 | Pre-label exclusion "none arising in Manavgat or Bejís"; C.1 "recorded as not run for Manavgat" | 3.2; Supp C.1 | `referee2_numbers.json` G; `ems_analyses/labels/r1_prelabel.json` | step8a pre-label; `ems_labels_1_prelabel.py` | D (verify only; the correction adds only in-window days) |
| 14 | Positive-carrying block counts "192 to 843" (2 cells), "16 to 70" (10), "6 to 33" (20). Man is now 235 / 28 / 12 and may become an endpoint | 3.7; 4.2 Table 1 note; 4.2 | `referee2_numbers.md` §C | `referee2_numbers.mjs` over step9b prediction tables (or recompute from the table) | B→M |
| 15 | λ sweep "nine values on four directions … at most 0.014"; λ = 1 outside the sweep | 3.9; Supp A(b) | `drive_new/diagnostics/coral_lambda_sensitivity/…` (directions Bej–Muğ and Man–Muğ) | `repo/src/coral_lambda_sensitivity.py` | B |
| 16 | "twenty transfer directions to within 1.6×10⁻⁷" (step10 environment vs pipeline) | 3.13; Supp C.6 | reproduction check | step10/step9b re-comparison | D (redo the check) |
| 17 | "Two of the twenty transfer verdicts are not stable across seeds" | 3.13; 4.5 | `transfer_ci_blocksize.csv/json` | `transfer_ci_blocksize.mjs` over step9b predictions | B→M |

### 1.3 Results §4.1–4.2 and Table 1

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 18 | Gate: admitted regions "0.723 to 0.991" (Man 0.984 inside) | 4.1 | Man `validation/labels/burned_landcover_gate.json` | step6b (via `run_label_gate_only.py`) | B / D |
| 19 | Table 1 Manavgat, block 2: 0.803 / 0.870 / +0.067 [+0.055, +0.079] | 4.2 | `experiments/manavgat_2021/step8c/step8c_bootstrap_metrics.json` | step8b → step8c | B |
| 20 | Table 1 Manavgat, block 10: 0.748 / 0.797 / +0.050 [+0.023, +0.077] | 4.2 | `…/manavgat_2021/robustness/step8_big_blocks_v2/block_10_cells` | `step8_big_block_robustness.py` (v2) | B |
| 21 | Table 1 Manavgat, block 20: 0.683 / 0.731 / +0.048 [+0.014, +0.085] | 4.2 | `…block_20_cells` | same | B |
| 22 | "at 10 km … from +0.048 to +0.154" (Man is the lower endpoint); "interval excluding zero in all five at 1 km and 5 km" | 4.2 | rows 19–21 | — | D |
| 23 | Fig. 3 (Manavgat markers in panels a–c); caption "every interval excludes zero", "6 to 33 positive-carrying blocks" | Fig. 3; Cap | `figures/data/fig_data.json` `fig34` | `extract_fig_data.mjs` → `fig3_within_robustness.py` | C |

### 1.4 Results §4.3 (Table 2 and the controls)

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 24 | Table 2 rows A 0.776 [0.738, 0.814], B 0.634, C 0.552, D 0.555, with CIs. Every scar's row D includes a Manavgat foreign model; the Manavgat scar is one of the eight | 4.3 | `matched_holdout.json` | `code/verify_matched.py` | A |
| 25 | A−C 0.225 [+0.157, +0.293]; "about two thirds"; region-clustered +0.155 [+0.082, +0.228] and +0.251 [+0.093, +0.409]; "2.3 times wider" | 4.3; Supp A(z) | `matched_holdout.json` | same | A |
| 26 | B−C +0.082 [−0.011, +0.175]; C−D −0.003 [−0.075, +0.069]; "bound it at about 0.18" | 4.3; Supp A(u), A(z) | same | same | A / D |
| 27 | Scar counts: "eight scars", "nine" (controls), "four in Muğla, two in Montiferru", "three of them starved"; Manavgat has 1 component ≥ 50 cells with 88 source positives left. **The component structure may change with 2,151 added cells**, which could add Manavgat scars and change N | 4.3; Supp A(i), A(u), A(z) | `matched_holdout.json`, `scar_control.json` | `verify_matched.py`, root `scar_control.py` | A / D |
| 28 | Prevalence control 0.782 / 0.782 / 0.627; A−A′ −0.000 [−0.003, +0.002]; A′−B +0.155 [+0.093, +0.217] | 4.3; Supp A(i) Table A4, A(z) | `prevalence_control.json` | `code/prevalence_control.py` | A |
| 29 | Negatives-only 0.147 [0.104, 0.191]; positives-only 0.002 [−0.052, +0.048], per-scar −0.12 to +0.12 | 4.3 | `pool_decomposition.json` | `code/pool_decomposition.py` | A |
| 30 | "+0.027 on a within-region half-split" (13 of 18) | 4.3; Supp A(z) | `positive_control.json` | `code/positive_control.py` | A |
| 31 | LOSO increment +0.022 [−0.032, +0.077] | 4.3; Supp A(z); graphical abstract | `scar_increment.json` | `code/scar_increment.py` | A |
| 32 | "+0.056 to +0.153 under blocked CV" (Man +0.067 inside the range); "falls monotonically" | 4.3; Supp A(z) | step8c | step8b → 8c | B / D |
| 33 | Distances "306 to 2,802 km" | 4.3 | geodesic distances between AOIs | — | independent (listed in §4) |

### 1.5 Results §4.4 and Table 3

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 34 | Far-field share "2.1 % to 63.1 %"; Manavgat 60.1 %, median 13.4 km (Table B6) | 4.4; B6; Supp A(o), A(w) | `aoi_frame_auc.csv` | `code/verify_aoi_frame.py` | A |
| 35 | Manavgat elevation by distance band: 472 m (0–5 km), 955 m, 1,273 m; burned cells 512 m | 4.4; Supp A(o), A(w) | `verify_aoi_frame.py` stdout (`aoi_frame_artefact.md`) | `code/verify_aoi_frame.py` | A |
| 36 | "all five agree in sign on elevation, LST, TVDI"; "both elevation reversals disappear"; "no reversal bootstrap-supported"; "Evia's by 0.003" | 4.4; Supp A(w) | `collar_frame_bootstrap.csv`, `aoi_frame_auc_frozen_mugla.csv` | `code/verify_collar_ci.py`, `code/frozen_mugla_verify_aoi_frame.py` | A |
| 37 | Difference instrument: "four opposite-sided pairs on lst_anomaly_mean" (Man vs Evia is one of them); "nine of ninety" | 4.4; Supp A(l) Table A6, A(o), A(w) | `matched_frame_gap.csv` | `code/verify_matched_gap.py` | A |
| 38 | Features supported in both "rise from 1.20 to 3.40 per direction" | 4.4; Supp A(w) | `diagnostics_collar_frame.csv` | `code/verify_diag_collar.py` | A |
| 39 | "crosses 0.5 in Manavgat" (0.505), Montiferru attenuated | 4.4; Supp A(k), A(o) | `matched_frame_gap.csv` | `code/verify_matched_gap.py` (already probed for the corrected label by `ems_labels_5b_…`) | A |
| 40 | Diagnostic on the collar "1.0 in all eighteen directions, variance zero"; cosine "+0.81 → −0.06" | 4.4; Supp App D Table 3 | `diagnostics_collar_frame.csv`, `collar_increment_and_cosine.csv`; the full-frame side is `conditional_similarity_transfer.json` | `verify_diag_collar.py`, `verify_collar_increment.py`; `conditional_similarity.mjs` over the step9g/synthesis output | A + B→M |
| 41 | Collar within-region increment mean +0.077 vs +0.086 as drawn; per region +0.041 (Man), …; 5 km collar +0.041; "positive in all five" | 4.4; Supp A(o), A(w) | `collar_increment_and_cosine.csv` | `code/verify_collar_increment.py` | A |
| 42 | Table 3, all five rows: mean, above/below counts, supported counts, paired delta | 4.4 | `aoi_frame_transfer_frozen_mugla.csv` (and `aoi_frame_transfer.csv`) | `code/regen_transfer_ci.py`; `code/verify_aoi_transfer.py` | A |
| 43 | Provenance paragraph: "forty of a hundred values by up to 0.022 … within 0.0012 … at most 0.008" | 4.4; Supp A(w) | `frozen_mugla_recheck.json` | — | D (the canonical re-run already shows it is inaccurate; rewrite it) |
| 44 | Baseline on the collar 0.593 vs 0.616; +0.023 vs +0.004; "about six times", "about four times at 5 km"; "four to one with interval support"; supported "9 above / 4 below → 15 / 1" | 4.4; Supp A(w) | `aoi_frame_transfer*.csv` | `regen_transfer_ci.py`; `code/verify_transfer_counts.py` | A / D |
| 45 | Equalised paired delta +0.023 [−0.004, +0.048] (pair cluster); target-cluster interval excludes zero | 4.4; 1.3 | `equalised_delta_interval.json`, `transfer_delta_ci.json` | `code/transfer_delta_ci.py` | A |
| 46 | Matched within-region reference 0.772; shortfall +0.155 [+0.094, +0.217]; "0.25 unmatched" | 4.4; 1.3; 6; Supp A(w) | `matched_frame_gap.csv` | `code/verify_matched_gap.py` | A |

### 1.6 Results §4.5–4.6

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 47 | Raw range "0.326 to 0.686" (both endpoints are Manavgat directions) | 4.5; Supp A(ix); Cap Fig 4 | `cross_region/<pair>/step10/step10_metrics.json`, step9b | step9b; step10 | B |
| 48 | Support counts 12 / 6 (2-cell) and 9 / 4 / 7 (10-cell); "only Manavgat to Bejís survives"; "Bejís to Manavgat and Manavgat to Muğla lose support" | 4.5; Supp A(ix), A(v), A(c) | B9 CIs: step10 bootstrap / step9c. 10-cell: `transfer_ci_blocksize.csv` | step9c / step10c; `transfer_ci_blocksize.mjs` | B, B→M |
| 49 | "that target's own within-region 0.870"; raw deficit "0.184 to 0.592" (both endpoints are Manavgat) | 4.5; Supp A(ix) | step8c + step9b | B | D |
| 50 | PR-AUC 0.156 vs no-skill 0.136; "six below baseline, five with intervals"; "exception Bejís→Manavgat"; "only one exceeds twice" (Evia→Man 2.45). Man prevalence 0.038 → ~0.143 changes every into-Manavgat lift | 4.5; 5.6; B4; Supp A(o), A(ix) | `multi_aoi_transfer_matrix.csv` (5-AOI synthesis) | `multi_aoi_transfer_synthesis` → `referee_round_numbers.mjs` | B→M |
| 51 | Paired-delta spread "−0.148 to +0.133", 12 positive / 8 negative, "thirty times the mean" | 4.5; Supp A(o), A(ix) | `baseline_vs_thermal_transfer.csv` | step9b/9c → `baseline_vs_thermal.mjs` | B→M |
| 52 | Four resampling units [−0.027, +0.034] … [−0.037, +0.046]; jackknife +0.0148 (Man) / +0.0021 / +0.0065 / −0.0081 / +0.0060; "dropping Evia reverses its sign" | 4.5; Supp A(o) | `transfer_delta_ci.json` | `code/transfer_delta_ci.py` (over `aoi_frame_transfer.csv` full/full, or `baseline_vs_thermal_transfer.csv`) | A |
| 53 | Adapted ranges z 0.431–0.630 and CORAL 0.443–0.624 (lower endpoints are Man→Muğ); "fourteen of twenty move closer"; "five of six involve Montiferru, sixth Manavgat→Muğla"; "Bejís→Manavgat … margin of 0.001" | 4.5; Supp A(ix); Cap Fig 4 | step10_metrics | step10b/10c | B |
| 54 | CORAL mean 0.552; oracle 0.556 | 4.5; 5.6; Supp A(ix) | step10_metrics | step10 | B |
| 55 | "at most 34 % of the gap" (Muğ→Man); "seven directions with negative recovery" | 4.5; Supp A(ix), A(j) | `four_aoi_decomposition.csv` | `transfer_decomposition.py` | B |
| 56 | Interventions: local cost −0.081; transfer +0.014 [−0.017, +0.045] | 4.6; 5.3; Supp A(n), A(aa); Cap Fig 7 | `feature_drop_transfer.json` | root `feature_drop.py` → `feature_drop_merge.mjs` | A-stg |
| 57 | Label budget: "85 to 89 % in three of six … 30 to 57 % … 7 to 20 %" | 4.6; Supp A(u), A(aa) | `recovery_curve.csv` | `few_shot_recovery.py` | B |
| 58 | Fig. 4, all three panels (8 Manavgat cells each, plus the diagonal); caption ranges, hatching edge cells, "worst case 4.7:1" | Fig 4; Cap | `fig_data.json` `fig5` ← step10_metrics | `extract_fig_data.mjs` → `fig4_transfer_matrix.py` (asserts panel ranges) | C |
| 59 | Fig. 5, 12 arrows (6 involve Manavgat); caption "five recovery / seven negative"; "exception Manavgat→Muğla 0.470 → 0.443"; "Evia→Manavgat 0.686 → 0.527 vs 0.870, −0.862" | Fig 5; Cap | `fig_data.json` `fig6_decomp` ← `four_aoi_decomposition.csv` | `fig5_adaptation.py`; asserts in `_conservation_common.py` | C |
| 60 | Fig. 6 LORO: all five targets (every pool contains Manavgat, or Manavgat is the target); caption "Manavgat 0.469, Bejís 0.417 … 0.686 and 0.583" | Fig 6; Cap | `loro_pooled_transfer.json` | root `loro_pooled.py` → `loro_merge.mjs` → fig_data → `fig6_loro.py` (asserts 0.469) | C (A-stg data) |
| 61 | Fig. 7 feature drop; caption 0.541 → 0.556, 0.888 → 0.807, 0.081, +0.014 | Fig 7; Cap | `feature_drop_transfer.json` | → `fig7_feature_drop.py` (asserts means and monotonicity) | C (A-stg data) |
| 62 | Graphical abstract: within 5 km per region (Man 0.050), 0.027, LOSO, across-region interval, frame cost | GA | parses `04_results.md` | `figures/graphical_abstract.py` (hard asserts) | C |

### 1.7 Discussion and Appendix C.5

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 63 | Window closure "positive and bootstrap-supported everywhere" (Man is one of the five); "weakens monotonically in Evia" | 5.2; 6; Supp A(d) | `drive_new/diagnostics/window_closure_sensitivity/manavgat_2021` (other regions in `window_closure_region`) | `window_closure_sensitivity.py` | B |
| 64 | Regime hypothesis: "wrong sign", "most regime-similar pair fails in both directions", "most regime-different pair transfers above chance" | 5.4 | `regime_transfer_correlation.json` | `burned_pattern_audit.py` (B) → `regime_correlation.mjs` | B→M |
| 65 | "subsampling Muğla … to Manavgat's cell count and … positive count leaves it inside the range". **The positive-count target changes from 784 to 2,935, and 2,935 exceeds Muğla's own 2,911**, so this arm must be re-specified | 5.4 | `drive_new/diagnostics/mugla_subsampling/…` | `mugla_subsampling.py` | B |
| 66 | "about 0.14 ROC-AUC on the same model" | 5.6 | row 1 | — | D |
| 67 | "5 km and 10 km give 0.608 against 0.616"; "−0.00045"; "effective sample of ten pairs" | 5.7; C5 (viii), (ix) | Table 3; `transfer_ci_blocksize.json` | A; B→M | A / B→M |
| 68 | C.5 (iv): Evia 0.287 "against 0.038 to 0.072 in three of the others" (Man 0.038 is the endpoint; it becomes ~0.143) | C5 | B8 | step8a stats | D |
| 69 | C.5 (vii) "Manavgat's atypical transfer behaviour remains unexplained … frame explains its elevation figure … QC moves nothing by more than +0.0003". The corrected label gives Man elevation AUC 0.232 [0.177, 0.287] (r5), so this paragraph needs a full rewrite | C5 | r5, QC arm, rows 34–39 | — | D |
| 70 | C.5 (viii) "ten positive, seven negative and three uncertain … −0.00045" | C5; Supp A(c), A(v) | `transfer_ci_blocksize.json` | `transfer_ci_blocksize.mjs` | B→M |
| 71 | C.5 (x) and A(h) model capacity: 0.510–0.556, "fourteen of twenty" for all four estimators | C5; Supp A(h) | `model_capacity.json` | `code/model_capacity.py` | A |

### 1.8 Appendix B tables

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 72 | Table B2, Manavgat column: 9 signed AUCs with 10-cell CIs and bold marks; the reversal-rule example (`current_lst` Man vs Muğ) | B2; Supp App D Table B10 | `multi_aoi_feature_stability.csv` (5-AOI synthesis) ← step9g | `step9g_univariate_…py` → `multi_aoi_transfer_synthesis` | B |
| 73 | Table B3: two elevation rows (Man vs Bej +0.269 [+0.138, +0.397]; Man vs Muğ +0.235); "three pair-level reversals across two features"; "twenty-nine further pairs"; the choice of the two dropped features (3.11) | B3; 3.11; Supp A(n) | step9g / synthesis; cross-check `signed_auc_bootstrap.json` | step9g (B); `signed_auc_bootstrap.mjs` | B |
| 74 | Table B4: 8 Manavgat directions plus the mean row | B4 | `multi_aoi_transfer_matrix.csv` | synthesis → `referee_round_numbers.mjs` | B→M |
| 75 | Table B6, Manavgat row (784, 13.4 km, 60.1 %) | B6 | `aoi_frame_auc.csv` | `verify_aoi_frame.py` | A |
| 76 | Table B7, Manavgat column (6 values) and the "straddles 0.5" column | B7 | `aoi_frame_auc_frozen_mugla.csv` | `frozen_mugla_verify_aoi_frame.py` | A |
| 77 | Table B8, Manavgat row: 796 / 0.033 / 784 / 0.038 / 0.984 gate | B8 | `experiments/manavgat_2021/step8a/step8a_dataset_stats.json`; gate JSON | step8a; step6b | B |
| 78 | Table B9: 8 Manavgat directions × {raw, z, CORAL} with 2-cell CIs | B9 | step10_metrics / step10_bootstrap_summary | step10 (raw also step9b/9c) | B |

### 1.9 Supplementary Appendix A

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 79 | A(a) legacy Evia: "up to 0.07 … no direction changes side" (includes Man↔Evia legacy) | Supp A(a) | `cross_region/manavgat_2021__evia_2021`, `mugla…evia_2021` etc. | step9b legacy pairs | B |
| 80 | A(b) λ = 1 on the four directions: thermal mean 0.519 → 0.522, values 0.510 / 0.444 / 0.559 / 0.575 vs λ = 0.1 | Supp A(b) | `coral_lambda1.csv`; drive_new `coral_lambda_sensitivity` | **producer of `coral_lambda1.csv` not found in the tree** (`observational_sensitivities.md` names it only) | B (script missing) |
| 81 | A(b) Bej→Man 0.5571 [0.5292, 0.5857], λ sweep 0.5644 / 0.5473 / 0.4850; Man→Bej 0.5108 → 0.4776 | Supp A(b) | `experiments/cross_region/step10/coral_lambda_sensitivity.csv` | `step10/run_e_coral_lambda_sensitivity.py` | A-s10 |
| 82 | A(c) counts 10/7/3 → 6/4/10; five seeds "5–6, 3–4, 10–11" | Supp A(c), A(v) | `transfer_ci_blocksize.json` | `transfer_ci_blocksize.mjs` (BSEED env) | B→M |
| 83 | A(d) window closure: Bejís 0.058 → 0.079, Muğla 0.115 → 0.128, Evia 0.156 / 0.149 / 0.135 (Man not quoted, but "stays positive and supported everywhere") | Supp A(d) | window_closure outputs | as row 63 | B / D |
| 84 | A(e) and A(v) QC arm: r = +0.615, 22,304 of 24,150 cells, 10.9 °C (predictor-only, label-independent); "no signed AUC moves > +0.0003"; "elevation identical 0.374"; increment [+0.055, +0.079] → [+0.054, +0.077] | Supp A(e), A(v); C5 (vii) | `modis_qc_downstream_propagation.json/.md` | `run_qc_propagation.ps1` (arms A/B, step8) + `qc_compare.py` | B (label-dependent parts only) |
| 85 | A(f) feature-set table: 0.5371 / 0.5442 / 0.5479 / 0.5414; 16 / 15 / 13 / 14; within 0.7896 … 0.8883; normalised − absolute −0.0037, 12 of 20, −0.099 to +0.094; "0.000000" reproduction | Supp A(f) | `no_coord_channels.json` (⊇ `anomaly_only_transfer.json`) | `code/anomaly_only.py` (+ `anomaly_stage.py` staging; asserts vs step9b / step8c) | A |
| 86 | A(g) no-coordinate channels: Man row +0.067 / +0.063 / 94 %; mean +0.099 / +0.091 / 92 %; "82 to 103 %"; transfer 0.545 | Supp A(g) | `no_coord_channels.json` | `code/anomaly_only.py` (config `no_coord_channels`) | A |
| 87 | A(h) model-capacity table (4 estimators × 5 columns) | Supp A(h) | `model_capacity.json` | `code/model_capacity.py` | A |
| 88 | A(i) Table A1: 4 Manavgat half-splits (700 / 84; 0.695 …); "two splits unusable because one half of Manavgat has no burned cells" (may change with the new label) | Supp A(i) | `positive_control.json` | `code/positive_control.py` | A |
| 89 | A(i) Table A2: Manavgat scar row (88 / 696 / 1,135 / 0.592); "four arms in the other regions mean 0.525"; 0.552 | Supp A(i), A(u) | `scar_control.json` / `matched_holdout.json` | root `scar_control.py` / `verify_matched.py` | A-stg / A |
| 90 | A(i) Table A3: Manavgat scar row (0.468, 0.407–0.563) plus the Manavgat-sourced cells of every other scar; "0.559", "ten below chance", spread 0.164 / 0.171 | Supp A(i), A(u), A(z) | `d_per_source.json` | `code/d_per_source.py` | A |
| 91 | A(i) Table A4: Manavgat row (0.61, 0.797 / 0.796 / 0.589) and the means | Supp A(i) | `prevalence_control.json` | `code/prevalence_control.py` | A |
| 92 | A(j) Table A5: 6 Manavgat directions and the status column | Supp A(j) | `four_aoi_decomposition.csv` | `transfer_decomposition.py` | B |
| 93 | A(k) table, Manavgat row (0.386 / 0.402 / 0.440 / 0.505 / 0.621 / 0.542); "four of five", "NDVI reverses in two" | Supp A(k) | `matched_frame_gap.csv` | `code/verify_matched_gap.py` | A |
| 94 | A(l) Table A6: Manavgat vs Evia 0.462 vs 0.584, −0.122 [−0.225, −0.020]; "nine of ninety" | Supp A(l) | `matched_frame_gap.csv` | `code/verify_matched_gap.py` | A |
| 95 | A(n) LORO: shortfalls 0.02–0.22, 0.28–0.50 below ceiling, Bejís 0.417 [0.369, 0.467], two targets below chance | Supp A(n) | `loro_pooled_transfer.json` | root `loro_pooled.py` + `loro_merge.mjs` (refs step9b / step8c / step10) | A-stg |
| 96 | A(n) feature drop: per-region −0.060 (Man) / −0.130 / −0.074 / −0.063 / −0.079; −0.061 and −0.013; configuration table 0.888 / 0.827 / 0.875 / 0.807 and 0.541 / 0.546 / 0.544 / 0.556 | Supp A(n) | `feature_drop_transfer.json` | root `feature_drop.py` + `feature_drop_merge.mjs` | A-stg |
| 97 | A(o) units table and jackknife (row 52); PR paragraph (row 50); Bejís→Man PR 0.034 [0.029, 0.042] vs 0.038; Evia→Man 0.094 vs 0.038 | Supp A(o) | as rows 50 and 52 | — | A / B→M |
| 98 | A(o) "ρ = +0.86 over fourteen … +0.84 over sixteen … three region pairs" scope note | Supp A(o) | `diagnostics_collar_frame.csv` | `verify_diag_collar.py` | A |
| 99 | A(o) collinearity on the collar: LST vs elevation −0.695 to −0.125; fused/current 0.99–1.00; downscaled 0.97–0.99; TVDI 0.87–0.98 (the collar membership of Manavgat cells changes) | Supp A(o) | `verify_collar_ci.py` / `verify_matched_gap.py` output | A | A |
| 100 | A(s) contrast pair: Manavgat–Muğla "same side 0.561 vs 0.606"; "below chance in both directions as drawn, above under collar"; "weakest Manavgat to Bejís at 0.417, strongest Muğla to Evia 0.727"; "five of nine directions point opposite" | Supp A(s) | `aoi_frame_transfer*.csv`, `aoi_frame_auc*.csv`, synthesis signed AUCs | A; B | A / B |
| 101 | A(t) distance curve: bins 0.692 / 0.519 / 0.499 / 0.445 / 0.541 / 0.421 (Man halves contribute); cross-region row 0.541 | Supp A(t) | `distance_curve.json` | `code/distance_curve.py` (cross points from `comparison_inputs.json` ← step9b) | A (+B) |
| 102 | A(t) "Manavgat to Bejís below chance with interval support on the frame as drawn and at the 10 km collar" | Supp A(t) | B9; Table 3 CSV | B; A | D |
| 103 | A(u): "ceiling 0.777 to 0.824" (Man 0.797 inside); "2,700 to 3,000 labelled cells"; "540 to 620 km²" | Supp A(u); S1 | `recovery_curve.csv`, `target_block_inventory.csv` | `few_shot_recovery.py` | B / D |
| 104 | A(v) secondary population: all-valid increment +0.044 to +0.061; primary +0.046 to +0.067 (Man +0.067 is the upper endpoint); paired difference −0.008 to +0.011 | Supp A(v) | `thermal-twin/experiments/manavgat_2021/step10/within_robustness.json` (`by_population`) | `step10/run_d_within_robustness.py` | A-s10 |
| 105 | A(w) "largest movers Bejís to Evia 0.383 → 0.602, Bejís to Manavgat 0.440 → 0.601" | Supp A(w) | `aoi_frame_transfer*.csv` | `regen_transfer_ci.py` | A |
| 106 | A(w) matched-gap table: 0.798 / 0.540 / 0.258; 0.772 / 0.616 / 0.155; 0.737 / 0.608 / 0.129; per-region shortfall +0.086 / +0.127 (Man) / +0.161 / +0.196 / +0.206; "fire-adjacent share 37 % to 98 %" | Supp A(w) | `matched_frame_gap.csv`, `aoi_frame_auc.csv` | `verify_matched_gap.py`, `verify_aoi_frame.py` | A |
| 107 | A(ix) "twelve above / six below with CI support: both directions of Manavgat to Bejís and of Manavgat to Muğla …"; "Evia to Manavgat at 0.686 … 0.870"; "one, Manavgat to Bejís at 0.417 [0.349, 0.488] … covers chance at 5 km"; "no adapted direction exceeds 0.631 against 0.859 to 0.918" | Supp A(ix) | B9; Table 3 CSV; step8c | B; A | B / D |
| 108 | A(y) and App D, section 4.6 Table 5, Table B1 (20 diagnostic ρ with CIs), common-subset +0.87 / +0.85 and "4.8 × 10⁻⁵"; p = 0.0060, 240 / 40,320, ceiling +0.861, Bonferroni; "eight region pairs"; unselected +0.50 / +0.18 | Supp A(y), App D | `all_diagnostics_vs_transfer.csv`, `conditional_similarity_transfer.json`, `niche_overlap_transfer.json`, `regime_transfer_correlation.json`, `diagnostics_common_subset.*` | `conditional_similarity.mjs`, `niche_overlap.py` + `niche_corr.mjs`, `regime_correlation.mjs`, `diagnostics_common_subset.mjs`, over step9b (B), synthesis (B), burned_pattern_audit (B), domain classifier (label-free), marginal AoA (B), ERA5 (label-free) | B→M / A-stg |
| 109 | A(y) geographic: ρ −0.32 (20 directions) and −0.24 (12); "2,802 km pair returns 0.326 and 0.444"; "two nearest directions among the worst" (Man–Muğ); "domain classifier ≥ 0.96" (label-free value) | Supp A(y), App D | as row 108 | — | B→M / D |
| 110 | App D §5.3: "Manavgat to Muğla … 0.875 of target cells inside the AoA … among the weakest on either frame" | Supp App D | `marginal_diagnostics_with_transfer.csv` (weighted AoA uses step8b importances) | `marginal_aoa_completion.py` | B |
| 111 | App D Table B10: Schoener D 0.826 / 0.479, per-feature 0.77–0.89 / 0.23–0.77; transfer 0.470 / 0.401 and 0.551 / 0.510; ranks 5th / 2nd, 15th / 11th; AoA 0.875 / 0.531. Global binning means the Bejís–Montiferru D can move too | Supp App D | `niche_overlap_transfer.json`, B9, `aoi_frame_transfer.csv`, marginal AoA | root `niche_overlap.py`; B; A | A-stg / B / A |
| 112 | Fig. 8 (App D contrast pairs), panel (a) Manavgat–Muğla; caption D̄ = 0.83, supported features {NDVI, elevation}, 0.470 / 0.401, 0.551 / 0.510 | Supp App D | `figure_contrast_pairs.json` | `niche_vs_conditional.mjs` → `figures/fig8_contrast_pairs.py` (asserts D̄ and supported sets) | C |
| 113 | A(z) patch-definition sweep "row-C mean 0.545 to 0.566", "eleven to seven scars", "flat across 2, 5, 10 km" | Supp A(z), A(u) | `scar_definition_sweep.csv`; buffers in `scar_control.json` | `code/scar_definition_sweep.py`; root `scar_control.py` | A / A-stg |
| 114 | A(z) increment ladder table (+0.056 to +0.153; +0.027; +0.022; +0.004) | Supp A(z) | rows 30–32 and 6 | — | A / B |
| 115 | A(aa) summary restatements (−0.081, +0.014, 85–89 %, 30–57 %, 7–20 %) | Supp A(aa) | rows 56 and 57 | — | D |

### 1.10 Supplement S1

| # | Quantity as printed | Location | Source artefact | Producer | Class |
|---|---|---|---|---|---|
| 116 | Table S1: 4 Manavgat directions (raw, 1–32 blocks, ceiling 0.797 / 0.824 / 0.777, recovered %) | S1 | `drive_new/diagnostics/few_shot_recovery/<id>/recovery_curve.csv` | `few_shot_recovery.py` | B |
| 117 | "Bejís → Manavgat [0.392, 0.484] at one block, [0.733, 0.748] at 32"; "Muğla → Manavgat below 0.5 after 8 blocks"; "the two directions … reach only 51 to 57 %" | S1.3 | `repeat_metrics.csv` / `recovery_curve.csv` | same | B |
| 118 | Limit 4: "Manavgat 26 and 28" blocks; "880.0 … Bejís" (Bejís target, but the source side includes Man→Bej) | S1.4 | `target_block_inventory.csv` | same | B |
| 119 | Limit 5 "0.777 to 0.824 against 0.859 to 0.918"; limit 6 ceiling reproduction "0.0 against 10⁻⁹"; limit 7 "67 PASS", "3,642 fits" | S1.4 | `validation_report.json` | `validate_few_shot_recovery.py` | B / D |

### 1.11 Headline counts

| Class | Rows |
|---|---:|
| A (incl. A-s10) | 49 |
| B | 27 |
| B→M | 12 |
| A-stg | 7 |
| C (figures) | 8 |
| D | 16 |
| Total | 119 |

Mixed rows are counted under the first class listed. About a dozen rows carry a secondary class.
Every printed per-direction table row with a Manavgat source or target is covered, and so is every
mean over 20 or 12 directions.

---

## 2. Dependency order

### 2.0 Prerequisite: the corrected table

A corrected `step8a_500m_modeling_dataset.parquet` for Manavgat must be consistent in every column:

- `burned`
- `burn_date`, `burn_month`, `burn_day_of_year` (step8b requires `burn_month`)
- `label_source == "MCD64A1"` for new positives (step9a errors otherwise)
- `burn_date_pixel_agreement_fraction`, `out_of_window_burndate`

It also needs corrected label rasters, stats and gate outputs:

- `step8a_dataset_stats.json`
- `step8a_500m_grid_burned_label.tif`
- `validation/labels/mcd64a1_raw.tif` and `mcd64a1_burned.tif`
- `burned_landcover_gate.{json,csv}`

The EE-validated full-window burndate image is already cached by `ems_labels_5` as
`<cache>/manavgat_2021_labelwin.npy`.

Cleanest route: in a code copy,

1. run `run_label_gate_only.py --experiment manavgat_2021 --export-labels` (Earth Engine) against the fixed step6;
2. run `step8a.run_step8a(ctx)` against the staged predictor rasters.

Alternative: substitute these columns by `cell_id` from the npy, then regenerate the stats and gate
JSON with step6b on the new raster.

### 2.1 Tier B1: within-region, Manavgat only

step8b → step8c (→ step8d → step8e) → the prerequisites below

- `step8_big_block_robustness` v2 (10 and 20 cells)
- `step8_large_block_robustness` (manavgat + bejis) and `_primary_all_valid`
- the QC arm (`run_qc_propagation`-equivalent), which substitutes labels into both QC arms' step8a tables, then runs step8b/8c and `qc_compare.py`

Consumers:

- Table 1 and Fig. 3
- `fig_data.json fig34`
- the `comparison_inputs.json` within references
- `loro_merge.mjs` and `feature_drop_merge.mjs` references
- the ceiling references of `few_shot_recovery`

### 2.2 Tier B2: cross-region

step9a → 9b → 9c (→ 9d → 9e) for these pair folders:

- `manavgat_2021__bejis_2022`
- `manavgat_2021__mugla_2021`
- `manavgat_2021__evia_2021_extended`
- `mugla_2021__manavgat_2021`
- `montiferru_2021__manavgat_2021`
- legacy `manavgat_2021__evia_2021`, for A(a)

`--reverse` covers both directions of each pair.

Then:

1. step10a–d for the five modern pairs. It aborts unless raw reproduces step9b and the target step8b cell and block alignment holds, so it needs Tier B1.
2. step9g univariate for the Manavgat pairs, then `step9g_multi_aoi_comparison`.
3. `transfer_decomposition` (four-AOI) and `multi_aoi_transfer_synthesis` (5-AOI and 4-AOI sets). The synthesis reads step8b, big_blocks_v2, 9b–9e, 9g and step10.
4. `coral_lambda_sensitivity` (Man–Muğ directions; gate against step10 predictions).
5. `few_shot_recovery` (needs the B1 big-block ceilings).
6. `burned_pattern_audit` (needs the corrected gate JSON).
7. `marginal_aoa_completion` (step8b importances plus `four_aoi_decomposition.csv`).
8. `mugla_subsampling` (needs new mugla↔manavgat step9b; must be re-specified).
9. `window_closure_sensitivity` for Manavgat, last, because it rebuilds step5→8A from label rasters.

### 2.3 Tier M: paper-side aggregators over B

| Aggregator | Reads (B outputs) | Writes | Feeds |
|---|---|---|---|
| `baseline_vs_thermal.mjs` | step9b + step9c | `baseline_vs_thermal_transfer.{csv,json}` | rows 6, 7, 51; **read by A scripts `transfer_delta_ci.py`, `verify_collar_increment.py`, `verify_diag_collar.py`, `ems_labels_2_history.py`** |
| `referee_round_numbers.mjs` | synthesis `multi_aoi_transfer_matrix.csv`, marginal AoA, step8a stats | `referee_round_numbers.{md,csv}` | B4 and PR rows |
| `referee2_numbers.mjs` | step9b prediction tables, step8a stats, step8d, step7c | `referee2_numbers.{md,json}` | block counts (row 14), pre-label |
| `transfer_ci_blocksize.mjs` | step9b predictions, step9c, step10 bootstrap summary | `transfer_ci_blocksize.{csv,json}` | rows 17, 48, 70, 82; **read by `ems_inference_units.py`** |
| `conditional_similarity.mjs` | synthesis `multi_aoi_feature_stability.csv`, step9b | `conditional_similarity_transfer.json` | row 108; `verify_diag_collar` full-frame side |
| `regime_correlation.mjs` | `burned_pattern_audit`, domain classifier, marginal AoA, step9b | `regime_transfer_correlation.json` | rows 64, 108 |
| `niche_corr.mjs` | root `niche_overlap.py` output (A-stg), step9b | `niche_overlap_transfer.json`, `all_diagnostics_vs_transfer.csv` | row 108; **read by `ems_inference_multiplicity.py`** |
| `niche_vs_conditional.mjs` | the above, step9c | `figure_contrast_pairs.json`, `niche_vs_conditional.json` | Fig. 8, Table B10 |
| `diagnostics_common_subset.mjs` | all of the above | `diagnostics_common_subset.*` | row 108 |
| `loro_merge.mjs` | root `loro_pooled.py` output, step9b, step8c, step10 | `loro_pooled_transfer.json` | Fig. 6, row 95 |
| `feature_drop_merge.mjs` | root `feature_drop.py` output, step9b, step8c | `feature_drop_transfer.json` | Fig. 7, rows 56 and 96 |

All `.mjs` files except `referee2_numbers.mjs` and `transfer_ci_blocksize.mjs` hard-code
`ROOT='C:/Users/CORSAIR/projects/thermal-twin'`, and they write into `ROOT/paper`. Parametrise
`ROOT` before re-running.

### 2.4 Tier A: paper/code and A-stg

Needs no B output (only the corrected table):

- `verify_aoi_frame.py`, `frozen_mugla_verify_aoi_frame.py`
- `verify_collar_ci.py`, `verify_matched_gap.py`
- `pool_decomposition.py`, `prevalence_control.py`, `positive_control.py`
- `scar_increment.py`, `verify_matched.py`, `d_per_source.py`
- `scar_definition_sweep.py`, `model_capacity.py`
- `regen_transfer_ci.py`, `verify_aoi_transfer.py`, `verify_transfer_counts.py`
- `ems_geometry_*`, `ems_labels_3/4/6`
- root `scar_control.py`, `niche_overlap.py`
- `step10/run_d`, `step10/run_e` (A-s10)

Then `transfer_delta_ci.py` and `verify_collar_increment.py`/`verify_diag_collar.py` run. They need
`aoi_frame_transfer.csv` from `regen_transfer_ci.py` (via `PAPER_ARTEFACTS`) and
`baseline_vs_thermal_transfer.csv` from Tier M.

Needs B references:

- `anomaly_only.py` and root `feature_drop.py`, `loro_pooled.py` take `comparison_inputs.json`, rebuilt from new step9b/step8c as `anomaly_stage.py` / CHANGES §6 do. Their hard asserts are <5e-4 against step9b and <1e-3 against step8c, so they then serve as the A-vs-B cross-check.
- `distance_curve.py` takes its cross-region points from `comparison_inputs.json`.
- `ems_inference_*` read `aoi_frame_transfer_frozen_mugla.csv`, `transfer_ci_blocksize.json`, `all_diagnostics_vs_transfer.csv` and `scar_increment.json` / `matched_holdout.json`, so they run last.

### 2.5 Tier C: figures

`figures/extract_fig_data.mjs` produces `fig_data.json`. It reads:

- step8c
- the robustness trees
- the 10 `step10_metrics.json`
- `four_aoi_decomposition.csv`
- `loro_pooled_transfer.json`
- `feature_drop_transfer.json`

Its drive_new paths are hard-coded under `ROOT`, so point `ROOT` at the staging outputs.

Scripts: `fig3`–`fig7`, then `fig8` (from `figure_contrast_pairs.json`), then `graphical_abstract.py`,
**after** `04_results.md` is edited, because it parses that text.

Figure asserts that will fail by design and must be updated with the numbers:

- fig4: panel ranges
- fig5: 7/12 negative recovery, −0.862
- fig6: Manavgat 0.469
- fig7: 0.888 / 0.541 → 0.807 / 0.556 and both monotonicities
- fig8: D̄ 0.826 / 0.479 and the supported set [NDVI, elevation]
- graphical abstract: the (−0.028, 0.036) tuple and Table 1 block-10 values

### 2.6 Tier D: text

Rewrite last. These are qualitative claims that may flip, not just numbers:

- **Man elevation reversal.** Corrected full-frame AUC is 0.232, a stronger reversal, which bears on C.5(vii) and the frame argument.
- **Man absolute-LST sign.** 0.538 becomes 0.665 on the full frame, and the collar sign changes (see `r5b`).
- Scar counts (row 27).
- Half-split usability (row 88).
- Prevalence ranges (rows 50 and 68).
- The Muğla positive-count subsampling design (row 65).
- The 4.4 provenance paragraph (row 43).

---

## 3. B-class producers: entry points and a non-invasive way to run them

### 3.0 General mechanism

This section is from the code audit, with file:line citations kept.

**No path is configurable, and there is no root environment variable.**

- `core/paths.py:5` sets `PROJECT_ROOT = Path(__file__).resolve().parent.parent`.
- `core/regions.py:1092` `get_experiment_output_root` returns `PROJECT_ROOT/outputs/experiments/<ns>`.
- `core/experiment_context.py:104` builds every step directory from that root.
- `step9a:136-137` builds cross-region paths as `BASE_DIR/outputs/cross_region/<s>__<t>`.
- `core/io_utils.py:7-8` `setup_logger` creates and writes `PROJECT_ROOT/logs` when a module is imported. **Importing `repo/` in place therefore writes into `repo/`.**

**Recommended: a code copy plus a mirrored staging tree.**

1. Copy `repo/{core,src,scripts,config}` to `STAGE/code/`.
2. Build `STAGE/code/outputs/` as a copy (or hardlinks for the read-only partners) of drive_new: `experiments/`, `cross_region/`, `diagnostics/`, `robustness/`.
3. Overwrite `outputs/experiments/manavgat_2021/{step8a,validation/labels}` with the corrected files.
4. Delete the CSV sibling of the Manavgat parquet, because step8b falls back to it (`step8b:187-205`).
5. Delete or rename every Manavgat-dependent output directory listed below, so no stale output and no immutable preregistration aborts a run.
6. Run with `PYTHONDONTWRITEBYTECODE=1` and cwd = `STAGE/code`.

`PROJECT_ROOT` then resolves to the copy, and nothing is written to `repo/` or `drive_new/`. In-process
monkeypatching of `PROJECT_ROOT` / `BASE_DIR` also works but is fragile across modules.

**Precedent.** The August "Manavgat repair" (corrupted `elevation_mean` at r0_c0; step8a regenerated to
sha 054a1961) re-ran this same set. Its checklist is
`drive_new/diagnostics/advisor_followup_provenance/pre_rerun_snapshot/pre_rerun_manifest.json`
(526 entries):

- Manavgat step8b–8e
- every pair's step9a–9e and step10 (9f for manavgat__bejis)
- all step9g pairs
- both `step8_large_block` trees
- big_blocks_v2 manifests

The old step10 was moved to `step10_superseded_pre_manavgat_repair`. `src/old_new_metric_deltas.py`
(`main.py old-new-deltas`) diffs the new outputs against `pre_repair_baseline/`. Reuse this manifest
as the checklist.

**Pinned hash.** `CANONICAL_STEP8A_SHA256["manavgat_2021"] = "054a1961…"` aborts in these places:

| Module | Pinned at | Aborts at |
|---|---|---|
| `coral_lambda_sensitivity.py` | `:78-79` | `:199-207` |
| `few_shot_recovery.py` | `:159-160` | `:594-622` (strict) |
| `marginal_aoa_completion.py` | `:129-130` | `:546-560` (strict) |
| `mugla_subsampling.py` | `:207-208` | `:662-688` |
| `multi_region_window_closure/inputs.py` | `:32-33` | `:117-126` |

The dicts are read at call time, so set `mod.CANONICAL_STEP8A_SHA256["manavgat_2021"] = <new sha>`
in-process, or edit the copy.

On the paper side, `_canonical.py` has the same pin. `THERMAL_TWIN_DATA` redirects the data root,
but the hash constant must gain a corrected entry: either a second, named set, or an env-selected
label version. Keep the frozen hash for the "as published" arm.

### 3.1 Per producer

Cost is in 300-tree RF fits. "Reps" means 1000 bootstrap replicates, which cost no fits.

| Producer | Entry point | Input location | Label-dependent extras and hard checks | Least-invasive run | Cost |
|---|---|---|---|---|---|
| Corrected label (upstream) | `scripts/run_label_gate_only.py --experiment manavgat_2021 --export-labels --force` (EE; `:872-875`, `step6:870`), then `step8a.run_step8a(ctx)` (`:3265-3287`) | `experiment_context` | Writes `mcd64a1_raw/burned.tif` and `burned_landcover_gate.*`. step8a derives `burned`, `burn_date`, `burn_month`, `label_source` and agreement (`:1116-1260`) plus stats and the label TIF | In the code copy | no RF |
| step8b | `src/step8b_train_baseline_vs_thermal_model.py` CLI `--input --output-dir --force --spatial-block-size-cells` (`:1348-1364`; `main` `:1124`) or `run_step8b(ctx)` (`:1325`). **Do not use `run_step8_modeling.py`**: it rebuilds step8a from rasters (`:580`, `:665-670`) | `BASE_DIR/(input or STEP8B_INPUT_DATASET)` (`:188`); an absolute `--input` wins | Requires `burn_month` (`:143`, `:164`); writes `spatial_block_id` (`:813`) | Absolute paths into staging | up to 48 |
| step8c | CLI `--input --output-dir --n-bootstrap` (`:874-883`), `main` `:460` | `step8b_predictions.parquet` (`:865`) | Monthly strata use `burn_month` (`:584-590`) | same | 0 fits; reps per population |
| step8d / 8e | `step8d main` `:964`; 8e = `run_step8_modeling.py --report-only` (`:640-660`) | step8b | 8e reads the gate JSON (label-derived) and step7e stats; 8e's namespace guard requires paths under `outputs/experiments/<id>/` (`:84-103`); 8d only warns on mismatch | Code copy | 8d ~264 (not needed for the paper beyond `referee2_numbers` D) |
| Big-block robustness v2 | `scripts/run_step8_big_block_robustness.py --experiment manavgat_2021 --block-sizes 10 20 --force`; the v2 `output_root` is a `main()` keyword only (`:22-26`) | `PROJECT_ROOT/outputs/experiments/<id>` (`step8_large_block_robustness.py:87-88`); parquet, `valid_mask.tif` (hashed), step8b / step8c JSON (`:252-253`), step8e report | `EXPECTED_SMALL_BLOCK_REFERENCE` (`:144-152`) only flags a mismatch | Call `main(output_root=STAGE/.../step8_big_blocks_v2)` in-process | 24 + 2×reps |
| Large-block (pair) | `run_step8_large_block_robustness.py --experiments manavgat_2021 bejis_2022 --block-sizes-cells 10 20` (order enforced `:37-38`, `:77-83`) | Constant `OUTPUT_ROOT` (`:43-46`) | Hashes inputs before and after (`:108-112`); step8b / 8c provenance (`:129-159`); an immutable preregistration aborts on mismatch (`:238-248`) | Empty staging output root | 48 + 4×reps |
| Large-block all_valid | `run_analysis(output_root=)` (`:747`) | same | `V1_EXPECTED_ANALYSIS_ID` hard-coded (`:119`, aborts `:156-164`), so patch it in-process to the new v1 ID; 2-cell equivalence gate against step8b at 1e-12 (`:392-430`) | In-process | ~72 + 4×reps |
| step9a–9d | `scripts/run_cross_region_transfer.py --source --target --reverse --force` (`main` `:124`) | Parquet next to `step8a_dataset_stats.json` under `get_experiment_output_root` (`step9a:140-180`); `validation/labels/burned_landcover_gate.json` with `decision == wildfire_candidate_pass` (`:183-184`, `:299-312`); stats-manifest fields incl. `predictor_paths.anomaly_zscore` (`:231-336`) | `label_source` check (`:376-381`); 9d aborts if 9a failed | Staging tree with the corrected Manavgat step8a, stats and gate plus frozen partners; outputs to `<pair>/step9*` | 72 per pair × 6 pairs ≈ 430; 9c reps |
| step10a–d | `scripts/run_step10_self_calibrated_transfer.py --source --target --reverse --force --bootstrap-replicates 1000 --seed 42` (`main` `:138`) | step9a resolvers; target step8b predictions and metrics (`core/step10_shared.py:83-90`); step9b outputs (`:93-98`) | **Aborts** if raw ≠ step9b at 1e-6 (`step10c:59`, `:372-375`) and on target cell/block misalignment (`:126-150`), so run B1 first | Staging tree; move the old `step10/` aside | 12 per pair × 5 = 60; reps |
| transfer_decomposition | `scripts/main.py transfer-decomposition --aoi …` (`:1153-1183`) → `src/transfer_decomposition.run(output_root=None)` | `CROSS_REGION_ROOT = PROJECT_ROOT/outputs/cross_region` (`:68`); every pair's step10 metrics and replicates | `relative_to(PROJECT_ROOT)` (`:477`, `:715`) raises if outputs live outside the root, which the code copy avoids | Code copy | 0 fits; reps |
| coral_lambda_sensitivity | `scripts/run_coral_lambda_sensitivity.py --output-root --experiments-root --force` | `--experiments-root` | Hash abort (patch); canonical tier gate against the persisted manavgat↔mugla step10 predictions (`:706-709`), so run after step10 | `--output-root` in staging | ~80; reps |
| few_shot_recovery | `scripts/run_few_shot_recovery.py --experiments … --output-root --experiments-root` | reads `Path(output_root).parent/outputs/robustness/…` (`:634`) | Strict hash (patch); `FROZEN_CEILING_REFERENCE` (`:174-211`: Man block-10 0.74755 / 0.79743, tol 1e-9) fails validator FSR-35 (`validate_few_shot_recovery.py:503-513`), so patch it to the new big-block values; block labels recomputed in-process (`:683`) | Staging; restricting `--experiments` does not skip Bej↔Muğ, so either run all six directions or accept rerunning them | **~3,642 (heaviest)** |
| step9g univariate | `src/step9g_univariate_feature_auc_direction_reversal.py --source --target --force`; `run_analysis(…, output_root)` (`:821`) | step8a parquet and stats (`:247-266`) | Analysis ID changes on re-run; no frozen asserts | Staging, all Manavgat pairs | 0 fits; 9 features × 2 regions × reps |
| step9g integration v2 | — | — | **Cannot be re-run as-is**: pins `EXPECTED_FROZEN_STEP9G_ANALYSIS_ID = 87d4ec…` (`:96`, `:171-178`), and `_assert_required_statements` demands exactly {elevation} supported plus 4 uncertain (`:569-596`), which the corrected label will not give. It is already stale (87d4ec is pre-repair; the current step9g is `cfe79457…`). Omit the Man–Bej v2 dir so the synthesis falls back to v1 | — | — |
| step9g multi-AOI comparison | `scripts/main.py concept-shift-compare --experiments …` | step9g outputs | Cross-pair consistency at 1e-12 (`consistency.py:40-65`), so recompute all Man pairs first | Code copy | none |
| multi_aoi_transfer_synthesis | `scripts/main.py transfer-synthesis --aoi … [--output-root]` | Inputs hard-wired to `PROJECT_ROOT` (`resolvers.py:104`, `:301`, `:382-406`, `:611`, `:690-708`, `:781`); reads step8b, big_blocks_v2, 9b–9e, 9g (prefers v2), step10 | See step9g v2 | Code copy; run the 5-AOI and 4-AOI (and 3-AOI) sets | none |
| burned_pattern_audit | `scripts/run_burned_pattern_audit.py --experiments … --output-root` | step8a | Aborts if the gate JSON `burned_count` or universe ≠ the table (`:466-490`), so it needs the corrected gate JSON | `--output-root` | none |
| marginal_aoa_completion | `run_analysis(strict_hashes=False)` | step8b feature importances (`:148-151`, `:422-427`); joins `four_aoi_decomposition.csv` (`:234-238`) | Climate stage needs EE: copy the existing climate raster (label-free) | In-process | small |
| mugla_subsampling | `scripts/run_mugla_subsampling.py` | includes Manavgat arms (`:144-148`) | Hash abort (`:662-688`); recomputes step9b at 1e-9 (`:1500-1507`), so stage the new mugla↔manavgat step9b. **The Manavgat positive-count arm (2,935 > Muğla's 2,911) needs a design decision** | Staging | up to ~284 |
| Window closure (Manavgat) | `window_closure_sensitivity.main(…, output_root, experiments_root)` programmatically (the CLI blocks Manavgat, `run_window_closure_sensitivity.py:71-82`; `run_window_closure_region.py` excludes Manavgat as the "reference AOI", `contract.py:36-41`) | experiments root | **A parquet swap is not enough.** Local-downstream copies `mcd64a1_raw.tif` / `mcd64a1_burned.tif` and re-runs Step5→8A per shift (`:104-114`, `:5330-5352`); `compare_step8a_invariance` (`:6609ff`) and `build_common_cohort` (`:1488`) abort if labels differ from canonical; synthesis hash check (`inputs.py:117-126`, `production.py:797-835`). Needs the corrected rasters **and** patched canonical references | Last, in the code copy | ~30 fits + reps + Step5–8A rebuilds |
| QC arm (A(e)) | `paper/run_qc_propagation.ps1` (writes into `repo/outputs`; refuses by default) + `paper/qc_compare.py` (reads `paper/qc_work/manavgat_2021`) | its own staged arms | Predictors unchanged, so only the labels matter: substitute corrected `burned` / burn-date columns by `cell_id` into both arms' step8a tables, rerun step8b/8c on each with absolute `--input/--output-dir`, rerun `qc_compare.py`. **Do not use the .ps1 as written** | Point `W` in `qc_compare.py` at the new arms | ~2×48 |
| domain_classifier_audit, marginal AoA v1, ERA5, evia_signed_auc_bootstrap | — | — | Label-free, or Evia-only | **No re-run**; only the correlations against transfer (Tier M) change | — |

---

## 4. Does not depend on Manavgat: no re-run

- **Figures 1 and 2** (AOI boxes and schematic, including "Kozan 98 % cropland"); Table C1; §3.1 AOI-provenance text; §3.3 gate rule; Kozan 0.017.
- **Predictor and grid facts:**
  - Evia AOI prevalence 0.676 → 0.287 (4.1)
  - the missing-thermal share "6 % to 58 %" of valid cells (3.5: label-free)
  - gap-fill 0.11–9.70 % (C.4)
  - grid geometry 0.199–0.208 km² (C.1)
  - QC predictor facts (+0.615, 22,304 cells, 10.9 °C)
  - AOI distances 306–2,802 km
- **Muğla two-event arm:** Table B5, A(m), C.3, `mugla_two_event_collar.csv`, 93.2 % / 55.3 %, 11 / 70 blocks, 41,730 / 38,790 rows.
- **Per-region within-region values for Bejís, Muğla, Evia and Montiferru:**
  - Table 1 rows (step8c and their robustness trees). Bejís block 10/20 sits in the `manavgat_2021__bejis_2022` large-block tree but is a Bejís-only model. If that tree is regenerated, check that Bejís reproduces bit-for-bit.
  - A(d) values for the four
  - the A(g) per-region rows for the four
  - A(k) rows for the four
  - Tables B2, B6, B7 and B8 for the four regions
  - collar signed AUCs and intervals for the four
- **Transfer directions with neither end in Manavgat (12 of 20):**
  - per-direction raw, z, CORAL, baseline and PR values
  - per-direction CIs
  - per-direction collar-frame values
  - four-AOI decomposition rows Bej↔Muğ, Bej↔Evia, Muğ↔Evia
  - Table B3 Bejís–Evia row
  - A(b) λ values for Bej↔Muğ
  - S1 rows Muğla→Bejís and Bejís→Muğla, with the Bejís and Muğla ceilings 0.824 / 0.777

  **Caveat:** anything pooled, averaged, ranked or counted over these (means, spans, counts, correlations, pair-cluster intervals, jackknife, LORO, `d_per_source`, niche overlap with global binning, Fig. 4 colour scale) does change.
- **Label-free diagnostics:** domain-classifier AUCs, unweighted AoA support, ERA5 climatic distance, geographic distance. Their correlations with transfer do change.
- `ems_labels_1` pre-label and `ems_labels_2` history counts for the other regions. The ems_* outputs are not cited in the manuscript text; re-run the Manavgat-touching ones only if they enter the response.

---

## 5. Cost: heavy versus light

| Weight | Runs |
|---|---|
| **Heavy** | `few_shot_recovery` (~3,642 RF fits; ~2,400 are Manavgat directions, but the run is all-or-nothing). `regen_transfer_ci.py` / `verify_aoi_transfer.py` / `frozen_mugla_verify_aoi_transfer.py` (≈200 fits each over 5 frame configurations × 20 directions × 2 sets; run one and copy, as CHANGES §1 did). `ems_inference_ladder.py` (blocked CV on three frames plus LOSO plus half-split plus foreign, on every region). `mugla_subsampling` (≤284). Window closure (Step5–8A rebuilds). |
| **Medium** | step9b over 6 pair folders (~430 fits). `anomaly_only.py` (5 configurations × (20 transfers + 25 within folds) ≈ 225). `feature_drop.py` (~180). `model_capacity.py` (~180, a quarter of them logistic). `verify_matched_gap.py` (~150). step8d (~264, optional). step10 (~60) and `coral_lambda` (~80). The all_valid large-block run (~72). LORO (20 pooled fits on large training sets). `scar_definition_sweep.py` (8 settings × scars × 2). |
| **Light** | step8b/8c (≤48 fits). Big- and large-block (24–48). step9c, step10 bootstrap, `transfer_decomposition`, step9g, synthesis, `burned_pattern_audit`, marginal AoA (bootstrap or aggregation only). All `.mjs` aggregators. `verify_aoi_frame`, `verify_collar_ci`, `verify_diag_collar`, `transfer_delta_ci` (no fits, or 1000–20,000 cheap replicates). `pool_decomposition`, `prevalence_control`, `positive_control`, `scar_increment`, `verify_matched`, `d_per_source`, `distance_curve` (5–40 fits each). `step10/run_d`, `run_e`. Figures. |

The `canonical_rerun/_logs` directory holds wall-clock times for the A tier from the 2026-09-19
re-run. Use them to schedule.

## 6. Open items and ambiguities

1. **The corrected table is not yet materialised.** Decide between the upstream route (EE export + step8a in the code copy, which also yields the rasters window closure needs) and a column substitution by `cell_id`. All burn-date columns must be updated too.
2. **`_canonical.py`** needs a corrected-hash mechanism. Decide whether the paper keeps a frozen "as published" arm.
3. **step9g integration v2 cannot be re-run**, and its assertions encode the frozen conclusion. Decide whether B2/B3 come from step9g v1 plus the synthesis, or from `signed_auc_bootstrap.mjs` / `ems_labels_5` (the same instrument, already run on the corrected label).
4. **`coral_lambda1.csv`** (A(b), λ = 1): no producer script was found in the tree.
5. **`mugla_subsampling`**: the Manavgat positive count (2,935) now exceeds Muğla's positives (2,911), so the "subsample to Manavgat's positive count" arm is undefined as specified.
6. **Scar structure.** Manavgat may gain components ≥ 50 cells, which changes N in Table 2 and A(i)–A(z) and possibly the "Bejís is the only single-scar region without row C" logic. The half-split "no burned cells in one half" statement may also change.
7. **The QC propagation driver writes into `repo/outputs`.** Re-run it only by label substitution into its staged arms, as described in §3.1.
