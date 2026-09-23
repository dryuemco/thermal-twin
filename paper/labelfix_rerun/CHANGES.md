# Label-corrected re-run of the class-A analyses — what moved

Date: 2026-09-19. Labels: **corrected Manavgat** (`_canonical.load`, default `labels="corrected"`,
`THERMAL_TWIN_LABELS=corrected` set explicitly; parquet SHA-256 `e4ab8b85…`, raster `8940e706…`). All
other regions load their frozen canonical files (unchanged). Python `.venv-step10`, seed 42, RF and folds
unchanged, `n_jobs=4`, at most 4 jobs at once. Nothing tuned. Logs: `_logs/*.log`, `_logs/status.txt`
(every job rc=0; `run_e` first failed on a console-encoding error printing "λ" and was re-run unchanged
with `PYTHONIOENCODING=utf-8`). Nothing written to `repo/` or `drive_new/` (checked by mtime scan).

"Frozen" below means: for `paper/code` artefacts the `paper/canonical_rerun/` values (frozen labels,
canonical data); for `ems_*` the published `paper/ems_analyses/` files; for the root harnesses the
published `paper/*.json`; for `run_e` `experiments/cross_region/step10/`. Where the printed manuscript value
differs from the frozen canonical value (see `canonical_rerun/CHANGES.md`), both are given.

