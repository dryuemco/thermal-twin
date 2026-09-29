# RUN_LOG — Manavgat label correction, upstream pipeline producers (2026-09-19)

Scratch trees in `thermal-twin/rerun_labelfix/` (untracked): `control` (frozen Manavgat, `054a1961…`)
and `pipeline` (corrected, `e4ab8b85…`), each a copy of `repo/{core,src,scripts,config}` plus the
needed `drive_new` outputs, with stale Manavgat-dependent outputs removed. `repo/` and `drive_new/`
audited before/after (path, size, mtime): **0 differences**. Derived tables: `_derived/`.

## Patches (scratch trees only; no analysis logic, model, seed, fold or bootstrap change)
1. Manavgat hash `054a1961…` → `e4ab8b85…` in `coral_lambda_sensitivity.py:79`,
   `few_shot_recovery.py:160`, `marginal_aoa_completion.py:130`, `mugla_subsampling.py:208`,
   `multi_region_window_closure/inputs.py:33` (pipeline tree).
2. In-process: `V1_EXPECTED_ANALYSIS_ID` of the all_valid large-block module set to the v1 id written in
   the same tree (the id hashes absolute paths).
3. CORAL λ: `PYTHONPATH=<tree>` (runner lacks a sys.path insert) and `subst` drives for MAX_PATH.
Environment: `.venv-step10`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, ≤ 6 threads.

## Controls (frozen Manavgat in scratch vs drive_new)
| Producer | max abs difference |
|---|---|
| gate | exact counts |
| step8b / step8c | 4.4e-16 |
| big_blocks_v2 10/20 | 2.2e-16 |
| large-block v1 and all_valid | ≤ 5.6e-16 |
| Step9A–E + Step10, five modern pairs | ≤ 6.8e-6 (RF thread nondeterminism) |
| legacy manavgat__evia_2021 | 1.3e-5 metrics, 1.3e-4 bootstrap samples |
| step9g, six pairs | 0 (AUC, CI, replicates, reversal tables) |
| concept-shift-compare, transfer-decomposition | 0 |
| synthesis 5/4/3-AOI | ≤ 3.3e-7 |
| burned_pattern_audit | 0 |
| 20-direction matrix from control step10 | ≤ 3.2e-7 |
| CORAL λ | fit-stage reproduction passes; bootstrap pending at time of writing |

All 12 non-Manavgat directions and all non-Manavgat region AUCs are identical under the correction.

## Old → new (corrected label, primary TSG population)
**Table 1, Manavgat:** block 2 0.803/0.870/+0.067 [+0.055, +0.079] → 0.841/0.908/+0.067 [+0.060, +0.073];
block 10 0.748/0.797/+0.050 → 0.820/0.882/+0.062 [+0.040, +0.082]; block 20 0.683/0.731/+0.048 →
0.798/0.845/+0.047 [+0.016, +0.081]. ΔPR block 2 +0.097 → +0.176. all_valid block 2 0.828/0.887/+0.059 →
0.865/0.921/+0.057.

**20-direction matrix:** raw mean 0.541 → 0.527 (range 0.314–0.677; above 14 → 13; supported 12/6 →
11/7); z-score 0.541 → 0.510 (supported 14/2 → 11/5); CORAL 0.552 → 0.517 (supported 15/1 → 10/6; closer
to chance 14 → 16); oracle 0.556 → 0.523; static baseline 0.537 → 0.519; paired thermal − baseline
+0.0042 → +0.0073, span −0.148 to +0.133 unchanged, 12+/8− unchanged; PR-AUC mean 0.156 → 0.181 (no-skill
0.136 → 0.157); below no-skill 6 → 7 (interval-supported 5 → 7).

**Manavgat directions (raw / z / CORAL):** Man→Bej 0.326/0.477/0.511 → 0.396/0.450/0.467; Bej→Man
0.444/0.457/0.555 → 0.314/0.302/0.406 [0.388, 0.423]; Man→Mug 0.470/0.431/0.443 → 0.438/0.427/0.417;
Mug→Man 0.401/0.559/0.560 → 0.345/0.485/0.476; Man→Evia 0.613/0.542/0.539 → 0.654/0.529/0.504;
Evia→Man 0.686/0.516/0.527 → 0.677/0.404/0.417; Mont→Man 0.567/0.573/0.606 → 0.404/0.388/0.436;
Man→Mont 0.533/0.586/0.592 → 0.518/0.527/0.505.

**Decomposition (four-AOI):** Bej→Man recovered +0.26 → +0.15 (chance not excluded); Mug→Man +0.34 →
+0.25; Man→Bej +0.31 → +0.14; Evia→Man −0.86 → −1.13; Man→Evia −0.23 → −0.48; negative recovery 7 of 12
unchanged; maximum recovered fraction 34 % (Mug→Man) → 28 % (Bej→Evia).

**Manavgat signed univariate AUC (10-cell CI; * excludes 0.5):** elevation 0.374* → 0.232*; slope 0.531
→ 0.400*; ndvi 0.636* → 0.564; lst_anomaly 0.482 → 0.509; current_lst 0.538 → 0.665*; current_tvdi 0.552
→ 0.677*; tvdi_difference 0.449 → 0.460; downscaled_lst 0.552 → 0.683*; fused_lst 0.540 → 0.666*.

**Reversals (B3):** bootstrap-supported 3 → **14** (elevation Man–Bej and Man–Muğ; slope Man–Muğ,
Man–Mont; current, downscaled and fused LST Man vs Muğ and Evia; current TVDI Man vs Muğ, Evia, Mont;
lst_anomaly Bej–Evia). Point-only 33 → 26. The text's "twenty-nine" is wrong on the frozen artefacts too.

**burned_pattern_audit, Manavgat:** burned 784 → 2,935; largest component 690 → 2,934; burned-cell
median elevation 508 → 272 m.

## Not run here
Few-shot recovery (ceiling reference for Manavgat block 10 becomes 0.8203 / 0.8822), marginal AoA,
Muğla subsampling (positive-count arm undefined: 2,935 > 2,911), window closure.
