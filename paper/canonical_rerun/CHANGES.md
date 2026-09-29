# Canonical re-run of paper/code — what moved

Date: 2026-09-19. Inputs: `_canonical.load(region)` (drive_new step8a exports, SHA-256 checked
against `CANONICAL_SHA256`). Python `.venv-step10` (numpy 2.4.4, pandas 3.0.2, scikit-learn 1.9.0).
Seed 42, RF and folds unchanged. RF `n_jobs=-1 -> 4` everywhere. Logs: `_logs/*.log`, `_logs/status.txt`.

## 0. What was actually wrong, and where

Hashes of the files the scripts had been reading (`repo/outputs/experiments/.../step8a`, main checkout):

| Region | repo/ file | canonical | same? |
|---|---|---|---|
| manavgat_2021 | 10af6847… | 054a1961… | **no** |
| mugla_2021 | 11ce8e74… | c4ab107d… | **no** (the nested `step8a/step8a/` copy the `frozen_mugla_*` scripts used **is** canonical, c4ab107d) |
| bejis, evia_ext, montiferru | = | = | yes |

So the scripts fall into three groups:

* **Staging-based** (anomaly_only, d_per_source, distance_curve, model_capacity, positive_control,
  prevalence_control, scar_increment, verify_matched): their staging parquets were copies of drive_new, i.e.
  already canonical. They reproduce the published artefacts (exactly, or to ≤1e-4 from float-summation
  tie effects of the n_jobs change). **No printed figure changes.**
* **frozen_mugla_* and pool_decomposition**: Muğla was already canonical; **Manavgat was contaminated**.
* **repo/-readers** (verify_aoi_*, verify_collar_*, verify_diag_collar, verify_matched_gap, verify_mugla_collar,
  scar_definition_sweep, regen_transfer_ci, verify_transfer_counts): **Manavgat and Muğla contaminated**.

Only `downscaled_lst_mean` and `fused_lst_mean` differ, so only arms that fit an RF on the thermal set or use
those two channels move. Univariate arms on other channels (collar_frame_bootstrap, mugla_two_event_collar,
the LST-anomaly difference intervals, reciprocal stratification) are bit-identical.