> **Correction and re-run, 2026-09-23.** The rename listed in §0, "`aoi_frame_transfer.csv →
> aoi_frame_transfer_frozen_mugla.csv`", means that `code/aoi_frame_transfer_frozen_mugla.csv` is a
> byte copy of **`regen_transfer_ci.py`'s** output. It carries that script's 10-cell bounds. It is
> not the output of `frozen_mugla_verify_aoi_transfer.py`, which went to
> `code/_staging/frozen_mugla_verify_aoi_transfer.csv`. Both scripts were re-run unchanged into
> `round5/collar/` as a re-run exception, and both reproduce this round to within 2×10⁻⁶ (identical
> at 3 dp). The paper now cites `round5/collar/aoi_frame_transfer.csv`. Details:
> `round5/collar/PROVENANCE.md`.

## 0. How each script was run, and every code change

Runner: `_logs/run_one.sh` (env `PAPER_ARTEFACTS=paper/labelfix_rerun/code`,
`EMS_OUT_ROOT=paper/labelfix_rerun`, `STEP10_OUT_DIR=…/labelfix_rerun/step10`); job lists
`_logs/jobs_phase1.txt`, `chain_*.sh`. Staging-dir scripts got `paper/labelfix_rerun/code/_staging`
(they write `{STAGING}/../X.json`). Copies, as in the canonical re-run: `verify_matched.json →
matched_holdout.json`, `verify_scar.json → scar_control.json`, `aoi_frame_transfer.csv →
aoi_frame_transfer_frozen_mugla.csv`, `_staging/aoi_frame_transfer.json → aoi_frame_transfer.json`.

Code changes (uncommitted; defaults unchanged unless the new env var is set):

| File | Change |
|---|---|
| `paper/scar_control.py`, `paper/loro_pooled.py`, `paper/niche_overlap.py` | `pd.read_parquet(f"{STAGING}/{reg}.parquet", columns=…)` → `_canonical.load(reg, columns=…)`; `_canonical.assert_no_leakage(...)` before each fit (niche: before the PCA fit); `n_jobs=-1 → 4`. niche_overlap: the hard-coded `parquet_sha256_prefixes` (which said `054a1961` for Manavgat) now records the actual hashes plus the label setting. |
| `paper/code/ems_geometry_common.py`, `ems_inference_common.py`, `ems_labels_common.py` | Optional `PAPER_ARTEFACTS` (input root for paper-level artefacts) and `EMS_OUT_ROOT` (output root) overrides. Pointing `PAPER_ARTEFACTS` at `labelfix_rerun/code` makes every class-B file absent, so any B dependency fails loudly instead of silently reading a frozen-label file. |
| `paper/code/ems_labels_common.py` | `read_local(region, "mcd64a1_raw.tif")` serves the corrected, SHA-verified Manavgat raster under the corrected label setting (otherwise the burned-fraction and V1/label-rule checks would mix frozen raster with corrected labels). Validated: V1 Manavgat mismatch 624,130 → **0** px; label rule 0 disagreements in all five regions; r3 `label_rule_disagreements` 0. |
| `paper/code/ems_inference_units.py` | `quantities()` omits Q1 (as-drawn Δ from `transfer_ci_blocksize.json`, class B→M) when that file is absent. |
| `paper/code/ems_inference_equivalence.py` | TOST loop skips a quantity that `quantities()` omitted (records `"skipped"`). |
| `paper/code/ems_inference_multiplicity.py` | Diagnostic family (reads four B→M files) skipped when `all_diagnostics_vs_transfer.csv` is absent; the reversal family (label data only) runs. |
| `step10/data_io.py` | `load_region` reads via `_canonical.load(region_key)` (the `config10.REGIONS` path does not exist in this tree). |
| `step10/run_e_coral_lambda_sensitivity.py` | Optional `STEP10_OUT_DIR` output override. Run through `_logs/run_e_driver.py`, which sets RF `n_jobs=4` in `config10` in-process. |

**No hard assert fired, so no expected value was changed.** Stale reference constants that are printed
but not asserted: `verify_matched_gap.py` prints "transfer means for reference: full 0.5400, 10 km 0.6166,
5 km 0.6077" (frozen); `scar_definition_sweep.py` prints "manuscript claims 0.543 to 0.565 / published
row C 0.552"; `scar_increment.py` prints "+0.056 to +0.153 … +0.004"; `transfer_delta_ci.json` field
`check_vs_step9b_max_abs_diff_4dp` = **0.0605** — it compares against the frozen step9b export
(`paper/baseline_vs_thermal_transfer.csv`), so it is expected to fail until step9b is regenerated; the
field is a cross-check only and feeds no quantity. `ems_labels_2_history.py` reads the same B file only to
log its column names.

**Semantic caveat, ems_geometry:** the scripts' set labelled `eight_scars_table2` is defined as
"region ≠ Bejís". Under the corrected label that set still has 8 scars but is **no longer Table 2's set**
(Manavgat now has no row C, see §1). The 7-scar Table-2 values below were computed from the scripts' own
per-scar CSVs (`a1_frame_cost_edge_excluded.csv`, `a2_placebo_by_scar.csv`), same `t` formula.

## 1. Manavgat scar list (8-connected components ≥ 50 TSG burned cells, 2 km dilation)

| | Frozen | Corrected |
|---|---|---|
| Components ≥ 50 cells | 1 (label 1; 690 cells) | **1 (label 1; 2,934 cells)** |
| Held area (scar + 2 km): cells / positives | 1,135 / 696 (prev 0.61) | **3,965 / 2,935 (prev 0.74)** |
| Source positives left outside held area | 88 | **0** |
| Row C (leave-one-scar-out) | 0.592 | **undefined (single class)** |

The 2,151 added TSG burns merge into the one existing scar (2,934 of 2,935 TSG positives; the last is
inside its 2 km buffer). **N does not rise; it falls**: all nine scars remain for rows A, B, D and the
prevalence/pool controls, but only **seven** have row C (Muğla 6, 1, 10, 8; Evia 1; Montiferru 1, 5).
Manavgat now joins Bejís as a single-scar region without row C, so the manuscript's "Bejís is the only
single-scar region without row C" and "eight scars … four in Muğla, two in Montiferru" become seven scars
in three regions. Other regions' scars are unchanged (verified per scar to 4 dp).

## 2. Artefact map and quoted numbers, frozen → corrected

### 2.1 Table 2 and Section 4.3 (`matched_holdout.json`, `pool_decomposition.json`, `prevalence_control.json`, `scar_increment.json`, `positive_control.json`, `d_per_source.json`)

Table 2 statistics recomputed from `matched_holdout.json` exactly as §4.3 defines them (`_logs/table2.py`,
which reproduces the frozen table to 3 dp).

| Quantity | Where | Frozen | Corrected |
|---|---|---|---|
| Scars in Table 2 | 04 §4.3, A(i), A(z) | 8 (4 Muğ, 2 Mont, 1 Evia, 1 Man) | **7 (4 Muğ, 2 Mont, 1 Evia)** |
| Row A | 04:89 | 0.776 [0.738, 0.814] | **0.773 [0.729, 0.818]** |
| Row B | 04:90 | 0.634 [0.552, 0.716] | **0.640 [0.544, 0.736]** |
| Row C | 04:91 | 0.552 [0.501, 0.602] | **0.546 [0.488, 0.604]** |
| Row D | 04:92 | 0.555 [0.495, 0.616] | **0.553 [0.495, 0.611]** |
| A−B, scar-level t (frame cost; abstract, HL1, 1.3, 4.3, 6, A(z), GA) | | +0.143 [+0.077, +0.208] | **+0.133 [+0.059, +0.207]** |
| A−C, scar-level | 04:106 | +0.225 [+0.157, +0.293] | **+0.227 [+0.147, +0.308]** |
| A−B region-clustered | 04:100 | +0.155 [+0.082, +0.228] (G=4) | **+0.137 [+0.048, +0.226] (G=3)** |
| A−C region-clustered | 04:101 | +0.251 [+0.093, +0.409] (G=4) | **+0.266 [−0.022, +0.553] (G=3) — spans zero** |
| "second 2.3 times wider" | 04:101 | 2.3 | **3.6** |
| (A−B)/(A−C) "about two thirds" | 04:104 | 0.635 | 0.586 |
| B−C | 04:112 | +0.082 [−0.011, +0.175] | **+0.094 [−0.012, +0.200]** |
| C−D | 04:113 | −0.003 [−0.075, +0.069] | **−0.007 [−0.070, +0.057]** |
| "bound it at about 0.18" (B−C upper) | 04:115 | 0.175 | **0.200** |
| "three of them starved" | 04:115 | 3 of 8 | 2 of 7 (Manavgat's 88-source-positive arm is gone; Evia scar 1 with 11 and Montiferru scar 1 with 97 source positives remain) |
| Nine-scar controls: A / A′ / B (prevalence_control) | 04:72–73, A(i) Table A4 | 0.782 / 0.782 / 0.627 | **0.791 / 0.793 / 0.644** |
| A−A′ prevalence alone | 04:73 | −0.000 [−0.003, +0.002] | **−0.002 [−0.005, +0.001]** |
| A′−B ("+0.155 against −0.000"; HL2) | 04:74, HL2 | +0.155 [+0.093, +0.217] | **+0.149 [+0.087, +0.211]** |
| Negatives-only (pool_decomposition) | 04:76 | 0.147 [0.104, 0.191] (canonical 0.148 [0.104, 0.192]) | **0.139 [0.098, 0.181]** |
| Positives-only | 04:77 | 0.002 [−0.052, +0.048] | **−0.002 [−0.055, +0.051]** |
| Both pools (B−A′, pool file) | not printed | −0.153 | −0.146 [−0.207, −0.085] |
| Table A4 Manavgat row: prev / A / A′ / B | A(i) | 0.61, 0.797 / 0.796 / 0.589 | **0.74, 0.882 / 0.884 / 0.743** |
| Table A2 Manavgat scar row (scar_control, 2 km) | A(i) | 88 / 696 / 1,135 / 0.592 | **no row (source has 0 positives)** |
| scar_control means 2 / 5 / 10 km | A(i), A(u) | 0.552 (8) / 0.540 (8) / 0.553 (7) | **0.546 (7) / 0.533 (7) / 0.548 (6)** |
| LOSO thermal increment (scar_increment; 4.3, A(z), GA) | 04:124 | +0.022 [−0.032, +0.077], 6 of 8 | **+0.024 [−0.040, +0.089], 5 of 7** |
| Half-split increment (positive_control) | 04:124 | +0.027, 13 of 18 | **+0.028, 13 of 18** |
| Table A1 Manavgat splits (E–W low→high / high→low) src/tgt pos; thermal | A(i) | 700/84, 84/700; 0.695, 0.557 | **1,795/1,140, 1,140/1,795; 0.761, 0.712** (baseline 0.793, 0.638) |
| "two splits unusable because one half of Manavgat has no burned cells" | A(i) | N–S both single-class | **unchanged** (N–S halves still 0 / 2,935) |
| Row D by source: pooled mean, below chance | A(z) | 0.559, 10 of 36 | **0.556, 10 of 36** |
| Row-D spread per scar (mean / max) | A(i), A(z) | 0.164 / 0.329 | **0.183 / 0.329** |
| Table A3 Manavgat scar row mean (min–max) | A(i) | 0.468 (0.407–0.563) | **0.542 (0.438–0.665)** |
| Manavgat-sourced row D, over 8 scars | A(i) | mean 0.558 | **0.506** |
| Row-C patch-definition sweep (scar_definition_sweep) | A2, A(z), A(u) | 0.543 to 0.565 | **0.541 to 0.561** |
| Sweep scar counts | A(z) | "eleven to seven scars" | **nine to six** |

### 2.2 Table 3 (`aoi_frame_transfer.csv` = `aoi_frame_transfer_frozen_mugla.csv`, `transfer_delta_ci.json`, `equalised_delta_interval.json`)

| Row | Printed | Frozen canonical | Corrected |
|---|---|---|---|
| full/full: mean · above · below · supported · Δ | 0.541 · 14 · 6 · 9/4 · +0.004 | 0.541 · 14 · 6 · 9/4 · +0.004 | **0.527 · 13 · 7 · 9/6 · +0.007** |
| full/10 km | 0.576 · 17 · 3 · 11/1 · +0.003 | 0.577 · 17 · 3 · 11/2 · +0.004 | **0.559 · 14 · 6 · 10/2 · +0.008** |
| 10 km/full | 0.570 · 17 · 3 · 11/3 · +0.014 | 0.570 · 17 · 3 · 11/3 · +0.013 | **0.546 · 14 · 6 · 10/5 · +0.014** |
| **10 km/10 km** | **0.616 · 19 · 1 · 15/1 · +0.023** | 0.616 · 19 · 1 · 16/1 · +0.022 | **0.589 · 15 · 5 · 13/2 · +0.024** |
| 5 km/5 km | 0.608 · 19 · 1 · 12/0 · +0.014 | 0.610 · 19 · 1 · 12/0 · +0.017 | **0.591 · 16 · 4 · 11/0 · +0.017** |
| Baseline mean 10 km / as drawn | 0.593 / 0.537 | 0.593 / 0.537 | **0.565 / 0.519** |
| "about six times" (10 km Δ ÷ as-drawn Δ) | 6 | 5.3 | **3.3** |
| "about four times at 5 km" | 4 | 3.9 | **2.3** |
| "5 km and 10 km give 0.608 against 0.616" | 05, A3, supp | 0.610 / 0.616 | **0.591 / 0.589** (5 km now the higher) |
| "reduces the directions below chance, 6 → 1" | 6, 4.4 | 6 → 1 | **7 → 5** |
| Only below-chance direction on the collar (Man→Bej) | 04:243, A(ix) | Man→Bej 0.380 | **five below: Man→Bej 0.407\*, Mug→Man 0.433\*, Bej→Man 0.452, Man→Mug 0.493, Mont→Man 0.497** (\* interval-supported) |
| Full-frame range (as refit) | 04:241 | 0.341/0.326–0.686 | **0.314–0.677** (Bej→Man low; Evia→Man high) |
| "Bejís→Manavgat 0.440 → 0.601" (full → 10/10) | supp:927 | 0.444 → 0.603 | **0.314 → 0.452** |
| "four to one with interval support" (supported below, full → collar) | supp:925 | 4 → 1 | **6 → 2** |
| verify_transfer_counts (1000 reps): full / collar | supp:923 | 9/4, 16/1 | **9/6, 13/2** |
| Equalised 10 km Δ, pair cluster B=1000 (4.4, 1.3) | 04:220 | +0.023 [−0.004, +0.048] | **+0.024 [−0.004, +0.049]** (B=20000: [−0.004, +0.051]) |
| Equalised 10 km Δ, target cluster | 04:222 | [+0.016, +0.031] | **[+0.011, +0.040]** |
| Equalised 5 km Δ pair / target | json | +0.017 [−0.003, +0.037] / [+0.004, +0.029] | **+0.017 [−0.004, +0.036] / [+0.002, +0.033]** |
| As-drawn Δ (A refit; abstract's +0.004 is step9b-based, B) pair cluster B=1000 | abstract, HL5, 4.3, A(o) | +0.004 [−0.027, +0.038] | **+0.007 [−0.020, +0.038]** (B=20000 [−0.021, +0.037]) |
| As-drawn naive / pair t / jackknife t | A(o) | [−0.027, +0.035] / [−0.034, +0.042] / [−0.037, +0.046] | **[−0.023, +0.037] / [−0.028, +0.043] / [−0.018, +0.033]** |
| LOO means Man/Bej/Muğ/Evia/Mont | A(o) | +0.0148/+0.0021/+0.0065/−0.0081/+0.0060 | **+0.0148/+0.0050/+0.0072/+0.0010/+0.0087** |
| "dropping Evia reverses its sign" | A(o) | yes | **no** (+0.0010) |
| Span, positive/negative | A(o) | −0.148 to +0.132, 12/8 | **−0.148 to +0.132, 12/8** |
| `region_count_projection` | not quoted | — | re-run (log only) |

(The published as-drawn +0.004 [−0.028, +0.036] is from step9b deltas — the step9b-based interval needs
the regenerated B file; the refit A analog is given above.)

### 2.3 Section 4.4 signed AUCs and the collar (`aoi_frame_auc.csv`, `aoi_frame_auc_frozen_mugla.csv`, `collar_frame_bootstrap.csv`, `matched_frame_gap.csv`)

| Quantity | Where | Frozen | Corrected |
|---|---|---|---|
| Table B6 Manavgat row: positives / median distance / far-field share | B6 | 784 / 13.4 km / 60.1 % | **2,935 / 13.1 km / 58.5 %** |
| Far-field range "2.1 % to 63.1 %" | 4.4 | — | unchanged (Man inside) |
| Manavgat elevation by band 0–5 / 5–10 / 10–20 / 20–50 km; burned | 4.4, A(o), A(w) | 472 / 501 / 955 / 1,273 m; 512 m | **330 / 723 / 995 / 1,273 m; 287 m** |
| Table B7 Manavgat, full frame: elev / slope / NDVI / LST / anomaly / TVDI / TVDI-diff / downscaled / fused | B7 | 0.374 / 0.531 / 0.636 / 0.538 / 0.482 / 0.552 / 0.449 / 0.552 / 0.540 | **0.232 / 0.400 / 0.564 / 0.665 / 0.509 / 0.677 / 0.460 / 0.683 / 0.666** |
| Collar (≤10 km) Manavgat, same order | 4.4 | 0.561 / 0.569 / 0.621 / 0.386 / 0.462 / 0.392 / 0.437 / 0.388 / 0.386 | **0.376 / 0.438 / 0.551 / 0.522 / 0.487 / 0.527 / 0.438 / 0.533 / 0.522** |
| Collar Manavgat with 10-cell CI: elevation | 4.4, A(w) | 0.561 [0.449, 0.674] | **0.376 [0.300, 0.465] — supported below 0.5** |
| current LST | | 0.386 [0.289, 0.478] (supported below) | **0.522 [0.451, 0.591] — above 0.5, not supported** |
| current TVDI | | 0.392 [0.287, 0.490] | **0.527 [0.453, 0.598]** |
| LST anomaly | | 0.462 [0.398, 0.517] | 0.487 [0.422, 0.553] |
| NDVI | | 0.621 [0.563, 0.674] (supported) | **0.551 [0.484, 0.614] (not supported)** |
| "all five agree in sign on elevation, LST, TVDI" on the collar | 4.4 | yes | **no — Manavgat is on the other side for all three** |
| Elevation on the collar "above 0.5 in all five, supported in two (Muğla, Evia)" | A(w) | yes | **no: Manavgat 0.376 supported below; Muğla 0.606 and Evia 0.648 supported above** |
| LST common direction "0.386, 0.405, 0.332, 0.286, 0.376" | A(w) | all < 0.5 | **0.522, 0.405, 0.332, 0.286, 0.376** |
| Features straddling 0.5 on the collar | 4.4 | anomaly, TVDI-diff only | **elevation, current LST, TVDI, downscaled, fused (and anomaly, TVDI-diff) straddle** |
| 5 km collar Manavgat elev / LST | A(w) "radii agree" | 0.560 / 0.421 | 0.428 / 0.521 (same side as 10 km: yes) |
| Difference instrument, supported opposite-sided pairs on `lst_anomaly_mean` | 4.4, A(l) | 4 (incl. Man–Evia −0.122 [−0.225, −0.020]) | **3** (Man–Evia now −0.097 [−0.210, +0.021]; Man–Bej +0.094 [+0.003, +0.185] excludes 0 but same side) |
| Table A6 Manavgat vs Evia | A(l) | 0.462 vs 0.584 | **0.487 vs 0.584** |
| Reciprocal stratification Manavgat: LST raw / LST\|NDVI / NDVI raw / NDVI\|LST / LST\|dist | A(k) | 0.386 / 0.440 / 0.621 / 0.542 / 0.505 | **0.522 / 0.556 / 0.551 / 0.550 / 0.454** |
| "crosses 0.5 in Manavgat" (LST within distance) | 4.4, A(k) | 0.505 | **0.454** (now: raw collar LST is *above* 0.5 and falls *below* within distance) |
| "holding temperature reverses greenness in two regions" | 6, A(k) | Evia, Montiferru | unchanged (Manavgat NDVI\|LST 0.550 > 0.5) |
| Thermal collinearity on the collar (Manavgat) | A(o) | fused/current 1.00, downscaled 0.97, TVDI 0.97 | 1.00 / 0.97 / 0.98; ranges unchanged |
| Matched within reference, 10 km collar, 5 km blocking | 04:225, A(w) | 0.772 (canonical 0.771) | **0.786** |
| Within reference full / 5 km collar | A(w) | 0.798 / 0.737 (canonical 0.797 / 0.735) | **0.814 / 0.759** |
| Mean transfer full / 10 km / 5 km (gap table) | A(w) | 0.540 / 0.616 / 0.608 | **0.527 / 0.589 / 0.591** |
| Gap full / 10 km / 5 km | A(w) | 0.258 / 0.155 / 0.129 | **0.287 / 0.197 / 0.169** |
| Shortfall paired by target, t over 5 (4.4, 1.3, 6) | 04:226 | +0.155 [+0.094, +0.217] (canonical +0.156 [+0.089, +0.222]) | **+0.197 [+0.091, +0.303]** |
| Per-region shortfall Mont / Man / Muğ / Bej / Evia | A(w) | +0.086 / +0.127 / +0.161 / +0.196 / +0.206 | **+0.081 / +0.319 / +0.172 / +0.202 / +0.211** (Manavgat now the largest) |
| "0.25 unmatched" | 4.4 | 0.25 | 0.29 |
| Muğla two-event arm (`mugla_two_event_collar.csv`) | 4.4, A(m) | — | identical (Muğla only) |

### 2.4 Within-region and collar increments (from `ems_inference_ladder`, same definitions as `verify_collar_increment.py`, which is skipped)

| Quantity | Where | Frozen | Corrected |
|---|---|---|---|
| Manavgat 1 km blocking base / thermal / Δ (step10 within_cv, r3/model_capacity) | Table 1 (B-sourced) | 0.803 / 0.870 / +0.067 | **0.841 / 0.908 / +0.067 [+0.061, +0.073]**; positive-carrying blocks 814 |
| Manavgat 5 km blocking (r3) | Table 1 (B-sourced) | 0.748 / 0.797 / +0.050 | **0.820 / 0.882 / +0.062 [+0.041, +0.082]**; 47 positive blocks |
| Collar (10 km) increment Man / Bej / Muğ / Evia / Mont | A(o), A(w) | +0.039 / +0.030 / +0.087 / +0.134 / +0.090 (canonical) | **+0.073** / +0.030 / +0.087 / +0.134 / +0.090 |
| Collar mean vs as drawn | 04:185 | +0.077 vs +0.086 (canonical +0.076 vs +0.084) | **+0.083 vs +0.087** |
| 5 km collar mean | A(w) | +0.041 (canonical +0.039) | **+0.042** (Man +0.035) |
| Positive in 5/5 at every frame | 04:184 | yes | yes |
| Fold-seed spread Manavgat Δ, B2 / B10 (r6) | not printed | +0.063–0.074 / +0.048–0.060 | +0.066–0.069 / +0.057–0.068 |

### 2.5 Model capacity (`model_capacity.json`; C5(x), A(h))

| Estimator | within thermal / incr | transfer thermal / incr / >0.5 (frozen → corrected) |
|---|---|---|
| rf_canonical | 0.888 → **0.896** / +0.099 → +0.099 | 0.541 → **0.527** / +0.004 → **+0.007** / 14 → **13** |
| rf_shallow | 0.829 → 0.838 / +0.055 → +0.053 | 0.556 → **0.527** / −0.007 → −0.011 / 14 → **13** |
| rf_leaf200 | 0.805 → 0.814 / +0.047 → +0.046 | 0.550 → **0.522** / −0.021 → −0.019 / 14 → **13** |
| logistic | 0.741 → 0.759 / +0.045 → +0.046 | 0.510 → **0.481** / −0.024 → −0.021 / 14 → **11** |

"0.510–0.556, fourteen of twenty for all four estimators" becomes **0.481–0.527, 11–13 of 20**.

### 2.6 A-stg harnesses

| Quantity | Where | Frozen (published) | Corrected |
|---|---|---|---|
| LORO raw thermal, target Man / Bej / Muğ / Evia / Mont (`loro_all.json`; merge is B→M) | Fig. 6, A(n) | 0.469 / 0.417 [0.369, 0.467] / 0.552 / 0.637 / 0.601 | **0.426 [0.369, 0.486] / 0.458 [0.396, 0.522] / 0.506 / 0.715 / 0.560** |
| LORO targets below chance | A(n) | 2 (Man, Bej) | 2 (Man, Bej) |
| Niche overlap Man–Muğ Schoener D̄ (1-D mean) | App D, Fig. 8 | 0.826 | **0.799** |
| Niche Bej–Mont D̄ | App D | 0.479 | 0.479 |
| `scar_control` | A(i) | see §2.1 | see §2.1 |

### 2.7 Step10 `run_e` (CORAL λ sweep, 2-cell CI; A(b))

| Direction | λ = 1e-5 / 1e-3 / 1e-1 / 1 (frozen) | Corrected |
|---|---|---|
| Bej→Man | 0.557 [0.529, 0.586] / 0.564 / 0.547 / 0.485 | **0.408 [0.389, 0.427] / 0.410 / 0.367 / 0.313** — supported *below* chance at every λ |
| Man→Bej | 0.511 / 0.505 / 0.483 / 0.478 | **0.470 [0.444, 0.494] / 0.474 / 0.466 / 0.457** |
| z-score reference Bej→Man / Man→Bej | 0.452 / 0.483 | **0.297 / 0.450** |

### 2.8 ems_geometry (post hoc, response material)

| Quantity | Frozen | Corrected |
|---|---|---|
| Reproduction gate: A, B vs `pool_decomposition.json` (labelfix) | 8/9 to 4 dp | **9/9 exact**; pair/target-cluster checks agree to ~0.001 |
| Band AUC mean, k=0: 0–0.5 / 1–2 / 2–5 / 5–10 / >10 km | 0.615 / 0.668 / 0.748 / 0.803 / 0.830 | 0.641 / 0.693 / 0.769 / 0.814 / 0.845 |
| k=2: 1–2 km vs >10 km | 0.715 [0.623, 0.807] vs 0.865 [0.838, 0.893] | 0.732 [0.633, 0.832] vs 0.877 [0.829, 0.925] |
| **Edge-excluded frame cost, Table-2 set**, k=0 / 1 / 2 | 0.143 / 0.133 / **0.122 [0.042, 0.202]** (8 scars) | **0.133 [0.060, 0.207] / 0.124 [0.039, 0.209] / 0.117 [0.022, 0.212]** (7 scars); region-clustered k=2 [0.065, 0.203] → **[0.003, 0.251]** |
| Share surviving 2-cell exclusion | 85 % | 88 % |
| Script's non-Bejís set (8 scars incl. Manavgat), k=0 / k=2 | 0.143 / 0.122 | 0.134 [0.072, 0.196] / 0.116 [0.037, 0.196] |
| **Placebo**, Table-2 set: A − placebo; placebo − B; share reproduced | +0.001 [−0.070, +0.072]; +0.148 [+0.116, +0.180]; 0.7 % (7 scars with placements) | **+0.007 [−0.070, +0.084]; +0.132 [+0.102, +0.162]; 5 %** (6 scars with placements) |
| Placebo, script's non-Bejís set | as above | +0.001 [−0.063, +0.065]; +0.138 [+0.110, +0.166]; 0.7 % |
| Manavgat scar placebo | 50 placements; 0.798 vs B 0.589 | 50 placements (1,412 candidates); 0.917 vs B 0.743; none ≤ B |
| Far-field slope, region level | +0.046 [−0.373, +0.464] | +0.005 [−0.411, +0.421] |
| Label-free frames (a4): as drawn / collar / trim src full / trim src 10 / AoA full / AoA 10 / 20 km window | 0.541 14 / 0.616 19 / 0.529 13 / 0.553 14 / 0.562 13 / 0.589 14 / 0.485 8 | **0.527 13 / 0.589 15 / 0.520 13 / 0.540 13 / 0.550 13 / 0.574 13 / 0.482 9**; every Δ pair-cluster interval still spans 0 |
| Partial-AUC drop region-wide → scar, Table-2 label set | 0.078 [0.037, 0.120] | 0.080 [0.038, 0.122] (script's non-Bejís set) |

### 2.9 ems_inference

| Quantity | Frozen | Corrected |
|---|---|---|
| Reproduction: LOSO vs `scar_increment.json`; row B vs `matched_holdout.json` | 1e-4; 5e-5 | 9.7e-5; 4.9e-5 |
| **Matched ladder, scar frame, 5 km blocking**: blocked / LOSO / foreign increments | +0.019 / +0.022 / +0.008 (8 scars, 4 regions) | **+0.021 / +0.024 / +0.008 (7 scars, 3 regions)** |
| **Blocked − LOSO (5 km, primary)**: scar t; CR1 t(G−1); cluster bootstrap | −0.004 [−0.060, +0.052]; [−0.092, +0.084]; [−0.064, +0.027] | **−0.004 [−0.070, +0.063]; [−0.148, +0.141]; [−0.084, +0.035]** |
| Blocked − LOSO (1 km) | +0.031 [−0.018, +0.080] | +0.031 [−0.027, +0.090] |
| Blocked (1 km) − foreign, CR1 | +0.045 [+0.007, +0.083] (only matched contrast excluding 0) | **+0.048 [−0.004, +0.099] — now spans 0** (scar t [+0.001, +0.094] still excludes) |
| Rescoring cost (region-wide − blocked-on-scar, 5 km) | +0.071 [+0.001, +0.141] | +0.074 [−0.009, +0.157] (scar t now spans 0) |
| Collar ladder: blocked / half-split / LOSO / cross | +0.076 / +0.036 / +0.000 / +0.023 | +0.083 / +0.039 / −0.005 [−0.053, +0.043] / +0.024 |
| TOST equalised Δ: equivalent within ±0.05 | 5 of 7 dependence-aware units | **4 of 5 defined** (CGM and dyadic now undefined, V < 0); ±0.02: none |
| "no gain larger than X" (pair cluster, 90 %) | 0.045 | **0.047** |
| As-drawn Q1 TOST | computed | **skipped (needs B `transfer_ci_blocksize.json`)** |
| W − T, 10 km collar | +0.053 [+0.004, +0.101], lower 90 % 0.016 | **+0.059 [+0.007, +0.110], 0.019** |
| W − T, 5 km collar | +0.025 [−0.001, +0.052], 0.005 | **+0.026 [−0.012, +0.063], −0.003** (one-sided bound now ≤ 0) |
| Scar frame LOSO − foreign, CR1 95 % | +0.014 [−0.083, +0.112] | +0.016 [−0.154, +0.186] |
| Foreign-increment equivalence ±0.05 under CR1 | yes | **no** (t: yes) |
| **Units**, equalised Δ (Q2): pair / target / source / pigeonhole / CGM / dyadic / jackknife | [−0.004, +0.049] / [+0.016, +0.031] / [+0.003, +0.052] / [−0.011, +0.060] / [+0.007, +0.039] / [+0.006, +0.040] / [−0.038, +0.084] | **[−0.003, +0.051] / [+0.010, +0.040] / [+0.010, +0.042] / [−0.005, +0.060] / undefined / undefined / [−0.017, +0.065]** — units excluding 0: 4 of 7 → **2 of 5 defined** (target, source) |
| Units, equalised mean (Q3) | 0.616; all but jackknife exclude 0.5 | 0.589 [pair 0.534, 0.639]; all but jackknife [0.428, 0.750] exclude 0.5 |
| Units, as-drawn refit Δ (S) | +0.004, spans 0 under all | +0.007, spans 0 under all; LORO means no longer flip at Evia |
| Units, Q1 (step9b as-drawn Δ) | computed | **skipped (B)** |
| **Reversal family, collar, 90 tests** (multiplicity): diff CI excl 0 / opposite & excl / strict / Holm (normal) / Holm IUT | 9 / 4 / **0** / 0 / 0 | **27 / 21 / 2 / 12 / 0** — strict pairs: elevation Man (0.376) vs Muğ (0.606) and vs Evia (0.648) |
| Reversal family, full frame | 27 / 22 / 3 / 11 / 0 | 39 / 31 / 14 / 27 / 5 |
| Diagnostic family (BH over 19) | computed | **skipped (B→M inputs)** |

### 2.10 ems_labels

| Artefact | Result |
|---|---|
| r1_prelabel | Manavgat pre-label window 0 cells (unchanged). V1 now **0 mismatches** for Manavgat (was 624,130 px — the defect itself). Bejís rerun unchanged. |
| r2_history | Manavgat 0 five-year cells in TSG (unchanged). Transfer reference: mean thermal 0.541 → **0.527**, Δ +0.004 → **+0.007**; B10 support +6/−4/?10 → **+6/−5/?9**; B2 +10/−7/?3 → **+12/−7/?1**. Excluded arm Δ +0.0004 → +0.0028. Manavgat within B10 +0.050 → **+0.062 [+0.041, +0.082]**. |
| r3_fraction | Manavgat 2,935 burned, 2,704 with f ≥ 0.5 (231 dropped); Δ B2 +0.067 → +0.062 with f ≥ 0.5, still supported. |
| r4_dimensionality | label-free; identical. |
| r6_calibration | only Manavgat rows move (see §2.4); Bejís random-removal null identical. |
| r5 / r5b | **not re-run: not applicable.** They are the frozen-vs-full-window comparisons that established the correction; under the corrected default their "frozen" arm would be the corrected label (V1 above already shows 0 mismatches). Their "full_window" arm is the corrected label. |

## 3. Verdicts that change

1. **"No reversal survives the collar" is false under the corrected label.** Manavgat's collar elevation
   is 0.376 [0.300, 0.465], interval-supported below 0.5, while Muğla (0.606 [0.525, 0.685]) and Evia
   (0.648 [0.550, 0.740]) are supported above: two strict-criterion elevation reversals survive the 10 km
   collar (also in the multiplicity family: strict 0 → 2; Holm-normal 0 → 12 of 90, though 0 under the
   intersection-union test). "All five agree in sign on elevation, LST and TVDI" on the collar is false.
2. **"Hotter pre-fire surfaces burned less in every region" is false at the point estimate**: Manavgat
   collar current LST 0.522 [0.451, 0.591], downscaled 0.533, fused 0.522 (full frame 0.665 / 0.683 /
   0.666); TVDI 0.527. Four of five, not five. (Manavgat's LST is also not interval-supported either way.)
3. **Table 2 has seven scars in three regions**, not eight; Manavgat has no row C. A − C region-clustered
   now **spans zero** ([−0.022, +0.553]); "2.3 times wider" → 3.6. A − B, A − C scar-level, B − C and C − D
   verdicts (exclude / span zero) are unchanged. LOSO: 5 of 7 positive.
4. **Frame cost** 0.143 → 0.133 [+0.059, +0.207], still excludes zero; region-clustered still excludes
   zero ([+0.048, +0.226]). Edge-excluded (2 cells) region-clustered lower bound falls to +0.003.
5. **Table 3 collar row**: 19 → **15 above chance, 1 → 5 below**, supported 15/1 (printed) → 13/2; the
   "six → one" below-chance reduction becomes **seven → five**; the collar is no longer near-unanimous.
   Mean 0.616 → 0.589; Δ equalised +0.023 → +0.024 (pair-cluster still spans 0, target-cluster still
   excludes). Baseline-control ratio "about six times" → about 3.3 (5 km: about 2.3).
6. **Matched shortfall grows**: +0.155 → **+0.197 [+0.091, +0.303]**; Manavgat is now the largest per-region
   shortfall (+0.319). No longer "numerically almost identical" to the §4.3 negative-pool effect (+0.149).
7. **Model capacity**: all four estimators now transfer at 0.481–0.527, 11–13 of 20 above chance (was
   14/20 for all four).
8. **CORAL λ sweep**: the single above-chance adapted result (Bej→Man CORAL 0.557, CI above 0.5 for
   λ ≤ 0.1) is gone: 0.408 [0.389, 0.427], below chance at every λ.
9. **Resampling units**: the equalised Δ excludes zero under 2 of 5 defined units (was 4 of 7); CGM and
   dyadic-robust estimators become undefined (V < 0). As-drawn jackknife no longer flips sign when Evia is
   dropped. W − T at the 5 km collar: one-sided lower bound becomes negative. Blocked(1 km) − foreign CR1
   interval now spans zero, so no matched contrast excludes zero under CR1.
10. Unchanged verdicts: prevalence alone ≈ 0; negative pool carries the drop (0.139 [0.098, 0.181]);
    positives-only null; half-split 13 of 18; LOSO interval spans zero; as-drawn Δ spans zero under every
    unit; every label-free frame's Δ interval spans zero; collar increment positive in all five; Manavgat
    half-split N–S still single-class; placebo still reproduces ≈ none of the cost; LORO two targets below
    chance.

## 4. Skipped: scripts that consume a class-B pipeline output

| Script | B input it needs |
|---|---|
| `paper/code/anomaly_only.py` | `comparison_inputs.json` rebuilt from new **step9b** (`cross_region/<pair>/step9b` transfer AUCs) and **step8c** (`experiments/manavgat_2021/step8c/step8c_bootstrap_metrics.json`); hard asserts < 5e-4 / < 1e-3 against them |
| `paper/feature_drop.py` | same `comparison_inputs.json` (step9b + step8c), same hard asserts |
| `paper/code/distance_curve.py` | `comparison_inputs.json` transfer block (step9b) for the cross-region points |
| `paper/code/verify_collar_increment.py` | `paper/baseline_vs_thermal_transfer.csv` (step9b/9c → `baseline_vs_thermal.mjs`) for the full-frame transfer vector (its collar increments are reproduced by `ems_inference_ladder`, §2.4) |
| `paper/code/verify_diag_collar.py` | `paper/baseline_vs_thermal_transfer.csv` (full-frame transfer vector) |
| `step10/run_d_within_robustness.py` | `experiments/<region>/step8e/final_step8_report.json` (new Manavgat **step8e**); hard FAIL if block-2 deviates > 0.05 |
| `ems_inference_multiplicity.py` — diagnostic half only | `regime_transfer_correlation.json`, `conditional_similarity_transfer.json`, `niche_overlap_transfer.json`, `all_diagnostics_vs_transfer.csv` (B→M) |
| `ems_inference_units.py` / `ems_inference_equivalence.py` — Q1 only | `transfer_ci_blocksize.json` (`transfer_ci_blocksize.mjs` over step9b predictions, step9c, step10 bootstrap) |
| Merges (not A scripts) | `loro_merge.mjs`, `niche_corr.mjs` need step9b/step8c/step10; raw harness outputs `loro_all.json`, `niche_measures.json` are here |
| `transfer_delta_ci.py` (ran) | its `check_vs_step9b` field and the published step9b-based +0.004 interval need new `baseline_vs_thermal_transfer.csv` |
