# Label-fix re-run, round 4 — results (2026-09-23)

Plan and gates: `PLAN_R4.md`. Checkers: `checkers/g1_check.py` (control vs frozen, all rows) and `checkers/g2_check.py`
(corrected vs frozen/control, non-Manavgat rows must be equal; unmatched non-Manavgat rows fail). Both were
negative-tested on a copy of `baseline_vs_thermal_transfer.csv` with one non-Manavgat number (+0.01) and one
non-Manavgat verdict string changed: both FAIL as they should.

Arms: frozen = `drive_new/` (pipeline) or `thermal-twin-main/paper/canonical_rerun/` (paper scripts);
control = `rerun_labelfix/control` (frozen Manavgat label `054a1961…`); corrected = `rerun_labelfix/pipeline`
(`e4ab8b85…`) and `thermal-twin-main/paper/labelfix_rerun/round3/`.

## Gate results

| # | Job | G1 control = frozen | G2 non-Manavgat unchanged | Notes |
|---|---|---|---|---|
| N3 | Marginal AoA completion | PASS, 10/10 tables, max 4.6e-13 | PASS, all 10 tables | Only Manavgat rows move (source feature weights come from RF importances). |
| N3 | Marginal area of applicability (its input) | PASS, 25/25 tables, max 0 | Corrected = frozen on all 25 tables (label-free) | — |
| N3 | Set-aside AoA runs `_round3/aside/aoa_*_no_unweighted{,_2}` | — | — | First two runs came before the `marginal_area_of_applicability` sidecar existed. The only differences are the four `unweighted_*` columns, which are NaN in those runs. The final run has them. drive_new before/after listing is identical. |
| N4 | CORAL λ sweep (RUN_LOG: "bootstrap pending") | PASS, 6/6 tables, max 1.4e-7 | PASS, 504 non-Manavgat rows | The bootstrap completed (`CORAL_D_DONE`). |
| N5 | `aside/no_coord_channels_firstrun.json` | — | — | Identical to the final file (1,318 leaves, 0 differences). It is a backup copy taken before a re-run that reproduced exactly. |
| N5 | `referee2_numbers` prints "undefined" ×5 | — | — | The frozen control run (`F_r2.log:171-175`) prints the same lines. They are a debug print of fused-LST stats keys and feed no number. |
| N1 | Few-shot recovery (`_round3/runners/fsr_driver.py`; ceiling reference read from the tree's corrected block-10 run, 0.82032/0.88222) | **Marginal FAIL at the pre-set 1e-5: max 1.25e-5.** Only 2 of 7,056 recovery-curve cells and 2 of 254,448 repeat cells exceed 1e-5. Every text/verdict column is identical, and feasibility and block inventory are exact. The maximum sits in `recovery_fraction`, a ratio that amplifies an AUC difference of 1.1e-5 (Bej→Man baseline, 1 block). Same analysis_id as frozen (`7e4ca051…`); validator PASS. This is consistent with RF thread nondeterminism: the order of the parallel predict_proba sums flips AUC ties. 09-19 accepted 1.3e-5 on the same grounds (legacy manavgat__evia). **Accepted by the user on 2026-09-23 (see Decisions §1). The tolerance itself was not changed.** | PASS: Bej↔Muğ over 84 recovery-curve rows and 4,464 repeat rows, max 2.7e-6 (RF thread nondeterminism, 09-19 level ≤ 6.8e-6); feasibility and block inventory exact | Module validator: OVERALL PASS. Fit accounting 3,642/3,642 as expected. Ceiling reproduction matches for all six (region, model). The 09-19 attempt never ran to completion (empty log). |
| 3 | distance_curve | canonical_rerun reproduced frozen (09-19) | PASS: 12 cross + 48 within non-Manavgat rows, max 0 | — |
| 5a | verify_diag_collar | as above | PASS: 24 non-Manavgat rows, max 0 | — |
| 5b | verify_collar_increment | as above | PASS: 12 non-Manavgat rows, max 0 | — |
| 3b | feature_drop (raw, then `feature_drop_merge.mjs`, which the round-3 queue never ran) | PASS: frozen-arm merge = published `paper/feature_drop_transfer.csv`, max 0 | PASS: 64 non-Manavgat rows, max 0 | Hard asserts vs step8c: diff 0.0000 in all five regions; step9b parity 0. |
| 7a | ems_inference_units / _equivalence, Q1 now computed | — | Every non-Q1 leaf equals the 09-19 corrected run. The only "differences" are NaN ≠ NaN in the already-undefined CGM and dyadic rows. | `loro_means["Manavgat"]` (the mean with Manavgat dropped) is identical in both arms, which is an internal G2. |
| 7b | ems_inference_multiplicity | — | Reversal family identical to the 09-19 corrected run (max 0). Diagnostic half newly computed. | — |
| 7c | transfer_delta_ci, step9b cross-check | — | All intervals identical to 09-19. | `check_vs_step9b` goes 0.0605 → **0.00006**: the paper-side refit and the regenerated pipeline step9b agree. The 0.0605 came only from comparing against the frozen step9b. Run with ART = `_round4/tdci/`, a copy of the same class-A input (byte-identical), so nothing committed is overwritten. |
| 6 | step10 run_d within-robustness | — | **Reference stale, not a failure.** Bejís rows differ from the committed `experiments/cross_region/step10/within_robustness_summary.csv` by ≤ 0.0012. That file dates from 2026-07-16 (before the canonical drive_new data): its Bejís block-2 baseline is 0.8615, while canonical `drive_new` step8e gives **0.8617 / 0.9178**, which is exactly what the new run gives. run_d's own block-2 reproduction against canonical step8e: 0.0000 deviation in all four rows. | The round-3 queue never ran it: `_env.sh` overwrites `$R`, so `bash $R` executed a directory. Runner bug fixed in `_round4/queue_paper.sh`. |
| new | **step8d thermal ablation, Manavgat** (`_round4/step8d.py`, which calls the pipeline's `run_step8d(ctx)`, same pattern as `_runners/step8bc.py`) | PASS, 5/5 tables, max 4.4e-16. The step8e report regenerated after step8d matches frozen on every number (max 2.2e-16). | n/a (one region) | Not in the 09-19 inventory. Before this, the regenerated step8e reports lacked the step8d section (815 vs 2,426 leaves). The 37 remaining text differences in step8e are metadata only (`results_ran.*` is empty in report-only mode, plus context tags that the CLI's `_enrich_metadata_with_experiment_context` adds), identical across arms. |
| N6 | G3: `repo/` and `drive_new/` path/size/mtime before (2026-09-23 start), mid-run and after | — | — | **0 differences** in both trees (3,160 and 7,938 files). |

## What moved (frozen → corrected), no gate

- **Q1, as-drawn thermal − baseline transfer Δ (20 directions):** mean +0.0042 → +0.0073. It spans zero
  under every defined unit, as before. TOST at ±0.02: target-cluster equivalence **True → False** (90 % CI
  [−0.0051, +0.0149] → [−0.0056, +0.0208]). Every other unit is unchanged (±0.02 False, ±0.05 True).
- **Diagnostic multiplicity family (BH/Holm over 20 measures):** the frozen result had two significant
  measures, both conditional similarity on supported features: `agree_fraction_supported` ρ = 0.84
  (n = 16, BH 0.001) and `cosine_supported` ρ = 0.81 (BH 0.010). **Under the corrected label both vanish:**
  ρ is 0.52 and 0.49, BH 0.73. Net: the one diagnostic family that ordered transfer under the frozen label
  (C4, conditional similarity) no longer does.
  **Not used:** `vector_spearman_supported` came out significant (ρ = 0.96, BH 0.001), but it rests on 6
  directions with a degenerate bootstrap interval (upper bound = point estimate, [0.853, 0.956]). It was not
  computable under the frozen label. Promoting it after the other measures failed would be a forking path,
  so it is not interpreted and not cited as evidence. **Superseded the same day (stage D):** it is one of the 20
  pre-fixed candidates, so it stays in the diagnostics table, flagged (6 directions, degenerate interval, not
  comparable with the other 19). Dropping a fixed candidate after seeing its result would itself be a forking
  path. The candidate set was fixed before computation and stays fixed.
- **Within-region robustness, Manavgat (TSG):** ΔAUC at blocks 2/10/20 is +0.067 [+0.061, +0.073],
  +0.062 [+0.041, +0.082] and +0.047 [+0.016, +0.081]. It is positive at every block, the same verdict
  as frozen (+0.067/+0.050/+0.049). all_valid is also positive at every block.
- **Few-shot recovery (thermal ROC-AUC; recovery fraction = (few-shot − raw)/(ceiling − raw)):**
  | Direction | raw | ceiling | 1 block | 4 blocks | 32 blocks |
  |---|---|---|---|---|---|
  | Bej→Man | 0.444 → 0.314 | 0.797 → 0.882 | 0.03 → **0.36** | 0.17 → 0.61 | 0.85 → 0.89 |
  | Man→Bej | 0.326 → 0.396 | 0.824 | 0.30 → 0.12 | 0.56 → 0.34 | 0.89 → 0.83 |
  | Man→Muğ | 0.470 → 0.438 | 0.777 | 0.04 → 0.03 | 0.13 → 0.09 | 0.51 → 0.39 |
  | Muğ→Man | 0.401 → 0.345 | 0.797 → 0.882 | 0.03 → 0.02 | 0.12 → 0.12 | 0.57 → 0.52 |

  The pattern is unchanged: recovery grows monotonically with target labels and is far from complete at
  small budgets, except Bej→Man, where a single target block now recovers about a third of the gap.
- **step8d ablation, Manavgat TSG (ΔAUC over baseline):** all_thermal +0.0669 → +0.0669 (rank 1 in both);
  tvdi_group +0.065 → +0.062 (rank 2 in both). Ranks 3–5 reorder: downscaled_only +0.059 → +0.050 (3 → 5),
  lst_anomaly_group +0.056 → +0.058 (5 → 3). Every single-group ablation stays positive (the smallest is
  lst_anomaly_only, +0.033 → +0.038).
- **feature_drop, supported gains/losses:** drop_elev gains 3 → 4 (adds Bej→Man); drop_anom gains 3 → 4
  (adds Evia→Man) and losses 2 → 3 (adds Mont→Man); drop_both is unchanged in count (5/3; Bej→Man replaces
  Mug→Man among the gains). Every change is a Manavgat direction.

- **Marginal AoA, primary rank correlations with raw thermal transfer (n = 12):** ρ goes from −0.24…+0.22 to
  −0.17…+0.21. Mean |ρ| over all 54 rows is 0.144 → 0.157. The conclusion is unchanged: no diagnostic
  orders transfer.
- **CORAL λ (Man↔Muğ, Bej↔Muğ):** the maximum deviation from canonical over the λ grid stays ≤ 0.0125, with
  no numerical failures. On Manavgat directions only, some tokens change between `modest_lambda_sensitivity`
  and `insensitive_over_grid` (Man→Muğ baseline ROC and Brier become insensitive; Man→Muğ thermal ROC
  deviation is 0.0075 → 0.0094). The conclusion is unchanged: CORAL is insensitive to λ in these directions.

## Decisions (user, 2026-09-23)

1. **Few-shot G1, max 1.25e-5 against the pre-set 1e-5: ACCEPTED.** Four of 261,504 cells exceed 1e-5.
   Every decision and text column is identical, the analysis_id is the same, and the validator passes.
   The cause is RF parallel nondeterminism: the summation order of predict_proba across threads flips AUC
   ties. The same reason was accepted for 1.3e-5 on 2026-09-19. The tolerance itself was not changed.
2. **Window closure: NO shim.** A shim that drops `historical_burn_excluded` would depart from the pipeline
   that Methods describes. The route was to request commit `734d621` from Emrehan. **Update, same day:**
   Emrehan is no longer active, so that commit cannot be obtained. The job stays blocked and needs a new
   decision.
3. **Muğla subsampling: conditional approval, path mapping only.** Not written. The frozen layout has
   `cross_region/mugla_2021__manavgat_2021/step9{a..e}` as a pair of its own. The Manavgat re-freeze
   (stage A) re-runs that pair natively, so the module will find its input without any shim. Re-evaluate
   after stage A.
4. **Landsat composite / harmonisation A/B chain: DEFERRED** until it is clear what the paper claims. Not
   started.
5. **Muğla positive-matched supplement (`paper/mugla_positive_matched.*`): WITHDRAWN, not re-specified.**
   The design (10 stratified draws of 20,511 Muğla rows with exactly `target_positives = 784`, Manavgat's
   frozen TSG positive count) is infeasible under the corrected label: 2,935 target positives exceed
   Muğla's 2,911. Changing the design after seeing the result is what the study avoids. The files are
   kept, with a withdrawal header.
6. `round3/` and this round-4 record are committed to `main` (they carry inputs of the pre-registration's
   precision analysis).

Diagnostics not used: see the multiplicity bullet above (`vector_spearman_supported`).