Cross-check: on canonical inputs the full/full thermal matrix reproduces the frozen step9b export
(anomaly_only's hard assert <5e-4 passed in all 20 directions; paired deltas match
`baseline_vs_thermal_transfer.csv` to 7e-5), and within-region OOF reproduces step8c (<1e-3). The published
`aoi_frame_transfer*.csv` full/full rows did **not** reproduce step9b (e.g. Manavgat→Bejís 0.341 vs 0.326,
range 0.341–0.679 vs step9b's 0.326–0.686); the canonical re-run does.

## 1. Artefact map (script → artefact in this folder)

| Script | Artefact(s) regenerated here | Numeric diff vs published |
|---|---|---|
| anomaly_only.py | `no_coord_channels.json` (superset of `anomaly_only_transfer.json`; the older file lacked the `no_coord_channels` config, all other fields identical by construction) | max 1.8e-6 — unchanged |
| d_per_source.py | `d_per_source.json` | identical |
| distance_curve.py | `distance_curve.json` | identical |
| model_capacity.py | `model_capacity.json` | max 9e-7 — unchanged |
| positive_control.py | `positive_control.json` | max 2e-8 — unchanged |
| prevalence_control.py | `prevalence_control.json` | identical |
| scar_increment.py | `scar_increment.json` | max 1e-4 (one scar) — printed values unchanged |
| verify_matched.py | `matched_holdout.json` (script writes `verify_matched.json`; copied; `paper/matched_holdout.py` is the same script) | identical — **Table 2 unchanged** |
| pool_decomposition.py | `pool_decomposition.json` | moves (Manavgat) |
| regen_transfer_ci.py | `aoi_frame_transfer.csv`; `aoi_frame_transfer_frozen_mugla.csv` is a copy (on canonical inputs the frozen-Muğla override is the canonical file, so the two are the same artefact) | moves |
| verify_aoi_transfer.py | `aoi_frame_transfer.json` (its CSV, without CIs, left in `_staging/`; thermal/baseline identical to regen's to 1e-16) | moves |
| frozen_mugla_verify_aoi_transfer.py | `_staging/frozen_mugla_verify_aoi_transfer.csv/.json` (check only; identical to verify_aoi_transfer to 1e-16) | — |
| verify_aoi_frame.py | `aoi_frame_auc.csv` | Manavgat+Muğla downscaled/fused only |
| frozen_mugla_verify_aoi_frame.py | `aoi_frame_auc_frozen_mugla.csv` | Manavgat downscaled only (≤0.001) |
| verify_collar_ci.py | `collar_frame_bootstrap.csv` | identical |
| verify_collar_increment.py | `collar_increment_and_cosine.csv` | moves (data + NB 400→1000) |
| verify_diag_collar.py | `diagnostics_collar_frame.csv` | moves (data + NB 400→1000) |
| verify_matched_gap.py | `matched_frame_gap.csv` | within-reference rows only |
| verify_mugla_collar.py | `mugla_two_event_collar.csv` | identical |
| scar_definition_sweep.py | `scar_definition_sweep.csv` | moves (Manavgat, Muğla) |
| verify_transfer_counts.py | stdout only (`_logs/verify_transfer_counts.log`) | counts below |
| region_count_projection.py | stdout only (`_logs/region_count_projection.log`); reads `aoi_frame_transfer_frozen_mugla.csv` from here | not quoted in the manuscript |
| transfer_delta_ci.py (new) | `transfer_delta_ci.json`, `equalised_delta_interval.json` (the latter had no stored script) | see §2.4 |

## 2. Quoted numbers, old → new (rounded as printed)

"=" means the printed figure is unchanged.

### 2.1 Table 2 and Section 4.3 (matched holdout, prevalence and pool controls)

| Quantity (source) | Where printed | Old | New | Printed changes? |
|---|---|---|---|---|
| Row A mean [CI], 8 scars (matched_holdout) | 04:92 | 0.776 [0.738, 0.814] | 0.776 [0.738, 0.814] | = |
| Row B | 04:93 | 0.634 [0.552, 0.716] | = | = |
| Row C | 04:94 | 0.552 [0.501, 0.602] | = | = |
| Row D | 04:95 | 0.555 [0.495, 0.616] | = | = |
| A−B scar-level | 04:106, abstract:133 | +0.143 [+0.077, +0.208] | = | = |
| A−C scar-level | 04:106 | 0.225 [+0.157, +0.293] | = | = |
| A−B region-clustered (t over 4 region means) | 04:100 | +0.155 [+0.082, +0.228] | = | = |
| A−C region-clustered | 04:101 | +0.251 [+0.093, +0.409] | = | = |
| B−C / C−D | 04:112–113 | +0.082 [−0.011, +0.175] / −0.003 [−0.075, +0.069] | = | = |
| Prevalence control A, A′, B (9 scars) | 04:72–73, supp:294 | 0.782, 0.782, 0.627 | = | = |
| A−A′ (prevalence alone) | 04:73, supp:293 | −0.000 [−0.003, +0.002] | = | = |
| A′−B | 04:74, supp:294 | +0.155 [+0.093, +0.217] | = | = |
| Negatives-only cost (pool_decomposition A′−C) | 04:76 | 0.147 [0.104, 0.191] | **0.148 [0.104, 0.192]** | **yes** |
| Positives-only (D−A′) | 04:77 | 0.002 [−0.052, +0.048] (per-scar −0.12…+0.12) | +0.0016 [−0.048, +0.052]; printed form unchanged | = |
| Both pools, pool file (B−A′) | commit d1925df only | −0.152 [−0.214, −0.091] | −0.153 [−0.215, −0.092] | not printed |
| LOSO thermal increment (scar_increment) | 04:124, supp:1177, abstract | +0.022 [−0.032, +0.077], 6 of 8 | = | = |
| Half-split increment (positive_control) | 04:124 | +0.027, 13 of 18 | = | = |
| Row D by source (d_per_source) | supp A(z) | pooled 0.559, 10 of 36 below | = | = |

### 2.2 Table 3 (aoi_frame_transfer_frozen_mugla.csv; 10-cell block bootstrap, 1000 reps — unchanged count)

| Row | Printed (04:197–201) | New | Printed changes? |
|---|---|---|---|
| full/full | 0.541 · 14 · 6 · 9/4 · +0.004 | 0.541 · 14 · 6 · 9/4 · +0.004 | = (0.5409→0.5414, 0.0038→0.0042) |
| full/10 km | 0.576 · 17 · 3 · 11/1 · +0.003 | **0.577** · 17 · 3 · **11/2** · **+0.004** | **yes** |
| 10 km/full | 0.570 · 17 · 3 · 11/3 · +0.014 | 0.570 · 17 · 3 · 11/3 · **+0.013** | **yes** (delta 0.0136→0.0133) |
| 10 km/10 km | 0.616 · 19 · 1 · 15/1 · +0.023 | 0.616 (0.6163→0.6155) · 19 · 1 · **16/1** · **+0.022** | **yes** |
| 5 km/5 km | 0.608 · 19 · 1 · 12/0 · +0.014 | **0.610** · 19 · 1 · 12/0 · **+0.017** | **yes** |
| Baseline mean, 10 km / as drawn | 04:210, 05, abstract | 0.593 / 0.537 | = | = |
| "about six times larger" (10 km delta ÷ as-drawn) | 04:211, supp:921 | 0.0231/0.0038 = 6.1 | 0.0223/0.0042 = **5.3** | **yes** ("about five") |
| "about four times at 5 km" | 04:212 | 0.0138/0.0038 = 3.6 | 0.0165/0.0042 = 3.9 | = |
| "5 km and 10 km give 0.608 against 0.616" | 05:101, A3:54, supp:946 | 0.608 | **0.610** | **yes** |
| Bejís→Evia full → 10/10 | supp:927 | 0.383 → 0.602 | = | = |
| Bejís→Manavgat full → 10/10 | supp:927 | 0.440 → 0.601 | **0.444 → 0.603** | **yes** |
| Full-frame thermal range (4.5 quotes step9b) | 04:241 | 0.326–0.686 | canonical matrix now reproduces this (published CSV gave 0.341–0.679) | = |
| Only below-chance direction at collar | 04:243 | Manavgat→Bejís | = (0.417→0.380) | = |
| Provenance note "moves forty of a hundred values by up to 0.022 … every headline unchanged to within 0.0012" | 04:203–206, supp:903–907 | — | vs the published frozen-Muğla file, **41 of 100** thermal values move, by up to **0.037** (all involve Manavgat; Manavgat→Bejís 10/10 0.417→0.380); headline means move ≤0.0027 (5 km delta 0.0138→0.0165) | **yes — statement no longer true** |

Per-direction support flips (10-cell, 1000 reps): full/10 km **Manavgat→Bejís** now interval-supported below
(0.424 [0.348, 0.505] → 0.407 [0.334, 0.487]); 10/10 **Manavgat→Muğla** now supported above
(0.550 [0.493, 0.607] → 0.560 [0.502, 0.617]). `verify_transfer_counts` (NB now 1000) agrees: full 9/4,
collar 16/1. "Four to one with interval support" (supp:925, 4 below → 1 below) is unchanged; the supported-above
side is 9 → 16 (was 9 → 15).

### 2.3 Matched gap and collar increment (Section 4.4, A(o)/A(w))

| Quantity | Where | Old | New | Printed changes? |
|---|---|---|---|---|
| Within reference, 10 km collar, 5 km blocking | 04:225, supp:945 | 0.772 | **0.771** | **yes** |
| Within reference full rectangle / 5 km collar | supp:944/946 | 0.798 / 0.737 | **0.797 / 0.735** | **yes** |
| Mean transfer full / 10 km / 5 km (gap table) | supp:944–946 | 0.540 / 0.616 / 0.608 | **0.541** / 0.616 / **0.610** | **yes** |
| Gap full / 10 km / 5 km | supp:944–946 | 0.258 / 0.155 / 0.129 | **0.255** / 0.155 (0.1555) / **0.125** | **yes** (two of three) |
| Shortfall paired by target, t over 5 | 04:226, supp:948 | +0.155 [+0.094, +0.217] | **+0.156 [+0.089, +0.222]** | **yes** |
| Per-region shortfall Montiferru/Manavgat/Muğla/Bejís/Evia | supp:949 | +0.086/+0.127/+0.161/+0.196/+0.206 | +0.086/**+0.122**/**+0.156**/**+0.208**/+0.206 (Bejís is now the largest) | **yes** |
| Collar (10 km) increment per region | supp:597–598 | +0.041, +0.030, +0.091, +0.134, +0.090 | **+0.039**, +0.030, **+0.087**, +0.134, +0.090 | **yes** |
| Collar mean increment vs as drawn | 04:185, supp:599 | +0.077 vs +0.086 | **+0.076 vs +0.084** | **yes** |
| 5 km collar mean increment | supp:600 | +0.041 | **+0.039** | **yes** |
| Positive in 5/5 at every frame | 04:184 | yes | yes | = |
| Supported-subset cosine, collar | 04:174, abstract:120, supp:1474 | ρ = −0.06 (p = 0.82, n = 18), var 0.00014 | **ρ = −0.004 (p = 0.99, n = 18)**, var 0.00014 | **yes** (data change: same at NB=400) |
| Supported-subset cosine, full frame | supp:1474 | +0.81 (p = 0.0005, n = 14) | +0.81 (p = 0.0002, **n = 16**) | n and p change |

### 2.4 Diagnostics on the collar (diagnostics_collar_frame.csv; NB 400 → 1000)

| Quantity | Where | Old | New | Printed changes? |
|---|---|---|---|---|
| Agreement fraction, full frame | supp:1473 | ρ = +0.86 (p = 0.0001, n = 14) | **ρ = +0.84 (p < 0.0001, n = 16)** | **yes** (replicate count; at NB=400 on canonical data it is still +0.86, n = 14) |
| Agreement fraction, collar | 04:172, supp:1473 | 1.0 in all 18, variance 0 | = | = |
| All-nine cosine full / collar | supp:1475 | +0.50 (p = 0.023) / +0.12 (p = 0.61) | +0.50 / **+0.16 (p = 0.49)** | **yes** (collar; data change) |
| Features supported in both, full → collar | 04:160, supp:857 | 1.20 → 3.40 | **1.40** → 3.40 | **yes** (replicate count) |
| "ρ = +0.86 over fourteen directions against the +0.84 over sixteen in Appendix D … three pairs carry no jointly supported feature rather than two" | supp:552–554 | — | at 1000 reps the full-frame value is **+0.84 over sixteen, reproducing Appendix D**; the stated discrepancy disappears | **yes — caveat obsolete** |

### 2.5 Paired thermal delta intervals (transfer_delta_ci.json, equalised_delta_interval.json)

Pair-cluster bootstrap over the 10 unordered pairs (both directions together), as in
`referee2_numbers.mjs` block A. Primary B = 1000 (Methods); B = 20000 reported because the published
figures used it. The as-drawn deltas equal step9b's (max diff 7e-5), so **for the abstract quantity the
change is Monte Carlo (numpy RNG, B), not data**.

| Quantity | Where | Old | New B=1000 | New B=20000 | Printed changes? |
|---|---|---|---|---|---|
| As-drawn mean, pair cluster (**abstract's +0.004**) | abstract:133, highlights:19, 04:126, supp:572, 1178 | +0.004 [−0.028, +0.036] | +0.004 **[−0.027, +0.038]** | +0.004 [−0.027, +0.035] | **yes** (either B) |
| Naive, directions | supp:571, 04:267, supp:999 | [−0.027, +0.034] | [−0.027, +0.035] | [−0.027, +0.034] | yes at B=1000 |
| Pair t / region jackknife | supp:573–574 | [−0.034, +0.042] / [−0.037, +0.046] | = (deterministic) | = | = |
| LOO means Man/Bej/Muğ/Evia/Mont | supp:577 | +0.0148/+0.0021/+0.0065/−0.0081/+0.0060 | = | = | = |
| Span, 12 positive / 8 negative | supp:561 | −0.148 to +0.133 | = | = | = |
| **Equalised 10 km paired delta, pair cluster** | 04:220 | +0.023 [−0.004, +0.048] | **+0.022 [−0.003, +0.047]** | +0.022 [−0.003, +0.047] | **yes** |
| Equalised 10 km, target-region cluster | 04:222 (text), json | [+0.016, +0.031] | [+0.016, +0.030] | [+0.016, +0.030] | not printed |
| Equalised 5 km pair cluster / target cluster | json only | +0.014 [−0.008, +0.035] / [+0.002, +0.028] | +0.017 [−0.003, +0.037] / [+0.004, +0.029] | — | not printed |

Reimplementation check: run on the *published* frozen-Muğla CSV, transfer_delta_ci.py gives equalised
10 km [−0.0034, +0.0484] (B=20000) against the stored [−0.0043, +0.0482] — agreement to ~0.001 (RNG /
unrecorded implementation; the producer of `equalised_delta_interval.json` is not in the tree).

### 2.6 Other arms

| Quantity | Where | Old | New | Printed changes? |
|---|---|---|---|---|
| Row-C robustness across patch definitions (scar_definition_sweep) | A2:30/125/189, supp:162/766/1165 | 0.545 to 0.566 (also "0.543 to 0.565" in its docstring) | **0.543 to 0.565** | **yes** |
| Published row C (min 50, 8-conn) in sweep | — | 0.5527 | 0.5518 (Table 2's 0.552 is from matched_holdout and unchanged) | = |
| Signed univariate AUCs (aoi_frame_auc*) | 04 §4.4, A(w) | Manavgat downscaled ≤0.001, Muğla downscaled ≤0.008 | no side of 0.5 changes; same features straddle 0.5 | = |
| Collar signed-AUC intervals, Evia by 0.003 (collar_frame_bootstrap) | 04:157 | — | identical | = |
| LST-anomaly difference instrument: four opposite-sided pairs supported (matched_frame_gap) | 04:153 | 4 | 4 (identical) | = |
| Reciprocal stratification / LST-within-distance | A(k) | — | identical | = |
| Thermal-channel collinearity on the collar (fused 0.99–1.00, downscaled 0.97–0.99) | supp:544–545 | — | identical ranges | = |
| Two-event Muğla arm (93.2 % vs 55.3 %, elevation verdicts) | 04:178 | — | identical | = |
| Model capacity, anomaly-only / no-coord, distance curve, positive control | supp | — | unchanged (≤2e-6) | = |

## 3. Verdicts and counts that change

1. **Table 3, 10 km/10 km: supported above 15 → 16** (Manavgat→Muğla now clears 0.5, lower bound 0.502).
   The "one below with support" and the "four to one" below-chance movement are unchanged.
2. **Table 3, full/10 km: supported below 1 → 2** (Manavgat→Bejís interval now entirely below 0.5).
3. **Section 4.4's provenance paragraph is no longer accurate**: it says the correction left every headline
   quantity unchanged to within 0.0012. Relative to the published frozen-Muğla matrix, the Manavgat fix
   moves 41/100 per-direction values by up to 0.037 and the 5 km paired delta by +0.0027 (0.014 → 0.017).
   The correction the paper applied was incomplete (Manavgat was contaminated too).
4. **Baseline-control ratio**: "about six times larger" becomes about five (5.3).
5. **Per-region shortfall ordering**: Bejís (+0.208) now exceeds Evia (+0.206) as the largest.
6. **Appendix full-frame diagnostic caveat (supp:552–554) is obsolete** at 1000 replicates: the full-frame
   agreement fraction is +0.84 over 16 directions, i.e. the published Appendix D value; the "+0.86 over
   fourteen" row of the collar Table 3 came from 400 replicates.
7. Supported-subset cosine on the collar: −0.06 → −0.004. Verdict (does not track transfer) unchanged.

Verdicts that **do not** flip: the equalised paired delta's pair-cluster interval still spans zero
([−0.003, +0.047]) and its target-region interval still excludes it; the as-drawn +0.004 interval
spans zero; the matched shortfall excludes zero; the collar increment is positive in 5/5 at every frame;
the agreement fraction is still degenerate (1.0 × 18) on the collar; no signed AUC changes side of 0.5;
Table 2 and every Section 4.3 control except the negatives-only figure (0.147 → 0.148) are identical.

## 4. Replicate-count decisions (Methods 3.13: 1000 throughout)

| Script | Was | Now | Note |
|---|---|---|---|
| verify_collar_increment.py | NB=400 | 1000 | Appendix Table 3 note states 1000 for this source |
| verify_diag_collar.py | NBOOT=400 | 1000 | same |
| verify_transfer_counts.py | NB=400 | 1000 | supp:923 states 1000 for these counts |
| region_count_projection.py | pair CI 400; inner simulation bootstrap 200 | 1000 / 1000 | projection, not quoted in the manuscript; REPS=2000 is cohorts, not replicates, left |
| transfer_delta_ci.py (new) | published 20000 (referee2_numbers.mjs) | 1000 primary, 20000 also reported | manuscript never states 20000 |
| equalised_delta_interval.json | 20000 | 1000 (both in transfer_delta_ci.json) | producer not in tree |
| all others | 1000 already | unchanged | pool/prevalence `DRAWS=20` are subsamples, not bootstrap replicates; left |

Separating replicate-count from data effects (canonical data, NB=400 re-runs in scratch): agreement-fraction
full frame +0.86 (n=14) and supported-in-both 1.20 are the NB=400 values; the move to +0.84 (n=16) and
1.40 is the replicate count. The collar cosine (−0.004) and all-nine collar cosine (+0.16) are the same at
NB=400, so those moves are data.

## 5. Figures

| Figure | Data source (provenance / script) | Reads changed data? |
|---|---|---|
| fig1 study map | `figures/data/fig1_aoi.json` (step0 geojson, drive_new) | no |
| fig2 schematic | none | no |
| fig3 within robustness | `fig_data.json` ← drive_new step8c + robustness | no |
| fig4 transfer matrix | `fig_data.json` ← drive_new step10_metrics (canonical, frozen) | no |
| fig5 adaptation | `fig_data.json` ← drive_new four_aoi_decomposition.csv | no |
| fig6 LORO | `fig_data.json` ← `paper/loro_pooled_transfer.json` (not produced by paper/code; staging harness from drive_new) | not re-run; no evidence of contamination |
| fig7 feature drop | `fig_data.json` ← `paper/feature_drop_transfer.json` (feature_drop.py asserts step9b reproduction) | not re-run; no evidence of contamination |
| fig8 contrast pairs | `paper/figure_contrast_pairs.json` (records canonical hash prefixes 054a1961/c4ab107d) | no |
| **graphical abstract** | parses `04_results.md` at build time: 0.143 [0.077, 0.208], LOSO 0.022 [−0.032, 0.077], **across regions 0.004 [−0.028, 0.036]** (hard `assert`), 0.541/0.616/0.537 | **yes, via the text**: if 04:126 is updated to the re-run interval, `graphical_abstract.py`'s assert on (−0.028, 0.036) fails and must be updated with it |

## 6. Run notes

* All 22 scripts plus transfer_delta_ci.py ran to rc=0. `verify_mugla_collar.py` failed at first because
  `paper/mugla_temporal_raw/.../component_membership.parquet` is untracked and absent from this worktree
  (unrelated to the path change); it was re-run unchanged with cwd = the main checkout, which has the file.
* `comparison_inputs.json` (the step9b/step8c reference values anomaly_only and distance_curve need) was
  rebuilt into `_staging/` from drive_new: transfer references as `paper/anomaly_stage.py` does; within
  references from `step8c_bootstrap_metrics.json` → `overall_point_estimates_from_predictions` (anomaly_stage's
  walker finds nothing in that layout).
* Derived-artefact paths (`aoi_frame_transfer.csv` read by verify_collar_increment/verify_diag_collar/
  region_count_projection and written by regen_transfer_ci) now honour `PAPER_ARTEFACTS` (default `paper`,
  i.e. unchanged behaviour); this re-run set it to `paper/canonical_rerun`. `baseline_vs_thermal_transfer.csv`
  (step9b frozen) is still read from `paper/`.
